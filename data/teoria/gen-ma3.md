# RAG adaptativo en sistemas agénticos

> Recurso troncal: **MIT-AI.md (Semana 13: "Applying adaptive RAG in generative AI systems")**. Une el RAG ([[gen-rag4]]) con los agentes ([[gen-ag3]]): recuperar deja de ser un paso fijo y se vuelve una decisión del agente. Sigue a [[gen-ma2]] (orquestación) y prepara [[gen-ma4]] (evaluación).

## De qué trata (y qué sabrás hacer al final)

El RAG básico ([[gen-rag1]]) recupera **siempre, una vez, lo mismo**: embebe la pregunta, trae $k$ fragmentos, responde. Pero muchas preguntas no encajan en ese molde: unas no necesitan recuperar nada, otras necesitan **varias** búsquedas encadenadas, otras requieren **reformular** la consulta o **decidir qué fuente** consultar. El **RAG adaptativo** (o **RAG agéntico**) pone la recuperación bajo el control de un agente que **decide cuándo, qué y cuántas veces** buscar. Es la convergencia de los dos clusters: un agente cuya herramienta principal es recuperar.

La intuición: el RAG básico es como un estudiante que, ante **cualquier** pregunta, abre **siempre** el mismo libro en una página fija y copia — aunque la pregunta no necesite el libro, o necesite tres libros distintos. El RAG adaptativo es un estudiante experto: **decide** si necesita consultar (¿lo sé ya?), **elige** qué fuente, **reformula** su búsqueda si la primera no sirvió, y **repite** hasta tener evidencia suficiente. Pasa de "recuperar por reflejo" a "recuperar con criterio".

Al terminar podrás: (1) explicar por qué el RAG fijo se queda corto; (2) describir el **RAG adaptativo/agéntico** (decidir, enrutar, iterar); (3) reconocer patrones (Self-RAG, RAG multi-paso, routing de fuentes); y (4) razonar su tradeoff (potencia vs costo/complejidad).

## Por qué el RAG fijo se queda corto

Recuperar siempre-una-vez-lo-mismo falla en casos comunes:
- **No hace falta recuperar:** "hola", "resume este texto que te di" → recuperar añade ruido y costo ([[gen-rag4]], RAG adaptativo decide **no** buscar).
- **Una búsqueda no basta:** "compara el ingreso de X en 2024 vs 2025" requiere **dos** recuperaciones (eco del agente de [[gen-ag3]]).
- **La consulta cruda recupera mal:** una pregunta vaga necesita **reformularse** antes de buscar (query rewriting, [[gen-rag4]]).
- **Hay varias fuentes:** una pregunta legal va a la base legal; una técnica, a la documentación → **routing de fuentes** ([[gen-ma2]]).

El RAG fijo ignora todo esto. El adaptativo lo decide caso a caso.

## RAG adaptativo / agéntico: recuperar con criterio

