# Intervalos de confianza, métodos asintóticos y delta method

## De qué trata esta lección (y qué sabrás hacer al final)

A veces tienes un pivote perfecto y el IC sale exacto. Pero muchas veces no: quieres un intervalo para una **función** del parámetro (un odds, una correlación), o solo tienes el MLE y su normalidad asintótica. Esta lección construye, desde cero, las dos herramientas que cubren esos casos: la **construcción rigurosa de ICs** (pivotes e inversión de tests) y el **delta method**, el truco universal para propagar incertidumbre a través de una transformación suave.

Al terminar podrás: (1) construir un IC exacto con un pivote y entender la dualidad IC↔test; (2) saber por qué los IC de distribuciones asimétricas (χ², F) no son de colas iguales; (3) aplicar el **delta method** para obtener el error estándar de $g(\hat\theta)$; y (4) usar transformaciones estabilizadoras (logit, √, arctanh) para que la normalidad y el IC se porten bien. Cada idea entra por su intuición; los teoremas van en `[CAJA NEGRA OK]`.

> Es la cara teórica de [[arena-dg3]] (IC aplicados) y usa la normalidad asintótica del MLE de [[arena-dg2]]/[[arena-cb2]].

---

## Intervalos de confianza: definición precisa

Un intervalo **aleatorio** $[L(X),U(X)]$ es un IC de nivel $1-\alpha$ para $\theta$ si

$$P_\theta\big(L(X)\le\theta\le U(X)\big)\ge 1-\alpha\quad\text{para todo }\theta.$$

La interpretación frecuentista, que tropieza a casi todos: lo aleatorio es el **intervalo**, no $\theta$ (que es fijo). "95% de confianza" significa que el *procedimiento* atrapa a $\theta$ el 95% de las veces si lo repites, no que "hay 95% de probabilidad de que $\theta$ esté en este intervalo concreto".

## Pivotes

Un **pivote** $Q(X,\theta)$ es una función de datos y parámetro cuya distribución **no depende de $\theta$**. Es la llave maestra: como conoces su distribución, sabes entre qué valores cae, y despejas $\theta$.

1. Encuentra $Q(X,\theta)$ con distribución conocida ($t$, $\chi^2$, $F$, $U$…).
2. Halla $a,b$ con $P(a\le Q\le b)=1-\alpha$.
3. Despeja $\theta$ de $a\le Q(X,\theta)\le b$.

| Situación | Pivote | IC $(1-\alpha)$ |
|-----------|--------|----------|
| $N(\mu,\sigma^2)$, $\sigma^2$ conocida | $Z=(\bar X-\mu)/(\sigma/\sqrt n)\sim N(0,1)$ | $\bar X\pm z_{\alpha/2}\,\sigma/\sqrt n$ |
| $N(\mu,\sigma^2)$, $\sigma^2$ desconocida | $T=(\bar X-\mu)/(S/\sqrt n)\sim t_{n-1}$ | $\bar X\pm t_{n-1,\alpha/2}\,S/\sqrt n$ |
| $N$, para $\sigma^2$ | $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$ | $[(n-1)S^2/b,\ (n-1)S^2/a]$ |
| Uniforme$[0,\theta]$ | $Y=X_{(n)}/\theta\sim\text{Beta}(n,1)$ | $[X_{(n)},\ X_{(n)}/\alpha^{1/n}]$ |

El caso uniforme es instructivo: el pivote no es una resta estandarizada sino un **cociente** $X_{(n)}/\theta$, porque la información de $\theta$ vive en el máximo, no en el promedio.

## IC por inversión de tests

Aquí la dualidad se vuelve definición. El IC es **el conjunto de valores que un test no rechazaría**:

$$C(x)=\{\theta_0:\ \text{el test de }H_0:\theta=\theta_0\text{ NO rechaza }x\}.$$

Si el test de nivel $\alpha$ tiene región de aceptación $A(\theta_0)$, entonces $C(x)=\{\theta_0:x\in A(\theta_0)\}$. Consecuencia elegante: el IC **más preciso** (UMA, *uniformly most accurate*) se obtiene invirtiendo el **test UMP** (ver [[arena-cb3]]). Mejor test → mejor intervalo.

