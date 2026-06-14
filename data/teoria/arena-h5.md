# Inferencia causal III: estimación con modelos (IP weighting, g-fórmula, PS, IV)

## ¿Por qué modelar?

Los estimadores no paramétricos por estratos solo sirven con **pocos** confundidores discretos; con muchos o continuos los estratos quedan vacíos (**maldición de la dimensionalidad**). Los **modelos** (paramétricos o ML) suavizan entre estratos para estimar E[Y|A,L] o P(A|L), a costa del supuesto de especificación.

## IP weighting y MSM

Modela el **tratamiento** P(A=a|L) y pondera por **1/P(A=a|L)** → **pseudo-población** donde A ⊥ L (sin confundimiento). Sobre ella se ajusta un **Modelo Estructural Marginal (MSM)** para E[Y^a] (p. ej. logit P(Y^a=1)=β0+β1·a). **Pesos estabilizados** SW = P(A=a)/P(A=a|L): menos variables y más eficientes; cuidan (no eliminan) casi-violaciones de positividad. Ver [[ip-weighting-msm]].

## Estandarización / g-fórmula

Modela el **outcome** E[Y|A,L], predice bajo a=1 y a=0 para cada individuo y promedia: **E[Y^a]=Σ_l E[Y|a,l]P(l)**. Es la **cara complementaria** del IP weighting (uno modela el outcome, el otro el tratamiento); bajo modelos correctos coinciden. Ver [[estandarizacion-g-formula]].

## Propensity score

**π(L)=P(A=1|L)**: probabilidad de tratamiento dados los confundidores. Es un **balancing score** (condicionar en π(L) equilibra L). Cuatro usos: **estratificación**, **emparejamiento**, **ponderación** (= IP weighting), **regresión** sobre el PS. Solo controla confundidores **medidos**; la falta de **solapamiento** (common support) señala problemas de positividad. Ver [[propensity-score]].

## Doble robustez y ML

Un estimador **doblemente robusto** combina el modelo del **tratamiento** y el del **outcome**: consistente si **uno de los dos** está bien especificado (AIPW/TMLE). Con **ML** flexible para ambos modelos + **cross-fitting** (double/debiased ML) se ajusta por confundidores de alta dimensión manteniendo inferencia válida. Ver [[doble-robustez]].

## Variable instrumental

Un instrumento Z permite estimar el efecto **con confundimiento no medido** si: (i) **relevancia** (Z→A), (ii) **restricción de exclusión** (Z afecta Y solo vía A), (iii) Z e Y sin causas comunes. Estimando usual = (E[Y|Z=1]−E[Y|Z=0])/(E[A|Z=1]−E[A|Z=0]). Las 3 dan solo **bounds**; para un punto se necesita una 4ª: **homogeneidad** o **monotonicidad** (sin defiers) → IV estima el **LATE** (efecto en **compliers**). Cuidado con **instrumentos débiles** (relevancia baja → varianza y sesgo enormes). Ver [[variable-instrumental]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Muchos confundidores | Modela: IP weighting o g-fórmula |
| Modelar el tratamiento | IP weighting + MSM (pesos estabilizados) |
| Modelar el outcome | Estandarización / g-fórmula paramétrica |
| No sé qué modelo acertaré | Doblemente robusto (AIPW/TMLE) + ML |
| Confundimiento no medido + instrumento creíble | IV (3 condiciones); +monotonicidad ⇒ LATE |
| ¿Qué covariables incluir? | Confundidores + predictores del outcome; nunca mediador/collider/instrumento |

---

> **Síntesis:** con muchos confundidores hay que **modelar**. **IP weighting** (modela el tratamiento, pseudo-población, MSM) y **estandarización/g-fórmula** (modela el outcome) son dos caras de la misma identificación; combinarlas da **doble robustez** (base del causal ML). El **propensity score** resume confundidores en una dimensión. La **variable instrumental** ataca el confundimiento no medido pero solo da el **LATE** bajo monotonicidad y sufre con instrumentos débiles.

---

*Retrieval: (1) ¿qué modela IP weighting vs estandarización?; (2) ¿qué es un balancing score?; (3) ¿qué garantiza la doble robustez?; (4) las 3 condiciones de IV y qué es el LATE.*
