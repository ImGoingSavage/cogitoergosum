# Conductual II: fracaso, errores, ambigüedad y feedback (STAR)

> Estas preguntas evalúan **autoconciencia, honestidad y aprendizaje**, no la ausencia de errores. Usa narrativa-star y centra la respuesta en el **aprendizaje aplicado**.

## De qué trata esta lección (y qué sabrás hacer al final)

Las preguntas de fracaso, error y "no sé" parecen trampas, pero miden algo concreto: **autoconciencia, honestidad y capacidad de aprender** — no la ausencia de errores. La peor respuesta finge que nunca fallaste; la mejor muestra qué cambiaste en tu proceso después. Esta lección construye, desde cero, cómo contar un fracaso, navegar la ambigüedad y manejar el feedback con STAR.

Al terminar podrás: (1) elegir un fracaso **real** y con consecuencias, asumir la responsabilidad y centrar la respuesta en el **cambio de proceso** que aplicaste; (2) responder a la ambigüedad descomponiendo y declarando supuestos explícitos; (3) detectar un plazo en riesgo y avisar a tiempo; y (4) recibir feedback sin defenderte y responder "no sé" con integridad, mostrando el método. Conecta con [[arena-c1]] (estructura STAR) y con la Constitución del proyecto: el error es parte del proceso.

---

## Fracaso y errores

Elige un caso **real** y con consecuencias (ni trivial ni imprudente). **Asume la responsabilidad** sin culpar, narra brevemente qué salió mal y **por qué**, y dedica el grueso al **aprendizaje** y al **cambio concreto** que aplicaste después (cómo evitas que se repita). Señales fuertes: ownership, causa raíz, reflexión y evidencia de que la lección 'pegó'. Ver responder-fracaso-star.

> El cap. 13 del libro ("When your data science project fails") normaliza el fracaso: lo valioso es la lección y el cambio de proceso (validar supuestos, añadir tests/monitoreo, comunicar antes con el negocio).

## Ambigüedad y plazos

- **Ambigüedad:** descompón, haz **supuestos explícitos**, empieza con un análisis exploratorio pequeño y **comunica** para alinear. No te paralices ni avances a ciegas.
- **Plazo incumplido:** detecta el riesgo y **avisa temprano**, mitiga (re-prioriza, pide ayuda, recorta alcance) y mejora tu **estimación/planeación** después.

## Feedback y "no sé"

- **Crítica/feedback:** escucha sin defenderte, pide ejemplos, implementa el cambio y demuéstralo. Evita el falso defecto ("soy perfeccionista").
- **"No sé":** admítelo con integridad y explica **cómo lo averiguarías** (consejo del libro: está bien no saber; muestra el método). No inventes.

---

## Mini-ejemplo trabajado: un esqueleto STAR de fracaso

"Cuéntame de un proyecto que fracasó." El valor está en la lección, no en el desastre:

- **Situación (1 frase):** lancé un modelo a producción confiando en que los datos de entrenamiento y los de producción coincidían.
- **Tarea:** era mi entrega; yo respondía por que funcionara.
- **Acción:** falló de forma silenciosa por un cambio de distribución; hice **causa raíz**, lo comuniqué pronto al negocio y añadí un test de validación de supuestos y una alerta de drift.
- **Resultado (el grueso):** lo corregí, pero lo importante es que el cambio de proceso **pegó**: en los proyectos siguientes valido supuestos y monitoreo antes de lanzar. El fracaso me dio un hábito.

El reparto se invierte respecto a otras respuestas: aquí el peso va al **aprendizaje aplicado**, no a la Acción.

**Predicción antes de seguir:** te preguntan "¿tu mayor debilidad?" y respondes "soy demasiado perfeccionista". ¿Suma o resta? **Resta**: el falso defecto se detecta al instante y señala falta de autoconciencia. Un defecto real con un cambio concreto ("tendía a no pedir ayuda a tiempo; ahora fijo un punto de control donde reviso si debo escalar") es mucho más fuerte.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** fracaso real con consecuencias + ownership (sin culpar) + la lección y el cambio de proceso que aplicaste después → respuesta fuerte.
- **Contraejemplo (parece buena, falla):** el falso defecto ("perfeccionista"), un fracaso trivial sin consecuencias, o echarle la culpa al equipo/al cliente. Cumplen el formato pero no muestran aprendizaje.
- **Caso borde:** "no sé la respuesta". Lo más fuerte no es inventar, sino admitirlo y explicar **cómo lo averiguarías** — el método vale más que una respuesta fabricada que se desmorona a la primera repregunta.

## Errores típicos

- **Conceptual:** el falso defecto ("soy perfeccionista") en vez de un error real con aprendizaje; el entrevistador lo detecta al instante.
- **De honestidad:** inventar una respuesta ante "no sé" en lugar de admitirlo y explicar **cómo lo averiguarías**.
- **De interpretación:** elegir un fracaso trivial (sin consecuencias) o uno imprudente (que revela mal juicio); el punto es la lección, no la ausencia de errores.

## Transferencia isomorfa

Estas preguntas premian la misma postura que la Constitución de CogitoErgoSum: **el error es parte del proceso**.

- **Fracaso → aprendizaje aplicado ↔ productive struggle:** narrar qué cambiaste tras fallar es el mismo "el amor es al proceso de pensar, no al resultado"; un fracaso sin cambio de proceso no enseña.
- **Ambigüedad → supuestos explícitos ↔ plantilla de diseño / target trial:** descomponer y declarar supuestos antes de avanzar es lo que hace la plantilla antes de proponer arquitectura, o los 7 componentes antes de analizar datos (conecta con [[arena-s1]] y [[arena-h2]]).
- **"No sé, así lo averiguaría" ↔ método socrático:** mostrar el método de búsqueda en vez de la respuesta es exactamente lo que entrena la mentoría socrática.
- **Plazo en riesgo → avisar temprano ↔ monitoreo y alertas:** detectar la desviación y comunicarla pronto es el mismo reflejo que una alarma de drift antes de que el daño crezca (conecta con [[arena-cds3]]).

Moraleja de la arista: *un fracaso vale por la lección que cambió tu proceso; admitir "no sé" con un método es más fuerte que inventar una respuesta.*

---

## Disparadores

| Pregunta | Jugada |
|----------|--------|
| "Un proyecto que fracasó" | Caso real + ownership + APRENDIZAJE aplicado |
| "Tu mayor error" | Asúmelo, mitiga, cambia el proceso (no culpes) |
| "Trabajar con ambigüedad" | Descomponer + supuestos explícitos + iterar/comunicar |
| "No cumpliste un plazo" | Avisar temprano + mitigar + mejorar la planeación |
| "No sabías la respuesta" | Admítelo + di cómo lo averiguarías |

---

> **Síntesis:** en fracasos/errores, elige un caso real, **asume responsabilidad** y enfócate en el **aprendizaje y el cambio aplicado**. Ante la **ambigüedad**, estructura, supone explícitamente y comunica; ante un **plazo** en riesgo, avisa pronto y mejora tu planeación. Recibe el **feedback** sin defenderte y acciónalo; si **no sabes**, dilo y explica cómo lo resolverías. Evita el falso defecto y echar culpas.

---

*Retrieval: (1) ¿qué debe dominar una respuesta de fracaso?; (2) ¿cómo se maneja la ambigüedad?; (3) ¿qué hacer ante un plazo en riesgo?; (4) ¿cómo respondes "no sé" bien?*
