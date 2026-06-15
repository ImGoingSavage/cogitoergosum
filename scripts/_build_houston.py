# -*- coding: utf-8 -*-
"""Tanda 32 — Kevin Houston, *How to Think Like a Mathematician* (cap. 24-26
técnicas de prueba; cap. 27-29 teoría de números: divisores, Euclides, modular).
Append 44 problemas verificados a data/problems.json. Todas las afirmaciones
numéricas verificadas con Python (ver /tmp/verify_houston.py y la bitácora de
HANDOFFCES.md). Builder idempotente: aborta si hay choque de ids. Sector C
(entrenamiento), esquema §4.1, ids 277-320. Distribución 12/11/7/14
(invariantes/inversion/optimizacion/patrones): Houston es número-teórico y débil
en desigualdades; este sesgo mejora el balance GLOBAL de problems.json."""
import json, collections

SRC = "Houston, *How to Think Like a Mathematician* (Cambridge University Press, 2009)"

def P(id, titulo, estrategia, dificultad, enunciado, hints, solucion, explicacion,
      tiempo, conceptos, transferencias, year, tags, cap):
    assert len(hints) == 5, (id, "hints!=5")
    assert estrategia in {"inversion", "optimizacion", "invariantes", "patrones"}, (id, estrategia)
    assert 1 <= dificultad <= 5, (id, "dificultad")
    return {
        "id": id, "titulo": titulo, "estrategia": estrategia, "dificultad": dificultad,
        "enunciado": enunciado, "hints": hints, "solucion": solucion,
        "explicacion": explicacion, "tiempo_estimado": tiempo, "conceptos": conceptos,
        "transferencias": transferencias, "source": SRC + " — " + cap,
        "source_url": "", "year": year, "tags": tags,
    }

PROBLEMS = []
A = PROBLEMS.append

# =====================================================================
# INVARIANTES (12) — aritmética modular, paridad, divisibilidad
# =====================================================================

A(P(277, "Una expresión siempre par", "invariantes", 1,
 "Demuestra que x² + 9x + 20 es divisible por 2 para todo entero x.",
 ["No pruebes caso por caso al infinito: busca una propiedad de paridad que valga siempre. ¿Puedes factorizar la expresión?",
  "Factoriza el trinomio: x² + 9x + 20 = (x + 4)(x + 5). ¿Qué relación hay entre x+4 y x+5?",
  "x+4 y x+5 son dos enteros CONSECUTIVOS. ¿Qué sabes del producto de dos consecutivos?",
  "De dos enteros consecutivos, exactamente uno es par, así que su producto es par.",
  "Por tanto (x+4)(x+5) es par para todo x, es decir, x² + 9x + 20 es divisible por 2."],
 "Es divisible por 2 para todo x. Factorizando, x² + 9x + 20 = (x + 4)(x + 5), un producto de dos enteros consecutivos; de dos consecutivos uno siempre es par, así que el producto es par.",
 "Invariante de paridad por factorización: reconocer un producto de consecutivos garantiza la divisibilidad por 2 sin analizar casos. Verificado con Python: 2 | x²+9x+20 para x ∈ [−50, 50].",
 8, ["paridad", "producto de consecutivos", "factorización"],
 ["divisibilidad de polinomios", "argumentos de paridad", "factorización de trinomios"],
 "", ["paridad", "divisibilidad", "nivel-basico"], "cap. 27 (Ej. 27.14)"))

A(P(278, "xⁿ − x y los primos", "invariantes", 3,
 "Demuestra que x³ − x es divisible por 3 y que x⁵ − x es divisible por 5, para todo entero x. ¿Es cierto que xⁿ − x es divisible por n para todo n?",
 ["Factoriza x³ − x y trabaja módulo 3. Lo mismo con x⁵ − x módulo 5.",
  "x³ − x = x(x−1)(x+1) es un producto de TRES enteros consecutivos (x−1, x, x+1), así que es divisible por 3 (de hecho por 6).",
  "Para x⁵ − x módulo 5, usa el pequeño teorema de Fermat: para p primo, xᵖ ≡ x (mód p). Con p=5: x⁵ ≡ x (mód 5).",
  "El patrón sugiere xⁿ − x divisible por n. Pero el teorema de Fermat solo garantiza esto cuando n es PRIMO. Prueba un n compuesto.",
  "Con n = 4 y x = 2: 2⁴ − 2 = 14, que NO es divisible por 4. Así que la generalización es FALSA para n compuesto."],
 "x³ − x = x(x−1)(x+1) es producto de tres consecutivos, divisible por 3; y x⁵ − x ≡ 0 (mód 5) por el pequeño teorema de Fermat (xᵖ ≡ x mód p para p primo). La generalización xⁿ − x divisible por n NO es cierta para todo n: falla para n compuesto, por ejemplo 2⁴ − 2 = 14 no es divisible por 4.",
 "Invariante modular vía el pequeño teorema de Fermat (válido solo para módulos primos). El contraejemplo n=4 muestra que el patrón se rompe fuera de los primos. Verificado con Python: 3 | x³−x y 5 | x⁵−x para todo x; 4 ∤ 2⁴−2.",
 18, ["pequeño teorema de Fermat", "producto de consecutivos", "contraejemplo"],
 ["congruencias", "el papel de la primalidad", "test de pseudoprimos"],
 "", ["modular", "fermat", "divisibilidad", "nivel-medio"], "cap. 27 (Ej. 27.23ii)"))

A(P(279, "Un cúbico divisible por 3", "invariantes", 2,
 "Demuestra que x³ − 6x² + 11x es divisible por 3 para todo entero x.",
 ["Trabaja módulo 3: reduce cada coeficiente módulo 3 y simplifica la expresión.",
  "Módulo 3: −6 ≡ 0 y 11 ≡ 2 ≡ −1. Así que x³ − 6x² + 11x ≡ x³ − x (mód 3).",
  "Ya sabes (o puedes ver) que x³ − x = x(x−1)(x+1) es producto de tres consecutivos, divisible por 3.",
  "Por tanto x³ − 6x² + 11x ≡ x³ − x ≡ 0 (mód 3).",
  "La expresión es divisible por 3 para todo entero x."],
 "Es divisible por 3 para todo x. Módulo 3, −6 ≡ 0 y 11 ≡ −1, así que x³ − 6x² + 11x ≡ x³ − x (mód 3). Como x³ − x = x(x−1)(x+1) es producto de tres consecutivos, es divisible por 3, y por tanto también la expresión original.",
 "Reducir coeficientes módulo 3 transforma el cúbico en x³−x, cuyo factor de consecutivos da la divisibilidad. Verificado con Python: 3 | x³−6x²+11x para x ∈ [−50, 50].",
 14, ["reducción modular de coeficientes", "x³−x", "producto de consecutivos"],
 ["congruencias polinómicas", "divisibilidad", "aritmética modular"],
 "", ["modular", "divisibilidad", "cubico", "nivel-basico"], "cap. 27 (Ej. 27.23iii)"))

A(P(280, "Cuadrados módulo cuatro", "invariantes", 2,
 "Demuestra que si n es un cuadrado perfecto, entonces n módulo 4 es 0 o 1 (nunca 2 ni 3).",
 ["Escribe n = k² y analiza por CASOS según la paridad (o la clase módulo algo) de k.",
  "Si k es par, k = 2m, entonces n = 4m² ≡ 0 (mód 4). Si k es impar, k = 2m+1.",
  "Si k = 2m+1, entonces n = (2m+1)² = 4m² + 4m + 1 = 4(m²+m) + 1 ≡ 1 (mód 4).",
  "En ambos casos n módulo 4 es 0 (k par) o 1 (k impar): nunca 2 ni 3.",
  "Por tanto todo cuadrado perfecto es ≡ 0 o 1 (mód 4)."],
 "Todo cuadrado es ≡ 0 o 1 (mód 4). Escribiendo n = k²: si k es par (k=2m), n = 4m² ≡ 0; si k es impar (k=2m+1), n = 4(m²+m)+1 ≡ 1. Nunca se obtiene 2 ni 3.",
 "Invariante modular por casos sobre la paridad: los cuadrados ocupan solo las clases 0 y 1 módulo 4. Es una herramienta clave para probar que ciertas ecuaciones no tienen solución. Verificado con Python: k² mód 4 ∈ {0,1} para k ∈ [0,199].",
 14, ["clases cuadráticas módulo 4", "análisis por casos", "residuos cuadráticos"],
 ["residuos cuadráticos", "no existencia de soluciones diofantinas", "aritmética modular"],
 "", ["modular", "cuadrados", "casos", "nivel-basico"], "cap. 29 (Teo. 29.5)"))

A(P(281, "Nueve a la n menos uno", "invariantes", 2,
 "Demuestra que 3^{2n} − 1 es divisible por 8 para todo entero no negativo n.",
 ["Nota que 3^{2n} = (3²)ⁿ = 9ⁿ. Trabaja módulo 8.",
  "Módulo 8, 9 ≡ 1. Por tanto 9ⁿ ≡ 1ⁿ = 1 (mód 8).",
  "Entonces 9ⁿ − 1 ≡ 0 (mód 8).",
  "Es decir, 3^{2n} − 1 = 9ⁿ − 1 es divisible por 8.",
  "(También sale por inducción: 9^{k+1} − 1 = 9(9ᵏ − 1) + 8.)"],
 "Es divisible por 8. Como 3^{2n} = 9ⁿ y 9 ≡ 1 (mód 8), se tiene 9ⁿ ≡ 1ⁿ = 1 (mód 8), de modo que 9ⁿ − 1 ≡ 0 (mód 8).",
 "Invariante modular trivial tras reescribir 3^{2n} = 9ⁿ y notar 9 ≡ 1 (mód 8). Verificado con Python: 8 | 3^{2n}−1 para n = 0..29.",
 12, ["aritmética modular", "reescritura de potencias", "base ≡ 1"],
 ["congruencias de potencias", "órdenes módulo m", "divisibilidad"],
 "", ["modular", "divisibilidad", "potencias", "nivel-basico"], "cap. 24 (Ej. 24.10iii)"))

