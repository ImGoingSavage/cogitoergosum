# Por qué RAG: anclar el LLM en conocimiento externo

> Recurso troncal: **MIT-AI.md (Semana 9)** + el paper fundacional [Retrieval-Augmented Generation (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401). Convierte un LLM que "alucina con confianza" en uno que responde **anclado** en tus datos. Construye sobre la atención de [[gen-tf2]] (RAG es atención sobre una base de conocimiento). Prepara [[gen-rag2]] (embeddings y chunking).

## De qué trata (y qué sabrás hacer al final)

Un LLM sabe lo que vio en su entrenamiento, hasta una fecha de corte, y **no** conoce tus documentos privados, tus datos de hoy, ni la política interna de tu empresa. Peor: cuando no sabe algo, **no calla** —rellena con una respuesta plausible pero falsa (alucinación)—. **RAG (Retrieval-Augmented Generation)** resuelve esto: antes de responder, **busca** los fragmentos relevantes en una fuente externa (tus documentos) y se los entrega al modelo como contexto, para que responda **basándose en evidencia** en lugar de en su memoria.

La intuición: un LLM sin RAG es como un experto brillante respondiendo **de memoria, con los ojos cerrados** — rápido, fluido, pero sin poder verificar y a veces inventando. RAG es **abrirle los ojos y ponerle los documentos correctos sobre la mesa** justo antes de que responda: "antes de contestar, lee estos tres párrafos relevantes". El experto sigue siendo el mismo; lo que cambia es que ahora responde **mirando la fuente**, no recitando.

Al terminar podrás: (1) explicar **qué problemas de los LLMs resuelve RAG** (corte de conocimiento, datos privados, alucinación, atribución); (2) describir el **flujo RAG** (indexar → recuperar → aumentar → generar); (3) distinguir **RAG de fine-tuning** y cuándo usar cada uno; y (4) reconocer la **arista de seguridad** (RAG = nueva superficie de ataque).

## Los cuatro problemas que RAG ataca

| Problema del LLM solo | Cómo lo resuelve RAG |
|---|---|
| **Corte de conocimiento** (no sabe nada tras su fecha de entrenamiento) | Recupera información actual de una fuente que tú actualizas |
| **Datos privados** (no conoce tus documentos) | Indexa y consulta tus documentos, sin reentrenar |
| **Alucinación** (inventa cuando no sabe) | Ancla la respuesta en pasajes recuperados (evidencia) |
| **Sin atribución** (no puedes verificar) | Puede **citar la fuente** de cada afirmación |

El cuarto es subestimado pero crucial en entornos serios (salud, legal, finanzas): RAG permite responder **con citas**, de modo que un humano pueda verificar. Sin atribución, una respuesta de LLM es "confía en mí"; con RAG, es "esto dice el documento X, párrafo Y".

## El flujo RAG, de punta a punta

RAG tiene dos fases. **Indexación** (offline, una vez o periódica):
1. **Cargar** tus documentos (PDFs, wikis, tickets…).
2. **Trocear** (chunking) en fragmentos manejables ([[gen-rag2]]).
3. **Embeber** cada fragmento en un vector que captura su significado ([[gen-rag2]]).
4. **Indexar** esos vectores en una base de datos vectorial.

**Consulta** (online, en cada pregunta):
5. **Embeber la pregunta** del usuario en el mismo espacio.
6. **Recuperar** los $k$ fragmentos más similares (búsqueda por vecinos cercanos).
7. **Aumentar** el prompt: insertar esos fragmentos como contexto + la pregunta.
8. **Generar**: el LLM responde **usando** ese contexto (idealmente, citando).

La frase clave: *RAG no cambia el modelo; cambia lo que el modelo ve justo antes de responder.* Es ingeniería de **contexto**, no de pesos.

## RAG vs fine-tuning: dos formas de "enseñarle" al modelo

Confusión frecuentísima. Sirven a cosas distintas:

- **RAG** inyecta **conocimiento** en tiempo de consulta (hechos, documentos). Ventajas: se actualiza al instante (cambias un documento y listo), permite atribución, no requiere reentrenar, y es trazable. Ideal para **"¿qué dice mi base de conocimiento?"**.
- **Fine-tuning** ajusta los **pesos** del modelo con ejemplos. Cambia **comportamiento/estilo/formato** (hablar como abogado, devolver JSON), no inyecta hechos frescos de forma fiable. Caro de actualizar.

Regla práctica (eco del consenso de la industria, p. ej. [Huyen, *Designing ML Systems*](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)): **RAG para conocimiento; fine-tuning para comportamiento.** Y se combinan. Meter "hechos" por fine-tuning es caro y propenso a que el modelo los olvide o los mezcle; meter "estilo" por RAG no funciona.

## Mini-ejemplo trabajado

Pregunta a un LLM sin RAG: *"¿Cuál es nuestra política de reembolsos para clientes enterprise?"* El modelo nunca vio tu política → inventa una plausible ("30 días, sin preguntas") que **suena** verosímil y es **falsa**. Con RAG: el sistema embebe la pregunta, recupera de tu wiki el fragmento real ("reembolsos enterprise: 60 días, requiere aprobación del account manager"), lo inserta en el prompt, y el LLM responde citándolo. 

Predicción antes de seguir: si el recuperador trae el fragmento **equivocado** (o ninguno), ¿qué pasa con la respuesta? → el LLM responderá con confianza basándose en contexto irrelevante, o volverá a alucinar. **RAG es tan bueno como su recuperación**: garbage in, garbage out. Por eso la calidad del retriever ([[gen-rag2]], [[gen-rag3]]) y su evaluación ([[gen-rag4]]) son el corazón del sistema.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "El modelo no conoce datos posteriores a su entrenamiento" | RAG (recuperar info actual) |
| "Necesito que responda sobre MIS documentos privados" | RAG, no fine-tuning |
| "Debo poder citar la fuente de cada respuesta" | RAG con atribución |
| "Quiero que hable en cierto estilo/formato fijo" | fine-tuning, no RAG |
| "El modelo inventa hechos con confianza" | ancla con RAG (+ evaluación de fidelidad) |

## Errores típicos

- **Usar fine-tuning para inyectar hechos:** caro, no se actualiza y el modelo los mezcla; eso es trabajo de RAG.
- **Creer que RAG elimina las alucinaciones:** las **reduce** si la recuperación es buena; con contexto malo, el modelo igual alucina o lo ignora.
- **Olvidar la atribución:** recuperar y no citar desperdicia la mayor ventaja de RAG (verificabilidad).
- **Tratar el RAG como "solo meter todo al prompt":** sin recuperación selectiva, saturas el contexto (y el costo) y empeoras la respuesta.

## Contraejemplo y caso borde

- **Contraejemplo (parece que RAG sobra):** si la pregunta es de **razonamiento puro** sin hechos externos ("resume este texto que te doy", "escribe un poema"), RAG no aporta — no hay nada que recuperar. RAG brilla cuando la respuesta **depende de conocimiento que el modelo no tiene memorizado**.
- **Caso borde (recuperación tóxica):** si un atacante coloca un documento en tu base con instrucciones ocultas, el RAG lo recuperará y lo pasará al modelo como contexto "confiable" → **indirect prompt injection / RAG poisoning** ([[cyber-llm1]], [[cyber-llm2]]). RAG amplía la capacidad **y** la superficie de ataque: todo lo recuperado es entrada no confiable.

## Transferencia isomorfa

- **RAG ↔ atención sobre una base de conocimiento:** en [[gen-tf2]], la Query buscaba entre Keys y recuperaba Values; en RAG, la pregunta (Query) busca entre embeddings de documentos (Keys) y recupera pasajes (Values). RAG es **atención a escala de corpus**, sin softmax global.
- **RAG ↔ examen a libro abierto:** en vez de memorizar todo (fine-tuning / estudiar de memoria), llevas el libro y consultas la página relevante en el momento. Cambia el problema de "recordar" a "encontrar y usar".
- **RAG ↔ índice de base de datos:** no escaneas toda la tabla; el índice te lleva a la fila relevante. RAG es el índice semántico del conocimiento no estructurado.

Moraleja de la arista: *RAG es examen a libro abierto: no memorices hechos, aprende a recuperarlos y a responder con la fuente delante.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para 3 tareas (responder sobre tu wiki interna, escribir en tono formal, contestar noticias de hoy), decide RAG, fine-tuning o ninguno, y justifica.
- **Misión externa (lab vivo):** lee la introducción del paper [RAG (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) y la guía [What is RAG? (AWS)](https://aws.amazon.com/what-is/retrieval-augmented-generation/). **Criterio de cierre:** explicar el flujo indexar→recuperar→aumentar→generar sin mirar.
- **Mini-entregable:** un diagrama del flujo RAG (las 8 etapas, indexación + consulta) con una frase por etapa.

---

> **Síntesis:** **RAG** ancla al LLM en conocimiento externo para atacar cuatro males —**corte de conocimiento, datos privados, alucinación y falta de atribución**—. Su flujo: **indexar** (cargar→trocear→embeber→indexar) y, por consulta, **recuperar→aumentar→generar**. No cambia los pesos del modelo, cambia **lo que ve antes de responder** (es ingeniería de contexto). Regla: **RAG para conocimiento, fine-tuning para comportamiento.** RAG es **atención a escala de corpus** / un examen a libro abierto, y es **tan bueno como su recuperación** — y todo lo recuperado es **entrada no confiable** (superficie de ataque, [[cyber-llm2]]).

---

**Referencias**

- Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- Gao, Y., et al. (2023). Retrieval-augmented generation for large language models: A survey. [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
- Amazon Web Services. (n.d.). What is retrieval-augmented generation (RAG)? [aws.amazon.com](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
- Huyen, C. (2022). *Designing machine learning systems*. O'Reilly. [Sitio](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)

*Retrieval: (1) ¿qué cuatro problemas del LLM ataca RAG?; (2) ¿cuáles son las etapas de indexación y de consulta?; (3) ¿cuándo RAG y cuándo fine-tuning?; (4) ¿por qué "RAG es tan bueno como su recuperación" y qué riesgo de seguridad introduce?*
