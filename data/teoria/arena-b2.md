# Variables aleatorias conjuntas y correlación

## De qué trata (y qué sabrás hacer)

Hasta ahora una variable aleatoria vivía sola. Aquí entran **dos o más a la vez**, y la pregunta nueva es cómo se relacionan: ¿saber una me dice algo de la otra? Ese vínculo se mide con la **covarianza** y la **correlación**, y se explota con dos leyes poderosísimas —la de la esperanza total y la de la varianza total— que resuelven problemas "anidados" (una variable que depende de otra aleatoria) condicionando y promediando.

Al terminar sabrás: leer una distribución conjunta y extraer marginales/condicionales, calcular covarianzas, reconocer que *correlación cero no es independencia*, y usar "condiciona y promedia" para medias y varianzas. Cada idea parte de un caso pequeño.

---

## Conjunta, marginal y condicional

La **conjunta** describe el par a la vez: $p_{X,Y}(x,y)=P(X=x,\,Y=y)$. De ella se obtiene todo lo demás:
- **Marginal** (olvidar la otra variable): $p_X(x)=\sum_y p_{X,Y}(x,y)$ — sumas la fila.
- **Condicional** (fijar una): $p_{Y\mid X}(y\mid x)=\dfrac{p_{X,Y}(x,y)}{p_X(x)}$ — reescalas a que sume 1.
- **Independencia:** $X\perp Y \iff p_{X,Y}(x,y)=p_X(x)\,p_Y(y)$ para todo $(x,y)$. La conjunta se factoriza: saber una no informa de la otra.

En el caso continuo, las sumas se vuelven integrales y la condición de independencia es idéntica: $f_{X,Y}(x,y)=f_X(x)\,f_Y(y)$.

---

## Covarianza y correlación

La **covarianza** mide si $X$ e $Y$ tienden a moverse juntas: positiva si cuando una sube la otra suele subir, negativa si una sube y la otra baja.

$$\text{Cov}(X,Y)=E[(X-\mu_X)(Y-\mu_Y)] = E[XY]-E[X]E[Y].$$

El problema de la covarianza es que su escala depende de las unidades. La **correlación** la normaliza a $[-1,1]$:

$$\rho(X,Y)=\frac{\text{Cov}(X,Y)}{\sigma_X\,\sigma_Y}\in[-1,1].$$

| Propiedad | Fórmula |
|-----------|---------|
| $\text{Cov}(aX+b,\,cY+d)$ | $ac\,\text{Cov}(X,Y)$ |
| $\text{Var}(X+Y)$ | $\text{Var}(X)+\text{Var}(Y)+2\,\text{Cov}(X,Y)$ |
| $X\perp Y \Rightarrow$ | $\text{Cov}=0$ (pero **no** al revés) |

**Atención — el contraejemplo clave:** $X\sim\text{Unif}(-1,1)$, $Y=X^2$. Entonces $\text{Cov}(X,Y)=E[X^3]=0$, pero $Y$ es función **determinista** de $X$: dependen totalmente. La covarianza solo detecta dependencia *lineal*. Correlación cero no es independencia (salvo en la normal bivariada, abajo).

---

## Normal bivariada

Cuando $(X,Y)$ es normal bivariada con correlación $\rho$, la mejor predicción de $Y$ dado $X$ es **lineal**:

$$E[Y\mid X=x]=\mu_Y + \rho\,\frac{\sigma_Y}{\sigma_X}\,(x-\mu_X).$$

Para variables estándar ($\mu=0,\sigma=1$): $E[Y\mid X=x]=\rho x$. Esta es la recta de regresión, y su pendiente es $\rho\,\sigma_Y/\sigma_X$. La normal bivariada tiene una propiedad especial que ninguna otra garantiza: aquí sí, $\text{Cov}=0\iff X\perp Y$.

---

## Ley de la esperanza total (condiciona y promedia)

A veces $E[Y]$ es difícil de golpe, pero fácil si **sabes** el valor de otra variable $X$. La ley de la esperanza total dice: calcula $E[Y\mid X]$ (fácil) y luego promédialo sobre $X$.

$$E[Y]=E\big[E[Y\mid X]\big].$$

Ejemplo — tiras un dado $X\in\{1,\ldots,6\}$ y luego lanzas $X$ monedas; $Y=$ número de caras. Dado $X=x$, $Y\sim\text{Bin}(x,\tfrac12)$, así que $E[Y\mid X]=X/2$. Entonces $E[Y]=E[X/2]=\tfrac{7/2}{2}=\tfrac74$. La táctica: **elige la $X$ que más simplifica** el problema condicional.

---

## Ley de la varianza total

La compañera para varianzas. La incertidumbre total de $Y$ se parte en dos: el ruido que queda **dentro** de cada escenario de $X$, más la variación **entre** escenarios.

$$\text{Var}[Y]=\underbrace{E\big[\text{Var}[Y\mid X]\big]}_{\text{ruido intra (within)}}+\underbrace{\text{Var}\big[E[Y\mid X]\big]}_{\text{variación entre (between)}}.$$

