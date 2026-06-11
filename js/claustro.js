/**
 * claustro.js — La capa social de CogitoErgoSum (Fase D, HANDOFFCES §2.4).
 *
 * "La red de amigos existe para compartir una pasión, no para establecer
 * dominancia intelectual" (Constitución §0.4). Reglas duras:
 *  - Amistades simétricas SOLO por código de invitación (sin sugerencias).
 *  - Lo único visible de un amigo: su vitrina (avatar, sellos ganados,
 *    rachas y mejor racha, y la moraleja que ÉL decida compartir).
 *    Jamás: actividad en tiempo real, qué problema hace, puntajes.
 *  - Única interacción: el reconocimiento ❧ (uno por sello por amigo;
 *    el UNIQUE del esquema impide que se vuelva contador de popularidad).
 *  - Todo es opt-in; la app es 100% funcional sin cuenta y sin amigos.
 *
 * Preferencias locales en cps_claustro: { username, fichaCompartidaUid }
 * (viaja en CLAVES_SYNC para que ambos dispositivos compartan la elección).
 */

import * as Storage from './storage.js';
import * as Api from './api.js';
import * as Badges from './badges.js';
import * as Avatar from './avatar.js';
import { NOMBRES_ESTRATEGIA } from './analytics.js';

const $ = (id) => document.getElementById(id);

let amigosCache = []; // [{amistadId, userId, username, vitrina}]

/* ========================= Vitrina propia ============================= */

function fichaCompartida() {
  const uid = Storage.load('claustro').fichaCompartidaUid;
  if (!uid) return null;
  const h = Storage.load('historial').find((x) => (x.uid ?? `${x.problemId}|${x.fecha}`) === uid);
  if (!h) return null;
  return {
    moraleja: h.moraleja,
    disparador: h.disparador,
    estrategia: NOMBRES_ESTRATEGIA[h.estrategia] ?? h.estrategia,
    fecha: h.fecha,
  };
}

/**
 * Lo ÚNICO que se publica de este usuario. Nada de puntajes, conteos de
 * problemas ni actividad: avatar, sellos, rachas y moraleja opt-in.
 */
function construirVitrina() {
  const perfil = Storage.load('perfil');
  const estudio = Storage.load('estudio');
  const ganadas = Badges.ganadas();
  return {
    rachas: {
      practica: perfil.racha ?? 0,
      mejorPractica: Math.max(perfil.mejorRachaHistorica ?? 0, perfil.racha ?? 0),
      estudio: estudio.rachaEstudio ?? 0,
      mejorEstudio: Math.max(estudio.mejorRachaEstudio ?? 0, estudio.rachaEstudio ?? 0),
    },
    insignias: Object.entries(ganadas).map(([id, r]) => ({
      id,
      fecha: r.fecha,
      contador: r.contador ?? 1,
    })),
    capas: Avatar.capasGanadas(),
    moraleja: fichaCompartida(),
  };
}

let publicando = false;

/** Sube la vitrina si el claustro está habilitado. Silencioso ante fallos. */
export async function publicarVitrina() {
  const { username } = Storage.load('claustro');
  if (!username || !Api.sesionActual() || publicando) return;
  publicando = true;
  try {
    await Api.publicarPerfil(username, construirVitrina());
  } catch {
    // Se reintentará en la próxima sincronización o visita al claustro.
  } finally {
    publicando = false;
  }
}

/* ============================ Arranque ================================ */

export function init() {
  // La vitrina se refresca sola después de cada sincronización exitosa
  window.addEventListener('cps:sync-completada', () => publicarVitrina());
}

export function configurarUI() {
  $('btn-claustro-crear').addEventListener('click', crearPerfil);
  $('btn-claustro-invitar').addEventListener('click', generarInvitacion);
  $('btn-claustro-canjear').addEventListener('click', canjearCodigo);
  $('btn-claustro-compartir').addEventListener('click', compartirFicha);
  $('btn-claustro-descompartir').addEventListener('click', descompartirFicha);
  $('btn-vitrina-cerrar').addEventListener('click', () => {
    $('claustro-vitrina').hidden = true;
  });
}

