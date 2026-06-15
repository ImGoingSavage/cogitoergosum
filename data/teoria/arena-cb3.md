# Contraste de hipótesis: NP Lemma, LRT y tests UMP

## Configuración básica

Hipótesis: H₀: θ∈Θ₀ vs H₁: θ∈Θ₁ (Θ = Θ₀∪Θ₁)

**Función de potencia:** β(θ) = Pθ(X∈R) — probabilidad de rechazar H₀ cuando θ es el verdadero valor.

| Error | Definición | Probabilidad |
|-------|------------|--------------|
| Tipo I (falso positivo) | Rechazar H₀ cuando θ∈Θ₀ | α = sup_{θ∈Θ₀} β(θ) |
| Tipo II (falso negativo) | Aceptar H₀ cuando θ∈Θ₁ | 1−β(θ), θ∈Θ₁ |

**Nivel de significancia:** α = tamaño del test (máx error tipo I).  
**Potencia:** β(θ) para θ∈Θ₁ (queremos maximizarla).

---

## Lema de Neyman-Pearson (NP)

Para testar H₀: θ=θ₀ vs H₁: θ=θ₁ (hipótesis simples), el **test más potente de tamaño α** rechaza H₀ cuando:

**f(x|θ₁)/f(x|θ₀) > k**

donde k se elige para que P_{θ₀}(razón > k) = α.

Consecuencia: el test NP es una función del cociente de verosimilitudes. La región crítica tiene la forma {x: L(θ₁|x)/L(θ₀|x) > k}.

**Ejemplo (Normal σ² conocida):** Para H₀: μ=μ₀ vs H₁: μ=μ₁ (μ₁>μ₀):

El cociente es exp((μ₁−μ₀)(Σxᵢ/σ²)−...), que aumenta en Σxᵢ → rechaza si X̄>k'. Es el test z unilateral.

---

## Razón de monotona de verosimilitudes (MLR)

Una familia {f(x|θ)} tiene **MLR** en T(x) si para θ₂>θ₁, el cociente f(x|θ₂)/f(x|θ₁) es función no decreciente de T(x).

Familias con MLR en X̄ (o estadístico suficiente): Normal, Poisson, Binomial, Exponencial, Gamma.

**No tiene MLR:** Cauchy (cola simétrica sin monotonía), distribución bimodal.

---

## Tests UMP (uniformemente más potentes)

Un test φ es **UMP de nivel α** si es de nivel α y β(θ) ≥ β'(θ) para todo θ∈Θ₁ y todo test alternativo φ' de nivel α.

**Corolario del MLR:** Si la familia tiene MLR en T, el test UMP de nivel α para H₀: θ≤θ₀ vs H₁: θ>θ₀ rechaza cuando T > c, donde P_{θ₀}(T>c) = α.

| Distribución | Test UMP (unilateral) |
|-------------|----------------------|
| Normal(μ,σ²) σ² conocida, H₀: μ≤μ₀ | Rechaza si X̄ > μ₀+z_α σ/√n |
| Poisson(λ), H₀: λ≤λ₀ | Rechaza si ΣXᵢ > c |
| Bernoulli(p), H₀: p≤p₀ | Rechaza si ΣXᵢ > c |
| Beta(θ,1), H₀: θ≤1 | Rechaza si Σlog Xᵢ < −c |
| Exponencial(θ), H₀: θ≤θ₀ | Rechaza si ΣXᵢ > c |

**No existe test UMP para hipótesis bilaterales** H₀: θ=θ₀ vs H₁: θ≠θ₀ en general (salvo en la familia exponencial de un parámetro, donde el test de dos colas es UMP entre los tests no sesgados).

---

## Razón de verosimilitud (LRT)

Para hipótesis compuestas, el **estadístico LRT** es:

λ(x) = sup_{θ∈Θ₀} L(θ|x) / sup_{θ∈Θ} L(θ|x)

Rechaza H₀ si λ(x) < k.

**Distribución asintótica (Wilks):** Bajo H₀, −2 log λ(X) →_d χ²(dim Θ − dim Θ₀).

Esta es la base de todos los tests F, t², chi-cuadrado y análisis de varianza.

| Test | Estadístico LRT |
|------|----------------|
| Normal: H₀: μ=μ₀ (σ² conocida) | z = (X̄−μ₀)/(σ/√n), rechaza si |z|>z_{α/2} |
| Normal: H₀: μ=μ₀ (σ² desconocida) | t = (X̄−μ₀)/(S/√n), rechaza si |t|>t_{n−1,α/2} |
| Normal: H₀: σ²=σ₀² | χ² = (n−1)S²/σ₀², rechaza si χ² fuera del IC |
| Dos medias normales iguales | t test de dos muestras |
| Igualdad de varianzas | F = S₁²/S₂², rechaza si F fuera del IC |

---

## p-valores

El **p-valor** es la probabilidad, bajo H₀, de observar algo tan o más extremo que los datos:

p(x) = sup_{θ∈Θ₀} P_{θ}(W(X) ≥ W(x))

donde W es el estadístico del test. Rechaza H₀ si p ≤ α.

**Paradoja de Lindley:** Para tests bilaterales, el p-valor y la probabilidad posterior P(H₀|x) pueden diferir enormemente. Con n grande y x moderado, el p-valor puede ser <.05 mientras P(H₀|x) > 0.50.

