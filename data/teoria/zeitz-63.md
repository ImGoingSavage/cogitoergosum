# El complemento e inclusión-exclusión (PIE)

*Lección redactada para CogitoErgoSum a partir de la sección 6.3 de Zeitz (The Principle of Inclusion-Exclusion). Cubre el contenido completo de la unidad.*

## Contar el complemento

**La señal:** la frase «**al menos uno**…» en un conteo o probabilidad.

**La jugada:** en vez de contar lo que SÍ pasa (que se fragmenta en mil casos: exactamente uno, exactamente dos…), cuenta el **total** y réstale los que **no tienen ninguno** — el complemento suele ser UNA sola condición homogénea.

- Cadenas de n bits con **algún** 0: directo exigiría sumar por número de ceros; complemento: total 2ⁿ menos la única cadena sin ceros = **2ⁿ − 1**.
- **Ejemplo del banco:** 10 niños eligen entre 31 sabores; ¿cuántas asignaciones tienen **al menos dos niños con el mismo sabor**? Complemento = «todos con sabores distintos». Total: 31¹⁰. Todos distintos: 31·30·29⋯22 = P(31,10). Respuesta: **31¹⁰ − P(31, 10)**. Dos renglones; el conteo directo es una pesadilla.

¿Por qué funciona tan bien? Porque «al menos uno» es una **unión** gigante de casos traslapados, pero su negación —«ninguno»— es una **intersección** homogénea, casi siempre un producto directo.

## PIE con dos conjuntos

Si A y B se traslapan, |A| + |B| **sobrecuenta exactamente la intersección** (sus elementos se contaron dos veces). Repararlo es restarla:

|A ∪ B| = |A| + |B| − |A ∩ B|

**El error clásico del banco:** enteros de 1 a 100 divisibles por 2 **o** por 3: «50 + 33 = 83». Falló porque los múltiplos de 6 (divisibles por ambos) se contaron dos veces. Corrección: 50 + 33 − ⌊100/6⌋ = 50 + 33 − 16 = **67**.

## PIE con tres conjuntos y el patrón general

|A ∪ B ∪ C| = |A| + |B| + |C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|

**De dónde sale el patrón de signos:** persigue a un elemento que esté en exactamente k de los conjuntos y verifica que la fórmula lo cuente UNA vez. Si está en los tres (k=3): la primera capa lo cuenta 3 veces, la segunda lo resta 3, la tercera lo suma 1 → 3 − 3 + 1 = 1 ✓. Si está en dos: 2 − 1 + 0 = 1 ✓. Cada capa **corrige el exceso de la anterior**: sumar todo sobrecuenta los traslapes; restar pares sobre-resta los triples; sumar triples repara… La forma general alterna signos:

|A₁ ∪ ⋯ ∪ Aₙ| = Σ|Aᵢ| − Σ|Aᵢ∩Aⱼ| + Σ|Aᵢ∩Aⱼ∩Aₖ| − ⋯ ± |A₁∩⋯∩Aₙ|

(El hecho fino de que el conteo neto siempre dé 1 para cualquier k ≥ 1 es la identidad C(k,1) − C(k,2) + ⋯ = 1, que sale del binomio con (1−1)ᵏ = 0.)

## Cuándo es rentable PIE

Cuando **las intersecciones son fáciles aunque la unión sea fea**. Las situaciones de manual:

- **Divisibilidades simultáneas:** «divisible por 2 y por 5» = divisible por 10 — la intersección es un solo cálculo de piso.
- **Propiedades que se imponen por separado:** «la palabra contiene la letra A y la B» — cada condición y sus combinaciones se cuentan con la misma técnica.
- **Desarreglos** (permutaciones sin puntos fijos): Aᵢ = «el elemento i queda en su lugar»; las intersecciones son (n−k)! y PIE da la fórmula clásica n!·(1 − 1/1! + 1/2! − ⋯ ± 1/n!).

**Ejemplo combinado (complemento + PIE), del banco:** ¿cuántos enteros entre 1 y 1000 **no** son divisibles ni por 2 ni por 5? Complemento: los divisibles por 2 **o** por 5 = 500 + 200 − 100 (los de 10) = 600. Respuesta: 1000 − 600 = **400**.

## El mapa completo del conteo (hasta aquí)

Las tácticas se **apilan**, no compiten. Ante un conteo:

1. ¿Casos disjuntos naturales? → parte y suma (6.1/6.2).
2. ¿Decisiones en etapas? → multiplica; ¿sobreconteo uniforme? → divide (6.1).
3. ¿«Al menos uno»? → complemento.
4. ¿Unión de condiciones traslapadas con intersecciones fáciles? → PIE.
5. ¿Nada de lo anterior y el casework explota? → busca la codificación/biyección (6.2).

Si ni el conjunto ni su complemento son manejables, vuelve al punto 5: partir y codificar siguen disponibles.

## Disparadores

- «Al menos un/dos…» → complemento.
- «Divisible por a o por b», «contiene X o Y» → PIE.
- Conteo de «sin ninguna coincidencia» (desarreglos, todos distintos) → complemento o PIE según el lado fácil.
- Tu cuenta dio de más y sospechas traslapes → identifica QUÉ se contó dos veces; PIE es la reparación sistemática.

## Síntesis

> **Chunk mínimo:** «Al menos uno» → complemento: la unión traslapada es fea, pero «ninguno» es una intersección homogénea (sabores: 31¹⁰ − P(31,10)). PIE repara el sobreconteo de las uniones: |A∪B| = |A|+|B|−|A∩B| (error 50+33: los múltiplos de 6 iban dobles → 67); con tres, suma−pares+triple; en general signos alternados, y el porqué se ve persiguiendo a un elemento en k conjuntos: cada capa corrige el exceso de la anterior y el neto siempre es 1. Rentable cuando las intersecciones son fáciles (divisibilidades simultáneas, desarreglos: n!(1 − 1/1! + ⋯)). Mapa: disjuntos→suma; etapas→producto; sobreconteo→divide; «al menos»→complemento; traslapes→PIE; si nada → codifica.

---

*Antes del quiz: reconstruye de memoria la señal del complemento con el ejemplo de los sabores, PIE para tres conjuntos, el porqué de los signos alternados (persigue a un elemento) y la corrección del error 50+33.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Complemento e inclusion-exclusion son antidotos contra contar mal por solapes. [[arena-b1]] introduce el principio en conteo basico, [[arena-fc1]] lo aplica a urnas y emparejamientos, y [[aime-cnt]] lo vuelve una decision tactica: contar lo prohibido puede ser mas barato que contar lo permitido.
<!-- GRAFO_CONEXO_OLEADA3_END -->