/* ====================== Render de la vista =========================== */

export async function renderizar() {
  const sesion = Api.sesionActual();
  const { username } = Storage.load('claustro');

  $('claustro-sin-cuenta').hidden = Boolean(sesion);
  $('claustro-sin-nombre').hidden = !sesion || Boolean(username);
  $('claustro-amigos').hidden = !sesion || !username;
  $('claustro-compartir').hidden = !sesion || !username;
  $('claustro-notifs').hidden = true;
  $('claustro-vitrina').hidden = true;
  if (!sesion || !username) return;

  $('claustro-mi-nombre').textContent = username;
  renderizarSelectorFicha();
  publicarVitrina();

  try {
    await Promise.all([renderizarAmigos(), renderizarReconocimientos()]);
  } catch {
    $('claustro-msg').textContent =
      'No se pudo consultar el claustro (¿sin conexión?). Tu entrenamiento no depende de esto.';
  }
}

/* ------------------------- Crear perfil ------------------------------ */

async function crearPerfil() {
  const nombre = $('claustro-username').value.trim();
  if (nombre.length < 3 || nombre.length > 24) {
    $('claustro-crear-msg').textContent = 'El nombre necesita entre 3 y 24 caracteres.';
    return;
  }
  $('claustro-crear-msg').textContent = 'Creando tu lugar en el claustro…';
  try {
    await Api.publicarPerfil(nombre, construirVitrina());
    Storage.update('claustro', (c) => {
      c.username = nombre;
      return c;
    });
    $('claustro-crear-msg').textContent = '';
    renderizar();
  } catch (e) {
    $('claustro-crear-msg').textContent = /duplicate|unique/i.test(e.message)
      ? 'Ese nombre ya está tomado: prueba otro.'
      : `No se pudo crear el perfil: ${e.message}`;
  }
}

/* ------------------------ Invitaciones ------------------------------- */

function codigoNuevo() {
  // Legible y suficiente: CES- + 8 caracteres alfanuméricos en mayúsculas
  const alfabeto = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
  let cuerpo = '';
  const aleatorio = new Uint32Array(8);
  crypto.getRandomValues(aleatorio);
  aleatorio.forEach((n) => {
    cuerpo += alfabeto[n % alfabeto.length];
  });
  return `CES-${cuerpo}`;
}

async function generarInvitacion() {
  $('claustro-codigo').textContent = 'Generando código…';
  try {
    const codigo = await Api.crearInvitacion(codigoNuevo());
    $('claustro-codigo').textContent =
      `Tu código: ${codigo} — compártelo con UNA persona; al canjearlo quedan vinculados.`;
  } catch (e) {
    $('claustro-codigo').textContent = `No se pudo generar: ${e.message}`;
  }
}

async function canjearCodigo() {
  const codigo = $('claustro-canje').value.trim();
  if (!codigo) return;
  $('claustro-msg').textContent = 'Canjeando…';
  try {
    const nombre = await Api.canjearInvitacion(codigo);
    $('claustro-canje').value = '';
    $('claustro-msg').textContent = `Vínculo creado con ${nombre}. Bienvenido al claustro.`;
    await renderizarAmigos();
  } catch (e) {
    $('claustro-msg').textContent = e.message.replace(/^API \d+:\s*/, '').slice(0, 160);
  }
}

/* ------------------------ Lista de amigos ---------------------------- */

async function renderizarAmigos() {
  const sesion = Api.sesionActual();
  const amistades = await Api.listarAmistades();
  const ids = amistades.map((a) => (a.user_a === sesion.userId ? a.user_b : a.user_a));
  const perfiles = await Api.perfilesDe(ids);
  amigosCache = amistades.map((a) => {
    const userId = a.user_a === sesion.userId ? a.user_b : a.user_a;
    const p = perfiles.find((x) => x.user_id === userId);
    return { amistadId: a.id, userId, username: p?.username ?? '(sin nombre aún)', vitrina: p?.vitrina ?? {} };
  });

  const ul = $('claustro-amigos-lista');
  ul.innerHTML = '';
  $('claustro-amigos-vacio').hidden = amigosCache.length > 0;
  amigosCache.forEach((amigo) => {
    const li = document.createElement('li');
    li.className = 'unidad-item';
    const btn = document.createElement('button');
    btn.className = 'unidad-boton';
    btn.innerHTML = '<span class="unidad-estado">❧</span><span class="unidad-nombre"></span>';
    btn.querySelector('.unidad-nombre').textContent = amigo.username;
    btn.addEventListener('click', () => abrirVitrina(amigo));
    li.appendChild(btn);
    ul.appendChild(li);
  });
}

