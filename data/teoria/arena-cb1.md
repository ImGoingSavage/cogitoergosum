# Suficiencia, estadísticos completos y el principio de verosimilitud

## Estadístico suficiente

T(X) es **suficiente** para θ si la distribución condicional de X dado T(X)=t no depende de θ.

Intuición: T captura toda la información que los datos contienen sobre θ; el resto es "ruido".

**Criterio de factorización (Fisher-Neyman):**

f(x|θ) = g(T(x), θ) · h(x)

T es suficiente ↔ la verosimilitud L(θ|x) solo depende de x a través de T(x).

| Distribución | Estadístico suficiente |
|-------------|----------------------|
| Bernoulli(p) | T = ΣXᵢ |
| Normal N(μ,σ²) — ambos desconocidos | T = (ΣXᵢ, ΣXᵢ²) |
| Poisson(λ) | T = ΣXᵢ |
| Uniform[0,θ] | T = X₍ₙ₎ = máx Xᵢ |
| Gamma(α,β) — α conocida | T = ΣXᵢ |
| Exponencial(θ) desplazada f(x|θ)=e^{iθ−x} | T = mín(Xᵢ/i) |

---

## Familias exponenciales

Para f(x|θ) = h(x)c(θ) exp(Σ wₖ(θ)tₖ(x)), los estadísticos suficientes son T = (Σtₖ(X₁),…,Σtₖ(Xₙ)).

Ejemplos: toda la tabla anterior pertenece a la familia exponencial (salvo la uniforme).

---

## Estadístico minimal suficiente

T es **minimal suficiente** si es función de todo estadístico suficiente — es la compresión máxima sin pérdida de información.

**Criterio de Lehmann-Scheffé:** T(x) es minimal suficiente si

L(θ|x)/L(θ|y) no depende de θ ↔ T(x) = T(y).

Ejemplos de estadísticos minimales:

| Distribución | Estadístico minimal suficiente |
|-------------|-------------------------------|
| Normal N(μ,σ²) | (X̄, S²) |
| Cauchy(θ,1) | Estadísticos de orden (X₍₁₎,…,X₍ₙ₎) |
| Uniforme U(θ,θ+1) | (X₍₁₎, X₍ₙ₎) |
| Logística loc. μ | Estadísticos de orden |

---

## Completitud

T es **completo** para una familia de distribuciones si:

E[g(T)] = 0 para todo θ ⟹ g(T) = 0 a.s. para todo θ.

Regla práctica: las familias exponenciales de rango completo tienen estadístico suficiente completo.

Ejemplo: X₁,…,Xₙ i.i.d. N(μ,σ²) con ambos parámetros desconocidos: T=(ΣXᵢ, ΣXᵢ²) es suficiente y **completo**.

Contraejemplo: familia n(θ, aθ²) con a conocido: (ΣXᵢ, ΣXᵢ²) es suficiente pero **no completo** (el espacio paramétrico no contiene un abierto en ℝ²).

---

## Estadístico ancilario

V(X) es **ancilario** para θ si su distribución no depende de θ.

Ejemplos:
- X₁ − X₂ para una familia de localización
- S² en N(μ,σ²) cuando se estima μ con σ² desconocida (la distribución de S² no depende de μ)
- (Xᵢ − X̄)/S en cualquier familia de localización-escala

---

## Teorema de Basu

Si T es **completo y suficiente** y V es **ancilario**, entonces T ⊥ V.

Aplicaciones clásicas:
- X̄ ⊥ S² en N(μ,σ²) (X̄ es completo suficiente para μ con σ² conocida; S² es ancilario para μ)
- X₍₁₎ ⊥ Sₙ en la exponencial desplazada (donde Sₙ = estadísticos de escala)

---

## Principio de suficiencia y de verosimilitud

**Principio de suficiencia formal:** Si T(x)=T(y), entonces cualquier inferencia sobre θ debe ser la misma para x que para y.

**Principio de verosimilitud (Birnbaum):** Toda la información de x sobre θ está contenida en L(θ|x) ∝ f(x|θ).

Consecuencia: la función de verosimilitud es uno-a-uno con el estadístico minimal suficiente en familias regulares.

---

## Mini-ejemplo trabajado: por qué ΣXᵢ basta (factorización)

n monedas Bernoulli(p), datos x=(1,0,1,1,0). La verosimilitud es:

> L(p|x) = ∏ p^{xᵢ}(1−p)^{1−xᵢ} = p^{Σxᵢ}(1−p)^{n−Σxᵢ}

