# Evaluar y medir sistemas de agentes

> Recurso troncal: **MIT-AI.md (Semana 13: "Defining evaluation metrics (e.g., tool accuracy)", "Measuring the effectiveness of agent-based systems")**. Capstone del cluster y de la parte agéntica: cómo saber si tu sistema de agentes funciona de verdad. Integra [[gen-ma1]]–[[gen-ma3]], la evaluación de [[gen-eval4]] y la seguridad de [[cyber-llm2]].

## De qué trata (y qué sabrás hacer al final)

Un sistema multi-agente es lo más complejo del bloque: varios LLMs, herramientas, routing, memoria, RAG adaptativo. Por eso es **donde más fácil te engañas** con una demo impresionante que en producción falla. Esta lección da el marco para medir un sistema agéntico de extremo a extremo y por componente, separando culpas (como el triángulo RAG de [[gen-rag4]]) y midiendo lo que importa: que **complete la tarea**, de forma **eficiente, segura y robusta**.

La intuición: evaluar un sistema de agentes es como **evaluar un equipo, no a una persona**. No basta "el proyecto salió" (resultado final): quieres saber si **cada miembro** hizo bien su parte (¿el investigador trajo buenas fuentes? ¿el revisor detectó los errores?), si el **coordinador** repartió bien, cuánto **costó** y si el equipo resiste a un **saboteador** (adversario). Un resultado bueno con un proceso frágil no es fiable; un resultado malo sin saber **qué eslabón falló** no se puede arreglar.

Al terminar podrás: (1) medir el **resultado de extremo a extremo** (task success); (2) medir **por componente** (tool accuracy, calidad de cada agente, routing); (3) evaluar **eficiencia y robustez/seguridad**; y (4) construir un loop de evaluación y ejecutar el mini-proyecto.

## Métrica reina: éxito de la tarea de extremo a extremo

