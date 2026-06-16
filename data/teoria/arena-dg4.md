# Teoría de la decisión, regresión y modelos lineales

## De qué trata esta lección (y qué sabrás hacer al final)

Esta lección cierra el cluster uniendo tres hilos: **cómo decidir bien bajo incertidumbre** (teoría de la decisión y la sorprendente paradoja de Stein), **el modelo lineal** (OLS, Gauss-Markov, R²) y sus **extensiones** (regularización, logística, ANOVA, selección de modelo). El hilo conductor: casi todo se reduce a un trade-off entre sesgo y varianza, y a elegir la métrica correcta para penalizar el error.

Al terminar podrás: (1) leer una función de pérdida y el riesgo, y entender por qué encoger (shrinkage) puede dominar al estimador insesgado; (2) estimar e interpretar una regresión lineal sabiendo qué garantiza Gauss-Markov; (3) reconocer la multicolinealidad y por qué ridge/lasso la curan; y (4) comparar modelos con AIC/BIC/CV en vez de R². Cada idea entra por su intuición. La paradoja de Stein va con su intuición de regularización, no con su prueba.

> Conecta el OLS=MLE de [[arena-dg2]] con el ML aplicado de [[arena-ads3]] y la inferencia causal de regresión de [[arena-pst4]].

---

## Teoría de la decisión

Estimar es **decidir**, y toda decisión tiene un costo. La **función de pérdida** $L(\theta,\delta)$ mide el costo de elegir $\delta$ cuando la verdad es $\theta$. Promediando sobre los datos obtienes el **riesgo frecuentista** $R(\theta,\delta)=E[L(\theta,\delta(X))]$; promediando además sobre un prior, el **riesgo de Bayes** $r(\delta)=\int R(\theta,\delta)\,\pi(\theta)\,d\theta$. La gracia: **la pérdida que elijas determina el estimador óptimo**.

| Pérdida | Estimador óptimo |
|---------|-----------------|
| Cuadrática $(\theta-\delta)^2$ | media posterior / $\bar X$ |
| Absoluta $\lvert\theta-\delta\rvert$ | mediana posterior |
| 0-1 | moda posterior (MAP) |

Si penalizas el error al cuadrado, la media minimiza; si lo penalizas en valor absoluto, la mediana (más robusta a outliers). No hay un "mejor estimador" universal — depende de cómo cuesta equivocarse.

## Admisibilidad y la paradoja de Stein

Un estimador $\delta_1$ **domina** a $\delta_2$ si $R(\theta,\delta_1)\le R(\theta,\delta_2)$ para todo $\theta$ (y estricto en alguno). Un estimador es **admisible** si nadie lo domina. Aquí viene uno de los resultados más contraintuitivos de la estadística:

**Paradoja de Stein ($d\ge 3$):** al estimar $d\ge 3$ medias normales independientes, el estimador "obvio" $X$ (insesgado, UMVUE) **no es admisible**. El estimador de **James-Stein**, que encoge hacia 0,

$$\hat\theta_{\text{JS}}=\Big(1-\frac{d-2}{\lVert X\rVert^2}\Big)X,$$

lo **domina** en MSE total — ¡aunque las medias no tengan nada que ver entre sí! La intuición (que el ML redescubriría como regularización): encoger introduce **sesgo** pero recorta tanta **varianza** que el MSE total baja. Para $d=1,2$, $\bar X$ es admisible; para $d\ge3$, encoger gana.

## Regresión lineal simple: modelo y estimación

El modelo más usado del mundo: $Y_i=\beta_0+\beta_1 x_i+\varepsilon_i$, con errores de media 0, varianza constante $\sigma^2$ e independientes. El **OLS** elige $\beta$ minimizando la suma de cuadrados de los residuos $\sum(y_i-\beta_0-\beta_1 x_i)^2$. La solución:

$$\hat\beta_1=\frac{S_{xy}}{S_{xx}}=\frac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2},\qquad \hat\beta_0=\bar y-\hat\beta_1\bar x.$$

Lee $\hat\beta_1$: es la **covarianza** de $x$ e $y$ normalizada por la **varianza** de $x$ — "cuánto sube $y$ por unidad de $x$". Los residuos $\hat e_i=y_i-\hat y_i$ son, geométricamente, **perpendiculares** al espacio de las covariables (la recta es la proyección de $y$).

## Teorema de Gauss-Markov

`[CAJA NEGRA OK]` — asume el resultado; su valor es saber **qué garantiza y qué no**.

Bajo errores con media 0, varianza constante e independientes (¡sin pedir normalidad!), el OLS es **BLUE**: el **mejor estimador lineal insesgado** (menor varianza entre todos los lineales insesgados). Si **además** los errores son normales, entonces OLS $=$ MLE y los estadísticos $t$ y $F$ son **exactos** (no solo asintóticos). La normalidad no se necesita para que OLS sea óptimo entre lineales; se necesita para la inferencia exacta.

