"""
Tanda 7: Cracking the Coding Interview (6th ed.) — 60 preguntas, 4 unidades
=============================================================================
EJECUTAR SOLO DESPUÉS DE QUE CASELLA (cuenta B) PUSHEE SUS CAMBIOS.

Flujo:
  git pull --rebase origin main
  python3 data/arena-cc-insert.py
  git add ... && git commit ... && git push

Slots reservados (no chocan con Casella):
  - sw.js:    VERSION → v34  (Casella usa v33)
  - Examen:   f7-ex-23, f7-ex-24  (Casella usa f7-ex-21, f7-ex-22)
  - Unidades: arena-cc1..cc4
  - Heurísticas: divide-y-venceras, programacion-dinamica (nuevas)
"""

import json

with open('data/study.json', 'r', encoding='utf-8') as f:
    study = json.load(f)

# ─── Heurísticas nuevas ───────────────────────────────────────────────────────
new_heuristicas = [
    {
        "id": "divide-y-venceras",
        "nombre": "Divide y vencerás",
        "descripcion": "Divide el problema en subproblemas más pequeños del mismo tipo, resuélvelos recursivamente y combina los resultados.",
        "cuando_usar": "Cuando el problema se puede partir en partes independientes: ordenamiento, búsqueda, multiplicación de matrices, FFT.",
        "ejemplo": "MergeSort: divide en dos mitades, ordena cada una, combina en O(n).",
        "patron": "T(n) = aT(n/b) + f(n) → Teorema Maestro"
    },
    {
        "id": "programacion-dinamica",
        "nombre": "Programación dinámica",
        "descripcion": "Resuelve subproblemas superpuestos una sola vez y almacena los resultados. Memoization (top-down) o tabulation (bottom-up).",
        "cuando_usar": "Cuando hay subproblemas superpuestos y subestructura óptima: shortest path, secuencias, mochila, conteo de formas.",
        "ejemplo": "Fibonacci en O(n): dp[i] = dp[i-1] + dp[i-2].",
        "patron": "Define dp[estado], escribe la recurrencia, identifica el caso base"
    }
]

existing_ids = {h['id'] for h in study['catalogoHeuristicas']}
for h in new_heuristicas:
    if h['id'] not in existing_ids:
        study['catalogoHeuristicas'].append(h)
        print(f"Heurística añadida: {h['id']}")
    else:
        print(f"Heurística ya existe (skip): {h['id']}")

# Máx orden en fase-7
max_ord = max((u.get('orden', 0) for u in study['unidades'] if u.get('bloque') == 'fase-7'), default=0)
print(f"Max orden fase-7 (post-pull): {max_ord}")

