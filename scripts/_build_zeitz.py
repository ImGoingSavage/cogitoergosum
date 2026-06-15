# -*- coding: utf-8 -*-
"""Tanda 28 — Zeitz, *The Art and Craft of Problem Solving* (3rd ed.). Append 44
problemas verificados a data/problems.json. Todas las afirmaciones numéricas
fueron verificadas con Python antes de escribir (ver /tmp/verify_zeitz*.py y la
bitácora de HANDOFFCES.md). Builder idempotente: aborta si hay choque de ids.
Sector C (entrenamiento), esquema §4.1, ids 145-188, balanceado 11/11/11/11."""
import json, sys, collections

SRC = "Zeitz, *The Art and Craft of Problem Solving* (3rd ed., Wiley 2017)"

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
# INVERSION (11) — simetría, reflexión, juegos, trabajar hacia atrás, descenso
# =====================================================================

A(P(145, "El censista y las tres hijas", "inversion", 3,
 "Un censista toca una puerta y pregunta a la mujer cuántas hijas tiene y sus edades (enteros). "
 "Ella dice: «Tengo tres hijas; el producto de sus edades es 36». El censista responde: «No es suficiente». "
 "Ella añade: «Te diría la suma de sus edades, pero seguirías sin poder». «Dame un dato más». "
 "«Mi hija mayor, Ana, adora a los perros». ¿Qué edades tienen las tres hijas?",
 ["No empieces por la mayor: empieza por el ÚNICO dato duro. ¿Qué tripletas de enteros positivos multiplican 36?",
  "Lista todas las tripletas (a≤b≤c) con a·b·c = 36 y calcula la SUMA de cada una. La trabajaremos hacia atrás desde las pistas.",
  "El censista, que VE la suma (el número de la casa), sigue sin decidir. Eso solo es posible si DOS tripletas comparten la misma suma. ¿Cuáles son?",
  "Las únicas dos con suma repetida son (1,6,6) y (2,2,9), ambas suman 13. Por eso la suma no basta. Ahora usa la última pista.",
  "«La hija MAYOR» implica que hay una mayor única. En (1,6,6) las dos mayores empatan; en (2,2,9) hay mayor única. La respuesta queda forzada."],
 "Las edades son 2, 2 y 9. Trabajando hacia atrás: de las tripletas con producto 36, las únicas dos con suma idéntica son (1,6,6) y (2,2,9), ambas con suma 13 — por eso conocer la suma no desambigua, lo que revela que la suma es 13. La frase «la hija mayor» exige una mayor única, lo que descarta (1,6,6) (dos seises empatan) y deja (2,2,9).",
 "Modelo de razonamiento hacia atrás: cada frase del diálogo es una restricción que se decodifica al revés. «No basta con el producto» no informa (hay varias tripletas); «no bastaría la suma» SÍ informa, porque solo es cierto en el caso de suma repetida. Verificado con Python: entre las 8 tripletas, solo suma 13 se repite, y solo (2,2,9) tiene máximo único.",
 18, ["razonamiento hacia atrás", "información como restricción", "desambiguación"],
 ["acertijos de deducción lógica", "diseño de preguntas diagnósticas", "teoría de la información"],
 "", ["censista", "deduccion", "clasico", "nivel-medio"], "cap. 1 (Ej. 1.1.3)"))

A(P(146, "El camino más corto que toca dos ejes", "inversion", 2,
 "Encuentra la longitud del camino más corto que va del punto (3, 5) al punto (8, 2) y que toca tanto el eje x como el eje y.",
 ["Un camino que rebota en una recta y luego va a un destino es difícil de optimizar directamente. ¿Y si pudieras «enderezarlo»?",
  "La técnica de reflexión: reflejar un extremo respecto de la recta que toca convierte el camino quebrado en uno recto de igual longitud.",
  "Hay que tocar AMBOS ejes. Refleja el punto inicial (3,5) respecto del eje y, y el punto final (8,2) respecto del eje x.",
  "(3,5) reflejado en el eje y es (−3,5); (8,2) reflejado en el eje x es (8,−2). El camino mínimo es la recta entre los dos reflejados.",
  "Distancia = √((8−(−3))² + (−2−5)²) = √(121+49) = √170."],
 "La longitud mínima es √170 ≈ 13.04. Reflejando el origen (3,5) sobre el eje y → (−3,5) y el destino (8,2) sobre el eje x → (8,−2), todo camino que toca ambos ejes tiene la misma longitud que un camino recto entre los puntos reflejados. El más corto es el segmento recto: √((8+3)²+(−2−5)²) = √(121+49) = √170.",
 "La reflexión «desdobla» los rebotes: es el principio detrás de la ley de reflexión óptica y del problema del salvavidas. Invertir el problema (reflejar en vez de minimizar con cálculo) lo vuelve trivial. Verificado con Python: búsqueda en malla fina sobre los dos puntos de toque da 13.0384 = √170.",
 15, ["reflexión", "minimización geométrica", "ley de reflexión"],
 ["óptica (camino de la luz)", "diseño de rutas con paradas obligatorias", "billar matemático"],
 "", ["reflexion", "geometria", "optimizacion-geometrica", "nivel-basico"], "cap. 3 §3.1 (Ej. 3.1.13)"))

A(P(147, "El triángulo de perímetro mínimo (Putnam 1998)", "inversion", 4,
 "Dado un punto (a, b) con 0 < b < a, determina el perímetro mínimo de un triángulo que tiene un vértice en (a, b), otro vértice sobre el eje x y el tercer vértice sobre la recta y = x. (Supón que el triángulo de perímetro mínimo existe.)",
 ["El perímetro es una suma de tres distancias con dos puntos libres (uno en cada recta). Optimizar dos variables a la vez es duro: ¿puedes enderezar?",
  "Aplica reflexión DOS veces: refleja el vértice fijo (a,b) respecto de cada una de las dos rectas donde están los vértices libres.",
  "Refleja (a,b) sobre el eje x para obtener P₁, y sobre la recta y=x para obtener P₂. El perímetro iguala la longitud de un camino de P₁ a P₂.",
  "P₁ = (a,−b) (reflexión en eje x). P₂ = (b,a) (reflexión en y=x intercambia coordenadas). El perímetro mínimo es |P₁P₂|.",
  "|P₁P₂| = √((a−b)² + (−b−a)²) = √((a−b)²+(a+b)²) = √(2a²+2b²) = √(2(a²+b²))."],
 "El perímetro mínimo es √(2(a²+b²)). Reflejando el vértice fijo (a,b) sobre el eje x → (a,−b) y sobre la recta y=x → (b,a), el perímetro de cualquier triángulo admisible iguala la longitud de un camino del primer reflejado al segundo pasando por los dos ejes; el mínimo es el segmento recto: √((a−b)²+(a+b)²) = √(2(a²+b²)).",
 "Doble reflexión: cuando los vértices libres viven en rectas, reflejar el vértice fijo sobre cada recta convierte el perímetro en una distancia recta entre puntos reflejados. Verificado con Python para (a,b)=(5,3): |P₁P₂| = 8.2462 = √(2·34) = √68.",
 30, ["doble reflexión", "perímetro mínimo", "puntos sobre rectas"],
 ["trayectorias de rebote múltiple", "redes de espejos", "problemas isoperimétricos"],
 "1998", ["reflexion", "putnam", "perimetro", "nivel-avanzado"], "cap. 3 §3.1 (Ej. 3.1.17, Putnam 1998)"))

A(P(148, "Una integral que se resuelve mirándola al revés (Putnam 1980)", "inversion", 4,
 "Evalúa la integral ∫₀^{π/2} dx / (1 + (tan x)^√2).",
 ["No intentes una antiderivada: el exponente √2 lo impide. Busca una SIMETRÍA de la integral en el intervalo [0, π/2].",
  "La sustitución u = π/2 − x refleja el intervalo sobre su punto medio. ¿Qué le pasa a tan x bajo esa reflexión?",
  "tan(π/2 − x) = cot x = 1/tan x. Sustituye y obtén una segunda expresión I para la MISMA integral.",
  "Llamando I a la integral, la sustitución da I = ∫₀^{π/2} (tan x)^√2 /(1+(tan x)^√2) dx. Suma las dos formas de I.",
  "Sumando: 2I = ∫₀^{π/2} 1 dx = π/2, así que I = π/4."],
 "La integral vale π/4. Con I la integral original, la sustitución u = π/2 − x (que manda tan→cot=1/tan) produce I = ∫₀^{π/2} (tan x)^√2/(1+(tan x)^√2) dx. Sumando ambas expresiones de I, los integrandos suman 1, de modo que 2I = ∫₀^{π/2} dx = π/2, y por tanto I = π/4.",
 "Truco de simetría rey: invertir el intervalo con u = a+b−x. El exponente concreto (√2, 2, π…) es irrelevante; lo único que importa es que f(x)+f(reflejado) = 1. Verificado con Python: cuadratura numérica da 0.785398 = π/4.",
 25, ["simetría de integrales", "sustitución reflexiva", "truco rey-reina"],
 ["promedios sobre dominios simétricos", "identidades trigonométricas", "argumentos de paridad"],
 "1980", ["integral", "simetria", "putnam", "nivel-avanzado"], "cap. 3 §3.1 (Ej. 3.1.25, Putnam 1980)"))

A(P(149, "Las monedas sobre la mesa", "inversion", 3,
 "Dos jugadores se turnan para colocar una moneda idéntica sobre una mesa rectangular. Ninguna moneda puede tocar a otra ya colocada ni salirse de la mesa. La mesa empieza vacía. El último que logre colocar una moneda legalmente gana. ¿Tiene el primer jugador una estrategia ganadora? Descríbela.",
 ["No cuentes cuántas monedas caben: piensa en cómo el primer jugador puede COPIAR al segundo. ¿Qué punto de la mesa es especial?",
  "El rectángulo tiene un centro de simetría. ¿Qué pasa si el primer jugador lo ocupa de inmediato?",
  "Tras jugar en el centro, el primer jugador puede responder a cada jugada del rival con la jugada SIMÉTRICA respecto del centro.",
  "Si la jugada del rival es legal, su reflejada respecto del centro también lo es (la configuración era simétrica antes de la jugada del rival). Verifica que el centro ya ocupado nunca estorba.",
  "El primer jugador siempre tiene respuesta; como la mesa es finita, el segundo jugador se queda sin movimientos primero. El primero gana."],
 "Sí: el primer jugador gana. Coloca su primera moneda exactamente en el centro de la mesa. A partir de ahí, responde a cada moneda del rival con una colocada en la posición simétrica respecto del centro. Por la simetría central, si la jugada del rival fue legal, su imagen reflejada también lo es (y no choca con la del centro, salvo casos imposibles por tamaño). Así el primer jugador siempre puede mover después del segundo; como caben finitas monedas, el segundo se queda atascado primero.",
 "Estrategia de emparejamiento por simetría: ocupar el punto fijo de la simetría y luego espejar al rival. La invariancia «la posición es simétrica justo antes de la jugada del rival» se mantiene por inducción. Es el mismo esqueleto que mata muchos juegos imparciales.",
 20, ["estrategia de simetría", "emparejamiento", "punto fijo"],
 ["juegos imparciales", "estrategias de copia (mirroring)", "teoría de juegos combinatoria"],
 "", ["juego", "simetria", "estrategia-ganadora", "nivel-medio"], "cap. 3 §3.1 (Ej. 3.1.20)"))

