# Arena Quant · Esperanza, juegos y parada óptima

Una familia entera de preguntas de entrevista quant se reduce a una idea: **¿cuál es el valor de un juego bajo la estrategia óptima?** No te piden tu apetito por el riesgo; te piden el valor *racional*. La técnica universal es **trabajar hacia atrás**: resuelve el juego con un paso, luego con dos, y deja que la recursión te lleve al caso completo.

## Parada óptima — el corazón del capítulo

«Tiras un dado hasta 3 veces; en cada tiro puedes quedarte con el número o volver a tirar. ¿Cuál es tu ganancia esperada?»

Empieza por el último tiro: con un solo tiro, E = 3.5. Con dos tiros, te quedas con el primero solo si supera 3.5 (es decir, si sale 4, 5 o 6), si no, continúas:

> E(2) = (6+5+4)/6 + (3/6)·3.5 = **4.25**

Con tres tiros, te quedas con el primero si supera 4.25 (sale 5 o 6):

> E(3) = (6+5)/6 + (4/6)·4.25 = **14/3 ≈ 4.667**

Esto es **exactamente** valorar una opción sobre un árbol multinomial: por eso encanta a los entrevistadores. La regla de parada («quédate si el valor inmediato supera la esperanza de continuar») es el principio de la parada óptima.

## Esperanzas de tiradas de moneda — la caja de herramientas

| Pregunta | Resultado | Truco |
|----------|-----------|-------|
| Tiros hasta la 1.ª cara (moneda sesgada p) | **1/p** | geométrica: E = Σ j·p(1−p)^{j−1} |
| Tiros hasta 2 caras o 2 cruces seguidas | **3** | tras el 1.º tiro faltan k−1 tiros determinados |
| Tiros hasta 3 caras seguidas (justa) | **14** | estrategia de apuesta-martingala |
| Geométrica N (incluye la cara final) | E(N)=2, Var(N)=2 | suma por diferencias |

El **truco de la martingala** para «3 caras seguidas»: apuesta de forma que ganes en cara y, tras una cruz en el tiro n, tu posición sea −n. Como las ganancias son una martingala y el tiempo de tres caras es un tiempo de parada de esperanza finita, el muestreo opcional da E(14 − n) = 0 → **E = 14**. Generaliza: para una moneda justa, el número esperado de tiros para n caras seguidas es 2^{n+1} − 2.

## Juegos «valor justo»

- **Cuatro cajas, una con 100, pagas X por abrir cada una hasta acertar.** Estrategia óptima: sigue jugando hasta ganar. E(coste) = X(1·¼ + 2·¼ + 3·¼ + 4·¼)… con probabilidades condicionales correctas: 100 = 2.5X → **X = 40**.
- **Adivina mi número de 1 a 100; te pago $n si aciertas.** Es teoría de juegos: elige k con probabilidad ∝ 1/k; la ganancia esperada es (Σ 1/j)^{−1} ≈ 0.193, independiente de la jugada del rival.
- **Doblas en cara, partes a la mitad en cruz, ∞ tiros.** E por tiro = ½·2 + ½·½ = 5/4 > 1 → E = (5/4)^n **→ ∞**. La media diverge aunque casi todas las trayectorias tiendan a 0 (¡la media la dominan trayectorias raras enormes!).

## Diana circular

Si aciertas uniformemente el área, la densidad del radio es 2s/R² (no uniforme: hay más área lejos del centro). La distancia esperada al centro es **2R/3**. Útil para detectar el error de suponer densidad uniforme en el radio.

## Disparadores

| Señal | Jugada |
|-------|--------|
| "puedes quedarte o continuar" | parada óptima: resuelve hacia atrás, compara inmediato vs E(continuar) |
| "tiros hasta el primer éxito" | geométrica, E = 1/p |
| "n resultados seguidos" | martingala + muestreo opcional |
| "juego justo, ¿cuánto pagar?" | iguala E(coste) = E(premio) bajo estrategia óptima |
| "área / dardos" | densidad radial 2s/R², no uniforme |

> ❧ **Síntesis:** la parada óptima es valorar una opción americana en miniatura: en cada nodo te quedas con el premio inmediato solo si supera la esperanza de seguir. Resuelve siempre hacia atrás, y cuando aparezcan «n éxitos seguidos», recuerda que una apuesta-martingala convierte el problema en una ecuación de una línea.

---

*Retrieval: cierra la página y responde — (1) E de 3 tiros de dado con parada óptima; (2) tiros esperados para 3 caras seguidas; (3) precio justo del juego de 4 cajas; (4) por qué la media de doblar/partir diverge.*
