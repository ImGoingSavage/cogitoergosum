# RAG avanzado y cómo evaluarlo

> Recurso troncal: **MIT-AI.md (Semana 9: "Evaluating RAG"; Semana 13: "adaptive RAG")**. Capstone del cluster: cómo medir si tu RAG funciona y cómo hacerlo más listo. Integra [[gen-rag1]]–[[gen-rag3]] y conecta con la evaluación de GenAI ([[gen-eval1]] cuando exista).

## De qué trata (y qué sabrás hacer al final)

"Funciona en mi demo" no es evaluar un RAG. Un RAG puede fallar en **dos lugares distintos** —la recuperación trajo lo equivocado, o el modelo respondió mal con buen contexto— y necesitas medir **cada uno por separado** para saber qué arreglar. Esta lección te da el marco de evaluación (las métricas del "triángulo RAG") y las técnicas de **RAG avanzado** (adaptativo, query rewriting) que llevan un prototipo a producción.

La intuición: evaluar un RAG es como diagnosticar por qué un estudiante respondió mal un examen a libro abierto. Dos causas posibles: **abrió la página equivocada** (falla de recuperación) o **abrió la correcta pero entendió/copió mal** (falla de generación). Si solo miras la nota final, no sabes cuál arreglar. El diagnóstico de RAG **separa ambas culpas**.