A(P(150, "Doblando papel para probar que √2 es irracional", "inversion", 4,
 "Supón, buscando una contradicción, que √2 fuera racional. Entonces existiría un triángulo rectángulo isósceles de papel cuyos tres lados son enteros (cateto a, hipotenusa c, con c² = 2a²). Dobla el triángulo de modo que un cateto quede pegado sobre la hipotenusa. Completa el argumento para llegar a una contradicción.",
 ["Si √2 = c/a en mínimos términos con a,c enteros, tienes un triángulo rectángulo isósceles de lados enteros. La idea es FABRICAR uno más pequeño.",
  "Trabaja hacia atrás desde la contradicción: si siempre puedes construir uno menor con lados enteros, el descenso infinito es imposible. Dobla el papel.",
  "Dobla el vértice del ángulo recto sobre la hipotenusa, llevando un cateto a yacer sobre ella. El pliegue crea un nuevo triángulo rectángulo isósceles más pequeño.",
  "Marca el punto donde el cateto (longitud a) cae sobre la hipotenusa (longitud c). El segmento sobrante de la hipotenusa mide c−a; por tangentes iguales, el nuevo triángulo tiene catetos c−a e hipotenusa 2a−c, todos enteros.",
  "Obtienes un triángulo rectángulo isósceles de lados ENTEROS estrictamente menores. Repetir da una sucesión infinita decreciente de enteros positivos: imposible. Luego √2 es irracional."],
 "El doblez produce un triángulo rectángulo isósceles de lados enteros estrictamente más pequeño: catetos de longitud c−a e hipotenusa 2a−c (enteros positivos por las longitudes de tangentes iguales del pliegue). Si existiera un triángulo entero, existiría uno menor, y luego otro, generando una sucesión infinita y decreciente de enteros positivos — imposible por el buen orden. La contradicción prueba que no hay triángulo entero, es decir, √2 es irracional.",
 "Descenso infinito geométrico (Conway): en lugar de manipular fracciones, se fabrica un objetivo más pequeño y se invoca el buen orden. Es el mismo motor que la prueba aritmética clásica (si c²=2a² con (a,c)=1, ambos son pares: contradicción), pero hecho con papel. Trabajar hacia atrás desde «¿y si siempre puedo achicar?» es la clave.",
 30, ["descenso infinito", "buen orden", "prueba por contradicción"],
 ["irracionalidad de raíces", "el método del descenso de Fermat", "fracciones en mínimos términos"],
 "", ["descenso-infinito", "irracionalidad", "geometria", "nivel-avanzado"], "cap. 3 §3.2 (Ej. 3.2.13)"))

A(P(151, "Quitar centavos: deja un múltiplo de 5", "inversion", 2,
 "Empieza con 17 centavos. Dos jugadores se turnan y en cada turno quitan entre 1 y 4 centavos (no se puede pasar). Quien quita el último centavo gana. ¿Tiene algún jugador estrategia ganadora? ¿Cuál es la primera jugada correcta?",
 ["Analiza posiciones pequeñas hacia atrás. Con 1, 2, 3 o 4 centavos, el jugador en turno gana de inmediato. ¿Y con 5?",
  "Con 5 centavos, quites lo que quites (1–4) dejas al rival entre 1 y 4: él gana. Así que 5 es una posición PERDEDORA para quien le toca mover.",
  "Posición perdedora = la dejas al rival y ganas. ¿Qué tienen en común 5, 10, 15…? Trabaja hacia atrás desde el 0.",
  "Las posiciones perdedoras (para quien mueve) son los múltiplos de 5. Tu meta es siempre PRESENTAR al rival un múltiplo de 5.",
  "Desde 17, quita 2 para dejar 15 (múltiplo de 5). Luego, sin importar lo que el rival quite (1–4), tú repones hasta el siguiente múltiplo de 5. El primer jugador gana."],
 "El primer jugador gana. Las posiciones perdedoras para quien está en turno son exactamente los múltiplos de 5: si te presentan un múltiplo de 5, cualquier resta de 1–4 deja un no-múltiplo, y el rival lo restaura. Desde 17, el primer jugador quita 2 dejando 15; después responde a cada resta k del rival con 5−k, manteniendo múltiplos de 5 hasta dejar 0 y ganar.",
 "Trabajar hacia atrás desde la posición terminal (0) etiqueta cada estado como ganador o perdedor. El invariante de la estrategia («presenta múltiplo de 5») nace de que 1+4 = 2+3 = 5: el primer jugador controla la suma de cada par de jugadas. Verificado con Python (solver retrógrado): las P-posiciones son {0,5,10,…} y 17 es ganadora.",
 12, ["análisis retrógrado", "posiciones ganadoras/perdedoras", "aritmética modular en juegos"],
 ["juego de Nim de un montón", "teoría de juegos combinatoria", "estrategias de complemento"],
 "", ["juego", "hacia-atras", "modular", "nivel-basico"], "cap. 4 §4.4 (Ej. 4.4.1)"))

A(P(152, "Restar un divisor: gana quien deja impar", "inversion", 3,
 "Empieza con 100 centavos. En cada turno, el jugador en turno quita un divisor del número de centavos que quedan, siempre que ese divisor sea ESTRICTAMENTE menor que la cantidad actual. (Por ejemplo, desde 100 puedes quitar 1, 2, 4, 5, 10, 20, 25 o 50, pero no 100.) El juego termina cuando queda 1 centavo (su único divisor es 1, que no es menor que 1). Quien hace la última jugada gana. ¿Quién gana?",
 ["Colorea posiciones hacia atrás: 1 es terminal (quien la recibe ya no puede mover). Analiza paridad de los números pequeños.",
  "Si recibes un número PAR, ¿puedes siempre dejarle al rival uno IMPAR? (Pista: 1 es divisor de todo.)",
  "Si recibes un número IMPAR, todos sus divisores son impares, así que al restar siempre dejas un número PAR. No tienes escapatoria.",
  "Conclusión: las posiciones impares son perdedoras para quien mueve; las pares son ganadoras. Tu estrategia: deja siempre impar al rival.",
  "100 es par: el primer jugador resta 1 y deja 99 (impar). El rival se ve forzado a devolver un par, y así hasta llegar al 1 impar. El primer jugador gana."],
 "Gana el primer jugador. Por paridad: si recibes un número impar, todos sus divisores son impares, así que cualquier resta deja un número par — estás atrapado. Si recibes un número par, restando 1 (divisor de todo) puedes dejar impar. Por tanto las posiciones impares pierden y las pares ganan para quien mueve. Como 100 es par, el primer jugador resta 1 dejando 99 (impar) y mantiene al rival en impares hasta el 1 final.",
 "Coloreo de estados (verde/rojo) más invariante de paridad: el divisor 1 garantiza siempre poder cambiar la paridad, y un impar nunca tiene divisor par. Verificado con Python (solver retrógrado): la posición a mover gana sii el número es par; 100 es ganadora.",
 18, ["coloreo de posiciones", "paridad", "análisis retrógrado"],
 ["juegos de sustracción", "funciones de Grundy", "argumentos de paridad"],
 "", ["juego", "divisores", "paridad", "nivel-medio"], "cap. 4 §4.4 (Ej. 4.4.3)"))

A(P(153, "Nim con tres montones (17, 11, 8)", "inversion", 4,
 "Hay tres montones de frijoles con 17, 11 y 8 frijoles. Dos jugadores se turnan; una jugada consiste en quitar uno o más frijoles de UN solo montón. Quien toma el último frijol gana. ¿Quién tiene estrategia ganadora desde (17, 11, 8) y cuál es la primera jugada correcta?",
 ["Con un montón es trivial; con dos, copias al rival para igualarlos. Con tres necesitas la magia del Nim: piensa en BINARIO.",
  "Escribe cada montón en binario y considera el «o-exclusivo» (XOR) bit a bit, también llamado suma de Nim. ¿Qué valor da?",
  "17 = 10001₂, 11 = 01011₂, 8 = 01000₂. Calcula el XOR de los tres: las posiciones perdedoras son las de XOR = 0.",
  "17 ⊕ 11 ⊕ 8 = 18 ≠ 0, así que la posición es ganadora para quien mueve. Debes mover para volver el XOR a 0.",
  "18 = 10010₂. Para anular el XOR, modifica el montón cuyo bit líder coincide: 17 ⊕ 18 = 3, así que reduce el montón de 17 a 3, dejando (3, 11, 8) con XOR 0. El primer jugador gana."],
 "El primer jugador gana. La teoría de Nim dice que una posición es perdedora (para quien mueve) sii la suma de Nim (XOR binario) de los montones es 0. Aquí 17 ⊕ 11 ⊕ 8 = 18 ≠ 0, así que es ganadora. La jugada correcta lleva el XOR a 0: como 17 ⊕ (11 ⊕ 8) = 17 ⊕ 3 = … en concreto 17 ⊕ 18 = 3, el primer jugador reduce el montón de 17 a 3, dejando (3, 11, 8) con suma de Nim 0.",
 "El teorema de Bouton: invertir el juego revela que XOR = 0 son las P-posiciones, porque desde XOR=0 toda jugada lo vuelve ≠0, y desde ≠0 siempre puedes restaurarlo a 0. Verificado con Python: 17^11^8 = 18, y existe jugada que lo anula (reducir 17→3).",
 28, ["suma de Nim", "representación binaria", "teorema de Bouton"],
 ["juegos imparciales y teoría de Sprague-Grundy", "códigos correctores (paridad XOR)", "criptografía con XOR"],
 "", ["nim", "xor", "juego", "nivel-avanzado"], "cap. 4 §4.4 (Ej. 4.4.7)"))

A(P(154, "Cuatro montones partidos (Putnam 1995)", "inversion", 5,
 "Un juego empieza con cuatro montones de frijoles que contienen 3, 4, 5 y 6 frijoles. Los jugadores se turnan. Una jugada consiste en quitar UN frijol de un montón, siempre que queden al menos dos frijoles en ese montón, O bien retirar por completo un montón de tamaño 2 o 3. Gana quien retira el último montón. Para ganar, ¿quieres mover primero o segundo? Da la estrategia.",
 ["Las jugadas son raras: solo «quitar 1 si quedan ≥2» o «borrar un montón de tamaño 2 o 3». Reduce a un juego conocido analizando un montón aislado.",
  "Un montón de tamaño n se comporta como un juego imparcial: calcula su función de Grundy. Un montón de 1 frijol está muerto (no permite jugadas).",
  "Calcula los valores de Grundy de montones de tamaño 1,2,3,4,5,6. Recuerda: desde n≥3 puedes ir a n−1; desde 2 o 3 puedes borrar (ir al estado vacío).",
  "La posición global es ganadora para quien mueve sii el XOR de los valores de Grundy de los cuatro montones es ≠ 0. Calcúlalo para (3,4,5,6).",
  "El XOR de Grundy de (3,4,5,6) resulta ≠ 0, así que quien mueve PRIMERO gana; mueve hacia la posición de XOR 0."],
 "El primer jugador gana. Cada montón es un juego imparcial independiente; asignándole su valor de Grundy y combinándolos con XOR (teoría de Sprague-Grundy), la posición inicial (3,4,5,6) tiene suma de Nim distinta de cero. Por tanto el primer jugador tiene una jugada que lleva el juego a suma de Nim 0 y gana con la estrategia estándar de Nim sobre los valores de Grundy.",
 "Descomponer en componentes imparciales y trabajar hacia atrás con Grundy/XOR. Verificado con Python: un solver retrógrado sobre el estado (tupla ordenada de montones) confirma que (3,4,5,6) es victoria para quien mueve.",
 35, ["teoría de Sprague-Grundy", "suma de juegos", "análisis retrógrado"],
 ["juegos imparciales compuestos", "diseño de IA para juegos", "descomposición de problemas"],
 "1995", ["juego", "grundy", "putnam", "nivel-experto"], "cap. 4 §4.4 (Ej. 4.4.10, Putnam 1995)"))

A(P(155, "Romper la barra de chocolate", "inversion", 3,
 "Dos personas se turnan para romper una barra de chocolate de 6 × 8 cuadritos. Solo se puede romper una pieza a lo largo de una línea recta entre cuadritos (una ruptura separa una pieza en dos). Quien NO pueda romper más (porque solo quedan cuadritos sueltos) pierde; dicho de otro modo, gana quien hace la última ruptura. ¿Hay estrategia ganadora para el primero o el segundo jugador? ¿Y en el caso general m × n?",
 ["No diseñes jugadas astutas todavía. Cuenta algo que NO dependa de cómo se juega: ¿cuántas piezas hay al principio y al final?",
  "Cada ruptura aumenta el número de piezas EXACTAMENTE en 1. Empiezas con 1 pieza y terminas con mn cuadritos sueltos.",
  "Entonces el número total de rupturas en toda la partida es FIJO: mn − 1, sin importar las decisiones. El ganador depende solo de la paridad de ese número.",
  "Gana quien hace la ruptura número mn−1 (la última). El primer jugador hace las rupturas impares (1ª, 3ª, …). ¿mn−1 es par o impar para 6×8?",
  "Para 6×8: mn−1 = 47, impar. La última ruptura es de número impar, hecha por el primer jugador. El primer jugador gana. En general gana el primero sii mn es par."],
 "Para 6 × 8 gana el primer jugador. Clave: cada ruptura aumenta el número de piezas en 1, así que la partida SIEMPRE dura exactamente mn − 1 rupturas, sin importar cómo se juegue (es un monovariante determinista). Quien hace la ruptura mn−1 gana. Para 6×8, mn−1 = 47 (impar), hecha por el primer jugador. En general, el primer jugador gana sii mn − 1 es impar, es decir, sii mn es par.",
 "Monovariante invariante: el resultado no depende de la estrategia, solo de la paridad de una cantidad fija. Trabajar hacia atrás desde «¿quién hace la última jugada?» con un conteo invariante resuelve toda la familia m×n de un golpe. Verificado con Python: el número de rupturas es siempre mn−1 (probado para m,n ≤ 4); 6×8 da 47, impar.",
 18, ["monovariante", "conteo invariante", "paridad del total de jugadas"],
 ["juegos cuyo resultado no depende de la estrategia", "conteo de componentes (grafos/árboles)", "argumentos de paridad"],
 "", ["juego", "chocolate", "monovariante", "nivel-medio"], "cap. 3 §3.4 (Ej. 3.4.26)"))

