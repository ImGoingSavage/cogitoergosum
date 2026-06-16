# Arrays, cadenas y tablas hash

## De qué trata esta lección (y qué sabrás hacer al final)

Más de la mitad de los problemas de "coding" de una entrevista MAANG son, en el fondo, problemas de **arrays y cadenas** disfrazados. La buena noticia: casi todos se resuelven con un puñado pequeño de herramientas, y la habilidad de élite no es memorizarlas sino **reconocer cuál pide el enunciado**. Esta lección las construye desde cero —la **tabla hash** (memoria comprada para consultar en $O(1)$), la **ventana deslizante** (para lo contiguo), los **dos punteros** (para lo ordenado)— y media docena de patrones que aparecen una y otra vez.

Al terminar podrás: (1) elegir entre hash, ventana y punteros leyendo una palabra del enunciado ("¿existe?" / "contiguo" / "ordenado"); (2) escribir Two Sum, sliding window y merge intervals con su complejidad justificada; (3) entender por qué el $O(1)$ de un hash es *amortizado* y cuándo se rompe; y (4) reconocer la misma estructura profunda fuera de los arrays (SQL, cohortes, streams). Cada técnica entra por su intuición y un mini-ejemplo trabajado a mano.

---

## La tabla hash: la idea de "memoria comprada"

Empieza por la herramienta que más entrevistas resuelve, y por su intuición antes que su mecánica. Imagina que te preguntan repetidamente "¿está el número 7 en esta lista?". Con un array crudo, cada pregunta te obliga a **re-escanear** todo: $O(n)$ por consulta. Una **tabla hash** cambia ese trabajo repetido por una inversión única de memoria: guardas lo que ves en un índice y respondes futuras preguntas en **tiempo constante**. Es la diferencia entre releer la guía telefónica entera cada vez (array) y tener un índice alfabético que te lleva directo a la página (hash). La regla mental: cada vez que un problema pregunta *"¿ya vi esto?"*, *"¿cuántas veces aparece?"* o *"¿existe su pareja?"*, la respuesta casi siempre es **guarda lo visto en un mapa**.

Cómo funciona por dentro: una función *hash* convierte una clave en un índice de un arreglo de **buckets**, y ahí se guarda el valor. Operaciones —insertar, buscar, borrar— en **$O(1)$ promedio**. El "promedio" es clave (volvemos a él abajo).

- **Factor de carga** $\alpha=n/m$ (elementos $n$ entre buckets $m$): mientras $\alpha$ se mantenga bajo (típicamente $<0.75$), el rendimiento es estable; al pasarse, la tabla **redimensiona** (duplica buckets y rehashea).
- **Colisiones** (dos claves al mismo bucket) se resuelven con **encadenamiento** (cada bucket es una lista; lookup $O(1+\alpha)$) o **direccionamiento abierto** (si el slot está ocupado, prueba el siguiente; sensible a aglomeraciones).

> **Predicción antes de seguir:** ¿la tabla hash garantiza $O(1)$ *siempre*? Respuesta: **no**. Es $O(1)$ **amortizado/promedio**; un adversario que fuerce a todas las claves al mismo bucket lo degrada a $O(n)$ por operación. En la entrevista, dilo así: "$O(1)$ promedio, $O(n)$ peor caso". Esa honestidad puntúa.

---

## Two Sum: el patrón canónico del hash map

El problema: dado un arreglo `nums` y un `target`, devuelve los índices $i,j$ tales que `nums[i] + nums[j] = target`. La solución ingenua prueba todos los pares: $O(n^2)$. El salto de calidad: para cada elemento $x$, lo que necesitas es saber si su **complemento** `target − x` ya apareció — y eso es justo una consulta de hash en $O(1)$.

```
funcion twoSum(nums, target):
    visto = {}                      # mapa valor -> índice
    para i, x en nums:
        c = target - x
        si c en visto:
            retorna (visto[c], i)   # ¡par encontrado!
        visto[x] = i                # recuerda este valor
    retorna ninguno
```

