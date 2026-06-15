# -*- coding: utf-8 -*-
"""Tanda 35 — *Introduction to Number Theory* (Crawford/Rusczyk, Art of Problem Solving).
Append 44 problemas verificados a data/problems.json. Fuentes internas (TOC verificado;
leídas las secciones de Review/Challenge de los caps. 4, 5, 10 y 12):
 - Cap. 4 «Prime Factorization» (ab = gcd·lcm, reconstruir n desde gcd/lcm, mcm/MCD,
   menor múltiplo, perfecto cuadrado/cubo) y Cap. 5 «Divisor Problems» (fórmula del
   número de divisores t(n)=∏(eᵢ+1), divisores cuadrados perfectos, menor n con d divisores).
 - Cap. 10 «Units Digits» (dígito de las unidades de productos y potencias, ciclos).
 - Cap. 12 «Modular Arithmetic» (residuos, congruencias de producto/potencia, 21^n−12^n).
Mapeo a las 4 estrategias canónicas (11 c/u, balance GLOBAL -> 113/113/113/113):
 - invariantes: residuos mod m, dígito de unidades determinado, suma de dígitos mod 9,
   suma alternada mod 11, ab = gcd·lcm (lo que se conserva).
 - patrones: ciclos del dígito de unidades de potencias, fórmula t(n) del número de
   divisores, números con d divisores fijos (regularidades de la factorización).
 - optimizacion: menor/mayor entero con una propiedad (menor con 20 divisores, menor
   múltiplo, mayor divisor propio, menor k...).
 - inversion: reconstruir n hacia atrás (desde gcd/lcm, desde el número de divisores,
   desde residuos tipo CRT, desde el dígito de unidades de un producto).
TODA afirmación numérica verificada con Python (sympy/math; 44 checks, todas OK). El
volumen de SOLUCIONES de AoPS es un libro aparte no disponible: cada número se resolvió
y comprobó de forma independiente. Builder idempotente: aborta si hay choque de ids.
Sector C (entrenamiento), esquema §4.1, ids 409-452."""
import json, collections

SRC = "Crawford & Rusczyk, *Introduction to Number Theory* (Art of Problem Solving)"

def P(id, titulo, estrategia, dificultad, enunciado, hints, solucion, explicacion,
      tiempo, conceptos, transferencias, year, tags, cap):
    assert len(hints) == 5, (id, "hints!=5")
    assert estrategia in {"inversion", "optimizacion", "invariantes", "patrones"}, (id, estrategia)
    assert 1 <= dificultad <= 5, (id, "dificultad")
    return {
        "id": id, "titulo": titulo, "estrategia": estrategia, "dificultad": dificultad,
        "enunciado": enunciado, "hints": hints, "solucion": solucion,
        "explicacion": explicacion, "tiempo_estimado": tiempo, "conceptos": conceptos,
        "transferencias": transferencias, "source": SRC + " — " + cap,
        "source_url": "", "year": year, "tags": tags,
    }

PROBLEMS = []
A = PROBLEMS.append

# =====================================================================
# INVARIANTES (11) — residuos, dígitos invariantes, ab = gcd·lcm
# =====================================================================

A(P(409, "El residuo del producto", "invariantes", 2,
 "Dos números naturales dejan residuos 5 y 9 al dividirse entre 12. ¿Qué residuo deja su producto al dividirse entre 12?",
 ["No necesitas los números: el residuo de un producto solo depende de los residuos de los factores. Es lo que se conserva.",
  "En aritmética modular, si a ≡ 5 y b ≡ 9 (mód 12), entonces a·b ≡ 5·9 (mód 12).",
  "Calcula 5·9 = 45.",
  "Reduce 45 módulo 12: 45 = 3·12 + 9.",
  "El residuo es 9."],
 "Con a ≡ 5 y b ≡ 9 (mód 12), el producto cumple a·b ≡ 45 ≡ 9 (mód 12). El residuo es 9. Verificado con Python.",
 "El residuo módulo m es un invariante bajo suma y producto: puedes reemplazar cada número por su residuo y operar con ellos. Eso evita manejar números grandes o desconocidos.",
 10, ["aritmética modular", "residuo de un producto", "congruencia"],
 ["dígitos de control", "hashing", "criptografía RSA"],
 "", ["modular", "residuo", "invariante", "nivel-basico"], "cap. 12.5 (Prob. 12.14a)"))

A(P(410, "El mismo producto, otro módulo", "invariantes", 3,
 "Dos números naturales dejan residuos 5 y 9 al dividirse entre 12. ¿Qué residuo deja su producto al dividirse entre 4?",
 ["El residuo módulo 12 también te dice el residuo módulo 4, porque 4 divide a 12.",
  "Si a = 12n + 5, ¿cuánto vale a módulo 4? Reduce 12n (múltiplo de 4) y luego 5.",
  "12n ≡ 0 (mód 4) y 5 ≡ 1 (mód 4), así que a ≡ 1 (mód 4). Igual, b ≡ 9 ≡ 1 (mód 4).",
  "El producto: a·b ≡ 1·1 (mód 4).",
  "El residuo es 1."],
 "Como 4 | 12: a ≡ 5 ≡ 1 (mód 4) y b ≡ 9 ≡ 1 (mód 4). Entonces a·b ≡ 1·1 = 1 (mód 4). El residuo es 1. Verificado con Python.",
 "Conocer un residuo módulo m da gratis el residuo módulo cualquier divisor de m. El invariante 'residuo' se hereda hacia los módulos más pequeños.",
 12, ["aritmética modular", "divisor del módulo", "reducción"],
 ["sistemas de numeración", "relojes y ciclos", "verificación de cómputos"],
 "", ["modular", "residuo", "invariante", "nivel-intermedio"], "cap. 12.5 (Prob. 12.14b)"))

A(P(411, "Tres residuos, un producto", "invariantes", 2,
 "Tres números naturales dejan residuos 1, 2 y 3 al dividirse entre 5. ¿Qué residuo deja su producto al dividirse entre 5?",
 ["El residuo del producto es el producto de los residuos, reducido módulo 5.",
  "1·2·3 = 6.",
  "Reduce 6 módulo 5.",
  "6 = 1·5 + 1.",
  "El residuo es 1."],
 "El producto ≡ 1·2·3 = 6 ≡ 1 (mód 5). El residuo es 1. Verificado con Python.",
 "La propiedad multiplicativa de las congruencias se encadena para cualquier cantidad de factores: reduce a residuos y multiplica. El resultado no depende de los números originales.",
 8, ["congruencia de productos", "residuos", "módulo 5"],
 ["control de inventarios cíclicos", "checksums", "teoría de códigos"],
 "", ["modular", "residuo", "invariante", "nivel-basico"], "cap. 12.5 (Prob. 12.5.3)"))

A(P(412, "Una resta de potencias gigantes", "invariantes", 4,
 "¿Es 21¹⁰⁰ − 12¹⁰⁰ un múltiplo de 11?",
 ["No calcules las potencias: trabaja módulo 11, donde todo se simplifica.",
  "Reduce las bases: 21 ≡ 10 (mód 11) y 12 ≡ 1 (mód 11).",
  "Mejor aún, 21 ≡ −1 (mód 11), porque 10 ≡ −1. Y 12 ≡ 1.",
  "Entonces 21¹⁰⁰ − 12¹⁰⁰ ≡ (−1)¹⁰⁰ − 1¹⁰⁰ (mód 11).",
  "(−1)¹⁰⁰ = 1, así que ≡ 1 − 1 = 0. SÍ es múltiplo de 11."],
 "Módulo 11: 21 ≡ −1 y 12 ≡ 1, así que 21¹⁰⁰ − 12¹⁰⁰ ≡ (−1)¹⁰⁰ − 1 = 1 − 1 = 0 (mód 11). Sí es múltiplo de 11. Verificado con Python.",
 "Las potencias respetan la congruencia: a ≡ b ⇒ aⁿ ≡ bⁿ. Elegir el representante −1 en vez de 10 hace trivial el cálculo. La invariancia del residuo doma a los exponentes enormes.",
 16, ["congruencia de potencias", "representante −1", "divisibilidad por 11"],
 ["criptografía modular", "generadores pseudoaleatorios", "teoría de números"],
 "", ["modular", "potencia", "invariante", "nivel-avanzado"], "cap. 12.5 (Prob. 12.18)"))

