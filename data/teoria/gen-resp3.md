# GenAI en producción: del prototipo al sistema confiable

> Recurso troncal: **MIT-AI.md (integración, despliegue, ciclo de vida)**. El abismo entre "funciona en mi notebook" y "funciona para miles de usuarios sin caerse ni arruinarte". Integra todo el bloque y conecta con ML Systems ([[cyber-mls5]]) y la operación segura. Prepara [[gen-resp4]] (casos por vertical).

## De qué trata (y qué sabrás hacer al final)

Construir un demo de GenAI es fácil; llevarlo a **producción** es donde la mayoría fracasa. En producción hay usuarios reales, costo por token, latencia que importa, fallos, ataques, deriva y obligación de monitorear. Esta lección reúne las prácticas que convierten un prototipo en un sistema **confiable, sostenible y observable** — el MLOps específico de la IA generativa (a veces "LLMOps").

La intuición: un prototipo es como un **plato cocinado una vez para un amigo**; producción es **abrir un restaurante** — el mismo plato, pero servido a cientos al día, con costos controlados, tiempos consistentes, higiene, y un plan para cuando se acabe un ingrediente o un cliente se queje. La receta es la parte fácil; la **operación** es el negocio.

Al terminar podrás: (1) nombrar los retos de producción (**costo, latencia, fiabilidad, seguridad**); (2) razonar **observabilidad y monitoreo** de un sistema GenAI; (3) gestionar **deriva, versiones y evaluación continua**; y (4) aplicar los controles de seguridad/operación a un despliegue.

## Los retos que no se ven en el notebook

- **Costo:** cada llamada al LLM cuesta dinero; a escala, la factura define la viabilidad. Estrategias: caché de respuestas, modelos más pequeños para tareas simples (routing, [[gen-ma2]]), límites por usuario (consumo no acotado, [[cyber-llm4]]), prompts concisos.
- **Latencia:** los usuarios esperan respuestas rápidas; LLMs grandes y cadenas de agentes son lentos. Estrategias: streaming, modelos más rápidos, paralelizar, caché.
- **Fiabilidad:** APIs que fallan, límites de tasa del proveedor, salidas mal formadas. Necesita reintentos, fallbacks, validación de salida ([[gen-ma2]]).
- **No determinismo:** el mismo prompt puede dar salidas distintas; complica testing y reproducibilidad (fija semillas/temperatura donde se pueda, evalúa estadísticamente, [[gen-eval4]]).

## Observabilidad: no puedes mejorar lo que no ves

En producción debes **registrar y monitorear** (con cuidado de privacidad, [[cyber-dp4]]): entradas/salidas, latencia, costo por petición, tasa de error, herramientas llamadas (en agentes), y señales de calidad (faithfulness, satisfacción). Sin trazas no puedes depurar por qué una respuesta fue mala ni detectar una regresión. La observabilidad de GenAI es el [[cyber-blue1]] (logs y detección) aplicado a tu propio sistema: ver, medir, alertar. Hoy hay herramientas dedicadas (tracing de LLM/agentes) que capturan toda la cadena de un agente para poder reconstruir qué pasó.

## Deriva, versiones y evaluación continua

Un sistema GenAI **no es estable** con el tiempo:
- **Deriva de datos/uso:** los usuarios preguntan cosas nuevas; el corpus del RAG cambia. Lo que funcionaba se degrada ([[cyber-blue5]], paralelo con el distribution shift de ML).
- **Cambios de modelo:** el proveedor actualiza el LLM (o lo deprecia) y tu sistema se comporta distinto **sin que tú cambiaras nada**. Por eso hay que **fijar versiones** del modelo cuando se pueda y **re-evaluar** ante cualquier cambio.
- **Evaluación continua:** correr tu set de evaluación ([[gen-eval4]], [[gen-rag4]]) de forma regular (no solo al lanzar) para detectar regresiones — un "CI de calidad" para GenAI.

Regla: *cada cambio (prompt, modelo, corpus, herramienta) dispara re-evaluación.* Sin esto, la calidad se degrada en silencio.

## Seguridad en producción (resumen aplicado)

Todo lo de la ruta de seguridad converge aquí: tratar entradas y contenido recuperado como **no confiables** (prompt injection, [[cyber-llm1]]); **agencia mínima** y humano en el lazo para agentes ([[cyber-llm2]], [[gen-ag4]]); no poner secretos en prompts ([[cyber-llm3]]); rate limiting y cuotas ([[cyber-llm4]]); y red teaming continuo. La seguridad de un sistema GenAI en producción **es** aplicar la Fase 8 a la vez.

## Mini-ejemplo trabajado

Tu asistente RAG funciona perfecto en la demo. En producción, una semana después: la factura se dispara, algunas respuestas tardan 20s, y empezó a alucinar más. Diagnóstico de producción:
- **Costo:** sin caché ni límites; cada usuario hace muchas llamadas → añade caché, límites por usuario, modelo más chico para consultas simples.
- **Latencia:** cadenas largas sin streaming → streaming + paralelizar + re-rankear menos candidatos.
- **Más alucinación:** ¿el proveedor actualizó el modelo? ¿el corpus cambió (deriva)? → fijar versión del modelo, re-evaluar con el set, revisar el corpus.
- **Observabilidad:** sin trazas no lo habrías sabido; con monitoreo de costo/latencia/faithfulness lo detectas a tiempo.

