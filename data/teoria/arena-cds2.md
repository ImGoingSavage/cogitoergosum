# Deep learning: redes neuronales por dentro

## De qué trata esta lección (y qué sabrás hacer al final)

Una red neuronal parece una caja negra, pero por dentro es sorprendentemente simple: cada neurona suma entradas por pesos, añade un sesgo y aplica una función que la "dobla". Esta lección abre esa caja desde cero: qué hace a una red "profunda", qué pasa exactamente en una neurona, por qué la **no-linealidad** es lo único que justifica apilar capas, cómo aprende (descenso de gradiente + **backpropagation**) y por qué las redes muy profundas sufren el **gradiente que se desvanece**.

Al terminar podrás: (1) explicar por qué sin activación no-lineal una red de 100 capas colapsa a un modelo lineal; (2) describir qué calcula backprop y con qué regla matemática; (3) reconocer y mitigar el vanishing/exploding gradient; y (4) elegir la activación correcta para una salida binaria, multiclase o una capa oculta. La intuición primero; la fórmula, solo cuando ayuda.

---

## Qué hace "profunda" a una red

Una red neuronal estándar tiene una o dos capas ocultas; una red de **deep learning** tiene decenas, cientos o miles. Esa profundidad le permite aprender **representaciones jerárquicas**: en visión, las primeras capas detectan bordes, las siguientes formas, las últimas objetos completos. Por eso domina visión, voz y lenguaje, donde el ML tradicional batalla. La ventaja decisiva: **aprende las features sola** (*feature learning*), sin que un humano las diseñe a mano — justo lo contrario del feature engineering manual.

## Anatomía de una neurona: pesos, sesgos, activación

Una neurona hace un "forward pass" en cinco pasos:

1. Cada entrada se multiplica por su **peso** (la fuerza de esa conexión).
2. Se **suman** todos los productos.
3. Se añade el **sesgo** (bias), una constante que desplaza el resultado y da flexibilidad (sin él, la neurona siempre pasaría por el origen).
4. Se aplica una **función de activación** (la no-linealidad).
5. La salida alimenta la siguiente neurona.

Los pesos y sesgos arrancan en valores aleatorios pequeños y se **ajustan durante el entrenamiento**: ahí, y solo ahí, está el "aprendizaje". Entrenar una red *es* encontrar los pesos que minimizan el error.

## Funciones de activación: el porqué de la no-linealidad

Esta es la idea central de toda la lección. Sin una activación **no-lineal** entre capas, apilar capas equivale a **una sola transformación lineal**: la red no podría representar patrones que se tuercen (una frontera curva). La activación es lo que "infunde vida" a la profundidad.

| Función | Rango | Uso típico |
|---------|-------|-----------|
| **Step** (escalón) | {0,1} | conceptual; decisión dura |
| **Sigmoide** | (0,1) | salida de clasificación **binaria** (probabilidades) |
| **Tanh** | (−1,1) | capas ocultas |
| **ReLU** | [0,∞) | capas ocultas de DNN; mitiga el gradiente que se desvanece |
| **Leaky ReLU** | ~ReLU | evita "dying ReLU" (gradiente no-cero en negativos) |
| **Softmax** | suma 1 | salida **multiclase** (probabilidades que suman 1) |

Regla rápida para la entrevista: salida **binaria** → sigmoide; salida **multiclase** → softmax; **capas ocultas** profundas → ReLU (porque su derivada no se satura en positivos).

## Backpropagation y descenso de gradiente

¿Cómo se ajustan los pesos? Dos piezas que trabajan juntas:

- **Descenso de gradiente:** la red predice → una **función de pérdida** mide cuán lejos quedó del objetivo → se mueven los pesos un poquito en la dirección que reduce el error → se repite. Busca el **mínimo** de la pérdida, pero en una red (no convexa) puede atascarse en un mínimo local.
- **Backpropagation** ("propagación hacia atrás del error"): para saber *cuánto* mover cada peso necesitas el gradiente, y backprop lo calcula usando la **regla de la cadena**, capa por capa desde la salida hacia la entrada. Atribuye a cada peso su parte de culpa en el error. El ciclo completo: pérdida → backprop (gradiente) → actualizar pesos → repetir.

## Gradiente que se desvanece (y que explota)

Aquí está el gran problema de las redes profundas, y sale directo de la mecánica de backprop. Como el gradiente se calcula **multiplicando** derivadas capa tras capa, si esas derivadas son pequeñas (sigmoide y tanh **saturan**: su derivada es ≤ 0.25), el producto **se encoge exponencialmente** al llegar a las primeras capas → casi no se actualizan → el aprendizaje se vuelve lentísimo o se detiene. Es el **vanishing gradient problem**, severo en RNNs y redes muy profundas.

Su gemelo, el **exploding gradient**, es lo opuesto: derivadas grandes multiplicadas dan actualizaciones enormes, inestabilidad numérica (NaNs) y no converge.

Mitigaciones:
- **ReLU** en lugar de sigmoide/tanh (su derivada vale 1 en positivos, no satura).
- **Gradient clipping** (recortar el gradiente por valor o por norma) contra la explosión.
- Inicialización cuidadosa: **Glorot/Xavier** (con tanh/sigmoide/softmax) o **He** (con ReLU).
- Conexiones de salto (*skip connections*), que dan al gradiente un atajo hacia las capas tempranas.

