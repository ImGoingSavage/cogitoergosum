"""
Tanda 12: Designing Machine Learning Systems (Chip Huyen) — 60 preguntas, 4 unidades
====================================================================================
Ruta ml-systems (§10). IDs calculados dinámicamente sobre la base integrada.

4 unidades de VALOR NUEVO (diseño de sistemas de ML end-to-end; complementa el
MLOps básico de Cracking cds3 sin duplicarlo):
arena-dmls1 (encuadre de problemas de ML: objetivos y tipos de tarea),
arena-dmls2 (datos de entrenamiento: muestreo, etiquetas, desbalance),
arena-dmls3 (despliegue y predicción: batch vs online, compresión, edge),
arena-dmls4 (cambios de distribución, monitoreo y test en producción).

9 heurísticas nuevas (esquema rico). Reúsa detectar-data-drift (de Cracking) y
diseno-experimento-ab (de Ace).
"""

import json

with open('data/study.json', 'r', encoding='utf-8') as f:
    study = json.load(f)

# ─── Heurísticas nuevas ───────────────────────────────────────────────────────
new_heuristicas = [
    {
        "id": "encuadrar-objetivo-ml",
        "nombre": "Atar el objetivo de ML al de negocio y desacoplar",
        "descripcion": "Un modelo solo sobrevive si su métrica de ML se mapea a una métrica de negocio. Si hay objetivos en conflicto, entrena un modelo por objetivo y combínalos al rankear, en vez de meterlos en una sola loss ponderada que exija reentrenar para reajustar prioridades.",
        "cuando_usar": "Al arrancar un proyecto de ML (¿mueve una métrica de negocio?) o cuando el sistema persigue metas que compiten (engagement vs calidad).",
        "ejemplo": "Engagement y calidad del feed: un modelo para cada uno y combinas sus scores; reajustar la prioridad no exige reentrenar.",
        "patron": "ML→métrica de negocio; objetivos en conflicto→desacoplar modelos"
    },
    {
        "id": "elegir-tipo-tarea-ml",
        "nombre": "Elegir el encuadre de la tarea de ML",
        "descripcion": "El mismo problema admite varios encuadres y cada uno tiene consecuencias de mantenimiento. Distingue binaria/multiclase/multietiqueta (un ejemplo con varias clases es multilabel), y considera reformular clasificación↔regresión/ranking para no tener que reentrenar al añadir categorías.",
        "cuando_usar": "Al definir la salida del modelo, sobre todo si el número de clases puede crecer o un ejemplo puede pertenecer a varias categorías.",
        "ejemplo": "Predecir 'qué app abre el usuario' como ranking por par usuario-app: añadir apps no obliga a reentrenar (vs clasificación con una salida por app).",
        "patron": "binaria/multiclase/multilabel; clasificación vs ranking"
    },
    {
        "id": "muestreo-streaming",
        "nombre": "Muestrear de streams y de distribuciones difíciles",
        "descripcion": "Para muestrear k elementos con igual probabilidad de un stream de tamaño desconocido usa reservoir sampling; para muestrear de una distribución cara o imposible P(x), usa otra Q(x) fácil y repondera por P(x)/Q(x) (importance sampling). Estratifica para no perder grupos raros.",
        "cuando_usar": "Datos en streaming que no caben en memoria (reservoir), o cuando la distribución objetivo es inaccesible y tienes una proposal más barata (importance).",
        "ejemplo": "Muestrear k tweets de un stream infinito: reservorio de k, y reemplazar el i-ésimo con probabilidad k/n.",
        "patron": "stream→reservoir; distribución cara→importance (P/Q); raros→estratificar"
    },
    {
        "id": "usar-natural-labels",
        "nombre": "Aprovechar natural labels y supervisión débil",
        "descripcion": "Antes de etiquetar a mano (caro, lento, discrepante), busca natural labels que el sistema infiera del comportamiento (clics, compras) y vigila su feedback-loop length; o genera etiquetas con weak supervision (labeling functions ruidosas pero escalables) y pide a etiquetar solo los ejemplos más informativos (active learning).",
        "cuando_usar": "Cuando etiquetar a mano es el cuello de botella, o cuando el sistema puede inferir la verdad del comportamiento del usuario.",
        "ejemplo": "Un recomendador usa el clic (o su ausencia) como etiqueta implícita; Snorkel combina reglas como labeling functions.",
        "patron": "natural labels>hand labels; weak supervision; active learning"
    },
    {
        "id": "manejar-desbalance-clases",
        "nombre": "Manejar el desbalance de clases",
        "descripcion": "Cuando una clase domina, la accuracy engaña (predecir siempre la mayoritaria 'acierta' casi siempre). Cambia a métricas adecuadas (F1, precision/recall, AUC) y aplica resampling (oversample la minoría tipo SMOTE, o undersample la mayoría) o una loss ponderada por coste.",
        "cuando_usar": "Detección de fraude/enfermedades raras/anomalías, o siempre que una clase sea una fracción ínfima del total.",
        "ejemplo": "Fraude 0.1%: un clasificador trivial logra 99.9% de accuracy y es inútil; mide AUC y sobremuestrea la clase fraude.",
        "patron": "clase rara→F1/AUC + resampling/weighted loss, NO accuracy"
    },
    {
        "id": "elegir-batch-vs-online",
        "nombre": "Elegir batch vs online prediction",
        "descripcion": "Batch prediction precomputa y guarda predicciones por adelantado (rápido de servir, pero pueden quedar rancias y desperdiciarse); online prediction predice on-demand con datos frescos, a costa de pelear contra la latencia y a menudo necesitar streaming features.",
        "cuando_usar": "Al diseñar el servicio de predicción: batch si no necesitas frescura inmediata y el volumen es alto; online si el input no se conoce de antemano o los datos frescos importan.",
        "ejemplo": "Recomendaciones precomputadas de noche (batch) vs pricing dinámico al instante de la petición (online).",
        "patron": "sin frescura→batch precomputado; datos frescos/on-demand→online"
    },
    {
        "id": "comprimir-modelo",
        "nombre": "Comprimir un modelo para servir",
        "descripcion": "Para que un modelo grande corra rápido o en hardware limitado, comprímelo: low-rank factorization, knowledge distillation (un student pequeño imita a un teacher grande, p.ej. DistilBERT), pruning (elimina parámetros poco útiles) y quantization (representar con menos bits, de 32 a 16/8).",
        "cuando_usar": "Cuando la inferencia es demasiado lenta/grande, o para desplegar en el edge (móvil/IoT) con recursos limitados.",
        "ejemplo": "DistilBERT: un student destila a BERT conservando ~el rendimiento a una fracción del tamaño; quantization baja a int8.",
        "patron": "modelo grande→distillation/quantization/pruning/low-rank"
    },
    {
        "id": "diagnosticar-distribution-shift",
        "nombre": "Diagnosticar el tipo de distribution shift",
        "descripcion": "Cuando un modelo se degrada en producción, identifica el tipo de shift partiendo de P(X,Y): covariate shift (cambia P(X), igual P(Y|X)), label shift (cambia P(Y), igual P(X|Y)) o concept drift (cambia P(Y|X), la relación misma — el más peligroso). Detéctalo con two-sample tests contra una referencia.",
        "cuando_usar": "Ante caída de desempeño en producción, o al diseñar el monitoreo de un modelo desplegado.",
        "ejemplo": "Llegan más usuarios jóvenes pero edad→compra es igual: covariate shift; 'caro' que pasa a 'normal': concept drift.",
        "patron": "P(X)→covariate; P(Y)→label; P(Y|X)→concept drift; detecta con two-sample test"
    },
    {
        "id": "test-en-produccion",
        "nombre": "Probar modelos en producción con bajo riesgo",
        "descripcion": "Evaluar offline no basta. Estrategias por riesgo creciente de exposición: shadow deployment (el candidato predice en paralelo sin servir), A/B testing (tráfico aleatorio repartido + test de significancia), canary release (subir % gradualmente con rollback), interleaving (mezclar resultados en una lista) y bandits (enrutar adaptativamente hacia el que gana).",
        "cuando_usar": "Antes de promover un modelo candidato a producción completa, para validarlo con tráfico real minimizando el daño.",
        "ejemplo": "Shadow primero (registra sin servir), luego A/B aleatorio; si hay muchos candidatos y se busca eficiencia, bandits.",
        "patron": "shadow→A/B→canary; bandits para asignación adaptativa"
    },
]

