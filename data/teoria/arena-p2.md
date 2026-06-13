# Combinatoria y probabilidad discreta

## Caminos en retícula

De (0,0) a (m,n) moviéndose solo derecha (+1,0) o arriba (0,+1):

**Número de caminos = C(m+n, n)**

Argumento: hay m+n pasos en total; elegir cuáles n son "arriba" determina el camino.

Para (4,3): C(7,3) = **35**.

Con obstáculos: usa programación dinámica (DP) o el principio de reflexión.

---

## Técnica del complemento

P(al menos uno) = 1 − P(ninguno).

Casi siempre más fácil que inclusión-exclusión directa.

Ejemplo — P(al menos un as en 5 cartas):
= 1 − C(48,5)/C(52,5) = 1 − 0.6588 = **0.3412**

---

## Stars and bars

Soluciones enteras no negativas de x₁ + x₂ + … + xₖ = n:

**C(n+k−1, k−1)**

Con xᵢ ≥ 1: substituye yᵢ = xᵢ−1 → Σyᵢ = n−k → C(n−1, k−1).

Para x₁+x₂+x₃+x₄=10, xᵢ≥0: C(13,3) = **286**.
Con xᵢ≥1: C(9,3) = **84**.

---

## Permutaciones con repetición

n objetos con multiplicidades n₁,n₂,…,nₖ (Σnᵢ=n):

**n! / (n₁!·n₂!·…·nₖ!)**

MISSISSIPPI: 11!/(1!·4!·4!·2!) = **34650**.

---

## Desarreglos (derangements)

Permutación sin puntos fijos:

**D(n) = n! · Σ_{k=0}^{n} (−1)^k/k!**

| n | D(n) |
|---|------|
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 9 |

D(n)/n! → **e^{−1} ≈ 0.3679** cuando n→∞.

Aproximación para n≥3: D(n) ≈ round(n!/e).

---

## Estadísticas de orden de uniformes discretas

n extracciones con reemplazo de {1,…,N}:

**E[X_(k)] = k(N+1)/(n+1)** (k-ésimo estadístico de orden)

E[mínimo] = (N+1)/(n+1); E[máximo] = n(N+1)/(n+1).

Para n=3, N=10: E[máx] = 3×11/4 = **8.25**.

---

## Ruina del jugador

Barreras en 0 y N, inicio en k, P(subir) = p.

| Caso | P(llegar a N) | E[duración] |
|------|--------------|-------------|
| p = 1/2 | k/N | k(N−k) |
| p ≠ 1/2 | (1−ρᵏ)/(1−ρᴺ) donde ρ=q/p | más compleja |

Para p=0.45, N=10, k=5: ρ=11/9; P₅ ≈ **32.8%** (vs 50% si p=0.5).

Una pequeña desventaja compuesta es devastadora.

---

## Aproximación de Poisson

Bin(n,p) ≈ Poisson(λ) con λ=np cuando n grande, p pequeño.

P(X=k) = e^{−λ}λ^k/k!; E[X] = Var[X] = λ.

Para n=1000, p=0.003: λ=3; P(0 defectos) = e^{-3} ≈ **4.98%**.

Poisson es el modelo por defecto para eventos raros e independientes.

---

## Distribución exponencial — falta de memoria

P(X > s+t | X > s) = P(X > t).

La única distribución continua con esta propiedad (análogo discreto: geométrica).

Si X ~ Exp(λ), Y ~ Exp(μ) independientes:
- P(X < Y) = **λ/(λ+μ)**
- min(X,Y) ~ **Exp(λ+μ)**

---

## Orden estadístico de uniformes continuas

X₁,…,Xₙ i.i.d. Uniform[0,1]:

**E[X_(k)] = k/(n+1)**

Los n puntos dividen [0,1] en n+1 intervalos de longitud esperada igual 1/(n+1).

---

## Desigualdades probabilísticas

| Desigualdad | Enunciado | Supuesto |
|------------|-----------|---------|
| Markov | P(X≥a) ≤ E[X]/a | X≥0 |
| Chebyshev | P(\|X−μ\|≥kσ) ≤ 1/k² | Var(X)<∞ |
| Jensen | E[f(X)] ≥ f(E[X]) si f convexa | — |

P(\|X−μ\|≥2σ) ≤ 1/4 = 25% (para la normal: ≈4.6%).

Jensen → E[e^X] ≥ e^{E[X]}; E[X²] ≥ (E[X])².

---

## Coleccionista de cupones (n tipos)

**E[T] = n·Hₙ = n·(1 + 1/2 + … + 1/n)**

Para n=6: E[T] = 6×(1+0.5+0.333+0.25+0.2+0.167) ≈ **14.7**.

En etapa k (ya tienes k distintos): probabilidad de nuevo tipo = (n−k)/n → espera n/(n−k).

---

## Competencia de exponenciales

X ~ Exp(λ), Y ~ Exp(μ), independientes:

- **min(X,Y) ~ Exp(λ+μ)**: las tasas suman.
- **P(X < Y) = λ/(λ+μ)**: proporcional a la tasa propia.
- X e Y son independientes conditional en min(X,Y).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Caminos en retícula m×n | C(m+n, n) |
| "Al menos uno" | Complemento: 1 − P(ninguno) |
| Enteros xᵢ≥0 sumando n en k variables | C(n+k−1, k−1) |
| Permutaciones sin punto fijo | D(n) ≈ round(n!/e) |
| E[max de n draws de {1..N}] | n(N+1)/(n+1) |
| Paseo entre 0 y N, p=1/2 | P(N) = k/N; duración = k(N−k) |
| Eventos raros (n grande, p pequeño) | Poisson con λ=np |
| Dos exponenciales compiten | P(X<Y) = λ/(λ+μ); min ~ Exp(λ+μ) |
| Coleccionar n tipos | E[T] = n·Hₙ |

---

> **Síntesis:** La combinatoria y la probabilidad discreta son un catálogo de modelos bien definidos: retícula (C(m+n,n)), desarreglos (1/e), ruina (k/N), Poisson (eventos raros), exponencial (competencia de procesos). Reconocer el modelo correcto reduce el problema a una fórmula; el esfuerzo está en el reconocimiento, no en el cálculo.

---

*Retrieval: sin mirar: (1) caminos de (0,0) a (3,3); (2) P(X<Y) si X~Exp(2), Y~Exp(3); (3) E[máx de 4 draws de {1..10}]; (4) D(5).*
