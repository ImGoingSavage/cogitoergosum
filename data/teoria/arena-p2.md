# Combinatoria y probabilidad discreta

## De qué trata (y qué sabrás hacer)

Muchos problemas de entrevista no piden creatividad: piden **reconocer el modelo**. "Caminos en una cuadrícula", "tiempo hasta el $r$-ésimo éxito", "dos procesos que compiten" — cada uno tiene una fórmula cerrada. La habilidad es traducir el enunciado al modelo correcto; el cálculo es entonces mecánico.

Esta lección es ese catálogo, pero construido: cada modelo se motiva con un caso pequeño antes de soltar la fórmula, y verás cómo se conectan entre sí (la binomial negativa generaliza la geométrica; la hipergeométrica es la binomial sin reemplazo; la Poisson es la binomial de eventos raros). Al final, ante un enunciado nuevo, sabrás preguntarte "¿de qué familia es esto?".

---

## Caminos en una retícula

Vas de $(0,0)$ a $(m,n)$ moviéndote solo a la **derecha** $(+1,0)$ o hacia **arriba** $(0,+1)$. ¿Cuántas rutas hay? Toda ruta usa exactamente $m+n$ pasos, de los cuales $m$ son "derecha" y $n$ son "arriba". Elegir la ruta es elegir **cuáles** de los $m+n$ pasos serán "arriba":

$$\text{número de caminos} = \binom{m+n}{n}.$$

Para $(4,3)$: $\binom{7}{3}=35$. Con obstáculos (casillas prohibidas), la fórmula cerrada se rompe y se usa programación dinámica o el principio de reflexión. La idea transferible: **un camino monótono es una secuencia de decisiones binarias**, y contar secuencias con cierto número de "unos" es un coeficiente binomial.

---

## Técnica del complemento

Cuando el enunciado dice "al menos uno", contar de frente obliga a sumar muchos casos. El complemento lo evita:

$$P(\text{al menos uno}) = 1 - P(\text{ninguno}).$$

Ejemplo — $P(\text{al menos un as en 5 cartas})$. "Ninguno" es un solo cociente (manos sin ases entre todas las manos):

$$1 - \frac{\binom{48}{5}}{\binom{52}{5}} = 1 - 0.6588 = 0.3412.$$

---

## Stars and bars (composiciones)

¿De cuántas formas reparten $n$ caramelos idénticos entre $k$ niños? Imagina los $n$ caramelos en fila como estrellas y pon $k-1$ "barras" para separarlos en $k$ grupos. Cada arreglo de estrellas y barras es un reparto:

$$\#\{x_1+\cdots+x_k=n,\ x_i\ge 0\} = \binom{n+k-1}{k-1}.$$

Si cada niño debe recibir **al menos uno** ($x_i\ge 1$), regala uno a cada uno primero ($y_i=x_i-1$, $\sum y_i=n-k$) y aplica la fórmula: $\binom{n-1}{k-1}$.

Para $x_1+\cdots+x_4=10$: con $x_i\ge0$, $\binom{13}{3}=286$; con $x_i\ge1$, $\binom{9}{3}=84$.

---

## Permutaciones con repetición

$n$ objetos donde hay repetidos con multiplicidades $n_1,\ldots,n_k$ (con $\sum n_i=n$): cuenta como si todos fueran distintos ($n!$) y divide por las reordenaciones internas de cada grupo idéntico, que no producen arreglos nuevos:

$$\frac{n!}{n_1!\,n_2!\cdots n_k!}.$$

MISSISSIPPI (M×1, I×4, S×4, P×2): $\dfrac{11!}{1!\,4!\,4!\,2!}=34650$.

---

## Desarreglos (derangements)

Un **desarreglo** es una permutación donde **nadie** queda en su sitio original (cero puntos fijos). Por inclusión-exclusión sobre "la persona $i$ sí queda fija":

$$D(n) = n!\sum_{k=0}^{n}\frac{(-1)^k}{k!}, \qquad \frac{D(n)}{n!}\xrightarrow{n\to\infty} e^{-1}\approx 0.3679.$$

| $n$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $D(n)$ | 0 | 1 | 2 | 9 |

Para $n\ge3$, $D(n)\approx \text{round}(n!/e)$. El $1/e$ es la probabilidad de que una permutación al azar no tenga ningún punto fijo (conecta con [[arena-fc1]]).

---

## Estadísticos de orden de uniformes discretas

Sacas $n$ valores (con reemplazo) de $\{1,\ldots,N\}$ y los ordenas. El $k$-ésimo de menor a mayor tiene, en promedio,

$$E[X_{(k)}] = \frac{k(N+1)}{n+1}.$$

Así $E[\text{mínimo}]=\tfrac{N+1}{n+1}$ y $E[\text{máximo}]=\tfrac{n(N+1)}{n+1}$. Intuición: los $n$ valores reparten el rango $\{1,\ldots,N\}$ en $n+1$ huecos de tamaño esperado igual. Para $n=3,N=10$: $E[\text{máx}]=\tfrac{3\cdot11}{4}=8.25$.

---

## Ruina del jugador

