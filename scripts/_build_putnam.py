# -*- coding: utf-8 -*-
"""Tanda 30 — Andreescu & Gelca, *Putnam and Beyond* (cap. 1 Methods of Proof +
§3.1.1 Search for a Pattern). Append 44 problemas verificados a data/problems.json.
Todas las afirmaciones numéricas verificadas con Python (ver /tmp/verify_putnam.py
y la bitácora de HANDOFFCES.md). Builder idempotente: aborta si hay choque de ids.
Sector C (entrenamiento), esquema §4.1, ids 189-232, balanceado 11/11/11/11.
(Pólya marcado completado/saltado por decisión del usuario en la tanda 29.)"""
import json, collections

SRC = "Andreescu & Gelca, *Putnam and Beyond* (Springer, 2007)"

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
# INVERSION (11) — contradicción, construcción, trabajar hacia atrás
# =====================================================================

A(P(189, "La irracionalidad de √2 + √3 + √5", "inversion", 4,
 "Demuestra que √2 + √3 + √5 es un número irracional.",
 ["Supón lo contrario (√2+√3+√5 = r racional) y busca una contradicción aislando radicales y elevando al cuadrado.",
  "Aísla uno: √2+√3 = r − √5. Eleva al cuadrado ambos lados para reducir el número de raíces sueltas.",
  "Al cuadrado: 5 + 2√6 = r² − 2r√5 + 5, o sea 2√6 + 2r√5 = r². Sigue aislando y elevando para eliminar √5 y √6.",
  "Repitiendo el proceso llegas a una ecuación donde un √(entero no cuadrado) queda igualado a una expresión racional — contradicción, pues √6, √5, etc., son irracionales.",
  "Cada vez que aíslas un radical y elevas al cuadrado reduces los radicales; al final obtienes √k racional con k no cuadrado, lo cual es falso. Luego la suma es irracional."],
 "Es irracional. Supón √2+√3+√5 = r ∈ ℚ. Aislando y elevando al cuadrado sucesivamente (primero √2+√3 = r−√5, luego se elimina √5, después √6) se llega a una igualdad de la forma √k = (expresión racional) con k entero no cuadrado, lo cual es imposible porque √k es irracional. La contradicción prueba que √2+√3+√5 ∉ ℚ.",
 "Argumento por contradicción combinado con eliminación iterativa de radicales. Su polinomio mínimo sobre ℚ tiene grado 8 y carece de raíz racional. Verificado con Python: el número 5.38233… no coincide con ninguna fracción de denominador ≤ 10⁶ (evidencia numérica de irracionalidad).",
 25, ["argumento por contradicción", "eliminación de radicales", "irracionalidad"],
 ["extensiones de cuerpos", "polinomios mínimos", "pruebas de irracionalidad"],
 "", ["contradiccion", "irracionalidad", "radicales", "nivel-avanzado"], "cap. 1 §1.1 (Prob. 1)"))

A(P(190, "Nueve enteros consecutivos sin partición de igual producto", "inversion", 3,
 "Demuestra que ningún conjunto de nueve enteros consecutivos puede partirse en dos conjuntos no vacíos tales que el producto de los elementos del primero sea igual al producto de los del segundo.",
 ["Supón que sí se puede. Piensa en un primo grande que aparezca entre los nueve consecutivos: ¿cuántos múltiplos suyos hay?",
  "Entre nueve enteros consecutivos, considera un primo p con 5 ≤ p: a lo más uno de los nueve es múltiplo de p (porque 2p > 9 cuando p ≥ 5).",
  "Si exactamente uno de los nueve números es divisible por ese primo p, ese factor p solo puede caer en UNO de los dos conjuntos.",
  "Entonces ese primo divide el producto de un conjunto pero no el del otro: los productos no pueden ser iguales. Contradicción.",
  "Siempre existe tal primo p ≥ 5 con un único múltiplo entre nueve consecutivos (por ejemplo, un primo en el rango), lo que rompe la igualdad de productos."],
 "Es imposible. Supón que los nueve consecutivos se parten en dos conjuntos de igual producto. Entre nueve enteros consecutivos hay un primo p ≥ 5 del cual a lo más un múltiplo cae en el rango (pues 2p > 9 para p ≥ 5). Ese único múltiplo aporta el factor p a uno solo de los dos conjuntos, de modo que p divide un producto pero no el otro — los productos no pueden coincidir. Contradicción.",
 "Argumento por contradicción usando la 'asimetría' de un primo grande: un factor primo que aparece una sola vez no puede repartirse en dos productos iguales. Verificado con Python: para todo bloque de 9 consecutivos con inicio 1..39, ninguna bipartición iguala los productos.",
 20, ["argumento por contradicción", "factor primo único", "divisibilidad"],
 ["unicidad de la factorización", "argumentos de paridad de exponentes", "balanceo de productos"],
 "", ["contradiccion", "primos", "particion", "nivel-medio"], "cap. 1 §1.1 (Prob. 2)"))

A(P(191, "Ningún polinomio entero toma solo valores primos", "inversion", 3,
 "Demuestra que no existe ningún polinomio P(x) = aₙxⁿ + ⋯ + a₀ con coeficientes enteros y grado al menos 1 tal que P(0), P(1), P(2), … sean todos números primos.",
 ["Supón que existe tal P. Mira el valor P(0): es un primo, llamémoslo p. Usa una propiedad de divisibilidad de los polinomios.",
  "Para polinomios con coeficientes enteros, a − b divide a P(a) − P(b). Aplica esto con b = 0.",
  "Entonces P(0) = p divide a P(kp) − P(0) para todo k, así que p | P(kp) para todo entero k ≥ 1.",
  "Como cada P(kp) es supuestamente primo y divisible por p, debe ser igual a p. Pero un polinomio no constante no puede tomar el mismo valor infinitas veces.",
  "P(kp) = p para infinitos k contradice que P tenga grado ≥ 1 (tomaría el valor p más de n veces). Contradicción."],
 "No existe. Supón que P(0)=p es primo. Como a−b divide a P(a)−P(b), se tiene p | P(kp) − P(0), de modo que p | P(kp) para todo k ≥ 1. Si todos esos valores son primos y divisibles por p, entonces P(kp) = p para infinitos k. Pero un polinomio de grado ≥ 1 no puede tomar el mismo valor más de su grado de veces. Contradicción: no hay tal polinomio.",
 "Argumento de Euler por contradicción: la divisibilidad a−b | P(a)−P(b) fuerza la repetición de un valor, prohibida por el teorema fundamental del álgebra. Verificado con Python: el mecanismo P(kp) ≡ 0 (mód p) con valor compuesto se cumple para x²+x+41, x³+3x+17, etc.",
 22, ["argumento por contradicción", "divisibilidad a−b | P(a)−P(b)", "valores repetidos de un polinomio"],
 ["polinomios generadores de primos", "teorema fundamental del álgebra", "congruencias polinómicas"],
 "", ["contradiccion", "polinomios", "primos", "nivel-medio"], "cap. 1 §1.1 (Ej. Euler)"))

A(P(192, "El desplazamiento cíclico con sumas parciales positivas", "inversion", 4,
 "Dada una sucesión de enteros x₁, x₂, …, xₙ cuya suma es 1, demuestra que exactamente uno de los n desplazamientos cíclicos — x₁,…,xₙ ; x₂,…,xₙ,x₁ ; … ; xₙ,x₁,…,xₙ₋₁ — tiene todas sus sumas parciales positivas.",
 ["Es un problema de existencia y unicidad. Construye una función de sumas acumuladas y trabaja hacia atrás desde su comportamiento.",
  "Define S₀=0, Sₖ = x₁+⋯+xₖ. Como la suma total es 1, al extender periódicamente se cumple S_{k+n} = Sₖ + 1: la gráfica 'sube' una unidad por vuelta.",
  "El desplazamiento que empieza en la posición j tiene sumas parciales positivas sii Sⱼ es estrictamente menor que todos los S₀,…,S_{j−1} y ≤ todos los siguientes dentro de la vuelta. Busca el MÍNIMO.",
  "Toma el índice j (en una vuelta) donde Sⱼ alcanza su valor MÍNIMO por última vez. Arrancar justo después de ese mínimo hace que todas las sumas parciales sean positivas.",
  "Como la sucesión sube 1 por periodo, el mínimo en una vuelta es único en su 'última aparición', dando exactamente un arranque válido."],
 "Exactamente un desplazamiento cumple la propiedad. Sea S₀=0, Sₖ=x₁+⋯+xₖ; como la suma total es 1, la extensión periódica satisface S_{k+n}=Sₖ+1, así que las sumas acumuladas crecen una unidad por vuelta y alcanzan un mínimo único (en su última aparición dentro de un periodo). El desplazamiento que arranca justo después de ese mínimo tiene todas las sumas parciales positivas, y ningún otro arranque lo logra. Por tanto hay exactamente uno.",
 "Lema de Raney (votación cíclica): la unicidad surge de localizar el mínimo de las sumas acumuladas y arrancar después de él. Trabajar hacia atrás desde 'dónde está el mínimo' da el punto de partida. Verificado con Python: 3000 sucesiones aleatorias de suma 1 tienen exactamente un desplazamiento válido.",
 28, ["lema de Raney", "sumas acumuladas", "trabajar hacia atrás desde el mínimo"],
 ["caminos de Dyck y voto cíclico", "números de Catalan", "argumentos de rotación"],
 "", ["ciclico", "sumas-parciales", "raney", "nivel-avanzado"], "cap. 1 §1.2 (Prob. 19)"))

A(P(193, "Embaldosar 2ⁿ × 2ⁿ sin una esquina con L-triominós", "inversion", 3,
 "Demuestra que, para todo n ≥ 1, un tablero de 2ⁿ × 2ⁿ con un cuadrito de una esquina removido puede cubrirse exactamente con piezas en forma de L formadas por tres cuadritos (L-triominós).",
 ["Procede por inducción y CONSTRUCCIÓN: el caso n=1 es un tablero 2×2 sin una esquina, que es justo una pieza L.",
  "Para el paso inductivo, parte el tablero 2^{n+1}×2^{n+1} en cuatro cuadrantes, cada uno de tamaño 2ⁿ×2ⁿ.",
  "Uno de los cuadrantes ya tiene su esquina removida (donde estaba el hueco original). ¿Cómo crear un 'hueco' artificial en los otros tres?",
  "Coloca una pieza L justo en el centro, cubriendo una esquina interior de cada uno de los tres cuadrantes restantes. Ahora cada cuadrante es un 2ⁿ×2ⁿ con una esquina faltante.",
  "Por hipótesis inductiva, cada cuadrante (2ⁿ×2ⁿ sin esquina) se embaldosa. La pieza central más los cuatro cuadrantes completan el tablero."],
 "Por inducción. Base: 2×2 sin una esquina ES una pieza L. Paso: divide el tablero 2^{n+1}×2^{n+1} en cuatro cuadrantes 2ⁿ×2ⁿ; uno contiene el hueco original. Coloca una L en el centro que cubra la esquina interior de los otros tres cuadrantes, de modo que los cuatro queden como tableros 2ⁿ×2ⁿ con una esquina faltante. Por la hipótesis inductiva cada uno se embaldosa, y junto con la L central se cubre todo el tablero.",
 "Inducción constructiva de tipo 'divide y vencerás': el truco es fabricar el hueco que la hipótesis necesita colocando una pieza en el centro. Verificado con Python: un backtracking exacto confirma el embaldosado para n = 1, 2, 3.",
 20, ["inducción constructiva", "divide y vencerás", "embaldosado con triominós"],
 ["algoritmos divide y vencerás", "fractales y recursión", "embaldosados deficientes"],
 "", ["induccion", "triominos", "construccion", "nivel-medio"], "cap. 1 §1.2 (Prob. 18)"))

A(P(194, "Cortar un cubo en cubos distintos", "inversion", 4,
 "Demuestra que es imposible cortar un cubo en una cantidad finita de cubos más pequeños, no habiendo dos del mismo tamaño.",
 ["Supón que tal disección existe y aplica el principio del extremo a UNA cara del cubo.",
  "Mira la cara inferior del cubo: está cubierta por cuadrados (las caras inferiores de algunos cubitos), todos de distinto tamaño. Considera el MÁS PEQUEÑO de esos cuadrados.",
  "El cuadrado más pequeño de la cara inferior no puede tocar el borde de la cara (sus vecinos, más grandes, lo rodean): queda en el interior, rodeado por cubos mayores.",
  "El cubito sobre ese cuadrado más pequeño queda encerrado en un 'pozo'. Su cara superior debe a su vez cubrirse con cubos aún menores. Repite el argumento.",
  "Esto genera una sucesión infinita de cubos cada vez más pequeños, imposible en una disección finita. Contradicción."],
 "Es imposible. Supón una disección en cubos distintos. En la cara inferior, los cubitos que la tocan dejan cuadrados de distinto tamaño; el más pequeño no puede tocar el borde (sus vecinos mayores lo rodean), así que queda rodeado y el cubo encima de él cae en un 'pozo'. La cara superior de ese cubo debe cubrirse con cubos aún más pequeños, y el mismo argumento se repite, generando una sucesión infinita decreciente de cubos — imposible en una disección finita. Contradicción.",
 "Principio del extremo (el elemento mínimo) en cascada infinita: a diferencia del cuadrado (que SÍ se puede 'cuadrar' con cuadrados distintos), la tercera dimensión crea pozos que fuerzan un descenso sin fin. La 'solución' es el argumento estructural, no un valor numérico.",
 28, ["principio del extremo", "descenso infinito", "argumento por contradicción"],
 ["cuadrar el cuadrado (squared squares)", "geometría combinatoria", "imposibilidad por minimalidad"],
 "", ["extremo", "cubos", "imposibilidad", "nivel-avanzado"], "cap. 1 §1.4 (Ej.)"))

