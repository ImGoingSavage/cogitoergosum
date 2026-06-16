# Cambios de distribución, monitoreo y test en producción

## De qué trata esta lección (y qué sabrás hacer al final)

Todo modelo en producción **se pudre**: el mundo cambia y los datos dejan de parecerse a los de entrenamiento. Esta lección construye, desde cero, cómo nombrar ese deterioro con precisión —descomponiendo $P(X,Y)$ en sus piezas para distinguir **covariate shift**, **label shift** y el temido **concept drift**—, cómo detectarlo (two-sample tests) y cómo validar un modelo nuevo en producción sin arriesgar usuarios (shadow, A/B, canary, bandits).

Al terminar podrás: (1) clasificar un shift por su probabilidad (¿cambió $P(X)$, $P(Y)$ o $P(Y\mid X)$?) y saber cuál solo se cura reentrenando; (2) detectar un shift con un two-sample test (KS/MMD), la misma maquinaria del A/B vista al revés; (3) explicar por qué el shadow deployment es el test más seguro; y (4) distinguir canary de bandits. El ejemplo de scoring crediticio nombra cada shift. Profundiza el skew/drift de [[arena-rml3]].

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

## Mini-ejemplo trabajado: nombrar el shift por su probabilidad

Un modelo de aprobación de crédito se degrada. Descompón P(X,Y) = P(Y|X)·P(X) para diagnosticar *qué* cambió:

- Llega una oleada de solicitantes **más jóvenes** (cambia P(X)), pero "a igual perfil, el riesgo es el mismo" → **covariate shift**: P(X) cambia, P(Y|X) intacto. Re-pesar por densidad suele bastar.
- Tras una crisis, **más gente** entra en default (cambia P(Y)), pero "dado que alguien hace default, sus features se ven igual" → **label shift**.
- Tras una nueva ley, el **mismo perfil** que antes era "riesgoso" ahora es "seguro" (cambia P(Y|X), la *relación* misma) → **concept drift**, el más peligroso, porque ni re-pesar lo arregla: hay que reentrenar con la nueva realidad.

**Predicción antes de seguir:** quieres detectar que la distribución de producción se movió. ¿Qué herramienta? Un **two-sample test** (Kolmogorov-Smirnov, MMD) contra una referencia — *la misma maquinaria del A/B testing*, vista desde el otro lado. Y para probar un modelo nuevo sin riesgo: **shadow deployment** (recibe el mismo tráfico, predice en paralelo, **no se sirve**), luego A/B aleatorio o canary.

## Prototipo, contraejemplo y caso borde

- **Prototipo (shadow → canary):** shadow valida sin servir, luego canary sube el % gradualmente con rollback si las métricas caen.
- **Contraejemplo (A/B sin aleatoriedad real):** enrutar al candidato por un criterio sesgado (p. ej. usuarios nuevos) → sesgo de selección que invalida el test.
- **Caso borde (concept drift):** re-pesar por densidad arregla covariate shift pero **no** el concept drift; ahí solo sirve reentrenar.

## Errores típicos

- **Conceptual:** llamar "concept drift" a todo shift; distingue P(X) (covariate), P(Y) (label) y P(Y|X) (concept).
- **De validación:** confiar solo en eval offline; hay que **test en producción** (shadow/A-B/canary).
- **De significancia:** olvidar que un p=0.05 falla el 5% de las veces, y que el tamaño de muestra importa.

## Transferencia isomorfa

- **Two-sample test de shift ↔ A/B testing:** detectar que dos distribuciones difieren es la misma maquinaria estadística vista desde el otro lado (conecta con [[arena-ads4]] y [[arena-pst3]], tests de permutación).
- **Concept drift ↔ prediction bias / umbral caducado:** que la relación input→output mute es lo que el prediction bias detecta y lo que invalida un umbral fijo (conecta con [[arena-htd4]]).
- **Covariate shift ↔ falta de overlap / independencia del PDP:** evaluar donde P(X) cambió es pedirle al modelo que prediga fuera de su soporte, como el PDP bajo correlación o la positividad causal (conecta con [[arena-iml3]] y [[arena-h3]]).

Moraleja de la arista: *nombra el shift por su probabilidad (P(X)/P(Y)/P(Y|X)), detéctalo con two-sample tests, y valida en producción con shadow→canary; el concept drift solo se cura reentrenando.*

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