existing_ids = {h['id'] for h in study['catalogoHeuristicas']}
for h in new_heuristicas:
    if h['id'] not in existing_ids:
        study['catalogoHeuristicas'].append(h)
        print(f"Heurística añadida: {h['id']}")
    else:
        print(f"Heurística ya existe (skip): {h['id']}")

for reuse in ['detectar-data-drift', 'diseno-experimento-ab']:
    print(f"Reusar '{reuse}': {'OK' if reuse in {h['id'] for h in study['catalogoHeuristicas']} else 'NO EXISTE!'}")

max_ord = max((u.get('orden', 0) for u in study['unidades'] if u.get('bloque') == 'fase-7'), default=0)
print(f"Max orden fase-7: {max_ord}")

# ─── arena-dmls1: Encuadre de problemas de ML ─────────────────────────────────
unit_dmls1 = {
    "id": "arena-dmls1",
    "bloque": "fase-7",
    "orden": max_ord + 1,
    "titulo": "Encuadre de problemas de ML: objetivos y tipos de tarea",
    "libro": "Designing Machine Learning Systems (Chip Huyen)",
    "lectura": "data/teoria/arena-dmls1.md",
    "dosis": 30,
    "objetivo": "Atar el objetivo de ML al de negocio, desacoplar objetivos en conflicto, decidir cuándo usar ML y elegir el tipo de tarea/encuadre.",
    "heuristicas": ["encuadrar-objetivo-ml", "elegir-tipo-tarea-ml"],
    "metadata": {"ruta": "ml-systems", "nivel": 1},
    "ideas_clave": [
        "Un modelo solo sobrevive si su métrica de ML mueve una métrica de negocio",
        "Objetivos en conflicto → un modelo por objetivo, combinados al rankear",
        "El encuadre (multilabel, clasificación vs ranking) decide el coste de mantener"
    ],
    "banco": [
        {"id": "ardmls1-q1", "tipo": "concepto", "enunciado": "¿Por qué muchos proyectos de ML mueren pese a buenas métricas de ML, y cómo se evita?", "solucion": "Porque optimizan métricas de ML (accuracy, F1) sin atarlas a una métrica de negocio (ingresos, retención), que es lo único que importa a la dirección. Se evita definiendo desde el principio cómo el modelo mueve una métrica de negocio concreta y midiendo esa conexión.", "explicacion": "El ML es un medio, no un fin; sin un mapeo claro a valor de negocio el proyecto pierde patrocinio y se cancela."},
        {"id": "ardmls1-q2", "tipo": "concepto", "enunciado": "¿En qué tipos de problema es más fácil mapear el rendimiento del modelo a métricas de negocio?", "solucion": "En aquellos donde la salida se traduce directamente en dinero: predicción de click-through de anuncios (cada punto de CTR es ingreso) y detección de fraude (cada fraude detectado es pérdida evitada). El mapeo directo facilita justificar y mantener el proyecto.", "explicacion": "Cuando la métrica de ML se convierte casi linealmente en ingreso/ahorro, el ROI es evidente y el proyecto sobrevive."},
        {"id": "ardmls1-q3", "tipo": "concepto", "enunciado": "Explica el desacople de objetivos (decoupling objectives) y el problema que resuelve.", "solucion": "Cuando un sistema persigue objetivos en conflicto (p.ej. engagement vs calidad), meterlos en una sola loss ponderada α·calidad + β·engagement obliga a reentrenar cada vez que reajustas los pesos. Desacoplar = entrenar un modelo por objetivo y combinar sus scores al rankear; así reajustar la prioridad es solo cambiar la combinación, sin reentrenar.", "explicacion": "Separar los objetivos desliga el ajuste de prioridades del entrenamiento y permite razonar sobre cada meta por separado."},
        {"id": "ardmls1-q4", "tipo": "concepto", "enunciado": "Da una razón concreta por la que desacoplar objetivos es mejor que una loss combinada, más allá de la limpieza.", "solucion": "Que reajustar la importancia relativa de los objetivos (subir 'calidad' frente a 'engagement') no requiere reentrenar: solo se cambian los pesos de la combinación de scores en tiempo de servicio. Con una loss única ponderada, cualquier cambio de pesos implica un reentrenamiento costoso.", "explicacion": "Es una ventaja operativa real: iterar sobre el trade-off es barato e inmediato cuando los modelos están desacoplados."},
        {"id": "ardmls1-q5", "tipo": "concepto", "enunciado": "¿Cuándo NO conviene usar ML para resolver un problema?", "solucion": "Cuando no hay patrón que aprender, faltan datos, el problema no es repetitivo (cada caso es único), el coste de un error es intolerable, o una heurística/regla simple ya lo resuelve bien. También si es poco ético o si se requiere una respuesta perfecta y explicable que el modelo no garantiza.", "explicacion": "ML aporta cuando hay patrones, datos y repetición con error tolerable; fuera de eso, una regla es más barata, fiable y mantenible."},
        {"id": "ardmls1-q6", "tipo": "concepto", "enunciado": "Enumera condiciones que hacen a un problema buen candidato para ML.", "solucion": "Existen patrones a aprender; hay datos (o se pueden conseguir); el problema es repetitivo, de modo que los patrones se repiten; el coste de las predicciones equivocadas es tolerable; y no se necesita una respuesta perfecta sino lo bastante buena. Idealmente la tarea es a escala (muchas decisiones similares).", "explicacion": "Estas condiciones aseguran que el modelo pueda generalizar y que su utilidad justifique el coste y los errores inevitables."},
        {"id": "ardmls1-q7", "tipo": "concepto", "enunciado": "Diferencia clasificación binaria, multiclase y multietiqueta (multilabel).", "solucion": "Binaria: dos clases posibles, cada ejemplo en una. Multiclase: más de dos clases, pero cada ejemplo pertenece a UNA sola. Multietiqueta: un ejemplo puede pertenecer a VARIAS clases a la vez (un artículo es 'tech' y 'finanzas'). La cardinalidad alta y la multietiqueta complican representación y métricas.", "explicacion": "La distinción clave es cuántas clases puede tener un mismo ejemplo: una (binaria/multiclase) o varias (multilabel)."},
        {"id": "ardmls1-q8", "tipo": "concepto", "enunciado": "¿Por qué Huyen considera la multietiqueta el tipo de tarea más problemático?", "solucion": "Porque la representación de la salida y la evaluación son más enredadas: hay que decidir cuántas etiquetas asignar a cada ejemplo (umbralizar probabilidades) y las métricas estándar (accuracy, F1) no se trasladan limpiamente al caso de múltiples etiquetas simultáneas por ejemplo.", "explicacion": "Salir de la suposición 'una clase por ejemplo' rompe los supuestos de las métricas y de la capa de salida, exigiendo decisiones extra."},
        {"id": "ardmls1-q9", "tipo": "concepto", "enunciado": "Un sistema predice 'qué app abrirá el usuario'. Compara encuadrarlo como clasificación vs como ranking/regresión por par usuario-app.", "solucion": "Como clasificación con una salida (neurona) por app: añadir una app nueva cambia la dimensión de salida y obliga a reentrenar todo el modelo. Como ranking/regresión que puntúa cada par (usuario, app): añadir apps solo agrega más pares a puntuar, sin reentrenar la arquitectura. El segundo encuadre es mucho más mantenible.", "explicacion": "Reformular la tarea para que las categorías sean inputs (pares a puntuar) en vez de salidas fijas elimina el reentrenamiento al crecer el catálogo."},
        {"id": "ardmls1-q10", "tipo": "concepto", "enunciado": "¿Por qué el diseño de un sistema de ML es iterativo y no lineal?", "solucion": "Porque cada etapa (encuadrar el problema, reunir datos, entrenar, evaluar, desplegar, monitorear) revela información que obliga a revisar etapas anteriores: el monitoreo descubre shifts que cambian el encuadre, la evaluación revela datos faltantes, etc. Esperar iteración desde el inicio evita tratar un paso como definitivo.", "explicacion": "El conocimiento del problema crece con el proyecto; un proceso cíclico incorpora ese aprendizaje en vez de congelar decisiones tempranas."},
        {"id": "ardmls1-q11", "tipo": "concepto", "enunciado": "¿Qué problemas trae una alta cardinalidad de clases en clasificación?", "solucion": "Con muchísimas clases es difícil tener suficientes ejemplos por clase (datos escasos por categoría), la salida se vuelve enorme, y a veces conviene reencuadrar (jerarquías de clases, o ranking por par) en lugar de una clasificación plana de miles de salidas.", "explicacion": "La escasez de datos por clase degrada el aprendizaje; reencuadrar o jerarquizar mitiga el problema de la alta cardinalidad."},
        {"id": "ardmls1-q12", "tipo": "concepto", "enunciado": "Una empresa quiere 'usar IA' pero su tarea es decidir casos legales únicos sin precedente. ¿Es buen caso de ML? Justifica.", "solucion": "No es buen caso: si cada decisión es esencialmente única y sin patrón repetible, el modelo no tiene de qué generalizar; además el coste de error suele ser alto y la explicabilidad es crítica. Sería mejor un sistema de apoyo basado en reglas/expertos que un modelo de ML.", "explicacion": "Sin repetición ni patrón, falta la materia prima del aprendizaje; el ML no aporta y arrastra riesgos de error y opacidad."},
        {"id": "ardmls1-q13", "tipo": "concepto", "enunciado": "¿Por qué conviene empezar con una heurística simple antes de un modelo de ML?", "solucion": "Porque establece un baseline barato y rápido contra el cual medir si el ML realmente aporta valor, valida el pipeline end-to-end, y a veces resuelve el problema suficientemente bien sin la complejidad y coste de mantener un modelo. Si el ML no supera a la heurística, no se justifica.", "explicacion": "La heurística es el punto de comparación honesto: el ML debe ganarse su complejidad superándola de forma medible."},
        {"id": "ardmls1-q14", "tipo": "concepto", "enunciado": "Una métrica de negocio común es la 'take-rate' de un recomendador. ¿Cómo conecta con las métricas de ML?", "solucion": "La take-rate (proporción de recomendaciones que el usuario acepta) es una métrica de negocio que se busca subir; las métricas de ML (precision@k, nDCG) son proxies que se optimizan esperando que muevan la take-rate. La empresa crea métricas puente para mapear el rendimiento del modelo a su impacto en take-rate e ingresos.", "explicacion": "Las métricas de ML solo valen si suben la métrica de negocio; las métricas puente hacen explícita y medible esa relación."},
        {"id": "ardmls1-q15", "tipo": "concepto", "enunciado": "Resume el principio central del encuadre de un problema de ML según Huyen.", "solucion": "Antes de modelar, encuadra bien: (1) ata la métrica de ML a una de negocio; (2) decide si ML es siquiera la herramienta adecuada; (3) si hay objetivos en conflicto, desacóplalos en modelos separados; (4) elige el tipo de tarea y el encuadre (clasificación vs ranking, multilabel) pensando en el coste de mantenimiento. El encuadre, más que el algoritmo, determina el éxito del sistema.", "explicacion": "Las decisiones de encuadre condicionan datos, métricas, arquitectura y mantenimiento; equivocarlas no se arregla con un mejor modelo."}
    ]
}

