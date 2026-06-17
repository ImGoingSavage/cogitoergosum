# Engel · Teoría de números de competencia: el formulario de combate

*Lección redactada para CogitoErgoSum a partir del capítulo 6 de «Problem-Solving Strategies» (A. Engel), Number Theory. Cubre el formulario de prerrequisitos y la sección de divisibilidad; el resto del capítulo es cantera para sesiones del camino 1.*

## La fórmula más útil en competencias (Engel dixit)

> **a − b | aⁿ − bⁿ para todo n ≥ 1.**

*Por qué:* aⁿ − bⁿ = (a − b)(aⁿ⁻¹ + aⁿ⁻²b + ⋯ + abⁿ⁻² + bⁿ⁻¹) — la factorización telescópica clásica. (Visto con congruencias es inmediato: a ≡ b (mod a−b) ⇒ aⁿ ≡ bⁿ.)

**La versión para sumas se deduce gratis:** sustituye b por −b. Si n es **IMPAR**, (−b)ⁿ = −bⁿ, y queda

**a + b | aⁿ + bⁿ para n impar.**

(Para n par no hay análogo: a + b ∤ a² + b² en general.) Y el caso n = 2 de la primera es la **diferencia de cuadrados** a² − b² = (a−b)(a+b): toda la familia sale de una sola matriz.

Usos típicos: 7 | 2³ᵏ − 1 (pues 8−1 | 8ᵏ−1); «demuestra que 13 divide a 4¹⁰⁰ + 9¹⁰⁰»… el reflejo es reescribir las potencias para que aparezca un a − b o a + b conveniente.

## La identidad de Sophie Germain

> **a⁴ + 4b⁴ = (a² + 2b² − 2ab)(a² + 2b² + 2ab)**

**La maniobra que la produce:** a⁴ + 4b⁴ no factoriza a la vista (es una *suma*). **Suma y resta el término cruzado** 4a²b² para completar el cuadrado:

a⁴ + 4b⁴ = (a⁴ + 4a²b² + 4b⁴) − 4a²b² = (a² + 2b²)² − (2ab)² — ¡diferencia de cuadrados! — = (a² + 2b² − 2ab)(a² + 2b² + 2ab).

**Por qué es excepcional:** las sumas de potencias casi nunca factorizan sobre los enteros (x² + y², x⁴ + y⁴ son irreducibles); esta es la gran excepción explotable. Aplicación de manual: ¿n⁴ + 4 es primo para algún n > 1? Sophie Germain con b = 1: n⁴ + 4 = (n² − 2n + 2)(n² + 2n + 2), y para n > 1 ambos factores son > 1 → **siempre compuesto**. Verifica además que ambos factores son positivos: a² + 2b² ± 2ab = (a ± b)² + b² ≥ 0, con igualdad imposible si b ≠ 0.

## La fórmula de Legendre: primos dentro de n!

> **El primo p aparece en n! con exponente ⌊n/p⌋ + ⌊n/p²⌋ + ⌊n/p³⌋ + ⋯** (suma finita).

*Por qué:* entre 1 y n hay ⌊n/p⌋ múltiplos de p (cada uno aporta al menos un factor p), ⌊n/p²⌋ múltiplos de p² (aportan un segundo), etc. Cada capa cuenta una contribución más — sin doble conteo ni omisión.

**Ejemplo del banco — ¿en cuántos ceros termina 100!?** Los ceros los fabrican los pares 2×5 y los 5 escasean. Exponente de 5 en 100!: ⌊100/5⌋ + ⌊100/25⌋ + ⌊100/125⌋ = 20 + 4 + 0 = **24 ceros**. (El exponente de 2 es 97, sobra de sobra.)

Toda pregunta de divisibilidad de factoriales pasa por aquí: ¿2¹⁰⁰ | 150!? Exponente de 2 en 150!: 75+37+18+9+4+2+1 = 146 ≥ 100 → sí.

## Pequeño Fermat: tres pruebas y una advertencia

