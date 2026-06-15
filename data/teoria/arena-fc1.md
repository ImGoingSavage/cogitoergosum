# Coincidencias, urnas y emparejamiento

## De qué trata (y qué sabrás hacer)

Este bloque reúne problemas que parecen distintos —calcetines en la oscuridad, sombreros revueltos, contratar al mejor candidato— pero comparten un esqueleto: contar coincidencias y emparejamientos cuando el azar mezcla las cosas. Dos números mágicos reaparecen: el **$1/e\approx 37\%$** (la firma de "esperaba uno y no salió ninguno") y el principio del **palomar** (si hay más objetos que cajas, alguna caja se repite).

Al terminar reconocerás cuándo un problema es "de coincidencias" y tendrás la herramienta lista: indicadores para las medias, complemento para las garantías, y los modelos clásicos (hipergeométrica, binomial negativa, secretario) para lo demás. Cada uno se construye desde un caso concreto.

---

## El principio del palomar aplicado a pares

Si repartes objetos en categorías y hay más objetos que categorías, dos caen en la misma. Para **garantizar** una coincidencia con $k$ colores, el peor caso es sacar uno de cada color y luego uno más: necesitas $k+1$.

Ejemplo — calcetines en la oscuridad (4 rojos + 6 azules):
- Garantizar **algún** par: 2 colores, así que $2+1=3$ calcetines.
- Garantizar un par **rojo**: el adversario te da los 6 azules primero, luego 2 rojos $\Rightarrow 8$.

Regla: para garantizar $r$ piezas de un color **específico**, saca todos los demás y luego $r$. El palomar no calcula probabilidades; da **garantías** (el peor caso).

---

## Puntos fijos de una permutación aleatoria

Barajas $n$ cartas numeradas; un "punto fijo" es una carta en su posición original. ¿Cuántos esperas? Define $X_i=1$ si la carta $i$ cae en su lugar. Por simetría $P(X_i=1)=1/n$, y por **linealidad de la esperanza** (que no exige independencia):

$$E[\text{puntos fijos}] = \sum_{i=1}^n E[X_i] = n\cdot\frac1n = 1 \quad\text{para todo } n.$$

¿Y la probabilidad de **cero** puntos fijos (un desarreglo)? Por inclusión-exclusión,

$$P(\text{ninguno}) = \frac{D(n)}{n!}=\sum_{k=0}^n\frac{(-1)^k}{k!}\xrightarrow{n\to\infty} \frac1e\approx 36.79\%.$$

| $n$ | 2 | 3 | 4 | 5 | $\infty$ |
|---|---|---|---|---|---|
| $D(n)/n!$ | 0.500 | 0.333 | 0.375 | 0.367 | $1/e$ |

Más aún, el número de coincidencias es aproximadamente $\text{Poisson}(1)$: $P(\text{exactamente }k)\approx \tfrac{e^{-1}}{k!}$.

---

## El problema de la boleta (ballot problem)

En un escrutinio, el candidato A obtiene $a$ votos y B obtiene $b$, con $a>b$. Si se cuentan en orden aleatorio, ¿probabilidad de que A vaya **siempre estrictamente adelante** durante todo el conteo?

$$P(\text{A siempre adelante}) = \frac{a-b}{a+b}.$$

Se prueba por **reflexión**: las trayectorias "malas" (donde A no siempre lidera) están en biyección con las que empiezan por un voto de B, y esas se cuentan fácil. Para $a=7,b=3$: $\tfrac{4}{10}=\tfrac25$. La reflexión —emparejar trayectorias buenas y malas— es la misma idea que en caminos de retícula con barrera.

---

## Valores récord

Lees una secuencia de $n$ valores i.i.d. de una distribución continua. Un "récord" es un valor mayor que todos los anteriores. ¿Probabilidad de que el $k$-ésimo sea récord? Entre los primeros $k$ valores, cualquiera es el máximo con igual probabilidad por simetría, así que

$$P(k\text{-ésimo es récord})=\frac1k, \qquad E[\text{récords en }n]=H_n=1+\tfrac12+\cdots+\tfrac1n.$$

Para $n=10$, $H_{10}\approx2.93$; para $n=100$, $\approx 5.19$ (crece como $\ln n$, lentísimo). Curiosamente los eventos "récord" son **independientes** aunque los valores no lo sean.

