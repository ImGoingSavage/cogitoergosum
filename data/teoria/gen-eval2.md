# Métricas semánticas y LLM-as-a-judge

> Recurso troncal: **MIT-AI.md (Semana 10)**. El salto de "contar palabras" a "medir significado" y a usar un LLM como evaluador. Sigue a [[gen-eval1]] (ROUGE/BLEU) y prepara [[gen-eval3]] (alucinaciones).

## De qué trata (y qué sabrás hacer al final)

Vimos que ROUGE/BLEU son ciegas al significado: premian paráfrasis erróneas, castigan correctas. Esta lección cubre las dos respuestas modernas: (1) **BERTScore**, que compara **significado** vía embeddings, y (2) **LLM-as-a-judge**, usar un modelo potente para **calificar** las salidas como lo haría un humano —la técnica dominante hoy—, con sus poderosos pros y sus traicioneros sesgos.

La intuición: si calificar texto es como evaluar un ensayo, ROUGE era "contar cuántas palabras coinciden con el ensayo modelo". **BERTScore** es "ver si los ensayos *significan* lo mismo aunque usen otras palabras". **LLM-as-a-judge** es "contratar a un evaluador experto (otro modelo) que lee el ensayo y la rúbrica y pone una nota con justificación". El evaluador escala infinitamente… pero tiene manías (le gustan los ensayos largos, los que suenan seguros, los que él mismo habría escrito).

Al terminar podrás: (1) explicar **BERTScore** (similitud semántica con embeddings); (2) entender **LLM-as-a-judge** y sus modos (puntuación, comparación por pares); (3) nombrar sus **sesgos** conocidos y cómo mitigarlos; y (4) elegir la métrica según la tarea.

## BERTScore: superposición de significado

