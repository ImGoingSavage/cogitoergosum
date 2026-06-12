# El diccionario de heurística de Pólya: seis entradas esenciales

*Lección redactada para CogitoErgoSum a partir del «Breve diccionario de heurística» de Pólya. Cubre las seis entradas de la unidad: analogía, descomponer y recomponer, generalización, particularización, trabajar hacia atrás e inducción.*

## Cómo usar este material

El diccionario de Pólya no se lee de corrido: es un **catálogo de jugadas mentales**. Cada entrada es una herramienta con su situación de uso. Lo que entrena no es memorizarlas sino reconocer *cuándo* pide cada una el problema.

---

## 1. Analogía

**Qué es:** resolver un problema más simple que tenga *la misma estructura* y trasplantar el método.

El ejemplo canónico de Pólya: para encontrar el centro de gravedad de un **tetraedro** (3D), estudia primero el del **triángulo** (2D). El triángulo no solo es más fácil: su solución (las medianas se cortan en un punto que las divide 2:1) sugiere *el método* para el tetraedro (las rectas de cada vértice al centroide de la cara opuesta).

La analogía útil no es superficial («ambos hablan de monedas») sino **estructural**: mismos roles, mismas relaciones, distinta carne.

**Señal de uso:** el problema vive en dimensión alta, con muchos objetos o con una configuración intimidante → busca el primo pequeño con el mismo esqueleto.

## 2. Descomponer y recomponer

**Qué es:** trocear el problema en partes (datos por un lado, condición por cláusulas, casos por separado) y reensamblar.

**La advertencia de Pólya:** no descompongas **demasiado pronto ni demasiado fino**. Primero intenta ver el problema *como un todo* — comprenderlo completo, sentir su forma. Quien lo pulveriza de entrada pierde de vista las conexiones entre las partes, y suele ahogarse en detalles que el problema global habría vuelto irrelevantes. Descompón cuando el todo ya no dé más de sí, y mantén siempre un ojo en cómo se recompone.

## 3. Generalización

**Qué es:** pasar de un objeto a una clase entera que lo contiene — de «este 7» a «todo n», de este triángulo a cualquier polígono.

Lo contraintuitivo: **a veces la afirmación más general es más fácil de probar**. Pólya lo llama la **paradoja del inventor**: el plan más ambicioso puede tener más probabilidades de éxito. ¿Por qué? Porque la afirmación general expone *la estructura* que importa, sin el ruido de los valores concretos; y porque la inducción, por ejemplo, necesita una hipótesis suficientemente fuerte para sostenerse a sí misma.

**Ejemplo clásico:** sumar 1 + 2 + ⋯ + 100 es un caso; probar que 1 + 2 + ⋯ + n = n(n+1)/2 te da una palanca (inducción, pareo de Gauss) que el caso aislado no sugiere.

## 4. Particularización

**Qué es:** lo inverso — bajar de la clase al caso concreto. Los **casos extremos y degenerados** son tests rápidos de cualquier conjetura: ¿qué pasa si n = 0, n = 1? ¿Si el triángulo se aplasta hasta ser un segmento? ¿Si la velocidad es 0 o infinita?

Usos:

- **Refutar rápido**: un caso especial que falla mata la conjetura sin más trabajo.
- **Generar intuición**: los casos pequeños hechos a mano revelan el patrón (esto conecta con «ensúciate las manos» de Zeitz).
- **Comprender el enunciado**: si no entiendes la afirmación general, mira qué dice para n = 2.

**Cuándo ayuda cada una:** generaliza cuando el caso concreto esconde la estructura o cuando necesitas una hipótesis inductiva más fuerte; particulariza cuando necesitas datos, intuición o un test barato de plausibilidad.

## 5. Trabajar hacia atrás (regresión)

**Qué es:** en vez de avanzar desde los datos, **parte de lo que buscas** y pregúntate: ¿de qué se obtendría esto? ¿Qué necesitaría tener justo antes? Se construye la cadena meta ← penúltimo ← antepenúltimo… hasta tocar los datos, y luego se recorre de frente.

El ejemplo clásico: medir exactamente 6 litros con jarras de 4 y 9. Hacia adelante hay demasiadas movidas posibles; hacia atrás casi no hay opciones: para tener 6 en la jarra de 9 necesito quitarle 3; quito 3 si la de 4 ya tiene 1; tengo 1 en la de 4 si… — la cadena se arma sola.

**Señal de uso:** la **meta es clara y específica**, pero el punto de partida ofrece demasiadas opciones. Cuando el árbol de movidas hacia adelante explota y hacia atrás se adelgaza, camina hacia atrás.

## 6. Inducción (en el sentido de Pólya)

**Qué es:** el procedimiento del científico aplicado a la matemática — observar casos, detectar regularidades, conjeturar, y *después* demostrar. Pólya distingue la **inducción** (heurística: generar la conjetura plausible) de la **inducción matemática** (demostrativa: probarla rigurosamente; la verás a fondo con Zeitz §2.3).

El flujo completo: casos pequeños → tabla → patrón → conjetura → demostración. Saltarse los primeros pasos deja sin materia prima a los últimos; quedarse en la conjetura sin demostrar no es matemática todavía.

---

## Tabla de disparadores

| Señal del enunciado | Jugada |
|---|---|
| Objeto en 3D / configuración intimidante | Analogía (primo en 2D / versión chica) |
| Problema enorme con cláusulas separables | Descomponer (pero no demasiado pronto) |
| El caso concreto esconde la estructura | Generalizar |
| Conjetura sin evidencia / enunciado opaco | Particularizar (casos extremos) |
| Meta clara, inicio con demasiadas opciones | Trabajar hacia atrás |
| «Encuentra el patrón / conjetura una fórmula» | Inducción: tabla de casos primero |

## Síntesis

> **Chunk mínimo:** Seis jugadas con su gatillo: **Analogía** = primo simple con la misma estructura (tetraedro ← triángulo) — dispara ante 3D/configuración intimidante. **Descomponer y recomponer** — pero no demasiado pronto: primero el todo. **Generalizar** = subir a la clase entera; paradoja del inventor: lo general puede ser MÁS fácil (expone estructura, fortalece la hipótesis inductiva). **Particularizar** = casos extremos/degenerados para refutar rápido, generar intuición o entender el enunciado. **Hacia atrás** = cuando la meta es clara y el inicio explota en opciones (jarras de 4 y 9). **Inducción (de Pólya)** = casos → tabla → patrón → conjetura → y DESPUÉS demostración.

---

*Antes del quiz: para cada una de las seis entradas, intenta decir de memoria (1) qué es en una frase y (2) una señal que la dispara.*
