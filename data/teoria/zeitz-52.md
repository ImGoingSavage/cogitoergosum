# Manipulación algebraica: factoriza sin piedad

*Lección redactada para CogitoErgoSum a partir de la sección 5.2 de Zeitz (Algebraic Manipulation Revisited). Cubre el contenido completo de la unidad.*

## El toque ligero

El álgebra de competencia **no es computación: es estética con propósito**. La regla del toque ligero: en cada paso muévete hacia **mayor simplicidad, simetría o belleza** — y desconfía del paso que multiplica términos o rompe estructura.

**El ejemplo modelo:** si x + y = xy = 3, halla x³ + y³.

- **El mal camino:** resolver el sistema. La cuadrática t² − 3t + 3 = 0 tiene discriminante negativo: raíces complejas, raíces cuadradas anidadas, cubos de eso… una carnicería que *puede* funcionar, pero castiga.
- **El toque ligero:** x³ + y³ es simétrico → exprésalo con s = x + y, p = xy (§3.1). El **penúltimo paso** natural es x² + y²: x³ + y³ = (x + y)(x² − xy + y²), y x² + y² = s² − 2p = 9 − 6 = 3, así que x² − xy + y² = 3 − 3 = 0. Entonces x³ + y³ = 3 · 0 = **0**, casi sin calcular.

La moraleja: el problema nunca pidió x e y — pedirle al álgebra más de lo necesario es el pecado original.

## La Factor Tactic

> **Factoriza sin piedad. Multiplicar (expandir) rara vez simplifica; factorizar casi siempre revela.**

Las **dos fábricas** de factorizaciones, con sus condiciones exactas:

1. **xⁿ − yⁿ = (x − y)(xⁿ⁻¹ + xⁿ⁻²y + ⋯ + xyⁿ⁻² + yⁿ⁻¹)** — para **TODO n ≥ 1**.
2. **xⁿ + yⁿ = (x + y)(xⁿ⁻¹ − xⁿ⁻²y + ⋯ − xyⁿ⁻² + yⁿ⁻¹)** — **SOLO para n IMPAR**.

La señal mnemónica de la condición: la segunda es la primera con y → −y, y (−y)ⁿ = −yⁿ exige n impar. (x² + y² no factoriza sobre los reales; x³ + y³ = (x+y)(x² − xy + y²) sí.) Hay que saberlas **activamente** — reconocer cuándo un x⁶ − 1 pide la vía (x²)³ − 1 o (x³)² − 1 según lo que el problema necesite — no recitarlas.

## Sumar cero creativamente (y multiplicar por uno astutamente)

Si los cuadrados perfectos que necesitas **no están, créalos**. El clásico:

**x⁴ + 4** (el acertijo del banco). No tiene raíces reales… y aun así factoriza:

x⁴ + 4 = x⁴ + 4x² + 4 − 4x² = (x² + 2)² − (2x)² = **(x² + 2x + 2)(x² − 2x + 2)**

Sumé y resté 4x² — sumar cero — para completar un cuadrado y abrir paso a la diferencia de cuadrados. **La jugada crucial es esa maniobra, no la fórmula final** (es la misma matriz de Sophie Germain, a⁴ + 4b⁴, de Engel).

**El error conceptual que destapa:** «x⁴ + 4 no tiene raíces reales, así que es irreducible: no se puede factorizar». Lo correcto: sin raíces reales ⇒ **sin factores LINEALES reales**. Pero irreducible significa sin factores de *ningún* grado — y todo polinomio real se factoriza en lineales y **cuadráticas** reales. x⁴+4 lo hace en dos cuadráticas (cada una con sus raíces complejas conjugadas). Raíz real y factor real no son sinónimos más que en grado 1.

## Completar el cuadrado: el prototipo que genera teoría

Completar el cuadrado es el caso semilla de «crear cuadrados», y sus variantes producen teoría entera:

- **(x − y)² + 4xy = (x + y)²** — al sustituir x, y por cuadrados (x = m², y = n²) produce **ternas pitagóricas**: (m² − n²)² + (2mn)² = (m² + n²)².
- **(x² + y²)(a² + b²) = (xa − yb)² + (xb + ya)²** — la identidad del producto: «ser suma de dos cuadrados» **se conserva al multiplicar**. (Detrás está |z|·|w| = |zw| de los complejos, §4.2.)

## Sustitución: si algo feo se repite, bautízalo

**AIME 1983:** resolver x² + 18x + 30 = 2√(x² + 18x + 45).

La señal: **la misma expresión cuadrática aparece dos veces, una bajo la raíz**. Bautiza: **y = √(x² + 18x + 45)**, con el cuidado obligatorio **y ≥ 0** (es una raíz). Entonces x² + 18x + 30 = y² − 15, y la ecuación colapsa:

y² − 15 = 2y → y² − 2y − 15 = (y − 5)(y + 3) = 0 → y = 5 (y = −3 queda prohibido por y ≥ 0)

De y = 5: x² + 18x + 45 = 25 → x² + 18x + 20 = 0, y de ahí lo que pida el problema (el producto de raíces reales es 20, vía Vieta). **El cuidado que exige la jugada:** la restricción del signo de la nueva variable, y verificar al final que las x obtenidas hacen real la raíz.

**La simetría también sugiere sustituciones:** las ecuaciones recíprocas de grado 4 (ax⁴ + bx³ + cx² + bx + a = 0) se parten dividiendo entre x² y poniendo **y = x + 1/x**: quedan dos cuadráticas. La sustitución correcta es la que respeta la simetría de la expresión.

## Disparadores

- Expresión simétrica en x, y → s = x+y, p = xy; pregunta por el penúltimo paso antes de resolver nada.
- Cualquier suma/diferencia de potencias → fábricas de factorización (vigila la paridad de n).
- «Debería factorizar pero no factoriza» → suma cero: crea el cuadrado que falta.
- Expresión fea repetida (a veces bajo raíz) → bautízala, con su restricción de signo.
- Ecuación con coeficientes palíndromos → y = x + 1/x.

## Síntesis

> **Chunk mínimo:** Toque ligero: muévete siempre hacia más simplicidad/simetría — el problema nunca pidió x e y (x+y = xy = 3 ⇒ x³+y³ = (x+y)(x²−xy+y²) = 3·0 = 0 vía s, p). Factor tactic: factoriza sin piedad; las dos fábricas: xⁿ−yⁿ = (x−y)(…) para todo n; xⁿ+yⁿ = (x+y)(…) SOLO n impar. Si el cuadrado no está, créalo sumando cero: x⁴+4 = (x²+2)² − (2x)² = (x²+2x+2)(x²−2x+2) — y «sin raíces reales» solo prohíbe factores LINEALES, no cuadráticos. Expresión fea repetida → bautízala (y = √(…) con y ≥ 0, AIME 1983); coeficientes palíndromos → y = x + 1/x.

---

*Antes del quiz: reconstruye de memoria el camino ligero de x³+y³, las dos fábricas con sus condiciones, la factorización completa de x⁴+4 y la sustitución del AIME 1983 con su cuidado.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Factorizar sin piedad es convertir expresiones opacas en estructura. [[arena-p4]] lo conecta con algebra lineal y calculo para quant, [[aime-alg]] lo practica en sustituciones y sucesiones, y [[engel-pol]] lo extiende a polinomios donde ceros y coeficientes revelan la solucion.
<!-- GRAFO_CONEXO_OLEADA3_END -->
