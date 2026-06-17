# Detección de alucinaciones: consistencia y anclaje

> Recurso troncal: **MIT-AI.md (Semana 10: "Identifying hallucinations through consistency checks")**. El fallo más peligroso de los LLMs y cómo cazarlo. Sigue a [[gen-eval2]] (LLM-as-judge) y prepara [[gen-eval4]] (optimización de prompts).

## De qué trata (y qué sabrás hacer al final)

Un LLM **alucina** cuando genera contenido que suena correcto pero es falso o no está respaldado por la fuente. Es el riesgo número uno para usar GenAI en serio (salud, legal, finanzas): no es que se equivoque, es que se equivoca **con total confianza y fluidez**, lo que hace difícil detectarlo a simple vista. Esta lección da las técnicas para **detectar** alucinaciones de forma sistemática, no por intuición.

La intuición: detectar alucinaciones es como verificar a un testigo muy elocuente que **nunca dice "no sé"**. Dos estrategias clásicas de un detective: (1) **hacerlo repetir la historia varias veces** —si inventa, las versiones se contradicen; si lo vivió, son consistentes (chequeo de **consistencia**)—; y (2) **contrastar con la evidencia** —¿lo que dice coincide con los documentos/hechos? (chequeo de **anclaje/groundedness**)—. Las dos juntas cazan la mayoría.

Al terminar podrás: (1) distinguir tipos de alucinación (**intrínseca** vs **extrínseca**); (2) usar **chequeos de consistencia** (self-consistency, SelfCheckGPT); (3) usar **anclaje** (verificar contra fuentes / faithfulness); y (4) reconocer por qué la incertidumbre del modelo es engañosa.

## Qué es una alucinación (y de qué tipo)