## Descomposición SS y R²

La variabilidad total de $y$ se parte en lo que el modelo explica y lo que queda: $SS_{\text{tot}}=SS_{\text{reg}}+SS_{\text{res}}$. El **R²** es la fracción explicada:

$$R^2=\frac{SS_{\text{reg}}}{SS_{\text{tot}}}=1-\frac{SS_{\text{res}}}{SS_{\text{tot}}}\in[0,1].$$

La **trampa**: $R^2$ **nunca baja** al añadir variables (siempre hay algo más que ajustar, aunque sea ruido). Por eso no sirve para comparar modelos de distinto tamaño. El **R² ajustado** penaliza por el número de predictores $p$ y sí puede bajar si una variable no aporta.

## Tests en regresión múltiple

- **Test F global** ($H_0:\beta_1=\dots=\beta_p=0$, "el modelo no explica nada"): $F=\dfrac{SS_{\text{reg}}/p}{SS_{\text{res}}/(n-p-1)}\sim F(p,n-p-1)$.
- **Test t individual** ($H_0:\beta_j=0$): $t=\hat\beta_j/\text{SE}(\hat\beta_j)$, con $\text{SE}(\hat\beta_j)=\hat\sigma\sqrt{[(X^\top X)^{-1}]_{jj}}$.

## Multicolinealidad

Cuando dos predictores están muy correlacionados, el modelo no puede separar sus efectos: $\hat\beta$ sigue **insesgado**, pero su **varianza se infla** (tests débiles, signos inestables). Se mide con el **VIF** $=1/(1-R_j^2)$, donde $R_j^2$ es el R² de regresar $X_j$ sobre los demás predictores; $\text{VIF}>10$ es problema serio. Curas: eliminar variables redundantes, **ridge**, o regresión sobre componentes PCA.

## Ridge y Lasso: regularización

Para combatir colinealidad y sobreajuste, se penaliza el tamaño de los coeficientes:

- **Ridge (L2):** minimiza $\lVert Y-X\beta\rVert^2+\lambda\lVert\beta\rVert^2$, con solución cerrada $\hat\beta_{\text{ridge}}=(X^\top X+\lambda I)^{-1}X^\top Y$. Encoge todos los coeficientes hacia 0 pero **ninguno a 0 exacto**.
- **Lasso (L1):** minimiza $\lVert Y-X\beta\rVert^2+\lambda\sum|\beta_j|$. Sin forma cerrada, pero **anula** coeficientes → selección automática de variables.

La conexión profunda: ridge **es** James-Stein/shrinkage, y equivale a un prior normal sobre $\beta$. Regularizar es cambiar sesgo por varianza, justo lo que Stein demostró óptimo.

## Regresión logística

Cuando $Y$ es binaria (0/1), no modelas $Y$ sino la **probabilidad**, forzando que el **log-odds** sea lineal:

$$\log\frac{p}{1-p}=\beta_0+\beta_1 X\quad\Longleftrightarrow\quad P(Y=1\mid X)=\sigma(\beta_0+\beta_1 X)=\frac{1}{1+e^{-(\beta_0+\beta_1 X)}}.$$

La sigmoide $\sigma$ comprime cualquier número real a $(0,1)$. El MLE maximiza la log-verosimilitud Bernoulli (sin forma cerrada → Newton-Raphson o descenso de gradiente). Interpretación clave: $\beta_1$ es el cambio en log-odds por unidad de $X$, y $e^{\beta_1}$ es el **odds ratio**.

## ANOVA y selección de modelo

**ANOVA de una vía** ($H_0:\mu_1=\dots=\mu_k$) compara la variabilidad **entre** grupos con la variabilidad **dentro** de grupos vía $F=MS_B/MS_W$. Es un caso especial de regresión con predictores indicadores (dummies). **Selección de modelo:**

- **AIC** $=-2\ell(\hat\theta)+2p$ — penaliza la complejidad; orientado a **predicción**.
- **BIC** $=-2\ell(\hat\theta)+p\ln n$ — penaliza más fuerte con $n$ grande; orientado a **identificar el modelo correcto**.
- **Cross-validation:** estima el error fuera de muestra rotando particiones.

Menor AIC/BIC → mejor. Todos comparten la moraleja: penaliza la complejidad, no premies el ajuste bruto.

> **Predicción antes de seguir:** añades 5 variables aleatorias (puro ruido) a tu regresión. ¿Qué pasa con R² y con R² ajustado? Respuesta: $R^2$ **sube** (o no baja) — siempre, porque el ruido explica algo del train por azar; $R^2$ ajustado, AIC, BIC y CV **empeoran**, penalizando las variables inútiles. Por eso comparar modelos por R² es un error clásico: confunde "ajusta más el train" con "predice mejor".

