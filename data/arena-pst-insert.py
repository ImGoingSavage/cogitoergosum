"""
Tanda 11: Practical Statistics for Data Scientists (Bruce & Bruce) — 60 preguntas, 4 unidades
=============================================================================================
Ruta ciencia-datos (§10). IDs calculados dinámicamente sobre la base integrada.

4 unidades de VALOR NUEVO (enfoque práctico / resampling-first; no duplica la
teoría de Ace ni el ML de Cracking):
arena-pst1 (EDA: estimadores robustos de centro y dispersión),
arena-pst2 (distribuciones muestrales y bootstrap),
arena-pst3 (experimentos estadísticos: A/B y tests de permutación),
arena-pst4 (regresión y predicción: interpretación y diagnóstico).

7 heurísticas nuevas (esquema rico). Reúsa intervalos-tests y
diseno-experimento-ab de Ace.
"""

import json

with open('data/study.json', 'r', encoding='utf-8') as f:
    study = json.load(f)

# ─── Heurísticas nuevas ───────────────────────────────────────────────────────
new_heuristicas = [
    {
        "id": "estimador-robusto",
        "nombre": "Elegir estimadores robustos en EDA",
        "descripcion": "Cuando hay outliers, prefiere resúmenes que no se dejen arrastrar por valores extremos: mediana o media recortada para el centro; IQR o MAD-mediana para la dispersión, en vez de la media y la desviación estándar.",
        "cuando_usar": "Al explorar una variable con cola larga u outliers, o cuando un solo valor extremo distorsiona el promedio/desviación.",
        "ejemplo": "El ingreso promedio de un pueblo sube si se muda un millonario; la mediana no se inmuta.",
        "patron": "Outliers→mediana/IQR/MAD; sin outliers→media/sd"
    },
    {
        "id": "bootstrap-resampling",
        "nombre": "Estimar variabilidad con el bootstrap",
        "descripcion": "Para conocer la distribución muestral de cualquier estadístico sin supuestos de normalidad, remuestrea CON reemplazo de tu propia muestra R veces y recalcula el estadístico; la dispersión de esos valores da el error estándar y el intervalo de confianza.",
        "cuando_usar": "Cuando no hay fórmula conocida para el error estándar de un estadístico, o quieres un IC sin asumir normalidad; también para la estabilidad de parámetros de un modelo.",
        "ejemplo": "Remuestrear los ingresos R=1000 veces y tomar la sd de las medianas como error estándar de la mediana.",
        "patron": "Remuestrea con reemplazo R veces → SE e IC; NO crea datos"
    },
    {
        "id": "test-permutacion",
        "nombre": "Significancia por test de permutación",
        "descripcion": "Para saber si una diferencia entre grupos es real o azar sin asumir normalidad: combina los grupos, barájalos y repártelos R veces, calcula el estadístico cada vez, y mira si la diferencia observada cae dentro (azar) o fuera (significativa) de esa distribución.",
        "cuando_usar": "En A/B tests con muestras pequeñas o desiguales, o cuando no quieres asumir una distribución; el p-valor es la fracción de permutaciones tan extremas como lo observado.",
        "ejemplo": "Página B retiene 21.4 s más que A: baraja los 36 tiempos en grupos de 21 y 15 mil veces y compara.",
        "patron": "Combina→baraja→reparte R veces→¿observado dentro o fuera?"
    },
    {
        "id": "vigilar-multiplicidad",
        "nombre": "Vigilar la multiplicidad",
        "descripcion": "Probar muchas comparaciones, subgrupos, variables o modelos garantiza que algo salga 'significativo' por azar. Contrólalo con un holdout etiquetado y validación cruzada, o con ajustes tipo Bonferroni/FDR.",
        "cuando_usar": "Siempre que explores muchas hipótesis o variables, o cuando un resultado 'significativo' aparezca tras mucho buscar. 'Si torturas los datos lo suficiente, confiesan'.",
        "ejemplo": "Revisar 20 subgrupos a α=0.05 → ~1 saldrá significativo por azar; cross-validation lo desenmascara.",
        "patron": "Más pruebas→más falsos positivos; holdout/CV/FDR lo controla"
    },
    {
        "id": "interpretar-coeficientes-regresion",
        "nombre": "Interpretar coeficientes de regresión",
        "descripcion": "Cada coeficiente se lee 'manteniendo lo demás constante', y de ahí salen tres trampas: multicolinealidad (predictores redundantes→inestable), confounding (omitir un predictor clave→coeficientes espurios) e interacciones (el efecto de X depende de otro).",
        "cuando_usar": "Al interpretar una regresión múltiple, sobre todo si un coeficiente tiene signo absurdo o los coeficientes cambian mucho al añadir/quitar variables.",
        "ejemplo": "Sin la variable 'ubicación', el coeficiente de recámaras salía negativo; al añadir el código postal se corrigió.",
        "patron": "Multicolinealidad(comisión)/confounding(omisión)/interacción"
    },
    {
        "id": "intervalo-prediccion-vs-confianza",
        "nombre": "Intervalo de predicción vs de confianza",
        "descripcion": "Un intervalo de confianza acota la incertidumbre de un estadístico (una media); un intervalo de predicción acota un valor individual futuro y es mucho más ancho, porque suma la incertidumbre del modelo más la variabilidad irreducible del dato.",
        "cuando_usar": "Al reportar la incertidumbre de una predicción: usa el de predicción para un caso individual, el de confianza para la media.",
        "ejemplo": "El precio medio de casas de 200 m² (confianza) tiene un intervalo estrecho; el precio de UNA casa concreta (predicción) uno mucho más ancho.",
        "patron": "Individual→predicción(ancho); media→confianza(estrecho)"
    },
    {
        "id": "diagnostico-residuales",
        "nombre": "Diagnóstico de regresión por residuales",
        "descripcion": "Los residuales (observado−predicho) validan los supuestos: residuales estandarizados detectan outliers, el leverage/hat-value señala puntos influyentes, y la heteroscedasticidad (varianza que cambia con el rango) suele indicar un predictor faltante.",
        "cuando_usar": "Tras ajustar una regresión, para evaluar el ajuste y descubrir outliers, puntos influyentes o variables omitidas.",
        "ejemplo": "Un residual estandarizado de 4 marca un outlier (4 errores estándar de la recta); un punto influyente mueve la pendiente al quitarlo.",
        "patron": "Residual estandarizado→outlier; leverage→influyente; heterosced.→falta predictor"
    },
]

existing_ids = {h['id'] for h in study['catalogoHeuristicas']}
for h in new_heuristicas:
    if h['id'] not in existing_ids:
        study['catalogoHeuristicas'].append(h)
        print(f"Heurística añadida: {h['id']}")
    else:
        print(f"Heurística ya existe (skip): {h['id']}")

# Verificar que las heurísticas reusadas existen
for reuse in ['intervalos-tests', 'diseno-experimento-ab']:
    print(f"Reusar '{reuse}': {'OK' if reuse in {h['id'] for h in study['catalogoHeuristicas']} else 'NO EXISTE!'}")

