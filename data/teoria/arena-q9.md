# Arena Quant · Probabilidad condicional, Bayes y conteo

## De qué trata (y qué sabrás hacer)

La mayoría de los errores en estos problemas no son de aritmética: son de **espacio muestral**. Antes de dividir nada, escribe los casos elementales y sus probabilidades. Esta lección reúne tres herramientas que, bien usadas, resuelven casi cualquier acertijo de probabilidad de mesa: **Bayes** (mezclar prior y verosimilitud), **simetría** (colapsar conteos por argumentos de "todos iguales") y **linealidad de la esperanza** (sumar indicadores sin pelear con la dependencia).

Al terminar sabrás reconocer cuál de las tres pide el problema, y tendrás presentes dos restricciones que la gente olvida: las correlaciones no son libres (la matriz debe ser semidefinida positiva) y no toda distribución tiene varianza (la Cauchy). Todo se construye desde casos pequeños.

---

## Bayes con tasa base

Una bolsa con 9 monedas justas y 1 de dos caras. Sacas una y salen 3 caras seguidas. ¿$P(\text{es la de dos caras})$?

$$P(2C\mid CCC)=\frac{1\cdot\tfrac1{10}}{1\cdot\tfrac1{10}+\tfrac18\cdot\tfrac9{10}}=\frac{8}{17}\approx 0.47.$$

La trampa: la verosimilitud ($1$ vs $\tfrac18$) empuja fuerte hacia la trucada, pero la **tasa base** ($\tfrac1{10}$ vs $\tfrac9{10}$) la frena. El resultado, $\tfrac8{17}$, vive entre ambas fuerzas — el mismo motor que el valor predictivo positivo de un test (conecta con [[arena-q2]]).

Variante reveladora: "saco una moneda de aspecto normal y salen 3 caras, ¿$P(\text{siguiente cara})$?". Si la crees justa: $\tfrac12$ (tiradas independientes). Pero con **100** caras seguidas, $P(\text{justa})$ se desploma ($2^{-100}$ de verosimilitud) y el prior despierta: ahora $P(\text{trucada}\mid 100H)\approx1$. Sin dato extremo, una moneda normal es justa; el dato extremo activa el razonamiento bayesiano.

---

## Simetría: la navaja del conteo

Cuando todos los casos son intercambiables, la simetría da la respuesta sin contar:

- **Dos cartas de un mazo; tú sacas una, yo otra. ¿$P(\text{la mía}>\text{la tuya})$?** O empatan en rango ($P=\tfrac{3}{51}$) o no; si no empatan, por simetría es $\tfrac12$. Respuesta: $\tfrac12\cdot\tfrac{48}{51}=\tfrac{24}{51}$.
- **Cajón con 2 rojos y 2 negros; sacas 2. ¿$P(\text{emparejan color})$?** Tras sacar uno quedan 3, de los cuales solo 1 empareja → $\tfrac13$.
- **Torneo de $2^n$ equipos, el mejor siempre gana. ¿$P(\text{el 2.º mejor llega a la final})$?** Solo si cae en la otra mitad del cuadro: $\tfrac{2^{n-1}}{2^n-1}$.

---

## Conteo y linealidad disfrazada

- **Dos ases al sacar 2 cartas:** con reemplazo $(\tfrac1{13})^2=\tfrac1{169}$; sin reemplazo $\tfrac1{13}\cdot\tfrac{3}{51}=\tfrac1{221}$.
- **Lanzas una moneda $10^6$ veces. ¿Número esperado de cadenas "6 caras seguidas de 6 cruces"?** Hay $10^6-11$ posiciones; cada una acierta con probabilidad $2^{-12}$. Por **linealidad** (que no exige independencia): $(10^6-11)/2^{12}\approx 244.14$.
- **¿El 4.º día hábil del mes cae en jueves?** Es jueves si el día 1 cae en sábado, domingo o lunes → $\tfrac37$.

---

## Matriz de correlaciones: ¿es posible?

"$\rho(A,B)=0.9$, $\rho(B,C)=0.8$, ¿puede $\rho(A,C)=0.1$?" Las correlaciones no son libres: la matriz debe ser **semidefinida positiva** (toda combinación lineal tiene varianza $\ge0$). Para

$$\begin{pmatrix}1&0.9&0.1\\0.9&1&0.8\\0.1&0.8&1\end{pmatrix}$$

el determinante es $-0.316<0$, así que **no** es PSD → imposible. Hay una desigualdad tipo triangular entre los ángulos: si A está muy cerca de B y B muy cerca de C, A no puede estar lejos de C.

---

## Varianza infinita

