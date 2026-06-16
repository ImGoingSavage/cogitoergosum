/**
 * app.js — Orquestador principal de CogitoErgoSum.
 *
 * Flujo diario (marco de Pólya + Schoenfeld):
 *  1. Comprender   → enunciado sin etiquetas + desconstrucción obligatoria
 *  2. Planear      → timer configurable (20-120 min, pausable) con checkpoints
 *                    metacognitivos (~40% y ~80% del forcejeo) + hints
 *                    socráticos + predicción de jugada antes de revelar
 *  3. Ejecutar     → registro libre dentro de la desconstrucción
 *  4. Reflexionar  → ficha de moralejas (★moraleja + ★disparador, obligatorias),
 *                    comparación y transferencia; la estrategia real se revela
 *                    solo al cerrar (momento de aprendizaje explícito)
 *
 * Sostenibilidad del hábito (Constitución §0): piso mínimo de racha en días
 * sin energía, fresh start sereno al romperla (el logro nunca se borra),
 * insignias deterministas reveladas SOLO en pantallas de cierre.
 */

import * as Storage from './storage.js';
import * as Timer from './timer.js';
import * as Hints from './hintSystem.js';
import * as Engine from './adaptiveEngine.js';
import * as SR from './spacedRepetition.js';
import * as Analytics from './analytics.js';
import {
  mentorDisponible,
  listarCuentas,
  cuentaActiva,
  agregarCuenta,
  activarCuenta,
  eliminarCuenta,
  probarCuenta,
} from './aiMentor.js';
import * as Factory from './problemFactory.js';
import * as Study from './study.js';
import * as Badges from './badges.js';
import * as Avatar from './avatar.js';
import * as Api from './api.js';
import * as Sync from './sync.js';
import * as CuentaUI from './cuentaUI.js';
import * as MentorChat from './mentorChat.js';
import * as MentorLocal from './mentorLocal.js';
import * as Claustro from './claustro.js';
import { renderInline } from './markdown.js';
import * as Pizarra from './pizarra.js';

const MIN_DESCONSTRUCCION = 200;
const MIN_FICHA = 15;        // moraleja y disparador: al menos una frase corta
const MIN_PISO = 80;         // recall mínimo del piso de racha

/**
 * Checkpoints metacognitivos (Schoenfeld): al ~40% y ~80% del forcejeo se
 * externaliza el monitoreo (con 20 min: a los 8 y 16, la pauta del PDF).
 * Cada uno es visible durante dos minutos; se deriva del tiempo EFECTIVO
 * transcurrido, así que sobrevive a recargas y las pausas no lo saltan.
 */
const CHECKPOINT_TEXTOS = [
  'Detente y pregúntate en voz alta: ¿este camino está funcionando? ' +
    '¿Cuál es mi plan ahora mismo? ¿Debería probar otra cosa? ' +
    'Si llevas un rato cavando el mismo hoyo, sal de él.',
  '¿Qué sabes ahora que no sabías al empezar? Si el plan no avanza, ' +
    'cambia de representación: dibuja, prueba un caso pequeño o trabaja hacia atrás.',
];

function checkpointsActuales(duracionMin) {
  return [
    { desdeMin: duracionMin * 0.4, hastaMin: duracionMin * 0.4 + 2, texto: CHECKPOINT_TEXTOS[0] },
    { desdeMin: duracionMin * 0.8, hastaMin: duracionMin * 0.8 + 2, texto: CHECKPOINT_TEXTOS[1] },
  ];
}

const ETIQUETA_TIMER_DEFAULT = 'La solución se desbloquea al agotarse';
const ETIQUETA_TIMER_INCUBACION =
  'Timer cumplido. Si no lo has resuelto: levántate y aléjate un momento — muchas ideas llegan en la pausa.';
const ETIQUETA_TIMER_PAUSA = 'En pausa — tu forcejeo te espera.';

let problemas = [];
const $ = (id) => document.getElementById(id);

/* ============================== Arranque ============================== */

async function init() {
  Storage.migrarSiNecesario(); // migraciones de datos locales (no-op en v1)
  // Inyectar getters en los módulos antes de configurar la UI
  CuentaUI.iniciar(() => { renderizarSesion(); actualizarFreshStartUI(); });
  MentorChat.iniciar({ getVistaActual: () => vistaActual, getProblemaActual: problemaActual });
  // Consume el hash de retorno de Google OAuth ANTES de mostrar la portada:
  // si hay token, guardarSesion() lo persiste y la portada no se abre.
  const sesionOAuth = Api.manejarHashOAuth();
  configurarFondoVideo(); // el fondo vive aunque falle la carga de datos
  CuentaUI.configurarLogin(); // la portada también: no depende de los datos
  try {
    const res = await fetch('data/problems.json');
    // Pool de selección: problemas curados + variantes generadas por IA
    problemas = (await res.json()).problemas.concat(Factory.problemasGenerados());
  } catch {
    $('problema-enunciado').textContent =
      'No se pudo cargar la base de problemas. Sirve la aplicación por HTTP, por ejemplo: python3 -m http.server';
    return;
  }

  actualizarRacha();
  asegurarAsignacionDelDia();
  configurarNavegacion();
  configurarTimerUI();
  configurarMentorUI();
  configurarMentorLocalUI();
  configurarFactoryUI();
  configurarPisoMinimo();
  configurarFreshStart();
  CuentaUI.configurarCuenta();
  MentorChat.configurarFlotante();
  MentorChat.configurarFoto();
  MentorChat.configurarRevision();
  configurarPizarra();
  Claustro.init();
  Claustro.configurarUI();
  Sync.iniciar(); // sincronización opcional: no-op sin sesión o sin red
  // Una sincronización pudo unir progreso de otro dispositivo: refrescar
  // SOLO el header (repintar la sesión a mitad de un forcejeo molestaría).
  window.addEventListener('cps:sync-completada', () => Study.actualizarHeaderRachas());
  // Carga en paralelo: study.json, sellos y mapa del avatar
  await Promise.all([Study.init(), Badges.init(), Avatar.init()]);
  Study.configurarUI();
  // Contexto perezoso para los sellos (también desde study.js, sin ciclos)
  Badges.setContexto({
    problemas: () => problemas,
    bloquesEstudio: () => Study.bloques(),
  });
  Claustro.setProblemas(() => problemas);
  // "Pensar juntos": el claustro pide abrir el problema compartido como
  // sesión normal del camino 1 (bucle completo, sin atajos)
  window.addEventListener('cps:pj-atacar', (e) => {
    abrirProblemaCompartido(e.detail.problemId, e.detail.pjId);
  });
  // Retorno de Google OAuth: merge + sync (como si el usuario hubiese pulsado
  // "Entrar" — despuesDeEntrar() llama renderizarSesion, así que lo hacemos
  // antes del renderizarSesion() de abajo para no pintar dos veces).
  if (sesionOAuth) {
    await CuentaUI.despuesDeEntrar();
  } else {
    renderizarSesion();
    actualizarFreshStartUI();
  }
  cargarCita();
  registrarServiceWorker();
}

/* ===================== PWA y citas de la biblioteca ==================== */

/**
 * Fondo de video (§5.4 p.0). A 0.5× para que acompañe sin intervenir con la
 * atención; se pausa con la pestaña oculta (batería) y, con
 * prefers-reduced-motion, jamás se reproduce ni se descarga (preload="none"
 * y sin atributo autoplay): queda el póster estático precacheado.
 */
