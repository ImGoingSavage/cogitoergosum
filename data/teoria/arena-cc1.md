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

## Intuición: la tabla hash es *memoria comprada*

Antes de la fórmula, la idea profunda: una tabla hash **cambia tiempo por espacio**. En lugar de re-escanear el array (O(n) por consulta), pagas memoria una vez para poder *recordar* lo que ya viste y responder en O(1). La analogía: es la diferencia entre buscar un nombre releyendo toda la guía telefónica cada vez (array) y tener un índice que te lleva directo a la página (hash). Cada vez que un problema dice "¿ya vi esto antes?", "¿cuántas veces aparece?", "¿existe su pareja?", la respuesta casi siempre es *guarda lo visto en un mapa*.

## Prototipo, contraejemplo y caso borde

- **Prototipo (hash brilla):** Two Sum. Necesitas, para cada `x`, saber si `target − x` ya apareció. Memoria comprada = O(1) por consulta.
- **Contraejemplo (hash *no* conviene):** "el k-ésimo elemento más pequeño" o "pares en array **ordenado**". Aquí el orden ya es estructura gratis: two pointers o búsqueda binaria resuelven en O(1) espacio. Meter un hash desperdicia la información del orden — señal de que elegiste mal la herramienta.
- **Caso borde:** duplicados y colisiones de clave. En Two Sum con `[3,3]` y target 6, si insertas *antes* de consultar te emparejas contigo mismo; si hay claves repetidas y guardas solo el último índice, pierdes pares. El borde revela la condición oculta: **consulta antes de insertar**.

## Errores típicos

- **Conceptual:** asumir O(1) *garantizado*. Es O(1) **amortizado**; con un adversario que fuerza colisiones, degrada a O(n) por operación. En entrevista, dilo: "O(1) promedio, O(n) peor caso".
- **Técnico:** insertar el elemento en el mapa antes de buscar su complemento → falsos positivos consigo mismo.
- **De interpretación:** usar hash cuando el enunciado dice "**contiguo**" (eso es ventana deslizante) o "**ordenado**" (eso es two pointers). La palabra del enunciado es la señal; el hash es para "¿existe / cuántos?".

## Transferencia isomorfa

La estructura "recordar lo visto para responder en O(1)" reaparece fuera de los arrays:

- **Eventos clínicos:** deduplicar diagnósticos por `patient_id` es exactamente un *hash set* de claves vistas; contar visitas por paciente es el *hash contador* de frecuencias.
- **Two Sum ↔ emparejar exposición-control:** "¿existe para este paciente expuesto uno de control con el mismo propensity score?" es buscar el *complemento* en un índice — el mismo patrón del complemento `target − x`, ahora sobre cohortes (conecta con [[propensity-score]] de Health AI).
- **Rolling hash ↔ ventana temporal:** el hash deslizante de Rabin-Karp es isomorfo a una ventana temporal de exposición clínica que se actualiza incrementalmente en lugar de recalcularse.

Moraleja de la arista: *el array es solo el disfraz; la estructura profunda es "memoria indexada para consulta O(1)", y esa estructura es la misma en SQL, en cohortes y en streams.*

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
