# Inferencia causal IV: longitudinal, supervivencia y target trial

> Complementa [[arena-h2]] (componentes del target trial / immortal time): aquí, tratamientos **tiempo-variables**, supervivencia causal y g-métodos.

## Supervivencia causal

El **hazard ratio** es problemático: el hazard en t condiciona en **haber sobrevivido** hasta t, y los sobrevivientes dejan de ser intercambiables (depleción de susceptibles) → **sesgo de selección incorporado** que crece con el tiempo. Prefiere contrastes de **riesgo/supervivencia a tiempo fijo** (diferencia/razón de riesgos a 1, 5 años; curvas ajustadas; supervivencia media restringida). La **censura** es un tratamiento tiempo-variable → **IPCW**. Ver [[analisis-supervivencia-hazard-vs-riesgo]].

## Tratamientos tiempo-variables y feedback

- **Intercambiabilidad secuencial:** en cada tiempo, comparabilidad dada la historia de tratamiento y covariables (Y^ā ⊥ A_t | Ā_{t-1}, L̄_t).
- **Feedback tratamiento-confundidor:** una covariable L_t es **confundidor** del tratamiento futuro **y** **mediador** del tratamiento pasado (A_{t-1}→L_t→Y). Los métodos tradicionales **fallan y no se pueden arreglar**: ajustar por L_t bloquea parte del efecto (mediador) y abre sesgo de collider; no ajustar deja confundimiento.
- **Solución: g-métodos** (g-fórmula, IP weighting de MSM, g-estimación), que **ponderan** (no condicionan) por la historia de confundidores. Ver [[confounding-tiempo-variable-gmetodos]].

## ITT vs per-protocol

- **ITT:** efecto de **asignar** una estrategia (respeta la aleatorización; con no adherencia **diluye** el efecto).
- **Per-protocol:** efecto de **seguir** la estrategia (pregunta clínica real). La adherencia NO está aleatorizada → confundimiento **post-aleatorización** tiempo-variable. Un per-protocol **ingenuo** (adherentes vs no) está sesgado; el correcto usa **g-métodos**. Ver [[itt-vs-per-protocol-estimando]].

## Emular un target trial (estrategias sostenidas)

Especifica el ECA hipotético y emula cada componente. Claves para evitar sesgos:
- **Alinear el tiempo cero** (elegibilidad, asignación a estrategia e inicio del seguimiento en el mismo instante) → evita **immortal time bias**.
- **New-user design** (solo nuevos usuarios) → evita **sesgo de usuario prevalente** (sobrevivientes/tolerantes).
- **Comparador activo** → reduce confundimiento por indicación.
- **Per-protocol con g-métodos**: censurar por desviación + IPCW/g-fórmula por confundidores en cada tiempo. Ver [[emular-target-trial-sostenido]].

Es el **caballo de batalla de la RWE**: convierte datos observacionales masivos (EHR, claims) en inferencia causal disciplinada.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Outcome de tiempo-hasta-evento | Riesgo/supervivencia a tiempo fijo, no un HR único |
| Tratamiento que cambia en el tiempo y depende de covariables que él afecta | Feedback → g-métodos |
| Pérdida de seguimiento | Censura como tratamiento → IPCW |
| No adherencia en un ensayo | ITT diluye; per-protocol con g-métodos |
| Estudio observacional tipo ensayo | Emular target trial: t=0 alineado, new-user, comparador activo |

---

> **Síntesis:** en supervivencia, evita el **hazard ratio** (selección incorporada) y usa **riesgo/supervivencia**. Con tratamientos tiempo-variables y **feedback tratamiento-confundidor** la regresión tradicional falla → usa **g-métodos**. El **ITT** mide asignar y el **per-protocol** seguir (necesita g-métodos). **Emular un target trial** (t=0 alineado, new-user, comparador activo, per-protocol con g-métodos) es la forma disciplinada de hacer **RWE**.

---

*Retrieval: (1) ¿por qué el HR es problemático?; (2) ¿qué es el feedback tratamiento-confundidor y por qué exige g-métodos?; (3) ITT vs per-protocol; (4) ¿cómo evita el target trial el immortal time y el usuario prevalente?*
