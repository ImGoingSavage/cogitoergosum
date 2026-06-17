# Árboles, grafos y búsqueda

## De qué trata esta lección (y qué sabrás hacer al final)

Un grafo es la abstracción de las **relaciones** —ciudades y carreteras, cursos y prerrequisitos, páginas y enlaces—, y un árbol es su caso particular sin ciclos. Esta lección construye desde cero las dos formas de recorrerlos (**BFS** y **DFS**) y, sobre ellas, los algoritmos que casi todas las entrevistas reciclan: camino más corto, detección de ciclos, orden topológico, BST, LCA, Dijkstra, Union-Find y Trie. La habilidad clave no es codificarlos de memoria, sino **leer el enunciado y saber cuál pide**.

Al terminar podrás: (1) elegir BFS (camino más corto en pasos) o DFS (ciclos, orden topológico) por la pregunta; (2) detectar ciclos correctamente en grafos dirigidos (estado "gris" en la pila de recursión) y no dirigidos; (3) producir un orden topológico con el algoritmo de Kahn y reconocerlo como "¿se pueden completar todas las tareas?"; y (4) saber cuándo Dijkstra, Union-Find o un Trie son la herramienta. Cada algoritmo entra por su intuición y un mini-ejemplo a mano.

---

## BFS vs DFS: la pregunta decide

Las dos recorren todo el grafo visitando cada nodo una vez, pero difieren en **el orden** y eso cambia para qué sirven.

| | BFS | DFS |
|-|-----|-----|
| Estructura | cola (FIFO) | pila / recursión (LIFO) |
| Encuentra | camino **más corto** (sin pesos) | cualquier camino |
| En grafos | shortest path, componentes | ciclos, orden topológico |
| Espacio | $O(\text{ancho máx})$ | $O(\text{profundidad máx})$ |

La intuición: **BFS** explora en "anillos" concéntricos desde el origen —primero los vecinos a distancia 1, luego a 2, etc.—, así que la primera vez que toca un nodo lo hace por el camino más corto *en número de aristas*. **DFS** se hunde por una rama hasta el fondo antes de retroceder, lo que lo hace natural para "¿hay un ciclo?" y "¿en qué orden respetar dependencias?". Regla de oro: *¿mínimo de pasos? → BFS. ¿exploración exhaustiva, ciclos, topo sort? → DFS.*

El BFS estándar en un grafo, con su distancia:

```
cola = [inicio];  visitados = {inicio};  dist = {inicio: 0}
mientras cola:
    u = cola.popleft()
    para v en grafo[u]:
        si v no en visitados:
            visitados.add(v);  dist[v] = dist[u] + 1
            cola.append(v)
```

$O(V+E)$ tiempo (toca cada nodo y arista una vez), $O(V)$ espacio. *Number of Islands* es esto disfrazado: lanza un BFS/DFS desde cada `'1'` no visitado, marca toda la isla, y cuenta cuántos lanzaste.

## Detección de ciclos: cuidado con dirigido vs no dirigido

Aquí cae mucha gente, porque la regla **cambia** según el grafo:

- **No dirigido:** hay ciclo si el DFS encuentra un vecino ya visitado que **no es el padre** (volver por donde viniste no cuenta).
- **Dirigido:** hay ciclo si el DFS encuentra un nodo que está **actualmente en la pila de recursión**. Se modela con tres colores: blanco (no visitado), **gris** (en la recursión activa), negro (terminado). Tocar un nodo **gris** = ciclo.

> **Predicción antes de seguir:** ¿puedes detectar ciclos en un grafo dirigido con la regla del no dirigido ("vecino ya visitado")? Respuesta: **no**. Un nodo "negro" (ya terminado) puede ser vecino legítimo sin formar ciclo; solo un nodo **gris** —en el camino actual— delata el ciclo. Confundir las dos reglas es el error clásico.

## Orden topológico (Kahn)

