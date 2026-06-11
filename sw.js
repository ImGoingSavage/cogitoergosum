/**
 * sw.js — Service worker de CogitoErgoSum (PWA, HANDOFFCES §3.2).
 *
 * Estrategia offline-first coherente con la arquitectura de la app:
 * LocalStorage es la verdad inmediata y el shell completo (HTML, CSS, JS,
 * datos JSON y fuentes) queda precacheado, de modo que la app funciona
 * sin red desde la segunda visita.
 *
 * - Mismo origen + GET: cache-first con refresco en segundo plano
 *   (stale-while-revalidate): siempre responde rápido y se actualiza solo.
 * - Cross-origin (p. ej. api.anthropic.com): NO se intercepta jamás.
 *
 * Al cambiar cualquier archivo del shell, sube VERSION para invalidar caché.
 */

const VERSION = 'cogitoergosum-v8';

// El video de fondo (1.5 MB) NO entra al precache del shell: se cachea bajo
// demanda en su propia caché, que sobrevive a los cambios de VERSION.
const CACHE_MEDIA = 'cogitoergosum-media-v1';
const RUTA_VIDEO_FONDO = '/assets/video/fondo.mp4';

const SHELL = [
  './',
  'index.html',
  'manifest.webmanifest',
  'css/styles.css',
  'js/app.js',
  'js/storage.js',
  'js/timer.js',
  'js/hintSystem.js',
  'js/adaptiveEngine.js',
  'js/spacedRepetition.js',
  'js/analytics.js',
  'js/aiMentor.js',
  'js/problemFactory.js',
  'js/study.js',
  'js/badges.js',
  'js/avatar.js',
  'js/api.js',
  'js/sync.js',
  'js/claustro.js',
  'data/problems.json',
  'data/study.json',
  'data/quotes.json',
  'data/badges.json',
  'data/avatar.json',
  'assets/fonts/EBGaramond-Regular.woff2',
  'assets/fonts/EBGaramond-SemiBold.woff2',
  'assets/fonts/EBGaramond-Italic.woff2',
  'assets/icons/icon.svg',
  'assets/icons/icon-192.png',
  'assets/icons/icon-512.png',
  'assets/video/fondo-poster.jpg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(VERSION).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((claves) =>
        Promise.all(
          claves.filter((k) => k !== VERSION && k !== CACHE_MEDIA).map((k) => caches.delete(k))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return; // la API de Claude va directo

  // Video de fondo: cache-first en CACHE_MEDIA con manejo de Range
  if (url.pathname.endsWith(RUTA_VIDEO_FONDO)) {
    event.respondWith(servirVideoFondo(request));
    return;
  }

  event.respondWith(
    caches.open(VERSION).then(async (cache) => {
      const enCache = await cache.match(request);
      const refresco = fetch(request)
        .then((res) => {
          if (res && res.ok) cache.put(request, res.clone());
          return res;
        })
        .catch(() => null);
      return enCache ?? (await refresco) ?? Response.error();
    })
  );
});

/**
 * Sirve el video de fondo offline-first. Se guarda SIEMPRE la respuesta
 * completa (la descarga se hace sin header Range, porque cache.put rechaza
 * respuestas 206) y las peticiones Range del reproductor se responden
 * recortando esa copia completa (1.5 MB: recortar en memoria es barato).
 */
async function servirVideoFondo(request) {
  const cache = await caches.open(CACHE_MEDIA);
  let completo = await cache.match(request.url);
  if (!completo) {
    try {
      const res = await fetch(request.url); // sin Range: copia completa
      if (!res || res.status !== 200) return res ?? Response.error();
      await cache.put(request.url, res.clone());
      completo = res;
    } catch {
      return Response.error(); // sin red ni caché: la app sigue con el póster
    }
  }
  const rango = request.headers.get('range');
  if (!rango) return completo;
  const buf = await completo.arrayBuffer();
  const m = /bytes=(\d+)-(\d+)?/i.exec(rango);
  const inicio = m ? Number(m[1]) : 0;
  const fin = m && m[2] ? Math.min(Number(m[2]), buf.byteLength - 1) : buf.byteLength - 1;
  return new Response(buf.slice(inicio, fin + 1), {
    status: 206,
    statusText: 'Partial Content',
    headers: {
      'Content-Type': 'video/mp4',
      'Accept-Ranges': 'bytes',
      'Content-Range': `bytes ${inicio}-${fin}/${buf.byteLength}`,
      'Content-Length': String(fin - inicio + 1),
    },
  });
}
