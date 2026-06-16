# Intervalos de confianza y tests de hipótesis

## De qué trata esta lección (y qué sabrás hacer al final)

Estimar un parámetro con un solo número esconde algo crucial: **cuánta incertidumbre tienes**. Un intervalo de confianza la hace explícita ("μ está entre 4.3 y 7.6"), y un test de hipótesis la convierte en una decisión ("¿hay evidencia de que cambió?"). Esta lección construye ambos desde cero, y revela que **son el mismo objeto visto de dos lados**: un IC es el conjunto de valores que un test no rechazaría.

Al terminar podrás: (1) construir un IC con la técnica del **pivote** y elegir entre z, t y χ²; (2) montar un test de hipótesis y leer correctamente el **p-valor** (sin el error clásico de invertir el condicional); (3) razonar el trade-off entre errores tipo I y II y calcular el tamaño de muestra para una potencia dada; y (4) corregir por **tests múltiples**. Cada herramienta entra por su intuición; la √n —el motor de toda la precisión— aparece una y otra vez.

> Comparte raíces con la versión aplicada en [[arena-ads2]] (p-valor, α/β, potencia) y profundiza hacia la teoría en [[arena-cb3]] (tests óptimos) y [[arena-cb4]] (IC asintóticos).

---

## Intervalos de confianza: la técnica del pivote

Primero, qué **es** un IC del 95%: un intervalo construido por un procedimiento que, repetido muchas veces, atrapa el parámetro verdadero el 95% de las veces. (Ojo: el parámetro es fijo; lo aleatorio es el intervalo. Detalle en [[arena-cb4]].)

¿Cómo se construye? Con un **pivote**: una función $Q(X,\theta)$ que mezcla datos y parámetro pero cuya **distribución es conocida y no depende de $\theta$**. La idea es astuta: si conozco la distribución de $Q$, sé entre qué cuantiles cae con probabilidad $1-\alpha$, y despejando $\theta$ de esa desigualdad obtengo el intervalo:

$$P\big(q_{\alpha/2}\le Q(X,\theta)\le q_{1-\alpha/2}\big)=1-\alpha\ \xrightarrow{\text{despejar }\theta}\ \text{IC}.$$

| Problema | Pivote | Distribución |
|---------|--------|-------------|
| $\mu$, $\sigma$ conocida | $(\bar X-\mu)/(\sigma/\sqrt n)$ | $N(0,1)$ |
| $\mu$, $\sigma$ desconocida | $(\bar X-\mu)/(S/\sqrt n)$ | $t(n-1)$ |
| $\sigma^2$ | $(n-1)S^2/\sigma^2$ | $\chi^2(n-1)$ |
| $p$ (Bernoulli) | $(\hat p-p)/\sqrt{p(1-p)/n}$ | $N(0,1)$ aprox. |

### IC para la media (σ conocida)

El más simple. El pivote $(\bar X-\mu)/(\sigma/\sqrt n)$ es $N(0,1)$, así que el IC es

$$\bar X \pm z_{\alpha/2}\,\frac{\sigma}{\sqrt n},$$

donde $z_{\alpha/2}$ es el cuantil de la normal (90%: 1.645; **95%: 1.96**; 99%: 2.576). El **semiancho** $ME=z_{\alpha/2}\,\sigma/\sqrt n$ es el "margen de error". Para garantizar $ME\le e$ despejas $n$:

$$n\ge\Big(\frac{z_{\alpha/2}\,\sigma}{e}\Big)^2.$$

Lee la dependencia: para **halve** el margen, necesitas **4×** los datos. La √n otra vez.

### IC para la media (σ desconocida — t de Student)

Aquí surge la sutileza que hace famosa a la $t$. Si no conoces $\sigma$, la estimas con $S$ — pero $S$ es ruidosa, sobre todo con pocos datos, así que el pivote ya no es normal sino **$t$ de Student** con $n-1$ grados de libertad, una campana de **colas más gruesas** que compensan esa incertidumbre extra:

$$\bar X \pm t_{\alpha/2,\,n-1}\,\frac{S}{\sqrt n}.$$

Con $n\ge 30$, la $t$ es casi idéntica a la $z$ (las colas se adelgazan al crecer $n$). Con $n$ pequeño, usar $z$ en vez de $t$ **subestima** el ancho: error clásico.

### IC para la varianza

El pivote $(n-1)S^2/\sigma^2$ es $\chi^2(n-1)$, una distribución **asimétrica**. Por eso el IC de $\sigma^2$,

$$\left[\frac{(n-1)S^2}{\chi^2_{1-\alpha/2,\,n-1}},\ \frac{(n-1)S^2}{\chi^2_{\alpha/2,\,n-1}}\right],$$

**no** se centra en $S^2$: la forma del pivote dicta la forma del intervalo. Usar un $\pm$ simétrico aquí es un error.

---

## Tests de hipótesis: la estructura

Un test convierte "¿señal o ruido?" en una decisión formal. Las piezas:

