# Máxima verosimilitud y familias exponenciales

## De qué trata esta lección (y qué sabrás hacer al final)

El **MLE** (estimador de máxima verosimilitud) es el caballo de batalla de la estadística: una receta casi automática que, ante cualquier modelo, te da el parámetro "que mejor explica los datos". Esta lección lo construye desde cero —qué es la verosimilitud, cómo se maximiza, por qué su distribución es normal con $n$ grande— y muestra por qué en las **familias exponenciales** todo sale limpio. También conecta dos cosas que parecían ajenas: el MLE bajo errores normales **es** la regresión por mínimos cuadrados.

Al terminar podrás: (1) plantear y resolver la ecuación de verosimilitud para distribuciones comunes; (2) usar la invarianza del MLE para estimar $g(\theta)$ sin re-optimizar; (3) reconocer los tres tests asintóticos (Wald, LRT, Score) y cuándo usar cada uno; y (4) ver el OLS como un MLE. La intuición primero; la fórmula, cuando aclara. Para la equivalencia asintótica de los tests uso `[CAJA NEGRA OK]`.

> Esta lección profundiza el MLE que [[arena-dg1]] introdujo. Si "verosimilitud", "información de Fisher" o "estadístico suficiente" te suenan nuevos, empieza por ahí.

---

## La función de verosimilitud

La idea raíz: **dado lo que observé, ¿qué valor de $\theta$ lo hace más probable?** Si lanzaste 10 monedas y salieron 7 caras, el $p$ que mejor lo explica es 0.7. Formalizamos esa pregunta con la **verosimilitud**: la densidad conjunta de los datos, pero leída como función de $\theta$ (los datos quedan fijos):

$$L(\theta\mid x) = \prod_{i=1}^n f(x_i\mid\theta).$$

Como multiplicar muchos términos es incómodo (y numéricamente traicionero), se trabaja con su logaritmo, que convierte el producto en suma —y como el log es creciente, maximizar una o la otra da el mismo $\theta$:

$$\ell(\theta\mid x) = \sum_{i=1}^n \ln f(x_i\mid\theta).$$

El **MLE** es el punto que maximiza esa log-verosimilitud, $\hat\theta=\arg\max_\theta \ell(\theta\mid x)$. Cuando el máximo es interior y la curva es suave, se halla derivando e igualando a cero — la **ecuación de verosimilitud**:

$$\frac{\partial\ell}{\partial\theta}=0.$$

Cuidado conceptual clave: $L(\theta)$ **no** es una densidad de probabilidad de $\theta$ (no integra a 1 sobre $\theta$). Es "compatibilidad de cada $\theta$ con los datos". El MLE no es una probabilidad.

---

## MLE para distribuciones comunes

| Distribución | Log-verosimilitud (esquema) | MLE |
|-------------|-------------------|-----|
| Bernoulli$(p)$ | $(\sum x)\ln p+(n-\sum x)\ln(1-p)$ | $\hat p=\bar X$ |
| Poisson$(\lambda)$ | $-n\lambda+(\sum x)\ln\lambda$ | $\hat\lambda=\bar X$ |
| $N(\mu,\sigma^2)$ | $-\tfrac n2\ln\sigma^2-\tfrac{\sum(x-\mu)^2}{2\sigma^2}$ | $\hat\mu=\bar X;\ \hat\sigma^2=\tfrac1n\sum(x-\bar X)^2$ |
| Exp$(\lambda)$ | $n\ln\lambda-\lambda\sum x$ | $\hat\lambda=1/\bar X$ |

Mira el patrón: casi todos los MLE son **el promedio** (o una función simple de él). No es coincidencia; lo explica la sección de familias exponenciales. **Nota importante:** el MLE de $\sigma^2$ divide por $n$ y es **sesgado** (subestima); la varianza muestral $S^2$ divide por $n-1$ y es insesgada. El MLE es óptimo asintóticamente, no necesariamente insesgado en muestra finita.

