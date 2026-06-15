# Arena Quant · Brainteasers: lógica, inducción y juegos

Estos acertijos prueban razonamiento deductivo y estrategia. La herramienta dominante es la **inducción** (empieza con 1, con 2, con 3… y ve el patrón) y el **análisis hacia atrás** en juegos (¿qué posición es perdedora?).

## Inducción: empieza por el caso cero

- **n leones, un trozo de carne; el que come se duerme y se vuelve presa. ¿Qué pasa?** 0 leones: nada. 1 león: come (nadie lo amenaza). 2 leones: nadie come (comer te vuelve presa del otro, que ya no tiene rival). 3: el más cercano come (sabe que con 2 nadie comería). Patrón: **par → nadie come; impar → uno come**.
- **50 isleños lógicos de ojos azules/marrones; quien deduzca que tiene ojos azules se va a medianoche. Un forastero dice "al menos uno tiene ojos azules". ¿Qué pasa?** Inducción: si n personas tienen ojos azules, todas se van la **n-ésima noche**. Con n=1 es inmediato; cada nivel espera ver si el anterior se fue. El forastero aporta *conocimiento común*, no información nueva.

## Pesadas: tres resultados por pesada

- **9 canicas, una más pesada; báscula de platillos, máximo 3 pesadas. ¿Cómo hallar la pesada?** Cada pesada tiene **tres** resultados (izquierda, derecha, equilibrio), no dos. Pesa 3 contra 3 dejando 3 fuera → identifica el grupo de 3 → pesa 1 contra 1. Solo **2 pesadas** (⌈log₃9⌉ = 2). El error es pensar en binario (dividir en mitades).

## Juegos: encuentra las posiciones perdedoras

- **Nim simple: n cerillas, tomas 1, 2 o 3 por turno; quien toma la última pierde.** Trabaja hacia atrás: dejar **1** al rival lo hace perder; en general, deja un múltiplo de 4 más 1 (deja 4j+1). Si "el que toma la última gana", deja 4j. Siempre respondes a la jugada x del rival con 4−x.
- **Monedas en una mesa redonda: por turnos colocáis monedas sin solapar; pierde quien no pueda. ¿Estrategia?** Ve **primero**: pon una moneda en el centro exacto y luego juega siempre el reflejo de tu rival respecto al centro. La simetría garantiza que siempre tengas respuesta.

## Lógica pura

- **Cuatro cartas muestran 7, 6, A, C. Regla: "si hay vocal en un lado, hay número par en el otro". ¿Cuáles giras?** Solo las que pueden *falsar* la regla: la **A** (vocal → verifica que detrás haya par) y el **7** (impar → verifica que detrás no haya vocal). No giras 6 ni C (la regla no dice nada sobre ellas). Es la tarea de selección de Wason: comprueba P→Q girando P y ¬Q.
- **Rectángulo pequeño dentro de uno grande; con una sola recta, divide en dos partes iguales el área del grande que NO está cubierta por el pequeño.** Cualquier recta por el centro de un rectángulo lo biseca. Traza la recta que pasa por **ambos centros**: biseca el grande y el pequeño, luego también la diferencia.

## Estrategia distribuida

- **22 presos, 2 interruptores en una sala; entran al azar uno a uno; deben afirmar (sin error) cuando todos hayan entrado.** Elige un **capitán contador**: los demás suben un interruptor solo la primera vez que lo ven abajo; el capitán cuenta cada vez que lo encuentra arriba y lo baja. Al llegar a 21, todos han entrado. Es el patrón canónico de comunicación con un canal mínimo.

## Mini-ejemplo trabajado: Nim resuelto hacia atrás

n cerillas; tomas 1, 2 o 3 por turno; **quien toma la última pierde**. Etiqueta cada posición como P (perdedora para quien va a mover) o N (ganadora). Trabaja hacia atrás:

- Dejar **1** al rival: lo obligas a tomarla y pierde → posición "1 cerilla restante, turno rival" es **N para ti**.
- Generaliza: las posiciones perdedoras para quien mueve son **4j+1** (1, 5, 9, 13, …). Desde cualquier otra puedes llevar al rival a un 4j+1.

