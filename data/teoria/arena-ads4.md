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
