# Ecuaciones diofánticas: factoriza y filtra

*Lección redactada para CogitoErgoSum a partir de la sección 7.4 de Zeitz (Diophantine Equations). Cubre el contenido completo de la unidad.*

## Las cuatro preguntas

Una **diofántica** es una ecuación cuyas soluciones se buscan en los enteros. Ante cualquiera, Zeitz manda hacer cuatro preguntas, en este orden:

1. **¿Está en forma simple?** Divide factores comunes, simplifica; a menudo conviene **suponer las variables coprimas** y reconstruir el caso general después (como en el análisis de ternas pitagóricas).
2. **¿Existe alguna solución?** Busca una a mano — un ejemplo orienta todo.
3. **¿Se puede probar que NO hay?** Esta conviene atacarla **temprano**: si la respuesta es no, un filtro modular lo zanja en dos líneas y te ahorra la búsqueda; y si los filtros no encuentran obstrucción, eso mismo sugiere que sí hay soluciones y que toca construirlas.
4. **¿Puedo encontrarlas TODAS?** La pregunta fuerte: parametrizar o agotar el conjunto completo.

## Lineales: teoría completa

Para **ax + by = c** (a, b, c enteros) la historia es completa:

> Hay solución ⟺ **mcd(a, b) | c**.

(⇒: mcd(a,b) divide al lado izquierdo siempre. ⇐: el algoritmo de Euclides al revés expresa el mcd como combinación ax₀ + by₀ y se escala.)

**Ejemplo del banco:** 3x + 21y = 19 — mcd(3,21) = 3, y 3 ∤ 19: **sin soluciones**, fin.

Y de una solución salen **todas**: si (x₀, y₀) funciona, la familia completa es

x = x₀ + (b/d)t,  y = y₀ − (a/d)t,  con d = mcd(a,b), t ∈ ℤ

(las soluciones forman una progresión: la diferencia entre dos soluciones resuelve la homogénea ax + by = 0).

## Táctica 1 — FACTORIZA: (algo)·(algo) = constante

La jugada estrella para no lineales: **maniobra el álgebra hasta que un producto iguale a una constante**. Como los factores son enteros, solo hay **finitas** opciones (los divisores de la constante) — y se revisan una a una.

**El truco a interiorizar — completar el producto:** xy − 4x − 4y + 8 = 0 casi factoriza; súmale a ambos lados **la constante que falta**: xy − 4x − 4y + 16 = 8, es decir **(x − 4)(y − 4) = 8**. Ahora enumera los pares de divisores de 8 (incluidos negativos) y filtra. Es el «completar el cuadrado» del mundo multiplicativo — llámalo *factorización SFFT* o como quieras, pero hazlo reflejo.

**Ejemplo resuelto del banco — 1/x + 1/y = 1/6 en enteros positivos:** multiplica por 6xy: 6y + 6x = xy → xy − 6x − 6y = 0 → suma 36: **(x − 6)(y − 6) = 36**. Con x, y > 0, ambos factores son > −6, y su producto 36 > 0 con suma compatible fuerza ambos positivos. Pares ordenados de divisores positivos de 36: 36 = 1·36 = 2·18 = 3·12 = 4·9 = 6·6 (y sus reversos) → 36 tiene 9 divisores → **9 parejas ordenadas** (x, y) = (7,42), (8,24), (9,18), (10,15), (12,12), (15,10), (18,9), (24,8), (42,7).

**Otro del banco — x² − y² = 10:** «probé valores pequeños y no encontré» NO es demostración (¿hasta dónde probaste? ¿por qué bastaría?). La de verdad: (x − y)(x + y) = 10, y **x − y y x + y tienen la misma paridad** (su suma 2x es par). Producto de dos pares es múltiplo de 4 (10 no lo es); producto de dos impares es impar (10 no lo es). **Sin soluciones.** ∎ — dos líneas, todas las soluciones descartadas de un golpe.

## Táctica 2 — FILTRA: mira la ecuación módulo n

Si los dos lados de la ecuación **no pueden coincidir en Zₙ** para algún n, no hay soluciones enteras — punto. El arte es elegir el módulo astuto:

- **Cuadrados** → mod 4 (residuos {0,1}) o mod 8 ({0,1,4}).
- **Cubos** → mod 9 (residuos {0, ±1}) o mod 7.
- Potencias de 2, dígitos → mod 3, 9, 10.

Ejemplo de molde: x² + y² = 4z + 3 es imposible — mod 4, la izquierda solo alcanza {0,1,2} y la derecha es 3.

El filtro también **restringe** sin matar: «mod 4 fuerza a x impar» reduce el espacio antes de factorizar. Filtra primero, factoriza después — o al revés: son las **dos primeras jugadas ante cualquier diofántica no lineal**, y el orden lo decide qué estructura veas (¿casi-producto? factoriza; ¿cuadrados/cubos sueltos? filtra).

## Disparadores

- ax + by = c → mcd | c y familia paramétrica. mcd ∤ c → no hay nada que buscar.
- xy con términos lineales → completa el producto: (x−a)(y−b) = const.
- 1/x + 1/y = 1/n y parientes → multiplica y completa el producto.
- Cuadrados o cubos con constantes sueltas → filtro modular (4, 8, 9).
- «No encontré soluciones probando» → eso es conjetura; la demostración es factorizar o filtrar.

## Síntesis

> **Chunk mínimo:** Cuatro preguntas: ¿forma simple (coprimiza)?, ¿hay una solución?, ¿se puede probar que NO hay? (atácala temprano), ¿puedo hallarlas TODAS? Lineales: ax + by = c tiene solución ⟺ mcd(a,b) | c (3x+21y = 19: no), y de una salen todas: x₀ + (b/d)t, y₀ − (a/d)t. Táctica 1, FACTORIZA: completa el producto hasta (algo)(algo) = constante — 1/x + 1/y = 1/6 → (x−6)(y−6) = 36 → 9 parejas; x² − y² = 10: x−y y x+y tienen la misma paridad ⇒ producto ≡ 0 mod 4 o impar ⇒ imposible. Táctica 2, FILTRA mod n: cuadrados → 4 u 8, cubos → 9 o 7 (x²+y² = 4z+3: izquierda nunca es 3 mod 4). «No encontré probando» es conjetura, no prueba.

---

*Antes del quiz: reconstruye de memoria las cuatro preguntas, el criterio de las lineales con el ejemplo 3x+21y=19, la maniobra de completar el producto con 1/x+1/y=1/6 y la demostración limpia de x²−y²=10.*
