# Aprendizaje estadístico I: el marco, sesgo-varianza y KNN

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
