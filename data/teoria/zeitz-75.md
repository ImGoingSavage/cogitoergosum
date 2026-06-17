# Ejemplos instructivos: primos, polinomios y collares

*Lección redactada para CogitoErgoSum a partir de la sección 7.5 de Zeitz (Miscellaneous Instructive Examples). Cubre el contenido completo de la unidad.*

## El polinomio de Euler: 40 confirmaciones no son una prueba

f(n) = n² + n + 41 da **primos para n = 0, 1, …, 39**. Cuarenta éxitos seguidos. ¿Demuestra algo? No — y lo notable es que **era previsible sin calculadora** que no podía dar primos siempre: mira **el caso que se delata a sí mismo**. En n = 41:

f(41) = 41² + 41 + 41 = 41·(41 + 1 + 1) — múltiplo obvio de 41.

(También n = 40: f(40) = 1600 + 40 + 41 = 1681 = 41².) No hizo falta probar nada: el propio 41 del polinomio grita dónde buscar el fallo. **Moraleja general:** ante «¿esta fórmula siempre da primos?», no acumules confirmaciones — busca el valor de n que **convierta a la fórmula en múltiplo evidente de algo** (típicamente, sustituir la propia constante del polinomio).

## El teorema: ningún polinomio da solo primos

> **Ningún polinomio no constante f con coeficientes enteros produce primos para todo entero positivo n.**

*Demostración.* Toma cualquier u con f(u) = p (algún valor primo; si ningún valor es primo, ya terminamos). Considera f(u + kp) para k = 1, 2, 3, …. Al expandir cada potencia (u + kp)ʲ con el binomio, **todo término que contenga kp es múltiplo de p**; lo que sobrevive sin p es exactamente uʲ. Agrupando:

f(u + kp) = f(u) + (múltiplos de p) ≡ f(u) ≡ 0 (mod p)

Así que **p divide a f(u + kp) para todo k**: el polinomio repite el factor p en una progresión aritmética completa. Para que esos valores fueran primos, tendrían que ser ±p siempre — pero un polinomio no constante toma cada valor a lo más un número finito de veces (grado n ⇒ a lo más n raíces de f(x) = p), y |f| → ∞. Luego algún f(u + kp) es compuesto. ∎

**La jugada técnica que enseña esta prueba:** al expandir f(u + p), **NO simplifiques a ciegas** — agrupa los términos para **EXTRAER f(u)** y verifica que el resto es múltiplo de p. Es «incorporar la hipótesis antes de calcular»: el cálculo se organiza alrededor de lo que quieres ver, no al revés. Ese hábito (calcular CON dirección) separa las cuentas que iluminan de las que entierran.

## La prueba del collar del pequeño Fermat

> **Si p es primo, entonces p | aᵖ − a.**

*Demostración combinatoria (collares).* Cuenta las cadenas de p perlas donde cada perla tiene uno de a colores: hay aᵖ. Quita las a cadenas monocromáticas: quedan **aᵖ − a cadenas no monocromáticas**. Ahora une las puntas de cada cadena para formar collares y agrupa las cadenas por **rotación** (dos cadenas son equivalentes si una es rotación de la otra). Afirmación: **cada órbita de rotaciones tiene exactamente p cadenas**. ¿Por qué? Si una cadena coincidiera consigo misma al rotarla d lugares con 0 < d < p, su patrón sería periódico de período d | p — pero p es primo, así que d = 1: la cadena sería monocromática, y esas ya las quitamos. Luego las aᵖ − a cadenas se parten en órbitas de tamaño exactamente p, y por lo tanto **p | aᵖ − a**. ∎

(De ahí, si p ∤ a, cancela una a: aᵖ⁻¹ ≡ 1 (mod p) — la forma de §7.2.)

**La técnica desnuda: contar objetos en órbitas = dividir.** Si una acción agrupa tus objetos en órbitas del mismo tamaño k, entonces k divide al total. La primalidad de p fue lo que garantizó órbitas completas — fíjate dónde se usó cada hipótesis.

## Experimentar → conjeturar → probar

El tercer ejemplo instructivo es de método puro. Estudia f(n) = n³ + n + 1: ¿da infinitos compuestos? Tabula:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| f(n) | 3 | 11 | 31 | 69 | 131 | 223 | 351 | 521 | 739 | 1011 |

Compuestos en n = 4, 7, 10… — ¡cada 3! La tabla **experimental** apunta directo al argumento **modular**: ¿qué pasa mod 3 cuando n ≡ 1 (mod 3)? f(n) ≡ 1 + 1 + 1 = 3 ≡ 0 (mod 3). Conjetura confirmada y demostrada: f(3k+1) es siempre múltiplo de 3 (y > 3), infinitos compuestos. El flujo completo de §2.2 — manos sucias, patrón, conjetura — rematado con la herramienta de §7.2.

## Disparadores

- «¿Puede esta fórmula dar siempre primos?» → en orden: (1) busca el caso que se delata (sustituye la constante del polinomio); (2) si es polinomio, el teorema general: f(u + kp) ≡ 0 (mod p); (3) tabula y busca el patrón modular.
- «Demuestra que la sucesión contiene infinitos compuestos» → tabula, detecta la progresión donde cae el factor, demuestra con congruencias.
- Conteo donde una acción cíclica agrupa en órbitas iguales → divide; vigila qué hipótesis garantiza órbitas completas.

## Síntesis

> **Chunk mínimo:** n² + n + 41 da primos hasta n = 39, pero el caso que se delata estaba a la vista: f(41) = 41·43 (sustituye la propia constante). Teorema: ningún polinomio no constante da solo primos — si f(u) = p, el binomio muestra f(u + kp) ≡ f(u) ≡ 0 (mod p) para todo k, y un polinomio toma cada valor finitas veces; la jugada: expande EXTRAYENDO f(u), calcula con dirección. Collar de Fermat: aᵖ − a cadenas no monocromáticas se parten en órbitas de rotación de tamaño exactamente p (período d | p y p primo ⇒ d = 1, excluido) ⇒ p | aᵖ − a; técnica desnuda: órbitas iguales ⇒ el tamaño divide al total. Y el flujo completo: tabula (n³+n+1), detecta el patrón cada 3, demuestra mod 3.

---

*Antes del quiz: reconstruye de memoria por qué n²+n+41 estaba condenado (el caso que se delata), la prueba completa de que ningún polinomio da solo primos (con la jugada de extraer f(u)) y la prueba del collar con el papel exacto de la primalidad.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Los ejemplos de primos, polinomios y collares son mapas de transferencia: [[zeitz-71]] explica las restricciones aritmeticas, [[zeitz-43]] muestra como empaquetar conteos, y [[arena-q12]] recuerda que simetrias e invariantes suelen ser el atajo que evita enumerar todo.
<!-- GRAFO_CONEXO_OLEADA3_END -->
