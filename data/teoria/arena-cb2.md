# Estimación puntual: MLE, Cramér-Rao y UMVUE

## De qué trata esta lección (y qué sabrás hacer al final)

Esta lección es el **manual de construcción** de estimadores: cómo *fabricar* uno (método de momentos, MLE), cómo saber si es lo mejor posible (cota de Cramér-Rao) y cómo encontrar el mejor entre los insesgados (UMVUE, vía una receta de tres pasos). Donde [[arena-dg1]] dio el panorama y [[arena-cb1]] la teoría de suficiencia, aquí ensamblamos todo en procedimientos que puedes ejecutar en una entrevista.

Al terminar podrás: (1) calcular el MLE y el estimador de momentos de una distribución; (2) escribir la cota de Cramér-Rao y saber cuándo se alcanza; (3) ejecutar la **receta de Rao-Blackwell / Lehmann-Scheffé** para hallar el UMVUE; y (4) usar priors conjugados para la versión bayesiana. Cada herramienta entra por su intuición. Los teoremas (Cramér-Rao, Lehmann-Scheffé) van en `[CAJA NEGRA OK]`.

> Comparte fundamentos con [[arena-dg1]] (sesgo, MSE, Fisher) y [[arena-dg2]] (MLE, asintótica). Si esos términos te son nuevos, empieza por dg1.

---

## Métodos de encontrar estimadores

### Método de momentos (MoM)

El más directo: los **momentos** de una distribución (media, media de los cuadrados, …) dependen de $\theta$. Iguala el momento teórico al **muestral** y despeja. Con un parámetro: pon $E[X]=\bar X$ y resuelve. Con $k$ parámetros, iguala los primeros $k$ momentos $m_j=\frac1n\sum X_i^j$ a sus expresiones teóricas $\mu_j'(\theta_1,\dots,\theta_k)$. Es simple y no exige una forma cerrada bonita, pero suele ser **ineficiente** (desperdicia información).

### Máxima verosimilitud (MLE)

Elige el $\theta$ que hace **más probables los datos observados** (intuición completa en [[arena-dg2]]). El procedimiento:

1. Escribe $\ell(\theta)=\sum_i\log f(x_i\mid\theta)$.
2. Resuelve la ecuación de verosimilitud $\partial\ell/\partial\theta=0$.
3. Verifica que sea **máximo** ($\partial^2\ell/\partial\theta^2<0$) y no de frontera.

| Distribución | MLE |
|-------------|-----|
| Bernoulli$(p)$ | $\hat p=\bar X$ |
| Normal$(\mu,\sigma^2)$ | $\hat\mu=\bar X,\ \hat\sigma^2=\frac1n\sum(X_i-\bar X)^2$ |
| Poisson$(\lambda)$ | $\hat\lambda=\bar X$ |
| Exponencial$(\lambda)$ | $\hat\lambda=1/\bar X$ |
| Uniforme$[0,\theta]$ | $\hat\theta=X_{(n)}=\max X_i$ |
| Doble exponencial (Laplace) | $\hat\theta=$ mediana muestral |

La última fila es reveladora: bajo errores Laplace el MLE es la **mediana** (no la media), porque minimizar $\sum|x_i-\theta|$ —la log-verosimilitud de Laplace— se logra en la mediana. La distribución del error decide qué estadístico es óptimo. **Invarianza:** el MLE de $g(\theta)$ es $g(\hat\theta)$.

---

## Información de Fisher (recordatorio operativo)

Mide la información que un dato trae sobre $\theta$ (curvatura de la log-verosimilitud; intuición en [[arena-dg1]]):

$$I(\theta)=E\!\left[\Big(\tfrac{\partial\log f}{\partial\theta}\Big)^2\right]=-E\!\left[\tfrac{\partial^2\log f}{\partial\theta^2}\right],\qquad I_n(\theta)=n\,I(\theta).$$

| Distribución | $I(\theta)$ |
|-------------|------|
| Bernoulli$(p)$ | $1/(p(1-p))$ |
| $N(\mu,\sigma^2)$ — para $\mu$ ($\sigma^2$ conocida) | $1/\sigma^2$ |
| $N(\mu,\sigma^2)$ — para $\sigma^2$ ($\mu$ conocida) | $1/(2\sigma^4)$ |
| Poisson$(\lambda)$ | $1/\lambda$ |
| Exponencial$(\lambda)$ | $1/\lambda^2$ |

---

## Cota de Cramér-Rao

`[CAJA NEGRA OK]` — asume la cota; lo que importa es leerla y saber cuándo se alcanza.

