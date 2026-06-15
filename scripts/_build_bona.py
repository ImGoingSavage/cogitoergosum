# -*- coding: utf-8 -*-
"""Tanda 31 — Miklós Bóna, *A Walk Through Combinatorics* (cap. 1 Pigeon-Hole,
cap. 2 Induction, cap. 9 Graph Theory). Append 44 problemas verificados a
data/problems.json. Todas las afirmaciones numéricas verificadas con Python
(ver /tmp/verify_bona*.py y la bitácora de HANDOFFCES.md). Builder idempotente:
aborta si hay choque de ids. Sector C (entrenamiento), esquema §4.1, ids 233-276,
balanceado 11/11/11/11."""
import json, collections

SRC = "Bóna, *A Walk Through Combinatorics* (2.ª ed., World Scientific, 2006)"

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
# INVARIANTES (11) — casillero (cap. 1) y paridad en grafos (cap. 9)
# =====================================================================

A(P(233, "La fiesta de los Smith", "invariantes", 4,
 "El Sr. y la Sra. Smith invitan a cuatro parejas a su casa (diez personas en total). Cuando llegan, las personas que ya se conocían se dan la mano. Después, el Sr. Smith pregunta a cada una de las otras nueve personas a cuántas dio la mano, y resulta que las nueve respuestas son TODAS distintas. Nadie se da la mano consigo mismo ni con su cónyuge. ¿A cuántas personas dio la mano la Sra. Smith?",
 ["Modela la fiesta como un grafo: cada persona es un vértice y cada apretón una arista. ¿Qué rango de grados son posibles?",
  "Las nueve respuestas son distintas y cada persona da la mano a lo más a 8 (no a sí misma ni a su cónyuge). Nueve valores distintos en {0,1,…,8}: ¡cada número aparece exactamente una vez!",
  "Considera a la persona con 8 apretones: dio la mano a todos menos a su cónyuge, así que su cónyuge es quien dio 0. Empareja extremos: 8↔0.",
  "Quita esa pareja (8 y 0). Entre los demás, el que daba 7 (ahora dio la mano a todos los que quedan salvo su cónyuge) se empareja con el que daba 1. Repite: 7↔1, 6↔2, 5↔3.",
  "Quedan emparejados (8,0),(7,1),(6,2),(5,3). El único sin pareja entre los nueve es el del 4 — y por eliminación, ese es la Sra. Smith. Dio la mano a 4 personas."],
 "La Sra. Smith dio la mano a 4 personas. Las nueve respuestas distintas, todas en {0,…,8}, son exactamente 0,1,…,8 una vez cada una. La persona con 8 apretones dio la mano a todos salvo a su cónyuge, que forzosamente es la de 0; quitándolos, la de 7 se empareja con la de 1, la de 6 con la de 2, la de 5 con la de 3. El único valor sin pareja es 4, que corresponde a la Sra. Smith (el Sr. Smith no fue interrogado).",
 "Casillero (nueve valores distintos llenan {0,…,8}) más un emparejamiento por simetría cónyuge↔complemento. El cónyuge de quien da k apretones siempre da 2n−k. Verificado con Python: con n parejas la anfitriona siempre da n apretones (aquí n=4).",
 26, ["principio del casillero", "modelado con grafos", "emparejamiento por complemento"],
 ["grafos de relaciones", "secuencias de grados", "problemas de apretones de manos"],
 "", ["casillero", "grafos", "apretones", "nivel-avanzado"], "cap. 1 (Ej. 1.7)"))

A(P(234, "Mil quinientos despegues", "invariantes", 1,
 "Un aeropuerto concurrido tiene 1500 despegues por día. Demuestra que hay dos aviones que deben despegar con menos de un minuto de diferencia.",
 ["Un día tiene una cantidad fija de minutos. ¿Cuántos? Esos serán los 'nidos'.",
  "Un día tiene 24·60 = 1440 minutos. Los 1500 despegues son las 'palomas' y los 1440 minutos los 'nidos'.",
  "Como 1500 > 1440, por el principio del casillero dos despegues caen en el mismo minuto.",
  "Dos despegues en el mismo minuto distan menos de un minuto entre sí.",
  "Por tanto hay dos aviones que despegan con menos de un minuto de diferencia."],
 "Hay dos despegues con menos de un minuto de diferencia. Un día tiene 1440 minutos; con 1500 despegues y solo 1440 minutos, el principio del casillero garantiza que dos despegues ocurren en el mismo minuto, y por tanto distan menos de un minuto.",
 "Aplicación directa del casillero: más objetos (despegues) que cajas (minutos del día) fuerza una coincidencia. La sutileza es identificar bien las cajas. Verificado con Python: 1500 > 1440.",
 8, ["principio del casillero", "conteo de minutos", "palomas vs nidos"],
 ["planificación de horarios", "colisiones por intervalos", "argumentos de conteo"],
 "", ["casillero", "tiempo", "nivel-basico"], "cap. 1 (Ej. 1)"))

A(P(235, "Cien puntos en un cubo", "invariantes", 3,
 "Se dan cien puntos dentro de un cubo de lado 1. Demuestra que cuatro de ellos forman un tetraedro de volumen a lo más 1/99.",
 ["Divide el cubo en losas (prismas) y mete los cien puntos. ¿Cuántas losas conviene usar?",
  "Corta el cubo con planos paralelos a la base en 33 losas iguales, cada una de altura 1/33 y volumen 1/33.",
  "Como 100 = 3·33 + 1, por el principio del casillero alguna losa contiene al menos cuatro puntos.",
  "Cuatro puntos dentro de una losa forman un tetraedro contenido en ella. ¿Cuál es el volumen máximo de un tetraedro dentro de un prisma?",
  "Un tetraedro dentro de un prisma tiene volumen a lo más un tercio del prisma, es decir ≤ (1/3)·(1/33) = 1/99."],
 "Corta el cubo en 33 losas de volumen 1/33 cada una. Como 100 = 3·33 + 1, por el casillero alguna losa contiene cuatro puntos. Un tetraedro inscrito en un prisma tiene volumen a lo más un tercio del prisma, así que esos cuatro puntos forman un tetraedro de volumen ≤ (1/3)·(1/33) = 1/99.",
 "Casillero geométrico (losas) + la cota 'tetraedro ≤ un tercio del prisma'. Verificado con Python: 100 > 3·33 y (1/33)/3 = 1/99 exacto.",
 20, ["principio del casillero", "tetraedro en un prisma", "subdivisión en losas"],
 ["geometría combinatoria en 3D", "cotas de volumen", "empaquetamiento de puntos"],
 "", ["casillero", "geometria", "volumen", "nivel-medio"], "cap. 1 (Ej. 3)"))

A(P(236, "Nueve enteros con factores pequeños", "invariantes", 3,
 "El conjunto M consta de nueve enteros positivos, ninguno con un divisor primo mayor que 6. Demuestra que M tiene dos elementos cuyo producto es el cuadrado de un entero.",
 ["Como ningún elemento tiene factor primo >6, cada uno es de la forma 2^i·3^j·5^k. ¿Qué información captura la PARIDAD de i, j, k?",
  "Asocia a cada número el vector (i mód 2, j mód 2, k mód 2). Dos números con el mismo vector tienen producto con todos los exponentes pares… es decir, un cuadrado.",
  "¿Cuántos vectores de paridad distintos hay? Cada coordenada es 0 o 1, así que hay 2³ = 8 clases.",
  "Tienes 9 números y 8 clases de paridad. Por el principio del casillero, dos números comparten clase.",
  "Esos dos números x, y cumplen que xy = 2^{2a}3^{2b}5^{2c} = (2^a 3^b 5^c)², un cuadrado perfecto."],
 "Cada elemento se escribe 2^i·3^j·5^k. Asociándole el vector de paridades (i mód 2, j mód 2, k mód 2), hay solo 2³ = 8 clases posibles. Con 9 elementos, el principio del casillero da dos, x e y, en la misma clase; entonces los exponentes de xy son todos pares, así que xy = (2^a 3^b 5^c)² es un cuadrado perfecto.",
 "Casillero sobre vectores de paridad de exponentes en (ℤ/2)³: misma clase ⇒ producto cuadrado. Verificado con Python: 9 > 2³ = 8.",
 20, ["principio del casillero", "vectores de paridad de exponentes", "cuadrados perfectos"],
 ["espacios sobre GF(2)", "factorización y exponentes", "argumentos de paridad"],
 "", ["casillero", "paridad", "cuadrados", "nivel-medio"], "cap. 1 (Ej. 6a)"))

A(P(237, "Quinientos dos enteros y el mil", "invariantes", 4,
 "Demuestra que entre cualesquiera 502 enteros positivos hay dos cuya suma o cuya diferencia es divisible por 1000.",
 ["Trabaja módulo 1000. A cada entero asígnale su resto, pero agrúpalo junto con su 'opuesto' módulo 1000.",
  "Para un resto r, considera la pareja {r, 1000−r}: dos números cuyos restos están en la misma pareja tienen suma o diferencia divisible por 1000.",
  "Los restos 0 y 500 son especiales (cada uno es su propio opuesto). Cuenta cuántas 'cajas' resultan al agrupar 0..999 en parejas {r,1000−r}.",
  "Hay 499 parejas {r,1000−r} (para r=1..499), más las cajas individuales {0} y {500}: en total 501 cajas. Tienes 502 números.",
  "Con 502 números y 501 cajas, el casillero da dos en la misma caja: su suma o diferencia es divisible por 1000."],
 "Agrupa los restos módulo 1000 en cajas: {0}, {500}, y las 499 parejas {r, 1000−r} para r = 1,…,499, en total 501 cajas. Dos enteros cuyos restos caen en la misma caja tienen suma o diferencia divisible por 1000 (si están en {0} o {500}, su diferencia lo es; si están en una pareja {r,1000−r}, su suma o su diferencia lo es). Con 502 enteros y 501 cajas, el principio del casillero garantiza dos en la misma caja.",
 "Casillero sobre clases de 'resto y su opuesto' módulo 1000: la cuenta correcta de cajas (501) hace que 502 fuerce la colisión. Verificado con Python: 502 > 501 = 499 + 2.",
 24, ["principio del casillero", "restos y opuestos módulo m", "emparejamiento de clases"],
 ["aritmética modular", "sumas y diferencias divisibles", "teoría combinatoria de números"],
 "", ["casillero", "modular", "suma-diferencia", "nivel-avanzado"], "cap. 1 (Ej. 10)"))

