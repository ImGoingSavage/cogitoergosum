# Variables aleatorias conjuntas y correlación

## Distribuciones conjuntas, marginales y condicionales

**Función de masa conjunta (discreta):** p_{X,Y}(x,y) = P(X=x, Y=y)

**Marginales:** p_X(x) = Σ_y p_{X,Y}(x,y) — suma sobre todos los y

**Condicional:** p_{Y|X}(y|x) = p_{X,Y}(x,y)/p_X(x)

**Independencia:** X⊥Y ↔ p_{X,Y}(x,y) = p_X(x)·p_Y(y) para todo (x,y)

Caso continuo: reemplaza sumas por integrales. La condición de independencia es igual: f_{X,Y}(x,y) = f_X(x)·f_Y(y).

---

## Normal bivariada

Si (X,Y) ~ Normal bivariada con medias μ_X,μ_Y, varianzas σ²_X,σ²_Y y correlación ρ:

**E[Y|X=x] = μ_Y + ρ·(σ_Y/σ_X)·(x − μ_X)**

La regresión condicional es **lineal** en x con pendiente ρ·σ_Y/σ_X.

Para X,Y estándar (μ=0, σ=1): **E[Y|X=x] = ρx**

Propiedad especial de la normal bivariada: Cov=0 ↔ X⊥Y.

---

## Covarianza y correlación

**Cov(X,Y) = E[XY] − E[X]·E[Y] = E[(X−μ_X)(Y−μ_Y)]**

**ρ(X,Y) = Cov(X,Y) / (σ_X·σ_Y) ∈ [−1,1]**

| Propiedad | Fórmula |
|-----------|---------|
| Cov(aX+b, cY+d) | ac·Cov(X,Y) |
| Var(X+Y) | Var(X)+Var(Y)+2Cov(X,Y) |
| X⊥Y ⟹ | Cov=0 (no al revés en general) |

**Atención:** Cov=0 no implica independencia. Contraejemplo: X~Unif(−1,1), Y=X². Cov(X,Y)=E[X³]=0 pero Y es función determinista de X.

---

## Ley de la Esperanza Total (LET)

**E[Y] = E[E[Y|X]]**

Dem: E[E[Y|X]] = Σₓ E[Y|X=x]·P(X=x) = Σₓ Σ_y y·P(Y=y|X=x)·P(X=x) = Σ_y y·P(Y=y) = E[Y].

Estrategia: elige X tal que E[Y|X=x] sea simple de calcular. Luego promedia sobre X.

Ejemplo — Y=número de caras al lanzar X monedas (X=dado):
E[Y|X=x]=x/2 → E[Y]=E[X/2]=E[X]/2=(7/2)/2=**7/4**.

---

## Ley de la Varianza Total (LVT)

**Var[Y] = E[Var[Y|X]] + Var[E[Y|X]]**

| Componente | Nombre | Significado |
|------------|--------|-------------|
| E[Var[Y|X]] | Varianza residual promedio | Ruido que X no explica |
| Var[E[Y|X]] | Varianza de las medias | Variación que X sí explica |

Analogía ANOVA: SS_total = SS_within + SS_between.

Ejemplo continuado (monedas y dado):
Var[Y|X=x]=x/4 → E[Var[Y|X]]=E[X]/4=7/8.
E[Y|X=x]=x/2 → Var[E[Y|X]]=Var[X/2]=Var[X]/4=(35/12)/4=35/48.
Var[Y] = 7/8 + 35/48 = 42/48 + 35/48 = **77/48**.

---

## Momentos y función generatriz de momentos (mgf)

M_X(t) = E[e^{tX}] (existe en entorno de t=0 para muchas distribuciones)

**E[Xⁿ] = M_X^{(n)}(0)** (n-ésima derivada evaluada en 0)

**Sumas independientes:** M_{X+Y}(t) = M_X(t)·M_Y(t)