---

## Tamaño muestral

Para test bilateral de media normal: si se desea potencia β* en θ=μ₁ con nivel α:

n ≥ (z_{α/2} + z_{β*})²·σ² / (μ₁−μ₀)²

Ejemplo: α=.05, β*=.90 da z_{α/2}+z_{β*}≈1.96+1.28=3.24.

---

## Mini-ejemplo trabajado: del cociente NP al test z

H₀: μ=0 vs H₁: μ=1, datos N(μ,1), n observaciones. El lema de Neyman-Pearson dice: el test **más potente** rechaza cuando la razón de verosimilitudes supera un umbral:

> L(1|x)/L(0|x) = exp(Σxᵢ − n/2) > k

Tomar logaritmo: Σxᵢ > k', es decir **X̄ > c**. El test óptimo no es una regla arbitraria: *cae* sobre el promedio, y c se fija para que P₀(X̄>c)=α. Así, el famoso test z unilateral es simplemente el cociente de verosimilitudes disfrazado.

**Predicción antes de seguir:** si la alternativa fuera bilateral (H₁: μ≠0), ¿sigue existiendo un único test más potente? Respuesta: **no** — para μ>0 conviene rechazar a la derecha y para μ<0 a la izquierda, y ningún test maximiza la potencia en *ambos* lados a la vez. Por eso no existe UMP bilateral en general; se recurre al LRT. La monotonía del cociente (MLR) es justo lo que salva el caso unilateral.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** familia con razón de verosimilitud monótona (MLR) en T → test UMP unilateral "rechaza si T>c".
- **Contraejemplo (Cauchy sin MLR):** la Cauchy no tiene MLR, así que ni siquiera el caso unilateral admite UMP simple; el cociente no es monótono.
- **Caso borde (paradoja de Lindley):** con n enorme, un p-valor de 0.04 puede convenir con P(H₀|datos)>0.5. El borde revela que p pequeño no es "H₀ improbable"; frecuentista y bayesiano divergen.

## Errores típicos

- **Conceptual:** leer el p-valor como P(H₀|datos); es P(estadístico tan extremo | H₀), el mismo condicional invertido que confunde sensibilidad con VPP.
- **Técnico:** usar χ²(1) para −2lnλ cuando hay r restricciones (debe ser χ²(r)) o cerca de un borde del espacio paramétrico (la asintótica de Wilks falla).
- **De supuestos:** buscar un UMP bilateral donde no existe en vez de usar el LRT.

## Transferencia isomorfa

- **Cociente de verosimilitudes NP ↔ likelihood ratio de un test diagnóstico:** "rechaza si L(H₁)/L(H₀)>k" es exactamente actualizar odds con LR⁺; el umbral k fija el trade-off sensibilidad/especificidad (conecta con [[arena-q2]]).
- **Función de potencia / UMP ↔ ROC y umbral óptimo:** elegir c que maximiza la potencia a α fijo es deslizarse por la curva ROC hasta el punto de operación; Neyman-Pearson *es* la teoría de detección óptima (conecta con [[arena-htd4]]).
- **LRT −2lnλ ~ χ²(r) ↔ comparación de modelos anidados:** el test de razón de verosimilitudes sustenta selección por verosimilitud, F-tests y deviance de GLM (conecta con [[arena-dg2]]).
- **p-valor uniforme bajo H₀ ↔ calibración:** que p~U(0,1) cuando H₀ es cierta es la base de chequear si un test (o un modelo) está bien calibrado (conecta con [[arena-dg3]]).

Moraleja de la arista: *el test óptimo siempre es un cociente de verosimilitudes contra un umbral; deslizar ese umbral es recorrer la ROC, y un p pequeño mide sorpresa bajo H₀, no la verdad de H₀.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Hipótesis simples vs simple, test más potente" | NP Lemma: rechaza si L(θ₁)/L(θ₀) > k |
| "Hipótesis unilateral, familia con MLR" | Test UMP: rechaza si T > c |
| "No existe UMP bilateral" | LRT o test de dos colas si familia exponencial unilateral |
| "Hipótesis compuesta, parámetros bajo H₀" | LRT: λ=sup_{Θ₀}L / sup_{Θ}L |
| "Distribución asintótica del LRT" | −2 log λ →_d χ²_r (r = grados de libertad de H₀) |
| "Medir evidencia sin umbral fijo" | p-valor: probabilidad de datos más extremos bajo H₀ |

---

> **Síntesis (Casella & Berger, Ch 8):** El lema NP fija el ideal (test más potente entre todos de nivel α). El MLR lo extiende a familias unilaterales. El LRT es el método universal para hipótesis compuestas; su distribución asintótica chi-cuadrado lo hace omnipresente. El p-valor es la moneda del reino, pero tiene límites bayesianos serios con n grande.

---

*Retrieval: (1) Enuncia el lema de Neyman-Pearson y da su región de rechazo. (2) X₁,…,Xₙ i.i.d. Poisson(λ), H₀: λ≤1 vs H₁: λ>1: ¿cuál es el test UMP? (3) ¿Cuándo NO existe test UMP? (4) Da la distribución asintótica de −2 log λ bajo H₀.*
