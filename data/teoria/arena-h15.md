# La causalidad según Pearl I: la escalera de la causalidad

> El enfoque **gráfico/do-calculus** de Pearl. Complementa [[arena-h3]] (What If, enfoque potential-outcomes) con la **escalera**, el **do-operator** y la mirada de IA.

## Los tres peldaños

| Peldaño | Pregunta | Notación | Quién |
|---|---|---|---|
| 1 **Asociación** (ver) | ¿Qué pasa si **veo** X? | P(Y\|X) | estadística, **ML/deep learning** |
| 2 **Intervención** (hacer) | ¿Qué pasa si **hago** X? | P(Y\|do(X)) | experimentos, políticas |
| 3 **Contrafactuales** (imaginar) | ¿Qué **habría** pasado si…? | Y_x | explicación, atribución |

Cada peldaño es más poderoso: uno superior responde preguntas de los inferiores, **no al revés**. El **deep learning** vive en el peldaño 1 (ajusta asociaciones a datos, como un búho que predice sin entender). Ver [[escalera-de-la-causalidad]].

## La causalidad requiere un modelo

Tesis central (**"mind over data"**): los **datos no contienen causalidad** — describen el peldaño 1. La misma tabla es compatible con A→Y, A←Y o A←C→Y; solo un **modelo causal** (DAG con supuestos) desempata y permite subir la escalera. Ver [[causalidad-requiere-modelo]].

**Mini-Turing test:** una máquina causal debe responder preguntas de los tres niveles dado un modelo; una que solo asocia falla en intervención y contrafactuales.

## Génesis histórica

- **Galton / Pearson:** fundadores de la estadística que **desterraron** la causalidad (solo correlación "objetiva") → tabú de un siglo.
- **Sewall Wright** (1920s): inventó los **path diagrams** (primer modelo causal cuantitativo), antecesores directos de los DAGs de Pearl.
- **do-operator:** intervenir do(X) = borrar las flechas hacia X (lo que hace un **RCT**); sube físicamente del peldaño 1 al 2.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "El modelo predice bien → entendemos causas" | No: es peldaño 1 (asociación) |
| "Dejemos que los datos hablen" (causal) | Datos = peldaño 1; necesitas un modelo |
| ¿Qué pregunta causal me hacen? | Clasifícala: ver / hacer / imaginar |
| ¿Por qué correlación ≠ causación? | Son peldaños distintos (1 vs 2) |
| ¿IA "fuerte"? | Falta razonar intervenciones y contrafactuales |

---

> **Síntesis:** la **escalera de la causalidad** ordena las preguntas en **ver (asociación), hacer (intervención) e imaginar (contrafactuales)**, con poder creciente. El ML actual está en el peldaño 1. **Subir requiere un modelo causal**, no más datos ("mind over data"). Históricamente Pearson desterró la causa y **Sewall Wright** (path diagrams) la rescató; el **do-operator** formaliza la intervención.

---

*Retrieval: (1) los 3 peldaños y su notación; (2) ¿por qué el ML está en el peldaño 1?; (3) ¿por qué los datos no bastan para la causalidad?; (4) ¿qué aportó Sewall Wright?*
