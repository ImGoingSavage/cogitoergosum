/**
 * storage.js — Capa de persistencia sobre LocalStorage.
 * Única puerta de entrada/salida de datos: el resto de módulos
 * no toca localStorage directamente (Single Responsibility).
 */

const PREFIX = 'cps_';

const DEFAULTS = {
  // Perfil del motor adaptativo
  perfil: {
    dificultad: 2,            // nivel actual (1-5)
    racha: 0,                 // días consecutivos
    ultimaSesion: null,       // 'YYYY-MM-DD'
    mejorRachaHistorica: 0,   // romper la racha nunca borra el logro (§2.2)
    freshStartPendiente: null, // { rachaPerdida } al romperse una racha > 0
    metaCorta: null,          // { fechaInicio, objetivo: 3 } tras un fresh start
  },
  // Preferencias del usuario (§2.6)
  preferencias: {
    duracionTimer: 20,        // minutos para próximas asignaciones (20-120, paso 5)
  },
  // Asignación del día: problema activo y su estado
  asignacion: null,
  /*
    {
      problemId, fecha, esRevision,
      revisionDe,            // id del problema original si esta sesión es una
                             // revisión presentada como variante isomórfica
      timerInicio, timerCumplido,
      duracionMin,           // duración elegida (fija al iniciar; solo extensible)
      pausadoEn,             // timestamp si el cronómetro está en pausa (§2.6)
      msPausadoTotal, pausas,
      desconstruccion, hintsUsados: [niveles],
      prediccion,            // estrategia que el usuario predijo antes de revelar
      revelado, completado
    }
  */
  // Asignaciones completadas (trazabilidad cuando hay varias sesiones al día)
  sesionesArchivadas: [],
  // Historial de problemas completados
  historial: [],
  /*
    [{ problemId, fecha, score, hintsUsados, tiempoMin,
       autoevaluacion: 'resuelto'|'parcial'|'fallado',
       estrategia, dificultad, esRevision, prediccion,
       moraleja, disparador,           // ficha del cuaderno de moralejas
       reflexion: {comparacion, transferencia} }]
  */
  // Pisos mínimos cumplidos (días sin energía: recall corto que conserva racha)
  pisosMinimos: [],
  /*  [{ fecha, problemId, recuerdo }]  */
  // Insignias ("Sellos de la biblioteca", §2.1): deterministas, ganadas por
  // esfuerzo. { ganadas: { insigniaId: { fecha, historia, contador } } }
  insignias: { ganadas: {} },
  // Modo Estudio (camino 2): progreso del roadmap. Racha SEPARADA de perfil.racha.
  estudio: {
    rachaEstudio: 0,
    mejorRachaEstudio: 0,
    ultimaSesionEstudio: null,    // 'YYYY-MM-DD'
    unidadesCompletadas: {},      // { unidadId: { fecha, aciertos, total, resultados } }
    quizEnCurso: null,            // { unidadId, preguntasIds, dificultad, indice, resultados, esRepaso? }
    examenes: {},                 // { bloqueId: { aprobado, fecha, coincidencias, total, registros, intentos } }
    examenEnCurso: null,          // { bloqueId, itemIds, indice, paso, registros }
    examenClusterEnCurso: null,   // { clusterId, clusterTitulo, preguntasIds, dificultad, indice, resultados }
    pendientesRepaso: {},         // { unidadId: [preguntaId, ...] } — mal o parcial en el último quiz
  },
  // Repetición espaciada: { problemId: { etapa, proximaRevision, revisiones: [] } }
  revisiones: {},
  // Variantes isomórficas generadas por IA (problemFactory.js); se fusionan
  // con los problemas estáticos en el pool de selección
  problemasGenerados: [],
  // Configuración del mentor IA (opcional)
  mentorIA: { habilitado: false, apiKey: '' },
  // Mentor local opcional (backend RAG+DeepSeek en la laptop, mentorLocal.js).
  // Config del dispositivo: url del túnel, service token y on/off. NUNCA viaja
  // al servidor (fuera de CLAVES_SYNC, igual que mentorIA): es plomería local.
  mentorLocal: { habilitado: false, url: '', serviceToken: '' },
  // El claustro (Fase D, §2.4): preferencias sociales del usuario.
  // username, ficha compartida (opt-in) y entregas de "pensar juntos"
  // que esperan red (jamás bloquean el cierre de una sesión).
  claustro: { username: null, fichaCompartidaUid: null, pjEntregasPendientes: [] },
  // Pizarras a mano alzada (papel de borrador del pencil, pizarra.js):
  // { contexto: { paginas: [[trazo,…]], pagina, actualizado } }.
  // Locales del dispositivo A PROPÓSITO (pesan y son borrador): fuera de
  // CLAVES_SYNC, igual que la asignación en curso.
  pizarras: {},
  // Portada de inicio de sesión: true si el usuario eligió "continuar sin
  // cuenta" (decisión por dispositivo; NO viaja al servidor). La cuenta es
  // siempre opcional (§0.7): la portada invita, jamás bloquea.
  loginOmitido: false,
  // Versión del esquema de datos locales. Sube en 1 cada vez que una
  // migración de migrarSiNecesario() cambia la forma de alguna clave.
  schemaVersion: 1,
  // ---- Sincronización opcional (Fase C, HANDOFFCES §5.2) ----
  // Cola de eventos pendientes de subir; LocalStorage sigue siendo la verdad
  outbox: [],            // [{uid, tipo, payload, ts}]
  deviceId: null,        // identificador del dispositivo (se genera una vez)
  sesionSupabase: null,  // {accessToken, refreshToken, expiraEn, userId, email}
  ultimaSync: null,      // ISO de la última sincronización exitosa
  // Registro local de avisos técnicos (ring buffer 50). Para depurar fallos
  // que por diseño son silenciosos (sync, IA). Solo este dispositivo.
  diagnostico: [],
};