A(P(238, "Diecisiete puntos en un triángulo", "invariantes", 2,
 "Se dan 17 puntos dentro de un triángulo equilátero de lado 1. Demuestra que dos de ellos están a una distancia de a lo más 1/4 uno del otro.",
 ["Divide el triángulo en triángulos pequeños iguales y mete los 17 puntos. ¿En cuántos conviene dividir?",
  "Divide cada lado en cuatro partes iguales y traza paralelas: el triángulo se parte en 4² = 16 triangulitos equiláteros de lado 1/4.",
  "Tienes 17 puntos y 16 triangulitos. Por el principio del casillero, algún triangulito contiene dos puntos.",
  "¿Cuál es la máxima distancia entre dos puntos dentro de un triángulo equilátero de lado 1/4?",
  "El diámetro de un triángulo equilátero es su lado, así que dos puntos en el mismo triangulito distan ≤ 1/4."],
 "Divide el triángulo equilátero de lado 1 en 16 triangulitos equiláteros de lado 1/4 (partiendo cada lado en cuatro). Con 17 puntos y 16 triangulitos, el principio del casillero da dos puntos en el mismo triangulito, y como el diámetro de un triángulo equilátero es su lado, esos dos puntos distan ≤ 1/4.",
 "Casillero geométrico: subdividir en celdas de diámetro acotado (1/4) y meter más puntos que celdas. Verificado con Python: 17 > 16 = 4².",
 14, ["principio del casillero", "diámetro de un triángulo equilátero", "subdivisión triangular"],
 ["empaquetamiento de puntos", "geometría combinatoria", "argumentos de distancia mínima"],
 "", ["casillero", "geometria", "triangulo", "nivel-basico"], "cap. 1 (Ej. 20)"))

A(P(239, "Uno divide a otro", "invariantes", 3,
 "Se eligen n + 1 enteros distintos del conjunto {1, 2, …, 2n}. Demuestra que siempre habrá dos entre los elegidos tales que uno divide al otro.",
 ["A cada entero asígnale algo que lo agrupe con sus múltiplos/divisores por potencias de 2. Piensa en su 'parte impar'.",
  "Todo entero m se escribe de forma única como m = 2^a · q con q IMPAR. Llama a q la parte impar de m.",
  "¿Cuántas partes impares distintas hay en {1,…,2n}? Las impares son 1,3,5,…,2n−1: exactamente n valores.",
  "Tienes n+1 números y solo n partes impares posibles. Por el casillero, dos elegidos comparten la misma parte impar q.",
  "Si m₁ = 2^a·q y m₂ = 2^b·q con a < b, entonces m₁ divide a m₂. Listo."],
 "Escribe cada entero como m = 2^a·q con q impar (su 'parte impar'). En {1,…,2n} solo hay n partes impares posibles (1,3,…,2n−1). Con n+1 enteros elegidos, el principio del casillero da dos con la misma parte impar q: digamos 2^a·q y 2^b·q con a < b. Entonces el primero divide al segundo.",
 "Casillero sobre la 'parte impar': dos números con igual parte impar forman una cadena por divisibilidad (potencias de 2). Verificado con Python: para n = 2..6, todo subconjunto de tamaño n+1 de {1,…,2n} contiene un par donde uno divide al otro. (Nota: la variante 'uno es el DOBLE del otro' es FALSA — p. ej. {1,3,4,5,7} para n=4.)",
 18, ["principio del casillero", "parte impar de un entero", "cadenas de divisibilidad"],
 ["estructura multiplicativa de los enteros", "antiCadenas y cadenas", "teoría de Dilworth"],
 "", ["casillero", "divisibilidad", "parte-impar", "nivel-medio"], "cap. 1 (Ej. 25b)"))

A(P(240, "Hermanos y el lema del apretón de manos", "invariantes", 2,
 "Demuestra que el número de personas vivas en el planeta que tienen un número IMPAR de hermanos es par.",
 ["Modela esto con un grafo: las personas son vértices y unes a dos si son hermanos. ¿Qué representa el 'grado' de un vértice?",
  "El grado de una persona (número de aristas que tocan su vértice) es su número de hermanos. Buscas cuántos vértices tienen grado impar.",
  "Recuerda el lema del apretón de manos: la suma de TODOS los grados de un grafo es par (igual a dos veces el número de aristas).",
  "Si la suma de todos los grados es par, ¿cuántos sumandos impares puede haber? Una suma de números es par solo si hay un número PAR de sumandos impares.",
  "Por tanto el número de vértices (personas) de grado impar (número impar de hermanos) es par."],
 "Construye el grafo donde las personas son vértices y dos se unen si son hermanos; el grado de cada persona es su número de hermanos. Por el lema del apretón de manos, la suma de todos los grados es par (es 2·#aristas). Una suma de enteros es par solo si la cantidad de sumandos impares es par; luego el número de personas con grado impar — es decir, con un número impar de hermanos — es par.",
 "Lema del apretón de manos: Σ grados = 2·#aristas es par, así que la cantidad de vértices de grado impar es par. Verificado con Python: en 2000 grafos aleatorios, el número de vértices de grado impar siempre es par.",
 12, ["lema del apretón de manos", "paridad de la suma de grados", "modelado con grafos"],
 ["teoría de grafos", "argumentos de paridad", "conservación combinatoria"],
 "", ["grafos", "apreton-manos", "paridad", "nivel-basico"], "cap. 9 (Ej. 10/27)"))

A(P(241, "Dos con el mismo grado", "invariantes", 2,
 "Demuestra que en todo grafo simple con al menos dos vértices hay dos vértices que tienen el mismo grado (el mismo número de vecinos).",
 ["En un grafo simple con n vértices, ¿qué valores puede tomar el grado de un vértice? Acota el rango.",
  "Cada grado está entre 0 y n−1 (un vértice puede no tener vecinos o estar unido a todos los demás). Eso da n valores posibles para n vértices: aún no hay colisión forzada…",
  "Observa que los grados 0 y n−1 NO pueden coexistir: si alguien tiene grado n−1 (unido a todos), nadie puede tener grado 0.",
  "Entonces los grados reales caben en {0,…,n−2} o en {1,…,n−1}: en ambos casos solo n−1 valores posibles para n vértices.",
  "Con n vértices y solo n−1 grados posibles, el principio del casillero da dos vértices con el mismo grado."],
 "En un grafo simple con n vértices cada grado está en {0,…,n−1}. Pero los valores 0 y n−1 son incompatibles (si un vértice se une a todos, ninguno queda aislado), así que los grados reales caben en un conjunto de solo n−1 valores. Con n vértices y n−1 grados posibles, el principio del casillero garantiza dos vértices con el mismo grado.",
 "Casillero con una observación fina: el rango de grados se reduce a n−1 valores porque 0 y n−1 no coexisten. Verificado con Python: en 2000 grafos aleatorios nunca todos los grados son distintos.",
 12, ["principio del casillero", "secuencia de grados", "rango de grados restringido"],
 ["teoría de grafos", "argumentos de existencia", "secuencias de grados"],
 "", ["grafos", "casillero", "grados", "nivel-basico"], "cap. 9 (Ej. 25)"))

A(P(242, "Apretones impares", "invariantes", 2,
 "En cualquier reunión, demuestra que el número de personas que han dado la mano un número impar de veces (a lo largo de la reunión) es par.",
 ["Modela los apretones como aristas de un grafo sobre las personas. ¿Qué cuenta el grado de cada vértice?",
  "El grado de una persona es el número de apretones que ha dado. Buscas cuántas personas tienen grado impar.",
  "Usa el lema del apretón de manos (que toma su nombre justo de este problema): la suma de todos los grados es 2·#aristas, un número par.",
  "Una suma de enteros es par solo si el número de sumandos impares es par.",
  "Por tanto la cantidad de personas con grado impar (número impar de apretones) es par."],
 "Modela los apretones como un grafo: personas = vértices, apretones = aristas; el grado de cada persona es cuántas manos estrechó. Por el lema del apretón de manos, Σ grados = 2·#aristas es par. Como una suma es par solo si la cantidad de sumandos impares es par, el número de personas que dieron la mano un número impar de veces es par.",
 "El lema homónimo: la paridad de la suma de grados obliga a que los vértices de grado impar sean un número par. Verificado con Python: en 2000 grafos aleatorios el conteo de grados impares siempre es par.",
 10, ["lema del apretón de manos", "paridad", "modelado con grafos"],
 ["teoría de grafos", "conteo doble", "argumentos de paridad"],
 "", ["grafos", "apreton-manos", "paridad", "nivel-basico"], "cap. 9 (Ej. 27)"))

A(P(243, "Una potencia de 44 menos uno", "invariantes", 2,
 "Demuestra que existe un entero positivo n tal que 44ⁿ − 1 es divisible por 7.",
 ["Trabaja módulo 7. Primero reduce la base: ¿a qué es congruente 44 módulo 7?",
  "44 = 6·7 + 2, así que 44 ≡ 2 (mód 7). Buscas n con 2ⁿ ≡ 1 (mód 7).",
  "Calcula las potencias de 2 módulo 7: 2, 4, 1, 2, 4, 1, … ¿Cuándo vale 1?",
  "2³ = 8 ≡ 1 (mód 7). Así que con n = 3 se tiene 44³ ≡ 2³ ≡ 1 (mód 7).",
  "Por tanto 44³ − 1 ≡ 0 (mód 7), es decir, 7 divide a 44³ − 1 (y a 44^{3k} − 1 para todo k)."],
 "Existe tal n; de hecho n = 3 sirve. Como 44 ≡ 2 (mód 7) y las potencias de 2 módulo 7 son 2, 4, 1, 2, 4, 1, …, se tiene 2³ = 8 ≡ 1 (mód 7). Luego 44³ ≡ 2³ ≡ 1 (mód 7), de modo que 7 divide a 44³ − 1.",
 "Periodicidad de potencias módulo 7 (el orden de 2 es 3): reducir la base y buscar el ciclo. Es un caso del pequeño teorema de Fermat. Verificado con Python: (44³ − 1) es divisible por 7.",
 10, ["aritmética modular", "orden multiplicativo", "pequeño teorema de Fermat"],
 ["potencias módulo m", "teoría de números elemental", "periodicidad"],
 "", ["modular", "divisibilidad", "fermat", "nivel-basico"], "cap. 1 (Ej. 16)"))

# =====================================================================
# INVERSION (11) — inducción y construcción (cap. 2)
# =====================================================================

