# Reglas de ML (Google) I: antes del ML y tu primer pipeline

La consigna de Zinkevich: **«haz machine learning como el gran ingeniero que eres, no como el gran experto en ML que no eres»**. La mayoría de los problemas son de ingeniería; casi todas las ganancias vienen de **buenas features**, no de algoritmos sofisticados. Enfoque básico: (1) pipeline sólido de punta a punta, (2) objetivo razonable, (3) features de sentido común de forma simple, (4) mantener el pipeline sólido. Diverge solo cuando se agoten los trucos simples: **añadir complejidad frena los lanzamientos futuros**.

## Antes del ML (Reglas 1-3)

- **R1 — No temas lanzar sin ML.** El ML necesita datos. Sin datos, una **heurística simple** te lleva lejos (≈50% del camino): tasa de instalación para rankear apps, lista negra para spam, ordenar contactos por uso reciente. No uses ML si no es imprescindible hasta tener datos.
- **R2 — Diseña e implementa métricas primero.** Antes de formalizar el ML, **instrumenta y rastrea todo** lo posible: es más fácil pedir permisos pronto, tendrás histórico, y no acabarás grepeando logs. Un **framework de experimentos** (buckets de usuarios, stats por experimento) es clave.
- **R3 — Prefiere ML a una heurística compleja.** Una heurística simple saca el producto; una **heurística compleja es inmantenible**. Con datos e idea básica, pasa a ML: el modelo aprendido es más fácil de actualizar y mantener.

## Tu primer pipeline (Reglas 4-7)

- **R4 — Primer modelo simple + infraestructura correcta.** El primer modelo da el mayor empujón, así que **no necesita ser sofisticado**; tendrás más problemas de infra de los que esperas. Decide cómo llegan los ejemplos, qué es «bueno/malo» y cómo integrar el modelo (live vs precomputado). Features simples → llegan bien al algoritmo, el modelo aprende pesos razonables y llegan bien al servidor. Algunos equipos buscan un **lanzamiento «neutral»** que de-prioriza las ganancias de ML para no distraerse.
- **R5 — Prueba la infraestructura independientemente del ML.** Encapsula el aprendizaje y testea todo alrededor: que entren los datos (feature columns pobladas, inspeccionar input) y que salga el modelo (mismo score en entrenamiento y serving → R37).
- **R6 — Cuidado con datos descartados al copiar pipelines.** Copiar un pipeline (cargo cult) suele arrastrar drops de datos que el nuevo pipeline sí necesita (p.ej. logear solo lo que el usuario vio → no puedes modelar por qué NO se vio algo).
- **R7 — Convierte heurísticas en features, o manéjalas externamente.** Las heurísticas existentes contienen intuición valiosa: mínalas. Cuatro vías: (1) **preprocesar** con la heurística (p.ej. bloquear ya-en-lista-negra), (2) **crear una feature** con su valor, (3) **minar los inputs crudos** de la heurística, (4) **modificar el label**.

## Monitoreo (Reglas 8-11)

- **R8 — Conoce los requisitos de frescura.** ¿Cuánto se degrada con un modelo de 1 día/semana/trimestre? Eso fija las prioridades de monitoreo y la frecuencia de reentrenamiento.
- **R9 — Detecta problemas antes de exportar el modelo.** Un problema en un modelo ya exportado es **user-facing**; antes de exportar es solo de entrenamiento y el usuario no lo nota. Haz sanity checks (AUC/ROC en held-out). *Problemas pre-export → alerta por email; en un modelo user-facing → page.*
- **R10 — Vigila los fallos silenciosos.** Propio del ML: si una tabla joinada deja de actualizarse, el sistema **se ajusta y decae lentamente** (una tabla 6 meses obsoleta cuyo refresco dio +2% de instalación). Rastrea estadísticas de los datos e inspecciónalos.
- **R11 — Da dueños y documentación a las feature columns.** Sabe quién mantiene cada una; documenta qué es, de dónde viene y cómo ayuda, para que el conocimiento no se pierda cuando alguien se va.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «Empecemos con un modelo de ML» y no hay datos | R1: heurística simple primero; ML cuando haya datos |
| «Instrumentamos métricas luego» | R2: métricas y framework de experimentos PRIMERO |
| La heurística ya tiene 20 reglas if/else | R3: heurística compleja es inmantenible → ML |
| Primer modelo con red neuronal fancy | R4: simple + infra correcta; el 1er modelo da el mayor empujón |
| Copiar un pipeline existente | R6: revisa qué datos descarta el viejo y el nuevo necesita |
| El modelo «funciona» pero la métrica baja sola | R10: fallo silencioso, tabla obsoleta; rastrea stats de datos |

---

> **Síntesis:** haz ML «como ingeniero»: pipeline sólido → objetivo razonable → features simples → mantenerlo. **Lanza sin ML** con una heurística mientras no haya datos (R1-3), pon el **primer modelo simple con la infra correcta** y pruébala aparte (R4-7), y **monitorea** frescura, fallos silenciosos y dueños de features (R8-11). Añadir complejidad antes de tiempo frena los lanzamientos.

---

*Retrieval: (1) ¿por qué lanzar sin ML y cuándo pasar a ML?; (2) ¿por qué el primer modelo simple y testear la infra aparte?; (3) ¿qué es un fallo silencioso en ML y cómo lo detectas?; (4) ¿alerta por email o page según dónde esté el problema del modelo?*