---

## Propiedades asintóticas del MLE

Esta es la razón por la que el MLE domina la práctica. Con $n$ grande y condiciones de regularidad, el MLE se distribuye **normal alrededor del valor real**, con varianza igual al inverso de la información de Fisher:

$$\sqrt{n}\,(\hat\theta_{\text{MLE}}-\theta)\xrightarrow{d}N\!\Big(0,\ \tfrac{1}{I(\theta)}\Big), \qquad\text{o sea}\qquad \hat\theta_{\text{MLE}}\ \approx\ N\!\Big(\theta,\ \tfrac{1}{n\,I(\theta)}\Big).$$

Reconoce las piezas: el centro es el valor verdadero $\theta$ (consistencia), y la varianza $1/(nI(\theta))$ es **justo la cota de Cramér-Rao** (eficiencia asintótica, ver [[arena-dg1]]). De aquí salen, casi gratis, dos herramientas:

- **Intervalo de confianza** del $(1-\alpha)$: $\ \hat\theta \pm z_{\alpha/2}\,/\sqrt{n\,I(\hat\theta)}$.
- **Test de Wald** para $H_0:\theta=\theta_0$: $\ z=(\hat\theta-\theta_0)\sqrt{n\,I(\hat\theta)}\sim N(0,1)$ bajo $H_0$.

---

## Invarianza del MLE

Una propiedad de oro por lo barata: **si $\hat\theta$ es el MLE de $\theta$, entonces $g(\hat\theta)$ es el MLE de $g(\theta)$**, para cualquier función $g$. No hay que volver a optimizar; enchufas el MLE en $g$.

- MLE de $\lambda$ en Exp es $\hat\lambda=1/\bar X$ → MLE de la media $E[X]=1/\lambda$ es $\bar X$.
- MLE de $p$ es $\bar X$ → MLE de los *odds* $p/(1-p)$ es $\bar X/(1-\bar X)$.
- MLE de $\sigma^2$ es $\hat\sigma^2$ → MLE de $\sigma$ es $\sqrt{\hat\sigma^2}$.

(La media posterior bayesiana **no** tiene esta propiedad: $E[g(\theta)]\ne g(E[\theta])$ en general. Es parte de por qué el MLE es tan cómodo.)

---

## Los tres tests asintóticos

Para contrastar $H_0:\theta=\theta_0$ contra $H_1:\theta\ne\theta_0$ hay tres estadísticos clásicos, y la gracia es **qué mide cada uno sobre la colina de la log-verosimilitud**:

| Test | Mide… | Estadístico | Distribución bajo $H_0$ |
|------|-------|-------------|----------------------|
| **Wald** | qué tan lejos cae $\hat\theta$ del pico de $\theta_0$ | $(\hat\theta-\theta_0)^2\,n\,I(\hat\theta)$ | $\chi^2(1)$ |
| **LRT** | cuánto baja la colina de $\hat\theta$ a $\theta_0$ | $-2[\ell(\theta_0)-\ell(\hat\theta)]$ | $\chi^2(1)$ |
| **Score (Rao)** | qué tan inclinada está la colina en $\theta_0$ | $[\partial\ell/\partial\theta\,|_{\theta_0}]^2/(n\,I(\theta_0))$ | $\chi^2(1)$ |

`[CAJA NEGRA OK]` — *Qué asumir:* que los tres son asintóticamente equivalentes bajo $H_0$ y bajo alternativas locales. *Qué sí razonar:* su geometría y su coste de cómputo: Wald solo necesita $\hat\theta$; el Score solo necesita $\theta_0$ (útil cuando $\hat\theta$ es caro de calcular); el LRT necesita **ambos**. Para $r$ restricciones, se cambia $\chi^2(1)$ por $\chi^2(r)$.

---

## Test de razón de verosimilitudes (LRT)