Es exactamente la descomposición de **ANOVA** (SS total = SS within + SS between) y prima hermana de la descomposición sesgo–varianza. Continuando el ejemplo: $\text{Var}[Y\mid X]=X/4$ y $E[Y\mid X]=X/2$, así que
$$E[\text{Var}[Y\mid X]]=\tfrac{E[X]}{4}=\tfrac78, \qquad \text{Var}[E[Y\mid X]]=\tfrac{\text{Var}[X]}{4}=\tfrac{35/12}{4}=\tfrac{35}{48},$$
y $\text{Var}[Y]=\tfrac78+\tfrac{35}{48}=\tfrac{77}{48}$.

---

## Función generatriz de momentos (mgf)

La **mgf** es una "huella digital" de la distribución que codifica todos sus momentos:

$$M_X(t)=E[e^{tX}], \qquad E[X^n]=M_X^{(n)}(0)\ (\text{la }n\text{-ésima derivada en }0).$$

Su superpoder: para variables **independientes**, la mgf de la suma es el producto de las mgf, $M_{X+Y}(t)=M_X(t)M_Y(t)$ (convierte convoluciones en multiplicaciones).

| Distribución | $M_X(t)$ |
|-------------|--------|
| $N(\mu,\sigma^2)$ | $e^{\mu t+\sigma^2 t^2/2}$ |
| Poisson$(\lambda)$ | $e^{\lambda(e^t-1)}$ |
| Exp$(\lambda)$ | $\dfrac{\lambda}{\lambda-t}$ para $t<\lambda$ |
| Bin$(n,p)$ | $(pe^t+1-p)^n$ |

Truco útil: $E[e^X]$ para $X\sim N(\mu,\sigma^2)$ es simplemente $M_X(1)=e^{\mu+\sigma^2/2}$ — el puente a la lognormal (conecta con [[arena-q7]]).

---

## Chi-cuadrado: cuadrados de normales

Si $X_1,\ldots,X_n\sim N(0,1)$ independientes, entonces $X_1^2+\cdots+X_n^2\sim\chi^2(n)$, con $E=n$ y $\text{Var}=2n$. Es un caso de la Gamma: $\chi^2(n)=\text{Gamma}(n/2,1/2)$. Aparece en toda la inferencia clásica; por ejemplo, para una muestra normal, $\tfrac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)$ (la varianza muestral tiene distribución chi-cuadrado).

---

## Propiedades de la normal

Si $X\sim N(\mu,\sigma^2)$:
- $aX+b\sim N(a\mu+b,\,a^2\sigma^2)$ — las transformaciones lineales preservan la normalidad.
- Si $Y\sim N(\nu,\tau^2)$ independiente: $X+Y\sim N(\mu+\nu,\,\sigma^2+\tau^2)$.
- Momentos pares de $N(0,1)$: $E[X^{2k}]=(2k-1)!!=1\cdot3\cdot5\cdots(2k-1)$, así $E[X^2]=1,\ E[X^4]=3,\ E[X^6]=15$; y $E[|X|]=\sqrt{2/\pi}\approx0.798$.

---

## Estadísticos de orden

$X_1,\ldots,X_n$ i.i.d. $\text{Unif}[0,1]$, ordenados $X_{(1)}\le\cdots\le X_{(n)}$. El $k$-ésimo cumple

$$E[X_{(k)}]=\frac{k}{n+1}.$$

Los $n$ puntos parten $[0,1]$ en $n+1$ huecos de tamaño esperado $\tfrac1{n+1}$. Para $n=4$: las medias son $\tfrac15,\tfrac25,\tfrac35,\tfrac45$. Es la base de los gráficos cuantil-cuantil.

---

## Desigualdades

| Desigualdad | Enunciado |
|------------|-----------|
| Markov | $P(X\ge a)\le E[X]/a$ para $X\ge 0$ |
| Chebyshev | $P(|X-\mu|\ge k\sigma)\le 1/k^2$ |
| Jensen | $E[f(X)]\ge f(E[X])$ si $f$ convexa |
| Cauchy–Schwarz | $(E[XY])^2\le E[X^2]\,E[Y^2]$ |

Jensen implica $E[X^2]\ge(E[X])^2$ (la varianza es $\ge0$), $E[e^X]\ge e^{E[X]}$ y $E[1/X]\ge 1/E[X]$ para $X>0$.

---

## Mini-ejemplo trabajado: dado que decide cuántas monedas (LET + LVT)

Tiras un dado justo ($X\in\{1..6\}$) y luego lanzas $X$ monedas; $Y=$ número de caras. Calcular $E[Y]$ y $\text{Var}[Y]$ directamente es engorroso, pero **condicionar en $X$** lo vuelve mecánico.

- **Esperanza total:** dado $X=x$, $Y\sim\text{Bin}(x,\tfrac12)$, así que $E[Y\mid X]=X/2$. Entonces $E[Y]=E[X/2]=\tfrac{7/2}{2}=\tfrac74$.
- **Varianza total:** $\text{Var}[Y\mid X]=X\cdot\tfrac14$ y $E[Y\mid X]=X/2$.
  - Componente intra: $E[\text{Var}[Y\mid X]]=\tfrac{E[X]}{4}=\tfrac78$.
  - Componente entre: $\text{Var}[E[Y\mid X]]=\tfrac{\text{Var}[X]}{4}=\tfrac{35/12}{4}=\tfrac{35}{48}$.
  - $\text{Var}[Y]=\tfrac78+\tfrac{35}{48}=\tfrac{42}{48}+\tfrac{35}{48}=\tfrac{77}{48}$.

