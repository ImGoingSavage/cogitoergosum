# Probabilidad y Bayes · Entrevistas cuantitativas

## Bayes con tasa base

La fórmula de Bayes es simple; la trampa es la **tasa base (prevalencia)**.

P(E|+) = P(+|E)·P(E) / [P(+|E)·P(E) + P(+|¬E)·P(¬E)]

**Ejemplo canónico:** prevalencia 0.5%, sensibilidad 100%, especificidad 93% (FP=7%).

- Numerador = 1 × 0.005 = 0.005
- Denominador = 0.005 + 0.07 × 0.995 ≈ 0.0747
- P(E|+) ≈ **6.7%**

La lección: con prevalencia baja, la mayoría de positivos son falsos positivos. En 10 000 personas: 50 verdaderos positivos vs ~697 falsos positivos → 14 falsos por cada verdadero.

---

## El problema de Monty Hall

Eliges puerta A (P=1/3 de premio). El anfitrión —con información— abre una puerta vacía diferente. La probabilidad del premio en A sigue siendo 1/3; la otra puerta no elegida hereda las 2/3.

**Cambiar siempre gana con P=2/3.**

Error clásico: "quedan 2 puertas, P=1/2". Incorrecto porque el anfitrión actúa con información, no al azar.

Verificación de fuerza bruta (3 escenarios igualmente probables):
- Premio en A: te quedas → ganas; cambias → pierdes.
- Premio en B: te quedas → pierdes; cambias → ganas.
- Premio en C: te quedas → pierdes; cambias → ganas.

Cambiar gana 2/3.

---

## Geometría probabilística

**Triángulo de palo roto:** P(3 trozos forman triángulo) = **1/4**.

Condición: cada trozo < 1/2. Con cortes en X e Y (0<X<Y<1), el espacio muestral es el triángulo superior {0<X<Y<1}. La región favorable tiene área 1/4 del espacio total.

**Cita de reconocimiento:** problema de longitudes aleatorias → dibujar el espacio muestral geométrico.

---

## Moneda de dos caras — Bayes secuencial

Frasco: 999 justas + 1 de dos caras. Observas 10 caras seguidas.

P(2C|10H) = 1/1000 / [1/1000 + (1/1024)×(999/1000)] = 1024/2023 ≈ **50.6%**

Intuición: la moneda de dos caras es 1024 veces más probable de producir el evento observado. Aunque es muy rara (1/1000), esa ventaja de likelihood casi cancela su rareza.

---

## Valor esperado con cadena de estados

Para calcular E[lanzamientos hasta k caras consecutivas con moneda justa (p=1/2):

Define estados: E₀ = "empezando", E₁ = "última fue cara", …, Eₖ₋₁ = "k−1 consecutivas".

**Sistema de ecuaciones (p=1/2):**
- E₀ = 1 + (1/2)E₁ + (1/2)E₀
- E₁ = 1 + (1/2)E₂ + (1/2)E₀
- …
- Eₖ₋₁ = 1 + (1/2)·0 + (1/2)E₀

**Solución general:** E₀ = 2 + 4 + 8 + … + 2ᵏ = 2(2ᵏ − 1)

| k | E[lanzamientos] |
|---|----------------|
| 2 | 6 |
| 3 | 14 |
| 4 | 30 |

---

## Ruleta rusa — probabilidad condicional en estados

2 balas contiguas en revólver de 6 recámaras. Sobreviviste al primer disparo (el tambor ya giró).

Dado que sobreviviste, las posiciones posibles de las balas son {2,3},{3,4},{4,5},{5,6} (4 casos igualmente probables). Solo {2,3} pone bala en la siguiente recámara.

- **No girar:** P(sobrevivir) = 3/4 = 75%
- **Girar:** P(sobrevivir) = 4/6 ≈ 66.7%

**No gires.**

---

## Optimización de probabilidad — frascos y bolas

50 blancas + 50 negras en 2 frascos, ojo vendado.

**Óptimo:** 1 blanca en frasco A, 49 blancas + 50 negras en frasco B.

P = 1/2 × 1 + 1/2 × (49/99) = 1/2 + 49/198 ≈ **74.75%**

Lógica: el frasco A garantiza P=1 cuando se elige. El frasco B maximiza la proporción condicionada. Ninguna otra distribución supera esta.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Prueba positiva, ¿qué probabilidad?" | Bayes con tasa base: prevalencia × sensibilidad / P(+) |
| "El anfitrión abre una puerta" | Monty Hall: cambia → P=2/3 |
| "¿Puedes formar un triángulo?" | Geometría del espacio de muestras |
| "¿Cuántos lanzamientos hasta k seguidos?" | Sistema de ecuaciones de estado → E=Σ2ⁱ |
| "¿Giras el tambor?" | Condiciona en haber sobrevivido y cuenta estados válidos |
| "Distribuir entre frascos para maximizar P" | Un frasco con certeza, el otro con máxima proporción |

---

> **Síntesis:** Probabilidad en entrevistas quant mide si ves la condición correcta. Monty Hall, Bayes y ruleta rusa fallan si calculas sin condicionar bien. El árbol de probabilidad siempre es tu aliado.

---

*Retrieval: sin mirar, calcula: (1) P(E|+) con prevalencia 1%, sensibilidad 95%, FP=10%; (2) E[lanzamientos para 2 caras seguidas]; (3) optimización del frasco.*