max_ord = max((u.get('orden', 0) for u in study['unidades'] if u.get('bloque') == 'fase-7'), default=0)
print(f"Max orden fase-7 (post-pull): {max_ord}")

# ─── arena-pst1: EDA — estimadores robustos ───────────────────────────────────
unit_pst1 = {
    "id": "arena-pst1",
    "bloque": "fase-7",
    "orden": max_ord + 1,
    "titulo": "Análisis exploratorio: estimadores robustos",
    "libro": "Practical Statistics for Data Scientists (Bruce & Bruce)",
    "lectura": "data/teoria/arena-pst1.md",
    "dosis": 30,
    "objetivo": "Elegir estimadores de centro y dispersión según su robustez a outliers, y dominar percentiles, IQR, MAD y correlación.",
    "heuristicas": ["estimador-robusto"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 1},
    "ideas_clave": [
        "Robusto = no se deja arrastrar por outliers: mediana y media recortada lo son, la media no",
        "Dispersión robusta: IQR y MAD-mediana; sd y varianza son sensibles",
        "n−1 en la varianza la vuelve un estimador insesgado (grados de libertad)"
    ],
    "banco": [
        {"id": "arpst1-q1", "tipo": "concepto", "enunciado": "¿Qué significa que un estimador sea 'robusto' y por qué la mediana lo es frente a la media?", "solucion": "Robusto significa que no se ve influido por valores extremos (outliers). La mediana es el valor central de la lista ordenada: solo depende de cuántos datos hay a cada lado, no de cuán extremos sean, así que un outlier no la mueve. La media, en cambio, usa todas las observaciones y un solo valor enorme la arrastra.", "explicacion": "La robustez es resistencia a outliers. La mediana ignora la magnitud de los extremos; por eso describe mejor el centro de datos sesgados (ingresos, precios)."},
        {"id": "arpst1-q2", "tipo": "concepto", "enunciado": "¿Qué es una media recortada (trimmed mean) y qué problema resuelve?", "solucion": "Se calcula descartando un porcentaje fijo de los valores más altos y más bajos y promediando el resto. Resuelve la sensibilidad de la media a outliers sin descartar tanta información como la mediana: es un compromiso entre ambas, robusto a los extremos pero usando la mayoría de los datos.", "explicacion": "Como en clavados, donde se quitan la nota más alta y la más baja para evitar que un juez sesgue el resultado. Es robusta y eficiente a la vez."},
        {"id": "arpst1-q3", "tipo": "concepto", "enunciado": "Para un pueblo donde de pronto se muda un multimillonario, ¿qué métrica de ingreso 'típico' reportarías y por qué?", "solucion": "La mediana (o una media recortada), porque la media se dispararía por ese único valor extremo y dejaría de representar al residente típico. La mediana no cambia por más rico que sea el recién llegado.", "explicacion": "Es el caso canónico de outlier: un valor extremo distorsiona la media pero no la mediana, que sigue describiendo el centro real de la distribución."},
        {"id": "arpst1-q4", "tipo": "concepto", "enunciado": "¿Por qué no se promedian directamente las desviaciones respecto a la media para medir dispersión?", "solucion": "Porque la suma de las desviaciones respecto a la media es exactamente cero (las negativas cancelan a las positivas), así que su promedio sería siempre 0 y no informaría nada. Por eso se usan valores absolutos (MAD) o cuadrados (varianza) de las desviaciones.", "explicacion": "La media es el punto que equilibra las desviaciones; hay que eliminar el signo (absoluto o cuadrado) para que no se anulen y capturar la magnitud de la dispersión."},
        {"id": "arpst1-q5", "tipo": "concepto", "enunciado": "Define varianza y desviación estándar. ¿Por qué se prefiere la desviación estándar para interpretar?", "solucion": "Varianza = promedio de las desviaciones al cuadrado respecto a la media (denominador n−1). Desviación estándar = raíz cuadrada de la varianza. Se prefiere la desviación estándar para interpretar porque está en la misma escala que los datos originales, mientras la varianza está en unidades al cuadrado.", "explicacion": "La sd es directamente comparable con los datos (mismas unidades); la varianza, aunque matemáticamente conveniente, vive en unidades al cuadrado poco intuitivas."},
        {"id": "arpst1-q6", "tipo": "concepto", "enunciado": "¿Por qué la varianza divide entre n−1 y no entre n?", "solucion": "Dividir entre n subestima la varianza poblacional (estimador sesgado); dividir entre n−1 la corrige a un estimador insesgado. La razón es que hay n−1 grados de libertad: la varianza muestral se calcula respecto a la media muestral, lo que impone una restricción. En la práctica, con n grande, la diferencia es despreciable.", "explicacion": "Los grados de libertad descuentan la restricción de haber estimado ya la media a partir de los mismos datos; n−1 compensa el optimismo del estimador."},
        {"id": "arpst1-q7", "tipo": "concepto", "enunciado": "Ni la varianza ni la desviación estándar son robustas. ¿Qué métrica de dispersión usarías con outliers y cómo se define?", "solucion": "La MAD mediana (median absolute deviation): la mediana de los valores absolutos de las desviaciones respecto a la mediana. Como se basa en medianas y no en cuadrados, no la afectan los valores extremos. También sirve el IQR.", "explicacion": "La sd, basada en desviaciones al cuadrado, es especialmente sensible a outliers (los eleva al cuadrado). La MAD-mediana es su análogo robusto."},
        {"id": "arpst1-q8", "tipo": "calculo", "enunciado": "Calcula el IQR de los datos: 3, 1, 5, 3, 6, 7, 2, 9.", "solucion": "Ordenados: 1,2,3,3,5,6,7,9. El percentil 25 está en ~2.5 y el percentil 75 en ~6.5, así que IQR = 6.5 − 2.5 = 4. (Distintos software pueden dar valores ligeramente distintos por la interpolación.)", "explicacion": "El IQR = P75 − P25 mide la dispersión del 50% central, ignorando las colas; por eso resiste outliers."},
        {"id": "arpst1-q9", "tipo": "concepto", "enunciado": "¿Qué es un percentil (cuantil) y cómo se relaciona con la mediana?", "solucion": "El percentil P es el valor tal que al menos P% de los datos son menores o iguales a él y (100−P)% son mayores o iguales. La mediana es el percentil 50. El cuantil es lo mismo indexado por fracciones (el cuantil .8 = percentil 80).", "explicacion": "Los percentiles describen la posición relativa dentro de la distribución ordenada; resumen forma y dispersión sin asumir ninguna distribución."},
        {"id": "arpst1-q10", "tipo": "concepto", "enunciado": "¿Qué muestra un boxplot y cómo marca los outliers?", "solucion": "Un boxplot resume la distribución con la mediana (línea central), los cuartiles 25 y 75 (la caja, cuya altura es el IQR) y los bigotes. Marca como outliers los puntos a más de 1.5×IQR por encima del P75 o por debajo del P25.", "explicacion": "Es una vista compacta basada en order statistics (robustas) que muestra centro, dispersión y outliers de un vistazo, ideal para comparar grupos."},
        {"id": "arpst1-q11", "tipo": "concepto", "enunciado": "¿Por qué el rango (máx − mín) es una mala medida general de dispersión?", "solucion": "Porque depende exactamente de los dos valores más extremos, así que es extremadamente sensible a outliers: un solo dato anómalo dispara el rango sin que el grueso de los datos esté más disperso. Por eso se prefiere el IQR, que recorta las colas.", "explicacion": "El rango usa solo los extremos, justo los más propensos a ser atípicos; no resume la dispersión típica de la masa de datos."},
        {"id": "arpst1-q12", "tipo": "concepto", "enunciado": "Ordena de mayor a menor la desviación estándar (sd), la MAD (media) y la MAD-mediana para datos normales, y di cuál es robusta.", "solucion": "sd > MAD (media) > MAD-mediana. La MAD-mediana es la robusta a outliers; la sd es la más sensible (por los cuadrados). A veces la MAD-mediana se multiplica por 1.4826 para ponerla en la misma escala que la sd bajo normalidad.", "explicacion": "Las tres miden dispersión pero no son equivalentes; elevar al cuadrado (sd) infla el peso de los valores grandes, de ahí el orden."},
        {"id": "arpst1-q13", "tipo": "concepto", "enunciado": "¿Qué mide el coeficiente de correlación de Pearson y cuáles son sus dos limitaciones clave?", "solucion": "Mide la fuerza y dirección de la asociación LINEAL entre dos variables numéricas, en [−1, 1]; es la covarianza normalizada por las desviaciones estándar, así que es adimensional. Limitaciones: (1) solo capta relaciones lineales (puede dar ~0 ante una relación fuerte pero curva); (2) es sensible a outliers.", "explicacion": "Normalizar la covarianza la hace comparable entre pares de variables, pero no detecta no-linealidades ni resiste valores extremos."},
        {"id": "arpst1-q14", "tipo": "concepto", "enunciado": "¿Cuándo usarías una media o mediana ponderada en lugar de la simple?", "solucion": "Cuando las observaciones no deben pesar igual: p.ej. al combinar tasas de varios grupos de distinto tamaño (ponderar por población), o cuando algunos datos son más confiables/representativos que otros. La mediana ponderada sigue siendo robusta a outliers.", "explicacion": "Promediar tasas sin ponderar por el tamaño de cada grupo da un resultado engañoso; los pesos corrigen la contribución de cada observación."},
        {"id": "arpst1-q15", "tipo": "concepto", "enunciado": "Resume la regla práctica para elegir entre estimadores clásicos (media, sd) y robustos (mediana, IQR, MAD).", "solucion": "Si los datos no tienen outliers ni cola pesada y se aproximan a una distribución simétrica, la media y la desviación estándar son apropiadas y eficientes. Si hay outliers, asimetría o colas largas, usa la mediana o media recortada para el centro y el IQR o la MAD-mediana para la dispersión.", "explicacion": "La elección equilibra eficiencia (clásicos, cuando los supuestos se cumplen) contra robustez (cuando hay contaminación por extremos)."}
    ]
}