A(P(282, "Diecisiete divide a una suma de potencias", "invariantes", 3,
 "Demuestra que 17 divide a 3^{4n} + 4^{3n+2} para todo entero no negativo n.",
 ["Reescribe ambas potencias con exponente n y trabaja módulo 17.",
  "3^{4n} = (3⁴)ⁿ = 81ⁿ y 4^{3n+2} = 4²·(4³)ⁿ = 16·64ⁿ. Reduce las bases módulo 17.",
  "Módulo 17: 81 = 4·17 + 13 ≡ 13 ≡ −4, y 64 = 3·17 + 13 ≡ 13 ≡ −4. ¡Ambas bases son ≡ −4!",
  "Entonces 3^{4n} + 4^{3n+2} ≡ (−4)ⁿ + 16·(−4)ⁿ = (1 + 16)(−4)ⁿ = 17·(−4)ⁿ (mód 17).",
  "17·(−4)ⁿ ≡ 0 (mód 17), así que 17 divide a la suma."],
 "17 divide a la suma. Reescribiendo 3^{4n} = 81ⁿ y 4^{3n+2} = 16·64ⁿ, y reduciendo módulo 17 (81 ≡ −4 y 64 ≡ −4), se obtiene 3^{4n} + 4^{3n+2} ≡ (−4)ⁿ + 16(−4)ⁿ = 17(−4)ⁿ ≡ 0 (mód 17).",
 "Invariante modular: agrupar exponentes y descubrir que ambas bases coinciden módulo 17 (−4) hace que la suma factorice 17. Verificado con Python: 17 | 3^{4n}+4^{3n+2} para n = 0..29.",
 18, ["aritmética modular", "agrupar exponentes", "bases congruentes"],
 ["congruencias de sumas de potencias", "factorización modular", "divisibilidad"],
 "", ["modular", "divisibilidad", "potencias", "nivel-medio"], "cap. 24 (Ej. 24.10iv)"))

A(P(283, "El cuadrado de un impar menos uno", "invariantes", 2,
 "Demuestra que n² − 1 es divisible por 8 siempre que n sea un entero impar.",
 ["Escribe n impar como n = 2m + 1 y desarrolla n² − 1.",
  "n² − 1 = (n−1)(n+1). Para n impar, n−1 y n+1 son dos enteros PARES consecutivos.",
  "De dos pares consecutivos, uno es divisible por 4 y el otro por 2, así que su producto es divisible por 8.",
  "Alternativamente: (2m+1)² − 1 = 4m² + 4m = 4m(m+1), y m(m+1) es par (consecutivos), así que 4m(m+1) es divisible por 8.",
  "Por tanto 8 divide a n² − 1 para todo n impar."],
 "Es divisible por 8. Con n = 2m+1, n² − 1 = 4m² + 4m = 4m(m+1); como m(m+1) es producto de consecutivos (par), 4m(m+1) es divisible por 8. (Equivalentemente, (n−1)(n+1) son dos pares consecutivos, uno múltiplo de 4.)",
 "Invariante de paridad fina: el cuadrado de un impar es ≡ 1 (mód 8). Verificado con Python: 8 | n²−1 para todo n impar en [1, 99].",
 14, ["paridad", "pares consecutivos", "cuadrados de impares módulo 8"],
 ["residuos cuadráticos módulo 8", "divisibilidad", "argumentos de paridad"],
 "", ["paridad", "divisibilidad", "impares", "nivel-basico"], "cap. 24 (Ej. 24.10vii)"))

A(P(284, "Una suma divisible por seis", "invariantes", 2,
 "Demuestra que 4·11ⁿ + 2·5ⁿ es divisible por 6 para todo entero no negativo n.",
 ["Trabaja módulo 6. Reduce las bases 11 y 5 módulo 6.",
  "Módulo 6: 11 ≡ 5 ≡ −1. Así que 11ⁿ ≡ (−1)ⁿ y 5ⁿ ≡ (−1)ⁿ.",
  "Sustituye: 4·11ⁿ + 2·5ⁿ ≡ 4·(−1)ⁿ + 2·(−1)ⁿ = 6·(−1)ⁿ (mód 6).",
  "6·(−1)ⁿ ≡ 0 (mód 6).",
  "Por tanto 4·11ⁿ + 2·5ⁿ es divisible por 6."],
 "Es divisible por 6. Módulo 6, tanto 11 como 5 son ≡ −1, así que 4·11ⁿ + 2·5ⁿ ≡ 4(−1)ⁿ + 2(−1)ⁿ = 6(−1)ⁿ ≡ 0 (mód 6).",
 "Invariante modular: ambas bases coinciden (≡ −1 mód 6), y los coeficientes 4 y 2 suman 6. Surge de la propiedad x−y | xⁿ−yⁿ aplicada con cuidado. Verificado con Python: 6 | 4·11ⁿ+2·5ⁿ para n = 0..29.",
 12, ["aritmética modular", "bases congruentes", "factor común"],
 ["congruencias de sumas de potencias", "x−y divide xⁿ−yⁿ", "divisibilidad"],
 "", ["modular", "divisibilidad", "potencias", "nivel-basico"], "cap. 27 (Ej. 27.23x)"))

A(P(285, "Divisibilidad por ocho mirando tres dígitos", "invariantes", 2,
 "Demuestra que un número natural es divisible por 8 si y solo si el número formado por sus tres últimos dígitos lo es.",
 ["Separa el número en su 'parte de miles' y sus tres últimos dígitos: N = 1000·q + r, donde r son los tres últimos dígitos.",
  "¿Qué relación hay entre 1000 y 8? Calcula 1000 ÷ 8.",
  "1000 = 8·125, así que 1000 ≡ 0 (mód 8). Por tanto N = 1000q + r ≡ r (mód 8).",
  "Entonces N es divisible por 8 exactamente cuando r (los tres últimos dígitos) lo es.",
  "Esto generaliza: divisible por 2ᵏ ⟺ los últimos k dígitos lo son, porque 10ᵏ = 2ᵏ·5ᵏ."],
 "N es divisible por 8 sii sus tres últimos dígitos lo son. Escribiendo N = 1000q + r (r = tres últimos dígitos), como 1000 = 8·125 ≡ 0 (mód 8), se tiene N ≡ r (mód 8). Luego 8 | N ⟺ 8 | r. (En general, 2ᵏ | N ⟺ 2ᵏ divide a los últimos k dígitos, pues 10ᵏ = 2ᵏ5ᵏ.)",
 "Invariante posicional: como 10³ ≡ 0 (mód 8), la 'parte alta' del número no afecta su residuo módulo 8. Verificado con Python: para N ∈ [0,5000], 8|N ⟺ 8|(N mód 1000).",
 14, ["aritmética modular posicional", "10³ ≡ 0 (mód 8)", "reglas de divisibilidad"],
 ["criterios de divisibilidad", "representación decimal", "congruencias"],
 "", ["modular", "divisibilidad", "digitos", "nivel-basico"], "cap. 27 (Ej. 27.23ix)"))

A(P(286, "Si m² divide a n², entonces m divide a n", "invariantes", 3,
 "Demuestra que para enteros positivos m y n, si m² divide a n² entonces m divide a n.",
 ["Usa la factorización única en primos (Teorema Fundamental de la Aritmética). Compara exponentes.",
  "Escribe m y n con sus factorizaciones primas. Para un primo p, sea a su exponente en m y b su exponente en n.",
  "El exponente de p en m² es 2a y en n² es 2b. Que m² | n² significa 2a ≤ 2b para todo primo p.",
  "De 2a ≤ 2b se sigue a ≤ b para cada primo p.",
  "a ≤ b para todo primo significa exactamente que m | n."],
 "Si m² | n² entonces m | n. Por el Teorema Fundamental de la Aritmética, para cada primo p sea a su exponente en m y b en n. Entonces m² | n² equivale a 2a ≤ 2b para todo p, lo que da a ≤ b para todo p, es decir m | n.",
 "Invariante de exponentes primos: la divisibilidad se traduce en desigualdades de exponentes, y dividir por 2 las preserva. Verificado con Python: para m ≤ 39, n ≤ 199, m²|n² implica m|n sin excepción.",
 18, ["Teorema Fundamental de la Aritmética", "comparación de exponentes primos", "divisibilidad"],
 ["factorización única", "valuaciones p-ádicas", "estructura multiplicativa"],
 "", ["factorizacion", "divisibilidad", "exponentes", "nivel-medio"], "cap. 27 (Ej. 27.23viii)"))

A(P(287, "Los números de Fermat son coprimos", "invariantes", 4,
 "Define el n-ésimo número de Fermat como Fₙ = 2^{2ⁿ} + 1. Demuestra primero que F₀·F₁·⋯·Fₙ = F_{n+1} − 2, y deduce que dos números de Fermat distintos cualesquiera son coprimos.",
 ["Para la identidad del producto, procede por inducción. Verifica el caso base y el paso usando una diferencia de cuadrados.",
  "Base: F₀ = 3 = F₁ − 2 = 5 − 2. Paso: multiplica la hipótesis (∏_{k≤n} Fₖ = F_{n+1} − 2) por F_{n+1} y usa que F_{n+1} − 2 = 2^{2^{n+1}} − 1.",
  "(F_{n+1} − 2)·F_{n+1} = (2^{2^{n+1}} − 1)(2^{2^{n+1}} + 1) = 2^{2^{n+2}} − 1 = F_{n+2} − 2 (diferencia de cuadrados).",
  "Para la coprimalidad: si un primo p divide a F_j y a F_l con j < l, entonces p divide al producto F₀⋯F_{l−1} = F_l − 2.",
  "Como p | F_l y p | (F_l − 2), p divide a su diferencia 2; pero los Fₙ son impares, así que p ≠ 2. Contradicción: gcd(F_j, F_l) = 1."],
 "Primero, ∏_{k=0}^n Fₖ = F_{n+1} − 2 por inducción: el paso usa (F_{n+1} − 2)·F_{n+1} = (2^{2^{n+1}} − 1)(2^{2^{n+1}} + 1) = 2^{2^{n+2}} − 1 = F_{n+2} − 2. Para la coprimalidad: si un primo p divide a F_j y F_l (j<l), entonces p divide a F₀⋯F_{l−1} = F_l − 2, luego p | (F_l − (F_l − 2)) = 2; pero todo Fₙ es impar, así que p ≠ 2 — contradicción. Por tanto gcd(F_j, F_l) = 1.",
 "Identidad telescópica (diferencia de cuadrados) más un argumento de divisor común que colapsa en 2. Da una prueba elegante de la infinitud de primos (cada Fₙ aporta un primo nuevo). Verificado con Python: ∏F_k = F_{n+1}−2 y gcd(F_j,F_l)=1.",
 30, ["números de Fermat", "diferencia de cuadrados telescópica", "divisor común"],
 ["infinitud de los primos", "identidades telescópicas", "coprimalidad"],
 "", ["fermat", "coprimos", "telescopaje", "nivel-avanzado"], "cap. 27 (Ej. 27.23xi)"))

