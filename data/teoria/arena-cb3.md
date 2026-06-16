# Contraste de hipótesis: NP Lemma, LRT y tests UMP

## De qué trata esta lección (y qué sabrás hacer al final)

[[arena-dg3]] te enseñó a *usar* tests (t, χ², z). Esta lección responde la pregunta de fondo: **¿cuál es el mejor test posible?** La respuesta, sorprendentemente limpia, es el **lema de Neyman-Pearson**: el test óptimo siempre compara verosimilitudes contra un umbral. De ahí se construye todo: cuándo existe un test "uniformemente más potente" (UMP), qué hacer cuando no existe (el LRT universal), y por qué un p-valor pequeño no significa "$H_0$ improbable".

Al terminar podrás: (1) aplicar el lema NP para hallar el test más potente; (2) reconocer la **razón de verosimilitud monótona (MLR)** que extiende la optimalidad a tests unilaterales; (3) saber cuándo **no** existe UMP y recurrir al LRT; y (4) entender la distribución asintótica $\chi^2$ del LRT (Wilks). Cada idea entra por su intuición. Los teoremas (NP, Wilks) van en `[CAJA NEGRA OK]`: la intuición es lo que se evalúa.

> Profundiza el LRT que [[arena-dg2]] introdujo y la teoría de errores de [[arena-dg3]].

---

## Configuración: potencia y los dos errores

Contrastamos $H_0:\theta\in\Theta_0$ contra $H_1:\theta\in\Theta_1$. La herramienta central es la **función de potencia** $\beta(\theta)=P_\theta(X\in R)$: la probabilidad de rechazar $H_0$ cuando el valor verdadero es $\theta$. Es una sola curva que captura ambos errores según dónde caiga $\theta$:

| Error | Definición | Probabilidad |
|-------|------------|--------------|
| Tipo I (falso positivo) | rechazar $H_0$ siendo cierta | $\alpha=\sup_{\theta\in\Theta_0}\beta(\theta)$ |
| Tipo II (falso negativo) | no rechazar siendo falsa | $1-\beta(\theta)$, con $\theta\in\Theta_1$ |

El **nivel** $\alpha$ es el peor error tipo I (el supremo sobre $\Theta_0$); la **potencia** es $\beta(\theta)$ en la alternativa, y queremos **maximizarla** sujetos a no pasarnos del nivel. Todo el capítulo es: *fijo $\alpha$, ¿qué test da la potencia más alta?*

---

## Lema de Neyman-Pearson

`[CAJA NEGRA OK]` — *Qué asumir:* que el test más potente tiene la forma de abajo. *Qué sí razonar:* por qué un cociente de verosimilitudes es la decisión correcta. *Cuándo reabrir:* para probar optimalidad formalmente.

Para hipótesis **simples** $H_0:\theta=\theta_0$ vs $H_1:\theta=\theta_1$, el test **más potente** de nivel $\alpha$ rechaza $H_0$ cuando los datos son **mucho más compatibles con $\theta_1$ que con $\theta_0$**:

$$\frac{f(x\mid\theta_1)}{f(x\mid\theta_0)}>k,$$

con $k$ elegido para que $P_{\theta_0}(\text{razón}>k)=\alpha$. La intuición es la de un detective: cada dato es evidencia; la razón de verosimilitudes mide *cuánto* inclina la balanza hacia $\theta_1$, y rechazas cuando la inclinación supera el umbral que fija tu tolerancia a falsos positivos. Todo test óptimo es, en el fondo, **este** cociente.

**Ejemplo (Normal, $\sigma^2$ conocida), $H_0:\mu=\mu_0$ vs $H_1:\mu=\mu_1$ con $\mu_1>\mu_0$:** el cociente resulta ser creciente en $\sum x_i$, así que "razón $>k$" equivale a "$\bar X>c$". El famoso **test z unilateral** no es una regla inventada: es el cociente NP disfrazado.

---

## Razón de verosimilitud monótona (MLR)

El lema NP solo cubre hipótesis simples. Para extenderlo a unilaterales ($H_0:\theta\le\theta_0$) necesitamos que el cociente se porte bien al variar $\theta$. Una familia tiene **MLR en $T(x)$** si, para $\theta_2>\theta_1$, el cociente $f(x\mid\theta_2)/f(x\mid\theta_1)$ es **no decreciente** en $T(x)$. Intuición: "valores más grandes de $T$ siempre apuntan a $\theta$ más grande", sin ambigüedad.

