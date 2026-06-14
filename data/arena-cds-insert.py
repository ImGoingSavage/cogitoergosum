"""
Tanda 10: Cracking the Data Science Interview (Gonzalez & Stubberfield) — 60 preguntas, 4 unidades
=================================================================================================
Ruta ciencia-datos (§10). IDs calculados dinámicamente sobre la base integrada.

Se eligen 4 unidades de VALOR NUEVO que complementan (no duplican) Ace DS:
arena-cds1 (feature engineering / preparación de datos), cds2 (deep learning),
cds3 (MLOps / despliegue y monitoreo), cds4 (toolkit práctico: visualización,
storytelling, Git, Bash/pandas).

8 heurísticas nuevas (esquema rico). Reúsa bias-varianza de Ace para DL.
"""

import json

with open('data/study.json', 'r', encoding='utf-8') as f:
    study = json.load(f)

# ─── Heurísticas nuevas ───────────────────────────────────────────────────────
new_heuristicas = [
    {
        "id": "evitar-data-leakage",
        "nombre": "Evitar data leakage",
        "descripcion": "Información ajena al set de entrenamiento se filtra al modelo y vuelve su desempeño falsamente optimista. La regla: divide train/test PRIMERO, ajusta toda transformación solo con train y aplícala al test.",
        "cuando_usar": "Siempre que escales, imputes o codifiques antes de entrenar; sospecha leakage si el test sale 'demasiado bueno' o si una feature conoce el futuro.",
        "ejemplo": "Estandarizar con la media de TODO el dataset (incluido test) antes de dividir → fuga; usa fit_transform en train y transform en test.",
        "patron": "Split → fit en train → transform en test; nunca al revés"
    },
    {
        "id": "imputar-faltantes",
        "nombre": "Imputar datos faltantes según su mecanismo",
        "descripcion": "Antes de rellenar NaN, identifica el mecanismo: MCAR (al azar puro), MAR (depende de variables observadas) o MNAR (depende del valor no observado). El mecanismo decide si borras filas o imputas, y cómo.",
        "cuando_usar": "Ante cualquier dataset con valores faltantes, antes de modelar. Imputar mal introduce sesgo.",
        "ejemplo": "MCAR pocos faltantes → dropna; MAR → imputar moda/media por grupo; MNAR → modelar el faltante con la info disponible.",
        "patron": "MCAR→borrar, MAR→condicional, MNAR→modelar"
    },
    {
        "id": "escalar-features",
        "nombre": "Escalar features (min-max vs z-score)",
        "descripcion": "Algoritmos de distancia (kNN, k-means, jerárquico) y PCA son sensibles a la magnitud; escala para igualar la influencia de cada feature. Min-max lleva a [0,1]; z-score centra en media 0, desv. 1 y resiste outliers.",
        "cuando_usar": "Antes de algoritmos basados en distancia o PCA, o cuando una feature de gran escala domina. Min-max si necesitas rango acotado; z-score si hay outliers.",
        "ejemplo": "Predecir BMI con calorías (1700), edad (50) y pasos (5000): z-score iguala su influencia.",
        "patron": "Distancia/PCA→escala; min-max acotado, z-score robusto"
    },
    {
        "id": "red-neuronal-activacion",
        "nombre": "Elegir la activación de una red neuronal",
        "descripcion": "La no-linealidad de la activación es lo que diferencia una red de un modelo lineal; sin ella, apilar capas colapsa a una transformación lineal. Elige según la posición y la tarea.",
        "cuando_usar": "Al diseñar las capas de una NN: salida binaria → sigmoide; salida multiclase → softmax; capa oculta de red profunda → ReLU.",
        "ejemplo": "Clasificación de imágenes con varias categorías: softmax en la salida (probabilidades que suman 1); ReLU en las ocultas.",
        "patron": "Binaria→sigmoide, multiclase→softmax, oculta→ReLU"
    },
    {
        "id": "gradiente-desvanecido",
        "nombre": "Gradiente que se desvanece o explota",
        "descripcion": "En redes profundas, multiplicar derivadas pequeñas (sigmoide/tanh) capa a capa encoge el gradiente exponencialmente (aprendizaje detenido); derivadas grandes lo hacen explotar (inestabilidad).",
        "cuando_usar": "Cuando una red profunda aprende lentísimo en sus capas tempranas, o la pérdida diverge a NaN. Más severo en RNNs.",
        "ejemplo": "Sustituir sigmoide por ReLU, recortar el gradiente (clipping) e inicializar con Glorot/He.",
        "patron": "Profundo+sigmoide→vanishing; ReLU+clipping+init lo mitiga"
    },
    {
        "id": "containerizar-modelo",
        "nombre": "Contenerizar y desplegar el modelo",
        "descripcion": "Empaca el modelo con sus dependencias y entorno en un contenedor (Docker) para que se comporte igual en testing, staging y producción. Kubernetes orquesta muchos contenedores a escala.",
        "cuando_usar": "Al pasar un modelo de notebook a producción, o cuando 'funciona en mi máquina' pero no en otra. Flask sirve las predicciones por HTTP dentro del contenedor.",
        "ejemplo": "Dockerfile con requirements.txt + app.py Flask; docker build / run; Kubernetes para alta disponibilidad.",
        "patron": "Docker empaca entorno; K8s orquesta el clúster"
    },
    {
        "id": "detectar-data-drift",
        "nombre": "Monitorear y detectar data drift",
        "descripcion": "Tras desplegar, las propiedades estadísticas de la entrada cambian con el tiempo (data drift) y degradan el modelo. Fija un baseline con los datos de entrenamiento y compara la entrada nueva contra él; el drift dispara reentrenamiento.",
        "cuando_usar": "En todo modelo en producción: el trabajo no termina al desplegar. Si la precisión cae sin causa de código, sospecha drift.",
        "ejemplo": "Population Stability Index o divergencia de Jensen-Shannon entre la distribución actual y la del training.",
        "patron": "Baseline de training → comparar entrada → drift → reentrenar"
    },
    {
        "id": "elegir-grafico",
        "nombre": "Elegir el gráfico correcto",
        "descripcion": "El tipo de gráfico debe servir a los datos, la narrativa y la audiencia. Barras comparan categorías; líneas muestran tendencias/series de tiempo; scatter revela correlación; histograma muestra la distribución de una variable.",
        "cuando_usar": "Al comunicar un hallazgo o construir un dashboard. El gráfico equivocado oscurece el mensaje.",
        "ejemplo": "Comparar ventas por categoría → barras; ver correlación entre dos numéricas → scatter; ver sesgo/outliers → histograma.",
        "patron": "Comparar→barras, tendencia→línea, correlación→scatter, distribución→histograma"
    },
    {
        "id": "data-storytelling",
        "nombre": "Data storytelling",
        "descripcion": "Un gráfico aislado no convence: datos + narrativa adaptada a la audiencia mueven a la acción. Conoce a tu audiencia (técnica vs ejecutiva), simplifica a un mensaje por visual y cierra con contexto y recomendación.",
        "cuando_usar": "Al presentar resultados a stakeholders, en portafolios o entrevistas de DS de analytics.",
        "ejemplo": "Para ejecutivos: una barra clara + 'esta región cae 20%, recomiendo reasignar presupuesto', en vez de una tabla cruda.",
        "patron": "Audiencia + gráfico simple + narrativa con recomendación"
    },
]

