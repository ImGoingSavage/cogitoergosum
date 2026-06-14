# Aprendizaje estadístico III: remuestreo, selección y regularización

## ¿Por qué remuestrear?

El **error de entrenamiento subestima** el de test (baja al añadir flexibilidad aunque haya overfit). Reutilizamos los datos ajustando muchas veces para **estimar el error de test** (CV) o **cuantificar incertidumbre** (bootstrap).

## Validación cruzada

- **Validation set** (una partición): simple, pero estimación **variable** y **sesgada al alza** (entrena con menos datos).
- **LOOCV** (k=n): deja una fuera, repite n veces. **Sin sesgo** y determinista, pero **caro** y de **alta varianza** (los n modelos están muy correlacionados → promediar reduce poco). En mínimos cuadrados hay fórmula con leverages (1 ajuste).
- **k-fold** (k=5/10): k grupos; cada uno valida una vez. Algo más de sesgo pero **menos varianza** y barato → **punto dulce** del trade-off sesgo-varianza del propio CV.
- En clasificación se promedia la **tasa de error**. Para elegir modelo: **regla de un error estándar** (el más simple dentro de 1 SE del mínimo).

## Bootstrap

Remuestrea **con reemplazo** (mismo n, con repeticiones/omisiones); calcula el estimador en cada réplica → su distribución empírica da el **error estándar / IC** sin fórmula teórica. Estima **incertidumbre**, no error de test. Ver [[bootstrap-resampling]].

## Selección de subconjuntos

- **Best subset:** los 2^p modelos (inviable si p>~40).
- **Forward** (añade el mejor de a uno; sirve si p>n) / **backward** (quita el peor; requiere n>p). Greedy, baratos, sin óptimo garantizado.
- **Tamaño del modelo:** el RSS/R² de train siempre mejora → usa **Cp, AIC, BIC** (BIC penaliza más, log n → modelos más pequeños), **R² ajustado** o **CV** (preferido).

## Regularización (shrinkage)

- **Ridge:** RSS + λΣβⱼ² (L2). Encoge hacia 0 **sin anular** (no selecciona); baja varianza. Ver [[regularizacion]].
- **Lasso:** RSS + λΣ|βⱼ| (L1). La geometría con **esquinas** pone coeficientes **exactamente en 0** ⇒ **selección de variables**, modelo disperso e interpretable.
- **Cuándo:** lasso si **pocos** predictores relevantes; ridge si **muchos** efectos pequeños. λ por **CV**; **estandarizar** siempre (la penalización depende de la escala).

## Reducción de dimensión y alta dimensión

- **PCR:** regresa sobre M componentes de **máxima varianza de X** (PCA, **no supervisado**: ignora Y). **PLS:** componentes que explican X **y** se correlacionan con Y (**supervisado**). Ambos: estandarizar, elegir M por CV.
- **Maldición de la dimensionalidad** (p≳n): mínimos cuadrados se rompen (overfit perfecto), Cp/AIC/BIC/R² dejan de ser fiables, features ruidosas empeoran. Usa selección/regularización/reducción de dimensión y **no afirmes** haber hallado el conjunto 'verdadero'.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Estimar el error de test | k-fold (k=5/10), no el error de train |
| LOOCV vs k-fold | LOOCV sin sesgo pero alta varianza/caro; k=5/10 mejor |
| SE de un estimador sin fórmula | Bootstrap |
| Elegir nº de predictores | Cp/AIC/BIC/adjR²/CV (BIC = más estricto) |
| Overfit / colinealidad / p grande | Ridge o lasso (lasso si pocos relevantes); λ por CV |
| p ≳ n | Selección / regularización / PCR-PLS; interpreta con cautela |

---

> **Síntesis:** el error de train engaña; estima el de test con **k-fold (5/10)** (mejor equilibrio que LOOCV) y cuantifica incertidumbre con **bootstrap**. Elige predictores con stepwise + **Cp/AIC/BIC/CV**, y combate el overfit con **ridge** (encoge) o **lasso** (encoge y **selecciona**), λ por CV y estandarizando. En **alta dimensión** reduce la flexibilidad efectiva.

---

*Retrieval: (1) ¿por qué k=5/10 vence a LOOCV?; (2) ¿qué estima el bootstrap?; (3) ¿por qué el lasso anula coeficientes y ridge no?; (4) ¿qué pasa cuando p≳n?*