A(P(244, "Una recurrencia que da 2·3ⁿ − 1", "inversion", 2,
 "Sea a₀ = 1 y a_{n+1} = 3aₙ + 2 para todo entero no negativo n. Demuestra que aₙ = 2·3ⁿ − 1.",
 ["Verifica la fórmula en n = 0 y luego prueba el paso inductivo: supón que vale para n y dedúcela para n+1.",
  "Base: a₀ = 2·3⁰ − 1 = 2 − 1 = 1. ✓. Supón aₙ = 2·3ⁿ − 1 (hipótesis inductiva).",
  "Sustituye la hipótesis en la recurrencia: a_{n+1} = 3aₙ + 2 = 3(2·3ⁿ − 1) + 2.",
  "Desarrolla: 3·2·3ⁿ − 3 + 2 = 2·3^{n+1} − 1.",
  "Eso es justo la fórmula para n+1, completando la inducción."],
 "aₙ = 2·3ⁿ − 1. Por inducción: la base a₀ = 2·3⁰ − 1 = 1 es correcta. Suponiendo aₙ = 2·3ⁿ − 1, la recurrencia da a_{n+1} = 3(2·3ⁿ − 1) + 2 = 2·3^{n+1} − 3 + 2 = 2·3^{n+1} − 1, que es la fórmula para n+1.",
 "Inducción directa sobre una recurrencia lineal de primer orden: sustituir la hipótesis y simplificar. Verificado con Python: aₙ = 2·3ⁿ − 1 para n = 0..20.",
 14, ["inducción", "recurrencia lineal de primer orden", "verificar y propagar"],
 ["soluciones cerradas de recurrencias", "progresiones geométricas trasladadas", "pruebas por inducción"],
 "", ["induccion", "recurrencia", "nivel-basico"], "cap. 2 (Ej. 5)"))

A(P(245, "La recurrencia 4aₙ − 1", "inversion", 2,
 "Sea a₀ = 1 y a_{n+1} = 4aₙ − 1 para todo entero no negativo n. Demuestra que aₙ = (2·4ⁿ + 1)/3.",
 ["Verifica la base y luego el paso inductivo sustituyendo la fórmula en la recurrencia.",
  "Base: a₀ = (2·4⁰ + 1)/3 = (2+1)/3 = 1. ✓. Supón aₙ = (2·4ⁿ + 1)/3.",
  "Sustituye: a_{n+1} = 4aₙ − 1 = 4·(2·4ⁿ + 1)/3 − 1.",
  "= (8·4ⁿ + 4)/3 − 1 = (8·4ⁿ + 4 − 3)/3 = (2·4^{n+1} + 1)/3.",
  "Eso es la fórmula para n+1, cerrando la inducción."],
 "aₙ = (2·4ⁿ + 1)/3. Por inducción: la base a₀ = (2+1)/3 = 1 es correcta. Suponiendo aₙ = (2·4ⁿ + 1)/3, la recurrencia da a_{n+1} = 4·(2·4ⁿ + 1)/3 − 1 = (8·4ⁿ + 4 − 3)/3 = (2·4^{n+1} + 1)/3.",
 "Inducción sobre una recurrencia lineal de primer orden con punto fijo en 1/3. Verificado con Python: aₙ = (2·4ⁿ + 1)/3 (entero) para n = 0..20.",
 14, ["inducción", "recurrencia lineal", "manipulación de fracciones"],
 ["puntos fijos de recurrencias", "soluciones cerradas", "pruebas por inducción"],
 "", ["induccion", "recurrencia", "nivel-basico"], "cap. 2 (Ej. 6)"))

A(P(246, "Suma acumulada que se duplica", "inversion", 3,
 "Sea a₀ = 1 y a_{n+1} = 2(a₀ + a₁ + ⋯ + aₙ) para todo entero no negativo n. Encuentra y demuestra una fórmula explícita para aₙ (n ≥ 1).",
 ["Calcula los primeros términos para conjeturar el patrón. a₀=1, a₁=2·1=2, a₂=2(1+2)=6, a₃=2(1+2+6)=18…",
  "Los términos 2, 6, 18, 54 sugieren aₙ = 2·3ⁿ⁻¹ para n ≥ 1. Pruébalo por inducción fuerte.",
  "Relaciona a_{n+1} con aₙ: a_{n+1} = 2(a₀+⋯+aₙ) y aₙ = 2(a₀+⋯+a_{n−1}). Resta para eliminar la suma.",
  "a_{n+1} − aₙ = 2aₙ, así que a_{n+1} = 3aₙ para n ≥ 1. Con a₁ = 2, esto da aₙ = 2·3ⁿ⁻¹.",
  "Verifica: a₁ = 2 = 2·3⁰, y a_{n+1} = 3aₙ = 3·2·3ⁿ⁻¹ = 2·3ⁿ. Fórmula demostrada."],
 "Para n ≥ 1, aₙ = 2·3ⁿ⁻¹. Restando a_{n+1} = 2(a₀+⋯+aₙ) y aₙ = 2(a₀+⋯+a_{n−1}) se obtiene a_{n+1} − aₙ = 2aₙ, es decir a_{n+1} = 3aₙ para n ≥ 1. Como a₁ = 2, la recurrencia geométrica da aₙ = 2·3ⁿ⁻¹.",
 "Convertir una recurrencia con suma acumulada en una de primer orden restando términos consecutivos (telescopaje de la suma). Verificado con Python: aₙ = 2·3ⁿ⁻¹ para n = 1..15.",
 18, ["inducción", "eliminar la suma acumulada", "recurrencia geométrica"],
 ["recurrencias con sumas parciales", "diferencias finitas", "soluciones cerradas"],
 "", ["induccion", "recurrencia", "suma-acumulada", "nivel-medio"], "cap. 2 (Ej. 7)"))

A(P(247, "n³ + 11n es divisible por 6", "inversion", 2,
 "Demuestra que para todo entero no negativo n, el número n³ + 11n es divisible por 6.",
 ["Inducción sobre n. Verifica n = 0 y estudia la DIFERENCIA entre el caso n+1 y el caso n.",
  "Base: 0³ + 11·0 = 0, divisible por 6. Supón que 6 divide a n³ + 11n.",
  "Calcula la diferencia (n+1)³ + 11(n+1) − (n³ + 11n) y simplifica.",
  "= 3n² + 3n + 1 + 11 = 3n² + 3n + 12 = 3(n² + n + 4). Falta ver que esto es divisible por 6, o sea que n²+n+4 es par.",
  "n² + n = n(n+1) es producto de dos consecutivos, siempre par; sumando 4 (par) sigue par. Así 3(n²+n+4) es divisible por 6, y la inducción cierra."],
 "Por inducción. Base: 0³ + 11·0 = 0 es divisible por 6. Paso: (n+1)³ + 11(n+1) − (n³ + 11n) = 3n² + 3n + 12 = 3(n² + n + 4); como n² + n = n(n+1) es par, n² + n + 4 es par, así que 3(n²+n+4) es divisible por 6. Sumado a n³+11n (divisible por 6 por hipótesis), también (n+1)³ + 11(n+1) lo es.",
 "Inducción por diferencias: probar que el incremento es divisible por 6 usando que n(n+1) es par. Verificado con Python: 6 | n³ + 11n para n = 0..59.",
 14, ["inducción", "divisibilidad por diferencias", "producto de consecutivos es par"],
 ["divisibilidad polinómica", "congruencias", "pruebas por inducción"],
 "", ["induccion", "divisibilidad", "nivel-basico"], "cap. 2 (Ej. 9)"))

A(P(248, "8ⁿ − 14n + 27 es divisible por 7", "inversion", 2,
 "Demuestra que si n es un entero positivo, entonces 8ⁿ − 14n + 27 es divisible por 7.",
 ["Inducción sobre n. Verifica n = 1 y mira la diferencia entre el caso n+1 y el caso n.",
  "Base: 8¹ − 14 + 27 = 21 = 7·3, divisible por 7. Supón que 7 divide a 8ⁿ − 14n + 27.",
  "Calcula a_{n+1} − aₙ = (8^{n+1} − 14(n+1) + 27) − (8ⁿ − 14n + 27).",
  "= 8^{n+1} − 8ⁿ − 14 = 8ⁿ(8 − 1) − 14 = 7·8ⁿ − 14 = 7(8ⁿ − 2).",
  "La diferencia 7(8ⁿ − 2) es divisible por 7; sumada a aₙ (divisible por 7), da a_{n+1} divisible por 7."],
 "Por inducción. Base: 8¹ − 14 + 27 = 21 = 7·3. Paso: la diferencia (8^{n+1} − 14(n+1) + 27) − (8ⁿ − 14n + 27) = 7·8ⁿ − 14 = 7(8ⁿ − 2) es divisible por 7. Sumada al caso n (divisible por 7), el caso n+1 también lo es.",
 "Inducción por diferencias: el incremento 7(8ⁿ−2) es manifiestamente múltiplo de 7. Verificado con Python: 7 | 8ⁿ − 14n + 27 para n = 1..39.",
 14, ["inducción", "divisibilidad por diferencias", "factorización del incremento"],
 ["divisibilidad de expresiones exponenciales", "congruencias", "pruebas por inducción"],
 "", ["induccion", "divisibilidad", "nivel-basico"], "cap. 2 (Ej. 11)"))

A(P(249, "Cortando cuadrados en cuatro", "inversion", 2,
 "Cortamos un cuadrado en cuatro cuadrados más pequeños; luego cortamos algunos de los cuadraditos obtenidos en cuatro cada uno, y así sucesivamente. Demuestra que en todo momento de este proceso el número total de cuadrados presentes es de la forma 3m + 1.",
 ["Inducción sobre el número de cortes realizados. ¿Cuántos cuadrados hay al inicio (cero cortes)?",
  "Al inicio hay 1 cuadrado = 3·0 + 1. Supón que tras cierto número de cortes hay 3m + 1 cuadrados.",
  "Cada corte toma UN cuadrado y lo reemplaza por cuatro. ¿Cómo cambia el conteo total?",
  "Un corte quita 1 cuadrado y añade 4, así que el total aumenta en 3.",
  "Si había 3m + 1, ahora hay 3m + 1 + 3 = 3(m+1) + 1, de nuevo de la forma 3m'+1. Por inducción, siempre lo es."],
 "Por inducción sobre el número de cortes. Base: con cero cortes hay 1 = 3·0 + 1 cuadrado. Paso: cada corte reemplaza un cuadrado por cuatro, aumentando el total en 3; si había 3m + 1 cuadrados, ahora hay 3m + 1 + 3 = 3(m+1) + 1. Por tanto el conteo siempre es de la forma 3m + 1.",
 "Invariante por inducción: cada operación incrementa el conteo en una cantidad fija (3), preservando la clase módulo 3. Verificado con Python: el conteo 1 + 3k es siempre ≡ 1 (mód 3).",
 12, ["inducción", "invariante módulo 3", "operación de incremento fijo"],
 ["procesos de subdivisión", "invariantes de conteo", "fractales y recursión"],
 "", ["induccion", "invariante", "cuadrados", "nivel-basico"], "cap. 2 (Ej. 12)"))