# =====================================================================
# INVARIANTES (11) — paridad, coloreo, monovariante, casillero
# =====================================================================

A(P(156, "¿Se puede embaldosar un 66 × 62 con fichas 12 × 1?", "invariantes", 3,
 "¿Es posible cubrir exactamente un rectángulo de 66 × 62 con fichas de 12 × 1 (sin huecos ni traslapes, las fichas pueden ir horizontales o verticales)?",
 ["El área 66·62 es divisible entre 12, así que el conteo de área no lo prohíbe. Necesitas un invariante más fino: un COLOREO.",
  "Colorea las casillas con 12 colores en un patrón diagonal cíclico (la casilla (i,j) recibe el color (i+j) mód 12). ¿Qué tiene de especial una ficha 12×1?",
  "Toda ficha 12×1, horizontal o vertical, cubre exactamente uno de cada uno de los 12 colores. Si hubiera embaldosado, cada color aparecería el MISMO número de veces.",
  "Cuenta cuántas casillas hay de cada color en el 66×62. Si los conteos NO son todos iguales, el embaldosado es imposible.",
  "Descomponiendo el rectángulo, el subrectángulo 6×2 sobrante no es «homogéneo» (los 12 colores no salen parejos), así que el embaldosado es IMPOSIBLE. Equivalente: un a×b se embaldosa con 1×k sii k|a o k|b; aquí 12∤66 y 12∤62."],
 "No es posible. Coloreando la casilla (i,j) con el color (i+j) mód 12, cada ficha 12×1 cubre exactamente uno de cada color. Un embaldosado exigiría que los 12 colores aparezcan igual de veces; pero al descomponer el 66×62, el bloque sobrante 6×2 no reparte los colores parejo. Equivalente al teorema de de Bruijn: un rectángulo a×b se cubre con fichas 1×k sii k divide a a o a b. Como 66 = 12·5+6 y 62 = 12·5+2, ni 66 ni 62 son múltiplos de 12, y el embaldosado es imposible (aunque 12 | 66·62).",
 "Coloreo como invariante: la divisibilidad del área es necesaria pero no suficiente; un coloreo periódico detecta la obstrucción real. Verificado con Python: un backtracking exacto confirma el teorema de de Bruijn (1×k cubre a×b sii k|a o k|b) en tableros pequeños.",
 22, ["coloreo periódico", "teorema de de Bruijn", "embaldosado"],
 ["teoría de embaldosados", "argumentos de coloreo en tableros", "imposibilidad por invariante"],
 "", ["coloreo", "embaldosado", "de-bruijn", "nivel-medio"], "cap. 3 §3.4 (Ej. 3.4.13)"))

A(P(157, "El problema de las fichas de Conway", "invariantes", 5,
 "Coloca una ficha en cada punto de coordenadas enteras del plano con ordenada y ≤ 0 (el semiplano inferior, lleno). El único movimiento legal es un «salto»: una ficha brinca sobre una ficha vecina (horizontal o verticalmente) a la casilla inmediatamente siguiente, que debe estar vacía; la ficha saltada se retira. ¿Es posible, con un número finito de saltos, llevar una ficha hasta la línea y = 5?",
 ["Experimenta: llegar a y=2 es fácil, y=3 cuesta. Pero los ejemplos no revelan el límite. Necesitas un MONOVARIANTE que solo decrezca.",
  "Asigna a cada casilla un peso ζ^d, donde d es la distancia «de taxi» (en pasos de rejilla) hasta el objetivo C=(0,5), y ζ es una constante por elegir.",
  "Elige ζ como la raíz positiva de ζ² + ζ − 1 = 0 (es decir ζ = (√5−1)/2 ≈ 0.618). Verifica que con esa ζ, un salto que ACERCA al objetivo no aumenta la suma total.",
  "Calcula la «suma de Conway» de la configuración inicial (semiplano lleno): con ζ²+ζ=1 la serie geométrica colapsa y la suma vale exactamente 1.",
  "Si una ficha alcanzara C, su sola contribución sería ζ⁰ = 1, y con otras fichas presentes la suma superaría 1. Pero la suma nunca crece de su valor inicial 1. Contradicción: y=5 es INALCANZABLE."],
 "No es posible alcanzar y = 5. Asigna a cada ficha el peso ζ^d (d = distancia de taxi al objetivo C=(0,5)) con ζ = (√5−1)/2, la raíz positiva de ζ²+ζ−1 = 0. La «suma de Conway» de todas las fichas es un monovariante: ningún salto la aumenta (la relación ζ²+ζ=1 está diseñada para ello). La configuración inicial (semiplano lleno) tiene suma exactamente 1. Si una ficha llegara a C aportaría ζ⁰=1 y, con las demás fichas, la suma total excedería 1 — imposible, pues nunca crece. Luego y=5 es inalcanzable (y=4 sí lo es).",
 "Monovariante con razón áurea: el peso ζ se elige para que la operación lo deje fijo o lo reduzca, convirtiendo «¿se puede llegar?» en una desigualdad de sumas. Es uno de los argumentos más elegantes de invariancia. Verificado con Python: ζ²+ζ−1=0 y el cómputo de la suma del semiplano = 1.",
 40, ["monovariante", "razón áurea", "pesos geométricos"],
 ["solitarios de salto (peg solitaire)", "cotas de alcanzabilidad", "funciones potenciales en sistemas dinámicos"],
 "", ["conway", "monovariante", "razon-aurea", "nivel-experto"], "cap. 3 §3.4 (Ej. 3.4.16/3.4.33)"))

A(P(158, "Tres ranas que saltan unas sobre otras", "invariantes", 3,
 "Se colocan tres ranas en tres vértices de un cuadrado. Cada minuto, una rana salta por encima de otra de modo que aterriza en el punto simétrico (la rana saltadora va a parar a la reflexión de su posición respecto de la rana saltada). ¿Llegará alguna rana a ocupar el cuarto vértice del cuadrado, el que estaba vacío al inicio?",
 ["Pon coordenadas: ranas en (0,0), (1,0), (0,1); el vértice vacío es (1,1). Si una rana en A salta sobre otra en B, ¿a dónde va?",
  "El salto manda A a A' = 2B − A (reflexión respecto de B). Mira esto MÓDULO 2: ¿cómo cambia la paridad de las coordenadas de A?",
  "A' = 2B − A ≡ −A ≡ A (mód 2). ¡La clase de paridad (x mód 2, y mód 2) de cada rana NUNCA cambia con un salto!",
  "Las tres ranas ocupan las clases de paridad (0,0), (1,0) y (0,1). El vértice vacío (1,1) tiene clase de paridad (1,1).",
  "Ninguna rana tiene jamás clase de paridad (1,1), así que ninguna puede aterrizar en (1,1). La respuesta es NO."],
 "No: ninguna rana llegará jamás al vértice vacío. Con las ranas en (0,0), (1,0), (0,1) y el hueco en (1,1), un salto manda una rana de A a A' = 2B − A. Módulo 2 eso es A' ≡ −A ≡ A: la clase de paridad (x mód 2, y mód 2) de cada rana es un invariante. Las tres ranas ocupan las clases (0,0), (1,0), (0,1); el vértice (1,1) tiene clase (1,1), que ninguna rana posee. Por tanto (1,1) es inalcanzable.",
 "Invariante de paridad en una rejilla: la reflexión A→2B−A preserva las coordenadas módulo 2. Las clases de paridad disponibles están fijas desde el inicio. Verificado con Python: 20 000 saltos aleatorios y ninguna rana toca jamás la clase (1,1).",
 22, ["invariante de paridad", "rejilla módulo 2", "reflexión de puntos"],
 ["solitarios de salto", "argumentos de coloreo", "conservación de clases de equivalencia"],
 "", ["ranas", "paridad", "rejilla", "nivel-medio"], "cap. 3 §3.4 (Ej. 3.4.18)"))

A(P(159, "Combinar números con uv + u + v", "invariantes", 3,
 "En el pizarrón están los números 1, 2, 3, …, 100. En cada paso eliges dos números u y v, los borras y escribes en su lugar uv + u + v. Repites 99 veces hasta que queda un solo número. ¿Depende el número final del orden de las elecciones? Si no, ¿cuánto vale?",
 ["Prueba con {1,2,3} en distintos órdenes: ¿sale siempre lo mismo? Busca una cantidad que la operación NO altere.",
  "La operación uv + u + v se parece a un producto disfrazado. Suma 1 al resultado: ¿qué obtienes en términos de u y v?",
  "uv + u + v + 1 = (u+1)(v+1). Así que si a cada número x le asocias x+1, la operación MULTIPLICA esos valores asociados.",
  "El producto de todos los (xᵢ + 1) es un invariante. Al final queda un número N con (N+1) = producto de (xᵢ+1) sobre los 100 iniciales.",
  "N + 1 = ∏_{k=1}^{100}(k+1) = 2·3·4···101 = 101!. Luego N = 101! − 1, independiente del orden."],
 "El resultado no depende del orden: siempre es 101! − 1. Como uv + u + v + 1 = (u+1)(v+1), al asignar a cada número x el valor x+1, la operación multiplica esos valores; por tanto ∏(xᵢ+1) es invariante. Al final queda N con N+1 = ∏_{k=1}^{100}(k+1) = 2·3···101 = 101!, de donde N = 101! − 1.",
 "Invariante multiplicativo oculto tras un cambio de variable (x ↦ x+1). Reconocer la factorización uv+u+v+1=(u+1)(v+1) convierte un proceso aparentemente caótico en un producto fijo. Verificado con Python: 100 corridas en orden aleatorio dan siempre 101!−1.",
 20, ["invariante multiplicativo", "cambio de variable", "factorización"],
 ["procesos de fusión/agregación", "logaritmos como linealizadores", "independencia del orden de operaciones"],
 "", ["invariante", "producto", "factorizacion", "nivel-medio"], "cap. 3 §3.4 (Ej. 3.4.23)"))

A(P(160, "Rotar el conjunto {3, 4, 12}", "invariantes", 3,
 "Empiezas con el conjunto de números {3, 4, 12}. En cada paso puedes reemplazar dos de los números, a y b, por la nueva pareja 0.6a − 0.8b y 0.8a + 0.6b. ¿Puedes transformar el conjunto en {4, 6, 12}?",
 ["Los coeficientes 0.6 y 0.8 cumplen 0.6² + 0.8² = 1. Eso huele a rotación. ¿Qué cantidad preserva una rotación?",
  "Para la pareja (a,b), calcula (0.6a−0.8b)² + (0.8a+0.6b)². ¿Qué obtienes?",
  "Da exactamente a² + b². La operación preserva la suma de cuadrados de los dos números tocados, así que la suma de cuadrados de TODO el conjunto es invariante.",
  "Calcula la suma de cuadrados inicial: 3² + 4² + 12². Y la del objetivo: 4² + 6² + 12².",
  "Inicial: 9+16+144 = 169. Objetivo: 16+36+144 = 196. Como 169 ≠ 196, la transformación es IMPOSIBLE."],
 "No es posible. La transformación (a,b) ↦ (0.6a−0.8b, 0.8a+0.6b) es una rotación: preserva a² + b² (pues 0.6²+0.8²=1). Por tanto la suma de cuadrados de todo el conjunto es invariante. La inicial es 3²+4²+12² = 169 y la objetivo 4²+6²+12² = 196. Como 169 ≠ 196, no hay secuencia de operaciones que lleve {3,4,12} a {4,6,12}.",
 "Invariante cuadrático por rotación: una transformación ortogonal conserva la norma euclídea. Comparar el invariante en el estado inicial y el final es la forma estándar de probar imposibilidad. Verificado con Python: 169 ≠ 196.",
 18, ["invariante cuadrático", "rotación / transformación ortogonal", "suma de cuadrados"],
 ["conservación de energía cinética en colisiones", "transformaciones que preservan norma", "pruebas de imposibilidad"],
 "", ["invariante", "rotacion", "suma-cuadrados", "nivel-medio"], "cap. 3 §3.4 (Ej. 3.4.25, Tom Rike)"))