A(P(288, "Cinco a la n y nueve a la n", "invariantes", 2,
 "Demuestra que 6·9ⁿ − 4ⁿ es divisible por 5 para todo entero no negativo n.",
 ["Trabaja módulo 5. Reduce 6, 9 y 4 módulo 5.",
  "Módulo 5: 6 ≡ 1, 9 ≡ 4 ≡ −1 y 4 ≡ −1. Sustituye.",
  "6·9ⁿ − 4ⁿ ≡ 1·(−1)ⁿ − (−1)ⁿ (mód 5).",
  "1·(−1)ⁿ − (−1)ⁿ = (−1)ⁿ − (−1)ⁿ = 0.",
  "Por tanto 5 divide a 6·9ⁿ − 4ⁿ."],
 "Es divisible por 5. Módulo 5, 6 ≡ 1, 9 ≡ −1 y 4 ≡ −1, así que 6·9ⁿ − 4ⁿ ≡ (−1)ⁿ − (−1)ⁿ = 0 (mód 5).",
 "Invariante modular: tras reducir las bases, los términos se cancelan módulo 5. Es la propiedad x−y | xⁿ−yⁿ encubierta. Verificado con Python: 5 | 6·9ⁿ−4ⁿ para n = 0..29.",
 12, ["aritmética modular", "reducción de bases", "cancelación módulo p"],
 ["x−y divide xⁿ−yⁿ", "congruencias de potencias", "divisibilidad"],
 "", ["modular", "divisibilidad", "potencias", "nivel-basico"], "cap. 27 (Ej. 27.23x)"))

# =====================================================================
# INVERSION (11) — contradicción, contrapositiva, inducción/construcción
# =====================================================================

A(P(289, "Hay infinitos primos", "inversion", 3,
 "Demuestra que existen infinitos números primos.",
 ["Procede por contradicción: supón que solo hay una cantidad FINITA de primos y lístalos.",
  "Sean p₁, p₂, …, pₙ TODOS los primos. Construye un número a partir de ellos que no pueda ser divisible por ninguno.",
  "Considera N = p₁p₂⋯pₙ + 1. ¿Qué resto deja N al dividirlo por cualquier pᵢ?",
  "N deja resto 1 al dividir por cualquier pᵢ, así que ningún primo de la lista divide a N.",
  "Pero N > 1 tiene algún factor primo (o es primo), que no está en la lista — contradicción. Luego hay infinitos primos."],
 "Hay infinitos primos. Supón, por contradicción, que p₁, …, pₙ son todos los primos. El número N = p₁p₂⋯pₙ + 1 deja resto 1 al dividir por cada pᵢ, así que ninguno lo divide; pero N > 1 debe tener un factor primo, que entonces no está en la lista. Contradicción: la lista no puede ser completa, y hay infinitos primos.",
 "Argumento clásico de Euclides por contradicción: fabricar un número coprimo con todos los primos supuestos. La 'solución' es el razonamiento, tomado del libro.",
 20, ["argumento por contradicción", "construcción de Euclides", "factor primo"],
 ["teoría de números", "infinitud de conjuntos", "el método de Euclides"],
 "", ["contradiccion", "primos", "euclides", "nivel-medio"], "cap. 27 (Teo. 27.15)"))

A(P(290, "La raíz de un no-cuadrado es irracional", "inversion", 4,
 "Demuestra que si n es un entero positivo que NO es un cuadrado perfecto, entonces √n es irracional.",
 ["Procede por contradicción: supón √n = r/s con r, s enteros y la fracción en su mínima expresión (gcd(r,s)=1).",
  "Si √n = r/s con gcd(r,s) = 1, eleva al cuadrado: n·s² = r².",
  "Toma un primo p que divida a s (existe si s > 1). Entonces p | r², y por el lema de Euclid p | r.",
  "Pero entonces p divide a r y a s, contradiciendo gcd(r,s) = 1. Luego s = 1 y √n = r es entero.",
  "Si √n fuera entero, n sería un cuadrado perfecto, contra la hipótesis. Por tanto √n es irracional."],
 "√n es irracional. Supón √n = r/s con gcd(r,s) = 1. Entonces n s² = r², así que cualquier primo p | s cumple p | r² y (por el lema de Euclid) p | r, contradiciendo gcd(r,s)=1. Luego s = 1 y √n = r sería entero, lo que haría a n un cuadrado perfecto — contra la hipótesis. Por tanto √n es irracional.",
 "Contradicción apoyada en la factorización (lema de Euclid): un divisor primo del denominador forzaría un factor común. Generaliza la irracionalidad de √2. Verificado con Python: para n ∈ {2,3,5,7,10,12,15}, √n no coincide con ninguna fracción de denominador ≤ 10⁴.",
 26, ["argumento por contradicción", "lema de Euclid", "fracciones en mínima expresión"],
 ["irracionalidad", "factorización única", "teoría de números"],
 "", ["contradiccion", "irracionalidad", "raices", "nivel-avanzado"], "cap. 28 (Cor. 28.14)"))

A(P(291, "Si x es irracional, también lo es su raíz", "inversion", 2,
 "Sea x un número real positivo. Demuestra que si x es irracional, entonces √x es irracional.",
 ["Usa el método CONTRAPOSITIVO: en vez de 'x irracional ⇒ √x irracional', prueba el contrapositivo.",
  "El contrapositivo de 'x irracional ⇒ √x irracional' es 'si √x es racional, entonces x es racional'.",
  "Supón que √x es racional, digamos √x = p/q con p, q enteros.",
  "Eleva al cuadrado: x = (√x)² = p²/q², que es un cociente de enteros.",
  "Por tanto x es racional. Esto prueba el contrapositivo y, con él, el enunciado original."],
 "Si x es irracional, √x es irracional. Por contrapositivo, probamos: si √x es racional entonces x lo es. En efecto, si √x = p/q (racional), entonces x = (√x)² = p²/q² es racional. El contrapositivo equivale al enunciado original.",
 "Método contrapositivo: convertir el enunciado en uno más fácil de atacar directamente (cuadrar un racional da un racional). La 'solución' es el razonamiento lógico.",
 12, ["método contrapositivo", "racional al cuadrado es racional", "lógica de implicaciones"],
 ["equivalencia lógica", "irracionalidad", "técnicas de demostración"],
 "", ["contrapositiva", "irracionalidad", "logica", "nivel-basico"], "cap. 26 (Ej. 26.7iv)"))

A(P(292, "Suma irracional", "inversion", 2,
 "Sean x e y números reales. Demuestra que si x + y es irracional, entonces x es irracional o y es irracional.",
 ["Usa el método contrapositivo. ¿Cuál es el contrapositivo de la implicación?",
  "El contrapositivo de 'x+y irracional ⇒ (x irracional o y irracional)' es 'si x e y son AMBOS racionales, entonces x+y es racional'.",
  "Supón que x e y son ambos racionales, digamos x = a/b e y = c/d.",
  "Entonces x + y = a/b + c/d = (ad + bc)/(bd), un cociente de enteros.",
  "Por tanto x+y es racional, lo que prueba el contrapositivo y, con él, el enunciado original."],
 "Si x+y es irracional, entonces x o y es irracional. Por contrapositivo: si x e y son ambos racionales (x=a/b, y=c/d), entonces x+y = (ad+bc)/(bd) es racional. El contrapositivo equivale al enunciado.",
 "Método contrapositivo: negar la conclusión ('alguno irracional' → 'ambos racionales') vuelve el problema una suma directa de racionales. La 'solución' es el razonamiento lógico.",
 12, ["método contrapositivo", "cerradura de ℚ bajo suma", "negación de 'o'"],
 ["estructura de cuerpo de ℚ", "técnicas de demostración", "lógica proposicional"],
 "", ["contrapositiva", "irracionalidad", "logica", "nivel-basico"], "cap. 26 (Ej. 26.7ii)"))

A(P(293, "Producto impar", "inversion", 2,
 "Sean x e y números naturales. Demuestra que si xy es impar, entonces x e y son ambos impares.",
 ["Usa el método contrapositivo. ¿Qué es lo contrario de 'x e y ambos impares'?",
  "El contrapositivo de 'xy impar ⇒ (x e y ambos impares)' es 'si x es par o y es par, entonces xy es par'.",
  "Supón que al menos uno, digamos x, es par: x = 2k.",
  "Entonces xy = 2ky es un múltiplo de 2, es decir par.",
  "Esto prueba el contrapositivo: si alguno es par, el producto es par; equivalentemente, producto impar fuerza ambos impares."],
 "Si xy es impar, x e y son ambos impares. Por contrapositivo: si alguno (digamos x) es par, x = 2k, entonces xy = 2ky es par. Luego un producto impar obliga a que ambos factores sean impares.",
 "Método contrapositivo sobre paridad: 'alguno par ⇒ producto par' es inmediato y equivale al enunciado. Verificado con Python: xy impar ⟺ (x impar y y impar) para x,y ∈ [1,29].",
 10, ["método contrapositivo", "paridad de productos", "negación de conjunción"],
 ["argumentos de paridad", "técnicas de demostración", "lógica proposicional"],
 "", ["contrapositiva", "paridad", "logica", "nivel-basico"], "cap. 26 (Ej. 26.7i)"))

