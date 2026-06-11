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
 * Llamada genérica a la Messages API con system y mensajes arbitrarios
 * (los mensajes pueden llevar bloques de imagen). Con `schema` fuerza
 * salida JSON validada vía output_config (structured outputs).
 */
async function llamarApi({ system, mensajes, maxTokens = 1024, schema = null }) {
  const cuenta = cuentaActiva();
  if (!cuenta?.apiKey) return null;
  const body = {
    model: MODEL,
    max_tokens: maxTokens,
    thinking: { type: 'adaptive' },
    system,
    messages: mensajes,
  };
  if (schema) body.output_config = { format: { type: 'json_schema', schema } };

  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': cuenta.apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  const data = await res.json();
  if (data.stop_reason === 'refusal') return null;
  const texto = (data.content ?? []).find((b) => b.type === 'text')?.text?.trim() ?? null;
  if (!texto) return null;
  return schema ? JSON.parse(texto) : texto;
}

/**
 * Reduce una foto a un tamaño razonable para la API (lado mayor ≤1568 px,
 * JPEG) y la devuelve como bloque base64 listo para un mensaje.
 * Nunca se persiste: la imagen viaja a la API del usuario y se descarta.
 */
export function prepararImagen(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      URL.revokeObjectURL(url);
      const escala = Math.min(1, 1568 / Math.max(img.width, img.height));
      const canvas = document.createElement('canvas');
      canvas.width = Math.max(1, Math.round(img.width * escala));
      canvas.height = Math.max(1, Math.round(img.height * escala));
      canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.85);
      resolve({
        type: 'image',
        source: { type: 'base64', media_type: 'image/jpeg', data: dataUrl.split(',')[1] },
      });
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error('No se pudo leer la imagen.'));
    };
    img.src = url;
  });
}

/* ===================== Chat del mentor (por modos) ===================== */
/* §4.4 HANDOFFCES ampliado: el mentor vive en todas las vistas. El modo
   define qué puede decir — durante el forcejeo JAMÁS revela ni confirma;
   tras el revelado puede comparar con la solución oficial; en estudio y
   dashboard acompaña sin romper ninguna mecánica de recuperación. */

const SYSTEM_CHAT_FORCEJEO =
  SYSTEM_MENTOR +
  `

Además, estás en un CHAT breve durante el forcejeo del usuario:
- Cada intervención tuya: 1 a 4 frases, casi siempre terminando en una pregunta.
- Nunca confirmes ni niegues si una respuesta propuesta es correcta: devuelve la pregunta que le permita comprobarlo por sí mismo.
- Si el usuario adjunta una FOTO de su trabajo en papel, léela con cuidado (incluidas las expresiones matemáticas) y reacciona a lo que ahí escribió — siempre con preguntas, sin validar resultados.
- Si pide la solución directamente, recuérdale con calidez que el forcejeo es el entrenamiento y ofrécele reenfocar.`;

const SYSTEM_CHAT_REVISION = `Eres un mentor de resolución de problemas (método de Pólya, fase "mirar hacia atrás"). El usuario YA reveló la solución oficial: ahora sí puedes compararla con su trabajo.

Reglas:
- Señala CON PRECISIÓN dónde divergió su camino: el paso exacto, el supuesto erróneo o el hueco lógico. Cita lo que él escribió.
- Valida primero el proceso (qué hizo bien) y trata el fallo como información, nunca como veredicto: prohibido "mal", "incorrecto" o "fallaste" a secas.
- Si adjunta una FOTO de su intento en papel, transcribe mentalmente lo relevante (incluidas expresiones matemáticas) y úsalo en la comparación.
- Cierra con la transferencia: qué señal del enunciado debería disparar la idea correcta la próxima vez.
- Español, tono sobrio y cálido, respuestas de chat breves (2-6 frases).`;

const SYSTEM_CHAT_ESTUDIO = `Eres un mentor socrático del Modo Estudio de CogitoErgoSum (lectura dirigida de libros de resolución de problemas, con quizzes de recuperación y exámenes de bloque).

Reglas:
- Puedes explicar conceptos y técnicas del material que el usuario ya leyó, con ejemplos NUEVOS tuyos.
- Si la pregunta es sobre un quiz o examen EN CURSO, no des la respuesta: guía con preguntas (la recuperación es el entrenamiento).
- Español, 1 a 5 frases, tono sobrio; termina en pregunta cuando estés guiando.`;

