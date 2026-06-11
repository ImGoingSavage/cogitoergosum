/**
 * analytics.js — Dashboard cognitivo.
 * Calcula métricas del historial y genera visualizaciones SVG sin librerías.
 */

import { load } from './storage.js';

export const NOMBRES_ESTRATEGIA = {
  inversion: 'Inversión',
  optimizacion: 'Optimización',
  invariantes: 'Invariantes',
  patrones: 'Patrones',
};

/** Descripción de la jugada, para el momento de aprendizaje post-sesión. */
export const DESCRIPCIONES_ESTRATEGIA = {
  inversion: 'pensar hacia atrás desde lo que quieres lograr',
  optimizacion: 'maximizar o minimizar bajo restricciones',
  invariantes: 'detectar lo que permanece constante mientras todo cambia',
  patrones: 'encontrar la regularidad oculta y explotarla',
};

export function resumen() {
  const historial = load('historial');
  const perfil = load('perfil');

  const total = historial.length;
  const resueltos = historial.filter((h) => h.autoevaluacion === 'resuelto').length;
  const tasaExito = total ? Math.round((resueltos / total) * 100) : 0;
  const tiempoProm = total
    ? Math.round(historial.reduce((s, h) => s + h.tiempoMin, 0) / total)
    : 0;
  const hintsTotales = historial.reduce((s, h) => s + h.hintsUsados, 0);

  // Reconocimiento de disparadores en frío: % de sesiones donde la predicción
  // de jugada (hecha antes de revelar) coincidió con la estrategia real.
  const conPrediccion = historial.filter((h) => h.prediccion);
  const reconocidos = conPrediccion.filter((h) => h.prediccion === h.estrategia).length;
  const disparadores = conPrediccion.length
    ? Math.round((reconocidos / conPrediccion.length) * 100)
    : null;

  // El termómetro del cuaderno: fichas completas (moraleja + disparador).
  const fichas = historial.filter((h) => h.moraleja && h.disparador).length;

  return {
    total,
    resueltos,
    tasaExito,
    tiempoProm,
    hintsTotales,
    disparadores,
    fichas,
    racha: perfil.racha,
    dificultadActual: perfil.dificultad,
  };
}

/**
 * Fichas del cuaderno de moralejas, de la más reciente a la más antigua.
 * Solo entran sesiones que destilaron al menos moraleja o disparador.
 */
export function cuadernoMoralejas() {
  return load('historial')
    .filter((h) => h.moraleja || h.disparador)
    .slice()
    .reverse();
}

/** Desempeño por estrategia mental: { estrategia, nombre, sesiones, tasa } */
export function porEstrategia() {
  const historial = load('historial');
  return Object.keys(NOMBRES_ESTRATEGIA).map((e) => {
    const sesiones = historial.filter((h) => h.estrategia === e);
    const exitos = sesiones.filter((h) => h.autoevaluacion === 'resuelto').length;
    return {
      estrategia: e,
      nombre: NOMBRES_ESTRATEGIA[e],
      sesiones: sesiones.length,
      tasa: sesiones.length ? exitos / sesiones.length : null,
    };
  });
}

/**
 * Rating por heurística (§2.5 HANDOFFCES, estilo Alcumus): un nivel por
 * estrategia, derivado del historial existente. PRIVADO por defecto: mide
 * al usuario contra su propio pasado, jamás contra otros.
 *
 * Umbral documentado: DOMINADA = ≥5 sesiones con score ≥70 en esa
 * estrategia. fechaDominio = fecha de la 5.ª sesión que lo cumplió.
 * Nivel 1-5 = promedio de score de las últimas 5 sesiones de la
 * estrategia, mapeado por tramos de 20 puntos.
 */
export function ratingPorEstrategia() {
  const historial = load('historial');
  return Object.keys(NOMBRES_ESTRATEGIA).map((e) => {
    const sesiones = historial.filter((h) => h.estrategia === e);
    const fuertes = sesiones.filter((h) => h.score >= 70);
    const dominada = fuertes.length >= 5;
    const recientes = sesiones.slice(-5);
    const promedio = recientes.length
      ? recientes.reduce((s, h) => s + h.score, 0) / recientes.length
      : null;
    return {
      estrategia: e,
      nombre: NOMBRES_ESTRATEGIA[e],
      sesiones: sesiones.length,
      nivel: promedio === null ? null : Math.max(1, Math.min(5, Math.ceil(promedio / 20))),
      dominada,
      fechaDominio: dominada ? fuertes[4].fecha : null,
    };
  });
}

