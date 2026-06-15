# SQL y product sense para entrevistas de ciencia de datos

## SQL: traducir negocio a consultas

Casi toda entrevista de DS de producto/analytics prueba SQL. No evalúan sintaxis exótica sino **traducir un requisito de reporte a una consulta**. Comandos núcleo: `SELECT`, `WHERE` (filtra antes de agrupar), `GROUP BY`, `HAVING` (filtra después de agrupar), `ORDER BY`, `DISTINCT`, `UNION`, joins.

**Táctica de resolución — trabajar hacia atrás:** imagina que ya tienes una única tabla ideal con todo lo necesario y el query final es un solo `SELECT`. Desde ahí, retrocede un paso a la vez (joins, subqueries, CTEs) hasta las tablas reales. No intentes resolver todas las piezas a la vez.

### Joins y CTEs
- **Joins** combinan tablas por clave (`INNER`, `LEFT`, etc.). Un **self-join** relaciona una tabla consigo misma (p.ej. comparar el evento de un usuario con el anterior).
- **CTE** (`WITH ... AS`): nombra subconsultas para encadenar pasos legibles, mejor que subqueries anidadas.

### Window functions
Calculan sobre una "ventana" de filas **sin colapsarlas** (a diferencia de `GROUP BY`). `func() OVER (PARTITION BY ... ORDER BY ...)`:
- `ROW_NUMBER / RANK / DENSE_RANK` — ranking dentro de cada grupo (top-N por categoría).
- `LAG / LEAD` — valor de la fila anterior/siguiente (deltas, retención mes a mes).
- Sumas/medias móviles acumuladas.

**Patrón clásico:** retención mes a mes, "producto más popular por categoría", deltas entre eventos consecutivos.

## Product sense: cuatro tipos de pregunta

1. **Definir una métrica:** ¿qué medirías para el éxito de un lanzamiento?
2. **Diagnosticar un cambio de métrica:** ¿por qué subió/bajó esta métrica?
3. **Brainstorm de features:** ¿debería lanzarse este producto? ¿qué ideas lo mejoran?
4. **Diseñar un A/B test:** ¿cómo lo montas y qué trampas evitas?

**Marco general:** haz preguntas aclaratorias (¿quién es el usuario?, ¿cuál es la meta de negocio?), acota el problema, **piensa en voz alta**, sé conversacional y mantén la **misión de la empresa** al frente. Mentalidad: actúa como si ya trabajaras ahí, charlando con un colega.

## Definir métricas: North Star + guardrail

- **Funnel de adquisición (AARRR / "pirate metrics"):** Acquisition, Activation, Retention, Referral, Revenue.
- **North Star:** la métrica única más alineada con el valor del producto (p.ej. tiempo viendo videos en YouTube).
- **Guardrail / counter metrics:** métricas que no deben empeorar al perseguir la principal. Es fácil inflar una métrica a costa de otra (subir notificaciones sube clics pero hunde la retención). Siempre propón guardrails junto a la métrica clave.

## Diagnosticar un cambio de métrica

Marco para "¿por qué cayó X?":
1. **¿Cambio natural?** Estacionalidad, día de la semana, evento externo (feriado, competidor, noticia).
2. **¿Causa interna?** Camina **hacia arriba por el funnel**: ¿hubo un release, un bug, un cambio de UI? ¿Una feature **canibaliza** a otra (comentar vs postear)?
3. **Segmenta:** corta por plataforma, país, versión, cohorte de usuario, para localizar dónde ocurre el cambio.
4. **Distingue** la **causa raíz** del **factor contribuyente** y del **resultado correlacionado** (síntoma que no causa). Ej.: menos comentarios por post → causa raíz de menos engagement.

## Diseñar un A/B test y sus trampas

Plantea $H_0$ (sin efecto), elige métrica primaria + guardrails, define tamaño de muestra y duración, asigna usuarios al azar a control/tratamiento. Trampas frecuentes:

- **Efecto novedad:** un pico inicial porque usuarios curiosos prueban lo nuevo; se estabiliza después. Detéctalo mirando **solo usuarios nuevos**, o corre el test más tiempo.
- **Efecto primacía:** aversión inicial al cambio (los viejos usuarios resisten).
- **Efectos de red:** en redes sociales, el tratamiento "contamina" al control (la mayor actividad del grupo test arrastra a sus amigos en control) → subestima el efecto. Mitigación: clusters/partición del grafo para aislar grupos.
- **Pruebas múltiples:** si corres 100 tests a α=0.05, algunos saldrán "significativos" por azar. Corrige con **Bonferroni** o controlando **FDR** (FP/(FP+TP)) / **FWER**.
- **Significancia ≠ enviar:** con millones de usuarios cualquier diferencia se vuelve detectable; evalúa el **tamaño del efecto** y qué pasó con los guardrails (si sube revenue pero baja retención, decide con negocio).

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