# ─── arena-pst2: Distribuciones muestrales y bootstrap ────────────────────────
unit_pst2 = {
    "id": "arena-pst2",
    "bloque": "fase-7",
    "orden": max_ord + 2,
    "titulo": "Distribuciones muestrales y bootstrap",
    "libro": "Practical Statistics for Data Scientists (Bruce & Bruce)",
    "lectura": "data/teoria/arena-pst2.md",
    "dosis": 30,
    "objetivo": "Distinguir distribución de datos vs muestral, error estándar vs desviación estándar, y usar el bootstrap para estimar variabilidad e intervalos sin supuestos.",
    "heuristicas": ["bootstrap-resampling", "intervalos-tests"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 2},
    "ideas_clave": [
        "Error estándar = variabilidad del estadístico; desviación estándar = de los datos",
        "El bootstrap remuestrea con reemplazo para estimar la distribución muestral de cualquier estadístico",
        "SE ∝ 1/√n: reducirlo a la mitad exige cuadruplicar n"
    ],
    "banco": [
        {"id": "arpst2-q1", "tipo": "concepto", "enunciado": "Distingue la distribución de los datos de la distribución muestral de un estadístico.", "solucion": "La distribución de los datos describe cómo se reparten las observaciones individuales. La distribución muestral describe cómo se repartiría un estadístico (la media, la mediana...) si tomaras muchas muestras distintas. La muestral es más estrecha y más normal que la de los datos.", "explicacion": "Una es sobre puntos individuales; la otra sobre un resumen calculado de cada muestra. Confundirlas lleva a malinterpretar la incertidumbre."},
        {"id": "arpst2-q2", "tipo": "concepto", "enunciado": "¿Cuál es la diferencia entre desviación estándar y error estándar?", "solucion": "La desviación estándar mide la variabilidad de los datos individuales. El error estándar mide la variabilidad de un estadístico muestral (p.ej. cuánto variaría la media de muestra a muestra). No son intercambiables: el error estándar resume la anchura de la distribución muestral.", "explicacion": "Una describe los datos; la otra, la precisión de un estimador calculado de esos datos. El error estándar siempre es menor que la sd de los datos (se encoge con n)."},
        {"id": "arpst2-q3", "tipo": "calculo", "enunciado": "El error estándar de la media es SE = s/√n. Si quieres reducir el SE a la mitad, ¿cuánto debes aumentar n?", "solucion": "Como SE ∝ 1/√n, para dividir el SE entre 2 hay que multiplicar √n por 2, es decir multiplicar n por 4 (cuadruplicarlo).", "explicacion": "La raíz cuadrada implica rendimientos decrecientes: cada mejora de precisión cuesta cada vez más datos. Por eso recolectar más no siempre vale la pena."},
        {"id": "arpst2-q4", "tipo": "concepto", "enunciado": "¿Qué dice el Teorema Central del Límite y por qué el libro sostiene que el data scientist no depende tanto de él?", "solucion": "El CLT dice que la distribución muestral de la media tiende a la normal al crecer n, sin importar la distribución de los datos; sustenta las fórmulas clásicas (t, IC, tests). El data scientist no depende tanto de él porque los tests formales pesan poco en la práctica y el bootstrap estima la distribución muestral sin necesidad de supuestos distribucionales.", "explicacion": "El CLT es el motor de la inferencia clásica, pero el bootstrap ofrece una vía empírica que funciona aun cuando no hay fórmula o no se cumple la normalidad."},
        {"id": "arpst2-q5", "tipo": "concepto", "enunciado": "Describe el algoritmo del bootstrap para estimar la variabilidad de la media.", "solucion": "1) Saca un valor de la muestra, regístralo y devuélvelo (con reemplazo). 2) Repite n veces para formar un bootstrap sample. 3) Registra la media de esos n valores. 4) Repite los pasos 1–3 R veces. 5) Con los R resultados: su desviación estándar estima el error estándar, y sus percentiles dan un intervalo de confianza.", "explicacion": "El muestreo con reemplazo simula sacar de una población infinita parecida a tu muestra; la dispersión de los R estadísticos aproxima la distribución muestral."},
        {"id": "arpst2-q6", "tipo": "concepto", "enunciado": "¿Por qué el bootstrap muestrea CON reemplazo y no sin reemplazo?", "solucion": "Porque muestrear con reemplazo simula extraer de una población infinita en la que la probabilidad de cada elemento se mantiene constante de extracción en extracción. Sin reemplazo se agotaría la muestra y se obtendría siempre el mismo conjunto reordenado, sin variabilidad útil.", "explicacion": "El reemplazo es lo que permite que distintos bootstrap samples difieran entre sí, generando la dispersión que estima la distribución muestral."},
        {"id": "arpst2-q7", "tipo": "concepto", "enunciado": "¿Cuál es el malentendido más común sobre el bootstrap? Da la advertencia correcta.", "solucion": "El malentendido es creer que el bootstrap crea datos nuevos o compensa una muestra pequeña ('hila oro de la paja'). La advertencia: el bootstrap NO crea datos ni llena huecos; solo informa cómo se comportarían muchas muestras tomadas de una población parecida a tu muestra original.", "explicacion": "El bootstrap cuantifica la incertidumbre dada tu muestra; si la muestra es mala o pequeña, el bootstrap lo reflejará pero no lo arreglará."},
        {"id": "arpst2-q8", "tipo": "concepto", "enunciado": "¿Para qué tipo de estadísticos es especialmente valioso el bootstrap frente a las fórmulas clásicas?", "solucion": "Para estadísticos donde no existe (o es complicada) una fórmula matemática de su distribución muestral: la mediana, percentiles, ratios, coeficientes de modelos complejos, etc. La distribución muestral de la media se conoce desde 1908, pero la de muchos otros no.", "explicacion": "El bootstrap es agnóstico al estadístico: el mismo procedimiento sirve para cualquiera, lo que lo hace ideal cuando no hay teoría disponible."},
        {"id": "arpst2-q9", "tipo": "concepto", "enunciado": "¿Cómo se aplica el bootstrap a datos multivariados y qué relación tiene con el bagging?", "solucion": "Con datos multivariados se remuestrean las FILAS completas como unidades (no las columnas por separado), preservando la estructura entre variables. Correr un modelo sobre muchas muestras bootstrap y promediar (o votar, en clasificación) sus predicciones es el bagging ('bootstrap aggregating'), que mejora la estabilidad — base del Random Forest.", "explicacion": "Remuestrear filas mantiene las correlaciones entre features; agregar muchos modelos bootstrap reduce la varianza de la predicción."},
        {"id": "arpst2-q10", "tipo": "concepto", "enunciado": "¿Qué es un intervalo de confianza para un data scientist, según el enfoque práctico del libro?", "solucion": "Una herramienta para ver cuán variable es un resultado muestral, más que un ritual de inferencia formal. Un IC del 90/95% es el rango central de la distribución muestral (p.ej. bootstrap) que contiene ese porcentaje de los valores del estadístico.", "explicacion": "El énfasis práctico es comunicar incertidumbre. El bootstrap produce el IC tomando los percentiles de los R estadísticos remuestreados."},
        {"id": "arpst2-q11", "tipo": "concepto", "enunciado": "¿Cuál es la interpretación correcta de un intervalo de confianza del 95% y cuál la incorrecta?", "solucion": "Correcta: es el resultado de un procedimiento que, repetido en muchas muestras, captura el parámetro verdadero el 95% de las veces (cobertura del método). Incorrecta: 'hay 95% de probabilidad de que el parámetro esté en este intervalo concreto', porque el parámetro es fijo y el intervalo es el aleatorio.", "explicacion": "La aleatoriedad vive en el intervalo (depende de la muestra), no en el parámetro. La probabilidad describe el procedimiento a largo plazo."},
        {"id": "arpst2-q12", "tipo": "concepto", "enunciado": "¿Qué es el sesgo de selección y qué es la self-selection bias?", "solucion": "El sesgo de selección es elegir datos —consciente o inconscientemente— de forma no representativa, lo que invalida conclusiones. La self-selection bias es un caso donde los propios sujetos deciden participar (p.ej. quienes dejan reseñas), de modo que la muestra no representa a la población.", "explicacion": "Si quién entra a la muestra depende de la variable de interés, los resultados se sesgan. Las reseñas las escriben los muy satisfechos o muy molestos, no el cliente típico."},
        {"id": "arpst2-q13", "tipo": "concepto", "enunciado": "Explica la regresión a la media y por qué puede confundirse con un efecto real.", "solucion": "Tras observar un valor extremo, la siguiente medición tiende a estar más cerca del promedio, solo por azar. Se confunde con un efecto real cuando, por ejemplo, una intervención aplicada justo después de un extremo parece 'funcionar', pero el regreso al promedio habría ocurrido de todos modos. Es una forma de sesgo de selección.", "explicacion": "Seleccionar casos por ser extremos garantiza que en promedio mejoren/empeoren hacia la media; atribuirlo a una causa es el error (el 'maleficio del novato del año')."},
        {"id": "arpst2-q14", "tipo": "concepto", "enunciado": "¿En qué se diferencia 'resampling' de 'bootstrap'?", "solucion": "Resampling es el término general para tomar muestras repetidas de los datos observados, e incluye tanto el bootstrap (con reemplazo) como los procedimientos de permutación (barajar, normalmente sin reemplazo). 'Bootstrap' siempre implica muestreo CON reemplazo.", "explicacion": "Todo bootstrap es resampling, pero no todo resampling es bootstrap; los tests de permutación son la otra gran familia de remuestreo."},
        {"id": "arpst2-q15", "tipo": "concepto", "enunciado": "Tienes la mediana de ingresos de 1000 préstamos y quieres reportar su incertidumbre, pero no recuerdas fórmula del error estándar de una mediana. ¿Qué haces?", "solucion": "Aplicar el bootstrap: remuestrear con reemplazo los 1000 ingresos R=1000 veces, calcular la mediana de cada remuestreo, y usar la desviación estándar de esas 1000 medianas como error estándar y sus percentiles 2.5/97.5 como IC del 95%. No se necesita fórmula ni supuesto de normalidad.", "explicacion": "Es el caso de uso paradigmático del bootstrap: estimar la variabilidad de un estadístico (la mediana) sin fórmula conocida, de forma puramente empírica."}
    ]
}

