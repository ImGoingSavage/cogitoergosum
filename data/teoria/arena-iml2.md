# Interpretabilidad II: modelos interpretables (intrínsecos)

> La opción más simple: usar un modelo que ya es interpretable. Propiedades deseables: **linealidad**, **monotonicidad** e **interacciones** explícitas (o su ausencia).

## De qué trata esta lección (y qué sabrás hacer al final)

La forma más honesta de interpretar un modelo es usar uno que **ya** se entiende por su estructura. Esta lección construye, desde cero, la familia de modelos intrínsecamente interpretables y cómo leer cada uno: regresión lineal (el peso es el efecto por unidad), logística (el odds ratio $e^{\beta_j}$), GLM/GAM (no linealidad sin perder la lectura por feature), árboles y RuleFit (interacciones legibles).

Al terminar podrás: (1) interpretar el peso de una regresión lineal (ceteris paribus) y medir su importancia con el t-statistic; (2) leer un coeficiente logístico como odds ratio; (3) saber qué gana un GAM sobre un GLM lineal; y (4) elegir el modelo según necesites linealidad, monotonicidad o interacciones. El ejemplo de leer un peso y un odds ratio hace de hilo, y la inestabilidad por multicolinealidad conecta con [[arena-htd2]]. Continúa la taxonomía de [[arena-iml1]].

| Modelo | Lineal | Monótono | Interacción | Tarea |
|---|---|---|---|---|
| Regresión lineal | sí | sí | no | regresión |
| Regresión logística | no | sí | no | clasificación |
| Árbol de decisión | no | algo | sí | ambas |
| RuleFit | sí | no | sí | ambas |
| k-NN | no | no | no | ambas |

## Regresión lineal

ŷ = β₀ + β₁x₁ + … + βₚxₚ + ε. **Interpretación del peso:** si xⱼ aumenta en **una unidad** y todo lo demás se mantiene fijo, la predicción cambia en **βⱼ**. Feature **categórica**: el peso es el cambio respecto a la **categoría de referencia**. La importancia de una feature suele medirse con el **t-statistic** (|β̂ⱼ / SE(β̂ⱼ)|). **R²** mide la varianza explicada; usa el **R² ajustado** (penaliza nº de features). Requiere supuestos (linealidad, normalidad, homocedasticidad, independencia, sin multicolinealidad fuerte — si dos features se correlacionan, los pesos se vuelven inestables). Visualízalo con **weight plots** y **effect plots** (efecto = peso × valor de la feature). Ver también [[interpretar-coeficientes-regresion]].

## Regresión logística

Modela P(y=1) pasando la combinación lineal por la **logística** (la salida queda en 0-1). No se interpreta el peso de forma lineal sobre la probabilidad, sino sobre los **log-odds**. **Odds ratio:** al aumentar xⱼ en una unidad, los **odds** se multiplican por **exp(βⱼ)** (manteniendo lo demás fijo). Para categóricas, exp(βⱼ) es el factor sobre los odds frente a la categoría base. Un exp(β)=2 ⇒ los odds se duplican; =1 ⇒ sin efecto.

## GLM y GAM (cuando lo lineal no basta)

- **GLM** generaliza: enlaza E(y) con la combinación lineal vía una **link function** y permite otras distribuciones del error (Poisson para conteos, etc.). Conserva la estructura aditiva.
- **GAM:** reemplaza cada término lineal por una **función no lineal flexible** f(xⱼ) (splines). Captura **no linealidades** sin perder la aditividad ⇒ sigues pudiendo leer el efecto de cada feature en su curva.
- **Interacciones:** los lineales no las modelan salvo que **añadas un término de interacción a mano** (xⱼ·xₖ).

## Árboles de decisión

Particiones recursivas (CART). **Interpretación:** sigue el camino raíz→hoja: "si x≤a Y z>b, entonces…". Capturan **interacciones** de forma natural y no necesitan linealidad/monotonicidad. Importancia de feature = suma de la **reducción de impureza** (Gini/varianza) en los splits que la usan. **Limitación:** inestables (cambiar un poco los datos cambia el árbol), malos para relaciones lineales/suaves (escalera), el nº de hojas crece rápido.

## Reglas de decisión y RuleFit

- **Reglas IF-THEN:** soporte (cobertura) y accuracy (precisión); muy legibles. **OneR** (una sola feature), secuencial covering, bayesian rule lists.
- **RuleFit (Friedman & Popescu):** entrena un ensemble de árboles, extrae **reglas** de sus caminos como features binarias, y ajusta un **modelo lineal LASSO** sobre esas reglas + las features originales ⇒ combina interacciones (de las reglas) con la interpretabilidad de los pesos lineales. Importancia = peso × frecuencia, sumando reglas relacionadas.