Recorres el arreglo **una vez** y cada consulta es $O(1)$, así que el total es $O(n)$ tiempo y $O(n)$ espacio. La sutileza que cazan los entrevistadores: **consulta antes de insertar**. Si insertaras `x` antes de buscar su complemento, en `nums=[3,3]` con `target=6` te emparejarías contigo mismo. Generalización: *3-sum* fija un elemento y reduce el resto a un Two Sum; *4-sum* anida dos niveles para $O(n^2)$ con hash.

---

## Ventana deslizante: para subarreglos contiguos

La señal inequívoca: el enunciado pide algo sobre un **subarreglo o subcadena contigua** ("la suma máxima de $k$ elementos seguidos", "la subcadena más larga sin repetir"). La idea: mantén una ventana $[\text{left}, \text{right}]$ y **actualízala en $O(1)$** al moverla, en vez de recalcular desde cero.

**Ventana fija (tamaño $k$)** — suma máxima de un subarreglo de longitud $k$. Calcula la suma de los primeros $k$, luego desliza restando el que sale y sumando el que entra:

```
suma = sum(arr[0..k-1]);  mejor = suma
para right en [k .. n-1]:
    suma += arr[right] - arr[right-k]   # entra uno, sale uno: O(1)
    mejor = max(mejor, suma)
```

$O(n)$ tiempo, $O(1)$ espacio. El truco es que cada paso toca solo **dos** elementos, no $k$.

**Ventana variable (condición)** — la subcadena más larga sin caracteres repetidos. Aquí `right` avanza siempre; `left` solo avanza **cuando se viola** la condición. Un mapa de frecuencias detecta el repetido:

```
freq = {};  left = 0;  mejor = 0
para right en [0 .. n-1]:
    freq[s[right]] += 1
    mientras freq[s[right]] > 1:     # hay un repetido: encoge por la izquierda
        freq[s[left]] -= 1;  left += 1
    mejor = max(mejor, right - left + 1)
```

Cada índice entra y sale de la ventana a lo sumo una vez → $O(n)$ amortizado; espacio $O(\min(n, |\text{alfabeto}|))$.

---

## Dos punteros: para lo ordenado

Cuando el arreglo está **ordenado**, el orden mismo es estructura gratis que vuelve innecesario el hash. Para hallar un par con suma `target`, coloca un puntero en cada extremo y deja que la comparación te diga hacia dónde moverte:

```
left = 0;  right = n-1
mientras left < right:
    s = nums[left] + nums[right]
    si s == target: retorna (left, right)
    si s < target:  left += 1      # necesito más: sube el menor
    sino:           right -= 1      # necesito menos: baja el mayor
```

$O(n)$ tiempo, $O(1)$ espacio — mejor que el hash en memoria, *porque aprovechaste el orden*. La misma idea, en su versión de **partición**, resuelve el *Dutch National Flag* (ordenar un arreglo de `{0,1,2}` en una sola pasada con tres punteros `low/mid/high`): un patrón clásico de partición in-place en $O(n)$.

> **Predicción antes de seguir:** te dan un arreglo **ordenado** y te piden pares con suma dada. ¿Hash o dos punteros? Respuesta: **dos punteros** — el hash funcionaría pero gasta $O(n)$ de memoria para reconstruir un orden que ya tienes gratis. Usar hash aquí es la señal de que no leíste la palabra "ordenado".

---

## Complejidad amortizada de los arrays

| Operación | Array dinámico | Array fijo |
|-----------|---------------|-----------|
| Acceso por índice | $O(1)$ | $O(1)$ |
| Insertar al final | $O(1)$ amortizado | — |
| Insertar en medio | $O(n)$ | $O(n)$ |
| Búsqueda lineal | $O(n)$ | $O(n)$ |
| Búsqueda binaria (ordenado) | $O(\log n)$ | $O(\log n)$ |

