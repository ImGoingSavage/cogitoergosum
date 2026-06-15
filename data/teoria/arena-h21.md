# The Mixtape III: variables instrumentales y regresión discontinua

> Diseños que rompen la dependencia del **CIA** ([[supuesto-seleccion-en-observables-cia]]) con variación **como-si exógena**.

## Variables instrumentales (2SLS)

Para un tratamiento **endógeno** (confundidor no medido o causalidad inversa), un **instrumento Z** aporta variación exógena. Ver [[variable-instrumental]].

**2SLS:** (1ª etapa) D ~ Z → D̂ (parte de D movida solo por Z); (2ª etapa) Y ~ D̂. Tres condiciones:
- **Relevancia** (Z→D, testeable en la 1ª etapa).
- **Exclusión** (Z afecta Y solo vía D).
- **Independencia** (Z como-si aleatorio respecto a confundidores).

Bajo **monotonicidad** (sin defiers) estima el **LATE** (efecto en los **compliers**, no ATE). **Instrumentos débiles** (relevancia baja) amplifican sesgo y varianza → exige **F>10** en la 1ª etapa. La **forma reducida** (Y~Z) es diagnóstico: IV ≈ (Y~Z)/(D~Z). Ver [[instrumentos-debiles-2sls]].

## Regresión discontinua (RDD)

El tratamiento se asigna por un **umbral** (cutoff) en una **running variable**. Las unidades justo arriba/abajo son comparables (**aleatorización local**) → el **salto** en E[Y] en el cutoff es el efecto. Ver [[regresion-discontinua-rdd]].

- **Sharp:** cruzar el umbral **determina** el tratamiento (0→1); efecto = salto en Y.
- **Fuzzy:** cambia la **probabilidad** de tratamiento → se estima por **IV** (cutoff como instrumento); LATE en el umbral.

**Supuestos/diagnósticos:** **no manipulación** (test de densidad de **McCrary**: sin bunching en el cutoff), **continuidad** de potenciales y covariables (placebo de covariables, cutoffs falsos), **bandwidth** (sesgo↔varianza) y **polinomios locales** de bajo grado (no globales de alto grado). Efecto **local** al umbral. Ventaja sobre matching: **no exige CIA** (cubre confundidores no observados).

Ejemplos: **Medicare a los 65** (Card et al.), **regla de Maimónides** para tamaño de clase (Angrist-Lavy).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Tratamiento endógeno + instrumento creíble | IV/2SLS (relevancia/exclusión/independencia) |
| Primera etapa floja | Instrumento débil (F>10); IC inestables |
| Efecto IV/RDD fuzzy | Es un LATE (compliers/umbral), no ATE |
| Tratamiento por un corte en una variable | RDD (salto en el cutoff) |
| ¿Pueden manipular la running variable? | Test de McCrary (densidad) |
| Especificar la RDD | Bandwidth + polinomio local, no global |

---

> **Síntesis:** **IV/2SLS** usa un instrumento (relevancia+exclusión+independencia) para extraer variación exógena del tratamiento endógeno; bajo monotonicidad estima el **LATE** y exige instrumentos fuertes (**F>10**). **RDD** explota un umbral (aleatorización local): **sharp** (determinista) o **fuzzy** (probabilidad→IV), con diagnósticos de **no manipulación (McCrary)**, continuidad y bandwidth/polinomio local. Ambos identifican **sin CIA**, a costa de un efecto **local**.

---

*Retrieval: (1) las dos etapas de 2SLS y las 3 condiciones; (2) ¿qué es un instrumento débil?; (3) RDD sharp vs fuzzy; (4) ¿qué detecta el test de McCrary?*
