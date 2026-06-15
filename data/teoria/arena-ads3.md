# Machine Learning para entrevistas de ciencia de datos

> La mayoría de los puestos de DS valoran **intuición de negocio + ML clásico** sobre deep learning. Tres tipos de pregunta: conceptual (¿qué es el trade-off sesgo-varianza?), de currículum (¿qué aplicaste?) y end-to-end (¿cómo modelarías X?).

## Trade-off sesgo–varianza

Modelamos $y=f(x)+w$ (ruido $w$). El error de predicción se descompone en:

1. **Sesgo (bias):** qué tan lejos caen las predicciones de la $f(x)$ real. Alto sesgo = modelo demasiado simple (**underfitting**).
2. **Varianza:** cuánto cambian las predicciones según los datos de entrenamiento. Alta varianza = modelo demasiado sensible al ruido (**overfitting**).
3. **Error irreducible:** ruido inherente de la observación.

- **Lineal/regresión simple:** alto sesgo, baja varianza.
- **Redes neuronales / árboles profundos:** bajo sesgo, alta varianza.

En la entrevista casi nunca piden la ecuación; piden **razonar**: si el modelo tiene alta varianza → consigue más datos o regulariza; si tiene alto sesgo → aumenta la complejidad. Navaja de Occam: el modelo más simple que cumple suele generalizar mejor.

## Overfitting y regularización

Overfitting = el modelo memoriza ruido del train y no generaliza. **Regularización** penaliza la complejidad para bajar varianza a costa de un poco de sesgo:

- **L2 (Ridge):** penaliza $\sum w_i^2$ → encoge los pesos hacia 0 sin anularlos.
- **L1 (Lasso):** penaliza $\sum |w_i|$ → lleva pesos exactamente a 0 → **selección de features** (modelos sparse). Encogimiento más estricto.
- **Elastic net:** combina L1 y L2.

Otras defensas contra overfitting: más datos, cross-validation, early stopping, dropout (redes), poda (árboles).

## Validación y selección de modelo

Separar **train / validación / test**. **Cross-validation** (k-fold): rota qué partición es validación para estimar el desempeño fuera de muestra de forma robusta. El test set se toca **una sola vez**, al final.

## Métricas de clasificación

Con la matriz de confusión (TP, FP, TN, FN):

- **Accuracy** = (TP+TN)/total. **Engaña con clases desbalanceadas** (99% sanos → predecir "sano" siempre da 99%).
- **Precisión** = TP/(TP+FP): de los que marqué positivos, ¿cuántos lo eran?
- **Recall (sensibilidad)** = TP/(TP+FN): de los positivos reales, ¿cuántos atrapé?
- **F1** = media armónica $2\cdot\dfrac{P\cdot R}{P+R}$: equilibra ambas.
- **ROC / AUC:** TPR vs FPR a distintos umbrales; AUC = prob. de rankear un positivo por encima de un negativo.

**Trade-off precisión–recall:** subir recall (atrapar todos los cánceres) cuesta más falsas alarmas; subir precisión cuesta dejar casos sin detectar. Elige según el costo de un FP vs un FN.

## Algoritmos clásicos

- **Regresión lineal:** supervisado, etiquetas continuas; alto sesgo, interpretable.
- **Regresión logística:** clasificación; salida lineal pasada por sigmoide → probabilidad; pérdida **log-loss**. Falla con fronteras no lineales.
- **Naive Bayes:** asume independencia condicional de features dado la clase → evita los $2^k$ parámetros; rápido, fuerte baseline en texto.
- **SVM:** maximiza el margen; con kernels logra fronteras no lineales.
- **Árboles de decisión:** interpretables pero propensos a overfit.
- **Ensembles** (bootstrapping/bagging): promedian muchos modelos para bajar varianza.
  - **Random Forest:** bagging de árboles con sub-muestreo de features; robusto, poco preprocesamiento.
  - **Boosting (AdaBoost/XGBoost):** modelos secuenciales que corrigen los errores del anterior; baja sesgo.

## No supervisado y reducción de dimensión

- **K-means / clustering:** halla grupos ocultos (segmentar clientes). Hay que elegir k.
- **PCA:** proyecta a las direcciones de **máxima varianza** (eigenvectores de la matriz de covarianza). Reduce dimensión conservando señal. Pitfall: sensible a la escala (estandariza antes) y los componentes pierden interpretabilidad.

## Optimización: descenso de gradiente

Minimiza la función de pérdida moviéndose en la dirección de máximo descenso: $x_{t+1}=x_t-\alpha\,\nabla f(x_t)$, con **learning rate** $\alpha$. Convexa → óptimo global; no convexa → puede quedar en mínimos locales. **SGD** usa mini-lotes para escalar.

