# Distribuciones importantes y sus relaciones

## De qué trata (y qué sabrás hacer)

La trampa al estudiar distribuciones es tratarlas como una lista de fórmulas que memorizar. No lo son: son una **red de parentescos**. La exponencial es un caso de la Gamma; la Beta es una Gamma normalizada; la chi-cuadrado es Gamma con parámetros concretos; la $t$ nace de dividir una normal por una chi. Si entiendes los vínculos, reconstruyes cualquier fórmula y eliges la distribución correcta ante un enunciado nuevo.

Al terminar sabrás, ante un problema, decir "esto es un tiempo de espera → Gamma", "esto es una proporción desconocida → Beta", "esto es un cociente de varianzas → F", y conocerás el porqué de cada parentesco. Cada familia se motiva desde lo que modela.

---

## La familia Gamma: tiempos de espera apilados

La **Gamma** modela el tiempo hasta que ocurren $\alpha$ eventos de un proceso sin memoria. Su densidad:

$$f(x)=\frac{\lambda^\alpha x^{\alpha-1}e^{-\lambda x}}{\Gamma(\alpha)}\quad(x>0), \qquad E[X]=\frac{\alpha}{\lambda},\quad \text{Var}[X]=\frac{\alpha}{\lambda^2}.$$

Lo importante son sus parentescos:
- $\text{Gamma}(1,\lambda)=\text{Exp}(\lambda)$ — la exponencial es una Gamma con $\alpha=1$ (esperar **un** evento).
- $\text{Gamma}(n,\lambda)=$ suma de $n$ exponenciales independientes (esperar el $n$-ésimo evento).
- $\text{Gamma}(n/2,\,1/2)=\chi^2(n)$ — la chi-cuadrado es una Gamma disfrazada.

| $\alpha$ | $\lambda$ | Caso especial |
|---|---|----------------------|
| 1 | $\lambda$ | $\text{Exp}(\lambda)$ |
| $n$ entero | $\lambda$ | Erlang$(n,\lambda)$ |
| $n/2$ | $1/2$ | $\chi^2(n)$ |

Y se **reproduce**: $X_1\sim\text{Gamma}(\alpha_1,\lambda)$ más $X_2\sim\text{Gamma}(\alpha_2,\lambda)$ (misma escala) da $\text{Gamma}(\alpha_1+\alpha_2,\lambda)$ — apilar esperas suma los $\alpha$.

---

## La distribución Beta: una proporción en $(0,1)$

La **Beta** vive en $(0,1)$, así que es la distribución natural de una **probabilidad o proporción desconocida**:

$$f(x)=\frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}\quad(0<x<1), \qquad E[X]=\frac{\alpha}{\alpha+\beta}.$$

Piensa en $\alpha$ como "éxitos previos" y $\beta$ como "fracasos previos"; la media $\tfrac{\alpha}{\alpha+\beta}$ es la fracción de éxitos. Casos especiales: $\text{Beta}(1,1)=\text{Unif}[0,1]$. Y su vínculo con la Gamma: si $X\sim\text{Gamma}(\alpha)$, $Y\sim\text{Gamma}(\beta)$ (misma escala), entonces $\tfrac{X}{X+Y}\sim\text{Beta}(\alpha,\beta)$ — **la Beta es una Gamma normalizada a proporción**.

Su rol estrella: es el **prior conjugado** de la binomial. Prior $\text{Beta}(\alpha,\beta)$ + datos $\text{Bin}$ con $x$ éxitos en $n$ → posterior $\text{Beta}(\alpha+x,\,\beta+n-x)$. Actualizar es **sumar conteos** (conecta con [[arena-b4]]).

---

## Distribución $t$ de Student: la normal con incertidumbre en $\sigma$

Cuando estimas la media de datos normales pero **no conoces** $\sigma$ y la estimas de la muestra, el estadístico ya no es normal sino $t$:

$$t(\nu)=\frac{Z}{\sqrt{V/\nu}},\quad Z\sim N(0,1),\ V\sim\chi^2(\nu)\ \text{indep.}$$

Es simétrica alrededor de 0, pero con **colas más pesadas** que la normal (el denominador aleatorio añade incertidumbre). $E[X]=0$ para $\nu>1$ y $\text{Var}[X]=\tfrac{\nu}{\nu-2}$ para $\nu>2$. Casos límite: $t(1)=$ Cauchy (¡sin media ni varianza!) y $t(\nu)\to N(0,1)$ cuando $\nu\to\infty$. Su aplicación canónica: $T=\tfrac{\bar X-\mu}{S/\sqrt n}\sim t(n-1)$.

---

## Distribución $F$: cociente de varianzas

La **$F$** compara dos varianzas dividiendo dos chi-cuadrado (cada una escalada por sus grados de libertad):

