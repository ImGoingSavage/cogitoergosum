# -*- coding: utf-8 -*-
"""Tanda 36 — David Patrick, *Introduction to Counting & Probability* (Art of Problem Solving).
Append 44 problemas verificados a data/problems.json. Fuentes internas (TOC verificado;
leídas las secciones de Review/Challenge de los caps. 2, 3, 4, 8 y 11):
 - Cap. 2 «Basic Counting Techniques» (casework, conteo complementario, constructivo,
   restricciones) y Cap. 3 «Correcting for Overcounting» (permutaciones con repetidos,
   simetrías circulares).
 - Cap. 4 «Committees and Combinations» (C(n,r), identidad C(n,r)=C(n,n-r)) y Cap. 5
   «More with Combinations» (caminos en cuadrícula).
 - Cap. 8 «Basic Probability Techniques» (suma/complemento/producto de probabilidades).
 - Cap. 11 «Expected Value» y Cap. 12 «Pascal's Triangle» (identidades, hockey stick).
Mapeo a las 4 estrategias canónicas (11 c/u, balance GLOBAL -> 124/124/124/124):
 - patrones: fórmulas y regularidades combinatorias (permutaciones con repetidos, C(n,r),
   identidades de Pascal / hockey stick, caminos en cuadrícula, palíndromos).
 - invariantes: conteo complementario (total fijo), corrección de sobreconteo por división
   (multiplicidad constante), P(A)+P(no A)=1, valor esperado como promedio ponderado.
 - optimizacion: máximos/mínimos y garantías (palomar/pigeonhole, menor n, decisión por
   valor esperado).
 - inversion: reconstruir n hacia atrás desde un conteo o una probabilidad; «contar lo que
   no quieres» (complementario) para llegar a lo que sí.
TODA afirmación numérica verificada con Python (math.comb/factorial, fractions; 44 checks,
todas OK). El volumen de SOLUCIONES de AoPS es un libro aparte no disponible: cada número se
resolvió y comprobó de forma independiente. Builder idempotente: aborta si hay choque de ids.
Sector C (entrenamiento), esquema §4.1, ids 453-496."""
import json, collections

SRC = "Patrick, *Introduction to Counting & Probability* (Art of Problem Solving)"

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
# PATRONES (11) — permutaciones con repetidos, C(n,r), Pascal, cuadrícula
# =====================================================================

A(P(453, "Las letras de BANANA", "patrones", 2,
 "¿Cuántos arreglos distintos de las letras de la palabra BANANA existen?",
 ["Si las 6 letras fueran distintas habría 6! arreglos. Pero hay letras repetidas que generan arreglos idénticos.",
  "BANANA tiene 3 A y 2 N (y 1 B). Esas repeticiones causan sobreconteo.",
  "Por cada arreglo real, las 3 A se pueden permutar de 3! formas y las 2 N de 2! formas sin cambiar la palabra.",
  "Divide para corregir: 6! / (3!·2!).",
  "= 720 / (6·2) = 60."],
 "Arreglos = 6! / (3!·2!) = 720/12 = 60, dividiendo por las permutaciones de las 3 A y las 2 N repetidas. Verificado con Python.",
 "La fórmula de permutaciones con repetición, n!/(a!·b!·…), corrige el sobreconteo dividiendo por las permutaciones de cada grupo de letras iguales. Es un patrón que aparece sin cesar.",
 12, ["permutaciones con repetición", "corregir sobreconteo", "factorial"],
 ["anagramas", "secuencias de ADN", "arreglos con elementos idénticos"],
 "", ["conteo", "permutaciones", "patron", "nivel-basico"], "cap. 3.2 (Prob. 3.2.2)"))

A(P(454, "El clásico MISSISSIPPI", "patrones", 3,
 "¿De cuántas maneras distintas se pueden ordenar las letras de la palabra MISSISSIPPI?",
 ["Cuenta cuántas veces aparece cada letra: ese es el dato que corrige el sobreconteo.",
  "MISSISSIPPI tiene 11 letras: 1 M, 4 I, 4 S, 2 P.",
  "Si todas fueran distintas serían 11!. Divide por las permutaciones de cada grupo repetido.",
  "11! / (4!·4!·2!·1!).",
  "= 39 916 800 / (24·24·2) = 34 650."],
 "Arreglos = 11! / (4!·4!·2!·1!) = 39 916 800 / 1152 = 34 650. Verificado con Python.",
 "La misma fórmula de permutaciones con repetición escala a cualquier número de grupos: un factorial en el numerador, el factorial de cada repetición en el denominador.",
 14, ["permutaciones con repetición", "factorial", "conteo"],
 ["anagramas largos", "bioinformática", "códigos con símbolos repetidos"],
 "", ["conteo", "permutaciones", "patron", "nivel-intermedio"], "cap. 3.2 (Prob. 3.2.3l)"))

A(P(455, "La combinación con atajo", "patrones", 2,
 "Calcula C(10, 8) (el número de maneras de elegir 8 objetos de entre 10).",
 ["Elegir 8 para incluir equivale a elegir cuáles 2 dejar fuera: ese es el patrón de simetría de las combinaciones.",
  "La identidad C(n, r) = C(n, n−r) convierte C(10, 8) en algo más fácil.",
  "C(10, 8) = C(10, 2).",
  "C(10, 2) = (10·9)/(2·1).",
  "= 90/2 = 45."],
 "Por la identidad C(n,r) = C(n,n−r): C(10,8) = C(10,2) = (10·9)/2 = 45. Verificado con Python.",
 "La simetría C(n,r) = C(n,n−r) refleja que elegir lo que entra es lo mismo que elegir lo que queda fuera. Usarla evita factoriales grandes.",
 10, ["combinaciones", "identidad C(n,r)=C(n,n−r)", "simetría"],
 ["selección de subconjuntos", "muestreo", "combinatoria"],
 "", ["combinaciones", "patron", "nivel-basico"], "cap. 4.4 (Prob. 4.9)"))

A(P(456, "Caminos por la cuadrícula", "patrones", 3,
 "En una cuadrícula, debes ir de la esquina inferior izquierda a la esquina superior derecha moviéndote solo hacia la DERECHA o hacia ARRIBA. Si el trayecto requiere 4 pasos a la derecha y 4 pasos hacia arriba, ¿cuántos caminos distintos hay?",
 ["Cada camino es una secuencia de 8 pasos: 4 'derecha' (D) y 4 'arriba' (A). Cuenta las secuencias distintas.",
  "El problema es ordenar la palabra DDDDAAAA: elegir en cuáles de los 8 lugares van las D.",
  "Eso es C(8, 4) (elegir 4 posiciones de 8 para las D).",
  "C(8, 4) = 8!/(4!·4!).",
  "= 70."],
 "Cada camino es una permutación de 4 D y 4 A, es decir C(8,4) = 70. Verificado con Python.",
 "Los caminos en cuadrícula con pasos D/A se cuentan como permutaciones con repetición, equivalentes a C(m+n, m). Es un patrón que conecta geometría con combinaciones.",
 14, ["caminos en cuadrícula", "C(m+n,m)", "permutación con repetición"],
 ["rutas en mapas", "algoritmos sobre matrices", "modelos de difusión"],
 "", ["combinaciones", "cuadricula", "patron", "nivel-intermedio"], "cap. 5.2 (Paths on a Grid)"))

