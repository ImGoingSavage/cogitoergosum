# Sistemas en tiempo real y de medios

## Sistema de chat (WhatsApp, Messenger)

**El reto central:** entrega en tiempo real y bidireccional. HTTP normal es petición-respuesta iniciada por el cliente; el servidor no puede "empujar" por sí solo.

**Opciones para que el servidor empuje al cliente:**
- **Polling:** el cliente pregunta cada X segundos. Desperdicia recursos si no hay mensajes.
- **Long polling:** el servidor mantiene la petición abierta hasta tener algo. Mejor, pero conexiones colgadas y reconexión frecuente.
- **WebSocket:** la respuesta canónica. Conexión **persistente y bidireccional** sobre un solo puerto (inicia como HTTP, hace upgrade). El servidor empuja cuando quiere.

**Arquitectura:**
- **Servicios sin estado** (login, perfil, registro de servicios) detrás de un load balancer.
- **Servicio de chat con estado:** mantiene las conexiones WebSocket vivas; un cliente está pegado a un servidor mientras dura la sesión.
- **Servicios de terceros:** push para notificar cuando estás offline.

**Almacenamiento — KV store** (no SQL relacional) por el enorme volumen y el patrón de acceso por `message_id`:
- 1-a-1: clave por par de usuarios.
- Grupo: clave por `channel_id`/`group_id`.
- El `message_id` debe ser **único y ordenable por tiempo** (secuencia local creciente) para ordenar la conversación.

**Sincronización de mensajes:** cada cliente recuerda el último `message_id` que vio; al reconectar pide los posteriores.

**Presencia (online/offline):** *heartbeat* periódico. Si no llega heartbeat en X segundos → offline. Se propaga a los contactos por publish/subscribe.

---

## Autocompletado de búsqueda (typeahead, "top k")

**Requisitos duros:** respuesta **< 100 ms** (si no, "stuttering"), resultados relevantes y **ordenados por popularidad** (frecuencia histórica). Cada carácter tecleado = una petición.

**Estructura: Trie (árbol de prefijos).**
- Cada nodo es un carácter; el camino desde la raíz forma el prefijo.
- **Optimización clave:** en cada nodo del trie, **cachea las top-k consultas** de ese prefijo. Así no recorres todo el subárbol en cada tecla; lees las k directamente del nodo → O(longitud del prefijo).

**Recolección de datos:** un servicio agrega la frecuencia de consultas (analytics logs → agregadores → un *Trie builder* que reconstruye el trie periódicamente, p.ej. semanal). El trie se sirve desde caché y se replica.

**Escala:** el trie es grande → **sharding por prefijo** (las que empiezan con 'a'–'m' en un shard, 'n'–'z' en otro), idealmente balanceando por popularidad real de cada letra, no uniformemente.

**Estimación:** 10 M DAU × 10 búsquedas × ~20 peticiones por búsqueda (una por tecla) → mucho QPS de lectura; por eso el cacheo en los nodos es esencial.

---

## YouTube (streaming de video)

**Dos grandes problemas:** subir y servir video a escala global.

**Subida y transcodificación:**
- El video original se sube a *blob storage* (S3-like).
- Un **pipeline de transcodificación** genera múltiples **resoluciones y formatos** (DAG de tareas: inspección, codificación, miniaturas, marca de agua). Distintos dispositivos y anchos de banda necesitan distintos bitrates.

**Servir el video:**
- **CDN** para entregar los bytes desde el nodo más cercano al usuario. Es la pieza más importante para la latencia y el costo.
- **Adaptive bitrate streaming:** el cliente cambia de calidad según su ancho de banda momentáneo (el video se trocea en segmentos por bitrate).
- **Modelo push para los virales, pull para la cola larga:** solo el contenido popular vale la pena pre-distribuir a todas las CDNs.

**Optimización de costo:** servir todo desde CDN es carísimo. Distribuye solo lo popular a la CDN; lo poco visto se sirve desde servidores propios o CDNs más baratas.

---

## Google Drive (almacenamiento y sincronización de archivos)

**Funciones:** subir/descargar, sincronizar entre dispositivos, notificaciones de cambios.

**Idea clave — almacenamiento por bloques (block storage):**
- Cada archivo se parte en **bloques** (p.ej. 4 MB).
- **Delta sync:** al modificar un archivo, solo se suben los **bloques que cambiaron**, no el archivo entero. Ahorra ancho de banda enorme.
- **Deduplicación:** bloques idénticos (mismo hash) se guardan una sola vez.
- **Compresión** por bloque según el tipo.

**Componentes:**
- **Metadata DB** (relacional): usuarios, archivos, versiones, qué bloques componen cada archivo.
- **Block storage** (cloud, S3-like) para los bloques en sí.
- **Servicio de notificación** para avisar a los otros dispositivos que hay cambios → bajan solo los deltas.

**Consistencia:** caché y BD deben coincidir; al subir, se confirma metadata solo tras persistir todos los bloques.

**Conflictos:** si dos clientes editan el mismo archivo, el primero en llegar gana y al segundo se le presenta una versión en conflicto para reconciliar (estilo "tu copia / su copia").

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Mensajería en tiempo real bidireccional" | WebSocket (conexión persistente), no polling |
| "Servicio que mantiene conexiones vivas" | Tier con estado (chat) separado del stateless |
| "Online/offline de contactos" | Heartbeat + pub/sub |
| "Sugerencias mientras tecleas, <100 ms" | Trie con top-k cacheadas en cada nodo |
| "Trie demasiado grande" | Sharding por prefijo balanceado por popularidad |
| "Servir video/imágenes global" | CDN + transcodificación a múltiples bitrates |
| "Ancho de banda variable del cliente" | Adaptive bitrate streaming |
| "Sincronizar archivos entre dispositivos" | Block storage + delta sync + dedup |
| "No re-subir el archivo entero al editar" | Delta sync: solo los bloques cambiados |

---

> **Síntesis:** Lo de tiempo real exige cambiar el modelo petición-respuesta: WebSocket para chat, heartbeat para presencia. Lo de medios y archivos exige acercar los datos (CDN) y mover lo mínimo (transcodificar a varios bitrates, sincronizar solo deltas de bloques). El hilo común con las unidades previas: precomputar y cachear lo que se lee mucho (top-k en nodos del trie, video popular en CDN) y desacoplar el trabajo pesado en pipelines (transcodificación como DAG, igual que las colas de notificaciones).

---

*Retrieval: cierra y responde: (1) ¿por qué WebSocket y no long polling para chat?; (2) ¿qué cachea cada nodo del trie y por qué importa?; (3) ¿qué es adaptive bitrate streaming?; (4) explica delta sync con block storage y qué ahorra.*
