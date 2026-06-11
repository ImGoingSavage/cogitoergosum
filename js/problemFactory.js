/**
 * problemFactory.js — Generador de variantes isomórficas con la API de Claude.
 *
 * Visión (claude.md § Sistema de Curación Automática): tomar un problema
 * semilla, extraer su estructura cognitiva (estrategia, esquema, invariante
 * o patrón central) y generar un problema nuevo con contexto superficial
 * completamente distinto pero la MISMA estructura. Eso entrena esquemas
 * mentales y transferencia, no memorización.
 *
 * Reglas de diseño:
 *  - Módulo opcional: la app funciona completa sin IA. Todo error de red,
 *    refusal o formato termina en `null` (fallback silencioso).
 *  - La cuenta activa se lee SIEMPRE desde aiMentor.js (única fuente de
 *    verdad multi-cuenta). Nada de keys propias ni hardcodeadas.
 *  - Los problemas generados viven en LocalStorage (cps_problemasGenerados)
 *    y NO dependen de la cuenta: cambiar o borrar cuentas no borra nada.
 *  - El usuario nunca debe poder deducir de qué semilla viene una variante;
 *    `semilla_id` es trazabilidad interna, jamás se muestra en la UI.
 *  - Structured outputs (output_config.format json_schema) garantizan JSON
 *    válido; la longitud exacta de los hints se valida aquí (el schema no
 *    soporta restricciones de longitud de arreglos).
 */

import { load, update } from './storage.js';
import { cuentaActiva, mentorDisponible } from './aiMentor.js';

const API_URL = 'https://api.anthropic.com/v1/messages';
const MODEL = 'claude-opus-4-8';

// Los ids generados viven por encima de cualquier id estático futuro.
const ID_BASE = 10000;

const SYSTEM_FACTORY = `Eres un diseñador experto de problemas de entrenamiento mental, formado en la tradición de Pólya, las olimpiadas matemáticas y la investigación sobre transferencia de aprendizaje.

Tu tarea: dado un problema semilla, crear una VARIANTE ISOMÓRFICA.

Proceso obligatorio:
1. Extrae la estructura cognitiva profunda de la semilla: la estrategia mental subyacente, el esquema, el invariante o el patrón que la resuelve.
2. Diseña un problema nuevo con esa MISMA estructura profunda pero con un contexto superficial COMPLETAMENTE distinto: cambia dominio, objetos, números, escenario y narrativa. Nadie debe poder reconocer la semilla a partir de la variante.
3. La variante debe tener dificultad comparable a la semilla y resolverse con la misma idea central.

Requisitos del resultado (todo en español, tono sobrio):
- "enunciado": autocontenido, preciso, sin pistas sobre la estrategia ni etiquetas de clasificación.
- "hints": EXACTAMENTE 5 pistas socráticas progresivas. Nivel 1 redirige la atención con una pregunta; nivel 2 señala una estructura o restricción relevante; nivel 3 reduce el espacio de búsqueda; nivel 4 sugiere una familia de estrategias; nivel 5 describe casi todo el camino dejando el paso final al usuario. Ninguna pista revela la respuesta.
- "solucion": respuesta correcta con el razonamiento completo y verificado. Verifica tu aritmética con cuidado antes de responder.
- "explicacion": qué hace funcionar la idea central y por qué es transferible.
- "conceptos", "transferencias" y "tags": listas breves (2-4 elementos).
- Nunca menciones la semilla, ni que esto es una variante, ni la estrategia de clasificación.`;

/* ======================= Acceso a los generados ======================== */

export function problemasGenerados() {
  return load('problemasGenerados');
}

function siguienteId() {
  const ids = problemasGenerados().map((p) => p.id);
  return Math.max(ID_BASE, ...ids) + 1;
}

/* ============================ Validación =============================== */

