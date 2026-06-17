# Análisis de supervivencia III: Cox extendido y modelos paramétricos/AFT

## De qué trata esta lección (y qué sabrás hacer al final)

El Cox básico asume un efecto que no cambia con el tiempo y deja el riesgo base sin especificar. ¿Qué haces cuando una covariable **sí cambia** (un trasplante ocurre a mitad del seguimiento) o cuando quieres **predecir y extrapolar** la supervivencia más allá de tus datos? Esta lección construye, desde cero, las extensiones: el **Cox extendido** (covariables tiempo-dependientes), los **modelos paramétricos** (que asumen una forma del tiempo a cambio de poder extrapolar) y el marco **AFT**, que mide el efecto sobre el *tiempo de vida* en vez de sobre el hazard —a menudo más intuitivo—.

Al terminar podrás: (1) usar el Cox extendido para covariables cambiantes o para modelar la no-PH, cuidando no mirar el futuro; (2) elegir una distribución paramétrica (exponencial/Weibull/log-logística) según la forma del hazard; (3) interpretar un factor de aceleración AFT ("duplica el tiempo típico"); y (4) entender por qué la Weibull es la única a la vez PH y AFT. Continúa el Cox de [[arena-h8]]. *(Ejemplos clínicos ilustran el método, no son consejo médico.)*

## Cox extendido (covariables tiempo-dependientes)

**h(t,X(t)) = h₀(t)·exp[Σ βᵢXᵢ + Σ δⱼXⱼ(t)].** Dos usos:
1. Covariables **genuinamente cambiantes** (estatus de trasplante, laboratorios repetidos).
2. **Modelar la no-PH** con interacciones covariable×g(t) (X·t, X·ln t): si δ es significativo, el efecto depende del tiempo.

Con términos tiempo-dependientes el **HR ya no es constante** (se evalúa en un instante). **Precaución:** la covariable en t solo usa información **hasta t**; usar el futuro = **immortal time bias**. Se implementa partiendo el tiempo en intervalos (start, stop] con el valor actual. Ver cox-extendido-tiempo-dependiente.

## Modelos paramétricos

Asumen una **distribución** del tiempo (modelan todo el hazard, a diferencia del Cox):
- **Exponencial:** hazard **constante** λ; S(t)=exp(−λt).
- **Weibull:** hazard **monótono** (creciente si forma p>1, decreciente si p<1; p=1 → exponencial).
- **Log-logística / log-normal:** hazard **no monótono** (sube y baja).

Ventajas: estimación más **eficiente** (si la forma es correcta), **predicción** de tiempos/percentiles y **extrapolación** más allá del seguimiento. Desventaja: **sesgo** si la distribución es errónea. Validar con diagnósticos (Weibull: ln(−ln Ŝ) vs ln t lineal), AIC, comparación con KM.

## AFT (Accelerated Failure Time)

Modela el efecto sobre el **TIEMPO** de supervivencia, no sobre el hazard: un **factor de aceleración** γ **estira** (γ>1, alarga la vida) o **encoge** (γ<1) el eje del tiempo. En ln T = α + γᵀX + error, el factor = exp(coef). Intuición: γ=2 ⇒ "duplica el tiempo típico hasta el evento". Ver modelo-parametrico-aft.

- **Weibull** es la **única** distribución a la vez **PH y AFT**; log-logística/log-normal son AFT pero no PH.
- **HR<1 ↔ factor de aceleración >1** (mismo beneficio, escalas inversas: menos riesgo = más tiempo).

---

## Mini-ejemplo trabajado: el factor de aceleración (AFT) frente al HR

Dos lentes para el mismo beneficio. Un fármaco con **HR = 0.5** dice "en cada instante, la mitad de la tasa de fallo". Un modelo **AFT** con factor de aceleración **γ = 2** dice "estira el reloj ×2": si la mediana de supervivencia sin tratamiento es 10 meses, **con** tratamiento es 20.

Las dos miran lo mismo desde escalas inversas (menos *riesgo* = más *tiempo*), pero el AFT es a menudo más intuitivo de comunicar a un clínico: "duplica el tiempo típico hasta el evento" se entiende mejor que "halve the hazard". En `ln T = α + γᵀX + error`, el factor es exp(coef): un coeficiente de ln(2)=0.69 → ×2 de tiempo.

**Predicción antes de seguir:** ¿por qué la Weibull es especial? Porque es la **única** distribución que se deja leer *a la vez* como HR (proporcional) y como factor de aceleración; en log-logística un mismo efecto solo tiene interpretación AFT (su hazard sube y baja, no es proporcional).

## Prototipo, contraejemplo y caso borde

- **Prototipo (covariable tiempo-dependiente legítima):** estado de trasplante que cambia el día del trasplante → entra al modelo solo *desde* ese día.
- **Contraejemplo (immortal time):** clasificar a alguien como "trasplantado" *desde el inicio* le regala los días previos sin evento → sesgo. Parece una covariable inocente, es leakage temporal.
- **Caso borde (forma del hazard mal elegida):** ajustar exponencial (hazard plano) a un proceso de desgaste (hazard creciente) → predicciones sesgadas; el diagnóstico ln(−ln Ŝ) vs ln t lo delata.

## Errores típicos

- **Conceptual:** reportar "el HR" de un Cox extendido como si fuera constante — con términos X×t el HR **depende del instante**.
- **Técnico:** construir la covariable tiempo-dependiente con información del futuro (immortal time); se evita partiendo el tiempo en intervalos (start, stop].
- **De supuestos:** elegir un paramétrico por eficiencia y olvidar validar la distribución (AIC, comparación con KM).

## Transferencia isomorfa

El AFT y las covariables tiempo-dependientes tienen gemelos en ingeniería y ML:

- **Factor de aceleración ↔ speedup / escala de tiempo:** "esta optimización hace el job 2× más rápido" es exactamente un γ=2 sobre el eje temporal.
- **X(t) usa solo info hasta t ↔ features sin look-ahead:** la regla de oro del Cox extendido es la misma que evita leakage en features de series de tiempo (conecta con [[arena-h6]] y [[arena-dmls1]]).
- **Paramétrico para extrapolar ↔ asumir una forma para predecir fuera del rango:** ganas extrapolación a cambio de sesgo si la forma es falsa — el mismo trade-off bias-varianza de elegir una familia de modelos.

Moraleja de la arista: *el AFT mide el efecto en tiempo (intuitivo), el Cox en hazard; y toda covariable que cambia en el tiempo solo puede mirar el pasado, nunca el futuro.*

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
