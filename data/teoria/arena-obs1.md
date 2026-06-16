# ¿Qué es observabilidad? Monitoreo vs. observabilidad

## De qué trata esta lección (y qué sabrás hacer al final)

"Tengo dashboards, luego tengo observabilidad" es uno de los malentendidos más caros de la ingeniería moderna. Esta lección construye, desde cero, la distinción real: el **monitoreo** comprueba condiciones contra umbrales que *ya anticipaste* (known-unknowns), mientras la **observabilidad** te deja entender *cualquier* estado nuevo o extraño **sin desplegar código nuevo** (unknown-unknowns). La clave técnica que las separa: la **alta cardinalidad** y la **alta dimensionalidad** de los eventos.

Al terminar podrás: (1) dar la prueba de fuego de la observabilidad (responder preguntas que no anticipaste, sin instrumentar primero); (2) explicar por qué monitoreo = known-unknowns y observabilidad = unknown-unknowns; (3) entender por qué la cardinalidad (user_id, request_id) hunde a las métricas preagregadas; y (4) decidir cuándo usar cada una (infra → monitoreo; tu código/cliente → observabilidad). El ejemplo del p99 "rápido" y el cliente furioso hace de hilo. Conecta con la observabilidad de modelos ([[arena-rml3]]).

El término **observabilidad** lo acuñó Rudolf Kálmán (1960) en teoría de control: una medida de qué tan bien se pueden inferir los **estados internos** de un sistema a partir de sus **salidas externas**. Aplicado al software, un sistema es observable en la medida en que puedes **entender y explicar cualquier estado en que pueda caer —por nuevo o extraño que sea— sin tener que desplegar código nuevo** para explicarlo.

## La prueba de fuego

¿Puedes responder preguntas abiertas e iterativas sobre tu sistema sin haber **predicho de antemano** que necesitarías esa métrica? Ej.: «de los usuarios que se quejaron de timeouts, ¿qué tienen en común si mis percentiles p99/p99.9 se ven rápidos?». Si para responder tienes que enviar código o configurar un monitor primero, **no tienes observabilidad**.

## Monitoreo es para *known-unknowns*; observabilidad para *unknown-unknowns*

- **Monitoreo** (métricas + dashboards + umbrales): comprueba condiciones contra umbrales conocidos. Es **fundamentalmente reactivo** — solo detecta modos de fallo que **ya anticipaste**. Funciona cuando el sistema es lo bastante simple para predecir cómo fallará.
- **Observabilidad**: investigación exploratoria iterativa para hallar el porqué de **cualquier** fallo, conocido o no. En sistemas distribuidos modernos (microservicios, 20-30 saltos de red por petición, autoescalado, polyglot persistence) los modos de fallo nuevos superan la capacidad de cualquiera para predecir dashboards.

## Por qué fallan las métricas: cardinalidad y dimensionalidad

- **Métrica** = un solo número preagregado con etiquetas; barato y de huella predecible, pero la **preagregación es el nivel mínimo de granularidad** y oculta al usuario individual.
- **Cardinalidad** = nº de valores únicos de un campo. Los IDs únicos (UUID, user_id, request_id) son de **alta cardinalidad** — y *la alta cardinalidad es casi siempre lo más útil para depurar* (encontrar la aguja en el pajar). Las métricas solo manejan baja cardinalidad a escala razonable.
- **Dimensionalidad** = nº de claves por evento. Los eventos observables son **arbitrariamente anchos** (cientos o miles de pares clave-valor): a más dimensiones, más correlaciones ocultas puedes descubrir.

## Sistema vs. software

Regla práctica: el **monitoreo** sirve para la salud del **sistema/infraestructura** (cambia poco, predecible: CPU, memoria, disco → autoescalado, capacity planning); la **observabilidad** sirve para el **software** que escribes (cambia a diario, impredecible, lo que viven tus clientes). Coexisten; excepción: métricas de infra de alto orden (CPU/mem/disco) que avisan de impacto en el código sí valen junto a tu observabilidad.

---

## Mini-ejemplo trabajado: el p99 "rápido" y el cliente furioso