existing_ids = {h['id'] for h in study['catalogoHeuristicas']}
for h in new_heuristicas:
    if h['id'] not in existing_ids:
        study['catalogoHeuristicas'].append(h)
        print(f"Heurística añadida: {h['id']}")
    else:
        print(f"Heurística ya existe (skip): {h['id']}")

max_ord = max((u.get('orden', 0) for u in study['unidades'] if u.get('bloque') == 'fase-7'), default=0)
print(f"Max orden fase-7 (post-pull): {max_ord}")

# ─── arena-cds1: Feature engineering y preparación de datos ────────────────────
unit_cds1 = {
    "id": "arena-cds1",
    "bloque": "fase-7",
    "orden": max_ord + 1,
    "titulo": "Feature engineering y preparación de datos",
    "libro": "Cracking the Data Science Interview (Gonzalez & Stubberfield)",
    "lectura": "data/teoria/arena-cds1.md",
    "dosis": 30,
    "objetivo": "Construir features sin data leakage, imputar faltantes según su mecanismo, escalar y transformar distribuciones como en una entrevista de DS.",
    "heuristicas": ["evitar-data-leakage", "imputar-faltantes", "escalar-features"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 2},
    "ideas_clave": [
        "Divide train/test ANTES de transformar: ajusta en train, aplica en test",
        "El mecanismo del faltante (MCAR/MAR/MNAR) decide cómo imputar",
        "Escala (min-max o z-score) antes de algoritmos de distancia y PCA"
    ],
    "banco": [
        {"id": "arcds1-q1", "tipo": "concepto", "enunciado": "¿Qué es feature engineering y por qué suele importar más que la elección del algoritmo?", "solucion": "Es seleccionar, transformar y crear representaciones de los datos crudos que capturen los patrones subyacentes que el modelo necesita. Importa más que el algoritmo porque un modelo simple con buenas features supera a uno complejo con features pobres: el algoritmo solo puede explotar la señal que las features le presentan.", "explicacion": "El dominio y la creatividad en construir features amplifican el poder predictivo. La 'basura entra, basura sale' domina sobre la sofisticación del modelo."},
        {"id": "arcds1-q2", "tipo": "concepto", "enunciado": "Define data leakage y explica por qué produce un rendimiento engañosamente optimista.", "solucion": "Data leakage ocurre cuando información ajena al set de entrenamiento se filtra durante la construcción del modelo, permitiéndole 'ver' lo que no debería. Infla la métrica estimada porque el modelo se evalúa con conocimiento que no tendrá en producción, y al desplegarlo el desempeño se desploma.", "explicacion": "El modelo 'hace trampa' al aprender de datos de test. La estimación de desempeño deja de ser válida porque ya no refleja datos verdaderamente no vistos."},
        {"id": "arcds1-q3", "tipo": "concepto", "enunciado": "Vas a estandarizar (z-score) tus features. Describe el orden correcto de pasos para evitar data leakage.", "solucion": "1) Divide en train/test primero. 2) Calcula la media y desviación SOLO con el train (fit). 3) Aplica esa transformación al train (transform) y 4) aplica la MISMA (la del train) al test. Nunca calcules estadísticas usando el test. Encapsular en un Pipeline garantiza el orden.", "explicacion": "Si la media se calcula sobre todo el dataset, el test contamina el train. Ajustar solo con train preserva al test como datos genuinamente no vistos."},
        {"id": "arcds1-q4", "tipo": "concepto", "enunciado": "Distingue los mecanismos MCAR, MAR y MNAR de datos faltantes.", "solucion": "MCAR (Missing Completely At Random): el faltante no depende de ninguna variable. MAR (Missing At Random): depende solo de variables observadas. MNAR (Missing Not At Random): depende del valor faltante mismo (no observado). Identificar el mecanismo es previo a decidir cómo imputar.", "explicacion": "El mecanismo determina si borrar es seguro (MCAR) o introduce sesgo (MNAR). MAR permite imputación condicional usando las variables observadas relacionadas."},
        {"id": "arcds1-q5", "tipo": "concepto", "enunciado": "¿Qué técnica de manejo de faltantes usarías para cada mecanismo y por qué?", "solucion": "MCAR: borrar las filas (dropna) si son pocas, ya que no sesga. MAR: imputación condicional (media/moda por grupo de la variable observada relacionada). MNAR: imputar con la info disponible o modelar explícitamente el patrón de ausencia, pues borrar o imputar ingenuamente sesga.", "explicacion": "Cada mecanismo cambia el riesgo de sesgo: borrar es válido solo bajo MCAR; bajo MAR la imputación condicional aprovecha la estructura; MNAR es el más delicado."},
        {"id": "arcds1-q6", "tipo": "concepto", "enunciado": "¿Por qué hay que escalar las features antes de usar kNN, k-means o PCA?", "solucion": "Estos algoritmos se basan en distancias (o varianza, en PCA), que son sensibles a la magnitud de las features. Una variable en miles domina el cálculo de distancia sobre otra en decenas, sesgando el resultado. Escalar iguala la contribución de cada feature.", "explicacion": "Sin escalar, las features de mayor rango monopolizan la geometría del problema. Escalar pone a todas en un rango comparable para que pesen equitativamente."},
        {"id": "arcds1-q7", "tipo": "calculo", "enunciado": "Da la fórmula del min-max scaling y del z-score scaling, y di a qué rango lleva cada uno.", "solucion": "Min-max: X' = (X − X_min)/(X_max − X_min), lleva al rango [0,1]. Z-score: X' = (X − μ)/σ, centra en media 0 y desviación 1 (típicamente cae entre −3 y 3).", "explicacion": "Min-max reescala a un intervalo fijo; z-score estandariza relativo a la media y la dispersión, sin acotar a un rango fijo."},
        {"id": "arcds1-q8", "tipo": "concepto", "enunciado": "¿Cuándo prefieres z-score sobre min-max scaling?", "solucion": "Cuando hay outliers: el min-max se deja arrastrar por valores extremos (el máximo/mínimo definen el rango), comprimiendo el resto; el z-score, basado en media y desviación, los resiste mejor. También cuando un algoritmo asume datos centrados en 0.", "explicacion": "Un solo outlier extremo distorsiona el min-max (aplasta los demás puntos cerca de 0), mientras el z-score solo lo refleja como un valor grande sin colapsar la escala."},
        {"id": "arcds1-q9", "tipo": "concepto", "enunciado": "¿Para qué sirve una transformación logarítmica y a qué tipo de datos se aplica?", "solucion": "Se aplica a datos sesgados a la derecha (cola larga positiva: ventas, ingresos, tiempos). El log comprime los valores altos y expande los bajos, volviendo la distribución más simétrica para cumplir supuestos de normalidad de muchos modelos.", "explicacion": "Acercar la distribución a la simetría ayuda a modelos que asumen normalidad. Hay que recordar revertir (exponenciar) las predicciones a la escala original."},
        {"id": "arcds1-q10", "tipo": "concepto", "enunciado": "¿Qué es one-hot encoding y cuándo lo usas en vez de codificar categorías como enteros?", "solucion": "One-hot crea una columna binaria por categoría (1 si pertenece, 0 si no). Se usa para variables categóricas nominales (sin orden), porque codificarlas como enteros 1,2,3 impone un orden y magnitud falsos que el modelo interpretaría como relación numérica.", "explicacion": "Asignar enteros a categorías sin orden engaña al modelo (haría 'rojo<verde<azul'). One-hot evita ese orden espurio a costa de más columnas."},
        {"id": "arcds1-q11", "tipo": "concepto", "enunciado": "Un colega aplica StandardScaler a todo el dataset y luego hace train_test_split. ¿Qué problema hay y cómo lo corriges?", "solucion": "Hay data leakage: la media y desviación del scaler se calcularon usando también las filas que terminarán en test, así que el test influyó en la transformación del train. Corrección: primero train_test_split, luego fit_transform del scaler solo en train y transform en test.", "explicacion": "Es el error de leakage más común. La métrica de validación sale optimista porque el preprocesamiento ya 'vio' el test."},
        {"id": "arcds1-q12", "tipo": "concepto", "enunciado": "¿Por qué un Pipeline (p.ej. de scikit-learn) ayuda a prevenir data leakage?", "solucion": "Un Pipeline encadena las transformaciones y el modelo de modo que, al hacer fit, todas las etapas se ajustan SOLO con los datos de entrenamiento, y al hacer transform/predict sobre test aplican esos parámetros sin re-ajustar. Esto hace el preprocesamiento reproducible y evita filtrar estadísticas del test.", "explicacion": "El Pipeline impone el orden correcto automáticamente, especialmente dentro de validación cruzada, donde reajustar por pliegue es crucial para no filtrar."},
        {"id": "arcds1-q13", "tipo": "concepto", "enunciado": "¿Qué problema busca resolver la reducción de dimensionalidad en la preparación de datos?", "solucion": "Reduce el número de features (p.ej. con PCA o selección de features) para combatir la maldición de la dimensionalidad, el overfitting y el costo computacional, conservando la mayor señal posible. Menos features correlacionadas/ruidosas suelen mejorar la generalización.", "explicacion": "Demasiadas features diluyen la señal y disparan la varianza del modelo. Comprimir o seleccionar conserva lo informativo y descarta redundancia y ruido."},
        {"id": "arcds1-q14", "tipo": "concepto", "enunciado": "Tienes una feature 'fecha de cancelación' para predecir si un cliente cancelará. ¿Por qué es un caso peligroso de leakage?", "solucion": "Esa feature solo existe DESPUÉS de que el cliente canceló: conoce el futuro respecto al momento de la predicción. Incluirla daría una accuracy casi perfecta en validación pero inútil en producción, donde no se conoce al predecir. Hay que excluir toda feature que no esté disponible en el instante de la predicción.", "explicacion": "Es leakage temporal: la feature filtra el resultado. La regla práctica es preguntarse '¿tendría este dato en el momento real de predecir?'."},
        {"id": "arcds1-q15", "tipo": "concepto", "enunciado": "¿Cómo decides entre min-max y z-score si no estás seguro cuál conviene?", "solucion": "Considera el contexto: si el algoritmo necesita un rango acotado [0,1] o los datos no tienen outliers, min-max; si hay outliers o el modelo asume datos centrados, z-score. Si la duda persiste, experimenta con ambos y compara el desempeño del modelo en validación.", "explicacion": "No hay regla universal: la elección depende de los datos y del algoritmo. Probar ambos y medir es una respuesta válida y honesta en una entrevista."}
    ]
}

