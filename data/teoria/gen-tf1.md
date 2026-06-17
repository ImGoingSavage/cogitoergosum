# El problema de las secuencias y la idea de atención

> Recurso troncal: **MIT-AI.md (Semana 9)** + el paper fundacional [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762). Es la lección cero de toda la IA generativa moderna: sin entender la atención, los LLMs, el RAG y los agentes son cajas mágicas. Prepara [[gen-tf2]] (self-attention).

## De qué trata (y qué sabrás hacer al final)

Toda la IA generativa de hoy —ChatGPT, Claude, Gemini— corre sobre una sola idea con nombre: **atención**. Antes de 2017, las máquinas leían texto palabra por palabra, en orden, arrastrando una "memoria" que se desvanecía. La atención rompió esa cadena: permitió que un modelo, al producir cada palabra, **mire directamente** cualquier parte de la entrada que importe, sin importar cuán lejos esté. Esta lección construye la atención **desde el problema que resuelve**, no como una fórmula caída del cielo.

La intuición: imagina traducir un párrafo largo del alemán al español. El enfoque viejo era leer todo el párrafo, memorizarlo en tu cabeza en un solo "resumen mental", y luego escribir la traducción **sin volver a mirar el original**. Para una frase corta funciona; para un párrafo, olvidas el principio cuando llegas al final. La atención es, simplemente, **permitirte volver a mirar el texto original y enfocarte en las palabras relevantes** mientras escribes cada palabra de la traducción. Eso es todo. El resto son detalles de cómo hacerlo con matrices.

Al terminar podrás: (1) explicar el **cuello de botella** de los modelos secuencia-a-secuencia clásicos; (2) entender la **atención** como acceso ponderado y selectivo a la entrada; (3) distinguir por qué la atención **escala** donde la recurrencia falla; y (4) ubicar este salto en la historia que llevó a los Transformers.

## El mundo antes de la atención: RNN, LSTM y el cuello de botella

