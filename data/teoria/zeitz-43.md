# Funciones generatrices

*Lección redactada para CogitoErgoSum a partir de la sección 4.3 de Zeitz (Generating Functions). Cubre el contenido completo de la unidad.*

## Qué es una generatriz

La **función generatriz** de la sucesión a₀, a₁, a₂, … es la serie

f(x) = a₀ + a₁x + a₂x² + a₃x³ + ⋯

**Toda la sucesión, empaquetada en un solo objeto algebraico.** La x no es una variable que «valga algo»: es un gancho del que cuelga la sucesión — el coeficiente de xⁿ ES aₙ. La ganancia: a las funciones se les puede hacer álgebra (multiplicar, derivar, evaluar), y cada manipulación algebraica ejecuta, en bloque, una operación sobre toda la sucesión.

## Los dos hechos que le dan todo su poder

1. **xᵐ · xⁿ = xᵐ⁺ⁿ — multiplicar polinomios SUMA exponentes.** Al multiplicar dos generatrices, el coeficiente de xⁿ en el producto es Σ aₖ·b_{n−k}: todas las maneras de **partir n entre dos elecciones**. Multiplicar generatrices = combinar elecciones independientes cuyos «tamaños» se suman (una convolución). Por eso las generatrices son máquinas de contar: codifican el «Y» del conteo (§6.1) en el producto.
2. **El diccionario local ↔ global.** Conocer los coeficientes (lo local) determina la función (lo global) y viceversa: puedes extraer información de la sucesión estudiando la función como objeto — evaluarla en puntos, descomponerla en fracciones, derivarla.

## La herramienta geométrica (apréndela como reflejo)

> **1/(1 − x) = 1 + x + x² + x³ + ⋯**

Funciona **en ambas direcciones**: ves la serie y la compactas; ves la fracción y la expandes. Variantes de uso diario:

- 1/(1 − cx) = 1 + cx + c²x² + ⋯ (razón c)
- 1/(1 − x²) = 1 + x² + x⁴ + ⋯ (razón x²)

**Ejemplo «en reversa» del banco — desarrollar x/(2 + x):** maniobra hasta la forma 1/(1 − ▯):

x/(2 + x) = (x/2) · 1/(1 + x/2) = (x/2) · 1/(1 − (−x/2)) = (x/2) · Σ (−x/2)ᵏ = Σ (−1)ᵏ xᵏ⁺¹/2ᵏ⁺¹

= x/2 − x²/4 + x³/8 − x⁴/16 + ⋯ — y de ahí lees el coeficiente que quieras.

## (1 + x)ⁿ: evaluar en puntos astutos ES contar

(1 + x)ⁿ = Σ C(n, k)xᵏ — **la generatriz de los coeficientes binomiales** (es el binomio de §6.1 visto como empaque). Ahora evalúa:

- **x = 1:** 2ⁿ = C(n,0) + C(n,1) + ⋯ + C(n,n). La suma de la fila de Pascal, de un golpe.
- **x = −1:** 0 = C(n,0) − C(n,1) + C(n,2) − ⋯ ± C(n,n) (n ≥ 1). La suma alternada es 0 — es decir, hay tantos subconjuntos pares como impares.

Eso es una **técnica general**: las sumas con C(n,k) que parecen difíciles suelen ser una generatriz conocida **evaluada en un punto astuto** (1, −1, 2, raíces de la unidad para sumas cada 3 o cada 4 términos…). También derivar ayuda: derivando (1+x)ⁿ y evaluando en 1 sale Σ k·C(n,k) = n·2ⁿ⁻¹.

## Generatrices y recurrencias

El uso estructural (el que remata §6.4): dada una recurrencia, multiplica ambos lados por xⁿ y suma sobre n — la recurrencia entera se convierte en una **ecuación algebraica para f(x)**. Resuélvela, descompón en fracciones parciales, expande cada pieza con la herramienta geométrica, y los coeficientes te dan la **fórmula cerrada**. Para Fibonacci: f(x) = x/(1 − x − x²) → fracciones parciales con raíces φ y ψ → fórmula de Binet. La generatriz es el camino sistemático hacia las fórmulas que §6.4 solo «verificaba».

## Particiones

Para contar particiones de n (escribirlo como suma de enteros sin importar orden), la generatriz por excelencia: cada parte k se usa 0, 1, 2, … veces, lo que aporta el factor (1 + xᵏ + x²ᵏ + ⋯) = 1/(1 − xᵏ), y la independencia multiplica:

Π 1/(1 − xᵏ) = generatriz de las particiones.

Manipular estos productos demuestra identidades enteras (p. ej., particiones en partes impares = particiones en partes distintas) sin contar nada a mano: pura álgebra de factores.

## No te angusties por la convergencia

En generatrices se trabaja **formalmente**: las series son empaques de coeficientes y las operaciones (suma, producto, composición razonable) están bien definidas coeficiente a coeficiente. Si además la serie converge en algún entorno de 0, evaluar en puntos es legítimo. Para el uso de competencia: manipula con confianza, la teoría respalda.

## Disparadores

- Suma con C(n,k) sospechosamente estructurada (alternada, con pesos k) → generatriz (1+x)ⁿ evaluada/derivada en un punto astuto.
- Recurrencia lineal que quieres en fórmula cerrada → multiplica por xⁿ, suma, despeja f(x), fracciones parciales.
- Conteo de «maneras de formar n» con piezas que se suman (monedas, particiones, dados) → producto de generatrices, una por tipo de pieza.
- 1/(1 − ▯) o serie geométrica a la vista → reflejo en ambas direcciones.

## Síntesis

> **Chunk mínimo:** Generatriz = la sucesión empaquetada: el coeficiente de xⁿ ES aₙ. Su poder: multiplicar suma exponentes ⇒ el producto de generatrices ejecuta el «Y» del conteo (convolución de elecciones independientes). Reflejo geométrico en ambas direcciones: 1/(1−x) = 1 + x + x² + ⋯ (x/(2+x) se desarrolla forzando la forma 1/(1−▯)). (1+x)ⁿ evaluada en puntos astutos cuenta: x=1 da 2ⁿ, x=−1 da suma alternada 0; derivar y evaluar da Σ k·C(n,k) = n·2ⁿ⁻¹. Recurrencia → multiplica por xⁿ y suma → ecuación para f(x) → fracciones parciales → fórmula cerrada (Binet). Particiones: Π 1/(1−xᵏ). Se opera formalmente: sin angustia de convergencia.

---

*Antes del quiz: reconstruye de memoria la definición, los dos hechos del poder, el desarrollo completo de x/(2+x) y el doblete de evaluaciones en x = ±1.*
