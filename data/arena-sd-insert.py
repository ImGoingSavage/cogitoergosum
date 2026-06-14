"""
Tanda 8: System Design Interview (Alex Xu) — 60 preguntas, 4 unidades
=====================================================================
Ruta maang (§10). IDs calculados dinámicamente sobre la base ya integrada.

Flujo:
  git pull --rebase origin main
  python3 data/arena-sd-insert.py
  # luego: sw.js VERSION → v36 + 4 teoría al SHELL; ledger → completado
  git add ... && git commit ... && git push

Heurísticas nuevas (dominio diseño de sistemas):
  estimacion-capacidad, trade-off-cap, descomponer-sistema,
  escalar-horizontal, cola-desacoplar
"""

import json

with open('data/study.json', 'r', encoding='utf-8') as f:
    study = json.load(f)

# ─── Heurísticas nuevas ───────────────────────────────────────────────────────
new_heuristicas = [
    {
        "id": "descomponer-sistema",
        "nombre": "Descomponer el sistema",
        "descripcion": "Parte un problema vago en componentes con responsabilidades claras: clientes, balanceador, servidores sin estado, caché, base de datos, CDN, colas.",
        "cuando_usar": "Ante un enunciado abierto ('diseña X'). Primero el diagrama de cajas y el flujo de datos, luego cada caja en profundidad.",
        "ejemplo": "News feed = servicio de publicación + fanout + caché de feed + BD de posts.",
        "patron": "Marco de 4 pasos: alcance → alto nivel → profundidad → cierre"
    },
    {
        "id": "estimacion-capacidad",
        "nombre": "Estimación de capacidad",
        "descripcion": "Calcula orden de magnitud de QPS, almacenamiento, ancho de banda y número de servidores con supuestos explícitos y redondeo.",
        "cuando_usar": "Para dimensionar el sistema y justificar decisiones (caché, sharding). El proceso importa más que la cifra exacta.",
        "ejemplo": "DAU × acciones/día / 86400 = QPS; pico ≈ 2× QPS.",
        "patron": "Supuestos → QPS → storage → servidores; etiqueta unidades"
    },
    {
        "id": "escalar-horizontal",
        "nombre": "Escalar horizontalmente",
        "descripcion": "Añade máquinas en vez de agrandarlas: tier sin estado tras un balanceador, réplicas de lectura, sharding de la BD y caché.",
        "cuando_usar": "Cuando una sola máquina no basta o necesitas redundancia. Mueve el estado a un almacén compartido.",
        "ejemplo": "Servidores web stateless + sesión en Redis → cualquier nodo atiende cualquier petición.",
        "patron": "Stateless tier + réplicas + sharding + caché"
    },
    {
        "id": "trade-off-cap",
        "nombre": "Trade-off CAP / consistencia",
        "descripcion": "Ante una partición de red, elige entre consistencia (CP) y disponibilidad (AP); ajusta el grado con quórum N/W/R (W+R>N = consistencia fuerte).",
        "cuando_usar": "Al diseñar almacenamiento replicado distribuido. Banca → CP; feed social → AP.",
        "ejemplo": "N=3, W=R=2 → W+R>N garantiza un nodo solapado con el dato fresco.",
        "patron": "CP vs AP; dial N/W/R; consistencia eventual + reconciliación"
    },
    {
        "id": "cola-desacoplar",
        "nombre": "Desacoplar con colas",
        "descripcion": "Inserta una cola de mensajes entre productor y consumidor para absorber picos, procesar asíncrono y escalar workers de forma independiente.",
        "cuando_usar": "Cuando un pico de tráfico hunde un componente lento, o cuando un proveedor externo puede caerse sin que se pierda el trabajo.",
        "ejemplo": "Notificaciones: servicios → cola por canal → workers → APNs/FCM.",
        "patron": "Productor → cola → worker; at-least-once + idempotencia"
    },
]

existing_ids = {h['id'] for h in study['catalogoHeuristicas']}
for h in new_heuristicas:
    if h['id'] not in existing_ids:
        study['catalogoHeuristicas'].append(h)
        print(f"Heurística añadida: {h['id']}")
    else:
        print(f"Heurística ya existe (skip): {h['id']}")

# Máx orden en fase-7
max_ord = max((u.get('orden', 0) for u in study['unidades'] if u.get('bloque') == 'fase-7'), default=0)
print(f"Max orden fase-7 (post-pull): {max_ord}")

