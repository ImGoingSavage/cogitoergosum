/**
 * pizarra.js — Pizarra de trabajo a mano alzada, estilo GoodNotes
 * (pedido del usuario, 2026-06-11): escribir con el Apple Pencil (o el
 * dedo, o el mouse) directamente en la app para forcejear los problemas.
 *
 * Comportamiento calcado de GoodNotes (funcionalidad, no su trade dress):
 *  - Pluma con presión del pencil; resaltador translúcido; goma de trazo;
 *    lazo (mover, duplicar, borrar en bloque).
 *  - Cada herramienta RECUERDA su color y su grosor (3 presets por
 *    herramienta, como los puntos de grosor de la barra de GoodNotes).
 *  - FIGURA PERFECTA: dibuja y sostén el pencil quieto ~0.6 s — el trazo
 *    se ajusta a línea, polilínea, triángulo, rectángulo o elipse.
 *  - El DEDO no dibuja cuando hay pencil: desplaza el lienzo (como en
 *    GoodNotes con "dibujar con el dedo" apagado). Doble toque del dedo:
 *    alterna pluma↔goma. NOTA honesta: el doble toque del PROPIO pencil
 *    es API nativa de iPadOS (UIPencilInteraction) y Safari no la expone
 *    a las web apps — el doble toque del dedo es el sustituto.
 *  - Dos dedos: pellizcar = zoom (0.5×–4×) y desplazar; toque corto de
 *    dos dedos = deshacer; de tres dedos = rehacer (gestos de GoodNotes).
 *  - Mouse: rueda = desplazar; ⌘/Ctrl + rueda = zoom al cursor.
 *  - Rechazo de palma: contactos anchos se ignoran; tras ver un pencil,
 *    el tacto jamás dibuja.
 *  - "Evaluar con el mentor" (solo con cuenta de Claude activa, §4.4):
 *    exporta la página actual como imagen y la envía al chat socrático.
 *
 * Cada contexto (problema del día, unidad de estudio, examen de bloque)
 * tiene SU pizarra, persistida en LocalStorage (cps_pizarras) vía
 * storage.js. Los trazos son locales del dispositivo: NO viajan al
 * servidor (igual que cps_asignacion — son papel de borrador, y pesan).
 * Sin dependencias: canvas 2D y pointer events, nada más.
 */

import { load, update } from './storage.js';

const $ = (id) => document.getElementById(id);

/* Tintas de la biblioteca (§1): tinta clara, índigo, lámpara, sanguina */
const COLORES = ['#ece7dd', '#8d96f7', '#d9a84e', '#e08f8f'];
const MAX_TABLEROS = 30;   // pizarras recordadas; las más viejas se podan
const MUESTREO_LAZO = 3;   // 1 de cada N puntos del trazo se testea contra el lazo

/* Presets de grosor por herramienta (los 3 puntos de GoodNotes) */
const GROSORES = {
  pluma: [2, 3.5, 6],
  marcador: [4, 7, 12],    // se pinta a ×3 de ancho
  goma: [12, 24, 40],      // radio de borrado (en pantalla)
};

const ZOOM_MIN = 0.5;
const ZOOM_MAX = 4;
const QUIETO_MS = 600;       // sostener para figura perfecta
const PALMA_ANCHO = 36;      // contactos más anchos se ignoran (palma)

let proveedorContexto = () => ({ clave: 'libre', titulo: 'Pizarra' });
let mentorCfg = { disponible: () => false, evaluar: null };

let canvas = null;
let ctx = null;

let clave = null;          // contexto de la pizarra abierta
let tablero = null;        // { paginas: [[trazo,…]], pagina }
let herramienta = 'pluma'; // 'pluma' | 'goma' | 'marcador' | 'lazo'

/* Memoria por herramienta (GoodNotes): color y grosor independientes */
let ajustes = {
  pluma: { color: COLORES[0], grosor: GROSORES.pluma[1] },
  marcador: { color: COLORES[2], grosor: GROSORES.marcador[1] },
  goma: { grosor: GROSORES.goma[1] },
};

/* Vista del lienzo: zoom y desplazamiento (pellizco / dedo / rueda) */
let vista = { k: 1, ox: 0, oy: 0 };

let activo = null;         // gesto de puntero de dibujo en curso
let seleccion = null;      // { indices: number[], caja: {x,y,w,h} }
let penVisto = false;      // tras ver un pencil, el dedo no dibuja: desplaza
let deshacer = [];
let rehacer = [];
let guardarTimeout = null;
let quietoTimer = null;    // dibuja-y-sostén → figura perfecta

let toques = new Map();    // pointers de tacto activos {id → {x, y}}
let gesto = null;          // gesto táctil en curso (pan / pinch)
let ultimoTap = null;      // doble toque del dedo → alternar pluma/goma
let hintMostrado = false;

/* ============================ Utilidades ============================== */

function paginaActual() {
  return tablero.paginas[tablero.pagina];
}

/** Punto del evento en coordenadas del MUNDO (descontando zoom/pan). */
function punto(e) {
  const r = canvas.getBoundingClientRect();
  return {
    x: (e.clientX - r.left - vista.ox) / vista.k,
    y: (e.clientY - r.top - vista.oy) / vista.k,
  };
}

function puntoPantalla(e) {
  const r = canvas.getBoundingClientRect();
  return { x: e.clientX - r.left, y: e.clientY - r.top };
}

function presion(e) {
  // Pencil: presión real. Mouse: 0.5 fijo. Tacto sin force: 0 → neutro.
  const p = e.pressure && e.pressure > 0 ? e.pressure : 0.5;
  return Math.min(1, Math.max(0.1, p));
}

function ancho(g, pr) {
  return g * (0.55 + 0.9 * pr);
}

function distancia2(ax, ay, bx, by) {
  return (ax - bx) ** 2 + (ay - by) ** 2;
}

