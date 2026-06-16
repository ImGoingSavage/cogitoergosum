# OHDSI III: analítica estandarizada (cohortes, caracterización, estimación, predicción)

## De qué trata esta lección (y qué sabrás hacer al final)

Con datos estandarizados (OMOP) y vocabularios mapeados, ¿cómo *analizas*? Todo empieza definiendo una **cohorte** —y ahí acecha una trampa de tasa base: un fenotipo con sensibilidad y especificidad altísimas puede aun así estar lleno de falsos positivos—. Esta lección construye, desde cero, la analítica estandarizada de OHDSI: cómo definir y **validar** cohortes/fenotipos, y los tres tipos de análisis que nunca deben confundirse —**caracterización** (describir), **estimación** (causa) y **predicción** (pronóstico)—.

Al terminar podrás: (1) definir una cohorte por sus tres componentes (entry/inclusión/exit); (2) entender por qué validar un fenotipo es Bayes puro (el PPV depende de la prevalencia); (3) distinguir cohort method/PS a gran escala de los diseños autocontrolados; y (4) evaluar un modelo de predicción (PLP) con AUC **y** calibración. La validación del fenotipo entra por números. *(Ejemplos clínicos ilustran el método, no son consejo médico.)*

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

## Mini-ejemplo trabajado: por qué hay que validar el fenotipo (y es Bayes)

Tu definición de "diabetes" tiene **sensibilidad 90%** y **especificidad 95%**, números que suenan excelentes. Pero el PPV —"si la definición marca a alguien, ¿de verdad es diabético?"— depende de la **prevalencia**. Con prevalencia del **5%** en la base, sobre 10 000 pacientes:

- Diabéticos reales: 500 → detectados: 0.90·500 = **450** verdaderos positivos.
- Sanos: 9 500 → falsos positivos: 0.05·9 500 = **475**.
- **PPV = 450 / (450+475) ≈ 49%.**

Casi **la mitad** de tu cohorte "diabética" no lo es, pese a sens/espec altísimas. Es la misma tasa-base que engaña en los tests diagnósticos (conecta con [[arena-q2]]): un clasificador bueno sobre una condición rara aún produce muchos falsos positivos. Por eso un fenotipo sin validar mete **misclasificación** que sesga todo el estudio.

**Predicción antes de seguir:** ¿qué pasa con el PPV si subes la especificidad a 99%? Falsos positivos = 0.01·9 500 = 95 → PPV = 450/545 ≈ **83%**. Sobre condiciones raras, **la especificidad manda** más que la sensibilidad.

## Prototipo, contraejemplo y caso borde

- **Prototipo (estimación, causa):** new-user + comparador activo + PS a gran escala con balance verificado → efecto causal de una exposición.
- **Contraejemplo (predicción disfrazada de causa):** un modelo PLP con AUC 0.85 cuyas features "predictivas" se presentan como factores *causales* — pronóstico ≠ etiología. Una variable puede predecir sin causar.
- **Caso borde (fenotipo probabilístico):** condiciones difíciles de definir con reglas → PheValuator da un gold standard probabilístico en vez de chart review caro.

## Errores típicos

- **Conceptual:** confundir **estimación** (causa, requiere desconfundir) con **predicción** (pronóstico, solo necesita asociación estable) — distinto objetivo, distinta validación.
- **Técnico:** evaluar un PLP solo con AUC y olvidar la **calibración** (un modelo puede discriminar bien y dar probabilidades mal escaladas).
- **De método:** no validar el fenotipo → misclasificación sistemática aguas abajo.

## Transferencia isomorfa

El marco de cohortes/PLP es ML aplicado con etiquetas imperfectas:

- **Validar fenotipo ↔ calidad de etiquetas / weak supervision:** medir sens/espec/PPV de una definición es exactamente auditar la calidad de las labels antes de entrenar (conecta con [[arena-dmls2]]).
- **Estimación vs predicción ↔ ML causal vs ML predictivo:** la frontera causa/pronóstico es la misma que separa "¿qué pasa si intervengo?" de "¿quién tiene alto riesgo?" (conecta con [[arena-h15]], la escalera).
- **PS a gran escala ↔ regresión logística regularizada de alta dimensión:** miles de covariables + LASSO para la propensión es un modelo de ML estándar puesto al servicio del desconfundimiento.

Moraleja de la arista: *define la cohorte con cuidado, valida el fenotipo (PPV depende de la tasa base) y nunca confundas predecir con causar.*

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