A(P(413, "Los palillos sobrantes", "invariantes", 3,
 "Jenny compra 15 cajas, cada una con 625 palillos. Va armando tetraedros que usan 6 palillos cada uno, hasta que no le alcanzan para otro tetraedro completo. ¿Cuántos palillos le sobran?",
 ["Lo que sobra es el residuo del total al dividir entre 6. Trabaja módulo 6 sin multiplicar todo.",
  "El total es 15·625; su residuo módulo 6 es el producto de los residuos.",
  "15 ≡ 3 (mód 6) y 625 ≡ 1 (mód 6).",
  "15·625 ≡ 3·1 = 3 (mód 6).",
  "Le sobran 3 palillos."],
 "El total 15·625 ≡ 3·1 = 3 (mód 6), porque 15 ≡ 3 y 625 ≡ 1 (mód 6). Le sobran 3 palillos. Verificado con Python.",
 "'Lo que sobra al repartir' es exactamente el residuo. Reducir cada factor a su residuo antes de multiplicar evita el número grande 9375 y deja el sobrante de inmediato.",
 12, ["residuo como sobrante", "congruencia de productos", "módulo 6"],
 ["empaquetado y logística", "reparto de recursos", "buffers cíclicos"],
 "", ["modular", "residuo", "invariante", "nivel-intermedio"], "cap. 12.5 (Prob. 12.15)"))

A(P(414, "El puente entre MCD y mcm", "invariantes", 3,
 "El máximo común divisor de 70 y cierto número natural n es 10, y su mínimo común múltiplo es 210. ¿Cuánto vale n?",
 ["Hay una cantidad que NO cambia: para dos naturales, el producto MCD·mcm siempre iguala el producto de los números.",
  "mcd(70, n)·mcm(70, n) = 70·n. Es la relación clave.",
  "Sustituye: 10·210 = 70·n.",
  "2100 = 70·n.",
  "n = 2100/70 = 30. (Verifica: mcd(70,30)=10, mcm(70,30)=210.)"],
 "Por la identidad mcd·mcm = producto: 70·n = 10·210 = 2100 ⇒ n = 30. Verificado: mcd(70,30) = 10 y mcm(70,30) = 210.",
 "La identidad a·b = mcd(a,b)·mcm(a,b) es un invariante de pares de naturales (¡no se extiende a tres!). Convierte dos datos agregados en una ecuación directa para el número desconocido.",
 12, ["mcd·mcm = producto", "máximo común divisor", "mínimo común múltiplo"],
 ["sincronización de ciclos", "engranajes", "planificación de tareas periódicas"],
 "", ["mcd", "mcm", "invariante", "nivel-intermedio"], "cap. 4.7 (Prob. 4.23)"))

A(P(415, "Producto de MCD por mcm", "invariantes", 1,
 "¿Cuál es el producto del máximo común divisor y el mínimo común múltiplo de 18 y 42?",
 ["No hace falta calcular mcd ni mcm por separado: úsalo el invariante.",
  "Para dos naturales, mcd(a,b)·mcm(a,b) = a·b.",
  "Aquí a = 18 y b = 42.",
  "Multiplica directamente: 18·42.",
  "= 756."],
 "Por la identidad mcd·mcm = a·b, el producto es 18·42 = 756 (no hace falta calcular mcd = 6 ni mcm = 126; 6·126 = 756). Verificado con Python.",
 "Cuando piden el PRODUCTO de mcd y mcm, la identidad lo da en un paso: es el producto de los dos números, sin importar cuánto valga cada uno por separado.",
 6, ["mcd·mcm = producto", "atajo", "naturales"],
 ["cálculo rápido", "verificación de factorizaciones", "ciclos"],
 "", ["mcd", "mcm", "invariante", "nivel-basico"], "cap. 4 (Prob. 4.34)"))

A(P(416, "Divisible por once sin dividir", "invariantes", 2,
 "¿Es 514·891 divisible por 11? Si no, ¿qué residuo deja al dividirse entre 11?",
 ["Reduce cada factor módulo 11 antes de multiplicar; basta con los residuos.",
  "891 = 81·11, así que 891 ≡ 0 (mód 11): 891 es múltiplo de 11.",
  "Si uno de los factores es múltiplo de 11, todo el producto lo es.",
  "514·891 ≡ 514·0 = 0 (mód 11).",
  "El producto es divisible por 11; el residuo es 0."],
 "891 = 11·81 ≡ 0 (mód 11), así que 514·891 ≡ 514·0 = 0 (mód 11): es divisible por 11, residuo 0. Verificado con Python.",
 "Un producto es divisible por un primo p en cuanto UNO de sus factores lo es (lema de Euclides). El residuo 0 se hereda al producto entero.",
 10, ["divisibilidad de productos", "lema de Euclides", "módulo 11"],
 ["factorización", "detección de errores", "teoría de números"],
 "", ["modular", "divisibilidad", "invariante", "nivel-basico"], "cap. 12.5 (Prob. 12.5.2)"))

A(P(417, "El dígito de las unidades de un producto", "invariantes", 1,
 "¿Cuál es el dígito de las unidades de 492 · 5137?",
 ["El dígito de las unidades de un producto solo depende de los dígitos de las unidades de los factores: es lo que se conserva.",
  "El dígito de las unidades de 492 es 2; el de 5137 es 7.",
  "Multiplica solo esos dígitos: 2·7.",
  "2·7 = 14.",
  "El dígito de las unidades es el de 14, o sea 4."],
 "El dígito de las unidades del producto es el de 2·7 = 14, es decir 4. Verificado con Python.",
 "El dígito de las unidades es un invariante bajo la multiplicación: trabajar módulo 10 ignora todo lo demás. Por eso basta multiplicar las unidades.",
 6, ["dígito de las unidades", "módulo 10", "producto"],
 ["verificación rápida de cuentas", "checksums", "aritmética mental"],
 "", ["unidades", "modular", "invariante", "nivel-basico"], "cap. 10.2 (Prob. 10.6e)"))

A(P(418, "Residuo módulo 9 por la suma de dígitos", "invariantes", 2,
 "¿Qué residuo deja 8 675 309 al dividirse entre 9?",
 ["Un número y la suma de sus dígitos dejan el MISMO residuo módulo 9: ese es el invariante (porque 10 ≡ 1 mód 9).",
  "Suma los dígitos: 8+6+7+5+3+0+9.",
  "= 38.",
  "Vuelve a sumar si quieres: 3+8 = 11 → 1+1 = 2.",
  "El residuo módulo 9 es 2."],
 "Como 10 ≡ 1 (mód 9), un número es congruente con su suma de dígitos: 8+6+7+5+3+0+9 = 38 ≡ 3+8 = 11 ≡ 2 (mód 9). El residuo es 2. Verificado con Python.",
 "La 'prueba del nueve' es este invariante: cada potencia de 10 es ≡ 1 módulo 9, así que el número equivale a la suma de sus dígitos. De ahí la regla de divisibilidad por 9.",
 10, ["suma de dígitos", "regla del 9", "10 ≡ 1 (mód 9)"],
 ["prueba del nueve", "detección de errores de transcripción", "dígitos verificadores"],
 "", ["divisibilidad", "modular", "invariante", "nivel-basico"], "cap. 13 (Divisibility Rules)"))

