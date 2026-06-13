/**
 * mentorChat.js — Chat socrático del mentor IA y superficies de foto.
 *
 * Extraído de app.js (oleada 5). El módulo recibe dos getters mediante
 * iniciar() para acceder al estado de navegación de app.js sin crear
 * un ciclo de importación: getVistaActual y getProblemaActual.
 *
 * Reglas pedagógicas que este módulo garantiza (§4.4, §0.7):
 *  - En modo 'forcejeo' el mentor JAMÁS revela ni confirma la solución.
 *  - El chat de forcejeo/revisión vive en la asignación y se archiva.
 *  - Los chats de estudio/general son efímeros (≤40 mensajes en memoria).
 *  - Las fotos NUNCA se persisten: viajan solo en la llamada a la API.
 *  - Sin cuenta de Claude activa, ninguna superficie de IA aparece.
 */

import * as Storage from './storage.js';
import * as Analytics from './analytics.js';
import * as Study from './study.js';
import * as MentorLocal from './mentorLocal.js';
import {
  mentorDisponible,
  chatMentor,
  prepararImagen,
  analizarFotoDesconstruccion,
  revisarIntento,
} from './aiMentor.js';

const $ = (id) => document.getElementById(id);

/* Getters inyectados por app.js (evitan ciclo de importación) */
let getVistaActual = () => 'sesion';
let getProblemaActual = () => null;

export function iniciar(cfg) {
  getVistaActual = cfg.getVistaActual;
  getProblemaActual = cfg.getProblemaActual;
}

/* ====================== Estado efímero del chat ======================= */

const chatsEfimeros = { estudio: [], entrevistador: [], general: [] };
let fotoMentorPendiente = null;

/* ====================== Modos y etiquetas UI ========================== */

const MENTOR_MODOS_UI = {
  forcejeo: {
    etiqueta: '· socrático, en pleno forcejeo',
    nota: 'El mentor pregunta y reenfoca; nunca revela ni confirma soluciones. La conversación se archiva con la sesión.',
  },
  revision: {
    etiqueta: '· revisión, mirando hacia atrás',
    nota: 'La solución ya está revelada: el mentor puede señalar dónde divergió tu camino.',
  },
  estudio: {
    etiqueta: '· modo estudio',
    nota: 'Explica lo ya leído con ejemplos nuevos; en quizzes y exámenes solo guía con preguntas.',
  },
  entrevistador: {
    etiqueta: '· entrevistador técnico',
    nota: 'Modo Arena: el mentor pregunta como entrevistador real; nunca revela ni confirma soluciones.',
  },
  general: {
    etiqueta: '· tu entrenamiento',
    nota: 'Conversa sobre tus métricas — siempre contra tu propio pasado, nunca contra nadie.',
  },
};

function modoMentor() {
  const vista = getVistaActual();
  if (vista === 'sesion') {
    const a = Storage.load('asignacion');
    if (a && !a.completado) return a.revelado ? 'revision' : 'forcejeo';
    return 'general';
  }
  if (vista !== 'estudio') return 'general';
  return Study.contextoEntrevista() ? 'entrevistador' : 'estudio';
}

function chatDeModo(modo) {
  if (modo === 'forcejeo' || modo === 'revision') return Storage.load('asignacion')?.chat ?? [];
  return chatsEfimeros[modo];
}

function guardarMensajeMentor(modo, msg) {
  if (modo === 'forcejeo' || modo === 'revision') {
    Storage.update('asignacion', (a) => {
      if (a) {
        a.chat = a.chat ?? [];
        a.chat.push(msg);
      }
      return a;
    });
  } else {
    const arr = chatsEfimeros[modo];
    arr.push(msg);
    if (arr.length > 40) arr.splice(0, arr.length - 40);
  }
}

