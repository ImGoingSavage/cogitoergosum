# -*- coding: utf-8 -*-
"""Tanda 38 — David Patrick, *Intermediate Counting & Probability* (Art of Problem Solving).
Append 44 problemas verificados a data/problems.json. El PDF (81 MB) NO tiene capa de
texto (es imagen pura); el TOC y secciones de ejercicio se leyeron como IMÁGENES con la
tool Read (caps. 3 PIE y 7 Distributions confirmados). Cada número se verifica de forma
independiente con Python (math.comb/factorial, fractions; 44 checks, todos OK). Capítulos:
 - cap. 3 «A Piece of PIE» (inclusión-exclusión) y cap. 12 «Combinatorial Identities».
 - cap. 5 «Pigeonhole Principle».
 - cap. 6 «Constructive Expectation» (linealidad de la esperanza) y cap. 11 «Conditional
   Probability» (Bayes, Monty Hall).
 - cap. 7 «Distributions» (estrellas y barras), cap. 9 «Fibonacci», cap. 10 «Recursion»
   (Catalan), cap. 8 «Mathematical Induction», cap. 14 «Generating Functions».
Mapeo a las 4 estrategias canónicas (11 c/u, balance GLOBAL -> 146/146/146/146):
 - patrones: Fibonacci, Catalan, estrellas y barras, identidades combinatorias.
 - invariantes: PIE (cada elemento contado una vez), probabilidad condicional/total,
   linealidad de la esperanza.
 - optimizacion: principio del palomar (garantías de peor caso).
 - inversion: recurrencias (reconstruir desplegando), Bayes (razonar hacia atrás desde la
   evidencia), particiones, Monty Hall.
Builder idempotente: aborta si hay choque de ids. Sector C (entrenamiento), esquema §4.1,
ids 541-584."""
import json, collections

SRC = "Patrick, *Intermediate Counting & Probability* (Art of Problem Solving)"

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
# PATRONES (11) — Fibonacci, Catalan, estrellas y barras, identidades
# =====================================================================

A(P(541, "Subir la escalera", "patrones", 3,
 "Una escalera tiene 10 escalones. Puedes subir de 1 en 1 o de 2 en 2 escalones. ¿De cuántas maneras distintas puedes subir los 10 escalones?",
 ["Resuelve casos pequeños y busca la regularidad: ¿de cuántas formas subes 1, 2, 3, 4 escalones?",
  "1 escalón: 1 forma; 2: 2 formas; 3: 3; 4: 5; 5: 8. Cada número es la suma de los dos anteriores.",
  "Es la sucesión de Fibonacci: el número de formas de subir n escalones es F(n+1).",
  "Para n = 10 necesitas F(11).",
  "F: 1,1,2,3,5,8,13,21,34,55,89 → F(11) = 89."],
 "El número de formas de subir n escalones (pasos de 1 o 2) cumple la recurrencia de Fibonacci: f(n) = f(n−1) + f(n−2). Para n = 10 da 89. Verificado con Python.",
 "El último paso es de 1 o de 2 escalones, así que f(n) = f(n−1) + f(n−2): exactamente Fibonacci. Reconocer el patrón evita enumerar las 89 secuencias.",
 14, ["sucesión de Fibonacci", "recurrencia", "casos base"],
 ["conteo de teselados", "modelos de población", "algoritmos recursivos"],
 "", ["fibonacci", "conteo", "patron", "nivel-intermedio"], "cap. 9 (Fibonacci Numbers)"))

A(P(542, "Cadenas sin unos seguidos", "patrones", 3,
 "¿Cuántas cadenas binarias (de 0s y 1s) de longitud 8 NO tienen dos unos consecutivos?",
 ["Cuenta para longitudes pequeñas y busca el patrón.",
  "Longitud 1: 2; longitud 2: 3 (todas menos '11'); longitud 3: 5; longitud 4: 8.",
  "Otra vez Fibonacci: el conteo para longitud n es F(n+2).",
  "Para n = 8 necesitas F(10).",
  "F(10) = 55."],
 "El número de cadenas binarias de longitud n sin '11' consecutivos es F(n+2); para n = 8 da F(10) = 55. Verificado con Python.",
 "Si la cadena termina en 0, las primeras n−1 son libres (sin '11'); si termina en 1, la anterior debe ser 0. Eso da la recurrencia de Fibonacci.",
 14, ["Fibonacci", "cadenas binarias", "recurrencia"],
 ["códigos sin patrones prohibidos", "autómatas", "teoría de la información"],
 "", ["fibonacci", "conteo", "patron", "nivel-intermedio"], "cap. 9 (Fibonacci Numbers)"))

A(P(543, "Paréntesis bien formados", "patrones", 4,
 "¿De cuántas maneras se pueden colocar 4 pares de paréntesis de forma que queden correctamente balanceados? (Por ejemplo, ()()()  y  (((())))  son válidos.)",
 ["Cuenta para pocos pares y busca la sucesión: 1 par → 1, 2 pares → 2, 3 pares → 5.",
  "La sucesión 1, 2, 5, 14, 42, … son los números de Catalan.",
  "El n-ésimo número de Catalan es C(2n, n)/(n + 1).",
  "Para n = 4 pares: C(8, 4)/5.",
  "= 70/5 = 14."],
 "El número de secuencias de n pares de paréntesis balanceados es el n-ésimo Catalan C_n = C(2n,n)/(n+1); para n = 4 da 70/5 = 14. Verificado con Python.",
 "Los números de Catalan cuentan estructuras 'que nunca se pasan de la raya': paréntesis balanceados, caminos que no cruzan la diagonal, triangulaciones. La fórmula es C(2n,n)/(n+1).",
 18, ["números de Catalan", "paréntesis balanceados", "C(2n,n)/(n+1)"],
 ["análisis sintáctico", "árboles binarios", "estructuras de datos"],
 "", ["catalan", "conteo", "patron", "nivel-avanzado"], "cap. 10 (Catalan Numbers)"))

A(P(544, "Triangular un hexágono", "patrones", 4,
 "¿De cuántas maneras se puede dividir un hexágono convexo (6 lados) en triángulos trazando diagonales que no se crucen? (Una triangulación usa diagonales que solo se tocan en los vértices.)",
 ["Cuenta para polígonos pequeños: triángulo → 1, cuadrilátero → 2, pentágono → 5.",
  "La sucesión 1, 2, 5, 14, … son de nuevo los números de Catalan.",
  "El número de triangulaciones de un polígono de (n + 2) lados es el n-ésimo Catalan C_n.",
  "Un hexágono tiene 6 = 4 + 2 lados, así que necesitas C_4.",
  "C_4 = C(8,4)/5 = 14."],
 "El número de triangulaciones de un polígono de n+2 lados es C_n. Para el hexágono (n=4) da C_4 = 14. Verificado con Python.",
 "Las triangulaciones de polígonos son uno de los muchos disfraces de los números de Catalan, que aparecen una y otra vez en combinatoria.",
 18, ["números de Catalan", "triangulaciones", "polígono convexo"],
 ["geometría computacional", "árboles de expresión", "mallas"],
 "", ["catalan", "geometria", "patron", "nivel-avanzado"], "cap. 10 (Catalan Numbers)"))

