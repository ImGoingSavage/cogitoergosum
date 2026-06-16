/**
 * study.js — Modo Estudio: el roadmap de Definitivo.pdf dentro de la app.
 *
 * Camino 2 de la app (independiente del entrenamiento diario, HANDOFF §3.11):
 *  - Lectura DIRIGIDA: la app dice qué leer y cuánto (puntero + dosis);
 *    la lectura ocurre en el libro, nunca aquí (anti-Brilliant).
 *  - Al volver, evaluación por retrieval de generación: el usuario escribe
 *    su respuesta ANTES de ver la esperada y se autoevalúa.
 *  - Las ideas clave (destilado) se muestran SOLO después del quiz.
 *  - Examen de bloque = "examen del motor" del PDF §8b: predicción de
 *    jugada → forcejeo → disparador correcto; acumulativo con interleaving
 *    de todos los bloques avanzados.
 *  - Racha de estudio SEPARADA de la de entrenamiento (no se cruzan) y
 *    visible en el header en todo momento.
 *
 * Contenido en data/study.json; progreso en LocalStorage (cps_estudio).
 * El módulo funciona completo sin IA.
 */

import { load, update, hoy, encolarEvento } from './storage.js';
import * as Badges from './badges.js';
import { renderMarkdown, renderInline } from './markdown.js';

const $ = (id) => document.getElementById(id);

const MIN_RESPUESTA_QUIZ = 40; // forcejeo mínimo antes de ver la respuesta
const DEFAULT_CLUSTER_EXAM_SIZE = 25; // preguntas del examen final de cluster

const NOMBRES_TIPO = {
  quiz: 'Pregunta de recuperación',
  acertijo: 'Acertijo',
  'encuentra-error': 'Encuentra el error',
  disparador: 'Quiz de disparador',
};

let datos = null; // contenido de data/study.json (null si no cargó)