---

## Mini-ejemplo trabajado: leer un peso y un odds ratio

**Lineal:** un modelo de precio de casa da β para `m²` = 1 500. Lectura: "manteniendo todo lo demás fijo, **cada m² extra** sube el precio predicho **1 500 €**". Para una categórica `barrio=centro` con β=20 000, es +20 000 € **respecto al barrio de referencia**. La importancia se mide con el **t-statistic** |β̂/SE(β̂)|, no con el tamaño crudo de β.

**Logística:** un modelo de aprobación de crédito da β para `tiene_mora` = 0.69. No leas eso sobre la probabilidad, sino sobre los **odds**: el odds ratio es exp(0.69) ≈ **2.0** → tener mora **duplica los odds** de rechazo, ceteris paribus. exp(β)=1 sería sin efecto.

**Predicción antes de seguir:** dos features muy correlacionadas (`m²` y `nº de habitaciones`). ¿Qué pasa con sus pesos? Se vuelven **inestables** (la multicolinealidad reparte el crédito de forma errática), y un cambio mínimo en los datos puede invertir los signos — la misma fragilidad de las *correlated features* de la deuda técnica.

## Prototipo, contraejemplo y caso borde

- **Prototipo (lineal interpretable):** relación aproximadamente lineal + features no colineales → el peso *es* el efecto por unidad.
- **Contraejemplo (árbol para relación suave):** modelar una relación lineal/suave con un árbol → aproximación en escalera, fea e inestable.
- **Caso borde (no linealidad con lectura por feature):** efecto curvo de la edad → un **GAM** (spline aditivo) captura la curva *sin* perder la lectura por feature, donde el lineal fallaría.

## Errores típicos

- **Conceptual:** interpretar el peso logístico como cambio en la **probabilidad** en vez de en los **log-odds** (usa exp(β) = odds ratio).
- **Estadístico:** confiar en R² crudo (sube al añadir features) en vez del **R² ajustado**; ignorar la multicolinealidad.
- **De modelo:** usar un lineal cuando hay interacciones sin añadir el término `xⱼ·xₖ` a mano.

## Transferencia isomorfa

- **Odds ratio exp(β) ↔ hazard ratio del Cox:** "exp del coeficiente = factor multiplicativo sobre odds/tasa" es la misma lectura que el HR=exp(β) de supervivencia (conecta con [[arena-h8]]).
- **Multicolinealidad ↔ correlated features:** pesos inestables por features correlacionadas es el riesgo de brittleness de la deuda técnica y de atribuir a la feature no causal (conecta con [[arena-htd2]] y [[arena-h4]]).
- **GAM aditivo ↔ separar efectos:** conservar la aditividad para leer el efecto de cada feature es el mismo espíritu que la linealidad de la esperanza descompone una suma (conecta con [[arena-q1]]).

Moraleja de la arista: *el peso lineal es el efecto por unidad (ceteris paribus) y exp(β) el factor sobre odds/tasa; la correlación entre features vuelve esos pesos inestables — interpreta con cuidado.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Relación aprox. lineal y necesito leer efectos | Regresión lineal: peso = cambio por unidad, ceteris paribus |
| Clasificación binaria interpretable | Logística: interpreta **odds ratio** exp(βⱼ) |
| Hay no linealidad pero quiero leer cada efecto | **GAM** (splines aditivos) |
| Sospecho interacciones | Árbol/RuleFit las capturan; en lineal, añádelas a mano |
| Quiero reglas legibles + algo de potencia | **RuleFit**: reglas de árboles + LASSO lineal |

---

> **Síntesis:** prefiere un modelo intrínsecamente interpretable cuando puedas. En **lineal** el peso es el cambio por unidad (ceteris paribus) y la importancia el **t-statistic**; en **logística** interpretas el **odds ratio** exp(βⱼ). **GAM** añade no linealidad conservando la aditividad; **árboles** y **RuleFit** capturan **interacciones** de forma legible. Cada uno paga un precio (inestabilidad, escalera, supuestos), así que elige según linealidad/monotonicidad/interacción.

---

*Retrieval: (1) interpreta el peso de una regresión lineal y di cómo medir su importancia; (2) ¿qué significa exp(βⱼ) en logística?; (3) ¿qué gana un GAM frente a un GLM lineal?; (4) ¿cómo combina RuleFit interacciones e interpretabilidad?*
