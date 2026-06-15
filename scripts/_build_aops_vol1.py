# -*- coding: utf-8 -*-
"""Tanda 39 — Lehoczky & Rusczyk, *the Art of Problem Solving, Volume 1* (the Basics).
Append 44 problemas verificados a data/problems.json. PDF de 5 MB CON capa de texto;
el TOC se extrajo con PyMuPDF (fitz): 29 capítulos que cubren TODO el temario básico
(exponentes/logaritmos, complejos, ecuaciones lineales, proporciones, enteros, cuadráticas,
factorizaciones, geometría -círculos/ángulos/triángulos/cuadriláteros/polígonos/áreas/
coordenadas/potencia de un punto/3D-, transformaciones, funciones, desigualdades, sucesiones
y series, conteo, probabilidad/estadística, conjuntos, demostraciones). Como Vol.1 es un
REPASO transversal de temas ya minados en tandas previas (Intro/Intermediate Algebra, Geometry,
Number Theory, C&P), se eligieron problemas con ÁNGULOS y NÚMEROS frescos para NO duplicar
(§1.6). Cada número se verifica de forma independiente con Python/sympy (44 checks, todos OK).
Mapeo a las 4 estrategias canónicas (11 c/u, balance GLOBAL -> 157/157/157/157):
 - invariantes: leyes de logaritmos (combinar), módulo/conjugado complejo, potencia de un
   punto, cadenas de proporciones, media, suma de ángulos.
 - patrones: sucesiones/series (aritm./geom.), leyes de exponentes, coeficientes binomiales,
   sumas notables, último dígito de potencias.
 - optimizacion: desigualdades (AM-GM, Cauchy-Schwarz), vértice, desigualdad triangular,
   distancias mínimas.
 - inversion: resolver ecuaciones (exponenciales/log/sistemas/cuadráticas), proporción inversa,
   porcentajes hacia atrás, reconstruir sucesiones, funciones inversas.
Builder idempotente: aborta si hay choque de ids. Sector C (entrenamiento), esquema §4.1,
ids 585-628."""
import json, collections

SRC = "Lehoczky & Rusczyk, *the Art of Problem Solving, Vol. 1*"

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
# INVARIANTES (11) — leyes de log, complejos, potencia de un punto, proporciones
# =====================================================================

A(P(585, "Combinar dos logaritmos", "invariantes", 2,
 "Calcula log₂(48) − log₂(3).",
 ["La resta de logaritmos de la misma base se combina en el logaritmo de un cociente.",
  "log_b(M) − log_b(N) = log_b(M/N).",
  "log₂(48) − log₂(3) = log₂(48/3) = log₂(16).",
  "16 = 2⁴.",
  "= 4."],
 "log₂(48) − log₂(3) = log₂(48/3) = log₂(16) = 4. Verificado con Python.",
 "Las leyes de los logaritmos hacen invariante el valor bajo reescritura: una resta se vuelve un cociente. Convierte un cálculo aparatoso en log₂(16) = 4.",
 10, ["ley del cociente de logaritmos", "logaritmo", "potencias de 2"],
 ["escalas logarítmicas", "decibeles", "complejidad algorítmica"],
 "", ["logaritmos", "invariante", "nivel-basico"], "cap. 1.5 (Logarithms)"))

A(P(586, "Sumar dos logaritmos", "invariantes", 2,
 "Calcula log₆(4) + log₆(9).",
 ["La suma de logaritmos de la misma base se combina en el logaritmo de un producto.",
  "log_b(M) + log_b(N) = log_b(M·N).",
  "log₆(4) + log₆(9) = log₆(36).",
  "36 = 6².",
  "= 2."],
 "log₆(4) + log₆(9) = log₆(36) = 2. Verificado con Python.",
 "La ley del producto de logaritmos: una suma se convierte en el log de un producto. El resultado no depende de cómo se separe (4·9 = 36 = 6²).",
 10, ["ley del producto de logaritmos", "logaritmo", "combinar"],
 ["acústica", "química (pH)", "teoría de la información"],
 "", ["logaritmos", "invariante", "nivel-basico"], "cap. 1.5 (Logarithms)"))

A(P(587, "El módulo de un producto", "invariantes", 3,
 "Calcula el módulo (valor absoluto) del número complejo (3 + 4i)(5 + 12i).",
 ["El módulo de un producto de complejos es el producto de los módulos: no hace falta multiplicar primero.",
  "|z·w| = |z|·|w|.",
  "|3 + 4i| = √(3² + 4²) = 5; |5 + 12i| = √(5² + 12²) = 13.",
  "|(3 + 4i)(5 + 12i)| = 5·13.",
  "= 65."],
 "|(3+4i)(5+12i)| = |3+4i|·|5+12i| = 5·13 = 65. Verificado con Python.",
 "La multiplicatividad del módulo (|zw| = |z||w|) es un invariante clave de los complejos: al multiplicar, los módulos se multiplican y los argumentos se suman.",
 12, ["módulo de complejos", "|zw|=|z||w|", "ternas pitagóricas"],
 ["procesamiento de señales", "rotaciones", "fasores eléctricos"],
 "", ["complejos", "invariante", "nivel-intermedio"], "cap. 2.2 (Complex Number Operations)"))

A(P(588, "Un complejo más su conjugado", "invariantes", 1,
 "Si z = 7 − 3i, calcula z + z̄ (la suma de z con su conjugado).",
 ["El conjugado de a + bi es a − bi; piensa qué pasa con la parte imaginaria al sumarlos.",
  "z̄ = 7 + 3i.",
  "z + z̄ = (7 − 3i) + (7 + 3i).",
  "Las partes imaginarias se cancelan: queda 7 + 7.",
  "= 14 (que es 2·Re(z))."],
 "z + z̄ = (7 − 3i) + (7 + 3i) = 14 = 2·Re(z). Verificado con Python.",
 "Sumar un complejo con su conjugado siempre da un número real (2·parte real): la parte imaginaria es invariante y se anula. Es la base para extraer la parte real.",
 8, ["conjugado complejo", "z+z̄=2Re(z)", "número real"],
 ["análisis de señales", "transformadas", "física"],
 "", ["complejos", "conjugado", "invariante", "nivel-basico"], "cap. 2.2 (Complex Number Operations)"))

