/**
 * spacedRepetition.js — Repetición espaciada para problemas difíciles o fallados.
 * Intervalos crecientes: 3 → 7 → 14 → 30 días.
 *
 * Un problema entra al ciclo de revisión cuando la sesión fue débil
 * (score < 50, autoevaluación fallida o 3+ hints). Cada revisión exitosa
 * avanza la etapa; una revisión fallida reinicia el ciclo.
 */

import { load, update, hoy } from './storage.js';

export const INTERVALOS_DIAS = [3, 7, 14, 30];

function sumarDias(fechaISO, dias) {
  const d = new Date(fechaISO + 'T00:00:00');
  d.setDate(d.getDate() + dias);
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${mm}-${dd}`;
}

/** ¿La sesión amerita programar (o reprogramar) revisión? */
export function necesitaRevision({ score, autoevaluacion, hintsUsados }) {
  return score < 50 || autoevaluacion === 'fallado' || hintsUsados >= 3;
}

/**
 * Registra el resultado de una sesión en el sistema de revisiones.
 * - Sesión débil: programa revisión (etapa 0 si es nueva, reinicio si recae).
 * - Sesión fuerte sobre un problema en revisión: avanza la etapa.
 * - Sesión fuerte sin historial de revisión: no hace nada.
 */
export function registrarResultado(problemId, sesion) {
  update('revisiones', (rev) => {
    const entrada = rev[problemId];
    const debil = necesitaRevision(sesion);

    if (debil) {
      rev[problemId] = {
        etapa: 0,
        proximaRevision: sumarDias(hoy(), INTERVALOS_DIAS[0]),
        revisiones: [...(entrada?.revisiones ?? []), { fecha: hoy(), resultado: 'debil' }],
      };
    } else if (entrada) {
      const nuevaEtapa = entrada.etapa + 1;
      if (nuevaEtapa >= INTERVALOS_DIAS.length) {
        // Ciclo completado: el problema se considera consolidado.
        rev[problemId] = {
          ...entrada,
          etapa: nuevaEtapa,
          proximaRevision: null,
          revisiones: [...entrada.revisiones, { fecha: hoy(), resultado: 'consolidado' }],
        };
      } else {
        rev[problemId] = {
          etapa: nuevaEtapa,
          proximaRevision: sumarDias(hoy(), INTERVALOS_DIAS[nuevaEtapa]),
          revisiones: [...entrada.revisiones, { fecha: hoy(), resultado: 'exito' }],
        };
      }
    }
    return rev;
  });
}

/** IDs de problemas cuya revisión ya venció (ordenados por antigüedad). */
export function revisionesVencidas() {
  const rev = load('revisiones');
  const fecha = hoy();
  return Object.entries(rev)
    .filter(([, r]) => r.proximaRevision && r.proximaRevision <= fecha)
    .sort((a, b) => a[1].proximaRevision.localeCompare(b[1].proximaRevision))
    .map(([id]) => Number(id));
}

export function enRevision(problemId) {
  const rev = load('revisiones');
  return Boolean(rev[problemId]?.proximaRevision);
}