# ─── arena-dmls2: Datos de entrenamiento ──────────────────────────────────────
unit_dmls2 = {
    "id": "arena-dmls2",
    "bloque": "fase-7",
    "orden": max_ord + 2,
    "titulo": "Datos de entrenamiento: muestreo, etiquetas y desbalance",
    "libro": "Designing Machine Learning Systems (Chip Huyen)",
    "lectura": "data/teoria/arena-dmls2.md",
    "dosis": 30,
    "objetivo": "Elegir métodos de muestreo (estratificado, reservoir, importance), conseguir etiquetas (natural labels, weak supervision, active learning) y manejar el desbalance de clases.",
    "heuristicas": ["muestreo-streaming", "usar-natural-labels", "manejar-desbalance-clases"],
    "metadata": {"ruta": "ml-systems", "nivel": 2},
    "ideas_clave": [
        "Reservoir sampling toma k de un stream con igual probabilidad k/n",
        "Natural labels (clics) y weak supervision evitan el etiquetado manual",
        "Con desbalance, accuracy engaña: usa F1/AUC + resampling/weighted loss"
    ],
    "banco": [
        {"id": "ardmls2-q1", "tipo": "concepto", "enunciado": "Diferencia el muestreo no probabilístico del aleatorio y su riesgo.", "solucion": "El no probabilístico selecciona datos sin criterio de probabilidad (por conveniencia, bola de nieve, juicio o cuotas): rápido y barato pero NO representativo, arrastra sesgos al modelo. El aleatorio (simple, estratificado, ponderado) sí da muestras representativas porque cada elemento tiene una probabilidad conocida de ser elegido.", "explicacion": "La falta de aleatoriedad introduce sesgo de selección sistemático; el modelo aprende un mundo distorsionado."},
        {"id": "ardmls2-q2", "tipo": "concepto", "enunciado": "¿Qué es el muestreo estratificado y qué problema evita?", "solucion": "Divide la población en grupos (estratos) y muestrea dentro de cada uno, garantizando representación de todos. Evita que un muestreo aleatorio simple deje fuera (o subrepresente) grupos minoritarios o raros que importan para el modelo.", "explicacion": "Asegurar muestras de cada estrato preserva la diversidad de la población, crucial cuando hay clases o segmentos poco frecuentes."},
        {"id": "ardmls2-q3", "tipo": "algoritmo", "enunciado": "Describe el algoritmo de reservoir sampling y qué garantiza.", "solucion": "Para tomar k muestras de un stream de tamaño desconocido: 1) mete los primeros k elementos en el reservorio; 2) para el n-ésimo elemento entrante, genera un aleatorio i con 1≤i≤n; 3) si i≤k, reemplaza el i-ésimo del reservorio por el nuevo; si no, descártalo. Garantiza que en cualquier instante en que pares, cada elemento visto tiene probabilidad k/n de estar en el reservorio (igual probabilidad para todos).", "explicacion": "Resuelve muestrear uniformemente sin conocer el tamaño total ni guardar todo en memoria, ideal para datos en streaming."},
        {"id": "ardmls2-q4", "tipo": "concepto", "enunciado": "¿Por qué reservoir sampling es valioso en producción?", "solucion": "Porque los datos en producción suelen llegar como un stream continuo cuyo tamaño no se conoce de antemano y no cabe en memoria; reservoir sampling permite mantener una muestra uniforme de tamaño fijo k sobre la marcha, pudiendo detenerse en cualquier momento con la probabilidad correcta.", "explicacion": "Es el método natural para muestrear datos en movimiento sin doble pasada ni almacenamiento total."},
        {"id": "ardmls2-q5", "tipo": "concepto", "enunciado": "¿Qué es importance sampling y cuándo se usa?", "solucion": "Permite muestrear de una distribución P(x) cara, lenta o imposible de muestrear, sacando muestras de otra Q(x) fácil (la proposal/importance distribution) y reponderando cada muestra por P(x)/Q(x). Requiere Q(x)>0 siempre que P(x)≠0. En RL basado en políticas estima la política nueva reponderando recompensas de la vieja.", "explicacion": "Reponderar corrige el sesgo de muestrear de Q en lugar de P, dejando la esperanza invariante; sirve cuando P es inaccesible pero Q es tratable."},
        {"id": "ardmls2-q6", "tipo": "concepto", "enunciado": "¿Qué son las natural labels y cuál es su ejemplo canónico?", "solucion": "Son etiquetas que el sistema infiere automáticamente de la realidad o del comportamiento del usuario, sin anotación manual. El ejemplo canónico es el sistema de recomendación: que el usuario haga clic, compre o ignore una recomendación es la etiqueta (etiqueta implícita) de si fue buena.", "explicacion": "El propio uso del sistema genera la verdad de campo, eliminando o reduciendo el coste de etiquetar a mano."},
        {"id": "ardmls2-q7", "tipo": "concepto", "enunciado": "¿Qué es el 'feedback loop length' y por qué importa?", "solucion": "Es el tiempo que tarda en llegar la natural label tras la predicción. Importa porque determina cuán rápido puedes evaluar el modelo y detectar fallos o shifts: un clic da feedback en minutos (loop corto), pero saber si una recomendación de compra de gran valor 'acertó' puede tardar semanas (loop largo), retrasando la detección de problemas.", "explicacion": "Loops cortos permiten iterar y monitorear rápido; loops largos obligan a usar proxies o esperar para conocer el desempeño real."},
        {"id": "ardmls2-q8", "tipo": "concepto", "enunciado": "¿Qué es la weak supervision con labeling functions?", "solucion": "En vez de etiquetar a mano, se escriben funciones heurísticas (labeling functions) que asignan etiquetas ruidosas según reglas (p.ej. 'si el email contiene la palabra oferta → spam'); luego se combinan sus votos, posiblemente en conflicto, para producir etiquetas probabilísticas a escala. Herramienta típica: Snorkel.", "explicacion": "Cambia etiquetado manual caro por reglas programáticas baratas y escalables, aceptando ruido que el modelo de combinación gestiona."},
        {"id": "ardmls2-q9", "tipo": "concepto", "enunciado": "¿Qué es active learning y por qué es más eficiente en etiquetas?", "solucion": "Es una estrategia donde el modelo ELIGE qué ejemplos quiere que se etiqueten —típicamente aquellos sobre los que está más incierto o que son más informativos— en lugar de etiquetar muestras al azar. Así alcanza buen rendimiento con menos etiquetas, concentrando el esfuerzo de anotación donde más aporta.", "explicacion": "Etiquetar los ejemplos más informativos da más aprendizaje por etiqueta que el muestreo aleatorio, reduciendo el coste total de anotación."},
        {"id": "ardmls2-q10", "tipo": "concepto", "enunciado": "¿Qué es el problema de label multiplicity en hand labels y cómo se mitiga?", "solucion": "Es que distintos anotadores asignan etiquetas diferentes al mismo ejemplo (discrepancia entre anotadores), generando datos inconsistentes. Se mitiga con instrucciones de anotación claras y detalladas, definiciones consensuadas, y mecanismos de resolución de desacuerdos (acuerdo entre anotadores, revisión).", "explicacion": "La subjetividad humana introduce ruido; estandarizar el criterio de etiquetado reduce la inconsistencia que confunde al modelo."},
        {"id": "ardmls2-q11", "tipo": "concepto", "enunciado": "¿Por qué la accuracy es engañosa con desbalance de clases? Da un ejemplo.", "solucion": "Porque un modelo que siempre predice la clase mayoritaria logra accuracy altísima sin aprender nada útil. Ejemplo: en fraude con 0.1% de casos positivos, predecir 'siempre legítimo' da 99.9% de accuracy pero detecta cero fraudes. La métrica no refleja el desempeño en la clase que importa.", "explicacion": "La accuracy promedia sobre clases; cuando una domina, oculta el fracaso total en la clase minoritaria, que suele ser la relevante."},
        {"id": "ardmls2-q12", "tipo": "concepto", "enunciado": "¿Qué métricas y técnicas usarías ante un fuerte desbalance de clases?", "solucion": "Métricas: F1, precision/recall, AUC-ROC o PR-AUC (no accuracy). Técnicas a nivel de datos: oversampling de la minoría (p.ej. SMOTE) o undersampling de la mayoría. Técnicas a nivel de algoritmo: loss ponderada/cost-sensitive que penaliza más los errores en la clase rara.", "explicacion": "Estas métricas evalúan la clase minoritaria; resampling y weighted loss reequilibran la atención del modelo hacia ella."},
        {"id": "ardmls2-q13", "tipo": "concepto", "enunciado": "Diferencia oversampling de undersampling y un riesgo de cada uno.", "solucion": "Oversampling replica o sintetiza ejemplos de la clase minoritaria (SMOTE) — riesgo: overfitting a los pocos ejemplos minoritarios o a artefactos sintéticos. Undersampling descarta ejemplos de la mayoritaria para equilibrar — riesgo: tirar información útil y degradar el modelo en la clase mayoritaria.", "explicacion": "Ambos reequilibran la proporción de clases pero por vías opuestas; cada uno sacrifica algo (sobreajuste vs pérdida de datos)."},
        {"id": "ardmls2-q14", "tipo": "concepto", "enunciado": "¿Por qué la mayoría de los modelos en producción siguen siendo supervisados pese al auge del no supervisado?", "solucion": "Porque, en la práctica, el rendimiento depende fuertemente de la cantidad y calidad de datos etiquetados, y los métodos supervisados siguen dando los mejores resultados en la mayoría de tareas de negocio. Por eso conseguir etiquetas (natural labels, weak supervision) es un problema central del diseño de sistemas de ML.", "explicacion": "El etiquetado es el cuello de botella real; aunque el no supervisado promete, la supervisión sigue dominando producción."},
        {"id": "ardmls2-q15", "tipo": "concepto", "enunciado": "Tienes un stream de tweets ilimitado y quieres entrenar con una muestra uniforme, pero etiquetar es caro. Describe una estrategia combinada.", "solucion": "Usar reservoir sampling para mantener una muestra uniforme de tamaño k del stream sin guardarlo todo; sobre esa muestra, en vez de etiquetar todo a mano, aplicar weak supervision (labeling functions) para etiquetas baratas y/o active learning para mandar a etiquetar manualmente solo los tweets más inciertos. Si hay desbalance, medir con F1/AUC y resamplear.", "explicacion": "Combina muestreo eficiente de streams con estrategias de etiquetado de bajo coste, atacando los dos cuellos de botella (volumen y etiquetas)."}
    ]
}