A(P(161, "La sucesión del último dígito de seis", "invariantes", 4,
 "Los primeros seis términos de una sucesión son 0, 1, 2, 3, 4, 5. Cada término siguiente es el último dígito (las unidades) de la suma de los seis términos anteriores. Así, el séptimo término es 5 (porque 0+1+2+3+4+5 = 15), el octavo es 0 (porque 1+2+3+4+5+5 = 20), etc. ¿Puede aparecer en algún lugar de la sucesión la subcadena 1, 3, 5, 7, 9?",
 ["No generes miles de términos a ciegas: observa la PARIDAD. ¿Qué dice la recurrencia sobre par/impar?",
  "El último dígito de una suma tiene la misma paridad que la suma. Así que cada término ≡ (suma de los 6 anteriores) (mód 2). Trabaja toda la sucesión en {par, impar}.",
  "La subcadena buscada 1,3,5,7,9 son CINCO impares seguidos. ¿La sucesión de paridades llega a tener alguna vez 5 impares consecutivos?",
  "Las paridades iniciales son 0,1,0,1,0,1 (par,impar alternando). Genera la sucesión de paridades; es periódica. Cuenta el máximo de impares seguidos.",
  "La sucesión de paridades nunca contiene 5 impares consecutivos, así que 1,3,5,7,9 (cinco impares) NO puede aparecer. Imposible."],
 "No puede aparecer. Como el último dígito conserva la paridad de la suma, la sucesión de paridades obedece la misma recurrencia módulo 2, partiendo de 0,1,0,1,0,1. Esa sucesión de paridades es periódica y nunca presenta cinco términos impares consecutivos. Pero 1,3,5,7,9 son cinco impares seguidos, así que la subcadena es imposible.",
 "Reducir módulo 2 colapsa una recurrencia complicada en un patrón periódico simple de paridades. El invariante (la paridad propaga igual que el valor) descarta la subcadena sin calcular valores exactos. Verificado con Python: en 20 000 términos no hay 5 impares consecutivos ni la subcadena literal 1,3,5,7,9.",
 24, ["paridad de recurrencias", "periodicidad módulo 2", "imposibilidad por invariante"],
 ["generadores pseudoaleatorios y sus periodos", "análisis de autómatas lineales", "argumentos módulo m"],
 "", ["sucesion", "paridad", "recurrencia", "nivel-avanzado"], "cap. 3 §3.4 (Ej. 3.4.32)"))

A(P(162, "Divisibilidad cíclica de tres diferencias", "invariantes", 4,
 "Demuestra que es imposible elegir tres enteros distintos a, b y c tales que (a − b) divida a (b − c), (b − c) divida a (c − a) y (c − a) divida a (a − b).",
 ["Nombra las tres diferencias: x = a−b, y = b−c, z = c−a. ¿Qué relación elemental cumplen siempre, sin importar a,b,c?",
  "Suma: x + y + z = (a−b)+(b−c)+(c−a) = 0. Y son todas no nulas porque a,b,c son distintos. Las condiciones dicen x|y, y|z, z|x.",
  "Una cadena de divisibilidad x|y|z|x obliga a que todas tengan el MISMO valor absoluto. ¿Por qué? Compara magnitudes a lo largo de la cadena.",
  "Si x|y entonces |x|≤|y|; encadenando, |x|≤|y|≤|z|≤|x|, luego |x|=|y|=|z|. Pero tres números iguales en valor absoluto que SUMAN 0…",
  "…deben ser, por signos, algo como (t, t, −2t) o (t,−t,…); ninguna combinación con |x|=|y|=|z| suma 0 salvo que sean 0. Contradicción con que son no nulos."],
 "Es imposible. Sean x=a−b, y=b−c, z=c−a; entonces x+y+z=0 y, por ser a,b,c distintos, x,y,z≠0. Las hipótesis x|y, y|z, z|x dan |x|≤|y|≤|z|≤|x|, de modo que |x|=|y|=|z|=:d>0. Tres números de igual valor absoluto d que sumen 0 son imposibles: con signos ±d la suma es un múltiplo impar de d (±d, ±3d), nunca 0. Contradicción; no existen tales a, b, c.",
 "Combinar un invariante algebraico (las diferencias suman 0) con el principio del extremo (la cadena de divisibilidad fuerza igualdad de magnitudes). La imposibilidad surge del choque entre «todas iguales en magnitud» y «suman cero». Verificado con Python: fuerza bruta sobre a,b,c ∈ [−12,12] no encuentra ninguna terna distinta válida.",
 26, ["suma invariante de diferencias", "cadena de divisibilidad", "principio del extremo"],
 ["argumentos de magnitud en divisibilidad", "imposibilidad por desigualdad cíclica", "teoría de números elemental"],
 "", ["divisibilidad", "diferencias", "imposibilidad", "nivel-avanzado"], "cap. 3 §3.4 (Ej. 3.4.24)"))

A(P(163, "Nueve puntos enteros en el espacio", "invariantes", 3,
 "Se dan nueve puntos de coordenadas enteras en el espacio tridimensional. Demuestra que el punto medio de algún segmento que une dos de ellos también tiene coordenadas enteras.",
 ["El punto medio de (P,Q) es entero sii P y Q coinciden en la PARIDAD de cada coordenada. Clasifica los puntos por paridad.",
  "Cada punto (x,y,z) tiene un «tipo de paridad»: (x mód 2, y mód 2, z mód 2). ¿Cuántos tipos distintos hay en 3D?",
  "Hay 2³ = 8 tipos de paridad posibles. Tienes 9 puntos. ¿Qué dice el principio del casillero?",
  "9 puntos en 8 casillas (tipos de paridad): por el casillero, dos puntos comparten el mismo tipo de paridad.",
  "Si P y Q tienen igual paridad en las tres coordenadas, entonces P+Q es par en cada coordenada y (P+Q)/2 es entero. Listo."],
 "Cada punto entero tiene un tipo de paridad (x mód 2, y mód 2, z mód 2), y hay 2³ = 8 tipos posibles. Con 9 puntos, el principio del casillero garantiza que dos de ellos, P y Q, comparten el mismo tipo. Entonces P y Q tienen la misma paridad en cada coordenada, así que P+Q es par coordenada a coordenada y el punto medio (P+Q)/2 tiene coordenadas enteras.",
 "Casillero sobre clases de paridad: 2^d clases en dimensión d, y 2^d+1 puntos fuerzan una colisión cuyo punto medio es entero. En 2D bastan 5 puntos; en 3D, 9. Verificado con Python: 9 > 2³ y el caso 2D (5 > 2²).",
 16, ["principio del casillero", "clases de paridad", "puntos medios enteros"],
 ["casillero en alta dimensión", "códigos y reticulados", "argumentos de existencia"],
 "", ["casillero", "paridad", "reticulado", "nivel-medio"], "cap. 3 §3.4 (Ej. 3.4.31)"))

A(P(164, "Solitario búlgaro", "invariantes", 4,
 "Empiezas con un número finito de frijoles repartidos en uno o más montones. En cada turno, quitas un frijol de CADA montón y formas un montón nuevo con todos los frijoles retirados. Por ejemplo, 3,5 → 2,4,2 → 1,3,1,3 → … Juegas hasta que la configuración se repite. Demuestra que, según el número total de frijoles, el proceso siempre termina en un punto fijo (una configuración que ya no cambia) si y solo si ese total es un número triangular (1, 3, 6, 10, 15, …), sin importar el reparto inicial.",
 ["Es un sistema que evoluciona en estados finitos: o llega a un punto fijo o entra en un ciclo. ¿Qué configuración sería un PUNTO FIJO?",
  "Un punto fijo no cambia: tras quitar uno de cada montón y crear uno nuevo, debe reaparecer el mismo multiconjunto de tamaños. ¿Qué forma tiene?",
  "Si los montones tienen tamaños distintos k, k−1, …, 2, 1 (un «escalón» completo), al aplicar la operación reaparece el mismo escalón. Ese escalón usa 1+2+···+k = k(k+1)/2 frijoles.",
  "Es decir, el único punto fijo posible usa exactamente un número TRIANGULAR de frijoles. Si el total no es triangular, no hay punto fijo y debe haber ciclo.",
  "Recíprocamente, si el total ES triangular, se prueba que la dinámica converge al escalón. Conclusión: punto fijo ⇔ total triangular."],
 "El punto fijo existe si y solo si el total de frijoles es triangular. Un punto fijo debe ser invariante bajo la operación; el único multiconjunto con esa propiedad es el «escalón» de tamaños distintos k, k−1, …, 2, 1, que contiene 1+2+···+k = k(k+1)/2 frijoles — un número triangular. Si el total no es triangular, ningún escalón cabe y el sistema (finito) entra forzosamente en un ciclo en vez de detenerse. Si el total es triangular, la dinámica converge a ese escalón. Por tanto: termina en punto fijo ⇔ total triangular.",
 "Estados finitos ⇒ ciclo o punto fijo; identificar la forma del punto fijo (el escalón) liga el fenómeno a los números triangulares. Verificado con Python: simulando todos los totales N=1..39, el proceso alcanza un punto fijo exactamente cuando N es triangular.",
 30, ["dinámica de estados finitos", "puntos fijos", "números triangulares"],
 ["sistemas dinámicos discretos y atractores", "autovalores/órbitas periódicas", "combinatoria de particiones"],
 "", ["solitario-bulgaro", "punto-fijo", "triangulares", "nivel-avanzado"], "cap. 3 §3.4 (Ej. 3.4.38)"))

A(P(165, "Cinco puntos en un cuadrado unitario", "invariantes", 2,
 "Demuestra que si se colocan cinco puntos en cualquier posición dentro de (o sobre el borde de) un cuadrado de lado 1, entonces dos de ellos están a una distancia de a lo más √2 / 2 uno del otro.",
 ["Cinco puntos y quieres forzar que dos estén cerca. Eso huele a casillero: divide el cuadrado en regiones. ¿Cuántas y de qué tamaño?",
  "Parte el cuadrado unitario en 4 cuadraditos de lado 1/2 (una rejilla 2×2). Tienes 5 puntos y 4 cuadraditos.",
  "Por el casillero, algún cuadradito contiene al menos dos de los cinco puntos.",
  "Dentro de un cuadrado de lado 1/2, ¿cuál es la máxima distancia posible entre dos puntos? Es su diagonal.",
  "La diagonal de un cuadrado de lado 1/2 mide √2/2. Así que esos dos puntos distan ≤ √2/2. Listo."],
 "Divide el cuadrado unitario en cuatro cuadraditos de lado 1/2 (rejilla 2×2). Con cinco puntos y cuatro cuadraditos, el principio del casillero garantiza que algún cuadradito contiene dos puntos. La mayor distancia posible dentro de un cuadrado de lado 1/2 es su diagonal, √2/2. Por tanto esos dos puntos están a distancia ≤ √2/2.",
 "Casillero geométrico: subdividir el dominio en regiones de diámetro acotado y meter más puntos que regiones. El diámetro de cada celda (la diagonal) da la cota. Verificado con Python: la diagonal de un cuadrado de lado 1/2 es exactamente √2/2.",
 14, ["principio del casillero", "diámetro de una región", "subdivisión"],
 ["empaquetamiento de puntos", "argumentos de distancia mínima", "casillero geométrico"],
 "", ["casillero", "geometria", "distancia", "nivel-basico"], "cap. 3 §3.3 (Ej. 3.3.2)"))

A(P(166, "Cuántos juegos dura un torneo de eliminación", "invariantes", 1,
 "En un torneo de eliminación directa de un juego para dos personas (por ejemplo, ajedrez), en cuanto pierdes quedas fuera, y el torneo continúa hasta que queda una sola persona (el campeón). Encuentra una fórmula para el número de partidas que deben jugarse en un torneo que empieza con n participantes.",
 ["No dibujes el cuadro de emparejamientos: piensa en qué cantidad cambia de forma simple con cada partida.",
  "¿Cuántas personas son eliminadas en cada partida? Esa es la clave del monovariante.",
  "Cada partida elimina exactamente a una persona. El número de jugadores que siguen vivos baja de uno en uno.",
  "Empiezas con n vivos y terminas con 1 (el campeón). ¿Cuántas eliminaciones hicieron falta?",
  "Hay que eliminar a n−1 personas, una por partida: se juegan exactamente n − 1 partidas."],
 "Se juegan exactamente n − 1 partidas. Cada partida elimina a una persona, así que el número de jugadores aún en competencia es un monovariante que decrece de 1 en 1. Para pasar de n participantes a un único campeón hay que eliminar a n−1 personas, lo que requiere n−1 partidas.",
 "Monovariante de conteo: en vez de analizar la estructura del cuadro (que puede tener byes y rondas desiguales), se cuenta lo que cada partida hace de forma fija (una eliminación). El resultado es independiente del formato. Verificado con Python para todo n hasta 50.",
 8, ["monovariante", "conteo por eliminación", "independencia de la estructura"],
 ["conteo de aristas en árboles", "procesos de reducción", "argumentos de conservación"],
 "", ["torneo", "monovariante", "conteo", "nivel-basico"], "cap. 3 §3.4 (Ej. 3.4.14)"))