# ─── arena-sd1: Fundamentos de escalabilidad y estimación ────────────────────
unit_sd1 = {
    "id": "arena-sd1",
    "bloque": "fase-7",
    "orden": max_ord + 1,
    "titulo": "Fundamentos de escalabilidad y estimación",
    "libro": "System Design Interview – An Insider's Guide (Alex Xu)",
    "lectura": "data/teoria/arena-sd1.md",
    "dosis": 30,
    "objetivo": "Escalar de un servidor a millones de usuarios, estimar capacidad y aplicar el marco de 4 pasos de la entrevista.",
    "heuristicas": ["descomponer-sistema", "estimacion-capacidad", "escalar-horizontal"],
    "metadata": {"ruta": "maang", "nivel": 2},
    "ideas_clave": [
        "Tier web stateless: el estado vive en un almacén compartido, no en el servidor",
        "Estimar es orden de magnitud: DAU → QPS → storage, redondeando",
        "El proceso de la entrevista (preguntar, acordar, trade-offs) vale más que el diagrama"
    ],
    "banco": [
        {"id": "arsd1-q1", "tipo": "concepto", "enunciado": "¿Por qué el tier de servidores web debe ser stateless y dónde se guarda entonces la sesión del usuario?", "solucion": "Stateless = cualquier servidor atiende cualquier petición → escala horizontal y tolera caídas. La sesión va en un almacén compartido (Redis, BD), no en la memoria del servidor.", "explicacion": "Si la sesión vive en un servidor concreto, el load balancer debe pegar al usuario a ese servidor (sticky session) y una caída pierde la sesión. Externalizar el estado permite añadir/quitar servidores libremente."},
        {"id": "arsd1-q2", "tipo": "concepto", "enunciado": "Compara escalado vertical y horizontal: ¿por qué a gran escala el horizontal es obligatorio?", "solucion": "Vertical = máquina más potente (tope físico, punto único de fallo). Horizontal = más máquinas (casi ilimitado, redundante). A gran escala no hay máquina suficiente y necesitas redundancia ante fallos.", "explicacion": "Vertical es más simple y vale para tráfico bajo, pero no da failover. Horizontal exige un tier sin estado y un balanceador, a cambio de escalabilidad real."},
        {"id": "arsd1-q3", "tipo": "calculo", "enunciado": "Una app tiene 100 millones de usuarios activos diarios que hacen 5 acciones al día en promedio. Estima el QPS promedio y el QPS pico.", "solucion": "QPS = 100M × 5 / 86400 ≈ 5.8M / 86400 ≈ 5787 ≈ ~5800 QPS. Pico ≈ 2× ≈ ~11600 QPS.", "explicacion": "500M acciones/día entre 86400 s ≈ 5800 QPS. La regla de pulgar es pico ≈ 2× el promedio. Se redondea: la precisión no importa, el orden de magnitud sí."},
        {"id": "arsd1-q4", "tipo": "calculo", "enunciado": "¿Cuánto downtime al año implica una disponibilidad de 99.99% (cuatro nueves)? ¿Y 99.9%?", "solucion": "99.99% ≈ 52.6 minutos/año. 99.9% ≈ 8.76 horas/año.", "explicacion": "Año = 525600 min. 0.01% de 525600 ≈ 52.6 min; 0.1% ≈ 526 min ≈ 8.76 h. Cada nueve adicional reduce el downtime ~10× y cuesta exponencialmente más."},
        {"id": "arsd1-q5", "tipo": "concepto", "enunciado": "Describe la estrategia de caché read-through (cache-aside) y tres consideraciones al usarla.", "solucion": "La app consulta la caché; si hay miss, lee la BD y rellena la caché. Consideraciones: (1) TTL adecuado (ni rancio ni muchos miss), (2) consistencia caché-BD (invalidación), (3) evicción (LRU) y evitar punto único de fallo con varios nodos.", "explicacion": "Ideal para datos que se leen mucho y cambian poco. El reto es mantener caché y BD sincronizadas cuando el dato se actualiza."},
        {"id": "arsd1-q6", "tipo": "concepto", "enunciado": "¿Qué es una CDN y qué tipo de contenido conviene servir desde ella?", "solucion": "Una CDN es una red de caché geográficamente distribuida que sirve contenido estático (imágenes, JS, CSS, video) desde el nodo más cercano al usuario.", "explicacion": "Reduce latencia (los bytes viajan menos) y descarga tus servidores. Las decisiones clave son TTL, invalidación y el costo por transferencia. El contenido dinámico/personalizado no se cachea bien en CDN."},
        {"id": "arsd1-q7", "tipo": "concepto", "enunciado": "Enumera en orden los pasos típicos para escalar de un solo servidor hacia millones de usuarios.", "solucion": "1) Un servidor; 2) separar la BD; 3) load balancer + servidores web stateless; 4) replicación de BD (primaria/réplicas); 5) caché + CDN; 6) sesiones en almacén compartido; 7) múltiples datacenters; 8) cola de mensajes + sharding.", "explicacion": "Es una secuencia incremental: cada paso ataca el cuello de botella que apareció en el anterior. No se salta de 1 a 8 de golpe."},
        {"id": "arsd1-q8", "tipo": "concepto", "enunciado": "En el marco de 4 pasos de la entrevista de diseño, ¿qué se hace en el Paso 1 y por qué es el más importante?", "solucion": "Paso 1 = entender el problema y fijar el alcance: hacer preguntas (features, escala, usuarios, crecimiento) y anotar supuestos. Es crítico porque el enunciado es vago y diseñar sin entender los requisitos es bandera roja.", "explicacion": "El libro lo ilustra con 'no seas como Jimmy': responder rápido sin entender no da puntos. Aclarar ambigüedades evita diseñar el sistema equivocado."},
        {"id": "arsd1-q9", "tipo": "concepto", "enunciado": "¿Qué es la 'sobre-ingeniería' y por qué es una bandera roja en una entrevista de diseño?", "solucion": "Diseñar complejidad innecesaria por 'pureza' ignorando trade-offs y costos. Es bandera roja porque demuestra falta de juicio: lo simple que cumple los requisitos es mejor.", "explicacion": "Los sistemas sobre-ingenierizados tienen costos compuestos (mantenimiento, operación). El entrevistador busca pragmatismo, no el diseño más sofisticado posible."},
        {"id": "arsd1-q10", "tipo": "concepto", "enunciado": "Ordena de más rápida a más lenta: lectura de SSD aleatoria, referencia a memoria principal, round trip intercontinental, seek de disco duro (HDD).", "solucion": "Memoria (~100 ns) < SSD aleatorio (~150 µs) < seek HDD (~10 ms) < round trip intercontinental (~150 ms).", "explicacion": "Saltan órdenes de magnitud: memoria en ns, SSD en µs, disco mecánico y red intercontinental en ms. Conclusión de diseño: evita seeks de disco y datacenters lejanos en la ruta crítica."},
        {"id": "arsd1-q11", "tipo": "calculo", "enunciado": "Estima el almacenamiento de medios a 5 años de una red social con 150M usuarios diarios que suben 2 posts/día, donde el 10% tiene una imagen de 1 MB.", "solucion": "Diario: 150M × 2 × 10% × 1MB = 30 TB/día. A 5 años: 30 TB × 365 × 5 ≈ 55 PB.", "explicacion": "30M imágenes/día × 1 MB = 30 TB/día. Multiplicado por ~1825 días ≈ 55 PB. Este cálculo justifica decisiones de storage distribuido y CDN."},
        {"id": "arsd1-q12", "tipo": "concepto", "enunciado": "¿Para qué sirven las réplicas de lectura en una base de datos y qué problema introducen?", "solucion": "Reparten las lecturas (primaria para escrituras, réplicas para lecturas) → escalan la lectura. Problema: lag de replicación → una lectura justo tras una escritura puede ver datos rancios (consistencia eventual).", "explicacion": "Sirve cuando lecturas >> escrituras (lo común). El lag se mitiga leyendo de la primaria datos recién escritos cuando la frescura es crítica."},
        {"id": "arsd1-q13", "tipo": "concepto", "enunciado": "¿Qué política de evicción de caché es la más común y qué decide?", "solucion": "LRU (Least Recently Used): cuando la caché se llena, expulsa el elemento usado hace más tiempo.", "explicacion": "Asume localidad temporal: lo recién usado se volverá a usar. Alternativas: LFU (menos frecuente), FIFO. La elección depende del patrón de acceso."},
        {"id": "arsd1-q14", "tipo": "concepto", "enunciado": "En el Paso 4 (cerrar) de la entrevista, ¿qué cuatro cosas conviene mencionar?", "solucion": "Cuellos de botella y puntos únicos de fallo; qué monitorear y métricas; manejo de errores/fallos; y cómo escalaría a 10× (qué cambiaría).", "explicacion": "El cierre demuestra visión operativa: no basta el 'happy path', hay que anticipar fallos, observabilidad y crecimiento futuro. También reconocer lo que quedó fuera por tiempo."},
        {"id": "arsd1-q15", "tipo": "calculo", "enunciado": "¿Cuántos bytes hay en un TB y en un PB usando potencias de 2, y por qué importa la convención?", "solucion": "1 TB = 2⁴⁰ bytes ≈ 10¹²; 1 PB = 2⁵⁰ bytes ≈ 10¹⁵. Importa para que las estimaciones de almacenamiento sean correctas y consistentes.", "explicacion": "KB=2¹⁰, MB=2²⁰, GB=2³⁰, TB=2⁴⁰, PB=2⁵⁰. Aunque en estimaciones se aproxima a potencias de 10, conocer la base 2 evita errores de factor en cálculos de capacidad."}
    ]
}

