# Estimación puntual: MLE, Cramér-Rao y UMVUE

## Métodos de encontrar estimadores

### Método de momentos (MoM)

Iguala los primeros k momentos muestrales mⱼ=(1/n)ΣXᵢʲ con los poblacionales μ'ⱼ(θ₁,…,θₖ) y despeja.

Simple pero puede ser ineficiente. No requiere forma cerrada de la distribución.

### Máxima verosimilitud (MLE)

Maximiza L(θ|x) = Πf(xᵢ|θ), equivalentemente ℓ(θ) = Σlog f(xᵢ|θ).

Pasos:
1. Calcula ℓ(θ) = Σlog f(xᵢ|θ)
2. Resuelve ∂ℓ/∂θ = 0 (ecuación de puntuación)
3. Verifica que sea máximo (segunda derivada negativa)

| Distribución | MLE |
|-------------|-----|
| Bernoulli(p) | p̂ = X̄ |
| Normal(μ,σ²) | μ̂=X̄, σ̂²=(1/n)Σ(Xᵢ−X̄)² |
| Poisson(λ) | λ̂ = X̄ |
| Exponencial(λ) | λ̂ = 1/X̄ |
| Uniform[0,θ] | θ̂ = X₍ₙ₎ = máx Xᵢ |
| f(x|θ)=θx^{θ−1}, 0<x<1 | θ̂ = −n/Σlog Xᵢ |
| Doble exponencial (Laplace) | θ̂ = mediana muestral |

**Invarianza del MLE:** Si θ̂ es MLE de θ, entonces g(θ̂) es MLE de g(θ).

---

## Información de Fisher

**I(θ) = E[(∂ log f(X|θ)/∂θ)²] = −E[∂² log f(X|θ)/∂θ²]**

Para n obs. i.i.d.: I_n(θ) = n·I(θ).

| Distribución | I(θ) |
|-------------|------|
| Bernoulli(p) | 1/(p(1−p)) |
| N(μ,σ²) — para μ (σ² conocida) | 1/σ² |
| N(μ,σ²) — para σ² (μ conocida) | 1/(2σ⁴) |
| Poisson(λ) | 1/λ |
| Exponencial(λ) | 1/λ² |
| Gamma(α,β) — para β (α conocido) | α/β² |

---

## Cota de Cramér-Rao

Para todo estimador insesgado τ̂ de τ(θ):

**Var(τ̂) ≥ [τ'(θ)]² / (n·I(θ))**

La cota se alcanza ↔ ∂ log f(x|θ)/∂θ = a(θ)[τ̂(x) − τ(θ)] para alguna función a(θ).

Esto sucede exactamente en las familias exponenciales de un parámetro.

**Eficiencia:** e(τ̂) = [τ'(θ)]²/(n·I(θ)·Var(τ̂)) ∈ (0,1]; vale 1 solo si τ̂ alcanza la cota.

Ejemplo: X̄ para Bernoulli(p) tiene Var=p(1−p)/n y la cota CR es p(1−p)/n → X̄ es eficiente.

---

## UMVUE: Estimador insesgado de mínima varianza uniforme

Un estimador δ* es **UMVUE** de τ(θ) si es insesgado y Var(δ*) ≤ Var(δ) para todo estimador insesgado δ y todo θ.

**Teorema de Rao-Blackwell:** Si δ es insesgado y T suficiente, entonces δ* = E[δ|T] es insesgado con Var(δ*) ≤ Var(δ) para todo θ. No peor en todos los θ simultáneamente.

**Teorema de Lehmann-Scheffé:** Si T es **suficiente y completo** y φ(T) es insesgado para τ(θ), entonces φ(T) es el único UMVUE de τ(θ).

**Receta para encontrar el UMVUE:**
1. Encuentra T suficiente y completo.
2. Encuentra cualquier estimador insesgado δ de τ(θ).
3. Calcula φ(T) = E[δ|T].
4. φ(T) es el UMVUE.

Ejemplos clásicos:

| Distribución | Parámetro | UMVUE |
|-------------|-----------|-------|
| Bernoulli(p) | p | X̄ |
| Bernoulli(p) | p² | X̄(X̄−1/n)·n/(n−1) = (ΣXᵢ)(ΣXᵢ−1)/(n(n−1)) |
| N(μ,σ²) | μ | X̄ |
| N(μ,σ²) | σ² | S² = Σ(Xᵢ−X̄)²/(n−1) |
| N(θ,1) | θ² | X̄²−1/n |
| Exp(λ) | 1/λ | X̄ |

---

## Estimación Bayesiana

| Función de pérdida | Estimador de Bayes δ*(x) |
|-------------------|--------------------------|
| Cuadrática (θ−δ)² | Media posterior E[θ|x] |
| Absoluta |θ−δ| | Mediana posterior |
| 0-1 | Moda posterior (MAP) |

**Familias conjugadas:**

| Verosimilitud | Prior conjugado | Posterior |
|---------------|-----------------|-----------|
| Bernoulli(p) | Beta(α,β) | Beta(α+Σxᵢ, β+n−Σxᵢ) |
| Poisson(λ) | Gamma(α,β) | Gamma(α+Σxᵢ, β+n) |
| N(μ,σ²) σ² conocida | N(μ₀,τ²) | N(media ponderada, varianza combinada) |

---

## Propiedades asintóticas del MLE

Para familias regulares, √n(θ̂_MLE − θ) →_d N(0, 1/I(θ)).

Esto implica:
- **Consistencia**: θ̂_MLE → θ en probabilidad
- **Eficiencia asintótica**: alcanza la cota CR en el límite
- **CI asintótico**: θ̂ ± z_{α/2}/√(n·I(θ̂))

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Estima θ maximizando la información" | MLE: maximiza ℓ(θ)=Σlog f(xᵢ|θ) |
| "Cota inferior de varianza de estimador insesgado" | Cramér-Rao: Var≥[τ'(θ)]²/(n·I(θ)) |
| "Mejorar un estimador con estadístico suficiente" | Rao-Blackwell: E[δ|T] |
| "Mejor estimador insesgado con T completo" | Lehmann-Scheffé: φ(T) insesgado es UMVUE |
| "MLE de g(θ)" | Invarianza: es g(θ̂_MLE) |
| "Pérdida cuadrática + prior" | Bayes = media posterior |

---

> **Síntesis (Casella & Berger, Ch 7):** MLE = cuasi-automático y asintóticamente óptimo. UMVUE = óptimo exacto entre todos los insesgados — se construye condicionando en T completo suficiente. La cota CR dice cuánto podemos aspirar a reducir la varianza; el MLE la alcanza en el límite. La estimación Bayesiana resuelve la cuestión de qué hacer cuando tenemos información previa.

---

*Retrieval: (1) X₁,…,Xₙ i.i.d. Uniform[0,θ]. Encuentra el MLE, su sesgo y un estimador insesgado basado en él. (2) ¿Cuándo alcanza un estimador insesgado la cota CR? (3) Enuncia Rao-Blackwell. (4) ¿Por qué el MLE de la doble exponencial es la mediana?*
