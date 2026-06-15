# Hashing, frecuencia y memoria comprada

## El principio central

Un hash map es **memoria comprada**. Pagas O(n) espacio para comprar O(1) tiempo de lookup. En cuanto ves que necesitas "¿ya vi este elemento?" o "¿existe su complemento?", el hash map es la herramienta.

---

## Análisis de complejidad honesto

| Operación | Caso esperado | Peor caso |
|-----------|--------------|-----------|
| Insert    | O(1)         | O(n)      |
| Lookup    | O(1)         | O(n)      |
| Delete    | O(1)         | O(n)      |

El peor caso ocurre cuando todas las claves colisionan en el mismo bucket (hash function maliciosa o diseñada para el input). En Python (`dict`), el hash function es resistente a esto en práctica. Para entrevistas: menciona que el peor caso es O(n) y que el esperado es O(1) amortizado.

Espacio: O(n) donde n es el número de elementos almacenados.

---

## Patrón 1: Complemento (Two-Sum)

**Señal:** "para cada elemento, ¿existe en el array (antes o después) un elemento relacionado?"

**Jugada:** store-and-lookup. Un set de "vistos".

```python
def two_sum(nums, target):
    seen = {}          # valor -> índice
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i    # inserta DESPUÉS de buscar
    return []
```

**Por qué el orden importa:** si insertaras antes de buscar, cuando `target = 0` y `nums[0] = 0`, el elemento buscaría su complemento `0` y lo encontraría en sí mismo (self-pair). Buscar primero garantiza que solo los elementos anteriores están disponibles.

---

## Patrón 2: Frecuencia

**Señal:** "¿cuántas veces aparece cada elemento?" o "¿existe algún elemento que aparece más de k veces?"

**Jugada:** un diccionario de conteo (en Python: `Counter`).

```python
from collections import Counter

def most_common(nums, k):
    freq = Counter(nums)
    return [x for x, count in freq.items() if count > k]
```

Una sola pasada O(n), lookup O(1).

---

## Patrón 3: Clave canónica (Agrupar anagramas)

**Señal:** "agrupa elementos equivalentes bajo alguna transformación"

**Jugada:** hash map con una representación canónica como clave.

```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        key = tuple(sorted(word))   # firma canónica
        groups[key].append(word)
    return list(groups.values())
```

La decisión creativa es el diseño de la clave. El resto es mecánico.

---

## El problema del duplicado: O(1) espacio

Un array de n+1 enteros, todos entre 1 y n. Hay al menos un duplicado. Encuéntralo en O(n) tiempo y O(1) espacio, sin modificar el array.

**Por qué el hash map no sirve aquí:** O(n) espacio viola la restricción.

**Solución: Floyd's Cycle Detection**

Trata el array como una lista enlazada donde el nodo i apunta al nodo `arr[i]`. El duplicado crea un ciclo (dos nodos apuntan al mismo destino).

