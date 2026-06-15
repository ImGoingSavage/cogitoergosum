# Paradojas probabilísticas

## De qué trata (y qué sabrás hacer)

Una "paradoja" probabilística casi nunca es un misterio profundo: es un **condicional invertido** o una **tasa base olvidada**. La intuición grita una respuesta; el cálculo cuidadoso da otra. Esta lección recorre las paradojas clásicas mostrando que casi todas se desarman con la misma herramienta —Bayes y un espacio muestral bien escrito—.

Al terminar reconocerás los tres errores recurrentes (confundir $P(A\mid B)$ con $P(B\mid A)$, ignorar la prevalencia, y mezclar priors mal definidos), y sabrás por qué surgen el sesgo de longitud (paradoja de la inspección) y la reversión de Simpson. Cada paradoja se construye desde su tabla de casos.

---

## Las tres cajas (Bertrand)

Tres cajas: una con dos monedas de oro (OO), una con dos de plata (PP), una mixta (OP). Eliges una caja al azar y sacas una moneda: es **oro**. ¿$P(\text{la otra moneda de esa caja es oro})$?

La intuición dice $\tfrac12$ ("quedan dos cajas compatibles, OO y OP"). Es falso. Cuenta **caras de oro**, no cajas: hay 3 monedas de oro en juego (las 2 de OO y la 1 de OP). De esas 3, **2** pertenecen a la caja OO (cuya otra moneda es oro). Por tanto

$$P=\frac23.$$

El error es tratar las dos cajas como equiprobables tras ver oro: la caja OO tenía el doble de probabilidad de entregarte una cara de oro.

---

## Dos hijos

Un padre tiene 2 hijos. La respuesta depende **exactamente** de cómo se da la información:
- **"Al menos uno es niño":** los casos $(N,N),(N,G),(G,N)$ siguen vivos, $(G,G)$ no. $P(\text{ambos niños})=\tfrac13$.
- **"El mayor es niño":** fija una coordenada, quedan $(N,N),(N,G)$. $P=\tfrac12$.
- **"Uno es niño nacido en martes":** $P=\tfrac{13}{27}$. El dato extra (el día) rompe parte de la simetría y mueve la respuesta entre $\tfrac13$ y $\tfrac12$.

La lección: "información sobre uno de dos" no es una sola pregunta; **cómo** se selecciona el dato cambia el espacio condicionado.

---

## Los tres prisioneros (Monty Hall disfrazado)

A, B, C; uno será liberado al azar. El guardia (que sabe quién) le dice a A: "B será ejecutado". ¿Sube la esperanza de A?

| Liberado | $P(\text{guardia dice "B"})$ | Peso posterior |
|-------|-----------------|-------------|
| A | $\tfrac12$ | $\tfrac16$ |
| B | $0$ | $0$ |
| C | $1$ | $\tfrac13$ |

$$P(\text{A libre}\mid\text{dice B})=\frac{1/6}{1/6+1/3}=\frac13, \qquad P(\text{C libre}\mid\cdots)=\frac23.$$

A **no** mejora ($\tfrac13$); toda la masa liberada cae en C. Es Monty Hall con otro disfraz: el guardia actúa con información.

---

## La paradoja de los dos sobres

Dos sobres; uno tiene el doble del otro. Abres uno y ves \$$x$. El argumento tentador: el otro vale $\tfrac12(\tfrac x2)+\tfrac12(2x)=\tfrac{5x}{4}>x$, así que **siempre conviene cambiar** — absurdo (por simetría no puede convenir siempre).

La falacia: tratar $x/2$ y $2x$ como igual de probables implica un **prior impropio** sobre la cantidad (uniforme sobre todas las potencias de 2, que no suma 1). Con cualquier prior **propio**, la ganancia esperada de cambiar es 0. Moraleja: la esperanza condicional exige un modelo probabilístico coherente; sin prior válido, el álgebra es vacía.

---

## La paradoja de Simpson

Un tratamiento puede ser mejor en **cada** subgrupo y peor en el **total**:

| | Hombres | Mujeres | Total |
|---|---------|---------|-------|
| Trat. A | $18/20=90\%$ | $2/10=20\%$ | $20/30\approx67\%$ |
| Trat. B | $7/10=70\%$ | $1/20=5\%$ | $8/30\approx27\%$ |