| Componente | Definición |
|------------|-----------|
| $H_0$ | hipótesis nula (el "status quo", no pasó nada) |
| $H_1$ | alternativa (lo que quieres demostrar) |
| Estadístico $T$ | resumen de los datos |
| Región de rechazo | valores de $T$ incompatibles con $H_0$ |
| Nivel $\alpha$ | $P(\text{rechazar }H_0\mid H_0\text{ cierta})$ = error tipo I |
| Potencia | $P(\text{rechazar }H_0\mid H_1\text{ cierta})$ = $1-$ error tipo II |

La regla: rechaza $H_0$ si $T$ cae en la región de rechazo. Todo el arte está en elegir esa región para controlar los dos errores.

## El p-valor (y su trampa)

El **p-valor** es la probabilidad, **suponiendo $H_0$ cierta**, de observar un estadístico tan extremo o más que el visto:

$$p\text{-valor}=P(\text{tan extremo o más}\mid H_0).$$

Si $p<\alpha$, rechazas. Datos clave para no equivocarte: bajo $H_0$, el p-valor es **Uniforme$[0,1]$** (cualquier valor es igual de probable). Y lo que **NO** es: no es $P(H_0\text{ cierta})$ ni $P(\text{ver estos datos})$. Confundir $P(\text{datos}\mid H_0)$ con $P(H_0\mid\text{datos})$ es el mismo condicional invertido que la falacia de la tasa base. Para un test bilateral, $p=2\,P(Z>|z_{\text{obs}}|)$.

## Errores tipo I y tipo II

| | $H_0$ verdadera | $H_0$ falsa |
|--|--------------|----------|
| Rechazar $H_0$ | error tipo I ($\alpha$) | correcto (potencia) |
| No rechazar | correcto ($1-\alpha$) | error tipo II ($\beta$) |

El **trade-off**: con $n$ fijo, bajar $\alpha$ (más exigente para gritar "efecto") **sube** $\beta$ (más efectos reales que se escapan). La única forma de reducir ambos a la vez es **aumentar $n$**. Por eso el diseño de muestra es una pregunta de potencia, no un capricho.

---

## Tests t para una y dos muestras

**Una muestra** ($H_0:\mu=\mu_0$): el estadístico $t=(\bar X-\mu_0)/(S/\sqrt n)\sim t(n-1)$ bajo $H_0$; rechazas si $|t|>t_{\alpha/2,n-1}$. La **dualidad IC↔test**: rechazar $H_0:\mu=\mu_0$ al nivel $\alpha$ es exactamente que $\mu_0$ **no** esté en el IC del $(1-\alpha)$.

**Dos muestras** ($H_0:\mu_1=\mu_2$, varianzas posiblemente distintas — test de Welch):

$$t=\frac{\bar X_1-\bar X_2}{\sqrt{S_1^2/n_1+S_2^2/n_2}},$$

con grados de libertad de Welch $\nu$ (una fórmula que pondera las dos varianzas). El denominador es el error estándar de la *diferencia*: suma de las incertidumbres de cada media.

## Tests chi-cuadrado

Para datos de **conteo/categorías**, el estadístico compara lo observado $O_i$ con lo esperado $E_i$ bajo $H_0$:

$$\chi^2=\sum_i\frac{(O_i-E_i)^2}{E_i}.$$

Cada término mide "cuánto se desvía esta celda, en relación a su tamaño esperado". Dos usos: **bondad de ajuste** (¿siguen los datos la distribución $f(x\mid\theta_0)$?, con $\chi^2(k-1-p)$ grados de libertad, $k$ categorías y $p$ parámetros estimados) e **independencia** en una tabla de contingencia ($\chi^2((r-1)(c-1))$, con $E_{ij}=(\text{total fila}_i)(\text{total col}_j)/n$).

## Diseño del tamaño de muestra

Para detectar un efecto $\delta=\mu_1-\mu_0$ con nivel $\alpha$ y potencia $1-\beta$ (test z unilateral):

$$n=\frac{(z_\alpha+z_\beta)^2\,\sigma^2}{(\mu_1-\mu_0)^2}.$$

Lee la fórmula como diseño de experimento: cuanto **menor** el efecto que quieres detectar ($\delta$ chico), **más** datos necesitas (crece con $1/\delta^2$). Para $\alpha=0.05$ y potencia 80%, $n\approx 7.85\,\sigma^2/\delta^2$.

## Corrección de tests múltiples

Si corres $m$ tests independientes a nivel $\alpha$, la probabilidad de **al menos un** falso positivo (FWER) es $1-(1-\alpha)^m\approx m\alpha$. Con 20 tests a 0.05, esperas ~1 falso positivo por puro azar. Dos antídotos:

- **Bonferroni:** usa $\alpha/m$ en cada test → garantiza FWER $\le\alpha$. Simple pero conservador.
- **Benjamini-Hochberg (BH):** controla el **FDR** (fracción de falsos entre los rechazados), no el FWER. Más potente cuando hay muchos tests.

