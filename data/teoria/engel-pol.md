# Polinomios: factor, Vieta y valores especiales

*Lección redactada para CogitoErgoSum a partir del capítulo de polinomios de Engel (Problem-Solving Strategies). Cubre el contenido completo de la unidad.*

## La idea central

Un polinomio se puede estudiar por sus **raíces** (factor, Vieta) o por sus **valores** (identidades, sustituciones especiales). Los problemas de competición suelen regalar información en uno de los dos lenguajes; saber traducir entre ellos es la habilidad central.

## Teorema del factor y principio de identidad

**Teorema del factor**: P(a) = 0 si y solo si (x − a) divide a P(x). Todo polinomio de grado n tiene a lo sumo n raíces (sobre un cuerpo sin divisores de cero).

**Principio de identidad** (el corolario más poderoso): si dos polinomios de grado ≤ n coinciden en n+1 puntos, son idénticos. Aplicación inmediata: para demostrar que P ≡ Q, basta exhibir n+1 puntos donde coinciden, donde n = max(grado P, grado Q). En la práctica, «fabricas» el polinomio P(x) − Q(x) y demuestras que tiene n+1 raíces → es el polinomio cero → P = Q.

## Fórmulas de Vieta

Para P(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ⋯ + a₀ con raíces r₁, …, rₙ (contando multiplicidades sobre ℂ):

| Función simétrica | Expresión en términos de coeficientes |
|---|---|
| r₁ + r₂ + ⋯ + rₙ | −aₙ₋₁ / aₙ |
| Σᵢ<ⱼ rᵢrⱼ | aₙ₋₂ / aₙ |
| ⋮ | ⋮ |
| r₁r₂⋯rₙ | (−1)ⁿ a₀ / aₙ |

Las funciones simétricas elementales de las raíces son **invariantes bajo permutarlas** —por eso quedan codificadas en los coeficientes. Vieta convierte «qué valen las raíces» en álgebra sin conocer las raíces explícitamente.

## Evaluaciones especiales como filtros

- **P(0)** = término independiente.
- **P(1)** = suma de todos los coeficientes.
- **P(−1)** = suma alternada de coeficientes (paridad).
- **P en raíces de la unidad** = filtro de coeficientes: para sumar coeficientes en posiciones con residuo k módulo m, promedia P evaluado en las m-ésimas raíces de la unidad ponderadas por la fase adecuada.

Ejemplo: la suma de coeficientes en posiciones pares de P(x) = P(1)/2 + P(−1)/2 (el filtro de paridad con las raíces cuadradas de la unidad 1 y −1).

## Coeficientes enteros y divisibilidad

**Teorema de la raíz racional**: si P tiene coeficientes enteros y la fracción p/q (en mínimos términos) es raíz, entonces p | a₀ y q | aₙ. Acota las candidatas y reduce la búsqueda a una lista finita.

**Divisibilidad por (a − b)**: para enteros a, b, el entero a − b divide a P(a) − P(b). Esto obliga a ciertos congruencias: por ejemplo, si P(a) ≡ 0 (mod m), entonces P(a + m) ≡ 0 (mod m) (porque (a+m) − a = m divide a P(a+m) − P(a)).

## Identidades de Newton

Las **sumas de potencias** pₖ = r₁ᵏ + r₂ᵏ + ⋯ + rₙᵏ se relacionan con las funciones simétricas elementales eₖ de Vieta por las identidades de Newton:

p₁ = e₁,  p₂ = e₁p₁ − 2e₂,  p₃ = e₁p₂ − e₂p₁ + 3e₃, …

En general: pₖ − e₁pₖ₋₁ + e₂pₖ₋₂ − ⋯ ± k·eₖ = 0 para k ≤ n.

Permiten calcular Σrᵢ², Σrᵢ³, … sin conocer las raíces individuales —solo con los coeficientes del polinomio.

## Disparadores

- «Polinomio que se anula en ciertos puntos» → factoriza (x − rᵢ) y usa la forma factorizada.
- «Relaciones entre raíces sin hallarlas» → Vieta + manipulación algebraica.
- «Suma de coeficientes en posiciones pares/impares» → evaluar en ±1 o en raíces de la unidad.
- «Raíces enteras o racionales de un polinomio de coeficientes enteros» → teorema de la raíz racional.
- «Σrᵢ², Σrᵢ³, …» → identidades de Newton desde los coeficientes.

## Síntesis

> **Chunk mínimo:** Teorema del factor: P(a)=0 ⟺ (x−a)|P. Principio de identidad: n+1 puntos comunes → idénticos (de grado ≤ n). Vieta: las funciones simétricas elementales de las raíces son los coeficientes (con signo): Σr_i = −a_{n-1}/a_n, Πr_i = (−1)ⁿa₀/a_n. Evaluaciones especiales: P(1)=suma de coef., P(−1)=suma alternada; filtro de raíces de la unidad para sumas parciales. Coeficientes enteros: raíz racional p/q → p|a₀, q|aₙ; a−b divide P(a)−P(b). Newton: identidades que calculan Σrᵢᵏ desde los coeficientes sin conocer raíces.

---

*Antes del quiz: reconstruye de memoria el principio de identidad (con la condición n+1), las fórmulas de Vieta para Σrᵢ y Πrᵢ, el significado de P(1) y P(−1), y el teorema de la raíz racional.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Polinomios en Engel retoman [[zeitz-54]] con factor, Vieta y valores especiales. [[aime-alg]] los convierte en tecnica de examen, y [[arena-p4]] muestra que la misma manipulacion algebraica sostiene modelos, optimizacion y calculo aplicado.
<!-- GRAFO_CONEXO_OLEADA3_END -->
