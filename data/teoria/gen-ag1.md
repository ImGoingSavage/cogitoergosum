# Del LLM reactivo al agente: el marco agente-entorno

> Recurso troncal: **MIT-AI.md (Semana 12)** + el texto canónico [Sutton & Barto, *Reinforcement Learning: An Introduction*](http://incompleteideas.net/book/the-book-2nd.html). El salto de "un modelo que responde" a "un sistema que actúa, observa y persigue un objetivo". Construye sobre los LLMs ([[gen-tf3]]) y prepara [[gen-ag2]] (cómo aprende a decidir).

## De qué trata (y qué sabrás hacer al final)

Un LLM por sí solo es **reactivo**: le das texto, te da texto, y olvida. Un **agente** es otra cosa: percibe un **entorno**, **actúa** sobre él, observa el resultado, y repite hasta lograr un **objetivo** —con memoria entre pasos—. Esta lección da el marco mental que une el aprendizaje por refuerzo (RL) clásico con los agentes LLM modernos: el bucle **agente-entorno** y su vocabulario (estado, acción, recompensa, política).

La intuición: un LLM reactivo es como pedirle indicaciones a alguien que te responde una frase y se va. Un agente es como un **conductor con GPS**: observa dónde está (estado), elige un giro (acción), ve cómo cambió la situación (nuevo estado + señal de si va bien), y ajusta — una y otra vez hasta llegar (objetivo). No es una respuesta; es un **bucle de decisión con propósito**.

Al terminar podrás: (1) distinguir un **LLM reactivo** de un **agente**; (2) nombrar los elementos del marco RL (**estado, acción, recompensa, política**); (3) explicar el **bucle agente-entorno** y el horizonte/objetivo; y (4) ubicar a los agentes LLM en este marco.

## Reactivo vs agente: el bucle es la diferencia

| LLM reactivo | Agente |
|---|---|
| Entrada → salida, una vez | Bucle: percibir → decidir → actuar → observar → repetir |
| Sin memoria entre llamadas | Mantiene estado/memoria a través de pasos |
| No actúa sobre el mundo | Usa herramientas/acciones que cambian el entorno |
| Objetivo: responder | Objetivo: **lograr una meta** multi-paso |

La clave: un agente **cierra el bucle con el mundo**. Pregunta el clima → recibe la respuesta → decide según ella → actúa otra vez. Esa realimentación es lo que le permite planear, corregirse y completar tareas que no caben en una sola respuesta.

## El vocabulario del aprendizaje por refuerzo

El marco formal viene del RL ([Sutton & Barto](http://incompleteideas.net/book/the-book-2nd.html)). Cinco piezas:

- **Entorno:** el mundo con el que el agente interactúa (un juego, un navegador, un sistema, una API).
- **Estado ($s$):** la situación actual tal como el agente la percibe (el tablero, la página web, el historial de la conversación).
- **Acción ($a$):** lo que el agente puede hacer (mover una ficha, hacer clic, llamar una herramienta).
- **Recompensa ($r$):** una señal numérica de qué tan bien lo hizo (puntos, +1 si ganó, −1 si perdió). Define el **objetivo**.
- **Política ($\pi$):** la **estrategia** del agente: qué acción elegir en cada estado, $\pi(a \mid s)$. Es "el cerebro" — lo que se aprende o se diseña.

El bucle: en el estado $s_t$, el agente elige la acción $a_t$ según su política $\pi$, el entorno responde con un nuevo estado $s_{t+1}$ y una recompensa $r_{t+1}$, y el ciclo continúa. Esto se formaliza como un **MDP** (Proceso de Decisión de Markov, ver [[gen-ag2]]).

## El objetivo: recompensa acumulada, no inmediata

Un punto sutil y crucial: el agente no maximiza la recompensa **del siguiente paso**, sino la **recompensa acumulada a futuro** (el *retorno*). A veces hay que sacrificar una recompensa inmediata por una mayor después (sacrificar una pieza en ajedrez para ganar la partida). Esto introduce dos tensiones centrales del RL:
- **Asignación de crédito:** si ganaste tras 40 movimientos, ¿cuál fue bueno? La recompensa llega tarde y dispersa.
- **Exploración vs explotación:** ¿repites lo que ya sabe funcionar (explotar) o pruebas algo nuevo que podría ser mejor (explorar)? Demasiada explotación te estanca; demasiada exploración malgasta. [[gen-ag2]] desarrolla cómo se resuelven.

## Los agentes LLM en este marco

Un **agente LLM** (tipo ReAct, [[gen-ag3]]) instancia el bucle así: el **estado** es el historial de la tarea (lo que ha pasado, observaciones), las **acciones** son llamadas a herramientas o pasos de razonamiento, la **observación** es lo que devuelve la herramienta, y la **política** es… el propio LLM razonando qué hacer a continuación (a menudo sin RL explícito, solo prompteando). La diferencia con el RL clásico: el agente LLM no suele **aprender** la política por ensayo y error; **usa** un LLM preentrenado como política y la guía con prompting, memoria y herramientas. Pero el **marco** —estado, acción, recompensa/objetivo, bucle— es el mismo, y entenderlo evita tratar a los agentes como magia.

## Mini-ejemplo trabajado

Tarea: "reserva la sala de juntas más barata para mañana a las 10". 
- **Reactivo:** un LLM responde "deberías revisar el sistema de reservas" — y ya. No actuó.
- **Agente:** estado = la petición; acción 1 = llamar a la API de salas (herramienta) → observación: lista con precios; acción 2 = razonar cuál es la más barata disponible; acción 3 = llamar a la API de reserva → observación: confirmación; objetivo cumplido. Cerró el bucle con el mundo varias veces.

Predicción antes de seguir: ¿qué pasa si la acción 1 falla (la API no responde)? Un reactivo no se entera; un buen agente **observa el fallo y decide** (reintentar, avisar, buscar otra vía). Esa capacidad de reaccionar a la observación es lo que distingue un agente de un script rígido — y también lo que lo hace impredecible y riesgoso ([[gen-ag4]], [[cyber-llm2]]).

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "Necesito que ejecute pasos y reaccione a resultados" | Agente (bucle), no LLM reactivo |
| "La tarea no cabe en una sola respuesta" | Agente multi-paso |
| "Hay que sacrificar lo inmediato por lo futuro" | Objetivo = recompensa acumulada |
| "¿Explorar opciones nuevas o repetir lo que sé?" | Dilema exploración/explotación |
| "El agente actúa sobre el mundo real" | Acciones con consecuencias → agencia/seguridad |

## Errores típicos

- **Confundir 'agente' con 'LLM con prompt largo':** lo que define al agente es el **bucle** percibir-actuar-observar, no la longitud del prompt.
- **Maximizar la recompensa inmediata:** el objetivo es el retorno acumulado; lo miope falla.
- **Olvidar el entorno:** sin un entorno que responda a las acciones, no hay realimentación ni aprendizaje/corrección.
- **Asumir que un agente LLM 'aprende' como un agente RL:** normalmente **usa** un LLM como política; no entrena por ensayo y error en tu tarea.

## Contraejemplo y caso borde

- **Contraejemplo (no todo necesita un agente):** si la tarea es de un solo paso ("traduce esto"), un LLM reactivo basta; montar un bucle de agente añade latencia, costo e impredecibilidad sin beneficio. El agente brilla en tareas **multi-paso con realimentación**.
- **Caso borde (recompensa mal especificada → reward hacking):** si la recompensa no captura lo que de verdad quieres, el agente la **explota** de formas indeseadas (el clásico: un agente que "gana" haciendo trampa al simulador). La señal de recompensa **es** la especificación del objetivo; mal puesta, el agente optimiza lo equivocado — eco de la ley de Goodhart de [[gen-eval1]].

## Transferencia isomorfa

- **Bucle agente-entorno ↔ OODA loop:** observar-orientar-decidir-actuar ([[cyber-mit4]]) es el mismo ciclo de decisión con realimentación, aplicado a defensa.
- **Política $\pi(a\mid s)$ ↔ una función/estrategia:** un mapeo de situación a acción; en RL se aprende, en un agente LLM la "calcula" el modelo razonando, en un sistema clásico la programas con reglas.
- **Reward hacking ↔ optimizar el proxy:** maximizar una métrica mal alineada con el objetivo real es el mismo fallo que subir ROUGE empeorando el resumen ([[gen-eval1]]) o el KPI que se vuelve trampa.

Moraleja de la arista: *un agente es un bucle de decisión con propósito (estado→acción→recompensa→repetir); la recompensa es la especificación del objetivo, y especificarla mal es pedir lo equivocado.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** modela la tarea "responder un correo de cliente y agendar un seguimiento" como un MDP: ¿qué son el estado, las acciones, la recompensa y la política?
- **Misión externa (lab vivo):** lee el Capítulo 1 ("The Reinforcement Learning Problem") de [Sutton & Barto](http://incompleteideas.net/book/the-book-2nd.html) (gratuito). **Criterio de cierre:** explicar el bucle agente-entorno y la diferencia entre recompensa inmediata y retorno.
- **Mini-entregable:** una tabla que mapee una tarea tuya a los cinco elementos (entorno, estado, acción, recompensa, política), señalando el riesgo de reward hacking.

---

> **Síntesis:** un **agente** se distingue de un LLM **reactivo** por el **bucle agente-entorno**: percibe un **estado**, elige una **acción** según su **política** $\pi(a\mid s)$, recibe un nuevo estado y una **recompensa**, y repite hacia un **objetivo**. No maximiza la recompensa inmediata sino el **retorno acumulado**, lo que crea las tensiones de **asignación de crédito** y **exploración/explotación**. Los **agentes LLM** instancian este marco pero suelen **usar** un LLM como política (vía prompting/herramientas) en vez de aprenderla por ensayo y error. Cuidado: la **recompensa es la especificación del objetivo** — mal puesta, el agente optimiza lo equivocado (reward hacking).

---

**Referencias**

- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press. [Libro gratuito](http://incompleteideas.net/book/the-book-2nd.html)
- Russell, S., & Norvig, P. (2021). *Artificial intelligence: A modern approach* (4th ed.) — agentes inteligentes. [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- Wang, L., et al. (2024). A survey on large language model based autonomous agents. *Frontiers of Computer Science*. [arXiv:2308.11432](https://arxiv.org/abs/2308.11432)

*Retrieval: (1) ¿qué distingue a un agente de un LLM reactivo?; (2) define estado, acción, recompensa y política; (3) ¿por qué el objetivo es el retorno acumulado y no la recompensa inmediata?; (4) ¿qué es reward hacking?*
