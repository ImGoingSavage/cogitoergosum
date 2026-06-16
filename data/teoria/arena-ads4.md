# SQL y product sense para entrevistas de ciencia de datos

## De qué trata esta lección (y qué sabrás hacer al final)

El lado "aplicado" de la entrevista de DS no prueba teoría: prueba si puedes **traducir una pregunta de negocio a datos** y **razonar sobre un producto** como lo haría alguien que ya trabaja ahí. Te dan un esquema de tablas y un requisito de reporte, o una pregunta abierta ("la retención cayó 5%, ¿por qué?"), y miran cómo estructuras la respuesta. Esta lección construye, desde cero, las dos mitades: SQL analítico (con la táctica de "trabajar hacia atrás" y las window functions) y product sense (definir métricas, diagnosticar cambios, diseñar A/B tests y esquivar sus trampas).

Al terminar podrás: (1) descomponer un query complejo en pasos manejables en vez de atacarlo de golpe; (2) saber cuándo necesitas una window function y no un `GROUP BY`; (3) proponer una métrica con su guardrail; (4) diagnosticar un cambio de métrica con un marco ordenado; y (5) diseñar un A/B test reconociendo sus trampas clásicas (novedad, red, pruebas múltiples).

---

## SQL: traducir negocio a consultas

Casi toda entrevista de DS de producto/analytics prueba SQL, pero **no** la sintaxis exótica: lo que evalúan es si puedes convertir "quiero el top-3 de productos por categoría el mes pasado" en una consulta correcta. El alfabeto que basta dominar: `SELECT` (qué columnas), `WHERE` (filtra filas **antes** de agrupar), `GROUP BY` (colapsa en grupos), `HAVING` (filtra **después** de agrupar), `ORDER BY`, `DISTINCT`, `UNION`, y los joins. La distinción `WHERE` vs `HAVING` —antes vs después del agrupamiento— es un clásico de entrevista.

**Táctica de resolución — trabajar hacia atrás:** no intentes escribir el query entero de un tirón. Imagina que ya existe **una única tabla ideal** con exactamente las columnas que necesita tu `SELECT` final. Escribe ese `SELECT` primero. Luego retrocede **un paso a la vez** (¿de dónde sale esa columna? un join, una subconsulta, una CTE) hasta llegar a las tablas reales. Es el mismo "pensar hacia atrás" que en un problema de probabilidad: parte del objetivo y reconstruye el camino.

### Joins y CTEs

- **Joins** combinan tablas por una clave. `INNER` deja solo las filas que casan en ambas; `LEFT` conserva todas las de la izquierda (y rellena con NULL lo que no casa) — clave cuando quieres "todos los usuarios, hayan comprado o no". Un **self-join** une una tabla **consigo misma**, p. ej. para comparar el evento de un usuario con su evento anterior.
- **CTE** (`WITH nombre AS (...)`): nombra una subconsulta para encadenar pasos legibles. Prefiérelas a subconsultas anidadas: convierten un query monstruoso en una secuencia de pasos con nombre, que es justo la táctica de trabajar hacia atrás hecha código.

### Window functions

Una **window function** calcula sobre una "ventana" de filas relacionadas **sin colapsarlas** — y ahí está toda la diferencia con `GROUP BY`, que sí colapsa cada grupo a una fila. Con una window conservas las filas originales y le añades a cada una un cálculo sobre su grupo. Sintaxis: `func() OVER (PARTITION BY ... ORDER BY ...)` — `PARTITION BY` define los grupos, `ORDER BY` el orden dentro de cada uno.

- `ROW_NUMBER / RANK / DENSE_RANK` — ranking dentro de cada grupo (el "top-N por categoría").
- `LAG / LEAD` — el valor de la fila anterior/siguiente (deltas, retención mes a mes).
- Sumas/medias móviles y acumuladas.

> **Predicción antes de seguir:** quieres "para cada usuario, su compra y la diferencia con su compra anterior", conservando **todas** las compras. ¿`GROUP BY` o window function? Respuesta: **window** (`LAG` sobre `PARTITION BY usuario ORDER BY fecha`). Un `GROUP BY usuario` colapsaría todas sus compras a una sola fila y perderías el detalle por compra. La señal "comparar una fila con otra fila **sin** perder filas" siempre apunta a window.

## Product sense: cuatro tipos de pregunta

El "product sense" mide si piensas como dueño del producto. Casi toda pregunta cae en uno de cuatro moldes:

1. **Definir una métrica:** ¿qué medirías para el éxito de un lanzamiento?
2. **Diagnosticar un cambio de métrica:** ¿por qué subió/bajó esta métrica?
3. **Brainstorm de features:** ¿debería lanzarse este producto? ¿qué ideas lo mejoran?
4. **Diseñar un A/B test:** ¿cómo lo montas y qué trampas evitas?