A(P(545, "Repartir dinero, todos al menos uno", "patrones", 3,
 "¿Cuántas soluciones en enteros positivos tiene la ecuación a + b + c + d = 17?",
 ["Es un problema de 'estrellas y barras': repartir 17 unidades entre 4 variables, cada una ≥ 1.",
  "Imagina 17 estrellas en fila; para dividirlas en 4 grupos necesitas 3 barras.",
  "Las barras van en los huecos ENTRE estrellas (17 − 1 = 16 huecos), uno por hueco como máximo.",
  "Elige 3 de los 16 huecos: C(16, 3).",
  "= 560."],
 "Por estrellas y barras, las soluciones positivas de a+b+c+d = 17 son C(16,3) = 560. Verificado con Python.",
 "Estrellas y barras: repartir n unidades entre k variables positivas equivale a poner k−1 barras en los n−1 huecos, es decir C(n−1, k−1).",
 14, ["estrellas y barras", "soluciones enteras positivas", "C(n−1,k−1)"],
 ["asignación de recursos", "ecuaciones diofánticas", "particiones"],
 "", ["estrellas-barras", "conteo", "patron", "nivel-intermedio"], "cap. 7 (Prob. 7.4)"))

A(P(546, "Soluciones no negativas", "patrones", 3,
 "¿Cuántas soluciones en enteros NO negativos tiene v + w + x + y + z = 21? (Las variables pueden ser 0.)",
 ["Las variables pueden valer 0, así que ajusta el truco de estrellas y barras para permitir grupos vacíos.",
  "Sustituye v' = v + 1, etc.: las nuevas variables son positivas y suman 21 + 5 = 26.",
  "Ahora cuenta soluciones positivas de la suma 26 con 5 variables: C(26 − 1, 5 − 1).",
  "= C(25, 4).",
  "= 12650."],
 "Sumando 1 a cada variable, el problema se vuelve positivo con suma 26: C(25,4) = 12650. (Equivale a C(n+k−1, k−1).) Verificado con Python.",
 "Para soluciones no negativas se usa C(n+k−1, k−1): basta 'prestar' una unidad a cada variable para reducirlo al caso positivo.",
 14, ["estrellas y barras", "soluciones no negativas", "C(n+k−1,k−1)"],
 ["distribución con ceros", "diofánticas", "combinatoria"],
 "", ["estrellas-barras", "conteo", "patron", "nivel-intermedio"], "cap. 7 (Prob. 7.5)"))

A(P(547, "Once paletas, seis niños", "patrones", 2,
 "¿De cuántas maneras puedo repartir 11 paletas idénticas entre 6 niños si cada niño debe recibir al menos una paleta?",
 ["Estrellas y barras: 11 paletas en fila, separadas en 6 grupos por barras.",
  "Para 6 grupos necesitas 5 barras.",
  "Las barras van en los 11 − 1 = 10 huecos entre paletas, uno por hueco.",
  "Elige 5 de los 10 huecos: C(10, 5).",
  "= 252."],
 "Por estrellas y barras, las formas de repartir 11 paletas entre 6 niños (cada uno ≥ 1) son C(10,5) = 252. Verificado con Python.",
 "Cada reparto equivale a elegir dónde poner las barras separadoras entre las paletas. La fórmula C(n−1, k−1) cuenta esas elecciones.",
 12, ["estrellas y barras", "reparto positivo", "C(n−1,k−1)"],
 ["distribución equitativa", "asignación", "combinatoria"],
 "", ["estrellas-barras", "conteo", "patron", "nivel-basico"], "cap. 7 (Prob. 7.2)"))

A(P(548, "La identidad de Vandermonde", "patrones", 3,
 "Calcula C(4,0)·C(3,2) + C(4,1)·C(3,1) + C(4,2)·C(3,0) y relaciónalo con una sola combinación.",
 ["Piensa: ¿de cuántas formas eliges 2 personas de un grupo de 4 hombres y 3 mujeres? Separa por cuántos hombres eliges.",
  "La identidad de Vandermonde: ∑ₖ C(m,k)·C(n,r−k) = C(m+n, r).",
  "Aquí m = 4, n = 3, r = 2.",
  "La suma vale C(4+3, 2) = C(7, 2).",
  "= 21. (Comprueba: 1·3 + 4·3 + 6·1 = 21.)"],
 "Por la identidad de Vandermonde, ∑ C(4,k)C(3,2−k) = C(7,2) = 21 (= 1·3 + 4·3 + 6·1). Verificado con Python.",
 "Vandermonde cuenta lo mismo de dos formas: elegir r de m+n directamente, o separar según cuántos vienen del primer grupo. El patrón resume la suma en una combinación.",
 14, ["identidad de Vandermonde", "doble conteo", "combinaciones"],
 ["convolución combinatoria", "probabilidad hipergeométrica", "álgebra"],
 "", ["identidades", "conteo", "patron", "nivel-intermedio"], "cap. 12 (Combinatorial Identities)"))

A(P(549, "Suma de cuadrados de combinaciones", "patrones", 3,
 "Calcula C(4,0)² + C(4,1)² + C(4,2)² + C(4,3)² + C(4,4)² y relaciónalo con una sola combinación.",
 ["Hay una identidad célebre para la suma de los cuadrados de una fila de Pascal.",
  "∑ₖ C(n,k)² = C(2n, n) (caso especial de Vandermonde con m = n, r = n).",
  "Aquí n = 4.",
  "= C(8, 4).",
  "= 70. (Comprueba: 1 + 16 + 36 + 16 + 1 = 70.)"],
 "∑ C(4,k)² = C(8,4) = 70 (= 1 + 16 + 36 + 16 + 1). Verificado con Python.",
 "Como C(n,k) = C(n,n−k), la suma de cuadrados es ∑ C(n,k)C(n,n−k) = C(2n,n) por Vandermonde: elegir n de 2n separando por el primer grupo.",
 14, ["suma de cuadrados de binomios", "∑C(n,k)²=C(2n,n)", "Vandermonde"],
 ["identidades combinatorias", "probabilidad", "álgebra"],
 "", ["identidades", "pascal", "patron", "nivel-intermedio"], "cap. 12 (Combinatorial Identities)"))

A(P(550, "Suma de los primeros Fibonacci", "patrones", 2,
 "Si F₁ = 1, F₂ = 1, F₃ = 2, … es la sucesión de Fibonacci, calcula F₁ + F₂ + ⋯ + F₁₀.",
 ["Suma los primeros términos y busca una relación con otro Fibonacci.",
  "Hay una identidad: F₁ + F₂ + ⋯ + Fₙ = F₍ₙ₊₂₎ − 1.",
  "Para n = 10 necesitas F₁₂ − 1.",
  "F₁₂ = 144.",
  "Suma = 144 − 1 = 143."],
 "Por la identidad de la suma parcial de Fibonacci, F₁ + ⋯ + F₁₀ = F₁₂ − 1 = 144 − 1 = 143. Verificado con Python.",
 "La suma de los primeros n Fibonacci es F(n+2) − 1: un patrón que telescopa usando F(k) = F(k+2) − F(k+1).",
 12, ["Fibonacci", "suma parcial", "identidad F(n+2)−1"],
 ["series", "análisis de algoritmos", "identidades"],
 "", ["fibonacci", "series", "patron", "nivel-basico"], "cap. 9 (Fibonacci Numbers)"))