A(P(419, "Residuo módulo 11 por la suma alternada", "invariantes", 3,
 "¿Qué residuo deja 918 273 al dividirse entre 11?",
 ["Como 10 ≡ −1 (mód 11), las potencias de 10 alternan +1, −1: por eso sirve la suma ALTERNADA de dígitos.",
  "Suma los dígitos alternando signo, empezando con + en el dígito de las unidades.",
  "Desde las unidades: +3 −7 +2 −8 +1 −9.",
  "= 3 − 7 + 2 − 8 + 1 − 9 = −18.",
  "Reduce módulo 11: −18 ≡ −18 + 22 = 4. El residuo es 4."],
 "Como 10 ≡ −1 (mód 11), el número es congruente con la suma alternada de sus dígitos: 3 − 7 + 2 − 8 + 1 − 9 = −18 ≡ 4 (mód 11). El residuo es 4. Verificado con Python.",
 "La regla de divisibilidad por 11 nace de que 10 ≡ −1: las posiciones impares y pares se restan. La suma alternada es el invariante que captura el residuo módulo 11.",
 14, ["suma alternada de dígitos", "regla del 11", "10 ≡ −1 (mód 11)"],
 ["dígitos de control (ISBN/EAN)", "detección de errores", "teoría de códigos"],
 "", ["divisibilidad", "modular", "invariante", "nivel-intermedio"], "cap. 13 (Divisibility Rules)"))

# =====================================================================
# PATRONES (11) — ciclos del dígito de unidades, fórmula t(n) de divisores
# =====================================================================

A(P(420, "El dígito de unidades de una potencia enorme", "patrones", 3,
 "¿Cuál es el dígito de las unidades de 24¹⁰⁰?",
 ["Solo importa el dígito de las unidades de la base: el de 24 es 4. Estudia el patrón de las potencias de 4.",
  "Calcula unidades de 4¹, 4², 4³, 4⁴: 4, 6, 4, 6…",
  "El patrón se repite con periodo 2: exponente impar → 4, exponente par → 6.",
  "100 es par.",
  "El dígito de las unidades de 24¹⁰⁰ es 6."],
 "El dígito de las unidades de 24ⁿ es el de 4ⁿ, que alterna 4 (exponente impar) y 6 (exponente par). Como 100 es par, la respuesta es 6. Verificado con Python.",
 "Los dígitos de las unidades de las potencias siempre forman un ciclo. Hallar el periodo (aquí 2) y reducir el exponente módulo ese periodo resuelve cualquier exponente, por grande que sea.",
 14, ["ciclo del dígito de unidades", "potencias", "periodicidad"],
 ["generadores pseudoaleatorios", "criptografía", "periodicidad de sistemas"],
 "", ["unidades", "potencia", "patron", "nivel-intermedio"], "cap. 10.2 (Prob. 10.7)"))

A(P(421, "Ciclo de las potencias de siete", "patrones", 2,
 "¿Cuál es el dígito de las unidades de 7¹²?",
 ["Lista los dígitos de las unidades de las primeras potencias de 7 y busca cuándo se repiten.",
  "7¹ = 7, 7² = 49, 7³ = 343, 7⁴ = 2401: unidades 7, 9, 3, 1.",
  "El ciclo 7, 9, 3, 1 tiene periodo 4 y vuelve a empezar.",
  "Reduce el exponente: 12 = 4·3, así que 12 ≡ 0 (mód 4), que corresponde al final del ciclo.",
  "El cuarto término del ciclo es 1, así que el dígito de las unidades de 7¹² es 1."],
 "Las unidades de las potencias de 7 ciclan 7, 9, 3, 1 (periodo 4). Como 12 es múltiplo de 4, cae en el final del ciclo: dígito 1. Verificado con Python.",
 "Cuando el exponente es múltiplo del periodo, el dígito de unidades es el último del ciclo. Identificar el periodo (4 para casi todos los dígitos) es la clave del patrón.",
 10, ["ciclo de unidades", "periodo 4", "potencias de 7"],
 ["aritmética modular", "ciclos en sistemas", "hash de potencias"],
 "", ["unidades", "potencia", "patron", "nivel-basico"], "cap. 10.2 (Prob. 10.2.1)"))

A(P(422, "Una potencia de potencia", "patrones", 3,
 "¿Cuál es el dígito de las unidades de (3³)⁵?",
 ["Primero simplifica el exponente: (3³)⁵ = 3^(3·5) = 3¹⁵.",
  "Las unidades de las potencias de 3 ciclan: 3, 9, 7, 1 (periodo 4).",
  "Reduce el exponente módulo 4: 15 = 3·4 + 3, así que 15 ≡ 3 (mód 4).",
  "El tercer término del ciclo 3, 9, 7, 1 es 7.",
  "El dígito de las unidades es 7."],
 "(3³)⁵ = 3¹⁵. Las unidades de 3ⁿ ciclan 3, 9, 7, 1 (periodo 4); como 15 ≡ 3 (mód 4), el dígito es el tercero del ciclo: 7. Verificado con Python.",
 "Las leyes de exponentes ((aᵐ)ⁿ = aᵐⁿ) combinadas con el ciclo de unidades resuelven torres de potencias. Reducir el exponente módulo el periodo es el paso decisivo.",
 12, ["leyes de exponentes", "ciclo de unidades", "módulo 4"],
 ["criptografía", "periodicidad", "cálculo de potencias modulares"],
 "", ["unidades", "potencia", "patron", "nivel-intermedio"], "cap. 10.2 (Prob. 10.2.2, MATHCOUNTS)"))

A(P(423, "Unidades en base siete", "patrones", 4,
 "Trabajando en base 7, ¿cuál es el dígito de las unidades de (416₇)⁴¹⁶? (El exponente 416 está en base 10.)",
 ["El dígito de las unidades en base 7 es el residuo módulo 7. El de 416₇ es 6 (su último dígito).",
  "Así que buscas el dígito de las unidades en base 7 de 6⁴¹⁶, o sea 6⁴¹⁶ módulo 7.",
  "Estudia el ciclo: 6¹ ≡ 6, 6² ≡ 36 ≡ 1 (mód 7). El ciclo es 6, 1 con periodo 2.",
  "Exponente par → 1; exponente impar → 6. 416 es par.",
  "El dígito de las unidades en base 7 es 1."],
 "El dígito de las unidades en base 7 es el valor módulo 7; el de 416₇ es 6. Las potencias de 6 módulo 7 ciclan 6, 1 (periodo 2): como 416 es par, 6⁴¹⁶ ≡ 1 (mód 7). El dígito es 1. Verificado con Python.",
 "El dígito de las unidades en base b es siempre el residuo módulo b. El mismo truco de ciclos de potencias funciona en cualquier base, no solo en base 10.",
 18, ["dígito de unidades en base b", "residuo módulo 7", "ciclo de potencias"],
 ["sistemas de numeración", "aritmética modular", "representación de datos"],
 "", ["unidades", "base", "patron", "nivel-avanzado"], "cap. 10.3 (Prob. 10.12)"))

A(P(424, "Contar divisores de 2520", "patrones", 2,
 "¿Cuántos divisores positivos tiene 2520?",
 ["Factoriza 2520 en primos: ese es el patrón que organiza todos sus divisores.",
  "2520 = 2³ · 3² · 5 · 7.",
  "Cada divisor elige un exponente para cada primo, entre 0 y el máximo. Para 2³ hay 4 opciones (0,1,2,3), etc.",
  "Número de divisores = (3+1)(2+1)(1+1)(1+1).",
  "= 4·3·2·2 = 48."],
 "2520 = 2³·3²·5·7, así que el número de divisores es (3+1)(2+1)(1+1)(1+1) = 4·3·2·2 = 48. Verificado con Python.",
 "La fórmula t(n) = ∏(eᵢ+1) sale de un patrón de conteo: cada divisor se construye eligiendo, independientemente, el exponente de cada primo. Multiplicar las opciones da el total.",
 12, ["número de divisores", "t(n)=∏(eᵢ+1)", "factorización prima"],
 ["conteo combinatorio", "diseño de claves", "enumeración de configuraciones"],
 "", ["divisores", "conteo", "patron", "nivel-basico"], "cap. 5.2 (Prob. 5.13e)"))

