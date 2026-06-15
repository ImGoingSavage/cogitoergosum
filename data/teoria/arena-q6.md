# Estadística inferencial · Distribuciones y estimación

## Regla 68-95-99.7

Para X ~ N(μ, σ²):

| Rango | Probabilidad |
|-------|-------------|
| μ ± 1σ | 68.27% |
| μ ± 2σ | 95.45% |
| μ ± 3σ | 99.73% |
| μ ± 4σ | 99.9937% (~1 en 15 800) |

**Clave de reconocimiento:** "dato a 4σ" → probabilidad < 0.01% bajo normalidad; en mercados ocurre con frecuencia mayor → las colas reales son más pesadas (leptocúrticas).

---

## LGN vs CLT

Ambos hablan sobre n observaciones i.i.d., pero son proposiciones distintas:

| | LGN | TCL |
|---|---|---|
| ¿Qué converge? | X̄_n → μ (en probabilidad) | √n(X̄_n − μ)/σ → N(0,1) en distribución |
| ¿Qué requiere? | E[X] < ∞ | σ² < ∞ (TCL clásico) |
| ¿Es sobre la distribución? | No; solo el valor límite | Sí; dice la forma de la distribución |

**Si σ² = ∞ (Cauchy):** LGN falla; TCL clásico no aplica. Existe una versión del TCL con distribuciones estables de Lévy.

---

## Error estándar de la media

σ_X̄ = σ / √n

- σ: variabilidad de una observación.
- σ_X̄: variabilidad del promedio de n observaciones.
- Para reducir el error a la mitad → cuadruplicar n (porque √(4n) = 2√n).

La misma raíz aparece en finanzas: σ(T) = σ(1 día)·√T para retornos i.i.d.

---

## P-valor — la definición correcta

**p = P(observar datos tan extremos o más | H₀ es verdadera)**

Errores frecuentes:

| Afirmación | ¿Correcta? |
|-----------|-----------|
| "p = probabilidad de que H₀ sea falsa" | ✗ (requeriría Bayes) |
| "p = probabilidad de que los datos sean por azar" | ✗ (impreciso) |
| "p < 0.05 → el efecto es importante" | ✗ (confunde significancia estadística con práctica) |
| "p = P(datos extremos \| H₀)" | ✓ |

Un p-valor pequeño dice: *si H₀ fuera verdadera, estos datos serían improbables.* No dice nada sobre cuán probable es H₀.

---

## Errores tipo I y tipo II

| | H₀ verdadera | H₀ falsa |
|---|---|---|
| **Rechazar H₀** | Error tipo I (α) — falso positivo | Correcto (poder) |
| **No rechazar H₀** | Correcto | Error tipo II (β) — falso negativo |

**Poder = 1 − β** = P(rechazar H₀ | H₁ verdadera).

Factores que aumentan el poder: mayor n, mayor efecto real, menor σ, mayor α.

**Tensión:** reducir α aumenta β para n fijo. Solo aumentar n mejora ambos simultáneamente.

---

## Varianza de suma de variables

**Var(X + Y) = Var(X) + Var(Y) + 2·Cov(X, Y)**

**Var(X − Y) = Var(X) + Var(Y) − 2·Cov(X, Y)**

Caso i.i.d.: Var(Σ Xᵢ) = n·Var(X) → SD(Σ Xᵢ) = √n·σ. Esto fundamenta la regla √T.

En portfolios: ρ < 0 reduce la varianza conjunta (diversificación).

---

## Correlación ρ y sus límites

ρ(X, Y) = Cov(X, Y) / (σ_X · σ_Y) ∈ [−1, 1]

- ρ = 1: relación lineal perfecta positiva (Y = aX + b, a > 0).
- ρ = 0: no correlación lineal (no implica independencia — Y = X² puede tener ρ = 0).
- ρ = −1: relación lineal perfecta negativa.

**Trampa frecuente:** ρ ≈ 0 ≠ independencia. Siempre distingue correlación de independencia.

---

## R² en regresión lineal

R² = 1 − SSR/SST = fracción de la varianza de Y explicada por el modelo.

