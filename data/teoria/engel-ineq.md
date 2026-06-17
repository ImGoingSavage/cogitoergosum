# Engel · Cantera de desigualdades: todo nace de x² ≥ 0

*Lección redactada para CogitoErgoSum a partir del capítulo 7 de «Problem-Solving Strategies» (A. Engel), Inequalities. Cubre la teoría central; el resto del capítulo es cantera para sesiones del camino 1.*

## El origen único

**Toda la teoría elemental de desigualdades nace de x² ≥ 0** (y de su suma: Σxᵢ² ≥ 0). Con x = a − b se despliega el abanico:

- (a − b)² ≥ 0 → **a² + b² ≥ 2ab**
- sumando 2ab a ambos lados → **2(a² + b²) ≥ (a + b)²**
- dividiendo a² + b² ≥ 2ab entre ab > 0 → **a/b + b/a ≥ 2**, y con b = 1/a: **x + 1/x ≥ 2** (x > 0)

## La cadena completa de medias

Para a, b > 0, las **cinco estaciones**, de menor a mayor:

**min(a,b) ≤ HM ≤ GM ≤ AM ≤ QM ≤ max(a,b)**

| Media | Fórmula |
|---|---|
| Armónica (HM) | 2ab/(a + b) = 2/(1/a + 1/b) |
| Geométrica (GM) | √(ab) |
| Aritmética (AM) | (a + b)/2 |
| Cuadrática (QM) | √((a² + b²)/2) |

**Igualdad en cualquier eslabón ⟺ a = b** (y entonces en todos). Cada eslabón se reduce al cuadrado correspondiente: GM ≤ AM es (√a − √b)² ≥ 0; AM ≤ QM es (a − b)² ≥ 0; HM ≤ GM es GM ≤ AM aplicada a 1/a, 1/b.

**Estatus en competencia:** la cadena (y su versión de n variables) **se APLICA sin demostrar** — es vocabulario estándar, como el teorema de Pitágoras. Cítala y úsala.

## Multiplicar desigualdades: divide en pares

Desigualdades **del mismo sentido con lados positivos se multiplican**. El modelo (acertijo del banco):

> **(a + b)(b + c)(c + a) ≥ 8abc** para a, b, c ≥ 0.

*Demostración:* tres AM-GM de dos variables: a + b ≥ 2√(ab), b + c ≥ 2√(bc), c + a ≥ 2√(ca). Todos los lados son no negativos: multiplica las tres → (a+b)(b+c)(c+a) ≥ 8·√(a²b²c²) = 8abc. ∎ (Igualdad ⟺ a = b = c.)

**La jugada general:** divide la desigualdad grande en **pares que ya sabes manejar** y multiplica (o suma) las piezas.

## Cuatro demostraciones-modelo de a² + b² + c² ≥ ab + bc + ca

Conocer las CUATRO es conocer los cuatro estilos del oficio:

1. **Suma de cuadrados:** multiplica por 2 y reagrupa: 2(a²+b²+c²) − 2(ab+bc+ca) = **(a−b)² + (b−c)² + (c−a)² ≥ 0**. *Estilo: reducir a cuadrados — el origen único.*
2. **Sumar desigualdades básicas:** a²+b² ≥ 2ab, b²+c² ≥ 2bc, c²+a² ≥ 2ca; suma las tres y divide entre 2. *Estilo: despiece en pares.*
3. **Ordenar:** WLOG a ≥ b ≥ c (la desigualdad es simétrica — §3.1 autoriza); entonces a²+b²+c² − ab−bc−ca = **(a−c)(a−b) + (b−c)² ≥ 0**, ambos sumandos no negativos por el orden. *Estilo: usar el orden como hipótesis gratis (rearrangement en miniatura).*
4. **Normalizar:** la desigualdad es **homogénea de grado 2** (escalar a,b,c por t escala todo por t²) — puedes imponer una normalización gratuita (p. ej. a+b+c = 1) y reducir variables/grados de libertad antes de calcular. *Estilo: explotar la homogeneidad.*

## Nesbitt y la forma producto

> **Nesbitt:** para a, b, c > 0: a/(b+c) + b/(a+c) + c/(a+b) ≥ 3/2.