function contextoMentor(modo) {
  if (modo === 'forcejeo' || modo === 'revision') {
    const a = Storage.load('asignacion');
    const p = getProblemaActual();
    if (!p) return '';
    const base =
      `Problema: ${p.enunciado}\n\n` +
      `Desconstrucción escrita por el usuario:\n${a?.desconstruccion || '(aún vacía)'}`;
    return modo === 'forcejeo'
      ? `${base}\n\nSolución de referencia (solo para tu contexto, JAMÁS la reveles ni la confirmes): ${p.solucion}`
      : `${base}\n\nSolución oficial (ya revelada al usuario): ${p.solucion}\n\nExplicación oficial: ${p.explicacion}`;
  }
  if (modo === 'entrevistador') {
    const ctx = Study.contextoEntrevista();
    if (!ctx) return 'El usuario está en la Arena de Entrevistas de Élite.';
    return ctx.examen
      ? `Entrevista simulada en el EXAMEN de la Arena. Problema en curso (JAMÁS reveles ni confirmes la solución): ${ctx.enunciado}`
      : `Entrevista simulada — ruta: ${ctx.ruta}. Unidad en estudio: «${ctx.titulo}».`;
  }
  if (modo === 'estudio') {
    const r = Study.progresoResumen();
    return r
      ? `Situación en el Modo Estudio — bloque actual: «${r.bloque}» (${r.unidadesHechas}/${r.unidadesTotal} unidades; examen ${r.examenAprobado ? 'aprobado' : 'pendiente'}; racha de estudio: ${r.racha} días).`
      : 'El usuario está en el Modo Estudio (lectura dirigida).';
  }
  const s = Analytics.resumen();
  return (
    `Resumen del entrenamiento del usuario (datos locales): ${s.total} sesiones, ` +
    `${s.tasaExito}% de éxito, ${s.tiempoProm} min promedio de forcejeo, ${s.hintsTotales} pistas usadas, ` +
    `${s.fichas} fichas completas en su cuaderno, racha actual de ${s.racha} días, nivel ${s.dificultadActual}` +
    (s.disparadores !== null ? `, ${s.disparadores}% de disparadores reconocidos en frío.` : '.')
  );
}

/* ====================== Superficies de IA ============================= */

/** Muestra u oculta TODAS las superficies de IA según cuenta y contexto. */
export function actualizarSuperficiesIA() {
  const ia = mentorDisponible();
  const a = Storage.load('asignacion');
  const forcejeo = Boolean(ia && a && !a.completado && !a.revelado);
  $('descon-foto-fila').hidden = !forcejeo;
  if (!forcejeo) $('descon-foto-resultado').hidden = true;
  $('revision-ia').hidden = !(ia && a && a.revelado && !a.completado);
  actualizarMentorUI();
}

export function actualizarMentorUI() {
  const modo = modoMentor();
  // El mentor local (RAG sobre la biblioteca) es útil SOLO en modo estudio
  // (TEORÍA). Así, un usuario sin Claude pero con backend local ve la burbuja
  // en Estudio; en forcejeo/Arena el chat sigue siendo de Claude (gating).
  const localUtil = MentorLocal.configurado() && modo === 'estudio';
  const ia = mentorDisponible() || localUtil;
  $('mentor-flotante').hidden = !ia;
  if (!ia) {
    $('mentor-panel').hidden = true;
    return;
  }
  $('mentor-modo').textContent = MENTOR_MODOS_UI[modo].etiqueta;
  $('mentor-nota').textContent = MENTOR_MODOS_UI[modo].nota;
  renderizarMentorMensajes(modo);
}

function renderizarMentorMensajes(modo) {
  const cont = $('mentor-mensajes');
  cont.innerHTML = '';
  chatDeModo(modo).forEach((m) => {
    const div = document.createElement('div');
    div.className = `chat-msg ${m.role === 'user' ? 'mio' : 'mentor'}`;
    div.textContent = m.content;
    cont.appendChild(div);
  });
  cont.scrollTop = cont.scrollHeight;
}

/* ====================== Chat flotante ================================= */