- SSR = Σ(yᵢ − ŷᵢ)² (residuos al cuadrado).
- SST = Σ(yᵢ − ȳ)² (varianza total de Y escalada).

**R² ajustado** penaliza predictores adicionales: R²_adj = 1 − (1−R²)(n−1)/(n−p−1). R² nunca baja al agregar variables; R²_adj sí puede bajar.

**Límite:** R² alto ≠ causalidad ni buena predicción fuera de muestra.

---

## Ley de la esperanza total

**E[X] = E[E[X|Y]]** (también llamada "torre de la esperanza")

Versión discreta: E[X] = Σ_y E[X | Y=y] · P(Y=y)

Uso: cuando hay una estructura condicional natural (primer evento, estado actual), escribir la ecuación y resolver.

**Ejemplo — distribución geométrica:**
E[X] = p·1 + (1−p)·(1 + E[X])  →  E[X] = 1/p

---

## Ley de la varianza total

**Var(X) = E[Var(X|Y)] + Var(E[X|Y])**

- Primer término: varianza media dentro de cada grupo (within-group).
- Segundo término: varianza de las medias entre grupos (between-group).

Fundamento de ANOVA y modelos mixtos. Si Y no es informativa: Var(E[X|Y]) ≈ 0, todo es varianza within.

---

## Problema del coleccionista de cupones

n tipos distintos, distribución uniforme.

**E[T] = n · H_n = n · (1 + 1/2 + 1/3 + … + 1/n)**

Para n=4: E[T] = 4·(25/12) ≈ 8.33. Para n=10: E[T] ≈ 29.3.

Derivación: cuando tienes k distintos, la probabilidad de uno nuevo es (n−k)/n → tiempo esperado = n/(n−k). Suma por linealidad.

Aplicaciones: caching, cobertura de casos de prueba, coleccionar todos los tipos de error.

---

## MLE y mínimos cuadrados

Para εᵢ ~ N(0, σ²) i.i.d. en el modelo Y = Xβ + ε:

log-verosimilitud = −(n/2)log(2πσ²) − (1/2σ²) · ‖y − Xβ‖²

Maximizar respecto a β ≡ minimizar ‖y − Xβ‖² → OLS.

Si los errores son Laplace (doble exponencial): MLE → mínimo de Σ|εᵢ| (LAD regression, más robusta).

---

## Distribución chi-cuadrado

Si Z₁, …, Zₙ ~ N(0,1) i.i.d., entonces Q = Σ Zᵢ² ~ χ²(n).

- E[Q] = n; Var[Q] = 2n.
- χ²(2) es exponencial con media 2.
- n·S²/σ² ~ χ²(n−1) (estimador de varianza muestral).
- t(k) = Z / √(χ²(k)/k); F(p,q) = χ²(p)/p / (χ²(q)/q).

---

## Transformaciones lineales de la normal

Si X ~ N(μ, σ²):

- Y = aX + b ~ N(aμ + b, a²σ²).
- X₁ + X₂ ~ N(μ₁ + μ₂, σ₁² + σ₂²) si son independientes.
- Con correlación: Var(X₁ + X₂) = σ₁² + σ₂² + 2ρσ₁σ₂.

La familia normal es cerrada bajo transformaciones lineales y convoluciones — la propiedad más útil en probabilidad aplicada.

---

## Mini-ejemplo trabajado: la torre de esperanza resuelve la geométrica

¿Cuántos lanzamientos esperas hasta la primera cara con moneda justa? En vez de sumar la serie, condiciona en el primer lanzamiento (eso es la torre E[X] = E[E[X|primer tiro]]):

> E[X] = (1/2)·1 + (1/2)·(1 + E[X])

El primer término: con prob 1/2 sale cara y terminas en 1 tiro. El segundo: con prob 1/2 sale cruz, gastaste 1 tiro y **vuelves al mismo estado**. Despejando: E[X] − (1/2)E[X] = 1 → E[X] = **2**. Generaliza a sesgo p: E[X] = 1/p.

