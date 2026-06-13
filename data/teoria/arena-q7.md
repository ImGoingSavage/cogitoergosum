# Finanzas avanzadas · Bonos, Greeks y procesos estocásticos

## Duración de un bono

Duración de Macaulay = media ponderada del tiempo hasta cada flujo:

D = Σₜ [ t · VP(flujo_t) / Precio ]

donde VP(flujo_t) = flujo_t · e^{−yt} (o dividido por (1+y)^t en discreto).

| Tipo de bono | Duración |
|-------------|---------|
| Cupón-cero, vencimiento T | D = T (exacto) |
| Perpetuidad con tasa y | D = (1+y)/y |
| Bono con cupón | D < T (los cupones intermedios ponderan el promedio hacia abajo) |

**Duración modificada:** D_mod = D_Macaulay / (1+y)

ΔP/P ≈ −D_mod · Δy

Para D_mod = 6.5 y Δy = +0.50% = +0.005: ΔP/P ≈ −6.5 × 0.005 = −3.25%.

---

## Convexidad

Corrección de segundo orden:

ΔP/P ≈ −D_mod·Δy + ½·C·(Δy)²

donde C = convexidad = (1/P) · ∂²P/∂y².

La convexidad es siempre positiva para bonos vanilla: la curva precio-tasa es convexa. Por eso, con el mismo precio y duración, mayor convexidad es mejor — te beneficia en ambas direcciones.

**Convexidad negativa:** bonos callable y MBS prepagables. Cuando bajan las tasas, el emisor prepaga → el bonista pierde el upside.

---

## YTM y precio del bono — dirección

| Condición | Precio |
|----------|--------|
| YTM > cupón | Bono bajo la par (descuento) |
| YTM = cupón | Bono a la par |
| YTM < cupón | Bono sobre la par (prima) |

**Pull to par:** a medida que se acerca el vencimiento, el precio siempre converge a la par (independientemente del YTM inicial).

---

## Ratio de Sharpe

S = (E[R] − r_f) / σ(R)

Mide exceso de retorno por unidad de volatilidad total. Útil para comparar portafolios con distintos niveles de riesgo.

**Limitación:** asume que toda la volatilidad es riesgo. Estrategias con alta kurtosis o cola izquierda pesada (ej. vender puts) pueden tener Sharpe alto con riesgo real subestimado.

---

## CAPM

**E[R_i] = r_f + β_i · (E[R_m] − r_f)**

β_i = Cov(R_i, R_m) / Var(R_m) = ρ_{i,m} · (σ_i / σ_m)

| β | Interpretación |
|---|----------------|
| β = 0 | Sin riesgo sistemático (ej. renta fija corta) |
| β = 1 | Mueve igual que el mercado |
| β > 1 | Amplifica el mercado (acciones cíclicas) |
| β < 1 | Amortigua el mercado (acciones defensivas) |

CAPM: solo el riesgo sistemático (β) recibe compensación; el riesgo idiosincrásico se diversifica en el portafolio.

---

## Greeks de opciones — mapa completo

| Greek | Definición | Signo (call/put) |
|-------|-----------|-----------------|
| Delta (Δ) | ∂C/∂S | Call: (0,1); Put: (−1,0) |
| Gamma (Γ) | ∂²C/∂S² | +, mismo para call y put |
| Vega (ν) | ∂C/∂σ | +, mismo para call y put |
| Theta (Θ) | ∂C/∂t | − para long options (se pierde tiempo) |
| Rho (ρ) | ∂C/∂r | Call: +; Put: − |

**Vega > 0 para ambas:** opciones son derechos asimétricos; más volatilidad → más probable ITM en algún momento → más valor. Si σ = 0, call y put ATM valen 0; al aumentar σ, ambas suben.

---

## Paridad de Tasas de Interés Cubierta (CIP)

No-arbitraje entre mercado FX y tasas de interés:

**(1 + r_dom) = (F/S) · (1 + r_ext)**

Reordenando: **F = S · (1 + r_dom) / (1 + r_ext)**

Ejemplo: r_USD = 4%, r_EUR = 1%, S = 1.08 EUR/USD:

F = 1.08 × 1.04/1.01 ≈ 1.1121