Tu dashboard muestra **p99 de latencia = 80 ms**, verde. Pero llegan quejas de timeouts. Con **monitoreo** (métricas preagregadas) estás atascado: el número está bien y no anticipaste un dashboard para "usuarios que se quejan".

Con **observabilidad** trozas eventos anchos: filtras `status=timeout`, agrupas por `user_id`, `region`, `app_version`, `device`… y descubres que **todos** los afectados comparten `app_version=3.2.1` en una sola región. La métrica p99 los ocultó porque son el 0.05% del tráfico —se promedian hacia la invisibilidad—, pero el evento individual de **alta cardinalidad** (user_id, request_id) los hace aparecer.

**Predicción antes de seguir:** ¿por qué una *métrica* no puede simplemente "agruparse por user_id"? Porque cada valor único de user_id crea una nueva serie temporal; con millones de usuarios la **cardinalidad** hace explotar el coste de almacenamiento. Las métricas viven en baja cardinalidad; los eventos anchos, no.

## Prototipo, contraejemplo y caso borde

- **Prototipo (observabilidad):** fallo nuevo y nunca visto → investigación iterativa sobre eventos de alta cardinalidad/dimensionalidad, sin desplegar código.
- **Contraejemplo (monitoreo donde toca observabilidad):** crear un dashboard por cada modo de fallo en un sistema de 30 microservicios → solo cubres los known-unknowns que imaginaste; los unknown-unknowns se escapan.
- **Caso borde (infra de alto orden):** CPU/memoria/disco sí son monitoreo legítimo —cambian poco y predecible— y conviven con la observabilidad del código.

## Errores típicos

- **Conceptual:** creer que "más dashboards" = observabilidad; los dashboards son monitoreo reactivo de known-unknowns.
- **De datos:** confiar en la **media** preagregada, que oculta al usuario individual; baja a eventos.
- **De diseño:** tirar la alta cardinalidad (user_id, request_id) "para ahorrar", justo la dimensión más útil para depurar.

## Transferencia isomorfa

Observabilidad es análisis exploratorio de datos aplicado a producción:

- **Cardinalidad ↔ granularidad de un GROUP BY:** "puedo trocear por user_id" es exactamente bajar el grano de una agregación SQL; la preagregación de una métrica es un GROUP BY que ya no puedes deshacer (conecta con [[arena-m2]], window functions).
- **Eventos anchos ↔ filas desnormalizadas:** cientos de claves por evento es una fila ancha que permite correlaciones ad-hoc, como una tabla de hechos rica.
- **Unknown-unknowns ↔ EDA / observabilidad del modelo:** investigar un fallo no anticipado es lo mismo que el debugging slice-by-slice de un modelo en producción (conecta con [[arena-htd1]], detección de cambios).

Moraleja de la arista: *monitorear responde preguntas que ya hiciste; observar responde las que aún no imaginabas — y eso exige guardar alta cardinalidad, no promedios.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «Crearé un dashboard para esto» | ¿Y para el fallo que aún no imaginaste? Los known-unknowns no bastan |
| Quieres filtrar por user_id / request_id | Alta cardinalidad → métricas no llegan; necesitas eventos anchos |
| «El promedio se ve bien» pero hay quejas | La métrica preagregada oculta al usuario individual; baja a eventos |
| Fallo nuevo y nunca visto | unknown-unknown → observabilidad, no monitoreo |
| ¿Monitoreo o observabilidad? | Sistema/infra → monitoreo; tu código/cliente → observabilidad |

---

> **Síntesis:** observabilidad = entender **cualquier** estado nuevo o extraño **sin desplegar código nuevo**, troceando datos de **alta cardinalidad y alta dimensionalidad** de forma iterativa. El monitoreo (métricas/umbrales) es reactivo y solo cubre **known-unknowns**; la observabilidad persigue los **unknown-unknowns** de los sistemas distribuidos modernos.

---

*Retrieval: (1) define observabilidad en una frase y da su prueba de fuego; (2) ¿por qué monitoreo = known-unknowns y observabilidad = unknown-unknowns?; (3) ¿qué son cardinalidad y dimensionalidad y por qué hunden a las métricas?; (4) ¿cuándo monitoreo y cuándo observabilidad (sistema vs. software)?*
