/**
 * avatar.js — "El pensador" (§2.3 HANDOFFCES).
 *
 * Avatar SVG generado por capas, estilo grabado/línea sobrio (nada cartoon).
 * La base (busto de perfil bajo la luz de una lámpara) es de todos; los
 * aditamentos se GANAN: el mapa requisito→capa vive en data/avatar.json.
 * Cada elemento ganado lleva su historia en un tooltip (<title>):
 * el avatar cuenta la historia del trabajo del usuario, no su estatus.
 */

import { ganadas } from './badges.js';
import { ratingPorEstrategia } from './analytics.js';
import { load } from './storage.js';

let mapa = null; // contenido de data/avatar.json

export async function init() {
  try {
    const res = await fetch('data/avatar.json');
    mapa = await res.json();
  } catch {
    mapa = null;
  }
}

const NS = 'http://www.w3.org/2000/svg';

function el(tag, attrs = {}) {
  const node = document.createElementNS(NS, tag);
  Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
  return node;
}

/** Grupo con estilo de grabado (línea fina, sin relleno). */
function grupo(transform, color = 'var(--lampara)') {
  return el('g', {
    transform,
    fill: 'none',
    stroke: color,
    'stroke-width': '1.6',
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
  });
}

/* --------------------- Base: el pensador y su lámpara ------------------ */

function dibujarBase(svg) {
  // Halo de la lámpara de escritorio: la luz es de la sala, no se gana
  svg.appendChild(el('circle', { cx: 120, cy: 110, r: 86, fill: 'var(--lampara-suave)', stroke: 'none' }));

  const base = grupo('', 'var(--texto-suave)');
  // Cabeza de perfil (línea de grabado simplificada)
  base.appendChild(el('circle', { cx: 120, cy: 88, r: 32 }));
  // Cuello y hombros
  base.appendChild(el('path', { d: 'M 104 116 Q 100 132 84 140 Q 120 168 156 140 Q 140 132 136 116' }));
  // Busto / pedestal
  base.appendChild(el('path', { d: 'M 70 196 Q 120 148 170 196' }));
  base.appendChild(el('line', { x1: 84, y1: 206, x2: 156, y2: 206 }));
  // Gesto pensante: una línea de mano hacia el mentón
  base.appendChild(el('path', { d: 'M 132 108 Q 142 116 138 126' }));
  svg.appendChild(base);
}

/* ------------------- Capas ganables (iconos de línea) ------------------ */

const DIBUJOS = {
  balanza(g) {
    g.appendChild(el('line', { x1: 0, y1: -16, x2: 0, y2: 8 }));
    g.appendChild(el('line', { x1: -14, y1: -10, x2: 14, y2: -10 }));
    g.appendChild(el('path', { d: 'M -18 -6 a 5 5 0 0 0 9 0' }));
    g.appendChild(el('path', { d: 'M 9 -6 a 5 5 0 0 0 9 0' }));
    g.appendChild(el('line', { x1: -6, y1: 8, x2: 6, y2: 8 }));
  },
  espejo(g) {
    g.appendChild(el('circle', { cx: 0, cy: -6, r: 9 }));
    g.appendChild(el('line', { x1: 0, y1: 3, x2: 0, y2: 15 }));
    g.appendChild(el('line', { x1: -4, y1: -9, x2: 3, y2: -2 }));
  },
  constelacion(g) {
    [[-24, 6], [-8, -4], [8, 2], [24, -6]].forEach(([x, y]) =>
      g.appendChild(el('circle', { cx: x, cy: y, r: 1.8, fill: 'currentColor', stroke: 'none' }))
    );
    g.appendChild(el('path', { d: 'M -24 6 L -8 -4 L 8 2 L 24 -6', opacity: 0.6 }));
  },
  compas(g) {
    g.appendChild(el('line', { x1: 0, y1: -14, x2: -8, y2: 10 }));
    g.appendChild(el('line', { x1: 0, y1: -14, x2: 8, y2: 10 }));
    g.appendChild(el('circle', { cx: 0, cy: -14, r: 2 }));
    g.appendChild(el('path', { d: 'M -8 10 Q 0 16 8 10', opacity: 0.6 }));
  },
  llave(g) {
    g.appendChild(el('circle', { cx: -8, cy: 0, r: 6 }));
    g.appendChild(el('line', { x1: -2, y1: 0, x2: 16, y2: 0 }));
    g.appendChild(el('line', { x1: 10, y1: 0, x2: 10, y2: 6 }));
    g.appendChild(el('line', { x1: 16, y1: 0, x2: 16, y2: 6 }));
  },
  pluma(g) {
    g.appendChild(el('path', { d: 'M -12 10 Q 2 -12 16 -10' }));
    g.appendChild(el('line', { x1: -4, y1: 2, x2: 2, y2: -4 }));
    g.appendChild(el('line', { x1: 2, y1: 6, x2: 8, y2: 0 }));
    g.appendChild(el('line', { x1: -12, y1: 10, x2: -16, y2: 14 }));
  },
  laurel(g) {
    // Laurel discreto sobre la cabeza (se dibuja en coordenadas absolutas)
    g.appendChild(el('path', { d: 'M 94 66 Q 84 88 96 106' }));
    g.appendChild(el('path', { d: 'M 146 66 Q 156 88 144 106' }));
    [[92, 76], [90, 88], [94, 99]].forEach(([x, y]) =>
      g.appendChild(el('line', { x1: x, y1: y, x2: x - 6, y2: y - 3 }))
    );
    [[148, 76], [150, 88], [146, 99]].forEach(([x, y]) =>
      g.appendChild(el('line', { x1: x, y1: y, x2: x + 6, y2: y - 3 }))
    );
  },
};