export async function enviarMensajeMentor() {
  const texto = $('mentor-entrada').value.trim();
  const modo = modoMentor();
  if (!texto && !fotoMentorPendiente) return;
  const foto = fotoMentorPendiente;
  fotoMentorPendiente = null;
  $('mentor-foto-chip').hidden = true;
  $('mentor-entrada').value = '';

  // El historial guarda SOLO texto: las fotos jamás se persisten.
  guardarMensajeMentor(modo, { role: 'user', content: (foto ? '📷 ' : '') + (texto || '(foto adjunta)') });
  renderizarMentorMensajes(modo);
  $('btn-mentor-enviar').disabled = true;
  $('mentor-chat-estado').textContent = 'El mentor está pensando…';
  try {
    const mensajes = chatDeModo(modo)
      .slice(-20)
      .map((m) => ({ role: m.role, content: m.content }));
    while (mensajes.length && mensajes[0].role !== 'user') mensajes.shift();
    if (foto) {
      mensajes[mensajes.length - 1].content = [
        foto,
        { type: 'text', text: texto || 'Te adjunto una foto de mi trabajo.' },
      ];
    }
    let respuesta = null;
    // En modo estudio (TEORÍA) y sin foto, intenta primero el mentor local
    // (RAG sobre la biblioteca). Si la laptop está apagada o falla, cae a
    // Claude; si tampoco hay Claude, queda el aviso de "no respondió".
    if (modo === 'estudio' && !foto && (await MentorLocal.disponible())) {
      const r = await MentorLocal.explicar({
        contexto_flujo: 'TEORIA',
        topic: '',
        difficulty: 1,
        problem_statement: '',
        user_desconstruccion: '',
        user_code_or_answer: '',
        error_message: '',
        user_question: texto || 'Explícame este tema apoyándote en la biblioteca.',
      });
      if (r?.answer) {
        respuesta = r.answer;
        const fuentes = [...new Set((r.retrieved_context ?? []).map((c) => c.fuente).filter(Boolean))].slice(0, 3);
        if (fuentes.length) respuesta += `\n\n— Apoyado en: ${fuentes.join(', ')}`;
      }
    }
    if (respuesta == null) {
      respuesta = await chatMentor(modo, contextoMentor(modo), mensajes);
    }
    if (respuesta) {
      guardarMensajeMentor(modo, { role: 'assistant', content: respuesta });
      $('mentor-chat-estado').textContent = '';
    } else {
      $('mentor-chat-estado').textContent = 'El mentor no respondió esta vez; tu trabajo sigue intacto.';
    }
  } catch (e) {
    Storage.registrarDiagnostico('mentor', e.message);
    $('mentor-chat-estado').textContent = 'No se pudo contactar al mentor (¿red o cuenta?).';
  }
  $('btn-mentor-enviar').disabled = false;
  renderizarMentorMensajes(modoMentor());
}

/**
 * Inicia un mensaje del mentor con una imagen de la pizarra adjunta.
 * Llamado desde configurarPizarra() en app.js.
 */
export function iniciarConFoto(jpegDataUrl) {
  fotoMentorPendiente = {
    type: 'image',
    source: { type: 'base64', media_type: 'image/jpeg', data: jpegDataUrl.split(',')[1] },
  };
  $('mentor-panel').hidden = false;
  actualizarMentorUI();
  $('mentor-entrada').value =
    'Te comparto mi pizarra con el proceso que llevo escrito a mano. Léela con cuidado y evalúa mi razonamiento.';
  enviarMensajeMentor();
}

export function configurarFlotante() {
  $('mentor-burbuja').addEventListener('click', () => {
    const panel = $('mentor-panel');
    panel.hidden = !panel.hidden;
    if (!panel.hidden) {
      actualizarMentorUI();
      $('mentor-entrada').focus();
    }
  });
  $('btn-mentor-cerrar').addEventListener('click', () => {
    $('mentor-panel').hidden = true;
  });
  $('btn-mentor-enviar').addEventListener('click', enviarMensajeMentor);
  $('mentor-entrada').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') enviarMensajeMentor();
  });
  $('btn-mentor-foto').addEventListener('click', () => $('input-mentor-foto').click());
  $('input-mentor-foto').addEventListener('change', async () => {
    const file = $('input-mentor-foto').files[0];
    $('input-mentor-foto').value = '';
    if (!file) return;
    try {
      fotoMentorPendiente = await prepararImagen(file);
      $('mentor-foto-chip').textContent = '📷 Foto lista — se enviará con tu próximo mensaje.';
      $('mentor-foto-chip').hidden = false;
    } catch {
      $('mentor-chat-estado').textContent = 'No se pudo leer esa imagen.';
    }
  });
}

