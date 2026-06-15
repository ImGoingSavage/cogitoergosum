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

## Mini-ejemplo trabajado: cómo el immortal time infla al tratado

Defines "tratado" = quien recibió el fármaco *en algún momento* del seguimiento. Pero para recibirlo hay que **seguir vivo** hasta la receta. Toma a un paciente que muere el día 10 sin alcanzar la receta: queda en el grupo "no tratado". Otro que sobrevive hasta el día 30 y entonces se trata aporta sus 30 días al grupo "tratado" — **incluidos los días 1–30 en que aún no tomaba nada**. Ese tramo "inmortal" (no podías morir tratado porque aún no lo estabas) se cuenta como tiempo-tratado-sin-eventos → la supervivencia del grupo tratado sale **artificialmente alta**. Con números: si repartes mal 20 días-persona inmortales por paciente, el "beneficio" puede ser puro artefacto.

**La corrección:** alinea el **tiempo cero** (elegibilidad, asignación a estrategia e inicio del seguimiento en el mismo instante) o clasifica el person-time como tratado *solo desde* que empieza el tratamiento. Es el mismo error que mirar el futuro al construir una feature.

**Predicción antes de seguir:** si en vez de "alguna vez tratado" usaras un **new-user design** (clasificas al inicio, t=0 alineado), ¿desaparece el sesgo? Sí: nadie acumula tiempo inmortal porque el reloj arranca con la decisión.

## Prototipo, contraejemplo y caso borde

- **Prototipo (g-métodos):** tratamiento que cambia en el tiempo con feedback L_t → ponderas por la historia (IP weighting de un MSM) en vez de condicionar.
- **Contraejemplo (per-protocol ingenuo):** comparar "adherentes vs no adherentes" parece la pregunta clínica, pero la adherencia no está aleatorizada → confundimiento post-aleatorización; sesgado salvo con g-métodos.
- **Caso borde (hazard ratio tardío):** un HR que cruza 1 con el tiempo suele ser **depleción de susceptibles** (los frágiles ya murieron), no un efecto que cambia — por eso se prefiere riesgo a tiempo fijo.

## Errores típicos

- **Conceptual:** ajustar por un confundidor tiempo-variable L_t con regresión estándar cuando L_t también es mediador del tratamiento pasado → sesga el efecto total y abre collider a la vez (no se arregla condicionando).
- **De diseño:** usuario prevalente (incluir a quienes ya llevaban años con el fármaco) → seleccionas sobrevivientes/tolerantes.
- **De interpretación:** leer el ITT diluido como "el fármaco no sirve" cuando lo que hubo fue baja adherencia.

## Transferencia isomorfa

La inferencia longitudinal tiene gemelos directos en ML systems:

- **Feedback tratamiento-confundidor ↔ feedback loops del modelo:** un recomendador cuyas predicciones moldean los clics que luego lo entrenan es exactamente A_{t-1}→L_t→Y_t; ignorarlo sesga como el confounding tiempo-variable (conecta con [[arena-htd2]], feedback loops).
- **Immortal time ↔ data leakage temporal / look-ahead:** contar person-time que "no podía tener el evento" es la versión clínica de usar información del futuro al construir una feature (conecta con [[arena-dmls1]]).
- **Target trial ↔ diseñar una eval offline fiel a la política online:** especificar el ensayo hipotético y emularlo es como definir el experimento que tu evaluación offline pretende imitar.

Moraleja de la arista: *cuando el tiempo entra, "ajustar" puede sesgar; pondera por la historia (g-métodos) y alinea siempre el t=0 — el immortal time es leakage con bata blanca.*

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
