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

const VERSION = 'cogitoergosum-v5';

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
      .then((claves) => Promise.all(claves.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return; // la API de Claude va directo

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
