# Simetría: trabajo que no harás dos veces

*Lección redactada para CogitoErgoSum a partir de la sección 3.1 de Zeitz (Symmetry). Cubre el contenido completo de la unidad.*

## Simetría como herramienta (no como concepto geométrico)

Para el resolvedor, **simetría = una transformación que deja el problema igual**: intercambiar x con y y que nada cambie, reflejar la figura y obtener la misma figura, rotar el tablero y recuperar el tablero.

¿Por qué ahorra trabajo? Porque **cada simetría es información gratuita**: lo que averigües de una parte vale automáticamente para su parte simétrica; lo que valga para un orden de las variables vale para todos los órdenes. Cada simetría que encuentres es trabajo que ya no harás dos veces. Y al revés: una solución de un problema simétrico tiende a ser simétrica (o a venir en familias simétricas) — saber eso restringe dónde buscar.

## WLOG: «sin pérdida de generalidad»

Si el problema **no distingue** entre x e y (intercambiarlas deja el enunciado idéntico), puedes suponer x ≤ y. Eso es WLOG (*without loss of generality*): la simetría te **autoriza** a elegir un caso porque cualquier otro caso es el mismo problema con etiquetas cambiadas — la demostración para tu caso se traduce automáticamente a los demás aplicando la transformación.

**Cuándo es legítimo:** solo cuando la transformación que lleva el caso general a tu caso especial **deja invariante el enunciado completo** (hipótesis Y conclusión).

**Cuándo es ilegítimo:** cuando algo SÍ distingue las variables. Si la hipótesis dice «x es par», no puedes WLOG intercambiar x con y; si la conclusión trata distinto a a y b, tampoco. El abuso de WLOG es un error clásico: siempre verifica que la simetría exista *en todo el enunciado*, no solo en la parte que te conviene.

## Simetría algebraica: polinomios simétricos

Una expresión es **simétrica** en x, y si intercambiarlas la deja igual: x + y, xy, x² + y², x³ + y³…

Hecho central: **toda expresión simétrica en x, y se reescribe en términos de s = x + y y p = xy** (los polinomios simétricos elementales). Las identidades de uso diario:

- x² + y² = s² − 2p
- (x − y)² = s² − 4p
- x³ + y³ = s³ − 3sp
- 1/x + 1/y = s/p

**El ejemplo del disparador:** x + y = 7, xy = 5; te piden x² + y². No resuelvas para x e y (saldrían irracionales feos): x² + y² = s² − 2p = 49 − 10 = **39**. Lo simétrico se calcula sin conocer las variables. Esta jugada reaparece en Vieta (§5.4): los coeficientes de un polinomio te dan s y p directamente.

## Imponer simetría donde no la hay

La jugada avanzada: si el problema no es simétrico, **fabrica la simetría que falta**.

- **El pareo de Gauss:** para sumar S = 1 + 2 + ⋯ + 100, escribe la suma al derecho y al revés y suma ambas: cada columna da 101, hay 100 columnas, 2S = 100·101, S = 5050. La suma original no era simétrica; *duplicarla* la volvió simétrica.
- **Reflejar un punto:** el problema del camino mínimo que toca una recta (ir de A a B pasando por un río) se resuelve reflejando B al otro lado: el camino mínimo A→río→B es la recta A→B′. La reflexión crea la simetría que endereza el camino.
- **Completar la figura:** extender un triángulo a paralelogramo, un semicírculo a círculo — la figura completa tiene simetrías que la mitad no tenía.

## Simetría en juegos: la estrategia del espejo

**El acertijo de la mesa redonda:** dos jugadores colocan por turnos monedas idénticas sobre una mesa redonda, sin encimarse; pierde quien ya no pueda colocar. **Gana el primero**: coloca su primera moneda exactamente en el **centro** (el único punto fijo de la simetría de la mesa) y, a partir de ahí, **copia cada jugada del rival reflejada por el centro** (punto diametralmente opuesto). Si el rival pudo colocar, el lugar simétrico está libre por construcción — el espejo garantiza que el primero siempre tiene respuesta, así que el que se queda sin lugares es el segundo.

La estructura general: **quien puede instalar y mantener una simetría del juego, convierte la simetría en victoria** — su respuesta está garantizada mientras la simetría se conserve. (Reaparecerá en Engel, capítulo de juegos, como «estrategia de pareo».)

## Disparadores

- El enunciado no cambia al intercambiar variables → trabaja con s = x+y, p = xy; considera WLOG.
- «De A a B tocando una recta/pared/río» → refleja.
- Suma o producto con principio y final emparejables → pareo de Gauss.
- Juego por turnos en tablero/mesa con simetría → estrategia del espejo (busca el punto fijo).
- Figura que parece la mitad de algo → complétala.

## Síntesis

> **Chunk mínimo:** Simetría = transformación que deja el problema igual; cada una es información gratuita (lo probado en una parte vale en su simétrica). **WLOG** es legítimo solo si la transformación deja invariante el enunciado COMPLETO (hipótesis y conclusión). Toda expresión simétrica en x, y se reescribe con s = x+y, p = xy: x²+y² = s²−2p, (x−y)² = s²−4p, x³+y³ = s³−3sp, 1/x+1/y = s/p. Si no hay simetría, fabrícala: pareo de Gauss (suma al derecho y al revés), reflejar el punto (camino mínimo que toca una recta), completar la figura. En juegos: quien instala y mantiene una simetría gana — centro de la mesa redonda + respuesta diametral.

---

*Antes del quiz: reconstruye de memoria la definición de simetría como herramienta, qué autoriza exactamente un WLOG (y cuándo es trampa), las identidades s-p, y la estrategia ganadora de la mesa redonda.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

La simetria reduce casos porque identifica lo que realmente cambia y lo que no. Esa misma compresion aparece en [[arena-q12]] al buscar invariantes, en [[aime-geo]] al elegir coordenadas o reflejos, y en [[zeitz-85a]] cuando una transformacion rigida conserva distancias y angulos.
<!-- GRAFO_CONEXO_OLEADA3_END -->
