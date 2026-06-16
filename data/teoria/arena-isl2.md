# Aprendizaje estadístico II: regresión lineal y clasificación

## De qué trata esta lección (y qué sabrás hacer al final)

Las dos tareas supervisadas más comunes son predecir un número (**regresión**) y predecir una etiqueta (**clasificación**). Esta lección construye, desde cero, los modelos de referencia de cada una: la regresión lineal (cómo se interpreta cada coeficiente y por qué el F-test existe **además** de los t) y los clasificadores fundamentales (logística, LDA/QDA), con su evaluación honesta (matriz de confusión, ROC/AUC) en vez del engañoso accuracy.

Al terminar podrás: (1) leer un coeficiente como efecto **parcial** y entender por qué puede cambiar de signo (confounding); (2) saber por qué el F global corrige la multiplicidad que los t individuales no ven; (3) elegir entre logística (discriminativa) y LDA/QDA (generativos) según el caso; y (4) evaluar un clasificador con sensibilidad/especificidad/AUC. Cada idea entra por un ejemplo concreto.

## Regresión lineal: estimación e inferencia

- **Mínimos cuadrados:** elige β̂ que minimizan RSS = Σ(yᵢ−ŷᵢ)². La recta pasa por (x̄, ȳ).
- **Error estándar** SE(β̂): precisión del coeficiente. IC 95% ≈ β̂ ± 2·SE.
- **Test del coeficiente:** H0: βⱼ=0. **t = β̂ⱼ/SE(β̂ⱼ)** y su p-valor; p pequeño ⇒ hay asociación.
- **Ajuste del modelo:** **RSE** (desviación del error, unidades de Y) y **R²** = 1 − RSS/TSS (proporción de varianza explicada, adimensional).

En **regresión múltiple** cada coeficiente es un efecto **parcial** (ceteris paribus). Por eso un coeficiente puede cambiar de signo respecto a la simple: en simple absorbía el efecto de variables correlacionadas omitidas (**confounding**). Ver también [[interpretar-coeficientes-regresion]].

### F-statistic (significancia global)
Contrasta H0: **todos** los β=0. Hace falta además de los t porque, con muchos predictores, ~5% darían p<0.05 por azar (**comparaciones múltiples**); el F evalúa el modelo en conjunto. F≈1 bajo H0; F grande + p pequeño ⇒ modelo útil.

### Extensiones y problemas
- **Cualitativos:** dummies (L−1 para L niveles); el coef. es la diferencia vs la **referencia**.
- **Interacción** X₁·X₂: el efecto de uno depende del otro; **principio jerárquico** (incluir los efectos principales).
- **Problemas potenciales:** no linealidad, errores correlacionados, heterocedasticidad, outliers, alto **leverage**, **colinealidad**.
- **Colinealidad** → SE inflados, pesos inestables. Detecta con **VIF = 1/(1−R²ⱼ)** (>5–10 problemático).

## Clasificación

**¿Por qué no regresión lineal?** Codificar clases impone orden/distancia falsos y, en binario, da probabilidades fuera de [0,1].

- **Regresión logística:** P(Y=1|X) vía la logística (salida en (0,1)); ajuste por máxima verosimilitud; efecto = **odds ratio** exp(βⱼ). Es **discriminativa** (modela P(Y|X) directo).
- **LDA** (generativo): modela X|clase como **Gaussiana con covarianza COMÚN** + Bayes ⇒ frontera **lineal**. Más estable que la logística con clases separadas o n pequeño.
- **QDA:** covarianza **por clase** ⇒ frontera **cuadrática** (más flexible, más varianza, más datos). **Naive Bayes:** features independientes dentro de cada clase.

### Evaluación
**Matriz de confusión** (TP/FP/TN/FN) revela el tipo de error. **Sensibilidad** = TP/(TP+FN); **especificidad** = TN/(TN+FP). El **umbral** mueve el balance; la **ROC** traza sensibilidad vs (1−especificidad) y el **AUC** resume (1=perfecto, 0.5=azar). Ver [[metrica-clasificacion]].

---

## Mini-ejemplo trabajado: por qué F además de los t

