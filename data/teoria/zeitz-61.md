# Contar: sumar, multiplicar, dividir

*Lección redactada para CogitoErgoSum a partir de la sección 6.1 de Zeitz (Introduction to Counting). Cubre el contenido completo de la unidad.*

## Las tres operaciones del conteo

El buen conteo no es recordar fórmulas: es saber **cuál operación toca**.

- **SUMA** cuando partes en **casos disjuntos**: «sopa O ensalada» (y nada es ambas). Si A y B no se traslapan, |A ∪ B| = |A| + |B|.
- **MULTIPLICA** cuando encadenas **decisiones independientes**: «sopa Y ensalada» — 4 sopas y 5 ensaladas dan 4 × 5 menús. Vale siempre que el número de opciones de cada etapa no dependa de *cuál* opción se tomó antes (aunque las opciones mismas cambien).
- **DIVIDE** cuando tu método **sobrecuenta uniformemente**: si cada objeto que quieres contar fue contado exactamente k veces, la cuenta verdadera es (tu cuenta)/k. Dividir es el corrector del orden irrelevante y de las repeticiones.

Mini-ejemplos: suma — palabras de 1 letra o de 2 letras: 26 + 26². Producto — placas de letra y dígito: 26 × 10. División — parejas de baile contadas como (persona A, persona B) ordenadas: divide entre 2.

## Permutaciones: elección CON orden

**P(n, r)** = maneras de elegir r objetos de n **en orden** (presidente, secretario, vocal…):

P(n, r) = n(n−1)(n−2)⋯(n−r+1)  (r factores)

**Cuidado con el off-by-one:** el último factor es (n − r + **1**), no (n − r). Verifícalo con un caso trivial: P(5, 5) debe terminar en 1, y en efecto 5·4·3·2·1. Caso especial: P(n, n) = n! (todas las ordenaciones).

## La fórmula Mississippi: repetidos → divide

¿Anagramas de una palabra con letras repetidas? Cuenta **como si todas fueran distintas** y **divide por las permutaciones internas de cada grupo de repetidas** (reordenar las repetidas entre sí no produce un anagrama nuevo):

MISSISSIPPI: 11 letras = 1 M, 4 I, 4 S, 2 P → 11!/(4!·4!·2!)

GAUSS: 5 letras con la S doble → 5!/2! = 60, no 120 — cada anagrama «verdadero» fue contado 2 veces (las dos S intercambiadas).

**Ejercicio del banco — ENSENADA:** 8 letras = E×2, N×2, A×2, S, D → 8!/(2!·2!·2!) = 40320/8 = **5040**.

## Combinaciones: dividir mata el orden

**C(n, r)** («n en r») = maneras de elegir r objetos de n **sin orden** (un comité):

C(n, r) = P(n, r)/r! = n!/(r!(n−r)!)

La división entre r! es exactamente la corrección por sobreconteo: cada comité de r personas fue contado r! veces por P (una por cada orden de elección).

**El error clásico:** «comités de 3 entre 10: son 10·9·8 = 720». Eso contó **tripletas ordenadas** — presidente, secretario y vocal, no comités. Cada comité {x, y, z} apareció 3! = 6 veces. Corrección: 720/6 = C(10,3) = **120**. La diferencia entre «elegir un comité» y «elegir presidente, secretario y vocal» ES la diferencia entre C y P.

## Argumentos combinatorios: contar lo mismo de dos maneras

La técnica más elegante de la sección: demostrar una identidad **contando la misma cosa de dos formas**. Nada de álgebra; las dos cuentas son correctas, luego son iguales.

- **Pascal:** C(n, r) = C(n−1, r−1) + C(n−1, r). Cuenta los comités de r entre n personas separando por una pregunta: *¿incluyo o no a la primera persona?* Si sí: faltan r−1 de las n−1 restantes. Si no: los r salen de las n−1 restantes. Casos disjuntos que agotan → suma. ∎
- **Suma de la fila:** C(n,0) + C(n,1) + ⋯ + C(n,n) = 2ⁿ. Ambos lados cuentan **los subconjuntos de un conjunto de n elementos**: la izquierda por tamaño (disjuntos, suma), la derecha por decisiones (cada elemento: ¿entra o no? — n decisiones binarias, producto). ∎ Esa técnica se llama **argumento combinatorio** (o demostración biyectiva/por conteo doble).

## El triángulo de Pascal y el binomio

Las C(n, r) forman el triángulo de Pascal (cada entrada = suma de las dos de arriba — eso ES la identidad de Pascal). Y son los coeficientes del **binomio**:

(x + y)ⁿ = Σ C(n, k) xᵏ yⁿ⁻ᵏ

¿Por qué? Al expandir (x+y)(x+y)⋯(x+y), cada término elige x o y de cada factor; el término xᵏyⁿ⁻ᵏ aparece una vez por cada **elección de k factores** que aportan x: C(n, k) veces. El binomio es un conteo.

## Disparadores

- «O» disjunto → suma. «Y» en etapas → producto. «El orden no importa» / objetos repetidos → divide.
- «¿De cuántas formas…?» con roles distintos → P; con grupo sin roles → C.
- Letras/objetos repetidos → Mississippi.
- Identidad con C(n,k) → intenta contar una misma colección de dos maneras antes que el álgebra.

## Síntesis

> **Chunk mínimo:** Tres operaciones: SUMA en casos disjuntos («o»), MULTIPLICA en decisiones independientes encadenadas («y»), DIVIDE cuando sobrecuentas uniformemente k veces. P(n,r) = n(n−1)⋯(n−r+1) elige CON orden (off-by-one: último factor n−r+1). Mississippi: repetidos → cuenta como distintos y divide por las permutaciones internas (ENSENADA: 8!/(2!·2!·2!) = 5040). C(n,r) = P(n,r)/r! mata el orden — el error de los comités: 10·9·8 cuenta tripletas ordenadas; divide entre 3! → 120. Argumento combinatorio = contar lo mismo de dos maneras: Pascal (¿incluyo a la primera persona o no?) y 2ⁿ = Σ C(n,k) (subconjuntos por tamaño vs. n decisiones binarias). Binomio: (x+y)ⁿ = Σ C(n,k)xᵏyⁿ⁻ᵏ — es un conteo de elecciones.

---

*Antes del quiz: reconstruye de memoria cuándo sumar/multiplicar/dividir con un ejemplo propio de cada una, la fórmula Mississippi, la corrección del error de los comités y el argumento combinatorio de 2ⁿ.*
