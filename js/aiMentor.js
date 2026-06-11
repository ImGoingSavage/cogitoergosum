/**
 * aiMentor.js — Integración con la API de Claude como mentor socrático.
 *
 * Arquitectura: módulo opcional y desacoplado. La aplicación funciona
 * completa sin IA (hints estáticos curados); si el usuario configura una
 * cuenta, los hints se generan dinámicamente adaptados a su desconstrucción.
 *
 * Multi-cuenta: el usuario puede registrar varias cuentas de Anthropic
 * (nombre + API key) y elegir cuál está activa. Todos los módulos que
 * consumen la API (este y el futuro problemFactory.js) deben leer la
 * cuenta activa desde aquí — única fuente de verdad.
 *
 * Modelo: claude-opus-4-8 (Messages API, fetch directo — proyecto sin SDK).
 * El mentor NUNCA da la respuesta: pregunta, guía, reenfoca y reduce el
 * espacio de búsqueda según el nivel solicitado.
 *
 * ⚠️ Las API keys se guardan en LocalStorage del navegador: úsalas solo en
 * un entorno local y personal. Para producción se requeriría un backend.
 */

import { load, save, update } from './storage.js';

const API_URL = 'https://api.anthropic.com/v1/messages';
const MODEL = 'claude-opus-4-8';

const SYSTEM_MENTOR = `Eres un mentor socrático de resolución de problemas, inspirado en la tutoría de olimpiadas matemáticas y el método de Pólya.

Reglas inquebrantables:
- NUNCA reveles la solución ni digas "la respuesta es...".
- Responde SOLO con la pista solicitada: una a tres frases, en español, tono sobrio y respetuoso.
- No menciones el nombre de la estrategia de clasificación del problema.
- Adapta la pista a lo que el usuario ya escribió en su desconstrucción: si va bien encaminado, profundiza su línea; si está bloqueado, reenfoca con una pregunta.

Calibra la pista al nivel solicitado:
Nivel 1: redirige la atención con una pregunta general.
Nivel 2: señala una estructura o restricción relevante del problema.
Nivel 3: reduce el espacio de búsqueda descartando caminos estériles.
Nivel 4: sugiere una familia de estrategias aplicable, sin ejecutarla.
Nivel 5: describe el camino casi completo, pero deja el paso final al usuario.`;

/* ========================= Gestión de cuentas ========================= */

/**
 * Devuelve la configuración en el formato nuevo { cuentas, activa },
 * migrando automáticamente el formato antiguo de una sola key.
 */
function cfgNormalizada() {
  const cfg = load('mentorIA') ?? {};
  if (Array.isArray(cfg.cuentas)) return cfg;
  const cuentas = cfg.apiKey
    ? [{ id: 1, nombre: 'Cuenta 1', apiKey: cfg.apiKey }]
    : [];
  const nuevo = { cuentas, activa: cuentas[0]?.id ?? null };
  save('mentorIA', nuevo);
  return nuevo;
}

export function listarCuentas() {
  return cfgNormalizada().cuentas;
}

export function cuentaActiva() {
  const cfg = cfgNormalizada();
  return cfg.cuentas.find((c) => c.id === cfg.activa) ?? null;
}

export function mentorDisponible() {
  return Boolean(cuentaActiva()?.apiKey);
}

/** Registra una cuenta nueva y la deja activa. Devuelve la cuenta o null. */
export function agregarCuenta(nombre, apiKey) {
  const n = nombre.trim();
  const k = apiKey.trim();
  if (!n || !k) return null;
  let creada = null;
  update('mentorIA', () => {
    const cfg = cfgNormalizada();
    const id = Math.max(0, ...cfg.cuentas.map((c) => c.id)) + 1;
    creada = { id, nombre: n, apiKey: k };
    cfg.cuentas.push(creada);
    cfg.activa = id;
    return cfg;
  });
  return creada;
}

export function activarCuenta(id) {
  update('mentorIA', () => {
    const cfg = cfgNormalizada();
    if (cfg.cuentas.some((c) => c.id === id)) cfg.activa = id;
    return cfg;
  });
}