# ─── arena-sd2: Bloques distribuidos fundamentales ───────────────────────────
unit_sd2 = {
    "id": "arena-sd2",
    "bloque": "fase-7",
    "orden": max_ord + 2,
    "titulo": "Bloques distribuidos fundamentales",
    "libro": "System Design Interview – An Insider's Guide (Alex Xu)",
    "lectura": "data/teoria/arena-sd2.md",
    "dosis": 30,
    "objetivo": "Dominar rate limiter, consistent hashing, CAP/quórum, vector clocks y generación de IDs Snowflake.",
    "heuristicas": ["trade-off-cap", "escalar-horizontal", "hashing-memoria"],
    "metadata": {"ruta": "maang", "nivel": 3},
    "ideas_clave": [
        "Consistent hashing mueve solo k/n claves al reescalar (vs hash%n que mueve casi todas)",
        "CAP fuerza CP vs AP; quórum W+R>N da consistencia fuerte",
        "Snowflake: 64 bits = timestamp(41)+datacenter(5)+máquina(5)+secuencia(12)"
    ],
    "banco": [
        {"id": "arsd2-q1", "tipo": "concepto", "enunciado": "Nombra cinco algoritmos de rate limiting y di cuál es el más usado y por qué.", "solucion": "Token bucket, leaking bucket, fixed window counter, sliding window log, sliding window counter. El más usado es token bucket: simple y permite ráfagas controladas (Amazon, Stripe).", "explicacion": "Token bucket rellena tokens a tasa fija; cada petición consume uno. Permite picos hasta el tamaño del bucket. Los demás trade-offs: fixed window tiene el problema del borde, sliding log es preciso pero pesado."},
        {"id": "arsd2-q2", "tipo": "concepto", "enunciado": "¿Qué código HTTP devuelve un rate limiter al rechazar, y qué cabeceras informativas suele incluir?", "solucion": "HTTP 429 (Too Many Requests). Cabeceras: X-Ratelimit-Limit, X-Ratelimit-Remaining, Retry-After.", "explicacion": "El 429 indica al cliente que se pase de cuota; Retry-After le dice cuándo reintentar. Las cabeceras permiten al cliente autorregularse sin adivinar."},
        {"id": "arsd2-q3", "tipo": "concepto", "enunciado": "¿Por qué 'servidor = hash(key) % n' es problemático al añadir o quitar un servidor, y cómo lo resuelve el consistent hashing?", "solucion": "Con módulo n, cambiar n remapea casi todas las claves → tormenta de cache miss. El consistent hashing coloca servidores y claves en un anillo; al añadir/quitar un nodo solo se mueven k/n claves (las de un segmento).", "explicacion": "El módulo cambia el destino de casi cada clave porque n está en el denominador. El anillo localiza el impacto al vecindario del nodo afectado."},
        {"id": "arsd2-q4", "tipo": "concepto", "enunciado": "¿Qué problema resuelven los nodos virtuales (vnodes) en consistent hashing?", "solucion": "Reducen la varianza del reparto (distribución más uniforme de claves) y permiten heterogeneidad: un servidor más potente recibe más vnodes.", "explicacion": "Con pocos puntos por servidor, el reparto del anillo es desigual. Muchos vnodes promedian mejor. El costo es más metadatos que mantener."},
        {"id": "arsd2-q5", "tipo": "concepto", "enunciado": "Enuncia el teorema CAP y explica por qué en la práctica eliges entre CP y AP (no CA).", "solucion": "CAP: un sistema distribuido no puede dar a la vez consistencia, disponibilidad y tolerancia a particiones; ante una partición eliges dos. CA no es real porque la partición de red es inevitable, así que siempre necesitas P y eliges entre C y A.", "explicacion": "Cuando la red se parte, o bloqueas escrituras para no servir datos inconsistentes (CP) o sigues sirviendo aunque sean rancios (AP). No puedes renunciar a tolerar particiones en un sistema distribuido real."},
        {"id": "arsd2-q6", "tipo": "concepto", "enunciado": "Da un ejemplo de sistema que debe ser CP y uno que debe ser AP, justificando.", "solucion": "CP: sistema bancario (el saldo debe ser exacto; mejor dar error que un dato inconsistente). AP: feed de red social (tolera ver posts un poco rancios con tal de seguir disponible).", "explicacion": "El criterio es el costo de la inconsistencia: en banca es inaceptable; en un feed es tolerable. El diseño se ajusta al caso de uso."},
        {"id": "arsd2-q7", "tipo": "calculo", "enunciado": "En un KV store con N=3 réplicas, ¿qué valores de W y R dan consistencia fuerte y por qué?", "solucion": "W=2, R=2 (W+R=4 > N=3). Consistencia fuerte requiere W+R>N para que haya al menos un nodo solapado entre el conjunto de escritura y el de lectura, garantizando leer el dato más reciente.", "explicacion": "Si los 2 nodos que confirman la escritura y los 2 que responden la lectura suman más que 3, por el principio del palomar comparten al menos un nodo con el valor fresco."},
        {"id": "arsd2-q8", "tipo": "concepto", "enunciado": "¿Cómo se optimiza un quórum para lectura rápida y cómo para escritura rápida?", "solucion": "Lectura rápida: R=1, W=N (lees de cualquier réplica, pero escribir es lento). Escritura rápida: W=1, R=N (confirmas la escritura con una réplica, pero leer es lento).", "explicacion": "W y R grandes aumentan la consistencia a costa de latencia (esperas al nodo más lento). Es un dial que se ajusta según si dominan lecturas o escrituras."},
        {"id": "arsd2-q9", "tipo": "concepto", "enunciado": "Distingue consistencia fuerte, débil y eventual. ¿Cuál adoptan Dynamo y Cassandra?", "solucion": "Fuerte: toda lectura ve la última escritura. Débil: puede no verla. Eventual (forma de débil): con tiempo suficiente todas las réplicas convergen. Dynamo y Cassandra adoptan consistencia eventual.", "explicacion": "La fuerte bloquea operaciones hasta que todas las réplicas concuerden → mala para alta disponibilidad. La eventual permite alta disponibilidad y reconcilia conflictos después."},
        {"id": "arsd2-q10", "tipo": "concepto", "enunciado": "¿Qué es un vector clock y qué resuelve que un timestamp simple no puede?", "solucion": "Un vector clock es un conjunto de pares [servidor, versión] asociado a un dato. Detecta si una versión es ancestro, descendiente o está en conflicto con otra. Un timestamp simple no distingue escrituras concurrentes (conflicto) de secuenciales.", "explicacion": "Versión X es ancestro de Y si cada contador de X ≤ el de Y. Si ninguna domina a la otra, son hermanas → conflicto que el cliente reconcilia. El timestamp solo da orden total, perdiendo la causalidad."},
        {"id": "arsd2-q11", "tipo": "concepto", "enunciado": "¿Cómo detecta un KV store distribuido que un nodo se cayó, usando gossip protocol?", "solucion": "Cada nodo mantiene una lista de miembros con heartbeat counters, incrementa el suyo periódicamente y lo propaga a nodos aleatorios. Si el heartbeat de un nodo no sube en cierto tiempo, se marca caído y se propaga.", "explicacion": "Es descentralizado y escala mejor que all-to-all multicast. Suele requerir confirmación de varias fuentes antes de marcar a un nodo como caído, para evitar falsos positivos."},
        {"id": "arsd2-q12", "tipo": "concepto", "enunciado": "¿Qué es hinted handoff y qué es anti-entropy con Merkle trees? ¿Qué tipo de fallo ataca cada uno?", "solucion": "Hinted handoff (fallo temporal): otro nodo acepta las escrituras del caído y se las entrega al volver. Anti-entropy con Merkle trees (fallo permanente / desincronización): árbol de hashes de rangos; comparas raíces y bajas solo por las ramas que difieren para sincronizar el mínimo.", "explicacion": "Hinted handoff mantiene la disponibilidad de escritura mientras un nodo está caído brevemente. Merkle trees evitan comparar todos los datos: solo transfieres lo que difiere."},
        {"id": "arsd2-q13", "tipo": "concepto", "enunciado": "Describe el write path y el read path de un KV store estilo Cassandra (LSM).", "solucion": "Write: commit log (durabilidad) → memtable en memoria → al llenarse, flush a SSTable inmutable en disco. Read: consulta memtable; si falla, usa un bloom filter para saber en qué SSTable podría estar antes de tocar disco.", "explicacion": "Las escrituras son secuenciales (rápidas). El bloom filter evita lecturas de disco inútiles: si dice 'no está', no está; si dice 'quizá', vale la pena buscar."},
        {"id": "arsd2-q14", "tipo": "concepto", "enunciado": "Para generar IDs únicos distribuidos, ¿por qué se descartan auto-increment de BD y UUID, y qué ofrece Snowflake?", "solucion": "Auto-increment no escala horizontalmente (coordinación central). UUID (128 bits) es único pero no numérico ni ordenable por tiempo. Snowflake da IDs de 64 bits, únicos, numéricos y ordenables por tiempo, sin coordinación entre nodos.", "explicacion": "Snowflake pone el timestamp en los bits altos → orden creciente. Cada máquina genera localmente, evitando un punto único de fallo o cuello de botella."},
        {"id": "arsd2-q15", "tipo": "calculo", "enunciado": "Reparte los 64 bits de un ID Snowflake y di cuántos IDs por milisegundo puede emitir una máquina.", "solucion": "1 bit signo + 41 timestamp + 5 datacenter + 5 máquina + 12 secuencia = 64. Con 12 bits de secuencia, 2¹² = 4096 IDs por milisegundo por máquina.", "explicacion": "41 bits de ms dan ~69 años desde una época propia. 5+5 bits = 32 datacenters × 32 máquinas. La secuencia de 12 bits evita colisiones dentro del mismo ms en la misma máquina."}
    ]
}

