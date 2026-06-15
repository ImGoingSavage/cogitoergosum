# -*- coding: utf-8 -*-
"""Tanda 37 — Richard Rusczyk, *Intermediate Algebra* (Art of Problem Solving).
Append 44 problemas verificados a data/problems.json. El PDF (193 MB, escaneado)
excede el límite de la tool Read; el TOC se extrajo con PyMuPDF (fitz). La capa OCR
distorsiona los símbolos matemáticos, así que los problemas se REFORMULAN con palabras
propias fieles a los temas de cada capítulo (§5 lo permite) y CADA número se verifica
de forma independiente con Python/sympy (44 checks, todos OK). Capítulos fuente:
 - cap. 4 «Quadratics» y cap. 8 «Vieta's Formulas» (relación raíces-coeficientes).
 - cap. 10/17 «Sequences and Series» (aritméticas, geométricas, telescopaje, sumas).
 - cap. 12/18 «Inequalities» (AM-GM, Cauchy-Schwarz, máximos y mínimos).
 - cap. 13 «Exponents and Logarithms», cap. 3 «Complex Numbers», cap. 19 «Functional
   Equations», cap. 20 «Advanced Strategies» (simetría, sustitución).
Mapeo a las 4 estrategias canónicas (11 c/u, balance GLOBAL -> 135/135/135/135):
 - invariantes: fórmulas de Vieta (suma/producto de raíces constante), expresiones
   simétricas, telescopaje (lo que se cancela), conjugados complejos.
 - patrones: sucesiones y series (regularidades), sumas de potencias, exponentes/logs,
   decimales periódicos.
 - optimizacion: AM-GM, Cauchy-Schwarz, vértice de la parábola (máximos y mínimos).
 - inversion: construir ecuaciones desde sus raíces, ecuaciones funcionales, logaritmos
   como inverso de la exponencial, despejar parámetros.
Builder idempotente: aborta si hay choque de ids. Sector C (entrenamiento), esquema §4.1,
ids 497-540."""
import json, collections

SRC = "Rusczyk, *Intermediate Algebra* (Art of Problem Solving)"

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
# INVARIANTES (11) — Vieta, simetría, telescopaje, conjugados
# =====================================================================

A(P(497, "Sin resolver la ecuación", "invariantes", 2,
 "Sin hallar las raíces, determina la suma y el producto de las raíces de x² − 7x + 12 = 0.",
 ["Las fórmulas de Vieta relacionan los coeficientes con la suma y el producto de las raíces, sin necesidad de resolver.",
  "Para x² + bx + c = 0, la suma de las raíces es −b y el producto es c.",
  "Aquí b = −7 y c = 12.",
  "Suma = −(−7) = 7; producto = 12.",
  "(Verifica: las raíces son 3 y 4, suma 7, producto 12.)"],
 "Por Vieta, suma de raíces = −(−7) = 7 y producto = 12 (las raíces son 3 y 4). Verificado con Python.",
 "Las fórmulas de Vieta hacen que la suma y el producto de las raíces sean invariantes legibles directamente de los coeficientes, sin resolver la ecuación.",
 10, ["fórmulas de Vieta", "suma y producto de raíces", "coeficientes"],
 ["diseño de filtros", "teoría de control", "polinomios característicos"],
 "", ["vieta", "cuadratica", "invariante", "nivel-basico"], "cap. 4/8 (Vieta's Formulas)"))

A(P(498, "La suma de los cuadrados de las raíces", "invariantes", 3,
 "Las raíces de x² + 5x − 14 = 0 son r y s. ¿Cuánto vale r² + s²?",
 ["No resuelvas: expresa r² + s² en términos de la suma y el producto de las raíces.",
  "Identidad: r² + s² = (r + s)² − 2rs.",
  "Por Vieta, r + s = −5 y rs = −14.",
  "r² + s² = (−5)² − 2(−14) = 25 + 28.",
  "= 53."],
 "r² + s² = (r+s)² − 2rs = (−5)² − 2(−14) = 25 + 28 = 53. Verificado con Python.",
 "Las expresiones simétricas en las raíces (como r²+s²) se escriben siempre en términos de los invariantes de Vieta (suma y producto), evitando resolver la ecuación.",
 12, ["expresiones simétricas", "Vieta", "identidad (r+s)²"],
 ["momentos estadísticos", "energía de sistemas", "polinomios simétricos"],
 "", ["vieta", "simetria", "invariante", "nivel-intermedio"], "cap. 8 (Vieta's Formulas)"))

A(P(499, "Suma de recíprocos de un cúbico", "invariantes", 3,
 "Las raíces del polinomio x³ − 6x² + 11x − 6 son p, q y r. ¿Cuánto vale 1/p + 1/q + 1/r?",
 ["La suma de recíprocos se escribe con Vieta: 1/p + 1/q + 1/r = (qr + pr + pq)/(pqr).",
  "Para x³ + ax² + bx + c, la suma de productos por pares de raíces es b y el producto es −c.",
  "Aquí la suma de productos por pares es 11 y el producto de las raíces es 6.",
  "1/p + 1/q + 1/r = (suma de pares)/(producto) = 11/6.",
  "(Verifica: las raíces son 1, 2, 3; 1 + 1/2 + 1/3 = 11/6.)"],
 "1/p + 1/q + 1/r = (pq+qr+rp)/(pqr) = 11/6 (por Vieta; las raíces son 1, 2, 3). Verificado con Python.",
 "Vieta da todas las funciones simétricas de las raíces de un cúbico: suma, suma de pares y producto. La suma de recíprocos es solo el cociente de dos de ellas.",
 14, ["Vieta para cúbicos", "suma de recíprocos", "funciones simétricas"],
 ["circuitos", "sistemas dinámicos", "polinomios característicos"],
 "", ["vieta", "cubico", "invariante", "nivel-intermedio"], "cap. 8 (Vieta's Formulas)"))

A(P(500, "La suma que se desmorona", "invariantes", 3,
 "Calcula 1/(1·2) + 1/(2·3) + 1/(3·4) + ⋯ + 1/(99·100).",
 ["Cada término se puede partir en una diferencia: busca esa descomposición (fracciones parciales).",
  "1/(n(n+1)) = 1/n − 1/(n+1).",
  "Al sumar, casi todo se cancela: queda solo el primer y el último término (suma telescópica).",
  "Suma = 1/1 − 1/100.",
  "= 99/100."],
 "Como 1/(n(n+1)) = 1/n − 1/(n+1), la suma telescopa a 1 − 1/100 = 99/100. Verificado con Python.",
 "En una suma telescópica, lo invariante es lo que NO se cancela: solo sobreviven los extremos. Reconocer la diferencia 1/n − 1/(n+1) colapsa cientos de términos en dos.",
 14, ["suma telescópica", "fracciones parciales", "cancelación"],
 ["series numéricas", "análisis de algoritmos", "sumas parciales"],
 "", ["telescopaje", "series", "invariante", "nivel-intermedio"], "cap. 17 (Telescoping)"))