```python
def find_duplicate(nums):
    # Fase 1: detectar el ciclo
    slow = nums[nums[0]]
    fast = nums[nums[nums[0]]]
    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    # Fase 2: encontrar la entrada del ciclo
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

**Señal → jugada:** "duplicado en array de rango acotado, sin espacio extra" → ciclo de Floyd.

---

## Complejidad de problemas relacionados

| Problema | Complejidad óptima | Estructura |
|----------|-------------------|------------|
| Two Sum  | O(n) tiempo, O(n) espacio | Hash set |
| Three Sum | O(n²) tiempo, O(1) extra | Sort + dos punteros |
| Find duplicate (sin modificar) | O(n) tiempo, O(1) espacio | Floyd's cycle |
| Group anagrams | O(n·k log k) tiempo, O(n·k) espacio | Hash map + sort de clave |
| Top K frequent | O(n log k) tiempo, O(n) espacio | Hash + heap |

---

## Casos borde que el entrevistador querrá discutir

Para Two Sum:
- Array vacío o con un elemento → retornar []
- Múltiples soluciones válidas → ¿se pide una o todas?
- Enteros negativos → no cambia nada, el hash map maneja cualquier entero

Para Group Anagrams:
- Strings vacíos: `sorted("")` = `[]`, es una clave válida
- Un solo carácter: funciona igual
- Strings muy largos: la clave es O(k log k) donde k es la longitud

---

## Mini-ejemplo trabajado: subarray con suma k (prefix sum + hash)

"¿Cuántos subarreglos contiguos suman exactamente k?" Truco: la suma del subarreglo (i, j] = `prefix[j] − prefix[i]`. Quieres `prefix[j] − prefix[i] = k`, es decir `prefix[i] = prefix[j] − k`. Eso es **¡Two Sum sobre sumas prefijas!**

Recorre llevando la suma acumulada y un **hash contador** de las sumas prefijas vistas: en cada j, suma cuántas veces apareció `prefix − k`. Con `nums=[1,1,1]`, `k=2`: prefijos 1,2,3; cuando vas en prefix=2 buscas 0 (1 vez, el prefix vacío) → 1 subarray; en prefix=3 buscas 1 (1 vez) → otro. Total **2**. Una pasada O(n).

Es la misma jugada del complemento: "¿existe un prefijo anterior tal que la diferencia sea k?" → hash de lo visto.

**Predicción antes de seguir:** "subarreglo contiguo de suma mínima ≥ k". ¿Hash? **No** necesariamente: con elementos positivos es **sliding window** (dos punteros); reconocer cuándo el hash *no* es la respuesta vale tanto como saber usarlo.

## Errores típicos

- **Conceptual:** asumir O(1) **garantizado**; es O(1) amortizado, O(n) peor caso (colisiones).
- **Técnico:** insertar antes de consultar en Two Sum → falso emparejamiento consigo mismo (orden: buscar, luego insertar).
- **De interpretación:** usar hash cuando el enunciado dice "**contiguo**" (ventana) u "**ordenado**" (two pointers).

## Transferencia isomorfa

- **Prefix sum + hash ↔ ventana temporal acumulada:** "diferencia entre dos acumulados" es el patrón de cualquier agregado sobre el tiempo (gasto entre dos fechas, eventos entre dos instantes) — pariente de las window functions de SQL (conecta con [[arena-m2]]).
- **Hash como memoria ↔ deduplicación de eventos:** "¿ya vi esta clave?" es deduplicar diagnósticos por `patient_id` (conecta con [[arena-h11]], observation_period).
- **Clave canónica (anagramas) ↔ entity resolution:** agrupar bajo una firma canónica es el mismo gesto que mapear códigos fuente a un concepto estándar (conecta con [[arena-h12]], 'Maps to').

Moraleja de la arista: *el hash compra O(1) con memoria; el patrón del complemento reaparece sobre sumas prefijas (suma k) y sobre cohortes — el array es solo el disfraz.*

---

## Señales de reconocimiento y jugadas

| Señal | Jugada |
|-------|--------|
| "¿Existe el complemento entre los vistos?" | Hash set: store-and-lookup |
| "¿Cuántas veces aparece cada X?" | Counter / dict de frecuencias |
| "Agrupa por equivalencia bajo transformación" | Hash map con clave canónica |
| "Duplicado, sin espacio extra, rango acotado" | Floyd's cycle detection |
| "Subarray con suma k" | Hash map de sumas prefijas |

---

## Ejercicio de consolidación

Dado un array de enteros, encuentra el subarreglo contiguo de longitud mínima cuya suma sea ≥ k. ¿Qué estructura de datos usas? ¿El hash map es la herramienta correcta aquí?

*Respuesta: No. Este problema se resuelve con sliding window (dos punteros) cuando los elementos son positivos, o con deque de sumas prefijas para el caso general. El hash map no es siempre la respuesta; reconocer cuándo NO usarlo es igualmente valioso.*