## Arquitecturas y transfer learning

- **CNN** (convolucionales): imágenes/visión; explotan que píxeles vecinos están relacionados.
- **RNN** (recurrentes): secuencias y series de tiempo; especialmente golpeadas por el vanishing gradient.
- **Transfer learning:** reusar una red ya entrenada (p. ej. BERT) y **afinarla** a una tarea nueva con pocos datos — práctico cuando recolectar datos es caro, porque heredas las representaciones ya aprendidas.

---

## Mini-ejemplo trabajado: por qué sin activación no-lineal la red colapsa

Apila dos capas lineales: h = W₁x, y = W₂h = W₂W₁x. El producto W₂W₁ es **otra matriz**, así que dos capas lineales equivalen a **una sola** transformación lineal. Añade 100 capas: sigue siendo lineal. Sin una no-linealidad entre capas, la profundidad no compra nada — la red no puede doblar la frontera de decisión.

Mete una ReLU entre capas: y = W₂·max(0, W₁x). Ahora cada neurona aporta un "doblez" y la composición genera fronteras arbitrariamente complejas. La activación no es un adorno: es lo que convierte "muchas capas" en "función expresiva".

**Predicción antes de seguir:** en una red muy profunda con sigmoides, ¿por qué las primeras capas aprenden lentísimo? Respuesta: backprop multiplica derivadas capa por capa, y la sigmoide satura (derivada ≤ 0.25). Multiplicar muchos números <1 hace que el gradiente **se desvanezca exponencialmente** hacia las capas tempranas → casi no se actualizan. Es el mismo fenómeno que multiplicar muchas probabilidades pequeñas y obtener casi cero; por eso se trabaja en log y se usa ReLU (derivada 1 en positivos).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** capa oculta profunda → ReLU (no satura en positivos); salida binaria → sigmoide; multiclase → softmax.
- **Contraejemplo (más capas sin no-linealidad):** apilar capas lineales no aumenta la capacidad; parece "más profundo" pero es un modelo lineal disfrazado.
- **Caso borde (exploding gradient):** el gemelo del vanishing — derivadas grandes multiplicadas dan actualizaciones enormes, NaNs; se corta con gradient clipping.

## Errores típicos

- **Conceptual:** creer que profundidad por sí sola da expresividad (sin activación no-lineal, no).
- **Técnico:** usar sigmoide/tanh en capas ocultas profundas y sufrir vanishing gradient; o mala inicialización (He para ReLU, Glorot para tanh).
- **De interpretación:** leer la salida de una sigmoide como probabilidad calibrada sin verificar calibración.

## Transferencia isomorfa

- **Descenso de gradiente ↔ optimización del MLE:** entrenar minimizando la pérdida es maximizar la log-verosimilitud por gradiente; la log-loss *es* el MLE de Bernoulli (conecta con [[arena-dg2]]).
- **Sigmoide de salida ↔ regresión logística:** la última capa con sigmoide es exactamente un modelo logístico sobre las features aprendidas (conecta con [[arena-isl2]]).
- **Vanishing gradient ↔ producto de números pequeños:** multiplicar derivadas <1 colapsa igual que multiplicar verosimilitudes pequeñas; por eso log-espacio y ReLU (conecta con [[arena-cb3]], log-verosimilitud).
- **Backprop (regla de la cadena) ↔ delta method:** ambos propagan una perturbación por derivadas encadenadas; uno hacia atrás en una red, otro a través de una transformación g (conecta con [[arena-cb4]]).

Moraleja de la arista: *la no-linealidad es lo que hace que apilar capas valga la pena; y multiplicar muchas derivadas pequeñas desvanece el gradiente, como multiplicar probabilidades desvanece la verosimilitud.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Salida = probabilidad binaria" | Sigmoide en la capa final |
| "Clasificación multiclase" | Softmax (suma 1) |
| "Capa oculta de red profunda" | ReLU (evita saturación) |
| "Red profunda aprende lentísimo en capas tempranas" | Vanishing gradient → ReLU + buena init |
| "Pérdida diverge, valores NaN" | Exploding gradient → gradient clipping |
| "Imágenes" / "secuencias" | CNN / RNN |
| "Pocos datos, tarea nueva" | Transfer learning desde modelo pre-entrenado |
| "Init de pesos con ReLU vs tanh" | He vs Glorot/Xavier |

---

> **Síntesis:** Una red profunda apila muchas capas para aprender representaciones jerárquicas y sus propias features. Cada neurona suma entradas×pesos + sesgo y aplica una activación **no-lineal** (sin ella, la red colapsa a un modelo lineal): sigmoide/softmax en salidas binarias/multiclase, ReLU en capas ocultas. Aprende vía descenso de gradiente, calculando con **backpropagation** (regla de la cadena) cuánto contribuyó cada peso al error. El riesgo en redes profundas es el **gradiente que se desvanece/explota**, que se mitiga con ReLU, gradient clipping e inicialización Glorot/He.

---

*Retrieval: cierra y responde: (1) ¿por qué la activación debe ser no-lineal?; (2) ¿qué calcula backpropagation y con qué regla matemática?; (3) describe el vanishing gradient y dos mitigaciones; (4) ¿qué activación usas para salida binaria, multiclase y capa oculta?*
