/**
 * adaptiveEngine.js — Motor de dificultad dinámica.
 *
 * Regla olímpica de dificultad óptima: mantener al usuario en una zona
 * donde resuelve ~30-50% de los problemas sin ayuda.
 *   successRate > 0.55  → subir dificultad (estancamiento)
 *   successRate < 0.30  → bajar dificultad (frustración)
 *
 * Además aplica ajustes inmediatos por desempeño puntual:
 *   score > 85, hints <= 1, tiempo < esperado  → dificultad++
 *   score < 50 o hints >= 3                    → dificultad--
 */

import { load, update } from './storage.js';

const VENTANA = 8; // problemas recientes considerados para la tasa de éxito
export const MIN_DIFICULTAD = 1;
export const MAX_DIFICULTAD = 5;

function clamp(n) {
  return Math.min(MAX_DIFICULTAD, Math.max(MIN_DIFICULTAD, n));
}

/** Tasa de éxito "sin ayuda" en la ventana reciente (resuelto con <=1 hint). */
export function tasaExitoReciente() {
  const historial = load('historial');
  if (historial.length === 0) return null;
  const recientes = historial.slice(-VENTANA);
  const exitos = recientes.filter(
    (h) => h.autoevaluacion === 'resuelto' && h.hintsUsados <= 1
  ).length;
  return exitos / recientes.length;
}

/**
 * Calcula la puntuación de una sesión.
 * Base por autoevaluación, penalización por hints, bono por desconstrucción rica.
 */
export function calcularScore({ autoevaluacion, hintsUsados, desconstruccionLen }) {
  const base = { resuelto: 100, parcial: 60, fallado: 25 }[autoevaluacion] ?? 0;
  const penalHints = hintsUsados * 8;
  const bonoDescon = desconstruccionLen >= 400 ? 5 : 0;
  return Math.max(0, Math.min(100, base - penalHints + bonoDescon));
}

/**
 * Ajusta la dificultad del perfil tras completar un problema.
 * Devuelve { antes, despues, motivo }.
 */
export function ajustarDificultad({ score, hintsUsados, tiempoMin, tiempoEstimado }) {
  const perfil = load('perfil');
  const antes = perfil.dificultad;
  let despues = antes;
  let motivo = 'estable';

  // Ajuste inmediato por desempeño puntual
  if (score > 85 && hintsUsados <= 1 && tiempoMin < tiempoEstimado) {
    despues = clamp(antes + 1);
    motivo = 'desempeño sobresaliente';
  } else if (score < 50 || hintsUsados >= 3) {
    despues = clamp(antes - 1);
    motivo = 'sesión con dificultades';
  }

  // Corrección por zona de aprendizaje (ventana reciente)
  const tasa = tasaExitoReciente();
  if (tasa !== null) {
    if (tasa > 0.55 && despues <= antes) {
      despues = clamp(antes + 1);
      motivo = 'tasa de éxito alta: zona de estancamiento';
    } else if (tasa < 0.30 && despues >= antes) {
      despues = clamp(antes - 1);
      motivo = 'tasa de éxito baja: zona de frustración';
    }
  }

  update('perfil', (p) => {
    p.dificultad = despues;
    return p;
  });

  return { antes, despues, motivo };
}

/** Rango de dificultad aceptable para seleccionar el próximo problema. */
export function rangoSeleccion() {
  const d = load('perfil').dificultad;
  return { min: clamp(d - 1), max: clamp(d + 1), centro: d };
}
