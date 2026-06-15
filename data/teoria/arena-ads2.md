# Estadística e inferencia para entrevistas

## Propiedades de las variables aleatorias

- **Esperanza:** $E[X]=\int x\,f_X(x)\,dx$ (peso de cada valor por su densidad).
- **Varianza:** $\mathrm{Var}(X)=E[X^2]-(E[X])^2$, siempre $\ge 0$; su raíz es la desviación estándar.
- **Covarianza:** $\mathrm{Cov}(X,Y)=E[XY]-E[X]E[Y]$ (relación lineal).
- **Correlación:** covarianza normalizada $\rho=\dfrac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\,\mathrm{Var}(Y)}}\in[-1,1]$.

No hace falta memorizar derivaciones de cada distribución, pero sí saber **derivar** la media/varianza de las comunes (uniforme, exponencial) cuando lo pidan.

## Las dos leyes asintóticas

- **Ley de los grandes números (LLN):** al muestrear muchas veces, el promedio empírico **converge a la esperanza verdadera**. Una moneda puede caer 5 caras seguidas, pero a la larga la proporción tiende a ½.
- **Teorema Central del Límite (CLT):** la distribución del **promedio muestral** tiende a una **normal**, sin importar la distribución original. Estandarizado: $\dfrac{\bar X_n-\mu}{\sigma/\sqrt n}\to N(0,1)$.

El CLT es la base de casi todo el testeo de hipótesis: por eso aproximamos por normal con muestras grandes, sea binomial, Poisson u otra.

## Prueba de hipótesis (la maquinaria del A/B test)

Pasos:
1. Plantea **$H_0$** (nula, el "no pasó nada" — p.ej. la campaña no cambió la conversión) y **$H_1$** (alternativa).
2. Calcula un **estadístico de prueba** y su **p-valor**.
3. Compara el p-valor con el nivel de significancia $\alpha$ (típico 0.05).

El **p-valor** es la probabilidad de observar un resultado al menos tan extremo como el visto **si $H_0$ fuera cierta**. p-valor bajo → evidencia para rechazar $H_0$. **Ojo:** no rechazar $H_0$ no la prueba verdadera, solo dice que no hubo evidencia suficiente.

- **Una cola** vs **dos colas:** según la alternativa sea direccional ($>$ o $<$) o de simple diferencia ($\ne$).
- **Tests comunes:** Z-test / t-test (medias), Chi-cuadrado (frecuencias observadas vs esperadas).

## Errores Tipo I y Tipo II

| | $H_0$ verdadera | $H_0$ falsa |
|---|---|---|
| **Rechazas $H_0$** | Tipo I (falso positivo), prob. $\alpha$ | Acierto (potencia $1-\beta$) |
| **No rechazas** | Acierto | Tipo II (falso negativo), prob. $\beta$ |

- **Tipo I (α):** condenar a un inocente — afirmar un efecto que no existe.
- **Tipo II (β):** dejar libre a un culpable — no detectar un efecto real.
- **Potencia** $=1-\beta$: prob. de detectar un efecto real; sube con el tamaño muestral.

Bajar α reduce falsos positivos pero sube β (y viceversa): es un trade-off que se equilibra con el tamaño de muestra.

## Intervalos de confianza

Un IC del 95% es un rango construido por un procedimiento que, repetido, **captura el parámetro verdadero el 95% de las veces**. No es "hay 95% de prob. de que μ esté aquí" (μ es fijo). Es complementario al test: si el IC del 95% no contiene el valor nulo, rechazas a α=0.05.

## Estimación: MLE y MAP

- **MLE (máxima verosimilitud):** elige el parámetro que **maximiza la probabilidad de los datos observados**, $\hat\theta=\arg\max_\theta L(\theta)$. Frecuentista, sin prior.
- **MAP (máximo a posteriori):** maximiza el **posterior** $\propto$ likelihood × prior → MLE más un prior bayesiano. Con prior uniforme, MAP = MLE.

Conexión con ML: muchas funciones de pérdida (p.ej. log-loss) salen de un MLE.

---

## Mini-ejemplo trabajado: por qué el A/B test "ve" diferencias pequeñas

Conversión control 10%, tratamiento 11%, con n=10 000 por grupo. ¿Es real? El SE de una proporción es √(p(1−p)/n) ≈ √(0.1·0.9/10 000) = 0.003. La diferencia 0.01 frente a un SE combinado de ~0.0042 da z ≈ 2.4 → p ≈ 0.016 < 0.05: **significativa**.