**La jugada estructural:** suma **3** al lado izquierdo (1 a cada fracción): cada término se vuelve (a+b+c)/(b+c) — ¡numeradores simetrizados! Con s = a+b+c:

Nesbitt + 3 = s·(1/(b+c) + 1/(a+c) + 1/(a+b)) ≥ 9/2

y como s = ((b+c) + (a+c) + (a+b))/2, esto es exactamente la **forma producto** con u = b+c, v = a+c, w = a+b:

> **(u + v + w)(1/u + 1/v + 1/w) ≥ 9**

*Demostración por conteo de términos (banco):* expande — salen n = 3 unos (los uᵢ/uᵢ) más los C(3,2) = 3 **pares** uᵢ/uⱼ + uⱼ/uᵢ, cada par ≥ 2. Total ≥ 3 + 3·2 = 9 ✓. La **generalización**:

**(a₁ + ⋯ + aₙ)(1/a₁ + ⋯ + 1/aₙ) ≥ n²** — n unos + C(n,2) pares ≥ n + 2·C(n,2) = n + n(n−1) = n².

(Es también AM-HM, o Cauchy-Schwarz con aᵢ = √uᵢ, bᵢ = 1/√uᵢ.) Restando el 3: Nesbitt ≥ 9/2 − 3 = 3/2 ∎.

## Reducir el espacio ANTES de calcular

Las dos jugadas estructurales que deben dispararse ante cualquier desigualdad **antes** del álgebra:

1. **¿Es simétrica?** → ordena WLOG a ≥ b ≥ c. Un mar de configuraciones se vuelve una.
2. **¿Es homogénea** (f(ta, tb, tc) = t^d·f(a, b, c))? → **normaliza gratis**: impón a+b+c = 1, o abc = 1, o max = 1 — la que más limpie. Una variable menos, denominadores domados.

Ambas son las tácticas de simetría (§3.1) y de «forma simple primero» (§7.4) vestidas de desigualdad.

## Disparadores

- Cualquier desigualdad de dos variables → ¿qué cuadrado (a−b)² la genera?
- Producto de sumas vs. producto de términos → multiplicar AM-GM por pares.
- Fracciones con denominadores b+c, a+c, a+b → suma 1 a cada una (Nesbitt) y busca la forma producto ≥ n².
- Simétrica → WLOG ordena. Homogénea → normaliza. SIEMPRE antes de calcular.
- Σuᵢ por Σ1/uᵢ → n² por conteo de pares.

## Síntesis

> **Chunk mínimo:** Todo nace de x² ≥ 0: con x = a−b salen a²+b² ≥ 2ab, x + 1/x ≥ 2 y la cadena min ≤ HM (2ab/(a+b)) ≤ GM (√ab) ≤ AM ((a+b)/2) ≤ QM ≤ max, igualdad ⟺ a = b; en competencia se cita sin demostrar. Desigualdades del mismo sentido con lados positivos se multiplican: tres AM-GM por pares dan (a+b)(b+c)(c+a) ≥ 8abc. Cuatro estilos para a²+b²+c² ≥ ab+bc+ca: suma de cuadrados, despiece en pares, WLOG ordenar, normalizar por homogeneidad. Nesbitt ≥ 3/2: suma 1 a cada fracción → forma producto (Σuᵢ)(Σ1/uᵢ) ≥ n² (n unos + C(n,2) pares ≥ 2). Antes de calcular: ¿simétrica? ordena; ¿homogénea? normaliza.

---

*Antes del quiz: reconstruye de memoria la cadena de cinco estaciones con fórmulas e igualdad, la prueba de (a+b)(b+c)(c+a) ≥ 8abc, los cuatro estilos para a²+b²+c² ≥ ab+bc+ca y el cierre de Nesbitt vía la forma producto.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

La cantera de desigualdades de Engel es la version intensiva de [[zeitz-55]]. Sus tecnicas se apoyan en la intuicion de optimizacion de [[arena-p4]] y reaparecen en [[arena-q5]] cuando una cota, una derivada o una convexidad decide que extremo financiero es posible.
<!-- GRAFO_CONEXO_OLEADA3_END -->