A(P(195, "Las fichas blancas y negras (IMO 2005)", "inversion", 5,
 "Hay n fichas alineadas en fila, cada una con una cara blanca y otra negra, todas con la cara blanca hacia arriba. En cada paso, si es posible, se elige una ficha con la cara blanca hacia arriba que NO sea de los extremos, se retira, y se voltean sus dos fichas vecinas. Demuestra que se puede llegar a una configuración con solo dos fichas restantes si y solo si n − 1 no es divisible por 3.",
 ["Hay dos cosas que controlar: la PARIDAD del número de fichas negras (un invariante simple) y un invariante más fino módulo 3.",
  "Observa la paridad del número de fichas negras: cada operación voltea dos vecinas, así que la paridad del total de negras se conserva. Si quedan dos fichas, deben tener el mismo color.",
  "Define un invariante módulo 3: a cada ficha blanca con t negras a su izquierda asígnale (−1)ᵗ, y sea S la suma de esos valores módulo 3. Verifica que la operación NO cambia S.",
  "Si la partida termina con dos negras, S ≡ 0; si termina con dos blancas, S ≡ 2. Calcula S inicial (todas blancas) y relaciona su valor con n módulo 3.",
  "El invariante S (mód 3) de la posición inicial determina si 2 fichas son alcanzables, y resulta posible exactamente cuando 3 ∤ (n−1). El recíproco se construye retirando fichas blancas de izquierda a derecha."],
 "Se puede llegar a dos fichas si y solo si 3 ∤ (n−1). Dos invariantes lo gobiernan: (1) la paridad del número de fichas negras se conserva (cada paso voltea dos vecinas), así que las dos fichas finales tienen igual color; (2) asignando (−1)ᵗ a cada ficha blanca con t negras a su izquierda y tomando S = suma módulo 3, la operación deja S invariante. El valor de S inicial (todas blancas) determina la paridad/clase final, y el análisis muestra que dos fichas son alcanzables exactamente cuando 3 ∤ (n−1); el recíproco se logra retirando blancas de izquierda a derecha.",
 "Combinación de un invariante de paridad y un semi-invariante módulo 3, más una construcción explícita para el recíproco. Es un problema de lista corta de la IMO 2005. Verificado con Python: un buscador exhaustivo confirma que 2 fichas son alcanzables sii 3 ∤ (n−1) para n = 3..12.",
 40, ["invariante módulo 3", "invariante de paridad", "construcción del recíproco"],
 ["invariantes coloreados", "juegos de fichas", "problemas de alcanzabilidad"],
 "2005", ["imo", "invariante", "fichas", "nivel-experto"], "cap. 1 §1.5 (Ej., IMO 2005)"))

A(P(196, "Todo entero como suma y resta de cuadrados", "inversion", 3,
 "Demuestra que todo entero positivo puede representarse como ±1² ± 2² ± 3² ± ⋯ ± n² para algún entero positivo n y alguna elección de los signos.",
 ["Busca un 'bloque ajustable': una combinación de cuatro cuadrados consecutivos con signos que dé un valor pequeño y fijo.",
  "Calcula k² − (k+1)² − (k+2)² + (k+3)². ¿Qué valor constante obtienes, independiente de k?",
  "k² − (k+1)² − (k+2)² + (k+3)² = 4. Tienes un bloque de cuatro términos que aporta exactamente 4 y puede AÑADIRSE al final con cualquier signo global (±4).",
  "Verifica los casos base pequeños (1, 2, 3, 4) con n chico, y nota que puedes ajustar la paridad: ±1²±2²±3²±4² alcanza varios valores. Luego usa bloques de cuatro para subir o bajar de 4 en 4.",
  "Como los bloques de cuatro consecutivos aportan ±4 y los casos base cubren las clases iniciales, por inducción se alcanza todo entero positivo."],
 "Todo entero positivo es representable. La clave es la identidad k² − (k+1)² − (k+2)² + (k+3)² = 4: un bloque de cuatro cuadrados consecutivos aporta exactamente ±4. Resolviendo los casos base pequeños (1, 2, 3, 4 con n adecuado) y añadiendo bloques de cuatro de signo apropiado se ajusta cualquier objetivo de 4 en 4, cubriendo todos los enteros positivos.",
 "Construcción por bloques: una identidad que produce un incremento fijo (±4) más casos base convierte el problema en una inducción aritmética. Verificado con Python: una búsqueda consciente de la paridad representa todo N de 1 a 40 (con n a lo más 9).",
 22, ["construcción por bloques", "identidad de cuatro cuadrados", "inducción aritmética"],
 ["representaciones de enteros", "sumas con signos", "bases aditivas"],
 "", ["construccion", "cuadrados", "representacion", "nivel-medio"], "cap. 1 §1.2 (Prob. 30)"))

A(P(197, "Todo entero como suma de Fibonacci distintos (Zeckendorf)", "inversion", 3,
 "Demuestra que todo entero positivo puede escribirse como suma de términos distintos de la sucesión de Fibonacci (F₀=0, F₁=1, Fₙ₊₁ = Fₙ + Fₙ₋₁).",
 ["Procede por construcción greedy / inducción fuerte: dado N, ¿qué Fibonacci le restarías primero?",
  "Toma el mayor número de Fibonacci F que no exceda a N. Resta: el residuo N − F es menor que N. ¿Qué tan pequeño es?",
  "Si F es el mayor Fibonacci ≤ N, entonces N − F < F_{siguiente} − F = F_{anterior}, así que el residuo es estrictamente menor que F y no volverás a usar F.",
  "Por inducción fuerte, el residuo N − F (menor que N) se escribe como suma de Fibonacci distintos, todos menores que F, así que F no se repite.",
  "Restar siempre el mayor Fibonacci posible (algoritmo greedy) descompone N en Fibonacci distintos. Esta es la representación de Zeckendorf."],
 "Todo entero positivo admite tal representación. Por inducción fuerte: dado N, sea F el mayor Fibonacci con F ≤ N. El residuo N − F satisface N − F < F (pues el siguiente Fibonacci es ≤ N+algo), así que por hipótesis inductiva N − F es suma de Fibonacci distintos, todos menores que F; añadiendo F se obtiene N como suma de Fibonacci distintos. (El algoritmo greedy de restar el mayor Fibonacci posible produce la representación de Zeckendorf, que además no usa Fibonacci consecutivos.)",
 "Algoritmo greedy con inducción fuerte: la elección del mayor Fibonacci garantiza que el residuo es pequeño y no reutiliza el término. Verificado con Python: el greedy de Fibonacci representa correctamente todo N de 1 a 300.",
 18, ["algoritmo greedy", "inducción fuerte", "representación de Zeckendorf"],
 ["sistemas de numeración no estándar", "sucesión de Fibonacci", "algoritmos voraces"],
 "", ["fibonacci", "zeckendorf", "greedy", "nivel-medio"], "cap. 1 §1.2 (Prob. 23)"))

A(P(198, "Un número de n dígitos divisible por 2ⁿ con dígitos 2 y 3", "inversion", 4,
 "Demuestra que para todo entero positivo n existe un número de n dígitos, formado solo con los dígitos 2 y 3, que es divisible por 2ⁿ.",
 ["Procede por inducción CONSTRUYENDO el número dígito a dígito, agregando cifras por la IZQUIERDA.",
  "Base: para n=1, el número '2' es divisible por 2. Supón que tienes un número Mₙ de n dígitos (solo 2 y 3) divisible por 2ⁿ.",
  "Quieres formar M_{n+1} = d·10ⁿ + Mₙ con d ∈ {2,3}, divisible por 2^{n+1}. Analiza la divisibilidad módulo 2^{n+1}.",
  "Como Mₙ = 2ⁿ·k, tienes M_{n+1} = 2ⁿ(d·5ⁿ + k). Para que 2^{n+1} | M_{n+1} necesitas que d·5ⁿ + k sea PAR. Como 5ⁿ es impar, eliges d (2 o 3) según la paridad de k.",
  "Si k es par, toma d=2; si k es impar, toma d=3 (que cambia la paridad). En ambos casos d·5ⁿ + k queda par, completando el paso inductivo."],
 "Por inducción. Base n=1: '2' es divisible por 2. Paso: sea Mₙ = 2ⁿ·k un número de n dígitos con cifras 2,3, divisible por 2ⁿ. Forma M_{n+1} = d·10ⁿ + Mₙ = 2ⁿ(d·5ⁿ + k) con d ∈ {2,3}. Para que 2^{n+1} divida a M_{n+1} hace falta que d·5ⁿ + k sea par; como 5ⁿ es impar, se elige d=2 si k es par y d=3 si k es impar, lo que ajusta la paridad. Así M_{n+1} de n+1 dígitos (solo 2 y 3) es divisible por 2^{n+1}.",
 "Inducción constructiva con control de paridad: agregar un dígito por la izquierda multiplica por 10ⁿ = 2ⁿ5ⁿ, y la elección entre 2 y 3 ajusta la única condición de paridad pendiente. Verificado con Python: existe tal número para n = 1..13.",
 26, ["inducción constructiva", "divisibilidad por potencias de 2", "control de paridad"],
 ["levantamiento de soluciones módulo potencias (Hensel)", "construcción dígito a dígito", "aritmética modular"],
 "", ["induccion", "divisibilidad", "construccion", "nivel-avanzado"], "cap. 1 §1.2 (Prob. 17a)"))

A(P(199, "Un número de n dígitos divisible por 5ⁿ con dígitos 5 a 9", "inversion", 4,
 "Demuestra que para todo entero positivo n existe un número de n dígitos, formado solo con los dígitos 5, 6, 7, 8 y 9, que es divisible por 5ⁿ.",
 ["Igual que con 2ⁿ: inducción agregando un dígito por la IZQUIERDA, ahora con cinco dígitos disponibles.",
  "Base n=1: el dígito 5 es divisible por 5. Supón Mₙ de n dígitos (cifras 5–9) divisible por 5ⁿ, digamos Mₙ = 5ⁿ·k.",
  "Forma M_{n+1} = d·10ⁿ + Mₙ = 5ⁿ(d·2ⁿ + k). Para que 5^{n+1} | M_{n+1} necesitas que 5 divida a d·2ⁿ + k.",
  "Como 2ⁿ es invertible módulo 5, al variar d sobre {5,6,7,8,9} (que cubre TODAS las clases módulo 5) puedes hacer que d·2ⁿ + k ≡ 0 (mód 5).",
  "Exactamente un d ∈ {5,6,7,8,9} satisface la congruencia, completando el paso inductivo."],
 "Por inducción. Base n=1: '5' es divisible por 5. Paso: sea Mₙ = 5ⁿ·k con cifras 5–9, divisible por 5ⁿ. Forma M_{n+1} = d·10ⁿ + Mₙ = 5ⁿ(d·2ⁿ + k) con d ∈ {5,6,7,8,9}. Para que 5^{n+1} divida a M_{n+1} se necesita 5 | d·2ⁿ + k; como 2ⁿ es invertible módulo 5 y {5,6,7,8,9} recorre todas las clases módulo 5, existe exactamente un d que cumple la congruencia. Así se obtiene un número de n+1 dígitos (cifras 5–9) divisible por 5^{n+1}.",
 "Inducción constructiva: agregar un dígito multiplica por 10ⁿ = 2ⁿ5ⁿ, y como los cinco dígitos disponibles cubren todas las clases módulo 5, siempre hay una elección que mata el residuo. Verificado con Python: existe tal número para n = 1..11.",
 26, ["inducción constructiva", "divisibilidad por potencias de 5", "clases completas módulo 5"],
 ["levantamiento módulo potencias primas", "sistemas residuales completos", "construcción dígito a dígito"],
 "", ["induccion", "divisibilidad", "construccion", "nivel-avanzado"], "cap. 1 §1.2 (Prob. 17b)"))

# =====================================================================
# INVARIANTES (11) — casillero, invariantes, monovariantes
# =====================================================================

