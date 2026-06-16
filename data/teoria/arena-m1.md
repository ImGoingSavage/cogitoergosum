# Hashing, frecuencia y memoria comprada

## De qué trata esta lección (y qué sabrás hacer al final)

Si tuvieras que apostar a una sola estructura de datos para una entrevista de código, apostarías a la **tabla hash**. Esta lección la lleva más allá del "qué es" hacia el **cuándo** y el **cómo razonar con ella**: la idea de "memoria comprada" (pagar espacio para comprar tiempo), los tres patrones que cubren la mayoría de los problemas (complemento, frecuencia, clave canónica), y —crucial— **cuándo el hash NO es la respuesta**, porque reconocer eso vale tanto como saber usarlo.

Al terminar podrás: (1) dar un análisis de complejidad honesto ($O(1)$ esperado, $O(n)$ peor caso) y defenderlo en la entrevista; (2) aplicar el patrón del complemento, el contador de frecuencias y la clave canónica; (3) resolver "subarreglo que suma $k$" reconociéndolo como Two Sum sobre sumas prefijas; y (4) saber cuándo cambiar a ventana deslizante o a detección de ciclos (Floyd) porque la restricción de espacio prohíbe el hash. Cada patrón entra por su señal y un ejemplo trabajado. Comparte raíz con [[arena-cc1]] (arrays) pero profundiza en los patrones de hashing.

---

## El principio central: memoria comprada

La frase que conviene grabar: una tabla hash es **memoria comprada**. Pagas $O(n)$ de espacio una vez para comprar $O(1)$ de tiempo en cada consulta futura. Toda la habilidad consiste en detectar la señal: en cuanto un problema pregunta *"¿ya vi este elemento?"*, *"¿existe su complemento?"* o *"¿cuántas veces aparece?"*, el hash map es la jugada. Es la herramienta que convierte un bucle anidado $O(n^2)$ ("para cada elemento, busca su pareja recorriendo el resto") en una sola pasada $O(n)$ ("para cada elemento, pregunta al índice si la pareja ya pasó").

## Análisis de complejidad honesto

| Operación | Caso esperado | Peor caso |
|-----------|--------------|-----------|
| Insert    | $O(1)$       | $O(n)$    |
| Lookup    | $O(1)$       | $O(n)$    |
| Delete    | $O(1)$       | $O(n)$    |

El peor caso $O(n)$ ocurre cuando **todas** las claves colisionan en el mismo bucket —un input adversarial o una función hash mala—. En la práctica, las implementaciones serias (como el `dict` de Python) usan funciones resistentes a esto, así que el caso esperado domina. La frase que el entrevistador quiere oír: *"$O(1)$ amortizado esperado, $O(n)$ en el peor caso por colisiones"*. Decir solo "$O(1)$" sin el matiz es un error de rigor. El espacio es $O(n)$ en el número de elementos guardados.

## Patrón 1: el complemento (Two Sum)

**Señal:** "para cada elemento, ¿existe en el arreglo uno relacionado?". **Jugada:** guarda lo visto y consulta el complemento.

```python
def two_sum(nums, target):
    seen = {}                      # valor -> índice
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i                # inserta DESPUÉS de buscar
    return []
```

La intuición: en vez de preguntar "¿hay un par que sume `target`?" (cuadrático), reformulas a "para *este* `x`, ¿pasó antes su complemento `target − x`?" (lineal). El orden —**buscar antes de insertar**— evita el auto-emparejamiento: con `target=0` y `nums[0]=0`, insertar primero haría que el `0` se encontrara a sí mismo.

## Patrón 2: frecuencia

**Señal:** "¿cuántas veces aparece cada elemento?" o "¿cuál aparece más de $k$ veces?". **Jugada:** un diccionario contador (en Python, `Counter`).

```python
from collections import Counter

def aparecen_mas_de(nums, k):
    freq = Counter(nums)
    return [x for x, c in freq.items() if c > k]
```

Una pasada $O(n)$ para contar, lookup $O(1)$. Es el hash en su forma más directa: el bucket *es* la cuenta.

## Patrón 3: clave canónica (agrupar anagramas)

**Señal:** "agrupa elementos equivalentes bajo alguna transformación". **Jugada:** un hash map cuya clave es una **representación canónica** —una firma que es idéntica para todos los equivalentes—.

```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        key = tuple(sorted(word))   # firma: las letras ordenadas
        groups[key].append(word)
    return list(groups.values())
```

`"eat"` y `"tea"` comparten la firma `('a','e','t')`, así que caen en el mismo grupo. Toda la creatividad está en **diseñar la clave**; el resto es mecánico. Cuesta $O(n\cdot k\log k)$ ($k$ = longitud de palabra, por el ordenamiento de cada firma).

## Cuándo el hash NO sirve: el duplicado en $O(1)$ espacio

Un giro revelador: un arreglo de $n+1$ enteros, todos entre $1$ y $n$, tiene al menos un duplicado. Hállalo en $O(n)$ tiempo **y $O(1)$ espacio**, sin modificar el arreglo. El hash map resolvería el tiempo pero **viola el espacio** ($O(n)$). Hay que cambiar de herramienta por completo.

La idea ingeniosa: trata el arreglo como una lista enlazada donde el nodo $i$ "apunta a" `nums[i]`. Como hay un valor repetido, dos nodos apuntan al mismo destino → se forma un **ciclo**. Detectarlo es la **tortuga y la liebre de Floyd**:

```python
def find_duplicate(nums):
    slow = fast = nums[0]
    # Fase 1: la liebre alcanza a la tortuga dentro del ciclo
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast: break
    # Fase 2: dos punteros a igual velocidad hallan la entrada del ciclo
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

La entrada del ciclo es el número duplicado. Es $O(n)$ tiempo, $O(1)$ espacio. **Señal → jugada:** "duplicado en rango acotado, sin espacio extra" → ciclo de Floyd, no hash.

> **Predicción antes de seguir:** la restricción "$O(1)$ espacio" es la que mata al hash. ¿Por qué los entrevistadores la ponen? Porque distingue a quien *memoriza* "hash para duplicados" de quien *razona* sobre las restricciones y reconoce una estructura oculta (el ciclo). Lee siempre las restricciones de espacio antes de elegir la herramienta.

## Complejidades de problemas vecinos

| Problema | Óptimo | Estructura |
|----------|--------|------------|
| Two Sum | $O(n)$ tiempo, $O(n)$ espacio | hash set |
| Three Sum | $O(n^2)$ tiempo, $O(1)$ extra | sort + dos punteros |
| Find duplicate (sin modificar) | $O(n)$ tiempo, $O(1)$ espacio | ciclo de Floyd |
| Group anagrams | $O(n\,k\log k)$ | hash + sort de clave |
| Top-K frequent | $O(n\log k)$ | hash + heap de tamaño $k$ |

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
