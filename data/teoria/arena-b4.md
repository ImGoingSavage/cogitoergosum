# Cadenas de Markov e inferencia bayesiana

## De qué trata (y qué sabrás hacer)

Dos ideas grandes, conectadas por un mismo motor (actualizar un vector de probabilidades). Las **cadenas de Markov** modelan sistemas cuya evolución depende solo del estado actual —el pasado se olvida—, y su pregunta central es el equilibrio de largo plazo. La **inferencia bayesiana** actualiza creencias sobre un parámetro desconocido a la luz de datos. Ambas se reducen a multiplicar y normalizar distribuciones.

Al terminar sabrás encontrar la distribución estacionaria de una cadena, decir cuándo converge, y actualizar un prior a un posterior usando conjugación (sumar pseudo-conteos). Cada idea parte de un caso pequeño manipulable a mano.

---

## Cadenas de Markov — la propiedad de "sin memoria"

La **propiedad de Markov** dice que el futuro depende del pasado solo a través del presente:

$$P(X_{n+1}=j\mid X_0,\ldots,X_n=i)=P(X_{n+1}=j\mid X_n=i).$$

Una cadena queda definida por su espacio de estados, una distribución inicial, y la **matriz de transición** $P$ con $P_{ij}=P(X_{n+1}=j\mid X_n=i)$. Cada fila suma 1 (de un estado *sales* a algún sitio). Para saber dónde estás tras $n$ pasos, elevas la matriz: $P(X_n=j\mid X_0=i)=(P^n)_{ij}$, y la distribución completa es $\pi_0 P^n$.

---

## Distribución estacionaria

Una distribución $\pi$ es **estacionaria** si al aplicar un paso no cambia: $\pi P=\pi$ (con $\sum_i\pi_i=1$). Es el equilibrio de largo plazo. Para hallarla, resuelve ese sistema lineal. Un atajo cuando aplica es el **balance detallado**:

$$\pi_i P_{ij}=\pi_j P_{ji}\quad\text{para todo }i,j,$$

que dice "el flujo de $i$ a $j$ iguala el de $j$ a $i$". El balance detallado implica estacionariedad (pero no al revés: hay cadenas con flujo circular estacionario que no lo cumplen).

---

## Convergencia: cuándo se olvida el inicio

**Teorema:** si la cadena es **irreducible** (de cualquier estado llegas a cualquier otro) y **aperiódica** (no queda atrapada en ciclos rígidos), entonces $P^n_{ij}\to\pi_j$ desde **cualquier** estado inicial. El sistema olvida de dónde partió. Dos hechos útiles:
- **Tiempo medio de retorno** a un estado $i$: $E[T_i]=1/\pi_i$ (si pasas $1/3$ del tiempo en $i$, vuelves cada 3 pasos en promedio).
- Una cadena periódica (alterna $1\to2\to1\to2$) tiene $\pi$ pero $P^n$ **oscila** sin converger — por eso hace falta aperiodicidad.

---

## Inferencia bayesiana — el motor

Bayes actualiza una creencia sobre un parámetro $\theta$ a la luz de datos:

$$P(\theta\mid\text{datos})\;\propto\; \underbrace{P(\text{datos}\mid\theta)}_{\text{verosimilitud}}\;\cdot\;\underbrace{P(\theta)}_{\text{prior}}.$$

El **prior** es lo que creías antes; la **verosimilitud** dice cómo de compatibles son los datos con cada $\theta$; el **posterior** es la creencia actualizada. La constante que falta (la evidencia $P(\text{datos})$) solo normaliza.

---

## Priors conjugados: cerrar la familia

Un prior es **conjugado** si el posterior tiene la misma forma que el prior — así actualizar es solo cambiar parámetros, sin integrales.

| Verosimilitud | Prior conjugado | Posterior |
|--------------|----------------|----------|
| $\text{Bin}(n,p)$ | $\text{Beta}(\alpha,\beta)$ | $\text{Beta}(\alpha+x,\;\beta+n-x)$ |
| $\text{Poisson}(\lambda)$ | $\text{Gamma}(\alpha,\beta)$ | $\text{Gamma}(\alpha+\sum x_i,\;\beta+n)$ |
| $N(\mu,\sigma^2)$, $\mu$ desconocida | $N(\mu_0,\tau^2)$ | $N(\mu_n,\tau_n^2)$ |

El caso estrella es **Beta–Binomial**: con prior $\text{Beta}(\alpha,\beta)$ y $x$ éxitos en $n$, el posterior es $\text{Beta}(\alpha+x,\beta+n-x)$. Interpreta $\alpha,\beta$ como **éxitos y fracasos previos** (pseudo-conteos): actualizar es literalmente sumar los datos a esos conteos.

$$E[p\mid x]=\frac{\alpha+x}{\alpha+\beta+n}.$$

Con prior uniforme ($\alpha=\beta=1$) esto es $\tfrac{x+1}{n+2}$ (la regla de sucesión de Laplace). Con muchos datos, $E[p\mid x]\to x/n$: el prior se diluye y manda la evidencia (conecta con [[arena-b3]]).

---

## Estimadores bayesianos según la pérdida

Del posterior sacas un único número según qué error quieras minimizar:

| Pérdida | Estimador óptimo |
|---------|-------------------|
| Cuadrática $(\theta-\delta)^2$ | media posterior $E[\theta\mid\text{datos}]$ |
| Absoluta $\lvert\theta-\delta\rvert$ | mediana posterior |
| 0–1 | moda posterior (MAP) |