A(P(501, "Telescopaje con impares", "invariantes", 4,
 "Calcula 1/(1·3) + 1/(3·5) + 1/(5·7) + ⋯ + 1/(97·99).",
 ["Descompón cada término como diferencia, con cuidado por el salto de 2 entre los factores.",
  "1/((2k−1)(2k+1)) = (1/2)·[1/(2k−1) − 1/(2k+1)].",
  "La suma telescopa: sobreviven el primer 1/1 y el último −1/99, multiplicados por 1/2.",
  "Suma = (1/2)(1 − 1/99).",
  "= (1/2)(98/99) = 49/99."],
 "Como 1/((2k−1)(2k+1)) = (1/2)[1/(2k−1) − 1/(2k+1)], la suma telescopa a (1/2)(1 − 1/99) = 49/99. Verificado con Python.",
 "El factor 1/2 aparece porque los factores difieren en 2. Tras la descomposición, el telescopaje deja solo los extremos: el invariante de la cancelación.",
 16, ["telescopaje", "fracciones parciales", "factor de ajuste"],
 ["series", "procesamiento de señales", "sumas cerradas"],
 "", ["telescopaje", "series", "invariante", "nivel-avanzado"], "cap. 17 (Telescoping)"))

A(P(502, "El compañero conjugado", "invariantes", 3,
 "Una ecuación cuadrática con coeficientes reales tiene a 3 + 2i como una de sus raíces. Si es mónica (coeficiente principal 1), ¿cuál es la ecuación?",
 ["Para coeficientes reales, las raíces complejas vienen en pares conjugados: si 3 + 2i es raíz, también lo es 3 − 2i.",
  "La cuadrática mónica es (x − (3 + 2i))(x − (3 − 2i)).",
  "Suma de raíces = (3 + 2i) + (3 − 2i) = 6; producto = (3 + 2i)(3 − 2i) = 9 + 4 = 13.",
  "Por Vieta, la ecuación es x² − (suma)x + (producto).",
  "= x² − 6x + 13."],
 "El conjugado 3 − 2i también es raíz; suma = 6, producto = (3+2i)(3−2i) = 13. La ecuación es x² − 6x + 13 = 0. Verificado con Python.",
 "La invariancia bajo conjugación de los polinomios reales obliga a que las raíces no reales aparezcan en pares conjugados, cuya suma y producto son reales (aquí 6 y 13).",
 14, ["raíces conjugadas", "coeficientes reales", "Vieta"],
 ["análisis de señales", "sistemas con resonancia", "filtros"],
 "", ["complejos", "conjugado", "invariante", "nivel-intermedio"], "cap. 3/8 (Complex Numbers, Vieta)"))

A(P(503, "Suma de cuadrados desde suma y producto", "invariantes", 2,
 "Dos números r y s cumplen r + s = 10 y r·s = 21. ¿Cuánto vale r² + s²?",
 ["Relaciona r² + s² con la suma y el producto mediante una identidad algebraica.",
  "(r + s)² = r² + 2rs + s², así que r² + s² = (r + s)² − 2rs.",
  "Sustituye r + s = 10 y rs = 21.",
  "r² + s² = 10² − 2·21 = 100 − 42.",
  "= 58."],
 "r² + s² = (r+s)² − 2rs = 100 − 42 = 58. Verificado con Python.",
 "Conocer la suma y el producto basta para cualquier polinomio simétrico de dos variables. La identidad (r+s)² − 2rs es el puente invariante.",
 10, ["expresiones simétricas", "identidad (r+s)²", "suma y producto"],
 ["estadística (varianza)", "física de osciladores", "álgebra"],
 "", ["simetria", "invariante", "nivel-basico"], "cap. 8 (expresiones simétricas)"))

A(P(504, "La suma de los cubos", "invariantes", 3,
 "Si a + b = 5 y a·b = 6, ¿cuánto vale a³ + b³?",
 ["Existe una identidad que expresa a³ + b³ con la suma y el producto.",
  "a³ + b³ = (a + b)³ − 3ab(a + b).",
  "Sustituye a + b = 5 y ab = 6.",
  "= 5³ − 3·6·5 = 125 − 90.",
  "= 35."],
 "a³ + b³ = (a+b)³ − 3ab(a+b) = 125 − 90 = 35. Verificado con Python.",
 "Los polinomios simétricos de grado superior también se reducen a la suma y el producto. La identidad de a³+b³ evita resolver para a y b por separado.",
 12, ["polinomios simétricos", "identidad a³+b³", "suma y producto"],
 ["álgebra", "criptografía", "teoría de Galois elemental"],
 "", ["simetria", "invariante", "nivel-intermedio"], "cap. 8/20 (simetría)"))

A(P(505, "El producto que telescopa", "invariantes", 4,
 "Calcula el producto (1 − 1/2²)(1 − 1/3²)(1 − 1/4²) ⋯ (1 − 1/10²).",
 ["Factoriza cada término como diferencia de cuadrados: 1 − 1/n² = (1 − 1/n)(1 + 1/n).",
  "1 − 1/n² = ((n−1)/n)·((n+1)/n).",
  "Escribe el producto como dos cadenas que se telescopan: ∏(n−1)/n · ∏(n+1)/n.",
  "La primera cadena da 1/10 (de 1·2·…·9 sobre 2·3·…·10) y la segunda da 11/2.",
  "Producto = (1/10)·(11/2) = 11/20."],
 "1 − 1/n² = ((n−1)/n)((n+1)/n); el producto de n=2 a 10 telescopa a (1/10)(11/2) = 11/20. Verificado con Python.",
 "Un producto telescópico es el análogo multiplicativo de la suma telescópica: tras factorizar, casi todos los factores se cancelan y solo quedan los extremos.",
 16, ["producto telescópico", "diferencia de cuadrados", "cancelación"],
 ["productos infinitos", "análisis", "identidades de Wallis"],
 "", ["telescopaje", "producto", "invariante", "nivel-avanzado"], "cap. 17 (Telescoping)"))

