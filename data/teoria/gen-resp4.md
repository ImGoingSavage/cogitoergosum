# Casos por vertical: aplicar GenAI a problemas reales de negocio

> Recurso troncal: **MIT-AI.md ("Practical Industry Use Cases & Applied Projects")**. Capstone de la Fase 9: integrar todo —transformers, RAG, evaluación, agentes, multi-agente, IA responsable— en soluciones reales por industria. Método de caso aplicado a construir, no solo a analizar.

## De qué trata (y qué sabrás hacer al final)

Toda la Fase 9 converge aquí: ante un **problema de negocio** real, ¿qué pieza de GenAI usas y cómo la armas, evalúas y gobiernas? Esta lección recorre los casos por vertical del programa MIT (consumer tech, e-commerce, seguros, finanzas, supply chain, legal) y, para cada uno, **elige la técnica correcta** y aplica el marco completo. No es teoría nueva: es **transferir** lo aprendido a decisiones de arquitectura.

La intuición: terminaste un curso de cocina (técnicas: cortar, saltear, emulsionar) y ahora te dan **comensales reales con pedidos concretos**. La habilidad ya no es "saber saltear", sino **elegir qué técnica usar para este plato**, ejecutarla, probarla y servirla consistente. Los casos por vertical son ese examen final: dado el problema, ¿clasificación, RAG, agente o multi-agente? ¿cómo lo evalúas? ¿qué riesgos responsables y de seguridad?

Al terminar podrás: (1) **mapear** un problema de negocio a la técnica GenAI correcta; (2) reconocer el patrón de cada vertical del MIT; (3) aplicar **evaluación, responsabilidad y seguridad** a cada caso; y (4) ejecutar el mini-proyecto integrador del cluster.

## La pregunta de arquitectura: ¿qué pieza usar?

Antes de construir, elige —usando todo el bloque— la solución **más simple que resuelva**:
- ¿Es **clasificar/extraer** texto? → modelo + buena evaluación (no necesitas agente). 
- ¿La respuesta depende de **conocimiento propio**? → **RAG** ([[gen-rag1]]).
- ¿Hace falta **decidir pasos y actuar**? → **agente** ([[gen-ag4]]) — y solo si los pasos no son fijos.
- ¿La tarea es grande y **divisible** con sub-roles? → **multi-agente** ([[gen-ma1]]) — solo si lo justifica la métrica.

Regla transversal del bloque: **no uses la pieza más compleja por moda; úsala si la métrica lo justifica** ([[gen-ag4]], [[gen-ma4]], [[gen-rag4]]).

## Los casos del MIT, mapeados

| Vertical (MIT-AI.md) | Problema | Pieza GenAI | Clave |
|---|---|---|---|
| **Consumer tech** — sentimiento de producto | Analizar reseñas de smartwatch (sentimiento, aspectos) | Clasificación / análisis con LLM | Evaluación rigurosa; no necesita agente |
| **E-commerce** — recomendaciones | Personalizar con historial + carrito + clics | Filtrado colaborativo / por contenido (+ embeddings) | Métricas de conversión; sesgo/privacidad |
| **Seguros** — asistente de pólizas | Responder dudas con base en pólizas | **RAG** | Fidelidad + atribución; no alucinar términos |
| **Finanzas** — asesor de inversión | Respuestas fiables sobre inversión/compliance | **RAG + consistency checks + prompt optimization** | Anti-alucinación crítica; cumplimiento |
| **Supply chain** — reabastecimiento | Monitorear stock, pronosticar, generar órdenes | **Agente** (forecasting + acciones) | Agencia mínima; humano en el lazo para órdenes |
| **Legal** — inteligencia regulatoria | Recuperar y sintetizar regulación, resumir compliance | **Multi-agente / RAG agéntico + LLM-eval** | Routing de fuentes; fidelidad; auditoría |

Patrón: a más **conocimiento propio**, RAG; a más **acción**, agente; a más **complejidad divisible**, multi-agente; siempre con **evaluación** y, en dominios sensibles (salud/finanzas/legal), **anti-alucinación, atribución y responsabilidad** fuertes.

## El marco completo aplicado a un caso

Tomemos **finanzas — asesor de inversión** (MIT-AI.md): "mejorar la fiabilidad de un asistente que maneja datos de inversión y compliance mediante consistency checks y prompt optimization dentro de un RAG".
1. **Pieza:** RAG (la respuesta depende de documentos de inversión/regulación) + el asistente.
2. **Construcción:** chunking por estructura ([[gen-rag2]]), recuperación híbrida + re-ranking ([[gen-rag3]]), prompt con "responde solo con el contexto y cita".
3. **Evaluación:** triángulo RAG ([[gen-rag4]]) + **consistency checks** y anclaje contra fuentes ([[gen-eval3]]) — la fiabilidad es el objetivo del caso —, optimizando el prompt dirigido por evaluación ([[gen-eval4]]).
4. **Responsabilidad/seguridad:** anti-alucinación crítica (un dato financiero falso causa daño), atribución para auditoría, control de acceso a documentos ([[cyber-llm2]]), no poner secretos en el prompt ([[cyber-llm3]]), y humano en el lazo para recomendaciones de alto impacto.
5. **Producción:** monitoreo de costo/latencia/faithfulness y re-evaluación ante cambios ([[gen-resp3]]).