# ─── arena-pst3: Experimentos estadísticos / permutación ──────────────────────
unit_pst3 = {
    "id": "arena-pst3",
    "bloque": "fase-7",
    "orden": max_ord + 3,
    "titulo": "Experimentos estadísticos y tests de permutación",
    "libro": "Practical Statistics for Data Scientists (Bruce & Bruce)",
    "lectura": "data/teoria/arena-pst3.md",
    "dosis": 30,
    "objetivo": "Diseñar A/B tests, evaluar significancia con tests de permutación, dimensionar por potencia y cuidarse de la multiplicidad.",
    "heuristicas": ["test-permutacion", "vigilar-multiplicidad", "diseno-experimento-ab"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 2},
    "ideas_clave": [
        "El test de permutación encarna la H0 combinando y barajando los grupos",
        "Potencia = prob. de detectar un efecto dado; más n → más potencia",
        "Multiplicidad: probar mucho garantiza falsos positivos; usa holdout/CV/FDR"
    ],
    "banco": [
        {"id": "arpst3-q1", "tipo": "concepto", "enunciado": "¿Qué es un A/B test y qué representa su hipótesis nula?", "solucion": "Un A/B test compara dos tratamientos (p.ej. página A vs B) asignando sujetos al azar a cada grupo y midiendo una métrica. La hipótesis nula (H0) afirma que no hay diferencia entre tratamientos: cualquier discrepancia observada se debe al azar. El objetivo es reunir evidencia para rechazarla.", "explicacion": "La asignación aleatoria hace comparables los grupos; la H0 es el punto de partida escéptico que el experimento intenta refutar."},
        {"id": "arpst3-q2", "tipo": "concepto", "enunciado": "Describe los pasos de un test de permutación para comparar dos grupos.", "solucion": "1) Combina los resultados de ambos grupos en un solo conjunto. 2) Baraja y reparte sin reemplazo un remuestreo del tamaño del grupo A; del resto, uno del tamaño de B. 3) Calcula el estadístico de interés (p.ej. diferencia de medias) para esos grupos barajados. 4) Repite R veces para formar la distribución de permutación. 5) Compara la diferencia observada con esa distribución.", "explicacion": "Combinar y barajar encarna la H0 (los grupos son intercambiables); la distribución resultante es la de 'puro azar' contra la que se mide lo observado."},
        {"id": "arpst3-q3", "tipo": "concepto", "enunciado": "En un test de permutación, ¿cómo decides si la diferencia observada es estadísticamente significativa?", "solucion": "Si la diferencia observada cae dentro del grueso de las diferencias permutadas, el azar podría explicarla y NO es significativa. Si cae fuera de casi todas (en las colas de la distribución de permutación), el azar no la explica y SÍ es estadísticamente significativa.", "explicacion": "La distribución de permutación representa lo que el azar produce bajo la H0; lo observado solo es 'real' si es atípico respecto a ella."},
        {"id": "arpst3-q4", "tipo": "concepto", "enunciado": "¿Qué ventajas tiene el test de permutación frente a un t-test clásico?", "solucion": "No asume normalidad de los datos, funciona con tamaños de grupo iguales o distintos, sirve para métricas numéricas o binarias, y es intuitivo (basado en barajar). Es especialmente útil con muestras pequeñas o distribuciones raras donde las fórmulas clásicas no aplican bien.", "explicacion": "Al construir empíricamente la distribución bajo H0, evita los supuestos distribucionales que sostienen al t-test."},
        {"id": "arpst3-q5", "tipo": "concepto", "enunciado": "Define el p-valor en el contexto de un test de permutación.", "solucion": "Es la probabilidad de observar un resultado tan o más extremo que el real suponiendo H0 cierta; en el test de permutación es directamente la fracción de las permutaciones cuyo estadístico iguala o supera al observado. No es la probabilidad de que H0 sea cierta.", "explicacion": "El p-valor cuantifica cuán sorprendente es lo observado bajo el azar; en permutación se calcula contando, no con fórmulas."},
        {"id": "arpst3-q6", "tipo": "concepto", "enunciado": "¿Qué es una variable proxy y cuándo se usa en un experimento?", "solucion": "Es una variable que sustituye a la verdadera variable de interés cuando esta es inaccesible, muy costosa o lenta de medir. P.ej., si las ventas son escasas y lentas, se mide el tiempo en la página como proxy del interés de compra. Conviene tener algo de datos de la variable verdadera para validar la asociación.", "explicacion": "El proxy permite experimentar cuando el outcome real tarda demasiado, pero su validez depende de cuán fuerte sea su relación con la variable verdadera."},
        {"id": "arpst3-q7", "tipo": "concepto", "enunciado": "Distingue error Tipo I y Tipo II en un experimento.", "solucion": "Error Tipo I: declarar real un efecto que en verdad es azar (falso positivo), con probabilidad α. Error Tipo II: no detectar un efecto que sí es real (falso negativo), con probabilidad β.", "explicacion": "α la fija el analista (típico 0.05); β depende del tamaño del efecto y de n. Reducir uno suele aumentar el otro a n fijo."},
        {"id": "arpst3-q8", "tipo": "concepto", "enunciado": "Define potencia estadística y di qué la aumenta.", "solucion": "La potencia es la probabilidad de detectar un efecto de un tamaño dado con un tamaño de muestra dado, es decir 1−β. Aumenta al incrementar el tamaño de muestra n, al aumentar el tamaño del efecto a detectar, o al reducir la varianza/mejorar el diseño de medición.", "explicacion": "Más datos y efectos más grandes son más fáciles de detectar; dimensionar un experimento es elegir n para una potencia objetivo dado un efecto."},
        {"id": "arpst3-q9", "tipo": "concepto", "enunciado": "¿Qué es el tamaño del efecto (effect size) y por qué es necesario para calcular el tamaño de muestra?", "solucion": "Es la magnitud mínima de diferencia que quieres poder detectar (p.ej. +1% de conversión). Es necesario porque la potencia depende de él: detectar un efecto pequeño exige muchos más datos que uno grande. Sin fijar el effect size no se puede despejar el n requerido.", "explicacion": "Potencia, α, tamaño del efecto y n están ligados: fijando tres se despeja el cuarto. El effect size traduce 'qué diferencia me importa' en datos necesarios."},
        {"id": "arpst3-q10", "tipo": "concepto", "enunciado": "Explica el problema de la multiplicidad con un ejemplo.", "solucion": "Si pruebas muchas comparaciones, subgrupos, variables o modelos, por puro azar algo saldrá 'significativo' aunque no haya efecto real. Ejemplo: revisar 20 subgrupos a α=0.05 hace esperar ~1 falso positivo; o 'no hubo efecto general, pero sí en mujeres solteras menores de 30'. 'Si torturas los datos lo suficiente, confiesan'.", "explicacion": "Cada test tiene 5% de falso positivo; con muchos, la probabilidad de al menos uno se dispara. Es una causa mayor de resultados irreproducibles."},
        {"id": "arpst3-q11", "tipo": "concepto", "enunciado": "Según el enfoque práctico del libro, ¿cómo controla un data scientist la multiplicidad en modelado predictivo?", "solucion": "Mediante validación cruzada y un holdout etiquetado: si un modelo parece eficaz solo por azar, no sobrevivirá en datos no vistos. Donde no hay holdout, se confía en la conciencia de que más manipulación = más rol del azar, y en heurísticas de remuestreo/simulación como benchmark del azar.", "explicacion": "El holdout es el antídoto empírico: un efecto ilusorio nacido de mucho buscar se desinfla en datos frescos. Es más práctico que ajustes formales rígidos."},
        {"id": "arpst3-q12", "tipo": "concepto", "enunciado": "¿Qué es la False Discovery Rate (FDR) y la corrección de Bonferroni?", "solucion": "La FDR es la tasa esperada de falsos descubrimientos (tests que declaran efecto sin haberlo) entre los rechazos; se busca mantenerla bajo un nivel cuando se hacen muchísimos tests (p.ej. genómica). Bonferroni es un ajuste conservador que divide α entre el número de tests (α/m) para controlar la probabilidad de al menos un falso positivo (FWER).", "explicacion": "Ambos endurecen el umbral para compensar la multiplicidad; Bonferroni controla la FWER (cualquier error), la FDR controla la proporción de errores entre los hallazgos."},
        {"id": "arpst3-q13", "tipo": "concepto", "enunciado": "¿Para qué sirve ANOVA y en qué se diferencia de un test entre dos grupos?", "solucion": "ANOVA generaliza la comparación a más de dos grupos: prueba si existe alguna diferencia entre las medias de varios grupos a la vez, en lugar de compararlos de a pares (lo que dispararía la multiplicidad). Su versión por remuestreo baraja los datos entre todos los grupos.", "explicacion": "Comparar k grupos por pares haría muchos tests; ANOVA hace una sola prueba global controlando el riesgo de falsos positivos por multiplicidad."},
        {"id": "arpst3-q14", "tipo": "concepto", "enunciado": "¿Cuándo usarías una prueba Chi-cuadrado en un experimento?", "solucion": "Cuando comparas conteos o proporciones entre categorías: p.ej. si las tasas de conversión de varias variantes difieren más de lo esperado por azar. Compara frecuencias observadas contra las esperadas bajo H0 en una tabla de contingencia.", "explicacion": "Es la herramienta para datos categóricos/de frecuencias; su análogo por remuestreo baraja las etiquetas de categoría y recalcula el estadístico."},
        {"id": "arpst3-q15", "tipo": "concepto", "enunciado": "Una empresa quiere comparar dos páginas pero solo tiene 21 y 15 visitas con tiempos de sesión muy variables. ¿Qué enfoque de significancia recomiendas y por qué?", "solucion": "Un test de permutación: combinar los 36 tiempos, barajarlos y repartirlos repetidamente en grupos de 21 y 15, recalcular la diferencia de medias cada vez, y comparar la diferencia observada con esa distribución. Con muestras pequeñas y posiblemente no normales, la permutación no exige supuestos distribucionales que aquí no se sostienen.", "explicacion": "Es justo el escenario donde las fórmulas clásicas son frágiles (n chico, varianza alta); la permutación da un p-valor empírico robusto."}
    ]
}

