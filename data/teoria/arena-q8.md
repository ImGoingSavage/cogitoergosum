# Arena Quant · Esperanza, juegos y parada óptima

## De qué trata (y qué sabrás hacer)

Una familia entera de preguntas quant se reduce a una sola: **¿cuánto vale un juego si lo juegas de forma óptima?** No te preguntan tu apetito por el riesgo, sino el valor *racional*. La técnica universal es **trabajar hacia atrás**: resuelve el juego con un paso que falta, luego con dos, y deja que la recursión te lleve al caso completo.

Al terminar sabrás aplicar la regla de parada óptima ("quédate si el premio en mano supera la esperanza de continuar"), calcular esperanzas de espera con la geométrica y con el truco de la martingala, y reconocer cuándo una media diverge. Todo se construye resolviendo casos pequeños primero.

---

## Parada óptima — el corazón del capítulo

**Tiras un dado hasta 3 veces; en cada tiro te quedas con el número o vuelves a tirar. ¿Ganancia esperada con la mejor estrategia?** Resuelve **hacia atrás**:

- **Último tiro** (sin opción): $E=\tfrac{1+2+\cdots+6}{6}=3.5$.
- **Con dos tiros disponibles:** te quedas con el primero solo si supera el valor de continuar (3.5), o sea si sale 4, 5 o 6; si no, continúas y obtienes 3.5:
$$E(2)=\frac{4+5+6}{6}+\frac{3}{6}\cdot 3.5=4.25.$$
- **Con tres tiros:** te quedas si el primero supera 4.25, o sea 5 o 6; si no, continúas con valor 4.25:
$$E(3)=\frac{5+6}{6}+\frac{4}{6}\cdot 4.25\approx 4.667.$$

Esto es **exactamente** valorar una opción sobre un árbol: por eso encanta a los entrevistadores. La regla —"quédate si el valor inmediato supera la esperanza de continuar"— es el principio de la parada óptima (conecta con la opción americana de [[arena-q5]]).

---

## Esperanzas de tiradas de moneda — la caja de herramientas

| Pregunta | Resultado | Truco |
|----------|-----------|-------|
| Tiros hasta la 1.ª cara (sesgo $p$) | $1/p$ | geométrica: $E=\sum_j j\,p(1-p)^{j-1}$ |
| Tiros hasta 2 iguales seguidas | $3$ | tras el 1.º faltan tiros determinados |
| Tiros hasta $n$ caras seguidas (justa) | $2^{n+1}-2$ | apuesta-martingala |

**El truco de la martingala** para "$n$ caras seguidas": imagina apostadores que entran en cada tiro doblando su apuesta a "cara". Sus ganancias forman una **martingala** (juego justo, esperanza constante), y el momento de ver $n$ caras es un tiempo de parada de esperanza finita. El teorema del **muestreo opcional** iguala el dinero ganado a lo apostado y da, en una línea, $E=2^{n+1}-2$. Para 3 caras seguidas: $2^4-2=14$.

---

## Juegos de "valor justo"

- **Doblas tu apuesta en cara, la partes a la mitad en cruz, infinitos tiros.** La esperanza por tiro es $\tfrac12\cdot2+\tfrac12\cdot\tfrac12=\tfrac54>1$, así que $E(n)=(\tfrac54)^n\to\infty$. La media **diverge** aunque casi toda trayectoria tienda a 0: la dominan trayectorias raras enormes. Aviso permanente: valor esperado $\ne$ resultado típico.

---

## Mini-ejemplo trabajado: el dado con parada, paso a paso

Tres tiros, te quedas o sigues. Resuelve **hacia atrás**:

1. **Último tiro:** sin opción, $E=\tfrac{1+2+3+4+5+6}{6}=3.5$.
2. **Dos tiros:** te quedas con el primero solo si supera el valor de continuar (3.5), o sea si sale 4, 5, 6; si no, continúas y obtienes 3.5. $E(2)=\tfrac{4+5+6}{6}+\tfrac{3}{6}\cdot3.5=2.5+1.75=4.25$.
3. **Tres tiros:** te quedas si el primero supera 4.25, o sea 5, 6; si no, continúas con valor 4.25. $E(3)=\tfrac{5+6}{6}+\tfrac{4}{6}\cdot4.25\approx1.833+2.833=4.667$.

