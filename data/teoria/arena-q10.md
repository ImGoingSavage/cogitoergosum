# Arena Quant · Distribuciones, geometría y estadísticos de orden

## De qué trata (y qué sabrás hacer)

Dos atajos visuales resuelven una enorme familia de problemas. El primero: cuando hay **dos cantidades uniformes al azar**, piénsalas como un **punto lanzado en un cuadrado**, y la probabilidad se vuelve un **área**. El segundo: cuando el enunciado dice "el máximo / el mínimo / el $k$-ésimo", es un **estadístico de orden**, con fórmulas cerradas. Ambos evitan integrar a ciegas.

Al terminar sabrás traducir "¿probabilidad de que…?" en una región del cuadrado unitario y medir su área, calcular $E[\max]$, $E[\min]$ y el $k$-ésimo orden, y reconocer el truco de la transformada integral (aplicar la CDF a su propia variable la vuelve uniforme). Cada idea se construye desde un dibujo concreto.

---

## Probabilidad como área

La idea raíz: **dos uniformes en $[0,1]$ son un punto $(x,y)$ lanzado al azar dentro del cuadrado unitario**, y como el área total es 1, la probabilidad de un evento es exactamente la fracción del cuadrado donde se cumple.

- **Romeo y Julieta** llegan al azar entre las 9 y las 10; cada uno espera 15 min. ¿$P(\text{se encuentran})$? Con $x,y$ uniformes en $[0,1]$, se encuentran si $|x-y|\le\tfrac14$. El complemento son dos triángulos que juntan un área $(\tfrac34)^2=\tfrac9{16}$. Respuesta: $1-\tfrac9{16}=\tfrac7{16}$.
- **Palo roto:** rompes un palo en dos puntos uniformes; los tres trozos forman triángulo si ninguno supera $\tfrac12$. En el cuadrado, la región válida tiene área $\tfrac14$.

La metáfora rectora: "dos uniformes → un punto en el cuadrado; la pregunta es qué fracción del cuadrado cumple la condición".

---

## El problema del avión (asientos)

100 personas abordan en orden; la primera (la abuela) se sienta al azar; cada siguiente toma su asiento si está libre, y si no, uno al azar. ¿$P(\text{el pasajero 100 acaba en SU asiento})$?

No hace falta álgebra: **condiciona en el evento que colapsa el problema**. El asiento de la abuela (1) y el del último pasajero (100) son los dos asientos "especiales"; por simetría, el primer pasajero forzado a elegir cae en uno u otro con igual probabilidad, y eso decide el destino del 100. Respuesta: $\tfrac12$. Es el ejemplo canónico de buscar el evento que vuelve trivial el problema.

---

## Estadísticos de orden de uniformes

Tienes $n$ uniformes i.i.d. en $[0,1]$. El **máximo** es $\le x$ solo si **todos** lo son, así que $P(\max\le x)=x^n$. Derivando obtienes la densidad $n x^{n-1}$ y de ahí

$$E[\max]=\frac{n}{n+1}.$$

Por simetría $E[\min]=\tfrac{1}{n+1}$, y por linealidad $E[\max-\min]=\tfrac{n-1}{n+1}$. En general, la densidad del $k$-ésimo ordenado es

$$f_{(k)}(x)=\frac{n!}{(k-1)!\,(n-k)!}\,f(x)\,F(x)^{k-1}\,(1-F(x))^{n-k},$$

que para uniformes es una Beta. El factor combinatorio cuenta de cuántas formas los datos se reparten en "menores que $x$, igual a $x$, mayores que $x$".

---

## Convolución: la densidad de una suma

La densidad de $X+Y$ (variables independientes) es la **convolución** de sus densidades: $h(z)=\int f(z-y)g(y)\,dy$. Para $X,Y\sim\text{Unif}(0,1)$ sale una densidad **triangular**: $h(z)=z$ en $[0,1]$ y $h(z)=2-z$ en $[1,2]$ (sumar dos uniformes concentra masa en el centro, como dos dados favorecen el 7). Patrón general: sumar variables = convolucionar densidades.

---

## Dos joyas de la gaussiana

- Para $X\sim N(\mu,\sigma^2)$: $E[X^2]=\sigma^2+\mu^2$ (de $\text{Var}=E[X^2]-(E[X])^2$), y la mgf $E[e^{\lambda X}]=e^{\mu\lambda+\sigma^2\lambda^2/2}$ — la base de la valoración lognormal (conecta con [[arena-q7]]).
- Si $\Phi$ es la CDF normal estándar y $X\sim N(0,1)$, entonces $\Phi(X)\sim\text{Unif}(0,1)$ por la **transformada integral de probabilidad**, así que $E[\Phi(X)]=\tfrac12$. Aplicar la propia CDF a su variable la uniformiza — por eso los $p$-valores son uniformes bajo $H_0$.

---

## Teorema del límite central (lo que de verdad dice)

Para $X_1,\ldots,X_n$ i.i.d. con media $\mu$ y varianza $\sigma^2$ **finita**, la suma estandarizada converge en distribución a una normal:

$$\frac{S_n-\mu n}{\sigma\sqrt n}\xrightarrow{d} N(0,1),$$

