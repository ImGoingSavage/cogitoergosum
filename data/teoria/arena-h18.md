# La causalidad según Pearl IV: contrafactuales y mediación

## Contrafactuales (peldaño 3)

'¿Qué **habría** pasado con Y para ESTE caso si X hubiera sido distinto, dado lo observado?'. No se obtienen ni con datos (peldaño 1) ni con experimentos (peldaño 2, que dan **promedios**): un contrafactual es sobre un **individuo** en un mundo que no ocurrió. Requiere un **Modelo Causal Estructural (SCM)**.

### SCM y el algoritmo de 3 pasos
Un SCM = ecuaciones causa→efecto + términos de error **U** (lo idiosincrático de cada unidad). Para computar un contrafactual:
1. **Abducción:** usar la evidencia observada para actualizar los **U** (qué tipo de caso es).
2. **Acción:** modificar el modelo con do() (imponer el antecedente hipotético).
3. **Predicción:** recalcular Y con esos U.

El contrafactual de Pearl **equivale** al **potential outcome** Y_x de Neyman-Rubin: mismo concepto, dos lenguajes. Ver [[contrafactual-modelo-estructural]].

## Mediación

Descompone el efecto de X sobre Y en **directo** (X→Y) e **indirecto** (X→M→Y) — el *mecanismo*, no solo el cuánto.
- **Baron-Kenny** (producto de coeficientes) solo vale **sin interacción ni no linealidad**.
- **Efectos naturales** (contrafactuales): **NDE** (mueve X con M congelado en su valor natural) y **NIE** (mueve M como respondería a X, con X fijo) → descomposición correcta con interacciones.
- Identificar mediación exige **más supuestos**: desconfundir también M-Y (y sin confundidores de M-Y afectados por X). Ver [[analisis-mediacion-efectos]].

## Causa necesaria vs suficiente

- **PN (probabilidad de necesidad):** ¿Y NO habría ocurrido **sin** X? — causalidad **'but-for'**, central en lo **legal** (atribuir culpa).
- **PS (probabilidad de suficiencia):** ¿X **bastaría** para producir Y? — relevante para **prevención/políticas**.

Estimables combinando datos **experimentales + observacionales** bajo supuestos. Aplicaciones: responsabilidad legal, atribución del cambio climático. Ver [[causa-necesaria-suficiente]].

---

## Mini-ejemplo trabajado: descomponer un efecto en directo e indirecto

Un programa de ejercicio X baja la presión Y, en parte directamente y en parte porque hace **perder peso** M. SCM lineal sencillo: M = 2·X (cada unidad de ejercicio quita 2 de peso), Y = −1·X − 0.5·M (el ejercicio baja Y directo, y el peso también).

- **Efecto indirecto (NIE)** X→M→Y: mueves M como respondería a X (2 por unidad), con X fijo: −0.5 · 2 = **−1**.
- **Efecto directo (NDE)** X→Y con M congelado: el coeficiente directo = **−1**.
- **Efecto total** = NDE + NIE = −1 + (−1) = **−2** por unidad de X.

La mitad del beneficio viaja por el peso, la mitad es directo. Eso es *mecanismo*, no solo magnitud — y Baron-Kenny (producto de coeficientes) coincide aquí **solo** porque no hay interacción; en cuanto el efecto del peso dependa del nivel de ejercicio, hay que usar NDE/NIE.

**Predicción antes de seguir:** si una pastilla bloqueara la pérdida de peso (congela M en su valor sin tratamiento), ¿cuánto bajaría Y? Solo el NDE = −1: matas el canal indirecto.

## Prototipo, contraejemplo y caso borde

- **Prototipo (contrafactual individual):** abducción (¿qué tipo de caso es, dados sus U?) → acción (impón el antecedente con do) → predicción. Da el "¿habría…?" de un individuo.
- **Contraejemplo (Baron-Kenny con interacción):** si X y M interactúan, el producto de coeficientes da una descomposición errónea; parece mediación clásica pero no lo es.
- **Caso borde (mediación con confundidor de M-Y afectado por X):** ni siquiera NDE/NIE se identifican sin supuestos extra — el caso que marca el límite del método.

## Errores típicos

- **Conceptual:** creer que un experimento (peldaño 2) responde un contrafactual individual (peldaño 3) — el RCT da promedios, no el "para este caso".
- **De supuestos:** estimar mediación sin desconfundir también la relación **M→Y**.
- **De interpretación:** confundir PN ('but-for', ¿sin X no habría pasado?) con PS (¿X basta para causarlo?) — la justicia usa PN, la prevención usa PS.

## Transferencia isomorfa

Contrafactuales y mediación son herramientas de ML interpretable y producto:

- **PN / 'but-for' ↔ explicación contrafactual:** "¿cuál es el cambio mínimo en las features que habría volteado la decisión del modelo?" es exactamente una pregunta but-for sobre el clasificador (conecta con [[arena-iml4]], métodos tipo SHAP/contrafactuales).
- **NDE/NIE ↔ atribución por caminos:** descomponer una predicción en la contribución *directa* de una feature vs la que pasa por features derivadas es el análogo de directo/indirecto.
- **Abducción→acción→predicción ↔ simulación what-if:** los gemelos digitales y los simuladores de política hacen el mismo bucle: inferir el estado latente, intervenir, repredecir.

Moraleja de la arista: *un contrafactual es "imaginar este caso en otro mundo"; mediación dice por qué canal viaja el efecto, y PN/PS separan culpar de prevenir.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿Habría pasado si…?" (un caso) | Contrafactual (peldaño 3): SCM + abducción/acción/predicción |
| Y_x (Rubin) vs contrafactual (Pearl) | Mismo concepto, dos lenguajes |
| ¿Por qué vía X afecta a Y? | Mediación: directo + indirecto (NDE/NIE) |
| Mediación con interacción | Baron-Kenny falla; usa efectos naturales |
| Atribución/responsabilidad (legal) | Probabilidad de necesidad (PN, 'but-for') |
| Prevención: ¿basta la causa? | Probabilidad de suficiencia (PS) |

---

> **Síntesis:** los **contrafactuales** (peldaño 3) requieren un **SCM** y el algoritmo **abducción→acción→predicción**; equivalen a los **potential outcomes** Y_x. La **mediación** separa efecto directo e indirecto (usa **NDE/NIE**, no Baron-Kenny con interacción) y exige desconfundir también M-Y. La causalidad **necesaria (PN, 'but-for'/legal)** y **suficiente (PS/prevención)** formaliza la atribución, estimable combinando experimento y observación.

---

*Retrieval: (1) los 3 pasos para computar un contrafactual; (2) ¿contrafactual de Pearl vs potential outcome?; (3) ¿por qué Baron-Kenny falla y qué usar?; (4) PN vs PS.*