Ajustas una regresión con **100 predictores irrelevantes** (ninguno asociado a Y). Cada test t individual rechaza H0: βⱼ=0 con prob 0.05 por azar, así que esperas **~5 coeficientes "significativos"** aunque el modelo no valga nada. Si solo miras los t, declararás hallazgos falsos.

El **F-statistic global** contrasta H0: *todos* los β=0 a la vez y, bajo esa nula, vale ≈1 sin importar cuántos predictores haya — corrige el problema de comparaciones múltiples que los t no ven. F grande con p pequeño dice "el modelo, en conjunto, explica algo".

**Predicción antes de seguir:** con p=100 predictores y n=1000, ¿bastaría con reportar el predictor de menor p-valor? Respuesta: **no**. Con 100 tests, el mínimo p-valor está sesgado a ser pequeño por puro azar (vast search). El F protege el conjunto; para predictores individuales necesitas corrección (Bonferroni/FDR) o validación fuera de muestra. Es exactamente la multiplicidad de los A/B tests.

## Prototipo, contraejemplo y caso borde

- **Prototipo (clasificación):** binaria con clases bien separadas y n chico → LDA (genera X|clase gaussiano, covarianza común) es más estable que la logística.
- **Contraejemplo (regresión lineal para clasificar):** codificar 3 clases como 1,2,3 impone orden y distancias falsos y da probabilidades fuera de [0,1]; parece funcionar pero está mal planteado.
- **Caso borde (error global engañoso):** con 99% de clase mayoritaria, un modelo que predice "siempre mayoría" tiene 99% de acierto y 0% de sensibilidad. El borde obliga a mirar la matriz de confusión, no el accuracy.

## Errores típicos

- **Conceptual:** leer un coeficiente parcial (ceteris paribus) como efecto marginal; con confounding puede hasta cambiar de signo.
- **Técnico:** ignorar la colinealidad (SE inflados, pesos inestables) — revisa VIF>5–10.
- **De interpretación:** resumir un clasificador por accuracy cuando hay desbalance, en vez de sensibilidad/especificidad/AUC.

## Transferencia isomorfa

- **t y F ↔ LRT y tests clásicos:** el t de un coeficiente y el F global son casos del test de razón de verosimilitudes; el F corrige multiplicidad igual que en experimentos (conecta con [[arena-dg3]] y [[arena-cb3]]).
- **Odds ratio e^β de la logística ↔ hazard ratio de Cox:** ambos son efectos multiplicativos sobre un log-link (conecta con [[arena-h8]]).
- **VIF / colinealidad ↔ confounding y leakage:** redundancia entre predictores infla la varianza, omitir un predictor sesga el signo (conecta con [[arena-dg4]] y [[arena-pst4]]).
- **ROC/AUC, sensibilidad, especificidad ↔ tasa base y VPP:** el umbral mueve el balance FP/FN y, con prevalencia baja, el AUC alto no garantiza precisión (conecta con [[arena-q2]] y [[arena-htd4]]).

Moraleja de la arista: *el t prueba un coeficiente, el F el modelo entero (y corrige el azar de los muchos t); en clasificación, nunca confíes en el accuracy global sin la matriz de confusión.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| ¿El predictor importa? | t = β̂/SE y su p-valor |
| Muchos predictores, ¿sirve el modelo? | F-statistic global (corrige el azar de los t) |
| Coeficiente cambia de signo | Confounding: efecto parcial vs marginal |
| Pesos inestables / SE enormes | Colinealidad: revisa el VIF |
| Clasificar con n chico y clases separadas | LDA (más estable que logística) |
| Error global bajo pero ¿detecta la clase rara? | Matriz de confusión + sensibilidad + ROC/AUC |

---

> **Síntesis:** en regresión, **t** prueba un coeficiente y **F** el modelo entero (corrige comparaciones múltiples); cuida la **colinealidad** con el **VIF** y respeta el **principio jerárquico**. En clasificación, la **logística** es discriminativa y **LDA/QDA** generativos (covarianza común→lineal, por clase→cuadrática). Evalúa con **matriz de confusión, sensibilidad/especificidad y ROC/AUC**, no solo el error global.

---

*Retrieval: (1) ¿qué prueba el F frente a los t?; (2) define el VIF y su umbral; (3) ¿LDA vs QDA, qué cambia en la frontera?; (4) ¿qué mide el AUC?*
