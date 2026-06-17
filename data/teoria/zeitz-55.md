# Desigualdades: AM-GM, massage y Cauchy-Schwarz

*Lección redactada para CogitoErgoSum a partir de la sección 5.5 de Zeitz (Inequalities). Cubre el contenido completo de la unidad.*

## Las igualdades son raras; la matemática real estima

La mayor parte del análisis serio no calcula valores exactos: **acota**. Dominar desigualdades es dominar el arte de comparar sin calcular.

## La técnica del «?»

Para decidir cuál de dos expresiones es mayor: escribe la comparación **alegada con un signo de interrogación encima** y opera **manteniendo equivalencia** (pasos reversibles) hasta llegar a algo obviamente cierto o falso — típicamente un cuadrado: (x − y)² ≥ 0.

**Ejemplo del banco — ¿√19 + √99 vs. √20 + √98?** Plantea √19 + √99 ?≷ √20 + √98 y eleva al cuadrado (legítimo: ambos lados positivos):

118 + 2√(19·99) ? 118 + 2√(20·98) → 19·99 = 1881 ? 1960 = 20·98

1881 < 1960 → **√19 + √99 < √20 + √98**. (Estructura de fondo: con suma fija de radicandos —118—, gana el par más parejo, sabor AM-GM.)

**Las operaciones peligrosas:** multiplicar por negativos invierte; y **tomar recíprocos INVIERTE el sentido** cuando ambos lados tienen el mismo signo (2 < 3 pero 1/2 > 1/3). Si en el camino tomas recíprocos, voltea el «?».

## La jerarquía de crecimiento

De menor a mayor para x grande: **logaritmos < potencias < exponenciales**. «Domina» significa: **para todo x suficientemente grande** — no desde el principio. 0.001x² **termina** ganándole a 100000x (a partir de x = 10⁸), y 1.001ˣ termina aplastando a x¹⁰⁰⁰. Dibuja las gráficas hasta interiorizar que las constantes solo retrasan lo inevitable.

## AM-GM

> Para x, y ≥ 0:  **(x + y)/2 ≥ √(xy)**, con igualdad **solo si x = y**.

*Demostración:* baja por equivalencias hasta el cuadrado: (x+y)/2 ≥ √(xy) ⟺ x + y ≥ 2√(xy) ⟺ x − 2√(xy) + y ≥ 0 ⟺ **(√x − √y)² ≥ 0** ✓.

*Lectura geométrica:* de todos los rectángulos con **perímetro fijo**, el **cuadrado maximiza el área** (y con área fija, el cuadrado minimiza el perímetro). AM-GM es la formalización de «lo parejo optimiza».

*Versión n:* (x₁ + ⋯ + xₙ)/n ≥ (x₁⋯xₙ)^(1/n), igualdad ⟺ todos iguales.

### El protocolo de optimización: adivina la igualdad PRIMERO

Para «máximo del producto con suma fija» (o mínimo de suma con producto fijo), **antes de calcular nada**: adivina el caso de igualdad — casi siempre el **punto simétrico** (todas las variables iguales). Ese candidato te dice **cómo partir los términos** para que AM-GM cierre exacto. El test de calidad: si tu aplicación de AM-GM **no alcanza la igualdad en tu candidato**, la partición está mal elegida — la cota saldrá floja y no será el óptimo. (Ejemplo: minimizar x + 2/x para x > 0 — la igualdad x = 2/x da x = √2; AM-GM directo sobre {x, 2/x} cierra: x + 2/x ≥ 2√2 ✓ con igualdad ahí.)

## Massage: afloja término a término

Cuando solo necesitas una **estimación**, está permitido (y mandado) reemplazar cada término por algo un poco mayor o menor que **sí se pueda sumar** — masajear la suma.

**El ejemplo 5.5.19, completo:** calcular ⌊Σ_{n=1}^{10000} 1/√n⌋ sin calculadora. Racionalizando:

2(√(n+1) − √n) = 2/(√(n+1) + √n) **< 1/√n <** 2/(√n + √(n−1)) = 2(√n − √(n−1))

Suma las tres partes de n = 1 a 10000 — **ambos lados telescopian** (§5.3):