# ─── arena-sd3: Sistemas de datos a escala ───────────────────────────────────
unit_sd3 = {
    "id": "arena-sd3",
    "bloque": "fase-7",
    "orden": max_ord + 3,
    "titulo": "Sistemas de datos a escala",
    "libro": "System Design Interview – An Insider's Guide (Alex Xu)",
    "lectura": "data/teoria/arena-sd3.md",
    "dosis": 30,
    "objetivo": "Diseñar acortador de URLs, web crawler, sistema de notificaciones y news feed, eligiendo entre precomputar y desacoplar.",
    "heuristicas": ["cola-desacoplar", "descomponer-sistema", "estimacion-capacidad"],
    "metadata": {"ruta": "maang", "nivel": 2},
    "ideas_clave": [
        "El cuello de botella suele ser lectura: precomputar y cachear (URL corta, feed)",
        "Las colas desacoplan y absorben picos (notificaciones, fanout)",
        "Fanout on write vs on read: la solución a escala es híbrida"
    ],
    "banco": [
        {"id": "arsd3-q1", "tipo": "calculo", "enunciado": "En un acortador de URLs con base62, ¿cuántas URLs distintas representa una clave de 7 caracteres y por qué basta?", "solucion": "62⁷ ≈ 3.5 billones (3.5 × 10¹²). Basta para años de operación incluso con millones de URLs nuevas al día.", "explicacion": "Base62 = [a-zA-Z0-9] = 62 símbolos. 62⁷ ≈ 3.5T. Más caracteres dan más espacio pero URLs más largas; 7 es el equilibrio típico."},
        {"id": "arsd3-q2", "tipo": "concepto", "enunciado": "Al redirigir una URL corta, ¿cuándo usas 301 y cuándo 302, y qué pierdes con cada uno?", "solucion": "301 (permanente): el navegador cachea → menos carga en tu servidor pero pierdes analítica de clics. 302 (temporal): cada visita pasa por tu servidor → buena analítica pero más carga.", "explicacion": "El trade-off es carga vs visibilidad: 301 descarga tu servidor sacrificando datos de uso; 302 te deja contar cada clic a cambio de procesar cada redirección."},
        {"id": "arsd3-q3", "tipo": "concepto", "enunciado": "Compara los dos enfoques para generar la clave corta: hash con resolución de colisiones vs conversión de base (ID→base62).", "solucion": "Hash+sal: recortas un hash de la URL; si choca, reintentas → requiere chequear la BD. ID→base62: un generador de ID único da un entero creciente que conviertes a base62 → sin colisiones ni chequeo, pero la clave es predecible (enumerable).", "explicacion": "El trade-off es seguridad/privacidad (no enumerable) vs simplicidad (sin chequeo de colisión). Si la enumeración es un riesgo, el hash es mejor pese al chequeo."},
        {"id": "arsd3-q4", "tipo": "concepto", "enunciado": "¿Qué es el URL frontier en un web crawler y qué dos responsabilidades clave tiene?", "solucion": "Es la cola de URLs por visitar. Gestiona (1) prioridad (qué URLs visitar antes, por importancia/frescura) y (2) politeness (no martillear un mismo host).", "explicacion": "El crawler es un BFS sobre el grafo web; el frontier es esa cola. Sin prioridad ni politeness, un crawler ingenuo desperdicia recursos y abusa de hosts."},
        {"id": "arsd3-q5", "tipo": "concepto", "enunciado": "¿Cómo implementa un crawler la 'politeness' para no sobrecargar un mismo servidor?", "solucion": "Una cola por host con un solo worker procesándola, más un delay entre peticiones al mismo host; y respetar robots.txt.", "explicacion": "Mapear cada host a una cola dedicada garantiza que las peticiones a un host se serialicen con espaciamiento, en vez de dispararlas en paralelo."},
        {"id": "arsd3-q6", "tipo": "concepto", "enunciado": "¿Cómo evita un crawler procesar contenido duplicado de forma eficiente en memoria?", "solucion": "Calcula un hash/checksum del contenido y lo consulta en un bloom filter (o conjunto de hashes). Si ya se vio, se ignora.", "explicacion": "~30% de la web está duplicada. Un bloom filter da pertenencia probabilística con muy poca memoria (sin falsos negativos), ideal para descartar duplicados a escala."},
        {"id": "arsd3-q7", "tipo": "concepto", "enunciado": "Nombra tres 'trampas' de la web que un crawler robusto debe manejar.", "solucion": "Spider traps (URLs de profundidad infinita → límite de longitud de ruta), páginas duplicadas/réplicas (dedup por hash), y HTML malo / servidores lentos o caídos (timeouts y reintentos).", "explicacion": "La robustez es tan importante como la escala: la web está llena de casos límite que pueden colgar o desperdiciar el crawler si no se anticipan."},
        {"id": "arsd3-q8", "tipo": "concepto", "enunciado": "En un sistema de notificaciones, ¿por qué se coloca una cola de mensajes entre los servidores de notificación y los proveedores (APNs/FCM/SMS)?", "solucion": "Para desacoplar: si un proveedor se cae o se ralentiza, los mensajes esperan en la cola en vez de perderse o bloquear al productor. Permite absorber picos y escalar los workers independientemente.", "explicacion": "Sin la cola, un proveedor lento propagaría su latencia a todo el sistema. La cola convierte la entrega en asíncrona y resiliente."},
        {"id": "arsd3-q9", "tipo": "concepto", "enunciado": "¿Qué canales de notificación hay y qué proveedor de terceros se usa para cada uno?", "solucion": "Push iOS → APNs; push Android → FCM; SMS → Twilio/Nexmo; email → SendGrid/Mailchimp.", "explicacion": "Cada plataforma exige su propio servicio de entrega. El sistema arma el payload adecuado y lo enruta a la cola del canal correcto."},
        {"id": "arsd3-q10", "tipo": "concepto", "enunciado": "¿Cómo se garantiza no perder ni duplicar notificaciones?", "solucion": "No perder: persistir en una BD de logs y reintentar los fallidos (entrega at-least-once). No duplicar: una clave de idempotencia/deduplicación; si el evento ya se procesó, se descarta.", "explicacion": "Exactly-once es prácticamente imposible en sistemas distribuidos, así que se combina at-least-once (reintentos) con deduplicación en el consumidor."},
        {"id": "arsd3-q11", "tipo": "concepto", "enunciado": "Explica el trade-off entre fanout on write y fanout on read en un news feed.", "solucion": "On write (push): al publicar, copias el post al feed de cada amigo → lectura instantánea pero escritura cara O(amigos). On read (pull): al abrir el feed, agregas los posts de los amigos → escritura barata pero lectura lenta.", "explicacion": "Push precomputa el feed (rápido al leer, caro al escribir); pull lo computa al vuelo (barato al escribir, lento al leer). La elección depende de si dominan lecturas o escrituras."},
        {"id": "arsd3-q12", "tipo": "concepto", "enunciado": "¿Qué es el problema de 'hotkey' en fanout on write y cómo lo resuelve el enfoque híbrido?", "solucion": "Hotkey: una celebridad con millones de seguidores dispara millones de escrituras por cada post. El híbrido usa fanout on write para usuarios normales y fanout on read para celebridades, evitando la tormenta de escritura.", "explicacion": "Así los feeds normales siguen siendo rápidos (precomputados) y los posts de celebridades se agregan en tiempo de lectura, eludiendo el cuello de botella de escritura."},
        {"id": "arsd3-q13", "tipo": "concepto", "enunciado": "¿Cómo se almacena un news feed para leerlo rápido y qué se guarda exactamente?", "solucion": "El feed se cachea (Redis) como una lista de post_id; el contenido completo de cada post se hidrata por separado desde la BD/caché de posts.", "explicacion": "Guardar solo IDs mantiene el feed compacto y barato de actualizar; la hidratación separa la estructura del feed del contenido, que puede cambiar (ediciones, borrados)."},
        {"id": "arsd3-q14", "tipo": "calculo", "enunciado": "Un acortador recibe 100 escrituras/s (URLs nuevas) y una proporción lectura:escritura de 10:1. ¿Cuál es el QPS de lectura y qué implica para el diseño?", "solucion": "Lecturas = 10 × 100 = 1000 QPS. El sistema es read-heavy → el diseño se centra en caché de redirecciones y réplicas de lectura, no en la escritura.", "explicacion": "La redirección (lectura) domina. Una caché de las URLs populares absorbe la mayoría de las lecturas; la escritura es comparativamente trivial."},
        {"id": "arsd3-q15", "tipo": "concepto", "enunciado": "¿Por qué un 'BFS simple' no basta para un web crawler a escala real?", "solucion": "Porque BFS puro trata todas las URLs igual: no prioriza por importancia/frescura, no aplica politeness (martillearía hosts) ni deduplica. A escala se necesita un frontier con prioridad, colas por host y dedup.", "explicacion": "El algoritmo base (descargar, extraer enlaces, repetir) es correcto pero ingenuo. La complejidad real está en hacerlo escalable, educado y robusto."}
    ]
}

