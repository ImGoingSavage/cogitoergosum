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
