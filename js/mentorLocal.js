/**
 * mentorLocal.js — Cliente del Mentor local opcional (backend RAG + DeepSeek).
 *
 * Constitución (§0.7): es una mejora PROGRESIVA. Si la laptop del backend está
 * apagada, `disponible()` devuelve false y la app sigue igual (Claude BYOK o
 * pistas curadas). Jamás bloquea.
 *
 * Seguridad: la API key de Claude NUNCA se manda aquí (el backend ni la pide).
 * Lo único que viaja es el JWT de Supabase (que ya tienes) + el service token.
 * La config (url, token, on/off) es LOCAL del dispositivo: fuera de CLAVES_SYNC.
 */

import * as Storage from './storage.js';
import * as Api from './api.js';

// Cache de salud: evita sondear /health en cada mensaje. TTL 60 s.
let saludCache = { ok: false, ts: 0 };

function cfg() {
  return Storage.load('mentorLocal') ?? { habilitado: false, url: '', serviceToken: '' };
}

export function configurado() {
  const c = cfg();
  return Boolean(c.habilitado && c.url);
}

function cabeceras() {
  const sesion = Api.sesionActual();
  const h = { 'Content-Type': 'application/json' };
  if (sesion?.accessToken) h.Authorization = `Bearer ${sesion.accessToken}`;
  const c = cfg();
  if (c.serviceToken) h['X-Service-Token'] = c.serviceToken;
  return h;
}

/** Sondea /health (con cache). El mentor local exige sesión Supabase válida. */
export async function disponible() {
  if (!configurado() || !Api.sesionActual()) return false;
  const ahora = Date.now();
  if (ahora - saludCache.ts < 60_000) return saludCache.ok;
  try {
    const res = await fetch(`${cfg().url.replace(/\/$/, '')}/health`, { method: 'GET' });
    saludCache = { ok: res.ok, ts: ahora };
  } catch {
    saludCache = { ok: false, ts: ahora };
  }
  return saludCache.ok;
}

/** Para el botón "Probar conexión": fuerza el sondeo y describe el resultado. */
export async function probar() {
  saludCache.ts = 0;
  if (!configurado()) return { ok: false, mensaje: 'Activa el mentor local y escribe su URL primero.' };
  if (!Api.sesionActual()) return { ok: false, mensaje: 'Inicia sesión: el mentor local exige tu cuenta.' };
  const ok = await disponible();
  return ok
    ? { ok: true, mensaje: 'Mentor local conectado y respondiendo.' }
    : { ok: false, mensaje: 'No respondió (¿laptop encendida, URL correcta, túnel arriba?).' };
}

/**
 * Pide una explicación al backend. Encola (202) y hace polling hasta
 * `completed`. Devuelve { answer, retrieved_context, provider, safety_flags }
 * o null ante cualquier fallo (el llamador cae a Claude/curado).
 */
export async function explicar(payload, { intentos = 30, esperaMs = 2000 } = {}) {
  if (!(await disponible())) return null;
  const base = cfg().url.replace(/\/$/, '');
  try {
    const res = await fetch(`${base}/mentor/evaluar`, {
      method: 'POST',
      headers: cabeceras(),
      body: JSON.stringify(payload),
    });
    if (res.status === 429) {
      return { answer: 'El mentor local está ocupado ahora mismo; intenta en un momento.', retrieved_context: [], provider: 'local', safety_flags: ['rate_limited'] };
    }
    if (!res.ok) return null;
    const { job_id } = await res.json();
    if (!job_id) return null;

    for (let i = 0; i < intentos; i++) {
      await new Promise((r) => setTimeout(r, esperaMs));
      const r = await fetch(`${base}/mentor/jobs/${job_id}`, { headers: cabeceras() });
      if (!r.ok) return null;
      const job = await r.json();
      if (job.status === 'completed') {
        return {
          answer: job.answer ?? '',
          retrieved_context: job.retrieved_context ?? [],
          provider: job.provider ?? 'local',
          safety_flags: job.safety_flags ?? [],
        };
      }
      if (['failed', 'timeout', 'rejected'].includes(job.status)) return null;
    }
    return null; // se agotó el polling
  } catch (e) {
    Storage.registrarDiagnostico('mentor-local', e.message);
    return null;
  }
}