Una alucinación es una afirmación generada que no está respaldada. Dos tipos ([Ji et al., 2023, survey](https://arxiv.org/abs/2202.03629)):
- **Intrínseca:** contradice la **fuente dada** (en RAG, dice algo que el contexto recuperado no dice o contradice). Es la más fácil de detectar: comparas con el contexto.
- **Extrínseca:** afirma algo **no verificable** con la fuente (inventa un hecho, una cita, un número que no está en ningún lado). Más difícil: requiere conocimiento externo o detección de inconsistencia.

Por qué ocurren: el LLM optimiza **plausibilidad** (qué texto es probable), no **verdad**; cuando no "sabe", completa con lo más plausible, que puede ser falso. No tiene un "no sé" por defecto.

## Estrategia 1: chequeos de consistencia

Si una respuesta es inventada, **muestrear varias veces** tiende a producir versiones **divergentes**; si está fundada, las versiones **concuerdan**. Dos usos:
- **Self-consistency** ([Wang et al., 2022](https://arxiv.org/abs/2203.11171)): para tareas con respuesta concreta (p. ej. razonamiento), generar varias cadenas de pensamiento y **votar** por la respuesta mayoritaria; sube la exactitud y revela cuando el modelo "duda" (respuestas dispersas).
- **SelfCheckGPT** ([Manakul et al., 2023](https://arxiv.org/abs/2305.15852)): genera varias respuestas a la misma pregunta y mide su **consistencia**; afirmaciones que aparecen consistentes en todas las muestras tienden a ser fiables; las que cambian de una muestra a otra, sospechosas de alucinación. **No necesita** una fuente externa — útil cuando no hay referencia.

Idea clave: *la inconsistencia entre muestras es una señal de alucinación.*

## Estrategia 2: anclaje (groundedness)

Cuando **hay** una fuente (RAG, documentos), la prueba más fuerte es verificar que cada afirmación se **deduzca** del contexto. Esto es la **faithfulness** de [[gen-rag4]]: descomponer la respuesta en afirmaciones y comprobar, una por una, que el contexto las respalda (con un verificador NLI o un LLM-juez con la instrucción precisa). Una afirmación que no se sostiene en la fuente es una alucinación intrínseca. En sistemas serios, **exigir citas** (atribución) y verificar que la cita realmente dice lo afirmado es el control operativo más práctico.

## La trampa: la "confianza" del modelo no es fiabilidad

Tentador: "usa la probabilidad/confianza del modelo para detectar cuándo alucina". Problema: los LLMs suelen estar **mal calibrados** —dicen falsedades con alta confianza aparente—. La fluidez y el tono seguro **no** correlacionan con la verdad. Por eso la detección se basa en **consistencia** (varias muestras) y **anclaje** (fuentes), no en pedirle al modelo que "diga cuán seguro está" (aunque la calibración es un área activa).

## Mini-ejemplo trabajado

Preguntas a un asistente legal: *"¿Qué dice el artículo 47 sobre plazos?"* y responde con un texto detallado y seguro citando "el artículo 47 establece 90 días". ¿Alucinación?
- **Anclaje:** ¿existe el artículo 47 en tu corpus y dice eso? Si tu RAG no recuperó nada o el artículo dice otra cosa → alucinación intrínseca/extrínseca. (Los casos reales de abogados sancionados por citar jurisprudencia inventada por ChatGPT son exactamente esto.)
- **Consistencia:** pregunta 5 veces; si el "90 días" baila a "60", "120", "no especifica" → señal fuerte de invención.
- **Control operativo:** exigir que **cite** el pasaje y verificar que el pasaje citado realmente lo diga.

Predicción antes de seguir: el modelo responde con un tono **muy** seguro y elocuente. ¿Eso sube tu confianza en que es verdad? → No: la elocuencia es ortogonal a la verdad; en LLMs, el tono seguro a veces acompaña justo a las invenciones. Desconfía de la fluidez.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| Respuesta segura sin fuente verificable | Posible alucinación extrínseca; exige cita |
| Contradice el contexto recuperado | Alucinación intrínseca; falla faithfulness |
| Las respuestas cambian al re-preguntar | Inconsistencia → señal de invención |
| Citas/números que no existen en el corpus | Alucinación; verifica la cita |
| "Confía, está muy seguro" | La confianza no es fiabilidad |

## Errores típicos

- **Confiar en el tono/confianza del modelo:** mal calibrado; seguro ≠ verdadero.
- **Detectar a ojo:** las alucinaciones son fluidas y plausibles; necesitas consistencia/anclaje sistemáticos.
- **Creer que RAG elimina alucinaciones:** las reduce, pero el modelo puede ignorar o contradecir el contexto (por eso se mide faithfulness).
- **Pedir una sola muestra:** sin varias muestras pierdes la señal de inconsistencia.

## Contraejemplo y caso borde

- **Contraejemplo (consistencia engañosa):** un modelo puede ser **consistentemente** incorrecto —repetir el mismo error en todas las muestras si el error está "horneado" en sus pesos—. La consistencia sugiere fiabilidad pero **no la garantiza**; por eso se combina con anclaje a fuentes externas.
- **Caso borde (creatividad ≠ alucinación):** en tareas creativas (escribir ficción, *brainstorming*) "inventar" es deseable, no un fallo. "Alucinación" solo es problema cuando la tarea exige **factualidad**. La métrica debe ajustarse a la tarea.

## Transferencia isomorfa

- **Consistencia entre muestras ↔ triangulación / replicación:** confiar más en lo que se sostiene al repetir la medición desde ángulos distintos — base del método científico y del *adversarial verify* (varios verificadores independientes).
- **Anclaje ↔ atribución y auditoría:** exigir que cada afirmación apunte a evidencia verificable es la misma disciplina que la auditoría de datos ([[cyber-dp4]]) o la verificación fuera de banda ([[cyber-mit2]]): no creas, verifica contra la fuente.
- **Confianza mal calibrada ↔ automation bias:** el tono seguro de la IA induce a aceptarla sin verificar ([[cyber-mit4]]); la defensa es la misma: verificar lo de alta consecuencia.

Moraleja de la arista: *para cazar alucinaciones, haz repetir (consistencia) y contrasta con la fuente (anclaje); nunca confíes en la elocuencia.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para un asistente que da datos médicos, diseña un protocolo de detección de alucinaciones que combine consistencia (cuántas muestras, qué señal) y anclaje (cómo verificar contra el corpus).
- **Misión externa (lab vivo):** lee el paper [SelfCheckGPT (Manakul et al., 2023)](https://arxiv.org/abs/2305.15852) (idea central) y el [survey de alucinaciones (Ji et al., 2023)](https://arxiv.org/abs/2202.03629). **Criterio de cierre:** explicar por qué la inconsistencia entre muestras señala alucinación.
- **Mini-entregable:** un checklist de detección de alucinaciones (consistencia + anclaje + exigir citas) para un sistema de alto riesgo.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (alucinación, faithfulness y consistencia contra fuentes) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** implementar checks de afirmaciones contra contexto y consistencia multi-muestra.
2. **Baseline obligatorio:** aceptar respuestas plausibles sin verificar soporte.
3. **Versión mejorada:** verificacion por claims y abstencion cuando falta evidencia.
4. **Evaluación:** unsupported claim rate, faithfulness y tasa de abstencion correcta.
5. **Fallo que debes explicar:** una respuesta segura agrega datos no presentes en la fuente.
6. **Transferencia:** dominios sensibles donde cada afirmación necesita trazabilidad.

**Laboratorio externo principal:** [RAGAS](https://docs.ragas.io/).
**Laboratorio alternativo:** [OpenAI Evals](https://github.com/openai/evals).
**Ruta de cluster:** harness de evaluación con línea base, prompts candidatos, LLM-as-judge calibrado y reporte de regresiones.

**Entregable:** set de hallucination eval con claims, fuentes y verdictos. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y qué harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** una **alucinación** es contenido generado no respaldado —**intrínseca** (contradice la fuente) o **extrínseca** (inventa lo no verificable)— y ocurre porque el LLM optimiza **plausibilidad, no verdad**. Se detecta con dos estrategias combinadas: **consistencia** (varias muestras divergen si inventa — self-consistency, SelfCheckGPT, sin necesitar fuente) y **anclaje** (verificar cada afirmación contra la fuente — faithfulness, exigir citas y comprobarlas). **No** confíes en la confianza/elocuencia del modelo (mal calibrado: seguro ≠ verdadero), y recuerda que la consistencia sugiere pero no garantiza, y que "inventar" solo es fallo cuando la tarea exige factualidad.

---

**Referencias**

- Ji, Z., et al. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys*. [arXiv:2202.03629](https://arxiv.org/abs/2202.03629)
- Wang, X., et al. (2022). Self-consistency improves chain of thought reasoning in language models. *ICLR*. [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
- Manakul, P., Liusie, A., & Gales, M. (2023). SelfCheckGPT: Zero-resource black-box hallucination detection. *EMNLP*. [arXiv:2305.15852](https://arxiv.org/abs/2305.15852)
- Huang, L., et al. (2023). A survey on hallucination in LLMs. [arXiv:2311.05232](https://arxiv.org/abs/2311.05232)

*Retrieval: (1) intrínseca vs extrínseca; (2) ¿por qué la inconsistencia entre muestras señala alucinación?; (3) ¿qué es anclaje/groundedness y cómo se verifica?; (4) ¿por qué no fiarse de la confianza del modelo?*
