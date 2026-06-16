# Clasificación de dificultad · Fase 7 Arena

Clasificación **manual, ejercicio a ejercicio** del banco completo de la Fase 7 Arena
según los criterios de `reformulacion-examenes.md` §2 (easy / medium / hard).
Hecha por el arquitecto; la ejecución en código/vistas la realiza el ejecutor
(ver `PROMPT-EJECUTOR-DIFICULTAD-ARENA.md`).

- **Fuente de las preguntas:** `data/study.json` → `unidades[]` con `bloque: "fase-7"`, campo `banco[]`.
- **Mapa de resultados machine-readable:** `data/arena-dificultades.json` (llave = id de pregunta).
- **Clusters:** definidos en `data/entrevista/_taxonomia.json`.

## Criterios aplicados

| Nivel | Criterio |
|---|---|
| `easy` | Reconocimiento, definición, intuición básica o aplicación directa de UNA idea; caso pequeño sin combinar ideas. |
| `medium` | Combinar 2+ ideas, razonamiento intermedio, evitar un error común. |
| `hard` | Transferencia, varios pasos, caso borde, trampa conceptual, razonamiento bajo presión o mezcla de dominios. |

## Resumen global (1619 preguntas)

| Dificultad | Preguntas | % |
|---|---|---|
| easy | 243 | 15% |
| medium | 1138 | 70% |
| hard | 238 | 15% |

## Desglose por cluster

| Cluster | Preguntas | easy | medium | hard |
|---|---|---|---|---|
| Probabilidad, esperanza y conteo (Quant) | 311 | 37 | 177 | 97 |
| Estadística aplicada e inferencia | 208 | 35 | 148 | 25 |
| Estructuras de datos y algoritmos (MAANG) | 68 | 14 | 45 | 9 |
| Diseño de sistemas (MAANG) | 60 | 12 | 43 | 5 |
| Ciencia de datos aplicada | 124 | 47 | 72 | 5 |
| ML Systems y feature pipelines | 480 | 51 | 404 | 25 |
| Causalidad y Health AI / RWE | 308 | 38 | 215 | 55 |
| Conductual y comunicación bajo presión | 60 | 9 | 34 | 17 |

## Detalle por unidad y pregunta

### Probabilidad, esperanza y conteo (Quant) (`quant-prob`)

**`arena-b1` — Fundamentos de probabilidad y conteo**  · easy 7 / medium 7 / hard 1

- `arb1-q1` → **easy** · ¿De cuántas formas se pueden ordenar las letras de STATISTICS?
- `arb1-q2` → **easy** · Explica la diferencia entre sampling with replacement y without replacement en combinatoria.
- `arb1-q3` → **medium** · En un grupo de 10 personas, ¿cuántos comités de 3 se pueden formar donde uno es presidente y los otros dos son…
- `arb1-q4` → **easy** · Lanzas dos dados justos. ¿Cuál es $P(\text{suma}=7)$?
- `arb1-q5` → **medium** · Si $X \sim \text{Geom}(p)$ (número de intentos hasta el primer éxito), calcula $E[X]$ usando LOTUS.
- `arb1-q6` → **medium** · $X \sim \text{Uniform}\{1,2,\dots,n\}$. Calcula $E[X]$ y $\text{Var}[X]$.
- `arb1-q7` → **hard** · En el problema del sombrero ($n$ personas), ¿cuál es la varianza del número de personas que recuperan su propi…
- `arb1-q8` → **easy** · Se elige un número entero al azar entre 1 y 100. ¿Cuál es $P(\text{divisible por 2 o por 5})$?
- `arb1-q9` → **medium** · ¿Cuántos enteros del 1 al 1000 son divisibles por 3, 5 o 7?
- `arb1-q10` → **easy** · Enuncia la Ley de la Probabilidad Total y da un ejemplo.
- `arb1-q11` → **easy** · $X \sim \text{Bin}(n,p)$. Demuestra $E[X]=np$ usando linealidad.
- `arb1-q12` → **medium** · $X \sim \text{Bin}(n,p)$. Calcula $\text{Var}[X]$.
- `arb1-q13` → **easy** · Una urna tiene 3 rojas y 7 azules. Se sacan 2 sin reemplazo. ¿$P(\text{ambas rojas})$?
- `arb1-q14` → **medium** · ¿Cuántos anagramas tiene ABRACADABRA?
- `arb1-q15` → **medium** · Si $X \sim \text{Poisson}(\lambda)$, calcula $E[X(X-1)]$ usando LOTUS.

**`arena-p1` — Acertijos matemáticos y razonamiento rápido**  · easy 4 / medium 10 / hard 1

- `arp1-q1` → **medium** · Calcula la suma $S = 1/(1\times2) + 1/(2\times3) + 1/(3\times4) + \dots + 1/(99\times100)$. Busca un patrón an…
- `arp1-q2` → **medium** · Tienes 8 bolas idénticas a la vista; una pesa levemente diferente (puedes asumir más pesada). Con una balanza …
- `arp1-q3` → **easy** · Calcula $S = 1 - 2 + 3 - 4 + 5 - 6 + \dots + 99 - 100$. ¿Hay un atajo sin sumar término a término?
- `arp1-q4` → **easy** · Calcula mentalmente $97 \times 103$ sin hacer multiplicación larga. ¿Cuál es la estrategia? ¿Y $98^2$?
- `arp1-q5` → **medium** · ¿Cuántas veces aparece el dígito 1 al escribir todos los enteros del 1 al 100?
- `arp1-q6` → **medium** · ¿Cuánto es $4444^{4444} \bmod 9$? Resuelve sin calculadora.
- `arp1-q7` → **hard** · $n$ puntos en una circunferencia; cada par está unido por una cuerda. ¿Cuántas cuerdas hay? ¿Cuántas intersecc…
- `arp1-q8` → **medium** · Calcula el producto $P = (1-1/4)(1-1/9)(1-1/16)\cdots(1-1/n^2)$. ¿Cuál es el valor para $n\to\infty$?
- `arp1-q9` → **medium** · Suma todos los dígitos de todos los enteros del 1 al 100 (por ejemplo, 99 contribuye 9+9=18). ¿Cuánto es la su…
- `arp1-q10` → **easy** · Simplifica $(\sqrt6 + \sqrt5) / (\sqrt6 - \sqrt5)$. ¿Cuál es la forma más simple sin raíz en el denominador?
- `arp1-q11` → **medium** · Para $|x| < 1$, ¿cuánto es $\sum_{k=0}^{\infty} x^k$? ¿Y $\sum_{k=1}^{\infty} k x^{k-1}$? Aplica esto a calcul…
- `arp1-q12` → **medium** · ¿Cuántos cuadrados (de todos los tamaños) hay en un tablero de ajedrez de $8\times8$?
- `arp1-q13` → **easy** · ¿Cuál es el menor $n$ tal que $n! > 10^6$? Estima primero, luego verifica.
- `arp1-q14` → **medium** · Tres hormigas se ubican en los vértices de un triángulo equilátero. Cada hormiga elige al azar (p=1/2) caminar…
- `arp1-q15` → **medium** · El problema del cumpleaños: ¿cuántas personas se necesitan para que P(al menos 2 compartan cumpleaños) > 50%? …

**`arena-q1` — Arena Quant · Linealidad de la esperanza**  · easy 1 / medium 3 / hard 0

