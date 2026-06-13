# Apuestas, colas y azar

## Craps — probabilidad exacta

Primer lanzamiento de dos dados (suma S):
- S ∈ {7,11}: gana de inmediato (P = 8/36)
- S ∈ {2,3,12}: pierde de inmediato (P = 4/36)
- S ∈ {4,5,6,8,9,10}: continúa; debes repetir S antes de 7

P(ganar en punto p) = p_cruce / (p_cruce + p_7) donde p_cruce = P(S=p), p_7 = 6/36.

| Punto | P(hacer el punto) |
|-------|-------------------|
| 4 o 10 | 3/(3+6) = 1/3 |
| 5 o 9 | 4/(4+6) = 2/5 |
| 6 o 8 | 5/(5+6) = 5/11 |

**P(ganar craps) = 244/495 ≈ 49.29%**

La ventaja de la casa es ~1.41% — el juego de dados más favorable al jugador en el casino.

---

## Chuck-a-luck — esperanza negativa garantizada

Tres dados, apuesta al número k. Ganas $1 por cada dado que muestra k, pierdes $1 si ninguno.

**E[ganancia] = −17/216 ≈ −7.87%** — desventaja enorme.

Dem.: P(0 ks) = (5/6)³ = 125/216; P(1k) = 3·(1/6)·(5/6)² = 75/216; P(2ks) = 3·(1/6)²·(5/6) = 15/216; P(3ks) = 1/216.

E = (−1)(125/216) + (1)(75/216) + (2)(15/216) + (3)(1/216) = **−17/216**.

El jugador intuitivamente espera "si aparece al menos una vez gano", sin ponderar por la frecuencia negativa.

---

## La caja de cerillas de Banach

Dos cajas, cada una con N cerillas. A cada momento sacas una cerilla de una caja aleatoria. P(la primera caja vacía encontrada tiene k cerillas en la otra):

**P(k) = C(2N−k, N) · (1/2)^{2N−k+1} · 2** (para k = 0, 1, ..., N)

**E[cerillas restantes] ≈ √(Nπ/2) − 1/2**

Para N=100: E ≈ √(100π/2) − 0.5 ≈ 12.1 cerillas.

El proceso termina antes de agotar la segunda caja: hay en promedio ~√(Nπ/2) cerillas sobrantes.

---

## Juego audaz vs. tímido

Ruleta rusa: p < 0.5 (en contra). Tienes $k, meta $N.

- **Juego tímido** (apostar $1 cada ronda): P(ganar) muy pequeña — exponencialmente mala.
- **Juego audaz** (apostar el mínimo de {capital, lo que falta}): maximiza P(llegar a N).

**Cuando p < 1/2: el juego audaz SIEMPRE es mejor.**

Dem.: cada apuesta audaz maximiza la "probabilidad de avanzar" en la dirección deseada. El juego tímido da más oportunidades al casino de erosionar el capital.

Para p=0.4, k=10, N=20: juego audaz P≈(0.4/0.6)^1/(1-(0.4/0.6)^2) ≈ 40%; juego tímido P ≈ 0.003%.

---

## Estrategia de doblaje (martingala)

Apuesta $1, si pierdes dobla, si ganas recuperas $1. Aparentemente infalible.

**E[pérdida] = ∞ con cualquier límite de capital finito.**

Dem. con crédito ilimitado: P(ganar $1 eventualmente) = 1, pero si hay límite M:
P(ruina antes de ganar) > 0, y la pérdida cuando ocurre ruina = M.

Con capital M = 2^n: E[resultado] = (−M)·P(ruina) + 1·P(ganar) = 0.

La martingala no genera valor esperado positivo; solo transfiere el riesgo hacia colas pesadas (pérdidas enormes y raras).

---

## Rachas de caras en n lanzamientos

Moneda justa, n lanzamientos. Longitud de la racha más larga esperada:

**E[max racha] ≈ log₂(n)**

Para n=1000: E[max] ≈ 10. Para n=2^20 ≈ 10^6: E[max] ≈ 20.

Intuición: hay n−k+1 ventanas de longitud k; P(racha de k) ≈ (1/2)^k; esperamos una cuando n·(1/2)^k ≈ 1 → k ≈ log₂(n).

Las rachas aparecen con más frecuencia de lo que la intuición sugiere — "anomalías" de 10+ caras consecutivas son esperables con muestras grandes.

---

## Tiempo de primer retorno a 0

Caminata aleatoria simple. P(volver al origen en exactamente 2n pasos):

**P(T₀ = 2n) = C(2n,n)/4^n**

**E[T₀] = ∞** — el tiempo esperado de primer retorno es infinito.