# ─── arena-cds2: Deep learning ────────────────────────────────────────────────
unit_cds2 = {
    "id": "arena-cds2",
    "bloque": "fase-7",
    "orden": max_ord + 2,
    "titulo": "Deep learning: redes neuronales por dentro",
    "libro": "Cracking the Data Science Interview (Gonzalez & Stubberfield)",
    "lectura": "data/teoria/arena-cds2.md",
    "dosis": 30,
    "objetivo": "Explicar pesos, sesgos y activaciones, derivar backpropagation y descenso de gradiente, y diagnosticar el gradiente que se desvanece/explota.",
    "heuristicas": ["red-neuronal-activacion", "gradiente-desvanecido", "bias-varianza"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 3},
    "ideas_clave": [
        "Sin activación no-lineal, apilar capas colapsa a un modelo lineal",
        "Backpropagation usa la regla de la cadena para repartir el error entre pesos",
        "Gradiente que se desvanece: ReLU + gradient clipping + init Glorot/He"
    ],
    "banco": [
        {"id": "arcds2-q1", "tipo": "concepto", "enunciado": "¿Qué hace 'profunda' a una red de deep learning frente a una red neuronal estándar?", "solucion": "La profundidad: una NN estándar tiene una o dos capas ocultas, mientras una de deep learning tiene decenas, cientos o miles. Esa profundidad le permite aprender representaciones jerárquicas (de bordes a formas a objetos) de los datos.", "explicacion": "Cada capa compone representaciones de la anterior; más capas → abstracciones más ricas, ideales para imágenes, voz y lenguaje."},
        {"id": "arcds2-q2", "tipo": "concepto", "enunciado": "Describe los pasos de un forward pass en una sola neurona.", "solucion": "1) Cada entrada se multiplica por su peso. 2) Se suman los productos. 3) Se añade el sesgo (bias). 4) Se aplica la función de activación a ese total. 5) La salida pasa como entrada a la siguiente neurona.", "explicacion": "Es una combinación lineal (pesos·entradas + sesgo) seguida de una no-linealidad. Apilar este bloque muchas veces forma la red."},
        {"id": "arcds2-q3", "tipo": "concepto", "enunciado": "Diferencia el rol de los pesos y los sesgos (biases) en una red neuronal.", "solucion": "Los pesos son valores en las conexiones entre neuronas que dictan la fuerza de la influencia de una neurona sobre otra. Los sesgos son constantes que se suman al total ponderado antes de la activación, permitiendo desplazar la salida y dar flexibilidad (como el intercepto de una recta). Ambos se ajustan durante el entrenamiento.", "explicacion": "Pesos = pendiente de la influencia; sesgo = desplazamiento. Sin sesgo, la neurona estaría forzada a pasar por el origen, limitando lo que puede representar."},
        {"id": "arcds2-q4", "tipo": "concepto", "enunciado": "¿Por qué la función de activación debe ser no-lineal? ¿Qué pasaría sin ella?", "solucion": "La no-linealidad permite a la red capturar patrones complejos que se 'tuercen'. Sin ella, cada capa sería una transformación lineal y la composición de transformaciones lineales sigue siendo lineal: por más capas que apiles, la red equivaldría a un único modelo lineal incapaz de modelar relaciones complejas.", "explicacion": "La no-linealidad es lo que distingue una red profunda de una regresión lineal. Es la fuente de su poder expresivo."},
        {"id": "arcds2-q5", "tipo": "concepto", "enunciado": "Empareja la activación adecuada para: (a) salida de clasificación binaria, (b) salida multiclase, (c) capa oculta de una red profunda.", "solucion": "(a) Sigmoide: aplasta a (0,1), ideal para una probabilidad binaria. (b) Softmax: produce probabilidades que suman 1 sobre las clases. (c) ReLU: estándar en capas ocultas profundas porque mitiga el gradiente que se desvanece.", "explicacion": "Sigmoide/softmax acotan salidas a probabilidades; ReLU mantiene gradientes saludables en profundidad al no saturar en su rama positiva."},
        {"id": "arcds2-q6", "tipo": "concepto", "enunciado": "¿Qué es ReLU, qué ventaja tiene y qué es el problema de la 'dying ReLU'?", "solucion": "ReLU(x)=max(0,x): pasa los positivos sin cambio y manda los negativos a 0. Su ventaja es mitigar el gradiente que se desvanece (su derivada es 1 en positivos, no satura) y es barata de calcular. El problema 'dying ReLU' es que neuronas con entradas siempre negativas quedan atascadas en 0 sin gradiente; Leaky ReLU (pequeña pendiente en negativos) lo evita.", "explicacion": "ReLU domina en redes profundas por su gradiente no saturante, pero puede 'matar' neuronas; sus variantes (Leaky, ELU) lo corrigen."},
        {"id": "arcds2-q7", "tipo": "concepto", "enunciado": "Explica el descenso de gradiente como proceso de entrenamiento de una red.", "solucion": "Hace una predicción, mide qué tan buena es con una función de pérdida, y ajusta ligeramente los pesos en la dirección que reduce esa pérdida; repite muchas iteraciones, mejorando gradualmente. Busca el mínimo de la función de pérdida moviéndose en contra del gradiente.", "explicacion": "El gradiente apunta al ascenso más empinado; restarlo desciende hacia un mínimo. El learning rate controla el tamaño del paso."},
        {"id": "arcds2-q8", "tipo": "concepto", "enunciado": "¿Qué es backpropagation y qué herramienta matemática usa?", "solucion": "Es el algoritmo que entrena redes calculando, capa por capa desde la salida hacia atrás, cuánto contribuyó cada peso y sesgo al error. Usa la regla de la cadena del cálculo para propagar eficientemente los gradientes de la pérdida respecto a cada parámetro.", "explicacion": "Backpropagation provee los gradientes que el descenso de gradiente necesita. La regla de la cadena permite descomponer la derivada a través de muchas capas."},
        {"id": "arcds2-q9", "tipo": "concepto", "enunciado": "Relaciona función de pérdida, backpropagation y descenso de gradiente en el bucle de entrenamiento.", "solucion": "La función de pérdida cuantifica el error entre predicción y objetivo. Backpropagation usa ese error para calcular el gradiente de la pérdida respecto a cada peso (regla de la cadena). El descenso de gradiente usa esos gradientes para actualizar los pesos hacia menor pérdida. Pérdida → backprop (gradientes) → descenso (actualiza) → repetir.", "explicacion": "Son tres engranajes del mismo bucle: medir el error, repartir la culpa entre los pesos, y corregirlos."},
        {"id": "arcds2-q10", "tipo": "concepto", "enunciado": "Describe el problema del gradiente que se desvanece: por qué ocurre y a qué redes afecta más.", "solucion": "Durante backpropagation, los gradientes se multiplican capa a capa por las derivadas de las activaciones. Con sigmoide/tanh esas derivadas son pequeñas (saturan lejos de 0), así que el producto encoge exponencialmente hacia las capas tempranas, que entonces aprenden lentísimo o se detienen. Afecta más a redes muy profundas y a las RNNs (dependencias de largo plazo).", "explicacion": "Multiplicar muchos números <1 tiende a 0. Las primeras capas reciben gradientes diminutos y casi no se actualizan."},
        {"id": "arcds2-q11", "tipo": "concepto", "enunciado": "¿Qué es el gradiente que explota y cómo se mitiga?", "solucion": "Es el opuesto: las derivadas grandes (>1) se multiplican y el gradiente crece exponencialmente, causando actualizaciones enormes, inestabilidad numérica y divergencia (NaN). Se mitiga con gradient clipping (recortar el gradiente por valor o por norma a un umbral) y con una inicialización de pesos cuidadosa.", "explicacion": "El clipping pone un techo al paso de actualización para que no se dispare; junto a una buena inicialización mantiene el entrenamiento estable."},
        {"id": "arcds2-q12", "tipo": "concepto", "enunciado": "¿Qué son las inicializaciones Glorot/Xavier y He, y con qué activaciones se usa cada una?", "solucion": "Ambas inicializan los pesos para que la varianza de las activaciones se mantenga estable a través de las capas, evitando que el gradiente se desvanezca o explote. Glorot/Xavier se usa con tanh, sigmoide y softmax; He se usa con ReLU y sus variantes (ajusta la varianza para la rama positiva de ReLU).", "explicacion": "Una mala inicialización (pesos muy pequeños o grandes) dispara los problemas de gradiente. Glorot y He calculan la escala adecuada según la activación."},
        {"id": "arcds2-q13", "tipo": "concepto", "enunciado": "¿Para qué tipo de datos se usan típicamente las CNN y las RNN?", "solucion": "CNN (convolucionales) para datos con estructura espacial, sobre todo imágenes y visión. RNN (recurrentes) para datos secuenciales y series de tiempo, donde el orden importa; son especialmente propensas al gradiente que se desvanece al capturar dependencias largas.", "explicacion": "Las CNN explotan la localidad espacial con filtros; las RNN mantienen un estado que recorre la secuencia, modelando el contexto temporal."},
        {"id": "arcds2-q14", "tipo": "concepto", "enunciado": "¿Qué es el transfer learning en deep learning y por qué es útil con pocos datos?", "solucion": "Reusar una red pre-entrenada en una tarea grande (p.ej. BERT en lenguaje, o una CNN en ImageNet) y afinarla (fine-tuning) para una tarea nueva relacionada. Es útil con pocos datos porque la red ya aprendió representaciones generales útiles, así que se entrena más rápido y con menos ejemplos que partir de cero.", "explicacion": "Las capas iniciales capturan features genéricas (bordes, sintaxis) transferibles; solo se reajustan las finales para la tarea específica, ahorrando datos y cómputo."},
        {"id": "arcds2-q15", "tipo": "concepto", "enunciado": "Diferencia mínimo local de mínimo global en la optimización de una red, y por qué importa.", "solucion": "Un mínimo local es un punto más bajo que sus vecinos pero no necesariamente el más bajo de todo el espacio; el mínimo global es el punto de menor pérdida absoluta. El descenso de gradiente busca el global pero puede quedar atrapado en uno local. Importa porque la solución hallada puede no ser la óptima.", "explicacion": "En superficies de pérdida no convexas (típicas en deep learning) abundan los mínimos locales y puntos silla; variantes como SGD con momento ayudan a escapar de ellos."}
    ]
}