A(P(457, "Sumar toda una fila de Pascal", "patrones", 2,
 "¿Cuánto vale C(4,0) + C(4,1) + C(4,2) + C(4,3) + C(4,4)?",
 ["Esta suma cuenta TODOS los subconjuntos de un conjunto de 4 elementos (de tamaño 0, 1, 2, 3 y 4).",
  "Un conjunto de n elementos tiene 2ⁿ subconjuntos en total.",
  "Por tanto la suma de toda la fila n del triángulo de Pascal es 2ⁿ.",
  "Aquí n = 4.",
  "2⁴ = 16. (En efecto 1+4+6+4+1 = 16.)"],
 "La suma de la fila n de Pascal cuenta todos los subconjuntos de un n-conjunto: ∑ C(n,k) = 2ⁿ. Para n = 4 da 16 (= 1+4+6+4+1). Verificado con Python.",
 "Cada elemento está o no en un subconjunto (2 opciones), de ahí 2ⁿ subconjuntos. Esa es la razón combinatoria de que cada fila de Pascal sume una potencia de 2.",
 10, ["suma de fila de Pascal", "∑C(n,k)=2ⁿ", "subconjuntos"],
 ["conteo de subconjuntos", "lógica booleana", "espacios de estados"],
 "", ["combinaciones", "pascal", "patron", "nivel-basico"], "cap. 12 / 4.5 (Prob. 4.18a)"))

A(P(458, "El palo de hockey", "patrones", 3,
 "¿Cuánto vale C(2,2) + C(3,2) + C(4,2) + C(5,2) + C(6,2) + C(7,2)?",
 ["Esta suma de combinaciones 'en diagonal' del triángulo de Pascal tiene una identidad propia (la del 'palo de hockey').",
  "La identidad del palo de hockey dice: C(r,r) + C(r+1,r) + … + C(n,r) = C(n+1, r+1).",
  "Aquí r = 2 y el último término es C(7,2), así que n = 7.",
  "La suma vale C(7+1, 2+1) = C(8, 3).",
  "C(8,3) = 56. (Comprueba: 1+3+6+10+15+21 = 56.)"],
 "Por la identidad del palo de hockey, C(2,2)+…+C(7,2) = C(8,3) = 56 (= 1+3+6+10+15+21). Verificado con Python.",
 "La identidad del palo de hockey suma una diagonal del triángulo de Pascal en un solo número. Reconocer ese patrón ahorra sumar término a término.",
 14, ["identidad del palo de hockey", "diagonal de Pascal", "combinaciones"],
 ["sumas telescópicas", "conteo combinatorio", "fórmulas cerradas"],
 "", ["combinaciones", "pascal", "patron", "nivel-intermedio"], "cap. 13 (Hockey Stick Identity)"))

A(P(459, "Triángulos en un dodecágono", "patrones", 2,
 "¿Cuántos triángulos se pueden formar usando como vértices los del dodecágono regular (polígono de 12 lados)?",
 ["Un triángulo queda determinado por la ELECCIÓN de 3 de los vértices; el orden no importa.",
  "Como no hay tres vértices alineados en un polígono convexo, cualquier terna de vértices forma un triángulo.",
  "Cuenta las maneras de elegir 3 vértices de 12: C(12, 3).",
  "C(12,3) = (12·11·10)/(3·2·1).",
  "= 1320/6 = 220."],
 "Cada triángulo es una elección de 3 vértices de 12: C(12,3) = 220. Verificado con Python.",
 "Contar figuras determinadas por puntos es contar combinaciones de esos puntos (el orden no importa). En un polígono convexo, toda terna da un triángulo válido.",
 10, ["combinaciones", "C(12,3)", "elegir vértices"],
 ["geometría combinatoria", "redes", "diseño de conexiones"],
 "", ["combinaciones", "geometria", "patron", "nivel-basico"], "cap. 4 (Prob. 4.16)"))

A(P(460, "Rectángulos en una cuadrícula de puntos", "patrones", 3,
 "En un arreglo de puntos de 4×4, ¿cuántos rectángulos con lados paralelos a la cuadrícula se pueden formar uniendo cuatro de los puntos?",
 ["Un rectángulo con lados paralelos queda fijado al elegir DOS líneas verticales y DOS horizontales.",
  "En un arreglo 4×4 de puntos hay 4 líneas verticales y 4 horizontales.",
  "Elige 2 verticales de 4 y 2 horizontales de 4, de forma independiente.",
  "C(4,2)·C(4,2).",
  "= 6·6 = 36."],
 "Un rectángulo se fija eligiendo 2 de las 4 líneas verticales y 2 de las 4 horizontales: C(4,2)·C(4,2) = 6·6 = 36. Verificado con Python.",
 "Muchos conteos geométricos se reducen a elegir las líneas o puntos que determinan la figura. Aquí dos elecciones independientes se multiplican.",
 14, ["combinaciones", "elegir líneas", "regla del producto"],
 ["diseño de tableros", "procesamiento de imágenes", "geometría combinatoria"],
 "", ["combinaciones", "cuadricula", "patron", "nivel-intermedio"], "cap. 4 (Prob. 4.17)"))

A(P(461, "Contar palíndromos de cuatro cifras", "patrones", 2,
 "¿Cuántos números capicúa (palíndromos) de cuatro cifras existen? (Un capicúa se lee igual de izquierda a derecha que de derecha a izquierda, como 1221.)",
 ["Un palíndromo de 4 cifras tiene la forma 'abba': el tercer dígito repite al segundo y el cuarto al primero.",
  "Así que basta elegir libremente los dos primeros dígitos a y b; los otros dos quedan forzados.",
  "El primer dígito a no puede ser 0 (si no, no sería de cuatro cifras): 9 opciones.",
  "El segundo dígito b puede ser cualquiera: 10 opciones.",
  "Total = 9·10 = 90."],
 "Un palíndromo de 4 cifras es 'abba'; se eligen a (9 opciones, no 0) y b (10 opciones), y el resto queda determinado: 9·10 = 90. Verificado con Python.",
 "Una estructura simétrica reduce las elecciones libres a la mitad: solo la primera mitad del número decide, la otra se refleja. Es conteo constructivo sobre el patrón de simetría.",
 10, ["palíndromos", "conteo constructivo", "simetría"],
 ["detección de simetrías", "códigos", "secuencias reversibles"],
 "", ["conteo", "palindromo", "patron", "nivel-basico"], "cap. 2 (Prob. 2.31a)"))

A(P(462, "La regla de Pascal", "patrones", 2,
 "¿Cuánto vale C(6,1) + C(6,2)? Relaciónalo con una sola combinación.",
 ["Hay una identidad que suma dos combinaciones contiguas de la misma fila: la regla de Pascal.",
  "La regla de Pascal: C(n,k) + C(n,k+1) = C(n+1, k+1).",
  "Aquí n = 6 y k = 1, así que C(6,1) + C(6,2) = C(7, 2).",
  "C(7,2) = (7·6)/2 = 21.",
  "(Comprueba directo: C(6,1)+C(6,2) = 6 + 15 = 21.)"],
 "Por la regla de Pascal, C(6,1) + C(6,2) = C(7,2) = 21 (= 6 + 15). Verificado con Python.",
 "La regla de Pascal —cada número del triángulo es la suma de los dos de arriba— es el patrón que genera todo el triángulo y la base de muchas identidades combinatorias.",
 10, ["regla de Pascal", "C(n,k)+C(n,k+1)=C(n+1,k+1)", "triángulo de Pascal"],
 ["recurrencias", "programación dinámica", "coeficientes binomiales"],
 "", ["combinaciones", "pascal", "patron", "nivel-basico"], "cap. 12 / 4.5 (Prob. 4.18b,c)"))