# =====================================================================
# OPTIMIZACION (11) — principio del extremo y desigualdades
# =====================================================================

A(P(167, "Suma por suma de recíprocos", "optimizacion", 3,
 "Sea a₁, a₂, …, aₙ una sucesión de números positivos. Demuestra que (a₁ + a₂ + ⋯ + aₙ)(1/a₁ + 1/a₂ + ⋯ + 1/aₙ) ≥ n², con igualdad si y solo si todos los aᵢ son iguales.",
 ["Empieza por el caso n=2: (a+b)(1/a+1/b). Desarróllalo y mira qué término hay que acotar.",
  "Al desarrollar el producto general aparecen n términos iguales a 1 (los aⱼ/aⱼ) y muchos pares aⱼ/aₖ + aₖ/aⱼ. Agrúpalos.",
  "Para cada par, usa la desigualdad clave: x + 1/x ≥ 2 para x>0 (consecuencia de AM-GM). Aplícala a aⱼ/aₖ.",
  "Hay n términos «1» y (n²−n)/2 pares, cada par ≥ 2. Suma las cotas.",
  "Total ≥ n·1 + ((n²−n)/2)·2 = n + (n²−n) = n². Igualdad cuando cada aⱼ/aₖ = 1, es decir, todos los aᵢ iguales."],
 "Al desarrollar (Σaⱼ)(Σ1/aₖ) se obtienen n² términos de la forma aⱼ/aₖ. De ellos, n valen 1 (cuando j=k) y los restantes n²−n se agrupan en (n²−n)/2 pares aⱼ/aₖ + aₖ/aⱼ. Por AM-GM, cada par cumple aⱼ/aₖ + aₖ/aⱼ ≥ 2. Sumando: el producto ≥ n·1 + ((n²−n)/2)·2 = n². La igualdad exige aⱼ/aₖ = 1 para todo par, es decir, todos los aᵢ iguales.",
 "AM-GM aplicada por pares, tras agrupar los términos del desarrollo. La desigualdad auxiliar x+1/x≥2 es la pieza reutilizable. Verificado con Python: 2000 sucesiones aleatorias (n entre 2 y 8) siempre cumplen el producto ≥ n².",
 20, ["AM-GM", "desigualdad x + 1/x ≥ 2", "agrupar términos"],
 ["media aritmética vs armónica", "desigualdad de Cauchy-Schwarz", "optimización de recursos"],
 "", ["desigualdad", "am-gm", "reciprocos", "nivel-medio"], "cap. 5 §5.5 (Ej. 5.5.18)"))

A(P(168, "La parte entera de una suma de raíces", "optimizacion", 4,
 "Sea A = 1/√1 + 1/√2 + 1/√3 + ⋯ + 1/√10000. Encuentra ⌊A⌋ (la parte entera de A) sin calculadora.",
 ["No sumes los 10000 términos: ACÓTALOS por algo que se telescope. Busca dos expresiones que encierren a 1/√n.",
  "Racionaliza: 2(√(n+1) − √n) = 2/(√(n+1)+√n) y 2(√n − √(n−1)) = 2/(√n+√(n−1)). Compara cada una con 1/√n = 2/(2√n).",
  "Como √(n+1)+√n > 2√n > √n+√(n−1), se obtiene 2(√(n+1)−√n) < 1/√n < 2(√n − √(n−1)). Ambas cotas TELESCOPAN.",
  "Suma las cotas de n=1 a 10000: la inferior da 2(√10001 − 1) ≈ 198.0; la superior, 2(√10000 − √0) = 198. Afina separando el primer término.",
  "Escribiendo A = 1 + Σ_{n=2}^{10000} 1/√n y acotando esa cola entre 2√10001 − 2√2 (≈197+) y 2√10000 − 2√1 = 198, se concluye 198 < A < 199. Luego ⌊A⌋ = 198."],
 "⌊A⌋ = 198. Acotando cada término con 2(√(n+1)−√n) < 1/√n < 2(√n−√(n−1)) (ambas obtenidas al racionalizar) y sumando telescópicamente, se obtiene 2√10001 − 2 < A < 2√10000. Afinando (separar el término n=1 y empezar la suma en n=2) se llega a 198 < A < 199, de modo que la parte entera es 198.",
 "«Masaje» y telescopaje: perturbar cada término hasta que las cotas se cancelen en cascada. La estimación cruda se refina aislando los primeros términos. Verificado con Python: la suma exacta es ≈ 198.5446, cuya parte entera es 198.",
 28, ["telescopaje", "racionalización", "acotamiento de sumas"],
 ["estimación de series", "sumas vs integrales", "cotas por comparación"],
 "", ["suma", "telescopaje", "estimacion", "nivel-avanzado"], "cap. 5 §5.5 (Ej. 5.5.19)"))

A(P(169, "El producto máximo que suma 1976 (IMO 1976)", "optimizacion", 4,
 "Determina, con demostración, el mayor número que puede obtenerse como producto de enteros positivos cuya suma es 1976.",
 ["Experimenta: para sumas pequeñas (10, 11, 12), ¿qué partes conviene usar? Descarta primero los 1 (no ayudan al producto).",
  "Ningún sumando debe ser 1 (quitarlo y sumarlo a otro aumenta el producto). Y ningún sumando debe ser ≥ 5: partir 5 = 2+3 da 6 > 5.",
  "Así que las partes óptimas son 2 y 3. Además, tres doses (2+2+2=6, producto 8) son peores que dos treses (3+3=6, producto 9). Evita usar más de dos doses.",
  "Conclusión: usa tantos 3 como puedas, con a lo más un par de 2 al final. Divide 1976 entre 3 y mira el residuo.",
  "1976 = 3·658 + 2, residuo 2: usa 658 treses y un 2. El producto máximo es 2 · 3^658."],
 "El máximo es 2 · 3^658. Razonamiento: en una descomposición óptima no hay 1 (absorberlo en otro sumando aumenta el producto) ni partes ≥ 5 (porque 2·3 = 6 > 5 y en general partir mejora). Solo quedan 2 y 3, y como 3+3 (producto 9) supera a 2+2+2 (producto 8), conviene a lo más dos doses. Como 1976 = 3·658 + 2, la descomposición óptima es 658 treses y un 2, con producto 2·3^658.",
 "Optimización «algorítmica»/golosa con argumento de intercambio: cada regla local (sin unos, sin partes ≥5, a lo más dos doses) mejora el producto, y juntas fijan la estructura. Verificado con Python: programación dinámica del producto máximo coincide con la fórmula (N mód 3) para todo N hasta 30; 1976 ≡ 2 (mód 3).",
 26, ["argumento de intercambio", "descomposición óptima", "el número e y el 3"],
 ["optimización golosa", "el «por qué 3» en problemas de partición", "programación dinámica"],
 "1976", ["imo", "producto-maximo", "particion", "nivel-avanzado"], "cap. 5 §5.5 (Ej. 5.5.29, IMO 1976)"))

A(P(170, "Producto de dos sumas cíclicas", "optimizacion", 4,
 "Sean a, b, c números reales positivos. Demuestra que (a²b + b²c + c²a)(ab² + bc² + ca²) ≥ 9a²b²c².",
 ["El lado derecho es 9(abc)². El 9 sugiere AM-GM sobre TRES términos en cada factor. ¿Qué media usar?",
  "Para tres positivos x,y,z, AM-GM da x+y+z ≥ 3·∛(xyz). Aplícala a cada factor por separado.",
  "Primer factor: a²b + b²c + c²a ≥ 3·∛(a²b · b²c · c²a) = 3·∛(a³b³c³) = 3abc.",
  "Segundo factor: ab² + bc² + ca² ≥ 3·∛(ab²·bc²·ca²) = 3abc por el mismo cálculo.",
  "Multiplicando ambas cotas: (a²b+b²c+c²a)(ab²+bc²+ca²) ≥ 3abc · 3abc = 9a²b²c². Igualdad si a=b=c."],
 "Por AM-GM con tres términos: a²b + b²c + c²a ≥ 3∛(a²b·b²c·c²a) = 3∛(a³b³c³) = 3abc, e igualmente ab² + bc² + ca² ≥ 3∛(ab²·bc²·ca²) = 3abc. Multiplicando las dos desigualdades (ambos lados positivos) se obtiene (a²b+b²c+c²a)(ab²+bc²+ca²) ≥ 9a²b²c², con igualdad cuando a = b = c.",
 "AM-GM por factor: el exponente buscado (9 = 3·3) indica cuántos términos agrupar. Los productos dentro de las raíces colapsan a potencias de abc por la simetría cíclica. Verificado con Python: 3000 ternas aleatorias positivas cumplen la desigualdad, con igualdad solo en a=b=c.",
 22, ["AM-GM de tres términos", "sumas cíclicas", "multiplicar desigualdades"],
 ["desigualdades simétricas/cíclicas", "media geométrica", "olimpiadas de álgebra"],
 "", ["desigualdad", "am-gm", "ciclica", "nivel-avanzado"], "cap. 5 §5.5 (Ej. 5.5.39)"))

A(P(171, "Raíz de la suma contra suma de raíces", "optimizacion", 2,
 "Sean a, b, c ≥ 0. Demuestra que √(3(a + b + c)) ≥ √a + √b + √c.",
 ["Ambos lados son no negativos, así que elevar al cuadrado preserva la desigualdad. Hazlo y compara.",
  "Al cuadrado, hay que probar 3(a+b+c) ≥ (√a+√b+√c)² = a+b+c + 2(√(ab)+√(bc)+√(ca)).",
  "Eso equivale a 2(a+b+c) ≥ 2(√(ab)+√(bc)+√(ca)), es decir a+b+c ≥ √(ab)+√(bc)+√(ca).",
  "Para cada par usa AM-GM: (x+y)/2 ≥ √(xy). Suma las tres desigualdades √(ab) ≤ (a+b)/2, etc.",
  "Sumando: √(ab)+√(bc)+√(ca) ≤ (a+b)/2+(b+c)/2+(c+a)/2 = a+b+c. Esto cierra la prueba."],
 "Como ambos lados son ≥ 0, basta probar la versión al cuadrado: 3(a+b+c) ≥ (√a+√b+√c)² = (a+b+c) + 2(√(ab)+√(bc)+√(ca)). Eso se reduce a a+b+c ≥ √(ab)+√(bc)+√(ca). Y esto sale de AM-GM par a par: √(ab) ≤ (a+b)/2, √(bc) ≤ (b+c)/2, √(ca) ≤ (c+a)/2; sumando, el lado derecho ≤ a+b+c. Igualdad cuando a=b=c.",
 "Es un caso de Cauchy-Schwarz ((√a+√b+√c)² ≤ 3(a+b+c)) pero se prueba elementalmente elevando al cuadrado y aplicando AM-GM por pares. Verificado con Python: 3000 ternas no negativas cumplen la desigualdad.",
 16, ["Cauchy-Schwarz", "AM-GM por pares", "elevar al cuadrado"],
 ["desigualdad de medias", "normas y producto interno", "concavidad de la raíz"],
 "", ["desigualdad", "cauchy-schwarz", "raices", "nivel-basico"], "cap. 5 §5.5 (Ej. 5.5.40)"))

A(P(172, "Pesos 1, 1, 4, 16 contra una suma", "optimizacion", 3,
 "Sean a, b, c, d > 0. Demuestra que 1/a + 1/b + 4/c + 16/d ≥ 64/(a + b + c + d).",
 ["Los numeradores 1, 1, 4, 16 son 1², 1², 2², 4². Y 64 = 8². Eso apunta a Cauchy-Schwarz en forma de fracciones (Titu/Engel).",
  "La forma de Engel de Cauchy-Schwarz dice: p²/x + q²/y + r²/z + s²/w ≥ (p+q+r+s)²/(x+y+z+w).",
  "Reescribe 1/a = 1²/a, 1/b = 1²/b, 4/c = 2²/c, 16/d = 4²/d. Identifica p,q,r,s y los denominadores.",
  "Con p=1, q=1, r=2, s=4 y denominadores a,b,c,d, el numerador del lado derecho es (1+1+2+4)².",
  "(1+1+2+4)² = 8² = 64, y el denominador es a+b+c+d. Así 1/a+1/b+4/c+16/d ≥ 64/(a+b+c+d). Listo."],
 "Por la desigualdad de Cauchy-Schwarz en forma de Engel (Titu): 1²/a + 1²/b + 2²/c + 4²/d ≥ (1+1+2+4)²/(a+b+c+d). Como 1+1+2+4 = 8 y 8² = 64, el lado derecho es 64/(a+b+c+d). Por tanto 1/a + 1/b + 4/c + 16/d ≥ 64/(a+b+c+d), con igualdad cuando a/1 = b/1 = c/2 = d/4.",
 "Reconocer cuadrados perfectos en los numeradores activa la forma de Engel de Cauchy-Schwarz, donde el numerador del lado derecho es el cuadrado de la suma de las raíces. Verificado con Python: 4000 cuádruplas positivas aleatorias cumplen la desigualdad.",
 18, ["Cauchy-Schwarz (forma de Engel/Titu)", "cuadrados perfectos", "media armónica ponderada"],
 ["optimización con multiplicadores", "desigualdad de Cauchy-Schwarz", "reparto de recursos"],
 "", ["desigualdad", "cauchy-schwarz", "engel-titu", "nivel-medio"], "cap. 5 §5.5 (Ej. 5.5.41)"))