# ─── arena-cds3: MLOps / despliegue y monitoreo ───────────────────────────────
unit_cds3 = {
    "id": "arena-cds3",
    "bloque": "fase-7",
    "orden": max_ord + 3,
    "titulo": "MLOps: despliegue y monitoreo en producción",
    "libro": "Cracking the Data Science Interview (Gonzalez & Stubberfield)",
    "lectura": "data/teoria/arena-cds3.md",
    "dosis": 30,
    "objetivo": "Llevar un modelo a producción: pipelines reproducibles, contenedores (Docker/K8s), validación, monitoreo y detección de data drift.",
    "heuristicas": ["containerizar-modelo", "detectar-data-drift"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 3},
    "ideas_clave": [
        "Docker empaca modelo + dependencias para consistencia entre entornos; K8s orquesta a escala",
        "El trabajo no termina al desplegar: hay que validar y monitorear",
        "Data drift: comparar la entrada contra un baseline de training; dispara reentrenamiento"
    ],
    "banco": [
        {"id": "arcds3-q1", "tipo": "concepto", "enunciado": "¿Qué es MLOps y qué problema resuelve?", "solucion": "MLOps mezcla los principios de DevOps con la ciencia de datos para gestionar todo el ciclo de vida del modelo: ingesta de datos, desarrollo, prueba, despliegue, monitoreo y mejora continua. Resuelve el problema de operacionalizar y mantener en producción los modelos, que de otro modo se quedan en un notebook sin generar valor.", "explicacion": "Es el puente entre el mundo del DS y el de operaciones de IT, asegurando que el modelo funcione y se mantenga de forma confiable en producción."},
        {"id": "arcds3-q2", "tipo": "concepto", "enunciado": "Nombra tres virtudes de un pipeline de modelo reproducible y automatizado.", "solucion": "Automatización (de prototipo a producción rápido, sin pasos manuales), consistencia (los mismos pasos cada vez reducen errores) y reproducibilidad (cada paso queda registrado, clave para auditoría y cumplimiento en industrias reguladas).", "explicacion": "El pipeline es el backbone de MLOps: convierte un proceso artesanal y frágil en uno repetible, fiable y documentado."},
        {"id": "arcds3-q3", "tipo": "concepto", "enunciado": "¿Qué es un contenedor y por qué es central para desplegar modelos de ML?", "solucion": "Un contenedor empaca el modelo junto con sus dependencias, librerías y entorno de ejecución en una unidad ligera y portátil. Es central porque garantiza que el modelo se comporte igual sin importar el entorno (testing, staging, producción), eliminando el problema de 'funciona en mi máquina' y estandarizando el entorno para todo el equipo.", "explicacion": "La encapsulación del entorno hace el despliegue consistente y portable, base de la colaboración y la reproducibilidad en MLOps."},
        {"id": "arcds3-q4", "tipo": "concepto", "enunciado": "¿Qué es Docker y qué define un Dockerfile?", "solucion": "Docker es la herramienta de contenerización más usada en MLOps. Un Dockerfile es una lista de instrucciones para construir la imagen: la imagen base (p.ej. Python), copiar archivos, instalar dependencias (pip install -r requirements.txt), exponer un puerto (EXPOSE) y el comando a ejecutar al arrancar (CMD, p.ej. python app.py).", "explicacion": "El Dockerfile es la receta declarativa del entorno; docker build crea la imagen y docker run levanta el contenedor que sirve el modelo."},
        {"id": "arcds3-q5", "tipo": "concepto", "enunciado": "¿Qué diferencia hay entre Docker y Kubernetes en un pipeline de MLOps?", "solucion": "Docker crea y corre contenedores individuales (empaca un modelo y su entorno). Kubernetes es un orquestador: gestiona la automatización y el despliegue de muchos contenedores a través de un clúster de máquinas, para escalabilidad y alta disponibilidad. Docker empaca; Kubernetes coordina muchos a escala.", "explicacion": "Para una app simple basta Docker; cuando necesitas escalar, balancear carga y tolerancia a fallos entre muchos contenedores, entra Kubernetes."},
        {"id": "arcds3-q6", "tipo": "concepto", "enunciado": "Tras desplegar un modelo, ¿cómo validas que funciona como se espera?", "solucion": "Conectas al endpoint del modelo desplegado, le envías datos preferiblemente NO vistos durante el entrenamiento, recoges las predicciones y las puntúas. Esto confirma dos cosas: que el despliegue funciona (devuelve resultados) y que el desempeño sobre datos frescos es el esperado, evitando sorpresas en producción.", "explicacion": "Es una verificación rápida post-despliegue: prueba la plomería (que responda) y la calidad (que prediga bien sobre datos nuevos)."},
        {"id": "arcds3-q7", "tipo": "concepto", "enunciado": "¿Qué es el logging en un modelo en producción y para qué sirve?", "solucion": "Logging es registrar los eventos y actividades del modelo: cada interacción, entrada y decisión. Sirve como registro histórico para rastrear qué pasó cuando surgen problemas (depuración y troubleshooting) y como base para monitorear el modelo y sus métricas en el tiempo.", "explicacion": "Sin logs operas a ciegas. Son la herramienta de detective para diagnosticar caídas de desempeño y entender el comportamiento real del modelo."},
        {"id": "arcds3-q8", "tipo": "concepto", "enunciado": "¿Qué es data drift y por qué degrada un modelo en producción?", "solucion": "Data drift ocurre cuando las propiedades estadísticas de los datos de entrada cambian con el tiempo (cambia el comportamiento del usuario, el mercado, el mundo) respecto a los datos con que se entrenó. Degrada el modelo porque éste aprendió patrones de una distribución que ya no coincide con la que recibe, así que sus predicciones pierden precisión.", "explicacion": "El modelo asume que producción se parece al training; cuando la entrada deriva, esa suposición se rompe y el desempeño cae aunque el código no cambie."},
        {"id": "arcds3-q9", "tipo": "concepto", "enunciado": "¿Cómo se detecta el data drift en la práctica?", "solucion": "Se fija un baseline con la distribución de los datos de entrenamiento como referencia, y se compara regularmente la distribución de los datos entrantes contra ese baseline usando tests estadísticos como el Population Stability Index (PSI), la divergencia de Jensen-Shannon o estadísticas simples por feature. Una desviación significativa señala drift.", "explicacion": "Comparar distribuciones (training vs producción) cuantifica cuánto ha cambiado la entrada; superar un umbral dispara una alerta y posible reentrenamiento."},
        {"id": "arcds3-q10", "tipo": "concepto", "enunciado": "Detectas data drift en tu modelo. ¿Cuál es la respuesta típica y por qué es 'fácil' bajo MLOps?", "solucion": "La respuesta típica es reentrenar el modelo con datos recientes que reflejen la nueva distribución. Bajo MLOps es relativamente fácil porque la mayor parte del proceso (ingesta, preparación, entrenamiento, despliegue) ya está codificada y automatizada en el pipeline, así que reentrenar es re-ejecutar un flujo existente, no rehacerlo a mano.", "explicacion": "El valor de automatizar el pipeline se cobra justo aquí: el reentrenamiento ante drift se vuelve rutinario en lugar de un proyecto manual."},
        {"id": "arcds3-q11", "tipo": "concepto", "enunciado": "¿Qué métricas, además de la precisión del modelo, conviene monitorear en producción?", "solucion": "Tiempos de respuesta (latencia), uso de recursos (CPU/memoria), throughput, y la distribución de los datos de entrada (para detectar drift). También alertas ante caídas súbitas de cualquier métrica. El monitoreo de salud operacional importa tanto como la precisión.", "explicacion": "Un modelo preciso pero lento o que consume demasiados recursos también falla en producción; el monitoreo cubre desempeño predictivo y operacional."},
        {"id": "arcds3-q12", "tipo": "concepto", "enunciado": "¿Qué son ETL y ELT en la ingesta de datos y en qué se diferencian?", "solucion": "Ambos son pipelines para mover datos. ETL (Extract-Transform-Load) transforma los datos antes de cargarlos al destino; ELT (Extract-Load-Transform) los carga crudos primero y transforma dentro del destino (aprovechando su poder de cómputo, p.ej. un data warehouse). Se ejecutan en procesos batch (lotes) o streaming (continuo).", "explicacion": "La diferencia es el orden de transformar vs cargar. ELT es común con almacenes modernos escalables que transforman in situ; ETL, cuando se transforma antes de cargar."},
        {"id": "arcds3-q13", "tipo": "concepto", "enunciado": "¿Para qué se usa Flask en el despliegue de un modelo dentro de un contenedor?", "solucion": "Flask (un microframework web de Python) construye una API que expone el modelo: el app.py recibe datos de entrada por HTTP (p.ej. un POST a /predict), los pasa al modelo entrenado y devuelve la predicción como respuesta. Empaquetado en el contenedor Docker, hace el modelo accesible como un servicio web.", "explicacion": "Flask convierte el modelo en un endpoint que otras aplicaciones pueden consumir; el contenedor lo hace portable y desplegable de forma consistente."},
        {"id": "arcds3-q14", "tipo": "concepto", "enunciado": "¿Por qué la gobernanza (model governance) es parte de MLOps, especialmente en salud y finanzas?", "solucion": "La gobernanza rastrea y gestiona versiones de modelos y datos, documenta el diseño y desempeño, y asegura el cumplimiento regulatorio. En salud y finanzas los requisitos son estrictos: los reguladores exigen trazabilidad completa del proceso de desarrollo del modelo y de las decisiones que toma, por lo que el versionado y la documentación son obligatorios.", "explicacion": "Sin gobernanza no hay auditoría ni cumplimiento; en industrias reguladas un modelo sin trazabilidad es inutilizable por más preciso que sea."},
        {"id": "arcds3-q15", "tipo": "concepto", "enunciado": "Resume el ciclo completo de un modelo bajo MLOps, de los datos a producción.", "solucion": "Ingesta de datos (ETL/ELT, batch/streaming) → preparación y feature engineering → entrenamiento y validación del modelo → empaquetado en contenedor (Docker) → despliegue (orquestado por Kubernetes a escala, servido vía Flask) → validación post-despliegue con datos no vistos → monitoreo continuo (logging, métricas, data drift) → reentrenamiento ante drift, todo bajo gobernanza. Es un ciclo, no una línea recta.", "explicacion": "MLOps cierra el lazo: el monitoreo retroalimenta el reentrenamiento, manteniendo el modelo vigente frente a un mundo que cambia."}
    ]
}