# ─── arena-cc1: Arrays, cadenas y hash maps ────────────────────────────────
unit_cc1 = {
    "id": "arena-cc1",
    "bloque": "fase-7",
    "orden": max_ord + 1,
    "titulo": "Arrays, cadenas y tablas hash",
    "libro": "Cracking the Coding Interview (6th ed.)",
    "lectura": "data/teoria/arena-cc1.md",
    "dosis": 30,
    "objetivo": "Dominar hash maps, sliding window y two-pointers para resolver problemas de arrays en O(n).",
    "heuristicas": ["divide-y-venceras", "caso-pequeno"],
    "metadata": {"ruta": "maang", "nivel": 2},
    "ideas_clave": [
        "Hash map = O(1) lookup; úsalo para complementos, frecuencias, duplicados",
        "Sliding window para subarreglos/subcadenas contiguas con propiedad X",
        "Two pointers para pares en arrays ordenados — O(n) vs O(n²)"
    ],
    "banco": [
        {"id": "arcc1-q1", "tipo": "calculo", "enunciado": "Dado un array de enteros y un target, describe el algoritmo O(n) para encontrar dos números que sumen al target (Two Sum).", "solucion": "Hash map: para cada x, busca (target-x) en el mapa. Si existe, retorna. Si no, inserta x→índice.", "explicacion": "El complemento target-x se busca en O(1) con el hash map. Un solo recorrido del array da O(n) tiempo y O(n) espacio."},
        {"id": "arcc1-q2", "tipo": "calculo", "enunciado": "¿Cuál es la complejidad amortizada de insertar al final de un array dinámico (como Python list o Java ArrayList)? Explica.", "solucion": "O(1) amortizado", "explicacion": "El array duplica capacidad cuando se llena. La operación costosa (copiar n elementos) ocurre cada n inserciones. Costo total de n inserciones = n + n/2 + n/4 + ... < 2n → O(1) por inserción amortizado."},
        {"id": "arcc1-q3", "tipo": "calculo", "enunciado": "Dado un string, verifica en O(n) si es permutación de un palíndromo.", "solucion": "Cuenta frecuencias con hash map. Un string es permutación de palíndromo ↔ a lo sumo UN carácter tiene frecuencia impar.", "explicacion": "Un palíndromo puede tener todos los caracteres en pares, excepto el del centro (longitud impar). Contar con hash map en O(n) y verificar la condición."},
        {"id": "arcc1-q4", "tipo": "calculo", "enunciado": "Sliding window: dado array nums y k, encuentra la suma máxima de un subarreglo de longitud exactamente k.", "solucion": "Suma los primeros k elementos. Luego desliza: suma += nums[r] - nums[r-k] y actualiza el máximo. O(n) tiempo, O(1) espacio.", "explicacion": "La ventana fija de tamaño k se actualiza en O(1) por paso: añade el elemento entrante, elimina el saliente."},
        {"id": "arcc1-q5", "tipo": "calculo", "enunciado": "Longitud de la subcadena más larga sin caracteres repetidos. Describe el algoritmo.", "solucion": "Sliding window variable: hash map de carácter→posición. Si s[r] ya está en el mapa y su posición ≥ left, mueve left a esa posición+1. Actualiza el máximo de (r-left+1). O(n).", "explicacion": "El puntero left garantiza que la ventana [left,r] no tiene duplicados. El hash map da O(1) lookup de si un carácter está en la ventana."},
        {"id": "arcc1-q6", "tipo": "calculo", "enunciado": "Dado un array de n enteros, calcula el array de productos donde result[i] = producto de todos los elementos excepto nums[i], sin usar división.", "solucion": "Pase izquierda: result[i] = producto de nums[0..i-1]. Pase derecha: multiplica por sufijo acumulado. O(n) tiempo, O(1) espacio extra.", "explicacion": "Ningún elemento se excluye explícitamente: se multiplican todos los que están a su izquierda y a su derecha."},
        {"id": "arcc1-q7", "tipo": "calculo", "enunciado": "Rota un array de n elementos k posiciones a la derecha en O(n) tiempo y O(1) espacio. Describe el método.", "solucion": "Método de 3 reversas: (1) reversa todo, (2) reversa los primeros k elementos, (3) reversa los últimos n-k.", "explicacion": "Ejemplo [1,2,3,4,5], k=2: → [5,4,3,2,1] → [4,5,3,2,1] → [4,5,1,2,3]. Tres reversas consecutivas logran la rotación."},
        {"id": "arcc1-q8", "tipo": "calculo", "enunciado": "Ordena un array con solo valores {0,1,2} en O(n) con un solo recorrido y O(1) espacio (Dutch National Flag).", "solucion": "Tres punteros: low=0, mid=0, high=n-1. Si nums[mid]=0: swap(low,mid), low++,mid++. Si 1: mid++. Si 2: swap(mid,high), high--.", "explicacion": "Invariante: [0..low-1] son 0s, [low..mid-1] son 1s, [high+1..n-1] son 2s. El puntero mid no avanza al hacer swap con high (el valor intercambiado aún no fue examinado)."},
        {"id": "arcc1-q9", "tipo": "calculo", "enunciado": "Dado una lista de intervalos [sᵢ,eᵢ] posiblemente solapados, combínalos. Describe el algoritmo.", "solucion": "Ordena por inicio. Recorre: si el intervalo actual comienza ≤ fin del resultado anterior, expande el fin. Si no, añade al resultado. O(n log n).", "explicacion": "Después de ordenar, dos intervalos solapados son adyacentes en la lista. La condición de solapamiento es: inicio_actual ≤ fin_anterior."},
        {"id": "arcc1-q10", "tipo": "calculo", "enunciado": "¿Cómo funciona el algoritmo de Rabin-Karp para buscar un patrón de longitud m en un texto de longitud n?", "solucion": "Usa un rolling hash: calcula el hash del patrón y de cada ventana de longitud m en O(1). Si los hashes coinciden, verifica carácter por carácter. O(n+m) esperado.", "explicacion": "El rolling hash actualiza en O(1): descarta el carácter saliente y añade el entrante. Las colisiones de hash se verifican explícitamente pero son raras."},
        {"id": "arcc1-q11", "tipo": "calculo", "enunciado": "Trapping Rain Water: dado un array heights de alturas de barras, calcula el agua total atrapada.", "solucion": "Para cada posición i: agua[i] = min(max_izq, max_der) - heights[i]. O(n) con dos pases o dos punteros.", "explicacion": "Con dos punteros: mantén max_left y max_right avanzando desde los extremos. El lado con menor max determina el agua del puntero que avanza."},
        {"id": "arcc1-q12", "tipo": "concepto", "enunciado": "¿Cuándo conviene usar open addressing vs chaining para resolver colisiones en una tabla hash?", "solucion": "Chaining: mejor con factor de carga alto (α>0.7), implementación sencilla. Open addressing: mejor con α bajo, evita overhead de punteros, mejor localidad de caché.", "explicacion": "Open addressing degrada rápido cuando α>0.7 por clustering. Chaining mantiene O(1+α) pero usa más memoria por los nodos de lista enlazada."},
        {"id": "arcc1-q13", "tipo": "calculo", "enunciado": "Encuentra todos los duplicados en un array de enteros donde 1 ≤ nums[i] ≤ n, n = len(nums). O(n) tiempo y O(1) espacio.", "solucion": "Usa los índices del propio array como hash: para cada nums[i], marca nums[abs(nums[i])-1] como negativo. Si ya era negativo, es duplicado.", "explicacion": "El signo del elemento en la posición abs(x)-1 indica si x fue visto antes. Funciona porque 1 ≤ x ≤ n garantiza que abs(x)-1 es índice válido."},
        {"id": "arcc1-q14", "tipo": "calculo", "enunciado": "Minimum Window Substring: dado s y t, encuentra la ventana mínima en s que contiene todos los caracteres de t.", "solucion": "Sliding window con dos hash maps (cuenta caracteres de t y de la ventana actual). Contrae left cuando la ventana es válida. O(|s|+|t|).", "explicacion": "Mantén un contador 'formados' que indica cuántos caracteres únicos de t están satisfechos. Al satisfacer todos, intenta contraer la ventana."},
        {"id": "arcc1-q15", "tipo": "calculo", "enunciado": "Two Sum con array ORDENADO: encuentra los dos índices con suma = target. O(n) tiempo, O(1) espacio.", "solucion": "Two pointers: left=0, right=n-1. Si suma < target: left++. Si suma > target: right--. Si igual: retorna.", "explicacion": "El array ordenado permite descartar elementos de forma determinista: si la suma es pequeña, el elemento mayor es insuficiente para cualquier valor a la izquierda."}
    ]
}