const SCHEMA_VARIANTE = {
  type: 'object',
  properties: {
    titulo: { type: 'string' },
    enunciado: { type: 'string' },
    hints: { type: 'array', items: { type: 'string' } },
    solucion: { type: 'string' },
    explicacion: { type: 'string' },
    conceptos: { type: 'array', items: { type: 'string' } },
    transferencias: { type: 'array', items: { type: 'string' } },
    tags: { type: 'array', items: { type: 'string' } },
  },
  required: [
    'titulo', 'enunciado', 'hints', 'solucion',
    'explicacion', 'conceptos', 'transferencias', 'tags',
  ],
  additionalProperties: false,
};

function textoNoVacio(v) {
  return typeof v === 'string' && v.trim().length > 0;
}

function listaDeTextos(v) {
  return Array.isArray(v) && v.every(textoNoVacio);
}

/** El schema garantiza tipos; aquí se exige lo que el schema no puede. */
function varianteValida(c) {
  return (
    c &&
    textoNoVacio(c.titulo) &&
    textoNoVacio(c.enunciado) &&
    textoNoVacio(c.solucion) &&
    textoNoVacio(c.explicacion) &&
    listaDeTextos(c.hints) && c.hints.length === 5 &&
    listaDeTextos(c.conceptos) &&
    listaDeTextos(c.transferencias) &&
    listaDeTextos(c.tags)
  );
}

/* ============================ Generación =============================== */

/**
 * Genera una variante isomórfica del problema semilla y la guarda en
 * LocalStorage. Devuelve el problema generado (con el mismo formato que
 * los estáticos) o null si la IA no está disponible o algo falla.
 */
export async function generarVariante(semilla) {
  const cuenta = cuentaActiva();
  if (!cuenta?.apiKey || !semilla) return null;

  const userPrompt = [
    'Problema semilla (solo para tu análisis interno; jamás lo menciones):',
    JSON.stringify({
      enunciado: semilla.enunciado,
      solucion: semilla.solucion,
      explicacion: semilla.explicacion,
      estrategia: semilla.estrategia,
      conceptos: semilla.conceptos,
      dificultad: semilla.dificultad,
    }),
    'Genera una variante isomórfica siguiendo tu proceso obligatorio.',
  ].join('\n\n');

  try {
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
        max_tokens: 16000,
        thinking: { type: 'adaptive' },
        system: SYSTEM_FACTORY,
        output_config: {
          format: { type: 'json_schema', schema: SCHEMA_VARIANTE },
        },
        messages: [{ role: 'user', content: userPrompt }],
      }),
    });

    if (!res.ok) return null;
    const data = await res.json();
    // Refusal o salida truncada: descartar en silencio.
    if (data.stop_reason === 'refusal' || data.stop_reason === 'max_tokens') return null;

    const texto = (data.content ?? []).find((b) => b.type === 'text')?.text;
    if (!texto) return null;

    const candidato = JSON.parse(texto);
    if (!varianteValida(candidato)) return null;

    const problema = {
      id: siguienteId(),
      titulo: candidato.titulo.trim(),
      // Estructura cognitiva heredada de la semilla: el motor adaptativo,
      // el interleaving y la repetición espaciada la tratan como cualquier
      // otro problema de esa estrategia y dificultad.
      estrategia: semilla.estrategia,
      dificultad: semilla.dificultad,
      enunciado: candidato.enunciado.trim(),
      hints: candidato.hints.map((h) => h.trim()),
      solucion: candidato.solucion.trim(),
      explicacion: candidato.explicacion.trim(),
      tiempo_estimado: semilla.tiempo_estimado,
      conceptos: candidato.conceptos,
      transferencias: candidato.transferencias,
      source: 'Variante generada por IA',
      source_url: '',
      year: '',
      tags: candidato.tags,
      origen: 'generado',
      semilla_id: semilla.id,
    };

    update('problemasGenerados', (arr) => {
      arr.push(problema);
      return arr;
    });
    return problema;
  } catch {
    // Red caída, JSON corrupto, key inválida…: la app sigue sin IA.
    return null;
  }
}

export { mentorDisponible as factoryDisponible };
