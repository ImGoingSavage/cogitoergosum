# Ordenamiento, búsqueda binaria y manipulación de bits

## Comparación de algoritmos de ordenamiento

| Algoritmo | Tiempo promedio | Tiempo peor | Espacio | Estable |
|-----------|----------------|------------|---------|---------|
| QuickSort | O(n log n) | O(n²) | O(log n) | No |
| MergeSort | O(n log n) | O(n log n) | O(n) | Sí |
| HeapSort | O(n log n) | O(n log n) | O(1) | No |
| TimSort (Python) | O(n log n) | O(n log n) | O(n) | Sí |
| InsertionSort | O(n²) | O(n²) | O(1) | Sí |
| CountingSort | O(n+k) | O(n+k) | O(k) | Sí |
| RadixSort | O(d·(n+k)) | O(d·(n+k)) | O(n+k) | Sí |

**QuickSort vs MergeSort:**
- QuickSort: in-place, mejor constante, pero O(n²) con pivote malo. Usar pivot aleatorio.
- MergeSort: garantiza O(n log n), estable, pero O(n) espacio. Preferido para datos externos.

---

## Búsqueda binaria — el patrón general

**Invariante:** la respuesta siempre está en [left, right].

```
left, right = 0, n-1
while left <= right:
    mid = left + (right - left) // 2   # evita overflow
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
return -1
```

**Primera/última ocurrencia:** cambia la condición de parada para seguir buscando hacia la izquierda/derecha cuando encuentras el target.

**Búsqueda en array rotado** (sin duplicados):
- Si arr[mid] >= arr[left]: lado izquierdo está ordenado
- Si target está en ese lado ordenado → busca ahí; si no → lado derecho

---

## Búsqueda binaria sobre la respuesta

Patrón: cuando el dominio de la respuesta es monótono (si X es posible, X-1 también lo es).

```
Busca el mínimo X tal que condición(X) == True

left, right = dominio_mínimo, dominio_máximo
while left < right:
    mid = (left + right) // 2
    if condicion(mid): right = mid
    else: left = mid + 1
return left
```

**Ejemplos:**
- Mínima velocidad para llegar a tiempo → buscar sobre velocidades
- Capacidad mínima de barco → buscar sobre capacidades
- kth smallest element en matriz ordenada → buscar sobre valores

---

## QuickSelect — kth elemento en O(n) esperado

Para encontrar el k-ésimo elemento más pequeño sin ordenar todo:

1. Elige pivote, particiona: menores izquierda, mayores derecha
2. Si el pivote queda en posición k → retorna
3. Si k < posición pivote → recurre en la izquierda
4. Si k > posición pivote → recurse en la derecha

**Tiempo:** O(n) promedio, O(n²) peor caso (con pivot aleatorio, O(n) esperado).

Alternativa garantizada O(n): "Median of medians" — más complejo.

---

## Conteo de inversiones (Merge Sort)

Una **inversión** en un array es un par (i,j) con i<j pero arr[i]>arr[j].

Contar inversiones en O(n log n) integrando el conteo en Merge Sort:
- Al hacer merge, si arr[left_i] > arr[right_j]: todas las posiciones restantes de la izquierda forman inversiones con arr[right_j].
- Sumar: inversiones += (mid - left_i + 1)

**Aplicación:** mide cuán lejos está un array de estar ordenado.

---

## HeapSort y Priority Queue

**Heap (min o max):** árbol binario completo donde cada padre ≤ hijos (min-heap).

Representación en array: hijo izquierdo en 2i+1, hijo derecho en 2i+2, padre en ⌊(i-1)/2⌋.

| Operación | Min-Heap |
|-----------|---------|
| Insert | O(log n) |
| Peek min | O(1) |
| Extract min | O(log n) |
| Build heap | O(n) — sorprendente: no O(n log n) |

**HeapSort:** build max-heap en O(n), luego extraer n veces en O(log n) → O(n log n) total, O(1) espacio.

**Usos comunes:** top-k elementos, merge de k listas ordenadas, Dijkstra, median dinámico (dos heaps).

---

## RadixSort y CountingSort

**CountingSort:** cuenta frecuencias de cada valor, acumula. O(n+k) donde k=rango de valores. Solo funciona para enteros pequeños.

**RadixSort:** ordena dígito por dígito (del menos al más significativo), usando CountingSort en cada dígito.
- d dígitos, base b: O(d·(n+b))
- Para enteros de 32 bits con base 2^8: d=4 pasadas, O(4(n+256)) = O(n)

**RadixSort domina** cuando d es pequeño y n es grande — útil para strings de longitud fija.

---

## Manipulación de bits

| Operación | Expresión | Uso |
|-----------|-----------|-----|
| Es potencia de 2 | n & (n-1) == 0 | Verifica power of 2 |
| Último bit encendido | n & (-n) | Lowest set bit |
| Contar bits encendidos | bin(n).count('1') o Kernighan | Hamming weight |
| XOR de dos iguales | x^x = 0 | Cancelación |
| XOR con 0 | x^0 = x | Identidad |
| Aislar bit k | (n >> k) & 1 | Leer bit k |
| Encender bit k | n | (1 << k) | Set bit k |
| Apagar bit k | n & ~(1 << k) | Clear bit k |

**Kernighan bit count:** n = n & (n-1) elimina el bit más bajo → repetir hasta n=0. Itera O(número de bits encendidos).

---

## Trucos de XOR

**Encontrar el número faltante** en [1..n]: XOR de 1..n y XOR de los elementos del array → el resultado es el faltante (por la propiedad x^x=0).

**Encontrar el único elemento no duplicado** en un array donde todos los demás aparecen dos veces: XOR de todos los elementos.

**Swap sin variable temporal:**
```
a ^= b
b ^= a
a ^= b
```

**Por qué funciona:** a^b^b = a; a^a^b = b.

---

## Elemento mayoritario (Boyer-Moore Voting)

Encontrar el elemento que aparece más de n/2 veces en O(n) tiempo y O(1) espacio.

```
candidate = None, count = 0
Para cada elemento x:
    if count == 0: candidate = x
    count += (1 if x == candidate else -1)
return candidate
```

**Intuición:** cada vez que el candidato "pierde" un voto contra un no-candidato, ambos se cancelan. El verdadero mayoritario siempre sobrevive.

---

## Encontrar pico (Peak Finding)

Un pico es un elemento mayor que sus vecinos. Siempre existe en cualquier array.

**Búsqueda binaria:** si arr[mid] < arr[mid+1]: pico en la derecha. Si arr[mid] < arr[mid-1]: pico en la izquierda. Si ninguno: arr[mid] es pico.

**Tiempo:** O(log n) — binaria sobre la monotonía local.

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
