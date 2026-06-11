/**
 * sync.js — Sincronización offline-first (HANDOFFCES §3.4 y §5.2 C.4).
 *
 * Principios innegociables:
 *  - LocalStorage sigue siendo la verdad inmediata; el servidor es respaldo
 *    y puente entre dispositivos. La app JAMÁS bloquea por falta de red.
 *  - Todo aquí es silencioso: un fallo deja la cola intacta y se reintenta
 *    en el próximo disparo (arranque, evento encolado, volver online).
 *  - El historial se UNE (event log append-only no colisiona); los
 *    contadores derivados (rachas) se RECOMPUTAN. Nada de CRDTs: el caso
 *    real es una persona con 2-3 dispositivos.
 *  - Las API keys de Claude (cps_mentorIA) NUNCA viajan (exclusión en
 *    Storage.CLAVES_SYNC).
 */

import * as Storage from './storage.js';
import * as Api from './api.js';

let sincronizando = false;
let timerProgramado = null;
const oyentes = [];

/* ====================== Estado para la UI ============================ */

export function estado() {
  return {
    configurado: Api.configurado(),
    sesion: Api.sesionActual(),
    pendientes: Storage.load('outbox').length,
    ultimaSync: Storage.load('ultimaSync'),
  };
}

export function alCambiarEstado(fn) {
  oyentes.push(fn);
}

function avisar() {
  oyentes.forEach((fn) => {
    try {
      fn(estado());
    } catch {
      // Un oyente roto no debe tumbar la sincronización.
    }
  });
}

/* ====================== Disparadores ================================== */

/** Conecta los disparadores automáticos. Llamar una vez desde app.js. */
export function iniciar() {
  window.addEventListener('online', () => sincronizar());
  window.addEventListener('cps:evento-encolado', () => programar());
  sincronizar(); // intento inicial (no-op sin sesión o sin red)
}

/** Drenado con debounce: agrupa varios eventos cercanos en una subida. */
export function programar(ms = 3000) {
  clearTimeout(timerProgramado);
  timerProgramado = setTimeout(() => sincronizar(), ms);
  avisar();
}

/* ====================== Subida (outbox + snapshot) ==================== */

function snapshotLocal() {
  const estadoLocal = {};
  Storage.CLAVES_SYNC.forEach((k) => {
    estadoLocal[k] = Storage.load(k);
  });
  return estadoLocal;
}

export async function sincronizar() {
  if (sincronizando || !Api.configurado() || !Api.sesionActual()) return;
  if (typeof navigator !== 'undefined' && navigator.onLine === false) return;
  sincronizando = true;
  try {
    const cola = Storage.load('outbox');
    if (cola.length) {
      await Api.subirEventos(cola);
      // Quita SOLO lo enviado: pudo encolarse algo nuevo durante el await
      const enviados = new Set(cola.map((e) => e.uid));
      Storage.update('outbox', (c) => c.filter((e) => !enviados.has(e.uid)));
    }
    await Api.subirSnapshot(snapshotLocal());
    Storage.save('ultimaSync', new Date().toISOString());
  } catch {
    // Cola intacta; se reintentará en el próximo disparo.
  } finally {
    sincronizando = false;
    avisar();
  }
}

/* ====================== Migración (§5.2 C.5) ========================== */

/**
 * "Importar mi progreso local a mi cuenta": sube TODO el estado local como
 * un evento retroactivo 'migracion' + snapshot. No toca nada local: cero
 * riesgo de perder un día de racha.
 */
export async function migrarProgresoLocal() {
  Storage.encolarEvento('migracion', snapshotLocal());
  await sincronizar();
  return estado();
}

/* ====================== Bajada: adoptar o unir ======================== */

/**
 * Tras iniciar sesión en un dispositivo:
 *  - servidor vacío            → no hay nada que bajar ('servidor-vacio')
 *  - local vacío               → adopta el snapshot tal cual ('adoptado')
 *  - datos en ambos lados      → unión por uid + recomputo de rachas ('unido')
 * Devuelve la etiqueta de lo que ocurrió (para el mensaje de la UI).
 */
export async function adoptarOUnir() {
  const snap = await Api.descargarSnapshot();
  if (!snap?.estado) return 'servidor-vacio';
  const remoto = snap.estado;

  const localConDatos =
    Storage.load('historial').length > 0 ||
    Object.keys(Storage.load('estudio').unidadesCompletadas ?? {}).length > 0 ||
    Storage.load('pisosMinimos').length > 0;

  if (!localConDatos) {
    Storage.CLAVES_SYNC.forEach((k) => {
      if (remoto[k] != null) Storage.save(k, remoto[k]);
    });
    return 'adoptado';
  }

  unirLista('historial', remoto.historial, claveSesion);
  unirLista('pisosMinimos', remoto.pisosMinimos, (p) => p.uid ?? `${p.fecha}|${p.problemId}`);
  unirLista('sesionesArchivadas', remoto.sesionesArchivadas, claveSesion);
  unirLista('problemasGenerados', remoto.problemasGenerados, (p) => `gen-${p.id}`);
  unirEstudio(remoto.estudio);
  unirInsignias(remoto.insignias);
  unirRevisiones(remoto.revisiones);
  // Escalares de perfil/preferencias: se conservan los locales (este
  // dispositivo es la verdad inmediata); las rachas se recomputan abajo.
  recomputarRachaEntrenamiento();
  recomputarRachaEstudio();
  return 'unido';
}