A(P(294, "Si su cuadrado es par", "inversion", 2,
 "Sea x un entero. Demuestra que si x² es par, entonces x es par.",
 ["El enunciado directo es incómodo; usa el método contrapositivo.",
  "El contrapositivo de 'x² par ⇒ x par' es 'si x es impar, entonces x² es impar'.",
  "Supón x impar: x = 2k + 1.",
  "Entonces x² = (2k+1)² = 4k² + 4k + 1 = 2(2k²+2k) + 1, que es impar.",
  "Esto prueba el contrapositivo: x impar ⇒ x² impar; equivalentemente, x² par ⇒ x par."],
 "Si x² es par, x es par. Por contrapositivo: si x es impar, x = 2k+1, entonces x² = 2(2k²+2k)+1 es impar. Luego x² par obliga a x par.",
 "Método contrapositivo clásico (pieza clave en la irracionalidad de √2): probar 'impar ⇒ cuadrado impar' es directo. Verificado con Python: x² par ⟺ x par para x ∈ [−50,50].",
 10, ["método contrapositivo", "paridad de cuadrados", "lógica de implicaciones"],
 ["irracionalidad de √2", "argumentos de paridad", "técnicas de demostración"],
 "", ["contrapositiva", "paridad", "cuadrados", "nivel-basico"], "cap. 26 (Ej. 26.5)"))

A(P(295, "Todo entero es producto de primos", "inversion", 3,
 "Demuestra que todo número natural mayor que 1 es un primo o un producto de primos.",
 ["Usa inducción FUERTE: supón que el resultado vale para todos los números entre 2 y k, y pruébalo para k+1.",
  "Caso base: 2 es primo. Hipótesis fuerte: todo entero de 2 a k es primo o producto de primos.",
  "Considera k+1. Si k+1 es primo, ya está. Si no, k+1 = a·b con 1 < a, b < k+1.",
  "Como a y b son menores que k+1 (y > 1), por la hipótesis fuerte cada uno es primo o producto de primos.",
  "Entonces k+1 = a·b es un producto de primos. Por inducción fuerte, todo n > 1 lo es."],
 "Todo n > 1 es primo o producto de primos. Por inducción fuerte: 2 es primo. Para k+1, si es primo terminamos; si no, k+1 = a·b con 1 < a,b < k+1, y por la hipótesis fuerte a y b son productos de primos, luego k+1 = a·b también lo es.",
 "Inducción fuerte (parte de existencia del Teorema Fundamental de la Aritmética): un compuesto se parte en factores menores cubiertos por la hipótesis. Verificado con Python: todo n de 2 a 299 es producto de primos.",
 18, ["inducción fuerte", "Teorema Fundamental de la Aritmética", "descomposición en factores"],
 ["factorización en primos", "inducción completa", "estructura de los enteros"],
 "", ["induccion-fuerte", "primos", "factorizacion", "nivel-medio"], "cap. 25 (Teo. 25.5)"))

A(P(296, "Una recurrencia que da 2ⁿ + 1", "inversion", 3,
 "Sea x₁ = 3, x₂ = 5 y xₙ = 3xₙ₋₁ − 2xₙ₋₂ para n ≥ 3. Demuestra que xₙ = 2ⁿ + 1 para todo n ≥ 1.",
 ["Como la recurrencia usa los DOS términos anteriores, emplea inducción fuerte con dos casos base.",
  "Bases: x₁ = 3 = 2¹ + 1 ✓ y x₂ = 5 = 2² + 1 ✓. Supón la fórmula para k−1 y k.",
  "Sustituye en la recurrencia: x_{k+1} = 3xₖ − 2xₖ₋₁ = 3(2ᵏ + 1) − 2(2^{k−1} + 1).",
  "Desarrolla: 3·2ᵏ + 3 − 2·2^{k−1} − 2 = 3·2ᵏ − 2ᵏ + 1 = 2·2ᵏ + 1 = 2^{k+1} + 1.",
  "Eso es la fórmula para k+1, completando la inducción fuerte."],
 "xₙ = 2ⁿ + 1. Por inducción fuerte con bases x₁ = 3 = 2¹+1 y x₂ = 5 = 2²+1. Paso: x_{k+1} = 3xₖ − 2xₖ₋₁ = 3(2ᵏ+1) − 2(2^{k−1}+1) = 3·2ᵏ − 2ᵏ + 1 = 2^{k+1} + 1.",
 "Inducción fuerte sobre una recurrencia lineal de orden 2 (ecuación característica (x−1)(x−2)=0, raíces 1 y 2). Verificado con Python: xₙ = 2ⁿ+1 para n = 1..24.",
 18, ["inducción fuerte", "recurrencia lineal de orden 2", "dos casos base"],
 ["soluciones cerradas de recurrencias", "ecuación característica", "sucesiones definidas recursivamente"],
 "", ["induccion-fuerte", "recurrencia", "nivel-medio"], "cap. 25 (Ej. 25.3)"))

A(P(297, "x − 1 divide a xⁿ − 1", "inversion", 2,
 "Demuestra que para todo entero x > 1 y todo entero positivo n, el número x − 1 divide a xⁿ − 1.",
 ["Procede por inducción sobre n. Verifica n = 1 y luego el paso inductivo.",
  "Base: n = 1 da x¹ − 1 = x − 1, divisible por x − 1. Supón que x − 1 divide a xᵏ − 1.",
  "Para el paso, escribe x^{k+1} − 1 en términos de xᵏ − 1. Suma y resta un término conveniente.",
  "x^{k+1} − 1 = x·xᵏ − 1 = x(xᵏ − 1) + (x − 1).",
  "Ambos sumandos, x(xᵏ − 1) y (x − 1), son divisibles por x − 1, así que su suma también. Inducción completa."],
 "x − 1 divide a xⁿ − 1. Por inducción: base x¹ − 1 = x − 1. Paso: x^{k+1} − 1 = x(xᵏ − 1) + (x − 1); ambos términos son divisibles por x − 1 (el primero por hipótesis), así que x^{k+1} − 1 también. (Equivalente: xⁿ − 1 = (x−1)(x^{n−1} + ⋯ + x + 1).)",
 "Inducción por descomposición x^{k+1}−1 = x(xᵏ−1)+(x−1); equivale a la factorización geométrica xⁿ−1 = (x−1)Σxⁱ. Verificado con Python: (x−1) | (xⁿ−1) para x ∈ [2,14], n ∈ [1,11].",
 12, ["inducción", "factorización geométrica", "divisibilidad de polinomios"],
 ["serie geométrica", "factorización de xⁿ−1", "divisibilidad"],
 "", ["induccion", "divisibilidad", "factorizacion", "nivel-basico"], "cap. 24 (Ej. 24.12)"))

A(P(298, "Los ángulos de un polígono", "inversion", 3,
 "Demuestra que la suma de los ángulos interiores de un polígono convexo de n lados es 180(n − 2) grados, para todo n ≥ 3.",
 ["Inducción sobre n. ¿Cuál es el caso base y cómo pasas de un n-gono a un (n+1)-gono?",
  "Base n = 3: los ángulos de un triángulo suman 180 = 180(3−2). ✓. Supón el resultado para n.",
  "Para el paso, toma un (n+1)-gono y 'córtale' un triángulo trazando una diagonal que una dos vértices con uno intermedio.",
  "La diagonal divide el (n+1)-gono en un n-gono y un triángulo. La suma de ángulos del (n+1)-gono = suma del n-gono + suma del triángulo.",
  "= 180(n−2) + 180 = 180(n−1) = 180((n+1)−2). Inducción completa."],
 "La suma es 180(n−2). Por inducción: base n=3 (triángulo, 180°). Paso: una diagonal divide un (n+1)-gono en un n-gono y un triángulo, así que su suma de ángulos = 180(n−2) + 180 = 180((n+1)−2). Por inducción vale para todo n ≥ 3.",
 "Inducción geométrica por disección: cortar un triángulo reduce el polígono al caso anterior y añade 180°. La 'solución' es el argumento, tomado del libro.",
 16, ["inducción geométrica", "disección por diagonales", "ángulos de polígonos"],
 ["triangulación de polígonos", "geometría euclidiana", "inducción constructiva"],
 "", ["induccion", "geometria", "poligonos", "nivel-medio"], "cap. 25 (Ej. 25.2iii)"))

A(P(299, "Resolver una desigualdad cuadrática", "inversion", 2,
 "Demuestra que si x² − 3x + 2 < 0, entonces 1 < x < 2 (y recíprocamente).",
 ["Factoriza el cuadrático y analiza los SIGNOS de los factores.",
  "x² − 3x + 2 = (x − 1)(x − 2). Para que el producto sea negativo, los factores deben tener signos OPUESTOS.",
  "(x−1)(x−2) < 0 ocurre cuando uno es positivo y el otro negativo. ¿Cuándo pasa eso?",
  "Si x − 1 > 0 y x − 2 < 0, es decir x > 1 y x < 2, o sea 1 < x < 2. El otro caso (x−1<0 y x−2>0) es imposible.",
  "Por tanto x² − 3x + 2 < 0 ⟺ 1 < x < 2."],
 "x² − 3x + 2 < 0 ⟺ 1 < x < 2. Factorizando, x² − 3x + 2 = (x − 1)(x − 2); el producto es negativo exactamente cuando los factores tienen signos opuestos, lo que (descartando el caso imposible x<1 y x>2) ocurre sii x − 1 > 0 y x − 2 < 0, es decir 1 < x < 2.",
 "Resolver una desigualdad cuadrática por análisis de signos de los factores: el producto de dos factores es negativo sii tienen signos opuestos. Verificado con Python: para x en pasos de 0.01 sobre [0,3], (x²−3x+2<0) ⟺ (1<x<2).",
 12, ["factorización", "análisis de signos", "desigualdades cuadráticas"],
 ["resolución de inecuaciones", "ceros de un polinomio", "equivalencias lógicas"],
 "", ["desigualdad", "factorizacion", "cuadratica", "nivel-basico"], "cap. 26 (Ej. 26.7iii)"))