El más usado para **comparar modelos anidados** (un modelo simple $\Theta_0$ dentro de uno general $\Theta$). Compara la mejor verosimilitud que alcanza cada uno:

$$\Lambda = \frac{\sup_{\theta\in\Theta_0} L(\theta\mid x)}{\sup_{\theta\in\Theta} L(\theta\mid x)}\in(0,1].$$

Si $\Lambda$ es pequeño, el modelo grande explica los datos **mucho** mejor que el restringido → evidencia contra $H_0$. El resultado mágico (teorema de Wilks):

$$-2\ln\Lambda\ \xrightarrow{d}\ \chi^2(r),\qquad r=\dim(\Theta)-\dim(\Theta_0),$$

donde $r$ es el número de restricciones (parámetros que el modelo simple fija). Es el motor de la selección de modelos por verosimilitud y el ancestro de AIC/BIC.

---

## Interpretación geométrica del MLE

Repasa la imagen de la colina, porque cierra el círculo con la información de Fisher. La log-verosimilitud $\ell(\theta)$ es una función de $\theta$ con un pico en $\hat\theta$:

- **Curvatura alta** en el pico (colina puntiaguda) → mucha información → estimación **precisa** (poca varianza).
- **Curvatura baja** (colina plana) → poca información → estimación **imprecisa**.

La curvatura observada en tus datos concretos es la **información observada** $J(\hat\theta)=-\partial^2\ell/\partial\theta^2\big|_{\hat\theta}$, y da una aproximación práctica a la varianza: $\text{Var}(\hat\theta)\approx 1/J(\hat\theta)$. (Es el primo "muestral" de la información esperada $I(\theta)$.)

---

## MLE para modelos de regresión: el OLS reaparece

Aquí está la conexión que vale oro en entrevista. Para $Y=X\beta+\varepsilon$ con errores normales $\varepsilon\sim N(0,\sigma^2)$, la log-verosimilitud es

$$\ell(\beta,\sigma^2)=-\tfrac n2\ln\sigma^2-\frac{(Y-X\beta)^\top(Y-X\beta)}{2\sigma^2}.$$

Maximizar en $\beta$ equivale a **minimizar** $\lVert Y-X\beta\rVert^2$ (la suma de cuadrados de los residuos), porque $\beta$ solo aparece ahí y con signo menos. La solución es la fórmula de mínimos cuadrados:

$$\hat\beta=(X^\top X)^{-1}X^\top Y\quad(\text{OLS}).$$

Es decir: **OLS = MLE bajo errores normales**. (Si los errores fueran Laplace en vez de normales, el MLE minimizaría $\sum|\varepsilon_i|$ → regresión robusta LAD.) El MLE de $\sigma^2$ vuelve a dividir por $n$ (sesgado; la versión insesgada divide por $n-p$).

---

## Familias exponenciales: por qué todo sale limpio

Casi todas las distribuciones útiles (Bernoulli, Poisson, normal, gamma…) comparten una forma común, la **familia exponencial**:

$$f(x\mid\theta)=h(x)\,\exp\big(\eta(\theta)\,T(x)-A(\theta)\big),$$

donde $T(x)$ es el estadístico suficiente y $A(\theta)$ normaliza. La consecuencia práctica: la ecuación de verosimilitud se vuelve una identidad bellísima —**el MLE iguala el estadístico suficiente a su esperanza**:

$$E_\theta[T(X)] = \tfrac1n\sum_i T(x_i).$$

Esto explica por qué tantos MLE son "el promedio": para Poisson, $T=\sum x$ y $E[\sum x]=n\lambda$, así que $\hat\lambda=\bar X$. Además, en familias exponenciales canónicas la log-verosimilitud es **cóncava**, así que el máximo es **único** y fácil de hallar (sin mínimos locales). Es el laboratorio donde toda la teoría funciona sin sobresaltos.

