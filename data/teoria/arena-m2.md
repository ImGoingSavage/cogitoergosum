# SQL Window Functions

## El problema que resuelven

Las funciones de ventana calculan valores sobre un conjunto de filas relacionadas **sin colapsar las filas en grupos**. Esto las distingue del `GROUP BY`: con `GROUP BY` pierdes las filas individuales; con `OVER`, las conservas con el valor calculado añadido.

---

## Anatomía de una función de ventana

```sql
función() OVER (
    PARTITION BY columna_de_agrupación
    ORDER BY columna_de_ordenación
    ROWS/RANGE BETWEEN límite_inferior AND límite_superior
)
```

- `PARTITION BY`: define el "grupo" dentro del cual opera la función (como `GROUP BY` pero sin colapsar)
- `ORDER BY`: ordena las filas dentro de la partición (obligatorio para funciones de ranking y acumulados)
- `ROWS/RANGE BETWEEN`: define el frame de filas (cuántas filas "anteriores" o "siguientes" incluye el cálculo)

---

## Las funciones más usadas en entrevistas

### Ranking

```sql
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY fecha)
-- 1, 2, 3, 4... sin empates (arbitrario en empates)

RANK() OVER (PARTITION BY user_id ORDER BY puntos DESC)
-- 1, 1, 3, 4... empates reciben el mismo número, el siguiente salta

DENSE_RANK() OVER (PARTITION BY user_id ORDER BY puntos DESC)
-- 1, 1, 2, 3... empates reciben el mismo número, no hay salto
```

**Cuándo usar cada uno:**
- `ROW_NUMBER`: cuando necesitas exactamente 1 fila (segunda compra de un usuario, primera sesión). Los empates en la columna de orden son desempates arbitrarios.
- `RANK`: cuando dos posiciones empatadas deben compartir el número (resultados deportivos, rankings de empleados).
- `DENSE_RANK`: como RANK pero los números son consecutivos.

### Desplazamiento

```sql
LAG(columna, n, default) OVER (PARTITION BY ... ORDER BY ...)
-- valor de la fila n posiciones atrás

LEAD(columna, n, default) OVER (PARTITION BY ... ORDER BY ...)
-- valor de la fila n posiciones adelante
```

Útil para comparar con el período anterior: "¿subió o bajó el KPI esta semana vs la anterior?"

### Agregados como ventana

```sql
SUM(monto) OVER (PARTITION BY user_id)
-- total del usuario para cada fila (sin ORDER BY = total de la partición)

SUM(monto) OVER (PARTITION BY user_id ORDER BY fecha)
-- acumulado del usuario hasta esa fecha (con ORDER BY = acumulado)

AVG(monto) OVER (PARTITION BY categoria ORDER BY fecha ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
-- promedio móvil de 7 días por categoría
```

---

## El patrón CTE: materializar antes de filtrar

El error más frecuente: intentar filtrar con `WHERE rn = 1` en la misma query que calcula el `ROW_NUMBER`. No funciona porque `WHERE` se evalúa antes que las funciones de ventana.

**Correcto:**

```sql
WITH ranked AS (
    SELECT
        user_id,
        order_id,
        created_at,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS rn
    FROM orders
)
SELECT user_id, order_id, created_at
FROM ranked
WHERE rn = 2;  -- segunda compra de cada usuario
```

**Incorrecto:**

```sql
-- Esto falla: no puedes referenciar el alias de la función de ventana en WHERE
SELECT user_id, order_id,
       ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS rn
FROM orders
WHERE rn = 2;  -- ERROR
```

---

## ROWS vs RANGE: la diferencia que importa con duplicados

```sql
SUM(monto) OVER (PARTITION BY user_id ORDER BY fecha
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
-- incluye filas físicas hasta la actual: determinístico

SUM(monto) OVER (PARTITION BY user_id ORDER BY fecha
    RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
-- incluye todas las filas con el mismo valor de fecha que la actual
-- (comportamiento default si omites ROWS/RANGE con ORDER BY)
```

Con `RANGE`, si dos filas tienen la misma fecha, ambas obtienen el mismo acumulado (el total hasta esa fecha inclusive para todas las filas iguales). Con `ROWS`, cada fila tiene su acumulado incremental.

En entrevistas: menciona esta distinción si el entrevistador hace preguntas sobre fechas duplicadas.

---

## Ejemplo completo: porcentaje por categoría

"Para cada producto, el porcentaje que representa sobre el total de ventas de su categoría."

```sql
SELECT
    producto_id,
    categoria_id,
    monto,
    ROUND(
        monto * 100.0 / SUM(monto) OVER (PARTITION BY categoria_id),
        2
    ) AS pct_categoria
FROM ventas;
```

`SUM OVER` sin `ORDER BY` = total de la partición. No hace falta subquery correlacionada ni `GROUP BY`. La función de ventana calcula el denominador para cada fila sin agruparlas.

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
