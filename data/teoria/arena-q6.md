# Estadística inferencial · Distribuciones y estimación

## De qué trata (y qué sabrás hacer)

La inferencia conecta tres cosas: cuánta confianza merece un promedio (la regla $\sqrt n$), cómo decidir bajo incertidumbre (p-valores y potencia), y cómo resolver esperanzas con estructura condicional (la torre de la esperanza). Esta lección es el puente entre el mundo de probabilidad de Quant y la estadística formal que viene después.

Al terminar sabrás por qué el error de un promedio cae como $1/\sqrt n$ (ni más rápido), qué dice y qué NO dice un p-valor, y cómo condicionar en el primer paso convierte una recurrencia en una ecuación lineal. Cada idea se ancla en un caso pequeño.

---

## La regla 68–95–99.7

Para $X\sim N(\mu,\sigma^2)$, la probabilidad de caer dentro de $k$ desviaciones:

| Rango | Probabilidad |
|-------|-------------|
| $\mu\pm1\sigma$ | $68.3\%$ |
| $\mu\pm2\sigma$ | $95.4\%$ |
| $\mu\pm3\sigma$ | $99.7\%$ |
| $\mu\pm4\sigma$ | $99.994\%$ ($\approx$1 en 15 800) |

Señal de reconocimiento: un evento "a $4\sigma$" debería ser rarísimo bajo normalidad; si en los mercados ocurren seguido, es que las **colas reales son más pesadas** que la normal (leptocúrticas).

---

## Ley de los grandes números vs. teorema del límite central

Ambos hablan de $n$ observaciones i.i.d., pero dicen cosas distintas:

| | LGN | TLC |
|---|---|---|
| ¿Qué converge? | $\bar X_n\to\mu$ | $\dfrac{\sqrt n(\bar X_n-\mu)}{\sigma}\to N(0,1)$ |
| ¿Qué requiere? | $E[X]<\infty$ | $\sigma^2<\infty$ |
| ¿Describe la forma? | No, solo el límite | Sí, la distribución del error |

La LGN dice que el promedio **converge** a la media; el TLC dice **cómo** se distribuye el error alrededor de ella (una campana). Si $\sigma^2=\infty$ (Cauchy), la LGN clásica falla y el TLC no aplica (conecta con [[arena-q9]]).

---

## Error estándar de la media — la raíz $\sqrt n$

El promedio de $n$ observaciones es menos variable que una sola:

$$\sigma_{\bar X}=\frac{\sigma}{\sqrt n}.$$

La consecuencia operativa: para **reducir el error a la mitad** debes **cuadruplicar** $n$ (porque $\sqrt{4n}=2\sqrt n$). Más datos ayudan, pero con rendimientos decrecientes. Es la misma raíz que la regla $\sqrt T$ de la volatilidad (conecta con [[arena-q5]] y [[arena-q7]]).

---

## El p-valor — la definición correcta

$$p=P(\text{datos tan extremos o más}\mid H_0\text{ es verdadera}).$$

Es un condicional, y se lee MAL en el sentido contrario. Errores frecuentes:

| Afirmación | ¿Correcta? |
|-----------|-----------|
| "$p=P(H_0\text{ es falsa})$" | ✗ (requeriría Bayes y un prior) |
| "$p<0.05\Rightarrow$ el efecto es importante" | ✗ (confunde significancia con magnitud) |
| "$p=P(\text{datos extremos}\mid H_0)$" | ✓ |

Un $p$ pequeño dice "si $H_0$ fuera verdadera, estos datos serían improbables" — **no** dice qué tan probable es $H_0$. Es el mismo condicional invertido que confundir sensibilidad con VPP (conecta con [[arena-q2]]).

---

## Errores tipo I/II y potencia

| | $H_0$ verdadera | $H_0$ falsa |
|---|---|---|
| **Rechazar** | Error tipo I ($\alpha$, falso positivo) | Correcto (potencia) |
| **No rechazar** | Correcto | Error tipo II ($\beta$, falso negativo) |

La **potencia** $=1-\beta$ es la probabilidad de detectar un efecto real. Sube con más $n$, mayor efecto real, menor $\sigma$ o mayor $\alpha$. La tensión: para $n$ fijo, bajar $\alpha$ sube $\beta$; solo subir $n$ mejora ambos a la vez.

---

## Ley de la esperanza total (la torre)

$$E[X]=E\big[E[X\mid Y]\big]=\sum_y E[X\mid Y=y]\,P(Y=y).$$

La técnica: cuando hay una estructura condicional natural (el primer evento, el estado actual), condiciona en ella y resuelve la ecuación. Es la herramienta que convierte recurrencias en álgebra. Su compañera, la **ley de la varianza total**, $\text{Var}(X)=E[\text{Var}(X\mid Y)]+\text{Var}(E[X\mid Y])$, parte la varianza en "dentro de grupos" más "entre grupos" (la base de ANOVA y de la descomposición sesgo–varianza, conecta con [[arena-b2]]).

---

## Correlación, $R^2$ y MLE↔OLS

La **correlación** $\rho=\tfrac{\text{Cov}(X,Y)}{\sigma_X\sigma_Y}\in[-1,1]$ mide relación **lineal**: $\rho=0$ no implica independencia ($Y=X^2$ con $X$ simétrica da $\rho=0$). El **$R^2$** es la fracción de varianza de $Y$ explicada por el modelo; nunca baja al añadir variables (por eso se usa el $R^2$ ajustado). Y un puente clave: bajo errores gaussianos, **maximizar la verosimilitud equivale a minimizar los cuadrados** ($\text{MLE}=\text{OLS}$), porque la log-verosimilitud tiene a $\lVert y-X\beta\rVert^2$ como único término dependiente de $\beta$ (conecta con [[arena-dg2]] e [[arena-isl2]]).