A(P(463, "Anagramas de TATTER", "patrones", 2,
 "¿Cuántos arreglos distintos de las letras de la palabra TATTER existen?",
 ["Cuenta las letras y sus repeticiones: TATTER tiene 6 letras, con la T repetida.",
  "Hay 3 T (y 1 A, 1 E, 1 R). Si todas fueran distintas habría 6! arreglos.",
  "Las 3 T se pueden permutar de 3! maneras sin cambiar la palabra: hay que dividir.",
  "6! / 3!.",
  "= 720/6 = 120."],
 "Arreglos = 6! / 3! = 720/6 = 120, corrigiendo el sobreconteo de las 3 T repetidas. Verificado con Python.",
 "Cuando solo un grupo de letras se repite, se divide por el factorial de ese grupo. Es el mismo patrón de permutaciones con repetición, en su forma más simple.",
 10, ["permutaciones con repetición", "factorial", "anagramas"],
 ["anagramas", "secuencias", "arreglos con repetidos"],
 "", ["conteo", "permutaciones", "patron", "nivel-basico"], "cap. 3.2 (Prob. 3.3)"))

# =====================================================================
# INVARIANTES (11) — conteo complementario, sobreconteo, P(A)+P(no A)=1
# =====================================================================

A(P(464, "Los que NO son cuadrados perfectos", "invariantes", 2,
 "¿Cuántos números entre 100 y 200 (ambos inclusive) NO son cuadrados perfectos?",
 ["Es más fácil contar los que SÍ son cuadrados perfectos y restarlos del total. El total no cambia.",
  "Total de números de 100 a 200 inclusive: 200 − 100 + 1 = 101.",
  "Cuadrados perfectos en ese rango: 10²=100, 11²=121, 12²=144, 13²=169, 14²=196 (15²=225 ya se pasa).",
  "Son 5 cuadrados perfectos.",
  "Los que NO lo son: 101 − 5 = 96."],
 "Total = 101 números. Cuadrados perfectos: 100, 121, 144, 169, 196 (5 en total). Los que no son cuadrados: 101 − 5 = 96. Verificado con Python.",
 "El conteo complementario usa que el total es un invariante: (lo que quieres) = (total) − (lo que no quieres). Contar los pocos cuadrados es más fácil que listar los 96 restantes.",
 10, ["conteo complementario", "total invariante", "cuadrados perfectos"],
 ["filtrado de datos", "conteo por exclusión", "estimación"],
 "", ["conteo", "complementario", "invariante", "nivel-basico"], "cap. 2 (Prob. 2.20)"))

A(P(465, "Alrededor de la mesa redonda", "invariantes", 2,
 "¿De cuántas maneras distintas pueden sentarse 6 personas alrededor de una mesa redonda? (Dos arreglos se consideran iguales si cada persona tiene los mismos vecinos; es decir, las rotaciones de la mesa no cuentan como distintas.)",
 ["Si la mesa fuera una fila habría 6! arreglos. Pero en una mesa redonda, rotar a todos no cambia el arreglo.",
  "Cada arreglo circular se cuenta 6 veces entre los 6! lineales (una por cada rotación).",
  "Para corregir ese sobreconteo, divide entre 6 (el número de asientos).",
  "6!/6 = 5!.",
  "= 120."],
 "Arreglos circulares = 6!/6 = 5! = 120, dividiendo los 6! lineales por las 6 rotaciones equivalentes. Verificado con Python.",
 "En arreglos circulares, la multiplicidad del sobreconteo es constante (igual al número de rotaciones, n). Por eso (n−1)! cuenta los arreglos de n personas en círculo.",
 12, ["permutaciones circulares", "sobreconteo por rotación", "(n−1)!"],
 ["disposición de mesas", "collares y pulseras", "simetrías cíclicas"],
 "", ["conteo", "circular", "invariante", "nivel-basico"], "cap. 3 (Permutaciones circulares)"))

A(P(466, "Al menos una cara", "invariantes", 2,
 "Se lanza una moneda equilibrada 3 veces. ¿Cuál es la probabilidad de obtener al menos una cara?",
 ["'Al menos una' invita a usar el complemento: es más fácil calcular la probabilidad de NINGUNA cara.",
  "El complemento de 'al menos una cara' es 'ninguna cara', es decir, las tres salen cruz.",
  "P(tres cruces) = (1/2)³ = 1/8.",
  "Como P(evento) + P(complemento) = 1, P(al menos una cara) = 1 − 1/8.",
  "= 7/8."],
 "P(al menos una cara) = 1 − P(ninguna cara) = 1 − (1/2)³ = 1 − 1/8 = 7/8. Verificado con Python.",
 "La identidad P(A) + P(no A) = 1 es un invariante: la probabilidad total siempre suma 1. 'Al menos uno' casi siempre se calcula mejor por su complemento 'ninguno'.",
 10, ["probabilidad complementaria", "P(A)+P(no A)=1", "al menos uno"],
 ["fiabilidad de sistemas", "control de calidad", "redundancia"],
 "", ["probabilidad", "complementario", "invariante", "nivel-basico"], "cap. 8 (Complementary Probabilities)"))

A(P(467, "Un divisor de seis", "invariantes", 1,
 "Se lanza un dado equilibrado de 6 caras. ¿Cuál es la probabilidad de que el número que salga sea un divisor de 6?",
 ["Cuenta los resultados favorables sobre los 6 igualmente probables.",
  "Los divisores de 6 entre 1 y 6 son: 1, 2, 3 y 6.",
  "Son 4 resultados favorables.",
  "Probabilidad = favorables / total = 4/6.",
  "= 2/3."],
 "Los divisores de 6 en {1,…,6} son 1, 2, 3, 6 (4 casos). Probabilidad = 4/6 = 2/3. Verificado con Python.",
 "Con resultados igualmente probables, la probabilidad es (favorables)/(total). El total de 6 resultados es el invariante del espacio muestral.",
 6, ["probabilidad clásica", "resultados equiprobables", "divisores"],
 ["juegos de azar", "muestreo uniforme", "simulación"],
 "", ["probabilidad", "invariante", "nivel-basico"], "cap. 8 (Prob. 8.17)"))

A(P(468, "Tres cartas, no todas del mismo color", "invariantes", 4,
 "Se eligen 3 cartas al azar de una baraja estándar de 52 (26 rojas y 26 negras). ¿Cuál es la probabilidad de que NO sean las tres del mismo color?",
 ["'No todas del mismo color' pide el complemento de 'las tres del mismo color'.",
  "Maneras de elegir 3 cartas de 52: C(52,3). Maneras de que las 3 sean del mismo color: 2·C(26,3) (rojas o negras).",
  "P(las tres del mismo color) = 2·C(26,3)/C(52,3).",
  "C(26,3) = 2600 y C(52,3) = 22100, así que P(mismo color) = 5200/22100 = 4/17.",
  "P(no todas del mismo color) = 1 − 4/17 = 13/17."],
 "P(las tres del mismo color) = 2·C(26,3)/C(52,3) = 5200/22100 = 4/17. Por complemento, P(no todas del mismo color) = 1 − 4/17 = 13/17. Verificado con Python.",
 "El complemento ('todas iguales') es un solo caso fácil de contar, frente a la casuística de 'no todas iguales'. La probabilidad total 1 hace el resto.",
 18, ["probabilidad complementaria", "combinaciones", "casos por color"],
 ["control de calidad por muestreo", "genética de poblaciones", "auditoría"],
 "", ["probabilidad", "complementario", "invariante", "nivel-avanzado"], "cap. 8 (Prob. 8.22)"))