/** Ray casting: ¿el punto cae dentro del polígono del lazo? */
function dentroPoligono(x, y, poli) {
  let dentro = false;
  for (let i = 0, j = poli.length - 1; i < poli.length; j = i++) {
    const xi = poli[i].x, yi = poli[i].y, xj = poli[j].x, yj = poli[j].y;
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) dentro = !dentro;
  }
  return dentro;
}

function cajaDe(indices) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  indices.forEach((i) => {
    paginaActual()[i].p.forEach(([x, y]) => {
      x0 = Math.min(x0, x); y0 = Math.min(y0, y);
      x1 = Math.max(x1, x); y1 = Math.max(y1, y);
    });
  });
  return { x: x0 - 10, y: y0 - 10, w: x1 - x0 + 20, h: y1 - y0 + 20 };
}

/* ==================== Figura perfecta (dibuja y sostén) =============== */

/** Ramer–Douglas–Peucker: simplifica el trazo a sus vértices esenciales. */
function rdp(pts, eps) {
  if (pts.length < 3) return pts.slice();
  const [x1, y1] = pts[0];
  const [x2, y2] = pts[pts.length - 1];
  const dx = x2 - x1, dy = y2 - y1;
  const len = Math.hypot(dx, dy) || 1e-9;
  let maxD = 0, idx = 0;
  for (let i = 1; i < pts.length - 1; i++) {
    const d = Math.abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / len;
    if (d > maxD) { maxD = d; idx = i; }
  }
  if (maxD <= eps) return [pts[0], pts[pts.length - 1]];
  return rdp(pts.slice(0, idx + 1), eps).slice(0, -1).concat(rdp(pts.slice(idx), eps));
}

/**
 * Reconoce el trazo como figura (línea, polilínea, triángulo, cuadrilátero,
 * rectángulo o elipse) y devuelve los puntos perfectos, o null si no hay
 * figura clara. Heurísticas clásicas: RDP para vértices; cerrado si los
 * extremos casi se tocan; elipse si lo cerrado es redondo (radios parejos
 * contra la elipse inscrita en su caja).
 */
function reconocerFigura(p) {
  if (p.length < 8) return null;
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  p.forEach(([x, y]) => {
    x0 = Math.min(x0, x); y0 = Math.min(y0, y);
    x1 = Math.max(x1, x); y1 = Math.max(y1, y);
  });
  const w = x1 - x0, h = y1 - y0;
  const diag = Math.hypot(w, h);
  if (diag < 30) return null;

  const cerrado =
    distancia2(p[0][0], p[0][1], p[p.length - 1][0], p[p.length - 1][1]) <
    (diag * 0.2) ** 2;

  const eps = Math.max(6, diag * 0.04);
  const xy = p.map(([x, y]) => [x, y]);
  let v;
  if (cerrado) {
    // RDP degenera si los extremos coinciden (contorno cerrado): se ancla
    // en los dos puntos más alejados entre sí y se simplifica cada mitad.
    let far = 1, fd = -1;
    xy.forEach(([x, y], i) => {
      const d = distancia2(x, y, xy[0][0], xy[0][1]);
      if (d > fd) { fd = d; far = i; }
    });
    const a = rdp(xy.slice(0, far + 1), eps);
    const b = rdp(xy.slice(far).concat([xy[0]]), eps);
    v = a.slice(0, -1).concat(b.slice(0, -1)); // sin duplicar anclas
    // Las anclas pueden caer a mitad de un lado recto: fuera colineales
    v = v.filter((q, i) => {
      const prev = v[(i - 1 + v.length) % v.length];
      const sig = v[(i + 1) % v.length];
      const ux = q[0] - prev[0], uy = q[1] - prev[1];
      const wx = sig[0] - q[0], wy = sig[1] - q[1];
      const cruz = Math.abs(ux * wy - uy * wx);
      const punto_ = ux * wx + uy * wy;
      return Math.atan2(cruz, punto_) > 0.26; // gira ≥ ~15°: vértice real
    });
  } else {
    v = rdp(xy, eps);
  }

  const pp = (x, y) => [x, y, 0.5];
  const poligono = (vs) => vs.map(([x, y]) => pp(x, y)).concat([pp(vs[0][0], vs[0][1])]);

  if (!cerrado) {
    if (v.length === 2) return [pp(v[0][0], v[0][1]), pp(v[1][0], v[1][1])]; // línea
    if (v.length <= 5) return v.map(([x, y]) => pp(x, y));                   // polilínea
    return null;
  }

  if (v.length < 3) return null;
  if (v.length === 3) return poligono(v); // triángulo

  if (v.length === 4) {
    // ¿Los 4 lados van con los ejes? → rectángulo perfecto de la caja
    const axial = v.every((q, i) => {
      const s = v[(i + 1) % 4];
      const ang = Math.abs(Math.atan2(s[1] - q[1], s[0] - q[0]));
      const aEje = Math.min(ang, Math.abs(ang - Math.PI / 2), Math.abs(ang - Math.PI));
      return aEje < 0.35; // ~20°
    });
    if (axial) return poligono([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]);
    return poligono(v); // cuadrilátero general
  }

  // ¿Redondo? — radios contra la elipse inscrita en la caja
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const a = Math.max(w / 2, 1e-6), b = Math.max(h / 2, 1e-6);
  let err = 0;
  p.forEach(([x, y]) => {
    err += Math.abs(((x - cx) / a) ** 2 + ((y - cy) / b) ** 2 - 1);
  });
  // Umbral fino: un rectángulo da error medio ≈ 1/3 contra su elipse
  // inscrita; un círculo a mano, ≈ 0.05 — el 0.18 los separa con holgura.
  if (err / p.length < 0.18) {
    const elipse = [];
    for (let i = 0; i <= 48; i++) {
      const t = (i / 48) * Math.PI * 2;
      elipse.push(pp(cx + a * Math.cos(t), cy + b * Math.sin(t)));
    }
    return elipse;
  }
  if (v.length <= 8) return poligono(v); // polígono de pocos vértices
  return null;
}

