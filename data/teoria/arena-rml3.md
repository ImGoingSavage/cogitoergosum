# Serving, monitoreo y observabilidad de modelos

## De qué trata esta lección (y qué sabrás hacer al final)

Un modelo en producción vive o muere por cómo se **sirve** y cómo se **vigila**. Esta lección construye, desde cero, las cuatro preguntas que definen la arquitectura de serving (carga, latencia, dónde vive, hardware) y las cuatro arquitecturas (offline, online, MaaS, edge), más el salto mental de **monitoreo** ("¿funciona?") a **observabilidad** ("¿por qué falla?", con métricas troceables por slice).

Al terminar podrás: (1) entender por qué replicar sube el throughput pero **no** baja la latencia de una predicción (y qué sí la baja); (2) elegir entre offline/online/MaaS/edge según el problema; (3) saber qué añade la observabilidad sobre el monitoreo y por qué mirar la tail latency (p99) y los slices, no el promedio; y (4) reconocer el training-serving skew como causa de caídas evitables. El ejemplo de QPS vs latencia hace de hilo. Conecta con [[arena-dmls3]] (despliegue) y [[arena-obs1]] (observabilidad).

## Cuatro preguntas clave de serving

1. **Carga (QPS):** ¿cuántas queries por segundo? Estrategias: replicar, hardware acelerador (con batching), abaratar el modelo (menos features/capas, cuantización/sparsificación) y **cascadas** (un modelo barato resuelve los casos fáciles, los difíciles van a uno caro).
2. **Latencia:** ¿cuánto tiempo por predicción? **Replicar NO baja la latencia de UNA predicción** (sube el throughput); para eso usa hardware potente o abarata el modelo. Mira la **tail latency** (peor 1–5%), no solo la media.
3. **Dónde vive:** nube (escala fácil, +latencia de red, privacidad/jurisdicción), servidores propios (privacidad/latencia crítica/hardware especial, -flexibilidad) o **edge/on-device** (latencia/privacidad, pero tamaño/energía limitados y actualizar es difícil).
4. **Hardware:** deep = matrices **densas** → **GPU** (miles de ALUs); modelos **sparse** (pocas piezas de un universo grande) aprovechan poco la GPU → la **CPU** puede ser mejor.

## Cuatro arquitecturas de serving

- **Offline (batch inference):** precomputa predicciones a un store → predicción on-demand se vuelve **lookup**. + Simple, verificable (revisas TODAS las predicciones), rápido, roll-out/rollback por tablas. − Datos de antemano, no cubre la **cola larga** ni el contexto en línea, escala mal.
- **Online:** infiere en tiempo real con contexto. + **Adaptable** (se adapta al concept drift en inferencia), modelos suplementarios. − Presupuesto de latencia (store en memoria tipo Redis), despliegue complejo, no escala horizontal sin más, más supervisión.
- **MaaS (Model-as-a-Service):** modelo como **microservicio** con API. + Aislamiento, **escalado horizontal** (stateless), versionado y A/B fáciles, monitoreo centralizado. La estrategia más flexible y escalable.
- **Edge:** on-device. + Latencia/privacidad. − Tamaño limitado, actualizar es caro o imposible.

**Actualizar sin caída:** (1) doble RAM + hot-swap, o (2) sobre-aprovisionar réplicas y actualizar por turnos (10% fuera de línea, permite canarying).

## Monitoreo vs observabilidad

- **Monitoreo:** ¿el sistema funciona? (datos almacenables y visualizables).
- **Observabilidad:** atributo del software; métricas **etiquetadas/sliceables** que dejan inferir **por qué**. No solo `requests_total`, sino `requests_total{lang=es}`.

**El cambio de mentalidad:** el modelista usa métricas para **optimizar** antes de desplegar; falta usarlas para **detectar** después. Monitorea en tres capas —**modelo, datos y servicio**— durante todo el ciclo de vida.

**Training-serving skew:** diferencia de cómo se computa una feature (o qué datos hay) entre train y serving. Causa común de caídas **evitables** y difíciles de depurar; se manifiesta como caída sutil de calidad. Mantén el pipeline de features consistente y monitoréalo.

