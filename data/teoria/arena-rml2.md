# Datos como pasivo y principios de sistemas de entrenamiento confiables

## De qué trata esta lección (y qué sabrás hacer al final)

"Más datos siempre es mejor" es una de las medias verdades más peligrosas del ML. Esta lección construye, desde cero, la cara incómoda: cada dato es también un **pasivo** (legal, ético, de borrado), anonimizar es casi imposible, y los pipelines de ML son **inusualmente sensibles** a pérdidas *sesgadas* de datos. Luego enuncia los principios de confiabilidad que asumen que todo se reentrenará, todo se romperá y todo necesitará rollback.

Al terminar podrás: (1) entender por qué quitar el nombre no anonimiza (Sweeney: 87% identificable con género+edad+CP) y cómo se borra "de verdad" (cifrar y tirar la llave); (2) preguntar si una pérdida de datos es sesgada (MCAR vs MAR/MNAR) antes de ignorarla; (3) saber qué dos problemas resuelve un feature store; y (4) enunciar los principios de entrenamiento confiable (fallback, rollback, versionado). Cada idea entra por un ejemplo.

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

## Mini-ejemplo trabajado: "ya quité el nombre, está anonimizado"

Un equipo publica un dataset "anónimo": borra nombres y emails, deja solo **género, fecha de nacimiento y código postal**. Parece seguro. Pero el estudio de **Sweeney** mostró que **el 87%** de la población de EE. UU. es identificable de forma única con *exactamente* esos tres campos. Cruzando con un padrón electoral público, reidentificas a la mayoría → no estaba anonimizado, estaba **pseudonimizado** (reversible con un dato extra), que debe tratarse como *tan arriesgado como el dato crudo*.

Por eso "más datos == mejor" es falso: cada dato es también un **pasivo** (legal, ético, de borrado). Y borrar de verdad es difícil (copias, backups, índices) → dos tácticas: reescritura periódica que omite lo borrado, o **cifrar todo y tirar la llave** (sin llave, el dato es ilegible en todos los backups).

**Predicción antes de seguir:** un apagón de pagos afecta *solo* al sitio en español. Pierdes esos datos de compra. ¿Ignorable? No: la pérdida es **sesgada** (MAR/MNAR, no MCAR). El modelo "aprende" que el español no compra, muestra menos resultados en español y **empeora las ventas aun después** del apagón. La pregunta de oro al perder datos: *¿la pérdida es sesgada?*

## Prototipo, contraejemplo y caso borde

- **Prototipo (confiabilidad asumida):** versionas configs, datos y snapshots porque *todo modelo se reentrenará*; tienes fallback + rollback.
- **Contraejemplo (fallback insuficiente):** el modelo supera tanto a la heurística que, cuando falla, el fallback ya no basta — la trampa de "un buen modelo se volverá malo".
- **Caso borde (entrenar demasiado rápido):** más learners distribuidos → race conditions que hacen **divergir** el modelo; hay que sincronizar el estado y limitar la tasa de actualización.

## Errores típicos

- **Conceptual:** creer que quitar el identificador directo anonimiza (los cuasi-identificadores reidentifican).
- **De datos:** tratar toda pérdida de datos como ignorable sin preguntar si es **sesgada** (MCAR vs MAR/MNAR).
- **De métrica:** confundir **utilización** (usado/pagado) con **eficiencia** (valor/coste) — GPU al 100% no significa producir valor.

## Transferencia isomorfa

- **MCAR/MAR/MNAR ↔ mecanismos de datos faltantes causales:** que la pérdida sea aleatoria o sesgada es el mismo marco que decide si ignorar o corregir datos faltantes en inferencia (conecta con [[arena-h19]], sesgo de selección).
- **Feature store ↔ paridad train/serving:** un lugar único y versionado para features ataca el training-serving skew (conecta con [[arena-rom3]]).
- **Cifrar y tirar la llave ↔ borrado criptográfico:** hacer un dato ilegible sin perseguir cada copia es privacidad por diseño (conecta con [[arena-h14]], estudios en red sin compartir datos).

Moraleja de la arista: *el dato es activo y pasivo; los cuasi-identificadores reidentifican (Sweeney 87%), la pérdida sesgada envenena el modelo, y "borrar" de verdad es cifrar y tirar la llave.*

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
