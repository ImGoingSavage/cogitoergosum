# Cambios de distribución, monitoreo y test en producción

## El modelo se pudre: data distribution shifts

Un modelo desplegado **degrada** porque el mundo cambia y los datos de producción dejan de parecerse a los de entrenamiento. Partiendo de P(X, Y) = P(Y|X)·P(X) = P(X|Y)·P(Y), hay tres subtipos distintos:

- **Covariate shift:** cambia **P(X)** pero **P(Y|X)** se mantiene. Cambia la distribución de los inputs, no la relación input→output (llegan más usuarios jóvenes, pero la relación edad→compra es la misma). Causa típica: sesgo de selección en el entrenamiento.
- **Label shift:** cambia **P(Y)** pero **P(X|Y)** se mantiene. Cambia la distribución de las salidas (más casos positivos), pero dado el label, los features se ven igual.
- **Concept drift** (a veces "posterior shift"): cambia **P(Y|X)** — la **relación** input→output muta. El mismo input ahora tiene otra respuesta (un precio que antes era "caro" hoy es "normal"). Es el más peligroso.

## Detección y monitoreo

- **Detección estadística:** comparar la distribución de producción contra una de referencia con **two-sample tests** (Kolmogorov-Smirnov, MMD). Un resultado significativo sugiere que la distribución se movió. (Es la misma maquinaria del A/B testing, vista desde el otro lado.)
- **Qué monitorear:** **métricas operacionales** (latencia, throughput, uptime) y **métricas de ML** (accuracy si hay labels; si no, proxies: distribución de predicciones, de features, de inputs crudos).
- **Observability:** no basta con saber **que** algo falla; el sistema debe dar visibilidad para entender **por qué** (logs, traces, slicing por segmento).

## Aprendizaje continuo (continual learning)

- **Stateless retraining:** reentrenar desde cero cada vez (lo más común, simple pero caro).
- **Stateful / incremental:** continuar el entrenamiento desde el checkpoint anterior con datos nuevos; más barato y rápido de actualizar.
- La pregunta clave no es "¿con qué frecuencia reentreno?" sino **cuánto valor** aporta actualizar (value of data freshness) frente a su coste y riesgo.

## Test en producción

Evaluar offline no basta: hay que probar con tráfico real, minimizando riesgo.

- **Shadow deployment** (lo más seguro): el modelo candidato recibe el **mismo tráfico** que el actual y predice **en paralelo**, pero sus predicciones **no se sirven**; solo se registran y comparan. Coste: doblas el cómputo.
- **A/B testing:** enruta un % del tráfico al candidato y el resto al actual, **al azar** (la aleatoriedad real es crítica: un sesgo de selección invalida el test), y compara con **tests de significancia** (two-sample). Cuida el tamaño de muestra y recuerda que la significancia no es infalible (un p=0.05 falla 5% de las veces).
- **Canary release:** despliega el candidato a un **subconjunto pequeño** de usuarios y ve **subiendo** el porcentaje si las métricas aguantan; si empeoran, *rollback*.
- **Interleaving:** mezcla resultados de ambos modelos en **una misma** lista y mira de cuál el usuario elige más (común en ranking/recsys).
- **Bandits:** enrutamiento **adaptativo** que asigna más tráfico al modelo que va ganando (explora/explota); más eficiente en datos que el A/B clásico, pero más complejo de implementar. Los **contextual bandits** consideran además el contexto de cada decisión.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Cambió la distribución de inputs, no la relación" | Covariate shift (P(X) cambia, P(Y\|X) igual) |
| "El mismo input ahora da otra respuesta" | Concept drift (P(Y\|X) cambia) — el más peligroso |
| "¿Se movió la distribución de producción?" | Two-sample test (KS/MMD) contra referencia |
| "Probar un modelo nuevo sin arriesgar usuarios" | Shadow deployment (predice en paralelo, no sirve) |
| "¿Cuál de dos modelos es mejor con tráfico real?" | A/B testing aleatorio + significancia |
| "Subir el nuevo modelo gradualmente con rollback" | Canary release |
| "Repartir tráfico hacia el que va ganando" | Bandits (explora/explota; contextual si hay contexto) |

---

> **Síntesis:** Todo modelo se degrada por **data distribution shift**: **covariate** (cambia P(X)), **label** (cambia P(Y)) o el temido **concept drift** (cambia P(Y|X), la relación misma). Se detecta con **two-sample tests** y se vigila monitoreando métricas operacionales y de ML (con proxies si faltan labels). Se corrige con **continual learning** (stateless vs stateful), decidido por el valor de la frescura. Y se valida con **test en producción**: shadow (paralelo, sin servir), **A/B** aleatorio, **canary** gradual, interleaving y **bandits** adaptativos.

---

*Retrieval: cierra y responde: (1) define covariate, label y concept shift por su probabilidad; (2) ¿cómo se detecta un shift?; (3) ¿qué es shadow deployment y por qué es seguro?; (4) diferencia canary de bandits.*