A gana en hombres ($90\%>70\%$) y en mujeres ($20\%>5\%$). En el total **A también gana aquí** ($67\%>27\%$) — pero invirtiendo las proporciones de asignación, el agregado se puede revertir. La causa es que la variable "sexo" confunde: si el grupo más fácil se asigna desproporcionadamente a un tratamiento, el promedio crudo miente. Estratificar por la confundidora corrige (conecta con [[arena-h1]] y [[arena-h17]]).

---

## La paradoja de la inspección (sesgo de longitud)

Un autobús pasa cada $\tau$ minutos en promedio (intervalo aleatorio). Llegas en un instante al azar. ¿Cuánto esperas? **No** es $E[\tau]/2$, porque tienes más probabilidad de aterrizar dentro de un intervalo **largo** que de uno corto:

$$E[\text{intervalo que interceptas}]=\frac{E[\tau^2]}{E[\tau]}\ge E[\tau].$$

Para llegadas de Poisson ($\tau\sim\text{Exp}(\lambda)$), el intervalo interceptado mide $2/\lambda=2\,E[\tau]$ — ¡el doble! El mismo sesgo explica por qué "tus amigos tienen en promedio más amigos que tú" (conecta con el immortal time de [[arena-h2]]).

---

## La falacia del fiscal

Un perfil de ADN coincide: el laboratorio dice $P(\text{coincidencia}\mid\text{inocente})=10^{-6}$. El fiscal concluye $P(\text{inocente}\mid\text{coincidencia})=10^{-6}$. **Error** — invirtió el condicional. Con una ciudad de $10^6$ personas y 1 culpable:

$$P(\text{coincidencia})\approx \underbrace{10^{-6}\cdot\tfrac{999999}{10^6}}_{\text{inocentes que coinciden}}+\underbrace{1\cdot 10^{-6}}_{\text{culpable}}\approx 2\times10^{-6},$$

así que $P(\text{inocente}\mid\text{coincidencia})\approx\tfrac12$, no uno en un millón. La evidencia sola, sin la tasa base de cuántos inocentes hay, no condena (conecta con [[arena-q2]]).

---

## El hash de cumpleaños

¿Cuántos elementos para que $P(\text{colisión})>\tfrac12$ en una tabla de $N$ slots? Usando $P(\text{sin colisión})\approx e^{-k(k-1)/(2N)}$:

$$k(k-1)<2N\ln 2 \;\Rightarrow\; k\approx 1.177\sqrt N.$$

Para $N=365$: $k\approx 23$ (el cumpleaños clásico). Para hashes de $2^{64}$ slots, esperas colisión tras $\approx 2^{32}\approx 4$ mil millones de entradas. Lo que crece es el número de **pares** $\binom{k}{2}$, no $k$.

---

## La tasa de error acumulada

Si corres $k$ pruebas independientes, cada una con significancia $\alpha=5\%$, la probabilidad de **al menos un** falso positivo es $1-(1-\alpha)^k$:

| $k$ | $P(\ge 1\text{ error tipo I})$ |
|-----------------|---------------------------|
| 1 | $5\%$ |
| 16 | $\approx 55\%$ |
| 100 | $\approx 99.4\%$ |

La corrección de **Bonferroni** usa $\alpha/k$ por prueba para controlar la tasa familiar (conecta con [[arena-dg3]]).

---

## Mini-ejemplo trabajado: la falacia del fiscal, con la tasa base

Un perfil de ADN coincide con el acusado; el laboratorio dice "$P(\text{coincidencia}\mid\text{inocente})=$ 1 en un millón". El fiscal concluye "luego hay 1 en un millón de que sea inocente". **Falso.** Aplica Bayes en una ciudad de 1 000 000:

- Esperados por azar entre inocentes: $1\,000\,000\times 10^{-6}\approx 1$ coincidencia inocente.
- Más la coincidencia del verdadero culpable: 1.
- $P(\text{inocente}\mid\text{coincidencia})\approx \tfrac{1}{1+1}=\tfrac12$, no 1 en un millón.

La evidencia sola, sin la tasa base de cuántos inocentes hay, no condena.