Para un **DAG** (dirigido acíclico), un orden topológico lista los nodos de modo que toda arista $u\to v$ ponga $u$ antes que $v$ —"haz primero los prerrequisitos"—. El algoritmo de Kahn lo construye con BFS sobre los **grados de entrada** (in-degree):

```
calcula in-degree de cada nodo
cola = todos los nodos con in-degree 0
mientras cola:
    u = cola.pop();  añade u al orden
    para v vecino de u:
        in-degree[v] -= 1
        si in-degree[v] == 0: cola.append(v)
si procesaste todos los nodos: no hay ciclo
```

$O(V+E)$. El chequeo final es valioso: si **quedan** nodos sin procesar (su in-degree nunca llegó a 0), hay un ciclo y el orden es imposible — que es exactamente la pregunta "¿se pueden terminar todos los cursos?" (*Course Schedule*). Aplica a compiladores, build systems y planificación.

## Árboles de búsqueda binaria (BST) y LCA

Un **BST** mantiene un invariante: para todo nodo $x$, todo el subárbol izquierdo es $<x<$ todo el derecho. La consecuencia mágica: su **recorrido in-order produce los valores ordenados**. Las operaciones son $O(\log n)$ si está balanceado, pero **$O(n)$ si degenera** (insertar datos ya ordenados lo convierte en una lista). Trampa de "validar BST": comprobar solo `hijo_izq < raíz < hijo_der` **falla con los nietos**; hay que heredar cotas `(min, max)` hacia abajo.

El **ancestro común más bajo (LCA)** explota el orden en un BST: si $p$ y $q$ están ambos a la izquierda de la raíz, el LCA está a la izquierda; ambos a la derecha → a la derecha; uno a cada lado → la raíz misma. En un árbol binario general, se resuelve recursivamente: si la raíz es $p$ o $q$ es el LCA; si las búsquedas izquierda y derecha devuelven ambas algo no nulo, la raíz actual es el LCA. $O(n)$ tiempo, $O(h)$ espacio (altura).

## Dijkstra, Union-Find y Trie

- **Dijkstra** (camino más corto con pesos **no negativos**): mantiene un min-heap de `(distancia, nodo)`, extrae el más cercano y **relaja** sus vecinos. $O((V+E)\log V)$. No funciona con pesos negativos —asume que una distancia fijada ya no mejora—; ahí va Bellman-Ford ($O(VE)$).
- **Union-Find (DSU):** responde "¿$x$ e $y$ están en el mismo componente?" en casi $O(1)$ con dos optimizaciones, *path compression* (aplana las cadenas al consultar) y *union by rank* (cuelga el árbol chico del grande), dando $O(\alpha(n))$ amortizado. Es la base de contar componentes, detectar ciclos y el MST de Kruskal.
- **Trie (árbol de prefijos):** guarda cadenas con búsqueda $O(m)$ ($m$=longitud) y, a diferencia de un hash set, **sí** soporta "todas las palabras que empiezan con…". Potencia autocompletado, spell-checkers y búsqueda de palabras en una matriz.

---

## Mini-ejemplo trabajado: orden topológico (Kahn) a mano

Cursos con prerrequisitos: A→C, B→C, C→D (toma A y B antes de C, C antes de D). ¿En qué orden cursarlos?

1. **In-degree:** A=0, B=0, C=2, D=1.
2. **Cola inicial** (in-degree 0): [A, B].
3. Saca A → reduce C a 1. Saca B → reduce C a 0 → entra C a la cola. Saca C → reduce D a 0 → entra D. Saca D.
4. Orden: **A, B, C, D**. Procesaste los 4 nodos → **no hay ciclo**.

Si al final quedaran nodos sin procesar (in-degree nunca llegó a 0), habría un **ciclo** → imposible ordenar. Ese es justo el chequeo de "¿se puede terminar todos los cursos?" (Course Schedule).

