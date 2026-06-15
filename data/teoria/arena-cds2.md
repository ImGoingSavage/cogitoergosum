# Deep learning: redes neuronales por dentro

## Qué hace "profunda" a una red

Una red neuronal (NN) estándar tiene una o dos capas ocultas; una de **deep learning** tiene decenas, cientos o miles. Esa profundidad permite aprender **representaciones jerárquicas** de los datos: bordes → formas → objetos. Por eso domina visión, voz y lenguaje, donde la ML tradicional batalla. Ventaja clave: **aprende las features sola** (feature learning), sin ingeniería manual.

## Anatomía de una neurona: pesos, sesgos, activación

Un "forward pass" en un nodo:
1. Cada entrada se multiplica por su **peso** (fuerza de la conexión).
2. Se suman los productos.
3. Se añade el **sesgo** (bias) — constante que desplaza el resultado, da flexibilidad.
4. Se aplica una **función de activación**.
5. La salida alimenta la siguiente neurona.

Pesos y sesgos arrancan en valores aleatorios pequeños y se **ajustan durante el entrenamiento**. Ahí está el aprendizaje.

## Funciones de activación: el porqué de la no-linealidad

Sin activación no-lineal, apilar capas equivale a **una sola transformación lineal**: la red no podría capturar patrones que se tuercen. La activación "infunde vida".

| Función | Rango | Uso típico |
|---------|-------|-----------|
| **Step** (escalón) | {0,1} | conceptual; decisión dura |
| **Sigmoide** | (0,1) | salida de clasificación **binaria** (probabilidades) |
| **Tanh** | (−1,1) | capas ocultas |
| **ReLU** | [0,∞) | capas ocultas de DNN; mitiga gradiente que se desvanece |
| **Leaky ReLU** | ~ReLU | evita "dying ReLU" (gradiente no-cero en negativos) |
| **Softmax** | suma 1 | salida **multiclase** (probabilidades que suman 1) |

Regla rápida: binaria → sigmoide; multiclase → softmax; capas ocultas profundas → ReLU.

## Backpropagation y descenso de gradiente

- **Descenso de gradiente:** predice → mide el error con una **función de pérdida** → ajusta los pesos un poquito en la dirección que reduce el error → repite. Busca el **mínimo global** de la pérdida, pero puede atascarse en un **mínimo local**.
- **Backpropagation** ("propagación hacia atrás del error"): usa la **regla de la cadena** para calcular, capa por capa desde la salida, cuánto contribuyó cada peso al error. Ese gradiente alimenta al descenso de gradiente. Pérdida → backprop → gradiente → actualizar pesos.

## Gradiente que se desvanece (y que explota)

En redes muy profundas, al multiplicar derivadas pequeñas capa tras capa (sigmoide/tanh saturan), el gradiente **se encoge exponencialmente** hacia las primeras capas → aprendizaje lento o detenido. Es el **vanishing gradient problem**, severo en RNNs y redes muy profundas.

Su gemelo, **exploding gradient**, multiplica derivadas grandes → actualizaciones enormes, inestabilidad numérica, no converge.

Mitigaciones:
- **ReLU** en lugar de sigmoide/tanh (su derivada no satura en positivos).
- **Gradient clipping** (recortar el gradiente por valor o por norma) contra la explosión.
- Inicialización cuidadosa: **Glorot/Xavier** (con tanh/sigmoide/softmax) o **He** (con ReLU).
- Conexiones de salto (skip connections).

## Arquitecturas y transfer learning

- **CNN** (convolucionales): imágenes/visión.
- **RNN** (recurrentes): secuencias y series de tiempo; especialmente afectadas por vanishing gradient.
- **Transfer learning:** reusar una red pre-entrenada (p.ej. BERT) y afinarla a una tarea nueva con pocos datos — práctico cuando recolectar datos es caro.

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
