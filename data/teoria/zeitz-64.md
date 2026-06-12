# Recurrencias: Fibonacci y Catalan

*Lección redactada para CogitoErgoSum a partir de la sección 6.4 de Zeitz (Recurrence). Cubre el contenido completo de la unidad.*

## La estrategia local

Cuando un conteo es demasiado complicado para verlo de golpe, Zeitz manda **mirar lo local**: no preguntes «¿cuántos objetos de tamaño n hay?» sino

> **¿Cómo se construye un objeto de tamaño n+1 a partir de los de tamaño ≤ n?**

Si respondes eso, obtienes una **recurrencia**. Las dos piezas para declarar el problema resuelto (al menos como algoritmo):

1. **La recurrencia** (la regla local de construcción).
2. **Los valores frontera** (los casos iniciales que arrancan la máquina).

Con ambas puedes calcular t(n) para cualquier n — y a menudo reconocer la sucesión.

## La jugada estándar: particiona según cómo TERMINAN

**El argumento del dominó:** ¿de cuántas maneras t(n) se cubre un rectángulo 2×n con fichas 1×2? Mira el **extremo derecho** de un cubrimiento cualquiera. Solo hay dos posibilidades:

- Termina en **un dominó vertical** → al quitarlo queda un 2×(n−1) cubierto de cualquiera de las t(n−1) formas.
- Termina en **dos dominós horizontales** apilados → al quitarlos queda un 2×(n−2): t(n−2) formas.

**La partición es legítima** porque los dos casos son **disjuntos** (el extremo es vertical o no lo es — no hay tercera opción ni traslape) y **agotan** todos los cubrimientos. Entonces:

t(n) = t(n−1) + t(n−2), con t(1) = 1, t(2) = 2 → 1, 2, 3, 5, 8, 13, … **Fibonacci.**

**El acertijo de la escalera es el mismo problema disfrazado:** subes 10 escalones con pasos de 1 o 2. Particiona según el **último paso**: fue de 1 (quedaban e(9) maneras) o de 2 (e(8)). e(n) = e(n−1) + e(n−2), e(1)=1, e(2)=2 → e(10) = **89**. (La tabla: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89.)

## Identificar sucesiones: el principio de unicidad

> **Misma recurrencia + mismos valores iniciales = misma sucesión.**

Para afirmar «mi conteo ES Fibonacci» no necesitas magia: demuestra que tu conteo satisface t(n) = t(n−1) + t(n−2) y **cuadra dos valores frontera**. Eso es todo — la recurrencia propaga la igualdad para siempre. Es el equivalente contable de «misma ecuación diferencial + mismas condiciones iniciales».

## Catalan: cuando el corte produce PRODUCTOS

Fibonacci salió de condicionar en un **extremo lineal** (el borde derecho). La recurrencia de **Catalan** sale de condicionar en un **elemento estructural interno**.

**Triangulaciones de un polígono convexo:** sea t(n) el número de maneras de partir un polígono de n+2 lados en triángulos con diagonales que no se cruzan. Fija una arista «base» y pregunta: ¿con qué tercer vértice forma triángulo la base? Al elegirlo, el polígono queda partido en el triángulo de la base y **dos polígonos menores, uno a cada lado** — y sus triangulaciones se eligen **independientemente** una de otra. Decisiones independientes = **producto** (§6.1):

t(n) = Σ t(u)·t(v) sobre u + v = n − 1 (con t(0) = 1)

**Por qué productos y no solo sumas como en Fibonacci:** porque el corte de Fibonacci deja **una sola** pieza restante (suma sobre casos), mientras que el corte de Catalan deja **dos piezas que se completan independientemente** — cada caso aporta el producto de sus dos conteos, y luego se suma sobre los casos. Suma de productos: esa es la firma de Catalan.

Los números de Catalan 1, 1, 2, 5, 14, 42, … aparecen dondequiera que un objeto se parta en dos sub-objetos independientes al condicionar: **triangulaciones, paréntesis balanceados** (condiciona en la pareja del primer paréntesis), **caminos reticulares que no cruzan la diagonal**, árboles binarios… Reconocer la firma ahorra rederivarla.

## Fórmulas cerradas: verificar es mecánico, encontrar no

¿Te dan una fórmula cerrada (como la de Binet para Fibonacci, F(n) = (φⁿ − ψⁿ)/√5)? **Verificarla es mecánico:** comprueba que satisface la recurrencia y los valores frontera — por el principio de unicidad, listo. **Encontrarla** es otra historia: para eso existen las funciones generatrices (§4.3, siguiente unidad) y la teoría de recurrencias lineales. Moraleja práctica: no le temas a «demuestra que F(n) = fórmula» — casi siempre es inducción mecánica sobre la recurrencia.

## Disparadores

- Contar objetos de tamaño n con **restricción local** («sin dos seguidos», «sin tres consecutivos», «termina en…») → primer reflejo: **particiona según cómo termina el objeto** y busca la recurrencia. Antes de confiar: verifica que los casos sean **disjuntos y agoten** todo, y cuadra los valores frontera a mano (n = 1, 2, 3).
- El conteo coincide con Fibonacci en recurrencia y dos valores → ES Fibonacci.
- Al condicionar, el objeto se parte en **dos piezas independientes** → suma de productos: huele a Catalan.
- Te dan la fórmula cerrada → verifica recurrencia + frontera (inducción), no la re-derives.

## Síntesis

> **Chunk mínimo:** Si el conteo no se ve de golpe, pregunta cómo se construye el objeto de tamaño n desde los menores: recurrencia + valores frontera = problema resuelto (como algoritmo). Jugada estándar: particiona según cómo TERMINA (dominó 2×n: vertical → t(n−1), dos horizontales → t(n−2) ⇒ Fibonacci; escalera de 10 con pasos 1-2 → 89) — verificando que los casos sean disjuntos y agoten. Unicidad: misma recurrencia + mismos iniciales = misma sucesión (así se identifica Fibonacci, y así se verifican fórmulas cerradas tipo Binet: inducción mecánica). Catalan: el corte interno deja DOS piezas independientes ⇒ suma de PRODUCTOS, t(n) = Σ t(u)t(v) (triangulaciones, paréntesis, caminos bajo la diagonal).

---

*Antes del quiz: reconstruye de memoria la estrategia local con sus dos piezas, el argumento completo del dominó (incluida la legitimidad de la partición), la respuesta de la escalera y por qué Catalan multiplica.*
