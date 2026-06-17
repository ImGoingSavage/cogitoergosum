# Orquestación: routing dinámico y manejo de errores entre agentes

> Recurso troncal: **MIT-AI.md (Semana 13: "dynamic task routing", "handling uncertainty and errors")**. El pegamento que hace funcionar a un sistema multi-agente ([[gen-ma1]]). Prepara [[gen-ma3]] (adaptive RAG) y [[gen-ma4]] (evaluación).

## De qué trata (y qué sabrás hacer al final)

Tener varios agentes no sirve si no se **coordinan** bien. La orquestación responde dos preguntas: ¿**a quién** le toca cada sub-tarea (routing)? y ¿qué pasa cuando algo **falla** (manejo de errores e incertidumbre)? Aquí está la diferencia entre un sistema multi-agente que en la demo brilla y uno que en producción no se cae, no entra en bucles ni dispara costos.

La intuición: la orquestación es el **director de orquesta** (o el jefe de turno de una cocina). Su trabajo no es tocar un instrumento, sino decidir **quién** entra y cuándo (routing), escuchar si alguien desafina y **corregir** (manejo de errores), y asegurar que el conjunto suene coherente. Sin director, músicos brillantes producen ruido; con un mal director, también.

Al terminar podrás: (1) explicar el **routing dinámico** (decidir qué agente/herramienta según la entrada); (2) diseñar **manejo de errores** entre agentes (reintento, fallback, escalada); (3) razonar el control de **bucles, costo y deriva**; y (4) reconocer la orquestación como **superficie de fallo y de ataque**.

## Routing dinámico: a quién le toca

El **router** decide, según la sub-tarea o la entrada, **qué agente o herramienta** debe atenderla. Formas:
- **Por reglas:** si la consulta es de facturación → agente de facturación; si es técnica → agente técnico. Predecible y barato.
- **Por clasificador/LLM:** un modelo clasifica la intención y enruta. Flexible para casos no anticipados.
- **Jerárquico:** un orquestador descompone y asigna ([[gen-ma1]], orquestador-trabajadores).

El routing es donde se decide la eficiencia: enrutar bien evita que un agente caro/lento atienda algo trivial (eco del cuadrante de [[gen-ag1]] y del RAG adaptativo de [[gen-rag4]]: no uses la herramienta pesada si no hace falta). Mal routing = sub-tareas al agente equivocado = resultados pobres.

## Manejo de errores e incertidumbre

En un sistema con N agentes y herramientas, **algo siempre falla**: una API cae, un agente devuelve basura, un sub-resultado es incierto. La orquestación robusta:
- **Reintento con backoff:** ante un fallo transitorio, reintentar (con espera creciente), no rendirse a la primera.
- **Fallback:** si el agente/herramienta preferido falla, una alternativa (otra fuente, otro método, una respuesta degradada).
- **Escalada a humano:** si la incertidumbre es alta o la acción es sensible, parar y pedir ayuda ([[gen-ag4]], humano en el lazo).
- **Validación entre etapas:** el orquestador verifica el resultado de un agente antes de pasarlo al siguiente (no propagar errores ni inyecciones, [[gen-ma1]]).
- **Manejo de incertidumbre:** propagar "no estoy seguro" en vez de afirmar; un sub-resultado dudoso debe marcarse, no enterrarse.

Principio: *el sistema es tan robusto como su peor manejo de fallos*; un agente brillante con orquestación frágil colapsa ante el primer error real.

## Bucles, costo y deriva: los límites duros

Los sistemas multi-agente tienen modos de fallo propios que la orquestación debe acotar (de [[gen-ag4]], a escala de equipo):
- **Bucles infinitos:** agente A pide a B, B pide a A… → límite de pasos/profundidad y detección de no-progreso.
- **Explosión de costo:** cada agente y reintento cuesta cómputo/dinero; N agentes pueden multiplicar el gasto → presupuesto global y por agente (*denial of wallet*, [[cyber-llm4]]).
- **Deriva del objetivo:** en cadenas largas, el sistema se aleja de la meta paso a paso → el orquestador re-ancla en el objetivo original periódicamente.

## Mini-ejemplo trabajado: asistente de soporte multi-agente

Sistema: router + agentes de facturación, técnico y de cuenta.
- **Routing:** llega "no puedo iniciar sesión" → el router (clasificador) lo manda al agente técnico. Llega "¿por qué me cobraron de más?" → al de facturación.
- **Error:** el agente técnico llama a la API de estado del sistema y **falla** → reintento con backoff; si persiste, **fallback** a la base de incidencias conocidos; si nada resuelve, **escala a humano**.
- **Validación:** antes de responder al usuario, el orquestador verifica que la respuesta del agente sea coherente y no contenga datos de otro cliente (no propagar fuga, [[cyber-llm2]]).
- **Límites:** máximo de saltos entre agentes y presupuesto por conversación.

Predicción antes de seguir: el agente técnico, al fallar, **inventa** un estado del sistema ("todo está operativo") en vez de reportar el fallo. ¿Qué control lo evita? → manejo de incertidumbre: el agente debe **decir que no pudo** y la orquestación debe **detectar el fallo de la herramienta**, no aceptar una afirmación no anclada. Un fallo silenciado es peor que un fallo reportado.

## Señales de reconocimiento