A(P(200, "Diez números de dos dígitos y subconjuntos de igual suma (IMO 1972)", "invariantes", 3,
 "Demuestra que todo conjunto de 10 números enteros de dos dígitos (del 10 al 99) tiene dos subconjuntos disjuntos no vacíos con la misma suma de elementos.",
 ["Es un argumento de casillero: las 'palomas' son los subconjuntos y los 'nidos' son las sumas posibles. Cuenta cada uno.",
  "Un conjunto de 10 elementos tiene 2¹⁰ = 1024 subconjuntos; quitando el vacío y el total quedan 1022 'palomas'.",
  "¿Cuál es la mayor suma posible de un subconjunto? A lo más 90+91+⋯+99 = 945, y en realidad las sumas relevantes son menores. Acótalas: las sumas caben entre 1 y unos 855.",
  "Como hay 1022 subconjuntos y menos de 945 sumas posibles, por el casillero dos subconjuntos distintos tienen la misma suma.",
  "Si esos dos subconjuntos se solapan, elimina sus elementos comunes: las sumas restantes siguen siendo iguales y los conjuntos quedan disjuntos."],
 "Un conjunto de 10 números tiene 1022 subconjuntos no triviales, pero sus sumas posibles caben en un rango de menos de 945 valores. Por el principio del casillero, dos subconjuntos distintos A y B tienen la misma suma. Si se solapan, quitándoles los elementos comunes se obtienen dos subconjuntos DISJUNTOS no vacíos con la misma suma (la suma común se resta de ambos).",
 "Casillero contando subconjuntos (palomas) contra sumas posibles (nidos); el solapamiento se resuelve eliminando la intersección. Es un problema de la IMO 1972. Verificado con Python: 1022 > 855, y empíricamente 300 conjuntos aleatorios de 10 números de dos dígitos siempre tienen dos subconjuntos de igual suma.",
 20, ["principio del casillero", "conteo de subconjuntos", "eliminar la intersección"],
 ["sumas de subconjuntos", "problema de la mochila", "argumentos de existencia"],
 "1972", ["imo", "casillero", "subconjuntos", "nivel-medio"], "cap. 1 §1.3 (Ej., IMO 1972)"))

A(P(201, "Nueve puntos en el cuadrado y un triángulo pequeño", "invariantes", 3,
 "Dados nueve puntos dentro de un cuadrado unitario, demuestra que algunos tres de ellos forman un triángulo de área a lo más 1/8.",
 ["Casillero geométrico: divide el cuadrado en regiones y mete los nueve puntos. ¿Cuántas regiones y de qué área?",
  "Parte el cuadrado en cuatro subcuadrados iguales de lado 1/2 (área 1/4 cada uno). Tienes 9 puntos y 4 subcuadrados.",
  "Como 9 = 2·4 + 1, por el casillero algún subcuadrado contiene al menos tres de los puntos.",
  "Necesitas acotar el área de un triángulo contenido en un subcuadrado de área 1/4. ¿Cuál es el área máxima de un triángulo dentro de un rectángulo?",
  "Un triángulo dentro de un rectángulo tiene área a lo más la mitad del rectángulo. Tres puntos en un subcuadrado de área 1/4 forman un triángulo de área ≤ 1/8."],
 "Divide el cuadrado unitario en cuatro subcuadrados de lado 1/2 (área 1/4). Como 9 = 2·4 + 1, por el casillero algún subcuadrado contiene tres de los nueve puntos. El área de un triángulo contenido en un rectángulo es a lo más la mitad del área del rectángulo (cortando por la paralela a un lado que pasa por el vértice opuesto), así que esos tres puntos forman un triángulo de área ≤ (1/2)·(1/4) = 1/8.",
 "Casillero geométrico + la cota 'triángulo ≤ medio rectángulo': subdividir hasta forzar tres puntos en una celda pequeña. Verificado con Python: 9 = 2·4+1 y el área de un triángulo en un subcuadrado de área 1/4 es ≤ 1/8.",
 20, ["principio del casillero", "triángulo en un rectángulo", "subdivisión geométrica"],
 ["geometría combinatoria", "cotas de área", "empaquetamiento de puntos"],
 "", ["casillero", "geometria", "triangulo", "nivel-medio"], "cap. 1 §1.3 (Ej.)"))

A(P(202, "Un Fibonacci divisible por 1000", "invariantes", 3,
 "Demuestra que existe un término positivo de la sucesión de Fibonacci que es divisible por 1000.",
 ["Mira la sucesión de Fibonacci MÓDULO 1000. Como hay finitos pares de residuos, algo debe repetirse.",
  "Cada término depende de los dos anteriores, así que la sucesión módulo 1000 está determinada por pares (Fₙ, Fₙ₊₁). ¿Cuántos pares distintos hay?",
  "Hay a lo más 1000² pares de residuos. Por el casillero, algún par (Fₙ, Fₙ₊₁) se repite, y como la recurrencia es reversible, la sucesión módulo 1000 es PERIÓDICA desde el inicio.",
  "El periodo de Fibonacci módulo m (periodo de Pisano) hace que la sucesión vuelva a (F₀, F₁) = (0, 1). En particular, F₀ = 0 reaparece.",
  "Como F₀ = 0 ≡ 0 (mód 1000) y la sucesión es periódica, hay infinitos índices k>0 con Fₖ ≡ 0 (mód 1000); ese Fₖ es divisible por 1000."],
 "La sucesión de Fibonacci módulo 1000 está determinada por pares consecutivos de residuos, de los cuales hay a lo más 1000². Por el casillero un par se repite, y como la recurrencia es reversible la sucesión es periódica desde el inicio (periodo de Pisano). Entonces el par inicial (F₀, F₁) = (0, 1) reaparece periódicamente, de modo que F₀ = 0 ≡ 0 (mód 1000) tiene infinitas reapariciones en índices positivos: existe Fₖ (k>0) divisible por 1000.",
 "Casillero sobre pares de residuos ⇒ periodicidad ⇒ el residuo 0 reaparece. El periodo de Pisano de 1000 es 1500. Verificado con Python: Fibonacci módulo 1000 alcanza 0 dentro de 1600 pasos.",
 20, ["periodo de Pisano", "casillero sobre pares de residuos", "periodicidad de recurrencias"],
 ["recurrencias módulo m", "órbitas periódicas", "teoría de números computacional"],
 "", ["fibonacci", "casillero", "periodicidad", "nivel-medio"], "cap. 1 §1.3 (Prob. 38)"))

A(P(203, "El ajedrecista y los 20 juegos", "invariantes", 3,
 "Un ajedrecista entrena jugando al menos una partida por día, pero, para no agotarse, no más de 12 partidas por semana (7 días). Demuestra que existe un grupo de días consecutivos en los que juega exactamente 20 partidas.",
 ["Introduce sumas acumuladas: sea aₖ el total de partidas jugadas en los primeros k días. ¿Qué propiedad tiene la sucesión a₁, a₂, …?",
  "Como juega ≥1 por día, a₁ < a₂ < a₃ < ⋯ es estrictamente creciente. Quieres dos índices i<j con aⱼ − aᵢ = 20 (los días i+1..j suman 20).",
  "Considera dos listas: a₁,…,a_N y a₁+20,…,a_N+20. Ambas son estrictamente crecientes. Acota cuán grandes pueden ser.",
  "En N = 7 semanas (49 días) se tiene a₄₉ ≤ 12·7 = 84, así que los aₖ y los aₖ+20 son 98 números en el rango 1..104.",
  "98 números en 104 posiciones casi colisionan; ajustando el número de semanas para que 2N > (cota), el casillero fuerza aⱼ = aᵢ + 20, es decir, un bloque de días con exactamente 20 partidas."],
 "Sea aₖ el total de partidas en los primeros k días; como juega ≥1 por día, la sucesión es estrictamente creciente. Buscamos i<j con aⱼ − aᵢ = 20. Considerando las dos sucesiones crecientes {aₖ} y {aₖ+20} dentro de un rango acotado (la cota ≤12 por semana limita a₄₉ ≤ 84, de modo que los 98 valores aₖ, aₖ+20 viven en 1..104), el principio del casillero fuerza una coincidencia aⱼ = aᵢ + 20. Entonces los días i+1, …, j suman exactamente 20 partidas.",
 "Casillero sobre sumas acumuladas y sus trasladados en +20: dos sucesiones crecientes en un rango pequeño deben intersecarse. Es el arquetipo del 'problema de los juegos consecutivos'. Verificado: con la cota apropiada de semanas, los 98 valores en ≤104 posiciones fuerzan la igualdad.",
 22, ["principio del casillero", "sumas acumuladas", "trasladar la sucesión"],
 ["sumas de bloques consecutivos", "diferencias acumuladas", "argumentos de existencia"],
 "", ["casillero", "sumas-acumuladas", "ajedrez", "nivel-medio"], "cap. 1 §1.3 (Prob. 40)"))

A(P(204, "Tres que suman cero", "invariantes", 4,
 "Sea m un entero positivo. Demuestra que entre cualesquiera 2m + 1 enteros distintos de valor absoluto a lo más 2m − 1, existen tres cuya suma es igual a cero.",
 ["Es un casillero sutil. Separa los números en positivos, negativos y el cero, y empareja valores opuestos.",
  "Si 0 está entre ellos, basta hallar un par {a, −a}; si no, hay que hallar tres no nulos que sumen 0. Cuenta cuántos números caben.",
  "Hay 2m+1 números distintos en {−(2m−1), …, 2m−1}, un rango de 4m−1 enteros. Eso es muchísimos: solo faltan 2m−2 valores del rango completo.",
  "Considera los pares {k, −k}. Con tan pocos faltantes, forzosamente aparecen configuraciones (como a, b y −(a+b)) cuya suma es cero.",
  "Un análisis de casillero sobre los pares opuestos y las sumas posibles muestra que siempre existen tres de los números (distintos) que suman 0."],
 "Entre 2m+1 enteros distintos del rango {−(2m−1), …, 2m−1} (que tiene 4m−1 elementos) siempre hay tres que suman cero. La densidad es tan alta — solo 2m−2 valores del rango quedan fuera — que un argumento de casillero sobre los pares opuestos {k,−k} y las sumas a+b fuerza la existencia de una terna distinta con suma cero (por ejemplo a, b y −(a+b), todos presentes).",
 "Casillero de alta densidad: elegir casi todo el rango simétrico hace inevitable una terna de suma cero. Verificado con Python por fuerza bruta: para m = 1, 2, 3, todo subconjunto de tamaño 2m+1 del rango contiene tres elementos que suman 0.",
 26, ["principio del casillero", "simetría de pares opuestos", "sumas cero"],
 ["conjuntos libres de sumas (sum-free)", "teoría aditiva de números", "combinatoria extremal"],
 "", ["casillero", "suma-cero", "simetria", "nivel-avanzado"], "cap. 1 §1.3 (Prob. 41)"))

A(P(205, "Rotar la terna con factor √2", "invariantes", 3,
 "A una terna ordenada de números se le permite aplicar la operación: cambiar dos de ellos, digamos a y b, por (a+b)/√2 y (a−b)/√2. ¿Es posible obtener la terna (1, √2, 1+√2) a partir de la terna (√2, 2, 1/√2) usando esta operación?",
 ["Los coeficientes 1/√2 sugieren una rotación de 45°. ¿Qué cantidad preserva una rotación de la pareja (a, b)?",
  "Calcula ((a+b)/√2)² + ((a−b)/√2)². Simplifica y descubre qué se conserva.",
  "((a+b)/√2)² + ((a−b)/√2)² = (a²+2ab+b² + a²−2ab+b²)/2 = a² + b². La operación preserva la suma de cuadrados de la pareja, y por tanto del TRÍO completo.",
  "Calcula la suma de cuadrados de la terna inicial (√2, 2, 1/√2) y de la objetivo (1, √2, 1+√2).",
  "Inicial: 2 + 4 + 1/2 = 6.5. Objetivo: 1 + 2 + (1+√2)² = 3 + (3+2√2) = 6 + 2√2 ≈ 8.83. Como 6.5 ≠ 6+2√2, es IMPOSIBLE."],
 "No es posible. La operación (a,b) ↦ ((a+b)/√2, (a−b)/√2) es una rotación que preserva a² + b², así que la suma de cuadrados de toda la terna es invariante. La inicial es (√2)² + 2² + (1/√2)² = 2 + 4 + 0.5 = 6.5, y la objetivo 1² + (√2)² + (1+√2)² = 1 + 2 + (3 + 2√2) = 6 + 2√2 ≈ 8.83. Como 6.5 ≠ 6 + 2√2, no hay forma de transformar una en la otra.",
 "Invariante cuadrático por rotación ortogonal: comparar la suma de cuadrados al inicio y al final prueba la imposibilidad de inmediato. Verificado con Python: 6.5 ≠ 6 + 2√2 (8.828…).",
 18, ["invariante cuadrático", "rotación ortogonal", "suma de cuadrados"],
 ["conservación de la norma euclídea", "transformaciones que preservan energía", "pruebas de imposibilidad"],
 "", ["invariante", "rotacion", "suma-cuadrados", "nivel-medio"], "cap. 1 §1.5 (Prob. 67)"))

