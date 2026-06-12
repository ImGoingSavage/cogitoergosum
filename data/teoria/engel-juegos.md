# Engel · Juegos: posiciones perdedoras y pareo

*Lección redactada para CogitoErgoSum a partir del capítulo 13 de «Problem-Solving Strategies» (A. Engel), Games (pp. 361-365): la partición W/L, la estrategia de pareo, Bachet y sus variantes. El resto del capítulo (Nim, Wythoff) es cantera.*

## El marco de Engel

Juegos de dos jugadores que **alternan turnos con las mismas reglas para ambos** (juegos *imparciales*), con información completa, sin azar y sin empates: **pierde quien no puede mover** (o quien toma/no toma la última ficha, según la versión). Para esta familia hay una teoría completa y mecánica.

## W y L: la partición que decide todo

Toda posición es **W** (ganadora: quien mueve desde ahí gana con juego perfecto) o **L** (perdedora: quien mueve desde ahí pierde contra juego perfecto). Las caracteriza una doble propiedad:

- desde toda posición de **W** EXISTE **al menos un** movimiento hacia L;
- desde toda posición de **L**, **TODOS** los movimientos van a W (no hay escapatoria);
- las posiciones **finales** (sin movimiento posible) están en **L**: quien está ahí ya perdió.

**La regla única del juego perfecto: muévete SIEMPRE a una posición de L.** El rival, parado en L, solo puede devolverte a W; tú vuelves a empujarlo a L; como el juego termina, el rival acaba en una L final — sin movimiento. Ganaste sin «calcular jugadas»: solo navegaste el mapa.

## El cálculo es HACIA ATRÁS

El mapa W/L no se adivina: se **etiqueta retrocediendo desde el final** (la heurística «trabaja hacia atrás» en estado puro). Marca L las posiciones finales; marca W todo lo que alcanza una L; marca L lo que solo alcanza W; repite. En juegos de fichas, etiqueta 0, 1, 2, 3, … hasta que el patrón de L se vuelva **periódico** — entonces tienes la estrategia completa.

**Bachet** (el modelo): n fichas; en tu turno tomas entre 1 y k; **gana quien toma la última**. Etiquetando hacia atrás: **L = múltiplos de (k+1)**. La doble verificación: desde un múltiplo de k+1 no alcanzas el siguiente múltiplo (restas a lo sumo k); desde un no-múltiplo, restas el residuo y caes en el múltiplo. Con k = 5 y n = 100: 100 = 6·16 + 4 no es múltiplo de 6 → **gana el primero**: toma 4 (deja 96) y de ahí responde siempre a la toma t del rival con 6 − t, bajando de múltiplo en múltiplo hasta tomar la última.

## Variantes que entrenan el reflejo modular

El conjunto de tomas permitidas M cambia el módulo del patrón, no el método:

- **M = {1, 2, 4, 8, 16, …}** (potencias de 2) → **L = múltiplos de 3**. Certificado: ninguna potencia de 2 es divisible entre 3 (2ᵏ ≡ 1 o 2 mod 3), así que de múltiplo de 3 no se llega a múltiplo de 3; y desde un no-múltiplo, restar 1 o 2 te deja en el múltiplo.
- **M = {1 y los primos}** → **L = múltiplos de 4**. Con 1, 2, 3 cubres todo residuo mod 4, y ningún elemento de M es múltiplo de 4 (el único primo par es 2; 1, 2, 3 no son múltiplos de 4 y un primo > 3 múltiplo de 4 no existe).
- **M = {1, 3, 8}** → L es **periódica mod 11**: L = {n ≡ 0, 2, 4, 6 (mod 11)}. Aquí el patrón ya no es «múltiplos de algo» — por eso la receta es etiquetar y BUSCAR el período, no adivinar la fórmula.

## Estrategia de PAREO: ganar sin calcular

A veces no hace falta el mapa completo: basta **partir las posiciones (o los movimientos) en parejas** tales que de un elemento de la pareja se pasa al otro. Cuando el rival usa uno, tú usas su pareja: **nunca te quedas sin respuesta**, así que el que muere es él.

El caso estrella es el **espejo**: si el tablero tiene una simetría central, ocupa el punto fijo (si hace falta) y **copia cada jugada del rival reflejada**. Las monedas en la mesa redonda (§3.1 de Zeitz, fase 1) eran exactamente esto: centro + respuesta diametral = pareo por reflexión. La condición de legitimidad es la misma de todo WLOG: la simetría debe preservar **las reglas completas** del juego, y tu jugada espejo debe estar siempre disponible (eso es lo que el punto fijo garantiza).

## Si el juego no encaja en ningún molde

Receta general (composición de heurísticas que ya tienes):

1. **Tabula posiciones pequeñas a mano** (caso pequeño): 0, 1, 2, … etiquetadas W/L hacia atrás.
2. **Busca el patrón** de las L (período, residuos).
3. **CONJETURA** la descripción de L.
4. **Demuestra** con la doble verificación: «de L solo se va a W» y «de W se puede ir a L». Sin las dos mitades no hay certificado: encontrar jugadas buenas contra respuestas malas del rival no prueba nada — el mapa W/L es contra **juego perfecto**.

## Disparadores

- «Dos jugadores alternan, pierde quien no pueda mover» → etiqueta W/L hacia atrás desde las finales; busca período.
- Juego de tomar fichas con tomas en M → patrón modular: calcula L para n pequeños y conjetura el módulo.
- Tablero/reglas con simetría (mesa redonda, dos pilas iguales) → pareo/espejo: punto fijo + copiar reflejado.
- Ya «encontraste» L → exige el certificado doble (L→solo W; W→alguna L) antes de creerlo.

## Síntesis

> **Chunk mínimo:** En juegos imparciales sin empate, toda posición es W (existe movimiento a L) o L (todo movimiento da a W; las finales son L), y el juego perfecto es una sola regla: muévete siempre a L. El mapa se calcula hacia atrás hasta hallar período. Bachet (tomas 1..k, gana la última): L = múltiplos de k+1; con potencias de 2, L = múltiplos de 3; con {1, primos}, L = múltiplos de 4; con {1,3,8}, L ≡ {0,2,4,6} mod 11. Pareo: aparea posiciones/movimientos (espejo = pareo por simetría con punto fijo) y responde siempre con la pareja. Certificado obligatorio: ambas mitades de la doble verificación.

---

*Antes del quiz: reconstruye de memoria la definición de W/L con su doble propiedad, la regla única del juego perfecto, el análisis completo de Bachet 100 con tomas 1-5, los conjuntos L de las tres variantes y qué garantiza exactamente una estrategia de pareo.*