A(P(469, "El dado par que paga", "invariantes", 2,
 "Se lanza un dado equilibrado de 6 caras. Si el resultado es par, ganas esa cantidad de dólares; si es impar, no ganas nada. ¿Cuál es el valor esperado de tu ganancia?",
 ["El valor esperado es el promedio ponderado de las ganancias por su probabilidad. Cada cara tiene probabilidad 1/6.",
  "Caras pares: 2, 4, 6 (ganas esa cantidad). Caras impares: 1, 3, 5 (ganas 0).",
  "E = (1/6)(0) + (1/6)(2) + (1/6)(0) + (1/6)(4) + (1/6)(0) + (1/6)(6).",
  "= (2 + 4 + 6)/6 = 12/6.",
  "= 2 dólares."],
 "E = (2 + 4 + 6)/6 = 12/6 = 2 dólares (las caras impares aportan 0). Verificado con Python.",
 "El valor esperado pondera cada resultado por su probabilidad, que suman 1 (invariante). Aquí, con caras equiprobables, basta promediar las ganancias de las seis caras.",
 10, ["valor esperado", "promedio ponderado", "probabilidades suman 1"],
 ["decisiones bajo riesgo", "seguros", "juegos de apuestas"],
 "", ["probabilidad", "valor-esperado", "invariante", "nivel-basico"], "cap. 11 (Prob. 11.6)"))

A(P(470, "Cinco libros, dos idénticos", "invariantes", 2,
 "Tengo 5 libros; dos de ellos son copias idénticas del mismo libro de matemáticas (los otros tres son todos distintos). ¿De cuántas maneras puedo acomodarlos en un estante?",
 ["Si los 5 libros fueran distintos habría 5! ordenamientos, pero las dos copias idénticas generan duplicados.",
  "Intercambiar las dos copias idénticas no produce un arreglo nuevo.",
  "Cada arreglo real se cuenta 2! = 2 veces entre los 5!.",
  "Divide para corregir: 5! / 2!.",
  "= 120/2 = 60."],
 "Arreglos = 5! / 2! = 120/2 = 60, dividiendo por las 2! permutaciones de las copias idénticas. Verificado con Python.",
 "El sobreconteo por objetos idénticos se corrige con una división constante (aquí entre 2!). Es el mismo invariante que en los anagramas con letras repetidas.",
 10, ["sobreconteo", "objetos idénticos", "factorial"],
 ["organización de inventarios", "arreglos con duplicados", "logística"],
 "", ["conteo", "permutaciones", "invariante", "nivel-basico"], "cap. 3.2 (Prob. 3.2.4)"))

A(P(471, "Al menos dos letras seguidas iguales", "invariantes", 4,
 "¿Cuántas 'palabras' de 5 letras (cualquier cadena de 5 letras del alfabeto de 26 cuenta como palabra) tienen al menos dos letras consecutivas iguales?",
 ["'Al menos dos consecutivas iguales' es difícil de contar directo; cuenta el complemento: las que NO tienen dos seguidas iguales.",
  "Total de palabras de 5 letras: 26⁵.",
  "Palabras sin dos consecutivas iguales: la 1ª letra 26 opciones, y cada siguiente debe diferir de la anterior, 25 opciones: 26·25⁴.",
  "Las que SÍ tienen alguna repetición consecutiva = 26⁵ − 26·25⁴.",
  "= 11 881 376 − 10 156 250 = 1 725 126."],
 "Total = 26⁵ = 11 881 376. Sin dos consecutivas iguales = 26·25⁴ = 10 156 250. Con al menos un par consecutivo = 26⁵ − 26·25⁴ = 1 725 126. Verificado con Python.",
 "El complemento ('ninguna repetición consecutiva') se cuenta fácil porque cada letra solo debe evitar a su vecina previa. El total 26⁵ es el invariante del que se resta.",
 18, ["conteo complementario", "regla del producto", "restricción local"],
 ["validación de contraseñas", "secuencias sin repetición", "autómatas"],
 "", ["conteo", "complementario", "invariante", "nivel-avanzado"], "cap. 2 (Prob. 2.34)"))

A(P(472, "Repartir las jaulas", "invariantes", 3,
 "Hay 8 jaulas en fila. Se deben asignar 4 jaulas a perros, 3 a gatos y 1 a gallos. ¿De cuántas maneras puede hacerse la asignación?",
 ["Es como ordenar la 'palabra' PPPP GGG R, con 4 P, 3 G y 1 R: cuenta los arreglos distintos.",
  "Si las 8 etiquetas fueran distintas habría 8!, pero los animales del mismo tipo son intercambiables.",
  "Divide por las permutaciones dentro de cada grupo: 4! (perros), 3! (gatos), 1! (gallos).",
  "8! / (4!·3!·1!).",
  "= 40 320 / (24·6) = 280."],
 "Asignaciones = 8! / (4!·3!·1!) = 40 320/144 = 280. Verificado con Python.",
 "Repartir posiciones entre grupos indistinguibles es una permutación con repetición; equivale al coeficiente multinomial. La división por cada factorial corrige el sobreconteo.",
 14, ["coeficiente multinomial", "permutación con repetición", "asignación a grupos"],
 ["asignación de recursos", "particiones", "planificación de turnos"],
 "", ["conteo", "permutaciones", "invariante", "nivel-intermedio"], "cap. 3.2 (Prob. 3.2.5)"))

A(P(473, "Dos cartas de figura", "invariantes", 3,
 "Se eligen al azar 2 cartas de una baraja estándar de 52. ¿Cuál es la probabilidad de que ambas sean cartas de figura (J, Q o K)? (Hay 12 cartas de figura.)",
 ["Calcula la probabilidad como producto de eventos dependientes, o como cociente de combinaciones.",
  "P(primera es figura) = 12/52. Tras sacarla, quedan 11 figuras de 51 cartas.",
  "P(segunda figura | primera figura) = 11/51.",
  "Multiplica: (12/52)·(11/51) = 132/2652.",
  "Simplifica: 132/2652 = 11/221."],
 "P(ambas figura) = (12/52)·(11/51) = 132/2652 = 11/221. Verificado con Python.",
 "Para eventos dependientes (sin reemplazo) se multiplican las probabilidades actualizando el espacio: el total de cartas disponibles cambia, pero la regla del producto se mantiene.",
 12, ["probabilidad con dependencia", "regla del producto", "sin reemplazo"],
 ["muestreo sin reemplazo", "control de calidad", "juegos de cartas"],
 "", ["probabilidad", "invariante", "nivel-intermedio"], "cap. 8 (Prob. 8.21a)"))

A(P(474, "Las letras de PAPA", "invariantes", 1,
 "¿Cuántos arreglos distintos de las letras de la palabra PAPA existen?",
 ["PAPA tiene 4 letras con dos repeticiones: 2 P y 2 A.",
  "Si todas fueran distintas serían 4! = 24 arreglos.",
  "Las 2 P se permutan de 2! maneras y las 2 A de 2! maneras sin cambiar la palabra.",
  "Divide: 4! / (2!·2!).",
  "= 24 / 4 = 6."],
 "Arreglos = 4! / (2!·2!) = 24/4 = 6, corrigiendo el sobreconteo de las dos P y las dos A. Verificado con Python.",
 "Con dos grupos repetidos se divide por el producto de sus factoriales (2!·2!), no por su suma. El sobreconteo de cada grupo es independiente.",
 8, ["permutaciones con repetición", "dos grupos repetidos", "factorial"],
 ["anagramas", "arreglos simétricos", "combinatoria básica"],
 "", ["conteo", "permutaciones", "invariante", "nivel-basico"], "cap. 3.2 (Prob. 3.4)"))

