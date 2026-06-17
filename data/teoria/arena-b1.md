# Fundamentos de probabilidad y conteo

## De qué trata esta lección (y qué sabrás hacer al final)

Toda la probabilidad nace de una pregunta sencilla: *"¿de cuántas maneras puede pasar esto?"*. Si sabes contar las maneras, sabes calcular probabilidades. Por eso esta lección empieza por el **conteo** (combinatoria) y solo después construye la probabilidad encima.

Al terminar podrás: (1) contar configuraciones sin enumerarlas a mano, (2) traducir "¿qué tan probable es?" a un cociente de conteos, (3) usar las dos herramientas que más atajan problemas —**linealidad de la esperanza** y **LOTUS**— y (4) actualizar una creencia con datos nuevos vía **Bayes**. No supongo nada previo: cada idea se construye desde un ejemplo concreto antes de su fórmula.

---

## Idea raíz: probabilidad como "casos favorables entre casos posibles"

Imagina que tiras un dado justo. Hay 6 resultados posibles, todos igual de plausibles. ¿Probabilidad de sacar par? Hay 3 favorables ($2,4,6$) de 6 posibles, así que $3/6 = 1/2$.

Esa es la definición clásica: cuando todos los resultados son **igualmente probables**,

$$P(\text{evento}) = \frac{\text{número de casos favorables}}{\text{número de casos posibles}}.$$

El numerador y el denominador son **conteos**. Toda la dificultad se traslada a contar bien. De ahí que la combinatoria sea el cimiento: no es un tema aparte, es *cómo* se calcula una probabilidad.

> **Predicción antes de seguir:** ¿esta definición sirve si los resultados NO son igualmente probables (un dado cargado)? Respuesta: **no directamente**. Si las caras no son simétricas, contar no basta: necesitas un peso por resultado. La fórmula de cociente asume simetría; cuando se rompe, se generaliza a $P(A)=\sum_{\omega\in A}P(\omega)$. Tenlo presente: el conteo simple es el caso bonito.

---

## Reglas del conteo

### La regla de la multiplicación (la madre de todas)

Si una tarea se hace en etapas y las elecciones de cada etapa no dependen de las anteriores, **multiplicas** las opciones.

Ejemplo mínimo: un menú con 3 entradas y 4 platos fuertes da $3 \times 4 = 12$ comidas distintas. ¿Por qué multiplicar y no sumar? Porque por **cada** entrada puedes elegir **cualquiera** de los 4 platos: el 4 se repite 3 veces. Sumar ($3+4$) contaría "elijo entrada *o* plato", no "entrada *y* plato".

En general, con $k$ etapas y $n_1, n_2, \ldots, n_k$ opciones,

$$\text{total} = n_1 \cdot n_2 \cdots n_k.$$

### Permutaciones: cuando el orden importa

¿De cuántas formas puedes ordenar 3 libros distintos en un estante? Primer lugar: 3 candidatos. Una vez puesto, segundo lugar: quedan 2. Tercero: queda 1. Por la regla de la multiplicación, $3\cdot 2\cdot 1 = 6$. Eso es $3!$ ("3 factorial").

**Permutar $n$ objetos distintos: $n!$ formas.** El factorial es "cuenta cuántas maneras hay de ordenar en fila".

Si solo colocas $k$ de los $n$ (un podio de $k=3$ entre $n=8$ atletas): $8\cdot 7\cdot 6$. Eso es $\dfrac{8!}{5!}$, porque el $5!$ cancela la cola que no usamos:

$$P(n,k) = \frac{n!}{(n-k)!} \quad (\text{orden importa}).$$

### Combinaciones: cuando el orden NO importa

Ahora elige un **comité** de 3 personas entre 8. Aquí "Ana, Beto, Carla" es el mismo comité que "Carla, Ana, Beto" — el orden no significa nada. Tomamos las $P(8,3)$ listas ordenadas y dividimos por las $3!$ reordenaciones que producen el mismo comité:

$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!} \quad (\text{orden no importa}).$$

Se lee "$n$ en $k$" o "coeficiente binomial". La intuición clave —**dividir por las repeticiones que no debías contar**— reaparece en toda la combinatoria.

### Permutaciones con repetición (anagramas)

