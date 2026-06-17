# Por qué evaluar texto generado es difícil: ROUGE, BLEU y sus límites

> Recurso troncal: **MIT-AI.md (Semana 10)**. Sin evaluación, "mejorar" un sistema GenAI es adivinar. Esta lección abre el problema y las métricas clásicas de superposición. Conecta con la evaluación de RAG ([[gen-rag4]]) y prepara [[gen-eval2]] (métricas semánticas y LLM-as-judge).

## De qué trata (y qué sabrás hacer al final)

En clasificación, evaluar es fácil: la predicción es correcta o no (accuracy, F1). En **generación de texto** no hay una sola respuesta correcta: "¿Cómo cancelo mi suscripción?" admite mil respuestas buenas con palabras distintas. ¿Cómo le pones un número a "qué tan buena es"? Esta es la pregunta más subestimada de la IA generativa, y resolverla mal hace que optimices hacia el lugar equivocado.

La intuición: evaluar una clasificación es como **corregir un examen de opción múltiple** (hay una clave). Evaluar texto generado es como **calificar un ensayo**: dos ensayos excelentes pueden no compartir ninguna frase, y uno que copia frases del modelo puede ser pésimo. Las métricas clásicas (ROUGE, BLEU) intentan calificar el ensayo **contando palabras compartidas con una respuesta de referencia** — útil pero ciego al significado.

Al terminar podrás: (1) explicar **por qué evaluar generación es intrínsecamente difícil**; (2) entender **ROUGE y BLEU** (superposición de n-gramas) y para qué sirven; (3) nombrar sus **límites** (ciegas al significado, dependen de referencias); y (4) distinguir métricas **con referencia** vs **sin referencia**.

## Por qué es difícil: no hay una respuesta correcta

Tres propiedades hacen dura la evaluación de generación:
- **Multiplicidad:** muchas salidas distintas son igual de válidas (paráfrasis, distinto orden, distinto estilo).
- **Multidimensionalidad:** "buena" mezcla dimensiones que pueden ir en direcciones opuestas — fidelidad a los hechos, relevancia, fluidez, concisión, tono, seguridad. Una respuesta puede ser fluida pero falsa.
- **Dependencia del contexto y la tarea:** lo "bueno" para un resumen ejecutivo no es lo bueno para una respuesta legal.

Por eso no existe **una** métrica universal; se usa un **conjunto** de señales, y casi siempre se combina con juicio humano (caro) o con un modelo-juez ([[gen-eval2]]).

## ROUGE: superposición de n-gramas (resumen)