function intentarFigura() {
  if (!activo || activo.tipo !== 'trazo') return;
  const figura = reconocerFigura(activo.trazo.p);
  if (!figura) return;
  const trazo = activo.trazo;
  trazo.p = figura;
  trazo.f = 1; // figura: se pinta con segmentos RECTOS (sin suavizado)
  // Se confirma de inmediato (como GoodNotes al soltar tras el ajuste);
  // el puntero queda "muerto" hasta levantarse para no seguir dibujando.
  activo = { tipo: 'muerto', id: activo.id };
  const pag = paginaActual();
  pag.push(trazo);
  registrar({ tipo: 'anadir', pagina: tablero.pagina, indice: pag.length - 1, trazo });
  guardar();
  renderTodo();
  actualizarBarra();
  toast('Figura perfecta');
}

/* ============================== Render ================================ */

function aplicarTransform() {
  const dpr = window.devicePixelRatio || 1;
  ctx.setTransform(dpr * vista.k, 0, 0, dpr * vista.k, dpr * vista.ox, dpr * vista.oy);
}

function dibujarTrazo(trazo, dx = 0, dy = 0, c = ctx) {
  const p = trazo.p;
  // Resaltador (trazo.m): translúcido, ancho constante, en UN solo path —
  // pintado por segmentos, las uniones doblarían el alfa y se oscurecerían.
  if (trazo.m) {
    c.save();
    c.globalAlpha = 0.38;
    c.strokeStyle = trazo.c;
    c.lineCap = 'round';
    c.lineJoin = 'round';
    c.lineWidth = trazo.g * 3;
    c.beginPath();
    p.forEach(([x, y], i) => (i ? c.lineTo(x + dx, y + dy) : c.moveTo(x + dx, y + dy)));
    if (p.length === 1) c.lineTo(p[0][0] + dx + 0.1, p[0][1] + dy);
    c.stroke();
    c.restore();
    return;
  }
  c.strokeStyle = trazo.c;
  c.fillStyle = trazo.c;
  c.lineCap = 'round';
  c.lineJoin = 'round';
  // Figura perfecta (trazo.f): polilínea recta de ancho constante — el
  // suavizado de puntos medios redondearía las esquinas que el ajuste creó.
  if (trazo.f) {
    c.beginPath();
    c.lineWidth = ancho(trazo.g, 0.5);
    p.forEach(([x, y], i) => (i ? c.lineTo(x + dx, y + dy) : c.moveTo(x + dx, y + dy)));
    c.stroke();
    return;
  }
  if (p.length === 1) {
    c.beginPath();
    c.arc(p[0][0] + dx, p[0][1] + dy, ancho(trazo.g, p[0][2]) / 2, 0, Math.PI * 2);
    c.fill();
    return;
  }
  // Suavizado por puntos medios: cada segmento es una curva corta con su
  // propio grosor (así la presión del pencil modula el trazo, como tinta).
  for (let i = 1; i < p.length; i++) {
    const [xa, ya, pa] = p[i - 1];
    const [xb, yb, pb] = p[i];
    c.beginPath();
    c.lineWidth = ancho(trazo.g, (pa + pb) / 2);
    const m0x = i > 1 ? (xa + p[i - 2][0]) / 2 : xa;
    const m0y = i > 1 ? (ya + p[i - 2][1]) / 2 : ya;
    const m1x = (xa + xb) / 2;
    const m1y = (ya + yb) / 2;
    c.moveTo(m0x + dx, m0y + dy);
    c.quadraticCurveTo(xa + dx, ya + dy, m1x + dx, m1y + dy);
    if (i === p.length - 1) c.lineTo(xb + dx, yb + dy);
    c.stroke();
  }
}

function renderTodo() {
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.restore();
  aplicarTransform();
  // Mientras se arrastra una selección, los trazos seleccionados se pintan
  // desplazados (el movimiento se vuelve permanente en el pointerup).
  const ox = activo?.tipo === 'mover' ? activo.dx : 0;
  const oy = activo?.tipo === 'mover' ? activo.dy : 0;
  paginaActual().forEach((trazo, i) => {
    const sel = seleccion?.indices.includes(i);
    dibujarTrazo(trazo, sel ? ox : 0, sel ? oy : 0);
  });
  const fino = 1.5 / vista.k;
  if (seleccion) {
    const c = seleccion.caja;
    ctx.save();
    ctx.strokeStyle = '#8d96f7';
    ctx.lineWidth = fino;
    ctx.setLineDash([6 / vista.k, 5 / vista.k]);
    ctx.strokeRect(c.x + ox, c.y + oy, c.w, c.h);
    ctx.restore();
  }
  if (activo?.tipo === 'lazo' && activo.camino.length > 1) {
    ctx.save();
    ctx.strokeStyle = '#8d96f7';
    ctx.lineWidth = fino;
    ctx.setLineDash([6 / vista.k, 5 / vista.k]);
    ctx.beginPath();
    activo.camino.forEach((q, i) => (i ? ctx.lineTo(q.x, q.y) : ctx.moveTo(q.x, q.y)));
    ctx.stroke();
    ctx.restore();
  }
}

function redimensionar() {
  const wrap = $('pizarra-lienzo-wrap');
  const r = wrap.getBoundingClientRect();
  if (!r.width || !r.height) return;
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.round(r.width * dpr);
  canvas.height = Math.round(r.height * dpr);
  canvas.style.width = `${r.width}px`;
  canvas.style.height = `${r.height}px`;
  if (tablero) renderTodo();
}

/* ====================== Acciones (deshacer/rehacer) =================== */

function registrar(accion) {
  deshacer.push(accion);
  if (deshacer.length > 100) deshacer.shift();
  rehacer = [];
  actualizarBarra();
}