**Predicción antes de seguir:** ¿qué error cometió el fiscal? Respuesta: confundir $P(\text{coincidencia}\mid\text{inocente})$ con $P(\text{inocente}\mid\text{coincidencia})$ — invertir el condicional. Es **idéntico** a leer la sensibilidad de un test como su valor predictivo positivo: con una base enorme de "negativos reales", los falsos positivos dominan. Bayes y la tasa base son el antídoto a las tres grandes paradojas (fiscal, dos sobres, Simpson).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "evidencia rara, ¿culpable/enfermo?" → Bayes con tasa base; no inviertas el condicional.
- **Contraejemplo (Simpson):** un tratamiento mejor en cada subgrupo puede salir peor en el total si la asignación está confundida; la asociación agregada se revierte al estratificar.
- **Caso borde (adivinar cartas con feedback):** aunque conozcas las cartas ya vistas, $E[\text{aciertos}]=26$ en un mazo de 52, igual que sin estrategia; la información no ayuda en esperanza. El borde muestra que "saber más" no siempre cambia el resultado esperado.

## Errores típicos

- **Conceptual:** confundir $P(A\mid B)$ con $P(B\mid A)$ (fiscal); ignorar la tasa base.
- **Técnico:** usar un prior impropio (dos sobres: $P(2x)$ y $P(x/2)$ "iguales") que no normaliza, produciendo el falso "siempre cambiar".
- **De supuestos:** leer una asociación agregada como causal sin estratificar por la confundidora (Simpson).

## Transferencia isomorfa

- **Falacia del fiscal ↔ tasa base y VPP:** $P(\text{inocente}\mid\text{match})\ne P(\text{match}\mid\text{inocente})$ es exactamente sensibilidad $\ne$ VPP (conecta con [[arena-q2]]).
- **Paradoja de Simpson ↔ confounding y back-door:** la reversión al estratificar es la firma de un confundidor no ajustado (conecta con [[arena-h17]] y [[arena-h1]]).
- **Hash de cumpleaños ($k\approx1.177\sqrt N$) ↔ colisiones y ocupación:** el mismo conteo que ~37% de cajas vacías y las colisiones de un sharding (conecta con [[arena-fc1]] y [[arena-sd2]]).
- **Tasa de error acumulada ↔ tests múltiples:** $1-(1-\alpha)^k$ creciendo a $\approx1$ es la multiplicidad que corrige Bonferroni (conecta con [[arena-dg3]]).
- **Paradoja de la inspección ↔ sesgo de longitud / supervivencia:** interceptar intervalos largos con más probabilidad es el mismo sesgo que el immortal time (conecta con [[arena-h2]]).

Moraleja de la arista: *casi toda paradoja probabilística es un condicional invertido o una tasa base olvidada; Bayes es el antídoto universal.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Sacas una moneda de oro, ¿la otra cara?" | Bertrand: $\tfrac23$ (no $\tfrac12$) |
| "Un hijo es niño, ¿ambos?" | "Al menos uno": $\tfrac13$; "el mayor": $\tfrac12$ |
| "Guardia revela que B ejecutado" | Tres prisioneros: A se queda en $\tfrac13$ |
| "Siempre cambiar el sobre" | Falacia: prior impropio |
| "Tratamiento mejor por subgrupo" | Simpson: verificar confundidora |
| "$E[\text{intervalo del autobús}]$" | Inspección: $\tfrac{E[\tau^2]}{E[\tau]}\ge E[\tau]$ |
| "Match de DNA, ¿culpable?" | Tasa base: $P(\text{inocente}\mid\text{match})\ne 1-p$ |
| "Colisión en tabla de $N$ slots" | $k\approx 1.177\sqrt N$ |

---

> **Síntesis:** Las paradojas probabilísticas exponen malentendidos del razonamiento condicional. Los tres grandes errores: (1) ignorar la tasa base (falacia del fiscal); (2) confundir $P(A\mid B)$ con $P(B\mid A)$; (3) mezclar priors impropios (dos sobres). El teorema de Bayes es el antídoto a todos.

---

*Retrieval: cierra y responde: (1) $P(\text{otra cara es oro})$ en las tres cajas; (2) $P(\text{ambos niños}\mid\text{al menos uno es niño})$; (3) $E[\text{intervalo interceptado}]$ para Poisson con $E[\tau]=10$; (4) $k$ para $P(\text{colisión})>50\%$ en tabla de 10 000 slots.*
