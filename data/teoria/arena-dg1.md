# Estimación puntual y propiedades de estimadores

## ¿Qué es un estimador?

Un **estimador** θ̂ = T(X₁,...,Xₙ) es una función de los datos que aproxima un parámetro desconocido θ.

Los estimadores son variables aleatorias — tienen distribución, esperanza y varianza.

---

## Propiedades deseables

### Insesgamiento (Unbiasedness)

**Bias(θ̂) = E[θ̂] − θ**

θ̂ es insesgado si Bias = 0, es decir, E[θ̂] = θ.

Ejemplo: X̄ es insesgado para μ (para cualquier distribución con media μ).

### Error cuadrático medio

**MSE(θ̂) = Var(θ̂) + Bias(θ̂)²**

MSE combina varianza y sesgo. Para estimadores insesgados: MSE = Var.

Comparación: Si θ̂₁ tiene menor MSE que θ̂₂ para todo θ → θ̂₁ domina a θ̂₂.

### Consistencia

θ̂ₙ es **consistente** si θ̂ₙ →^P θ para todo θ.

Condición suficiente: si Bias(θ̂ₙ)→0 y Var(θ̂ₙ)→0, entonces θ̂ₙ es consistente (por desigualdad de Chebyshev).

La Ley de los Grandes Números implica que X̄ es consistente para μ.

---

## Información de Fisher

**I(θ) = E[(∂ ln f(X|θ)/∂θ)²] = −E[∂² ln f(X|θ)/∂θ²]**

Mide cuánta información contiene un dato sobre θ — la curvatura promedio de la log-verosimilitud.

| Distribución | I(θ) |
|-------------|------|
| Bernoulli(p) | 1/(p(1-p)) |
| N(μ,σ²) — para μ | 1/σ² |
| Poisson(λ) | 1/λ |
| Exp(λ) | 1/λ² |

Para n observaciones i.i.d.: **I_n(θ) = n·I(θ)** (la información es aditiva).

---

## Cota de Cramér-Rao

Para cualquier estimador insesgado θ̂:

**Var(θ̂) ≥ 1 / (n·I(θ))**

La **eficiencia** de θ̂ es: e(θ̂) = [n·I(θ)]⁻¹ / Var(θ̂) ∈ (0,1].

Un estimador es **eficiente** si alcanza la cota (e=1).

El MLE es asintóticamente eficiente (alcanza la cota para n grande).

---

## Estadístico suficiente

T(X) es **suficiente** para θ si la distribución condicional de X dado T(X)=t no depende de θ.

**Criterio de factorización (Fisher-Neyman):**

f(x|θ) = g(T(x), θ) · h(x)

T es suficiente ↔ la verosimilitud solo depende de x a través de T(x).

| Distribución | Estadístico suficiente |
|-------------|----------------------|
| Bernoulli(p) | T = ΣXᵢ (total de éxitos) |
| N(μ,σ²) — μ desconocida | T = ΣXᵢ (o X̄) |
| N(μ,σ²) — ambos desconocidos | T = (ΣXᵢ, ΣXᵢ²) |
| Poisson(λ) | T = ΣXᵢ |
| Uniform[0,θ] | T = X₍ₙ₎ = max(X₁,...,Xₙ) |

---

## Métodos de estimación

### Estimador de momentos (MM)

Iguala los momentos teóricos a los muestrales:

E[X] = X̄, E[X²] = (1/n)ΣXᵢ², etc.

Simple pero puede ser ineficiente.

### Máxima verosimilitud (MLE)

Maximiza L(θ|x) = ∏ f(xᵢ|θ) (o su logaritmo).

Propiedades del MLE:
1. **Consistente**: θ̂_MLE →^P θ
2. **Asintóticamente normal**: √n(θ̂_MLE-θ) →^d N(0, 1/I(θ))
3. **Asintóticamente eficiente**: alcanza la cota de Cramér-Rao
4. **Invariante**: MLE de g(θ) es g(θ̂_MLE)

---

## UMVUE

**Uniformly Minimum Variance Unbiased Estimator** — estimador insesgado con menor varianza para todo θ.

**Teorema de Rao-Blackwell:** Si θ̂ es insesgado y T es suficiente, entonces E[θ̂|T] es insesgado con Var ≤ Var(θ̂).

**Teorema de Lehmann-Scheffé:** Si T es suficiente y **completo**, toda función de T que sea insesgada es el UMVUE.

T es completo si: E[g(T)]=0 para todo θ ⟹ g(T)=0 a.s.

Ejemplo: X̄ es UMVUE de μ para la distribución normal (T=ΣXᵢ es suficiente y completo).

---

## Eficiencia relativa

**e(θ̂₁, θ̂₂) = MSE(θ̂₂) / MSE(θ̂₁)**

Si e > 1: θ̂₁ es más eficiente.

Para estimadores insesgados: e(X̄, mediana) = π/2 ≈ 1.57 para la normal — X̄ es 57% más eficiente que la mediana.

Para colas pesadas (Cauchy): la mediana es mucho más eficiente que X̄ (X̄ tiene varianza infinita).

---

## Estimación Bayesiana

| Pérdida | Estimador de Bayes |
|---------|-------------------|
| Cuadrática (θ-δ)² | Media posterior E[θ|x] |
| Absoluta |θ-δ| | Mediana posterior |
| 0-1 | Moda posterior (MAP) |

**Riesgo de Bayes:** r(δ) = E_θ[R(θ,δ)] = ∫ R(θ,δ)·π(θ) dθ

El estimador de Bayes minimiza el riesgo de Bayes (esperanza del riesgo frecuentista sobre el prior).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿El estimador sobreestima?" | Calcular E[θ̂]-θ (sesgo) |
| "¿Converge con n grande?" | Consistencia: Bias→0, Var→0 |
| "Cota inferior de la varianza" | Cramér-Rao: Var≥1/(n·I(θ)) |
| "¿La muestra captura toda la info de θ?" | Estadístico suficiente (factorización) |
| "Mejorar estimador dado suficiente" | Rao-Blackwell: condiciona en T |
| "Pérdida cuadrática + prior" | Estimador de Bayes = media posterior |
| "MLE de función de θ" | Invarianza: g(θ̂_MLE) |

---

> **Síntesis:** El triángulo insesgamiento-consistencia-eficiencia define qué hace un buen estimador. La cota de Cramér-Rao es el límite físico de la precisión. El estadístico suficiente comprime los datos sin pérdida de información. El MLE es el estimador universal: consistente, eficiente y fácil de construir.

---

*Retrieval: cierra y responde: (1) MSE de un estimador con Bias=0.3 y Var=4; (2) I(λ) para Poisson(λ); (3) cota CR para varianza de estimador insesgado de λ con n=50 Poissons; (4) estadístico suficiente para Uniform[0,θ].*
