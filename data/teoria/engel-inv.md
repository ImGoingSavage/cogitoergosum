# Engel · El principio de invariancia

*Lección redactada para CogitoErgoSum a partir del capítulo 1 de «Problem-Solving Strategies» (A. Engel), The Invariance Principle. Cubre la teoría y los ejemplos E1-E5; el resto del capítulo es cantera.*

## El lema central

> **SI HAY REPETICIÓN, BUSCA LO QUE NO CAMBIA.**

Ante cualquier **algoritmo** (un juego, una transformación que se repite, una operación «en cada paso puedes…»), Engel manda hacerse **cuatro preguntas**:

1. ¿Puede alcanzarse tal **estado final**?
2. ¿Cuáles son **TODOS** los estados finales posibles?
3. ¿Hay **convergencia** (el proceso termina)?
4. ¿Hay **períodos** (el proceso cicla)?

**El invariante es la herramienta directa de la pregunta 1** (y reduce drásticamente la 2): si I se conserva en cada paso e I(inicial) ≠ I(final deseado), el estado es inalcanzable. Para la 3, la herramienta es el monovariante (abajo).

## El catálogo, con los ejemplos E1-E5

- **Producto (E1):** la operación reemplaza x, y por nuevas combinaciones cuyo producto reproduce xy → **xₙyₙ = ab para siempre**: el estado final está atado al inicial.
- **Paridad de la suma (E2):** borrar a, b y escribir **|a − b|** cambia la suma en a + b − |a−b| = **2·min(a, b)** — siempre PAR. La paridad de la suma inicial decide la del número final.
- **Suma alternada (E3):** con números en círculo y la operación «incrementa dos VECINOS en 1», la suma alternada a₁ − a₂ + a₃ − ⋯ **no cambia** (los dos vecinos entran con signos opuestos). 
- **Monovariante (E4):** abajo.
- **Distancia al origen (E5):** abajo.

**El acertijo del banco, resuelto con E2:** en el pizarrón están 1, 2, …, 2n con n **impar**; repetidamente borras a, b y escribes |a − b|. Suma inicial: S = 2n(2n+1)/2 = **n(2n+1)**, que con n impar es **impar × impar = impar**. Cada paso cambia S en un número par → la paridad se conserva → el último número tiene la paridad de S: **impar**. ∎

**El error del banco (círculo 1,0,1,0,0,0, incrementar dos vecinos):** «la suma crece de 2 en 2 y 2 divide a la suma objetivo, así que se puede». Falla porque **un invariante compatible no demuestra posibilidad** — solo que ESE invariante no obstruye. Y aquí otro invariante sí obstruye: la **suma alternada** (E3) vale 1 − 0 + 1 − 0 + 0 − 0 = 2 al inicio y debe valer 0 en cualquier estado «todo igual» (a − a + a − a + a − a = 0). 2 ≠ 0: imposible. La moraleja doble: (1) posibilidad se demuestra con una construcción, no con la ausencia de UNA obstrucción; (2) ten SIEMPRE más de un candidato a invariante.

## El monovariante: la flecha que garantiza el final

**E4 — el parlamento de Sikinia:** cada miembro tiene a lo sumo 3 enemigos (la enemistad es mutua). Hay que partir el parlamento en dos cámaras tal que cada quien tenga **a lo sumo 1 enemigo en su propia cámara**.

**La solución modelo:** toma cualquier partición inicial y define **H = número total de pares de enemigos que comparten cámara**. Mientras alguien tenga ≥ 2 enemigos en su cámara, **muévelo a la otra**: pierde ≥ 2 enemistades internas y gana a lo sumo 1 (tenía ≤ 3 en total) → **H decrece estrictamente**. H es un entero ≥ 0: **no puede decrecer para siempre** → el proceso termina, y en el estado final nadie tiene 2 enemigos internos — exactamente la propiedad pedida. ∎

Nota la estructura: el monovariante **no es un invariante estricto — es una flecha**. Y el argumento es además **constructivo**: describe un algoritmo que encuentra la partición. El estado donde H alcanza su mínimo ES el objeto bueno — aquí invariancia y **principio extremal** (capítulo 3) se dan la mano.

## E5: la función estrella para puntos que se mueven

Para procesos sobre **puntos o vectores** (cada paso transforma posiciones), la función a vigilar es **la distancia al origen** (o su cuadrado, que evita raíces — el truco |z|² de §4.2). En E5, una identidad algebraica más el invariante lineal a+b+c+d = 0 demuestran que la distancia al origen **crece geométricamente** con cada paso → alguna coordenada explota → comportamiento a largo plazo decidido **sin calcular una sola órbita**.

## El método de trabajo (en orden)

Ante un proceso repetido, prueba como candidatos a invariante, **en este orden**:

1. **Paridad** (de sumas, de conteos),
2. **Suma**,
3. **Suma alternada** (si hay estructura circular o de signos),
4. **Producto**,
5. **Residuos mod m** (m = 3, 4, 9 según el paso),
6. y si nada es constante, **busca algo MONÓTONO** (un monovariante: energía, suma de cuadrados, pares en conflicto).

Pista de diseño: el invariante correcto suele ser **la combinación lineal que el paso del proceso aniquila** — escribe el cambio genérico de un paso e iguala a cero los coeficientes.

## Disparadores

- «En cada paso puedes… ¿es alcanzable X?» → batería en orden: paridad, suma, alternada, producto, mod m.
- «¿El proceso termina siempre?» → monovariante entero acotado.
- Puntos/vectores iterados → distancia al origen al cuadrado.
- Tu invariante es compatible con el objetivo → cuidado: eso NO demuestra que se pueda; busca otra obstrucción o construye la secuencia.

## Síntesis

> **Chunk mínimo:** Si hay repetición, busca lo que no cambia. Cuatro preguntas ante todo algoritmo: ¿alcanzable tal final?, ¿cuáles son TODOS los finales?, ¿converge?, ¿cicla? El invariante responde la 1: si I se conserva e I(inicial) ≠ I(final), inalcanzable. Batería en orden: paridad → suma → suma alternada (círculos: vecinos entran con signos opuestos) → producto → mod m → y si nada es constante, **monovariante** (entero acotado que decrece ⇒ el proceso termina; Sikinia: mover al de ≥2 enemigos internos baja H y el algoritmo construye la partición). Ojo: un invariante compatible NO demuestra posibilidad — posibilidad se demuestra construyendo. Puntos iterados → distancia al origen al cuadrado.

---

*Antes del quiz: reconstruye de memoria el lema y las cuatro preguntas, el argumento completo de 1…2n con n impar, el monovariante de Sikinia con su doble lección (flecha + algoritmo) y por qué «las cuentas cuadran» no prueba posibilidad.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

El principio de invariancia de Engel profundiza [[zeitz-34]]: si algo no cambia, restringe todo el proceso. [[arena-q12]] lo usa para brainteasers de conteo, y [[arena-cc3]] lo convierte en argumento de terminacion o correccion cuando un algoritmo recursivo debe conservar una propiedad.
<!-- GRAFO_CONEXO_OLEADA3_END -->