/** Posición de cada capa alrededor del busto (slots fijos, composición sobria). */
const POSICIONES = {
  balanza: 'translate(46,150)',
  espejo: 'translate(194,150)',
  constelacion: 'translate(120,26)',
  compas: 'translate(194,216)',
  llave: 'translate(46,216)',
  pluma: 'translate(120,236)',
  laurel: '', // coordenadas absolutas sobre la cabeza
};

/* ------------------------- Estado de requisitos ------------------------ */

/** Devuelve { ganada, fecha, n } para una capa según su requisito. */
function estadoCapa(capa) {
  const req = capa.requisito ?? {};
  if (req.tipo === 'dominio') {
    const r = ratingPorEstrategia().find((x) => x.estrategia === req.estrategia);
    return r?.dominada ? { ganada: true, fecha: r.fechaDominio } : { ganada: false };
  }
  if (req.tipo === 'insignia') {
    const reg = ganadas()[req.insignia];
    return reg ? { ganada: true, fecha: reg.fecha } : { ganada: false };
  }
  if (req.tipo === 'examenes') {
    const aprobados = Object.values(load('estudio').examenes ?? {}).filter((e) => e.aprobado).length;
    return aprobados >= (req.minimo ?? 1) ? { ganada: true, n: aprobados } : { ganada: false };
  }
  return { ganada: false };
}

/* ------------------------------ Render --------------------------------- */

/**
 * Capas ganadas por el usuario LOCAL, en el formato que viaja a la vitrina
 * del claustro: [{id, fecha, n}]. Es la representación pública del avatar.
 */
export function capasGanadas() {
  return (mapa?.capas ?? [])
    .map((capa) => ({ capa, estado: estadoCapa(capa) }))
    .filter((x) => x.estado.ganada)
    .map((x) => ({ id: x.capa.id, fecha: x.estado.fecha ?? null, n: x.estado.n ?? null }));
}

function renderCapas(contenedor, capas, etiqueta) {
  if (!contenedor) return;
  contenedor.innerHTML = '';

  const svg = el('svg', { viewBox: '0 0 240 260', role: 'img', 'aria-label': etiqueta });
  dibujarBase(svg);

  (capas ?? []).forEach(({ id, fecha, n }) => {
    const capa = (mapa?.capas ?? []).find((c) => c.id === id);
    if (!capa || !DIBUJOS[id]) return;
    const g = grupo(POSICIONES[id] ?? '');
    DIBUJOS[id](g);
    const title = el('title');
    title.textContent = capa.tooltip.replace('{fecha}', fecha ?? '').replace('{n}', n ?? '');
    g.appendChild(title);
    svg.appendChild(g);
  });

  contenedor.appendChild(svg);
}

/** Avatar del usuario local (capas calculadas de su propio estado). */
export function render(contenedor) {
  renderCapas(contenedor, capasGanadas(), 'El pensador: tu avatar, construido con tu propio trabajo');
}

/** Avatar de un amigo, a partir de las capas publicadas en su vitrina. */
export function renderDesdeCapas(contenedor, capas, nombre) {
  renderCapas(contenedor, capas, `El pensador de ${nombre ?? 'un colega'}`);
}
