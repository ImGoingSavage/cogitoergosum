# Fundamentos de probabilidad y conteo

## Reglas del conteo

**Regla de la multiplicación:** Si una tarea tiene k etapas, con n₁ opciones en la primera, n₂ en la segunda (independientemente), etc., el total de formas es n₁·n₂·…·nₖ.

**Permutaciones de n objetos distintos:** n! formas.

**Permutaciones de k objetos de n distintos (orden importa):** P(n,k) = n!/(n−k)!

**Combinaciones de k objetos de n (orden no importa):** C(n,k) = n!/(k!(n−k)!)

**Permutaciones con repetición** (n objetos con multiplicidades n₁,…,nₘ):

**n! / (n₁!·n₂!·…·nₘ!)** ← coeficiente multinomial

Ejemplo — STATISTICS (10 letras: S×3, T×3, I×2, A×1, C×1):
10!/(3!·3!·2!·1!·1!) = **50400**

---

## Principio de inclusión-exclusión

Para tres eventos:

**|A∪B∪C| = |A|+|B|+|C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|**

Regla mnemónica: suma los de orden 1, resta los de orden 2, suma los de orden 3, …

Para enteros del 1 al n divisibles por a o b o c: usa ⌊n/a⌋, ⌊n/ab⌋, etc.

---

## LOTUS (Law of the Unconscious Statistician)

**E[g(X)] = Σₓ g(x) · P(X=x)** (discreta)

**E[g(X)] = ∫ g(x) · f_X(x) dx** (continua)

No necesitas derivar la distribución de g(X). Trabajas directamente con la distribución de X.

Ejemplo — X ~ Geom(p): E[X] = Σ_{k=1}^∞ k·p(1−p)^{k-1} = p · d/dp [−(1−p)/(1−(1−p))] → **1/p**.

Ejemplo — X ~ Poisson(λ): E[X²] vía LOTUS = E[X(X-1)] + E[X] = **λ²+λ**.

---

## Linealidad de la esperanza

**E[aX + bY + c] = a·E[X] + b·E[Y] + c** (incluso si X e Y no son independientes)

Aplicación — E[puntos fijos de permutación aleatoria]:
Sea Xᵢ=1 si persona i recupera su sombrero. E[Xᵢ]=1/n.
E[X₁+…+Xₙ] = Σ E[Xᵢ] = n · (1/n) = **1** (para cualquier n).

---

## Esperanza y varianza de distribuciones básicas

| Distribución | E[X] | Var[X] |
|-------------|------|--------|
| Bernoulli(p) | p | p(1-p) |
| Bin(n,p) | np | np(1-p) |
| Geom(p) | 1/p | (1-p)/p² |
| Poisson(λ) | λ | λ |
| Uniform{1,...,n} | (n+1)/2 | (n²-1)/12 |
| Uniform[0,1] | 1/2 | 1/12 |

---

## Ley de la Probabilidad Total

Sea {A₁,…,Aₖ} una partición del espacio muestral (eventos disjuntos que cubren todo):

**P(B) = Σᵢ P(B|Aᵢ) · P(Aᵢ)**

Cuando usar: si P(B) es difícil directamente pero P(B|Aᵢ) es fácil para cada pieza Aᵢ.

Ejemplo: probabilidad de obtener positivo en una prueba médica = P(+|enfermo)·P(E) + P(+|sano)·P(Ē).

---

## Teorema de Bayes

**P(A|B) = P(B|A) · P(A) / P(B)**

Versión extendida con la regla total:

P(Aᵢ|B) = P(B|Aᵢ)·P(Aᵢ) / Σⱼ P(B|Aⱼ)·P(Aⱼ)

Terminología bayesiana: P(A) = prior; P(B|A) = verosimilitud; P(A|B) = posterior.

**Trampa clásica:** P(prueba+|enfermo) ≠ P(enfermo|prueba+). Con tasa base baja, la mayoría de los positivos son falsos.

---

## Muestreo con y sin reemplazo

| Modo | k objetos de n | Fórmula |
|------|---------------|---------|
| Con reemplazo, orden importa | n^k | |
| Con reemplazo, orden no importa | C(n+k−1, k) | "stars and bars" |
| Sin reemplazo, orden importa | P(n,k) | n!/(n−k)! |
| Sin reemplazo, orden no importa | C(n,k) | n!/(k!(n−k)!) |

**Regla del complemento:** P(al menos uno) = 1 − P(ninguno). Casi siempre más sencilla.

---

## Identidades combinatorias útiles

C(n,k) = C(n, n−k) — simetría

C(n,k) = C(n−1,k−1) + C(n−1,k) — identidad de Pascal

Σ_{k=0}^n C(n,k) = 2^n — subconjuntos de un conjunto de n elementos

