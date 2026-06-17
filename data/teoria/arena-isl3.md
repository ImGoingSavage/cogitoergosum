# Aprendizaje estadístico III: remuestreo, selección y regularización

## De qué trata esta lección (y qué sabrás hacer al final)

Dos preguntas dominan la práctica del ML: **¿qué tan bien predigo fuera de muestra?** y **¿qué predictores conservo?** Esta lección construye, desde cero, las herramientas que las responden: el **remuestreo** (validación cruzada para estimar el error de test, bootstrap para la incertidumbre), la **selección de subconjuntos** y la **regularización** (ridge y lasso), con su distinción geométrica clave —por qué el lasso anula coeficientes y el ridge solo los encoge—.

Al terminar podrás: (1) elegir k-fold sobre LOOCV sabiendo por qué; (2) distinguir lo que estima el CV (error de test) de lo que estima el bootstrap (incertidumbre); (3) decidir entre ridge y lasso según cuántos predictores importen; y (4) reconocer la maldición de la dimensionalidad cuando $p\gtrsim n$. La intuición primero, incluida la del rombo L1 que produce sparsity.

## ¿Por qué remuestrear?

El **error de entrenamiento subestima** el de test (baja al añadir flexibilidad aunque haya overfit). Reutilizamos los datos ajustando muchas veces para **estimar el error de test** (CV) o **cuantificar incertidumbre** (bootstrap).

## Validación cruzada

- **Validation set** (una partición): simple, pero estimación **variable** y **sesgada al alza** (entrena con menos datos).
- **LOOCV** (k=n): deja una fuera, repite n veces. **Sin sesgo** y determinista, pero **caro** y de **alta varianza** (los n modelos están muy correlacionados → promediar reduce poco). En mínimos cuadrados hay fórmula con leverages (1 ajuste).
- **k-fold** (k=5/10): k grupos; cada uno valida una vez. Algo más de sesgo pero **menos varianza** y barato → **punto dulce** del trade-off sesgo-varianza del propio CV.
- En clasificación se promedia la **tasa de error**. Para elegir modelo: **regla de un error estándar** (el más simple dentro de 1 SE del mínimo).

## Bootstrap

Remuestrea **con reemplazo** (mismo n, con repeticiones/omisiones); calcula el estimador en cada réplica → su distribución empírica da el **error estándar / IC** sin fórmula teórica. Estima **incertidumbre**, no error de test. Ver bootstrap-resampling.

## Selección de subconjuntos

- **Best subset:** los 2^p modelos (inviable si p>~40).
- **Forward** (añade el mejor de a uno; sirve si p>n) / **backward** (quita el peor; requiere n>p). Greedy, baratos, sin óptimo garantizado.
- **Tamaño del modelo:** el RSS/R² de train siempre mejora → usa **Cp, AIC, BIC** (BIC penaliza más, log n → modelos más pequeños), **R² ajustado** o **CV** (preferido).

## Regularización (shrinkage)

- **Ridge:** RSS + λΣβⱼ² (L2). Encoge hacia 0 **sin anular** (no selecciona); baja varianza. Ver regularizacion.
- **Lasso:** RSS + λΣ|βⱼ| (L1). La geometría con **esquinas** pone coeficientes **exactamente en 0** ⇒ **selección de variables**, modelo disperso e interpretable.
- **Cuándo:** lasso si **pocos** predictores relevantes; ridge si **muchos** efectos pequeños. λ por **CV**; **estandarizar** siempre (la penalización depende de la escala).

## Reducción de dimensión y alta dimensión

- **PCR:** regresa sobre M componentes de **máxima varianza de X** (PCA, **no supervisado**: ignora Y). **PLS:** componentes que explican X **y** se correlacionan con Y (**supervisado**). Ambos: estandarizar, elegir M por CV.
- **Maldición de la dimensionalidad** (p≳n): mínimos cuadrados se rompen (overfit perfecto), Cp/AIC/BIC/R² dejan de ser fiables, features ruidosas empeoran. Usa selección/regularización/reducción de dimensión y **no afirmes** haber hallado el conjunto 'verdadero'.

---

## Mini-ejemplo trabajado: por qué la geometría del lasso anula coeficientes

Dos coeficientes (β₁,β₂). Minimizas RSS sujeto a un presupuesto de penalización. Las curvas de nivel del RSS son **elipses**; la región factible es:
- **Ridge (L2):** un **círculo** β₁²+β₂² ≤ t — borde liso. La elipse toca el círculo casi siempre en un punto con *ambos* coeficientes ≠ 0: encoge pero no anula.
- **Lasso (L1):** un **rombo** |β₁|+|β₂| ≤ t — con **esquinas** sobre los ejes. La elipse tiende a tocar el rombo en una **esquina**, donde un coeficiente es exactamente 0: selecciona variables.

La sparsity del lasso no es un truco numérico: nace de que las esquinas del rombo viven sobre los ejes.

**Predicción antes de seguir:** si tienes muchos predictores con efectos pequeños y parecidos, ¿ridge o lasso? Respuesta: **ridge** — reparte el encogimiento entre todos y conserva la señal difusa; el lasso, forzado a elegir esquinas, descartaría arbitrariamente unos y quedaría inestable. Lasso brilla cuando *pocos* predictores importan de verdad.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** estimar error de test → k-fold (5/10), el punto dulce entre sesgo y varianza del propio CV.
- **Contraejemplo (LOOCV no es "lo mejor"):** LOOCV no tiene sesgo pero sus n modelos están casi idénticos → promediar reduce poco la varianza, y es caro. k=5/10 suele ganar.
- **Caso borde (p ≳ n):** mínimos cuadrados sobreajustan perfecto (train error 0), y Cp/AIC/BIC/R² dejan de ser fiables; hay que regularizar y no afirmar haber hallado el conjunto "verdadero".

## Errores típicos

- **Conceptual:** confundir lo que estima el CV (error de test) con lo que estima el bootstrap (incertidumbre/SE de un estimador).
- **Técnico:** no estandarizar antes de ridge/lasso (la penalización depende de la escala de cada feature).
- **De supuestos:** elegir λ o el tamaño del modelo mirando el error de entrenamiento en vez de CV.

## Transferencia isomorfa

- **Validación cruzada / holdout ↔ control de multiplicidad:** evaluar fuera de muestra es el antídoto del DS contra "probar mucho hasta que algo salga" (conecta con [[arena-pst3]]).
- **Bootstrap ↔ remuestreo con reemplazo:** misma maquinaria para SE/IC sin fórmula que en estadística aplicada (conecta con [[arena-pst2]]).
- **Ridge / lasso ↔ shrinkage de James-Stein y priors:** encoger hacia 0 cambia sesgo por varianza, exactamente como Stein y un prior bayesiano (conecta con [[arena-dg4]]).
- **Cp/AIC/BIC ↔ LRT y selección por verosimilitud:** penalizar complejidad para predecir bien es la misma lógica que comparar modelos por razón de verosimilitudes (conecta con [[arena-dg2]]).

Moraleja de la arista: *el error de train engaña; estima el de test con k-fold; y la esquina del rombo L1 es la razón geométrica de que el lasso seleccione donde el ridge solo encoge.*

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