| Distribución | M_X(t) |
|-------------|--------|
| N(μ,σ²) | e^{μt+σ²t²/2} |
| Poisson(λ) | e^{λ(e^t−1)} |
| Exp(λ) | λ/(λ−t) para t<λ |
| Bin(n,p) | (pe^t+1−p)^n |

**E[e^X] para X~N(μ,σ²):** M(1) = **e^{μ+σ²/2}**

---

## Distribución chi-cuadrado

Si X₁,…,Xₙ ~ N(0,1) i.i.d., entonces **X₁²+…+Xₙ² ~ χ²(n)**

χ²(n) = Gamma(n/2, 1/2). E[χ²(n)]=n, Var[χ²(n)]=2n.

Si X ~ N(0,1), entonces **X² ~ χ²(1)**.

Para X ~ N(μ,σ²): **((X−μ)/σ)² ~ χ²(1)**.

En estimación: **(n−1)S²/σ² ~ χ²(n−1)** para muestra normal (n−1 grados de libertad).

---

## Propiedades de la distribución normal

Si X ~ N(μ,σ²):
- aX+b ~ N(aμ+b, a²σ²)
- Si Y ~ N(ν,τ²) independiente: X+Y ~ N(μ+ν, σ²+τ²)
- Momentos: E[X^{2k}] = σ^{2k}·(2k-1)!! donde (2k-1)!!=1·3·5·…·(2k-1)

Para X ~ N(0,1):
- E[X²]=1, E[X⁴]=3, E[X⁶]=15
- E[|X|] = √(2/π) ≈ 0.798

---

## Estadísticos de orden

X₁,…,Xₙ i.i.d. Uniform[0,1]. Ordenados: X₍₁₎≤X₍₂₎≤…≤X₍ₙ₎.

**E[X₍ₖ₎] = k/(n+1)**

Los n puntos dividen [0,1] en n+1 intervalos de longitud esperada 1/(n+1) cada uno.

Para n=4: E[X₍₁₎]=1/5, E[X₍₂₎]=2/5, E[X₍₃₎]=3/5, E[X₍₄₎]=4/5.

---

## Desigualdades

| Desigualdad | Enunciado |
|------------|-----------|
| Markov | P(X≥a) ≤ E[X]/a para X≥0 |
| Chebyshev | P(|X−μ|≥kσ) ≤ 1/k² |
| Jensen | E[f(X)] ≥ f(E[X]) si f convexa |
| Cauchy-Schwarz | (E[XY])² ≤ E[X²]·E[Y²] |

Jensen implica: E[X²] ≥ (E[X])², E[e^X] ≥ e^{E[X]}, E[1/X] ≥ 1/E[X] (para X>0).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "E[Y] donde Y depende de X random" | LET: E[E[Y|X]] |
| "Var[Y] con mezcla de fuentes" | LVT: E[Var[Y|X]] + Var[E[Y|X]] |
| "E[e^X] para X normal" | mgf en t=1: e^{μ+σ²/2} |
| "Suma de cuadrados de normales" | Chi-cuadrado: χ²(n) |
| "Cov=0, ¿independencia?" | Solo para normal bivariada; en general no |
| "E[Y|X] para normal bivariada" | μ_Y + ρ(σ_Y/σ_X)(x−μ_X) |
| "E[k-ésimo estadístico de orden de Unif]" | k/(n+1) |

---

> **Síntesis:** LET y LVT son las herramientas para calcular E y Var de variables que dependen de otra aleatoria — "condiciona en lo que sabe más y luego promedia". La mgf codifica todos los momentos y convierte la convolución en multiplicación. Chi-cuadrado surge naturalmente de cuadrados de normales, base de toda la inferencia clásica.

---

*Retrieval: cierra y responde: (1) E[Y] y Var[Y] para Y=suma de N monedas con N~Poisson(5); (2) E[e^{2X}] para X~N(3,4); (3) E[X₍₃₎] para 5 Unif[0,1]; (4) Cov(X,Y) si Var[X+Y]=10, Var[X]=4, Var[Y]=3.*