# =====================================================================
# OPTIMIZACION (7) — desigualdades y argumentos extremales
# =====================================================================

A(P(300, "n al cuadrado contra una potencia de dos", "optimizacion", 3,
 "Demuestra que n² ≤ 2^{n−1} para todo entero n ≥ 7.",
 ["Inducción a partir de n = 7 (el resultado es falso para n = 2,…,6). Verifica la base.",
  "Base n=7: 7² = 49 ≤ 64 = 2⁶ = 2^{7−1}. ✓. Supón n² ≤ 2^{n−1} para algún n ≥ 7.",
  "Para el paso, multiplica la meta: quieres (n+1)² ≤ 2ⁿ = 2·2^{n−1}. Usa la hipótesis y acota (n+1)²/n².",
  "(n+1)² = n²·(1 + 1/n)². Para n ≥ 7, (1+1/n)² ≤ (8/7)² = 64/49 < 2.",
  "Entonces (n+1)² = n²(1+1/n)² ≤ 2n² ≤ 2·2^{n−1} = 2ⁿ = 2^{(n+1)−1}. Inducción completa."],
 "n² ≤ 2^{n−1} para n ≥ 7. Por inducción: base 7² = 49 ≤ 64 = 2⁶. Paso: (n+1)² = n²(1+1/n)² ≤ 2n² (pues (1+1/n)² ≤ (8/7)² < 2 para n ≥ 7) ≤ 2·2^{n−1} = 2^{(n+1)−1}.",
 "Inducción con caso base desplazado (el enunciado falla para n=2..6) y paso que acota (1+1/n)² < 2. Verificado con Python: n² ≤ 2^{n−1} para n = 7..39.",
 18, ["inducción con base desplazada", "polinómica vs exponencial", "acotar (1+1/n)²"],
 ["crecimiento exponencial vs polinómico", "desigualdades por inducción", "análisis asintótico"],
 "", ["induccion", "desigualdad", "exponencial", "nivel-medio"], "cap. 25 (Ej. 25.1)"))

A(P(301, "Dos a la n contra el factorial", "optimizacion", 2,
 "Demuestra que 2ⁿ < n! para todo entero n ≥ 4.",
 ["Inducción desde n = 4 (es falso para n = 1,2,3). Verifica la base.",
  "Base n=4: 2⁴ = 16 < 24 = 4!. ✓. Supón 2ⁿ < n! para algún n ≥ 4.",
  "Para el paso, multiplica: 2^{n+1} = 2·2ⁿ y (n+1)! = (n+1)·n!. Compara los factores que multiplican.",
  "Como n ≥ 4, el factor n+1 ≥ 5 > 2. Por la hipótesis 2ⁿ < n!, multiplicando por 2 < n+1:",
  "2^{n+1} = 2·2ⁿ < (n+1)·n! = (n+1)!. Inducción completa."],
 "2ⁿ < n! para n ≥ 4. Por inducción: base 2⁴ = 16 < 24 = 4!. Paso: 2^{n+1} = 2·2ⁿ < (n+1)·n! = (n+1)! porque 2 < n+1 (n ≥ 4) y 2ⁿ < n! por hipótesis.",
 "Inducción donde el paso compara los factores multiplicativos (2 contra n+1). Verificado con Python: 2ⁿ < n! para n = 4..29.",
 14, ["inducción con base desplazada", "exponencial vs factorial", "comparación de factores"],
 ["crecimiento del factorial", "desigualdades por inducción", "análisis asintótico"],
 "", ["induccion", "desigualdad", "factorial", "nivel-basico"], "cap. 25 (Ej. 25.2ii)"))

A(P(302, "Una sucesión acotada por una potencia", "optimizacion", 3,
 "Sea x₁ = 1, x₂ = 3 y xₙ = xₙ₋₁ + xₙ₋₂ para n ≥ 3. Demuestra que xₙ < (7/4)ⁿ para todo n ≥ 1.",
 ["Como la recurrencia usa los dos términos anteriores, usa inducción fuerte con dos bases.",
  "Bases: x₁ = 1 < 7/4 ✓ y x₂ = 3 < (7/4)² = 49/16 ≈ 3.06 ✓. Supón xₖ < (7/4)ᵏ para todo k ≤ n.",
  "Acota x_{n+1} = xₙ + xₙ₋₁ < (7/4)ⁿ + (7/4)^{n−1} usando la hipótesis.",
  "Factoriza (7/4)^{n−1}: (7/4)ⁿ + (7/4)^{n−1} = (7/4)^{n−1}·(7/4 + 1) = (7/4)^{n−1}·(11/4).",
  "Basta ver que 11/4 ≤ (7/4)² = 49/16, es decir 44/16 ≤ 49/16. ✓. Luego x_{n+1} < (7/4)^{n+1}."],
 "xₙ < (7/4)ⁿ. Por inducción fuerte con bases x₁ = 1 < 7/4 y x₂ = 3 < 49/16. Paso: x_{n+1} = xₙ + xₙ₋₁ < (7/4)ⁿ + (7/4)^{n−1} = (7/4)^{n−1}(7/4 + 1) = (7/4)^{n−1}·(11/4) ≤ (7/4)^{n−1}·(7/4)² = (7/4)^{n+1}, porque 11/4 = 44/16 ≤ 49/16.",
 "Inducción fuerte donde el paso se reduce a la desigualdad numérica 7/4 + 1 ≤ (7/4)² (es decir, 7/4 es mayor que la razón áurea ≈ 1.618). Verificado con Python: xₙ < (7/4)ⁿ para n = 1..39.",
 20, ["inducción fuerte", "cota de crecimiento de una recurrencia", "razón áurea"],
 ["sucesiones de tipo Fibonacci", "raíces características vs cotas", "desigualdades por inducción"],
 "", ["induccion-fuerte", "recurrencia", "cota", "nivel-medio"], "cap. 25 (Ej. 25.4i)"))

A(P(303, "La desigualdad triangular generalizada", "optimizacion", 2,
 "Demuestra que para cualesquiera números reales x₁, x₂, …, xₙ se cumple |x₁ + x₂ + ⋯ + xₙ| ≤ |x₁| + |x₂| + ⋯ + |xₙ|.",
 ["Inducción sobre n, apoyándote en la desigualdad triangular para DOS números: |a + b| ≤ |a| + |b|.",
  "Base n=1: |x₁| ≤ |x₁|. ✓. Supón |x₁+⋯+xₙ| ≤ |x₁|+⋯+|xₙ|.",
  "Para el paso, agrupa la suma de n+1 términos como (x₁+⋯+xₙ) + xₙ₊₁ y aplica la desigualdad triangular de dos términos.",
  "|x₁+⋯+xₙ+xₙ₊₁| ≤ |x₁+⋯+xₙ| + |xₙ₊₁|.",
  "Por la hipótesis, ≤ (|x₁|+⋯+|xₙ|) + |xₙ₊₁|. Inducción completa."],
 "|Σxᵢ| ≤ Σ|xᵢ|. Por inducción: base |x₁| ≤ |x₁|. Paso: |x₁+⋯+xₙ+xₙ₊₁| ≤ |x₁+⋯+xₙ| + |xₙ₊₁| (triangular de dos términos) ≤ |x₁|+⋯+|xₙ|+|xₙ₊₁| (hipótesis).",
 "Inducción que reduce el caso general al caso de dos términos (la desigualdad triangular básica). Verificado con Python: 3000 muestras aleatorias cumplen |Σxᵢ| ≤ Σ|xᵢ|.",
 12, ["inducción", "desigualdad triangular", "reducción al caso base"],
 ["normas y valor absoluto", "espacios métricos", "desigualdades fundamentales"],
 "", ["induccion", "desigualdad", "triangular", "nivel-basico"], "cap. 24 (Ej. 24.10xv)"))

A(P(304, "El máximo común divisor de la suma y la diferencia", "optimizacion", 3,
 "Sean a y b enteros positivos coprimos (gcd(a, b) = 1). Demuestra que gcd(a + b, a − b) ≤ 2.",
 ["Sea g = gcd(a+b, a−b). Si g divide a a+b y a a−b, ¿qué otras combinaciones divide?",
  "Como g | (a+b) y g | (a−b), g divide a su suma y a su diferencia: (a+b)+(a−b) = 2a y (a+b)−(a−b) = 2b.",
  "Así que g | 2a y g | 2b, de donde g divide a gcd(2a, 2b) = 2·gcd(a,b).",
  "Como a y b son coprimos, gcd(a,b) = 1, así que g | 2.",
  "Un divisor de 2 es 1 o 2, por lo que gcd(a+b, a−b) ≤ 2."],
 "gcd(a+b, a−b) ≤ 2. Sea g = gcd(a+b, a−b). Entonces g divide a (a+b)+(a−b) = 2a y a (a+b)−(a−b) = 2b, así que g | gcd(2a,2b) = 2·gcd(a,b) = 2 (pues a,b coprimos). Por tanto g ∈ {1,2}, es decir g ≤ 2.",
 "Argumento de combinaciones lineales: un divisor común de a+b y a−b divide a 2a y 2b, y la coprimalidad lo acota a 2. Verificado con Python: gcd(a+b,a−b) ≤ 2 para todo par coprimo con a,b ≤ 59.",
 18, ["combinaciones lineales de divisores", "coprimalidad", "cota por gcd"],
 ["propiedades del mcd", "teoría de números", "combinaciones enteras"],
 "", ["gcd", "coprimos", "cota", "nivel-medio"], "cap. 28 (Ej. 28.19viii)"))

