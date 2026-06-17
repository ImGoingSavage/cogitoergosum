# Sistemas multi-agente: por qué y cuándo varios agentes

> Recurso troncal: **MIT-AI.md (Semana 13)**. De un agente ([[gen-ag4]]) a un equipo de agentes que colaboran. Conecta con la propagación de inyecciones entre agentes ([[cyber-llm2]]). Prepara [[gen-ma2]] (orquestación y routing).

## De qué trata (y qué sabrás hacer al final)

Un solo agente con muchas herramientas y un objetivo enorme se vuelve frágil: el contexto se satura, el razonamiento se enreda y un error contamina todo. La alternativa es un **sistema multi-agente**: varios agentes **especializados** que colaboran, cada uno con un rol acotado, coordinándose para resolver una tarea compleja. Esta lección explica **por qué** (y, crucialmente, **cuándo**) varios agentes superan a uno, y los patrones de colaboración.

La intuición: un agente único es como pedirle a **una sola persona** que sea a la vez investigadora, redactora, revisora y administradora de un proyecto grande — se agobia y comete errores en todo. Un sistema multi-agente es un **equipo**: un investigador busca, un redactor escribe, un revisor critica, un coordinador reparte y junta. Cada uno hace **una cosa bien**, con su propio "espacio mental" (contexto) limpio. Pero, como en todo equipo, aparece el costo de **coordinarse**: reuniones, malentendidos, alguien que tiene que dirigir.

Al terminar podrás: (1) explicar **por qué** dividir en agentes especializados ayuda (contexto, modularidad); (2) nombrar **patrones** (orquestador-trabajadores, pipeline, debate); (3) razonar **cuándo NO** usar multi-agente; y (4) reconocer los **riesgos nuevos** que introduce.

## Por qué varios agentes: especialización y contexto limpio

Tres razones por las que dividir ayuda:
- **Contexto acotado:** cada agente trabaja con solo la información de su sub-tarea, evitando saturar la ventana (*lost in the middle*, [[gen-rag3]]). Un investigador no necesita el contexto del formateador.
- **Especialización:** un agente con un rol estrecho y herramientas mínimas razona mejor y es más fácil de evaluar y depurar que un "todólogo" ([[gen-ag4]], agencia mínima).
- **Modularidad y robustez:** puedes mejorar/cambiar un agente sin tocar los demás; un fallo queda más contenido. Es la **separación de responsabilidades** del buen software ([[cyber-dev3]]) aplicada a agentes.