Σ_{k=0}^n C(n,k)·x^k = (1+x)^n — teorema del binomio

---

## Mini-ejemplo trabajado: el problema de los sombreros sin tocar la independencia

n personas dejan su sombrero; se los devuelven al azar. ¿Cuántas esperan recuperar el suyo? La tentación es modelar la permutación completa (¡n! casos, dependencias horribles). En vez de eso, define indicadores: Xᵢ = 1 si la persona i recupera su sombrero. Por simetría P(Xᵢ=1) = 1/n, así que E[Xᵢ] = 1/n. Por **linealidad de la esperanza**:

> E[X₁+…+Xₙ] = Σ E[Xᵢ] = n · (1/n) = **1**

En promedio, exactamente **una** persona recupera su sombrero, *para cualquier n* —2 personas o un millón.

**Predicción antes de seguir:** los eventos Xᵢ no son independientes (si n−1 personas tienen su sombrero, la última también). ¿Eso rompe el cálculo? Respuesta: **no**. La linealidad de la esperanza no pide independencia; sumar esperanzas funciona aunque los sumandos estén correlacionados. Esa es justo su superpotencia: descompone un problema enredado en piezas triviales.

## Prototipo, contraejemplo y caso borde

- **Prototipo (complemento):** "P(al menos un éxito)" casi siempre es más fácil como 1 − P(ninguno); p. ej. P(al menos dos cumpleaños iguales) = 1 − (365·364·…)/365ⁿ.
- **Contraejemplo (Bayes invertido):** P(+|enfermo) ≠ P(enfermo|+). Con prevalencia 2% y test al 95%, la mayoría de positivos son falsos. Leer la verosimilitud como posterior es el error clásico.
- **Caso borde (orden sí/no importa):** "k de n con reemplazo sin orden" no es nᵏ ni C(n,k) sino C(n+k−1, k) (stars and bars). El borde fuerza a declarar si el orden y el reemplazo cuentan antes de elegir fórmula.

## Errores típicos

- **Conceptual:** exigir independencia para sumar esperanzas de indicadores (no hace falta).
- **Técnico:** olvidar dividir por las multiplicidades en anagramas (n!/(n₁!…)) y sobrecontar permutaciones de letras repetidas.
- **De interpretación:** confundir "con/sin reemplazo" o "ordenado/no ordenado", que cambian por completo la fórmula de conteo.

## Transferencia isomorfa

- **Linealidad de la esperanza ↔ conteo de eventos en sistemas:** "número esperado de coincidencias / colisiones / patrones" se resuelve con indicadores sin pelear con la dependencia, idéntico al conteo de patrones en una secuencia (conecta con [[arena-q9]]).
- **Bayes con tasa base ↔ VPP de un clasificador:** prior×verosimilitud/evidencia es exactamente el valor predictivo positivo; sin prevalencia no inviertes el condicional (conecta con [[arena-q2]]).
- **LOTUS ↔ valorar g(X) sin su distribución:** E[g(X)] = Σ g(x)P(x) evita derivar la distribución de g(X), como valorar un payoff f(S) integrando contra la densidad de S (conecta con [[arena-q5]]).
- **Inclusión-exclusión ↔ deduplicado por uniones:** sumar–restar solapamientos es el mismo principio que contar elementos únicos en uniones de conjuntos.

Moraleja de la arista: *para contar lo enredado, suma indicadores (la dependencia no estorba a la esperanza); para "al menos uno", usa el complemento; y nunca confundas la verosimilitud con el posterior.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "De cuántas formas ordenar con repeticiones" | n!/(n₁!·…·nₖ!) |
| "k objetos de n, sin orden, sin reemplazo" | C(n,k) |
| "k objetos de n, con orden, sin reemplazo" | P(n,k) |
| "E[función de VA]" | LOTUS directamente sobre distribución de X |
| "E[suma de indicadores]" | Linealidad; E[Xᵢ]·n |
| "P(algún evento) difícil" | Complemento: 1−P(ninguno) |
| "P(evento dado condición) → P(condición dado evento)" | Bayes con regla total |

---

> **Síntesis:** El conteo provee el espacio muestral; las reglas de probabilidad navegan en él. LOTUS y linealidad son los dos atajos más poderosos: LOTUS evita derivar nuevas distribuciones; linealidad elimina la necesidad de independencia. Bayes actualiza creencias. El principio de complemento simplifica "al menos uno".

---

*Retrieval: cierra y responde: (1) anagramas de PROBABILITY; (2) E[X²] para X~Poisson(3); (3) P(divisible por 2 o 3 entre 1 y 60); (4) P(primer positivo en enfermedad 2%, sensibilidad 90%, especificidad 95%).*
