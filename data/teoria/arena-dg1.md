# Estimación puntual y propiedades de estimadores

## De qué trata esta lección (y qué sabrás hacer al final)

Tienes datos y quieres adivinar un número desconocido del mundo que los generó: la tasa de fallo de una máquina, la conversión media de una campaña, la varianza de un proceso. Una **regla** que convierte datos en esa adivinanza es un *estimador*. Esta lección construye, desde cero, cómo se juzga si un estimador es bueno —y descubre la idea más importante de toda la estadística aplicada: **no busques acertar en promedio, busca el menor error total**, que es exactamente el trade-off sesgo–varianza que después gobierna todo el machine learning.

Al terminar podrás: (1) calcular el sesgo, la varianza y el MSE de un estimador y entender por qué un estimador *sesgado* puede ganar; (2) leer la información de Fisher y la cota de Cramér-Rao como "el límite físico de la precisión"; (3) reconocer un estadístico suficiente (lo que comprime los datos sin perder información); y (4) saber qué es el MLE y el UMVUE y cuándo usar cada uno. No se asume teoría previa: cada concepto entra por su intuición antes de cualquier fórmula. Para los teoremas pesados (Cramér-Rao, Lehmann-Scheffé) uso `[CAJA NEGRA OK]`: la intuición es obligatoria, la demostración no.

---

## ¿Qué es un estimador?

Imagina que quieres conocer la altura media $\theta$ de una población. No puedes medir a todos, así que tomas una muestra $X_1,\dots,X_n$ y calculas el promedio. Esa receta —"promedia tus datos"— es un **estimador**: una función de los datos,

$$\hat\theta = T(X_1,\dots,X_n),$$

que aproxima un parámetro desconocido $\theta$. La notación $\hat\theta$ ("theta sombrero") significa "mi estimación de $\theta$".

La idea sutil, y la que todo lo demás necesita: como los datos son aleatorios (otra muestra daría otros números), **el estimador también es aleatorio**. Tiene su propia distribución, su esperanza y su varianza. Juzgar un estimador es, por tanto, estudiar el comportamiento de esa distribución: ¿cae cerca de $\theta$ en promedio? ¿cuánto se mueve de muestra a muestra?

---

## Propiedades deseables

### Insesgamiento: ¿aciertas en promedio?

El **sesgo** (bias) mide cuánto se desvía, en promedio, tu estimador del valor real:

$$\text{Bias}(\hat\theta) = E[\hat\theta] - \theta.$$

Aquí $E[\hat\theta]$ es el promedio de tu estimador sobre todas las muestras posibles. Si el sesgo es 0 (es decir $E[\hat\theta]=\theta$), el estimador es **insesgado**: en promedio da en el blanco. Ejemplo: el promedio muestral $\bar X$ es insesgado para la media $\mu$, sea cual sea la distribución.

Cuidado con la trampa que viene: insesgado **no** significa "bueno". Significa solo "centrado". Un estimador puede estar centrado pero temblar muchísimo de muestra a muestra.

### Error cuadrático medio: la medida que de verdad importa

Lo que quieres no es acertar en promedio, sino estar **cerca**. El **error cuadrático medio (MSE)** mide la distancia típica al cuadrado entre $\hat\theta$ y $\theta$, y se descompone en dos piezas:

$$\text{MSE}(\hat\theta) = \underbrace{\text{Var}(\hat\theta)}_{\text{cuánto tiembla}} + \underbrace{\text{Bias}(\hat\theta)^2}_{\text{cuánto se desvía}}.$$

Esta igualdad es la frase más importante de la lección. Dice que el error total tiene dos enemigos: la **varianza** (inestabilidad) y el **sesgo** (descentrado). Para un estimador insesgado, $\text{MSE}=\text{Var}$. Pero —y aquí está la revelación— a veces **aceptar un poco de sesgo reduce tanto la varianza que el MSE total baja**. Perseguir insesgamiento a toda costa puede dejarte con un estimador peor. Si $\hat\theta_1$ tiene menor MSE que $\hat\theta_2$ para todo $\theta$, decimos que $\hat\theta_1$ **domina**.

### Consistencia: ¿mejora con más datos?

Un estimador es **consistente** si, al crecer el tamaño de muestra $n$, se acerca al valor real: $\hat\theta_n \xrightarrow{P} \theta$ (converge en probabilidad). Es el requisito mínimo: "si junto datos infinitos, acierto". Una condición suficiente, muy intuitiva: si **tanto el sesgo como la varianza tienden a 0** cuando $n\to\infty$, el estimador es consistente. La Ley de los Grandes Números es justo el caso que garantiza que $\bar X$ es consistente para $\mu$.

---

## Información de Fisher: ¿cuánto te dice un dato sobre θ?