> **Predicción antes de seguir:** ¿qué pasa con el p-valor si miras los datos repetidamente y paras en cuanto cruza 0.05 ("peeking")? Respuesta: **inflas el error tipo I** muchísimo — cada "vistazo" es otro test, y con suficientes vistazos casi siempre cruzarás 0.05 por azar aunque $H_0$ sea cierta. Es el mismo problema de tests múltiples disfrazado de tiempo. Por eso los A/B tests fijan $n$ y el momento de mirar **antes** de empezar.

---

## Mini-ejemplo trabajado: test t y su IC dual, a mano

n=25, X̄=6, S=4, y quieres contrastar H₀: μ=5. El estadístico:

> t = (X̄ − μ₀)/(S/√n) = (6 − 5)/(4/5) = 1/0.8 = **1.25**

Con 24 grados de libertad, el crítico bilateral al 5% es ≈2.064. Como |1.25| < 2.064, **no rechazas H₀**. Y de forma equivalente, el IC del 95% es 6 ± 2.064·0.8 = (4.35, 7.65), que **contiene** el 5. Misma decisión por dos caminos: ese es el principio de dualidad IC↔test.

**Predicción antes de seguir:** si cuadruplicas el tamaño a n=100 (mismos X̄, S), ¿qué le pasa al estadístico y al ancho del IC? Respuesta: el error estándar S/√n cae a la **mitad** (√100=10 vs 5), así que t≈2.5 (ahora *sí* rechazas) y el IC se estrecha a la mitad. Cuadruplicar n duplica la precisión — la misma √n de σ/√n que aparece por todas partes. No es que el efecto crezca; es que lo ves mejor.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** un parámetro, un pivote con distribución conocida (z, t, χ²) → construyes IC y test simultáneamente.
- **Contraejemplo (p-valor mal leído):** p=0.03 NO es "97% de que H₁ sea cierta" ni "3% de que los datos sean azar"; es P(datos tan extremos | H₀). Confundirlo con P(H₀|datos) es el mismo error de condicional invertido que la tasa base.
- **Caso borde (IC de σ² asimétrico):** como la χ² no es simétrica, el IC de la varianza no se centra en S²; usar ± simétrico es incorrecto. El borde recuerda que el pivote dicta la forma.

## Errores típicos

- **Conceptual:** interpretar "no rechazar H₀" como "H₀ es verdadera"; solo significa evidencia insuficiente.
- **Técnico:** usar z en vez de t con n pequeño y σ desconocida (subestima el ancho del IC).
- **De supuestos:** correr m tests y reportar el p<0.05 más bonito sin corregir (FWER ≈ m·α); con 20 tests, esperas ~1 falso positivo por azar.

## Transferencia isomorfa

- **Error tipo I/II ↔ falso positivo/negativo de un clasificador:** α y β son exactamente 1−especificidad y 1−sensibilidad; la curva de potencia es la ROC del test (conecta con [[arena-q2]] y [[arena-htd4]]).
- **p-valor uniforme bajo H₀ ↔ transformada integral:** que p~U(0,1) cuando H₀ es cierta es la misma propiedad CDF→uniforme de la valoración probabilística (conecta con [[arena-q6]]).
- **Corrección de tests múltiples ↔ peeking en A/B testing:** mirar muchas métricas o parar temprano infla el error tipo I; Bonferroni/BH son el antídoto, igual que en experimentación online (conecta con [[arena-obs1]], monitoreo de muchas señales).
- **Tamaño de muestra n≈(z_α+z_β)²σ²/δ² ↔ MDE de un experimento:** diseñar potencia es elegir el efecto mínimo detectable antes de lanzar (conecta con [[arena-dmls3]], rollout/experimentos).

Moraleja de la arista: *IC y test son el mismo objeto visto de dos lados; el p-valor mide sorpresa bajo H₀, no la verdad de H₀; y la √n manda en la precisión.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "IC con σ conocida" | z_{α/2}·σ/√n |
| "IC con σ desconocida" | t_{α/2,n-1}·S/√n |
| "IC para σ²" | Chi-cuadrado (asimétrico) |
| "¿Rechazar H₀?" | p-value < α |
| "Cuántas obs para ME ≤ e" | n ≥ (z_{α/2}·σ/e)² |
| "Cuántas obs para potencia 80%" | n ≈ 7.85·σ²/δ² (nivel 5%) |
| "m tests simultáneos" | Bonferroni: α/m cada uno |

---

> **Síntesis:** El IC y el test de hipótesis son duales: H₀ se rechaza al nivel α ↔ θ₀ no está en el IC al (1-α)%. El pivote es la clave para construir ambos. El p-value es una medida de evidencia, no de probabilidad de H₀. El balance errores tipo I / tipo II se controla aumentando n.

---

*Retrieval: cierra y responde: (1) IC del 99% para μ: n=36, X̄=100, σ=15; (2) estadístico t y p-value para H₀:μ=5, n=25, X̄=6, S=4; (3) n para ME=0.1 con σ=1 al 95%; (4) χ² crítico para bondad de ajuste con k=5 categorías, nivel 5%.*
