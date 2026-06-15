# Cálculo y álgebra lineal para finanzas cuantitativas

## Series de Taylor esenciales

| Función | Expansión alrededor de 0 | Radio de convergencia |
|---------|--------------------------|----------------------|
| e^x | 1 + x + x²/2! + x³/3! + … | ∞ |
| sin(x) | x − x³/6 + x⁵/120 − … | ∞ |
| cos(x) | 1 − x²/2 + x⁴/24 − … | ∞ |
| ln(1+x) | x − x²/2 + x³/3 − … | \|x\|<1 |
| (1+x)^α | 1 + αx + α(α−1)x²/2 + … | \|x\|<1 |

Para e^{0.1}: 1+0.1+0.005+0.000167 ≈ 1.10517 (error ≈ 4×10^{-6}).

---

## Taylor aplicado a opciones — Greeks como derivadas

C(S+ΔS) ≈ C(S) + **Δ**·ΔS + ½**Γ**·(ΔS)²

donde Δ = ∂C/∂S (delta) y Γ = ∂²C/∂S² (gamma).

**P&L de un portafolio delta-neutral** (long call, short Δ acciones):

ΔP&L ≈ **½Γ·(ΔS)²** + Θ·dt

- Γ > 0 (long gamma): gana con movimientos grandes (convexo). Costo: Θ < 0.
- Long gamma pierde si vol_realizada < vol_implícita (el tiempo corroe más de lo que se gana con la gamma).

---

## Límites importantes

| Límite | Resultado | Método |
|--------|-----------|--------|
| lim sin(x)/x, x→0 | 1 | Taylor: sin(x)≈x |
| lim (e^x−1−x)/x², x→0 | 1/2 | Taylor: e^x−1−x≈x²/2 |
| lim x·e^{-x}, x→∞ | 0 | Exponencial domina |
| lim (1+x/n)^n, n→∞ | e^x | Definición de e |

L'Hôpital para 0/0 o ∞/∞: lim f(x)/g(x) = lim f'(x)/g'(x). Pero Taylor es más rápido cuando los primeros términos son evidentes.

---

## Integración por partes

**∫u dv = uv − ∫v du**

Mnemónico LIATE para elegir u: Logarítmica > Inversa > Algebraica > Trig > Exponencial.

| Integral | u | dv | Resultado |
|---------|---|-----|-----------|
| ∫x·e^x dx | x | e^x dx | (x−1)e^x + C |
| ∫ln(x) dx | ln(x) | dx | x·ln(x) − x + C |
| ∫x²·e^x dx | x² | e^x dx | (x²−2x+2)e^x + C |

---

## Integral gaussiana

**∫_{-∞}^∞ e^{-x²} dx = √π**

Demostración (truco 2D):

I² = ∫∫e^{-(x²+y²)}dxdy = ∫₀^{2π}∫₀^∞ e^{-r²}·r dr dθ = 2π·[−e^{-r²}/2]₀^∞ = π

∴ I = **√π**. Consecuencia: ∫_{-∞}^∞ e^{-x²/2}dx = **√(2π)** (normalización de N(0,1)).

---

## Función Gamma y factoriales

**Γ(n+1) = n!** para n entero no negativo.

Γ(n+1) = n·Γ(n) (relación de recurrencia).
Γ(1/2) = √π.

Aparece en: distribución chi-cuadrado χ²(ν) = Gamma(ν/2, 1/2), t-Student, Beta.

---

## Álgebra lineal — relaciones de valores propios

Para A n×n con valores propios λ₁,…,λₙ:

- **det(A) = ∏ λᵢ**
- **tr(A) = Σ λᵢ**
- **tr(AB) = tr(BA)** (permutación cíclica)
- A singular ↔ algún λᵢ = 0

Para A simétrica: todos los valores propios son reales; los vectores propios son ortogonales.

---

## Matrices positivas definidas

A es **positiva definida (SPD)** si:
- xᵀAx > 0 para todo x ≠ 0
- Equivalente: todos los valores propios > 0
- Equivalente: todos los menores principales > 0 (criterio de Sylvester)

Toda **matriz de covarianza** Σ = E[(X−μ)(X−μ)ᵀ] es **semidefinida positiva** (SDP):
xᵀΣx = E[(xᵀ(X−μ))²] ≥ 0.