function claveSesion(h) {
  return h.uid ?? `${h.problemId}|${h.fecha}|${h.score ?? ''}`;
}

function unirLista(nombre, remota, claveFn) {
  if (!Array.isArray(remota) || remota.length === 0) return;
  Storage.update(nombre, (local) => {
    const vistas = new Set(local.map(claveFn));
    remota.forEach((e) => {
      if (!vistas.has(claveFn(e))) local.push(e);
    });
    if (local[0]?.fecha) local.sort((a, b) => (a.fecha < b.fecha ? -1 : a.fecha > b.fecha ? 1 : 0));
    return local;
  });
}

function unirEstudio(remoto) {
  if (!remoto) return;
  Storage.update('estudio', (e) => {
    Object.entries(remoto.unidadesCompletadas ?? {}).forEach(([id, reg]) => {
      if (!e.unidadesCompletadas[id]) e.unidadesCompletadas[id] = reg;
    });
    Object.entries(remoto.examenes ?? {}).forEach(([id, ex]) => {
      const local = e.examenes[id];
      if (!local) e.examenes[id] = ex;
      else {
        local.aprobado = local.aprobado || ex.aprobado;
        local.intentos = Math.max(local.intentos ?? 0, ex.intentos ?? 0);
      }
    });
    e.mejorRachaEstudio = Math.max(e.mejorRachaEstudio ?? 0, remoto.mejorRachaEstudio ?? 0, remoto.rachaEstudio ?? 0);
    return e;
  });
}

function unirInsignias(remoto) {
  if (!remoto?.ganadas) return;
  Storage.update('insignias', (st) => {
    st.ganadas = st.ganadas ?? {};
    Object.entries(remoto.ganadas).forEach(([id, reg]) => {
      const local = st.ganadas[id];
      if (!local) st.ganadas[id] = reg;
      else {
        local.contador = Math.max(local.contador ?? 1, reg.contador ?? 1);
        local.claves = [...new Set([...(local.claves ?? []), ...(reg.claves ?? [])])];
        if (reg.fecha < local.fecha) local.fecha = reg.fecha; // se ganó antes
      }
    });
    return st;
  });
}

function unirRevisiones(remoto) {
  if (!remoto) return;
  Storage.update('revisiones', (local) => {
    Object.entries(remoto).forEach(([id, reg]) => {
      const mio = local[id];
      // Gana el ciclo con más revisiones registradas (más historia real)
      if (!mio || (reg.revisiones?.length ?? 0) > (mio.revisiones?.length ?? 0)) {
        local[id] = reg;
      }
    });
    return local;
  });
}

/* ====================== Recomputo de rachas =========================== */

function hoyYAyer() {
  const hoy = Storage.hoy();
  const d = new Date();
  d.setDate(d.getDate() - 1);
  const ayer = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  return { hoy, ayer };
}

/** Cadena de días consecutivos al final de una lista de fechas YYYY-MM-DD. */
function cadenas(fechas) {
  const dias = [...new Set(fechas)].sort();
  let mejor = 0;
  let actual = 0;
  let previa = null;
  dias.forEach((f) => {
    if (previa) {
      const d = new Date(previa);
      d.setDate(d.getDate() + 1);
      const siguiente = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      actual = f === siguiente ? actual + 1 : 1;
    } else {
      actual = 1;
    }
    mejor = Math.max(mejor, actual);
    previa = f;
  });
  return { mejor, final: actual, ultima: dias.at(-1) ?? null };
}

function recomputarRachaEntrenamiento() {
  const fechas = [
    ...Storage.load('historial').map((h) => h.fecha),
    ...Storage.load('pisosMinimos').map((p) => p.fecha),
  ].filter(Boolean);
  if (!fechas.length) return;
  const { mejor, final, ultima } = cadenas(fechas);
  const { hoy, ayer } = hoyYAyer();
  Storage.update('perfil', (p) => {
    p.ultimaSesion = ultima;
    p.racha = ultima === hoy || ultima === ayer ? final : 0;
    p.mejorRachaHistorica = Math.max(p.mejorRachaHistorica ?? 0, mejor, p.racha);
    return p;
  });
}

function recomputarRachaEstudio() {
  const e = Storage.load('estudio');
  const fechas = [
    ...Object.values(e.unidadesCompletadas ?? {}).map((u) => u.fecha),
    ...Object.values(e.examenes ?? {}).map((x) => x.fecha),
  ].filter(Boolean);
  if (!fechas.length) return;
  const { mejor, final, ultima } = cadenas(fechas);
  const { hoy, ayer } = hoyYAyer();
  Storage.update('estudio', (st) => {
    st.ultimaSesionEstudio = ultima;
    st.rachaEstudio = ultima === hoy || ultima === ayer ? final : 0;
    st.mejorRachaEstudio = Math.max(st.mejorRachaEstudio ?? 0, mejor, st.rachaEstudio);
    return st;
  });
}
