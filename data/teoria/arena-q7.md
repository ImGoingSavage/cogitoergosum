# Finanzas avanzadas · Bonos, Greeks y procesos estocásticos

## De qué trata (y qué sabrás hacer)

Tres mundos —bonos, opciones y acciones— que parecen distintos comparten un esqueleto: el precio de cualquier instrumento es **sensible** a su factor de riesgo, y esa sensibilidad es una **derivada**. La duración de un bono, el delta de una opción y la beta de una acción son la misma idea (primera derivada del precio); la convexidad y la gamma son la segunda. Y el mismo $\sigma^2/2$ que corrige el log-precio explica por qué la media de un precio supera a su mediana.

Al terminar sabrás medir el riesgo de tasa de un bono (duración/convexidad), leer los Greeks de una opción, y manejar la distribución lognormal sin confundir media y mediana. Cada idea se ancla en un número.

---

## Duración de un bono

La **duración** mide cuánto cae el precio de un bono cuando suben las tasas. La duración de Macaulay es el tiempo promedio de los flujos (ponderado por su valor presente); la **duración modificada** la convierte en sensibilidad porcentual:

$$\frac{\Delta P}{P}\approx -D_{\text{mod}}\cdot\Delta y.$$

Para $D_{\text{mod}}=6.5$ y $\Delta y=+0.50\%$: $\Delta P/P\approx-6.5\times0.005=-3.25\%$. Un cupón-cero a plazo $T$ tiene duración exactamente $T$; un bono con cupones tiene duración menor que $T$ (los cupones intermedios "adelantan" el promedio). La duración es, literalmente, la **elasticidad-precio respecto a la tasa**.

---

## Convexidad

La duración es la aproximación lineal; la **convexidad** $C$ es la corrección de segundo orden (Taylor de nuevo):

$$\frac{\Delta P}{P}\approx -D_{\text{mod}}\,\Delta y+\tfrac12\,C\,(\Delta y)^2.$$

Para bonos vainilla $C>0$: la curva precio-tasa es convexa, lo que **te favorece en ambas direcciones** (ganas más cuando las tasas bajan y pierdes menos cuando suben). Por eso, a igual precio y duración, más convexidad es mejor. **Convexidad negativa** (bonos callable, MBS prepagables): cuando bajan las tasas el emisor prepaga y te corta el upside — te quitan justo el lado bueno.

---

## Greeks de opciones — el mapa

| Greek | Definición | Signo |
|-------|-----------|-------|
| Delta $\Delta$ | $\partial C/\partial S$ | call $(0,1)$; put $(-1,0)$ |
| Gamma $\Gamma$ | $\partial^2 C/\partial S^2$ | $+$, igual call y put |
| Vega $\nu$ | $\partial C/\partial\sigma$ | $+$, igual call y put |
| Theta $\Theta$ | $\partial C/\partial t$ | $-$ para opciones largas |
| Rho $\rho$ | $\partial C/\partial r$ | call $+$; put $-$ |

**Vega $>0$ para ambas:** una opción es un derecho asimétrico, así que más volatilidad la hace más valiosa (más chance de acabar ITM). Si $\sigma=0$, call y put ATM valen 0; al subir $\sigma$, ambas suben.

---

## Ratio de Sharpe y CAPM

El **ratio de Sharpe** $S=\tfrac{E[R]-r_f}{\sigma(R)}$ mide el exceso de retorno por unidad de volatilidad. Su trampa: asume que **toda** la volatilidad es riesgo; estrategias con cola izquierda pesada (vender puts) lucen con Sharpe alto y riesgo real subestimado.

El **CAPM** dice que solo el riesgo *sistemático* se paga: $E[R_i]=r_f+\beta_i(E[R_m]-r_f)$, con $\beta_i=\tfrac{\text{Cov}(R_i,R_m)}{\text{Var}(R_m)}$. La $\beta$ es la pendiente de regresar el activo contra el mercado — el mismo coeficiente OLS (conecta con [[arena-q6]]). El riesgo idiosincrásico se diversifica y no recibe prima.

---

## Distribución lognormal — media vs. mediana

Si $\ln S\sim N(\mu,\sigma^2)$, entonces $S$ es lognormal, y aquí vive un error clásico:

$$E[S]=e^{\mu+\sigma^2/2}, \qquad \text{mediana}(S)=e^{\mu}.$$

La media **supera** a la mediana (la cola derecha tira del promedio); el término $+\sigma^2/2$ es la **prima de Jensen**. En finanzas, si $\ln(S_T/S_0)\sim N(\mu T,\sigma^2 T)$, entonces $E[S_T]=S_0\,e^{\mu T+\sigma^2 T/2}$.

---

## Lema de Itô y el drift $-\sigma^2/2$

Para el browniano geométrico $dS=\mu S\,dt+\sigma S\,dW$, aplicar Itô a $f=\ln S$ da

$$d(\ln S)=\left(\mu-\frac{\sigma^2}{2}\right)dt+\sigma\,dW \;\Rightarrow\; \ln\frac{S_T}{S_0}\sim N\!\left(\left(\mu-\tfrac{\sigma^2}{2}\right)T,\ \sigma^2 T\right).$$

El **mismo** $\sigma^2/2$ aparece restando en el drift del log-precio y sumando en $E[S]$: son las dos caras de la convexidad de la exponencial (conecta con [[arena-q11]] y [[arena-p3]]). Confundir $\mu$ (crecimiento del precio) con $\mu-\sigma^2/2$ (crecimiento del log, el camino típico) es un error frecuente.

