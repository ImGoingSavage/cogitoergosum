# Aprender a decidir: Q-learning y policy gradient

> Recurso troncal: **MIT-AI.md (Semana 12)** + [Sutton & Barto](http://incompleteideas.net/book/the-book-2nd.html). Cómo un agente **aprende** su política por ensayo y error. Sigue a [[gen-ag1]] (el marco) y prepara [[gen-ag3]] (agentes LLM). Conecta con RLHF, que alinea a los propios LLMs.

## De qué trata (y qué sabrás hacer al final)

Ya sabes que un agente tiene una **política** (qué acción tomar en cada estado). Pero, ¿cómo la **aprende** sin que nadie le diga la respuesta correcta, solo con recompensas? Hay dos grandes familias: aprender **el valor** de las situaciones y actuar en consecuencia (**Q-learning**), o ajustar **directamente** la política para que las acciones buenas sean más probables (**policy gradient**). Entenderlas te da la base de todo el RL — y de **RLHF**, lo que alinea a los LLMs que usas a diario.

La intuición: aprender por refuerzo es como aprender a cocinar **sin receta, solo probando y notando si quedó rico**. Dos estilos: (1) **Q-learning** — llevas una libreta mental de "qué tan bueno fue cada ingrediente en cada situación" y eliges el de mejor nota (aprendes a **valorar**). (2) **Policy gradient** — no llevas notas de valor; simplemente, cuando un plato sale rico, **haces más probables** los gestos que hiciste, y cuando sale mal, menos probables (ajustas **el hábito** directamente).

Al terminar podrás: (1) explicar el **MDP** y el papel del **descuento $\gamma$**; (2) entender **Q-learning** (aprender valores de acción); (3) entender **policy gradient** (ajustar la política directamente); y (4) conectar con **RLHF**.

## El MDP y el descuento

Formalmente, el problema es un **MDP** (Markov Decision Process): estados, acciones, una dinámica de transición y recompensas, con la **propiedad de Markov** (el futuro depende solo del estado actual, no de toda la historia). El agente busca la política que maximiza el **retorno**: la suma de recompensas futuras, **descontadas**:

$$G_t = r_{t+1} + \gamma\, r_{t+2} + \gamma^2 r_{t+3} + \cdots$$

El **factor de descuento $\gamma \in [0,1)$** pondera cuánto valen las recompensas futuras frente a las inmediatas. $\gamma$ cercano a 0 = miope (solo importa lo inmediato); cercano a 1 = paciente (valora el largo plazo). Es el mando que dice "¿cuánto futuro me importa?".

## Q-learning: aprender el valor de las acciones

[CAJA NEGRA OK — la intuición importa más que la derivación]
**Q-learning** ([Watkins, 1989](https://link.springer.com/article/10.1007/BF00992698)) aprende una función **$Q(s,a)$**: "qué retorno esperar si en el estado $s$ tomo la acción $a$ y luego actúo bien". Si conoces $Q$, tu política es trivial: en cada estado, elige la acción de mayor $Q$. Se aprende iterativamente con la **ecuación de Bellman**: el valor de una acción = recompensa inmediata + (descuento × mejor valor del siguiente estado), acercando poco a poco la estimación a esa consistencia.

- **Es value-based** (aprende valores, la política se deriva de ellos).
- **Es off-policy** (puede aprender de experiencia pasada o ajena).
- **Su límite:** la versión tabular guarda un valor por cada par $(s,a)$ — inviable si hay millones de estados. La solución: aproximar $Q$ con una **red neuronal** → **Deep Q-Networks (DQN)** ([Mnih et al., 2015](https://www.nature.com/articles/nature14236)), que aprendió a jugar Atari desde píxeles. Hito que reabrió el RL moderno.

## Policy gradient: ajustar la política directamente

El otro camino: en vez de aprender valores, parametrizar la política $\pi_\theta(a\mid s)$ (p. ej. una red) y **ajustar $\theta$** para subir el retorno esperado. La idea de **REINFORCE** ([Williams, 1992](https://link.springer.com/article/10.1007/BF00992696); [policy gradient theorem, Sutton et al., 2000](https://proceedings.neurips.cc/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html)): tras un episodio, **aumenta la probabilidad** de las acciones que llevaron a buen retorno y **disminuye** la de las malas — "haz más de lo que funcionó".

- **Es policy-based** (optimiza la política directamente, sin necesitar $Q$).
- **Ventaja:** maneja **acciones continuas** y políticas estocásticas, donde Q-learning sufre.
- **Límite:** alta **varianza** (las estimaciones son ruidosas). Se mitiga con métodos **actor-critic** (combinan política + valor) y algoritmos estables como **PPO** ([Schulman et al., 2017](https://arxiv.org/abs/1707.06347)), hoy el caballo de batalla.

| | Q-learning (value-based) | Policy gradient (policy-based) |
|---|---|---|
| Qué aprende | Valor $Q(s,a)$; la política se deriva | La política $\pi_\theta$ directamente |
| Acciones | Discretas | Discretas y **continuas** |
| Punto débil | No escala sin aproximación (DQN) | Alta varianza (→ actor-critic, PPO) |

## El puente que importa: RLHF alinea a los LLMs

Aquí RL toca tu día a día. Los LLMs tipo ChatGPT/Claude se afinan con **RLHF** (RL from Human Feedback, [Ouyang et al., 2022 — InstructGPT](https://arxiv.org/abs/2203.02155)): humanos comparan respuestas, se entrena un **modelo de recompensa** que predice la preferencia humana, y luego se **optimiza la política del LLM con policy gradient (PPO)** para producir respuestas que ese modelo de recompensa puntúa alto. Es decir: el "ser útil, honesto e inofensivo" del LLM se logró con **policy gradient** sobre una recompensa aprendida de preferencias humanas. (Variantes recientes: [DPO](https://arxiv.org/abs/2305.18290), que evita el RL explícito.) Entender policy gradient es entender cómo se alinean los modelos que usas.

## Mini-ejemplo trabajado

Un robot aprende a salir de un laberinto, recompensa +1 al salir, 0 si no.
- **Q-learning:** aprende $Q(\text{casilla}, \text{dirección})$ — qué tan prometedor es ir en cada dirección desde cada casilla. Al final, en cada casilla va hacia el mayor $Q$. Funciona genial con pocas casillas; con un laberinto enorme (o entrada = imagen), necesita DQN.
- **Policy gradient:** prueba rutas completas; las que salieron, sube la probabilidad de sus movimientos; las que no, la baja. Tras muchos episodios, la política favorece rutas exitosas.

Predicción antes de seguir: la recompensa solo llega **al final** (+1 al salir). ¿Por qué eso dificulta el aprendizaje? → **asignación de crédito** ([[gen-ag1]]): ¿cuál de los 50 movimientos mereció el +1? El descuento $\gamma$ y los métodos de valor ayudan a propagar esa señal tardía hacia atrás, pero las recompensas **dispersas** son uno de los grandes retos del RL.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "Pocos estados discretos, recompensa clara" | Q-learning tabular |
| "Estados enormes / entrada perceptual (imágenes)" | DQN (aproximar Q con red) |
| "Acciones continuas (control, robótica)" | Policy gradient / actor-critic |
| "Cómo se hizo útil un LLM" | RLHF: recompensa aprendida + PPO |
| "La recompensa solo llega al final" | Asignación de crédito + descuento γ |

## Errores típicos

- **Creer que Q-learning escala tal cual:** la versión tabular no; necesita aproximación (DQN) en espacios grandes.
- **Olvidar la varianza del policy gradient:** sin actor-critic/PPO, el entrenamiento es inestable.
- **Pensar que RLHF 'enseña hechos':** ajusta el **comportamiento/preferencia** (como el fine-tuning de [[gen-rag1]]), no inyecta conocimiento fresco.
- **Ignorar la especificación de la recompensa:** sigue siendo el objetivo; mal puesta → reward hacking ([[gen-ag1]]).

## Contraejemplo y caso borde

- **Contraejemplo (a veces no hace falta aprender la política):** un agente LLM ([[gen-ag3]]) muchas veces **no** entrena por RL: usa un LLM ya alineado como política y la guía con prompting. RL es para cuando hay que **aprender** a decidir por ensayo y error en un entorno; no todo agente lo necesita.
- **Caso borde (recompensa de modelo explotable):** en RLHF, el LLM puede aprender a **engañar al modelo de recompensa** (producir respuestas que el modelo puntúa alto pero a un humano no le gustan) — *reward model hacking*. Por eso se vigila la divergencia y se combinan señales; la recompensa aprendida también es un proxy imperfecto.

## Transferencia isomorfa

- **Q vs policy ↔ 'valorar opciones' vs 'ajustar el hábito':** estimar el valor de cada elección y elegir el mejor, vs reforzar directamente lo que funcionó — dos formas de mejorar que reaparecen en decisiones humanas.
- **Descuento $\gamma$ ↔ tasa de interés / cortoplacismo:** cuánto pesa el futuro frente al presente, igual que en finanzas o en hábitos.
- **RLHF ↔ alinear con preferencias:** optimizar hacia lo que la gente prefiere (recompensa aprendida) es el mismo patrón que evaluar con LLM-as-a-judge sobre una rúbrica ([[gen-eval2]]) — y comparte su riesgo de optimizar un proxy de la preferencia.

Moraleja de la arista: *aprender a decidir es valorar las opciones (Q-learning) o reforzar lo que funcionó (policy gradient); RLHF alinea a los LLMs con policy gradient sobre una recompensa aprendida de preferencias.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el laberinto, explica qué guardaría Q-learning (¿qué es una entrada de su "tabla"?) vs qué ajustaría policy gradient. ¿Cuál elegirías si la entrada fuera una imagen de la cámara del robot?
- **Misión externa (lab vivo):** lee la intro de [PPO (Schulman et al., 2017)](https://arxiv.org/abs/1707.06347) y el resumen de [InstructGPT/RLHF (Ouyang et al., 2022)](https://arxiv.org/abs/2203.02155). **Criterio de cierre:** explicar en una frase cómo RLHF usa policy gradient para alinear un LLM.
- **Mini-entregable:** una comparación de una carilla Q-learning vs policy gradient (qué aprende, fortalezas, debilidades, cuándo usar cada uno) y dónde encaja RLHF.

---

> **Síntesis:** el agente busca la política que maximiza el **retorno descontado** (con $\gamma$ ponderando el futuro) en un **MDP**. Dos familias para aprenderla: **Q-learning** (value-based: aprende $Q(s,a)$ y deriva la política; escala con **DQN**) y **policy gradient** (policy-based: ajusta $\pi_\theta$ directamente — maneja acciones continuas, pero con alta varianza → actor-critic, **PPO**). El puente clave: **RLHF** alinea a los LLMs entrenando un modelo de recompensa de preferencias humanas y optimizando la política con **PPO**. La recompensa sigue siendo un **proxy** del objetivo: aprendida o no, mal puesta, el agente la **hackea**.

---

**Referencias**

- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). [Libro gratuito](http://incompleteideas.net/book/the-book-2nd.html)
- Mnih, V., et al. (2015). Human-level control through deep reinforcement learning (DQN). *Nature*. [nature.com](https://www.nature.com/articles/nature14236)
- Schulman, J., et al. (2017). Proximal policy optimization algorithms (PPO). [arXiv:1707.06347](https://arxiv.org/abs/1707.06347)
- Williams, R. J. (1992). Simple statistical gradient-following algorithms (REINFORCE). *Machine Learning*. [Springer](https://link.springer.com/article/10.1007/BF00992696)
- Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback (InstructGPT/RLHF). *NeurIPS*. [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)

*Retrieval: (1) ¿qué es el descuento $\gamma$ y qué controla?; (2) ¿qué aprende Q-learning y qué lo hace escalar (DQN)?; (3) ¿qué ajusta policy gradient y cuál es su debilidad?; (4) ¿cómo usa RLHF el policy gradient para alinear un LLM?*