---

## Mini-ejemplo trabajado: la torre de esperanza resuelve la geométrica

¿Cuántos lanzamientos esperas hasta la primera cara con moneda justa? En vez de sumar la serie, condiciona en el primer lanzamiento (eso es la torre $E[X]=E[E[X\mid\text{primer tiro}]]$):

$$E[X]=\tfrac12\cdot1+\tfrac12\cdot(1+E[X]).$$

El primer término: con prob $\tfrac12$ sale cara y terminas en 1 tiro. El segundo: con prob $\tfrac12$ sale cruz, gastaste 1 tiro y **vuelves al mismo estado**. Despejando: $E[X]-\tfrac12 E[X]=1\Rightarrow E[X]=2$. Generaliza a sesgo $p$: $E[X]=1/p$.

**Predicción antes de seguir:** ¿la varianza de la media muestral de 100 tiros de un dado es mayor o menor que la de un solo tiro? Respuesta: **menor, por un factor 100** ($\sigma^2/n$). Promediar no cambia la media pero divide la varianza entre $n$; por eso para *reducir el error a la mitad* hay que *cuadruplicar* $n$. La misma $\sqrt n$ que reaparece en la regla $\sqrt T$ de finanzas.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** proceso con reinicio o estructura condicional (geométrica, coleccionista, primer éxito) → plantea la torre $E[X]=\sum_y E[X\mid Y]P(Y)$ y resuelve la ecuación lineal.
- **Contraejemplo ($\rho=0\ne$ independencia):** $Y=X^2$ con $X$ simétrica tiene $\text{Cov}(X,Y)=0$, así que $\rho=0$, pero $Y$ depende totalmente de $X$. Correlación cero solo descarta relación *lineal*.
- **Caso borde (Cauchy):** si $\sigma^2=\infty$, la LGN clásica falla y el TLC no aplica; promediar muestras de Cauchy no concentra nada. El borde revela qué supuesto (varianza finita) sostiene ambos teoremas.

## Errores típicos

- **Conceptual:** leer el p-valor como $P(H_0\mid\text{datos})$. Es $P(\text{datos extremos}\mid H_0)$ — el condicional invertido, el mismo error que confundir sensibilidad con VPP.
- **Técnico:** reportar $R^2$ alto como evidencia de buen modelo: $R^2$ nunca baja al añadir variables; usa $R^2$ ajustado y validación fuera de muestra.
- **De supuestos:** aplicar el TLC con $n$ pequeño y cola pesada, o usar $\sigma/\sqrt n$ cuando las observaciones están autocorrelacionadas (el $n$ "efectivo" es menor).

## Transferencia isomorfa

- **Error estándar $\sigma/\sqrt n$ ↔ regla $\sqrt T$ de volatilidad:** ambas salen de $\text{Var}(\sum X_i)=n\,\text{Var}(X)$ para i.i.d.; reducir incertidumbre con datos y escalar riesgo con el horizonte son la misma raíz (conecta con [[arena-q5]] y [[arena-q7]]).
- **p-valor ↔ tasa base / VPP:** "datos improbables bajo $H_0$" no es "$H_0$ improbable", igual que "sensibilidad alta" no es "VPP alto" (conecta con [[arena-q2]]).
- **Ley de varianza total ↔ descomposición sesgo-varianza:** within + between es la misma partición que error irreducible vs. varianza del modelo en ML (conecta con [[arena-iml4]]).
- **Torre de esperanza ↔ backward induction / DP:** condicionar en el primer paso y resolver la recurrencia es el motor de la parada óptima (conecta con [[arena-q8]] y [[arena-cc3]]).

Moraleja de la arista: *cuando algo tiene estructura condicional, condiciona en el primer paso; cuando promedias $n$ cosas i.i.d., la incertidumbre cae como $1/\sqrt n$ — no más rápido.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Dato a $k\sigma$ de la media" | Regla 68–95–99.7; a $>3\sigma$ ya es muy inusual |
| "Media muestral de $n$ obs." | $\sigma_{\bar X}=\sigma/\sqrt n$ |
| "¿Qué significa $p=0.03$?" | $P(\text{datos extremos}\mid H_0)$, NO $P(H_0\text{ falsa})$ |
| "Tipo I vs tipo II" | FP vs FN; ambos dependen del umbral |
| "$\text{Var}(X+Y)$ con correlación" | $\text{Var}(X)+\text{Var}(Y)+2\text{Cov}$ |
| "$E[]$ de proceso con reinicio" | Torre: $E[X]=p\,a+(1-p)(b+E[X])$ |
| "Suma de cuadrados de normales" | $\chi^2(n)$: $E=n$, $\text{Var}=2n$ |

---

> **Síntesis:** La estadística inferencial conecta la variabilidad de los datos con la precisión de los estimadores ($\sqrt n$), las decisiones bajo incertidumbre (p-valor, potencia) y la estructura condicional (la torre de $E[]$). La ley de la esperanza total es la llave maestra: convierte recurrencias y árboles de probabilidad en una ecuación lineal.

---

*Retrieval: cierra y responde: (1) la regla 68–95–99.7; (2) diferencia LGN/TLC; (3) $E[X]$ de la geométrica con probabilidad $p$; (4) por qué reducir el error a la mitad exige cuadruplicar $n$.*