| Señal | Jugada de orquestación |
|---|---|
| "Distintas consultas necesitan distintos agentes" | Routing (reglas o clasificador) |
| "Una API/agente puede fallar" | Reintento + fallback + escalada |
| "Agentes se llaman en círculo" | Límite de pasos / detección de no-progreso |
| "El costo se dispara con varios agentes" | Presupuesto global y por agente |
| "En cadenas largas se desvía del objetivo" | Re-anclar la meta periódicamente |

## Errores típicos

- **Asumir que las herramientas/agentes nunca fallan:** el camino feliz no existe en producción; diseña para el fallo.
- **Sin límites de pasos/costo:** bucles y explosión de gasto.
- **Propagar resultados sin validar:** errores e inyecciones saltan entre agentes.
- **Silenciar la incertidumbre:** un sub-resultado dudoso tratado como cierto envenena la respuesta final.

## Contraejemplo y caso borde

- **Contraejemplo (routing simple gana):** si solo hay dos tipos de consulta bien definidos, un router **por reglas** es más fiable y barato que un clasificador LLM; no toda decisión de routing necesita un modelo. Lo simple primero.
- **Caso borde (fallo en cascada):** un agente del que dependen muchos otros cae y arrastra a todo el sistema (punto único de fallo). La orquestación necesita **aislamiento** y degradación: que el fallo de una parte no tumbe el todo (resiliencia, [[cyber-ms5]]).

## Transferencia isomorfa

- **Orquestación ↔ sistemas distribuidos:** routing, reintentos con backoff, fallback, circuit breakers, timeouts y límites son los patrones clásicos de microservicios/sistemas distribuidos (diseño de sistemas) aplicados a agentes. Un sistema multi-agente **es** un sistema distribuido cuyos nodos son LLMs.
- **Validación entre etapas ↔ trust boundaries:** verificar lo que pasa de un agente a otro es revisar la frontera de confianza en cada salto ([[cyber-llm2]]).
- **Manejo de incertidumbre ↔ decir 'no sé':** propagar la duda en vez de inventar es la misma disciplina anti-alucinación de [[gen-eval3]].

Moraleja de la arista: *un sistema multi-agente es un sistema distribuido de LLMs; la orquestación —routing, manejo de errores, límites, validación entre etapas— decide si funciona, y es su mayor superficie de fallo.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el asistente de soporte, define las reglas de routing, la cadena reintento→fallback→escalada para un fallo de API, y los límites (pasos, presupuesto).
- **Misión externa (lab vivo):** hojea cómo orquestan [LangGraph](https://langchain-ai.github.io/langgraph/) o [AutoGen](https://microsoft.github.io/autogen/) (grafos de agentes, estado, control de flujo). **Criterio de cierre:** explicar cómo evitarían un bucle infinito entre agentes.
- **Mini-entregable:** un diagrama de orquestación de un sistema multi-agente con el router, las rutas de error (reintento/fallback/escalada) y los límites duros marcados.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (orquestacion, routing dinámico y manejo de errores) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** implementar un router que elija especialista, limite pasos y maneje tool errors.
2. **Baseline obligatorio:** conversacion libre entre agentes sin límites.
3. **Versión mejorada:** orquestacion por grafo con contratos, timeouts y fallback.
4. **Evaluación:** routing accuracy, loops evitados, latencia y fallback success.
5. **Fallo que debes explicar:** los agentes entran en bucle o pasan errores sin verificar.
6. **Transferencia:** sistemas de soporte con dominios, escalamiento y SLAs.

**Laboratorio externo principal:** [LangGraph tutorials](https://langchain-ai.github.io/langgraph/tutorials/).
**Laboratorio alternativo:** [Microsoft AutoGen](https://microsoft.github.io/autogen/).
**Ruta de cluster:** sistema multi-agente con roles, grafo de estado, presupuesto, red team y comparación contra agente unico.

**Entregable:** grafo de estado con casos de exito, fallo y recuperación. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y que harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** la **orquestación** hace funcionar a un sistema multi-agente respondiendo **a quién** (routing: por reglas, clasificador o jerárquico — enrutar bien evita usar el agente caro para lo trivial) y **qué pasa al fallar** (reintento con backoff, fallback, **escalada a humano**, validación entre etapas y manejo de la incertidumbre). Debe acotar modos de fallo propios: **bucles** (límite de pasos), **costo** (presupuesto) y **deriva** (re-anclar la meta). Un sistema multi-agente **es un sistema distribuido de LLMs**: la orquestación es su mayor superficie de fallo y de ataque (errores e inyecciones se propagan entre agentes).

---

**Referencias**

- Anthropic. (2024). How we built our multi-agent research system. [anthropic.com](https://www.anthropic.com/engineering/multi-agent-research-system)
- LangChain. (n.d.). LangGraph: Build stateful, multi-actor LLM applications. [langchain-ai.github.io](https://langchain-ai.github.io/langgraph/)
- Wu, Q., et al. (2023). AutoGen. [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)

*Retrieval: (1) ¿qué decide el routing y de qué formas?; (2) nombra la cadena de manejo de errores entre agentes; (3) ¿qué modos de fallo propios acota la orquestación (bucles/costo/deriva)?; (4) ¿por qué un sistema multi-agente es un sistema distribuido?*
