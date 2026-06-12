/**
 * api.js — Puerta única al backend (Supabase, HANDOFFCES §5.2 C.3).
 *
 * fetch directo a GoTrue (auth) y PostgREST (datos), SIN SDK: cero
 * dependencias, convención del proyecto. La interfaz de ~10 operaciones es
 * estable a propósito: cambiar de backend (p. ej. a PocketBase) significa
 * reemplazar SOLO este archivo.
 *
 * La ANON_KEY es pública por diseño (vive igualmente en cada navegador);
 * la seguridad real la dan las políticas RLS de supabase/schema.sql: cada
 * usuario solo puede leer/escribir SUS filas. Lo que jamás debe aparecer
 * aquí: la service_role key.
 */

import { load, save, remove, deviceId } from './storage.js';

const URL_BASE = 'https://rcaljqmibtkorcmdyqvg.supabase.co';
const ANON_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJjYWxqcW1pYnRrb3JjbWR5cXZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNjE0MTksImV4cCI6MjA5NjczNzQxOX0.wN8mxz_skkQepj64Wd_YlPN9koIH8UU2ZrJplkJwGJ8';

export function configurado() {
  return Boolean(URL_BASE && ANON_KEY);
}

/* ========================= Sesión y tokens ============================ */

export function sesionActual() {
  return load('sesionSupabase');
}

function guardarSesion(data) {
  if (!data?.access_token) return null;
  const sesion = {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
    expiraEn: Date.now() + (data.expires_in ?? 3600) * 1000,
    userId: data.user?.id ?? sesionActual()?.userId ?? null,
    email: data.user?.email ?? sesionActual()?.email ?? null,
  };
  save('sesionSupabase', sesion);
  return sesion;
}

function cabeceras(token) {
  return {
    'Content-Type': 'application/json',
    apikey: ANON_KEY,
    Authorization: `Bearer ${token ?? ANON_KEY}`,
  };
}

async function gotrue(ruta, body, token) {
  const res = await fetch(`${URL_BASE}/auth/v1/${ruta}`, {
    method: 'POST',
    headers: cabeceras(token),
    body: JSON.stringify(body ?? {}),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.msg ?? data.error_description ?? data.message ?? `Auth ${res.status}`);
  }
  return data;
}

/**
 * Registro. Con "Confirm email" desactivado, Supabase devuelve sesión
 * directa; si está activado, devuelve usuario sin tokens (el llamador debe
 * avisar "revisa tu correo").
 */
export async function registrar(email, password) {
  const data = await gotrue('signup', { email, password });
  return guardarSesion(data); // null si falta confirmar el correo
}

export async function iniciarSesion(email, password) {
  const data = await gotrue('token?grant_type=password', { email, password });
  return guardarSesion(data);
}

/**
 * Redirige a Google OAuth vía Supabase. El usuario vuelve a la misma URL
 * con #access_token=…&refresh_token=… en el hash; manejarHashOAuth() lo
 * consume en el arranque.
 */
export function loginConGoogle() {
  const origen = window.location.href.split('#')[0];
  window.location.href =
    `${URL_BASE}/auth/v1/authorize?provider=google&redirect_to=${encodeURIComponent(origen)}`;
}

/**
 * Consume el hash de retorno del flujo OAuth (Google → Supabase → app).
 * Si hay access_token guarda la sesión y limpia el hash. No-op si no hay
 * hash o si ya fue consumido. Retorna la sesión guardada o null.
 */
export function manejarHashOAuth() {
  const hash = window.location.hash.slice(1);
  if (!hash) return null;
  const params = new URLSearchParams(hash);
  if (!params.get('access_token')) return null;
  history.replaceState(null, '', window.location.pathname + window.location.search);
  return guardarSesion({
    access_token: params.get('access_token'),
    refresh_token: params.get('refresh_token'),
    expires_in: Number(params.get('expires_in')) || 3600,
    token_type: params.get('token_type'),
  });
}

