# Arena Quant · Probabilidad condicional, Bayes y conteo

La mayoría de los errores en entrevista no son de cálculo: son de **espacio muestral**. Antes de dividir, escribe los casos elementales y sus probabilidades. Bayes formaliza la actualización; la simetría y el conteo cuidadoso hacen el resto.

## Bayes con tasa base

«Bolsa con 9 monedas normales y 1 de dos caras. Saco una, sale cara 3 veces. ¿P(es la de dos caras)?»

> P(2caras | CCC) = (1·1/10) / (1·1/10 + 1/8·9/10) = **8/17 ≈ 0.47**

La trampa: la verosimilitud (1 vs 1/8) empuja fuerte hacia la moneda trucada, pero la **tasa base** (1/10 vs 9/10) la frena. El resultado, 8/17, vive entre ambas fuerzas. Esto es el mismo motor que el valor predictivo positivo de un test médico.

«Saco una moneda normal de mi bolsillo y salen 3 caras. ¿P(la siguiente es cara)?» Si crees que es justa: **1/2** (las tiradas son independientes). Pero con 100 caras seguidas, P=2^{−100} bajo "justa": ahora el prior importa y P(dos caras | N caras) = p / (p + (1−p)2^{−N}) → ≈ 1. Lección: sin información extra, una moneda «de aspecto normal» es justa; el dato extremo activa el razonamiento bayesiano.

## Simetría: la navaja del conteo

- **Dos cartas de un mazo ordenado A>K>…>2; tú sacas una, yo otra. ¿P(la mía > la tuya)?** Divide: misma rango (prob 3/51) o distinto. Si distinto, por simetría ½. Respuesta: ½·48/51 = **24/51**.
- **Cajón con 2 rojos y 2 negros; sacas 2. ¿P(emparejan)?** Tras sacar uno quedan 3, solo 1 empareja → **1/3**.
- **Torneo eliminatorio con 2ⁿ equipos, el mejor rankeado siempre gana. ¿P(el 2.º mejor juega la final)?** El 2.º solo llega a la final si cae en la otra mitad del cuadro: **2^{n−1}/(2ⁿ−1)**.

## Conteo y linealidad disfrazada

- **Dos ases al sacar 2 cartas:** con reemplazo (1/13)² = **1/169**; sin reemplazo 1/13·3/51 = **1/221**.
- **Lanzas una moneda 1 000 000 de veces. ¿Nº esperado de cadenas "6 caras seguidas de 6 cruces"?** Hay 10⁶ − 11 posiciones; cada una acierta con prob 2^{−12}. Por linealidad de la esperanza (¡no requiere independencia!): (10⁶ − 11)/2¹² ≈ **244.14**.
- **¿El 4.º día hábil del mes es jueves?** Es jueves si el día 1 cae sábado, domingo o lunes → **3/7**.

## Matriz de correlaciones — ¿es posible?

«ρ(A,B)=0.9, ρ(B,C)=0.8, ¿puede ρ(A,C)=0.1?» Una matriz de correlaciones debe ser **semidefinida positiva**. Para [[1,.9,.1],[.9,1,.8],[.1,.8,1]] el determinante es **−0.316 < 0** → no es PSD → **imposible**. Las correlaciones no son libres: están encadenadas por la geometría (desigualdad tipo triangular sobre ángulos).

## Varianza infinita

La **Cauchy**, densidad 1/(π(1+x²)), tiene varianza (y ni siquiera media propia) infinita: ∫x²/(1+x²) diverge. Es el contraejemplo estándar al TLC y a «promediar siempre reduce el ruido».

## Mini-ejemplo trabajado: contar patrones con linealidad

«Lanzas una moneda justa 1 000 000 de veces. ¿Cuántas apariciones esperadas del patrón exacto "6 caras seguidas de 6 cruces" (12 símbolos)?» No intentes modelar dependencias entre posiciones solapadas: define un **indicador** Iₖ = 1 si el patrón empieza en la posición k. Hay 10⁶ − 11 posiciones válidas, y cada una acierta con prob 2⁻¹². Por **linealidad de la esperanza** (que NO exige independencia):

