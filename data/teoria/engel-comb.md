# Engel · Combinatoria de competencia: la técnica de la tabla y el conteo doble

*Lección redactada para CogitoErgoSum a partir del capítulo 5 de «Problem-Solving Strategies» (A. Engel), Enumerative Combinatorics. Engel es cantera: esta lección cubre la técnica central; los problemas del capítulo se atacan como sesiones del camino 1.*

## El sello de Engel

Los problemas de Engel son **«sin prerrequisitos»**: no piden teoremas avanzados — piden **organizar un argumento**. Un olímpico de preparatoria no corre con desventaja frente a un profesional, porque la dificultad no está en saber, sino en estructurar. Eso los vuelve el material de entrenamiento perfecto: cada problema es pura habilidad de resolución, sin peaje de conocimientos.

## El problema prototipo (IMO 1977)

> En una sucesión finita de números reales, **toda suma de 7 términos consecutivos es negativa** y **toda suma de 11 términos consecutivos es positiva**. ¿Cuál es la longitud máxima de la sucesión?

Parece inabordable: condiciones sobre *todos* los tramos. La jugada que lo desarma es la **técnica de la tabla**.

## La técnica de la tabla

Supón que la sucesión a₁, a₂, …, aₙ existe con n = 17. Construye la tabla cuyas **filas son las 7-sumas sucesivas** desplazadas de una en una:

| | | | | | | |
|---|---|---|---|---|---|---|
| a₁ | a₂ | a₃ | a₄ | a₅ | a₆ | a₇ |
| a₂ | a₃ | a₄ | a₅ | a₆ | a₇ | a₈ |
| a₃ | a₄ | a₅ | a₆ | a₇ | a₈ | a₉ |
| ⋮ | | | | | | |
| a₁₁ | a₁₂ | a₁₃ | a₁₄ | a₁₅ | a₁₆ | a₁₇ |

Son 11 filas (de a₁…a₇ hasta a₁₁…a₁₇) y 7 columnas. Ahora mira la tabla de las **dos maneras**:

- **Por filas:** cada fila es una suma de 7 consecutivos → **negativa**. Total de la tabla: suma de 11 números negativos → **negativo**.
- **Por columnas:** cada columna es a_k + a_{k+1} + ⋯ + a_{k+10}, ¡una suma de 11 consecutivos! → **positiva**. Total: suma de 7 números positivos → **positivo**.

El mismo total no puede ser negativo y positivo. **Contradicción**: no existe sucesión de longitud 17. (Y en general, de longitud ≥ 17; el conflicto aparece en cuanto caben 11 filas y 7 columnas completas.)

**La otra mitad:** falta la **construcción** para n = 16 — una sucesión explícita que cumpla ambas condiciones. Existe (el patrón periódico clásico: 5, 5, −13, 5, 5, 5, −13, 5, 5, −13, 5, 5, 5, −13, 5, 5 — verifica algunas 7-sumas y 11-sumas). Respuesta: **16**.

## Por qué funciona: conteo doble

El corazón de la técnica: **el mismo total calculado de dos formas**. Es el «argumento combinatorio» de Zeitz §6.1 en versión de combate: allá contabas comités de dos maneras para probar una identidad; acá sumas una tabla de dos maneras para fabricar una **contradicción de signos**. El conteo doble es de las armas más versátiles de toda la combinatoria: cuando dos estructuras (filas/columnas, parejas/elementos, aristas/vértices) atraviesan el mismo conjunto, suma sobre ambas y compara.

## La regla de las dos mitades

**Todo problema de «¿cuál es el máximo número de…?» tiene DOS mitades:**

1. **La cota:** demostrar que ninguna configuración supera N (arriba: la tabla mata n = 17).
2. **La construcción:** exhibir una configuración que alcanza N (arriba: la sucesión de longitud 16).

Una cota sin construcción solo prueba «≤ N» — quizá el máximo real es menor. Una construcción sin cota solo prueba «≥ N» — quizá se puede más. **Cada mitad sola es media solución**, y los puntos de olimpiada se reparten así. Hazlo reflejo: al escribir «el máximo es N», pregunta de inmediato «¿dónde está mi cota? ¿dónde está mi ejemplo?».

## La variante con productos

Si las condiciones hablan de **productos** en vez de sumas (todo p-producto < 1, todo q-producto > 1, con términos positivos), **toma logaritmos**: los productos se vuelven sumas (log de producto = suma de logs), «< 1» se vuelve «< 0» y «> 1» se vuelve «> 0» — exactamente el problema anterior. Transformar el problema en uno ya resuelto es la traducción de Zeitz §2.4 en acción.

## Cómo usar Engel (modo cantera)

Engel no se lee de corrido. El protocolo: estudiar la técnica del capítulo (esta lección) y luego **elegir 2-3 problemas del capítulo a tu nivel** y atacarlos con el bucle completo del camino 1 — timer, desconstrucción, ficha de moraleja. La lista de problemas del capítulo 5 es enorme: es tu mina de sesiones de entrenamiento para esta fase.

## Disparadores

- Sucesión con condiciones sobre **todos los tramos de longitud fija** (toda p-suma cumple X, toda q-suma cumple Y) → tabla de sumas desplazadas; suma por filas y por columnas.
- Condiciones sobre p-**productos** y q-**productos** → logaritmos, luego la tabla.
- «¿Máximo/mínimo número de…?» → exige las dos mitades: cota Y construcción.
- Dos estructuras que atraviesan el mismo conjunto → conteo doble: suma sobre ambas y compara.

## Síntesis

> **Chunk mínimo:** Técnica de la tabla (IMO 1977: toda 7-suma negativa, toda 11-suma positiva): con n = 17, arma la tabla de 11 filas × 7 columnas de sumas desplazadas — por filas el total es negativo (once 7-sumas), por columnas positivo (siete 11-sumas): contradicción. Es CONTEO DOBLE: el mismo total calculado de dos maneras. Regla de las dos mitades en todo «¿máximo número de…?»: cota (la tabla mata 17) Y construcción (la sucesión explícita de longitud 16) — cada mitad sola es media solución. Con p-productos y q-productos: toma logaritmos y es el mismo problema. Engel es cantera: técnica aquí, problemas como sesiones del camino 1.

---

*Antes del quiz: reconstruye de memoria la tabla del IMO 1977 (qué hay en filas y columnas y de dónde sale la contradicción), por qué cota y construcción son obligatorias, y el truco del logaritmo.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

La cantera combinatoria de Engel funciona como gimnasio para las tecnicas de [[zeitz-61]], [[zeitz-62]] y [[zeitz-63]]. En la Arena, [[arena-p2]] organiza esas mismas ideas como probabilidad discreta, mientras [[aime-cnt]] las prueba en problemas donde elegir casos correctos importa mas que expandir formulas.
<!-- GRAFO_CONEXO_OLEADA3_END -->