/* ====== Foto de la desconstrucción en papel (forcejeo, IA opcional) === */

let transcripcionPendiente = null;

export function configurarFoto() {
  $('btn-descon-foto').addEventListener('click', () => $('input-descon-foto').click());
  $('input-descon-foto').addEventListener('change', async () => {
    const file = $('input-descon-foto').files[0];
    $('input-descon-foto').value = '';
    const p = getProblemaActual();
    if (!file || !p) return;
    $('descon-foto-estado').textContent = 'El mentor está leyendo tu hoja…';
    try {
      const imagen = await prepararImagen(file);
      const r = await analizarFotoDesconstruccion(p, imagen);
      if (r?.transcripcion) {
        transcripcionPendiente = r.transcripcion;
        $('descon-foto-transcripcion').textContent = r.transcripcion;
        $('descon-foto-observacion').textContent = r.observacion ?? '';
        $('descon-foto-resultado').hidden = false;
        $('descon-foto-estado').textContent = '';
      } else {
        $('descon-foto-estado').textContent = 'El mentor no pudo leer la hoja esta vez; intenta con más luz o de frente.';
      }
    } catch (e) {
      Storage.registrarDiagnostico('mentor', e.message);
      $('descon-foto-estado').textContent = 'No se pudo analizar la foto (¿red o cuenta?). Tu forcejeo sigue intacto.';
    }
  });

  $('btn-descon-foto-anadir').addEventListener('click', () => {
    if (!transcripcionPendiente) return;
    const ta = $('desconstruccion');
    ta.value =
      (ta.value ? `${ta.value.trimEnd()}\n\n` : '') +
      `— De mi hoja (transcrita por el mentor):\n${transcripcionPendiente}`;
    // Persiste en la asignación por la misma puerta que el tecleo normal
    ta.dispatchEvent(new Event('input'));
    transcripcionPendiente = null;
    $('descon-foto-resultado').hidden = true;
  });

  $('btn-descon-foto-descartar').addEventListener('click', () => {
    transcripcionPendiente = null;
    $('descon-foto-resultado').hidden = true;
  });
}

/* ===== Revisión del intento (SOLO tras el revelado, IA opcional) ====== */

let fotoRevisionPendiente = null;

export function configurarRevision() {
  $('btn-revision-foto').addEventListener('click', () => $('input-revision-foto').click());
  $('input-revision-foto').addEventListener('change', async () => {
    const file = $('input-revision-foto').files[0];
    $('input-revision-foto').value = '';
    if (!file) return;
    try {
      fotoRevisionPendiente = await prepararImagen(file);
      $('revision-estado').textContent = '📷 Foto de tu intento lista.';
    } catch {
      $('revision-estado').textContent = 'No se pudo leer esa imagen.';
    }
  });

  $('btn-revision-pedir').addEventListener('click', async () => {
    const a = Storage.load('asignacion');
    const p = getProblemaActual();
    if (!p || !a?.revelado) return; // gating pedagógico: jamás antes del revelado
    $('btn-revision-pedir').disabled = true;
    $('revision-estado').textContent = 'El mentor está comparando tu camino con la solución…';
    try {
      const resultado = await revisarIntento(p, {
        desconstruccion: a.desconstruccion ?? '',
        intentoTexto: $('reflexion-comparacion').value.trim(),
        imagen: fotoRevisionPendiente,
      });
      if (resultado) {
        $('revision-resultado').textContent = resultado;
        $('revision-resultado').hidden = false;
        $('revision-estado').textContent = '';
        // La revisión se archiva con la sesión (cps_sesionesArchivadas)
        Storage.update('asignacion', (x) => {
          if (x) x.revisionIA = resultado;
          return x;
        });
      } else {
        $('revision-estado').textContent = 'El mentor no respondió esta vez.';
      }
    } catch (e) {
      Storage.registrarDiagnostico('mentor', e.message);
      $('revision-estado').textContent = 'No se pudo pedir la revisión (¿red o cuenta?).';
    }
    fotoRevisionPendiente = null;
    $('btn-revision-pedir').disabled = false;
  });
}