---

## Mini-ejemplo trabajado: precisión vs recall con una matriz de confusión

Detector de cáncer sobre 1000 pacientes, 50 enfermos. El modelo marca 60 positivos: 45 son cáncer real (TP), 15 son falsas alarmas (FP); deja 5 cánceres sin detectar (FN).

- **Precisión** = TP/(TP+FP) = 45/60 = **75%** (de mis alarmas, cuántas aciertan).
- **Recall** = TP/(TP+FN) = 45/50 = **90%** (de los cánceres, cuántos atrapo).
- **Accuracy** = (45+935)/1000 = 98% — alta, pero engaña: predecir "sano" siempre daría 95%.

**Predicción antes de seguir:** si bajas el umbral para atrapar los 5 cánceres que se escapan (recall→100%), ¿qué le pasa a la precisión? Respuesta: **baja** — atraparás más cánceres a costa de más falsas alarmas, así que FP sube y la precisión cae. Precisión y recall están en tensión; el umbral los intercambia, y eliges según cueste más un FP (alarma innecesaria) o un FN (cáncer perdido). En cáncer, priorizas recall.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** clases desbalanceadas → razona con precisión/recall/F1/AUC, nunca accuracy.
- **Contraejemplo (alta varianza disfrazada de éxito):** train accuracy 100% es overfitting, no maestría; el test lo desmiente. El error de train siempre baja con la complejidad.
- **Caso borde (PCA y escala):** PCA sin estandarizar deja que la feature con unidades grandes (ingresos en pesos) domine las componentes; el borde obliga a estandarizar antes.

## Errores típicos

- **Conceptual:** atacar alta varianza con más complejidad (empeora) o alto sesgo con más datos (no ayuda); el remedio depende de cuál domina.
- **Técnico:** tocar el test set más de una vez (lo conviertes en validación y sobreajustas a él).
- **De interpretación:** reportar accuracy en problemas desbalanceados.

## Transferencia isomorfa

- **Sesgo-varianza ↔ MSE = Var + Bias²:** el eje central del ML es la descomposición de teoría de estimación; alta varianza pide regularizar (conecta con [[arena-dg1]] y [[arena-isl1]]).
- **L1/L2 ↔ shrinkage de James-Stein y priors:** lasso/ridge encogen los pesos, cambiando sesgo por varianza, exactamente como Stein (conecta con [[arena-dg4]]).
- **Precisión ↔ VPP y tasa base:** la precisión *es* el valor predictivo positivo; con clase rara, AUC alta no garantiza precisión (conecta con [[arena-q2]]).
- **Bagging / Random Forest ↔ bootstrap y decorrelación:** promediar modelos sobre muestras con reemplazo baja varianza (conecta con [[arena-pst2]] e [[arena-isl4]]).
- **PCA ↔ covarianza PSD:** las componentes son los ejes de la matriz de covarianza, semidefinida positiva (conecta con [[arena-q9]]).

Moraleja de la arista: *accuracy engaña con clases raras; razona con precisión (=VPP) y recall, que el umbral intercambia según el costo de FP vs FN.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "El modelo va perfecto en train y mal en test" | Overfitting (alta varianza) → regulariza / más datos |
| "Predicciones siempre lejos, modelo simple" | Alto sesgo → más complejidad |
| "Quiero selección de features automática" | L1 (Lasso) → pesos a 0 |
| "Clases desbalanceadas, accuracy 99%" | Usa precisión/recall/F1, no accuracy |
| "Cuesta más un falso negativo (cáncer)" | Optimiza recall; ROC/AUC para umbral |
| "Estima desempeño fuera de muestra" | k-fold cross-validation; test una sola vez |
| "Bajar varianza promediando modelos" | Bagging / Random Forest |
| "Reducir dimensión conservando señal" | PCA (eigenvectores de la covarianza) |

---

> **Síntesis:** El ML de entrevista se sostiene en un eje central —sesgo vs varianza— del que cuelgan overfitting, regularización (L1 sparse / L2 shrink) y cross-validation. Para clasificación, accuracy engaña: razona con precisión, recall, F1 y ROC según el costo de FP vs FN. Conoce a fondo un puñado de algoritmos clásicos (logística, árboles, random forest, PCA) y el descenso de gradiente como motor de optimización. Más vale dominar una técnica que recitar diez.

---

*Retrieval: cierra y responde: (1) describe el trade-off sesgo-varianza y qué hacer ante alta varianza; (2) diferencia L1 de L2 y cuál da sparsity; (3) define precisión y recall y cuándo priorizar cada una; (4) ¿qué maximiza PCA y por qué estandarizar antes?*
