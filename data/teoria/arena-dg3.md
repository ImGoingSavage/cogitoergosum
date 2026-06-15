# Intervalos de confianza y tests de hipótesis

## Intervalos de confianza — construcción via pivote

**Pivote:** función Q(X,θ) con distribución **conocida** que no depende de θ.

**Construcción del IC:** P(q_{α/2} ≤ Q ≤ q_{1-α/2}) = 1-α → despejar θ.

| Problema | Pivote | Distribución |
|---------|--------|-------------|
| μ, σ conocida | (X̄-μ)/(σ/√n) | N(0,1) |
| μ, σ desconocida | (X̄-μ)/(S/√n) | t(n-1) |
| σ² | (n-1)S²/σ² | χ²(n-1) |
| p (Bernoulli) | (p̂-p)/√(p(1-p)/n) | N(0,1) aprox. |
| μ₁-μ₂, σᵢ desconocidas | Welch t | t(ν_Welch) |

---

## IC para la media (σ conocida)

**IC al (1-α)%:** X̄ ± z_{α/2} · σ/√n

Donde z_{α/2} es el percentil 1-α/2 de N(0,1):
- 90%: z=1.645; 95%: z=1.96; 99%: z=2.576

**Semiancho:** ME = z_{α/2} · σ/√n

Para lograr ME ≤ e: **n ≥ (z_{α/2}·σ/e)²**

---

## IC para la media (σ desconocida — t de Student)

**IC al (1-α)%:** X̄ ± t_{α/2,n-1} · S/√n

| n | t_{0.025,n-1} |
|---|-------------|
| 5 | 2.776 |
| 10 | 2.228 |
| 20 | 2.093 |
| 30 | 2.045 |
| ∞ | 1.960 |

Para muestras grandes (n≥30), t ≈ z — la diferencia es pequeña.

---

## IC para la varianza

**IC al (1-α)% para σ²:**

**[(n-1)S²/χ²_{α/2,n-1}, (n-1)S²/χ²_{1-α/2,n-1}]**

El IC para σ² es **asimétrico** porque la chi-cuadrado no es simétrica.

---

## Tests de hipótesis — estructura

| Componente | Definición |
|------------|-----------|
| H₀ | Hipótesis nula (status quo) |
| H₁ | Hipótesis alternativa (lo que quieres mostrar) |
| Estadístico de test | T = función de los datos |
| Región de rechazo | Valores de T incompatibles con H₀ |
| Nivel α | P(rechazar H₀ | H₀ verdadera) = error tipo I |
| Potencia | P(rechazar H₀ | H₁ verdadera) = 1 - error tipo II |

**Regla de decisión:** rechaza H₀ si T cae en la región de rechazo.

---

## El p-value

**p-value = P(observar un estadístico tan extremo o más extremo | H₀)**

- p < α → rechaza H₀
- p-value bajo H₀ es Uniform[0,1]
- NO es P(H₀ es verdadera)
- NO es P(observar los mismos datos)

Para test z bilateral: **p-value = 2·P(Z > |z_obs|)**

Para test t con n-1 df: **p-value = 2·P(t(n-1) > |t_obs|)**

---

## Errores tipo I y tipo II

| | H₀ verdadera | H₀ falsa |
|--|--------------|----------|
| Rechazar H₀ | Error tipo I (α) | Correcto (potencia) |
| No rechazar H₀ | Correcto (1-α) | Error tipo II (β) |

**Tradeoff:** Al bajar α, sube β (con n fijo). Para reducir ambos: aumentar n.

---

## Test t para una muestra

H₀: μ = μ₀ vs H₁: μ ≠ μ₀

**Estadístico:** t = (X̄ − μ₀) / (S/√n) ~ t(n-1) bajo H₀

Rechazar si |t| > t_{α/2, n-1}.

**Equivalencia IC-test:** H₀:μ=μ₀ se rechaza al nivel α ↔ μ₀ no está en el IC al (1-α)% para μ.

---

## Test t para dos muestras (Welch)

H₀: μ₁ = μ₂ (varianzas posiblemente desiguales):

**t = (X̄₁ − X̄₂) / √(S₁²/n₁ + S₂²/n₂)**

Con grados de libertad de Welch:

**ν = (S₁²/n₁ + S₂²/n₂)² / [(S₁²/n₁)²/(n₁-1) + (S₂²/n₂)²/(n₂-1)]**

---

## Tests chi-cuadrado

**Bondad de ajuste:** H₀: la distribución es f(x|θ₀).

χ² = Σᵢ (Oᵢ − Eᵢ)² / Eᵢ ~ χ²(k-1-p) bajo H₀

donde k = número de categorías, p = parámetros estimados de los datos.

**Independencia (tabla de contingencia):** H₀: las variables son independientes.

χ² = Σᵢⱼ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ ~ χ²((r-1)(c-1)) bajo H₀

donde Eᵢⱼ = (fila i total)×(col j total) / n.

---

## Diseño del tamaño de muestra

Para test z unilateral (H₁:μ=μ₁>μ₀) con nivel α y potencia 1-β:

**n = (z_{α} + z_{β})² · σ² / (μ₁-μ₀)²**