---

## Mini-ejemplo trabajado: shrinkage de James-Stein con intuición

Estimas 3 medias independientes θ₁,θ₂,θ₃ con una observación N(θᵢ,1) cada una: X=(2, −1, 4). El estimador "obvio" es X̄=X mismo. James-Stein encoge hacia 0:

> θ̂_JS = (1 − (d−2)/‖X‖²)·X, con d=3, ‖X‖²=4+1+16=21
> factor = 1 − 1/21 ≈ 0.952 → θ̂_JS ≈ (1.90, −0.95, 3.81)

Para d≥3, **este estimador sesgado domina a X** en MSE total, *aunque las tres medias no tengan nada que ver entre sí*. La paradoja: prestar fuerza entre problemas independientes mejora el agregado.

**Predicción antes de seguir:** ¿de dónde sale la mejora si los θᵢ son ajenos? Respuesta: encoger introduce **sesgo** pero recorta mucha **varianza**; con d≥3 la cuenta MSE=Var+Bias² sale a favor. Es exactamente lo que hace la **regularización ridge** (y un prior bayesiano hacia 0): cambiar un poco de sesgo por mucha varianza. Stein descubrió en 1961 lo que ML redescubrió como regularización.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** errores con media 0 y varianza constante → OLS es BLUE (Gauss-Markov), sin pedir normalidad.
- **Contraejemplo (R² engañoso):** añadir variables irrelevantes nunca baja R²; parece "mejor modelo" pero sobreajusta. Solo R² ajustado / AIC / CV penalizan la complejidad.
- **Caso borde (multicolinealidad):** con predictores casi colineales, β̂ sigue insesgado pero Var(β̂) explota (VIF alto) y los signos se vuelven inestables. El borde muestra que insesgado no implica interpretable.

## Errores típicos

- **Conceptual:** leer un coeficiente OLS grande como "efecto importante" sin mirar su SE ni la colinealidad.
- **Técnico:** comparar modelos de distinto tamaño por R² en vez de R² ajustado / AIC / BIC / CV.
- **De interpretación:** interpretar β de regresión observacional como causal sin un diseño que controle confundidores.

## Transferencia isomorfa

- **James-Stein ↔ ridge / prior bayesiano:** encoger hacia 0 es regularización L2; el shrinkage óptimo es un prior disfrazado (conecta con [[arena-iml4]], regularización y sesgo-varianza).
- **Odds ratio de la logística (e^β) ↔ hazard ratio de Cox:** ambos son efectos multiplicativos sobre un log-link; e^β en log-odds es el primo de e^β en log-hazard (conecta con [[arena-h8]]).
- **ANOVA (between/within) ↔ ley de varianza total:** SS_between + SS_within es exactamente Var[E[Y|X]] + E[Var[Y|X]] (conecta con [[arena-b2]]).
- **Multicolinealidad / VIF ↔ leakage y features redundantes:** predictores que cargan la misma información inflan la varianza igual que features filtradas inflan el desempeño aparente (conecta con [[arena-dmls1]]).
- **AIC/BIC/CV ↔ selección de modelo en producción:** penalizar complejidad para predecir bien fuera de muestra es la misma decisión que elegir capacidad de un modelo desplegado (conecta con [[arena-iml4]]).

Moraleja de la arista: *OLS es BLUE pero no intocable; encoger (Stein/ridge) cambia sesgo por varianza y suele ganar, y comparar modelos exige penalizar complejidad, no mirar R².*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Mínima varianza entre lineales insesgados" | BLUE = OLS bajo Gauss-Markov |
| "¿R² sube al añadir variables?" | Sí siempre; usa R² ajustado |
| "Colinealidad entre predictores" | VIF, ridge, PCA |
| "H₀: todos los betas=0" | Test F global |
| "H₀: βⱼ=0 individualmente" | Test t con n-p-1 df |
| "Variable binaria a predecir" | Regresión logística (log-odds) |
| "d≥3 medias con pérdida cuadrática" | James-Stein domina a X̄ |
| "Comparar modelos distintos" | AIC/BIC/CV |

---

> **Síntesis:** El OLS es el BLUE por Gauss-Markov — sin normalidad. Con normalidad, OLS = MLE y los tests son exactos. R² mide cuánto explica el modelo, pero solo R² ajustado compara modelos de diferente tamaño. Regularización (ridge, lasso) es el antídoto a la multicolinealidad y el sobreajuste.

---

*Retrieval: cierra y responde: (1) fórmula de β̂₁ en regresión simple; (2) estadístico F para test global de regresión; (3) β̂_ridge para X'X=I (matriz identidad); (4) odds ratio para β₁=0.7 en logística.*