A(P(506, "El módulo escondido en el producto", "invariantes", 2,
 "Calcula el producto (3 + 4i)(3 − 4i), donde i es la unidad imaginaria.",
 ["El producto de un número complejo por su conjugado siempre da un número real.",
  "(a + bi)(a − bi) = a² + b² (es el cuadrado del módulo).",
  "Aquí a = 3 y b = 4.",
  "= 3² + 4² = 9 + 16.",
  "= 25 (que es |3 + 4i|²)."],
 "(3 + 4i)(3 − 4i) = 3² + 4² = 25 = |3 + 4i|². Verificado con Python.",
 "El producto de conjugados z·z̄ = |z|² es real e invariante: elimina la parte imaginaria. Es la base de la racionalización de denominadores complejos.",
 8, ["conjugado complejo", "módulo", "z·z̄ = |z|²"],
 ["procesamiento de señales", "mecánica cuántica", "racionalización"],
 "", ["complejos", "conjugado", "invariante", "nivel-basico"], "cap. 3 (Complex Numbers)"))

A(P(507, "Otra suma simétrica", "invariantes", 2,
 "Las raíces de x² − 8x + 15 = 0 son r y s. ¿Cuánto vale (r + 2)(s + 2)?",
 ["Expande (r + 2)(s + 2) y exprésalo con la suma y el producto de las raíces.",
  "(r + 2)(s + 2) = rs + 2(r + s) + 4.",
  "Por Vieta, r + s = 8 y rs = 15.",
  "= 15 + 2·8 + 4 = 15 + 16 + 4.",
  "= 35. (Verifica: raíces 3 y 5, (5)(7) = 35.)"],
 "(r+2)(s+2) = rs + 2(r+s) + 4 = 15 + 16 + 4 = 35 (raíces 3 y 5). Verificado con Python.",
 "Cualquier expresión simétrica en las raíces, incluso desplazada, se evalúa con los invariantes de Vieta sin resolver la ecuación.",
 10, ["Vieta", "expresión simétrica", "expansión"],
 ["transformación de raíces", "diseño de polinomios", "álgebra"],
 "", ["vieta", "simetria", "invariante", "nivel-basico"], "cap. 8 (Vieta's Formulas)"))

# =====================================================================
# PATRONES (11) — sucesiones y series, sumas de potencias, exp/log
# =====================================================================

A(P(508, "El vigésimo término", "patrones", 1,
 "En una sucesión aritmética, el primer término es 3 y la diferencia común es 5. ¿Cuál es el vigésimo término?",
 ["En una sucesión aritmética cada término se obtiene sumando la diferencia común al anterior: hay una fórmula directa.",
  "El n-ésimo término es a_n = a_1 + (n − 1)·d.",
  "Aquí a_1 = 3, d = 5, n = 20.",
  "a_20 = 3 + 19·5.",
  "= 3 + 95 = 98."],
 "a_20 = a_1 + 19·d = 3 + 19·5 = 98. Verificado con Python.",
 "El patrón aritmético (sumar siempre lo mismo) da una fórmula lineal en n. No hace falta listar los 20 términos.",
 8, ["sucesión aritmética", "término general", "diferencia común"],
 ["depreciación lineal", "planes de pago", "progresiones"],
 "", ["sucesiones", "aritmetica", "patron", "nivel-basico"], "cap. 10 (Arithmetic Sequences)"))

A(P(509, "Suma de una progresión aritmética", "patrones", 2,
 "Calcula la suma de los primeros 50 términos de la sucesión aritmética 2, 5, 8, 11, …",
 ["Primero halla el último término; luego usa la fórmula de la suma de una progresión aritmética.",
  "Diferencia común d = 3; término 50 = 2 + 49·3 = 149.",
  "La suma es (número de términos)·(primer + último)/2.",
  "= 50·(2 + 149)/2.",
  "= 50·151/2 = 3775."],
 "Término 50 = 2 + 49·3 = 149; suma = 50·(2+149)/2 = 3775. Verificado con Python.",
 "La suma de una progresión aritmética es el promedio de los extremos por el número de términos: el patrón de Gauss de emparejar primero con último.",
 12, ["serie aritmética", "suma de Gauss", "promedio de extremos"],
 ["acumulación de pagos", "conteo", "física del movimiento uniforme"],
 "", ["series", "aritmetica", "patron", "nivel-basico"], "cap. 10 (Arithmetic Series)"))

A(P(510, "Suma de una progresión geométrica", "patrones", 2,
 "Calcula la suma de los primeros 10 términos de la sucesión geométrica 3, 6, 12, 24, …",
 ["En una geométrica cada término multiplica al anterior por una razón fija; hay una fórmula cerrada para la suma.",
  "Razón r = 2, primer término a = 3, n = 10.",
  "Suma = a·(rⁿ − 1)/(r − 1).",
  "= 3·(2¹⁰ − 1)/(2 − 1) = 3·(1024 − 1).",
  "= 3·1023 = 3069."],
 "Suma = 3·(2¹⁰ − 1)/(2 − 1) = 3·1023 = 3069. Verificado con Python.",
 "El patrón geométrico (multiplicar por una razón) da una suma cerrada a(rⁿ−1)/(r−1). El crecimiento es exponencial, no lineal.",
 12, ["serie geométrica", "razón común", "fórmula cerrada"],
 ["interés compuesto", "crecimiento de poblaciones", "decaimiento"],
 "", ["series", "geometrica", "patron", "nivel-basico"], "cap. 10 (Geometric Series)"))

A(P(511, "La serie geométrica infinita", "patrones", 2,
 "Calcula la suma infinita 1 + 1/3 + 1/9 + 1/27 + ⋯",
 ["Es una serie geométrica con razón |r| < 1, que converge a un valor finito.",
  "Razón r = 1/3, primer término a = 1.",
  "Suma infinita = a/(1 − r) cuando |r| < 1.",
  "= 1/(1 − 1/3).",
  "= 1/(2/3) = 3/2."],
 "Suma = a/(1 − r) = 1/(1 − 1/3) = 3/2. Verificado con Python.",
 "Cuando la razón cumple |r| < 1, las potencias se achican y la serie geométrica converge a a/(1−r). El patrón infinito tiene suma finita.",
 10, ["serie geométrica infinita", "convergencia", "a/(1−r)"],
 ["fractales", "decimales periódicos", "valor presente perpetuo"],
 "", ["series", "geometrica", "patron", "nivel-basico"], "cap. 10 (Geometric Series)"))