A(P(250, "El torneo donde alguien conoce a todos", "inversion", 3,
 "En un torneo de tenis cada par de jugadores se enfrenta exactamente una vez (no hay empates). Terminado el torneo, cada jugador escribe los nombres de quienes venció y los nombres de quienes fueron vencidos por alguien a quien él venció. Demuestra que al menos un jugador escribe los nombres de TODOS los demás.",
 ["Considera al jugador que ganó MÁS partidos (un 'rey' del torneo). Demuestra que su lista contiene a todos.",
  "Sea W un jugador con el máximo número de victorias, digamos k. Su lista incluye a los k que venció y a los vencidos por esos k.",
  "Supón, por contradicción, que algún jugador P NO está en la lista de W. Entonces P venció a W (no fue vencido por W) y P venció a todos los k que W venció (si no, P estaría en la lista).",
  "Pero entonces P ganó al menos k+1 partidos (a W más a los k), MÁS que W.",
  "Eso contradice que W tuviera el máximo de victorias. Luego la lista de W contiene a todos."],
 "Toma un jugador W con el máximo número de victorias k. Afirmamos que su lista (los k que venció más los vencidos por ellos) contiene a todos. Si algún P no estuviera en ella, P habría vencido a W y también a los k jugadores que W venció — por lo que P tendría al menos k+1 victorias, contradiciendo la maximalidad de W. Por tanto la lista de W contiene a todos los demás.",
 "Principio del extremo (el jugador con más victorias, un 'rey') combinado con argumento por contradicción. Es un resultado clásico sobre torneos. La 'solución' es el razonamiento, tomado del libro.",
 22, ["principio del extremo", "argumento por contradicción", "reyes de torneos"],
 ["torneos dirigidos", "grafos de competencia", "vértices dominantes"],
 "", ["torneo", "extremo", "contradiccion", "nivel-medio"], "cap. 2 (Ej. 2)"))

A(P(251, "Una fila de jugadores que se vencen", "inversion", 3,
 "En un torneo con 2ⁿ participantes, cada par jugó exactamente una vez (sin empates). Demuestra que se puede formar una fila con n + 1 jugadores de modo que cada uno haya vencido al que le sigue inmediatamente en la fila.",
 ["Inducción sobre n y construye la fila a partir de un jugador con muchas victorias.",
  "Base n=0: con 2⁰ = 1 jugador, la 'fila' de 1 persona cumple (vacuamente). Para el paso, mira al jugador que más ganó.",
  "En un torneo de 2^{n+1} jugadores, el que más ganó venció al menos a 2^{n+1}/2 = 2ⁿ jugadores (¿por qué? su número de victorias es al menos el promedio).",
  "Toma a ese jugador X y al subconjunto de los 2ⁿ que venció. Aplica la hipótesis inductiva a ese subgrupo de 2ⁿ jugadores.",
  "La hipótesis da una fila de n+1 jugadores dentro del subgrupo; poniendo a X al frente (X venció a todos ellos) se obtiene una fila de n+2 jugadores. Inducción completa."],
 "Por inducción sobre n. Base n=0: un solo jugador forma una fila válida de longitud 1. Paso: en un torneo de 2^{n+1} jugadores, el que más victorias tiene venció al menos a 2ⁿ de ellos (su total ≥ el promedio de victorias). Tomando a ese jugador X y a los 2ⁿ que venció, la hipótesis inductiva da una fila de n+1 dentro de ese subgrupo; anteponiendo X (que venció a todos ellos) se obtiene una fila de n+2 jugadores, cada uno venciendo al siguiente.",
 "Inducción constructiva: el jugador con más victorias domina la mitad, y se le antepone a la fila obtenida recursivamente en esa mitad. Verificado conceptualmente; el conteo 2^{n+1}/2 = 2ⁿ es exacto.",
 24, ["inducción constructiva", "principio del extremo", "torneos"],
 ["caminos dirigidos en torneos", "divide y vencerás", "órdenes de dominación"],
 "", ["torneo", "induccion", "construccion", "nivel-medio"], "cap. 2 (Ej. 3)"))

A(P(252, "Dividir un triángulo en 3n + 1 triángulos semejantes", "inversion", 3,
 "Demuestra que para todo entero positivo n se puede dividir cualquier triángulo en 3n + 1 triángulos semejantes a él.",
 ["Inducción sobre n. Busca una operación que aumente el número de piezas en una cantidad fija de 3.",
  "Base n=1: divide el triángulo por las paralelas medias en 4 = 3·1 + 1 triángulos semejantes (cada uno a escala 1/2).",
  "Para el paso, parte de una división en 3n + 1 triángulos semejantes. ¿Cómo añadir exactamente 3 piezas más?",
  "Toma UNO cualquiera de los triángulos semejantes y subdivídelo en 4 (por sus paralelas medias): eso quita 1 y añade 4.",
  "El total pasa de 3n + 1 a 3n + 1 + 3 = 3(n+1) + 1, todos semejantes al original. Inducción completa."],
 "Por inducción. Base n=1: las tres paralelas medias dividen el triángulo en 4 = 3·1 + 1 triángulos semejantes (a escala 1/2). Paso: dada una división en 3n + 1 triángulos semejantes, subdivide uno cualquiera en 4 (por sus paralelas medias); esto quita 1 y añade 4, dejando 3n + 1 + 3 = 3(n+1) + 1 triángulos, todos semejantes al original.",
 "Inducción constructiva con incremento fijo (+3 al subdividir uno en cuatro). La semejanza se conserva porque la subdivisión por paralelas medias produce copias a escala. Verificado: 3n+1 recorre 4,7,10,… para n=1,2,3,…",
 20, ["inducción constructiva", "semejanza de triángulos", "incremento fijo"],
 ["disecciones autosemejantes", "fractales (triángulo de Sierpiński)", "subdivisión geométrica"],
 "", ["induccion", "geometria", "semejanza", "nivel-medio"], "cap. 2 (Ej. 29)"))

A(P(253, "Partir un cuadrado en n cuadrados menores", "inversion", 3,
 "Demuestra que para todo entero n > 14 se puede partir un cuadrado en exactamente n cuadrados más pequeños (no necesariamente iguales).",
 ["Identifica primero qué valores 'base' de n sabes lograr, y luego una operación que aumente el conteo de forma controlada.",
  "Una operación clave: tomar uno de los cuadrados y partirlo en 4, lo que aumenta el conteo total en 3 (quita 1, pone 4).",
  "Encuentra particiones para tres valores consecutivos de n cualesquiera (que cubran las tres clases módulo 3). Por ejemplo, sabes hacer n = 4, 6, 7, 8, 9 directamente.",
  "Con la operación '+3' aplicada a una partición existente, desde n = 4 alcanzas 7, 10, 13, …; desde 6 alcanzas 9, 12, …; desde 8 alcanzas 11, 14, …",
  "Combinando las tres progresiones (que cubren las clases módulo 3) y los casos base, se alcanzan todos los n > 14 (de hecho todos salvo 2, 3, 5)."],
 "Para todo n > 14 (y en general para todo n salvo 2, 3 y 5) se puede partir un cuadrado en n cuadrados. La herramienta es la operación que parte un cuadrado en 4, aumentando el conteo en 3. Partiendo de los casos base 4, 6 y 8 (que cubren las tres clases módulo 3) y aplicando '+3' repetidamente, se alcanzan 4,7,10,…; 6,9,12,…; 8,11,14,…, cuya unión contiene todos los enteros n > 14.",
 "Inducción/construcción con paso fijo (+3) sobre representantes de las tres clases módulo 3. Verificado con Python: todo n de 15 a 39 es realizable (n = 1 o n ≥ 4 con n ≠ 5, y siempre para n > 14).",
 22, ["inducción constructiva", "clases módulo 3", "operación de incremento fijo"],
 ["disecciones de cuadrados", "cobertura de progresiones aritméticas", "construcciones combinatorias"],
 "", ["induccion", "geometria", "construccion", "nivel-medio"], "cap. 2 (Ej. 30)"))

A(P(254, "La recurrencia 10aₙ − 1", "inversion", 2,
 "Sea a₀ = 1 y a_{n+1} = 10aₙ − 1 para todo entero no negativo n. Demuestra que aₙ = (8·10ⁿ + 1)/9.",
 ["Verifica la base y luego el paso inductivo sustituyendo la fórmula en la recurrencia.",
  "Base: a₀ = (8·10⁰ + 1)/9 = (8+1)/9 = 1. ✓. Supón aₙ = (8·10ⁿ + 1)/9.",
  "Sustituye: a_{n+1} = 10aₙ − 1 = 10·(8·10ⁿ + 1)/9 − 1.",
  "= (80·10ⁿ + 10)/9 − 1 = (80·10ⁿ + 10 − 9)/9 = (8·10^{n+1} + 1)/9.",
  "Eso es la fórmula para n+1, completando la inducción."],
 "aₙ = (8·10ⁿ + 1)/9. Por inducción: la base a₀ = (8+1)/9 = 1 es correcta. Suponiendo aₙ = (8·10ⁿ + 1)/9, la recurrencia da a_{n+1} = 10·(8·10ⁿ + 1)/9 − 1 = (80·10ⁿ + 10 − 9)/9 = (8·10^{n+1} + 1)/9.",
 "Inducción sobre una recurrencia lineal con punto fijo en 1/9. Verificado con Python: aₙ = (8·10ⁿ + 1)/9 (entero, = 1, 9, 89, 889, …) para n = 0..15.",
 14, ["inducción", "recurrencia lineal", "punto fijo"],
 ["soluciones cerradas de recurrencias", "repunits y patrones de dígitos", "pruebas por inducción"],
 "", ["induccion", "recurrencia", "nivel-basico"], "cap. 2 (Ej. 20)"))

# =====================================================================
# OPTIMIZACION (11) — desigualdades (cap. 2) y grafos extremales (cap. 9)
# =====================================================================

