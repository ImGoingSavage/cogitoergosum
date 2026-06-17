# Agentes LLM: razonamiento, memoria, planificación y herramientas

> Recurso troncal: **MIT-AI.md (Semana 12)** + [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629). Cómo un LLM se convierte en un agente que actúa en el mundo. Aplica el marco de [[gen-ag1]] y usa el LLM como política sin RL. Conecta fuerte con la seguridad de agentes ([[cyber-llm2]]).

## De qué trata (y qué sabrás hacer al final)

Un LLM "piensa" pero no actúa. Para volverlo agente le damos cuatro capacidades: **razonar** sobre qué hacer, **usar herramientas** (buscar, calcular, llamar APIs), **recordar** lo que ha pasado (memoria) y **planificar** pasos. El patrón que las une —**ReAct** (Reason + Act)— es la receta dominante de los agentes LLM actuales. Esta lección la desarma para que entiendas qué hace LangChain, AutoGPT o un agente de Claude por dentro.

La intuición: un LLM solo es como un experto brillante **encerrado en una habitación sin ventanas ni teléfono** — sabe mucho pero no puede consultar nada ni hacer nada. Convertirlo en agente es darle un **teléfono** (herramientas: buscar, calcular, llamar APIs), una **libreta** (memoria), y enseñarle a **pensar en voz alta antes de cada acción** ("necesito el clima → llamo a la API del clima → me dice 18°C → entonces…"). El bucle pensar→actuar→observar es ReAct.

Al terminar podrás: (1) explicar el patrón **ReAct** (intercalar razonamiento y acción); (2) describir el **uso de herramientas** (function calling); (3) distinguir tipos de **memoria** y **planificación**; y (4) reconocer la **autocrítica** (Reflexion) y por qué la **agencia** es un riesgo.

## ReAct: razonar y actuar, intercalados

[ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) es engañosamente simple: en vez de que el LLM dé una respuesta de golpe, se le hace alternar **Pensamiento → Acción → Observación**, en bucle:
- **Thought:** el LLM razona qué necesita ("para responder esto necesito el precio actual").
- **Action:** elige y ejecuta una herramienta ("buscar_precio('BTC')").
- **Observation:** recibe el resultado ("$67,000").
- …y vuelve a pensar con esa nueva información, hasta poder responder.

Esto **funde** dos cosas que antes iban separadas: el razonamiento (chain-of-thought, [[gen-eval4]]) y la acción sobre el mundo. El razonamiento explícito hace las acciones más acertadas; las observaciones reales anclan el razonamiento en hechos (anti-alucinación, [[gen-eval3]]). En el marco de [[gen-ag1]]: el LLM **es** la política $\pi$, el estado es el historial Thought/Action/Observation, y las acciones son llamadas a herramientas.

## Uso de herramientas (function calling)

