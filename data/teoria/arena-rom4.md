# Reglas de ML (Google) IV: Fase III — crecimiento lento, modelos complejos

Señales de que la Fase II se acaba: las ganancias mensuales disminuyen y aparecen **trade-offs entre métricas** (unas suben, otras bajan). Como las ganancias cuestan más, el ML se vuelve más sofisticado. Esta sección tiene más reglas «blue-sky»: tras la Fase III cada equipo halla su camino.

## Reglas 38-43

- **R38 — No malgastes tiempo en features nuevas si el problema son objetivos desalineados.** Si las metas de producto no las cubre el objetivo algorítmico actual, cambia **el objetivo o las metas de producto**, no añadas features. P.ej. optimizas clicks/descargas pero decides lanzamientos según raters humanos.
- **R39 — Las decisiones de lanzamiento son un proxy de las metas de producto a largo plazo.** Alice baja el log loss de predecir instalaciones y sube la tasa de instalación en vivo, pero en la review alguien nota que los DAU caen 5% y NO se lanza: las decisiones de lanzamiento dependen de **múltiples criterios**, solo algunos optimizables por ML. No hay «hit points» del producto: engagement, DAU, 30-DAU, revenue, ROI del anunciante son **proxies** de metas a largo plazo (satisfacer usuarios/partners, crecer, beneficio). **Los lanzamientos fáciles son cuando todas las métricas mejoran (o no empeoran).** No hay un ranking explícito de combinaciones de métricas: con A=(1M DAU, \$4M/día) y B=(2M DAU, \$2M/día), un equipo en A no cambiaría a B y uno en B no cambiaría a A — cada métrica cubre un riesgo distinto, y predecir cambios de métrica conlleva riesgo. El multi-objetivo ayuda, pero predecir el éxito futuro de un sitio es **AI-complete**.
- **R40 — Mantén los ensembles simples.** Modelos unificados que toman features crudas y rankean son los más fáciles de depurar, pero un **ensemble** (modelo que combina scores de otros) puede ir mejor. Para mantenerlo simple, cada modelo debe ser **o bien un ensemble que solo toma el input de otros modelos, o un modelo base que toma muchas features, pero no ambos**. Usa un modelo simple para combinar que solo toma las salidas de los base, e impón propiedades: que **subir el score de un clasificador base no baje** el score del ensemble (monotonicidad); que los modelos entrantes sean interpretables/calibrados.
- **R41 — Cuando el rendimiento se estanca, busca fuentes de información cualitativamente NUEVAS, no refines las señales existentes.** Si ya añadiste demografía, palabras del documento, exploraste templates y tuneaste regularización y no ves >1% de mejora en varios trimestres: construye infra para features **radicalmente distintas** (historial del usuario del último día/semana/año, datos de otra property, knowledge graph, deep learning) y ajusta expectativas de ROI.
- **R42 — No esperes que diversidad, personalización o relevancia estén tan correlacionadas con la popularidad como crees.** Diversidad, personalización y relevancia se definen como **distintas de lo ordinario**, y «lo ordinario es difícil de batir». Si mides clicks/tiempo/watches/+1s/reshares, estás midiendo **popularidad**, y las features de personalización/diversidad suelen recibir menos peso (o signo distinto) del esperado. No significa que no valgan: usa post-procesamiento para inyectarlas, y si los objetivos a largo plazo suben, decláralas valiosas (o modifica el objetivo).
- **R43 — Tus amigos tienden a ser los mismos entre productos; tus intereses, no.** Google ha tenido tracción transfiriendo un modelo que predice la cercanía de una conexión de un producto a otro («tus amigos son quienes son»), pero la **personalización de intereses NO transfiere** bien entre divisiones de producto. Aun así, saber que un usuario tiene historial en otra property puede ayudar (su mera presencia es señal).

---

## Mini-ejemplo trabajado: por qué no hay "mejor" lanzamiento (R39)

Dos estados posibles del producto:

- **A = (1M DAU, \$4M/día)** — menos usuarios, más ingreso por usuario.
- **B = (2M DAU, \$2M/día)** — el doble de usuarios, la mitad de ingreso.

¿Cuál es mejor? **No hay respuesta objetiva.** Un equipo que está en A no se movería a B (perdería ingreso) y uno en B no se movería a A (perdería usuarios). Cada métrica cubre un **riesgo distinto** (crecer vs monetizar) y no existe un *ranking* explícito de combinaciones. Por eso una decisión de lanzamiento es **multi-métrica**: Alice baja el log loss y sube la instalación en vivo, pero si los DAU caen 5%, **no se lanza**. Predecir el éxito futuro de un sitio es, literalmente, **AI-complete**.