**ROUGE** ([Lin, 2004](https://aclanthology.org/W04-1013/)) mide cuánto se **solapan** las palabras/secuencias de la salida con una **referencia humana**. Variantes clave:
- **ROUGE-N:** fracción de n-gramas de la referencia que aparecen en la salida (recall de n-gramas). ROUGE-1 = unigramas, ROUGE-2 = bigramas.
- **ROUGE-L:** longitud de la subsecuencia común más larga (captura orden sin exigir contigüidad).

Se usa sobre todo para **resumen** (¿el resumen generado cubre lo que cubre el de referencia?). Es barato, reproducible y correlaciona razonablemente con calidad **cuando hay buenas referencias**.

## BLEU: el primo de la traducción

**BLEU** ([Papineni et al., 2002](https://aclanthology.org/P02-1040/)) nació para **traducción automática**: mide **precisión** de n-gramas (qué fracción de los n-gramas de la salida están en la referencia), con una penalización por brevedad (para que el modelo no haga trampa generando textos cortísimos). ROUGE es "recall-orientado" (resumen: cubrir todo), BLEU es "precisión-orientado" (traducción: no inventar). Misma familia: contar n-gramas compartidos con una referencia.

## Mini-ejemplo trabajado: dos resúmenes, una métrica ciega

Referencia: *"El paciente debe tomar el medicamento dos veces al día."*
- Salida A: *"El medicamento se toma dos veces al día."* → comparte muchos n-gramas → ROUGE alto. Correcta.
- Salida B: *"El paciente debe tomar el medicamento dos veces a la semana."* → comparte **casi todos** los n-gramas (cambió "día"→"semana") → ROUGE **altísimo**… y es **médicamente peligrosa**.
- Salida C: *"Hay que medicarse cada 12 horas."* → **cero** n-gramas compartidos con la referencia → ROUGE **bajo**… y es **correcta** (paráfrasis perfecta).

Moraleja brutal: ROUGE premió a B (peligrosa) y castigó a C (correcta), porque **cuenta palabras, no significado**. Predicción antes de seguir: ¿qué tipo de métrica arreglaría esto? → una que compare **significado** (embeddings), no superficie — el tema de [[gen-eval2]] (BERTScore, LLM-as-judge).

## Con referencia vs sin referencia

Distinción clave para todo lo que sigue:
- **Métricas con referencia (reference-based):** comparan la salida con una "respuesta correcta" humana (ROUGE, BLEU, BERTScore). Problema: **necesitas referencias**, que son caras de crear y a menudo no existen (¿cuál es la "respuesta de referencia" de un chatbot abierto?).
- **Métricas sin referencia (reference-free):** evalúan la salida **en sí** o contra el contexto/pregunta, sin una respuesta dorada (LLM-as-judge, faithfulness contra el contexto recuperado de [[gen-rag4]]). Escalan a producción donde no hay referencias, a costa de más subjetividad.

La industria se mueve hacia métricas **sin referencia** (sobre todo LLM-as-judge) porque los sistemas reales rara vez tienen referencias para cada consulta.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "Quiero un número rápido y reproducible para resumen/traducción" | ROUGE/BLEU (con buenas referencias) |
| "La métrica premia paráfrasis peligrosas / castiga correctas" | Métrica ciega al significado → usa semántica |
| "No tengo respuestas de referencia" | Métricas sin referencia (LLM-as-judge, faithfulness) |
| "Una respuesta fluida pero falsa pasó la evaluación" | Falta medir fidelidad/factualidad por separado |

## Errores típicos

- **Tratar ROUGE/BLEU como medida de 'calidad' general:** miden superposición léxica, no corrección ni utilidad; correlacionan débilmente con el juicio humano en tareas abiertas.
- **Optimizar la métrica en vez de la tarea:** subir ROUGE copiando frases de la referencia produce textos peores (es *gaming* de la métrica; ver ley de Goodhart).
- **Asumir que existe la referencia:** en chat/asistentes abiertos no hay una respuesta dorada por consulta.

## Contraejemplo y caso borde

- **Contraejemplo (ROUGE/BLEU sí sirven):** para traducción con referencias profesionales y para *benchmarks* comparables, BLEU/ROUGE siguen siendo útiles y estándar — baratos, reproducibles, buenos para comparar sistemas en igualdad. No son inútiles; son **insuficientes** para tareas abiertas.
- **Caso borde (la referencia es mala):** si la referencia humana es pobre o única (cuando había muchas válidas), la métrica penaliza salidas buenas que simplemente difieren de esa referencia. La métrica nunca es mejor que su referencia.

## Transferencia isomorfa

- **Evaluar generación ↔ evaluar problemas abiertos:** como calificar una desconstrucción o un ensayo, no hay clave única; necesitas rúbricas y juicio, no coincidencia exacta (eco de cómo evaluamos las preguntas de reflexión).
- **ROUGE/BLEU ↔ métricas proxy:** un número fácil de medir que **aproxima** lo que importa pero puede divergir de ello — como confundir "líneas de código" con "valor", o "n.º de alertas" con "seguridad" ([[cyber-blue5]]). Cuidado con optimizar el proxy.
- **Con/sin referencia ↔ supervisado/no supervisado:** con etiqueta dorada vs evaluar la estructura intrínseca.

Moraleja de la arista: *contar palabras compartidas no es medir significado; toda métrica es un proxy y optimizar el proxy a ciegas degrada lo que importaba.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** inventa un par referencia/salida donde ROUGE sea alto pero la salida sea incorrecta, y otro donde ROUGE sea bajo pero la salida sea correcta. Explica por qué.
- **Misión externa (lab vivo):** lee el paper de [ROUGE (Lin, 2004)](https://aclanthology.org/W04-1013/) (intro) y la entrada de [BLEU](https://aclanthology.org/P02-1040/). **Criterio de cierre:** explicar la diferencia recall (ROUGE) vs precisión (BLEU) y un límite de cada una.
- **Mini-entregable:** una tabla "métrica → qué mide → cuándo sirve → cuándo engaña" para ROUGE y BLEU.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (límites de BLEU/ROUGE y necesidad de métricas semánticas) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** comparar ROUGE/BLEU contra BERTScore o juez rubricado en ejemplos controlados.
2. **Baseline obligatorio:** ROUGE/BLEU como única métrica.
3. **Versión mejorada:** métrica semántica más revisión de factualidad.
4. **Evaluación:** correlacion con juicio humano, errores por parafrasis y factualidad.
5. **Fallo que debes explicar:** sube la superposicion de palabras pero baja la calidad real.
6. **Transferencia:** evaluar respuestas de un asistente sin una única respuesta dorada.

**Laboratorio externo principal:** [Stanford CS224N: NLP with Deep Learning](https://web.stanford.edu/class/cs224n/).
**Laboratorio alternativo:** [OpenAI Evals](https://github.com/openai/evals).
**Ruta de cluster:** harness de evaluación con línea base, prompts candidatos, LLM-as-judge calibrado y reporte de regresiones.

**Entregable:** reporte con pares de salidas, métricas y juicio humano razonado. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y que harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** evaluar texto generado es difícil porque **no hay una respuesta correcta** (multiplicidad), "bueno" es **multidimensional** (fidelidad ≠ fluidez), y depende de la tarea. **ROUGE** (recall de n-gramas, resumen) y **BLEU** (precisión de n-gramas, traducción) miden **superposición léxica con una referencia**: baratas y estándar, pero **ciegas al significado** (premian paráfrasis peligrosas, castigan correctas) y dependen de **referencias** que a menudo no existen. De ahí el giro a métricas **semánticas** y **sin referencia** ([[gen-eval2]]). Toda métrica es un **proxy**: optimizarla a ciegas degrada la tarea.

---

**Referencias**

- Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. *ACL Workshop*. [aclanthology.org/W04-1013](https://aclanthology.org/W04-1013/)
- Papineni, K., et al. (2002). BLEU: A method for automatic evaluation of machine translation. *ACL*. [aclanthology.org/P02-1040](https://aclanthology.org/P02-1040/)
- Zhang, T., et al. (2020). BERTScore: Evaluating text generation with BERT. *ICLR*. [arXiv:1904.09675](https://arxiv.org/abs/1904.09675)
- Celikyilmaz, A., Clark, E., & Gao, J. (2020). Evaluation of text generation: A survey. [arXiv:2006.14799](https://arxiv.org/abs/2006.14799)

*Retrieval: (1) ¿por qué evaluar generación es más difícil que clasificación?; (2) ¿qué miden ROUGE y BLEU y en qué se diferencian?; (3) da un caso donde ROUGE engaña; (4) ¿con referencia vs sin referencia, y por qué la industria va hacia la segunda?*
