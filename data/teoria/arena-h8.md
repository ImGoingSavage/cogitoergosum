# Análisis de supervivencia II: modelo de Cox y supuesto PH

## De qué trata esta lección (y qué sabrás hacer al final)

Kaplan-Meier compara grupos enteros, pero ¿cómo mides el efecto de una covariable *ajustando por otras*, sin comprometerte con la forma exacta del riesgo en el tiempo? Esta lección construye, desde cero, la respuesta más usada de toda la bioestadística: el **modelo de Cox**, que entrega un **hazard ratio** limpio porque deja el riesgo base *sin especificar* y lo cancela en el cociente. Su precio es un supuesto —**hazards proporcionales (PH)**, que el efecto no derive con el tiempo— que hay que verificar siempre.

Al terminar podrás: (1) leer un HR como una razón de tasas instantáneas a igualdad de las demás covariables; (2) entender por qué el hazard base se cancela y qué hace la verosimilitud parcial; (3) evaluar el supuesto PH de tres formas (log-log, Schoenfeld, interacción×tiempo); y (4) saber qué hacer si se viola (Cox estratificado o extendido). El ejemplo de "fumar, HR≈2" hace de hilo. Profundiza la mecánica de [[arena-h7]]. *(Ejemplos clínicos ilustran el método, no son consejo médico.)*

## El modelo de Cox

**h(t,X) = h₀(t)·exp(β₁X₁+…+βₚXₚ).** El **hazard base** h₀(t) (cuando todas X=0) queda **sin especificar**; el factor exp(ΣβⱼXⱼ) lo escala según las covariables y **no depende del tiempo**.

- **Semiparamétrico:** parte paramétrica (β) + h₀(t) libre → flexible y robusto, muy popular.
- **Hazard ratio:** HR = exp(β·Δx); binaria → **HR=exp(β)** (>1 más riesgo, <1 protector). El h₀(t) se cancela en el cociente.
- **Verosimilitud parcial:** estima los β usando solo el **orden** de los eventos y los risk sets, sin h₀(t).
- Permite **curvas de supervivencia ajustadas**: Ŝ(t,X)=Ŝ₀(t)^exp(ΣβⱼXⱼ). Ver modelo-cox-ph.

**Significancia:** razón de verosimilitud (bloques/modelos anidados), Wald (coef. sueltos), score.

## El supuesto de hazards proporcionales (PH)

**El HR es constante en el tiempo** (los hazards de los grupos son proporcionales ⇔ curvas log(−log S) **paralelas**). Si el efecto de una covariable cambia con el tiempo, se **viola** PH y un único HR es engañoso.

### Tres formas de evaluarlo
1. **Gráfica:** log(−log Ŝ(t)) por categoría → deben ser **paralelas**; si se **cruzan**, no-PH.
2. **GOF / residuos de Schoenfeld:** ¿correlacionan con el tiempo? Significativo ⇒ no-PH.
3. **Variable tiempo-dependiente:** añadir covariable×g(t) (p. ej. X·ln t) y testear; significativo ⇒ HR depende de t. Ver evaluar-supuesto-ph.

### Si se viola PH
- **Cox estratificado** (controlar una variable sin estimar su HR).
- **Cox extendido** con término tiempo-dependiente (modelar el efecto cambiante).

## Cox estratificado

Cada estrato g recibe su **propio h₀g(t)**, con β **compartidos** (modelo sin interacción). **No** da HR para la variable de estratificación. Modelo **con interacción** = β distintos por estrato; se decide con **prueba de razón de verosimilitud**. Ver cox-estratificado.

---

## Mini-ejemplo trabajado: leer un HR

Un Cox da β = **0.69** para "fuma (sí/no)". El hazard ratio es HR = exp(0.69) ≈ **2.0**: en cualquier instante, un fumante tiene *el doble* de tasa de fallo que un no fumante, **a igualdad de las demás covariables**. Si en vez de binaria fuera "cigarros/día" con β=0.05, el HR por **10** cigarros es exp(0.05·10) = exp(0.5) ≈ **1.65**.

Lo crucial: el HR es el **mismo a t=1 mes y a t=5 años** — eso *es* el supuesto PH. El hazard base h₀(t) puede subir o bajar con el tiempo (la gente se muere más con la edad), pero **se cancela en el cociente**, por eso el Cox no necesita especificarlo (verosimilitud parcial: usa solo el orden de los eventos).

**Predicción antes de seguir:** si el efecto de fumar fuera enorme a los 60 años pero nulo a los 30, ¿qué pasa con un único HR? Es engañoso (promedia dos efectos distintos) → PH **violado**; lo verías en curvas log(−log S) que **se cruzan**.

### [CAJA NEGRA OK] Verosimilitud parcial de Cox

- **Qué puedes asumir:** estima los β usando solo el *orden* de los eventos y quién está en riesgo en cada uno, sin tocar h₀(t).
- **Por qué se permite:** la derivación formal (procesos de conteo, martingalas) no cambia cómo la usas ni la interpretas en entrevista.
- **Qué sí debes razonar:** que h₀(t) se cancela en el HR, y que por eso el Cox es *semiparamétrico* (β paramétrico + base libre).
- **Intuición mínima:** "comparo, en cada muerte, al que murió contra los que seguían vivos" → el ranking, no los tiempos exactos.
- **Cuándo reabrir la caja:** al estudiar residuos de martingala/Schoenfeld formalmente.

## Prototipo, contraejemplo y caso borde

- **Prototipo (PH se sostiene):** efecto multiplicativo estable → un HR resume todo; curvas log-log paralelas.
- **Contraejemplo (PH violado):** un tratamiento quirúrgico que mata al principio (riesgo operatorio) y protege después → los hazards se cruzan; un HR único miente.
- **Caso borde (HR≈1, IC amplio):** no es "no hay efecto", es **faltan eventos** (potencia); la incertidumbre, no la nulidad, manda.

## Errores típicos

- **Conceptual:** interpretar el HR como un *riesgo* o una *razón de tiempos* — es una razón de **tasas instantáneas**.
- **De supuestos:** reportar el HR sin verificar PH (log-log / Schoenfeld / X×t).
- **Técnico:** estratificar por la variable de interés y luego buscar su HR (el Cox estratificado no lo da).

## Transferencia isomorfa

El Cox es un modelo multiplicativo con un supuesto de estabilidad temporal — patrón que reaparece:

- **HR constante ↔ efecto relativo estable en A/B:** asumir que un tratamiento multiplica la tasa por un factor fijo en el tiempo es el mismo "PH" implícito en muchos análisis de experimentos longitudinales.
- **Residuos de Schoenfeld ↔ chequear estabilidad de un coeficiente:** "¿el efecto de esta feature deriva con el tiempo?" es el mismo diagnóstico que el de PH (conecta con drift de modelo, [[arena-dmls4]]).
- **Verosimilitud parcial por ranking ↔ pérdidas de ranking (pairwise):** estimar usando solo el orden de los eventos es pariente de las pérdidas tipo ranking en ML.

Moraleja de la arista: *el Cox da un HR limpio porque el hazard base se cancela; ese regalo depende de que el efecto no derive con el tiempo (PH) — siempre verifícalo.*

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
