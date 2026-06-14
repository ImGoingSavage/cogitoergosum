# Análisis exploratorio: estimadores robustos de centro y dispersión

## La estadística empieza por mirar los datos

Antes de modelar, el científico de datos **explora** (EDA, en la tradición de Tukey): resume el centro, la dispersión y la forma de cada variable. La elección del resumen no es trivial — depende de cuán sensible quieras ser a los **outliers**.

## Estimadores de localización (centro)

- **Media:** suma/n. Usa todas las observaciones → **sensible a outliers** (Bill Gates muda el promedio de un pueblo).
- **Media recortada (trimmed mean):** descarta un % de valores en cada extremo y promedia el resto. Compromiso entre media y mediana; muy usada (p.ej. en clavados se descartan la nota más alta y la más baja).
- **Mediana:** el valor central de la lista ordenada. **Robusta:** no la afecta cuán extremo sea un outlier, solo cuántos hay.
- **Media/mediana ponderada:** cada dato pesa distinto (p.ej. tasas por población).

> **Robusto** = no se deja arrastrar por valores extremos. La mediana y la media recortada lo son; la media no.

## Estimadores de variabilidad (dispersión)

Las **desviaciones** (también: errores, residuales) son las diferencias entre cada dato y el centro. Como su suma respecto a la media es **cero**, se resumen de otras formas:

| Métrica | Definición | Robusta a outliers |
|---------|-----------|--------------------|
| **Varianza** | media de las desviaciones **al cuadrado** (denominador n−1) | No (muy sensible) |
| **Desviación estándar** | √varianza; en la **misma escala** que los datos | No |
| **MAD (desv. absoluta media)** | media de los valores absolutos de las desviaciones | No |
| **MAD mediana** (mediana de \|x−mediana\|) | mediana de las desviaciones absolutas a la mediana | **Sí** |
| **Rango** | máximo − mínimo | No (extremo) |
| **IQR** (rango intercuartílico) | percentil 75 − percentil 25 | **Sí** |

La **desviación estándar** se prefiere en teoría estadística porque trabajar con cuadrados es matemáticamente conveniente, no porque sea más robusta (de hecho: sd > MAD > MAD-mediana).

### ¿Por qué n−1? Grados de libertad
Dividir entre n **subestima** la varianza poblacional (estimador sesgado); dividir entre **n−1** la vuelve insesgada. La razón: hay n−1 grados de libertad porque la sd depende de haber calculado ya la media (una restricción). En la práctica, con n grande, n vs n−1 casi no cambia nada.

## Estimadores basados en percentiles

El **percentil P** (≡ cuantil) es el valor tal que P% de los datos caen por debajo. La **mediana = percentil 50**. El **IQR = P75 − P25** mide dispersión ignorando las colas, por eso es robusto. El **boxplot** visualiza mediana, cuartiles y outliers (puntos a más de 1.5×IQR de la caja).

## Correlación

El **coeficiente de correlación** (Pearson) mide la asociación **lineal** entre dos variables numéricas, en [−1, 1]: es la covarianza normalizada por las desviaciones estándar, así que es adimensional y comparable. Cuidado: solo capta relación lineal y es sensible a outliers.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Hay outliers extremos y quiero el centro" | Mediana o media recortada, no la media |
| "Quiero dispersión resistente a outliers" | IQR o MAD-mediana, no la desviación estándar |
| "¿Por qué n−1 y no n?" | Estimador insesgado; grados de libertad (una restricción: la media) |
| "Resumir la forma y detectar outliers" | Boxplot (percentiles 25/50/75 + 1.5×IQR) |
| "Asociación entre dos numéricas" | Correlación de Pearson (solo lineal, ojo con outliers) |
| "Las notas más alta y baja distorsionan" | Media recortada |

---

> **Síntesis:** El análisis exploratorio resume cada variable por su centro y su dispersión, y la clave es la **robustez a outliers**. Para el centro: la media usa todo pero se deja arrastrar; la mediana y la media recortada resisten. Para la dispersión: la varianza/desviación estándar (basadas en cuadrados, denominador n−1 por los grados de libertad) son sensibles, mientras el IQR y la MAD-mediana resisten. Los percentiles y el boxplot describen la forma y delatan outliers; la correlación de Pearson mide asociación lineal.

---

*Retrieval: cierra y responde: (1) ¿qué significa que la mediana sea un estimador robusto?; (2) ordena sd, MAD y MAD-mediana por magnitud y di cuál es robusta; (3) ¿por qué se divide entre n−1 en la varianza?; (4) ¿qué es el IQR y por qué resiste outliers?*