## IC más corto y asimetría

Si el pivote tiene densidad $f$ unimodal continua, el IC **más corto** de nivel $1-\alpha$ con extremos $[a,b]$ cumple $\int_a^b f=1-\alpha$ **y** $f(a)=f(b)$ (igual densidad en los bordes). Para densidades **simétricas** (z, t), eso da el intervalo de colas iguales $a=-b$ — el de siempre. Pero para densidades **asimétricas** ($\chi^2$, $F$, Beta), el IC de colas iguales **no** es el más corto. De ahí que el IC de $\sigma^2$ no se centre en $S^2$: la forma del pivote manda.

## Intervalos de predicción y tolerancia

Distingue tres preguntas que se confunden:
- **IC para $\mu$**: ¿dónde está la *media*? Ancho $\propto S/\sqrt n$.
- **Intervalo de predicción** para una **nueva** observación $X_{n+1}$: $\bar X\pm t_{n-1,\alpha/2}\,S\sqrt{1+1/n}$. Es **más ancho**: además de la incertidumbre sobre $\mu$, suma la variabilidad de la observación nueva (el $1+$ bajo la raíz).
- **Intervalo de tolerancia**: cubre al menos $p\%$ de la *población* con confianza $1-\alpha$.

---

## Delta method: propagar incertidumbre por una transformación

El problema: sabes que $\hat\theta$ es aproximadamente normal, y quieres un IC para $g(\hat\theta)$ (un odds, una raíz, una correlación). No hay pivote exacto. La solución es **linealizar**: cerca de $\theta$, una función suave $g$ se parece a su recta tangente, y la pendiente $g'(\theta)$ **estira o encoge** el error.

`[CAJA NEGRA OK]` — asume el resultado; la prueba es una expansión de Taylor de primer orden.

Si $\sqrt n(\hat\theta-\theta)\xrightarrow{d}N(0,\sigma^2)$ y $g$ es derivable con $g'(\theta)\ne0$:

$$\sqrt n\big(g(\hat\theta)-g(\theta)\big)\xrightarrow{d}N\!\big(0,\ \sigma^2\,[g'(\theta)]^2\big).$$

En palabras: **el error estándar se multiplica por $|g'|$**, la sensibilidad local de $g$. De ahí el IC asintótico $g(\hat\theta)\pm z_{\alpha/2}\,\hat\sigma\,|g'(\hat\theta)|/\sqrt n$.

| Transformación $g$ | $g'(\theta)$ | Uso |
|-----------------|-------|------------|
| logit $\log\frac{p}{1-p}$ | $1/(p(1-p))$ | IC para el logit de una proporción |
| $\sqrt\lambda$ (raíz Poisson) | $1/(2\sqrt\lambda)$ | estabiliza la varianza de Poisson |
| arctanh$(r)$ (Fisher) | $1/(1-r^2)$ | IC para una correlación $\rho$ |

## Normalidad asintótica del MLE (cierre)

Para familias regulares (ver [[arena-dg2]]): $\hat\theta_{\text{MLE}}$ es consistente y $\sqrt n(\hat\theta-\theta)\xrightarrow{d}N(0,1/I(\theta))$, lo que da el IC asintótico $\hat\theta\pm z_{\alpha/2}/\sqrt{n\,\hat I(\hat\theta)}$, usando la **información observada** $\hat I(\hat\theta)=-\frac1n\sum\partial^2\log f(x_i\mid\hat\theta)/\partial\theta^2$. Es el puente entre "tengo un MLE" y "tengo un intervalo".

## Bonferroni e inferencia simultánea

Para $k$ parámetros a la vez, la cota de la unión da $P(\text{todos los IC contienen su parámetro})\ge 1-\sum\alpha_i$. La **regla de Bonferroni**: usa $\alpha_i=\alpha/k$ en cada IC para garantizar nivel conjunto $1-\alpha$. Es el mismo reparto de $\alpha$ que en tests múltiples ([[arena-dg3]]).

> **Predicción antes de seguir:** ¿qué le pasa al delta method si $g'(\theta)=0$ (un punto plano de $g$)? Respuesta: **falla** — la varianza de primer orden $\sigma^2[g'(\theta)]^2$ daría 0, lo cual es falso. En un punto plano, la recta tangente es horizontal y no captura la curvatura; hay que ir al **segundo orden** (la aproximación se vuelve $\chi^2$, no normal). El método de primer orden vale solo donde $g$ tiene pendiente no nula.

---

## Mini-ejemplo trabajado: delta method para un odds estimado

Estimas una proporción p̂=0.2 con n=100 (SE de p̂ ≈ √(0.2·0.8/100)=0.04) y quieres un IC para el **logit** g(p)=log(p/(1−p)). No hay pivote exacto, pero el delta method propaga la incertidumbre usando la derivada:

> g'(p) = 1/(p(1−p)) = 1/(0.2·0.8) = 6.25
> SE(logit) ≈ g'(p̂)·SE(p̂) = 6.25·0.04 = 0.25

IC del 95% para el logit: log(0.2/0.8) ± 1.96·0.25 = −1.386 ± 0.49. La idea: **una transformación suave estira el error por su pendiente local** g'(θ). Linealizas g alrededor de θ̂ y la normalidad se transfiere.

**Predicción antes de seguir:** ¿por qué construir el IC en la escala logit y luego transformar de vuelta, en lugar de p̂±1.96·SE directo? Respuesta: porque cerca de p=0 o p=1 el IC simétrico en p se sale de [0,1] y la aproximación normal es mala; en la escala logit (sin fronteras) la normalidad funciona mejor y al des-transformar el intervalo queda **dentro de (0,1)** y asimétrico, como debe ser. La transformación estabiliza.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** hay pivote con distribución conocida (z, t, χ², F) → IC exacto despejando θ.
- **Contraejemplo (g'(θ)=0):** si la derivada se anula, el delta method de primer orden da varianza 0 (falso); hay que ir al segundo orden (χ²). El método falla justo en los puntos planos.
- **Caso borde (IC asimétrico):** para σ² el pivote χ² no es simétrico, así que el IC más corto NO es de colas iguales; usar ± simétrico es un error. El borde recuerda que la forma del pivote manda.

## Errores típicos

- **Conceptual:** interpretar "IC 95%" como "P(θ en el intervalo)=0.95"; θ es fijo, el intervalo es aleatorio — la cobertura es frecuentista.
- **Técnico:** aplicar IC simétrico (±) a pivotes asimétricos (χ², F, Beta).
- **De supuestos:** usar el delta method con n pequeño o cerca de g'(θ)=0, donde la linealización es pobre.

## Transferencia isomorfa

- **Delta method ↔ propagación de errores e ingeniería:** "SE(g(θ̂)) ≈ |g'|·SE(θ̂)" es la fórmula universal de propagación de incertidumbre en física y métricas derivadas (conecta con [[arena-q7]], donde la duración es g'(precio) y la convexidad el segundo orden).
- **Transformación estabilizadora (logit, √, arctanh) ↔ feature engineering / normalización:** transformar para que la varianza sea constante y el rango no tenga fronteras es lo mismo que normalizar features antes de un modelo (conecta con [[arena-dmls1]]).
- **IC por inversión de test ↔ dualidad IC-test:** el IC es el conjunto de θ₀ que el test no rechaza; el IC más preciso viene de invertir el test UMP (conecta con [[arena-cb3]] y [[arena-dg3]]).
- **Bonferroni simultáneo ↔ corrección de tests múltiples:** repartir α entre k intervalos es el mismo control de error familiar que en experimentación con muchas métricas (conecta con [[arena-dg3]] y [[arena-obs1]]).

Moraleja de la arista: *sin pivote exacto, linealiza con el delta method (el error se estira por la pendiente g'); y transformar a una escala sin fronteras hace que la normalidad —y el IC— se porten bien.*

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