A(P(551, "Cien repartido entre tres", "patrones", 2,
 "¿Cuántas soluciones en enteros positivos tiene a + b + c = 100?",
 ["Estrellas y barras con 100 unidades y 3 variables positivas.",
  "Necesitas 2 barras para dividir las 100 estrellas en 3 grupos.",
  "Las barras van en los 100 − 1 = 99 huecos entre estrellas.",
  "Elige 2 de los 99 huecos: C(99, 2).",
  "= 4851."],
 "Por estrellas y barras, las soluciones positivas de a+b+c = 100 son C(99,2) = 4851. Verificado con Python.",
 "El mismo patrón de estrellas y barras: C(n−1, k−1) cuenta los repartos positivos. Para tres variables, son C(n−1, 2).",
 10, ["estrellas y barras", "soluciones positivas", "C(n−1,2)"],
 ["diofánticas", "particiones", "asignación"],
 "", ["estrellas-barras", "conteo", "patron", "nivel-basico"], "cap. 7 (Prob. 7.2.3)"))

# =====================================================================
# INVARIANTES (11) — PIE, prob. condicional/total, linealidad de la esperanza
# =====================================================================

A(P(552, "Lacrosse o futbol", "invariantes", 2,
 "En un grupo de estudiantes, 18 juegan lacrosse, 12 juegan futbol y 6 juegan ambos. ¿Cuántos juegan al menos uno de los dos deportes?",
 ["Si sumas los dos grupos cuentas dos veces a quienes juegan ambos: hay que corregirlo.",
  "Inclusión-exclusión: |A ∪ B| = |A| + |B| − |A ∩ B|.",
  "= 18 + 12 − 6.",
  "= 24.",
  "Juegan al menos uno: 24 estudiantes."],
 "Por inclusión-exclusión, |lacrosse ∪ futbol| = 18 + 12 − 6 = 24. Verificado con Python.",
 "El principio de inclusión-exclusión (PIE) garantiza que cada elemento se cuente exactamente una vez: se resta la intersección que el doble conteo agregó de más.",
 10, ["inclusión-exclusión", "unión de conjuntos", "doble conteo"],
 ["bases de datos", "estadística de encuestas", "conjuntos"],
 "", ["pie", "conjuntos", "invariante", "nivel-basico"], "cap. 3 (PIE With 2 Properties)"))

A(P(553, "Múltiplos de 2, 3 o 5", "invariantes", 3,
 "¿Cuántos enteros del 1 al 100 son divisibles por 2, por 3 o por 5?",
 ["Usa inclusión-exclusión con los tres conjuntos de múltiplos.",
  "Múltiplos de 2: 50; de 3: 33; de 5: 20.",
  "Resta las intersecciones: múltiplos de 6: 16; de 10: 10; de 15: 6.",
  "Suma la triple intersección: múltiplos de 30: 3.",
  "50 + 33 + 20 − 16 − 10 − 6 + 3 = 74."],
 "Por PIE: 50 + 33 + 20 − 16 − 10 − 6 + 3 = 74 enteros divisibles por 2, 3 o 5. Verificado con Python.",
 "Con tres conjuntos, PIE alterna signos: suma individuales, resta pares, suma la triple. Así cada múltiplo se cuenta una sola vez.",
 14, ["inclusión-exclusión", "divisibilidad", "tres conjuntos"],
 ["criba de Eratóstenes", "teoría de números", "conteo"],
 "", ["pie", "divisibilidad", "invariante", "nivel-intermedio"], "cap. 3 (PIE With 3 Properties)"))

A(P(554, "Ni dos ni cinco", "invariantes", 2,
 "¿Cuántos enteros del 1 al 100 NO son divisibles ni por 2 ni por 5?",
 ["Cuenta el complemento con PIE: los divisibles por 2 o por 5, y resta del total.",
  "Divisibles por 2 o por 5 = 50 + 20 − (divisibles por 10) = 50 + 20 − 10 = 60.",
  "El total es 100.",
  "Los que NO son divisibles ni por 2 ni por 5 = 100 − 60.",
  "= 40."],
 "Divisibles por 2 o 5 = 50 + 20 − 10 = 60 (PIE); los que no = 100 − 60 = 40. Verificado con Python.",
 "Combinar PIE con conteo complementario: cuenta los 'malos' (divisibles por 2 o 5) con inclusión-exclusión y réstalos del total invariante.",
 12, ["inclusión-exclusión", "conteo complementario", "divisibilidad"],
 ["función phi de Euler", "criba", "teoría de números"],
 "", ["pie", "complementario", "invariante", "nivel-basico"], "cap. 3 (PIE)"))

A(P(555, "Nadie en su lugar", "invariantes", 4,
 "Cuatro personas dejan su sombrero en el guardarropa y al salir cada una toma un sombrero al azar. ¿De cuántas maneras puede ocurrir que NINGUNA persona reciba su propio sombrero?",
 ["Cuenta el complemento con PIE: las permutaciones que SÍ fijan al menos a alguien.",
  "Total de permutaciones de 4: 4! = 24. Resta las que tienen algún punto fijo (alguien con su sombrero).",
  "Por PIE: fijos = C(4,1)·3! − C(4,2)·2! + C(4,3)·1! − C(4,4)·0! = 24 − 12 + 4 − 1 = 15.",
  "Sin ningún punto fijo = 24 − 15 = 9. (Es el número de 'desarreglos' D₄.)",
  "La respuesta es 9."],
 "Los desarreglos de 4 elementos son D₄ = 4!(1 − 1/1! + 1/2! − 1/3! + 1/4!) = 9 (también 24 − 15 por PIE). Verificado con Python.",
 "Un desarreglo es una permutación sin puntos fijos. PIE sobre los eventos 'la persona i recibe su sombrero' da la fórmula alternante de los desarreglos.",
 18, ["desarreglos", "inclusión-exclusión", "permutaciones sin punto fijo"],
 ["criptografía", "asignación aleatoria", "combinatoria"],
 "", ["pie", "desarreglos", "invariante", "nivel-avanzado"], "cap. 3 (PIE)"))

A(P(556, "Palabras con vocal en los extremos", "invariantes", 3,
 "¿Cuántas 'palabras' de 4 letras (cualquier secuencia del alfabeto de 26) comienzan o terminan con vocal? (Vocales: A, E, I, O, U.)",
 ["'O' sugiere inclusión-exclusión: cuenta las que empiezan con vocal, las que terminan con vocal, y resta las que cumplen ambas.",
  "Empiezan con vocal: 5·26³. Terminan con vocal: 26³·5.",
  "Cumplen ambas (empiezan y terminan con vocal): 5·26²·5 = 25·26².",
  "PIE: 5·26³ + 5·26³ − 25·26².",
  "= 87880 + 87880 − 16900 = 158860."],
 "Por PIE: 5·26³ + 5·26³ − 25·26² = 175760 − 16900 = 158860. Verificado con Python.",
 "PIE evita el doble conteo de las palabras que empiezan Y terminan con vocal, restando esa intersección una vez.",
 14, ["inclusión-exclusión", "conteo de palabras", "intersección"],
 ["validación de cadenas", "criptografía", "combinatoria"],
 "", ["pie", "conteo", "invariante", "nivel-intermedio"], "cap. 3 (Prob. 3.25)"))

