# Procesos estocásticos y movimiento browniano

## Caminata aleatoria simple

Sₙ = X₁+…+Xₙ con P(Xᵢ=+1) = P(Xᵢ=−1) = 1/2.

| Propiedad | Valor |
|-----------|-------|
| E[Sₙ] | 0 |
| Var(Sₙ) | n |
| E[Sₙ²] | n |
| Distribución asintótica | Sₙ/√n → N(0,1) |

La dispersión crece como **√n**, no n — raíz de la regla √T en finanzas.

---

## Ruina del jugador — tabla de resultados

Barreras en 0 (ruina) y N (meta). Inicio en k.

| p | P(llegar a N) | E[pasos hasta absorción] |
|---|--------------|--------------------------|
| 1/2 | k/N | k(N−k) |
| ≠1/2 (ρ=q/p) | (1−ρᵏ)/(1−ρᴺ) | compleja pero finita |

Para p<1/2: P(llegar a N) cae exponencialmente en la ventaja del casino.

**Ecuación de balance:** Pₖ = p·P_{k+1} + q·P_{k−1}, P₀=0, P_N=1. Solución general: Pₖ = A + B·ρᵏ; condiciones de frontera dan A,B.

---

## Movimiento browniano estándar — propiedades

B_t es movimiento browniano si:
1. B₀ = 0
2. Incrementos independientes: (B_t − B_s) ⊥ σ(B_r, r≤s) para s<t
3. Incrementos estacionarios: B_t − B_s ~ N(0, t−s)
4. Trayectorias continuas (a.s.)
5. Variación cuadrática: [B,B]_t = t

**Covarianza:** Cov(B_s, B_t) = min(s,t) para s≤t.

Dem.: E[B_sB_t] = E[B_s·(B_t−B_s)] + E[B_s²] = 0 + s = s.

---

## Variación cuadrática — por qué importa

En cálculo clásico: (dx)² → 0 al segundo orden.
En cálculo estocástico: **(dB)² = dt** (variación cuadrática = t).

Esta identidad es la raíz del lema de Itô: la expansión de Taylor necesita el término ½f''·(dB)².

La variación total de B_t en [0,T] es ∞ (las trayectorias son continuamente "rugosas").

---

## Lema de Itô — fórmula completa

Para dS = μS dt + σS dW y f(t,S) suave:

**df = (∂f/∂t + μS·∂f/∂S + ½σ²S²·∂²f/∂S²) dt + σS·∂f/∂S dW**

Caso f = ln(S):
∂f/∂S = 1/S, ∂²f/∂S² = −1/S².

**d(ln S) = (μ − σ²/2) dt + σ dW**

Integrando: ln(S_T/S_0) ~ N((μ−σ²/2)T, σ²T).

---

## Martingalas fundamentales del BM

| Proceso | Martingala? | Verificación |
|---------|-------------|-------------|
| B_t | ✓ | E[B_t\|F_s] = B_s |
| B_t² − t | ✓ | E[B_t²\|F_s] = B_s² + (t−s); resta t |
| e^(σB_t − σ²t/2) | ✓ | Girsanov: E[e^{σ(B_t−B_s)} \| F_s] = e^{σ²(t−s)/2} |

---

## Tiempo de primer toque

T_a = inf{t ≥ 0 : B_t = a} para a > 0.

- P(T_a < ∞) = **1** (BM alcanza cualquier nivel)
- E[T_a] = **∞** (los tiempos de toque tienen cola pesada)
- Distribución de T_a: Lévy-estable con índice 1/2; densidad: f(t) = a·e^{−a²/(2t)} / √(2πt³)

OST (optional sampling): E[B_{T_a}]=0≠a → E[T_a]=∞ es necesario para que el OST falle.

---

## Principio de reflexión

P(max_{s≤t} B_s ≥ a) = **2·P(B_t ≥ a) = 2Φ(−a/√t)**

Intuición: una vez que B toca a, la parte futura se refleja equiprobablemente hacia arriba y hacia abajo. La mitad de las trayectorias que cruzan a terminan por encima.

Aplicación: opciones de barrera y knock-out — P(tocar la barrera en [0,T]).

---

## Proceso de Ornstein-Uhlenbeck (OU)

dX = −κ(X−θ)dt + σdW

- κ: velocidad de reversión a la media
- θ: nivel de equilibrio a largo plazo
- Distribución estacionaria: N(θ, σ²/(2κ))

Diferencia con BM: Var[X_t] → σ²/(2κ) (constante); BM tiene Var[B_t] = t (crece sin límite).

**Usos:** modelo de Vasicek (tasas de interés), pares trading.

---

## Proceso de Poisson

N(t) ~ Poisson(λt): E[N(t)] = Var[N(t)] = λt.

| Operación | Resultado |
|-----------|-----------|
| Superposición: Poisson(λ₁)+Poisson(λ₂) | Poisson(λ₁+λ₂) |
| Adelgazamiento: incluye c/evento con prob p | Poisson(λp) |
| Tiempo entre llegadas | Exp(λ) con E[T]=1/λ |

---

## Cambio de medida — Girsanov

Si W_t es BM bajo ℙ y el proceso tiene drift θ:

dX = θ dt + dW (bajo ℙ)