Antes de preguntar "¿qué tan preciso puedo ser?", necesitamos medir **cuánta información sobre $\theta$ trae cada observación**. Esa es la **información de Fisher** $I(\theta)$. La intuición geométrica es preciosa: dibuja la log-verosimilitud (qué tan "creíble" es cada valor de $\theta$ dados tus datos) como una colina cuyo pico está en la mejor estimación. Si la colina es **muy puntiaguda**, datos vecinos descartan rápido los valores cercanos → mucha información, estimación precisa. Si es **plana**, muchos valores de $\theta$ explican casi igual de bien → poca información. La información de Fisher es esa **curvatura** promedio:

$$I(\theta) = E\!\left[\left(\frac{\partial \ln f(X\mid\theta)}{\partial\theta}\right)^2\right] = -\,E\!\left[\frac{\partial^2 \ln f(X\mid\theta)}{\partial\theta^2}\right].$$

La primera forma es la varianza de la "pendiente" de la log-verosimilitud; la segunda, su curvatura (la segunda derivada con signo menos). Ambas coinciden bajo regularidad.

| Distribución | $I(\theta)$ |
|-------------|------|
| Bernoulli$(p)$ | $1/(p(1-p))$ |
| $N(\mu,\sigma^2)$ — para $\mu$ | $1/\sigma^2$ |
| Poisson$(\lambda)$ | $1/\lambda$ |
| Exp$(\lambda)$ | $1/\lambda^2$ |

La información **se acumula**: con $n$ datos i.i.d., $I_n(\theta) = n\,I(\theta)$. Más datos, más curvatura, más precisión — exactamente lo que esperarías.

---

## Cota de Cramér-Rao: el límite físico de la precisión

`[CAJA NEGRA OK]` — *Qué asumir:* que existe una cota inferior universal para la varianza de cualquier estimador insesgado, y que vale $1/(nI(\theta))$. *Por qué se permite:* la demostración (desigualdad de Cauchy-Schwarz aplicada a la score) no añade intuición para usarla. *Qué sí razonar:* su significado y cuándo se alcanza. *Cuándo reabrir:* si necesitas probar eficiencia formalmente.

Ningún estimador insesgado puede ser arbitrariamente preciso: hay un suelo para su varianza, fijado por la información disponible:

$$\text{Var}(\hat\theta) \ge \frac{1}{n\,I(\theta)}.$$

Léelo así: cuanta más información $I(\theta)$ traen tus datos, más bajo puede llegar el suelo, y más preciso puedes aspirar a ser. La **eficiencia** de un estimador mide qué tan cerca está de ese suelo,

$$e(\hat\theta) = \frac{1/[n\,I(\theta)]}{\text{Var}(\hat\theta)} \in (0,1],$$

y vale 1 (estimador **eficiente**) solo si toca la cota. El MLE, que veremos enseguida, es **asintóticamente eficiente**: alcanza el suelo cuando $n$ es grande.

---

## Estadístico suficiente: comprimir sin perder información

Aquí una idea elegante. Si lanzas una moneda 5 veces y obtienes $(1,0,1,1,0)$, ¿necesitas el orden para estimar $p$? No: basta con saber que hubo **3 éxitos**. El total $\sum X_i$ contiene *toda* la información sobre $p$; el orden es ruido. Un estadístico $T(X)$ es **suficiente** para $\theta$ cuando, una vez que conoces $T$, los datos crudos no añaden nada sobre $\theta$ (formalmente: la distribución de $X$ dado $T=t$ no depende de $\theta$).

Para detectarlo sin pensar en distribuciones condicionales, está el **criterio de factorización (Fisher-Neyman):** $T$ es suficiente si y solo si la densidad se parte en

$$f(x\mid\theta) = g(T(x),\theta)\cdot h(x),$$

donde $g$ contiene toda la dependencia de $\theta$ (a través de $T$) y $h(x)$ no depende de $\theta$. En palabras: **la verosimilitud solo toca a los datos a través de $T(x)$**.

| Distribución | Estadístico suficiente |
|-------------|----------------------|
| Bernoulli$(p)$ | $T=\sum X_i$ (total de éxitos) |
| $N(\mu,\sigma^2)$ — $\mu$ desconocida | $T=\sum X_i$ (o $\bar X$) |
| $N(\mu,\sigma^2)$ — ambos desconocidos | $T=(\sum X_i,\ \sum X_i^2)$ |
| Poisson$(\lambda)$ | $T=\sum X_i$ |
| Uniforme$[0,\theta]$ | $T=X_{(n)}=\max X_i$ |

> **Predicción antes de seguir:** ¿el estadístico suficiente es siempre una suma o un promedio? Respuesta: **no**. Para Uniforme$[0,\theta]$ el suficiente es el **máximo** $X_{(n)}$, no la suma — el dato más grande es el que más restringe a $\theta$ (sabes que $\theta\ge$ ese máximo). La forma del suficiente la dicta la familia, no tu costumbre de promediar.

