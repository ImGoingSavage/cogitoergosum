# Coincidencias, urnas y emparejamiento

## El principio del palomar aplicado a pares

Para garantizar un par con k colores: necesitas **k + 1** objetos (peor caso: uno de cada color).

Ejemplo clásico — calcetines en la oscuridad (4 rojos + 6 azules):
- Garantizar algún par: sacar **3** (2 colores → 3 para garantizar coincidencia)
- Garantizar un par rojo: sacar **8** (6 azules primero + 2 rojos)

Regla: para garantizar r piezas del mismo color específico, saca todos los otros + r.

---

## Puntos fijos de permutación aleatoria

**E[puntos fijos] = 1** para cualquier n (linealidad de E[]).

Dem.: E[X] = Σ E[Xᵢ] = n × (1/n) = 1.

**P(ningún punto fijo) = D(n)/n! → 1/e ≈ 36.79%**

| n | D(n) | D(n)/n! |
|---|------|---------|
| 2 | 1 | 0.500 |
| 3 | 2 | 0.333 |
| 4 | 9 | 0.375 |
| 5 | 44 | 0.367 |
| ∞ | — | 1/e |

**Número de coincidencias ≈ Poisson(1)**: P(exactamente k coincidencias) ≈ e^{-1}/k!.

---

## El problema de la boleta (Ballot problem)

A recibe **a** votos, B recibe **b** votos (a > b). Conteo aleatorio.

**P(A siempre estrictamente adelante) = (a − b) / (a + b)**

Dem. por reflexión: las "malas" trayectorias (donde A no siempre va adelante) tienen biyección con trayectorias que empiezan con B → contar con combinatoria.

Para a=7, b=3: P = 4/10 = **2/5**.

---

## Valores récord

En secuencia de n valores i.i.d. de distribución continua:

**P(el k-ésimo es récord) = 1/k** (por simetría: cualquiera de los primeros k es el máximo con igual probabilidad)

**E[récords en n valores] = H_n = 1 + 1/2 + 1/3 + … + 1/n**

Para n=10: H₁₀ ≈ 2.93; para n=100: H₁₀₀ ≈ 5.19.

Los récords son eventos *independientes* (aunque los valores no lo sean).

---

## Distribución hipergeométrica

Muestreo sin reemplazo de N objetos (K del tipo A, N−K del tipo B), muestra de tamaño n:

**P(X = k) = C(K,k) · C(N−K, n−k) / C(N,n)**

**E[X] = nK/N** (igual que binomial)

**Var[X] = n · (K/N) · (1−K/N) · (N−n)/(N−1)** ← factor de corrección finita

La hipergeométrica → binomial cuando N → ∞.

---

## Distribución binomial negativa

Número de intentos hasta el **r-ésimo éxito** (p = probabilidad de éxito):

**P(X = n) = C(n−1, r−1) · p^r · (1−p)^{n−r}**

**E[X] = r/p ;  Var[X] = r(1−p)/p²**

Para r=3, p=0.3: E[X] = 10 intentos.

---

## La urna de Pólya

Start: 1 roja, 1 azul. Cada paso: saca una, regresa + 1 nueva del mismo color.

**Distribución de rojas en n adiciones: Uniforme en {0, 1, …, n}**

Cada resultado es igualmente probable → P(k rojas en n pasos) = 1/(n+1).

E[fracción de rojas] = 1/2; Var[fracción] → 1/12 para n grande.

Modelo de refuerzo positivo: el rico se hace más rico, pero la distribución final es uniforme.

---

## El problema del secretario (optimal stopping)

n candidatos en orden aleatorio; contratar o rechazar inmediatamente; quieres el mejor.

Estrategia óptima: **rechaza los primeros ⌊n/e⌋ candidatos, luego contrata el siguiente mejor**.

**P(contratar al mejor) → 1/e ≈ 36.8%**

Para n=100: rechaza los primeros 37, luego actúa.

---

## El problema de ocupación

n bolas lanzadas en n cajas uniformemente al azar:

**E[cajas vacías] = n · (1 − 1/n)^n → n/e ≈ 0.368n**

~37% de las cajas quedan vacías. Modela hashing con colisiones: después de n inserciones en tabla de n slots, ~37% de slots están vacíos.

---

## Mini-ejemplo trabajado: el secretario y el 1/e que reaparece

