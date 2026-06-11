/**
 * badges.js — Sellos de la biblioteca (§2.1 HANDOFFCES).
 *
 * Motor declarativo: data/badges.json define los metadatos; aquí vive un
 * evaluador puro por id que mira el estado real (historial, pisos, estudio,
 * perfil) y decide si el sello está ganado y con qué historia.
 *
 * Reglas de la Constitución (§0):
 *  - Determinista y anunciable: nada aleatorio, nada comprable.
 *  - Se premia el PROCESO; el acierto es consecuencia.
 *  - El revelado ocurre SOLO en pantallas de cierre (jamás interrumpe el
 *    forcejeo): app.js/study.js llaman evaluarYRegistrar() al cerrar sesión,
 *    piso, unidad o examen, y pintan lo nuevo con renderReveladas().
 *  - En la vitrina ("Mi estante"), las no ganadas son siluetas sin nombre.
 */

import { load, update, hoy, encolarEvento } from './storage.js';

const ESTRATEGIAS = ['inversion', 'optimizacion', 'invariantes', 'patrones'];

let catalogo = null; // contenido de data/badges.json

/**
 * Contexto base inyectado por app.js (funciones perezosas, para que
 * study.js pueda evaluar sellos sin importar app.js — sin ciclos):
 * { problemas: () => [...], bloquesEstudio: () => [...] }
 */
let contextoBase = {};

export function setContexto(ctx) {
  contextoBase = ctx ?? {};
}

function resolver(fuente, respaldo) {
  if (typeof fuente === 'function') return fuente() ?? respaldo;
  return fuente ?? respaldo;
}

export async function init() {
  try {
    const res = await fetch('data/badges.json');
    catalogo = await res.json();
  } catch {
    catalogo = null;
  }
}

export function disponible() {
  return Boolean(catalogo?.insignias?.length);
}

export function ganadas() {
  return load('insignias').ganadas ?? {};
}

/** Metadatos de un sello por id (para pintar vitrinas de amigos). */
export function definicion(id) {
  return catalogo?.insignias.find((i) => i.id === id) ?? null;
}

/* ====================== Datos que miran los sellos ===================== */

function recolectar(ctx) {
  const historial = load('historial');
  const estudio = load('estudio');
  const perfil = load('perfil');
  return {
    historial,
    estudio,
    perfil,
    pisos: load('pisosMinimos'),
    problemas: resolver(ctx?.problemas ?? contextoBase.problemas, []),
    bloquesEstudio: resolver(ctx?.bloquesEstudio ?? contextoBase.bloquesEstudio, []),
    fichas: historial.filter((h) => h.moraleja && h.disparador),
    rachaMax: Math.max(perfil.racha ?? 0, perfil.mejorRachaHistorica ?? 0),
    rachaEstudioMax: Math.max(estudio.rachaEstudio ?? 0, estudio.mejorRachaEstudio ?? 0),
  };
}

/** Predicciones de jugada correctas acumuladas (camino 1 + exámenes). */
function prediccionesCorrectas(d) {
  const camino1 = d.historial.filter((h) => h.prediccion && h.prediccion === h.estrategia).length;
  const examenes = Object.values(d.estudio.examenes ?? {})
    .flatMap((e) => e.registros ?? [])
    .filter((r) => r.prediccion === r.heuristica).length;
  return camino1 + examenes;
}

/** Tasa de disparadores reconocidos en un mes 'YYYY-MM' (null si <5 datos). */
function tasaDisparadoresMes(historial, mes) {
  const del = historial.filter((h) => h.prediccion && h.fecha?.startsWith(mes));
  if (del.length < 5) return null;
  return del.filter((h) => h.prediccion === h.estrategia).length / del.length;
}

function mesAnteriorDe(mes) {
  const [y, m] = mes.split('-').map(Number);
  const d = new Date(y, m - 2, 1); // mes - 1 (los meses de Date van de 0 a 11)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
}

/* =========================== Evaluadores ============================== */
/* Cada evaluador devuelve { ok, historia, contador?, claveRepeticion? }.   */