**Marco general (vale para los cuatro):** empieza con **preguntas aclaratorias** (¿quién es el usuario?, ¿cuál es la meta de negocio?), **acota** el problema, **piensa en voz alta** y mantén al frente la **misión de la empresa**. La mentalidad ganadora: actúa como si ya trabajaras ahí, conversando con un colega — no como quien resuelve un acertijo cerrado. La estructura del razonamiento importa más que "la respuesta correcta".

## Definir métricas: North Star + guardrail

Para decidir si algo "funcionó" necesitas medirlo bien. Tres piezas:

- **Funnel de adquisición (AARRR / "pirate metrics"):** Acquisition → Activation → Retention → Referral → Revenue. Ubica tu métrica en alguna etapa del embudo; te obliga a pensar en todo el ciclo de vida del usuario.
- **North Star:** la métrica **única** más alineada con el valor real del producto (p. ej. tiempo viendo videos en YouTube, no solo "usuarios registrados"). Una sola, para que el equipo reme en la misma dirección.
- **Guardrail / counter metrics:** métricas que **no deben empeorar** mientras persigues la principal. Aquí está la trampa que buscan: es fácil inflar una métrica a costa de otra (subir notificaciones sube clics… pero hunde la retención y la satisfacción). **Siempre** propón guardrails junto a la métrica clave; demuestra que piensas en consecuencias, no en un número aislado.

## Diagnosticar un cambio de métrica

"La métrica X cayó, ¿por qué?" tiene un marco ordenado; el error es lanzarte a adivinar la causa. Recórrelo de fuera hacia dentro:

1. **¿Cambio natural?** Estacionalidad, día de la semana, evento externo (feriado, competidor, una noticia). Descarta lo trivial primero.
2. **¿Causa interna?** Camina **hacia arriba por el funnel**: ¿hubo un release, un bug, un cambio de UI? ¿Una feature **canibaliza** a otra (comentar vs postear)?
3. **Segmenta:** corta por plataforma, país, versión, cohorte. Una caída global rara vez es global; localizar *dónde* ocurre apunta a la causa.
4. **Distingue** la **causa raíz** del **factor contribuyente** y del **resultado correlacionado** (un síntoma que no causa nada). Ejemplo: "menos comentarios por post" puede ser la causa raíz de "menos engagement", no al revés.

Esa distinción causa-raíz vs correlación es la misma disciplina de la inferencia causal: un síntoma que se mueve junto al problema no es el problema.

## Diseñar un A/B test y sus trampas

El esqueleto: plantea $H_0$ (sin efecto), elige una **métrica primaria + guardrails**, define **tamaño de muestra y duración** (cuestión de potencia), y **asigna usuarios al azar** a control/tratamiento. La aleatorización es lo que vuelve comparables los dos grupos: cualquier diferencia posterior es atribuible al tratamiento, no a quién cayó en cada grupo. Las trampas que separan a un candidato bueno de uno excelente:

- **Efecto novedad:** un pico inicial porque los usuarios curiosos prueban lo nuevo; luego se estabiliza. Lo detectas mirando **solo usuarios nuevos** (que no tienen "lo viejo" como referencia) o corriendo el test más tiempo.
- **Efecto primacía:** lo contrario — aversión inicial al cambio; los usuarios veteranos resisten lo nuevo antes de adaptarse.
- **Efectos de red:** en productos sociales, el tratamiento "contamina" al control (la mayor actividad del grupo test arrastra a sus amigos que están en control) → **subestimas** el efecto. Mitigación: aleatorizar por **clusters** (particiona el grafo en comunidades y asigna comunidades enteras), aislando el tratamiento.
- **Pruebas múltiples:** si corres 100 tests a $\alpha=0.05$, ~5 saldrán "significativos" por puro azar aunque nada sea real. Corrige con **Bonferroni** (divide $\alpha$ entre el nº de tests) o controlando el **FDR** (fracción de falsos entre los rechazados) / **FWER**.
- **Significancia ≠ enviar:** con millones de usuarios cualquier diferencia cruza $p<0.05$; evalúa el **tamaño del efecto** y qué pasó con los **guardrails** (si sube revenue pero baja retención, es decisión de negocio, no del p-valor).

---

## Mini-ejemplo trabajado: cuando el A/B test subestima por efectos de red

Pruebas una feature social (p.ej. "reacciones") en una red de amigos: asignas usuarios al azar a control/tratamiento. El grupo tratamiento reacciona más… pero sus amigos en **control** ven esas reacciones y también se activan. El control "se contamina": su métrica sube, así que la **diferencia tratamiento − control se encoge** y subestimas el efecto real.