export function estrategiasDominadasYDebiles() {
  const datos = porEstrategia().filter((d) => d.sesiones >= 2);
  const dominadas = datos.filter((d) => d.tasa >= 0.6).map((d) => d.nombre);
  const debiles = datos.filter((d) => d.tasa < 0.4).map((d) => d.nombre);
  return { dominadas, debiles };
}

/* ---------- Generadores SVG ---------- */

const SVG_NS = 'http://www.w3.org/2000/svg';

function el(tag, attrs = {}) {
  const node = document.createElementNS(SVG_NS, tag);
  Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
  return node;
}

/**
 * Curva de dificultad y scores: línea de dificultad + puntos de score
 * sobre las últimas sesiones.
 */
export function svgCurvaDificultad(ancho = 560, alto = 180) {
  const historial = load('historial').slice(-20);
  const svg = el('svg', {
    viewBox: `0 0 ${ancho} ${alto}`,
    class: 'chart',
    role: 'img',
    'aria-label': 'Curva de dificultad y puntuaciones recientes',
  });

  if (historial.length === 0) {
    const t = el('text', { x: ancho / 2, y: alto / 2, class: 'chart-empty', 'text-anchor': 'middle' });
    t.textContent = 'Aún no hay sesiones registradas';
    svg.appendChild(t);
    return svg;
  }

  const m = { top: 14, right: 14, bottom: 22, left: 30 };
  const w = ancho - m.left - m.right;
  const h = alto - m.top - m.bottom;
  const n = historial.length;
  const x = (i) => m.left + (n === 1 ? w / 2 : (i / (n - 1)) * w);
  const yDif = (d) => m.top + h - ((d - 1) / 4) * h;        // dificultad 1-5
  const yScore = (s) => m.top + h - (s / 100) * h;          // score 0-100

  // Rejilla horizontal por nivel de dificultad
  for (let d = 1; d <= 5; d++) {
    svg.appendChild(el('line', {
      x1: m.left, y1: yDif(d), x2: ancho - m.right, y2: yDif(d), class: 'chart-grid',
    }));
    const lbl = el('text', { x: m.left - 8, y: yDif(d) + 4, class: 'chart-label', 'text-anchor': 'end' });
    lbl.textContent = d;
    svg.appendChild(lbl);
  }

  // Línea de dificultad
  const path = historial
    .map((s, i) => `${i === 0 ? 'M' : 'L'} ${x(i).toFixed(1)} ${yDif(s.dificultad).toFixed(1)}`)
    .join(' ');
  svg.appendChild(el('path', { d: path, class: 'chart-line' }));

  // Puntos de score (color según autoevaluación)
  historial.forEach((s, i) => {
    svg.appendChild(el('circle', {
      cx: x(i), cy: yScore(s.score), r: 4,
      class: `chart-dot dot-${s.autoevaluacion}`,
    }));
  });

  return svg;
}

/** Barras horizontales de tasa de éxito por estrategia. */
export function svgBarrasEstrategias(ancho = 560, altoFila = 40) {
  const datos = porEstrategia();
  const alto = datos.length * altoFila + 10;
  const svg = el('svg', {
    viewBox: `0 0 ${ancho} ${alto}`,
    class: 'chart',
    role: 'img',
    'aria-label': 'Tasa de éxito por estrategia mental',
  });

  const labelW = 130;
  const barW = ancho - labelW - 60;

  datos.forEach((d, i) => {
    const y = i * altoFila + 12;

    const lbl = el('text', { x: 0, y: y + 14, class: 'chart-label' });
    lbl.textContent = d.nombre;
    svg.appendChild(lbl);

    svg.appendChild(el('rect', {
      x: labelW, y, width: barW, height: 18, rx: 4, class: 'chart-bar-bg',
    }));

    if (d.tasa !== null) {
      svg.appendChild(el('rect', {
        x: labelW, y, width: Math.max(2, barW * d.tasa), height: 18, rx: 4, class: 'chart-bar',
      }));
    }

    const val = el('text', { x: labelW + barW + 8, y: y + 14, class: 'chart-label' });
    val.textContent = d.tasa === null ? '—' : `${Math.round(d.tasa * 100)}% (${d.sesiones})`;
    svg.appendChild(val);
  });

  return svg;
}