Pero el motor es la **√n**: con n=100 por grupo, el SE sería 10× mayor (0.03) y esa misma diferencia de 1 pp sería invisible (z≈0.24). El test no detecta efectos grandes; detecta efectos *frente al ruido*, y el ruido cae como 1/√n.

**Predicción antes de seguir:** con 50 millones de usuarios, ¿una diferencia de 0.01 pp será "significativa"? Respuesta: **casi seguro sí** — con n gigantesco el SE es minúsculo y cualquier diferencia cruza p<0.05. Por eso significancia estadística ≠ relevancia: hay que mirar el **tamaño del efecto**, no solo el p-valor. La potencia te deja ver hasta lo trivial.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "¿funcionó el cambio?" → test de hipótesis: H0 sin efecto, estadístico, p-valor vs α.
- **Contraejemplo (p-valor mal leído):** p=0.04 NO es "4% de que H0 sea cierta"; es P(dato tan extremo | H0). Confundirlo invierte el condicional, como leer sensibilidad por VPP.
- **Caso borde (no rechazar ≠ probar H0):** un test sin potencia (n chico) "no encuentra efecto" aunque exista (error tipo II). El borde recuerda que ausencia de evidencia no es evidencia de ausencia.

## Errores típicos

- **Conceptual:** interpretar el IC del 95% como "95% de probabilidad de que μ esté aquí"; μ es fijo, la cobertura es del procedimiento.
- **Técnico:** usar test de una cola cuando la pregunta es de simple diferencia (o viceversa).
- **De supuestos:** declarar "no hay efecto" sin haber calculado potencia/tamaño de muestra.

## Transferencia isomorfa

- **CLT y √n ↔ error estándar universal:** que el promedio muestral se vuelva normal con SE σ/√n es la misma raíz que escala la volatilidad y que rige el bootstrap (conecta con [[arena-q6]] y [[arena-pst2]]).
- **p-valor / tipo I-II ↔ tests clásicos y detección:** la maquinaria H0/α/potencia es la de Neyman-Pearson y la dualidad IC-test (conecta con [[arena-dg3]] y [[arena-cb3]]).
- **Tipo I/II ↔ falso positivo/negativo de un clasificador:** α y β son 1−especificidad y 1−sensibilidad; el costo de FP vs FN fija el umbral (conecta con [[arena-q2]]).
- **MLE / MAP ↔ verosimilitud y prior:** estimar maximizando los datos (MLE) o datos×prior (MAP) es el puente a la inferencia bayesiana y a las funciones de pérdida (conecta con [[arena-dg2]] y [[arena-b4]]).

Moraleja de la arista: *el test detecta señal frente a ruido, y el ruido cae como 1/√n; con n enorme todo es "significativo", así que mira el tamaño del efecto.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Promedio sobre muchas muestras" | LLN: converge a la esperanza |
| "Distribución del promedio muestral" | CLT → normal, estandariza a N(0,1) |
| "¿Funcionó la campaña / el cambio?" | Test de hipótesis: H0 = sin efecto, mira el p-valor |
| "¿Qué es un p-valor?" | P(dato tan extremo \| H0 cierta); NO la prob. de H0 |
| "Costo de un falso positivo vs negativo" | Tipo I (α) vs Tipo II (β), potencia 1−β |
| "Estima el parámetro desde los datos" | MLE; con prior → MAP |
| "Rango plausible del parámetro" | Intervalo de confianza (interpretación frecuentista) |

---

> **Síntesis:** La estadística de entrevista gira en torno a CLT (por qué todo se vuelve normal con n grande) y al testeo de hipótesis, que es el motor del A/B test: H0/H1, p-valor, α, errores Tipo I/II y potencia. Los intervalos de confianza son la otra cara del test. Y la estimación se reparte entre MLE (datos solos) y MAP (datos + prior). Cuidado con interpretar mal el p-valor y el IC: ambos hablan del procedimiento, no de la probabilidad de la hipótesis.

---

*Retrieval: cierra y responde: (1) enuncia el CLT en una frase; (2) define p-valor sin decir "probabilidad de que H0 sea cierta"; (3) ¿qué es un error Tipo I y uno Tipo II, y qué es la potencia?; (4) diferencia MLE de MAP.*
