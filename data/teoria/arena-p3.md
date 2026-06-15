# Procesos estocásticos y movimiento browniano

## De qué trata (y qué sabrás hacer)

Un **proceso estocástico** es el azar desplegándose en el tiempo. Esta lección construye, desde la caminata aleatoria más simple, el objeto central de las finanzas modernas: el **movimiento browniano**. La gran sorpresa es que el azar acumulado tiene una "rugosidad" que rompe el cálculo clásico, y arreglarla (el lema de Itô) explica las fórmulas que de otro modo parecen mágicas.

Al terminar sabrás por qué la dispersión crece como $\sqrt T$, qué hace especial al browniano, de dónde sale la corrección $-\sigma^2/2$ al pasar a logaritmos, y cómo el cambio de medida permite valorar derivados como esperanzas. Se construye desde la caminata aleatoria, paso a paso.

---

## Caminata aleatoria simple

Sumas pasos $\pm1$ al azar: $S_n=X_1+\cdots+X_n$ con $P(X_i=\pm1)=\tfrac12$. Como los pasos son independientes con media 0 y varianza 1:

$$E[S_n]=0, \qquad \text{Var}(S_n)=n, \qquad \frac{S_n}{\sqrt n}\xrightarrow{d}N(0,1).$$

La clave: la dispersión típica es $\sqrt{\text{Var}}=\sqrt n$, **no** $n$. Caminas "a la deriva" alejándote del origen como raíz del tiempo. Esa es la raíz de la regla $\sqrt T$ en finanzas (la volatilidad de un retorno escala con la raíz del horizonte).

---

## Movimiento browniano estándar

Toma la caminata aleatoria, reduce el tamaño del paso y acelera el tiempo: en el límite obtienes el **movimiento browniano** $B_t$, definido por:
1. $B_0=0$;
2. **incrementos independientes** (lo que pasa después de $s$ es independiente de lo anterior);
3. **incrementos gaussianos:** $B_t-B_s\sim N(0,\,t-s)$;
4. trayectorias continuas.

De aquí sale su covarianza, $\text{Cov}(B_s,B_t)=\min(s,t)$. (Para $s\le t$: $E[B_s B_t]=E[B_s(B_t-B_s)]+E[B_s^2]=0+s=s$, usando incrementos independientes.) La varianza $\text{Var}(B_t)=t$ crece sin límite: el browniano se aleja, no revierte.

---

## Variación cuadrática — por qué el cálculo cambia

En el cálculo clásico, un incremento al cuadrado $(dx)^2$ es despreciable. Para el browniano **no**:

$$(dB)^2=dt.$$

Las trayectorias son tan "rugosas" (continuas pero en ningún punto derivables) que la suma de incrementos al cuadrado en $[0,t]$ no tiende a 0 sino a $t$. Esta identidad es la fuente de todo lo que sigue: obliga a conservar un término de segundo orden que en el cálculo normal se tira.

---

## Lema de Itô — la regla de la cadena estocástica

Si un activo sigue $dS=\mu S\,dt+\sigma S\,dW$ (browniano geométrico) y $f(t,S)$ es suave, la regla de la cadena gana un término extra por $(dW)^2=dt$:

$$df=\left(\frac{\partial f}{\partial t}+\mu S\frac{\partial f}{\partial S}+\tfrac12\sigma^2 S^2\frac{\partial^2 f}{\partial S^2}\right)dt+\sigma S\frac{\partial f}{\partial S}\,dW.$$

El caso más importante, $f=\ln S$ (con $\partial f/\partial S=1/S$, $\partial^2 f/\partial S^2=-1/S^2$):

$$d(\ln S)=\left(\mu-\frac{\sigma^2}{2}\right)dt+\sigma\,dW \;\Rightarrow\; \ln\frac{S_T}{S_0}\sim N\!\left(\left(\mu-\tfrac{\sigma^2}{2}\right)T,\ \sigma^2 T\right).$$

Ese $-\sigma^2/2$ (la "corrección de Itô") es la diferencia entre la media aritmética y la geométrica de los retornos — fuente de incontables errores (conecta con [[arena-q7]]).