La **Cauchy**, con densidad $\tfrac{1}{\pi(1+x^2)}$, no tiene ni media ni varianza: $\int \tfrac{x^2}{1+x^2}\,dx$ diverge. Es el contraejemplo estándar al teorema del límite central y a la idea de que "promediar siempre reduce el ruido" — con colas tan pesadas, el promedio de $n$ Cauchy sigue siendo Cauchy (conecta con [[arena-q11]]).

---

## Mini-ejemplo trabajado: contar patrones con linealidad

Lanzas una moneda justa $10^6$ veces. ¿Cuántas apariciones esperadas del patrón exacto "6 caras seguidas de 6 cruces" (12 símbolos)? No modeles las dependencias entre posiciones solapadas: define un **indicador** $I_k=1$ si el patrón empieza en la posición $k$. Hay $10^6-11$ posiciones válidas, y cada una acierta con probabilidad $2^{-12}$. Por **linealidad de la esperanza** (que NO exige independencia):

$$E[\text{total}]=\sum_k E[I_k]=(10^6-11)\cdot 2^{-12}\approx 244.14.$$

**Predicción antes de seguir:** los eventos $I_k$ de posiciones vecinas están correlacionados (se solapan). ¿Eso invalida el cálculo de la *esperanza*? Respuesta: **no**. La linealidad de la esperanza es ciega a la dependencia; solo necesitarías la independencia si calcularas la *varianza*. Esa ceguera es justo lo que la hace tan potente.

## Prototipo, contraejemplo y caso borde

- **Prototipo (Bayes con base):** un dato a favor (3 caras) más una tasa base ($\tfrac1{10}$ trucada) → la respuesta $\tfrac8{17}$ vive *entre* prior y verosimilitud, nunca en el extremo.
- **Contraejemplo (correlaciones "libres"):** $\rho(A,B)=0.9$, $\rho(B,C)=0.8$ no permiten $\rho(A,C)=0.1$; la matriz no es semidefinida positiva (det $<0$). Tratar las correlaciones como independientes es el error.
- **Caso borde (Cauchy):** sin media ni varianza, promediar no concentra nada; el contraejemplo estándar a "más muestras = menos ruido".

## Errores típicos

- **Conceptual:** dejar que la verosimilitud arrastre toda la decisión e ignorar la tasa base (la moneda trucada es rara: $\tfrac1{10}$).
- **Técnico:** exigir independencia para sumar esperanzas de indicadores solapados — no hace falta.
- **De supuestos:** asignar correlaciones a mano sin verificar que la matriz sea PSD, o aplicar el TLC a colas pesadas (Cauchy).

## Transferencia isomorfa

- **Linealidad de la esperanza ↔ conteo de eventos raros en sistemas:** "número esperado de colisiones / de falsos positivos / de patrones" se suma con indicadores sin pelear con la dependencia, igual que estimar carga esperada en un sharding (conecta con [[arena-sd2]]).
- **Bayes (prior×verosimilitud) ↔ VPP:** $\tfrac8{17}$ es el mismo motor que el valor predictivo positivo de un test; la rareza frena al dato (conecta con [[arena-q2]]).
- **Matriz de correlación PSD ↔ varianza de portafolio $\ge0$:** que toda combinación $a^\top C a$ sea no negativa es por qué no puedes inventar correlaciones; la misma restricción gobierna el riesgo de una cartera (conecta con [[arena-q6]]).
- **Cauchy ↔ TLC que falla:** cola pesada sin segundo momento aparece también como cociente de dos brownianos (conecta con [[arena-q11]]).

Moraleja de la arista: *para contar, suma indicadores (la dependencia no estorba a la esperanza); para creer, mezcla prior y verosimilitud; y recuerda que las correlaciones viven presas dentro de una matriz PSD.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "test/moneda trucada, dato a favor" | Bayes con tasa base; el resultado vive entre prior y verosimilitud |
| "¿mi carta $>$ la tuya?" | divide en empate/no-empate, usa simetría $\tfrac12$ |
| "nº esperado de patrones" | linealidad de la esperanza sobre indicadores |
| "¿es posible esta correlación?" | exige matriz PSD (determinantes $\ge0$) |
| "media/varianza no existe" | piensa en Cauchy (colas pesadas) |

---

> ❧ **Síntesis:** condicionar bien es enumerar el espacio muestral correcto. Bayes mezcla prior y verosimilitud; la simetría colapsa conteos; la linealidad de la esperanza suma indicadores sin pelear con la independencia; y recuerda que las correlaciones viven dentro de una matriz que debe ser PSD.

---

*Retrieval: cierra la página y responde — (1) $P(\text{dos caras}\mid\text{3 caras})$ con 1 de 10 trucada; (2) $P(\text{mi carta}>\text{la tuya})$; (3) por qué $(10^6-11)/2^{12}$; (4) criterio PSD para una matriz de correlaciones.*
