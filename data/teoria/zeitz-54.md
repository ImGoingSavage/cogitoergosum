# Polinomios: ceros, coeficientes y Vieta

*Lección redactada para CogitoErgoSum a partir de la sección 5.4 de Zeitz (Polynomials). Cubre el contenido completo de la unidad.*

## Teorema del resto y teorema del factor

> **Teorema del resto:** al dividir P(x) entre (x − a), el resto es **P(a)**.

*Demostración en una línea:* el algoritmo de división da P(x) = Q(x)(x − a) + r con r constante. Esa es una **identidad** (vale para todo x) — así que usa la herramienta «**sustituye valores convenientes**»: con x = a, el término con Q se anula y queda P(a) = r. ∎

> **Corolario (teorema del factor):** a es cero de P ⟺ (x − a) divide a P.

Estos dos renglones son el puente entre el mundo de los **ceros** y el mundo de los **factores**.

## Conocer los ceros es conocer el polinomio

Por el **teorema fundamental del álgebra** (todo polinomio de grado n ≥ 1 tiene n ceros complejos, contados con multiplicidad), un P de grado n se escribe

P(x) = aₙ(x − r₁)(x − r₂)⋯(x − rₙ)

— el coeficiente líder y los ceros lo determinan todo.

**La jugada profesional: si los ceros de TU polinomio no se ven, DEFINE OTRO cuyos ceros sí se vean.**

**USAMO 1975 (el ejemplo a interiorizar):** P tiene grado n y P(k) = k/(k+1) para k = 0, 1, …, n. Halla P(n+1).

1. La condición «P(k) = k/(k+1)» es fea (no son ceros). Límpiala: define **Q(x) = (x+1)·P(x) − x**. Ahora Q(k) = (k+1)·k/(k+1) − k = 0 para k = 0, …, n: ¡**Q tiene ceros 0, 1, …, n**, y grado n+1!
2. Luego Q(x) = C·x(x−1)(x−2)⋯(x−n) para alguna constante C.
3. **Sustituye el valor que mata lo molesto:** en x = **−1**, el término (x+1)P(x) se anula: Q(−1) = 1. Y el producto da C·(−1)(−2)⋯(−1−n) = C·(−1)ⁿ⁺¹(n+1)!. Despeja: C = (−1)ⁿ⁺¹/(n+1)!.
4. Evalúa donde piden: Q(n+1) = (n+2)P(n+1) − (n+1) = C·(n+1)! = (−1)ⁿ⁺¹. Despeja:

P(n+1) = (n+1 + (−1)ⁿ⁺¹)/(n+2) — es decir, **1 si n es impar** y **n/(n+2) si n es par**.

Dos herramientas hicieron todo: *fabricar el polinomio con ceros visibles* y *evaluar la identidad en puntos convenientes* (x = −1 para despejar C; x = n+1 para responder). Una identidad polinómica vale para TODO x: **elige el x que mate lo molesto** — es la herramienta más barata del capítulo.

## Las fórmulas de Vieta

Para el polinomio **mónico** xⁿ + aₙ₋₁xⁿ⁻¹ + ⋯ + a₁x + a₀ con ceros r₁, …, rₙ, expandir Π(x − rᵢ) da el patrón **«suma de productos» con signos alternados**:

aₙ₋ₖ = (−1)ᵏ · (suma de todos los productos de k ceros distintos)

**La cúbica, explícita** — x³ + a₂x² + a₁x + a₀ con ceros q, r, s:

- a₂ = −(q + r + s)
- a₁ = qr + qs + rs
- a₀ = −qrs

(Verifica los signos con (x−1)³: ceros 1,1,1 → x³ − 3x² + 3x − 1 ✓.)

## Vieta rara vez pide los ceros

**El patrón de uso:** el problema da información sobre las raíces (suma, producto, producto de dos de ellas) pero **NO pide las raíces** — pide una **combinación simétrica** de ellas. El error de principiante que Vieta evita: lanzarse a resolver el polinomio.

**Mini-ejemplo (banco):** suma de los **cuadrados** de las raíces de x² − 5x + 3 = 0. Vieta: r + s = 5, rs = 3. Entonces r² + s² = (r+s)² − 2rs = 25 − 6 = **19**. Sin discriminante, sin raíces.

**USAMO 1984 (la versión de combate):** el polinomio x⁴ − 18x³ + a x² + 200x − 1984 tiene cuatro raíces y se sabe que **el producto de dos de ellas es −32**; halla a. Vieta: el producto de las cuatro es −1984, así que el producto de las otras dos es −1984/(−32) = **62**. Agrupa por parejas: llama u = (suma del primer par), v = (suma del segundo). Vieta para la suma total: u + v = 18; para el coeficiente de x: la expansión da que 200 = −(u·62 + v·(−32))… resolviendo el sistemita lineal sale u, v, y a = 62 + (−32) + uv = **86**. El punto pedagógico: jamás se conocieron las raíces individuales — solo **bloques simétricos** (sumas y productos por pares) manejados como nuevas incógnitas.

## Disparadores

- «Halla el resto de dividir P entre (x − a)» → evalúa: P(a).
- Condición fea sobre P en muchos puntos (P(k) = algo) → fabrica Q con ceros visibles; evalúa en los x que anulan piezas.
- Datos sobre raíces sin pedir raíces (sumas, productos, simétricas) → Vieta + identidades simétricas (s, p de §3.1/§5.2).
- «Suma de cuadrados/recíprocos de las raíces» → (r+s)² − 2rs, (r+s)/rs — nunca el discriminante.

## Síntesis

> **Chunk mínimo:** Resto de P entre (x−a) = P(a) (la división es identidad: evalúa en x = a); corolario: a es cero ⟺ (x−a) divide. Grado n ⇒ P = aₙ·Π(x−rᵢ): líder + ceros lo determinan todo. Jugada profesional: si tus ceros no se ven, fabrica OTRO polinomio que sí los tenga (USAMO 1975: Q = (x+1)P − x tiene ceros 0…n; evalúa en x = −1 para despejar C y en n+1 para responder) — una identidad vale para TODO x: elige el que mate lo molesto. Vieta (mónico): aₙ₋ₖ = (−1)ᵏ·(suma de productos de k ceros); cúbica: a₂ = −(q+r+s), a₁ = qr+qs+rs, a₀ = −qrs. Patrón de uso: piden combinaciones simétricas, NO raíces — r²+s² = (r+s)² − 2rs, jamás el discriminante.

---

*Antes del quiz: reconstruye de memoria la prueba de una línea del teorema del resto, la jugada completa del USAMO 1975, las tres relaciones de la cúbica con sus signos y el cálculo de r²+s² sin resolver.*
