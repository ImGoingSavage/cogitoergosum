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
