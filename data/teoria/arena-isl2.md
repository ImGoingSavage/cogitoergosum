# Aprendizaje estadístico II: regresión lineal y clasificación

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
