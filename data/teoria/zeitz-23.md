# Métodos de argumento: deducción, contradicción e inducción

*Lección redactada para CogitoErgoSum a partir de la sección 2.3 de Zeitz (Methods of Argument). Cubre el contenido completo de la unidad.*

## De la idea al argumento

Las estrategias te dan la idea; esta sección te da las **formas válidas de convertir la idea en demostración**. Tres métodos cubren casi todo: argumento directo (deducción), contradicción e inducción.

## Deducción y un mínimo de lógica simbólica

El argumento directo encadena implicaciones: A ⇒ B ⇒ C. Conviene tener afilado el vocabulario:

- «Si A entonces B» (A ⇒ B) **no** equivale a su recíproca (B ⇒ A). Confundirlas es el error lógico más común.
- Sí equivale a su **contrapositiva**: «si no B, entonces no A». Son lógicamente idénticas — y a menudo la contrapositiva es **más manejable**: «si n² es par, n es par» se vuelve transparente como «si n es impar, n² es impar» (impar × impar = impar, fin).
- «A si y solo si B» exige demostrar **ambas** direcciones.

**Reflejo útil:** cuando una implicación se resista de frente, escribe su contrapositiva y mírala un minuto.

## Argumento por contradicción (reductio ad absurdum)

**Estructura:** supón que la tesis es falsa; deduce algo absurdo; concluye que la tesis es verdadera.

**Cuándo brilla:** con tesis **negativas** — «no existe», «es imposible», «es irracional», «no puede ser». La razón es concreta: la tesis negativa no te da nada que manipular («no existe tal x»… ¿y ahora qué?). Al negarla, **te regala un objeto concreto que atacar**: «supongamos que SÍ existe tal x» — y ahora x tiene propiedades, ecuaciones, restricciones que explotar hasta que algo truene.

**Ejemplo canónico — √2 es irracional:** supón √2 = p/q con la fracción **en términos mínimos**. Entonces p² = 2q², así que p² es par, así que p es par (contrapositiva de arriba): p = 2k. Sustituyendo, 4k² = 2q², o sea q² = 2k², así que q también es par. Pero entonces p y q comparten el factor 2 — contradice «términos mínimos». Absurdo: √2 no es racional. Nota cómo *cada paso* usó al objeto regalado (la fracción p/q).

## Inducción matemática

**Las dos piezas, ambas obligatorias:**

1. **Caso base:** verificar la afirmación para el primer valor (n = 1, o donde arranque).
2. **Paso inductivo:** suponer la afirmación para n (la **hipótesis inductiva**) y demostrarla para n + 1.

La imagen: fichas de dominó. El caso base tumba la primera; el paso inductivo garantiza que cada ficha tumba a la siguiente.

**El error más común al ejecutarla:** escribir el paso inductivo **sin usar la hipótesis**. Si tu argumento para n + 1 jamás invocó la suposición sobre n, una de dos: o tienes un argumento directo (y la inducción sobra), o tu paso está mal y no demostraste nada. Verifícalo siempre: señala con el dedo *dónde* usaste la hipótesis.

**Ejemplo mínimo:** 1 + 2 + ⋯ + n = n(n+1)/2. Base: n = 1, ambos lados valen 1. Paso: asume la fórmula para n; entonces 1 + ⋯ + n + (n+1) = n(n+1)/2 + (n+1) = (n+1)(n+2)/2 — que es la fórmula para n + 1. (La hipótesis se usó en la primera igualdad: ahí está el dedo.)

### Inducción fuerte

A veces para llegar a n + 1 no basta el caso n: necesitas **todos los anteriores**. La inducción fuerte autoriza asumir la afirmación para *todo* k ≤ n. Ejemplo: «todo entero ≥ 2 es producto de primos» — si n + 1 no es primo, se parte como a·b con a, b ≤ n, y la hipótesis fuerte cubre a ambos factores (el caso n solo, no serviría de nada). Las recurrencias que miran varios términos atrás (Fibonacci) también la piden.

## El caballo monocolor: encuentra el error

Argumento famoso (falso): «Todo grupo de n caballos es monocolor. Base: n = 1, obvio. Paso: en un grupo de n+1, quita un caballo — los n restantes son monocolor por hipótesis; reincorpóralo y quita otro — también monocolor; luego los n+1 comparten color.»

**Dónde falla exactamente:** el paso necesita que los dos subgrupos de n caballos **se traslapen** (un caballo común transmite el color de un subgrupo al otro). Eso es cierto para n ≥ 2… pero **falla justo en el paso de n = 1 a n = 2**: los dos subgrupos de 1 caballo son disjuntos y nada conecta sus colores. Una sola junta rota derrumba toda la cadena de dominós. Moraleja: revisa el paso inductivo *en sus valores pequeños*, donde suele esconderse la grieta.

## Escribir con limpieza no es estética

Los huecos lógicos se esconden en la prosa borrosa («claramente», «es fácil ver», «y así sucesivamente»). Escribir el argumento completo, con cada implicación explícita, es el detector de errores más barato que existe. Si no puedes escribirlo limpio, todavía no lo tienes.

## Disparadores

- «Demuestra que NO existe / es imposible / es irracional» → contradicción: niega y ataca el objeto regalado.
- «Demuestra que para todo n ≥ 1…» → considera **inducción** y **argumento directo**; pregunta rápida que decide: *¿el caso n + 1 se construye naturalmente desde el caso n?* Si sí, inducción; si la afirmación se prueba igual de fácil para n arbitrario, directo.
- Implicación dura de frente → contrapositiva.
- Paso inductivo que no usó la hipótesis → alarma roja: revisa.

## Síntesis

> **Chunk mínimo:** Tres formas de argumento. **Deducción**: A ⇒ B equivale a su contrapositiva (¬B ⇒ ¬A) — úsala cuando la implicación se resista — y NO a su recíproca; «si y solo si» exige ambas direcciones. **Contradicción**: brilla con tesis negativas porque negar la tesis te REGALA un objeto concreto que atacar (√2 = p/q en términos mínimos → p y q ambos pares → absurdo). **Inducción**: caso base + paso inductivo, y el error clásico es no usar la hipótesis (señala con el dedo dónde); la fuerte asume todo k ≤ n (factorización en primos, Fibonacci); los caballos monocolor truenan exactamente en n = 1 → 2 (subgrupos disjuntos): revisa el paso en valores pequeños.

---

*Antes del quiz: reconstruye de memoria qué regala exactamente la contradicción con tesis negativas, las dos piezas de la inducción con su error típico, y dónde truena el argumento de los caballos.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Contradiccion e induccion son motores de prueba que reaparecen en [[engel-ind]] como induccion fuerte y descenso, y en [[arena-cc3]] como razonamiento recursivo sobre subproblemas. En entrevistas, [[arena-q13]] usa la misma estructura cuando un juego o una logica solo cede al fortalecer la hipotesis.
<!-- GRAFO_CONEXO_OLEADA3_END -->