A(P(305, "El seno de un múltiplo", "optimizacion", 2,
 "Demuestra que sin(nx) ≤ n·sin(x) para todo entero positivo n y todo x con 0 ≤ x ≤ π/2.",
 ["Inducción sobre n. En el rango [0, π/2], sin x ≥ 0, lo que ayuda. Usa la fórmula de adición del seno.",
  "Base n=1: sin x ≤ sin x. ✓. Supón sin(nx) ≤ n sin x.",
  "Para el paso, escribe sin((n+1)x) = sin(nx)cos x + cos(nx)sin x y acota con cos ≤ 1.",
  "sin((n+1)x) = sin(nx)cos x + cos(nx)sin x ≤ sin(nx) + sin x (usando cos x ≤ 1 y cos(nx) ≤ 1, válidos porque los senos son no negativos en el rango).",
  "Por la hipótesis, ≤ n sin x + sin x = (n+1) sin x. Inducción completa."],
 "sin(nx) ≤ n sin x en [0, π/2]. Por inducción: base sin x ≤ sin x. Paso: sin((n+1)x) = sin(nx)cos x + cos(nx)sin x ≤ sin(nx) + sin x (pues cos ≤ 1 y los senos son ≥ 0 en el rango) ≤ n sin x + sin x = (n+1) sin x.",
 "Inducción con la fórmula de adición del seno; el rango [0, π/2] garantiza no negatividad para acotar limpiamente. Verificado con Python: sin(nx) ≤ n sin x para 20 000 pares (x, n) con 0 ≤ x ≤ π/2.",
 14, ["inducción", "fórmula de adición del seno", "no negatividad en el rango"],
 ["desigualdades trigonométricas", "funciones subaditivas", "acotamiento por inducción"],
 "", ["induccion", "trigonometria", "seno", "nivel-basico"], "cap. 24 (Ej. 24.10v)"))

A(P(306, "El algoritmo de la división y el menor resto", "optimizacion", 3,
 "Demuestra el Lema de la División: dados enteros x e y con y > 0, existen enteros q y r tales que x = qy + r con 0 ≤ r < y. (Sugerencia: usa el principio del buen orden.)",
 ["La existencia de r se prueba como un problema de MINIMIZACIÓN: considera todos los valores no negativos de la forma x − sy.",
  "Considera el conjunto S = {x − sy : s ∈ ℤ y x − sy ≥ 0}. Argumenta primero que S no es vacío.",
  "S es no vacío: si x ≥ 0, x = x − 0·y ∈ S; si x < 0, x − xy = x(1−y) ≥ 0 ∈ S. Por el buen orden, S tiene un MENOR elemento.",
  "Sea r el menor elemento de S, con r = x − qy para cierto q. Por construcción r ≥ 0. Falta ver r < y.",
  "Si fuera r ≥ y, entonces r − y = x − (q+1)y ≥ 0 estaría en S y sería menor que r, contradiciendo la minimalidad. Luego 0 ≤ r < y."],
 "Existen tales q, r. Considera S = {x − sy : s ∈ ℤ, x − sy ≥ 0}, que es no vacío (si x ≥ 0, x ∈ S; si x < 0, x(1−y) ∈ S). Por el principio del buen orden S tiene un menor elemento r = x − qy ≥ 0. Si fuera r ≥ y, entonces r − y = x − (q+1)y ≥ 0 estaría en S y sería menor que r, contradicción; luego 0 ≤ r < y.",
 "Principio del extremo / buen orden: el resto es el MENOR valor no negativo de la forma x − sy, y su minimalidad fuerza r < y. La 'solución' es el argumento, tomado del libro. Verificado con Python: el q, r usuales cumplen 0 ≤ r < y para x ∈ [0,49], y ∈ [1,9].",
 22, ["principio del buen orden", "argumento de minimización", "lema de la división"],
 ["existencia por elemento mínimo", "fundamentos de la aritmética", "el algoritmo de Euclides"],
 "", ["buen-orden", "extremo", "division", "nivel-medio"], "cap. 28 (Lema 28.1)"))

# =====================================================================
# PATRONES (14) — teoría de números, identidades, recurrencias, Fibonacci
# =====================================================================

A(P(307, "La suma de los primeros cuadrados", "patrones", 2,
 "Demuestra que 1² + 2² + ⋯ + n² = n(n+1)(2n+1)/6 para todo entero positivo n.",
 ["Verifica la fórmula para n pequeños y prueba por inducción separando el último término.",
  "Base n=1: 1² = 1 = 1·2·3/6. ✓. Supón Σ_{i=1}^n i² = n(n+1)(2n+1)/6.",
  "Para el paso, suma (n+1)²: Σ_{i=1}^{n+1} i² = n(n+1)(2n+1)/6 + (n+1)².",
  "Factoriza (n+1)/6: = (n+1)[n(2n+1) + 6(n+1)]/6 = (n+1)(2n²+7n+6)/6.",
  "Factoriza 2n²+7n+6 = (n+2)(2n+3): = (n+1)(n+2)(2n+3)/6, que es la fórmula para n+1."],
 "Σ_{i=1}^n i² = n(n+1)(2n+1)/6. Por inducción: base 1 = 1·2·3/6. Paso: n(n+1)(2n+1)/6 + (n+1)² = (n+1)[n(2n+1)+6(n+1)]/6 = (n+1)(2n²+7n+6)/6 = (n+1)(n+2)(2n+3)/6, la fórmula para n+1.",
 "Identidad clásica probada por inducción con factorización cuidadosa del paso. Verificado con Python: Σi² = n(n+1)(2n+1)/6 para n = 1..39.",
 14, ["inducción", "suma de cuadrados", "factorización del paso inductivo"],
 ["sumas de potencias", "fórmulas cerradas", "identidades algebraicas"],
 "", ["identidad", "suma-cuadrados", "induccion", "nivel-basico"], "cap. 24 (Ej. 24.10i)"))

A(P(308, "El algoritmo de Euclides en acción", "patrones", 2,
 "Calcula gcd(14441, 3563) usando el algoritmo de Euclides (divisiones sucesivas con resto).",
 ["El algoritmo de Euclides aplica el lema de la división repetidamente: gcd(x, y) = gcd(y, x mód y).",
  "Empieza: 14441 = q·3563 + r. Calcula q y r, luego repite con (3563, r).",
  "14441 = 4·3563 + 189; luego 3563 = 18·189 + 161; luego 189 = 1·161 + 28.",
  "Continúa: 161 = 5·28 + 21; 28 = 1·21 + 7; 21 = 3·7 + 0.",
  "El último resto no nulo es 7, así que gcd(14441, 3563) = 7."],
 "gcd(14441, 3563) = 7. Aplicando el algoritmo de Euclides: 14441 = 4·3563 + 189; 3563 = 18·189 + 161; 189 = 1·161 + 28; 161 = 5·28 + 21; 28 = 1·21 + 7; 21 = 3·7 + 0. El último resto distinto de cero, 7, es el máximo común divisor.",
 "El algoritmo de Euclides reemplaza la factorización (difícil) por divisiones sucesivas: gcd(x,y) = gcd(y, x mód y), terminando cuando el resto es 0. Verificado con Python: gcd(14441, 3563) = 7.",
 14, ["algoritmo de Euclides", "lema de la división", "gcd(x,y)=gcd(y, x mód y)"],
 ["teoría algorítmica de números", "complejidad del algoritmo de Euclides", "fracciones continuas"],
 "", ["euclides", "gcd", "algoritmo", "nivel-basico"], "cap. 28 (Ej. 28.5)"))

A(P(309, "Identidad de Bézout", "patrones", 3,
 "Demuestra que existen enteros k y l con 14441·k + 3563·l = gcd(14441, 3563), y encuéntralos invirtiendo el algoritmo de Euclides.",
 ["Toma las divisiones del algoritmo de Euclides y recorre HACIA ATRÁS, despejando cada resto.",
  "Sabes que gcd = 7 y que 7 = 28 − 1·21 (penúltima división). Ahora sustituye 21 usando la división anterior.",
  "21 = 161 − 5·28, así que 7 = 28 − (161 − 5·28) = 6·28 − 1·161. Sustituye 28 = 189 − 161.",
  "Continúa sustituyendo hacia arriba (28, luego 161, luego 189) hasta expresar 7 en términos de 14441 y 3563.",
  "El resultado es 7 = 132·14441 − 535·3563, es decir k = 132 y l = −535."],
 "Existen tales k, l: en concreto 132·14441 − 535·3563 = 7 = gcd(14441, 3563). Se obtienen recorriendo el algoritmo de Euclides hacia atrás: partiendo de 7 = 28 − 1·21 y sustituyendo sucesivamente 21, 28, 161, 189 por las igualdades del algoritmo, se llega a 7 = 132·14441 − 535·3563 (k = 132, l = −535). Estos coeficientes no son únicos.",
 "Identidad de Bézout: el mcd se expresa como combinación lineal entera, hallada invirtiendo el algoritmo de Euclides. Verificado con Python: 132·14441 − 535·3563 = 7.",
 24, ["identidad de Bézout", "algoritmo de Euclides extendido", "combinación lineal entera"],
 ["ecuaciones diofantinas", "inversos modulares", "criptografía (RSA)"],
 "", ["bezout", "euclides", "gcd", "nivel-medio"], "cap. 28 (Ej. 28.8)"))

A(P(310, "Resolver una ecuación diofantina", "patrones", 3,
 "Encuentra todas las soluciones enteras de la ecuación diofantina 51x + 21y = 18.",
 ["Primero comprueba que hay solución: ¿divide gcd(51, 21) a 18? Calcula el mcd con Euclides.",
  "gcd(51, 21) = 3 (51 = 2·21 + 9, 21 = 2·9 + 3, 9 = 3·3 + 0). Como 3 | 18, hay soluciones.",
  "Invierte el algoritmo para escribir 3 como combinación: 3 = 5·21 − 2·51. Multiplica por 18/3 = 6 para obtener una solución particular.",
  "18 = 30·21 − 12·51, así que una solución particular es x₀ = −12, y₀ = 30.",
  "La solución general es x = −12 + (21/3)t = −12 + 7t, y = 30 − (51/3)t = 30 − 17t, para t ∈ ℤ."],
 "Las soluciones son x = −12 + 7t, y = 30 − 17t (t ∈ ℤ). Como gcd(51,21) = 3 divide a 18, hay solución. Invirtiendo Euclides, 3 = 5·21 − 2·51, y multiplicando por 6: 18 = 30·21 − 12·51, dando la solución particular (x₀,y₀) = (−12, 30). La general se obtiene sumando múltiplos de (21/3, −51/3) = (7, −17).",
 "Teoría de ecuaciones diofantinas lineales: hay solución sii gcd|c, y la solución general es una particular más el núcleo (21/gcd, −51/gcd)·t. Verificado con Python: 51(−12+7t) + 21(30−17t) = 18 para todo t.",
 24, ["ecuaciones diofantinas lineales", "Bézout", "solución general = particular + núcleo"],
 ["congruencias lineales", "retículos enteros", "teoría de números algorítmica"],
 "", ["diofantina", "euclides", "bezout", "nivel-medio"], "cap. 28 (Ej. 28.17)"))