# ─── arena-sd4: Sistemas en tiempo real y de medios ──────────────────────────
unit_sd4 = {
    "id": "arena-sd4",
    "bloque": "fase-7",
    "orden": max_ord + 4,
    "titulo": "Sistemas en tiempo real y de medios",
    "libro": "System Design Interview – An Insider's Guide (Alex Xu)",
    "lectura": "data/teoria/arena-sd4.md",
    "dosis": 30,
    "objetivo": "Diseñar chat, autocompletado, YouTube y Google Drive: tiempo real con WebSocket y medios con CDN, transcodificación y delta sync.",
    "heuristicas": ["cola-desacoplar", "trade-off-cap", "descomponer-sistema"],
    "metadata": {"ruta": "maang", "nivel": 3},
    "ideas_clave": [
        "Tiempo real rompe petición-respuesta: WebSocket (chat), heartbeat (presencia)",
        "Medios: acerca los datos (CDN) y mueve lo mínimo (transcodificar, delta sync)",
        "Trie con top-k cacheadas en cada nodo para autocompletar en <100 ms"
    ],
    "banco": [
        {"id": "arsd4-q1", "tipo": "concepto", "enunciado": "Para un chat en tiempo real, compara polling, long polling y WebSocket. ¿Cuál se elige y por qué?", "solucion": "Polling: el cliente pregunta cada X s (desperdicia recursos). Long polling: el servidor mantiene la petición abierta hasta tener algo (mejor, pero reconexiones). WebSocket: conexión persistente y bidireccional; el servidor empuja cuando quiere → la elegida.", "explicacion": "HTTP normal lo inicia el cliente; el servidor no puede empujar. WebSocket hace upgrade desde HTTP a una conexión full-duplex sobre un puerto, ideal para mensajería instantánea."},
        {"id": "arsd4-q2", "tipo": "concepto", "enunciado": "¿Por qué el servicio de chat es 'con estado' mientras otros servicios son stateless, y qué implica?", "solucion": "Porque mantiene vivas las conexiones WebSocket: un cliente queda pegado a un servidor concreto durante la sesión. Implica gestionar esas conexiones, su balanceo y la reconexión, separándolo de los servicios stateless (login, perfil).", "explicacion": "El estado es la conexión persistente. No puedes tratarlo como un tier web cualquiera; necesita un service discovery que sepa a qué servidor está conectado cada usuario."},
        {"id": "arsd4-q3", "tipo": "concepto", "enunciado": "¿Por qué se usa un KV store en vez de una BD relacional para los mensajes de chat, y qué propiedad debe tener el message_id?", "solucion": "Por el enorme volumen y el patrón de acceso simple por clave (par de usuarios o channel_id). El message_id debe ser único y ordenable por tiempo (secuencia local creciente) para ordenar la conversación.", "explicacion": "Los mensajes son muchísimos y se acceden por conversación, no con joins complejos. Un ID ordenable permite reconstruir el orden y sincronizar (pedir mensajes posteriores al último visto)."},
        {"id": "arsd4-q4", "tipo": "concepto", "enunciado": "¿Cómo se implementa el estado de presencia (online/offline) en un chat?", "solucion": "Con heartbeats: el cliente envía una señal periódica; si no llega en X segundos, se marca offline. El cambio se propaga a los contactos por publish/subscribe.", "explicacion": "El heartbeat evita marcar offline a alguien con un lapso breve de red. Pub/sub propaga el cambio solo a quienes les interesa (los contactos), sin difundir a todos."},
        {"id": "arsd4-q5", "tipo": "concepto", "enunciado": "¿Cómo sincroniza un cliente de chat los mensajes tras reconectar?", "solucion": "Cada cliente recuerda el último message_id que vio; al reconectar pide al servidor los mensajes con ID posterior.", "explicacion": "Como el message_id es ordenable, basta un 'dame todo lo que sea mayor que X'. Evita re-descargar la conversación entera y cubre los mensajes perdidos durante la desconexión."},
        {"id": "arsd4-q6", "tipo": "concepto", "enunciado": "En un autocompletado, ¿qué estructura se usa y cuál es la optimización clave para responder en <100 ms?", "solucion": "Un Trie (árbol de prefijos). La optimización clave: cachear en cada nodo las top-k consultas de ese prefijo, para no recorrer todo el subárbol en cada tecla → O(longitud del prefijo).", "explicacion": "Sin la caché por nodo, cada pulsación exigiría explorar el subárbol y rankear. Con las top-k precomputadas en el nodo, la respuesta es casi inmediata."},
        {"id": "arsd4-q7", "tipo": "concepto", "enunciado": "¿Cómo se recolectan y actualizan los datos de popularidad del trie de autocompletado?", "solucion": "Un pipeline de analítica agrega la frecuencia histórica de consultas (logs → agregadores → un Trie builder que reconstruye el trie periódicamente, p.ej. semanal). El trie se sirve desde caché y se replica.", "explicacion": "El ranking no necesita ser en tiempo real: reconstruir el trie cada cierto tiempo basta. Esto separa la ruta de lectura (rápida, cacheada) de la de actualización (batch)."},
        {"id": "arsd4-q8", "tipo": "concepto", "enunciado": "El trie de autocompletado es demasiado grande para una máquina. ¿Cómo se reparte?", "solucion": "Sharding por prefijo (p.ej. iniciales a–m en un shard, n–z en otro), idealmente balanceando por la popularidad real de cada letra inicial, no de forma uniforme.", "explicacion": "Repartir uniformemente por letra desbalancea (hay letras mucho más frecuentes). Balancear por carga real evita que un shard se sature mientras otro está ocioso."},
        {"id": "arsd4-q9", "tipo": "concepto", "enunciado": "En el diseño de YouTube, ¿qué hace el pipeline de transcodificación y por qué es necesario?", "solucion": "Genera múltiples resoluciones y formatos del video original (un DAG de tareas: inspección, codificación, miniaturas, marca de agua). Es necesario porque distintos dispositivos y anchos de banda requieren distintos bitrates.", "explicacion": "Un único archivo no sirve a todos: un móvil con 3G y un TV 4K necesitan versiones distintas. La transcodificación las pre-genera para servirlas según el cliente."},
        {"id": "arsd4-q10", "tipo": "concepto", "enunciado": "¿Qué es el adaptive bitrate streaming y qué problema resuelve?", "solucion": "El video se trocea en segmentos a varios bitrates; el cliente cambia de calidad segmento a segmento según su ancho de banda momentáneo. Resuelve la variabilidad de la conexión del usuario.", "explicacion": "En vez de cortar el video cuando baja la red, baja la calidad y sigue reproduciendo. Mejora la experiencia frente a buffering."},
        {"id": "arsd4-q11", "tipo": "concepto", "enunciado": "Servir todo el video desde CDN es carísimo. ¿Cómo se optimiza el costo?", "solucion": "Distribuir a la CDN solo el contenido popular (modelo push para los virales); el contenido de cola larga (poco visto) se sirve desde servidores propios o CDNs más baratas (pull).", "explicacion": "La distribución de vistas es muy sesgada: un pequeño porcentaje de videos acapara la mayoría del tráfico. Solo vale la pena pre-distribuir esos."},
        {"id": "arsd4-q12", "tipo": "concepto", "enunciado": "En Google Drive, ¿qué es el almacenamiento por bloques y qué es delta sync?", "solucion": "Cada archivo se parte en bloques (p.ej. 4 MB). Delta sync: al modificar un archivo, solo se suben los bloques que cambiaron, no el archivo entero.", "explicacion": "Editar un carácter de un archivo de 1 GB no debería re-subir 1 GB. Trocear en bloques permite transferir solo el delta, ahorrando ancho de banda enorme."},
        {"id": "arsd4-q13", "tipo": "concepto", "enunciado": "¿Cómo separa Google Drive los metadatos del contenido y por qué?", "solucion": "Una metadata DB (relacional) guarda usuarios, archivos, versiones y qué bloques componen cada archivo; un block storage (S3-like) guarda los bloques en sí.", "explicacion": "Los metadatos son pequeños y relacionales (consultas, permisos, versiones); los bloques son grandes y opacos. Separarlos permite escalar y optimizar cada uno por su cuenta."},
        {"id": "arsd4-q14", "tipo": "concepto", "enunciado": "¿Cómo se notifica a los demás dispositivos de un usuario que un archivo cambió en Drive?", "solucion": "Un servicio de notificación avisa a los dispositivos conectados que hay cambios; cada uno baja solo los deltas (bloques modificados) en vez del archivo completo.", "explicacion": "Combina la notificación de cambios con el delta sync: el aviso dispara una sincronización mínima, manteniendo todos los dispositivos al día con poco tráfico."},
        {"id": "arsd4-q15", "tipo": "concepto", "enunciado": "¿Qué hilo común conecta el trie de autocompletado, la CDN de YouTube y el feed precomputado del news feed?", "solucion": "Todos precomputan y cachean lo que se lee mucho: top-k en los nodos del trie, video popular en la CDN, feed como lista de IDs en Redis. Y desacoplan el trabajo pesado en pipelines (transcodificación, fanout, builder del trie).", "explicacion": "Es el patrón central de diseño a escala: acercar/precalcular lo leído masivamente y empujar lo costoso a procesos asíncronos, en vez de calcular en la ruta crítica."}
    ]
}