Tienen MLR (en su suficiente): Normal, Poisson, Binomial, Exponencial, Gamma. **No** tiene MLR la **Cauchy** (su cociente sube y baja, sin monotonía). Esta propiedad es la que decide si existe un test óptimo único.

## Tests UMP (uniformemente más potentes)

Un test es **UMP de nivel $\alpha$** si tiene la mayor potencia posible **para todo $\theta$ en la alternativa**, simultáneamente. Es un ideal exigente, y el MLR es lo que lo hace alcanzable:

**Corolario (Karlin-Rubin):** si la familia tiene MLR en $T$, el test UMP para $H_0:\theta\le\theta_0$ vs $H_1:\theta>\theta_0$ **rechaza si $T>c$**, con $c$ tal que $P_{\theta_0}(T>c)=\alpha$.

| Distribución | Test UMP unilateral |
|-------------|----------------------|
| Normal $\sigma^2$ conocida, $H_0:\mu\le\mu_0$ | rechaza si $\bar X>\mu_0+z_\alpha\sigma/\sqrt n$ |
| Poisson, $H_0:\lambda\le\lambda_0$ | rechaza si $\sum X_i>c$ |
| Bernoulli, $H_0:p\le p_0$ | rechaza si $\sum X_i>c$ |
| Exponencial, $H_0:\theta\le\theta_0$ | rechaza si $\sum X_i>c$ |

**La advertencia crucial:** **no existe UMP para hipótesis bilaterales** $H_0:\theta=\theta_0$ vs $H_1:\theta\ne\theta_0$ en general. La razón es geométrica: para $\theta>\theta_0$ el mejor test rechaza a la derecha, y para $\theta<\theta_0$ a la izquierda; ningún test maximiza la potencia en ambos lados a la vez.

---

## Razón de verosimilitud (LRT): el método universal

Cuando no hay UMP (bilateral, hipótesis compuestas, parámetros de estorbo), se usa el **LRT**, que generaliza el cociente NP comparando la mejor verosimilitud bajo $H_0$ con la mejor sin restricción:

$$\lambda(x)=\frac{\sup_{\theta\in\Theta_0}L(\theta\mid x)}{\sup_{\theta\in\Theta}L(\theta\mid x)}\in(0,1].$$

Rechaza $H_0$ si $\lambda$ es **pequeño** (los datos son mucho más compatibles con el modelo libre que con el restringido). Su magia, el **teorema de Wilks**:

`[CAJA NEGRA OK]` — asume el resultado asintótico; su valor es que **no necesitas la distribución exacta del estadístico**.

$$-2\log\lambda(X)\ \xrightarrow{d}\ \chi^2\big(\dim\Theta-\dim\Theta_0\big)\quad\text{bajo }H_0.$$

Los grados de libertad son el número de restricciones que impone $H_0$. Esto convierte al LRT en el motor de los tests $t$, $F$, $\chi^2$ y del ANOVA — casi todos son un LRT con otro nombre.

## p-valores y la paradoja de Lindley

El **p-valor** es la probabilidad bajo $H_0$ de un estadístico tan extremo como el observado; rechazas si $p\le\alpha$. Pero cuidado con sobreinterpretarlo: la **paradoja de Lindley** muestra que, con $n$ **muy grande**, un p-valor de 0.04 puede coexistir con una probabilidad posterior $P(H_0\mid x)>0.5$ — es decir, "significativo" para el frecuentista y "probablemente cierto" para el bayesiano, **a la vez**. Un p pequeño mide *sorpresa bajo $H_0$*, no la verdad de $H_0$.

> **Predicción antes de seguir:** la Cauchy no tiene MLR. ¿Existe un test UMP unilateral para su parámetro de localización? Respuesta: **no** — sin monotonía del cociente, ni siquiera el caso unilateral admite un test óptimo único; el "mejor" test depende de cuál $\theta$ de la alternativa te importe. La MLR es justo la propiedad que salva el caso unilateral; sin ella, se cae a LRT o tests específicos.

---

## Mini-ejemplo trabajado: del cociente NP al test z

H₀: μ=0 vs H₁: μ=1, datos N(μ,1), n observaciones. El lema de Neyman-Pearson dice: el test **más potente** rechaza cuando la razón de verosimilitudes supera un umbral:

> L(1|x)/L(0|x) = exp(Σxᵢ − n/2) > k

