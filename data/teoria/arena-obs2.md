# Pilares de la observabilidad: eventos estructurados, trazas y el Core Analysis Loop

## El bloque de construcción: el evento estructurado ancho

El bloque fundamental NO es la métrica ni el log, sino el **evento estructurado arbitrariamente ancho**: un registro de **todo** lo que ocurrió mientras **una petición** interactuó con tu servicio. Se inicializa un mapa vacío al entrar la petición y se le añaden, durante su vida, IDs, parámetros, tiempos, llamadas remotas, etc.; al salir o errar, se emite ese mapa como pares clave-valor (a menudo JSON). Una instrumentación madura suele tener **300-400 dimensiones por evento**.

- **Las métricas no sirven como bloque base**: son **preagregadas** sobre una ventana fija → granularidad demasiado gruesa y rígida; no puedes reconstruir qué le pasó a *una* petición.
- **Los logs no estructurados** son legibles por humanos pero difíciles de procesar; la solución son **logs estructurados** (clave=valor). Un evento ≈ varias líneas de log de una **unidad de trabajo** plegadas en un solo registro.

## Trazas: eventos enlazados

Una **traza distribuida** es simplemente una serie de eventos interrelacionados que sigue **una petición** a través de servicios, procesos y máquinas. Visualización en **cascada (waterfall)**: cada etapa es un **span**. Spans **root** (sin Parent ID) y anidados (relación **padre-hijo**).

**Cinco campos imprescindibles de un span:** `Trace ID` (identifica la petición, lo crea el root y se **propaga**), `Span ID` (identifica el span), `Parent ID` (define el anidamiento; ausente = root), `Timestamp` (inicio) y `Duration` (cuánto tardó). Campos útiles extra: `service_name`, `span_name`, tags (`hostname`, `user_name`, `build_id`…). La propagación entre servicios se hace por **cabeceras HTTP** (estándar W3C o B3: `X-B3-TraceId`, `X-B3-ParentSpanId`).

## OpenTelemetry: instrumentar una sola vez

Las librerías propietarias atan tu código a un proveedor (reinstrumentar para cambiar). **OpenTelemetry (OTel)** es el estándar abierto: instrumentas **una vez** (automática + custom) y envías a múltiples backends.

## Depurar desde primeros principios: el Core Analysis Loop

Un **primer principio** es una verdad básica no deducida de otra. Depurar así = método **científico**, sin asumir nada, en vez de saltar por intuición/«scar tissue» (que no escala con la complejidad). Los **runbooks** que intentan listar toda causa se vuelven obsoletos y peligrosos; la **instrumentación es mejor documentación**.

**Core Analysis Loop** (4 pasos):
1. ¿Qué intentas entender? (qué dijo el cliente/alerta)
2. Visualiza la telemetría para ver una **anomalía** (cambio en una curva).
3. Busca **dimensiones comunes** en la zona anómala: muestra filas, agrupa (`GROUP BY`) y filtra por atributos.
4. ¿Ya sabes qué pasa? Si no, **aísla** esa zona como nuevo punto de partida y vuelve al paso 3.

Es fuerza bruta sobre **todas** las dimensiones sin conocimiento previo. Una herramienta debe **automatizar** esa parte: comparar la distribución de cada dimensión **dentro** del área anómala vs. el **baseline** y ordenar por mayor diferencia (p.ej. *BubbleUp* de Honeycomb: «`availability_zone=us-east-1a` aparece en 98% del área anómala pero solo 17% del baseline»).

## AIOps no es magia

La IA solo ayuda si existen patrones **estables**; en entornos que cambian rápido (cada deploy es una anomalía) dibuja la «caja» del baseline mal → demasiado ruido o demasiado silencio. Lo pragmático: **humano + máquina** — la máquina cruje los números y **surfacea** patrones; el humano les **da significado** (¿bueno o malo, intencional o no?). Automatizar el core analysis loop materializa esa fusión.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «¿Guardo métricas o logs?» | El bloque base es el **evento estructurado ancho** (una unidad de trabajo) |
| Latencia 3 capas arriba, ¿de quién es? | Traza distribuida: waterfall de spans con relación padre-hijo |
| Diseñar un span a mano | 5 campos: Trace ID, Span ID, Parent ID, Timestamp, Duration (+ propaga por cabecera) |
| No sé ni por dónde empezar a depurar | Core Analysis Loop: anomalía → GROUP BY dimensiones → aísla → repite |
| Vendedor promete «AIOps lo resuelve» | Sin patrones estables falla; humano da significado, máquina cruje números |

---

> **Síntesis:** el bloque base de la observabilidad es el **evento estructurado ancho** (toda una unidad de trabajo, no la métrica preagregada ni el log suelto). Enlazados forman **trazas** (spans con Trace/Span/Parent ID + timestamp + duration, propagados por cabecera; OTel instrumenta una vez). Se depura **desde primeros principios** con el **Core Analysis Loop** (anomalía → agrupar/filtrar dimensiones → aislar → repetir), automatizando la fuerza bruta y dejando que el humano dé el significado que AIOps no puede.

---

*Retrieval: (1) ¿por qué el evento ancho y no la métrica/log es el bloque base?; (2) nombra los 5 campos de un span y cómo se propaga una traza; (3) describe los 4 pasos del Core Analysis Loop; (4) ¿por qué AIOps no es bala de plata y cuál es el rol del humano?*