A(P(589, "La tangente y la secante", "invariantes", 3,
 "Desde un punto exterior a una circunferencia se traza una recta tangente y una recta secante. La secante corta la circunferencia a distancias 3 y 12 del punto exterior. ¿Cuánto mide el segmento tangente?",
 ["La 'potencia del punto' es la misma para cualquier recta que pase por el punto: tangente² = (segmento externo de la secante)·(secante completa).",
  "Para la secante, el producto es (distancia al primer corte)·(distancia al segundo corte) = 3·12.",
  "= 36.",
  "Para la tangente, ese producto es el cuadrado del segmento tangente: t² = 36.",
  "t = 6."],
 "Por la potencia de un punto, t² = 3·12 = 36, así que t = 6. Verificado con Python.",
 "La potencia de un punto exterior es invariante: vale t² para la tangente y (externo)·(total) para cualquier secante. Igualar ambas da la tangente.",
 14, ["potencia de un punto", "tangente y secante", "t²=producto"],
 ["óptica", "triangulación", "geometría de circunferencias"],
 "", ["potencia-punto", "circulo", "invariante", "nivel-intermedio"], "cap. 17 (Power of a Point)"))

A(P(590, "Encadenar proporciones", "invariantes", 2,
 "Se sabe que a/b = 3/5 y b/c = 5/7. Si c = 21, ¿cuánto vale a?",
 ["Encadena las razones para escribir a, b y c en una sola proporción continua.",
  "a : b = 3 : 5 y b : c = 5 : 7 comparten el 5 de b, así que a : b : c = 3 : 5 : 7.",
  "Entonces a/c = 3/7.",
  "Con c = 21: a = (3/7)·21.",
  "= 9."],
 "Encadenando, a : b : c = 3 : 5 : 7, así que a = (3/7)·c = (3/7)·21 = 9. Verificado con Python.",
 "Las razones encadenadas componen un invariante: a/c = (a/b)·(b/c). Alinear los términos comunes da una proporción continua directa.",
 10, ["proporciones encadenadas", "razón continua", "composición de razones"],
 ["conversión de unidades", "escalas", "engranajes"],
 "", ["proporciones", "invariante", "nivel-basico"], "cap. 4 (Proportions)"))

A(P(591, "Subir el promedio", "invariantes", 2,
 "El promedio de 5 números es 12. ¿Qué número hay que agregar al conjunto para que el promedio de los 6 números sea 14?",
 ["El promedio fija la suma: úsala como invariante antes y después de agregar el número.",
  "Suma de los 5 números = 5·12 = 60.",
  "Para que 6 números promedien 14, su suma debe ser 6·14 = 84.",
  "El número agregado es 84 − 60.",
  "= 24."],
 "Suma inicial = 60; suma requerida = 84; el número a agregar es 84 − 60 = 24. Verificado con Python.",
 "El promedio es la suma dividida por la cantidad; razonar con la SUMA (un invariante recuperable) evita confusiones al cambiar el tamaño del conjunto.",
 10, ["promedio", "suma como invariante", "estadística"],
 ["control de calidad", "calificaciones", "análisis de datos"],
 "", ["estadistica", "invariante", "nivel-basico"], "cap. 26 (Statistics and Probability)"))

A(P(592, "El ángulo exterior del triángulo", "invariantes", 1,
 "En un triángulo, dos de sus ángulos interiores miden 40° y 65°. ¿Cuánto mide el ángulo exterior adyacente al tercer ángulo?",
 ["Hay un invariante de ángulos: el ángulo exterior de un triángulo es igual a la suma de los dos ángulos interiores no adyacentes (los 'remotos').",
  "Los ángulos remotos son 40° y 65°.",
  "El ángulo exterior buscado es su suma.",
  "= 40° + 65°.",
  "= 105°."],
 "El ángulo exterior es igual a la suma de los dos interiores remotos: 40° + 65° = 105°. Verificado con Python.",
 "El teorema del ángulo exterior se deriva de que los tres interiores suman 180° (invariante): el exterior (= 180 − tercero) iguala la suma de los otros dos.",
 8, ["ángulo exterior", "suma de remotos", "ángulos de un triángulo"],
 ["navegación", "diseño geométrico", "topografía"],
 "", ["angulos", "triangulo", "invariante", "nivel-basico"], "cap. 14 (Angle Chasing)"))

A(P(593, "Distancia entre dos puntos", "invariantes", 1,
 "¿Cuál es la distancia entre los puntos (1, 2) y (7, 10) en el plano cartesiano?",
 ["La distancia se obtiene del teorema de Pitágoras aplicado a las diferencias de coordenadas.",
  "Distancia = √((x₂ − x₁)² + (y₂ − y₁)²).",
  "Diferencias: 7 − 1 = 6 y 10 − 2 = 8.",
  "= √(6² + 8²) = √(36 + 64) = √100.",
  "= 10."],
 "Distancia = √(6² + 8²) = √100 = 10. Verificado con Python.",
 "La fórmula de la distancia es Pitágoras en coordenadas: invariante bajo traslaciones. Aquí aparece la terna 6-8-10.",
 8, ["distancia entre puntos", "Pitágoras", "coordenadas"],
 ["GPS", "gráficos por computadora", "física"],
 "", ["coordenadas", "distancia", "invariante", "nivel-basico"], "cap. 16 (The Power of Coordinates)"))

A(P(594, "Cambio de base", "invariantes", 3,
 "Calcula log₈(32).",
 ["Expresa ambos números como potencias de una base común (2) y usa la relación entre logaritmos.",
  "32 = 2⁵ y 8 = 2³.",
  "log₈(32) = log₈(2⁵) = 5·log₈(2).",
  "Como 8 = 2³, log₈(2) = 1/3.",
  "= 5·(1/3) = 5/3."],
 "log₈(32) = log(32)/log(8) = (5·log2)/(3·log2) = 5/3. Verificado con Python.",
 "La fórmula de cambio de base hace invariante el cociente log(M)/log(N) bajo la base elegida: log₈(32) = 5/3 sin importar en qué base se calcule.",
 14, ["cambio de base", "logaritmo", "potencias de 2"],
 ["conversión entre escalas", "informática", "matemática financiera"],
 "", ["logaritmos", "invariante", "nivel-intermedio"], "cap. 1.5 (Logarithms)"))