# ─── arena-cc2: Árboles y grafos ─────────────────────────────────────────────
unit_cc2 = {
    "id": "arena-cc2",
    "bloque": "fase-7",
    "orden": max_ord + 2,
    "titulo": "Árboles, grafos y búsqueda",
    "libro": "Cracking the Coding Interview (6th ed.)",
    "lectura": "data/teoria/arena-cc2.md",
    "dosis": 30,
    "objetivo": "Aplicar BFS, DFS, Dijkstra y Union-Find a problemas de árboles y grafos en entrevistas.",
    "heuristicas": ["divide-y-venceras", "caso-pequeno"],
    "metadata": {"ruta": "maang", "nivel": 2},
    "ideas_clave": [
        "BFS = camino más corto (sin pesos); DFS = ciclos, topológico, componentes",
        "In-order de BST produce valores ordenados — úsalo para validar y buscar",
        "Union-Find responde '¿conectados?' en O(α) amortizado"
    ],
    "banco": [
        {"id": "arcc2-q1", "tipo": "concepto", "enunciado": "¿Cuándo usas BFS en lugar de DFS para explorar un grafo?", "solucion": "BFS cuando necesitas el camino más corto (sin pesos) o la distancia mínima en pasos. DFS para detectar ciclos, orden topológico, o exploración exhaustiva.", "explicacion": "BFS explora por niveles garantizando distancia mínima. DFS usa pila y puede ir más profundo antes de explorar en anchura — útil para problemas de conectividad."},
        {"id": "arcc2-q2", "tipo": "calculo", "enunciado": "¿Cuál es la complejidad de BFS y DFS sobre un grafo con V vértices y E aristas?", "solucion": "O(V+E) para ambos.", "explicacion": "Cada vértice se visita una vez (O(V)) y cada arista se examina una vez (O(E)). La estructura de datos difiere (cola vs pila) pero la complejidad es la misma."},
        {"id": "arcc2-q3", "tipo": "calculo", "enunciado": "Number of Islands: dado un grid 2D de '0's y '1's, cuenta el número de islas. Describe el algoritmo.", "solucion": "DFS/BFS desde cada '1' no visitado, marcando toda la isla como visitada. Incrementa el contador cada vez que lanzas un DFS. O(m·n).", "explicacion": "Cada celda se visita exactamente una vez. Los 4 vecinos (arriba, abajo, izquierda, derecha) se exploran recursivamente o con cola."},
        {"id": "arcc2-q4", "tipo": "calculo", "enunciado": "Orden topológico con el algoritmo de Kahn (BFS). ¿Cuándo no existe un orden topológico?", "solucion": "No existe cuando el grafo tiene un ciclo. Si al final no procesaste todos los V vértices → hay ciclo.", "explicacion": "Kahn: inicia con nodos de in-degree 0 en la cola. Al procesar un nodo, reduce in-degree de sus vecinos; si llega a 0, añádelo a la cola. Si la cola se vacía antes de procesar V nodos → ciclo."},
        {"id": "arcc2-q5", "tipo": "calculo", "enunciado": "¿Cómo validas que un árbol binario es un BST válido?", "solucion": "DFS con bounds: cada nodo debe estar en (min_val, max_val). Para el hijo izquierdo: max_val=nodo.val. Para el derecho: min_val=nodo.val.", "explicacion": "Verificar solo hijo < padre < hijo no es suficiente — un neto podría violar la propiedad BST con el abuelo. Los bounds heredados lo capturan."},
        {"id": "arcc2-q6", "tipo": "calculo", "enunciado": "Lowest Common Ancestor (LCA) en un BST. Describe el algoritmo O(h).", "solucion": "Si ambos nodos p,q < raíz → LCA en subárbol izquierdo. Si ambos > raíz → derecho. Si uno a cada lado (o uno es la raíz) → la raíz es el LCA.", "explicacion": "La propiedad BST permite dirigir la búsqueda sin explorar todo el árbol. Complejidad O(h) donde h = altura."},
        {"id": "arcc2-q7", "tipo": "calculo", "enunciado": "Recorrido level-by-level (BFS) de un árbol binario. ¿Cómo sabes cuándo termina cada nivel?", "solucion": "Al inicio de cada iteración del bucle, el tamaño de la cola es el número de nodos en ese nivel. Procesa exactamente ese número antes de pasar al siguiente.", "explicacion": "queue = [raíz]. while queue: level_size = len(queue). for _ in range(level_size): nodo = queue.popleft(); añade hijos. Cada iteración exterior = un nivel completo."},
        {"id": "arcc2-q8", "tipo": "calculo", "enunciado": "Algoritmo de Dijkstra: ¿qué garantiza y cuándo falla?", "solucion": "Garantiza el camino más corto en grafos con pesos ≥ 0. Falla con pesos negativos (usa Bellman-Ford en ese caso).", "explicacion": "Dijkstra es greedy: extrae el nodo de menor distancia acumulada y no revisa aristas a ese nodo nuevamente. Con pesos negativos, una arista posterior podría mejorar un nodo ya 'finalizado'."},
        {"id": "arcc2-q9", "tipo": "calculo", "enunciado": "¿Cómo detectas un ciclo en un grafo dirigido con DFS?", "solucion": "Usa tres colores: blanco (no visitado), gris (en pila de recursión actual), negro (terminado). Si encuentras un vecino gris → ciclo.", "explicacion": "Un vecino negro es un nodo que ya terminó de explorarse — no implica ciclo. Un vecino gris es un ancestro en la recursión actual — implica back-edge → ciclo."},
        {"id": "arcc2-q10", "tipo": "calculo", "enunciado": "Union-Find: describe las operaciones find y union con path compression y union by rank.", "solucion": "find: sigue el parent hasta la raíz, aplana el path al volver. union: une las raíces; el árbol de menor rank queda bajo el mayor.", "explicacion": "Path compression: cada nodo apunta directamente a la raíz después de find. Union by rank: evita cadenas largas. Juntos: find es O(α(n)) amortizado (casi constante)."},
        {"id": "arcc2-q11", "tipo": "calculo", "enunciado": "Trie: ¿en qué se diferencia de un hash set para almacenar strings?", "solucion": "El Trie soporta búsqueda por prefijo en O(m) donde m = longitud del prefijo. Un hash set solo soporta búsqueda exacta.", "explicacion": "Trie almacena cada carácter como un nodo; el camino desde la raíz forma el string. Ideal para autocompletado, longest common prefix, y word search en matriz."},
        {"id": "arcc2-q12", "tipo": "calculo", "enunciado": "Diámetro de un árbol binario: la longitud del camino más largo entre dos hojas. Describe el algoritmo.", "solucion": "DFS postorden: para cada nodo, el diámetro que pasa por él = altura_izq + altura_der. Actualiza el máximo global. Retorna 1 + max(alt_izq, alt_der).", "explicacion": "El diámetro no necesariamente pasa por la raíz. El DFS bottom-up calcula la altura de cada subárbol y simultáneamente evalúa el diámetro local."},
        {"id": "arcc2-q13", "tipo": "calculo", "enunciado": "¿Cómo verificas si un grafo no dirigido es bipartito?", "solucion": "BFS con 2-coloreo: colorea el nodo inicial con color 0. Para cada vecino, asigna el color opuesto. Si un vecino ya tiene el mismo color → no bipartito.", "explicacion": "Un grafo es bipartito ↔ no tiene ciclos de longitud impar. El 2-coloreo con BFS detecta esto: un ciclo impar fuerza dos nodos adyacentes del mismo color."},
        {"id": "arcc2-q14", "tipo": "calculo", "enunciado": "Clona un grafo con nodos y aristas arbitrarias en O(V+E).", "solucion": "BFS/DFS con un hash map original→clon. Al visitar un nodo, crea su clon si no existe. Para cada vecino: crea su clon si no existe y añade la arista al clon actual.", "explicacion": "El hash map evita visitar el mismo nodo dos veces y permite referenciar nodos ya clonados cuando se conectan aristas."},
        {"id": "arcc2-q15", "tipo": "calculo", "enunciado": "Serialización de un árbol binario: ¿cómo reconstruyes el árbol exacto a partir de una secuencia?", "solucion": "Pre-orden + marcadores de nulo: al serializar, escribe el valor si existe o '#' si es nulo. Al deserializar, reconstruye en pre-orden consumiendo el stream.", "explicacion": "Pre-orden con nulos identifica unívocamente el árbol. In-orden sin nulos NO es suficiente (varios árboles pueden tener el mismo in-orden). La combinación pre+in sí es única pero más compleja."}
    ]
}