$$F(m,n)=\frac{\chi^2(m)/m}{\chi^2(n)/n}, \qquad E[F]=\frac{n}{n-2}\ (n>2).$$

Aparece en el test de igualdad de varianzas ($F=S_1^2/S_2^2$) y en **ANOVA** (varianza entre grupos / varianza dentro). Si la $F$ es grande, la señal "entre grupos" supera al ruido "dentro".

---

## Distribución Lognormal: crecimiento multiplicativo

Si $\ln X\sim N(\mu,\sigma^2)$, entonces $X$ es **lognormal**. Modela cantidades que crecen de forma multiplicativa y no pueden ser negativas: precios de activos, ingresos, tamaños de partículas.

$$E[X]=e^{\mu+\sigma^2/2}, \qquad \text{mediana}=e^{\mu}, \qquad \text{Var}[X]=e^{2\mu+\sigma^2}(e^{\sigma^2}-1).$$

Ojo: la **media supera a la mediana** ($e^{\mu+\sigma^2/2}>e^\mu$) porque la cola derecha tira del promedio. Confundirlas distorsiona cualquier análisis de precios o ingresos (conecta con [[arena-q7]]).

---

## Distribución Weibull: tasas de fallo

La **Weibull** generaliza la exponencial para modelar fallos cuya tasa cambia con el tiempo:

$$F(x)=1-e^{-(x/\lambda)^k}\quad(x>0), \qquad E[X]=\lambda\,\Gamma(1+1/k).$$

El parámetro de forma $k$ dicta el comportamiento del hazard (la tasa instantánea de fallo):

| $k$ | Tasa de fallo |
|---|---------------|
| $k<1$ | decreciente (mortalidad infantil) |
| $k=1$ | constante (es la exponencial) |
| $k>1$ | creciente (envejecimiento) |

Es exactamente la forma del hazard que estudia el análisis de supervivencia (conecta con [[arena-h8]]).

---

## Familia binomial y familia Poisson

La **familia binomial** (ensayos discretos éxito/fracaso):

| Distribución | Modela |
|-------------|--------|
| Bernoulli$(p)$ | un ensayo |
| Bin$(n,p)$ | éxitos en $n$ ensayos |
| Geom$(p)$ | ensayos hasta el 1.er éxito |
| Bin. negativa$(r,p)$ | ensayos hasta el $r$-ésimo éxito |
| Hipergeométrica | éxitos en muestra **sin** reemplazo |

La **Poisson** (conteos de eventos raros), $P(X=k)=\tfrac{e^{-\lambda}\lambda^k}{k!}$, tiene tres propiedades que vale la pena saber:
- **Reproducción:** suma de Poissons independientes es Poisson (suma los $\lambda$).
- **Adelgazamiento:** si retienes cada evento de $\text{Poisson}(\lambda)$ con probabilidad $p$, lo retenido es $\text{Poisson}(\lambda p)$.
- **Condicional:** dado $X+Y=n$ (con $X\sim\text{Poisson}(\lambda)$, $Y\sim\text{Poisson}(\mu)$ indep.), $X\mid X+Y=n\sim\text{Bin}\!\big(n,\tfrac{\lambda}{\lambda+\mu}\big)$.

---

## Familia exponencial (el paraguas)

Muchísimas distribuciones se escriben en la forma

$$f(x\mid\theta)=h(x)\exp\!\big(\eta(\theta)\,T(x)-A(\theta)\big).$$

| Distribución | $\eta(\theta)$ | $T(x)$ |
|-------------|------|------|
| $N(\mu,1)$ | $\mu$ | $x$ |
| Poisson$(\lambda)$ | $\ln\lambda$ | $x$ |
| Bernoulli$(p)$ | $\text{logit}(p)$ | $x$ |

$T(x)$ es un **estadístico suficiente**: resume todo lo que los datos dicen del parámetro. Esta estructura común es la que hace que estas familias tengan priors conjugados y estimadores limpios (conecta con [[arena-cb1]] y [[arena-cb2]]).

---

## Mini-ejemplo trabajado: la Gamma es solo exponenciales apiladas

¿Cuánto esperas hasta el 3.er autobús si llegan como Poisson a tasa $\lambda=2$/hora? Cada espera entre autobuses es $\text{Exp}(2)$ con media $1/2$ h. El tiempo hasta el 3.º es la **suma de 3 exponenciales independientes** $=\text{Gamma}(3,2)$:

$$E[X]=\frac{\alpha}{\lambda}=\frac{3}{2}=1.5\text{ h}, \qquad \text{Var}[X]=\frac{\alpha}{\lambda^2}=\frac34.$$

No hay que integrar la densidad Gamma: "tiempo hasta el $n$-ésimo evento de Poisson" *es* $\text{Gamma}(n,\lambda)$ por construcción, igual que $\text{Gamma}(1,\lambda)=\text{Exp}(\lambda)$ y $\text{Gamma}(n/2,1/2)=\chi^2(n)$. Las distribuciones no son fichas sueltas: son la misma familia mirada desde ángulos distintos.

