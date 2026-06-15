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
