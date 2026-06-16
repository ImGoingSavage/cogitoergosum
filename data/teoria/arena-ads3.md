# Machine Learning para entrevistas de ciencia de datos

## De qué trata esta lección (y qué sabrás hacer al final)

La mayoría de los puestos de DS valoran **intuición + ML clásico** por encima del deep learning, y casi todas las preguntas caen en tres moldes: conceptual ("¿qué es el trade-off sesgo-varianza?"), de currículum ("¿qué aplicaste?") y end-to-end ("¿cómo modelarías X?"). Esta lección construye, desde cero, el eje del que cuelga todo —**sesgo vs varianza**— y de ahí deriva overfitting, regularización, validación, métricas de clasificación, los algoritmos clásicos que debes conocer y el descenso de gradiente que los entrena.

Al terminar podrás: (1) diagnosticar si un modelo sufre alto sesgo o alta varianza y qué hacer en cada caso; (2) explicar L1 vs L2 y por qué L1 da sparsity; (3) elegir la métrica correcta para clases desbalanceadas sin caer en la trampa del accuracy; y (4) razonar el trade-off precisión-recall según el costo de un falso positivo vs uno falso negativo. La regla de fondo: más vale dominar una técnica que recitar diez.

---

## El eje central: trade-off sesgo–varianza

Casi todo el ML cuelga de una sola descomposición. Modelamos la realidad como $y=f(x)+w$, donde $f(x)$ es el patrón verdadero y $w$ es ruido inevitable. Cuando entrenas un modelo y mides su error de predicción fuera de muestra, ese error se parte en tres:

1. **Sesgo (bias):** qué tan lejos caen *en promedio* tus predicciones de la $f(x)$ real. Sesgo alto = el modelo es **demasiado simple** para capturar el patrón → **underfitting**. (Intentar ajustar una curva con una recta.)
2. **Varianza:** cuánto **cambian** tus predicciones si reentrenas con otra muestra de datos. Varianza alta = el modelo es **demasiado sensible** y aprende el ruido del train particular → **overfitting**. (Memoriza en vez de generalizar.)
3. **Error irreducible:** el ruido $w$ inherente; ningún modelo lo puede vencer.

La tensión: bajar el sesgo (más complejidad) suele subir la varianza, y viceversa. Por eso es un *trade-off*, no un problema con solución única.

- **Lineal / regresión simple:** alto sesgo, baja varianza (rígido pero estable).
- **Redes neuronales / árboles profundos:** bajo sesgo, alta varianza (flexible pero inestable).

En la entrevista casi nunca piden la ecuación; piden **razonar el remedio**, y aquí está el truco que muchos invierten: si el modelo tiene **alta varianza** → consigue más datos o **regulariza** (no más complejidad, que empeora); si tiene **alto sesgo** → aumenta la complejidad (más datos no ayudan a un modelo que ni siquiera puede capturar el patrón). Navaja de Occam: el modelo más simple que cumple suele generalizar mejor.

## Overfitting y regularización

**Overfitting** es el síntoma de varianza alta: el modelo memoriza ruido del train y no generaliza al test. La **regularización** lo combate **penalizando la complejidad** —cambia un poco de sesgo por mucha menos varianza—. La idea: añade a la pérdida un castigo por pesos grandes, así que el optimizador prefiere modelos más "suaves".

- **L2 (Ridge):** penaliza $\sum_i w_i^2$ (la suma de los pesos al cuadrado) → **encoge** los pesos hacia 0 sin anularlos. Suaviza.
- **L1 (Lasso):** penaliza $\sum_i |w_i|$ (suma de valores absolutos) → lleva pesos **exactamente a 0** → hace **selección de features** (modelos *sparse*). La geometría del valor absoluto, con sus esquinas, es lo que empuja pesos al cero exacto; el cuadrado de L2 no.
- **Elastic net:** combina L1 y L2 para tener selección *y* suavizado.

Otras defensas contra overfitting: más datos, cross-validation, early stopping, dropout (en redes), poda (en árboles).

## Validación y selección de modelo

