# Estadística e inferencia para entrevistas

## De qué trata esta lección (y qué sabrás hacer al final)

La inferencia estadística responde una sola pregunta de fondo: **¿lo que veo en mis datos es señal real o ruido de muestreo?** Mediste 11% de conversión en el grupo nuevo contra 10% en el viejo; ¿el producto mejoró, o es la diferencia que esperarías por puro azar? Esta lección construye, desde cero, la maquinaria que contesta eso: por qué los promedios se vuelven normales (CLT), cómo se monta un test de hipótesis (el motor del A/B test), qué errores puede cometer, y cómo se estima un parámetro (MLE/MAP).

Al terminar podrás: (1) explicar por qué el ruido de un promedio cae como $1/\sqrt{n}$; (2) plantear y leer un test de hipótesis sin confundir el p-valor; (3) razonar el trade-off entre falsos positivos y falsos negativos; (4) interpretar un intervalo de confianza correctamente; y (5) distinguir estimar con datos solos (MLE) de datos + creencia previa (MAP). Cada idea entra primero como intuición y solo después como fórmula.

---

## El vocabulario mínimo: esperanza, varianza, covarianza

Antes de inferir hay que poder **resumir** una variable aleatoria con dos números: dónde está centrada y cuánto se dispersa.

- **Esperanza** $E[X]=\int x\,f_X(x)\,dx$ — el "centro de gravedad": cada valor pesa por su densidad $f_X$. Es el promedio que obtendrías a la larga.
- **Varianza** $\mathrm{Var}(X)=E[X^2]-(E[X])^2$ — cuánto se aleja $X$ de su media en promedio (al cuadrado); siempre $\ge 0$. Su raíz, la **desviación estándar**, vuelve a las unidades originales.
- **Covarianza** $\mathrm{Cov}(X,Y)=E[XY]-E[X]E[Y]$ — si $X$ e $Y$ tienden a subir juntas (positiva) o en sentidos opuestos (negativa). Mide relación **lineal**.
- **Correlación** $\rho=\dfrac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\,\mathrm{Var}(Y)}}\in[-1,1]$ — la covarianza normalizada a una escala interpretable: −1 (anti), 0 (sin relación lineal), +1 (perfecta).

No memorices derivaciones de cada distribución, pero sí practica **derivar** la media y varianza de las comunes (uniforme, exponencial) si lo piden: es un chequeo de que entiendes las definiciones, no solo las fórmulas.

## Las dos leyes asintóticas: por qué los datos "se portan" con muchas muestras

Toda la inferencia descansa en dos teoremas sobre qué pasa cuando $n$ (el tamaño de muestra) crece.

- **Ley de los grandes números (LLN):** el **promedio empírico** $\bar X_n$ converge a la esperanza verdadera $\mu$. Una moneda justa puede dar 5 caras seguidas, pero a la larga la proporción se acerca a ½. Intuición: el azar de cada dato se va promediando hasta cancelarse.
- **Teorema Central del Límite (CLT):** la *distribución* del promedio muestral $\bar X_n$ se vuelve **normal** (campana) **sin importar** la forma original de los datos. Estandarizado:

$$\frac{\bar X_n-\mu}{\sigma/\sqrt n}\to N(0,1).$$

Lee esa fórmula con calma: $\bar X_n-\mu$ es "cuánto se desvía el promedio de la verdad"; se divide por $\sigma/\sqrt n$, el **error estándar**, que es cuánto fluctúa típicamente ese promedio. El motor es la **$\sqrt n$**: el ruido del promedio encoge como $1/\sqrt n$, así que para halve el ruido necesitas 4× los datos. El CLT es la razón de que aproximemos casi todo por normal con $n$ grande, sea el dato original binomial, Poisson u otra cosa.

## Prueba de hipótesis: la maquinaria del A/B test

Un test de hipótesis formaliza "¿es señal o ruido?". Los pasos:

1. Plantea **$H_0$** (la hipótesis nula, el "no pasó nada" — la campaña *no* cambió la conversión) y **$H_1$** (la alternativa, "sí cambió").
2. Calcula un **estadístico de prueba** (resume los datos en un número) y su **p-valor**.
3. Compáralo con el **nivel de significancia** $\alpha$ (típico 0.05): si el p-valor $<\alpha$, rechazas $H_0$.

