# Recursión y programación dinámica

## El patrón de DP en 4 pasos

1. **Define el estado:** ¿qué es dp[i]? (la respuesta al subproblema de tamaño i)
2. **Recurrencia:** cómo dp[i] depende de estados anteriores
3. **Caso base:** dp[0], dp[1], etc.
4. **Orden de llenado:** bottom-up (tabulation) o top-down (memoization)

**Memoization vs Tabulation:**
- Memoization (top-down): recursión + diccionario de caché. Fácil de derivar, llena solo los subproblemas necesarios.
- Tabulation (bottom-up): bucle iterativo. Sin overhead de recursión, mejor para espacio.

---

## Fibonacci — el arquetipo

```
dp[0] = 0, dp[1] = 1
dp[i] = dp[i-1] + dp[i-2]
```

| Implementación | Tiempo | Espacio |
|---------------|--------|---------|
| Recursión naive | O(2^n) | O(n) pila |
| Memoization | O(n) | O(n) |
| Tabulation | O(n) | O(n) |
| Optimizado (solo 2 vars) | O(n) | O(1) |

**Matrix exponentiation:** Fib(n) en O(log n) — relevante para n muy grande.

---

## Subida de escaleras / combinaciones de monedas

**Climbing Stairs (k pasos permitidos):**

dp[i] = Σ dp[i−j] para j en pasos_permitidos

Para pasos={1,2}: dp[i]=dp[i-1]+dp[i-2] (idéntico a Fibonacci).

**Coin Change (mínimo de monedas):**

dp[0]=0; dp[amount] = min(dp[amount-coin]+1) para cada coin.

Tiempo: O(amount × |coins|), espacio: O(amount).

**Coin Change 2 (número de formas):**

dp[0]=1; para cada coin: para cada j de coin a amount: dp[j] += dp[j-coin].

El orden de los loops importa: coin en el externo evita permutaciones duplicadas.

---

## Subsecuencia común más larga (LCS)

X[1..m], Y[1..n]. LCS(X,Y) = longitud de la subsecuencia común más larga.

```
dp[i][j] = LCS de X[1..i] y Y[1..j]

Si X[i] == Y[j]: dp[i][j] = dp[i-1][j-1] + 1
Else:            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Tiempo:** O(mn), **Espacio:** O(mn) o O(min(m,n)) optimizado.

**Aplicaciones:** diff de archivos, DNA alignment, edit distance.

---

## Distancia de edición (Edit Distance / Levenshtein)

Costo mínimo de convertir palabra A en B usando insert, delete, replace (costo 1 cada uno).

```
dp[i][j] = edit distance entre A[1..i] y B[1..j]

Si A[i] == B[j]: dp[i][j] = dp[i-1][j-1]
Else:            dp[i][j] = 1 + min(dp[i-1][j],    # delete en A
                                     dp[i][j-1],    # insert en A
                                     dp[i-1][j-1])  # replace
```

Caso base: dp[i][0]=i (borrar i chars de A), dp[0][j]=j (insertar j chars).

---

## Mochila 0/1 (0/1 Knapsack)

n items, cada uno con peso wᵢ y valor vᵢ. Capacidad W. Maximizar valor sin exceder W.

```
dp[j] = max valor con capacidad j

Para cada item i (de 1 a n):
  Para j de W a wᵢ (orden inverso — 0/1: cada item una vez):
    dp[j] = max(dp[j], dp[j - wᵢ] + vᵢ)
```

**Tiempo:** O(nW), **Espacio:** O(W) con la optimización de 1D.

**Unbounded knapsack** (items ilimitados): recorre j hacia adelante.

---

## Corte de varilla (Rod Cutting)

Varilla de longitud n, precio pᵢ por varilla de longitud i. Maximizar ingreso.

Equivalente a unbounded knapsack con longitudes como "pesos" y precios como valores.

dp[j] = max(pᵢ + dp[j−i]) para i de 1 a j.

---

## Subcadena palindrómica más larga

dp[i][j] = True si s[i..j] es palíndromo.

```
dp[i][i] = True (base: un carácter)
dp[i][i+1] = (s[i]==s[i+1])

Para len de 3 a n:
  Para i: j = i+len-1
    dp[i][j] = (s[i]==s[j]) and dp[i+1][j-1]
```

La respuesta es el máximo len tal que dp[i][j]=True.

Tiempo O(n²). Alternativa: Manacher's algorithm en O(n).

---

## Decodificación de string (Decode Ways)

'1' → 'A', ..., '26' → 'Z'. Cuenta formas de decodificar una cadena de dígitos.

```
dp[0]=1, dp[1]=1 (si s[0]!='0')
Para i de 2 a n:
  Si s[i-1]!='0': dp[i] += dp[i-1]   (toma un dígito)
  Si s[i-2..i-1] en [10..26]: dp[i] += dp[i-2]  (toma dos dígitos)
```

Trampa: '0' no puede ser un dígito solo; '30' o '00' no es válido como par.

---

## DP con bitmask

Para n pequeño (≤20), el estado puede incluir un conjunto de elementos usados codificado como bitmask.

**Traveling Salesman Problem (TSP):** dp[mask][i] = costo mínimo de visitar los nodos en mask y terminar en nodo i.

```
dp[(1<<n)-1][i] = camino completo terminando en i.
```

Tiempo: O(2^n · n²). Factible hasta n≈20.

---

## Greedy vs DP

| Problema | Greedy | DP |
|---------|--------|-----|
| Coin change (monedas arbitrarias) | ✗ puede fallar | ✓ |
| Coin change (monedas {1,5,10,25}) | ✓ funciona | ✓ |
| Interval scheduling (max no-solapados) | ✓ ordena por fin | ✓ |
| Knapsack 0/1 | ✗ | ✓ |
| Fractional Knapsack | ✓ ratio v/w | — |
| Shortest path (pesos ≥ 0) | Dijkstra (greedy) | Bellman-Ford (DP) |

**Cuándo greedy:** cuando la elección localmente óptima lleva a la global. Demostrar con exchange argument.

---

## Máxima ganancia en bolsa (k transacciones)

dp[k][i] = max ganancia con k transacciones hasta el día i.

dp[k][i] = max(dp[k][i-1], prices[i] + max_{j<i}(dp[k-1][j] - prices[j]))

Con k=1: una transacción → O(n) con un pase.
Con k=∞: acumula todos los incrementos positivos.
Con k=2: dos transacciones → dp 2D O(n).

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