/**
 * Claves que viajan al servidor (snapshot y migración). EXCLUIDAS a
 * propósito: mentorIA (API keys de Claude JAMÁS salen del dispositivo, §4.2),
 * asignacion (estado efímero del día), outbox/deviceId/sesionSupabase
 * (plomería local de la propia sincronización).
 */
export const CLAVES_SYNC = [
  'perfil',
  'historial',
  'pisosMinimos',
  'estudio',
  'insignias',
  'revisiones',
  'sesionesArchivadas',
  'problemasGenerados',
  'preferencias',
  'claustro',
];

function key(name) {
  return PREFIX + name;
}

export function load(name) {
  try {
    const raw = localStorage.getItem(key(name));
    if (raw === null) return structuredClone(DEFAULTS[name] ?? null);
    return JSON.parse(raw);
  } catch {
    return structuredClone(DEFAULTS[name] ?? null);
  }
}

export function save(name, value) {
  const json = JSON.stringify(value);
  try {
    localStorage.setItem(key(name), json);
  } catch {
    // LocalStorage lleno: podar lo más pesado (archivo de sesiones) y
    // reintentar UNA vez. Si aun así falla, registrar sin lanzar: una
    // excepción a mitad de completarSesion() dejaría estado parcial.
    try {
      const archivadas = JSON.parse(localStorage.getItem(key('sesionesArchivadas')) ?? '[]');
      if (Array.isArray(archivadas) && archivadas.length > 100) {
        localStorage.setItem(key('sesionesArchivadas'), JSON.stringify(archivadas.slice(-100)));
      }
      localStorage.setItem(key(name), json);
    } catch {
      registrarDiagnostico('storage', `No se pudo guardar «${name}»: LocalStorage lleno.`);
    }
  }
}

export function update(name, fn) {
  const current = load(name);
  const next = fn(current);
  save(name, next);
  return next;
}

export function remove(name) {
  localStorage.removeItem(key(name));
}

/** Fecha local en formato YYYY-MM-DD (las "sesiones diarias" usan día local). */
export function hoy() {
  const d = new Date();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${mm}-${dd}`;
}

export function resetTotal() {
  Object.keys(DEFAULTS).forEach((n) => remove(n));
}

/**
 * Migraciones de datos locales. Se llama UNA VEZ al arrancar la app.
 * Cada bloque `if (v < N)` aplica los cambios de la versión N y sube el
 * contador: idempotente, seguro de llamar incluso si ya se ejecutó.
 */
export function migrarSiNecesario() {
  const v = load('schemaVersion') ?? 0;
  // v1 → estado inicial: sin transformaciones estructurales.
  if (v < 1) save('schemaVersion', 1);
}

/**
 * Anota un aviso técnico. Usa setItem crudo con try/catch propio: jamás
 * recursa en save() ni tumba al llamador (el diagnóstico nunca rompe nada).
 */
export function registrarDiagnostico(origen, mensaje) {
  try {
    const lista = JSON.parse(localStorage.getItem(key('diagnostico')) ?? '[]');
    lista.push({ ts: new Date().toISOString(), origen, mensaje: String(mensaje).slice(0, 300) });
    localStorage.setItem(key('diagnostico'), JSON.stringify(lista.slice(-50)));
  } catch {
    // Nada: el diagnóstico es lo único que puede perderse en silencio.
  }
}

/* ---------------- Sincronización (Fase C, §5.2 C.4) ---------------- */

/** Identificador único corto (eventos, dispositivos). */
export function uidNuevo() {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export function deviceId() {
  let id = load('deviceId');
  if (!id) {
    id = uidNuevo();
    save('deviceId', id);
  }
  return id;
}

/**
 * Encola un evento para subir al servidor cuando haya red y sesión.
 * Emite 'cps:evento-encolado' para que sync.js programe el drenado
 * (evento del DOM y no import directo: evita ciclos de módulos).
 */
export function encolarEvento(tipo, payload) {
  update('outbox', (cola) => {
    cola.push({ uid: uidNuevo(), tipo, payload, ts: new Date().toISOString() });
    return cola;
  });
  try {
    window.dispatchEvent(new CustomEvent('cps:evento-encolado'));
  } catch {
    // Entornos sin window (tests): la cola queda lista igualmente.
  }
}
