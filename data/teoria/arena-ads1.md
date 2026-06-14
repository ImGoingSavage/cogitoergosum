# Probabilidad para entrevistas de ciencia de datos

## Probabilidad condicional y Bayes

La probabilidad de A dado que ocurrió B se invierte con **Bayes**:

$$P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}$$

- **Prior** $P(A)$ — lo que creías antes del dato.
- **Likelihood** $P(B\mid A)$ — qué tan compatible es el dato con la hipótesis.
- **Posterior** $P(A\mid B)$ — la creencia actualizada.

A y B son **independientes** si $P(A\mid B)=P(A)$ (saber B no informa sobre A). Señal verbal en la entrevista: las palabras *"dado que"* casi siempre piden Bayes. El caso canónico es el **test de enfermedad rara**: aunque el test sea "98% preciso", la baja tasa base hace que la mayoría de positivos sean falsos. No diagnostiques sin la tasa base.

## Ley de probabilidad total

Si los $B_i$ particionan el espacio (disjuntos y exhaustivos):

$$P(A)=\sum_i P(A\mid B_i)\,P(B_i)$$

Sirve cuando la probabilidad depende de un **árbol de escenarios**: descompón A en la suma ponderada por cada rama. Ejemplo: probabilidad de que un cliente compre, condicionada al segmento al que pertenece.

## Conteo

- **Permutaciones** (el orden importa): $\dfrac{n!}{(n-k)!}$. Ej.: contraseñas.
- **Combinaciones** (el orden no importa): $\binom{n}{k}=\dfrac{n!}{k!\,(n-k)!}$. Ej.: elegir restaurantes en un mapa.

La pregunta puede venir directa ("¿de cuántas formas se sientan 5 personas?") o disfrazada de probabilidad ("¿prob. de sacar 4 cartas del mismo palo?"). Decide siempre si el orden importa.

## Variables aleatorias y distribuciones

Una v.a. tiene una distribución asociada: **PMF** (discreta) o **PDF** (continua); ambas no negativas y suman/integran a 1. La **CDF** $F_X(x)=P(X\le x)$ es no negativa y monótona creciente.

| Distribución | Modela | Media | Varianza |
|---|---|---|---|
| **Binomial**(n,p) | nº de éxitos en n ensayos binarios | $np$ | $np(1-p)$ |
| **Poisson**(λ) | nº de eventos en un intervalo fijo, tasa λ | $\lambda$ | $\lambda$ |
| **Uniforme**(a,b) | valor equiprobable en [a,b] | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$ |
| **Exponencial**(λ) | tiempo entre eventos de un Poisson | $1/\lambda$ | $1/\lambda^2$ |
| **Normal**(μ,σ²) | campana; CLT | $\mu$ | $\sigma^2$ |

Claves de aplicación: binomial = coin flips / signups; Poisson = visitas a un sitio por hora; exponencial = tiempos de espera (y es **sin memoria**); normal = casi todo por el Teorema Central del Límite.

## Distribuciones conjuntas, marginales y condicionales

Con dos v.a. surge la **conjunta** $f_{X,Y}$. La **marginal** se obtiene integrando la otra: $f_X(x)=\int f_{X,Y}(x,y)\,dy$. Las condicionales extienden Bayes al caso multivariado. Regla: cuando hay más de una v.a., piensa en términos de la conjunta.

## Cadenas de Markov

Proceso con estados finitos donde la probabilidad del próximo estado depende **solo del actual** (propiedad de Markov: pasado y futuro condicionalmente independientes dado el presente). Las transiciones viven en una **matriz $P$**.

- Estado **recurrente**: si entras, volverás con certeza. **Transiente**: hay prob. positiva de no volver nunca.
- La **distribución estacionaria** $\pi$ cumple $\pi = \pi P$ → proporción de tiempo a largo plazo en cada estado.

Pista: modela usuarios (nuevo / activo / churned) como cadena y pregunta el comportamiento a largo plazo.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "...dado que ocurrió..." | Bayes: prior × likelihood / evidencia |
| "Test muy preciso de algo raro" | Tasa base: la mayoría de positivos son falsos |
| "La prob. depende de un árbol de escenarios" | Ley de probabilidad total |
| "¿De cuántas formas...?" / "¿prob. de tal mano?" | Conteo: ¿el orden importa? perm vs comb |
| "Tiempo hasta el próximo evento" | Exponencial (sin memoria), Poisson de fondo |
| "Eventos por intervalo a tasa constante" | Poisson(λ): media = varianza = λ |
| "Estados con transiciones / largo plazo" | Cadena de Markov → estacionaria π=πP |

---

> **Síntesis:** El núcleo probabilístico de la entrevista de DS es Bayes (con la trampa de la tasa base), la ley de probabilidad total para descomponer escenarios, el conteo (orden sí/no), un puñado de distribuciones y sus medias/varianzas, y las cadenas de Markov para comportamiento a largo plazo. No se evalúa memoria de fórmulas exóticas, sino aplicarlas a una situación concreta.

---

*Retrieval: cierra y responde: (1) enuncia Bayes nombrando prior, likelihood y posterior; (2) ¿por qué un test "98% preciso" de una enfermedad rara da mayoría de falsos positivos?; (3) media y varianza de Poisson y de exponencial; (4) ¿qué cumple la distribución estacionaria de una cadena de Markov?*