const EVALUADORES = {
  'forcejeo-limpio': (d) => {
    const s = d.historial.find(
      (h) => h.dificultad >= 4 && h.hintsUsados === 0 && (h.desconstruccionLen ?? 0) >= 400
    );
    return s
      ? {
          ok: true,
          historia: `Un nivel ${s.dificultad} sin una sola pista y ${s.desconstruccionLen} caracteres de desconstrucción (${s.fecha}). Eso es entrenamiento real.`,
        }
      : { ok: false };
  },

  'tinta-abundante': (d) => {
    const n = d.historial.filter((h) => (h.desconstruccionLen ?? 0) >= 400).length;
    return n >= 10
      ? { ok: true, historia: 'Diez desconstrucciones de más de 400 caracteres: el papel ya es parte de tu pensamiento.' }
      : { ok: false };
  },

  'el-que-mira-atras': (d) =>
    d.fichas.length >= 25
      ? { ok: true, historia: `Veinticinco fichas completas en tu cuaderno de moralejas (hoy llevas ${d.fichas.length}).` }
      : { ok: false },

  incubadora: (d) => {
    const n = d.historial.filter((h) => h.incubada).length;
    return n >= 5
      ? { ok: true, historia: 'Cinco problemas cerrados en un día posterior al inicio: aprendiste a dejar que las ideas lleguen en la pausa.' }
      : { ok: false };
  },

  'paciencia-de-piedra': (d) => {
    const n = d.historial.filter((h) => (h.tiempoMin ?? 0) >= (h.duracionMin ?? 20)).length;
    return n >= 10
      ? { ok: true, historia: 'Diez sesiones que agotaron el temporizador completo antes de revelar: paciencia de piedra volcánica.' }
      : { ok: false };
  },

  fenix: (d) => {
    let n = 0;
    const fallados = new Set();
    d.historial.forEach((h) => {
      const objetivo = h.revisionDe ?? h.problemId;
      if (h.esRevision && h.autoevaluacion === 'resuelto' && fallados.has(objetivo)) n += 1;
      if (h.autoevaluacion === 'fallado') fallados.add(objetivo);
    });
    return n > 0
      ? { ok: true, contador: n, historia: 'Volviste a un problema que no había salido — y esta vez salió. Eso es exactamente mejorar contra ti mismo.' }
      : { ok: false };
  },

  'ojo-halcon-i': (d, def) => evalOjoHalcon(d, def),
  'ojo-halcon-ii': (d, def) => evalOjoHalcon(d, def),
  'ojo-halcon-iii': (d, def) => evalOjoHalcon(d, def),

  'marea-que-sube': (d) => {
    const mes = hoy().slice(0, 7);
    const tasaActual = tasaDisparadoresMes(d.historial, mes);
    const tasaPrevia = tasaDisparadoresMes(d.historial, mesAnteriorDe(mes));
    if (tasaActual === null || tasaPrevia === null || tasaActual <= tasaPrevia) return { ok: false };
    return {
      ok: true,
      claveRepeticion: mes,
      historia: `Tu tasa de disparadores reconocidos subió de ${Math.round(tasaPrevia * 100)}% a ${Math.round(tasaActual * 100)}% respecto al mes anterior.`,
    };
  },

  cartografo: (d) => {
    const cubiertas = new Set(d.fichas.map((f) => f.estrategia));
    return ESTRATEGIAS.every((e) => cubiertas.has(e))
      ? { ok: true, historia: 'Una ficha de moraleja en cada una de las cuatro estrategias: el mapa básico está trazado.' }
      : { ok: false };
  },

  'cartografo-mayor': (d) => {
    const mapa = catalogo?.mapaHeuristicas ?? {};
    const tagsCubiertos = new Set(
      d.fichas.flatMap((f) => d.problemas.find((p) => p.id === f.problemId)?.tags ?? [])
    );
    const todas = Object.keys(mapa).every((h) => (mapa[h] ?? []).some((t) => tagsCubiertos.has(t)));
    return todas
      ? { ok: true, historia: 'Tus fichas cubren las doce heurísticas del catálogo: el mapa completo del territorio.' }
      : { ok: false };
  },

  'piso-firme': (d) =>
    d.pisos.length >= 5
      ? { ok: true, historia: 'Cinco días difíciles salvados con el piso mínimo: el hábito sobrevive a los días malos.' }
      : { ok: false },

  'lector-disciplinado': (d) => {
    if (!d.bloquesEstudio.length) return { ok: false };
    const todos = d.bloquesEstudio.every((b) => d.estudio.examenes?.[b.id]?.aprobado);
    return todos
      ? { ok: true, historia: `Examen aprobado en los ${d.bloquesEstudio.length} bloques del Modo Estudio disponibles hasta hoy.` }
      : { ok: false };
  },
};

function evalOjoHalcon(d, def) {
  const n = prediccionesCorrectas(d);
  return n >= def.umbral
    ? { ok: true, historia: `${def.umbral} predicciones de jugada correctas acumuladas: reconoces disparadores en frío.` }
    : { ok: false };
}

/** Sellos de racha (umbral en la definición, fuente según el id). */
function evalRacha(d, def) {
  const valor = def.id.startsWith('racha-estudio') ? d.rachaEstudioMax : d.rachaMax;
  return valor >= def.umbral
    ? { ok: true, historia: `${def.umbral} días consecutivos. La constancia es el verdadero superpoder.` }
    : { ok: false };
}