# =====================================================================
# OPTIMIZACION (11) — máximos/mínimos, garantías (palomar), decisión por EV
# =====================================================================

A(P(475, "¿Cuántas fotos bastan?", "optimizacion", 3,
 "Cada foto que tomo tiene 1/4 de probabilidad de que todos miren a la cámara. ¿Cuál es el menor número de fotos que debo tomar para tener al menos 4/5 de probabilidad de conseguir una foto donde todos miren?",
 ["Quieres P(al menos una buena) ≥ 4/5. Usa el complemento: P(ninguna buena).",
  "Cada foto NO es buena con probabilidad 3/4. Con n fotos independientes, P(ninguna buena) = (3/4)ⁿ.",
  "P(al menos una buena) = 1 − (3/4)ⁿ ≥ 4/5, o sea (3/4)ⁿ ≤ 1/5.",
  "Prueba valores: (3/4)⁵ = 243/1024 ≈ 0.237 > 0.2; (3/4)⁶ ≈ 0.178 < 0.2.",
  "El menor n que cumple es 6."],
 "Hace falta (3/4)ⁿ ≤ 1/5. (3/4)⁵ ≈ 0.237 (no basta) y (3/4)⁶ ≈ 0.178 (sí). El menor número de fotos es 6. Verificado con Python.",
 "Para 'cuántos intentos garantizan cierta probabilidad', se plantea la desigualdad con el complemento y se busca el menor entero que la satisface. La probabilidad de fallar cae geométricamente.",
 14, ["probabilidad complementaria", "desigualdad geométrica", "menor n"],
 ["pruebas redundantes", "control de fallos", "diseño de reintentos"],
 "", ["probabilidad", "optimizacion", "nivel-intermedio"], "cap. 8 (Prob. 8.36)"))

A(P(476, "¿Cuántos helicópteros contratar?", "optimizacion", 4,
 "Un tesoro de $100 000 cayó en un pantano; si no lo encuentras hoy, se hunde para siempre. Puedes contratar helicópteros: cada uno cuesta $1 000 por el día y tiene 90% de probabilidad de encontrar el tesoro. ¿Cuántos helicópteros debes contratar para maximizar tu ganancia esperada?",
 ["Escribe la ganancia esperada con k helicópteros y busca el k que la maximiza.",
  "Cada helicóptero falla con probabilidad 0.1; con k independientes, P(ninguno lo encuentra) = 0.1ᵏ.",
  "Ganancia esperada = 100 000·(1 − 0.1ᵏ) − 1 000·k.",
  "Evalúa: k=1 → 89 000; k=2 → 99 000 − 2 000 = 97 000; k=3 → 99 900 − 3 000 = 96 900.",
  "Después de k=2 el ingreso extra es menor que el costo de otro helicóptero: el óptimo es 2."],
 "Ganancia esperada(k) = 100 000(1 − 0.1ᵏ) − 1 000k: k=1→89 000, k=2→97 000, k=3→96 900. El máximo es k = 2 helicópteros. Verificado con Python.",
 "La decisión óptima compara el beneficio marginal de cada helicóptero (reduce el riesgo de no hallar el tesoro) con su costo fijo. Se contrata mientras el beneficio extra supere los $1 000.",
 18, ["valor esperado", "beneficio marginal", "decisión óptima"],
 ["análisis costo-beneficio", "redundancia óptima", "inversión bajo riesgo"],
 "", ["probabilidad", "valor-esperado", "optimizacion", "nivel-avanzado"], "cap. 11 (Prob. 11.19)"))