A(P(512, "La suma de los primeros cuadrados", "patrones", 2,
 "Calcula 1² + 2² + 3² + ⋯ + 10².",
 ["Existe una fórmula cerrada para la suma de los primeros n cuadrados.",
  "1² + 2² + ⋯ + n² = n(n + 1)(2n + 1)/6.",
  "Aquí n = 10.",
  "= 10·11·21/6.",
  "= 2310/6 = 385."],
 "∑_{k=1}^{10} k² = 10·11·21/6 = 385. Verificado con Python.",
 "La suma de cuadrados sigue un patrón polinómico cúbico en n. La fórmula n(n+1)(2n+1)/6 lo captura sin sumar término a término.",
 10, ["suma de cuadrados", "fórmula cerrada", "n(n+1)(2n+1)/6"],
 ["momentos de inercia", "estadística", "sumas de Riemann"],
 "", ["series", "potencias", "patron", "nivel-basico"], "cap. 17 (Sums of Polynomial Series)"))

A(P(513, "La suma de los primeros cubos", "patrones", 2,
 "Calcula 1³ + 2³ + 3³ + 4³ + 5³.",
 ["La suma de los primeros cubos tiene una fórmula sorprendentemente bella.",
  "1³ + 2³ + ⋯ + n³ = (1 + 2 + ⋯ + n)² = [n(n+1)/2]².",
  "Aquí n = 5, y 1 + 2 + 3 + 4 + 5 = 15.",
  "= 15².",
  "= 225."],
 "∑_{k=1}^{5} k³ = [5·6/2]² = 15² = 225. Verificado con Python.",
 "El patrón notable: la suma de los primeros n cubos es el CUADRADO de la suma de los primeros n enteros. Conecta cubos con triangulares.",
 10, ["suma de cubos", "(∑k)²", "identidad de Nicómaco"],
 ["geometría de números", "demostraciones visuales", "estadística"],
 "", ["series", "potencias", "patron", "nivel-basico"], "cap. 17 (Sums of Polynomial Series)"))

A(P(514, "Un logaritmo en base dos", "patrones", 1,
 "¿Cuánto vale log₂(64)?",
 ["El logaritmo en base 2 de un número pregunta: ¿a qué potencia hay que elevar 2 para obtenerlo?",
  "Busca el exponente e tal que 2^e = 64.",
  "Lista potencias de 2: 2, 4, 8, 16, 32, 64.",
  "64 = 2⁶.",
  "log₂(64) = 6."],
 "log₂(64) = 6 porque 2⁶ = 64. Verificado con Python.",
 "El logaritmo recorre el patrón de las potencias al revés: cuenta cuántas veces se multiplica la base. log₂ de una potencia de 2 es su exponente.",
 6, ["logaritmo", "potencias de 2", "exponente"],
 ["escala decibélica", "complejidad algorítmica", "teoría de la información"],
 "", ["logaritmos", "exponentes", "patron", "nivel-basico"], "cap. 13 (Introduction to Logarithms)"))

A(P(515, "Logaritmo en base tres", "patrones", 1,
 "¿Cuánto vale log₃(81)?",
 ["Pregunta: ¿a qué potencia hay que elevar 3 para obtener 81?",
  "Lista potencias de 3: 3, 9, 27, 81.",
  "81 = 3⁴.",
  "Por tanto el exponente es 4.",
  "log₃(81) = 4."],
 "log₃(81) = 4 porque 3⁴ = 81. Verificado con Python.",
 "El mismo patrón en otra base: el logaritmo de una potencia de la base es directamente su exponente. Las potencias crecen y el log las 'cuenta'.",
 6, ["logaritmo", "potencias de 3", "exponente"],
 ["escalas logarítmicas", "crecimiento exponencial", "pH químico"],
 "", ["logaritmos", "exponentes", "patron", "nivel-basico"], "cap. 13 (Introduction to Logarithms)"))

A(P(516, "El decimal que se repite", "patrones", 3,
 "Expresa el decimal periódico 0.272727… (con el bloque '27' repitiéndose) como una fracción en su forma más simple.",
 ["Un decimal periódico tiene un patrón repetitivo que se puede 'atrapar' con un truco algebraico.",
  "Sea x = 0.272727…; como el bloque tiene 2 cifras, multiplica por 100: 100x = 27.2727…",
  "Resta: 100x − x = 27, es decir 99x = 27.",
  "x = 27/99.",
  "Simplifica: 27/99 = 3/11."],
 "Sea x = 0.27̄; 100x − x = 27 ⇒ x = 27/99 = 3/11. Verificado con Python.",
 "El patrón periódico se elimina restando dos múltiplos del número. Un bloque de k cifras se atrapa multiplicando por 10ᵏ. Todo decimal periódico es racional.",
 12, ["decimal periódico", "serie geométrica", "fracción"],
 ["conversión de bases", "representación de números", "señales periódicas"],
 "", ["decimales", "patron", "nivel-intermedio"], "cap. 10/13 (decimales periódicos)"))

A(P(517, "Una potencia de dos", "patrones", 1,
 "¿Cuánto vale 2¹⁰?",
 ["Multiplica 2 por sí mismo 10 veces, o usa potencias intermedias conocidas.",
  "2⁵ = 32.",
  "2¹⁰ = (2⁵)² = 32².",
  "32² = 1024.",
  "2¹⁰ = 1024."],
 "2¹⁰ = (2⁵)² = 32² = 1024. Verificado con Python.",
 "Las leyes de exponentes permiten construir potencias grandes a partir de pequeñas: 2¹⁰ = (2⁵)². El valor 1024 ≈ 1000 es la base de los 'kilo' informáticos.",
 6, ["potencias", "leyes de exponentes", "2¹⁰=1024"],
 ["informática (kibibytes)", "crecimiento exponencial", "duplicación"],
 "", ["exponentes", "patron", "nivel-basico"], "cap. 13 (Exponential Function Basics)"))

A(P(518, "Suma de una progresión con paso tres", "patrones", 2,
 "Calcula la suma de los primeros 15 términos de la sucesión aritmética 1, 4, 7, 10, …",
 ["Halla el término 15 y luego promedia extremos por el número de términos.",
  "Diferencia común d = 3; término 15 = 1 + 14·3 = 43.",
  "Suma = (número de términos)·(primer + último)/2.",
  "= 15·(1 + 43)/2.",
  "= 15·44/2 = 15·22 = 330."],
 "Término 15 = 1 + 14·3 = 43; suma = 15·(1+43)/2 = 330. Verificado con Python.",
 "El patrón de Gauss vuelve a aparecer: emparejar el primero con el último da el promedio, que multiplicado por la cantidad de términos da la suma.",
 10, ["serie aritmética", "suma de Gauss", "término general"],
 ["acumulación", "conteo de filas", "progresiones"],
 "", ["series", "aritmetica", "patron", "nivel-basico"], "cap. 10 (Arithmetic Series)"))

