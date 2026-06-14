# Máxima verosimilitud y familias exponenciales

## La función de verosimilitud

Dado un modelo paramétrico f(x|θ) y observaciones x₁,...,xₙ i.i.d.:

**L(θ|x) = ∏ᵢ f(xᵢ|θ)**

**ℓ(θ|x) = Σᵢ ln f(xᵢ|θ)** — log-verosimilitud (más fácil de optimizar)

El MLE es: **θ̂ = argmax_θ ℓ(θ|x)**

Condición de primer orden (cuando el máximo es interior): **∂ℓ/∂θ = 0** (ecuación de verosimilitud)

---

## MLE para distribuciones comunes

| Distribución | Log-verosimilitud | MLE |
|-------------|-------------------|-----|
| Bernoulli(p) | xΣlnp+(n-Σx)ln(1-p) | p̂=X̄ |
| Poisson(λ) | -nλ+Σx·lnλ | λ̂=X̄ |
| N(μ,σ²) | -n/2·ln(σ²)-Σ(x-μ)²/(2σ²) | μ̂=X̄; σ̂²=Σ(x-X̄)²/n |
| Exp(λ) | n·lnλ-λΣx | λ̂=1/X̄ |
| Gamma(α,β) — β desconocido | n·α·lnβ+(α-1)Σlnx-βΣx | β̂=X̄/α (α fijo) |

**Nota:** El MLE de σ² para la normal (÷n) es sesgado; la varianza muestral S² (÷n-1) es insesgada.

---

## Propiedades asintóticas del MLE

Para n grande, bajo condiciones de regularidad:

**√n(θ̂_MLE − θ) →^d N(0, 1/I(θ))**

Equivalentemente: **θ̂_MLE ≈ N(θ, 1/(n·I(θ)))**

Esto da:
- IC del (1-α)%: θ̂ ± z_{α/2} / √(n·I(θ̂))
- Test de Wald: z = (θ̂-θ₀) · √(n·I(θ̂)) ~ N(0,1) bajo H₀

---

## Invarianza del MLE

**Si θ̂ es MLE de θ, entonces g(θ̂) es MLE de g(θ)**

Ejemplos:
- MLE de λ~Exp es λ̂=1/X̄ → MLE de E[X]=1/λ es X̄
- MLE de p~Bernoulli es p̂=X̄ → MLE de odds p/(1-p) es p̂/(1-p̂)
- MLE de σ² es σ̂² → MLE de σ es √σ̂² = σ̂

---

## Los tres tests asintóticos

Sean H₀:θ=θ₀ vs H₁:θ≠θ₀.

| Test | Estadístico | Distribución bajo H₀ |
|------|-------------|----------------------|
| Wald | (θ̂-θ₀)²·n·I(θ̂) | χ²(1) |
| LRT (razón de veros.) | -2·[ℓ(θ₀)-ℓ(θ̂)] | χ²(1) |
| Score (Rao) | [∂ℓ/∂θ|_{θ₀}]²/(n·I(θ₀)) | χ²(1) |

Los tres son asintóticamente equivalentes bajo H₀ y bajo alternativas locales.

Para r restricciones: sustituir χ²(1) por χ²(r).

---

## Test de razón de verosimilitudes (LRT)

H₀: θ ∈ Θ₀ vs H₁: θ ∈ Θ₁.

**Λ = sup_{θ∈Θ₀} L(θ|x) / sup_{θ∈Θ} L(θ|x)**

**−2 ln Λ →^d χ²(r)** donde r = dim(Θ) − dim(Θ₀)

Λ ∈ (0,1]: cuando Λ es pequeño, los datos son mucho más compatibles con Θ que con Θ₀.

---

## Interpretación geométrica del MLE

La log-verosimilitud ℓ(θ) es una función de θ (no de los datos):
- **Curvatura alta** en θ̂ → información alta → estimación precisa
- **Curvatura baja** → información baja → estimación imprecisa

La matriz de información observada: **J(θ̂) = −∂²ℓ/∂θ²|_{θ=θ̂}**

Aproximación: Var(θ̂) ≈ 1/J(θ̂) (información observada vs. esperada)

---

## MLE para modelos de regresión

Para Y=Xβ+ε con ε~N(0,σ²):

ℓ(β,σ²) = -n/2·ln(σ²) - (Y-Xβ)'(Y-Xβ)/(2σ²)

**Maximizar respecto a β:** ∂ℓ/∂β=0 → X'Xβ = X'Y → **β̂=(X'X)⁻¹X'Y** (OLS)

**Maximizar respecto a σ²:** σ̂²=(Y-Xβ̂)'(Y-Xβ̂)/n (sesgado — divide por n, no n-p)

El OLS = MLE bajo normalidad de los errores.

---

## Verosimilitud perfilada

Cuando el modelo tiene parámetros de interés θ y "nuisance parameters" η:

**L_P(θ) = max_η L(θ,η|x)**

La verosimilitud perfilada solo depende de θ y se puede analizar como si fuera una verosimilitud estándar.

Ejemplo: para N(μ,σ²) con σ² desconocido, la verosimilitud perfilada de μ es proporcional a una t-Student.

---

## Familias exponenciales y el MLE

Para familia exponencial f(x|θ) = h(x)·exp(η(θ)·T(x) − A(θ)):

**Ecuación de verosimilitud: E_θ[T(X)] = (1/n)ΣT(xᵢ)**

El MLE igualal estadístico suficiente T a su valor esperado bajo el modelo. Esto hace que el MLE sea fácil de calcular y que la solución sea única (la log-verosimilitud es cóncava para familias exponenciales canónicas).

---

## Diagnósticos de convergencia del MLE

1. Verifica que ∂²ℓ/∂θ² < 0 en θ̂ (máximo, no mínimo)
2. Verifica que la ecuación de verosimilitud tiene solución única
3. Para el MLE numérico: Newton-Raphson converge cuadráticamente

**Newton-Raphson para el MLE:**
θₙ₊₁ = θₙ − [∂²ℓ/∂θ²]⁻¹ · ∂ℓ/∂θ  evaluado en θₙ

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Maximizar verosimilitud" | Log-verosimilitud → derivar → igualar a 0 |
| "Distribución del MLE" | N(θ, 1/(n·I(θ))) asintóticamente |
| "IC para el MLE" | θ̂ ± z_{α/2}/√(n·I(θ̂)) |
| "Comparar dos modelos anidados" | LRT: -2ΔlnL ~ χ²(r) |
| "MLE de función de θ" | Invarianza: g(θ̂) |
| "OLS bajo normalidad" | β̂=(X'X)⁻¹X'Y es MLE de β |
| "Familia exponencial: MLE" | E_θ[T(X)] = T̄ (estadístico suficiente) |

---

> **Síntesis:** El MLE es la solución a ∂ℓ/∂θ=0. Su distribución asintótica N(θ,1/(nI(θ))) es la base de todos los ICs y tests frecuentistas de gran muestra. Los tres tests asintóticos (Wald, LRT, Score) dan resultados equivalentes para n grande pero difieren en qué necesitan calcular: Wald solo necesita θ̂; LRT necesita ambos θ̂ y θ̂₀; Score solo necesita θ̂₀.

---

*Retrieval: cierra y responde: (1) MLE de λ para n=30 Poissons con ΣxI=90; (2) ecuación de verosimilitud para Exp(λ); (3) por qué σ̂²=Σ(xᵢ-x̄)²/n es sesgado; (4) -2ln(Λ) para LRT → qué distribución.*
