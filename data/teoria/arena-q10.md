# Arena Quant · Distribuciones, geometría y estadísticos de orden

Cuando un problema mezcla varias variables uniformes o pregunta «¿cuál es la probabilidad de que…?», casi siempre el atajo es **dibujarlo como un área** en el cuadrado o el cubo unitario. Y cuando aparece «el máximo / el mínimo / el k-ésimo», es un **estadístico de orden**.

## Probabilidad como área

- **Romeo y Julieta llegan al azar entre las 9 y las 10; cada uno espera 15 min. ¿P(se encuentran)?** Toma x, y uniformes en [0,1]; se encuentran si |x − y| ≤ ¼. El complemento son dos triángulos que forman un cuadrado de lado ¾: área 9/16. Respuesta: 1 − 9/16 = **7/16**.
- **Rompes un palo en dos puntos uniformes. ¿P(forman triángulo)?** Los tres trozos forman triángulo si ninguno supera ½. En el cuadrado unitario la región válida son dos medios cuadraditos → área **1/4**.

La metáfora rectora: «dos uniformes → un punto en el cuadrado; la pregunta es qué fracción del cuadrado cumple la condición».

## El problema del avión (asientos)

«100 personas abordan en orden; la abuela (1.ª) se sienta al azar; cada siguiente toma su asiento si está libre, si no uno al azar. ¿P(el pasajero 100 acaba en su asiento)?»

Condiciona en el evento correcto: el primer pasajero «desplazado» que tenga elección acabará en el asiento 1 o en el 100, y ambos son simétricos. Respuesta: **1/2**, sin álgebra. Es el ejemplo canónico de «condiciona en el evento que colapsa el problema».

## Estadísticos de orden de uniformes

Para n uniformes i.i.d. en [0,1]:

> P(máx ≤ x) = xⁿ ⟹ densidad n·x^{n−1} ⟹ **E(máx) = n/(n+1)**

Por simetría **E(mín) = 1/(n+1)**, y por linealidad **E(máx − mín) = (n−1)/(n+1)**. En general, la densidad del k-ésimo estadístico de orden es

> f_{(k)}(x) = n!/[(k−1)!(n−k)!] · f(x)·F(x)^{k−1}·(1−F(x))^{n−k}

(es una Beta cuando los datos son uniformes). La **CDF de una U(a,b)** es F(x) = (x−a)/(b−a) en [a,b].

## Convolución: suma de dos uniformes

La densidad de X+Y con X,Y ~ U(0,1) es **triangular**: h(z)=z en [0,1], h(z)=2−z en [1,2]. Sale de la convolución h(z)=∫f(z−y)g(y)dy partiendo en casos según los límites. Patrón general: la densidad de una suma es la convolución de las densidades.

## Dos joyas de la Gaussiana

- **X ~ N(μ,σ):** E(X²) = σ² + μ² (de Var = E(X²) − (EX)²); y la función generatriz de momentos **E(e^{λX}) = exp(μλ + σ²λ²/2)**. Esta segunda fórmula es la base de la valoración lognormal.
- **Si M es la Gaussiana acumulada y X ~ N(0,1), ¿E[M(X)]?** Como M(X) ~ U(0,1) (la transformada integral de probabilidad), **E[M(X)] = 1/2**. Elegante: aplicar la propia CDF a su variable la uniformiza.

## Teorema del Límite Central (lo que de verdad dice)

Para X₁,…,Xₙ i.i.d. con media μ y varianza σ² **finita**, la suma estandarizada (Sₙ − μn)/(σ√n) **converge en distribución** a N(0,1) — sin importar la distribución de partida. La condición clave es el segundo momento finito (por eso la Cauchy no obedece). Una matriz de covarianzas es siempre semidefinida positiva porque la varianza de cualquier combinación lineal aᵀX es aᵀCa ≥ 0.

## Disparadores

| Señal | Jugada |
|-------|--------|
| "dos tiempos/longitudes al azar" | dibuja un punto en el cuadrado, mide el área |
| "máx / mín / k-ésimo de n" | estadístico de orden; E(máx)=n/(n+1) |
| "densidad de una suma" | convolución de densidades |
| "E(e^{λX}), X normal" | MGF lognormal exp(μλ+σ²λ²/2) |
| "aplica la CDF a su variable" | sale uniforme → E=1/2 |

> ❧ **Síntesis:** geometría para probabilidades de uniformes (área en el cuadrado), estadísticos de orden para máx/mín/k-ésimo, convolución para sumas, y la MGF gaussiana exp(μλ+σ²λ²/2) como puente hacia la valoración lognormal. El TLC funciona solo con segundo momento finito.

---

*Retrieval: cierra la página y responde — (1) P(Romeo y Julieta se encuentran); (2) P(pasajero 100 en su asiento); (3) E(máx) de n uniformes; (4) E(e^{λX}) para X ~ N(μ,σ).*