Al terminar podrás: (1) descomponer la calidad de un RAG en **recuperación** vs **generación**; (2) nombrar métricas (context precision/recall, **faithfulness**, answer relevancy) y herramientas ([RAGAS](https://docs.ragas.io/)); (3) entender **RAG adaptativo** y **query rewriting**; y (4) diseñar un loop de evaluación con datos.

## Las dos culpas: recuperación vs generación

Un fallo de RAG vive en uno de dos sitios (o ambos):
1. **Recuperación:** ¿los chunks recuperados **contienen** la respuesta? Si no, da igual cuán bueno sea el LLM. Métricas: **context recall** (¿se recuperó toda la info necesaria?) y **context precision** (¿los recuperados son relevantes, sin ruido?).
2. **Generación:** dado un buen contexto, ¿el modelo respondió **fielmente** a él y **a la pregunta**? Métricas: **faithfulness/fidelidad** (¿la respuesta se sostiene en el contexto, sin inventar? = anti-alucinación) y **answer relevancy** (¿responde lo que se preguntó?).

Esto es el **"RAG triad"** (popularizado por [TruLens](https://www.trulens.org/getting_started/core_concepts/rag_triad/)): *context relevance → groundedness/faithfulness → answer relevance*. Medir los tres te dice **dónde** está el problema: contexto malo → arregla recuperación ([[gen-rag2]]/[[gen-rag3]]); contexto bueno pero respuesta inventada → arregla el prompt/modelo (instrucción "solo con el contexto", mejor LLM).

## Cómo medir sin un humano por cada respuesta

- **Con ground truth (dataset de evaluación):** preparas pares pregunta→respuesta correcta (y, si puedes, los chunks correctos). Mides recuperación (¿trajo los chunks correctos?) y generación (¿la respuesta coincide?). Es lo más fiable; el cuello de botella es **construir el dataset** (a mano o sintético).
- **LLM-as-a-judge:** un LLM evalúa la respuesta contra el contexto y la pregunta (¿es fiel? ¿es relevante?). Escala sin humanos, pero **hereda los sesgos del juez** (tema de [[gen-eval2]] cuando exista). Frameworks como **[RAGAS](https://docs.ragas.io/)** automatizan estas métricas con esta técnica.
- **Faithfulness por verificación de afirmaciones:** descomponer la respuesta en afirmaciones y verificar que cada una se deduzca del contexto. Detecta alucinaciones específicas.

Regla: **evalúa con datos, no con vibras.** Sin un set de evaluación, cada "mejora" del RAG es una apuesta a ciegas.

## RAG avanzado: hacerlo más listo

El RAG básico ("embebe la pregunta, recupera $k$, responde") tiene límites. Técnicas que rinden:

- **Query rewriting / expansion:** reescribir la pregunta antes de buscar (corregir, expandir con sinónimos, descomponer en sub-preguntas). Una pregunta vaga recupera mal; reescrita, recupera bien.
- **RAG adaptativo (MIT-AI Semana 13):** **decidir si recuperar** y cuánto, según la pregunta. Para "hola" no recuperes; para una pregunta factual compleja, recupera y quizá itera. [Self-RAG (Asai et al., 2023)](https://arxiv.org/abs/2310.11511) entrena al modelo para decidir cuándo recuperar y para **criticar** si lo recuperado sostiene su respuesta.
- **RAG multi-paso / agéntico:** descomponer una pregunta en pasos, recuperar para cada uno, y combinar — puente con los **agentes** ([[gen-ag1]] cuando exista). 
- **HyDE:** generar una respuesta hipotética y buscar con su embedding (a veces recupera mejor que con la pregunta cruda).

La frontera: el RAG deja de ser un paso fijo y se vuelve un **proceso adaptativo** que decide, reescribe, recupera, critica e itera.

## Mini-ejemplo trabajado

Tu RAG responde mal "¿cuántos días de reembolso enterprise?". ¿Qué arreglas? **Primero diagnostica con el triángulo:**
- Mides **context recall**: ¿el chunk con "enterprise: 60 días" fue recuperado? Si **no** → problema de **recuperación** (mejora chunking/híbrida/re-ranking). 
- Si **sí** fue recuperado pero la respuesta dijo "30 días" → problema de **generación/fidelidad** (el modelo ignoró el contexto o alucinó → refuerza la instrucción "responde solo con el contexto", o cambia de modelo).

Sin separar las culpas, podrías pasar días "mejorando el prompt" cuando el problema era que el chunk nunca se recuperó. Predicción antes de seguir: tu RAG tiene **faithfulness alta** pero **answer relevancy baja**. ¿Qué significa? → Responde fielmente al contexto… pero **no** lo que se preguntó (recuperó contexto fiel pero irrelevante, o respondió otra cosa). El diagnóstico por métrica separada te lo dice; la nota global, no.

## Señales de reconocimiento

| Síntoma | Métrica que falla → qué arreglar |
|---|---|
| Inventa datos que no están en los docs | Faithfulness baja → instrucción/modelo |
| Responde con info correcta pero irrelevante | Answer relevancy baja → recuperación/prompt |
| El chunk correcto nunca se recupera | Context recall baja → chunking/híbrida/re-rank |
| Recupera mucho ruido junto a lo bueno | Context precision baja → re-ranking, menos k |
| "Mejoro a ciegas, no sé si subió" | Falta dataset de evaluación |

## Errores típicos

- **Evaluar solo la respuesta final:** no distingue culpa de recuperación vs generación; mide ambas.
- **No tener dataset de evaluación:** sin ground truth (o LLM-judge sistemático), las mejoras son anécdotas.
- **Confiar ciegamente en LLM-as-a-judge:** hereda sesgos; calíbralo contra algún juicio humano.
- **Saltar a "RAG agéntico" sin medir el básico:** complejidad sin evaluación esconde regresiones.

## Contraejemplo y caso borde

- **Contraejemplo (más complejo no es mejor):** añadir query rewriting + re-ranking + multi-paso puede **empeorar** si no lo mides; a veces el RAG simple, bien chunked, gana. La evaluación es la que autoriza cada capa de complejidad.
- **Caso borde (el juez se equivoca):** un LLM-judge puede premiar respuestas largas y seguras aunque sean menos correctas (sesgo de verbosidad/autoconfianza). Por eso la evaluación seria combina LLM-judge con muestreo humano y con ground truth donde se pueda.

## Transferencia isomorfa

- **Triángulo RAG ↔ descomponer un error de pipeline:** separar "¿el dato llegó bien?" de "¿el modelo lo usó bien?" es el mismo diagnóstico que separar *data leakage* de *model error* en ML, o *recuperación* de *razonamiento*.
- **RAG adaptativo ↔ agencia mínima:** recuperar solo cuando hace falta es least effort/least privilege aplicado al contexto (no satures, no traigas de más).
- **Evaluar con datos ↔ detection engineering:** sin un set etiquetado y métricas, no sabes si tu detección (o tu RAG) mejoró; las "vibras" no son evidencia ([[cyber-blue5]]).

Moraleja de la arista: *un RAG falla en la recuperación o en la generación; mide cada culpa por separado, con datos, antes de añadir complejidad.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para tres fallos (inventa datos / responde irrelevante / nunca recupera el chunk), di qué métrica del triángulo falla y qué arreglarías.
- **Misión externa (lab vivo):** recorre la doc de [RAGAS](https://docs.ragas.io/) (métricas faithfulness, context precision/recall) y el [RAG Triad de TruLens](https://www.trulens.org/getting_started/core_concepts/rag_triad/). **Criterio de cierre:** explicar qué mide cada vértice del triángulo.
- **Mini-entregable (mini-proyecto del cluster):** un **plan de evaluación de RAG**: cómo construirías un set de evaluación, qué métricas medirías (recuperación y generación), y qué técnica de RAG avanzado probarías y cómo verificarías que ayudó.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (evaluación RAG separando recuperación, generación y fidelidad) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** crear un set con preguntas, fuentes esperadas, respuestas y casos adversarios.
2. **Baseline obligatorio:** evaluar solo la respuesta final.
3. **Versión mejorada:** evaluación por componente con RAGAS o rúbrica propia.
4. **Evaluación:** context recall, faithfulness, answer relevancy y tasa de abstencion.
5. **Fallo que debes explicar:** mejoras de prompt esconden que el contexto correcto nunca se recupero.
6. **Transferencia:** auditoría de asistentes corporativos con documentos privados.

**Laboratorio externo principal:** [RAGAS](https://docs.ragas.io/).
**Laboratorio alternativo:** [OpenAI Evals](https://github.com/openai/evals).
**Ruta de cluster:** asistente RAG con recuperación, atribucion, pruebas de faithfulness y casos adversarios.

**Entregable:** dashboard pequeño con context recall, faithfulness y ejemplos fallidos. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y qué harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** un RAG falla en **recuperación** (no trajo la evidencia) o en **generación** (respondió mal con buena evidencia); el **triángulo RAG** —context relevance, **faithfulness/groundedness**, answer relevance— mide cada culpa por separado para saber **qué** arreglar. Evalúa **con datos** (ground truth y/o **LLM-as-a-judge** vía [RAGAS](https://docs.ragas.io/), con sus sesgos), no con vibras. El **RAG avanzado** (query rewriting, **adaptativo**/Self-RAG, multi-paso/agéntico, HyDE) lo hace más listo, pero **cada capa de complejidad debe justificarse midiendo**. Diagnostica antes de complicar.

---

**Referencias**

- Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Asai, A., et al. (2023). Self-RAG: Learning to retrieve, generate, and critique through self-reflection. [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
- Es, S., et al. (2023). RAGAS: Automated evaluation of retrieval augmented generation. [arXiv:2309.15217](https://arxiv.org/abs/2309.15217) · [Docs](https://docs.ragas.io/)
- TruLens. (n.d.). The RAG triad. [trulens.org](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- Gao, Y., et al. (2023). Retrieval-augmented generation for LLMs: A survey. [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)

*Retrieval: (1) ¿en qué dos lugares puede fallar un RAG y cómo lo separas?; (2) ¿qué miden los tres vértices del triángulo RAG?; (3) ¿qué es RAG adaptativo / Self-RAG?; (4) ¿por qué cada capa de complejidad debe justificarse midiendo?*
