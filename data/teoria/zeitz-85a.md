# Transformaciones rígidas: reflexión, rotación y traslación

*Lección redactada para CogitoErgoSum a partir de la sección 8.5a de Zeitz (The Art and Craft of Problem Solving). Cubre el contenido completo de la unidad.*

## La idea central: mover sin distorsionar

Una **isometría** (del griego: «misma medida») es una función del plano en sí mismo que conserva distancias y ángulos. Hay tres tipos fundamentales: **reflexión**, **rotación** y **traslación**. La jugada de Zeitz no es usarlas para describir figuras —ya lo hace la geometría clásica—, sino para **reubicar datos**. Al aplicar una isometría a *parte* de la figura, la nueva posición suele exhibir una recta, un triángulo conocido o una colinealidad que el enunciado original escondía.

## Reflexión: el principio del espejo

Para minimizar un camino que toca una recta ℓ y regresa (AP + PB con A y B del mismo lado), **refleja uno de los extremos** a través de ℓ. Llámalo B′.

- Para cualquier punto P sobre ℓ, PB = PB′ (la reflexión preserva distancias).
- Luego AP + PB = AP + PB′ ≥ |AB′| por la desigualdad triangular.
- La igualdad ocurre exactamente cuando A, P, B′ son colineales: P es la intersección de AB′ con ℓ.

Este es el principio del **billar** (el rebote en la pared) y de la **ley de reflexión de la luz** («el ángulo de incidencia igual al de reflexión»). Ambos son la misma reflexión disfrazada.

## Rotación: fabricar triángulos equiláteros

En configuraciones con ángulos de 60° o 90° —triángulos equiláteros, cuadrados, hexágonos—, **rotar 60° (o 90°) alrededor de un vértice** manda un segmento sobre otro y *fabrica* triángulos equiláteros o cuadrados «gratis».

El ejemplo canónico es el **punto de Fermat** de un triángulo: construye triángulos equiláteros exteriores sobre cada lado y une su tercer vértice al vértice opuesto del triángulo original. Las tres líneas concurren en el punto que minimiza la suma de distancias a los tres vértices. La demostración usa rotar 60° alrededor de uno de los vértices para alinear los tres segmentos en una sola recta.

**Firma de la rotación:** el enunciado tiene ángulos fijos (60°, 90°, 120°), polígonos regulares, o pide demostrar que tres segmentos «pueden colocarse como los lados de un triángulo».

## Traslación: reunir piezas separadas

Deslizar un segmento para **reunir dos piezas que estaban separadas** es el uso más simple de la traslación, y a menudo el más elegante. El ejemplo clásico: en un trapecio ABCD, traslada un segmento diagonal junto al otro. El resultado es un triángulo cuyos lados son las dos diagonales y la suma (o diferencia) de las bases —en esa posición, la desigualdad triangular o el teorema de Pitágoras se aplican directamente.

## Cómo reconocer qué movimiento usar

| Firma en el enunciado | Movimiento a probar |
|---|---|
| «Minimizar AP + PB con A,B del mismo lado de una recta» | Reflexión del extremo |
| «Demostrar que tres segmentos son iguales» o «triángulo equilátero oculto» | Rotación de 60° |
| «El ángulo de rebote es igual al de incidencia» | Reflexión (billar) |
| «Dos piezas separadas que suman un valor fijo» | Traslación para reunirlas |
| «La suma de distancias a puntos fijos es mínima» | Rotación (Fermat) o reflexión iterada |

La señal unificadora: **el enunciado pide minimizar, igualar o alinear** —y no hay una recta auxiliar obvia que lo haga solo. Una isometría la construye.

## Disparadores

- «Camino que toca una recta y regresa» → refleja un extremo: AP+PB = AP+PB′ ≥ |AB′|.
- «Demostrar igualdad de segmentos en figura con triángulos equiláteros» → rotar 60° para hacer aparecer el triángulo equilátero deseado.
- «Mínima suma de distancias desde un punto interior a tres vértices» → punto de Fermat vía rotación.
- «Trapecio, suma o diferencia de diagonales» → traslación que convierte las dos diagonales en lados de un triángulo.

## Síntesis

> **Chunk mínimo:** Una isometría conserva distancias y ángulos; usada sobre parte de la figura, convierte un camino quebrado en uno recto. **Reflexión del espejo**: para minimizar AP+PB (A,B del mismo lado de ℓ), refleja B en B′; el mínimo es |AB′| y P es la intersección de AB′ con ℓ —es el principio del billar. **Rotación de 60°** alrededor de un vértice fabrica triángulos equiláteros gratis y es la llave del punto de Fermat. **Traslación** reúne piezas separadas para aplicar la desigualdad triangular o Pitágoras. Firma unificadora: el enunciado pide minimizar, igualar o alinear —la isometría adecuada lo logra en un paso.

---

*Antes del quiz: reconstruye de memoria el argumento del espejo (AP+PB=AP+PB′ y por qué ≥|AB′|), la rotación de 60° para el punto de Fermat y la traslación en el trapecio.*
