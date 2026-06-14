# Distribuciones importantes y sus relaciones

## La familia Gamma

**Gamma(α, λ):** densidad f(x) = λ^α·x^{α-1}·e^{-λx}/Γ(α) para x>0.

E[X] = α/λ ;  Var[X] = α/λ²

**Relaciones clave:**
- Gamma(1, λ) = Exp(λ) — la exponencial es un caso especial
- Gamma(n, λ) = suma de n Exp(λ) independientes (para n entero)
- Gamma(n/2, 1/2) = χ²(n) — la chi-cuadrado es una Gamma

| α | λ | Distribución especial |
|---|---|----------------------|
| 1 | λ | Exp(λ) |
| n entero | λ | Erlang(n,λ) |
| n/2 | 1/2 | χ²(n) |

Propiedad de reproducción: X₁~Gamma(α₁,λ), X₂~Gamma(α₂,λ) independientes → X₁+X₂~Gamma(α₁+α₂,λ).

---

## La distribución Beta

**Beta(α, β):** densidad f(x) = x^{α-1}(1-x)^{β-1}/B(α,β) para x∈(0,1).

**E[X] = α/(α+β);  Var[X] = αβ/((α+β)²(α+β+1))**

| α | β | Distribución especial |
|---|---|----------------------|
| 1 | 1 | Uniform[0,1] |
| 1/2 | 1/2 | Arcsine |
| n | m | k-ésimo estadístico de orden de Unif[0,1] (k=n, n+m-1 total) |

**Relación con Gamma:** Si X~Gamma(α), Y~Gamma(β) independientes (misma escala), entonces **X/(X+Y) ~ Beta(α,β)**.

La Beta es el **conjugate prior** de la binomial: prior Beta(α,β) + datos Bin(n,p) → posterior Beta(α+x, β+n-x).

---

## Distribución t-Student

**t(ν) = Z / √(V/ν)** donde Z~N(0,1), V~χ²(ν) independientes.

**E[X] = 0** para ν>1 (indefinida para ν≤1, como la Cauchy t(1))

**Var[X] = ν/(ν-2)** para ν>2 (indefinida para ν≤2)

Propiedades:
- Simétrica alrededor de 0
- Colas más pesadas que la normal
- t(ν) → N(0,1) cuando ν→∞
- t(1) = Cauchy (sin media ni varianza)

**Aplicación:** T = (X̄−μ)/(S/√n) ~ t(n−1) para muestra de N(μ,σ²) con σ desconocida.

---

## Distribución F de Snedecor

**F(m,n) = (χ²(m)/m) / (χ²(n)/n)** donde χ²s independientes.

**E[F] = n/(n−2)** para n>2

Aplicaciones:
- Test de igualdad de varianzas: F = S₁²/S₂² ~ F(n₁−1, n₂−1)
- ANOVA: MS_between/MS_within ~ F(k−1, n−k)

---

## Distribución Lognormal

**X = e^Y** con Y~N(μ,σ²):

**E[X] = e^{μ+σ²/2}** (mayor que e^μ por la convexidad de e^y)

**Var[X] = e^{2μ+σ²}·(e^{σ²}−1)**

**Mediana de X = e^μ** (siempre menor que la media)

La distribución de ln(X) es N(μ,σ²) — útil para modelar precios de activos, ingresos, tamaños de partículas.

---

## Distribución Weibull

**F(x) = 1 − e^{-(x/λ)^k}** para x>0.

**E[X] = λ·Γ(1+1/k)**

| k | Comportamiento |
|---|---------------|
| k < 1 | Tasa de fallo decreciente (infant mortality) |
| k = 1 | Tasa constante (Exp) |
| k > 1 | Tasa de fallo creciente (envejecimiento) |

---

## Distribución Bernoulli y familia binomial

| Distribución | Modela | Parámetros |
|-------------|--------|-----------|
| Bernoulli(p) | Un ensayo binario | p |
| Bin(n,p) | Suma de n Bernoulli i.i.d. | n, p |
| Geom(p) | Intentos hasta primer éxito | p |
| Bin. negativa(r,p) | Intentos hasta r-ésimo éxito | r, p |
| Hipergeométrica | Éxitos en muestra sin reemplazo | N, K, n |

---

## La familia Poisson

**Poisson(λ):** P(X=k) = e^{-λ}λ^k/k!

Propiedad de reproducción: sum de Poissons independientes es Poisson.

**Adelgazamiento:** Si X~Poisson(λ) y cada evento se retiene con probabilidad p independientemente, el número retenido ~ Poisson(λp).

**Condicional:** Si X+Y~Poisson(λ+μ) y X~Poisson(λ) independiente de Y~Poisson(μ), entonces [X|X+Y=n] ~ Bin(n, λ/(λ+μ)).

---

## Momentos de la distribución normal estándar

X~N(0,1): E[X^{2k}] = (2k-1)!! = (2k-1)·(2k-3)·…·3·1

| Momento | Valor |
|---------|-------|
| E[X] | 0 |
| E[X²] | 1 |
| E[X³] | 0 |
| E[X⁴] | 3 |
| E[X⁵] | 0 |
| E[X⁶] | 15 |
| E[|X|] | √(2/π) |

**Función generatriz de momentos de N(0,1):** M(t) = e^{t²/2}

---

## Familia exponencial

Densidad de la forma: **f(x|θ) = h(x) · exp(η(θ)·T(x) − A(θ))**

| Distribución | η(θ) | T(x) | A(θ) |
|-------------|------|------|------|
| N(μ,σ²=1) | μ | x | μ²/2 |
| Poisson(λ) | ln(λ) | x | λ |
| Bernoulli(p) | logit(p) | x | ln(1/(1-p)) |

Propiedad: E[T(X)] = dA/dη. La familia exponencial tiene **estadístico suficiente** T(x) (compacto) y **priors conjugados**.

---

## Dispersadores clave

| Señal | Jugada |
|-------|--------|
| "Tiempo hasta n-ésimo evento de Poisson" | Gamma(n, λ) |
| "Fracción de dos Gammas" | Beta(α,β) |
| "Prior para proporción" | Beta(α,β) conjugado binomial |
| "Normal con σ desconocida" | t(n-1) |
| "Cociente de chi-cuadrados" | F(m,n) |
| "ln(X) es normal" | X es lognormal |
| "P(X es par) para Poisson" | (1+e^{-2λ})/2 via pgf |
| "Mgf de N(μ,σ²) en t=1" | e^{μ+σ²/2} |

---

> **Síntesis:** Las distribuciones no son listas de fórmulas — son familias relacionadas. La Gamma generaliza la Exp; la Beta es una Gamma normalizada; la t es normal/chi; la F es cociente de chi. El principio unificador: las mgf (o pgf o función característica) convierten todas estas relaciones en álgebra.

---

*Retrieval: cierra y responde: (1) E y Var de Gamma(4,2); (2) distribución de X/(X+Y) si X~Gamma(3), Y~Gamma(5); (3) E[F(5,10)]; (4) E[X] y mediana[X] para X~Lognormal(1,1).*
