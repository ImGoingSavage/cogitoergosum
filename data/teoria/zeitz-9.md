# Cálculo de competencia: convergencia y matemática euleriana

*Lección redactada para CogitoErgoSum a partir de las secciones 9.2 y 9.4 de Zeitz (Convergence and Continuity; Eulerian mathematics). Cubre el contenido completo de la unidad.*

## El piso de todo: la definición de convergencia

> **aₙ → L** significa: para todo ε > 0 existe N tal que, desde N en adelante, **|aₙ − L| < ε**.

(Reto cualquier margen de error ε; siempre hay un punto a partir del cual la sucesión vive dentro de ese margen alrededor de L.) Todo el cálculo —límites, continuidad, derivadas, integrales— se apoya en esta sola definición: dominarla es dominar el piso del edificio.

## Las seis vías para probar convergencia

1. **Dibuja.** Grafica los términos: el dibujo conjetura el límite y el modo de acercarse (¿monótono?, ¿oscilante?).
2. **Adivina L y acerca los términos:** estima |aₙ − L| directamente y muéstralo < ε.
3. **Propiedad de Cauchy:** demuestra que los términos **se acercan ENTRE SÍ** (|aₘ − aₙ| → 0). Es la vía cuando **no tienes idea del valor del límite** — no menciona a L para nada, y en los reales Cauchy ⟺ convergente.
4. **Monótona y acotada ⇒ converge.** Creciente con techo (o decreciente con piso) siempre tiene límite. **La trampa señalada por el banco:** «creciente y acotada por 4, luego converge **a 4**» — lo correcto es solo que converge a ALGO ≤ 4; **la cota no tiene por qué ser el límite** (1 − 1/n es creciente, acotada por 4, y converge a 1). La cota da existencia, no el valor.
5. **Sándwich (squeeze):** bₙ ≤ aₙ ≤ cₙ con bₙ y cₙ → L fuerza aₙ → L. (Pariente directo del massage de §5.5: encajar entre cotas telescópicas.)
6. **Big-O / little-o:** compara tasas de crecimiento y quédate con lo que importa.

## La lupa big-O

- **f = O(g):** |f| ≤ C·|g| eventualmente (f no crece más rápido que g, salvo constante).
- **f = o(g):** f/g → 0 (f es despreciable frente a g).

Su gracia: permite **álgebra de errores** — O(x²)·x = O(x³), O(x²) + O(x³) = O(x³) para x grande — y por lo tanto quedarse con «la parte que importa» de una expresión sin arrastrar términos muertos. Es el idioma de las estimaciones (el mismo de la complejidad de algoritmos) y la versión formal de la jerarquía de crecimiento de §5.5.

## Matemática euleriana: doblar las reglas para conjeturar

**Definición de Zeitz:** razonamiento no riguroso —incluso «incorrecto»— que **conduce a una verdad**, bautizado en honor a Euler (maestro de manipular lo infinito sin permiso y atinar). Los **dos momentos** donde conviene aflojar el rigor:

1. **Al explorar**: para encontrar el candidato a respuesta.
2. **Al planear**: para decidir qué vale la pena intentar demostrar.

**La regla de oro que la separa de la charlatanería:** se dobla el rigor **para conjeturar, NUNCA para concluir** — la conjetura euleriana se verifica rigurosamente después, o no se afirma.

**Ejemplo 9.4.5 (Δ como derivada):** una sucesión cumple que la diferencia de las diferencias es constante: Δ(ΔA) = (1, 1, 1, …). Eulerianamente, Δ «se parece» a la derivada: d²A/dn² = 1 sugiere A ≈ n²/2 + bn + c — **conjetura: aₙ es cuadrática en n**. La verificación rigurosa (inducción / telescopio, §5.3) la confirma. El cálculo continuo iluminó al problema discreto.

**Ejemplo 9.4.6 (producto máximo con suma fija):** ¿cómo partir S en partes positivas para maximizar el producto? Versión continua: partes iguales de tamaño x dan (S/x)... el producto (S/x partes de tamaño x) es x^(S/x), que se maximiza en **x = e ≈ 2.718** (cálculo de una variable). «Partes de tamaño e» no significa nada para enteros — pero **enfoca la atención en partes de 2 y 3** (los enteros vecinos de e). De ahí, el cierre riguroso discreto: nunca uses partes ≥ 5 (4 = 2+2 empata, 5 < 2·3 mejora al partirse), nunca más de dos 2 (2+2+2 = 3+3 pero 8 < 9 — tres 2 pierden contra dos 3): **usa todos los 3 posibles y completa con 2.**

**El acertijo del banco — suma 20:** 20 = 3+3+3+3+3+3+2 → producto máximo **3⁶·2 = 1458**. (La heurística continua eligió el tamaño; la aritmética de 2 y 3 cerró el argumento.)

## Disparadores

- «Demuestra que converge» sin pista del límite → **Cauchy** o **monótona + acotada**.
- Estimar sumas/productos enormes (Σ1/√n, productos infinitos) → sándwich con cotas telescópicas (§5.3/§5.5) y big-O para despreciar colas.
- Problema discreto que «huele» a cálculo (diferencias ≈ derivadas, máximos) → resuélvelo eulerianamente en versión continua, luego ciérralo discreto.
- Optimizar productos con suma fija → partes de 3 (y 2) — y recuerda de dónde salió: e.
- Tentación de concluir desde la heurística → regla de oro: conjetura sí, conclusión no.

## Síntesis

> **Chunk mínimo:** aₙ → L: para todo ε > 0 hay N con |aₙ − L| < ε desde N. Seis vías: dibuja; estima |aₙ − L|; Cauchy (los términos se acercan ENTRE SÍ — la vía sin conocer L); monótona + acotada (da existencia, NO el valor: la cota no es el límite); sándwich (massage con cotas telescópicas); big-O/little-o (álgebra de errores: quédate con la parte que importa). Matemática euleriana: dobla el rigor para CONJETURAR, jamás para concluir — Δ se parece a derivada (Δ²A = 1 ⇒ aₙ cuadrática, luego inducción); producto máximo con suma fija: el continuo señala e ⇒ el discreto cierra con «todos los 3 posibles y completa con 2» (20 → 3⁶·2 = 1458).

---

*Antes del quiz: reconstruye de memoria la definición ε-N, las seis vías (y cuál no necesita conocer L), el error «converge a la cota», la regla de oro euleriana y el cierre completo del producto máximo con suma 20.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

El calculo de competencia une convergencia, series y manipulacion euleriana. [[arena-p4]] ofrece el marco de calculo para finanzas cuantitativas, [[arena-q5]] conecta derivadas con mercados, y [[zeitz-53]] muestra que muchas series primero se vuelven manejables por telescopio.
<!-- GRAFO_CONEXO_OLEADA3_END -->