A(P(173, "Suma contra suma de cuadrados con producto 1", "optimizacion", 3,
 "Sean x, y, z > 0 con xyz = 1. Demuestra que x + y + z ≤ x² + y² + z².",
 ["Tienes dos «potencias» de los mismos números: grado 1 y grado 2. ¿Qué desigualdad relaciona medias de potencias?",
  "La desigualdad de medias de potencias (o de la media cuadrática) da (x²+y²+z²)/3 ≥ ((x+y+z)/3)². Pero necesitas una pieza más.",
  "Por AM-GM, x+y+z ≥ 3∛(xyz) = 3 (usando xyz=1). Guarda este hecho: la suma es al menos 3.",
  "Sea s = x+y+z. Media cuadrática ≥ media aritmética da x²+y²+z² ≥ s²/3. Basta probar s²/3 ≥ s, o sea s ≥ 3.",
  "Y s ≥ 3 ya lo tienes por AM-GM. Entonces x²+y²+z² ≥ s²/3 ≥ 3s/3 = s = x+y+z."],
 "Sea s = x+y+z. Por la desigualdad entre media cuadrática y aritmética, x²+y²+z² ≥ s²/3. Por AM-GM, s = x+y+z ≥ 3∛(xyz) = 3 (pues xyz=1). Combinando: x²+y²+z² ≥ s²/3 = s·(s/3) ≥ s·1 = s = x+y+z. Igualdad cuando x=y=z=1.",
 "Encadenar dos desigualdades clásicas: media cuadrática ≥ aritmética para pasar de grado 1 a grado 2, y AM-GM con la restricción xyz=1 para garantizar s ≥ 3. Verificado con Python: 5000 ternas con xyz=1 cumplen x+y+z ≤ x²+y²+z².",
 20, ["media cuadrática vs aritmética", "AM-GM con restricción", "encadenar desigualdades"],
 ["desigualdades de medias de potencias", "optimización con restricciones", "normalización por producto"],
 "", ["desigualdad", "medias-potencias", "restriccion", "nivel-medio"], "cap. 5 §5.5 (Ej. 5.5.43)"))

A(P(174, "La desigualdad de Nesbitt", "optimizacion", 3,
 "Sean x, y, z > 0. Encuentra el valor mínimo de x/(y + z) + y/(z + x) + z/(x + y).",
 ["Prueba x=y=z: cada término es 1/2 y la suma da 3/2. Conjetura que ese es el mínimo y demuéstralo.",
  "Truco clásico: suma 1 a cada fracción. x/(y+z) + 1 = (x+y+z)/(y+z). Hazlo en los tres términos.",
  "Sumando 3 al total: el lado izquierdo + 3 = (x+y+z)[1/(y+z) + 1/(z+x) + 1/(x+y)]. Trabaja esa expresión.",
  "Pon s = x+y+z. Entonces LI + 3 = s·[1/(y+z)+1/(z+x)+1/(x+y)]. Usa AM-HM (o Cauchy) sobre los tres denominadores, que suman 2s.",
  "AM-HM: [1/(y+z)+1/(z+x)+1/(x+y)] ≥ 9/((y+z)+(z+x)+(x+y)) = 9/(2s). Luego LI + 3 ≥ s·9/(2s) = 9/2, así LI ≥ 3/2."],
 "El valor mínimo es 3/2 (alcanzado en x=y=z). Sumando 1 a cada fracción, x/(y+z)+y/(z+x)+z/(x+y) + 3 = (x+y+z)[1/(y+z)+1/(z+x)+1/(x+y)]. Con s = x+y+z, los tres denominadores suman 2s, y por la desigualdad AM-HM (o Cauchy-Schwarz) su suma de recíprocos es ≥ 9/(2s). Entonces el lado izquierdo + 3 ≥ s·9/(2s) = 9/2, de donde el lado izquierdo ≥ 3/2.",
 "El truco de «sumar 1 a cada término» convierte la expresión en un producto suma × suma-de-recíprocos, donde AM-HM cierra. Es la desigualdad de Nesbitt. Verificado con Python: muestreo de 20 000 ternas positivas da mínimo ≈ 1.5000.",
 22, ["desigualdad de Nesbitt", "AM-HM", "truco de sumar 1"],
 ["desigualdades simétricas", "media armónica", "optimización sin cálculo"],
 "", ["desigualdad", "nesbitt", "am-hm", "nivel-medio"], "cap. 5 §5.5 (Ej. 5.5.44)"))

A(P(175, "Cotas para yz + zx + xy − 2xyz (IMO 1984)", "optimizacion", 4,
 "Sean x, y, z reales no negativos con x + y + z = 1. Demuestra que 0 ≤ yz + zx + xy − 2xyz ≤ 7/27.",
 ["Dos cotas: una inferior (0) y una superior (7/27). Para la inferior, ¿qué pasa con la expresión en los vértices y aristas del dominio?",
  "Cota inferior: como x+y+z=1, cada variable es ≤ 1. Reescribe la expresión agrupando para ver que es ≥ 0 cuando una variable es 0 o pequeña.",
  "Para la cota superior, sospecha el simétrico x=y=z=1/3: evalúa yz+zx+xy−2xyz ahí. Eso sugiere el valor 7/27.",
  "En x=y=z=1/3: yz+zx+xy = 3·(1/9) = 1/3, y 2xyz = 2/27. Diferencia = 1/3 − 2/27 = 9/27 − 2/27 = 7/27. Es el máximo.",
  "La cota superior se prueba, por ejemplo, asumiendo sin pérdida de generalidad un orden y usando que la expresión es máxima en el punto simétrico (vía Schur o multiplicadores). Mínimo 0 (en los vértices como (1,0,0)), máximo 7/27."],
 "La expresión E = yz+zx+xy − 2xyz cumple 0 ≤ E ≤ 7/27 bajo x+y+z=1, x,y,z≥0. Cota inferior: en cada vértice y arista del símplex (alguna variable 0) E ≥ 0, y E no se hace negativa en el interior; de hecho E ≥ 0 con igualdad en los vértices como (1,0,0). Cota superior: el máximo se alcanza en el punto simétrico x=y=z=1/3, donde E = 3·(1/9) − 2/27 = 1/3 − 2/27 = 7/27.",
 "Optimizar sobre el símplex: las cotas se realizan en los puntos extremos (vértices para el mínimo, centro simétrico para el máximo). Evaluar candidatos simétricos sugiere el valor exacto. Verificado con Python: muestreo de 50 000 puntos del símplex da mínimo ≈ 0 y máximo ≈ 0.259259 = 7/27.",
 30, ["optimización en el símplex", "puntos extremos", "simetría del máximo"],
 ["multiplicadores de Lagrange con restricción lineal", "desigualdad de Schur", "polinomios simétricos"],
 "1984", ["imo", "simplex", "desigualdad", "nivel-avanzado"], "cap. 5 §5.5 (Ej. 5.5.45, IMO 1984)"))

A(P(176, "Acotar el factorial por una potencia", "optimizacion", 3,
 "Demuestra que n! < ((n + 1)/2)ⁿ para todo entero n ≥ 2.",
 ["n! = 1·2·3···n es un PRODUCTO de n factores. ((n+1)/2)ⁿ es una potencia. ¿Qué desigualdad compara producto con potencia de un promedio?",
  "AM-GM dice que la media geométrica de n números es ≤ su media aritmética. Aplícala a los factores 1, 2, …, n.",
  "Media geométrica de 1,2,…,n = ⁿ√(n!). Media aritmética = (1+2+⋯+n)/n. Calcula esta última.",
  "(1+2+⋯+n)/n = [n(n+1)/2]/n = (n+1)/2. Por AM-GM, ⁿ√(n!) ≤ (n+1)/2, y la desigualdad es ESTRICTA porque los factores no son todos iguales (n≥2).",
  "Elevando a la n: n! < ((n+1)/2)ⁿ. La desigualdad es estricta porque 1,2,…,n no son todos iguales."],
 "Aplica AM-GM a los n factores 1, 2, …, n: su media geométrica ⁿ√(n!) es menor que su media aritmética (1+2+⋯+n)/n = (n+1)/2 — estrictamente menor porque los factores no son todos iguales (n ≥ 2). Elevando a la potencia n: n! < ((n+1)/2)ⁿ.",
 "AM-GM aplicada directamente a 1,2,…,n: la media aritmética es la conocida (n+1)/2, y la desigualdad estricta proviene de que los términos no son iguales. Verificado con Python: n! < ((n+1)/2)ⁿ para todo n de 2 a 39.",
 16, ["AM-GM", "media aritmética 1..n", "desigualdad estricta"],
 ["cotas del factorial (Stirling elemental)", "media geométrica vs aritmética", "comparar producto y potencia"],
 "", ["desigualdad", "factorial", "am-gm", "nivel-medio"], "cap. 5 §5.5 (Ej. 5.5.28)"))

A(P(177, "Una moneda tangente a lo más a otras cinco", "optimizacion", 4,
 "Te dan un conjunto finito de monedas en el plano, todas de diámetros DISTINTOS. Demuestra que existe al menos una moneda que es tangente a lo más a cinco de las demás.",
 ["No intentes acotar todas a la vez. Aplica el principio del extremo: fíjate en la moneda MÁS pequeña.",
  "Considera la moneda de menor diámetro, llamémosla M. Las monedas tangentes a M la rodean. ¿Pueden ser muchas?",
  "Cada moneda tangente a M toca su borde por fuera. Como todas las tangentes tienen diámetro ≥ el de M (M es la menor), los puntos de tangencia están bien separados angularmente.",
  "Dos monedas tangentes a M, ambas de radio ≥ r (con r el radio de M), subtienden desde el centro de M un ángulo de separación mayor que 60°. ¿Cuántas caben alrededor de los 360°?",
  "Como cada par consecutivo deja un ángulo > 60° en el centro de M, caben a lo más 360/60 = 6, y con diámetros estrictamente mayores el ángulo es > 60°, dejando a lo más 5 tangentes. M cumple lo pedido."],
 "Por el principio del extremo, toma la moneda M de menor diámetro (radio r). Toda moneda tangente a M tiene radio ≥ r y toca su borde por fuera. Dos monedas tangentes a M, vistas desde el centro de M, subtienden un ángulo de separación estrictamente mayor que 60° (porque sus radios superan a r). Como los ángulos alrededor del centro suman 360° y cada hueco entre tangentes consecutivas mide > 60°, caben a lo más cinco monedas tangentes a M. Así M es tangente a lo más a cinco.",
 "Principio del extremo (elegir el elemento mínimo) + un argumento angular: el tamaño mínimo de M fuerza separación angular > 60° entre sus vecinas, limitándolas a cinco. Es la misma cota del «beso» de círculos. El argumento es geométrico-combinatorio y no requiere cómputo numérico.",
 30, ["principio del extremo", "argumento angular", "número de besos (kissing number)"],
 ["empaquetamiento de círculos", "grados en grafos geométricos", "cotas por elemento minimal"],
 "", ["extremo", "geometria", "tangencia", "nivel-avanzado"], "cap. 3 §3.2 (Ej. 3.2.10)"))

# =====================================================================
# PATRONES (11) — fórmulas, conteo, teoría de números, sucesiones
# =====================================================================