# ─── arena-pst4: Regresión y predicción ───────────────────────────────────────
unit_pst4 = {
    "id": "arena-pst4",
    "bloque": "fase-7",
    "orden": max_ord + 4,
    "titulo": "Regresión y predicción: interpretación y diagnóstico",
    "libro": "Practical Statistics for Data Scientists (Bruce & Bruce)",
    "lectura": "data/teoria/arena-pst4.md",
    "dosis": 30,
    "objetivo": "Interpretar coeficientes de regresión múltiple evitando multicolinealidad/confounding/interacciones, distinguir intervalos de predicción vs confianza y diagnosticar por residuales.",
    "heuristicas": ["interpretar-coeficientes-regresion", "intervalo-prediccion-vs-confianza", "diagnostico-residuales"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 3},
    "ideas_clave": [
        "Cada coeficiente se lee 'manteniendo lo demás constante': de ahí sus trampas",
        "Intervalo de predicción (individual) ≫ intervalo de confianza (media)",
        "Residuales validan supuestos: outliers, leverage, heteroscedasticidad"
    ],
    "banco": [
        {"id": "arpst4-q1", "tipo": "concepto", "enunciado": "Diferencia el uso explicativo del uso predictivo de una regresión.", "solucion": "El uso explicativo busca entender cómo se relaciona cada predictor con la respuesta (foco en interpretar los coeficientes y validar supuestos). El uso predictivo busca estimar bien la respuesta para nuevos casos (foco en la precisión predictiva fuera de muestra), donde la interpretación de coeficientes importa menos.", "explicacion": "Son objetivos distintos: explicar exige diagnóstico riguroso de coeficientes; predecir prioriza el desempeño en datos no vistos."},
        {"id": "arpst4-q2", "tipo": "concepto", "enunciado": "¿Cómo se interpreta un coeficiente b_j en una regresión lineal múltiple, y por qué esa cláusula causa problemas?", "solucion": "b_j es el cambio esperado en Y por unidad de X_j MANTENIENDO LOS DEMÁS PREDICTORES CONSTANTES. Esa cláusula causa problemas porque rara vez los predictores son independientes: si están correlacionados (multicolinealidad) o falta uno importante (confounding), 'mantener lo demás constante' deja de ser realista y la interpretación se distorsiona.", "explicacion": "El 'todo lo demás igual' es una idealización; cuando los predictores se mueven juntos o falta información, los coeficientes dejan de tener el significado limpio que sugiere la fórmula."},
        {"id": "arpst4-q3", "tipo": "concepto", "enunciado": "¿Qué es la multicolinealidad y cuándo es 'perfecta'? ¿Qué problema causa?", "solucion": "Es la redundancia entre predictores por estar muy correlacionados. Es perfecta cuando un predictor es combinación lineal exacta de otros (incluir una variable dos veces, crear P dummies en vez de P−1, dos variables casi idénticas). La perfecta deja a la regresión SIN solución única; la imperfecta produce coeficientes inestables (varían mucho ante pequeños cambios en los datos).", "explicacion": "Si dos predictores aportan la misma información, el modelo no puede repartir el efecto entre ellos de forma única; hay que eliminar la redundancia."},
        {"id": "arpst4-q4", "tipo": "concepto", "enunciado": "¿Qué es una variable confusora (confounding) y cómo se distingue de la multicolinealidad?", "solucion": "Confounding es un problema de OMISIÓN: se deja fuera del modelo un predictor importante, y su efecto contamina a los incluidos, generando relaciones espurias. La multicolinealidad es un problema de COMISIÓN: incluir predictores redundantes. Una omite algo clave; la otra incluye algo de más.", "explicacion": "El confounding hace que coeficientes parezcan tener un efecto que en realidad pertenece a la variable omitida; corregirlo es añadir esa variable, no quitarla."},
        {"id": "arpst4-q5", "tipo": "concepto", "enunciado": "En el ejemplo de precios de casas, los coeficientes de recámaras y baños salían negativos. ¿Qué causaba esto y cómo se corrigió?", "solucion": "Era confounding: faltaba la variable de ubicación, un predictor clave del precio. Sin ella, recámaras/baños actuaban como proxy distorsionado y salían con signo negativo (absurdo). Al añadir una variable de grupo de código postal, los signos se corrigieron a valores razonables.", "explicacion": "Un coeficiente con signo contraintuitivo es una señal típica de confounding: una variable importante omitida cuyo efecto se filtra a las demás."},
        {"id": "arpst4-q6", "tipo": "concepto", "enunciado": "¿Qué es un término de interacción y cuándo lo necesitas?", "solucion": "Un término de interacción (X1·X2) se necesita cuando el efecto de un predictor sobre la respuesta DEPENDE del nivel de otro. Ejemplo: el valor del pie cuadrado depende de la zona — en la zona más cara cada pie² suma mucho más que en la más barata. Sin la interacción, el modelo asumiría un efecto único para todas las zonas.", "explicacion": "La interacción captura que la relación entre las variables y la respuesta es interdependiente; ignorarla sesga las predicciones por subgrupo."},
        {"id": "arpst4-q7", "tipo": "concepto", "enunciado": "Menciona maneras de decidir qué términos de interacción incluir en un modelo.", "solucion": "Conocimiento del dominio e intuición; selección stepwise para tamizar modelos; regresión penalizada que ajusta automáticamente un gran conjunto de posibles interacciones; o modelos de árbol (y sus derivados, random forest y gradient boosting) que buscan interacciones óptimas automáticamente.", "explicacion": "Con muchos predictores las interacciones posibles explotan; estas estrategias evitan probarlas todas a mano, y los árboles las descubren por construcción."},
        {"id": "arpst4-q8", "tipo": "concepto", "enunciado": "Distingue un intervalo de confianza de un intervalo de predicción en regresión.", "solucion": "Un intervalo de confianza acota la incertidumbre alrededor de un estadístico, como la respuesta MEDIA predicha para un conjunto de casos. Un intervalo de predicción acota un VALOR INDIVIDUAL futuro. El de predicción es mucho más ancho porque suma la incertidumbre del modelo más la variabilidad irreducible de un dato individual.", "explicacion": "Predecir un caso concreto es más incierto que predecir el promedio de muchos; por eso el intervalo de predicción es siempre más amplio."},
        {"id": "arpst4-q9", "tipo": "concepto", "enunciado": "¿Por qué confundir el intervalo de confianza con el de predicción es peligroso al reportar una predicción individual?", "solucion": "Porque el de confianza (mucho más estrecho) subestima gravemente la incertidumbre real de una predicción individual: daría una falsa sensación de precisión. Para un caso concreto (p.ej. el precio de UNA casa) hay que usar el intervalo de predicción, que incluye la variabilidad del dato individual.", "explicacion": "Reportar el IC para un valor individual oculta el error real; el de predicción comunica honestamente cuánto puede desviarse una predicción puntual."},
        {"id": "arpst4-q10", "tipo": "concepto", "enunciado": "¿Qué son los residuales y por qué son la base del diagnóstico de una regresión?", "solucion": "Los residuales son las diferencias entre los valores observados y los predichos (observado − predicho). Son la base del diagnóstico porque analizarlos permite verificar los supuestos del modelo: detectar outliers, puntos influyentes, varianza no constante (heteroscedasticidad) y predictores faltantes.", "explicacion": "El modelo asume que los residuales son ruido sin estructura; cualquier patrón en ellos revela una violación de supuestos o una variable omitida."},
        {"id": "arpst4-q11", "tipo": "concepto", "enunciado": "¿Qué es un residual estandarizado y cómo lo usas para detectar outliers en regresión?", "solucion": "Es el residual dividido por el error estándar de los residuales; se interpreta como 'número de errores estándar de distancia a la recta de regresión'. Un valor con residual estandarizado grande (p.ej. >3 o 4 en magnitud) se marca como outlier, pues está muy lejos de su valor predicho.", "explicacion": "Estandarizar pone todos los residuales en una escala común comparable, lo que permite un criterio uniforme para flaggear outliers."},
        {"id": "arpst4-q12", "tipo": "concepto", "enunciado": "Diferencia un outlier de un valor influyente (leverage) en regresión.", "solucion": "Un outlier es un registro cuyo valor observado está lejos del predicho (residual grande). Un valor influyente es uno cuya presencia o ausencia cambia notablemente la ecuación de regresión; su grado de influencia se mide con el leverage (hat-value). Un punto puede ser influyente sin tener un residual enorme, y viceversa.", "explicacion": "Influencia ≠ residual grande: un punto en un extremo del eje X puede 'jalar' la recta (alto leverage) aunque caiga cerca de ella; conviene revisar ambos."},
        {"id": "arpst4-q13", "tipo": "concepto", "enunciado": "¿Qué es la heteroscedasticidad y qué suele indicar?", "solucion": "Es cuando la varianza de los residuales no es constante: cambia según el rango de la respuesta o de los predictores (p.ej. los errores crecen para valores grandes). Suele indicar que falta un predictor en la ecuación, o que hace falta una transformación. En ciencia de datos no invalida la predicción, pero es una pista diagnóstica útil.", "explicacion": "Un patrón de embudo en los residuales señala que el modelo captura peor cierta región; a menudo una variable omitida explica esa variabilidad extra."},
        {"id": "arpst4-q14", "tipo": "concepto", "enunciado": "¿Por qué los residuales no normales rara vez preocupan al data scientist, según el libro?", "solucion": "Porque la normalidad de los residuales es un requisito técnico para algunos procedimientos de inferencia formal (intervalos, tests sobre coeficientes), pero en ciencia de datos el foco suele estar en la precisión predictiva, no en la inferencia. Para predecir, residuales no normales generalmente no son un problema.", "explicacion": "El supuesto de normalidad importa para la maquinaria inferencial clásica; cuando el objetivo es predecir bien, pesa mucho menos."},
        {"id": "arpst4-q15", "tipo": "concepto", "enunciado": "¿Por qué la multicolinealidad es menos problemática para árboles, clustering y kNN que para la regresión?", "solucion": "Porque esos métodos no estiman coeficientes lineales que repartan el efecto entre predictores correlacionados; usan particiones, distancias o vecindades. La regresión necesita una solución única para cada coeficiente, que la multicolinealidad vuelve indeterminada o inestable; los métodos no paramétricos no sufren esa indeterminación (aunque la no redundancia sigue siendo deseable).", "explicacion": "El problema de la multicolinealidad es de identificabilidad de coeficientes; donde no hay coeficientes que identificar, deja de ser crítico."}
    ]
}

