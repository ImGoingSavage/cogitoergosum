# Geometría avanzada: vectores, complejos y trigonometría

*Lección redactada para CogitoErgoSum a partir del capítulo de geometría analítica avanzada de Engel (Problem-Solving Strategies). Cubre el contenido completo de la unidad.*

## La idea central

La geometría sintética pura es elegante, pero puede atascarse cuando la configuración tiene muchas razones, ángulos mixtos con longitudes, o rotaciones. Las herramientas analíticas —vectores, números complejos, trigonometría— convierten la figura en **álgebra controlada**. La habilidad clave es **elegir la herramienta por la firma del enunciado**, no usarlas todas al mismo tiempo.

## Vectores: geometría afín

Coloca el origen donde haya más simetría. Todo punto del plano es un vector, y las operaciones clave son:

- **Suma y diferencia**: AB = B − A (el vector de A a B).
- **Combinación afín**: el punto que divide AB en razón m:n desde A es (nA + mB)/(m+n). El baricentro es (A+B+C)/3.
- **Colinealidad**: P, Q, R son colineales ⟺ Q−P y R−P son paralelos ⟺ det(Q−P, R−P) = 0.
- **Perpendicularidad**: u ⊥ v ⟺ u·v = 0 (producto punto).
- **Proyección**: la proyección de v sobre u es (u·v/|u|²)·u.

**Cuándo usar vectores**: muchos puntos medios, razones divididas, paralelas (geometría afín). El producto punto maneja perpendiculares; el producto cruz (o determinante 2×2) da áreas con signo.

## Números complejos: geometría del plano

Identifica cada punto con un número complejo z = x + iy. Las operaciones geométricas se vuelven multiplicaciones y sumas:

- **Rotación de ángulo θ alrededor del origen**: z ↦ z·e^{iθ} = z(cos θ + i sin θ).
- **Rotación alrededor de un centro w**: z ↦ w + e^{iθ}(z − w).
- **Reflexión sobre el eje real**: z ↦ z̄ (conjugado).
- **Distancia**: |z − w|.
- **Ángulo** del segmento AB con el eje x: arg(B − A).

**En el círculo unitario** (|z| = 1): el conjugado z̄ = 1/z. Las fórmulas del circuncentro, reflexiones y pies de alturas se simplifican notablemente. El ortocentro de un triángulo inscrito en la unitaria es H = A + B + C.

**Semejanza espiral**: la transformación z ↦ az + b (con a, b ∈ ℂ) es una semejanza espiral (|a| = la razón, arg(a) = el ángulo). Dos puntos cualesquiera AB y CD se aparean con la única semejanza espiral que lleva A ↦ C, B ↦ D; su parámetro a = (D−C)/(B−A).

**Cuándo usar complejos**: rotaciones, simetrías de reflexión, círculos, configuraciones con ángulos fijos (60°, 90°, 120°) o cuando «multiplicar» captura la estructura (producto de complejos = composición de rotación + escala).

## Trigonometría

Las dos leyes fundamentales para mezclar ángulos con longitudes:

- **Ley de senos**: a/sin A = 2R (donde R es el circunradio). Permite pasar entre lados y ángulos del triángulo, y obtener el circunradio directamente.
- **Ley de cosenos**: c² = a² + b² − 2ab·cos C. Generalización de Pitágoras; da el tercer lado o el coseno de un ángulo.
- **Área**: K = (1/2)ab·sin C. Combinada con K = rs (r el inradio, s el semiperímetro) permite hallar r sin hallar explícitamente las alturas.

La cacería de ángulos (angle chasing) con estas leyes resuelve cuando la figura mezcla ángulos inscritos y longitudes.

## Cómo elegir la herramienta

| Firma del enunciado | Herramienta |
|---|---|
| Muchas razones, puntos medios, paralelas | Vectores |
| Rotaciones, círculos, simetrías, ángulos fijos | Complejos |
| Mezcla de ángulos y longitudes, circunradio | Trigonometría |
| Perpendiculares, proyecciones | Vectores (producto punto) |
| «Demostrar que tres puntos son colineales» | Vectores (determinante) o complejos (parte imaginaria) |

La señal de peligro: si empiezas con coordenadas cartesianas brutas sin aprovechar la simetría, la cuenta se vuelve inmanejable. Siempre coloca el origen en el lugar más ventajoso.

## Disparadores

- «Demostrar que P está en el circuncírculo de ABC» → complejos en la unitaria, o Ptolemeo.
- «Distancias que involucran ángulos del triángulo» → ley de senos da el circunradio; ley de cosenos da los lados.
- «Rotación de un ángulo fijo alrededor de un punto» → complejos directamente.
- «Proyección de un vértice sobre un lado» → vectores (producto punto) o la fórmula del pie de la altura.
- «Puntos medios y baricentro» → vectores con coeficientes aritméticos.

## Síntesis

> **Chunk mínimo:** Vectores: punto ↔ vector; baricentro = (A+B+C)/3; colinealidad ⟺ determinante = 0; perpendicularidad ⟺ producto punto = 0. Complejos: rotación de θ alrededor del origen = ·e^{iθ}; en unitaria, z̄=1/z y H=A+B+C; semejanza espiral z↦az+b con a=(D−C)/(B−A) aparea AB con CD. Trigonometría: a/sinA=2R (circunradio); c²=a²+b²−2ab·cosC; área=(1/2)ab·sinC. Elegir: razones/paralelas→vectores; rotaciones/círculos→complejos; ángulos+longitudes→trigonometría.

---

*Antes del quiz: reconstruye de memoria la fórmula del baricentro como combinación afín, la rotación en complejos, la ley de senos con el circunradio y cuándo usar cada herramienta.*
