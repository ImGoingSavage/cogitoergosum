# Homotecia y semejanza espiral

*Lección redactada para CogitoErgoSum a partir de la sección 8.5b de Zeitz (The Art and Craft of Problem Solving). Cubre el contenido completo de la unidad.*

## La idea central: cambiar de escala

Las isometrías de §8.5a conservan todas las distancias. Ahora las relajamos: la **homotecia** estira (o comprime) uniformemente desde un centro fijo, y la **semejanza espiral** combina ese cambio de escala con una rotación. Ambas *conservan ángulos y formas*, pero no las longitudes absolutas. Su utilidad: **transportar razones y alinear figuras semejantes** que el enunciado separa.

## Homotecia: dilatación con centro

Una homotecia de **centro O** y **razón k** manda cada punto P al punto O + k·(P − O) sobre el segmento OP. Propiedades esenciales:

- Lleva una figura a otra **semejante con lados paralelos** (las rectas correspondientes son paralelas).
- Si k > 0, los puntos correspondientes quedan del mismo lado del centro; si k < 0, del lado opuesto.
- Su **firma en una figura**: dos segmentos (o triángulos) con lados respectivamente paralelos → hay una homotecia que lleva uno al otro, y su **centro es la intersección de las rectas que unen vértices correspondientes**.

## El baricentro y el círculo de los nueve puntos

El **baricentro** G de un triángulo es el centro de una homotecia de razón −1/2 que manda cada vértice al punto medio del lado opuesto. Por eso G divide cada mediana en razón 2:1 desde el vértice.

El **círculo de los nueve puntos** (radio R/2) es la imagen del circuncírculo bajo la homotecia de centro H (ortocentro) y razón 1/2. Esto explica en un solo párrafo por qué los pies de las alturas, los puntos medios de los lados y los puntos medios de los segmentos vértice-ortocentro son concíclicos: los nueve puntos son imágenes de seis puntos del circuncírculo bajo esa homotecia.

## Círculos tangentes

Dos círculos tienen **dos centros de homotecia** sobre la recta de centros: el **externo** (razón +R/r, del mismo lado del segmento OO′) y el **interno** (razón −R/r, entre los centros). Las tangentes comunes pasan por ellos.

Caso especial: si los círculos son **tangentes exteriormente en T**, entonces T es el centro de homotecia interno (si la tangencia es interior, T es el centro externo) y toda recta por T corta ambos círculos en puntos correspondientes —donde las tangentes a cada círculo son **paralelas** (una firma visual muy útil).

## Semejanza espiral: rotación + escala

Una semejanza espiral de centro O, razón k y ángulo θ es, en números complejos, la transformación z ↦ a·z + b donde |a| = k y arg(a) = θ. Propiedades:

- **Aparea cualquier par de segmentos**: dada AB y CD cualesquiera, existe una única semejanza espiral que lleva A↦C y B↦D.
- Su **centro** se localiza con el lema estándar: si P es la intersección de las rectas AB y CD, el centro es el segundo punto de intersección de los circuncírculos de los triángulos PAC y PBD.
- En el **círculo unitario**, el conjugado de z es 1/z y las fórmulas del circuncentro, reflexiones y pies de alturas se vuelven limpias.

## Cómo elegir

| Firma en el enunciado | Herramienta |
|---|---|
| Dos figuras con lados paralelos y semejantes | Homotecia |
| Círculos tangentes o anidados | Homotecia (el punto de tangencia es el centro interno) |
| «Razón constante» entre segmentos en varias posiciones | Homotecia (busca el centro) |
| Dos segmentos arbitrarios que deben aparearse | Semejanza espiral |
| Ángulos y escalas mezcladas, rotación evidente | Semejanza espiral (mejor vía complejos) |

## Disparadores

- «Tangente exterior común a dos círculos» → construir el trapecio de centros y radios, Pitágoras.
- «Dos triángulos semejantes con lados paralelos» → homotecia; el centro es la intersección de los lados correspondientes.
- «El baricentro divide la mediana en razón 2:1» → homotecia de razón −1/2 centrada en G.
- «Cuatro puntos que vienen de aplicar una transformación con ángulo y escala» → semejanza espiral, resolver en complejos.

## Síntesis

> **Chunk mínimo:** Homotecia de razón k y centro O: P ↦ O + k(P−O); produce figuras semejantes con lados paralelos. Firma: dos figuras con lados paralelos → hay una homotecia, su centro es la intersección de las rectas que unen correspondientes. El baricentro es el centro de la homotecia de razón −1/2 que manda vértices a puntos medios opuestos. Dos centros de homotecia para cada par de círculos (externo e interno). Semejanza espiral = rotación + homotecia (en complejos: z ↦ az+b); aparea cualquier par de segmentos; su centro es la segunda intersección de los circuncírculos de PAC y PBD (P = AB∩CD). Elegir homotecia para razones/paralelas, semejanza espiral para razones + giros.

---

*Antes del quiz: reconstruye de memoria la definición de homotecia, por qué el baricentro es un centro de homotecia de razón −1/2, los dos centros de homotecia de dos círculos y qué es una semejanza espiral en términos de números complejos.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Homotecia y semejanza espiral son transformaciones donde escala y giro explican relaciones escondidas. [[aime-geo]] las necesita para reconocer semejanza, [[engel-geo2]] aporta herramientas avanzadas, y [[zeitz-42]] muestra por que los complejos son un lenguaje natural para rotar y escalar.
<!-- GRAFO_CONEXO_OLEADA3_END -->