function configurarFondoVideo() {
  const video = $('fondo-video');
  if (!video) return;
  const reducido = window.matchMedia('(prefers-reduced-motion: reduce)');
  const ajustar = () => {
    if (reducido.matches || document.visibilityState === 'hidden') {
      video.pause();
      return;
    }
    video.defaultPlaybackRate = 0.5;
    video.playbackRate = 0.5;
    video.play().catch(() => {}); // si el navegador lo impide, queda el póster
  };
  // Algunos navegadores reinician el rate al cargar metadatos: reafirmarlo
  video.addEventListener('loadedmetadata', () => { video.playbackRate = 0.5; });
  document.addEventListener('visibilitychange', ajustar);
  reducido.addEventListener?.('change', ajustar);
  ajustar();
}

function registrarServiceWorker() {
  if (!('serviceWorker' in navigator)) return;
  navigator.serviceWorker.register('sw.js').catch(() => {
    // Sin SW (p. ej. file:// o navegador antiguo) la app funciona igual.
  });
  // Cuando una versión nueva del SW toma el control (VERSION cambió en
  // sw.js), recargar UNA vez para servir el shell fresco. Solo aplica si ya
  // había un SW controlando: la primera instalación no recarga nada.
  if (navigator.serviceWorker.controller) {
    let recargado = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (recargado) return;
      recargado = true;
      window.location.reload();
    });
  }
}

/** Cita curada del día (rotación determinista; serif, con autor). */
async function cargarCita() {
  try {
    const res = await fetch('data/quotes.json');
    const { citas } = await res.json();
    if (!citas?.length) return;
    const dia = Math.floor(Date.now() / 86400000);
    const cita = citas[dia % citas.length];
    $('cita-texto').textContent = `«${cita.texto}»`;
    $('cita-autor').textContent = cita.autor;
    $('pie-biblioteca').hidden = false;
  } catch {
    // El pie simplemente no aparece.
  }
}

/* ====================== Selección del problema ======================= */

function problemaActual() {
  const a = Storage.load('asignacion');
  return a ? problemas.find((p) => p.id === a.problemId) : null;
}

/**
 * Selecciona el problema del día:
 *  1. Prioriza revisiones espaciadas vencidas.
 *  2. Filtra por rango de dificultad adaptativa.
 *  3. Interleaving: evita repetir la estrategia de la sesión anterior.
 *  4. Evita repeticiones de problemas ya completados.
 */
function seleccionarProblema() {
  const historial = Storage.load('historial');
  const completados = new Set(historial.map((h) => h.problemId));
  const ultimaEstrategia = historial.at(-1)?.estrategia ?? null;

  // 1. Revisiones vencidas (la repetición espaciada gana a la novedad)
  const vencidas = SR.revisionesVencidas();
  if (vencidas.length > 0) {
    const candidatosRev = vencidas
      .map((id) => problemas.find((p) => p.id === id))
      .filter((p) => p && p.estrategia !== ultimaEstrategia);
    const elegido = candidatosRev[0] ?? problemas.find((p) => p.id === vencidas[0]);
    if (elegido) return { problema: elegido, esRevision: true };
  }

  // 2-4. Problemas nuevos en la zona de aprendizaje
  const { min, max, centro } = Engine.rangoSeleccion();
  let candidatos = problemas.filter(
    (p) =>
      !completados.has(p.id) &&
      p.dificultad >= min &&
      p.dificultad <= max &&
      p.estrategia !== ultimaEstrategia
  );

  // Relajación progresiva si el filtro vació el conjunto
  if (candidatos.length === 0) {
    candidatos = problemas.filter(
      (p) => !completados.has(p.id) && p.estrategia !== ultimaEstrategia
    );
  }
  if (candidatos.length === 0) {
    candidatos = problemas.filter((p) => !completados.has(p.id));
  }
  if (candidatos.length === 0) {
    // Biblioteca agotada: reciclar el problema más antiguo del historial
    candidatos = problemas;
  }

  // Preferir dificultad cercana al centro; desempate aleatorio
  candidatos.sort(
    (a, b) =>
      Math.abs(a.dificultad - centro) - Math.abs(b.dificultad - centro) ||
      Math.random() - 0.5
  );
  return { problema: candidatos[0], esRevision: false };
}

/**
 * Repaso por variantes (estilo Chessable): una revisión vencida entrena mejor
 * con una variante isomórfica que repitiendo el enunciado memorizado — se
 * ejercita el DISPARADOR, no la memoria. Si existe una variante de esa semilla
 * aún no trabajada, se presenta en lugar del original; si no, se usa el
 * original hoy y se genera una variante en segundo plano para que la PRÓXIMA
 * revisión sí la tenga (sin bloquear nunca el arranque de la sesión).
 */
function resolverProblemaDeRevision(original) {
  if (!mentorDisponible()) return { elegido: original, revisionDe: null };

  // Si lo que está en revisión ya es una variante, su familia isomórfica es la
  // de su semilla curada (nunca se generan variantes de variantes).
  const semillaId = original.origen === 'generado' ? original.semilla_id : original.id;

  const completados = new Set(Storage.load('historial').map((h) => h.problemId));
  const varianteLista = problemas.find(
    (p) => p.origen === 'generado' && p.semilla_id === semillaId && !completados.has(p.id)
  );
  if (varianteLista) return { elegido: varianteLista, revisionDe: original.id };

  const semilla = problemas.find((p) => p.id === semillaId);
  if (semilla && semilla.origen !== 'generado') {
    Factory.generarVariante(semilla).then((v) => {
      if (v) problemas.push(v);
    });
  }
  return { elegido: original, revisionDe: null };
}

function crearAsignacion() {
  const { problema, esRevision } = seleccionarProblema();
  const { elegido, revisionDe } = esRevision
    ? resolverProblemaDeRevision(problema)
    : { elegido: problema, revisionDe: null };

  Storage.save('asignacion', {
    problemId: elegido.id,
    fecha: Storage.hoy(),
    esRevision,
    revisionDe,
    timerInicio: Date.now(),
    timerCumplido: false,
    // §2.6: duración fija al iniciar (preferencia del usuario, 20-120 min);
    // solo puede extenderse en caliente, jamás recortarse.
    duracionMin: Timer.normalizarDuracion(Storage.load('preferencias')?.duracionTimer),
    pausadoEn: null,
    msPausadoTotal: 0,
    pausas: 0,
    desconstruccion: '',
    hintsUsados: [],
    prediccion: null,
    revelado: false,
    completado: false,
    pensarJuntosId: null,
  });
}

/**
 * "Pensar juntos" (§2.4): abre el problema compartido como asignación normal
 * del camino 1 — timer, desconstrucción, predicción y ficha intactos. Nunca
 * pisa un forcejeo vivo: si hay una sesión sin completar, primero se cierra.
 */