# ─── arena-cc3: Recursión y DP ────────────────────────────────────────────────
unit_cc3 = {
    "id": "arena-cc3",
    "bloque": "fase-7",
    "orden": max_ord + 3,
    "titulo": "Recursión y programación dinámica",
    "libro": "Cracking the Coding Interview (6th ed.)",
    "lectura": "data/teoria/arena-cc3.md",
    "dosis": 30,
    "objetivo": "Identificar subproblemas superpuestos y subestructura óptima para aplicar DP o memoización.",
    "heuristicas": ["programacion-dinamica", "divide-y-venceras"],
    "metadata": {"ruta": "maang", "nivel": 3},
    "ideas_clave": [
        "DP = recursión + memoria. Estado mínimo que captura todo lo necesario.",
        "Recurrencia: ¿qué pasó en el ÚLTIMO paso? (coin: tomé esta moneda o no)",
        "Memoization top-down cuando solo necesitas algunos subproblemas; tabulation cuando los necesitas todos"
    ],
    "banco": [
        {"id": "arcc3-q1", "tipo": "calculo", "enunciado": "Climbing Stairs: llegas a un escalón n dando pasos de 1 o 2. ¿Cuántas formas distintas hay? Recurrencia y complejidad.", "solucion": "dp[n] = dp[n-1] + dp[n-2], dp[1]=1, dp[2]=2. Tiempo O(n), espacio O(1) con dos variables.", "explicacion": "El último paso fue de 1 (venías de n-1) o de 2 (venías de n-2). Idéntico a Fibonacci: dp[n] = F(n+1)."},
        {"id": "arcc3-q2", "tipo": "calculo", "enunciado": "Coin Change (mínimo de monedas): monedas [1,5,11], amount=15. ¿Mínimo de monedas? ¿Falla greedy?", "solucion": "DP: dp[15]=3 (11+1+1+1=4, pero 5+5+5=3). Greedy falla: elegiría 11+1+1+1+1=5 monedas.", "explicacion": "Greedy elige la moneda mayor posible. Para [1,5,11]: greedy da 11+4×1=5; DP da 3×5=3. Sin propiedad de intercambio óptimo, greedy no funciona."},
        {"id": "arcc3-q3", "tipo": "calculo", "enunciado": "LCS de 'ABCBDAB' y 'BDCAB'. Escribe la recurrencia y da la longitud.", "solucion": "dp[i][j] = dp[i-1][j-1]+1 si X[i]==Y[j]; max(dp[i-1][j], dp[i][j-1]) si no. LCS = 4 ('BCAB' o 'BDAB').", "explicacion": "Tabla 7×5 llenada bottom-up. La LCS no necesita ser contigua. Backtrack por la tabla para reconstruir la subsecuencia."},
        {"id": "arcc3-q4", "tipo": "calculo", "enunciado": "Edit Distance entre 'kitten' y 'sitting'. Recurrencia y valor.", "solucion": "dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+(0 si iguales, 1 si no)). Resultado = 3.", "explicacion": "kitten→sitten (replace k→s) → sittin (replace e→i) → sitting (insert g). Tabla 7×8 con dp[0][j]=j y dp[i][0]=i como bases."},
        {"id": "arcc3-q5", "tipo": "calculo", "enunciado": "Knapsack 0/1: items {(peso=2,val=6),(peso=2,val=10),(peso=3,val=12)}, W=5. ¿Máximo valor?", "solucion": "22 (items 2 y 3: peso 2+3=5, valor 10+12=22).", "explicacion": "dp[j]: max valor con capacidad j. Recorre items en externo, j de W a peso[i] en interno (orden inverso para 0/1). dp[5] al final da 22."},
        {"id": "arcc3-q6", "tipo": "calculo", "enunciado": "Número de formas de usar monedas [1,2,5] para hacer exactamente amount=5 (Coin Change 2).", "solucion": "4 formas: (5), (2+2+1), (2+1+1+1), (1+1+1+1+1).", "explicacion": "dp[0]=1. Para cada coin: for j de coin a amount: dp[j]+=dp[j-coin]. El orden (coin externo) evita contar permutaciones como distintas."},
        {"id": "arcc3-q7", "tipo": "calculo", "enunciado": "Word Break: ¿puede 'leetcode' segmentarse usando el diccionario ['leet','code']? Describe el DP.", "solucion": "Sí: 'leet' + 'code'. dp[i]=True si dp[j]=True y s[j..i] está en el diccionario para algún j<i.", "explicacion": "dp[0]=True (string vacío). Para i de 1 a n: para j de 0 a i-1: si dp[j] y s[j..i-1] en diccionario → dp[i]=True. O(n²·m) donde m = longitud máxima de palabra."},
        {"id": "arcc3-q8", "tipo": "calculo", "enunciado": "¿Cuántas formas de decodificar '226' usando la regla A=1,...,Z=26?", "solucion": "3 formas: '2','2','6' (BBF) / '22','6' (VF) / '2','26' (BZ).", "explicacion": "dp[0]=1, dp[1]=1. Para i≥2: si s[i-1]≠'0': dp[i]+=dp[i-1]. Si s[i-2..i-1] en [10..26]: dp[i]+=dp[i-2]."},
        {"id": "arcc3-q9", "tipo": "calculo", "enunciado": "Maximum profit con una transacción (buy low, sell high). Algoritmo O(n).", "solucion": "Rastrea el mínimo visto hasta hoy. Para cada día: ganancia = precio_hoy - min_hasta_hoy. Actualiza el máximo de ganancia y el mínimo.", "explicacion": "DP implícito: dp[i] = max ganancia vendiendo en el día i = precio[i] - min(precio[0..i-1]). Se puede calcular en un pase."},
        {"id": "arcc3-q10", "tipo": "calculo", "enunciado": "Largest Square of 1s in binary matrix. Recurrencia DP.", "solucion": "dp[i][j] = lado del cuadrado más grande con esquina inferior derecha en (i,j). Si matrix[i][j]=1: dp[i][j]=min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])+1.", "explicacion": "El cuadrado más grande con esquina en (i,j) está limitado por los cuadrados en sus tres vecinos (arriba, izquierda, diagonal). El mínimo de los tres determina cuánto puede crecer."},
        {"id": "arcc3-q11", "tipo": "calculo", "enunciado": "Unique Paths: cuántos caminos únicos hay de esquina superior-izquierda a inferior-derecha en un grid m×n moviéndose solo derecha o abajo.", "solucion": "dp[i][j] = dp[i-1][j] + dp[i][j-1], dp[0][j]=dp[i][0]=1. Resultado = dp[m-1][n-1]. Alternativamente: C(m+n-2, m-1).", "explicacion": "Hay m+n-2 movimientos totales, de los cuales m-1 son hacia abajo. Elegir cuáles son abajo: C(m+n-2, m-1). DP y combinatoria dan el mismo resultado."},
        {"id": "arcc3-q12", "tipo": "concepto", "enunciado": "¿Cuándo la recursión con memoización es preferible a la tabulation (y viceversa)?", "solucion": "Memoization: cuando solo necesitas algunos subproblemas o el orden de llenado es complejo. Tabulation: cuando necesitas todos los subproblemas, sin overhead de recursión y stack overflow.", "explicacion": "Para n=10^6, la recursión puede causar stack overflow. Tabulation es iterativa y evita este problema. Memoization es más natural para problemas con estado complejo (e.g., bitmask DP)."},
        {"id": "arcc3-q13", "tipo": "calculo", "enunciado": "Palindrome Partitioning: número mínimo de cortes para que cada parte sea palíndromo. Recurrencia.", "solucion": "dp[i] = min cortes para s[0..i]. Para cada j≤i: si s[j..i] es palíndromo → dp[i] = min(dp[i], dp[j-1]+1). Tiempo O(n²) o O(n) con Manacher.", "explicacion": "Precalcula si cada s[i..j] es palíndromo con otra tabla de O(n²). Luego la DP de cortes es O(n²) en total."},
        {"id": "arcc3-q14", "tipo": "calculo", "enunciado": "Burst Balloons: n globos con valores nums[i]. Al reventar el globo i ganas nums[i-1]*nums[i]*nums[i+1]. Maximiza monedas.", "solucion": "dp[i][j] = max monedas de reventar todos los globos en [i..j]. El último globo en reventarse en [i..j] es k: dp[i][j] = max(dp[i][k-1] + nums[i-1]*nums[k]*nums[j+1] + dp[k+1][j]).", "explicacion": "La clave: en lugar de pensar en cuál globo reventar PRIMERO, pensar en cuál es el ÚLTIMO (los vecinos en ese momento son los bordes i-1 y j+1). O(n³)."},
        {"id": "arcc3-q15", "tipo": "calculo", "enunciado": "DP con bitmask: TSP con n=4 ciudades. ¿Cuántos estados tiene dp[mask][i]?", "solucion": "2^n × n = 16 × 4 = 64 estados.", "explicacion": "mask representa el conjunto de ciudades ya visitadas (2^n posibles subconjuntos); i es la ciudad actual (n opciones). Para n=20: 2^20×20 ≈ 20 millones — factible."}
    ]
}

