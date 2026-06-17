# Congruencias: el mundo finito de Zₘ

*Lección redactada para CogitoErgoSum a partir de la sección 7.2 de Zeitz (Congruence). Cubre el contenido completo de la unidad.*

## La definición y la idea

**a ≡ b (mod m)** significa: m divide a a − b; equivalentemente, **a = b + mk** para algún entero k; equivalentemente, a y b dejan el mismo residuo al dividirse entre m.

La idea grande: «ver el problema módulo m» colapsa los infinitos enteros en **solo m clases** {0, 1, …, m−1} = Zₘ. Un problema imposible sobre infinitos números se vuelve una verificación **finita** — a veces de una tabla de m × m casos. Es la simplificación más rentable de la teoría de números: tiras la información que no importa (el cociente) y conservas la que importa (el residuo).

## Qué operaciones sobreviven la reducción

Las congruencias **respetan suma, resta y producto**: si a ≡ a′ y b ≡ b′ (mod m), entonces

a + b ≡ a′ + b′,  a − b ≡ a′ − b′,  a·b ≡ a′·b′ (mod m)

Consecuencia práctica enorme: **puedes reducir ANTES de operar, no después**. Para el residuo de 123456 × 654321 mod 7 no multiplicas los grandes: reduces cada factor mod 7 primero y multiplicas residuos. Las potencias también (son productos repetidos): aⁿ ≡ (a mod m)ⁿ.

**Lo que NO sobrevive sin cuidado: la división.** De 2x ≡ 2y (mod 4) no se sigue x ≡ y (mod 4) (toma x=1, y=3). Cancelar c exige mcd(c, m) = 1.

## Potencias gigantes: busca el ±1

**El método:** para aⁿ mod m con n enorme, busca una potencia pequeña de a que sea ≡ 1 o ≡ −1 (mod m), y descompón el exponente.

**Ejemplo del banco:** 2¹⁰⁰⁰ mod 17. Calcula potencias chicas: 2⁴ = 16 ≡ **−1** (mod 17). Entonces

2¹⁰⁰⁰ = (2⁴)²⁵⁰ ≡ (−1)²⁵⁰ = 1 (mod 17) → **residuo 1**, sin calcular nada grande.

El −1 es incluso mejor que el 1: llega en la mitad de pasos y sus potencias alternan de forma controlada.

## Las reglas de divisibilidad SON congruencias

- **Regla del 9 (y del 3):** como 10 ≡ 1 (mod 9), cada potencia 10ᵏ ≡ 1ᵏ = 1. Un número d_r…d₁d₀ = Σ dᵢ·10ⁱ ≡ Σ dᵢ (mod 9): **todo número es congruente con la suma de sus dígitos mod 9** (y mod 3, pues 10 ≡ 1 también mod 3). Divisible entre 9 ⟺ su suma de dígitos lo es. ∎
- **Regla del 11:** como 10 ≡ **−1** (mod 11), 10ᵏ ≡ (−1)ᵏ, y el número ≡ d₀ − d₁ + d₂ − ⋯: la **suma alternada de dígitos** decide la divisibilidad entre 11.

Mismo molde: la regla de divisibilidad de m depende solo de qué es 10 módulo m.

## Por qué los primos son el mejor módulo

En Zₚ (p primo) **todo elemento no nulo tiene inverso multiplicativo único**: para cada a ≢ 0 hay un x con ax ≡ 1. (Razón: a, 2a, 3a, …, (p−1)a son todos distintos mod p — si ia ≡ ja entonces p | (i−j)a, y p primo sin dividir a a fuerza p | i−j — así que recorren todos los residuos no nulos, incluido el 1.) Consecuencia: **en Zₚ se puede dividir** — es un mundo donde el álgebra funciona completa.

De esa misma rotación de residuos vive el **pequeño teorema de Fermat**:

> Si p es primo y p ∤ a, entonces **a^(p−1) ≡ 1 (mod p)**.

(Esbozo: {a, 2a, …, (p−1)a} es una permutación de {1, 2, …, p−1}; multiplica todo en ambos lados y cancela (p−1)!.) Es el «busca el 1» garantizado: con módulo primo, siempre hay una potencia ≡ 1 de exponente p−1 o un divisor suyo. Para 2¹⁰⁰⁰ mod 17: Fermat da 2¹⁶ ≡ 1, y 1000 = 16·62 + 8, así que 2¹⁰⁰⁰ ≡ 2⁸ = 256 ≡ 1 ✓ (coincide con el camino del −1).

## Elegir el módulo ES la jugada

- La **paridad** de la fase 1 era el caso m = 2; las **coloraciones**, otros m disfrazados de geometría.
- «Demuestra que ningún número de la forma … es un cuadrado perfecto» → estudia **qué residuos pueden tener los cuadrados** en un módulo pequeño. Los cuadrados mod 4 solo son {0, 1}; mod 8 solo {0, 1, 4}; mod 3 solo {0, 1}. Si la forma dada cae siempre en un residuo prohibido (p. ej. ≡ 3 mod 4), jamás es cuadrado. ∎ Los módulos 3, 4, 8, 9 son los sospechosos de siempre para cuadrados; 7 y 9 para cubos.
- Al investigar un problema nuevo, **supón primero los datos primos o coprimos**: el caso general casi siempre se reduce al caso primo (vía PPF) — y el caso primo tiene todas las herramientas (inversos, Fermat).

## Disparadores

- «Residuo de una potencia gigante» → potencia pequeña ≡ ±1 (o Fermat si el módulo es primo).
- «Demuestra que nunca es cuadrado/cubo» → residuos posibles en módulo pequeño (4, 8, 3, 9).
- Dígitos, sumas de dígitos → mod 9; suma alternada → mod 11.
- Ecuación con enteros que «no cuadra» → redúcela mod 2, 3, 4… hasta que un lado no pueda igualar al otro.

## Síntesis

> **Chunk mínimo:** a ≡ b (mod m) ⟺ m | a−b: los infinitos enteros colapsan en m clases. Suma, resta y producto sobreviven ⇒ reduce ANTES de operar; la división NO (cancelar c exige mcd(c,m) = 1). Potencias gigantes: busca la potencia pequeña ≡ ±1 (2⁴ ≡ −1 mod 17 ⇒ 2¹⁰⁰⁰ ≡ 1). Reglas de divisibilidad = congruencias de 10: mod 9, 10 ≡ 1 ⇒ suma de dígitos; mod 11, 10 ≡ −1 ⇒ suma alternada. Zₚ con p primo: todo no nulo tiene inverso (a, 2a, …, (p−1)a permutan los residuos) ⇒ se puede dividir, y Fermat: a^(p−1) ≡ 1 si p ∤ a. Elegir el módulo ES la jugada: cuadrados solo {0,1} mod 4 y {0,1,4} mod 8; cubos → 7 y 9.

---

*Antes del quiz: reconstruye de memoria qué operaciones sobreviven la reducción, el cálculo completo de 2¹⁰⁰⁰ mod 17, la demostración de la regla del 9 y de dónde sale la del 11, y por qué Zₚ permite dividir.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Las congruencias convierten una pregunta infinita en un mundo finito donde los residuos importan. Se apoyan en [[zeitz-71]] para factorizacion y divisibilidad, alimentan problemas diofanticos en [[zeitz-74]], y conectan con [[arena-q12]] porque un residuo modulo m suele ser el invariante que no cambia.
<!-- GRAFO_CONEXO_OLEADA3_END -->