Toda la dependencia de x entra **solo a través de Σxᵢ = 3**: dos muestras distintas con el mismo total (p. ej. (1,1,1,0,0)) dan exactamente la misma verosimilitud. Por el criterio de factorización f(x|p)=g(T,p)·h(x) con g=p^T(1−p)^{n−T} y h(x)=1, T=ΣXᵢ es **suficiente**. El orden y las posiciones de los 1 son "ruido" irrelevante para p.

**Predicción antes de seguir:** ¿el suficiente es siempre una suma/promedio? Respuesta: **no**. Para Uniforme[0,θ] el suficiente es el **máximo** X₍ₙ₎, no la suma; para la Cauchy ningún resumen comprime y hay que retener *todos* los estadísticos de orden. La forma del suficiente la dicta la familia, y fuera de la exponencial puede no haber compresión. (Caja negra: que la familia exponencial sea la única con suficiente de dimensión fija —Pitman-Koopman-Darmois— asúmelo por ahora; lo que importa es la intuición "comprime sin perder θ".)

## Prototipo, contraejemplo y caso borde

- **Prototipo:** familia exponencial → T=(Σt₁(Xᵢ),…) suficiente y, si es de rango completo, **completo** → habilita Lehmann-Scheffé.
- **Contraejemplo (suficiente pero no completo):** N(θ, aθ²) con a fijo: (ΣXᵢ, ΣXᵢ²) es suficiente pero NO completo porque el espacio paramétrico es una curva, no un abierto. Suficiente no garantiza UMVUE único.
- **Caso borde (ancilario):** S²/σ² no informa de μ pero su distribución es libre de μ → es **ancilario**; por Basu, X̄ ⊥ S² en la normal. El borde muestra que un estadístico puede ignorar por completo el parámetro.

## Errores típicos

- **Conceptual:** confundir suficiente (captura θ) con completo (unicidad); se necesita completo *además* de suficiente para Lehmann-Scheffé.
- **Técnico:** olvidar el factor h(x) al factorizar, o intentar derivar el suficiente cuando el soporte depende de θ (Uniforme).
- **De supuestos:** aplicar Basu sin verificar que T sea completo *y* suficiente y V ancilario.

## Transferencia isomorfa

- **Estadístico suficiente ↔ estado mínimo / compresión de features:** T(X) resume los datos sin perder información sobre θ, igual que un estado markoviano resume la historia o un embedding resume una entrada (conecta con [[arena-b4]] y [[arena-dg1]]).
- **Ancilario ↔ pivote:** un estadístico cuya distribución no depende de θ es la materia prima de un pivote para construir intervalos de confianza (conecta con [[arena-cb4]]).
- **Familia exponencial ↔ GLM y conjugación:** la forma h(x)exp(η·T−A) es la misma que da suficientes compactos, priors conjugados y los modelos lineales generalizados (conecta con [[arena-b4]]).
- **Principio de verosimilitud ↔ "solo la verosimilitud importa":** dos datasets con la misma L dan la misma inferencia — el fundamento de comparar modelos por razón de verosimilitudes (conecta con [[arena-cb3]]).

Moraleja de la arista: *el suficiente comprime los datos a lo que importa de θ; la completitud lo vuelve único; y un ancilario —ciego a θ— es la semilla de un pivote.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿Captura toda la info de θ?" | Estadístico suficiente (factorización) |
| "¿La densidad es de la familia exponencial?" | T = (Σt₁(Xᵢ),…,Σtₖ(Xᵢ)) es suficiente |
| "¿Compresión máxima sin pérdida?" | Minimal suficiente (criterio de cociente) |
| "E[g(T)]=0 para todo θ implica g=0" | Completo — habilita Lehmann-Scheffé |
| "Independencia entre estadísticos" | Basu: uno completo suficiente, otro ancilario |
| "La distribución de V no depende de θ" | V es ancilario |

---

> **Síntesis (Casella & Berger, Ch 6):** La suficiencia comprime; la completitud garantiza unicidad; Basu conecta completitud con independencia. La familia exponencial es el laboratorio donde todo esto funciona limpiamente. Para familias fuera de la exponencial (Cauchy, uniforme en intervalo desconocido) los estadísticos de orden son el refugio.

---

*Retrieval: cierra y responde: (1) ¿Cuál es el estadístico suficiente de una Poisson(λ) con n observaciones? (2) ¿Qué condición hace que T=(ΣXᵢ,ΣXᵢ²) NO sea completo en N(θ,aθ²)? (3) Enuncia el teorema de Basu y da un ejemplo. (4) ¿Por qué los estadísticos de orden son minimales suficientes para la Cauchy?*
