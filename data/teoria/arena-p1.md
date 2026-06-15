# Acertijos matemáticos y razonamiento rápido

## Sumas telescópicas

1/(k(k+1)) = 1/k − 1/(k+1) → **suma telescopa**.

Σ_{k=1}^{n} 1/(k(k+1)) = 1 − 1/(n+1) = **n/(n+1)**

Para n=99: suma = 99/100. No hay que sumar 99 términos — el patrón colapsa en dos.

**Variante:** Σ 1/(k(k+2)) = ½(1/1 − 1/(n+2)); Σ 1/(k(k+1)(k+2)) también telescopa.

---

## Cálculo mental con identidades algebraicas

| Producto | Identidad | Ejemplo |
|---------|-----------|---------|
| (a−b)(a+b) | a²−b² | 97×103 = 100²−3² = 9991 |
| (a±b)² | a²±2ab+b² | 98² = (100−2)² = 9604 |
| (a−b)³ | a³−3a²b+3ab²−b³ | 99³ ≈ 100³−3×100² = 970 299 |

Regla práctica: elige a = múltiplo de 10 más cercano. El ajuste es siempre pequeño.

---

## Potencias grandes mod m

**Algoritmo en 3 pasos:**
1. Reduce la base: b mod m.
2. Encuentra el período: ciclo de (b mod m)^k mod m.
3. Reduce el exponente mod período.

Ejemplo — 4444^4444 mod 9:
- 4444 mod 9 = suma de dígitos = 16 → 7
- Ciclo de 7 mod 9: 7,4,1,7,4,1,… período = 3
- 4444 mod 3 = suma de dígitos de 4444 = 16 → 1
- Resultado: 7^1 mod 9 = **7**

Herramienta general: teorema de Euler — si mcd(b,m)=1: b^φ(m) ≡ 1 (mod m).

---

## Conteo de dígitos

Para contar apariciones del dígito d en {1,…,n}: cuenta por posición.

Ejemplo — dígito 1 en {1,…,100}:
- Unidades: 1,11,21,…,91 → 10 unos
- Decenas: 10,11,…,19 → 10 unos
- Centenas: 100 → 1 uno
- **Total: 21**

Cuidado: 11 contribuye a dos posiciones. Nunca cuentes por número — cuenta por posición.

---

## Serie de potencias y derivación

**Σ_{k=0}^∞ x^k = 1/(1−x)** para |x|<1.

Derivar término a término: **Σ_{k=1}^∞ k·x^{k−1} = 1/(1−x)²**.

Multiplicar por x: **Σ_{k=1}^∞ k·x^k = x/(1−x)²**.

Para x=1/2: Σ k·(1/2)^k = (1/2)/(1/2)² = **2**.

Esto aparece en esperanzas de distribuciones geométricas y en valoración de perpetuidades crecientes.

---

## Producto telescópico (1−1/k²)

∏_{k=2}^{n} (1−1/k²) = **(n+1)/(2n)**

Factoriza: 1−1/k² = (k−1)(k+1)/k². El doble telescopio anula casi todo.

Para n→∞: producto → **1/2**.

---

## Suma de dígitos de todos los enteros

Para sumar todos los dígitos de {1,…,100}:

- {1–9}: suma de dígitos = 1+…+9 = 45
- {10–99}: unidades (0-9 aparecen 9 veces cada uno) = 9×45 = 405; decenas (1-9 aparecen 10 veces) = 10×45 = 450; subtotal = 855
- {100}: 1+0+0 = 1
- **Total: 901**

---

## Cuadrados en un tablero n×n

Un cuadrado de lado k tiene (n−k+1)² posiciones.

Total = Σ_{k=1}^{n} (n−k+1)² = Σ_{j=1}^{n} j² = **n(n+1)(2n+1)/6**

Para n=8: 8×9×17/6 = **204**.

---

## Problema del cumpleaños

P(al menos 2 comparten cumpleaños en grupo de n) ≈ 1 − e^{−n(n−1)/730}.

Umbral para P > 50%: n(n−1) > 730·ln2 ≈ 506 → **n ≈ 23**.

Contraintuitivo: el número de **pares** crece como n²/2, no el tamaño del grupo.

---

## Pesaje de bolas con balanza

k pesadas permiten distinguir hasta **3^k** bolas (3 resultados por pesada).

Para 8 bolas: 3² = 9 > 8 → **2 pesadas bastan**.
Estrategia: divide 3-3-2. Si la primera pesada balancea, la diferente está entre las 2 restantes (1 pesada las distingue). Si se inclina, 1 pesada en el grupo de 3 sospechosos basta.

---

## Hormigas en triángulo — simetría y conteo