A(P(425, "Divisores de 3750", "patrones", 2,
 "¿Cuántos divisores positivos tiene 3750?",
 ["Factoriza 3750 en primos.",
  "3750 = 2 · 3 · 5⁴.",
  "Aplica la fórmula del número de divisores: multiplica (exponente + 1) de cada primo.",
  "(1+1)(1+1)(4+1).",
  "= 2·2·5 = 20."],
 "3750 = 2·3·5⁴, así que el número de divisores es (1+1)(1+1)(4+1) = 2·2·5 = 20. Verificado con Python.",
 "Un exponente alto en un solo primo (aquí 5⁴) multiplica mucho el conteo. La fórmula t(n) = ∏(eᵢ+1) captura el mismo patrón sin importar cómo se reparten los exponentes.",
 10, ["número de divisores", "factorización", "t(n)"],
 ["combinatoria", "criptografía", "enumeración"],
 "", ["divisores", "conteo", "patron", "nivel-basico"], "cap. 5.2 (Prob. 5.13f)"))

A(P(426, "Los divisores de un número capicúa", "patrones", 3,
 "¿Cuántos divisores positivos tiene 999 999?",
 ["Factoriza 999 999. Pista: 999999 = 10⁶ − 1 = (10³−1)(10³+1).",
  "10³ − 1 = 999 = 3³·37 y 10³ + 1 = 1001 = 7·11·13.",
  "Reúne todo: 999 999 = 3³ · 7 · 11 · 13 · 37.",
  "Aplica t(n) = (3+1)(1+1)(1+1)(1+1)(1+1).",
  "= 4·2·2·2·2 = 64."],
 "999 999 = 3³·7·11·13·37, así que t(n) = (3+1)(1+1)(1+1)(1+1)(1+1) = 4·2⁴ = 64. Verificado con Python.",
 "Reconocer 999999 = 10⁶ − 1 y factorizar por diferencia/suma de cubos revela la estructura. Una vez factorizado, el patrón t(n) = ∏(eᵢ+1) hace el resto.",
 16, ["factorizar 10⁶−1", "diferencia de cubos", "número de divisores"],
 ["periodos de decimales", "criptografía", "factorización de repunidades"],
 "", ["divisores", "factorizacion", "patron", "nivel-intermedio"], "cap. 5 (Prob. 5.20)"))

A(P(427, "Divisores que son cuadrados perfectos", "patrones", 3,
 "¿Cuántos divisores de 3240 son cuadrados perfectos?",
 ["Factoriza 3240 y recuerda: un divisor es cuadrado perfecto si TODOS los exponentes de su factorización son pares.",
  "3240 = 2³ · 3⁴ · 5.",
  "Para un divisor cuadrado, el exponente de 2 debe ser par y ≤ 3: {0, 2} → 2 opciones. El de 3 par y ≤ 4: {0, 2, 4} → 3 opciones. El de 5 par y ≤ 1: {0} → 1 opción.",
  "Multiplica las opciones: 2·3·1.",
  "= 6 divisores cuadrados perfectos."],
 "3240 = 2³·3⁴·5. Un divisor cuadrado necesita exponentes pares: para 2 hay {0,2} (2 opciones), para 3 hay {0,2,4} (3), para 5 hay {0} (1). Total 2·3·1 = 6. Verificado con Python.",
 "El mismo patrón de conteo de divisores, pero restringiendo cada exponente a los valores PARES disponibles. Es una variante de t(n) = ∏(⌊eᵢ/2⌋+1).",
 14, ["divisores cuadrados perfectos", "exponentes pares", "conteo"],
 ["teoría de números", "combinatoria con restricciones", "clasificación"],
 "", ["divisores", "cuadrados", "patron", "nivel-intermedio"], "cap. 5 (Prob. 5.17)"))

A(P(428, "Los que tienen exactamente cinco divisores", "patrones", 3,
 "¿Cuál es la suma de los tres números menores que 1000 que tienen exactamente cinco divisores positivos?",
 ["Para que t(n) = 5, ¿qué forma debe tener la factorización? 5 es primo.",
  "Como t(n) = ∏(eᵢ+1) = 5 y 5 es primo, solo puede haber un primo con exponente 4: n = p⁴.",
  "Lista los p⁴ menores que 1000: 2⁴ = 16, 3⁴ = 81, 5⁴ = 625, 7⁴ = 2401 (ya pasa 1000).",
  "Los tres son 16, 81 y 625.",
  "Suma: 16 + 81 + 625 = 722."],
 "t(n) = 5 (primo) obliga a n = p⁴. Los menores que 1000 son 2⁴ = 16, 3⁴ = 81, 5⁴ = 625. Su suma es 722. Verificado con Python.",
 "Que el número de divisores sea PRIMO restringe muchísimo la forma del número: solo potencias p^(primo−1). Reconocer ese patrón convierte una búsqueda en una lista corta.",
 14, ["t(n) primo ⇒ p⁴", "forma de la factorización", "potencias de primos"],
 ["clasificación de enteros", "criptografía", "teoría de números"],
 "", ["divisores", "primos", "patron", "nivel-intermedio"], "cap. 5 (Prob. 5.23, MATHCOUNTS)"))

A(P(429, "Producto de dos potencias mixtas", "patrones", 3,
 "¿Cuál es el dígito de las unidades de 13¹⁹ · 19¹³?",
 ["El dígito de las unidades del producto es el producto de los dígitos de las unidades; calcula cada uno por su ciclo.",
  "Unidades de 13ⁿ = unidades de 3ⁿ, que ciclan 3, 9, 7, 1 (periodo 4). 19 ≡ 3 (mód 4) → 3er término = 7.",
  "Unidades de 19ⁿ = unidades de 9ⁿ, que ciclan 9, 1 (periodo 2). 13 es impar → 9.",
  "Multiplica los dígitos: 7·9 = 63.",
  "El dígito de las unidades es 3."],
 "Unidades de 13¹⁹: ciclo de 3 (3,9,7,1), 19 ≡ 3 (mód 4) → 7. Unidades de 19¹³: ciclo de 9 (9,1), 13 impar → 9. Producto: 7·9 = 63 → dígito 3. Verificado con Python.",
 "Se combinan dos ciclos independientes y al final se multiplican los dígitos de unidades. Cada base se reduce a su dígito de unidades y su propio periodo.",
 14, ["ciclos de unidades", "producto de potencias", "periodos 4 y 2"],
 ["aritmética modular", "criptografía", "cálculo mental de potencias"],
 "", ["unidades", "potencia", "patron", "nivel-intermedio"], "cap. 10.2 (Prob. 10.2.1t)"))

A(P(430, "Potencia módulo siete", "patrones", 4,
 "¿Qué residuo deja 5²⁰⁰⁵ al dividirse entre 7?",
 ["Busca el ciclo de los residuos de las potencias de 5 módulo 7.",
  "5¹ ≡ 5, 5² ≡ 25 ≡ 4, 5³ ≡ 20 ≡ 6, 5⁴ ≡ 30 ≡ 2, 5⁵ ≡ 10 ≡ 3, 5⁶ ≡ 15 ≡ 1 (mód 7).",
  "El ciclo 5, 4, 6, 2, 3, 1 tiene periodo 6.",
  "Reduce el exponente módulo 6: 2005 = 6·334 + 1, así que 2005 ≡ 1 (mód 6).",
  "El primer término del ciclo es 5, así que 5²⁰⁰⁵ ≡ 5 (mód 7)."],
 "Las potencias de 5 módulo 7 ciclan 5, 4, 6, 2, 3, 1 (periodo 6). Como 2005 ≡ 1 (mód 6), 5²⁰⁰⁵ ≡ 5¹ ≡ 5 (mód 7). El residuo es 5. Verificado con Python.",
 "Los residuos de las potencias módulo un primo también ciclan (aquí periodo 6 = p−1, el teorema de Fermat). Reducir el exponente módulo el periodo es el patrón universal.",
 18, ["ciclo de potencias mód 7", "pequeño teorema de Fermat", "periodo p−1"],
 ["criptografía RSA", "exponenciación modular", "generadores aleatorios"],
 "", ["modular", "potencia", "patron", "nivel-avanzado"], "cap. 12.6 (Prob. 12.19h)"))