# ─── arena-dmls3: Despliegue y predicción ─────────────────────────────────────
unit_dmls3 = {
    "id": "arena-dmls3",
    "bloque": "fase-7",
    "orden": max_ord + 3,
    "titulo": "Despliegue y predicción: batch vs online, compresión y edge",
    "libro": "Designing Machine Learning Systems (Chip Huyen)",
    "lectura": "data/teoria/arena-dmls3.md",
    "dosis": 30,
    "objetivo": "Elegir entre batch y online prediction, distinguir batch/streaming features, comprimir modelos (distillation/quantization/pruning/low-rank) y decidir edge vs cloud.",
    "heuristicas": ["elegir-batch-vs-online", "comprimir-modelo"],
    "metadata": {"ruta": "ml-systems", "nivel": 2},
    "ideas_clave": [
        "Batch precomputa (rápido, rancio); online predice on-demand (fresco, latencia)",
        "Compresión: low-rank, distillation, pruning, quantization",
        "Edge gana latencia/offline/privacidad a costa de comprimir el modelo"
    ],
    "banco": [
        {"id": "ardmls3-q1", "tipo": "concepto", "enunciado": "Diferencia batch prediction de online prediction.", "solucion": "Batch prediction (asíncrona) calcula las predicciones por adelantado en lotes y las guarda para servirlas al instante cuando se piden. Online prediction (síncrona, on-demand) genera la predicción en el momento en que llega la petición, con los datos más frescos. Batch prioriza throughput; online, frescura a costa de pelear contra la latencia.", "explicacion": "El eje es cuándo se calcula: antes (batch, almacenada) o al momento (online, fresca)."},
        {"id": "ardmls3-q2", "tipo": "concepto", "enunciado": "¿Cuándo conviene batch prediction y cuál es su principal riesgo?", "solucion": "Conviene cuando no necesitas frescura inmediata y el volumen es alto y predecible (recomendaciones precomputadas de noche). Su principal riesgo es que las predicciones queden rancias (el mundo o el usuario cambian entre el cálculo y el uso) y que se desperdicie cómputo prediciendo para usuarios que nunca lo piden.", "explicacion": "Precomputar gana velocidad de servicio pero pierde frescura; sirve solo cuando el input es conocido y estable de antemano."},
        {"id": "ardmls3-q3", "tipo": "concepto", "enunciado": "¿Cuándo es obligatoria la online prediction y cuál es su reto técnico central?", "solucion": "Es obligatoria cuando el input no se conoce de antemano y depende de la petición en tiempo real (búsqueda con query arbitraria, pricing dinámico). Su reto central es la latencia: hay que generar la predicción —y a menudo extraer features en vivo— lo bastante rápido para no degradar la experiencia.", "explicacion": "On-demand permite frescura y inputs arbitrarios, pero pone toda la presión en responder dentro de un presupuesto de latencia estricto."},
        {"id": "ardmls3-q4", "tipo": "concepto", "enunciado": "Diferencia batch features de streaming features.", "solucion": "Batch features se calculan de datos históricos en reposo mediante batch processing (la edad media histórica de un cliente). Streaming features se extraen de datos en movimiento mediante stream processing (cuántos viajes pidió el usuario en los últimos 5 minutos). Muchos sistemas online serios necesitan ambas.", "explicacion": "La diferencia es la frescura/origen del dato: histórico en reposo vs en vivo en movimiento; la online prediction suele depender de las streaming features."},
        {"id": "ardmls3-q5", "tipo": "concepto", "enunciado": "Diferencia el paso de datos request-driven del event-driven en sistemas de ML.", "solucion": "Request-driven (REST/RPC) es síncrono: el servicio destino debe escuchar y responder a cada petición; acopla servicios. Event-driven (pub/sub con un message broker tipo Kafka) es asíncrono: los servicios publican y se suscriben a eventos, desacoplándose y permitiendo procesamiento en streaming con latencia razonablemente baja.", "explicacion": "El estilo de comunicación define el acoplamiento y la capacidad de streaming; event-driven habilita las streaming features y la escalabilidad."},
        {"id": "ardmls3-q6", "tipo": "concepto", "enunciado": "Nombra las cuatro técnicas frecuentes de compresión de modelos.", "solucion": "Low-rank factorization (factorizar tensores densos en factores de menor rango), knowledge distillation (un student pequeño imita a un teacher grande), pruning (eliminar parámetros/conexiones poco útiles o ponerlos a cero) y quantization (representar los números con menos bits).", "explicacion": "Las cuatro reducen tamaño/latencia por vías distintas: estructura, imitación, esparsidad y precisión numérica."},
        {"id": "ardmls3-q7", "tipo": "concepto", "enunciado": "¿Qué es knowledge distillation y da un ejemplo conocido?", "solucion": "Es entrenar un modelo pequeño (student) para imitar el comportamiento de uno grande (teacher), usando las salidas (soft targets) del teacher como objetivo. El student conserva casi el rendimiento del teacher a una fracción del tamaño y latencia. Ejemplo: DistilBERT, una versión destilada y más ligera de BERT.", "explicacion": "Transferir el 'conocimiento' del teacher al student logra modelos compactos sin entrenar desde cero con datos etiquetados masivos."},
        {"id": "ardmls3-q8", "tipo": "concepto", "enunciado": "¿Qué hace la quantization y cuál es su riesgo?", "solucion": "Representa los números (pesos y/o activaciones) con menos bits: de 32 bits de punto flotante a 16 u 8 bits, o int8. Reduce memoria y acelera el cómputo, y es la técnica de compresión más general y usada. Su riesgo es la pérdida de precisión numérica (menor rango y más redondeo), que puede degradar la exactitud del modelo si no se calibra.", "explicacion": "Menos bits = menos memoria y más velocidad, a cambio de granularidad numérica; el reto es comprimir sin sacrificar exactitud."},
        {"id": "ardmls3-q9", "tipo": "concepto", "enunciado": "¿Qué es pruning y por qué a veces ayuda a generalizar?", "solucion": "Pruning elimina parámetros, conexiones o neuronas que aportan poco (o los pone a cero), reduciendo el tamaño del modelo y la latencia. A veces mejora la generalización porque quitar pesos redundantes actúa como regularización, reduciendo el sobreajuste a la vez que comprime.", "explicacion": "Recortar capacidad innecesaria reduce el modelo y, como toda regularización, puede mejorar el desempeño fuera de muestra."},
        {"id": "ardmls3-q10", "tipo": "concepto", "enunciado": "Compara desplegar en la nube vs en el edge (ventajas y costes).", "solucion": "Nube: cómputo en servidores, fácil de escalar y actualizar, pero suma latencia de red, coste continuo, dependencia de conectividad y riesgos de privacidad (los datos salen del dispositivo). Edge: el modelo corre en el dispositivo, gana baja latencia, funciona sin red, abarata el servidor y protege la privacidad, a costa de necesitar hardware capaz y modelos comprimidos.", "explicacion": "El trade-off central es flexibilidad/escala (nube) frente a latencia, autonomía y privacidad (edge)."},
        {"id": "ardmls3-q11", "tipo": "concepto", "enunciado": "¿Por qué la tendencia hacia el edge hace más relevante la compresión de modelos?", "solucion": "Porque los dispositivos edge (móviles, IoT) tienen memoria, cómputo y energía limitados; un modelo grande no cabe ni corre con la latencia requerida. La compresión (quantization, distillation, pruning) es lo que permite que modelos potentes quepan y respondan rápido en hardware restringido.", "explicacion": "El edge impone restricciones de recursos que solo modelos comprimidos pueden satisfacer; por eso ambas tendencias se refuerzan."},
        {"id": "ardmls3-q12", "tipo": "concepto", "enunciado": "Un servicio de búsqueda debe responder a queries arbitrarias en <100 ms. ¿Batch u online? ¿Qué features?", "solucion": "Online prediction: las queries son arbitrarias y no se pueden precomputar, y se necesita respuesta inmediata. Requiere features frescas, típicamente una mezcla de batch features (históricas, precomputadas en un feature store) y streaming features (señales de los últimos segundos/minutos), todo dentro del presupuesto de latencia.", "explicacion": "Inputs imprevisibles + baja latencia obligan a online; el reto es servir features frescas sin exceder el tiempo."},
        {"id": "ardmls3-q13", "tipo": "concepto", "enunciado": "¿Por qué demasiadas features pueden ser un problema en online prediction?", "solucion": "Porque cada feature hay que extraerla/calcularla en vivo para cada petición, lo que añade latencia de inferencia; muchas features (sobre todo si exigen consultas o stream processing) pueden hacer que el servicio no cumpla su presupuesto de tiempo. Conviene podar features de bajo valor.", "explicacion": "En online, el coste de extracción de cada feature se paga en cada request; la latencia limita cuántas features son viables."},
        {"id": "ardmls3-q14", "tipo": "concepto", "enunciado": "Quieres servir un modelo grande en móviles sin conexión estable. Esboza el plan.", "solucion": "Desplegar en el edge (en el dispositivo) para funcionar offline y con baja latencia, comprimiendo antes el modelo: destilarlo a un student pequeño, cuantizarlo a int8 y/o prunearlo hasta que quepa y corra dentro de las restricciones del móvil. Validar que la pérdida de exactitud por la compresión sea aceptable.", "explicacion": "Edge resuelve el offline y la latencia; la compresión hace que el modelo grande sea servible en hardware limitado."},
        {"id": "ardmls3-q15", "tipo": "concepto", "enunciado": "Resume las tres decisiones clave del despliegue de un modelo según Huyen.", "solucion": "1) Batch vs online prediction (precomputar y servir rápido pero rancio, vs predecir on-demand fresco peleando la latencia). 2) Cómo conseguir las features (batch features históricas vs streaming features en vivo, normalmente ambas). 3) Dónde y con qué tamaño correr el modelo (cloud vs edge, y compresión: low-rank/distillation/pruning/quantization).", "explicacion": "Cuándo se predice, con qué datos y dónde corre el modelo definen la arquitectura del servicio de predicción."}
    ]
}

