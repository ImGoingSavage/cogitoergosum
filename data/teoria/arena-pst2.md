# Distribuciones muestrales y el bootstrap

## Dos distribuciones que no hay que confundir

- **Distribución de los datos:** cómo se reparten las observaciones individuales.
- **Distribución muestral de un estadístico:** cómo se repartiría un **estadístico** (la media, la mediana…) si tomaras muchas muestras distintas. Es más estrecha y más normal que la de los datos.

## Error estándar vs desviación estándar

- **Desviación estándar:** variabilidad de los **datos individuales**.
- **Error estándar (SE):** variabilidad del **estadístico muestral**. Resume en un número la anchura de la distribución muestral.

Fórmula clásica: SE = s/√n. La **raíz de n** implica que para **reducir el SE a la mitad hay que cuadruplicar n** (rendimientos decrecientes de recolectar más datos).

## Teorema Central del Límite (visión práctica)

La distribución muestral de la media tiende a la **normal** al crecer n, sin importar la distribución de los datos. El CLT es el motor de las fórmulas clásicas (t de Student, intervalos, tests). Pero el libro advierte: en ciencia de datos los tests formales pesan poco y **el bootstrap está siempre disponible**, así que no es indispensable apoyarse en el CLT.

## El bootstrap: remuestreo con reemplazo

Para estimar la distribución muestral de **cualquier** estadístico sin supuestos de normalidad: remuestrea **con reemplazo** de la propia muestra y recalcula el estadístico muchas veces.

**Algoritmo (para la media de una muestra de tamaño n):**
1. Saca un valor, regístralo y **devuélvelo** (reemplazo).
2. Repite n veces → un *bootstrap sample*.
3. Registra la media de esos n valores.
4. Repite los pasos 1–3 **R** veces.
5. Con los R resultados: calcula su desviación estándar (≈ **error estándar**), grafica un histograma/boxplot y construye un **intervalo de confianza**.

Conceptualmente, es como replicar la muestra infinitas veces para formar una "población hipotética" y muestrear de ahí. Sirve para estadísticos donde no hay fórmula matemática conocida, y para datos multivariados (se remuestrean **filas completas**).

> **Advertencia clave:** el bootstrap **no** crea datos nuevos ni compensa una muestra pequeña; solo informa cómo se comportarían muchas muestras tomadas de una población *parecida* a la tuya.

**Bootstrap vs resampling:** "resampling" abarca tanto el bootstrap (con reemplazo) como los **tests de permutación** (barajar, normalmente sin reemplazo). "Bootstrap" siempre implica **con reemplazo**. El bootstrap aplicado a árboles y promediado = **bagging**.

## Intervalo de confianza

Un IC del 90%/95% es el rango central de la distribución muestral (bootstrap) que contiene ese % de los valores. Para el data scientist es una **herramienta para ver cuán variable es un resultado**, más que un ritual de inferencia formal. Interpretación correcta: es la cobertura del *procedimiento* a largo plazo, no la probabilidad de que el parámetro fijo caiga en este intervalo concreto.

## Sesgos de muestreo a vigilar

- **Sesgo de selección:** elegir datos (consciente o no) de forma no representativa; incluye el **self-selection bias** (quienes opinan se eligen a sí mismos) y el "vast search effect" (buscar tanto que algo aparece por azar).
- **Regresión a la media:** tras un valor extremo, el siguiente tiende a estar más cerca del promedio (no es el método de regresión). Confundirla con un efecto real es una forma de sesgo de selección (el "maleficio del novato").

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "¿Cuán variable es mi media/mediana/coeficiente?" | Bootstrap: remuestrea con reemplazo R veces |
| "No hay fórmula para el SE de este estadístico" | Bootstrap (no necesita supuestos) |
| "Quiero un IC sin asumir normalidad" | IC por percentiles del bootstrap |
| "Datos multivariados / estabilidad de un modelo" | Bootstrap por filas; bagging para árboles |
| "Reducir el error estándar a la mitad" | Cuadruplica n (SE ∝ 1/√n) |
| "Comparar SE entre datos y estadístico" | SD = datos; SE = estadístico, no confundir |
| "Una estrella tuvo un mal segundo año" | Regresión a la media, no necesariamente declive real |

---

> **Síntesis:** La distribución muestral describe cómo varía un estadístico de muestra a muestra; su anchura se resume en el **error estándar** (SE ∝ 1/√n, no confundir con la desviación estándar de los datos). El CLT la vuelve normal al crecer n, pero el **bootstrap** —remuestrear con reemplazo y recalcular R veces— estima esa variabilidad para *cualquier* estadístico sin supuestos, y de él salen el error estándar y los intervalos de confianza. El bootstrap no inventa datos; y hay que vigilar el sesgo de selección y la regresión a la media.

---

*Retrieval: cierra y responde: (1) diferencia error estándar de desviación estándar; (2) escribe los pasos del bootstrap para la media; (3) ¿qué NO hace el bootstrap?; (4) ¿qué es la regresión a la media y por qué engaña?*
