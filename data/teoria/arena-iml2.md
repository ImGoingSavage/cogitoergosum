# Interpretabilidad II: modelos interpretables (intrínsecos)

> La opción más simple: usar un modelo que ya es interpretable. Propiedades deseables: **linealidad**, **monotonicidad** e **interacciones** explícitas (o su ausencia).

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
