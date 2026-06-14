# Interpretabilidad IV: LIME, Shapley/SHAP y explicaciones por ejemplos

## LIME — Local Interpretable Model-agnostic Explanations

Explica **una predicción** entrenando un **modelo interpretable local** (lineal) que aproxima a la caja negra **alrededor de esa instancia**. Receta: (1) genera muestras **perturbadas** cerca de la instancia; (2) pide al modelo negro su predicción para cada una; (3) **pondera** las muestras por su cercanía a la instancia (kernel de proximidad); (4) ajusta un modelo lineal disperso sobre esas muestras ponderadas. Los pesos del lineal son la explicación local. Funciona para tabular, **texto** (presencia/ausencia de palabras) e **imágenes** (superpíxeles). **Debilidades:** definición de "vecindad"/kernel es arbitraria y frágil; **inestabilidad** (dos corridas pueden dar explicaciones distintas).

## Valores de Shapley (teoría de juegos cooperativos)

La predicción es el "pago"; las features son "jugadores". El **valor de Shapley** de una feature = su **contribución marginal promedio** a la predicción sobre **todas las coaliciones** (órdenes) posibles de features. Es el **único** método que cumple los 4 axiomas: **eficiencia** (las contribuciones suman exactamente la diferencia entre la predicción y la **predicción media**), **simetría**, **dummy** (feature sin efecto → 0) y **aditividad**. Es un reparto **justo y completo**. **Coste:** exacto es exponencial → se **estima por muestreo** de coaliciones. **No** entrega un modelo de predicción (a diferencia de LIME).

## SHAP (SHapley Additive exPlanations)

Implementación moderna de los valores de Shapley con base teórica sólida (Lundberg & Lee). Aporta:
- **KernelSHAP** (agnóstico, conecta LIME + Shapley) y **TreeSHAP** (rápido y exacto para árboles/ensembles).
- **Local:** *force plot* — cómo cada feature empuja la predicción desde el valor base hasta ŷ.
- **Global por agregación:** promediar |SHAP| da **importancia global consistente**; los *summary/beeswarm plots* muestran magnitud + dirección por feature; los *dependence plots* muestran el efecto y revelan interacciones. Ventaja sobre permutación: la importancia global está **fundada** en explicaciones locales sólidas y es consistente.

## Explicaciones basadas en ejemplos (model-agnostic, usan instancias)

- **Contrafactuales:** "el menor cambio en las features que **voltea** la predicción al resultado deseado" (te niegan el crédito → "si tu ingreso fuera +5k, te lo aprobarían"). Naturalmente **contrastivos** y accionables (recurso). Criterios de Wachter: cercanía, cambiar pocas features, valores plausibles. Suele haber **varios** (efecto Rashomon).
- **Ejemplos adversariales:** contrafactuales para **engañar** al modelo — perturbación mínima (a veces 1 píxel) que cambia la clase sin que el humano note la diferencia (riesgo de seguridad).
- **Prototipos y críticas (MMD-critic):** prototipos = instancias **representativas** de los datos; críticas = instancias **mal representadas** por los prototipos (outliers/regiones poco cubiertas). Juntos describen la distribución.
- **Instancias influyentes:** ¿qué puntos de **entrenamiento** moldearon más el modelo/esta predicción? Vía **deletion diagnostics** (DFBETA: borrar y reentrenar) o **influence functions** (aproximación con gradientes/Hessiano, sin reentrenar). Útil para depurar datos.
- **Anchors:** reglas IF-THEN locales de alta **precisión** ("ancla") que fijan la predicción con alta probabilidad pase lo que pase con el resto de features; complementan a LIME con cobertura explícita.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Explica esta predicción con un sustituto local | **LIME** (ojo: vecindad arbitraria, inestable) |
| Quiero un reparto **justo y completo** entre features | **Valores de Shapley** (suman ŷ − ŷ̄; 4 axiomas) |
| Importancia local **y** global consistente, árboles rápidos | **SHAP** (TreeSHAP; beeswarm/force/dependence) |
| "¿Qué cambio mínimo cambiaría la decisión?" / recurso | **Contrafactual** (contrastivo, accionable) |
| Describir el dataset / detectar lo no representado | **Prototipos y críticas** (MMD-critic) |
| ¿Qué datos de entrenamiento causaron esto? | **Instancias influyentes** (DFBETA / influence functions) |

---

> **Síntesis:** **LIME** ajusta un lineal local sobre muestras perturbadas y ponderadas (potente pero inestable). Los **valores de Shapley** reparten la predicción de forma **justa y completa** (única que cumple eficiencia/simetría/dummy/aditividad) sobre todas las coaliciones; **SHAP** los hace prácticos (TreeSHAP) y da importancia global **consistente**. Las explicaciones **por ejemplos** —contrafactuales (contrastivos y accionables), adversariales, prototipos/críticas, instancias influyentes y anchors— explican con data points en vez de resúmenes.

---

*Retrieval: (1) describe los 4 pasos de LIME y su debilidad; (2) ¿qué propiedad de "eficiencia" cumplen los valores de Shapley?; (3) ¿qué añade SHAP frente a la importancia por permutación?; (4) ¿por qué un contrafactual es contrastivo y accionable?*