# ─── arena-cc4: Ordenamiento, búsqueda binaria y bits ─────────────────────────
unit_cc4 = {
    "id": "arena-cc4",
    "bloque": "fase-7",
    "orden": max_ord + 4,
    "titulo": "Ordenamiento, búsqueda binaria y bits",
    "libro": "Cracking the Coding Interview (6th ed.)",
    "lectura": "data/teoria/arena-cc4.md",
    "dosis": 30,
    "objetivo": "Aplicar QuickSort, MergeSort, búsqueda binaria sobre respuesta y trucos de bits en entrevistas.",
    "heuristicas": ["divide-y-venceras", "invariantes"],
    "metadata": {"ruta": "maang", "nivel": 2},
    "ideas_clave": [
        "QuickSort: in-place, O(n log n) promedio. MergeSort: estable, O(n log n) garantizado.",
        "Búsqueda binaria sobre la respuesta: cuando el dominio es monótono.",
        "XOR tricks: x^x=0, x^0=x — detecta el elemento sin par o el faltante."
    ],
    "banco": [
        {"id": "arcc4-q1", "tipo": "calculo", "enunciado": "Compara QuickSort y MergeSort: complejidad, espacio y cuándo preferir cada uno.", "solucion": "QuickSort: O(n log n) promedio / O(n²) peor, O(log n) espacio, no estable. MergeSort: O(n log n) garantizado, O(n) espacio, estable. Prefiere QuickSort in-memory; MergeSort para datos externos o cuando necesitas estabilidad.", "explicacion": "QuickSort es más rápido en la práctica (mejor localidad de caché, constantes menores). MergeSort garantiza O(n log n) y es necesario para external sort o listas enlazadas."},
        {"id": "arcc4-q2", "tipo": "calculo", "enunciado": "Búsqueda binaria estándar: describe el invariante y la condición de parada.", "solucion": "Invariante: si el target existe, está en [left, right]. Condición: while left <= right. Actualiza mid = left + (right-left)//2 para evitar overflow.", "explicacion": "El bug más común es usar left + right que puede overflow en enteros de 32 bits. La fórmula left + (right-left)//2 es equivalente pero segura."},
        {"id": "arcc4-q3", "tipo": "calculo", "enunciado": "Búsqueda binaria sobre la respuesta: 'mínima velocidad v para que el barco entregue todos los paquetes en d días'. ¿Cómo planteas la búsqueda?", "solucion": "left=max(pesos), right=sum(pesos). Función canLoad(v): simula la entrega y retorna True si caben en d días. Busca el mínimo v donde canLoad(v)==True.", "explicacion": "La función es monótona: si v es suficiente, v+1 también lo es. Búsqueda binaria sobre la respuesta en O(n log(sum)) en lugar de probar cada velocidad."},
        {"id": "arcc4-q4", "tipo": "calculo", "enunciado": "QuickSelect: encuentra el kth elemento más pequeño. Complejidad esperada y peor caso.", "solucion": "O(n) esperado (con pivote aleatorio), O(n²) peor caso. Después de particionar, recurre solo en la mitad que contiene k.", "explicacion": "A diferencia de QuickSort que recurre en ambas mitades, QuickSelect solo recurre en una → T(n) = T(n/2) + O(n) → O(n) esperado."},
        {"id": "arcc4-q5", "tipo": "calculo", "enunciado": "Buscar en un array rotado sin duplicados: [4,5,6,7,0,1,2], target=0.", "solucion": "Binaria: identifica qué mitad está ordenada. Si arr[left]≤arr[mid]: izquierda ordenada. Si target en rango izquierdo → busca ahí; si no → derecha. O(log n).", "explicacion": "Para el ejemplo: mid=6, arr[left]=4≤arr[mid]=7 → izquierda [4,5,6,7] ordenada. target=0 no está en [4,7] → busca en [0,1,2]. Continúa."},
        {"id": "arcc4-q6", "tipo": "calculo", "enunciado": "Conteo de inversiones en un array: describe cómo usar MergeSort.", "solucion": "Al hacer merge de left_arr y right_arr: si left_arr[i] > right_arr[j], todas las posiciones restantes de left_arr forman inversiones con right_arr[j]. inversiones += (mid - left_i + 1). O(n log n).", "explicacion": "Cada inversión (i<j, arr[i]>arr[j]) se cuenta exactamente una vez durante la fase de merge donde los dos elementos se comparan por primera vez."},
        {"id": "arcc4-q7", "tipo": "calculo", "enunciado": "¿Cómo construyes un heap de n elementos en O(n)?", "solucion": "Heapify desde el último nodo interno hacia la raíz (bottom-up). El nodo en posición ⌊n/2⌋-1 es el último con hijos. O(n) por análisis de suma de alturas.", "explicacion": "Intuitivamente parece O(n log n), pero la mayoría de los nodos están en niveles inferiores con pocas operaciones de sift-down. La suma converge a O(n)."},
        {"id": "arcc4-q8", "tipo": "calculo", "enunciado": "Top-k elementos más frecuentes en un array. ¿Cuál es el enfoque óptimo?", "solucion": "Hash map de frecuencias + min-heap de tamaño k: mantén los k más frecuentes en el heap. Al insertar si el heap tiene k+1 elementos, expulsa el mínimo. O(n log k).", "explicacion": "Alternativa: bucket sort por frecuencia (0 a n) → O(n). El heap da O(n log k) — mejor para k pequeño y n grande."},
        {"id": "arcc4-q9", "tipo": "calculo", "enunciado": "¿Cuándo RadixSort es más eficiente que QuickSort?", "solucion": "Cuando d (número de dígitos) es pequeño y n es grande: RadixSort es O(d·n) vs O(n log n). Para enteros de 32 bits con d=4 pasadas de base 256: O(4n) = O(n).", "explicacion": "RadixSort no es de comparación — puede romper el límite Ω(n log n). Útil para strings de longitud fija, enteros en rango acotado, o IPs."},
        {"id": "arcc4-q10", "tipo": "calculo", "enunciado": "Número faltante en [1..n] usando XOR. Explica por qué funciona.", "solucion": "XOR de 1..n XOR XOR de todos los elementos del array. Los números presentes se cancelan (x^x=0), queda el faltante.", "explicacion": "XOR es conmutativo y asociativo. (1^2^...^n) ^ (todos_excepto_k) = k, porque todos los demás aparecen exactamente 2 veces y se cancelan."},
        {"id": "arcc4-q11", "tipo": "calculo", "enunciado": "¿Qué hace n & (n-1) y para qué sirve?", "solucion": "Elimina el bit más bajo encendido de n. Si el resultado es 0, n es potencia de 2.", "explicacion": "n-1 flippea todos los bits desde el bit menos significativo encendido hacia abajo. El AND borra ese bit. Aplicaciones: contar bits (Kernighan), verificar potencia de 2, limpiar el último bit encendido."},
        {"id": "arcc4-q12", "tipo": "calculo", "enunciado": "Find Peak Element: un pico es un elemento mayor que sus vecinos. Encuentra uno en O(log n).", "solucion": "Binaria: si arr[mid] < arr[mid+1] → el pico está en la derecha. Si arr[mid] < arr[mid-1] → está en la izquierda. Si ambas condiciones son falsas → arr[mid] es pico.", "explicacion": "Siempre existe un pico (el máximo del array siempre lo es). La monotonía local (si mid < mid+1, hay un pico a la derecha) permite búsqueda binaria."},
        {"id": "arcc4-q13", "tipo": "calculo", "enunciado": "Merge k sorted lists en una sola lista ordenada. Complejidad óptima.", "solucion": "Min-heap de tamaño k con el primer elemento de cada lista. Extrae el mínimo, inserta el siguiente elemento de la misma lista. O(N log k) donde N = total de elementos.", "explicacion": "El heap siempre tiene ≤k elementos → cada operación es O(log k). N inserciones + N extracciones = O(N log k). Mejor que merge secuencial O(N·k)."},
        {"id": "arcc4-q14", "tipo": "calculo", "enunciado": "Elemento mayoritario (aparece más de n/2 veces). Describe el algoritmo O(n) con O(1) espacio.", "solucion": "Boyer-Moore Voting: mantén un candidato y un contador. Si contador=0, el candidato es el elemento actual. Si el elemento = candidato, counter++. Si no, counter--.", "explicacion": "El elemento mayoritario 'gana' todos los votos. Aunque pierde contra otros, siempre quedan votos positivos al final porque aparece más de n/2 veces."},
        {"id": "arcc4-q15", "tipo": "calculo", "enunciado": "Median de dos arrays ordenados de tamaños m y n. ¿Cuál es la complejidad óptima?", "solucion": "O(log(min(m,n))) con búsqueda binaria sobre el array más pequeño.", "explicacion": "Particiona el array más pequeño en dos mitades de forma que los elementos a la izquierda de ambas particiones sean ≤ los de la derecha. Búsqueda binaria encuentra la partición correcta en O(log m)."}
    ]
}