Para estimar el desempeño **fuera de muestra** sin engañarte: separa **train / validación / test**. Entrenas en train, eliges hiperparámetros mirando validación, y el **test se toca una sola vez, al final** — si lo miras varias veces para decidir, se convierte en otro set de validación y sobreajustas a él. La **cross-validation (k-fold)** rota qué partición hace de validación (k veces) y promedia, dando una estimación más robusta cuando tienes pocos datos.

## Métricas de clasificación

Toda métrica de clasificación nace de la **matriz de confusión** (TP verdaderos positivos, FP falsos positivos, TN verdaderos negativos, FN falsos negativos). La trampa #1 de entrevista es reportar **accuracy** en problemas desbalanceados:

- **Accuracy** $=\dfrac{TP+TN}{\text{total}}$. **Engaña con clases desbalanceadas:** si 99% son sanos, predecir "sano" siempre da 99% sin haber aprendido nada.
- **Precisión** $=\dfrac{TP}{TP+FP}$: de los que marqué positivos, ¿cuántos lo eran de verdad? (Calidad de mis alarmas.)
- **Recall (sensibilidad)** $=\dfrac{TP}{TP+FN}$: de los positivos reales, ¿cuántos atrapé? (Cobertura.)
- **F1** $=2\cdot\dfrac{P\cdot R}{P+R}$: la media armónica de precisión y recall; castiga que una sea baja, equilibra ambas.
- **ROC / AUC:** curva de TPR vs FPR al barrer el umbral; el **AUC** es la probabilidad de que el modelo rankee un positivo aleatorio por encima de un negativo aleatorio.

**Trade-off precisión–recall:** mover el umbral los intercambia. Subir recall (atrapar todos los cánceres) cuesta más falsas alarmas (menos precisión); subir precisión cuesta dejar casos sin detectar (menos recall). Eliges según cueste más un **FP** (alarma innecesaria) o un **FN** (caso perdido).

## Algoritmos clásicos

Conoce a fondo un puñado; no los recites, entiende qué supone cada uno:

- **Regresión lineal:** supervisado, etiquetas continuas; alto sesgo, muy interpretable.
- **Regresión logística:** clasificación; pasa una combinación lineal por una **sigmoide** para producir una probabilidad; entrena con **log-loss**. Falla con fronteras no lineales.
- **Naive Bayes:** asume independencia condicional de las features dada la clase, lo que evita estimar $2^k$ parámetros; rápido y un baseline fuerte en texto.
- **SVM:** busca la frontera que **maximiza el margen**; con *kernels* logra fronteras no lineales.
- **Árboles de decisión:** muy interpretables pero propensos a overfit.
- **Ensembles:** combinan muchos modelos. **Bagging / Random Forest** promedia árboles entrenados sobre muestras con reemplazo (y sub-muestreo de features) para **bajar varianza**; **Boosting (AdaBoost/XGBoost)** entrena modelos en secuencia, cada uno corrigiendo los errores del anterior, para **bajar sesgo**.

## No supervisado y reducción de dimensión

- **K-means / clustering:** halla grupos ocultos (segmentar clientes); debes elegir $k$.
- **PCA:** proyecta los datos a las direcciones de **máxima varianza** (los eigenvectores de la matriz de covarianza), conservando la mayor señal en menos dimensiones. Dos pitfalls: es **sensible a la escala** (estandariza antes, como k-means) y los componentes pierden interpretabilidad directa.

## Optimización: descenso de gradiente

El motor que entrena casi todo. Para minimizar una función de pérdida, te mueves en la dirección de **máximo descenso**:

$$x_{t+1}=x_t-\alpha\,\nabla f(x_t),$$

donde $\nabla f(x_t)$ es el gradiente (la dirección de mayor subida; por eso lo restas) y $\alpha$ es el **learning rate** (cuánto avanzas en cada paso). Si la pérdida es **convexa**, llegas al óptimo global; si **no** lo es (redes), puedes quedarte en un mínimo local. **SGD** (descenso estocástico) usa mini-lotes en vez de todos los datos para escalar.

> **Predicción antes de seguir:** tu modelo da 100% de accuracy en train y 70% en test. ¿Más complejidad o más regularización? Respuesta: **regularización (o más datos)**. La brecha train≫test es la firma de **alta varianza** (overfitting); subir la complejidad la agranda. El error de train siempre baja con la complejidad, así que un train perfecto no es maestría, es la señal de alarma.

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