Para procesar una secuencia (texto, audio), durante décadas se usaron **redes recurrentes** (RNN) y su versión mejorada, las **LSTM** ([Hochreiter & Schmidhuber, 1997](https://www.bioinf.jku.at/publications/older/2604.pdf)). Procesan palabra por palabra, manteniendo un **estado oculto** $h_t$ que resume "todo lo visto hasta ahora":

$$h_t = f(h_{t-1}, x_t)$$

El modelo de traducción clásico ([Sutskever et al., 2014](https://arxiv.org/abs/1409.3215)) tenía un **encoder** que comprimía toda la frase de entrada en un **único vector** (el último estado oculto) y un **decoder** que generaba la traducción a partir de ese vector. Aquí está el pecado original: **toda la frase, por larga que sea, debe caber en un solo vector de tamaño fijo.** Es el "cuello de botella": como resumir una novela en un tuit y luego pedir que alguien la reconstruya. Cuanto más larga la frase, más información se pierde, y el desempeño se desplomaba con la longitud.

Dos problemas, entonces:
1. **Cuello de botella de información:** un vector fijo no puede representar fielmente secuencias largas.
2. **Dependencias largas y secuencialidad:** la señal del principio debe sobrevivir muchos pasos hasta el final (gradientes que se desvanecen), y el cómputo es **inherentemente secuencial** (no se puede paralelizar: $h_t$ necesita $h_{t-1}$).

## La idea de atención: deja de comprimir, aprende a mirar

La primera grieta la abrió [Bahdanau, Cho & Bengio (2015)](https://arxiv.org/abs/1409.0473). Su propuesta, en una frase: **en vez de comprimir toda la entrada en un vector, conserva todos los estados de la entrada y, al generar cada palabra de salida, calcula una mezcla ponderada de ellos** —prestando más "atención" a los relevantes—.

Formalmente, para producir la salida en el paso $i$, el modelo calcula un **vector de contexto** $c_i$ como una suma ponderada de todos los estados de entrada $h_j$:

$$c_i = \sum_j \alpha_{ij}\, h_j$$

donde los pesos $\alpha_{ij}$ (que suman 1, vía softmax) dicen **cuánta atención** pone la palabra de salida $i$ en la palabra de entrada $j$. Si traduces "die Katze" → "el gato", al generar "gato" los pesos $\alpha$ se concentran en "Katze". El modelo **aprende** esos pesos; nadie se los dicta.

Esto resuelve el cuello de botella: ya no hay un solo vector que lo cargue todo; hay acceso directo y ponderado a **toda** la entrada en cada paso. El [paper de Bahdanau](https://arxiv.org/abs/1409.0473) mostró que el desempeño dejaba de desplomarse con la longitud de la frase.

## El salto de 2017: "Attention Is All You Need"

Bahdanau usaba atención **encima** de una RNN. El paper [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) hizo la jugada radical: **quitar la recurrencia por completo** y construir el modelo **solo** con atención (y capas feed-forward). El resultado —el **Transformer**— tenía dos superpoderes:

- **Paralelización total:** sin recurrencia, todas las posiciones se procesan a la vez (clave para entrenar en GPUs con datasets gigantes → posibilitó los LLMs).
- **Caminos cortos entre palabras lejanas:** cualquier palabra puede atender a cualquier otra en **un solo paso**, sin que la señal se degrade a través de la secuencia.

Esa es la frase del título: la atención no es un complemento de la recurrencia; **es suficiente por sí sola**. Toda la lección [[gen-tf2]] desarma cómo lo hace (self-attention con Query/Key/Value).

## Mini-ejemplo trabajado: la palabra ambigua

Considera la frase: *"El **banco** estaba cerrado, así que me senté en él a esperar."* ¿"banco" es una institución financiera o un asiento? La pista ("me senté en él") está **después**. Una RNN que procesó "banco" antes de ver "me senté" tuvo que adivinar y arrastrar su decisión. Con atención, cuando el modelo representa "banco", puede **mirar hacia adelante y atrás** y ponderar fuerte la palabra "senté", resolviendo la ambigüedad. 

Predicción antes de seguir: si el modelo procesa todas las palabras **en paralelo** (sin orden), ¿cómo sabe que "senté" viene después de "banco" y no antes? → No lo sabe por sí solo; hay que **inyectar la posición** explícitamente. Ese es el tema del *positional encoding* en [[gen-tf4]]. Guarda esta tensión: ganamos paralelismo pero perdemos el orden, y hay que devolverlo.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "El modelo olvida el principio de textos largos" | Cuello de botella del vector fijo (era de RNN) |
| "Cualquier palabra debe poder influir en cualquier otra" | Necesitas atención (caminos cortos) |
| "Hay que entrenar rápido con mucho dato en GPU" | Necesitas paralelismo → quitar la recurrencia |
| "Proceso todo en paralelo pero importa el orden" | Falta positional encoding |

## Errores típicos

- **Creer que la atención es 'memoria':** no es un estado que se arrastra; es acceso **directo y ponderado** a todas las posiciones a la vez.
- **Pensar que el Transformer 'lee en orden':** no; procesa todo en paralelo y el orden se añade aparte (PE).
- **Confundir atención con la solución a todo:** la atención clásica cuesta $O(n^2)$ en la longitud $n$ (cada palabra mira a todas) — es su talón de Aquiles, motor de mucha investigación posterior ([Longformer](https://arxiv.org/abs/2004.05150), [FlashAttention](https://arxiv.org/abs/2205.14135)).

## Contraejemplo y caso borde

- **Contraejemplo (parece que la recurrencia bastaba):** para secuencias **muy cortas**, una LSTM funciona bien y es más barata; la atención brilla cuando hay dependencias largas y se entrena a gran escala. No toda tarea necesita un Transformer.
- **Caso borde (el costo cuadrático):** atender de todos a todos es $O(n^2)$ en memoria y cómputo; para contextos de cientos de miles de tokens, eso es prohibitivo y obliga a variantes (atención dispersa, lineal, FlashAttention). La atención resolvió el cuello de botella de información, pero **abrió** un cuello de botella de cómputo.

## Transferencia isomorfa

La idea "deja de comprimir todo en un resumen; conserva las fuentes y mézclalas según relevancia" reaparece en todas partes:
- En **RAG** ([[gen-rag1]] cuando exista): en vez de meter todo en el prompt, **recuperas** los fragmentos relevantes y se los das al modelo — atención sobre una base de conocimiento.
- En **bases de datos**: un `JOIN` con índice es "ir a buscar exactamente la fila relevante" en vez de escanear todo.
- En la **lectura humana**: no relees el libro entero para responder una pregunta; **vas a la sección** pertinente. La atención es eso, formalizado.

Moraleja de la arista: *la atención es recuperación selectiva y diferenciable: aprender a qué mirar.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** explica con tus palabras por qué un único vector de contexto fijo limita la traducción de frases largas, y cómo la suma ponderada $c_i = \sum_j \alpha_{ij} h_j$ lo resuelve.
- **Misión externa (lab vivo):** lee [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) hasta la sección de self-attention. **Criterio de cierre:** poder explicar, sin la página, qué representa cada peso $\alpha_{ij}$.
- **Mini-entregable:** un párrafo que compare RNN/LSTM vs atención en tres ejes: cuello de botella, dependencias largas y paralelismo.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (cuello de botella seq2seq y atención como recuperación diferenciable) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** comparar un encoder fijo con una capa de atención sobre frases sinteticas.
2. **Baseline obligatorio:** LSTM encoder-decoder sin atención.
3. **Versión mejorada:** decoder con atención Bahdanau o Transformer pequeno.
4. **Evaluación:** accuracy/BLEU por longitud y error analysis de dependencias largas.
5. **Fallo que debes explicar:** la calidad cae justo al aumentar la longitud de la frase.
6. **Transferencia:** RAG: conservar fuentes y recuperar fragmentos en vez de resumir todo.

**Laboratorio externo principal:** [Karpathy Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html).
**Laboratorio alternativo:** [Stanford CS224N: NLP with Deep Learning](https://web.stanford.edu/class/cs224n/).
**Ruta de cluster:** proyecto final tipo GPT-2: tokenizador simple, decoder causal, entrenamiento, generación y evaluación.

**Entregable:** notebook con curva por longitud, heatmap de atención y explicacion Q/A. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y que harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** los modelos secuenciales clásicos (RNN/LSTM) sufrían un **cuello de botella**: comprimir toda la entrada en un vector fijo, con cómputo secuencial y señales que se desvanecían. La **atención** ([Bahdanau, 2015](https://arxiv.org/abs/1409.0473)) lo rompió: en vez de comprimir, conserva todos los estados y, en cada paso, calcula una **mezcla ponderada** $c_i=\sum_j \alpha_{ij}h_j$ que decide **a qué mirar**. [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762) quitó la recurrencia por completo, ganando **paralelismo** y **caminos cortos** entre palabras lejanas — el Transformer—. El precio: un costo **$O(n^2)$** que define la investigación posterior. Al perder el orden por procesar en paralelo, habrá que reinyectarlo (positional encoding).

---

**Referencias**

- Vaswani, A., et al. (2017). Attention is all you need. *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural machine translation by jointly learning to align and translate. *ICLR*. [arXiv:1409.0473](https://arxiv.org/abs/1409.0473)
- Sutskever, I., Vinyals, O., & Le, Q. V. (2014). Sequence to sequence learning with neural networks. *NeurIPS*. [arXiv:1409.3215](https://arxiv.org/abs/1409.3215)
- Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*. [PDF](https://www.bioinf.jku.at/publications/older/2604.pdf)
- Alammar, J. (2018). The Illustrated Transformer. [jalammar.github.io](https://jalammar.github.io/illustrated-transformer/)

*Retrieval: (1) ¿cuál es el cuello de botella de los seq2seq clásicos?; (2) ¿qué calcula $c_i=\sum_j \alpha_{ij}h_j$ y qué significan los $\alpha$?; (3) ¿qué dos superpoderes ganó el Transformer al quitar la recurrencia?; (4) ¿qué nuevo cuello de botella abrió la atención?*