---

## Métodos de estimación

### Estimador de momentos (MM)

El más simple: iguala los **momentos teóricos** a los **muestrales** y despeja. Como $E[X]$ depende de $\theta$, pones $E[X]=\bar X$ (y si hace falta $E[X^2]=\frac1n\sum X_i^2$, etc.) y resuelves. Rápido y no necesita forma cerrada bonita, pero suele ser **ineficiente** (no aprovecha toda la información).

### Máxima verosimilitud (MLE)

La idea estrella: **elige el $\theta$ que hace más probables los datos que viste**. La *verosimilitud* es la probabilidad conjunta de tus datos vista como función de $\theta$, $L(\theta\mid x)=\prod_i f(x_i\mid\theta)$, y el MLE la maximiza (en la práctica se maximiza su logaritmo, que convierte el producto en suma):

$$\hat\theta_{\text{MLE}} = \arg\max_\theta\ \sum_i \ln f(x_i\mid\theta).$$

Sus propiedades lo hacen el estimador "por defecto" de la estadística:

1. **Consistente:** $\hat\theta_{\text{MLE}}\xrightarrow{P}\theta$.
2. **Asintóticamente normal:** $\sqrt{n}(\hat\theta_{\text{MLE}}-\theta)\xrightarrow{d}N\!\big(0,\,1/I(\theta)\big)$ — base de todos los ICs y tests de gran muestra.
3. **Asintóticamente eficiente:** alcanza la cota de Cramér-Rao cuando $n$ es grande.
4. **Invariante:** el MLE de $g(\theta)$ es simplemente $g(\hat\theta_{\text{MLE}})$ — no hay que re-optimizar. (Desarrollado en [[arena-dg2]].)

---

## UMVUE: el mejor estimador insesgado

Si te *empeñas* en insesgamiento, ¿cuál es el mejor que puedes tener? El **UMVUE** (estimador insesgado de varianza mínima uniforme) es el insesgado con menor varianza para **todo** $\theta$. Se construye con dos teoremas que conviene entender como recetas:

`[CAJA NEGRA OK]` — asume estos dos resultados; la intuición basta para aplicarlos.

- **Rao-Blackwell:** si $\hat\theta$ es insesgado y $T$ suficiente, entonces $E[\hat\theta\mid T]$ es insesgado y tiene varianza **menor o igual**. Intuición: promediar sobre el ruido irrelevante (lo que $T$ ya resumió) nunca empeora. Es la versión teórica de "promedia para reducir varianza".
- **Lehmann-Scheffé:** si además $T$ es **completo** (una condición técnica de unicidad: $E[g(T)]=0$ para todo $\theta$ obliga a $g\equiv 0$), entonces cualquier función de $T$ que sea insesgada es **el** UMVUE.

Ejemplo: en la normal, $\bar X$ es el UMVUE de $\mu$ (porque $\sum X_i$ es suficiente y completo). El detalle de completitud y el teorema de Basu se desarrollan en [[arena-cb1]]; la receta completa para construir UMVUEs, en [[arena-cb2]].

---

## Eficiencia relativa y robustez

Para comparar dos estimadores, la **eficiencia relativa** es el cociente de sus MSE:

$$e(\hat\theta_1,\hat\theta_2) = \frac{\text{MSE}(\hat\theta_2)}{\text{MSE}(\hat\theta_1)}.$$

Si $e>1$, $\hat\theta_1$ es mejor. Caso famoso: en la normal, $e(\bar X,\text{mediana})=\pi/2\approx 1.57$ — la media es 57% más eficiente que la mediana. Pero **cambia la distribución y todo se invierte**: en colas pesadas (Cauchy), $\bar X$ tiene varianza infinita y la **mediana la aplasta**. La lección de robustez: el mejor estimador depende de cuánto contamina la cola; no hay un campeón universal.

---

## Estimación Bayesiana

Si tienes **creencia previa** sobre $\theta$ (un *prior* $\pi(\theta)$), la combinas con los datos vía Bayes y obtienes un *posterior*. ¿Qué número reportas del posterior? Depende de cómo penalices el error (la **función de pérdida**):

| Pérdida | Estimador de Bayes |
|---------|-------------------|
| Cuadrática $(\theta-\delta)^2$ | Media posterior $E[\theta\mid x]$ |
| Absoluta $\lvert\theta-\delta\rvert$ | Mediana posterior |
| 0-1 | Moda posterior (MAP) |

El **riesgo de Bayes** es el riesgo frecuentista promediado sobre el prior, $r(\delta)=\int R(\theta,\delta)\,\pi(\theta)\,d\theta$, y el estimador de Bayes es justo el que lo minimiza. Nota la conexión: la moda posterior es el MAP que viste en inferencia aplicada — el puente entre este capítulo y el ML.

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