/* ---------------------- Vitrina de un amigo -------------------------- */

async function abrirVitrina(amigo) {
  const v = amigo.vitrina ?? {};
  $('claustro-vitrina').hidden = false;
  $('vitrina-nombre').textContent = amigo.username;

  // Rachas: el logro sostenido del par, presentado como inspiración
  const rachas = $('vitrina-rachas');
  rachas.innerHTML = '';
  const r = v.rachas ?? {};
  [
    [`🔥 ${r.practica ?? 0}`, 'Racha de entrenamiento'],
    [`📘 ${r.estudio ?? 0}`, 'Racha de estudio'],
    [`Mejor: ${Math.max(r.mejorPractica ?? 0, r.practica ?? 0)} 🔥 · ${Math.max(r.mejorEstudio ?? 0, r.estudio ?? 0)} 📘`, 'Mejores rachas'],
  ].forEach(([texto, titulo]) => {
    const chip = document.createElement('span');
    chip.className = 'racha-chip';
    chip.title = titulo;
    chip.textContent = texto;
    rachas.appendChild(chip);
  });

  Avatar.renderDesdeCapas($('vitrina-avatar'), v.capas ?? [], amigo.username);

  // Moraleja de la semana (solo si el amigo decidió compartirla)
  const cajaMoraleja = $('vitrina-moraleja');
  if (v.moraleja?.moraleja) {
    cajaMoraleja.hidden = false;
    cajaMoraleja.innerHTML = '';
    const titulo = document.createElement('p');
    titulo.append(`Su moraleja de la semana (${v.moraleja.estrategia ?? ''} · ${v.moraleja.fecha ?? ''}):`);
    const m = document.createElement('p');
    const bm = document.createElement('strong');
    bm.textContent = '★ Moraleja: ';
    m.append(bm, v.moraleja.moraleja);
    cajaMoraleja.append(titulo, m);
    if (v.moraleja.disparador) {
      const d = document.createElement('p');
      const bd = document.createElement('strong');
      bd.textContent = '★ Disparador: ';
      d.append(bd, v.moraleja.disparador);
      cajaMoraleja.appendChild(d);
    }
  } else {
    cajaMoraleja.hidden = true;
  }

  // Estante del amigo: SOLO sellos ganados (lo no ganado es privado), con ❧
  const yaReconocidas = new Set(
    (await Api.reconocimientosHechosA(amigo.userId).catch(() => [])).map((x) => x.insignia_id)
  );
  const estante = $('vitrina-insignias');
  estante.innerHTML = '';
  const insignias = v.insignias ?? [];
  if (!insignias.length) {
    const vacio = document.createElement('p');
    vacio.className = 'cuaderno-vacio';
    vacio.textContent = 'Su estante aún está empezando — como empezamos todos.';
    estante.appendChild(vacio);
  }
  insignias.forEach(({ id, fecha, contador }) => {
    const def = Badges.definicion(id);
    if (!def) return;
    const card = document.createElement('div');
    card.className = 'estante-sello ganado';
    const glifo = document.createElement('div');
    glifo.className = 'estante-glifo';
    glifo.textContent = def.glifo;
    const nombre = document.createElement('div');
    nombre.className = 'estante-nombre';
    nombre.textContent = contador > 1 ? `${def.nombre} ×${contador}` : def.nombre;
    const f = document.createElement('div');
    f.className = 'estante-fecha';
    f.textContent = fecha;
    card.append(glifo, nombre, f);

    const btn = document.createElement('button');
    btn.className = 'enlace reconocer';
    if (yaReconocidas.has(id)) {
      btn.textContent = '❧ reconocido';
      btn.disabled = true;
    } else {
      btn.textContent = '❧ reconocer';
      btn.title = 'Un gesto único: reconocer el trabajo detrás de este sello';
      btn.addEventListener('click', async () => {
        btn.disabled = true;
        try {
          await Api.reconocer(amigo.userId, id);
          btn.textContent = '❧ reconocido';
        } catch {
          btn.textContent = '❧ reconocido'; // duplicado (409): ya estaba hecho
        }
      });
    }
    card.appendChild(btn);
    estante.appendChild(card);
  });

  // Deshacer el vínculo: 2 clics, sin súplicas (§0.1)
  const btnEliminar = $('btn-vitrina-eliminar');
  btnEliminar.onclick = async () => {
    if (!window.confirm(`¿Deshacer el vínculo con ${amigo.username}?`)) return;
    try {
      await Api.eliminarAmistad(amigo.amistadId);
      $('claustro-vitrina').hidden = true;
      await renderizarAmigos();
    } catch (e) {
      $('claustro-msg').textContent = `No se pudo deshacer: ${e.message}`;
    }
  };

  $('claustro-vitrina').scrollIntoView({ behavior: 'smooth' });
}