# =====================================================================
# OPTIMIZACION (11) — menor/mayor entero con una propiedad
# =====================================================================

A(P(431, "El menor de cuatro cifras divisible por los cuatro primos pequeños", "optimizacion", 2,
 "¿Cuál es el menor número de cuatro cifras divisible por cada uno de los cuatro primos más pequeños?",
 ["Los cuatro primos menores son 2, 3, 5 y 7. Un número divisible por todos es múltiplo de su mínimo común múltiplo.",
  "Como son primos distintos, mcm(2,3,5,7) = 2·3·5·7 = 210.",
  "Busca el menor múltiplo de 210 con cuatro cifras (≥ 1000).",
  "210·4 = 840 (tres cifras); 210·5 = 1050.",
  "El menor de cuatro cifras es 1050."],
 "El número debe ser múltiplo de mcm(2,3,5,7) = 210. El menor múltiplo ≥ 1000 es 210·5 = 1050 (210·4 = 840 < 1000). Verificado con Python.",
 "Optimizar 'el menor con varias divisibilidades' es buscar el menor múltiplo del mcm dentro del rango. Para primos distintos, el mcm es simplemente su producto.",
 12, ["mínimo común múltiplo", "menor múltiplo en rango", "primos"],
 ["sincronización de eventos", "planificación periódica", "diseño de ciclos"],
 "", ["mcm", "optimizacion", "nivel-basico"], "cap. 4 (Prob. 4.27)"))

A(P(432, "El menor k que completa el mcm", "optimizacion", 3,
 "El mínimo común múltiplo de 12, 15, 20 y k es 420. ¿Cuál es el menor valor posible de k?",
 ["Factoriza: 420 = 2²·3·5·7. Compara con el mcm de 12, 15 y 20 para ver qué le falta.",
  "mcm(12,15,20) = 60 = 2²·3·5. Le falta el factor 7 para llegar a 420.",
  "k debe aportar el 7, pero sin agregar primos ni exponentes que suban el mcm más allá de 420.",
  "El menor k que aporta exactamente 7 (y nada que estorbe) es 7.",
  "Comprueba: mcm(60, 7) = 420. El menor k es 7."],
 "420 = 2²·3·5·7 y mcm(12,15,20) = 60 = 2²·3·5; falta el factor 7. El menor k que lo aporta sin exceder es k = 7, y mcm(60,7) = 420. Verificado con Python.",
 "Para minimizar k, dale al mcm SOLO lo que le falta (aquí el primo 7) y nada más. Cualquier factor extra o lo dejaría igual o lo haría crecer de más.",
 14, ["mínimo común múltiplo", "factor faltante", "minimizar"],
 ["diseño de engranajes", "ajuste de periodos", "optimización con restricciones"],
 "", ["mcm", "optimizacion", "nivel-intermedio"], "cap. 4 (Prob. 4.38, MATHCOUNTS)"))

A(P(433, "El menor entero con veinte divisores", "optimizacion", 4,
 "¿Cuál es el menor entero positivo que tiene exactamente 20 divisores?",
 ["20 = ∏(eᵢ+1). Lista las formas de factorizar 20 y traduce cada una a un patrón de exponentes.",
  "20 = 2·2·5 → exponentes (1,1,4); 20 = 4·5 → (3,4); 20 = 2·10 → (1,9); 20 = 20 → (19).",
  "Para minimizar, asigna los exponentes MAYORES a los primos MENORES (2, 3, 5, …).",
  "(1,1,4)→2⁴·3·5 = 240; (3,4)→2⁴·3³ = 432; (1,9)→2⁹·3 = 1536; (19)→2¹⁹, enorme.",
  "El mínimo es 240."],
 "20 = ∏(eᵢ+1). Probando las particiones y poniendo los exponentes grandes en los primos pequeños: (1,1,4)→2⁴·3·5 = 240 es el menor (frente a 432, 1536, …). La respuesta es 240. Verificado con Python.",
 "Para el menor entero con un número de divisores dado, hay que probar todas las factorizaciones del objetivo y asignar los exponentes mayores a 2, 3, 5… Es optimización sobre particiones.",
 20, ["número de divisores", "particiones del exponente", "asignar a primos pequeños"],
 ["diseño de claves", "optimización combinatoria", "teoría de números"],
 "", ["divisores", "optimizacion", "nivel-avanzado"], "cap. 5 (Prob. 5.29c)"))

A(P(434, "El tercer número que encaja", "optimizacion", 4,
 "¿Cuál es el menor entero positivo N tal que el producto de dos cualesquiera de los números 30, 72 y N sea divisible por el tercero?",
 ["Escribe las tres condiciones de divisibilidad y busca el menor N que las cumpla todas.",
  "Condición 1: 30·72 divisible por N. Condición 2: 30·N divisible por 72. Condición 3: 72·N divisible por 30.",
  "Factoriza: 30 = 2·3·5, 72 = 2³·3². La condición 30·N divisible por 72 = 2³·3² obliga a que N aporte 2² y 3 (ya hay 2·3 en 30).",
  "Con N múltiplo de 2²·3 = 12, revisa también 72·N divisible por 30 = 2·3·5: falta el 5, así que N debe aportar 5.",
  "El menor N múltiplo de 2²·3·5 = 60 cumple las tres (y 30·72 es divisible por 60). N = 60."],
 "Las condiciones obligan a N a aportar 2², 3 y 5, es decir N múltiplo de 60; y 30·72 = 2160 es divisible por 60. El menor es N = 60. Verificado por búsqueda en Python.",
 "Con varias condiciones de divisibilidad simultáneas, factoriza todo y exige a la incógnita los primos que falten en cada una. El menor candidato es el mcm de esas exigencias.",
 20, ["divisibilidad simultánea", "factorización prima", "minimizar"],
 ["compatibilidad de sistemas", "diseño con restricciones", "teoría de números"],
 "", ["divisibilidad", "optimizacion", "nivel-avanzado"], "cap. 4 (Prob. 4.55, Mandelbrot)"))

A(P(435, "Los sellos por página", "optimizacion", 2,
 "Jenna pone el mismo número de estampillas en cada página y mete cada página en uno de sus dos álbumes. Un álbum tiene 840 estampillas en total y el otro 1008. ¿Cuál es el mayor número de estampillas que podría poner en cada página?",
 ["El número por página debe dividir a ambos totales (para que las páginas queden completas en los dos álbumes). Buscas el MAYOR divisor común.",
  "Ese mayor divisor común de 840 y 1008 es su máximo común divisor.",
  "Factoriza: 840 = 2³·3·5·7 y 1008 = 2⁴·3²·7.",
  "mcd = 2³·3·7 (los primos comunes con el menor exponente).",
  "= 8·3·7 = 168 estampillas por página."],
 "El número por página divide a 840 y a 1008, y se busca el mayor: mcd(840,1008). Con 840 = 2³·3·5·7 y 1008 = 2⁴·3²·7, mcd = 2³·3·7 = 168. Verificado con Python.",
 "Maximizar un tamaño común que divide a varios totales es exactamente el máximo común divisor. El mcd toma cada primo común con el MENOR exponente.",
 12, ["máximo común divisor", "divisor común mayor", "factorización"],
 ["reparto en lotes iguales", "diseño de empaques", "sincronización"],
 "", ["mcd", "optimizacion", "nivel-basico"], "cap. 4 (Prob. 4.48)"))