**Retraining como roll-forward:** el rollback es la táctica común; reentrenar es "roll-forward" — útil si el rollback no funciona, pero **no mitiga** si reentrenas sobre los mismos datos o si tarda demasiado.

---

## Mini-ejemplo trabajado: por qué replicar no baja la latencia de UNA predicción

Tu modelo tarda **200 ms** por predicción y recibes **1 000 QPS**, pero un solo servidor solo aguanta 500 QPS. Añades una segunda réplica → ahora aguantas 1 000 QPS. ¿Bajó la latencia? **No**: cada predicción **sigue tardando 200 ms**; lo que subió es el **throughput** (peticiones/seg), no la velocidad de una.

Para bajar la latencia de *una* predicción hay otras palancas: hardware más potente (GPU para matrices densas), o **abaratar el modelo** (menos features/capas, cuantización, o una **cascada** donde un modelo barato resuelve los casos fáciles y solo los difíciles van al caro). Y mide la **tail latency** (peor 1–5%), no la media: el usuario que sufre es el de la cola.

**Predicción antes de seguir:** el espacio de queries es acotado y conocido (recomendaciones diarias por usuario). ¿Online o batch? **Batch (offline)**: precomputas todo a un store y servir se vuelve un *lookup* — simple, verificable (revisas todas las predicciones), con rollback por tablas. Online solo si el input no se conoce de antemano.

## Prototipo, contraejemplo y caso borde

- **Prototipo (MaaS):** modelo como microservicio stateless → escalado horizontal, versionado y A/B fáciles, monitoreo centralizado.
- **Contraejemplo (replicar para latencia):** añadir réplicas esperando que *una* predicción sea más rápida → solo sube throughput.
- **Caso borde (modelo sparse en GPU):** un modelo disperso aprovecha poco las miles de ALUs de la GPU → a veces la **CPU** sirve mejor.

## Errores típicos

- **Conceptual:** confundir **throughput** (QPS) con **latencia** (tiempo de una predicción) — réplicas suben el primero, no bajan la segunda.
- **De medición:** mirar la latencia **media** en vez de la **tail** (p99) que define la peor experiencia.
- **De operación:** quedarse en monitoreo agregado sin **observabilidad por slices** → no ves el subgrupo afectado.

## Transferencia isomorfa

- **Cascada de serving ↔ two-phase predictions:** un modelo barato que filtra y delega lo difícil es el patrón cascade/two-phase de los design patterns (conecta con [[arena-mldp3]]).
- **Observabilidad por slices ↔ alta cardinalidad:** `requests_total{lang=es}` en vez del agregado es la misma idea de trocear por dimensión (conecta con [[arena-obs1]]).
- **Training-serving skew ↔ paridad de features:** que la feature se compute igual en train y serving es el problema recurrente de [[arena-rom3]] y [[arena-dmls4]].

Moraleja de la arista: *réplicas suben el throughput, no bajan la latencia de una predicción (para eso, hardware/modelo más barato/cascada); y vigila la cola y los slices, no el promedio.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Tengo mucho QPS" | Replica / acelera+batch / abarata / cascada |
| "La latencia de una predicción es alta" | Hardware potente o modelo más barato — NO más réplicas |
| "El espacio de queries es acotado y conocido" | Offline/batch a un store |
| "Necesito contexto de sesión en tiempo real" | Online o MaaS |
| "La métrica agregada se ve bien pero hay quejas" | Slicing (observabilidad): busca el subgrupo afectado |
| "Rinde peor en prod que en eval offline" | Training-serving skew |

---

> **Síntesis:** La arquitectura de serving sale de **carga, latencia, dónde vive y hardware**. Elige entre **offline** (precompute, verificable), **online** (tiempo real, adaptable), **MaaS** (microservicio escalable) y **edge** (on-device). Para operar, pasa de monitoreo a **observabilidad** (métricas en slices), adopta la mentalidad de **detectar** en producción (no solo optimizar antes), vigila el **training-serving skew** y recuerda que el **retraining** no siempre mitiga una caída.

---

*Retrieval: cierra y responde: (1) ¿por qué replicar no baja la latencia de una predicción?; (2) ¿cuándo offline vs online vs MaaS vs edge?; (3) ¿qué añade la observabilidad sobre el monitoreo?; (4) ¿qué es el training-serving skew?*
