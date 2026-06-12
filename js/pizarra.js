/**
 * pizarra.js — Pizarra de trabajo a mano alzada (pedido del usuario,
 * 2026-06-11): escribir con el Apple Pencil (o el dedo, o el mouse)
 * directamente en la app para forcejear los problemas, sin papel ni
 * apps externas. Estilo cuaderno tipo GoodNotes:
 *
 *  - Pluma con grosor configurable, sensible a la presión del pencil.
 *  - Resaltador: tinta translúcida de ancho constante, para marcar encima.
 *  - Goma (borra trazos completos, como la goma de trazo de GoodNotes).
 *  - Lazo: rodear trazos para moverlos o borrarlos en bloque.
 *  - Deshacer/rehacer, varias páginas por pizarra.
 *  - Rechazo de palma: en cuanto se detecta un pencil, el tacto de la
 *    mano deja de dibujar (los botones siguen funcionando al tacto).
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

let proveedorContexto = () => ({ clave: 'libre', titulo: 'Pizarra' });

let canvas = null;
let ctx = null;

let clave = null;          // contexto de la pizarra abierta
let tablero = null;        // { paginas: [[trazo,…]], pagina }
let herramienta = 'pluma'; // 'pluma' | 'marcador' | 'goma' | 'lazo'
let color = COLORES[0];
let grosor = 3;

let activo = null;         // gesto de puntero en curso
let seleccion = null;      // { indices: number[], caja: {x,y,w,h} }
let penVisto = false;      // rechazo de palma: tras ver un pencil, el dedo no dibuja
let deshacer = [];
let rehacer = [];
let guardarTimeout = null;

/* ============================ Utilidades ============================== */

function paginaActual() {
  return tablero.paginas[tablero.pagina];
}