function evaluadorPara(def) {
  if (def.id.startsWith('racha-')) return evalRacha;
  return EVALUADORES[def.id] ?? null;
}

/* ======================= Registro y revelado ========================== */

/**
 * Evalúa todos los sellos contra el estado actual y registra los nuevos
 * (o los incrementos de los repetibles). Devuelve la lista de novedades
 * [{ def, registro }] para pintar en la pantalla de cierre.
 */
export function evaluarYRegistrar(ctx = {}) {
  if (!disponible()) return [];
  const datos = recolectar(ctx);
  const novedades = [];

  update('insignias', (st) => {
    st.ganadas = st.ganadas ?? {};
    catalogo.insignias.forEach((def) => {
      const evaluar = evaluadorPara(def);
      if (!evaluar) return;
      const r = evaluar(datos, def);
      if (!r?.ok) return;

      const previo = st.ganadas[def.id];
      if (!previo) {
        st.ganadas[def.id] = {
          fecha: hoy(),
          historia: r.historia,
          contador: r.contador ?? 1,
          claves: r.claveRepeticion ? [r.claveRepeticion] : [],
        };
        novedades.push({ def, registro: st.ganadas[def.id] });
      } else if (def.repetible) {
        if (r.contador != null && r.contador > (previo.contador ?? 1)) {
          previo.contador = r.contador;
          previo.fecha = hoy();
          previo.historia = r.historia;
          novedades.push({ def, registro: previo });
        } else if (r.claveRepeticion && !(previo.claves ?? []).includes(r.claveRepeticion)) {
          previo.claves = [...(previo.claves ?? []), r.claveRepeticion];
          previo.contador = (previo.contador ?? 1) + 1;
          previo.fecha = hoy();
          previo.historia = r.historia;
          novedades.push({ def, registro: previo });
        }
      }
    });
    return st;
  });

  // Sincronización opcional: cada sello nuevo viaja como evento (§5.2 C.4)
  novedades.forEach(({ def, registro }) => encolarEvento('insignia', { id: def.id, registro }));

  return novedades;
}

/* =========================== Render (DOM) ============================= */

function nombreConContador(def, registro) {
  const n = registro?.contador ?? 1;
  return def.repetible && n > 1 ? `${def.nombre} ×${n}` : def.nombre;
}

/** Pinta los sellos recién ganados en un contenedor de pantalla de cierre. */
export function renderReveladas(novedades, contenedor) {
  if (!contenedor) return;
  contenedor.innerHTML = '';
  novedades.forEach(({ def, registro }) => {
    const div = document.createElement('div');
    div.className = 'insignia-revelada';
    const glifo = document.createElement('span');
    glifo.className = 'insignia-glifo';
    glifo.textContent = def.glifo;
    const cuerpo = document.createElement('div');
    const nombre = document.createElement('div');
    nombre.className = 'insignia-nombre';
    nombre.textContent = `Sello nuevo: ${nombreConContador(def, registro)}`;
    const historia = document.createElement('div');
    historia.className = 'insignia-historia';
    historia.textContent = registro.historia;
    cuerpo.append(nombre, historia);
    div.append(glifo, cuerpo);
    contenedor.appendChild(div);
  });
}

/** Vitrina "Mi estante": ganadas con historia; el resto, siluetas sin nombre. */
export function renderEstante(contenedor) {
  if (!contenedor) return;
  contenedor.innerHTML = '';
  if (!disponible()) return;
  const g = ganadas();

  catalogo.insignias.forEach((def) => {
    const registro = g[def.id];
    const card = document.createElement('div');
    card.className = `estante-sello ${registro ? 'ganado' : 'silueta'}`;

    const glifo = document.createElement('div');
    glifo.className = 'estante-glifo';
    glifo.textContent = registro ? def.glifo : '◌';
    card.appendChild(glifo);

    const nombre = document.createElement('div');
    nombre.className = 'estante-nombre';
    nombre.textContent = registro ? nombreConContador(def, registro) : 'Aún por descubrir';
    card.appendChild(nombre);

    if (registro) {
      const fecha = document.createElement('div');
      fecha.className = 'estante-fecha';
      fecha.textContent = registro.fecha;
      card.appendChild(fecha);

      const historia = document.createElement('div');
      historia.className = 'estante-historia';
      historia.textContent = registro.historia;
      card.appendChild(historia);

      const familia = document.createElement('div');
      familia.className = 'estante-familia';
      familia.textContent = catalogo.familias?.[def.familia] ?? def.familia;
      card.appendChild(familia);
    }

    contenedor.appendChild(card);
  });
}