/** Elimina una cuenta; si era la activa, activa la primera disponible. */
export function eliminarCuenta(id) {
  update('mentorIA', () => {
    const cfg = cfgNormalizada();
    cfg.cuentas = cfg.cuentas.filter((c) => c.id !== id);
    if (cfg.activa === id) cfg.activa = cfg.cuentas[0]?.id ?? null;
    return cfg;
  });
}

/* ========================= Llamadas a la API ========================== */

async function llamarClaude(userPrompt) {
  const cuenta = cuentaActiva();
  if (!cuenta?.apiKey) return null;

  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': cuenta.apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 1024,
      thinking: { type: 'adaptive' },
      system: SYSTEM_MENTOR,
      messages: [{ role: 'user', content: userPrompt }],
    }),
  });

  if (!res.ok) throw new Error(`API ${res.status}`);
  const data = await res.json();
  if (data.stop_reason === 'refusal') return null;
  const bloque = (data.content ?? []).find((b) => b.type === 'text');
  return bloque?.text?.trim() ?? null;
}

/**
 * Genera un hint dinámico para el nivel dado, usando la desconstrucción
 * del usuario como contexto. Devuelve el texto o null si no es posible.
 */
export async function generarHintIA(problema, nivel, desconstruccion) {
  if (!mentorDisponible()) return null;
  const userPrompt = [
    `Problema: ${problema.enunciado}`,
    `Solución de referencia (solo para tu contexto, jamás la reveles): ${problema.solucion}`,
    desconstruccion
      ? `Desconstrucción escrita por el usuario hasta ahora:\n${desconstruccion}`
      : 'El usuario aún no ha escrito su desconstrucción.',
    `Genera la pista de nivel ${nivel}.`,
  ].join('\n\n');
  return llamarClaude(userPrompt);
}

/**
 * Chat socrático durante el forcejeo (§4.4 HANDOFFCES): conversación breve
 * y multi-turno. Jamás revela ni confirma soluciones; pregunta y reenfoca.
 * El historial vive en la asignación (se archiva con la sesión).
 */
const SYSTEM_CHAT =
  SYSTEM_MENTOR +
  `

Además, estás en un CHAT breve durante el forcejeo del usuario:
- Cada intervención tuya: 1 a 4 frases, casi siempre terminando en una pregunta.
- Nunca confirmes ni niegues si una respuesta propuesta es correcta: devuelve la pregunta que le permita comprobarlo por sí mismo.
- Si pide la solución directamente, recuérdale con calidez que el forcejeo es el entrenamiento y ofrécele reenfocar.`;

export async function chatSocratico(problema, desconstruccion, mensajes) {
  const cuenta = cuentaActiva();
  if (!cuenta?.apiKey || !mensajes?.length) return null;

  const contexto =
    `Problema: ${problema.enunciado}\n\n` +
    `Solución de referencia (solo para tu contexto, JAMÁS la reveles ni la confirmes): ${problema.solucion}\n\n` +
    `Desconstrucción escrita por el usuario hasta ahora:\n${desconstruccion || '(aún vacía)'}`;

  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': cuenta.apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 1024,
      thinking: { type: 'adaptive' },
      system: `${SYSTEM_CHAT}\n\n${contexto}`,
      messages: mensajes,
    }),
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  const data = await res.json();
  if (data.stop_reason === 'refusal') return null;
  return (data.content ?? []).find((b) => b.type === 'text')?.text?.trim() ?? null;
}

/**
 * Evalúa la desconstrucción del usuario: detecta bloqueos y formula
 * UNA pregunta orientadora (sin pistas sobre la solución).
 * Pensado para la fase "Comprender el problema" de Pólya.
 */
export async function evaluarDesconstruccion(problema, desconstruccion) {
  if (!mentorDisponible() || !desconstruccion) return null;
  return llamarClaude(
    `Problema: ${problema.enunciado}\n\n` +
    `Desconstrucción del usuario:\n${desconstruccion}\n\n` +
    'Analiza la desconstrucción: ¿qué información clave pasó por alto o qué supuesto no examinó? ' +
    'Responde únicamente con UNA pregunta orientadora breve, sin dar pistas de la solución.'
  );
}
