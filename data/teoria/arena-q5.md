# Derivadas y mercados · No-arbitraje y Black-Scholes

## Put-call parity — el resultado más importante

**C − P = S − K·e^(−rT)**

Demostración por no-arbitraje:

| Portfolio | Hoy | S(T) > K | S(T) ≤ K |
|-----------|-----|----------|----------|
| A: Long call + K·e^{-rT} en efectivo | C + K·e^{-rT} | S(T) | K |
| B: Long put + Long acción | P + S | S(T) | K |

Ambos pagan max(S(T), K) → deben costar lo mismo hoy.

Con r=0 y S=K (ATM): **C = P** siempre. El upside ilimitado de la call ya está capturado en el precio de equilibrio.

---

## Delta de una call ATM

Δ = N(d₁) donde d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T).

Para una call **ATM** (S=K): ln(S/K)=0 → d₁ = (r + σ²/2)·√T/σ ≈ 0 para tasas y vols moderadas.

**Δ ≈ 0.5** para una call ATM.

Intuición: hay ~50% de probabilidad de que la call venza in-the-money. Un aumento de \$1 en S mueve la call ~\$0.50. Cobertura: 1 call vendida ↔ 0.5 acciones compradas.

---

## Black-Scholes con σ = 0

Si la volatilidad es cero, el activo crece deterministamente a S·e^(rT). Con S=K (ATM):

- S(T) = S·e^(rT) > K con certeza → la call siempre expira in-the-money.
- Payoff = S·e^(rT) − K; PV = S − K·e^(−rT).
- **C = S − K·e^(−rT)** (igual que la parity con P=0).
- **Δ = 1**: el delta hedge requiere 1 acción por call vendida.

Para S=K=\$100, r=5%, T=1: C = 100 − 100·e^{-0.05} ≈ **\$4.88**.

---

## Theta y Gamma — el intercambio tiempo/convexidad

De la ecuación de B-S:

**Θ + ½σ²S²Γ + rSΔ − rC = 0**

Long gamma (Γ>0): el portafolio gana con movimientos grandes (convexidad). Costo: Θ<0 (pierdes valor por el paso del tiempo).

Short gamma: cobras tiempo (Θ>0) pero pierdes si el mercado se mueve mucho.

**Theta y gamma tienen signo opuesto** para opciones vainilla (con r pequeño o derivada sin dividendos). La ecuación de B-S fuerza este balance.

---

## Precio de call ATM — regla de dedo

Para S=K, r≈0, madurez T, volatilidad σ:

**C ≈ S·σ·√T / √(2π) ≈ 0.4·S·σ·√T**

Para S=\$100, σ=10%, T=1 año: C ≈ 0.4×100×0.1 = **\$4** (≈\$3.99 exacto).

Las tres anclas: \$1 (demasiado bajo para σ=10%), **\$5** (la respuesta correcta de orden de magnitud), \$10 (sería σ≈25%).

---

## Tasa libre de riesgo en Black-Scholes

¿Por qué no aparece μ (retorno esperado del activo)?

El portafolio delta-hedgeado (long opción + short Δ acciones) tiene riesgo cero en el instante dt. Por no-arbitraje, debe rendir exactamente r. Al derivar la EDP de B-S, el término μ se cancela.

Consecuencia: el precio de una opción **no depende de lo optimistas o pesimistas** que seamos sobre el activo. Dos traders con μ distintos le asignan el mismo precio a la opción (dado S, K, r, σ, T).

---

## Regla √T — escalar volatilidad en el tiempo

Para retornos i.i.d. sin autocorrelación:

**σ(T años) = σ(1 año) × √T**

Base: Var(r₁+r₂+…+rT) = T·Var(r) para i.i.d. → SD escala con √T.

Para σ=10% anual: σ(4 años) = 10%×2 = **20%**; σ(1 mes) = 10%/√12 ≈ 2.89%.

Límite: no vale con reversión a la media (la volatilidad de largo plazo crece más lento que √T).

---

## Estructura temporal — tasa forward

La tasa forward del período [T₁, T₂] satisface:

(1+r₂)^T₂ = (1+r₁)^T₁ × (1+f)^(T₂−T₁)

Para r₅=10%, r₁₀=15%: f₅→₁₀ = [(1.15)^10/(1.10)^5]^(1/5) − 1 ≈ **20.23%**.

Aproximación lineal: f ≈ (r₂·T₂ − r₁·T₁)/(T₂−T₁) = (15%×10 − 10%×5)/5 = **20%**. Subestima el exacto por efecto de composición.

---

## Paradoja de San Petersburgo

E[payoff] = Σₖ 2^k·(1/2)^k = Σ1 = **∞**. Pero nadie paga ∞.

