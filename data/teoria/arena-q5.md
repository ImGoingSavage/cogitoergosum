# Derivadas y mercados · No-arbitraje y Black–Scholes

## De qué trata (y qué sabrás hacer)

Casi toda la valoración de derivados sale de **una** idea: el **no-arbitraje**. Si dos carteras pagan exactamente lo mismo en todos los estados futuros, deben costar lo mismo hoy; si no, hay dinero gratis. De ahí salen la paridad put-call, el precio de una opción, y el hecho contraintuitivo de que el optimismo sobre el activo **no** afecta el precio de la opción.

Al terminar sabrás derivar la paridad put-call por replicación, estimar el precio de una call ATM con una regla de dedo, y explicar por qué $\mu$ (el retorno esperado) desaparece de Black–Scholes. Cada idea se ancla en una cartera concreta.

---

## Paridad put-call — el resultado más importante

$$C-P=S-K\,e^{-rT}.$$

Aquí $C,P$ son los precios de una call y una put con el mismo strike $K$ y vencimiento $T$, $S$ el precio del activo, y $r$ la tasa libre de riesgo. Se demuestra por **replicación**: compara dos carteras —(A) una call más $K\,e^{-rT}$ en efectivo; (B) una put más una acción—. Al vencimiento, **ambas** pagan $\max(S_T,K)$ en todos los estados. Como pagan igual siempre, cuestan igual hoy, y reordenando sale la paridad. Caso especial: con $r=0$ y $S=K$ (ATM), $C=P$ exactamente.

---

## Delta de una call ATM

El **delta** $\Delta=\partial C/\partial S$ mide cuánto se mueve la opción cuando el activo se mueve \$1. Para una call at-the-money ($S=K$), $\Delta=N(d_1)$ con $d_1\approx0$, así que

$$\Delta\approx 0.5.$$

Intuición: hay $\approx50\%$ de probabilidad de que la call venza in-the-money, y un aumento de \$1 en $S$ mueve la call $\approx$\$0.50. Cobertura: vender 1 call se cubre comprando $\approx0.5$ acciones. (Ojo: $\Delta$ es sensibilidad de precio, no exactamente la probabilidad de acabar ITM, que usa $N(d_2)$.)

---

## Regla de dedo para una call ATM

Para $S=K$, $r\approx0$, vencimiento $T$ y volatilidad $\sigma$:

$$C\approx \frac{S\,\sigma\sqrt T}{\sqrt{2\pi}}\approx 0.4\,S\,\sigma\sqrt T.$$

Para $S=$\$100, $\sigma=10\%$, $T=1$ año: $C\approx0.4\times100\times0.1=$\$4. El valor de una opción ATM es esencialmente **tiempo × volatilidad**: sin volatilidad ($\sigma=0$) la call ATM se vuelve un forward y vale $S-K\,e^{-rT}$ con $\Delta=1$.

---

## Por qué $\mu$ no aparece en Black–Scholes

¿Por qué el retorno esperado del activo ($\mu$) no entra en el precio de la opción? Porque un portafolio **delta-hedgeado** (long opción, short $\Delta$ acciones) no tiene riesgo en el instante $dt$. Por no-arbitraje, algo sin riesgo debe rendir exactamente $r$; al escribir esa condición y derivar la EDP de Black–Scholes, el término $\mu$ **se cancela**.

Consecuencia: dos traders, uno alcista y uno bajista (distinto $\mu$), le ponen **el mismo** precio a la opción dado $S,K,r,\sigma,T$. Lo que cobras no es tu opinión sobre la dirección, sino tu exposición a la **magnitud** (la volatilidad).

---

## Theta y gamma — el intercambio tiempo/convexidad

La EDP de Black–Scholes amarra los Greeks: $\Theta+\tfrac12\sigma^2 S^2\Gamma+rS\Delta-rC=0$. La lectura práctica: **theta y gamma tienen signo opuesto** en opciones vainilla. Si eres long gamma ($\Gamma>0$, ganas con movimientos grandes), pagas con theta negativo (pierdes valor por el paso del tiempo). No puedes tener ambos a tu favor: la convexidad se paga con carry.

---

## Regla $\sqrt T$ — escalar volatilidad en el tiempo

Para retornos i.i.d. (sin autocorrelación), las varianzas de los incrementos se suman, así que la desviación estándar escala con la raíz del horizonte:

$$\sigma(T\text{ años})=\sigma(1\text{ año})\times\sqrt T.$$

Para $\sigma=10\%$ anual: $\sigma(4\text{ años})=20\%$; $\sigma(1\text{ mes})\approx2.89\%$. **No** vale con reversión a la media (crece más lento) ni con momentum (más rápido). Es la misma raíz que el error estándar $\sigma/\sqrt n$ (conecta con [[arena-q6]]).

---

## Mini-ejemplo trabajado: parity con números, y por qué $\mu$ desaparece