La causa profunda: la aleatorización a nivel usuario rompe el supuesto de que la asignación de A no afecta el resultado de B (no interferencia). La mitigación es **aleatorizar por clusters** (particiona el grafo en comunidades y asigna comunidades enteras), aislando el tratamiento dentro de cada grupo.

**Predicción antes de seguir:** ¿este sesgo infla o desinfla el efecto medido? Respuesta: lo **desinfla** (el control mejora "por contagio", reduciendo la brecha). Es el espejo del problema causal de *interferencia*/SUTVA: el resultado de una unidad depende del tratamiento de otras. Randomizar por clusters es a las redes lo que el ajuste por confundidores es a los datos observacionales: proteger la comparación.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "¿lanzamos esta feature?" → A/B test: H0 sin efecto, métrica primaria + guardrails, randomiza, evalúa tamaño de efecto.
- **Contraejemplo (significancia ≠ enviar):** con millones de usuarios cualquier diferencia es p<0.05; si sube revenue pero baja retención (guardrail), no se envía. El p-valor no decide solo.
- **Caso borde (efecto novedad):** un pico inicial por curiosidad se desvanece; mirar solo el promedio temprano engaña. Aísla usuarios nuevos o corre el test más tiempo.

## Errores típicos

- **Conceptual:** confundir causa raíz con correlación al diagnosticar una caída de métrica (un síntoma correlacionado no es la causa).
- **Técnico:** usar GROUP BY cuando necesitas conservar las filas (ranking, deltas) — ahí van window functions.
- **De supuestos:** correr decenas de tests/segmentos y reportar el significativo sin corregir multiplicidad (Bonferroni/FDR).

## Transferencia isomorfa

- **A/B test (randomización) ↔ do-operator:** asignar al azar estima un efecto causal cortando los confundidores, exactamente P(Y|do(X)) (conecta con [[arena-h17]]).
- **Efectos de red ↔ interferencia / SUTVA:** que el tratamiento de unos afecte a otros es el mismo problema que viola la no interferencia en inferencia causal; clusters ↔ aislar unidades (conecta con [[arena-h17]]).
- **Pruebas múltiples / peeking ↔ control de error familiar:** corregir muchos tests es lo mismo que en experimentos estadísticos y monitoreo (conecta con [[arena-pst3]] y [[arena-dg3]]).
- **Causa raíz vs correlación ↔ confounding y variable omitida:** distinguir el síntoma del impulsor es el reflejo causal que también corrige signos absurdos en regresión (conecta con [[arena-pst4]]).
- **Window function LAG/cohortes ↔ ventanas temporales:** comparar una fila con la anterior (retención mes a mes) es el patrón de ventanas deslizantes sobre el tiempo.

Moraleja de la arista: *aleatorizar vuelve comparables los grupos (como do(x)), pero los efectos de red rompen esa comparación; aíslalos por clusters y decide con tamaño de efecto y guardrails, no con el p-valor solo.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Query con muchos joins/pasos" | Trabaja hacia atrás desde la tabla ideal; usa CTEs |
| "Top-N por categoría / mes a mes" | Window function: RANK / LAG OVER (PARTITION BY) |
| "¿Qué métrica mide el éxito de X?" | North Star + guardrail; ubícala en el funnel AARRR |
| "La métrica subió/bajó, ¿por qué?" | Natural→interna→segmenta; causa raíz vs correlación |
| "Una feature nueva, ¿la lanzamos?" | A/B test: H0, métrica primaria, guardrails, randomiza |
| "Pico inicial que luego baja" | Efecto novedad → mira solo usuarios nuevos |
| "Red social, control contaminado" | Efectos de red → particiona por clusters |
| "Corrí muchos tests, uno salió significativo" | Pruebas múltiples → Bonferroni / FDR |
| "p<0.05, ¿lo enviamos?" | Mira tamaño del efecto y guardrails, no solo el p-valor |

---

> **Síntesis:** El lado aplicado de la entrevista de DS combina SQL (traducir negocio a queries trabajando hacia atrás; window functions para rankings y retención) con product sense. Lo central de producto: definir métricas con North Star + guardrails sobre el funnel AARRR, diagnosticar cambios de métrica distinguiendo causa raíz de correlación, y diseñar A/B tests sorteando sus trampas (novedad, red, pruebas múltiples) recordando que significancia estadística no equivale a enviar.

---

*Retrieval: cierra y responde: (1) ¿qué hace una window function que un GROUP BY no?; (2) ¿qué es una métrica guardrail y por qué proponerla?; (3) lista el marco para diagnosticar una caída de métrica; (4) explica el efecto novedad y cómo detectarlo.*
