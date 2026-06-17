# AIME · Geometría: Herón, potencia de un punto y coordenadas

*Lección redactada para CogitoErgoSum a partir de problemas de geometría del AIME (American Invitational Mathematics Examination). Cubre el contenido completo de la unidad.*

## El contexto del AIME geométrico

Los problemas de geometría del AIME suelen mezclar longitudes, áreas y círculos en una sola figura, y piden un número exacto (a veces como m+n de una fracción irreducible). Las herramientas preferidas son **métricas concretas** —Herón para el área de un triángulo de lados enteros, potencia del punto para relaciones con círculos— y el **coordinate bash** cuando todo lo demás se enreda.

## El triángulo 13-14-15 y las fórmulas del triángulo

El triángulo de lados 13, 14, 15 es el *workhorse* del AIME: sus fórmulas son exactas y vale memorizarlas.

Con s = (13+14+15)/2 = 21:

- **Área** (Herón): K = √(s(s−a)(s−b)(s−c)) = √(21·8·7·6) = √7056 = **84**.
- **Inradio**: r = K/s = 84/21 = **4**.
- **Circunradio**: R = abc/(4K) = (13·14·15)/(4·84) = 2730/336 = **65/8**.
- Altura sobre el lado de 14: h = 2K/14 = 12.

En general, para **cualquier triángulo con lados a, b, c enteros**: Herón da K, luego r = K/s, y R = abc/(4K). Si K no sale entera, verifica si el triángulo es acutángulo o rectángulo (en AIME, los triángulos de lados enteros suelen tener K entera o ser del tipo pythagorean).

## Potencia de un punto

Fija un punto P y un círculo. Para **toda recta por P** que corte al círculo en X e Y, el producto PX · PY es constante (la «potencia» de P).

- P **exterior** al círculo: potencia positiva. Las dos tangentes desde P tienen longitud √(potencia).
- P **sobre** el círculo: potencia cero.
- P **interior**: potencia negativa; PX · PY sigue siendo constante en valor absoluto para cuerdas que pasan por P.

**Corolario de las tangentes**: si desde P se trazan dos tangentes al círculo, que tocan en T₁ y T₂, entonces PT₁ = PT₂ = √(potencia). Las tangentes desde un punto exterior son iguales.

**El recíproco certifica concíclicos**: si PA · PB = PC · PD (con la configuración correcta de signos y orden sobre las rectas), entonces A, B, C, D están en un círculo.

Aplicación frecuente: en una figura con una cuerda AB y una tangente desde un punto P en la cuerda prolongada, PT² = PA · PB da PT directamente.

## Semejanza y razones

Los triángulos semejantes aparecen en casi toda figura del AIME (ángulos iguales por paralelas, ángulos inscritos en el mismo arco, ángulos en un círculo). El protocolo:

1. Identifica el par semejante (por AA: dos ángulos iguales → semejantes).
2. Escribe la razón de semejanza k = lado₁/lado₂.
3. Traduce: todos los lados del primer triángulo son k veces los correspondientes del segundo.

La semejanza **transporta razones** sin necesidad de coordenadas: es la herramienta «limpia» antes del coordinate bash.

## Coordinate bash

Cuando la figura tiene muchas perpendiculares, o piden una longitud exacta en una figura con ángulos rectos, **coloca ejes**:

- Pon el origen en el vértice donde más términos se anulen (esquina de un ángulo recto, centro de un círculo).
- Asigna coordenadas sencillas a los puntos dados (enteros o semienteros si es posible).
- Calcula la longitud pedida por la fórmula de distancia o álgebra directa.

El coordinate bash no es elegante pero es **robusto**: si la cuenta es limpia desde el principio (coordenadas pequeñas, muchos términos nulos), raramente falla. El riesgo es la explosión algebraica si el origen se elige mal.

## La forma del resultado en el AIME

La respuesta puede pedirse en varias formas:

- El número directo (si es entero entre 0 y 999).
- **m + n** donde la longitud es √(m/n) con m/n irreducible (o m/n irreducible directamente).
- **p + q** donde el área o longitud es p + q√r con r libre de cuadrados.

Leer exactamente qué número reportar es tan importante como el cálculo.

## Disparadores

- «Triángulo con tres lados dados» → Herón para K, luego r = K/s y R = abc/(4K).
- «Tangentes y secantes desde un punto exterior» → potencia del punto; tangente² = secante·secante exterior.
- «Cuatro puntos concíclicos» → potencia del punto (recíproco) o ángulos iguales en el arco.
- «Figura con ángulos rectos o perpendiculares» → coordinate bash desde el ángulo recto.
- «Triangulos con ángulos iguales (paralelas o inscriptos)» → semejanza AA.

## Síntesis

> **Chunk mínimo:** Herón: K=√(s(s−a)(s−b)(s−c)); r=K/s; R=abc/(4K). El 13-14-15: K=84, r=4, R=65/8. Potencia del punto PX·PY=constante para toda recta por P; tangentes desde P exterior: PT=√(potencia) → PT₁=PT₂; recíproco: PA·PB=PC·PD ⟹ concíclicos. Semejanza AA: identificar el par, escribir la razón, transportar todas las longitudes. Coordinate bash: origen en el ángulo recto o centro de simetría para minimizar la cuenta. Resultado en AIME: puede ser m+n (fracción) o p+q (radical); leer qué reportar.

---

*Antes del quiz: reconstruye de memoria la fórmula de Herón con los datos del 13-14-15, el enunciado de la potencia del punto (con el caso tangente), el recíproco para concíclicos y cuándo usar coordinate bash.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

La geometria AIME exige elegir rapido entre Heron, potencia, coordenadas y semejanza. [[zeitz-82]] y [[zeitz-83]] construyen los fundamentos, mientras [[engel-geo2]] ofrece herramientas avanzadas para convertir el diagrama en relaciones calculables.
<!-- GRAFO_CONEXO_OLEADA3_END -->