Una herramienta es cualquier función que el agente puede invocar: buscar en la web, ejecutar código, consultar una base de datos, llamar una API, hacer RAG ([[gen-rag1]]). Los LLMs modernos hacen **function calling**: dado un catálogo de herramientas con sus descripciones, el modelo decide **cuál** llamar y con **qué argumentos**, en formato estructurado (JSON). Esto rompe los límites del LLM: deja de estar atado a su conocimiento congelado y puede actuar sobre datos frescos y sistemas reales ([Toolformer, Schick et al., 2023](https://arxiv.org/abs/2302.04761)). Cada herramienta que añades amplía lo que el agente **puede hacer** — y, ojo, lo que un atacante podría hacer a través de él ([[gen-ag4]]).

## Memoria: corto y largo plazo

- **Memoria de trabajo (corto plazo):** el contexto de la tarea actual —los Thought/Action/Observation acumulados—. Limitada por la ventana de contexto; por eso las tareas largas necesitan resumir o externalizar.
- **Memoria de largo plazo:** información que persiste entre sesiones, típicamente en una **base vectorial** que el agente consulta por similitud (¡es RAG! [[gen-rag2]]) — "recuerda" hechos del usuario, resultados previos, lecciones. La memoria de largo plazo de un agente y un sistema RAG son, técnicamente, lo mismo: recuperación semántica de lo guardado.

## Planificación y autocrítica

- **Planificación:** descomponer un objetivo en sub-pasos antes (o durante) la ejecución. Desde simple (pedir al LLM un plan y ejecutarlo) hasta árboles de posibilidades ([Tree of Thoughts, Yao et al., 2023](https://arxiv.org/abs/2305.10601)). Es la descomposición de [[gen-eval4]] llevada a la acción.
- **Autocrítica / reflexión:** el agente **evalúa su propio resultado** y reintenta si falló. [Reflexion (Shinn et al., 2023)](https://arxiv.org/abs/2303.11366): el agente genera, critica su salida, guarda la lección en memoria y reintenta mejor. Es el bucle observar→corregir de [[gen-ag1]], hecho con el LLM juzgándose a sí mismo (con los sesgos de [[gen-eval2]]: un crítico que comparte el error del actor no lo detecta).

## Mini-ejemplo trabajado: un agente de investigación

Pregunta: "¿Cuál fue el ingreso de la empresa X el último trimestre y cómo se compara con el anterior?"
- **Thought:** necesito el último trimestre → **Action:** buscar_web("ingreso X Q3 2026") → **Obs:** "$2.1B".
- **Thought:** ahora el anterior → **Action:** buscar_web("ingreso X Q2 2026") → **Obs:** "$1.8B".
- **Thought:** comparar → **Action:** calcular((2.1-1.8)/1.8) → **Obs:** "+16.7%".
- **Thought:** tengo todo → **respuesta** con cifras y fuente.

Cerró el bucle con el mundo tres veces, anclando cada paso en una observación real. Predicción antes de seguir: una de las búsquedas devuelve un dato de **otra** empresa (homónima). Si el agente **no observa críticamente**, lo usará y dará una respuesta falsa con confianza. La calidad de un agente depende tanto de su razonamiento como de **verificar sus observaciones** — y de que sus herramientas sean confiables (lo recuperado/devuelto es entrada no confiable, [[cyber-llm2]]).

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "Necesita buscar/calcular/actuar, no solo saber" | Herramientas (function calling) |
| "Debe encadenar pasos reaccionando a resultados" | ReAct (Thought/Action/Observation) |
| "Tiene que recordar entre sesiones" | Memoria de largo plazo = RAG |
| "Tarea compleja con sub-objetivos" | Planificación / descomposición |
| "Falla y debería reintentar mejor" | Autocrítica (Reflexion) |
| "El agente puede ejecutar acciones reales" | Agencia → riesgo (least privilege) |

## Errores típicos

- **Darle todas las herramientas 'por si acaso':** cada herramienta amplía la superficie de ataque y el daño de un error/inyección (agencia excesiva, [[cyber-llm2]]).
- **Confiar en las observaciones sin verificarlas:** lo que devuelve una herramienta puede ser erróneo o malicioso (RAG/web no confiables).
- **Confundir 'razona en voz alta' con 'razona bien':** ReAct mejora, no garantiza; el agente puede encadenar pasos lógicos sobre una premisa falsa.
- **Memoria infinita en el contexto:** la ventana se satura (*lost in the middle*, [[gen-rag3]]); hay que resumir/externalizar.

## Contraejemplo y caso borde

- **Contraejemplo (un workflow fijo gana):** si la tarea siempre sigue los mismos pasos (extraer→validar→guardar), un **pipeline determinista** es más fiable, barato y auditable que un agente que "decide" cada vez. La autonomía es útil cuando los pasos **no** se conocen de antemano; si se conocen, codifícalos.
- **Caso borde (bucle infinito / deriva):** un agente puede quedar atrapado repitiendo acciones sin progresar, o desviarse del objetivo paso a paso. Necesita límites (máximo de pasos, presupuesto, detección de no-progreso) — agencia acotada por diseño.

## Transferencia isomorfa

- **ReAct ↔ el método científico / OODA:** hipótesis (thought) → experimento (action) → observación → revisar; el mismo bucle de [[cyber-mit4]] y de la detección de alucinaciones por anclaje ([[gen-eval3]]).
- **Memoria de largo plazo = RAG:** literalmente la misma recuperación semántica de [[gen-rag2]]; "recordar" es "recuperar lo guardado".
- **Herramientas + agencia mínima ↔ least privilege:** dar solo las herramientas y permisos necesarios es el principio de [[cyber-ms2]]/[[cyber-llm2]] aplicado a lo que un agente puede invocar.

Moraleja de la arista: *un agente LLM es ReAct —pensar, actuar con herramientas, observar, repetir— con memoria (=RAG) y autocrítica; su poder y su riesgo crecen con cada herramienta, así que dale la mínima.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** escribe la traza ReAct (Thought/Action/Observation) de un agente que responde "¿lloverá mañana donde vivo y debo llevar paraguas?".
- **Misión externa (lab vivo):** lee [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) (figura del bucle) y hojea la doc de [agentes de LangChain](https://python.langchain.com/docs/concepts/agents/). **Criterio de cierre:** explicar por qué intercalar razonamiento y acción supera a solo razonar o solo actuar.
- **Mini-entregable:** el diseño de un agente para una tarea tuya: qué herramientas (mínimas) le das, qué memoria usa, y dónde pondrías autocrítica y límites.

## Reconstrucción mínima en código

El ciclo ReAct (pensar -> actuar -> observar) con una herramienta estrecha y tipada.

```python
def calculadora(expr):
    return eval(expr)                    # toy; NUNCA eval() sobre entrada no confiable
TOOLS = {"calc": calculadora}

def agente(tarea, max_pasos=3):
    for _ in range(max_pasos):
        # <- tu LLM decide: pensamiento -> (herramienta, args) -> observacion
        accion, args = "calc", "2+2"     # stub de la decision del modelo
        if accion in TOOLS:
            return f"resultado: {TOOLS[accion](args)}"   # detente al resolver
    return "sin respuesta"

print(agente("cuanto es 2+2?"))
```

**Qué observar:** Agencia minima: pocas herramientas, permisos estrechos y limite de pasos. (El eval() ilustra por que la entrada no confiable es peligrosa: ver [[cyber-llm2]].)

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (agentes LLM con ReAct, herramientas, memoria y autocrítica) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** implementar ciclo pensar-actuar-observar con herramientas limitadas.
2. **Baseline obligatorio:** LLM de una sola respuesta sin herramientas.
3. **Versión mejorada:** workflow ReAct con herramientas tipadas y límites duros.
4. **Evaluación:** task success, tool accuracy, pasos promedio y costo.
5. **Fallo que debes explicar:** el agente llama herramientas irrelevantes o actua con argumentos inseguros.
6. **Transferencia:** asistentes operativos que consultan APIs pero requieren permisos estrechos.

**Laboratorio externo principal:** [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents).
**Laboratorio alternativo:** [LangGraph tutorials](https://langchain-ai.github.io/langgraph/tutorials/).
**Ruta de cluster:** agente con herramientas estrechas, límites duros, evaluación por task success y fallos controlados.

**Entregable:** trazas de agente con llamadas a herramientas, errores y correcciones. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y qué harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** un LLM se vuelve **agente** con cuatro capacidades unidas por **ReAct**: **razonar** (Thought), **actuar** con **herramientas** (Action / function calling), **observar** el resultado, y repetir — anclando el razonamiento en hechos reales. Añade **memoria** (la de largo plazo **es RAG**), **planificación** (descomposición, Tree of Thoughts) y **autocrítica** (Reflexion, con los sesgos de un crítico que puede compartir el error). El LLM hace de **política** sin RL. Cada herramienta amplía poder **y** riesgo: dale **agencia mínima**, verifica observaciones, y pon límites; si los pasos son fijos, un pipeline determinista gana.

---

**Referencias**

- Yao, S., et al. (2022). ReAct: Synergizing reasoning and acting in language models. *ICLR*. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Schick, T., et al. (2023). Toolformer: Language models can teach themselves to use tools. *NeurIPS*. [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
- Shinn, N., et al. (2023). Reflexion: Language agents with verbal reinforcement learning. *NeurIPS*. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
- Yao, S., et al. (2023). Tree of Thoughts: Deliberate problem solving with LLMs. *NeurIPS*. [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)
- LangChain. (n.d.). Agents (concepts). [python.langchain.com](https://python.langchain.com/docs/concepts/agents/)

*Retrieval: (1) ¿qué intercala el patrón ReAct y por qué ayuda?; (2) ¿qué es function calling?; (3) ¿por qué la memoria de largo plazo de un agente es RAG?; (4) ¿qué es Reflexion y qué riesgo tiene la autocrítica?*
