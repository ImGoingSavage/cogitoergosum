# Inferencia causal III: estimación con modelos (IP weighting, g-fórmula, PS, IV)

## De qué trata esta lección (y qué sabrás hacer al final)

Identificar un efecto es saber que *se puede* estimar; esta lección construye, desde cero, *cómo* se estima cuando hay **muchos** confundidores y los estratos a mano ya no alcanzan. La idea central es que hay dos rutas duales —modelar el **tratamiento** (IP weighting) o modelar el **outcome** (g-fórmula)— que llegan al mismo sitio, y que combinarlas compra robustez. Y cuando el confundidor **no está medido**, queda el último recurso: la variable instrumental.

Al terminar podrás: (1) construir la pseudo-población del IP weighting y entender por qué los pesos estabilizados existen; (2) ver IP weighting y g-fórmula como dos caras de la misma identificación; (3) usar el propensity score como balancing score que vence la dimensionalidad; y (4) saber qué ataca una variable instrumental (confundimiento no medido) y qué entrega a cambio (el LATE, solo en compliers). Profundiza la estimación que [[arena-h3]] dejó planteada.

## ¿Por qué modelar?

Los estimadores no paramétricos por estratos solo sirven con **pocos** confundidores discretos; con muchos o continuos los estratos quedan vacíos (**maldición de la dimensionalidad**). Los **modelos** (paramétricos o ML) suavizan entre estratos para estimar E[Y|A,L] o P(A|L), a costa del supuesto de especificación.

## IP weighting y MSM

Modela el **tratamiento** P(A=a|L) y pondera por **1/P(A=a|L)** → **pseudo-población** donde A ⊥ L (sin confundimiento). Sobre ella se ajusta un **Modelo Estructural Marginal (MSM)** para E[Y^a] (p. ej. logit P(Y^a=1)=β0+β1·a). **Pesos estabilizados** SW = P(A=a)/P(A=a|L): menos variables y más eficientes; cuidan (no eliminan) casi-violaciones de positividad. Ver ip-weighting-msm.

## Estandarización / g-fórmula

Modela el **outcome** E[Y|A,L], predice bajo a=1 y a=0 para cada individuo y promedia: **E[Y^a]=Σ_l E[Y|a,l]P(l)**. Es la **cara complementaria** del IP weighting (uno modela el outcome, el otro el tratamiento); bajo modelos correctos coinciden. Ver estandarizacion-g-formula.

## Propensity score

**π(L)=P(A=1|L)**: probabilidad de tratamiento dados los confundidores. Es un **balancing score** (condicionar en π(L) equilibra L). Cuatro usos: **estratificación**, **emparejamiento**, **ponderación** (= IP weighting), **regresión** sobre el PS. Solo controla confundidores **medidos**; la falta de **solapamiento** (common support) señala problemas de positividad. Ver propensity-score.

## Doble robustez y ML

Un estimador **doblemente robusto** combina el modelo del **tratamiento** y el del **outcome**: consistente si **uno de los dos** está bien especificado (AIPW/TMLE). Con **ML** flexible para ambos modelos + **cross-fitting** (double/debiased ML) se ajusta por confundidores de alta dimensión manteniendo inferencia válida. Ver doble-robustez.

## Variable instrumental

Un instrumento Z permite estimar el efecto **con confundimiento no medido** si: (i) **relevancia** (Z→A), (ii) **restricción de exclusión** (Z afecta Y solo vía A), (iii) Z e Y sin causas comunes. Estimando usual = (E[Y|Z=1]−E[Y|Z=0])/(E[A|Z=1]−E[A|Z=0]). Las 3 dan solo **bounds**; para un punto se necesita una 4ª: **homogeneidad** o **monotonicidad** (sin defiers) → IV estima el **LATE** (efecto en **compliers**). Cuidado con **instrumentos débiles** (relevancia baja → varianza y sesgo enormes). Ver variable-instrumental.

---

## Mini-ejemplo trabajado: la pseudo-población del IP weighting

Confundidor L (frágil/sano) que empuja a tratar a los frágiles. Supón estas propensiones P(A=1|L):

- **Sanos:** P(tratar)=0.2. Un sano tratado pesa 1/0.2 = **5**; un sano no tratado pesa 1/0.8 = **1.25**.
- **Frágiles:** P(tratar)=0.8. Un frágil tratado pesa 1/0.8 = **1.25**; un frágil no tratado pesa 1/0.2 = **5**.

Cada persona "vale" por varias en la **pseudo-población**: los pocos sanos tratados (raros) se clonan ×5; los muchos frágiles tratados (comunes) apenas ×1.25. Tras reponderar, tratamiento y L quedan **independientes** (A⊥L), como si hubieras aleatorizado — y sobre esa pseudo-población un MSM estima E[Y^a] sin confundimiento. La g-fórmula llega al mismo sitio modelando el *outcome* en vez del *tratamiento*: dos caras de la misma identificación.

**Predicción antes de seguir:** ¿qué pasa con el peso de un frágil no tratado si casi ningún frágil queda sin tratar (P(A=0|frágil)=0.02)? Peso = 1/0.02 = 50: una sola observación domina la estimación → **casi-violación de positividad**, varianza explosiva. Por eso existen los **pesos estabilizados**.

## Prototipo, contraejemplo y caso borde

- **Prototipo (doble robustez):** modelas tratamiento *y* outcome; basta que **uno** esté bien especificado (AIPW/TMLE) → red de seguridad contra mala especificación.
- **Contraejemplo (IV inválida):** un "instrumento" que afecta Y por otra vía (viola exclusión) — p. ej. la distancia al hospital también refleja nivel socioeconómico. Parece IV, sesga como confundidor.
- **Caso borde (instrumento débil):** relevancia minúscula (F<10) → el denominador (E[A|Z=1]−E[A|Z=0]) ≈ 0 hace estallar la estimación; un poco de sesgo en exclusión se amplifica enormemente.

## Errores típicos

- **Conceptual:** creer que IV o PS arreglan confundidores **no medidos** por la vía del ajuste — solo IV los ataca, y a cambio estima un **LATE**, no el ATE.
- **Técnico:** pesos sin estabilizar ante propensiones extremas → varianza enorme.
- **De interpretación:** reportar el LATE (compliers) como si fuera el efecto poblacional.

## Transferencia isomorfa

El reponderar por probabilidad inversa es maquinaria compartida:

- **IP weighting ↔ importance sampling / off-policy (IPS):** evaluar una política nueva reponderando logs por 1/propensión de la vieja es *literalmente* el mismo estimador (conecta con [[arena-dmls1]]).
- **Doble robustez ↔ ensamble de dos modelos:** "consistente si uno de los dos acierta" es la intuición de combinar un modelo de propensión y uno de outcome, como un blending con garantía.
- **Instrumento ↔ encouragement design:** en experimentos, un empujón aleatorio (email que sube la adopción) es un instrumento que da el LATE sobre quienes responden.

Moraleja de la arista: *modelar el tratamiento (pesos) y modelar el outcome (g-fórmula) son duales; combinarlos compra robustez, y un instrumento cambia "confundimiento no medido" por "efecto solo en compliers".*

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
