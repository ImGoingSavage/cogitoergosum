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

const VERSION = 'cogitoergosum-v130';

// Los videos (fondo 1.5 MB, login 5 MB) NO entran al precache del shell: se
// cachean bajo demanda en su propia caché, que sobrevive a los cambios de
// VERSION.
const CACHE_MEDIA = 'cogitoergosum-media-v1';

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
  'js/cuentaUI.js',
  'js/mentorChat.js',
  'js/mentorLocal.js',
  'js/claustro.js',
  'js/markdown.js',
  'js/pizarra.js',
  // KaTeX vendorizado local (render de matemáticas, offline): JS + CSS + fuentes
  // woff2. js/markdown.js lo usa con fallback a Unicode si no cargara.
  'assets/katex/katex.min.js',
  'assets/katex/katex.min.css',
  'assets/katex/fonts/KaTeX_AMS-Regular.woff2',
  'assets/katex/fonts/KaTeX_Caligraphic-Bold.woff2',
  'assets/katex/fonts/KaTeX_Caligraphic-Regular.woff2',
  'assets/katex/fonts/KaTeX_Fraktur-Bold.woff2',
  'assets/katex/fonts/KaTeX_Fraktur-Regular.woff2',
  'assets/katex/fonts/KaTeX_Main-Bold.woff2',
  'assets/katex/fonts/KaTeX_Main-BoldItalic.woff2',
  'assets/katex/fonts/KaTeX_Main-Italic.woff2',
  'assets/katex/fonts/KaTeX_Main-Regular.woff2',
  'assets/katex/fonts/KaTeX_Math-BoldItalic.woff2',
  'assets/katex/fonts/KaTeX_Math-Italic.woff2',
  'assets/katex/fonts/KaTeX_SansSerif-Bold.woff2',
  'assets/katex/fonts/KaTeX_SansSerif-Italic.woff2',
  'assets/katex/fonts/KaTeX_SansSerif-Regular.woff2',
  'assets/katex/fonts/KaTeX_Script-Regular.woff2',
  'assets/katex/fonts/KaTeX_Size1-Regular.woff2',
  'assets/katex/fonts/KaTeX_Size2-Regular.woff2',
  'assets/katex/fonts/KaTeX_Size3-Regular.woff2',
  'assets/katex/fonts/KaTeX_Size4-Regular.woff2',
  'assets/katex/fonts/KaTeX_Typewriter-Regular.woff2',
  'data/problems.json',
  'data/study.json',
  'data/quotes.json',
  'data/badges.json',
  'data/avatar.json',
  // Simulación de entrevista (Nivel E): taxonomía + un guion por ronda/cluster.
  'data/entrevista/_taxonomia.json',
  'data/entrevista/cluster-quant-prob.json',
  'data/entrevista/cluster-stats-inf.json',
  'data/entrevista/cluster-dsa.json',
  'data/entrevista/cluster-system-design.json',
  'data/entrevista/cluster-ds-applied.json',
  'data/entrevista/cluster-ml-systems.json',
  'data/entrevista/cluster-causal-health.json',
  'data/entrevista/cluster-conductual.json',
  // Lecciones de teoría del Modo Estudio (una por unidad): texto plano
  // pequeño — precachearlas garantiza estudiar sin red desde el iPad.
  'data/teoria/polya-cuatro-pasos.md',
  'data/teoria/polya-diccionario.md',
  'data/teoria/zeitz-1.md',
  'data/teoria/zeitz-2a.md',
  'data/teoria/zeitz-2b.md',
  'data/teoria/zeitz-23.md',
  'data/teoria/zeitz-24.md',
  'data/teoria/zeitz-31.md',
  'data/teoria/zeitz-32.md',
  'data/teoria/zeitz-33.md',
  'data/teoria/zeitz-34.md',
  'data/teoria/zeitz-41.md',
  'data/teoria/zeitz-61.md',
  'data/teoria/zeitz-62.md',
  'data/teoria/zeitz-63.md',
  'data/teoria/engel-comb.md',
  'data/teoria/zeitz-71.md',
  'data/teoria/zeitz-72.md',
  'data/teoria/zeitz-64.md',
  'data/teoria/zeitz-43.md',
  'data/teoria/zeitz-73.md',
  'data/teoria/zeitz-74.md',
  'data/teoria/zeitz-75.md',
  'data/teoria/engel-nt.md',
  'data/teoria/zeitz-52.md',
  'data/teoria/zeitz-53.md',
  'data/teoria/zeitz-54.md',
  'data/teoria/zeitz-55.md',
  'data/teoria/engel-ineq.md',
  'data/teoria/zeitz-42.md',
  'data/teoria/zeitz-82.md',
  'data/teoria/zeitz-83.md',
  'data/teoria/zeitz-84.md',
  'data/teoria/zeitz-9.md',
  'data/teoria/engel-inv.md',
  'data/teoria/engel-color.md',
  'data/teoria/engel-extremo.md',
  'data/teoria/engel-juegos.md',
  'data/teoria/arena-q1.md',
  'data/teoria/arena-q2.md',
  'data/teoria/arena-q3.md',
  'data/teoria/arena-q4.md',
  'data/teoria/arena-q5.md',
  'data/teoria/arena-q6.md',
  'data/teoria/arena-q7.md',
  'data/teoria/arena-q8.md',
  'data/teoria/arena-q9.md',
  'data/teoria/arena-q10.md',
  'data/teoria/arena-q11.md',
  'data/teoria/arena-q12.md',
  'data/teoria/arena-q13.md',
  'data/teoria/arena-p1.md',
  'data/teoria/arena-p2.md',
  'data/teoria/arena-p3.md',
  'data/teoria/arena-p4.md',
  'data/teoria/arena-fc1.md',
  'data/teoria/arena-fc2.md',
  'data/teoria/arena-fc3.md',
  'data/teoria/arena-fc4.md',
  'data/teoria/arena-b1.md',
  'data/teoria/arena-b2.md',
  'data/teoria/arena-b3.md',
  'data/teoria/arena-b4.md',
  'data/teoria/arena-dg1.md',
  'data/teoria/arena-dg2.md',
  'data/teoria/arena-dg3.md',
  'data/teoria/arena-dg4.md',
  'data/teoria/arena-cb1.md',
  'data/teoria/arena-cb2.md',
  'data/teoria/arena-cb3.md',
  'data/teoria/arena-cb4.md',
  'data/teoria/arena-cc1.md',
  'data/teoria/arena-cc2.md',
  'data/teoria/arena-cc3.md',
  'data/teoria/arena-cc4.md',
  'data/teoria/arena-sd1.md',
  'data/teoria/arena-sd2.md',
  'data/teoria/arena-sd3.md',
  'data/teoria/arena-sd4.md',
  'data/teoria/arena-ads1.md',
  'data/teoria/arena-ads2.md',
  'data/teoria/arena-ads3.md',
  'data/teoria/arena-ads4.md',
  'data/teoria/arena-cds1.md',
  'data/teoria/arena-cds2.md',
  'data/teoria/arena-cds3.md',
  'data/teoria/arena-cds4.md',
  'data/teoria/arena-pst1.md',
  'data/teoria/arena-pst2.md',
  'data/teoria/arena-pst3.md',
  'data/teoria/arena-pst4.md',
  'data/teoria/arena-dmls1.md',
  'data/teoria/arena-dmls2.md',
  'data/teoria/arena-dmls3.md',
  'data/teoria/arena-dmls4.md',
  'data/teoria/arena-rml1.md',
  'data/teoria/arena-rml2.md',
  'data/teoria/arena-rml3.md',
  'data/teoria/arena-rml4.md',
  'data/teoria/arena-mldp1.md',
  'data/teoria/arena-mldp2.md',
  'data/teoria/arena-mldp3.md',
  'data/teoria/arena-mldp4.md',
  'data/teoria/arena-sre1.md',
  'data/teoria/arena-sre2.md',
  'data/teoria/arena-sre3.md',
  'data/teoria/arena-sre4.md',
  'data/teoria/arena-obs1.md',
  'data/teoria/arena-obs2.md',
  'data/teoria/arena-obs3.md',
  'data/teoria/arena-obs4.md',
  'data/teoria/arena-rom1.md',
  'data/teoria/arena-rom2.md',
  'data/teoria/arena-rom3.md',
  'data/teoria/arena-rom4.md',
  'data/teoria/arena-htd1.md',
  'data/teoria/arena-htd2.md',
  'data/teoria/arena-htd3.md',
  'data/teoria/arena-htd4.md',
  'data/teoria/arena-iml1.md',
  'data/teoria/arena-iml2.md',
  'data/teoria/arena-iml3.md',
  'data/teoria/arena-iml4.md',
  'data/teoria/arena-isl1.md',
  'data/teoria/arena-isl2.md',
  'data/teoria/arena-isl3.md',
  'data/teoria/arena-isl4.md',
  'data/teoria/arena-h3.md',
  'data/teoria/arena-h4.md',
  'data/teoria/arena-h5.md',
  'data/teoria/arena-h6.md',
  'data/teoria/arena-h7.md',
  'data/teoria/arena-h8.md',
  'data/teoria/arena-h9.md',
  'data/teoria/arena-h10.md',
  'data/teoria/arena-h11.md',
  'data/teoria/arena-h12.md',
  'data/teoria/arena-h13.md',
  'data/teoria/arena-h14.md',
  'data/teoria/arena-h15.md',
  'data/teoria/arena-h16.md',
  'data/teoria/arena-h17.md',
  'data/teoria/arena-h18.md',
  'data/teoria/arena-h19.md',
  'data/teoria/arena-h20.md',
  'data/teoria/arena-h21.md',
  'data/teoria/arena-h22.md',
  'data/teoria/arena-c1.md',
  'data/teoria/arena-c2.md',
  'data/teoria/arena-c3.md',
  'data/teoria/arena-c4.md',
  'data/teoria/arena-m1.md',
  'data/teoria/arena-m2.md',
  'data/teoria/arena-h1.md',
  'data/teoria/arena-s1.md',
  'data/teoria/arena-h2.md',
  'data/teoria/zeitz-85a.md',
  'data/teoria/zeitz-85b.md',
  'data/teoria/engel-ind.md',
  'data/teoria/engel-suc.md',
  'data/teoria/engel-pol.md',
  'data/teoria/engel-fun.md',
  'data/teoria/engel-geo2.md',
  'data/teoria/aime-alg.md',
  'data/teoria/aime-geo.md',
  'data/teoria/aime-cnt.md',
  'assets/fonts/EBGaramond-Regular.woff2',
  'assets/fonts/EBGaramond-SemiBold.woff2',
  'assets/fonts/EBGaramond-Italic.woff2',
  'assets/icons/icon.svg',
  'assets/icons/icon-192.png',
  'assets/icons/icon-512.png',
  'assets/video/fondo-poster.jpg',
  'assets/video/login-poster.jpg',
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

  // Videos (fondo y login): cache-first en CACHE_MEDIA con manejo de Range
  if (url.pathname.includes('/assets/video/') && url.pathname.endsWith('.mp4')) {
    event.respondWith(servirVideo(request));
    return;
  }

  event.respondWith(responderShell(event, request));
});

/**
 * App shell: cache-first con refresco en segundo plano (stale-while-
 * revalidate). El refresco se registra con event.waitUntil para que el
 * navegador no termine el SW antes de completar el cache.put (válido:
 * waitUntil se llama mientras la promesa de respondWith sigue pendiente).
 */
async function responderShell(event, request) {
  const cache = await caches.open(VERSION);
  const enCache = await cache.match(request);
  const refresco = fetch(request)
    .then((res) => {
      if (res && res.ok) cache.put(request, res.clone());
      return res;
    })
    .catch(() => null);
  if (enCache) {
    event.waitUntil(refresco);
    return enCache;
  }
  return (await refresco) ?? Response.error();
}

/**
 * Sirve los videos offline-first. Se guarda SIEMPRE la respuesta completa
 * (la descarga se hace sin header Range, porque cache.put rechaza
 * respuestas 206) y las peticiones Range del reproductor se responden
 * recortando esa copia completa (≤5 MB: recortar en memoria es barato).
 */
async function servirVideo(request) {
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
