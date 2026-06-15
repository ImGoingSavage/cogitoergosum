# Observabilidad a escala: almacenamiento, muestreo y madurez

## Requisitos funcionales del almacén de observabilidad

Los datos son **eventos ultra-anchos**; cualquier campo debe ser **consultable** sin preagregar (no sabes de antemano qué dimensión importará). De ahí: **todo indexado o ningún índice privilegiado** (todas las dimensiones igual de rápidas), datos **frescos en segundos**, y almacén **durable y tolerante a fallos** (no puede caerse justo cuando depuras una caída).

### Por qué la TSDB no sirve
Una **TSDB** amortiza el coste reusando series de tiempo, pero meterle alta cardinalidad (p.ej. indexar por `user_id`) **explota** el nº de series: cada evento único crea una serie nueva → coste lineal en eventos = **explosión de cardinalidad**. NoSQL (Mongo/Snowflake) ingiere bien pero el **egress** (consulta arbitraria por dimensionalidad y cardinalidad) es lento sin preindexar; preindexar todo cuesta tanto como los datos.

### Fila vs. columna → columnar híbrido
- **Row-based** (Bigtable, base de Dapper): recuperar una traza/span es rápido (clave primaria indexada), pero el análisis de campos arbitrarios obliga a leer toda la fila; la **compactación** (write-once-read-many) penaliza el ingreso en segundos.
- **Column-based**: lees solo las columnas de la consulta → ideal para filtrar/agrupar por dimensiones arbitrarias. Coste: reconstruir filas exige índice de timestamp + secuencia.
- **Híbrido** (caso *Retriever* de Honeycomb): **particiona por tiempo en segmentos** (metadata = timestamp más viejo/nuevo → en consulta solo se leen segmentos que solapan la ventana), almacena **por columna dentro del segmento** (un archivo append-only por campo, con compresión por diccionario/RLE/LZ4), **tiering** (SSD reciente → S3 antiguo), **paralelismo** estilo map-reduce con serverless (e **impaciencia**: si el 90% de subconsultas terminó, reintenta el 10% lento), y **Kafka** para durabilidad/orden. Para observabilidad, **es más importante que el resultado llegue rápido que que sea perfecto**.

## Muestreo: barato y suficientemente exacto

Como muchos eventos son casi idénticos, transmitir el 100% es derrochador. El **muestreo** envía eventos **representativos** + metadata para reconstruir la forma original; a diferencia de la métrica preagregada, **conserva la cardinalidad completa** en el evento muestreado.

- **Probabilidad constante** (1 de cada N): fácil, pero falla si te importan los errores raros, si unos clientes pesan mucho más, o ante picos de tráfico.
- **Dinámico por volumen reciente**: ajusta la tasa según tráfico (requiere algoritmo ponderado: multiplicar por la tasa vigente al reconstruir; mediana/p99 deben expandir cada evento a los que representa).
- **Por contenido/clave**: tasa según campos (errores > éxitos; clientes de pago > free tier).
- **Target rate**: automatiza la tasa para un objetivo de eventos/seg, sin ajustar flags a mano.
- **Grabar la sample rate dentro del evento** es clave para reconstruir bien al cambiar la tasa.

### Head vs. tail (decisión en trazas)
- **Head-based (up-front)**: decides muestrear al **iniciar** la traza (por endpoint/cliente, datos conocidos al inicio) y propagas la decisión a los hijos. Barato; no conoce el resultado.
- **Tail-based**: decides al **final**, cuando ya conoces status/latencia (puedes quedarte solo con errores/lentos). Requiere **bufferizar** todos los spans en un colector externo → caro.
- **Muestreo consistente**: usa un **sampling/trace ID** central propagado para que una traza se conserve **entera o nada** (nunca un hijo huérfano sin su padre).

## Madurez: el Observability Maturity Model (OMM)

La observabilidad es **socio-técnica** (herramienta + cultura). El OMM mide cinco capacidades de los equipos de alto desempeño (no es lineal ni universal; sirve como punto de partida):
1. **Responder a fallos con resiliencia** (MTTR, alertas accionables, on-call sostenible).
2. **Entregar código de alta calidad** (depurar igual en 1 máquina que en 10.000).
3. **Gestionar complejidad y deuda técnica** (no «haunted graveyard»).
4. **Liberar con cadencia predecible** (deploy/rollback rápidos, feature flags).
5. **Entender el comportamiento del usuario** (KPIs de cliente accesibles, iterar con flags).

---

## Mini-ejemplo trabajado: por qué una TSDB explota con `user_id`