¿Cuántas "palabras" salen de reordenar las letras de **STATISTICS**? Son 10 letras, pero hay repetidas: S×3, T×3, I×2, A×1, C×1. Si fueran todas distintas serían $10!$. Pero intercambiar las tres S entre sí no produce una palabra nueva: hay que dividir por $3!$ por las S, otro $3!$ por las T y $2!$ por las I.

$$\frac{10!}{3!\,3!\,2!\,1!\,1!} = 50400.$$

En general, $n$ objetos con multiplicidades $n_1,\ldots,n_m$:

$$\frac{n!}{n_1!\,n_2!\cdots n_m!} \quad (\text{coeficiente multinomial}).$$

Misma idea de siempre: cuenta como si todo fuera distinto y **divide por las simetrías** que no querías contar.

---

## Principio de inclusión-exclusión

Si quieres contar la **unión** de eventos que se solapan, sumar sus tamaños cuenta dos veces lo compartido. Lo arreglas restando los solapes:

$$|A\cup B| = |A| + |B| - |A\cap B|.$$

Analogía: dos círculos que se intersecan; al sumar áreas, la lente del medio entra dos veces, así que la restas una. Para tres eventos hay que restar los tres solapes de a pares y volver a sumar el centro (que restaste de más):

$$|A\cup B\cup C| = |A|+|B|+|C| - |A\cap B| - |A\cap C| - |B\cap C| + |A\cap B\cap C|.$$

Regla mnemónica: **suma** órdenes impares, **resta** órdenes pares (suma de a 1, resta de a 2, suma de a 3, …).

Ejemplo concreto: enteros del 1 al 60 divisibles por 2 **o** 3. Por 2: $\lfloor 60/2\rfloor = 30$. Por 3: $\lfloor 60/3\rfloor = 20$. Por 6 (ambos): $\lfloor 60/6\rfloor = 10$. Unión: $30+20-10 = 40$.

---

## LOTUS: la esperanza de una función sin recalcular su distribución

Antes de LOTUS, fija qué es la **esperanza** (valor esperado): el promedio de una variable aleatoria ponderado por sus probabilidades. Si $X$ vale $x$ con probabilidad $P(X=x)$, entonces $E[X]=\sum_x x\,P(X=x)$. Es el "centro de gravedad" de la distribución.

Ahora la pregunta práctica: quieres $E[g(X)]$ —la esperanza de una **función** de $X$, p. ej. $E[X^2]$—. El camino ingenuo es hallar la distribución de $Y=g(X)$ y promediar. LOTUS ("ley del estadístico inconsciente") dice que no hace falta: pondera $g(x)$ con la distribución que **ya tienes**, la de $X$.

$$E[g(X)] = \sum_x g(x)\,P(X=x) \quad(\text{discreta}), \qquad E[g(X)] = \int g(x)\,f_X(x)\,dx \quad(\text{continua}).$$

Aquí $f_X$ es la **densidad** de $X$ (el análogo continuo de $P(X=x)$). El nombre del teorema es un guiño: lo aplicas "inconscientemente" sin pasar por la distribución de $g(X)$.

Ejemplo — $X\sim\text{Poisson}(\lambda)$, quieres $E[X^2]$. Truco estándar: $E[X^2]=E[X(X-1)]+E[X]$. Para Poisson, $E[X(X-1)]=\lambda^2$ y $E[X]=\lambda$, así que $E[X^2]=\lambda^2+\lambda$.

---

## Linealidad de la esperanza: el atajo más poderoso

Esta es la herramienta que más entrevistas resuelve, y su superpotencia es contraintuitiva. Dice:

$$E[aX + bY + c] = a\,E[X] + b\,E[Y] + c,$$

**aunque $X$ e $Y$ estén correlacionadas**. No necesitas independencia. Puedes partir una suma horrible en pedacitos triviales, sacar la esperanza de cada uno por separado y sumarlas.

La táctica se llama **variables indicadoras**: defines $X_i=1$ si ocurre el evento $i$ y $X_i=0$ si no. Entonces $E[X_i]=1\cdot P(\text{ocurre})+0\cdot P(\text{no})=P(\text{ocurre})$. La esperanza de un indicador *es* la probabilidad del evento. Sumando indicadores cuentas "cuántos ocurren en promedio".

