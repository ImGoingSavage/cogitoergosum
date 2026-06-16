# SQL Window Functions

## De qué trata esta lección (y qué sabrás hacer al final)

Hay un momento en casi toda entrevista de SQL en que `GROUP BY` deja de alcanzar: necesitas un cálculo **sobre un grupo** —un ranking, un acumulado, una comparación con la fila anterior— pero **sin perder las filas individuales**. Esa es exactamente la frontera que cruzan las *window functions*. Esta lección las construye desde cero: su anatomía (`PARTITION BY` / `ORDER BY` / frame), las familias que más aparecen (ranking, desplazamiento, agregados como ventana) y la trampa de orden de evaluación que hace que `WHERE rn = 1` falle.

Al terminar podrás: (1) explicar qué hace una window function que un `GROUP BY` no (conservar la fila y añadir el cálculo); (2) elegir entre `ROW_NUMBER`, `RANK` y `DENSE_RANK` según cómo trates los empates; (3) comparar cada fila con su período anterior usando `LAG`/`LEAD`; y (4) usar el patrón CTE para filtrar el resultado de una ventana sin chocar con el orden de evaluación de SQL. Cada función entra por el problema que resuelve. La idea de fondo: **la ventana conserva la fila y calcula sobre su vecindad**, y ese gesto reaparece en cohortes, paneles (LAG = diferencias) y streams.

---

## El problema que resuelven: agregar sin colapsar

`GROUP BY` resume: convierte muchas filas de un grupo en **una**. Pero a veces quieres el resumen *junto a* cada fila original —"el total de su categoría", "su posición en el ranking", "cuánto cambió desde la semana pasada"—. Una **window function** hace eso: calcula sobre un conjunto de filas relacionadas y **devuelve el resultado en cada fila**, sin colapsarlas. Es la diferencia entre un *aggregate* (colapsa) y un *transform* (conserva la fila y le añade una columna calculada).

## Anatomía

```sql
funcion() OVER (
    PARTITION BY columna_de_grupo      -- el "grupo", como GROUP BY pero sin colapsar
    ORDER BY columna_de_orden          -- orden dentro de la partición (necesario para ranking/acumulados)
    ROWS/RANGE BETWEEN inf AND sup     -- el "frame": cuántas filas alrededor entran al cálculo
)
```

Las tres piezas: `PARTITION BY` corta el conjunto en grupos independientes; `ORDER BY` ordena dentro de cada grupo (obligatorio para rankings y acumulados); el **frame** (`ROWS`/`RANGE BETWEEN`) define cuántas filas vecinas entran (por ejemplo, "las 6 anteriores y la actual" para un promedio móvil de 7).

## Las familias que más se preguntan

**Ranking** — numerar dentro de cada partición. La elección depende de **cómo tratas los empates**:

```sql
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY fecha)   -- 1,2,3,4  sin empates (arbitrario si hay)
RANK()       OVER (PARTITION BY user_id ORDER BY pts DESC) -- 1,1,3,4  empate comparte, luego salta
DENSE_RANK() OVER (PARTITION BY user_id ORDER BY pts DESC) -- 1,1,2,3  empate comparte, sin salto
```

Usa `ROW_NUMBER` cuando necesitas **exactamente una** fila por grupo (la 2ª compra de un usuario, su 1ª sesión); `RANK` cuando los empates deben compartir posición (resultados deportivos); `DENSE_RANK` igual pero con números consecutivos.

**Desplazamiento** — mirar la fila vecina:

```sql
LAG(col, n, default)  OVER (PARTITION BY ... ORDER BY ...)   -- valor n filas atrás
LEAD(col, n, default) OVER (PARTITION BY ... ORDER BY ...)   -- valor n filas adelante
```

`LAG` es la herramienta de "¿subió o bajó respecto al período anterior?" — comparas cada fila con su predecesora.

**Agregados como ventana** — `SUM`, `AVG`, `COUNT` con `OVER`. El comportamiento cambia con `ORDER BY`:

```sql
SUM(monto) OVER (PARTITION BY user_id)                 -- total del usuario, repetido en cada fila
SUM(monto) OVER (PARTITION BY user_id ORDER BY fecha)  -- acumulado hasta esa fecha (running total)
AVG(monto) OVER (PARTITION BY cat ORDER BY fecha
                 ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)  -- promedio móvil de 7 días
```

Sin `ORDER BY`, el agregado es el **total de la partición**; con `ORDER BY`, se vuelve **acumulado**.

## La trampa del orden de evaluación: usa un CTE

El error más común: intentar filtrar el ranking en el mismo `WHERE`.

```sql
-- INCORRECTO: WHERE se evalúa ANTES que las window functions
SELECT user_id, order_id,
       ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS rn
FROM orders
WHERE rn = 2;   -- ERROR: rn aún no existe cuando WHERE corre
```