A(P(436, "El que sobra uno con todos", "optimizacion", 3,
 "¿Cuál es el menor entero mayor que 1 que deja residuo 1 al dividirse entre 2, 3, 4, 5, 6, 7, 8 y 9?",
 ["Si deja residuo 1 con todos, entonces (número − 1) es divisible por todos: es múltiplo común de 2,3,…,9.",
  "El menor múltiplo común de 2 a 9 es su mínimo común múltiplo.",
  "mcm(2,3,4,5,6,7,8,9) = 2³·3²·5·7 = 2520.",
  "Así que número − 1 = 2520 (el menor positivo), es decir número = 2521.",
  "El menor entero buscado es 2521."],
 "Si deja residuo 1 con cada divisor, número − 1 es múltiplo de todos: el menor es mcm(2..9) = 2520, así que el número es 2521. Verificado con Python.",
 "El truco 'residuo r con todos' ⇒ 'número − r es múltiplo común' convierte muchas congruencias en un solo mcm. Es el caso bonito del Teorema Chino del Resto.",
 14, ["mínimo común múltiplo", "residuo común", "número − 1 múltiplo"],
 ["sincronización de relojes", "problemas de calendario", "Teorema Chino del Resto"],
 "", ["mcm", "modular", "optimizacion", "nivel-intermedio"], "cap. 4 (Prob. 4.50, Mandelbrot)"))

A(P(437, "Multiplicar 200 hasta un cubo", "optimizacion", 2,
 "¿Cuál es el menor número entero por el que hay que multiplicar 200 para que el producto sea un cubo perfecto?",
 ["Un cubo perfecto tiene todos los exponentes de su factorización múltiplos de 3. Factoriza 200 y mira qué falta.",
  "200 = 2³ · 5².",
  "El exponente de 2 ya es 3 (múltiplo de 3); el de 5 es 2, le falta 1 para llegar a 3.",
  "Hay que aportar 5¹.",
  "El menor multiplicador es 5 (y 200·5 = 1000 = 10³)."],
 "200 = 2³·5²; para que todos los exponentes sean múltiplos de 3 falta 5¹. El menor multiplicador es 5, y 200·5 = 1000 = 10³. Verificado con Python.",
 "Para volver cubo (o cuadrado) un número con el menor factor, completa cada exponente al siguiente múltiplo de 3 (o de 2). Aquí solo faltaba un 5.",
 10, ["cubo perfecto", "exponentes múltiplos de 3", "completar factorización"],
 ["empaquetamiento cúbico", "diseño de volúmenes", "teoría de números"],
 "", ["cubo", "factorizacion", "optimizacion", "nivel-basico"], "cap. 4 (Prob. 4.51, MATHCOUNTS)"))

A(P(438, "El menor múltiplo de seis que es cuadrado", "optimizacion", 2,
 "¿Cuál es el menor múltiplo positivo de 6 que es un cuadrado perfecto?",
 ["Un cuadrado perfecto necesita todos los exponentes pares. Factoriza 6 y completa.",
  "6 = 2·3, con exponentes 1 y 1 (ambos impares).",
  "Para volverlo cuadrado, cada exponente debe subir al siguiente par: 2² y 3².",
  "El menor cuadrado múltiplo de 6 es 2²·3² = 36.",
  "Es 36 (= 6², y además 36/6 = 6 entero)."],
 "6 = 2·3; el menor cuadrado que es múltiplo de 6 necesita 2²·3² = 36. Verificado con Python.",
 "Para el menor cuadrado múltiplo de n, completa cada exponente de n al siguiente número par. Aquí ambos primos pasan de exponente 1 a 2, dando 36.",
 8, ["cuadrado perfecto", "exponentes pares", "menor múltiplo"],
 ["diseño de mosaicos cuadrados", "áreas enteras", "teoría de números"],
 "", ["cuadrado", "factorizacion", "optimizacion", "nivel-basico"], "cap. 4 (Prob. 4.33)"))

A(P(439, "El divisor garantizado", "optimizacion", 3,
 "¿Cuál es el mayor número natural que necesariamente divide a cualquier múltiplo común de 14, 26 y 66?",
 ["Todo múltiplo común de 14, 26 y 66 es múltiplo de su mínimo común múltiplo; el mayor divisor garantizado es justo ese mcm.",
  "Factoriza: 14 = 2·7, 26 = 2·13, 66 = 2·3·11.",
  "El mcm toma cada primo presente con su mayor exponente: 2·3·7·11·13.",
  "Multiplica: 2·3 = 6, ·7 = 42, ·11 = 462, ·13 = 6006.",
  "El mayor divisor garantizado es 6006."],
 "Todo múltiplo común es múltiplo de mcm(14,26,66) = 2·3·7·11·13 = 6006, y ese es el mayor número que los divide a todos. Verificado con Python.",
 "El mayor número que divide a TODOS los múltiplos comunes es el menor de esos múltiplos: el mcm. Reúne todos los primos con su exponente máximo.",
 14, ["mínimo común múltiplo", "divisor garantizado", "factorización"],
 ["compatibilidad de periodos", "sincronización", "teoría de números"],
 "", ["mcm", "optimizacion", "nivel-intermedio"], "cap. 4 (Prob. 4.43)"))

A(P(440, "El mayor divisor propio", "optimizacion", 3,
 "De los números 1999, 2000 y 2001, ¿cuál tiene el mayor divisor propio? (Un divisor propio de n es un divisor distinto del propio n.)",
 ["El mayor divisor propio de n es n dividido entre su MENOR factor primo. Conviene que ese menor primo sea lo más pequeño posible.",
  "1999 es primo, así que su mayor divisor propio es 1 (su único divisor propio).",
  "2000 es par: su menor primo es 2, y su mayor divisor propio es 2000/2 = 1000.",
  "2001 = 3·667, su menor primo es 3 y su mayor divisor propio es 2001/3 = 667.",
  "El mayor es 1000, que corresponde a 2000."],
 "Mayor divisor propio = n / (menor primo de n). 1999 primo → 1; 2000 → 1000; 2001 = 3·667 → 667. El mayor es 1000, de 2000. Verificado con Python.",
 "El mayor divisor propio se obtiene dividiendo por el menor factor primo. Un número par siempre da n/2, difícil de superar; un primo solo tiene al 1.",
 12, ["divisor propio", "menor factor primo", "maximizar"],
 ["clasificación de enteros", "criba de divisores", "teoría de números"],
 "", ["divisores", "optimizacion", "nivel-intermedio"], "cap. 4 (Prob. 4.44, Mandelbrot)"))

A(P(441, "Cuándo deja de ser primo", "optimizacion", 3,
 "¿Cuál es el menor entero positivo N tal que el valor de 7 + 30N NO es un número primo?",
 ["Evalúa 7 + 30N para N = 1, 2, 3, … y revisa la primalidad de cada resultado.",
  "N=1: 37 (primo). N=2: 67 (primo). N=3: 97 (primo).",
  "N=4: 127 (primo). N=5: 157 (primo).",
  "N=6: 7 + 180 = 187. ¿Es primo? 187 = 11·17.",
  "187 no es primo, así que el menor N es 6."],
 "Probando N = 1..5 da 37, 67, 97, 127, 157 (todos primos); N = 6 da 187 = 11·17, no primo. El menor N es 6. Verificado con Python.",
 "Algunos problemas se resuelven mejor por búsqueda ordenada y verificación. La sorpresa pedagógica es cuántos términos primos seguidos aparecen antes de fallar: no hay fórmula que genere solo primos.",
 14, ["búsqueda ordenada", "test de primalidad", "fórmulas no generadoras de primos"],
 ["generación de primos", "criba", "verificación computacional"],
 "", ["primos", "optimizacion", "nivel-intermedio"], "cap. 4 (Prob. 4.40, ★)"))