El renglón sutil es "insertar al final, $O(1)$ amortizado". Un array dinámico **duplica su capacidad** cuando se llena: esa copia puntual cuesta $O(n)$, pero ocurre cada vez menos seguido (al doble, al cuádruple…). Repartido sobre $n$ inserciones, el coste por inserción promedia $O(1)$. Es el mismo razonamiento "amortizado" del rehasheo de la tabla hash: un trabajo caro pero raro se diluye.

---

## Merge intervals: ordenar primero, fundir después

Dado un conjunto de intervalos $[s_i, e_i]$, fusiona los que se solapan. La clave es que el solapamiento solo se puede razonar localmente **si los intervalos vienen ordenados por inicio**:

```
ordena intervalos por inicio s        # O(n log n) — domina el costo
res = [primer intervalo]
para cada [s, e] en el resto:
    si s <= res.ultimo.fin:           # solapa: extiende el fin
        res.ultimo.fin = max(res.ultimo.fin, e)
    sino:                             # disjunto: empieza uno nuevo
        res.append([s, e])
```

El **invariante** que lo hace correcto: lo ya guardado en `res` está siempre disjunto y ordenado. Ejemplo trabajado:

```
entrada: (1,3) (2,6) (8,10) (15,18)
(2,6) solapa con (1,3)  -> funde a (1,6)
(8,10) no solapa        -> nuevo
(15,18) no solapa       -> nuevo
salida:  (1,6) (8,10) (15,18)
```

El costo lo domina el ordenamiento, $O(n\log n)$; la pasada de fusión es $O(n)$.

---

## Tres patrones más que conviene reconocer

- **Producto de todos menos el propio (sin división):** haz una pasada de izquierda acumulando el prefijo de productos en `result`, y otra de derecha acumulando el sufijo y multiplicándolo en sitio. $O(n)$ tiempo, $O(1)$ espacio extra. La idea: `result[i] = (producto a su izquierda) × (producto a su derecha)`, y cada lado se acumula incrementalmente.
- **Rotar $k$ a la derecha con tres reversos:** revierte todo el arreglo, luego los primeros $k$, luego los últimos $n-k$. Mágicamente queda rotado, en $O(n)$ tiempo y $O(1)$ espacio. (Verifícalo a mano con `[1,2,3,4,5]`, $k=2$.)
- **Rabin-Karp (hash de cadenas):** para buscar un patrón de largo $m$ en un texto de largo $n$, un **hash rodante** actualiza el hash de la ventana en $O(1)$ al avanzar una posición (resta el carácter que sale, suma el que entra), dando $O(n+m)$ esperado. Es la versión-cadena de la ventana deslizante, y la base de detección de subcadenas duplicadas.

---

## Mini-ejemplo trabajado: Two Sum paso a paso

`nums = [2, 7, 11, 15]`, `target = 9`. Recorremos manteniendo el mapa `visto`:

- `i=0, x=2`: complemento `9−2=7`, no está en `visto`. Guardamos `visto[2]=0`.
- `i=1, x=7`: complemento `9−7=2`, **sí está** (`visto[2]=0`). Devolvemos `(0, 1)`. ✓

Una sola pasada, cada consulta $O(1)$. Compara con la fuerza bruta: probar `(2,7),(2,11),(2,15),(7,11)…` es $O(n^2)$. El hash convirtió "buscar la pareja" de $O(n)$ a $O(1)$, y eso bajó el problema entero un orden de magnitud.

**Predicción antes de seguir:** ¿por qué insertar *después* de consultar y no antes? Porque si guardas `visto[x]=i` antes de buscar `target−x`, en `nums=[3,3]`, `target=6` encontrarías el `3` que acabas de meter y devolverías `(0,0)` —un índice consigo mismo, inválido—. Consultar primero garantiza que el complemento sea un elemento **anterior**, distinto.

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
- **Two Sum ↔ emparejar exposición-control:** "¿existe para este paciente expuesto uno de control con el mismo propensity score?" es buscar el *complemento* en un índice — el mismo patrón del complemento `target − x`, ahora sobre cohortes (conecta con [[arena-h20]] de Health AI).
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
