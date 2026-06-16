# Aprendizaje estadístico I: el marco, sesgo-varianza y KNN

## De qué trata esta lección (y qué sabrás hacer al final)

Todo el machine learning supervisado cabe en una ecuación: $Y=f(X)+\varepsilon$. Aprender es estimar esa $f$ a partir de datos. Esta lección construye, desde cero, el marco mental que organiza el resto del cluster: por qué estimamos $f$ (predecir vs inferir), por qué siempre hay un error que **ningún** modelo puede vencer, y por qué la flexibilidad es un arma de doble filo —el **trade-off sesgo-varianza**, que aquí cobra su forma definitiva con la curva en U del error de test.

Al terminar podrás: (1) distinguir error reducible de irreducible; (2) escribir y leer la descomposición sesgo-varianza; (3) entender por qué un error de entrenamiento de 0 suele ser mala señal; y (4) usar el clasificador de Bayes como techo y KNN como su aproximación, con $K$ de perilla. Cada idea entra por su intuición. Es el cimiento de [[arena-ads3]] y de los tres ISL siguientes.

## ¿Qué es estimar f?

Asumimos **Y = f(X) + ε**: f es la información SISTEMÁTICA que X aporta sobre Y, y ε un error aleatorio independiente de X con media 0. El aprendizaje estadístico estima **f̂** por dos motivos:
- **Predicción:** solo importa ŷ = f̂(X); f̂ puede ser caja negra.
- **Inferencia:** entender CÓMO afecta cada feature a Y (signo, magnitud, forma); f̂ debe ser interpretable.

El error se descompone en **reducible** (mejora con un mejor f̂) e **irreducible** = **Var(ε)** (ruido, variables no medidas): cota inferior que ningún modelo supera.

## Paramétrico vs no paramétrico y el trade-off

- **Paramétrico:** asume una forma para f (lineal) → pocos parámetros, simple, interpretable, pero arriesga mal ajuste si la forma es errónea.
- **No paramétrico:** no asume forma, sigue los datos (KNN, splines, árboles) → muy flexible pero necesita muchos datos, menos interpretable, propenso a overfit.

**Trade-off flexibilidad/precisión ↔ interpretabilidad:** más flexible puede predecir mejor pero es caja negra. Para **inferencia** o con pocos datos se prefiere lo restrictivo.

**Supervisado** (hay Y) vs **no supervisado** (no hay Y: clustering, PCA). **Regresión** (Y cuantitativa) vs **clasificación** (Y cualitativa) — lo decide el tipo de la RESPUESTA.

## Medir la calidad del ajuste

El **MSE de entrenamiento** siempre baja al aumentar la flexibilidad (puede memorizar ruido → overfit), así que lo que importa es el **MSE de TEST**, que sigue una **curva en U**: baja, mínimo, y vuelve a subir.

### Descomposición sesgo-varianza
$$E[(y_0 - \hat f(x_0))^2] = \mathrm{Var}(\hat f(x_0)) + [\mathrm{Bias}(\hat f(x_0))]^2 + \mathrm{Var}(\varepsilon)$$
- **Sesgo:** error por aproximar lo real con un modelo más simple.
- **Varianza:** cuánto cambiaría f̂ con otro dataset.
- Al subir la flexibilidad: **sesgo↓, varianza↑**. El óptimo minimiza la suma; **Var(ε)** es el piso.

## Clasificación: Bayes y KNN

- Calidad = **tasa de error** (fracción mal clasificada); importa la de TEST.
- **Clasificador de Bayes:** asigna a la clase más probable, argmax_j P(Y=j|X). Es óptimo; su error, la **tasa de error de Bayes** = 1 − E[máx_j P(Y=j|X)], es el análogo al irreducible. No realizable (no conocemos P(Y|X)).
- **KNN** lo aproxima: voto mayoritario de los K vecinos. **K controla la flexibilidad:** K=1 → frontera irregular, bajo sesgo, **alta varianza**; K grande → frontera suave, **alto sesgo**, baja varianza. K óptimo por CV.

---

## Mini-ejemplo trabajado: KNN con K=1 vs K=n y la U del MSE

