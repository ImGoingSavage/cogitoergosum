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

## Mini-ejemplo trabajado: "al menos un as" por complemento

P(al menos un as en 5 cartas de una baraja de 52). Contar directamente "exactamente 1, 2, 3, 4 ases" y sumar es laborioso. El complemento lo vuelve trivial:

> P(al menos uno) = 1 − P(ninguno) = 1 − C(48,5)/C(52,5) = 1 − 0.6588 = **0.3412**

C(48,5) cuenta las manos sin ningún as; dividir entre todas las manos da P(ninguno), y 1 menos eso es la respuesta. Un solo cociente en vez de cuatro sumandos.

**Predicción antes de seguir:** ¿cuándo el complemento NO ayuda? Respuesta: cuando "ninguno" es tan complejo como "al menos uno" — por ejemplo, "exactamente 2 ases" no tiene complemento simple. La regla: el complemento brilla para "al menos uno / al menos un éxito", porque "ninguno" suele ser un producto limpio de probabilidades. Reconocer la forma "al menos uno" es la señal.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** reconoce el modelo → retícula C(m+n,n), stars and bars C(n+k−1,k−1), ruina k/N, Poisson(np), competencia de exponenciales.
- **Contraejemplo (ruina con desventaja):** con p=0.45 (no 0.5), P(llegar a N) no es k/N sino (1−ρᵏ)/(1−ρᴺ) con ρ=q/p; una desventaja del 5% compuesta es devastadora (32.8% vs 50%).
- **Caso borde (exponencial sin memoria):** P(X>s+t|X>s)=P(X>t); el tiempo ya esperado no cambia el restante. La única continua con esa propiedad — el borde la define.

## Errores típicos

- **Conceptual:** usar la fórmula simétrica k/N de la ruina cuando el juego no es justo (p≠½).
- **Técnico:** en stars and bars, confundir el caso xᵢ≥0 (C(n+k−1,k−1)) con xᵢ≥1 (C(n−1,k−1)).
- **De supuestos:** aproximar Bin(n,p) por Poisson cuando p no es pequeño (la aproximación pide n grande, p chico, λ=np moderado).

## Transferencia isomorfa

- **Complemento "al menos uno" ↔ palomar y conteo:** 1−P(ninguno) es el mismo atajo que resuelve garantías y coincidencias (conecta con [[arena-fc1]]).
- **Derangements (D(n)/n!→1/e) ↔ puntos fijos y el secretario:** el 1/e reaparece en sombreros y parada óptima (conecta con [[arena-fc1]]).
- **Ruina del jugador ↔ muestreo opcional / barreras:** P(absorción) lineal en p=½ sale del argumento de martingala (conecta con [[arena-q11]] y [[arena-fc4]]).
- **min(X,Y)~Exp(λ+μ), P(X<Y)=λ/(λ+μ) ↔ proceso de Poisson:** competir exponenciales es el mecanismo de las llegadas y la Gamma (conecta con [[arena-b3]] y [[arena-ads1]]).
- **Coleccionista n·Hₙ ↔ récords y caché:** el número armónico cuenta cupones, récords y cobertura (conecta con [[arena-q6]]).

Moraleja de la arista: *el trabajo está en reconocer el modelo, no en calcular; "al menos uno" pide complemento, y una desventaja compuesta en la ruina es letal.*

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
