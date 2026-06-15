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

## Mini-ejemplo trabajado: el dado con parada, paso a paso

Tres tiros, te quedas o sigues. Resuelve **hacia atrás**:

1. **Último tiro:** sin opción, E = (1+2+3+4+5+6)/6 = 3.5.
2. **Dos tiros:** te quedas con el primero solo si supera el valor de continuar (3.5), o sea si sale 4,5,6; si no, continúas y obtienes 3.5. E(2) = (4+5+6)/6 + (3/6)·3.5 = 2.5 + 1.75 = **4.25**.
3. **Tres tiros:** te quedas con el primero si supera 4.25, o sea si sale 5,6; si no, continúas con valor 4.25. E(3) = (5+6)/6 + (4/6)·4.25 = 1.833 + 2.833 = **4.667**.

La regla de parada —"quédate si el valor inmediato supera la esperanza de continuar"— es idéntica al ejercicio temprano de una opción americana.

**Predicción antes de seguir:** con 10 tiros disponibles, ¿el umbral de "quédate" sube o baja? Respuesta: **sube** (hacia ~5), porque tener más tiros por delante hace más valioso continuar, así que solo un valor muy alto justifica detenerte. Más opciones futuras ⇒ umbral de ejercicio más exigente.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "puedes quedarte o seguir / cuándo detenerte" → parada óptima por backward induction; compara premio inmediato vs E(continuar).
- **Contraejemplo (densidad radial):** en la diana, suponer que el radio es uniforme da R/2; es **falso** porque hay más área lejos del centro (densidad 2s/R²), y la distancia esperada es 2R/3. "Uniforme en el área" ≠ "uniforme en el radio".
- **Caso borde (media divergente):** doblar en cara / partir a la mitad en cruz tiene E por tiro = 5/4 > 1, así que E(n) = (5/4)ⁿ → ∞, *aunque casi toda trayectoria tiende a 0*. La media la dominan trayectorias raras enormes — un borde que avisa: valor esperado ≠ resultado típico.

## Errores típicos

- **Conceptual:** resolver hacia adelante en vez de hacia atrás; el valor de continuar solo se conoce desde el final.
- **Técnico:** en "n éxitos seguidos", intentar sumar una serie infinita en vez de usar la apuesta-martingala + muestreo opcional (que da 2^(n+1)−2 en una línea).
- **De interpretación:** reportar la media cuando la distribución es de cola pesada (San Petersburgo): el precio justo no es E[payoff] si el bankroll es finito.

## Transferencia isomorfa

"Trabajar hacia atrás bajo la estrategia óptima" es una estructura, no un truco aislado:

- **Parada óptima ↔ opción americana:** quedarte si el premio inmediato supera la continuación *es* el criterio de ejercicio temprano de una americana (conecta con [[arena-q5]], valoración por no-arbitraje).
- **Backward induction ↔ programación dinámica:** resolver E(1)→E(2)→E(3) es exactamente llenar una tabla de DP de atrás hacia adelante (conecta con [[arena-cc3]], coin change/DP).
- **Torre de esperanza ↔ ecuaciones de estado:** plantear E₀ = 1 + ½E₁ + ½E₀ para "k caras seguidas" es la ley de esperanza total aplicada a una cadena de estados (conecta con [[arena-q6]]).
- **Media divergente ↔ paradoja de San Petersburgo:** colas tan pesadas que E=∞ aparecen igual en juegos de doblar y en payoffs de cola larga; el valor esperado deja de ser precio justo.

Moraleja de la arista: *valorar un juego es valorar una opción: resuelve hacia atrás y quédate solo cuando el premio en mano supere la esperanza de seguir.*

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