# ─── Ítems examen f7-ex-23 y f7-ex-24 ────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        items = bloque['examen']['items']
        # IMPORTANTE: después del pull de Casella, habrá f7-ex-21 y f7-ex-22
        # Verificar el último ID real y usar el siguiente
        last_id = int(items[-1]['id'].split('-')[-1])
        print(f"Último examen id post-pull: f7-ex-{last_id:02d}")
        next_id1 = last_id + 1
        next_id2 = last_id + 2
        break

ex_next1 = {
    "id": f"f7-ex-{next_id1:02d}",
    "heuristica": "programacion-dinamica",
    "enunciado": "Tienes una escalera de n=10 escalones. Puedes subir 1, 2 o 3 escalones a la vez. (a) ¿Cuántas formas distintas de llegar al escalón 10? (b) ¿Cuál es la complejidad? (c) ¿Cómo optimizas el espacio?",
    "pistas": [
        "Define dp[i] = número de formas de llegar al escalón i. ¿De dónde puedes venir al escalón i?",
        "Puedes venir del escalón i-1, i-2 o i-3. Entonces dp[i] = dp[i-1] + dp[i-2] + dp[i-3].",
        "Casos base: dp[0]=1 (en el suelo), dp[1]=1, dp[2]=2. Calcula dp[3]=4, dp[4]=7, ...",
        "Para n=10: dp[10]. Complejidad O(n) tiempo, O(n) espacio. ¿Puedes reducir a O(1)?",
        "Sí: solo necesitas los últimos 3 valores. Usa tres variables que se deslizan. dp[10]=274."
    ],
    "solucion": "dp[10] = 274 formas; O(n) tiempo, O(1) espacio con rolling tres variables.",
    "disparador": "Cuando puedes llegar al paso i desde varios pasos anteriores: dp[i] = suma de dp[i-k] para cada tamaño de paso k permitido. Reduce espacio a O(pasos).",
    "metadata": {
        "ruta": "maang",
        "nivel": 2,
        "skills": ["programacion-dinamica", "casos-base", "optimizacion-espacio"],
        "errores_comunes": ["Caso base dp[0]: ¿hay 1 forma o 0 de llegar al escalón 0?", "Olvidar que dp[2]=2 (1+1 o 2)"],
        "casos_borde": ["Si n=0: hay exactamente 1 forma (no hacer nada)"],
        "source": "Cracking the Coding Interview (6th ed.) — Capítulo 8"
    }
}