A(P(557, "Puntos fijos esperados", "invariantes", 4,
 "Se baraja al azar una permutación de los números 1, 2, …, 10. ¿Cuál es el número esperado de posiciones i en las que aparece el número i (puntos fijos)?",
 ["Usa la linealidad de la esperanza: define una variable indicadora por cada posición.",
  "Sea Xᵢ = 1 si la posición i tiene al número i, y 0 si no. El total de puntos fijos es X₁ + ⋯ + X₁₀.",
  "E[Xᵢ] = P(la posición i tiene al número i) = 1/10.",
  "Por linealidad, E[total] = 10 · (1/10).",
  "= 1."],
 "Por linealidad de la esperanza, E[puntos fijos] = ∑ E[Xᵢ] = 10·(1/10) = 1, sin importar n. Verificado con Python (simulación/cálculo).",
 "La linealidad de la esperanza es invariante: E[suma] = suma de E, aunque las variables no sean independientes. El número esperado de puntos fijos es siempre 1.",
 16, ["linealidad de la esperanza", "variables indicadoras", "puntos fijos"],
 ["análisis de algoritmos", "muestreo aleatorio", "probabilidad"],
 "", ["esperanza", "linealidad", "invariante", "nivel-avanzado"], "cap. 6 (Constructive Expectation)"))

A(P(558, "Caras esperadas en cien lanzamientos", "invariantes", 1,
 "Se lanza una moneda equilibrada 100 veces. ¿Cuál es el número esperado de caras?",
 ["Usa la linealidad de la esperanza sobre cada lanzamiento.",
  "Cada lanzamiento aporta 1 cara con probabilidad 1/2, es decir esperanza 1/2.",
  "Hay 100 lanzamientos independientes.",
  "E[total] = 100 · (1/2).",
  "= 50."],
 "Por linealidad, E[caras] = 100·(1/2) = 50. Verificado con Python.",
 "La esperanza de una suma es la suma de las esperanzas: 100 lanzamientos, cada uno con esperanza 1/2, dan 50. Es la esperanza de una binomial: np.",
 8, ["linealidad de la esperanza", "binomial", "esperanza np"],
 ["control de calidad", "muestreo", "estadística"],
 "", ["esperanza", "linealidad", "invariante", "nivel-basico"], "cap. 6 (Constructive Expectation)"))

A(P(559, "Probabilidad condicional con dados", "invariantes", 3,
 "Se lanzan dos dados equilibrados. Dado que el PRIMER dado muestra un número par, ¿cuál es la probabilidad de que la suma sea 7?",
 ["Probabilidad condicional: P(suma 7 | primer par) = P(suma 7 Y primer par)/P(primer par).",
  "El primer dado par (2, 4, 6) ocurre con probabilidad 1/2 (18 de 36 resultados).",
  "Para suma 7 con primer par: (2,5), (4,3), (6,1) → 3 resultados favorables.",
  "P(suma 7 y primer par) = 3/36 = 1/12.",
  "P = (1/12)/(1/2) = 1/6."],
 "P(suma 7 | primer par) = (3/36)/(18/36) = 3/18 = 1/6. Verificado con Python.",
 "Condicionar reduce el espacio muestral a los 18 casos con primer dado par; entre ellos, 3 dan suma 7. La probabilidad condicional reparte sobre ese subconjunto invariante.",
 12, ["probabilidad condicional", "espacio reducido", "P(A|B)"],
 ["diagnóstico", "filtrado de eventos", "inferencia"],
 "", ["condicional", "probabilidad", "invariante", "nivel-intermedio"], "cap. 11 (Conditional Probability)"))

A(P(560, "La bola verde", "invariantes", 3,
 "El recipiente I tiene 8 bolas rojas y 4 verdes. Los recipientes II y III tienen cada uno 2 rojas y 4 verdes. Se elige un recipiente al azar y luego una bola al azar de él. ¿Cuál es la probabilidad de que la bola sea verde?",
 ["Usa la ley de la probabilidad total: promedia la probabilidad de verde en cada recipiente, ponderando por elegirlo.",
  "Cada recipiente se elige con probabilidad 1/3.",
  "P(verde | I) = 4/12 = 1/3; P(verde | II) = P(verde | III) = 4/6 = 2/3.",
  "P(verde) = (1/3)(1/3) + (1/3)(2/3) + (1/3)(2/3).",
  "= 1/9 + 2/9 + 2/9 = 5/9."],
 "Por probabilidad total, P(verde) = (1/3)(1/3) + (1/3)(2/3) + (1/3)(2/3) = 5/9. Verificado con Python.",
 "La ley de la probabilidad total descompone un evento según una partición del espacio (el recipiente elegido) y promedia las condicionales. Las probabilidades de la partición suman 1.",
 14, ["probabilidad total", "partición del espacio", "promedio ponderado"],
 ["modelos de mezcla", "diagnóstico", "árboles de decisión"],
 "", ["probabilidad-total", "condicional", "invariante", "nivel-intermedio"], "cap. 11 (Conditional Probability)"))

A(P(561, "Divisibles por 7 u 11", "invariantes", 3,
 "¿Cuántos números de tres cifras (del 100 al 999) son divisibles por 7 o por 11?",
 ["Inclusión-exclusión con los múltiplos de 7 y de 11 en el rango de tres cifras.",
  "Múltiplos de 7 entre 100 y 999: ⌊999/7⌋ − ⌊99/7⌋ = 142 − 14 = 128.",
  "Múltiplos de 11: ⌊999/11⌋ − ⌊99/11⌋ = 90 − 9 = 81.",
  "Múltiplos de 77 (=7·11): ⌊999/77⌋ − ⌊99/77⌋ = 12 − 1 = 11.",
  "PIE: 128 + 81 − 11 = 198."],
 "Por PIE: 128 (múltiplos de 7) + 81 (de 11) − 11 (de 77) = 198. Verificado con Python.",
 "PIE con divisibilidad: la intersección 'divisible por 7 y por 11' es 'divisible por 77' (mcm de primos). Restarla evita el doble conteo.",
 14, ["inclusión-exclusión", "divisibilidad", "conteo en rango"],
 ["criba", "teoría de números", "filtros"],
 "", ["pie", "divisibilidad", "invariante", "nivel-intermedio"], "cap. 3 (PIE)"))

A(P(562, "Suma esperada de dos dados", "invariantes", 1,
 "Se lanzan dos dados equilibrados de 6 caras. ¿Cuál es el valor esperado de la suma de los dos resultados?",
 ["Usa la linealidad de la esperanza: la esperanza de la suma es la suma de las esperanzas.",
  "El valor esperado de un solo dado es (1+2+3+4+5+6)/6 = 3.5.",
  "Hay dos dados.",
  "E[suma] = 3.5 + 3.5.",
  "= 7."],
 "Por linealidad, E[suma] = E[dado₁] + E[dado₂] = 3.5 + 3.5 = 7. Verificado con Python.",
 "La linealidad de la esperanza permite sumar las esperanzas de cada dado sin analizar la distribución conjunta de la suma. El promedio de un dado es 3.5.",
 8, ["linealidad de la esperanza", "valor esperado de un dado", "suma"],
 ["juegos de azar", "estadística", "simulación"],
 "", ["esperanza", "linealidad", "invariante", "nivel-basico"], "cap. 6 / 1 (Expected Value)"))

