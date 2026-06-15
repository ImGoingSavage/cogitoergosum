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

## Mini-ejemplo trabajado: distribución estacionaria de una cadena 2×2

Dos estados (soleado=1, lluvioso=2) con P = [[0.6, 0.4], [0.2, 0.8]]. La estacionaria π=(π₁,π₂) cumple πP=π. La forma más rápida es el **balance detallado** (vale para 2 estados): π₁·P₁₂ = π₂·P₂₁ → π₁·0.4 = π₂·0.2 → π₁ = ½·π₂. Con π₁+π₂=1:

> π₂ = 2/3, π₁ = 1/3 → **π = (1/3, 2/3)**

A largo plazo el sistema pasa 1/3 del tiempo soleado y 2/3 lluvioso, **sin importar el clima inicial** (la cadena es irreducible y aperiódica). Y el tiempo medio de retorno a "soleado" es 1/π₁ = **3 días**.

**Predicción antes de seguir:** si arrancas 100% seguro de que hoy está soleado, ¿la distribución a 50 pasos depende de ese arranque? Respuesta: **prácticamente no** — converge a (1/3, 2/3). El estado inicial se "olvida" tras el mixing time; esa amnesia es la propiedad de Markov llevada al límite. (Excepción: si la cadena fuera periódica o reducible, el olvido no ocurriría.)

## Prototipo, contraejemplo y caso borde

- **Prototipo:** sistema cuyo futuro depende solo del estado actual → cadena de Markov; busca π con πP=π (o balance detallado).
- **Contraejemplo (no toda π viene de balance detallado):** balance detallado ⟹ estacionariedad, pero no al revés; una cadena con flujo circular (1→2→3→1) puede tener π estacionaria sin ser reversible. Asumir reversibilidad siempre es el error.
- **Caso borde (periódica):** una cadena que alterna 1→2→1→2 tiene π=(½,½) pero Pⁿ **no converge** (oscila); el teorema de convergencia exige aperiodicidad. El borde revela qué hipótesis sostiene "se olvida el inicio".

## Errores típicos

- **Conceptual:** confundir la distribución estacionaria (equilibrio de largo plazo) con la distribución inicial, o creer que toda cadena converge (hace falta irreducible + aperiódica).
- **Técnico:** en Metropolis-Hastings, olvidar el cociente de propuestas q(x|y)/q(y|x) cuando q no es simétrica, rompiendo el balance detallado.
- **De supuestos:** reportar el posterior como si el prior no importara con pocos datos; el prior domina hasta que n crece.

## Transferencia isomorfa

- **Balance detallado de MCMC ↔ estacionariedad por construcción:** la tasa de aceptación de Metropolis está *diseñada* para que π satisfaga balance detallado; muestrear de π difícil = construir una cadena cuyo equilibrio es π.
- **Beta-Binomial conjugado ↔ familia de distribuciones:** el posterior Beta(α+x, β+n−x) es la misma Beta=Gamma-normalizada de antes; conjugación es cerrar la familia bajo actualización (conecta con [[arena-b3]]).
- **Posterior ∝ verosimilitud × prior ↔ Bayes con tasa base:** actualizar creencias sobre θ es el mismo gesto que actualizar odds de enfermedad con un test (conecta con [[arena-q2]]).
- **Propiedad de Markov (estado suficiente) ↔ estado mínimo en sistemas/RL:** "el futuro depende solo del presente" es la definición de un estado bien diseñado en control y en diseño de features (conecta con [[arena-q11]], procesos como el OU, que son markovianos).
- **HMM (estados latentes que evolucionan) ↔ secuencias con estructura oculta:** etiquetado de secuencias y series temporales con régimen oculto comparten el forward-backward.

Moraleja de la arista: *una cadena de Markov olvida su inicio si es irreducible y aperiódica; el equilibrio es π con πP=π; y la inferencia bayesiana es exactamente "actualizar π" con verosimilitud × prior.*

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