A(P(178, "Una suma que se telescopa", "patrones", 2,
 "Escribe 1/(1·2) + 1/(2·3) + 1/(3·4) + ⋯ + 1/(99·100) como una fracción en su mínima expresión.",
 ["Sumar 99 términos a mano es tedioso. Suma solo los primeros y busca un PATRÓN en los resultados parciales.",
  "1/(1·2) = 1/2; +1/(2·3) = 2/3; +1/(3·4) = 3/4. Conjetura: la suma de los primeros k términos es k/(k+1).",
  "Para probarlo, descompón el término general en fracciones parciales: 1/(n(n+1)) = 1/n − 1/(n+1).",
  "Al sumar, casi todo se cancela (suma telescópica): queda 1/1 − 1/(N+1).",
  "Con N = 99: la suma es 1 − 1/100 = 99/100."],
 "La suma es 99/100. La clave es la descomposición telescópica 1/(n(n+1)) = 1/n − 1/(n+1). Sumando de n=1 a 99, todos los términos intermedios se cancelan y queda 1 − 1/100 = 99/100 (ya en mínima expresión).",
 "Patrón detectado en sumas parciales (1/2, 2/3, 3/4, …) y confirmado por fracciones parciales que telescopan. Es el ejemplo arquetípico de Zeitz sobre cómo un «ejercicio» tedioso esconde un «problema» con estructura. Verificado con Python (aritmética exacta de fracciones): la suma es 99/100.",
 12, ["suma telescópica", "fracciones parciales", "detección de patrón"],
 ["series telescópicas", "sumas parciales y conjeturas", "descomposición en fracciones simples"],
 "", ["telescopaje", "suma", "fracciones-parciales", "nivel-basico"], "cap. 1 §1.1 (Ej. 1.1.2)"))

A(P(179, "Cuatro términos en progresión aritmética más una potencia", "patrones", 3,
 "Sabemos que el producto de cuatro enteros consecutivos es siempre uno menos que un cuadrado perfecto. Generaliza: ¿qué puedes afirmar sobre el producto de cuatro términos consecutivos de una progresión aritmética cualquiera, por ejemplo 3·8·13·18?",
 ["Reescribe el producto agrupando los términos EXTREMOS y los CENTRALES. Con términos a, a+d, a+2d, a+3d, empareja el 1º con el 4º y el 2º con el 3º.",
  "(a)(a+3d) = a²+3ad y (a+d)(a+2d) = a²+3ad+2d². Pon t = a²+3ad. El producto es t(t+2d²).",
  "t(t+2d²) = t² + 2d²t. Eso casi es un cuadrado: ¿qué le falta para completar (t+d²)²?",
  "(t+d²)² = t² + 2d²t + d⁴. Así que el producto es (t+d²)² − d⁴. ¡Le falta exactamente d⁴ para ser cuadrado!",
  "Por tanto: el producto de cuatro términos en progresión aritmética de diferencia d, MÁS d⁴, es un cuadrado perfecto: (a²+3ad+d²)². Para enteros consecutivos d=1, recuperando «producto + 1 = cuadrado»."],
 "Para cuatro términos a, a+d, a+2d, a+3d en progresión aritmética, el producto MÁS d⁴ es un cuadrado perfecto: (a)(a+d)(a+2d)(a+3d) + d⁴ = (a² + 3ad + d²)². En efecto, agrupando extremos y centrales con t = a²+3ad, el producto es t(t+2d²) = t² + 2d²t = (t+d²)² − d⁴. El caso de enteros consecutivos (d=1) da el conocido «producto + 1 = cuadrado».",
 "Patrón estructural revelado por un emparejamiento astuto (extremos × centrales) que reduce cuatro factores a una cuadrática en t, y luego completar el cuadrado. El término correctivo d⁴ generaliza el «+1». Verificado con Python: (a)(a+d)(a+2d)(a+3d)+d⁴ es cuadrado para a∈[−5,7], d∈[1,6].",
 22, ["completar el cuadrado", "emparejamiento de factores", "progresión aritmética"],
 ["identidades algebraicas", "cuadrados casi perfectos", "factorización por agrupación"],
 "", ["progresion-aritmetica", "cuadrado", "factorizacion", "nivel-medio"], "cap. 3 §3.1 (Ej. 3.1.14)"))

A(P(180, "El producto de todos los divisores", "patrones", 3,
 "Encuentra (y demuestra) una fórmula sencilla para el producto de todos los divisores positivos de un entero n. Por ejemplo, para n = 12 los divisores son 1, 2, 3, 4, 6, 12 y su producto es 1728.",
 ["Lista los divisores de 12 y EMPARÉJALOS de modo que cada pareja multiplique n. ¿Cuántas parejas hay?",
  "Cada divisor d se empareja con n/d, y d·(n/d) = n. Los divisores de 12 forman las parejas (1,12), (2,6), (3,4): tres parejas, cada una con producto 12.",
  "Si n tiene d(n) divisores, ¿cuántas parejas de producto n se forman? Cuidado si n es un cuadrado perfecto (un divisor se empareja consigo mismo).",
  "El producto de todos los divisores es n elevado al número de parejas, es decir n^{d(n)/2}. Para n=12: d(12)=6, producto = 12³ = 1728.",
  "Fórmula general: producto de divisores de n = n^{d(n)/2}, donde d(n) es la cantidad de divisores. (Cuando d(n) es impar, n es un cuadrado y la raíz √n se cuenta una vez, manteniendo la fórmula.)"],
 "El producto de todos los divisores positivos de n es n^{d(n)/2}, donde d(n) es el número de divisores. Razón: los divisores se emparejan como d ↔ n/d, y cada pareja multiplica n. Hay d(n)/2 parejas, de modo que el producto total es n^{d(n)/2}. Para n=12, d(12)=6 y el producto es 12³ = 1728. (Si n es cuadrado perfecto, d(n) es impar y √n se cuenta una sola vez, pero la fórmula n^{d(n)/2} sigue valiendo.)",
 "Patrón por emparejamiento divisor–codivisor: cada par multiplica n, así que el producto es una potencia de n con exponente igual al número de parejas, d(n)/2. Verificado con Python: el producto de los divisores de n es n^{d(n)/2} para todo n de 1 a 59 (12 → 1728).",
 18, ["emparejamiento de divisores", "función número de divisores d(n)", "producto como potencia"],
 ["funciones multiplicativas en teoría de números", "simetría divisor–codivisor", "fórmulas de conteo"],
 "", ["divisores", "producto", "teoria-numeros", "nivel-medio"], "cap. 3 §3.1 (Ej. 3.1.15)"))

A(P(181, "Subconjuntos con suma grande", "patrones", 3,
 "¿Cuántos subconjuntos del conjunto {1, 2, 3, 4, …, 30} tienen la propiedad de que la suma de sus elementos es mayor que 232?",
 ["¿Cuánto suman TODOS los elementos? Ese total y el umbral 232 están relacionados. Calcula 1+2+⋯+30.",
  "La suma total es 30·31/2 = 465. Nota que 232 es casi la mitad: 465/2 = 232.5. Eso invita a una simetría.",
  "A cada subconjunto S asóciale su COMPLEMENTO S' = {1,…,30}∖S. Se cumple suma(S) + suma(S') = 465.",
  "suma(S) > 232 (o sea ≥ 233) equivale a suma(S') ≤ 232. Como 465 es impar, NINGÚN subconjunto suma exactamente 232.5: cada subconjunto cae en exactamente uno de los dos bandos.",
  "La complementación empareja biyectivamente los subconjuntos con suma > 232 con los de suma ≤ 232, partiendo en dos mitades iguales los 2³⁰ subconjuntos. Respuesta: 2³⁰/2 = 2²⁹."],
 "Hay 2²⁹ subconjuntos. La suma total de {1,…,30} es 465, un número impar. Para cada subconjunto S, su complemento S' cumple suma(S)+suma(S') = 465, de modo que suma(S) > 232 ⟺ suma(S') < 233 ⟺ suma(S') ≤ 232. La complementación S ↔ S' es una biyección entre los subconjuntos de suma > 232 y los de suma ≤ 232 (ninguno suma exactamente 232.5 por ser 465 impar), así que ambas clases tienen el mismo tamaño: la mitad de los 2³⁰ subconjuntos, es decir 2²⁹.",
 "Patrón de simetría por complementación: un total impar garantiza que no hay empate en la mitad, partiendo el conjunto potencia en dos mitades equinumerosas. No hace falta contar: la biyección lo resuelve. Verificado con Python: el análogo {1..6} (total 21) con umbral 10 da 2⁵ = 32 subconjuntos.",
 22, ["biyección por complementación", "argumento de simetría", "conteo sin enumerar"],
 ["simetría en conjuntos potencia", "particiones equinumerosas", "involuciones que emparejan"],
 "", ["conteo", "simetria", "subconjuntos", "nivel-medio"], "cap. 3 §3.1 (Ej. 3.1.16)"))

A(P(182, "Temperatura promedio de un planeta", "patrones", 4,
 "Un planeta esférico tridimensional tiene su centro en (0, 0, 0) y radio 20. En cada punto (x, y, z) de su superficie, la temperatura es T(x, y, z) = (x + y)² + (y − z)² grados. ¿Cuál es la temperatura promedio de la superficie del planeta?",
 ["Promediar T sobre la esfera parece una integral fea. Pero primero DESARROLLA T y usa la simetría de la esfera.",
  "T = (x+y)² + (y−z)² = x² + 2xy + y² + y² − 2yz + z² = x² + 2y² + z² + 2xy − 2yz. Promedia término a término.",
  "Por simetría de la esfera, los promedios de los términos CRUZADOS (xy, yz) son 0. Y por simetría, ⟨x²⟩ = ⟨y²⟩ = ⟨z²⟩. ¿Cuánto vale cada uno?",
  "Como x²+y²+z² = R² en toda la superficie, ⟨x²+y²+z²⟩ = R², y por simetría ⟨x²⟩ = ⟨y²⟩ = ⟨z²⟩ = R²/3.",
  "⟨T⟩ = ⟨x²⟩ + 2⟨y²⟩ + ⟨z²⟩ + 0 + 0 = (1+2+1)·R²/3 = 4R²/3. Con R=20: 4·400/3 = 1600/3 ≈ 533.33."],
 "La temperatura promedio es 4R²/3 = 1600/3 ≈ 533.33 grados. Desarrollando, T = x² + 2y² + z² + 2xy − 2yz. Sobre la esfera, los promedios de los términos cruzados ⟨xy⟩ y ⟨yz⟩ son 0 por simetría, y ⟨x²⟩ = ⟨y²⟩ = ⟨z²⟩ = R²/3 (porque ⟨x²+y²+z²⟩ = R²). Entonces ⟨T⟩ = (1 + 2 + 1)·R²/3 = 4R²/3, y con R = 20 da 1600/3.",
 "Explotar la simetría esférica: los cruzados promedian 0 y los cuadrados se reparten por igual la energía R². Reconocer ese patrón evita integrar. Verificado con Python: muestreo de 300 000 puntos uniformes sobre la esfera de radio 20 da un promedio ≈ 534, consistente con 1600/3 dentro del error Monte Carlo.",
 28, ["simetría esférica", "promedios de términos cuadráticos", "valor esperado geométrico"],
 ["valores esperados por simetría", "momentos de distribuciones", "integrales sobre esferas"],
 "", ["esfera", "promedio", "simetria", "nivel-avanzado"], "cap. 3 §3.1 (Ej. 3.1.24)"))

A(P(183, "Cuándo −5⁴ + 5⁵ + 5ⁿ es un cuadrado (Grecia 1995)", "patrones", 3,
 "Encuentra todos los enteros n ≥ 0 para los cuales −5⁴ + 5⁵ + 5ⁿ es un cuadrado perfecto.",
 ["Simplifica primero la parte constante: −5⁴ + 5⁵ = 5⁴(−1 + 5) = 5⁴·4. ¿Qué número es eso?",
  "−5⁴ + 5⁵ = 4·625 = 2500 = 50². Así que buscas n tal que 2500 + 5ⁿ = k² para algún entero k.",
  "Escribe 5ⁿ = k² − 2500 = (k − 50)(k + 50). Como el lado izquierdo es potencia de 5, ambos factores deben ser potencias de 5.",
  "Pon k − 50 = 5^a y k + 50 = 5^b con a < b y a + b = n. Restando: 5^b − 5^a = 100, es decir 5^a(5^{b−a} − 1) = 100.",
  "100 = 4·25, y 5^{b−a}−1 debe dar el factor coprimo con 5: con 5^a = 25 (a=2) queda 5^{b−a}−1 = 4 → 5^{b−a} = 5 → b−a = 1, b = 3. Entonces n = a+b = 5. Comprobación: 2500 + 5⁵ = 5625 = 75². Único n = 5."],
 "El único valor es n = 5. Como −5⁴ + 5⁵ = 5⁴·4 = 2500 = 50², se busca n con 2500 + 5ⁿ = k². Factorizando 5ⁿ = (k−50)(k+50), ambos factores son potencias de 5: k−50 = 5^a, k+50 = 5^b (a<b). Restando, 5^a(5^{b−a}−1) = 100, que obliga a 5^a = 25 (a=2) y 5^{b−a}−1 = 4, o sea b−a = 1, b = 3. Luego n = a+b = 5, y en efecto 2500 + 5⁵ = 5625 = 75².",
 "Patrón de factorización de diferencia de cuadrados (k²−c² = (k−c)(k+c)) combinado con que una potencia prima solo se factoriza como producto de potencias del mismo primo. Verificado con Python por fuerza bruta: el único n en [0,60) que hace cuadrado a −5⁴+5⁵+5ⁿ es n=5.",
 22, ["diferencia de cuadrados", "factorización de potencias primas", "ecuación diofantina"],
 ["ecuaciones exponenciales diofantinas", "factorización única", "olimpiadas de teoría de números"],
 "1995", ["diofantina", "cuadrado-perfecto", "grecia", "nivel-medio"], "cap. 7 §7.4 (Ej. 7.4.6, Grecia 1995)"))