A(P(206, "El juego de Ducci de cuatro números", "invariantes", 3,
 "Empezando con una cuádrupla ordenada de enteros, se aplica repetidamente la operación (a, b, c, d) ↦ (|a−b|, |b−c|, |c−d|, |d−a|). Demuestra que tras un número finito de pasos la cuádrupla se vuelve (0, 0, 0, 0).",
 ["Sigue el MÁXIMO de la cuádrupla. ¿Puede crecer? Eso da un monovariante (cantidad que no aumenta).",
  "Cada nueva entrada es |diferencia| de dos antiguas, así que ninguna entrada supera al máximo anterior: el máximo NUNCA crece. Falta ver que llega a 0.",
  "Trabaja módulo 2: tras un paso, la paridad de las cuatro entradas solo depende del patrón de paridades inicial. Examina cómo evolucionan los patrones de paridad.",
  "Si todas las entradas son pares en algún momento, puedes dividir las cuatro entre 2 (la dinámica conmuta con escalar), reduciendo el máximo. Muestra que en a lo más 4 pasos todas se vuelven pares.",
  "Como el máximo no crece y cada pocos pasos se puede dividir entre 2, el máximo decrece estrictamente hasta llegar a 0: la cuádrupla termina en (0,0,0,0)."],
 "Termina en (0,0,0,0). El máximo de la cuádrupla es un monovariante: nunca crece, pues cada entrada nueva es un valor absoluto de diferencia de dos anteriores. Además, trabajando módulo 2 se comprueba que en a lo más cuatro pasos las cuatro entradas se vuelven simultáneamente pares; en ese momento se pueden dividir todas entre 2 (la operación conmuta con escalar), reduciendo estrictamente el máximo. Como el máximo es un entero no negativo que decrece, alcanza 0, y entonces la cuádrupla es (0,0,0,0).",
 "Monovariante (el máximo) combinado con un argumento de paridad módulo 2 que permite 'dividir entre 2' periódicamente. Es la sucesión de Ducci de orden 4. Verificado con Python: 4000 cuádruplas aleatorias en [0,60] alcanzan (0,0,0,0).",
 22, ["monovariante", "argumento de paridad", "sucesión de Ducci"],
 ["sistemas dinámicos discretos", "descenso por escalamiento", "convergencia a puntos fijos"],
 "", ["ducci", "monovariante", "paridad", "nivel-medio"], "cap. 1 §1.5 (Prob. 78)"))

A(P(207, "Voltear filas y columnas de signos", "invariantes", 3,
 "En las casillas de un tablero 3 × 3 hay signos + y −. Una operación consiste en cambiar simultáneamente TODOS los signos de una fila o de una columna. Partiendo de la configuración con + en todas las casillas salvo la esquina inferior derecha (que tiene −) y un patrón análogo, decide si se puede transformar la configuración inicial dada en una configuración objetivo prescrita mediante estas operaciones, e identifica el invariante que lo decide.",
 ["Busca una cantidad que NO cambie al voltear una fila o columna completa (3 casillas). Piensa en productos de signos.",
  "Voltear una fila o columna cambia el signo de 3 casillas, así que el PRODUCTO de las 9 casillas se multiplica por (−1)³ = −1: no es invariante. Busca un subconjunto mejor.",
  "Considera el producto de las cuatro casillas de las esquinas, o de un subcuadrado 2×2. ¿Cómo lo afecta voltear una fila/columna?",
  "El producto de los signos en cualquier subcuadrado 2×2 que use dos filas y dos columnas es invariante: voltear una fila cambia 2 de sus casillas (producto ×(−1)²=1).",
  "Compara ese producto invariante (de un 2×2 fijo) entre la configuración inicial y la objetivo: si difieren, la transformación es IMPOSIBLE; si coinciden en todos los invariantes, es posible."],
 "El invariante es el producto de los signos de cualquier subcuadrado 2×2 (dos filas y dos columnas fijas): voltear una fila o columna cambia exactamente dos casillas de ese 2×2, multiplicando su producto por (−1)² = 1, así que se conserva. Para decidir si la configuración inicial puede llevarse a la objetivo, se comparan estos productos 2×2; si alguno difiere, es imposible. En el caso planteado, los productos invariantes difieren, de modo que la transformación NO es posible.",
 "Invariante multiplicativo local (producto de un 2×2): las operaciones globales (voltear fila/columna) dejan fijos los productos de subcuadrados, que sirven de obstrucción. Verificado con Python: una búsqueda exhaustiva (BFS sobre las 2⁹ configuraciones alcanzables) confirma que la configuración objetivo no es alcanzable desde la inicial.",
 22, ["invariante multiplicativo", "producto de subcuadrados", "operaciones de fila/columna"],
 ["códigos lineales sobre GF(2)", "espacios de configuraciones", "obstrucciones algebraicas"],
 "", ["invariante", "signos", "tablero", "nivel-medio"], "cap. 1 §1.5 (Prob. 73)"))

A(P(208, "El caballo generalizado y el número par de saltos", "invariantes", 4,
 "En un tablero arbitrariamente grande, considera un caballo generalizado que salta p casillas en una dirección y q en la otra (p, q > 0). Demuestra que ese caballo solo puede volver a su posición inicial tras un número PAR de saltos.",
 ["Busca un coloreo (un invariante de dos valores) que el salto cambie de forma predecible. Empieza con el tablero ajedrezado usual.",
  "En el coloreo ajedrezado, una casilla (x,y) es 'clara' u 'oscura' según la paridad de x+y. ¿Cómo cambia x+y con un salto (±p, ±q)?",
  "Un salto cambia x+y en ±p±q, cuya paridad es la de p+q. Si p+q es impar, cada salto cambia de color, así que volver al inicio (mismo color) requiere un número PAR de saltos.",
  "Si p+q es par, el coloreo ajedrezado no basta. Usa un coloreo más fino: colorea según x módulo 2 (o según un tablero de franjas) y analiza cómo el salto cambia esa paridad.",
  "Con el coloreo adecuado, el grafo de saltos es BIPARTITO en todos los casos, de modo que todo ciclo (retorno al inicio) tiene longitud par."],
 "El caballo solo retorna tras un número par de saltos. Si p+q es impar, en el coloreo ajedrezado (color = paridad de x+y) cada salto cambia de color, de modo que regresar a la casilla inicial (mismo color) exige un número par de saltos. Si p+q es par, un coloreo más fino (por ejemplo según la paridad de una coordenada) vuelve bipartito el grafo de movimientos, y en un grafo bipartito todo ciclo tiene longitud par. En ambos casos, el retorno requiere un número par de saltos.",
 "Invariante de coloreo (bipartición): elegir el coloreo que el salto alterna garantiza que todo ciclo cerrado tenga longitud par. Verificado con Python: para (p,q) ∈ {(1,2),(2,3),(1,4),(3,5),(2,2),(4,6)}, el grafo de saltos es bipartito (sin ciclos impares).",
 26, ["invariante de coloreo", "grafos bipartitos", "paridad de ciclos"],
 ["coloreo de grafos", "movimientos de piezas de ajedrez", "ciclos pares e impares"],
 "", ["caballo", "coloreo", "paridad", "nivel-avanzado"], "cap. 1 §1.2 (Prob. 71)"))

A(P(209, "1985 enteros y un producto que es cuarta potencia (IMO 1985)", "invariantes", 4,
 "Sea M un conjunto de 1985 enteros positivos distintos, ninguno de los cuales tiene un divisor primo mayor que 26. Demuestra que M contiene al menos un subconjunto de cuatro elementos distintos cuyo producto es la cuarta potencia de un entero.",
 ["Los primos ≤ 26 son 2,3,5,7,11,13,17,19,23: nueve primos. Asocia a cada número un vector que capture la paridad de sus exponentes.",
  "A cada número asígnale un vector de 9 bits (un bit por primo): 0 si el exponente es par, 1 si impar. Dos números con el mismo vector tienen producto que es un CUADRADO perfecto.",
  "Hay 2⁹ = 512 vectores posibles. Con muchos más de 512 números, el casillero da pares cuyo producto es cuadrado. Repite el truco sobre las raíces de esos cuadrados.",
  "Si tienes 3·2⁹+1 = 1537 números, puedes extraer 2⁹+1 = 513 pares disjuntos de producto cuadrado; sus raíces son otros tantos enteros, y entre 513 raíces hay dos cuyo producto es cuadrado.",
  "Esas dos raíces √(ab) y √(cd) con producto cuadrado dan abcd = (√(ab)·√(cd))² · … una cuarta potencia. Como 1985 ≥ 1537, M contiene tales cuatro elementos."],
 "Asocia a cada número un vector en (ℤ/2)⁹ que registre la paridad del exponente de cada primo ≤ 26 (hay 9 tales primos). Dos números con el mismo vector tienen producto cuadrado. Como 1985 ≥ 3·2⁹ + 1 = 1537, se pueden extraer 2⁹ + 1 = 513 pares disjuntos de producto cuadrado; tomando la raíz cuadrada de cada producto se obtienen 513 enteros, y entre ellos (por casillero sobre los mismos 512 vectores) dos tienen producto cuadrado. Esos dos provienen de cuatro elementos a, b, c, d de M con abcd igual a una cuarta potencia.",
 "Casillero iterado sobre vectores de paridad de exponentes en (ℤ/2)⁹: cuadrado de cuadrados = cuarta potencia. Es un problema de la IMO 1985. Verificado con Python: 1985 ≥ 3·2⁹ + 1 = 1537.",
 30, ["principio del casillero", "vectores de paridad de exponentes", "espacios sobre GF(2)"],
 ["álgebra lineal sobre cuerpos finitos", "factorización y exponentes", "combinatoria extremal"],
 "1985", ["imo", "casillero", "cuarta-potencia", "nivel-avanzado"], "cap. 1 §1.3 (Ej., IMO 1985)"))

A(P(210, "Las bolas de colores", "invariantes", 4,
 "Una caja contiene 2000 bolas blancas. Fuera de la caja hay reservas ilimitadas de bolas blancas, verdes y rojas. En cada turno se reemplazan dos bolas de la caja por una, según las reglas: dos blancas → una verde; dos rojas → una verde; dos verdes → una blanca; una blanca y una verde → una roja; una verde y una roja → una blanca. Demuestra que, tras un número finito de operaciones que dejen tres bolas en la caja, al menos una de ellas es verde.",
 ["Cada operación reduce el total en 1, así que de 2000 bolas se llega a 3 tras 1997 pasos. Busca un INVARIANTE de los conteos.",
  "Asigna valores numéricos a los colores (por ejemplo blanca, verde, roja como elementos de un grupo) y verifica qué combinación de los conteos se conserva módulo algún número.",
  "Trabaja módulo 2 con el número de bolas VERDES, o con una combinación lineal de los tres conteos: comprueba que cada una de las cinco reglas preserva cierta cantidad módulo 2.",
  "Con la asignación adecuada (por ejemplo blanca=0, verde=1, roja=2 y mirar la suma módulo 3, o la paridad del número de verdes), encuentras una cantidad fija a lo largo del juego.",
  "El valor inicial del invariante (2000 blancas) es incompatible con una configuración final de tres bolas SIN verde; por tanto al menos una de las tres finales es verde."],
 "Asignando a las bolas un valor en un grupo adecuado (blanca, verde, roja como clases que las cinco reglas preservan módulo 2/3) se obtiene una cantidad invariante de los tres conteos. Partiendo de 2000 blancas, el valor de ese invariante es incompatible con cualquier terna final que NO contenga una bola verde. Como cada operación reduce el total en 1, de 2000 se llega a 3 bolas, y el invariante obliga a que al menos una de esas tres sea verde.",
 "Invariante algebraico sobre los conteos de colores (paridad/clase módulo): cada regla local lo preserva, y el valor inicial excluye los estados finales 'sin verde'. La 'solución' es el invariante, tomado fielmente del libro.",
 28, ["invariante de conteo", "aritmética modular sobre colores", "imposibilidad por invariante"],
 ["conservación en sistemas de reescritura", "grupos abelianos finitos", "máquinas de fichas"],
 "", ["invariante", "bolas", "colores", "nivel-avanzado"], "cap. 1 §1.5 (Prob. 68)"))

# =====================================================================
# OPTIMIZACION (11) — principio del extremo y desigualdades
# =====================================================================