Tomar logaritmo: Σxᵢ > k', es decir **X̄ > c**. El test óptimo no es una regla arbitraria: *cae* sobre el promedio, y c se fija para que P₀(X̄>c)=α. Así, el famoso test z unilateral es simplemente el cociente de verosimilitudes disfrazado.

**Predicción antes de seguir:** si la alternativa fuera bilateral (H₁: μ≠0), ¿sigue existiendo un único test más potente? Respuesta: **no** — para μ>0 conviene rechazar a la derecha y para μ<0 a la izquierda, y ningún test maximiza la potencia en *ambos* lados a la vez. Por eso no existe UMP bilateral en general; se recurre al LRT. La monotonía del cociente (MLR) es justo lo que salva el caso unilateral.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** familia con razón de verosimilitud monótona (MLR) en T → test UMP unilateral "rechaza si T>c".
- **Contraejemplo (Cauchy sin MLR):** la Cauchy no tiene MLR, así que ni siquiera el caso unilateral admite UMP simple; el cociente no es monótono.
- **Caso borde (paradoja de Lindley):** con n enorme, un p-valor de 0.04 puede convenir con P(H₀|datos)>0.5. El borde revela que p pequeño no es "H₀ improbable"; frecuentista y bayesiano divergen.

## Errores típicos

- **Conceptual:** leer el p-valor como P(H₀|datos); es P(estadístico tan extremo | H₀), el mismo condicional invertido que confunde sensibilidad con VPP.
- **Técnico:** usar χ²(1) para −2lnλ cuando hay r restricciones (debe ser χ²(r)) o cerca de un borde del espacio paramétrico (la asintótica de Wilks falla).
- **De supuestos:** buscar un UMP bilateral donde no existe en vez de usar el LRT.

## Transferencia isomorfa

- **Cociente de verosimilitudes NP ↔ likelihood ratio de un test diagnóstico:** "rechaza si L(H₁)/L(H₀)>k" es exactamente actualizar odds con LR⁺; el umbral k fija el trade-off sensibilidad/especificidad (conecta con [[arena-q2]]).
- **Función de potencia / UMP ↔ ROC y umbral óptimo:** elegir c que maximiza la potencia a α fijo es deslizarse por la curva ROC hasta el punto de operación; Neyman-Pearson *es* la teoría de detección óptima (conecta con [[arena-htd4]]).
- **LRT −2lnλ ~ χ²(r) ↔ comparación de modelos anidados:** el test de razón de verosimilitudes sustenta selección por verosimilitud, F-tests y deviance de GLM (conecta con [[arena-dg2]]).
- **p-valor uniforme bajo H₀ ↔ calibración:** que p~U(0,1) cuando H₀ es cierta es la base de chequear si un test (o un modelo) está bien calibrado (conecta con [[arena-dg3]]).

Moraleja de la arista: *el test óptimo siempre es un cociente de verosimilitudes contra un umbral; deslizar ese umbral es recorrer la ROC, y un p pequeño mide sorpresa bajo H₀, no la verdad de H₀.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Hipótesis simples vs simple, test más potente" | NP Lemma: rechaza si L(θ₁)/L(θ₀) > k |
| "Hipótesis unilateral, familia con MLR" | Test UMP: rechaza si T > c |
| "No existe UMP bilateral" | LRT o test de dos colas si familia exponencial unilateral |
| "Hipótesis compuesta, parámetros bajo H₀" | LRT: λ=sup_{Θ₀}L / sup_{Θ}L |
| "Distribución asintótica del LRT" | −2 log λ →_d χ²_r (r = grados de libertad de H₀) |
| "Medir evidencia sin umbral fijo" | p-valor: probabilidad de datos más extremos bajo H₀ |

---

> **Síntesis (Casella & Berger, Ch 8):** El lema NP fija el ideal (test más potente entre todos de nivel α). El MLR lo extiende a familias unilaterales. El LRT es el método universal para hipótesis compuestas; su distribución asintótica chi-cuadrado lo hace omnipresente. El p-valor es la moneda del reino, pero tiene límites bayesianos serios con n grande.

---

*Retrieval: (1) Enuncia el lema de Neyman-Pearson y da su región de rechazo. (2) X₁,…,Xₙ i.i.d. Poisson(λ), H₀: λ≤1 vs H₁: λ>1: ¿cuál es el test UMP? (3) ¿Cuándo NO existe test UMP? (4) Da la distribución asintótica de −2 log λ bajo H₀.*