function abrirProblemaCompartido(problemId, pjId) {
  const a = Storage.load('asignacion');
  if (a && !a.completado) {
    $('claustro-msg').textContent =
      'Tienes una sesión de entrenamiento abierta: ciérrala primero y vuelve a intentarlo.';
    return;
  }
  const p = problemas.find((x) => x.id === problemId);
  if (!p) {
    $('claustro-msg').textContent = 'Ese problema no está en tu biblioteca local.';
    return;
  }
  Storage.save('asignacion', {
    problemId,
    fecha: Storage.hoy(),
    esRevision: false,
    revisionDe: null,
    timerInicio: Date.now(),
    timerCumplido: false,
    duracionMin: Timer.normalizarDuracion(Storage.load('preferencias')?.duracionTimer),
    pausadoEn: null,
    msPausadoTotal: 0,
    pausas: 0,
    desconstruccion: '',
    hintsUsados: [],
    prediccion: null,
    revelado: false,
    completado: false,
    pensarJuntosId: pjId,
  });
  resetearVistaSesion();
  renderizarSesion();
  cambiarVista('sesion');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function asegurarAsignacionDelDia() {
  const a = Storage.load('asignacion');

  // Asignación sin completar (de hoy o de un día anterior): se conserva
  if (a && !a.completado) return;
  // Asignación completada hoy: la sesión del día está cerrada; el usuario
  // puede abrir otra voluntariamente con "Entrenar otro problema"
  if (a && a.completado && a.fecha === Storage.hoy()) return;

  crearAsignacion();
}

/* ============================= Racha diaria =========================== */

function actualizarRacha() {
  const perfil = Storage.load('perfil');
  if (!perfil.ultimaSesion) return;
  const ayer = new Date();
  ayer.setDate(ayer.getDate() - 1);
  const mm = String(ayer.getMonth() + 1).padStart(2, '0');
  const dd = String(ayer.getDate()).padStart(2, '0');
  const fechaAyer = `${ayer.getFullYear()}-${mm}-${dd}`;
  // Si la última sesión no fue ni ayer ni hoy, la racha se rompe — pero
  // romperla nunca borra el logro (§2.2): la mejor racha queda en el estante
  // y se ofrece un fresh start sereno.
  if (perfil.ultimaSesion !== fechaAyer && perfil.ultimaSesion !== Storage.hoy()) {
    Storage.update('perfil', (p) => {
      if (p.racha > 0) {
        p.mejorRachaHistorica = Math.max(p.mejorRachaHistorica ?? 0, p.racha);
        p.freshStartPendiente = { rachaPerdida: p.racha };
      }
      p.racha = 0;
      return p;
    });
  }
}

/** Cuenta el día de hoy en la racha de entrenamiento (sesión o piso mínimo). */
function registrarDiaEntrenamiento() {
  Storage.update('perfil', (perfil) => {
    if (perfil.ultimaSesion !== Storage.hoy()) {
      perfil.racha += 1;
      perfil.ultimaSesion = Storage.hoy();
      perfil.mejorRachaHistorica = Math.max(perfil.mejorRachaHistorica ?? 0, perfil.racha);
    }
    return perfil;
  });
}

/* ===================== Fresh start y meta corta (§2.2) ================= */

function configurarFreshStart() {
  $('btn-freshstart-meta').addEventListener('click', () => {
    Storage.update('perfil', (p) => {
      p.metaCorta = { fechaInicio: Storage.hoy(), objetivo: 3 };
      p.freshStartPendiente = null;
      return p;
    });
    actualizarFreshStartUI();
  });
  $('btn-freshstart-cerrar').addEventListener('click', () => {
    Storage.update('perfil', (p) => {
      p.freshStartPendiente = null;
      return p;
    });
    actualizarFreshStartUI();
  });
}

function actualizarFreshStartUI() {
  const perfil = Storage.load('perfil');
  const pendiente = perfil.freshStartPendiente;
  $('seccion-freshstart').hidden = !pendiente;
  if (pendiente) {
    const mejor = Math.max(perfil.mejorRachaHistorica ?? 0, pendiente.rachaPerdida ?? 0);
    $('freshstart-texto').textContent =
      `Tu mejor racha fue de ${mejor} día(s) — está guardada en tu estante y nadie te la quita. ` +
      'Hoy empieza una nueva. Si quieres, márcate una meta corta: tres días seguidos, nada más.';
  }
}

/** Texto de racha para la pantalla de cierre, con meta corta si está activa. */
function textoRacha() {
  const perfil = Storage.load('perfil');
  let texto = `Racha: ${perfil.racha} día(s)`;
  const meta = perfil.metaCorta;
  if (meta) {
    if (perfil.racha >= (meta.objetivo ?? 3)) {
      Storage.update('perfil', (p) => {
        p.metaCorta = null;
        return p;
      });
      texto += ' · Meta corta cumplida — el hábito vuelve a estar de pie.';
    } else {
      texto += ` · Meta corta: ${perfil.racha}/${meta.objetivo ?? 3}`;
    }
  }
  return texto;
}

/* ============================ Render sesión =========================== */

function renderizarSesion() {
  const a = Storage.load('asignacion');
  const p = problemaActual();
  if (!a || !p) return;

  $('problema-titulo').textContent = p.titulo;
  $('problema-enunciado').innerHTML = renderInline(p.enunciado);
  $('problema-dificultad').innerHTML = '●'.repeat(p.dificultad) + '○'.repeat(5 - p.dificultad);
  $('badge-revision').hidden = !a.esRevision;
  $('guia-revision').hidden = !a.esRevision;

  // Desconstrucción
  const ta = $('desconstruccion');
  ta.value = a.desconstruccion ?? '';
  actualizarContador();

  // Predicción de jugada hecha previamente (sobrevive a recargas)
  document.querySelectorAll('input[name="prediccion"]').forEach((r) => {
    r.checked = r.value === a.prediccion;
  });

  // Hints ya solicitados
  $('hints-lista').innerHTML = '';
  a.hintsUsados.forEach((nivel) => {
    agregarHintAlDOM(nivel, p.hints[nivel - 1], 'estatico');
  });
  actualizarBotonHint();
  actualizarPisoUI();

  if (a.completado) {
    mostrarEstadoCompletado(p);
    return;
  }

  // Temporizador (tiempo EFECTIVO: las pausas lo congelan, nunca lo adelantan)
  Timer.asegurarInicio();
  actualizarTimerControles();
  Timer.iniciar(
    (ms, fraccion, pausado) => {
      // Si el forcejeo ya terminó (natural o manualmente), fijar display en 00:00
      if (Timer.cumplido()) {
        $('timer-display').textContent = '00:00';
        $('timer-progreso').style.width = '100%';
        return;
      }
      $('timer-display').textContent = Timer.formato(ms);
      $('timer-progreso').style.width = `${(fraccion * 100).toFixed(2)}%`;
      actualizarCheckpoint();
      actualizarEstadoBloqueo();
      if (pausado) $('timer-etiqueta').textContent = ETIQUETA_TIMER_PAUSA;
    },
    () => {
      $('timer-progreso').style.width = '100%';
      actualizarCheckpoint();
      actualizarEstadoBloqueo();
    }
  );

  if (a.revelado) revelarSolucion(true);
  actualizarEstadoBloqueo();
  MentorChat.actualizarSuperficiesIA();
}

let vistaActual = 'sesion';

/* ================= Controles del temporizador (§2.6) ================== */

function configurarTimerUI() {
  // Selector de duración para PRÓXIMOS forcejeos (preferencia persistente).
  // El mínimo no baja de 20: el piso de forcejeo no se negocia desde la UI.
  const sel = $('select-duracion');
  for (let m = Timer.DURACION_MINIMA_MIN; m <= Timer.DURACION_MAXIMA_MIN; m += Timer.PASO_MIN) {
    const opt = document.createElement('option');
    opt.value = String(m);
    opt.textContent = `${m} min`;
    sel.appendChild(opt);
  }
  sel.value = String(Timer.normalizarDuracion(Storage.load('preferencias')?.duracionTimer));
  sel.addEventListener('change', () => {
    const duracion = Timer.normalizarDuracion(sel.value);
    Storage.update('preferencias', (p) => {
      const prefs = p ?? {};
      prefs.duracionTimer = duracion;
      return prefs;
    });
    sel.value = String(duracion);
  });

  $('btn-timer-pausa').addEventListener('click', () => {
    if (Timer.enPausa()) Timer.reanudar();
    else Timer.pausar();
    actualizarTimerControles();
    actualizarCheckpoint();
    if (Timer.enPausa()) $('timer-etiqueta').textContent = ETIQUETA_TIMER_PAUSA;
  });

  $('btn-timer-extender').addEventListener('click', () => {
    Timer.extender(10); // extender nunca rompe el gating: solo pospone
    actualizarTimerControles();
  });

  $('btn-timer-terminar').addEventListener('click', terminarForcejeo);
}

function actualizarTimerControles() {
  const a = Storage.load('asignacion');
  const activo = Boolean(a && !a.revelado && !a.completado);
  $('btn-timer-pausa').hidden = !activo;
  $('btn-timer-extender').hidden = !activo;
  // "Listo" solo aparece mientras el forcejeo está en curso (no cumplido aún)
  $('btn-timer-terminar').hidden = !activo || Timer.cumplido();
  $('timer-sugerencia').textContent = '';
  if (!activo) return;

  const pausado = Timer.enPausa();
  $('btn-timer-pausa').textContent = pausado ? '▶' : '⏸';
  $('btn-timer-pausa').title = pausado
    ? 'Reanudar el forcejeo'
    : 'Pausar el cronómetro (pausar nunca adelanta el desbloqueo: solo lo pospone)';

  const dur = Timer.duracionMin();
  const btnExt = $('btn-timer-extender');
  btnExt.disabled = dur >= Timer.DURACION_MAXIMA_MIN;
  btnExt.textContent = btnExt.disabled ? 'Máx. 120 min' : '+10 min';

  // tiempo_estimado sugiere sin imponer (§2.6)
  const p = problemaActual();
  $('timer-sugerencia').textContent =
    p?.tiempo_estimado && p.tiempo_estimado !== dur
      ? `Esta sesión: ${dur} min. Este problema sugiere ~${p.tiempo_estimado} min.`
      : `Esta sesión: ${dur} min.`;
}

function terminarForcejeo() {
  const a = Storage.load('asignacion');
  if (!a || a.timerCumplido || a.revelado || a.completado) return;
  Storage.update('asignacion', (as) => {
    if (as) as.timerCumplido = true;
    return as;
  });
  $('timer-display').textContent = '00:00';
  $('timer-progreso').style.width = '100%';
  actualizarTimerControles();
  actualizarCheckpoint();
  actualizarEstadoBloqueo();
}

/* ============ Checkpoint metacognitivo (~40% y ~80%, efectivo) ========= */

function actualizarCheckpoint() {
  const a = Storage.load('asignacion');
  const caja = $('checkpoint-metacognitivo');
  const etiqueta = $('timer-etiqueta');

  if (!a || a.revelado || a.completado) {
    caja.hidden = true;
    etiqueta.textContent = ETIQUETA_TIMER_DEFAULT;
    return;
  }

  // Incubación: al cumplirse el timer (natural o manual), antes de revelar
  etiqueta.textContent = Timer.cumplido() ? ETIQUETA_TIMER_INCUBACION : ETIQUETA_TIMER_DEFAULT;

  // Calculado sobre tiempo efectivo: una pausa no salta el checkpoint
  const minTranscurridos = Timer.msTranscurridos() / 60000;
  const activo = checkpointsActuales(Timer.duracionMin()).find(
    (c) => minTranscurridos >= c.desdeMin && minTranscurridos < c.hastaMin
  );
  caja.hidden = !activo;
  if (activo) caja.querySelector('p').textContent = activo.texto;
}

/* ======================= Predicción de jugada ========================= */

function guardarPrediccion(valor) {
  Storage.update('asignacion', (a) => {
    if (a && !a.revelado && !a.completado) a.prediccion = valor;
    return a;
  });
  actualizarEstadoBloqueo();
}

/* ===================== Desconstrucción y bloqueo ====================== */

function actualizarContador() {
  const len = $('desconstruccion').value.length;
  const c = $('contador-caracteres');
  c.textContent = `${len} / ${MIN_DESCONSTRUCCION} caracteres`;
  c.classList.toggle('ok', len >= MIN_DESCONSTRUCCION);
}

function actualizarEstadoBloqueo() {
  const a = Storage.load('asignacion');
  if (!a || a.revelado || a.completado) return;

  const timerOk = Timer.cumplido();
  const desconOk = ($('desconstruccion').value.length) >= MIN_DESCONSTRUCCION;
  const predOk = Boolean(a.prediccion);
  const btn = $('btn-revelar');
  btn.disabled = !(timerOk && desconOk && predOk);

  const faltantes = [];
  if (!timerOk) faltantes.push('completar el tiempo de reflexión');
  if (!desconOk) faltantes.push(`escribir tu desconstrucción (mínimo ${MIN_DESCONSTRUCCION} caracteres)`);
  if (!predOk) faltantes.push('registrar tu predicción de jugada');
  $('bloqueo-mensaje').textContent = faltantes.length
    ? `Para revelar la solución falta: ${faltantes.join(', ')}.`
    : 'Solución disponible. Revélala solo cuando hayas agotado el forcejeo.';
}

let autosaveTimeout = null;
function autoguardarDesconstruccion() {
  actualizarContador();
  actualizarEstadoBloqueo();
  clearTimeout(autosaveTimeout);
  autosaveTimeout = setTimeout(() => {
    Storage.update('asignacion', (a) => {
      if (a) a.desconstruccion = $('desconstruccion').value;
      return a;
    });
    const s = $('autosave-indicador');
    s.textContent = 'Guardado';
    setTimeout(() => (s.textContent = ''), 1500);
  }, 400);
}

/* ============================== Hints ================================ */

function agregarHintAlDOM(nivel, texto, fuente) {
  const li = document.createElement('li');
  li.className = 'hint-item';
  li.innerHTML = `<span class="hint-nivel">Pista ${nivel}</span>${fuente === 'ia' ? '<span class="hint-ia">mentor IA</span>' : ''}<p></p>`;
  li.querySelector('p').innerHTML = renderInline(texto);
  $('hints-lista').appendChild(li);
}

function actualizarBotonHint() {
  const siguiente = Hints.siguienteNivel();
  const btn = $('btn-hint');
  if (siguiente === null) {
    btn.disabled = true;
    btn.textContent = 'No hay más pistas';
  } else {
    btn.disabled = false;
    btn.textContent = `Pedir pista ${siguiente} de 5 (−${Hints.PENALIZACION_POR_HINT} pts)`;
  }
}

async function pedirHint() {
  const p = problemaActual();
  if (!p) return;
  const btn = $('btn-hint');
  btn.disabled = true;
  btn.textContent = mentorDisponible() ? 'Consultando al mentor…' : 'Cargando…';
  const hint = await Hints.solicitarHint(p);
  if (hint) agregarHintAlDOM(hint.nivel, hint.texto, hint.fuente);
  actualizarBotonHint();
}

/* ========================= Revelar y reflexión ======================== */

function revelarSolucion(soloRender = false) {
  const p = problemaActual();
  if (!p) return;

  if (!soloRender) {
    Timer.reanudar(); // cierra una pausa abierta: el registro de pausas queda íntegro
    Storage.update('asignacion', (a) => {
      if (a) a.revelado = true;
      return a;
    });
  }
  actualizarTimerControles();
  MentorChat.actualizarSuperficiesIA(); // el mentor pasa a modo revisión; el chat se archiva con la sesión

  $('solucion-texto').innerHTML = renderInline(p.solucion);
  $('explicacion-texto').innerHTML = renderInline(p.explicacion);
  $('seccion-solucion').hidden = false;
  $('seccion-reflexion').hidden = false;
  $('btn-revelar').hidden = true;
  $('fieldset-prediccion').hidden = true;
  $('checkpoint-metacognitivo').hidden = true;
  $('timer-etiqueta').textContent = ETIQUETA_TIMER_DEFAULT;
  $('bloqueo-mensaje').textContent = '';
  $('seccion-solucion').scrollIntoView({ behavior: 'smooth' });
}

function completarSesion() {
  const a = Storage.load('asignacion');
  const p = problemaActual();
  if (!a || !p || a.completado) return;

  const autoevaluacion = document.querySelector('input[name="autoeval"]:checked')?.value;
  if (!autoevaluacion) {
    $('reflexion-error').textContent = 'Selecciona tu autoevaluación antes de cerrar la sesión.';
    return;
  }

  // Ficha del cuaderno: moraleja y disparador son obligatorios — ahí vive la
  // transferencia. Sin ficha no hay cierre de sesión.
  const moraleja = $('ficha-moraleja').value.trim();
  const disparador = $('ficha-disparador').value.trim();
  if (moraleja.length < MIN_FICHA || disparador.length < MIN_FICHA) {
    $('reflexion-error').textContent =
      'Tu ficha necesita una moraleja y un disparador (al menos una frase cada uno). ' +
      'Es el artefacto más valioso de la sesión.';
    return;
  }
  $('reflexion-error').textContent = '';

  // Tiempo EFECTIVO de forcejeo: las pausas no cuentan (§2.6)
  const tiempoMin = Math.round(Timer.msTranscurridos() / 60000);
  const msPausado = (a.msPausadoTotal ?? 0) + (a.pausadoEn ? Date.now() - a.pausadoEn : 0);
  const sesion = {
    autoevaluacion,
    hintsUsados: a.hintsUsados.length,
    desconstruccionLen: a.desconstruccion.length,
  };
  const score = Engine.calcularScore(sesion);

  // Historial (el uid permite unir historiales entre dispositivos, §5.2 C.4)
  const entrada = {
    uid: Storage.uidNuevo(),
    problemId: p.id,
    fecha: Storage.hoy(),
    score,
    hintsUsados: a.hintsUsados.length,
    tiempoMin,
    autoevaluacion,
    estrategia: p.estrategia,
    dificultad: p.dificultad,
    esRevision: Boolean(a.esRevision),
    revisionDe: a.revisionDe ?? null,
    prediccion: a.prediccion ?? null,
    moraleja,
    disparador,
    // Datos de proceso (alimentan sellos y Dashboard; jamás penalizan)
    desconstruccionLen: a.desconstruccion.length,
    duracionMin: a.duracionMin ?? Timer.DURACION_DEFECTO_MIN,
    pausas: a.pausas ?? 0,
    msPausado,
    incubada: Boolean(a.timerCumplido) && a.fecha !== Storage.hoy(),
    reflexion: {
      comparacion: $('reflexion-comparacion').value.trim(),
      transferencia: $('reflexion-transferencia').value.trim(),
    },
  };
  Storage.update('historial', (h) => {
    h.push(entrada);
    return h;
  });
  Storage.encolarEvento('sesion', entrada);

  // Pensar juntos: al cerrar, la entrega viaja al claustro (struggle first:
  // la del amigo solo será legible ahora que la tuya existe)
  if (a.pensarJuntosId) {
    Claustro.entregar(a.pensarJuntosId, {
      desconstruccion: a.desconstruccion,
      moraleja,
      disparador,
      fecha: Storage.hoy(),
    });
  }

  // Motor adaptativo
  const ajuste = Engine.ajustarDificultad({
    score,
    hintsUsados: a.hintsUsados.length,
    tiempoMin,
    tiempoEstimado: p.tiempo_estimado,
  });

  // Repetición espaciada: si la sesión fue una revisión presentada como
  // variante isomórfica, el resultado avanza (o reinicia) el ciclo del
  // problema ORIGINAL — la variante solo es el vehículo del repaso.
  SR.registrarResultado(a.revisionDe ?? p.id, {
    score,
    autoevaluacion,
    hintsUsados: a.hintsUsados.length,
  });

  // Racha (con mejor racha histórica, §2.2)
  registrarDiaEntrenamiento();

  const asignacionFinal = Storage.update('asignacion', (asig) => {
    if (asig) asig.completado = true;
    return asig;
  });

  // Archivo de trazabilidad: la asignación se sobrescribe al abrir otra
  // sesión, pero su copia completa queda registrada aquí.
  Storage.update('sesionesArchivadas', (arr) => {
    arr.push({ ...asignacionFinal, score });
    return arr;
  });

  // Sellos de la biblioteca: se evalúan SOLO al cierre (jamás interrumpen)
  const insigniasNuevas = Badges.evaluarYRegistrar();

  Timer.detener();
  mostrarResultado(score, ajuste, insigniasNuevas);
}

/**
 * Validación del proceso (§2.2): tras un fallo o avance parcial, nunca un
 * veredicto seco — se valida el esfuerzo con datos concretos y se reencuadra
 * hacia la siguiente oportunidad (el problema volverá vía repetición espaciada).
 */
function textoValidacionProceso(sesion) {
  if (!sesion || sesion.autoevaluacion === 'resuelto') return null;
  const datos = [];
  if (sesion.tiempoMin > 0) datos.push(`forcejeaste ${sesion.tiempoMin} min con un problema nivel ${sesion.dificultad}`);
  else datos.push(`te plantaste frente a un problema nivel ${sesion.dificultad}`);
  if ((sesion.desconstruccionLen ?? 0) > 0) datos.push(`dejaste ${sesion.desconstruccionLen} caracteres de pensamiento escrito`);
  const esfuerzo = datos.join(' y ');
  if (sesion.autoevaluacion === 'fallado') {
    return `No salió esta vez — y eso también es entrenamiento real: ${esfuerzo}. ` +
      'Este problema volverá a buscarte en unos días, quizá con otra cara, y tu ficha ya guarda la señal que faltaba.';
  }
  return `Avanzaste de verdad: ${esfuerzo}. Lo que quedó abierto volverá en revisión para terminar de asentarse.`;
}

/**
 * Momento de aprendizaje explícito (estilo Lichess): la estrategia se nombra
 * SOLO después de cerrar la sesión, junto con el veredicto de la predicción.
 */
function renderizarEstrategiaRevelada(sesionHistorial) {
  const estrategia = sesionHistorial?.estrategia;
  if (!estrategia || !Analytics.NOMBRES_ESTRATEGIA[estrategia]) {
    $('resultado-estrategia').textContent = '';
    $('resultado-prediccion').textContent = '';
    return;
  }

  $('resultado-estrategia').innerHTML = '';
  const b = document.createElement('strong');
  b.textContent = Analytics.NOMBRES_ESTRATEGIA[estrategia];
  $('resultado-estrategia').append(
    'Esto era ', b, ` — ${Analytics.DESCRIPCIONES_ESTRATEGIA[estrategia]}.`
  );

  const pred = sesionHistorial.prediccion;
  let veredicto = '';
  if (pred === estrategia) {
    veredicto = '✓ Tu predicción coincidió: reconociste el disparador en frío.';
  } else if (pred === 'nose') {
    veredicto = 'La jugada no se dejó ver a tiempo — el disparador que acabas de destilar es justo la señal a guardar.';
  } else if (pred) {
    veredicto = 'Predijiste otra jugada — vuelve a tu ficha: ¿qué señal del enunciado apuntaba aquí?';
  }
  $('resultado-prediccion').textContent = veredicto;
}

function mostrarResultado(score, ajuste, insigniasNuevas = []) {
  $('seccion-reflexion').hidden = true;
  $('seccion-resultado').hidden = false;
  $('resultado-score').textContent = score;
  const ultima = Storage.load('historial').at(-1);
  renderizarEstrategiaRevelada(ultima);

  // Validación del proceso (§2.2): dato + reencuadre, nunca veredicto seco
  const proceso = textoValidacionProceso(ultima);
  $('resultado-proceso').hidden = !proceso;
  $('resultado-proceso').textContent = proceso ?? '';

  let msg = `Dificultad: nivel ${ajuste.despues}`;
  if (ajuste.despues > ajuste.antes) msg += ' (sube — tu zona de aprendizaje creció)';
  else if (ajuste.despues < ajuste.antes) msg += ' (baja un nivel para consolidar la base — así entrenan también los olímpicos)';
  $('resultado-dificultad').textContent = msg;
  $('resultado-racha').textContent = textoRacha();

  // Revelado sobrio de sellos: solo aquí, en el cierre
  Badges.renderReveladas(insigniasNuevas, $('resultado-insignias'));

  Study.actualizarHeaderRachas();
  actualizarPisoUI();
  MentorChat.actualizarSuperficiesIA(); // sesión cerrada: el mentor pasa a modo general
}

function mostrarEstadoCompletado(p) {
  Timer.detener();
  $('timer-display').textContent = '—';
  $('timer-progreso').style.width = '100%';
  $('timer-etiqueta').textContent = ETIQUETA_TIMER_DEFAULT;
  $('checkpoint-metacognitivo').hidden = true;
  actualizarTimerControles();
  MentorChat.actualizarSuperficiesIA();
  $('btn-revelar').hidden = true;
  $('fieldset-prediccion').hidden = true;
  $('btn-hint').disabled = true;
  $('bloqueo-mensaje').textContent = '';
  $('solucion-texto').innerHTML = renderInline(p.solucion);
  $('explicacion-texto').innerHTML = renderInline(p.explicacion);
  $('seccion-solucion').hidden = false;
  $('seccion-resultado').hidden = false;
  const ultima = Storage.load('historial').at(-1);
  $('resultado-score').textContent = ultima?.score ?? '—';
  renderizarEstrategiaRevelada(ultima);
  $('resultado-proceso').hidden = true;
  $('resultado-insignias').innerHTML = '';
  $('resultado-dificultad').textContent =
    'Sesión de hoy completada. Vuelve mañana, o entrena otro problema si aún tienes energía.';
  $('resultado-racha').textContent = textoRacha();
}

/* ================== Sesiones adicionales del mismo día ================= */

/** Restaura la vista Sesión a su estado inicial para una nueva asignación. */
function resetearVistaSesion() {
  $('seccion-solucion').hidden = true;
  $('seccion-reflexion').hidden = true;
  $('seccion-resultado').hidden = true;
  $('btn-revelar').hidden = false;
  $('btn-revelar').disabled = true;
  $('fieldset-prediccion').hidden = false;
  $('btn-hint').disabled = false;
  $('hints-lista').innerHTML = '';
  $('checkpoint-metacognitivo').hidden = true;
  $('timer-etiqueta').textContent = ETIQUETA_TIMER_DEFAULT;
  $('resultado-proceso').hidden = true;
  $('resultado-insignias').innerHTML = '';
  $('descon-foto-resultado').hidden = true;
  $('descon-foto-estado').textContent = '';
  $('revision-ia').hidden = true;
  $('revision-resultado').hidden = true;
  $('revision-resultado').textContent = '';
  $('revision-estado').textContent = '';
  transcripcionPendiente = null;
  fotoRevisionPendiente = null;
  document.querySelectorAll('input[name="autoeval"]').forEach((r) => (r.checked = false));
  document.querySelectorAll('input[name="prediccion"]').forEach((r) => (r.checked = false));
  $('ficha-moraleja').value = '';
  $('ficha-disparador').value = '';
  $('reflexion-comparacion').value = '';
  $('reflexion-transferencia').value = '';
  $('reflexion-error').textContent = '';
  $('resultado-estrategia').textContent = '';
  $('resultado-prediccion').textContent = '';
}

/**
 * Abre una sesión adicional el mismo día (opcional, a voluntad del usuario).
 * La racha sigue contando por día (perfil.ultimaSesion) y el interleaving y
 * el motor adaptativo funcionan igual porque leen del historial.
 */
function entrenarOtroProblema() {
  const a = Storage.load('asignacion');
  if (!a?.completado) return;
  crearAsignacion();
  resetearVistaSesion();
  renderizarSesion();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ========================== Piso mínimo de racha ====================== */

/**
 * "Nunca dos días seguidos en cero": en días sin energía, un recall corto de
 * una ficha pasada (retrieval practice de la moraleja y su disparador)
 * conserva la cadena sin tocar el historial ni el motor adaptativo.
 */
let pisoRecuerdo = null;

function pisoDisponibleHoy() {
  const perfil = Storage.load('perfil');
  return perfil.ultimaSesion !== Storage.hoy() && Storage.load('historial').length > 0;
}

/** Prioriza fichas de sesiones débiles (ahí el recall rinde más). */
function elegirRecuerdoParaPiso() {
  const historial = Storage.load('historial');
  const conFicha = historial.filter((h) => h.moraleja);
  const debiles = conFicha.filter((h) => h.score < 50 || h.autoevaluacion === 'fallado');
  const grupo = debiles.length ? debiles : conFicha.length ? conFicha : historial;
  return grupo[Math.floor(Math.random() * grupo.length)] ?? null;
}

function actualizarPisoUI() {
  const disponible = pisoDisponibleHoy();
  $('piso-invitacion').hidden = !disponible;
  if (!disponible) $('seccion-piso').hidden = true;
}

function abrirPisoMinimo() {
  pisoRecuerdo = elegirRecuerdoParaPiso();
  if (!pisoRecuerdo) return;
  const p = problemas.find((x) => x.id === pisoRecuerdo.problemId);
  $('piso-titulo').textContent = p?.titulo ?? `Problema #${pisoRecuerdo.problemId}`;
  $('piso-enunciado').innerHTML = renderInline(p?.enunciado ?? '');
  $('piso-recuerdo').value = '';
  $('piso-contador').textContent = `0 / ${MIN_PISO} caracteres`;
  $('btn-piso-completar').disabled = true;
  $('piso-quiz').hidden = false;
  $('piso-ficha').hidden = true;
  $('piso-resultado').textContent = '';
  $('seccion-piso').hidden = false;
  $('seccion-piso').scrollIntoView({ behavior: 'smooth' });
}

function completarPisoMinimo() {
  if (!pisoRecuerdo) return;
  const recuerdo = $('piso-recuerdo').value.trim();
  if (recuerdo.length < MIN_PISO) return;

  const piso = {
    uid: Storage.uidNuevo(),
    fecha: Storage.hoy(),
    problemId: pisoRecuerdo.problemId,
    recuerdo,
  };
  Storage.update('pisosMinimos', (arr) => {
    arr.push(piso);
    return arr;
  });
  Storage.encolarEvento('piso', piso);
  registrarDiaEntrenamiento();

  // Feedback inmediato: la ficha original como autocomparación del recall
  const ficha = $('piso-ficha');
  ficha.innerHTML = '';
  if (pisoRecuerdo.moraleja || pisoRecuerdo.disparador) {
    const titulo = document.createElement('p');
    titulo.append('Tu ficha original — compárala con lo que recordaste:');
    ficha.appendChild(titulo);
    if (pisoRecuerdo.moraleja) {
      const m = document.createElement('p');
      const b = document.createElement('strong');
      b.textContent = '★ Moraleja: ';
      m.append(b, pisoRecuerdo.moraleja);
      ficha.appendChild(m);
    }
    if (pisoRecuerdo.disparador) {
      const d = document.createElement('p');
      const b = document.createElement('strong');
      b.textContent = '★ Disparador: ';
      d.append(b, pisoRecuerdo.disparador);
      ficha.appendChild(d);
    }
  } else {
    const p = problemas.find((x) => x.id === pisoRecuerdo.problemId);
    const e = document.createElement('p');
    e.innerHTML = renderInline(p?.explicacion ?? '');
    ficha.appendChild(e);
  }
  ficha.hidden = false;
  $('piso-quiz').hidden = true;
  $('piso-resultado').textContent =
    `Cadena conservada — racha de ${Storage.load('perfil').racha} día(s). ` +
    'La meta de hoy ya está cumplida; el problema del día te espera cuando quieras.';
  $('piso-invitacion').hidden = true;

  // El piso también puede ganar sellos (Piso firme, rachas): cierre de sesión
  Badges.renderReveladas(Badges.evaluarYRegistrar(), $('piso-insignias'));
  Study.actualizarHeaderRachas();
}

function configurarPisoMinimo() {
  $('btn-piso-abrir').addEventListener('click', abrirPisoMinimo);
  $('btn-piso-completar').addEventListener('click', completarPisoMinimo);
  $('piso-recuerdo').addEventListener('input', () => {
    const len = $('piso-recuerdo').value.trim().length;
    $('piso-contador').textContent = `${len} / ${MIN_PISO} caracteres`;
    $('btn-piso-completar').disabled = len < MIN_PISO;
  });
}

/* ============================= Dashboard ============================== */

function renderizarCuaderno() {
  const lista = $('cuaderno-lista');
  lista.innerHTML = '';
  const fichas = Analytics.cuadernoMoralejas();

  if (fichas.length === 0) {
    const vacio = document.createElement('p');
    vacio.className = 'cuaderno-vacio';
    vacio.textContent =
      'Aún no hay fichas. Cada sesión que cierres destilando moraleja y disparador aparecerá aquí.';
    lista.appendChild(vacio);
    return;
  }

  fichas.forEach((f) => {
    const p = problemas.find((x) => x.id === f.problemId);
    const item = document.createElement('div');
    item.className = 'ficha-cuaderno';

    const meta = document.createElement('div');
    meta.className = 'ficha-meta';
    const titulo = document.createElement('span');
    titulo.className = 'ficha-titulo';
    titulo.textContent = p?.titulo ?? `Problema #${f.problemId}`;
    const chip = document.createElement('span');
    chip.className = 'chip-estrategia';
    chip.textContent = Analytics.NOMBRES_ESTRATEGIA[f.estrategia] ?? f.estrategia;
    const fecha = document.createElement('span');
    fecha.className = 'ficha-fecha';
    fecha.textContent = f.fecha;
    meta.append(titulo, chip, fecha);
    item.appendChild(meta);

    [['★ Moraleja: ', f.moraleja], ['★ Disparador: ', f.disparador]].forEach(([rotulo, texto]) => {
      if (!texto) return;
      const linea = document.createElement('p');
      linea.className = 'ficha-linea';
      const b = document.createElement('strong');
      b.textContent = rotulo;
      linea.append(b, texto);
      item.appendChild(linea);
    });

    lista.appendChild(item);
  });
}

function renderizarDashboard() {
  const r = Analytics.resumen();
  const perfil = Storage.load('perfil');
  $('stat-resueltos').textContent = r.total;
  $('stat-exito').textContent = `${r.tasaExito}%`;
  $('stat-tiempo').textContent = `${r.tiempoProm} min`;
  $('stat-hints').textContent = r.hintsTotales;
  $('stat-racha').textContent = `${r.racha} 🔥`;
  $('stat-mejor-racha').textContent =
    `${Math.max(perfil.mejorRachaHistorica ?? 0, perfil.racha)} 🔥`;
  $('stat-dificultad').textContent = `Nivel ${r.dificultadActual}`;
  $('stat-disparadores').textContent = r.disparadores === null ? '—' : `${r.disparadores}%`;
  $('stat-fichas').textContent = r.fichas;

  // El pensador (avatar por capas) + rating privado por heurística
  Avatar.render($('avatar-figura'));
  renderizarRatingHeuristicas();

  // Mi estante: vitrina de sellos (las no ganadas, siluetas sin nombre)
  Badges.renderEstante($('estante-insignias'));

  // Progreso del camino 2 (Modo Estudio)
  const pe = Study.progresoResumen();
  const dash = $('dash-estudio');
  dash.innerHTML = '';
  const filas = pe
    ? [
        ['Bloque actual', pe.bloque],
        ['Unidades completadas', `${pe.unidadesHechas} de ${pe.unidadesTotal}`],
        ['Examen del bloque', pe.examenAprobado ? 'Aprobado' : pe.examenIntentos ? `${pe.examenIntentos} intento(s), pendiente` : 'Pendiente'],
        ['Racha de estudio', `${pe.racha} día(s)`],
      ]
    : [['Modo Estudio', 'Sin contenido cargado (data/study.json).']];
  filas.forEach(([k, v]) => {
    const p = document.createElement('p');
    p.className = 'fila';
    const b = document.createElement('strong');
    b.textContent = `${k}: `;
    p.append(b, v);
    dash.appendChild(p);
  });

  renderizarCuaderno();

  const { dominadas, debiles } = Analytics.estrategiasDominadasYDebiles();
  $('estrategias-dominadas').textContent = dominadas.length ? dominadas.join(', ') : 'Aún por descubrir';
  $('estrategias-debiles').textContent = debiles.length ? debiles.join(', ') : 'Ninguna detectada';

  const curva = $('chart-curva');
  curva.innerHTML = '';
  curva.appendChild(Analytics.svgCurvaDificultad());

  const barras = $('chart-estrategias');
  barras.innerHTML = '';
  barras.appendChild(Analytics.svgBarrasEstrategias());

  const diag = $('diagnostico-lista');
  diag.innerHTML = '';
  const avisos = Storage.load('diagnostico').slice(-15).reverse();
  if (!avisos.length) {
    const p = document.createElement('p');
    p.className = 'fila';
    p.textContent = 'Sin avisos registrados.';
    diag.appendChild(p);
  } else {
    avisos.forEach((d) => {
      const p = document.createElement('p');
      p.className = 'fila';
      p.textContent = `${d.ts.slice(0, 16).replace('T', ' ')} · ${d.origen} · ${d.mensaje}`;
      diag.appendChild(p);
    });
  }
}

/**
 * Rating por heurística (§2.5): nivel por estrategia, PRIVADO — compara al
 * usuario con su propio pasado. Umbral documentado en analytics.js.
 */
function renderizarRatingHeuristicas() {
  const cont = $('rating-heuristicas');
  cont.innerHTML = '';
  Analytics.ratingPorEstrategia().forEach((r) => {
    const fila = document.createElement('div');
    fila.className = 'rating-fila';
    const nombre = document.createElement('span');
    nombre.textContent = r.nombre;
    const valor = document.createElement('span');
    if (r.dominada) {
      valor.className = 'rating-dominada';
      valor.textContent = `Dominada · ${r.fechaDominio}`;
    } else if (r.nivel !== null) {
      valor.textContent = `Nivel ${r.nivel} · ${r.sesiones} sesión(es)`;
    } else {
      valor.textContent = 'Aún sin sesiones';
    }
    fila.append(nombre, valor);
    cont.appendChild(fila);
  });
}

/* ====================== Navegación y mentor UI ======================== */

function configurarNavegacion() {
  $('nav-sesion').addEventListener('click', () => cambiarVista('sesion'));
  $('nav-estudio').addEventListener('click', () => {
    Study.renderizar();
    cambiarVista('estudio');
  });
  $('nav-claustro').addEventListener('click', () => {
    Claustro.renderizar();
    cambiarVista('claustro');
  });
  $('nav-dashboard').addEventListener('click', () => {
    renderizarDashboard();
    cambiarVista('dashboard');
  });

  $('desconstruccion').addEventListener('input', autoguardarDesconstruccion);
  $('btn-hint').addEventListener('click', pedirHint);
  $('btn-revelar').addEventListener('click', () => revelarSolucion());
  $('btn-completar').addEventListener('click', completarSesion);
  $('btn-otro-problema').addEventListener('click', entrenarOtroProblema);

  document.querySelectorAll('input[name="prediccion"]').forEach((r) =>
    r.addEventListener('change', () => guardarPrediccion(r.value))
  );
}

function cambiarVista(vista) {
  vistaActual = vista;
  ['sesion', 'estudio', 'claustro', 'dashboard'].forEach((v) => {
    $(`vista-${v}`).hidden = vista !== v;
    $(`nav-${v}`).classList.toggle('activo', vista === v);
  });
  MentorChat.actualizarMentorUI(); // el mentor flotante cambia de modo según la vista
  Pizarra.actualizarVisibilidad(vista); // la pizarra vive en sesión y estudio
}

/**
 * Pizarra a mano alzada (pedido 2026-06-11): el contexto decide QUÉ pizarra
 * se abre — la del problema del día, la de la unidad de estudio abierta o
 * la del examen en curso. Cada una persiste por separado en el dispositivo.
 */
function configurarPizarra() {
  Pizarra.init();
  // Evaluar con el mentor (pedido 2026-06-11): la página de la pizarra
  // viaja como imagen al chat socrático. El botón solo existe con cuenta
  // de Claude activa (§0.7); el MODO del chat ya protege el gating —
  // durante el forcejeo el mentor pregunta y orienta, jamás confirma.
  Pizarra.configurarMentor({
    disponible: mentorDisponible,
    evaluar: (jpegDataUrl) => MentorChat.iniciarConFoto(jpegDataUrl),
  });
  Pizarra.setContexto(() => {
    if (vistaActual === 'sesion') {
      const a = Storage.load('asignacion');
      if (a?.problemId != null) {
        const p = problemas.find((x) => x.id === a.problemId);
        return {
          clave: `problema-${a.problemId}`,
          titulo: p ? `Pizarra — ${p.titulo}` : 'Pizarra del problema',
        };
      }
      return { clave: 'entrenamiento', titulo: 'Pizarra de entrenamiento' };
    }
    const e = Storage.load('estudio');
    if (e.examenEnCurso) {
      return { clave: `examen-${e.examenEnCurso.bloqueId}`, titulo: 'Pizarra — examen del bloque' };
    }
    const panel = $('estudio-unidad');
    if (panel && !panel.hidden && panel.dataset.unidad) {
      return { clave: `unidad-${panel.dataset.unidad}`, titulo: 'Pizarra — unidad de estudio' };
    }
    return { clave: 'estudio', titulo: 'Pizarra de estudio' };
  });
  Pizarra.actualizarVisibilidad(vistaActual);
}

function renderizarCuentas() {
  const ul = $('mentor-cuentas');
  ul.innerHTML = '';
  const activa = cuentaActiva();

  listarCuentas().forEach((c) => {
    const li = document.createElement('li');
    li.className = 'cuenta-item';
    li.innerHTML =
      '<label><input type="radio" name="cuenta-activa" /> <span class="cuenta-nombre"></span> <span class="cuenta-key"></span></label>' +
      '<button class="cuenta-borrar" title="Eliminar cuenta">✕</button>';
    li.querySelector('input').checked = activa?.id === c.id;
    li.querySelector('.cuenta-nombre').textContent = c.nombre;
    li.querySelector('.cuenta-key').textContent = `····${c.apiKey.slice(-4)}`;
    li.querySelector('input').addEventListener('change', () => {
      activarCuenta(c.id);
      renderizarCuentas();
    });
    li.querySelector('.cuenta-borrar').addEventListener('click', () => {
      eliminarCuenta(c.id);
      renderizarCuentas();
    });
    ul.appendChild(li);
  });

  $('mentor-estado').textContent = mentorDisponible()
    ? `Mentor IA activo — cuenta en uso: ${cuentaActiva().nombre}`
    : 'Mentor IA inactivo (hints curados). Agrega una cuenta para activarlo.';

  // Agregar/quitar la cuenta enciende o apaga TODAS las superficies de IA
  MentorChat.actualizarSuperficiesIA();
}

function configurarMentorUI() {
  renderizarCuentas();
  $('btn-cuenta-agregar').addEventListener('click', () => {
    const creada = agregarCuenta($('cuenta-nombre').value, $('cuenta-apikey').value);
    if (creada) {
      $('cuenta-nombre').value = '';
      $('cuenta-apikey').value = '';
      renderizarCuentas();
      if (!creada.apiKey.startsWith('sk-ant-')) {
        $('mentor-estado').textContent =
          'Aviso: la key no empieza con sk-ant- — verifica que sea una API key de la Console (no una contraseña de claude.ai). Usa «Probar la cuenta».';
      }
    }
  });
  $('btn-cuenta-probar').addEventListener('click', async () => {
    $('mentor-estado').textContent = 'Probando la cuenta…';
    const r = await probarCuenta();
    $('mentor-estado').textContent = r.mensaje;
  });
}

/* ============ Mentor local opcional (backend RAG, mentorLocal.js) ========= */

function configurarMentorLocalUI() {
  const cfg = Storage.load('mentorLocal') ?? { habilitado: false, url: '', serviceToken: '' };
  $('local-habilitado').checked = Boolean(cfg.habilitado);
  $('local-url').value = cfg.url ?? '';
  $('local-token').value = cfg.serviceToken ?? '';

  $('btn-local-guardar').addEventListener('click', () => {
    Storage.save('mentorLocal', {
      habilitado: $('local-habilitado').checked,
      url: $('local-url').value.trim(),
      serviceToken: $('local-token').value,
    });
    $('local-estado').textContent = 'Guardado. Usa «Probar conexión» para verificar.';
    MentorChat.actualizarMentorUI(); // la burbuja puede aparecer/ocultarse
  });

  $('btn-local-probar').addEventListener('click', async () => {
    $('local-estado').textContent = 'Probando…';
    const r = await MentorLocal.probar();
    $('local-estado').textContent = r.mensaje;
  });
}

/* ================ Portada de inicio de sesión (login) ================= */
/* Portada + tarjeta "Mi cuenta" → cuentaUI.js (CuentaUI.configurarLogin /
   CuentaUI.configurarCuenta / CuentaUI.despuesDeEntrar / CuentaUI.abrirPortada) */

/* ===================== Generador de variantes IA ====================== */

/**
 * Elige la semilla para una variante isomórfica. Prioriza problemas que
 * el usuario trabajó con dificultades (ahí la transferencia rinde más);
 * solo usa semillas curadas, nunca variantes de variantes.
 * La elección jamás se revela al usuario.
 */
function elegirSemillaParaVariante() {
  const estaticos = problemas.filter((p) => p.origen !== 'generado');
  const historial = Storage.load('historial');
  const trabajados = new Set(historial.map((h) => h.problemId));
  const debiles = new Set(
    historial
      .filter((h) => h.score < 50 || h.autoevaluacion === 'fallado')
      .map((h) => h.problemId)
  );

  const porPrioridad = [
    estaticos.filter((p) => debiles.has(p.id)),
    estaticos.filter((p) => trabajados.has(p.id)),
    estaticos,
  ].find((grupo) => grupo.length > 0);

  return porPrioridad[Math.floor(Math.random() * porPrioridad.length)] ?? null;
}

async function generarVarianteUI() {
  const btn = $('btn-generar-variante');
  const estado = $('factory-estado');

  if (!mentorDisponible()) {
    estado.textContent = 'Necesitas una cuenta de Claude activa (configúrala abajo).';
    return;
  }

  btn.disabled = true;
  estado.textContent = 'Generando variante… puede tardar un par de minutos.';

  const variante = await Factory.generarVariante(elegirSemillaParaVariante());

  if (variante) {
    problemas.push(variante);
    estado.textContent = 'Variante añadida a tu biblioteca. Aparecerá en una sesión futura.';
  } else {
    estado.textContent = 'No se pudo generar la variante. Revisa tu cuenta o intenta más tarde.';
  }
  $('factory-contador').textContent = Factory.problemasGenerados().length;
  btn.disabled = false;
}

function configurarFactoryUI() {
  $('factory-contador').textContent = Factory.problemasGenerados().length;
  $('btn-generar-variante').addEventListener('click', generarVarianteUI);
}

document.addEventListener('DOMContentLoaded', init);
