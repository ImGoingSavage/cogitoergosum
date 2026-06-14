# Aprendizaje estadístico IV: no linealidad, árboles, SVM y no supervisado

## Más allá de la linealidad (Cap. 7)

Extensiones lineales **en los parámetros** vía **funciones base**:
- **Polinómica** (x, x², x³…): se descontrola en los **extremos**.
- **Funciones escalón:** cortar x en intervalos, constante por tramo.
- **Splines de regresión:** polinomios (cúbicos) **a trozos** unidos en **nudos (knots)** con continuidad de la función y sus derivadas. Más nudos = más flexibilidad. Mejor que un polinomio global (flexibilidad **local**, colas estables; spline **natural** = lineal en los extremos).
- **Spline suavizante:** un nudo por dato + penalización de rugosidad controlada por **λ** (CV).
- **GAM:** y = β₀ + Σ **fⱼ(xⱼ)** (cada fⱼ un spline): no linealidad **por feature** conservando la **aditividad** (interpretable); sin interacciones salvo que se añadan.

## Árboles y ensembles (Cap. 8)

- **Árbol:** partición binaria recursiva; predice media (regresión) o clase mayoritaria (clasif.). Divide minimizando RSS o impureza (**Gini/entropía**). Interpretable pero de **alta varianza**.
- **Bagging:** muchos árboles sobre muestras **bootstrap**, promediados → reduce **varianza**. Problema: con un predictor fuerte los árboles quedan **correlacionados**.
- **Random Forest:** en cada split solo **m predictores al azar** (≈√p clasif., p/3 regresión) → **decorrelaciona** los árboles → más reducción de varianza. Con m=p es bagging. Ver [[elegir-ensemble]].
- **OOB error:** cada dato se predice con los ~⅓ de árboles que no lo vieron → estimación de test **gratis**.
- **Importancia de variables:** reducción total de RSS/impureza atribuida a cada feature.
- **Boosting:** árboles **secuenciales** ajustados a los **residuos**; aprende lento. Params: **B** (puede sobreajustar → CV), **d** (profundidad, a veces stumps d=1), **λ** (shrinkage/learning rate pequeño).

## SVM (Cap. 9)

- **Margen máximo:** hiperplano que maximiza la distancia a los puntos más cercanos (**support vectors**, los únicos que lo determinan). Falla si no es separable.
- **Support vector classifier (soft margin):** permite violaciones con un coste **C**. C regula **sesgo-varianza**: C pequeño → margen ancho, muchos SV, más sesgo/menos varianza; C grande → margen estrecho, menos sesgo/más varianza. C por CV.
- **SVM:** **kernel trick** (polinómico, **RBF**) → fronteras **no lineales** sin expandir features. Multiclase: **one-vs-one** / **one-vs-all**.

## No supervisado (Cap. 10)

- **PCA:** direcciones ortogonales de **máxima varianza** (componentes); **PVE**/scree para elegir cuántas; estandarizar si las escalas difieren.
- **K-means:** particiona en **K fijo** minimizando la varianza intra-cluster; depende de la inicialización (corre varias veces); clusters esféricos.
- **Jerárquico:** **no fija K**; **dendrograma** aglomerativo que se corta a la altura deseada; depende del **linkage** (complete/average > single) y la distancia. Ver [[clustering-kmeans-jerarquico]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Relación no lineal pero legible | Splines / GAM (no polinomio de alto grado) |
| Árbol inestable | Bagging → RF (decorrelaciona con m=√p); usa OOB |
| Máxima precisión con tuning | Boosting (B, d, λ pequeño) |
| Frontera no lineal en clasificación | SVM con kernel RBF; C por CV |
| Sin etiquetas | PCA (reducir) / clustering (K-means fija K; jerárquico no) |

---

> **Síntesis:** para no linealidad legible usa **splines/GAM** (nudos, no grado). Los árboles son inestables → **bagging** baja varianza y **random forests** la bajan más **decorrelacionando** (m=√p, con **OOB** gratis); el **boosting** aprende lento y secuencial (B/d/λ). La **SVM** maximiza el margen, regula sesgo-varianza con **C** y captura fronteras no lineales con **kernels**. Sin etiquetas, **PCA** resume y **K-means/jerárquico** agrupan.

---

*Retrieval: (1) ¿por qué splines mejor que polinomio global?; (2) ¿cómo decorrelaciona un RF y qué es el OOB?; (3) ¿qué regula C en una SVM?; (4) ¿K-means vs jerárquico?*
