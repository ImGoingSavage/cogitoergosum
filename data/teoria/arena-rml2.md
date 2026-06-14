# Datos como pasivo y principios de sistemas de entrenamiento confiables

## El dato también es un pasivo

"Más datos == mejor" es falso si los datos exponen **riesgo legal/ético**. Recolectar, almacenar y curar expone complejidad: hay que cumplir leyes, restringir el acceso (incluso a empleados), anonimizar y **poder borrar**.

- **Pseudonimización** (reversible con un dato/sistema extra): protege de inspección casual, pero trátala como **tan arriesgada como el dato crudo**.
- **Anonimización** (romper la conexión con la persona): es difícil. *Sweeney* mostró que el **87%** de la gente es identificable con solo **género + edad + código postal**.
- **Borrar de verdad** es difícil (copias, backups, índices). Dos tácticas: **reescritura periódica** (omitir lo "borrado" la próxima regeneración) y **cifrar todo y tirar la llave** (perder la llave = dato ilegible en todos los backups).

## Sensibilidad de los pipelines de ML a los datos

Un pipeline de ML es **inusualmente sensible** a su entrada. Ejemplo: un apagón de pagos solo en el sitio en español hace caer las compras en español; el modelo "aprende" que el español no compra, muestra menos resultados en español y **empeora las ventas incluso después** del apagón. La pregunta clave al perder datos: **¿la pérdida es sesgada?** Perder 1/1000 al azar (MCAR) es ignorable; perder todo España o las mañanas (MAR/MNAR) introduce sesgos nuevos.

## El ciclo de vida del dato

Creación → ingestión (filtrado/muestreo) → procesamiento (validación, limpieza/consistencia, enriquecimiento/etiquetado) → post-procesamiento (gestión, almacenamiento, análisis) → borrado. **Normalización**: scaling a rango, clipping, log scaling, z-score — todas peligrosas si los parámetros se calculan sobre datos distintos a donde se aplican.

## Feature store y model management

- **Feature store:** lugar dedicado para las features. Frente a "archivos en un directorio" resuelve (1) **consistencia** (evita training-serving skew y semánticas que derivan) y (2) **colaboración/procedencia** (quién añadió cada feature, cuándo y por qué).
- **Model management system:** ata serving↔training↔almacenamiento. Tres funciones: metadatos del modelo (config, hiperparámetros, autoría), **snapshots** (transfer learning + recuperación ante desastre) y metadatos de features.

## Principios de confiabilidad del entrenamiento

- **Models will be retrained** → asume que todo modelo se reentrenará; versiona configs, datos y metadatos, guarda snapshots.
- **Multiple versions at the same time** → sirve varias versiones a la vez (A/B de modelos, rollback rápido).
- **Good models will become bad** → ten un **fallback** (heurística) y **rollback**; la trampa: si el modelo supera con mucho a la heurística, el fallback deja de bastar.
- **Data will be unavailable** → planéalo; pregunta si la pérdida es sesgada (MCAR/MAR/MNAR).
- **Models can train too fast** → race conditions en entrenamiento distribuido hacen divergir el modelo; mitiga sincronizando el estado (RAM) y limitando la tasa de actualización.
- **Utilization ≠ efficiency** → utilización = usado/pagado; eficiencia = valor/coste. Alta utilización no implica producir valor.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Recojamos todos los datos posibles" | El dato es pasivo: ¿riesgo legal/ético?, ¿puedo borrarlo? |
| "Ya quité el nombre, está anonimizado" | No: 87% identificable con género+edad+CP |
| "Perdimos parte de los datos" | ¿La pérdida es sesgada? (MCAR ok; MAR/MNAR peligroso) |
| "El modelo rinde peor en prod que en eval" | Sospecha training-serving skew |
| "Este modelo no hace falta reentrenarlo" | Falso: versiona todo, se reentrenará |
| "Entreno más rápido con más learners y empeora" | Quizá entrenas demasiado rápido (race conditions) |

---

> **Síntesis:** Trata los datos como **activo y pasivo**: anonimizar es difícil y borrar de verdad también (cifra y tira la llave). Los pipelines de ML son **sensibles a pérdidas sesgadas** de datos. Construye un **feature store** y un **model management system** versionados. Y aplica los principios de confiabilidad: **todo modelo se reentrenará**, habrá **varias versiones a la vez**, un buen modelo **se volverá malo** (ten fallback + rollback), los datos **faltarán** y un modelo puede **entrenarse demasiado rápido**.

---

*Retrieval: cierra y responde: (1) ¿por qué el dato es un pasivo y cómo se borra "de verdad"?; (2) explica el ejemplo del apagón en español; (3) ¿qué dos problemas resuelve un feature store?; (4) enuncia tres principios de confiabilidad del entrenamiento.*
