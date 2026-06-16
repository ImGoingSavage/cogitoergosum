# Aprendizaje estadístico IV: no linealidad, árboles, SVM y no supervisado

## De qué trata esta lección (y qué sabrás hacer al final)

Cuando la relación entre $X$ e $Y$ no es lineal, hace falta un arsenal más flexible. Esta lección lo recorre desde cero: cómo capturar no linealidad **sin perder control** (splines, GAM), los métodos basados en árboles (y por qué un **random forest** decorrelaciona para ganar donde el bagging se estanca), las **SVM** con su margen y su kernel trick, y el aprendizaje **no supervisado** (PCA, clustering). El hilo conductor sigue siendo el sesgo-varianza: cada método es una forma distinta de marcar la perilla de flexibilidad.

Al terminar podrás: (1) preferir splines/GAM a un polinomio global y saber por qué; (2) explicar cómo y por qué un random forest decorrelaciona los árboles (m=√p) y qué regala el OOB; (3) entender qué regula la C de una SVM y qué hace el kernel trick; y (4) distinguir PCA, K-means y clustering jerárquico. Cada idea entra por su intuición.

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

## Mini-ejemplo trabajado: por qué un Random Forest decorrelaciona

Un solo árbol es de **alta varianza**: cambia mucho con otro dataset. Bagging promedia B árboles bootstrap; si fueran independientes, la varianza del promedio caería a σ²/B. Pero hay un problema: si existe **un predictor dominante**, casi todos los árboles lo eligen para el primer corte y quedan **parecidos** (correlación ρ alta). La varianza del promedio de B variables con correlación ρ es:

> ρσ² + (1−ρ)σ²/B

El segundo término se desvanece con B, pero el primero, **ρσ², no baja** por más árboles que sumes. El Random Forest ataca justo ρ: en cada split solo considera **m≈√p predictores al azar**, así que muchos árboles *no pueden* usar el predictor dominante → se **decorrelacionan** → ρ baja → la varianza del bosque cae más.

**Predicción antes de seguir:** ¿qué pasa si pones m=p en un Random Forest? Respuesta: vuelve a ser **bagging** (todos los árboles ven todos los predictores, se recorrelacionan). El parámetro m es exactamente la perilla de decorrelación; m pequeño decorrelaciona más pero arriesga ignorar señales útiles. Y el **OOB error** sale gratis: cada dato se evalúa con el ~⅓ de árboles que no lo vieron.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** árbol inestable → bagging baja varianza → Random Forest la baja más decorrelacionando (m=√p), con OOB como test gratis.
- **Contraejemplo (boosting ≠ bagging):** el boosting NO promedia modelos independientes; ajusta árboles **secuenciales a los residuos**, aprende lento y *puede* sobreajustar si B crece sin CV. Reduce sesgo, no solo varianza.
- **Caso borde (polinomio global):** subir el grado de un polinomio se descontrola en los extremos; un spline natural (lineal en las colas) da flexibilidad local estable. El borde motiva splines sobre polinomios.

## Errores típicos

- **Conceptual:** creer que añadir árboles a un RF puede sobreajustar; promediar no sobreajusta (a diferencia del boosting con B grande).
- **Técnico:** no estandarizar antes de PCA/SVM-RBF/K-means (todos dependen de la escala/distancia).
- **De interpretación:** leer un dendrograma asumiendo un K fijo, o K-means como si hallara clusters no esféricos.

## Transferencia isomorfa

- **Bagging ↔ bootstrap:** los árboles se entrenan sobre muestras con reemplazo; es el bootstrap de estadística aplicada puesto a reducir varianza (conecta con [[arena-pst2]]).
- **Decorrelación del RF ↔ reducir varianza promediando:** bajar ρ para que el promedio concentre es el principio que Rao-Blackwell formaliza (conecta con [[arena-dg1]]).
- **C de la SVM ↔ regularización sesgo-varianza:** C pequeño = margen ancho, más sesgo/menos varianza, la misma perilla que λ en ridge/lasso (conecta con [[arena-isl1]] y [[arena-isl3]]).
- **PCA (máxima varianza) ↔ matriz de covarianza PSD:** las componentes son los ejes de la covarianza, que es semidefinida positiva porque toda varianza aᵀΣa≥0 (conecta con [[arena-q9]]).

Moraleja de la arista: *promediar baja la varianza solo si los modelos están decorrelacionados; el RF lo logra escondiendo predictores (m=√p), y el OOB te regala el error de test.*

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