SQL evalúa `WHERE` **antes** de calcular las funciones de ventana, así que el alias `rn` no existe todavía. La solución es materializar el cálculo en un CTE (o subconsulta) y filtrar **fuera**:

```sql
WITH ranked AS (
    SELECT user_id, order_id, created_at,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS rn
    FROM orders
)
SELECT user_id, order_id, created_at
FROM ranked
WHERE rn = 2;   -- la 2ª compra de cada usuario
```

> **Predicción antes de seguir:** quieres "el porcentaje que cada producto representa sobre el total de **su** categoría". ¿Subconsulta correlacionada o window? Respuesta: **window** — `monto / SUM(monto) OVER (PARTITION BY categoria)` calcula el denominador por categoría en cada fila, sin `GROUP BY` ni subconsulta. Una sola pasada, legible.

## ROWS vs RANGE (el matiz con fechas duplicadas)

Con `ORDER BY` pero sin frame explícito, el default es `RANGE`, que agrupa **todas las filas con el mismo valor de orden**: si dos filas comparten fecha, ambas reciben el mismo acumulado (el total hasta esa fecha inclusive). `ROWS` cuenta filas **físicas** una a una, dando un acumulado incremental por fila. Menciona esta distinción si el entrevistador pregunta por fechas duplicadas; usar el default `RANGE` cuando querías `ROWS` produce acumulados "saltados".

---

## Errores típicos

- **Conceptual:** filtrar el resultado de una ventana en el mismo `WHERE` (`WHERE rn = 1`) — el `WHERE` se evalúa **antes** que las funciones de ventana; necesitas un **CTE/subquery** y filtrar fuera.
- **Técnico:** olvidar el desempate en `ROW_NUMBER` con empates en la columna de orden → resultado no determinístico (añade `id` como segundo criterio).
- **De frame:** confiar en el default `RANGE` con fechas duplicadas cuando querías un acumulado fila a fila → usa `ROWS BETWEEN ... CURRENT ROW`.

## Transferencia isomorfa

La ventana SQL "calcula sobre filas relacionadas sin colapsarlas" reaparece en análisis y ciencia de datos:

- **PARTITION BY ↔ GROUP BY sin colapsar:** conservar la fila y añadir el agregado es lo que distingue un *transform* de un *aggregate* — la misma idea que un feature derivado que se une de vuelta a cada registro (conecta con [[arena-cds1]], feature engineering).
- **LAG/LEAD ↔ diferencias en panel / DiD:** comparar cada fila con su período anterior es exactamente la "primera diferencia" (post − pre) del estimador de diferencias en diferencias (conecta con [[arena-h22]], DiD).
- **AVG OVER ... ROWS k PRECEDING ↔ ventana deslizante / streaming feature:** el promedio móvil de k días es una ventana deslizante temporal, igual que las streaming features de ML systems (conecta con [[arena-dmls3]]) y la ventana del array (conecta con [[arena-cc1]]).

Moraleja de la arista: *las window functions conservan la fila y calculan sobre su vecindad (partición/orden/frame); definir cohortes, comparar períodos (LAG=DiD) y promedios móviles es el mismo gesto en SQL, en paneles y en streams.*

---

## Señales de reconocimiento y jugadas

| Señal | Jugada |
|-------|--------|
| "La N-ésima fila dentro de cada grupo" | ROW_NUMBER() + CTE + WHERE rn = N |
| "Comparar con el período anterior" | LAG() sobre la columna de interés |
| "Acumulado por grupo" | SUM OVER con ORDER BY |
| "Total de la partición en cada fila" | SUM/COUNT OVER sin ORDER BY |
| "Porcentaje respecto al grupo" | col / SUM(col) OVER (PARTITION BY grupo) |
| "Promedio móvil de k días" | AVG OVER con ROWS BETWEEN k-1 PRECEDING AND CURRENT ROW |

---

## Casos borde en entrevistas

- **Empates en la columna de ORDER BY con ROW_NUMBER:** el orden entre empates es no determinístico. Añadir un desempate adicional (como `id`) si necesitas consistencia.
- **NULL en columnas de PARTITION/ORDER:** los NULLs van al mismo grupo (PARTITION BY NULL = NULL), y en ORDER BY se ordenan primero o último según la base de datos.
- **Ventanas que cruzan la primera/última fila:** LAG en la primera fila retorna NULL (o el default que especifiques). LEAD en la última igual.

---

## Ejercicio de consolidación

Tabla `eventos(event_id, user_id, tipo, timestamp)`. Escribe la consulta que, para cada usuario, encuentre el tiempo transcurrido entre su primer y segundo evento (diferencia en segundos).

*Pista: necesitas LAG o dos ROW_NUMBER. ¿Qué orden de operaciones usas?*

*Respuesta: WITH ranked AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) AS rn, LAG(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) AS prev_ts FROM eventos) SELECT user_id, EXTRACT(EPOCH FROM (timestamp - prev_ts)) AS segundos_entre_eventos FROM ranked WHERE rn = 2;*