Valores típicos:
- α=0.05, potencia=80% (β=0.20): z_{0.05}=1.645, z_{0.20}=0.842 → n≈7.85·σ²/δ²
- α=0.05, potencia=90%: z_{0.10}=1.282 → n≈10.5·σ²/δ²

---

## Corrección de tests múltiples

Tasa de error familiar (FWER) con m tests independientes al nivel α:
P(al menos 1 error tipo I) = 1-(1-α)^m ≈ m·α para α pequeño.

**Bonferroni:** usa α_corr=α/m → FWER ≤ α. Conservadora.

**Benjamini-Hochberg (BH):** controla FDR (False Discovery Rate), no FWER. Más potente que Bonferroni.

---

## Mini-ejemplo trabajado: test t y su IC dual, a mano

n=25, X̄=6, S=4, y quieres contrastar H₀: μ=5. El estadístico:

> t = (X̄ − μ₀)/(S/√n) = (6 − 5)/(4/5) = 1/0.8 = **1.25**

Con 24 grados de libertad, el crítico bilateral al 5% es ≈2.064. Como |1.25| < 2.064, **no rechazas H₀**. Y de forma equivalente, el IC del 95% es 6 ± 2.064·0.8 = (4.35, 7.65), que **contiene** el 5. Misma decisión por dos caminos: ese es el principio de dualidad IC↔test.

**Predicción antes de seguir:** si cuadruplicas el tamaño a n=100 (mismos X̄, S), ¿qué le pasa al estadístico y al ancho del IC? Respuesta: el error estándar S/√n cae a la **mitad** (√100=10 vs 5), así que t≈2.5 (ahora *sí* rechazas) y el IC se estrecha a la mitad. Cuadruplicar n duplica la precisión — la misma √n de σ/√n que aparece por todas partes. No es que el efecto crezca; es que lo ves mejor.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** un parámetro, un pivote con distribución conocida (z, t, χ²) → construyes IC y test simultáneamente.
- **Contraejemplo (p-valor mal leído):** p=0.03 NO es "97% de que H₁ sea cierta" ni "3% de que los datos sean azar"; es P(datos tan extremos | H₀). Confundirlo con P(H₀|datos) es el mismo error de condicional invertido que la tasa base.
- **Caso borde (IC de σ² asimétrico):** como la χ² no es simétrica, el IC de la varianza no se centra en S²; usar ± simétrico es incorrecto. El borde recuerda que el pivote dicta la forma.

## Errores típicos

- **Conceptual:** interpretar "no rechazar H₀" como "H₀ es verdadera"; solo significa evidencia insuficiente.
- **Técnico:** usar z en vez de t con n pequeño y σ desconocida (subestima el ancho del IC).
- **De supuestos:** correr m tests y reportar el p<0.05 más bonito sin corregir (FWER ≈ m·α); con 20 tests, esperas ~1 falso positivo por azar.

## Transferencia isomorfa

- **Error tipo I/II ↔ falso positivo/negativo de un clasificador:** α y β son exactamente 1−especificidad y 1−sensibilidad; la curva de potencia es la ROC del test (conecta con [[arena-q2]] y [[arena-htd4]]).
- **p-valor uniforme bajo H₀ ↔ transformada integral:** que p~U(0,1) cuando H₀ es cierta es la misma propiedad CDF→uniforme de la valoración probabilística (conecta con [[arena-q6]]).
- **Corrección de tests múltiples ↔ peeking en A/B testing:** mirar muchas métricas o parar temprano infla el error tipo I; Bonferroni/BH son el antídoto, igual que en experimentación online (conecta con [[arena-obs1]], monitoreo de muchas señales).
- **Tamaño de muestra n≈(z_α+z_β)²σ²/δ² ↔ MDE de un experimento:** diseñar potencia es elegir el efecto mínimo detectable antes de lanzar (conecta con [[arena-dmls3]], rollout/experimentos).

Moraleja de la arista: *IC y test son el mismo objeto visto de dos lados; el p-valor mide sorpresa bajo H₀, no la verdad de H₀; y la √n manda en la precisión.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "IC con σ conocida" | z_{α/2}·σ/√n |
| "IC con σ desconocida" | t_{α/2,n-1}·S/√n |
| "IC para σ²" | Chi-cuadrado (asimétrico) |
| "¿Rechazar H₀?" | p-value < α |
| "Cuántas obs para ME ≤ e" | n ≥ (z_{α/2}·σ/e)² |
| "Cuántas obs para potencia 80%" | n ≈ 7.85·σ²/δ² (nivel 5%) |
| "m tests simultáneos" | Bonferroni: α/m cada uno |

---

> **Síntesis:** El IC y el test de hipótesis son duales: H₀ se rechaza al nivel α ↔ θ₀ no está en el IC al (1-α)%. El pivote es la clave para construir ambos. El p-value es una medida de evidencia, no de probabilidad de H₀. El balance errores tipo I / tipo II se controla aumentando n.

---

*Retrieval: cierra y responde: (1) IC del 99% para μ: n=36, X̄=100, σ=15; (2) estadístico t y p-value para H₀:μ=5, n=25, X̄=6, S=4; (3) n para ME=0.1 con σ=1 al 95%; (4) χ² crítico para bondad de ajuste con k=5 categorías, nivel 5%.*