---

## Mini-ejemplo trabajado: duración como gradiente del precio

Un bono con duración modificada $D_{\text{mod}}=6.5$. Las tasas suben $\Delta y=+0.50\%=+0.005$. Primer orden: $\Delta P/P\approx-6.5\times0.005=-3.25\%$. La duración es, literalmente, la **elasticidad-precio respecto a la tasa**: un gradiente local. La convexidad $C>0$ es la curvatura que corrige ese gradiente: con $C=80$, el término $\tfrac12\cdot80\cdot(0.005)^2=+0.10\%$ amortigua la caída a $\approx-3.15\%$.

**Predicción antes de seguir:** entre dos bonos con igual precio y duración pero distinta convexidad, ¿cuál prefieres? Respuesta: el de **mayor convexidad** — gana más cuando las tasas bajan y pierde menos cuando suben (la curvatura te favorece en ambas direcciones). Por eso los MBS, con convexidad *negativa* (el deudor prepaga cuando bajan las tasas), se penalizan: te quitan justo el lado bueno de la curva.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** sensibilidad de primer orden de un precio a un factor → duración (bono/tasa), delta (opción/subyacente), beta (acción/mercado). Todos son $\partial\text{precio}/\partial\text{factor}$.
- **Contraejemplo (Sharpe engañoso):** vender puts produce retornos suaves con Sharpe alto, pero la cola izquierda es catastrófica; el Sharpe asume que *toda* la volatilidad mide el riesgo e ignora la asimetría. Sharpe alto $\ne$ bajo riesgo.
- **Caso borde (convexidad negativa):** un bono callable o un MBS rompe la regla "más convexidad es mejor" porque cuando las tasas bajan, el emisor prepaga y te corta el upside. El borde revela qué supuesto (convexidad positiva) tenía la regla vainilla.

## Errores típicos

- **Conceptual:** confundir $E[S_T]$ con la mediana en una lognormal. $E[S]=e^{\mu+\sigma^2/2}>$ mediana $=e^\mu$; el $+\sigma^2/2$ es la prima de Jensen, no un error.
- **Técnico:** olvidar el drift de Itô $-\sigma^2/2$ al pasar de $dS$ a $d(\ln S)$; da una distribución log-precio mal centrada.
- **De supuestos:** anualizar volatilidad con $\sqrt{252}$ cuando hay autocorrelación o cambios de régimen (GARCH); el $\sqrt T$ solo vale para i.i.d.

## Transferencia isomorfa

- **$-\sigma^2/2$ de Itô ↔ $+\sigma^2/2$ de Jensen:** el mismo $\sigma^2/2$ aparece restando en el drift del log-precio y sumando en $E[e^X]$; son las dos caras de la convexidad de la exponencial (conecta con [[arena-q6]]).
- **Duración ↔ delta ↔ beta:** los tres son la primera derivada de un precio frente a su factor de riesgo; la convexidad/gamma es la segunda que los corrige (conecta con [[arena-q5]] y [[arena-p4]]).
- **$\beta=\text{Cov}/\text{Var}$ ↔ coeficiente OLS:** la beta del CAPM es exactamente la pendiente de regresar el activo contra el mercado (conecta con [[arena-q6]]).
- **mgf gaussiana ↔ valoración lognormal:** $E[e^X]=e^{\mu+\sigma^2/2}$ sale de la mgf evaluada en 1 (conecta con [[arena-p4]] y [[arena-b2]]).

Moraleja de la arista: *sensibilidad es la primera derivada del precio; convexidad es la segunda. El mismo $\sigma^2/2$ que baja el log-precio sube la media — conócelo y no confundirás media con mediana.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Sensibilidad del bono a tasas" | $\Delta P/P\approx-D_{\text{mod}}\,\Delta y$ |
| "A igual duración, ¿qué bono?" | Mayor convexidad |
| "Sharpe de dos portafolios" | Exceso retorno $/\,\sigma$; cuidado con la asimetría |
| "$\beta$ de una acción" | $\beta=\text{Cov}(R_i,R_m)/\text{Var}(R_m)$ |
| "¿Vega de una put?" | Positivo — igual que call |
| "$E[e^X]$ con $X$ normal" | $e^{\mu+\sigma^2/2}$; mediana $e^\mu$ |
| "$d(\ln S)$ con GBM" | Itô → drift $(\mu-\sigma^2/2)\,dt+\sigma\,dW$ |
| "Vol diaria a anual" | $\times\sqrt{252}$ (solo i.i.d.) |

---

> **Síntesis:** Los pilares del quant finance avanzado se conectan: no-arbitraje (paridad, CIP) ↔ lema de Itô (GBM, lognormal) ↔ Greeks (sensibilidades). La corrección de Itô $-\sigma^2/2$ es la fuente del drift log; la prima de Jensen $+\sigma^2/2$ es por qué $E[\text{precio}]>$ mediana del precio. Y duración, delta y beta son la misma primera derivada en tres mercados.

---

*Retrieval: sin mirar, responde: (1) fórmula de duración modificada y su uso; (2) $E[e^X]$ si $X\sim N(0,0.04)$; (3) $d(\ln S)$ por lema de Itô; (4) por qué la media de una lognormal supera a su mediana.*