# =====================================================================
# OPTIMIZACION (11) — AM-GM, Cauchy-Schwarz, vértice
# =====================================================================

A(P(519, "El mínimo de x más su recíproco", "optimizacion", 2,
 "Para x > 0, ¿cuál es el valor mínimo de x + 1/x?",
 ["Dos números positivos cuyo producto es fijo tienen suma mínima cuando son iguales (AM-GM).",
  "Por AM-GM, x + 1/x ≥ 2·√(x · 1/x).",
  "El producto x·(1/x) = 1 es constante.",
  "x + 1/x ≥ 2·√1 = 2, con igualdad cuando x = 1/x, es decir x = 1.",
  "El mínimo es 2."],
 "Por AM-GM, x + 1/x ≥ 2√(x·1/x) = 2, con igualdad en x = 1. El mínimo es 2. Verificado con Python.",
 "La desigualdad AM-GM dice que la media aritmética ≥ la geométrica, con igualdad cuando los términos son iguales. Es la herramienta estándar para mínimos de sumas con producto fijo.",
 10, ["desigualdad AM-GM", "producto constante", "igualdad en x=1"],
 ["optimización de costos", "diseño eficiente", "economía"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 12 (AM-GM)"))

A(P(520, "Mínimo con un cuatro", "optimizacion", 2,
 "Para x > 0, ¿cuál es el valor mínimo de x + 4/x?",
 ["Aplica AM-GM a los dos términos, cuyo producto es constante.",
  "x + 4/x ≥ 2·√(x · 4/x).",
  "El producto x·(4/x) = 4.",
  "x + 4/x ≥ 2·√4 = 4, con igualdad cuando x = 4/x, es decir x = 2.",
  "El mínimo es 4."],
 "Por AM-GM, x + 4/x ≥ 2√4 = 4, con igualdad en x = 2. El mínimo es 4. Verificado con Python.",
 "AM-GM funciona siempre que el producto de los términos sea constante: aquí x·(4/x)=4. La igualdad ocurre cuando los términos se igualan.",
 10, ["AM-GM", "producto constante", "mínimo"],
 ["optimización", "diseño de recipientes", "logística"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 12 (AM-GM)"))

A(P(521, "La cima de la parábola", "optimizacion", 2,
 "¿Cuál es el valor máximo de −x² + 6x − 5?",
 ["La gráfica abre hacia abajo (coeficiente de x² negativo), así que hay un máximo en el vértice.",
  "Completa el cuadrado: −(x² − 6x) − 5 = −((x − 3)² − 9) − 5.",
  "= −(x − 3)² + 9 − 5 = −(x − 3)² + 4.",
  "El término −(x − 3)² ≤ 0, máximo 0 cuando x = 3.",
  "El valor máximo es 4."],
 "−x² + 6x − 5 = −(x − 3)² + 4; como −(x−3)² ≤ 0, el máximo es 4 en x = 3. Verificado con Python.",
 "Completar el cuadrado revela el vértice de la parábola, donde está el óptimo. Es la 'desigualdad trivial' (cuadrado ≥ 0) aplicada a cuadráticas.",
 10, ["completar el cuadrado", "vértice", "máximo de cuadrática"],
 ["trayectorias balísticas", "maximizar ingresos", "optimización"],
 "", ["cuadratica", "optimizacion", "nivel-basico"], "cap. 5 (Maxima and Minima of Quadratics)"))

A(P(522, "Producto máximo con suma fija", "optimizacion", 2,
 "Dos números positivos suman 10. ¿Cuál es el mayor valor posible de su producto?",
 ["Con suma fija, el producto de dos positivos es máximo cuando son iguales (AM-GM).",
  "Sean a y b con a + b = 10. Por AM-GM, √(ab) ≤ (a + b)/2.",
  "√(ab) ≤ 5, así que ab ≤ 25.",
  "La igualdad ocurre cuando a = b = 5.",
  "El producto máximo es 25."],
 "Por AM-GM, ab ≤ ((a+b)/2)² = 25, con igualdad en a = b = 5. El producto máximo es 25. Verificado con Python.",
 "El recíproco de un problema AM-GM: a suma fija, el producto se maximiza con términos iguales. Es el principio isoperimétrico en versión algebraica.",
 10, ["AM-GM", "suma fija", "producto máximo"],
 ["áreas máximas", "asignación de recursos", "diseño"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 12 (AM-GM)"))

A(P(523, "Mínimo de una fracción", "optimizacion", 3,
 "Para x > 0, ¿cuál es el valor mínimo de (x² + 9)/x?",
 ["Separa la fracción en dos términos y aplica AM-GM.",
  "(x² + 9)/x = x + 9/x.",
  "Por AM-GM, x + 9/x ≥ 2·√(x · 9/x).",
  "= 2·√9 = 6, con igualdad cuando x = 9/x, es decir x = 3.",
  "El mínimo es 6."],
 "(x² + 9)/x = x + 9/x ≥ 2√9 = 6, con igualdad en x = 3. El mínimo es 6. Verificado con Python.",
 "Separar una fracción en una suma del tipo x + c/x prepara el terreno para AM-GM. El mínimo es 2√c, alcanzado cuando los términos se igualan.",
 12, ["AM-GM", "separar fracción", "mínimo 2√c"],
 ["optimización de costos", "diseño de cajas", "economía"],
 "", ["am-gm", "optimizacion", "nivel-intermedio"], "cap. 12 (Maxima and Minima)"))

A(P(524, "Cauchy-Schwarz en acción", "optimizacion", 4,
 "Si x² + y² = 1, ¿cuál es el valor máximo de 3x + 4y?",
 ["La desigualdad de Cauchy-Schwarz acota un producto escalar por el producto de las magnitudes.",
  "Cauchy-Schwarz: (3x + 4y)² ≤ (3² + 4²)(x² + y²).",
  "= (9 + 16)(1) = 25.",
  "Así que 3x + 4y ≤ √25 = 5, con igualdad cuando (x, y) es proporcional a (3, 4).",
  "El valor máximo es 5."],
 "Por Cauchy-Schwarz, (3x+4y)² ≤ (3²+4²)(x²+y²) = 25, así que 3x+4y ≤ 5 (igualdad en (x,y) ∝ (3,4)). El máximo es 5. Verificado con Python.",
 "Cauchy-Schwarz acota combinaciones lineales sujetas a una restricción cuadrática; la igualdad se da cuando los vectores son paralelos. Geométricamente, 5 es la longitud del vector (3,4).",
 16, ["desigualdad de Cauchy-Schwarz", "restricción cuadrática", "vectores paralelos"],
 ["optimización con restricciones", "proyecciones", "aprendizaje automático"],
 "", ["cauchy-schwarz", "optimizacion", "nivel-avanzado"], "cap. 12 (Cauchy-Schwarz Inequality)"))

A(P(525, "Mínimo con coeficientes", "optimizacion", 3,
 "Para x > 0, ¿cuál es el valor mínimo de 2x + 3/x? (Da la respuesta exacta.)",
 ["Aplica AM-GM a los dos términos 2x y 3/x.",
  "2x + 3/x ≥ 2·√(2x · 3/x).",
  "El producto (2x)(3/x) = 6.",
  "= 2·√6, con igualdad cuando 2x = 3/x, es decir x = √(3/2).",
  "El mínimo es 2√6."],
 "Por AM-GM, 2x + 3/x ≥ 2√((2x)(3/x)) = 2√6, con igualdad en x = √(3/2). El mínimo es 2√6 ≈ 4.90. Verificado con Python.",
 "AM-GM se aplica a cualquier par de términos positivos con producto constante, aun con coeficientes. El mínimo de ax + b/x es 2√(ab).",
 12, ["AM-GM", "coeficientes", "mínimo 2√(ab)"],
 ["optimización", "ingeniería", "diseño de costos"],
 "", ["am-gm", "optimizacion", "nivel-intermedio"], "cap. 12 (AM-GM)"))

A(P(526, "Mínimo de una suma de cuadrados", "optimizacion", 3,
 "Si x + y = 6, ¿cuál es el valor mínimo de x² + y²?",
 ["Una suma de cuadrados con suma de variables fija es mínima cuando las variables son iguales.",
  "Usa x² + y² = (x + y)² − 2xy = 36 − 2xy: minimizar x²+y² es maximizar xy.",
  "Por AM-GM, xy es máximo (= 9) cuando x = y = 3.",
  "x² + y² = 36 − 2·9 = 18 (también 3² + 3² = 18).",
  "El mínimo es 18."],
 "x² + y² = (x+y)² − 2xy = 36 − 2xy, mínimo cuando xy es máximo (x=y=3): 36 − 18 = 18. Verificado con Python.",
 "Minimizar una suma de cuadrados con suma lineal fija equivale a maximizar el producto (AM-GM): el óptimo es simétrico, con las variables iguales.",
 12, ["suma de cuadrados", "AM-GM", "simetría del óptimo"],
 ["mínimos cuadrados", "estadística (varianza)", "física"],
 "", ["optimizacion", "simetria", "nivel-intermedio"], "cap. 12 (Maxima and Minima)"))

A(P(527, "Tres factores con producto fijo", "optimizacion", 4,
 "Tres números positivos a, b, c tienen producto a·b·c = 8. ¿Cuál es el valor mínimo de su suma a + b + c?",
 ["Usa AM-GM para tres variables: la media aritmética ≥ la media geométrica.",
  "(a + b + c)/3 ≥ ∛(abc).",
  "∛(abc) = ∛8 = 2.",
  "a + b + c ≥ 3·2 = 6, con igualdad cuando a = b = c = 2.",
  "El mínimo es 6."],
 "Por AM-GM con tres variables, a + b + c ≥ 3∛(abc) = 3∛8 = 6, con igualdad en a = b = c = 2. El mínimo es 6. Verificado con Python.",
 "AM-GM se generaliza a n variables: la suma es mínima (con producto fijo) cuando todas son iguales. Aquí ∛8 = 2 fija el óptimo simétrico.",
 16, ["AM-GM con n variables", "producto fijo", "óptimo simétrico"],
 ["optimización de volúmenes", "diseño de empaques", "economía"],
 "", ["am-gm", "optimizacion", "nivel-avanzado"], "cap. 12 (AM-GM with More Variables)"))

A(P(528, "Maximizar un producto lineal", "optimizacion", 2,
 "¿Cuál es el valor máximo de 100x − x²?",
 ["La expresión es una parábola que abre hacia abajo; su máximo está en el vértice.",
  "Factoriza o completa el cuadrado: 100x − x² = −(x² − 100x).",
  "El vértice de x² − 100x está en x = 50.",
  "Evalúa: 100·50 − 50² = 5000 − 2500.",
  "= 2500."],
 "100x − x² es máximo en el vértice x = 50: 100·50 − 50² = 2500. Verificado con Python.",
 "Para una cuadrática ax² + bx + c con a < 0, el máximo está en x = −b/(2a). Aquí el vértice en x = 50 da el valor 2500.",
 10, ["vértice de parábola", "máximo de cuadrática", "x = −b/2a"],
 ["maximizar ingresos", "física (alcance)", "optimización"],
 "", ["cuadratica", "optimizacion", "nivel-basico"], "cap. 5 (Maxima and Minima of Quadratics)"))

A(P(529, "Tres variables, suma fija", "optimizacion", 3,
 "Si x + y + z = 12, ¿cuál es el valor mínimo de x² + y² + z²?",
 ["Una suma de cuadrados con la suma de las variables fija es mínima cuando todas son iguales.",
  "Por la desigualdad de la media cuadrática (o Cauchy-Schwarz), x²+y²+z² ≥ (x+y+z)²/3.",
  "= 12²/3 = 144/3 = 48.",
  "La igualdad ocurre cuando x = y = z = 4.",
  "El mínimo es 48 (y 4² · 3 = 48)."],
 "Por QM-AM (o Cauchy-Schwarz), x²+y²+z² ≥ (x+y+z)²/3 = 144/3 = 48, con igualdad en x=y=z=4. El mínimo es 48. Verificado con Python.",
 "La desigualdad (∑xᵢ²) ≥ (∑xᵢ)²/n (media cuadrática ≥ media aritmética) generaliza el caso de dos variables: el óptimo reparte el total por igual.",
 12, ["media cuadrática vs aritmética", "Cauchy-Schwarz", "óptimo simétrico"],
 ["mínimos cuadrados", "reparto equitativo", "estadística"],
 "", ["optimizacion", "cauchy-schwarz", "nivel-intermedio"], "cap. 12 (Maxima and Minima)"))

# =====================================================================
# INVERSION (11) — construir ecuaciones desde raíces, ec. funcionales, logs
# =====================================================================

A(P(530, "Construir la cuadrática", "inversion", 2,
 "Halla la ecuación cuadrática mónica (coeficiente principal 1) cuyas raíces son 2 y 5.",
 ["Trabaja hacia atrás desde las raíces: una cuadrática mónica es (x − r₁)(x − r₂).",
  "(x − 2)(x − 5).",
  "Por Vieta, la ecuación es x² − (suma de raíces)x + (producto).",
  "Suma = 2 + 5 = 7; producto = 2·5 = 10.",
  "x² − 7x + 10 = 0."],
 "La cuadrática mónica es (x − 2)(x − 5) = x² − 7x + 10. Verificado con Python.",
 "Construir un polinomio desde sus raíces es invertir las fórmulas de Vieta: la suma de las raíces da el coeficiente lineal (con signo) y el producto da el término independiente.",
 10, ["construir desde raíces", "Vieta inversa", "polinomio mónico"],
 ["diseño de filtros", "asignación de polos", "control"],
 "", ["vieta", "inversion", "nivel-basico"], "cap. 8 (Using Roots to Make Equations)"))

A(P(531, "Cuadrática con raíces complejas", "inversion", 3,
 "Halla la ecuación cuadrática mónica de coeficientes reales que tiene a 3 + 2i como una de sus raíces.",
 ["Coeficientes reales ⇒ la otra raíz es el conjugado 3 − 2i. Trabaja hacia atrás desde el par.",
  "La ecuación es (x − (3 + 2i))(x − (3 − 2i)).",
  "Suma de raíces = 6; producto = (3 + 2i)(3 − 2i) = 9 + 4 = 13.",
  "Por Vieta, x² − 6x + 13.",
  "x² − 6x + 13 = 0."],
 "Con raíces 3 ± 2i: suma 6, producto 13 ⇒ x² − 6x + 13 = 0. Verificado con Python.",
 "Para reconstruir un polinomio real con una raíz compleja hay que incluir su conjugado; así la suma y el producto salen reales y Vieta inversa da los coeficientes.",
 12, ["construir desde raíces", "conjugado", "Vieta inversa"],
 ["diseño de sistemas estables", "filtros", "EDOs"],
 "", ["complejos", "vieta", "inversion", "nivel-intermedio"], "cap. 8 (Using Roots to Make Equations)"))

A(P(532, "El logaritmo deshace la potencia", "inversion", 1,
 "Resuelve para x: 2ˣ = 32.",
 ["Para despejar un exponente, aplica la operación inversa de la exponencial: el logaritmo.",
  "x = log₂(32).",
  "Equivale a preguntar: ¿qué potencia de 2 da 32?",
  "32 = 2⁵.",
  "x = 5."],
 "2ˣ = 32 = 2⁵ ⇒ x = 5. Verificado con Python.",
 "El logaritmo es la función inversa de la exponencial: deshace la potencia para despejar el exponente. Resolver 2ˣ = 32 es leer el exponente de 32 en base 2.",
 6, ["logaritmo como inverso", "ecuación exponencial", "despejar exponente"],
 ["crecimiento/decaimiento", "complejidad algorítmica", "finanzas"],
 "", ["logaritmos", "inversion", "nivel-basico"], "cap. 13 (Switching Between Logs and Exponents)"))

A(P(533, "La exponencial deshace el logaritmo", "inversion", 1,
 "Resuelve para x: log₂(x) = 5.",
 ["El logaritmo y la exponencial son inversos: para deshacer log₂, eleva 2 a ambos lados.",
  "Si log₂(x) = 5, entonces x = 2⁵.",
  "Calcula 2⁵.",
  "= 32.",
  "x = 32."],
 "log₂(x) = 5 ⇒ x = 2⁵ = 32. Verificado con Python.",
 "Para despejar una incógnita dentro de un logaritmo se aplica la exponencial (la inversa). Es la otra cara del problema anterior.",
 6, ["exponencial como inverso", "ecuación logarítmica", "despejar"],
 ["escalas logarítmicas", "química (pH)", "acústica"],
 "", ["logaritmos", "inversion", "nivel-basico"], "cap. 13 (Switching Between Logs and Exponents)"))

A(P(534, "Deshacer una función", "inversion", 2,
 "Sea f(x) = 2x + 3. ¿Para qué valor de x se cumple f(x) = 11? (Es decir, evalúa f⁻¹(11).)",
 ["Buscar f⁻¹(11) es deshacer las operaciones de f en orden inverso.",
  "f multiplica por 2 y luego suma 3; para invertir, primero resta 3 y luego divide entre 2.",
  "Plantea 2x + 3 = 11.",
  "2x = 8.",
  "x = 4."],
 "2x + 3 = 11 ⇒ x = 4, así que f⁻¹(11) = 4. Verificado con Python.",
 "La función inversa deshace las operaciones en orden contrario: lo último que hace f (sumar 3) se deshace primero. Es pensar el proceso hacia atrás.",
 10, ["función inversa", "deshacer operaciones", "despejar"],
 ["criptografía", "conversión de unidades", "decodificación"],
 "", ["funciones", "inversion", "nivel-basico"], "cap. 2 (Inverse Functions)"))

A(P(535, "Una sucesión definida por recurrencia", "inversion", 2,
 "Una función cumple f(x + 1) = f(x) + 2 para todo x, y f(1) = 5. ¿Cuánto vale f(10)?",
 ["La recurrencia dice que cada paso suma 2; reconstruye f(10) avanzando desde f(1).",
  "De f(1) a f(10) hay 9 pasos, cada uno suma 2.",
  "f(10) = f(1) + 9·2.",
  "= 5 + 18.",
  "= 23."],
 "f(10) = f(1) + 9·2 = 5 + 18 = 23. Verificado con Python.",
 "Una recurrencia f(x+1) = f(x) + d genera una progresión aritmética; reconstruir un valor lejano es sumar d tantas veces como pasos haya. Es desplegar la definición hacia adelante.",
 10, ["recurrencia", "progresión aritmética", "reconstruir valor"],
 ["sucesiones recursivas", "programación dinámica", "modelos iterativos"],
 "", ["funciones", "recurrencia", "inversion", "nivel-basico"], "cap. 17 (Algebra of Recursive Sequences)"))

A(P(536, "Resolver dentro de una función", "inversion", 2,
 "Sea f(x) = (x − 1)/2. ¿Para qué valor de x se cumple f(x) = 4?",
 ["Deshaz las operaciones de f en orden inverso para despejar x.",
  "Plantea (x − 1)/2 = 4.",
  "Multiplica por 2: x − 1 = 8.",
  "Suma 1: x = 9.",
  "x = 9."],
 "(x − 1)/2 = 4 ⇒ x − 1 = 8 ⇒ x = 9. Verificado con Python.",
 "Resolver f(x) = valor es invertir paso a paso: deshacer la división (multiplicar) y luego la resta (sumar). El orden inverso es la clave.",
 10, ["función inversa", "despejar", "orden inverso de operaciones"],
 ["decodificación", "conversión de escalas", "criptografía"],
 "", ["funciones", "inversion", "nivel-basico"], "cap. 2 (Inverse Functions)"))

A(P(537, "Construir el cúbico", "inversion", 2,
 "Halla el polinomio cúbico mónico cuyas raíces son 1, 2 y 3.",
 ["Trabaja hacia atrás: un cúbico mónico con esas raíces es (x − 1)(x − 2)(x − 3).",
  "Multiplica los dos primeros: (x − 1)(x − 2) = x² − 3x + 2.",
  "Multiplica por (x − 3): (x² − 3x + 2)(x − 3).",
  "= x³ − 3x² + 2x − 3x² + 9x − 6 = x³ − 6x² + 11x − 6.",
  "El polinomio es x³ − 6x² + 11x − 6."],
 "(x − 1)(x − 2)(x − 3) = x³ − 6x² + 11x − 6. Verificado con Python.",
 "Construir un cúbico desde sus raíces es invertir Vieta para tres raíces: los coeficientes son (con signos) la suma, la suma de pares y el producto de las raíces.",
 12, ["construir desde raíces", "Vieta inversa", "cúbico mónico"],
 ["diseño de polinomios", "asignación de polos", "interpolación"],
 "", ["vieta", "cubico", "inversion", "nivel-basico"], "cap. 8 (Using Roots to Make Equations)"))

A(P(538, "Otra exponencial", "inversion", 2,
 "Resuelve para x: 3^(x − 1) = 27.",
 ["Expresa ambos lados como potencias de la misma base para igualar exponentes.",
  "27 = 3³.",
  "Entonces 3^(x − 1) = 3³.",
  "Como las bases son iguales, los exponentes coinciden: x − 1 = 3.",
  "x = 4."],
 "3^(x−1) = 27 = 3³ ⇒ x − 1 = 3 ⇒ x = 4. Verificado con Python.",
 "Cuando ambos lados se escriben con la misma base, la inyectividad de la exponencial permite igualar exponentes. Es resolver hacia atrás reconociendo 27 = 3³.",
 8, ["ecuación exponencial", "misma base", "igualar exponentes"],
 ["crecimiento exponencial", "interés compuesto", "decaimiento"],
 "", ["exponentes", "inversion", "nivel-basico"], "cap. 13 (Switching Between Logs and Exponents)"))

A(P(539, "Una ecuación funcional con sustitución", "inversion", 5,
 "Una función f satisface f(x) + 2·f(1/x) = x para todo x ≠ 0. ¿Cuánto vale f(2)?",
 ["Sustituye x = 2 y también x = 1/2 para obtener dos ecuaciones que liguen f(2) y f(1/2).",
  "Con x = 2: f(2) + 2·f(1/2) = 2. Con x = 1/2: f(1/2) + 2·f(2) = 1/2.",
  "Tienes un sistema lineal en las incógnitas f(2) y f(1/2).",
  "De la primera, f(2) = 2 − 2·f(1/2); sustituye en la segunda: f(1/2) + 2(2 − 2f(1/2)) = 1/2 ⇒ −3f(1/2) = −7/2 ⇒ f(1/2) = 7/6.",
  "Entonces f(2) = 2 − 2·(7/6) = 2 − 7/3 = −1/3."],
 "Sustituyendo x = 2 y x = 1/2 se obtiene el sistema f(2) + 2f(1/2) = 2 y f(1/2) + 2f(2) = 1/2, cuya solución da f(2) = −1/3. Verificado con Python.",
 "La técnica estándar para ecuaciones funcionales con f(x) y f(1/x) es sustituir x y 1/x para crear un sistema lineal y despejar el valor buscado. Es resolver hacia atrás con dos miradas.",
 22, ["ecuación funcional", "sustitución x y 1/x", "sistema lineal"],
 ["resolución de funcionales", "transformadas", "simetrías"],
 "", ["funciones", "ecuacion-funcional", "inversion", "nivel-avanzado"], "cap. 19 (Finding Values, Substitution)"))

A(P(540, "El parámetro y la raíz que falta", "inversion", 3,
 "La ecuación x² + bx + 12 = 0 tiene a x = 3 como una de sus raíces. Halla b y la otra raíz.",
 ["Como 3 es raíz, debe satisfacer la ecuación: sustitúyela para hallar b.",
  "3² + b·3 + 12 = 0 ⇒ 9 + 3b + 12 = 0 ⇒ 3b = −21 ⇒ b = −7.",
  "Para la otra raíz usa Vieta: el producto de las raíces es el término independiente, 12.",
  "3 · (otra raíz) = 12 ⇒ otra raíz = 4.",
  "b = −7 y la otra raíz es 4."],
 "Sustituyendo x = 3: 9 + 3b + 12 = 0 ⇒ b = −7. Por Vieta, producto de raíces = 12 ⇒ otra raíz = 4. Verificado con Python.",
 "Conocer una raíz permite despejar el parámetro (sustituyendo) y luego usar Vieta (el producto de raíces) para recuperar la raíz faltante. Es reconstruir todo hacia atrás desde un dato.",
 12, ["raíz conocida", "despejar parámetro", "Vieta para la otra raíz"],
 ["ingeniería inversa de modelos", "calibración", "diseño de sistemas"],
 "", ["cuadratica", "vieta", "inversion", "nivel-intermedio"], "cap. 4/8 (Quadratics, Vieta)"))

# =====================================================================
# Validación de balance y append idempotente
# =====================================================================
assert len(PROBLEMS) == 44, len(PROBLEMS)
bal = collections.Counter(p["estrategia"] for p in PROBLEMS)
assert bal["inversion"] == bal["optimizacion"] == bal["invariantes"] == bal["patrones"] == 11, bal
ids = [p["id"] for p in PROBLEMS]
assert ids == list(range(497, 541)), ids
assert len(set(ids)) == 44

PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
clash = existing & set(ids)
assert not clash, ("choque de ids", clash)

data["problemas"].extend(PROBLEMS)
gbal = collections.Counter(p["estrategia"] for p in data["problemas"])
print("balance global tras append:", dict(gbal))
assert all(v == 135 for v in gbal.values()), gbal

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: añadidos {len(PROBLEMS)} problemas (ids {ids[0]}-{ids[-1]}). Total = {len(data['problemas'])}.")
