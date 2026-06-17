# La causalidad según Pearl I: la escalera de la causalidad

> El enfoque **gráfico/do-calculus** de Pearl. Complementa [[arena-h3]] (What If, enfoque potential-outcomes) con la **escalera**, el **do-operator** y la mirada de IA.

## De qué trata esta lección (y qué sabrás hacer al final)

"Correlación no es causación" lo repite todo el mundo, pero pocos saben *por qué* ni qué se necesita para cruzar de una a otra. Esta lección construye, desde cero, la respuesta de Judea Pearl: la **escalera de la causalidad**, tres peldaños de preguntas con poder creciente —**ver** (asociación), **hacer** (intervención), **imaginar** (contrafactuales)—. La tesis central, contraintuitiva en la era del big data: **los datos por sí solos no contienen causalidad**; subir la escalera exige un *modelo*, no más datos.

Al terminar podrás: (1) clasificar cualquier pregunta causal en su peldaño; (2) explicar por qué el machine learning, por potente que sea, vive en el peldaño 1; (3) entender por qué una misma tabla es compatible con mundos causales opuestos; y (4) reconocer el do-operator como el salto físico del peldaño 1 al 2. No se asume nada de causalidad previa; cada idea entra por un ejemplo cotidiano.

## Los tres peldaños

| Peldaño | Pregunta | Notación | Quién |
|---|---|---|---|
| 1 **Asociación** (ver) | ¿Qué pasa si **veo** X? | P(Y\|X) | estadística, **ML/deep learning** |
| 2 **Intervención** (hacer) | ¿Qué pasa si **hago** X? | P(Y\|do(X)) | experimentos, políticas |
| 3 **Contrafactuales** (imaginar) | ¿Qué **habría** pasado si…? | Y_x | explicación, atribución |

Cada peldaño es más poderoso: uno superior responde preguntas de los inferiores, **no al revés**. El **deep learning** vive en el peldaño 1 (ajusta asociaciones a datos, como un búho que predice sin entender). Ver escalera-de-la-causalidad.

## La causalidad requiere un modelo

Tesis central (**"mind over data"**): los **datos no contienen causalidad** — describen el peldaño 1. La misma tabla es compatible con A→Y, A←Y o A←C→Y; solo un **modelo causal** (DAG con supuestos) desempata y permite subir la escalera. Ver causalidad-requiere-modelo.

**Mini-Turing test:** una máquina causal debe responder preguntas de los tres niveles dado un modelo; una que solo asocia falla en intervención y contrafactuales.

## Génesis histórica

- **Galton / Pearson:** fundadores de la estadística que **desterraron** la causalidad (solo correlación "objetiva") → tabú de un siglo.
- **Sewall Wright** (1920s): inventó los **path diagrams** (primer modelo causal cuantitativo), antecesores directos de los DAGs de Pearl.
- **do-operator:** intervenir do(X) = borrar las flechas hacia X (lo que hace un **RCT**); sube físicamente del peldaño 1 al 2.

---

## Mini-ejemplo trabajado: una tabla, tres mundos causales

Observas que helados y ahogamientos suben juntos: P(ahogamiento | ves helados altos) es alta. Esa **única** tabla de asociación (peldaño 1) es compatible con tres modelos causales distintos:

1. Helado → ahogamiento (el azúcar te marea).
2. Ahogamiento → helado (improbable, pero los datos no lo prohíben).
3. Calor → helado y Calor → ahogamiento (fork: el **verano** causa ambos).

Los números son **idénticos** en los tres mundos; ninguna estadística los distingue. Solo un **modelo** (sé que el calor confunde) te deja subir al peldaño 2 y predecir: *si prohíbo los helados (do), ¿bajan los ahogamientos?* → no, porque la flecha era espuria. Esa es la tesis "mind over data": la causa no está en los datos, está en el supuesto que traes.

**Predicción antes de seguir:** un modelo con AUC 0.99 que predice ahogamientos a partir de ventas de helado, ¿sabe que prohibir helados no salva vidas? No: vive en el peldaño 1; jamás respondió una pregunta de *do()*.

## Prototipo, contraejemplo y caso borde

- **Prototipo (peldaño 2):** un RCT —borrar las flechas hacia X aleatorizando— responde "¿qué pasa si hago X?" sin necesitar el modelo completo.
- **Contraejemplo (peldaño 1 disfrazado de 3):** un modelo predictivo enorme presentado como "entiende causas". Predecir ≠ intervenir; es el error de marketing más común en IA.
- **Caso borde (contrafactual, peldaño 3):** "¿este paciente *habría* mejorado sin el fármaco?" no lo responde ni un RCT (da promedios), solo un SCM sobre el individuo (ver [[arena-h18]]).

## Errores típicos

- **Conceptual:** "dejemos que los datos hablen" para una pregunta causal — los datos solo hablan del peldaño 1.
- **De interpretación:** tratar buen desempeño predictivo como evidencia de mecanismo.
- **De nivel:** intentar responder un contrafactual (peldaño 3) con un experimento (peldaño 2), que solo da efectos promedio.

## Transferencia isomorfa

La escalera ordena tareas de datos, no solo de epidemiología:

- **Peldaño 1 ↔ todo el ML supervisado:** clasificación/regresión ajustan P(Y|X); brillan prediciendo y son **ciegos** a intervenciones (conecta con [[arena-isl1]], estimar f).
- **Peldaño 2 ↔ A/B testing:** aleatorizar una feature es el do-operator del producto; por eso el experimento, no el modelo offline, decide causalidad.
- **Peldaño 3 ↔ explicaciones contrafactuales:** "¿qué cambio mínimo habría volteado esta decisión del modelo?" es una pregunta de peldaño 3 sobre el clasificador.

Moraleja de la arista: *predecir, intervenir e imaginar son tres preguntas distintas; subir de una a otra exige un modelo, no más datos.*

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
