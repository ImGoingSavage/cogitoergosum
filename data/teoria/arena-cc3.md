# Recursión y programación dinámica

## De qué trata esta lección (y qué sabrás hacer al final)

La programación dinámica (DP) intimida porque parece magia, pero en el fondo es una sola idea humilde: **recursión con memoria**. Si un problema se resuelve combinando soluciones de subproblemas, y esos subproblemas **se repiten**, entonces calcularlos una vez y guardarlos convierte un algoritmo exponencial en uno lineal o polinómico. Esta lección construye desde cero el método de cuatro pasos para *derivar* una DP, y lo aplica a la galería de problemas que toda entrevista recicla (Fibonacci, monedas, LCS, edit distance, mochila).

Al terminar podrás: (1) plantear una DP definiendo estado, recurrencia, caso base y orden de llenado; (2) elegir entre memoización (top-down) y tabulación (bottom-up); (3) reconocer la recurrencia preguntándote "¿qué pasó en el último paso?"; y (4) saber cuándo el **greedy** basta y cuándo traiciona (el contraejemplo de las monedas). Cada problema entra por su intuición y un mini-ejemplo llenando la tabla a mano. La regla de fondo: **encuentra el estado mínimo que captura todo lo necesario para decidir.**

---

## El método de cuatro pasos

Toda DP se deriva respondiendo cuatro preguntas, en orden:

1. **Define el estado:** ¿qué significa `dp[i]`? (la respuesta al subproblema de "tamaño" $i$).
2. **Recurrencia:** ¿cómo se construye `dp[i]` a partir de estados ya resueltos?
3. **Caso base:** los valores iniciales (`dp[0]`, `dp[1]`…) que no dependen de nadie.
4. **Orden de llenado:** *bottom-up* (un bucle que va de lo chico a lo grande) o *top-down* (recursión que cachea).

La diferencia entre los dos estilos de llenado:

- **Memoización (top-down):** escribes la recursión natural y le pones un diccionario de caché. Fácil de derivar y solo calcula los subproblemas que realmente necesitas, a costa del overhead de la pila de recursión.
- **Tabulación (bottom-up):** un bucle iterativo que llena la tabla en orden. Sin overhead de recursión y suele permitir optimizar el espacio (a menudo guardas solo las últimas filas).

## Fibonacci: el arquetipo que muestra el ahorro

La recurrencia `dp[i] = dp[i-1] + dp[i-2]` con `dp[0]=0, dp[1]=1` es la DP más simple, y revela por qué la memoria importa:

| Implementación | Tiempo | Espacio |
|---------------|--------|---------|
| Recursión ingenua | $O(2^n)$ | $O(n)$ pila |
| Memoización | $O(n)$ | $O(n)$ |
| Tabulación | $O(n)$ | $O(n)$ |
| Solo 2 variables | $O(n)$ | $O(1)$ |

La recursión ingenua es exponencial porque **recalcula** `fib(n-2)` una y otra vez; la memoización lo arregla guardando cada resultado. Y como `dp[i]` solo mira dos atrás, ni siquiera necesitas la tabla entera: dos variables bastan ($O(1)$ espacio). *Subir escaleras de 1 o 2 pasos* es literalmente este Fibonacci.

## Monedas: la trampa del greedy

Dos problemas clásicos sobre un conjunto de monedas:

- **Mínimo de monedas para sumar `amount`:** `dp[0]=0`; `dp[j] = min(dp[j-coin] + 1)` sobre cada moneda. La intuición: "¿qué moneda usé *de última*?". Cada opción se apoya en un subproblema ya resuelto. $O(\text{amount}\times|\text{coins}|)$.
- **Número de formas de sumar `amount`:** `dp[0]=1`; para cada moneda, para cada `j` de `coin` a `amount`: `dp[j] += dp[j-coin]`. El **orden de los bucles importa**: la moneda en el bucle externo evita contar `(1,3)` y `(3,1)` como formas distintas.

> **Predicción antes de seguir:** ¿el greedy (toma siempre la moneda más grande que quepa) da el óptimo? Con monedas `{1,3,4}` y `amount=6`, el greedy hace `4+1+1 = 3` monedas; la DP encuentra `3+3 = 2`. El greedy **falla** con monedas arbitrarias; solo es seguro con sistemas "canónicos" como `{1,5,10,25}`. La lección: desconfía del greedy salvo que un *exchange argument* lo justifique.

## Problemas de dos secuencias: LCS y edit distance

Cuando el problema compara **dos** cadenas, el estado es bidimensional: `dp[i][j]` resuelve los prefijos `X[1..i]` y `Y[1..j]`.

- **Subsecuencia común más larga (LCS):** si `X[i]==Y[j]`, los últimos caracteres coinciden → `dp[i][j] = dp[i-1][j-1] + 1`; si no, `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`. $O(mn)$.
- **Edit distance (Levenshtein):** mínimo de inserciones/borrados/reemplazos para convertir A en B. Si los últimos caracteres coinciden, no cuesta nada (`dp[i-1][j-1]`); si no, pagas 1 más el mínimo de las tres operaciones. Casos base: `dp[i][0]=i` (borrar todo), `dp[0][j]=j` (insertar todo).

Ambas son el mismo patrón —"¿el último carácter coincidió o no?"— y aparecen en diff de archivos y alineamiento de ADN.

## Mochila y sus parientes

La **mochila 0/1** ($n$ ítems con peso $w_i$ y valor $v_i$, capacidad $W$) es el arquetipo de "decisión bajo recurso limitado". Con la optimización a 1D:

