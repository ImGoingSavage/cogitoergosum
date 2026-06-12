# Sucesiones y recurrencias

*Lección redactada para CogitoErgoSum a partir del capítulo de sucesiones y recurrencias de Engel (Problem-Solving Strategies). Cubre el contenido completo de la unidad.*

## La idea central

Una recurrencia *define* una sucesión a través de cómo cada término depende de los anteriores. El objetivo es hallar una **fórmula cerrada** que exprese aₙ sin recurrir a todos los términos previos. Las herramientas dependen del tipo: lineal homogénea (ecuación característica), no homogénea (solución particular + homogénea), no lineal (sustitución que linealiza) y de primer orden (puntos fijos, telescopio).

## Recurrencias lineales homogéneas de coeficientes constantes

La forma estándar: aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ + ⋯ + c_k aₙ₋k.

**Método**: escribe la **ecuación característica** xᵏ = c₁xᵏ⁻¹ + ⋯ + c_k (equivalentemente, x^k − c₁x^{k-1} − ⋯ − c_k = 0) y factoriza.

- **Raíces distintas r₁, …, r_m**: la solución general es aₙ = A₁r₁ⁿ + ⋯ + Aₘrₘⁿ. Los coeficientes A_i se determinan con las condiciones iniciales.
- **Raíz repetida r de multiplicidad m**: la contribución de r no es solo r^n, sino **(A₀ + A₁n + ⋯ + A_{m-1}nᵐ⁻¹)·rⁿ**. El factor polinomial en n aparece porque dos raíces colisionaron (límite de r₁ⁿ y r₂ⁿ cuando r₂→r₁). Ejemplo: si la ecuación tiene raíz doble r=2, la solución incluye (A+Bn)·2ⁿ.

Fibonacci: aₙ = aₙ₋₁ + aₙ₋₂ → x² − x − 1 = 0 → raíces φ = (1+√5)/2 y ψ = (1−√5)/2. Fórmula de Binet: aₙ = (φⁿ − ψⁿ)/√5.

## Recurrencias no homogéneas

Si aₙ = (parte lineal) + g(n), la solución general es la solución de la ecuación **homogénea asociada** más una **solución particular**:

- g(n) polinómica de grado d → probar una particular polinómica de grado d (o d+1 si 1 es raíz característica).
- g(n) = b·sⁿ → probar A·sⁿ (y multiplicar por n si s ya es raíz característica).

Las condiciones iniciales se aplican a la suma (homogénea + particular), no por separado.

## Puntos fijos para recurrencias de primer orden

Para aₙ₊₁ = f(aₙ), el **punto fijo** L resuelve L = f(L). Si la sucesión converge, converge a un punto fijo. Análisis de estabilidad:

- |f′(L)| < 1: L es **atractor** (las trayectorias cercanas se acercan → L).
- |f′(L)| > 1: L es **repulsor** (las trayectorias cercanas se alejan de L).

Truco práctico: el cambio de variable bₙ = aₙ − L suele dejar una recurrencia más simple (a menudo lineal homogénea de primer orden en bₙ), que se resuelve de inmediato: bₙ₊₁ = f′(L)·bₙ + correcciones de orden superior.

## Telescopio y sustituciones linealizadoras

**Telescopio**: si aₙ₊₁ − aₙ = g(n) es manejable, suma en cascada: aₙ = a₁ + Σg(k). Si aₙ₊₁/aₙ = g(n), multiplica en cascada.

**Sustituciones que linealizan**: muchas recurrencias no lineales se vuelven lineales tras una sustitución adecuada.

| Forma | Sustitución | Resultado |
|---|---|---|
| aₙ₊₁ = aₙ/(1 + aₙ) | bₙ = 1/aₙ | bₙ₊₁ = bₙ + 1 (aritmética) |
| aₙ₊₁ = aₙ² | bₙ = log aₙ | bₙ₊₁ = 2bₙ (geométrica) |
| aₙ₊₁ = raíz de aₙ · C | bₙ = log aₙ | lineal |
| aₙ₊₁ = L − k(aₙ − L)² | bₙ = aₙ − L | cuadrática cerca del punto fijo |

La pregunta correcta: «¿qué función de aₙ se comporta linealmente?»

## Disparadores

- «Recurrencia lineal de orden k con coeficientes constantes» → ecuación característica; raíces distintas → combinación de potencias; raíz doble → factor polinomial n multiplicando la potencia.
- «aₙ₊₁ = f(aₙ), ¿converge?» → busca el punto fijo L = f(L) y calcula |f′(L)|.
- «aₙ₊₁ = aₙ/(1 + aₙ)» o forma similar → sustitución bₙ = 1/aₙ linealiza.
- «aₙ₊₁ − aₙ = g(n)» y g(n) es una función simple → telescopio, suma en cascada.

## Síntesis

> **Chunk mínimo:** Recurrencia lineal homogénea: ecuación característica x^k − c₁x^{k-1} − ⋯ = 0; raíces distintas r_i → Σ A_i r_iⁿ; raíz r de multiplicidad m → (A₀+A₁n+⋯+A_{m-1}nᵐ⁻¹)rⁿ (el factor polinomial distingue el caso de raíz repetida). No homogénea: particular + homogénea; tipo de particular según la forma de g(n). Primer orden aₙ₊₁=f(aₙ): punto fijo L=f(L); |f′(L)|<1 atractor. Telescopio cuando aₙ₊₁−aₙ es manejable. Sustituciones linealizadoras: bₙ=1/aₙ para aₙ₊₁=aₙ/(1+aₙ); bₙ=log aₙ para productos/potencias.

---

*Antes del quiz: reconstruye de memoria la regla de la raíz repetida (con el factor polinomial), el criterio de estabilidad del punto fijo y la sustitución que linealiza aₙ₊₁=aₙ/(1+aₙ).*