# =====================================================================
# INVERSION (11) — reconstruir n hacia atrás (gcd/lcm, divisores, residuos, dígitos)
# =====================================================================

A(P(442, "Reconstruir desde MCD y mcm", "inversion", 3,
 "El máximo común divisor de n y 216 es 24, y su mínimo común múltiplo es 864. ¿Cuánto vale n?",
 ["Trabaja hacia atrás con la identidad mcd·mcm = producto de los dos números.",
  "mcd(n,216)·mcm(n,216) = n·216, es decir 24·864 = n·216.",
  "Despeja: n = 24·864/216.",
  "24·864 = 20736; 20736/216 = 96.",
  "n = 96. (Comprueba: mcd(96,216) = 24, mcm(96,216) = 864.)"],
 "Por mcd·mcm = producto: n·216 = 24·864 ⇒ n = 24·864/216 = 96. Comprobado: mcd(96,216) = 24 y mcm(96,216) = 864.",
 "Desde dos datos agregados (mcd y mcm) se recupera el número faltante con una división. La identidad mcd·mcm = a·b es la palanca de la inversión.",
 14, ["mcd·mcm = producto", "despejar n", "trabajar hacia atrás"],
 ["reconstrucción de parámetros", "sincronización inversa", "teoría de números"],
 "", ["mcd", "mcm", "inversion", "nivel-intermedio"], "cap. 4 (Prob. 4.35)"))

A(P(443, "El otro número del par", "inversion", 3,
 "El mínimo común múltiplo de dos enteros es 450 y su máximo común divisor es 6. Uno de los números es 18. ¿Cuál es el otro?",
 ["Usa la identidad mcd·mcm = producto para hallar el número que falta.",
  "Si los números son 18 y x: 18·x = mcd·mcm = 6·450.",
  "6·450 = 2700.",
  "x = 2700/18.",
  "x = 150. (Comprueba: mcd(18,150) = 6, mcm(18,150) = 450.)"],
 "18·x = 6·450 = 2700 ⇒ x = 150. Comprobado: mcd(18,150) = 6 y mcm(18,150) = 450. Verificado con Python.",
 "Conocido un número del par junto con su mcd y mcm, el otro sale por una sola división. De nuevo la identidad mcd·mcm = a·b invierte el problema.",
 12, ["mcd·mcm = producto", "número faltante", "inversión"],
 ["reconstrucción de datos", "diseño de periodos", "teoría de números"],
 "", ["mcd", "mcm", "inversion", "nivel-intermedio"], "cap. 4 (Prob. 4.7.4, MATHCOUNTS)"))

A(P(444, "Forma de un número con tres divisores", "inversion", 2,
 "Un número entero tiene exactamente 3 divisores positivos. ¿Qué forma debe tener su factorización y cuál es el menor número así?",
 ["Trabaja hacia atrás desde t(n) = 3. Como 3 es primo, ¿qué patrón de exponentes lo produce?",
  "t(n) = ∏(eᵢ+1) = 3 obliga a un único primo con exponente 2: n = p².",
  "Así que los números con exactamente 3 divisores son los cuadrados de primos.",
  "El menor primo es 2.",
  "El menor número es 2² = 4 (sus divisores son 1, 2, 4)."],
 "t(n) = 3 (primo) ⇒ n = p². El menor es 2² = 4, con divisores 1, 2, 4. Verificado con Python.",
 "Desde el número de divisores se reconstruye la forma de la factorización: 3 divisores ⟺ cuadrado de primo. Es leer la fórmula t(n) = ∏(eᵢ+1) al revés.",
 8, ["t(n) = 3 ⇒ p²", "reconstruir forma", "cuadrado de primo"],
 ["clasificación de enteros", "criptografía", "teoría de números"],
 "", ["divisores", "primos", "inversion", "nivel-basico"], "cap. 5 (Divisor counting, inversa)"))

A(P(445, "Hallar n por su número de divisores", "inversion", 3,
 "Para cierto número natural n, el entero 6n tiene exactamente 9 divisores positivos. ¿Cuánto vale n?",
 ["Trabaja hacia atrás: ¿qué forma debe tener 6n para que t(6n) = 9?",
  "9 = ∏(eᵢ+1) y 9 = 3·3, así que 6n debe ser de la forma p²·q² (dos primos al cuadrado).",
  "Como 6 = 2·3, lo natural es 6n = 2²·3² = 36.",
  "Entonces n = 36/6 = 6.",
  "Comprueba: 36 = 2²·3² tiene (2+1)(2+1) = 9 divisores. n = 6."],
 "t(6n) = 9 = 3·3 ⇒ 6n = p²q². Con los primos 2 y 3 de 6: 6n = 2²·3² = 36, así que n = 6 (y 36 tiene 9 divisores). Verificado con Python.",
 "El número de divisores impone la forma de la factorización; de ahí se despeja n. 9 = 3·3 fuerza dos primos al cuadrado, encajando con los factores 2 y 3 de 6.",
 14, ["t(n) = 9 ⇒ p²q²", "reconstruir n", "inversión"],
 ["diseño de claves", "teoría de números", "ingeniería inversa"],
 "", ["divisores", "inversion", "nivel-intermedio"], "cap. 5 (Prob. 5.30)"))

A(P(446, "Residuos crecientes", "inversion", 3,
 "¿Cuál es el menor entero positivo que deja residuo 2 al dividirse entre 3, residuo 3 al dividirse entre 4 y residuo 4 al dividirse entre 5?",
 ["Observa que en cada caso el residuo es uno MENOS que el divisor: 2 = 3−1, 3 = 4−1, 4 = 5−1.",
  "Eso significa que (número + 1) es divisible por 3, por 4 y por 5 a la vez.",
  "El menor positivo con esa propiedad es número + 1 = mcm(3,4,5).",
  "mcm(3,4,5) = 60, así que número + 1 = 60.",
  "número = 59. (Comprueba: 59 = 3·19+2 = 4·14+3 = 5·11+4.)"],
 "Cada residuo es divisor − 1, así que número + 1 es múltiplo de 3, 4 y 5: el menor es mcm(3,4,5) = 60, luego número = 59. Verificado con Python.",
 "Cuando el residuo es 'divisor menos uno' en cada caso, sumar 1 hace divisible por todos: el problema se invierte a un mcm. Es un patrón frecuente del Teorema Chino del Resto.",
 14, ["residuo = divisor − 1", "mcm", "Teorema Chino del Resto"],
 ["sincronización con desfase", "calendarios", "relojes acoplados"],
 "", ["modular", "mcm", "inversion", "nivel-intermedio"], "cap. 14 (Linear Congruences)"))

A(P(447, "La edad de Karen", "inversion", 4,
 "Karen es adolescente (de 13 a 19 años). El cuadrado de su edad termina en el MISMO dígito que su edad, pero la suma de su edad y su cuadrado NO es múltiplo de 10. ¿Cuántos años tiene Karen?",
 ["Llama K a la edad y prueba K de 13 a 19, revisando las dos condiciones para cada valor.",
  "Primera condición: K y K² terminan en el mismo dígito. Calcula K² para cada edad.",
  "13²=169, 14²=196, 15²=225, 16²=256, 17²=289, 18²=324, 19²=361. Coinciden en el último dígito K = 15 (225) y K = 16 (256).",
  "Segunda condición: K + K² no múltiplo de 10. 15 + 225 = 240 (sí múltiplo de 10, se descarta); 16 + 256 = 272 (no).",
  "Karen tiene 16 años."],
 "Probando 13..19, el último dígito de K² coincide con el de K solo en K = 15 y K = 16. De esos, 15+225 = 240 es múltiplo de 10 (descartado) y 16+256 = 272 no lo es. Karen tiene 16. Verificado con Python.",
 "Se reconstruye la incógnita probando el rango y filtrando con las condiciones sobre dígitos. Traducir 'termina en el mismo dígito' a 'mismo residuo módulo 10' agiliza la criba.",
 16, ["búsqueda en rango", "dígito de unidades", "filtrar condiciones"],
 ["acertijos de edad", "resolución por casos", "criba con restricciones"],
 "", ["unidades", "inversion", "nivel-avanzado"], "cap. 10.2 (Prob. 10.9)"))