**BERTScore** ([Zhang et al., 2020](https://arxiv.org/abs/1904.09675)) reemplaza "¿comparten palabras?" por "¿comparten significado?". En vez de coincidencia exacta de n-gramas, embebe cada token de la salida y de la referencia (con un modelo tipo BERT) y los empareja por **similitud coseno** (la del [[gen-rag2]]), calculando precisión, recall y F1 sobre esos emparejamientos semánticos. Así, "cada 12 horas" y "dos veces al día" obtienen alta similitud aunque no compartan palabras — arregla el contraejemplo de [[gen-eval1]]. 

Sigue siendo **con referencia** (necesita una respuesta dorada) y hereda los límites del modelo de embeddings (p. ej. la negación, [[gen-rag2]]), pero es un gran salto sobre ROUGE para medir adecuación semántica. Otras de su familia: [BLEURT](https://arxiv.org/abs/2004.04696) (entrenada para correlacionar con humanos), [MoverScore](https://arxiv.org/abs/1909.02622).

## LLM-as-a-judge: el evaluador escalable

La idea ([Zheng et al., 2023, "MT-Bench / LLM-as-a-judge"](https://arxiv.org/abs/2306.05685); [Liu et al., 2023, "G-Eval"](https://arxiv.org/abs/2303.16634)): darle a un LLM potente la pregunta, la respuesta (y opcionalmente el contexto o una rúbrica) y pedirle que la **evalúe** —una nota, un veredicto, o cuál de dos respuestas es mejor—. Ventajas enormes: **no necesita referencias**, captura matices que las métricas léxicas no, escala sin humanos y se puede pedir que **justifique** su nota. Por eso es el estándar de facto para evaluar chatbots, RAG ([[gen-rag4]], RAGAS) y agentes.

Dos modos principales:
- **Puntuación directa (pointwise):** "del 1 al 5, ¿qué tan fiel/útil es esta respuesta?" Simple, pero las escalas absolutas son ruidosas.
- **Comparación por pares (pairwise):** "¿es mejor A o B?" Más fiable (a los humanos y a los LLMs se les da mejor comparar que puntuar en abstracto); base de los rankings tipo [Chatbot Arena](https://arxiv.org/abs/2403.04132).

## Los sesgos del juez (y cómo mitigarlos)

Un LLM-juez **no es neutral**. Sesgos documentados ([Zheng et al., 2023](https://arxiv.org/abs/2306.05685)):
- **Sesgo de posición:** tiende a preferir la primera (o última) respuesta presentada → mitígalo **promediando ambos órdenes** (A vs B y B vs A).
- **Sesgo de verbosidad:** prefiere respuestas más largas, aunque no sean mejores.
- **Sesgo de autoafinidad (self-enhancement):** un modelo tiende a preferir respuestas de su propia familia/estilo.
- **Sesgo de autoconfianza:** premia el tono seguro aunque el contenido sea dudoso.

Mitigaciones: rúbricas explícitas (qué cuenta como bueno), comparación por pares con orden barajado, pedir razonamiento antes de la nota (chain-of-thought mejora la consistencia), usar varios jueces o un panel, y **calibrar el juez contra una muestra de juicio humano**. Regla de oro: *trata al LLM-juez como un evaluador útil pero sesgado, no como la verdad.*

## Mini-ejemplo trabajado

Comparas dos respuestas a "¿cómo configuro 2FA?": A es correcta y concisa (3 líneas); B es correcta pero envuelta en 3 párrafos de relleno. Pides al LLM-juez "¿cuál es mejor?" y dice **B**. ¿Por qué? Probable **sesgo de verbosidad**: confundió "más largo y detallado" con "mejor". Mitigación: una rúbrica que premie concisión y penalice relleno, y promediar el orden (por si también hubo sesgo de posición). Predicción antes de seguir: si evalúas respuestas de **tu propio modelo** con **un juez de la misma familia**, ¿qué riesgo corres? → **self-enhancement**: el juez infla las notas de su propia familia; conviene un juez distinto o una rúbrica anclada.

## Señales de reconocimiento

| Señal | Jugada |
|---|---|
| "Necesito medir significado, no palabras, y tengo referencias" | BERTScore/BLEURT |
| "No tengo referencias y quiero evaluar a escala" | LLM-as-a-judge |
| "El juez prefiere siempre la respuesta A" | Sesgo de posición → promedia órdenes |
| "El juez premia respuestas largas/relleno" | Sesgo de verbosidad → rúbrica + concisión |
| "Evalúo mi modelo con un juez de su familia" | Self-enhancement → juez distinto / rúbrica anclada |

## Errores típicos

- **Tratar la nota del LLM-juez como verdad objetiva:** es un evaluador sesgado; calíbralo y vigílalo.
- **Puntuación absoluta sin rúbrica:** escalas 1-5 sin criterios son ruidosas; mejor pairwise con rúbrica.
- **No controlar el orden en comparaciones:** el sesgo de posición contamina los resultados.
- **Usar BERTScore creyendo que entiende factualidad:** mide adecuación semántica, no si los hechos son verdad (un dato falso bien parafraseado puntúa alto).

## Contraejemplo y caso borde

- **Contraejemplo (el juez acierta donde las léxicas fallan):** en el caso de [[gen-eval1]] (paráfrasis correcta con cero n-gramas compartidos), un LLM-juez con rúbrica la reconoce como correcta — justo donde ROUGE la castigaba. El juez es más capaz; el precio es el sesgo.
- **Caso borde (juez y generador comparten el error):** si el conocimiento erróneo está tanto en el modelo evaluado como en el juez, el juez **valida la alucinación** (ambos "creen" lo mismo falso). Por eso la factualidad necesita anclaje externo (fuentes, [[gen-eval3]]), no solo otro LLM opinando.

## Transferencia isomorfa

- **LLM-as-a-judge ↔ panel de jueces / revisión por pares:** evaluar con criterio experto y rúbrica, con el cuidado de sesgos (posición, verbosidad) — el mismo patrón que un panel de revisores o jueces que ya usamos en evaluación, y que el método de caso del MIT ([[cyber-mit5]]).
- **Pairwise > pointwise ↔ comparar es más fácil que puntuar:** humanos y modelos calibran mejor "¿cuál es mejor?" que "del 1 al 10"; base de los rankings Elo (Chatbot Arena).
- **Calibrar el juez ↔ validar un detector:** un evaluador automático, como una regla de detección ([[cyber-blue2]]), debe validarse contra ground truth antes de confiar en él.

Moraleja de la arista: *BERTScore mide significado; el LLM-juez mide casi todo pero con sesgos — úsalo como evaluador calibrado, compara por pares, ancla la factualidad fuera del modelo.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** diseña un prompt de LLM-as-a-judge **pairwise** para evaluar fidelidad de respuestas de soporte, incluyendo rúbrica y control del orden. Di qué sesgos mitigas y cómo.
- **Misión externa (lab vivo):** lee el paper [Judging LLM-as-a-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685) (sección de sesgos) y explora [Chatbot Arena](https://lmarena.ai/). **Criterio de cierre:** nombrar 3 sesgos del juez y su mitigación.
- **Mini-entregable:** una guía de "cómo usar LLM-as-a-judge sin engañarte": modo (pairwise), rúbrica, control de orden, calibración humana, anclaje de factualidad.

---

> **Síntesis:** **BERTScore** mide **significado** (similitud coseno de embeddings entre salida y referencia), arreglando la ceguera léxica de ROUGE/BLEU, pero sigue necesitando referencia y no juzga factualidad. **LLM-as-a-judge** evalúa **sin referencia y a escala**, captando matices y justificando, por eso domina (chatbots, RAG, agentes); mejor en modo **pairwise** que pointwise. Pero el juez tiene **sesgos** (posición, verbosidad, self-enhancement, autoconfianza): mitígalos con rúbricas, barajar el orden, paneles y **calibración contra humanos**. Y la **factualidad** se ancla fuera del modelo, porque juez y generador pueden compartir el mismo error.

---

**Referencias**

- Zhang, T., et al. (2020). BERTScore: Evaluating text generation with BERT. *ICLR*. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)
- Zheng, L., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS*. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Liu, Y., et al. (2023). G-Eval: NLG evaluation using GPT-4 with better human alignment. *EMNLP*. [arXiv:2303.16634](https://arxiv.org/abs/2303.16634)
- Sellam, T., Das, D., & Parikh, A. (2020). BLEURT: Learning robust metrics for text generation. *ACL*. [arXiv:2004.04696](https://arxiv.org/abs/2004.04696)
- Chiang, W.-L., et al. (2024). Chatbot Arena: An open platform for evaluating LLMs by human preference. [arXiv:2403.04132](https://arxiv.org/abs/2403.04132) · [lmarena.ai](https://lmarena.ai/)

*Retrieval: (1) ¿qué mide BERTScore y cómo, frente a ROUGE?; (2) ¿qué es LLM-as-a-judge y por qué pairwise > pointwise?; (3) nombra 3 sesgos del juez y su mitigación; (4) ¿por qué la factualidad no se puede dejar solo a otro LLM?*