# =====================================================================
# OPTIMIZACION (11) — principio del palomar (garantías de peor caso)
# =====================================================================

A(P(563, "Mismo residuo módulo cuatro", "optimizacion", 2,
 "¿Cuántos enteros hay que elegir (sin importar cuáles) para GARANTIZAR que dos de ellos dejen el mismo residuo al dividirse entre 4?",
 ["Los 'casilleros' son los posibles residuos módulo 4.",
  "Al dividir entre 4, los residuos posibles son 0, 1, 2 y 3: cuatro casilleros.",
  "En el peor caso eliges cuatro enteros con residuos todos distintos.",
  "El quinto entero repite forzosamente un residuo.",
  "Se necesitan 4 + 1 = 5 enteros."],
 "Hay 4 residuos posibles módulo 4; por el palomar, 5 enteros garantizan dos con el mismo residuo. Verificado por conteo de casilleros.",
 "El principio del palomar: con más objetos que casilleros (residuos), dos comparten casillero. Aquí 4 residuos ⇒ 5 enteros bastan.",
 10, ["principio del palomar", "residuos módulo 4", "peor caso"],
 ["funciones hash", "garantías de colisión", "teoría de números"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 5 (Pigeonhole Principle)"))

A(P(564, "Tres del mismo palo", "optimizacion", 2,
 "De una baraja estándar (4 palos), ¿cuántas cartas hay que sacar para GARANTIZAR que haya 3 cartas del mismo palo?",
 ["Piensa en el peor caso: ¿cuántas cartas puedes tener con a lo más 2 de cada palo?",
  "Hay 4 palos; en el peor caso sacas 2 de cada uno: 8 cartas sin lograr 3 iguales.",
  "La novena carta, sea del palo que sea, completa un trío.",
  "Palomar generalizado: 4·(3 − 1) + 1.",
  "= 8 + 1 = 9 cartas."],
 "En el peor caso se sacan 2 de cada palo (8 cartas); la 9.ª completa un trío. Se necesitan 9. Verificado por el palomar generalizado.",
 "Palomar generalizado: para garantizar k del mismo tipo con c tipos, hacen falta c(k−1)+1 objetos. Aquí 4·2+1 = 9.",
 10, ["palomar generalizado", "palos de baraja", "peor caso"],
 ["garantías de muestreo", "tolerancia a fallos", "combinatoria"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 5 (Pigeonhole Principle)"))

A(P(565, "Suma nueve", "optimizacion", 2,
 "Del conjunto {1, 2, 3, 4, 5, 6, 7, 8}, ¿cuántos números hay que elegir para GARANTIZAR que dos de ellos sumen 9?",
 ["Agrupa los números en parejas que sumen 9: esos son los casilleros.",
  "Parejas que suman 9: (1,8), (2,7), (3,6), (4,5): cuatro parejas que cubren los 8 números.",
  "En el peor caso eliges uno de cada pareja: 4 números sin sumar 9.",
  "El quinto número cae en una pareja ya iniciada.",
  "Se necesitan 4 + 1 = 5 números."],
 "Hay 4 parejas que suman 9; por el palomar, 5 números garantizan una pareja completa. Verificado por conteo de casilleros.",
 "La clave del palomar es elegir bien los casilleros: las parejas complementarias que suman 9. Con 4 casilleros, 5 objetos fuerzan una coincidencia.",
 12, ["principio del palomar", "parejas complementarias", "suma fija"],
 ["teoría de Ramsey", "diseño de pruebas", "combinatoria"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 5 (Pigeonhole Principle)"))

A(P(566, "Diferencia múltiplo de nueve", "optimizacion", 3,
 "¿Cuántos enteros hay que elegir para GARANTIZAR que dos de ellos difieran en un múltiplo de 9?",
 ["Dos números difieren en un múltiplo de 9 exactamente cuando dejan el mismo residuo al dividir entre 9.",
  "Los casilleros son los residuos módulo 9: hay 9 de ellos (0 a 8).",
  "En el peor caso eliges 9 enteros con residuos distintos.",
  "El décimo repite un residuo, así que su diferencia con otro es múltiplo de 9.",
  "Se necesitan 9 + 1 = 10 enteros."],
 "Diferir en múltiplo de 9 ⇔ mismo residuo módulo 9; hay 9 residuos, así que 10 enteros garantizan dos con el mismo residuo. Verificado por conteo.",
 "Traducir 'diferencia múltiplo de m' a 'mismo residuo módulo m' convierte el problema en palomar con m casilleros: se necesitan m+1 objetos.",
 12, ["principio del palomar", "residuos módulo 9", "diferencias"],
 ["aritmética modular", "garantías", "teoría de números"],
 "", ["palomar", "optimizacion", "nivel-intermedio"], "cap. 5 (Pigeonhole Principle)"))

A(P(567, "Cuatro del mismo palo", "optimizacion", 2,
 "De una baraja estándar (4 palos), ¿cuántas cartas hay que sacar para GARANTIZAR que haya 4 cartas del mismo palo?",
 ["Peor caso: a lo más 3 de cada palo sin lograr 4.",
  "Con 4 palos, en el peor caso sacas 3 de cada uno: 12 cartas.",
  "La carta número 13 completa un grupo de 4 de algún palo.",
  "Palomar generalizado: 4·(4 − 1) + 1.",
  "= 12 + 1 = 13 cartas."],
 "En el peor caso se sacan 3 de cada palo (12 cartas); la 13.ª completa un grupo de 4. Se necesitan 13. Verificado por el palomar generalizado.",
 "El palomar generalizado c(k−1)+1 escala con k: para 4 del mismo palo, 4·3+1 = 13.",
 10, ["palomar generalizado", "palos de baraja", "garantía"],
 ["muestreo", "control de calidad", "combinatoria"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 5 (Pigeonhole Principle)"))

A(P(568, "Uno divide a otro", "optimizacion", 4,
 "Del conjunto {1, 2, 3, …, 10}, ¿cuántos números hay que elegir para GARANTIZAR que entre los elegidos uno sea múltiplo de otro?",
 ["Escribe cada número como (potencia de 2)·(parte impar). Los casilleros son las partes impares.",
  "Las partes impares posibles en 1–10 son 1, 3, 5, 7, 9: cinco casilleros.",
  "Dos números con la misma parte impar cumplen que uno divide al otro (difieren solo en potencias de 2).",
  "En el peor caso eliges 5 números con partes impares distintas; el sexto repite una parte impar.",
  "Se necesitan 5 + 1 = 6 números."],
 "Cada número es 2ᵃ·(impar); hay 5 partes impares (1,3,5,7,9) en 1–10. Por el palomar, 6 números garantizan dos con la misma parte impar, donde uno divide al otro. Verificado por conteo de cadenas.",
 "El truco (de Erdős) es agrupar por la parte impar: dentro de cada cadena {m, 2m, 4m, …} uno divide a otro. Con 5 cadenas, 6 números fuerzan dos en la misma.",
 18, ["principio del palomar", "parte impar", "cadenas de divisibilidad"],
 ["teoría de números", "combinatoria extremal", "diseño"],
 "", ["palomar", "optimizacion", "nivel-avanzado"], "cap. 5 (Pigeonhole Principle)"))

A(P(569, "Cuatro del mismo mes", "optimizacion", 2,
 "¿Cuántas personas debe haber para GARANTIZAR que al menos 4 cumplan años en el mismo mes?",
 ["Hay 12 meses; usa el palomar generalizado para garantizar 4 en un mismo casillero.",
  "En el peor caso, cada mes tiene a lo más 3 personas: 12·3 = 36 personas sin llegar a 4 en ninguno.",
  "La persona número 37 lleva algún mes a 4.",
  "Palomar generalizado: 12·(4 − 1) + 1.",
  "= 36 + 1 = 37 personas."],
 "En el peor caso 3 personas por mes (36); la 37.ª lleva un mes a 4. Se necesitan 37. Verificado por el palomar generalizado.",
 "El palomar generalizado: para k en un casillero con c casilleros, c(k−1)+1. Aquí 12·3+1 = 37.",
 10, ["palomar generalizado", "meses", "garantía"],
 ["planificación", "garantías estadísticas", "combinatoria"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 5 (Pigeonhole Principle)"))

A(P(570, "Dos consecutivos", "optimizacion", 3,
 "Del conjunto {1, 2, 3, …, 20}, ¿cuántos números hay que elegir para GARANTIZAR que dos de ellos sean consecutivos?",
 ["Piensa en el mayor subconjunto SIN números consecutivos: ese es el peor caso.",
  "El mayor conjunto sin consecutivos toma uno sí y uno no: {1, 3, 5, …, 19}, que tiene 10 números.",
  "Con 10 números podrías evitar todos los consecutivos.",
  "El número 11 forzosamente queda junto a alguno.",
  "Se necesitan 10 + 1 = 11 números."],
 "El mayor subconjunto sin consecutivos de {1..20} tiene 10 elementos ({1,3,…,19}); por el palomar, 11 números garantizan dos consecutivos. Verificado por construcción del peor caso.",
 "Aquí los 'casilleros' son las 10 parejas {1,2},{3,4},…,{19,20}: elegir 11 de 20 fuerza dos en una misma pareja, es decir consecutivos.",
 12, ["principio del palomar", "números consecutivos", "peor caso"],
 ["teoría de Ramsey", "combinatoria", "diseño de pruebas"],
 "", ["palomar", "optimizacion", "nivel-intermedio"], "cap. 5 (Pigeonhole Principle)"))

A(P(571, "Suma diez", "optimizacion", 3,
 "Del conjunto {1, 2, 3, …, 9}, ¿cuántos números hay que elegir para GARANTIZAR que dos de ellos sumen 10?",
 ["Agrupa en parejas que suman 10 y trata al sobrante por separado.",
  "Parejas que suman 10: (1,9), (2,8), (3,7), (4,6). El número 5 no tiene pareja (5+5 no son dos distintos).",
  "Casilleros: 4 parejas + el singleton {5} = 5 casilleros.",
  "En el peor caso eliges uno de cada pareja y además el 5: 5 números sin sumar 10.",
  "El sexto número completa una pareja: se necesitan 5 + 1 = 6 números."],
 "Hay 4 parejas que suman 10 más el 5 solitario: 5 casilleros. Por el palomar, 6 números garantizan una pareja que suma 10. Verificado por conteo de casilleros.",
 "Cuidado con el elemento sin pareja (el 5): cuenta como casillero propio. Con 5 casilleros, 6 objetos fuerzan dos en una pareja completa.",
 12, ["principio del palomar", "parejas complementarias", "elemento sin pareja"],
 ["combinatoria", "diseño de pruebas", "teoría de Ramsey"],
 "", ["palomar", "optimizacion", "nivel-intermedio"], "cap. 5 (Pigeonhole Principle)"))

A(P(572, "Suma diecisiete", "optimizacion", 3,
 "Del conjunto {1, 2, 3, …, 16}, ¿cuántos números hay que elegir para GARANTIZAR que dos de ellos sumen 17?",
 ["Agrupa los 16 números en parejas que sumen 17.",
  "Parejas: (1,16), (2,15), (3,14), …, (8,9): exactamente 8 parejas que cubren los 16 números.",
  "En el peor caso eliges uno de cada pareja: 8 números sin sumar 17.",
  "El noveno número completa una pareja.",
  "Se necesitan 8 + 1 = 9 números."],
 "Hay 8 parejas que suman 17; por el palomar, 9 números garantizan una pareja que suma 17. Verificado por conteo de casilleros.",
 "Cuando todos los elementos se emparejan perfectamente (aquí 8 parejas), elegir más de la mitad fuerza dos en la misma pareja.",
 12, ["principio del palomar", "parejas complementarias", "suma fija"],
 ["combinatoria", "teoría de Ramsey", "diseño"],
 "", ["palomar", "optimizacion", "nivel-intermedio"], "cap. 5 (Pigeonhole Principle)"))

A(P(573, "Cinco puntos en el cuadrado", "optimizacion", 4,
 "Se colocan 5 puntos dentro (o en el borde) de un cuadrado de lado 2. Demuestra que el principio del palomar garantiza que dos de ellos están a distancia menor o igual que √2. ¿En cuántas regiones se divide el cuadrado para lograr la garantía?",
 ["Divide el cuadrado de lado 2 en cuadraditos iguales que sirvan de casilleros.",
  "Divídelo en 4 cuadrados de lado 1 (una cuadrícula 2×2): cuatro casilleros.",
  "Con 5 puntos y 4 cuadraditos, por el palomar dos puntos caen en el mismo cuadrado de lado 1.",
  "La mayor distancia dentro de un cuadrado de lado 1 es su diagonal, √2.",
  "Por tanto esos dos puntos están a distancia ≤ √2. Se usan 4 regiones."],
 "Dividiendo el cuadrado de lado 2 en 4 cuadrados de lado 1, con 5 puntos dos caen en el mismo (palomar); su distancia ≤ diagonal = √2. Se usan 4 regiones. Verificado por el argumento del palomar.",
 "El palomar geométrico: partir la figura en regiones de diámetro acotado. Con más puntos que regiones, dos comparten región y quedan cerca (≤ el diámetro de la región).",
 16, ["palomar geométrico", "diagonal de cuadrado", "diámetro de región"],
 ["geometría combinatoria", "empaquetamiento", "diseño espacial"],
 "", ["palomar", "geometria", "optimizacion", "nivel-avanzado"], "cap. 5 (Pigeonhole Principle)"))

# =====================================================================
# INVERSION (11) — recurrencias, Bayes, particiones, Monty Hall
# =====================================================================

A(P(574, "Desplegar la recurrencia", "inversion", 2,
 "Una sucesión cumple aₙ = 2·aₙ₋₁ + 1 con a₁ = 1. ¿Cuánto vale a₅?",
 ["Reconstruye la sucesión aplicando la regla paso a paso desde a₁.",
  "a₂ = 2·1 + 1 = 3.",
  "a₃ = 2·3 + 1 = 7.",
  "a₄ = 2·7 + 1 = 15.",
  "a₅ = 2·15 + 1 = 31."],
 "Desplegando: a₁=1, a₂=3, a₃=7, a₄=15, a₅=31. Verificado con Python.",
 "Una recurrencia define cada término por el anterior; reconstruir un valor lejano es desplegar la regla. (Aquí aₙ = 2ⁿ − 1.)",
 10, ["recurrencia", "desplegar paso a paso", "sucesión"],
 ["programación dinámica", "modelos iterativos", "algoritmos"],
 "", ["recurrencia", "inversion", "nivel-basico"], "cap. 10 (Recursion)"))

A(P(575, "La torre de Hanói", "inversion", 3,
 "En la Torre de Hanói con 6 discos, ¿cuál es el número mínimo de movimientos para pasar toda la torre de una varilla a otra (moviendo un disco a la vez y nunca poniendo uno grande sobre uno pequeño)?",
 ["Plantea la recurrencia: para mover n discos hay que mover n−1, luego el grande, luego otra vez n−1.",
  "Mₙ = 2·Mₙ₋₁ + 1, con M₁ = 1.",
  "Esto da Mₙ = 2ⁿ − 1.",
  "Para n = 6: 2⁶ − 1.",
  "= 64 − 1 = 63 movimientos."],
 "La recurrencia Mₙ = 2Mₙ₋₁ + 1 da Mₙ = 2ⁿ − 1; para 6 discos, 2⁶ − 1 = 63. Verificado con Python.",
 "La Torre de Hanói se resuelve pensando hacia atrás: para mover n discos hay que resolver primero el subproblema de n−1. La recurrencia se cierra en 2ⁿ − 1.",
 14, ["recurrencia", "Torre de Hanói", "2ⁿ−1"],
 ["recursión en programación", "backtracking", "complejidad"],
 "", ["recurrencia", "inversion", "nivel-intermedio"], "cap. 10 (Recursion)"))

A(P(576, "Una sucesión tipo Fibonacci", "inversion", 2,
 "Una sucesión cumple aₙ = aₙ₋₁ + aₙ₋₂, con a₁ = 2 y a₂ = 3. ¿Cuánto vale a₆?",
 ["Cada término es la suma de los dos anteriores; reconstruye hasta a₆.",
  "a₃ = 3 + 2 = 5.",
  "a₄ = 5 + 3 = 8.",
  "a₅ = 8 + 5 = 13.",
  "a₆ = 13 + 8 = 21."],
 "Desplegando: 2, 3, 5, 8, 13, 21 → a₆ = 21. Verificado con Python.",
 "Una recurrencia de segundo orden (cada término depende de los DOS anteriores) necesita dos valores iniciales; reconstruir es sumar hacia adelante.",
 10, ["recurrencia de segundo orden", "tipo Fibonacci", "desplegar"],
 ["modelos de población", "sucesiones recursivas", "algoritmos"],
 "", ["recurrencia", "fibonacci", "inversion", "nivel-basico"], "cap. 10 (Linear Recurrences)"))

A(P(577, "El cuarto número de Catalan", "inversion", 4,
 "Los números de Catalan cumplen C₀ = 1 y la recurrencia Cₙ₊₁ = C₀·Cₙ + C₁·Cₙ₋₁ + ⋯ + Cₙ·C₀. ¿Cuánto vale C₄?",
 ["Aplica la recurrencia (una convolución) paso a paso desde C₀.",
  "C₁ = C₀·C₀ = 1. C₂ = C₀C₁ + C₁C₀ = 1 + 1 = 2.",
  "C₃ = C₀C₂ + C₁C₁ + C₂C₀ = 2 + 1 + 2 = 5.",
  "C₄ = C₀C₃ + C₁C₂ + C₂C₁ + C₃C₀ = 5 + 2 + 2 + 5.",
  "= 14."],
 "Desplegando la recurrencia de convolución: C₁=1, C₂=2, C₃=5, C₄=14. (Coincide con C(8,4)/5.) Verificado con Python.",
 "La recurrencia de Catalan es una convolución: se reconstruye sumando productos de términos previos. Es el patrón de dividir una estructura en dos partes.",
 18, ["números de Catalan", "recurrencia de convolución", "desplegar"],
 ["árboles binarios", "análisis sintáctico", "combinatoria"],
 "", ["catalan", "recurrencia", "inversion", "nivel-avanzado"], "cap. 10 (Catalan Numbers)"))

A(P(578, "El test positivo", "inversion", 5,
 "Una enfermedad afecta al 1% de la población. Una prueba detecta correctamente al 90% de los enfermos (sensibilidad 90%) y da falso positivo en el 10% de los sanos. Si una persona da positivo, ¿cuál es la probabilidad de que realmente esté enferma?",
 ["Razona hacia atrás con el teorema de Bayes: de la evidencia (positivo) a la causa (enfermo).",
  "P(enfermo) = 0.01, P(+|enfermo) = 0.9, P(+|sano) = 0.1.",
  "P(+ y enfermo) = 0.01·0.9 = 0.009; P(+ y sano) = 0.99·0.1 = 0.099.",
  "P(enfermo | +) = 0.009 / (0.009 + 0.099) = 0.009/0.108.",
  "= 1/12 ≈ 8.3%."],
 "Por Bayes, P(enfermo|+) = (0.01·0.9)/(0.01·0.9 + 0.99·0.1) = 0.009/0.108 = 1/12 ≈ 8.3%. Verificado con Python.",
 "Bayes invierte la condicional: de P(+|enfermo) a P(enfermo|+). Pese a una prueba 'buena', la baja prevalencia hace que la mayoría de positivos sean falsos (paradoja de la tasa base).",
 22, ["teorema de Bayes", "tasa base", "probabilidad condicional inversa"],
 ["diagnóstico médico", "detección de fraude", "filtros de spam"],
 "", ["bayes", "condicional", "inversion", "nivel-avanzado"], "cap. 11 (Conditional Probability)"))

A(P(579, "El problema de Monty Hall", "inversion", 4,
 "En un concurso hay 3 puertas: detrás de una hay un auto y detrás de las otras dos, cabras. Eliges una puerta. El presentador, que sabe dónde está el auto, abre OTRA puerta que tiene una cabra y te ofrece cambiar a la puerta cerrada restante. ¿Cuál es la probabilidad de ganar el auto si CAMBIAS?",
 ["Razona hacia atrás incorporando la información de que el presentador siempre revela una cabra.",
  "Tu primera elección acierta el auto con probabilidad 1/3 y falla con probabilidad 2/3.",
  "Si tu elección inicial era cabra (prob 2/3), el presentador revela la otra cabra y cambiar te lleva al auto.",
  "Si tu elección inicial era el auto (prob 1/3), cambiar te aleja del auto.",
  "Por tanto, cambiar gana con probabilidad 2/3."],
 "Cambiar gana exactamente cuando la elección inicial era cabra, lo que ocurre con probabilidad 2/3. Verificado con Python (enumeración).",
 "La clave es que el presentador da información: condicionar a 'abrió una cabra' concentra la probabilidad 2/3 en la puerta no elegida. Cambiar duplica la probabilidad de ganar.",
 16, ["probabilidad condicional", "información del presentador", "razonar hacia atrás"],
 ["teoría de decisiones", "actualización bayesiana", "estrategia"],
 "", ["monty-hall", "condicional", "inversion", "nivel-avanzado"], "cap. 11 (Let's Make a Deal!)"))

A(P(580, "La moneda de dos caras", "inversion", 4,
 "Tienes dos monedas: una normal (cara/cruz) y otra con dos caras. Eliges una al azar, la lanzas y sale cara. ¿Cuál es la probabilidad de que hayas elegido la moneda de dos caras?",
 ["Razona hacia atrás con Bayes: de la evidencia (salió cara) a la causa (cuál moneda).",
  "P(dos caras) = 1/2, P(normal) = 1/2. P(cara | dos caras) = 1, P(cara | normal) = 1/2.",
  "P(cara y dos caras) = 1/2·1 = 1/2; P(cara y normal) = 1/2·1/2 = 1/4.",
  "P(dos caras | cara) = (1/2) / (1/2 + 1/4) = (1/2)/(3/4).",
  "= 2/3."],
 "Por Bayes, P(dos caras | cara) = (1/2·1)/(1/2·1 + 1/2·1/2) = (1/2)/(3/4) = 2/3. Verificado con Python.",
 "La cara observada es más 'esperable' de la moneda de dos caras, así que la evidencia desplaza la probabilidad a su favor: de 1/2 a priori sube a 2/3 a posteriori.",
 14, ["teorema de Bayes", "actualización", "probabilidad inversa"],
 ["inferencia", "diagnóstico", "aprendizaje automático"],
 "", ["bayes", "condicional", "inversion", "nivel-avanzado"], "cap. 11 (Conditional Probability)"))

A(P(581, "Al menos un niño", "inversion", 3,
 "Una familia tiene dos hijos. Sabes que al menos uno es niño (varón). Suponiendo que cada hijo es niño o niña con igual probabilidad e independientemente, ¿cuál es la probabilidad de que AMBOS sean niños?",
 ["Lista el espacio muestral de dos hijos y condiciona a la información dada.",
  "Igualmente probables: (N,N), (N,M), (M,N), (M,M) con N=niño, M=niña.",
  "'Al menos un niño' descarta (M,M): quedan 3 casos igualmente probables.",
  "De esos 3, solo (N,N) tiene ambos niños.",
  "P(ambos niños | al menos uno) = 1/3."],
 "Condicionando a 'al menos un niño', el espacio se reduce a {NN, NM, MN}; solo NN cumple. La probabilidad es 1/3. Verificado con Python.",
 "Condicionar a 'al menos uno' NO es lo mismo que fijar un hijo concreto: deja 3 casos, no 2. Por eso la respuesta es 1/3 y no 1/2 (paradoja de los dos niños).",
 12, ["probabilidad condicional", "espacio reducido", "paradoja de los dos niños"],
 ["razonamiento probabilístico", "inferencia", "estadística"],
 "", ["condicional", "inversion", "nivel-intermedio"], "cap. 11 (Conditional Probability)"))

A(P(582, "El décimo número triangular", "inversion", 2,
 "Una sucesión cumple a₀ = 0 y aₙ = aₙ₋₁ + n. ¿Cuánto vale a₁₀?",
 ["Despliega la recurrencia: cada paso suma el índice actual.",
  "a₁ = 0 + 1 = 1; a₂ = 1 + 2 = 3; a₃ = 3 + 3 = 6; …",
  "Reconoces los números triangulares: aₙ = 1 + 2 + ⋯ + n = n(n+1)/2.",
  "Para n = 10: 10·11/2.",
  "= 55."],
 "Desplegando, aₙ = 1 + 2 + ⋯ + n = n(n+1)/2; a₁₀ = 55. Verificado con Python.",
 "Resolver una recurrencia aₙ = aₙ₋₁ + n equivale a acumular una suma; aquí da los números triangulares n(n+1)/2.",
 10, ["recurrencia", "números triangulares", "n(n+1)/2"],
 ["sumas acumuladas", "análisis de algoritmos", "series"],
 "", ["recurrencia", "inversion", "nivel-basico"], "cap. 10 (Recursion)"))

A(P(583, "Particiones de cinco", "inversion", 3,
 "¿De cuántas maneras se puede escribir 5 como suma de enteros positivos, sin importar el orden de los sumandos? (Por ejemplo, 3 + 1 + 1 y 1 + 1 + 3 cuentan como la misma.)",
 ["Reconstruye sistemáticamente todas las particiones de 5, ordenando los sumandos de mayor a menor.",
  "Con un sumando: 5. Con mayor sumando 4: 4+1. Con mayor 3: 3+2, 3+1+1.",
  "Con mayor 2: 2+2+1, 2+1+1+1. Con mayor 1: 1+1+1+1+1.",
  "Lista completa: 5; 4+1; 3+2; 3+1+1; 2+2+1; 2+1+1+1; 1+1+1+1+1.",
  "Son 7 particiones."],
 "Las particiones de 5 son: 5; 4+1; 3+2; 3+1+1; 2+2+1; 2+1+1+1; 1+1+1+1+1 → 7 en total. Verificado con Python.",
 "Contar particiones requiere reconstruirlas sin repetir; ordenar los sumandos de mayor a menor evita contar dos veces la misma. p(5) = 7.",
 14, ["particiones de enteros", "enumeración sistemática", "función de partición"],
 ["funciones generadoras", "teoría de números", "combinatoria"],
 "", ["particiones", "inversion", "nivel-intermedio"], "cap. 14 (Generating Function for Partitions)"))

A(P(584, "Recurrencia lineal de segundo orden", "inversion", 3,
 "Una sucesión cumple aₙ = 3·aₙ₋₁ − 2·aₙ₋₂, con a₁ = 1 y a₂ = 2. ¿Cuánto vale a₅?",
 ["Despliega la recurrencia término a término desde los dos valores iniciales.",
  "a₃ = 3·a₂ − 2·a₁ = 3·2 − 2·1 = 4.",
  "a₄ = 3·a₃ − 2·a₂ = 3·4 − 2·2 = 8.",
  "a₅ = 3·a₄ − 2·a₃ = 3·8 − 2·4 = 16.",
  "a₅ = 16. (De hecho aₙ = 2ⁿ⁻¹.)"],
 "Desplegando: a₃=4, a₄=8, a₅=16. (La fórmula cerrada es aₙ = 2ⁿ⁻¹.) Verificado con Python.",
 "Una recurrencia lineal de segundo orden se resuelve desplegando, o hallando su fórmula cerrada vía la ecuación característica x² = 3x − 2 (raíces 1 y 2 ⇒ aₙ = 2ⁿ⁻¹).",
 12, ["recurrencia lineal", "ecuación característica", "fórmula cerrada"],
 ["sistemas dinámicos", "algoritmos", "modelos lineales"],
 "", ["recurrencia", "inversion", "nivel-intermedio"], "cap. 10 (Linear Recurrences)"))

# =====================================================================
# Validación de balance y append idempotente
# =====================================================================
assert len(PROBLEMS) == 44, len(PROBLEMS)
bal = collections.Counter(p["estrategia"] for p in PROBLEMS)
assert bal["inversion"] == bal["optimizacion"] == bal["invariantes"] == bal["patrones"] == 11, bal
ids = [p["id"] for p in PROBLEMS]
assert ids == list(range(541, 585)), ids
assert len(set(ids)) == 44

PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
clash = existing & set(ids)
assert not clash, ("choque de ids", clash)

data["problemas"].extend(PROBLEMS)
gbal = collections.Counter(p["estrategia"] for p in data["problemas"])
print("balance global tras append:", dict(gbal))
assert all(v == 146 for v in gbal.values()), gbal

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: añadidos {len(PROBLEMS)} problemas (ids {ids[0]}-{ids[-1]}). Total = {len(data['problemas'])}.")
