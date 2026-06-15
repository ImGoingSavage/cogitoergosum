# Sistemas de datos a escala

## Acortador de URLs (TinyURL, bit.ly)

**Dos operaciones:** acortar (`POST` URL larga → URL corta) y redirigir (`GET` corta → 301/302 a la larga).

**301 vs 302:**
- **301 (permanente):** el navegador cachea; las siguientes visitas van directo sin tocar tu servidor → menos carga, pero pierdes analítica de clics.
- **302 (temporal):** cada visita pasa por tu servidor → buena para analítica.

**Longitud del hash:** con **base62** (`[a-zA-Z0-9]`, 62 símbolos), una clave de **7 caracteres** da 62⁷ ≈ **3.5 billones** de URLs. Suficiente para años.

**Dos enfoques para generar la clave:**
- **Hash + resolver colisiones:** `hash(url)` recortado; si choca, reintenta con sal. Requiere chequear la BD.
- **Conversión de base (ID → base62):** un generador de ID único produce un entero creciente; lo conviertes a base62. Sin colisiones, sin chequeo, pero la clave es predecible (enumerable).

**Almacenamiento:** tabla `<short_key, long_url>`. Una **caché** delante (las URLs populares se leen muchísimo). El cuello de botella es lectura, no escritura.

---

## Web crawler

**Algoritmo base:** dado un conjunto de URLs semilla → descarga las páginas → extrae enlaces → añade los nuevos a la cola → repite (un BFS sobre el grafo web).

**Componentes:**
- **URL Frontier:** cola de URLs por visitar. Gestiona **prioridad** (PageRank, tráfico) y **politeness**.
- **Politeness:** no martillees un mismo host. Una cola por host + un *delay* entre peticiones; respeta `robots.txt`.
- **Dedup de contenido:** evita procesar páginas duplicadas. Hash del contenido (o checksum) en un **bloom filter** / conjunto.
- **Almacenamiento del frontier:** demasiado grande para memoria → mayoría en disco, buffers en RAM.

**Trampas a manejar (robustez):**
- **Spider traps:** URLs que generan profundidad infinita → límite de longitud de ruta.
- **Páginas duplicadas / réplicas:** ~30% de la web está duplicada.
- **HTML malo, servidores lentos o caídos:** timeouts y reintentos.

**BFS vs prioridad:** BFS puro trata todas las URLs igual; un buen crawler prioriza por importancia y frescura, y separa el frontier por host para la politeness.

---

## Sistema de notificaciones (push, SMS, email)

**Tres tipos de canal**, cada uno con su proveedor de terceros:
- **iOS push:** APNs (Apple Push Notification service).
- **Android push:** FCM (Firebase Cloud Messaging).
- **SMS:** Twilio, Nexmo. **Email:** SendGrid, Mailchimp.

**Flujo:** servicios (origen) → **servidores de notificación** (validan, arman el payload) → **colas de mensajes** (una por canal, desacopla y absorbe picos) → **workers** → proveedores → dispositivos.

**Por qué la cola es central:** desacopla los servicios de los proveedores; si un proveedor se cae o se ralentiza, los mensajes esperan en la cola en vez de perderse o bloquear al productor. Permite escalar los workers de forma independiente.

**Fiabilidad:**
- **No perder notificaciones:** persiste en una BD de logs; reintenta los fallidos.
- **Evitar duplicados (idempotencia):** clave de deduplicación; si ya se vio el evento, descártalo (la entrega exactly-once es imposible, así que apunta a at-least-once + dedup).
- **Tasa de entrega, rate limiting** por usuario para no spamear, y opt-out.

---

## News feed (timeline social)

**Dos flujos:**
1. **Publicar (feed publishing):** el usuario postea → se escribe en caché y BD → se **populariza** a los feeds de sus amigos.
2. **Construir (feed building):** agregar los posts de los amigos en orden cronológico inverso.

**El gran trade-off: fanout on write vs on read.**

| | Fanout on write (push) | Fanout on read (pull) |
|-|------------------------|-----------------------|
| Cuándo | Al publicar, copia el post al feed de cada amigo | Al abrir el feed, recopila los posts de los amigos |
| Lectura del feed | Instantánea (precomputada) | Lenta (agrega en tiempo real) |
| Escritura | Cara: O(amigos) por post | Barata |
| Problema | **"Hotkey":** una celebridad con 50 M seguidores dispara 50 M escrituras | Lecturas costosas para todos |
| Datos rancios | Pre-genera feeds de usuarios inactivos en vano | Siempre fresco |

**Solución híbrida (la que se usa):** fanout on write para usuarios normales; fanout on read para celebridades. Lo mejor de ambos: feeds rápidos sin la tormenta de escritura del influencer.

