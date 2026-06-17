# Primos y divisibilidad: el Teorema Fundamental de la Aritmética

*Lección redactada para CogitoErgoSum a partir de la sección 7.1 de Zeitz (Primes and Divisibility). Cubre el contenido completo de la unidad.*

## Euclides: hay infinitos primos

La demostración que todo resolvedor debe poder **reproducir sin mirar**:

> Supón que la lista de primos es completa y finita: p₁, p₂, …, p_N. Considera
>
> **Q = p₁·p₂⋯p_N + 1   (la movida crux)**
>
> Q deja residuo 1 al dividirse entre cualquier pᵢ, así que **ningún primo de la lista divide a Q**. Pero Q > 1 tiene *algún* divisor primo (todo entero > 1 lo tiene). Ese primo no está en la lista — la lista no era completa. Contradicción: hay infinitos primos. ∎

**El malentendido clásico:** «Q siempre es primo; por eso funciona». **Falso.** Q puede ser compuesto: 2·3·5·7·11·13 + 1 = 30031 = 59 × 509. La prueba **no** afirma que Q sea primo — solo que **sus factores primos son nuevos** (ninguno de la lista lo divide). Con eso basta para la contradicción. Distinguir lo que un argumento usa de lo que no usa es entrenamiento de lectura fina.

Nota la arquitectura: tesis «negativa» (no hay una lista finita completa) → **contradicción** (§2.3), y la creatividad está en *construir el objeto* Q que revienta la suposición.

## El Teorema Fundamental de la Aritmética (TFA)

Dos afirmaciones, y la segunda es la profunda:

1. **Existencia:** todo entero n > 1 se factoriza como producto de primos. (Inducción **fuerte**: si n es primo, listo; si no, n = a·b con a, b < n, y la hipótesis fuerte cubre a ambos.)
2. **Unicidad:** esa factorización es única salvo el orden.

**¿La unicidad es obvia? No — y el «mundo de los pares» lo demuestra.** Considera E = {…, −4, −2, 0, 2, 4, …}, los pares con su multiplicación usual. Ahí los «primos» son los pares que no son producto de dos pares (2, 6, 10, 14, 18, 30…). Y resulta que **60 = 2·30 = 6·10** — dos factorizaciones en «primos» de E genuinamente distintas. En E la unicidad falla, y con ella colapsa todo: no hay mcd bien definido por factorización, «p divide a ab ⇒ p divide a a o a b» es falso… El contenido real del TFA es que **en ℤ eso no pasa**: la estructura de divisibilidad de los enteros descansa entera sobre la unicidad.

## La PPF: la radiografía del número

La **factorización en potencias de primos** n = p₁^e₁ · p₂^e₂ ⋯ es la radiografía de n: casi toda pregunta de divisibilidad **se lee en los exponentes**.

- **d | n** ⟺ cada exponente de d es ≤ al de n.
- **Número de divisores:** cada divisor elige un exponente entre 0 y eᵢ para cada primo → **(e₁+1)(e₂+1)⋯**. *Ejemplo del banco:* 360 = 2³·3²·5 → (3+1)(2+1)(1+1) = **24 divisores**. (¡Es un conteo por producto de decisiones — §6.1 dentro de la teoría de números!)
- **mcd:** exponente mínimo primo a primo. **mcm:** exponente máximo.
- **Cuadrado perfecto** ⟺ todos los exponentes pares (cubo ⟺ múltiplos de 3, etc.).
- De min + max = suma (por exponente): **mcd(a,b)·mcm(a,b) = a·b.**

**Señal:** «demuestra que existe/no existe un entero con tal divisibilidad» → escribe todo en PPF y compara exponentes primo por primo.

## El algoritmo de Euclides: mcd sin factorizar

Factorizar números grandes es caro; el mcd no lo necesita:

> **mcd(a, b) = mcd(b, a mod b)**, repetido hasta residuo 0.

*Por qué:* todo divisor común de a y b divide también a a − qb = (a mod b), y al revés — el conjunto de divisores comunes no cambia, solo los números se achican. Ejemplo: mcd(8 cifras, 8 cifras) sale en unos cuantos pasos de división.

**Versión con variable:** mcd(n, n+12) = mcd(n, 12) — porque (n+12) mod n = 12. El mcd de dos expresiones cercanas se reduce a la **diferencia**: mcd(a, b) divide a b − a. Es el reflejo correcto ante «¿qué valores puede tomar mcd(n, n+k)?»: divisores de k.

**Respuesta al disparador del banco:** ¿mcd de dos números de ocho cifras? **No factorices: Euclides.** ¿mcd(n, n+12)? La diferencia: divide a 12.

## Disparadores

- «¿Hay infinitos…?» con primos → reproduce a Euclides; la movida crux: producto de todos + 1.
- Divisores, cuadrados perfectos, mcd/mcm → PPF y mira exponentes.
- mcd de números grandes o de expresiones con variable → algoritmo de Euclides / diferencia.
- «¿Cuántos divisores?» → producto de (exponente + 1).

## Síntesis

> **Chunk mínimo:** Euclides: si los primos fueran p₁…p_N, Q = p₁⋯p_N + 1 deja residuo 1 con todos ⇒ sus factores primos son NUEVOS (Q no tiene que ser primo: 30031 = 59×509) ⇒ infinitos primos. TFA: existencia (inducción fuerte) + UNICIDAD — la parte profunda: en el «mundo de los pares» 60 = 2·30 = 6·10 y todo colapsa; ℤ no es así. PPF = radiografía: d|n ⟺ exponentes ≤; número de divisores = Π(eᵢ+1) (360 → 24); mcd = mínimos, mcm = máximos, mcd·mcm = a·b; cuadrado ⟺ exponentes pares. mcd sin factorizar: Euclides mcd(a,b) = mcd(b, a mod b); con variable, mcd(n, n+k) divide a k.

---

*Antes del quiz: reproduce de memoria la prueba de Euclides señalando la movida crux y el malentendido de «Q es primo», explica la unicidad con el mundo de los pares, y calcula divisores de 360 desde la PPF.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Primos y divisibilidad son restricciones estructurales: factorizan el universo antes de calcular. [[engel-nt]] ofrece mas cantera de teoria de numeros, [[zeitz-72]] transforma divisibilidad en congruencias manejables, y [[arena-q13]] reutiliza esa mentalidad cuando una prueba necesita filtrar casos imposibles.
<!-- GRAFO_CONEXO_OLEADA3_END -->
