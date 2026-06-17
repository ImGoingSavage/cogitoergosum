# Geometría de supervivencia II: área y semejanza

*Lección redactada para CogitoErgoSum a partir de la sección 8.3 de Zeitz (Survival Geometry II). Cubre el contenido completo de la unidad.*

## El área como lente multiplicativa

Área de un triángulo = (base × altura)/2. La consecuencia operativa, humilde y demoledora:

> **Triángulos con la misma ALTURA tienen áreas en razón de sus BASES** (y con la misma base, en razón de sus alturas).

¿Por qué eso resuelve problemas enteros? Porque permite **comparar áreas de piezas sin calcular ninguna**. En un triángulo cortado por **cevianas** (segmentos de un vértice al lado opuesto), las piezas comparten alturas por todos lados: cada razón de áreas se traduce en razón de bases y viceversa. Encadenando esas razones se demuestran las divisiones «mágicas» de los puntos de corte — sin coordenadas, sin trigonometría, sin una sola longitud explícita. La pregunta operativa frente a una figura partida: *¿qué pares de triángulos comparten altura (o base)?*

## Semejanza

Dos triángulos son **semejantes** (∼) si tienen los ángulos respectivamente iguales **y** los lados proporcionales — misma forma, distinto tamaño. Los **tres atajos** (Fact 8.3.8) — cada uno basta por sí solo:

1. **AA**: dos pares de ángulos iguales (el tercero es automático).
2. **SSS proporcional**: los tres pares de lados en la misma razón.
3. **SAS proporcional**: dos pares de lados proporcionales **y el ángulo COMPRENDIDO igual**.

**El error a vigilar (banco):** «dos lados proporcionales y un ángulo igual» NO basta si el ángulo **no es el comprendido** entre esos lados — es el primo de ASS de §8.2 (mismo caso ambiguo). Verifica siempre *cuál* ángulo es el igual.

## La fábrica estándar de semejantes (8.3.9)

> **Una paralela a un lado de un triángulo corta un triángulo semejante al original.** (AA inmediato: ángulos correspondientes por la paralela.)
>
> **Y el recíproco:** si un segmento corta dos lados en proporciones iguales, es **paralelo** al tercer lado.

Esta pareja es la fábrica: ¿necesitas semejantes y no los hay? **Traza la paralela.** ¿Necesitas una paralela? **Demuestra la proporción.** (El teorema del punto medio es el caso 1:1.)

## La configuración estrella (8.3.10): la altura a la hipotenusa

En un triángulo rectángulo con catetos a, b, hipotenusa c, traza la **altura h desde el ángulo recto** a la hipotenusa; divide a c en segmentos x (junto a a... digamos junto al cateto a) e y.

**La altura crea DOS triángulos semejantes entre sí y al original** (AA: cada uno comparte un ángulo agudo con el original y tiene su ángulo recto). De las proporciones:

- Comparando los dos pequeños entre sí: x/h = h/y → **h² = xy → h = √(xy)** — la altura es la **media geométrica** de los segmentos (¡AM-GM tiene aquí su dibujo!).
- Comparando cada pequeño con el original: a/c = x/a → **a² = cx**, y b/c = y/b → **b² = cy**.

**Pitágoras cae gratis:** suma las dos últimas: a² + b² = cx + cy = c(x + y) = c². ∎ Una configuración, tres teoremas.

## El mantra de la sección

> **Si un problema de geometría involucra RAZONES o proporciones, casi seguro necesitas triángulos semejantes. Búscalos; si no están, fabrícalos** (paralelas o perpendiculares auxiliares).

Y el protocolo de los problemas «de cuadrado inscrito / altura / proporción»: **plantea la proporción ANTES de calcular** — identifica los dos semejantes, escribe lado chico/lado grande = lado chico/lado grande, y solo entonces despeja. **El penúltimo paso es la ecuación, no el número**: quien empieza por aritmética sin tener la proporción escrita está adivinando.

*Mini-ejemplo del protocolo:* cuadrado de lado s inscrito en un triángulo de base b y altura h, con un lado sobre la base. El lado superior del cuadrado es **paralelo a la base** → el triángulo de arriba es semejante al original (la fábrica 8.3.9). Su altura es h − s, y su base es el lado superior del cuadrado, que mide s. La proporción base/altura de ambos semejantes: **s/(h − s) = b/h**. Despeja: sh = b(h − s) → s = **bh/(b + h)**. La mecánica importa más que el resultado: *semejantes → proporción → despeje*.

## Disparadores

- El enunciado pide una **RAZÓN** (x/y, AB/CD) o «divide en proporción» → semejantes: identifícalos o fabrícalos con una paralela; escribe la proporción primero.
- Figura partida por cevianas → compara áreas vía bases/alturas compartidas.
- Triángulo rectángulo con altura a la hipotenusa → h = √(xy), a² = cx, b² = cy.
- «Dos lados proporcionales y un ángulo» → verifica que sea el comprendido.
- Punto medio + paralela → teorema del punto medio y su recíproco (fábrica 1:1).

## Síntesis

> **Chunk mínimo:** Misma altura ⇒ áreas en razón de bases (y viceversa): así se comparan piezas de cevianas sin calcular nada. Semejanza: AA, SSS proporcional, SAS proporcional (el ángulo debe ser el COMPRENDIDO — primo de ASS). Fábrica 8.3.9: paralela a un lado ⇒ triángulo semejante; recíproco: proporciones iguales ⇒ paralela (punto medio = caso 1:1). Configuración estrella (altura a la hipotenusa): h² = xy, a² = cx, b² = cy — y sumando, Pitágoras gratis. Mantra: ¿razones o proporciones? → semejantes; si no están, fabrícalos; y escribe la PROPORCIÓN antes de calcular (cuadrado inscrito: s/(h−s) = b/h ⇒ s = bh/(b+h)).

---

*Antes del quiz: reconstruye de memoria los tres atajos y la fábrica con su recíproco, la configuración completa de la altura a la hipotenusa (con Pitágoras de regalo) y el principio de comparar áreas por bases compartidas.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Area y semejanza convierten una figura en relaciones de escala. [[aime-geo]] las usa con Heron, potencia y coordenadas, [[engel-geo2]] aporta herramientas avanzadas, y [[zeitz-85b]] muestra como homotecia y semejanza espiral explican por que ciertas longitudes cambian juntas.
<!-- GRAFO_CONEXO_OLEADA3_END -->
