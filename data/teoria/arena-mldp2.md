# Ensembles, cascada, clase neutra y rebalanceo

## El error reducible: sesgo y varianza

El error de un modelo = **irreducible** (ruido del dato/encuadre, no reducible) + **sesgo** (no aprende la relación → underfit) + **varianza** (no generaliza → overfit). Sesgo y varianza son el **error reducible**; subir complejidad baja sesgo pero sube varianza.

## Ensembles — combinar modelos

- **Bagging** (bootstrap + promediar/votar; p.ej. random forest): ensemble **paralelo** que reduce **VARIANZA**. Funciona si los errores están poco correlacionados (cov≈0 → error baja hacia var/k). Clave: **diversidad**. Ayuda poco a modelos estables (lineal, kNN, naive Bayes).
- **Boosting** (secuencial, cada modelo corrige los **residuos** del anterior; AdaBoost, XGBoost): reduce **SESGO** construyendo un modelo de más capacidad enfocado en los casos difíciles.
- **Stacking**: un **meta-modelo** aprende a combinar las salidas de varios modelos base.
- Coste: más tiempo de diseño/entrenamiento y **menos interpretabilidad**. El **dropout** aproxima bagging (pero comparte parámetros).

| Problema | Ensemble |
|---|---|
| Alto sesgo (underfit) | Boosting |
| Alta varianza (overfit) | Bagging |

## Cascade — usual + raro

Cuando un problema mezcla actividad usual e inusual con comportamientos muy distintos, un solo modelo ignora lo raro. Divide en: (1) **clasificar la circunstancia**, (2) modelo para lo típico, (3) modelo para lo inusual, (4) modelo que **combina** las salidas. **Riesgo central:** en inferencia no hay etiquetas, se elige el modelo según la predicción del clasificador (que falla), así que 2 y 3 ven datos que no vieron en entrenamiento → diseño experimental cuidadoso (por eso no es solo un Ensemble).

## Neutral Class — el "Maybe"

En vez de binario Sí/No, entrena tres clases disjuntas: Sí, No y **Maybe** (neutra). Evita que el modelo malgaste esfuerzo en casos **arbitrarios/ambiguos**. Útil cuando los **expertos discrepan**, en satisfacción de cliente (1-4 malo / 5-7 neutro / 8-10 bueno), etc. **Requiere diseñar la recolección**: la clase neutra no se fabrica después.

## Rebalancing — datasets desbalanceados

- **El accuracy engaña:** con 5% de positivos, predecir siempre la mayoría da 95%. Usa **precision, recall, F-measure**; para todos los umbrales, **precision-recall promedio** > AUC. El **test set mantiene el desbalance** original.
- **Downsampling** (reducir la mayoritaria, a menudo + Ensemble), **class weighting** (más peso a la minoritaria), **upsampling** (duplicar/aumentar la minoritaria).
- **Reencuadre:** si la minoría es rarísima, trátalo como **detección de anomalías** o clustering.

---

## Mini-ejemplo trabajado: la paradoja del accuracy

Detector de fraude con **5%** de positivos. Entrenas un modelo y reporta **95% de accuracy**. ¿Celebrar? No: un modelo que predice **siempre "no fraude"** acierta el 95% sin detectar *ni un solo* fraude. El accuracy está secuestrado por la clase mayoritaria.

Mira precision y recall en su lugar. Si tu modelo marca 100 transacciones como fraude y 60 lo son (precision 0.60) pero hay 200 fraudes reales (recall 0.30), el F1 ≈ 0.40 — muy lejos del "95%". Y el **test set conserva el desbalance original** (no lo rebalancees, o medirás un mundo que no existe).

**Predicción antes de seguir:** ¿es éste el mismo fenómeno que el PPV de un fenotipo clínico raro? Sí: con una clase rara, una métrica "global" engaña; hay que mirar la tasa base (conecta con [[arena-h13]], donde sens 90% daba PPV 49%).

Para el sesgo-varianza: si subes la complejidad y el error de *entrenamiento* baja pero el de *validación* sube, estás cambiando sesgo por **varianza** (overfit) → toca **bagging**; si ambos errores son altos (underfit), es **sesgo** → **boosting**.

## Prototipo, contraejemplo y caso borde

- **Prototipo (bagging):** modelos con errores **poco correlacionados** (random forest) → el promedio baja la varianza hacia var/k.
- **Contraejemplo (bagging inútil):** baggear un modelo **estable** (lineal, kNN, naive Bayes) → casi no ayuda; necesitas diversidad.
- **Caso borde (cascade ≠ ensemble):** en inferencia no hay etiqueta, así que el modelo "típico" y el "raro" ven datos elegidos por un clasificador que **falla** → entrenarlos sobre predicciones exige diseño cuidadoso.

## Errores típicos

- **Conceptual:** confiar en el **accuracy** con clases desbalanceadas (paradoja del accuracy).
- **Técnico:** rebalancear el **test set** (debe conservar el desbalance real) o baggear modelos estables.
- **De diseño:** fabricar la **clase neutra** después de recolectar; el "Maybe" exige diseñar la recolección desde el inicio.

## Transferencia isomorfa

- **Paradoja del accuracy ↔ tasa base / PPV:** una clase rara vuelve engañosa la métrica global, igual que la prevalencia hunde el PPV de un test (conecta con [[arena-h13]] y [[arena-q2]]).
- **Bagging/boosting ↔ reducir varianza/sesgo:** la descomposición sesgo-varianza es el marco de [[arena-isl1]]; los ensembles son sus dos remedios.
- **Neutral class ↔ opción de abstención:** dejar que el modelo diga "no sé" en casos ambiguos es pariente de un umbral de confianza / rechazar la predicción.

Moraleja de la arista: *con clases desbalanceadas el accuracy miente (mira P/R/F1 y la tasa base); elige el ensemble por el error que ataca —bagging para varianza, boosting para sesgo.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Modelo subajusta | Boosting |
| Modelo sobreajusta | Bagging (miembros diversos) |
| Usual + raro con valores muy distintos | Cascade (clasificar + modelo por segmento + combinar) |
| Casos ambiguos / expertos discrepan | Neutral Class |
| Clase minoritaria muy escasa | Downsampling/weighting; métricas P/R/F1; o anomalías |

---

> **Síntesis:** Combina modelos según el error: **bagging** baja varianza (errores poco correlacionados), **boosting** baja sesgo (residuos), **stacking** aprende a combinar. Cuando hay casos **raros** con comportamiento distinto, usa una **Cascade** (cuidando que los modelos posteriores se entrenan sobre predicciones). Una **clase neutra** rescata los casos ambiguos. Y ante **desbalance**, no te fíes del accuracy: usa precision/recall/F1 y downsampling/weighting (o reencuadra como anomalía).

---

*Retrieval: (1) descompón el error y di qué ensemble ataca cada parte; (2) ¿por qué la Cascade no es solo un Ensemble?; (3) ¿cuándo una clase neutra?; (4) ¿por qué el accuracy engaña en desbalance y qué métricas usar?*
