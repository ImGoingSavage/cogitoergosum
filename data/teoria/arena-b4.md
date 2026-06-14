# Cadenas de Markov e inferencia bayesiana

## Cadenas de Markov — definición

**Propiedad de Markov:** P(Xₙ₊₁=j | X₀=i₀,...,Xₙ=iₙ) = P(Xₙ₊₁=j | Xₙ=iₙ)

El futuro es condicionalmente independiente del pasado dado el presente.

Una cadena de Markov de tiempo discreto queda determinada por:
1. Espacio de estados S = {s₁, s₂, ...}
2. Distribución inicial π₀
3. Matriz de transición P donde Pᵢⱼ = P(Xₙ₊₁=j | Xₙ=i)

Cada fila de P suma 1 (matriz estocástica por filas).

---

## n pasos y la distribución de Xₙ

P(Xₙ=j | X₀=i) = (Pⁿ)ᵢⱼ — potencia n-ésima de la matriz de transición.

La distribución de Xₙ es π₀·Pⁿ (vector fila).

---

## Distribución estacionaria

π es **estacionaria** si **πP = π** y Σπᵢ=1.

Método para encontrarla:
1. Escribe el sistema πP=π (o balance detallado)
2. Añade la condición Σπᵢ=1
3. Resuelve el sistema lineal (n−1 ecuaciones + normalización)

**Balance detallado** (condición suficiente para estacionariedad):
πᵢ·Pᵢⱼ = πⱼ·Pⱼᵢ para todo i,j

Balance detallado ⟹ πP=π (pero no al revés).

---

## Convergencia y mixing

**Teorema:** Si la cadena es **irreducible** (conectada: de cualquier estado puedes llegar a cualquier otro) y **aperiódica** (mcd de tiempos de retorno = 1), entonces:

Pⁿᵢⱼ → πⱼ cuando n→∞ (independientemente del estado inicial)

**Período de un estado:** mcd{n: Pⁿᵢᵢ > 0}.

Una cadena con un estado con un auto-loop (Pᵢᵢ > 0) es aperiódica.

**Tiempo de retorno esperado:** E[Tᵢ] = 1/πᵢ.

**Mixing time:** número de pasos para que la distribución sea ε-cercana (en variación total) a π.

---

## MCMC — Metropolis-Hastings

Objetivo: muestrear de una distribución π difícil de normalizar.

**Algoritmo:**
1. En estado x, propón y ~ q(y|x) (distribución de propuesta)
2. Acepta y con probabilidad α = min(1, π(y)q(x|y)/(π(x)q(y|x)))
3. Si rechazas, quédate en x

**Por qué funciona:** la tasa de aceptación garantiza balance detallado → π es estacionaria.

Si q es simétrica (q(y|x)=q(x|y)): **α = min(1, π(y)/π(x))** (Metropolis clásico).

No necesitas normalizar π — solo calcular π(y)/π(x).

---

## Inferencia bayesiana — fundamentos

**Teorema de Bayes:**
**P(θ|datos) ∝ P(datos|θ) · P(θ)**

Posterior ∝ verosimilitud × prior

| Término | Nombre | Rol |
|---------|--------|-----|
| P(θ) | Prior | Creencia antes de los datos |
| P(datos|θ) | Verosimilitud | Cómo los datos dependen de θ |
| P(θ|datos) | Posterior | Creencia actualizada |
| P(datos) | Evidencia | Normalización (a menudo ignorada) |

---

## Conjugate priors

Un prior es **conjugado** para una verosimilitud si el posterior tiene la misma forma funcional.

| Verosimilitud | Prior conjugado | Posterior |
|--------------|----------------|----------|
| Bin(n,p) | Beta(α,β) | Beta(α+x, β+n−x) |
| Poisson(λ) | Gamma(α,β) | Gamma(α+Σxᵢ, β+n) |
| Normal(μ,σ²) — μ desconocida | N(μ₀,τ²) | N(μₙ,τₙ²) |
| Bernoulli(p) | Beta(α,β) | Beta(α+x, β+1−x) |

**Interpretación de Beta(α,β):** α = éxitos previos, β = fracasos previos (pseudo-counts).

---

## Beta-Binomial (el caso más importante)

Prior: p ~ Beta(α,β)
Datos: X|p ~ Bin(n,p)
**Posterior: p|X ~ Beta(α+X, β+n−X)**

**E[p|X] = (α+X)/(α+β+n)**

Para α=β=1 (prior uniforme): E[p|X] = (X+1)/(n+2) (ley de sucesión de Laplace).

Con muchos datos (n grande): la media posterior → X/n (MLE domina el prior).

---

## Normal-Normal conjugado

Prior: μ ~ N(μ₀, τ²)
Datos: X₁,...,Xₙ|μ ~ N(μ, σ²) i.i.d.
**Posterior: μ|datos ~ N(μₙ, τₙ²)**

Donde:
- 1/τₙ² = 1/τ² + n/σ²
- μₙ = τₙ² · (μ₀/τ² + nX̄/σ²)

Interpretación: la media posterior es el promedio ponderado de prior y datos (ponderado por precisiones).

---

## Estimadores bayesianos

| Pérdida | Estimador de Bayes |
|---------|-------------------|
| Cuadrática (θ-δ)² | Media posterior E[θ|datos] |
| Absoluta |θ-δ| | Mediana posterior |
| 0-1 (I(δ≠θ)) | Moda posterior (MAP) |

**MAP (Maximum A Posteriori):** maximiza P(θ|datos) ∝ P(datos|θ)·P(θ). Con prior uniforme: MAP = MLE.

---

## Modelo gráfico y cadenas de Markov ocultas

En un HMM (Hidden Markov Model):
- Estados ocultos X₁,X₂,... siguen una cadena de Markov
- Observaciones Yₜ ~ P(Y|Xₜ) condicionalmente independientes dado Xₜ

Algoritmos:
- Forward-Backward: P(Xₜ|Y₁,...,Yₙ)
- Viterbi: argmax P(X₁,...,Xₙ|Y₁,...,Yₙ)
- Baum-Welch (EM): estima parámetros

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿Cuándo converge la cadena?" | Irreducible + aperiódica |
| "E[tiempo de retorno al estado i]" | 1/πᵢ |
| "Muestrear de distribución difícil" | Metropolis-Hastings |
| "Prior para proporción + datos binomiales" | Beta conjugado |
| "Actualizar media con datos normales" | Normal-Normal conjugado |
| "Posterior con muchos datos" | Domina el prior → ≈ MLE |
| "Estimador bajo pérdida cuadrática" | Media posterior |
| "MAP con prior uniforme" | MAP = MLE |

---

> **Síntesis:** Las cadenas de Markov modelan sistemas donde el pasado solo importa a través del estado actual — memoria de primer orden. La distribución estacionaria es el equilibrio de largo plazo; el mixing time es cuánto tardas en llegar. La inferencia bayesiana es actualización de creencias vía Bayes: los conjugate priors hacen el cálculo analítico; MCMC lo hace numéricamente cuando no hay forma cerrada.

---

*Retrieval: cierra y responde: (1) distribución estacionaria para P=[[0.6,0.4],[0.2,0.8]]; (2) posterior de p después de Beta(3,3) + 4 éxitos en 10; (3) E[p|datos] en la respuesta anterior; (4) tasa de aceptación de Metropolis para pasar de estado con π=0.3 a estado con π=0.6.*
