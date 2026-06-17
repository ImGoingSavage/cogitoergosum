# Arena Quant · Brainteasers: lógica, inducción y juegos

## De qué trata (y qué sabrás hacer)

Estos acertijos prueban razonamiento deductivo y estrategia, no cálculo. Dos herramientas dominan: la **inducción** (resuelve el caso con 0, con 1, con 2… y descubre el patrón) y el **análisis hacia atrás** en juegos (¿qué posición deja perdiendo al rival?). El reflejo a entrenar es no atacar el caso grande de frente, sino construirlo desde el más pequeño.

Al terminar sabrás montar argumentos inductivos, identificar posiciones ganadoras/perdedoras desde el final, contar con un canal de tres salidas (la balanza), y reconocer la tarea de Wason (falsar, no confirmar). Cada idea se construye desde su caso base.

---

## Inducción: empieza por el caso cero

- **$n$ leones y un trozo de carne; el que come se duerme y se vuelve presa indefenso. ¿Qué pasa?** Sube desde abajo: con 1 león, come (nadie lo amenaza). Con 2, **nadie** come (el que comiera quedaría a merced del otro). Con 3, el más cercano come (sabe que tras él quedan 2, y con 2 nadie come). Patrón: **par → nadie come; impar → uno come**.
- **Isleños lógicos de ojos azules; quien deduce que los suyos son azules se va esa noche. Un forastero anuncia "al menos uno tiene ojos azules". ¿Qué pasa?** Por inducción, si hay $n$ de ojos azules, todos se van la **$n$-ésima noche**. El forastero no aporta un hecho nuevo (todos veían ojos azules) sino **conocimiento común** —"todos saben que todos saben"—, y eso dispara la cascada.

---

## Pesadas: tres resultados por pesada

**9 canicas, una más pesada; balanza de platillos, máximo 3 pesadas. ¿Cómo hallarla?** Cada pesada tiene **tres** desenlaces (izquierda baja, derecha baja, equilibrio), no dos. Pesa 3 contra 3 dejando 3 fuera: identificas el grupo de 3 que la contiene; luego 1 contra 1. Bastan $\lceil\log_3 9\rceil=2$ pesadas. Pensar en binario (mitades, $\log_2$) sobreestima: el canal tiene 3 salidas.

---

## Juegos: encuentra las posiciones perdedoras

- **Nim simple: $n$ cerillas, tomas 1, 2 o 3 por turno; quien toma la última pierde.** Hacia atrás: dejar **1** al rival lo condena. En general, deja $4j+1$ cerillas (1, 5, 9, …); luego responde a cada jugada $x$ del rival con $4-x$, de modo que cada ronda completa retira 4. Si la regla fuera "quien toma la última **gana**", dejarías múltiplos de 4.
- **Monedas en una mesa redonda: por turnos colocáis monedas sin solapar; pierde quien no pueda jugar.** Ve **primero**: coloca una moneda en el centro exacto y luego juega siempre el reflejo de la jugada del rival respecto al centro. La simetría te garantiza respuesta mientras el rival la tenga.

---

## Lógica pura

- **Cuatro cartas muestran 7, 6, A, C. Regla: "si hay vocal en un lado, hay número par en el otro". ¿Cuáles giras?** Solo las que pueden **falsar** la regla: la **A** (vocal → comprueba que detrás haya par) y el **7** (impar → comprueba que detrás no haya vocal). No giras la 6 ni la C. Es la tarea de selección de Wason: para verificar $P\Rightarrow Q$ giras $P$ y $\neg Q$, nunca el que solo confirma.
- **Rectángulo pequeño dentro de uno grande; con una sola recta divide en dos áreas iguales la parte del grande NO cubierta por el pequeño.** Cualquier recta por el centro de un rectángulo lo biseca. Traza la que pasa por **ambos** centros: biseca el grande y el pequeño, luego también su diferencia.

---

## Estrategia distribuida

**22 presos, una sala con 2 interruptores; entran de uno en uno al azar (repitiéndose); deben afirmar sin error cuando todos hayan entrado al menos una vez.** Elige un **capitán contador**: cada otro preso sube el interruptor designado solo la **primera** vez que lo encuentra abajo; el capitán lo baja y cuenta. Al contar 21 subidas, sabe que los 21 restantes ya pasaron. Es el patrón canónico de comunicar con un canal mínimo y memoria distribuida.

---

## Mini-ejemplo trabajado: Nim resuelto hacia atrás

$n$ cerillas; tomas 1, 2 o 3 por turno; **quien toma la última pierde**. Etiqueta cada posición como P (perdedora para quien va a mover) o N (ganadora). Trabaja hacia atrás:

- Dejar **1** al rival: lo obligas a tomarla y pierde → estar a punto de dejarle 1 es bueno para ti.
- Generaliza: las posiciones perdedoras para quien mueve son $4j+1$ (1, 5, 9, 13, …). Desde cualquier otra, puedes llevar al rival a un $4j+1$.

Estrategia: deja $4j+1$ y luego responde a cada jugada $x$ del rival con $4-x$ (cada ronda completa retira 4). Con 13 cerillas ya estás en $4\cdot3+1$ → si mueves primero pierdes con juego óptimo; conviene ir segundo.

**Predicción antes de seguir:** si la regla cambia a "quien toma la última **gana**", ¿qué posiciones dejas? Respuesta: múltiplos de 4 ($4j$). El análisis hacia atrás es idéntico; solo se desplaza el ancla porque el caso base se invierte. Cambiar quién gana en la última jugada recalibra todo el patrón.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "juego por turnos, ¿quién gana?" → identifica posiciones perdedoras trabajando hacia atrás desde el final.
- **Contraejemplo (pensar en binario):** con 9 canicas y una más pesada, dividir en mitades sugiere $\lceil\log_2 9\rceil=4$ pesadas. Falso: la balanza da **tres** resultados, así que bastan $\lceil\log_3 9\rceil=2$. El canal tiene 3 salidas, no 2.
- **Caso borde (ojos azules):** el forastero dice algo que los isleños "ya sabían"… pero crea **conocimiento común**, y eso dispara la cascada inductiva en la $n$-ésima noche. El borde revela la diferencia entre "saber" y "saber que todos saben".

## Errores típicos

- **Conceptual:** confundir información nueva con conocimiento común (el forastero no aporta un hecho, aporta que el hecho es público).
- **Técnico:** modelar la balanza como binaria ($\log_2$) en vez de ternaria ($\log_3$); sobreestima las pesadas.
- **De interpretación:** en Wason, girar la carta que *confirma* (la 6, par) en vez de la que puede *falsar* (el 7, impar); solo $P$ y $\neg Q$ falsan $P\Rightarrow Q$.

## Transferencia isomorfa

- **Inducción desde el caso base ↔ recursión / DP:** "resuelve $n=0,1,2$ y sube" es exactamente cómo se construye una solución por programación dinámica desde los subproblemas (conecta con [[arena-cc3]]).
- **Análisis hacia atrás en juegos ↔ parada óptima / minimax:** etiquetar posiciones P/N desde el final es la misma backward induction que valora un juego o una opción americana (conecta con [[arena-q8]]).
- **Tres resultados por pesada ↔ entropía / cota de información:** $\lceil\log_3 n\rceil$ es una cota de teoría de información: cada pesada extrae a lo sumo $\log_2 3$ bits (conecta con [[arena-p1]]).
- **Wason (gira $P$ y $\neg Q$) ↔ falsación y casos de prueba:** buscar el caso que *rompe* la regla, no el que la confirma, es el principio de diseñar tests por contraejemplo.
- **Estrategia de simetría (centro + reflejo) ↔ invariante:** reflejar la jugada del rival mantiene una invariante de simetría que garantiza respuesta (conecta con [[arena-q12]]).

Moraleja de la arista: *para un juego, pinta las posiciones perdedoras desde el final; para un acertijo de agentes, empieza en $n=0$ y sube; y desconfía del binario cuando el canal tiene tres salidas.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "$n$ agentes, ¿qué pasa?" | inducción desde 0/1/2; busca paridad |
| "ojos azules / sabios" | inducción por niveles; conocimiento común |
| "báscula de platillos" | tres resultados por pesada → $\log_3$ |
| "juego por turnos, quién gana" | hacia atrás: posiciones perdedoras ($4j+1$) |
| "mesa simétrica / tablero" | estrategia de simetría (centro + reflejo) |
| "si vocal entonces par" | Wason: gira $P$ y $\neg Q$ |

---

> ❧ **Síntesis:** la lógica de entrevista se desarma con inducción (empieza en cero y sube) y con análisis hacia atrás en juegos (¿qué le dejo al rival para que pierda?). La báscula tiene tres salidas, no dos; y la simetría convierte un juego espacial en una respuesta automática.

---

*Retrieval: cierra la página y responde — (1) leones: ¿par o impar come?; (2) pesadas para hallar 1 entre 9; (3) qué cartas giras en Wason (7,6,A,C); (4) cuántas cerillas dejar en Nim para ganar.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puentes de regreso

La logica de entrevistas recupera tecnicas de prueba clasicas: [[zeitz-23]] para contradiccion e induccion, [[engel-ind]] para fortalecer la hipotesis, [[engel-extremo]] para elegir un objeto limite, [[engel-juegos]] para posiciones ganadoras y [[engel-fun]] para reglas que se prueban por sustitucion.
<!-- GRAFO_CONEXO_OLEADA3_END -->