SPD si no hay multicolinealidad perfecta (ninguna variable es combinación lineal de las otras).

---

## Descomposición espectral (PCA)

Para A simétrica: A = PΛPᵀ (P ortogonal, Λ diagonal con valores propios).

**PCA** = descomposición espectral de la matriz de covarianza Σ:
- Componentes principales = vectores propios de Σ
- Varianzas explicadas = valores propios λᵢ
- Fracción explicada por PC_k = λₖ/Σλᵢ

Ejemplo: curva de tasas de interés — las primeras 3 PCs (nivel, pendiente, curvatura) explican >95% del movimiento.

---

## Newton-Raphson

Para resolver f(x*) = 0:

**xₙ₊₁ = xₙ − f(xₙ)/f'(xₙ)**

Convergencia cuadrática: el número de dígitos correctos se **duplica** en cada iteración.

Para f(x) = x²−2, f'(x) = 2x (encontrar √2):

| n | xₙ |
|---|-----|
| 0 | 1.5 |
| 1 | 1.41667 |
| 2 | 1.41422 |
| 3 | 1.41421356… |

---

## Función generatriz de momentos (mgf)

M_X(t) = E[e^{tX}]

**E[X^n] = M_X^{(n)}(0)** (n-ésima derivada evaluada en 0).

Para sumas independientes: **M_{X+Y}(t) = M_X(t)·M_Y(t)**.

| Distribución | M_X(t) | E[X] | Var[X] |
|-------------|---------|------|--------|
| N(μ,σ²) | e^{μt+σ²t²/2} | μ | σ² |
| N(0,1) | e^{t²/2} | 0 | 1 |
| Exp(λ) | λ/(λ−t), t<λ | 1/λ | 1/λ² |

**De N(0,1):** M(t)=e^{t²/2} → E[e^X]=M(1)=e^{1/2} para X~N(0,1) → generalmente E[e^X]=e^{μ+σ²/2}.

---

## Regla de la cadena y diferenciación implícita

Regla de la cadena: d/dx f(g(x)) = f'(g(x))·g'(x).

Diferenciación implícita: si F(x,y)=0, entonces dy/dx = −(∂F/∂x)/(∂F/∂y).

**Optimización con restricciones — Lagrange:**

min f(x) sujeto a g(x)=0 → ∇f = λ∇g (CPO).

Markowitz: min ½xᵀΣx sujeto a 1ᵀx=1, μᵀx=r. CPO: Σx = λμ + γ1.

---

## Función característica

φ_X(t) = E[e^{itX}] (t ∈ ℝ, i imaginaria).

Siempre existe (a diferencia de la mgf). Identifica unívocamente la distribución.

Para N(0,1): φ(t) = e^{-t²/2}.

Usos: demostrar el TCL; valorar opciones cuando la función característica es conocida pero la densidad no (método de Carr-Madan).

---

## Métodos numéricos — error de integración

| Método | Error | Complejidad |
|--------|-------|-------------|
| Trapezoidal | O(h²) | n+1 evaluaciones |
| Simpson | O(h⁴) | n+1 evaluaciones (n par) |
| Gauss-Legendre (n puntos) | exacto para poly ≤2n−1 | n evaluaciones |
| Monte Carlo | O(1/√N) | N muestras aleatorias |

Monte Carlo: error independiente de la dimensión — ventaja decisiva en integrales de alta dimensión (≥4D).

---

## Mini-ejemplo trabajado: Taylor convierte una opción en Δ y Γ

¿Cómo cambia el precio de una opción C(S) ante un movimiento ΔS del subyacente? Expande en Taylor alrededor de S:

> C(S+ΔS) ≈ C(S) + Δ·ΔS + ½Γ·(ΔS)²

donde Δ=∂C/∂S y Γ=∂²C/∂S². La **primera derivada** (delta) es la sensibilidad lineal; la **segunda** (gamma) es la curvatura. Un portafolio delta-neutral (long call, short Δ acciones) borra el término lineal y deja:

> ΔP&L ≈ ½Γ·(ΔS)² + Θ·dt

Con Γ>0 (long gamma) ganas con movimientos grandes en cualquier dirección, pero pagas Θ<0 (el tiempo corroe). Toda la "magia" de los Greeks es una serie de Taylor truncada en el segundo término.