---

## Distribución hipergeométrica

Es la binomial **sin reemplazo**. De $N$ objetos ($K$ del tipo A, $N-K$ del tipo B) sacas una muestra de $n$ sin reponer. La probabilidad de obtener $k$ del tipo A:

$$P(X=k)=\frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}, \qquad E[X]=\frac{nK}{N}.$$

La media es igual que la binomial, pero la varianza lleva un **factor de corrección por población finita**:

$$\text{Var}[X]=n\cdot\frac{K}{N}\cdot\left(1-\frac{K}{N}\right)\cdot\frac{N-n}{N-1}.$$

Cuando $N\to\infty$ (sacar de un mar) el factor $\tfrac{N-n}{N-1}\to1$ y la hipergeométrica se vuelve binomial.

---

## Distribución binomial negativa

Cuenta el número de ensayos hasta el **$r$-ésimo éxito** (con probabilidad de éxito $p$). Generaliza la geométrica (que es el caso $r=1$):

$$P(X=n)=\binom{n-1}{r-1}p^r(1-p)^{n-r}, \qquad E[X]=\frac{r}{p}, \quad \text{Var}[X]=\frac{r(1-p)}{p^2}.$$

Para $r=3$, $p=0.3$: esperas $E[X]=10$ ensayos. Intuición de $E[X]=r/p$: cada éxito cuesta en promedio $1/p$ ensayos, y necesitas $r$.

---

## La urna de Pólya (refuerzo positivo)

Empiezas con 1 bola roja y 1 azul. Cada paso: sacas una al azar, la devuelves **y añades otra del mismo color**. El éxito atrae éxito ("el rico se hace más rico"). Y sin embargo, tras $n$ adiciones, el número de rojas es **uniforme**:

$$P(k\text{ rojas en }n\text{ pasos})=\frac{1}{n+1}\quad\text{para }k=0,1,\ldots,n.$$

$E[\text{fracción de rojas}]=1/2$ y su varianza $\to 1/12$. Lo contraintuitivo: el refuerzo positivo no concentra la distribución, la **aplana**. El borde rompe la intuición de que "el rico se hace más rico" produce un ganador claro.

---

## El problema del secretario (parada óptima)

$n$ candidatos en orden aleatorio; entrevistas uno a uno y debes contratar o rechazar **en el acto**, sin volver atrás; quieres al mejor. La estrategia óptima tiene dos fases: **explora** rechazando los primeros $\lfloor n/e\rfloor$ (y memoriza al mejor visto), luego **explota** contratando al primero que supere ese listón.

$$P(\text{contratar al mejor})\to \frac1e\approx 36.8\%.$$

Para $n=100$: rechaza los primeros 37, luego actúa. El punto $n/e$ equilibra "explorar de más y dejar pasar al mejor" contra "explotar de más sin información".

---

## El problema de ocupación

Lanzas $n$ bolas en $n$ cajas al azar. ¿Cuántas cajas quedan vacías? Una caja queda vacía si las $n$ bolas la evitan: $P(\text{vacía})=(1-1/n)^n\to e^{-1}$. Por linealidad,

$$E[\text{cajas vacías}]=n\left(1-\tfrac1n\right)^n\to \frac{n}{e}\approx 0.368\,n.$$

~37% de las cajas quedan vacías. Esto modela el **hashing**: tras $n$ inserciones en una tabla de $n$ slots, ~37% de los slots están vacíos y hay colisiones (conecta con [[arena-sd2]]).

---

## Mini-ejemplo trabajado: el secretario y el $1/e$ que reaparece

100 candidatos en orden aleatorio; decides en el acto contratar o rechazar; quieres al mejor. La estrategia óptima: **rechaza los primeros $\lfloor n/e\rfloor\approx 37$**, memoriza el mejor visto, y contrata al primero que lo supere. La probabilidad de quedarte con el verdadero mejor tiende a **$1/e\approx 37\%$** — sorprendentemente alta para "una sola oportunidad".

La estructura: una fase de **exploración** (mira sin comprometerte para calibrar) y una de **explotación** (actúa con el umbral aprendido). El punto $n/e$ equilibra "explorar de más y dejar pasar al mejor" contra "explotar de más sin información".

