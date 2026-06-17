# Particiones y biyecciones: partir y codificar

*Lección redactada para CogitoErgoSum a partir de la sección 6.2 de Zeitz (Partitions and Bijections). Cubre el contenido completo de la unidad.*

## Las dos tácticas en tándem

Cuando el conteo directo explota, dos jugadas lo rescatan:

1. **PARTIR:** divide la colección en piezas **disjuntas que la agotan** y suma las piezas. (Es la versión estructural del «suma en casos disjuntos» de 6.1.)
2. **CODIFICAR:** construye una **biyección** entre tus objetos y las palabras de un código simple — y cuenta el código, que es fácil.

## Qué es una biyección y por qué permite contar

Una **biyección** entre dos conjuntos es una correspondencia donde **cada objeto del primero produce exactamente una palabra del segundo, y cada palabra recupera exactamente un objeto**. Si existe, los dos conjuntos tienen el mismo tamaño — así que puedes contar el que sea fácil.

**La verificación obligatoria (las dos direcciones):**

- **No pierde información:** objetos distintos → palabras distintas (si dos objetos dieran la misma palabra, el código cuenta de menos).
- **No inventa:** toda palabra del código proviene de algún objeto (si hay palabras huérfanas, el código cuenta de más).

Ahí mueren los conteos falsos: una «codificación» que no se verifica en ambas direcciones no es biyección, es deseo.

## El ejemplo canónico: subconjuntos como cadenas binarias

¿Cuántos subconjuntos tiene un conjunto de n elementos? Codifica: a cada subconjunto asígnale la cadena de n símbolos sí/no respondiendo «¿está el elemento i?». Cada subconjunto da una única cadena; cada cadena define un único subconjunto. Biyección ⇒ tantos subconjuntos como cadenas: **2ⁿ** — sin sumar ni una sola C(n, k). (Compara con sumar C(n,0)+⋯+C(n,n): el código se saltó todo ese trabajo.)

## Barras y estrellas (bolas en urnas)

**Problema patrón:** repartir k bolas **idénticas** en n urnas **distinguibles**. Equivalente: contar las soluciones enteras de

x₁ + x₂ + ⋯ + xₙ = k, con todas las xᵢ ≥ 0.

**Codificación:** escribe cada reparto como una cadena de **k estrellas** (las bolas) y **n − 1 barras** (las paredes entre urnas consecutivas). Ejemplo con n = 3, k = 4: la cadena ★★|★|★ significa x₁=2, x₂=1, x₃=1. Cada reparto da una única cadena (escribe las bolas de cada urna y separa con barras); cada cadena recupera un único reparto (lee cuántas estrellas hay entre barras — puede ser cero). Biyección ⇒ tantos repartos como cadenas, y las cadenas son elecciones de posición para las barras entre n−1+k lugares:

**C(n + k − 1, n − 1)**

Esta fórmula no se memoriza: se **rededuce** con la imagen de estrellas y barras cada vez (30 segundos).

## Composiciones: el truco de los espacios

**Problema del banco:** ¿de cuántas maneras se escribe 8 como suma **ordenada** de enteros positivos (2+6 ≠ 6+2)? — las *composiciones* de 8.

**Codificación:** imagina 8 unos en fila: 1 1 1 1 1 1 1 1. Entre ellos hay **7 espacios**; en cada espacio decides **cortar o no cortar**. Cada patrón de cortes da una única suma ordenada (los bloques entre cortes son los sumandos) y cada suma ordenada da un único patrón. Biyección con las cadenas de 7 decisiones binarias ⇒ **2⁷ = 128**. En general, n tiene **2ⁿ⁻¹** composiciones.

Nota la familia: subconjuntos, repartos, composiciones — tres problemas distintos, **el mismo movimiento**: encontrar la secuencia de decisiones que determina por completo cada objeto, y contar las secuencias.

## Manejo de información: contar lo que determina al objeto

El principio detrás de toda codificación: pregúntate **qué información mínima determina por completo cada objeto** que cuentas. Esa información ES el código. Si un objeto queda determinado por r decisiones binarias independientes, hay 2ʳ; si por la posición de unas barras, es un C(·,·); si por una palabra con letras repetidas, es Mississippi (6.1). El conteo se reduce a inventariar la información.

## Disparadores

- El **casework se multiplica sin control** → alto: ¿qué secuencia de decisiones determina cada objeto? Codifícala.
- Bolas idénticas en cajas distintas / soluciones de x₁+⋯+xₙ = k → estrellas y barras.
- Sumas **ordenadas** de enteros positivos → cortes en los espacios: 2ⁿ⁻¹.
- «¿Cuántos subconjuntos / opciones binarias?» → cadenas sí/no.
- Cualquier código que propongas → verifica las DOS direcciones antes de confiar en la cuenta.

## Síntesis

> **Chunk mínimo:** Cuando el casework explota: PARTE (piezas disjuntas que agotan, y suma) o CODIFICA (biyección con un código fácil de contar). Biyección exige DOS verificaciones: no pierde información (objetos distintos → palabras distintas) y no inventa (toda palabra viene de un objeto). Subconjuntos = cadenas sí/no ⇒ 2ⁿ. Estrellas y barras: x₁+⋯+xₙ = k con xᵢ ≥ 0 ⟺ cadenas de k estrellas y n−1 barras ⇒ C(n+k−1, n−1) — se rededuce, no se memoriza. Composiciones de n (sumas ordenadas): cortar o no en los n−1 espacios ⇒ 2ⁿ⁻¹. El principio: identifica la información mínima que determina cada objeto — esa información ES el código.

---

*Antes del quiz: reconstruye de memoria qué es una biyección y sus dos verificaciones, la deducción completa de estrellas y barras y la codificación de las composiciones de n.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Particiones y biyecciones muestran que contar es elegir una representacion donde los objetos se vuelven comparables. [[arena-b1]] da el lenguaje probabilistico, [[arena-p2]] lo extiende a estructuras discretas, y [[aime-cnt]] lo exige cuando una cuenta directa es torpe pero una correspondencia limpia resuelve el problema.
<!-- GRAFO_CONEXO_OLEADA3_END -->