$S=100$, $K=100$, $r=0$, $T=1$. La paridad put-call dice $C-P=S-K\,e^{-rT}=100-100=0$, así que $C=P$ exactamente, **sin saber** $\sigma$ ni la dirección esperada del activo. Compra una call y vende una put (ambas strike 100): el payoff combinado es $S_T-100$ en *todo* estado — replicas un forward. Si $C\ne P$ con $r=0$, ese forward sintético cotizaría distinto de cero y habría arbitraje.

**Predicción antes de seguir:** dos traders, uno alcista ($\mu$ alto) y uno bajista ($\mu$ bajo), ¿le ponen precios distintos a la call? Respuesta: **no**. El portafolio delta-hedgeado (long call $-\,\Delta$ acciones) no tiene riesgo en $dt$, así que por no-arbitraje rinde $r$, y al derivar la EDP de Black–Scholes el término $\mu$ se cancela. El precio depende de $\sigma$, no del optimismo. *Lo que cobras no es tu opinión sobre la dirección, sino tu exposición a la magnitud.*

## Prototipo, contraejemplo y caso borde

- **Prototipo:** dos carteras con idéntico payoff en todos los estados → mismo precio hoy (toda la paridad put-call sale de aquí).
- **Contraejemplo (confundir $\Delta$ con probabilidad):** $\Delta=N(d_1)\approx0.5$ para una ATM se lee mal como "50% de acabar ITM". La probabilidad real usa $N(d_2)$, no $N(d_1)$; coinciden solo aproximadamente. Delta es sensibilidad de precio, no probabilidad.
- **Caso borde ($\sigma\to0$):** sin volatilidad la call ATM ya no vale $\approx0.4\,S\,\sigma\sqrt T$ sino $S-K\,e^{-rT}$ con $\Delta=1$: se vuelve un forward. El borde muestra que el valor "óptico" de la opción es puro tiempo × volatilidad.

## Errores típicos

- **Conceptual:** creer que un activo con mayor retorno esperado hace más cara la opción. No: $\mu$ no entra en B-S; entra $\sigma$.
- **Técnico:** escalar volatilidad con $\sqrt T$ cuando hay reversión a la media o momentum (la regla $\sqrt T$ solo vale para retornos i.i.d.).
- **De interpretación:** olvidar el signo opuesto $\Theta\leftrightarrow\Gamma$; "soy long gamma y además quiero theta positivo" es imposible en vainilla (la EDP los amarra).

## Transferencia isomorfa

- **Delta-hedge cancela $\mu$ ↔ aleatorización borra el confundidor:** cubrir con $\Delta$ acciones elimina la dependencia de la dirección igual que un A/B test elimina la dependencia del confundidor; ambos aíslan el efecto "puro" cortando una flecha (conecta con [[arena-h17]], $do(x)$ borra las flechas hacia $X$).
- **Regla $\sqrt T$ ↔ error estándar $\sigma/\sqrt n$:** la volatilidad escala con $\sqrt T$ porque las varianzas de incrementos i.i.d. se suman — exactamente por qué el SE de la media decae como $1/\sqrt n$ (conecta con [[arena-q6]] y [[arena-q7]]).
- **Replicación de payoff ↔ identificación causal:** "expresar un derivado con instrumentos cotizados" es estructuralmente "expresar $P(Y\mid do(x))$ con cantidades observables"; en ambos, si no se puede replicar/identificar, ningún dato lo salva (conecta con [[arena-h5]]).

Moraleja de la arista: *si dos cosas pagan igual en todos los estados, valen igual hoy; cubrir el riesgo direccional deja solo el precio de la incertidumbre.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Call ATM con $\sigma=0$" | $C=S-K\,e^{-rT}$; $\Delta=1$ |
| "Call vs put ATM, $r=0$" | $C=P$ (paridad put-call) |
| "Delta de call ATM" | $\approx0.5$ ($N(d_1)$ con $d_1\approx0$) |
| "Theta y gamma" | Signo opuesto: $\Theta+\tfrac12\sigma^2S^2\Gamma=$ cte |
| "Precio de call ATM (regla de dedo)" | $\approx0.4\,S\,\sigma\sqrt T$ |
| "¿Por qué $r$ y no $\mu$ en B-S?" | Delta-hedge → cartera sin riesgo → rinde $r$ |
| "SD de retornos $T$ años" | $\sigma\sqrt T$ (solo i.i.d.) |

---

> **Síntesis:** El no-arbitraje es la navaja de Occam de las finanzas cuantitativas: si dos posiciones tienen el mismo payoff en todos los estados, cuestan lo mismo hoy. Esa única idea genera la paridad put-call, el precio de la call con $\sigma=0$ y por qué $\mu$ no aparece en Black–Scholes.

---

*Retrieval: sin mirar, deriva la paridad put-call con las dos carteras; calcula el precio aproximado de una call ATM con $\sigma=20\%$, $S=K=100$, $r=0$, $T=1$.*
