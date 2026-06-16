# Ordenamiento, búsqueda binaria y manipulación de bits

## De qué trata esta lección (y qué sabrás hacer al final)

Ordenar y buscar son los dos verbos más antiguos de la computación, y siguen siendo el corazón de media entrevista. Esta lección los construye desde cero con la mirada que importa en una entrevista: no recitar algoritmos, sino saber **cuál elegir y por qué**, y reconocer la **búsqueda binaria donde no hay un arreglo ordenado a la vista** —su forma más poderosa, "binaria sobre la respuesta"—. Cierra con los trucos de bits y XOR, que son invariantes de conteo disfrazados.

Al terminar podrás: (1) elegir entre QuickSort, MergeSort y HeapSort por sus garantías (tiempo, espacio, estabilidad); (2) escribir una búsqueda binaria correcta —incluido el `mid` sin overflow y las variantes de primera/última ocurrencia y arreglo rotado—; (3) reconocer "mínimo X tal que condición(X)" como binaria sobre un predicado **monótono**; y (4) usar QuickSelect, heaps de tamaño $k$ y trucos de XOR (número faltante, swap sin temporal). Cada técnica entra por su intuición y un mini-ejemplo. La idea unificadora: **la búsqueda binaria sirve para cualquier propiedad monótona, no solo para arreglos ordenados.**

---

## Elegir el ordenamiento por sus garantías

| Algoritmo | Tiempo promedio | Tiempo peor | Espacio | Estable |
|-----------|----------------|------------|---------|---------|
| QuickSort | $O(n\log n)$ | $O(n^2)$ | $O(\log n)$ | No |
| MergeSort | $O(n\log n)$ | $O(n\log n)$ | $O(n)$ | Sí |
| HeapSort | $O(n\log n)$ | $O(n\log n)$ | $O(1)$ | No |
| TimSort (Python) | $O(n\log n)$ | $O(n\log n)$ | $O(n)$ | Sí |
| CountingSort | $O(n+k)$ | $O(n+k)$ | $O(k)$ | Sí |
| RadixSort | $O(d(n+k))$ | $O(d(n+k))$ | $O(n+k)$ | Sí |

No memorices la tabla; razónala por la pregunta del entrevistador. **¿QuickSort o MergeSort?** QuickSort es *in-place* (memoria $O(\log n)$ de la recursión) y tiene la mejor constante en la práctica, pero un pivote desafortunado lo lleva a $O(n^2)$ —por eso se elige el pivote al azar—. MergeSort **garantiza** $O(n\log n)$ y es **estable** (no reordena elementos iguales), a costa de $O(n)$ de espacio; es el preferido para datos externos o cuando la estabilidad importa. **HeapSort** es el único $O(n\log n)$ garantizado *e* in-place, pero no estable. Y los ordenamientos **no comparativos** (Counting, Radix) rompen la barrera $O(n\log n)$ explotando que las claves son enteros pequeños —cuentan en vez de comparar—.

## Búsqueda binaria: el invariante de "la respuesta está en [left, right]"

La búsqueda binaria divide a la mitad el espacio en cada paso, dando $O(\log n)$. Lo que la hace correcta es un **invariante**: la respuesta, si existe, siempre vive en el intervalo `[left, right]`, que va encogiendo.

```
left, right = 0, n-1
while left <= right:
    mid = left + (right - left) // 2     # evita overflow de (left+right)
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
return -1
```

El detalle `mid = left + (right-left)//2` no es cosmético: en lenguajes con enteros acotados, `(left+right)` puede **desbordar**; esta forma no. Variantes que conviene dominar: **primera/última ocurrencia** (al encontrar el target, no pares: sigue buscando hacia el lado correspondiente); **arreglo rotado sin duplicados** (en cada paso, un lado del `mid` está ordenado —detecta cuál comparando `arr[mid]` con `arr[left]`— y decide si el target cae en ese lado ordenado o en el otro).

## Búsqueda binaria sobre la respuesta: la versión que separa a los buenos

Aquí está la idea más valiosa de la lección. A veces no hay arreglo que buscar, pero el **dominio de la respuesta** es monótono: si un valor $X$ "funciona", todos los mayores (o menores) también. Entonces buscas binariamente el **umbral**, evaluando un predicado en vez de comparar elementos:

```
# Busca el MÍNIMO X tal que condicion(X) es True
left, right = dominio_min, dominio_max
while left < right:
    mid = (left + right) // 2
    if condicion(mid): right = mid       # mid sirve; busca uno menor
    else:              left = mid + 1     # mid no sirve; sube
return left
```