# ─── arena-dmls4: Shift, monitoreo y test en producción ───────────────────────
unit_dmls4 = {
    "id": "arena-dmls4",
    "bloque": "fase-7",
    "orden": max_ord + 4,
    "titulo": "Cambios de distribución, monitoreo y test en producción",
    "libro": "Designing Machine Learning Systems (Chip Huyen)",
    "lectura": "data/teoria/arena-dmls4.md",
    "dosis": 30,
    "objetivo": "Diagnosticar los tipos de distribution shift, monitorear modelos en producción, aplicar aprendizaje continuo y elegir estrategias de test en producción (shadow, A/B, canary, bandits).",
    "heuristicas": ["diagnosticar-distribution-shift", "test-en-produccion", "detectar-data-drift", "diseno-experimento-ab"],
    "metadata": {"ruta": "ml-systems", "nivel": 3},
    "ideas_clave": [
        "Covariate (P(X)), label (P(Y)) y concept drift (P(Y|X)) son shifts distintos",
        "Test en producción por riesgo: shadow → A/B → canary; bandits adaptativo",
        "Continual learning: stateless (desde cero) vs stateful (incremental)"
    ],
    "banco": [
        {"id": "ardmls4-q1", "tipo": "concepto", "enunciado": "¿Por qué un modelo desplegado se degrada con el tiempo?", "solucion": "Porque el mundo cambia y la distribución de los datos de producción deja de parecerse a la de entrenamiento (data distribution shift). El modelo aprendió relaciones de un mundo que ya no es el actual, así que su desempeño cae aunque el código no cambie. Es la razón por la que el monitoreo y el reentrenamiento son indispensables.", "explicacion": "El ML asume que producción se parece a entrenamiento; cuando esa suposición se rompe por el cambio del mundo, el modelo se 'pudre'."},
        {"id": "ardmls4-q2", "tipo": "concepto", "enunciado": "Define covariate shift con su expresión de probabilidad y un ejemplo.", "solucion": "Covariate shift: cambia P(X) (la distribución de los inputs) pero P(Y|X) (la relación input→output) se mantiene. Ejemplo: a tu servicio empiezan a llegar más usuarios jóvenes (cambia la distribución de edades), pero la relación entre edad y probabilidad de compra es la misma de siempre. Causa típica: sesgo de selección en los datos de entrenamiento.", "explicacion": "Cambian los inputs que ves, no cómo se mapean a la salida; basta reponderar/reentrenar con la nueva mezcla de inputs."},
        {"id": "ardmls4-q3", "tipo": "concepto", "enunciado": "Define label shift y concept drift, distinguiéndolos.", "solucion": "Label shift: cambia P(Y) (la distribución de las salidas) pero P(X|Y) se mantiene (dado el label, los features se ven igual); p.ej. sube la proporción de casos positivos. Concept drift: cambia P(Y|X), la relación misma input→output; el mismo input ahora produce otra salida (un precio antes 'caro' hoy es 'normal'). El concept drift es el más peligroso porque invalida lo aprendido.", "explicacion": "Label shift mueve la frecuencia de las clases; concept drift muta la función que el modelo aproxima, exigiendo reaprender la relación."},
        {"id": "ardmls4-q4", "tipo": "concepto", "enunciado": "¿Cómo se detecta estadísticamente un distribution shift?", "solucion": "Comparando la distribución de los datos de producción contra una distribución de referencia (la de entrenamiento o una ventana previa) con two-sample tests, como Kolmogorov-Smirnov o Maximum Mean Discrepancy. Un resultado estadísticamente significativo indica que las dos muestras provienen de distribuciones distintas, es decir, que hubo shift.", "explicacion": "Es la misma maquinaria del A/B testing aplicada al revés: si dos muestras difieren significativamente, la distribución se movió."},
        {"id": "ardmls4-q5", "tipo": "concepto", "enunciado": "¿Qué métricas hay que monitorear en un modelo en producción cuando no hay labels inmediatos?", "solucion": "Métricas operacionales (latencia, throughput, uptime, tasa de error del servicio) y, ante la falta de labels, proxies de las métricas de ML: la distribución de las predicciones, de los features de entrada y de los inputs crudos. Cambios en esas distribuciones señalan posibles shifts o problemas antes de que lleguen las etiquetas.", "explicacion": "Sin ground truth inmediato, se vigilan proxies distribucionales; un cambio en ellos es alerta temprana de degradación."},
        {"id": "ardmls4-q6", "tipo": "concepto", "enunciado": "Diferencia monitoreo de observabilidad.", "solucion": "El monitoreo es rastrear métricas para saber QUE algo va mal (una alerta dispara cuando la latencia o la accuracy caen). La observabilidad es diseñar el sistema para poder entender POR QUÉ va mal: logs, traces y capacidad de cortar (slice) por segmentos para diagnosticar la causa raíz, no solo detectar el síntoma.", "explicacion": "Monitorear detecta; observar explica. Sin observabilidad sabes que falla pero no puedes diagnosticarlo."},
        {"id": "ardmls4-q7", "tipo": "concepto", "enunciado": "Diferencia el reentrenamiento stateless del stateful (continual learning).", "solucion": "Stateless retraining: reentrenar el modelo desde cero cada vez con datos nuevos (lo más común; simple pero costoso y lento de actualizar). Stateful/incremental: continuar el entrenamiento desde el checkpoint anterior incorporando solo los datos nuevos; es más barato, más rápido de actualizar y necesita menos datos por actualización.", "explicacion": "Stateless reinicia; stateful acumula sobre lo aprendido, abaratando actualizaciones frecuentes a cambio de más complejidad de infraestructura."},
        {"id": "ardmls4-q8", "tipo": "concepto", "enunciado": "¿Cuál es la pregunta correcta sobre la frecuencia de reentrenamiento?", "solucion": "No es '¿cada cuánto reentreno?' en abstracto, sino '¿cuánto valor aporta actualizar el modelo (value of data freshness) frente al coste y el riesgo de hacerlo?'. Si datos más frescos mejoran mucho el desempeño, conviene reentrenar seguido; si apenas mueven la métrica, no justifica el coste.", "explicacion": "La cadencia óptima sale de un análisis coste-beneficio del valor de la frescura, no de un calendario fijo arbitrario."},
        {"id": "ardmls4-q9", "tipo": "concepto", "enunciado": "¿Qué es shadow deployment y por qué es la forma más segura de probar un modelo?", "solucion": "El modelo candidato se despliega junto al actual y recibe el MISMO tráfico, generando predicciones en paralelo, pero sus predicciones NO se sirven a los usuarios: solo se registran y comparan contra las del modelo en producción. Es la más segura porque el candidato nunca afecta a usuarios reales; su coste es duplicar el cómputo de inferencia.", "explicacion": "Probar sin exponer al usuario elimina el riesgo de daño; a cambio se paga el doble de inferencia mientras se valida."},
        {"id": "ardmls4-q10", "tipo": "concepto", "enunciado": "¿Cómo funciona un A/B test de modelos y qué dos cosas hay que hacer bien?", "solucion": "Se despliega el candidato junto al actual y se enruta un porcentaje del tráfico al candidato y el resto al actual, midiendo métricas predefinidas. Dos cosas críticas: (1) el ruteo debe ser verdaderamente ALEATORIO —cualquier sesgo de selección (p.ej. móvil vs desktop por variante) invalida el test—; (2) hay que correrlo con suficientes muestras y evaluar la diferencia con un test de significancia (two-sample).", "explicacion": "La aleatoriedad asegura grupos comparables y el tamaño de muestra da poder; sin ambos, la conclusión sobre cuál modelo es mejor no es válida."},
        {"id": "ardmls4-q11", "tipo": "concepto", "enunciado": "¿Por qué la significancia estadística en un A/B test no es infalible?", "solucion": "Porque un resultado significativo a p=0.05 implica que, si repitieras el experimento muchas veces, ~5% de las veces obtendrías la conclusión contraria por azar. Así, aun con significancia, existe una probabilidad de haber elegido el modelo equivocado. Y un resultado no significativo con muchas muestras puede simplemente indicar que ambos modelos son equivalentes.", "explicacion": "El p-valor acota pero no elimina el error tipo I; la significancia reduce el riesgo de equivocarse, no lo anula."},
        {"id": "ardmls4-q12", "tipo": "concepto", "enunciado": "¿Qué es un canary release y cómo reduce el riesgo?", "solucion": "Es desplegar el modelo candidato a un subconjunto pequeño de usuarios y monitorear sus métricas; si aguantan, se sube gradualmente el porcentaje de tráfico hasta el 100%, y si empeoran, se hace rollback de inmediato. Reduce el riesgo limitando la exposición inicial: un fallo afecta solo a una fracción pequeña antes de revertir.", "explicacion": "El despliegue gradual con rollback contiene el radio de impacto de un modelo defectuoso, a diferencia de un cambio total de golpe."},
        {"id": "ardmls4-q13", "tipo": "concepto", "enunciado": "¿Qué es el interleaving y en qué tareas se usa?", "solucion": "Interleaving mezcla los resultados de dos modelos en una MISMA lista mostrada al usuario y observa de cuál modelo provienen los ítems que el usuario elige (clics). Se usa sobre todo en ranking y sistemas de recomendación, donde permite comparar modelos de forma sensible con menos tráfico que un A/B test clásico.", "explicacion": "Al enfrentar ambos modelos dentro de la misma experiencia, controla por el usuario y la sesión, ganando sensibilidad en tareas de ranking."},
        {"id": "ardmls4-q14", "tipo": "concepto", "enunciado": "¿Qué son los bandits y qué ventaja tienen sobre el A/B testing? ¿Y los contextual bandits?", "solucion": "Los bandits son un enrutamiento adaptativo que asigna más tráfico al modelo que va rindiendo mejor mientras sigue explorando los demás (balance explora/explota). Ventaja sobre el A/B: son más eficientes en datos —desperdician menos tráfico en la variante mala y convergen antes—, a costa de mayor complejidad de implementación. Los contextual bandits incorporan además el contexto de cada decisión (features del usuario/situación) para elegir la mejor variante por contexto.", "explicacion": "El A/B reparte fijo y evalúa al final; el bandit reasigna sobre la marcha hacia lo que funciona, reduciendo el coste de oportunidad de explorar."},
        {"id": "ardmls4-q15", "tipo": "concepto", "enunciado": "Un modelo en producción empieza a fallar. Esboza cómo lo diagnosticarías y cómo validarías el reemplazo.", "solucion": "Diagnóstico: monitorear métricas operacionales y proxies (distribución de inputs/predicciones); aplicar two-sample tests para detectar shift y clasificar su tipo —covariate (cambia P(X)), label (cambia P(Y)) o concept drift (cambia P(Y|X))— usando observabilidad para hallar el segmento afectado. Validación del reemplazo: entrenar un candidato (stateless o stateful), probarlo primero en shadow deployment (sin servir), luego en A/B aleatorio con significancia o canary gradual, y solo entonces promoverlo a todo el tráfico.", "explicacion": "Primero identificar el tipo de shift con tests y observabilidad, luego validar el nuevo modelo con exposición de riesgo creciente (shadow→A/B/canary) antes del despliegue total."}
    ]
}