function aplicar(accion, inverso) {
  tablero.pagina = accion.pagina ?? tablero.pagina;
  const pag = paginaActual();
  switch (accion.tipo) {
    case 'anadir':
      if (inverso) pag.splice(accion.indice, 1);
      else pag.splice(accion.indice, 0, accion.trazo);
      break;
    case 'anadirVarios': // duplicados del lazo: siempre al final de la página
      if (inverso) pag.splice(pag.length - accion.trazos.length, accion.trazos.length);
      else pag.push(...accion.trazos);
      break;
    case 'borrar':
      if (inverso) {
        [...accion.items].reverse().forEach(({ i, trazo }) => pag.splice(i, 0, trazo));
      } else {
        accion.items.forEach(({ i }) => pag.splice(i, 1));
      }
      break;
    case 'mover': {
      const dx = inverso ? -accion.dx : accion.dx;
      const dy = inverso ? -accion.dy : accion.dy;
      accion.indices.forEach((i) => {
        pag[i].p.forEach((q) => {
          q[0] += dx;
          q[1] += dy;
        });
      });
      break;
    }
    case 'limpiar':
      if (inverso) tablero.paginas[accion.pagina] = accion.trazos;
      else tablero.paginas[accion.pagina] = [];
      break;
    case 'pagina':
      if (inverso) {
        tablero.paginas.splice(accion.indice, 1);
        tablero.pagina = Math.max(0, accion.indice - 1);
      } else {
        tablero.paginas.splice(accion.indice, 0, []);
        tablero.pagina = accion.indice;
      }
      break;
  }
}

function hacerDeshacer() {
  const a = deshacer.pop();
  if (!a) return;
  seleccion = null;
  aplicar(a, true);
  rehacer.push(a);
  guardar();
  renderTodo();
  actualizarBarra();
}

function hacerRehacer() {
  const a = rehacer.pop();
  if (!a) return;
  seleccion = null;
  aplicar(a, false);
  deshacer.push(a);
  guardar();
  renderTodo();
  actualizarBarra();
}

/* ========================== Persistencia ============================== */

function redondearTrazo(trazo) {
  trazo.p = trazo.p.map(([x, y, pr]) => [
    Math.round(x * 2) / 2,
    Math.round(y * 2) / 2,
    Math.round(pr * 100) / 100,
  ]);
  return trazo;
}

function guardar() {
  clearTimeout(guardarTimeout);
  guardarTimeout = setTimeout(persistir, 500);
}

function persistir() {
  clearTimeout(guardarTimeout);
  if (!tablero || !clave) return;
  const escribir = (max) => {
    update('pizarras', (t) => {
      t[clave] = {
        paginas: tablero.paginas,
        pagina: tablero.pagina,
        actualizado: Date.now(),
      };
      // Poda de tableros viejos (las claves "_..." son metadatos, no tableros)
      const claves = Object.keys(t).filter((k) => !k.startsWith('_'));
      if (claves.length > max) {
        claves
          .sort((a, b) => (t[a].actualizado ?? 0) - (t[b].actualizado ?? 0))
          .slice(0, claves.length - max)
          .forEach((k) => delete t[k]);
      }
      return t;
    });
  };
  try {
    escribir(MAX_TABLEROS);
  } catch {
    // LocalStorage lleno: podar fuerte y reintentar una vez. Si aun así
    // falla, la pizarra sigue funcionando en memoria durante la sesión.
    try {
      escribir(5);
    } catch {
      /* sin espacio: solo en memoria */
    }
  }
}

function guardarAjustes() {
  try {
    update('pizarras', (t) => {
      t._ajustes = structuredClone(ajustes);
      return t;
    });
  } catch {
    /* sin espacio: los ajustes viven en memoria */
  }
}

/* =================== Exportar página (para el mentor) ================= */

/**
 * Compone la página actual (fondo de la pizarra + trazos) en un JPEG
 * recortado a lo dibujado. Devuelve un data URL, o null si está vacía.
 */
function exportarPaginaJPEG() {
  const trazos = paginaActual();
  if (!trazos.length) return null;
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  trazos.forEach((t) => {
    const m = (t.m ? t.g * 3 : t.g) + 6;
    t.p.forEach(([x, y]) => {
      x0 = Math.min(x0, x - m); y0 = Math.min(y0, y - m);
      x1 = Math.max(x1, x + m); y1 = Math.max(y1, y + m);
    });
  });
  const w = Math.max(1, x1 - x0), h = Math.max(1, y1 - y0);
  const escala = Math.min(2, 1500 / Math.max(w, h));
  const off = document.createElement('canvas');
  off.width = Math.max(1, Math.round(w * escala));
  off.height = Math.max(1, Math.round(h * escala));
  const c2 = off.getContext('2d');
  c2.fillStyle = '#1d1a16'; // el papel de la pizarra
  c2.fillRect(0, 0, off.width, off.height);
  c2.setTransform(escala, 0, 0, escala, -x0 * escala, -y0 * escala);
  trazos.forEach((t) => dibujarTrazo(t, 0, 0, c2));
  return off.toDataURL('image/jpeg', 0.85);
}

/* ===================== Zoom, pan y gestos táctiles ==================== */

function fijarZoom(k, pivoteX, pivoteY) {
  const nuevo = Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, k));
  // El punto del mundo bajo el pivote no se mueve al cambiar la escala
  vista.ox = pivoteX - ((pivoteX - vista.ox) / vista.k) * nuevo;
  vista.oy = pivoteY - ((pivoteY - vista.oy) / vista.k) * nuevo;
  vista.k = nuevo;
  renderTodo();
  chipZoom();
}

let chipZoomTimer = null;
function chipZoom() {
  const chip = $('piz-zoom');
  chip.textContent = `${Math.round(vista.k * 100)}%`;
  chip.hidden = false;
  clearTimeout(chipZoomTimer);
  chipZoomTimer = setTimeout(() => { chip.hidden = true; }, 900);
}

let toastTimer = null;
function toast(texto, ms = 1500) {
  const t = $('piz-toast');
  t.textContent = texto;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; }, ms);
}

function abortarTrazoTactil() {
  // Un segundo dedo convierte el dibujo en gesto: el trazo a medias se
  // descarta (GoodNotes hace exactamente esto al pellizcar).
  if (activo && (activo.tipo === 'trazo' || activo.tipo === 'goma' || activo.tipo === 'lazo')
    && activo.esTactil) {
    clearTimeout(quietoTimer);
    activo = null;
    renderTodo();
  }
}