Aplicación canónica — **sombreros**: $n$ personas dejan su sombrero y se los devuelven al azar. ¿Cuántas recuperan el suyo en promedio? Sea $X_i=1$ si la persona $i$ recupera el suyo. Por simetría $P(X_i=1)=1/n$, así que $E[X_i]=1/n$. El total es $X=\sum_i X_i$ y

$$E[X] = \sum_{i=1}^n E[X_i] = n\cdot\frac1n = 1.$$

En promedio **exactamente una** persona recupera su sombrero, para cualquier $n$: dos personas o un millón.

> **Predicción antes de seguir:** los $X_i$ no son independientes (si $n-1$ personas tienen su sombrero, la última también, forzosamente). ¿Eso rompe el cálculo? Respuesta: **no**. La linealidad de la esperanza ignora por completo la dependencia entre los sumandos. Por eso es tan potente: convierte un problema enredado (la permutación entera tiene $n!$ casos y dependencias feas) en una suma de piezas triviales.

---

## Esperanza y varianza de las distribuciones básicas

Antes de la tabla, dos palabras sobre **varianza**: mide cuánto se dispersa $X$ alrededor de su media, $\text{Var}[X]=E[(X-E[X])^2]$. Varianza grande = resultados muy regados; varianza 0 = constante. Estas distribuciones son el alfabeto del cluster quant; conviene reconocerlas de memoria, pero entendiendo de dónde sale cada número.

| Distribución | Qué modela | $E[X]$ | $\text{Var}[X]$ |
|-------------|------------|--------|--------|
| Bernoulli$(p)$ | un ensayo: éxito/fracaso | $p$ | $p(1-p)$ |
| Binomial$(n,p)$ | éxitos en $n$ ensayos | $np$ | $np(1-p)$ |
| Geométrica$(p)$ | ensayos hasta el 1.er éxito | $1/p$ | $(1-p)/p^2$ |
| Poisson$(\lambda)$ | conteos raros en un intervalo | $\lambda$ | $\lambda$ |
| Uniforme$\{1,\ldots,n\}$ | dado de $n$ caras | $(n+1)/2$ | $(n^2-1)/12$ |
| Uniforme$[0,1]$ | punto al azar en $[0,1]$ | $1/2$ | $1/12$ |

Mira la coherencia: una Binomial es $n$ Bernoullis sumadas, y en efecto su media $np$ y su varianza $np(1-p)$ son $n$ veces las de una Bernoulli (la varianza suma porque los ensayos son independientes). La Geométrica con $p$ pequeño tiene media $1/p$ grande: si el éxito es raro, esperas muchos intentos. Reconocer "qué modela" cada una es media batalla.

---

## Probabilidad condicional, ley total y Bayes

### Condicionar = reducir el universo

$P(A\mid B)$ ("probabilidad de $A$ dado $B$") es la probabilidad de $A$ una vez que **sabes** que ocurrió $B$. Saber $B$ achica el espacio de posibilidades a solo los casos con $B$:

$$P(A\mid B) = \frac{P(A\cap B)}{P(B)}.$$

Ejemplo: en una baraja, $P(\text{rey})=4/52$. Pero si ya sé que la carta es figura ($B=$ {J,Q,K}, 12 cartas), entonces $P(\text{rey}\mid\text{figura})=4/12=1/3$. Condicionar reescaló el denominador.

### Ley de la probabilidad total: divide y vencerás

A veces $P(B)$ es difícil de calcular de golpe pero fácil si separas el mundo en casos. Si $A_1,\ldots,A_k$ son una **partición** (casos disjuntos que cubren todo),

$$P(B) = \sum_i P(B\mid A_i)\,P(A_i).$$

Calculas $B$ "por rebanadas" y las recombinas con su peso. Ejemplo: probabilidad de dar positivo en una prueba $=P(+\mid\text{enfermo})P(\text{enfermo})+P(+\mid\text{sano})P(\text{sano})$.

### Bayes: dar vuelta el condicional

Aquí está la joya. A menudo conoces $P(B\mid A)$ pero quieres $P(A\mid B)$ —el condicional **al revés**—. Bayes los conecta:

$$P(A\mid B) = \frac{P(B\mid A)\,P(A)}{P(B)}.$$

