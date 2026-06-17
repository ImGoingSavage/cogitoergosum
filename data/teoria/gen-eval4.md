# Optimización de prompts dirigida por evaluación

> Recurso troncal: **MIT-AI.md (Semana 10: "Prompt optimization techniques")**. Capstone del cluster: mejorar prompts con método, no por intuición, cerrando el lazo con la evaluación. Integra [[gen-eval1]]–[[gen-eval3]] y conecta con la inyección de [[cyber-llm1]].

## De qué trata (y qué sabrás hacer al final)

El prompt es el "programa" de un LLM: pequeñas diferencias en cómo pides algo cambian enormemente la calidad. Pero "mejorar el prompt" suele hacerse a ojo —cambias una palabra, te parece mejor, sigues—. Esta lección convierte la **ingeniería de prompts** en una disciplina **dirigida por evaluación**: técnicas que funcionan (few-shot, chain-of-thought, descomposición) y, sobre todo, **cómo medir** que un cambio de prompt de verdad mejoró, usando lo aprendido en [[gen-eval2]]/[[gen-eval3]].

La intuición: optimizar prompts sin evaluación es como **ajustar una receta a ojo, sin probar el plato y sin escribir qué cambiaste** — crees que mejora pero no sabes, y no puedes reproducirlo. Con evaluación es **cocina seria**: cambias un ingrediente a la vez, lo pruebas contra un panel (tu set de evaluación) y conservas el cambio solo si la nota sube. La diferencia entre "me parece" y "lo medí".

Al terminar podrás: (1) aplicar técnicas de prompting que rinden (**few-shot, chain-of-thought, descomposición, formato/rol**); (2) cerrar el **lazo de evaluación** (cambiar → medir contra un set → conservar si mejora); (3) reconocer **optimización automática de prompts**; y (4) evitar el *gaming* y los riesgos de seguridad.

## Técnicas de prompting que rinden

