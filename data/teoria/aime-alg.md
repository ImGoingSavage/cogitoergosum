# AIME · Álgebra: sucesiones, Vieta y sustitución

*Lección redactada para CogitoErgoSum a partir de problemas de álgebra del AIME (American Invitational Mathematics Examination). Cubre el contenido completo de la unidad.*

## El contexto del AIME

El AIME es un examen de competición estadounidense de 15 problemas, con respuesta entera entre 0 y 999. Esa restricción no es accidental: **los enunciados están diseñados para colapsar en un entero pequeño y exacto**. Si tu cuenta da un número fuera de rango, o una fracción donde no debería, hay un error —la restricción es una herramienta de verificación gratuita.

Los problemas de álgebra del AIME tienden a tener estructuras de tres tipos: **bases posicionales**, **Vieta con acotación**, y **sistemas simétricos**. Los veremos uno por uno.

## Representación en bases

Algunos problemas definen una sucesión como «sumas de potencias distintas de b» (p. ej. potencias de 3 escogidas sin repetir). La clave: esos términos están en biyección con los subconjuntos de {b⁰, b¹, b², …}, es decir, con los números en **base 2** leídos en base b.

Protocolo: escribe el índice n en binario. Los 1's en la representación binaria marcan qué potencias de b aparecen en el n-ésimo término. Por ejemplo, para potencias de 3: el término 6.º (110₂) es 3² + 3¹ = 12.

Esta traducción convierte una sucesión aparentemente complicada en una función aritmética simple del índice.

## Vieta con acotación

Cuando un polinomio con **coeficientes dados** tiene raíces **enteras**, las fórmulas de Vieta (suma, pares, producto) se convierten en ecuaciones diofánticas con las raíces como incógnitas. El número de soluciones candidatas es finito porque:

- La suma r₁ + r₂ + ⋯ + rₙ está fijada por −aₙ₋₁/aₙ.
- El producto r₁r₂⋯rₙ está fijado por (−1)ⁿa₀/aₙ.
- Para raíces enteras, la búsqueda se reduce a los divisores del producto fijo.

Ejemplo con tres raíces enteras r, s, t con r+s+t=0 y rs+rt+st=k: sustituye t=−r−s, obtienes r²+rs+s²=−k, una ecuación en dos variables —fácil de explorar acotando por |r|, |s|.

## Sistemas simétricos

Cuando el sistema es simétrico en x e y (o en más variables), la sustitución **s = x+y, p = xy** reduce dos ecuaciones en x,y a dos ecuaciones en s,p, y x,y son las raíces de t² − st + p = 0. Este es el mismo Vieta de siempre, visto al revés.

Generalización: si tienes expresiones tipo xⁿ+yⁿ, usa las identidades de Newton (con las funciones simétricas elementales e₁=s, e₂=p) para calcularlas sin hallar x,y explícitamente.

## Radicales y extraneidad

Al **elevar al cuadrado** para eliminar raíces cuadradas, la implicación va en un solo sentido:

> P ⟹ P² (pero P² no implica P; puede implicar −P).

Esto introduce **soluciones extrañas** que satisfacen la ecuación al cuadrado pero no la original. Protocolo obligatorio: verificar toda solución candidata en la ecuación original. Una solución extraña en el AIME produce una respuesta fuera del rango 0–999 o que no satisface una restricción explícita del enunciado —la restricción de entero actúa como filtro.

## El número final es un entero entre 0 y 999

Esta restricción tiene tres usos prácticos:

1. **Verificación**: si tu respuesta es una fracción o un número negativo, busca el error.
2. **Guía de estructura**: el enunciado está diseñado para que todo se simplifique a algo exacto y pequeño. Si el cálculo se complica, generalmente hay una simplificación que no has visto.
3. **Forma de reporte**: a veces la respuesta pedida no es el número en sí, sino «m+n» donde la fracción exacta es m/n, o «a+b» donde el resultado es a+b√c con c libre de cuadrados. Lee con cuidado qué número hay que reportar.

## Disparadores

- «Sucesión de sumas de potencias distintas de b» → indexar por números en base 2 leídos en base b.
- «Polinomio con coeficientes dados y raíces enteras» → Vieta + acotación por divisores del producto.
- «Sistema simétrico en x, y» → sustitución s=x+y, p=xy; x,y son raíces de t²−st+p=0.
- «Ecuación con raíces cuadradas» → elevar al cuadrado, luego verificar en la original.

## Síntesis

> **Chunk mínimo:** AIME respuesta 0–999: si sale de rango, hay un error; la restricción es un filtro y una pista de que la estructura colapsa a algo exacto. Bases: índice n en binario → qué potencias de b suman el n-ésimo término. Vieta + acotación: coeficientes enteros + raíces enteras → explorar divisores del producto (o de la suma). Sistemas simétricos: s=x+y, p=xy; las variables son raíces de t²−st+p=0. Radicales: elevar al cuadrado introduce extrañas → verificar en la ecuación original. La forma de reporte (m+n para m/n, a+b para a+b√c) es parte del enunciado.

---

*Antes del quiz: reconstruye de memoria la traducción base-2→base-b para sucesiones de potencias, el protocolo Vieta+acotación, la sustitución s,p para sistemas simétricos y por qué elevar al cuadrado requiere verificación.*