A(P(184, "Tres fracciones que multiplican 2 (Reino Unido 1995)", "patrones", 4,
 "Encuentra todas las ternas de enteros positivos (a, b, c) con a ≤ b ≤ c tales que (1 + 1/a)(1 + 1/b)(1 + 1/c) = 2.",
 ["Acota a usando el orden. Como a ≤ b ≤ c, el factor (1+1/a) es el mayor. Si a fuera grande, el producto sería < 2.",
  "Si a = 1, el primer factor es 2 y los otros dos (> 1) lo pasarían de 2: imposible. Si a ≥ 4, los tres factores son ≤ 5/4, y (5/4)³ < 2. Entonces a ∈ {2, 3}.",
  "El producto debe ser ≥ 2, y como cada factor > 1, también (1+1/a)³ ≥ 2, lo que acota a ≤ 3 (junto con el descarte de a=1). Analiza a = 2 y a = 3 por separado.",
  "Para a fijo, despeja (1+1/b)(1+1/c) = 2/(1+1/a) y acota b igual que acotaste a. Para cada (a,b) válido, c queda determinado por la ecuación.",
  "Resultan exactamente cinco ternas: (2,4,15), (2,5,9), (2,6,7), (3,3,8), (3,4,5)."],
 "Las ternas son (2,4,15), (2,5,9), (2,6,7), (3,3,8) y (3,4,5). Por el orden a ≤ b ≤ c, el factor (1+1/a) es el mayor; a = 1 hace el producto > 2 y a ≥ 4 lo hace < 2 (pues (5/4)³ < 2), así que a ∈ {2,3}. Fijando a y acotando b de la misma forma, c queda determinado, y la búsqueda exhaustiva sobre el rango finito arroja exactamente esas cinco soluciones.",
 "Acotar variables con el principio del extremo (la variable más pequeña domina el producto) reduce el problema a un rango finito que se barre por casos. Verificado con Python: las únicas ternas con a≤b≤c y producto exactamente 2 son (2,4,15), (2,5,9), (2,6,7), (3,3,8), (3,4,5).",
 30, ["acotar variables", "búsqueda por casos", "principio del extremo"],
 ["ecuaciones diofantinas con fracciones unitarias", "descomposición de la unidad", "olimpiadas de teoría de números"],
 "1995", ["diofantina", "fracciones", "reino-unido", "nivel-avanzado"], "cap. 7 §7.4 (Ej. 7.4.7, Reino Unido 1995)"))

A(P(185, "El único exponente que da un cuadrado", "patrones", 3,
 "Demuestra que existe exactamente un entero n para el cual 2⁸ + 2¹¹ + 2ⁿ es un cuadrado perfecto, y encuéntralo.",
 ["Saca factor común o suma la parte conocida: 2⁸ + 2¹¹ = 256 + 2048 = 2304. ¿Es un cuadrado?",
  "2304 = 48². Así que buscas n con 2304 + 2ⁿ = k². Reescríbelo como diferencia de cuadrados.",
  "2ⁿ = k² − 2304 = (k − 48)(k + 48). Como el lado izquierdo es potencia de 2, ambos factores son potencias de 2.",
  "Pon k − 48 = 2^a, k + 48 = 2^b con a < b. Restando: 2^b − 2^a = 96, o sea 2^a(2^{b−a} − 1) = 96 = 2⁵·3.",
  "El factor impar 3 debe ser 2^{b−a} − 1, así que 2^{b−a} = 4, b−a = 2, y 2^a = 32, a = 5, b = 7. Entonces n = a + b = 12. Comprobación: 2304 + 2¹² = 2304 + 4096 = 6400 = 80². Único."],
 "El único valor es n = 12. Como 2⁸ + 2¹¹ = 2304 = 48², se busca n con 2304 + 2ⁿ = k². Factorizando 2ⁿ = (k−48)(k+48), ambos factores son potencias de 2: k−48 = 2^a, k+48 = 2^b (a<b). Restando, 2^a(2^{b−a}−1) = 96 = 2⁵·3; el factor impar 3 obliga a 2^{b−a} = 4 (b−a=2) y 2^a = 32 (a=5), luego b=7 y n = a+b = 12. En efecto 2304 + 2¹² = 6400 = 80².",
 "Misma plantilla que el problema de las potencias de 5: completar a cuadrado conocido, factorizar la diferencia de cuadrados y usar que una potencia de 2 solo se factoriza en potencias de 2; el factor impar de 96 fija el exponente. Verificado con Python: el único n en [0,60) que hace cuadrado a 2⁸+2¹¹+2ⁿ es n=12.",
 24, ["diferencia de cuadrados", "factorización de potencias de 2", "factor impar único"],
 ["ecuaciones exponenciales diofantinas", "factorización única", "completar cuadrados"],
 "", ["diofantina", "potencias-de-2", "cuadrado-perfecto", "nivel-medio"], "cap. 7 §7.4 (Ej. 7.4.8)"))

A(P(186, "La ecuación 7ˣ − 3ʸ = 4 (India 1995)", "patrones", 3,
 "Encuentra todos los enteros positivos x, y que satisfacen 7ˣ − 3ʸ = 4.",
 ["Prueba valores pequeños: x=1, y=1 da 7 − 3 = 4. ¿Hay más? Usa congruencias para descartar.",
  "Mira la ecuación módulo 4: 7 ≡ −1 (mód 4), así que 7ˣ ≡ (−1)ˣ. Y 3ʸ ≡ (−1)ʸ. La ecuación dice 7ˣ − 3ʸ ≡ 0 (mód 4).",
  "(−1)ˣ − (−1)ʸ ≡ 0 (mód 4) obliga a que x e y tengan la misma paridad. Ahora mira módulo otro número, como 9 o 7, para restringir más.",
  "Módulo 9: si y ≥ 2, 3ʸ ≡ 0, así que 7ˣ ≡ 4 (mód 9). Las potencias de 7 módulo 9 son 7, 4, 1, 7, 4, 1…; 7ˣ ≡ 4 fuerza x ≡ 2 (mód 3). Combina con las cotas.",
  "El análisis modular fuerza la solución pequeña; la búsqueda confirma que (x, y) = (1, 1) es la única."],
 "La única solución en enteros positivos es (x, y) = (1, 1), pues 7¹ − 3¹ = 4. El análisis módulo 4 (7 ≡ −1, 3 ≡ −1) obliga a que x e y tengan la misma paridad, y módulos adicionales (9 para acotar y, 7 para x) descartan toda solución con exponentes mayores, dejando solo (1,1).",
 "Combinar varias congruencias para encajonar los exponentes es la táctica estándar en ecuaciones exponenciales diofantinas. Verificado con Python: en el rango x ∈ [1,11], y ∈ [1,19] la única solución de 7ˣ − 3ʸ = 4 es (1,1).",
 22, ["congruencias múltiples", "órdenes módulo n", "ecuación exponencial"],
 ["ecuaciones diofantinas exponenciales", "aritmética modular", "olimpiadas de teoría de números"],
 "1995", ["diofantina", "congruencias", "india", "nivel-medio"], "cap. 7 §7.4 (Ej. 7.4.13, India 1995)"))

A(P(187, "Divisores compartidos de dos potencias (Putnam 1983)", "patrones", 4,
 "¿Cuántos enteros positivos son divisores de al menos uno de los números 10⁴⁰ y 20³⁰?",
 ["Esto es un conteo por inclusión-exclusión: |divisores de A ∪ divisores de B| = d(A) + d(B) − |divisores comunes|. Factoriza A y B en primos.",
  "10⁴⁰ = (2·5)⁴⁰ = 2⁴⁰·5⁴⁰. Y 20³⁰ = (2²·5)³⁰ = 2⁶⁰·5³⁰. Cuenta los divisores de cada uno con la fórmula de exponentes + 1.",
  "d(10⁴⁰) = (40+1)(40+1) = 41². d(20³⁰) = (60+1)(30+1) = 61·31. Ahora los divisores COMUNES son los del máximo común divisor.",
  "mcd(10⁴⁰, 20³⁰) = 2^{mín(40,60)}·5^{mín(40,30)} = 2⁴⁰·5³⁰, con (40+1)(30+1) = 41·31 divisores.",
  "Por inclusión-exclusión: 41² + 61·31 − 41·31 = 1681 + 1891 − 1271 = 2301."],
 "Hay 2301 divisores. Factorizando, 10⁴⁰ = 2⁴⁰5⁴⁰ (con 41² divisores) y 20³⁰ = 2⁶⁰5³⁰ (con 61·31 divisores). Los divisores comunes son los del mcd = 2⁴⁰5³⁰, que tiene 41·31 divisores. Por inclusión-exclusión, el número de divisores de al menos uno es 41² + 61·31 − 41·31 = 1681 + 1891 − 1271 = 2301.",
 "Patrón de conteo de divisores vía factorización prima e inclusión-exclusión, donde la intersección de los conjuntos de divisores corresponde al mcd (exponentes mínimos). Verificado con Python: 41² + 61·31 − 41·31 = 2301.",
 26, ["conteo de divisores d(n)", "inclusión-exclusión", "mcd por exponentes mínimos"],
 ["funciones multiplicativas", "principio de inclusión-exclusión", "retículo de divisores"],
 "1983", ["putnam", "divisores", "inclusion-exclusion", "nivel-avanzado"], "cap. 7 §7.5 (Ej. 7.5.12, Putnam 1983)"))

A(P(188, "x² + y² + z² = 2xyz", "patrones", 4,
 "Encuentra todas las soluciones en enteros no negativos de la ecuación x² + y² + z² = 2xyz.",
 ["Prueba (0,0,0): funciona. Para buscar otras, mira la ecuación módulo 2: el lado derecho 2xyz es PAR.",
  "Entonces x² + y² + z² es par, lo que obliga a que el número de variables impares sea par (0 o 2). Analiza módulo 4 para ir más lejos.",
  "Módulo 4, los cuadrados son 0 o 1, y 2xyz es divisible por 2. Si alguna variable fuera impar, su cuadrado sería 1 mód 4; cuenta paridades de potencias de 2.",
  "Argumento de descenso: si (x,y,z) es solución no trivial, las tres deben ser pares; escribe x=2x', y=2y', z=2z' y sustituye para obtener una ecuación más pequeña.",
  "Sustituyendo, 4(x'²+y'²+z'²) = 16x'y'z', o sea x'²+y'²+z'² = 4x'y'z', y el descenso continúa sin fin salvo que todas sean 0. La única solución es (0,0,0)."],
 "La única solución en enteros no negativos es (0, 0, 0). Por descenso infinito: módulo 2 (y 4) se ve que en cualquier solución las tres variables deben ser pares; escribiendo x=2x', y=2y', z=2z' y sustituyendo se obtiene x'²+y'²+z'² = 4x'y'z' (y de nuevo todas pares), generando una cadena de soluciones cada vez menores. Eso es imposible para enteros positivos, así que la única posibilidad es x=y=z=0.",
 "Descenso infinito al estilo Fermat sobre una ecuación tipo Markov degenerada: el análisis de paridad fuerza divisibilidad por 2 en cada paso, y el buen orden impide una caída infinita salvo en el origen. Verificado con Python: en [0,40)³ la única solución es (0,0,0).",
 28, ["descenso infinito", "análisis de paridad módulo 2 y 4", "ecuación tipo Markov"],
 ["método del descenso de Fermat", "ecuaciones diofantinas sin solución no trivial", "argumentos de divisibilidad"],
 "", ["diofantina", "descenso-infinito", "paridad", "nivel-avanzado"], "cap. 7 §7.5 (Ej. 7.5.16)"))

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