Predicción antes de seguir: el equipo, presionado, lanza el asesor financiero **sin** consistency checks ni atribución "porque la demo respondía bien". ¿Qué riesgo corre? → una alucinación financiera con tono seguro ([[gen-eval3]]) puede causar pérdidas reales y responsabilidad legal; en dominios de alta consecuencia, la fiabilidad **es** el producto, no un extra.

## Señales de reconocimiento

| Señal del problema | Pieza |
|---|---|
| "Clasificar/extraer de texto" | Modelo + evaluación (sin agente) |
| "Responder sobre nuestros documentos" | RAG |
| "Decidir pasos y ejecutar acciones" | Agente (si los pasos no son fijos) |
| "Tarea grande con sub-roles" | Multi-agente (si la métrica lo justifica) |
| "Dominio sensible (salud/finanzas/legal)" | Anti-alucinación + atribución + responsabilidad fuertes |

## Errores típicos

- **Usar la pieza de moda, no la adecuada:** multi-agente para algo que es una clasificación; RAG donde no hay conocimiento externo.
- **Saltarse la evaluación por la demo:** lo que funciona en la demo falla en producción y en casos adversarios.
- **Ignorar responsabilidad/seguridad en dominios sensibles:** una alucinación en salud/finanzas/legal tiene consecuencias reales.
- **Olvidar la atribución:** en dominios auditables, responder sin citar la fuente es inservible.

## Contraejemplo y caso borde

- **Contraejemplo (la solución simple gana):** para el caso de **sentimiento de reseñas**, un modelo de clasificación bien evaluado supera a un agente sofisticado — más simple, barato y fiable. No todo problema de GenAI necesita lo último; el caso decide.
- **Caso borde (el caso prohíbe la IA generativa):** en algunos dominios regulados, una decisión de alto impacto **no** puede delegarse a un sistema no explicable o no auditable; la respuesta responsable puede ser usar GenAI solo de **apoyo** (con humano decidiendo) o **no usarla** para esa decisión. La mejor arquitectura a veces es "humano + IA de apoyo", no "IA autónoma".

## Transferencia isomorfa

- **Mapear problema→pieza ↔ método de caso del MIT:** dado un caso, transferir el patrón correcto (como en [[cyber-mit5]]) — aquí para construir, no solo analizar.
- **"La pieza más simple que funcione" ↔ agente vs workflow / RAG fijo vs adaptativo:** el mismo principio de [[gen-ag4]], [[gen-ma1]] y [[gen-rag4]]; la complejidad se justifica midiendo.
- **Dominios sensibles ↔ defensa proporcional:** más consecuencia → más fidelidad, atribución, responsabilidad y humano en el lazo ([[cyber-ms5]], [[cyber-mit1]]).

Moraleja de la arista: *ante un problema real, elige la pieza más simple que lo resuelva (clasificar < RAG < agente < multi-agente), evalúa siempre, y en dominios sensibles haz de la fidelidad, la atribución y la responsabilidad el producto, no un extra.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para los seis verticales del MIT, di qué pieza GenAI usarías y una métrica de evaluación clave para cada uno.
- **Misión externa (lab vivo):** elige un caso del MIT-AI.md (p. ej. asistente de seguros o asesor de inversión) y revisa una guía real de implementación (RAG, evaluación) de [LangChain](https://python.langchain.com/docs/tutorials/rag/) o [LlamaIndex](https://docs.llamaindex.ai/). **Criterio de cierre:** justificar la pieza elegida y cómo la evaluarías.
- **Mini-entregable (mini-proyecto del cluster):** un **diseño de solución GenAI de extremo a extremo** para un problema de negocio (elige un vertical): la pieza (con justificación), la arquitectura (chunking/recuperación/agente según aplique), el **plan de evaluación**, las medidas de **IA responsable** (equidad/transparencia/privacidad) y de **seguridad**, y la operación en producción. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** los casos por vertical son el **examen final**: dado un problema de negocio, **elige la pieza más simple que lo resuelva** —clasificar/extraer < **RAG** (conocimiento propio) < **agente** (acción) < **multi-agente** (complejidad divisible)— guiado por la métrica, no por la moda. Mapea cada caso (seguros→RAG, supply chain→agente, legal→multi-agente/RAG agéntico…), **evalúa siempre**, y en **dominios sensibles** (salud, finanzas, legal) haz de la **fidelidad, la atribución y la responsabilidad** el producto, con humano en el lazo. A veces la mejor arquitectura es **humano + IA de apoyo**, o no usar IA para esa decisión.

---

**Referencias**

- Massachusetts Institute of Technology. (n.d.). *Generative AI, Responsible AI, and Agentic AI* — Practical industry use cases. MIT Professional Education.
- Huyen, C. (2022). *Designing machine learning systems*. O'Reilly. [Sitio](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)
- LangChain. (n.d.). Build a RAG app (tutorial). [python.langchain.com](https://python.langchain.com/docs/tutorials/rag/)
- LlamaIndex. (n.d.). Documentation. [docs.llamaindex.ai](https://docs.llamaindex.ai/)

*Retrieval: (1) ¿cómo eliges entre clasificación, RAG, agente y multi-agente?; (2) ¿qué pieza usarías para un asistente de pólizas de seguros y por qué?; (3) ¿qué cambia en dominios sensibles (finanzas/salud/legal)?; (4) ¿cuándo la mejor arquitectura es "humano + IA de apoyo" o no usar IA?*