**Predicción antes de seguir:** ¿reconoces ese 37%? Es el mismo $1/e$ de "$P(\text{nadie recupera su sombrero})$" y de "fracción esperada de cajas vacías" ($n/e$). Aparece siempre que cuentas eventos raros con tasa $\approx1$: $P(0\text{ éxitos})$ en una $\text{Poisson}(1)$ es $e^{-1}$. El $1/e$ es la firma de "esperaba uno, no salió ninguno".

## Prototipo, contraejemplo y caso borde

- **Prototipo (palomar):** "garantizar un par de $k$ colores" → $k+1$ objetos; para $r$ de un color específico, todos los otros $+\,r$.
- **Contraejemplo (puntos fijos no se acumulan):** $E[\text{puntos fijos}]=1$ para todo $n$, pero NO porque sean independientes (no lo son); la linealidad no lo exige. Creer que "más personas = más coincidencias esperadas" es el error.
- **Caso borde (urna de Pólya):** refuerzo positivo "el rico se hace más rico", y aun así la fracción final de rojas es **uniforme** en $\{0,\ldots,n\}$. El borde rompe la intuición de que el refuerzo concentra.

## Errores típicos

- **Conceptual:** exigir independencia para sumar esperanzas de indicadores (puntos fijos, coincidencias).
- **Técnico:** olvidar el factor de corrección finita $\tfrac{N-n}{N-1}$ en la varianza hipergeométrica.
- **De interpretación:** confundir "número de intentos hasta el $r$-ésimo éxito" (binomial negativa, $E=r/p$) con el número de éxitos en $n$ intentos (binomial).

## Transferencia isomorfa

- **Problema de ocupación ($n/e$ cajas vacías) ↔ colisiones de hash:** tras $n$ inserciones en $n$ slots, ~37% quedan vacíos y hay colisiones; es el mismo conteo que el cumpleaños (conecta con [[arena-sd2]] y [[arena-fc3]]).
- **Secretario ($1/e$) ↔ parada óptima:** explorar y luego fijar umbral es backward induction sobre "quedarse vs seguir" (conecta con [[arena-q8]]).
- **$E[\text{récords}]=H_n$ ↔ coleccionista de cupones:** el número armónico cuenta récords y también el tiempo de coleccionar $n$ tipos (conecta con [[arena-q6]]).
- **Puntos fijos por indicadores ↔ linealidad de la esperanza:** el sombrero es el ejemplo canónico de descomponer en indicadores sin pelear con la dependencia (conecta con [[arena-q1]] y [[arena-b1]]).

Moraleja de la arista: *el $1/e$ es la firma de "esperaba uno y salió ninguno"; aparece en sombreros, cajas vacías y en el secretario por la misma $\text{Poisson}(1)$.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Garantizar par de $k$ colores" | Palomar: $k+1$ objetos |
| "$E[\text{puntos fijos de permutación}]$" | Siempre 1, por linealidad |
| "$P(\text{ningún punto fijo})$" | $D(n)/n!\to 1/e$ |
| "A siempre adelante en conteo" | Ballot: $\tfrac{a-b}{a+b}$ |
| "$P(k\text{-ésimo es récord})$" | $1/k$ |
| "$E[\text{récords en }n]$" | $H_n$ |
| "Muestreo sin reemplazo" | Hipergeométrica: $E=nK/N$ |
| "$k$-ésimo éxito, $p$ fija" | Binomial negativa: $E=r/p$ |
| "Contratar al mejor, 1 oportunidad" | Secretario: rechaza $n/e$, luego el mejor |

---

> **Síntesis:** Los problemas de coincidencia y emparejamiento tienen dos resultados contraintuitivos clave: $E[\text{puntos fijos}]=1$ siempre (linealidad); $P(\text{ningún punto fijo})\approx 1/e\approx 37\%$ (convergencia rápida). El principio del palomar resuelve los problemas de garantía. El problema del secretario muestra que $1/e$ también aparece en parada óptima.

---

*Retrieval: cierra y responde: (1) $E[\text{puntos fijos de permutación de }n=50]$; (2) $P(\text{ningún punto fijo}, n=6)$; (3) fórmula del ballot problem; (4) $P(k\text{-ésimo es récord en }n$ i.i.d.$)$.*