export async function cerrarSesion() {
  const sesion = sesionActual();
  if (sesion) {
    try {
      await gotrue('logout', {}, sesion.accessToken);
    } catch {
      // El servidor puede haber expirado la sesión; localmente se cierra igual.
    }
  }
  remove('sesionSupabase');
}

/** Token vigente, renovándolo si está por expirar. null = sin sesión. */
async function tokenVigente() {
  let sesion = sesionActual();
  if (!sesion) return null;
  if (Date.now() > sesion.expiraEn - 60_000) {
    try {
      const data = await gotrue('token?grant_type=refresh_token', {
        refresh_token: sesion.refreshToken,
      });
      sesion = guardarSesion(data);
    } catch {
      remove('sesionSupabase'); // refresh inválido: la sesión caducó de verdad
      try {
        window.dispatchEvent(new CustomEvent('cps:sesion-invalida'));
      } catch {
        // Entornos sin window.
      }
      return null;
    }
  }
  return sesion;
}

/* ========================= Datos (PostgREST) ========================== */

async function rest(metodo, ruta, body, prefer) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  const headers = cabeceras(sesion.accessToken);
  if (prefer) headers.Prefer = prefer;
  const res = await fetch(`${URL_BASE}/rest/v1/${ruta}`, {
    method: metodo,
    headers,
    body: body == null ? undefined : JSON.stringify(body),
  });
  const texto = await res.text();
  if (!res.ok) throw new Error(`API ${res.status}: ${texto.slice(0, 180)}`);
  return texto ? JSON.parse(texto) : null;
}

/** Sube un lote de eventos del outbox (append-only). */
export async function subirEventos(eventos) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  const filas = eventos.map((e) => ({
    user_id: sesion.userId,
    device_id: deviceId(),
    uid: e.uid,
    tipo: e.tipo,
    payload: { ...e.payload, _uid: e.uid, _ts: e.ts },
  }));
  await rest('POST', 'events?on_conflict=uid', filas, 'resolution=ignore-duplicates');
}

/**
 * RESERVA, sin llamadores hoy: el arranque en dispositivo nuevo usa solo el
 * snapshot (sync.js → adoptarOUnir), que siempre está al día porque
 * sincronizar() lo sube tras cada drenado. Se conserva como parte de la
 * interfaz C.3 para una futura reconstrucción completa desde el event log.
 */
export async function descargarEventos(desdeISO) {
  const filtro = desdeISO ? `&ts=gt.${encodeURIComponent(desdeISO)}` : '';
  return (await rest('GET', `events?select=ts,tipo,payload&order=ts.asc${filtro}`)) ?? [];
}

export async function subirSnapshot(estado) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  await rest(
    'POST',
    'snapshots',
    [{ user_id: sesion.userId, actualizado: new Date().toISOString(), estado }],
    'resolution=merge-duplicates'
  );
}

/** Devuelve { actualizado, estado } o null si el usuario aún no tiene snapshot. */
export async function descargarSnapshot() {
  const filas = await rest('GET', 'snapshots?select=actualizado,estado');
  return filas?.[0] ?? null;
}

/** Borra al usuario y todos sus datos del servidor (RPC, 2 clics, §0.1). */
export async function borrarCuenta() {
  await rest('POST', 'rpc/borrar_mi_cuenta', {});
  remove('sesionSupabase');
}

/* ================= El claustro (Fase D, §2.4) ========================= */
/* Tablas y RLS en supabase/schema-fase-d.sql. Inspiración, no dominancia. */

export async function obtenerMiPerfil() {
  const sesion = await tokenVigente();
  if (!sesion) return null;
  const filas = await rest('GET', `perfiles?user_id=eq.${sesion.userId}&select=username,vitrina,actualizado`);
  return filas?.[0] ?? null;
}