Para todo estimador insesgado $\hat\tau$ de una cantidad $\tau(\theta)$, su varianza tiene un **suelo**:

$$\text{Var}(\hat\tau)\ \ge\ \frac{[\tau'(\theta)]^2}{n\,I(\theta)}.$$

El numerador $[\tau'(\theta)]^2$ ajusta por la "sensibilidad" de lo que estimas (si $\tau$ cambia rápido con $\theta$, su estimación tiembla más). La cota **se alcanza** —el estimador es **eficiente**— exactamente cuando la score se factoriza como $\partial\log f/\partial\theta=a(\theta)[\hat\tau(x)-\tau(\theta)]$, lo que ocurre **solo en las familias exponenciales de un parámetro**. La **eficiencia** $e(\hat\tau)=[\tau'(\theta)]^2/(n\,I(\theta)\,\text{Var}(\hat\tau))\in(0,1]$ vale 1 ahí. Ejemplo: $\bar X$ para Bernoulli tiene $\text{Var}=p(1-p)/n$, que iguala la cota → $\bar X$ es eficiente.

---

## UMVUE: el mejor estimador insesgado

El **UMVUE** ($\delta^*$) es insesgado y tiene varianza mínima para **todo** $\theta$. Se construye con dos teoremas, que en la práctica son una receta.

`[CAJA NEGRA OK]` — asume ambos; la intuición basta para aplicarlos.

- **Rao-Blackwell:** si $\delta$ es insesgado y $T$ suficiente, entonces $\delta^*=E[\delta\mid T]$ es insesgado y **nunca tiene más varianza** ($\text{Var}(\delta^*)\le\text{Var}(\delta)$). Intuición: promediar sobre el ruido que $T$ ya resumió solo puede ayudar.
- **Lehmann-Scheffé:** si $T$ es suficiente **y completo** (ver [[arena-cb1]]), cualquier función de $T$ insesgada para $\tau(\theta)$ es **el único** UMVUE.

**Receta para el UMVUE:**
1. Encuentra $T$ suficiente **y completo**.
2. Encuentra **cualquier** estimador insesgado $\delta$ de $\tau(\theta)$ (aunque sea malo).
3. Calcula $\delta^*=E[\delta\mid T]$ (lo "Rao-Blackwellizas").
4. $\delta^*$ es el UMVUE.

| Distribución | Parámetro | UMVUE |
|-------------|-----------|-------|
| Bernoulli$(p)$ | $p$ | $\bar X$ |
| Bernoulli$(p)$ | $p^2$ | $\dfrac{(\sum X_i)(\sum X_i-1)}{n(n-1)}$ |
| $N(\mu,\sigma^2)$ | $\mu$ | $\bar X$ |
| $N(\mu,\sigma^2)$ | $\sigma^2$ | $S^2=\frac{1}{n-1}\sum(X_i-\bar X)^2$ |
| Exp$(\lambda)$ | $1/\lambda$ | $\bar X$ |

La fila de $p^2$ enseña algo: el UMVUE de una función **no** es esa función del UMVUE (no es $\bar X^2$); hay que corregir el sesgo de $\bar X^2$. El UMVUE no tiene la invarianza cómoda del MLE.

---

## Estimación Bayesiana y conjugación

Si tienes un prior $\pi(\theta)$, lo combinas con los datos para un posterior, y reportas la media/mediana/moda posterior según la pérdida (cuadrática/absoluta/0-1; ver [[arena-dg1]]). El truco que lo hace tratable es la **conjugación**: ciertos priors hacen que el posterior sea de la **misma familia**, así que actualizar es solo sumar a los parámetros:

| Verosimilitud | Prior conjugado | Posterior |
|---------------|-----------------|-----------|
| Bernoulli$(p)$ | Beta$(\alpha,\beta)$ | Beta$(\alpha+\sum x_i,\ \beta+n-\sum x_i)$ |
| Poisson$(\lambda)$ | Gamma$(\alpha,\beta)$ | Gamma$(\alpha+\sum x_i,\ \beta+n)$ |
| $N(\mu,\sigma^2)$, $\sigma^2$ conocida | $N(\mu_0,\tau^2)$ | $N(\text{media ponderada},\ \text{var. combinada})$ |

Lee Beta-Binomial: el prior $\text{Beta}(\alpha,\beta)$ actúa como "$\alpha$ éxitos y $\beta$ fracasos imaginarios"; el posterior simplemente les suma los reales. La actualización bayesiana de tasas es exactamente esto (conecta con [[arena-b4]]).

---

## Propiedades asintóticas del MLE (cierre)

Para familias regulares (detalle en [[arena-dg2]]):

$$\sqrt{n}(\hat\theta_{\text{MLE}}-\theta)\xrightarrow{d}N\!\big(0,\ 1/I(\theta)\big),$$

lo que da **consistencia**, **eficiencia asintótica** (alcanza la cota CR en el límite) y el **IC** $\hat\theta\pm z_{\alpha/2}/\sqrt{n\,I(\hat\theta)}$. El MLE es, por eso, el estimador "por defecto": casi siempre óptimo cuando $n$ es grande, aunque pueda ser sesgado en muestra finita.

> **Predicción antes de seguir:** la cota de Cramér-Rao asume "condiciones de regularidad". ¿Se aplica a Uniforme$[0,\theta]$? Respuesta: **no** — su soporte depende de $\theta$, lo que rompe la regularidad. Por eso el MLE $X_{(n)}$ converge a tasa $1/n$ (¡más rápido que el habitual $1/\sqrt n$!) y la asintótica normal estándar no aplica. La uniforme es el caso borde que rompe casi todos los teoremas de este capítulo.

---

## Mini-ejemplo trabajado: el MLE de Uniforme[0,θ] es sesgado y cómo arreglarlo

n=4 muestras de Uniforme[0,θ], máximo observado X₍₄₎=8. El MLE es θ̂=X₍ₙ₎=8 (no puedes haber generado un 8 con θ<8, y la verosimilitud decrece en θ por encima). Pero **siempre** X₍ₙ₎ ≤ θ, así que el MLE **subestima sistemáticamente**:

> E[X₍ₙ₎] = n/(n+1)·θ = 4/5·θ → Bias = −θ/5

El insesgado se obtiene reescalando: θ̃ = (n+1)/n · X₍ₙ₎ = 5/4·8 = **10**. Y este θ̃, función del suficiente-completo X₍ₙ₎, es el **UMVUE**.

**Predicción antes de seguir:** ¿el MLE θ̂=8 o el insesgado θ̃=10 tiene menor MSE? Respuesta: sorprendentemente el insesgado **no siempre gana**; el estimador de mínimo MSE escala por (n+2)/(n+1), entre ambos. De nuevo: insesgado, MLE y mínimo-MSE son tres objetivos distintos, y aquí divergen visiblemente. (Conecta con el trade-off MSE=Var+Bias².)

## Prototipo, contraejemplo y caso borde

- **Prototipo (receta UMVUE):** halla T suficiente y completo, toma cualquier insesgado δ, calcula E[δ|T] → UMVUE (Lehmann-Scheffé).
- **Contraejemplo (la cota CR no siempre se alcanza):** solo en familias exponenciales de un parámetro un insesgado iguala 1/(nI(θ)); fuera de ahí el UMVUE puede tener varianza estrictamente mayor que la cota.
- **Caso borde (soporte dependiente de θ):** en Uniforme[0,θ] la regularidad de Cramér-Rao **falla** (el soporte depende de θ), por eso el MLE converge a tasa 1/n, no 1/√n. El borde rompe la asintótica estándar.

## Errores típicos

- **Conceptual:** reportar el MLE como insesgado; muchos MLE (σ̂², X₍ₙ₎) lo son solo asintóticamente.
- **Técnico:** aplicar Cramér-Rao a la Uniforme (condiciones de regularidad violadas).
- **De supuestos:** condicionar en un suficiente no completo y creer que el resultado es UMVUE.

## Transferencia isomorfa

- **Rao-Blackwell (E[δ|T]) ↔ promediar para reducir varianza:** condicionar en el suficiente nunca empeora, el análogo teórico de ensamblar modelos (conecta con [[arena-dg1]]).
- **MLE asintóticamente N(θ,1/(nI)) ↔ IC y tests de Wald:** la normalidad asintótica es el motor de todos los intervalos de gran muestra (conecta con [[arena-cb4]] y [[arena-dg2]]).
- **Insesgado ≠ mínimo MSE ↔ sesgo-varianza en ML:** corregir el sesgo del máximo es la misma decisión que regularizar un modelo (conecta con [[arena-iml4]]).
- **Conjugación Beta-Binomial ↔ actualización bayesiana de tasas:** el posterior cierra la familia, igual que en toda inferencia de proporciones (conecta con [[arena-b4]]).

Moraleja de la arista: *el MLE del máximo subestima; reescalar por (n+1)/n lo insesga y lo vuelve UMVUE — pero insesgado, MLE y mínimo-MSE rara vez coinciden.*

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
