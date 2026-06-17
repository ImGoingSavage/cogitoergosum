# Funciones aritméticas: d, σ y φ

*Lección redactada para CogitoErgoSum a partir de la sección 7.3 de Zeitz (Number Theoretic Functions). Cubre el contenido completo de la unidad.*

## Funciones multiplicativas

Una función f sobre los enteros positivos es **multiplicativa** si

**f(ab) = f(a)·f(b) siempre que a ⊥ b** (a y b coprimos: mcd = 1)

**La consecuencia que lo es todo:** una multiplicativa queda **determinada por sus valores en potencias de primos**. Razón: por el TFA, todo n se parte como n = p₁^e₁ · p₂^e₂ ⋯ donde los factores p^e son coprimos entre sí dos a dos; la multiplicatividad despedaza f(n) = f(p₁^e₁)·f(p₂^e₂)⋯. Protocolo: **evalúa en pʳ y multiplica**. Toda la sección es ese protocolo aplicado tres veces.

## d(n): número de divisores

**En potencias de primos:** los divisores de pʳ son 1, p, …, pʳ → d(pʳ) = r + 1.

**En general:** d(n) = (e₁+1)(e₂+1)⋯ — la fórmula que ya viste en §7.1.

**La biyección que sustenta todo (principio 7.3.6):** si n = ab con a ⊥ b, **cada divisor de n se factoriza de manera ÚNICA como (divisor de a)·(divisor de b)** — la parte del divisor hecha de primos de a, y la parte hecha de primos de b (la unicidad viene del TFA). Es una biyección entre divisores de n y pares (divisor de a, divisor de b): la misma maquinaria de codificación de §6.2 trabajando dentro de la teoría de números. De ella heredan la multiplicatividad d, σ y compañía.

## σ(n): suma de divisores

**En potencias de primos:** σ(pʳ) = 1 + p + p² + ⋯ + pʳ = **(pʳ⁺¹ − 1)/(p − 1)** (serie geométrica).

**Multiplicativa** por la misma biyección: al sumar sobre divisores de n = ab, sumas sobre pares y el doble sumatorio factoriza: σ(n) = σ(a)·σ(b).

Ejemplo: σ(360) = σ(2³)σ(3²)σ(5) = 15 · 13 · 6 = 1170.

## φ(n): el totient de Euler

**φ(n) = cuántos de 1, …, n son coprimos con n.** (Equivalente: cuántas fracciones k/n son irreducibles, cuántos residuos invertibles hay mod n.)

**Cálculo por complemento + PIE (los músculos de §6.3):** ejemplo φ(12). Los primos de 12 son 2 y 3. De los 12 números, quita los múltiplos de 2 (hay 6) y los de 3 (hay 4); devuelve los de 6 contados dos veces (hay 2):

φ(12) = 12 − 6 − 4 + 2 = **4** (son 1, 5, 7, 11 ✓)

PIE en general colapsa en el producto:

**φ(n) = n · Π (1 − 1/p)** sobre los primos p que dividen a n

(cada factor (1 − 1/p) «filtra» los múltiplos de p; la independencia de los filtros es PIE condensado). En potencias de primos se ve directo: φ(pʳ) = pʳ − pʳ⁻¹ (todos menos los múltiplos de p). Y es multiplicativa.

**Ejemplo del banco — φ(60):** 60 = 2²·3·5 → φ(60) = 60·(1/2)·(2/3)·(4/5) = **16** fracciones irreducibles k/60.

Lección de fondo: **el conteo (fase 2) y la teoría de números son el mismo músculo** — φ es literalmente un problema de complemento + PIE.

## El teorema gratis: sumas sobre divisores

> **Si f es multiplicativa, entonces F(n) = Σ_{d|n} f(d) también es multiplicativa.**

(La demostración es otra vez la biyección 7.3.6: los divisores de ab se parten en pares.) Consecuencia práctica: las temibles «sumas sobre divisores» se **domestican calculando en potencias de primos** y multiplicando. Casos conocidos: Σ_{d|n} 1 = d(n), Σ_{d|n} d = σ(n), y la joya Σ_{d|n} φ(d) = n (verifícala en pʳ: φ(1)+φ(p)+⋯+φ(pʳ) telescopia a pʳ).

**El disparador del banco:** aparece Σ_{d|n} f(d). Primera pregunta: **¿f es multiplicativa?** Si sí, la suma entera es multiplicativa → basta evaluarla en pʳ (donde los divisores son la lista limpia 1, p, …, pʳ) y multiplicar. Un problema sobre todo n se reduce a un cálculo de una línea.

## Disparadores

- «¿Cuántos divisores? ¿Suma de divisores?» → PPF: d = Π(eᵢ+1), σ = Π(p^{e+1}−1)/(p−1).
- «Fracciones irreducibles», «coprimos con n», «residuos invertibles» → φ(n) = n·Π(1−1/p).
- Σ sobre divisores de n → ¿multiplicativa? → evalúa en pʳ y multiplica.
- Cualquier función nueva con f(ab) = f(a)f(b) en coprimos → conócela en pʳ y la conoces entera.

## Síntesis

> **Chunk mínimo:** Multiplicativa = f(ab) = f(a)f(b) en coprimos ⇒ queda determinada por sus valores en pʳ: evalúa ahí y multiplica (vía TFA). El sustento es la biyección 7.3.6: divisor de ab ⟷ par (divisor de a, divisor de b), única por TFA. d(pʳ) = r+1 ⇒ d(n) = Π(eᵢ+1); σ(pʳ) = (pʳ⁺¹−1)/(p−1) (geométrica); φ = conteo por complemento + PIE: φ(12) = 12−6−4+2 = 4, en general φ(n) = n·Π(1−1/p), φ(pʳ) = pʳ − pʳ⁻¹ (φ(60) = 16). Teorema gratis: f multiplicativa ⇒ Σ_{d|n} f(d) multiplicativa — las sumas sobre divisores se domestican en pʳ; joya: Σ_{d|n} φ(d) = n.

---

*Antes del quiz: reconstruye de memoria la definición de multiplicativa y su consecuencia, la biyección 7.3.6, el cálculo de φ(12) por PIE, la fórmula del producto y las fórmulas de d y σ.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Las funciones aritmeticas d, sigma y phi cuentan estructura interna de los enteros. Dependen de la factorizacion de [[zeitz-71]], se simplifican con congruencias de [[zeitz-72]], y conectan con [[arena-b1]] porque muchas identidades son conteos de divisores vistos desde dos perspectivas.
<!-- GRAFO_CONEXO_OLEADA3_END -->