---

## Martingalas del browniano

Una **martingala** es un "juego justo": su esperanza futura, dado el presente, es el valor actual. Tres martingalas clásicas del browniano (úsalas como plantillas para el test "¿es martingala?"):

| Proceso | ¿Martingala? |
|---------|-------------|
| $B_t$ | sí ($E[B_t\mid \mathcal F_s]=B_s$) |
| $B_t^2-t$ | sí (resta justo la varianza acumulada) |
| $e^{\sigma B_t-\sigma^2 t/2}$ | sí (la exponencial con su corrección) |

El test operativo: aplica Itô y exige que el término $dt$ (la deriva) se anule. Si sobrevive deriva, no es martingala.

---

## Tiempo de primer toque y reflexión

Sea $T_a$ el primer instante en que $B_t$ alcanza el nivel $a>0$. Notable:

$$P(T_a<\infty)=1\quad\text{(siempre lo alcanza)}, \qquad E[T_a]=\infty\quad\text{(cola pesada)}.$$

"Seguro que pasa" no implica "en tiempo esperado finito". El **principio de reflexión** da la probabilidad de que el máximo supere $a$:

$$P\!\left(\max_{s\le t}B_s\ge a\right)=2\,P(B_t\ge a)=2\,\Phi\!\left(-\frac{a}{\sqrt t}\right).$$

Intuición: cada trayectoria que toca $a$ y termina por debajo tiene una imagen espejo (reflejada en $a$ desde el toque) que termina por encima, igual de probable. Esto valora opciones de barrera.

---

## Ornstein–Uhlenbeck (reversión a la media)

$$dX=-\kappa(X-\theta)\,dt+\sigma\,dW.$$

A diferencia del browniano, este proceso es **jalado** de vuelta hacia un nivel $\theta$ a velocidad $\kappa$. Su varianza no crece sin límite sino que se estabiliza en $\sigma^2/(2\kappa)$; su distribución estacionaria es $N(\theta,\sigma^2/(2\kappa))$. Es el modelo de tasas de interés (Vasicek) y de spreads en pairs trading.

---

## Proceso de Poisson y cambio de medida

El **proceso de Poisson** cuenta eventos: $N(t)\sim\text{Poisson}(\lambda t)$, con tiempos entre llegadas $\text{Exp}(\lambda)$; superponer dos procesos suma las tasas, y adelgazar (retener con prob $p$) escala a $\lambda p$ (conecta con [[arena-b3]]).

El **cambio de medida** (Girsanov) reescribe la probabilidad para **eliminar el drift**: bajo una nueva medida $\mathbb Q$, un proceso con deriva se vuelve browniano puro. En finanzas, $\mathbb Q$ es la medida neutral al riesgo y el precio de un derivado es $E^{\mathbb Q}[e^{-rT}\cdot\text{payoff}]$ — por eso el drift real $\mu$ desaparece de Black–Scholes (conecta con [[arena-q5]]).

---

## Mini-ejemplo trabajado: el principio de reflexión, intuición y número

¿$P(\text{el máximo de un browniano en }[0,t]\text{ supera }a>0)$? El principio de reflexión da una respuesta limpia:

$$P\!\left(\max_{s\le t}B_s\ge a\right)=2\,P(B_t\ge a)=2\,\Phi\!\left(-\frac{a}{\sqrt t}\right).$$

La intuición: cada trayectoria que toca $a$ y termina **por debajo** tiene una imagen espejo (reflejada en $a$ desde el instante del toque) que termina **por encima**, igual de probable. Así, las que terminan $\ge a$ son la mitad de las que tocaron $a$, de donde $P(\text{tocar})=2P(B_t\ge a)$. Para $a=\sqrt t$: $2\Phi(-1)\approx 2\cdot0.159=0.317$.