Resolución de Bernoulli: utilidad logarítmica → E[log(W+payoff)] < ∞.

Lección: valor esperado ≠ precio justo cuando la distribución tiene colas muy pesadas o el bankroll es finito.

---

## Mini-ejemplo trabajado: parity con números, y por qué μ desaparece

S=100, K=100, r=0, T=1. Put-call parity dice C − P = S − K·e^(−rT) = 100 − 100 = 0, así que **C = P** exactamente, sin saber σ ni la dirección esperada del activo. Compra una call y vende una put (ambas strike 100): el payoff combinado es S(T) − 100 en *todo* estado — replicas un forward. Si C ≠ P con r=0, ese forward sintético cotizaría distinto de cero y habría arbitraje.

**Predicción antes de seguir:** dos traders, uno alcista (μ alto) y uno bajista (μ bajo), ¿le ponen precios distintos a la call? Respuesta: **no**. El portafolio delta-hedgeado (long call − Δ acciones) no tiene riesgo en dt, así que por no-arbitraje rinde r, y al derivar la EDP de Black-Scholes el término μ se cancela. El precio depende de σ, no del optimismo. *Lo que cobras no es tu opinión sobre la dirección, sino tu exposición a la magnitud.*

## Prototipo, contraejemplo y caso borde

- **Prototipo:** dos carteras con idéntico payoff en todos los estados → mismo precio hoy (toda la put-call parity sale de aquí).
- **Contraejemplo (confundir Δ con probabilidad):** Δ = N(d₁) ≈ 0.5 para una ATM se lee mal como "50% de acabar ITM". La probabilidad real (medida física) usa N(d₂), no N(d₁); coinciden solo aproximadamente. Delta es sensibilidad de precio, no probabilidad.
- **Caso borde (σ→0):** sin volatilidad la call ATM ya no vale ~0.4·S·σ·√T sino S − K·e^(−rT) con Δ=1: se vuelve un forward. El borde muestra que el valor "óptico" de la opción es puro tiempo×volatilidad.

## Errores típicos

- **Conceptual:** creer que un activo con mayor retorno esperado hace más cara la opción. No: μ no entra en B-S; entra σ.
- **Técnico:** escalar volatilidad con √T cuando hay reversión a la media o momentum (la regla √T solo vale para retornos i.i.d.).
- **De interpretación:** olvidar el signo opuesto Θ↔Γ; "soy long gamma y además quiero theta positivo" es imposible en vanilla (la EDP los amarra).

## Transferencia isomorfa

No-arbitraje y la corrección √T se transfieren más allá de las opciones:

- **Delta-hedge cancela μ ↔ aleatorización borra el confundidor:** cubrir con Δ acciones elimina la dependencia de la dirección igual que un A/B test elimina la dependencia del confundidor; ambos aíslan el efecto "puro" cortando una flecha (conecta con [[arena-h17]], do(x) borra las flechas hacia X).
- **Regla √T ↔ error estándar σ/√n:** la volatilidad escala con √T porque las varianzas de incrementos i.i.d. se suman — exactamente por qué el SE de la media decae como 1/√n (conecta con [[arena-q6]] y [[arena-q7]]).
- **Replicación de payoff ↔ identificación causal:** "expresar un derivado con instrumentos cotizados" es estructuralmente "expresar P(Y|do(x)) con cantidades observables"; en ambos, si no se puede replicar/identificar, ningún dato lo salva.

Moraleja de la arista: *si dos cosas pagan igual en todos los estados, valen igual hoy; cubrir el riesgo direccional deja solo el precio de la incertidumbre.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Call ATM con σ=0" | C = S − K·e^{-rT}; Δ=1 |
| "Call vs put ATM, r=0" | C = P (put-call parity) |
| "Break-even del straddle" | Strike ± prima total |
| "Delta de call ATM" | ~0.5 (N(d₁) con d₁≈0) |
| "Theta y gamma" | Opuesto siempre: Θ + ½σ²S²Γ = constante |
| "Tasa forward implícita" | (1+r_largo)^T_largo/(1+r_corto)^T_corto = (1+f)^ΔT |
| "¿Por qué r y no μ en B-S?" | Delta hedge → portafolio sin riesgo → debe rendir r |
| "SD de retornos T años" | σ·√T (solo para i.i.d.) |

---

> **Síntesis:** No-arbitraje es la navaja de Occam de las finanzas cuantitativas: si dos posiciones tienen el mismo payoff en todos los estados, deben costar lo mismo hoy. Esa única idea genera put-call parity, el precio de la call con σ=0 y por qué μ no aparece en B-S.

---

*Retrieval: sin mirar, deriva la put-call parity con los dos portfolios; calcula el precio de una call ATM con σ=20%, S=K=100, r=0, T=1.*
