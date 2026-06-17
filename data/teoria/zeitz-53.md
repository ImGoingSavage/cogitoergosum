# Sumas y productos: el telescopio

*Lección redactada para CogitoErgoSum a partir de la sección 5.3 de Zeitz (Sums and Products). Cubre el contenido completo de la unidad.*

## Notación Σ y Π

Σ y Π comprimen sumas y productos con un índice. El vocabulario fino que pagará dividendos: una suma con **doble índice 1 ≤ i < j ≤ n** recorre los **pares** — tiene C(n, 2) términos. La identidad puente que hay que tener activa:

(Σ xᵢ)² = Σ xᵢ² + 2·Σ_{i<j} xᵢxⱼ

(el cuadrado de una suma = cuadrados + dobles productos cruzados). Este vocabulario de índices reaparece en Cauchy-Schwarz (§5.5) y en toda la combinatoria.

## Serie aritmética: el pareo de Gauss

Para a + (a+d) + ⋯ + ℓ (n términos), escribe la suma **dos veces, la segunda al revés**, y suma por columnas: **cada columna vale lo mismo** (a + ℓ). Hay n columnas:

2S = n(a + ℓ) → **S = n(a + ℓ)/2** — «promedio por cantidad».

Funciona porque la serie aritmética tiene **simetría aditiva**: término k-ésimo desde el inicio + k-ésimo desde el final es constante. El pareo de Gauss es la herramienta de simetría (§3.1) en versión aditiva.

## Serie geométrica: nace el telescopio

En a + ar + ar² + ⋯ + arⁿ⁻¹ el pareo **fracasa**: no hay simetría aditiva (los términos crecen multiplicativamente; las columnas no son constantes). La jugada que lo reemplaza: compara S con **rS** — son casi idénticas, desplazadas un lugar — y **resta**:

S − rS = a − arⁿ → **S = a(1 − rⁿ)/(1 − r)**

Esa resta donde **casi todo se cancela en cascada** es el **TELESCOPIO** — la herramienta central de la sección.

## Telescopio en fracciones

**El acertijo del banco:** 1/(1·2) + 1/(2·3) + ⋯ + 1/(99·100).

Reescribe cada término como **diferencia de consecutivos**: 1/(k(k+1)) = 1/k − 1/(k+1). La suma colapsa:

(1 − 1/2) + (1/2 − 1/3) + ⋯ + (1/99 − 1/100) = 1 − 1/100 = **99/100**

**Lo difícil no es cancelar: es REESCRIBIR** cada término como diferencia — otra vez «sumar cero creativamente» (§5.2). La descomposición en fracciones parciales es la fábrica estándar de esas diferencias.

**El error clásico (banco):** «1/(k(k+2)) = 1/k − 1/(k+2), y todo se cancela salvo primero y último». **Dos errores:** (1) la descomposición olvidó el factor: 1/(k(k+2)) = **(1/2)**(1/k − 1/(k+2)); (2) con salto 2, el telescopio deja **dos términos vivos en cada punta**: sobreviven 1/1 y 1/2 al inicio, y −1/(n+1), −1/(n+2) al final. Regla general: con diferencia de salto d sobreviven d términos por punta. Siempre **verifica el colapso con n pequeño** antes de confiar.

## El telescopio imperfecto: deducir Σ k²

¿Σ_{k=1}^n k²? No hay u(k) evidente con u(k+1) − u(k) = k². **Wishful thinking sistemático: no necesitas la diferencia exacta — basta una parecida.** Prueba u(k) = k³:

(k+1)³ − k³ = 3k² + 3k + 1

Suma esa identidad para k = 1, …, n. La izquierda **telescopia** a (n+1)³ − 1; la derecha es 3Σk² + 3Σk + n. Con Σk = n(n+1)/2 conocido, **despeja**:

3Σk² = (n+1)³ − 1 − 3n(n+1)/2 − n → **Σk² = n(n+1)(2n+1)/6**

El patrón escala: para Σkᵖ, telescopia con u(k) = kᵖ⁺¹ y despeja usando las sumas de potencias menores. El telescopio imperfecto convierte «no conozco la antiderivada discreta» en «conozco una vecina y ajusto».

## Productos y la serie armónica

- Los **productos telescópicos** funcionan igual con cocientes: Π (k+1)/k = (n+1)/1.
- **La serie armónica diverge:** 1 + 1/2 + 1/3 + ⋯ crece sin tope. El argumento de agrupación (Oresme): 1/3 + 1/4 > 1/2; 1/5 + ⋯ + 1/8 > 1/2; cada bloque de longitud doble aporta más de 1/2 — infinitos medios. Compáralo con Σ1/k²,  que sí converge (sus colas se aplastan por el telescopio de 1/(k(k+1))): la frontera entre crecer y saturar pasa exactamente por aquí.

## Disparadores

- Suma de términos **equiespaciados** → Gauss: promedio × cantidad.
- Razón constante entre términos → compara S con rS y resta.
- Términos de la forma 1/(k(k+algo)), √(k+1) − √k, log((k+1)/k), productos de consecutivos → **telescopio**: reescribe como diferencia de consecutivos (fracciones parciales, racionalizar).
- Σ kᵖ o suma sin antiderivada discreta evidente → telescopio **imperfecto** con la potencia siguiente.
- Cuadrado de una suma vs. suma de cuadrados → identidad de los productos cruzados.

## Síntesis

> **Chunk mínimo:** Aritmética → pareo de Gauss: S = n(a+ℓ)/2, «promedio por cantidad» (funciona por la simetría aditiva k-ésimo + k-ésimo del final = constante). Geométrica → el pareo fracasa: compara S con rS y resta — nace el TELESCOPIO: S = a(1−rⁿ)/(1−r). Fracciones: 1/(k(k+1)) = 1/k − 1/(k+1) ⇒ Σ hasta 99·100 = 1 − 1/100 = 99/100; lo difícil es REESCRIBIR como diferencia (fracciones parciales). Con salto d sobreviven d términos por punta (y no olvides el factor 1/2 en 1/(k(k+2))); verifica el colapso con n pequeño. Telescopio imperfecto: para Σk², suma (k+1)³ − k³ = 3k² + 3k + 1 y despeja → n(n+1)(2n+1)/6. La armónica diverge (bloques de Oresme > 1/2).

---

*Antes del quiz: reconstruye de memoria por qué Gauss funciona en la aritmética y fracasa en la geométrica, el cálculo completo de Σ1/(k(k+1)) hasta 99/100, el telescopio imperfecto de Σk² y los dos errores del salto 2.*

<!-- GRAFO_CONEXO_OLEADA3_START -->
## Puente de transferencia

El telescopio muestra que una suma puede colapsar si eliges la forma correcta. [[arena-p4]] usa esa manipulacion en calculo y finanzas, [[aime-alg]] la entrena como algebra de competencia, y [[zeitz-9]] la lleva a series y convergencia cuando el patron se vuelve infinito.
<!-- GRAFO_CONEXO_OLEADA3_END -->