> E[total] = Σ E[Iₖ] = (10⁶ − 11) · 2⁻¹² ≈ **244.14**

**Predicción antes de seguir:** los eventos Iₖ de posiciones vecinas están correlacionados (se solapan). ¿Eso invalida el cálculo de la *esperanza*? Respuesta: **no**. La linealidad de la esperanza es ciega a la dependencia; solo necesitarías la independencia si calcularas la *varianza*. Esa ceguera es justo lo que la hace tan potente.

## Prototipo, contraejemplo y caso borde

- **Prototipo (Bayes con base):** un dato a favor (3 caras) más una tasa base (1/10 trucada) → la respuesta 8/17 vive *entre* prior y verosimilitud, nunca en el extremo.
- **Contraejemplo (correlaciones "libres"):** ρ(A,B)=0.9, ρ(B,C)=0.8 no permiten ρ(A,C)=0.1; la matriz no es semidefinida positiva (det < 0). Tratar las correlaciones como independientes es el error: están encadenadas geométricamente.
- **Caso borde (Cauchy):** sin media ni varianza, promediar no concentra nada; el contraejemplo estándar a "más muestras = menos ruido".

## Errores típicos

- **Conceptual:** dejar que la verosimilitud arrastre toda la decisión e ignorar la tasa base (la moneda trucada es rara: 1/10).
- **Técnico:** exigir independencia para sumar esperanzas de indicadores solapados — no hace falta.
- **De supuestos:** asignar correlaciones a mano sin verificar que la matriz sea PSD, o aplicar el TCL a colas pesadas (Cauchy).

## Transferencia isomorfa

- **Linealidad de la esperanza ↔ conteo de eventos raros en sistemas:** "número esperado de colisiones / de falsos positivos / de patrones" se suma con indicadores sin pelear con la dependencia, igual que estimar carga esperada en un sharding (conecta con [[arena-sd2]]).
- **Bayes (prior×verosimilitud) ↔ VPP:** 8/17 es el mismo motor que el valor predictivo positivo de un test; la rareza frena al dato (conecta con [[arena-q2]]).
- **Matriz de correlación PSD ↔ varianza de portafolio ≥ 0:** que toda combinación aᵀCa sea no negativa es por qué no puedes inventar correlaciones; la misma restricción gobierna el riesgo de una cartera (conecta con [[arena-q6]], Var de sumas con covarianza).
- **Cauchy ↔ TCL que falla:** cola pesada sin segundo momento aparece también como cociente de dos brownianos (conecta con [[arena-q11]]).

Moraleja de la arista: *para contar, suma indicadores (la dependencia no estorba a la esperanza); para creer, mezcla prior y verosimilitud; y recuerda que las correlaciones viven presas dentro de una matriz PSD.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "test/moneda trucada, dato a favor" | Bayes con tasa base; el resultado vive entre prior y verosimilitud |
| "¿mi carta > la tuya?" | divide en empate/no-empate, usa simetría ½ |
| "nº esperado de patrones" | linealidad de la esperanza sobre indicadores |
| "¿es posible esta correlación?" | exige matriz PSD (determinantes ≥ 0) |
| "media/varianza no existe" | piensa en Cauchy (colas pesadas) |

> ❧ **Síntesis:** condicionar bien es enumerar el espacio muestral correcto. Bayes mezcla prior y verosimilitud; la simetría colapsa conteos; la linealidad de la esperanza suma indicadores sin pelear con la independencia; y recuerda que las correlaciones viven dentro de una matriz que debe ser PSD.

---

*Retrieval: cierra la página y responde — (1) P(dos caras | 3 caras) con 1 de 10 trucada; (2) P(mi carta > la tuya); (3) por qué (10⁶−11)/2¹²; (4) criterio PSD para una matriz de correlaciones.*