[Investigación de Anthropic sobre sistemas multi-agente](https://www.anthropic.com/engineering/multi-agent-research-system) muestra ganancias reales en tareas de investigación amplia — donde el trabajo se **paraleliza** entre subagentes— a costa de mucho más cómputo.

## Patrones de colaboración

| Patrón | Cómo funciona | Cuándo |
|---|---|---|
| **Orquestador–trabajadores** | Un agente "líder" descompone la tarea, delega sub-tareas a trabajadores especializados y junta resultados | Tareas divisibles con un coordinador claro |
| **Pipeline (secuencial)** | Cada agente procesa y pasa al siguiente (investigar → redactar → revisar) | Etapas con dependencia clara |
| **Debate / crítica** | Varios agentes proponen y se critican entre sí para mejorar la respuesta | Cuando la diversidad de perspectivas mejora la calidad |
| **Mercado / votación** | Agentes proponen soluciones y se elige/combina la mejor | Decisiones con múltiples candidatos |

El **orquestador-trabajadores** es el más común: un agente coordinador (manager) reparte y un grupo de trabajadores ejecuta — exactamente como un equipo humano con un líder de proyecto.

## El debate y la diversidad de perspectivas

Un caso valioso: hacer que **varios agentes con roles o vistas distintas** aborden el mismo problema y se critiquen ([Du et al., 2023, "multiagent debate"](https://arxiv.org/abs/2305.14325)). La idea es la misma que un **panel de revisores**: perspectivas independientes detectan errores que una sola pasa por alto, y el desacuerdo fuerza a justificar. Conecta con la autocrítica de [[gen-ag3]], pero con una ventaja: si los críticos son **independientes** (distinto rol/modelo), no comparten el mismo punto ciego — justo lo que le faltaba a la autocrítica de un solo agente ([[gen-eval2]]).

## Mini-ejemplo trabajado: informe de mercado

Tarea: "investiga el mercado de X y entrega un informe con fuentes". 
- **Un agente:** debe buscar, evaluar fuentes, sintetizar, redactar y revisar — su contexto se llena de resultados crudos, se pierde, mezcla.
- **Multi-agente (orquestador-trabajadores):** el **coordinador** divide en sub-preguntas; varios **investigadores** las atacan **en paralelo** (cada uno con contexto limpio); un **sintetizador** junta; un **revisor** verifica fuentes y coherencia; el coordinador entrega. Más rápido (paralelo) y cada pieza es mejor.

Predicción antes de seguir: el coordinador divide mal la tarea (sub-preguntas que se solapan o dejan huecos). ¿Qué pasa con el informe? → resultados redundantes o incompletos: la **calidad del sistema depende de la orquestación**, no solo de los agentes. La coordinación es el nuevo punto de fallo ([[gen-ma2]]).

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "El contexto de un solo agente se satura" | Dividir en agentes con contexto acotado |
| "La tarea tiene sub-tareas paralelizables" | Orquestador–trabajadores |
| "Etapas con dependencia clara" | Pipeline secuencial |
| "Quiero detectar errores con perspectivas distintas" | Debate / crítica entre agentes independientes |
| "La tarea es simple y de un paso" | NO multi-agente (sobreingeniería) |

## Errores típicos

- **Multi-agente por moda:** añade coordinación, costo (mucho más cómputo) e impredecibilidad; úsalo solo si la tarea lo justifica.
- **Roles solapados o mal divididos:** agentes que duplican trabajo o dejan huecos; la descomposición debe ser limpia (MECE: sin solapes, sin faltantes).
- **Autocrítica disfrazada de multi-agente:** varios "agentes" que son el mismo modelo con el mismo punto ciego no aportan diversidad real.
- **Olvidar el costo:** N agentes ≈ N veces el cómputo (o más); la ganancia debe compensarlo.

## Contraejemplo y caso borde

- **Contraejemplo (un agente o workflow basta):** para tareas de un solo paso o con pasos fijos, un workflow determinista ([[gen-ag4]]) es más fiable y barato que un sistema multi-agente. La regla de [[gen-ag4]] manda: usa lo más simple que funcione; multi-agente es la opción **más** compleja.
- **Caso borde (propagación de errores e inyecciones):** un error (o una **prompt injection**, [[cyber-llm1]]) en un agente puede **propagarse** a los demás a través de sus mensajes — el contenido no confiable salta de agente en agente ([[cyber-llm2]]). Más agentes = más fronteras de confianza que vigilar, no menos.

## Transferencia isomorfa

- **Multi-agente ↔ división del trabajo / microservicios:** especializar y coordinar componentes pequeños, con el costo de orquestación — el mismo tradeoff de monolito vs microservicios, o de un experto vs un equipo.
- **Debate entre agentes ↔ panel de jueces / revisión por pares:** perspectivas independientes que detectan más errores que una sola — el patrón que ya usamos para evaluar ([[gen-eval2]], [[cyber-mit5]]).
- **Orquestador-trabajadores ↔ map-reduce:** repartir (map), procesar en paralelo, juntar (reduce); la coordinación es el reduce.

Moraleja de la arista: *divide en agentes especializados cuando la tarea es grande y divisible; ganas contexto limpio y paralelismo, pero pagas coordinación, costo y nuevas fronteras de confianza — y si la tarea es simple, no lo hagas.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** descompón "planear un viaje (vuelos, hotel, actividades, presupuesto)" en agentes especializados; di qué patrón usarías y por qué.
- **Misión externa (lab vivo):** lee [How we built our multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system) y hojea [AutoGen (Microsoft)](https://microsoft.github.io/autogen/). **Criterio de cierre:** explicar cuándo multi-agente vale la pena y cuándo no.
- **Mini-entregable:** un diagrama de un sistema multi-agente para una tarea, con roles, patrón de colaboración y dónde podría propagarse un error.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (descomposicion multi-agente y patrones de colaboración) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** comparar agente unico contra roles separados con el mismo presupuesto.
2. **Baseline obligatorio:** un solo agente con prompt amplio.
3. **Versión mejorada:** orquestador con especialistas y contrato de salida.
4. **Evaluación:** task success, costo, latencia y errores por rol.
5. **Fallo que debes explicar:** más agentes aumentan costo sin mejorar task success.
6. **Transferencia:** equipos humanos: especializar solo cuando la coordinación se paga.

**Laboratorio externo principal:** [Anthropic multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
**Laboratorio alternativo:** [Microsoft AutoGen](https://microsoft.github.io/autogen/).
**Ruta de cluster:** sistema multi-agente con roles, grafo de estado, presupuesto, red team y comparación contra agente unico.

**Entregable:** experimento con roles, trazas y comparación contra baseline simple. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y que harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** un **sistema multi-agente** divide una tarea grande en **agentes especializados** que colaboran, ganando **contexto acotado**, especialización, modularidad y **paralelismo**. Patrones: **orquestador–trabajadores** (el más común), **pipeline**, **debate/crítica** (perspectivas independientes que detectan más errores) y votación. Pero introduce **costo de coordinación**, mucho más cómputo, e **nuevas fronteras de confianza**: un error o una **inyección** puede propagarse entre agentes ([[cyber-llm2]]). Úsalo solo cuando la tarea es grande y divisible; si es simple o de pasos fijos, un agente o un workflow gana.

---

**Referencias**

- Anthropic. (2024). How we built our multi-agent research system. [anthropic.com](https://www.anthropic.com/engineering/multi-agent-research-system)
- Du, Y., et al. (2023). Improving factuality and reasoning in language models through multiagent debate. [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)
- Wu, Q., et al. (2023). AutoGen: Enabling next-gen LLM applications via multi-agent conversation. [arXiv:2308.08155](https://arxiv.org/abs/2308.08155) · [AutoGen](https://microsoft.github.io/autogen/)
- Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human behavior. *UIST*. [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)

*Retrieval: (1) ¿por qué dividir en agentes especializados ayuda?; (2) nombra 3 patrones de colaboración; (3) ¿cuándo NO usar multi-agente?; (4) ¿qué riesgo nuevo introduce respecto a un solo agente?*