/* -------------------- Reconocimientos recibidos ---------------------- */

async function renderizarReconocimientos() {
  const recibidos = await Api.reconocimientosRecibidos();
  if (!recibidos.length) return;
  $('claustro-notifs').hidden = false;
  const lista = $('claustro-notifs-lista');
  lista.innerHTML = '';

  // Resolver nombres desde la lista de amigos ya cargada
  const nombreDe = (userId) =>
    amigosCache.find((a) => a.userId === userId)?.username ?? 'Un colega del claustro';

  recibidos.forEach((rec) => {
    const def = Badges.definicion(rec.insignia_id);
    const p = document.createElement('p');
    p.className = `notif-reconocimiento${rec.visto ? '' : ' nueva'}`;
    p.textContent = `❧ ${nombreDe(rec.de_user)} reconoció tu sello «${def?.nombre ?? rec.insignia_id}».`;
    lista.appendChild(p);
  });

  const nuevas = recibidos.filter((r) => !r.visto).map((r) => r.id);
  if (nuevas.length) Api.marcarReconocimientosVistos(nuevas).catch(() => {});
}

/* -------------------- Moraleja de la semana -------------------------- */

function renderizarSelectorFicha() {
  const sel = $('claustro-ficha-select');
  sel.innerHTML = '';
  const { fichaCompartidaUid } = Storage.load('claustro');
  const fichas = Storage.load('historial')
    .filter((h) => h.moraleja && h.disparador)
    .slice(-20)
    .reverse();

  if (!fichas.length) {
    const opt = document.createElement('option');
    opt.textContent = 'Aún no tienes fichas en el cuaderno';
    opt.disabled = true;
    sel.appendChild(opt);
    return;
  }
  fichas.forEach((h) => {
    const uid = h.uid ?? `${h.problemId}|${h.fecha}`;
    const opt = document.createElement('option');
    opt.value = uid;
    opt.textContent = `${h.fecha} — ${h.moraleja.slice(0, 60)}${h.moraleja.length > 60 ? '…' : ''}`;
    opt.selected = uid === fichaCompartidaUid;
    sel.appendChild(opt);
  });

  $('claustro-compartir-msg').textContent = fichaCompartidaUid
    ? 'Hay una ficha compartida: tus amigos pueden leerla en tu vitrina.'
    : 'Nada compartido: tu cuaderno es privado por defecto.';
}

async function compartirFicha() {
  const uid = $('claustro-ficha-select').value;
  if (!uid) return;
  Storage.update('claustro', (c) => {
    c.fichaCompartidaUid = uid;
    return c;
  });
  await publicarVitrina();
  renderizarSelectorFicha();
}

async function descompartirFicha() {
  Storage.update('claustro', (c) => {
    c.fichaCompartidaUid = null;
    return c;
  });
  await publicarVitrina();
  renderizarSelectorFicha();
}