**Infra:** el feed se guarda en caché (Redis) como lista de `post_id`; el contenido completo se hidrata por separado. Réplicas de lectura para la BD.

---

## Mini-ejemplo trabajado: el hotkey del fanout on write

Usuario normal con 200 amigos publica un post. **Fanout on write** (push): copias el `post_id` a los 200 feeds → 200 escrituras, barato, y leer el feed es instantáneo (precomputado). Perfecto.

Ahora una **celebridad con 50 M seguidores** publica. Fanout on write dispara **50 M escrituras** de golpe → tormenta que satura el sistema (el "hotkey"). Y si pre-generas feeds de seguidores **inactivos**, gastas en vano.

La **solución híbrida** (la real): fanout on write para usuarios normales (feeds rápidos), y **fanout on read** (pull) para las celebridades — al abrir tu feed, *recoges* en el momento los posts de las pocas celebridades que sigues. Lo mejor de ambos: lectura rápida sin la tormenta del influencer.

**Predicción antes de seguir:** ¿qué decisión de ML es isomorfa a "push vs pull"? **Batch vs online prediction**: fanout on write = precomputar (batch, rápido al leer, caro y rancio si nadie lo pide); fanout on read = computar on-demand (online, fresco, pelea contra la latencia). La misma dualidad precompute/compute (conecta con [[arena-dmls3]]).

## Prototipo, contraejemplo y caso borde

- **Prototipo (cuello = lectura):** URL corta o feed que se lee muchísimo → precomputa y cachea; las colas absorben los picos de escritura.
- **Contraejemplo (fanout write para celebridad):** push a 50 M feeds → hotkey; ahí va pull.
- **Caso borde (301 vs 302):** 301 (permanente) el navegador cachea → menos carga pero **pierdes analítica de clics**; 302 (temporal) cada visita pasa por tu servidor (analítica, más carga).

## Errores típicos

- **Conceptual:** elegir un único modo de fanout para todos; la respuesta a escala es **híbrida**.
- **De diseño:** clave de URL por **conversión de base** (ID→base62) sin notar que es **enumerable** (predecible) cuando el caso exige no-adivinable → hash+sal.
- **De robustez:** un crawler "BFS simple" sin **politeness**, dedup ni límite de profundidad (spider traps) → martillea hosts y se cuelga.

## Transferencia isomorfa

- **Fanout write/read ↔ batch/online prediction:** precomputar vs computar on-demand es la misma decisión que servir predicciones en batch o en tiempo real (conecta con [[arena-dmls3]]).
- **Bloom filter para dedup ↔ hashing probabilístico:** el filtro de Bloom del crawler es memoria comprada con falsos positivos controlados, pariente de la tabla hash (conecta con [[arena-cc1]] y [[arena-sd2]], Merkle/SSTable).
- **Cola de notificaciones ↔ desacoplar con event-driven:** la cola que absorbe picos y aísla proveedores es el pub/sub asíncrono que desacopla servicios (conecta con [[arena-dmls3]]).

Moraleja de la arista: *a escala el cuello es la lectura → precomputa y cachea; pero precomputar (fanout write/batch) cuesta al escribir, así que para los casos extremos (celebridad) cambias a on-demand (pull/online) — híbrido.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Acortar/redirigir URLs" | base62 7 chars (3.5 T); 301 cachea vs 302 da analítica |
| "Clave única sin colisión y no enumerable" | hash+sal vs ID→base62 (trade-off predecibilidad) |
| "Recorrer y descubrir páginas web" | BFS con URL frontier + politeness + bloom filter |
| "No martillear un host" | Cola por host + delay + robots.txt |
| "Enviar push/SMS/email a escala" | Colas por canal + workers + proveedores externos |
| "No perder ni duplicar mensajes" | Persistir + reintentar + clave de idempotencia |
| "Timeline de amigos rápido" | Fanout on write; híbrido para celebridades |
| "Celebridad con millones de seguidores" | Fanout on read para ese caso (evita hotkey) |

---

> **Síntesis:** Estos sistemas comparten un patrón: el cuello de botella suele ser la lectura, y se resuelve precomputando y cacheando (URL corta cacheada, feed precomputado), mientras las colas desacoplan y absorben los picos de escritura (notificaciones, fanout). El web crawler enseña que un "BFS simple" a escala real necesita prioridad, politeness y dedup. Y el news feed encapsula el trade-off push/pull: precomputar es rápido al leer pero caro al escribir, y la solución casi siempre es híbrida.

---

*Retrieval: cierra y responde: (1) ¿cuántas URLs da base62 con 7 caracteres y por qué 301 reduce carga?; (2) ¿qué tres trampas debe manejar un crawler robusto?; (3) ¿por qué una cola de mensajes es central en notificaciones?; (4) explica el problema de hotkey del fanout on write y su solución híbrida.*