La moraleja operativa: *condiciona en la variable que más reduce la incertidumbre y luego promedia.*

**Predicción antes de seguir:** ¿qué representa el término $\text{Var}[E[Y\mid X]]=\tfrac{35}{48}$? Respuesta: la varianza de $Y$ que **el dado explica** (la parte "between"); $E[\text{Var}[Y\mid X]]=\tfrac78$ es el ruido de las monedas que el dado *no* explica (la parte "within"). Es exactamente la partición de ANOVA y la descomposición sesgo–varianza.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** $Y$ depende de una $X$ aleatoria → esperanza total para la media, varianza total para la varianza ("condiciona y promedia").
- **Contraejemplo ($\text{Cov}=0 \ne$ independencia):** $X\sim\text{Unif}(-1,1)$, $Y=X^2$. $\text{Cov}(X,Y)=E[X^3]=0$, pero $Y$ es función determinista de $X$. $\text{Cov}=0$ solo descarta dependencia *lineal* — salvo en la normal bivariada, donde sí equivale a independencia.
- **Caso borde (Jensen):** para $f$ convexa, $E[f(X)]\ge f(E[X])$; por eso $E[e^X]=e^{\mu+\sigma^2/2}>e^{E[X]}=e^\mu$. El "extra" $\sigma^2/2$ no es error: es la convexidad.

## Errores típicos

- **Conceptual:** leer $\text{Cov}=0$ como independencia fuera de la normal bivariada.
- **Técnico:** en la varianza total, olvidar el término $\text{Var}[E[Y\mid X]]$ y reportar solo el ruido intra-grupo, subestimando $\text{Var}[Y]$.
- **De supuestos:** aplicar $M_{X+Y}=M_X M_Y$ sin que $X,Y$ sean independientes (la factorización de la mgf exige independencia).

## Transferencia isomorfa

- **Esperanza total ↔ torre de la esperanza:** $E[Y]=E[E[Y\mid X]]$ es la misma ley que resuelve la geométrica y la parada óptima condicionando en el primer paso (conecta con [[arena-q6]]).
- **Varianza total ↔ descomposición sesgo-varianza:** within + between es error irreducible + varianza explicada en ML (conecta con [[arena-iml4]]).
- **mgf gaussiana $e^{\mu t+\sigma^2 t^2/2}$ ↔ valoración lognormal:** evaluarla en $t=1$ da $E[e^X]$, el puente directo al precio lognormal y a la prima de Jensen (conecta con [[arena-q7]]).
- **Estadísticos de orden $E[X_{(k)}]=\tfrac{k}{n+1}$ ↔ cuantiles muestrales:** los $n$ puntos parten $[0,1]$ en $n+1$ huecos iguales en esperanza, la base de los plots cuantil-cuantil.

Moraleja de la arista: *para variables anidadas, condiciona y promedia; la varianza total siempre se parte en "lo que la condición explica" más "lo que deja como ruido".*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "$E[Y]$ donde $Y$ depende de $X$ random" | Esperanza total: $E[E[Y\mid X]]$ |
| "$\text{Var}[Y]$ con mezcla de fuentes" | Varianza total: $E[\text{Var}[Y\mid X]]+\text{Var}[E[Y\mid X]]$ |
| "$E[e^X]$ para $X$ normal" | mgf en $t=1$: $e^{\mu+\sigma^2/2}$ |
| "Suma de cuadrados de normales" | Chi-cuadrado: $\chi^2(n)$ |
| "$\text{Cov}=0$, ¿independencia?" | Solo para normal bivariada; en general no |
| "$E[Y\mid X]$ para normal bivariada" | $\mu_Y+\rho\tfrac{\sigma_Y}{\sigma_X}(x-\mu_X)$ |
| "$E[k$-ésimo estadístico de orden de Unif$]$" | $\tfrac{k}{n+1}$ |

---

> **Síntesis:** Las leyes de esperanza y varianza total son las herramientas para calcular $E$ y $\text{Var}$ de variables que dependen de otra aleatoria — "condiciona en lo que más sabe y luego promedia". La mgf codifica todos los momentos y convierte la convolución en multiplicación. Chi-cuadrado surge de cuadrados de normales, base de toda la inferencia clásica.

---

*Retrieval: cierra y responde: (1) $E[Y]$ y $\text{Var}[Y]$ para $Y=$ suma de $N$ monedas con $N\sim\text{Poisson}(5)$; (2) $E[e^{2X}]$ para $X\sim N(3,4)$; (3) $E[X_{(3)}]$ para 5 $\text{Unif}[0,1]$; (4) $\text{Cov}(X,Y)$ si $\text{Var}[X+Y]=10$, $\text{Var}[X]=4$, $\text{Var}[Y]=3$.*