Una TSDB (Prometheus, etc.) amortiza el coste **reusando series de tiempo**: cada combinación única de etiquetas es una serie. Mientras las etiquetas sean de **baja cardinalidad** (status=200/500, region=3 valores), hay pocas series y todo va barato.

Indexa por `user_id` con 10 millones de usuarios y, de golpe, cada usuario crea **su propia serie** → 10M de series, el coste crece **lineal en eventos**: la **explosión de cardinalidad**. Por eso el almacén de observabilidad es **columnar híbrido particionado por tiempo**: lee solo las columnas de la consulta, y para observabilidad *que el resultado llegue rápido importa más que sea perfecto*.

Y para no transmitir el 100%: **muestreo** que conserva la forma. Constante (1 de cada N) falla con errores raros; mejor **por clave** (errores > éxitos, clientes de pago > free) y, en trazas, **consistente** (mismo `trace ID` decide la traza **entera o nada**, nunca un hijo huérfano). Clave: **graba la sample rate dentro del evento** para reconstruir bien.

**Predicción antes de seguir:** muestreas head-based (decides al iniciar la traza) pero te importan solo los errores. ¿Problema? Head-based no conoce el resultado aún → no puedes quedarte "solo con los errores"; eso exige **tail-based** (decides al final, pero bufferizas todo → caro).

## Prototipo, contraejemplo y caso borde

- **Prototipo (columnar particionado):** segmentos por tiempo + archivo por columna → consulta arbitraria barata, frescura en segundos.
- **Contraejemplo (TSDB para alta cardinalidad):** indexar `user_id`/`request_id` en una TSDB → explosión de series; herramienta equivocada.
- **Caso borde (impaciencia):** si el 90% de las subconsultas terminó, reintenta el 10% lento en vez de esperar → "rápido > perfecto" llevado a la ejecución.

## Errores típicos

- **Conceptual:** tratar la observabilidad como puramente técnica; el OMM es **socio-técnico** (herramienta + cultura).
- **Técnico:** muestreo por probabilidad constante cuando importan los eventos raros → los pierdes.
- **De integridad:** muestrear spans de forma inconsistente → trazas rotas; usa un trace ID propagado (entera o nada).

## Transferencia isomorfa

- **Explosión de cardinalidad ↔ granularidad de un índice/GROUP BY:** el coste de indexar alta cardinalidad es el mismo dilema que bajar el grano de una agregación (conecta con [[arena-obs1]] y [[arena-m2]]).
- **Almacén columnar ↔ OLAP / formatos column-store:** leer solo las columnas de la consulta es exactamente Parquet/columnar de un data warehouse (conecta con [[arena-sd3]]).
- **Muestreo que conserva cardinalidad ↔ muestreo representativo vs agregación:** guardar el evento con su sample rate es como un muestreo ponderado que permite reconstruir la población (conecta con [[arena-pst2]], bootstrap/muestreo).

Moraleja de la arista: *la alta cardinalidad hunde a la TSDB; usa columnar particionado por tiempo y muestreo por clave/consistente con la sample rate grabada — rápido y representativo gana a exhaustivo y caro.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «Guardemos los eventos en una TSDB» | Explosión de cardinalidad: usa almacén **columnar** particionado por tiempo |
| Consulta lenta por dimensión arbitraria | Columnar: lee solo esas columnas; rápido > perfecto |
| Enviar el 100% de eventos cuesta una fortuna | Muestrea representativos + graba la sample rate en el evento |
| Me importan los errores raros | Muestreo por clave/tail (errores > éxitos), no probabilidad constante |
| Trazas rotas al muestrear | Muestreo consistente con trace ID propagado: la traza entera o nada |
| «¿Qué tan maduros somos?» | OMM: resiliencia, calidad, deuda, cadencia, comportamiento de usuario |

---

> **Síntesis:** a escala, las **TSDB** sufren explosión de cardinalidad; el almacén de observabilidad es **columnar híbrido particionado por tiempo** (frescura en segundos, durable, rápido > perfecto). El **muestreo** conserva la forma de los datos a fracción del coste: por clave/dinámico mejor que constante, **head vs. tail**, **consistente** (traza entera o nada) y **grabando la sample rate**. La madurez (OMM) es socio-técnica: resiliencia, calidad de código, deuda, cadencia de release y comportamiento del usuario.

---

*Retrieval: (1) ¿por qué una TSDB no sirve para eventos de alta cardinalidad?; (2) ¿qué ventajas da el almacén columnar y por qué «rápido > perfecto»?; (3) compara muestreo constante vs por clave y head vs tail; (4) ¿qué es el muestreo consistente y por qué grabar la sample rate?; (5) nombra las 5 capacidades del OMM.*
