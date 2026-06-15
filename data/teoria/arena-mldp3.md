# Patrones de entrenamiento y de serving resiliente

## Entrenamiento

- **Useful Overfitting:** renunciar a la generalización y **sobreajustar a propósito** cuando (1) no hay ruido y (2) tienes el dataset **completo** (todas las entradas posibles). Caso típico: aproximar la solución de un **PDE/sistema dinámico** tabulable (sobreajustar = interpolar). También **overfit a un batch** pequeño como *sanity check*: un modelo bien configurado DEBE poder llevar un batch a pérdida ~0; si no, hay un bug.
- **Checkpoints:** guardar periódicamente el **estado COMPLETO** (no solo el modelo exportado: faltarían epoch/batch, estado del learning rate, dropout, historial RNN). Da **resiliencia**, **early stopping / checkpoint selection** (entrena de más y elige el mejor, por el *double descent*) y **fine-tuning** (reanudar desde un checkpoint del inicio de fase 2 y entrenar pocas epochs con datos frescos). La **regularización** puede ser mejor que early stopping porque usa todo el dataset.
- **Transfer Learning:** reusar un modelo preentrenado en la **misma modalidad** y tarea similar, **quitar la salida, congelar** el resto y entrenar una cabeza nueva. La penúltima capa es el **bottleneck**. Permite alta precisión con cientos de ejemplos.
- **Distribution Strategy:** distribuir el entrenamiento. **Data parallelism** (cada worker, distinto subconjunto de datos, copia del modelo) vs **model parallelism** (partir el modelo). Síncrono (**all-reduce**, agregar gradientes cada paso) vs asíncrono (parameter server, tolera lentos pero arriesga *stale gradients*).
- **Hyperparameter Tuning:** los **parámetros** los aprende el modelo; los **hiperparámetros** los fijas tú. Grid search no escala (explosión combinatoria, no aprende de los trials); random es más rápido pero ciego; **optimización bayesiana** (keras-tuner) aprende de los trials previos.

## Serving resiliente

- **Stateless Serving Function:** exporta el modelo como **función sin estado** (salida solo según la entrada) → instancias compartibles desde un pool → escala a miles de QPS.
- **Batch Serving:** inferencia **asíncrona masiva** sobre infraestructura distribuida (BigQuery/Spark/Beam). Para puntuar millones de ítems sin latencia crítica (problema embarazosamente paralelo).
- **Two-Phase Predictions:** modelo **pequeño on-device** (tarea simple, corre siempre) + modelo **complejo en la nube** (solo cuando hace falta). Ej.: wake word + consulta. El edge suele requerir **cuantización** (menos bytes, menos tamaño/latencia, posible pérdida de precisión).
- **Keyed Predictions:** el cliente envía una **clave** con cada input; el modelo la devuelve junto a la predicción → casar entradas y salidas **desordenadas** de un job distribuido y evitar hot spots.

---

## Mini-ejemplo trabajado: overfit a un batch como sanity check

Antes de entrenar horas, haz esta prueba de 5 minutos: toma **un solo batch** de ~8 ejemplos y entrénalo sin parar. Un modelo bien configurado **debe** poder llevar ese batch a pérdida ≈ 0 (memorizarlo). Si *no* lo consigue, no tienes un problema de generalización: tienes un **bug** (learning rate, función de pérdida, conexión rota, labels mal formateadas). Es el patrón **Useful Overfitting** en su versión diagnóstica.

Y ojo: este "sobreajustar a propósito" solo es *legítimo como solución* cuando (1) no hay ruido y (2) tienes el dataset **completo** (todas las entradas posibles), como al tabular la solución de una PDE. En cualquier otro caso, sobreajustar es el enemigo.

**Predicción antes de seguir:** un checkpoint que solo guarda el modelo exportado, ¿basta para reanudar el entrenamiento tras un crash? No: falta el **estado completo** (epoch/batch, estado del learning rate, dropout, historial RNN). El checkpoint ≠ el modelo exportado.

## Prototipo, contraejemplo y caso borde

- **Prototipo (transfer learning):** pocos cientos de ejemplos en una modalidad conocida → reusa un preentrenado, congela hasta el **bottleneck** (penúltima capa) y entrena una cabeza nueva.
- **Contraejemplo (Useful Overfitting indebido):** sobreajustar a propósito cuando *sí* hay datos no vistos o ruido → memorizas ruido, desastre.
- **Caso borde (two-phase en el edge):** wake-word on-device (corre siempre, pequeño) + modelo grande en la nube (solo cuando se activa) → exige **cuantización** que puede costar algo de precisión.

## Errores típicos

- **Conceptual:** confundir **parámetros** (los aprende el modelo) con **hiperparámetros** (los fijas tú) — y hacer grid search que no escala ni aprende de los trials.
- **Técnico:** guardar solo el modelo exportado como "checkpoint" → no puedes reanudar ni hacer fine-tuning.
- **De despliegue:** servir con estado en vez de una **función sin estado** → no escala a miles de QPS.

## Transferencia isomorfa

- **Two-Phase Predictions ↔ Cascade de modelos:** un modelo barato que filtra y delega lo difícil a uno caro es la misma idea que la cascade usual/raro (conecta con [[arena-mldp2]]).
- **Batch Serving ↔ problema embarazosamente paralelo / Map-Reduce:** puntuar millones de ítems sin latencia es map puro sobre infra distribuida (conecta con [[arena-sd1]], estimación a escala).
- **Stateless Serving Function ↔ funciones puras / horizontal scaling:** salida solo según entrada = instancias intercambiables desde un pool, el principio de escalado horizontal (conecta con [[arena-rml1]], models as code).

Moraleja de la arista: *sobreajusta a propósito solo para diagnosticar (un batch a pérdida 0) o tabular funciones exactas; guarda el estado completo, congela hasta el bottleneck y sirve sin estado.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Aproximo una función exacta sin datos no vistos | Useful Overfitting |
| "¿Por qué no aprende nada?" | Overfit a un batch (sanity check) |
| Entrenamiento largo, riesgo de fallo | Checkpoints (estado completo) |
| Pocos datos, modalidad conocida | Transfer learning (congelar al bottleneck) |
| Entrenamiento demasiado lento | Distribution Strategy (data/model parallelism) |
| Muchos hiperparámetros caros | Optimización bayesiana |
| Miles de QPS | Stateless serving function |
| Puntuar millones sin latencia | Batch serving |
| Edge sin buena conexión | Two-phase (on-device + nube) + cuantización |
| Job distribuido, salidas desordenadas | Keyed predictions |

---

> **Síntesis:** Para **entrenar**: sobreajusta solo cuando no hay datos no vistos (**Useful Overfitting**), guarda el **estado completo** (**Checkpoints** → early stopping/fine-tuning), reusa preentrenados **congelando hasta el bottleneck** (**Transfer Learning**), distribuye (**data/model parallelism**) y tunea con **optimización bayesiana**. Para **servir**: exporta una **función sin estado**, usa **batch** para volumen sin latencia, **dos fases** (edge+nube) con **cuantización**, y **claves** para casar entradas/salidas en lotes distribuidos.

---

*Retrieval: (1) ¿cuándo es válido el Useful Overfitting?; (2) ¿por qué el checkpoint ≠ modelo exportado?; (3) ¿qué es el bottleneck en transfer learning?; (4) ¿cuándo batch vs two-phase y para qué sirven las keyed predictions?*