**Predicción antes de seguir:** si en vez del tiempo absoluto preguntas "¿qué fracción del tiempo total hasta los 5 autobuses transcurrió antes del 3.º?", ¿qué distribución aparece? Respuesta: una **Beta**. $\tfrac{X}{X+Y}$ con $X\sim\text{Gamma}(3)$, $Y\sim\text{Gamma}(2)$ es $\text{Beta}(3,2)$: la Beta es una Gamma *normalizada*, una proporción acotada en $(0,1)$. Por eso la Beta es el prior natural de una probabilidad.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "tiempo hasta el $n$-ésimo evento" → Gamma; "una proporción / probabilidad desconocida" → Beta; "cociente de varianzas" → F.
- **Contraejemplo ($t$ no siempre tiene varianza):** la $t(\nu)$ parece "casi normal", pero $t(1)=$ Cauchy no tiene media ni varianza, y $\text{Var}$ existe solo para $\nu>2$. Tratar toda $t$ como de cola ligera es el error.
- **Caso borde (lognormal):** $E[X]=e^{\mu+\sigma^2/2}>$ mediana $=e^\mu$ siempre. El borde recuerda que en distribuciones sesgadas a la derecha la media supera a la mediana — confundirlas distorsiona precios e ingresos.

## Errores típicos

- **Conceptual:** ver las distribuciones como una lista que memorizar en vez de una red de relaciones ($\text{Exp}\subset\text{Gamma}$, $\chi^2\subset\text{Gamma}$, Beta = Gamma normalizada, $t=Z/\sqrt{\chi^2/\nu}$).
- **Técnico:** usar la media $e^{\mu+\sigma^2/2}$ cuando se quería la mediana $e^\mu$ de una lognormal (o viceversa).
- **De supuestos:** aplicar el adelgazamiento de Poisson sin que las retenciones sean independientes entre eventos.

## Transferencia isomorfa

- **Beta conjugada ↔ actualización bayesiana de una proporción:** $\text{Beta}(\alpha,\beta)+\text{Bin}(n,x)\to\text{Beta}(\alpha+x,\beta+n-x)$; $\alpha,\beta$ son éxitos/fracasos previos (pseudo-conteos), el motor de toda inferencia de tasas (conecta con [[arena-b4]]).
- **Gamma (tiempo al $n$-ésimo evento) ↔ procesos de llegada:** colas, fallos de servidores y eventos de tráfico se modelan con el mismo proceso Poisson↔Gamma (conecta con [[arena-sre4]]).
- **Weibull (forma $k$) ↔ análisis de supervivencia:** $k<1,=1,>1$ son hazard decreciente/constante/creciente, exactamente la forma del hazard de Cox (conecta con [[arena-h8]]).
- **$t$ de cola pesada ↔ Cauchy y varianza infinita:** $\nu$ pequeño = colas gordas que rompen la intuición normal (conecta con [[arena-q11]]).
- **Lognormal ↔ precios de activos:** $\ln X$ normal modela precios, ingresos y tamaños multiplicativos (conecta con [[arena-q7]]).

Moraleja de la arista: *no memorices distribuciones; memoriza sus parentescos — la Gamma apila exponenciales, la Beta normaliza Gammas, y la mgf convierte cada relación en álgebra.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Tiempo hasta $n$-ésimo evento de Poisson" | $\text{Gamma}(n,\lambda)$ |
| "Fracción de dos Gammas" | $\text{Beta}(\alpha,\beta)$ |
| "Prior para proporción" | $\text{Beta}(\alpha,\beta)$ conjugado binomial |
| "Normal con $\sigma$ desconocida" | $t(n-1)$ |
| "Cociente de chi-cuadrados" | $F(m,n)$ |
| "$\ln(X)$ es normal" | $X$ es lognormal |
| "mgf de $N(\mu,\sigma^2)$ en $t=1$" | $e^{\mu+\sigma^2/2}$ |

---

> **Síntesis:** Las distribuciones no son listas de fórmulas — son familias relacionadas. La Gamma generaliza la Exp; la Beta es una Gamma normalizada; la $t$ es normal/chi; la $F$ es cociente de chi. El principio unificador: las mgf convierten todas estas relaciones en álgebra.

---

*Retrieval: cierra y responde: (1) $E$ y $\text{Var}$ de $\text{Gamma}(4,2)$; (2) distribución de $\tfrac{X}{X+Y}$ si $X\sim\text{Gamma}(3)$, $Y\sim\text{Gamma}(5)$; (3) $E[F(5,10)]$; (4) $E[X]$ y mediana de $X\sim\text{Lognormal}(1,1)$.*