function iniciarGestoTactil() {
  const dedos = [...toques.values()];
  // t0, mov y maxDedos sobreviven a los cambios de dedos: el toque corto
  // se clasifica al final por el MÁXIMO de dedos que tocaron (2 = deshacer,
  // 3 = rehacer), sin importar el orden en que se levanten.
  const base = {
    t0: gesto?.t0 ?? performance.now(),
    mov: gesto?.mov ?? 0,
    maxDedos: Math.max(gesto?.maxDedos ?? 0, toques.size),
  };
  if (dedos.length === 1) {
    gesto = {
      ...base, tipo: 'pan',
      x0: dedos[0].x, y0: dedos[0].y, ox0: vista.ox, oy0: vista.oy,
    };
  } else if (dedos.length >= 2) {
    const [a, b] = dedos;
    gesto = {
      ...base, tipo: 'pinch',
      d0: Math.hypot(a.x - b.x, a.y - b.y) || 1,
      m0: { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 },
      k0: vista.k, ox0: vista.ox, oy0: vista.oy,
    };
  }
}

function moverGestoTactil() {
  if (!gesto) return;
  const dedos = [...toques.values()];
  if (gesto.tipo === 'pan' && dedos.length === 1) {
    const dx = dedos[0].x - gesto.x0, dy = dedos[0].y - gesto.y0;
    gesto.mov = Math.max(gesto.mov, Math.hypot(dx, dy));
    vista.ox = gesto.ox0 + dx;
    vista.oy = gesto.oy0 + dy;
    renderTodo();
  } else if (gesto.tipo === 'pinch' && dedos.length >= 2) {
    const [a, b] = dedos;
    const d = Math.hypot(a.x - b.x, a.y - b.y) || 1;
    const m = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
    gesto.mov = Math.max(
      gesto.mov,
      Math.abs(d - gesto.d0),
      Math.hypot(m.x - gesto.m0.x, m.y - gesto.m0.y)
    );
    const k = Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, gesto.k0 * (d / gesto.d0)));
    vista.k = k;
    vista.ox = m.x - ((gesto.m0.x - gesto.ox0) / gesto.k0) * k;
    vista.oy = m.y - ((gesto.m0.y - gesto.oy0) / gesto.k0) * k;
    renderTodo();
    chipZoom();
  }
}

function terminarGestoTactil(e) {
  if (!gesto || toques.size > 0) return;
  const duracion = performance.now() - gesto.t0;
  const fueTap = duracion < 280 && gesto.mov < 14;
  if (fueTap && gesto.maxDedos >= 2) {
    // Gestos de GoodNotes: toque de 2 dedos = deshacer; de 3 = rehacer
    if (gesto.maxDedos >= 3) hacerRehacer();
    else hacerDeshacer();
    toast(gesto.maxDedos >= 3 ? 'Rehacer' : 'Deshacer', 700);
  } else if (fueTap && gesto.maxDedos === 1 && penVisto) {
    // Doble toque del DEDO: alternar pluma↔goma (sustituto del doble
    // toque del pencil, que iPadOS no expone a las web apps)
    const ahora = performance.now();
    const pt = puntoPantalla(e);
    if (ultimoTap && ahora - ultimoTap.t < 350 &&
      Math.hypot(pt.x - ultimoTap.x, pt.y - ultimoTap.y) < 48) {
      elegirHerramienta(herramienta === 'goma' ? 'goma_prev' : 'goma');
      toast(herramienta === 'goma' ? 'Goma' : 'Pluma', 700);
      ultimoTap = null;
    } else {
      ultimoTap = { t: ahora, x: pt.x, y: pt.y };
    }
  }
  gesto = null;
}

/* ========================= Gestos del puntero ========================= */

function borrarEn(pt) {
  const pag = paginaActual();
  // El tamaño de la goma es visual (pantalla): se divide por el zoom
  const radio = ajustes.goma.grosor / vista.k;
  for (let i = pag.length - 1; i >= 0; i--) {
    const t = pag[i];
    const r2 = (radio + (t.m ? t.g * 3 : t.g)) ** 2;
    if (t.p.some(([x, y]) => distancia2(x, y, pt.x, pt.y) <= r2)) {
      pag.splice(i, 1);
      activo.borrados.push({ i, trazo: t });
      renderTodo();
    }
  }
}

function seleccionarConLazo(camino) {
  const pag = paginaActual();
  const indices = [];
  pag.forEach((t, i) => {
    let dentro = 0;
    let total = 0;
    for (let j = 0; j < t.p.length; j += MUESTREO_LAZO) {
      total += 1;
      if (dentroPoligono(t.p[j][0], t.p[j][1], camino)) dentro += 1;
    }
    if (total && dentro / total >= 0.6) indices.push(i);
  });
  seleccion = indices.length ? { indices, caja: cajaDe(indices) } : null;
}

function capturar(id) {
  try {
    canvas.setPointerCapture(id);
  } catch {
    /* puntero sintético o ya levantado: sin captura, el gesto sigue */
  }
}