El concepto que más se malinterpreta es el **p-valor**: es la probabilidad de observar un resultado **al menos tan extremo** como el visto, **suponiendo que $H_0$ es cierta**. Un p-valor bajo significa "estos datos serían raros si no pasara nada" → evidencia para rechazar $H_0$. **Ojo a dos trampas:** (a) el p-valor **no** es "la probabilidad de que $H_0$ sea cierta" (eso invierte el condicional, igual que confundir sensibilidad con VPP); (b) **no rechazar $H_0$ no la prueba verdadera** — solo dice que no hubo evidencia suficiente.

- **Una cola** vs **dos colas:** usa una cola si la alternativa es direccional ($H_1:\mu>\mu_0$ o $<$), dos colas si es de simple diferencia ($\ne$).
- **Tests comunes:** Z-test / t-test (comparar medias), Chi-cuadrado (frecuencias observadas vs esperadas).

## Errores Tipo I y Tipo II: los dos modos de equivocarse

Como decides con datos ruidosos, puedes fallar de dos maneras. La analogía judicial lo fija de inmediato ($H_0$ = "el acusado es inocente"):

| | $H_0$ verdadera | $H_0$ falsa |
|---|---|---|
| **Rechazas $H_0$** | Tipo I (falso positivo), prob. $\alpha$ | Acierto (potencia $1-\beta$) |
| **No rechazas** | Acierto | Tipo II (falso negativo), prob. $\beta$ |

- **Tipo I ($\alpha$):** condenar a un inocente — afirmar un efecto que no existe.
- **Tipo II ($\beta$):** dejar libre a un culpable — no detectar un efecto real.
- **Potencia** $=1-\beta$: la probabilidad de detectar un efecto real cuando lo hay. Sube con el **tamaño de muestra** y con el tamaño del efecto.

El trade-off clave: bajar $\alpha$ (ser más exigente para gritar "efecto") reduce falsos positivos pero **sube** $\beta$ (más falsos negativos), y viceversa. La única forma de mejorar ambos a la vez es **más datos**. Por eso "¿qué $n$ necesito?" es una pregunta de potencia, no de capricho.

## Intervalos de confianza: el rango y su interpretación delicada

Un **intervalo de confianza (IC) del 95%** es un rango construido por un procedimiento que, **si lo repitieras muchas veces**, capturaría el parámetro verdadero el 95% de las veces. La sutileza que te van a probar: **no** es "hay 95% de probabilidad de que $\mu$ esté en este intervalo concreto". El parámetro $\mu$ es fijo (no aleatorio); lo aleatorio es el intervalo, que cambia con cada muestra. La cobertura es una propiedad del **procedimiento**, no de un intervalo particular.

El IC es la otra cara del test: si el IC del 95% **no contiene** el valor nulo, rechazas $H_0$ a $\alpha=0.05$. Dan exactamente la misma decisión, pero el IC además te dice **cuánto** y con qué precisión, no solo "sí/no".

## Estimación: MLE y MAP

¿Cómo eliges el valor de un parámetro $\theta$ a partir de datos? Dos filosofías:

- **MLE (máxima verosimilitud):** elige el $\theta$ que hace **más probables los datos que observaste**, $\hat\theta=\arg\max_\theta L(\theta)$, donde $L(\theta)=P(\text{datos}\mid\theta)$ es la verosimilitud. Intuición: "¿qué moneda explica mejor que salieran 7 caras de 10?" → la de $p=0.7$. Es frecuentista: sin creencia previa.
- **MAP (máximo a posteriori):** maximiza el **posterior** $\propto$ likelihood $\times$ prior. Es MLE más un prior bayesiano que regulariza hacia lo que ya creías. Caso límite revelador: con **prior uniforme** (no creo nada en particular), MAP $=$ MLE.

Conexión con ML que vale oro en entrevista: muchas **funciones de pérdida** salen de un MLE. Minimizar el error cuadrático equivale a MLE bajo ruido normal; la **log-loss** (entropía cruzada) es el MLE de un modelo Bernoulli/multinomial. "Entrenar" es, muchas veces, maximizar verosimilitud disfrazada de minimizar pérdida.

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
