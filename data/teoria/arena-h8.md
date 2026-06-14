# Análisis de supervivencia II: modelo de Cox y supuesto PH

## El modelo de Cox

**h(t,X) = h₀(t)·exp(β₁X₁+…+βₚXₚ).** El **hazard base** h₀(t) (cuando todas X=0) queda **sin especificar**; el factor exp(ΣβⱼXⱼ) lo escala según las covariables y **no depende del tiempo**.

- **Semiparamétrico:** parte paramétrica (β) + h₀(t) libre → flexible y robusto, muy popular.
- **Hazard ratio:** HR = exp(β·Δx); binaria → **HR=exp(β)** (>1 más riesgo, <1 protector). El h₀(t) se cancela en el cociente.
- **Verosimilitud parcial:** estima los β usando solo el **orden** de los eventos y los risk sets, sin h₀(t).
- Permite **curvas de supervivencia ajustadas**: Ŝ(t,X)=Ŝ₀(t)^exp(ΣβⱼXⱼ). Ver [[modelo-cox-ph]].

**Significancia:** razón de verosimilitud (bloques/modelos anidados), Wald (coef. sueltos), score.

## El supuesto de hazards proporcionales (PH)

**El HR es constante en el tiempo** (los hazards de los grupos son proporcionales ⇔ curvas log(−log S) **paralelas**). Si el efecto de una covariable cambia con el tiempo, se **viola** PH y un único HR es engañoso.

### Tres formas de evaluarlo
1. **Gráfica:** log(−log Ŝ(t)) por categoría → deben ser **paralelas**; si se **cruzan**, no-PH.
2. **GOF / residuos de Schoenfeld:** ¿correlacionan con el tiempo? Significativo ⇒ no-PH.
3. **Variable tiempo-dependiente:** añadir covariable×g(t) (p. ej. X·ln t) y testear; significativo ⇒ HR depende de t. Ver [[evaluar-supuesto-ph]].

### Si se viola PH
- **Cox estratificado** (controlar una variable sin estimar su HR).
- **Cox extendido** con término tiempo-dependiente (modelar el efecto cambiante).

## Cox estratificado

Cada estrato g recibe su **propio h₀g(t)**, con β **compartidos** (modelo sin interacción). **No** da HR para la variable de estratificación. Modelo **con interacción** = β distintos por estrato; se decide con **prueba de razón de verosimilitud**. Ver [[cox-estratificado]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Efecto (HR) ajustado por covariables | Modelo de Cox |
| ¿Mi HR es válido para todo t? | Verifica PH (log-log / Schoenfeld / ×tiempo) |
| Una variable de control viola PH | Cox estratificado (sin HR para ella) |
| El efecto cambia con el tiempo y me interesa | Cox extendido (tiempo-dependiente) |
| HR≈1 con IC amplio | Inconcluso: faltan eventos, no "no efecto" |

---

> **Síntesis:** el **Cox** modela h(t,X)=h₀(t)exp(βX), da el **HR=exp(β)** vía **verosimilitud parcial** sin asumir h₀(t). Su supuesto es **PH** (HR constante), evaluable con **log-log / Schoenfeld / interacción×tiempo**; si se viola, **estratificar** (controlar) o **Cox extendido** (modelar). El **Cox estratificado** da baselines por estrato pero no HR del estratificador.

---

*Retrieval: (1) ¿qué es la verosimilitud parcial?; (2) define PH y cómo evaluarlo (3 formas); (3) ¿qué hace el Cox estratificado y su limitación?; (4) ¿estratificar vs Cox extendido?*