Bajo la medida ℚ definida por dℚ/dℙ = e^{θW_T − θ²T/2}:

**X_t es BM estándar bajo ℚ**

En finanzas: ℙ es la medida real (drift μ), ℚ es la medida neutral al riesgo (drift r).
Precio de opción = E^ℚ[e^{−rT}·payoff].

---

## Cadena de Markov — distribución estacionaria

**πP = π, Σπᵢ = 1**

Método: sistema lineal n×n con la condición de normalización.

Para cadenas ergódicas (irreducibles + aperiódicas): converge a π desde cualquier estado inicial.

---

## Mini-ejemplo trabajado: el principio de reflexión, intuición y número

¿P(el máximo de un browniano en [0,t] supera el nivel a>0)? El principio de reflexión da una respuesta sorprendentemente limpia:

> P(max_{s≤t} B_s ≥ a) = 2·P(B_t ≥ a) = 2Φ(−a/√t)

La intuición: cada trayectoria que toca a y termina **por debajo** de a tiene una imagen espejo (reflejada en a desde el instante del toque) que termina **por encima**, igual de probable. Así, las que terminan ≥ a son la mitad de las que tocaron a → P(tocar) = 2·P(B_t ≥ a). Para a=√t: 2Φ(−1) ≈ 2·0.159 = **0.317**.

**Predicción antes de seguir:** el browniano alcanza cualquier nivel a con probabilidad 1, pero ¿el tiempo esperado para hacerlo es finito? Respuesta: **no, E[T_a]=∞** (cola Lévy pesada). "Seguro que pasa" y "pasa en tiempo esperado finito" son cosas distintas; por eso el muestreo opcional falla aquí (E[B_{T_a}]=0≠a). El mismo abismo que separa recurrencia de la caminata (P=1) de su tiempo de retorno (∞).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** barrera/absorción → ruina del jugador (martingala) o reflexión para el máximo del BM.
- **Contraejemplo (OU no es BM):** el browniano tiene Var=t creciente sin límite; el Ornstein-Uhlenbeck revierte a la media y su Var→σ²/(2κ) constante. Tratar un proceso con reversión como un BM rompe la escala √T.
- **Caso borde (variación cuadrática):** (dB)²=dt no es cero — las trayectorias son tan rugosas que su variación total es ∞. El borde es la razón de que exista el término extra de Itô.

## Errores típicos

- **Conceptual:** olvidar el drift de Itô −σ²/2 al pasar de S a ln S (confunde media aritmética y geométrica).
- **Técnico:** aplicar muestreo opcional sin verificar que el tiempo de parada tenga esperanza finita (falla para T_a).
- **De supuestos:** escalar volatilidad con √t bajo reversión a la media (OU crece más lento).

## Transferencia isomorfa

- **Variación cuadrática (dB)²=dt ↔ corrección de Itô y prima de Jensen:** el término ½f''(dB)² es el origen del −σ²/2 del log-precio y del +σ²/2 de E[e^X] (conecta con [[arena-q7]]).
- **Ruina del jugador ↔ muestreo opcional en barreras:** P(absorción)=k/N sale de que la posición es martingala (conecta con [[arena-q11]] y [[arena-fc4]]).
- **Girsanov (cambiar drift μ→r) ↔ no-arbitraje y medida neutral al riesgo:** quitar el drift para valorar como esperanza descontada es por qué μ no entra en Black-Scholes (conecta con [[arena-q5]]).
- **Proceso de Poisson (superposición/adelgazamiento) ↔ exponencial y Gamma:** tiempos entre llegadas Exp(λ), conteo Poisson(λt) (conecta con [[arena-b3]]).

Moraleja de la arista: *(dB)²=dt es la fuente del −σ²/2 de Itô; y "alcanza el nivel con probabilidad 1" no implica "en tiempo esperado finito".*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Var del proceso en t pasos" | Caminata: Var=t; BM: Var=t |
| "P(absorción en N desde k)" | Ruina: p=1/2 → k/N; p≠1/2 → (1−ρᵏ)/(1−ρᴺ) |
| "Cov entre B_s y B_t" | min(s,t) |
| "d(ln S) con GBM" | Itô: (μ−σ²/2)dt + σdW |
| "E[max B_s en [0,t]]" | Reflexión: 2Φ(−a/√t) |
| "¿E[T_a] para BM?" | ∞ (cola Lévy pesada) |
| "Proceso que revierte a la media" | OU: dX = −κ(X−θ)dt + σdW |
| "Cambiar drift μ a r" | Girsanov: cambio de medida |
| "Precio de opción como esperanza" | E^ℚ[e^{−rT}·payoff] |

---

> **Síntesis:** El movimiento browniano es la continuación del límite de la caminata aleatoria. Sus propiedades clave son Cov(B_s,B_t)=min(s,t) y [B,B]_t=t. El lema de Itô es la regla de la cadena con este extra: el término (dB)²=dt genera el drift de Itô −σ²/2. El cambio de medida de Girsanov elimina el drift μ y permite calcular precios de derivados como esperanzas.

---

*Retrieval: sin mirar: (1) P(ruina desde k=4, N=8, p=0.4); (2) Cov(B_2, B_5); (3) distribución de ln(S_T/S_0) para GBM; (4) min de dos Poisson(3) y Poisson(5) independientes.*