A(P(595, "El cuadrado del módulo", "invariantes", 2,
 "Para el número complejo z = 2 + i, calcula z·z̄ (el producto de z por su conjugado).",
 ["El producto de un complejo por su conjugado es siempre un número real: el cuadrado de su módulo.",
  "z·z̄ = (a + bi)(a − bi) = a² + b².",
  "Aquí a = 2 y b = 1.",
  "= 2² + 1² = 4 + 1.",
  "= 5 (que es |z|²)."],
 "z·z̄ = 2² + 1² = 5 = |z|². Verificado con Python.",
 "z·z̄ = |z|² es real e invariante: elimina la parte imaginaria. Es la base de la división de complejos (racionalizar multiplicando por el conjugado).",
 8, ["módulo al cuadrado", "z·z̄=|z|²", "conjugado"],
 ["división de complejos", "mecánica cuántica", "fasores"],
 "", ["complejos", "conjugado", "invariante", "nivel-basico"], "cap. 2.2 (Complex Number Operations)"))

# =====================================================================
# PATRONES (11) — sucesiones/series, exponentes, binomios, sumas notables
# =====================================================================

A(P(596, "El término número cien", "patrones", 2,
 "En la sucesión aritmética 7, 11, 15, 19, …, ¿cuál es el término número 100?",
 ["Identifica la diferencia común y usa la fórmula del término general.",
  "Diferencia común d = 4; primer término a₁ = 7.",
  "Término n-ésimo: aₙ = a₁ + (n − 1)·d.",
  "a₁₀₀ = 7 + 99·4.",
  "= 7 + 396 = 403."],
 "a₁₀₀ = 7 + 99·4 = 403. Verificado con Python.",
 "El patrón aritmético da una fórmula lineal en n: aₙ = a₁ + (n−1)d. No hace falta listar 100 términos.",
 10, ["sucesión aritmética", "término general", "diferencia común"],
 ["proyecciones lineales", "planes de pago", "depreciación"],
 "", ["sucesiones", "aritmetica", "patron", "nivel-basico"], "cap. 24 (Sequences and Series)"))

A(P(597, "Suma de Gauss hasta doscientos", "patrones", 2,
 "Calcula 1 + 2 + 3 + ⋯ + 200.",
 ["Empareja el primer término con el último, el segundo con el penúltimo, etc.: todos los pares suman lo mismo.",
  "Cada par (1+200), (2+199), … suma 201, y hay 100 pares.",
  "O usa la fórmula: suma = n(n + 1)/2.",
  "= 200·201/2.",
  "= 20100."],
 "Suma = 200·201/2 = 20100. Verificado con Python.",
 "El truco de Gauss: emparejar extremos da pares de suma constante. La fórmula n(n+1)/2 captura ese patrón.",
 8, ["suma de Gauss", "serie aritmética", "n(n+1)/2"],
 ["conteo acumulado", "complejidad de algoritmos", "sumas"],
 "", ["series", "aritmetica", "patron", "nivel-basico"], "cap. 24 (Sequences and Series)"))

A(P(598, "Quinto término geométrico", "patrones", 2,
 "En la sucesión geométrica 2, 6, 18, 54, …, ¿cuál es el quinto término?",
 ["Encuentra la razón común (cada término entre el anterior) y aplica el término general.",
  "Razón r = 6/2 = 3; primer término a₁ = 2.",
  "Término n-ésimo: aₙ = a₁·rⁿ⁻¹.",
  "a₅ = 2·3⁴.",
  "= 2·81 = 162."],
 "a₅ = 2·3⁴ = 162. Verificado con Python.",
 "El patrón geométrico multiplica por una razón fija: aₙ = a₁·rⁿ⁻¹. El crecimiento es exponencial.",
 10, ["sucesión geométrica", "razón común", "término general"],
 ["interés compuesto", "crecimiento poblacional", "decaimiento"],
 "", ["sucesiones", "geometrica", "patron", "nivel-basico"], "cap. 24 (Sequences and Series)"))

A(P(599, "Suma de potencias de dos", "patrones", 2,
 "Calcula 1 + 2 + 4 + 8 + ⋯ + 512 (las potencias de 2 desde 2⁰ hasta 2⁹).",
 ["Es una serie geométrica de razón 2; usa la fórmula de la suma.",
  "Suma de 2⁰ + 2¹ + ⋯ + 2ⁿ = 2ⁿ⁺¹ − 1.",
  "Aquí el último término es 2⁹, así que n = 9.",
  "= 2¹⁰ − 1.",
  "= 1024 − 1 = 1023."],
 "1 + 2 + ⋯ + 2⁹ = 2¹⁰ − 1 = 1023. Verificado con Python.",
 "La suma de potencias de 2 desde 2⁰ es siempre una menos que la siguiente potencia: 2ⁿ⁺¹ − 1. Es la base de la representación binaria.",
 10, ["serie geométrica", "potencias de 2", "2ⁿ⁺¹−1"],
 ["representación binaria", "estructuras de datos", "informática"],
 "", ["series", "geometrica", "patron", "nivel-basico"], "cap. 24 (Sequences and Series)"))

A(P(600, "Una serie geométrica infinita", "patrones", 2,
 "Calcula la suma infinita 2/3 + 2/9 + 2/27 + 2/81 + ⋯",
 ["Es geométrica con razón 1/3 (< 1), así que converge.",
  "Primer término a = 2/3, razón r = 1/3.",
  "Suma infinita = a/(1 − r).",
  "= (2/3)/(1 − 1/3) = (2/3)/(2/3).",
  "= 1."],
 "Suma = (2/3)/(1 − 1/3) = 1. Verificado con Python.",
 "Una serie geométrica con |r| < 1 converge a a/(1−r). El patrón infinito tiene suma finita, aquí exactamente 1.",
 10, ["serie geométrica infinita", "convergencia", "a/(1−r)"],
 ["fractales", "valor presente perpetuo", "decimales periódicos"],
 "", ["series", "geometrica", "patron", "nivel-basico"], "cap. 24 (Sequences and Series)"))