# ─── Ítems de examen (IDs dinámicos) ──────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        items = bloque['examen']['items']
        nums = [int(it['id'].split('-')[-1]) for it in items]
        last_id = max(nums)
        print(f"Último examen id post-pull: f7-ex-{last_id}")
        next_id1 = last_id + 1
        next_id2 = last_id + 2
        break

ex_next1 = {
    "id": f"f7-ex-{next_id1}",
    "heuristica": "trade-off-cap",
    "enunciado": "Diseñas el almacén de datos de un sistema de pagos y el de un feed de 'me gusta'. Para cada uno: (a) ¿eliges CP o AP ante una partición de red? (b) con N=3 réplicas, ¿qué W y R propones? (c) justifica el contraste.",
    "pistas": [
        "Pregúntate el costo de servir un dato inconsistente en cada caso: ¿qué pasa si el saldo o el conteo de likes está rancio?",
        "CAP: ante partición eliges C o A. Pagos no tolera inconsistencia; un feed sí tolera datos un poco rancios.",
        "Recuerda: W+R>N da consistencia fuerte; W o R = 1 da baja latencia sacrificando consistencia.",
        "Pagos → CP, prioriza consistencia: W=2, R=2 (W+R=4>3). Feed → AP, prioriza disponibilidad/latencia: p.ej. W=1, R=1.",
        "El contraste: el costo de la inconsistencia decide. En pagos es inaceptable (mejor error); en likes es trivial (converge luego, consistencia eventual)."
    ],
    "solucion": "Pagos: CP, W=2/R=2 (W+R>N → consistencia fuerte; mejor rechazar que mostrar saldo erróneo). Feed de likes: AP, W=1/R=1 (baja latencia, alta disponibilidad; el conteo converge por consistencia eventual). El criterio es el costo de la inconsistencia: inaceptable en dinero, tolerable en likes.",
    "disparador": "Señal: 'almacén distribuido replicado, ¿qué garantía?'. Jugada: CAP fuerza CP vs AP según el costo de la inconsistencia; el quórum N/W/R afina el punto (W+R>N = fuerte).",
    "metadata": {
        "ruta": "maang",
        "nivel": 3,
        "skills": ["teorema CAP", "quórum N/W/R", "consistencia vs disponibilidad"],
        "errores_comunes": ["Buscar 'CA' como si fuera viable (la partición es inevitable)", "Dar W/R sin verificar W+R>N para consistencia fuerte"],
        "casos_borde": ["Si la red nunca se particiona, C y A coexisten — pero no se puede asumir", "W=R=N maximiza consistencia pero la latencia sube al nodo más lento"],
        "source": "System Design Interview – An Insider's Guide (Alex Xu) — Cap. 6"
    }
}