function punto(e) {
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

/* ============================== Render ================================ */

function dibujarTrazo(trazo, dx = 0, dy = 0) {
  const p = trazo.p;
  // Resaltador (trazo.m): translúcido, ancho constante, en UN solo path —
  // pintado por segmentos, las uniones doblarían el alfa y se oscurecerían.
  if (trazo.m) {
    ctx.save();
    ctx.globalAlpha = 0.38;
    ctx.strokeStyle = trazo.c;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = trazo.g * 3;
    ctx.beginPath();
    p.forEach(([x, y], i) => (i ? ctx.lineTo(x + dx, y + dy) : ctx.moveTo(x + dx, y + dy)));
    if (p.length === 1) ctx.lineTo(p[0][0] + dx + 0.1, p[0][1] + dy);
    ctx.stroke();
    ctx.restore();
    return;
  }
  ctx.strokeStyle = trazo.c;
  ctx.fillStyle = trazo.c;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  if (p.length === 1) {
    ctx.beginPath();
    ctx.arc(p[0][0] + dx, p[0][1] + dy, ancho(trazo.g, p[0][2]) / 2, 0, Math.PI * 2);
    ctx.fill();
    return;
  }
  // Suavizado por puntos medios: cada segmento es una curva corta con su
  // propio grosor (así la presión del pencil modula el trazo, como tinta).
  for (let i = 1; i < p.length; i++) {
    const [xa, ya, pa] = p[i - 1];
    const [xb, yb, pb] = p[i];
    ctx.beginPath();
    ctx.lineWidth = ancho(trazo.g, (pa + pb) / 2);
    const m0x = i > 1 ? (xa + p[i - 2][0]) / 2 : xa;
    const m0y = i > 1 ? (ya + p[i - 2][1]) / 2 : ya;
    const m1x = (xa + xb) / 2;
    const m1y = (ya + yb) / 2;
    ctx.moveTo(m0x + dx, m0y + dy);
    ctx.quadraticCurveTo(xa + dx, ya + dy, m1x + dx, m1y + dy);
    if (i === p.length - 1) ctx.lineTo(xb + dx, yb + dy);
    ctx.stroke();
  }
}

function renderTodo() {
  const r = canvas.getBoundingClientRect();
  ctx.clearRect(0, 0, r.width, r.height);
  // Mientras se arrastra una selección, los trazos seleccionados se pintan
  // desplazados (el movimiento se vuelve permanente en el pointerup).
  const ox = activo?.tipo === 'mover' ? activo.dx : 0;
  const oy = activo?.tipo === 'mover' ? activo.dy : 0;
  paginaActual().forEach((trazo, i) => {
    const sel = seleccion?.indices.includes(i);
    dibujarTrazo(trazo, sel ? ox : 0, sel ? oy : 0);
  });
  if (seleccion) {
    const c = seleccion.caja;
    ctx.save();
    ctx.strokeStyle = '#8d96f7';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([6, 5]);
    ctx.strokeRect(c.x + ox, c.y + oy, c.w, c.h);
    ctx.restore();
  }
  if (activo?.tipo === 'lazo' && activo.camino.length > 1) {
    ctx.save();
    ctx.strokeStyle = '#8d96f7';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([6, 5]);
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
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
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
      const claves = Object.keys(t);
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

/* ========================= Gestos del puntero ========================= */

function borrarEn(pt) {
  const pag = paginaActual();
  const radio = Math.max(10, grosor * 3);
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

function onPointerDown(e) {
  if (e.pointerType === 'pen') penVisto = true;
  if (e.pointerType === 'touch' && penVisto) return; // palma apoyada: ignorar
  if (activo) return; // un solo puntero dibuja a la vez
  e.preventDefault();
  canvas.setPointerCapture(e.pointerId);
  const pt = punto(e);

  if (herramienta === 'lazo') {
    if (seleccion) {
      const c = seleccion.caja;
      if (pt.x >= c.x && pt.x <= c.x + c.w && pt.y >= c.y && pt.y <= c.y + c.h) {
        activo = { tipo: 'mover', id: e.pointerId, x0: pt.x, y0: pt.y, dx: 0, dy: 0 };
        return;
      }
      seleccion = null;
      renderTodo();
    }
    activo = { tipo: 'lazo', id: e.pointerId, camino: [pt] };
    return;
  }

  if (herramienta === 'goma') {
    activo = { tipo: 'goma', id: e.pointerId, borrados: [] };
    borrarEn(pt);
    return;
  }

  activo = {
    tipo: 'trazo',
    id: e.pointerId,
    trazo: { c: color, g: grosor, p: [[pt.x, pt.y, presion(e)]] },
  };
  if (herramienta === 'marcador') activo.trazo.m = 1;
}

function onPointerMove(e) {
  if (!activo || e.pointerId !== activo.id) return;
  e.preventDefault();
  const eventos = e.getCoalescedEvents?.() ?? [e];

  if (activo.tipo === 'trazo') {
    const esMarcador = !!activo.trazo.m;
    eventos.forEach((ev) => {
      const pt = punto(ev);
      const p = activo.trazo.p;
      const ultimo = p[p.length - 1];
      if (distancia2(ultimo[0], ultimo[1], pt.x, pt.y) < 1) return;
      p.push([pt.x, pt.y, presion(ev)]);
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
    if (esMarcador) {
      renderTodo();
      dibujarTrazo(activo.trazo);
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
  if (!activo || e.pointerId !== activo.id) return;
  const gesto = activo;

  if (gesto.tipo === 'trazo') {
    activo = null;
    const pag = paginaActual();
    pag.push(redondearTrazo(gesto.trazo));
    registrar({ tipo: 'anadir', pagina: tablero.pagina, indice: pag.length - 1, trazo: gesto.trazo });
    guardar();
    renderTodo();
  } else if (gesto.tipo === 'goma') {
    activo = null;
    if (gesto.borrados.length) {
      registrar({ tipo: 'borrar', pagina: tablero.pagina, items: gesto.borrados });
      guardar();
    }
  } else if (gesto.tipo === 'lazo') {
    activo = null;
    if (gesto.camino.length >= 3) seleccionarConLazo(gesto.camino);
    renderTodo();
  } else if (gesto.tipo === 'mover') {
    activo = null;
    if (gesto.dx || gesto.dy) {
      seleccion.indices.forEach((i) => {
        paginaActual()[i].p.forEach((q) => {
          q[0] += gesto.dx;
          q[1] += gesto.dy;
        });
      });
      seleccion.caja = cajaDe(seleccion.indices);
      registrar({
        tipo: 'mover',
        pagina: tablero.pagina,
        indices: [...seleccion.indices],
        dx: gesto.dx,
        dy: gesto.dy,
      });
      guardar();
    }
    renderTodo();
  }
  actualizarBarra();
}

/* ============================ Barra de UI ============================= */

function elegirHerramienta(h) {
  herramienta = h;
  if (h !== 'lazo') {
    seleccion = null;
    if (tablero) renderTodo();
  }
  ['pluma', 'marcador', 'goma', 'lazo'].forEach((x) =>
    $(`btn-piz-${x}`).classList.toggle('activo', x === h)
  );
  canvas.dataset.herramienta = h;
  actualizarBarra();
}

function actualizarBarra() {
  $('btn-piz-deshacer').disabled = !deshacer.length;
  $('btn-piz-rehacer').disabled = !rehacer.length;
  $('btn-piz-sel-borrar').hidden = !seleccion;
  if (tablero) {
    $('piz-pag-info').textContent = `${tablero.pagina + 1}/${tablero.paginas.length}`;
    $('btn-piz-pag-prev').disabled = tablero.pagina === 0;
    $('btn-piz-pag-next').disabled = tablero.pagina >= tablero.paginas.length - 1;
  }
  const vista = $('piz-grosor-vista');
  const d = Math.max(3, Math.min(16, grosor * 1.2));
  vista.style.width = `${d}px`;
  vista.style.height = `${d}px`;
  vista.style.background = color;
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
  $('pizarra-overlay').hidden = false;
  document.body.classList.add('sin-scroll');
  redimensionar();
  renderTodo();
  actualizarBarra();
}

function cerrar() {
  persistir();
  $('pizarra-overlay').hidden = true;
  document.body.classList.remove('sin-scroll');
  tablero = null;
  clave = null;
}

/* ============================== API ================================== */

/** app.js entrega aquí cómo saber el contexto actual (problema/unidad/examen). */
export function setContexto(fn) {
  proveedorContexto = fn;
}

/** El botón flotante existe solo en Entrenamiento y Estudio. */
export function actualizarVisibilidad(vista) {
  $('pizarra-flotante').hidden = !(vista === 'sesion' || vista === 'estudio');
}

export function init() {
  canvas = $('pizarra-canvas');
  ctx = canvas.getContext('2d');

  $('pizarra-burbuja').addEventListener('click', abrir);
  $('btn-pizarra-cerrar').addEventListener('click', cerrar);

  $('btn-piz-pluma').addEventListener('click', () => elegirHerramienta('pluma'));
  $('btn-piz-marcador').addEventListener('click', () => elegirHerramienta('marcador'));
  $('btn-piz-goma').addEventListener('click', () => elegirHerramienta('goma'));
  $('btn-piz-lazo').addEventListener('click', () => elegirHerramienta('lazo'));
  $('btn-piz-deshacer').addEventListener('click', hacerDeshacer);
  $('btn-piz-rehacer').addEventListener('click', hacerRehacer);
  $('btn-piz-limpiar').addEventListener('click', limpiarPagina);
  $('btn-piz-sel-borrar').addEventListener('click', borrarSeleccion);
  $('btn-piz-pag-prev').addEventListener('click', () => cambiarPagina(-1));
  $('btn-piz-pag-next').addEventListener('click', () => cambiarPagina(1));
  $('btn-piz-pag-nueva').addEventListener('click', nuevaPagina);

  $('piz-grosor').addEventListener('input', (e) => {
    grosor = Number(e.target.value);
    actualizarBarra();
  });

  const colores = $('piz-colores');
  COLORES.forEach((c, i) => {
    const b = document.createElement('button');
    b.className = 'piz-color' + (i === 0 ? ' activo' : '');
    b.style.background = c;
    b.title = 'Color de tinta';
    b.setAttribute('aria-label', `Tinta ${i + 1}`);
    b.addEventListener('click', () => {
      color = c;
      colores.querySelectorAll('.piz-color').forEach((x) => x.classList.remove('activo'));
      b.classList.add('activo');
      actualizarBarra();
    });
    colores.appendChild(b);
  });

  canvas.addEventListener('pointerdown', onPointerDown);
  canvas.addEventListener('pointermove', onPointerMove);
  canvas.addEventListener('pointerup', onPointerUp);
  canvas.addEventListener('pointercancel', onPointerUp);
  canvas.addEventListener('contextmenu', (e) => e.preventDefault());

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
