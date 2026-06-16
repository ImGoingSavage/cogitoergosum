# Regresión y predicción: interpretación y diagnóstico

## De qué trata esta lección (y qué sabrás hacer al final)

Ajustas una regresión y un coeficiente sale **negativo**: ¿una recámara más *baja* el precio de una casa? El número no está mal calculado; está respondiendo a la pregunta equivocada. Esta lección construye, desde cero, cómo **interpretar** una regresión sin caer en sus trampas (multicolinealidad, confounding, interacciones) y cómo **diagnosticarla** con los residuales. El hilo conductor es una sola cláusula traicionera: "manteniendo lo demás constante".

Al terminar podrás: (1) distinguir un intervalo de confianza (de la media) de uno de predicción (individual, mucho más ancho); (2) diagnosticar un coeficiente absurdo como **omisión** (confounding) y uno inestable como **comisión** (multicolinealidad); (3) modelar una **interacción** cuando el efecto de un predictor depende de otro; y (4) leer residuales para detectar outliers, leverage y heteroscedasticidad. Cada trampa entra por un ejemplo concreto.

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
El efecto de un predictor **depende del nivel de otro**. Ejemplo: el valor del pie cuadrado depende de la zona — en la zona más cara cada pie² suma ~\$447, en la más barata ~\$177. Se modela con un **término de interacción** $X_1 \cdot X_2$. Cómo elegir cuáles incluir: conocimiento del dominio, selección stepwise, regresión penalizada, o **modelos de árbol** (que las buscan solas).

## Diagnóstico por residuales

Los **residuales** (observado − predicho) son la materia prima para validar los supuestos:

- **Residual estandarizado:** residual ÷ su error estándar; "número de errores estándar de distancia a la recta". Detecta **outliers** (y en boxplot, > 1.5×IQR).
- **Valor influyente / leverage (hat-value):** un registro cuya presencia/ausencia mueve mucho la ecuación. Un punto puede ser influyente sin ser un outlier grande.
- **Heteroscedasticidad:** la varianza de los residuales **cambia** según el rango de la predicción — suele indicar que **falta un predictor**.
- **Residuales no normales:** invalidan algunos requisitos técnicos, pero **rara vez preocupan** en ciencia de datos (importan más para inferencia que para predicción).
- **Partial residual plots:** muestran la relación entre la respuesta y **un** predictor aislando los demás.

---

## Mini-ejemplo trabajado: el coeficiente con signo absurdo (confounding)

Regresas el precio de casas sobre número de recámaras y baños, y obtienes coeficientes **negativos**: ¿una recámara más *baja* el precio? Absurdo. Lo que pasa: falta la variable **ubicación**. Las casas grandes (más recámaras) abundan en zonas baratas (afueras), así que, al ignorar la zona, "más recámaras" carga con "zona barata".

Al añadir el código postal como predictor, la cláusula "manteniendo lo demás constante" por fin incluye la zona, y los signos se **corrigen a positivos**. El coeficiente no estaba mal calculado: estaba respondiendo a la pregunta equivocada.

**Predicción antes de seguir:** ¿este es un problema de *comisión* (incluir de más) o de *omisión* (excluir de más)? Respuesta: de **omisión** — confounding por variable omitida. Su gemelo de comisión es la *multicolinealidad* (incluir dos predictores redundantes), que en vez de sesgar el signo infla la varianza y vuelve inestables los coeficientes. Omitir lo importante sesga; incluir lo redundante desestabiliza.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** coeficiente con signo o magnitud absurda → sospecha confounding → busca el predictor omitido (ubicación, tamaño, tiempo).
- **Contraejemplo (multicolinealidad, no confounding):** dos predictores casi idénticos (m² y pies²) no sesgan la predicción pero hacen que los coeficientes "salten" entre signos; el modelo predice bien aunque sus betas sean ilegibles.
- **Caso borde (heteroscedasticidad):** si la varianza de los residuales crece con la predicción, suele faltar un predictor o una interacción; el ajuste promedio engaña sobre el error local.

## Errores típicos

- **Conceptual:** interpretar un beta observacional como efecto causal sin haber cerrado los confundidores.
- **Técnico:** usar un intervalo de confianza (de la media) cuando se quiere la incertidumbre de **una** predicción individual (intervalo de predicción, mucho más ancho).
- **De interpretación:** crear P variables dummy en vez de P−1 e introducir multicolinealidad perfecta (sin solución única).

## Transferencia isomorfa

- **Confounding / variable omitida ↔ back-door y ajuste:** "manteniendo lo demás constante" falla exactamente cuando no ajustas por la causa común; añadir la ubicación es cerrar un camino trasero (conecta con [[arena-h17]]).
- **Multicolinealidad ↔ VIF y features redundantes:** predictores que cargan la misma información inflan la varianza igual que en la teoría de Gauss-Markov, y como el leakage infla el desempeño (conecta con [[arena-dg4]] y [[arena-dmls1]]).
- **Término de interacción ↔ modificación de efecto / heterogeneidad:** que el valor del m² dependa de la zona es el mismo fenómeno que un efecto de tratamiento que varía por subgrupo (conecta con [[arena-h8]]).
- **Intervalo de predicción vs confianza ↔ incertidumbre del modelo + ruido irreducible:** la misma descomposición Var = explicada + irreducible de la ley de varianza total (conecta con [[arena-cb4]] y [[arena-b2]]).

Moraleja de la arista: *un signo absurdo grita "falta un predictor" (confounding, omisión); coeficientes que saltan gritan "sobra un predictor" (multicolinealidad, comisión); y predecir un individuo necesita el intervalo ancho, no el de la media.*

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