Engel presenta el teorema (p primo ⇒ p | aᵖ − a) por tres caminos — tenerlos los tres es entrenamiento de transferencia:

1. **Inducción con binomio:** (a+1)ᵖ ≡ aᵖ + 1 (mod p) porque todos los C(p,k) intermedios son múltiplos de p (el p del numerador no se cancela: p es primo).
2. **Congruencias:** {a, 2a, …, (p−1)a} es permutación de {1, …, p−1} mod p; multiplica y cancela (p−1)!.
3. **Collares:** órbitas de rotación de tamaño exactamente p (la combinatoria pura de Zeitz §7.5).

**La advertencia: el recíproco FALLA.** «n | 2ⁿ − 2 ⇒ n primo» es falso: el contraejemplo mínimo es **n = 341 = 11 · 31**, compuesto, y sin embargo 341 | 2³⁴¹ − 2 (es un *pseudoprimo* de Fermat en base 2). El pequeño Fermat da condición **necesaria** de primalidad, jamás suficiente. Quien lo cite al revés está cometiendo el error lógico recíproca-por-implicación de §2.3.

## Fermat–Euler: el puente con φ

> **Si a ⊥ m, entonces a^φ(m) ≡ 1 (mod m).**

La generalización de Fermat a módulo compuesto (con m = p primo, φ(p) = p−1 recupera el original). La prueba es la misma del camino 2: los φ(m) residuos invertibles, multiplicados todos por a, se permutan. Es el puente entre §7.3 (φ) y §7.2 (congruencias): para reducir potencias gigantes módulo m compuesto, **el exponente se reduce módulo φ(m)**. Ejemplo: 7¹⁰⁰⁰ mod 20 — φ(20) = 8, 1000 ≡ 0 (mod 8), así que 7¹⁰⁰⁰ ≡ (7⁸)¹²⁵ ≡ 1.

## Disparadores

- Divisibilidad de **diferencias/sumas de potencias** → a−b | aⁿ−bⁿ; con n impar, a+b | aⁿ+bⁿ.
- a⁴ + 4b⁴, n⁴ + 4, sumas que «deberían» factorizar → Sophie Germain (suma y resta el cruzado).
- **Factoriales**: ceros finales, ¿pᵏ divide a n!? → Legendre.
- Potencia gigante módulo compuesto → Fermat–Euler: reduce el exponente mod φ(m).
- «n divide a 2ⁿ−2, luego es primo» → falso: 341.

## Síntesis

> **Chunk mínimo:** La fórmula más útil: a − b | aⁿ − bⁿ (factorización telescópica); con b → −b y n IMPAR: a + b | aⁿ + bⁿ. Sophie Germain: a⁴ + 4b⁴ = (a² + 2b² − 2ab)(a² + 2b² + 2ab) — suma y resta 4a²b² para fabricar la diferencia de cuadrados; n⁴ + 4 es compuesto para n > 1. Legendre: el exponente de p en n! es ⌊n/p⌋ + ⌊n/p²⌋ + ⋯ (100! termina en 24 ceros: los 5 escasean). Fermat por tres caminos (binomio con C(p,k) ≡ 0, permutación de residuos, collares) y la advertencia: el recíproco falla — 341 = 11·31 es pseudoprimo en base 2. Fermat–Euler: a ⊥ m ⇒ a^φ(m) ≡ 1 (mod m): reduce exponentes gigantes mod φ(m).

---

*Antes del quiz: reconstruye de memoria la fórmula útil con su deducción para sumas, la maniobra completa de Sophie Germain, el cálculo de los ceros de 100! y el contraejemplo 341.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

La cantera de teoria de numeros de Engel profundiza los filtros de [[zeitz-71]] y las congruencias de [[zeitz-72]]. En entrevistas, [[arena-q13]] usa la misma caja de herramientas para pruebas cortas donde modularidad, paridad y descenso eliminan familias completas de candidatos.
<!-- GRAFO_CONEXO_OLEADA3_END -->
