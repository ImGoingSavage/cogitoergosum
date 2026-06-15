# Arena Quant · Movimiento browniano, Itô y martingalas

## De qué trata (y qué sabrás hacer)

Este es el corazón de la valoración moderna. Dos herramientas resuelven casi todo: el **muestreo opcional** (si un proceso es una "apuesta justa", su valor esperado al detenerte es su valor inicial) y la **fórmula de Itô** (la regla de la cadena cuando la variable tiene ruido browniano, con un término extra de segundo orden). Suenan abstractas; aquí se construyen desde un paseo aleatorio y un par de cuentas a mano.

Al terminar sabrás recitar qué es el movimiento browniano, usar el muestreo opcional para resolver barreras en una línea, aplicar Itô para pasar de un proceso a otro, y reconocer cuándo algo es martingala. Cada idea se ancla en un ejemplo numérico.

---

## Movimiento browniano — la definición que debes recitar

$W_t$ es un **movimiento browniano** si $W_0=0$, sus incrementos son independientes, y $W_t-W_s\sim N(0,\,t-s)$. Es el límite de un paseo aleatorio con pasos infinitesimales. Consecuencias notables: es continuo en todas partes pero diferenciable en ninguna; cruza cualquier nivel infinitas veces en un instante; y su covarianza es $E[W_s W_t]=\min(s,t)$ (truco: escribe $W_t=W_s+(W_t-W_s)$ y usa que el incremento es independiente de $W_s$).

---

## Muestreo opcional en acción

Una **martingala** es un proceso cuya esperanza futura, dado el presente, es su valor actual (un juego justo). El **teorema del muestreo opcional** dice que si paras en un tiempo $\tau$ de esperanza finita, $E[X_\tau]=X_0$.

Ejemplo: paseo aleatorio en $[0,1000]$ que arranca en 80, $\pm1$ con probabilidad $\tfrac12$. ¿$P(\text{toca 0 antes que 1000})$? La posición es una martingala y el tiempo de salida tiene esperanza finita, así que $E[\text{posición al parar}]=80$. Como al parar solo vale 0 o 1000, si $p=P(\text{tocar }1000)$ entonces $1000p=80\Rightarrow p=0.08$, y $P(\text{tocar }0)=0.92$. La probabilidad de absorción es **lineal** en el punto de partida cuando el paso es justo.

---

## Itô: convertir un proceso en otro

Para el browniano geométrico $dS_t=\mu S_t\,dt+\sigma S_t\,dW_t$, el lema de Itô da:

$$d(\ln S_t)=\left(\mu-\frac{\sigma^2}{2}\right)dt+\sigma\,dW_t \;\Rightarrow\; S_t=S_0\exp\!\left(\left(\mu-\tfrac{\sigma^2}{2}\right)t+\sigma W_t\right).$$

El término $-\sigma^2/2$ (la "corrección de Itô") es la diferencia entre la media aritmética y la geométrica de los retornos — fuente de incontables errores. La razón profunda es que $(dW)^2=dt$: el ruido browniano tiene una variación cuadrática que no se desprecia, y obliga a conservar el término $\tfrac12 f''(dW)^2$ de la expansión de Taylor.

---

## ¿Es martingala? El test de la deriva cero

Aplica Itô y mira si sobrevive algún término $dt$ (deriva):

- $W_t^3$: $d(W_t^3)=3W_t\,dt+3W_t^2\,dW_t$ → hay deriva $3W_t$ → **NO** es martingala.
- $\cosh(\lambda W_t)\,e^{-\lambda^2 t/2}$: todos los $dt$ se cancelan → **SÍ**. Igual que $W_t^2-t$, $W_t^3-3tW_t$ y $e^{\sigma W_t-\sigma^2 t/2}$.

Regla mnemónica: una función $f(W_t)$ sin dependencia explícita en $t$ es martingala solo si $f$ es lineal (su deriva $\tfrac12 f''$ debe anularse en esperanza). Añadir el factor temporal correcto "mata" la deriva.

---

## Dos resultados que sorprenden

- **El cociente $W_t/Z_t$ de dos brownianos independientes es Cauchy estándar** (cociente de dos normales centradas). Por eso no tiene media: las colas pesadas aparecen al dividir.
- **Si $X_0=0$ y $X_1>0$, ¿$P(X_2<0)$?** Por simetría de los incrementos: necesitas $X_2-X_1$ negativo (prob $\tfrac12$) y de magnitud mayor que $X_1$ (prob $\tfrac12$ por igual distribución) → $\tfrac14$.

---

## El proceso de Ornstein–Uhlenbeck (reversión a la media)

$$dX_t=\theta(\mu-X_t)\,dt+\sigma\,dW_t.$$

Se resuelve con el factor integrante $e^{\theta t}$, dando $X_t=X_0 e^{-\theta t}+\mu(1-e^{-\theta t})+\int_0^t \sigma e^{\theta(s-t)}\,dW_s$. El parámetro $\theta$ controla la velocidad de reversión hacia $\mu$. Es el modelo base de tasas de interés (Vasicek) y de spreads. Y $(dW_t)^2=dt$ no es magia: dice que la variación cuadrática del browniano crece a razón 1 por unidad de tiempo, por eso el término de segundo orden sobrevive en Itô.