A(P(255, "La desigualdad de las medias por inducción", "optimizacion", 4,
 "Demuestra por inducción la desigualdad entre la media geométrica y la aritmética: si a₁, a₂, …, aₙ son números no negativos, entonces ⁿ√(a₁a₂⋯aₙ) ≤ (a₁ + a₂ + ⋯ + aₙ)/n.",
 ["Usa la inducción 'hacia adelante y hacia atrás' de Cauchy: primero pruébala para potencias de 2, luego desciende.",
  "Base n=2: √(a₁a₂) ≤ (a₁+a₂)/2 equivale a 0 ≤ (√a₁ − √a₂)², que es cierto.",
  "Paso hacia adelante (duplicar): si vale para n, agrupa 2n números en dos bloques de n, aplica la hipótesis a cada bloque y luego el caso n=2 a las dos medias. Así vale para todas las potencias de 2.",
  "Paso hacia atrás (descender de n a n−1): dados a₁,…,a_{n−1}, añade aₙ = (a₁+⋯+a_{n−1})/(n−1) (su propia media aritmética) y aplica el caso n.",
  "El término extra se cancela y queda la desigualdad para n−1 números. Como subes a cualquier potencia de 2 y bajas de uno en uno, vale para todo n."],
 "ⁿ√(a₁⋯aₙ) ≤ (a₁+⋯+aₙ)/n. Por inducción de Cauchy: el caso n=2 es 0 ≤ (√a₁−√a₂)². El paso hacia adelante duplica n agrupando 2n números en dos bloques de n y aplicando la hipótesis más el caso n=2, cubriendo todas las potencias de 2. El paso hacia atrás baja de n a n−1 tomando aₙ igual a la media aritmética de los demás: al sustituir, el término extra se cancela y queda la desigualdad para n−1. Como se alcanza toda potencia de 2 y se desciende uno a uno, vale para todo n, con igualdad cuando todos los aᵢ son iguales.",
 "Inducción 'forward-backward' de Cauchy: el caso 2 más duplicación y descenso cubren todos los n. Verificado con Python: 3000 muestras no negativas cumplen GM ≤ AM.",
 30, ["inducción de Cauchy (forward-backward)", "media geométrica vs aritmética", "cuadrado perfecto base"],
 ["desigualdad de Jensen", "optimización", "desigualdades clásicas"],
 "", ["desigualdad", "am-gm", "cauchy", "nivel-avanzado"], "cap. 2 (Ej. 15)"))

A(P(256, "Media armónica contra media geométrica", "optimizacion", 3,
 "Demuestra que si a₁, a₂, …, aₙ son números reales positivos, entonces n / (1/a₁ + 1/a₂ + ⋯ + 1/aₙ) ≤ ⁿ√(a₁a₂⋯aₙ) (la media armónica no supera a la geométrica).",
 ["Relaciona la media armónica con la geométrica aplicando AM-GM a los RECÍPROCOS de los aᵢ.",
  "Aplica la desigualdad GM ≤ AM a los números 1/a₁, …, 1/aₙ.",
  "ⁿ√(1/a₁ · ⋯ · 1/aₙ) ≤ (1/a₁ + ⋯ + 1/aₙ)/n. El lado izquierdo es 1/ⁿ√(a₁⋯aₙ).",
  "Reescribe: 1/ⁿ√(a₁⋯aₙ) ≤ (Σ 1/aᵢ)/n. Toma recíprocos (invirtiendo el sentido de la desigualdad).",
  "ⁿ√(a₁⋯aₙ) ≥ n/(Σ 1/aᵢ), que es justo HM ≤ GM."],
 "HM ≤ GM. Aplicando GM ≤ AM a los recíprocos 1/aᵢ: ⁿ√(∏ 1/aᵢ) ≤ (Σ 1/aᵢ)/n, es decir 1/ⁿ√(∏ aᵢ) ≤ (Σ 1/aᵢ)/n. Tomando recíprocos (que invierte la desigualdad) se obtiene ⁿ√(∏ aᵢ) ≥ n/(Σ 1/aᵢ), o sea n/(Σ 1/aᵢ) ≤ ⁿ√(∏ aᵢ).",
 "HM ≤ GM se deduce de GM ≤ AM aplicada a los recíprocos. La cadena completa HM ≤ GM ≤ AM es la jerarquía clásica de medias. Verificado con Python: 3000 muestras positivas cumplen HM ≤ GM.",
 18, ["desigualdad de medias", "AM-GM sobre recíprocos", "tomar recíprocos"],
 ["jerarquía de medias (HM ≤ GM ≤ AM)", "optimización", "desigualdades clásicas"],
 "", ["desigualdad", "medias", "armonica", "nivel-medio"], "cap. 2 (Ej. 16)"))

A(P(257, "Tres a la n contra n a la cuarta", "optimizacion", 3,
 "Demuestra que 3ⁿ > n⁴ para todo entero n ≥ 8.",
 ["Inducción a partir de n = 8. Verifica la base y luego el paso multiplicando por 3.",
  "Base n=8: 3⁸ = 6561 y 8⁴ = 4096, así que 3⁸ > 8⁴. ✓. Supón 3ⁿ > n⁴.",
  "Para el paso, 3^{n+1} = 3·3ⁿ > 3n⁴. Basta probar que 3n⁴ ≥ (n+1)⁴ para n ≥ 8.",
  "3n⁴ ≥ (n+1)⁴ equivale a 3 ≥ (1 + 1/n)⁴. ¿Qué tan grande es (1+1/n)⁴ para n ≥ 8?",
  "Para n ≥ 8, (1 + 1/n)⁴ ≤ (9/8)⁴ = 6561/4096 ≈ 1.60 < 3, así que 3n⁴ > (n+1)⁴ y la inducción cierra."],
 "Por inducción desde n = 8. Base: 3⁸ = 6561 > 4096 = 8⁴. Paso: 3^{n+1} = 3·3ⁿ > 3n⁴, y basta ver 3n⁴ ≥ (n+1)⁴, que equivale a 3 ≥ (1+1/n)⁴; como para n ≥ 8 se tiene (1+1/n)⁴ ≤ (9/8)⁴ ≈ 1.60 < 3, la desigualdad se cumple. Por tanto 3ⁿ > n⁴ para todo n ≥ 8.",
 "Inducción cuyo paso se reduce a acotar (1+1/n)⁴ por debajo de 3. Verificado con Python: 3ⁿ > n⁴ para n = 8..39.",
 18, ["inducción", "exponencial vs polinómica", "acotar (1+1/n)⁴"],
 ["crecimiento exponencial vs polinómico", "desigualdades por inducción", "análisis asintótico"],
 "", ["induccion", "desigualdad", "exponencial", "nivel-medio"], "cap. 2 (Ej. 10)"))

A(P(258, "Cien números, noventa y nueve sumas no negativas", "optimizacion", 4,
 "La suma de cien números reales dados es cero. Demuestra que al menos 99 de las sumas por parejas (sumas de dos de ellos) son no negativas. ¿Es óptimo este resultado?",
 ["Ordena los números a₁ ≤ a₂ ≤ ⋯ ≤ a₁₀₀ y razona sobre las sumas aᵢ + aⱼ usando que el total es 0.",
  "Distingue según el signo de a₅₀ + a₉₉. Si a₅₀ + a₉₉ ≥ 0, entonces aᵢ + a₉₉ ≥ 0 para i ≥ 50 (51 sumas) y aᵢ + a₁₀₀ ≥ aᵢ + a₉₉ para i de 50 a 98 (49 sumas más).",
  "Esas dos familias dan 51 + 49 = 100 sumas no negativas (cuida el solapamiento; quedan ≥ 99).",
  "Si a₅₀ + a₉₉ < 0, demuestra que aₙ + a₁₀₀ ≥ 0 para todos: como la suma total es 0 y los pequeños son muy negativos, a₁ + a₁₀₀ ≥ 0, dando 99 sumas con a₁₀₀.",
  "En ambos casos hay ≥ 99 sumas no negativas. El óptimo: con a₁₀₀ = 99 y a₁ = ⋯ = a₉₉ = −1 (suma 0), exactamente 99 sumas son no negativas (las que incluyen a₁₀₀)."],
 "Al menos 99 sumas por parejas son no negativas, y 99 es óptimo. Ordenando a₁ ≤ ⋯ ≤ a₁₀₀ con suma 0: si a₅₀ + a₉₉ ≥ 0, las familias {aᵢ + a₉₉ : i ≥ 50} y {aᵢ + a₁₀₀ : 50 ≤ i ≤ 98} aportan ≥ 99 sumas no negativas; si a₅₀ + a₉₉ < 0, se prueba que a₁ + a₁₀₀ ≥ 0, de modo que las 99 sumas aⱼ + a₁₀₀ (j ≤ 99) son no negativas. El ejemplo a₁₀₀ = 99, a₁ = ⋯ = a₉₉ = −1 (suma 0) tiene exactamente 99 sumas no negativas, así que el resultado es el mejor posible.",
 "Argumento extremal sobre los números ordenados (monotonizar) más un ejemplo que alcanza la cota. Verificado con Python: el ejemplo a₁₀₀=99, resto −1 produce exactamente 99 sumas no negativas.",
 30, ["principio del extremo", "ordenar y monotonizar", "cota óptima con ejemplo"],
 ["combinatoria extremal", "sumas de parejas", "análisis de casos extremos"],
 "", ["extremo", "sumas", "optimo", "nivel-avanzado"], "cap. 1 (Ej. 8)"))

A(P(259, "Veintiocho aristas fuerzan un cuadrilátero", "optimizacion", 4,
 "Sea G un grafo simple con 10 vértices y 28 aristas. Demuestra que G contiene un ciclo de longitud 4.",
 ["Un ciclo de longitud 4 aparece cuando dos vértices tienen dos vecinos comunes. Busca dos vértices de grado alto.",
  "La suma de los grados es 2·28 = 56. Por el principio del casillero, hay dos vértices cuya suma de grados es grande (al menos 12).",
  "Toma esos dos vértices A y B (suma de grados ≥ 12). Entre ambos tocan al menos 12 'extremos' de aristas, dirigidos hacia los otros 8 vértices.",
  "Doce extremos repartidos entre 8 vértices: por el casillero, al menos dos vértices C, D son vecinos de A y de B a la vez.",
  "Entonces A–C–B–D–A es un ciclo de longitud 4."],
 "G contiene un C₄. La suma de grados es 2·28 = 56, así que existen dos vértices A, B con suma de grados ≥ 12. Sus aristas tocan a los otros 8 vértices con al menos (≈)12 extremos; por el principio del casillero, dos vértices C, D son adyacentes tanto a A como a B. Entonces A–C–B–D–A es un ciclo de longitud 4. (De hecho ex(10; C₄) = 16, así que cualquier grafo de 10 vértices con más de 16 aristas contiene un C₄.)",
 "Conteo doble + casillero: grado total alto fuerza vecinos comunes, que crean el C₄. Verificado con Python: 20 000 grafos aleatorios de 10 vértices y 28 aristas SIEMPRE contienen un C₄, y el número extremal ex(10; C₄) = 16 < 28.",
 26, ["principio del casillero", "vecinos comunes y C₄", "número extremal de Turán-Zarankiewicz"],
 ["teoría de grafos extremal", "el problema de Zarankiewicz", "conteo doble"],
 "", ["grafos", "extremal", "ciclo", "nivel-avanzado"], "cap. 9 (Ej. 3)"))