- `arq1-q1` → **medium** · Enuncia el teorema de linealidad de la esperanza en tus palabras y da el paso clave de la demostración (sin me…
- `arq1-q2` → **medium** · Un mazo de 52 cartas se mezcla aleatoriamente. ¿Cuántos pares adyacentes (posiciones i e i+1) del mismo palo e…
- `arq1-q3` → **medium** · Se lanzan $n$ dados (6 caras, justos). Sea $X$ el número de valores distintos que aparecen. Calcula $E[X]$ par…
- `arq1-q4` → **easy** · En una entrevista te dicen: '$n$ personas arrojan sus llaves al centro; cada persona toma una al azar. ¿Cuánta…

**`arena-q2` — Arena Quant · Bayes, tasas base y señales ruidosas**  · easy 1 / medium 2 / hard 1

- `arq2-q1` → **medium** · Un test tiene sensibilidad 90% y especificidad 95%. La prevalencia es 10%. Usando una tabla de contingencia pa…
- `arq2-q2` → **medium** · Define Likelihood Ratio positivo (LR+) y explica cómo se usa con los odds del prior para obtener los odds del …
- `arq2-q3` → **hard** · Un modelo de fraude tiene VPP≈49% en producción (el ejemplo de la lección: sensibilidad 97%, especificidad 99.…
- `arq2-q4` → **easy** · En una entrevista para un hedge fund te dicen: 'tu señal de trading tiene un 70% de precisión en backtesting c…

**`arena-p2` — Combinatoria y probabilidad discreta**  · easy 0 / medium 11 / hard 5

- `arp2-q1` → **medium** · ¿De cuántas maneras puedes caminar de $(0,0)$ a $(m,n)$ en una retícula, moviéndote solo derecha o arriba? Cal…
- `arp2-q2` → **medium** · Inclusión-exclusión: en una baraja de 52 cartas, ¿cuál es la probabilidad de que una mano de 5 cartas contenga…
- `arp2-q3` → **medium** · Stars and bars: ¿cuántas soluciones enteras no negativas tiene $x_1 + x_2 + x_3 + x_4 = 10$? ¿Y si cada $x_i \…
- `arp2-q4` → **medium** · ¿Cuántas formas hay de ordenar las letras de MISSISSIPPI? ¿Cuántas permutaciones de 4 de sus letras distintas …
- `arp2-q5` → **medium** · Define desarreglo $D(n)$ como permutación de $\{1,\dots,n\}$ sin punto fijo. Da la fórmula y calcula $D(4)$. ¿…
- `arp2-q6` → **hard** · Sacas 3 cartas (con reemplazo) de un mazo de 10 cartas numeradas del 1 al 10. ¿Cuál es el valor esperado del m…
- `arp2-q7` → **hard** · Ruina del jugador con barrera: empiezas con \$3, quieres llegar a \$10, ganas \$1 con $p=1/2$ y pierdes \$1 co…
- `arp2-q8` → **hard** · Duración esperada del juego de la ruina: empiezas con \$$k$, barreras en 0 y $N$, moneda justa ($p=1/2$). ¿Cuá…
- `arp2-q9` → **medium** · Enuncia la aproximación de Poisson al binomial. ¿Bajo qué condiciones es válida? Estima $P(\text{0 defectos en…
- `arp2-q10` → **medium** · La distribución geométrica tiene la propiedad de falta de memoria. Enuncia esta propiedad formalmente. ¿Qué di…
- `arp2-q11` → **hard** · Sean $X_1,\dots,X_n$ i.i.d. con distribución Uniforme$[0,1]$. Calcula $E[X_{(1)}]$ (el mínimo) y $E[X_{(n)}]$ …
- `arp2-q12` → **medium** · Enuncia la desigualdad de Markov y la de Chebyshev. ¿Cuál es más fuerte? Aplica Chebyshev para acotar $P(|X-\m…
- `arp2-q13` → **hard** · Enuncia la desigualdad de Jensen para funciones convexas. Da dos aplicaciones: una en finanzas y una en probab…
- `arp2-q14` → **medium** · Una variable aleatoria $X$ tiene $P(X=-1)=1/3$, $P(X=0)=1/3$, $P(X=1)=1/3$. ¿Cuántas observaciones i.i.d. nece…
- `arp2-q15` → **medium** · Lanzas un dado de 6 caras repetidamente. ¿Cuántos lanzamientos esperas hasta obtener todas las caras al menos …
- `arp2-q16` → **medium** · Sean $X \sim \text{Exp}(\lambda)$ e $Y \sim \text{Exp}(\mu)$ independientes. ¿Cuál es $P(X < Y)$? ¿Cuál es la …

**`arena-fc1` — Coincidencias, urnas y emparejamiento**  · easy 1 / medium 9 / hard 5

- `arfc1-q1` → **easy** · Un cajón tiene 10 calcetines: 4 rojos y 6 azules, mezclados en oscuridad. ¿Cuántos debes sacar para garantizar…
- `arfc1-q2` → **medium** · El problema de los sombreros: $n$ personas dejan sus sombreros y se devuelven al azar. ¿Cuál es $E[\text{perso…
- `arfc1-q3` → **hard** · El problema de la boleta electoral (Ballot problem): candidato A recibe a votos y B recibe b votos, con a > b.…
- `arfc1-q4` → **medium** · Barajas adivinación sin retroalimentación: adivinas el palo de cada carta de una baraja de 52 antes de verla. …
- `arfc1-q5` → **hard** · Valores récord: se observan $n$ números i.i.d. de una distribución continua uno a uno. $X_k$ es un récord si e…
- `arfc1-q6` → **medium** · Muestreo sin reemplazo: una urna tiene 6 bolas rojas y 4 azules. Sacas 3 sin reemplazo. ¿Cuál es la distribuci…
- `arfc1-q7` → **hard** · Problema del cumpleaños con tripletes: ¿aproximadamente cuántas personas necesitas para que P(al menos 3 compa…
- `arfc1-q8` → **medium** · Distribución binomial negativa: lanzas una moneda injusta ($p=0.3$) hasta obtener 3 caras. ¿Cuál es $P(\text{e…
- `arfc1-q9` → **medium** · ¿Cuántos pares de personas en un grupo de n comparten cumpleaños en expectativa? Para n=50, ¿cuál es el número…
- `arfc1-q10` → **medium** · Barajas coincidentes: tienes dos barajas de 52 cartas barajadas independientemente. Las volteas al mismo tiemp…
- `arfc1-q11` → **hard** · Problema del secretario (optimal stopping): n candidatos se entrevistan en orden aleatorio. Debes contratar o …
- `arfc1-q12` → **hard** · Urna de Polya: empiezas con 1 bola roja y 1 azul. En cada paso, sacas una bola y la regresas junto con una nue…
- `arfc1-q13` → **medium** · Problema de la ocupación: lanzas n bolas en n cajas uniformemente al azar. ¿Cuál es E[cajas vacías]? ¿Y P(al m…
- `arfc1-q14` → **medium** · Distribución hipergeométrica — prueba de calidad: un lote de 100 piezas contiene 5 defectuosas. Inspeccionas 2…
- `arfc1-q15` → **medium** · El problema del intercambio de parejas: en una fiesta, n parejas intercambian parejas al azar (men con women s…

**`arena-b2` — Variables aleatorias conjuntas y correlación**  · easy 4 / medium 11 / hard 0

- `arb2-q1` → **medium** · ¿Condición necesaria y suficiente para independencia de X e Y continuas?
- `arb2-q2` → **medium** · $X,Y \sim$ Normal bivariada estándar con correlación $\rho$. Calcula $E[Y\mid X=x]$.
- `arb2-q3` → **medium** · Si $\text{Cov}(X,Y) = 0$, ¿implica $X$ e $Y$ independientes?
- `arb2-q4` → **easy** · $X,Y$ independientes con $\text{Var}[X]=4$, $\text{Var}[Y]=9$. Calcula $\text{Var}[2X-3Y+1]$.
- `arb2-q5` → **medium** · $X,Y \sim \text{Exp}(1)$ i.i.d. independientes. Calcula $P(X < Y)$.
- `arb2-q6` → **easy** · $X_1,\dots,X_n$ i.i.d. con media $\mu$ y varianza $\sigma^2$. Calcula $\text{Var}[\bar X]$.
- `arb2-q7` → **medium** · Enuncia la Ley de la Varianza Total.
- `arb2-q8` → **medium** · $X \sim N(0,1)$. Calcula $E[X^2]$ y $E[X^4]$.
- `arb2-q9` → **easy** · Duración de proyecto sigue $\text{Exp}(0.1)$. Dado que ya llevamos 5 días, ¿$P(\text{terminar en 5 más})$?
- `arb2-q10` → **easy** · $X\sim\text{Poisson}(\lambda)$, $Y\sim\text{Poisson}(\mu)$ independientes. ¿Distribución de $X+Y$?
- `arb2-q11` → **medium** · ¿Por qué $\rho(X,Y) \in [-1,1]$?
- `arb2-q12` → **medium** · Lanzas un dado justo, luego lanzas $X$ monedas justas. Sea $Y$ el número de caras. Calcula $E[Y]$ y $\text{Var…
- `arb2-q13` → **medium** · $X \sim N(\mu,\sigma^2)$. Calcula $E[e^X]$.
- `arb2-q14` → **medium** · $X_1,X_2,X_3 \sim N(0,1)$ i.i.d. ¿Distribución de $X_1^2+X_2^2+X_3^2$?
- `arb2-q15` → **medium** · $X\sim N(0,1)$ e $Y=X^2$. ¿Distribución de $Y$?

**`arena-b3` — Distribuciones importantes y sus relaciones**  · easy 1 / medium 10 / hard 4

- `arb3-q1` → **easy** · ¿Cuál es la relación entre Gamma(α,λ) y Exp(λ)?
- `arb3-q2` → **medium** · $X \sim \text{Gamma}(3,2)$. Calcula $E[X]$ y $\text{Var}[X]$.
- `arb3-q3` → **hard** · ¿Distribución de $X/(X+Y)$ con $X\sim\text{Gamma}(\alpha)$, $Y\sim\text{Gamma}(\beta)$ independientes (misma e…
- `arb3-q4` → **medium** · $X \sim \text{Beta}(\alpha,\beta)$. Calcula $E[X]$ y $\text{Var}[X]$.
- `arb3-q5` → **medium** · $X \sim t(\nu)$. ¿Para qué $\nu$ existe $E[X]$? ¿Y $\text{Var}[X]$?
- `arb3-q6` → **medium** · ¿Cómo se construye $t(\nu)$ a partir de variables normales y chi-cuadrado?
- `arb3-q7` → **hard** · $X\sim\text{Poisson}(\lambda)$, $Y\mid X\sim\text{Bin}(X,p)$. ¿Distribución marginal de $Y$?
- `arb3-q8` → **medium** · $X\sim$Lognormal: $X=e^Y$, $Y\sim N(\mu,\sigma^2)$. Calcula $E[X]$ y $\text{Var}[X]$.
- `arb3-q9` → **medium** · $X_1,\dots,X_n\sim N(\mu,\sigma^2)$. ¿Distribución de $(n-1)S^2/\sigma^2$ donde $S^2$ es la varianza muestral?
- `arb3-q10` → **medium** · ¿Qué es una familia exponencial? Da un ejemplo.
- `arb3-q11` → **medium** · $X_1\sim\chi^2(m)$, $X_2\sim\chi^2(n)$ independientes. ¿Distribución de $F=(X_1/m)/(X_2/n)$?
- `arb3-q12` → **medium** · $X\sim N(0,1)$. Calcula $E[|X|]$.
- `arb3-q13` → **hard** · Para $X\sim\text{Poisson}(\lambda)$, calcula $P(X\text{ es par})$ usando la pgf.
- `arb3-q14` → **medium** · $X\sim\text{Weibull}(k,\lambda)$: $F(x)=1-e^{-(x/\lambda)^k}$. Calcula $E[X]$.
- `arb3-q15` → **hard** · Explica el TCL en términos de la función característica.

**`arena-q10` — Arena Quant · Distribuciones, geometría y estadísticos de orden**  · easy 0 / medium 5 / hard 5

- `arena-q10-q1` → **medium** · Romeo y Julieta llegan independientemente a una hora uniforme entre las 9 y las 10; cada uno espera 15 minutos…
- `arena-q10-q2` → **hard** · Rompes un palo en dos puntos elegidos uniformemente al azar. ¿Probabilidad de que los tres trozos formen un tr…
- `arena-q10-q3` → **hard** · 100 personas abordan un avión de 100 asientos en orden. La primera (la abuela) se sienta al azar; cada siguien…
- `arena-q10-q4` → **medium** · $X_1,\dots,X_n$ son uniformes i.i.d. en $[0,1]$. ¿$E(\max)$, $E(\min)$ y $E(\max-\min)$?
- `arena-q10-q5` → **hard** · Da la función de densidad del $k$-ésimo estadístico de orden de $n$ variables i.i.d. con densidad $f$ y CDF $F…
- `arena-q10-q6` → **medium** · $X$ e $Y$ son uniformes independientes en $[0,1]$. ¿Cuál es la densidad de $X+Y$?
- `arena-q10-q7` → **medium** · Si $X \sim N(\mu,\sigma)$, calcula $E(X^2)$ y $E(e^{\lambda X})$ para $\lambda>0$.
- `arena-q10-q8` → **hard** · $M$ es la Gaussiana acumulada (CDF de $N(0,1)$) y $X \sim N(0,1)$. ¿Cuánto vale $E[M(X)]$?
- `arena-q10-q9` → **medium** · Enuncia con precisión el Teorema del Límite Central. ¿Qué condición es imprescindible?
- `arena-q10-q10` → **hard** · Demuestra que toda matriz de covarianzas es semidefinida positiva.

**`arena-fc2` — Probabilidad geométrica**  · easy 0 / medium 5 / hard 10

- `arfc2-q1` → **hard** · La aguja de Buffon: una aguja de longitud L se lanza al azar sobre un piso con líneas paralelas separadas por …
- `arfc2-q2` → **medium** · Dos puntos $X$ e $Y$ se eligen independientemente en $[0,1]$. ¿Cuál es $P(|X-Y| < 1/3)$? ¿Y $P(X + Y > 1)$?
- `arfc2-q3` → **hard** · La paradoja de Bertrand: elige una cuerda 'al azar' en un círculo de radio 1. ¿Cuál es $P(\text{cuerda} > \tex…
- `arfc2-q4` → **hard** · Se eligen 3 puntos uniformemente en $[0,1]$. ¿Cuál es $P(\text{el mayor} - \text{el menor} < 1/2)$? Generaliza…
- `arfc2-q5` → **medium** · Monte Carlo para π: lanzas dardos al azar en el cuadrado [−1,1]². ¿Cuál es P(caer dentro del círculo unitario)…
- `arfc2-q6` → **hard** · Problema del palo roto (generalización): se rompe un palo en dos puntos elegidos uniformemente en $[0,1]$. ¿Cu…
- `arfc2-q7` → **medium** · Dos autobuses llegan a una parada de forma independiente, cada uno uniformemente entre las 12:00 y 13:00. ¿Cuá…
- `arfc2-q8` → **medium** · Un punto $P$ se elige uniformemente dentro de un círculo de radio $R$. ¿Cuál es $E[\text{distancia de }P\text{…
- `arfc2-q9` → **hard** · Se elige un ángulo $\theta$ uniformemente en $[0,2\pi)$ y se lanza una flecha en esa dirección desde el centro…
- `arfc2-q10` → **hard** · Problema de la aguja corta (generalización de Buffon): líneas horizontales Y también verticales, separadas por…
- `arfc2-q11` → **hard** · Tres puntos se eligen uniformemente en un segmento de longitud 1. ¿Cuál es $P(\text{el punto del medio está a …
- `arfc2-q12` → **hard** · Se eligen 2 puntos al azar en el perímetro de un cuadrado de lado 1. ¿Cuál es E[distancia euclidiana entre ell…
- `arfc2-q13` → **hard** · Cobertura circular: n puntos se eligen uniformemente en un círculo de radio 1. ¿Cuál es P(todos los puntos est…
- `arfc2-q14` → **medium** · Distancia de Manhattan: $X=(X_1,X_2)$ e $Y=(Y_1,Y_2)$ son puntos aleatorios uniformes en $[0,1]^2$. ¿Cuál es $…
- `arfc2-q15` → **hard** · Ley del arco seno: en una caminata aleatoria de 2n pasos (n grande), ¿cuál es la distribución aproximada de la…

**`arena-q4` — Arena Quant · Probabilidad y Bayes**  · easy 1 / medium 5 / hard 4

- `arq4-q1` → **medium** · Monty Hall: tienes 3 puertas. Elegiste la puerta 3. El anfitrión abre la 2 (siempre vacía) y te ofrece cambiar…
- `arq4-q2` → **medium** · Enfermedad con prevalencia 0.5%. Test: 100% sensible, 7% falsos positivos. Un desconocido da positivo. ¿Cuál e…
- `arq4-q3` → **hard** · Partes un palo al azar en dos puntos elegidos uniformemente en [0,1]. ¿Cuál es la probabilidad de que los tres…
- `arq4-q4` → **medium** · Tienes dos hijos y uno de ellos es una niña (no sabes nada del otro). ¿Cuál es P(ambos sean niñas)?
- `arq4-q5` → **easy** · De una baraja de 52 cartas sacas 2 sin reposición. ¿Cuál es P(ambas son Reyes)?
- `arq4-q6` → **medium** · X e Y se eligen independientemente de Uniforme[0,1]. ¿Cuál es P(XY > 1/2)?
- `arq4-q7` → **medium** · Un frasco tiene 999 monedas justas y 1 moneda con dos caras. Sacas una al azar, la lanzas 10 veces y obtienes …
- `arq4-q8` → **hard** · Lanzas una moneda justa. ¿Cuántos lanzamientos esperas para (a) 2 caras consecutivas? (b) 3 caras consecutivas…
- `arq4-q9` → **hard** · Revólver de 6 recámaras: 2 balas contiguas cargadas. Se giró el tambor al azar y sobreviviste al primer dispar…
- `arq4-q10` → **hard** · Tienes 50 bolas blancas y 50 negras, y 2 frascos. Distribúyelas como quieras. Con ojos vendados se elige un fr…

**`arena-q9` — Arena Quant · Probabilidad condicional, Bayes y conteo**  · easy 2 / medium 5 / hard 3

- `arena-q9-q1` → **medium** · Una bolsa tiene 9 monedas normales y 1 de dos caras. Sacas una y sale cara 3 veces seguidas. ¿Probabilidad de …
- `arena-q9-q2` → **medium** · Sacas una moneda 'de aspecto normal' del bolsillo y salen 3 caras seguidas. ¿Probabilidad de que la siguiente …
- `arena-q9-q3` → **medium** · Mazo ordenado A>K>Q>…>2 (con palos, 52 cartas). Tú sacas una carta y luego yo otra. ¿Probabilidad de que mi ca…
- `arena-q9-q4` → **easy** · Cajón con 2 calcetines rojos y 2 negros. Sacas 2 al azar. ¿Probabilidad de que emparejen (mismo color)?
- `arena-q9-q5` → **easy** · Sacas 2 cartas de un mazo. ¿Probabilidad de que ambas sean ases (a) con reposición y (b) sin reposición?
- `arena-q9-q6` → **hard** · Lanzas una moneda justa 1 000 000 de veces. ¿Número esperado de cadenas '6 caras seguidas de 6 cruces' (CCCCCC…
- `arena-q9-q7` → **medium** · Torneo eliminatorio con 2ⁿ equipos; el de mayor ranking siempre gana. Emparejamientos iniciales al azar. ¿Prob…
- `arena-q9-q8` → **hard** · ¿Es posible que tres activos A,B,C tengan ρ(A,B)=0.9, ρ(B,C)=0.8 y ρ(A,C)=0.1?
- `arena-q9-q9` → **medium** · Da un ejemplo de distribución con varianza infinita y explica por qué importa.
- `arena-q9-q10` → **hard** · Ruleta rusa: dos balas en recámaras CONTIGUAS de un revólver de 6 tiros. Se gira el tambor, aprietas el gatill…

**`arena-fc3` — Paradojas probabilísticas y condicionales**  · easy 0 / medium 9 / hard 6

- `arfc3-q1` → **medium** · La paradoja de la caja de Bertrand: hay 3 cajas — GG (dos monedas de oro), GP (una de oro y una de plata), PP …
- `arfc3-q2` → **hard** · El problema de los dos hijos: una familia tiene dos hijos. (a) Dado que al menos uno es niño, ¿P(ambos son niñ…
- `arfc3-q3` → **hard** · El problema de los tres prisioneros: A, B, C esperan sentencia. Uno será liberado al azar. A le pregunta al gu…
- `arfc3-q4` → **hard** · La paradoja de los dos sobres: un sobre tiene el doble que el otro (cantidades $X$ y $2X$). Ves que tu sobre t…
- `arfc3-q5` → **medium** · La paradoja de Simpson: en un hospital, el tratamiento A tiene mejor tasa de éxito que B en hombres (80% vs 70…
- `arfc3-q6` → **hard** · La paradoja de la inspección: llegan autobuses con intervalo promedio de 10 minutos (proceso de Poisson). Lleg…
- `arfc3-q7` → **medium** · La falacia del fiscal: un acusado tiene tipo de sangre que coincide con el de la escena del crimen (1% de la p…
- `arfc3-q8` → **medium** · ¿Cuántos números debes elegir aleatoriamente de {1,…,n} (con reemplazo) para que la probabilidad de obtener al…
- `arfc3-q9` → **medium** · La paradoja del examen sorpresa: un profesor dice 'habrá un examen sorpresa algún día de la semana'. Los alumn…
- `arfc3-q10` → **hard** · Adivinación de barajas con estrategia: las 52 cartas de una baraja se voltean una a una. Puedes hacer UNA sola…
- `arfc3-q11` → **hard** · Urna con bolas numeradas: una urna tiene bolas $1, 2, \dots, N$. Sacas una y ves el número $k$. ¿Cuál es tu es…
- `arfc3-q12` → **medium** · Probabilidad condicional con múltiples tests: un test médico tiene sensibilidad 95% y especificidad 95%. La pr…
- `arfc3-q13` → **medium** · Paradoja del ahorro: si cada persona ahorra más, el ahorro total del país puede bajar (paradoja de la frugalid…
- `arfc3-q14` → **medium** · Problema del azar y el tiempo: lanzas una moneda justa hasta obtener cara. El tiempo de espera es X (geométric…
- `arfc3-q15` → **medium** · El cazador y el pato: un cazador dispara y acierta con probabilidad $p = 0.4$ por disparo. ¿Cuántos disparos n…

**`arena-q3` — Arena Quant · Brainteasers y lógica cuantitativa**  · easy 2 / medium 9 / hard 0

- `arq3-q1` → **easy** · ¿Cuál es la suma de los enteros del 1 al 100? Generaliza: da la fórmula para la suma del 1 al n y explica el r…
- `arq3-q2` → **medium** · ¿Cuántos grados hay entre el minutero y el horario de un reloj analógico cuando marca las 3:15?
- `arq3-q3` → **medium** · ¿Cuándo es la primera vez después de las 3:00 PM que el minutero y el horario quedan exactamente superpuestos?
- `arq3-q4` → **medium** · 100 bombillas en fila, apagadas. La persona k (k=1…100) activa/desactiva cada k-ésima bombilla. ¿En qué estado…
- `arq3-q5` → **medium** · Con las mismas 100 bombillas y 100 personas: ¿cuántas bombillas quedan encendidas al final, y cuáles son?
- `arq3-q6` → **medium** · Una rana duplica su área cada día y cubre un estanque en 30 días. Si empiezas con 8 ranas idénticas, ¿en cuánt…
- `arq3-q7` → **medium** · ¿Cuántos ceros finales tiene 100! (100 factorial)? Explica el método general.
- `arq3-q8` → **medium** · Un macro-cubo de 10×10×10 microcubos flota en el aire. La capa exterior se desprende y cae. ¿Cuántos microcubo…
- `arq3-q9` → **medium** · En un tablero $20\times20$ la casilla $(i,j)$ tiene $i+j-1$ cubos ($i,j \in \{1,\dots,20\}$). ¿Cuántos cubos h…
- `arq3-q10` → **easy** · Un cajón tiene 8 calcetines rojos y 11 azules. Con la luz apagada, ¿cuántos calcetines debes sacar para GARANT…
- `arq3-q11` → **medium** · Juego de números: por turnos se dicen enteros. El primero en decir '50' gana. Reglas: el primer jugador empiez…

**`arena-q12` — Arena Quant · Brainteasers: trucos, invariantes y conteo**  · easy 3 / medium 4 / hard 3

- `arena-q12-q1` → **medium** · Copa de vino blanco y copa de tinto, 100 ml cada una. Pasas 5 ml de tinto al blanco, mezclas, y devuelves 5 ml…
- `arena-q12-q2` → **medium** · Estás en un bote en una piscina y tiras el ancla por la borda hasta el fondo. ¿Sube, baja o queda igual el niv…
- `arena-q12-q3` → **medium** · Una tableta de chocolate de n cuadritos. ¿Cuántas roturas (siempre por una línea recta de una sola pieza) nece…
- `arena-q12-q4` → **hard** · Una hormiga va de un vértice a su opuesto sobre la SUPERFICIE de un cubo de volumen 1 m³. ¿Cuál es la distanci…
- `arena-q12-q5` → **hard** · ¿Cuál es el número mínimo de pesas enteras para equilibrar exactamente cualquier peso entero de 1 a 40 usando …
- `arena-q12-q6` → **easy** · Tú y yo bebemos una pinta: yo tomo la mitad, tú la mitad de lo que queda, yo la mitad del nuevo resto, y así i…
- `arena-q12-q7` → **easy** · Un conejo sube una escalera de n peldaños dando saltos de 1 o 2 peldaños. ¿De cuántas formas distintas puede l…
- `arena-q12-q8` → **easy** · ¿De cuántas formas se puede embaldosar un tablero 2×n con fichas de dominó 2×1?
- `arena-q12-q9` → **medium** · Una vuelta a una pista de 1 milla la recorres a 30 mph de media. ¿A qué velocidad debes hacer la segunda vuelt…
- `arena-q12-q10` → **hard** · Empieza a nevar a ritmo constante en algún momento antes del mediodía. Un quitanieves arranca a las 12:00 con …

**`arena-q13` — Arena Quant · Brainteasers: lógica, inducción y juegos**  · easy 1 / medium 4 / hard 5

- `arena-q13-q1` → **hard** · Hay n leones hambrientos y un trozo de carne. Un león puede comerlo, pero al hacerlo se duerme y se vuelve pre…
- `arena-q13-q2` → **hard** · 50 isleños perfectamente lógicos tienen ojos azules o marrones; nadie conoce su propio color y no hay espejos.…
- `arena-q13-q3` → **medium** · Tienes 9 canicas idénticas salvo una más pesada, y una báscula de dos platillos. ¿En cuántas pesadas garantiza…
- `arena-q13-q4` → **medium** · Cuatro cartas muestran 7, 6, A, C. La afirmación es: 'si una carta tiene una vocal en una cara, tiene un númer…
- `arena-q13-q5` → **medium** · Juego de Nim: hay n cerillas; por turnos cada jugador toma 1, 2 o 3; el que toma la ÚLTIMA cerilla pierde. ¿Cu…
- `arena-q13-q6` → **hard** · Por turnos colocáis monedas idénticas sobre una mesa redonda, sin solapar ni salirse; pierde quien no pueda co…
- `arena-q13-q7` → **hard** · Un rectángulo pequeño está completamente dentro de uno grande, en posición y orientación arbitrarias. Con una …
- `arena-q13-q8` → **hard** · 22 presos en 22 celdas. Uno a uno, al azar, entran a una sala con dos interruptores (inicialmente abajo); el p…
- `arena-q13-q9` → **medium** · ¿Cuántos cuadritos 1×1×1 de un cubo 4×4×4 tienen pintura, si se pinta toda la superficie exterior del cubo gra…
- `arena-q13-q10` → **easy** · Calcula mentalmente 15³ y estima su magnitud antes de dar el número exacto.

**`arena-q8` — Arena Quant · Esperanza, juegos y parada óptima**  · easy 1 / medium 7 / hard 2

- `arena-q8-q1` → **medium** · Tiras un dado justo hasta 3 veces; en cada tiro puedes quedarte con el número (en dólares) o volver a tirar. ¿…
- `arena-q8-q2` → **medium** · Cuatro cajas selladas; una contiene \$100 y el resto están vacías. Pagas $X$ por abrir una caja y tomar su con…
- `arena-q8-q3` → **medium** · Yo elijo un número $n$ de 1 a 100. Si lo adivinas te pago \$$n$; si no, nada. ¿Cuánto pagarías por jugar?
- `arena-q8-q4` → **hard** · Empiezas con \$1. Lanzas una moneda justa infinitas veces: en cara tu posición se duplica, en cruz se reduce a…
- `arena-q8-q5` → **medium** · Lanzas una moneda justa hasta que sale cara; N es el número de tiros (incluyendo la cara final). Calcula E(N) …
- `arena-q8-q6` → **medium** · Con una moneda justa, el juego para cuando aparecen dos caras (CC) o dos cruces (XX) consecutivas. ¿Tiempo esp…
- `arena-q8-q7` → **hard** · ¿Número esperado de lanzamientos de una moneda justa para obtener tres caras seguidas?
- `arena-q8-q8` → **easy** · Una moneda sesgada tiene probabilidad p de cara. ¿Tiempo esperado hasta la primera cara?
- `arena-q8-q9` → **medium** · Lanzas un dardo a una diana circular de radio R acertando el área uniformemente. ¿Distancia esperada al centro…
- `arena-q8-q10` → **medium** · Un dado de n caras justo. ¿Cuál es la esperanza de un tiro y la del 4.º día hábil del mes siendo jueves (seman…

**`arena-fc4` — Apuestas, colas y el azar en el tiempo**  · easy 1 / medium 4 / hard 10

- `arfc4-q1` → **hard** · En el juego del craps: lanzas dos dados. Ganas si sacas 7 u 11 en el primer lanzamiento; pierdes si sacas 2, 3…
- `arfc4-q2` → **medium** · Chuck-a-luck: tres dados; apuestas a un número (1-6); ganas \$1 por cada dado que muestra ese número, pierdes …
- `arfc4-q3` → **hard** · La caja de cerillas de Banach: tienes dos cajas con $n=20$ cerillas cada una. Eliges una al azar con $P=1/2$ c…
- `arfc4-q4` → **hard** · Estrategia atrevida vs tímida: tienes \$1 y quieres llegar a \$4. Puedes apostar en pasos de \$1 (tímida) o to…
- `arfc4-q5` → **medium** · La estrategia de duplicar (martingala): apuestas \$1, si pierdes doblas, si ganas empiezas de nuevo. ¿Por qué …
- `arfc4-q6` → **hard** · Rachas en lanzamientos de moneda: en $n=20$ lanzamientos de moneda justa, ¿cuál es $E[\text{longitud de la rac…
- `arfc4-q7` → **hard** · Tiempo de retorno a 0 en caminata aleatoria: ¿cuál es P(la caminata aleatoria simple 1D retorna a 0 por primer…
- `arfc4-q8` → **medium** · Cola de espera M/M/1: clientes llegan como $\text{Poisson}(\lambda=8/\text{hora})$, servicio toma tiempo $\tex…
- `arfc4-q9` → **hard** · El problema del elevador: un edificio de n pisos. El elevador empieza en el piso 1 y sube hasta el piso donde …
- `arfc4-q10` → **hard** · Problema de la ruina con ventaja: juegas en un casino con $P(\text{ganar})=0.51$ (ligeramente favorable). Empi…
- `arfc4-q11` → **hard** · Distribución de la suma máxima parcial: en una caminata aleatoria de $n$ pasos, ¿cuál es $E[\max_{0\le k\le n}…
- `arfc4-q12` → **hard** · Problema de la red de colas (Jackson network): dos servidores en serie, $\lambda=5/\text{hora}$, $\mu_1=8/\tex…
- `arfc4-q13` → **hard** · La paradoja del tiempo de espera (bus problem): los autobuses llegan con intervalos exponenciales de media 10 …
- `arfc4-q14` → **medium** · Tiempo hasta la ruina con apuestas de tamaño fijo: empiezas con \$10, cada apuesta es exactamente \$1, $p=0.5$…
- `arfc4-q15` → **easy** · El problema de la ruleta: juegas ruleta americana (38 números: 1-36, 0, 00). Apuestas \$1 al rojo (18 números)…

**`arena-b4` — Cadenas de Markov e inferencia bayesiana**  · easy 2 / medium 10 / hard 3

- `arb4-q1` → **easy** · Define la propiedad de Markov y explica por qué es útil.
- `arb4-q2` → **medium** · Cadena de Markov con $P=\begin{pmatrix}0.7 & 0.3\\ 0.4 & 0.6\end{pmatrix}$. Encuentra la distribución estacion…
- `arb4-q3` → **medium** · ¿Cuál es el tiempo esperado de retorno al estado $i$ con distribución estacionaria $\pi_i$?
- `arb4-q4` → **medium** · ¿Cuándo converge una cadena a su distribución estacionaria?
- `arb4-q5` → **hard** · ¿Por qué Metropolis-Hastings acepta la propuesta $y$ con probabilidad $\min(1, \pi(y)q(x\mid y)/(\pi(x)q(y\mid…
- `arb4-q6` → **medium** · ¿Qué significa que $\text{Beta}(\alpha,\beta)$ sea el prior conjugado para la binomial?
- `arb4-q7` → **medium** · Prior: $\theta\sim\text{Beta}(2,2)$. Observas 6 éxitos en 10 intentos. ¿Posterior?
- `arb4-q8` → **medium** · ¿Prior conjugado para Poisson y cuál es el posterior?
- `arb4-q9` → **medium** · ¿Cuál es el estimador de Bayes bajo pérdida cuadrática?
- `arb4-q10` → **medium** · Tres monedas: $P(\text{cara})=0.5, 0.8, 0.2$. Eliges al azar y sale cara. ¿$P(\text{elegiste la justa})$?
- `arb4-q11` → **hard** · Cadena de nacimiento-muerte, estados $\{0,1,2\}$, tasas $\lambda_0=2, \lambda_1=1, \mu_1=1, \mu_2=2$. Encuentr…
- `arb4-q12` → **medium** · ¿Qué es el mixing time de una cadena de Markov?
- `arb4-q13` → **hard** · $X_1,X_2\mid\mu\sim N(\mu,1)$ i.i.d., prior $\mu\sim N(0,\tau^2)$. ¿$E[\mu\mid X_1,X_2]$?
- `arb4-q14` → **medium** · Test: $H_0:\mu=0$ vs $H_1:\mu\ne0$. $\bar X=1.5$, $\sigma=3$, $n=36$. $z$-score y decisión a $\alpha=0.05$.
- `arb4-q15` → **easy** · IC del 95% para $\mu$: $\bar X=25$, $\sigma=10$, $n=100$.

**`arena-p3` — Procesos estocásticos y movimiento browniano**  · easy 0 / medium 4 / hard 11

- `arp3-q1` → **medium** · Define la caminata aleatoria simple $S_n = X_1+\dots+X_n$ con $P(X_i=+1)=P(X_i=-1)=1/2$ y $S_0=0$. Calcula $E[…
- `arp3-q2` → **hard** · Ruina del jugador: empiezas con \$$k$, barreras absorbentes en 0 y $N$, $P(\text{subir})=p$, $P(\text{bajar})=…
- `arp3-q3` → **hard** · Define el movimiento browniano estándar $B_t$. Enuncia sus 5 propiedades fundamentales y calcula $\text{Cov}(B…
- `arp3-q4` → **hard** · ¿Qué es la variación cuadrática de $B_t$? ¿Por qué es diferente de la variación total? ¿Qué implica para el le…
- `arp3-q5` → **hard** · ¿Qué es una martingala? Verifica que $B_t$, $B_t^2-t$ y $M_t = e^{\sigma B_t - \sigma^2 t/2}$ son martingalas …
- `arp3-q6` → **hard** · Tiempo de primer toque: $B_t$ es movimiento browniano y $T_a = \inf\{t \ge 0 : B_t = a\}$ para $a > 0$. ¿Es $E…
- `arp3-q7` → **hard** · Enuncia el principio de reflexión del movimiento browniano. Aplícalo para calcular $P(\max_{s\le t} B_s \ge a)…
- `arp3-q8` → **hard** · GBM: $dS = \mu S\,dt + \sigma S\,dW$. Usa el lema de Itô para derivar la distribución de $S(T)$. Calcula $E[S(…
- `arp3-q9` → **hard** · ¿Qué es un proceso de Ornstein-Uhlenbeck (OU)? ¿Cómo se diferencia del BM? ¿Para qué se usa en finanzas?
- `arp3-q10` → **medium** · Proceso de Poisson $N(t)$ con tasa $\lambda$. Calcula $E[N(t)]$, $\text{Var}[N(t)]$ y $P(N(t)=k)$. ¿Cuál es la…
- `arp3-q11` → **medium** · Mezcla y adelgazamiento de Poisson: (a) Si llegan coches y motos de forma independiente como $\text{Poisson}(3…
- `arp3-q12` → **medium** · Cadena de Markov: estados $\{0,1,2\}$ con matriz de transición $P = \begin{pmatrix}0.5 & 0.4 & 0.1\\ 0.2 & 0.6…
- `arp3-q13` → **hard** · ¿Por qué la caminata aleatoria en $\mathbb Z^1$ y $\mathbb Z^2$ es recurrente, pero en $\mathbb Z^3$ es transi…
- `arp3-q14` → **hard** · Explica el teorema de muestreo opcional (OST) de Doob. ¿Cuándo se puede aplicar para calcular el valor esperad…
- `arp3-q15` → **hard** · Cambio de medida (Girsanov): si $W_t$ es BM bajo $\mathbb P$ y $d\mathbb Q/d\mathbb P = e^{\theta W_T - \theta…

**`arena-q11` — Arena Quant · Movimiento browniano, Itô y martingalas**  · easy 0 / medium 4 / hard 7

- `arena-q11-q1` → **medium** · Define el movimiento browniano estándar $W_t$ y da el valor de $E(W_s W_t)$.
- `arena-q11-q2` → **medium** · Un paseo aleatorio simétrico en $\{0,\dots,1000\}$ arranca en 80; $\pm1$ con prob $\tfrac12$; para al tocar 0 …
- `arena-q11-q3` → **hard** · Si $S_t$ sigue un browniano geométrico $dS_t=\mu S_t\,dt+\sigma S_t\,dW_t$, ¿qué proceso sigue $(S_t)^2$?
- `arena-q11-q4` → **medium** · Dado $dS_t=\mu S_t\,dt+\sigma S_t\,dW_t$, deriva la SDE de $\log(S_t)$.
- `arena-q11-q5` → **hard** · Demuestra que $X_t=\cosh(\lambda W_t)\,e^{-\lambda^2 t/2}$ es una martingala.
- `arena-q11-q6` → **hard** · Si $W_t$ es browniano estándar, ¿es $W_t^3$ una martingala?
- `arena-q11-q7` → **hard** · Aplica Itô a $2^{W_t}$. ¿Es martingala?
- `arena-q11-q8` → **hard** · $W_t$ y $Z_t$ son dos movimientos brownianos independientes. ¿Cuál es la distribución del cociente $W_t/Z_t$?
- `arena-q11-q9` → **hard** · Para un browniano con $X_0=0$ y $X_1>0$, ¿cuál es la probabilidad de que $X_2<0$?
- `arena-q11-q10` → **hard** · Resuelve la SDE del proceso de Ornstein-Uhlenbeck $dX_t=\theta(\mu-X_t)\,dt+\sigma\,dW_t$.
- `arena-q11-q11` → **medium** · ¿Qué significa la regla $dt=(dW_t)^2$ y por qué importa en el lema de Itô?

**`arena-p4` — Cálculo y álgebra lineal para finanzas cuantitativas**  · easy 0 / medium 12 / hard 4

- `arp4-q1` → **medium** · Escribe las series de Taylor de $e^x$, $\sin x$ y $\cos x$ alrededor de 0. Usa la de $e^x$ para estimar $e^{0.…
- `arp4-q2` → **medium** · Evalúa los límites: (a) $\lim_{x\to0} \sin(x)/x$, (b) $\lim_{x\to0} (e^x - 1 - x)/x^2$, (c) $\lim_{x\to\infty}…
- `arp4-q3` → **medium** · Calcula $\int x\,e^x\,dx$ e $\int \ln x\,dx$ usando integración por partes. Enuncia la regla.
- `arp4-q4` → **hard** · Usa la expansión de Taylor del precio de una opción C(S) para interpretar Delta y Gamma. ¿Qué dice esta expans…
- `arp4-q5` → **medium** · Para matrices A y B compatibles, demuestra que tr(AB) = tr(BA). ¿Es cierto AB = BA en general? Da un contraeje…
- `arp4-q6` → **medium** · Para una matriz $A$ $n\times n$ con valores propios $\lambda_1,\dots,\lambda_n$ (contados con multiplicidad), …
- `arp4-q7` → **medium** · ¿Cuándo es una matriz simétrica positiva definida (SPD)? ¿Por qué toda matriz de covarianza es semidefinida po…
- `arp4-q8` → **medium** · Aplica Newton-Raphson para encontrar $\sqrt2$ empezando de $x_0 = 1.5$. Escribe la iteración y calcula 3 pasos…
- `arp4-q9` → **hard** · Problema de Markowitz: minimiza la varianza del portafolio $x^\top\Sigma x$ sujeto a $\mathbf 1^\top x=1$ (pes…
- `arp4-q10` → **medium** · Calcula la función generatriz de momentos $M_X(t) = E[e^{tX}]$ para $X \sim N(0,1)$ y $X \sim \text{Exp}(\lamb…
- `arp4-q11` → **medium** · Descompón $A = \begin{pmatrix}4&2\\2&3\end{pmatrix}$ en sus valores y vectores propios. Verifica que $A = P\La…
- `arp4-q12` → **medium** · Calcula $\int_0^\infty x^n e^{-x}\,dx$. ¿Cuál es la conexión con la función Gamma y el factorial?
- `arp4-q13` → **medium** · Regla trapezoidal: aproxima $\int_0^1 e^{-x^2}\,dx$ con $n=4$ subintervalos. ¿Cuál es el orden del error?
- `arp4-q14` → **hard** · ¿Qué es la transformada de Fourier de una función $f(x)$? ¿Por qué se usa en probabilidad (función característ…
- `arp4-q15` → **medium** · ¿Qué es PCA (Análisis de Componentes Principales)? ¿Cuál es el problema de optimización que resuelve? Aplica a…
- `arp4-q16` → **hard** · Calcula la integral gaussiana $\int_{-\infty}^\infty e^{-x^2}\,dx$. Usa el truco de elevar al cuadrado en 2D y…

**`arena-q5` — Arena Quant · Derivadas y mercados financieros**  · easy 1 / medium 6 / hard 3

- `arq5-q1` → **medium** · Black-Scholes con $\sigma=0$, $S=K=\$100$, $r=5\%$, $T=1$ año. ¿Cuánto vale la call europea? ¿Cómo la cubres s…
- `arq5-q2` → **medium** · Bajo Black-Scholes con $r=0$, sin dividendos, una call ATM europea y una put ATM europea (mismos $S, K, T$). ¿…
- `arq5-q3` → **medium** · Compras un straddle ATM: call + put con strike \$25, costo total \$5. ¿En qué precios al vencimiento ganas din…
- `arq5-q4` → **medium** · ¿Cuántas acciones debes tener (delta) para cubrir una call europea at-the-money?
- `arq5-q5` → **hard** · ¿Por qué theta y gamma tienen signos opuestos para opciones vainilla? ¿Es siempre así?
- `arq5-q6` → **medium** · La tasa spot a 5 años es 10% y la tasa spot a 10 años es 15% (anual). ¿Cuál es la tasa forward implícita del a…
- `arq5-q7` → **medium** · Juego de San Petersburgo: lanzas una moneda hasta que salga cara; en el lanzamiento $k$ ganas $\$2^k$. ¿Cuánto…
- `arq5-q8` → **easy** · Si la desviación estándar de los retornos anuales continuamente compuestos es 10%, ¿cuál es la desviación está…
- `arq5-q9` → **hard** · Call europea ATM: $S=K=\$100$, $r=0$, $T=1$ año. La SD del precio al vencimiento es \$10 ($\approx10\%$ vol). …
- `arq5-q10` → **hard** · ¿Por qué Black-Scholes usa la tasa libre de riesgo y no el retorno esperado μ del activo para valorar opciones…

**`arena-q7` — Finanzas avanzadas · Bonos, Greeks y procesos estocásticos**  · easy 1 / medium 9 / hard 4

- `arq7-q1` → **medium** · ¿Qué mide la duración de un bono? ¿Cuál es la duración de un bono cupón-cero con vencimiento en 5 años? ¿Y de …
- `arq7-q2` → **medium** · Un bono tiene duración modificada $D_\text{mod} = 6.5$ años. Si la tasa de interés sube 50 puntos base (0.50%)…
- `arq7-q3` → **hard** · Explica la convexidad de un bono. ¿Por qué un bono con mayor convexidad es preferible (con precio igual)? ¿Qué…
- `arq7-q4` → **medium** · Un bono tiene cupón del 5% y vence a la par en 3 años. Si la tasa de mercado es 7%, ¿el bono se negocia sobre …
- `arq7-q5` → **easy** · El portafolio A tiene retorno esperado 12%, desviación estándar 15%, tasa libre de riesgo 3%. El portafolio B …
- `arq7-q6` → **medium** · Según CAPM, una acción con $\beta = 1.5$, tasa libre de riesgo 2% y prima de mercado $(E[R_m] - r_f) = 6\%$. ¿…
- `arq7-q7` → **medium** · Una acción tiene correlación 0.6 con el mercado, desviación estándar del 20% y el mercado tiene $\sigma_m = 15…
- `arq7-q8` → **medium** · ¿Cuál es el signo de vega para una call y para una put? ¿Por qué ambas opciones valen más con mayor volatilida…
- `arq7-q9` → **medium** · ¿Cuál es el signo de rho (∂C/∂r) para una call europea vs una put europea? Explica la intuición.
- `arq7-q10` → **hard** · Enuncia la Paridad de Tasas de Interés Cubierta (CIP). Si la tasa USD a 1 año es 5% y la tasa EUR es 2%, ¿qué …
- `arq7-q11` → **medium** · Si $X \sim N(\mu, \sigma^2)$, calcula $E[e^X]$. ¿Cuál es la media de una distribución lognormal con parámetros…
- `arq7-q12` → **hard** · Enuncia el Lema de Itô para $f(t, S_t)$ donde $dS_t = \mu S_t\,dt + \sigma S_t\,dW_t$. Aplícalo para calcular …
- `arq7-q13` → **hard** · El precio de una acción sigue GBM: $S(0)=100, \mu=10\%, \sigma=20\%, T=1$ año. ¿Cuál es la distribución de $S(…
- `arq7-q14` → **medium** · ¿Por qué la volatilidad diaria se escala por √252 para obtener volatilidad anual? ¿Cuáles son los supuestos im…

**`arena-q6` — Estadística inferencial · Distribuciones y estimación**  · easy 3 / medium 12 / hard 0

- `arq6-q1` → **easy** · Para una distribución normal, ¿qué porcentaje de los datos cae dentro de $\mu\pm\sigma$, $\mu\pm2\sigma$ y $\m…
- `arq6-q2` → **medium** · Explica la diferencia entre la Ley de los Grandes Números (LGN) y el Teorema Central del Límite (TCL). ¿Pueden…
- `arq6-q3` → **easy** · El tiempo de espera en una tienda tiene $\sigma = 5$ minutos. Si tomas muestras de $n = 100$ clientes, ¿cuál e…
- `arq6-q4` → **medium** · Define el p-valor correctamente. ¿Qué afirmación es incorrecta: (A) $P(\text{datos tan extremos}\mid H_0\text{…
- `arq6-q5` → **medium** · Define error tipo I y error tipo II en una prueba de hipótesis. ¿Cuál es más grave en un test de detección de …
- `arq6-q6` → **medium** · ¿Qué es el poder estadístico de una prueba? Si $\beta = 0.20$, ¿cuál es el poder? ¿Qué factores lo aumentan?
- `arq6-q7` → **medium** · Sean $X$ e $Y$ con $\text{Var}(X) = 4$, $\text{Var}(Y) = 9$, $\text{Cov}(X,Y) = 3$. Calcula $\text{Var}(X + Y)…
- `arq6-q8` → **medium** · ¿Cuál es el rango posible del coeficiente de correlación $\rho(X,Y)$? Demuestra que $|\rho| \le 1$. ¿Cuándo $\…
- `arq6-q9` → **medium** · En una regresión lineal simple $Y = \beta_0 + \beta_1 X + \varepsilon$, ¿qué mide $R^2$? ¿Puede $R^2$ ser nega…
- `arq6-q10` → **medium** · Sea $Y$ el número de lanzamientos de una moneda justa hasta obtener cara. Calcula $E[Y]$ usando la ley de la e…
- `arq6-q11` → **medium** · Enuncia la ley de la varianza total. Aplícala: $X$ es el resultado de un dado justo (1-6). $Y = X^2$. Calcula …
- `arq6-q12` → **medium** · El problema del coleccionista de cupones: hay $n$ tipos distintos de cupones, distribuidos uniformemente. ¿Cuá…
- `arq6-q13` → **medium** · ¿Por qué la Estimación de Máxima Verosimilitud (MLE) para una distribución normal equivale a mínimos cuadrados…
- `arq6-q14` → **medium** · Si $Z_1, Z_2, \dots, Z_n$ son $N(0,1)$ independientes, ¿cuál es la distribución de $Q = \sum Z_i^2$? ¿Cuál es …
- `arq6-q15` → **easy** · Si $X \sim N(\mu, \sigma^2)$, ¿cuál es la distribución de $Y = aX + b$? ¿Y si $X_1, X_2$ son $N(\mu_1,\sigma_1…

### Estadística aplicada e inferencia (`stats-inf`)

**`arena-dg1` — Estimación puntual y propiedades de estimadores**  · easy 3 / medium 11 / hard 1

- `ardg1-q1` → **easy** · ¿Cuándo un estimador $\hat\theta$ es insesgado (unbiased)?
- `ardg1-q2` → **medium** · Para $X_1,\dots,X_n \sim N(\mu,\sigma^2)$, ¿es $S^2=\sum(X_i-\bar X)^2/(n-1)$ un estimador insesgado de $\sigm…
- `ardg1-q3` → **easy** · ¿Qué significa que un estimador sea consistente?
- `ardg1-q4` → **medium** · ¿Cuál es la información de Fisher $I(\theta)$ y qué mide?
- `ardg1-q5` → **medium** · Enuncia la cota de Cramér-Rao.
- `ardg1-q6` → **medium** · Para $X\sim\text{Bernoulli}(p)$ con $n$ observaciones, calcula $I(p)$.
- `ardg1-q7` → **medium** · ¿Cuándo $T(X)$ es un estadístico suficiente para $\theta$?
- `ardg1-q8` → **medium** · Para $X_1,\dots,X_n\sim\text{Poisson}(\lambda)$, muestra que $T=\sum X_i$ es suficiente para $\lambda$.
- `ardg1-q9` → **medium** · ¿Cuál es el estimador de momentos de $\theta$ para $X\sim\text{Uniform}[0,\theta]$?
- `ardg1-q10` → **hard** · Para Uniform$[0,\theta]$, compara MSE del estimador de momentos ($2\bar X$) y del MLE ($X_{(n)}\cdot(n+1)/n$).
- `ardg1-q11` → **medium** · ¿Qué es el UMVUE?
- `ardg1-q12` → **easy** · Para $X_1,\dots,X_n\sim\text{Exp}(\lambda)$, calcula el MLE de $\lambda$.
- `ardg1-q13` → **medium** · Explica la propiedad de invarianza del MLE.
- `ardg1-q14` → **medium** · Para $X\sim N(\mu,\sigma^2)$ con ambos parámetros desconocidos, calcula el MLE de $(\mu,\sigma^2)$.
- `ardg1-q15` → **medium** · ¿Qué es la eficiencia relativa de dos estimadores?

**`arena-dg2` — Máxima verosimilitud y familias exponenciales**  · easy 2 / medium 12 / hard 1

- `ardg2-q1` → **easy** · Para $X_1,\dots,X_n\sim\text{Bernoulli}(p)$, calcula el MLE de $p$.
- `ardg2-q2` → **medium** · Para $X_1,\dots,X_n\sim N(\mu,1)$ ($\sigma$ conocida), ¿cuál es la distribución del MLE $\hat\mu$?
- `ardg2-q3` → **easy** · ¿Qué es la log-verosimilitud de una muestra de Poisson$(\lambda)$?
- `ardg2-q4` → **medium** · Para $X\sim\text{Gamma}(\alpha,\beta)$ con ambos parámetros desconocidos, ¿tiene el MLE forma cerrada?
- `ardg2-q5` → **medium** · Enuncia la distribución asintótica del MLE.
- `ardg2-q6` → **medium** · ¿Cuál es el estadístico de Wald para $H_0:\theta=\theta_0$?
- `ardg2-q7` → **medium** · ¿Qué es el estadístico de razón de verosimilitudes (LRT)?
- `ardg2-q8` → **medium** · Para Bernoulli, calcula el LRT para $H_0:p=0.5$ con $n=100$, $\sum X_i=60$.
- `ardg2-q9` → **medium** · ¿Qué es el estadístico Score (o Rao) para $H_0:\theta=\theta_0$?
- `ardg2-q10` → **hard** · Para $X_1,\dots,X_n\sim\text{Cauchy}(\theta,1)$: $f(x\mid\theta)=1/(\pi(1+(x-\theta)^2))$, calcula la ecuación…
- `ardg2-q11` → **medium** · Para X~Bin(n,p) con n fijo, ¿cuál es la función de verosimilitud perfilada de p después de observar x=8 en n=2…
- `ardg2-q12` → **medium** · ¿Por qué el MLE de la varianza $\sigma^2$ (dividiendo por $n$) es sesgado?
- `ardg2-q13` → **medium** · Para $X\sim\text{Beta}(\alpha,\beta)$ con $\alpha=1$ y $\beta$ desconocida, calcula el MLE de $\beta$.
- `ardg2-q14` → **medium** · Calcula el IC del 95% para $p$ en Bernoulli con $n=100$, $\bar x=0.35$ usando la normal asintótica.
- `ardg2-q15` → **medium** · ¿Cuándo el MLE puede no existir o ser único?

**`arena-cb1` — Arena Inferencia · Suficiencia, completitud y Basu**  · easy 0 / medium 0 / hard 7

- `arena-cb1-q1` → **hard** · $X_1,\dots,X_n$ i.i.d. con $f(x_i\mid\theta) = e^{i\theta - x_i}\cdot I(x_i\ge i\theta)$, $i=1,\dots,n$. Muest…
- `arena-cb1-q2` → **hard** · $X_1,\dots,X_n$ i.i.d. Geométrica: $P(X=x\mid\theta)=\theta(1-\theta)^{x-1}$, $x=1,2,\dots$ Muestra que $\sum …
- `arena-cb1-q3` → **hard** · Demuestra que para $X_1,\dots,X_n$ i.i.d. $N(\theta, a\theta^2)$ con $a>0$ conocido, $T=(\sum X_i, \sum X_i^2)…
- `arena-cb1-q4` → **hard** · Sea $f(x\mid\theta) = (1/2\theta)\cdot I(-\theta<x<\theta)$, $\theta>0$. Encuentra el estadístico minimal sufi…
- `arena-cb1-q5` → **hard** · Enuncia el teorema de Basu y aplícalo: $X_1,\dots,X_n$ i.i.d. $N(\mu,\sigma^2)$ con ambos parámetros desconoci…
- `arena-cb1-q6` → **hard** · $X_1,\dots,X_n$ i.i.d. Uniform$(\theta, 2\theta)$, $\theta>0$. Encuentra el estadístico minimal suficiente y d…
- `arena-cb1-q7` → **hard** · $X_1,\dots,X_n$ i.i.d. con $f(x\mid\theta) = \theta x^{\theta-1}$, $0<x<1$, $\theta>0$. (a) Encuentra el estad…

**`arena-cb2` — Arena Inferencia · MLE, Cramér-Rao y UMVUE**  · easy 0 / medium 2 / hard 5

- `arena-cb2-q1` → **hard** · $X_1,\dots,X_n$ i.i.d. Uniform$[0,\theta]$. (a) Halla el MLE $\hat\theta$. (b) Calcula su sesgo. (c) Da un est…
- `arena-cb2-q2` → **hard** · $X_1,\dots,X_n$ i.i.d. con $f(x\mid\theta) = \theta x^{\theta-1}$, $0<x<1$, $\theta>0$. Halla el MLE de $\thet…
- `arena-cb2-q3` → **hard** · $X_1,\dots,X_n$ i.i.d. con densidad doble exponencial $f(x\mid\theta)=(1/2)e^{-|x-\theta|}$. Muestra que el ML…
- `arena-cb2-q4` → **medium** · $X_1,\dots,X_n$ i.i.d. Bernoulli$(p)$. Demuestra que $\bar X$ alcanza la cota de Cramér-Rao para $p$. ¿Cuál es…
- `arena-cb2-q5` → **hard** · $X_1,\dots,X_n$ i.i.d. $N(\theta,1)$. Halla el UMVUE de $\theta^2$ y calcula su varianza. ¿Supera la cota CR p…
- `arena-cb2-q6` → **hard** · $X_1,\dots,X_n$ i.i.d. Bernoulli$(p)$. Usa Rao-Blackwell para mejorar el estimador $\delta(X_1)=X_1$ de $p$ y …
- `arena-cb2-q7` → **medium** · Para la distribución Gamma$(\alpha,\beta)$ con $\alpha$ conocido, halla el MLE de $\beta$ y verifica que alcan…

**`arena-dg3` — Intervalos de confianza y tests de hipótesis**  · easy 0 / medium 15 / hard 0

- `ardg3-q1` → **medium** · ¿Qué es un pivote y cómo se usa para construir un IC?
- `ardg3-q2` → **medium** · IC del 95% para $\mu$ con $\sigma$ desconocida: $n=25$, $\bar X=10$, $S=4$.
- `ardg3-q3` → **medium** · IC del 95% para $\sigma^2$: $n=20$, $S^2=16$.
- `ardg3-q4` → **medium** · ¿Cuántas observaciones necesitas para que el IC del 95% de $p$ (Bernoulli) tenga semiancho $\le0.05$?
- `ardg3-q5` → **medium** · ¿Cuál es la interpretación frecuentista correcta de un IC del 95%?
- `ardg3-q6` → **medium** · Test z para $H_0:\mu=50$ vs $H_1:\mu\ne50$, $\sigma=10$, $n=100$, $\bar X=53$. ¿Rechazas al 1%?
- `ardg3-q7` → **medium** · ¿Qué es el p-value y cómo se interpreta?
- `ardg3-q8` → **medium** · Define la función de potencia de un test.
- `ardg3-q9` → **medium** · Enuncia el lema de Neyman-Pearson.
- `ardg3-q10` → **medium** · Test t para dos muestras independientes: $n_1=30$, $\bar X_1=10$, $S_1=3$; $n_2=25$, $\bar X_2=8$, $S_2=4$. $H…
- `ardg3-q11` → **medium** · ¿Qué es el IC por bootstrap y cómo difiere del paramétrico?
- `ardg3-q12` → **medium** · Para $H_0:\mu=0$ con $n=16$, $\bar X=2$, $S=8$, ¿cuál es el p-value del test t bilateral?
- `ardg3-q13` → **medium** · ¿Qué es la corrección de Bonferroni para tests múltiples?
- `ardg3-q14` → **medium** · Test chi-cuadrado de bondad de ajuste: 100 dados lanzados, observas [15,18,16,17,19,15]. ¿Rechazas la hipótesi…
- `ardg3-q15` → **medium** · ¿Qué es la potencia de un test y cómo se calcula el tamaño de muestra para alcanzarla?

**`arena-cb3` — Arena Inferencia · NP Lemma, LRT y tests UMP**  · easy 0 / medium 1 / hard 6

- `arena-cb3-q1` → **medium** · En 1000 lanzamientos de una moneda salen 560 caras. ¿Es razonable que la moneda sea justa? Plantea un test de …
- `arena-cb3-q2` → **hard** · Enuncia el Lema de Neyman-Pearson y aplícalo: $X_1,\dots,X_n$ i.i.d. $N(\mu,1)$. Test $H_0$: $\mu=0$ vs $H_1$:…
- `arena-cb3-q3` → **hard** · $X_1,\dots,X_n$ i.i.d. Poisson$(\lambda)$. Encuentra el test UMP de nivel $\alpha$ para $H_0$: $\lambda\le\lam…
- `arena-cb3-q4` → **hard** · $X\sim\text{Beta}(\theta,1)$, $f(x\mid\theta)=\theta x^{\theta-1}$, $0<x<1$, $\theta>0$. Encuentra el test UMP…
- `arena-cb3-q5` → **hard** · $X_1,\dots,X_n$ i.i.d. $N(\mu,\sigma^2)$ con $\sigma^2$ desconocida. Deriva el LRT para $H_0$: $\mu=\mu_0$ vs …
- `arena-cb3-q6` → **hard** · Dos muestras independientes: $X_1,\dots,X_n\sim N(\mu_X,\sigma^2)$ y $Y_1,\dots,Y_m\sim N(\mu_Y,\sigma^2)$ con…
- `arena-cb3-q7` → **hard** · Se desea un test de nivel $\alpha=0.05$ para $H_0$: $\mu=\mu_0$ vs $H_1$: $\mu=\mu_1>\mu_0$ en $N(\mu,\sigma^2…

**`arena-cb4` — Arena Inferencia · Intervalos de confianza y métodos asintóticos**  · easy 0 / medium 2 / hard 5

- `arena-cb4-q1` → **medium** · $X_1,\dots,X_n$ i.i.d. $N(\mu,\sigma^2)$ con $\sigma^2$ desconocida. Construye un IC de nivel 95% para $\mu$ i…
- `arena-cb4-q2` → **hard** · $X_1,\dots,X_n$ i.i.d. Uniform$[0,\theta]$. (a) Muestra que $Q=X_{(n)}/\theta$ es un pivote. (b) Halla el IC d…
- `arena-cb4-q3` → **hard** · $X_1,\dots,X_n$ i.i.d. Exponencial$(\lambda)$. Construye un IC de nivel $1-\alpha$ para $\lambda$ invirtiendo …
- `arena-cb4-q4` → **hard** · Enuncia el método delta y aplícalo: $X_1,\dots,X_n$ i.i.d. Bernoulli$(p)$ y queremos un IC de nivel 95% para e…
- `arena-cb4-q5` → **medium** · $X_1,\dots,X_n$ i.i.d. $N(\mu,\sigma^2)$ con $\sigma^2$ conocida. ¿Cuál es el mínimo $n$ para garantizar que u…
- `arena-cb4-q6` → **hard** · El coeficiente de correlación muestral $\hat r$ de una muestra de tamaño $n$ tiene la propiedad de que su dist…
- `arena-cb4-q7` → **hard** · $X_1,\dots,X_n$ i.i.d. $N(\mu,\sigma^2)$ con ambos desconocidos. Usa la desigualdad de Bonferroni para constru…

**`arena-dg4` — Teoría de la decisión, regresión y modelos lineales**  · easy 1 / medium 14 / hard 0

- `ardg4-q1` → **medium** · ¿Qué es el riesgo frecuentista de un estimador?
- `ardg4-q2` → **medium** · ¿Qué es un estimador admisible?
- `ardg4-q3` → **medium** · Regresión OLS: $Y=\beta_0+\beta_1 X+\varepsilon$. Calcula las fórmulas de los estimadores $\hat\beta_0$ y $\ha…
- `ardg4-q4` → **medium** · Enuncia el teorema de Gauss-Markov.
- `ardg4-q5` → **medium** · ¿Qué mide R² en una regresión y cuáles son sus limitaciones?
- `ardg4-q6` → **medium** · $n=50$, $\hat\beta_1=2.3$, $\text{SE}(\hat\beta_1)=0.8$. ¿Cuál es el IC del 95% y el test de $H_0:\beta_1=0$?
- `ardg4-q7` → **medium** · ¿Cuál es el efecto de la multicolinealidad en las estimaciones OLS?
- `ardg4-q8` → **easy** · ¿Cuándo usar regresión logística en lugar de regresión lineal?
- `ardg4-q9` → **medium** · En logística: $\hat\beta_1=0.5$. ¿Cuál es el odds ratio por incremento de 1 en $X$?
- `ardg4-q10` → **medium** · ¿Qué supuestos del modelo lineal se verifican con los residuos?
- `ardg4-q11` → **medium** · ¿Cuál es el estimador de ridge regression y por qué reduce la varianza?
- `ardg4-q12` → **medium** · ¿Cuál es la diferencia entre ridge (L2) y lasso (L1)?
- `ardg4-q13` → **medium** · ¿Cuál es la función de pérdida implícita en OLS y cuándo no es apropiada?
- `ardg4-q14` → **medium** · ¿Qué es el criterio de información de Akaike (AIC)?
- `ardg4-q15` → **medium** · En ANOVA de una vía con k grupos e igual n por grupo, ¿cuándo rechazas la igualdad de medias?

**`arena-pst1` — Análisis exploratorio: estimadores robustos**  · easy 10 / medium 5 / hard 0

- `arpst1-q1` → **easy** · ¿Qué significa que un estimador sea 'robusto' y por qué la mediana lo es frente a la media?
- `arpst1-q2` → **easy** · ¿Qué es una media recortada (trimmed mean) y qué problema resuelve?
- `arpst1-q3` → **easy** · Para un pueblo donde de pronto se muda un multimillonario, ¿qué métrica de ingreso 'típico' reportarías y por …
- `arpst1-q4` → **medium** · ¿Por qué no se promedian directamente las desviaciones respecto a la media para medir dispersión?
- `arpst1-q5` → **easy** · Define varianza y desviación estándar. ¿Por qué se prefiere la desviación estándar para interpretar?
- `arpst1-q6` → **medium** · ¿Por qué la varianza divide entre n−1 y no entre n?
- `arpst1-q7` → **medium** · Ni la varianza ni la desviación estándar son robustas. ¿Qué métrica de dispersión usarías con outliers y cómo …
- `arpst1-q8` → **easy** · Calcula el IQR de los datos: 3, 1, 5, 3, 6, 7, 2, 9.
- `arpst1-q9` → **easy** · ¿Qué es un percentil (cuantil) y cómo se relaciona con la mediana?
- `arpst1-q10` → **easy** · ¿Qué muestra un boxplot y cómo marca los outliers?
- `arpst1-q11` → **easy** · ¿Por qué el rango (máx − mín) es una mala medida general de dispersión?
- `arpst1-q12` → **medium** · Ordena de mayor a menor la desviación estándar (sd), la MAD (media) y la MAD-mediana para datos normales, y di…
- `arpst1-q13` → **medium** · ¿Qué mide el coeficiente de correlación de Pearson y cuáles son sus dos limitaciones clave?
- `arpst1-q14` → **easy** · ¿Cuándo usarías una media o mediana ponderada en lugar de la simple?
- `arpst1-q15` → **easy** · Resume la regla práctica para elegir entre estimadores clásicos (media, sd) y robustos (mediana, IQR, MAD).

**`arena-pst2` — Distribuciones muestrales y bootstrap**  · easy 4 / medium 11 / hard 0

- `arpst2-q1` → **medium** · Distingue la distribución de los datos de la distribución muestral de un estadístico.
- `arpst2-q2` → **easy** · ¿Cuál es la diferencia entre desviación estándar y error estándar?
- `arpst2-q3` → **easy** · El error estándar de la media es $\text{SE} = s/\sqrt{n}$. Si quieres reducir el $\text{SE}$ a la mitad, ¿cuán…
- `arpst2-q4` → **medium** · ¿Qué dice el Teorema Central del Límite y por qué el libro sostiene que el data scientist no depende tanto de …
- `arpst2-q5` → **medium** · Describe el algoritmo del bootstrap para estimar la variabilidad de la media.
- `arpst2-q6` → **medium** · ¿Por qué el bootstrap muestrea CON reemplazo y no sin reemplazo?
- `arpst2-q7` → **medium** · ¿Cuál es el malentendido más común sobre el bootstrap? Da la advertencia correcta.
- `arpst2-q8` → **medium** · ¿Para qué tipo de estadísticos es especialmente valioso el bootstrap frente a las fórmulas clásicas?
- `arpst2-q9` → **medium** · ¿Cómo se aplica el bootstrap a datos multivariados y qué relación tiene con el bagging?
- `arpst2-q10` → **easy** · ¿Qué es un intervalo de confianza para un data scientist, según el enfoque práctico del libro?
- `arpst2-q11` → **medium** · ¿Cuál es la interpretación correcta de un intervalo de confianza del 95% y cuál la incorrecta?
- `arpst2-q12` → **easy** · ¿Qué es el sesgo de selección y qué es la self-selection bias?
- `arpst2-q13` → **medium** · Explica la regresión a la media y por qué puede confundirse con un efecto real.
- `arpst2-q14` → **medium** · ¿En qué se diferencia 'resampling' de 'bootstrap'?
- `arpst2-q15` → **medium** · Tienes la mediana de ingresos de 1000 préstamos y quieres reportar su incertidumbre, pero no recuerdas fórmula…

**`arena-pst3` — Experimentos estadísticos y tests de permutación**  · easy 4 / medium 11 / hard 0

- `arpst3-q1` → **easy** · ¿Qué es un A/B test y qué representa su hipótesis nula?
- `arpst3-q2` → **medium** · Describe los pasos de un test de permutación para comparar dos grupos.
- `arpst3-q3` → **medium** · En un test de permutación, ¿cómo decides si la diferencia observada es estadísticamente significativa?
- `arpst3-q4` → **medium** · ¿Qué ventajas tiene el test de permutación frente a un t-test clásico?
- `arpst3-q5` → **medium** · Define el p-valor en el contexto de un test de permutación.
- `arpst3-q6` → **easy** · ¿Qué es una variable proxy y cuándo se usa en un experimento?
- `arpst3-q7` → **easy** · Distingue error Tipo I y Tipo II en un experimento.
- `arpst3-q8` → **medium** · Define potencia estadística y di qué la aumenta.
- `arpst3-q9` → **medium** · ¿Qué es el tamaño del efecto (effect size) y por qué es necesario para calcular el tamaño de muestra?
- `arpst3-q10` → **medium** · Explica el problema de la multiplicidad con un ejemplo.
- `arpst3-q11` → **medium** · Según el enfoque práctico del libro, ¿cómo controla un data scientist la multiplicidad en modelado predictivo?
- `arpst3-q12` → **medium** · ¿Qué es la False Discovery Rate (FDR) y la corrección de Bonferroni?
- `arpst3-q13` → **medium** · ¿Para qué sirve ANOVA y en qué se diferencia de un test entre dos grupos?
- `arpst3-q14` → **easy** · ¿Cuándo usarías una prueba Chi-cuadrado en un experimento?
- `arpst3-q15` → **medium** · Una empresa quiere comparar dos páginas pero solo tiene 21 y 15 visitas con tiempos de sesión muy variables. ¿…

**`arena-pst4` — Regresión y predicción: interpretación y diagnóstico**  · easy 2 / medium 13 / hard 0

- `arpst4-q1` → **easy** · Diferencia el uso explicativo del uso predictivo de una regresión.
- `arpst4-q2` → **medium** · ¿Cómo se interpreta un coeficiente $b_j$ en una regresión lineal múltiple, y por qué esa cláusula causa proble…
- `arpst4-q3` → **medium** · ¿Qué es la multicolinealidad y cuándo es 'perfecta'? ¿Qué problema causa?
- `arpst4-q4` → **medium** · ¿Qué es una variable confusora (confounding) y cómo se distingue de la multicolinealidad?
- `arpst4-q5` → **medium** · En el ejemplo de precios de casas, los coeficientes de recámaras y baños salían negativos. ¿Qué causaba esto y…
- `arpst4-q6` → **medium** · ¿Qué es un término de interacción y cuándo lo necesitas?
- `arpst4-q7` → **medium** · Menciona maneras de decidir qué términos de interacción incluir en un modelo.
- `arpst4-q8` → **medium** · Distingue un intervalo de confianza de un intervalo de predicción en regresión.
- `arpst4-q9` → **medium** · ¿Por qué confundir el intervalo de confianza con el de predicción es peligroso al reportar una predicción indi…
- `arpst4-q10` → **easy** · ¿Qué son los residuales y por qué son la base del diagnóstico de una regresión?
- `arpst4-q11` → **medium** · ¿Qué es un residual estandarizado y cómo lo usas para detectar outliers en regresión?
- `arpst4-q12` → **medium** · Diferencia un outlier de un valor influyente (leverage) en regresión.
- `arpst4-q13` → **medium** · ¿Qué es la heteroscedasticidad y qué suele indicar?
- `arpst4-q14` → **medium** · ¿Por qué los residuales no normales rara vez preocupan al data scientist, según el libro?
- `arpst4-q15` → **medium** · ¿Por qué la multicolinealidad es menos problemática para árboles, clustering y kNN que para la regresión?

**`arena-isl1` — Arena Aprendizaje Estadístico · El marco (estimar f, sesgo-varianza, KNN)**  · easy 6 / medium 9 / hard 0

- `arisl1-q1` → **easy** · En el marco del aprendizaje estadístico se escribe Y = f(X) + ε. ¿Qué representan f y ε, y qué es 'estimar f'?
- `arisl1-q2` → **easy** · ¿Cuál es la diferencia entre estimar f para PREDICCIÓN y para INFERENCIA?
- `arisl1-q3` → **medium** · Distingue el error REDUCIBLE del IRREDUCIBLE. ¿Cuál es la cota inferior del error de predicción?
- `arisl1-q4` → **medium** · ¿Qué diferencia a un método PARAMÉTRICO de uno NO PARAMÉTRICO? Da pros y contras.
- `arisl1-q5` → **medium** · Explica el trade-off entre flexibilidad/precisión e interpretabilidad. ¿Por qué a veces se prefiere un modelo …
- `arisl1-q6` → **easy** · ¿Qué diferencia el aprendizaje SUPERVISADO del NO SUPERVISADO?
- `arisl1-q7` → **easy** · ¿Qué distingue un problema de REGRESIÓN de uno de CLASIFICACIÓN?
- `arisl1-q8` → **medium** · Al medir la calidad del ajuste con el MSE, ¿por qué no basta con el MSE de ENTRENAMIENTO?
- `arisl1-q9` → **medium** · Escribe e interpreta la descomposición sesgo-varianza del error de test esperado.
- `arisl1-q10` → **medium** · Define SESGO y VARIANZA de un método y di cómo cambian con la flexibilidad.
- `arisl1-q11` → **medium** · ¿Por qué la curva del MSE de test en función de la flexibilidad suele tener forma de U?
- `arisl1-q12` → **easy** · En clasificación, ¿cómo se mide la calidad del ajuste y qué es la tasa de error?
- `arisl1-q13` → **medium** · ¿Qué es el clasificador de Bayes y la tasa de error de Bayes?
- `arisl1-q14` → **easy** · ¿Cómo funciona KNN para clasificación y qué papel juega K?
- `arisl1-q15` → **medium** · En KNN, ¿qué pasa con K=1 frente a un K muy grande, en términos de sesgo y varianza?

**`arena-isl2` — Arena Aprendizaje Estadístico · Regresión lineal y clasificación**  · easy 2 / medium 13 / hard 0

- `arisl2-q1` → **easy** · En la regresión lineal simple, ¿cómo se estiman los coeficientes $\beta_0$ y $\beta_1$?
- `arisl2-q2` → **medium** · ¿Qué es el error estándar de un coeficiente y cómo se usa para un intervalo de confianza?
- `arisl2-q3` → **medium** · ¿Cómo se contrasta si un predictor tiene relación con la respuesta (test del coeficiente)?
- `arisl2-q4` → **easy** · ¿Qué miden el RSE y el R² como medidas de ajuste del modelo?
- `arisl2-q5` → **medium** · En regresión múltiple, ¿por qué el coeficiente de un predictor puede cambiar (incluso de signo) respecto a la …
- `arisl2-q6` → **medium** · ¿Para qué sirve el F-statistic y por qué no basta con mirar los t individuales?
- `arisl2-q7` → **medium** · ¿Cómo se incorporan predictores CUALITATIVOS (categóricos) a una regresión lineal?
- `arisl2-q8` → **medium** · ¿Qué es un término de INTERACCIÓN y qué dice el principio jerárquico (hierarchy)?
- `arisl2-q9` → **medium** · Enumera los principales problemas potenciales al ajustar una regresión lineal.
- `arisl2-q10` → **medium** · ¿Qué es la colinealidad, por qué es un problema y cómo se detecta con el VIF?
- `arisl2-q11` → **medium** · ¿Por qué NO se usa la regresión lineal directamente para clasificación?
- `arisl2-q12` → **medium** · ¿Qué modela la regresión logística y por qué es preferible a la lineal para probabilidades?
- `arisl2-q13` → **medium** · Explica el Análisis Discriminante Lineal (LDA): supuestos y forma de la frontera.
- `arisl2-q14` → **medium** · ¿En qué se diferencia QDA de LDA y cómo elegir entre ellos?
- `arisl2-q15` → **medium** · Al evaluar un clasificador, ¿qué aportan la matriz de confusión, sensibilidad/especificidad y la curva ROC/AUC…

**`arena-isl3` — Arena Aprendizaje Estadístico · Remuestreo, selección y regularización**  · easy 1 / medium 14 / hard 0

- `arisl3-q1` → **medium** · ¿Por qué necesitamos métodos de REMUESTREO en vez de confiar en el error de entrenamiento?
- `arisl3-q2` → **medium** · Describe el enfoque del VALIDATION SET y sus dos desventajas.
- `arisl3-q3` → **medium** · ¿Qué es LOOCV y cuáles son sus ventajas?
- `arisl3-q4` → **easy** · ¿Qué es la validación cruzada de k-fold?
- `arisl3-q5` → **medium** · Explica el trade-off sesgo-varianza del propio método de validación cruzada. ¿Por qué se prefiere k=5 o 10 sob…
- `arisl3-q6` → **medium** · ¿Cómo se usa la validación cruzada en problemas de CLASIFICACIÓN?
- `arisl3-q7` → **medium** · ¿Qué es el bootstrap y qué tipo de cantidad estima?
- `arisl3-q8` → **medium** · ¿Qué es la BEST SUBSET SELECTION y cuál es su limitación?
- `arisl3-q9` → **medium** · Compara la selección stepwise FORWARD y BACKWARD.
- `arisl3-q10` → **medium** · ¿Por qué no sirve el RSS/R² de entrenamiento para elegir el tamaño del modelo, y qué criterios se usan?
- `arisl3-q11` → **medium** · Explica la regresión RIDGE: qué penaliza y qué efecto tiene.
- `arisl3-q12` → **medium** · ¿Qué hace el LASSO distinto de ridge y por qué produce modelos dispersos?
- `arisl3-q13` → **medium** · ¿Cuándo conviene ridge y cuándo lasso?
- `arisl3-q14` → **medium** · Compara la Regresión por Componentes Principales (PCR) con Partial Least Squares (PLS).
- `arisl3-q15` → **medium** · ¿Qué es la 'maldición de la dimensionalidad' y qué hacer cuando p ≳ n?

**`arena-isl4` — Arena Aprendizaje Estadístico · No linealidad, árboles, SVM y no supervisado**  · easy 0 / medium 15 / hard 0

- `arisl4-q1` → **medium** · ¿Qué son la regresión polinómica, las funciones escalón y las funciones base?
- `arisl4-q2` → **medium** · ¿Qué es un spline de regresión (cúbico) y para qué sirven los nudos (knots)?
- `arisl4-q3` → **medium** · ¿Por qué suelen preferirse los splines a la regresión polinómica de alto grado?
- `arisl4-q4` → **medium** · ¿Qué son un spline suavizante y un GAM?
- `arisl4-q5` → **medium** · ¿Cómo construye un árbol de decisión sus predicciones y qué métrica usa al dividir?
- `arisl4-q6` → **medium** · ¿Cuáles son las ventajas y desventajas de los árboles frente a los modelos lineales?
- `arisl4-q7` → **medium** · ¿Qué es el bagging y por qué mejora a un solo árbol?
- `arisl4-q8` → **medium** · ¿Qué problema del bagging resuelve un Random Forest y cómo?
- `arisl4-q9` → **medium** · ¿Qué es el error OOB (out-of-bag) y por qué es útil?
- `arisl4-q10` → **medium** · ¿Cómo se mide la importancia de variables en bagging/random forests?
- `arisl4-q11` → **medium** · ¿Cómo funciona el boosting y cuáles son sus hiperparámetros clave?
- `arisl4-q12` → **medium** · ¿Qué es el clasificador de margen máximo y qué son los vectores de soporte?
- `arisl4-q13` → **medium** · ¿Qué aporta el support vector classifier (soft margin) y qué papel juega C?
- `arisl4-q14` → **medium** · ¿Cómo extiende la SVM al caso no lineal con el 'kernel trick' y cómo maneja >2 clases?
- `arisl4-q15` → **medium** · En aprendizaje NO supervisado, ¿qué hace PCA y en qué se diferencian K-means y el clustering jerárquico?

### Estructuras de datos y algoritmos (MAANG) (`dsa`)

**`arena-cc1` — Arrays, cadenas y tablas hash**  · easy 4 / medium 9 / hard 2

- `arcc1-q1` → **easy** · Dado un array de enteros y un target, describe el algoritmo $O(n)$ para encontrar dos números que sumen al tar…
- `arcc1-q2` → **medium** · ¿Cuál es la complejidad amortizada de insertar al final de un array dinámico (como Python list o Java ArrayLis…
- `arcc1-q3` → **easy** · Dado un string, verifica en $O(n)$ si es permutación de un palíndromo.
- `arcc1-q4` → **easy** · Sliding window: dado array nums y k, encuentra la suma máxima de un subarreglo de longitud exactamente k.
- `arcc1-q5` → **medium** · Longitud de la subcadena más larga sin caracteres repetidos. Describe el algoritmo.
- `arcc1-q6` → **medium** · Dado un array de n enteros, calcula el array de productos donde result[i] = producto de todos los elementos ex…
- `arcc1-q7` → **medium** · Rota un array de $n$ elementos $k$ posiciones a la derecha en $O(n)$ tiempo y $O(1)$ espacio. Describe el méto…
- `arcc1-q8` → **medium** · Ordena un array con solo valores $\{0,1,2\}$ en $O(n)$ con un solo recorrido y $O(1)$ espacio (Dutch National …
- `arcc1-q9` → **medium** · Dado una lista de intervalos [sᵢ,eᵢ] posiblemente solapados, combínalos. Describe el algoritmo.
- `arcc1-q10` → **medium** · ¿Cómo funciona el algoritmo de Rabin-Karp para buscar un patrón de longitud m en un texto de longitud n?
- `arcc1-q11` → **hard** · Trapping Rain Water: dado un array heights de alturas de barras, calcula el agua total atrapada.
- `arcc1-q12` → **medium** · ¿Cuándo conviene usar open addressing vs chaining para resolver colisiones en una tabla hash?
- `arcc1-q13` → **medium** · Encuentra todos los duplicados en un array de enteros donde $1 \le$ nums[i] $\le n$, $n=$ len(nums). $O(n)$ ti…
- `arcc1-q14` → **hard** · Minimum Window Substring: dado s y t, encuentra la ventana mínima en s que contiene todos los caracteres de t.
- `arcc1-q15` → **easy** · Two Sum con array ORDENADO: encuentra los dos índices con suma = target. $O(n)$ tiempo, $O(1)$ espacio.

**`arena-m1` — Arena MAANG · Hashing, frecuencia y memoria comprada**  · easy 1 / medium 2 / hard 1

- `arm1-q1` → **medium** · Describe el algoritmo two-sum en $O(n)$ tiempo y $O(n)$ espacio. ¿Por qué el orden 'buscar antes de insertar' …
- `arm1-q2` → **medium** · ¿Cuál es la complejidad de encontrar todos los tripletes que suman cero en un array de n enteros? Describe el …
- `arm1-q3` → **hard** · Un array tiene $n+1$ enteros, todos entre $1$ y $n$. Por tanto hay al menos un duplicado. Encuentra UN duplica…
- `arm1-q4` → **easy** · Ves un problema: 'dado un array de strings, agrupa los anagramas juntos'. ¿Qué estructura de datos usas y cuál…

**`arena-cc4` — Ordenamiento, búsqueda binaria y bits**  · easy 3 / medium 11 / hard 1

- `arcc4-q1` → **medium** · Compara QuickSort y MergeSort: complejidad, espacio y cuándo preferir cada uno.
- `arcc4-q2` → **easy** · Búsqueda binaria estándar: describe el invariante y la condición de parada.
- `arcc4-q3` → **medium** · Búsqueda binaria sobre la respuesta: 'mínima velocidad v para que el barco entregue todos los paquetes en d dí…
- `arcc4-q4` → **medium** · QuickSelect: encuentra el kth elemento más pequeño. Complejidad esperada y peor caso.
- `arcc4-q5` → **medium** · Buscar en un array rotado sin duplicados: [4,5,6,7,0,1,2], target=0.
- `arcc4-q6` → **medium** · Conteo de inversiones en un array: describe cómo usar MergeSort.
- `arcc4-q7` → **medium** · ¿Cómo construyes un heap de $n$ elementos en $O(n)$?
- `arcc4-q8` → **medium** · Top-k elementos más frecuentes en un array. ¿Cuál es el enfoque óptimo?
- `arcc4-q9` → **medium** · ¿Cuándo RadixSort es más eficiente que QuickSort?
- `arcc4-q10` → **easy** · Número faltante en [1..n] usando XOR. Explica por qué funciona.
- `arcc4-q11` → **easy** · ¿Qué hace n & (n-1) y para qué sirve?
- `arcc4-q12` → **medium** · Find Peak Element: un pico es un elemento mayor que sus vecinos. Encuentra uno en O(log n).
- `arcc4-q13` → **medium** · Merge k sorted lists en una sola lista ordenada. Complejidad óptima.
- `arcc4-q14` → **medium** · Elemento mayoritario (aparece más de $n/2$ veces). Describe el algoritmo $O(n)$ con $O(1)$ espacio.
- `arcc4-q15` → **hard** · Median de dos arrays ordenados de tamaños m y n. ¿Cuál es la complejidad óptima?

**`arena-cc2` — Árboles, grafos y búsqueda**  · easy 3 / medium 11 / hard 1

- `arcc2-q1` → **easy** · ¿Cuándo usas BFS en lugar de DFS para explorar un grafo?
- `arcc2-q2` → **easy** · ¿Cuál es la complejidad de BFS y DFS sobre un grafo con V vértices y E aristas?
- `arcc2-q3` → **medium** · Number of Islands: dado un grid 2D de '0's y '1's, cuenta el número de islas. Describe el algoritmo.
- `arcc2-q4` → **medium** · Orden topológico con el algoritmo de Kahn (BFS). ¿Cuándo no existe un orden topológico?
- `arcc2-q5` → **medium** · ¿Cómo validas que un árbol binario es un BST válido?
- `arcc2-q6` → **medium** · Lowest Common Ancestor (LCA) en un BST. Describe el algoritmo O(h).
- `arcc2-q7` → **easy** · Recorrido level-by-level (BFS) de un árbol binario. ¿Cómo sabes cuándo termina cada nivel?
- `arcc2-q8` → **medium** · Algoritmo de Dijkstra: ¿qué garantiza y cuándo falla?
- `arcc2-q9` → **medium** · ¿Cómo detectas un ciclo en un grafo dirigido con DFS?
- `arcc2-q10` → **medium** · Union-Find: describe las operaciones find y union con path compression y union by rank.
- `arcc2-q11` → **medium** · Trie: ¿en qué se diferencia de un hash set para almacenar strings?
- `arcc2-q12` → **medium** · Diámetro de un árbol binario: la longitud del camino más largo entre dos hojas. Describe el algoritmo.
- `arcc2-q13` → **medium** · ¿Cómo verificas si un grafo no dirigido es bipartito?
- `arcc2-q14` → **medium** · Clona un grafo con nodos y aristas arbitrarias en O(V+E).
- `arcc2-q15` → **hard** · Serialización de un árbol binario: ¿cómo reconstruyes el árbol exacto a partir de una secuencia?

**`arena-cc3` — Recursión y programación dinámica**  · easy 3 / medium 9 / hard 3

- `arcc3-q1` → **easy** · Climbing Stairs: llegas a un escalón n dando pasos de 1 o 2. ¿Cuántas formas distintas hay? Recurrencia y comp…
- `arcc3-q2` → **medium** · Coin Change (mínimo de monedas): monedas [1,5,11], amount=15. ¿Mínimo de monedas? ¿Falla greedy?
- `arcc3-q3` → **medium** · LCS de 'ABCBDAB' y 'BDCAB'. Escribe la recurrencia y da la longitud.
- `arcc3-q4` → **medium** · Edit Distance entre 'kitten' y 'sitting'. Recurrencia y valor.
- `arcc3-q5` → **medium** · Knapsack 0/1: items {(peso=2,val=6),(peso=2,val=10),(peso=3,val=12)}, W=5. ¿Máximo valor?
- `arcc3-q6` → **medium** · Número de formas de usar monedas [1,2,5] para hacer exactamente amount=5 (Coin Change 2).
- `arcc3-q7` → **medium** · Word Break: ¿puede 'leetcode' segmentarse usando el diccionario ['leet','code']? Describe el DP.
- `arcc3-q8` → **medium** · ¿Cuántas formas de decodificar '226' usando la regla A=1,...,Z=26?
- `arcc3-q9` → **easy** · Maximum profit con una transacción (buy low, sell high). Algoritmo $O(n)$.
- `arcc3-q10` → **medium** · Largest Square of 1s in binary matrix. Recurrencia DP.
- `arcc3-q11` → **easy** · Unique Paths: cuántos caminos únicos hay de esquina superior-izquierda a inferior-derecha en un grid $m\times …
- `arcc3-q12` → **medium** · ¿Cuándo la recursión con memoización es preferible a la tabulation (y viceversa)?
- `arcc3-q13` → **hard** · Palindrome Partitioning: número mínimo de cortes para que cada parte sea palíndromo. Recurrencia.
- `arcc3-q14` → **hard** · Burst Balloons: n globos con valores nums[i]. Al reventar el globo i ganas nums[i-1]\*nums[i]\*nums[i+1]. Maxi…
- `arcc3-q15` → **hard** · DP con bitmask: TSP con n=4 ciudades. ¿Cuántos estados tiene dp[mask][i]?

**`arena-m2` — Arena MAANG · SQL Window Functions**  · easy 0 / medium 3 / hard 1

- `arm2-q1` → **medium** · Tabla `ventas(id, empleado_id, monto, fecha)`. Escribe la consulta que devuelve para cada venta el monto acumu…
- `arm2-q2` → **medium** · ¿Cuándo usarías RANK en vez de ROW_NUMBER? Da un ejemplo donde la diferencia importa.
- `arm2-q3` → **hard** · Tabla `sesiones(session_id, user_id, inicio, fin)`. Escribe la consulta que devuelve los usuarios cuya sesión …
- `arm2-q4` → **medium** · En una entrevista te piden 'para cada producto, el porcentaje de ventas que representa respecto al total de su…

### Diseño de sistemas (MAANG) (`system-design`)

**`arena-sd1` — Fundamentos de escalabilidad y estimación**  · easy 10 / medium 5 / hard 0

- `arsd1-q1` → **easy** · ¿Por qué el tier de servidores web debe ser stateless y dónde se guarda entonces la sesión del usuario?
- `arsd1-q2` → **easy** · Compara escalado vertical y horizontal: ¿por qué a gran escala el horizontal es obligatorio?
- `arsd1-q3` → **medium** · Una app tiene 100 millones de usuarios activos diarios que hacen 5 acciones al día en promedio. Estima el QPS …
- `arsd1-q4` → **easy** · ¿Cuánto downtime al año implica una disponibilidad de 99.99% (cuatro nueves)? ¿Y 99.9%?
- `arsd1-q5` → **medium** · Describe la estrategia de caché read-through (cache-aside) y tres consideraciones al usarla.
- `arsd1-q6` → **easy** · ¿Qué es una CDN y qué tipo de contenido conviene servir desde ella?
- `arsd1-q7` → **medium** · Enumera en orden los pasos típicos para escalar de un solo servidor hacia millones de usuarios.
- `arsd1-q8` → **easy** · En el marco de 4 pasos de la entrevista de diseño, ¿qué se hace en el Paso 1 y por qué es el más importante?
- `arsd1-q9` → **easy** · ¿Qué es la 'sobre-ingeniería' y por qué es una bandera roja en una entrevista de diseño?
- `arsd1-q10` → **medium** · Ordena de más rápida a más lenta: lectura de SSD aleatoria, referencia a memoria principal, round trip interco…
- `arsd1-q11` → **medium** · Estima el almacenamiento de medios a 5 años de una red social con 150M usuarios diarios que suben 2 posts/día,…
- `arsd1-q12` → **easy** · ¿Para qué sirven las réplicas de lectura en una base de datos y qué problema introducen?
- `arsd1-q13` → **easy** · ¿Qué política de evicción de caché es la más común y qué decide?
- `arsd1-q14` → **easy** · En el Paso 4 (cerrar) de la entrevista, ¿qué cuatro cosas conviene mencionar?
- `arsd1-q15` → **easy** · ¿Cuántos bytes hay en un TB y en un PB usando potencias de 2, y por qué importa la convención?

**`arena-sd2` — Bloques distribuidos fundamentales**  · easy 1 / medium 12 / hard 2

- `arsd2-q1` → **medium** · Nombra cinco algoritmos de rate limiting y di cuál es el más usado y por qué.
- `arsd2-q2` → **easy** · ¿Qué código HTTP devuelve un rate limiter al rechazar, y qué cabeceras informativas suele incluir?
- `arsd2-q3` → **medium** · ¿Por qué 'servidor = hash(key) % n' es problemático al añadir o quitar un servidor, y cómo lo resuelve el cons…
- `arsd2-q4` → **medium** · ¿Qué problema resuelven los nodos virtuales (vnodes) en consistent hashing?
- `arsd2-q5` → **medium** · Enuncia el teorema CAP y explica por qué en la práctica eliges entre CP y AP (no CA).
- `arsd2-q6` → **medium** · Da un ejemplo de sistema que debe ser CP y uno que debe ser AP, justificando.
- `arsd2-q7` → **medium** · En un KV store con N=3 réplicas, ¿qué valores de W y R dan consistencia fuerte y por qué?
- `arsd2-q8` → **medium** · ¿Cómo se optimiza un quórum para lectura rápida y cómo para escritura rápida?
- `arsd2-q9` → **medium** · Distingue consistencia fuerte, débil y eventual. ¿Cuál adoptan Dynamo y Cassandra?
- `arsd2-q10` → **medium** · ¿Qué es un vector clock y qué resuelve que un timestamp simple no puede?
- `arsd2-q11` → **medium** · ¿Cómo detecta un KV store distribuido que un nodo se cayó, usando gossip protocol?
- `arsd2-q12` → **hard** · ¿Qué es hinted handoff y qué es anti-entropy con Merkle trees? ¿Qué tipo de fallo ataca cada uno?
- `arsd2-q13` → **hard** · Describe el write path y el read path de un KV store estilo Cassandra (LSM).
- `arsd2-q14` → **medium** · Para generar IDs únicos distribuidos, ¿por qué se descartan auto-increment de BD y UUID, y qué ofrece Snowflak…
- `arsd2-q15` → **medium** · Reparte los 64 bits de un ID Snowflake y di cuántos IDs por milisegundo puede emitir una máquina.

**`arena-sd3` — Sistemas de datos a escala**  · easy 1 / medium 13 / hard 1

- `arsd3-q1` → **medium** · En un acortador de URLs con base62, ¿cuántas URLs distintas representa una clave de 7 caracteres y por qué bas…
- `arsd3-q2` → **medium** · Al redirigir una URL corta, ¿cuándo usas 301 y cuándo 302, y qué pierdes con cada uno?
- `arsd3-q3` → **medium** · Compara los dos enfoques para generar la clave corta: hash con resolución de colisiones vs conversión de base …
- `arsd3-q4` → **medium** · ¿Qué es el URL frontier en un web crawler y qué dos responsabilidades clave tiene?
- `arsd3-q5` → **medium** · ¿Cómo implementa un crawler la 'politeness' para no sobrecargar un mismo servidor?
- `arsd3-q6` → **medium** · ¿Cómo evita un crawler procesar contenido duplicado de forma eficiente en memoria?
- `arsd3-q7` → **medium** · Nombra tres 'trampas' de la web que un crawler robusto debe manejar.
- `arsd3-q8` → **medium** · En un sistema de notificaciones, ¿por qué se coloca una cola de mensajes entre los servidores de notificación …
- `arsd3-q9` → **easy** · ¿Qué canales de notificación hay y qué proveedor de terceros se usa para cada uno?
- `arsd3-q10` → **medium** · ¿Cómo se garantiza no perder ni duplicar notificaciones?
- `arsd3-q11` → **medium** · Explica el trade-off entre fanout on write y fanout on read en un news feed.
- `arsd3-q12` → **hard** · ¿Qué es el problema de 'hotkey' en fanout on write y cómo lo resuelve el enfoque híbrido?
- `arsd3-q13` → **medium** · ¿Cómo se almacena un news feed para leerlo rápido y qué se guarda exactamente?
- `arsd3-q14` → **medium** · Un acortador recibe 100 escrituras/s (URLs nuevas) y una proporción lectura:escritura de 10:1. ¿Cuál es el QPS…
- `arsd3-q15` → **medium** · ¿Por qué un 'BFS simple' no basta para un web crawler a escala real?

**`arena-sd4` — Sistemas en tiempo real y de medios**  · easy 0 / medium 13 / hard 2

- `arsd4-q1` → **medium** · Para un chat en tiempo real, compara polling, long polling y WebSocket. ¿Cuál se elige y por qué?
- `arsd4-q2` → **medium** · ¿Por qué el servicio de chat es 'con estado' mientras otros servicios son stateless, y qué implica?
- `arsd4-q3` → **medium** · ¿Por qué se usa un KV store en vez de una BD relacional para los mensajes de chat, y qué propiedad debe tener …
- `arsd4-q4` → **medium** · ¿Cómo se implementa el estado de presencia (online/offline) en un chat?
- `arsd4-q5` → **medium** · ¿Cómo sincroniza un cliente de chat los mensajes tras reconectar?
- `arsd4-q6` → **medium** · En un autocompletado, ¿qué estructura se usa y cuál es la optimización clave para responder en <100 ms?
- `arsd4-q7` → **medium** · ¿Cómo se recolectan y actualizan los datos de popularidad del trie de autocompletado?
- `arsd4-q8` → **hard** · El trie de autocompletado es demasiado grande para una máquina. ¿Cómo se reparte?
- `arsd4-q9` → **medium** · En el diseño de YouTube, ¿qué hace el pipeline de transcodificación y por qué es necesario?
- `arsd4-q10` → **medium** · ¿Qué es el adaptive bitrate streaming y qué problema resuelve?
- `arsd4-q11` → **medium** · Servir todo el video desde CDN es carísimo. ¿Cómo se optimiza el costo?
- `arsd4-q12` → **medium** · En Google Drive, ¿qué es el almacenamiento por bloques y qué es delta sync?
- `arsd4-q13` → **medium** · ¿Cómo separa Google Drive los metadatos del contenido y por qué?
- `arsd4-q14` → **medium** · ¿Cómo se notifica a los demás dispositivos de un usuario que un archivo cambió en Drive?
- `arsd4-q15` → **hard** · ¿Qué hilo común conecta el trie de autocompletado, la CDN de YouTube y el feed precomputado del news feed?

### Ciencia de datos aplicada (`ds-applied`)

**`arena-ads1` — Probabilidad para ciencia de datos**  · easy 7 / medium 7 / hard 1

- `arads1-q1` → **easy** · Enuncia el teorema de Bayes nombrando prior, likelihood, evidencia y posterior. ¿Qué palabra en un enunciado s…
- `arads1-q2` → **medium** · Una en mil personas tiene una enfermedad. El test detecta al 98% de los enfermos y tiene 1% de falsos positivo…
- `arads1-q3` → **medium** · Dos monedas: una justa (cara/cruz) y una trucada (cruz en ambos lados). Eliges una al azar, la lanzas 5 veces …
- `arads1-q4` → **medium** · Dos equipos parejos (50% cada uno por juego, sin empates) juegan una serie al mejor de 7 (gana quien llega a 4…
- `arads1-q5` → **medium** · Lanzas un dado tres veces, uno tras otro. ¿Probabilidad de obtener tres números en orden estrictamente crecien…
- `arads1-q6` → **easy** · Enuncia la ley de probabilidad total y da un ejemplo de cuándo usarla en un problema de negocio.
- `arads1-q7` → **easy** · ¿Cuándo usas permutaciones y cuándo combinaciones? Da la fórmula de cada una y un ejemplo cotidiano.
- `arads1-q8` → **easy** · Distingue PMF, PDF y CDF. ¿Qué propiedades cumple toda CDF?
- `arads1-q9` → **easy** · Da la media y la varianza de la binomial$(n,p)$ y de la Poisson$(\lambda)$, y el caso de uso típico de cada un…
- `arads1-q10` → **easy** · ¿Qué distribución modela el tiempo entre eventos de un proceso de Poisson y qué propiedad notable tiene? Da su…
- `arads1-q11` → **medium** · ¿Qué es la propiedad de Markov y qué representa una distribución estacionaria $\pi$ de una cadena de Markov?
- `arads1-q12` → **medium** · Tres amigos en Seattle te dicen que está lloviendo; cada uno miente con prob. 1/3 independientemente. Si la pr…
- `arads1-q13` → **hard** · Una baraja de 100 cartas con valores 1..100. Sacas dos sin reemplazo. ¿Probabilidad de que el valor de una sea…
- `arads1-q14` → **medium** · Jugadores A y B se turnan lanzando una moneda con prob. p de cara (gana quien saca cara primero). A empieza. ¿…
- `arads1-q15` → **easy** · ¿Por qué la distribución normal aparece tan a menudo al modelar fenómenos reales y promedios?

**`arena-ads2` — Estadística e inferencia**  · easy 2 / medium 13 / hard 0

- `arads2-q1` → **medium** · Enuncia la Ley de los Grandes Números y el Teorema Central del Límite, y di en qué se diferencian.
- `arads2-q2` → **medium** · Define correctamente el p-valor. ¿Cuál es la interpretación errónea más común?
- `arads2-q3` → **medium** · Define los errores Tipo I y Tipo II y la potencia de una prueba. ¿Cómo se relacionan con α y β?
- `arads2-q4` → **medium** · Describe los pasos de una prueba de hipótesis aplicada a un A/B test de una campaña de email que busca subir l…
- `arads2-q5` → **medium** · ¿Qué es un intervalo de confianza del 95% y cuál es su interpretación correcta (y la incorrecta)?
- `arads2-q6` → **medium** · ¿Qué relación hay entre un intervalo de confianza del 95% y una prueba de hipótesis a $\alpha=0.05$?
- `arads2-q7` → **medium** · Define MLE y MAP y di en qué se diferencian. ¿Cuándo coinciden?
- `arads2-q8` → **easy** · Sea X uniforme en [a,b]. Deriva su esperanza.
- `arads2-q9` → **medium** · ¿Qué prueba usarías para comparar frecuencias observadas vs esperadas en categorías (p.ej. si un dado es justo…
- `arads2-q10` → **easy** · Define covarianza y correlación. ¿Por qué suele preferirse la correlación?
- `arads2-q11` → **medium** · Una prueba con n pequeño no es significativa. Menciona tres formas de aumentar la potencia para detectar un ef…
- `arads2-q12` → **medium** · ¿Por qué con una muestra grande casi cualquier diferencia se vuelve estadísticamente significativa, y qué debe…
- `arads2-q13` → **medium** · ¿Qué es la corrección de Bonferroni y qué problema resuelve?
- `arads2-q14` → **medium** · Bajo H0, ¿por qué el número de caras en muchos lanzamientos puede tratarse con una normal, y cómo se estandari…
- `arads2-q15` → **medium** · ¿Qué significa que 'no rechazar H0' no es lo mismo que 'aceptar H0 como verdadera'?

**`arena-ads4` — SQL y product sense / A·B testing**  · easy 2 / medium 11 / hard 2

- `arads4-q1` → **medium** · Describe la táctica de 'trabajar hacia atrás' para escribir una consulta SQL compleja con varios joins y CTEs.
- `arads4-q2` → **easy** · ¿Cuál es la diferencia entre WHERE y HAVING en SQL?
- `arads4-q3` → **medium** · ¿Qué hace una window function que un GROUP BY no puede, y da dos funciones de ventana útiles con su caso de us…
- `arads4-q4` → **medium** · ¿Cómo calcularías la retención mes a mes de usuarios con SQL, conceptualmente?
- `arads4-q5` → **medium** · ¿Qué es una métrica North Star y por qué siempre debe acompañarse de métricas guardrail (counter)?
- `arads4-q6` → **easy** · Nombra las etapas del funnel de adquisición AARRR (pirate metrics) y para qué sirve el marco.
- `arads4-q7` → **medium** · Te dicen que el engagement de un producto cayó esta semana. Esboza un marco para diagnosticar la causa.
- `arads4-q8` → **medium** · Distingue causa raíz, factor contribuyente y resultado correlacionado al diagnosticar un cambio de métrica.
- `arads4-q9` → **medium** · Esboza cómo diseñarías un A/B test para una nueva feature: qué defines antes de lanzarlo.
- `arads4-q10` → **medium** · ¿Qué es el efecto novedad en un A/B test y cómo lo detectas y mitigas?
- `arads4-q11` → **hard** · Explica por qué los efectos de red sesgan un A/B test en una red social y cómo mitigarlo.
- `arads4-q12` → **medium** · ¿Qué es el problema de pruebas múltiples y cómo se controla?
- `arads4-q13` → **medium** · Tu A/B test da p<0.05 a favor del tratamiento. ¿Por qué eso no implica automáticamente lanzar la feature?
- `arads4-q14` → **medium** · Al enfrentar una pregunta abierta de product sense ('¿deberíamos lanzar X?'), ¿cuáles son los primeros pasos d…
- `arads4-q15` → **hard** · Un PM quiere reemplazar un feed cronológico por uno rankeado por ML. ¿Qué métricas primaria y guardrail propon…

**`arena-cds1` — Feature engineering y preparación de datos**  · easy 6 / medium 9 / hard 0

- `arcds1-q1` → **easy** · ¿Qué es feature engineering y por qué suele importar más que la elección del algoritmo?
- `arcds1-q2` → **easy** · Define data leakage y explica por qué produce un rendimiento engañosamente optimista.
- `arcds1-q3` → **medium** · Vas a estandarizar (z-score) tus features. Describe el orden correcto de pasos para evitar data leakage.
- `arcds1-q4` → **medium** · Distingue los mecanismos MCAR, MAR y MNAR de datos faltantes.
- `arcds1-q5` → **medium** · ¿Qué técnica de manejo de faltantes usarías para cada mecanismo y por qué?
- `arcds1-q6` → **medium** · ¿Por qué hay que escalar las features antes de usar kNN, k-means o PCA?
- `arcds1-q7` → **easy** · Da la fórmula del min-max scaling y del z-score scaling, y di a qué rango lleva cada uno.
- `arcds1-q8` → **medium** · ¿Cuándo prefieres z-score sobre min-max scaling?
- `arcds1-q9` → **easy** · ¿Para qué sirve una transformación logarítmica y a qué tipo de datos se aplica?
- `arcds1-q10` → **easy** · ¿Qué es one-hot encoding y cuándo lo usas en vez de codificar categorías como enteros?
- `arcds1-q11` → **medium** · Un colega aplica StandardScaler a todo el dataset y luego hace train_test_split. ¿Qué problema hay y cómo lo c…
- `arcds1-q12` → **medium** · ¿Por qué un Pipeline (p.ej. de scikit-learn) ayuda a prevenir data leakage?
- `arcds1-q13` → **easy** · ¿Qué problema busca resolver la reducción de dimensionalidad en la preparación de datos?
- `arcds1-q14` → **medium** · Tienes una feature 'fecha de cancelación' para predecir si un cliente cancelará. ¿Por qué es un caso peligroso…
- `arcds1-q15` → **medium** · ¿Cómo decides entre min-max y z-score si no estás seguro cuál conviene?

**`arena-ads3` — Machine Learning aplicado**  · easy 3 / medium 12 / hard 0

- `arads3-q1` → **medium** · Explica el trade-off sesgo-varianza como si fuera para un stakeholder no técnico, y di qué harías ante alta va…
- `arads3-q2` → **easy** · ¿Qué es el overfitting, cómo lo detectas y por qué los modelos más simples suelen generalizar mejor?
- `arads3-q3` → **medium** · Diferencia la regularización L1 de la L2. ¿Cuál produce modelos sparse y por qué es útil?
- `arads3-q4` → **medium** · Tienes un dataset con 99% de transacciones legítimas y 1% de fraude. ¿Por qué el accuracy es mala métrica y qu…
- `arads3-q5` → **medium** · Define precisión y recall con la matriz de confusión y explica su trade-off con un ejemplo médico.
- `arads3-q6` → **medium** · ¿Qué es el F1 score y cuándo lo prefieres sobre precisión o recall por separado?
- `arads3-q7` → **medium** · ¿Qué representan la curva ROC y el AUC?
- `arads3-q8` → **easy** · ¿Qué es la validación cruzada k-fold y por qué es mejor que un solo train/test split?
- `arads3-q9` → **medium** · ¿Cómo funciona la regresión logística y cuál es su limitación principal?
- `arads3-q10` → **medium** · ¿Qué supuesto hace Naive Bayes y por qué ese supuesto lo vuelve eficiente?
- `arads3-q11` → **medium** · Explica bootstrapping y bagging, y cómo los usa un Random Forest para reducir varianza.
- `arads3-q12` → **medium** · ¿En qué se diferencia el boosting (AdaBoost/XGBoost) del bagging?
- `arads3-q13` → **medium** · ¿Qué hace PCA, sobre qué matriz opera y cuáles son sus dos pitfalls más comunes?
- `arads3-q14` → **medium** · Describe el descenso de gradiente y el rol del learning rate. ¿Qué pasa si es demasiado grande o demasiado peq…
- `arads3-q15` → **easy** · ¿Cuál es la diferencia entre aprendizaje supervisado y no supervisado? Da un ejemplo de cada uno.

**`arena-cds2` — Deep learning: redes neuronales por dentro**  · easy 6 / medium 8 / hard 1

- `arcds2-q1` → **easy** · ¿Qué hace 'profunda' a una red de deep learning frente a una red neuronal estándar?
- `arcds2-q2` → **easy** · Describe los pasos de un forward pass en una sola neurona.
- `arcds2-q3` → **easy** · Diferencia el rol de los pesos y los sesgos (biases) en una red neuronal.
- `arcds2-q4` → **medium** · ¿Por qué la función de activación debe ser no-lineal? ¿Qué pasaría sin ella?
- `arcds2-q5` → **medium** · Empareja la activación adecuada para: (a) salida de clasificación binaria, (b) salida multiclase, (c) capa ocu…
- `arcds2-q6` → **medium** · ¿Qué es ReLU, qué ventaja tiene y qué es el problema de la 'dying ReLU'?
- `arcds2-q7` → **easy** · Explica el descenso de gradiente como proceso de entrenamiento de una red.
- `arcds2-q8` → **medium** · ¿Qué es backpropagation y qué herramienta matemática usa?
- `arcds2-q9` → **medium** · Relaciona función de pérdida, backpropagation y descenso de gradiente en el bucle de entrenamiento.
- `arcds2-q10` → **medium** · Describe el problema del gradiente que se desvanece: por qué ocurre y a qué redes afecta más.
- `arcds2-q11` → **medium** · ¿Qué es el gradiente que explota y cómo se mitiga?
- `arcds2-q12` → **hard** · ¿Qué son las inicializaciones Glorot/Xavier y He, y con qué activaciones se usa cada una?
- `arcds2-q13` → **easy** · ¿Para qué tipo de datos se usan típicamente las CNN y las RNN?
- `arcds2-q14` → **easy** · ¿Qué es el transfer learning en deep learning y por qué es útil con pocos datos?
- `arcds2-q15` → **medium** · Diferencia mínimo local de mínimo global en la optimización de una red, y por qué importa.

**`arena-cds3` — MLOps: despliegue y monitoreo en producción**  · easy 8 / medium 7 / hard 0

- `arcds3-q1` → **easy** · ¿Qué es MLOps y qué problema resuelve?
- `arcds3-q2` → **easy** · Nombra tres virtudes de un pipeline de modelo reproducible y automatizado.
- `arcds3-q3` → **easy** · ¿Qué es un contenedor y por qué es central para desplegar modelos de ML?
- `arcds3-q4` → **easy** · ¿Qué es Docker y qué define un Dockerfile?
- `arcds3-q5` → **medium** · ¿Qué diferencia hay entre Docker y Kubernetes en un pipeline de MLOps?
- `arcds3-q6` → **medium** · Tras desplegar un modelo, ¿cómo validas que funciona como se espera?
- `arcds3-q7` → **easy** · ¿Qué es el logging en un modelo en producción y para qué sirve?
- `arcds3-q8` → **easy** · ¿Qué es data drift y por qué degrada un modelo en producción?
- `arcds3-q9` → **medium** · ¿Cómo se detecta el data drift en la práctica?
- `arcds3-q10` → **medium** · Detectas data drift en tu modelo. ¿Cuál es la respuesta típica y por qué es 'fácil' bajo MLOps?
- `arcds3-q11` → **medium** · ¿Qué métricas, además de la precisión del modelo, conviene monitorear en producción?
- `arcds3-q12` → **easy** · ¿Qué son ETL y ELT en la ingesta de datos y en qué se diferencian?
- `arcds3-q13` → **easy** · ¿Para qué se usa Flask en el despliegue de un modelo dentro de un contenedor?
- `arcds3-q14` → **medium** · ¿Por qué la gobernanza (model governance) es parte de MLOps, especialmente en salud y finanzas?
- `arcds3-q15` → **medium** · Resume el ciclo completo de un modelo bajo MLOps, de los datos a producción.

**`arena-s1` — Arena ML Systems · Del modelo al sistema: skew, drift y rollback**  · easy 0 / medium 3 / hard 1

- `ars1-q1` → **medium** · Define training-serving skew, da tres causas típicas y la defensa principal.
- `ars1-q2` → **medium** · Data drift vs concept drift: define cada uno y di cómo monitorearías cada uno en producción.
- `ars1-q3` → **hard** · Reentrenas un modelo de ranking: el AUC offline sube de 0.85 a 0.91, pero al desplegarlo el CTR cae. Da al men…
- `ars1-q4` → **medium** · En una entrevista te dicen: 'diseña el sistema de ML para detectar transacciones fraudulentas'. ¿Cuál es tu PR…

**`arena-cds4` — Toolkit práctico: visualización, storytelling y Git**  · easy 13 / medium 2 / hard 0

- `arcds4-q1` → **easy** · ¿Qué tres cosas debe servir un buen gráfico, según el marco de storytelling?
- `arcds4-q2` → **easy** · ¿Cuándo usas un gráfico de barras y qué buena práctica evita malinterpretarlo?
- `arcds4-q3` → **easy** · ¿Para qué sirve un gráfico de líneas y cuál es su variante de serie de tiempo?
- `arcds4-q4` → **easy** · ¿Cuándo eliges un scatter plot y qué le puedes añadir para reforzar el mensaje?
- `arcds4-q5` → **easy** · ¿Qué muestra un histograma y por qué el tamaño del bin es crítico?
- `arcds4-q6` → **easy** · Empareja el gráfico con el objetivo: (a) comparar ventas por categoría, (b) ver la evolución del precio de una…
- `arcds4-q7` → **easy** · ¿Por qué un buen gráfico por sí solo no basta y qué añade el data storytelling?
- `arcds4-q8` → **medium** · Vas a presentar resultados a una audiencia ejecutiva (no técnica). ¿Cómo adaptas tu visualización y narrativa?
- `arcds4-q9` → **easy** · Describe el flujo mínimo de Git para guardar tu trabajo en un repositorio local, en orden.
- `arcds4-q10` → **easy** · ¿Qué es el staging area en Git y cómo deshaces un archivo que agregaste por error?
- `arcds4-q11` → **easy** · ¿Cómo enlazas un repositorio local con uno remoto en GitHub y subes tus cambios?
- `arcds4-q12` → **easy** · Menciona tres formas de inspeccionar la historia de un proyecto con git log.
- `arcds4-q13` → **easy** · ¿Qué papel juega pandas en el flujo de trabajo de un data scientist?
- `arcds4-q14` → **easy** · ¿Para qué sirve Bash/shell en el día a día de un data scientist?
- `arcds4-q15` → **medium** · Al crear un repo nuevo en GitHub para subir un proyecto local existente, ¿por qué conviene NO inicializarlo co…

### ML Systems y feature pipelines (`ml-systems`)

**`arena-rom1` — Arena Reglas de ML · Antes del ML y tu primer pipeline**  · easy 4 / medium 11 / hard 0

- `arrom1-q1` → **medium** · ¿Qué quiere decir la consigna 'haz ML como el gran ingeniero que eres, no como el gran experto en ML que no er…
- `arrom1-q2` → **easy** · Regla 1: ¿por qué no temer lanzar un producto sin machine learning?
- `arrom1-q3` → **medium** · Regla 2: ¿por qué diseñar e implementar métricas ANTES de formalizar el sistema de ML?
- `arrom1-q4` → **medium** · Regla 3: ¿cuándo conviene pasar de una heurística a machine learning?
- `arrom1-q5` → **medium** · Regla 4: ¿por qué el primer modelo debe ser simple y el foco estar en la infraestructura?
- `arrom1-q6` → **medium** · Regla 5: ¿qué significa probar la infraestructura independientemente del machine learning?
- `arrom1-q7` → **medium** · Regla 6: ¿qué peligro hay al copiar un pipeline existente para crear uno nuevo?
- `arrom1-q8` → **medium** · Regla 7: ¿cuáles son las cuatro formas de aprovechar una heurística existente en un sistema de ML?
- `arrom1-q9` → **medium** · Regla 8: ¿por qué importa conocer los requisitos de FRESCURA del sistema?
- `arrom1-q10` → **medium** · Regla 9: ¿por qué detectar problemas ANTES de exportar el modelo, y cómo se alerta según el caso?
- `arrom1-q11` → **medium** · Regla 10: ¿qué son los 'fallos silenciosos' y por qué son propios del ML?
- `arrom1-q12` → **easy** · Regla 11: ¿por qué dar dueños y documentación a las feature columns?
- `arrom1-q13` → **medium** · ¿Qué tres cosas debes determinar antes de que alguien pueda usar tu primer sistema de ML (Regla 4)?
- `arrom1-q14` → **easy** · Según el documento, ¿cuál es el enfoque básico de cuatro pasos para hacer buenos productos con ML?
- `arrom1-q15` → **easy** · ¿Qué distingue 'instance', 'label', 'feature' y 'objective' en la terminología del documento?

**`arena-dmls1` — Encuadre de problemas de ML: objetivos y tipos de tarea**  · easy 2 / medium 11 / hard 2

- `ardmls1-q1` → **medium** · ¿Por qué muchos proyectos de ML mueren pese a buenas métricas de ML, y cómo se evita?
- `ardmls1-q2` → **medium** · ¿En qué tipos de problema es más fácil mapear el rendimiento del modelo a métricas de negocio?
- `ardmls1-q3` → **medium** · Explica el desacople de objetivos (decoupling objectives) y el problema que resuelve.
- `ardmls1-q4` → **hard** · Da una razón concreta por la que desacoplar objetivos es mejor que una loss combinada, más allá de la limpieza…
- `ardmls1-q5` → **medium** · ¿Cuándo NO conviene usar ML para resolver un problema?
- `ardmls1-q6` → **medium** · Enumera condiciones que hacen a un problema buen candidato para ML.
- `ardmls1-q7` → **easy** · Diferencia clasificación binaria, multiclase y multietiqueta (multilabel).
- `ardmls1-q8` → **medium** · ¿Por qué Huyen considera la multietiqueta el tipo de tarea más problemático?
- `ardmls1-q9` → **hard** · Un sistema predice 'qué app abrirá el usuario'. Compara encuadrarlo como clasificación vs como ranking/regresi…
- `ardmls1-q10` → **medium** · ¿Por qué el diseño de un sistema de ML es iterativo y no lineal?
- `ardmls1-q11` → **medium** · ¿Qué problemas trae una alta cardinalidad de clases en clasificación?
- `ardmls1-q12` → **medium** · Una empresa quiere 'usar IA' pero su tarea es decidir casos legales únicos sin precedente. ¿Es buen caso de ML…
- `ardmls1-q13` → **easy** · ¿Por qué conviene empezar con una heurística simple antes de un modelo de ML?
- `ardmls1-q14` → **medium** · Una métrica de negocio común es la 'take-rate' de un recomendador. ¿Cómo conecta con las métricas de ML?
- `ardmls1-q15` → **medium** · Resume el principio central del encuadre de un problema de ML según Huyen.

**`arena-rom2` — Arena Reglas de ML · Tu primer objetivo y feature engineering**  · easy 0 / medium 15 / hard 0

- `arrom2-q1` → **medium** · Regla 12: ¿por qué no sobrepensar qué objetivo optimizar directamente al inicio?
- `arrom2-q2` → **medium** · Regla 13: ¿qué hace que una métrica sea un buen primer objetivo de ML?
- `arrom2-q3` → **medium** · Regla 13: ¿qué tipos de objetivo conviene EVITAR modelar directamente al inicio?
- `arrom2-q4` → **medium** · Regla 14: ¿por qué empezar con un modelo interpretable facilita el debugging?
- `arrom2-q5` → **medium** · Regla 14: ¿qué significa que un modelo de regresión esté 'calibrado'?
- `arrom2-q6` → **medium** · Regla 15: ¿por qué separar el filtrado de spam del ranking de calidad en una policy layer?
- `arrom2-q7` → **medium** · Regla 16: ¿qué significa 'planear lanzar e iterar' y por qué importa la complejidad añadida?
- `arrom2-q8` → **medium** · Regla 17: ¿por qué empezar con features observadas/reportadas en lugar de aprendidas?
- `arrom2-q9` → **medium** · Regla 19: ¿por qué usar features muy específicas cuando se puede?
- `arrom2-q10` → **medium** · Regla 20: explica discretización y cruces como formas de crear features.
- `arrom2-q11` → **medium** · Regla 21: ¿qué relación hay entre la cantidad de datos y el número de pesos en un modelo lineal?
- `arrom2-q12` → **medium** · Regla 22: ¿por qué limpiar las features que ya no usas y qué papel juega la cobertura?
- `arrom2-q13` → **medium** · ¿Cuál es la diferencia entre un 'objetivo' y una 'métrica' según el documento, y por qué importa?
- `arrom2-q14` → **medium** · Según la Regla 13, ¿qué ejemplos de comportamiento 'directamente observado y atribuible' conviene modelar?
- `arrom2-q15` → **medium** · ¿Por qué un cruce de muchas feature columns con texto puede sobreajustar, y qué alternativas hay (Regla 20)?

**`arena-dmls2` — Datos de entrenamiento: muestreo, etiquetas y desbalance**  · easy 2 / medium 11 / hard 2

- `ardmls2-q1` → **medium** · Diferencia el muestreo no probabilístico del aleatorio y su riesgo.
- `ardmls2-q2` → **easy** · ¿Qué es el muestreo estratificado y qué problema evita?
- `ardmls2-q3` → **hard** · Describe el algoritmo de reservoir sampling y qué garantiza.
- `ardmls2-q4` → **medium** · ¿Por qué reservoir sampling es valioso en producción?
- `ardmls2-q5` → **medium** · ¿Qué es importance sampling y cuándo se usa?
- `ardmls2-q6` → **easy** · ¿Qué son las natural labels y cuál es su ejemplo canónico?
- `ardmls2-q7` → **medium** · ¿Qué es el 'feedback loop length' y por qué importa?
- `ardmls2-q8` → **medium** · ¿Qué es la weak supervision con labeling functions?
- `ardmls2-q9` → **medium** · ¿Qué es active learning y por qué es más eficiente en etiquetas?
- `ardmls2-q10` → **medium** · ¿Qué es el problema de label multiplicity en hand labels y cómo se mitiga?
- `ardmls2-q11` → **medium** · ¿Por qué la accuracy es engañosa con desbalance de clases? Da un ejemplo.
- `ardmls2-q12` → **medium** · ¿Qué métricas y técnicas usarías ante un fuerte desbalance de clases?
- `ardmls2-q13` → **medium** · Diferencia oversampling de undersampling y un riesgo de cada uno.
- `ardmls2-q14` → **medium** · ¿Por qué la mayoría de los modelos en producción siguen siendo supervisados pese al auge del no supervisado?
- `ardmls2-q15` → **hard** · Tienes un stream de tweets ilimitado y quieres entrenar con una muestra uniforme, pero etiquetar es caro. Desc…

**`arena-mldp1` — Patrones de representación de datos y de problemas**  · easy 0 / medium 15 / hard 0

- `armldp1-q1` → **medium** · ¿Qué tres problemas de las variables categóricas resuelve el patrón Hashed Feature?
- `armldp1-q2` → **medium** · ¿Por qué hay que usar un hash de huella (fingerprint) determinista y NO uno criptográfico como MD5 en Hashed F…
- `armldp1-q3` → **medium** · ¿Cómo se elige el número de buckets en Hashed Feature y qué pasa si es muy alto o muy bajo?
- `armldp1-q4` → **medium** · ¿Qué es un embedding y qué ventaja tiene sobre one-hot encoding?
- `armldp1-q5` → **medium** · ¿Qué es un Feature Cross y por qué puede ayudar a un modelo simple?
- `armldp1-q6` → **medium** · ¿Qué problema aborda el patrón Multimodal Input?
- `armldp1-q7` → **medium** · En qué consiste el patrón Reframing y da un ejemplo de regresión reformulada como clasificación.
- `armldp1-q8` → **medium** · ¿Cuándo conviene reformular una clasificación como regresión?
- `armldp1-q9` → **medium** · ¿Qué es el patrón Multilabel y en qué se diferencia de la clasificación multiclase?
- `armldp1-q10` → **medium** · ¿Qué función de activación se usa en la capa de salida para multilabel y por qué, frente a multiclase?
- `armldp1-q11` → **medium** · ¿Cómo se parsea la salida de un modelo multilabel para tomar decisiones?
- `armldp1-q12` → **medium** · ¿Qué pasa con un valor fuera de vocabulario o un valor nuevo (cold-start) en Hashed Feature en serving?
- `armldp1-q13` → **medium** · En Reframing, ¿cómo afecta el ancho de los buckets a la precisión al reformular regresión como clasificación?
- `armldp1-q14` → **medium** · ¿Por qué es ventajoso modelar una distribución (PDF) en vez de un solo número en Reframing?
- `armldp1-q15` → **medium** · ¿Para qué sirve el multitask learning como alternativa al Reframing?

**`arena-rml2` — Datos como pasivo y principios de sistemas de entrenamiento confiables**  · easy 1 / medium 14 / hard 0

- `arrml2-q1` → **medium** · ¿Qué quiere decir tratar los datos como 'pasivo' (data as liability) y por qué 'más datos == mejor' es engaños…
- `arrml2-q2` → **medium** · Explica con el ejemplo del apagón de pagos en español por qué los pipelines de ML son especialmente sensibles …
- `arrml2-q3` → **medium** · Al perder datos, ¿cuál es la pregunta clave, y qué son MCAR, MAR y MNAR?
- `arrml2-q4` → **medium** · Diferencia pseudonimización de anonimización y explica el hallazgo de Latanya Sweeney.
- `arrml2-q5` → **medium** · ¿Por qué borrar datos 'de verdad' es difícil y qué dos optimizaciones propone el libro?
- `arrml2-q6` → **easy** · Enumera las fases del ciclo de vida del dato en un sistema de ML.
- `arrml2-q7` → **medium** · Nombra las técnicas de normalización que cita el libro y su riesgo común.
- `arrml2-q8` → **medium** · ¿Qué es un feature store y qué dos grandes problemas resuelve frente a 'un montón de archivos en un directorio…
- `arrml2-q9` → **medium** · ¿Qué es un model management system y qué tres funciones ofrece?
- `arrml2-q10` → **medium** · 'Models will be retrained': ¿por qué asumirlo siempre y qué guardar?
- `arrml2-q11` → **medium** · 'Models will have multiple versions (at the same time!)': ¿por qué y qué infraestructura requiere?
- `arrml2-q12` → **medium** · 'Good models will become bad': ¿cuáles son los dos planes de respaldo y cuál es la trampa del fallback?
- `arrml2-q13` → **medium** · 'Models can train too fast': ¿cómo ocurre y cómo se mitiga?
- `arrml2-q14` → **medium** · Distingue utilización (utilization) de eficiencia (efficiency) y por qué importan en ML.
- `arrml2-q15` → **medium** · ¿Qué es el training-serving skew y por qué es una causa común de caídas evitables?

**`arena-mldp2` — Ensembles, cascada, clase neutra y rebalanceo**  · easy 1 / medium 13 / hard 1

- `armldp2-q1` → **medium** · ¿En qué tres partes se descompone el error de un modelo de ML y cuál se puede influir?
- `armldp2-q2` → **medium** · ¿Qué es bagging, qué tipo de error reduce y por qué funciona?
- `armldp2-q3` → **medium** · ¿Qué es boosting, qué tipo de error reduce y cómo funciona?
- `armldp2-q4` → **medium** · ¿Qué es stacking y en qué se diferencia del simple promediado de modelos?
- `armldp2-q5` → **medium** · ¿Qué ensemble eliges para alto sesgo y cuál para alta varianza?
- `armldp2-q6` → **easy** · Menciona dos desventajas de los métodos de ensemble.
- `armldp2-q7` → **medium** · ¿Cómo se relaciona dropout con bagging?
- `armldp2-q8` → **medium** · ¿Qué problema aborda el patrón Cascade y cómo se descompone?
- `armldp2-q9` → **hard** · ¿Cuál es el riesgo central al entrenar una Cascade y por qué no es solo un Ensemble?
- `armldp2-q10` → **medium** · ¿Qué es el patrón Neutral Class y qué problema resuelve?
- `armldp2-q11` → **medium** · Da dos situaciones donde una clase neutra es útil.
- `armldp2-q12` → **medium** · ¿Por qué el accuracy es engañoso en datasets desbalanceados y qué métricas usar?
- `armldp2-q13` → **medium** · Explica downsampling y class weighting como soluciones al desbalance.
- `armldp2-q14` → **medium** · ¿Por qué precision y recall suelen estar en tensión y qué los distingue en el denominador?
- `armldp2-q15` → **medium** · Al reframe el desbalance como detección de anomalías o clustering, ¿qué idea se aplica?

**`arena-mldp3` — Patrones de entrenamiento y de serving resiliente**  · easy 0 / medium 14 / hard 1

- `armldp3-q1` → **medium** · ¿Qué es el patrón Useful Overfitting y cuándo es válido sobreajustar a propósito?
- `armldp3-q2` → **medium** · ¿Qué es 'overfitting a un batch' y para qué se usa?
- `armldp3-q3` → **medium** · ¿Qué es el patrón Checkpoints y por qué guardar el estado COMPLETO, no solo el modelo exportado?
- `armldp3-q4` → **medium** · Además de resiliencia, ¿qué dos capacidades habilitan los checkpoints?
- `armldp3-q5` → **medium** · ¿Por qué usar regularización puede ser mejor que early stopping?
- `armldp3-q6` → **medium** · ¿Qué es el patrón Transfer Learning y cómo se implementa con la capa cuello de botella?
- `armldp3-q7` → **medium** · ¿Qué problema resuelve el patrón Distribution Strategy y cuáles son sus dos enfoques?
- `armldp3-q8` → **medium** · En data parallelism, ¿qué diferencia hay entre entrenamiento síncrono y asíncrono?
- `armldp3-q9` → **medium** · Distingue parámetros de hiperparámetros y di por qué grid search no escala.
- `armldp3-q10` → **hard** · ¿Cómo funciona la optimización bayesiana para hiperparámetros y qué la diferencia del grid/random search?
- `armldp3-q11` → **medium** · ¿Qué es el patrón Stateless Serving Function y por qué escala?
- `armldp3-q12` → **medium** · ¿Qué es Batch Serving y cuándo conviene frente al serving online?
- `armldp3-q13` → **medium** · ¿Qué es el patrón Two-Phase Predictions y para qué sirve?
- `armldp3-q14` → **medium** · ¿Qué problema resuelve el patrón Keyed Predictions?
- `armldp3-q15` → **medium** · ¿Qué es la cuantización (quantization) y qué rol juega al servir en el edge?

**`arena-rom4` — Arena Reglas de ML · Fase III: modelos complejos y trade-offs**  · easy 1 / medium 12 / hard 2

- `arrom4-q1` → **medium** · ¿Qué señales indican que la Fase II del ciclo de ML se está cerrando y empieza la Fase III?
- `arrom4-q2` → **medium** · Regla 38: ¿qué hacer si el problema son objetivos desalineados, no la falta de features?
- `arrom4-q3` → **medium** · Regla 39: ¿por qué las decisiones de lanzamiento son un proxy de las metas de producto a largo plazo?
- `arrom4-q4` → **hard** · Regla 39: con A=(1M DAU, \$4M/día) y B=(2M DAU, \$2M/día), ¿por qué ningún equipo cambia al otro escenario?
- `arrom4-q5` → **medium** · Regla 39: ¿por qué los individuos tienden a favorecer un único objetivo y qué ofrece el ML multi-objetivo?
- `arrom4-q6` → **medium** · Regla 40: ¿cómo se mantiene un ensemble simple?
- `arrom4-q7` → **medium** · Regla 40: ¿qué propiedad de monotonicidad debe cumplir un ensemble?
- `arrom4-q8` → **medium** · Regla 41: cuando el rendimiento se estanca, ¿qué tipo de información buscar?
- `arrom4-q9` → **medium** · Regla 42: ¿por qué diversidad, personalización y relevancia no están tan correlacionadas con la popularidad co…
- `arrom4-q10` → **medium** · Regla 43: ¿qué transfiere bien entre productos y qué no?
- `arrom4-q11` → **hard** · Regla 38 vs Regla 41: ¿cómo distingues 'objetivos desalineados' de 'rendimiento estancado por falta de señales…
- `arrom4-q12` → **medium** · ¿Por qué predecir 'la salud última del producto' es considerado AI-complete en la Regla 39?
- `arrom4-q13` → **medium** · ¿Qué riesgo introduce apilar modelos entrenados por separado, y cómo lo previene la Regla 40?
- `arrom4-q14` → **medium** · Según la Regla 42, ¿cómo se debe incorporar diversidad/personalización/relevancia si se mide popularidad?
- `arrom4-q15` → **easy** · ¿Qué advertencia general hace el documento sobre toda la sección de Fase III?

**`arena-dmls3` — Despliegue y predicción: batch vs online, compresión y edge**  · easy 2 / medium 12 / hard 1

- `ardmls3-q1` → **easy** · Diferencia batch prediction de online prediction.
- `ardmls3-q2` → **medium** · ¿Cuándo conviene batch prediction y cuál es su principal riesgo?
- `ardmls3-q3` → **medium** · ¿Cuándo es obligatoria la online prediction y cuál es su reto técnico central?
- `ardmls3-q4` → **medium** · Diferencia batch features de streaming features.
- `ardmls3-q5` → **medium** · Diferencia el paso de datos request-driven del event-driven en sistemas de ML.
- `ardmls3-q6` → **easy** · Nombra las cuatro técnicas frecuentes de compresión de modelos.
- `ardmls3-q7` → **medium** · ¿Qué es knowledge distillation y da un ejemplo conocido?
- `ardmls3-q8` → **medium** · ¿Qué hace la quantization y cuál es su riesgo?
- `ardmls3-q9` → **medium** · ¿Qué es pruning y por qué a veces ayuda a generalizar?
- `ardmls3-q10` → **medium** · Compara desplegar en la nube vs en el edge (ventajas y costes).
- `ardmls3-q11` → **medium** · ¿Por qué la tendencia hacia el edge hace más relevante la compresión de modelos?
- `ardmls3-q12` → **medium** · Un servicio de búsqueda debe responder a queries arbitrarias en <100 ms. ¿Batch u online? ¿Qué features?
- `ardmls3-q13` → **medium** · ¿Por qué demasiadas features pueden ser un problema en online prediction?
- `ardmls3-q14` → **hard** · Quieres servir un modelo grande en móviles sin conexión estable. Esboza el plan.
- `ardmls3-q15` → **medium** · Resume las tres decisiones clave del despliegue de un modelo según Huyen.

**`arena-rml3` — Serving, monitoreo y observabilidad de modelos**  · easy 1 / medium 14 / hard 0

- `arrml3-q1` → **medium** · ¿Cuáles son las cuatro preguntas clave para diseñar el serving de un modelo?
- `arrml3-q2` → **medium** · ¿Qué estrategias hay ante alta carga (QPS)?
- `arrml3-q3` → **medium** · ¿Por qué replicar el modelo NO reduce la latencia de una predicción individual, y qué es la tail latency?
- `arrml3-q4` → **medium** · Compara los lugares donde puede 'vivir' un modelo: nube, servidores propios y on-device.
- `arrml3-q5` → **medium** · ¿Por qué las GPUs sirven para modelos deep y las CPUs pueden ser mejores para modelos sparse?
- `arrml3-q6` → **easy** · Nombra las cuatro categorías amplias de arquitecturas de serving.
- `arrml3-q7` → **medium** · Resume ventajas y desventajas del serving offline (batch inference).
- `arrml3-q8` → **medium** · Resume ventajas y desventajas del serving online.
- `arrml3-q9` → **medium** · ¿Qué ventajas aporta el enfoque Model-as-a-Service (MaaS)?
- `arrml3-q10` → **medium** · Para actualizar el modelo en serving sin caídas, ¿qué dos estrategias hay?
- `arrml3-q11` → **medium** · Diferencia monitoreo de observabilidad.
- `arrml3-q12` → **medium** · ¿Qué es el training-serving skew y por qué causa caídas difíciles de depurar?
- `arrml3-q13` → **medium** · ¿Cuál es el 'cambio de mentalidad' necesario para monitorear ML, y por qué?
- `arrml3-q14` → **medium** · ¿En qué tres niveles conviene dividir el monitoreo en serving, y qué se vigila del input data?
- `arrml3-q15` → **medium** · Retraining como 'roll-forward': ¿cuándo se usa y cuándo NO sirve para mitigar una caída?

**`arena-rom3` — Arena Reglas de ML · Análisis humano y training-serving skew**  · easy 0 / medium 15 / hard 0

- `arrom3-q1` → **medium** · Regla 23: ¿por qué 'no eres un usuario típico' y qué hacer en su lugar?
- `arrom3-q2` → **medium** · Regla 24: ¿cómo y por qué medir el 'delta' entre modelos?
- `arrom3-q3` → **medium** · Regla 25: ¿qué significa que 'el rendimiento utilitario gana a la potencia predictiva'?
- `arrom3-q4` → **medium** · Regla 26: ¿cómo se usan los errores medidos para crear nuevas features?
- `arrom3-q5` → **medium** · Regla 27: ¿qué significa 'mide primero, optimiza después'?
- `arrom3-q6` → **medium** · Regla 28: ¿por qué comportamiento idéntico a corto plazo no implica idéntico a largo plazo?
- `arrom3-q7` → **medium** · ¿Qué es el training-serving skew y cuáles son sus tres causas?
- `arrom3-q8` → **medium** · Regla 29: ¿cuál es la mejor forma de asegurar que entrenas como sirves?
- `arrom3-q9` → **medium** · Regla 30: ¿por qué ponderar por importancia los datos muestreados en vez de descartarlos?
- `arrom3-q10` → **medium** · Regla 31: ¿qué riesgo hay al joinear datos de una tabla en entrenamiento y serving?
- `arrom3-q11` → **medium** · Regla 32: ¿cómo ayuda reusar código entre los pipelines de entrenamiento y serving?
- `arrom3-q12` → **medium** · Regla 33: ¿por qué testear un modelo con datos POSTERIORES a los de entrenamiento?
- `arrom3-q13` → **medium** · Regla 34: ¿cómo obtener datos limpios en una tarea de filtrado (spam) sin sesgo de muestreo?
- `arrom3-q14` → **medium** · Regla 36: ¿cómo se evitan los feedback loops con features posicionales?
- `arrom3-q15` → **medium** · Regla 37: ¿en qué tres componentes se divide la medición del training-serving skew?

**`arena-dmls4` — Cambios de distribución, monitoreo y test en producción**  · easy 0 / medium 13 / hard 2

- `ardmls4-q1` → **medium** · ¿Por qué un modelo desplegado se degrada con el tiempo?
- `ardmls4-q2` → **medium** · Define covariate shift con su expresión de probabilidad y un ejemplo.
- `ardmls4-q3` → **medium** · Define label shift y concept drift, distinguiéndolos.
- `ardmls4-q4` → **medium** · ¿Cómo se detecta estadísticamente un distribution shift?
- `ardmls4-q5` → **medium** · ¿Qué métricas hay que monitorear en un modelo en producción cuando no hay labels inmediatos?
- `ardmls4-q6` → **medium** · Diferencia monitoreo de observabilidad.
- `ardmls4-q7` → **medium** · Diferencia el reentrenamiento stateless del stateful (continual learning).
- `ardmls4-q8` → **medium** · ¿Cuál es la pregunta correcta sobre la frecuencia de reentrenamiento?
- `ardmls4-q9` → **medium** · ¿Qué es shadow deployment y por qué es la forma más segura de probar un modelo?
- `ardmls4-q10` → **medium** · ¿Cómo funciona un A/B test de modelos y qué dos cosas hay que hacer bien?
- `ardmls4-q11` → **medium** · ¿Por qué la significancia estadística en un A/B test no es infalible?
- `ardmls4-q12` → **medium** · ¿Qué es un canary release y cómo reduce el riesgo?
- `ardmls4-q13` → **medium** · ¿Qué es el interleaving y en qué tareas se usa?
- `ardmls4-q14` → **hard** · ¿Qué son los bandits y qué ventaja tienen sobre el A/B testing? ¿Y los contextual bandits?
- `ardmls4-q15` → **hard** · Un modelo en producción empieza a fallar. Esboza cómo lo diagnosticarías y cómo validarías el reemplazo.

**`arena-rml1` — Confiabilidad de extremo a extremo: el ciclo de vida del ML y los SLOs**  · easy 2 / medium 13 / hard 0

- `arrml1-q1` → **medium** · ¿Por qué los autores afirman que un sistema de ML 'nunca está realmente terminado'?
- `arrml1-q2` → **easy** · Enumera las etapas del ciclo de vida (el 'ML loop') según el libro.
- `arrml1-q3` → **medium** · ¿Por qué un pipeline de entrenamiento de ML es más difícil de operar de forma fiable que un ETL convencional?
- `arrml1-q4` → **medium** · Lista los fallos más comunes de un pipeline de entrenamiento de ML.
- `arrml1-q5` → **medium** · Define SLO y SLI y da un ejemplo concreto.
- `arrml1-q6` → **medium** · ¿Cómo conviene separar los SLOs de un sistema de ML?
- `arrml1-q7` → **easy** · ¿Cuáles son las 'cuatro señales doradas' (golden signals) y de dónde vienen?
- `arrml1-q8` → **medium** · Distingue las tres categorías de señales de monitoreo: salud del sistema, salud básica del modelo y calidad de…
- `arrml1-q9` → **medium** · ¿Por qué la calidad del modelo es lo más difícil de monitorear?
- `arrml1-q10` → **medium** · 'Los modelos son código': ¿qué implicación tiene para el despliegue?
- `arrml1-q11` → **medium** · En un despliegue progresivo ('launch slowly'), ¿qué dos dimensiones se limitan y por qué?
- `arrml1-q12` → **medium** · ¿Por qué la regla 'release, not refactor' es especialmente aguda en sistemas de ML?
- `arrml1-q13` → **medium** · ¿Qué significa 'aislar los rollouts en la capa de datos' y qué enseña la historia del rollback de pagos?
- `arrml1-q14` → **medium** · Distingue live launch, dark launch y el punto medio de 'fracción de usuarios'.
- `arrml1-q15` → **medium** · 'Most failures will not be ML failures': ¿qué implica para priorizar el trabajo de confiabilidad?

**`arena-sre1` — Fundamentos SRE: riesgo, error budgets y SLOs**  · easy 2 / medium 13 / hard 0

- `arsre1-q1` → **medium** · ¿Por qué Google NO busca construir servicios 100% fiables?
- `arsre1-q2` → **medium** · ¿Por qué el coste de la fiabilidad no crece de forma lineal?
- `arsre1-q3` → **medium** · ¿Cómo mide Google el riesgo/disponibilidad de un servicio y por qué prefiere la tasa de éxito de peticiones al…
- `arsre1-q4` → **medium** · ¿Qué es un error budget y cómo se calcula?
- `arsre1-q5` → **medium** · ¿Qué tensión organizativa resuelve el error budget y cómo?
- `arsre1-q6` → **medium** · ¿Por qué el objetivo de disponibilidad se ve como un mínimo Y un máximo?
- `arsre1-q7` → **medium** · Explica el caso de la caída planificada de Chubby.
- `arsre1-q8` → **easy** · Define SLI y da ejemplos.
- `arsre1-q9` → **easy** · Define SLO y por qué publicarlo es útil.
- `arsre1-q10` → **medium** · Define SLA y cómo distinguirlo de un SLO.
- `arsre1-q11` → **medium** · ¿Por qué conviene elegir pocos SLIs y qué SLIs importan según el tipo de sistema?
- `arsre1-q12` → **medium** · ¿Por qué un SLI casi siempre debe verse como una distribución y no como una media?
- `arsre1-q13` → **medium** · ¿Cómo ayuda el coste a fijar el objetivo de disponibilidad cuando se traduce en ingresos?
- `arsre1-q14` → **medium** · ¿Por qué distintos tipos de fallo importan de forma distinta aunque den el mismo número de errores?
- `arsre1-q15` → **medium** · ¿Por qué la tolerancia al riesgo de un servicio de infraestructura difiere de un producto de consumo?

**`arena-sre2` — Eliminar toil, monitoreo y las cuatro señales doradas**  · easy 5 / medium 10 / hard 0

- `arsre2-q1` → **easy** · Define toil y sus características.
- `arsre2-q2` → **medium** · ¿Qué NO es toil: overhead y grunt work con valor?
- `arsre2-q3` → **medium** · ¿Por qué SRE limita el toil a menos del 50% y qué pasa si no?
- `arsre2-q4` → **easy** · ¿Qué cuenta como 'ingeniería' en SRE?
- `arsre2-q5` → **easy** · ¿Cuáles son las cuatro señales doradas del monitoreo?
- `arsre2-q6` → **medium** · ¿Qué mide la señal de Latencia y por qué hay que separar éxito de error?
- `arsre2-q7` → **easy** · ¿Qué miden las señales de Tráfico y Errores?
- `arsre2-q8` → **medium** · ¿Qué mide la señal de Saturación y por qué importa la cola/latencia como indicador?
- `arsre2-q9` → **medium** · Diferencia black-box monitoring de white-box monitoring.
- `arsre2-q10` → **medium** · En un sistema multicapa, ¿por qué el síntoma de uno es la causa de otro?
- `arsre2-q11` → **medium** · ¿Qué cuatro propiedades debe tener una buena página (alerta que despierta a un humano)?
- `arsre2-q12` → **medium** · ¿Por qué hay que vigilar la cola (tail), no la media, e instrumentar con histogramas?
- `arsre2-q13` → **medium** · ¿Cómo elegir la resolución de las mediciones y por qué importa el coste?
- `arsre2-q14` → **easy** · ¿Qué guía de simplicidad da SRE para el sistema de monitoreo?
- `arsre2-q15` → **medium** · ¿Por qué es mejor alertar por síntomas que por causas?

**`arena-sre3` — Troubleshooting, gestión de incidentes y postmortems sin culpa**  · easy 3 / medium 12 / hard 0

- `arsre3-q1` → **medium** · ¿Cómo describe SRE el proceso de troubleshooting?
- `arsre3-q2` → **medium** · ¿Qué debe contener un buen reporte de problema y por qué abrir un bug por cada incidencia?
- `arsre3-q3` → **medium** · Menciona trampas comunes del troubleshooting inefectivo.
- `arsre3-q4` → **medium** · ¿Qué significa 'caballos, no cebras' y 'correlación no es causa' en el diagnóstico?
- `arsre3-q5` → **medium** · ¿Qué cuatro fallos comunes convierten un incidente en 'no gestionado' (la historia de Mary)?
- `arsre3-q6` → **medium** · ¿En qué se basa el sistema de gestión de incidentes de Google y por qué la separación de responsabilidades da …
- `arsre3-q7` → **easy** · ¿Cuáles son los roles distintos del Incident Command System?
- `arsre3-q8` → **easy** · ¿Qué es un postmortem y cuándo se escribe?
- `arsre3-q9` → **medium** · ¿Qué es un postmortem 'sin culpa' (blameless) y por qué importa?
- `arsre3-q10` → **medium** · Da un ejemplo de redacción 'señalando con el dedo' vs 'sin culpa' para el mismo problema.
- `arsre3-q11` → **medium** · ¿Por qué no se debe estigmatizar a quien produce muchos postmortems?
- `arsre3-q12` → **medium** · ¿Qué prácticas hacen colaborativo el proceso de postmortem?
- `arsre3-q13` → **medium** · ¿Por qué es esencial definir los criterios de postmortem ANTES de que ocurra un incidente?
- `arsre3-q14` → **medium** · ¿Cómo se prueban las hipótesis en el troubleshooting, según las dos vías de SRE?
- `arsre3-q15` → **easy** · ¿Por qué los postmortems son una herramienta esencial para SRE y no solo una formalidad?

**`arena-sre4` — Robustez en producción: releases, simplicidad, sobrecarga y cascada**  · easy 1 / medium 13 / hard 1

- `arsre4-q1` → **easy** · ¿Cuáles son los cuatro principios de la ingeniería de releases en Google?
- `arsre4-q2` → **medium** · ¿Por qué lanzar frecuentemente ('high velocity', push on green) facilita la operación?
- `arsre4-q3` → **medium** · ¿Qué es un build hermético y por qué importa para la fiabilidad?
- `arsre4-q4` → **medium** · ¿Qué es el método de rama + cherry-pick y qué problema evita?
- `arsre4-q5` → **medium** · ¿Por qué 'aburrido' es una virtud en software (the virtue of boring)?
- `arsre4-q6` → **medium** · Distingue complejidad esencial de accidental y qué debe hacer SRE con ellas.
- `arsre4-q7` → **medium** · ¿Por qué 'cada línea de código es un pasivo' y qué es la métrica de 'líneas negativas'?
- `arsre4-q8` → **medium** · ¿Qué son las APIs mínimas y la modularidad como patrones de simplicidad?
- `arsre4-q9` → **medium** · ¿Por qué son mejores los releases simples (en lotes pequeños)?
- `arsre4-q10` → **medium** · ¿Cuál es la causa más común de fallos en cascada y cómo se propaga?
- `arsre4-q11` → **hard** · ¿Qué es el agotamiento de recursos y la 'GC death spiral'?
- `arsre4-q12` → **medium** · ¿Cómo amplifican los reintentos un fallo en cascada y cómo mitigarlo?
- `arsre4-q13` → **medium** · Enumera estrategias para prevenir la sobrecarga de un servidor (en orden de prioridad).
- `arsre4-q14` → **medium** · ¿Qué son el load shedding y la degradación elegante (graceful degradation)?
- `arsre4-q15` → **medium** · ¿Por qué hay que ejercitar regularmente el modo de degradación y mantenerlo simple?

**`arena-rml4` — Respuesta a incidentes en sistemas de ML**  · easy 3 / medium 12 / hard 0

- `arrml4-q1` → **medium** · ¿Cuáles son los tres conceptos básicos de una gestión de incidentes exitosa y qué es un 'incidente no gestiona…
- `arrml4-q2` → **easy** · Enumera las fases de la vida de un incidente.
- `arrml4-q3` → **easy** · Distingue mitigación de resolución.
- `arrml4-q4` → **easy** · ¿Cuáles son los cuatro roles mínimos de respuesta a incidentes (marco tipo FEMA/ICS)?
- `arrml4-q5` → **medium** · ¿Qué aspectos del manejo de un incidente cambian cuando es de ML frente a uno no-ML?
- `arrml4-q6` → **medium** · Explica los tres principios rectores de los incidentes de ML: Public, Fuzzy y Unbounded.
- `arrml4-q7` → **medium** · ¿Por qué las caídas de ML suelen detectarse primero por los usuarios ('Public')?
- `arrml4-q8` → **medium** · ¿Por qué un incidente de ML es 'Fuzzy' en tiempo e impacto?
- `arrml4-q9` → **medium** · En la Historia 1 (búsqueda que no encuentra), ¿cuáles fueron la causa próxima y la causa raíz?
- `arrml4-q10` → **medium** · ¿Cuál es la lección clave de detección de la Historia 1 sobre la señal de calidad?
- `arrml4-q11` → **medium** · ¿Qué acciones de seguimiento (follow-up) salieron de la Historia 1?
- `arrml4-q12` → **medium** · Para preparar incidentes, ¿cuál es el paso más importante del data scientist/modelista, y qué más debe hacer?
- `arrml4-q13` → **medium** · ¿Qué debe preparar el software engineer para que los incidentes vayan mejor?
- `arrml4-q14` → **medium** · ¿Por qué conviene buscar mitigaciones FUERA del sistema de ML, según la Historia 3?
- `arrml4-q15` → **medium** · ¿Qué dice el 'manifiesto del ingeniero ético de guardia' sobre privacidad y ética durante un incidente?

**`arena-obs1` — Arena Observabilidad · ¿Qué es? Monitoreo vs. observabilidad**  · easy 4 / medium 11 / hard 0

- `arobs1-q1` → **easy** · ¿De dónde viene el término 'observabilidad' y cómo se define en teoría de control?
- `arobs1-q2` → **easy** · Define observabilidad para sistemas de software en una frase.
- `arobs1-q3` → **medium** · ¿Cuál es la 'prueba de fuego' para saber si un sistema es observable?
- `arobs1-q4` → **medium** · ¿Qué diferencia clave hay entre lo que detectan el monitoreo y la observabilidad respecto a lo 'conocido'?
- `arobs1-q5` → **medium** · ¿Por qué se dice que el monitoreo tradicional es 'fundamentalmente reactivo'?
- `arobs1-q6` → **medium** · ¿Por qué una métrica es demasiado limitada para ser el bloque base de la observabilidad?
- `arobs1-q7` → **easy** · Define cardinalidad y da ejemplos de campos de alta y baja cardinalidad.
- `arobs1-q8` → **medium** · ¿Por qué importa la alta cardinalidad para depurar?
- `arobs1-q9` → **medium** · ¿Qué es la dimensionalidad y en qué se diferencia de la cardinalidad?
- `arobs1-q10` → **medium** · ¿Qué significa que un evento sea 'ancho' (wide) y por qué conviene?
- `arobs1-q11` → **medium** · ¿Por qué las herramientas basadas en métricas obligan a 'predecir por adelantado'?
- `arobs1-q12` → **medium** · Como regla práctica, ¿cuándo conviene monitoreo y cuándo observabilidad?
- `arobs1-q13` → **medium** · Los autores no son fans del modelo de los 'tres pilares' (métricas, logs, trazas). ¿Por qué?
- `arobs1-q14` → **easy** · ¿Qué es la 'explorabilidad' (explorability) de un sistema?
- `arobs1-q15` → **medium** · ¿Por qué la observabilidad importa especialmente AHORA, con sistemas distribuidos modernos?

**`arena-obs2` — Arena Observabilidad · Eventos, trazas y Core Analysis Loop**  · easy 5 / medium 10 / hard 0

- `arobs2-q1` → **easy** · ¿Qué es un 'evento estructurado' y cómo se construye?
- `arobs2-q2` → **medium** · ¿Por qué las métricas no sirven como bloque de construcción de la observabilidad?
- `arobs2-q3` → **medium** · ¿Cuál es la diferencia entre logs no estructurados y estructurados, y cuál sirve para observabilidad?
- `arobs2-q4` → **medium** · ¿Qué es una 'unidad de trabajo' y por qué define el alcance de un evento?
- `arobs2-q5` → **easy** · ¿Cuántas dimensiones suele tener un evento con instrumentación madura?
- `arobs2-q6` → **easy** · ¿Qué es una traza distribuida?
- `arobs2-q7` → **medium** · ¿Qué es un 'span' y qué relación padre-hijo existe en una traza?
- `arobs2-q8` → **easy** · Nombra los cinco campos imprescindibles para ensamblar un span.
- `arobs2-q9` → **medium** · ¿Cómo se propaga el contexto de traza entre servicios?
- `arobs2-q10` → **easy** · ¿Qué problema resuelve OpenTelemetry?
- `arobs2-q11` → **medium** · ¿Qué significa 'depurar desde primeros principios' y por qué es central en observabilidad?
- `arobs2-q12` → **medium** · ¿Por qué los autores consideran los runbooks 'trabajo en gran parte desperdiciado'?
- `arobs2-q13` → **medium** · Describe los cuatro pasos del Core Analysis Loop.
- `arobs2-q14` → **medium** · ¿Cómo automatiza una herramienta la parte de fuerza bruta del Core Analysis Loop?
- `arobs2-q15` → **medium** · ¿Por qué AIOps no es la bala de plata para depurar, y cuál es el enfoque correcto?

**`arena-obs3` — Arena Observabilidad · SLOs, alertas por síntoma y burn alerts**  · easy 1 / medium 12 / hard 2

- `arobs3-q1` → **medium** · ¿Qué es la fatiga de alertas y con qué concepto del desastre del Challenger se relaciona?
- `arobs3-q2` → **medium** · ¿Qué dos criterios debe cumplir una alerta para considerarse útil?
- `arobs3-q3` → **medium** · ¿Por qué se dice que el 'umbral estático es solo para known-unknowns'?
- `arobs3-q4` → **medium** · ¿Por qué es importante 'desacoplar el qué del por qué' al alertar?
- `arobs3-q5` → **medium** · ¿Deberían las fallas auto-remediadas disparar alertas que despierten a alguien?
- `arobs3-q6` → **medium** · ¿Qué significa que 'la experiencia del usuario es el North Star' del alerting?
- `arobs3-q7` → **easy** · ¿Qué es un SLO (Service-Level Objective)?
- `arobs3-q8` → **medium** · ¿Qué es un SLI y por qué se prefieren los SLI basados en eventos sobre los basados en tiempo?
- `arobs3-q9` → **medium** · Da un ejemplo de un SLI basado en eventos bien definido.
- `arobs3-q10` → **medium** · ¿Qué es el error budget y cómo se calcula?
- `arobs3-q11` → **medium** · ¿Qué pasa (y qué debe hacer el equipo) cuando se agota el error budget?
- `arobs3-q12` → **medium** · ¿Por qué calcular el SLO sobre una ventana DESLIZANTE y no fija de calendario?
- `arobs3-q13` → **medium** · ¿Por qué 30 días es la ventana más pragmática para la mayoría de SLOs?
- `arobs3-q14` → **hard** · Compara los dos modelos para disparar una burn alert por encima del nivel cero.
- `arobs3-q15` → **hard** · En una burn alert predictiva, ¿qué son el lookahead window y el baseline window, y qué relación deben guardar?

**`arena-obs4` — Arena Observabilidad · Escala: almacenamiento, muestreo y madurez**  · easy 1 / medium 12 / hard 2

- `arobs4-q1` → **medium** · ¿Cuáles son los requisitos funcionales del almacén de datos de observabilidad?
- `arobs4-q2` → **medium** · ¿Por qué una TSDB es inadecuada para almacenar eventos de observabilidad?
- `arobs4-q3` → **medium** · ¿Por qué una base NoSQL de propósito general tampoco resuelve el problema?
- `arobs4-q4` → **medium** · ¿Qué ventaja y qué desventaja tiene el almacenamiento por filas (row-based, p.ej. Bigtable) para observabilida…
- `arobs4-q5` → **medium** · ¿Qué gana y qué cuesta el almacenamiento por columnas (column-based) para observabilidad?
- `arobs4-q6` → **medium** · ¿En qué consiste la estrategia híbrida de particionar datos por tiempo en segmentos?
- `arobs4-q7` → **medium** · Dentro de un segmento, ¿cómo se almacena por columna y cómo se reduce el espacio?
- `arobs4-q8` → **medium** · Menciona tres técnicas que hacen el almacén columnar asequible, rápido y durable a escala.
- `arobs4-q9` → **medium** · ¿Qué significa que para observabilidad 'es más importante que el resultado llegue rápido que que sea perfecto'…
- `arobs4-q10` → **medium** · ¿Qué es el muestreo (sampling) y qué conserva que la métrica preagregada no?
- `arobs4-q11` → **medium** · ¿Cuándo NO es efectivo el muestreo de probabilidad constante (1 de cada N)?
- `arobs4-q12` → **hard** · ¿Qué es el muestreo dinámico por contenido/clave y cómo reconstruyes los conteos?
- `arobs4-q13` → **medium** · ¿Qué es el target rate sampling y qué resuelve?
- `arobs4-q14` → **hard** · Diferencia muestreo head-based de tail-based y explica el muestreo consistente.
- `arobs4-q15` → **easy** · ¿Qué cinco capacidades mide el Observability Maturity Model (OMM) y qué naturaleza tiene?

**`arena-htd1` — Arena Deuda Técnica ML · Fundamentos y erosión de fronteras**  · easy 2 / medium 11 / hard 2

- `arhtd1-q1` → **easy** · ¿Qué es la 'deuda técnica' (Cunningham, 1992) y qué se quiere decir con que 'toda deuda debe servirse'?
- `arhtd1-q2` → **medium** · ¿Por qué los sistemas de ML tienen una capacidad ESPECIAL de incurrir deuda técnica?
- `arhtd1-q3` → **medium** · ¿Por qué es difícil imponer fronteras de abstracción fuertes en un sistema de ML?
- `arhtd1-q4` → **medium** · Enuncia el principio CACE y explica el 'entanglement' que lo causa.
- `arhtd1-q5` → **medium** · ¿A qué cosas, además de las señales de entrada, aplica el principio CACE?
- `arhtd1-q6` → **hard** · ¿Cómo ayuda 'aislar modelos y servir ensembles' contra el entanglement, y cuál es su trampa?
- `arhtd1-q7` → **medium** · ¿Qué segunda estrategia de mitigación se propone para el entanglement, además de los ensembles?
- `arhtd1-q8` → **medium** · ¿Qué es una 'correction cascade' y cómo surge?
- `arhtd1-q9` → **medium** · ¿Por qué es peligrosa una correction cascade y cómo se mitiga?
- `arhtd1-q10` → **medium** · ¿Qué son los 'undeclared consumers' y con qué deuda clásica se relacionan?
- `arhtd1-q11` → **medium** · ¿Por qué los undeclared consumers son 'caros en el mejor caso y peligrosos en el peor'?
- `arhtd1-q12` → **medium** · ¿Cómo se previenen los undeclared consumers?
- `arhtd1-q13` → **medium** · ¿Qué quiere decir que la deuda técnica de ML existe a 'nivel de sistema' y no a 'nivel de código'?
- `arhtd1-q14` → **easy** · Según el paper, ¿qué NO pretende aportar y qué sí busca?
- `arhtd1-q15` → **hard** · ¿Por qué confiar en la combinación de un ensemble puede ocultar un entanglement fuerte?

**`arena-htd2` — Arena Deuda Técnica ML · Dependencias de datos y feedback loops**  · easy 0 / medium 13 / hard 2

- `arhtd2-q1` → **medium** · ¿Por qué las dependencias de DATOS cuestan más que las de código?
- `arhtd2-q2` → **medium** · ¿Qué es una dependencia de datos INESTABLE y de qué formas surge?
- `arhtd2-q3` → **hard** · ¿Por qué incluso una 'mejora' a una señal de entrada inestable puede ser peligrosa? Da el ejemplo del paper.
- `arhtd2-q4` → **medium** · ¿Cuál es la mitigación estándar para una dependencia de datos inestable y qué cuesta?
- `arhtd2-q5` → **medium** · ¿Qué es una dependencia de datos INFRAUTILIZADA y por qué importa?
- `arhtd2-q6` → **medium** · Nombra y explica las cuatro formas en que una dependencia infrautilizada se cuela en un modelo.
- `arhtd2-q7` → **medium** · ¿Por qué las features correlacionadas producen 'brittleness' y cómo se detectan las infrautilizadas?
- `arhtd2-q8` → **medium** · ¿Qué papel juega el análisis estático y un sistema de gestión de features en las dependencias de datos?
- `arhtd2-q9` → **hard** · ¿Qué es un 'direct feedback loop' y por qué los bandits no lo resuelven directamente?
- `arhtd2-q10` → **medium** · ¿Cómo se mitiga un direct feedback loop si los bandits no escalan?
- `arhtd2-q11` → **medium** · ¿Qué es un 'hidden feedback loop' y por qué es más difícil que uno directo?
- `arhtd2-q12` → **medium** · Da el ejemplo del paper de un hidden feedback loop entre sistemas completamente disjuntos.
- `arhtd2-q13` → **medium** · ¿Por qué los feedback loops se describen como una forma de 'analysis debt'?
- `arhtd2-q14` → **medium** · ¿En qué se diferencian una dependencia de datos inestable y una infrautilizada?
- `arhtd2-q15` → **medium** · ¿Por qué dejar 'ambos esquemas' (viejo y nuevo) de numeración de productos ilustra el peligro de las dependenc…

**`arena-htd3` — Arena Deuda Técnica ML · Anti-patrones de sistema y configuración**  · easy 1 / medium 14 / hard 0

- `arhtd3-q1` → **easy** · Según la Figura 1 del paper, ¿qué fracción del código de un sistema ML real es realmente aprendizaje/predicció…
- `arhtd3-q2` → **medium** · ¿Qué es el 'glue code' y por qué es costoso?
- `arhtd3-q3` → **medium** · ¿Cuál es la mitigación recomendada para el glue code?
- `arhtd3-q4` → **medium** · ¿Qué es una 'pipeline jungle' y cómo se evita?
- `arhtd3-q5` → **medium** · ¿Cuál es la raíz organizacional común del glue code y las pipeline jungles, y cómo se reduce?
- `arhtd3-q6` → **medium** · ¿Qué son los 'dead experimental codepaths' y por qué se acumulan?
- `arhtd3-q7` → **medium** · ¿Por qué son peligrosos los dead experimental codepaths y qué ejemplo célebre cita el paper?
- `arhtd3-q8` → **medium** · ¿Cómo se mitigan los dead experimental codepaths?
- `arhtd3-q9` → **medium** · ¿Qué es la 'abstraction debt' y qué comparación usa el paper?
- `arhtd3-q10` → **medium** · ¿Qué dice el paper sobre Map-Reduce y el parameter-server como abstracciones para ML?
- `arhtd3-q11` → **medium** · Describe los tres 'common smells' de sistemas ML que identifica el paper.
- `arhtd3-q12` → **medium** · ¿Por qué la 'configuration debt' es un área sorprendente de deuda?
- `arhtd3-q13` → **medium** · Da ejemplos del 'desorden' de configuración que cita el paper.
- `arhtd3-q14` → **medium** · Enuncia los principios de buena configuración según el paper.
- `arhtd3-q15` → **medium** · ¿Por qué usar un paquete genérico puede 'inhibir mejoras' en un sistema ML?

**`arena-htd4` — Arena Deuda Técnica ML · Mundo externo, otras deudas y medición**  · easy 1 / medium 14 / hard 0

- `arhtd4-q1` → **medium** · ¿Por qué la interacción con el mundo externo es una fuente de deuda en sistemas ML?
- `arhtd4-q2` → **medium** · ¿Qué problema causan los 'fixed thresholds in dynamic systems'?
- `arhtd4-q3` → **medium** · ¿Cómo se mitiga el problema de los umbrales fijos en sistemas dinámicos?
- `arhtd4-q4` → **medium** · ¿Por qué los unit tests y los tests end-to-end no bastan para un sistema ML, y qué se necesita?
- `arhtd4-q5` → **medium** · ¿Qué es el 'prediction bias' y por qué es un diagnóstico útil para monitorear?
- `arhtd4-q6` → **medium** · ¿Qué son los 'action limits' y para qué sirven?
- `arhtd4-q7` → **medium** · ¿Qué medidas recomienda el paper respecto a los 'up-stream producers'?
- `arhtd4-q8` → **medium** · ¿Por qué la respuesta al monitoreo debe ser automatizada y en tiempo real?
- `arhtd4-q9` → **medium** · ¿Qué es la 'data testing debt' y por qué se justifica testear los datos?
- `arhtd4-q10` → **easy** · ¿Qué es la 'reproducibility debt'?
- `arhtd4-q11` → **medium** · ¿Qué es la 'process management debt' y qué smell se debe evitar?
- `arhtd4-q12` → **medium** · ¿Qué es la 'cultural debt' y cómo se paga?
- `arhtd4-q13` → **medium** · Enumera las cinco preguntas útiles que el paper propone para evaluar la deuda técnica de un sistema ML.
- `arhtd4-q14` → **medium** · Según las conclusiones, ¿por qué 'moverse rápido' no es evidencia de baja deuda?
- `arhtd4-q15` → **medium** · ¿Qué conclusión central da el paper sobre los trade-offs de complejidad y cómo pagar la deuda?

**`arena-mldp4` — Patrones de reproducibilidad e IA responsable**  · easy 0 / medium 15 / hard 0

- `armldp4-q1` → **medium** · ¿Qué problema resuelve el patrón Transform y cómo?
- `armldp4-q2` → **medium** · ¿Por qué dividir datos con un random sin semilla es problemático y qué propone Repeatable Splitting?
- `armldp4-q3` → **medium** · ¿Qué características debe tener la columna por la que se divide en Repeatable Splitting?
- `armldp4-q4` → **medium** · ¿Qué problema resuelve el patrón Bridged Schema?
- `armldp4-q5` → **medium** · En Bridged Schema, ¿qué es el método estático y por qué se prefiere al probabilístico?
- `armldp4-q6` → **medium** · ¿Qué problema resuelve el patrón Windowed Inference?
- `armldp4-q7` → **medium** · ¿Cómo funciona la solución de Windowed Inference?
- `armldp4-q8` → **medium** · ¿Qué problema resuelve el patrón Workflow Pipeline y cómo?
- `armldp4-q9` → **medium** · ¿Qué es el patrón Model Versioning y qué beneficios da?
- `armldp4-q10` → **medium** · ¿Qué es Continued Model Evaluation y qué dos causas de degradación atiende?
- `armldp4-q11` → **medium** · ¿Qué es el patrón Heuristic Benchmark y para qué sirve?
- `armldp4-q12` → **medium** · ¿Qué problema resuelve el patrón Explainable Predictions?
- `armldp4-q13` → **medium** · ¿Qué es el patrón Fairness Lens y por qué quitar la feature sensible no basta?
- `armldp4-q14` → **medium** · Nombra tres fuentes de sesgo problemático que cita el patrón Fairness Lens.
- `armldp4-q15` → **medium** · ¿Por qué optimizar solo el accuracy global puede ser un problema de equidad?

**`arena-iml1` — Arena Interpretabilidad ML · Conceptos, taxonomía y buenas explicaciones**  · easy 5 / medium 10 / hard 0

- `ariml1-q1` → **easy** · ¿Qué es la 'interpretabilidad' de un modelo y por qué un modelo más interpretable es más fácil de confiar/depu…
- `ariml1-q2` → **easy** · Da tres razones por las que necesitamos interpretabilidad.
- `ariml1-q3` → **easy** · ¿Cuándo NO necesitamos interpretabilidad?
- `ariml1-q4` → **easy** · Distingue interpretabilidad INTRÍNSECA de POST-HOC.
- `ariml1-q5` → **medium** · ¿Qué diferencia a un método ESPECÍFICO del modelo de uno AGNÓSTICO, y cuál es la gran ventaja del agnóstico?
- `ariml1-q6` → **easy** · Diferencia interpretabilidad GLOBAL de LOCAL.
- `ariml1-q7` → **medium** · ¿Qué tipos de RESULTADO puede tener una explicación?
- `ariml1-q8` → **medium** · Explica el ALCANCE de la interpretabilidad: global holístico vs modular vs local.
- `ariml1-q9` → **medium** · ¿Por qué una explicación LOCAL suele ser más fiel y más simple que una global?
- `ariml1-q10` → **medium** · ¿Qué significa que una buena explicación es CONTRASTIVA y por qué importa?
- `ariml1-q11` → **medium** · ¿Qué quiere decir que una explicación debe ser SELECTIVA, y qué es el efecto Rashomon?
- `ariml1-q12` → **medium** · Menciona otras propiedades de una buena explicación además de contrastiva y selectiva.
- `ariml1-q13` → **medium** · ¿Qué propiedades sirven para evaluar los MÉTODOS de interpretabilidad?
- `ariml1-q14` → **medium** · ¿Qué propiedades evalúan una EXPLICACIÓN individual? Distingue accuracy, fidelity y stability.
- `ariml1-q15` → **medium** · ¿Cuáles son los tres niveles de evaluación de interpretabilidad de Doshi-Velez & Kim?

**`arena-iml2` — Arena Interpretabilidad ML · Modelos interpretables (intrínsecos)**  · easy 1 / medium 14 / hard 0

- `ariml2-q1` → **medium** · ¿Qué tres propiedades determinan cuán interpretable es un modelo, y cómo se sitúan regresión lineal, árbol y k…
- `ariml2-q2` → **medium** · En una regresión lineal $\hat y = \beta_0 + \sum \beta_j x_j$, ¿cómo se interpreta el peso $\beta_j$ de una fe…
- `ariml2-q3` → **medium** · ¿Cómo se interpreta el peso de una feature CATEGÓRICA en una regresión lineal?
- `ariml2-q4` → **medium** · ¿Cómo se mide la IMPORTANCIA de una feature dentro de una regresión lineal?
- `ariml2-q5` → **easy** · ¿Qué mide R² y por qué se prefiere el R² ajustado?
- `ariml2-q6` → **medium** · ¿Por qué la multicolinealidad (features correlacionadas) dificulta interpretar los pesos lineales?
- `ariml2-q7` → **medium** · ¿Qué diferencia hay entre un WEIGHT PLOT y un EFFECT PLOT en regresión lineal?
- `ariml2-q8` → **medium** · ¿Por qué en regresión logística NO se interpreta el peso como un cambio lineal sobre la probabilidad?
- `ariml2-q9` → **medium** · Interpreta el ODDS RATIO de una feature en regresión logística.
- `ariml2-q10` → **medium** · ¿Qué generaliza un GLM respecto a la regresión lineal?
- `ariml2-q11` → **medium** · ¿Qué es un GAM y qué problema de la regresión lineal resuelve?
- `ariml2-q12` → **medium** · ¿Cómo se interpreta una predicción de un árbol de decisión y qué capta de forma natural?
- `ariml2-q13` → **medium** · ¿Cómo se mide la importancia de una feature en un árbol y cuál es la principal limitación de los árboles?
- `ariml2-q14` → **medium** · En reglas de decisión IF-THEN, ¿qué son el soporte y la accuracy de una regla? ¿Qué es OneR?
- `ariml2-q15` → **medium** · ¿Cómo funciona RuleFit y qué combina?

**`arena-iml3` — Arena Interpretabilidad ML · Métodos agnósticos: efectos e importancia**  · easy 0 / medium 12 / hard 3

- `ariml3-q1` → **medium** · ¿Qué es un método de interpretabilidad AGNÓSTICO y cuál es su ventaja central?
- `ariml3-q2` → **medium** · ¿Qué muestra un Partial Dependence Plot (PDP) y cómo se computa?
- `ariml3-q3` → **medium** · ¿Cuál es el supuesto peligroso del PDP y qué problema causa?
- `ariml3-q4` → **medium** · ¿Por qué un PDP plano puede ser engañoso?
- `ariml3-q5` → **medium** · ¿Qué es un gráfico ICE y cómo se relaciona con el PDP?
- `ariml3-q6` → **medium** · En un gráfico ICE, ¿qué indica que las líneas NO sean paralelas, y qué son las c-ICE?
- `ariml3-q7` → **hard** · Explica cómo se computa un ALE plot.
- `ariml3-q8` → **hard** · ¿Por qué ALE es mejor que el PDP cuando hay features correlacionadas? ¿Qué son los M-plots?
- `ariml3-q9` → **medium** · ¿Cómo se interpreta el eje y de un ALE plot (que está centrado en 0)?
- `ariml3-q10` → **medium** · ¿Qué mide la H-statistic de Friedman y cuál es su rango?
- `ariml3-q11` → **hard** · ¿Cómo se construye la H-statistic y cuál es su principal coste?
- `ariml3-q12` → **medium** · Explica la importancia por permutación.
- `ariml3-q13` → **medium** · ¿Conviene calcular la importancia por permutación en datos de TRAIN o de TEST? ¿Por qué? ¿Y por qué repetirla?
- `ariml3-q14` → **medium** · ¿Qué problema introducen las features correlacionadas en la importancia por permutación?
- `ariml3-q15` → **medium** · ¿Qué es un modelo SUSTITUTO global y cómo se valida su calidad?

**`arena-iml4` — Arena Interpretabilidad ML · LIME, Shapley/SHAP y ejemplos**  · easy 0 / medium 13 / hard 2

- `ariml4-q1` → **medium** · Describe los cuatro pasos de LIME para explicar una predicción.
- `ariml4-q2` → **medium** · ¿Cómo aplica LIME a texto e imágenes?
- `ariml4-q3` → **medium** · ¿Cuáles son las principales debilidades de LIME?
- `ariml4-q4` → **medium** · ¿Qué es el valor de Shapley de una feature?
- `ariml4-q5` → **hard** · ¿Qué cuatro axiomas cumple ÚNICAMENTE el valor de Shapley?
- `ariml4-q6` → **medium** · ¿Qué garantiza la propiedad de EFICIENCIA en una explicación con valores de Shapley?
- `ariml4-q7` → **medium** · ¿Cuál es el coste de calcular valores de Shapley exactos y qué NO entregan?
- `ariml4-q8` → **medium** · ¿Qué aporta SHAP y qué diferencia hay entre KernelSHAP y TreeSHAP?
- `ariml4-q9` → **medium** · ¿Cómo da SHAP importancia GLOBAL y qué ventaja tiene sobre la importancia por permutación?
- `ariml4-q10` → **medium** · Compara SHAP con LIME.
- `ariml4-q11` → **medium** · ¿Qué es una explicación CONTRAFACTUAL y por qué es valiosa? Menciona los criterios de Wachter.
- `ariml4-q12` → **medium** · ¿Qué es un ejemplo ADVERSARIAL y en qué se parece a un contrafactual?
- `ariml4-q13` → **medium** · ¿Qué son los PROTOTIPOS y las CRÍTICAS (MMD-critic)?
- `ariml4-q14` → **hard** · ¿Qué son las INSTANCIAS INFLUYENTES y cómo se identifican (deletion diagnostics vs influence functions)?
- `ariml4-q15` → **medium** · ¿Qué son los ANCHORS y en qué complementan a LIME?

### Causalidad y Health AI / RWE (`causal-health`)

**`arena-h15` — Arena Inferencia Causal (Pearl) · La escalera de la causalidad**  · easy 7 / medium 8 / hard 0

- `arh15-q1` → **easy** · ¿Cuáles son los tres peldaños de la ESCALERA DE LA CAUSALIDAD de Pearl?
- `arh15-q2` → **medium** · ¿Qué tipo de preguntas vive en cada peldaño y por qué el machine learning actual está en el primero?
- `arh15-q3` → **medium** · ¿Por qué Pearl insiste en que 'los datos no contienen información causal' por sí solos?
- `arh15-q4` → **easy** · ¿Qué es el mini-Turing test que propone Pearl?
- `arh15-q5` → **easy** · ¿Qué papel jugaron Galton y Pearson en la historia de la causalidad según el libro?
- `arh15-q6` → **easy** · ¿Quién fue Sewall Wright y por qué es importante en la génesis de la inferencia causal?
- `arh15-q7` → **medium** · ¿Por qué 'correlación no implica causación', en términos de la escalera?
- `arh15-q8` → **medium** · ¿Qué quiere decir que un nivel superior de la escalera puede responder preguntas de los inferiores pero no al …
- `arh15-q9` → **medium** · ¿Por qué Pearl dice que el deep learning, pese a sus éxitos, sigue en el peldaño 1?
- `arh15-q10` → **easy** · ¿Qué significa 'mind over data' frente a 'data over mind'?
- `arh15-q11` → **medium** · Da un ejemplo de cada peldaño con la misma variable (p. ej. un medicamento).
- `arh15-q12` → **medium** · ¿Por qué la aleatorización (RCT) es tan valiosa en el lenguaje de la escalera/do-operator?
- `arh15-q13` → **easy** · ¿Qué relación tienen los diagramas causales con los path diagrams de Wright?
- `arh15-q14` → **medium** · Según Pearl, ¿qué le falta a una IA que solo aprende de datos para tener inteligencia 'humana'?
- `arh15-q15` → **easy** · ¿Por qué Pearl considera la causalidad una 'revolución' y no un detalle técnico?

**`arena-h16` — Arena Inferencia Causal (Pearl) · Diagramas, junciones y paradojas**  · easy 2 / medium 10 / hard 3

- `arh16-q1` → **easy** · ¿Qué es un diagrama causal (DAG) y qué codifica?
- `arh16-q2` → **medium** · Describe las tres JUNCIONES básicas de un diagrama causal.
- `arh16-q3` → **hard** · ¿Cómo cambia el flujo de asociación al CONDICIONAR cada tipo de junción?
- `arh16-q4` → **medium** · En el lenguaje de junciones, ¿qué es un confundidor y por qué ajustarlo elimina el sesgo?
- `arh16-q5` → **medium** · ¿Por qué NO se debe ajustar por un collider, con un ejemplo?
- `arh16-q6` → **medium** · ¿Qué es el sesgo de Berkson?
- `arh16-q7` → **hard** · ¿Cómo explica el razonamiento causal/collider el problema de Monty Hall?
- `arh16-q8` → **medium** · ¿En qué consiste la paradoja de Simpson?
- `arh16-q9` → **medium** · ¿Cómo RESUELVE el razonamiento causal la paradoja de Simpson?
- `arh16-q10` → **medium** · ¿Por qué la paradoja de Simpson demuestra la tesis central del libro?
- `arh16-q11` → **medium** · ¿Qué relación hay entre las redes bayesianas y los diagramas causales?
- `arh16-q12` → **medium** · ¿Qué significa que las flechas AUSENTES en un DAG son los supuestos más fuertes?
- `arh16-q13` → **hard** · ¿Por qué un mediador y un confundidor, aun pareciendo iguales en los datos, exigen tratamientos opuestos?
- `arh16-q14` → **medium** · ¿Qué es 'desconfundir' (deconfounding) en el marco de Pearl?
- `arh16-q15` → **easy** · ¿Por qué Pearl dice que los diagramas hacen 'transparentes los supuestos'?

**`arena-h1` — Arena Health AI · DAGs y adjustment sets**  · easy 0 / medium 2 / hard 2

- `arh1-q1` → **medium** · Define confounder, mediator y collider con una frase cada uno. Luego dibuja un DAG simple de 4 nodos (X, Y, y …
- `arh1-q2` → **hard** · Paradoja de Berkson: en un hospital, observas que los pacientes con enfermedad A parecen tener MENOS probabili…
- `arh1-q3` → **hard** · En un DAG con X→Y, C→X, C→Y (C es confounder), A→X, A→C (A causa X vía C y directamente). ¿Qué conjunto mínimo…
- `arh1-q4` → **medium** · Un colega propone agregar la variable 'adherencia al tratamiento' al modelo de regresión para 'controlar su ef…

**`arena-h17` — Arena Inferencia Causal (Pearl) · do-operator, back-door, front-door y do-calculus**  · easy 1 / medium 13 / hard 1

- `arh17-q1` → **medium** · ¿Qué distingue P(Y|X) de P(Y|do(X))?
- `arh17-q2` → **medium** · ¿Qué le hace el do-operator al diagrama causal?
- `arh17-q3` → **medium** · ¿En qué consiste la IDENTIFICACIÓN de un efecto causal?
- `arh17-q4` → **medium** · Describe la fórmula de ajuste por la PUERTA TRASERA (back-door adjustment).
- `arh17-q5` → **hard** · ¿Qué es el criterio de la PUERTA DELANTERA (front-door) y cuándo se usa?
- `arh17-q6` → **medium** · Da el ejemplo clásico de Pearl para el criterio de la puerta delantera.
- `arh17-q7` → **medium** · ¿Qué es el do-calculus y qué garantiza?
- `arh17-q8` → **easy** · ¿Por qué el do-calculus se describe como un 'mapa universal' de Mount Intervention?
- `arh17-q9` → **medium** · ¿Cómo encaja la estimación por VARIABLE INSTRUMENTAL en este marco?
- `arh17-q10` → **medium** · ¿Cómo ilustra el caso del Dr. John Snow (cólera) un instrumento/intervención natural?
- `arh17-q11` → **medium** · ¿Por qué ajustar por MÁS variables no siempre mejora una estimación causal?
- `arh17-q12` → **medium** · ¿Qué ventaja tiene el front-door sobre el back-door en la práctica?
- `arh17-q13` → **medium** · ¿Qué significa que un efecto causal NO sea identificable?
- `arh17-q14` → **medium** · ¿En qué se parecen el do-operator y la aleatorización de un RCT?
- `arh17-q15` → **medium** · Resume la 'conquista de Mount Intervention': las rutas para estimar P(Y|do(x)).

**`arena-h3` — Arena Inferencia Causal · Contrafactuales, experimentos e identificación**  · easy 1 / medium 12 / hard 2

- `arh3-q1` → **medium** · ¿Qué son los resultados POTENCIALES (contrafactuales) y qué es el efecto causal INDIVIDUAL?
- `arh3-q2` → **medium** · Define el efecto causal PROMEDIO en una población y por qué es identificable cuando el individual no lo es.
- `arh3-q3` → **medium** · Explica por qué 'la asociación no es causación' en términos contrafactuales.
- `arh3-q4` → **medium** · ¿Qué garantiza un experimento aleatorizado y cómo se llama esa propiedad?
- `arh3-q5` → **medium** · Enuncia las TRES condiciones para identificar un efecto causal en un estudio observacional.
- `arh3-q6` → **medium** · ¿Qué es la condición de POSITIVIDAD y qué la viola?
- `arh3-q7` → **medium** · ¿Qué es la condición de CONSISTENCIA y por qué exige 'intervenciones bien definidas'?
- `arh3-q8` → **easy** · Define las medidas de efecto causal: diferencia de riesgos, razón de riesgos y razón de momios (odds ratio).
- `arh3-q9` → **hard** · ¿Qué es la MODIFICACIÓN DE EFECTO y por qué depende de la escala?
- `arh3-q10` → **hard** · ¿En qué se diferencia la INTERACCIÓN de la modificación de efecto?
- `arh3-q11` → **medium** · ¿Qué es el riesgo de confundimiento en estudios observacionales frente a los aleatorizados?
- `arh3-q12` → **medium** · ¿Por qué el efecto causal promedio puede ser nulo aunque haya efectos en individuos?
- `arh3-q13` → **medium** · ¿Qué significa estimar un efecto causal por ESTANDARIZACIÓN, a nivel intuitivo?
- `arh3-q14` → **medium** · ¿Qué es el IP weighting a nivel intuitivo y qué problema resuelve?
- `arh3-q15` → **medium** · ¿Por qué a veces se dice que la inferencia causal es 'un problema de datos faltantes'?

**`arena-h19` — Arena Inferencia Causal (Mixtape) · Resultados potenciales y sesgo de selección**  · easy 0 / medium 14 / hard 1

- `arh19-q1` → **medium** · En el modelo de resultados potenciales, ¿qué son Y¹ e Y⁰ y por qué el efecto individual es inobservable?
- `arh19-q2` → **medium** · Define ATE, ATT y ATU y di cuándo difieren.
- `arh19-q3` → **medium** · ¿Qué es el supuesto SUTVA y qué lo viola?
- `arh19-q4` → **hard** · Descompón la diferencia simple de medias $E[Y\mid D=1]-E[Y\mid D=0]$ en sus componentes.
- `arh19-q5` → **medium** · ¿Qué es el SESGO DE SELECCIÓN en esta descomposición?
- `arh19-q6` → **medium** · ¿Por qué la ALEATORIZACIÓN resuelve el problema de identificación?
- `arh19-q7` → **medium** · ¿Qué significa el supuesto de INDEPENDENCIA y cómo se relaciona con la 'asignación como-si-aleatoria'?
- `arh19-q8` → **medium** · ¿Cuál es la diferencia entre el estimando ATE y el ATT, y por qué a veces solo se puede estimar el ATT?
- `arh19-q9` → **medium** · ¿Qué relación tiene el modelo de resultados potenciales con los DAGs/inferencia causal de Pearl?
- `arh19-q10` → **medium** · ¿Por qué 'no hay causación sin manipulación' es relevante para definir bien un efecto?
- `arh19-q11` → **medium** · Da un ejemplo donde la comparación naïve engaña por sesgo de selección.
- `arh19-q12` → **medium** · ¿Qué es la 'switching equation' y qué problema ilustra?
- `arh19-q13` → **medium** · ¿Por qué el efecto promedio del tratamiento puede ser positivo aunque para muchos individuos sea negativo?
- `arh19-q14` → **medium** · ¿Qué papel juega la covariable X en lograr independencia condicional?
- `arh19-q15` → **medium** · ¿Por qué los economistas distinguen entre tratamiento 'endógeno' y 'exógeno'?

**`arena-h4` — Arena Inferencia Causal · Confundimiento, selección y sesgo de medición**  · easy 0 / medium 11 / hard 4

- `arh4-q1` → **medium** · ¿Qué es el CONFUNDIMIENTO en términos estructurales y qué es un camino trasero (backdoor)?
- `arh4-q2` → **medium** · Enuncia el CRITERIO DE LA PUERTA TRASERA (backdoor) para elegir el conjunto de ajuste.
- `arh4-q3` → **hard** · Explica las reglas de d-separación: ¿cuándo un camino está bloqueado?
- `arh4-q4` → **medium** · ¿Por qué NO se debe ajustar por un MEDIADOR si se busca el efecto TOTAL?
- `arh4-q5` → **medium** · ¿Qué es el SESGO DE SELECCIÓN en términos estructurales y en qué se diferencia del confundimiento?
- `arh4-q6` → **medium** · ¿Cómo genera la CENSURA / pérdida de seguimiento un sesgo de selección y cómo se corrige?
- `arh4-q7` → **medium** · ¿Qué es el sesgo de medición y qué es la misclasificación NO DIFERENCIAL vs DIFERENCIAL?
- `arh4-q8` → **medium** · ¿Qué problema causa un CONFUNDIDOR medido con error?
- `arh4-q9` → **medium** · Distingue IDENTIFICACIÓN de ESTIMACIÓN en inferencia causal.
- `arh4-q10` → **medium** · ¿Qué es la 'maldición de la dimensionalidad' al ajustar por muchos confundidores y cómo se enfrenta?
- `arh4-q11` → **medium** · ¿Cómo distingue un DAG el confundimiento del sesgo de selección al mirar los caminos?
- `arh4-q12` → **medium** · ¿Qué es un 'noncausal diagram' y por qué los diagramas de medición incluyen flechas no causales?
- `arh4-q13` → **hard** · ¿Por qué condicionar (ajustar) por una variable NO siempre reduce el sesgo?
- `arh4-q14` → **hard** · ¿Qué es el sesgo en M (M-bias) y por qué advierte contra ajustar 'por si acaso'?
- `arh4-q15` → **hard** · ¿Qué son los Single-World Intervention Graphs (SWIGs) y para qué sirven?

**`arena-h18` — Arena Inferencia Causal (Pearl) · Contrafactuales y mediación**  · easy 1 / medium 9 / hard 5

- `arh18-q1` → **medium** · ¿Qué es un contrafactual y por qué está en el peldaño más alto de la escalera?
- `arh18-q2` → **medium** · ¿Por qué los contrafactuales no se pueden obtener solo con datos ni solo con experimentos?
- `arh18-q3` → **medium** · ¿Qué es un Modelo Causal Estructural (SCM) y qué papel juegan los términos de error U?
- `arh18-q4` → **hard** · Describe el algoritmo de TRES PASOS para computar un contrafactual.
- `arh18-q5` → **medium** · ¿Qué relación hay entre los contrafactuales de Pearl y los potential outcomes de Neyman-Rubin?
- `arh18-q6` → **medium** · ¿En qué consiste el análisis de MEDIACIÓN?
- `arh18-q7` → **hard** · ¿Por qué el método clásico de Baron-Kenny (producto de coeficientes) puede fallar?
- `arh18-q8` → **hard** · ¿Qué son los efectos directo e indirecto NATURALES (NDE/NIE)?
- `arh18-q9` → **medium** · ¿Por qué identificar efectos de mediación requiere MÁS supuestos que estimar el efecto total?
- `arh18-q10` → **hard** · Distingue la PROBABILIDAD DE NECESIDAD (PN) de la PROBABILIDAD DE SUFICIENCIA (PS).
- `arh18-q11` → **hard** · ¿Cómo se aplican PN/PS a una pregunta legal de responsabilidad?
- `arh18-q12` → **medium** · ¿Por qué los contrafactuales son esenciales para la EXPLICACIÓN y la atribución?
- `arh18-q13` → **medium** · ¿Cómo enmarca Pearl la atribución del cambio climático en términos causales?
- `arh18-q14` → **easy** · ¿Qué quiere decir Pearl con 'la virtud de ver tus supuestos'?
- `arh18-q15` → **medium** · Según Pearl, ¿por qué los contrafactuales son clave para una IA verdaderamente inteligente?

**`arena-h5` — Arena Inferencia Causal · Modelos: IP weighting, g-fórmula, PS, IV**  · easy 0 / medium 10 / hard 5

- `arh5-q1` → **medium** · ¿Por qué hace falta MODELAR en inferencia causal (Parte II) si en la Parte I se estimaba sin modelos?
- `arh5-q2` → **medium** · Explica el IP weighting: qué se modela y qué es la pseudo-población.
- `arh5-q3` → **medium** · ¿Qué es un Modelo Estructural Marginal (MSM)?
- `arh5-q4` → **hard** · ¿Qué son los PESOS ESTABILIZADOS y por qué se prefieren a los no estabilizados?
- `arh5-q5` → **medium** · Explica la ESTANDARIZACIÓN / g-fórmula y su relación con el IP weighting.
- `arh5-q6` → **medium** · ¿Qué es el PROPENSITY SCORE y por qué es un 'balancing score'?
- `arh5-q7` → **medium** · ¿Cómo se usa el propensity score en la práctica (4 formas)?
- `arh5-q8` → **hard** · ¿Qué es un estimador DOBLEMENTE ROBUSTO y por qué es valioso?
- `arh5-q9` → **hard** · ¿Cómo combina la inferencia causal moderna el MACHINE LEARNING con la doble robustez?
- `arh5-q10` → **medium** · ¿Por qué no basta con poner muchas covariables en una regresión del outcome para 'controlar confundimiento'?
- `arh5-q11` → **medium** · Enuncia las TRES condiciones que debe cumplir una VARIABLE INSTRUMENTAL.
- `arh5-q12` → **hard** · ¿Cuál es el estimando IV usual y por qué las 3 condiciones no bastan para un efecto puntual?
- `arh5-q13` → **hard** · Bajo MONOTONICIDAD, ¿qué estima la variable instrumental (LATE) y qué limita su interpretación?
- `arh5-q14` → **medium** · ¿Qué es un INSTRUMENTO DÉBIL y por qué es peligroso?
- `arh5-q15` → **medium** · ¿Qué variables conviene y NO conviene incluir al seleccionar covariables para inferencia causal?

**`arena-h20` — Arena Inferencia Causal (Mixtape) · Matching, subclasificación y propensity score**  · easy 0 / medium 14 / hard 1

- `arh20-q1` → **medium** · ¿Qué es el supuesto de INDEPENDENCIA CONDICIONAL (CIA) y por qué es central para matching/regresión?
- `arh20-q2` → **medium** · ¿Por qué el CIA es 'fuerte' y no verificable?
- `arh20-q3` → **medium** · ¿Cómo funciona la SUBCLASIFICACIÓN para estimar un efecto causal?
- `arh20-q4` → **medium** · ¿Qué es la MALDICIÓN DE LA DIMENSIONALIDAD en matching exacto?
- `arh20-q5` → **medium** · ¿Qué resume el PROPENSITY SCORE y cómo ayuda con la dimensionalidad?
- `arh20-q6` → **medium** · ¿Qué es la ponderación por probabilidad inversa (IPW) en este contexto?
- `arh20-q7` → **medium** · ¿Qué es el SOPORTE COMÚN (common support / overlap) y por qué importa?
- `arh20-q8` → **hard** · ¿Por qué el matching de vecino más cercano introduce sesgo y cómo se corrige?
- `arh20-q9` → **medium** · ¿En qué se diferencian conceptualmente el MATCHING y la REGRESIÓN?
- `arh20-q10` → **medium** · ¿Qué ilustra el caso Lalonde / Dehejia-Wahba sobre matching?
- `arh20-q11` → **medium** · ¿Cómo se verifica que el matching/propensity score logró BALANCE?
- `arh20-q12` → **medium** · ¿Qué es el COARSENED EXACT MATCHING (CEM)?
- `arh20-q13` → **medium** · ¿Por qué matching, subclasificación, IPW y regresión comparten la misma debilidad fundamental?
- `arh20-q14` → **medium** · ¿Cuándo es preferible matching sobre una regresión lineal estándar?
- `arh20-q15` → **medium** · ¿Qué estima típicamente el matching: ATE o ATT?

**`arena-h21` — Arena Inferencia Causal (Mixtape) · Variables instrumentales y RDD**  · easy 1 / medium 10 / hard 4

- `arh21-q1` → **medium** · ¿Cómo se estima un efecto por variable instrumental usando 2SLS?
- `arh21-q2` → **medium** · Enuncia las tres condiciones que debe cumplir un instrumento válido.
- `arh21-q3` → **medium** · ¿Qué es un INSTRUMENTO DÉBIL y por qué es peligroso?
- `arh21-q4` → **hard** · Bajo MONOTONICIDAD, ¿qué estima el IV (LATE) y a quién se refiere?
- `arh21-q5` → **medium** · ¿Qué es la FORMA REDUCIDA y por qué es un diagnóstico útil en IV?
- `arh21-q6` → **medium** · ¿Qué explota la REGRESIÓN DISCONTINUA (RDD) para identificar un efecto causal?
- `arh21-q7` → **medium** · Diferencia la RDD NÍTIDA (sharp) de la DIFUSA (fuzzy).
- `arh21-q8` → **hard** · ¿Qué es el test de densidad de McCrary y qué amenaza detecta?
- `arh21-q9` → **medium** · ¿Qué supuestos clave debe cumplir una RDD válida además de la no manipulación?
- `arh21-q10` → **medium** · ¿Por qué la elección del BANDWIDTH implica un trade-off sesgo-varianza en RDD?
- `arh21-q11` → **medium** · ¿Por qué se prefieren POLINOMIOS LOCALES de bajo grado a polinomios globales de alto grado en RDD?
- `arh21-q12` → **easy** · Da un ejemplo clásico de RDD del libro.
- `arh21-q13` → **hard** · ¿Por qué tanto la RDD fuzzy como el IV estiman un LATE y no un ATE?
- `arh21-q14` → **medium** · ¿Qué ventaja tiene la RDD frente a matching/regresión en cuanto a supuestos?
- `arh21-q15` → **hard** · ¿Qué chequeos de robustez/falsación se hacen en una RDD creíble?

**`arena-h22` — Arena Inferencia Causal (Mixtape) · Panel/efectos fijos, DiD y control sintético**  · easy 2 / medium 10 / hard 3

- `arh22-q1` → **medium** · ¿Qué controlan los EFECTOS FIJOS de unidad en datos de panel?
- `arh22-q2` → **medium** · ¿Qué NO pueden resolver los efectos fijos y qué supuesto exigen?
- `arh22-q3` → **medium** · ¿Cómo estima un efecto la estrategia de DIFERENCIAS EN DIFERENCIAS (DiD)?
- `arh22-q4` → **medium** · ¿Cuál es el supuesto de identificación de DiD?
- `arh22-q5` → **medium** · ¿Cómo se apoya empíricamente el supuesto de tendencias paralelas?
- `arh22-q6` → **hard** · ¿Qué problema tiene la regresión TWFE con adopción ESCALONADA (staggered) y efectos heterogéneos?
- `arh22-q7` → **easy** · Da un ejemplo clásico de DiD y su lógica de control.
- `arh22-q8` → **medium** · ¿Qué controla DiD que un simple antes-después o un simple tratado-vs-control NO controlan?
- `arh22-q9` → **medium** · ¿Qué es el CONTROL SINTÉTICO y para qué se usa?
- `arh22-q10` → **medium** · ¿Qué ventajas tiene el control sintético sobre un DiD estándar?
- `arh22-q11` → **hard** · ¿Cómo se hace inferencia en el control sintético si solo hay una unidad tratada?
- `arh22-q12` → **easy** · Da un ejemplo clásico de control sintético.
- `arh22-q13` → **medium** · ¿Cuándo conviene usar panel/efectos fijos frente a un corte transversal con matching?
- `arh22-q14` → **hard** · Resume cómo cada diseño cuasi-experimental relaja la dependencia del CIA.
- `arh22-q15` → **medium** · ¿Por qué ningún método cuasi-experimental es universalmente superior?

**`arena-h2` — Arena Health AI · Target trial emulation e immortal time bias**  · easy 0 / medium 3 / hard 1

- `arh2-q1` → **medium** · ¿Qué es el 'tiempo cero' de un estudio y por qué debe coincidir con el momento de elegibilidad y asignación? ¿…
- `arh2-q2` → **hard** · Un paper concluye que los pacientes que tomaron un medicamento antihipertensivo por más de 2 años tienen 30% m…
- `arh2-q3` → **medium** · Enuncia los 7 componentes del protocolo de un target trial, usando como ejemplo el estudio de una app de medit…
- `arh2-q4` → **medium** · Ves un análisis donde el grupo 'tratado con inmunoterapia' se define como 'pacientes que recibieron al menos 3…

**`arena-h6` — Arena Inferencia Causal · Longitudinal, supervivencia y target trial**  · easy 0 / medium 9 / hard 6

- `arh6-q1` → **hard** · En análisis de supervivencia causal, ¿por qué el HAZARD RATIO es problemático como medida de efecto?
- `arh6-q2` → **medium** · ¿Qué medidas de efecto se prefieren en supervivencia causal en lugar del hazard ratio?
- `arh6-q3` → **hard** · ¿Por qué la CENSURA se trata como un 'tratamiento tiempo-variable' y cómo se ajusta?
- `arh6-q4` → **hard** · ¿Qué es la INTERCAMBIABILIDAD SECUENCIAL y por qué se necesita con tratamientos tiempo-variables?
- `arh6-q5` → **hard** · ¿Qué es el FEEDBACK TRATAMIENTO-CONFUNDIDOR y por qué hace fallar a los métodos tradicionales?
- `arh6-q6` → **medium** · Si los métodos tradicionales 'no se pueden arreglar' ante el feedback, ¿cuál es la solución?
- `arh6-q7` → **hard** · ¿Qué hace el IP weighting en el caso de tratamientos tiempo-variables (MSM longitudinal)?
- `arh6-q8` → **medium** · Diferencia el efecto de INTENCIÓN DE TRATAR (ITT) del efecto PER-PROTOCOL.
- `arh6-q9` → **medium** · ¿Por qué un análisis PER-PROTOCOL ingenuo (comparar adherentes vs no adherentes) está sesgado?
- `arh6-q10` → **medium** · ¿Qué es el TARGET TRIAL y qué se gana al especificarlo explícitamente?
- `arh6-q11` → **medium** · ¿Qué es el IMMORTAL TIME BIAS y cómo lo evita la emulación del target trial?
- `arh6-q12` → **medium** · ¿Qué es el SESGO DE USUARIO PREVALENTE y cómo se corrige con un new-user design?
- `arh6-q13` → **medium** · ¿Por qué se recomienda un COMPARADOR ACTIVO en la emulación de un target trial?
- `arh6-q14` → **hard** · ¿Cómo se estima el efecto PER-PROTOCOL al emular un target trial de una estrategia SOSTENIDA?
- `arh6-q15` → **medium** · ¿Por qué la emulación de target trials se ha vuelto central en la evidencia de mundo real (RWE) y la salud-IA?

**`arena-h7` — Arena Análisis de Supervivencia · Fundamentos, Kaplan-Meier y log-rank**  · easy 4 / medium 11 / hard 0

- `arh7-q1` → **medium** · ¿Qué caracteriza a los datos de SUPERVIVENCIA (tiempo-hasta-evento) y por qué necesitan métodos propios?
- `arh7-q2` → **easy** · Define la función de SUPERVIVENCIA S(t) y la función de HAZARD h(t).
- `arh7-q3` → **medium** · ¿Qué relación matemática conecta S(t), h(t) y el hazard acumulado H(t)?
- `arh7-q4` → **easy** · ¿Qué es la CENSURA y cuáles son sus tipos?
- `arh7-q5` → **medium** · ¿Qué es el supuesto de censura NO INFORMATIVA y por qué importa?
- `arh7-q6` → **medium** · Explica cómo se construye el estimador de KAPLAN-MEIER de S(t).
- `arh7-q7` → **medium** · ¿Por qué la curva de Kaplan-Meier es escalonada y qué papel juega la censura en ella?
- `arh7-q8` → **medium** · ¿Cómo se obtiene la MEDIANA de supervivencia de una curva KM y por qué a veces la media no se reporta?
- `arh7-q9` → **medium** · ¿Qué compara la prueba de LOG-RANK y cuál es su hipótesis nula?
- `arh7-q10` → **medium** · ¿Cómo se construye el estadístico de log-rank?
- `arh7-q11` → **medium** · ¿Qué variantes del log-rank existen y en qué se diferencian?
- `arh7-q12` → **medium** · ¿Por qué NO se debe usar una regresión logística o lineal en vez de métodos de supervivencia?
- `arh7-q13` → **easy** · ¿Qué significa que un sujeto esté 'en riesgo' (risk set) en un tiempo dado?
- `arh7-q14` → **easy** · ¿Qué información se necesita por individuo para un análisis de supervivencia básico?
- `arh7-q15` → **medium** · ¿Qué describe un hazard CONSTANTE, CRECIENTE y DECRECIENTE en términos prácticos?

**`arena-h8` — Arena Análisis de Supervivencia · Modelo de Cox y supuesto PH**  · easy 1 / medium 11 / hard 3

- `arh8-q1` → **medium** · Escribe el modelo de Cox de hazards proporcionales e interpreta sus componentes.
- `arh8-q2` → **medium** · ¿Por qué el modelo de Cox se llama SEMIPARAMÉTRICO y por qué es tan popular?
- `arh8-q3` → **medium** · ¿Cómo se interpreta el HAZARD RATIO en un modelo de Cox?
- `arh8-q4` → **hard** · ¿Qué es la VEROSIMILITUD PARCIAL y por qué es clave para el Cox?
- `arh8-q5` → **easy** · ¿Cuál es el supuesto central del modelo de Cox?
- `arh8-q6` → **medium** · Describe el método GRÁFICO para evaluar el supuesto PH con curvas log-log.
- `arh8-q7` → **hard** · ¿Cómo se evalúa PH con una PRUEBA DE BONDAD DE AJUSTE (residuos de Schoenfeld)?
- `arh8-q8` → **hard** · ¿Cómo se evalúa PH usando una VARIABLE DEPENDIENTE DEL TIEMPO?
- `arh8-q9` → **medium** · Si se VIOLA el supuesto de hazards proporcionales, ¿qué opciones hay?
- `arh8-q10` → **medium** · ¿Qué es el COX ESTRATIFICADO y qué limitación tiene?
- `arh8-q11` → **medium** · En el Cox estratificado, ¿qué diferencia hay entre el modelo de NO INTERACCIÓN y el de INTERACCIÓN?
- `arh8-q12` → **medium** · ¿Cómo se obtienen CURVAS DE SUPERVIVENCIA AJUSTADAS a partir de un modelo de Cox?
- `arh8-q13` → **medium** · ¿Por qué a veces se prefiere el HR del Cox frente al resultado del log-rank?
- `arh8-q14` → **medium** · ¿Qué significa un HR cercano a 1 con un intervalo de confianza amplio?
- `arh8-q15` → **medium** · ¿Cómo se prueba la significancia global y de coeficientes en un modelo de Cox?

**`arena-h9` — Arena Análisis de Supervivencia · Cox extendido y modelos paramétricos/AFT**  · easy 0 / medium 10 / hard 5

- `arh9-q1` → **medium** · ¿Qué es una covariable DEPENDIENTE DEL TIEMPO y por qué requiere extender el Cox?
- `arh9-q2` → **medium** · Escribe el modelo de Cox EXTENDIDO y sus dos usos principales.
- `arh9-q3` → **medium** · ¿Por qué con covariables tiempo-dependientes el hazard ratio ya no es constante?
- `arh9-q4` → **hard** · ¿Qué precaución hay que tener al definir covariables tiempo-dependientes (anticipación/inmortalidad)?
- `arh9-q5` → **medium** · ¿Qué asumen los modelos PARAMÉTRICOS de supervivencia y en qué se diferencian del Cox?
- `arh9-q6` → **hard** · Compara los hazards de los modelos EXPONENCIAL, WEIBULL y LOG-LOGÍSTICO.
- `arh9-q7` → **medium** · ¿Qué es el marco de ACCELERATED FAILURE TIME (AFT) y cómo se interpreta?
- `arh9-q8` → **hard** · ¿Qué tiene de especial la distribución WEIBULL respecto a PH y AFT?
- `arh9-q9` → **medium** · ¿Cuándo conviene un modelo PARAMÉTRICO frente al Cox?
- `arh9-q10` → **medium** · ¿Cómo se elige y valida un modelo paramétrico?
- `arh9-q11` → **hard** · ¿Cómo se construye una variable tiempo-dependiente para un evento que ocurre en un momento del seguimiento (p.…
- `arh9-q12` → **medium** · ¿Qué relación hay entre el coeficiente AFT y el factor de aceleración?
- `arh9-q13` → **hard** · ¿Por qué un hazard ratio y un factor de aceleración pueden apuntar en 'direcciones' opuestas numéricamente per…
- `arh9-q14` → **medium** · ¿Qué ventaja práctica tiene poder EXTRAPOLAR de un modelo paramétrico?
- `arh9-q15` → **medium** · ¿Cómo se decide entre un Cox extendido (tiempo-dependiente) y un Cox estratificado ante una violación de PH?

**`arena-h10` — Arena Análisis de Supervivencia · Eventos recurrentes y riesgos competitivos**  · easy 0 / medium 8 / hard 7

- `arh10-q1` → **medium** · ¿Qué son los EVENTOS RECURRENTES y qué problema plantean para el análisis estándar?
- `arh10-q2` → **hard** · Describe el enfoque de PROCESO DE CONTEO (Andersen-Gill) para eventos recurrentes.
- `arh10-q3` → **hard** · ¿Qué distingue a los modelos CONDICIONALES (PWP) y MARGINALES (WLW) en eventos recurrentes?
- `arh10-q4` → **medium** · ¿Por qué es indispensable la VARIANZA ROBUSTA en eventos recurrentes?
- `arh10-q5` → **medium** · ¿Qué son los RIESGOS COMPETITIVOS?
- `arh10-q6` → **medium** · ¿Qué es el HAZARD ESPECÍFICO DE CAUSA y cómo se estima de forma estándar?
- `arh10-q7` → **hard** · ¿Por qué (1 − Kaplan-Meier) SOBRESTIMA la incidencia acumulada cuando hay riesgos competitivos?
- `arh10-q8` → **medium** · ¿Qué es la FUNCIÓN/CURVA DE INCIDENCIA ACUMULADA (CIF/CIC) y por qué es la medida correcta?
- `arh10-q9` → **hard** · ¿Qué modela el método de FINE-GRAY y en qué se diferencia del Cox de causa específica?
- `arh10-q10` → **hard** · ¿Cuándo usar el hazard ESPECÍFICO DE CAUSA y cuándo el de SUBDISTRIBUCIÓN (Fine-Gray)?
- `arh10-q11` → **hard** · ¿Qué es la CURVA DE PROBABILIDAD CONDICIONAL (CPC) derivada de la CIF?
- `arh10-q12` → **medium** · ¿Por qué tratar un evento competidor simplemente como 'censura' puede ser engañoso?
- `arh10-q13` → **medium** · ¿Cómo se compara la incidencia acumulada de un evento entre grupos con riesgos competitivos?
- `arh10-q14` → **hard** · En eventos recurrentes, ¿cómo elegir entre el enfoque de Andersen-Gill, PWP y WLW?
- `arh10-q15` → **medium** · Resume la diferencia conceptual entre CENSURA y RIESGO COMPETITIVO.

**`arena-h11` — Arena OHDSI · Comunidad, datos observacionales y OMOP CDM**  · easy 8 / medium 7 / hard 0

- `arh11-q1` → **easy** · ¿Qué es OHDSI y qué problema resuelve?
- `arh11-q2` → **easy** · ¿Qué tipos de datos observacionales de salud usa OHDSI y en qué se diferencian?
- `arh11-q3` → **easy** · ¿Cuáles son los TRES casos de uso analíticos de OHDSI?
- `arh11-q4` → **easy** · ¿Qué es el OMOP Common Data Model y qué estandariza?
- `arh11-q5` → **easy** · Nombra las principales tablas clínicas del OMOP CDM.
- `arh11-q6` → **medium** · ¿Por qué es importante la tabla OBSERVATION_PERIOD?
- `arh11-q7` → **medium** · ¿Qué significa que el CDM permite 'escribir el análisis una vez y correrlo en cualquier base'?
- `arh11-q8` → **easy** · ¿Por qué la filosofía de CIENCIA ABIERTA es central en OHDSI?
- `arh11-q9` → **medium** · ¿Qué diferencia hay entre la estandarización SINTÁCTICA y la SEMÁNTICA en OMOP?
- `arh11-q10` → **medium** · ¿Qué son las tablas de ERA (CONDITION_ERA, DRUG_ERA) y para qué sirven?
- `arh11-q11` → **medium** · ¿Por qué los datos observacionales se recolectaron para fines distintos a la investigación y qué implica?
- `arh11-q12` → **easy** · ¿Qué es ATLAS y qué es HADES en el ecosistema OHDSI?
- `arh11-q13` → **medium** · ¿Qué ventaja da que todo evento clínico tenga un CONCEPT_ID estándar?
- `arh11-q14` → **medium** · ¿En qué se diferencia la evidencia observacional de OHDSI de un ensayo clínico aleatorizado?
- `arh11-q15` → **easy** · ¿Qué papel juega EUNOMIA en aprender OHDSI?

**`arena-h12` — Arena OHDSI · Vocabularios, ETL y calidad de datos**  · easy 3 / medium 12 / hard 0

- `arh12-q1` → **easy** · ¿Qué son los Vocabularios Estandarizados de OMOP?
- `arh12-q2` → **medium** · ¿Cuál es la diferencia entre un concepto ESTÁNDAR y uno FUENTE (no estándar)?
- `arh12-q3` → **medium** · ¿Qué es un DOMINIO (domain) en los vocabularios y por qué importa?
- `arh12-q4` → **medium** · ¿Qué es la tabla CONCEPT_ANCESTOR y para qué sirve en las definiciones de cohortes?
- `arh12-q5` → **medium** · ¿En qué consiste el proceso de ETL hacia el CDM?
- `arh12-q6` → **easy** · ¿Qué hacen WhiteRabbit, Rabbit-in-a-Hat y Usagi?
- `arh12-q7` → **medium** · ¿Por qué el ETL nunca es perfecto y qué implica?
- `arh12-q8` → **medium** · Describe el marco de KAHN para la calidad de datos.
- `arh12-q9` → **easy** · ¿Qué hacen ACHILLES y el Data Quality Dashboard (DQD)?
- `arh12-q10` → **medium** · ¿Por qué la calidad de DATOS es condición necesaria para la calidad de la EVIDENCIA?
- `arh12-q11` → **medium** · ¿Qué diferencia hay entre VERIFICATION y VALIDATION en calidad de datos (Kahn)?
- `arh12-q12` → **medium** · Da ejemplos de un problema de CONFORMANCE, uno de COMPLETENESS y uno de PLAUSIBILITY.
- `arh12-q13` → **medium** · ¿Por qué mapear a conceptos estándar (en vez de usar los códigos fuente) habilita los estudios en red?
- `arh12-q14` → **medium** · ¿Qué es un CONCEPT SET y cómo se usa?
- `arh12-q15` → **medium** · ¿Por qué es importante distinguir 'dato ausente porque no ocurrió' de 'dato ausente porque no se observó'?

**`arena-h13` — Arena OHDSI · Analítica estandarizada: cohortes, caracterización, estimación, predicción**  · easy 4 / medium 11 / hard 0

- `arh13-q1` → **easy** · ¿Cómo define OHDSI una COHORTE?
- `arh13-q2` → **easy** · ¿Cuáles son los tres componentes de una definición de cohorte?
- `arh13-q3` → **medium** · ¿Qué diferencia hay entre una definición de cohorte BASADA EN REGLAS y una PROBABILÍSTICA?
- `arh13-q4` → **medium** · ¿Qué es un FENOTIPO y por qué hay que validarlo?
- `arh13-q5` → **medium** · ¿Qué es la CARACTERIZACIÓN y qué niveles tiene?
- `arh13-q6` → **easy** · ¿Qué son los TREATMENT PATHWAYS?
- `arh13-q7` → **medium** · ¿Qué es la ESTIMACIÓN A NIVEL DE POBLACIÓN y qué dos familias de diseño usa OHDSI?
- `arh13-q8` → **medium** · ¿Qué ventaja tienen los diseños AUTOCONTROLADOS (p. ej. SCCS, case-crossover)?
- `arh13-q9` → **medium** · ¿Qué son los propensity scores 'a gran escala' en el cohort method de OHDSI?
- `arh13-q10` → **medium** · ¿Qué es la PREDICCIÓN A NIVEL DE PACIENTE (PLP) y en qué se diferencia de la estimación?
- `arh13-q11` → **medium** · ¿Cómo se especifica un problema de PLP en el marco estandarizado?
- `arh13-q12` → **medium** · ¿Cómo se evalúa un modelo de predicción a nivel de paciente?
- `arh13-q13` → **medium** · ¿Por qué se usan MUCHAS covariables (miles) tanto en estimación como en predicción en OHDSI?
- `arh13-q14` → **easy** · ¿Qué herramientas de OHDSI se usan para cada caso de uso analítico?
- `arh13-q15` → **medium** · ¿Por qué una buena variable PREDICTIVA no implica un factor CAUSAL (y al revés)?

**`arena-h14` — Arena OHDSI · Calidad de la evidencia, validez de método y estudios en red**  · easy 3 / medium 10 / hard 2

- `arh14-q1` → **easy** · ¿Cuáles son los cuatro tipos de validez que componen la CALIDAD DE LA EVIDENCIA en OHDSI?
- `arh14-q2` → **medium** · ¿Qué es la VALIDEZ CLÍNICA y cómo se evalúa un fenotipo?
- `arh14-q3` → **easy** · ¿Qué es PheValuator?
- `arh14-q4` → **easy** · ¿Qué es la VALIDEZ DE SOFTWARE y por qué importa en OHDSI?
- `arh14-q5` → **medium** · ¿Qué es la VALIDEZ DE MÉTODO y cuál es su herramienta central?
- `arh14-q6` → **medium** · ¿Qué es un CONTROL NEGATIVO y cómo se interpreta su resultado?
- `arh14-q7` → **medium** · ¿Qué son los CONTROLES POSITIVOS y para qué sirven?
- `arh14-q8` → **hard** · ¿Qué es la CALIBRACIÓN EMPÍRICA de p-valores e intervalos de confianza?
- `arh14-q9` → **medium** · ¿Por qué los p-valores e intervalos clásicos son insuficientes en estudios observacionales?
- `arh14-q10` → **medium** · ¿Qué DIAGNÓSTICOS de estudio, además de los controles negativos, se usan en estimación?
- `arh14-q11` → **medium** · ¿Qué es la OHDSI Methods Benchmark?
- `arh14-q12` → **medium** · ¿Qué es un ESTUDIO EN RED de OHDSI y qué problema de privacidad resuelve?
- `arh14-q13` → **medium** · ¿Qué hace creíble y reproducible a un estudio en red de OHDSI frente a un estudio observacional 'a medida'?
- `arh14-q14` → **medium** · ¿Qué es la generación de evidencia 'a gran escala' (p. ej. LEGEND) y por qué importa?
- `arh14-q15` → **hard** · Resume la cadena completa de calidad que propone OHDSI para confiar en una estimación causal observacional.

### Conductual y comunicación bajo presión (`conductual`)

**`arena-c1` — Arena Conductual · Conflicto, colaboración y comunicación (STAR)**  · easy 2 / medium 9 / hard 4

- `arc1-q1` → **medium** · Cuéntame de una vez que tuviste un conflicto con un compañero de equipo. ¿Cómo lo resolviste?
- `arc1-q2` → **hard** · Háblame de una ocasión en que estuviste en desacuerdo con tu manager. ¿Qué hiciste?
- `arc1-q3` → **medium** · Describe una situación en la que tuviste que explicar un concepto técnico complejo a una audiencia no técnica.
- `arc1-q4` → **medium** · Cuéntame de una vez que tuviste que trabajar con alguien difícil o con un estilo muy distinto al tuyo.
- `arc1-q5` → **medium** · Háblame de una vez que tuviste que convencer a otros de adoptar tu idea o enfoque.
- `arc1-q6` → **medium** · Describe una vez que recibiste feedback crítico sobre tu comunicación o tu trabajo en equipo.
- `arc1-q7` → **medium** · Cuéntame de un proyecto que requirió colaborar con equipos de otras áreas (ingeniería, producto, negocio).
- `arc1-q8` → **hard** · Háblame de una vez que un stakeholder pidió algo que considerabas una mala idea o inviable.
- `arc1-q9` → **medium** · Describe una situación en la que tu comunicación evitó (o causó) un malentendido importante.
- `arc1-q10` → **easy** · Cuéntame de una vez que ayudaste a un compañero con dificultades o mentorizaste a alguien junior.
- `arc1-q11` → **hard** · Háblame de una vez que tuviste que dar feedback difícil a un compañero o reporte.
- `arc1-q12` → **medium** · Describe cómo manejaste una situación con expectativas poco claras o instrucciones ambiguas de un cliente/jefe…
- `arc1-q13` → **medium** · Cuéntame de una vez que tuviste que comunicar malas noticias (un retraso, un problema) a tu equipo o jefe.
- `arc1-q14` → **hard** · Háblame de una decisión de equipo con la que no estabas de acuerdo pero tuviste que apoyar.
- `arc1-q15` → **easy** · Describe una vez que tuviste que colaborar en remoto o con un equipo en otra zona horaria/cultura.

**`arena-c2` — Arena Conductual · Fracaso, errores, ambigüedad y feedback (STAR)**  · easy 2 / medium 10 / hard 3

- `arc2-q1` → **medium** · Háblame de un proyecto que fracasó. ¿Qué pasó y qué aprendiste?
- `arc2-q2` → **hard** · Cuéntame del mayor error que has cometido en el trabajo.
- `arc2-q3` → **medium** · Describe una vez que recibiste una crítica dura sobre tu trabajo. ¿Cómo reaccionaste?
- `arc2-q4` → **medium** · Háblame de una vez que tuviste que trabajar con un alto grado de ambigüedad o sin un camino claro.
- `arc2-q5` → **medium** · Cuéntame de una vez que no cumpliste un plazo. ¿Qué pasó?
- `arc2-q6` → **medium** · Describe una decisión que tomaste y que, en retrospectiva, harías diferente.
- `arc2-q7` → **hard** · Háblame de una vez que tu análisis o modelo resultó estar equivocado.
- `arc2-q8` → **medium** · Cuéntame de una vez que te sentiste abrumado por la carga de trabajo o el estrés. ¿Cómo lo manejaste?
- `arc2-q9` → **medium** · Describe un riesgo que tomaste que no salió como esperabas.
- `arc2-q10` → **easy** · Háblame de una vez que tuviste que aprender una herramienta o tema nuevo muy rápido.
- `arc2-q11` → **medium** · Cuéntame de una vez que tuviste que abandonar un enfoque en el que ya habías invertido tiempo.
- `arc2-q12` → **hard** · Describe una vez en que cometiste un error que afectó a otros (compañeros, clientes, usuarios).
- `arc2-q13` → **medium** · Háblame de un feedback de desempeño (review) que te sorprendió.
- `arc2-q14` → **medium** · Cuéntame de una vez que tuviste éxito a pesar de un obstáculo importante.
- `arc2-q15` → **easy** · Describe una vez que tuviste que decir 'no sé' o admitir que no tenías la respuesta.

**`arena-c3` — Arena Conductual · Liderazgo, iniciativa, impacto y priorización (STAR)**  · easy 1 / medium 9 / hard 5

- `arc3-q1` → **medium** · Cuéntame de una vez que lideraste un proyecto o iniciativa.
- `arc3-q2` → **medium** · Háblame de una vez que tomaste la iniciativa para resolver un problema que nadie te pidió resolver.
- `arc3-q3` → **medium** · Describe cómo priorizaste cuando tenías múltiples tareas/proyectos compitiendo por tu tiempo.
- `arc3-q4` → **medium** · Cuéntame de una vez que fuiste más allá de lo que tu rol exigía.
- `arc3-q5` → **hard** · Háblame de una decisión difícil que tuviste que tomar con información incompleta.
- `arc3-q6` → **medium** · Describe una vez que motivaste o alineaste a un equipo hacia un objetivo común.
- `arc3-q7` → **hard** · Cuéntame de una vez que tuviste que tomar una decisión impopular.
- `arc3-q8` → **medium** · Háblame de una vez que identificaste una oportunidad de mejora en un proceso y la implementaste.
- `arc3-q9` → **easy** · Describe tu mayor logro profesional.
- `arc3-q10` → **medium** · Cuéntame de una vez que tuviste que equilibrar la calidad técnica con un plazo ajustado.
- `arc3-q11` → **hard** · Háblame de una vez que tuviste que influir en una decisión sin tener autoridad formal.
- `arc3-q12` → **hard** · Describe una vez que tuviste que gestionar prioridades en conflicto entre distintos stakeholders.
- `arc3-q13` → **medium** · Cuéntame de un objetivo ambicioso que te fijaste y cómo lo lograste.
- `arc3-q14` → **hard** · Háblame de una vez que defendiste al usuario/cliente o a la calidad del producto frente a presiones internas.
- `arc3-q15` → **medium** · Describe una vez que tuviste que delegar o confiar una tarea importante a otra persona.

**`arena-c4` — Arena Conductual · Data science aplicada, stakeholders y carrera (STAR)**  · easy 4 / medium 6 / hard 5

- `arc4-q1` → **medium** · Cuéntame de un proyecto de data science del que estés orgulloso, de principio a fin.
- `arc4-q2` → **hard** · Háblame de una vez que tuviste que comunicar un resultado negativo o nulo a stakeholders.
- `arc4-q3` → **hard** · Describe una vez que un modelo o análisis funcionó en desarrollo pero falló en producción/realidad.
- `arc4-q4` → **medium** · Cuéntame de una vez que tuviste que trabajar con datos sucios, incompletos o poco fiables.
- `arc4-q5` → **hard** · Háblame de una vez que un stakeholder no entendía o no confiaba en tu análisis.
- `arc4-q6` → **medium** · Describe cómo decidiste qué métrica usar o cómo definiste el éxito de un proyecto de datos.
- `arc4-q7` → **hard** · Cuéntame de una vez que enfrentaste una consideración ética o de privacidad en un proyecto de datos.
- `arc4-q8` → **easy** · ¿Por qué quieres trabajar en data science (o en este puesto/empresa)?
- `arc4-q9` → **easy** · Cuéntame de ti / guíame por tu trayectoria.
- `arc4-q10` → **medium** · Háblame de una vez que el alcance de un proyecto cambió a mitad de camino.
- `arc4-q11` → **hard** · Describe una vez que tu recomendación basada en datos fue ignorada o no se implementó.
- `arc4-q12` → **medium** · Cuéntame de una vez que tuviste que elegir entre un modelo simple e interpretable y uno complejo más preciso.
- `arc4-q13` → **medium** · Háblame de una vez que tuviste que estimar algo con datos muy limitados (un problema de Fermi/back-of-envelope…
- `arc4-q14` → **easy** · Describe cómo te mantienes actualizado y cómo aprendes nuevas técnicas o herramientas.
- `arc4-q15` → **easy** · ¿Dónde te ves en 3-5 años / cuáles son tus metas profesionales?