- Cota inferior: 2(√10001 − 1) > 198.00…
- Cota superior: 2√10000 = 200… demasiado floja porque el primer término (n = 1: cota 2(√1 − 0) = 2 contra valor real 1) **desperdicia un punto entero**. **Afina el encaje burdo:** usa el valor exacto 1 para n = 1 y la cota solo desde n = 2: Σ < 1 + 2(√10000 − 1) = 199.

Entonces 198 < Σ < 199 → **⌊Σ⌋ = 198**. La moraleja doble: telescopio como máquina de cotas, y *afinar los primeros términos* cuando el massage es demasiado generoso.

## Cauchy-Schwarz

> **(Σ aᵢbᵢ)² ≤ (Σ aᵢ²)(Σ bᵢ²)**, igualdad ⟺ las sucesiones son proporcionales.

*De dónde nace:* de «una suma de cuadrados es ≥ 0» aplicada con astucia: (Σaᵢ²)(Σbᵢ²) − (Σaᵢbᵢ)² = Σ_{i<j} (aᵢbⱼ − aⱼbᵢ)² ≥ 0 (identidad de Lagrange — nota los índices i < j de §5.3).

*Señales:* **productos cruzados** Σaᵢbᵢ que quieres separar; o un **cuadrado de una suma** contra **sumas de cuadrados**. Truco frecuente: escribir 1·xᵢ para usar (Σxᵢ)² ≤ n·Σxᵢ².

## El mini-acertijo de las fracciones

**¿1998/1999 vs. 1999/2000?** Dos caminos de la sección: (1) **multiplica en cruz** (denominadores positivos, sentido se conserva): 1998·2000 = 1999² − 1 < 1999² → la primera es menor. (2) **Complementos:** 1998/1999 = 1 − 1/1999 y 1999/2000 = 1 − 1/2000; como 1/1999 > 1/2000 (¡recíprocos invierten!), la primera resta más → **1998/1999 < 1999/2000**.

## Disparadores

- ¿Cuál es mayor? → técnica del «?» con pasos reversibles (ojo con recíprocos).
- Producto con suma fija / suma con producto fijo → AM-GM, adivinando ANTES el punto de igualdad.
- Estimar una suma sin fórmula → massage con cotas telescópicas; afina las puntas.
- Productos cruzados o (Σ)² vs. Σ()² → Cauchy-Schwarz.
- ¿Quién domina para n grande? → jerarquía log < potencia < exponencial.

## Síntesis

> **Chunk mínimo:** Técnica del «?»: opera con pasos REVERSIBLES hasta algo obvio (un cuadrado ≥ 0); recíprocos y negativos INVIERTEN el sentido. Jerarquía para x grande: log < potencia < exponencial («termina ganando»; las constantes solo retrasan). AM-GM: (x+y)/2 ≥ √(xy), igualdad ⟺ iguales (prueba: (√x−√y)² ≥ 0; geometría: el cuadrado optimiza); protocolo: adivina el punto de igualdad ANTES y parte los términos para que cierre exacto ahí. Massage: reemplaza término a término por cotas sumables — 2(√(n+1)−√n) < 1/√n < 2(√n−√(n−1)) telescopia y, afinando n = 1, da ⌊Σ⌋ = 198. Cauchy-Schwarz: (Σaᵢbᵢ)² ≤ (Σaᵢ²)(Σbᵢ²), igualdad ⟺ proporcionales; señal: productos cruzados o (Σ)² vs Σ()².

---

*Antes del quiz: reconstruye de memoria la comparación √19+√99 vs √20+√98, AM-GM con su cuadrado y su geometría, el massage completo de la suma de 1/√n y la señal de Cauchy-Schwarz.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

Las desigualdades son control de forma: AM-GM, Cauchy y massage dicen que expresiones pueden dominar a otras. [[engel-ineq]] profundiza tecnicas de competencia, [[arena-p4]] las conecta con optimizacion y calculo, y [[arena-q5]] las usa cuando derivadas y convexidad explican mercados y riesgo.
<!-- GRAFO_CONEXO_OLEADA3_END -->