La regla de parada —"quédate si el valor inmediato supera la esperanza de continuar"— es idéntica al ejercicio temprano de una opción americana.

**Predicción antes de seguir:** con 10 tiros disponibles, ¿el umbral de "quédate" sube o baja? Respuesta: **sube** (hacia $\sim5$), porque tener más tiros por delante hace más valioso continuar, así que solo un valor muy alto justifica detenerte. Más opciones futuras ⇒ umbral de ejercicio más exigente.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "puedes quedarte o seguir / cuándo detenerte" → parada óptima por backward induction; compara premio inmediato vs $E(\text{continuar})$.
- **Contraejemplo (densidad radial):** en una diana, suponer que el radio es uniforme da $R/2$; es **falso** porque hay más área lejos del centro (densidad $2s/R^2$), y la distancia esperada es $2R/3$. "Uniforme en el área" $\ne$ "uniforme en el radio".
- **Caso borde (media divergente):** doblar en cara / partir a la mitad en cruz tiene $E$ por tiro $=\tfrac54>1$, así que $E(n)=(\tfrac54)^n\to\infty$, *aunque casi toda trayectoria tiende a 0*. La media la dominan trayectorias raras enormes.

## Errores típicos

- **Conceptual:** resolver hacia adelante en vez de hacia atrás; el valor de continuar solo se conoce desde el final.
- **Técnico:** en "$n$ éxitos seguidos", intentar sumar una serie infinita en vez de usar la apuesta-martingala + muestreo opcional (que da $2^{n+1}-2$ en una línea).
- **De interpretación:** reportar la media cuando la distribución es de cola pesada (San Petersburgo): el precio justo no es $E[\text{payoff}]$ si el bankroll es finito.

## Transferencia isomorfa

"Trabajar hacia atrás bajo la estrategia óptima" es una estructura, no un truco aislado:

- **Parada óptima ↔ opción americana:** quedarte si el premio inmediato supera la continuación *es* el criterio de ejercicio temprano de una americana (conecta con [[arena-q5]]).
- **Backward induction ↔ programación dinámica:** resolver $E(1)\to E(2)\to E(3)$ es exactamente llenar una tabla de DP de atrás hacia adelante (conecta con [[arena-cc3]]).
- **Torre de esperanza ↔ ecuaciones de estado:** plantear $E_0=1+\tfrac12 E_1+\tfrac12 E_0$ para "$k$ caras seguidas" es la ley de esperanza total aplicada a una cadena de estados (conecta con [[arena-q6]]).
- **Media divergente ↔ paradoja de San Petersburgo:** colas tan pesadas que $E=\infty$ aparecen igual en juegos de doblar y en payoffs de cola larga (conecta con [[arena-fc4]]).

Moraleja de la arista: *valorar un juego es valorar una opción: resuelve hacia atrás y quédate solo cuando el premio en mano supere la esperanza de seguir.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "puedes quedarte o continuar" | parada óptima: hacia atrás, inmediato vs $E(\text{continuar})$ |
| "tiros hasta el primer éxito" | geométrica, $E=1/p$ |
| "$n$ resultados seguidos" | martingala + muestreo opcional ($2^{n+1}-2$) |
| "juego justo, ¿cuánto pagar?" | iguala $E(\text{coste})=E(\text{premio})$ bajo estrategia óptima |
| "área / dardos" | densidad radial $2s/R^2$, no uniforme |

---

> ❧ **Síntesis:** la parada óptima es valorar una opción americana en miniatura: en cada nodo te quedas con el premio inmediato solo si supera la esperanza de seguir. Resuelve siempre hacia atrás, y cuando aparezcan "$n$ éxitos seguidos", recuerda que una apuesta-martingala convierte el problema en una ecuación de una línea.

---

*Retrieval: cierra la página y responde — (1) $E$ de 3 tiros de dado con parada óptima; (2) tiros esperados para 3 caras seguidas; (3) por qué la media de doblar/partir diverge.*