# ─── Ítems de examen (IDs dinámicos) ──────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        items = bloque['examen']['items']
        nums = [int(it['id'].split('-')[-1]) for it in items]
        last_id = max(nums)
        print(f"Último examen id post-pull: f7-ex-{last_id}")
        next_id1 = last_id + 1
        next_id2 = last_id + 2
        break

ex_next1 = {
    "id": f"f7-ex-{next_id1}",
    "heuristica": "test-permutacion",
    "enunciado": "Tu equipo prueba dos versiones de una landing page de un producto caro y de venta lenta. En 3 semanas reúnes 18 sesiones en A y 12 en B; el tiempo medio de sesión de B supera al de A por 19 segundos. Los tiempos son muy variables y claramente no normales. Un compañero quiere correr un t-test y reportar el p-valor. (a) ¿Por qué el t-test es frágil aquí? (b) ¿qué procedimiento usarías y cuáles son sus pasos? (c) ¿cómo obtienes el p-valor y cómo concluyes?",
    "pistas": [
        "¿Qué supuesto del t-test no se cumple con n pequeño y datos no normales?",
        "Piensa en un método que no asuma ninguna distribución y use solo barajar los datos.",
        "La H0 dice que las páginas no difieren: si fuera cierta, las etiquetas A/B serían intercambiables. ¿Qué pasa si las barajas?",
        "Combina las 30 sesiones, baraja y reparte en grupos de 18 y 12 R veces, calcula la diferencia de medias cada vez → distribución de permutación.",
        "El p-valor es la fracción de permutaciones con diferencia ≥ 19 s; si es alta, la diferencia cabe en el azar; si es pequeña, es significativa."
    ],
    "solucion": "(a) El t-test asume normalidad (o n grande por el CLT); con 18 y 12 sesiones muy variables y no normales, ese supuesto no se sostiene y el p-valor clásico es poco fiable. (b) Un test de permutación: 1) combinar las 30 sesiones en un solo conjunto; 2) barajar y repartir sin reemplazo un grupo de 18 (A) y uno de 12 (B); 3) calcular la diferencia de medias; 4) repetir R≈1000 veces para la distribución de permutación; 5) comparar los 19 s observados con ella. (c) El p-valor es la fracción de permutaciones cuya diferencia iguala o supera los 19 s; si la diferencia observada cae dentro del grueso de la distribución, el azar la explica (no significativa); si cae en la cola (p pequeño), es estadísticamente significativa. Conviene además mirar el tamaño del efecto y la potencia dado el n chico.",
    "disparador": "Señal: 'comparar dos grupos con muestra pequeña y datos no normales'. Jugada: test de permutación (combina→baraja→reparte R veces); p-valor = fracción tan extrema como lo observado.",
    "metadata": {
        "ruta": "ciencia-datos",
        "nivel": 2,
        "skills": ["test de permutación", "remuestreo", "p-valor empírico", "supuestos del t-test"],
        "errores_comunes": ["Aplicar un t-test a muestras pequeñas y no normales sin verificar supuestos", "Confundir el p-valor con la probabilidad de que H0 sea cierta"],
        "casos_borde": ["Con n muy pequeño puede convenir una permutación exhaustiva en vez de aleatoria", "Aun siendo significativo, con n chico la potencia es baja: vigila el tamaño del efecto"],
        "source": "Practical Statistics for Data Scientists (Bruce & Bruce) — Cap. 3"
    }
}

