# Feature engineering y preparación de datos

## Qué es feature engineering

Tomar datos crudos y **construir representaciones que capturen los patrones** que el modelo necesita. Es donde el dominio y la creatividad del científico de datos amplifican (o hunden) el poder predictivo. Más vale un modelo simple con buenas features que uno complejo con features pobres.

## La trampa #1: data leakage (fuga de información)

**Data leakage** = información ajena al set de entrenamiento se cuela durante la construcción del modelo, dándole un "vistazo" a lo que no debería conocer. Resultado: rendimiento estimado **demasiado optimista** que se desploma en producción.

El error clásico del novato: aplicar transformaciones (escalado, imputación) **sobre todo el dataset antes de separar train/test**. La media o el mínimo se calculan usando datos de test → fuga.

**Regla de oro:** divide primero, **ajusta la transformación SOLO con train** (`fit_transform` en train), y luego **aplícala** al test (`transform`, sin re-ajustar). Encapsula todo en un *pipeline* reproducible.

## Datos faltantes: identifica el mecanismo, luego actúa

No todo faltante se trata igual. El mecanismo de "missingness" decide la jugada:

| Mecanismo | Significa | Manejo típico |
|-----------|-----------|---------------|
| **MCAR** (completamente al azar) | el faltante no depende de nada | borrar filas (`dropna`) si son pocas |
| **MAR** (al azar condicional) | depende de variables **observadas** | imputación condicional (moda/media por grupo) |
| **MNAR** (no al azar) | depende del **valor mismo** no observado | imputar con info disponible; modelar el faltante |

Imputar mal introduce sesgo. Siempre considera el impacto de la imputación sobre el análisis final.

## Escalado: poner las features en rangos comparables

Algoritmos basados en distancia (k-means, kNN, jerárquico) y PCA son **sensibles a la magnitud**: una feature en miles domina a otra en decenas. Escalar iguala su influencia.

- **Min-max** → rango fijo $[0,1]$: $X' = \dfrac{X - X_{min}}{X_{max}-X_{min}}$. Útil cuando quieres un rango acotado; **sensible a outliers** (un extremo aplasta el resto).
- **Z-score (estandarización)** → media 0, desv. 1: $X' = \dfrac{X-\mu}{\sigma}$. **Más robusto a outliers**; preferido cuando hay valores extremos legítimos.

Si dudas, prueba ambos y compara el rendimiento del modelo.

## Transformaciones de distribución

Cambian la **forma** (sesgo) de los datos para cumplir los supuestos de un modelo. La **transformación logarítmica** comprime colas largas de datos sesgados a la derecha (ventas, ingresos), volviéndolos más simétricos. Otras: Box-Cox, potencia, exponencial. También se transforma la variable respuesta — recordando **revertir** la predicción a su escala original.

## Codificar categóricas y reducir dimensión

- **One-hot encoding:** una columna binaria por categoría (sin orden implícito).
- **Selección de features:** quedarse con las informativas (menos ruido, menos overfitting).
- **Reducción de dimensión (PCA):** comprimir muchas features correlacionadas en pocos componentes.

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