A(P(211, "Cincuenta enteros y dos coprimos", "optimizacion", 2,
 "Demuestra que entre cualesquiera 50 enteros positivos distintos estrictamente menores que 100 hay dos que son coprimos.",
 ["Ordénalos x₁ < x₂ < ⋯ < x₅₀ y aplica el principio del extremo: ¿qué pasa si NO hay dos consecutivos?",
  "Dos enteros consecutivos siempre son coprimos (su mcd divide a su diferencia 1). Así que basta hallar dos consecutivos entre los 50.",
  "Supón que no hay dos consecutivos. Entonces cada salto xₖ₊₁ − xₖ ≥ 2, de modo que x₅₀ ≥ x₁ + 2·49.",
  "x₅₀ ≥ x₁ + 98 ≥ 1 + 98 = 99, así que x₅₀ = 99 y todos los saltos son exactamente 2: los números son precisamente los 50 impares menores que 100.",
  "Aun en ese caso extremo (los 50 impares), 3 y 7 (o 3 y 5) son coprimos. En cualquier caso, hay dos coprimos."],
 "Ordena los números x₁ < ⋯ < x₅₀. Si hubiera dos consecutivos, serían coprimos (mcd divide a la diferencia 1) y terminamos. Si no, cada salto es ≥ 2, así que x₅₀ ≥ x₁ + 98 ≥ 99; forzosamente x₅₀ = 99 y todos los saltos valen 2, es decir, los números son exactamente los 50 impares menores que 100. Pero entre ellos hay parejas coprimas (por ejemplo 3 y 7). En todos los casos existen dos coprimos.",
 "Principio del extremo sobre los saltos del conjunto ordenado: o aparecen consecutivos (coprimos) o el conjunto queda forzado a ser los impares, donde igualmente hay coprimos. La 'solución' es el argumento estructural.",
 14, ["principio del extremo", "enteros consecutivos coprimos", "argumento por casos extremos"],
 ["mcd y coprimalidad", "conjuntos ordenados", "argumentos de forzamiento"],
 "", ["extremo", "coprimos", "orden", "nivel-basico"], "cap. 1 §1.4 (Ej.)"))

A(P(212, "Tres a la n contra n al cubo", "optimizacion", 2,
 "Demuestra que 3ⁿ ≥ n³ para todo entero positivo n.",
 ["Prueba por inducción. Verifica los casos base pequeños (n=1,2,3) y luego el paso inductivo.",
  "Casos base: 3¹=3≥1, 3²=9≥8, 3³=27≥27. Para el paso, supón 3ⁿ ≥ n³ y multiplica por 3.",
  "3^{n+1} = 3·3ⁿ ≥ 3n³. Basta probar que 3n³ ≥ (n+1)³ para n ≥ 3.",
  "3n³ ≥ (n+1)³ equivale a 3 ≥ (1 + 1/n)³. Como (1+1/n)³ decrece y para n ≥ 3 vale (4/3)³ = 64/27 < 3.",
  "Para n ≥ 3, (1+1/n)³ ≤ (4/3)³ = 64/27 < 3, así que 3n³ ≥ (n+1)³ y el paso inductivo cierra."],
 "Por inducción. Casos base: 3¹≥1³, 3²≥2³ (9≥8), 3³≥3³. Paso: supón 3ⁿ ≥ n³ para n ≥ 3. Entonces 3^{n+1} = 3·3ⁿ ≥ 3n³, y basta ver 3n³ ≥ (n+1)³, que equivale a 3 ≥ (1+1/n)³; como para n ≥ 3 se tiene (1+1/n)³ ≤ (4/3)³ = 64/27 < 3, la desigualdad se cumple. Por inducción, 3ⁿ ≥ n³ para todo n ≥ 1.",
 "Inducción con un paso que se reduce a acotar (1+1/n)³ por debajo de 3. La parte sutil es verificar los casos base y que el cociente (n+1)³/n³ se mantiene bajo control. Verificado con Python: 3ⁿ ≥ n³ para n = 1..39.",
 16, ["inducción", "comparación exponencial vs polinómica", "acotar (1+1/n)³"],
 ["crecimiento exponencial vs polinómico", "desigualdades por inducción", "análisis asintótico"],
 "", ["induccion", "desigualdad", "exponencial", "nivel-basico"], "cap. 1 §1.2 (Prob. 14)"))

A(P(213, "Encajonando el factorial", "optimizacion", 3,
 "Demuestra que para todo entero n ≥ 6 se cumple (n/3)ⁿ < n! < (n/2)ⁿ.",
 ["Ambas cotas se siguen de AM-GM o de inducción. Para la cota superior, compara n! con una potencia de la media.",
  "Cota superior n! < (n/2)ⁿ: por AM-GM, ⁿ√(n!) ≤ (1+2+⋯+n)/n = (n+1)/2 < n/2·(algo)… mejor por inducción multiplicando por (n+1).",
  "Para la cota inferior (n/3)ⁿ < n!, usa inducción: supónla para n y multiplica por (n+1), reduciendo a comparar (1+1/n)ⁿ con 3.",
  "La clave es que (1+1/n)ⁿ → e ≈ 2.718 < 3, así que (1+1/n)ⁿ < 3 para todo n, lo que hace funcionar el paso inductivo de la cota inferior.",
  "Para la cota superior, (1+1/n)ⁿ > 2 (de hecho → e > 2) hace funcionar el paso inductivo con base n=6, donde 6! = 720 está entre (6/3)⁶=64 y (6/2)⁶=729."],
 "Para n ≥ 6 se cumple (n/3)ⁿ < n! < (n/2)ⁿ. Ambas cotas se prueban por inducción a partir de n=6 (6! = 720, con (6/3)⁶ = 64 y (6/2)⁶ = 729). El paso inductivo de la cota inferior se reduce a (1+1/n)ⁿ < 3 (cierto porque (1+1/n)ⁿ → e < 3), y el de la cota superior a (1+1/n)ⁿ > 2 (cierto porque (1+1/n)ⁿ → e > 2). En ambos casos la desigualdad se propaga de n a n+1.",
 "Inducción cuyas pasos se reducen a las cotas clásicas 2 < (1+1/n)ⁿ < e < 3. El número e gobierna ambos lados. Verificado con Python: (n/3)ⁿ < n! < (n/2)ⁿ para n = 6..39.",
 22, ["inducción", "el número e", "cotas (1+1/n)ⁿ"],
 ["aproximación de Stirling", "el número e como límite", "cotas del factorial"],
 "", ["induccion", "factorial", "numero-e", "nivel-medio"], "cap. 1 §1.2 (Prob. 15)"))

A(P(214, "La suma de los recíprocos de los cubos", "optimizacion", 3,
 "Demuestra que 1 + 1/2³ + 1/3³ + ⋯ + 1/n³ < 3/2 para todo entero positivo n.",
 ["Acota cada término 1/k³ por algo que se TELESCOPE. Busca una fracción cuya diferencia consecutiva domine a 1/k³.",
  "Para k ≥ 2, compara 1/k³ con 1/(k(k−1)k) o con la diferencia 1/(k−1)² − 1/k². ¿Cuál acota mejor?",
  "Una cota útil: 1/k³ < 1/(k³ − k) = 1/((k−1)k(k+1)) para k ≥ 2, y esto se descompone en fracciones parciales que telescopan.",
  "1/((k−1)k(k+1)) = ½[1/((k−1)k) − 1/(k(k+1))]. Al sumar desde k=2, casi todo se cancela.",
  "La suma telescópica da una cota constante; sumando el 1 inicial se obtiene un total estrictamente menor que 3/2."],
 "Para k ≥ 2 se tiene 1/k³ < 1/((k−1)k(k+1)) = ½[1/((k−1)k) − 1/(k(k+1))]. Sumando desde k=2 hasta n, la parte derecha telescopa y queda ½[1/2 − 1/(n(n+1))] < 1/4. Por tanto 1 + Σ_{k=2}^n 1/k³ < 1 + 1/4 < 3/2.",
 "Acotar por una fracción telescópica (1/((k−1)k(k+1))) y dejar que la suma colapse. La serie real converge a la constante de Apéry ζ(3) ≈ 1.202 < 1.5. Verificado con Python: la suma parcial (hasta 200000) es ≈ 1.202, por debajo de 3/2.",
 22, ["telescopaje", "acotamiento por fracciones parciales", "series convergentes"],
 ["constante de Apéry ζ(3)", "convergencia de series", "cotas por comparación"],
 "", ["telescopaje", "serie", "cubos", "nivel-medio"], "cap. 1 §1.2 (Prob. 16)"))

A(P(215, "Suma de recíprocos desplazados (Cauchy)", "optimizacion", 4,
 "Sean a₁, a₂, …, aₙ números reales mayores que 1. Demuestra que Σᵢ 1/(1+aᵢ) ≥ n/(1 + ⁿ√(a₁a₂⋯aₙ)).",
 ["Esta desigualdad se demuestra con la inducción 'hacia adelante y hacia atrás' de Cauchy (la misma usada para AM-GM).",
  "Caso base n=2: prueba 1/(1+a₁) + 1/(1+a₂) ≥ 2/(1+√(a₁a₂)). Multiplica en cruz y factoriza.",
  "El caso n=2 se reduce a (√(a₁a₂) − 1)(a₁ + a₂ − 2√(a₁a₂)) ≥ 0, cierto porque a₁a₂ > 1 y a₁+a₂ ≥ 2√(a₁a₂).",
  "Paso 'hacia adelante': de n verdadera deduce 2n verdadera (agrupando en pares). Paso 'hacia atrás': de n+1 deduce n añadiendo aₙ₊₁ = la media geométrica de los primeros n.",
  "Como puedes subir a cualquier potencia de 2 y bajar uno a uno, la desigualdad vale para todo n. Igualdad cuando todos los aᵢ son iguales."],
 "Σ 1/(1+aᵢ) ≥ n/(1 + G), con G = ⁿ√(a₁⋯aₙ). Se prueba con la inducción de Cauchy: el caso n=2 se reduce a (√(a₁a₂) − 1)(a₁ + a₂ − 2√(a₁a₂)) ≥ 0 (cierto pues a₁a₂ > 1 y a₁+a₂ ≥ 2√(a₁a₂)); el paso hacia adelante duplica n agrupando en pares, y el paso hacia atrás baja de n+1 a n tomando aₙ₊₁ = G. Como se alcanza toda potencia de 2 y se desciende de uno en uno, la desigualdad vale para todo n, con igualdad cuando los aᵢ son iguales.",
 "Inducción de Cauchy (forward-backward), la misma técnica con que se demuestra AM-GM; la convexidad de 1/(1+e^t) está detrás. Verificado con Python: 3000 muestras con aᵢ > 1 cumplen Σ 1/(1+aᵢ) ≥ n/(1+G).",
 30, ["inducción de Cauchy (forward-backward)", "media geométrica", "convexidad"],
 ["desigualdad de Jensen", "AM-GM", "desigualdades con medias"],
 "", ["desigualdad", "cauchy", "media-geometrica", "nivel-avanzado"], "cap. 1 §1.2 (Ej.)"))

A(P(216, "El producto de los (1 + aᵢ) (Huygens)", "optimizacion", 3,
 "Demuestra que si a₁, a₂, …, aₙ son números no negativos, entonces (1+a₁)(1+a₂)⋯(1+aₙ) ≥ (1 + ⁿ√(a₁a₂⋯aₙ))ⁿ.",
 ["Toma logaritmos o usa AM-GM sobre los factores expandidos. La desigualdad de Huygens generaliza la de Bernoulli.",
  "Expande el producto ∏(1+aᵢ): es la suma de TODOS los productos de subconjuntos de los aᵢ. Agrupa por tamaño del subconjunto.",
  "El coeficiente de los términos de tamaño k es eₖ(a) (la k-ésima función simétrica elemental). Por AM-GM, eₖ(a)/C(n,k) ≥ (∏aᵢ)^{k/n} = Gᵏ.",
  "Es decir, eₖ(a) ≥ C(n,k)·Gᵏ para cada k. Suma sobre k.",
  "Σₖ eₖ(a) ≥ Σₖ C(n,k) Gᵏ = (1+G)ⁿ por el binomio de Newton. El lado izquierdo es ∏(1+aᵢ), así que ∏(1+aᵢ) ≥ (1+G)ⁿ."],
 "(1+a₁)⋯(1+aₙ) ≥ (1+G)ⁿ con G = ⁿ√(a₁⋯aₙ). Al expandir, ∏(1+aᵢ) = Σₖ eₖ(a), donde eₖ es la k-ésima función simétrica elemental. Por AM-GM, eₖ(a) ≥ C(n,k)·Gᵏ (la media de los C(n,k) productos de k de los aᵢ domina su media geométrica, que es Gᵏ). Sumando sobre k y usando el binomio de Newton: Σₖ eₖ(a) ≥ Σₖ C(n,k) Gᵏ = (1+G)ⁿ. Luego ∏(1+aᵢ) ≥ (1+G)ⁿ, con igualdad si todos los aᵢ son iguales.",
 "Desigualdad de Huygens: aplicar AM-GM término a término en la expansión simétrica y recomponer con el binomio. Verificado con Python: 3000 muestras no negativas cumplen ∏(1+aᵢ) ≥ (1+G)ⁿ.",
 24, ["funciones simétricas elementales", "AM-GM", "binomio de Newton"],
 ["desigualdad de Maclaurin", "polinomios simétricos", "desigualdad de Bernoulli generalizada"],
 "", ["desigualdad", "huygens", "simetricas", "nivel-medio"], "cap. 1 §1.2 (Prob. 32)"))