A(P(260, "Suma de grados y un vértice de grado cuatro", "optimizacion", 2,
 "Sea G un grafo simple con 9 vértices, y supón que la suma de todos los grados es al menos 27. Demuestra que G tiene un vértice de grado al menos 4.",
 ["Recuerda que la suma de los grados de un grafo siempre es PAR. ¿Qué implica eso para 'al menos 27'?",
  "Como la suma es par y ≥ 27, en realidad es ≥ 28.",
  "Si los 9 vértices tuvieran todos grado ≤ 3, ¿cuál sería la suma máxima de grados?",
  "9 vértices con grado ≤ 3 dan suma ≤ 27 < 28. Contradicción con que la suma es ≥ 28.",
  "Por tanto algún vértice tiene grado ≥ 4."],
 "G tiene un vértice de grado ≥ 4. La suma de grados es par, así que de ser ≥ 27 es en realidad ≥ 28. Si todos los 9 vértices tuvieran grado ≤ 3, la suma sería ≤ 27 < 28, una contradicción. Luego algún vértice tiene grado ≥ 4.",
 "Paridad de la suma de grados (≥27 ⇒ ≥28) más un argumento de promedio/casillero. Verificado con Python: el promedio 28/9 > 3 fuerza un grado ≥ 4.",
 12, ["lema del apretón de manos", "argumento de promedio", "paridad de la suma de grados"],
 ["secuencias de grados", "principio del casillero", "teoría de grafos"],
 "", ["grafos", "grados", "promedio", "nivel-basico"], "cap. 9 (Ej. 4)"))

A(P(261, "Treinta y ocho aristas fuerzan un K₄", "optimizacion", 5,
 "Sea G un grafo simple con 10 vértices y 38 aristas. Demuestra que G contiene un K₄ inducido (cuatro vértices mutuamente adyacentes).",
 ["Cuenta, sobre todos los subconjuntos de 4 vértices, cuántas aristas inducen en promedio. Si el promedio es alto, alguno tiene muchas.",
  "Hay C(10,4) = 210 subconjuntos de 4 vértices. Suma, sobre todos ellos, el número de aristas inducidas: cada arista se cuenta en C(8,2) = 28 de esos subconjuntos.",
  "La suma total es 38·28 = 1064, así que el promedio de aristas por cuádruple es 1064/210 ≈ 5.07.",
  "Por el principio del casillero, algún cuádruple induce al menos ⌈5.07⌉ = 6 aristas.",
  "Un conjunto de 4 vértices con 6 aristas es K₄ (el máximo de aristas entre 4 vértices es C(4,2) = 6). Ese es el K₄ inducido."],
 "G contiene un K₄ inducido. Sobre los C(10,4) = 210 cuádruples de vértices, la suma del número de aristas inducidas es 38·C(8,2) = 38·28 = 1064 (cada arista está en 28 cuádruples). El promedio es 1064/210 ≈ 5.07, así que por el principio del casillero algún cuádruple induce ≥ 6 aristas; como 6 = C(4,2) es el máximo posible, ese cuádruple es un K₄.",
 "Conteo doble (aristas por cuádruple) + casillero: el promedio > 5 fuerza un cuádruple con las 6 aristas. Verificado con Python: ⌈1064/210⌉ = 6 = C(4,2).",
 32, ["conteo doble", "principio del casillero", "subgrafo completo inducido"],
 ["teoría de grafos extremal", "teorema de Turán", "promedios y casillero"],
 "", ["grafos", "extremal", "k4", "nivel-experto"], "cap. 9 (Ej. 5)"))

A(P(262, "Grado tres en siete vértices implica conexo", "optimizacion", 3,
 "Demuestra que no existe un grafo simple con 7 vértices que sea disconexo y en el que cada vértice tenga grado al menos 3.",
 ["Si el grafo fuera disconexo, se partiría en componentes. ¿Qué tamaño mínimo necesita una componente para que sus vértices tengan grado ≥ 3?",
  "En una componente, cada vértice solo puede tener vecinos DENTRO de ella. Para que un vértice tenga grado ≥ 3, su componente necesita al menos 4 vértices.",
  "Así que cada componente tiene ≥ 4 vértices. Si hay al menos dos componentes, el total de vértices es ≥ 4 + 4 = 8.",
  "Pero el grafo tiene solo 7 vértices, lo que impide dos componentes de tamaño ≥ 4.",
  "Por tanto no puede ser disconexo: con grado mínimo 3 y 7 vértices, el grafo es necesariamente conexo."],
 "No existe tal grafo. Si fuera disconexo, cada componente debería tener al menos 4 vértices (un vértice de grado ≥ 3 necesita 3 vecinos dentro de su componente). Dos o más componentes sumarían ≥ 8 vértices, imposible con solo 7. Luego un grafo de 7 vértices con grado mínimo 3 es necesariamente conexo.",
 "Argumento extremal sobre el tamaño mínimo de una componente con grado mínimo dado: 4 vértices por componente y 7 < 8 fuerzan la conexión. La 'solución' es el razonamiento, tomado del libro.",
 18, ["argumento extremal", "tamaño mínimo de componente", "grado mínimo y conexión"],
 ["conexión en grafos", "componentes conexas", "cotas por grado mínimo"],
 "", ["grafos", "conexion", "grado-minimo", "nivel-medio"], "cap. 9 (Ej. 38)"))

A(P(263, "Grado mínimo k garantiza un ciclo largo", "optimizacion", 3,
 "Sea G un grafo simple en el que todo vértice tiene grado al menos k (con k ≥ 2). Demuestra que G contiene un ciclo de longitud al menos k + 1.",
 ["Aplica el principio del extremo a los CAMINOS de G: considera un camino lo más largo posible.",
  "Toma un camino simple P de longitud máxima, con extremo v. Todos los vecinos de v deben estar SOBRE el camino (si no, podrías alargarlo).",
  "El vértice v tiene al menos k vecinos, y todos están en P. Considera el vecino de v más alejado a lo largo del camino.",
  "Ese vecino w, junto con el tramo del camino entre v y w, forma un ciclo. ¿Cuántos vértices abarca ese tramo?",
  "Como v tiene k vecinos en el camino, el más lejano está al menos a k pasos; el ciclo v…w…v tiene longitud ≥ k + 1."],
 "G contiene un ciclo de longitud ≥ k + 1. Toma un camino simple de longitud máxima con extremo v. Por maximalidad, todos los vecinos de v están sobre el camino. Como v tiene ≥ k vecinos en el camino, el más lejano w está al menos a k aristas de v a lo largo de él; el tramo de v a w más la arista vw forman un ciclo de longitud ≥ k + 1.",
 "Principio del extremo (camino más largo): el extremo no puede tener vecinos fuera del camino, y su vecino más lejano cierra un ciclo largo. La 'solución' es el argumento, tomado del libro.",
 22, ["principio del extremo", "camino de longitud máxima", "ciclos a partir de caminos"],
 ["teoría de grafos", "circunferencia (girth/circumference)", "argumentos por elemento extremo"],
 "", ["grafos", "extremo", "ciclo", "nivel-medio"], "cap. 9 (Ej. 39)"))

A(P(264, "Una recurrencia acotada por 3ⁿ", "optimizacion", 3,
 "Sea a₀ = a₁ = 1 y a_{n+2} = a_{n+1} + 5aₙ para todo n ≥ 0. Demuestra que aₙ ≤ 3ⁿ para todo n ≥ 0.",
 ["Inducción FUERTE (usa los dos casos anteriores). Verifica las dos bases y luego el paso.",
  "Bases: a₀ = 1 ≤ 3⁰ = 1 y a₁ = 1 ≤ 3¹ = 3. ✓. Supón aₖ ≤ 3ᵏ para todo k ≤ n+1.",
  "Acota a_{n+2} usando la recurrencia y la hipótesis: a_{n+2} = a_{n+1} + 5aₙ ≤ 3^{n+1} + 5·3ⁿ.",
  "Factoriza 3ⁿ: 3^{n+1} + 5·3ⁿ = 3ⁿ(3 + 5) = 8·3ⁿ. Compáralo con 3^{n+2} = 9·3ⁿ.",
  "8·3ⁿ ≤ 9·3ⁿ = 3^{n+2}, así que a_{n+2} ≤ 3^{n+2}. La inducción fuerte cierra."],
 "aₙ ≤ 3ⁿ. Por inducción fuerte: a₀ = a₁ = 1 ≤ 3⁰, 3¹. Suponiendo aₖ ≤ 3ᵏ para k ≤ n+1, la recurrencia da a_{n+2} = a_{n+1} + 5aₙ ≤ 3^{n+1} + 5·3ⁿ = 8·3ⁿ ≤ 9·3ⁿ = 3^{n+2}. Por tanto aₙ ≤ 3ⁿ para todo n.",
 "Inducción fuerte con una cota cómoda: la combinación 3^{n+1} + 5·3ⁿ = 8·3ⁿ queda por debajo de 9·3ⁿ. Verificado con Python: aₙ ≤ 3ⁿ para n = 0..20.",
 18, ["inducción fuerte", "acotar una recurrencia", "factorizar potencias"],
 ["recurrencias lineales", "cotas de crecimiento", "raíces características vs cotas simples"],
 "", ["induccion", "recurrencia", "cota", "nivel-medio"], "cap. 2 (Ej. 24)"))

A(P(265, "Una secuencia de grados imposible", "optimizacion", 3,
 "Demuestra que no existe ningún grafo simple con 6 vértices cuyos grados sean 4, 4, 4, 2, 1, 1.",
 ["Aplica el criterio de Havel–Hakimi: el vértice de mayor grado debe conectarse a otros, reduciendo sus grados.",
  "Ordena los grados de mayor a menor: 4, 4, 4, 2, 1, 1. Toma el primer 4: debe unirse a cuatro de los demás, restando 1 a sus grados.",
  "Conéctalo a los siguientes cuatro mayores (4, 4, 2, 1): la secuencia restante es 3, 3, 1, 0, 1 → reordena a 3, 3, 1, 1, 0.",
  "Repite con el nuevo 3: debe unirse a tres vértices, pero solo quedan 3, 1, 1, 0 con valores positivos suficientes. Réstale a los tres mayores (3, 1, 1) → 2, 0, 0, 0.",
  "Sigue: ahora hay un 2 pero solo quedan dos vértices con grado positivo necesario; el proceso produce un grado negativo. La secuencia NO es realizable."],
 "No existe tal grafo. Por el criterio de Havel–Hakimi, al conectar el vértice de grado 4 con los cuatro siguientes mayores la secuencia se reduce, y tras un par de pasos se llega a pedir más conexiones de las disponibles (aparece un déficit), de modo que la secuencia 4,4,4,2,1,1 no es 'gráfica'. (Equivalentemente, los tres vértices de grado 4 obligan a una estructura incompatible con los grados 1 restantes.)",
 "Criterio de Havel–Hakimi / Erdős–Gallai para decidir si una secuencia de grados es realizable. Verificado con Python: el algoritmo de Havel–Hakimi declara [4,4,4,2,1,1] no gráfica (y también [4,4,3,2,1]).",
 18, ["criterio de Havel–Hakimi", "secuencias gráficas", "reducción de grados"],
 ["teoría de grafos", "realizabilidad de secuencias de grados", "teorema de Erdős–Gallai"],
 "", ["grafos", "grados", "havel-hakimi", "nivel-medio"], "cap. 9 (Ej. 17)"))

