/**
 * timer.js — Temporizador de reflexión obligatorio (§2.6 HANDOFFCES).
 *
 * Basado en timestamps persistidos en la asignación (no en contadores):
 * recargar la página no reinicia la cuenta (desirable difficulty real).
 *
 * Pausa/reanudar: se guarda `pausadoEn` y se acumula `msPausadoTotal`;
 * el tiempo EFECTIVO de forcejeo = ahora − inicio − pausas. Pausar nunca
 * adelanta el desbloqueo de la solución: solo lo pospone (pedagógicamente
 * neutro). Los checkpoints se calculan sobre tiempo efectivo.
 *
 * Duración configurable 20-120 min (pasos de 5). El mínimo NO baja de 20:
 * el piso de forcejeo es la regla pedagógica central de claude.md y no se
 * negocia desde la UI. Una vez iniciado el problema la duración queda fija
 * para esa asignación; solo puede EXTENDERSE en caliente (+10 min), lo cual
 * jamás rompe el gating (un desbloqueo ya ganado no se revoca).
 */

import { load, update } from './storage.js';

export const DURACION_DEFECTO_MIN = 20;  // la dosis del PDF
export const DURACION_MINIMA_MIN = 20;   // piso pedagógico innegociable
export const DURACION_MAXIMA_MIN = 120;
export const PASO_MIN = 5;

let intervalId = null;

/** Normaliza una duración elegida por el usuario al rango y paso permitidos. */
export function normalizarDuracion(min) {
  const n = Math.round(Number(min) / PASO_MIN) * PASO_MIN;
  if (!Number.isFinite(n)) return DURACION_DEFECTO_MIN;
  return Math.min(DURACION_MAXIMA_MIN, Math.max(DURACION_MINIMA_MIN, n));
}

/** Duración de la asignación actual, en minutos. */
export function duracionMin() {
  return load('asignacion')?.duracionMin ?? DURACION_DEFECTO_MIN;
}

function duracionMs() {
  return duracionMin() * 60 * 1000;
}

/**
 * Garantiza que la asignación tenga timerInicio y duración; los crea si
 * faltan (migración silenciosa de asignaciones previas a §2.6).
 */
export function asegurarInicio() {
  return update('asignacion', (a) => {
    if (!a) return a;
    if (!a.timerInicio) a.timerInicio = Date.now();
    if (!a.duracionMin) a.duracionMin = DURACION_DEFECTO_MIN;
    if (a.msPausadoTotal == null) a.msPausadoTotal = 0;
    if (a.pausas == null) a.pausas = 0;
    return a;
  });
}

/** Milisegundos de forcejeo EFECTIVO (descuenta pausas; congelado en pausa). */
export function msTranscurridos() {
  const a = load('asignacion');
  if (!a?.timerInicio) return 0;
  const fin = a.pausadoEn ?? Date.now();
  return Math.max(0, fin - a.timerInicio - (a.msPausadoTotal ?? 0));
}

export function msRestantes() {
  return Math.max(0, duracionMs() - msTranscurridos());
}

export function cumplido() {
  const a = load('asignacion');
  if (a?.timerCumplido) return true; // un desbloqueo ganado no se revoca
  return msRestantes() === 0;
}

export function enPausa() {
  return Boolean(load('asignacion')?.pausadoEn);
}

/** Pausa el cronómetro (interrupciones de la vida real; sin culpa). */
export function pausar() {
  update('asignacion', (a) => {
    if (a && a.timerInicio && !a.pausadoEn && !a.revelado && !a.completado) {
      a.pausadoEn = Date.now();
      a.pausas = (a.pausas ?? 0) + 1;
    }
    return a;
  });
}

export function reanudar() {
  update('asignacion', (a) => {
    if (a?.pausadoEn) {
      a.msPausadoTotal = (a.msPausadoTotal ?? 0) + (Date.now() - a.pausadoEn);
      a.pausadoEn = null;
    }
    return a;
  });
}

/**
 * Extiende la duración en caliente (+10 min por defecto). Solo crece, nunca
 * recorta, y no revoca un timerCumplido ya ganado.
 */
export function extender(minutos = 10) {
  return update('asignacion', (a) => {
    if (a && !a.completado) {
      a.duracionMin = Math.min(
        DURACION_MAXIMA_MIN,
        (a.duracionMin ?? DURACION_DEFECTO_MIN) + minutos
      );
    }
    return a;
  });
}

export function formato(ms) {
  const total = Math.ceil(ms / 1000);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

/**
 * Inicia el tic visual. onTick(msRestantes, fraccionTranscurrida, enPausa);
 * onDone() se dispara una sola vez al llegar a cero (marca timerCumplido).
 * El intervalo sigue vivo tras llegar a cero para soportar extensiones.
 */
export function iniciar(onTick, onDone) {
  detener();
  const tick = () => {
    const ms = msRestantes();
    onTick(ms, 1 - ms / duracionMs(), enPausa());
    if (ms === 0 && !load('asignacion')?.timerCumplido) {
      update('asignacion', (a) => {
        if (a) a.timerCumplido = true;
        return a;
      });
      onDone();
    }
  };
  tick();
  intervalId = setInterval(tick, 1000);
}

export function detener() {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
}