function onPointerDown(e) {
  if (e.pointerType === 'pen' && !penVisto) {
    penVisto = true;
    if (!hintMostrado) {
      hintMostrado = true;
      toast('Dedo: desplaza · doble toque del dedo: pluma↔goma · 2 dedos: zoom (toque corto = deshacer)', 3600);
    }
  }

  if (e.pointerType === 'touch') {
    // Rechazo de palma: contactos anchos se ignoran por completo
    if ((e.width || 0) >= PALMA_ANCHO || (e.height || 0) >= PALMA_ANCHO) return;
    const pt = puntoPantalla(e);
    toques.set(e.pointerId, pt);
    capturar(e.pointerId);
    // El dedo es gesto (no tinta) si hay pencil conocido, si ya hay otro
    // dedo en el lienzo, o si hay un trazo de pen activo (palma chica).
    if (penVisto || toques.size > 1 || (activo && !activo.esTactil)) {
      e.preventDefault();
      abortarTrazoTactil();
      if (activo && !activo.esTactil) return; // pen dibujando: la palma no gesticula
      iniciarGestoTactil();
      return;
    }
    // Sin pencil a la vista: un dedo dibuja (modo mouse/tacto puro)
  }

  if (activo) return; // un solo puntero dibuja a la vez
  e.preventDefault();
  capturar(e.pointerId);
  const pt = punto(e);
  const esTactil = e.pointerType === 'touch';

  if (herramienta === 'lazo') {
    if (seleccion) {
      const c = seleccion.caja;
      if (pt.x >= c.x && pt.x <= c.x + c.w && pt.y >= c.y && pt.y <= c.y + c.h) {
        activo = { tipo: 'mover', id: e.pointerId, x0: pt.x, y0: pt.y, dx: 0, dy: 0, esTactil };
        return;
      }
      seleccion = null;
      renderTodo();
    }
    activo = { tipo: 'lazo', id: e.pointerId, camino: [pt], esTactil };
    return;
  }

  if (herramienta === 'goma') {
    activo = { tipo: 'goma', id: e.pointerId, borrados: [], esTactil };
    borrarEn(pt);
    return;
  }

  const aj = ajustes[herramienta] ?? ajustes.pluma;
  activo = {
    tipo: 'trazo',
    id: e.pointerId,
    esTactil,
    trazo: { c: aj.color, g: aj.grosor, p: [[pt.x, pt.y, presion(e)]] },
  };
  if (herramienta === 'marcador') activo.trazo.m = 1;
  clearTimeout(quietoTimer);
  quietoTimer = setTimeout(intentarFigura, QUIETO_MS);
}

function onPointerMove(e) {
  if (e.pointerType === 'touch' && toques.has(e.pointerId) && gesto) {
    toques.set(e.pointerId, puntoPantalla(e));
    moverGestoTactil();
    return;
  }
  if (!activo || e.pointerId !== activo.id) return;
  e.preventDefault();
  // getCoalescedEvents puede venir VACÍO (eventos sintéticos): caer a [e]
  const coalescidos = e.getCoalescedEvents?.() ?? [];
  const eventos = coalescidos.length ? coalescidos : [e];

  if (activo.tipo === 'trazo') {
    const esMarcador = !!activo.trazo.m;
    let dibujo = false;
    eventos.forEach((ev) => {
      const pt = punto(ev);
      const p = activo.trazo.p;
      const ultimo = p[p.length - 1];
      if (distancia2(ultimo[0], ultimo[1], pt.x, pt.y) < 1) return;
      p.push([pt.x, pt.y, presion(ev)]);
      dibujo = true;
      if (esMarcador) return; // se repinta entero abajo (alfa sin uniones)
      // Trazo en vivo: solo el último segmento (rápido); el suavizado
      // completo llega con el renderTodo del pointerup.
      const i = p.length - 1;
      ctx.strokeStyle = activo.trazo.c;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.lineWidth = ancho(activo.trazo.g, (p[i - 1][2] + p[i][2]) / 2);
      ctx.moveTo(p[i - 1][0], p[i - 1][1]);
      ctx.lineTo(p[i][0], p[i][1]);
      ctx.stroke();
    });
    if (dibujo) {
      // Dibuja-y-sostén: el reposo del pencil dispara la figura perfecta
      clearTimeout(quietoTimer);
      quietoTimer = setTimeout(intentarFigura, QUIETO_MS);
      if (esMarcador) {
        renderTodo();
        dibujarTrazo(activo.trazo);
      }
    }
    return;
  }

  const pt = punto(e);
  if (activo.tipo === 'goma') {
    borrarEn(pt);
  } else if (activo.tipo === 'lazo') {
    activo.camino.push(pt);
    renderTodo();
  } else if (activo.tipo === 'mover') {
    activo.dx = pt.x - activo.x0;
    activo.dy = pt.y - activo.y0;
    renderTodo();
  }
}

function onPointerUp(e) {
  if (e.pointerType === 'touch' && toques.has(e.pointerId)) {
    toques.delete(e.pointerId);
    if (gesto) {
      terminarGestoTactil(e);
      if (toques.size) iniciarGestoTactil(); // de pinch a pan sin saltos
      return;
    }
  }
  if (!activo || e.pointerId !== activo.id) return;
  clearTimeout(quietoTimer);
  const gestoDibujo = activo;

  if (gestoDibujo.tipo === 'muerto') {
    activo = null; // la figura perfecta ya se confirmó en intentarFigura()
    return;
  }

  if (gestoDibujo.tipo === 'trazo') {
    activo = null;
    const pag = paginaActual();
    pag.push(redondearTrazo(gestoDibujo.trazo));
    registrar({ tipo: 'anadir', pagina: tablero.pagina, indice: pag.length - 1, trazo: gestoDibujo.trazo });
    guardar();
    renderTodo();
  } else if (gestoDibujo.tipo === 'goma') {
    activo = null;
    if (gestoDibujo.borrados.length) {
      registrar({ tipo: 'borrar', pagina: tablero.pagina, items: gestoDibujo.borrados });
      guardar();
    }
  } else if (gestoDibujo.tipo === 'lazo') {
    activo = null;
    if (gestoDibujo.camino.length >= 3) seleccionarConLazo(gestoDibujo.camino);
    renderTodo();
  } else if (gestoDibujo.tipo === 'mover') {
    activo = null;
    if (gestoDibujo.dx || gestoDibujo.dy) {
      seleccion.indices.forEach((i) => {
        paginaActual()[i].p.forEach((q) => {
          q[0] += gestoDibujo.dx;
          q[1] += gestoDibujo.dy;
        });
      });
      seleccion.caja = cajaDe(seleccion.indices);
      registrar({
        tipo: 'mover',
        pagina: tablero.pagina,
        indices: [...seleccion.indices],
        dx: gestoDibujo.dx,
        dy: gestoDibujo.dy,
      });
      guardar();
    }
    renderTodo();
  }
  actualizarBarra();
}