El patrón aparece disfrazado en muchos enunciados: "mínima velocidad para llegar a tiempo", "capacidad mínima de un barco para entregar en $D$ días", "$k$-ésimo elemento más pequeño en una matriz ordenada". En todos, conviertes un problema de **optimización** en "hallar el primer True de un predicado monótono". El coste es $O(\log(\text{rango}) \times \text{costo de condicion})$.

> **Predicción antes de seguir:** ¿puedes usar binaria sobre la respuesta si el predicado oscila (True, False, True…)? Respuesta: **no**. La binaria exige **monotonía**: que una vez que el predicado se vuelve True, siga True. Sin esa garantía, descartar media mitad es incorrecto. Antes de aplicarla, verifica que la condición sea monótona en el dominio.

## QuickSelect: el $k$-ésimo sin ordenar todo

Si solo quieres el $k$-ésimo elemento más pequeño, ordenar todo ($O(n\log n)$) es desperdicio. **QuickSelect** reutiliza la partición de QuickSort: elige un pivote, particiona, y mira **dónde quedó el pivote**. Si quedó en la posición $k$, terminaste; si $k$ está a su izquierda, recurres solo en la izquierda (y viceversa). Como cada paso descarta un lado, el trabajo esperado es $O(n) + O(n/2) + \dots = O(n)$ esperado (peor caso $O(n^2)$, mitigado con pivote aleatorio). La variante "median of medians" lo garantiza en $O(n)$ a costa de más complejidad.

## Heaps y colas de prioridad

Un **heap** es un árbol binario completo con la propiedad de que cada padre es $\le$ sus hijos (min-heap). Se guarda en un arreglo sin punteros: el hijo izquierdo de $i$ está en $2i+1$, el derecho en $2i+2$, el padre en $\lfloor(i-1)/2\rfloor$.

| Operación | Min-Heap |
|-----------|---------|
| Insert | $O(\log n)$ |
| Peek mínimo | $O(1)$ |
| Extract mínimo | $O(\log n)$ |
| Build heap | $O(n)$ — sí, lineal, no $n\log n$ |

El "build en $O(n)$" sorprende: aunque cada *sift-down* cuesta hasta $O(\log n)$, la mayoría de los nodos están cerca de las hojas (poco que bajar), y la suma converge a $O(n)$. La regla de oro de entrevista: para los **$k$ más grandes**, usa un **min-heap de tamaño $k$** (expulsa el menor cada vez que crece) → $O(n\log k)$, mucho mejor que ordenar todo. Heaps potencian top-$k$, merge de $k$ listas ordenadas, Dijkstra y la mediana en streaming (dos heaps).

## Ordenamientos por conteo y trucos de bits

**CountingSort** cuenta cuántas veces aparece cada valor y reconstruye: $O(n+k)$ con $k$ = rango. Solo sirve para enteros de rango chico. **RadixSort** ordena dígito por dígito (del menos al más significativo) usando CountingSort en cada uno: para enteros de 32 bits en base 256, son 4 pasadas → efectivamente $O(n)$.

Los **trucos de bits** son aritmética de conjuntos en binario:

| Operación | Expresión | Uso |
|-----------|-----------|-----|
| ¿Potencia de 2? | `n & (n-1) == 0` | un solo bit encendido |
| Bit más bajo encendido | `n & (-n)` | aislar el lowest set bit |
| Leer/encender/apagar bit $k$ | `(n>>k)&1` / `n\|(1<<k)` / `n & ~(1<<k)` | manipular bit $k$ |
| Cancelación | `x ^ x = 0`, `x ^ 0 = x` | base de los trucos de XOR |

El **conteo de Kernighan** (`n = n & (n-1)` apaga el bit más bajo, repetido hasta 0) itera tantas veces como bits encendidos haya.

## Trucos de XOR e invariantes de conteo

El XOR cumple `x^x=0` y `x^0=x`, así que **lo que aparece en par se cancela**. De ahí salen joyas:

- **Número faltante en $[1..n]$:** haz XOR de $1\oplus2\oplus\dots\oplus n$ contra el XOR de los elementos del arreglo; todo lo presente se cancela en pares y queda el faltante.
- **Único sin pareja** (todos los demás aparecen dos veces): XOR de todo el arreglo.
- **Swap sin variable temporal:** `a^=b; b^=a; a^=b` (porque `a^b^b=a` y `a^a^b=b`).