El patrón: un agente (el LLM como política, [[gen-ag3]]) trata la **recuperación como una herramienta** que invoca cuando, como y cuantas veces convenga, en un bucle ReAct:
- **Decidir si recuperar:** ¿necesito información externa o puedo responder ya? ([Self-RAG, Asai et al., 2023](https://arxiv.org/abs/2310.11511) entrena al modelo para decidirlo).
- **Reformular/expandir** la consulta antes de buscar.
- **Enrutar** a la fuente correcta (multi-índice).
- **Iterar:** buscar, evaluar si lo recuperado basta, y **volver a buscar** con una consulta refinada si no (RAG multi-paso).
- **Criticar:** ¿el contexto recuperado sostiene mi respuesta? Si no, recupera más o di que no sabe (anti-alucinación, [[gen-eval3]]).

Es el bucle del agente ([[gen-ag1]]) aplicado a la recuperación: percibir (¿qué me falta?) → actuar (buscar) → observar (¿basta?) → repetir.

## En un sistema multi-agente

En un equipo de agentes ([[gen-ma1]]), el RAG adaptativo suele encarnarse como un **agente recuperador** especializado al que otros consultan, o como la capacidad de cada agente de buscar en su dominio. La **memoria de largo plazo** del sistema (que es RAG, [[gen-ag3]]) también se consulta adaptativamente: un agente recupera de la memoria compartida solo lo relevante a su sub-tarea. El routing de [[gen-ma2]] decide qué agente/fuente atiende cada necesidad de información.

## Mini-ejemplo trabajado

Pregunta a un asistente: "¿Cuál es la diferencia entre nuestra política de reembolsos de 2024 y la actual, y cumple con la nueva regulación europea?"
- **RAG fijo:** una búsqueda con la pregunta cruda → recupera fragmentos mezclados, responde incompleto.
- **RAG adaptativo:** el agente **descompone**: (1) recupera la política 2024 (fuente: histórico), (2) recupera la política actual (fuente: vigente), (3) recupera la regulación europea relevante (fuente: legal) — **routing** a tres fuentes—, (4) **evalúa** si tiene todo; si la regulación recuperada es vaga, **reformula y vuelve a buscar**, (5) sintetiza con citas. Cada paso es una decisión.

Predicción antes de seguir: el agente, tras dos búsquedas, **no encuentra** la regulación europea en el corpus. ¿Qué debe hacer un RAG adaptativo bien diseñado? → reconocer la **ausencia de evidencia** y decir "no tengo la regulación europea en mis fuentes" en vez de inventarla (la trampa de [[gen-eval3]]). Adaptativo no significa "insistir hasta inventar"; significa **saber cuándo parar y admitir el límite**.

## Señales de reconocimiento

| Señal | Jugada |
|---|---|
| "Para esta pregunta no hace falta buscar" | RAG adaptativo: decidir NO recuperar |
| "La pregunta tiene varias partes/fuentes" | Multi-paso + routing de fuentes |
| "La búsqueda cruda recupera mal" | Reformular la consulta antes de buscar |
| "Una sola búsqueda no alcanzó" | Iterar: evaluar y volver a buscar refinado |
| "No está en el corpus" | Admitir el límite, no inventar |

## Errores típicos

- **Recuperar siempre por reflejo:** añade ruido y costo cuando no hace falta; el adaptativo decide.
- **Iterar sin criterio de parada:** buscar en bucle hasta inventar o disparar el costo (límites de [[gen-ma2]]).
- **Una sola fuente para todo:** sin routing, preguntas de dominios distintos recuperan mal.
- **Confundir 'más búsquedas' con 'mejor':** como subir $k$ ([[gen-rag3]]), más no es mejor; mejor recuperación sí.

## Contraejemplo y caso borde

- **Contraejemplo (RAG fijo basta):** para un FAQ sobre un solo documento con preguntas simples, el RAG fijo (una búsqueda, $k$ fragmentos) es más simple, barato y predecible que un agente adaptativo. La adaptatividad se justifica con preguntas complejas/multi-fuente, no siempre.
- **Caso borde (costo y latencia explotan):** un RAG adaptativo que itera y enruta puede hacer muchas llamadas → latencia y costo altos, y más oportunidades de inyección (cada fuente recuperada es no confiable, [[cyber-llm2]]). La potencia tiene precio; mídelo ([[gen-ma4]]).

## Transferencia isomorfa

- **RAG adaptativo ↔ el agente aplicado a recuperar:** es el bucle ReAct de [[gen-ag3]] con "buscar" como acción; percibir el vacío de información, actuar buscando, observar si basta, repetir.
- **Decidir si recuperar ↔ agencia/esfuerzo mínimo:** no uses la herramienta pesada si no hace falta — el cuadrante de [[gen-ag1]] y la economía del RAG adaptativo de [[gen-rag4]].
- **Routing de fuentes ↔ índices y control de acceso:** elegir la fuente correcta (y solo la permitida) es routing ([[gen-ma2]]) + control de acceso por documento ([[cyber-llm2]]).

Moraleja de la arista: *el RAG adaptativo es un agente cuya herramienta es recuperar: decide si buscar, qué fuente, cómo reformular y cuándo parar — incluido admitir que no está en el corpus.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para "compara dos contratos y di si cumplen la nueva ley", traza el plan de un RAG adaptativo (qué decide, qué fuentes, cuándo itera, cuándo admite el límite).
- **Misión externa (lab vivo):** repasa [Self-RAG (Asai et al., 2023)](https://arxiv.org/abs/2310.11511) y la idea de [RAG agéntico en LlamaIndex](https://docs.llamaindex.ai/en/stable/use_cases/agents/). **Criterio de cierre:** explicar cuándo el agente debe decidir NO recuperar.
- **Mini-entregable:** un flujo de RAG adaptativo para una pregunta multi-fuente, marcando los puntos de decisión (recuperar/no, reformular, enrutar, iterar, parar).

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (RAG adaptativo y agentes que deciden que recuperar) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** comparar always-retrieve contra retrieval condicional y reintentos guiados.
2. **Baseline obligatorio:** siempre recuperar k documentos.
3. **Versión mejorada:** RAG adaptativo con decisión de query, k y re-ranking.
4. **Evaluación:** decisión accuracy de retrieval, faithfulness, costo y context precisión.
5. **Fallo que debes explicar:** el agente recupera ruido y lo convierte en argumento final.
6. **Transferencia:** asistentes expertos que alternan memoria interna, búsqueda y herramientas.

**Laboratorio externo principal:** [RAGAS](https://docs.ragas.io/).
**Laboratorio alternativo:** [LangGraph tutorials](https://langchain-ai.github.io/langgraph/tutorials/).
**Ruta de cluster:** sistema multi-agente con roles, grafo de estado, presupuesto, red team y comparación contra agente unico.

**Entregable:** policy de retrieval con trazas, fuentes y evaluación por consulta. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y que harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** el **RAG fijo** (recuperar siempre-una-vez-lo-mismo) falla cuando no hace falta buscar, hacen falta varias búsquedas, la consulta debe reformularse o hay varias fuentes. El **RAG adaptativo/agéntico** pone la recuperación bajo un agente que **decide si recuperar, qué fuente, cómo reformular, cuándo iterar y cuándo parar** (incluido admitir que no está en el corpus, anti-alucinación). Es el **bucle ReAct aplicado a recuperar**; en sistemas multi-agente vive como un recuperador especializado y memoria consultada con criterio. Su potencia cuesta latencia, dinero y más superficie de inyección: justifícalo midiendo.

---

**Referencias**

- Asai, A., et al. (2023). Self-RAG: Learning to retrieve, generate, and critique through self-reflection. *ICLR*. [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
- Jeong, S., et al. (2024). Adaptive-RAG: Learning to adapt retrieval-augmented LLMs through question complexity. *NAACL*. [arXiv:2403.14403](https://arxiv.org/abs/2403.14403)
- LlamaIndex. (n.d.). Agentic strategies / agents. [docs.llamaindex.ai](https://docs.llamaindex.ai/en/stable/use_cases/agents/)

*Retrieval: (1) ¿por qué el RAG fijo se queda corto?; (2) ¿qué decide un RAG adaptativo?; (3) ¿qué relación tiene con el bucle ReAct?; (4) ¿qué debe hacer si la respuesta no está en el corpus?*