# ─── Ítems de examen (IDs dinámicos) ──────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        items = bloque['examen']['items']
        nums = [int(it['id'].split('-')[-1]) for it in items]
        last_id = max(nums)
        print(f"Último examen id: f7-ex-{last_id}")
        next_id1 = last_id + 1
        next_id2 = last_id + 2
        break

ex_next1 = {
    "id": f"f7-ex-{next_id1}",
    "heuristica": "test-en-produccion",
    "enunciado": "Tienes un modelo de recomendación en producción y un candidato nuevo que en evaluación offline luce mejor. El negocio teme degradar la experiencia si el candidato falla con tráfico real. (a) ¿Por qué la evaluación offline no basta? (b) describe una secuencia de estrategias de test en producción ordenada de menor a mayor exposición del usuario, explicando cada una; (c) si tuvieras decenas de modelos candidatos y quisieras minimizar el tráfico desperdiciado en los malos, ¿qué método elegirías y por qué?",
    "pistas": [
        "Offline usas datos históricos estáticos; producción tiene tráfico vivo y posibles shifts. ¿Qué no captura lo offline?",
        "La estrategia más segura no muestra al usuario las predicciones del candidato: ¿cómo se llama?",
        "Piensa en una escalera de riesgo: registrar en paralelo → repartir tráfico aleatorio → subir gradualmente con rollback.",
        "Para 'cuál de dos es mejor' con tráfico aleatorio y significancia estadística está el A/B; para subir poco a poco con rollback, el canary.",
        "Si quieres reasignar tráfico sobre la marcha hacia el que va ganando (explora/explota), piensa en bandits."
    ],
    "solucion": "(a) La evaluación offline usa un conjunto de test estático y no captura el comportamiento con tráfico real, las interacciones con el usuario, ni los distribution shifts de producción; un modelo mejor offline puede ser peor en vivo. (b) De menor a mayor exposición: SHADOW DEPLOYMENT — el candidato recibe el mismo tráfico y predice en paralelo, pero sus predicciones NO se sirven, solo se registran y comparan (cero riesgo, doble cómputo); A/B TESTING — se enruta un % del tráfico al candidato de forma verdaderamente aleatoria y el resto al actual, comparando métricas con un test de significancia (two-sample), cuidando el tamaño de muestra; CANARY RELEASE — se expone el candidato a un subconjunto pequeño y se sube el porcentaje gradualmente mientras las métricas aguanten, con rollback inmediato si empeoran. (Interleaving — mezclar resultados de ambos en una lista — es otra opción sensible en ranking.) (c) Bandits: enrutan el tráfico de forma adaptativa hacia los modelos que van rindiendo mejor mientras siguen explorando los demás (explora/explota), así desperdician menos tráfico en los candidatos malos y convergen antes que repartir fijo como el A/B; el coste es mayor complejidad de implementación (y contextual bandits si conviene decidir por contexto).",
    "disparador": "Señal: 'validar un modelo candidato con tráfico real sin arriesgar usuarios'. Jugada: escalera shadow → A/B aleatorio + significancia → canary; bandits para asignación adaptativa con muchos candidatos.",
    "metadata": {
        "ruta": "ml-systems",
        "nivel": 3,
        "skills": ["test en producción", "shadow deployment", "A/B testing", "canary release", "bandits"],
        "errores_comunes": ["Promover a producción solo por mejores métricas offline", "Hacer A/B con ruteo no aleatorio (sesgo de selección invalida el test)"],
        "casos_borde": ["Si las predicciones de un modelo afectan al otro (pricing dinámico), servir variantes en días alternos", "Interleaving es preferible al A/B clásico en tareas de ranking por su mayor sensibilidad"],
        "source": "Designing Machine Learning Systems (Chip Huyen) — Cap. 9"
    }
}

