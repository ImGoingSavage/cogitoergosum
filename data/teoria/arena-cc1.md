# Arrays, cadenas y tablas hash

## La tabla hash — el arma universal de MAANG

Una tabla hash mapea keys a values en tiempo O(1) amortizado.

**Operaciones:** insert, lookup, delete → O(1) promedio; O(n) peor caso (todos al mismo bucket).

**Factor de carga α = n/m** (n=elementos, m=buckets). Para α < 0.75: rendimiento estable.

**Resolución de colisiones:**
- **Chaining:** cada bucket es una lista enlazada. Lookup: O(1+α).
- **Open addressing (probing lineal):** si hay colisión, prueba slot+1, slot+2,... Sensible a clusters.

**Cuándo usar tabla hash:** detección de duplicados, frecuencias, lookup en O(1), two-sum, anagramas.

---

## Two Sum — el patrón fundamental de hash map

Problema: dado array nums y target, retorna índices i,j tal que nums[i]+nums[j]=target.

**Solución O(n) con hash map:**
1. Para cada elemento x en el array
2. Busca `complement = target - x` en el mapa
3. Si existe: retorna (mapa[complement], índice actual)
4. Si no: inserta mapa[x] = índice actual

**Por qué no O(n²):** el complemento se busca en O(1), no O(n).

Generalización: three-sum → fijar un elemento y reducir a two-sum. Four-sum → O(n²) con hash.

---

## Ventana deslizante (sliding window)

**Patrón:** mantener una ventana [left, right] sobre el array y actualizarla en O(1) por paso.

**Ventana fija (tamaño k):** suma máxima de subarray de longitud k.
1. Calcula suma de primeros k elementos
2. Desliza: suma += arr[right] − arr[left−1]
3. Tiempo: O(n), espacio: O(1)

**Ventana variable (condición):** cadena más larga sin repetir caracteres.
1. Usa hash map de frecuencias + puntero left
2. right avanza siempre; left avanza solo cuando se viola la condición
3. Tiempo: O(n), espacio: O(min(n,k)) donde k=tamaño del alfabeto

**Señal de sliding window:** "subarreglo/subcadena contigua con propiedad X".

---

## Dos punteros (two pointers)

**Array ordenado:** para encontrar pares con suma objetivo:
- left=0, right=n−1
- Si nums[left]+nums[right] == target: encontrado
- Si < target: left++; si > target: right--
- Tiempo: O(n)

**Partición:** Dutch National Flag (3-way partition para ordenar {0,1,2}):
- low=0, mid=0, high=n−1
- nums[mid]==0: swap(low,mid), low++, mid++
- nums[mid]==1: mid++
- nums[mid]==2: swap(mid,high), high--
- Tiempo: O(n), un solo paso

**Señal de two pointers:** array ordenado, o problema que pide pares/tríos con suma.

---

## Complejidad amortizada y operaciones de arrays

| Operación | Array dinámico | Array fijo |
|-----------|---------------|-----------|
| Acceso por índice | O(1) | O(1) |
| Insert al final | O(1) amortizado | — |
| Insert al medio | O(n) | O(n) |
| Búsqueda lineal | O(n) | O(n) |
| Búsqueda binaria (ordenado) | O(log n) | O(log n) |

**Análisis amortizado:** un array dinámico duplica capacidad al llenarse. Aunque una inserción individual toma O(n), el costo por inserción promediado sobre n inserciones es O(1).

---

## Intervalos solapados (merge intervals)

Dado un conjunto de intervalos [sᵢ,eᵢ], combina los que se solapan.

**Algoritmo:**
1. Ordena por inicio sᵢ → O(n log n)
2. Recorre: si el intervalo actual comienza ≤ fin del anterior, expande el fin
3. Si no, añade a resultado y avanza

**Invariante:** los intervalos ya procesados en resultado son disjuntos y ordenados.

Ejemplo: [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]

---

## Producto de array excepto el índice propio

Sin usar división: calcula result[i] = producto de todos menos nums[i].

**Algoritmo O(n) en O(1) espacio extra:**
1. Pase izquierda: result[i] = producto de nums[0..i-1]
2. Pase derecha: acumula sufijo de derecha a izquierda y multiplica

```
nums   = [1, 2, 3, 4]
prefix = [1, 1, 2, 6]     # producto de todo a la izquierda
result = [24,12,8, 6]      # multiplicar por sufijo derecho
```

---

## Rotación de array

Rotar n elementos k posiciones a la derecha:

**Método de 3 reversos** (O(n) tiempo, O(1) espacio):
1. Reversa todo el array
2. Reversa los primeros k elementos
3. Reversa los últimos n-k elementos

Ejemplo k=2: [1,2,3,4,5] → [5,4,3,2,1] → [4,5,3,2,1] → [4,5,1,2,3] ✓

---

## Rabin-Karp — hashing de cadenas

Búsqueda de patrón de longitud m en texto de longitud n: O(n+m) esperado.

Hash rodante (rolling hash): H([i+1..i+m]) = (H([i..i+m-1]) − text[i]·b^{m-1})·b + text[i+m]

Actualizar el hash en O(1) por posición → O(n) total.

Aplicación: detección de plagios, substring search, Longest Duplicate Substring.

---

## Trampa del agua (trapping rain water) — concepto

Para cada posición i, el agua acumulada = min(max_left[i], max_right[i]) − height[i].

**Precomputar:** max_left[i] = max(height[0..i]), max_right[i] = max(height[i..n-1]).

**Versión O(1) espacio:** dos punteros que avanzan desde los extremos.

Ilustra el principio: "la cantidad de agua depende del mínimo de las dos paredes más altas".

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿Existen dos elementos con suma X?" | Hash map: complemento en O(1) |
| "Subcadena/subarreglo contiguo" | Sliding window |
| "Pares en array ordenado" | Two pointers desde los extremos |
| "Frecuencia de elementos" | Hash map contador |
| "Detectar duplicados en O(n)" | Hash set |
| "Productos sin división" | Pases izquierda + derecha |
| "Ordenar {0,1,2}" | Dutch national flag (3 punteros) |
| "Buscar patrón en texto rápido" | Rabin-Karp rolling hash |

---

> **Síntesis:** El 80% de los problemas de arrays en MAANG se resuelven con tres herramientas: (1) hash map para lookup O(1), (2) sliding window para subarreglos contiguos, (3) two pointers para pares en arrays ordenados. La clave es reconocer cuál aplica: si el enunciado dice "contiguo" → ventana; si dice "par/trío con suma" → punteros; si dice "¿existe X?" → hash.

---

*Retrieval: cierra y responde: (1) complejidad de two-sum con hash map; (2) cómo actualizar sliding window al mover right un paso; (3) steps para merge intervals; (4) complejidad amortizada de insert al final de array dinámico.*