Con nombres: $P(A)$ es el **prior** (creencia antes del dato), $P(B\mid A)$ la **verosimilitud** (qué tan compatible es el dato con $A$), y $P(A\mid B)$ el **posterior** (creencia actualizada). El denominador $P(B)$ se calcula con la ley total y solo normaliza.

**La trampa clásica:** confundir $P(+\mid\text{enfermo})$ con $P(\text{enfermo}\mid +)$. Son cosas distintas, y cuando la enfermedad es rara, distintísimas. Mini-caso: enfermedad con prevalencia $2\%$, prueba con sensibilidad $90\%$ y especificidad $95\%$. De cada 1000 personas, 20 enfermas (18 dan positivo) y 980 sanas (≈49 falsos positivos). Positivos totales ≈ 67, de los cuales solo 18 son reales: $P(\text{enfermo}\mid +)\approx 18/67 \approx 27\%$. Una prueba "del 90%" deja la mayoría de las alarmas como falsas, porque la **tasa base** manda. Esta arista vuelve en [[arena-q2]].

---

## Muestreo con y sin reemplazo

Cuatro variantes según si repones lo extraído y si el orden cuenta:

| Modo | $k$ de $n$ | Fórmula |
|------|-----------|---------|
| Con reemplazo, orden importa | secuencias | $n^k$ |
| Con reemplazo, orden no importa | "stars and bars" | $\binom{n+k-1}{k}$ |
| Sin reemplazo, orden importa | listas | $P(n,k)=\frac{n!}{(n-k)!}$ |
| Sin reemplazo, orden no importa | subconjuntos | $\binom{n}{k}$ |

Antes de elegir fórmula, **declara dos cosas**: ¿se repone? ¿importa el orden? Cambiar cualquiera de las dos cambia la fórmula por completo. Es el error de conteo más frecuente.

**Regla del complemento:** cuando el enunciado dice "al menos uno", casi siempre es más fácil contar lo contrario:

$$P(\text{al menos uno}) = 1 - P(\text{ninguno}).$$

Ejemplo (cumpleaños): $P(\text{dos personas coinciden})=1-\dfrac{365\cdot 364\cdots(365-n+1)}{365^n}$. Calcular "al menos una coincidencia" de frente es un infierno de casos; su complemento "ninguna coincidencia" es un producto limpio.

---

## Identidades combinatorias útiles

No las memorices como símbolos: cada una cuenta lo mismo de dos formas.

- $\binom{n}{k}=\binom{n}{n-k}$ — **simetría**: elegir quién entra es lo mismo que elegir quién queda fuera.
- $\binom{n}{k}=\binom{n-1}{k-1}+\binom{n-1}{k}$ — **Pascal**: fija a una persona; o está en el comité ($\binom{n-1}{k-1}$) o no ($\binom{n-1}{k}$).
- $\sum_{k=0}^n \binom{n}{k}=2^n$ — cada uno de los $n$ elementos entra o no en un subconjunto: $2^n$ subconjuntos.
- $\sum_{k=0}^n \binom{n}{k}x^k=(1+x)^n$ — **teorema del binomio**, la versión con peso de lo anterior.

---

## Mini-ejemplo trabajado: el problema de los sombreros sin tocar la independencia

$n$ personas dejan su sombrero; se los devuelven al azar. ¿Cuántas esperan recuperar el suyo? La tentación es modelar la permutación completa ($n!$ casos, dependencias horribles). En vez de eso, define indicadores: $X_i = 1$ si la persona $i$ recupera su sombrero. Por simetría $P(X_i=1) = 1/n$, así que $E[X_i] = 1/n$. Por **linealidad de la esperanza**:

$$E[X_1+\cdots+X_n] = \sum_{i=1}^n E[X_i] = n \cdot \frac1n = 1.$$

En promedio, exactamente **una** persona recupera su sombrero, *para cualquier $n$* —2 personas o un millón.

**Predicción antes de seguir:** los eventos $X_i$ no son independientes (si $n-1$ personas tienen su sombrero, la última también). ¿Eso rompe el cálculo? Respuesta: **no**. La linealidad de la esperanza no pide independencia; sumar esperanzas funciona aunque los sumandos estén correlacionados. Esa es justo su superpotencia: descompone un problema enredado en piezas triviales.

## Prototipo, contraejemplo y caso borde

