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

## Mini-ejemplo trabajado: un estimador sesgado puede ganar (MSE)

Estima la varianza σ² de una normal con n=5 datos. Dos candidatos:
- **Insesgado** S² = Σ(xᵢ−x̄)²/(n−1). Bias=0, pero Var grande.
- **MLE** σ̂² = Σ(xᵢ−x̄)²/n (divide por n). Tiene Bias<0 (subestima), pero menor Var.

Como **MSE = Var + Bias²**, un poco de sesgo a cambio de mucha menos varianza puede bajar el MSE total. De hecho, el estimador de mínimo MSE para σ² en la normal divide por **n+1**, ¡más sesgado aún que el MLE! Ninguno es "el correcto": depende de qué penalizas.

**Predicción antes de seguir:** si te obsesionas con insesgamiento (Bias=0) y eliges siempre S², ¿garantizas el menor error de estimación? Respuesta: **no**. Insesgado solo significa que aciertas *en promedio sobre muchas muestras*; en una muestra concreta, un estimador con sesgo pequeño y varianza baja suele estar más cerca de σ². El sesgo no es el enemigo; el MSE es lo que importa. Esa es la semilla del trade-off sesgo–varianza de todo ML.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** comparar estimadores por MSE = Var + Bias²; el que domina para todo θ es preferible.
- **Contraejemplo (insesgado ≠ mejor):** X̄ es insesgado para μ, pero en Cauchy tiene varianza infinita y la mediana lo aplasta. Insesgado y útil no son lo mismo.
- **Caso borde (suficiencia en Uniforme[0,θ]):** aquí el suficiente no es X̄ sino el **máximo** X₍ₙ₎. El borde rompe la intuición "promedia siempre": la última observación (la mayor) contiene toda la información de θ.

## Errores típicos

- **Conceptual:** creer que insesgado implica bajo error; ignora la varianza (y el MSE).
- **Técnico:** olvidar que la información de Fisher es aditiva (Iₙ=n·I), y mal-escalar la cota de Cramér-Rao.
- **De supuestos:** aplicar Lehmann-Scheffé sin verificar *completitud* del estadístico suficiente (suficiente solo no basta para UMVUE).

## Transferencia isomorfa

- **MSE = Var + Bias² ↔ trade-off sesgo-varianza en ML:** el mismo desglose gobierna por qué un modelo flexible (baja sesgo, alta varianza) puede generalizar peor que uno simple (conecta con [[arena-iml4]]).
- **Estadístico suficiente ↔ compresión de features / estado mínimo:** T(X) resume los datos sin perder información sobre θ, igual que un buen embedding o un estado markoviano resume la historia (conecta con [[arena-b4]]).
- **Rao-Blackwell (condiciona en T) ↔ promediar para reducir varianza:** "E[θ̂|T] nunca empeora" es la versión teórica de ensamblar/bagging para bajar varianza.
- **Mediana vs media en colas pesadas ↔ robustez:** cuando hay Cauchy/outliers, la mediana (más eficiente) gana a X̄ (conecta con [[arena-q11]]).

Moraleja de la arista: *no persigas insesgamiento; persigue MSE bajo. Var + Bias² es el mismo trade-off que decide si un modelo generaliza.*

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