El **MAP** (máximo a posteriori) maximiza $P(\theta\mid\text{datos})$; con prior uniforme coincide con el MLE (conecta con [[arena-cb2]]).

---

## Mini-ejemplo trabajado: distribución estacionaria de una cadena 2×2

Dos estados (soleado$=1$, lluvioso$=2$) con $P=\begin{pmatrix}0.6&0.4\\0.2&0.8\end{pmatrix}$. La estacionaria $\pi=(\pi_1,\pi_2)$ cumple $\pi P=\pi$. La forma más rápida es el **balance detallado** (vale para 2 estados): $\pi_1 P_{12}=\pi_2 P_{21}$, o sea $\pi_1\cdot0.4=\pi_2\cdot0.2$, de donde $\pi_1=\tfrac12\pi_2$. Con $\pi_1+\pi_2=1$:

$$\pi_2=\tfrac23,\quad \pi_1=\tfrac13 \;\Rightarrow\; \pi=(\tfrac13,\tfrac23).$$

A largo plazo el sistema pasa $\tfrac13$ del tiempo soleado y $\tfrac23$ lluvioso, **sin importar el clima inicial** (la cadena es irreducible y aperiódica). El tiempo medio de retorno a "soleado" es $1/\pi_1=3$ días.

**Predicción antes de seguir:** si arrancas 100% seguro de que hoy está soleado, ¿la distribución a 50 pasos depende de ese arranque? Respuesta: **prácticamente no** — converge a $(\tfrac13,\tfrac23)$. El estado inicial se "olvida" tras el mixing time; esa amnesia es la propiedad de Markov llevada al límite. (Excepción: si la cadena fuera periódica o reducible, el olvido no ocurriría.)

## Prototipo, contraejemplo y caso borde

- **Prototipo:** sistema cuyo futuro depende solo del estado actual → cadena de Markov; busca $\pi$ con $\pi P=\pi$ (o balance detallado).
- **Contraejemplo (no toda $\pi$ viene de balance detallado):** balance detallado $\Rightarrow$ estacionariedad, pero no al revés; una cadena con flujo circular ($1\to2\to3\to1$) puede tener $\pi$ estacionaria sin ser reversible. Asumir reversibilidad siempre es el error.
- **Caso borde (periódica):** una cadena que alterna $1\to2\to1\to2$ tiene $\pi=(\tfrac12,\tfrac12)$ pero $P^n$ **no converge** (oscila); el teorema de convergencia exige aperiodicidad.

## Errores típicos

- **Conceptual:** confundir la distribución estacionaria (equilibrio de largo plazo) con la inicial, o creer que toda cadena converge (hace falta irreducible + aperiódica).
- **Técnico:** en la actualización bayesiana, olvidar sumar los datos a *ambos* parámetros (éxitos a $\alpha$, fracasos a $\beta$).
- **De supuestos:** reportar el posterior como si el prior no importara con pocos datos; el prior domina hasta que $n$ crece.

## Transferencia isomorfa

- **Beta–Binomial conjugado ↔ familia de distribuciones:** el posterior $\text{Beta}(\alpha+x,\beta+n-x)$ es la misma Beta$=$Gamma-normalizada de antes; conjugar es cerrar la familia bajo actualización (conecta con [[arena-b3]]).
- **Posterior $\propto$ verosimilitud $\times$ prior ↔ Bayes con tasa base:** actualizar la creencia sobre $\theta$ es el mismo gesto que actualizar las odds de enfermedad con un test (conecta con [[arena-q2]]).
- **Propiedad de Markov (estado suficiente) ↔ estado mínimo en sistemas/RL:** "el futuro depende solo del presente" es la definición de un estado bien diseñado en control y en features (conecta con [[arena-q11]], el OU es markoviano).
- **MAP con prior uniforme $=$ MLE ↔ regularización:** un prior gaussiano sobre los pesos es exactamente la regularización L2 del MAP (conecta con [[arena-isl3]]).

Moraleja de la arista: *una cadena de Markov olvida su inicio si es irreducible y aperiódica; el equilibrio es $\pi$ con $\pi P=\pi$; y la inferencia bayesiana es "actualizar $\pi$" con verosimilitud $\times$ prior.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿Cuándo converge la cadena?" | Irreducible + aperiódica |
| "$E[\text{tiempo de retorno al estado }i]$" | $1/\pi_i$ |
| "Prior para proporción + datos binomiales" | Beta conjugado |
| "Actualizar media con datos normales" | Normal–Normal conjugado |
| "Posterior con muchos datos" | Domina la evidencia → $\approx$ MLE |
| "Estimador bajo pérdida cuadrática" | Media posterior |
| "MAP con prior uniforme" | $=$ MLE |

---

> **Síntesis:** Las cadenas de Markov modelan sistemas con memoria de primer orden — el pasado solo importa por el estado actual. La distribución estacionaria es el equilibrio de largo plazo, al que se converge si la cadena es irreducible y aperiódica. La inferencia bayesiana es actualización de creencias vía Bayes; los priors conjugados convierten esa actualización en sumar pseudo-conteos.

---

*Retrieval: cierra y responde: (1) distribución estacionaria para $P=\big(\begin{smallmatrix}0.6&0.4\\0.2&0.8\end{smallmatrix}\big)$; (2) posterior de $p$ tras $\text{Beta}(3,3)$ y 4 éxitos en 10; (3) $E[p\mid\text{datos}]$ de lo anterior; (4) por qué una cadena periódica no converge aunque tenga $\pi$.*