# =====================================================================
# PATRONES (11) — identidades (cap. 2) y conteo de grafos (cap. 9)
# =====================================================================

A(P(266, "La suma de cubos es un cuadrado", "patrones", 2,
 "Demuestra que para todo entero positivo n se cumple 1³ + 2³ + ⋯ + n³ = (1 + 2 + ⋯ + n)².",
 ["Calcula ambos lados para n pequeños y confirma el patrón; luego prueba por inducción.",
  "Para n=1,2,3: 1 = 1², 1+8 = 9 = 3², 1+8+27 = 36 = 6². El lado derecho es (n(n+1)/2)².",
  "Inducción: supón 1³+⋯+n³ = (n(n+1)/2)². Suma (n+1)³ a ambos lados.",
  "(n(n+1)/2)² + (n+1)³ = (n+1)²[n²/4 + (n+1)] = (n+1)²(n²+4n+4)/4 = (n+1)²(n+2)²/4.",
  "= ((n+1)(n+2)/2)², que es el lado derecho para n+1. Inducción completa."],
 "1³ + ⋯ + n³ = (1 + ⋯ + n)² = (n(n+1)/2)². Por inducción: base 1 = 1². Paso: (n(n+1)/2)² + (n+1)³ = (n+1)²[n²/4 + n + 1] = (n+1)²(n+2)²/4 = ((n+1)(n+2)/2)², la fórmula para n+1.",
 "Identidad de Nicómaco: la suma de los primeros n cubos es el cuadrado del n-ésimo número triangular. Verificado con Python: 1³+⋯+n³ = (n(n+1)/2)² para n = 1..39.",
 14, ["identidad de Nicómaco", "inducción", "números triangulares"],
 ["sumas de potencias", "identidades algebraicas", "fórmulas cerradas"],
 "", ["identidad", "cubos", "induccion", "nivel-basico"], "cap. 2 (Ej. 17)"))

A(P(267, "Suma de productos de consecutivos", "patrones", 2,
 "Encuentra una fórmula cerrada (sin signos de sumatoria) para la expresión Σᵢ₌₁ⁿ i(i + 1) = 1·2 + 2·3 + ⋯ + n(n+1).",
 ["Separa i(i+1) = i² + i y usa las fórmulas conocidas de Σi² y Σi. O busca un patrón telescópico.",
  "Σ i(i+1) = Σ i² + Σ i = n(n+1)(2n+1)/6 + n(n+1)/2. Factoriza n(n+1).",
  "= n(n+1)[(2n+1)/6 + 1/2] = n(n+1)[(2n+1+3)/6] = n(n+1)(2n+4)/6.",
  "= n(n+1)·2(n+2)/6 = n(n+1)(n+2)/3.",
  "Alternativamente, i(i+1) = [i(i+1)(i+2) − (i−1)i(i+1)]/3 telescopa directamente a n(n+1)(n+2)/3."],
 "Σᵢ₌₁ⁿ i(i+1) = n(n+1)(n+2)/3. Separando i(i+1) = i² + i y usando Σi² = n(n+1)(2n+1)/6, Σi = n(n+1)/2, se factoriza n(n+1) y se obtiene n(n+1)(n+2)/3. (También sale por telescopaje: i(i+1) = [i(i+1)(i+2) − (i−1)i(i+1)]/3.)",
 "Buscar el patrón vía descomposición o telescopaje; el resultado es 3 veces un coeficiente binomial: n(n+1)(n+2)/3 = 2·C(n+2, 3). Verificado con Python: Σ i(i+1) = n(n+1)(n+2)/3 para n = 1..39.",
 14, ["telescopaje", "sumas de potencias", "factorización"],
 ["sumas telescópicas", "coeficientes binomiales", "fórmulas cerradas"],
 "", ["identidad", "suma", "telescopaje", "nivel-basico"], "cap. 2 (Ej. 19)"))

A(P(268, "La recurrencia con raíz doble", "patrones", 3,
 "Sea a₀ = 0, a₁ = 1 y a_{n+2} = 6a_{n+1} − 9aₙ para todo n ≥ 0. Demuestra que aₙ = n·3ⁿ⁻¹.",
 ["Resuelve la recurrencia lineal: halla su ecuación característica y observa si tiene raíz doble.",
  "La ecuación característica es x² − 6x + 9 = 0, es decir (x − 3)² = 0: raíz DOBLE x = 3.",
  "Con raíz doble r, la solución general es aₙ = (A + Bn)·3ⁿ. Ajusta A y B con las condiciones iniciales.",
  "a₀ = A = 0, así que A = 0. a₁ = (0 + B)·3 = 3B = 1, así que B = 1/3.",
  "Entonces aₙ = (n/3)·3ⁿ = n·3ⁿ⁻¹. Verifica que cumple la recurrencia."],
 "aₙ = n·3ⁿ⁻¹. La ecuación característica x² − 6x + 9 = (x−3)² = 0 tiene la raíz doble 3, así que la solución general es aₙ = (A + Bn)·3ⁿ. De a₀ = A = 0 y a₁ = 3B = 1 se obtiene A = 0, B = 1/3, luego aₙ = (n/3)·3ⁿ = n·3ⁿ⁻¹.",
 "Resolver una recurrencia lineal con raíz característica doble: la solución incorpora el factor n. Verificado con Python: aₙ = n·3ⁿ⁻¹ (= 0, 1, 6, 27, 108, …) para n = 0..20.",
 18, ["recurrencias lineales", "ecuación característica", "raíz doble"],
 ["soluciones cerradas de recurrencias", "raíces repetidas", "álgebra lineal de sucesiones"],
 "", ["recurrencia", "raiz-doble", "patron", "nivel-medio"], "cap. 2 (Ej. 23)"))

A(P(269, "Cuántos grafos hay", "patrones", 2,
 "¿Cuántos grafos simples diferentes hay sobre el conjunto de vértices etiquetados [n] = {1, 2, …, n}? Demuestra tu fórmula.",
 ["Un grafo queda determinado por cuáles pares de vértices están unidos. Cuenta los pares posibles.",
  "El número de pares de vértices (posibles aristas) es C(n,2) = n(n−1)/2.",
  "Para cada par, hay dos opciones independientes: la arista está presente o ausente.",
  "Como las decisiones son independientes, el total es 2 elevado al número de pares.",
  "Hay 2^{C(n,2)} = 2^{n(n−1)/2} grafos simples etiquetados sobre [n]."],
 "Hay 2^{C(n,2)} = 2^{n(n−1)/2} grafos. Un grafo simple sobre [n] queda determinado por el subconjunto de pares de vértices que son aristas; como hay C(n,2) pares posibles y cada uno está presente o ausente de forma independiente, el total es 2^{C(n,2)}.",
 "Conteo por elección independiente sobre cada arista potencial: 2 opciones por par, C(n,2) pares. Verificado con Python: 2^{C(3,2)} = 8 y 2^{C(4,2)} = 64.",
 12, ["principio del producto", "subconjuntos de aristas", "conteo de estructuras"],
 ["enumeración de grafos etiquetados", "conjuntos potencia", "principio de la multiplicación"],
 "", ["conteo", "grafos", "producto", "nivel-basico"], "cap. 9 (Ej. 7)"))

A(P(270, "Las simetrías de cuatro grafos", "patrones", 3,
 "Un automorfismo de un grafo es una biyección de sus vértices en sí mismos que preserva las aristas. Cuenta los automorfismos de: (a) el grafo completo Kₙ; (b) el ciclo Cₙ; (c) el camino Pₙ; (d) la estrella Sₙ (un centro de grado n−1 y n−1 hojas).",
 ["Para cada grafo, pregúntate qué permutaciones de vértices preservan la estructura de aristas.",
  "(a) En Kₙ todos los pares son aristas, así que CUALQUIER permutación las preserva: hay n! automorfismos.",
  "(b) En el ciclo Cₙ, un automorfismo es una de las simetrías del polígono regular: n rotaciones y n reflexiones, total 2n.",
  "(c) En el camino Pₙ, solo puedes dejarlo igual o invertirlo extremo con extremo: 2 automorfismos.",
  "(d) En la estrella Sₙ, el centro (único vértice de grado n−1) debe fijarse, y las n−1 hojas se permutan libremente: (n−1)! automorfismos."],
 "Los conteos son: (a) Kₙ tiene n! automorfismos (toda permutación preserva las aristas); (b) Cₙ tiene 2n (las n rotaciones y n reflexiones del polígono regular); (c) Pₙ tiene 2 (la identidad y la inversión del camino); (d) Sₙ tiene (n−1)! (el centro se fija y las n−1 hojas se permuten libremente).",
 "Contar automorfismos identificando qué estructura debe preservarse (todas las aristas, el ciclo, los extremos, el centro). Verificado con Python: aut(K₄)=24=4!, aut(C₅)=10=2·5, aut(P₄)=2, aut(S₅)=24=4!.",
 18, ["automorfismos de grafos", "grupos de simetría", "preservación de estructura"],
 ["teoría de grupos y simetrías", "grupo diédrico", "isomorfismos de grafos"],
 "", ["conteo", "grafos", "automorfismos", "nivel-medio"], "cap. 9 (Ej. 8)"))