100 candidatos en orden aleatorio; decides en el acto contratar o rechazar; quieres al mejor. La estrategia óptima: **rechaza los primeros ⌊n/e⌋ ≈ 37**, memoriza el mejor visto, y contrata al primero que lo supere. La probabilidad de quedarte con el verdadero mejor tiende a **1/e ≈ 37%** — sorprendentemente alta para "una sola oportunidad".

La estructura: una fase de **exploración** (mira sin comprometerte para calibrar) y una de **explotación** (actúa con el umbral aprendido). El punto n/e equilibra "explorar de más y dejar pasar al mejor" contra "explotar de más sin información".

**Predicción antes de seguir:** ¿reconoces ese 37%? Es el mismo 1/e de "P(ninguna persona recupera su sombrero)" y de "fracción esperada de cajas vacías" (n/e). Aparece siempre que cuentas eventos raros con tasa ≈1: P(0 éxitos) en una Poisson(1) es e⁻¹. El 1/e es la firma de "esperaba uno, no salió ninguno".

## Prototipo, contraejemplo y caso borde

- **Prototipo (palomar):** "garantizar un par de k colores" → k+1 objetos; para r de un color específico, todos los otros + r.
- **Contraejemplo (puntos fijos no se acumulan):** E[puntos fijos]=1 para todo n, pero NO porque sean independientes (no lo son); la linealidad no lo exige. Creer que "más personas = más coincidencias esperadas" es el error.
- **Caso borde (urna de Pólya):** refuerzo positivo "el rico se hace más rico", y aun así la fracción final de rojas es **uniforme** en {0,…,n}. El borde rompe la intuición de que el refuerzo concentra.

## Errores típicos

- **Conceptual:** exigir independencia para sumar esperanzas de indicadores (puntos fijos, coincidencias).
- **Técnico:** olvidar el factor de corrección finita (N−n)/(N−1) en la varianza hipergeométrica.
- **De interpretación:** confundir "número de intentos hasta el r-ésimo éxito" (binomial negativa, E=r/p) con el número de éxitos en n intentos (binomial).

## Transferencia isomorfa

- **Problema de ocupación (n/e cajas vacías) ↔ colisiones de hash:** tras n inserciones en n slots, ~37% quedan vacíos y hay colisiones; es el mismo conteo que el cumpleaños (conecta con [[arena-sd2]] y [[arena-fc3]]).
- **Secretario (1/e) ↔ parada óptima:** explorar y luego fijar umbral es backward induction sobre "quedarse vs seguir" (conecta con [[arena-q8]]).
- **E[récords]=Hₙ ↔ coleccionista de cupones:** el número armónico cuenta récords y también el tiempo de coleccionar n tipos (conecta con [[arena-q6]]).
- **Puntos fijos por indicadores ↔ linealidad de la esperanza:** el sombrero es el ejemplo canónico de descomponer en indicadores sin pelear con la dependencia (conecta con [[arena-q1]] y [[arena-b1]]).

Moraleja de la arista: *el 1/e es la firma de "esperaba uno y salió ninguno"; aparece en sombreros, cajas vacías y en el secretario por la misma Poisson(1).*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Garantizar par de k colores" | Palomar: k+1 objetos |
| "E[puntos fijos de permutación]" | Siempre 1, por linealidad |
| "P(ningún punto fijo)" | D(n)/n! → 1/e |
| "A siempre adelante en conteo" | Ballot: (a−b)/(a+b) |
| "P(k-ésimo elemento es récord)" | 1/k |
| "E[récords en n elementos]" | H_n |
| "Muestreo sin reemplazo" | Hipergeométrica: E = nK/N |
| "k-ésimo éxito, p fija" | Binomial negativa: E = r/p |
| "Contratar al mejor, 1 oportunidad" | Secretario: rechaza n/e, luego el mejor |

---

> **Síntesis:** Los problemas de coincidencia y emparejamiento tienen dos resultados contraintuitivos clave: E[puntos fijos] = 1 siempre (linealidad); P(ningún punto fijo) ≈ 1/e ≈ 37% (convergencia rápida). El principio del palomar resuelve los problemas de garantía. El problema del secretario muestra que 1/e también aparece en parada óptima.

---

*Retrieval: cierra y responde: (1) E[puntos fijos de permutación de n=50]; (2) P(ningún punto fijo, n=6); (3) fórmula del ballot problem; (4) P(k-ésimo es récord en n i.i.d.).*