ex_next2 = {
    "id": f"f7-ex-{next_id2}",
    "heuristica": "descomponer-sistema",
    "enunciado": "Te piden diseñar el timeline de una red social con 10M usuarios diarios, hasta 5000 amigos por usuario, con algunas cuentas de celebridades de millones de seguidores. (a) ¿Fanout on write u on read? (b) ¿qué problema aparece con las celebridades? (c) propón la arquitectura de almacenamiento del feed.",
    "pistas": [
        "Primero descompón: publicación (escribir el post y propagarlo) vs construcción del feed (agregar posts de amigos).",
        "Fanout on write precomputa el feed (lee rápido, escribe caro O(amigos)); on read agrega al vuelo (escribe barato, lee lento).",
        "¿Qué pasa al hacer fanout on write de un post de alguien con 50M seguidores? Cuenta las escrituras.",
        "El usuario normal: fanout on write. La celebridad: fanout on read (sus posts se agregan al abrir el feed) → evita la tormenta de escritura. Eso es el híbrido.",
        "Almacén: el feed se cachea en Redis como lista de post_id; el contenido se hidrata aparte. Réplicas de lectura para la BD de posts."
    ],
    "solucion": "(a) Híbrido: fanout on write para usuarios normales (feed precomputado, lectura instantánea). (b) Hotkey: una celebridad con millones de seguidores dispararía millones de escrituras por post → para esas cuentas se usa fanout on read (se agregan sus posts al construir el feed). (c) Feed en Redis como lista de post_id, contenido hidratado por separado, réplicas de lectura para la BD de posts.",
    "disparador": "Señal: 'timeline/feed a escala con influencers'. Jugada: descomponer en publicar vs construir; fanout on write por defecto, on read para el caso hotkey; cachear el feed como lista de IDs.",
    "metadata": {
        "ruta": "maang",
        "nivel": 3,
        "skills": ["fanout on write/read", "descomposición de sistema", "caché de feed"],
        "errores_comunes": ["Elegir un solo modelo de fanout para todos los usuarios", "Olvidar el hotkey de las celebridades"],
        "casos_borde": ["Usuario inactivo: precomputar su feed (push) puede ser trabajo desperdiciado", "Usuario con 0 amigos: feed vacío, ningún fanout"],
        "source": "System Design Interview – An Insider's Guide (Alex Xu) — Cap. 11"
    }
}