A(P(477, "El par de calcetines garantizado", "optimizacion", 2,
 "Un cajón a oscuras contiene calcetines de 3 colores distintos, mezclados. ¿Cuántos calcetines debes sacar (sin mirar) para GARANTIZAR que tengas al menos un par del mismo color?",
 ["Piensa en el PEOR caso posible: ¿cuántos puedes sacar sin lograr todavía un par?",
  "En el peor caso sacas uno de cada color sin repetir: 3 calcetines de colores distintos, aún sin par.",
  "El siguiente calcetín, sea del color que sea, repite alguno de los tres.",
  "Por el principio del palomar, basta uno más que el número de colores.",
  "3 + 1 = 4 calcetines."],
 "En el peor caso sacas 3 de colores distintos (sin par); el 4.º forzosamente repite un color. Se necesitan 4. Verificado por el principio del palomar.",
 "El principio del palomar garantiza coincidencias: con más objetos (calcetines) que casilleros (colores), dos caen en el mismo. Se razona siempre sobre el peor caso.",
 10, ["principio del palomar", "peor caso", "garantía"],
 ["asignación de recursos", "garantías de colisión", "hashing"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 2 (Pigeonhole)"))

A(P(478, "Dos del mismo mes", "optimizacion", 2,
 "¿Cuántas personas debe haber en una sala para GARANTIZAR que al menos dos cumplan años en el mismo mes?",
 ["Hay 12 meses posibles; piensa en el peor caso para que no haya coincidencia.",
  "En el peor caso, las primeras personas nacen en meses todos distintos: hasta 12 personas, una por mes.",
  "Con 12 personas podría no haber dos del mismo mes (una por cada mes).",
  "La persona número 13 cae forzosamente en un mes ya ocupado.",
  "Se necesitan 12 + 1 = 13 personas."],
 "Con 12 personas podrían ocupar los 12 meses sin repetir; la 13.ª repite un mes. Hacen falta 13. Verificado por el principio del palomar.",
 "Para garantizar una coincidencia con n casilleros, basta n+1 objetos. Aquí 12 meses ⇒ 13 personas aseguran dos en el mismo mes.",
 8, ["principio del palomar", "casilleros y objetos", "garantía"],
 ["programación de calendarios", "garantías estadísticas", "colisiones"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 2 (Pigeonhole)"))

A(P(479, "El cumpleaños asegurado", "optimizacion", 2,
 "Suponiendo que un año tiene 366 fechas posibles de cumpleaños (incluido el 29 de febrero), ¿cuántas personas garantizan que al menos dos compartan la fecha exacta de cumpleaños?",
 ["Hay 366 fechas posibles; usa el peor caso del principio del palomar.",
  "Con 366 personas, en el peor caso cada una tiene una fecha distinta (una por día del año).",
  "La persona número 367 debe repetir alguna fecha.",
  "Así que el mínimo garantizado es 366 + 1.",
  "= 367 personas."],
 "Con 366 personas podrían ocupar las 366 fechas distintas; la 367.ª repite una. Se necesitan 367. Verificado por el principio del palomar.",
 "No confundir con el 'problema del cumpleaños' probabilístico (donde 23 personas ya dan 50%): aquí se pide GARANTÍA absoluta, que exige n+1 = 367.",
 8, ["principio del palomar", "garantía vs probabilidad", "fechas"],
 ["seguridad de identificadores", "colisiones de hash", "garantías"],
 "", ["palomar", "optimizacion", "nivel-basico"], "cap. 2 (Pigeonhole)"))

A(P(480, "Cuántas tiradas para un seis", "optimizacion", 3,
 "Se lanza repetidamente un dado equilibrado. ¿Cuál es el menor número de lanzamientos para que la probabilidad de obtener al menos un seis sea al menos 1/2?",
 ["Usa el complemento: P(ningún seis en n tiros) y exige que P(al menos un seis) ≥ 1/2.",
  "Cada tiro NO da seis con probabilidad 5/6; en n tiros, P(ningún seis) = (5/6)ⁿ.",
  "P(al menos un seis) = 1 − (5/6)ⁿ ≥ 1/2, o sea (5/6)ⁿ ≤ 1/2.",
  "Prueba: (5/6)³ ≈ 0.579 > 0.5; (5/6)⁴ ≈ 0.482 < 0.5.",
  "El menor n es 4."],
 "Se necesita (5/6)ⁿ ≤ 1/2. (5/6)³ ≈ 0.579 (no basta), (5/6)⁴ ≈ 0.482 (sí). El menor número de lanzamientos es 4. Verificado con Python.",
 "Otra vez el complemento convierte 'al menos un éxito' en 'ningún éxito', cuya probabilidad decae geométricamente. Se busca el menor entero que cruza el umbral.",
 12, ["probabilidad complementaria", "umbral 1/2", "menor n"],
 ["diseño de reintentos", "pruebas repetidas", "tiempo de espera"],
 "", ["probabilidad", "optimizacion", "nivel-intermedio"], "cap. 8 (al menos un éxito)"))

A(P(481, "Asegurar una suma de once", "optimizacion", 3,
 "De los enteros del 1 al 10, ¿cuántos hay que elegir (sin repetir) para GARANTIZAR que dos de los elegidos sumen 11?",
 ["Agrupa los números en parejas que sumen 11; esas parejas son los 'casilleros'.",
  "Las parejas que suman 11 son (1,10), (2,9), (3,8), (4,7), (5,6): 5 parejas que cubren los 10 números.",
  "En el peor caso eliges un número de cada pareja sin completar ninguna: hasta 5 números.",
  "El sexto número elegido cae forzosamente en una pareja ya iniciada, completando una suma 11.",
  "Se necesitan 5 + 1 = 6 números."],
 "Hay 5 parejas que suman 11. En el peor caso se eligen 5 (uno por pareja) sin sumar 11; el 6.º completa una pareja. Se necesitan 6. Verificado por el principio del palomar.",
 "La clave del palomar es elegir bien los casilleros: aquí las parejas que suman 11. Con 5 casilleros, 6 elecciones fuerzan dos en el mismo casillero.",
 14, ["principio del palomar", "parejas complementarias", "garantía"],
 ["teoría de Ramsey", "diseño de pruebas", "combinatoria"],
 "", ["palomar", "optimizacion", "nivel-intermedio"], "cap. 2 (Pigeonhole)"))

A(P(482, "Tres del mismo color", "optimizacion", 3,
 "Una bolsa contiene 5 canicas rojas, 5 azules y 5 verdes. ¿Cuántas canicas hay que sacar (sin mirar) para GARANTIZAR que haya 3 del mismo color?",
 ["Piensa en el peor caso: ¿cuántas puedes sacar teniendo a lo más 2 de cada color?",
  "En el peor caso sacas 2 rojas, 2 azules y 2 verdes: 6 canicas, sin llegar a 3 de un color.",
  "La séptima canica, sea del color que sea, hace que un color llegue a 3.",
  "Hay 3 colores y el umbral es 3 por color: 3·(3−1) + 1.",
  "= 6 + 1 = 7 canicas."],
 "En el peor caso se sacan 2 de cada color (6 canicas) sin tener 3 iguales; la 7.ª completa un trío. Se necesitan 7. Verificado por el principio del palomar.",
 "Versión generalizada del palomar: para garantizar k del mismo tipo con c tipos, hacen falta c·(k−1)+1. Aquí 3·2+1 = 7.",
 12, ["principio del palomar generalizado", "peor caso", "garantía"],
 ["control de inventarios", "garantías de muestreo", "tolerancia a fallos"],
 "", ["palomar", "optimizacion", "nivel-intermedio"], "cap. 2 (Pigeonhole)"))

A(P(483, "La combinación más grande de la fila", "optimizacion", 2,
 "Entre C(10,0), C(10,1), …, C(10,10), ¿cuál es la mayor y cuánto vale?",
 ["Los coeficientes de una fila de Pascal crecen hacia el centro y luego decrecen: el máximo está en el medio.",
  "La fila 10 tiene 11 términos (k de 0 a 10); el central corresponde a k = 5.",
  "El máximo es C(10, 5).",
  "C(10,5) = 10!/(5!·5!).",
  "= 252."],
 "Los coeficientes binomiales de una fila son máximos en el centro: C(10,5) = 252 es el mayor. Verificado con Python.",
 "La 'unimodalidad' de cada fila de Pascal (sube al centro, baja después) garantiza que el coeficiente central C(n, n/2) es el máximo. Maximizar = ir al medio.",
 10, ["coeficientes binomiales", "unimodalidad", "máximo central"],
 ["distribución binomial", "moda estadística", "optimización discreta"],
 "", ["combinaciones", "pascal", "optimizacion", "nivel-basico"], "cap. 12 (Pascal's Triangle)"))

A(P(484, "Apretones de manos suficientes", "optimizacion", 3,
 "En una reunión, cada par de personas se da la mano exactamente una vez. ¿Cuál es el menor número de personas para que el número total de apretones de manos sea al menos 100?",
 ["El número de apretones entre n personas es C(n,2) = n(n−1)/2. Busca el menor n con C(n,2) ≥ 100.",
  "Plantea n(n−1)/2 ≥ 100, es decir n(n−1) ≥ 200.",
  "Prueba: 14·13 = 182 < 200; 15·14 = 210 ≥ 200.",
  "Con n = 14 hay C(14,2) = 91 apretones (insuficiente); con n = 15 hay C(15,2) = 105.",
  "El menor n es 15."],
 "C(n,2) ≥ 100 ⇔ n(n−1) ≥ 200. Con n = 14 da 91 (insuficiente) y n = 15 da 105. El menor n es 15. Verificado con Python.",
 "Cuando una cantidad crece con C(n,2), encontrar el menor n que supera un umbral es resolver una desigualdad cuadrática y tomar el siguiente entero.",
 12, ["combinaciones C(n,2)", "desigualdad cuadrática", "menor n"],
 ["redes de conexiones", "dimensionar sistemas", "grafos completos"],
 "", ["combinaciones", "optimizacion", "nivel-intermedio"], "cap. 4 / 1 (apretones de manos)"))

A(P(485, "Dos con la misma suma de dígitos", "optimizacion", 3,
 "¿Cuántos números de tres cifras hace falta elegir para GARANTIZAR que dos de ellos tengan la misma suma de dígitos?",
 ["Los 'casilleros' son los posibles valores de la suma de dígitos de un número de tres cifras.",
  "El menor número de tres cifras es 100 (suma 1) y el mayor es 999 (suma 27).",
  "Así que la suma de dígitos toma valores de 1 a 27: 27 casilleros posibles.",
  "En el peor caso eliges 27 números con sumas todas distintas.",
  "El número 28 forzosamente repite una suma: se necesitan 27 + 1 = 28."],
 "La suma de dígitos de un número de tres cifras va de 1 (100) a 27 (999): 27 valores. Por el palomar, 28 números garantizan dos con la misma suma. Verificado con el conteo de casilleros.",
 "Lo difícil del palomar suele ser CONTAR los casilleros correctamente: aquí, los 27 valores posibles de la suma de dígitos. Con 27 casilleros, 28 objetos fuerzan una coincidencia.",
 14, ["principio del palomar", "suma de dígitos", "contar casilleros"],
 ["funciones hash", "clasificación", "garantías de colisión"],
 "", ["palomar", "optimizacion", "nivel-intermedio"], "cap. 2 (Pigeonhole)"))

# =====================================================================
# INVERSION (11) — reconstruir n desde conteo/probabilidad; complementario
# =====================================================================

A(P(486, "Cuántas personas dan 21 apretones", "inversion", 2,
 "En un grupo, cada par de personas se da la mano exactamente una vez, y hay 21 apretones de manos en total. ¿Cuántas personas hay?",
 ["El número de apretones es C(n,2) = n(n−1)/2. Trabaja hacia atrás desde 21.",
  "Plantea n(n−1)/2 = 21, es decir n(n−1) = 42.",
  "Busca dos enteros consecutivos cuyo producto sea 42.",
  "6·7 = 42, así que n = 7.",
  "Comprueba: C(7,2) = 21. Hay 7 personas."],
 "C(n,2) = 21 ⇒ n(n−1) = 42 = 6·7 ⇒ n = 7. Verificado con Python.",
 "Desde un conteo de pares se recupera el tamaño del grupo resolviendo n(n−1) = 2·(conteo). Reconocer el producto de consecutivos evita la fórmula cuadrática.",
 10, ["combinaciones C(n,2)", "producto de consecutivos", "reconstruir n"],
 ["dimensionar redes", "ingeniería inversa", "grafos"],
 "", ["combinaciones", "inversion", "nivel-basico"], "cap. 1 / 4 (apretones, inversa)"))

A(P(487, "Veintiocho partidos", "inversion", 2,
 "En un torneo de todos contra todos, cada par de equipos juega exactamente una vez, y se disputan 28 partidos en total. ¿Cuántos equipos participan?",
 ["El número de partidos es C(n,2) = n(n−1)/2. Despeja n desde 28.",
  "n(n−1)/2 = 28 ⇒ n(n−1) = 56.",
  "Dos consecutivos con producto 56: 7·8 = 56.",
  "n = 8.",
  "Comprueba: C(8,2) = 28. Hay 8 equipos."],
 "C(n,2) = 28 ⇒ n(n−1) = 56 = 7·8 ⇒ n = 8. Verificado con Python.",
 "El mismo método inverso: el conteo de enfrentamientos fija n vía n(n−1) = 2·(partidos). Buscar consecutivos con ese producto da la respuesta directa.",
 10, ["combinaciones C(n,2)", "torneo round-robin", "reconstruir n"],
 ["calendarios deportivos", "diseño de torneos", "redes"],
 "", ["combinaciones", "inversion", "nivel-basico"], "cap. 1 / 4 (round-robin, inversa)"))

A(P(488, "Treinta y dos subconjuntos", "inversion", 2,
 "Un conjunto tiene exactamente 32 subconjuntos (contando el vacío y el total). ¿Cuántos elementos tiene?",
 ["El número de subconjuntos de un conjunto de n elementos es 2ⁿ. Trabaja hacia atrás desde 32.",
  "2ⁿ = 32.",
  "Expresa 32 como potencia de 2: 32 = 2⁵.",
  "Por tanto n = 5.",
  "El conjunto tiene 5 elementos."],
 "2ⁿ = 32 = 2⁵ ⇒ n = 5. Verificado con Python.",
 "Cada elemento duplica el número de subconjuntos (entra o no), así que el total es 2ⁿ. Recuperar n es tomar el logaritmo base 2 del conteo.",
 8, ["subconjuntos 2ⁿ", "logaritmo base 2", "reconstruir n"],
 ["espacios de estados", "lógica booleana", "complejidad combinatoria"],
 "", ["conteo", "inversion", "nivel-basico"], "cap. 2 / 12 (subconjuntos, inversa)"))

A(P(489, "Cuántos lanzamientos para 15/16", "inversion", 3,
 "Se lanza una moneda equilibrada n veces. La probabilidad de obtener al menos una cara resulta ser 15/16. ¿Cuánto vale n?",
 ["Usa el complemento: P(ninguna cara) = 1 − 15/16 = 1/16.",
  "P(ninguna cara en n lanzamientos) = (1/2)ⁿ.",
  "Iguala: (1/2)ⁿ = 1/16.",
  "Como 1/16 = (1/2)⁴, se tiene n = 4.",
  "Hay 4 lanzamientos."],
 "P(ninguna cara) = 1 − 15/16 = 1/16 = (1/2)⁴ ⇒ n = 4. Verificado con Python.",
 "Desde una probabilidad de 'al menos uno' se recupera el número de intentos pasando al complemento y resolviendo (1/2)ⁿ = valor. Es inversión apoyada en P(A)+P(no A)=1.",
 12, ["probabilidad complementaria", "ecuación exponencial", "reconstruir n"],
 ["fiabilidad de sistemas", "diseño de pruebas", "tiempo de espera"],
 "", ["probabilidad", "inversion", "nivel-intermedio"], "cap. 8 (complemento, inversa)"))

A(P(490, "Ajustar el valor esperado a 2", "inversion", 3,
 "Una bolsa tiene 8 papeles: seis con un 1 y dos con un 3. ¿Cuántos papeles adicionales con un 3 hay que agregar para que el valor esperado del número que se saca al azar sea exactamente 2?",
 ["Escribe el valor esperado tras añadir k treses y resuelve para k.",
  "Tras añadir k treses hay 6 unos y (2+k) treses, total 8+k papeles. La suma de valores es 6·1 + (2+k)·3.",
  "Valor esperado = (6 + 3(2+k)) / (8+k) = 2.",
  "6 + 6 + 3k = 2(8+k) ⇒ 12 + 3k = 16 + 2k ⇒ k = 4.",
  "Hay que agregar 4 papeles con un 3."],
 "Con k treses añadidos: (6 + 3(2+k))/(8+k) = 2 ⇒ 12 + 3k = 16 + 2k ⇒ k = 4. Verificado con Python.",
 "Se invierte la fórmula del valor esperado: se fija el resultado deseado y se despeja la cantidad a añadir. Cada nuevo 3 sube el promedio hacia 3.",
 14, ["valor esperado", "despejar la incógnita", "promedio ponderado"],
 ["calibración de modelos", "ajuste de muestras", "diseño de loterías"],
 "", ["probabilidad", "valor-esperado", "inversion", "nivel-intermedio"], "cap. 11 (Prob. 11.14d)"))

A(P(491, "Subir el valor esperado a 2.5", "inversion", 4,
 "Una bolsa tiene 8 papeles: seis con un 1 y dos con un 3. ¿Cuántos papeles adicionales con un 3 hay que agregar para que el valor esperado sea al menos 2.5?",
 ["Plantea la desigualdad del valor esperado tras añadir k treses.",
  "(6 + 3(2+k)) / (8+k) ≥ 2.5, es decir (12 + 3k)/(8+k) ≥ 5/2.",
  "Multiplica en cruz (8+k > 0): 2(12 + 3k) ≥ 5(8+k).",
  "24 + 6k ≥ 40 + 5k ⇒ k ≥ 16.",
  "Hay que agregar al menos 16 papeles con un 3."],
 "(12 + 3k)/(8+k) ≥ 5/2 ⇒ 24 + 6k ≥ 40 + 5k ⇒ k ≥ 16. El mínimo es 16 papeles. Verificado con Python.",
 "Mismo proceso inverso pero con desigualdad: se despeja el menor k que alcanza el valor esperado pedido. El promedio se acerca a 3 cada vez más lento, por eso hace falta tanto.",
 16, ["valor esperado", "desigualdad", "despejar mínimo"],
 ["calibración estadística", "rebalanceo de carteras", "ajuste de muestras"],
 "", ["probabilidad", "valor-esperado", "inversion", "nivel-avanzado"], "cap. 11 (Prob. 11.14e)"))

A(P(492, "Al menos un siete", "inversion", 3,
 "¿Cuántos números de tres cifras tienen al menos un dígito igual a 7?",
 ["'Al menos un 7' se cuenta mejor por el complemento: los de tres cifras SIN ningún 7.",
  "Total de números de tres cifras: del 100 al 999, son 900.",
  "Sin ningún 7: el dígito de las centenas tiene 8 opciones (1-9 sin el 7), y los de decenas y unidades 9 cada uno (0-9 sin el 7).",
  "Sin ningún 7 = 8·9·9 = 648.",
  "Con al menos un 7 = 900 − 648 = 252."],
 "Total = 900. Sin ningún 7 = 8·9·9 = 648. Con al menos un 7 = 900 − 648 = 252. Verificado con Python.",
 "El conteo complementario es 'pensar hacia atrás': cuentas lo que NO quieres (sin sietes) y lo restas del total. Las restricciones de 'al menos uno' casi siempre se invierten así.",
 12, ["conteo complementario", "restricción por dígito", "trabajar hacia atrás"],
 ["validación de datos", "conteo por exclusión", "filtros"],
 "", ["conteo", "complementario", "inversion", "nivel-intermedio"], "cap. 2 (complementario)"))

A(P(493, "Dos que no se sienten juntos", "inversion", 3,
 "¿De cuántas maneras pueden sentarse 5 personas en una fila de 5 asientos de modo que dos personas específicas NO queden una al lado de la otra?",
 ["Cuenta el total y resta los arreglos donde sí están juntas (pensar hacia atrás).",
  "Total de arreglos de 5 personas en fila: 5! = 120.",
  "Cuenta los arreglos donde las dos específicas SÍ están juntas: trátalas como un bloque (2 ordenamientos internos) junto con las otras 3, o sea 2·4!.",
  "Juntas = 2·4! = 2·24 = 48.",
  "No juntas = 120 − 48 = 72."],
 "Total = 5! = 120. Juntas (bloque de 2) = 2·4! = 48. No juntas = 120 − 48 = 72. Verificado con Python.",
 "La condición 'no adyacentes' se cuenta restando del total los casos 'adyacentes', que se cuentan fácil agrupando a los dos en un bloque. Es conteo complementario sobre arreglos.",
 12, ["conteo complementario", "técnica del bloque", "permutaciones"],
 ["asignación de asientos", "restricciones de adyacencia", "planificación"],
 "", ["conteo", "complementario", "inversion", "nivel-intermedio"], "cap. 2 (restricciones)"))

A(P(494, "La moneda sesgada", "inversion", 3,
 "Una moneda cargada cae en cara con probabilidad p. Se lanza dos veces y la probabilidad de obtener dos caras resulta ser 9/25. ¿Cuánto vale p?",
 ["La probabilidad de dos caras en lanzamientos independientes es p². Trabaja hacia atrás.",
  "p² = 9/25.",
  "Toma raíz cuadrada (p es una probabilidad, así que p > 0).",
  "p = 3/5.",
  "Comprueba: (3/5)² = 9/25. La moneda cae cara con probabilidad 3/5."],
 "p² = 9/25 ⇒ p = 3/5 (raíz positiva). Verificado con Python.",
 "Desde la probabilidad de un evento compuesto (dos caras) se recupera la probabilidad de un solo evento tomando la raíz. La independencia permite escribir p².",
 12, ["eventos independientes", "raíz cuadrada", "reconstruir probabilidad"],
 ["estimación de parámetros", "calibración de modelos", "inferencia"],
 "", ["probabilidad", "inversion", "nivel-intermedio"], "cap. 8 (producto, inversa)"))

A(P(495, "Setecientos veinte ordenamientos", "inversion", 2,
 "Un conjunto de objetos distintos se puede ordenar en fila de exactamente 720 maneras diferentes. ¿Cuántos objetos hay?",
 ["El número de ordenamientos de n objetos distintos es n!. Trabaja hacia atrás desde 720.",
  "n! = 720.",
  "Calcula factoriales: 5! = 120, 6! = 720.",
  "Entonces n = 6.",
  "Hay 6 objetos."],
 "n! = 720 = 6! ⇒ n = 6. Verificado con Python.",
 "Recuperar n desde n! es buscar en la tabla de factoriales: crecen tan rápido que el match es único. Aquí 6! = 720.",
 8, ["factorial", "permutaciones", "reconstruir n"],
 ["dimensionar arreglos", "complejidad de permutaciones", "criptografía"],
 "", ["conteo", "inversion", "nivel-basico"], "cap. 1 (permutaciones, inversa)"))

A(P(496, "Cuando elegir dos es como elegir tres", "inversion", 3,
 "Para cierto entero n, el número de subconjuntos de 2 elementos de un conjunto de n elementos es igual al número de subconjuntos de 3 elementos. ¿Cuánto vale n?",
 ["Plantea la igualdad C(n,2) = C(n,3) y usa la simetría de las combinaciones.",
  "Por la identidad C(n,r) = C(n,n−r), C(n,2) = C(n,3) ocurre cuando 2 y 3 son 'complementarios': 2 + 3 = n.",
  "Eso da n = 5.",
  "Comprueba: C(5,2) = 10 y C(5,3) = 10. Coinciden.",
  "El valor es n = 5."],
 "C(n,2) = C(n,3) se cumple cuando 2 + 3 = n (por la simetría C(n,r)=C(n,n−r)), es decir n = 5; en efecto C(5,2) = C(5,3) = 10. Verificado con Python.",
 "La simetría de las combinaciones invierte la ecuación: C(n,a) = C(n,b) (con a ≠ b) obliga a a + b = n. Reconocer ese patrón evita resolver una ecuación polinómica.",
 12, ["identidad C(n,r)=C(n,n−r)", "simetría", "reconstruir n"],
 ["combinatoria", "resolución de ecuaciones", "teoría de números"],
 "", ["combinaciones", "inversion", "nivel-intermedio"], "cap. 4 (simetría, inversa)"))

# =====================================================================
# Validación de balance y append idempotente
# =====================================================================
assert len(PROBLEMS) == 44, len(PROBLEMS)
bal = collections.Counter(p["estrategia"] for p in PROBLEMS)
assert bal["inversion"] == bal["optimizacion"] == bal["invariantes"] == bal["patrones"] == 11, bal
ids = [p["id"] for p in PROBLEMS]
assert ids == list(range(453, 497)), ids
assert len(set(ids)) == 44

PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
clash = existing & set(ids)
assert not clash, ("choque de ids", clash)

data["problemas"].extend(PROBLEMS)
gbal = collections.Counter(p["estrategia"] for p in data["problemas"])
print("balance global tras append:", dict(gbal))
assert all(v == 124 for v in gbal.values()), gbal

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: añadidos {len(PROBLEMS)} problemas (ids {ids[0]}-{ids[-1]}). Total = {len(data['problemas'])}.")