> **Predicción antes de seguir:** para Uniforme$[0,\theta]$, ¿el MLE sale de $\partial\ell/\partial\theta=0$? Respuesta: **no**. La verosimilitud $L(\theta)=\theta^{-n}$ para $\theta\ge\max x_i$ **decrece** sin tener derivada cero; el MLE es la **frontera** $\hat\theta=\max x_i$. Derivar a ciegas falla cuando el soporte depende de $\theta$ (la Uniforme no es familia exponencial). Siempre verifica si el máximo es interior o de borde.

---

## Mini-ejemplo trabajado: el MLE de Poisson es solo el promedio

Observas conteos diarios de eventos: n=30 días, Σxᵢ=90. Modelo Poisson(λ). La log-verosimilitud es ℓ(λ) = −nλ + (Σx)·lnλ + const. Deriva e iguala a 0:

> ∂ℓ/∂λ = −n + Σx/λ = 0 → λ̂ = Σx/n = 90/30 = **3**

El MLE es la media muestral. No es casualidad: en una familia exponencial la ecuación de verosimilitud iguala el **estadístico suficiente** a su esperanza, E_λ[T(X)] = T̄. Aquí T=Σx y E[Σx]=nλ, así que λ̂=X̄.

**Predicción antes de seguir:** ¿el MLE de E[X²]=λ²+λ es 3²+3=12? Respuesta: **sí**, por la **invarianza del MLE** — el MLE de cualquier g(λ) es g(λ̂). No hay que re-optimizar: enchufas λ̂=3. Esa propiedad (que la media posterior bayesiana *no* tiene) es lo que hace al MLE tan barato de usar.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** familia regular → log-verosimilitud cóncava → deriva, iguala a 0, y el MLE es único (en exponenciales canónicas siempre).
- **Contraejemplo (MLE en el borde):** para Uniforme[0,θ], ∂ℓ/∂θ no se anula nunca; el MLE es θ̂=máx(xᵢ), una solución de *frontera*, no de derivada cero. Derivar a ciegas falla.
- **Caso borde (σ̂² sesgado):** el MLE de σ² divide por n, no por n−1; es sesgado aunque sea MLE. Optimalidad asintótica no implica insesgamiento en muestra finita.

## Errores típicos

- **Conceptual:** confundir la verosimilitud (función de θ, datos fijos) con una densidad de θ; el MLE no es una probabilidad.
- **Técnico:** usar la información esperada I(θ) cuando solo se tiene la observada J(θ̂)=−ℓ''(θ̂); para ICs prácticos a veces se prefiere J.
- **De supuestos:** aplicar la normalidad asintótica √n(θ̂−θ)→N(0,1/I) con n pequeño o cerca de un borde del espacio paramétrico.

## Transferencia isomorfa

- **OLS = MLE bajo errores normales ↔ mínimos cuadrados:** maximizar la verosimilitud gaussiana es exactamente minimizar ‖y−Xβ‖²; con errores Laplace sería minimizar Σ|ε| (LAD, robusto) (conecta con [[arena-q6]] y [[arena-dg4]]).
- **LRT −2lnΛ ~ χ²(r) ↔ comparación de modelos anidados:** el test de razón de verosimilitudes es el motor de la selección por verosimilitud y prima a AIC/BIC (conecta con [[arena-dg4]]).
- **Familia exponencial (E[T]=T̄) ↔ GLM y conjugación:** el estadístico suficiente compacto y los priors conjugados nacen de la misma forma h(x)exp(η·T−A) (conecta con [[arena-b4]], conjugados).
- **Newton-Raphson para el MLE ↔ optimización de la pérdida en ML:** maximizar log-verosimilitud cóncava ≡ minimizar una pérdida convexa por descenso/segundo orden (conecta con [[arena-dmls1]]).

Moraleja de la arista: *el MLE resuelve ∂ℓ/∂θ=0, iguala el suficiente a su media, y se propaga por g(θ̂) gratis; bajo errores normales, eso es exactamente OLS.*

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
