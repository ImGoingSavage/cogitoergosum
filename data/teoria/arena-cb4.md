# Intervalos de confianza, métodos asintóticos y delta method

## Intervalos de confianza: definición

Un intervalo aleatorio [L(X), U(X)] es un **intervalo de confianza (IC) de nivel 1−α** para θ si:

P_θ(L(X) ≤ θ ≤ U(X)) ≥ 1−α para todo θ∈Θ.

Interpretación frecuentista: si repitiéramos el experimento muchas veces, al menos el 100(1−α)% de los intervalos construidos contendrían al verdadero θ.

---

## Pivotes

Un **estadístico pivote** Q(X,θ) tiene distribución que no depende de θ.

Pasos para construir un IC vía pivot:
1. Encuentra Q(X,θ) con distribución conocida (e.g., t, χ², F, U).
2. Halla a, b tales que P(a ≤ Q ≤ b) = 1−α.
3. Despeja θ de a ≤ Q(X,θ) ≤ b.

| Situación | Pivote | IC (1−α) |
|-----------|--------|----------|
| N(μ,σ²), σ² conocida | Z = (X̄−μ)/(σ/√n) ~ N(0,1) | X̄ ± z_{α/2}·σ/√n |
| N(μ,σ²), σ² desconocida | T = (X̄−μ)/(S/√n) ~ t_{n−1} | X̄ ± t_{n−1,α/2}·S/√n |
| N(μ,σ²), para σ² (μ desconocida) | χ² = (n−1)S²/σ² ~ χ²_{n−1} | [(n−1)S²/b, (n−1)S²/a] |
| Uniforme[0,θ] | Y = X_{(n)}/θ ~ Beta(n,1) | [X_{(n)}, X_{(n)}/α^{1/n}] |
| Exponencial(λ), ΣXᵢ | 2λΣXᵢ ~ χ²_{2n} | [χ²_{2n,1-α/2}/(2ΣXᵢ), χ²_{2n,α/2}/(2ΣXᵢ)] |
| Relación F: σ²_X/σ²_Y | F = (S₁²/σ²_X)/(S₂²/σ²_Y) ~ F_{n−1,m−1} | S₁²/(S₂²·F_{upper}), S₁²/(S₂²·F_{lower}) |

---

## IC por inversión de tests

Un IC de nivel 1−α equivale a invertir la familia de tests de nivel α:

C(x) = {θ₀ : test de H₀: θ=θ₀ NO rechaza los datos x}

**Resultado:** Si el test de H₀: θ=θ₀ vs H₁: θ≠θ₀ es de nivel α con región de aceptación A(θ₀), el IC es C(x)={θ₀: x∈A(θ₀)}.

**UMA (Uniformly Most Accurate):** El IC más corto en esperanza se obtiene invirtiendo el test UMP.

| IC | Resultado de invertir |
|----|----------------------|
| Normal una cola: [θ, X̄+z_α σ/√n] | Invierte test UMP de H₀: θ≥θ₀ |
| Normal dos colas | Invierte LRT bilateral |
| Exponencial: [0, 2ΣXᵢ/χ²_{2n,α}] | Invierte test UMP de Poisson/Exp |

---

## IC más corto para pivote continuo

Si Q~f (densidad unimodal y continua), el IC más corto de nivel 1−α con extremos [a,b] satisface:
- ∫_a^b f(q)dq = 1−α
- f(a) = f(b) (densidades iguales en los extremos)

Para densidades **simétricas**: usa a = −b (igual-colas, automáticamente el más corto).

Para densidades **asimétricas** (χ², F, Beta): el IC igual-colas NO es el más corto.

---

## Intervalos de predicción y tolerancia

**Intervalo de predicción** para X_{n+1}: tiene forma X̄ ± t_{n−1,α/2}·S√(1+1/n).

Más largo que el IC para μ: incorpora incertidumbre de la nueva observación.

**Intervalo de tolerancia:** cubre al menos p·100% de la población con confianza 1−α.

---

## Delta method (método delta)

Si √n(θ̂−θ) →_d N(0,σ²) y g es diferenciable en θ con g'(θ)≠0, entonces:

**√n(g(θ̂)−g(θ)) →_d N(0, σ²·[g'(θ)]²)**

Uso inmediato: IC asintótico para g(θ):

g(θ̂) ± z_{α/2}·σ̂·|g'(θ̂)|/√n

| Transformación g | g'(θ) | Aplicación |
|-----------------|-------|------------|
| g(p)=log(p/(1−p)) — logit | 1/(p(1−p)) | CI para el logit de una proporción |
| g(λ)=√λ — raíz Poisson | 1/(2√λ) | Estabiliza varianza de Poisson |
| g(r)=arctanh(r) — correlación | 1/(1−r²) | Transformación de Fisher para ρ |
| g(μ)=1/μ — recíproca | −1/μ² | IC para 1/E(X) |

---

## Consistencia y normalidad asintótica del MLE

Para familias regulares con muestra i.i.d.:

1. **Consistencia:** θ̂_MLE →_P θ
2. **Normalidad asintótica:** √n(θ̂_MLE−θ) →_d N(0, 1/I(θ))
3. **IC asintótico:** θ̂ ± z_{α/2}/√(n·Î(θ̂))

donde Î es la información observada: Î(θ̂) = −(1/n)Σ∂² log f(xᵢ|θ̂)/∂θ².

---

## Bonferroni y métodos de inferencia simultánea

Para k parámetros simultáneos con IC individuales de nivel 1−αᵢ:

P(todos los CI contienen su parámetro) ≥ 1 − Σαᵢ

Regla de Bonferroni: usa αᵢ = α/k en cada IC para garantizar nivel 1−α conjunto.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "IC para μ normal, σ desconocida" | Pivot t_{n−1}: X̄ ± t_{n−1,α/2}·S/√n |
| "IC más corto para distribución asimétrica" | Condición f(a)=f(b) con ∫=1−α |
| "IC para transformación de parámetro" | Delta method: ± z_{α/2}·σ̂|g'(θ̂)|/√n |
| "IC para μ cuando solo tenemos MLE" | CI asintótico vía información de Fisher |
| "Dos parámetros simultáneamente" | Bonferroni con αᵢ=α/2 en cada uno |
| "IC invirtiendo un test" | C(x)={θ₀: x∈región de aceptación de H₀:θ=θ₀} |

---

> **Síntesis (Casella & Berger, Ch 9−10):** El pivote convierte una distribución conocida en un IC exacto. La inversión de tests alinea IC con tests: el IC más corto viene del test UMP. El delta method es el puente universal cuando no hay pivote exacto — basta que el MLE sea √n-consistente y g sea derivable.

---

*Retrieval: (1) X₁,…,Xₙ i.i.d. Uniform[0,θ]. Da un IC exacto de nivel 0.95 para θ usando el pivot Y=X_{(n)}/θ. (2) Enuncia el delta method. (3) ¿Qué IC resulta de invertir el test t unilateral? (4) ¿Cómo difieren el IC de predicción y el IC para μ?*
