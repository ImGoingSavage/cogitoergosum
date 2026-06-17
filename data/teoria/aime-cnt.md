# AIME · Conteo y probabilidad: complemento, biyección y casos

*Lección redactada para CogitoErgoSum a partir de problemas de conteo y probabilidad del AIME (American Invitational Mathematics Examination). Cubre el contenido completo de la unidad.*

## La idea central

El conteo en olimpiadas es el arte de **no duplicar ni omitir**. Cada técnica es una estrategia para hacer eso: el conteo complementario evita una condición enredada contando su ausencia; la inclusión-exclusión corrige el solapamiento; las estrellas y barras traduce distribuciones en caminos; la biyección colapsa el problema en uno que ya conoces. La probabilidad, en espacios equiprobables, es siempre conteo.

## Conteo complementario

Cuando «lo que quieres» tiene condiciones complicadas, pero «lo que NO quieres» es sencillo:

> Total − complemento = lo que quieres.

**Firma**: «al menos uno», «no todos iguales», «contiene al menos un X». Calcularlo directamente requiere inclusión-exclusión; la negación suele ser «ninguno», que es un producto directo.

Ejemplo: ¿cuántas cadenas binarias de longitud 10 tienen al menos un 1? Total = 2¹⁰ = 1024; ningún 1: solo 1 cadena (0000000000). Respuesta: 1023.

## Inclusión-exclusión

Para contar elementos en la unión de conjuntos:

> |A∪B∪C| = |A| + |B| + |C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|.

**Para complementos**: el número de elementos que **no** están en ninguno de A₁, …, A_k es:

> Total − Σ|Aᵢ| + Σ|Aᵢ∩Aⱼ| − ⋯ ± |A₁∩⋯∩Aₖ|.

Los términos de intersección suelen simplificarse si las propiedades son independientes o si la intersección de k conjuntos tiene una cuenta uniforme.

**Firma**: «que evite las propiedades P₁, P₂, …, P_k simultáneamente», «desórdenes» (permutaciones sin punto fijo), «distribución sin casillas vacías».

## Estrellas y barras

El número de soluciones enteras **no negativas** de x₁ + x₂ + ⋯ + xₖ = n es:

> C(n+k−1, k−1).

Para soluciones **positivas** (xᵢ ≥ 1): sustituye yᵢ = xᵢ − 1 (rango 0 a n−k) y cuenta C(n−1, k−1). **Confundir las dos versiones es el error más frecuente del AIME.**

Generalización: si xᵢ ≤ M_i para algún i, aplica inclusión-exclusión sobre la restricción violada.

## Biyección

Traducir el conteo a otro conjunto que ya sabes contar. El ejemplo canónico: los **subconjuntos de {1,…,n} sin dos elementos consecutivos** están en biyección con las cadenas binarias de longitud n sin dos 1's seguidos (la posición i lleva 1 exactamente si el elemento i está en el subconjunto). Su número f(n) cumple f(n) = f(n−1) + f(n−2) —según el último bit sea 0 o 1— con f(0)=1, f(1)=2, de donde f(n) = Fibonacci(n+2). La biyección colapsa el problema a una recurrencia conocida.

**Protocolo**: busca una función f del conjunto A al conjunto B tal que f sea biyectiva (inyectiva + sobreyectiva). Calcular |B| es equivalente a calcular |A|, y B es generalmente más sencillo.

## Probabilidad como conteo

En un espacio equiprobable:

> P(evento) = (casos favorables) / (casos totales).

Las técnicas de conteo se aplican al numerador y al denominador por separado. Si los eventos **no** son igualmente probables, trabaja con probabilidades condicionales o con la esperanza.

**Linealidad de la esperanza**: E[X₁ + X₂ + ⋯ + Xₙ] = E[X₁] + ⋯ + E[Xₙ] aunque las variables **no sean independientes**. Esto permite calcular «¿cuántos elementos esperados tienen la propiedad P?» descomponiendo en indicadores Xᵢ = 1 si el i-ésimo elemento tiene la propiedad. Cada E[Xᵢ] es solo una probabilidad puntual, fácil de calcular.

## Disparadores

- «Al menos uno» o «no todos» → conteo complementario (Total − ninguno).
- «Evitar varias propiedades simultáneamente» → inclusión-exclusión.
- «Distribuir n objetos en k cajas» → estrellas y barras; distinguir si objetos/cajas son distintos o iguales.
- «Contar un conjunto con estructura secuencial» → busca la biyección con cadenas, caminos o subconjuntos conocidos.
- «¿Cuántos en promedio?» o «¿cuántos esperados?» → linealidad de la esperanza con indicadores.
- «Suma de consecutivos que da N» → traducción a factorizaciones de 2N con paridades opuestas.

## Síntesis

> **Chunk mínimo:** Complementario: Total − «ninguno» para «al menos uno». Inclusión-exclusión: |A∪B∪C|=Σ|Aᵢ|−Σ|Aᵢ∩Aⱼ|+…; para «que evite todas»: Total − Σ + Σ − …. Estrellas y barras: enteros no negativos C(n+k−1,k−1); positivos C(n−1,k−1) — el cambio es crucial. Biyección: hallar f biyectiva al conjunto más fácil; subconjuntos sin consecutivos ↔ Fibonacci. Probabilidad = conteo en espacio equiprobable. Linealidad de esperanza: descomponer en indicadores Xᵢ, E[ΣXᵢ]=ΣE[Xᵢ] incluso con dependencias.

---

*Antes del quiz: reconstruye de memoria la fórmula de estrellas y barras para no negativas vs. positivas, la fórmula de inclusión-exclusión para la unión de tres conjuntos, la biyección de subconjuntos sin consecutivos y el enunciado de la linealidad de la esperanza.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Conteo y probabilidad AIME vuelven tacticas a las tecnicas de [[zeitz-61]], [[zeitz-62]] y [[zeitz-63]]. [[arena-b1]] da el hogar conceptual: suma, producto, complemento y casos son el mismo lenguaje que luego se mide como probabilidad.
<!-- GRAFO_CONEXO_OLEADA3_END -->