Si el forward de mercado difiere: hay arbitraje —pide prestado en la divisa barata, invierte en la cara, cubre el FX con el forward.

**En crisis (2008, 2020):** la escasez de USD encareció el financiamiento, rompiendo CIP. El cruce EUR/USD mostraba primas de hasta 80bps.

---

## Distribución lognormal — media y mediana

Si X ~ N(μ, σ²), entonces Y = e^X ~ Lognormal(μ, σ²).

**E[Y] = e^(μ + σ²/2)** ← el término +σ²/2 es la "prima de Jensen"

**Mediana(Y) = e^μ**

E[Y] > Mediana porque la lognormal es sesgada a la derecha.

En finanzas: si log(S_T/S_0) ~ N(μT, σ²T), entonces E[S_T] = S_0·e^(μT + σ²T/2). El retorno esperado del precio usa μ + σ²/2; el retorno esperado del log usa μ − σ²/2. Estos difieren en σ²T.

---

## Lema de Itô

Para dS = μS dt + σS dW (GBM) y f(t, S):

**df = (∂f/∂t + μS·∂f/∂S + ½σ²S²·∂²f/∂S²) dt + σS·∂f/∂S dW**

**Aplicación — f = ln(S):**

∂f/∂t = 0, ∂f/∂S = 1/S, ∂²f/∂S² = −1/S²

d(ln S) = (μ − σ²/2) dt + σ dW

El término **−σ²/2** es el drift de Itô. Integrando:

ln(S_T/S_0) = (μ − σ²/2)T + σ·W_T ~ N((μ−σ²/2)T, σ²T)

---

## GBM — distribución completa

S(t) = S(0) · exp( (μ − σ²/2)t + σ·W(t) )

| Cantidad | Fórmula |
|---------|---------|
| E[S(T)] | S(0)·e^(μT) |
| Mediana de S(T) | S(0)·e^((μ−σ²/2)T) |
| Var(S(T)) | S(0)²·e^(2μT)·(e^(σ²T) − 1) |
| P(S(T) > K) | N(d₂) bajo medida real; N(d₂) bajo neutral al riesgo |

**Intuición μ vs μ−σ²/2:**
- μ: tasa de crecimiento esperada del precio.
- μ−σ²/2: tasa de crecimiento del log-precio (camino real).
- La diferencia σ²/2 es el "costo de la aleatoriedad" (corrección de Jensen).

---

## Escalar volatilidad en el tiempo

Para retornos i.i.d.:

**σ(T períodos) = σ(1 período) · √T**

Conversión práctica: σ_anual = σ_diaria · √252 (días de trading).

**Cuando NO aplica:**
- Autocorrelación positiva (momentum): la vol anual crece más rápido que √T.
- Reversión a la media: la vol anual crece más lento que √T.
- GARCH / volatilidad estocástica: el factor de escala depende del régimen.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Sensibilidad del bono a tasas" | ΔP/P ≈ −D_mod·Δy |
| "Tasa > cupón" | Bono bajo la par |
| "Sharpe de dos portafolios" | Exceso retorno / σ; no basta el retorno absoluto |
| "β de una acción" | β = ρ·(σ_acción/σ_mercado) |
| "¿Vega de una put?" | Positivo — igual que call; más vol → más valor |
| "Forward FX + dos tasas" | CIP: F = S·(1+r_dom)/(1+r_ext) |
| "E[e^X] con X normal" | e^(μ + σ²/2); mediana e^μ |
| "d(ln S) con GBM" | Lema de Itô → drift (μ − σ²/2) dt + σ dW |
| "Vol diaria a anual" | ×√252 (solo i.i.d.) |

---

> **Síntesis:** Los tres pilares de quant finance avanzado se conectan: no-arbitraje (CIP, put-call parity) ↔ lema de Itô (GBM, distribución lognormal) ↔ Greeks (cómo cambia el precio ante cada parámetro). La corrección de Itô −σ²/2 es la fuente del drift log; la prima de Jensen +σ²/2 es por qué E[precio] > mediana del precio.

---

*Retrieval: sin mirar, responde: (1) fórmula de duración modificada y su uso; (2) E[e^X] si X ~ N(0, 0.04); (3) d(ln S) por lema de Itô; (4) F_CIP con r_dom=5%, r_ext=2%, S=1.20.*