- **Prototipo (complemento):** "$P(\text{al menos un éxito})$" casi siempre es más fácil como $1 - P(\text{ninguno})$; p. ej. $P(\text{al menos dos cumpleaños iguales}) = 1 - \tfrac{365\cdot364\cdots}{365^n}$.
- **Contraejemplo (Bayes invertido):** $P(+\mid\text{enfermo}) \neq P(\text{enfermo}\mid+)$. Con prevalencia $2\%$ y test al $95\%$, la mayoría de positivos son falsos. Leer la verosimilitud como posterior es el error clásico.
- **Caso borde (orden sí/no importa):** "$k$ de $n$ con reemplazo sin orden" no es $n^k$ ni $\binom{n}{k}$ sino $\binom{n+k-1}{k}$ (stars and bars). El borde fuerza a declarar si el orden y el reemplazo cuentan antes de elegir fórmula.

## Errores típicos

- **Conceptual:** exigir independencia para sumar esperanzas de indicadores (no hace falta).
- **Técnico:** olvidar dividir por las multiplicidades en anagramas ($n!/(n_1!\cdots)$) y sobrecontar permutaciones de letras repetidas.
- **De interpretación:** confundir "con/sin reemplazo" u "ordenado/no ordenado", que cambian por completo la fórmula de conteo.

## Transferencia isomorfa

- **Linealidad de la esperanza ↔ conteo de eventos en sistemas:** "número esperado de coincidencias / colisiones / patrones" se resuelve con indicadores sin pelear con la dependencia, idéntico al conteo de patrones en una secuencia (conecta con [[arena-q9]]).
- **Bayes con tasa base ↔ VPP de un clasificador:** prior×verosimilitud/evidencia es exactamente el valor predictivo positivo; sin prevalencia no inviertes el condicional (conecta con [[arena-q2]]).
- **LOTUS ↔ valorar $g(X)$ sin su distribución:** $E[g(X)] = \sum g(x)P(x)$ evita derivar la distribución de $g(X)$, como valorar un payoff $f(S)$ integrando contra la densidad de $S$ (conecta con [[arena-q5]]).
- **Inclusión-exclusión ↔ deduplicado por uniones:** sumar–restar solapamientos es el mismo principio que contar elementos únicos en uniones de conjuntos.

Moraleja de la arista: *para contar lo enredado, suma indicadores (la dependencia no estorba a la esperanza); para "al menos uno", usa el complemento; y nunca confundas la verosimilitud con el posterior.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "De cuántas formas ordenar con repeticiones" | $n!/(n_1!\cdots n_k!)$ |
| "$k$ objetos de $n$, sin orden, sin reemplazo" | $\binom{n}{k}$ |
| "$k$ objetos de $n$, con orden, sin reemplazo" | $P(n,k)$ |
| "$E[$función de VA$]$" | LOTUS directamente sobre la distribución de $X$ |
| "$E[$suma de indicadores$]$" | Linealidad; $E[X_i]\cdot n$ |
| "$P(\text{algún evento})$ difícil" | Complemento: $1-P(\text{ninguno})$ |
| "$P(\text{evento}\mid\text{condición}) \to P(\text{condición}\mid\text{evento})$" | Bayes con regla total |

---

> **Síntesis:** El conteo provee el espacio muestral; las reglas de probabilidad navegan en él. LOTUS y linealidad son los dos atajos más poderosos: LOTUS evita derivar nuevas distribuciones; linealidad elimina la necesidad de independencia. Bayes actualiza creencias. El principio de complemento simplifica "al menos uno".

---

*Retrieval: cierra y responde: (1) anagramas de PROBABILITY; (2) $E[X^2]$ para $X\sim\text{Poisson}(3)$; (3) $P(\text{divisible por 2 o 3 entre 1 y 60})$; (4) $P(\text{enfermo}\mid+)$ con prevalencia $2\%$, sensibilidad $90\%$, especificidad $95\%$.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puentes de regreso

El hogar de conteo y probabilidad se vuelve mas transferible cuando enlaza con sus canteras olimpicas: [[zeitz-61]] formaliza suma/producto/division, [[zeitz-62]] entrena particiones y biyecciones, [[zeitz-63]] controla solapes con inclusion-exclusion, [[engel-comb]] aporta practica intensa y [[aime-cnt]] muestra la version de examen bajo presion.
<!-- GRAFO_CONEXO_OLEADA3_END -->
