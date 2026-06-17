# Engel · El principio extremal

*Lección redactada para CogitoErgoSum a partir del capítulo 3 de «Problem-Solving Strategies» (A. Engel), The Extremal Principle (pp. 39-58). Cubre la receta, los tres hechos de base y los ejemplos E1-E2; el resto del capítulo es cantera.*

## La receta

> **Para probar que EXISTE un objeto con cierta propiedad: toma el objeto que MAXIMIZA o MINIMIZA una función bien elegida, y demuestra que si no tuviera la propiedad, una perturbación pequeña mejoraría el extremo — contradicción.**

Por eso Engel lo llama también **método variacional**: el corazón del argumento es la *variación* («si muevo esto un poco, la función mejora — pero ya era óptima»). Dos virtudes que lo hacen favorito:

1. **Da pruebas cortísimas.** Toda la dificultad se concentra en UNA decisión: *qué* función extremar. Elegida bien, la contradicción sale en dos líneas.
2. **Es constructivo.** «Toma el mínimo y mejora mientras se pueda» describe un **algoritmo** que encuentra el objeto bueno (el parlamento de Sikinia del capítulo 1 era exactamente esto: el estado donde el monovariante H alcanza su mínimo ES la partición buscada — invariancia y extremal se dan la mano).

## Los tres hechos de base (p. 40)

Antes de usar un extremo hay que saber que **existe**:

- **Todo conjunto finito no vacío de reales tiene mínimo y máximo** (quizá no únicos — puede haber empate, y no importa: elige cualquiera).
- **Todo subconjunto no vacío de enteros positivos tiene MÍNIMO** aunque sea infinito: es el **principio del buen orden**, lógicamente equivalente a la inducción. Su forma de combate: el **contraejemplo mínimo** («si hubiera contraejemplos, tomo el menor y fabrico uno menor — absurdo») es la inducción disfrazada.
- **Un conjunto infinito de reales puede no tener ni mínimo ni máximo**: el intervalo (0, 1) solo tiene ínfimo y supremo, que no le pertenecen. Este es el supuesto que más se olvida verificar — «tomo el real positivo más pequeño con la propiedad…» es un error si nadie garantizó que exista.

## E1 — ¿en cuántas partes cortan el plano n rectas?

n rectas en posición general (sin dos paralelas, sin tres concurrentes). El conteo amorfo se vuelve **biyección extremal**:

- Gira el plano para que ninguna recta sea horizontal. Cada parte **acotada por abajo** tiene exactamente **UN punto más profundo** (su mínimo), que es uno de los **C(n,2)** puntos de intersección — y cada intersección es el punto profundo de exactamente una parte. Biyección: hay C(n,2) partes acotadas por abajo.
- Las partes **no acotadas por abajo** se cuentan con una recta horizontal auxiliar g, por debajo de todas las intersecciones: las n rectas la cortan en n puntos que la parten en **n + 1** pedazos, y cada pedazo vive en una parte distinta no acotada por abajo.

Total: **C(n,2) + n + 1 = C(n,0) + C(n,1) + C(n,2)**. El extremo («el punto más profundo de cada región») convirtió un conteo sin asideros en una biyección limpia.

## E2 — tetraedros entre n planos

n planos en posición general parten el espacio; Engel demuestra que **al menos (2n − 3)/4 de las partes son tetraedros**. La jugada extremal: para cada plano, mira cada uno de sus dos semiespacios y toma el **vértice MÁS CERCANO** al plano dentro de ese semiespacio; ese vértice, con la cara que lo enfrenta, define un tetraedro que **ningún otro plano puede cortar** — si uno lo cortara, produciría un vértice aún más cercano, contradiciendo la minimalidad. El extremo (distancia mínima) garantiza la *limpieza* del objeto construido; después solo queda contar cuántas veces pudo repetirse cada tetraedro.

## Sylvester-Gallai: el clásico del par extremo

**En todo conjunto finito de puntos del plano, no todos colineales, hay una recta que pasa por exactamente dos de ellos.** La prueba extremal (la que cerró el problema tras décadas): considera todos los pares (recta L por ≥ 2 puntos del conjunto, punto P del conjunto fuera de L) y elige el par con **distancia de P a L mínima**. Si L tuviera tres puntos, dos de ellos quedarían del mismo lado del pie de la perpendicular desde P, y el más lejano de esos dos con la recta que une P al otro formaría un par con distancia **menor** — contradicción. Luego L tiene exactamente dos puntos. ∎ Nota la forma pura de la receta: la función extremada (distancia punto-recta) no aparece en el enunciado — se **eligió** para que la perturbación funcionara.

## Cuándo dispararlo y qué extremar

Frases gatillo: «demuestra que existe…», «siempre hay…», «el proceso termina», configuraciones finitas de puntos/rectas, grafos, torneos. Funciones extremales favoritas:

- **distancia mínima** (entre puntos, de punto a recta — Sylvester-Gallai, E2),
- **ángulo máximo** o mínimo,
- **suma o producto mínimo/máximo** (en grafos: el vértice de grado máximo, el camino más largo),
- **el contraejemplo mínimo** (buen orden = inducción),
- en procesos: el **monovariante** entero acotado que decrece — el proceso muere donde el extremo ya no puede mejorar.

## Disparadores

- «Demuestra que existe X» en una configuración finita → toma el objeto que extrema algo y perturba.
- «El proceso termina» → monovariante entero ≥ 0 estrictamente decreciente.
- «El camino más largo», «el par más cercano», «el primer momento en que…» → ya estás usando el principio; hazlo explícito.
- Vas a tomar un mínimo → verifica ANTES que exista (finito, o enteros positivos; los reales pueden no tenerlo).

## Síntesis

> **Chunk mínimo:** Existencia se prueba extremando: elige el objeto que maximiza/minimiza una función bien elegida y muestra que fallar la propiedad permitiría mejorar el extremo (método variacional; corto y constructivo). Bases: finito no vacío ⇒ hay mín y máx; enteros positivos ⇒ siempre hay mínimo (buen orden = inducción, contraejemplo mínimo); infinitos de reales pueden no tener ninguno. E1: cada parte acotada por abajo tiene UN punto más profundo ⇒ C(n,2) partes + (n+1) no acotadas = C(n,0)+C(n,1)+C(n,2). E2: el vértice más cercano a cada plano da tetraedros limpios, ≥ (2n−3)/4. Sylvester-Gallai: el par (recta, punto) de distancia mínima fuerza una recta con exactamente 2 puntos.

---

*Antes del quiz: reconstruye de memoria la receta y por qué es «variacional», los tres hechos de base (y cuál se olvida siempre), la biyección extremal de E1 con su fórmula, la jugada del vértice más cercano de E2 y la prueba completa de Sylvester-Gallai.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

El principio extremal de Engel es el compañero directo de [[zeitz-32]]. En [[arena-q13]] aparece cuando eliges el objeto minimo o maximo para forzar una contradiccion, y en [[arena-sre4]] se reconoce como buscar el caso limite que dispara cascada, sobrecarga o fallo de simplicidad.
<!-- GRAFO_CONEXO_OLEADA3_END -->