Apuestas \$1 por ronda; ganas con probabilidad $p$. Empiezas con $k$ y juegas hasta llegar a $N$ (ganar) o a $0$ (quebrar). ¿Probabilidad de ganar?

| Caso | $P(\text{llegar a }N)$ | $E[\text{duración}]$ |
|------|--------------|-------------|
| $p=\tfrac12$ (justo) | $k/N$ | $k(N-k)$ |
| $p\ne\tfrac12$ | $\dfrac{1-\rho^{k}}{1-\rho^{N}}$, con $\rho=\dfrac{1-p}{p}$ | más compleja |

Cuando el juego es **justo**, la probabilidad de ganar es simplemente tu fracción del objetivo, $k/N$ (esto sale de que tu fortuna es una martingala — ver [[arena-q11]]). Pero una pequeña desventaja se compone brutalmente: con $p=0.45$, $N=10$, $k=5$, da $P\approx 32.8\%$ en vez del 50%. La casa no necesita mucha ventaja.

---

## Aproximación de Poisson

Para "muchos ensayos, cada uno improbable" (clientes que llegan, defectos en un lote, mutaciones), la binomial $\text{Bin}(n,p)$ con $n$ grande y $p$ pequeño se aproxima por

$$\text{Poisson}(\lambda),\quad \lambda=np: \quad P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!}, \quad E[X]=\text{Var}[X]=\lambda.$$

Para $n=1000$, $p=0.003$: $\lambda=3$, y $P(0\text{ defectos})=e^{-3}\approx 4.98\%$. La firma de la Poisson: media y varianza **iguales**.

---

## Distribución exponencial — falta de memoria

La exponencial modela el **tiempo de espera** de un proceso sin desgaste. Su propiedad definitoria:

$$P(X>s+t\mid X>s) = P(X>t).$$

"Ya esperé $s$ y no ha pasado nada" no cambia lo que falta: el proceso **no tiene memoria**. Es la única distribución continua con esa propiedad (su análoga discreta es la geométrica). Para dos exponenciales independientes $X\sim\text{Exp}(\lambda)$, $Y\sim\text{Exp}(\mu)$:

$$P(X<Y)=\frac{\lambda}{\lambda+\mu}, \qquad \min(X,Y)\sim\text{Exp}(\lambda+\mu).$$

---

## Estadísticos de orden de uniformes continuas

Si $X_1,\ldots,X_n$ son i.i.d. $\text{Uniforme}[0,1]$, el $k$-ésimo ordenado cumple

$$E[X_{(k)}]=\frac{k}{n+1}.$$

Los $n$ puntos parten $[0,1]$ en $n+1$ intervalos de longitud esperada $\tfrac{1}{n+1}$ — el continuo del modelo discreto anterior.

---

## Desigualdades probabilísticas

Cuando no conoces la distribución completa pero sí algún momento, estas cotas te dan garantías:

| Desigualdad | Enunciado | Supuesto |
|------------|-----------|---------|
| Markov | $P(X\ge a)\le \dfrac{E[X]}{a}$ | $X\ge 0$ |
| Chebyshev | $P(|X-\mu|\ge k\sigma)\le \dfrac{1}{k^2}$ | $\text{Var}(X)<\infty$ |
| Jensen | $E[f(X)]\ge f(E[X])$ | $f$ convexa |

Chebyshev da $P(|X-\mu|\ge 2\sigma)\le 25\%$ (para la normal el valor real es $\approx 4.6\%$: la cota es floja pero **universal**). Jensen explica por qué $E[e^X]\ge e^{E[X]}$ y $E[X^2]\ge (E[X])^2$ (la varianza es $\ge0$).

---

## Coleccionista de cupones

Hay $n$ tipos de cromo; cada sobre trae uno al azar. ¿Cuántos sobres para completar la colección? Cuando ya tienes $k$ tipos distintos, la probabilidad de que el siguiente sea nuevo es $\tfrac{n-k}{n}$, así que esperas $\tfrac{n}{n-k}$ sobres para conseguirlo. Sumando:

$$E[T]=\sum_{k=0}^{n-1}\frac{n}{n-k}=n\,H_n=n\left(1+\tfrac12+\cdots+\tfrac1n\right).$$

Para $n=6$: $E[T]\approx 6\times 2.45\approx 14.7$. El número armónico $H_n\approx\ln n$ vuelve en récords y cobertura de caché (conecta con [[arena-q6]]).

---

## Mini-ejemplo trabajado: "al menos un as" por complemento

$P(\text{al menos un as en 5 cartas de una baraja de 52})$. Contar directamente "exactamente 1, 2, 3, 4 ases" y sumar es laborioso. El complemento lo vuelve trivial:

$$P(\text{al menos uno}) = 1 - P(\text{ninguno}) = 1 - \frac{\binom{48}{5}}{\binom{52}{5}} = 1 - 0.6588 = 0.3412.$$

$\binom{48}{5}$ cuenta las manos sin ningún as; dividir entre todas las manos da $P(\text{ninguno})$, y 1 menos eso es la respuesta. Un solo cociente en vez de cuatro sumandos.