[CAJA NEGRA OK — son patrones empíricos; lo importante es cuándo y por qué]
- **Instrucción clara + rol + formato:** decir exactamente la tarea, el rol ("eres un analista…") y el formato de salida (JSON, lista). Reduce ambigüedad.
- **Few-shot (ejemplos):** incluir 2-5 ejemplos resueltos en el prompt. El modelo imita el patrón ([Brown et al., 2020, "GPT-3 / in-context learning"](https://arxiv.org/abs/2005.14165)). Crucial para formato y tareas específicas.
- **Chain-of-Thought (CoT):** pedir "razona paso a paso" mejora tareas de razonamiento, porque el modelo genera pasos intermedios en vez de saltar a la respuesta ([Wei et al., 2022](https://arxiv.org/abs/2201.11903)). Combínalo con **self-consistency** ([[gen-eval3]]) para votar entre cadenas.
- **Descomposición:** partir una tarea compleja en sub-tareas encadenadas (prompt chaining) — más fiable que un mega-prompt que lo pide todo de golpe. Puente con los **agentes** ([[gen-ag1]] cuando exista).
- **Grounding/restricción:** "responde solo con el contexto; si no está, dilo" (anti-alucinación, [[gen-rag3]]).

Ninguna es mágica; cuál ayuda **depende de la tarea**, y por eso hay que **medir**.

## El lazo: optimización dirigida por evaluación

La clave de la lección: **no optimices a ciegas.** El método:
1. **Define la métrica** y un **set de evaluación** (casos representativos con lo que cuenta como bueno — de [[gen-eval2]]/[[gen-eval3]]).
2. **Establece una línea base** (mide el prompt actual).
3. **Cambia una cosa** (una técnica, una instrucción).
4. **Mide** contra el mismo set; conserva el cambio **solo si la métrica sube** sin regresiones.
5. Repite.

Sin pasos 1-2-4, "mejorar el prompt" es superstición. Con ellos, es ingeniería. Es el mismo rigor que la evaluación de RAG ([[gen-rag4]]): *evalúa con datos, no con vibras.*

## Optimización automática de prompts

Probar prompts a mano no escala. Hay enfoques que **buscan** buenos prompts automáticamente:
- **APE** ([Zhou et al., 2022, "Automatic Prompt Engineer"](https://arxiv.org/abs/2211.01910)): un LLM **genera** candidatos de prompt y se **evalúan** para quedarse con el mejor.
- **DSPy** ([Khattab et al., 2023](https://arxiv.org/abs/2310.03714)): trata el prompt como **parámetros a optimizar** dado un objetivo y datos — "programar, no promptear". Mueve la ingeniería de prompts de artesanía a **compilación dirigida por métricas**.

Todos comparten la idea de esta lección: la mejora la decide la **evaluación**, no el gusto.

## Mini-ejemplo trabajado

Tu asistente extrae datos de facturas pero falla en ~20% de los casos. Optimización dirigida:
1. **Set de evaluación:** 50 facturas con su extracción correcta.
2. **Base:** prompt actual → 80% exacto.
3. **Cambio 1 (few-shot):** añades 3 ejemplos resueltos → mides → 88%. **Conservas.**
4. **Cambio 2 (CoT):** "razona el tipo de cada campo antes de extraer" → mides → 86% (¡bajó! añadió ruido en una tarea de extracción). **Descartas.**
5. **Cambio 3 (formato JSON estricto + "si falta un campo, null"):** → 92%. **Conservas.**

Sin medir, habrías "sentido" que CoT ayudaba (suena sofisticado) y lo habrías dejado, empeorando. Predicción antes de seguir: subes la métrica del set a 99% iterando muchísimos cambios sobre **esos mismos 50 ejemplos**. ¿Es seguro asumir 99% en producción? → No: corres riesgo de **sobreajustar al set de evaluación** (lo memorizaste). Necesitas un **set de prueba aparte** (held-out) que no usaste para optimizar, igual que train/test en ML.

## Señales de reconocimiento

| Señal | Jugada |
|---|---|
| "Cambié el prompt y me parece mejor" | Mídelo contra un set; "parece" no basta |
| Tarea de razonamiento que falla | Chain-of-thought (+ self-consistency) |
| Formato de salida inconsistente | Few-shot + formato explícito (JSON) |
| Mega-prompt que pide diez cosas | Descomponer en sub-prompts encadenados |
| "99% en mi set tras 50 cambios" | Riesgo de overfitting → set held-out |

## Errores típicos

- **Optimizar por intuición:** sin métrica ni set, cada cambio es una apuesta; cosas que "suenan mejor" (como CoT) a veces empeoran según la tarea.
- **Cambiar varias cosas a la vez:** no sabes cuál ayudó; cambia una y mide.
- **Sobreajustar al set de evaluación:** iterar mil veces sobre los mismos ejemplos los memoriza; usa held-out.
- **Ignorar la seguridad del prompt:** meter datos no confiables en el prompt abre **prompt injection** ([[cyber-llm1]]); el prompt no es un lugar para secretos ([[cyber-llm3]], LLM07).

## Contraejemplo y caso borde

- **Contraejemplo (la técnica famosa empeora):** chain-of-thought es excelente para razonamiento pero **puede empeorar** tareas simples de clasificación/extracción (añade ruido, latencia y oportunidades de divagar). La evaluación, no la fama de la técnica, decide.
- **Caso borde (el set no representa producción):** si optimizas contra un set que no refleja la distribución real (casos fáciles, un solo idioma), subes la métrica y bajas en producción. La calidad del set de evaluación **es** la calidad de tu optimización.

## Transferencia isomorfa

- **Prompt-eval-loop ↔ entrenamiento dirigido por validación:** cambiar→medir→conservar es el ciclo de cualquier optimización con datos (ML, A/B testing, detection engineering de [[cyber-blue5]]); el prompt es el "parámetro" y la métrica la guía.
- **Overfitting al set ↔ data leakage:** memorizar el set de evaluación infla la métrica como el leakage temporal infla un modelo; la defensa es la misma: held-out / no mirar el futuro.
- **Descomposición ↔ divide y vencerás / agentes:** partir una tarea grande en pasos verificables es el puente con los sistemas agénticos y con el diseño de software ([[cyber-dev3]]).

Moraleja de la arista: *el prompt es código; optimízalo como ingeniería —una técnica decidida por la métrica sobre un set representativo, con held-out— no por gusto.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para una tarea (extracción, resumen o clasificación), propón 3 cambios de prompt y describe el set y la métrica con que decidirías cuál conservar.
- **Misión externa (lab vivo):** lee la [Prompt Engineering Guide](https://www.promptingguide.ai/) (few-shot, CoT) y el paper de [Chain-of-Thought (Wei et al., 2022)](https://arxiv.org/abs/2201.11903). **Criterio de cierre:** explicar una tarea donde CoT ayuda y otra donde estorba.
- **Mini-entregable (mini-proyecto del cluster):** un **protocolo de optimización de prompts dirigida por evaluación**: la métrica, cómo construirías el set (con held-out), qué técnicas probarías y la regla para conservar/descartar un cambio.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (optimización de prompts dirigida por evaluación y held-out) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** probar candidatos de prompt cambiando una variable a la vez y midiendo held-out.
2. **Baseline obligatorio:** prompt elegido por gusto o demo.
3. **Versión mejorada:** prompt seleccionado por métrica en validación y confirmado en held-out.
4. **Evaluación:** delta contra baseline, intervalo de confianza y regresiones por segmento.
5. **Fallo que debes explicar:** 99% en el set iterado pero caída en casos nuevos.
6. **Transferencia:** A/B interno de asistentes, clasificadores o extractores con prompts.

**Laboratorio externo principal:** [DeepLearning.AI Generative AI for Everyone](https://www.deeplearning.ai/courses/generative-ai-for-everyone/).
**Laboratorio alternativo:** [Prompt Engineering Guide](https://www.promptingguide.ai/).
**Ruta de cluster:** harness de evaluación con línea base, prompts candidatos, LLM-as-judge calibrado y reporte de regresiones.

**Entregable:** reporte de experimentos con baseline, candidatos, métricas y decisión. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y que harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** el prompt es el **programa** del LLM y se optimiza como **ingeniería, no por intuición**. Técnicas que rinden —**instrucción/rol/formato, few-shot, chain-of-thought (+ self-consistency), descomposición, grounding**— ayudan **según la tarea**, así que hay que **medir**: define métrica y set ([[gen-eval2]]/[[gen-eval3]]), fija línea base, **cambia una cosa, mide, conserva solo si sube**, y valida en **held-out** para no sobreajustar. La optimización **automática** (APE, DSPy) lleva esto a "compilar prompts dirigidos por datos". Cuidado: una técnica famosa (CoT) puede **empeorar** tareas simples, y el prompt es superficie de **inyección** y no es lugar para secretos.

---

**Referencias**

- Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in LLMs. *NeurIPS*. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
- Brown, T., et al. (2020). Language models are few-shot learners (GPT-3). *NeurIPS*. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Zhou, Y., et al. (2022). Large language models are human-level prompt engineers (APE). *ICLR*. [arXiv:2211.01910](https://arxiv.org/abs/2211.01910)
- Khattab, O., et al. (2023). DSPy: Compiling declarative LM calls into self-improving pipelines. [arXiv:2310.03714](https://arxiv.org/abs/2310.03714)
- DAIR.AI. (n.d.). Prompt Engineering Guide. [promptingguide.ai](https://www.promptingguide.ai/)

*Retrieval: (1) nombra 3 técnicas de prompting y cuándo ayudan; (2) ¿cuáles son los pasos del lazo de optimización dirigida por evaluación?; (3) ¿por qué hace falta un set held-out?; (4) ¿qué es APE/DSPy y qué idea comparten?*
