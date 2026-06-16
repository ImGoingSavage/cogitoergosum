# Feature engineering y preparación de datos

## De qué trata esta lección (y qué sabrás hacer al final)

Antes de que un modelo aprenda algo, alguien tuvo que convertir datos crudos —fechas, texto, campos con huecos, números en escalas dispares— en **features** que el modelo pueda explotar. Ese trabajo, el *feature engineering*, decide más del resultado que la elección del algoritmo: un modelo simple con buenas features gana a uno complejo con features pobres. Esta lección construye, desde cero, las decisiones que más se evalúan en entrevista: cómo evitar el **data leakage** (el error que infla tus métricas y te traiciona en producción), cómo tratar datos faltantes según *por qué* faltan, cómo escalar, y cómo transformar distribuciones y categóricas.

Al terminar podrás: (1) explicar por qué ajustar transformaciones sobre todo el dataset es trampa y cómo evitarla; (2) elegir el manejo de NaN según el mecanismo de missingness (MCAR/MAR/MNAR); (3) decidir entre min-max y z-score; y (4) saber cuándo una transformación logarítmica o un one-hot encoding es la jugada. Cada idea entra primero como intuición y problema concreto, no como receta.

---

## Qué es feature engineering (y por qué decide el resultado)

**Feature engineering** es tomar datos crudos y **construir representaciones que capturen los patrones** que el modelo necesita ver. Una fecha cruda no le dice nada a un modelo; "día de la semana" o "días desde el último login" sí. Es donde el conocimiento del dominio y la creatividad del científico de datos amplifican —o hunden— el poder predictivo. La moraleja que conviene grabar: **más vale un modelo simple con buenas features que uno complejo con features pobres.** El algoritmo no inventa información que las features no contienen.

## La trampa #1: data leakage (fuga de información)

Esta es la que más entrevistas decide, así que va primero. **Data leakage** ocurre cuando información que el modelo **no debería conocer al predecir** se cuela durante el entrenamiento, dándole un "vistazo" al futuro o al conjunto de evaluación. El síntoma es traicionero: el rendimiento offline sale **demasiado optimista** y luego se **desploma en producción**, donde esa información ya no está disponible.

El error clásico del novato: aplicar transformaciones que **aprenden parámetros** (escalado, imputación) **sobre todo el dataset antes de separar train/test**. Si la media o el mínimo se calculan usando también las filas de test, el modelo ya "vio" información del conjunto con el que lo vas a evaluar → fuga.

**Regla de oro (memorízala):** **separa primero**, **ajusta la transformación SOLO con train** (`fit_transform` en train), y luego **aplícala** al test sin re-ajustar (`transform`). El test debe comportarse como un futuro que tu pipeline nunca tocó. Encapsúlalo todo en un *pipeline* reproducible para que el orden sea imposible de equivocar.

## Datos faltantes: identifica el mecanismo, luego actúa

El error aquí es tratar todo NaN igual. **Por qué** falta un dato decide la jugada correcta; hay tres mecanismos de "missingness":

| Mecanismo | Significa | Manejo típico |
|-----------|-----------|---------------|
| **MCAR** (completamente al azar) | el faltante no depende de nada | borrar filas (`dropna`) si son pocas |
| **MAR** (al azar condicional) | depende de variables **observadas** | imputación condicional (moda/media por grupo) |
| **MNAR** (no al azar) | depende del **valor mismo** no observado | imputar con info disponible; modelar el faltante |

La distinción clave es MCAR vs MNAR. Si los datos faltan **al azar** (MCAR), borrarlos solo te cuesta tamaño de muestra. Pero si faltan **por su propio valor** (MNAR: los de ingreso alto no declaran ingreso), borrarlos o imputar la media **sesga** la muestra — estás borrando sistemáticamente a un tipo de unidad. Imputar mal introduce sesgo; siempre considera el efecto de la imputación sobre el análisis final.

## Escalado: poner las features en rangos comparables

Algunos algoritmos miran **distancias** (k-means, kNN, clustering jerárquico) o varianzas (PCA), y ahí la **magnitud** importa: una feature medida en miles (ingreso) aplastará a otra en decenas (edad), no porque sea más informativa sino porque sus números son más grandes. Escalar iguala su influencia. Dos formas:

- **Min-max** → lleva al rango fijo $[0,1]$:
  $$X' = \frac{X - X_{\min}}{X_{\max}-X_{\min}}.$$
  El valor mínimo va a 0, el máximo a 1, el resto se interpola. Útil cuando quieres un rango acotado; pero es **sensible a outliers**: un solo valor extremo fija el máximo y aplasta todo lo demás cerca de 0.
- **Z-score (estandarización)** → media 0, desviación 1:
  $$X' = \frac{X-\mu}{\sigma}.$$
  Resta la media $\mu$ y divide por la desviación $\sigma$, así que mide "a cuántas desviaciones del promedio está cada valor". Es **más robusto a outliers** que min-max y se prefiere cuando hay valores extremos legítimos.

Si dudas, prueba ambos y compara el rendimiento del modelo — no hay una respuesta universal.

> **Predicción antes de seguir:** una columna de ingresos tiene un valor de 50 millones (un multimillonario) entre miles de salarios normales. Si la escalas con **min-max**, ¿dónde quedan los salarios normales? Respuesta: **aplastados cerca de 0**, porque ese único extremo define el máximo (=1) y comprime todo el rango útil. Esa es justo la señal para preferir **z-score**: tolera el outlier sin destruir la resolución del resto.

## Transformaciones de distribución