Predicción antes de seguir: el equipo arregla todo "a mano" mirando casos, sin un set de evaluación ni monitoreo. ¿Qué pasará en el próximo cambio del proveedor? → otra regresión silenciosa que descubrirán por quejas de usuarios. Producción sin **evaluación continua y observabilidad** es apagar incendios para siempre.

## Señales de reconocimiento

| Señal | Jugada de producción |
|---|---|
| "La factura del LLM se dispara" | Caché, límites, modelo más chico, routing |
| "Las respuestas tardan demasiado" | Streaming, paralelizar, modelo más rápido |
| "Empeoró sin que cambiáramos nada" | Cambio del proveedor / deriva → fijar versión + re-evaluar |
| "No sé por qué esta respuesta fue mala" | Falta observabilidad/tracing |
| "Solo evaluamos al lanzar" | Evaluación continua (CI de calidad) |

## Errores típicos

- **Tratar el demo como producción:** ignora costo, latencia, fallos, seguridad y deriva.
- **No monitorear:** sin trazas, los problemas se descubren por quejas, no por alertas.
- **No fijar versión del modelo:** el proveedor cambia y tu sistema se rompe sin aviso.
- **Evaluar solo al lanzar:** la calidad se degrada en silencio sin evaluación continua.

## Contraejemplo y caso borde

- **Contraejemplo (producción madura):** un sistema con caché, límites, streaming, versión de modelo fijada, observabilidad completa (costo/latencia/calidad) y evaluación continua ante cada cambio: escala, no se arruina y detecta regresiones antes que los usuarios. La operación, no el modelo, lo hace confiable.
- **Caso borde (el proveedor depreca el modelo):** tu sistema dependía de una versión que el proveedor retira; sin un plan de migración y re-evaluación, dejas de funcionar. La dependencia de un modelo externo es supply chain ([[cyber-llm4]]): ten un plan B.

## Transferencia isomorfa

- **GenAI en producción ↔ MLOps / SRE:** monitoreo, deriva, versiones, fiabilidad y costo son el ML Systems de la Arena ([[cyber-mls5]] y los clusters ML-systems) aplicados a GenAI; "LLMOps" es MLOps con tokens.
- **Evaluación continua ↔ CI/CD + detection engineering:** correr el set en cada cambio es el "CI de calidad", hermano del CI/CD seguro ([[cyber-dev5]]) y del ciclo de mejora del blue team ([[cyber-blue5]]).
- **Observabilidad ↔ logs y detección:** ver/medir/alertar sobre tu propio sistema es [[cyber-blue1]] aplicado a GenAI.

Moraleja de la arista: *el modelo es la parte fácil; producción es operación —costo, latencia, fiabilidad, seguridad, observabilidad y evaluación continua—, y cada cambio (incluido el del proveedor) dispara re-evaluación.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para tu asistente RAG, lista 3 controles de costo, 2 de latencia y qué monitorearías en producción.
- **Misión externa (lab vivo):** lee sobre evaluación/observabilidad de LLMs en producción (p. ej. [LangSmith](https://docs.smith.langchain.com/) o la guía de [OpenAI sobre producción](https://platform.openai.com/docs/guides/production-best-practices)). **Criterio de cierre:** explicar por qué fijar la versión del modelo y re-evaluar es crítico.
- **Mini-entregable:** un checklist de "GenAI a producción": costo, latencia, fiabilidad, observabilidad, versiones/deriva, evaluación continua y seguridad.

---

> **Síntesis:** llevar GenAI a **producción** es operación, no la receta: gestiona **costo** (caché, límites, modelos más chicos, routing), **latencia** (streaming, paralelizar), **fiabilidad** (reintentos, fallbacks, validar salida) y el **no determinismo**. Exige **observabilidad** (registrar entradas/salidas, costo, latencia, calidad — el blue team aplicado a tu sistema) y manejo de **deriva y versiones**: fija la versión del modelo y **re-evalúa ante cada cambio** (incluido el del proveedor), con **evaluación continua** (CI de calidad). La seguridad converge: aplicar la Fase 8 a la vez. El modelo es lo fácil; **la operación lo hace confiable**.

---

**Referencias**

- Huyen, C. (2022). *Designing machine learning systems*. O'Reilly. [Sitio](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)
- Google. (n.d.). MLOps: Continuous delivery and automation pipelines in ML. [cloud.google.com](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- OpenAI. (n.d.). Production best practices. [platform.openai.com](https://platform.openai.com/docs/guides/production-best-practices)
- LangChain. (n.d.). LangSmith: Observability and evaluation for LLM apps. [docs.smith.langchain.com](https://docs.smith.langchain.com/)

*Retrieval: (1) nombra cuatro retos de producción de GenAI; (2) ¿qué se monitorea (observabilidad) y por qué?; (3) ¿por qué fijar la versión del modelo y re-evaluar ante cada cambio?; (4) ¿qué es la evaluación continua?*