Estrategia: deja **4j+1** y luego responde a cada jugada x del rival con **4−x** (así cada ronda completa retira 4). Con 13 cerillas ya estás en 4·3+1 → si mueves primero, pierdes con juego óptimo; conviene ir segundo.

**Predicción antes de seguir:** si cambiamos la regla a "quien toma la última **gana**", ¿qué posiciones dejas? Respuesta: múltiplos de 4 (**4j**). El análisis hacia atrás es idéntico; solo se desplaza el ancla porque el caso base se invierte. Cambiar quién gana en la última jugada recalibra todo el patrón.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "juego por turnos, ¿quién gana?" → identifica posiciones perdedoras trabajando hacia atrás desde el final.
- **Contraejemplo (pensar en binario):** con 9 canicas y una más pesada, dividir en mitades sugiere ⌈log₂9⌉=4 pesadas. Falso: la balanza da **tres** resultados (izq/der/equilibrio), así que bastan ⌈log₃9⌉=2. El canal tiene 3 salidas, no 2.
- **Caso borde (ojos azules):** el forastero dice algo que los 50 "ya sabían"… pero crea **conocimiento común**, y eso dispara la cascada inductiva en la n-ésima noche. El borde revela la diferencia entre "saber" y "saber que todos saben".

## Errores típicos

- **Conceptual:** confundir información nueva con conocimiento común (el forastero no aporta un hecho, aporta que el hecho es público).
- **Técnico:** modelar la balanza como binaria (log₂) en vez de ternaria (log₃); sobreestima las pesadas.
- **De interpretación:** en Wason, girar la carta que *confirma* (el 6, par) en vez de la que puede *falsar* (el 7, impar); solo P y ¬Q falsan P→Q.

## Transferencia isomorfa

- **Inducción desde el caso base ↔ recursión / DP:** "resuelve n=0,1,2 y sube" es exactamente cómo se construye una solución por programación dinámica desde los subproblemas (conecta con [[arena-cc3]]).
- **Análisis hacia atrás en juegos ↔ parada óptima / minimax:** etiquetar posiciones P/N desde el final es la misma backward induction que valora un juego o una opción americana (conecta con [[arena-q8]]).
- **Tres resultados por pesada ↔ entropía / cota de información:** ⌈log₃ n⌉ es una cota de teoría de información: cada pesada extrae a lo sumo log₂3 bits; el límite del canal fija el mínimo de pruebas.
- **Wason (gira P y ¬Q) ↔ falsación y casos de prueba:** buscar el caso que *rompe* la regla, no el que la confirma, es el principio de diseñar tests por contraejemplo y de la contrapositiva.
- **Estrategia de simetría (centro + reflejo) ↔ invariante:** reflejar la jugada del rival mantiene una invariante de simetría que garantiza respuesta (conecta con [[arena-q3]], invariantes).

Moraleja de la arista: *para un juego, pinta las posiciones perdedoras desde el final; para un acertijo de agentes, empieza en n=0 y sube; y desconfía del binario cuando el canal tiene tres salidas.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "n agentes, ¿qué pasa?" | inducción desde 0/1/2; busca paridad |
| "ojos azules / sabios" | inducción por niveles; conocimiento común |
| "báscula de platillos" | tres resultados por pesada → log₃ |
| "juego por turnos, quién gana" | hacia atrás: identifica posiciones perdedoras (4j+1) |
| "mesa simétrica / tablero" | estrategia de simetría (centro + reflejo) |
| "si vocal entonces par" | Wason: gira P y ¬Q |

> ❧ **Síntesis:** la lógica de entrevista se desarma con inducción (empieza en cero y sube) y con análisis hacia atrás en juegos (¿qué le dejo al rival para que pierda?). La báscula tiene tres salidas, no dos; y la simetría convierte un juego espacial en una respuesta automática.

---

*Retrieval: cierra la página y responde — (1) leones: ¿par o impar come?; (2) pesadas para hallar 1 entre 9; (3) qué cartas giras en Wason (7,6,A,C); (4) cuántas cerillas dejar en Nim para ganar.*
