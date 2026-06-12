# Engel · Coloraciones: imposibilidad con crayones

*Lección redactada para CogitoErgoSum a partir del capítulo 2 de «Problem-Solving Strategies» (A. Engel), Coloring Proofs. Cubre la teoría y el muestrario clásico; el resto del capítulo es cantera.*

## El prototipo: el tablero mutilado (Gomory)

> A un tablero 8×8 se le quitan **dos esquinas opuestas**. ¿Puede cubrirse con 31 dominós 2×1?

**El argumento:** colorea como tablero de ajedrez. Un dominó 2×1, **donde sea y como sea que se coloque, cubre SIEMPRE una casilla blanca y una negra** (casillas adyacentes alternan color). Las dos esquinas opuestas son del **mismo color**: al quitarlas quedan **30 de un color y 32 del otro**. Pero 31 dominós cubrirían 31 y 31. **Imposible.** ∎

Dos líneas matan un problema que la fuerza bruta no agota jamás. La esencia: **colorear = particionar las casillas en clases**, y **cada pieza consume una combinación fija de clases**.

## La receta general

Toda demostración por coloración tiene tres pasos:

1. **Elige una coloración** tal que **CADA pieza o movimiento, en cualquier posición y orientación, cubra el mismo multiconjunto de colores** (p. ej. «siempre 1 blanca + 1 negra», o «siempre los 4 colores una vez»). Esta es la **decisión de diseño**: la coloración se diseña **mirando la pieza**, no al revés.
2. **Cuenta cuántas celdas hay de cada color** en la región.
3. **Compara:** si las cuentas no son compatibles con el consumo por pieza (no son múltiplos correctos, o difieren donde deberían igualar), la tarea es **imposible** — la demostración es una contradicción aritmética.

Es el invariante de Engel cap. 1 vestido de geometría: la cuenta por colores es la cantidad que ninguna colocación puede alterar.

## Más de dos colores: el 10×10 y los tetrominós 1×4

> ¿Puede un tablero 10×10 cubrirse con 25 tetrominós rectos 1×4?

Dos colores no obstruyen (50/50, y la pieza cubre 2+2). **Diseña mirando la pieza:** colorea **en diagonal con 4 colores** — la casilla (i, j) recibe el color **(i + j) mod 4**. Una pieza 1×4, horizontal o vertical, ocupa 4 casillas consecutivas en i o en j → sus colores son k, k+1, k+2, k+3 (mod 4): **cubre los 4 colores exactamente una vez, siempre**.

Censa el 10×10: los cuatro colores aparecen **25, 26, 25 y 24 veces** (no parejo: 100/4 = 25 pero la diagonal no reparte exacto en 10×10). 25 piezas cubrirían 25 de **cada** color. 26 ≠ 25 ≠ 24. **Imposible.** ∎

## Coloraciones sobre grafos y caminos

> ¿Existe un camino que pase por cada una de las 14 ciudades exactamente una vez (dado el mapa de carreteras)?

**Bicolorea las ciudades como tablero** (posible si el grafo es bipartito — el mapa de Engel lo es). Cada paso del camino **alterna color**; un camino hamiltoniano de 14 vértices alterna B, N, B, N, … → visita **7 y 7**. Si el grafo tiene **8 de un color y 6 del otro**, tal camino no existe. ∎ (Compárese con la advertencia de §4.1: los hamiltonianos no tienen teoría general — pero la coloración da obstrucciones concretas.)

## Coloraciones del plano continuo: palomar geométrico

«Todo punto del plano es rojo o azul» + una distancia fija = **casillero geométrico**:

- **Dos colores, distancia 1:** toma un **triángulo equilátero de lado 1** — sus 3 vértices, con 2 colores, fuerzan dos del mismo color a distancia 1.
- **Rectángulo monocromático:** en una **retícula 3×7 bicoloreada** siempre hay 4 esquinas de un rectángulo del mismo color (las columnas de altura 3 solo tienen 2³ = 8 patrones; con 7 columnas y el palomar sobre los pares monocolor por columna, dos columnas repiten el par).

Colorear es también una forma de CASILLERO (§3.3): los colores son las cajas.

## La dirección que la coloración NO prueba

**El error del banco:** «las cuentas de colores cuadran, por lo tanto el cubrimiento existe». **No.** La coloración solo produce **obstrucciones**: cuentas incompatibles ⇒ imposible. Cuentas compatibles ⇒ *esta* obstrucción no aplica — y nada más. La **posibilidad se demuestra construyendo el cubrimiento** (o con otro argumento). Mismo principio que en invariantes: la ausencia de una obstrucción no es una construcción.

## Disparadores

- «¿Puede teselarse esta región con esta pieza?» / «¿puede llenarse el cubo con estos ladrillos?» → coloración; **decisión clave: diseña los colores mirando la pieza** (ajedrez para dominós; (i+j) mod n para piezas 1×n; capas/diagonales 3D para ladrillos).
- «¿Camino que visite cada ciudad/casilla una vez?» → bicolorea y cuenta clases.
- «Todo punto del plano de 2 (o 3) colores…» → figura rígida pequeña (triángulo equilátero, retícula) + palomar.
- Las cuentas cuadran → recuerda: falta la construcción.

## Síntesis

> **Chunk mínimo:** Receta de tres pasos: (1) diseña la coloración MIRANDO LA PIEZA, tal que toda colocación consuma el mismo multiconjunto de colores (ajedrez para dominós: 1 blanca + 1 negra; (i+j) mod 4 para 1×4: los cuatro colores); (2) censa los colores de la región; (3) si las cuentas no cuadran con el consumo, imposible. Tablero mutilado: esquinas opuestas del mismo color ⇒ 30/32 ≠ 31/31. 10×10 con 1×4: censo 25/26/25/24 ≠ 25 de cada uno. Caminos: bicolorea — un hamiltoniano de 14 alterna 7 y 7; con 8/6, no existe. Plano continuo: figura rígida + palomar (triángulo equilátero de lado 1; retícula 3×7). Y la dirección que NO prueba: cuentas compatibles ≠ posibilidad — eso exige construcción.

---

*Antes del quiz: reconstruye de memoria el argumento del tablero mutilado, la receta de tres pasos, la coloración (i+j) mod 4 con el censo 25/26/25/24 y la obstrucción bicolor al camino de 14 ciudades.*