**Predicción antes de seguir:** ¿reconoces Δ y Γ de algún otro instrumento? Respuesta: son **exactamente** la duración y la convexidad de un bono — primera y segunda derivada del precio frente a su factor de riesgo. Delta↔duración, gamma↔convexidad, theta↔carry. Una vez ves "Taylor de primer y segundo orden", el bono y la opción son el mismo objeto.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** sensibilidad de un precio a un factor → Taylor: primer orden (Δ/duración) + segundo orden (Γ/convexidad).
- **Contraejemplo (PCA y escala):** la descomposición espectral de Σ supone features comparables; sin estandarizar, la variable de unidades grandes domina las componentes principales. PCA "sin escalar" engaña.
- **Caso borde (covarianza singular):** si una variable es combinación lineal de otras (multicolinealidad perfecta), Σ tiene un valor propio 0 (semidefinida, no definida) y no es invertible. El borde conecta álgebra lineal con colinealidad.

## Errores típicos

- **Conceptual:** confundir media y mediana de una lognormal: E[e^X]=e^{μ+σ²/2} > e^μ por la convexidad (Jensen).
- **Técnico:** usar L'Hôpital donde Taylor es inmediato (lim(e^x−1−x)/x²=½ sale de e^x−1−x≈x²/2).
- **De supuestos:** aplicar Monte Carlo esperando convergencia rápida; el error cae como 1/√N (su ventaja es la dimensión, no la velocidad).

## Transferencia isomorfa

- **Taylor → Δ, Γ ↔ duración y convexidad:** primera y segunda derivada del precio son los mismos Greeks de un bono (conecta con [[arena-q7]]).
- **Descomposición espectral (PCA) ↔ matriz de covarianza PSD:** las componentes son vectores propios de Σ, semidefinida positiva porque xᵀΣx=E[(xᵀ(X−μ))²]≥0 (conecta con [[arena-q9]] y [[arena-q6]]).
- **mgf gaussiana e^{μt+σ²t²/2} ↔ valoración lognormal:** evaluarla en t=1 da E[e^X], el puente a la prima de Jensen (conecta con [[arena-q7]]).
- **Newton-Raphson ↔ optimización del MLE:** resolver f'(θ)=0 con convergencia cuadrática es cómo se ajusta una logística o se maximiza una log-verosimilitud (conecta con [[arena-dg2]]).
- **Monte Carlo O(1/√N) ↔ error estándar:** la lentitud √N es la misma del SE de la media y del bootstrap (conecta con [[arena-pst2]] y [[arena-fc2]]).

Moraleja de la arista: *casi todo es una derivada: delta/gamma son duración/convexidad, PCA son los ejes de la covarianza, y el segundo orden de Taylor es donde vive la convexidad.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Aproximar e^x cerca de 0" | 1+x+x²/2+x³/6 |
| "P&L de portafolio con opción" | ½Γ·(ΔS)² + Θ·dt |
| "Lim sin(x)/x" | Taylor: ≡1 |
| "∫x·e^x dx" | Partes: (x−1)e^x + C |
| "∫e^{-x²}dx completo" | √π (truco 2D polar) |
| "det y tr de A" | ∏λᵢ y Σλᵢ |
| "tr(AB) = tr(BA)?" | Sí; permutación cíclica |
| "Raíz de f(x)=0" | Newton-Raphson: convergencia cuadrática |
| "E[e^X] para X~N(μ,σ²)" | e^{μ+σ²/2} (desde mgf) |
| "PCA de Σ" | Vectores propios de Σ; varianza = valor propio |

---

> **Síntesis:** El cálculo y álgebra lineal son el lenguaje matemático de las finanzas cuantitativas. Taylor traduce no-linealidades en Δ y Γ; el lema de Itô extiende Taylor al ruido estocástico; la descomposición espectral (PCA) reduce la dimensión; la mgf codifica todos los momentos en una función. La integral gaussiana (√π) conecta el análisis real con la distribución normal — la base de todo.

---

*Retrieval: sin mirar: (1) taylor de e^x hasta el 3er término; (2) ∫₀^1 x·e^x dx; (3) tr(A) y det(A) para A=[[2,1],[1,3]]; (4) x₁ de Newton-Raphson aplicado a x²−3=0, x₀=2.*