A(P(601, "Simplificar potencias", "patrones", 2,
 "Calcula 8⁴ / 4³ expresando todo como potencias de 2.",
 ["Convierte las bases a potencias de 2 y usa las leyes de los exponentes.",
  "8 = 2³, así que 8⁴ = 2¹²; 4 = 2², así que 4³ = 2⁶.",
  "8⁴/4³ = 2¹²/2⁶.",
  "Al dividir potencias de la misma base se restan los exponentes: 2¹²⁻⁶.",
  "= 2⁶ = 64."],
 "8⁴/4³ = 2¹²/2⁶ = 2⁶ = 64. Verificado con Python.",
 "Reducir todo a una base común revela el patrón: al dividir, los exponentes se restan. Las leyes de exponentes evitan calcular números grandes.",
 10, ["leyes de exponentes", "base común", "restar exponentes"],
 ["notación científica", "informática", "escalas"],
 "", ["exponentes", "patron", "nivel-basico"], "cap. 1 (Integer Exponents)"))

A(P(602, "Un coeficiente binomial", "patrones", 3,
 "En el desarrollo de (x + y)⁵, ¿cuál es el coeficiente del término x²y³?",
 ["El teorema del binomio dice que el coeficiente de xᵏyⁿ⁻ᵏ en (x+y)ⁿ es C(n, k).",
  "Aquí n = 5 y el término x²y³ tiene k = 2 (el exponente de x).",
  "El coeficiente es C(5, 2).",
  "C(5,2) = (5·4)/(2·1).",
  "= 10."],
 "El coeficiente de x²y³ en (x+y)⁵ es C(5,2) = 10. Verificado con Python.",
 "Los coeficientes del binomio son los números de una fila del triángulo de Pascal: C(n,k). El patrón conecta álgebra con combinatoria.",
 12, ["teorema del binomio", "coeficientes binomiales", "triángulo de Pascal"],
 ["probabilidad binomial", "expansiones algebraicas", "combinatoria"],
 "", ["binomio", "pascal", "patron", "nivel-intermedio"], "cap. 25 (Learning to Count)"))

A(P(603, "Suma de los primeros impares", "patrones", 1,
 "Calcula 1 + 3 + 5 + 7 + ⋯ + 19 (la suma de los primeros 10 números impares).",
 ["Suma los primeros impares y busca el patrón: 1, 1+3=4, 1+3+5=9, …",
  "Los resultados 1, 4, 9, 16, … son cuadrados perfectos.",
  "La suma de los primeros n impares es n².",
  "Aquí hay 10 impares (del 1 al 19).",
  "= 10² = 100."],
 "La suma de los primeros n impares es n²; para n = 10 da 100. Verificado con Python.",
 "Un patrón clásico: 1 + 3 + ⋯ + (2n−1) = n². Se 've' apilando capas en forma de L para completar un cuadrado.",
 8, ["suma de impares", "cuadrados perfectos", "1+3+...+(2n−1)=n²"],
 ["demostraciones visuales", "series", "números figurados"],
 "", ["series", "patron", "nivel-basico"], "cap. 24 (Sequences and Series)"))

A(P(604, "Diferencia de cuadrados", "patrones", 2,
 "Calcula 51² − 49² sin elevar al cuadrado.",
 ["Reconoce el patrón de la diferencia de cuadrados: a² − b² = (a + b)(a − b).",
  "Aquí a = 51 y b = 49.",
  "51² − 49² = (51 + 49)(51 − 49).",
  "= 100·2.",
  "= 200."],
 "51² − 49² = (51+49)(51−49) = 100·2 = 200. Verificado con Python.",
 "La factorización a² − b² = (a+b)(a−b) convierte una resta de cuadrados grandes en un producto sencillo. Es un patrón de cálculo mental muy útil.",
 8, ["diferencia de cuadrados", "factorización", "cálculo mental"],
 ["aritmética rápida", "factorización de enteros", "álgebra"],
 "", ["factorizacion", "patron", "nivel-basico"], "cap. 7 (Special Factorizations)"))

A(P(605, "El último dígito de una potencia grande", "patrones", 3,
 "¿Cuál es el último dígito (dígito de las unidades) de 3¹⁰⁰?",
 ["El último dígito de las potencias de 3 sigue un ciclo; encuéntralo.",
  "3¹ = 3, 3² = 9, 3³ = 27, 3⁴ = 81: los últimos dígitos son 3, 9, 7, 1 y luego se repiten.",
  "El ciclo tiene longitud 4. Reduce el exponente módulo 4.",
  "100 = 4·25, así que 100 ≡ 0 (mód 4), que corresponde al final del ciclo.",
  "El cuarto término del ciclo es 1, así que el último dígito de 3¹⁰⁰ es 1."],
 "Los últimos dígitos de las potencias de 3 ciclan 3, 9, 7, 1 (periodo 4); como 100 es múltiplo de 4, el último dígito es 1. Verificado con Python.",
 "El último dígito de las potencias es periódico (aquí periodo 4). Reducir el exponente módulo el periodo resuelve exponentes enormes.",
 12, ["ciclo de últimos dígitos", "potencias de 3", "periodicidad módulo 4"],
 ["aritmética modular", "criptografía", "verificación de cálculos"],
 "", ["unidades", "potencia", "patron", "nivel-intermedio"], "cap. 5 (Using the Integers)"))