ex_next2 = {
    "id": f"f7-ex-{next_id2:02d}",
    "heuristica": "divide-y-venceras",
    "enunciado": "Dado el array [3,1,4,1,5,9,2,6], (a) encuentra el elemento pico en O(log n); (b) encuentra los 2 elementos más frecuentes en O(n); (c) verifica si hay dos elementos que sumen 10 en O(n).",
    "pistas": [
        "Para (a): aplica búsqueda binaria — si arr[mid] < arr[mid+1], el pico está a la derecha.",
        "Para (b): construye un hash map de frecuencias. Luego usa un min-heap de tamaño k=2.",
        "Para (c): inserta cada elemento en un hash set. Para cada x, verifica si (10-x) está en el set.",
        "Pico: mid=3 (arr[3]=1), arr[4]=5>1 → busca derecha; mid=5 (arr[5]=9) > arr[4]=5 y arr[6]=2 → pico=9.",
        "Frecuencias: {3:1,1:2,4:1,5:1,9:1,2:1,6:1} → más frecuentes son 1 (×2) y cualquier otro (×1). Par que suma 10: (1,9),(4,6) — sí existen."
    ],
    "solucion": "(a) pico=9; (b) top-2: [1, cualquier con frec 1]; (c) sí: (1,9) y (4,6).",
    "disparador": "Pico → binaria sobre monotonía. Top-k → min-heap de tamaño k. Suma objetivo → hash set con complemento.",
    "metadata": {
        "ruta": "maang",
        "nivel": 2,
        "skills": ["busqueda-binaria", "hash-map", "heap"],
        "errores_comunes": ["Pico: no verificar los bordes del array", "Top-k: confundir min-heap con max-heap"],
        "casos_borde": ["Array de un elemento: siempre es pico"],
        "source": "Cracking the Coding Interview (6th ed.) — Capítulos 10 y 5"
    }
}