Y el **voto de Boyer-Moore** halla el elemento mayoritario (>$n/2$) en $O(n)$ tiempo, $O(1)$ espacio, con la intuición de que cada voto del mayoritario y un voto contrario **se cancelan**, y el verdadero mayoritario siempre sobrevive a la cancelación. Es el mismo espíritu del XOR: un invariante de conteo.

---

## Mini-ejemplo trabajado: búsqueda binaria sobre la respuesta

"Un barco debe llevar todos los paquetes en ≤ 5 días; ¿la **mínima capacidad** diaria?" El truco: no buscas en un array, buscas en el **dominio de la respuesta** (capacidades), que es **monótono**: si una capacidad C funciona, toda capacidad > C también.

- `condicion(C)` = "¿se puede en ≤ 5 días con capacidad C?" (simulas en O(n)).
- Rango: `left = max(paquete)` (no puedes llevar menos que el paquete más grande), `right = suma(paquetes)` (todo en un día).
- Binaria: si `condicion(mid)` es True, baja `right=mid` (busca menor); si no, `left=mid+1`.

Conviertes un problema de optimización en **buscar el primer True** sobre un predicado monótono — el mismo esqueleto sirve para "mínima velocidad para llegar a tiempo" o "kth smallest en matriz ordenada".

**Predicción antes de seguir:** te dan [1..n] con un número faltante y quieres O(1) espacio. ¿Cómo? **XOR** de 1..n contra el XOR del array: como `x^x=0`, todo lo presente se cancela y queda el faltante. La cancelación del XOR es un **invariante** puro.

## Prototipo, contraejemplo y caso borde

- **Prototipo (binaria sobre respuesta):** cualquier "mínimo/máximo X tal que condición(X)" con condición monótona.
- **Contraejemplo (binaria sin monotonía):** aplicar búsqueda binaria a un predicado que oscila (True/False/True) → no converge; la binaria exige monotonía.
- **Caso borde (overflow del mid):** `mid = (left+right)/2` puede desbordar; usa `left + (right-left)/2`.

## Errores típicos

- **Conceptual:** creer que la búsqueda binaria es solo para arrays ordenados; sirve para **cualquier propiedad monótona**.
- **Técnico:** condiciones de parada mal puestas en "primera/última ocurrencia" → bucle infinito o off-by-one.
- **De heap:** para los k **más grandes**, usar un max-heap de todo (O(n log n)) en vez de un **min-heap de tamaño k** (O(n log k)).

## Transferencia isomorfa

- **Binaria sobre respuesta ↔ monotonicidad como heurística:** explotar "si X cumple, todo lo mayor también" es la misma palanca que ordena el espacio de soluciones en optimización y en parada óptima (conecta con [[arena-q8]], parada óptima).
- **XOR / Boyer-Moore ↔ invariante:** "lo que se empareja se cancela" y "el mayoritario sobrevive a los votos" son invariantes de conteo, el corazón del brainteaser (conecta con [[arena-q12]]).
- **QuickSelect / median-of-medians ↔ estadísticos de orden:** hallar el k-ésimo sin ordenar todo es el cómputo de cuantiles, base de estimadores robustos (conecta con [[arena-pst1]]).

Moraleja de la arista: *la búsqueda binaria es para cualquier predicado monótono (no solo arrays), y los trucos de XOR son invariantes de conteo disfrazados de bits.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "kth elemento sin ordenar todo" | QuickSelect O(n) promedio |
| "Buscar en array rotado" | Binaria: identificar lado ordenado |
| "Mínimo X tal que condición(X)" | Binaria sobre la respuesta |
| "Top-k elementos" | Min-heap de tamaño k |
| "Merge k listas ordenadas" | Min-heap con (valor, lista_índice) |
| "Número faltante en [1..n]" | XOR acumulado |
| "n & (n-1) == 0" | Es potencia de 2 |
| "Un elemento sin par" | XOR de todos |
| "Mayoritario > n/2 veces" | Boyer-Moore voting |
| "Contar inversiones" | MergeSort modificado |

---

> **Síntesis:** La búsqueda binaria no es solo para arrays ordenados — es para cualquier problema con propiedad monótona (si X cumple, todo lo menor/mayor también). El truco de bitmask (n&(n-1)) es más rápido que contar. QuickSort gana en práctica, MergeSort gana en garantías y estabilidad. La regla del heap: para los k más grandes usa un min-heap de tamaño k (expulsa los pequeños).

---

*Retrieval: cierra y responde: (1) cómo encontrar el número faltante en [1..n] con XOR; (2) complejidad de build-heap; (3) cómo buscar en array rotado con binaria; (4) cuántas iteraciones toma Kernighan para n=12 (0b1100).*
