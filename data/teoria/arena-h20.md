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

## Intuición: el propensity score *colapsa* muchas X en un número

Antes de la fórmula, la idea: si tuvieras que emparejar pacientes por edad, sexo, peso, presión, glucosa… nunca encontrarías dos idénticos (la maldición de la dimensionalidad). El **propensity score** e(X)=P(D=1|X) resume *toda* esa X en una sola cifra — "la probabilidad de que a este paciente lo trataran" — y basta equilibrar **ese número** para equilibrar las X que lo componen. Analogía: en vez de comparar dos casas por 30 atributos, comparas su *precio estimado*, que ya los condensa.

## Mini-ejemplo trabajado: subclasificación a mano

Confundidor edad con dos estratos. Tasa de recuperación (con − sin tratamiento):

- **Jóvenes** (60% de la población): 0.80 − 0.70 = **+0.10**.
- **Viejos** (40% de la población): 0.50 − 0.30 = **+0.20**.

- **ATE** (pondera por la población P(z)): 0.6·0.10 + 0.4·0.20 = **+0.14**.
- **ATT** (pondera por la composición de los *tratados*; supón que el 80% de los tratados son viejos): 0.2·0.10 + 0.8·0.20 = **+0.18**.

Mismo dato, dos estimandos distintos: el efecto *promedio* (+0.14) y el efecto *sobre quienes de hecho se tratan* (+0.18). El propensity score haría esto sin estratos discretos, pero la lógica de "promediar efectos por estrato con los pesos correctos" es idéntica (conecta con [[arena-h19]], ATE vs ATT).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** buen **overlap** — para cada e(X) hay tratados y controles → emparejas y estimas sin extrapolar.
- **Contraejemplo (positividad rota):** un estrato donde *todos* se trataron (e(X)=1) no tiene control con quién compararse; el método "funciona" en código pero el efecto ahí es **inidentificable**, no cero.
- **Caso borde (matching exacto):** con muchas X continuas no hay dos iguales → necesitas PS o coarsening; el borde revela *por qué* existe el propensity score.

## Errores típicos

- **Conceptual:** creer que un PS bien estimado arregla un **confundidor no medido**. El PS solo equilibra las X que *metes*; si falta una, el sesgo persiste (CIA sigue siendo indemostrable).
- **Técnico:** no verificar **balance** (SMD<0.1) tras emparejar, ni el **soporte común** antes.
- **De interpretación:** reportar el ATT y llamarlo ATE (o viceversa) — los pesos importan.

## Transferencia isomorfa

Ponderar por el propensity score es la misma maquinaria que en ML/Quant:

- **IPW ↔ off-policy evaluation (IPS):** estimar el valor de una política nueva reponderando los logs por 1/propensión de la política vieja es *idéntico* al inverse-probability weighting causal (conecta con [[arena-dmls1]]).
- **Overlap/positividad ↔ covariate shift:** exigir que tratados y controles cubran el mismo rango de X es el mismo requisito que "train y test comparten soporte" en domain adaptation.
- **Matching ↔ nearest-neighbor join:** emparejar por distancia en e(X) es un join por vecino más cercano sobre una clave de baja dimensión.

Moraleja de la arista: *un balancing score convierte un problema de muchas dimensiones en uno de una; pero solo equilibra lo que mides, nunca lo que ignoras.*

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
