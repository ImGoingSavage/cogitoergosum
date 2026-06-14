# Regresión y predicción: interpretación y diagnóstico

## Dos usos de la regresión

- **Explicar:** entender cómo se relaciona cada predictor con la respuesta (foco en los coeficientes).
- **Predecir:** estimar la respuesta para nuevos casos (foco en la precisión predictiva).

La **regresión lineal múltiple** modela $Y = b_0 + b_1X_1 + \dots + b_pX_p + \varepsilon$. El coeficiente $b_j$ es el cambio esperado en Y por unidad de $X_j$ **manteniendo los demás constantes** — y esa última cláusula es la fuente de casi todas las trampas de interpretación.

## Intervalos: confianza vs predicción

- **Intervalo de confianza:** incertidumbre alrededor de un **estadístico** (la media predicha para un conjunto de casos).
- **Intervalo de predicción:** incertidumbre alrededor de un **valor individual** futuro.

Un intervalo de predicción es **mucho más ancho** que uno de confianza para el mismo punto, porque suma la incertidumbre del modelo **más** la variabilidad irreducible de un dato individual. Confundirlos lleva a subestimar el error real de una predicción.

## Las tres trampas de los coeficientes

### 1. Multicolinealidad (problema de comisión)
Predictores **redundantes** entre sí. La **multicolinealidad perfecta** ocurre cuando un predictor es combinación lineal de otros (incluir una variable dos veces, crear P dummies en vez de P−1, dos variables casi perfectamente correlacionadas). Con multicolinealidad perfecta la regresión **no tiene solución única**; con la imperfecta, los coeficientes se vuelven **inestables**. Solución: quitar variables hasta eliminarla. (Árboles, clustering y kNN no sufren tanto este problema.)

### 2. Variables confusoras / confounding (problema de omisión)
Se **omite** un predictor importante, y su efecto contamina a los incluidos, generando relaciones **espurias**. Ejemplo del libro: sin la variable "ubicación", los coeficientes de recámaras y baños salían **negativos** (absurdo); al añadir el grupo de código postal, los signos se corrigieron. La cláusula "manteniendo lo demás constante" falla si lo importante no está en el modelo.

### 3. Interacciones
El efecto de un predictor **depende del nivel de otro**. Ejemplo: el valor del pie cuadrado depende de la zona — en la zona más cara cada pie² suma ~$447, en la más barata ~$177. Se modela con un **término de interacción** $X_1 \cdot X_2$. Cómo elegir cuáles incluir: conocimiento del dominio, selección stepwise, regresión penalizada, o **modelos de árbol** (que las buscan solas).

## Diagnóstico por residuales

Los **residuales** (observado − predicho) son la materia prima para validar los supuestos:

- **Residual estandarizado:** residual ÷ su error estándar; "número de errores estándar de distancia a la recta". Detecta **outliers** (y en boxplot, > 1.5×IQR).
- **Valor influyente / leverage (hat-value):** un registro cuya presencia/ausencia mueve mucho la ecuación. Un punto puede ser influyente sin ser un outlier grande.
- **Heteroscedasticidad:** la varianza de los residuales **cambia** según el rango de la predicción — suele indicar que **falta un predictor**.
- **Residuales no normales:** invalidan algunos requisitos técnicos, pero **rara vez preocupan** en ciencia de datos (importan más para inferencia que para predicción).
- **Partial residual plots:** muestran la relación entre la respuesta y **un** predictor aislando los demás.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Incertidumbre de UNA predicción individual" | Intervalo de predicción (más ancho), no de confianza |
| "Coeficientes inestables o sin solución" | Multicolinealidad → quita predictores redundantes |
| "Un coeficiente tiene signo absurdo" | Sospecha confounding → falta un predictor (p.ej. ubicación) |
| "El efecto de X depende del nivel de Z" | Añade término de interacción X·Z |
| "Detectar outliers en la regresión" | Residual estandarizado (#SE de la recta) |
| "Un punto mueve mucho la recta" | Valor influyente / leverage (hat-value) |
| "La varianza de los residuales crece" | Heteroscedasticidad → quizá falta un predictor |

---

> **Síntesis:** En la regresión lineal múltiple cada coeficiente se lee "manteniendo lo demás constante", y de ahí salen sus trampas: **multicolinealidad** (predictores redundantes → solución inestable), **confounding** (omitir un predictor clave → coeficientes espurios, hasta con signo absurdo) e **interacciones** (el efecto de X depende de otro). Para predecir, el **intervalo de predicción** (individual) es mucho más ancho que el de confianza (media). El **diagnóstico por residuales** —residuales estandarizados para outliers, leverage para puntos influyentes, heteroscedasticidad como señal de un predictor faltante— valida los supuestos del modelo.

---

*Retrieval: cierra y responde: (1) ¿por qué un intervalo de predicción es más ancho que uno de confianza?; (2) distingue multicolinealidad de confounding (comisión vs omisión); (3) ¿qué indica la heteroscedasticidad?; (4) ¿cómo detectas un outlier en una regresión?*