/** Fisher-Yates en sitio: devuelve una copia barajada del array. */
function barajar(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Todas las preguntas de banco de las unidades fase-7 de un cluster. */
function getClusterQuestionPool(clusterId) {
  const c = taxonomia.find((x) => x.id === clusterId);
  return (c?.unidades ?? [])
    .map(unidad)
    .filter((u) => u && u.bloque === 'fase-7')
    .flatMap((u) => u.banco ?? []);
}

// Simulación de entrevista (Nivel E), organizada sobre la TAXONOMÍA semántica
// de la Fase 7 (auditoria.md Fase 3). El contenido vive en data/entrevista/
// (artefacto paralelo a data/teoria/, sin tocar el esquema de study.json):
// _taxonomia.json define los clusters (rondas de entrevista) y sus unidades;
// cada cluster.sim apunta a su guion cluster-<id>.json. Cada ronda se simula
// por área, no por unidad suelta.
let taxonomia = []; // [{ id, titulo, track, descripcion, sim, unidades[] }]
const simClusterCache = {}; // clusterId → objeto del guion (null si no cargó)

/* ============================ Arranque ================================ */

export async function init() {
  try {
    const res = await fetch('data/study.json');
    datos = await res.json();
  } catch {
    datos = null;
  }
  try {
    const r = await fetch('data/entrevista/_taxonomia.json');
    taxonomia = r.ok ? (await r.json()).clusters ?? [] : [];
  } catch {
    taxonomia = [];
  }
  actualizarRachaEstudio();
  actualizarHeaderRachas();
}

export function disponible() {
  return Boolean(datos?.bloques?.length);
}

/** Bloques del syllabus (para los sellos: lector disciplinado, etc.). */
export function bloques() {
  return datos?.bloques ?? [];
}

/* ======================= Racha de estudio ============================= */

function ayerISO() {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${mm}-${dd}`;
}

/**
 * Rompe la racha de estudio si la última sesión no fue ni ayer ni hoy.
 * Romperla nunca borra el logro (§2.2): la mejor racha queda guardada.
 */
export function actualizarRachaEstudio() {
  update('estudio', (e) => {
    if (
      e.ultimaSesionEstudio &&
      e.ultimaSesionEstudio !== hoy() &&
      e.ultimaSesionEstudio !== ayerISO()
    ) {
      e.mejorRachaEstudio = Math.max(e.mejorRachaEstudio ?? 0, e.rachaEstudio);
      e.rachaEstudio = 0;
    }
    return e;
  });
}

/** Completar una unidad o un examen cuenta el día (una sola vez). */
function marcarDiaEstudio() {
  update('estudio', (e) => {
    if (e.ultimaSesionEstudio !== hoy()) {
      e.rachaEstudio += 1;
      e.ultimaSesionEstudio = hoy();
      e.mejorRachaEstudio = Math.max(e.mejorRachaEstudio ?? 0, e.rachaEstudio);
    }
    return e;
  });
  actualizarHeaderRachas();
}

/**
 * Rachas siempre visibles (pedido explícito del usuario): el header las
 * muestra en todo momento. La de práctica vive en perfil.racha; la de
 * estudio aquí. app.js también llama esto al cerrar sesiones del camino 1.
 */
export function actualizarHeaderRachas() {
  const el = $('header-rachas');
  if (!el) return;
  const practica = load('perfil').racha;
  const estudio = load('estudio').rachaEstudio;
  el.innerHTML = '';
  const mk = (titulo, valor, simbolo) => {
    const span = document.createElement('span');
    span.className = 'racha-chip';
    span.title = `${titulo}: ${valor} día(s) consecutivos`;
    span.textContent = `${simbolo} ${valor}`;
    return span;
  };
  el.append(mk('Racha de entrenamiento', practica, '🔥'), mk('Racha de estudio', estudio, '📘'));
}

/* ===================== Estado de bloques/unidades ===================== */

function unidad(id) {
  return datos.unidades.find((u) => u.id === id) ?? null;
}

function unidadesDe(bloque) {
  return bloque.unidades.map(unidad).filter(Boolean);
}

function unidadCompletada(id) {
  return Boolean(load('estudio').unidadesCompletadas[id]);
}

function bloqueAprobado(id) {
  return Boolean(load('estudio').examenes[id]?.aprobado);
}

function indiceBloqueActual() {
  const i = datos.bloques.findIndex((b) => !bloqueAprobado(b.id));
  return i === -1 ? datos.bloques.length - 1 : i;
}

export function bloqueActual() {
  return datos ? datos.bloques[indiceBloqueActual()] : null;
}

/** Candado de orden eliminado (2026-06-12): toda unidad es accesible.
 *  Se conserva la función como punto único por si vuelve un modo guiado. */
function unidadDisponible() {
  return true;
}

function bloqueUnidadesCompletas(bloque) {
  return unidadesDe(bloque).every((u) => unidadCompletada(u.id));
}

/** Contexto de entrevista para el Mentor: no-null solo cuando hay actividad de fase-7. */
export function contextoEntrevista() {
  if (!disponible()) return null;
  const ex = load('estudio').examenEnCurso;
  if (ex && ex.bloqueId === 'fase-7') {
    const bloque = datos.bloques.find((b) => b.id === 'fase-7');
    const item = (bloque?.examen?.items ?? []).find((it) => it.id === ex.itemIds[ex.indice]);
    // Solo entrevistador cuando el ítem ES de arena (tiene ruta); los ítems
    // acumulados de fases 0-6 no tienen metadata.ruta y no invocan ese modo.
    if (!item?.metadata?.ruta) return null;
    return { ruta: item.metadata.ruta, examen: true, enunciado: item?.enunciado ?? '' };
  }
  const panel = document.getElementById('estudio-unidad');
  if (panel && !panel.hidden && panel.dataset.unidad) {
    const u = unidad(panel.dataset.unidad);
    if (u?.bloque === 'fase-7') return { ruta: u.metadata?.ruta ?? 'general', titulo: u.titulo };
  }
  return null;
}

/** Resumen para el Dashboard (camino 2). */
export function progresoResumen() {
  if (!disponible()) return null;
  const b = bloqueActual();
  const us = unidadesDe(b);
  const hechas = us.filter((u) => unidadCompletada(u.id)).length;
  const examen = load('estudio').examenes[b.id];
  return {
    bloque: b.titulo,
    unidadesHechas: hechas,
    unidadesTotal: us.length,
    examenAprobado: Boolean(examen?.aprobado),
    examenIntentos: examen?.intentos ?? 0,
    racha: load('estudio').rachaEstudio,
  };
}

/* ========================= Navegación de bloques ========================= */

let bloqueVisible = null;

function bloqueVisibleObj() {
  return bloqueVisible ?? bloqueActual();
}

/* ========================= Render: el camino ========================== */

export function renderizar() {
  if (!disponible()) {
    $('estudio-bloque-titulo').textContent = 'No se pudo cargar data/study.json.';
    $('estudio-unidades').innerHTML = '';
    return;
  }

  const e = load('estudio');
  const b = bloqueVisibleObj();
  $('estudio-bloque-titulo').textContent = b.titulo;
  $('estudio-bloque-meta').textContent = b.meta ?? '';
  const sel = $('estudio-bloque-selector');
  if (sel) {
    sel.innerHTML = '';
    datos.bloques.forEach((blq) => {
      const opt = document.createElement('option');
      opt.value = blq.id;
      opt.textContent = `${bloqueAprobado(blq.id) ? '✓ ' : ''}${blq.titulo}`;
      sel.appendChild(opt);
    });
    sel.value = b.id;
  }

  // Lista de unidades del bloque con su estado. En el bloque Arena (fase-7) la
  // lista plana de 118 lecciones se agrupa bajo las 8 categorías de la taxonomía
  // (cada una colapsable, con sus unidades en orden didáctico + su simulación de
  // entrevista). Las demás fases conservan la lista plana directa.
  const ul = $('estudio-unidades');
  ul.innerHTML = '';
  if (b.id === 'fase-7' && taxonomia.length > 0) {
    ul.classList.add('estudio-clusters');
    renderClustersFase7(ul, b);
  } else {
    ul.classList.remove('estudio-clusters');
    unidadesDe(b).forEach((u) => ul.appendChild(crearUnidadItem(u, b)));
  }

  // Estado del examen del bloque
  const listo = bloqueUnidadesCompletas(b);
  const aprobado = bloqueAprobado(b.id);
  $('estudio-examen-estado').textContent = aprobado
    ? 'Examen aprobado — el siguiente bloque está abierto.'
    : listo
      ? 'Todas las unidades completas: puedes presentar el examen del bloque.'
      : 'El examen se abre al completar todas las unidades del bloque.';
  $('btn-examen-iniciar').hidden = aprobado || !listo;
  $('btn-examen-iniciar').textContent = e.examenes[b.id]?.intentos
    ? 'Reintentar examen del bloque'
    : 'Presentar examen del bloque';

  // Paneles: retomar lo que estaba en curso
  $('estudio-unidad').hidden = true;
  $('estudio-examen').hidden = true;
  const panelCluster = $('estudio-examen-cluster');
  if (panelCluster) panelCluster.hidden = true;
  if (e.examenClusterEnCurso) renderExamenCluster();
  else if (e.examenEnCurso?.bloqueId === b.id) renderExamen();
  else if (e.quizEnCurso) abrirUnidad(e.quizEnCurso.unidadId);

  actualizarHeaderRachas();
}

/* ================== Lección integrada (teoría en la app) =============== */

/**
 * Teoría completa de cada unidad, redactada para la app (data/teoria/*.md)
 * y legible aquí mismo: estudiable sin el libro físico (pedido 2026-06-11).
 * El puntero al libro se conserva como referencia para profundizar.
 */
const leccionesCache = {}; // unidadId → HTML listo (null si no se pudo cargar)

async function alternarLeccion(u) {
  const btn = $('btn-unidad-leccion');
  const cont = $('unidad-leccion');
  if (!cont.hidden) {
    cont.hidden = true;
    btn.textContent = '📖 Leer la lección aquí';
    return;
  }
  if (!(u.id in leccionesCache)) {
    btn.disabled = true;
    try {
      const res = await fetch(`data/teoria/${u.id}.md`);
      leccionesCache[u.id] = res.ok ? renderMarkdown(await res.text()) : null;
    } catch {
      leccionesCache[u.id] = null;
    }
    btn.disabled = false;
  }
  cont.innerHTML =
    leccionesCache[u.id] ??
    '<p class="leccion-error">La lección no está disponible ahora mismo — revisa la conexión e inténtalo de nuevo (una vez cargada queda guardada para leer sin red).</p>';
  cont.hidden = false;
  btn.textContent = 'Cerrar la lección';
  cablearEnlacesLeccion(cont);
}

// Hace navegables los enlaces [[arena-xxx]] de una lección ya renderizada:
// pone el título real de la unidad (cuando el enlace no traía etiqueta propia),
// marca los rotos y abre la unidad destino al hacer click.
function cablearEnlacesLeccion(cont) {
  cont.querySelectorAll('.enlace-unidad').forEach((el) => {
    const id = el.dataset.unidad;
    const u = unidad(id);
    if (!u) {
      el.classList.add('enlace-roto');
      el.removeAttribute('role');
      el.removeAttribute('tabindex');
      return;
    }
    if (el.dataset.auto) el.textContent = u.titulo;
    el.addEventListener('click', () => navegarAUnidad(id));
    el.addEventListener('keydown', (ev) => {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        navegarAUnidad(id);
      }
    });
  });
}

/* ===================== Simulación de entrevista (Nivel E) ============= */

const ETIQUETA_TRACK = {
  quant: 'quant',
  maang: 'maang',
  health: 'health ai',
  ds: 'ciencia de datos',
  conductual: 'conductual',
};

// Mapea el track de un cluster a la clase .ruta-* del chip (mismo color que la
// ruta de las unidades, para que categoría y unidades se lean como una familia).
function rutaDeTrack(track) {
  return track === 'health' ? 'health-ai-rwe' : track === 'ds' ? 'ciencia-datos' : track;
}

// Construye el <li> de una unidad (lección): botón con estado, título, chip de
// ruta y libro; al click abre el panel de unidad. Extraído para reutilizarlo en
// la lista plana (fases 0-6) y dentro de los acordeones de la taxonomía (fase-7).
const ETIQUETA_RUTA = {
  quant: 'quant',
  maang: 'maang',
  'health-ai-rwe': 'health ai',
  'ml-systems': 'ml systems',
  'ciencia-datos': 'ciencia de datos',
  conductual: 'conductual',
};

function crearUnidadItem(u, b) {
  const li = document.createElement('li');
  li.className = 'unidad-item';
  const hecha = unidadCompletada(u.id);
  const abierta = unidadDisponible(b, u);
  const estado = hecha ? '✓' : abierta ? '▸' : '🔒';
  li.classList.add(hecha ? 'hecha' : abierta ? 'abierta' : 'bloqueada');

  const btn = document.createElement('button');
  btn.className = 'unidad-boton';
  btn.disabled = !hecha && !abierta;
  const rutaLabel = u.metadata?.ruta
    ? `<span class="ruta-chip ruta-${u.metadata.ruta}">${ETIQUETA_RUTA[u.metadata.ruta] ?? u.metadata.ruta}</span>`
    : '';
  btn.innerHTML = `<span class="unidad-estado">${estado}</span><span class="unidad-nombre"></span>${rutaLabel}<span class="unidad-libro"></span>`;
  btn.querySelector('.unidad-nombre').textContent = u.titulo;
  btn.querySelector('.unidad-libro').textContent = u.libro;
  btn.addEventListener('click', () => abrirUnidad(u.id));
  li.appendChild(btn);
  return li;
}

/* ============ Acordeones de la taxonomía (vista del bloque Arena) ========= */

// Qué categorías quedan desplegadas — en memoria, para conservar el estado entre
// re-renders de la sesión (p. ej. al cerrar una unidad) sin tocar el esquema de
// almacenamiento. Vista limpia por defecto: todas colapsadas al cargar.
const clustersExpandidos = new Set();

// Pinta las 118 lecciones de fase-7 agrupadas en las 8 categorías de la taxonomía:
// cada una es un acordeón (categoría → al desplegar muestra sus unidades en orden
// didáctico + el botón para simular su ronda de entrevista). Una unidad de fase-7
// que no estuviera en ninguna categoría se recoge en un grupo "Otras unidades"
// para no perderla nunca.
function renderClustersFase7(container, b) {
  const colocadas = new Set();
  taxonomia.forEach((c) => {
    const unidades = (c.unidades ?? []).map(unidad).filter((u) => u && u.bloque === b.id);
    unidades.forEach((u) => colocadas.add(u.id));
    container.appendChild(crearClusterAcordeon(c, unidades, b));
  });

  const sueltas = unidadesDe(b).filter((u) => !colocadas.has(u.id));
  if (sueltas.length) {
    container.appendChild(
      crearClusterAcordeon(
        {
          id: '__otras',
          titulo: 'Otras unidades',
          descripcion: 'Unidades del bloque aún sin categoría en la taxonomía.',
        },
        sueltas,
        b
      )
    );
  }
}

// Un acordeón = cabecera (chevron + título + chip de track + progreso) y cuerpo
// colapsable (descripción, secuencia didáctica, lista de unidades y simulación).
function crearClusterAcordeon(c, unidades, b) {
  const li = document.createElement('li');
  li.className = 'cluster-acordeon';

  const hechas = unidades.filter((u) => unidadCompletada(u.id)).length;
  const total = unidades.length;
  const completo = total > 0 && hechas === total;
  if (completo) li.classList.add('cluster-completo');
  const abierto = clustersExpandidos.has(c.id);

  const cuerpoId = `cluster-cuerpo-${c.id}`;

  const cab = document.createElement('button');
  cab.type = 'button';
  cab.className = 'cluster-cabecera';
  cab.setAttribute('aria-expanded', String(abierto));
  cab.setAttribute('aria-controls', cuerpoId);
  const chip = ETIQUETA_TRACK[c.track]
    ? `<span class="ruta-chip ruta-${rutaDeTrack(c.track)}">${ETIQUETA_TRACK[c.track]}</span>`
    : '';
  cab.innerHTML =
    '<span class="cluster-chevron" aria-hidden="true">▸</span>' +
    '<span class="cluster-titulo"></span>' +
    chip +
    `<span class="cluster-progreso${completo ? ' cluster-progreso-ok' : ''}"></span>`;
  cab.querySelector('.cluster-titulo').textContent = c.titulo;
  cab.querySelector('.cluster-progreso').textContent =
    total > 0 ? `${hechas}/${total} ${completo ? '✓' : 'unidades'}` : 'sin unidades';

  const cuerpo = document.createElement('div');
  cuerpo.className = 'cluster-cuerpo';
  cuerpo.id = cuerpoId;
  cuerpo.hidden = !abierto;

  if (c.descripcion) {
    const desc = document.createElement('p');
    desc.className = 'cluster-desc';
    desc.textContent = c.descripcion;
    cuerpo.appendChild(desc);
  }
  if (c.secuencia) {
    const sec = document.createElement('p');
    sec.className = 'cluster-secuencia';
    const sb = document.createElement('strong');
    sb.textContent = 'Secuencia: ';
    sec.append(sb, document.createTextNode(c.secuencia));
    cuerpo.appendChild(sec);
  }

  const ul = document.createElement('ul');
  ul.className = 'estudio-unidades';
  unidades.forEach((u) => ul.appendChild(crearUnidadItem(u, b)));
  cuerpo.appendChild(ul);

  // Simulación de entrevista de esta ronda (Nivel E), integrada en la categoría.
  if (c.sim) {
    const wrap = document.createElement('div');
    wrap.className = 'cluster-sim-wrap';
    const lanzar = document.createElement('button');
    lanzar.type = 'button';
    lanzar.className = 'secundario entrevista-launch';
    lanzar.textContent = '🎤 Simular entrevista de esta ronda';
    const panel = document.createElement('div');
    panel.className = 'entrevista';
    panel.hidden = true;
    lanzar.addEventListener('click', () => abrirSimCluster(c.id, lanzar, panel));
    wrap.append(lanzar, panel);
    cuerpo.appendChild(wrap);
  }

  // Examen final del cluster: banco completo de todas las lecciones, con selector de nivel.
  if (c.id !== '__otras') {
    const examWrap = document.createElement('div');
    examWrap.className = 'cluster-exam-wrap';
    const examBtn = document.createElement('button');
    examBtn.type = 'button';
    examBtn.className = 'secundario cluster-exam-launch';
    examBtn.textContent = '📝 Examen final del cluster';
    examBtn.addEventListener('click', () => prepararExamenCluster(c.id, c.titulo));
    examWrap.appendChild(examBtn);
    cuerpo.appendChild(examWrap);
  }

  // Referencias bibliográficas: fuentes que sirvieron de base para el cluster.
  if (c.id !== '__otras' && Array.isArray(c.referencias) && c.referencias.length) {
    const refWrap = document.createElement('div');
    refWrap.className = 'cluster-referencias';
    const refTit = document.createElement('p');
    refTit.className = 'cluster-ref-titulo';
    refTit.textContent = 'Referencias';
    refWrap.appendChild(refTit);
    const refList = document.createElement('ul');
    refList.className = 'cluster-ref-lista';
    c.referencias.forEach((ref) => {
      const li2 = document.createElement('li');
      li2.textContent = ref;
      refList.appendChild(li2);
    });
    refWrap.appendChild(refList);
    cuerpo.appendChild(refWrap);
  }

  cab.addEventListener('click', () => {
    const ahora = cuerpo.hidden;
    cuerpo.hidden = !ahora;
    cab.setAttribute('aria-expanded', String(ahora));
    li.classList.toggle('abierto', ahora);
    if (ahora) clustersExpandidos.add(c.id);
    else clustersExpandidos.delete(c.id);
  });

  li.classList.toggle('abierto', abierto);
  li.append(cab, cuerpo);
  return li;
}

// Abre (o cierra si ya estaba) la simulación de un cluster en SU panel (cada
// categoría tiene el suyo): carga su guion cluster-<id>.json y lo renderiza como
// ronda interactiva (forcejeo antes de la rúbrica). JSON estructurado, sin tocar
// el esquema de study.json.
async function abrirSimCluster(clusterId, btn, panel) {
  const cluster = taxonomia.find((c) => c.id === clusterId);
  if (!cluster || !panel) return;

  // Segundo click → cerrar.
  if (!panel.hidden) {
    panel.hidden = true;
    panel.innerHTML = '';
    btn.textContent = '🎤 Simular entrevista de esta ronda';
    return;
  }

  if (!(clusterId in simClusterCache)) {
    if (btn) btn.disabled = true;
    try {
      const res = await fetch(`data/entrevista/${cluster.sim}`);
      simClusterCache[clusterId] = res.ok ? await res.json() : null;
    } catch {
      simClusterCache[clusterId] = null;
    }
    if (btn) btn.disabled = false;
  }

  panel.innerHTML = '';
  const sim = simClusterCache[clusterId];
  if (!sim) {
    panel.innerHTML =
      '<p class="leccion-error">La simulación no está disponible ahora mismo — revisa la conexión e inténtalo de nuevo (una vez cargada queda guardada para practicar sin red).</p>';
  } else {
    const titulo = document.createElement('h3');
    titulo.className = 'entrevista-sim-titulo';
    titulo.textContent = `Ronda: ${cluster.titulo}`;
    panel.appendChild(titulo);
    panel.appendChild(construirEntrevista(sim));
  }
  panel.hidden = false;
  btn.textContent = '✕ Cerrar simulación';
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Construye el DOM de una simulación (sin innerHTML de datos: todo con textContent,
// el contenido es nuestro pero así no hay forma de inyectar markup por error).
function construirEntrevista(sim) {
  const frag = document.createDocumentFragment();

  const rol = document.createElement('p');
  rol.className = 'entrevista-rol';
  const rolB = document.createElement('strong');
  rolB.textContent = 'El entrevistador: ';
  rol.append(rolB, document.createTextNode(sim.rol ?? ''));
  if (sim.duracion) {
    const d = document.createElement('span');
    d.className = 'entrevista-duracion';
    d.textContent = ` · ${sim.duracion}`;
    rol.appendChild(d);
  }
  frag.appendChild(rol);

  const intro = document.createElement('p');
  intro.className = 'entrevista-instruccion';
  intro.textContent =
    'Responde cada pregunta en voz alta (o por escrito) antes de revelar la rúbrica. La nota la pones tú: ¿cubriste los puntos? ¿caíste en alguna trampa de comunicación?';
  frag.appendChild(intro);

  (sim.preguntas ?? []).forEach((p, i) => {
    const card = document.createElement('div');
    card.className = 'entrevista-q';

    const preg = document.createElement('p');
    preg.className = 'entrevista-pregunta';
    const num = document.createElement('span');
    num.className = 'entrevista-num';
    num.textContent = `P${i + 1}. `;
    preg.append(num, document.createTextNode(p.q ?? ''));
    card.appendChild(preg);

    const revelar = document.createElement('div');
    revelar.className = 'entrevista-revelar';
    revelar.hidden = true;

    const tituloR = document.createElement('p');
    tituloR.className = 'entrevista-subt';
    tituloR.textContent = 'Una respuesta fuerte cubre:';
    revelar.appendChild(tituloR);
    revelar.appendChild(listaEntrevista(p.rubrica, 'rubrica'));

    if (p.seguimiento) {
      const seg = document.createElement('p');
      seg.className = 'entrevista-seguimiento';
      const segB = document.createElement('strong');
      segB.textContent = 'Repregunta de presión: ';
      seg.append(segB, document.createTextNode(p.seguimiento));
      revelar.appendChild(seg);
    }

    if (p.errores?.length) {
      const tituloE = document.createElement('p');
      tituloE.className = 'entrevista-subt';
      tituloE.textContent = 'Errores de comunicación frecuentes:';
      revelar.appendChild(tituloE);
      revelar.appendChild(listaEntrevista(p.errores, 'errores'));
    }

    const btn = document.createElement('button');
    btn.className = 'secundario entrevista-toggle';
    btn.type = 'button';
    btn.textContent = 'Ver rúbrica y trampas';
    btn.addEventListener('click', () => {
      revelar.hidden = !revelar.hidden;
      btn.textContent = revelar.hidden ? 'Ver rúbrica y trampas' : 'Ocultar rúbrica';
    });

    card.append(btn, revelar);
    frag.appendChild(card);
  });

  if (sim.cierre) {
    const cierre = document.createElement('blockquote');
    cierre.className = 'entrevista-cierre';
    cierre.textContent = sim.cierre;
    frag.appendChild(cierre);
  }
  return frag;
}

function listaEntrevista(items, clase) {
  const ul = document.createElement('ul');
  ul.className = `entrevista-lista entrevista-${clase}`;
  (items ?? []).forEach((it) => {
    const li = document.createElement('li');
    li.textContent = it;
    ul.appendChild(li);
  });
  return ul;
}

// Navega a otra unidad desde un enlace de concepto y abre su lección directamente
// (el lector venía leyendo). Si la unidad vive en otro bloque, lo hace visible.
function navegarAUnidad(id) {
  const u = unidad(id);
  if (!u) return;
  const b = datos.bloques.find((x) => x.id === u.bloque);
  if (b && b.id !== bloqueVisibleObj().id) {
    bloqueVisible = b;
    // Si la unidad destino vive en una categoría de la taxonomía, despliégala
    // para que el lector aterrice viendo su contexto (no una lista colapsada).
    const cl = taxonomia.find((c) => (c.unidades ?? []).includes(id));
    if (cl) clustersExpandidos.add(cl.id);
    renderizar();
  }
  abrirUnidad(id);
  alternarLeccion(u); // el panel nace con la lección cerrada → esto la abre
}

/* ===================== Render: unidad y su quiz ======================= */

function abrirUnidad(unidadId) {
  const u = unidad(unidadId);
  if (!u) return;
  const panel = $('estudio-unidad');
  panel.hidden = false;
  panel.dataset.unidad = u.id;

  $('unidad-titulo').textContent = u.titulo;
  $('unidad-lectura').innerHTML = '';
  const filas = [
    ['Libro', u.libro],
    ['Lectura', u.lectura],
    ['Dosis', u.dosis],
    ['Al leer, busca', u.objetivo],
  ];
  filas.forEach(([k, v]) => {
    if (!v) return;
    const p = document.createElement('p');
    p.className = 'fila';
    const b = document.createElement('strong');
    b.textContent = `${k}: `;
    p.append(b, v);
    $('unidad-lectura').appendChild(p);
  });

  // Lección integrada: cerrada al entrar; se abre/cierra con el botón
  const btnLeccion = $('btn-unidad-leccion');
  btnLeccion.hidden = false;
  btnLeccion.disabled = false;
  btnLeccion.textContent = '📖 Leer la lección aquí';
  $('unidad-leccion').hidden = true;
  $('unidad-leccion').innerHTML = '';
  btnLeccion.onclick = () => alternarLeccion(u);

  const e = load('estudio');
  const enCurso = e.quizEnCurso?.unidadId === u.id;

  // Limpiar selector de dificultad de una unidad anterior
  const prevSel = $('quiz-dificultad-selector');
  if (prevSel) prevSel.remove();

  if (unidadCompletada(u.id)) {
    $('unidad-quiz').hidden = true;
    $('btn-quiz-iniciar').hidden = true;
    mostrarCierreUnidad(u, e.unidadesCompletadas[u.id]);
  } else if (enCurso) {
    $('unidad-cierre').hidden = true;
    $('btn-quiz-iniciar').hidden = true;
    renderPreguntaQuiz();
  } else {
    $('unidad-cierre').hidden = true;
    $('unidad-quiz').hidden = true;

    // Selector de dificultad antes del botón de inicio
    const selectorDif = document.createElement('div');
    selectorDif.id = 'quiz-dificultad-selector';
    selectorDif.className = 'quiz-dif-selector';
    $('btn-quiz-iniciar').insertAdjacentElement('beforebegin', selectorDif);

    const labelEl = document.createElement('span');
    labelEl.className = 'quiz-dif-label';
    labelEl.textContent = 'Nivel:';
    selectorDif.appendChild(labelEl);

    const msgVacioLeccion = document.createElement('p');
    msgVacioLeccion.className = 'quiz-dif-vacio';
    msgVacioLeccion.hidden = true;

    let difSeleccionada = 'mixto';
    const difOpciones = [
      { valor: 'mixto', etiqueta: 'Mixto' },
      { valor: 'easy', etiqueta: 'Fácil' },
      { valor: 'medium', etiqueta: 'Medio' },
      { valor: 'hard', etiqueta: 'Difícil' },
    ];
    difOpciones.forEach(({ valor, etiqueta }) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `quiz-dif-btn${valor === 'mixto' ? ' activo' : ''}`;
      btn.textContent = etiqueta;
      btn.dataset.valor = valor;
      btn.addEventListener('click', () => {
        difSeleccionada = valor;
        selectorDif.querySelectorAll('.quiz-dif-btn').forEach((b) =>
          b.classList.toggle('activo', b.dataset.valor === valor)
        );
        const pool = difSeleccionada === 'mixto'
          ? u.banco
          : u.banco.filter((q) => q.difficulty === difSeleccionada);
        if (pool.length === 0) {
          $('btn-quiz-iniciar').hidden = true;
          msgVacioLeccion.hidden = false;
          msgVacioLeccion.textContent =
            `Esta lección no tiene preguntas de nivel ${etiqueta}. Prueba otro nivel.`;
        } else {
          $('btn-quiz-iniciar').hidden = false;
          msgVacioLeccion.hidden = true;
        }
      });
      selectorDif.appendChild(btn);
    });
    selectorDif.appendChild(msgVacioLeccion);

    $('btn-quiz-iniciar').hidden = false;
    $('btn-quiz-iniciar').onclick = () => {
      const pool = difSeleccionada === 'mixto'
        ? u.banco
        : u.banco.filter((q) => q.difficulty === difSeleccionada);
      if (!pool.length) return;
      const ids = barajar(pool.map((q) => q.id));
      update('estudio', (st) => {
        st.quizEnCurso = {
          unidadId: u.id,
          preguntasIds: ids,
          dificultad: difSeleccionada,
          indice: 0,
          resultados: [],
          esRepaso: false,
        };
        return st;
      });
      selectorDif.remove();
      $('btn-quiz-iniciar').hidden = true;
      renderPreguntaQuiz();
    };
  }
  panel.scrollIntoView({ behavior: 'smooth' });
}

/** Pinta la pregunta actual del quiz (retrieval: responder antes de ver). */
function renderPreguntaQuiz() {
  const e = load('estudio');
  const qc = e.quizEnCurso;
  const u = unidad(qc?.unidadId);
  if (!u) return;

  // Soporte para preguntasIds (repaso y quiz normal)
  const ids = qc.preguntasIds ?? u.banco.map((b) => b.id);
  const qid = ids[qc.indice];
  const q = u.banco.find((b) => b.id === qid);
  if (!q) return finalizarQuiz();

  const cont = $('unidad-quiz');
  cont.hidden = false;
  cont.innerHTML = '';

  const head = document.createElement('p');
  head.className = 'quiz-progreso';
  const prefijo = qc.esRepaso ? 'Repaso' : (NOMBRES_TIPO[q.tipo] ?? 'Pregunta');
  head.textContent = `${prefijo} · ${qc.indice + 1} de ${ids.length}`;
  cont.appendChild(head);

  const enunciado = document.createElement('p');
  enunciado.className = 'quiz-enunciado';
  enunciado.innerHTML = renderInline(q.enunciado); // markdown + KaTeX
  cont.appendChild(enunciado);

  const ta = document.createElement('textarea');
  ta.className = 'textarea-corta';
  ta.placeholder = 'Responde desde la memoria, por escrito. El forcejeo es el aprendizaje.';
  ta.value = qc.respuestaParcial ?? ''; // recupera lo escrito si se recargó
  cont.appendChild(ta);

  const pie = document.createElement('div');
  pie.className = 'textarea-pie';
  const contador = document.createElement('span');
  pie.appendChild(contador);
  cont.appendChild(pie);

  const btnRevelar = document.createElement('button');
  btnRevelar.className = 'primario';
  btnRevelar.textContent = 'Mostrar respuesta esperada';
  cont.appendChild(btnRevelar);

  const refrescarEstado = () => {
    const len = ta.value.trim().length;
    contador.textContent = `${len} / ${MIN_RESPUESTA_QUIZ} caracteres`;
    btnRevelar.disabled = len < MIN_RESPUESTA_QUIZ;
  };
  refrescarEstado();

  let autosave = null;
  ta.addEventListener('input', () => {
    refrescarEstado();
    clearTimeout(autosave);
    autosave = setTimeout(() => {
      update('estudio', (st) => {
        if (st.quizEnCurso?.unidadId === u.id) st.quizEnCurso.respuestaParcial = ta.value;
        return st;
      });
    }, 400);
  });

  btnRevelar.addEventListener('click', () => {
    btnRevelar.hidden = true;
    ta.readOnly = true;

    const sol = document.createElement('div');
    sol.className = 'quiz-solucion';
    const st = document.createElement('p');
    st.innerHTML = renderInline(q.solucion); // markdown + KaTeX
    sol.appendChild(st);
    if (q.explicacion) {
      const ex = document.createElement('p');
      ex.className = 'quiz-explicacion';
      ex.innerHTML = renderInline(q.explicacion);
      sol.appendChild(ex);
    }
    cont.appendChild(sol);

    // Autoevaluación honesta del recall
    const fs = document.createElement('fieldset');
    fs.className = 'autoeval';
    fs.innerHTML =
      '<legend>Comparado con la respuesta esperada, ¿cómo estuvo la tuya?</legend>' +
      '<label><input type="radio" name="quiz-eval" value="bien" /> Lo tenía</label>' +
      '<label><input type="radio" name="quiz-eval" value="parcial" /> A medias</label>' +
      '<label><input type="radio" name="quiz-eval" value="mal" /> No lo tenía</label>';
    cont.appendChild(fs);

    const btnSig = document.createElement('button');
    btnSig.className = 'primario';
    btnSig.textContent = qc.indice + 1 < ids.length ? 'Siguiente pregunta' : 'Cerrar evaluación';
    cont.appendChild(btnSig);

    btnSig.addEventListener('click', () => {
      const evalSel = cont.querySelector('input[name="quiz-eval"]:checked')?.value;
      if (!evalSel) return;
      update('estudio', (st2) => {
        st2.quizEnCurso.resultados.push({
          preguntaId: q.id,
          tipo: q.tipo,
          respuesta: ta.value.trim(),
          evaluacion: evalSel,
        });
        st2.quizEnCurso.indice += 1;
        st2.quizEnCurso.respuestaParcial = '';
        return st2;
      });
      renderPreguntaQuiz();
    });
  });
}

/** Cierra la unidad: guarda resultados, cuenta el día y muestra el destilado. */
function finalizarQuiz() {
  const e = load('estudio');
  const qc = e.quizEnCurso;
  const u = unidad(qc?.unidadId);
  if (!u) return;

  const aciertos = qc.resultados.filter((r) => r.evaluacion === 'bien').length;
  const esRepaso = qc.esRepaso ?? false;

  // Preguntas que necesitan otro repaso (mal o parcial)
  const bienIds = new Set(
    qc.resultados.filter((r) => r.evaluacion === 'bien').map((r) => r.preguntaId)
  );
  const nuevasPendientes = (qc.preguntasIds ?? u.banco.map((b) => b.id))
    .filter((id) => !bienIds.has(id));

  const registro = esRepaso
    ? { ...load('estudio').unidadesCompletadas[u.id] }   // preserva la primera fecha y aciertos
    : { fecha: hoy(), aciertos, total: u.banco.length, resultados: qc.resultados };

  update('estudio', (st) => {
    if (!esRepaso) st.unidadesCompletadas[u.id] = registro;
    st.pendientesRepaso ??= {};
    st.pendientesRepaso[u.id] = nuevasPendientes;
    st.quizEnCurso = null;
    return st;
  });
  marcarDiaEstudio();
  encolarEvento('unidad', { unidadId: u.id, registro });
  // Sellos: el cierre de unidad es pantalla de cierre válida para revelar.
  // Quedan en un buffer que mostrarCierreUnidad consume una sola vez.
  sellosPendientes = Badges.evaluarYRegistrar();

  $('unidad-quiz').hidden = true;
  renderizar();
  abrirUnidad(u.id);
}

/** Inicia un quiz de repaso con solo las preguntas aún pendientes. */
function iniciarRepaso(u) {
  const pendientes = load('estudio').pendientesRepaso?.[u.id] ?? [];
  if (!pendientes.length) return;
  update('estudio', (st) => {
    st.quizEnCurso = {
      unidadId: u.id,
      preguntasIds: pendientes,
      indice: 0,
      resultados: [],
      esRepaso: true,
    };
    return st;
  });
  $('unidad-cierre').hidden = true;
  renderPreguntaQuiz();
}

/** Sellos recién ganados, pendientes de revelar en el próximo cierre pintado. */
let sellosPendientes = [];

/** Las ideas clave se muestran SOLO aquí: después del retrieval, nunca antes. */
function mostrarCierreUnidad(u, registro) {
  const cierre = $('unidad-cierre');
  cierre.hidden = false;
  cierre.innerHTML = '';

  const resumen = document.createElement('p');
  resumen.className = 'fila';
  resumen.textContent = `Unidad completada el ${registro.fecha} — recall: ${registro.aciertos}/${registro.total}.`;
  cierre.appendChild(resumen);

  if (u.ideas_clave?.length) {
    const h = document.createElement('p');
    h.className = 'cierre-titulo';
    h.textContent = 'Ideas clave del capítulo (ya te las ganaste):';
    cierre.appendChild(h);
    const ul = document.createElement('ul');
    ul.className = 'ideas-clave';
    u.ideas_clave.forEach((idea) => {
      const li = document.createElement('li');
      li.innerHTML = renderInline(idea); // markdown + KaTeX
      ul.appendChild(li);
    });
    cierre.appendChild(ul);
  }

  // Botón de repaso si hay preguntas pendientes
  const pendientes = load('estudio').pendientesRepaso?.[u.id] ?? [];
  if (pendientes.length) {
    const btnRepaso = document.createElement('button');
    btnRepaso.className = 'secundario';
    btnRepaso.textContent =
      `Repasar ${pendientes.length} pregunta${pendientes.length > 1 ? 's' : ''} pendiente${pendientes.length > 1 ? 's' : ''}`;
    btnRepaso.addEventListener('click', () => iniciarRepaso(u));
    cierre.appendChild(btnRepaso);
  }

  const nota = document.createElement('p');
  nota.className = 'nota-privacidad';
  nota.textContent = pendientes.length
    ? 'Las preguntas marcadas "no lo tenía" o "a medias" aparecen aquí hasta que las domines.'
    : 'Todas las preguntas dominadas — el recall fue completo.';
  cierre.appendChild(nota);

  if (sellosPendientes.length) {
    const cajaSellos = document.createElement('div');
    cajaSellos.className = 'insignias-reveladas';
    Badges.renderReveladas(sellosPendientes, cajaSellos);
    cierre.appendChild(cajaSellos);
    sellosPendientes = [];
  }
}

/* ================== Examen del bloque (motor, PDF §8b) ================ */

/**
 * Pool acumulativo con interleaving: ítems de examen de TODOS los bloques
 * hasta el actual, barajados evitando dos heurísticas iguales consecutivas.
 */
function muestrearExamen(bloque, n = 5) {
  const idx = datos.bloques.findIndex((b) => b.id === bloque.id);
  const pool = datos.bloques
    .slice(0, idx + 1)
    .flatMap((b) => b.examen?.items ?? []);
  const baraja = [...pool].sort(() => Math.random() - 0.5);
  const sel = [];
  while (sel.length < Math.min(n, baraja.length)) {
    let i = baraja.findIndex((it) => it.heuristica !== sel.at(-1)?.heuristica);
    if (i === -1) i = 0;
    sel.push(baraja.splice(i, 1)[0]);
  }
  return sel.map((it) => it.id);
}

function itemExamen(id) {
  return datos.bloques
    .flatMap((b) => b.examen?.items ?? [])
    .find((it) => it.id === id);
}

function iniciarExamen() {
  const b = bloqueVisibleObj();
  update('estudio', (st) => {
    st.examenEnCurso = {
      bloqueId: b.id,
      itemIds: muestrearExamen(b),
      indice: 0,
      paso: 'prediccion',
      registros: [],
      iniciadoEn: Date.now(),
      textareasPorItem: {},
    };
    return st;
  });
  renderExamen();
}

/** Pinta el paso actual del examen (predicción → forcejeo → revelado). */
function renderExamen() {
  const ex = load('estudio').examenEnCurso;
  if (!ex) return;
  const item = itemExamen(ex.itemIds[ex.indice]);
  if (!item) return finalizarExamen();

  const panel = $('estudio-examen');
  panel.hidden = false;
  const cont = $('examen-contenido');
  cont.innerHTML = '';
  $('estudio-unidad').hidden = true;

  const head = document.createElement('div');
  head.className = 'examen-cabecera';

  const progreso = document.createElement('span');
  progreso.className = 'quiz-progreso';
  progreso.textContent = `Problema ${ex.indice + 1} de ${ex.itemIds.length}`;
  head.appendChild(progreso);

  if (ex.iniciadoEn) {
    const reloj = document.createElement('span');
    reloj.className = 'examen-reloj';
    const tick = () => {
      const seg = Math.floor((Date.now() - ex.iniciadoEn) / 1000);
      const m = Math.floor(seg / 60).toString().padStart(2, '0');
      const s = (seg % 60).toString().padStart(2, '0');
      reloj.textContent = `${m}:${s}`;
    };
    tick();
    const iv = setInterval(tick, 1000);
    // Limpia el intervalo cuando el panel desaparece del DOM
    new MutationObserver((_, obs) => {
      if (!document.contains(reloj)) { clearInterval(iv); obs.disconnect(); }
    }).observe(document.body, { childList: true, subtree: true });
    head.appendChild(reloj);
  }

  cont.appendChild(head);

  const enunciado = document.createElement('p');
  enunciado.className = 'quiz-enunciado';
  enunciado.innerHTML = renderInline(item.enunciado); // markdown + KaTeX
  cont.appendChild(enunciado);

  if (ex.paso === 'prediccion') renderPasoPrediccion(cont, item, ex);
  else renderPasoForcejeo(cont, item, ex);

  panel.scrollIntoView({ behavior: 'smooth' });
}

/** Paso 1 (PDF §8b): predicción de jugada ANTES de atacar. */
function renderPasoPrediccion(cont, item, ex) {
  const fs = document.createElement('fieldset');
  fs.className = 'autoeval vertical';
  const legend = document.createElement('legend');
  legend.textContent =
    'Antes de atacar: ¿qué jugada del catálogo crees que pide este problema?';
  fs.appendChild(legend);

  // Heurísticas relevantes para este examen: unión de lo enseñado en las
  // unidades del bloque + lo que realmente se pide en los ítems del examen.
  // Así se excluyen las heurísticas de otros bloques que el usuario aún
  // no ha visto, sin ocultar jamás la respuesta correcta.
  const bloqueObj = datos.bloques.find((b) => b.id === ex.bloqueId) ?? {};
  const heurBloque = new Set([
    ...unidadesDe(bloqueObj).flatMap((u) => u.heuristicas ?? []),
    ...(bloqueObj.examen?.items ?? []).map((it) => it.heuristica).filter(Boolean),
  ]);
  const opcionesPred = (datos.catalogoHeuristicas ?? []).filter(
    (h) => heurBloque.has(h.id)
  );
  // Fallback: si el bloque no mapea heurísticas, mostrar el catálogo completo
  (opcionesPred.length ? opcionesPred : datos.catalogoHeuristicas ?? []).forEach((h) => {
    const label = document.createElement('label');
    const input = document.createElement('input');
    input.type = 'radio';
    input.name = 'examen-prediccion';
    input.value = h.id;
    label.append(input, ` ${h.nombre}`);
    fs.appendChild(label);
  });
  const labelNo = document.createElement('label');
  labelNo.innerHTML = '<input type="radio" name="examen-prediccion" value="nose" /> Aún no lo veo';
  fs.appendChild(labelNo);
  cont.appendChild(fs);

  const fsConf = document.createElement('fieldset');
  fsConf.className = 'autoeval vertical';
  const legendConf = document.createElement('legend');
  legendConf.textContent = '¿Qué tan seguro estás? (1 = adivinando, 5 = lo veo claro)';
  fsConf.appendChild(legendConf);
  [1, 2, 3, 4, 5].forEach((v) => {
    const labelConf = document.createElement('label');
    const inputConf = document.createElement('input');
    inputConf.type = 'radio';
    inputConf.name = 'examen-confianza';
    inputConf.value = v;
    labelConf.append(inputConf, ` ${v}`);
    fsConf.appendChild(labelConf);
  });
  cont.appendChild(fsConf);

  const btn = document.createElement('button');
  btn.className = 'primario';
  btn.textContent = 'Registrar predicción y forcejear';
  cont.appendChild(btn);

  btn.addEventListener('click', () => {
    const pred = cont.querySelector('input[name="examen-prediccion"]:checked')?.value;
    if (!pred) return;
    const conf = Number(cont.querySelector('input[name="examen-confianza"]:checked')?.value ?? 3);
    update('estudio', (st) => {
      st.examenEnCurso.registros.push({
        itemId: item.id,
        heuristica: item.heuristica,
        prediccion: pred,
        confianza: conf,
        pistaUsada: false,
        pistasUsadas: 0,
        resultado: null,
        disparadorOk: null,
      });
      st.examenEnCurso.paso = 'forcejeo';
      return st;
    });
    renderExamen();
  });
}

/** Pasos 2-3 (PDF §8b): forcejeo con autoreporte y disparador correcto. */
function renderPasoForcejeo(cont, item, ex) {
  const ta = document.createElement('textarea');
  ta.placeholder = 'Forcejea aquí por escrito: intentos, casos pequeños, caminos muertos…';
  // Restaurar y persistir el texto de forcejeo del examen (sobrevive recargas)
  const textoGuardado = load('estudio').examenEnCurso?.textareasPorItem?.[item.id] ?? '';
  if (textoGuardado) ta.value = textoGuardado;
  ta.addEventListener('input', () => {
    update('estudio', (st) => {
      if (st.examenEnCurso) {
        st.examenEnCurso.textareasPorItem ??= {};
        st.examenEnCurso.textareasPorItem[item.id] = ta.value;
      }
      return st;
    });
  });
  cont.appendChild(ta);

  // Pistas graduadas (fase-7+): array de 5 niveles
  if (item.pistas?.length) {
    const pistasContainer = document.createElement('div');
    pistasContainer.className = 'pistas-container';
    cont.appendChild(pistasContainer);

    const btnPistas = document.createElement('button');
    btnPistas.className = 'secundario';
    pistasContainer.appendChild(btnPistas);

    let nivelActual = 0;
    const revelarPista = (registrar) => {
      if (nivelActual >= item.pistas.length) return;
      const div = document.createElement('div');
      div.className = 'hint-item';
      const nivel = document.createElement('span');
      nivel.className = 'pista-nivel';
      nivel.textContent = `Pista ${nivelActual + 1}/${item.pistas.length}: `;
      div.appendChild(nivel);
      const txt = document.createElement('span');
      txt.innerHTML = renderInline(item.pistas[nivelActual]); // markdown + KaTeX
      div.appendChild(txt);
      pistasContainer.insertBefore(div, btnPistas);
      nivelActual++;
      if (registrar) {
        update('estudio', (st) => {
          const r = st.examenEnCurso.registros.at(-1);
          r.pistaUsada = true;
          r.pistasUsadas = Math.max(r.pistasUsadas ?? 0, nivelActual);
          return st;
        });
      }
      btnPistas.hidden = nivelActual >= item.pistas.length;
      btnPistas.textContent = `Pedir pista ${nivelActual + 1}/${item.pistas.length}`;
    };
    btnPistas.addEventListener('click', () => revelarPista(true));

    // Tras una recarga, reponer las pistas ya pedidas (el examen persiste)
    const yaPedidas = load('estudio').examenEnCurso?.registros.at(-1)?.pistasUsadas ?? 0;
    btnPistas.textContent = `Pedir pista 1/${item.pistas.length}`;
    for (let i = 0; i < yaPedidas; i++) revelarPista(false);

  // Una sola pista permitida, como en el protocolo del PDF
  } else if (item.pista) {
    const btnPista = document.createElement('button');
    btnPista.className = 'secundario';
    btnPista.textContent = 'Pedir LA pista (solo hay una)';
    cont.appendChild(btnPista);
    btnPista.addEventListener('click', () => {
      btnPista.hidden = true;
      const div = document.createElement('div');
      div.className = 'hint-item';
      div.innerHTML = renderInline(item.pista); // markdown + KaTeX
      cont.insertBefore(div, btnPista);
      update('estudio', (st) => {
        st.examenEnCurso.registros.at(-1).pistaUsada = true;
        return st;
      });
    });
  }

  const labelConPista = item.pistas?.length > 1 ? 'Resuelto con las pistas' : 'Resuelto con la pista';
  const fs = document.createElement('fieldset');
  fs.className = 'autoeval';
  fs.innerHTML =
    '<legend>Resultado honesto:</legend>' +
    '<label><input type="radio" name="examen-resultado" value="resuelto-solo" /> Resuelto sin ayuda</label>' +
    `<label><input type="radio" name="examen-resultado" value="resuelto-pista" /> ${labelConPista}</label>` +
    '<label><input type="radio" name="examen-resultado" value="no-resuelto" /> No resuelto</label>';
  cont.appendChild(fs);

  const btnRevelar = document.createElement('button');
  btnRevelar.className = 'primario';
  btnRevelar.textContent = 'Revelar solución y disparador';
  cont.appendChild(btnRevelar);

  btnRevelar.addEventListener('click', () => {
    const resultado = cont.querySelector('input[name="examen-resultado"]:checked')?.value;
    if (!resultado) return;
    btnRevelar.hidden = true;
    fs.querySelectorAll('input').forEach((i) => (i.disabled = true));
    ta.readOnly = true;

    const reg = load('estudio').examenEnCurso.registros.at(-1);
    const sol = document.createElement('div');
    sol.className = 'quiz-solucion';

    const h = datos.catalogoHeuristicas.find((x) => x.id === item.heuristica);
    const p1 = document.createElement('p');
    const b1 = document.createElement('strong');
    b1.textContent = `Jugada: ${h?.nombre ?? item.heuristica}. `;
    p1.append(b1, reg.prediccion === item.heuristica
      ? '✓ Tu predicción coincidió: reconociste la jugada en frío.'
      : 'Tu predicción apuntó a otra jugada — compara: ¿qué señal del enunciado te faltó leer?');
    sol.appendChild(p1);

    if (reg.confianza >= 4 && reg.prediccion !== item.heuristica) {
      const pCal = document.createElement('p');
      pCal.className = 'quiz-calibracion';
      pCal.textContent = 'Ibas muy seguro y la jugada era otra: re-calibra tu confianza.';
      sol.appendChild(pCal);
    } else if (reg.confianza <= 2 && reg.prediccion === item.heuristica) {
      const pCal = document.createElement('p');
      pCal.className = 'quiz-calibracion';
      pCal.textContent = 'Acertaste dudando: la intuición iba bien — confía un punto más la próxima.';
      sol.appendChild(pCal);
    }

    const p2 = document.createElement('p');
    p2.innerHTML = renderInline(item.solucion); // markdown + KaTeX
    sol.appendChild(p2);

    const p3 = document.createElement('p');
    p3.className = 'quiz-explicacion';
    const b3 = document.createElement('strong');
    b3.textContent = '★ Disparador: ';
    const disp = document.createElement('span');
    disp.innerHTML = renderInline(item.disparador);
    p3.append(b3, disp);
    sol.appendChild(p3);
    cont.appendChild(sol);

    // Cierre del ítem: en fallados, el disparador identificado es lo que puntúa
    const fs2 = document.createElement('fieldset');
    fs2.className = 'autoeval';
    fs2.innerHTML =
      '<legend>¿Quedó claro (y anotado) qué señal del enunciado apuntaba a esa jugada?</legend>' +
      '<label><input type="radio" name="examen-disparador" value="si" /> Sí, lo identifico</label>' +
      '<label><input type="radio" name="examen-disparador" value="no" /> Todavía no</label>';
    cont.appendChild(fs2);

    const btnSig = document.createElement('button');
    btnSig.className = 'primario';
    btnSig.textContent = 'Siguiente';
    cont.appendChild(btnSig);

    btnSig.addEventListener('click', () => {
      const disp = cont.querySelector('input[name="examen-disparador"]:checked')?.value;
      if (!disp) return;
      update('estudio', (st) => {
        const r = st.examenEnCurso.registros.at(-1);
        r.resultado = resultado;
        r.disparadorOk = disp === 'si';
        st.examenEnCurso.indice += 1;
        st.examenEnCurso.paso = 'prediccion';
        return st;
      });
      renderExamen();
    });
  });
}

/**
 * Criterio de aprobado del PDF §8b: predicción coincide en ≥3 de 5 Y por
 * cada problema fallado el disparador quedó correctamente identificado.
 */
function finalizarExamen() {
  const ex = load('estudio').examenEnCurso;
  if (!ex) return;

  const coincidencias = ex.registros.filter((r) => r.prediccion === r.heuristica).length;
  const fallados = ex.registros.filter((r) => r.resultado === 'no-resuelto');
  const minCoincidencias = Math.min(3, ex.registros.length);
  const aprobado =
    coincidencias >= minCoincidencias && fallados.every((r) => r.disparadorOk);

  let registroExamen = null;
  update('estudio', (st) => {
    const previo = st.examenes[ex.bloqueId];
    registroExamen = {
      aprobado: aprobado || Boolean(previo?.aprobado),
      fecha: hoy(),
      coincidencias,
      total: ex.registros.length,
      registros: ex.registros,
      intentos: (previo?.intentos ?? 0) + 1,
    };
    st.examenes[ex.bloqueId] = registroExamen;
    st.examenEnCurso = null;
    return st;
  });
  marcarDiaEstudio();
  encolarEvento('examen', { bloqueId: ex.bloqueId, registro: registroExamen });
  const insigniasNuevas = Badges.evaluarYRegistrar();

  const cont = $('examen-contenido');
  cont.innerHTML = '';
  const res = document.createElement('p');
  res.className = 'quiz-enunciado';
  // Lenguaje de fallo (§2.2): validar el proceso + dato + reencuadre
  res.textContent = aprobado
    ? `Examen aprobado: ${coincidencias}/${ex.registros.length} disparadores reconocidos en frío. El siguiente bloque está abierto.`
    : `Todavía no — y este intento ya fue entrenamiento real: reconociste ${coincidencias}/${ex.registros.length} jugadas en frío` +
      (fallados.some((r) => !r.disparadorOk)
        ? ' y detectaste qué disparadores te faltan por anotar.'
        : '.') +
      ' Relee tus fichas de esas heurísticas y reintenta cuando quieras: se aprueba reconociendo jugadas, no resolviéndolo todo.';
  cont.appendChild(res);

  if (insigniasNuevas.length) {
    const cajaSellos = document.createElement('div');
    cajaSellos.className = 'insignias-reveladas';
    Badges.renderReveladas(insigniasNuevas, cajaSellos);
    cont.appendChild(cajaSellos);
  }

  const btn = document.createElement('button');
  btn.className = 'secundario';
  btn.textContent = 'Volver al camino';
  btn.addEventListener('click', () => renderizar());
  cont.appendChild(btn);
}

/* =================== Examen final de cluster (Fase 7) ================ */

/**
 * Muestra el panel del examen con el selector de dificultad antes de iniciarlo.
 * Se llama al pulsar el botón dentro del acordeón del cluster.
 */
function prepararExamenCluster(clusterId, clusterTitulo) {
  $('estudio-unidad').hidden = true;
  $('estudio-examen').hidden = true;
  const panel = $('estudio-examen-cluster');
  panel.hidden = false;
  $('examen-cluster-titulo').textContent = `Examen: ${clusterTitulo}`;

  const cont = $('examen-cluster-contenido');
  cont.innerHTML = '';

  let difSeleccionada = 'mixto';
  const difOpciones = [
    { valor: 'mixto', etiqueta: 'Mixto' },
    { valor: 'easy', etiqueta: 'Fácil' },
    { valor: 'medium', etiqueta: 'Medio' },
    { valor: 'hard', etiqueta: 'Difícil' },
  ];

  const wrapDif = document.createElement('div');
  wrapDif.className = 'quiz-dif-selector';
  const labelEl = document.createElement('span');
  labelEl.className = 'quiz-dif-label';
  labelEl.textContent = 'Nivel:';
  wrapDif.appendChild(labelEl);

  const msgVacio = document.createElement('p');
  msgVacio.className = 'quiz-dif-vacio';
  msgVacio.hidden = true;

  const btnIniciar = document.createElement('button');
  btnIniciar.className = 'primario';
  btnIniciar.textContent = 'Iniciar examen';

  difOpciones.forEach(({ valor, etiqueta }) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `quiz-dif-btn${valor === 'mixto' ? ' activo' : ''}`;
    btn.textContent = etiqueta;
    btn.dataset.valor = valor;
    btn.addEventListener('click', () => {
      difSeleccionada = valor;
      wrapDif.querySelectorAll('.quiz-dif-btn').forEach((b) =>
        b.classList.toggle('activo', b.dataset.valor === valor)
      );
      const pool = valor === 'mixto'
        ? getClusterQuestionPool(clusterId)
        : getClusterQuestionPool(clusterId).filter((q) => q.difficulty === valor);
      if (pool.length === 0) {
        btnIniciar.hidden = true;
        msgVacio.hidden = false;
        msgVacio.textContent =
          `Este cluster no tiene preguntas de nivel ${etiqueta}. Prueba otro nivel.`;
      } else {
        btnIniciar.hidden = false;
        msgVacio.hidden = true;
      }
    });
    wrapDif.appendChild(btn);
  });

  cont.append(wrapDif, msgVacio, btnIniciar);

  btnIniciar.addEventListener('click', () => {
    const pool = difSeleccionada === 'mixto'
      ? getClusterQuestionPool(clusterId)
      : getClusterQuestionPool(clusterId).filter((q) => q.difficulty === difSeleccionada);
    if (!pool.length) return;

    const barajado = barajar(pool.map((q) => q.id));
    const seleccionadas = barajado.slice(0, DEFAULT_CLUSTER_EXAM_SIZE);
    const nota = seleccionadas.length < DEFAULT_CLUSTER_EXAM_SIZE
      ? `Solo hay ${seleccionadas.length} pregunta(s) de este nivel en el cluster.`
      : null;

    update('estudio', (st) => {
      st.examenClusterEnCurso = {
        clusterId,
        clusterTitulo,
        preguntasIds: seleccionadas,
        dificultad: difSeleccionada,
        indice: 0,
        resultados: [],
      };
      return st;
    });
    renderExamenCluster(nota);
  });

  panel.scrollIntoView({ behavior: 'smooth' });
}

/** Pinta la pregunta actual del examen de cluster (mismo patrón que renderPreguntaQuiz). */
function renderExamenCluster(notaInicial) {
  const e = load('estudio');
  const ec = e.examenClusterEnCurso;
  if (!ec) return;

  const panel = $('estudio-examen-cluster');
  panel.hidden = false;
  $('estudio-unidad').hidden = true;
  $('estudio-examen').hidden = true;
  if (ec.clusterTitulo) $('examen-cluster-titulo').textContent = `Examen: ${ec.clusterTitulo}`;

  if (ec.indice >= ec.preguntasIds.length) {
    finalizarExamenCluster();
    return;
  }

  const pool = getClusterQuestionPool(ec.clusterId);
  const qid = ec.preguntasIds[ec.indice];
  const q = pool.find((b) => b.id === qid);
  if (!q) {
    // Pregunta no encontrada en el pool (no debería ocurrir): saltar
    update('estudio', (st) => { st.examenClusterEnCurso.indice += 1; return st; });
    renderExamenCluster();
    return;
  }

  const cont = $('examen-cluster-contenido');
  cont.innerHTML = '';

  if (notaInicial) {
    const nota = document.createElement('p');
    nota.className = 'nota-privacidad';
    nota.textContent = notaInicial;
    cont.appendChild(nota);
  }

  const head = document.createElement('p');
  head.className = 'quiz-progreso';
  head.textContent = `Pregunta · ${ec.indice + 1} de ${ec.preguntasIds.length}`;
  cont.appendChild(head);

  const enunciado = document.createElement('p');
  enunciado.className = 'quiz-enunciado';
  enunciado.innerHTML = renderInline(q.enunciado);
  cont.appendChild(enunciado);

  const ta = document.createElement('textarea');
  ta.className = 'textarea-corta';
  ta.placeholder = 'Responde desde la memoria, por escrito. El forcejeo es el aprendizaje.';
  cont.appendChild(ta);

  const pie = document.createElement('div');
  pie.className = 'textarea-pie';
  const contador = document.createElement('span');
  pie.appendChild(contador);
  cont.appendChild(pie);

  const btnRevelar = document.createElement('button');
  btnRevelar.className = 'primario';
  btnRevelar.textContent = 'Mostrar respuesta esperada';
  cont.appendChild(btnRevelar);

  const refrescarEstado = () => {
    const len = ta.value.trim().length;
    contador.textContent = `${len} / ${MIN_RESPUESTA_QUIZ} caracteres`;
    btnRevelar.disabled = len < MIN_RESPUESTA_QUIZ;
  };
  refrescarEstado();
  ta.addEventListener('input', refrescarEstado);

  btnRevelar.addEventListener('click', () => {
    btnRevelar.hidden = true;
    ta.readOnly = true;

    const sol = document.createElement('div');
    sol.className = 'quiz-solucion';
    const sp = document.createElement('p');
    sp.innerHTML = renderInline(q.solucion);
    sol.appendChild(sp);
    if (q.explicacion) {
      const ex = document.createElement('p');
      ex.className = 'quiz-explicacion';
      ex.innerHTML = renderInline(q.explicacion);
      sol.appendChild(ex);
    }
    cont.appendChild(sol);

    const fs = document.createElement('fieldset');
    fs.className = 'autoeval';
    fs.innerHTML =
      '<legend>Comparado con la respuesta esperada, ¿cómo estuvo la tuya?</legend>' +
      '<label><input type="radio" name="cluster-eval" value="bien" /> Lo tenía</label>' +
      '<label><input type="radio" name="cluster-eval" value="parcial" /> A medias</label>' +
      '<label><input type="radio" name="cluster-eval" value="mal" /> No lo tenía</label>';
    cont.appendChild(fs);

    const ec2 = load('estudio').examenClusterEnCurso;
    const btnSig = document.createElement('button');
    btnSig.className = 'primario';
    btnSig.textContent =
      ec2 && ec2.indice + 1 < ec2.preguntasIds.length ? 'Siguiente pregunta' : 'Cerrar examen';
    cont.appendChild(btnSig);

    btnSig.addEventListener('click', () => {
      const evalSel = cont.querySelector('input[name="cluster-eval"]:checked')?.value;
      if (!evalSel) return;
      update('estudio', (st) => {
        st.examenClusterEnCurso.resultados.push({ preguntaId: q.id, evaluacion: evalSel });
        st.examenClusterEnCurso.indice += 1;
        return st;
      });
      renderExamenCluster();
    });
  });
}

/** Cierra el examen de cluster: muestra resumen y limpia el estado. */
function finalizarExamenCluster() {
  const e = load('estudio');
  const ec = e.examenClusterEnCurso;
  if (!ec) return;

  const aciertos = ec.resultados.filter((r) => r.evaluacion === 'bien').length;
  const parciales = ec.resultados.filter((r) => r.evaluacion === 'parcial').length;
  const total = ec.resultados.length;

  update('estudio', (st) => {
    st.examenClusterEnCurso = null;
    return st;
  });
  marcarDiaEstudio();

  const cont = $('examen-cluster-contenido');
  cont.innerHTML = '';

  const res = document.createElement('p');
  res.className = 'quiz-enunciado';
  res.textContent =
    `Examen completado: ${aciertos}/${total} recordados completamente` +
    (parciales > 0 ? `, ${parciales} a medias.` : '.');
  cont.appendChild(res);

  const btn = document.createElement('button');
  btn.className = 'secundario';
  btn.textContent = 'Volver al roadmap';
  btn.addEventListener('click', () => {
    $('estudio-examen-cluster').hidden = true;
    renderizar();
  });
  cont.appendChild(btn);
}

/* ============================ Wiring inicial =========================== */

export function configurarUI() {
  $('btn-examen-iniciar').addEventListener('click', iniciarExamen);
  $('estudio-bloque-selector')?.addEventListener('change', (ev) => {
    bloqueVisible = datos.bloques.find((x) => x.id === ev.target.value) ?? null;
    renderizar();
  });
}
