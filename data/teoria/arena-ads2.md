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