sin importar la distribución de partida. La condición crítica es el **segundo momento finito**: por eso la Cauchy (sin varianza) no obedece. Dato relacionado: una matriz de covarianzas siempre es semidefinida positiva porque $\text{Var}(a^\top X)=a^\top C a\ge0$ para todo $a$.

---

## Mini-ejemplo trabajado: Romeo y Julieta como un área

Dos uniformes en $[0,1]$ son un punto $(x,y)$ lanzado al azar dentro del cuadrado unitario. Se encuentran si $|x-y|\le\tfrac14$. El **complemento** (no se encuentran) son dos triángulos rectángulos: cada uno con catetos de $\tfrac34$, área $\tfrac12(\tfrac34)^2=\tfrac{9}{32}$, y juntos $\tfrac9{16}$. Por tanto $P(\text{encuentro})=1-\tfrac9{16}=\tfrac7{16}$.

El truco mental: no integres, **dibuja**. La pregunta "¿qué fracción del cuadrado cumple $|x-y|\le\tfrac14$?" se responde restando dos triángulos.

**Predicción antes de seguir:** si cada uno esperara 30 min (umbral $\tfrac12$) en vez de 15, ¿la probabilidad de encuentro se duplica? Respuesta: **no, crece más** — sube a $1-(\tfrac12)^2=\tfrac34$. La relación es cuadrática en el complemento, no lineal: los triángulos encogen con el *cuadrado* del umbral. Intuir "doble espera = doble probabilidad" es el error típico.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** dos (o tres) uniformes → punto en el cuadrado (cubo); la probabilidad es un área (volumen). Romeo-Julieta, palo roto.
- **Contraejemplo (uniforme en el radio):** en la diana, suponer el radio uniforme está mal; el área crece con $r$, así que la densidad del radio es $2r$, no constante. "Uniforme en el área" $\ne$ "uniforme en el radio".
- **Caso borde (problema del avión):** condicionar en el evento que colapsa —el primer desplazado acaba en el asiento 1 o el 100, simétricos— da $\tfrac12$ sin álgebra. El borde enseña a buscar el evento que vuelve trivial el problema.

## Errores típicos

- **Conceptual:** integrar a ciegas en vez de dibujar la región; o confundir uniforme-en-área con uniforme-en-radio.
- **Técnico:** olvidar el factor combinatorio $\tfrac{n!}{(k-1)!(n-k)!}$ en la densidad del $k$-ésimo estadístico de orden.
- **De interpretación:** tratar $E[\max]$ y $E[\min]$ como independientes; por simetría $E[\min]=1-E[\max]$ en uniformes $[0,1]$.

## Transferencia isomorfa

- **Probabilidad como área ↔ integración Monte Carlo:** estimar $P$ como fracción de puntos que caen en una región es exactamente cómo Monte Carlo aproxima integrales; el cuadrado unitario es el espacio muestral (conecta con [[arena-fc2]]).
- **Estadísticos de orden (máx/mín) ↔ valores extremos / VaR:** $E[\max]$ de $n$ muestras es la semilla de la teoría de valores extremos que sostiene el cálculo de pérdidas de cola (conecta con [[arena-q6]]).
- **mgf gaussiana $e^{\mu\lambda+\sigma^2\lambda^2/2}$ ↔ valoración lognormal:** esta función generatriz es el puente directo a $E[e^X]$ y al precio lognormal (conecta con [[arena-q7]]).
- **Transformada integral $\Phi(X)\sim\text{Unif}(0,1)$ ↔ $p$-valores uniformes:** aplicar la CDF a su variable la uniformiza; por eso, bajo $H_0$, los $p$-valores son $\text{Unif}(0,1)$ (conecta con [[arena-q6]]).

Moraleja de la arista: *dos uniformes son un punto en el cuadrado; "máx/mín/$k$-ésimo" es un estadístico de orden; y aplicar la CDF a su propia variable la aplana a $\text{Unif}(0,1)$.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "dos tiempos/longitudes al azar" | dibuja un punto en el cuadrado, mide el área |
| "máx / mín / $k$-ésimo de $n$" | estadístico de orden; $E[\max]=\tfrac{n}{n+1}$ |
| "densidad de una suma" | convolución de densidades |
| "$E[e^{\lambda X}]$, $X$ normal" | mgf lognormal $e^{\mu\lambda+\sigma^2\lambda^2/2}$ |
| "aplica la CDF a su variable" | sale uniforme → $E=\tfrac12$ |

---

> ❧ **Síntesis:** geometría para probabilidades de uniformes (área en el cuadrado), estadísticos de orden para máx/mín/$k$-ésimo, convolución para sumas, y la mgf gaussiana $e^{\mu\lambda+\sigma^2\lambda^2/2}$ como puente hacia la valoración lognormal. El TLC funciona solo con segundo momento finito.

---

*Retrieval: cierra la página y responde — (1) $P(\text{Romeo y Julieta se encuentran})$; (2) $P(\text{pasajero 100 en su asiento})$; (3) $E[\max]$ de $n$ uniformes; (4) $E[e^{\lambda X}]$ para $X\sim N(\mu,\sigma^2)$.*
