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
    quizEnCurso: null,            // { unidadId, indice, resultados: [] }
    examenes: {},                 // { bloqueId: { aprobado, fecha, coincidencias, total, registros, intentos } }
    examenEnCurso: null,          // { bloqueId, itemIds, indice, paso, registros }
  },
  // Repetición espaciada: { problemId: { etapa, proximaRevision, revisiones: [] } }
  revisiones: {},
  // Variantes isomórficas generadas por IA (problemFactory.js); se fusionan
  // con los problemas estáticos en el pool de selección
  problemasGenerados: [],
  // Configuración del mentor IA (opcional)
  mentorIA: { habilitado: false, apiKey: '' },
  // El claustro (Fase D, §2.4): preferencias sociales del usuario.
  // username, ficha compartida (opt-in) y entregas de "pensar juntos"
  // que esperan red (jamás bloquean el cierre de una sesión).
  claustro: { username: null, fichaCompartidaUid: null, pjEntregasPendientes: [] },
  // ---- Sincronización opcional (Fase C, HANDOFFCES §5.2) ----
  // Cola de eventos pendientes de subir; LocalStorage sigue siendo la verdad
  outbox: [],            // [{uid, tipo, payload, ts}]
  deviceId: null,        // identificador del dispositivo (se genera una vez)
  sesionSupabase: null,  // {accessToken, refreshToken, expiraEn, userId, email}
  ultimaSync: null,      // ISO de la última sincronización exitosa
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
  localStorage.setItem(key(name), JSON.stringify(value));
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
