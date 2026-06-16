# Probabilidad para entrevistas de ciencia de datos

## De qué trata esta lección (y qué sabrás hacer al final)

Una entrevista de ciencia de datos casi nunca te pide demostrar un teorema; te pide **razonar bajo incertidumbre** con números concretos: "dado que el usuario hizo clic, ¿qué tan probable es que compre?", "este test salió positivo, ¿cuánto debo creerlo?", "¿cómo se comportan los usuarios a largo plazo?". Esta lección construye, **desde cero**, las cinco herramientas que cubren casi todas esas preguntas: probabilidad condicional y Bayes, la ley de probabilidad total, el conteo, un puñado de distribuciones y las cadenas de Markov.

Al terminar podrás: (1) reconocer que "dado que…" pide condicionar y a menudo **invertir** un condicional con Bayes; (2) no caer en la trampa de la **tasa base**; (3) descomponer una probabilidad enredada en un árbol de escenarios; (4) elegir la distribución correcta para un fenómeno (clics, llegadas, tiempos de espera); y (5) modelar transiciones de estado para predecir el equilibrio. No asumo nada previo: cada idea sale primero de un ejemplo, y solo después aparece la fórmula.

---

## Probabilidad condicional: saber algo achica el universo

Empecemos por lo más básico, porque todo lo demás cuelga de aquí. La **probabilidad** de un evento es "qué fracción de los mundos posibles lo cumplen". Si tiras un dado justo, $P(\text{par})=3/6$ porque 3 de los 6 mundos posibles son pares.

La **probabilidad condicional** $P(A\mid B)$ —se lee "probabilidad de $A$ dado $B$"— responde: *si ya sé que ocurrió $B$, ¿qué tan probable es $A$?* Saber $B$ **tacha** todos los mundos donde $B$ no pasó y reescala lo que queda:

$$P(A\mid B)=\frac{P(A\cap B)}{P(B)}.$$

Aquí $A\cap B$ es "ocurren $A$ **y** $B$ a la vez", y dividir por $P(B)$ es justamente "quedarme solo con el universo donde $B$ pasó". Ejemplo mínimo: saco una carta; $P(\text{rey})=4/52$. Pero si ya me dijeron que es figura ($B=$ {J,Q,K}, 12 cartas), entonces $P(\text{rey}\mid\text{figura})=4/12=1/3$. Condicionar no cambió las cartas; cambió el denominador.

Dos eventos son **independientes** si saber uno no informa del otro: $P(A\mid B)=P(A)$. Es la excepción cómoda, no la regla; en producto casi todo está correlacionado.

> **Señal de entrevista:** las palabras *"dado que"*, *"sabiendo que"*, *"entre los que…"* casi siempre piden condicionar, y muchas veces **invertir** el condicional. Eso último es Bayes.

## Bayes: dar vuelta el condicional

Aquí está la herramienta estrella. El problema recurrente es que **conoces $P(B\mid A)$ pero quieres $P(A\mid B)$**: el test te da $P(\text{positivo}\mid\text{enfermo})$ (su sensibilidad), pero a ti te importa $P(\text{enfermo}\mid\text{positivo})$. Bayes conecta los dos sentidos:

$$P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}.$$

Cada pieza tiene nombre y rol:

- **Prior** $P(A)$ — lo que creías *antes* de ver el dato (p. ej. la prevalencia de la enfermedad).
- **Likelihood** (verosimilitud) $P(B\mid A)$ — qué tan compatible es el dato con la hipótesis.
- **Posterior** $P(A\mid B)$ — tu creencia *actualizada* tras ver el dato.
- El denominador $P(B)$ solo **normaliza** (se calcula con la ley de probabilidad total, abajo).

La idea profunda: $\text{posterior} \propto \text{likelihood} \times \text{prior}$. Un dato muy informativo (likelihood alta) mueve mucho la creencia, pero **siempre** pesa contra lo que creías antes. Por eso un prior diminuto (enfermedad rara) puede aplastar un dato fuerte.

## Ley de probabilidad total: descomponer en un árbol de escenarios

A veces $P(A)$ es difícil de calcular de golpe, pero fácil si parto el mundo en casos. Si los $B_i$ forman una **partición** (disjuntos —no se solapan— y exhaustivos —cubren todo—):

$$P(A)=\sum_i P(A\mid B_i)\,P(B_i).$$

En palabras: calculo $A$ "por ramas" y recombino cada rama con su peso $P(B_i)$. Es el promedio ponderado de las probabilidades condicionales.

Ejemplo: probabilidad de que un cliente compre $=P(\text{compra}\mid\text{segmento premium})\,P(\text{premium}) + P(\text{compra}\mid\text{segmento básico})\,P(\text{básico})$. Cada segmento es una rama; sumo ponderando por su tamaño. Esta ley es la que produce el $P(B)$ que necesita Bayes: por eso suelen aparecer juntas.

## Conteo: cuando la probabilidad es un cociente de "de cuántas formas"

Cuando todos los resultados son igualmente probables, $P=\dfrac{\text{casos favorables}}{\text{casos posibles}}$, y ambos son **conteos**. Las dos preguntas que siempre debes hacerte: *¿importa el orden? ¿se repone lo extraído?*