A veces el problema no es la escala sino la **forma** de la distribución. Muchos modelos suponen datos aproximadamente simétricos, y variables como ventas o ingresos están **sesgadas a la derecha** (una cola larga de valores enormes). La **transformación logarítmica** comprime esa cola y vuelve los datos más simétricos: el log convierte multiplicativo en aditivo, así que un salto de 100 a 1000 pesa lo mismo que de 1000 a 10000. Otras opciones: Box-Cox, potencia, exponencial. Cuidado: si transformas la **variable respuesta**, debes **revertir** la predicción a su escala original antes de reportarla.

## Codificar categóricas y reducir dimensión

- **One-hot encoding:** convierte una categórica de texto en una columna binaria por categoría (rojo/verde/azul → tres columnas 0/1). Se usa cuando **no hay orden** entre categorías; codificarlas como 1,2,3 le inventaría al modelo un orden falso (azul > verde) que no existe.
- **Selección de features:** quedarte solo con las informativas reduce ruido y overfitting (menos features espurias que el modelo pueda sobre-ajustar).
- **Reducción de dimensión (PCA):** comprime muchas features correlacionadas en pocos **componentes** que conservan la mayor varianza. Recuerda: PCA mira varianzas, así que **exige escalar antes** (mismo motivo que k-means).

---

## Mini-ejemplo trabajado: cómo el escalado filtra el futuro

Tienes 1000 filas; quieres estandarizar (z-score) y luego evaluar. El novato hace `fit_transform` sobre las **1000** y después separa 800 train / 200 test. Problema: la media y la σ usadas para escalar el train se calcularon **incluyendo las 200 de test** — el modelo ya "vio" información del conjunto de evaluación. El AUC offline sale inflado y se desploma en producción.

Lo correcto: **separa primero**, calcula media/σ **solo con las 800 de train** (`fit`), y aplica esa misma transformación al test (`transform`, sin recalcular). El test debe ser un futuro que el pipeline nunca tocó.

**Predicción antes de seguir:** ¿el leakage hace que el modelo sea peor o que tu *estimación* del modelo sea peor? Respuesta: hace que tu **estimación** sea engañosamente optimista — el modelo no es mejor, solo *parece* mejor porque lo evaluaste con datos que ya influyeron en su preparación. El daño no es al modelo, es a tu capacidad de confiar en la métrica. Por eso el leakage es tan peligroso: no avisa hasta producción.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** cualquier transformación que aprende parámetros (escalado, imputación, encoding por frecuencia) → ajusta solo con train, aplica a test.
- **Contraejemplo (MNAR ≠ MCAR):** borrar filas con NaN es válido si son MCAR (faltan al azar), pero si el faltante depende del valor no observado (MNAR: los ricos no declaran ingreso), borrar sesga la muestra. No todo NaN se trata igual.
- **Caso borde (min-max y un outlier):** un solo valor extremo fija el máximo y aplasta todo lo demás a ~0; el borde motiva z-score cuando hay outliers legítimos.

## Errores típicos

- **Conceptual:** imputar/escalar antes de separar train/test (leakage).
- **Técnico:** re-ajustar la transformación sobre el test (`fit_transform` en test) en vez de solo `transform`.
- **De supuestos:** imputar la media global ignorando el mecanismo de missingness, introduciendo sesgo.

## Transferencia isomorfa

- **Data leakage ↔ ajustar por un collider / mirar el futuro:** colar información posterior al outcome infla el desempeño igual que condicionar en un collider infla una asociación espuria (conecta con [[arena-h17]] y [[arena-dmls1]]).
- **Fit-en-train, transform-en-test ↔ training-serving skew:** la misma feature debe calcularse igual en train y en serving; discrepancias rompen el modelo en producción (conecta con [[arena-s1]]).
- **Escalado antes de KNN/PCA ↔ sensibilidad a la distancia:** algoritmos de distancia exigen features comparables, como exige PCA estandarizar antes (conecta con [[arena-isl4]] y [[arena-cds2]]).
- **MNAR ↔ sesgo de selección:** que el dato falte por su propio valor es el mismo fenómeno que filtrar la muestra por una variable informativa.

Moraleja de la arista: *el leakage no daña al modelo, daña tu confianza en la métrica; separa primero, ajusta solo con train, y calcula la feature igual offline y online.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Escalé/imputé y el test salió buenísimo" | Sospecha **leakage**: ¿ajustaste sobre todo el dataset? |
| "Hay NaN en el dataset" | Identifica MCAR/MAR/MNAR antes de imputar |
| "kNN/k-means/PCA da raro" | Escala las features (min-max o z-score) |
| "Una feature en miles domina" | Z-score para igualar influencia |
| "Distribución con cola larga a la derecha" | Transformación logarítmica |
| "Variable categórica de texto" | One-hot encoding |
| "Outliers fuertes y necesito escalar" | Z-score (min-max se deja influir) |

---

> **Síntesis:** El feature engineering convierte datos crudos en representaciones que el modelo puede explotar. La regla que todo lo gobierna: **ajustar transformaciones solo con train y aplicarlas a test** para evitar data leakage. Antes de imputar faltantes, identifica el mecanismo (MCAR/MAR/MNAR); antes de usar algoritmos de distancia, escala (min-max para rango acotado, z-score cuando hay outliers); y transforma distribuciones sesgadas (log) para cumplir supuestos.

---

*Retrieval: cierra y responde: (1) ¿qué es data leakage y cuál es la regla para evitarlo?; (2) diferencia MCAR vs MNAR y cómo tratar cada uno; (3) ¿cuándo prefieres z-score sobre min-max?; (4) ¿para qué sirve una transformación logarítmica?*
