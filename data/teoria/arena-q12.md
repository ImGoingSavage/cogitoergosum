# Arena Quant · Brainteasers: trucos, invariantes y conteo

Los acertijos de entrevista premian encontrar **la cantidad que no cambia** o **la reformulación que colapsa el problema**. Casi nunca hay que resolver ecuaciones: hay que ver el truco.

## Conservación — sigue lo que no cambia

- **Copa de vino blanco y otra de tinto, 100 ml cada una. Pasas 5 ml de tinto al blanco, mezclas, devuelves 5 ml de la mezcla. ¿Hay más blanco en el tinto o tinto en el blanco?** Truco: al final cada copa tiene 100 ml. Por conservación, el blanco que falta en su copa está en la otra, y viceversa: **exactamente iguales**. Nada de álgebra.
- **Lanzas el ancla del bote al fondo de la piscina. ¿Sube o baja el nivel?** En el bote, el ancla desplaza agua según su *peso*; en el fondo, según su *volumen*. Como el ancla es más densa que el agua, en el bote desplaza más → al tirarla, el nivel **baja**.

## Invariantes de conteo

- **Tableta de chocolate de n cuadritos: ¿cuántas roturas para separarlos todos?** Cada rotura aumenta el número de piezas en exactamente 1. De 1 pieza a n piezas: siempre **n − 1 roturas**, sin importar la forma. Es el invariante más limpio del capítulo.
- **Pesas para equilibrar todo entero de 1 a 40 en un solo platillo:** cada pesa entra o no entra → binario → **1, 2, 4, 8, 16, 32** (6 pesas; con 5 solo cubres 2⁵=32 combinaciones < 40).
- **Si puedes poner pesas en ambos platillos** (cada una suma, resta o no participa → ternario): **1, 3, 9, 27** bastan (3⁴ = 81 ≥ 2·40+1).

## Reformular geometría: desdoblar

- **Una hormiga va de un vértice a su opuesto en un cubo de volumen 1 m³, por la superficie. ¿Distancia mínima?** Desdobla el cubo: el camino se vuelve la diagonal de un rectángulo 1×2 → **√5 m**. El truco de aplanar convierte un problema 3D en uno plano.

## Series infinitas que se suman solas

- **Bebemos una pinta: yo tomo la mitad, tú la mitad del resto, yo la mitad de lo que queda… ¿cuánto bebe cada uno?** Yo bebo Σ 1/2^{2k+1}, tú la mitad de eso → yo bebo el **doble** que tú: **2/3 y 1/3**. La pinta entera se consume (Σ1/2^k = 1).

## Recurrencias: Fibonacci escondido

- **Conejo sube n escalones de 1 o 2 en 2. ¿Cuántas formas?** p(n) = p(n−1) + p(n−2), con p(1)=1, p(2)=2 → **Fibonacci** (p(n) = F_{n+1}).
- **¿De cuántas formas embaldosas un tablero 2×n con fichas de dominó?** Misma recurrencia → también **Fibonacci**. Cuando «la última pieza es de un tipo u otro», suele aparecer Fibonacci.

## Trampas de promedio

- **Una vuelta a 30 mph; ¿a qué velocidad la segunda para promediar 60 mph en las dos?** Trampa del promedio aritmético. 2 millas a 60 mph = 2 min; pero 1 milla a 30 mph ya consume 2 min → no queda tiempo → **imposible** (necesitarías velocidad infinita). La velocidad media es la *media armónica*, no la aritmética.
- **La nieve empieza antes del mediodía; un quitanieves arranca a las 12 con velocidad inversa al tiempo desde que nevó; recorre el doble de 12-1 que de 1-2. ¿Cuándo empezó?** Integrando α/t: x = ½(√5 − 1) horas antes del mediodía.

## Disparadores

| Señal | Jugada |
|-------|--------|
| "trasvases / mezclas" | conservación: las cantidades finales fijan el resultado |
| "¿cuántas roturas/cortes?" | invariante: cada operación cambia el conteo en 1 |
| "pesas para cubrir 1..N" | un platillo → binario; dos platillos → ternario |
| "camino sobre una superficie 3D" | desdobla a un plano, usa Pitágoras |
| "una pieza de dos tipos / subir escalones" | recurrencia → Fibonacci |
| "promediar velocidades" | media armónica, no aritmética |

> ❧ **Síntesis:** el brainteaser no pide cálculo sino *mirada*. Busca la cantidad conservada (vino, agua, piezas), reformula la geometría desdoblándola, y reconoce a Fibonacci cuando «la última pieza» bifurca en dos casos. Y desconfía siempre del promedio aritmético de velocidades.

---

*Retrieval: cierra la página y responde — (1) ¿más blanco en el tinto o al revés?; (2) roturas para n cuadritos; (3) distancia mínima de la hormiga en el cubo; (4) por qué la segunda vuelta a 60 mph es imposible.*
