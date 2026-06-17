# Grafos: recodificar relaciones

*Lección redactada para CogitoErgoSum a partir de la sección 4.1 de Zeitz (Graph Theory). Cubre el contenido completo de la unidad.*

## La jugada: de palabrería a estructura

Un **grafo** es un conjunto de **vértices** (puntos) unidos por **aristas** (líneas). Eso es todo — y es suficiente para recodificar **cualquier relación mutua entre objetos**: personas que se conocen (vértices = personas, arista = se conocen), ciudades con vuelos, equipos que jugaron entre sí, casillas alcanzables por un movimiento, regiones fronterizas.

El valor de la recodificación: la prosa («Ana conoce a Beto, que conoce a…») no se puede calcular; el grafo sí — tiene **grados, caminos, ciclos, componentes**, y teoremas que los gobiernan. Tu primer movimiento ante relaciones por parejas: **dibuja el grafo y calcula los grados antes que nada**.

## Vocabulario mínimo

- **Grado** de un vértice: cuántas aristas le tocan.
- **Camino**: secuencia de aristas consecutivas; **ciclo**: camino que vuelve al inicio.
- **Conexo**: todo par de vértices está unido por algún camino.
- **Árbol**: conexo y sin ciclos.

## El lema del apretón de manos

> **La suma de todos los grados es igual a 2·(número de aristas).**

*Demostración:* cada arista tiene dos extremos, así que al sumar grados, cada arista se cuenta exactamente dos veces. ∎ (Es un conteo doble: el mismo conjunto —los pares (vértice, arista incidente)— contado por vértices y por aristas.)

**Corolario inmediato y letal:**

> **En cualquier grafo, el número de vértices de grado impar es PAR.**

*Demostración:* la suma de los grados es par (es 2·aristas). La suma de los grados pares es par; luego la suma de los grados impares también debe ser par — y una suma de números impares solo es par si hay una cantidad par de ellos. ∎

**Aplicación instantánea — el torneo imposible:** ¿pueden 9 equipos jugar exactamente 3 partidos cada uno (contra rivales del torneo)? Grafo: 9 vértices, todos de grado 3. Serían 9 vértices de grado impar — número **impar** de vértices impares. **Imposible.** (Vía lema: la suma de grados sería 27, que tendría que ser 2·aristas — pero 27 es impar.) Sin dibujar un solo emparejamiento.

## Árboles: el extremo aplicado a grafos

Hechos básicos de un árbol con v vértices:

- Tiene **exactamente v − 1 aristas**.
- Tiene **al menos dos hojas** (vértices de grado 1).

La demostración de las hojas es una joya táctica: considera el **camino más largo** del árbol (existe: hay finitos). Sus dos puntas deben ser hojas — si una punta tuviera otra arista, o alarga el camino (contradice maximalidad) o cierra un ciclo (contradice árbol). Es el **principio del extremo** (§3.2) trabajando dentro de la teoría de grafos: agarra el objeto extremo y explota lo que no puede hacer.

## Caminos eulerianos: la condición exacta

**Camino euleriano** = recorre **cada ARISTA exactamente una vez** (los puentes de Königsberg). Teorema (Euler):

> Un grafo **conexo** tiene camino euleriano ⟺ tiene **0 o 2 vértices de grado impar**. (Con 0, el camino puede cerrarse en circuito; con 2, debe empezar en uno de los impares y terminar en el otro.)

**Por qué los grados impares son el obstáculo:** en cualquier vértice intermedio del recorrido, cada vez que entras tienes que salir — las aristas se consumen **en pares**. Un vértice de grado impar no puede emparejar todas sus aristas: forzosamente es inicio o final del camino. Y solo hay un inicio y un final disponibles: más de 2 impares, no hay recorrido. (Königsberg tenía 4 vértices impares: por eso no hay paseo.)

## Caminos hamiltonianos: la advertencia

**Camino hamiltoniano** = visita **cada VÉRTICE exactamente una vez**. Suena gemelo del euleriano; no lo es: **no existe una condición simple ni teoría completa** para decidir si un grafo lo tiene (es un problema computacionalmente duro en general). Moraleja práctica: si un problema de olimpiada parece pedir un hamiltoniano, **sospecha** — casi seguro la solución real pasa por otro lado (paridad, coloración, conteo), no por una teoría general que no existe.

## Disparadores

- «Se conocen», «jugaron entre sí», «hay vuelo», «comparten frontera», «se puede llegar» → **vértices y aristas; calcula los grados**.
- Suma de grados rara o cantidad impar de vértices impares → imposibilidad por apretón de manos.
- «Recorrer todos los caminos/puentes/pasillos sin repetir» → euleriano: cuenta los vértices impares.
- «Visitar todas las casillas/ciudades una vez» → hamiltoniano: cuidado, busca otra estructura (paridad/coloración).
- Estructura conexa mínima, jerarquías, «sin ciclos» → árbol: v − 1 aristas, dos hojas, camino más largo.

## Síntesis

> **Chunk mínimo:** Relaciones por parejas → grafo (vértices + aristas) y calcula los grados primero. Apretón de manos: Σ grados = 2·aristas (cada arista se cuenta dos veces) ⇒ el número de vértices de grado impar es PAR ⇒ 9 equipos con 3 partidos cada uno: imposible (27 impar). Árboles: v−1 aristas y ≥2 hojas (las puntas del camino MÁS LARGO — extremo dentro de grafos). Euleriano (cada ARISTA una vez): existe en conexo ⟺ 0 o 2 vértices impares, porque en vértices de paso las aristas se consumen en pares (Königsberg: 4 impares ⇒ no hay paseo). Hamiltoniano (cada VÉRTICE una vez): sin teoría simple — si parece pedirlo, la solución va por paridad/coloración/conteo.

---

*Antes del quiz: reconstruye de memoria el lema del apretón de manos con su demostración, el corolario de los impares, la condición euleriana exacta con su porqué, y el veredicto del torneo de 9 equipos.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Los grafos recodifican relaciones para que caminos, componentes y grados hagan visible lo oculto. [[arena-cc2]] enseña busqueda en arboles y grafos, [[arena-h1]] usa DAGs para razonar causalidad y adjustment sets, y [[gen-ma2]] lleva la misma idea a orquestacion: agentes como nodos y mensajes como aristas con fallos posibles.
<!-- GRAFO_CONEXO_OLEADA3_END -->
