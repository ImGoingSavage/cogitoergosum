# OHDSI III: analítica estandarizada (cohortes, caracterización, estimación, predicción)

## Definir cohortes y fenotipos

**Cohorte** = "un conjunto de personas que satisfacen uno o más criterios de inclusión durante un periodo de tiempo". Tres componentes:
1. **Eventos de entrada** (qué inicia la pertenencia).
2. **Reglas de inclusión** (filtros: ≥365 días de observación previa, edad…).
3. **Criterios de salida** (fin de exposición/observación).

Se construyen con **concept sets** (conceptos estándar + descendientes). Enfoques: **basado en reglas** (determinista, ATLAS) vs **probabilístico** (un modelo da una probabilidad; PheValuator). Un **fenotipo** es la definición computable de una condición; **valídalo** (sensibilidad/especificidad/**PPV**) o introduces misclasificación. Ver [[definir-cohorte-fenotipo]].

## Caracterización (descriptivo)

Responde "¿qué hay en los datos?": nivel **base de datos** (demografía, conteos, tendencias — ACHILLES), nivel **cohorte** (comorbilidades, fármacos), **treatment pathways** (secuencias de tratamiento) e **incidencia/prevalencia**. Describe, no infiere. Ver [[caracterizacion-ohdsi]].

## Estimación a nivel de población (causa)

Efectos causales de una exposición. Dos familias:
- **Cohort method** (comparativa): new-user + comparador, ajustando confundidores con **propensity scores a gran escala** (miles de covariables + LASSO); evalúa **balance**.
- **Autocontrolados** (cada persona su propio control): **SCCS**, **case-crossover**, self-controlled cohort → eliminan confundidores **fijos** (pero sensibles a los que cambian en el tiempo). Ver [[estimacion-nivel-poblacion-ohdsi]].

## Predicción a nivel de paciente (PLP)

**Pronóstico** individual (no causa). Marco estandarizado: **cohorte objetivo** (target) + **cohorte de outcome** + **time-at-risk**. Se extraen miles de features, se ajusta el modelo y se evalúa con **discriminación (AUC)** + **calibración**, con validación interna y **externa**. Una variable predictiva ≠ causa. Ver [[prediccion-nivel-paciente-plp]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Definir exposición/outcome/población | Cohorte: entry/inclusión/exit + concept sets |
| ¿La definición captura el concepto? | Valida el fenotipo (sens/espec/PPV) |
| ¿Qué hay en la base? | Caracterización (pathways, incidencia) — descriptivo |
| ¿Causa este fármaco el evento? | Estimación: cohort method (PS a gran escala) o autocontrolado |
| ¿Quién tiene alto riesgo? | Predicción (PLP): target+outcome+time-at-risk; AUC+calibración |

---

> **Síntesis:** una **cohorte** se define por entry/inclusión/exit sobre **concept sets**; el **fenotipo** debe validarse (sens/PPV). La **caracterización** describe (pathways, incidencia). La **estimación** busca causa con **cohort method + PS a gran escala** o diseños **autocontrolados**. La **predicción (PLP)** pronostica con **target+outcome+time-at-risk**, evaluada por **AUC y calibración**. Estimación ≠ predicción: causa vs pronóstico.

---

*Retrieval: (1) los 3 componentes de una cohorte; (2) ¿por qué validar un fenotipo y con qué métricas?; (3) cohort method vs autocontrolados; (4) ¿cómo se evalúa un modelo PLP?*