**Predicción antes de seguir:** ¿la varianza de la media muestral de 100 tiros de un dado es mayor o menor que la de un solo tiro? Respuesta: **menor, por un factor 100** (σ²/n). Promediar no cambia la media pero divide la varianza entre n; por eso para *reducir el error a la mitad* hay que *cuadruplicar* n. La misma √n que reaparece en la regla √T de finanzas.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** proceso con reinicio o estructura condicional (geométrica, coleccionista, primer éxito) → plantea la torre E[X] = Σ E[X|Y]P(Y) y resuelve la ecuación lineal.
- **Contraejemplo (ρ=0 ≠ independencia):** Y = X² con X simétrica tiene Cov(X,Y)=0, así que ρ=0, pero Y depende totalmente de X. Correlación cero solo descarta relación *lineal*.
- **Caso borde (Cauchy):** si σ²=∞, la LGN clásica falla y el TCL clásico no aplica; promediar muestras de Cauchy no concentra nada. El borde revela qué supuesto (varianza finita) sostiene ambos teoremas.

## Errores típicos

- **Conceptual:** leer el p-valor como P(H₀ verdadera|datos). Es P(datos tan extremos|H₀) — el condicional invertido, el mismo error que confundir sensibilidad con VPP.
- **Técnico:** reportar R² alto como evidencia de buen modelo: R² nunca baja al añadir variables; usa R²_adj y validación fuera de muestra.
- **De supuestos:** aplicar el TCL con n pequeño y cola pesada, o usar σ/√n cuando las observaciones están autocorrelacionadas (entonces el n "efectivo" es menor).

## Transferencia isomorfa

Las dos llaves maestras —la √n y la torre— cruzan dominios:

- **Error estándar σ/√n ↔ regla √T de volatilidad:** ambas salen de Var(ΣXᵢ)=n·Var(X) para i.i.d.; reducir incertidumbre con más datos y escalar riesgo con el horizonte son la misma raíz (conecta con [[arena-q5]] y [[arena-q7]]).
- **p-valor ↔ tasa base / VPP:** "datos improbables bajo H₀" no es "H₀ improbable", igual que "sensibilidad alta" no es "VPP alto"; sin la prior/tasa base no inviertes el condicional (conecta con [[arena-q2]]).
- **Ley de varianza total ↔ descomposición sesgo-varianza:** within + between es la misma partición que error irreducible vs varianza del modelo en ML (conecta con [[arena-iml4]], donde se descompone el error de predicción).
- **Torre de esperanza ↔ backward induction / DP:** condicionar en el primer paso y resolver la recurrencia es el motor de la parada óptima (conecta con [[arena-cc3]]).

Moraleja de la arista: *cuando algo tiene estructura condicional, condiciona en el primer paso; cuando promedias n cosas i.i.d., la incertidumbre cae como 1/√n — no más rápido.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Dato a kσ de la media" | Regla 68-95-99.7; a >3σ ya es muy inusual |
| "Media muestral de n obs." | σ_X̄ = σ/√n |
| "¿Qué significa p=0.03?" | P(datos extremos \| H₀), NO P(H₀ falsa) |
| "Tipo I vs tipo II" | FP vs FN; ambos dependen del umbral |
| "Var(X+Y) con correlación" | Var(X) + Var(Y) + 2Cov |
| "E[] de proceso con reinicio" | Torre: E[X] = p·a + (1−p)·(b + E[X]) |
| "Coleccionar n tipos" | E[T] = n·H_n |
| "Suma de cuadrados de normales" | χ²(n): E=n, Var=2n |

---

> **Síntesis:** La estadística inferencial conecta la variabilidad de los datos con la precisión de los estimadores (√n), las decisiones bajo incertidumbre (p-valor, potencia) y la estructura condicional (torre de E[]). La ley de la esperanza total es la llave maestra: convierte recurrencias y árbol de probabilidad en una ecuación lineal.

---

*Retrieval: cierra y responde: (1) regla 68-95-99.7, (2) diferencia LGN/CLT, (3) E[X] distribución geométrica con probabilidad p, (4) E[coleccionista con n=5 cupones].*