Pero **P(volver eventual) = 1** — la caminata es recurrente nula.

Esto es análogo al tiempo de primer toque del movimiento browniano: P=1 de alcanzar cualquier nivel, pero E[tiempo] = ∞.

---

## Colas M/M/1

λ = tasa de llegada; μ = tasa de servicio; ρ = λ/μ (factor de utilización, ρ < 1 para estabilidad).

| Métrica | Fórmula |
|---------|---------|
| P(sistema vacío) | 1 − ρ |
| P(n en sistema) | (1−ρ)·ρⁿ |
| E[en sistema] L | ρ/(1−ρ) |
| E[en cola] Lq | ρ²/(1−ρ) |
| E[tiempo en sistema] W | 1/(μ−λ) |
| E[tiempo en cola] Wq | ρ/(μ−λ) |

Ley de Little: **L = λW** (y Lq = λWq). Válida para sistemas en equilibrio en general.

Para λ=4/h, μ=5/h: ρ=0.8; L=4; W=1h; Wq=0.8h.

---

## El problema del ascensor

k ascensores, m personas. Cada persona elige ascensor uniformemente.

**E[número de ascensores usados] = k·(1 − (1−1/k)^m)**

Para k=10, m=10: E = 10·(1 − (0.9)^{10}) ≈ 10·(1 − 0.349) = **6.51**.

~65% de los ascensores son llamados. Analogía directa con el problema de ocupación (cajas y bolas).

---

## Ruina con ventaja (doblar el capital)

p = 0.51 (ventaja pequeña del jugador), inicio en k = N/2 (meta doblar). P(llegar a N) ≈ ?

Con ρ = q/p = 0.49/0.51 ≈ 0.961:

P = (1 − ρ^k) / (1 − ρ^N)

Para N=100, k=50: P = (1 − 0.961^{50}) / (1 − 0.961^{100}) ≈ **0.862 / 0.875 ≈ 98.5%**

Una ventaja marginal del 1% casi garantiza doblar el capital dado suficientes manos.

---

## Suma máxima parcial

X₁,…,Xₙ i.i.d. con media 0, varianza 1. Mₙ = max_{1≤k≤n} Sₖ.

**E[Mₙ] ≈ √(2n/π)**

Para n=100: E[M₁₀₀] ≈ √(200/π) ≈ **7.98**. El máximo parcial crece como √n.

---

## La paradoja del autobús (doble cara)

Autobuses llegan como Poisson(λ). Llegas en tiempo aleatorio.

**E[próximo autobús] = 1/λ** (fácil).

**E[autobús anterior también] = 1/λ** (por falta de memoria de Poisson).

Luego E[intervalo completo que interceptas] = **2/λ** — el doble del intervalo típico.

Paradoja de la inspección: ves el doble del intervalo promedio porque llegas con más probabilidad durante intervalos largos.

---

## Duración del jugador

Ruina en barreras 0 y N, inicio en k, p = 1/2. Duración esperada hasta absorción:

**E[T | X₀=k] = k(N−k)**

Para k=5, N=10: E[T] = 25. Para k=N/2: E[T] = N²/4.

La duración máxima ocurre en el punto medio; es cuadrática en la escala del problema.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "P(ganar craps)" | 244/495 ≈ 49.3% |
| "E[Chuck-a-luck]" | −17/216 ≈ −7.9% |
| "Cerillas sobrantes en Banach" | ≈√(Nπ/2) |
| "p < 0.5, ¿tímido o audaz?" | Audaz siempre domina |
| "¿Martingala garantiza ganar?" | E[pérdida] = ∞ con capital finito |
| "Racha más larga en n lanzamientos" | ≈log₂(n) |
| "E[T₀] caminata aleatoria" | ∞ (recurrente nula) |
| "M/M/1 estable con ρ=λ/μ" | L=ρ/(1−ρ), W=1/(μ−λ) |
| "E[número ascensores usados]" | k·(1−(1−1/k)^m) |
| "E[duración, ruina p=1/2, inicio k]" | k(N−k) |

---

> **Síntesis:** Las apuestas y colas revelan la asimetría entre probabilidad y esperanza: P=1 de volver al origen, pero E[T]=∞. La ruina con p<0.5 es dominada por el juego audaz. La martingala no crea valor: solo redistribuye riesgo hacia la cola. En colas M/M/1, la Ley de Little (L=λW) conecta todas las métricas; ρ<1 es condición necesaria y suficiente para estabilidad.

---

*Retrieval: cierra y responde: (1) P(ganar craps exacta); (2) E[Chuck-a-luck por apuesta de $1]; (3) E[L] para M/M/1 con λ=3, μ=4; (4) E[duración para k=3, N=7, p=1/2].*