ex_next2 = {
    "id": f"f7-ex-{next_id2}",
    "heuristica": "interpretar-coeficientes-regresion",
    "enunciado": "Ajustas una regresión lineal para predecir el precio de viviendas con metros, número de recámaras y baños, pero SIN ninguna variable de ubicación. Los coeficientes de recámaras y baños salen NEGATIVOS, lo que parece absurdo. El modelo además tiene buen R². (a) ¿Qué fenómeno explica los signos negativos y cómo se llama? (b) ¿cómo lo corriges? (c) si quisieras reportar la incertidumbre del precio de UNA casa concreta, ¿qué intervalo usarías y por qué?",
    "pistas": [
        "¿Hay algún predictor muy importante del precio que dejaste fuera del modelo?",
        "El signo absurdo de un coeficiente suele delatar una variable omitida cuyo efecto se filtra a las demás.",
        "Es confounding (problema de omisión), distinto de la multicolinealidad (problema de comisión); la solución es AÑADIR, no quitar.",
        "Agrega una variable de ubicación (p.ej. grupos de código postal); verás los signos corregirse a valores razonables.",
        "Para una casa individual usa el intervalo de PREDICCIÓN (más ancho), no el de confianza, que solo acota la media."
    ],
    "solucion": "(a) Es confounding (variable confusora): se omitió la ubicación, un predictor clave del precio. Sin ella, recámaras y baños actúan como proxies distorsionados y absorben un efecto que no es suyo, saliendo con signo negativo. (Un buen R² no protege contra esto.) (b) Se corrige AÑADIENDO la variable omitida —por ejemplo, agrupar el código postal en niveles de precio— tras lo cual los coeficientes recuperan signos razonables. Es lo opuesto a la multicolinealidad, que se corrige quitando predictores redundantes. (c) Para el precio de UNA casa concreta se usa el intervalo de predicción, no el de confianza: el de confianza solo acota la respuesta media, mientras el de predicción suma la variabilidad irreducible del dato individual y es mucho más ancho, reflejando la incertidumbre real de una predicción puntual.",
    "disparador": "Señal: 'coeficiente con signo absurdo en regresión'. Jugada: sospecha confounding (variable omitida), añádela; distingue de multicolinealidad; para un caso individual usa intervalo de predicción.",
    "metadata": {
        "ruta": "ciencia-datos",
        "nivel": 3,
        "skills": ["confounding", "interpretación de coeficientes", "multicolinealidad vs omisión", "intervalo de predicción vs confianza"],
        "errores_comunes": ["Confiar en un R² alto e ignorar coeficientes con signo absurdo", "Reportar el intervalo de confianza para una predicción individual"],
        "casos_borde": ["Si la variable omitida correlaciona con varias incluidas, el sesgo se reparte de forma difícil de anticipar", "Añadir la variable puede introducir multicolinealidad si está muy correlacionada con otra ya presente"],
        "source": "Practical Statistics for Data Scientists (Bruce & Bruce) — Cap. 4"
    }
}

# ─── Insertar ─────────────────────────────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        bloque['unidades'].extend(['arena-pst1', 'arena-pst2', 'arena-pst3', 'arena-pst4'])
        bloque['examen']['items'].extend([ex_next1, ex_next2])
        print(f"fase-7: {len(bloque['unidades'])} unidades, {len(bloque['examen']['items'])} examen items")
        break

for u in [unit_pst1, unit_pst2, unit_pst3, unit_pst4]:
    study['unidades'].append(u)
    print(f"Unidad: {u['id']} ({len(u['banco'])}q)")

with open('data/study.json', 'w', encoding='utf-8') as f:
    json.dump(study, f, ensure_ascii=False, indent=2)

print("\n✅ study.json actualizado.")
dupes = {}
for u in study['unidades']:
    for q in u.get('banco', []):
        dupes[q['id']] = dupes.get(q['id'], 0) + 1
bad = [(k, v) for k, v in dupes.items() if v > 1]
print(f"Duplicados banco: {bad or 'ninguno'}")
print(f"Total heurísticas: {len(study['catalogoHeuristicas'])}")
print(f"Examen nuevos: {ex_next1['id']}, {ex_next2['id']}")