# ─── arena-cds4: Toolkit práctico ─────────────────────────────────────────────
unit_cds4 = {
    "id": "arena-cds4",
    "bloque": "fase-7",
    "orden": max_ord + 4,
    "titulo": "Toolkit práctico: visualización, storytelling y Git",
    "libro": "Cracking the Data Science Interview (Gonzalez & Stubberfield)",
    "lectura": "data/teoria/arena-cds4.md",
    "dosis": 30,
    "objetivo": "Elegir el gráfico correcto, contar historias con datos para una audiencia, y manejar control de versiones con Git y el flujo de shell del día a día.",
    "heuristicas": ["elegir-grafico", "data-storytelling"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 1},
    "ideas_clave": [
        "El gráfico debe servir a los datos, la narrativa y la audiencia",
        "Datos + narrativa con recomendación mueven a la acción; un gráfico solo no",
        "Flujo Git mínimo: init/clone → add → commit → push; git log para la historia"
    ],
    "banco": [
        {"id": "arcds4-q1", "tipo": "concepto", "enunciado": "¿Qué tres cosas debe servir un buen gráfico, según el marco de storytelling?", "solucion": "Los datos (su naturaleza y estructura), la narrativa (el mensaje que quieres transmitir) y la audiencia (su nivel técnico y qué necesita entender). Elegir el gráfico equivocado para cualquiera de los tres oscurece el mensaje.", "explicacion": "La fuerza de una visualización está en su adecuación: el mismo dato puede pedir gráficos distintos según qué historia cuentas y a quién."},
        {"id": "arcds4-q2", "tipo": "concepto", "enunciado": "¿Cuándo usas un gráfico de barras y qué buena práctica evita malinterpretarlo?", "solucion": "Barras para comparar cantidades entre categorías (o pocas categorías a lo largo del tiempo) y mostrar proporciones relativas. Buena práctica: empezar el eje Y en cero para no exagerar las diferencias; usar barras horizontales si las etiquetas son largas o hay muchas categorías.", "explicacion": "Truncar el eje Y infla visualmente diferencias pequeñas, una distorsión común; arrancar en cero preserva la proporción real."},
        {"id": "arcds4-q3", "tipo": "concepto", "enunciado": "¿Para qué sirve un gráfico de líneas y cuál es su variante de serie de tiempo?", "solucion": "Las líneas muestran tendencias o la relación entre dos variables numéricas conectando puntos. La variante de serie de tiempo pone el tiempo (minutos, días, años) en el eje X para mostrar cómo cambia una variable a lo largo del tiempo. Consejo: pocas líneas y marcadores en los puntos para legibilidad.", "explicacion": "La línea enfatiza la continuidad y la dirección del cambio; con el tiempo en X se vuelve la herramienta natural para tendencias temporales."},
        {"id": "arcds4-q4", "tipo": "concepto", "enunciado": "¿Cuándo eliges un scatter plot y qué le puedes añadir para reforzar el mensaje?", "solucion": "Scatter para mostrar la relación o correlación entre dos variables cuantitativas (o su ausencia), y la distribución conjunta de los datos. Puedes añadir una línea de tendencia para visualizar la relación global y usar colores/formas por categoría, lo que a veces revela segmentos naturales no conocidos.", "explicacion": "El scatter es el precursor de la línea cuando se confirma un patrón; colorear por grupo puede descubrir estructura latente en la nube de puntos."},
        {"id": "arcds4-q5", "tipo": "concepto", "enunciado": "¿Qué muestra un histograma y por qué el tamaño del bin es crítico?", "solucion": "Un histograma muestra la distribución de una variable numérica: barras adyacentes cuyo alto es la frecuencia de valores en cada rango (bin). Permite ver sesgo (skewness), kurtosis y outliers. El tamaño del bin es crítico porque cambia drásticamente la forma percibida: bins muy anchos ocultan detalle; muy estrechos generan ruido.", "explicacion": "Un mismo dato con bins distintos cuenta historias distintas; conviene experimentar con varios tamaños para hallar el que mejor representa la distribución."},
        {"id": "arcds4-q6", "tipo": "concepto", "enunciado": "Empareja el gráfico con el objetivo: (a) comparar ventas por categoría, (b) ver la evolución del precio de una acción, (c) ver si dos variables correlacionan, (d) ver la distribución y outliers de una variable.", "solucion": "(a) Barras. (b) Línea / serie de tiempo. (c) Scatter plot (con línea de tendencia). (d) Histograma (o density plot).", "explicacion": "Cada tarea tiene un gráfico canónico: comparación→barras, tendencia temporal→línea, relación→scatter, distribución→histograma."},
        {"id": "arcds4-q7", "tipo": "concepto", "enunciado": "¿Por qué un buen gráfico por sí solo no basta y qué añade el data storytelling?", "solucion": "Un gráfico aislado muestra datos pero no necesariamente convence ni mueve a la acción. El storytelling añade una narrativa: contexto, el mensaje clave y una recomendación, adaptados a la audiencia. Datos + narrativa se vuelven una herramienta persuasiva que un gráfico crudo no logra.", "explicacion": "Los stakeholders deciden con historias, no con tablas; enmarcar el dato en un relato con conclusión clara es lo que produce impacto."},
        {"id": "arcds4-q8", "tipo": "concepto", "enunciado": "Vas a presentar resultados a una audiencia ejecutiva (no técnica). ¿Cómo adaptas tu visualización y narrativa?", "solucion": "Simplifica: un mensaje claro por visual, sin jerga ni detalle técnico innecesario; usa gráficos directos (barras/líneas) y destaca el insight y la recomendación de negocio, no la metodología. Conoce a tu audiencia y mantén la conexión con la meta de negocio al frente.", "explicacion": "La audiencia ejecutiva quiere el 'y qué' y la acción; sobrecargar con técnica diluye el mensaje. Adaptar el nivel es parte central del storytelling."},
        {"id": "arcds4-q9", "tipo": "concepto", "enunciado": "Describe el flujo mínimo de Git para guardar tu trabajo en un repositorio local, en orden.", "solucion": "1) git init (crea el repo en el directorio) o git clone <url> (copia uno remoto). 2) Crea/edita archivos. 3) git add . (mueve los cambios al staging area). 4) git commit -m \"mensaje\" (confirma los cambios al repositorio con un mensaje descriptivo).", "explicacion": "init → add → commit es el ciclo básico: el staging area separa lo que vas a confirmar; el mensaje de commit es permanente, conviene que sea claro."},
        {"id": "arcds4-q10", "tipo": "concepto", "enunciado": "¿Qué es el staging area en Git y cómo deshaces un archivo que agregaste por error?", "solucion": "El staging area es la zona intermedia donde se colocan los cambios (con git add) antes de confirmarlos en un commit; te permite elegir qué entra en el próximo commit. Para sacar un archivo del staging sin perder sus modificaciones en el directorio de trabajo: git reset HEAD <archivo>.", "explicacion": "El staging da control fino sobre qué confirmas. reset HEAD desindexa sin tocar tu trabajo; útil cuando agregaste algo que no quieres en ese commit."},
        {"id": "arcds4-q11", "tipo": "concepto", "enunciado": "¿Cómo enlazas un repositorio local con uno remoto en GitHub y subes tus cambios?", "solucion": "git remote add origin <url> vincula el repo local con el remoto; luego git push -u origin master (o main) sube los commits al remoto, sirviendo de backup y permitiendo colaborar. Después, git pull baja los cambios que otros suban.", "explicacion": "remote add registra la URL destino; push sincroniza tu trabajo hacia GitHub. Conviene no inicializar el repo remoto con README/.gitignore si vas a empujar uno local (evita conflictos)."},
        {"id": "arcds4-q12", "tipo": "concepto", "enunciado": "Menciona tres formas de inspeccionar la historia de un proyecto con git log.", "solucion": "git log -3 archivo.py (los últimos 3 commits de ese archivo), git log --since YYYY-MM-DD (commits desde una fecha), git log --author=<nombre> (todos los commits de un autor). Para descubrir más flags de cualquier comando: git <comando> --help.", "explicacion": "git log con flags filtra la historia por archivo, fecha o autor, esencial para auditar quién cambió qué y cuándo en un proyecto colaborativo."},
        {"id": "arcds4-q13", "tipo": "concepto", "enunciado": "¿Qué papel juega pandas en el flujo de trabajo de un data scientist?", "solucion": "Pandas es la librería central de Python para manipular datos tabulares: leer archivos (read_csv), estructurar en DataFrames, filtrar, agrupar (groupby), unir (merge), detectar faltantes (isnull().sum()) y transformar. Es la base sobre la que se hace la limpieza y el feature engineering antes de modelar.", "explicacion": "Casi toda preparación de datos en Python pasa por pandas; dominarlo es prerrequisito tácito en una entrevista de DS."},
        {"id": "arcds4-q14", "tipo": "concepto", "enunciado": "¿Para qué sirve Bash/shell en el día a día de un data scientist?", "solucion": "Bash es el 'pegamento' del flujo: navegar el sistema de archivos (cd, ls), mover/copiar datos, lanzar scripts (python app.py), encadenar comandos con pipes y automatizar tareas repetitivas. En MLOps los comandos de Docker (docker build, docker run) se ejecutan desde el shell.", "explicacion": "Muchas tareas de datos y despliegue viven en la terminal; el shell automatiza y conecta herramientas sin escribir un programa completo."},
        {"id": "arcds4-q15", "tipo": "concepto", "enunciado": "Al crear un repo nuevo en GitHub para subir un proyecto local existente, ¿por qué conviene NO inicializarlo con README/.gitignore/License?", "solucion": "Porque esos archivos crean commits en el remoto que tu repo local no tiene, provocando conflictos (rechazo del push o un historial divergente) al hacer el primer push. Es más limpio crear el remoto vacío, hacer push del local, y añadir README/.gitignore después.", "explicacion": "Un remoto con commits previos y un local con su propia historia divergen; empezar el remoto vacío evita tener que reconciliar historias en el primer push."}
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
    "heuristica": "evitar-data-leakage",
    "enunciado": "Un compañero entrena un clasificador de churn. Reporta 97% de AUC en validación y quiere desplegarlo. Revisando su código ves: (1) estandariza todas las features con StandardScaler sobre el dataset completo y luego hace train_test_split; (2) entre sus features está 'días_desde_última_factura', que incluye facturas posteriores a la fecha de corte. (a) ¿Qué dos formas de data leakage hay? (b) ¿cómo corriges cada una? (c) ¿qué esperas que pase con el AUC tras corregir?",
    "pistas": [
        "¿En qué orden se deben hacer el split y el escalado?",
        "¿La feature 'días_desde_última_factura' estaría disponible en el momento real de predecir churn?",
        "Una fuga es de preprocesamiento (el scaler vio el test); la otra es temporal (una feature conoce el futuro).",
        "Corrige: split primero, fit del scaler solo en train; y elimina (o recalcula con corte temporal) la feature que filtra el futuro.",
        "El AUC bajará al corregir, porque el 97% estaba inflado por la fuga; el nuevo número es el desempeño real esperado en producción."
    ],
    "solucion": "(a) Leakage de preprocesamiento: estandarizar sobre todo el dataset antes de dividir hace que la media/desviación del scaler incluyan filas del test, contaminando el train. Leakage temporal: 'días_desde_última_factura' usa facturas posteriores al corte, info que no existe al momento de predecir. (b) Primero train_test_split, luego fit_transform del scaler solo en train y transform en test (idealmente dentro de un Pipeline); y eliminar o recalcular la feature usando solo datos anteriores a la fecha de predicción. (c) El AUC caerá: el 97% era optimista por la fuga; el valor corregido refleja el desempeño real en producción.",
    "disparador": "Señal: 'métrica de validación sospechosamente alta' o 'transformé antes de dividir'. Jugada: revisa orden split→fit, y busca features que conozcan el futuro.",
    "metadata": {
        "ruta": "ciencia-datos",
        "nivel": 3,
        "skills": ["data leakage", "orden split/transform", "leakage temporal", "Pipeline reproducible"],
        "errores_comunes": ["Escalar o imputar sobre el dataset completo antes del split", "Incluir features que solo existen después del evento a predecir"],
        "casos_borde": ["En validación cruzada hay que reajustar el preprocesamiento por pliegue, no una vez global", "Algunas fugas son sutiles: IDs ordenados por tiempo, agregados que incluyen el target"],
        "source": "Cracking the Data Science Interview (Gonzalez & Stubberfield) — Cap. 9"
    }
}

ex_next2 = {
    "id": f"f7-ex-{next_id2}",
    "heuristica": "detectar-data-drift",
    "enunciado": "Un modelo de recomendación lleva 8 meses en producción con buen desempeño, pero las últimas semanas la precisión cae sin que nadie haya tocado el código ni el pipeline. (a) ¿Cuál es la causa más probable y cómo la confirmarías? (b) ¿qué herramienta de monitoreo debió estar en su lugar? (c) ¿cuál es la respuesta una vez confirmada y por qué es manejable bajo MLOps?",
    "pistas": [
        "Si el código no cambió pero el desempeño cae, ¿qué pudo cambiar en su lugar?",
        "Piensa en cómo evoluciona el comportamiento de los usuarios o el catálogo con el tiempo.",
        "Compara la distribución de los datos de entrada de hoy contra la de entrenamiento.",
        "Es data drift: confírmalo con un baseline de training y tests como PSI o divergencia de Jensen-Shannon sobre las features de entrada.",
        "La respuesta es reentrenar con datos recientes; es manejable porque el pipeline (ingesta→entrenamiento→despliegue) ya está automatizado."
    ],
    "solucion": "(a) La causa más probable es data drift: las propiedades estadísticas de la entrada cambiaron con el tiempo (nuevos usuarios, cambios de gustos, catálogo distinto) y ya no coinciden con la distribución de entrenamiento. Se confirma fijando un baseline con los datos de training y comparando la distribución entrante contra él. (b) Monitoreo de drift: comparación continua de distribuciones con Population Stability Index o divergencia de Jensen-Shannon, más logging y alertas de métricas. (c) Reentrenar el modelo con datos recientes; es manejable porque bajo MLOps el pipeline está codificado y automatizado, así que reentrenar es re-ejecutar el flujo, no rehacerlo a mano.",
    "disparador": "Señal: 'el desempeño cae en producción sin cambios de código'. Jugada: sospecha data drift; compara entrada vs baseline de training (PSI/JS) y reentrena.",
    "metadata": {
        "ruta": "ciencia-datos",
        "nivel": 3,
        "skills": ["data drift", "monitoreo en producción", "PSI / Jensen-Shannon", "reentrenamiento automatizado"],
        "errores_comunes": ["Asumir que un modelo desplegado se mantiene válido para siempre", "No instrumentar monitoreo de distribución de entrada"],
        "casos_borde": ["Concept drift (cambia la relación X→y, no solo la distribución de X) requiere diagnóstico distinto", "Una caída por un bug de pipeline o de datos de upstream imita al drift; el logging ayuda a distinguir"],
        "source": "Cracking the Data Science Interview (Gonzalez & Stubberfield) — Cap. 12"
    }
}

# ─── Insertar ─────────────────────────────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        bloque['unidades'].extend(['arena-cds1', 'arena-cds2', 'arena-cds3', 'arena-cds4'])
        bloque['examen']['items'].extend([ex_next1, ex_next2])
        print(f"fase-7: {len(bloque['unidades'])} unidades, {len(bloque['examen']['items'])} examen items")
        break

for u in [unit_cds1, unit_cds2, unit_cds3, unit_cds4]:
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
