# Arena Quant · Movimiento browniano, Itô y martingalas

El corazón de la valoración moderna. Dos herramientas resuelven casi todo: **el muestreo opcional** (si algo es martingala, su esperanza en un tiempo de parada finito es su valor inicial) y **la fórmula de Itô** (la regla de la cadena estocástica, con el término extra ½f″(dW)²).

## Movimiento browniano — la definición que debes recitar

Wₜ es un movimiento browniano si W₀=0, los incrementos son independientes y **Wₜ − Wₛ ~ N(0, t−s)**. Consecuencias: continuo en todas partes, diferenciable en ninguna; cruza cualquier nivel infinitas veces en un instante; **E(Wₛ Wₜ) = mín(s,t)** (truco x = x+y−y con independencia de incrementos).

## Muestreo opcional en acción

«Paseo aleatorio en [0,1000] que arranca en 80, ±1 con prob ½. ¿P(toca 0 antes que 1000)?» La posición es una **martingala**; el tiempo de salida es un tiempo de parada de esperanza finita, así que E(posición al parar) = 80. Si p = P(tocar 1000): 1000p = 80 → p = 0.08, y **P(tocar 0) = 0.92**. La probabilidad de absorción es lineal en el punto de partida cuando el paso es justo.

## Itô: convertir un proceso en otro

Si dSₜ = μSₜdt + σSₜdWₜ (browniano geométrico), entonces:

> d log Sₜ = (μ − σ²/2)dt + σdWₜ  →  Sₜ = S₀ exp((μ − σ²/2)t + σWₜ)

y al cuadrado, **(Sₜ)² es otro browniano geométrico** con deriva (2μ + σ²) y difusión 2σ. El término −σ²/2 (la «corrección de Itô») es la diferencia entre la media aritmética y la geométrica de los retornos: la fuente de incontables errores.

## ¿Es martingala? El test de la deriva cero

Aplica Itô y mira si sobrevive algún término dt:

- **Wₜ³:** dWₜ³ = 3Wₜdt + 3Wₜ²dWₜ → hay deriva 3Wₜ → **NO** es martingala.
- **2^{Wₜ}:** d(2^W) = ln2·2^W dW + ½(ln2)²2^W dt → deriva → **NO**.
- **cosh(λWₜ)·exp(−λ²t/2):** todos los dt se cancelan → **SÍ** es martingala. Igual que Wₜ²−t, Wₜ³−3tWₜ y exp(σWₜ − σ²t/2).

Regla mnemónica: una función f(Wₜ) sin dependencia explícita en t es martingala solo si f es lineal (deriva = ½f″ que debe anularse en esperanza). Añadir el factor temporal correcto «mata» la deriva.

## Dos resultados que sorprenden

- **El cociente Wₜ/Zₜ de dos brownianos independientes es Cauchy estándar** (cociente de dos normales centradas). Por eso no tiene media: las colas pesadas aparecen al dividir.
- **Si X₀=0 y X₁>0, ¿P(X₂<0)?** Por simetría de los incrementos: necesitas X₂−X₁ negativo (prob ½) y de magnitud mayor que X₁ (prob ½ por igual distribución) → **1/4**.

## El proceso de Ornstein-Uhlenbeck (reversión a la media)

dXₜ = θ(μ − Xₜ)dt + σdWₜ. Se resuelve con el factor integrante e^{θt}:

> Xₜ = X₀e^{−θt} + μ(1 − e^{−θt}) + ∫₀ᵗ σe^{θ(s−t)}dWₛ

θ controla la velocidad de reversión hacia μ. Es el modelo base de tasas de interés (Vasicek) y de spreads. Y **dt = (dWₜ)²** no es magia: dice que la variación cuadrática del browniano crece a razón 1 por unidad de tiempo, por eso el término de segundo orden sobrevive en Itô.

## Disparadores

| Señal | Jugada |
|-------|--------|
| "P(tocar barrera A antes que B)" | martingala + muestreo opcional → lineal en el inicio |
| "proceso de log S / S²" | Itô; cuidado con la corrección −σ²/2 |
| "¿es martingala?" | aplica Itô, exige deriva (dt) nula |
| "cociente de dos normales" | Cauchy (sin media) |
| "reversión a la media" | OU; factor integrante e^{θt} |

> ❧ **Síntesis:** muestreo opcional resuelve barreras y «valores justos» en una línea; Itô traduce un proceso en otro con su corrección de segundo orden; y un proceso es martingala exactamente cuando Itô deja deriva cero. El −σ²/2 lognormal y dt=(dW)² son los dos detalles que separan al que entrenó del que improvisa.

---

*Retrieval: cierra la página y responde — (1) P(tocar 0) desde 80 en [0,1000]; (2) d log Sₜ; (3) ¿es Wₜ³ martingala?; (4) distribución de Wₜ/Zₜ.*
