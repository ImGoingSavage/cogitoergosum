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

## Mini-ejemplo trabajado: filtro de spam, regla por regla

Sigue el orden de Zinkevich en un caso concreto:

1. **Sin datos (R1):** lanzas con una **lista negra** de dominios + "≥3 enlaces ⇒ sospechoso". Cubres ~50% del problema y *ya recoges datos* (qué se marcó, qué reportó el usuario).
2. **Instrumentas primero (R2):** registras cada decisión y el feedback antes de tocar ML; en un mes tienes histórico para entrenar.
3. **Heurística simple → ML (R3):** cuando la lista negra crece a 200 reglas if/else inmantenibles, pasas a un clasificador.
4. **Primer modelo simple + infra (R4-R5):** regresión logística con features obvias (nº de enlaces, dominio en lista negra como **feature**, no como filtro — R7); testeas la tubería *sin* el modelo.
5. **Fallo silencioso (R10):** semanas después la precisión cae sola. No hay error en logs: la tabla de "dominios reportados" dejó de refrescarse hace 40 días y el modelo **se reajustó** alrededor del dato podrido. Solo lo ves si rastreas estadísticas de los datos de entrada.

**Predicción antes de seguir:** ese fallo del paso 5, ¿salta como `page` o como email? Como el modelo malo ya está en producción, es **user-facing → page** (R9); si lo hubieras cazado antes de exportar, bastaba un email.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** problema con patrón + datos que llegan + error tolerable → heurística primero, ML después, pipeline simple y monitoreado.
- **Contraejemplo (ML prematuro):** montar una red neuronal el día 1 sin datos ni instrumentación → mucha infra rota y cero señal; la heurística habría sacado el 50%.
- **Caso borde (heurística compleja):** una heurística con 200 reglas que *funciona* pero nadie puede mantener — la señal de que tocaba ML hace tiempo (R3).

## Errores típicos

- **Conceptual:** creer que el algoritmo sofisticado es la palanca; casi siempre lo son **las features y la infra** ("haz ML como ingeniero, no como experto en ML").
- **Técnico:** copiar un pipeline (cargo cult) arrastrando *drops* de datos que el nuevo caso sí necesita (R6).
- **De monitoreo:** vigilar solo métricas de modelo y no las **estadísticas de los datos de entrada** → los fallos silenciosos pasan inadvertidos.

## Transferencia isomorfa

Las reglas de Zinkevich son ingeniería de propósito general:

- **"Lanza sin ML" ↔ evitar optimización prematura:** empezar simple y complejizar solo al agotar lo barato es la misma disciplina que no microoptimizar antes de medir.
- **Fallo silencioso por tabla obsoleta ↔ data drift / leakage:** un input que decae sin lanzar error es exactamente el monitoreo de distribución de [[arena-dmls4]]; el modelo "se adapta" al dato podrido en vez de quejarse.
- **Heurística → feature (R7) ↔ feature engineering:** convertir conocimiento de dominio en una columna es el corazón del feature engineering (conecta con [[arena-cds1]]).

Moraleja de la arista: *el primer modelo es de ingeniería, no de ML; las ganancias vienen de features e infra fiable, y el peor bug del ML es el que no lanza error.*

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