A(P(606, "El vigésimo número triangular", "patrones", 1,
 "Los números triangulares son 1, 3, 6, 10, 15, … (cada uno suma un entero más que el anterior). ¿Cuál es el vigésimo número triangular?",
 ["El n-ésimo número triangular es la suma 1 + 2 + ⋯ + n.",
  "Hay una fórmula cerrada: Tₙ = n(n + 1)/2.",
  "Aquí n = 20.",
  "= 20·21/2.",
  "= 210."],
 "T₂₀ = 20·21/2 = 210. Verificado con Python.",
 "Los números triangulares cuentan puntos en un triángulo y valen n(n+1)/2: el mismo patrón de la suma de Gauss.",
 8, ["números triangulares", "n(n+1)/2", "suma de Gauss"],
 ["conteo de conexiones", "apretones de manos", "números figurados"],
 "", ["series", "patron", "nivel-basico"], "cap. 24 (Sequences and Series)"))

# =====================================================================
# OPTIMIZACION (11) — desigualdades, vértice, desigualdad triangular, distancias
# =====================================================================

A(P(607, "Mínimo con dieciséis", "optimizacion", 2,
 "Para x > 0, ¿cuál es el valor mínimo de x + 16/x?",
 ["Aplica AM-GM a los dos términos, cuyo producto es constante.",
  "x + 16/x ≥ 2·√(x · 16/x).",
  "El producto x·(16/x) = 16.",
  "= 2·√16 = 8, con igualdad cuando x = 16/x, es decir x = 4.",
  "El mínimo es 8."],
 "Por AM-GM, x + 16/x ≥ 2√16 = 8, con igualdad en x = 4. El mínimo es 8. Verificado con Python.",
 "AM-GM da el mínimo de x + c/x como 2√c (cuando los términos se igualan). Aquí c = 16 da mínimo 8.",
 10, ["desigualdad AM-GM", "producto constante", "mínimo 2√c"],
 ["optimización de costos", "diseño eficiente", "economía"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 22 (Inequalities)"))

A(P(608, "La cima de otra parábola", "optimizacion", 2,
 "¿Cuál es el valor máximo de 12x − x²?",
 ["La expresión es una parábola que abre hacia abajo; su máximo está en el vértice.",
  "Para ax² + bx + c con a < 0, el vértice está en x = −b/(2a).",
  "Aquí a = −1, b = 12, así que x = −12/(2·(−1)) = 6.",
  "Evalúa: 12·6 − 6² = 72 − 36.",
  "= 36."],
 "El máximo está en x = 6: 12·6 − 6² = 36. Verificado con Python.",
 "El vértice x = −b/(2a) localiza el óptimo de cualquier cuadrática. Para a < 0 es un máximo.",
 10, ["vértice de parábola", "máximo de cuadrática", "x=−b/2a"],
 ["maximizar ingresos", "física (alcance)", "optimización"],
 "", ["cuadratica", "optimizacion", "nivel-basico"], "cap. 6 (Quadratic Equations)"))

A(P(609, "Producto máximo con suma veinte", "optimizacion", 2,
 "Dos números positivos suman 20. ¿Cuál es el mayor valor posible de su producto?",
 ["Con suma fija, el producto de dos positivos es máximo cuando son iguales (AM-GM).",
  "Por AM-GM, √(ab) ≤ (a + b)/2 = 10.",
  "Así que ab ≤ 100.",
  "La igualdad ocurre cuando a = b = 10.",
  "El producto máximo es 100."],
 "Por AM-GM, ab ≤ (20/2)² = 100, con igualdad en a = b = 10. El máximo es 100. Verificado con Python.",
 "A suma fija, el producto se maximiza con términos iguales: principio isoperimétrico en versión algebraica.",
 10, ["AM-GM", "suma fija", "producto máximo"],
 ["áreas máximas", "asignación de recursos", "diseño"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 22 (Inequalities)"))

A(P(610, "El fondo de la parábola", "optimizacion", 2,
 "¿Cuál es el valor mínimo de x² − 10x + 30?",
 ["Completa el cuadrado para revelar el vértice.",
  "x² − 10x + 30 = (x² − 10x + 25) + 5 = (x − 5)² + 5.",
  "El término (x − 5)² es ≥ 0, mínimo 0 cuando x = 5.",
  "El valor mínimo es entonces 0 + 5.",
  "= 5."],
 "x² − 10x + 30 = (x − 5)² + 5; como (x−5)² ≥ 0, el mínimo es 5 en x = 5. Verificado con Python.",
 "Completar el cuadrado escribe la cuadrática como (cuadrado) + constante; el mínimo se lee directo de la constante.",
 10, ["completar el cuadrado", "vértice", "mínimo de cuadrática"],
 ["mínimos cuadrados", "minimizar costos", "física"],
 "", ["cuadratica", "optimizacion", "nivel-basico"], "cap. 6 (Quadratic Equations)"))

A(P(611, "Cauchy-Schwarz con cinco y doce", "optimizacion", 4,
 "Si x² + y² = 1, ¿cuál es el valor máximo de 5x + 12y?",
 ["Usa la desigualdad de Cauchy-Schwarz para acotar la combinación lineal.",
  "(5x + 12y)² ≤ (5² + 12²)(x² + y²).",
  "= (25 + 144)(1) = 169.",
  "Así que 5x + 12y ≤ √169 = 13, con igualdad cuando (x, y) es proporcional a (5, 12).",
  "El máximo es 13."],
 "Por Cauchy-Schwarz, (5x+12y)² ≤ (5²+12²)(x²+y²) = 169, así que 5x+12y ≤ 13. El máximo es 13. Verificado con Python.",
 "Cauchy-Schwarz acota una combinación lineal sujeta a una restricción cuadrática: el máximo es la longitud del vector de coeficientes, √(5²+12²) = 13.",
 16, ["Cauchy-Schwarz", "restricción cuadrática", "vectores"],
 ["optimización con restricciones", "proyecciones", "aprendizaje automático"],
 "", ["cauchy-schwarz", "optimizacion", "nivel-avanzado"], "cap. 22 (Inequalities)"))

A(P(612, "El cerco mínimo de cien", "optimizacion", 2,
 "Entre todos los rectángulos de área 100, ¿cuál tiene el menor perímetro y cuánto vale?",
 ["A área fija, el perímetro es mínimo cuando el rectángulo es un cuadrado (AM-GM).",
  "Si los lados son l y w con l·w = 100, por AM-GM l + w ≥ 2√(lw) = 2√100 = 20.",
  "El perímetro 2(l + w) ≥ 40.",
  "La igualdad ocurre cuando l = w = 10.",
  "El perímetro mínimo es 40."],
 "Por AM-GM, l + w ≥ 2√100 = 20, así que el perímetro mínimo es 2·20 = 40 (cuadrado de lado 10). Verificado con Python.",
 "A área fija, el cuadrado minimiza el perímetro: AM-GM aplicada a los lados. Es el principio isoperimétrico para rectángulos.",
 12, ["AM-GM", "área fija", "perímetro mínimo"],
 ["minimizar material", "diseño de envases", "tensión superficial"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 22 (Inequalities)"))

A(P(613, "Máximo producto con suma treinta", "optimizacion", 2,
 "Dos números positivos suman 30. ¿Cuál es su máximo producto posible?",
 ["A suma fija, el producto es máximo cuando los números son iguales.",
  "Por AM-GM, ab ≤ ((a + b)/2)².",
  "= (30/2)² = 15².",
  "La igualdad es a = b = 15.",
  "El producto máximo es 225."],
 "Por AM-GM, ab ≤ (30/2)² = 225, con igualdad en a = b = 15. El máximo es 225. Verificado con Python.",
 "El mismo principio AM-GM con otro total: a + b fijo ⇒ producto máximo en el punto medio. Aquí 15·15 = 225.",
 10, ["AM-GM", "suma fija", "producto máximo"],
 ["áreas", "asignación", "diseño óptimo"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 22 (Inequalities)"))

A(P(614, "Suma mínima con producto fijo", "optimizacion", 2,
 "Dos números positivos x e y cumplen x·y = 36. ¿Cuál es el menor valor posible de x + y?",
 ["A producto fijo, la suma es mínima cuando los números son iguales (AM-GM).",
  "Por AM-GM, x + y ≥ 2√(xy).",
  "= 2√36 = 2·6.",
  "La igualdad ocurre cuando x = y = 6.",
  "La suma mínima es 12."],
 "Por AM-GM, x + y ≥ 2√36 = 12, con igualdad en x = y = 6. El mínimo es 12. Verificado con Python.",
 "El recíproco del problema anterior: a producto fijo, la suma se minimiza con términos iguales. AM-GM funciona en ambos sentidos.",
 10, ["AM-GM", "producto fijo", "suma mínima"],
 ["minimizar costos", "diseño", "economía"],
 "", ["am-gm", "optimizacion", "nivel-basico"], "cap. 22 (Inequalities)"))

A(P(615, "El tercer lado del triángulo", "optimizacion", 3,
 "Un triángulo tiene dos lados de longitudes 5 y 9, y el tercer lado mide un número entero. ¿Cuántos valores enteros distintos puede tomar ese tercer lado?",
 ["La desigualdad triangular acota el tercer lado: debe ser menor que la suma y mayor que la diferencia de los otros dos.",
  "Si el tercer lado es t: |9 − 5| < t < 9 + 5.",
  "Es decir 4 < t < 14.",
  "Los enteros estrictamente entre 4 y 14 son 5, 6, 7, …, 13.",
  "Son 9 valores."],
 "Por la desigualdad triangular, 4 < t < 14, así que t ∈ {5, …, 13}: 9 valores enteros. Verificado con Python.",
 "La desigualdad triangular define el rango válido del tercer lado: entre la diferencia y la suma de los otros dos. Contar los enteros del intervalo abierto da la respuesta.",
 12, ["desigualdad triangular", "rango de valores", "conteo de enteros"],
 ["diseño de estructuras", "rangos factibles", "geometría"],
 "", ["desigualdad-triangular", "optimizacion", "nivel-intermedio"], "cap. 11 (Triangles)"))

A(P(616, "Minimizar una suma de distancias", "optimizacion", 3,
 "¿Cuál es el valor mínimo de |x − 2| + |x − 7| cuando x recorre todos los números reales?",
 ["Interpreta la expresión como la suma de las distancias de x a 2 y a 7 en la recta.",
  "La distancia total de un punto a 2 y a 7 es mínima cuando x está ENTRE 2 y 7.",
  "Para cualquier x entre 2 y 7, las dos distancias suman exactamente la distancia entre 2 y 7.",
  "= 7 − 2.",
  "= 5 (el mínimo, alcanzado para todo x en [2, 7])."],
 "|x−2| + |x−7| es la distancia total a 2 y 7; su mínimo es la distancia entre ellos, 7 − 2 = 5, para cualquier x ∈ [2,7]. Verificado con Python.",
 "Sumar distancias a dos puntos fijos se minimiza colocándose entre ellos: el mínimo es la distancia entre los puntos. Es geometría de la recta, no cálculo.",
 12, ["valor absoluto", "suma de distancias", "interpretación geométrica"],
 ["ubicación de instalaciones", "logística", "optimización"],
 "", ["valor-absoluto", "optimizacion", "nivel-intermedio"], "cap. 22 (Inequalities)"))

A(P(617, "El mayor cuadrado bajo doscientos", "optimizacion", 1,
 "¿Cuál es el mayor entero n tal que n² < 200?",
 ["Busca el cuadrado perfecto más grande que sea menor que 200.",
  "13² = 169 < 200.",
  "14² = 196 < 200.",
  "15² = 225 > 200, así que 15 ya se pasa.",
  "El mayor n es 14."],
 "14² = 196 < 200 y 15² = 225 > 200, así que el mayor n es 14. Verificado con Python.",
 "Maximizar un entero bajo una cota cuadrática es tomar la parte entera de la raíz: ⌊√199⌋ = 14.",
 8, ["maximizar entero", "cota cuadrática", "raíz cuadrada"],
 ["acotar soluciones", "estimación", "diseño con límites"],
 "", ["optimizacion", "nivel-basico"], "cap. 5 (Using the Integers)"))

# =====================================================================
# INVERSION (11) — resolver ecuaciones, proporción inversa, % hacia atrás
# =====================================================================

A(P(618, "Despejar el exponente", "inversion", 1,
 "Resuelve para x: 5ˣ = 625.",
 ["Expresa 625 como potencia de 5 para igualar exponentes (o usa el logaritmo).",
  "625 = 5⁴.",
  "Entonces 5ˣ = 5⁴.",
  "Como las bases coinciden, x = 4.",
  "x = 4."],
 "5ˣ = 625 = 5⁴ ⇒ x = 4. Verificado con Python.",
 "Resolver una ecuación exponencial es deshacer la potencia: igualar exponentes cuando las bases coinciden, o aplicar el logaritmo (su inverso).",
 8, ["ecuación exponencial", "misma base", "logaritmo inverso"],
 ["crecimiento/decaimiento", "finanzas", "complejidad"],
 "", ["exponentes", "inversion", "nivel-basico"], "cap. 1 (Exponents)"))

A(P(619, "La base desconocida", "inversion", 2,
 "Resuelve para x: log_x(64) = 3.",
 ["La ecuación logarítmica dice que x elevado a 3 da 64; deshazla con la definición de logaritmo.",
  "log_x(64) = 3 significa x³ = 64.",
  "Busca el número cuyo cubo es 64.",
  "4³ = 64.",
  "x = 4."],
 "log_x(64) = 3 ⇔ x³ = 64 ⇒ x = 4. Verificado con Python.",
 "La definición de logaritmo invierte la ecuación: log_x(64) = 3 equivale a x³ = 64. Despejar la base es tomar la raíz cúbica.",
 10, ["definición de logaritmo", "ecuación logarítmica", "raíz cúbica"],
 ["escalas", "modelos exponenciales", "álgebra"],
 "", ["logaritmos", "inversion", "nivel-basico"], "cap. 1.5 (Logarithms)"))

A(P(620, "Más obreros, menos días", "inversion", 2,
 "Tres obreros construyen un muro en 12 días. Trabajando al mismo ritmo, ¿cuántos días tardarían 4 obreros en construir el mismo muro?",
 ["Es una proporción INVERSA: más obreros ⇒ menos días. Lo invariante es el trabajo total (obreros × días).",
  "Trabajo total = 3 obreros · 12 días = 36 'obrero-días'.",
  "Con 4 obreros, los días cumplen 4 · días = 36.",
  "días = 36/4.",
  "= 9 días."],
 "El trabajo total es 3·12 = 36 obrero-días; con 4 obreros, días = 36/4 = 9. Verificado con Python.",
 "En proporción inversa, el producto de las cantidades es constante. Reconocer ese invariante (obrero-días) permite despejar hacia atrás los días.",
 10, ["proporción inversa", "producto constante", "trabajo"],
 ["planificación de proyectos", "productividad", "logística"],
 "", ["proporciones", "inversion", "nivel-basico"], "cap. 4 (Proportions)"))

A(P(621, "Deshacer un aumento", "inversion", 2,
 "Un precio aumentó un 20% y quedó en $60. ¿Cuál era el precio original?",
 ["Trabaja hacia atrás: el precio final es 1.20 veces el original, no el original más 20% del final.",
  "Si P es el original, entonces 1.20·P = 60.",
  "Despeja P = 60/1.20.",
  "= 60/(6/5) = 60·(5/6).",
  "= 50."],
 "1.20·P = 60 ⇒ P = 60/1.20 = 50. Verificado con Python.",
 "Para deshacer un aumento porcentual hay que DIVIDIR por el factor (1.20), no restar el 20% del final. Pensar el final como múltiplo del original evita el error común.",
 10, ["porcentaje inverso", "factor multiplicativo", "trabajar hacia atrás"],
 ["precios e impuestos", "descuentos", "finanzas"],
 "", ["porcentajes", "inversion", "nivel-basico"], "cap. 4 (Proportions)"))

A(P(622, "Sistema de dos ecuaciones", "inversion", 2,
 "Resuelve el sistema: x + y = 10 y x − y = 4. ¿Cuánto valen x e y?",
 ["Suma o resta las ecuaciones para eliminar una variable.",
  "Sumando las dos ecuaciones: (x + y) + (x − y) = 10 + 4 ⇒ 2x = 14.",
  "x = 7.",
  "Sustituye en x + y = 10: 7 + y = 10 ⇒ y = 3.",
  "x = 7, y = 3."],
 "Sumando: 2x = 14 ⇒ x = 7; luego y = 3. Verificado con Python.",
 "La eliminación resuelve el sistema sumando ecuaciones para cancelar una variable. Es reconstruir los valores individuales a partir de su suma y su diferencia.",
 10, ["sistema de ecuaciones", "eliminación", "suma y diferencia"],
 ["mezclas", "circuitos", "balance de cuentas"],
 "", ["sistemas", "inversion", "nivel-basico"], "cap. 3 (Linear Equations)"))

A(P(623, "Raíz cuadrada de un negativo", "inversion", 2,
 "Resuelve para z (número complejo): z² = −9. Da la solución con parte imaginaria positiva.",
 ["No hay raíz real de un negativo; usa la unidad imaginaria i, con i² = −1.",
  "Buscas z tal que z² = −9 = 9·(−1).",
  "z = ±√9·√(−1) = ±3i.",
  "La solución con parte imaginaria positiva es 3i.",
  "Comprueba: (3i)² = 9·i² = −9. ✓"],
 "z² = −9 ⇒ z = ±3i; la de parte imaginaria positiva es 3i (pues (3i)² = −9). Verificado con Python.",
 "Los números complejos permiten resolver ecuaciones sin solución real: √(−9) = 3i. Resolver z² = −9 es invertir el cuadrado en el plano complejo.",
 10, ["números complejos", "unidad imaginaria", "z²=−9"],
 ["circuitos de corriente alterna", "ecuaciones diferenciales", "física"],
 "", ["complejos", "inversion", "nivel-basico"], "cap. 2 (Complex Numbers)"))

A(P(624, "Reconstruir la sucesión aritmética", "inversion", 3,
 "En una sucesión aritmética, el tercer término es 10 y el séptimo es 26. ¿Cuál es el primer término?",
 ["Del salto entre el 3.º y el 7.º término recupera la diferencia común; luego retrocede al primero.",
  "Del término 3 al 7 hay 4 pasos: a₇ − a₃ = 4·d ⇒ 26 − 10 = 4d ⇒ d = 4.",
  "El primer término es a₃ menos 2 pasos: a₁ = a₃ − 2d.",
  "= 10 − 2·4.",
  "= 2."],
 "d = (26 − 10)/4 = 4; a₁ = a₃ − 2d = 10 − 8 = 2. Verificado con Python.",
 "Dos términos cualesquiera determinan la diferencia común (por su separación) y, retrocediendo, el primer término. Es resolver la sucesión hacia atrás.",
 12, ["sucesión aritmética", "diferencia común", "reconstruir a₁"],
 ["interpolación", "calibración", "modelos lineales"],
 "", ["sucesiones", "inversion", "nivel-intermedio"], "cap. 24 (Sequences and Series)"))

A(P(625, "Reconstruir la sucesión geométrica", "inversion", 3,
 "En una sucesión geométrica de términos positivos, el segundo término es 6 y el cuarto es 54. ¿Cuál es el primer término?",
 ["Del cociente entre el 4.º y el 2.º término recupera la razón; luego retrocede al primero.",
  "a₄/a₂ = r², así que 54/6 = r² ⇒ r² = 9 ⇒ r = 3 (positivo).",
  "El primer término es a₂ dividido entre r: a₁ = a₂/r.",
  "= 6/3.",
  "= 2."],
 "r² = a₄/a₂ = 9 ⇒ r = 3; a₁ = a₂/r = 6/3 = 2. Verificado con Python.",
 "En una geométrica, la razón entre términos separados k posiciones es rᵏ; recuperarla permite retroceder al primer término dividiendo.",
 12, ["sucesión geométrica", "razón común", "reconstruir a₁"],
 ["interés compuesto", "decaimiento", "modelos exponenciales"],
 "", ["sucesiones", "geometrica", "inversion", "nivel-intermedio"], "cap. 24 (Sequences and Series)"))

A(P(626, "Deshacer la función", "inversion", 2,
 "Sea f(x) = 3x − 5. ¿Para qué valor de x se cumple f(x) = 16?",
 ["Deshaz las operaciones de f en orden inverso para despejar x.",
  "f multiplica por 3 y resta 5; para invertir, primero suma 5 y luego divide entre 3.",
  "Plantea 3x − 5 = 16.",
  "3x = 21.",
  "x = 7."],
 "3x − 5 = 16 ⇒ 3x = 21 ⇒ x = 7. Verificado con Python.",
 "Resolver f(x) = valor es aplicar la función inversa: deshacer cada operación en orden contrario (sumar el 5, dividir por el 3).",
 10, ["función inversa", "despejar", "orden inverso"],
 ["decodificación", "conversión de unidades", "criptografía"],
 "", ["funciones", "inversion", "nivel-basico"], "cap. 21 (Functions)"))

A(P(627, "Deshacer un descuento", "inversion", 2,
 "Tras un descuento del 25%, un artículo cuesta $90. ¿Cuál era su precio original?",
 ["Trabaja hacia atrás: el precio final es el 75% del original (100% − 25%).",
  "Si P es el original, 0.75·P = 90.",
  "Despeja P = 90/0.75.",
  "= 90/(3/4) = 90·(4/3).",
  "= 120."],
 "0.75·P = 90 ⇒ P = 90/0.75 = 120. Verificado con Python.",
 "Para deshacer un descuento se divide por el factor restante (0.75), no se suma el 25% del precio rebajado. El precio final es una fracción del original.",
 10, ["porcentaje inverso", "factor de descuento", "trabajar hacia atrás"],
 ["precios y rebajas", "impuestos", "finanzas personales"],
 "", ["porcentajes", "inversion", "nivel-basico"], "cap. 4 (Proportions)"))

A(P(628, "El número y su cuadrado", "inversion", 2,
 "Un número entero positivo, sumado a su propio cuadrado, da 42. ¿Cuál es el número?",
 ["Traduce a una ecuación cuadrática y resuélvela.",
  "Sea x el número: x² + x = 42, es decir x² + x − 42 = 0.",
  "Factoriza: busca dos números que multipliquen −42 y sumen 1: 7 y −6.",
  "(x + 7)(x − 6) = 0, con raíces x = −7 y x = 6.",
  "Como se pide positivo, x = 6 (y en efecto 6² + 6 = 42)."],
 "x² + x = 42 ⇒ (x + 7)(x − 6) = 0 ⇒ x = 6 (positivo). Verificado con Python.",
 "Plantear y factorizar la cuadrática reconstruye el número desde la condición. La factorización busca dos enteros con producto −42 y suma 1.",
 10, ["ecuación cuadrática", "factorización", "raíz positiva"],
 ["modelado de problemas", "diseño", "álgebra aplicada"],
 "", ["cuadratica", "inversion", "nivel-basico"], "cap. 6 (Quadratic Equations)"))

# =====================================================================
# Validación de balance y append idempotente
# =====================================================================
assert len(PROBLEMS) == 44, len(PROBLEMS)
bal = collections.Counter(p["estrategia"] for p in PROBLEMS)
assert bal["inversion"] == bal["optimizacion"] == bal["invariantes"] == bal["patrones"] == 11, bal
ids = [p["id"] for p in PROBLEMS]
assert ids == list(range(585, 629)), ids
assert len(set(ids)) == 44

PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
clash = existing & set(ids)
assert not clash, ("choque de ids", clash)

data["problemas"].extend(PROBLEMS)
gbal = collections.Counter(p["estrategia"] for p in data["problemas"])
print("balance global tras append:", dict(gbal))
assert all(v == 157 for v in gbal.values()), gbal

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: añadidos {len(PROBLEMS)} problemas (ids {ids[0]}-{ids[-1]}). Total = {len(data['problemas'])}.")
