# Análisis de supervivencia III: Cox extendido y modelos paramétricos/AFT

## Cox extendido (covariables tiempo-dependientes)

**h(t,X(t)) = h₀(t)·exp[Σ βᵢXᵢ + Σ δⱼXⱼ(t)].** Dos usos:
1. Covariables **genuinamente cambiantes** (estatus de trasplante, laboratorios repetidos).
2. **Modelar la no-PH** con interacciones covariable×g(t) (X·t, X·ln t): si δ es significativo, el efecto depende del tiempo.

Con términos tiempo-dependientes el **HR ya no es constante** (se evalúa en un instante). **Precaución:** la covariable en t solo usa información **hasta t**; usar el futuro = **immortal time bias**. Se implementa partiendo el tiempo en intervalos (start, stop] con el valor actual. Ver [[cox-extendido-tiempo-dependiente]].

## Modelos paramétricos

Asumen una **distribución** del tiempo (modelan todo el hazard, a diferencia del Cox):
- **Exponencial:** hazard **constante** λ; S(t)=exp(−λt).
- **Weibull:** hazard **monótono** (creciente si forma p>1, decreciente si p<1; p=1 → exponencial).
- **Log-logística / log-normal:** hazard **no monótono** (sube y baja).

Ventajas: estimación más **eficiente** (si la forma es correcta), **predicción** de tiempos/percentiles y **extrapolación** más allá del seguimiento. Desventaja: **sesgo** si la distribución es errónea. Validar con diagnósticos (Weibull: ln(−ln Ŝ) vs ln t lineal), AIC, comparación con KM.

## AFT (Accelerated Failure Time)

Modela el efecto sobre el **TIEMPO** de supervivencia, no sobre el hazard: un **factor de aceleración** γ **estira** (γ>1, alarga la vida) o **encoge** (γ<1) el eje del tiempo. En ln T = α + γᵀX + error, el factor = exp(coef). Intuición: γ=2 ⇒ "duplica el tiempo típico hasta el evento". Ver [[modelo-parametrico-aft]].

- **Weibull** es la **única** distribución a la vez **PH y AFT**; log-logística/log-normal son AFT pero no PH.
- **HR<1 ↔ factor de aceleración >1** (mismo beneficio, escalas inversas: menos riesgo = más tiempo).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Una covariable cambia durante el seguimiento | Cox extendido con X(t) |
| Se viola PH y quiero modelar el efecto | Cox extendido (covariable×tiempo) |
| Necesito predecir/extrapolar S(t) o la media | Modelo paramétrico |
| Pienso el efecto en escala de tiempo | AFT (factor de aceleración) |
| ¿Forma del hazard? | Exponencial=plano, Weibull=monótono, log-logística=joroba |

---

> **Síntesis:** el **Cox extendido** incorpora covariables **tiempo-dependientes** (o modela la no-PH con X×g(t)), y el HR pasa a depender del tiempo —cuidado con usar info futura. Los modelos **paramétricos** asumen una distribución (exponencial/Weibull/log-logística) y permiten **predecir/extrapolar**; el marco **AFT** describe el efecto como un **factor de aceleración** del tiempo. La **Weibull** es la única PH y AFT a la vez.

---

*Retrieval: (1) dos usos del Cox extendido; (2) ¿qué precaución con variables tiempo-dependientes?; (3) hazard de exponencial/Weibull/log-logística; (4) ¿qué es el factor de aceleración y por qué Weibull es especial?*
