# Probabilidad geométrica

## La aguja de Buffon

Aguja de longitud L, líneas paralelas separadas d (L ≤ d):

**P(aguja cruza una línea) = 2L / (πd)**

Para L=d: P = 2/π ≈ 63.7%.

Dem.: Sea x = distancia del centro al línea más cercana (Uniform[0, d/2]) y θ = ángulo (Uniform[0, π/2]). El cruce ocurre cuando x < (L/2)cosθ.

P = (2/d)·∫₀^{π/2} (L/2)cosθ · (2/π) dθ = **2L/(πd)**

Aplicación: estimar π experimentalmente (π ≈ 2L·n / (d·c), donde c = número de cruces en n lanzamientos).

---

## Par uniforme en un cuadrado

X,Y i.i.d. Uniform[0,1]. P(|X−Y| < r) para r ∈ (0,1):

**P(|X−Y| < r) = 2r − r²**

Dem.: área del cuadrado fuera de la banda de ancho r alrededor de la diagonal:
P = 1 − 2·(1−r)²/2 = 1 − (1−r)² = **2r − r²**

Para r=0.3: P = 0.51.

---

## La paradoja de Bertrand

¿Cuál es P(una cuerda aleatoria de un círculo de radio R es más larga que el lado del triángulo equilátero inscrito, √3·R)?

Depende de qué se entiende por "aleatoria":

| Método de elección | P(cuerda > √3·R) |
|--------------------|-----------------|
| Dos puntos aleatorios en la circunferencia | **1/3** |
| Punto medio aleatorio en el disco | **1/4** |
| Distancia al centro aleatoria (0 a R) | **1/2** |

Los tres son correctos dado su modelo; la paradoja ilustra que "uniforme" no está definida sin especificar la geometría del espacio de muestreo.

---

## Rango de 3 uniformes

X₁,X₂,X₃ i.i.d. Uniform[0,1]. Rango = X₍₃₎ − X₍₁₎.

**E[rango] = E[X₍₃₎] − E[X₍₁₎] = 3/4 − 1/4 = 1/2**

En general, para n variables: E[X₍ₙ₎ − X₍₁₎] = (n−1)/(n+1).

P(rango < r) = r²·(3 − 2r) para r ∈ [0,1].

---

## Monte Carlo para π

Puntos uniformes en [−1,1]² (cuadrado de lado 2, área 4). Círculo inscrito de radio 1 (área π).

**π ≈ 4 · (número de puntos dentro del círculo) / (número total de puntos)**

P(punto cae en círculo) = π/4. Error estándar: σ/√n con σ²=π/4·(1−π/4).

Con n=10,000 puntos: error típico ≈ 0.016; requiere n≈10^6 para 3 decimales correctos.

Monte Carlo es lento (error ∝ 1/√n) pero escala bien a dimensiones altas.

---

## El palo roto (broken stick)

Se rompe un palo en 3 piezas, rotura uniforme. P(formar triángulo):

**P = 1/4**

Dem.: sean los puntos de corte U₁ < U₂ en [0,1]. Las 3 piezas forman triángulo ↔ cada pieza < 1/2. El área de la región {U₁<1/2, U₂>1/2, U₂−U₁<1/2} dentro del triángulo del espacio muestral (0<U₁<U₂<1) es 1/4 del total.

Analogía: los 3 segmentos cumplen desigualdad triangular ↔ punto cae en triángulo central del triángulo de Sierpinski.

---

## El encuentro del autobús

Dos personas llegan uniformemente en [0,60] min. Cada una espera 15 min.

P(se encuentran) = P(|X−Y| ≤ 15):

Usando la fórmula P(|X−Y| < r) para X,Y ∈ [0,T]: P = 1 − (1−r/T)².

**P = 1 − (45/60)² = 1 − 9/16 = 7/16 ≈ 43.75%**

---

## Distancia esperada al centro

Punto uniformemente distribuido en disco de radio R:

**E[distancia al centro] = 2R/3**

Dem.: P(d ≤ r) = πr²/(πR²) = r²/R². Densidad de d: f(r) = 2r/R² para r ∈ [0,R].

E[d] = ∫₀^R r·(2r/R²)dr = [2r³/(3R²)]₀^R = **2R/3**.

---

## Ley del arcoseno

Para movimiento browniano estándar B_t en [0,1]:

Sea τ = último tiempo en [0,1] que B_t = 0 (o, equivalentemente, fracción del tiempo que B_t > 0).

**P(τ ≤ x) = (2/π)·arcsin(√x)**

Consecuencia: τ tiene distribución Beta(1/2, 1/2) con moda en 0 y 1.

Contraintuitivo: el proceso browniano pasa la mitad del tiempo con el mismo signo con mayor probabilidad que alternando frecuentemente. El tiempo más probable es que el BM esté casi siempre > 0 o casi siempre < 0, no 50/50.

---

## Cobertura circular

n arcos de longitud (2π/n) colocados uniformemente en una circunferencia de longitud 2π:

**P(arcos cubren toda la circunferencia) = n/2^{n-1}**

Para n=3: P = 3/4. Para n=4: P = 4/8 = 1/2. Para n=5: P = 5/16.

---

## Distancia Manhattan esperada

Dos puntos uniformes en [0,1]²:

**E[|X₁−X₂| + |Y₁−Y₂|] = 2/3**

Por linealidad: E[|X₁−X₂|] + E[|Y₁−Y₂|] = 1/3 + 1/3 = **2/3**.

E[|U−V|] = 1/3 para U,V i.i.d. Uniform[0,1] (dem.: ∫∫|u−v|du dv = 1/3).

---

## Mini-ejemplo trabajado: Bertrand y por qué "aleatorio" no basta

¿Probabilidad de que una cuerda al azar de un círculo sea más larga que el lado del triángulo inscrito (√3·R)? La respuesta depende de **cómo** eliges la cuerda:

- Dos puntos al azar en la circunferencia → **1/3**.
- Punto medio al azar en el disco → **1/4**.
- Distancia al centro al azar en [0,R] → **1/2**.

Los tres cálculos son correctos; lo que cambia es qué objeto se distribuye uniformemente (ángulo, área, radio). "Cuerda aleatoria" no define una probabilidad hasta que fijas el espacio de muestreo.

**Predicción antes de seguir:** ¿es la paradoja de Bertrand un error de cálculo o de planteamiento? Respuesta: de **planteamiento** — la pregunta está mal especificada. Es el mismo defecto que la paradoja de los dos sobres (un prior impropio mal definido): sin un modelo probabilístico explícito, el cálculo condicional es inválido aunque el álgebra sea correcta. "Uniforme respecto a qué" es siempre la primera pregunta.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** dos uniformes → punto en el cuadrado; "qué fracción cumple la condición" es un área (Romeo-Julieta 7/16, palo roto 1/4).
- **Contraejemplo (Bertrand):** "elige al azar" sin especificar la geometría no tiene respuesta única.
- **Caso borde (ley del arcoseno):** el browniano NO alterna de signo equitativamente; lo más probable es que pase casi todo el tiempo de un lado (Beta(½,½), moda en 0 y 1). El borde desafía la intuición de "se reparte 50/50".

## Errores típicos

- **Conceptual:** suponer "uniforme en el radio" en problemas de disco; la densidad del radio es 2r/R² (más área lejos del centro).
- **Técnico:** integrar a ciegas en vez de dibujar la región y restar áreas/triángulos.
- **De supuestos:** confiar en Monte Carlo para 3 decimales con pocas muestras; el error cae como 1/√n (n≈10⁶ para 3 decimales).

## Transferencia isomorfa

- **Probabilidad como área ↔ integración Monte Carlo:** estimar π con 4·(hits/n) es estimar una integral como fracción de puntos en una región (conecta con [[arena-q10]]).
- **Error Monte Carlo 1/√n ↔ error estándar de la media:** la lentitud de Monte Carlo es la misma √n del SE y del bootstrap (conecta con [[arena-pst2]]).
- **Ley del arcoseno ↔ movimiento browniano:** la fracción de tiempo positivo de un BM es Beta(½,½), un resultado de procesos estocásticos (conecta con [[arena-q11]]).
- **Bertrand (modelo mal definido) ↔ prior impropio:** ambos enseñan que sin un modelo probabilístico explícito el cálculo es vacío (conecta con [[arena-fc3]]).

Moraleja de la arista: *en probabilidad geométrica, dibuja y mide áreas; pero antes pregunta "¿uniforme respecto a qué?" — Bertrand cae si no lo haces.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Aguja sobre líneas paralelas" | Buffon: 2L/(πd) |
| "P(dos uniformes están cerca)" | 2r − r² para |X−Y| < r en [0,1] |
| "Cuerda aleatoria y triángulo" | Bertrand: depende del modelo |
| "Monte Carlo para estimar π" | 4 × (hits en círculo) / n |
| "3 piezas forman triángulo" | P = 1/4 |
| "Dos personas llegan en [0,T]" | P(se encuentran) = 1 − ((T−d)/T)² |
| "E[distancia al centro en disco]" | 2R/3 |
| "Fracción del tiempo BM > 0" | Ley del arcoseno: Beta(1/2, 1/2) |
| "E[|U−V|] para uniformes" | 1/3 |

---

> **Síntesis:** La probabilidad geométrica conecta el azar con el área/volumen. Los resultados clave son: Buffon (2L/πd), par uniforme (2r−r²), palo roto (1/4), Bertrand (la pregunta mal planteada), Monte Carlo (4·hits/n). La ley del arcoseno es la más contraintuitiva: el movimiento browniano no "alterna" — tiende a quedarse en el mismo semiplano.

---

*Retrieval: cierra y responde: (1) P(aguja de longitud 1 cruza líneas separadas 2); (2) P(|X−Y|<0.5) para X,Y~Unif[0,1]; (3) P(palo roto forma triángulo); (4) E[distancia Manhattan en [0,1]²].*
