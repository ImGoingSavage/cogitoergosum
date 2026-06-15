# The Mixtape II: matching, subclasificación y propensity score

## Selección en observables (CIA)

El **supuesto de independencia condicional (CIA)** —ignorabilidad, unconfoundedness, "selección en observables"—: **(Y¹,Y⁰) ⊥ D | X**. Condicionando en las covariables observadas X, el tratamiento es independiente de los resultados potenciales (X cierra todos los caminos traseros; no hay confundimiento no observado). Es lo que justifica matching, subclasificación, propensity score y regresión. Es **fuerte y NO testeable**: si hay un confundidor no medido, todos fallan → de ahí los diseños IV/RDD/DiD. Ver [[supuesto-seleccion-en-observables-cia]].

## Matching y subclasificación

- **Subclasificación:** estratificar por X, estimar el efecto en cada estrato y promediar (por población→ATE, por tratados→ATT).
- **Matching exacto:** aparear tratados con controles idénticos en X → **maldición de la dimensionalidad** (con muchas X continuas no hay matches exactos).
- **Matching aproximado** (vecino más cercano por distancia): introduce **sesgo** de emparejamiento → corregir con ajuste de regresión (bias-corrected). **Coarsened exact matching**: discretizar y emparejar exacto. Ver [[matching-subclasificacion]].

## Propensity score

**e(X)=P(D=1|X)**: balancing score que resume X en una dimensión → condicionar/emparejar/ponderar (**IPW**, 1/e(X)) por él equilibra X y vence la dimensionalidad. Requiere **soporte común** (overlap: tratados y controles en el mismo rango) y verificar **balance** (SMD<0.1) tras el ajuste. Ver [[propensity-score]].

**Matching ≠ regresión:** matching **no extrapola** (solo soporte común) y no impone forma funcional; la regresión extrapola e impone linealidad. Caso **Lalonde/Dehejia-Wahba**: el PS matching funciona si el CIA es plausible, hay overlap y balance.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| ¿Puedo medir todos los confundidores? | Si sí (CIA), matching/PS/regresión; si no, IV/RDD/DiD |
| Muchas covariables continuas | Propensity score (resume X) |
| ¿El ajuste es creíble? | Verifica overlap + balance (SMD<0.1) |
| Relación no lineal / extrapolación | Matching (no extrapola) > regresión lineal |
| Estrato sin tratados o sin controles | Falta soporte común (positividad) |

---

> **Síntesis:** matching, subclasificación, propensity score y regresión estiman el efecto bajo el **CIA** ((Y¹,Y⁰)⊥D|X), un supuesto fuerte e indemostrable. El **propensity score** resume X en una dimensión y vence la maldición de la dimensionalidad; hay que verificar **soporte común** y **balance**. El matching **no extrapola** (vs regresión), pero todos comparten la fragilidad: un confundidor no observado los sesga.

---

*Retrieval: (1) enuncia el CIA y por qué no es testeable; (2) ¿qué es la maldición de la dimensionalidad en matching?; (3) ¿qué resume el propensity score?; (4) matching vs regresión.*