/* ============================ Barra de UI ============================= */

let herramientaPrev = 'pluma'; // para alternar pluma/goma con doble toque

function elegirHerramienta(h) {
  if (h === 'goma_prev') h = herramientaPrev; // volver desde la goma
  if (h === 'goma' && herramienta !== 'goma') herramientaPrev = herramienta;
  herramienta = h;
  if (h !== 'lazo') {
    seleccion = null;
    if (tablero) renderTodo();
  }
  ['pluma', 'marcador', 'goma', 'lazo'].forEach((x) =>
    $(`btn-piz-${x}`).classList.toggle('activo', x === h)
  );
  canvas.dataset.herramienta = h;
  renderAjustesUI();
  actualizarBarra();
}

/** Los 3 puntos de grosor + las tintas, según la herramienta activa. */
function renderAjustesUI() {
  const cont = $('piz-grosores');
  cont.innerHTML = '';
  const lista = GROSORES[herramienta];
  cont.hidden = !lista;
  if (lista) {
    lista.forEach((g) => {
      const b = document.createElement('button');
      b.className = 'piz-grosor-preset' + (ajustes[herramienta].grosor === g ? ' activo' : '');
      b.title = 'Grosor';
      b.setAttribute('aria-label', `Grosor ${g}`);
      const d = document.createElement('span');
      const visual = Math.max(4, Math.min(18, herramienta === 'goma' ? g * 0.42 : g * 2.2));
      d.style.width = `${visual}px`;
      d.style.height = `${visual}px`;
      d.style.background = ajustes[herramienta].color ?? 'var(--texto)';
      b.appendChild(d);
      b.addEventListener('click', () => {
        ajustes[herramienta].grosor = g;
        guardarAjustes();
        renderAjustesUI();
      });
      cont.appendChild(b);
    });
  }
  const colores = $('piz-colores');
  const conColor = herramienta === 'pluma' || herramienta === 'marcador';
  colores.hidden = !conColor;
  if (conColor) {
    colores.querySelectorAll('.piz-color').forEach((b) => {
      b.classList.toggle('activo', b.dataset.color === ajustes[herramienta].color);
    });
  }
}

function actualizarBarra() {
  $('btn-piz-deshacer').disabled = !deshacer.length;
  $('btn-piz-rehacer').disabled = !rehacer.length;
  $('btn-piz-sel-borrar').hidden = !seleccion;
  $('btn-piz-sel-duplicar').hidden = !seleccion;
  if (tablero) {
    $('piz-pag-info').textContent = `${tablero.pagina + 1}/${tablero.paginas.length}`;
    $('btn-piz-pag-prev').disabled = tablero.pagina === 0;
    $('btn-piz-pag-next').disabled = tablero.pagina >= tablero.paginas.length - 1;
  }
}

function cambiarPagina(delta) {
  const destino = tablero.pagina + delta;
  if (destino < 0 || destino >= tablero.paginas.length) return;
  seleccion = null;
  tablero.pagina = destino;
  guardar();
  renderTodo();
  actualizarBarra();
}

function nuevaPagina() {
  seleccion = null;
  const indice = tablero.pagina + 1;
  tablero.paginas.splice(indice, 0, []);
  tablero.pagina = indice;
  registrar({ tipo: 'pagina', pagina: indice, indice });
  guardar();
  renderTodo();
  actualizarBarra();
}

let limpiarArmado = null;

function limpiarPagina() {
  const btn = $('btn-piz-limpiar');
  if (!limpiarArmado) {
    // Doble toque deliberado: el primero arma, el segundo limpia (y aun
    // así se puede deshacer).
    btn.classList.add('peligro-armado');
    btn.textContent = '¿limpiar?';
    limpiarArmado = setTimeout(() => desarmarLimpiar(), 2500);
    return;
  }
  desarmarLimpiar();
  const trazos = paginaActual();
  if (!trazos.length) return;
  registrar({ tipo: 'limpiar', pagina: tablero.pagina, trazos: [...trazos] });
  tablero.paginas[tablero.pagina] = [];
  seleccion = null;
  guardar();
  renderTodo();
}

function desarmarLimpiar() {
  clearTimeout(limpiarArmado);
  limpiarArmado = null;
  const btn = $('btn-piz-limpiar');
  btn.classList.remove('peligro-armado');
  btn.textContent = '⌫';
}

function borrarSeleccion() {
  if (!seleccion) return;
  const pag = paginaActual();
  const items = [...seleccion.indices]
    .sort((a, b) => b - a)
    .map((i) => ({ i, trazo: pag[i] }));
  items.forEach(({ i }) => pag.splice(i, 1));
  registrar({ tipo: 'borrar', pagina: tablero.pagina, items });
  seleccion = null;
  guardar();
  renderTodo();
  actualizarBarra();
}

function duplicarSeleccion() {
  if (!seleccion) return;
  const pag = paginaActual();
  const desplaza = 24 / vista.k;
  const copias = seleccion.indices.map((i) => {
    const t = structuredClone(pag[i]);
    t.p.forEach((q) => { q[0] += desplaza; q[1] += desplaza; });
    return t;
  });
  pag.push(...copias);
  registrar({ tipo: 'anadirVarios', pagina: tablero.pagina, trazos: copias });
  // La selección pasa a las copias (como GoodNotes al duplicar)
  seleccion = {
    indices: copias.map((_, j) => pag.length - copias.length + j),
    caja: null,
  };
  seleccion.caja = cajaDe(seleccion.indices);
  guardar();
  renderTodo();
  actualizarBarra();
}

/* ========================== Abrir y cerrar ============================ */

