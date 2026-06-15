# Conductual IV: data science aplicada, stakeholders y carrera (STAR)

> Preguntas conductuales **específicas de DS** y de carrera. Usa [[narrativa-star]] y demuestra **orientación al negocio** y **traducción** técnica. Ver [[comunicar-resultado-ds-star]].

## Proyectos y stakeholders

- **Proyecto end-to-end:** encuadra el problema de **negocio** (no solo técnico), recorre el ciclo (entender→datos→modelar→validar→desplegar/comunicar) destacando **tus** decisiones, y da el **impacto de negocio** cuantificado (no solo el AUC: la decisión/valor que habilitó).
- **Resultado negativo/nulo:** comunícalo con **honestidad** y enmárcalo como **aprendizaje accionable** (saber qué NO hacer ahorra recursos); propón el siguiente paso.
- **Modelo que falló en producción:** diagnostica la **causa raíz** (skew/drift/supuestos), corrige y añade **monitoreo/salvaguardas**.
- **Stakeholder escéptico:** indaga su preocupación, **traduce**, valida de forma comprensible y conecta con su objetivo.
- **Datos sucios:** perfila la calidad, decide el manejo, **documenta supuestos** y comunica limitaciones.

## DS responsable y métricas

- **Ética/privacidad/fairness:** identifica el riesgo, plantéalo y propón **mitigaciones** concretas (anonimización, auditoría de sesgo, consentimiento).
- **Definir métrica:** alinéala con el **valor de negocio** (+ guardrails); evita métricas vanidosas o 'gameables'.
- **Simple vs complejo:** elige según el **contexto** (interpretabilidad, regulación, confianza, mantenimiento), no por moda.

## Carrera y motivación

- **"Por qué DS / este puesto":** motivación **específica** (con ejemplo), encaje con el rol/empresa (investígala), y valor que aportas.
- **"Cuéntame de ti":** narrativa breve presente-pasado-futuro con 1-2 logros cuantificados.
- **Aprendizaje continuo / metas:** hábitos + un ejemplo **aplicado** con impacto; metas alineadas con el rol.

---

## Errores típicos

- **Conceptual:** reportar solo la métrica técnica (AUC, F1) en vez del **impacto de negocio** (la decisión o el valor que habilitó).
- **De métrica:** proponer una métrica vanidosa o 'gameable' sin guardrails; lo que se optimiza sin contrapeso se infla a costa de otra cosa.
- **De honestidad:** ocultar o maquillar un resultado negativo en vez de enmarcarlo como aprendizaje accionable.

## Transferencia isomorfa

Las conductuales de DS son las técnicas vistas desde el negocio: la misma estructura, otra audiencia.

- **"Modelo que falló en producción" ↔ training-serving skew / drift:** diagnosticar causa raíz y añadir monitoreo es exactamente la lección de del-modelo-al-sistema (conecta con [[arena-s1]] y [[arena-cds3]]).
- **Definir métrica + guardrails ↔ North Star y counter-metrics:** alinear la métrica al valor de negocio sin que se 'gamee' es el marco North Star + guardrail (conecta con [[arena-ads4]]).
- **Causa raíz vs síntoma ↔ confounding y diagnóstico de métrica:** distinguir el impulsor del correlacionado es el mismo reflejo causal que corrige un coeficiente con signo absurdo (conecta con [[arena-pst4]]).
- **Simple vs complejo según contexto ↔ sesgo-varianza e interpretabilidad:** elegir el modelo por interpretabilidad/regulación, no por moda, es el trade-off flexibilidad↔interpretabilidad (conecta con [[arena-isl1]]).

Moraleja de la arista: *un proyecto de DS se cuenta por el valor de negocio que movió, no por su AUC; y una métrica sin guardrail siempre se acaba gameando.*

---

## Disparadores

| Pregunta | Jugada |
|----------|--------|
| "Proyecto del que estés orgulloso" | Encuadre de negocio + tu rol + impacto medible |
| "Comunicar un resultado negativo" | Honesto + aprendizaje accionable + siguiente paso |
| "Modelo que falló en producción" | Causa raíz + monitoreo/salvaguardas |
| "Stakeholder no confía en tu análisis" | Indagar + traducir + validar comprensible |
| "¿Por qué este puesto?" | Específico, investigado, alineado con el rol |

---

> **Síntesis:** en las conductuales de **DS**, demuestra **orientación al negocio**: proyectos end-to-end con **impacto medible** (no solo métricas técnicas), comunicación **honesta** de resultados negativos, **causa raíz** y salvaguardas ante fallos en producción, **traducción** para stakeholders escépticos, rigor con datos sucios y **DS responsable**. En **carrera**, respuestas **específicas, investigadas y alineadas** con el rol.

---

*Retrieval: (1) ¿qué impacto reportar en un proyecto DS end-to-end?; (2) ¿cómo comunicar un resultado negativo?; (3) ¿qué hacer con un modelo que falla en producción?; (4) ¿qué hace fuerte un "por qué este puesto"?*