ex_next2 = {
    "id": f"f7-ex-{next_id2}",
    "heuristica": "diagnosticar-distribution-shift",
    "enunciado": "Un clasificador que predice si un email es spam (Y) a partir de su contenido (X) lleva meses en producción y su desempeño cayó. (a) Partiendo de P(X,Y), define covariate shift, label shift y concept drift por su probabilidad. (b) Para cada uno, da un ejemplo plausible en este sistema de spam. (c) ¿Cómo detectarías cuál ocurrió, y por qué el concept drift es el más difícil de manejar?",
    "pistas": [
        "Descompón P(X,Y) de dos formas: P(Y|X)P(X) y P(X|Y)P(Y).",
        "Covariate: cambia P(X) y P(Y|X) igual. Label: cambia P(Y), P(X|Y) igual. Concept: cambia P(Y|X).",
        "Covariate: llegan emails de un idioma/tema nuevo. Label: sube la proporción global de spam. Concept: lo que cuenta como spam cambia.",
        "Para detectar, compara la distribución de producción contra una referencia con un two-sample test (KS/MMD) sobre X, sobre Y y, si hay labels, sobre la relación.",
        "Concept drift cambia la relación X→Y misma: el conocimiento aprendido queda inválido, no basta con reponderar inputs."
    ],
    "solucion": "(a) Con P(X,Y)=P(Y|X)P(X)=P(X|Y)P(Y): COVARIATE SHIFT = cambia P(X) (distribución de los inputs) pero P(Y|X) se mantiene; LABEL SHIFT = cambia P(Y) (distribución de las salidas) pero P(X|Y) se mantiene; CONCEPT DRIFT = cambia P(Y|X), la relación input→output. (b) Covariate: empiezan a llegar emails en un idioma o sobre temas nuevos (cambia la mezcla de contenidos X), pero qué palabras indican spam sigue igual. Label: una campaña masiva dispara la proporción global de spam recibido (sube P(Y=spam)) sin que el aspecto de un spam cambie. Concept: los spammers cambian de táctica y emails que antes eran legítimos ahora son spam (o viceversa): el mismo contenido X recibe otra etiqueta Y. (c) Se compara la distribución de producción contra una de referencia con two-sample tests (Kolmogorov-Smirnov, MMD): sobre los features X se detecta covariate shift, sobre las etiquetas Y el label shift, y observando que la relación X→Y cambió (cuando llegan labels) el concept drift. El concept drift es el más difícil porque invalida lo aprendido: la función que el modelo aproxima cambió, así que no basta reponderar o reentrenar con la misma relación —hay que reaprender el nuevo mapeo X→Y, y a menudo detectarlo tarda porque requiere labels frescos.",
    "disparador": "Señal: 'modelo en producción que se degrada'. Jugada: clasifica el shift por probabilidad —P(X)→covariate, P(Y)→label, P(Y|X)→concept drift— con two-sample tests; concept drift = reaprender la relación.",
    "metadata": {
        "ruta": "ml-systems",
        "nivel": 3,
        "skills": ["distribution shift", "covariate/label/concept", "two-sample test", "monitoreo"],
        "errores_comunes": ["Confundir covariate shift (cambia P(X)) con concept drift (cambia P(Y|X))", "Asumir que reentrenar con los mismos datos arregla un concept drift"],
        "casos_borde": ["Sin labels frescos el concept drift es casi indetectable directamente; se usan proxies", "Los tres tipos pueden coexistir, complicando el diagnóstico"],
        "source": "Designing Machine Learning Systems (Chip Huyen) — Cap. 8"
    }
}

# ─── Insertar ─────────────────────────────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        bloque['unidades'].extend(['arena-dmls1', 'arena-dmls2', 'arena-dmls3', 'arena-dmls4'])
        bloque['examen']['items'].extend([ex_next1, ex_next2])
        print(f"fase-7: {len(bloque['unidades'])} unidades, {len(bloque['examen']['items'])} examen items")
        break

for u in [unit_dmls1, unit_dmls2, unit_dmls3, unit_dmls4]:
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