- **Permutaciones** (el orden **sí** importa): ordenar $k$ de $n$ da $\dfrac{n!}{(n-k)!}$. El factorial $n!=n\cdot(n-1)\cdots 1$ cuenta de cuántas formas se ordena una fila. Ejemplo: contraseñas, podios.
- **Combinaciones** (el orden **no** importa): elegir $k$ de $n$ da $\binom{n}{k}=\dfrac{n!}{k!\,(n-k)!}$. Se divide por $k!$ porque las $k!$ reordenaciones de los mismos elegidos son el mismo grupo. Ejemplo: elegir 4 restaurantes de un mapa, una mano de cartas.

La pregunta puede venir directa ("¿de cuántas formas se sientan 5 personas?") o disfrazada de probabilidad ("¿prob. de sacar 4 cartas del mismo palo?"). Decide **siempre** orden/reemplazo antes de escribir una fórmula: es el error de conteo más común.

> **Predicción antes de seguir:** "¿de cuántas formas elegir un comité de 3 entre 8?" ¿$8\cdot7\cdot6$ o $\binom{8}{3}$? Respuesta: $\binom{8}{3}=56$. Un comité {Ana, Beto, Carla} es el mismo sin importar el orden en que los nombres; $8\cdot7\cdot6=336$ cuenta cada comité $3!=6$ veces. Divides por las repeticiones que no querías contar.

## Variables aleatorias y sus distribuciones

Una **variable aleatoria** (v.a.) es un número que depende del azar (el resultado de un dado, el nº de clics en una hora). Su **distribución** dice con qué probabilidad toma cada valor: **PMF** $P(X=x)$ si es discreta (valores separados), **PDF** $f_X(x)$ si es continua (un continuo de valores). Ambas son no negativas y suman/integran a 1. La **CDF** $F_X(x)=P(X\le x)$ acumula "probabilidad hasta $x$": es monótona creciente, de 0 a 1.

No se trata de memorizar fórmulas exóticas, sino de **reconocer qué fenómeno modela cada distribución** y recordar su media y varianza:

| Distribución | Modela | Media | Varianza |
|---|---|---|---|
| **Binomial**(n,p) | nº de éxitos en n ensayos binarios | $np$ | $np(1-p)$ |
| **Poisson**(λ) | nº de eventos en un intervalo fijo, tasa λ | $\lambda$ | $\lambda$ |
| **Uniforme**(a,b) | valor equiprobable en $[a,b]$ | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$ |
| **Exponencial**(λ) | tiempo entre eventos de un Poisson | $1/\lambda$ | $1/\lambda^2$ |
| **Normal**(μ,σ²) | campana; límite de promedios (CLT) | $\mu$ | $\sigma^2$ |

Cómo elegir, con la intuición de cada una: **binomial** = "cuántos de $n$ intentos binarios salen bien" (signups de $n$ visitantes); **Poisson** = "cuántos eventos raros caen en una ventana" (visitas por hora); **exponencial** = "cuánto espero hasta el próximo evento" y es **sin memoria** (lo esperado no cambia por lo ya esperado); **normal** = aparece sola cuando promedias muchas cosas, por el Teorema Central del Límite. Nota la coherencia: una Binomial es $n$ Bernoullis sumadas, y su media $np$ es $n$ veces la de una ($p$).

## Distribuciones conjuntas, marginales y condicionales

Con dos v.a. a la vez surge la **conjunta** $f_{X,Y}(x,y)$ ("probabilidad de que $X$ valga $x$ **y** $Y$ valga $y$"). Si solo te importa una, recuperas su **marginal** sumando/integrando la otra: $f_X(x)=\int f_{X,Y}(x,y)\,dy$ (barres todos los valores de $Y$). Y las **condicionales** extienden Bayes al caso multivariado. Regla práctica: cuando aparece más de una v.a. relacionada, piensa en términos de la conjunta y de ahí baja a marginales o condicionales según lo que pidan.

## Cadenas de Markov: el futuro solo mira al presente

Una **cadena de Markov** es un proceso que salta entre estados finitos, donde la probabilidad del próximo estado depende **solo del actual**, no de toda la historia (propiedad de Markov: pasado y futuro son condicionalmente independientes dado el presente). Las probabilidades de salto viven en una **matriz de transición** $P$, donde $P_{ij}=P(\text{ir a } j\mid\text{estar en } i)$.

Dos conceptos clave:

- Un estado es **recurrente** si, una vez que entras, volverás con certeza; es **transiente** si hay probabilidad positiva de no volver jamás.
- La **distribución estacionaria** $\pi$ es la que cumple $\pi=\pi P$: una vez ahí, el sistema se queda en esa mezcla. Bajo condiciones suaves, $\pi$ es la **proporción de tiempo a largo plazo** en cada estado, y *olvida* dónde empezaste.

Aplicación típica: modela usuarios como estados (nuevo → activo → churned), pon las probabilidades de transición y pregunta el comportamiento a largo plazo. La estacionaria te dice qué fracción acabará en cada estado, sin importar la mezcla inicial.

> **Predicción antes de seguir:** si la matriz $P$ cambia de un día para otro (el producto se rediseñó), ¿la $\pi$ de antes sigue valiendo? Respuesta: **no**. La estacionaria es de *esa* matriz; cambiar las transiciones cambia el equilibrio. La propiedad de Markov asume transiciones estables — un supuesto que conviene declarar en voz alta en la entrevista.

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