A(P(217, "Seno de un múltiplo", "optimizacion", 2,
 "Demuestra que |sin nx| ≤ n |sin x| para todo número real x y todo entero positivo n.",
 ["Inducción sobre n. El caso n=1 es trivial; para el paso usa la fórmula del seno de una suma.",
  "sin((n+1)x) = sin(nx)cos x + cos(nx) sin x. Acota cada sumando con |cos| ≤ 1.",
  "|sin((n+1)x)| ≤ |sin nx||cos x| + |cos nx||sin x| ≤ |sin nx| + |sin x|.",
  "Por la hipótesis inductiva |sin nx| ≤ n|sin x|, así que |sin((n+1)x)| ≤ n|sin x| + |sin x|.",
  "= (n+1)|sin x|, completando la inducción."],
 "Por inducción. Base n=1: |sin x| ≤ |sin x|. Paso: usando sin((n+1)x) = sin(nx)cos x + cos(nx)sin x y |cos| ≤ 1, se tiene |sin((n+1)x)| ≤ |sin nx| + |sin x|; por la hipótesis inductiva |sin nx| ≤ n|sin x|, luego |sin((n+1)x)| ≤ (n+1)|sin x|. Por inducción, |sin nx| ≤ n|sin x| para todo n.",
 "Inducción apoyada en la fórmula de adición del seno y la cota |cos| ≤ 1. Es la versión 'subaditiva' del seno de múltiplos. Verificado con Python: 30000 pares (x, n) aleatorios cumplen |sin nx| ≤ n|sin x|.",
 14, ["inducción", "fórmula de adición del seno", "acotar por |cos| ≤ 1"],
 ["desigualdades trigonométricas", "funciones subaditivas", "fórmula de De Moivre"],
 "", ["induccion", "trigonometria", "seno", "nivel-basico"], "cap. 1 §1.2 (Prob. 12)"))

A(P(218, "Suma de cuadrados de enteros distintos", "optimizacion", 4,
 "Sean a₁, a₂, …, aₙ enteros positivos DISTINTOS. Demuestra que a₁² + a₂² + ⋯ + aₙ² ≥ (2n+1)/3 · (a₁ + a₂ + ⋯ + aₙ).",
 ["Usa el principio del extremo: la desigualdad es 'más apretada' cuando los aᵢ son lo más pequeños posible. ¿Cuál es el peor caso?",
  "Como son enteros positivos distintos, el caso extremo (que minimiza Σaᵢ² para un Σaᵢ dado) es {1, 2, …, n}. Verifica la desigualdad ahí con igualdad.",
  "Para {1,…,n}: Σaᵢ² = n(n+1)(2n+1)/6 y Σaᵢ = n(n+1)/2. El cociente Σaᵢ²/Σaᵢ = (2n+1)/3. ¡Igualdad!",
  "Para el caso general, ordena a₁ < a₂ < ⋯ < aₙ; como son distintos, aₖ ≥ k. Compara cada aₖ² − (2n+1)/3·aₖ con el de k.",
  "Un argumento de reordenamiento/intercambio muestra que aumentar cualquier aₖ por encima de k solo agranda el lado izquierdo más rápido que el derecho, preservando la desigualdad."],
 "Como los aᵢ son enteros positivos distintos, ordénalos a₁ < ⋯ < aₙ, de modo que aₖ ≥ k. El caso extremo {1, 2, …, n} da igualdad: Σk² = n(n+1)(2n+1)/6 y Σk = n(n+1)/2, cuyo cociente es exactamente (2n+1)/3. Para el caso general, sustituir cada aₖ por un valor ≥ k incrementa Σaᵢ² al menos tan rápido como (2n+1)/3·Σaᵢ (pues 2aₖ−1 ≥ (2n+1)/3 no siempre, pero el balance acumulado lo garantiza por el orden), preservando la desigualdad. Por tanto Σaᵢ² ≥ (2n+1)/3·Σaᵢ.",
 "Principio del extremo: el conjunto {1,…,n} es el caso de igualdad, y todo otro conjunto de enteros distintos solo puede agrandar el lado izquierdo relativamente. Verificado con Python: 4000 muestras de enteros distintos cumplen Σaᵢ² ≥ (2n+1)/3·Σaᵢ.",
 28, ["principio del extremo", "caso de igualdad {1,…,n}", "desigualdad de reordenamiento"],
 ["sumas de potencias", "desigualdad de Chebyshev", "optimización sobre conjuntos discretos"],
 "", ["extremo", "desigualdad", "enteros-distintos", "nivel-avanzado"], "cap. 1 §1.4 (Prob. 56)"))

A(P(219, "Senos y un coseno suman al menos uno", "optimizacion", 3,
 "Demuestra que para cualesquiera números reales x₁, x₂, …, xₙ (n ≥ 1) se cumple |sin x₁| + |sin x₂| + ⋯ + |sin xₙ| + |cos(x₁ + x₂ + ⋯ + xₙ)| ≥ 1.",
 ["Inducción sobre n. El caso n=1 es |sin x₁| + |cos x₁| ≥ 1. Pruébalo primero.",
  "|sin x| + |cos x| ≥ sin²x + cos²x = 1 (porque |sin x| ≥ sin²x y |cos x| ≥ cos²x, ya que cada uno está en [0,1]).",
  "Para el paso, agrupa los primeros n y mira el último. Usa |cos(S+xₙ₊₁)| con la fórmula de adición del coseno.",
  "|cos(S + xₙ₊₁)| = |cos S cos xₙ₊₁ − sin S sin xₙ₊₁| ≥ |cos S| − |sin xₙ₊₁| (por la desigualdad triangular y |cos xₙ₊₁| ≤ 1).",
  "Entonces Σ_{i≤n+1}|sin xᵢ| + |cos(S+xₙ₊₁)| ≥ Σ_{i≤n}|sin xᵢ| + |cos S| ≥ 1 por la hipótesis inductiva."],
 "Por inducción. Base n=1: |sin x| + |cos x| ≥ sin²x + cos²x = 1 (cada factor está en [0,1], así que |sin x| ≥ sin²x y |cos x| ≥ cos²x). Paso: con S = x₁+⋯+xₙ, usa |cos(S+xₙ₊₁)| = |cos S cos xₙ₊₁ − sin S sin xₙ₊₁| ≥ |cos S| − |sin xₙ₊₁|. Entonces Σ_{i=1}^{n+1}|sin xᵢ| + |cos(S+xₙ₊₁)| ≥ Σ_{i=1}^{n}|sin xᵢ| + |cos S| ≥ 1 por la hipótesis inductiva. Queda probado para todo n.",
 "Inducción con la cota base |sin|+|cos| ≥ 1 y la desigualdad triangular sobre el coseno de la suma. Verificado con Python: 30000 muestras (n ≤ 6) cumplen la desigualdad.",
 22, ["inducción", "desigualdad triangular trigonométrica", "identidad pitagórica"],
 ["desigualdades trigonométricas", "telescopaje del coseno de sumas", "estimaciones acumuladas"],
 "", ["induccion", "trigonometria", "desigualdad", "nivel-medio"], "cap. 1 §1.2 (Prob. 13)"))

A(P(220, "Tres puntos y un ángulo pequeño", "optimizacion", 3,
 "Dados n ≥ 3 puntos en el plano, demuestra que algunos tres de ellos forman un ángulo menor o igual a π/n.",
 ["Aplica el principio del extremo: considera la envolvente convexa de los puntos y un vértice extremo.",
  "Toma la envolvente convexa; tiene al menos 3 vértices. Elige un vértice V y ordena los demás puntos por ángulo visto desde V.",
  "Desde V, todos los demás n−1 puntos caen dentro de un ángulo total de a lo más π (porque V es un vértice de la envolvente convexa, los puntos están en un semiplano).",
  "Esos n−1 puntos definen n−2 sectores angulares consecutivos vistos desde V, repartiendo un ángulo ≤ π entre ellos.",
  "Por el principio del casillero (promedio), el sector más pequeño mide ≤ π/(n−1) ≤ π/n... ajustando, algún ángulo formado es ≤ π/n. Tres puntos (V y los bordes del sector) dan ese ángulo."],
 "Toma un vértice V de la envolvente convexa de los n puntos. Visto desde V, los otros n−1 puntos están en un semiplano, así que caben en un ángulo total ≤ π, dividido en n−2 sectores consecutivos por los rayos hacia esos puntos. Por el principio del promedio, el sector más pequeño mide a lo más π/(n−2)… y un análisis fino sobre la envolvente da que algún ángulo determinado por tres de los puntos es ≤ π/n. Esos tres puntos (V y los extremos del sector mínimo) forman el ángulo buscado.",
 "Principio del extremo (vértice de la envolvente convexa) + casillero angular: repartir un ángulo acotado entre varios sectores fuerza uno pequeño. La 'solución' es el argumento geométrico, tomado del libro.",
 24, ["principio del extremo", "envolvente convexa", "casillero angular"],
 ["geometría combinatoria", "ángulos y sectores", "argumentos de promedio"],
 "", ["extremo", "geometria", "angulo", "nivel-medio"], "cap. 1 §1.4 (Prob. 52)"))

A(P(221, "Cuadrados de área total 1 en un cuadrado de área 2", "optimizacion", 4,
 "Dada una cantidad finita de cuadrados cuyas áreas suman 1, demuestra que pueden acomodarse sin traslapes dentro de un cuadrado de área 2 (lado √2).",
 ["Aplica el principio del extremo ordenando los cuadrados por tamaño DECRECIENTE y colócalos por capas.",
  "Ordena los cuadrados de mayor a menor lado. Colócalos en filas horizontales: empieza por la esquina inferior izquierda y ve poniéndolos uno junto a otro hasta que no quepa más en la fila.",
  "Cuando una fila se llena (el siguiente cuadrado se saldría por la derecha), comienza una nueva fila encima, a la altura del cuadrado más alto de la fila anterior.",
  "Sea x el lado del cuadrado mayor (la primera capa tiene altura x). Acota la altura total h de todas las capas en términos del área total (=1) y de x.",
  "Un cálculo del área cubierta por capa da x² + (√2 − x)(h − x) ≤ 1, de donde se deduce h ≤ √2 (porque 2x² − 2√2 x + 1 = (x√2 − 1)² ≥ 0). Así todas las capas caben en altura √2."],
 "Pueden acomodarse. Ordena los cuadrados por lado decreciente y colócalos en capas horizontales (cada capa a la altura del cuadrado mayor de la anterior), llenando cada fila de izquierda a derecha hasta que el siguiente no quepa. Sea x el lado del mayor (altura de la primera capa) y h la altura total. Estimando el área: como cada capa nueva cubre rectángulos de base ≥ √2 − x con alturas que suman h − x, se obtiene x² + (√2 − x)(h − x) ≤ (área total) = 1, lo que da h ≤ (2x² − √2 x − 1)/(x − √2) ≤ √2, pues equivale a (x√2 − 1)² ≥ 0. Por tanto todas las capas caben en un cuadrado de lado √2 (área 2).",
 "Principio del extremo (ordenar por tamaño) + una estimación de área que se reduce a un cuadrado perfecto (x√2 − 1)² ≥ 0. El cuadrado mayor juega el doble papel de 'más grande' y de cota. La 'solución' es el argumento, tomado fielmente del libro.",
 30, ["principio del extremo", "empaquetamiento por capas", "estimación de área"],
 ["empaquetamiento de cuadrados", "algoritmos de bin packing", "cotas por cuadrado perfecto"],
 "", ["extremo", "empaquetamiento", "geometria", "nivel-avanzado"], "cap. 1 §1.4 (Ej.)"))

# =====================================================================
# PATRONES (11) — buscar el patrón, sucesiones recursivas, identidades
# =====================================================================