---

## Mini-ejemplo trabajado: barrera por muestreo opcional

Paseo aleatorio simétrico ($\pm1$ con prob $\tfrac12$) que arranca en 80, dentro de $[0,1000]$. ¿$P(\text{toca 0 antes que 1000})$? La posición $X_t$ es una **martingala**: $E[X_{t+1}\mid X_t]=\tfrac12(X_t+1)+\tfrac12(X_t-1)=X_t$. El tiempo de salida $\tau$ tiene esperanza finita, así que por muestreo opcional $E[X_\tau]=X_0=80$. Pero $X_\tau$ solo vale 0 o 1000:

$$1000\,p+0\,(1-p)=80 \;\Rightarrow\; p=P(\text{tocar }1000)=0.08 \;\Rightarrow\; P(\text{tocar }0)=0.92.$$

La probabilidad de absorción es **lineal** en el punto de partida cuando el paso es justo: empezar en 80 de 1000 → 92% de caer al 0.

**Predicción antes de seguir:** si el paseo tuviera una ligera deriva positiva (prob de subir $>\tfrac12$), ¿la probabilidad de tocar 1000 sube o baja respecto a 0.08? Respuesta: **sube** — ya no es martingala, la deriva empuja hacia arriba y la relación lineal se curva (la ruina del jugador con sesgo da una fórmula exponencial). El argumento de martingala solo vale con paso justo.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** ¿es martingala? aplica Itô y exige que el término $dt$ se anule. $W_t^2-t$, $W_t^3-3tW_t$, $e^{\sigma W_t-\sigma^2 t/2}$ sí lo son.
- **Contraejemplo (parece martingala, no lo es):** $W_t^3$ tiene $d(W_t^3)=3W_t^2\,dW_t+3W_t\,dt$ → la deriva $3W_t$ sobrevive → NO es martingala. El cubo "se ve simétrico" pero la convexidad mete deriva.
- **Caso borde (cociente de normales):** $W_t/Z_t$ de dos brownianos independientes es Cauchy: sin media. Dividir crea colas pesadas donde no las había.

## Errores típicos

- **Conceptual:** olvidar la corrección de Itô $-\sigma^2/2$ al pasar de $S$ a $\ln S$, confundiendo media aritmética con geométrica de los retornos.
- **Técnico:** aplicar muestreo opcional sin verificar que el tiempo de parada tenga esperanza finita (si no, el teorema no garantiza $E[X_\tau]=X_0$).
- **De supuestos:** suponer que escalar la volatilidad con $\sqrt T$ vale siempre; bajo reversión a la media (OU) crece más lento.

## Transferencia isomorfa

- **Muestreo opcional ↔ no-arbitraje y precio justo:** "una martingala vale hoy lo que su esperanza futura" es la versión probabilística de "bajo la medida neutral al riesgo, el precio descontado es martingala" (conecta con [[arena-q5]], delta-hedge y EDP de B-S).
- **Corrección $-\sigma^2/2$ de Itô ↔ prima de Jensen $+\sigma^2/2$:** el mismo término que baja el drift del log-precio sube la media del precio (conecta con [[arena-q7]]).
- **Probabilidad de absorción lineal ↔ ruina del jugador / parada óptima:** "empezar en $x$ de $N$ → $x/N$ de tocar arriba" es el esqueleto de la ruina del jugador y del valor de continuar (conecta con [[arena-q8]]).
- **Cauchy del cociente ↔ varianza infinita:** las colas que rompen el TLC aparecen igual al dividir normales (conecta con [[arena-q9]]).

Moraleja de la arista: *si algo es martingala, su esperanza al parar es su valor inicial — eso resuelve barreras en una línea; un proceso es martingala exactamente cuando Itô le deja deriva cero.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "$P(\text{tocar barrera A antes que B})$" | martingala + muestreo opcional → lineal en el inicio |
| "proceso de $\ln S$ / $S^2$" | Itô; cuidado con la corrección $-\sigma^2/2$ |
| "¿es martingala?" | aplica Itô, exige deriva ($dt$) nula |
| "cociente de dos normales" | Cauchy (sin media) |
| "reversión a la media" | OU; factor integrante $e^{\theta t}$ |

> ❧ **Síntesis:** el muestreo opcional resuelve barreras y "valores justos" en una línea; Itô traduce un proceso en otro con su corrección de segundo orden; y un proceso es martingala exactamente cuando Itô deja deriva cero. El $-\sigma^2/2$ lognormal y $dt=(dW)^2$ son los dos detalles que separan al que entrenó del que improvisa.

---

*Retrieval: cierra la página y responde — (1) $P(\text{tocar }0)$ desde 80 en $[0,1000]$; (2) $d(\ln S_t)$; (3) ¿es $W_t^3$ martingala?; (4) distribución de $W_t/Z_t$.*