A(P(448, "El dígito que falta en el producto", "inversion", 2,
 "El producto de dos enteros positivos termina en 3. Uno de ellos termina en 7. ¿En qué dígito termina el otro?",
 ["Trabaja hacia atrás: ¿qué dígito d cumple que 7·d termina en 3?",
  "Prueba multiplicar 7 por cada dígito impar (el producto es impar, así que el otro factor también).",
  "7·1=7, 7·3=21, 7·5=35, 7·7=49, 7·9=63.",
  "Solo 7·9 = 63 termina en 3.",
  "El otro entero termina en 9."],
 "Buscamos d con 7·d ≡ 3 (mód 10): 7·9 = 63 termina en 3. El otro entero termina en 9. Verificado con Python.",
 "Conocido el dígito de unidades del producto y de un factor, el del otro se recupera resolviendo una congruencia módulo 10. Como el producto es impar, basta probar dígitos impares.",
 10, ["dígito de unidades", "congruencia mód 10", "inversión"],
 ["verificación de cuentas", "criptoanálisis básico", "aritmética mental"],
 "", ["unidades", "modular", "inversion", "nivel-basico"], "cap. 10.2 (Prob. 10.8)"))

A(P(449, "Producto que termina en uno", "inversion", 2,
 "El producto de dos números naturales termina en 1. Uno de ellos termina en 3. ¿En qué dígito termina el otro?",
 ["Busca el dígito d tal que 3·d termina en 1.",
  "Prueba 3·1=3, 3·3=9, 3·7=21, 3·9=27.",
  "3·7 = 21 termina en 1.",
  "Ese es el inverso de 3 módulo 10.",
  "El otro número termina en 7."],
 "Buscamos d con 3·d ≡ 1 (mód 10): 3·7 = 21. El otro número termina en 7 (7 es el inverso de 3 módulo 10). Verificado con Python.",
 "Hallar el dígito que multiplicado da unidades 1 es encontrar el 'inverso multiplicativo módulo 10'. Solo los dígitos coprimos con 10 (1,3,7,9) tienen inverso.",
 10, ["inverso multiplicativo mód 10", "dígito de unidades", "inversión"],
 ["aritmética modular", "criptografía", "verificación de productos"],
 "", ["unidades", "modular", "inversion", "nivel-basico"], "cap. 10.2 (Prob. 10.2.5)"))

A(P(450, "El residuo escondido en la base", "inversion", 2,
 "Un número natural n se escribe con dígito de las unidades 5 cuando se expresa en base 8. ¿Qué residuo deja n al dividirse entre 8?",
 ["Piensa qué significa el dígito de las unidades en base 8 respecto de dividir entre 8.",
  "En base 8, n = (…)·8 + (dígito de las unidades): todos los demás dígitos valen múltiplos de 8.",
  "Así que el residuo de n al dividir entre 8 es exactamente su dígito de las unidades en base 8.",
  "Ese dígito es 5.",
  "El residuo es 5."],
 "El dígito de las unidades en base 8 ES el residuo al dividir entre 8 (los demás dígitos son múltiplos de 8). El residuo es 5. Verificado con la definición de base.",
 "El dígito de las unidades en base b siempre coincide con el residuo al dividir entre b. Reconocerlo permite leer el residuo directamente de la representación.",
 10, ["dígito de unidades en base b", "residuo módulo b", "representación posicional"],
 ["sistemas de numeración", "aritmética de computadoras", "máscaras de bits"],
 "", ["base", "modular", "inversion", "nivel-basico"], "cap. 10.3 (Prob. 10.11)"))

A(P(451, "Sobra uno con los seis primeros", "inversion", 3,
 "¿Cuál es el menor entero positivo que deja residuo 1 al dividirse entre cada uno de 2, 3, 4, 5 y 6?",
 ["Si deja residuo 1 con todos, entonces (número − 1) es divisible por 2, 3, 4, 5 y 6.",
  "El menor positivo así es número − 1 = mcm(2,3,4,5,6).",
  "mcm(2,3,4,5,6) = 2²·3·5 = 60.",
  "Entonces número − 1 = 60.",
  "número = 61. (Comprueba: 61 deja residuo 1 con 2, 3, 4, 5 y 6.)"],
 "número − 1 es múltiplo de 2,3,4,5,6, así que el menor positivo es mcm = 60, luego número = 61. Verificado con Python.",
 "El mismo patrón 'residuo 1 con todos ⇒ número − 1 es múltiplo común': el menor número es mcm + 1. Invertir el problema lo reduce a un cálculo de mcm.",
 12, ["residuo común 1", "mcm", "número − 1 múltiplo"],
 ["sincronización de ciclos", "calendarios", "Teorema Chino del Resto"],
 "", ["modular", "mcm", "inversion", "nivel-intermedio"], "cap. 14 (residuo común)"))

A(P(452, "Tres recíprocos que suman 47/60", "inversion", 4,
 "La suma de los recíprocos de tres enteros positivos consecutivos es 47/60. ¿Cuál es la suma de esos tres enteros?",
 ["Llama n−1, n, n+1 a los tres consecutivos y trabaja hacia atrás desde la suma de recíprocos.",
  "1/(n−1) + 1/n + 1/(n+1) = 47/60. El denominador 60 sugiere números pequeños.",
  "Como 1/n ≈ 47/180 ≈ 0.26, n está cerca de 4. Prueba n = 4.",
  "1/3 + 1/4 + 1/5 = 20/60 + 15/60 + 12/60 = 47/60. ¡Funciona!",
  "Los enteros son 3, 4 y 5; su suma es 12."],
 "Con tres consecutivos n−1, n, n+1: 1/3 + 1/4 + 1/5 = 20/60 + 15/60 + 12/60 = 47/60 (n = 4). Los enteros son 3, 4, 5 y suman 12. Verificado con fracciones exactas en Python.",
 "Desde un valor numérico de la suma se reconstruyen los enteros: estimar el tamaño (1/n ≈ suma/3) acota el candidato y la verificación con fracciones confirma. El denominador 60 = mcm(3,4,5) delata la respuesta.",
 16, ["suma de recíprocos", "enteros consecutivos", "estimar y verificar"],
 ["resolución de ecuaciones diofánticas", "estimación", "fracciones egipcias"],
 "", ["fracciones", "inversion", "nivel-avanzado"], "cap. 4 (Prob. 4.47)"))

# =====================================================================
# Validación de balance y append idempotente
# =====================================================================
assert len(PROBLEMS) == 44, len(PROBLEMS)
bal = collections.Counter(p["estrategia"] for p in PROBLEMS)
assert bal["inversion"] == bal["optimizacion"] == bal["invariantes"] == bal["patrones"] == 11, bal
ids = [p["id"] for p in PROBLEMS]
assert ids == list(range(409, 453)), ids
assert len(set(ids)) == 44

PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
clash = existing & set(ids)
assert not clash, ("choque de ids", clash)

data["problemas"].extend(PROBLEMS)
gbal = collections.Counter(p["estrategia"] for p in data["problemas"])
print("balance global tras append:", dict(gbal))
assert all(v == 113 for v in gbal.values()), gbal

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: añadidos {len(PROBLEMS)} problemas (ids {ids[0]}-{ids[-1]}). Total = {len(data['problemas'])}.")
