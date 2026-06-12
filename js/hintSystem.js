/**
 * hintSystem.js — Sistema progresivo de pistas socráticas.
 *
 * Cinco niveles por problema:
 *   1 Redirigir atención · 2 Estructura relevante · 3 Reducir búsqueda
 *   4 Sugerir estrategia · 5 Revelar el camino
 *
 * Reglas: liberación secuencial (no puedes saltar al nivel 3 sin el 2),
 * cada hint penaliza la puntuación y queda registrado en la asignación.
 */

import { load, update, registrarDiagnostico } from './storage.js';
import { generarHintIA, mentorDisponible } from './aiMentor.js';

export const PENALIZACION_POR_HINT = 8;
export const MAX_NIVEL = 5;

export function hintsUsados() {
  return load('asignacion')?.hintsUsados ?? [];
}

export function siguienteNivel() {
  const usados = hintsUsados();
  return usados.length >= MAX_NIVEL ? null : usados.length + 1;
}

/**
 * Solicita el siguiente hint disponible. Registra el uso y devuelve
 * { nivel, texto, fuente: 'estatico'|'ia' }.
 * Si el mentor IA está configurado, intenta generar un hint dinámico
 * adaptado a la desconstrucción del usuario; si falla, cae al estático.
 */
export async function solicitarHint(problema) {
  const nivel = siguienteNivel();
  if (nivel === null) return null;

  let texto = problema.hints[nivel - 1];
  let fuente = 'estatico';

  if (mentorDisponible()) {
    const asignacion = load('asignacion');
    try {
      const dinamico = await generarHintIA(problema, nivel, asignacion?.desconstruccion ?? '');
      if (dinamico) {
        texto = dinamico;
        fuente = 'ia';
      }
    } catch (e) {
      registrarDiagnostico('mentor-hint', e.message);
      // El hint estático curado es el respaldo silencioso.
    }
  }

  update('asignacion', (a) => {
    if (a && !a.hintsUsados.includes(nivel)) a.hintsUsados.push(nivel);
    return a;
  });

  return { nivel, texto, fuente };
}

export function penalizacionActual() {
  return hintsUsados().length * PENALIZACION_POR_HINT;
}
