# El principio del extremo

*Lección redactada para CogitoErgoSum a partir de la sección 3.2 de Zeitz (The Extreme Principle). Cubre el contenido completo de la unidad.*

## El principio

> **Todo conjunto finito y no vacío de números reales tiene un máximo y un mínimo.** (Y todo conjunto no vacío de enteros positivos tiene mínimo, aunque sea infinito — el principio del buen orden.)

Suena a trivialidad. Su poder está en el uso: **el elemento extremo tiene propiedades especiales gratis**, propiedades que un elemento cualquiera no tiene. La táctica completa en una línea: *ordena algo, agarra la punta y explota lo que la punta no puede hacer.*

## Por qué el extremo «trae propiedades gratis»

Porque el extremo **restringe a sus vecinos y a todo lo demás**:

- El vecino del máximo **no puede superarlo**.
- Nada está más cerca que **el par a distancia mínima**.
- A la izquierda del punto más a la izquierda **no hay nada**.
- El contraejemplo **mínimo** no admite contraejemplos menores.

Cada una de esas imposibilidades es una **palanca**: una desigualdad o un «no existe» que el problema general no te daba. El arte está en elegir *qué* ordenar (¿los números?, ¿las distancias?, ¿los ángulos?, ¿el primer momento en que algo pasa?) para que la palanca apunte a la conclusión.

## Ejemplo resuelto: el círculo de promedios

**Problema:** cien números están escritos en círculo y cada uno es exactamente el promedio de sus dos vecinos. Demuestra que todos son iguales.

**Solución por extremo:** sea M el **máximo** de los cien números (existe: conjunto finito), y toma una posición donde se alcance. Sus vecinos a y b cumplen M = (a + b)/2 con a ≤ M y b ≤ M. Si cualquiera fuera estrictamente menor que M, el promedio sería < M — imposible. Luego **ambos vecinos valen M**. Repitiendo el argumento alrededor del círculo, el valor M se propaga a todos. ∎

Nota la mecánica: el máximo no puede tener vecinos menores *porque es promedio de ellos* — esa es la propiedad gratis, y sola arrastra todo el problema.

## Extremo + contradicción: el descenso infinito

La combinación clásica: para probar que algo no existe, **supón el contraejemplo MÍNIMO y construye a partir de él uno menor**. Contradicción: no había mínimo, luego no había contraejemplos.

Esquema (descenso infinito de Fermat):

1. Supón que existen soluciones «malas»; por buen orden, toma la mínima (en algún sentido: el menor n, la menor suma…).
2. Manipula esa solución mínima para fabricar otra solución mala **estrictamente menor**.
3. Absurdo. No existen soluciones malas.

Ejemplo de sabor: en la demostración de que √2 es irracional vía p² = 2q², de una solución (p, q) se fabrica (q, p/2)… más pequeña — el descenso remata. Lo mismo prueba que x³ = 2y³ no tiene soluciones enteras positivas, y un sinfín de diofánticas.

## Procesos que terminan

«¿El proceso puede continuar para siempre?» — el extremo responde mediante su pariente, el **monovariante** (§3.4): si cada paso del proceso hace decrecer estrictamente una cantidad entera positiva, el buen orden dice que el proceso **se detiene** (no hay descensos infinitos en ℕ). El extremo y el monovariante son las dos caras de «las cantidades discretas no bajan para siempre».

## Galería rápida de usos geométricos

- **El punto más cercano / el par más cercano**: en configuraciones finitas de puntos, empieza por la distancia mínima — nada puede meterse entre ese par.
- **El ángulo más grande / el lado más largo** de un polígono: enfrenta al lado más largo el análisis de ángulos.
- **La envolvente**: el punto más alto, el más a la izquierda — un punto extremo del conjunto está en su «borde», y por él pasan rectas que dejan todo el conjunto de un lado.

## Disparadores

- «**Demuestra que existe**…» (un par cercano, un elemento con cierta propiedad) → considera el extremo: el candidato suele ser el máximo/mínimo de algo.
- **Configuración geométrica finita** (puntos, segmentos, distancias) → ordena distancias o ángulos y agarra la punta.
- «**¿Puede el proceso seguir para siempre?**» → busca el monovariante; el buen orden lo remata.
- «**No existe solución**» en enteros → contraejemplo mínimo + descenso.
- Problema sin asidero aparente → pregunta: *¿qué puedo ordenar aquí?* — y mira la punta.

## Errores comunes

- Invocar máximo de un conjunto **infinito** de reales (puede no existir: (0,1) no tiene máximo). El principio pide finitud — o enteros positivos con mínimo.
- Tomar el extremo y no usar su propiedad especial: si tu argumento sirve para un elemento cualquiera, no necesitabas el extremo (y probablemente no avanza).

## Síntesis

> **Chunk mínimo:** Todo conjunto finito no vacío de reales tiene máximo y mínimo (y los enteros positivos siempre tienen mínimo: buen orden). La táctica: ordena algo, agarra la punta y explota lo que la punta NO puede hacer — el extremo trae propiedades gratis (su vecino no lo supera, nada se mete entre el par mínimo). Círculo de promedios: el máximo es promedio de vecinos ≤ M ⇒ ambos valen M ⇒ se propaga. Descenso infinito = extremo + contradicción: del contraejemplo mínimo fabrica uno menor. Procesos que terminan: monovariante entero decreciente + buen orden. Errores: invocar máximo de infinitos reales; tomar el extremo y no usar su propiedad especial.

---

*Antes del quiz: reconstruye de memoria el enunciado del principio, por qué el extremo trae propiedades gratis, el argumento completo del círculo de promedios y el esquema del descenso infinito.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

El principio extremo convierte una coleccion desordenada en un punto de ataque: toma el menor, mayor o mas saturado y fuerzalo. [[engel-extremo]] profundiza esa cantera, [[arena-q13]] lo usa en pruebas de logica e induccion, y [[arena-sre4]] lo refleja en produccion cuando buscas el cuello de botella o el modo de fallo limite antes de generalizar.
<!-- GRAFO_CONEXO_OLEADA3_END -->