**Predicción antes de seguir:** el browniano alcanza cualquier nivel $a$ con probabilidad 1, pero ¿el tiempo esperado para hacerlo es finito? Respuesta: **no, $E[T_a]=\infty$** (cola Lévy pesada). "Seguro que pasa" y "pasa en tiempo esperado finito" son cosas distintas; por eso el muestreo opcional falla aquí ($E[B_{T_a}]=0\ne a$). El mismo abismo que separa la recurrencia de la caminata ($P=1$) de su tiempo de retorno ($\infty$) (conecta con [[arena-fc4]]).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** barrera/absorción → ruina del jugador (martingala) o reflexión para el máximo del browniano.
- **Contraejemplo (OU no es browniano):** el browniano tiene $\text{Var}=t$ creciente sin límite; el Ornstein–Uhlenbeck revierte a la media y su $\text{Var}\to\sigma^2/(2\kappa)$ constante. Tratar un proceso con reversión como un browniano rompe la escala $\sqrt T$.
- **Caso borde (variación cuadrática):** $(dB)^2=dt$ no es cero — las trayectorias son tan rugosas que su variación total es $\infty$. El borde es la razón de que exista el término extra de Itô.

## Errores típicos

- **Conceptual:** olvidar el drift de Itô $-\sigma^2/2$ al pasar de $S$ a $\ln S$ (confunde media aritmética y geométrica).
- **Técnico:** aplicar muestreo opcional sin verificar que el tiempo de parada tenga esperanza finita (falla para $T_a$).
- **De supuestos:** escalar volatilidad con $\sqrt t$ bajo reversión a la media (el OU crece más lento).

## Transferencia isomorfa

- **Variación cuadrática $(dB)^2=dt$ ↔ corrección de Itô y prima de Jensen:** el término $\tfrac12 f''(dB)^2$ es el origen del $-\sigma^2/2$ del log-precio y del $+\sigma^2/2$ de $E[e^X]$ (conecta con [[arena-q7]]).
- **Ruina del jugador ↔ muestreo opcional en barreras:** $P(\text{absorción})=k/N$ sale de que la posición es martingala (conecta con [[arena-q11]] y [[arena-fc4]]).
- **Girsanov (cambiar drift $\mu\to r$) ↔ no-arbitraje y medida neutral al riesgo:** quitar el drift para valorar como esperanza descontada es por qué $\mu$ no entra en Black–Scholes (conecta con [[arena-q5]]).
- **Proceso de Poisson (superposición/adelgazamiento) ↔ exponencial y Gamma:** tiempos entre llegadas $\text{Exp}(\lambda)$, conteo $\text{Poisson}(\lambda t)$ (conecta con [[arena-b3]]).

Moraleja de la arista: *$(dB)^2=dt$ es la fuente del $-\sigma^2/2$ de Itô; y "alcanza el nivel con probabilidad 1" no implica "en tiempo esperado finito".*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Var del proceso en $t$" | Caminata y browniano: $\text{Var}=t$ |
| "Cov entre $B_s$ y $B_t$" | $\min(s,t)$ |
| "$d(\ln S)$ con GBM" | Itô: $(\mu-\sigma^2/2)dt+\sigma\,dW$ |
| "$E[\max B_s$ en $[0,t]]$" | Reflexión: $2\Phi(-a/\sqrt t)$ |
| "¿$E[T_a]$ para browniano?" | $\infty$ (cola Lévy pesada) |
| "Proceso que revierte a la media" | OU: $dX=-\kappa(X-\theta)dt+\sigma\,dW$ |
| "Precio de opción como esperanza" | $E^{\mathbb Q}[e^{-rT}\cdot\text{payoff}]$ |

---

> **Síntesis:** El movimiento browniano es el límite continuo de la caminata aleatoria, con $\text{Cov}(B_s,B_t)=\min(s,t)$ y variación cuadrática $(dB)^2=dt$. El lema de Itô es la regla de la cadena con ese término extra, que genera el drift $-\sigma^2/2$. El cambio de medida de Girsanov elimina el drift y permite valorar derivados como esperanzas descontadas.

---

*Retrieval: sin mirar: (1) $\text{Cov}(B_2,B_5)$; (2) distribución de $\ln(S_T/S_0)$ para GBM; (3) $P(\max_{s\le t}B_s\ge a)$ por reflexión; (4) por qué $E[T_a]=\infty$ aunque $P(T_a<\infty)=1$.*