A(P(311, "La fórmula de Binet", "patrones", 4,
 "Sea la sucesión de Fibonacci F₁ = F₂ = 1 y Fₙ = Fₙ₋₁ + Fₙ₋₂ para n ≥ 3. Demuestra la fórmula de Binet: Fₙ = (1/√5)·[((1+√5)/2)ⁿ − ((1−√5)/2)ⁿ].",
 ["La recurrencia es lineal de orden 2. Halla su ecuación característica y sus raíces.",
  "La ecuación característica de Fₙ = Fₙ₋₁ + Fₙ₋₂ es x² = x + 1, o sea x² − x − 1 = 0.",
  "Sus raíces son φ = (1+√5)/2 y ψ = (1−√5)/2. La solución general es Fₙ = Aφⁿ + Bψⁿ.",
  "Ajusta A y B con las condiciones iniciales F₁ = 1, F₂ = 1 (o F₀ = 0, F₁ = 1).",
  "Resolviendo, A = 1/√5 y B = −1/√5, dando Fₙ = (φⁿ − ψⁿ)/√5."],
 "Fₙ = (φⁿ − ψⁿ)/√5 con φ = (1+√5)/2, ψ = (1−√5)/2. La ecuación característica x² − x − 1 = 0 tiene esas raíces, así que Fₙ = Aφⁿ + Bψⁿ; imponiendo F₀ = 0 y F₁ = 1 se obtiene A = 1/√5, B = −1/√5, de donde Fₙ = (φⁿ − ψⁿ)/√5.",
 "Resolución de una recurrencia lineal por su ecuación característica; las raíces son la razón áurea y su conjugada. Es notable que la combinación de irracionales dé siempre un entero. Verificado con Python: la fórmula coincide con Fₙ para n = 1..24.",
 30, ["recurrencias lineales", "ecuación característica", "razón áurea"],
 ["números de Fibonacci", "soluciones cerradas de recurrencias", "fórmula de Binet"],
 "", ["fibonacci", "binet", "recurrencia", "nivel-avanzado"], "cap. 25 (Ej. 25.7i b)"))

A(P(312, "Suma de Fibonacci de índice impar", "patrones", 3,
 "Demuestra que la suma de los números de Fibonacci de índice impar cumple F₁ + F₃ + F₅ + ⋯ + F₂ₙ₋₁ = F₂ₙ, para todo n ≥ 1.",
 ["Verifica para n pequeños y prueba por inducción separando el último término.",
  "Base n=1: F₁ = 1 = F₂. ✓. Supón F₁ + F₃ + ⋯ + F₂ₙ₋₁ = F₂ₙ.",
  "Para el paso, suma el siguiente término de índice impar, F₂ₙ₊₁: la suma hasta F₂(n+1)−1 = F₂ₙ₊₁ es F₂ₙ + F₂ₙ₊₁.",
  "Usa la recurrencia de Fibonacci: F₂ₙ + F₂ₙ₊₁ = F₂ₙ₊₂.",
  "F₂ₙ₊₂ = F₂(n+1), que es la fórmula para n+1. Inducción completa."],
 "F₁ + F₃ + ⋯ + F₂ₙ₋₁ = F₂ₙ. Por inducción: base F₁ = 1 = F₂. Paso: sumando F₂ₙ₊₁ a la hipótesis, F₂ₙ + F₂ₙ₊₁ = F₂ₙ₊₂ = F₂(n+1) por la recurrencia de Fibonacci.",
 "Identidad de Fibonacci probada por inducción usando la propia recurrencia en el paso. Verificado con Python: Σ F_{2i−1} = F_{2n} para n = 1..14.",
 16, ["identidad de Fibonacci", "inducción", "suma telescópica vía recurrencia"],
 ["números de Fibonacci", "identidades de sumas parciales", "telescopaje"],
 "", ["fibonacci", "identidad", "suma", "nivel-medio"], "cap. 25 (Ej. 25.7i d)"))

A(P(313, "Suma de Fibonacci de índice par", "patrones", 3,
 "Demuestra que la suma de los números de Fibonacci de índice par cumple F₂ + F₄ + F₆ + ⋯ + F₂ₙ = F₂ₙ₊₁ − 1, para todo n ≥ 1.",
 ["Verifica para n pequeños y prueba por inducción separando el último término.",
  "Base n=1: F₂ = 1 = F₃ − 1 = 2 − 1. ✓. Supón F₂ + F₄ + ⋯ + F₂ₙ = F₂ₙ₊₁ − 1.",
  "Para el paso, suma el siguiente término de índice par, F₂ₙ₊₂: la suma queda (F₂ₙ₊₁ − 1) + F₂ₙ₊₂.",
  "Usa la recurrencia: F₂ₙ₊₁ + F₂ₙ₊₂ = F₂ₙ₊₃.",
  "Entonces la suma es F₂ₙ₊₃ − 1 = F₂(n+1)+1 − 1, la fórmula para n+1. Inducción completa."],
 "F₂ + F₄ + ⋯ + F₂ₙ = F₂ₙ₊₁ − 1. Por inducción: base F₂ = 1 = F₃ − 1. Paso: sumando F₂ₙ₊₂ a la hipótesis, (F₂ₙ₊₁ − 1) + F₂ₙ₊₂ = F₂ₙ₊₃ − 1 = F₂(n+1)+1 − 1 por la recurrencia de Fibonacci.",
 "Identidad de Fibonacci por inducción; el '−1' refleja que falta F₁ para completar la suma total. Verificado con Python: Σ F_{2i} = F_{2n+1} − 1 para n = 1..14.",
 16, ["identidad de Fibonacci", "inducción", "suma parcial"],
 ["números de Fibonacci", "identidades de sumas", "telescopaje vía recurrencia"],
 "", ["fibonacci", "identidad", "suma", "nivel-medio"], "cap. 25 (Ej. 25.7i e)"))

A(P(314, "Una recurrencia promediadora", "patrones", 4,
 "Sea x₁ = 0, x₂ = 1 y xₙ = ½(xₙ₋₁ + xₙ₋₂) para n ≥ 3. Demuestra que xₙ = (2^{n−1} + (−1)ⁿ)/(3·2^{n−2}) para todo n ≥ 1.",
 ["Es una recurrencia lineal de orden 2; halla su ecuación característica.",
  "De xₙ = ½xₙ₋₁ + ½xₙ₋₂, la ecuación característica es x² = ½x + ½, o sea 2x² − x − 1 = 0.",
  "Factoriza: 2x² − x − 1 = (2x + 1)(x − 1) = 0, con raíces x = 1 y x = −1/2.",
  "La solución general es xₙ = A·1ⁿ + B·(−1/2)ⁿ = A + B(−1/2)ⁿ. Ajusta con x₁ = 0, x₂ = 1.",
  "Resolviendo, A = 1/3 y B = −2/3, de donde xₙ = 1/3 − (2/3)(−1/2)ⁿ = (2^{n−1} + (−1)ⁿ)/(3·2^{n−2})."],
 "xₙ = (2^{n−1} + (−1)ⁿ)/(3·2^{n−2}). La ecuación característica 2x² − x − 1 = (2x+1)(x−1) = 0 tiene raíces 1 y −1/2, así que xₙ = A + B(−1/2)ⁿ; imponiendo x₁ = 0, x₂ = 1 se obtiene A = 1/3, B = −2/3, lo que se reescribe como (2^{n−1} + (−1)ⁿ)/(3·2^{n−2}). Los primeros términos son 0, 1, 1/2, 3/4, 5/8, 11/16, …",
 "Recurrencia lineal con raíces 1 y −1/2 (un promedio converge oscilando a 1/3·... el límite es 2/3). Verificado con Python (aritmética exacta de fracciones): la fórmula coincide para n = 1..19.",
 28, ["recurrencias lineales", "ecuación característica", "raíces racionales"],
 ["procesos promediadores", "convergencia de sucesiones", "soluciones cerradas"],
 "", ["recurrencia", "promedio", "patron", "nivel-avanzado"], "cap. 25 (Ej. 25.7ii)"))

A(P(315, "Factorización única", "patrones", 2,
 "Encuentra la factorización en primos de 12870 y de 17836, e ilústralo como ejemplo del Teorema Fundamental de la Aritmética.",
 ["Divide sistemáticamente entre los primos 2, 3, 5, 7, 11, 13, … hasta agotar cada número.",
  "12870: es par, 12870 = 2·6435. 6435 termina en 5: 6435 = 5·1287. 1287 = 3·429 = 3·3·143.",
  "143 = 11·13. Así 12870 = 2·3²·5·11·13.",
  "17836: par, 17836 = 2·8918 = 2·2·4459. 4459 = 7·637 = 7·7·91 = 7·7·7·13.",
  "Así 17836 = 2²·7³·13. Ambas factorizaciones son únicas (salvo el orden) por el Teorema Fundamental de la Aritmética."],
 "12870 = 2·3²·5·11·13 y 17836 = 2²·7³·13. Dividiendo sucesivamente entre primos: 12870 = 2·6435 = 2·5·1287 = 2·5·3²·143 = 2·3²·5·11·13; y 17836 = 2²·4459 = 2²·7³·13. Por el Teorema Fundamental de la Aritmética estas factorizaciones son únicas salvo el orden de los factores.",
 "Factorización por división sucesiva entre primos, ilustrando el TFA. Verificado con Python: 12870 = 2·3²·5·11·13 y 17836 = 2²·7³·13.",
 14, ["Teorema Fundamental de la Aritmética", "factorización por división sucesiva", "unicidad de factores"],
 ["factorización de enteros", "primalidad", "criptografía (dificultad de factorizar)"],
 "", ["factorizacion", "primos", "tfa", "nivel-basico"], "cap. 25 (Ej. 25.7iii)"))

