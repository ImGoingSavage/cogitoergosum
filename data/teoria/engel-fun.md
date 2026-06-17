# Ecuaciones funcionales

*Lección redactada para CogitoErgoSum a partir del capítulo de ecuaciones funcionales de Engel (Problem-Solving Strategies). Cubre el contenido completo de la unidad.*

## La idea central

Una ecuación funcional no especifica los valores de f sino una **relación que f debe satisfacer para todos los argumentos**. La estrategia no es resolver por manipulación algebraica directa —como con ecuaciones ordinarias— sino **obtener información incremental** mediante sustituciones hábiles, deducir propiedades estructurales (inyectividad, paridad, crecimiento) y, solo entonces, conjeturar y verificar la familia de soluciones.

## El protocolo de ataque

### Paso 1: sustituciones especiales

Cada sustitución es un «caso pequeño» que arranca información concreta sobre f:

- **y = 0** y **x = 0**: suelen despegar f(0) o establecer f(0) = 0.
- **x = y**: da f en términos de f(x)² o f(2x), según la ecuación.
- **y = −x**: relaciona f(x) con f(−x), revelando si f es par o impar.
- **x = 1** o **y = 1**: calibra constantes multiplicativas o fuerza una condición algebraica puntual.
- **x ↔ y** (intercambiar): si la ecuación no es simétrica, obtienes una nueva ecuación que puede combinarse con la original.

### Paso 2: propiedades estructurales

Con la información del paso 1, deduce:

- **Inyectividad** (f(a) = f(b) ⇒ a = b): permite «cancelar» f en ambos lados. Se prueba sustituyendo la condición f(a)=f(b) en la ecuación funcional y derivando a=b.
- **Sobreyectividad** (para todo y existe x con f(x)=y): permite «elegir x tal que f(x) sea lo que necesitas». Se prueba construyendo explícitamente ese x.
- **Paridad**: ¿es f par (f(−x)=f(x)), impar (f(−x)=−f(x)) o ninguna?
- **f(0)**: casi siempre se fuerza en el primer paso.

### Paso 3: conjeturar y verificar

Con los valores y propiedades acumulados, **adivina la familia** de soluciones candidatas: f(x) = cx, f(x) = cx + d, f(x) = xⁿ, f(x) = aˣ, f(x) = 0, f ≡ constante.

**Siempre** sustituye la conjetura en la ecuación original para confirmar que la satisface. Luego argumenta **unicidad**: dado lo que sabes de f (los valores forzados, la inyectividad…), la función está completamente determinada.

## La ecuación de Cauchy y sus parientes

**f(x + y) = f(x) + f(y)** es la ecuación de Cauchy aditiva. Sus consecuencias:

1. Por inducción, f(n) = nf(1) = nc para todo n ∈ ℕ.
2. De f(1) = f(1/q · q) = qf(1/q), se sigue f(1/q) = c/q y f(p/q) = cp/q: f es lineal sobre ℚ.
3. Para extender a ℝ, basta **una** hipótesis de regularidad: continuidad en un punto, monotonía, o acotación en un intervalo. Cualquiera de las tres fuerza f(x) = cx para todo x real.
4. Sin ninguna hipótesis de regularidad, existen soluciones patológicas (que usan el axioma de elección y no son medibles). En olimpiada, el enunciado siempre da una hipótesis extra —buscarla.

**Parientes de Cauchy**:

| Ecuación | Forma de la solución |
|---|---|
| f(x+y) = f(x)f(y) (f continua) | f(x) = aˣ (o f ≡ 0) |
| f(xy) = f(x) + f(y) (f continua, x,y > 0) | f(x) = c·log x |
| f(xy) = f(x)f(y) (f continua) | f(x) = xᵃ |
| f(x+y) = f(x) + f(y) + f(x)f(y) | f(x) = g(x)−1 donde g es exponencial |

La primera transformación es tomar logaritmos o exponenciales para convertir una pariente en la ecuación de Cauchy estándar.

## Trampa clásica: asumir regularidad no dada

Dar por hecho que f es continua o diferenciable cuando el enunciado no lo dice es un error grave. Si el dominio es ℤ o ℚ, no existe el problema de las soluciones patológicas y la inducción basta; si el dominio es ℝ, verificar qué hipótesis da el enunciado antes de aplicar el paso 3.

## Disparadores

- «f(x+y)=f(x)+f(y)» → Cauchy; over ℚ basta inducción, over ℝ necesita hipótesis de regularidad.
- «¿Qué funciones continuas satisfacen…?» → la continuidad es la hipótesis que elimina las soluciones patológicas.
- «Sustituir y=0 da f(f(x))=…» → sustituciones especiales; la composición de f consigo misma es información directa.
- «La ecuación es simétrica en x, y» → la familia de soluciones probablemente también lo es.

## Síntesis

> **Chunk mínimo:** Protocolo: (1) sustituciones especiales (0,0), (x,x), (x,−x), (1,y) → acumular valores; (2) propiedades estructurales: inyectividad (cancelar f), sobreyectividad (elegir preimagen), paridad, f(0); (3) conjeturar familia (lineal, exponencial, log, potencia) + VERIFICAR en la ecuación original + argumentar unicidad. Cauchy f(x+y)=f(x)+f(y): lineal sobre ℚ por inducción; sobre ℝ necesita una hipótesis de regularidad (continuidad, monotonía, acotación en un intervalo) para forzar f(x)=cx. Parientes: multiplicativa → exponencial; logarítmica → logaritmo. Trampa: no asumir regularidad sin que el enunciado la dé.

---

*Antes del quiz: reconstruye de memoria las cuatro sustituciones especiales más frecuentes, cuándo se necesita la hipótesis de regularidad en Cauchy y la tabla de las tres variantes de Cauchy con sus soluciones.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Las ecuaciones funcionales exigen tratar una regla como objeto de prueba: probar valores, forzar simetrias y usar invariantes. [[arena-q13]] aporta el marco de logica y juegos de estrategia, [[zeitz-54]] recuerda el papel de identidades polinomiales, y [[aime-alg]] practica sustituciones controladas.
<!-- GRAFO_CONEXO_OLEADA3_END -->