# ─── Insertar ─────────────────────────────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        bloque['unidades'].extend(['arena-cc1','arena-cc2','arena-cc3','arena-cc4'])
        bloque['examen']['items'].extend([ex_next1, ex_next2])
        print(f"fase-7: {len(bloque['unidades'])} unidades, {len(bloque['examen']['items'])} examen items")
        break

for u in [unit_cc1, unit_cc2, unit_cc3, unit_cc4]:
    study['unidades'].append(u)
    print(f"Unidad: {u['id']} ({len(u['banco'])}q)")

with open('data/study.json', 'w', encoding='utf-8') as f:
    json.dump(study, f, ensure_ascii=False, indent=2)

print("\n✅ study.json actualizado.")
for uid in ['arena-cc1','arena-cc2','arena-cc3','arena-cc4']:
    u = next(x for x in study['unidades'] if x['id']==uid)
    print(f"  {uid}: {len(u['banco'])}q")

dupes = {}
for u in study['unidades']:
    for q in u.get('banco',[]):
        dupes[q['id']] = dupes.get(q['id'],0)+1
bad = [(k,v) for k,v in dupes.items() if v>1]
print(f"Duplicados: {bad or 'ninguno'}")
print(f"Total heurísticas: {len(study['catalogoHeuristicas'])}")

# ─── INSTRUCCIONES POST-EJECUCIÓN ─────────────────────────────────────────────
print("""
DESPUÉS DE EJECUTAR ESTE SCRIPT:

1. Actualiza sw.js:
   - VERSION = 'cogitoergosum-v34'
   - Añade al SHELL:
       'data/teoria/arena-cc1.md',
       'data/teoria/arena-cc2.md',
       'data/teoria/arena-cc3.md',
       'data/teoria/arena-cc4.md',

2. Actualiza ledger: Cracking the Coding Interview → completado (60q)

3. Commit y push:
   git add data/study.json sw.js data/arena-ingesta-ledger.json \\
     data/teoria/arena-cc1.md data/teoria/arena-cc2.md \\
     data/teoria/arena-cc3.md data/teoria/arena-cc4.md
   git commit -m "Tanda 7: CCI (60q) · maang · arena-cc1..cc4 · sw v34"
   git push origin main
""")