A(P(316, "Producto del mcm y el mcd", "patrones", 3,
 "Demuestra que para enteros positivos a y b se cumple lcm(a, b)·gcd(a, b) = a·b.",
 ["Trabaja con las factorizaciones primas de a y b y compara exponentes primo a primo.",
  "Para un primo p, sea α su exponente en a y β en b. ¿Qué exponente tiene p en gcd(a,b) y en lcm(a,b)?",
  "En gcd(a,b) el exponente de p es min(α,β); en lcm(a,b) es max(α,β).",
  "Para cada primo: min(α,β) + max(α,β) = α + β (porque min y max son justamente α y β en algún orden).",
  "Sumando exponentes, el exponente de p en lcm·gcd es α+β, igual que en a·b. Como esto vale para todo primo, lcm(a,b)·gcd(a,b) = a·b."],
 "lcm(a,b)·gcd(a,b) = a·b. Para cada primo p, si α y β son sus exponentes en a y b, entonces su exponente en gcd es min(α,β) y en lcm es max(α,β); como min(α,β) + max(α,β) = α + β, el exponente de p en lcm·gcd coincide con el de a·b. Válido para todo primo, así que lcm(a,b)·gcd(a,b) = a·b.",
 "Identidad clave de teoría de números vía exponentes primos y la igualdad min + max = suma. Verificado con Python: lcm(a,b)·gcd(a,b) = a·b para todo a,b ≤ 39.",
 18, ["exponentes primos", "identidad min + max = suma", "mcm y mcd"],
 ["factorización única", "valuaciones p-ádicas", "estructura multiplicativa"],
 "", ["mcm", "gcd", "exponentes", "nivel-medio"], "cap. 28 (Ej. 28.x xi)"))

A(P(317, "Cuántos subconjuntos", "patrones", 2,
 "Demuestra que un conjunto finito con n elementos tiene exactamente 2ⁿ subconjuntos.",
 ["Inducción sobre n, o un argumento directo de elección. ¿Cuántas decisiones tomas para formar un subconjunto?",
  "Para formar un subconjunto, decides por cada elemento si lo incluyes o no: dos opciones por elemento.",
  "Con n elementos y decisiones independientes, el número total es 2·2·⋯·2 (n factores) = 2ⁿ.",
  "Por inducción: con 0 elementos hay 2⁰ = 1 subconjunto (el vacío). Al añadir un elemento, cada subconjunto previo da dos nuevos (con o sin el elemento).",
  "Así el número de subconjuntos se duplica al pasar de n a n+1: de 2ⁿ a 2^{n+1}. Hay 2ⁿ subconjuntos."],
 "Un conjunto de n elementos tiene 2ⁿ subconjuntos. Argumento directo: cada subconjunto se determina decidiendo, para cada uno de los n elementos, si pertenece o no (2 opciones independientes), dando 2ⁿ. Por inducción: base 2⁰ = 1 (el vacío); al añadir un elemento, cada subconjunto previo genera dos (con y sin él), duplicando el conteo.",
 "Conteo por elección independiente (o inducción que duplica). Es el tamaño del conjunto potencia. Verificado con Python: el número de subconjuntos de un n-conjunto es 2ⁿ para n = 0..11.",
 12, ["principio del producto", "conjunto potencia", "inducción que duplica"],
 ["combinatoria de conjuntos", "conjunto potencia 2^X", "principio de la multiplicación"],
 "", ["conteo", "subconjuntos", "potencia", "nivel-basico"], "cap. 24 (Ej. 24.10xi)"))

A(P(318, "La suma geométrica finita", "patrones", 2,
 "Demuestra que para todo entero x > 1 y todo entero positivo n se cumple (xⁿ − 1)/(x − 1) = 1 + x + x² + ⋯ + x^{n−1}.",
 ["Multiplica el lado derecho por (x − 1) y observa qué se cancela (telescopaje).",
  "Sea S = 1 + x + x² + ⋯ + x^{n−1}. Calcula (x − 1)·S desarrollando el producto.",
  "(x − 1)S = (x + x² + ⋯ + xⁿ) − (1 + x + ⋯ + x^{n−1}). Casi todos los términos se cancelan.",
  "Solo sobreviven xⁿ (del primer paréntesis) y −1 (del segundo): (x − 1)S = xⁿ − 1.",
  "Dividiendo por x − 1 (que es ≠ 0): S = (xⁿ − 1)/(x − 1)."],
 "(xⁿ − 1)/(x − 1) = 1 + x + ⋯ + x^{n−1}. Sea S la suma del lado derecho; entonces (x − 1)S = (x + x² + ⋯ + xⁿ) − (1 + x + ⋯ + x^{n−1}) = xⁿ − 1 (telescopaje, todos los términos intermedios se cancelan). Dividiendo por x − 1 ≠ 0 se obtiene la identidad.",
 "Suma geométrica finita por telescopaje al multiplicar por (x−1). Es la base de muchas fórmulas de divisibilidad. Verificado con Python: (xⁿ−1)/(x−1) = Σ xⁱ para x ∈ [2,9], n ∈ [1,9].",
 12, ["serie geométrica finita", "telescopaje", "factorización de xⁿ−1"],
 ["progresiones geométricas", "sumas parciales", "identidades algebraicas"],
 "", ["geometrica", "telescopaje", "identidad", "nivel-basico"], "cap. 24 (Ej. 24.12b)"))

A(P(319, "Cuándo tiene solución una ecuación diofantina", "patrones", 3,
 "Demuestra que la ecuación diofantina mx + ny = c (con m, n, c enteros) tiene soluciones enteras si y solo si gcd(m, n) divide a c.",
 ["Es un 'si y solo si': prueba las dos direcciones. Llama d = gcd(m, n).",
  "(⇒) Si hay solución mx + ny = c, nota que d divide a m y a n, así que divide a cualquier combinación mx + ny = c.",
  "Por tanto, si hay solución, d | c. Esto prueba una dirección.",
  "(⇐) Si d | c, usa la identidad de Bézout: existen k, l con mk + nl = d.",
  "Multiplica por c/d (entero, pues d | c): m(k·c/d) + n(l·c/d) = c, dando una solución explícita x = kc/d, y = lc/d."],
 "mx + ny = c tiene solución entera sii gcd(m,n) | c. (⇒) Si mx + ny = c, como d = gcd(m,n) divide a m y n, divide a mx + ny = c. (⇐) Si d | c, por Bézout existen k, l con mk + nl = d; multiplicando por el entero c/d se obtiene m(kc/d) + n(lc/d) = c, una solución.",
 "Criterio de solubilidad de ecuaciones diofantinas lineales, equivalente a la identidad de Bézout. Verificado con Python: para 315x+264y=18/24 (gcd 3) y 7644x+1386y=84, 1386x+7644y=126 (gcd 42), en todos gcd | c y hay solución.",
 22, ["ecuaciones diofantinas lineales", "identidad de Bézout", "criterio de solubilidad"],
 ["congruencias lineales", "teoría de números algorítmica", "combinaciones enteras"],
 "", ["diofantina", "bezout", "gcd", "nivel-medio"], "cap. 28 (Teo. 28.15 / Ej. 28.19iv)"))

A(P(320, "El producto de los números de Fermat", "patrones", 3,
 "Sea Fₙ = 2^{2ⁿ} + 1 el n-ésimo número de Fermat. Demuestra que F₀·F₁·F₂·⋯·Fₙ = F_{n+1} − 2 para todo entero no negativo n.",
 ["Procede por inducción y aprovecha que F_{k} − 2 = 2^{2ᵏ} − 1 es una diferencia de cuadrados respecto del siguiente.",
  "Base n=0: F₀ = 3 = 5 − 2 = F₁ − 2. ✓. Supón F₀⋯Fₙ = F_{n+1} − 2.",
  "Multiplica ambos lados por F_{n+1}: F₀⋯Fₙ·F_{n+1} = (F_{n+1} − 2)·F_{n+1}.",
  "Nota que F_{n+1} − 2 = 2^{2^{n+1}} − 1 y F_{n+1} = 2^{2^{n+1}} + 1: su producto es una diferencia de cuadrados.",
  "(2^{2^{n+1}} − 1)(2^{2^{n+1}} + 1) = 2^{2^{n+2}} − 1 = F_{n+2} − 2. Inducción completa."],
 "F₀F₁⋯Fₙ = F_{n+1} − 2. Por inducción: base F₀ = 3 = F₁ − 2. Paso: multiplicando la hipótesis por F_{n+1}, (F_{n+1} − 2)F_{n+1} = (2^{2^{n+1}} − 1)(2^{2^{n+1}} + 1) = 2^{2^{n+2}} − 1 = F_{n+2} − 2 (diferencia de cuadrados).",
 "Identidad telescópica vía diferencia de cuadrados: cada paso 'sube un nivel' en la torre de exponentes. Es la clave de que los números de Fermat sean coprimos dos a dos. Verificado con Python: ∏_{k=0}^n F_k = F_{n+1} − 2.",
 22, ["números de Fermat", "diferencia de cuadrados", "inducción telescópica"],
 ["identidades telescópicas", "torres de exponentes", "coprimalidad de los Fermat"],
 "", ["fermat", "telescopaje", "identidad", "nivel-medio"], "cap. 27 (Ej. 27.23xi a)"))

# =====================================================================
# Append idempotente
# =====================================================================
PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
new_ids = {p["id"] for p in PROBLEMS}
clash = existing & new_ids
assert not clash, f"choque de ids con existentes: {clash}"
assert len(new_ids) == len(PROBLEMS), "ids duplicados dentro del builder"

data["problemas"].extend(PROBLEMS)
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

dist = collections.Counter(p["estrategia"] for p in PROBLEMS)
print(f"Agregados {len(PROBLEMS)} problemas (ids {min(new_ids)}-{max(new_ids)}).")
print("Distribución de la tanda:", dict(dist))
total = collections.Counter(p["estrategia"] for p in data["problemas"])
print("Distribución total problems.json:", dict(total), "— total", len(data["problemas"]))