# ─── Insertar ─────────────────────────────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        bloque['unidades'].extend(['arena-sd1', 'arena-sd2', 'arena-sd3', 'arena-sd4'])
        bloque['examen']['items'].extend([ex_next1, ex_next2])
        print(f"fase-7: {len(bloque['unidades'])} unidades, {len(bloque['examen']['items'])} examen items")
        break

for u in [unit_sd1, unit_sd2, unit_sd3, unit_sd4]:
    study['unidades'].append(u)
    print(f"Unidad: {u['id']} ({len(u['banco'])}q)")

with open('data/study.json', 'w', encoding='utf-8') as f:
    json.dump(study, f, ensure_ascii=False, indent=2)

print("\n✅ study.json actualizado.")
for uid in ['arena-sd1', 'arena-sd2', 'arena-sd3', 'arena-sd4']:
    u = next(x for x in study['unidades'] if x['id'] == uid)
    print(f"  {uid}: {len(u['banco'])}q")

dupes = {}
for u in study['unidades']:
    for q in u.get('banco', []):
        dupes[q['id']] = dupes.get(q['id'], 0) + 1
bad = [(k, v) for k, v in dupes.items() if v > 1]
print(f"Duplicados banco: {bad or 'ninguno'}")
print(f"Total heurísticas: {len(study['catalogoHeuristicas'])}")
print(f"Examen nuevos: {ex_next1['id']}, {ex_next2['id']}")