**Predicción antes de seguir:** ¿cuándo el complemento NO ayuda? Respuesta: cuando "ninguno" es tan complejo como "al menos uno" — por ejemplo, "exactamente 2 ases" no tiene complemento simple. La regla: el complemento brilla para "al menos uno / al menos un éxito", porque "ninguno" suele ser un producto limpio de probabilidades. Reconocer la forma "al menos uno" es la señal.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** reconoce el modelo → retícula $\binom{m+n}{n}$, stars and bars $\binom{n+k-1}{k-1}$, ruina $k/N$, Poisson$(np)$, competencia de exponenciales.
- **Contraejemplo (ruina con desventaja):** con $p=0.45$ (no $0.5$), $P(\text{llegar a }N)$ no es $k/N$ sino $\tfrac{1-\rho^k}{1-\rho^N}$ con $\rho=q/p$; una desventaja del 5% compuesta es devastadora ($32.8\%$ vs $50\%$).
- **Caso borde (exponencial sin memoria):** $P(X>s+t\mid X>s)=P(X>t)$; el tiempo ya esperado no cambia el restante. La única continua con esa propiedad — el borde la define.

## Errores típicos

- **Conceptual:** usar la fórmula simétrica $k/N$ de la ruina cuando el juego no es justo ($p\ne\tfrac12$).
- **Técnico:** en stars and bars, confundir el caso $x_i\ge0$ ($\binom{n+k-1}{k-1}$) con $x_i\ge1$ ($\binom{n-1}{k-1}$).
- **De supuestos:** aproximar $\text{Bin}(n,p)$ por Poisson cuando $p$ no es pequeño (la aproximación pide $n$ grande, $p$ chico, $\lambda=np$ moderado).

## Transferencia isomorfa

- **Complemento "al menos uno" ↔ palomar y conteo:** $1-P(\text{ninguno})$ es el mismo atajo que resuelve garantías y coincidencias (conecta con [[arena-fc1]]).
- **Derangements ($D(n)/n!\to 1/e$) ↔ puntos fijos y el secretario:** el $1/e$ reaparece en sombreros y parada óptima (conecta con [[arena-fc1]]).
- **Ruina del jugador ↔ muestreo opcional / barreras:** $P(\text{absorción})$ lineal en $p=\tfrac12$ sale del argumento de martingala (conecta con [[arena-q11]] y [[arena-fc4]]).
- **$\min(X,Y)\sim\text{Exp}(\lambda+\mu)$, $P(X<Y)=\tfrac{\lambda}{\lambda+\mu}$ ↔ proceso de Poisson:** competir exponenciales es el mecanismo de las llegadas y la Gamma (conecta con [[arena-b3]] y [[arena-ads1]]).
- **Coleccionista $n H_n$ ↔ récords y caché:** el número armónico cuenta cupones, récords y cobertura (conecta con [[arena-q6]]).

Moraleja de la arista: *el trabajo está en reconocer el modelo, no en calcular; "al menos uno" pide complemento, y una desventaja compuesta en la ruina es letal.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Caminos en retícula $m\times n$ | $\binom{m+n}{n}$ |
| "Al menos uno" | Complemento: $1-P(\text{ninguno})$ |
| Enteros $x_i\ge0$ sumando $n$ en $k$ variables | $\binom{n+k-1}{k-1}$ |
| Permutaciones sin punto fijo | $D(n)\approx\text{round}(n!/e)$ |
| $E[\max$ de $n$ draws de $\{1..N\}]$ | $\tfrac{n(N+1)}{n+1}$ |
| Paseo entre $0$ y $N$, $p=\tfrac12$ | $P(N)=k/N$; duración $=k(N-k)$ |
| Eventos raros ($n$ grande, $p$ pequeño) | Poisson con $\lambda=np$ |
| Dos exponenciales compiten | $P(X<Y)=\tfrac{\lambda}{\lambda+\mu}$; $\min\sim\text{Exp}(\lambda+\mu)$ |
| Coleccionar $n$ tipos | $E[T]=n H_n$ |

---

> **Síntesis:** La combinatoria y la probabilidad discreta son un catálogo de modelos bien definidos: retícula ($\binom{m+n}{n}$), desarreglos ($1/e$), ruina ($k/N$), Poisson (eventos raros), exponencial (competencia de procesos). Reconocer el modelo correcto reduce el problema a una fórmula; el esfuerzo está en el reconocimiento, no en el cálculo.

---

*Retrieval: sin mirar: (1) caminos de $(0,0)$ a $(3,3)$; (2) $P(X<Y)$ si $X\sim\text{Exp}(2)$, $Y\sim\text{Exp}(3)$; (3) $E[\max$ de 4 draws de $\{1..10\}]$; (4) $D(5)$.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puentes de regreso

La combinatoria discreta de la Arena no vive aislada: [[zeitz-43]] empaqueta conteos en funciones generatrices, [[zeitz-64]] convierte estructuras en recurrencias, y [[engel-suc]] entrena sucesiones donde el estado correcto decide si la cuenta cierra.
<!-- GRAFO_CONEXO_OLEADA3_END -->