const SYSTEM_CHAT_COACH = `Eres el mentor de CogitoErgoSum y conversas con el usuario sobre SU entrenamiento, usando el resumen de métricas que se te da.

Reglas:
- Compara al usuario únicamente contra su propio pasado, jamás contra otras personas.
- Celebra el proceso (forcejeo, fichas, constancia); el acierto es consecuencia.
- Sé concreto: apóyate en los números del resumen y sugiere a lo sumo UN foco siguiente.
- Español, 1 a 6 frases, sin culpa ni urgencia.`;

const SYSTEMS_CHAT = {
  forcejeo: SYSTEM_CHAT_FORCEJEO,
  revision: SYSTEM_CHAT_REVISION,
  estudio: SYSTEM_CHAT_ESTUDIO,
  general: SYSTEM_CHAT_COACH,
};

/**
 * Chat multi-turno del mentor. `modo` ∈ forcejeo|revision|estudio|general,
 * `contexto` es el texto de situación que arma la app, `mensajes` va en el
 * formato de la API (el último puede llevar bloques de imagen).
 */
export async function chatMentor(modo, contexto, mensajes) {
  if (!mensajes?.length) return null;
  const system = `${SYSTEMS_CHAT[modo] ?? SYSTEM_CHAT_COACH}\n\n${contexto}`;
  return llamarApi({ system, mensajes });
}

/* ================== Foto de la desconstrucción en papel ================ */

const SCHEMA_TRANSCRIPCION = {
  type: 'object',
  properties: {
    transcripcion: { type: 'string' },
    observacion: { type: 'string' },
  },
  required: ['transcripcion', 'observacion'],
  additionalProperties: false,
};

/**
 * Analiza la foto de una desconstrucción escrita a mano: la transcribe
 * fielmente (texto y expresiones matemáticas) y devuelve una observación
 * socrática sobre su redacción/completitud. JAMÁS evalúa si el camino es
 * correcto ni insinúa la solución (es material de forcejeo).
 */
export async function analizarFotoDesconstruccion(problema, imagen) {
  const system = `Transcribes a texto el trabajo manuscrito de un estudiante durante su forcejeo con un problema.

Reglas inquebrantables:
- Transcribe FIELMENTE lo escrito, en su idioma. Expresiones matemáticas en notación lineal legible (p. ej. "x^2/(y+1)", "sqrt(2n+1)") o LaTeX sencillo; si algo es ilegible, márcalo como [ilegible].
- NO corrijas el razonamiento, NO confirmes ni niegues resultados, NO des pistas de la solución del problema.
- "observacion": 1 a 3 frases en español, socráticas, SOLO sobre la redacción y completitud de la desconstrucción (¿se entiende qué se pide, qué datos hay, qué restricciones, qué hipótesis?) y sobre expresiones ambiguas o ilegibles si las hay. Nada sobre si el camino es correcto.

Contexto del problema (solo para entender la letra; no opines sobre la solución):
${problema.enunciado}`;

  return llamarApi({
    system,
    mensajes: [{
      role: 'user',
      content: [
        imagen,
        { type: 'text', text: 'Transcribe mi hoja y dime si mi desconstrucción se entiende bien.' },
      ],
    }],
    maxTokens: 2048,
    schema: SCHEMA_TRANSCRIPCION,
  });
}

/* ================ Revisión del intento (tras el revelado) ============== */

/**
 * Revisión "mirar hacia atrás": compara el intento del usuario (texto y/o
 * foto) con la solución oficial y señala con precisión dónde divergió.
 * SOLO debe llamarse con la solución ya revelada — el gating lo garantiza
 * la app, no este módulo.
 */
export async function revisarIntento(problema, { desconstruccion, intentoTexto, imagen }) {
  const system = `${SYSTEM_CHAT_REVISION}

Esta vez NO es un chat: entrega una revisión completa en prosa (sin encabezados Markdown), de 120 a 250 palabras, con esta estructura: (1) qué hizo bien el proceso, (2) el punto EXACTO de divergencia citando su trabajo, (3) la señal del enunciado que dispara la idea correcta.

Problema: ${problema.enunciado}

Solución oficial: ${problema.solucion}

Explicación oficial: ${problema.explicacion}`;

  const partes = [];
  if (imagen) partes.push(imagen);
  const texto = [
    desconstruccion ? `Mi desconstrucción durante el forcejeo:\n${desconstruccion}` : null,
    intentoTexto ? `Mi intento / comparación escrita:\n${intentoTexto}` : null,
    imagen ? 'Adjunto la foto de mi intento en papel.' : null,
    '¿Dónde exactamente divergió mi camino de la solución?',
  ].filter(Boolean).join('\n\n');
  partes.push({ type: 'text', text: texto });

  return llamarApi({
    system,
    mensajes: [{ role: 'user', content: partes }],
    maxTokens: 2048,
  });
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