```
para cada item i:
    para j de W bajando hasta w_i:     # orden INVERSO: cada ítem una vez
        dp[j] = max(dp[j], dp[j - w_i] + v_i)
```

El detalle decisivo es el **orden inverso** de `j`: recorrer hacia atrás garantiza que cada ítem se use a lo sumo una vez (0/1); recorrer hacia adelante permitiría reusarlo (esa es la **mochila ilimitada**, y también el *rod cutting*). $O(nW)$ tiempo, $O(W)$ espacio. La pregunta-recurrencia es siempre la misma: "¿incluyo el último ítem o no?".

Otros que vale reconocer de un vistazo: **palíndromo más largo** (`dp[i][j]` = "¿`s[i..j]` es palíndromo?", construyendo por longitud), **decode ways** (cuidado con el `'0'`, que no decodifica solo), **DP con bitmask** (para $n\le 20$, codifica el subconjunto usado en los bits de un entero; base del TSP en $O(2^n n^2)$), y **DP de transacciones bursátiles** ($k$ compraventas con `dp[k][i]`).

---

## Mini-ejemplo trabajado: coin change mínimo, llenando la tabla

Monedas {1, 3, 4}, objetivo amount=6. `dp[j]` = mínimo de monedas para sumar j. Base `dp[0]=0`:

- `dp[1]` = 1 (una de 1)
- `dp[2]` = 2 (1+1)
- `dp[3]` = 1 (una de 3)
- `dp[4]` = 1 (una de 4)
- `dp[5]` = min(dp[5−1], dp[5−3], dp[5−4]) + 1 = min(dp[4], dp[2], dp[1]) + 1 = min(1,2,1)+1 = **2** (1+4 ó 3+... )
- `dp[6]` = min(dp[5], dp[3], dp[2]) + 1 = min(2,1,2)+1 = **2** (3+3)

Cada `dp[j]` pregunta "¿qué moneda usé *de última*?" y se apoya en un subproblema ya resuelto — eso *es* DP: recursión con memoria sobre el último paso.

**Predicción antes de seguir:** con monedas {1, 3, 4} y amount=6, ¿el **greedy** (toma la moneda más grande que quepa) da el óptimo? Greedy haría 4+1+1 = **3 monedas**; la DP encuentra 3+3 = **2**. Greedy **falla** con monedas arbitrarias; solo es seguro con sistemas "canónicos" como {1,5,10,25}.

## Prototipo, contraejemplo y caso borde

- **Prototipo (subproblemas superpuestos):** Fibonacci/escaleras → el mismo subproblema se recalcula muchas veces → memoiza.
- **Contraejemplo (greedy donde se necesita DP):** coin change con {1,3,4} → greedy subóptimo; knapsack 0/1 también requiere DP.
- **Caso borde (orden de loops en Coin Change 2):** para **contar formas** sin permutaciones duplicadas, la moneda va en el bucle **externo**; invertirlo cuenta (1,3) y (3,1) como distintos.

## Errores típicos

- **Conceptual:** memoizar sin subproblemas superpuestos (no aporta) o elegir un estado que no captura todo lo necesario para decidir.
- **Técnico:** en knapsack 0/1 recorrer la capacidad **hacia adelante** (eso es unbounded, reusa el ítem) en vez de en orden inverso.
- **De interpretación:** aplicar greedy a coin change con monedas arbitrarias.

## Transferencia isomorfa

- **Escaleras (1 ó 2 pasos) ↔ Fibonacci:** la recurrencia dp[i]=dp[i−1]+dp[i−2] es *literalmente* el conejo de Fibonacci del brainteaser quant (conecta con [[arena-q12]]).
- **Edit distance / LCS ↔ alineamiento de secuencias:** la misma DP de dos secuencias aparece en diff de archivos y en alineamiento de ADN/eventos clínicos (conecta con [[arena-h7]], series temporales de eventos).
- **Knapsack ↔ subset-sum / asignación bajo presupuesto:** maximizar valor bajo una capacidad es el patrón de cualquier decisión con recurso limitado (conecta con [[arena-h21]], asignación).

Moraleja de la arista: *DP = recursión con memoria; encuentra el estado mínimo y pregunta "¿qué pasó en el último paso?" — y desconfía del greedy salvo que un exchange argument lo justifique.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Cuenta formas de llegar a X" | DP: dp[i] = suma de estados anteriores |
| "Mínimo/máximo costo para X" | DP con recurrencia de optimización |
| "¿Tiene sentido memorizarlo?" | ¿Hay subproblemas superpuestos? → sí |
| "n items, capacidad W" | Knapsack (0/1 si un uso, unbounded si ilimitado) |
| "Dos secuencias, alinear/comparar" | LCS o Edit Distance |
| "Subconjunto con suma X" | DP de mochila sobre suma |
| "n pequeño (≤20) con subconjuntos" | Bitmask DP |
| "Elección local lleva a global" | Greedy (demostrar con exchange) |

---

> **Síntesis:** DP = recursión con memoria. El truco es encontrar el estado mínimo que captura todo lo necesario para tomar la decisión. La recurrencia viene de preguntarte: "¿qué pasó en el último paso?" (escalera: último escalón fue de 1 o 2; mochila: incluiste o no el último ítem; LCS: el último carácter coincidió o no).

---

*Retrieval: cierra y responde: (1) recurrencia de coin change (mínimo); (2) dp[3][2] para LCS de "ABCD" y "ACBD"; (3) complejidad de knapsack 0/1 con n=100 items y W=1000; (4) cuándo NO usar greedy para coin change.*