La pregunta que más importa: ¿el sistema **completó el objetivo** del usuario? **Task success rate** sobre un conjunto de tareas representativas (con held-out, [[gen-eval4]]). Variantes según la tarea: éxito binario (logró/no), parcial (cuántos sub-objetivos), o calidad de la salida final (con LLM-as-judge + rúbrica, [[gen-eval2]]). Sin esta métrica, "mejorar el sistema" es adivinar. Benchmarks de referencia: [AgentBench](https://arxiv.org/abs/2308.03688), [GAIA](https://arxiv.org/abs/2311.12983) (tareas que requieren herramientas), [τ-bench](https://arxiv.org/abs/2406.12045) (agente-usuario-herramientas).

## Medir por componente: separar las culpas

Como un RAG falla en recuperación **o** generación ([[gen-rag4]]), un sistema de agentes falla en algún **eslabón** específico, y medir solo el resultado final no dice cuál. Componentes a medir:
- **Tool accuracy (lo destaca MIT-AI):** ¿el agente eligió la herramienta correcta con los argumentos correctos? Fallo aquí ≠ fallo de razonamiento.
- **Calidad por agente:** ¿el investigador trajo fuentes relevantes? ¿el sintetizador fue fiel? (evaluar cada uno como un mini-sistema).
- **Routing accuracy:** ¿el router mandó cada sub-tarea al agente correcto? ([[gen-ma2]]).
- **Calidad de los pasos intermedios:** ¿la cadena de razonamiento/acciones fue sensata, no solo el resultado?

Medir por componente convierte "el sistema falló" en "el agente de facturación eligió mal la herramienta en el 30% de los casos" — accionable.

## Eficiencia y robustez

- **Eficiencia:** número de pasos/llamadas, **costo** (cómputo/dinero — recuerda que N agentes multiplican el gasto, [[gen-ma2]]) y latencia para lograr la tarea. Un sistema que acierta pero cuesta 10× puede ser inviable.
- **Robustez / seguridad:** ¿resiste entradas adversarias e **inyecciones** que se propagan entre agentes ([[cyber-llm2]])? ¿maneja fallos de herramientas sin colapsar ([[gen-ma2]])? Esto se mide con **red teaming**: casos diseñados para romperlo (un dato de tarea que es una inyección, una API caída, una consulta ambigua). Un sistema que solo pasa los casos felices no está evaluado.

## El loop de evaluación

Igual que en prompts ([[gen-eval4]]) y RAG ([[gen-rag4]]): **evalúa con datos, no con demos**. Construye un set de tareas representativas (+ adversarias + held-out), mide la línea base de extremo a extremo y por componente, cambia **una cosa** (un agente, el router, un prompt), vuelve a medir y conserva solo si mejora sin regresiones. La complejidad de cada capa (más agentes, RAG adaptativo, debate) **debe justificarse midiendo** — si un sistema multi-agente no supera a un agente simple en tu métrica, no lo uses ([[gen-ma1]]).

## Mini-ejemplo trabajado

Tu asistente de investigación multi-agente entrega informes correctos el 70% de las veces. ¿Qué arreglas? **Mide por componente:**
- **Routing:** ¿el coordinador dividió bien las sub-preguntas? Si descompuso mal en el 25% → arregla el orquestador.
- **Tool accuracy:** ¿los investigadores eligieron bien las herramientas de búsqueda? Si fallan argumentos → arregla sus prompts/herramientas.
- **Síntesis:** ¿el sintetizador fue fiel a lo recuperado (faithfulness, [[gen-eval3]])? Si inventa → refuerza anclaje.
- **Robustez:** ¿qué pasa si una fuente trae una inyección? Red team.

Sin medir por componente, "subir el 70%" sería tocar a ciegas. Predicción antes de seguir: el sistema sube a 95% en tu set… tras iterar 100 veces sobre **los mismos** casos. ¿Confías en producción? → No: overfitting al set de evaluación ([[gen-eval4]]); necesitas **held-out** y casos nuevos. La trampa es la misma a nivel de sistema que de prompt.

## Señales de reconocimiento

| Señal | Jugada |
|---|---|
| "El sistema falla pero no sé en qué eslabón" | Medir por componente (tool accuracy, routing, por agente) |
| "Funciona en la demo" | Set de tareas + adversarios + held-out |
| "Acierta pero cuesta carísimo/lento" | Medir eficiencia (pasos, costo, latencia) |
| "¿Resiste una inyección entre agentes?" | Red teaming del sistema |
| "Multi-agente no supera al agente simple" | No uses multi-agente (no se justifica) |

## Errores típicos

- **Medir solo el resultado final:** no localiza el eslabón que falla; mide por componente.
- **Confiar en demos:** un sistema agéntico impresiona en demo y cae ante el primer caso adversario.
- **Ignorar costo/latencia:** un sistema correcto pero carísimo es inviable; la eficiencia es parte de la métrica.
- **No hacer red teaming:** las inyecciones que se propagan entre agentes ([[cyber-llm2]]) solo se ven probándolas.
- **Overfitting al set:** iterar sobre los mismos casos infla la métrica; usa held-out.

## Contraejemplo y caso borde

- **Contraejemplo (evaluación que autoriza la simplicidad):** mides y descubres que un **agente único** logra el 90% donde tu sistema multi-agente logra 88% al triple de costo → la evaluación te dice que **no** uses multi-agente. La métrica protege de la sobreingeniería ([[gen-ma1]]).
- **Caso borde (la métrica no captura el daño):** un sistema con alto task success puede aun así ser inseguro (cae ante una inyección que causa una acción dañina). Task success y seguridad son **dimensiones distintas**; un sistema "exitoso" pero explotable no está listo. Mide ambas.

## Transferencia isomorfa

- **Evaluar por componente ↔ triángulo RAG / separar culpas:** localizar el eslabón que falla (recuperación vs generación; routing vs tool vs síntesis) es el mismo diagnóstico de [[gen-rag4]] y de separar data leakage de model error.
- **Red teaming del sistema ↔ emulación adversaria:** probar a romperlo a propósito antes que el atacante es el [[cyber-blue5]] aplicado a agentes.
- **La métrica autoriza la complejidad ↔ usa lo más simple que funcione:** el mismo principio de [[gen-ag4]] (agente vs workflow) y [[gen-rag4]] (RAG avanzado): cada capa se justifica midiendo.

Moraleja de la arista: *evalúa un sistema de agentes como a un equipo: el resultado de extremo a extremo (task success) Y por componente (tool accuracy, routing, cada agente), con eficiencia y red teaming — y deja que la métrica, no la moda, justifique la complejidad.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para un sistema multi-agente de soporte, define la métrica de extremo a extremo, dos métricas por componente, y dos casos adversarios para red team.
- **Misión externa (lab vivo):** hojea [AgentBench](https://arxiv.org/abs/2308.03688) y [GAIA (Mialon et al., 2023)](https://arxiv.org/abs/2311.12983). **Criterio de cierre:** explicar por qué medir solo el resultado final no basta.
- **Mini-entregable (mini-proyecto del cluster):** un **plan de evaluación de un sistema multi-agente**: métrica de éxito de tarea, métricas por componente (incluida tool accuracy), eficiencia (costo/pasos), casos adversarios (red team) y cómo evitarías overfitting (held-out). Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** evaluar un sistema de agentes es evaluar **un equipo**: la métrica reina es el **éxito de tarea de extremo a extremo** (task success sobre un set con held-out), pero hay que medir **por componente** —**tool accuracy**, routing, calidad de cada agente y de los pasos— para localizar **qué eslabón** falla (como el triángulo RAG). Añade **eficiencia** (pasos, costo, latencia — N agentes multiplican el gasto) y **robustez/seguridad** vía **red teaming** (inyecciones que se propagan, fallos de herramientas). Evalúa **con datos, no demos**, evita overfitting con held-out, y deja que la **métrica justifique la complejidad**: si multi-agente no supera a un agente simple, no lo uses.

---

**Referencias**

- Liu, X., et al. (2023). AgentBench: Evaluating LLMs as agents. *ICLR*. [arXiv:2308.03688](https://arxiv.org/abs/2308.03688)
- Mialon, G., et al. (2023). GAIA: A benchmark for general AI assistants. *ICLR*. [arXiv:2311.12983](https://arxiv.org/abs/2311.12983)
- Yao, S., et al. (2024). τ-bench: A benchmark for tool-agent-user interaction in real-world domains. [arXiv:2406.12045](https://arxiv.org/abs/2406.12045)
- Anthropic. (2024). How we built our multi-agent research system. [anthropic.com](https://www.anthropic.com/engineering/multi-agent-research-system)

*Retrieval: (1) ¿cuál es la métrica reina y por qué no basta sola?; (2) ¿qué se mide por componente (tool accuracy, routing…)?; (3) ¿cómo se evalúa la robustez/seguridad?; (4) ¿cómo decide la evaluación si usar multi-agente?*