function abrir() {
  const contexto = proveedorContexto();
  clave = contexto.clave;
  $('pizarra-titulo').textContent = contexto.titulo;
  const guardado = load('pizarras')[clave];
  tablero = guardado
    ? structuredClone({ paginas: guardado.paginas, pagina: guardado.pagina ?? 0 })
    : { paginas: [[]], pagina: 0 };
  if (tablero.pagina >= tablero.paginas.length) tablero.pagina = 0;
  deshacer = [];
  rehacer = [];
  seleccion = null;
  activo = null;
  gesto = null;
  toques.clear();
  vista = { k: 1, ox: 0, oy: 0 };
  // El botón del mentor SOLO existe con cuenta de Claude activa (§0.7/§4)
  $('btn-piz-mentor').hidden = !mentorCfg.disponible?.();
  $('pizarra-overlay').hidden = false;
  document.body.classList.add('sin-scroll');
  redimensionar();
  renderTodo();
  actualizarBarra();
  renderAjustesUI();
}

function cerrar() {
  persistir();
  $('pizarra-overlay').hidden = true;
  document.body.classList.remove('sin-scroll');
  tablero = null;
  clave = null;
}

function evaluarConMentor() {
  if (!mentorCfg.evaluar) return;
  const imagen = exportarPaginaJPEG();
  if (!imagen) {
    toast('La página está vacía — escribe tu proceso primero');
    return;
  }
  persistir();
  cerrar(); // el panel del mentor vive debajo del overlay de la pizarra
  mentorCfg.evaluar(imagen);
}

/* ============================== API ================================== */

/** app.js entrega aquí cómo saber el contexto actual (problema/unidad/examen). */
export function setContexto(fn) {
  proveedorContexto = fn;
}

/**
 * Conexión con el mentor socrático (§4.4): `disponible()` decide si el
 * botón existe (cuenta de Claude activa) y `evaluar(jpegDataUrl)` recibe
 * la página exportada para enviarla al chat.
 */
export function configurarMentor(cfg) {
  mentorCfg = { ...mentorCfg, ...cfg };
}

/** El botón flotante existe solo en Entrenamiento y Estudio. */
export function actualizarVisibilidad(vistaApp) {
  $('pizarra-flotante').hidden = !(vistaApp === 'sesion' || vistaApp === 'estudio');
}

export function init() {
  canvas = $('pizarra-canvas');
  ctx = canvas.getContext('2d');

  // Memoria por herramienta persistida (clave meta _ajustes, no es tablero)
  const previos = load('pizarras')._ajustes;
  if (previos) {
    ['pluma', 'marcador', 'goma'].forEach((h) => {
      if (previos[h]) ajustes[h] = { ...ajustes[h], ...previos[h] };
    });
  }

  $('pizarra-burbuja').addEventListener('click', abrir);
  $('btn-pizarra-cerrar').addEventListener('click', cerrar);
  $('btn-piz-mentor').addEventListener('click', evaluarConMentor);

  $('btn-piz-pluma').addEventListener('click', () => elegirHerramienta('pluma'));
  $('btn-piz-marcador').addEventListener('click', () => elegirHerramienta('marcador'));
  $('btn-piz-goma').addEventListener('click', () => elegirHerramienta('goma'));
  $('btn-piz-lazo').addEventListener('click', () => elegirHerramienta('lazo'));
  $('btn-piz-deshacer').addEventListener('click', hacerDeshacer);
  $('btn-piz-rehacer').addEventListener('click', hacerRehacer);
  $('btn-piz-limpiar').addEventListener('click', limpiarPagina);
  $('btn-piz-sel-borrar').addEventListener('click', borrarSeleccion);
  $('btn-piz-sel-duplicar').addEventListener('click', duplicarSeleccion);
  $('btn-piz-pag-prev').addEventListener('click', () => cambiarPagina(-1));
  $('btn-piz-pag-next').addEventListener('click', () => cambiarPagina(1));
  $('btn-piz-pag-nueva').addEventListener('click', nuevaPagina);

  const colores = $('piz-colores');
  COLORES.forEach((c, i) => {
    const b = document.createElement('button');
    b.className = 'piz-color' + (i === 0 ? ' activo' : '');
    b.style.background = c;
    b.dataset.color = c;
    b.title = 'Color de tinta';
    b.setAttribute('aria-label', `Tinta ${i + 1}`);
    b.addEventListener('click', () => {
      if (ajustes[herramienta]?.color === undefined) return;
      ajustes[herramienta].color = c;
      guardarAjustes();
      renderAjustesUI();
    });
    colores.appendChild(b);
  });

  canvas.addEventListener('pointerdown', onPointerDown);
  canvas.addEventListener('pointermove', onPointerMove);
  canvas.addEventListener('pointerup', onPointerUp);
  canvas.addEventListener('pointercancel', onPointerUp);
  canvas.addEventListener('contextmenu', (e) => e.preventDefault());

  // Escritorio: rueda desplaza; ⌘/Ctrl + rueda hace zoom al cursor
  canvas.addEventListener('wheel', (e) => {
    if (!tablero) return;
    e.preventDefault();
    if (e.ctrlKey || e.metaKey) {
      const pt = puntoPantalla(e);
      fijarZoom(vista.k * Math.exp(-e.deltaY * 0.01), pt.x, pt.y);
    } else {
      vista.ox -= e.deltaX;
      vista.oy -= e.deltaY;
      renderTodo();
    }
  }, { passive: false });

  new ResizeObserver(redimensionar).observe($('pizarra-lienzo-wrap'));

  // Atajos mientras la pizarra está abierta
  document.addEventListener('keydown', (e) => {
    if ($('pizarra-overlay').hidden) return;
    if (e.key === 'Escape') cerrar();
    const mod = e.metaKey || e.ctrlKey;
    if (mod && e.key === 'z' && !e.shiftKey) {
      e.preventDefault();
      hacerDeshacer();
    } else if (mod && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
      e.preventDefault();
      hacerRehacer();
    }
  });

  // Si la pestaña se va con la pizarra abierta, el trazo no se pierde
  window.addEventListener('pagehide', () => {
    if (!$('pizarra-overlay').hidden) persistir();
  });

  elegirHerramienta('pluma');
}