A(P(271, "Ciclos hamiltonianos del grafo completo", "patrones", 3,
 "¿Cuántos ciclos hamiltonianos distintos tiene el grafo completo Kₙ? (Dos ciclos son iguales si tienen el mismo conjunto de aristas.)",
 ["Un ciclo hamiltoniano es un orden circular de los n vértices. Cuenta los órdenes y luego corrige por las repeticiones.",
  "Hay n! maneras de ordenar los n vértices en una secuencia. Cada ciclo hamiltoniano corresponde a varias de estas secuencias.",
  "Un mismo ciclo se puede empezar en cualquiera de sus n vértices (n rotaciones) y recorrer en dos direcciones (2 sentidos).",
  "Así que cada ciclo está contado 2n veces entre las n! secuencias.",
  "El número de ciclos hamiltonianos distintos es n!/(2n) = (n−1)!/2."],
 "Kₙ tiene (n−1)!/2 ciclos hamiltonianos. Cada ciclo es un orden circular de los n vértices; hay n! secuencias lineales, pero cada ciclo (como conjunto de aristas) se cuenta 2n veces (n puntos de inicio × 2 direcciones), de modo que el número de ciclos distintos es n!/(2n) = (n−1)!/2.",
 "Conteo con sobreconteo controlado: dividir las n! ordenaciones por las 2n simetrías de un ciclo. Verificado con Python: K₅ tiene (4!)/2 = 12 ciclos hamiltonianos (enumeración directa).",
 18, ["conteo con sobreconteo", "ciclos hamiltonianos", "simetrías de rotación y reflexión"],
 ["permutaciones circulares", "el problema del viajante", "enumeración de ciclos"],
 "", ["conteo", "grafos", "hamiltoniano", "nivel-medio"], "cap. 9 (Ej. 33)"))

A(P(272, "Muchos grafos no isomorfos", "patrones", 3,
 "Demuestra que hay más de 6600 grafos simples no isomorfos sobre 8 vértices.",
 ["Cuenta los grafos ETIQUETADOS sobre 8 vértices y luego acota cuántas etiquetas distintas puede tener una misma 'forma' (clase de isomorfismo).",
  "Hay 2^{C(8,2)} = 2^{28} = 268 435 456 grafos etiquetados sobre 8 vértices.",
  "Cada grafo no etiquetado (clase de isomorfismo) corresponde a a lo más 8! = 40 320 grafos etiquetados (las maneras de etiquetar sus 8 vértices).",
  "Entonces el número de clases de isomorfismo es al menos 2²⁸ / 8! = 268 435 456 / 40 320.",
  "268 435 456 / 40 320 ≈ 6657.6 > 6600, así que hay más de 6600 grafos no isomorfos."],
 "Hay más de 6600 grafos no isomorfos sobre 8 vértices. El número de grafos etiquetados es 2^{C(8,2)} = 2²⁸ = 268 435 456. Cada clase de isomorfismo agrupa a lo más 8! = 40 320 grafos etiquetados (las reetiquetaciones de sus vértices), así que el número de clases es al menos 2²⁸/8! ≈ 6657.6 > 6600.",
 "Cota inferior por conteo: grafos etiquetados divididos por el máximo de reetiquetaciones (8!). Verificado con Python: 2²⁸/8! ≈ 6657.6 > 6600.",
 18, ["cota por conteo", "clases de isomorfismo", "acción de reetiquetado"],
 ["enumeración de grafos no etiquetados", "órbitas y lema de Burnside", "cotas combinatorias"],
 "", ["conteo", "grafos", "isomorfismo", "nivel-medio"], "cap. 9 (Ej. 9)"))

A(P(273, "Las simetrías del cubo", "patrones", 4,
 "Considera el grafo del cubo (8 vértices, cada uno unido a los tres que difieren en una coordenada). Demuestra que tiene exactamente 48 automorfismos.",
 ["El grafo del cubo es el esqueleto de un cubo geométrico; cuenta sus simetrías. Empieza fijando una cara.",
  "Un automorfismo queda determinado por la imagen de una cara (cuatro vértices). ¿A cuántas caras puede ir una cara dada y de cuántas formas?",
  "Una cara puede mapearse a cualquiera de las 6 caras del cubo, y sobre cada cara destino hay 4 rotaciones posibles: eso da 6·4 = 24 simetrías que preservan la orientación.",
  "Además, cada una de esas 24 puede componerse con una reflexión (que invierte la orientación), duplicando el conteo.",
  "24 que preservan la orientación + 24 que la invierten = 48 automorfismos en total."],
 "El grafo del cubo tiene 48 automorfismos. Un automorfismo se determina por la imagen de una cara: hay 6 caras destino y 4 rotaciones por cara, dando 24 simetrías que preservan la orientación; componiendo cada una con una reflexión se obtienen otras 24 que la invierten. En total 6·4·2 = 48 (el grupo de simetría del cubo, isomorfo a S₄ × ℤ₂).",
 "Contar simetrías geométricas del cubo: orientación (24) por reflexión (×2). Verificado con Python: un contador exhaustivo de automorfismos del grafo Q₃ (vértices = cadenas de 3 bits, aristas a distancia de Hamming 1) da exactamente 48.",
 28, ["automorfismos de grafos", "grupo de simetría del cubo", "orientación y reflexión"],
 ["teoría de grupos (S₄ × ℤ₂)", "simetrías de poliedros", "grupos de isometrías"],
 "", ["conteo", "grafos", "cubo", "nivel-avanzado"], "cap. 9 (Ej. 19)"))

A(P(274, "Ciclos hamiltonianos del cubo", "patrones", 3,
 "Demuestra que el grafo del cubo Q₃ (8 vértices, las cadenas de 3 bits, con aristas entre cadenas que difieren en un bit) tiene exactamente 6 ciclos hamiltonianos.",
 ["Un ciclo hamiltoniano recorre los 8 vértices del cubo. Aprovecha la simetría (48 automorfismos) para no contar a ciegas.",
  "Cuenta primero por enumeración o por simetría: fija una arista inicial y extiende, o usa que los 48 automorfismos permutan los ciclos hamiltonianos.",
  "Cada ciclo hamiltoniano del cubo (un hexágono… en realidad un 8-ciclo) usa 8 aristas de las 12 del cubo, dejando 4 aristas fuera que forman un emparejamiento perfecto especial.",
  "Los ciclos hamiltonianos del cubo se corresponden con ciertos pares de caras opuestas / direcciones; un conteo cuidadoso (o la enumeración directa) da 6.",
  "Enumerando todos los recorridos cerrados que visitan los 8 vértices exactamente una vez (corrigiendo por inicio y dirección) se obtienen exactamente 6 ciclos hamiltonianos."],
 "El grafo del cubo Q₃ tiene exactamente 6 ciclos hamiltonianos. Cada uno es un 8-ciclo que usa 8 de las 12 aristas del cubo; enumerando los recorridos cerrados que visitan los ocho vértices una sola vez (e identificando los que difieren solo en punto de inicio o dirección) se obtienen 6 ciclos distintos. La alta simetría del cubo (48 automorfismos) agrupa estos 6 en una sola órbita.",
 "Enumeración aprovechando la simetría del cubo; los 6 ciclos forman una única órbita bajo el grupo de automorfismos. Verificado con Python: un enumerador de ciclos hamiltonianos sobre Q₃ encuentra exactamente 6.",
 22, ["ciclos hamiltonianos", "enumeración con simetría", "el cubo Q₃"],
 ["caminos en hipercubos", "códigos de Gray", "conteo de ciclos"],
 "", ["conteo", "grafos", "hamiltoniano", "nivel-medio"], "cap. 9 (Ej. 37)"))

A(P(275, "Tres fracciones unitarias que suman 1", "patrones", 3,
 "Encuentra todas las ternas de enteros positivos a < b < c para las cuales 1/a + 1/b + 1/c = 1.",
 ["Acota a usando el orden a < b < c: el término 1/a es el mayor de los tres. ¿Qué valores puede tomar a?",
  "Como a < b < c, se tiene 1/a > 1/3 (si fuera 1/a ≤ 1/3, la suma sería < 1). Y 1/a < 1 (un solo término no llega a 1). Así a ∈ {2, 3}.",
  "Si a = 3, entonces 1/b + 1/c = 2/3 con b > 3; pero 1/b + 1/c < 2/3, contradicción. Luego a = 2.",
  "Con a = 2: 1/b + 1/c = 1/2 con b > 2. Por el mismo argumento, 1/b > 1/4, así que b ∈ {3, 4} (y b < c).",
  "b = 3 da 1/c = 1/6 → c = 6. b = 4 da 1/c = 1/4 → c = 4, pero c > b falla. Única terna: (2, 3, 6)."],
 "La única terna es (2, 3, 6). Como a < b < c, el mayor término 1/a debe cumplir 1/3 < 1/a < 1, así que a = 2 (a = 3 daría 1/b + 1/c = 2/3 imposible con b, c > 3). Con a = 2, queda 1/b + 1/c = 1/2 con b > 2; b = 3 da c = 6, y b = 4 daría c = 4 (no cumple c > b). Por tanto (a, b, c) = (2, 3, 6).",
 "Acotar la variable más pequeña con el principio del extremo reduce el problema a un puñado de casos. Verificado con Python: la única solución con a < b < c es (2, 3, 6).",
 18, ["acotar variables", "fracciones unitarias", "principio del extremo"],
 ["ecuaciones diofantinas", "fracciones egipcias", "descomposición de la unidad"],
 "", ["diofantina", "fracciones", "egipcias", "nivel-medio"], "cap. 1 (Ej. 2)"))

A(P(276, "Cuatro fracciones unitarias distintas que suman 1", "patrones", 4,
 "Encuentra todas las cuádruplas de enteros positivos distintos a < b < c < d tales que 1/a + 1/b + 1/c + 1/d = 1.",
 ["Acota a: como es la variable más pequeña, 1/a domina la suma. ¿Entre qué valores está a?",
  "Como hay cuatro términos decrecientes que suman 1, se tiene 1/4 < 1/a < 1, así que a ∈ {2, 3} (a=1 ya excede 1).",
  "Para cada a, queda 1/b + 1/c + 1/d = 1 − 1/a con b > a, y se acota b del mismo modo. Luego c y d quedan en rangos finitos.",
  "Recorre los casos a ∈ {2,3}, luego b, luego c, despejando d. Solo cuenta las soluciones con a < b < c < d.",
  "Resultan exactamente seis cuádruplas: (2,3,7,42), (2,3,8,24), (2,3,9,18), (2,3,10,15), (2,4,5,20), (2,4,6,12)."],
 "Las cuádruplas son (2,3,7,42), (2,3,8,24), (2,3,9,18), (2,3,10,15), (2,4,5,20) y (2,4,6,12). Acotando la variable más pequeña (1/4 < 1/a < 1 ⇒ a ∈ {2,3}) y, fijada a, acotando sucesivamente b y c, el problema se reduce a un rango finito que se barre por casos; la búsqueda exhaustiva da exactamente esas seis soluciones con a < b < c < d.",
 "Acotar variables en cascada con el principio del extremo y barrer el rango finito resultante. Verificado con Python: las únicas seis cuádruplas distintas con suma 1 son las listadas.",
 26, ["acotar variables en cascada", "fracciones unitarias", "búsqueda por casos"],
 ["fracciones egipcias", "ecuaciones diofantinas", "descomposición de la unidad"],
 "", ["diofantina", "fracciones", "egipcias", "nivel-avanzado"], "cap. 1 (Ej. 18)"))

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
