"""
Tanda 9: Ace the Data Science Interview (Singh & Huo) — 60 preguntas, 4 unidades
================================================================================
Ruta ciencia-datos (§10). IDs calculados dinámicamente sobre la base integrada.

Unidades: arena-ads1 (probabilidad), ads2 (estadística/inferencia),
ads3 (machine learning), ads4 (SQL + product sense / A/B testing).

6 heurísticas nuevas (esquema rico): bias-varianza, regularizacion,
metrica-clasificacion, diagnosticar-metrica, diseno-experimento-ab,
definir-metrica-producto. Se reutilizan las existentes de prob/estadística.
"""

import json

with open('data/study.json', 'r', encoding='utf-8') as f:
    study = json.load(f)

# ─── Heurísticas nuevas ───────────────────────────────────────────────────────
new_heuristicas = [
    {
        "id": "bias-varianza",
        "nombre": "Trade-off sesgo–varianza",
        "descripcion": "Descompón el error en sesgo (modelo demasiado simple, underfitting) y varianza (demasiado sensible al ruido, overfitting), más error irreducible. Diagnostica cuál domina y actúa.",
        "cuando_usar": "Ante un modelo que falla: si va mal en train y test → sesgo (sube complejidad); si va bien en train y mal en test → varianza (regulariza o consigue datos).",
        "ejemplo": "Lineal = alto sesgo/baja varianza; red neuronal = bajo sesgo/alta varianza.",
        "patron": "Underfit↔sesgo, overfit↔varianza; más datos bajan varianza"
    },
    {
        "id": "regularizacion",
        "nombre": "Regularización L1/L2",
        "descripcion": "Penaliza la complejidad del modelo para reducir varianza a costa de algo de sesgo. L2 (Ridge) encoge pesos; L1 (Lasso) los lleva a 0 y selecciona features.",
        "cuando_usar": "Cuando un modelo hace overfit, o cuando quieres un modelo sparse/interpretable (L1) eliminando variables irrelevantes.",
        "ejemplo": "Lasso pone a 0 los coeficientes inútiles → selección automática de features.",
        "patron": "L2=shrink suave, L1=sparse, elastic net=ambos"
    },
    {
        "id": "metrica-clasificacion",
        "nombre": "Elegir la métrica de clasificación",
        "descripcion": "Con clases desbalanceadas, accuracy engaña: razona con precisión (de los marcados positivos, ¿cuántos lo eran?), recall (de los positivos reales, ¿cuántos atrapé?), F1 y ROC/AUC.",
        "cuando_usar": "Siempre que evalúes un clasificador, sobre todo con clases raras. Prioriza recall si un falso negativo es caro (cáncer); precisión si lo caro es el falso positivo (spam).",
        "ejemplo": "99% sanos: predecir 'sano' siempre da 99% accuracy pero 0% recall.",
        "patron": "Desbalance→P/R/F1; costo FP vs FN decide el umbral"
    },
    {
        "id": "diagnosticar-metrica",
        "nombre": "Diagnosticar un cambio de métrica",
        "descripcion": "Ante 'la métrica subió/bajó, ¿por qué?', descarta causas naturales (estacionalidad, evento externo), luego internas caminando hacia arriba por el funnel, segmenta, y separa causa raíz de factor contribuyente y de mera correlación.",
        "cuando_usar": "En preguntas de product sense sobre una métrica que se movió, o ante una alerta en producción.",
        "ejemplo": "Cae el engagement → segmentas por plataforma → un release rompió el feed en Android.",
        "patron": "Natural→interna→segmenta; causa raíz ≠ correlación"
    },
    {
        "id": "diseno-experimento-ab",
        "nombre": "Diseñar un A/B test (y sus trampas)",
        "descripcion": "Plantea H0 sin efecto, elige métrica primaria + guardrails, randomiza control/tratamiento, fija tamaño y duración; y anticipa las trampas: efecto novedad, efectos de red, pruebas múltiples, y que significancia ≠ enviar.",
        "cuando_usar": "Al validar una feature o cambio. Recuerda que un p<0.05 con millones de usuarios puede ser un efecto trivial.",
        "ejemplo": "Pico inicial al lanzar reacciones → efecto novedad; míralo solo en usuarios nuevos.",
        "patron": "H0+guardrails+randomiza; novedad/red/múltiples tests; mira tamaño del efecto"
    },
    {
        "id": "definir-metrica-producto",
        "nombre": "Definir métricas de producto",
        "descripcion": "Elige una North Star alineada con el valor real del producto y acompáñala de métricas guardrail (counter) que no deben empeorar; ubícala en el funnel AARRR.",
        "cuando_usar": "Cuando piden medir el éxito de un lanzamiento o feature. Evita métricas vanidosas; conecta con la misión.",
        "ejemplo": "YouTube: North Star = tiempo viendo videos; guardrail = reportes/insatisfacción.",
        "patron": "North Star + guardrail sobre el funnel AARRR"
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

# ─── arena-ads1: Probabilidad ─────────────────────────────────────────────────
unit_ads1 = {
    "id": "arena-ads1",
    "bloque": "fase-7",
    "orden": max_ord + 1,
    "titulo": "Probabilidad para ciencia de datos",
    "libro": "Ace the Data Science Interview (Singh & Huo)",
    "lectura": "data/teoria/arena-ads1.md",
    "dosis": 30,
    "objetivo": "Aplicar Bayes y la tasa base, la ley de probabilidad total, conteo, distribuciones y cadenas de Markov a problemas de entrevista.",
    "heuristicas": ["bayes-tasa-base", "ley-total-esperanza", "linealidad-esperanza"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 2},
    "ideas_clave": [
        "'Dado que' es la señal de Bayes; la tasa base manda en tests de eventos raros",
        "Descompón por escenarios disjuntos con la ley de probabilidad total",
        "Cada distribución tiene su caso de uso: binomial=conteos binarios, Poisson=eventos/intervalo, exponencial=tiempos de espera"
    ],
    "banco": [
        {"id": "arads1-q1", "tipo": "concepto", "enunciado": "Enuncia el teorema de Bayes nombrando prior, likelihood, evidencia y posterior. ¿Qué palabra en un enunciado suele delatar que toca usarlo?", "solucion": "P(A|B)=P(B|A)P(A)/P(B): P(A) prior, P(B|A) likelihood, P(B) evidencia, P(A|B) posterior. La frase 'dado que' (given that) suele delatar Bayes.", "explicacion": "Bayes invierte la condicional: convierte 'prob. del dato dada la hipótesis' en 'prob. de la hipótesis dado el dato', actualizando el prior con la evidencia."},
        {"id": "arads1-q2", "tipo": "calculo", "enunciado": "Una en mil personas tiene una enfermedad. El test detecta al 98% de los enfermos y tiene 1% de falsos positivos en sanos. Si alguien da positivo, ¿cuál es la probabilidad aproximada de que esté enfermo? ¿Qué enseña el resultado?", "solucion": "P(enf|+) = (0.98·0.001)/(0.98·0.001 + 0.01·0.999) ≈ 0.00098/(0.00098+0.00999) ≈ 0.089 ≈ 9%. Enseña que, con una enfermedad rara, la mayoría de los positivos son falsos pese a un test 'preciso': la tasa base domina.", "explicacion": "Hay muchos más sanos (999) que enfermos (1), así que el 1% de falsos positivos sobre los sanos supera a los verdaderos positivos. Sin la tasa base, diagnosticar por el test es engañoso."},
        {"id": "arads1-q3", "tipo": "calculo", "enunciado": "Dos monedas: una justa (cara/cruz) y una trucada (cruz en ambos lados). Eliges una al azar, la lanzas 5 veces y salen 5 cruces. ¿Probabilidad de que sea la trucada?", "solucion": "P(trucada|5 cruces) = (1·½)/(1·½ + (1/32)·½) = ½/(½ + 1/64) = (32/64)/(33/64) = 32/33 ≈ 0.97.", "explicacion": "Bayes: la trucada da 5 cruces con prob. 1; la justa con prob. (1/2)^5=1/32. El posterior pondera ambas con prior ½, dando 32/33."},
        {"id": "arads1-q4", "tipo": "calculo", "enunciado": "Dos equipos parejos (50% cada uno por juego, sin empates) juegan una serie al mejor de 7 (gana quien llega a 4). ¿Probabilidad de que la serie llegue a 7 juegos?", "solucion": "Que llegue a 7 = tras 6 juegos el marcador es 3-3. P = C(6,3)·(½)^6 = 20/64 = 5/16 ≈ 0.3125.", "explicacion": "El 7º juego ocurre solo si los primeros 6 quedan empatados 3-3. Hay C(6,3)=20 formas de repartir esas victorias, cada secuencia con prob. (½)^6."},
        {"id": "arads1-q5", "tipo": "calculo", "enunciado": "Lanzas un dado tres veces, uno tras otro. ¿Probabilidad de obtener tres números en orden estrictamente creciente?", "solucion": "Hay C(6,3)=20 conjuntos de tres valores distintos, y cada uno se ordena de forma creciente de una sola manera. Total de resultados: 6³=216. P = 20/216 = 5/54 ≈ 0.093.", "explicacion": "Estrictamente creciente exige tres valores distintos; cada terna de valores distintos tiene exactamente un orden creciente entre sus 3!=6 permutaciones."},
        {"id": "arads1-q6", "tipo": "concepto", "enunciado": "Enuncia la ley de probabilidad total y da un ejemplo de cuándo usarla en un problema de negocio.", "solucion": "Si los B_i particionan el espacio: P(A)=Σ P(A|B_i)P(B_i). Ejemplo: la prob. de que un cliente compre se descompone por segmento: P(compra)=Σ P(compra|segmento_i)P(segmento_i).", "explicacion": "Permite calcular una probabilidad marginal sumando sobre escenarios disjuntos ponderados por su probabilidad. Útil cuando el resultado depende de un 'árbol' de casos."},
        {"id": "arads1-q7", "tipo": "concepto", "enunciado": "¿Cuándo usas permutaciones y cuándo combinaciones? Da la fórmula de cada una y un ejemplo cotidiano.", "solucion": "Permutaciones (el orden importa): n!/(n−k)! — ej. contraseñas. Combinaciones (el orden no importa): C(n,k)=n!/(k!(n−k)!) — ej. elegir restaurantes de una lista.", "explicacion": "La distinción clave es si reordenar los mismos elementos cuenta como un resultado distinto. Las combinaciones dividen las permutaciones por k! para descontar los reordenamientos."},
        {"id": "arads1-q8", "tipo": "concepto", "enunciado": "Distingue PMF, PDF y CDF. ¿Qué propiedades cumple toda CDF?", "solucion": "PMF: prob. de cada valor de una v.a. discreta. PDF: densidad de una v.a. continua (la prob. puntual es 0). CDF: F(x)=P(X≤x), suma de la PMF o integral de la PDF. Toda CDF es no negativa y monótona creciente, de 0 a 1.", "explicacion": "PMF/PDF deben sumar/integrar a 1. La CDF acumula la masa de probabilidad hasta x y se usa más en la práctica para calcular P(X≤x)."},
        {"id": "arads1-q9", "tipo": "concepto", "enunciado": "Da la media y la varianza de la binomial(n,p) y de la Poisson(λ), y el caso de uso típico de cada una.", "solucion": "Binomial: media np, varianza np(1−p); cuenta éxitos en n ensayos binarios (caras, signups). Poisson: media λ, varianza λ; cuenta eventos en un intervalo fijo a tasa constante (visitas/hora, defectos/m²).", "explicacion": "La binomial modela un número fijo de ensayos con prob. p; la Poisson, eventos raros en un continuo. Que media=varianza=λ caracteriza a la Poisson."},
        {"id": "arads1-q10", "tipo": "concepto", "enunciado": "¿Qué distribución modela el tiempo entre eventos de un proceso de Poisson y qué propiedad notable tiene? Da su media.", "solucion": "La exponencial(λ), con media 1/λ. Su propiedad notable es la falta de memoria: P(X>s+t | X>s)=P(X>t); el tiempo ya esperado no cambia la distribución del restante.", "explicacion": "Modela tiempos de espera (hasta una compra, hasta un default). La memorylessness la hace única entre las continuas y genera preguntas naturales."},
        {"id": "arads1-q11", "tipo": "concepto", "enunciado": "¿Qué es la propiedad de Markov y qué representa una distribución estacionaria π de una cadena de Markov?", "solucion": "Propiedad de Markov: el próximo estado depende solo del actual (pasado y futuro condicionalmente independientes dado el presente). La estacionaria cumple π=πP y da las proporciones de tiempo a largo plazo en cada estado.", "explicacion": "La cadena 'olvida' su historia más allá del estado actual. π es el punto fijo de la matriz de transición: una vez alcanzada, las transiciones no la cambian."},
        {"id": "arads1-q12", "tipo": "calculo", "enunciado": "Tres amigos en Seattle te dicen que está lloviendo; cada uno miente con prob. 1/3 independientemente. Si la prob. a priori de lluvia un día cualquiera es 0.25, ¿cuál es la probabilidad de que llueva dado que los tres dijeron que sí?", "solucion": "P(lluvia|3 sí) = [0.25·(2/3)³]/[0.25·(2/3)³ + 0.75·(1/3)³] = [0.25·8/27]/[0.25·8/27 + 0.75·1/27] = 2/27 / (2/27 + 0.75/27) = 2/2.75 ≈ 0.727.", "explicacion": "Bayes con likelihoods: si llueve, los tres dicen verdad con (2/3)³; si no, los tres mienten con (1/3)³. El prior 0.25 se actualiza a ~0.73."},
        {"id": "arads1-q13", "tipo": "calculo", "enunciado": "Una baraja de 100 cartas con valores 1..100. Sacas dos sin reemplazo. ¿Probabilidad de que el valor de una sea exactamente el doble del de la otra?", "solucion": "Pares (x,2x) con 2x≤100 → x=1..50 → 50 pares no ordenados favorables. Total de pares: C(100,2)=4950. P = 50/4950 = 1/99 ≈ 0.0101.", "explicacion": "Cada x de 1 a 50 da un único par {x,2x}. Dividimos los 50 pares favorables entre todos los C(100,2) pares posibles."},
        {"id": "arads1-q14", "tipo": "calculo", "enunciado": "Jugadores A y B se turnan lanzando una moneda con prob. p de cara (gana quien saca cara primero). A empieza. ¿Probabilidad de que gane A?", "solucion": "P(A) = p + (1−p)²·p + (1−p)⁴·p + ... = p/(1−(1−p)²) = p/(2p−p²) = 1/(2−p).", "explicacion": "A gana en su 1er tiro (p), o ambos fallan (prob. (1−p)²) y se repite el problema. Serie geométrica con razón (1−p)², que suma 1/(2−p)."},
        {"id": "arads1-q15", "tipo": "concepto", "enunciado": "¿Por qué la distribución normal aparece tan a menudo al modelar fenómenos reales y promedios?", "solucion": "Por el Teorema Central del Límite: la suma/promedio de muchas v.a. independientes tiende a una normal sin importar su distribución original. Por eso medias muestrales y muchos fenómenos agregados son aproximadamente normales.", "explicacion": "Muchos fenómenos reales son sumas de pequeños efectos independientes; el CLT garantiza que esa agregación se aproxima a la campana normal."}
    ]
}

# ─── arena-ads2: Estadística e inferencia ─────────────────────────────────────
unit_ads2 = {
    "id": "arena-ads2",
    "bloque": "fase-7",
    "orden": max_ord + 2,
    "titulo": "Estadística e inferencia",
    "libro": "Ace the Data Science Interview (Singh & Huo)",
    "lectura": "data/teoria/arena-ads2.md",
    "dosis": 30,
    "objetivo": "Dominar LLN, CLT, prueba de hipótesis, p-valores, errores Tipo I/II, intervalos de confianza y estimación MLE/MAP.",
    "heuristicas": ["intervalos-tests", "mle-suficiencia", "escalado-varianza"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 2},
    "ideas_clave": [
        "El CLT (promedio→normal) es el motor del A/B test",
        "El p-valor es P(dato tan extremo | H0), no la prob. de que H0 sea cierta",
        "Tipo I = falso positivo (α); Tipo II = falso negativo (β); potencia = 1−β"
    ],
    "banco": [
        {"id": "arads2-q1", "tipo": "concepto", "enunciado": "Enuncia la Ley de los Grandes Números y el Teorema Central del Límite, y di en qué se diferencian.", "solucion": "LLN: el promedio muestral converge a la esperanza verdadera al crecer n. CLT: la distribución del promedio muestral tiende a una normal al crecer n, sea cual sea la distribución original. La LLN habla del valor al que converge la media; el CLT, de la forma de su distribución.", "explicacion": "La LLN garantiza el 'a dónde' (la media verdadera); el CLT, el 'cómo se distribuye alrededor' (normal), y por eso permite construir tests e intervalos."},
        {"id": "arads2-q2", "tipo": "concepto", "enunciado": "Define correctamente el p-valor. ¿Cuál es la interpretación errónea más común?", "solucion": "p-valor = probabilidad de observar un estadístico al menos tan extremo como el visto, suponiendo que H0 es cierta. El error común es leerlo como 'la probabilidad de que H0 sea cierta', que es falso.", "explicacion": "El p-valor condiciona en H0; no asigna probabilidad a la hipótesis. Un p pequeño solo indica que los datos serían improbables bajo H0."},
        {"id": "arads2-q3", "tipo": "concepto", "enunciado": "Define los errores Tipo I y Tipo II y la potencia de una prueba. ¿Cómo se relacionan con α y β?", "solucion": "Tipo I: rechazar H0 siendo cierta (falso positivo), prob. α. Tipo II: no rechazar H0 siendo falsa (falso negativo), prob. β. Potencia = 1−β = prob. de detectar un efecto real.", "explicacion": "α lo fija el analista (típico 0.05); β depende del tamaño del efecto y de n. Subir n aumenta la potencia sin tocar α."},
        {"id": "arads2-q4", "tipo": "concepto", "enunciado": "Describe los pasos de una prueba de hipótesis aplicada a un A/B test de una campaña de email que busca subir la conversión.", "solucion": "1) H0: las dos versiones tienen igual conversión; H1: la campaña la cambia. 2) Asigna usuarios al azar a control (sin email) y tratamiento (con email). 3) Calcula un estadístico y su p-valor. 4) Compara con α; si p<α, rechazas H0 a favor de que la campaña tuvo efecto.", "explicacion": "El A/B test es prueba de hipótesis aplicada: la nula es 'sin diferencia' y el objetivo es reunir evidencia para rechazarla con significancia."},
        {"id": "arads2-q5", "tipo": "concepto", "enunciado": "¿Qué es un intervalo de confianza del 95% y cuál es su interpretación correcta (y la incorrecta)?", "solucion": "Es un rango producido por un procedimiento que, repetido muchas veces, captura el parámetro verdadero el 95% de las veces. Incorrecto: 'hay 95% de probabilidad de que μ esté en este intervalo concreto' (μ es fijo, no aleatorio).", "explicacion": "La aleatoriedad está en el intervalo (depende de la muestra), no en el parámetro. Es la cobertura del método a largo plazo lo que es 95%."},
        {"id": "arads2-q6", "tipo": "concepto", "enunciado": "¿Qué relación hay entre un intervalo de confianza del 95% y una prueba de hipótesis a α=0.05?", "solucion": "Son complementarios: si el IC del 95% para el parámetro no contiene el valor nulo, rechazas H0 a α=0.05; si lo contiene, no rechazas.", "explicacion": "El IC reúne todos los valores nulos que no se rechazarían; quedar fuera equivale a un resultado significativo a ese nivel."},
        {"id": "arads2-q7", "tipo": "concepto", "enunciado": "Define MLE y MAP y di en qué se diferencian. ¿Cuándo coinciden?", "solucion": "MLE: el parámetro que maximiza la verosimilitud de los datos, argmax L(θ). MAP: el que maximiza el posterior ∝ likelihood × prior. MAP añade un prior bayesiano; coinciden cuando el prior es uniforme.", "explicacion": "MLE usa solo los datos; MAP los combina con una creencia previa. Con prior plano el término del prior es constante y ambos dan el mismo óptimo."},
        {"id": "arads2-q8", "tipo": "calculo", "enunciado": "Sea X uniforme en [a,b]. Deriva su esperanza.", "solucion": "E[X]=∫_a^b x·(1/(b−a))dx = (1/(b−a))·[x²/2]_a^b = (b²−a²)/(2(b−a)) = (a+b)/2.", "explicacion": "La densidad es constante 1/(b−a). Integrar x por esa densidad da el punto medio del intervalo, como dicta la simetría."},
        {"id": "arads2-q9", "tipo": "concepto", "enunciado": "¿Qué prueba usarías para comparar frecuencias observadas vs esperadas en categorías (p.ej. si un dado es justo), y cuál es la forma de su estadístico?", "solucion": "La prueba Chi-cuadrado de bondad de ajuste: χ² = Σ (O_i − E_i)²/E_i, donde O_i es lo observado y E_i lo esperado bajo H0.", "explicacion": "Mide cuánto se desvían los conteos observados de los esperados; valores grandes de χ² dan p-valores pequeños y evidencia contra H0."},
        {"id": "arads2-q10", "tipo": "concepto", "enunciado": "Define covarianza y correlación. ¿Por qué suele preferirse la correlación?", "solucion": "Cov(X,Y)=E[XY]−E[X]E[Y], medida lineal de co-variación con unidades de X·Y. Correlación ρ = Cov(X,Y)/(σ_X σ_Y) ∈ [−1,1], adimensional. Se prefiere ρ porque está normalizada y es comparable entre pares de variables.", "explicacion": "La covarianza depende de la escala de las variables; dividir por las desviaciones la normaliza a un rango fijo interpretable."},
        {"id": "arads2-q11", "tipo": "concepto", "enunciado": "Una prueba con n pequeño no es significativa. Menciona tres formas de aumentar la potencia para detectar un efecto real.", "solucion": "(1) Aumentar el tamaño de muestra n; (2) aumentar el tamaño del efecto detectable o reducir la varianza (mejor diseño/medición); (3) relajar α (a costa de más falsos positivos) o usar un test de una cola si la dirección está justificada.", "explicacion": "La potencia 1−β crece con n y con el tamaño del efecto, y disminuye con la varianza. Subir n es la palanca más limpia porque no sacrifica α."},
        {"id": "arads2-q12", "tipo": "concepto", "enunciado": "¿Por qué con una muestra grande casi cualquier diferencia se vuelve estadísticamente significativa, y qué deberías mirar además del p-valor?", "solucion": "Con n enorme el error estándar se encoge, así que diferencias minúsculas dan p<0.05. Además del p-valor hay que mirar el tamaño del efecto (magnitud práctica) y los costos/guardrails de negocio.", "explicacion": "Significancia estadística ≠ relevancia práctica. Un efecto detectable pero diminuto puede no justificar el cambio; el tamaño del efecto lo aterriza."},
        {"id": "arads2-q13", "tipo": "concepto", "enunciado": "¿Qué es la corrección de Bonferroni y qué problema resuelve?", "solucion": "Resuelve el problema de pruebas múltiples: si corres muchos tests a α, por azar algunos saldrán significativos. Bonferroni ajusta el umbral dividiendo α entre el número de tests (α/m), controlando la tasa de error familiar (FWER).", "explicacion": "Al hacer m comparaciones, la prob. de al menos un falso positivo crece. Exigir α/m por test mantiene la FWER global cerca de α, a costa de potencia."},
        {"id": "arads2-q14", "tipo": "concepto", "enunciado": "Bajo H0, ¿por qué el número de caras en muchos lanzamientos puede tratarse con una normal, y cómo se estandariza?", "solucion": "Por el CLT: la suma de muchos Bernoulli(p) es aproximadamente normal con media np y varianza np(1−p). Se estandariza con Z=(X−np)/√(np(1−p)) ~ N(0,1).", "explicacion": "Aunque cada lanzamiento es discreto, su suma sobre n grande se aproxima a la normal, lo que permite calcular p-valores con la Z."},
        {"id": "arads2-q15", "tipo": "concepto", "enunciado": "¿Qué significa que 'no rechazar H0' no es lo mismo que 'aceptar H0 como verdadera'?", "solucion": "No rechazar H0 solo indica que no hubo evidencia suficiente para descartarla, no que sea cierta. La ausencia de evidencia de un efecto no es evidencia de su ausencia (puede faltar potencia).", "explicacion": "Un test controla el error de rechazar H0 siendo cierta, no el de no detectar un efecto real. Con n chico puedes 'no rechazar' aun existiendo efecto."}
    ]
}

# ─── arena-ads3: Machine Learning ─────────────────────────────────────────────
unit_ads3 = {
    "id": "arena-ads3",
    "bloque": "fase-7",
    "orden": max_ord + 3,
    "titulo": "Machine Learning aplicado",
    "libro": "Ace the Data Science Interview (Singh & Huo)",
    "lectura": "data/teoria/arena-ads3.md",
    "dosis": 30,
    "objetivo": "Razonar sesgo-varianza, regularización, métricas de clasificación, algoritmos clásicos, PCA y descenso de gradiente como en una entrevista.",
    "heuristicas": ["bias-varianza", "regularizacion", "metrica-clasificacion"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 2},
    "ideas_clave": [
        "Sesgo↔underfit, varianza↔overfit: diagnostica cuál domina y actúa",
        "Accuracy engaña con clases desbalanceadas; usa precisión/recall/F1/ROC",
        "L1 da modelos sparse (selección de features); L2 encoge pesos"
    ],
    "banco": [
        {"id": "arads3-q1", "tipo": "concepto", "enunciado": "Explica el trade-off sesgo-varianza como si fuera para un stakeholder no técnico, y di qué harías ante alta varianza y ante alto sesgo.", "solucion": "Sesgo = el modelo es demasiado simple y se equivoca sistemáticamente (underfitting). Varianza = es demasiado sensible y cambia mucho con los datos (overfitting). Alta varianza → consigue más datos o regulariza/simplifica; alto sesgo → aumenta la complejidad del modelo.", "explicacion": "Es el marco central de ML: el error total se reparte entre sesgo, varianza y ruido irreducible. El objetivo es el punto que minimiza la suma, no cada uno por separado."},
        {"id": "arads3-q2", "tipo": "concepto", "enunciado": "¿Qué es el overfitting, cómo lo detectas y por qué los modelos más simples suelen generalizar mejor?", "solucion": "Overfitting: el modelo memoriza el ruido del train y rinde mal fuera de muestra. Se detecta por una gran brecha entre desempeño en train (bueno) y en validación/test (malo). Modelos simples (navaja de Occam) capturan la señal sin el ruido, así que generalizan mejor.", "explicacion": "Un modelo muy flexible ajusta fluctuaciones aleatorias que no se repiten en datos nuevos. La parsimonia reduce la varianza."},
        {"id": "arads3-q3", "tipo": "concepto", "enunciado": "Diferencia la regularización L1 de la L2. ¿Cuál produce modelos sparse y por qué es útil?", "solucion": "L2 (Ridge) penaliza Σwᵢ² y encoge los pesos hacia 0 sin anularlos. L1 (Lasso) penaliza Σ|wᵢ| y lleva pesos exactamente a 0 → modelos sparse, lo que equivale a selección automática de features (útil para interpretar y descartar variables irrelevantes).", "explicacion": "La geometría de la penalización L1 (vértices en los ejes) hace que el óptimo caiga sobre coeficientes nulos; la L2 (círculo) solo los reduce."},
        {"id": "arads3-q4", "tipo": "concepto", "enunciado": "Tienes un dataset con 99% de transacciones legítimas y 1% de fraude. ¿Por qué el accuracy es mala métrica y qué usarías?", "solucion": "Un modelo que prediga 'legítima' siempre logra 99% de accuracy sin detectar ningún fraude. Mejor usar precisión, recall y F1 sobre la clase fraude, y ROC/AUC; aquí el recall importa (atrapar el fraude), vigilando la precisión para no inundar de falsas alarmas.", "explicacion": "Con clases desbalanceadas la accuracy premia a la clase mayoritaria. Las métricas por clase reflejan el desempeño en la clase rara, que es la de interés."},
        {"id": "arads3-q5", "tipo": "concepto", "enunciado": "Define precisión y recall con la matriz de confusión y explica su trade-off con un ejemplo médico.", "solucion": "Precisión = TP/(TP+FP): de los marcados positivos, cuántos lo eran. Recall = TP/(TP+FN): de los positivos reales, cuántos atrapé. En cáncer, alto recall salva vidas (no perder enfermos) pero genera falsas alarmas; alta precisión evita asustar a sanos pero deja escapar enfermos.", "explicacion": "Bajar el umbral sube recall y baja precisión, y viceversa. La elección depende del costo relativo de un falso negativo vs un falso positivo."},
        {"id": "arads3-q6", "tipo": "concepto", "enunciado": "¿Qué es el F1 score y cuándo lo prefieres sobre precisión o recall por separado?", "solucion": "F1 = media armónica de precisión y recall = 2·P·R/(P+R). Se prefiere cuando ambas importan por igual y hay desbalance de clases, porque penaliza que una de las dos sea baja.", "explicacion": "La media armónica castiga los valores pequeños: F1 solo es alto si precisión y recall son ambos altos, evitando inflarlo a costa de uno."},
        {"id": "arads3-q7", "tipo": "concepto", "enunciado": "¿Qué representan la curva ROC y el AUC?", "solucion": "La ROC grafica el True Positive Rate (recall) vs el False Positive Rate al variar el umbral de decisión. El AUC (área bajo la curva) es la probabilidad de que el modelo rankee un positivo aleatorio por encima de un negativo aleatorio; 0.5 = azar, 1 = perfecto.", "explicacion": "La ROC resume el desempeño a todos los umbrales; el AUC lo condensa en un número independiente del umbral y del balance de clases."},
        {"id": "arads3-q8", "tipo": "concepto", "enunciado": "¿Qué es la validación cruzada k-fold y por qué es mejor que un solo train/test split?", "solucion": "Se divide el dato en k pliegues; se entrena con k−1 y se valida con el restante, rotando k veces, y se promedia. Da una estimación más robusta y de menor varianza del desempeño fuera de muestra que un único split, que depende del azar de esa partición.", "explicacion": "Cada observación sirve de validación una vez. Promediar reduce la dependencia de una partición afortunada o desafortunada. El test final se reserva aparte."},
        {"id": "arads3-q9", "tipo": "concepto", "enunciado": "¿Cómo funciona la regresión logística y cuál es su limitación principal?", "solucion": "Pasa una combinación lineal de los features por la sigmoide para producir una probabilidad entre 0 y 1, y se ajusta minimizando la log-loss. Su limitación: asume una frontera de decisión lineal, así que rinde mal cuando la separación entre clases es no lineal.", "explicacion": "Es interpretable y eficiente como baseline. Para fronteras no lineales se recurre a kernels, árboles o ingeniería de features."},
        {"id": "arads3-q10", "tipo": "concepto", "enunciado": "¿Qué supuesto hace Naive Bayes y por qué ese supuesto lo vuelve eficiente?", "solucion": "Asume que los features son condicionalmente independientes dada la clase. Eso reduce los parámetros de orden 2^k (todas las combinaciones) a estimar cada feature por separado, haciéndolo rápido y efectivo incluso con pocos datos (fuerte baseline en texto).", "explicacion": "El supuesto 'naive' rara vez es cierto pero funciona sorprendentemente bien; evita la explosión combinatoria de modelar dependencias entre features."},
        {"id": "arads3-q11", "tipo": "concepto", "enunciado": "Explica bootstrapping y bagging, y cómo los usa un Random Forest para reducir varianza.", "solucion": "Bootstrapping: re-muestrear con reemplazo para crear múltiples datasets. Bagging: entrenar un modelo en cada uno y promediar sus predicciones, lo que reduce la varianza. Random Forest aplica bagging a árboles de decisión y además sub-muestrea features en cada split para decorrelacionarlos.", "explicacion": "Promediar modelos independientes baja la varianza sin subir el sesgo. El sub-muestreo de features evita que todos los árboles se parezcan por culpa de un predictor dominante."},
        {"id": "arads3-q12", "tipo": "concepto", "enunciado": "¿En qué se diferencia el boosting (AdaBoost/XGBoost) del bagging?", "solucion": "Bagging entrena modelos en paralelo sobre muestras bootstrap y promedia (reduce varianza). Boosting entrena modelos en secuencia, cada uno enfocándose en los errores del anterior, y los combina ponderados (reduce sesgo).", "explicacion": "Bagging ataca la varianza con modelos independientes; boosting ataca el sesgo construyendo un modelo fuerte a partir de aprendices débiles encadenados."},
        {"id": "arads3-q13", "tipo": "concepto", "enunciado": "¿Qué hace PCA, sobre qué matriz opera y cuáles son sus dos pitfalls más comunes?", "solucion": "PCA proyecta los datos sobre las direcciones de máxima varianza, que son los eigenvectores de la matriz de covarianza, para reducir dimensión conservando señal. Pitfalls: (1) es sensible a la escala, hay que estandarizar antes; (2) los componentes son combinaciones lineales difíciles de interpretar.", "explicacion": "Los eigenvalores miden la varianza capturada por cada componente. Sin estandarizar, las variables de mayor escala dominan artificialmente los componentes."},
        {"id": "arads3-q14", "tipo": "concepto", "enunciado": "Describe el descenso de gradiente y el rol del learning rate. ¿Qué pasa si es demasiado grande o demasiado pequeño?", "solucion": "Minimiza la pérdida moviéndose en dirección contraria al gradiente: x_{t+1}=x_t − α∇f(x_t). El learning rate α controla el paso: muy grande → oscila o diverge; muy pequeño → converge lentísimo. En funciones no convexas puede quedar atrapado en mínimos locales.", "explicacion": "El gradiente da la dirección de máximo ascenso; restarlo desciende. Ajustar α es clave para converger; SGD usa mini-lotes para escalar a datos grandes."},
        {"id": "arads3-q15", "tipo": "concepto", "enunciado": "¿Cuál es la diferencia entre aprendizaje supervisado y no supervisado? Da un ejemplo de cada uno.", "solucion": "Supervisado: se entrena con datos etiquetados para predecir una salida (regresión lineal para precio de casas, logística para clasificar spam). No supervisado: halla estructura sin etiquetas (k-means para segmentar clientes, PCA para reducir dimensión).", "explicacion": "La distinción es si existe una variable objetivo conocida. El supervisado mapea entradas a salidas; el no supervisado descubre patrones o grupos latentes."}
    ]
}

# ─── arena-ads4: SQL y product sense ──────────────────────────────────────────
unit_ads4 = {
    "id": "arena-ads4",
    "bloque": "fase-7",
    "orden": max_ord + 4,
    "titulo": "SQL y product sense / A·B testing",
    "libro": "Ace the Data Science Interview (Singh & Huo)",
    "lectura": "data/teoria/arena-ads4.md",
    "dosis": 30,
    "objetivo": "Traducir negocio a SQL (joins, CTEs, window functions) y razonar producto: definir métricas, diagnosticar cambios y diseñar A/B tests evitando sus trampas.",
    "heuristicas": ["ventana-sql", "definir-metrica-producto", "diagnosticar-metrica", "diseno-experimento-ab"],
    "metadata": {"ruta": "ciencia-datos", "nivel": 2},
    "ideas_clave": [
        "SQL: trabaja hacia atrás desde la tabla ideal; window functions para rankings y retención",
        "Métricas: North Star + guardrail sobre el funnel AARRR",
        "A/B test: cuidado con novedad, efectos de red, pruebas múltiples; significancia ≠ enviar"
    ],
    "banco": [
        {"id": "arads4-q1", "tipo": "concepto", "enunciado": "Describe la táctica de 'trabajar hacia atrás' para escribir una consulta SQL compleja con varios joins y CTEs.", "solucion": "Imagina que ya tienes una única tabla ideal con todas las columnas que necesitas, de modo que la respuesta sería un solo SELECT. Desde ahí retrocede un paso a la vez (qué join, subquery o CTE produce esa tabla) hasta llegar a las tablas reales, en vez de resolver todas las piezas a la vez.", "explicacion": "Descompone un query intimidante en pasos manejables y legibles (CTEs encadenadas), reduciendo la carga cognitiva."},
        {"id": "arads4-q2", "tipo": "concepto", "enunciado": "¿Cuál es la diferencia entre WHERE y HAVING en SQL?", "solucion": "WHERE filtra filas ANTES de agrupar (sobre columnas individuales); HAVING filtra DESPUÉS de agrupar (sobre resultados de agregaciones como COUNT o SUM). Ej.: HAVING COUNT(*)>5 para grupos con más de 5 filas.", "explicacion": "El orden lógico es WHERE → GROUP BY → HAVING. No puedes filtrar por un agregado en WHERE porque aún no se ha calculado."},
        {"id": "arads4-q3", "tipo": "concepto", "enunciado": "¿Qué hace una window function que un GROUP BY no puede, y da dos funciones de ventana útiles con su caso de uso?", "solucion": "Calcula sobre una ventana de filas SIN colapsarlas (conserva el detalle por fila). Ejemplos: RANK() OVER (PARTITION BY categoria ORDER BY ventas DESC) para top-N por categoría; LAG() OVER (ORDER BY mes) para comparar con el mes previo (retención/deltas).", "explicacion": "GROUP BY reduce cada grupo a una fila; las window functions agregan manteniendo todas las filas, ideales para rankings y comparaciones entre filas."},
        {"id": "arads4-q4", "tipo": "concepto", "enunciado": "¿Cómo calcularías la retención mes a mes de usuarios con SQL, conceptualmente?", "solucion": "Self-join o window: relaciona la actividad de cada usuario en el mes M con su actividad en el mes M+1 (p.ej. con LAG o un join sobre user_id y mes+1). La retención del mes es la fracción de usuarios activos en M que siguen activos en M+1.", "explicacion": "Requiere comparar cada cohorte consigo misma en el periodo siguiente; un self-join por user_id y mes desplazado, o funciones de ventana, lo resuelven."},
        {"id": "arads4-q5", "tipo": "concepto", "enunciado": "¿Qué es una métrica North Star y por qué siempre debe acompañarse de métricas guardrail (counter)?", "solucion": "La North Star es la métrica única más alineada con el valor real del producto (ej. tiempo viendo videos en YouTube). Las guardrail evitan que se infle la principal a costa de algo dañino (ej. subir notificaciones sube clics pero hunde la retención); por eso siempre van juntas.", "explicacion": "Optimizar una sola métrica invita a gamearla. Los guardrails ponen límites que protegen la salud global del producto y del negocio."},
        {"id": "arads4-q6", "tipo": "concepto", "enunciado": "Nombra las etapas del funnel de adquisición AARRR (pirate metrics) y para qué sirve el marco.", "solucion": "Acquisition, Activation, Retention, Referral, Revenue. Sirve para ubicar métricas y razonar dónde está el problema u oportunidad: cada etapa tiene sus propias métricas y un mismo cambio puede afectar una etapa y no otra.", "explicacion": "El funnel ordena el ciclo de vida del usuario; pensar por etapas ayuda a definir métricas y a diagnosticar en qué punto se rompe la conversión."},
        {"id": "arads4-q7", "tipo": "concepto", "enunciado": "Te dicen que el engagement de un producto cayó esta semana. Esboza un marco para diagnosticar la causa.", "solucion": "1) ¿Cambio natural? Estacionalidad, día de la semana, evento externo (feriado, competidor). 2) ¿Causa interna? Camina hacia arriba por el funnel: ¿hubo un release, bug, cambio de UI? ¿una feature canibaliza a otra? 3) Segmenta por plataforma/país/versión/cohorte para localizar dónde ocurre. 4) Distingue causa raíz de factor contribuyente y de mera correlación.", "explicacion": "El error común es saltar a una causa; el marco descarta primero lo externo, luego rastrea internamente por el funnel y segmenta hasta aislar la causa raíz."},
        {"id": "arads4-q8", "tipo": "concepto", "enunciado": "Distingue causa raíz, factor contribuyente y resultado correlacionado al diagnosticar un cambio de métrica.", "solucion": "Causa raíz: el origen real del cambio (ej. menos comentarios por post). Factor contribuyente: ayuda pero no es el origen. Resultado correlacionado: un síntoma que se mueve junto pero no causa el cambio. Confundirlos lleva a 'arreglar' un síntoma.", "explicacion": "Solo actuar sobre la causa raíz corrige el problema; tratar correlaciones o síntomas desperdicia esfuerzo y puede empeorar las cosas."},
        {"id": "arads4-q9", "tipo": "concepto", "enunciado": "Esboza cómo diseñarías un A/B test para una nueva feature: qué defines antes de lanzarlo.", "solucion": "Plantea H0 (la feature no cambia la métrica), elige una métrica primaria alineada con el objetivo + métricas guardrail, calcula el tamaño de muestra y la duración necesarios, y asigna usuarios al azar a control y tratamiento (grupos balanceados).", "explicacion": "Definir la hipótesis, las métricas y el tamaño de muestra de antemano evita p-hacking y asegura potencia suficiente para detectar el efecto buscado."},
        {"id": "arads4-q10", "tipo": "concepto", "enunciado": "¿Qué es el efecto novedad en un A/B test y cómo lo detectas y mitigas?", "solucion": "Es un pico inicial de la métrica porque usuarios curiosos prueban lo nuevo; luego se estabiliza más bajo. Se detecta mirando el efecto solo en usuarios nuevos (que no conocían lo anterior) o corriendo el test más tiempo hasta que la métrica se asiente.", "explicacion": "El entusiasmo inicial sobreestima el efecto a largo plazo. Aislar usuarios nuevos o extender el test separa la curiosidad del valor sostenido."},
        {"id": "arads4-q11", "tipo": "concepto", "enunciado": "Explica por qué los efectos de red sesgan un A/B test en una red social y cómo mitigarlo.", "solucion": "El supuesto de independencia se rompe: la mayor actividad del grupo tratamiento contagia a sus amigos en control (spillover), subestimando el efecto real. Mitigación: asignar clusters de usuarios conectados al mismo grupo (partición del grafo social) para aislar tratamiento de control.", "explicacion": "Si control y tratamiento interactúan, la diferencia medida se contamina. Agrupar por comunidades reduce la interferencia entre grupos."},
        {"id": "arads4-q12", "tipo": "concepto", "enunciado": "¿Qué es el problema de pruebas múltiples y cómo se controla?", "solucion": "Si corres muchos tests a α=0.05, por puro azar algunos darán 'significativos' (falsos positivos). Se controla con la corrección de Bonferroni (usar α/m) o controlando la FDR (FP/(FP+TP)) o la FWER (prob. de ≥1 error Tipo I).", "explicacion": "Cada test tiene 5% de falso positivo; con muchos, la probabilidad de al menos uno se dispara. Las correcciones endurecen el umbral para compensar."},
        {"id": "arads4-q13", "tipo": "concepto", "enunciado": "Tu A/B test da p<0.05 a favor del tratamiento. ¿Por qué eso no implica automáticamente lanzar la feature?", "solucion": "Porque con muchos usuarios un efecto trivial alcanza significancia: hay que evaluar el tamaño del efecto (¿es prácticamente relevante?) y qué pasó con los guardrails (si revenue sube pero retención baja, la decisión no es obvia y se consulta con negocio).", "explicacion": "Significancia estadística ≠ relevancia práctica ni decisión de negocio. El tamaño del efecto y los trade-offs entre métricas determinan si conviene enviar."},
        {"id": "arads4-q14", "tipo": "concepto", "enunciado": "Al enfrentar una pregunta abierta de product sense ('¿deberíamos lanzar X?'), ¿cuáles son los primeros pasos del marco recomendado?", "solucion": "Hacer preguntas aclaratorias (quién es el usuario, cuál es el flujo, qué meta de negocio se persigue), acotar el problema (decir qué dejas fuera por tiempo), pensar en voz alta y mantener la misión de la empresa al frente. Mentalidad: actúa como si ya trabajaras ahí, charlando con un colega.", "explicacion": "Estas preguntas evalúan el proceso de pensamiento. Aclarar y acotar evita ir por el camino equivocado y demuestra criterio de producto."},
        {"id": "arads4-q15", "tipo": "concepto", "enunciado": "Un PM quiere reemplazar un feed cronológico por uno rankeado por ML. ¿Qué métricas primaria y guardrail propondrías y por qué?", "solucion": "Primaria: una de engagement alineada con el valor (ej. tiempo de sesión o interacciones por usuario). Guardrails: retención a 7/30 días, reportes/quejas, diversidad de contenido y notificaciones, para detectar si el ranking infla el engagement a corto plazo dañando la salud a largo plazo.", "explicacion": "Un feed rankeado puede subir clics pero crear adicción/insatisfacción o cámaras de eco; los guardrails protegen contra optimizar un número a costa de la experiencia."}
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
    "heuristica": "diseno-experimento-ab",
    "enunciado": "Lanzas una nueva pantalla de inicio en una app social y el A/B test muestra +12% de engagement en el grupo tratamiento durante la primera semana, con p<0.001. El PM quiere enviarla ya. (a) ¿Qué tres amenazas a la validez revisarías antes de concluir? (b) ¿cómo distinguirías un efecto novedad de uno real? (c) ¿basta el p<0.001 para decidir?",
    "pistas": [
        "El grupo control y el tratamiento, ¿son realmente independientes en una red social?",
        "Una semana es poco: ¿qué pasa con usuarios curiosos que entran solo a ver lo nuevo?",
        "Piensa en novedad, efectos de red y en qué pasó con las métricas guardrail; ¿se corrieron otros tests a la vez?",
        "Efecto novedad: mira el efecto SOLO en usuarios nuevos (que no conocían la pantalla vieja) o extiende el test hasta que la métrica se estabilice.",
        "p<0.001 con millones de usuarios puede reflejar un efecto trivial: evalúa el tamaño del efecto y los guardrails (retención, reportes), no solo la significancia."
    ],
    "solucion": "(a) Efecto novedad (pico inicial por curiosidad), efectos de red (el tratamiento contamina al control vía spillover social, sesgando la diferencia) y pruebas múltiples / guardrails (¿bajó la retención o subieron los reportes? ¿se corrían otros experimentos?). (b) Analiza el efecto solo en usuarios nuevos o corre el test varias semanas: si el +12% se desvanece al estabilizarse, era novedad. (c) No: con n enorme cualquier efecto es significativo; hay que mirar el tamaño del efecto y los guardrails antes de enviar.",
    "disparador": "Señal: 'A/B test con resultado positivo, ¿lo lanzamos?'. Jugada: revisa novedad, efectos de red y pruebas múltiples; separa significancia de tamaño del efecto; consulta guardrails.",
    "metadata": {
        "ruta": "ciencia-datos",
        "nivel": 3,
        "skills": ["diseño de A/B test", "efecto novedad", "efectos de red", "significancia vs tamaño del efecto"],
        "errores_comunes": ["Tomar p<0.05 como decisión de lanzamiento", "Ignorar el spillover entre control y tratamiento en redes sociales"],
        "casos_borde": ["Si los usuarios nuevos no se parecen a los tenured, testear solo en ellos sesga", "Efecto primacía: el signo opuesto a la novedad (aversión inicial al cambio)"],
        "source": "Ace the Data Science Interview (Singh & Huo) — Cap. 10"
    }
}

ex_next2 = {
    "id": f"f7-ex-{next_id2}",
    "heuristica": "metrica-clasificacion",
    "enunciado": "Construyes un clasificador para detectar fraude; el 0.5% de las transacciones son fraudulentas. Tu modelo reporta 99.4% de accuracy y el equipo lo quiere desplegar. (a) ¿Por qué la accuracy es engañosa aquí? (b) ¿qué métricas usarías y cuál priorizarías? (c) ¿cómo decidirías el umbral de decisión?",
    "pistas": [
        "¿Qué accuracy obtendría un modelo que SIEMPRE dice 'no fraude'?",
        "Con 0.5% de positivos, la clase de interés es minúscula: ¿qué métricas miran la clase rara?",
        "Define precisión (TP/(TP+FP)) y recall (TP/(TP+FN)); ¿qué cuesta más, un fraude no detectado o una transacción legítima bloqueada?",
        "Prioriza recall para no dejar pasar fraude, pero vigila la precisión para no bloquear demasiadas compras legítimas; el F1 equilibra ambas.",
        "El umbral sale del trade-off precisión-recall según el costo de FP vs FN; usa la curva ROC/PR para elegirlo, no un 0.5 por defecto."
    ],
    "solucion": "(a) Un modelo trivial que prediga 'no fraude' siempre logra 99.5% de accuracy sin atrapar ningún fraude: la accuracy premia la clase mayoritaria. (b) Precisión, recall, F1 y AUC sobre la clase fraude; se prioriza recall (no dejar pasar fraude), vigilando la precisión para no bloquear demasiadas transacciones legítimas. (c) El umbral se fija según el costo relativo de un falso negativo (fraude perdido) vs un falso positivo (compra legítima bloqueada), eligiéndolo sobre la curva ROC/precision-recall, no en 0.5 por defecto.",
    "disparador": "Señal: 'clasificador con clases muy desbalanceadas y accuracy alta'. Jugada: descarta accuracy; razona precisión/recall/F1/AUC y fija el umbral por el costo de FP vs FN.",
    "metadata": {
        "ruta": "ciencia-datos",
        "nivel": 2,
        "skills": ["métricas de clasificación", "clases desbalanceadas", "trade-off precisión-recall", "selección de umbral"],
        "errores_comunes": ["Reportar accuracy con clases desbalanceadas", "Dejar el umbral en 0.5 sin considerar el costo asimétrico de los errores"],
        "casos_borde": ["Si el costo de un FP es altísimo (bloquear clientes), conviene priorizar precisión", "Con clases extremadamente raras, la curva precision-recall informa mejor que la ROC"],
        "source": "Ace the Data Science Interview (Singh & Huo) — Cap. 7"
    }
}

# ─── Insertar ─────────────────────────────────────────────────────────────────
for bloque in study['bloques']:
    if bloque['id'] == 'fase-7':
        bloque['unidades'].extend(['arena-ads1', 'arena-ads2', 'arena-ads3', 'arena-ads4'])
        bloque['examen']['items'].extend([ex_next1, ex_next2])
        print(f"fase-7: {len(bloque['unidades'])} unidades, {len(bloque['examen']['items'])} examen items")
        break

for u in [unit_ads1, unit_ads2, unit_ads3, unit_ads4]:
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
