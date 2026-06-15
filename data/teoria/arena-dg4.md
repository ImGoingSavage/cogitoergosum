# Teoría de la decisión, regresión y modelos lineales

## Teoría de la decisión

**Función de pérdida:** L(θ, δ) = costo de tomar decisión δ cuando el verdadero parámetro es θ.

**Riesgo frecuentista:** R(θ,δ) = E[L(θ,δ(X))]

**Riesgo de Bayes:** r(δ) = E_π[R(θ,δ)] = ∫ R(θ,δ) π(θ) dθ

| Pérdida | Estimador óptimo |
|---------|-----------------|
| Cuadrática (θ-δ)² | Media posterior (Bayes) / X̄ (frecuentista insesgado) |
| Absoluta |θ-δ| | Mediana posterior |
| 0-1 | Moda posterior (MAP) |
| Asimétrica | Pérdidas distintas para sobreestimar/subestimar |

---

## Admisibilidad y la paradoja de Stein

Un estimador δ₁ **domina** a δ₂ si R(θ,δ₁) ≤ R(θ,δ₂) para todo θ, estrictamente para alguno.

δ es **admisible** si ningún estimador lo domina.

**Paradoja de Stein (d≥3):** Para d≥3 variables N(θᵢ,1), el estimador X (insesgado, UMVUE) NO es admisible bajo pérdida cuadrática total. El estimador de **James-Stein** lo domina:

θ̂_JS = (1 - (d-2)/||X||²) · X

Lección: para d=1,2: X̄ es admisible. Para d≥3: shrinkage estimators son mejores.

---

## Regresión lineal simple — modelo y estimación

**Modelo:** Yᵢ = β₀ + β₁xᵢ + εᵢ

Supuestos: E[εᵢ]=0, Var[εᵢ]=σ², independencia.

**OLS** (Ordinary Least Squares) minimiza SS_res = Σ(yᵢ-β₀-β₁xᵢ)²:

**β̂₁ = S_{xy} / S_{xx}** donde S_{xy}=Σ(xᵢ-x̄)(yᵢ-ȳ), S_{xx}=Σ(xᵢ-x̄)²

**β̂₀ = ȳ − β̂₁·x̄**

Valores ajustados: ŷᵢ = β̂₀ + β̂₁xᵢ

Residuos: êᵢ = yᵢ − ŷᵢ (perpendiculares al espacio de las covariables)

---

## Teorema de Gauss-Markov

Bajo E[ε]=0, Var[ε]=σ²I (errores con media 0, varianza constante, independientes):

**β̂_OLS es BLUE:** Best Linear Unbiased Estimator.

"Mejor" = mínima varianza entre todos los estimadores lineales insesgados.

**Bajo normalidad (ε~N):** β̂_OLS = β̂_MLE, y los estadísticos t y F son exactos.

---

## Descomposición SS y R²

SS_tot = SS_reg + SS_res

| Término | Fórmula | df |
|---------|---------|---|
| SS_tot | Σ(yᵢ-ȳ)² | n-1 |
| SS_reg | Σ(ŷᵢ-ȳ)² | p |
| SS_res | Σ(yᵢ-ŷᵢ)² | n-p-1 |

**R² = SS_reg/SS_tot = 1 - SS_res/SS_tot ∈ [0,1]**

R² nunca baja al añadir variables (siempre hay más para explicar).

**R² ajustado** = 1 - (SS_res/(n-p-1))/(SS_tot/(n-1)) — penaliza por p.

---

## Tests en regresión múltiple

**Test F global** (H₀:β₁=…=βₚ=0):

F = (SS_reg/p) / (SS_res/(n-p-1)) ~ F(p, n-p-1) bajo H₀

**Test t individual** (H₀:βⱼ=0):

t = β̂ⱼ / SE(β̂ⱼ) ~ t(n-p-1) bajo H₀

donde SE(β̂ⱼ) = σ̂·√[(X'X)⁻¹]_{jj}

---

## Multicolinealidad

Cuando dos o más predictores están altamente correlacionados:
- β̂_OLS sigue siendo insesgado
- Pero Var(β̂) se infla — tests poco potentes

**VIF (Variance Inflation Factor):**

VIF_j = 1/(1-R²_j)

donde R²_j es el R² de la regresión de Xⱼ sobre los demás predictores.

VIF > 10 → problema severo.

**Soluciones:** eliminar variables colineales, ridge regression, PCA regression.

---

## Ridge y Lasso — regularización

### Ridge (L2):
min_β ||Y-Xβ||² + λ||β||²

**β̂_ridge = (X'X + λI)⁻¹X'Y**

Encoge todos los coeficientes hacia 0, pero ninguno queda exactamente en 0.

### Lasso (L1):
min_β ||Y-Xβ||² + λΣ|βⱼ|

No tiene forma cerrada. Puede anular coeficientes → selección de variables automática.

| Propiedad | Ridge | Lasso |
|-----------|-------|-------|
| Solución cerrada | Sí | No |
| Sparsity | No | Sí |
| Maneja multicolinealidad | Bien | Selecciona uno |

---

## Regresión logística

**Modelo:** log(p/(1-p)) = β₀ + β₁X (log-odds es lineal)

**P(Y=1|X) = σ(β₀+β₁X) = 1/(1+e^{-(β₀+β₁X)})**

El MLE maximiza la log-verosimilitud bernoulli — no tiene forma cerrada; se resuelve con Newton-Raphson o descenso de gradiente.

**Interpretación:** β₁ = cambio en log-odds por unidad de X. e^{β₁} = odds ratio.

---

## ANOVA de una vía

Datos: grupos 1,...,k con nⱼ obs cada uno. H₀:μ₁=…=μₖ.

| Fuente | SS | df | MS | F |
|--------|-----|---|-----|---|
| Entre grupos | n·Σ(ȳⱼ-ȳ)² | k-1 | MS_B | MS_B/MS_W |
| Dentro de grupos | ΣΣ(yᵢⱼ-ȳⱼ)² | n-k | MS_W | |

F ~ F(k-1, n-k) bajo H₀.

ANOVA es un caso especial de regresión lineal con predictores indicadores (dummies).

---

## Criterios de selección de modelo

**AIC = -2ℓ(θ̂) + 2p** — penaliza por número de parámetros p.

**BIC = -2ℓ(θ̂) + p·ln(n)** — penaliza más fuerte para n grande.

**Cross-validation (k-fold):** divide datos en k partes; ajusta en k-1, evalúa en 1; rota y promedia.

Menor AIC/BIC → mejor modelo. Para selección consistente de modelo: BIC. Para predicción: AIC o CV.

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