/** Crea o actualiza el perfil-vitrina propio (upsert por user_id). */
export async function publicarPerfil(username, vitrina) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  await rest(
    'POST',
    'perfiles',
    [{ user_id: sesion.userId, username, vitrina, actualizado: new Date().toISOString() }],
    'resolution=merge-duplicates'
  );
}

export async function perfilesDe(userIds) {
  if (!userIds.length) return [];
  const lista = userIds.join(',');
  return (await rest('GET', `perfiles?user_id=in.(${lista})&select=user_id,username,vitrina`)) ?? [];
}

export async function crearInvitacion(codigo) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  await rest('POST', 'invitaciones', [{ codigo, de_user: sesion.userId }]);
  return codigo;
}

export async function invitacionesPendientes() {
  return (await rest('GET', 'invitaciones?usado_por=is.null&select=codigo,creado&order=creado.desc')) ?? [];
}

/** Canjea el código de un amigo; devuelve su nombre en el claustro. */
export async function canjearInvitacion(codigo) {
  return rest('POST', 'rpc/canjear_invitacion', { codigo_entrada: codigo });
}

export async function listarAmistades() {
  return (await rest('GET', 'amistades?select=id,user_a,user_b,creado')) ?? [];
}

export async function eliminarAmistad(id) {
  await rest('DELETE', `amistades?id=eq.${id}`);
}

/** ❧ — la única interacción. El UNIQUE del esquema impide acumular. */
export async function reconocer(paraUser, insigniaId) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  await rest('POST', 'reconocimientos', [
    { de_user: sesion.userId, para_user: paraUser, insignia_id: insigniaId },
  ]);
}

export async function reconocimientosRecibidos(limite = 10) {
  const sesion = await tokenVigente();
  if (!sesion) return [];
  return (
    (await rest(
      'GET',
      `reconocimientos?para_user=eq.${sesion.userId}&select=id,de_user,insignia_id,creado,visto&order=creado.desc&limit=${limite}`
    )) ?? []
  );
}

export async function reconocimientosHechosA(paraUser) {
  const sesion = await tokenVigente();
  if (!sesion) return [];
  return (
    (await rest(
      'GET',
      `reconocimientos?de_user=eq.${sesion.userId}&para_user=eq.${paraUser}&select=insignia_id`
    )) ?? []
  );
}

export async function marcarReconocimientosVistos(ids) {
  if (!ids.length) return;
  await rest('PATCH', `reconocimientos?id=in.(${ids.join(',')})`, { visto: true });
}

/* ============== Pensar juntos (§2.4 punto 15, aprobado) =============== */

export async function proponerPensarJuntos(amigoId, candidatos) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  await rest('POST', 'pensar_juntos', [
    { user_a: sesion.userId, user_b: amigoId, candidatos },
  ]);
}

export async function listarPensarJuntos() {
  return (
    (await rest('GET', 'pensar_juntos?select=id,user_a,user_b,candidatos,problem_id,estado,creado&order=creado.desc')) ?? []
  );
}

/** El invitado acepta: fija el problema sorteado y activa la sesión conjunta. */
export async function aceptarPensarJuntos(id, problemId) {
  await rest('PATCH', `pensar_juntos?id=eq.${id}`, {
    problem_id: problemId,
    estado: 'activa',
  });
}

export async function retirarPensarJuntos(id) {
  await rest('DELETE', `pensar_juntos?id=eq.${id}`);
}

export async function entregarPensarJuntos(pjId, payload) {
  const sesion = await tokenVigente();
  if (!sesion) throw new Error('Sin sesión');
  await rest('POST', 'pj_entregas', [{ pj_id: pjId, user_id: sesion.userId, payload }]);
}

/**
 * Entregas de un pensar-juntos. Por RLS, la del otro SOLO llega cuando la
 * tuya ya existe (struggle first garantizado por el servidor).
 */
export async function entregasPensarJuntos(pjId) {
  return (await rest('GET', `pj_entregas?pj_id=eq.${pjId}&select=user_id,payload,creado`)) ?? [];
}