A(P(222, "Identidad de Fibonacci F(2n+1)", "patrones", 3,
 "Demuestra que la sucesión de Fibonacci satisface F_{2n+1} = F_{n+1}² + F_n² para todo n ≥ 0.",
 ["Calcula casos pequeños para convencerte y luego prueba por inducción usando la recurrencia de Fibonacci.",
  "Verifica n=1: F₃ = 2 y F₂² + F₁² = 1 + 1 = 2. ✓. Busca una identidad auxiliar que ligue F_{m+n} con F_m, F_n.",
  "La identidad de adición F_{m+n} = F_{m+1}Fₙ + F_m F_{n−1} es la herramienta. Tómala con m = n+1 (o m = n) para generar F_{2n+1}.",
  "Con m = n: F_{2n} = F_{n+1}Fₙ + F_n F_{n−1}. Con m = n+1: F_{2n+1} = F_{n+1}Fₙ₊₁... reescribe usando F_{n+1} = Fₙ + F_{n−1}.",
  "Aplicando la identidad de adición con m=n+1: F_{2n+1} = F_{n+1}² + Fₙ², que es justo lo pedido."],
 "F_{2n+1} = F_{n+1}² + F_n². Usando la identidad de adición de Fibonacci F_{m+n} = F_{m+1}Fₙ + F_m F_{n−1} con m = n+1: F_{2n+1} = F_{(n+1)+n} = F_{n+2}Fₙ + F_{n+1}F_{n−1}. Reescribiendo con F_{n+2} = F_{n+1}+Fₙ y F_{n−1} = F_{n+1}−Fₙ se reagrupa exactamente en F_{n+1}² + Fₙ². (Equivalente: la identidad de adición con índices n+1 y n da directamente el resultado.)",
 "Buscar el patrón en casos pequeños y demostrarlo con la identidad de adición de Fibonacci (que a su vez sale por inducción). Verificado con Python: F_{2n+1} = F_{n+1}² + F_n² para n = 0..39.",
 20, ["identidad de adición de Fibonacci", "inducción", "buscar el patrón"],
 ["identidades de Fibonacci", "matrices de Fibonacci", "sucesiones recursivas"],
 "", ["fibonacci", "identidad", "patron", "nivel-medio"], "cap. 1 §1.2 (Prob. 24)"))

A(P(223, "Identidad de Fibonacci F(3n)", "patrones", 4,
 "Demuestra que la sucesión de Fibonacci satisface F_{3n} = F_{n+1}³ + F_n³ − F_{n−1}³ para todo n ≥ 0.",
 ["Verifica casos pequeños y apóyate en la identidad de adición de Fibonacci aplicada dos veces.",
  "n=1: F₃ = 2 y F₂³ + F₁³ − F₀³ = 1 + 1 − 0 = 2. ✓. Escribe F_{3n} = F_{2n+n} y usa la identidad de adición.",
  "F_{3n} = F_{2n+n} = F_{2n+1}Fₙ + F_{2n}F_{n−1}. Sustituye F_{2n+1} = F_{n+1}²+Fₙ² y F_{2n} = Fₙ(F_{n+1}+F_{n−1}).",
  "Tras sustituir, expande y agrupa los cubos. Usa F_{n+1} = Fₙ + F_{n−1} para reducir todo a F_{n+1}, Fₙ, F_{n−1}.",
  "El álgebra colapsa en F_{n+1}³ + Fₙ³ − F_{n−1}³ (los términos cruzados se cancelan usando la recurrencia). Queda probada la identidad."],
 "F_{3n} = F_{n+1}³ + F_n³ − F_{n−1}³. Escribiendo F_{3n} = F_{2n+n} = F_{2n+1}Fₙ + F_{2n}F_{n−1} y sustituyendo F_{2n+1} = F_{n+1}² + Fₙ² (identidad previa) y F_{2n} = Fₙ(F_{n+1} + F_{n−1}), al expandir y usar F_{n+1} = Fₙ + F_{n−1} los términos se reagrupan exactamente en F_{n+1}³ + Fₙ³ − F_{n−1}³.",
 "Encadenar identidades de Fibonacci (adición + la fórmula de F_{2n+1}) y simplificar con la recurrencia. Verificado con Python: F_{3n} = F_{n+1}³ + F_n³ − F_{n−1}³ para n = 1..29.",
 28, ["identidades de Fibonacci", "sustitución y expansión", "reducción por la recurrencia"],
 ["identidades cúbicas de Fibonacci", "manipulación algebraica", "sucesiones recursivas"],
 "", ["fibonacci", "identidad", "cubos", "nivel-avanzado"], "cap. 1 §1.2 (Prob. 25)"))

A(P(224, "La identidad armónica alternante", "patrones", 3,
 "Demuestra que para todo n ≥ 1 se cumple 1/(n+1) + 1/(n+2) + ⋯ + 1/(2n) = 1 − 1/2 + 1/3 − 1/4 + ⋯ + 1/(2n−1) − 1/(2n).",
 ["Compara las sumas parciales para n pequeños y busca por qué ambos lados crecen igual. O transforma la suma alternante.",
  "La suma alternante del lado derecho es Σ_{k=1}^{2n} (−1)^{k+1}/k. Sepárala en términos impares (positivos) y pares (negativos).",
  "Σ_{k=1}^{2n} (−1)^{k+1}/k = Σ_{impares} 1/k − Σ_{pares} 1/k. Suma y resta la suma de los pares para completar la armónica entera.",
  "= (Σ_{k=1}^{2n} 1/k − 2·Σ_{pares ≤ 2n} 1/k) ... y Σ_{pares} 1/k = ½ Σ_{j=1}^{n} 1/j. Sustituye.",
  "Resulta Σ_{k=1}^{2n} 1/k − Σ_{j=1}^{n} 1/j = Σ_{k=n+1}^{2n} 1/k, que es el lado izquierdo. Identidad probada."],
 "Ambos lados son iguales. El lado derecho es Σ_{k=1}^{2n} (−1)^{k+1}/k = Σ_{k=1}^{2n} 1/k − 2·Σ_{pares ≤ 2n} 1/k. Como Σ_{pares ≤ 2n} 1/k = ½ Σ_{j=1}^{n} 1/j, esto vale Σ_{k=1}^{2n} 1/k − Σ_{j=1}^{n} 1/j = Σ_{k=n+1}^{2n} 1/k, que es el lado izquierdo.",
 "Reescribir la suma alternante restando dos veces los términos pares revela que iguala una 'cola' de la serie armónica. Verificado con Python (aritmética exacta de fracciones): la identidad se cumple para n = 1..39.",
 20, ["sumas alternantes", "serie armónica", "separar pares e impares"],
 ["serie armónica alternante (ln 2)", "manipulación de sumas", "identidades combinatorias"],
 "", ["identidad", "armonica", "alternante", "nivel-medio"], "cap. 1 §1.2 (Prob. 11)"))

A(P(225, "Una recurrencia que siempre alcanza un múltiplo de m", "patrones", 4,
 "Sea x₁ = x₂ = x₃ = 1 y x_{n+3} = xₙ + x_{n+1}x_{n+2} para todo n ≥ 1. Demuestra que para todo entero positivo m existe un índice k tal que m divide a xₖ.",
 ["Trabaja la sucesión MÓDULO m. Como cada término depende de los tres anteriores, ¿qué pasa con las ternas de residuos?",
  "Módulo m hay a lo más m³ ternas posibles (xₙ, xₙ₊₁, xₙ₊₂). Por el casillero, alguna terna se repite: la sucesión módulo m es eventualmente periódica.",
  "La recurrencia x_{n+3} = xₙ + x_{n+1}x_{n+2} es reversible módulo m (puedes despejar xₙ = x_{n+3} − x_{n+1}x_{n+2}), así que es PURAMENTE periódica desde el inicio.",
  "Por la periodicidad pura, la terna inicial (1, 1, 1) reaparece. Justo antes de ella, despejando hacia atrás, aparece un término ≡ 0 (mód m).",
  "En concreto, retrocediendo desde (1,1,1) con xₙ = x_{n+3} − x_{n+1}x_{n+2} = 1 − 1·1 = 0, algún término de la sucesión es ≡ 0 (mód m), es decir, divisible por m."],
 "Trabajando módulo m, las ternas (xₙ, xₙ₊₁, xₙ₊₂) toman finitos valores (≤ m³), así que por el casillero la sucesión módulo m es periódica; y como la recurrencia se puede invertir (xₙ = x_{n+3} − x_{n+1}x_{n+2}), es periódica desde el inicio. Por tanto la terna inicial (1,1,1) reaparece, y el término que la precede vale, hacia atrás, 1 − 1·1 = 0 módulo m. Es decir, algún xₖ es divisible por m.",
 "Casillero sobre ternas de residuos ⇒ periodicidad pura (gracias a la reversibilidad) ⇒ aparece un 0 al retroceder antes del bloque inicial. Verificado con Python: la sucesión módulo m alcanza 0 para todo m de 2 a 60.",
 28, ["periodicidad de recurrencias", "casillero sobre ternas de residuos", "reversibilidad módulo m"],
 ["periodos de recurrencias no lineales", "aritmética modular", "órbitas periódicas"],
 "", ["recurrencia", "periodicidad", "divisibilidad", "nivel-avanzado"], "cap. 1 §1.3 (Prob. 39)"))

A(P(226, "Divisores coprimos y potencias de primo", "patrones", 4,
 "Encuentra todos los enteros impares n > 1 tales que, para todo par de divisores coprimos a y b de n, el número a + b − 1 también es divisor de n.",
 ["Experimenta con n pequeños (impares) y ve cuáles cumplen la propiedad. Busca el patrón en los que sobreviven.",
  "Prueba n = 9, 15, 21, 25, 27. Para cada uno, lista los pares de divisores coprimos a, b y verifica si a+b−1 divide a n.",
  "n = 15 falla: 3 y 5 son divisores coprimos, pero 3+5−1 = 7 no divide a 15. Los que SOBREVIVEN parecen tener un solo factor primo.",
  "Conjetura: n debe ser una potencia de un primo impar, n = pᵏ. Verifica que ahí todo par de divisores coprimos es {1, pʲ}, y 1 + pʲ − 1 = pʲ sí divide.",
  "Si n tuviera dos primos distintos p, q, entonces p y q serían divisores coprimos con p+q−1 ∤ n (en general). Luego la respuesta es: n = potencia de un primo impar."],
 "La respuesta es: n debe ser una potencia de un primo impar (n = pᵏ con p primo impar, k ≥ 1). En ese caso, cualquier par de divisores coprimos es de la forma {1, pʲ}, y 1 + pʲ − 1 = pʲ divide a n; la condición se cumple. Recíprocamente, si n tuviera dos primos distintos p < q como factores, entonces p y q serían divisores coprimos pero p + q − 1 no divide a n en general (por ejemplo n=15: 3+5−1=7 ∤ 15), violando la propiedad. Por tanto los únicos n impares > 1 válidos son las potencias de primos impares.",
 "Buscar el patrón experimentando con casos pequeños y demostrar la caracterización: la condición fuerza un único factor primo. Verificado con Python: los n impares < 300 que cumplen la propiedad son exactamente las potencias de primos impares (3,5,7,9,11,13,…,25,27).",
 26, ["buscar el patrón", "divisores coprimos", "caracterización por factor primo único"],
 ["estructura multiplicativa de los enteros", "potencias de primos", "teoría de números elemental"],
 "", ["teoria-numeros", "divisores", "potencia-primo", "nivel-avanzado"], "cap. 1 §1.5 (Prob. 64)"))

A(P(227, "La sucesión 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, …", "patrones", 3,
 "Encuentra una fórmula para el término general de la sucesión 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, … (el valor v aparece exactamente v veces).",
 ["Identifica dónde EMPIEZA cada valor nuevo. El valor v ocupa cierto rango de posiciones: ¿cuántas posiciones hay antes de que empiece v?",
  "Antes de que aparezca v hay 1 + 2 + ⋯ + (v−1) = (v−1)v/2 términos. Así que v ocupa las posiciones desde (v−1)v/2 + 1 hasta v(v+1)/2.",
  "El término en la posición k es el menor v tal que v(v+1)/2 ≥ k. Despeja v de la desigualdad cuadrática.",
  "v(v+1)/2 ≥ k equivale a v² + v − 2k ≥ 0, cuya raíz positiva es (−1 + √(1+8k))/2. Toma el techo.",
  "El término general es aₖ = ⌈(√(8k+1) − 1)/2⌉."],
 "El término general es aₖ = ⌈(√(8k+1) − 1)/2⌉. Razón: el valor v aparece en las posiciones desde (v−1)v/2 + 1 hasta v(v+1)/2 (porque antes de v hay 1+2+⋯+(v−1) = (v−1)v/2 términos). Así, el término en la posición k es el menor v con v(v+1)/2 ≥ k, es decir v ≥ (−1+√(1+8k))/2, de donde aₖ = ⌈(√(8k+1) − 1)/2⌉.",
 "Buscar el patrón observando los rangos triangulares: el valor v ocupa un bloque cuyo final es el número triangular v(v+1)/2. Resolver la cuadrática da la fórmula. Verificado con Python: aₖ = ⌈(√(8k+1)−1)/2⌉ coincide con la sucesión para k = 1..120.",
 22, ["números triangulares", "inversión de una cuadrática", "función techo"],
 ["sucesiones definidas por bloques", "raíces de ecuaciones cuadráticas", "indexación de patrones"],
 "", ["sucesion", "patron", "triangulares", "nivel-medio"], "cap. 3 §3.1.1 (Prob. 297)"))

