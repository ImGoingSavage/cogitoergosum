# The Mixtape I: resultados potenciales y sesgo de selección

> El **toolkit cuasi-experimental econométrico** de Cunningham. Complementa [[arena-h3]] (What If) y [[arena-h15]] (Pearl) con la mirada de economía: matching, IV/2SLS, RDD, DiD, panel, control sintético.

## De qué trata esta lección (y qué sabrás hacer al final)

¿Por qué a veces "los tratados resultan peor" cuando el tratamiento en realidad ayuda? Esta lección construye, desde cero, la respuesta que vertebra toda la inferencia causal observacional: el **sesgo de selección**. Con la notación de resultados potenciales descompone la ingenua diferencia de medias en su parte causal (el efecto) y su parte tramposa (la diferencia de base entre quienes se tratan y quienes no), y muestra que **aleatorizar significa, exactamente, igualar esa base**.

Al terminar podrás: (1) distinguir ATE, ATT y ATU y cuándo difieren; (2) enunciar las dos partes de SUTVA; (3) descomponer la diferencia naïve en efecto + sesgo de selección + sesgo heterogéneo; y (4) reconocer un tratamiento "endógeno" que pide un diseño cuasi-experimental. El ejemplo de 4 pacientes hace ver el sesgo a ojo. Es la puerta de entrada al toolkit econométrico de los lotes siguientes (matching, IV, RDD, DiD).

## Resultados potenciales

Cada unidad tiene **Y¹** (con tratamiento) e **Y⁰** (sin él); efecto individual δᵢ=Y¹ᵢ−Y⁰ᵢ. **Switching equation** Y = D·Y¹ + (1−D)·Y⁰: solo observamos uno (problema fundamental → datos faltantes).

**Estimandos:** **ATE** = E[Y¹−Y⁰] (todos), **ATT** = E[·|D=1] (tratados), **ATU** = E[·|D=0] (no tratados). Difieren si el efecto es **heterogéneo**.

**SUTVA:** (1) no interferencia entre unidades, (2) tratamiento bien definido. Lo viola, p. ej., la inmunidad de rebaño. Ver [[rubin-ate-att-atu-sutva]].

## La descomposición clave

$$\underbrace{E[Y|D{=}1]-E[Y|D{=}0]}_{\text{diferencia naïve}} = \text{ATE} + \underbrace{E[Y^0|D{=}1]-E[Y^0|D{=}0]}_{\text{sesgo de selección}} + \text{sesgo heterogéneo}$$

El **sesgo de selección** = cuánto difieren tratados y controles en el resultado **base** (sin tratamiento). Si los más graves se tratan, enmascara el efecto. La **aleatorización** ((Y¹,Y⁰)⊥D) anula ambos sesgos → la diferencia de medias = ATE. Toda la inferencia causal observacional busca eliminar el sesgo de selección. Ver [[descomponer-comparacion-naive]].

Un tratamiento es **endógeno** si su asignación se relaciona con el outcome (sesgo); el objetivo es hallar variación **como-si exógena**. "No hay causación sin manipulación": define la intervención.

---

## Mini-ejemplo trabajado: ver el sesgo de selección con 4 pacientes

Tabla con *ambos* potenciales (en la vida real solo ves uno; aquí los inventamos para entender):

| Paciente | Y⁰ (sin tto) | Y¹ (con tto) | δ = Y¹−Y⁰ | Recibe tto (D) |
|---|---|---|---|---|
| Grave 1 | 20 | 30 | +10 | sí |
| Grave 2 | 30 | 40 | +10 | sí |
| Leve 1 | 70 | 80 | +10 | no |
| Leve 2 | 80 | 90 | +10 | no |

El **efecto real es +10 para todos** (homogéneo → ATE=ATT=+10). Pero la diferencia naïve que un analista calcularía es:

media(tratados observados Y¹) − media(controles observados Y⁰) = (30+40)/2 − (70+80)/2 = 35 − 75 = **−40**.

¡El tratamiento parece **dañino** (−40) cuando en verdad ayuda (+10)! Todo el hueco es **sesgo de selección**: E[Y⁰|tratados] − E[Y⁰|controles] = 25 − 75 = −50. Los graves (peor base) recibieron el tratamiento. Suma: −50 (selección) + 10 (efecto) = −40. La aleatorización habría igualado el Y⁰ base de ambos grupos y devuelto +10.

**Predicción antes de seguir:** si en vez de tratar a los graves hubieras aleatorizado, ¿qué diferencia de medias esperarías? +10, porque E[Y⁰|D=1]=E[Y⁰|D=0] y el sesgo se anula.

## Prototipo, contraejemplo y caso borde

- **Prototipo (sin sesgo):** ensayo aleatorizado. D ⊥ (Y⁰,Y¹) → diferencia de medias = ATE.
- **Contraejemplo (parece causal, no lo es):** "los que tomaron el suplemento viven más". Si los sanos tienden a tomarlo, el Y⁰ base difiere → sesgo de selección disfrazado de efecto.
- **Caso borde (SUTVA):** una vacuna con inmunidad de rebaño viola "no interferencia" — el tratamiento de unos cambia el Y⁰ de otros, y ni la aleatorización salva el contraste ingenuo.

## Errores típicos

- **Conceptual:** confundir ATT con ATE cuando el efecto es heterogéneo (el efecto *sobre los tratados* no es el de la población).
- **De interpretación:** leer "los tratados resultan peor" como "el tratamiento daña", sin preguntar cómo estaban *de base*.
- **De supuestos:** asumir SUTVA en redes sociales/epidemias donde hay interferencia evidente.

## Transferencia isomorfa

La switching equation y el sesgo de selección reaparecen fuera de la epidemiología:

- **Off-policy en recomendadores ↔ datos faltantes:** solo observas la recompensa del ítem que *mostraste* (el Y de la acción tomada); estimar qué habría pasado con otro ítem es exactamente el problema del contrafactual no observado (conecta con [[arena-dmls1]]).
- **Uplift / marketing ↔ ATT vs ATE:** "¿a quién mover con el cupón?" es el efecto sobre los tratados, no el promedio poblacional.
- **Survivorship bias en Quant ↔ sesgo de selección:** comparar fondos vivos vs muertos sin igualar su riesgo base es el mismo E[Y⁰|D=1]≠E[Y⁰|D=0].

Moraleja de la arista: *toda inferencia causal observacional es un combate contra una sola cosa —el sesgo de selección— y "aleatorizar" significa "igualar el Y⁰ base de los grupos".*

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