Datos en una recta ruidosa Y=f(X)+ε. Ajusta KNN:
- **K=1:** cada predicción copia al vecino más cercano. El MSE de **entrenamiento es 0** (cada punto se predice a sí mismo), pero la frontera es dentada y cambia por completo con otro dataset → **varianza altísima, sesgo casi nulo**.
- **K=n:** cada predicción es la media global, ignorando X. Estable entre datasets (**varianza baja**) pero ciega a la señal → **sesgo alto**.

El MSE de **test** dibuja una **U**: baja al pasar de K=n hacia K moderado (cae el sesgo), toca un mínimo, y vuelve a subir hacia K=1 (explota la varianza). El óptimo está en medio, no en los extremos.

**Predicción antes de seguir:** un modelo con MSE de entrenamiento 0, ¿es el mejor? Respuesta: **casi nunca** — K=1 logra train=0 y es de los peores en test. El error de entrenamiento siempre baja con la flexibilidad, así que premiar "ajuste perfecto" selecciona overfit. Solo el error de *test* (o CV) tiene forma de U y revela el óptimo.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** elegir flexibilidad → minimiza el MSE de test (la U), equilibrando Var↑ contra Bias↓.
- **Contraejemplo (train engaña):** train MSE monótono decreciente sugiere "más flexible siempre mejor"; es falso, ignora la varianza fuera de muestra.
- **Caso borde (error de Bayes):** ni el clasificador perfecto baja de la tasa de error de Bayes = 1−E[máx P(Y=j|X)]; es el piso irreducible. El borde recuerda que parte del error no es culpa del modelo.

## Errores típicos

- **Conceptual:** confundir error reducible (mejora con mejor f̂) con irreducible Var(ε) (ruido y variables no medidas).
- **Técnico:** seleccionar el modelo por error de entrenamiento en vez de CV/test.
- **De interpretación:** perseguir flexibilidad cuando el objetivo es inferencia (entender el efecto de cada feature pide un modelo legible).

## Transferencia isomorfa

- **Sesgo-varianza ↔ MSE = Var + Bias²:** la descomposición de ISL es idéntica a la de teoría de estimación; un estimador sesgado de menor varianza puede ganar (conecta con [[arena-dg1]]).
- **Error irreducible Var(ε) ↔ ley de varianza total:** el piso de error es la varianza que X no explica, el término E[Var(Y|X)] (conecta con [[arena-b2]]).
- **Clasificador de Bayes ↔ regla óptima de Neyman-Pearson:** asignar a argmax P(Y|X) es la decisión que minimiza el error, primo del test más potente (conecta con [[arena-cb3]]).
- **KNN en alta dimensión ↔ maldición de la dimensionalidad:** "vecinos cercanos" deja de tener sentido cuando p≳n (conecta con [[arena-isl3]]).

Moraleja de la arista: *la flexibilidad baja el sesgo y sube la varianza; el mínimo de la U vive en medio, y el error de entrenamiento nunca te lleva ahí.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| ¿Caja negra o modelo legible? | Predicción → flexible; inferencia → restrictivo/interpretable |
| El error de train es casi 0 | Mira el TEST: probable overfit (U del MSE) |
| ¿Subir la flexibilidad mejora? | Solo hasta el mínimo de la U (sesgo↓ vs varianza↑) |
| ¿Cuál es el mejor error posible? | La tasa de error de Bayes (irreducible) |
| KNN se comporta raro | Ajusta K: pequeño = alta varianza, grande = alto sesgo |

---

> **Síntesis:** Y=f(X)+ε; estimamos f̂ para **predecir** (caja negra) o **inferir** (interpretable). El error es **reducible + irreducible (Var ε)**. Más flexibilidad baja el sesgo y sube la varianza (MSE de test en **U**), con un trade-off frente a la interpretabilidad. En clasificación, el **clasificador de Bayes** marca el techo y **KNN** lo aproxima, con K como perilla de flexibilidad.

---

*Retrieval: (1) ¿predicción vs inferencia?; (2) escribe la descomposición sesgo-varianza; (3) ¿qué es el error irreducible/error de Bayes?; (4) ¿cómo afecta K al sesgo y la varianza de KNN?*