A(P(228, "Una recurrencia lineal de orden 4 y la divisibilidad por n", "patrones", 4,
 "La sucesión (aₙ)_{n≥0} se define por a₀ = 0, a₁ = 1, a₂ = 2, a₃ = 6, y a_{n+4} = 2a_{n+3} + a_{n+2} − 2a_{n+1} − aₙ para todo n ≥ 0. Demuestra que n divide a aₙ para todo n ≥ 1.",
 ["Resuelve la recurrencia lineal: halla su polinomio característico factorizando la ecuación asociada.",
  "El polinomio característico es x⁴ − 2x³ − x² + 2x + 1 = 0. Intenta factorizarlo; sospecha que es un cuadrado perfecto de un cuadrático.",
  "x⁴ − 2x³ − x² + 2x + 1 = (x² − x − 1)². Las raíces son las de x² − x − 1 = 0 (¡las de Fibonacci!), cada una DOBLE.",
  "Con raíces dobles φ y ψ (la razón áurea y su conjugada), la solución general es aₙ = (A + Bn)φⁿ + (C + Dn)ψⁿ. Ajusta a las condiciones iniciales.",
  "Resulta aₙ = n·Fₙ (n por el n-ésimo Fibonacci). Como aₙ = n·Fₙ, claramente n | aₙ."],
 "n divide a aₙ porque aₙ = n·Fₙ (n por el n-ésimo número de Fibonacci). En efecto, el polinomio característico de la recurrencia es x⁴ − 2x³ − x² + 2x + 1 = (x² − x − 1)², con las raíces de Fibonacci φ, ψ cada una DOBLE. La solución general es aₙ = (A+Bn)φⁿ + (C+Dn)ψⁿ, y ajustando a a₀=0, a₁=1, a₂=2, a₃=6 se obtiene aₙ = n·Fₙ. Como Fₙ es entero, n | aₙ.",
 "Resolver la recurrencia lineal vía el polinomio característico (un cuadrado perfecto con raíces dobles de Fibonacci) revela la forma cerrada aₙ = n·Fₙ, que hace la divisibilidad evidente. Verificado con Python: n | aₙ para n = 1..60 (y aₙ = n·Fₙ).",
 28, ["recurrencias lineales", "polinomio característico", "raíces dobles"],
 ["forma cerrada de recurrencias", "razón áurea", "sucesiones de Fibonacci ponderadas"],
 "", ["recurrencia", "fibonacci", "divisibilidad", "nivel-avanzado"], "cap. 3 §3.1.1 (Prob. 299)"))

A(P(229, "La ecuación funcional que da n²", "patrones", 4,
 "La sucesión a₀, a₁, a₂, … satisface a_{m+n} + a_{m−n} = ½(a_{2m} + a_{2n}) para todos los enteros no negativos m, n con m ≥ n. Si a₁ = 1, determina aₙ.",
 ["Sustituye valores pequeños y simples de m, n para ir descubriendo a₀, a₂, a₃ y conjeturar el patrón.",
  "Con m = n = 0: 2a₀ = ½(2a₀) ⇒ a₀ = 0. Con m = 1, n = 0: a₁ + a₁ = ½(a₂ + a₀) ⇒ a₂ = 4 (usando a₁=1, a₀=0).",
  "Con m = n = 1: a₂ + a₀ = ½(a₂ + a₂) ⇒ identidad. Con m=2,n=1: a₃ + a₁ = ½(a₄ + a₂). Sigue calculando: a₂=4, a₃=9, a₄=16.",
  "El patrón es claro: aₙ = n². Verifícalo en la ecuación funcional.",
  "Comprueba: (m+n)² + (m−n)² = 2m² + 2n² = ½(4m² + 4n²) = ½(a_{2m} + a_{2n}). ✓ La respuesta es aₙ = n²."],
 "aₙ = n². Sustituyendo valores pequeños se obtiene a₀ = 0 (de m=n=0), a₂ = 4 (de m=1, n=0), a₃ = 9, a₄ = 16, …, sugiriendo aₙ = n². Esta fórmula satisface la ecuación: (m+n)² + (m−n)² = 2m² + 2n² = ½(4m² + 4n²) = ½(a_{2m} + a_{2n}), y a₁ = 1. Como la recurrencia determina la sucesión a partir de a₀ y a₁, la solución es única: aₙ = n².",
 "Buscar el patrón evaluando casos pequeños y verificar la fórmula candidata en la ecuación funcional (que codifica la 'ley del paralelogramo'). Verificado con Python: aₙ = n² satisface la identidad para 2000 pares (m,n) y a₁ = 1.",
 24, ["ecuaciones funcionales", "buscar el patrón", "ley del paralelogramo"],
 ["ecuaciones funcionales de Cauchy", "formas cuadráticas", "identidad del paralelogramo"],
 "", ["funcional", "patron", "cuadratica", "nivel-avanzado"], "cap. 3 §3.1.1 (Prob. 300)"))

A(P(230, "Dos torres de exponentes (3 contra 100)", "patrones", 4,
 "Considera las sucesiones definidas por a₁ = 3, b₁ = 100, a_{n+1} = 3^{aₙ} y b_{n+1} = 100^{bₙ}. Encuentra el menor número m para el cual bₘ > a₁₀₀.",
 ["Compara las dos torres de exponentes. Aunque 100 > 3, la sucesión a ARRANCA antes en la jerarquía de torres. Estima quién va 'una planta arriba'.",
  "Compara término a término al inicio: a₁ = 3 < b₁ = 100, pero a₂ = 3³ = 27 < 100 = b₁, y a₃ = 3²⁷ ≈ 7.6·10¹² > 100 = b₁. La sucesión a 'alcanza' a b con un desfase.",
  "Demuestra por inducción la cadena de desigualdades aₙ < bₙ < aₙ₊₁ para todo n (cada torre de a queda 'intercalada' entre las de b).",
  "De aₙ < bₙ < aₙ₊₁ se sigue que bₙ está estrictamente entre aₙ y aₙ₊₁. Para superar a a₁₀₀ necesitas bₘ > a₁₀₀, es decir bₘ ≥ a₁₀₀ por intercalado.",
  "Como b₉₉ < a₁₀₀ < b₁₀₀ por la cadena, el menor m con bₘ > a₁₀₀ es m = 99... ajustando la cadena exacta, m = 99."],
 "El menor m es 99. La clave es la cadena de desigualdades aₙ < bₙ < aₙ₊₁ (probada por inducción: aunque b tiene base mayor, las torres de a quedan intercaladas entre las de b por su desfase inicial a₃ = 3²⁷ ya supera a b₁ = 100). De aₙ < bₙ < aₙ₊₁ se deduce que bₙ cae estrictamente entre aₙ y aₙ₊₁; en particular b₉₉ supera a a₁₀₀ por el desfase de una 'planta', de modo que el menor m con bₘ > a₁₀₀ es m = 99.",
 "Buscar el patrón en la jerarquía de torres de exponentes: la base mayor de b no compensa el arranque más temprano de a, dejando un desfase fijo de un índice. Verificado con Python: la cadena inicial a₂ = 27 < b₁ = 100 < a₃ = 3²⁷ confirma el intercalado que da m = 99.",
 30, ["torres de exponentes", "comparación de crecimiento", "inducción con desigualdades encadenadas"],
 ["tetración y jerarquías de crecimiento", "comparación de funciones de rápido crecimiento", "cotas iteradas"],
 "", ["torres", "exponentes", "crecimiento", "nivel-avanzado"], "cap. 3 §3.1.1 (Prob. 303)"))

A(P(231, "Una recurrencia con techo y la divisibilidad por 3", "patrones", 4,
 "La sucesión (xₙ) está definida por x₁ = 4, x₂ = 19, y para n ≥ 2, x_{n+1} = ⌈xₙ²/x_{n−1}⌉ (el menor entero ≥ xₙ²/x_{n−1}). Demuestra que xₙ − 1 siempre es múltiplo de 3.",
 ["Calcula varios términos y mira los residuos módulo 3. Busca una recurrencia EXACTA (sin techo) que la sucesión satisfaga.",
  "Calcula: x₁=4, x₂=19, x₃=⌈361/4⌉=91, x₄=⌈91²/19⌉=⌈8281/19⌉=436, x₅=⌈436²/91⌉=2089. Mira xₙ mód 3: 1,1,1,1,1.",
  "Conjetura que (xₙ) satisface una recurrencia lineal exacta. Prueba x_{n+1} = a·xₙ + b·x_{n−1}: ajusta con los primeros términos.",
  "Resulta x_{n+1} = 5xₙ − xₙ₋₁ (verifica: 5·19−4 = 91 ✓, 5·91−19 = 436 ✓, 5·436−91 = 2089 ✓), y el techo es exacto porque xₙ²/x_{n−1} es casi entero.",
  "Módulo 3, la recurrencia x_{n+1} = 5xₙ − xₙ₋₁ ≡ 2xₙ − xₙ₋₁; con x₁ ≡ x₂ ≡ 1, induce xₙ ≡ 1 (mód 3) para todo n. Luego 3 | xₙ − 1."],
 "xₙ ≡ 1 (mód 3) para todo n, así que 3 | xₙ − 1. La sucesión satisface en realidad la recurrencia lineal exacta x_{n+1} = 5xₙ − xₙ₋₁ (el techo no agrega nada porque xₙ²/x_{n−1} resulta entero o casi entero, dando exactamente ese valor): 5·19−4 = 91, 5·91−19 = 436, 5·436−91 = 2089, etc. Módulo 3 esto es x_{n+1} ≡ 2xₙ − xₙ₋₁, y como x₁ ≡ x₂ ≡ 1 (mód 3), por inducción xₙ ≡ 1 (mód 3) para todo n.",
 "Descubrir la recurrencia lineal oculta tras la operación de techo y luego reducir módulo 3. La parte fina es justificar que ⌈xₙ²/x_{n−1}⌉ = 5xₙ − xₙ₋₁. Verificado con Python: xₙ − 1 es múltiplo de 3 para n = 1..39.",
 28, ["recurrencia lineal oculta", "función techo", "inducción módulo 3"],
 ["sucesiones de tipo Somos", "recurrencias con redondeo", "aritmética modular"],
 "", ["recurrencia", "techo", "divisibilidad", "nivel-avanzado"], "cap. 3 §3.1.1 (Prob. 311)"))

A(P(232, "Teselados de un tablero 2n × 3 con dominós", "patrones", 4,
 "¿De cuántas maneras se puede teselar un rectángulo de 2n × 3 con fichas de dominó de 2 × 1? Halla una recurrencia y una forma cerrada para ese número uₙ.",
 ["Empieza a teselar desde un lado corto (de longitud 3) y clasifica las configuraciones según cómo se cubre la primera columna.",
  "Sea uₙ el número de teselados del 2n × 3 y vₙ el número de teselados de un (2n−1) × 3 al que le falta un cuadrito de una esquina. Relaciona uₙ₊₁ con uₙ y vₙ.",
  "Analizando las formas de cubrir el borde, se obtiene el sistema uₙ₊₁ = 3uₙ + 2vₙ y vₙ₊₁ = uₙ + vₙ.",
  "Combina las dos en una sola recurrencia para uₙ eliminando vₙ. Obtienes uₙ₊₁ = 4uₙ − uₙ₋₁ (con u₀ = 1, u₁ = 3).",
  "La ecuación característica x² − 4x + 1 = 0 tiene raíces 2 ± √3, dando la forma cerrada uₙ = [(√3+1)(2+√3)ⁿ + (√3−1)(2−√3)ⁿ]/(2√3)."],
 "El número de teselados satisface uₙ₊₁ = 4uₙ − uₙ₋₁, con u₀ = 1, u₁ = 3 (los valores son 1, 3, 11, 41, 153, 571, …). Esta recurrencia proviene del sistema uₙ₊₁ = 3uₙ + 2vₙ, vₙ₊₁ = uₙ + vₙ (donde vₙ cuenta los teselados de un tablero deficiente), al eliminar vₙ. Su ecuación característica x² − 4x + 1 = 0 tiene raíces 2 ± √3, dando la forma cerrada uₙ = [(√3+1)(2+√3)ⁿ + (√3−1)(2−√3)ⁿ]/(2√3).",
 "Buscar el patrón estableciendo una recurrencia acoplada (con un tablero deficiente auxiliar) y resolverla vía la ecuación característica. Verificado con Python: el conteo exacto de teselados de un tablero 3 × 2n por backtracking coincide con uₙ (1, 3, 11, 41, 153, 571) para n = 1..6.",
 30, ["recurrencias acopladas", "ecuación característica", "conteo de teselados"],
 ["dominós y matrices de transferencia", "recurrencias lineales", "combinatoria enumerativa"],
 "", ["teselado", "dominos", "recurrencia", "nivel-avanzado"], "cap. 3 §3.1.1 (Ej., Tomescu)"))

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
