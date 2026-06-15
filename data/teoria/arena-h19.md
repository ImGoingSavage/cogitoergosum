# The Mixtape I: resultados potenciales y sesgo de selección

> El **toolkit cuasi-experimental econométrico** de Cunningham. Complementa [[arena-h3]] (What If) y [[arena-h15]] (Pearl) con la mirada de economía: matching, IV/2SLS, RDD, DiD, panel, control sintético.

## Resultados potenciales

Cada unidad tiene **Y¹** (con tratamiento) e **Y⁰** (sin él); efecto individual δᵢ=Y¹ᵢ−Y⁰ᵢ. **Switching equation** Y = D·Y¹ + (1−D)·Y⁰: solo observamos uno (problema fundamental → datos faltantes).

**Estimandos:** **ATE** = E[Y¹−Y⁰] (todos), **ATT** = E[·|D=1] (tratados), **ATU** = E[·|D=0] (no tratados). Difieren si el efecto es **heterogéneo**.

**SUTVA:** (1) no interferencia entre unidades, (2) tratamiento bien definido. Lo viola, p. ej., la inmunidad de rebaño. Ver [[rubin-ate-att-atu-sutva]].

## La descomposición clave

$$\underbrace{E[Y|D{=}1]-E[Y|D{=}0]}_{\text{diferencia naïve}} = \text{ATE} + \underbrace{E[Y^0|D{=}1]-E[Y^0|D{=}0]}_{\text{sesgo de selección}} + \text{sesgo heterogéneo}$$

El **sesgo de selección** = cuánto difieren tratados y controles en el resultado **base** (sin tratamiento). Si los más graves se tratan, enmascara el efecto. La **aleatorización** ((Y¹,Y⁰)⊥D) anula ambos sesgos → la diferencia de medias = ATE. Toda la inferencia causal observacional busca eliminar el sesgo de selección. Ver [[descomponer-comparacion-naive]].

Un tratamiento es **endógeno** si su asignación se relaciona con el outcome (sesgo); el objetivo es hallar variación **como-si exógena**. "No hay causación sin manipulación": define la intervención.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| ¿Qué efecto exacto busco? | ATE vs ATT vs ATU |
| "Los tratados resultan peor" | ¿Sesgo de selección (estaban peor de base)? |
| Vacuna / red social | ¿SUTVA? (interferencia entre unidades) |
| Tratamiento endógeno | Busca variación exógena (matching/IV/RDD/DiD) |
| Atributo inmutable (raza) | Sin manipulación clara, el contrafactual es ambiguo |

---

> **Síntesis:** el efecto causal es un contraste **Y¹−Y⁰** que solo se observa a medias (switching equation); se promedia en **ATE/ATT/ATU** bajo **SUTVA**. La diferencia naïve = **ATE + sesgo de selección + sesgo heterogéneo**; la **aleatorización** los anula. Todo diseño observacional busca neutralizar el **sesgo de selección** convirtiendo un tratamiento endógeno en uno como-si exógeno.

---

*Retrieval: (1) ATE vs ATT vs ATU; (2) las dos partes de SUTVA; (3) descompón la diferencia naïve; (4) ¿qué es el sesgo de selección?*
