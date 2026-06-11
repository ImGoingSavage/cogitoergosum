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
    tipo: e.tipo,
    payload: { ...e.payload, _uid: e.uid, _ts: e.ts },
  }));
  await rest('POST', 'events', filas);
}

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
