# Probabilidad y Bayes · Entrevistas cuantitativas

## De qué trata (y qué sabrás hacer)

Casi todos los errores en estos problemas no son de cálculo, sino de **espacio muestral mal condicionado**: no actualizar correctamente cuando llega información. El hilo de esta lección es uno solo: *cuando alguien con información revela algo, el espacio de posibilidades se reescribe*. Monty Hall, la moneda trucada y la ruleta rusa son la misma idea vista desde ángulos distintos.

Al terminar sabrás: aplicar Bayes recordando la tasa base, reconocer cuándo una revelación es informativa (y cuándo no), montar cadenas de estados para esperanzas con rachas, y resolver problemas de optimización condicional. Cada uno se construye contando estados.

---

## Bayes con tasa base

La fórmula es fácil; la trampa es **la prevalencia**:

$$P(E\mid +)=\frac{P(+\mid E)\,P(E)}{P(+\mid E)\,P(E)+P(+\mid\neg E)\,P(\neg E)}.$$

Ejemplo: prevalencia $0.5\%$, sensibilidad $100\%$, especificidad $93\%$ (falsos positivos $7\%$).
- Numerador: $1\times0.005=0.005$.
- Denominador: $0.005+0.07\times0.995\approx0.0747$.
- $P(E\mid +)\approx 6.7\%$.

Con prevalencia baja, la mayoría de positivos son falsos. En 10 000 personas: 50 verdaderos positivos frente a $\approx697$ falsos $\Rightarrow$ 14 falsos por cada verdadero (conecta con [[arena-q2]]).

---

## El problema de Monty Hall

Eliges la puerta A (premio con $P=\tfrac13$). El anfitrión —que **sabe** dónde está el premio— abre una puerta vacía distinta. ¿Conviene cambiar? Sí: cambiar gana con $P=\tfrac23$.

Recupéralo contando los tres estados igual de probables (eliges A):
- Premio en **A** ($\tfrac13$): el anfitrión abre B o C; **quedarte gana**, cambiar pierde.
- Premio en **B** ($\tfrac13$): el anfitrión *debe* abrir C; **cambiar a B gana**.
- Premio en **C** ($\tfrac13$): el anfitrión *debe* abrir B; **cambiar a C gana**.

Cambiar gana 2 de 3. El error clásico ("quedan 2 puertas, $\tfrac12$") ignora que el anfitrión **actúa con información**: su elección de qué abrir concentra la masa $\tfrac23$ en la puerta que no abrió.

---

## Moneda de dos caras — Bayes secuencial

Un frasco tiene 999 monedas justas y 1 de dos caras. Sacas una y salen 10 caras seguidas. ¿$P(\text{es la de dos caras})$?

$$P(2C\mid 10H)=\frac{1/1000}{1/1000+(1/1024)(999/1000)}=\frac{1024}{2023}\approx 50.6\%.$$

Intuición: la moneda de dos caras es $1024$ veces más capaz de producir lo observado (verosimilitud). Aunque es rarísima a priori ($1/1000$), esa enorme ventaja de verosimilitud casi cancela su rareza. La respuesta vive **entre** prior y verosimilitud.

---

## Valor esperado con cadena de estados

¿Cuántos lanzamientos de una moneda justa esperas hasta ver $k$ caras seguidas? Define estados según cuántas caras llevas: $E_j$ = lanzamientos esperados desde "llevo $j$ caras consecutivas". Cada lanzamiento avanza (cara) o reinicia (cruz):

$$E_0=1+\tfrac12 E_1+\tfrac12 E_0,\quad E_1=1+\tfrac12 E_2+\tfrac12 E_0,\ \ldots,\ E_{k-1}=1+\tfrac12\cdot0+\tfrac12 E_0.$$

Resolviendo, $E_0=2+4+\cdots+2^k=2(2^k-1)$.

| $k$ | $E[\text{lanzamientos}]$ |
|---|----------------|
| 2 | 6 |
| 3 | 14 |
| 4 | 30 |

Plantear estados y resolver hacia atrás es **backward induction**, idéntico a la recurrencia de un DP (conecta con [[arena-cc3]]).

---

## Ruleta rusa — condicionar en lo ya ocurrido

Revólver de 6 recámaras con **2 balas contiguas**. Sobreviviste al primer disparo (el tambor ya estaba en posición, sin girar). ¿Girar antes del segundo?

Dado que sobreviviste, las posiciones posibles de las balas son $\{2,3\},\{3,4\},\{4,5\},\{5,6\}$ (4 casos igual de probables). Solo $\{2,3\}$ pone una bala en la siguiente recámara:
- **No girar:** $P(\text{sobrevivir})=\tfrac34=75\%$.
- **Girar:** $P(\text{sobrevivir})=\tfrac46\approx66.7\%$.

**No gires.** La contigüidad de las balas es el dato que rompe la simetría y cambia la respuesta.

---

## Optimización de probabilidad — frascos y bolas

50 bolas blancas y 50 negras en 2 frascos; eliges un frasco al azar con los ojos vendados y sacas una bola, ganando si es blanca. ¿Cómo repartes para maximizar $P(\text{blanca})$?

