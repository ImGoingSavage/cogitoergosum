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
