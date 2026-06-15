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

## Mini-ejemplo trabajado: el test "98% preciso" de algo raro

Enfermedad con prevalencia 1%. Test con sensibilidad 98% y especificidad 98%. Das positivo: ¿probabilidad de estar enfermo? Tabla con N=10 000:

- Enfermos: 100 → 98 verdaderos positivos.
- Sanos: 9900 → 2% falsos positivos = 198.
- P(enfermo | +) = 98/(98+198) = 98/296 ≈ **33%**.

Un test "98% preciso" deja **dos de cada tres positivos como falsos**, porque hay 99× más sanos que enfermos: el 2% de una base enorme aplasta al 98% de una base diminuta.

**Predicción antes de seguir:** ¿qué sube más el valor predictivo, mejorar la sensibilidad de 98% a 99% o aplicar el test solo a un grupo de riesgo con prevalencia 10%? Respuesta: **la prevalencia** — con prev 10% el VPP salta a ~84% sin tocar el test. La palanca más fuerte casi nunca es el test; es a quién se lo aplicas. Por eso "dado que" siempre exige preguntar la tasa base.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "dado que ocurrió B" → Bayes; descompón el denominador con la ley de probabilidad total.
- **Contraejemplo (independencia falsa):** dos eventos pueden parecer ligados pero ser independientes si P(A|B)=P(A); confundir "ocurren juntos a veces" con dependencia es un error.
- **Caso borde (exponencial sin memoria):** el tiempo de espera ya transcurrido no cambia la distribución del restante: P(X>s+t | X>s)=P(X>t). El borde define la exponencial y la separa de distribuciones con envejecimiento (Weibull).

## Errores típicos

- **Conceptual:** invertir el condicional (leer sensibilidad P(+|E) como VPP P(E|+)).
- **Técnico:** en conteo, no decidir si el orden importa (permutación vs combinación).
- **De interpretación:** modelar tiempos de espera con normal en vez de exponencial/Poisson.

## Transferencia isomorfa

- **Bayes con tasa base ↔ VPP de un clasificador:** la enfermedad rara es el mismo cálculo que la precisión de un modelo de fraude en producción (conecta con [[arena-q2]]).
- **Exponencial sin memoria ↔ proceso de Poisson y Gamma:** los tiempos entre eventos son exponenciales y su suma es Gamma; modela colas y llegadas (conecta con [[arena-b3]]).
- **Cadena de Markov estacionaria ↔ comportamiento a largo plazo:** usuarios nuevo/activo/churned convergen a π=πP, el equilibrio que olvida el estado inicial (conecta con [[arena-b4]]).
- **Conteo (orden sí/no) ↔ linealidad de la esperanza:** muchos problemas de "¿cuántas formas / qué probabilidad" se resuelven con indicadores sin pelear con la dependencia (conecta con [[arena-b1]]).

Moraleja de la arista: *"dado que" pide Bayes, y Bayes siempre discute con la tasa base; cuando la base es rara, la base gana.*

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