**Predicción antes de seguir:** llevas 3 trimestres sin pasar del 1% de mejora retocando regularización y features de texto. ¿Sigues refinando? No (R41): busca una **fuente de información cualitativamente nueva** (historial del usuario, datos de otra property, knowledge graph), no más ajuste de lo que ya tienes.

## Prototipo, contraejemplo y caso borde

- **Prototipo (lanzamiento fácil):** todas las métricas mejoran o ninguna empeora → decisión trivial.
- **Contraejemplo (objetivos desalineados, R38):** el rendimiento se estanca y echas features nuevas, pero el problema real es que el **objetivo no cubre las metas de producto** (optimizas clicks pero lanzas según raters) → cambia el objetivo, no añadas features.
- **Caso borde (personalización que rinde poco, R42):** mides clics/tiempo → mides **popularidad**; diversidad y personalización se *definen* como lo no-ordinario, y "lo ordinario es difícil de batir", así que reciben menos peso del esperado.

## Errores típicos

- **Conceptual:** buscar un único número que decida el lanzamiento; las métricas de producto son **proxies** de metas a largo plazo, sin "hit points".
- **De diseño:** apilar modelos sobre modelos entrenados aparte sin estructura → ensemble frágil; manténlo simple (base XOR combinador, monotónico, R40).
- **De transferencia:** reusar el modelo de **intereses** de un producto en otro (R43) — los amigos transfieren, los intereses no.

## Transferencia isomorfa

- **Lanzamiento multi-métrica ↔ frontera de Pareto / sin objetivo único:** A vs B es un par no dominado; elegir entre ellos es el problema multiobjetivo de cualquier sistema con trade-offs (conecta con [[arena-dmls1]], desacoplar objetivos).
- **"Medir clicks = medir popularidad" ↔ proxy desalineado:** optimizar un proxy fácil y creer que mides lo que quieres es el mismo riesgo de las métricas en quant o en evals de ML (conecta con [[arena-rml1]]).
- **Ensemble monotónico (R40) ↔ stacking con restricciones:** combinar scores de modelos base con un meta-modelo simple y monótono es stacking disciplinado (conecta con [[arena-mldp2]]).

Moraleja de la arista: *en la madurez no hay un número que mande; las decisiones son multi-métrica (Pareto), mides popularidad cuando crees medir calidad, y las ganancias vienen de información nueva, no de refinar la vieja.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Las metas de producto no las cubre el objetivo | R38: cambia objetivo o metas, no añadas features |
| «Subió mi métrica, ¿lanzo?» y otra métrica baja | R39: lanzamiento = decisión multi-métrica, proxy a largo plazo |
| A=(1M DAU,\$4M) vs B=(2M DAU,\$2M): ¿cuál? | R39: sin ranking explícito; cada métrica cubre un riesgo |
| Apilar modelos sobre modelos entrenados aparte | R40: ensemble simple, monotónico; base XOR combinador |
| Estancado en <1% de mejora por trimestres | R41: fuentes de info nuevas, no refinar lo existente |
| «Personalizo y no mejora como esperaba» | R42: mides popularidad; lo ordinario es difícil de batir |
| Reusar el modelo de intereses en otro producto | R43: amigos transfieren, intereses no |

---

> **Síntesis:** en la Fase III las ganancias escasean y aparecen trade-offs. Si el problema es de **objetivos desalineados**, cambia el objetivo/metas, no añadas features (R38). Las **decisiones de lanzamiento son multi-métrica** y proxies de metas a largo plazo, sin ranking explícito de combinaciones (R39). Mantén **ensembles simples y monotónicos** (R40), ante un plateau busca **fuentes de información nuevas** (R41), y recuerda que medir clicks mide **popularidad** (diversidad/personalización rinden menos de lo esperado, R42) y que los **amigos transfieren entre productos pero los intereses no** (R43).

---

*Retrieval: (1) ¿qué hacer si el problema son objetivos desalineados (R38)?; (2) ¿por qué las decisiones de lanzamiento son multi-métrica y qué ilustra el ejemplo DAU vs revenue?; (3) ¿cuál es la regla para mantener un ensemble simple (R40)?; (4) ¿por qué personalización/diversidad rinden menos de lo esperado (R42)?*
