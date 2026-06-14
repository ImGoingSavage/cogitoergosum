# Árboles, grafos y búsqueda

## BFS vs DFS — cuándo usar cada uno

| | BFS | DFS |
|-|-----|-----|
| Estructura | Cola (queue) | Pila (stack) / recursión |
| Encuentra | Camino **más corto** (sin pesos) | Cualquier camino |
| Uso en árboles | Nivel por nivel | Pre/in/post-orden |
| Uso en grafos | Shortest path, componentes | Ciclos, topo sort, componentes |
| Espacio | O(ancho máximo) | O(profundidad máxima) |
| Implementación | Iterativa (queue) | Recursiva o iterativa (stack) |

**Regla de oro:**
- ¿Camino más corto o mínimo de pasos? → **BFS**
- ¿Exploración exhaustiva, ciclos, orden topológico? → **DFS**

---

## BFS estándar en grafo

```
queue = [nodo_inicio]
visitados = {nodo_inicio}
distancia = {nodo_inicio: 0}

while queue:
    nodo = queue.popleft()
    for vecino in grafo[nodo]:
        if vecino not in visitados:
            visitados.add(vecino)
            distancia[vecino] = distancia[nodo] + 1
            queue.append(vecino)
```

**Tiempo:** O(V+E); **Espacio:** O(V)

**Number of Islands:** BFS/DFS desde cada '1' no visitado, marcando todo el island como visitado. Contar cuántos BFS lanzaste.

---

## DFS — detección de ciclos

**Grafo no dirigido:** ciclo ↔ DFS encuentra un nodo vecino ya visitado que NO es el padre.

**Grafo dirigido:** ciclo ↔ DFS encuentra un nodo que está en el "stack de recursión" actual (color gris).

Estados: blanco (no visitado), gris (en recursión), negro (terminado).

Si llegas a un nodo gris → ciclo.

---

## Orden topológico

Solo para DAGs (grafos dirigidos acíclicos). Linealización de nodos tal que toda arista u→v tiene u antes de v.

**Algoritmo de Kahn (BFS):**
1. Calcula in-degree de cada nodo
2. Añade a la cola todos los nodos con in-degree = 0
3. Procesa: al sacar un nodo, reduce in-degree de sus vecinos
4. Si vecino queda en 0 → añadir a la cola
5. Si al final procesaste todos los nodos: no hay ciclo

**Tiempo:** O(V+E)

**Aplicaciones:** compiladores (dependencias), build systems, orden de cursos.

---

## Árbol binario de búsqueda (BST) — propiedades

En un BST: para todo nodo x, todos los valores en el subárbol izquierdo < x < todos los del derecho.

| Operación | BST balanceado | BST degenerado |
|-----------|---------------|---------------|
| Búsqueda | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| In-order traversal | O(n) | O(n) |

**El recorrido in-order de un BST produce los valores ordenados.**

**Validar BST:** no basta verificar que hijo_izq < raíz < hijo_der (falla con netos). Usa min/max bounds que se heredan hacia abajo.

---

## Ancestro Común Más Bajo (LCA)

**En BST:** si ambos nodos p,q están a la izquierda de la raíz → LCA en subárbol izquierdo. Si ambos a la derecha → subárbol derecho. Si uno a cada lado → la raíz es el LCA.

**En árbol binario general:**
- Si raíz == p o raíz == q: la raíz es el LCA
- Busca en izquierda e derecha recursivamente
- Si ambos lados retornan non-null: la raíz actual es el LCA

**Tiempo:** O(n), **Espacio:** O(h) donde h = altura del árbol.

---

## Algoritmo de Dijkstra — camino más corto con pesos

Para grafos con pesos **no negativos**.

**Algoritmo:**
1. dist[s]=0, dist[v]=∞ para v≠s
2. Priority queue (min-heap) con (0, s)
3. Extraer el nodo u con menor distancia
4. Para cada vecino v: si dist[u]+peso(u,v) < dist[v], actualizar y añadir al heap

**Tiempo:** O((V+E)·log V) con min-heap binario.

**No funciona con pesos negativos** → usar Bellman-Ford O(VE).

---

## Union-Find (Disjoint Set Union)

Estructura para responder: "¿pertenecen x e y al mismo componente conectado?"

**Operaciones:**
- `find(x)`: retorna el representante del componente de x
- `union(x,y)`: une los componentes de x e y

**Optimizaciones:**
- **Path compression:** al llamar find, aplana la cadena → find es O(α(n)) amortizado
- **Union by rank:** une el árbol pequeño bajo el grande

**Aplicaciones:** número de componentes, detección de ciclos, MST (Kruskal).

---

## Trie — árbol de prefijos

Estructura para almacenar strings con búsqueda O(m) donde m = longitud de la clave.

Cada nodo tiene hasta 26 hijos (para el alfabeto inglés) y un flag "es_fin_de_palabra".

| Operación | Trie | Hash set |
|-----------|------|---------|
| Búsqueda por prefijo | O(m) | O(m) pero no soporta prefijos |
| Búsqueda exacta | O(m) | O(m) |
| Enumerar prefijo k | O(m+output) | O(n·m) |

**Usos:** autocompletado, spell checker, longest common prefix, word search en matriz.

---

## Grafo bipartito

Un grafo es **bipartito** si sus nodos se pueden colorear con 2 colores sin que dos nodos del mismo color sean adyacentes.

**Test:** BFS/DFS intentando 2-colorear. Si en algún momento un vecino tiene el mismo color que el nodo actual → no bipartito (tiene ciclo impar).

**Aplicación:** asignación de tareas, matchings, detección de conflictos.

---

## Clonación de grafo

Clona un grafo (nodos + aristas) sin visitar nodos dos veces:

1. Usa hash map: original_nodo → clon_nodo
2. BFS/DFS: al visitar un nodo, créa su clon si no existe
3. Para cada vecino del original: crea su clon y añade al clon actual

**Tiempo:** O(V+E), **Espacio:** O(V)

---

## Serializar/Deserializar árbol binario

Para serializar: recorrido pre-orden con marcadores de nulo ("#").

```
serialize: [1, 2, #, #, 3, 4, #, #, 5, #, #]
```

Para deserializar: reconstruye el árbol procesando los valores en pre-orden, usando recursión.

**Invariante:** pre-orden + marcadores de nulo identifican unívocamente cualquier árbol binario.

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