**Predicción antes de seguir:** quieres el **camino más corto en pasos** en un grafo *sin pesos*. ¿Dijkstra? No hace falta: BFS lo da en O(V+E), porque sin pesos "menos aristas = más corto". Dijkstra es para pesos ≥ 0; con pesos negativos, Bellman-Ford.

## Prototipo, contraejemplo y caso borde

- **Prototipo (BFS para shortest path sin pesos):** laberinto/grid → BFS desde el origen da la distancia mínima en pasos.
- **Contraejemplo (Dijkstra con pesos negativos):** Dijkstra falla si hay aristas negativas (asume que una vez fijada la distancia mínima no mejora) → usa Bellman-Ford.
- **Caso borde (validar BST):** comprobar solo `hijo_izq < raíz < hijo_der` **falla** con nietos; hay que heredar cotas min/max hacia abajo.

## Errores típicos

- **Conceptual:** usar DFS para el camino más corto (no lo garantiza); el shortest path sin pesos es **BFS**.
- **Técnico:** detección de ciclo en grafo **dirigido** mirando "vecino ya visitado" (eso vale para no dirigido); en dirigido necesitas el estado **gris** (en la pila de recursión).
- **De estructura:** asumir que un BST está balanceado → en el degenerado (insertar ordenado) las operaciones caen a O(n).

## Transferencia isomorfa

- **Orden topológico ↔ DAG causal / build systems:** ordenar tareas por dependencias es el mismo DAG que ordena causas antes que efectos en inferencia causal (conecta con [[arena-h16]]) y que resuelve dependencias en un compilador.
- **Union-Find ↔ componentes conexas / Kruskal:** "¿están en el mismo grupo?" en casi O(1) es la base del MST y de contar islas — el mismo invariante de "cada unión baja el nº de componentes en 1" del brainteaser de las roturas (conecta con [[arena-q12]]).
- **Trie ↔ hash map para prefijos:** un árbol de prefijos es la versión de hashing que *sí* soporta "todas las palabras que empiezan con…" (conecta con [[arena-cc1]], hashing como memoria).

Moraleja de la arista: *el grafo es la abstracción de las relaciones; BFS da el camino más corto en pasos, DFS detecta ciclos y ordena (topo sort = DAG), y Union-Find responde "¿conectados?" casi gratis.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Mínimo de pasos / camino más corto (sin pesos)" | BFS |
| "¿Existe el camino? / componentes" | BFS o DFS |
| "Orden de tareas con dependencias" | Topological sort (Kahn) |
| "¿Hay ciclo en grafo dirigido?" | DFS con estados gris/negro |
| "Ancestro común más bajo" | LCA recursivo con herencia |
| "Camino más corto con pesos ≥ 0" | Dijkstra + min-heap |
| "¿Mismo componente? / agrupar" | Union-Find |
| "Búsqueda por prefijo / autocompletado" | Trie |
| "2-coloreable / matching" | BFS bipartite check |

---

> **Síntesis:** Los grafos son la abstracción de las relaciones. BFS encuentra el camino más corto (en pasos), DFS encuentra ciclos y ordena topológicamente. Dijkstra añade pesos. Union-Find responde "¿están conectados?" en tiempo casi constante. El Trie es el hash map para prefijos. La mayoría de los problemas de grafos en entrevistas son variantes de BFS, DFS, o Union-Find.

---

*Retrieval: cierra y responde: (1) cuándo usar BFS en vez de DFS; (2) complejidad de Dijkstra con min-heap; (3) cómo detectar ciclo en grafo dirigido; (4) recorrido in-order de BST y su propiedad.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puentes de regreso

Arboles, grafos y busqueda tienen una raiz olimpica en [[zeitz-41]]: recodificar relaciones como nodos y aristas. Ese mismo gesto reaparece en causalidad con [[arena-h1]] y en agentes con [[gen-ma2]], donde la estructura del grafo decide rutas, dependencias y fallos.
<!-- GRAFO_CONEXO_OLEADA3_END -->