Óptimo: **1 blanca sola en el frasco A**, y las 49 blancas + 50 negras en el B.

$$P=\tfrac12\cdot1+\tfrac12\cdot\frac{49}{99}=\tfrac12+\frac{49}{198}\approx 74.75\%.$$

Lógica: el frasco A garantiza victoria si lo eliges; el B conserva casi la mitad de las blancas para no desperdiciar masa. Ninguna otra repartición supera esto.

---

## Mini-ejemplo trabajado: Monty Hall por conteo de estados

No memorices "$\tfrac23$"; recupéralo contando. Tres puertas, premio uniforme, eliges A:

- Premio en **A** (prob $\tfrac13$): el anfitrión abre B o C; **quedarte gana**, cambiar pierde.
- Premio en **B** (prob $\tfrac13$): el anfitrión *debe* abrir C (no puede abrir tu A ni el premio); **cambiar a B gana**.
- Premio en **C** (prob $\tfrac13$): el anfitrión *debe* abrir B; **cambiar a C gana**.

Cambiar gana en 2 de los 3 estados → $P=\tfrac23$. La clave es que el anfitrión **actúa con información**: su elección de qué abrir filtra los estados, concentrando la masa $\tfrac23$ en la puerta que no abrió.

**Predicción antes de seguir:** ¿qué pasa si el anfitrión abre una puerta *al azar* (y resulta vacía por suerte)? Respuesta: entonces no filtra información condicionada y la probabilidad se vuelve $\tfrac12$ — quedarte o cambiar da igual. La paradoja vive *enteramente* en que el anfitrión sabe.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** un agente con información revela algo no aleatorio → recondiciona el espacio (Monty Hall, moneda de dos caras).
- **Contraejemplo (Monty aleatorio):** si quien revela actúa sin información, no hay actualización informativa y "quedan 2, luego $\tfrac12$" sí vale. El error es aplicar la intuición de Monty cuando la revelación fue azarosa.
- **Caso borde (ruleta rusa):** balas *contiguas* rompen la simetría; condicionar en "sobreviví" deja $\{2,3\},\{3,4\},\{4,5\},\{5,6\}$ y solo $\{2,3\}$ es fatal → no girar ($\tfrac34>\tfrac23$). El borde muestra que la contigüidad es el dato que cambia la respuesta.

## Errores típicos

- **Conceptual:** no condicionar sobre el evento ya ocurrido (sobreviví, el anfitrión abrió) y contar estados a priori.
- **Técnico:** en Bayes secuencial, comparar solo las *prior* ("la moneda de dos caras es rarísima, $1/1000$") e ignorar el cociente de verosimilitudes ($1024\times$) que casi cancela la rareza.
- **De interpretación:** confundir "el anfitrión abrió una vacía" (información) con "salió una vacía por azar" (sin información).

## Transferencia isomorfa

El hilo común es **actualizar creencias cuando una observación reduce el espacio de estados**:

- **Moneda de dos caras ↔ likelihood ratio encadenado:** $P(2C\mid 10H)\propto$ verosimilitud $\times$ prior es el mismo cómputo que multiplicar $LR^+$ de tests médicos independientes (conecta con [[arena-q2]], odds posteriores $=LR\times$ odds previos).
- **Anfitrión que revela ↔ selección/censura informativa:** condicionar en lo que un proceso con información decide mostrar es la estructura del sesgo de selección y del *collider* causal (conecta con [[arena-h17]], condicionar en un collider abre caminos espurios).
- **Valor esperado por estados ↔ programación dinámica:** plantear $E_0,E_1,\ldots$ y resolver el sistema es backward induction, idéntico a la recurrencia de un DP (conecta con [[arena-cc3]]).
- **Triángulo del palo roto ↔ probabilidad geométrica:** "longitudes aleatorias" → dibuja el espacio muestral como región y compara áreas (conecta con [[arena-fc2]]).

Moraleja de la arista: *no preguntes "cuántos casos hay" sino "qué me dijo la observación"; quien revela con información reescribe el espacio de estados.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Prueba positiva, ¿qué probabilidad?" | Bayes con tasa base: prevalencia $\times$ sensibilidad $/\,P(+)$ |
| "El anfitrión abre una puerta" | Monty Hall: cambia → $P=\tfrac23$ |
| "¿Puedes formar un triángulo?" | Geometría del espacio de muestras |
| "¿Cuántos lanzamientos hasta $k$ seguidos?" | Sistema de ecuaciones de estado → $E=\sum 2^i$ |
| "¿Giras el tambor?" | Condiciona en haber sobrevivido y cuenta estados válidos |
| "Distribuir entre frascos para maximizar $P$" | Un frasco con certeza, el otro con máxima proporción |

---

> **Síntesis:** La probabilidad en entrevistas quant mide si ves la condición correcta. Monty Hall, Bayes y ruleta rusa fallan si calculas sin condicionar bien. El árbol de probabilidad siempre es tu aliado.

---

*Retrieval: sin mirar, calcula: (1) $P(E\mid +)$ con prevalencia $1\%$, sensibilidad $95\%$, FP$=10\%$; (2) $E[\text{lanzamientos para 2 caras seguidas}]$; (3) la optimización del frasco.*