n hormigas en vértices de polígono regular; cada una elige CW o CCW con p=1/2.

P(ningún choque) = 2/2^n = 2^{1−n}.

Para triángulo (n=3): P = 2/8 = **1/4**.

Solo hay 2 "buenas" disposiciones de 2^n posibles (todas CW o todas CCW).

---

## Mini-ejemplo trabajado: telescopio que colapsa 99 términos en 2

Quieres Σ_{k=1}^{99} 1/(k(k+1)). En vez de sumar 99 fracciones, descompón cada término:

> 1/(k(k+1)) = 1/k − 1/(k+1)

Al sumar, cada −1/(k+1) cancela el +1/(k+1) del término siguiente:

> (1/1 − 1/2) + (1/2 − 1/3) + … + (1/99 − 1/100) = 1 − 1/100 = **99/100**

Solo sobreviven el primer y el último término. El "trabajo" es ver la **fracción parcial**, no sumar.

**Predicción antes de seguir:** ¿qué tienen en común el telescopio, contar cuadrados perfectos por paridad de divisores y los productos ∏(1−1/k²)? Respuesta: todos **colapsan una operación larga a sus extremos** al revelar una estructura que se cancela o se empareja. Es el mismo reflejo de "buscar la cantidad invariante que evita enumerar" — el corazón de los brainteasers cuantitativos.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** suma de la forma 1/(k(k+1)) o producto (1−1/k²) → fracciones parciales → telescopio.
- **Contraejemplo (contar por número, no por posición):** para "cuántos dígitos 1 en {1,…,100}", contar número por número se enreda; el 11 aporta a dos posiciones. Cuenta **por posición** (unidades, decenas…).
- **Caso borde (balanza ternaria):** k pesadas distinguen 3ᵏ bolas, no 2ᵏ — la balanza da tres resultados. Pensar en binario sobreestima las pesadas.

## Errores típicos

- **Conceptual:** intentar sumar/multiplicar a fuerza bruta cuando hay una identidad que colapsa (telescopio, diferencia de cuadrados).
- **Técnico:** en potencias mod m, no reducir el exponente módulo el **período** del ciclo de residuos (Euler).
- **De interpretación:** en el cumpleaños, pensar que el tamaño del grupo (n) es lo que crece, cuando lo que crece es el número de **pares** (~n²/2).

## Transferencia isomorfa

- **Telescopio ↔ invariante que colapsa el conteo:** cancelar términos intermedios es el mismo gesto que la paridad de divisores o un módulo que evita enumerar (conecta con [[arena-q3]]).
- **Balanza 3ᵏ ↔ cota de información / log₃:** cada pesada extrae log₂3 bits; el límite del canal fija el mínimo de pruebas (conecta con [[arena-q13]]).
- **Cumpleaños (pares ~n²/2) ↔ colisiones de hash:** el umbral √N de colisiones es el mismo conteo de pares (conecta con [[arena-fc1]] y [[arena-fc3]]).
- **Σ k·xᵏ = x/(1−x)² ↔ esperanza geométrica y perpetuidad:** derivar la serie geométrica da E[geométrica] y el valor de un flujo creciente (conecta con [[arena-q5]] y [[arena-q8]]).

Moraleja de la arista: *antes de calcular, busca la identidad que colapsa —telescopio, diferencia de cuadrados, módulo—; el esfuerzo está en reconocer el patrón, no en sumar.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Suma de forma 1/(k(k+1)) | Fracciones parciales → telescopio |
| Multiplicación cerca de potencia de 10 | (a±b)(a∓b) = a²−b² o (a±b)² |
| Potencia mod m | Reduce base, halla período, reduce exponente |
| "Cuántos dígitos d en {1..n}" | Cuenta por posición |
| Σk·x^k | Derivar Σx^k e igualar |
| Cuadrados en tablero n×n | Σj² = n(n+1)(2n+1)/6 |
| "Umbral de cumpleaños" | √(2N·ln2) ≈ 23 para N=365 |
| Pesaje con balanza, k pesadas | Máximo 3^k objetos |
| Hormigas en polígono sin choque | 2/2^n |

---

> **Síntesis:** Los acertijos cuantitativos casi siempre tienen un atajo algebraico o combinatorio. La señal de reconocimiento es la clave: suma de la forma 1/(k(k+1)) → telescopio; multiplicación cerca de múltiplo de 10 → diferencia de cuadrados; potencia mod m → ciclo de residuos. Busca el patrón antes de calcular.

---

*Retrieval: sin mirar, calcula (1) Σ_{k=1}^{99} 1/(k(k+1)); (2) 97² mentalmente; (3) 7^100 mod 9; (4) número de cuadrados en un tablero 5×5.*
