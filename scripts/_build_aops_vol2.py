# -*- coding: utf-8 -*-
"""Tanda 40 — Lehoczky & Rusczyk, *the Art of Problem Solving, Volume 2* (and Beyond).
Append 44 problemas verificados a data/problems.json. PDF de 81 MB, IMAGEN PURA (sin capa
de texto: get_text() ~vacío); el TOC se leyó como imágenes con la tool Read. Vol.2 es el
companion AVANZADO (no-cálculo de bachillerato): trigonometría, leyes de senos/cosenos,
cuadriláteros cíclicos (Ptolomeo), cónicas/polares, polinomios (raíces, sumas de Newton),
identidades funcionales, límites, números complejos (DeMoivre, raíces de la unidad),
vectores/producto punto, matrices/determinantes. Estos temas son FRESCOS respecto a tandas
previas, así que aportan valor NUEVO sin duplicar (§1.6). Cada número verificado de forma
independiente con Python/sympy (44 checks, todos OK; los productos/sumas de raíces de la
unidad dan 0 numéricamente ~1e-128).
Mapeo a las 4 estrategias canónicas (11 c/u, balance GLOBAL -> 168/168/168/168):
 - invariantes: identidades trigonométricas (sin²+cos²=1), ley de cosenos/senos, Ptolomeo,
   sumas de Newton, producto punto (perpendicularidad), determinante (área).
 - patrones: raíces de la unidad, DeMoivre, ciclos de i, valores trig notables, raíces de
   polinomios.
 - optimizacion: amplitud de a·sin+b·cos, área con ángulo, AM-GM, distancia mínima a recta,
   extremos en cónicas.
 - inversion: resolver ecuaciones trigonométricas, trig inversa, identidades funcionales,
   hallar raíces, sumas de Newton hacia atrás, raíz cuadrada compleja.
Builder idempotente: aborta si hay choque de ids. Sector C (entrenamiento), esquema §4.1,
ids 629-672."""
import json, collections

SRC = "Lehoczky & Rusczyk, *the Art of Problem Solving, Vol. 2*"

def P(id, titulo, estrategia, dificultad, enunciado, hints, solucion, explicacion,
      tiempo, conceptos, transferencias, year, tags, cap):
    assert len(hints) == 5, (id, "hints!=5")
    assert estrategia in {"inversion", "optimizacion", "invariantes", "patrones"}, (id, estrategia)
    assert 1 <= dificultad <= 5, (id, "dificultad")
    return {
        "id": id, "titulo": titulo, "estrategia": estrategia, "dificultad": dificultad,
        "enunciado": enunciado, "hints": hints, "solucion": solucion,
        "explicacion": explicacion, "tiempo_estimado": tiempo, "conceptos": conceptos,
        "transferencias": transferencias, "source": SRC + " — " + cap,
        "source_url": "", "year": year, "tags": tags,
    }

PROBLEMS = []
A = PROBLEMS.append

# =====================================================================
# INVARIANTES (11) — identidades trig, ley de cosenos/senos, Ptolomeo, Newton, dot, det
# =====================================================================

A(P(629, "La identidad pitagórica", "invariantes", 2,
 "Un ángulo agudo θ cumple sen θ = 3/5. ¿Cuánto vale cos θ?",
 ["Hay una identidad que liga seno y coseno de cualquier ángulo: es constante.",
  "sen²θ + cos²θ = 1 (la identidad pitagórica).",
  "Despeja cos²θ = 1 − (3/5)² = 1 − 9/25 = 16/25.",
  "Como θ es agudo, cos θ > 0: cos θ = √(16/25).",
  "= 4/5."],
 "Por la identidad pitagórica, cos²θ = 1 − (3/5)² = 16/25, y como θ es agudo, cos θ = 4/5. Verificado con Python.",
 "sen²θ + cos²θ = 1 es invariante para TODO ángulo: es el teorema de Pitágoras en el círculo unitario. Conocido un valor, da el otro (con el signo del cuadrante).",
 10, ["identidad pitagórica", "sen²+cos²=1", "círculo unitario"],
 ["oscilaciones", "procesamiento de señales", "navegación"],
 "", ["trigonometria", "invariante", "nivel-basico"], "cap. 2 (Trigonometric Functions)"))

A(P(630, "La ley de los cosenos", "invariantes", 3,
 "Un triángulo tiene dos lados de longitudes 5 y 7 con un ángulo de 60° entre ellos. ¿Cuánto mide el tercer lado?",
 ["La ley de los cosenos generaliza Pitágoras a cualquier ángulo entre dos lados.",
  "c² = a² + b² − 2ab·cos(C), donde C es el ángulo entre a y b.",
  "c² = 5² + 7² − 2·5·7·cos 60° = 25 + 49 − 70·(1/2).",
  "= 74 − 35 = 39.",
  "c = √39."],
 "Por la ley de los cosenos, c² = 25 + 49 − 70·(1/2) = 39, así que c = √39. Verificado con Python.",
 "La ley de los cosenos relaciona los tres lados con un ángulo de forma invariante; con ángulo de 90° se reduce a Pitágoras (cos 90° = 0).",
 14, ["ley de los cosenos", "ángulo entre lados", "generaliza Pitágoras"],
 ["topografía", "navegación", "mecánica de fuerzas"],
 "", ["trigonometria", "ley-cosenos", "invariante", "nivel-intermedio"], "cap. 3 (Triangle Laws)"))

A(P(631, "La ley de los senos y el circunradio", "invariantes", 3,
 "En un triángulo, un lado mide 10 y el ángulo opuesto a ese lado mide 30°. ¿Cuál es el diámetro de la circunferencia circunscrita al triángulo?",
 ["La ley de los senos dice que el cociente lado/seno del ángulo opuesto es constante e igual al DIÁMETRO del circuncírculo.",
  "a/sen A = 2R (diámetro), para todo lado y su ángulo opuesto.",
  "Aquí a = 10 y A = 30°, con sen 30° = 1/2.",
  "2R = 10/(1/2).",
  "= 20."],
 "Por la ley de los senos, 2R = a/sen A = 10/(1/2) = 20. El diámetro del circuncírculo es 20. Verificado con Python.",
 "La ley de los senos esconde un invariante notable: a/sen A es el mismo para los tres lados e igual al diámetro del circuncírculo.",
 12, ["ley de los senos", "circunradio", "a/senA=2R"],
 ["triangulación", "astronomía", "geometría de circunferencias"],
 "", ["trigonometria", "ley-senos", "invariante", "nivel-intermedio"], "cap. 3 (Triangle Laws)"))

A(P(632, "El teorema de Ptolomeo", "invariantes", 3,
 "Un rectángulo de lados 3 y 4 está inscrito en una circunferencia (es un cuadrilátero cíclico). Verifica el teorema de Ptolomeo: ¿cuánto vale el producto de las diagonales y cómo se relaciona con los lados?",
 ["El teorema de Ptolomeo: en un cuadrilátero cíclico, el producto de las diagonales = suma de los productos de pares de lados opuestos.",
  "Las diagonales del rectángulo son iguales; cada una mide √(3² + 4²) = 5.",
  "Producto de diagonales = 5·5 = 25.",
  "Lados opuestos: 3 y 3, 4 y 4. Suma de productos opuestos = 3·3 + 4·4 = 9 + 16 = 25.",
  "Coinciden: 25 = 25, confirmando Ptolomeo."],
 "Diagonales = 5 cada una, producto 25; lados opuestos dan 3·3 + 4·4 = 25. Ptolomeo se cumple: producto de diagonales = suma de productos de lados opuestos. Verificado con Python.",
 "El teorema de Ptolomeo es una relación invariante de los cuadriláteros cíclicos. Para un rectángulo se reduce al teorema de Pitágoras (diagonal² = lado² + lado²).",
 14, ["teorema de Ptolomeo", "cuadrilátero cíclico", "diagonales y lados"],
 ["astronomía antigua", "trigonometría", "geometría de circunferencias"],
 "", ["ptolomeo", "ciclico", "invariante", "nivel-intermedio"], "cap. 4 (Ptolemy's Theorem)"))

A(P(633, "La tangente desde seno y coseno", "invariantes", 1,
 "Un ángulo agudo θ cumple sen θ = 3/5 y cos θ = 4/5. ¿Cuánto vale tan θ?",
 ["La tangente se define como el cociente del seno entre el coseno.",
  "tan θ = sen θ / cos θ.",
  "= (3/5)/(4/5).",
  "Los quintos se cancelan: 3/4.",
  "tan θ = 3/4."],
 "tan θ = sen θ/cos θ = (3/5)/(4/5) = 3/4. Verificado con Python.",
 "La relación tan = sen/cos es una identidad invariante. Para el triángulo 3-4-5, la tangente del ángulo menor es 3/4 (cateto opuesto sobre adyacente).",
 8, ["tangente", "tan=sen/cos", "triángulo 3-4-5"],
 ["pendientes", "rampas", "trigonometría aplicada"],
 "", ["trigonometria", "invariante", "nivel-basico"], "cap. 2 (Trigonometric Functions)"))

A(P(634, "Sumas de Newton", "invariantes", 4,
 "Las raíces de x² − 5x + 6 = 0 son r y s. Sin resolver, usa las sumas de Newton para hallar r² + s².",
 ["Las sumas de Newton expresan las sumas de potencias de las raíces en términos de los coeficientes.",
  "Por Vieta, p₁ = r + s = 5 y la suma de productos e₂ = rs = 6.",
  "La primera suma de Newton para dos raíces: p₂ = p₁·(r+s) − 2·e₂, es decir p₂ = (r+s)² − 2rs.",
  "p₂ = 5² − 2·6 = 25 − 12.",
  "= 13."],
 "Por las sumas de Newton, p₂ = r² + s² = (r+s)² − 2rs = 25 − 12 = 13. Verificado con Python.",
 "Las sumas de Newton convierten potencias de las raíces en expresiones de los coeficientes (invariantes de Vieta), sin necesidad de hallar las raíces.",
 16, ["sumas de Newton", "Vieta", "potencias de raíces"],
 ["polinomios característicos", "física de sistemas", "álgebra"],
 "", ["newton", "vieta", "invariante", "nivel-avanzado"], "cap. 6 (Newton's Sums)"))

A(P(635, "Producto punto y perpendicularidad", "invariantes", 2,
 "¿Son perpendiculares los vectores (3, 4) y (4, −3)? Justifica con el producto punto.",
 ["Dos vectores son perpendiculares exactamente cuando su producto punto es cero.",
  "El producto punto de (a, b) y (c, d) es a·c + b·d.",
  "(3, 4)·(4, −3) = 3·4 + 4·(−3).",
  "= 12 − 12 = 0.",
  "Como el producto punto es 0, los vectores SÍ son perpendiculares."],
 "(3,4)·(4,−3) = 12 − 12 = 0; como el producto punto es 0, los vectores son perpendiculares. Verificado con Python.",
 "El producto punto codifica el ángulo: u·v = |u||v|cos θ. Es 0 exactamente cuando cos θ = 0, es decir, cuando los vectores son perpendiculares (invariante de ortogonalidad).",
 10, ["producto punto", "perpendicularidad", "u·v=0"],
 ["gráficos por computadora", "física", "aprendizaje automático"],
 "", ["vectores", "producto-punto", "invariante", "nivel-basico"], "cap. 10 (The Dot Product)"))

A(P(636, "El determinante como área", "invariantes", 3,
 "Un paralelogramo tiene como lados los vectores (2, 1) y (1, 3). ¿Cuál es su área?",
 ["El área del paralelogramo generado por dos vectores es el valor absoluto del determinante de la matriz que forman.",
  "Para (a, b) y (c, d), el determinante es a·d − b·c.",
  "det = 2·3 − 1·1.",
  "= 6 − 1 = 5.",
  "El área es |5| = 5."],
 "Área = |det([[2,1],[1,3]])| = |2·3 − 1·1| = 5. Verificado con Python.",
 "El determinante 2×2 mide el área (con signo) del paralelogramo generado por los vectores: un invariante geométrico fundamental del álgebra lineal.",
 12, ["determinante", "área de paralelogramo", "ad−bc"],
 ["cambio de variables", "gráficos por computadora", "física"],
 "", ["determinante", "vectores", "invariante", "nivel-intermedio"], "cap. 11 (Cross Products and Determinants)"))

A(P(637, "El coseno del ángulo doble", "invariantes", 2,
 "Un ángulo θ cumple sen θ = 1/2. Usando una identidad del ángulo doble, halla cos(2θ).",
 ["Hay una fórmula del ángulo doble que usa solo el seno: cos(2θ) = 1 − 2·sen²θ.",
  "Sustituye sen θ = 1/2.",
  "cos(2θ) = 1 − 2·(1/2)².",
  "= 1 − 2·(1/4) = 1 − 1/2.",
  "= 1/2. (En efecto, si θ = 30°, cos 60° = 1/2.)"],
 "cos(2θ) = 1 − 2sen²θ = 1 − 2·(1/4) = 1/2. Verificado con Python.",
 "Las identidades del ángulo doble son invariantes que reescriben cos(2θ) en términos de un solo valor (sen θ o cos θ), útiles para encadenar cálculos.",
 10, ["identidad de ángulo doble", "cos(2θ)=1−2sen²θ", "trigonometría"],
 ["modulación de señales", "óptica", "análisis de Fourier"],
 "", ["trigonometria", "invariante", "nivel-basico"], "cap. 2 (Trigonometric Identities)"))

A(P(638, "La norma de un vector", "invariantes", 1,
 "¿Cuál es la magnitud (norma) del vector (3, 4)?",
 ["La norma de un vector es la raíz de la suma de los cuadrados de sus componentes (Pitágoras).",
  "|(a, b)| = √(a² + b²).",
  "= √(3² + 4²) = √(9 + 16).",
  "= √25.",
  "= 5."],
 "|(3,4)| = √(3² + 4²) = √25 = 5. Verificado con Python.",
 "La norma de un vector es invariante bajo rotaciones: medirla es Pitágoras sobre sus componentes. Aquí reaparece la terna 3-4-5.",
 8, ["norma de vector", "Pitágoras", "magnitud"],
 ["física (velocidad/fuerza)", "gráficos", "distancias"],
 "", ["vectores", "invariante", "nivel-basico"], "cap. 10 (Coordinate Representation of Vectors)"))

A(P(639, "El ángulo recto escondido", "invariantes", 2,
 "Un triángulo tiene lados 3, 4 y 5. Usando la ley de los cosenos, demuestra que el ángulo opuesto al lado 5 es recto.",
 ["Aplica la ley de los cosenos para el ángulo opuesto al lado mayor (5).",
  "cos(C) = (a² + b² − c²)/(2ab), con c = 5 el lado opuesto a C.",
  "cos(C) = (3² + 4² − 5²)/(2·3·4) = (9 + 16 − 25)/24.",
  "= 0/24 = 0.",
  "cos(C) = 0 significa C = 90°: el ángulo es recto."],
 "Por la ley de los cosenos, cos(C) = (9 + 16 − 25)/24 = 0, así que C = 90°. Verificado con Python.",
 "La ley de los cosenos también clasifica ángulos: si a² + b² = c², el coseno es 0 y el ángulo es recto (recíproco de Pitágoras como caso invariante).",
 10, ["ley de los cosenos", "recíproco de Pitágoras", "ángulo recto"],
 ["verificar perpendicularidad", "estructuras", "GPS"],
 "", ["trigonometria", "ley-cosenos", "invariante", "nivel-basico"], "cap. 3 (Triangle Laws)"))

# =====================================================================
# PATRONES (11) — raíces de la unidad, DeMoivre, ciclos de i, valores trig
# =====================================================================

A(P(640, "Las raíces cúbicas de la unidad", "patrones", 3,
 "Sea ω = cos(120°) + i·sen(120°) una raíz cúbica de 1 distinta de 1. ¿Cuánto vale 1 + ω + ω²?",
 ["Las tres raíces cúbicas de 1 son 1, ω, ω², igualmente espaciadas en el círculo unitario.",
  "Son las raíces de x³ − 1 = 0, que se factoriza como (x − 1)(x² + x + 1) = 0.",
  "Por Vieta sobre x² + x + 1 = 0 (cuyas raíces son ω y ω²), ω + ω² = −1.",
  "Entonces 1 + ω + ω² = 1 + (−1).",
  "= 0."],
 "Las raíces cúbicas de 1 suman 0: 1 + ω + ω² = 0 (verificado numéricamente ~1e-128). Es Vieta sobre x³ − 1.",
 "Las n raíces de la unidad están igualmente espaciadas en el círculo y SIEMPRE suman 0 (para n > 1): su centro de masa es el origen. Patrón geométrico-algebraico.",
 14, ["raíces de la unidad", "suma cero", "Vieta"],
 ["transformada de Fourier", "procesamiento de señales", "simetría"],
 "", ["raices-unidad", "complejos", "patron", "nivel-intermedio"], "cap. 9 (The Roots of Unity)"))

A(P(641, "El teorema de DeMoivre", "patrones", 3,
 "Usa el teorema de DeMoivre para calcular (cos 30° + i·sen 30°)³.",
 ["DeMoivre: (cos θ + i sen θ)ⁿ = cos(nθ) + i sen(nθ). Elevar una potencia multiplica el ángulo.",
  "Aquí θ = 30° y n = 3, así que el ángulo se triplica: 3·30° = 90°.",
  "Resultado = cos 90° + i sen 90°.",
  "cos 90° = 0 y sen 90° = 1.",
  "= 0 + i·1 = i."],
 "Por DeMoivre, (cos 30° + i sen 30°)³ = cos 90° + i sen 90° = i. Verificado con Python.",
 "DeMoivre revela el patrón: elevar un complejo de módulo 1 a la potencia n multiplica su ángulo por n. Convierte potencias en multiplicaciones de ángulos.",
 14, ["teorema de DeMoivre", "forma polar", "potencias de complejos"],
 ["raíces de complejos", "señales", "rotaciones"],
 "", ["demoivre", "complejos", "patron", "nivel-intermedio"], "cap. 9 (DeMoivre's Theorem)"))

A(P(642, "El ciclo de las potencias de i", "patrones", 2,
 "¿Cuánto vale i²⁰²⁴ (donde i es la unidad imaginaria)?",
 ["Las potencias de i se repiten en un ciclo corto: calcula las primeras.",
  "i¹ = i, i² = −1, i³ = −i, i⁴ = 1, y luego se repite con periodo 4.",
  "Reduce el exponente módulo 4: 2024 = 4·506, así que 2024 ≡ 0 (mód 4).",
  "i⁴ᵏ = 1.",
  "i²⁰²⁴ = 1."],
 "Las potencias de i ciclan i, −1, −i, 1 (periodo 4); como 2024 es múltiplo de 4, i²⁰²⁴ = 1. Verificado con Python.",
 "El patrón de las potencias de i tiene periodo 4. Reducir el exponente módulo 4 resuelve cualquier potencia, igual que los ciclos de últimos dígitos.",
 10, ["potencias de i", "ciclo de periodo 4", "unidad imaginaria"],
 ["aritmética modular", "rotaciones de 90°", "señales"],
 "", ["complejos", "patron", "nivel-basico"], "cap. 9 (Complex Numbers)"))

A(P(643, "Suma de senos cuadrados", "patrones", 2,
 "Calcula sen²(30°) + sen²(45°) + sen²(60°).",
 ["Usa los valores notables del seno y eleva al cuadrado.",
  "sen 30° = 1/2, sen 45° = √2/2, sen 60° = √3/2.",
  "Cuadrados: (1/2)² = 1/4, (√2/2)² = 1/2, (√3/2)² = 3/4.",
  "Suma = 1/4 + 1/2 + 3/4.",
  "= 1/4 + 2/4 + 3/4 = 6/4 = 3/2."],
 "sen²30° + sen²45° + sen²60° = 1/4 + 1/2 + 3/4 = 3/2. Verificado con Python.",
 "Los valores notables del seno (1/2, √2/2, √3/2) forman un patrón ordenado; sus cuadrados (1/4, 2/4, 3/4) lo hacen evidente y la suma es exacta.",
 10, ["valores trigonométricos notables", "seno al cuadrado", "patrón"],
 ["trigonometría aplicada", "física de ondas", "ingeniería"],
 "", ["trigonometria", "patron", "nivel-basico"], "cap. 2 (Trigonometric Functions)"))

A(P(644, "Producto de las raíces de un cúbico", "patrones", 2,
 "¿Cuál es el producto de las raíces del polinomio x³ − 6x² + 11x − 6?",
 ["Las fórmulas de Vieta relacionan el producto de las raíces con el término constante.",
  "Para x³ + ax² + bx + c, el producto de las raíces es −c.",
  "Aquí c = −6.",
  "Producto = −(−6) = 6.",
  "(Las raíces son 1, 2, 3 y 1·2·3 = 6.)"],
 "Por Vieta, el producto de las raíces es −c = 6 (las raíces son 1, 2, 3). Verificado con Python.",
 "El patrón de Vieta: para un cúbico mónico, el producto de las raíces es el término constante con signo cambiado. No hace falta hallar las raíces.",
 10, ["Vieta", "producto de raíces", "polinomio cúbico"],
 ["diseño de filtros", "polinomios característicos", "álgebra"],
 "", ["vieta", "polinomios", "patron", "nivel-basico"], "cap. 6 (Coefficients and Roots)"))

A(P(645, "Módulo de una potencia compleja", "patrones", 3,
 "¿Cuál es el módulo (valor absoluto) de (1 + i)⁸?",
 ["El módulo de una potencia es la potencia del módulo: |zⁿ| = |z|ⁿ.",
  "|1 + i| = √(1² + 1²) = √2.",
  "|(1 + i)⁸| = (√2)⁸.",
  "(√2)⁸ = 2⁴.",
  "= 16."],
 "|(1+i)⁸| = |1+i|⁸ = (√2)⁸ = 2⁴ = 16. Verificado con Python.",
 "El patrón |zⁿ| = |z|ⁿ (multiplicatividad del módulo) evita expandir la potencia: solo se eleva el módulo. (√2)⁸ = 16.",
 12, ["módulo de potencia", "|zⁿ|=|z|ⁿ", "complejos"],
 ["crecimiento de señales", "estabilidad de sistemas", "fasores"],
 "", ["complejos", "demoivre", "patron", "nivel-intermedio"], "cap. 9 (The Complex Absolute Value)"))

A(P(646, "Suma de un ciclo de potencias de i", "patrones", 3,
 "Calcula la suma i⁰ + i¹ + i² + ⋯ + i⁹⁹ (los primeros 100 términos).",
 ["Las potencias de i se repiten cada 4 términos; agrupa de a cuatro.",
  "Cada bloque i⁴ᵏ + i⁴ᵏ⁺¹ + i⁴ᵏ⁺² + i⁴ᵏ⁺³ = 1 + i − 1 − i = 0.",
  "Hay 100 términos, que son exactamente 25 bloques completos de 4.",
  "Cada bloque suma 0.",
  "Suma total = 25·0 = 0."],
 "Cada bloque de 4 potencias consecutivas de i suma 0; con 100 términos (25 bloques), la suma total es 0. Verificado con Python.",
 "El patrón periódico de i hace que cualquier bloque de 4 potencias consecutivas se anule. Cuando el número de términos es múltiplo de 4, la suma es 0.",
 12, ["potencias de i", "suma periódica", "agrupar en bloques"],
 ["series complejas", "transformadas", "análisis de señales"],
 "", ["complejos", "series", "patron", "nivel-intermedio"], "cap. 9 (Complex Numbers)"))

A(P(647, "Elevar uno más i al cuadrado", "patrones", 1,
 "Calcula (1 + i)².",
 ["Desarrolla el cuadrado del binomio y recuerda que i² = −1.",
  "(1 + i)² = 1² + 2·1·i + i².",
  "= 1 + 2i + i².",
  "Como i² = −1: 1 + 2i − 1.",
  "= 2i."],
 "(1 + i)² = 1 + 2i + i² = 1 + 2i − 1 = 2i. Verificado con Python.",
 "El cuadrado de 1 + i es 2i: en forma polar, 1+i tiene módulo √2 y ángulo 45°, así que al cuadrado da módulo 2 y ángulo 90° (= 2i). Un patrón clave para potencias.",
 8, ["números complejos", "i²=−1", "cuadrado de binomio"],
 ["rotaciones", "señales", "álgebra compleja"],
 "", ["complejos", "patron", "nivel-basico"], "cap. 9 (Complex Numbers)"))

A(P(648, "Coseno de cero más coseno de pi", "patrones", 1,
 "Calcula cos(0°) + cos(180°).",
 ["Usa los valores del coseno en los extremos del círculo unitario.",
  "cos(0°) = 1 (el punto más a la derecha del círculo).",
  "cos(180°) = −1 (el punto más a la izquierda).",
  "Suma = 1 + (−1).",
  "= 0."],
 "cos 0° + cos 180° = 1 + (−1) = 0. Verificado con Python.",
 "El coseno recorre el círculo unitario de 1 (en 0°) a −1 (en 180°): valores opuestos en ángulos suplementarios. El patrón de simetría hace que se cancelen.",
 6, ["valores del coseno", "círculo unitario", "simetría"],
 ["ondas estacionarias", "interferencia", "física"],
 "", ["trigonometria", "patron", "nivel-basico"], "cap. 2 (Graphing Trigonometric Functions)"))

A(P(649, "Las raíces quintas de la unidad", "patrones", 3,
 "¿Cuánto vale la suma de las cinco raíces quintas de la unidad (las cinco soluciones complejas de z⁵ = 1)?",
 ["Las cinco raíces son las soluciones de z⁵ − 1 = 0; usa Vieta o la simetría del círculo.",
  "Por Vieta, la suma de las raíces de z⁵ − 1 es el coeficiente de z⁴ (con signo), que es 0.",
  "Geométricamente, las raíces son 5 puntos igualmente espaciados en el círculo unitario.",
  "Su centro de masa (promedio) es el origen, así que su suma es 0.",
  "La suma es 0."],
 "Las cinco raíces quintas de la unidad suman 0 (coeficiente de z⁴ en z⁵ − 1 es 0; verificado numéricamente ~1e-128).",
 "Para todo n > 1, las n raíces de la unidad suman 0: están repartidas simétricamente en el círculo y su centro de masa es el origen. Es el mismo patrón que las cúbicas.",
 12, ["raíces de la unidad", "suma cero", "simetría del círculo"],
 ["transformada discreta de Fourier", "señales", "polígonos regulares"],
 "", ["raices-unidad", "complejos", "patron", "nivel-intermedio"], "cap. 9 (The Roots of Unity)"))

A(P(650, "Tangente de cuarenta y cinco", "patrones", 1,
 "¿Cuánto vale tan(45°)?",
 ["En 45° el seno y el coseno son iguales, así que su cociente es sencillo.",
  "sen 45° = √2/2 y cos 45° = √2/2.",
  "tan 45° = sen 45°/cos 45° = (√2/2)/(√2/2).",
  "= 1.",
  "tan 45° = 1."],
 "tan 45° = sen 45°/cos 45° = 1 (seno y coseno iguales). Verificado con Python.",
 "En el triángulo rectángulo isósceles (45-45-90) los catetos son iguales, así que tan 45° = opuesto/adyacente = 1. Un valor notable que conviene memorizar.",
 6, ["tangente de 45°", "triángulo 45-45-90", "valor notable"],
 ["pendientes del 100%", "rampas", "trigonometría"],
 "", ["trigonometria", "patron", "nivel-basico"], "cap. 2 (Trigonometric Functions)"))

# =====================================================================
# OPTIMIZACION (11) — amplitud trig, área con ángulo, AM-GM, distancia, cónicas
# =====================================================================

A(P(651, "El máximo del seno", "optimizacion", 1,
 "¿Cuál es el valor máximo de sen θ cuando θ recorre todos los ángulos?",
 ["El seno mide la coordenada vertical de un punto que recorre el círculo unitario.",
  "Esa coordenada vertical varía entre −1 y 1.",
  "El máximo se alcanza en lo más alto del círculo.",
  "Eso ocurre en θ = 90°.",
  "El valor máximo es 1."],
 "El seno varía en [−1, 1]; su máximo es 1, alcanzado en θ = 90°. Verificado con Python.",
 "El seno está acotado por el círculo unitario: |sen θ| ≤ 1. Su máximo 1 se da en 90° (lo más alto del círculo).",
 6, ["rango del seno", "círculo unitario", "máximo"],
 ["amplitud de ondas", "oscilaciones", "física"],
 "", ["trigonometria", "optimizacion", "nivel-basico"], "cap. 2 (Trigonometric Functions)"))

A(P(652, "La amplitud de una combinación", "optimizacion", 3,
 "¿Cuál es el valor máximo de 3·sen θ + 4·cos θ?",
 ["Una combinación a·sen θ + b·cos θ se puede escribir como R·sen(θ + φ), donde R es la amplitud.",
  "La amplitud es R = √(a² + b²).",
  "Aquí a = 3 y b = 4.",
  "R = √(3² + 4²) = √25 = 5.",
  "Como sen(θ + φ) ≤ 1, el máximo de la expresión es R = 5."],
 "3 sen θ + 4 cos θ = 5·sen(θ + φ), cuya amplitud es √(3² + 4²) = 5. El máximo es 5. Verificado con Python.",
 "Toda combinación a·sen + b·cos es una sinusoide de amplitud √(a²+b²); su máximo es esa amplitud. Es Cauchy-Schwarz disfrazado de trigonometría.",
 12, ["amplitud", "a·sen+b·cos=R·sen(θ+φ)", "máximo trigonométrico"],
 ["superposición de ondas", "circuitos AC", "acústica"],
 "", ["trigonometria", "optimizacion", "nivel-intermedio"], "cap. 2 (Trigonometric Identities)"))

A(P(653, "El mínimo de una combinación", "optimizacion", 3,
 "¿Cuál es el valor mínimo de 5·cos θ + 12·sen θ?",
 ["Otra vez, a·sen θ + b·cos θ tiene amplitud √(a² + b²) y oscila entre −R y R.",
  "Amplitud R = √(5² + 12²) = √169 = 13.",
  "La expresión varía entre −R y R.",
  "El mínimo es −R.",
  "= −13."],
 "5 cos θ + 12 sen θ tiene amplitud √(5² + 12²) = 13, así que su mínimo es −13. Verificado con Python.",
 "Una sinusoide de amplitud R alcanza su mínimo en −R. Aquí √(5²+12²) = 13 da el rango [−13, 13].",
 12, ["amplitud", "mínimo trigonométrico", "√(a²+b²)"],
 ["señales", "vibraciones", "ingeniería"],
 "", ["trigonometria", "optimizacion", "nivel-intermedio"], "cap. 2 (Trigonometric Identities)"))

A(P(654, "Máximo del producto seno por coseno", "optimizacion", 2,
 "¿Cuál es el valor máximo de sen θ · cos θ?",
 ["Usa una identidad del ángulo doble para reescribir el producto.",
  "sen(2θ) = 2·sen θ·cos θ, así que sen θ·cos θ = (1/2)·sen(2θ).",
  "El máximo de sen(2θ) es 1.",
  "Por tanto el máximo de (1/2)·sen(2θ) es 1/2.",
  "El valor máximo es 1/2 (en θ = 45°)."],
 "sen θ·cos θ = (1/2)sen(2θ), cuyo máximo es 1/2 (en θ = 45°). Verificado con Python.",
 "La identidad del ángulo doble convierte un producto en un solo seno, cuyo máximo (1) se lee de inmediato. El producto sen·cos nunca pasa de 1/2.",
 10, ["identidad de ángulo doble", "sen·cos=½sen2θ", "máximo"],
 ["optimización de potencia", "área máxima", "física"],
 "", ["trigonometria", "optimizacion", "nivel-basico"], "cap. 2 (Trigonometric Identities)"))

A(P(655, "Área máxima con dos lados", "optimizacion", 2,
 "Un triángulo tiene dos lados de longitudes 6 y 8. Variando el ángulo entre ellos, ¿cuál es la mayor área posible?",
 ["El área en función del ángulo entre dos lados es (1/2)·a·b·sen θ.",
  "Área = (1/2)·6·8·sen θ = 24·sen θ.",
  "Lo único variable es sen θ, cuyo máximo es 1.",
  "El máximo ocurre en θ = 90° (lados perpendiculares).",
  "Área máxima = 24."],
 "Área = (1/2)·6·8·sen θ = 24 sen θ, máxima cuando sen θ = 1 (θ = 90°): área 24. Verificado con Python.",
 "Con dos lados fijos, el área es máxima cuando son perpendiculares: la fórmula (1/2)ab·sen θ reduce el problema a maximizar el seno.",
 10, ["área = ½ab·senθ", "maximizar seno", "ángulo recto"],
 ["diseño de brazos mecánicos", "máxima cobertura", "navegación"],
 "", ["trigonometria", "optimizacion", "nivel-basico"], "cap. 3 (Areas, Areas, Areas)"))

A(P(656, "Tres factores con producto fijo", "optimizacion", 3,
 "Tres números positivos a, b, c cumplen a·b·c = 27. ¿Cuál es el menor valor posible de a + b + c?",
 ["Aplica AM-GM con tres variables.",
  "(a + b + c)/3 ≥ ∛(abc).",
  "∛(abc) = ∛27 = 3.",
  "a + b + c ≥ 3·3 = 9, con igualdad cuando a = b = c = 3.",
  "El mínimo es 9."],
 "Por AM-GM, a + b + c ≥ 3∛27 = 9, con igualdad en a = b = c = 3. El mínimo es 9. Verificado con Python.",
 "AM-GM con n variables: la suma es mínima (a producto fijo) cuando todas son iguales. Aquí ∛27 = 3 fija el óptimo simétrico.",
 12, ["AM-GM con n variables", "producto fijo", "óptimo simétrico"],
 ["optimización de volúmenes", "diseño", "economía"],
 "", ["am-gm", "optimizacion", "nivel-intermedio"], "cap. 6 / inequalities"))

A(P(657, "Distancia mínima a una recta", "optimizacion", 3,
 "Si x e y son números reales con x + 2y = 5, ¿cuál es el valor mínimo de x² + y²?",
 ["x² + y² es el cuadrado de la distancia del origen al punto (x, y), que vive en la recta x + 2y = 5.",
  "El mínimo de esa distancia es la distancia perpendicular del origen a la recta.",
  "Distancia² = (coeficiente independiente)² / (suma de cuadrados de los coeficientes) = 5²/(1² + 2²).",
  "= 25/5.",
  "= 5."],
 "x² + y² mínimo = distancia² del origen a x + 2y = 5 = 5²/(1²+2²) = 5. Verificado con Python.",
 "Minimizar x² + y² con una restricción lineal es hallar el punto de la recta más cercano al origen: la proyección perpendicular. La fórmula c²/(a²+b²) lo da directo.",
 12, ["distancia punto-recta", "minimizar norma", "proyección"],
 ["mínimos cuadrados", "optimización con restricciones", "geometría"],
 "", ["optimizacion", "geometria-analitica", "nivel-intermedio"], "cap. 5 (Conics and Polar Coordinates)"))

A(P(658, "Producto máximo con suma de cuadrados", "optimizacion", 2,
 "Dos números reales cumplen a² + b² = 50. ¿Cuál es el mayor valor posible de a·b?",
 ["Relaciona el producto con la suma de cuadrados mediante AM-GM (o la desigualdad 2ab ≤ a²+b²).",
  "Como (a − b)² ≥ 0, se tiene 2ab ≤ a² + b².",
  "2ab ≤ 50, así que ab ≤ 25.",
  "La igualdad ocurre cuando a = b, es decir 2a² = 50 ⇒ a = 5.",
  "El producto máximo es 25."],
 "De 2ab ≤ a² + b² = 50 se obtiene ab ≤ 25, con igualdad en a = b = 5. El máximo es 25. Verificado con Python.",
 "La desigualdad 2ab ≤ a² + b² (equivalente a (a−b)² ≥ 0) acota el producto por la suma de cuadrados; la igualdad es el caso simétrico a = b.",
 10, ["desigualdad (a−b)²≥0", "suma de cuadrados", "producto máximo"],
 ["optimización", "física (energía)", "diseño"],
 "", ["optimizacion", "am-gm", "nivel-basico"], "cap. 6 / inequalities"))

A(P(659, "Suma de cuadrados de tangente y cotangente", "optimizacion", 3,
 "Para un ángulo agudo θ, ¿cuál es el valor mínimo de tan²θ + cot²θ?",
 ["tan θ y cot θ son recíprocos, así que su producto es 1: aplica AM-GM a sus cuadrados.",
  "tan²θ · cot²θ = (tan θ·cot θ)² = 1² = 1.",
  "Por AM-GM, tan²θ + cot²θ ≥ 2·√(tan²θ·cot²θ).",
  "= 2·√1 = 2, con igualdad cuando tan²θ = cot²θ, es decir θ = 45°.",
  "El mínimo es 2."],
 "Como tan²θ·cot²θ = 1, por AM-GM tan²θ + cot²θ ≥ 2, con igualdad en θ = 45°. El mínimo es 2. Verificado con Python.",
 "El producto de tan²θ y cot²θ es constante (= 1), así que AM-GM da su suma mínima 2. La igualdad es la simetría tan = cot en 45°.",
 12, ["AM-GM", "tan·cot=1", "mínimo trigonométrico"],
 ["optimización", "trigonometría aplicada", "ingeniería"],
 "", ["trigonometria", "am-gm", "optimizacion", "nivel-intermedio"], "cap. 2 / inequalities"))

A(P(660, "El máximo de dos senos", "optimizacion", 2,
 "¿Cuál es el valor máximo de 2·sen θ + 2·cos θ?",
 ["Es una combinación a·sen θ + b·cos θ con amplitud √(a² + b²).",
  "Aquí a = b = 2.",
  "Amplitud = √(2² + 2²) = √8.",
  "√8 = 2√2.",
  "El máximo es 2√2 ≈ 2.83."],
 "2 sen θ + 2 cos θ tiene amplitud √(2² + 2²) = 2√2, así que su máximo es 2√2. Verificado con Python.",
 "La amplitud √(a²+b²) da el máximo de cualquier a·sen + b·cos. Con a = b, sale √(2a²) = a√2.",
 10, ["amplitud", "máximo trigonométrico", "√(a²+b²)"],
 ["superposición de ondas", "circuitos", "acústica"],
 "", ["trigonometria", "optimizacion", "nivel-basico"], "cap. 2 (Trigonometric Identities)"))

A(P(661, "El punto más a la derecha de la elipse", "optimizacion", 2,
 "¿Cuál es el mayor valor que puede tomar la coordenada x de un punto sobre la elipse x²/9 + y²/4 = 1?",
 ["La elipse acota cada coordenada; piensa en el semieje horizontal.",
  "Para que x sea máximo, el término y²/4 debe ser lo menor posible, es decir y = 0.",
  "Con y = 0: x²/9 = 1, así que x² = 9.",
  "x = ±3; el mayor es 3.",
  "El máximo de x es 3 (el semieje mayor horizontal)."],
 "Con y = 0, x²/9 = 1 ⇒ x = 3. El mayor valor de x en la elipse es 3. Verificado con Python.",
 "En una elipse x²/a² + y²/b² = 1, la coordenada x está acotada por ±a (el semieje). El extremo se alcanza cuando y = 0.",
 10, ["elipse", "semieje", "extremo de coordenada"],
 ["órbitas planetarias", "diseño de lentes", "acústica de salas"],
 "", ["conicas", "optimizacion", "nivel-basico"], "cap. 5 (Ellipses)"))

# =====================================================================
# INVERSION (11) — resolver trig, trig inversa, identidades funcionales, raíces
# =====================================================================

A(P(662, "Despejar el ángulo del seno", "inversion", 1,
 "Halla el ángulo θ entre 0° y 90° tal que sen θ = 1/2.",
 ["Pregunta inversa: ¿qué ángulo tiene seno 1/2? Usa los valores notables.",
  "Recuerda que sen 30° = 1/2.",
  "En el rango [0°, 90°] el seno es inyectivo, así que hay una única solución.",
  "θ = 30°.",
  "Comprueba: sen 30° = 1/2. ✓"],
 "sen θ = 1/2 en [0°, 90°] ⇒ θ = 30° (= arcsen(1/2)). Verificado con Python.",
 "Resolver una ecuación trigonométrica es aplicar la función inversa (arcoseno). En [0°, 90°] el seno es inyectivo, así que la solución es única.",
 8, ["ecuación trigonométrica", "arcoseno", "valores notables"],
 ["diseño de rampas", "óptica (refracción)", "navegación"],
 "", ["trigonometria", "inversion", "nivel-basico"], "cap. 2 (Going Backwards)"))

A(P(663, "Cuando el coseno se anula", "inversion", 1,
 "Halla el ángulo θ entre 0° y 180° tal que cos θ = 0.",
 ["Pregunta inversa: ¿en qué ángulo el coseno (coordenada horizontal en el círculo) es 0?",
  "El coseno es 0 donde el punto del círculo está sobre el eje vertical.",
  "En el rango [0°, 180°] eso ocurre en la parte superior del círculo.",
  "θ = 90°.",
  "Comprueba: cos 90° = 0. ✓"],
 "cos θ = 0 en [0°, 180°] ⇒ θ = 90° (= arccos(0)). Verificado con Python.",
 "El arcocoseno invierte el coseno: cos θ = 0 corresponde a θ = 90°, donde el punto del círculo cruza el eje vertical.",
 8, ["ecuación trigonométrica", "arcocoseno", "círculo unitario"],
 ["fase de ondas", "perpendicularidad", "física"],
 "", ["trigonometria", "inversion", "nivel-basico"], "cap. 2 (Going Backwards)"))

A(P(664, "El ángulo de tangente uno", "inversion", 1,
 "Halla el ángulo agudo θ tal que tan θ = 1.",
 ["Pregunta inversa: ¿qué ángulo tiene tangente 1? Eso pasa cuando seno y coseno son iguales.",
  "tan θ = 1 significa sen θ = cos θ.",
  "Entre los ángulos agudos, eso ocurre en 45°.",
  "θ = 45°.",
  "Comprueba: tan 45° = 1. ✓"],
 "tan θ = 1 (agudo) ⇒ θ = 45° (= arctan 1). Verificado con Python.",
 "El arcotangente invierte la tangente: tan θ = 1 ocurre donde seno y coseno coinciden, es decir θ = 45°.",
 8, ["ecuación trigonométrica", "arcotangente", "sen=cos"],
 ["pendientes", "rampas del 100%", "trigonometría"],
 "", ["trigonometria", "inversion", "nivel-basico"], "cap. 2 (Going Backwards)"))

A(P(665, "Arcoseno de un valor notable", "inversion", 2,
 "¿Cuánto vale arcsen(√3/2)? (Da el ángulo entre 0° y 90°.)",
 ["El arcoseno responde: ¿qué ángulo tiene este seno?",
  "Busca θ con sen θ = √3/2 en [0°, 90°].",
  "Recuerda los valores notables: sen 60° = √3/2.",
  "Por tanto θ = 60°.",
  "arcsen(√3/2) = 60°."],
 "arcsen(√3/2) = 60° porque sen 60° = √3/2. Verificado con Python.",
 "La función arcoseno es la inversa del seno restringido a [−90°, 90°]: devuelve el ángulo cuyo seno es el valor dado.",
 8, ["arcoseno", "función inversa", "valores notables"],
 ["robótica", "óptica", "navegación"],
 "", ["trigonometria", "inversion", "nivel-basico"], "cap. 2 (Going Backwards)"))

A(P(666, "Una identidad funcional", "inversion", 3,
 "Una función f satisface f(x) + 3·f(2 − x) = x para todo x. ¿Cuánto vale f(1)?",
 ["Busca un valor de x que haga aparecer f(1) en ambos términos (un punto fijo de x ↦ 2 − x).",
  "Si x = 1, entonces 2 − x = 1 también, así que ambos términos son f(1).",
  "La ecuación queda f(1) + 3·f(1) = 1.",
  "4·f(1) = 1.",
  "f(1) = 1/4."],
 "Con x = 1, 2 − x = 1, así que f(1) + 3f(1) = 1 ⇒ 4f(1) = 1 ⇒ f(1) = 1/4. Verificado con Python.",
 "Para identidades funcionales con f(x) y f(g(x)), evaluar en un punto fijo de g (aquí x = 2 − x ⇒ x = 1) colapsa la ecuación a una sola incógnita.",
 14, ["ecuación funcional", "punto fijo", "sustitución astuta"],
 ["resolución de funcionales", "simetrías", "transformadas"],
 "", ["funciones", "ecuacion-funcional", "inversion", "nivel-intermedio"], "cap. 7 (Solving Functional Identities)"))

A(P(667, "La raíz que falta del cúbico", "inversion", 3,
 "El polinomio x³ − 7x + 6 tiene a x = 1 como raíz. ¿Cuál es la suma de las otras dos raíces?",
 ["Usa Vieta: la suma de TODAS las raíces de x³ + ax² + bx + c es −a.",
  "Aquí el coeficiente de x² es 0, así que la suma de las tres raíces es 0.",
  "Una raíz es 1, así que la suma de las otras dos es 0 − 1.",
  "= −1.",
  "(En efecto, las raíces son 1, 2 y −3; 2 + (−3) = −1.)"],
 "Por Vieta, la suma de las tres raíces es 0 (no hay término x²); quitando la raíz 1, las otras dos suman −1. (Raíces: 1, 2, −3.) Verificado con Python.",
 "Vieta da la suma total de raíces sin resolver; conocida una raíz, se recupera la suma de las restantes por resta. Es trabajar hacia atrás desde los coeficientes.",
 12, ["Vieta", "suma de raíces", "raíz conocida"],
 ["factorización de polinomios", "diseño de sistemas", "álgebra"],
 "", ["vieta", "polinomios", "inversion", "nivel-intermedio"], "cap. 6 (Finding Roots of Polynomials)"))

A(P(668, "La raíz cúbica real", "inversion", 1,
 "Resuelve para z (número real): z³ = 8.",
 ["Busca el número real cuyo cubo es 8.",
  "z = ∛8.",
  "2³ = 8.",
  "Como 8 > 0, la raíz cúbica real es positiva y única.",
  "z = 2."],
 "z³ = 8 ⇒ z = ∛8 = 2 (raíz real). Verificado con Python.",
 "La raíz cúbica invierte el cubo. A diferencia de la raíz cuadrada, todo real tiene una única raíz cúbica real (aquí 2). (Hay además dos raíces complejas.)",
 8, ["raíz cúbica", "ecuación z³=8", "inverso del cubo"],
 ["volúmenes", "escalado", "modelos físicos"],
 "", ["raices", "inversion", "nivel-basico"], "cap. 6 (Finding Roots of Polynomials)"))

A(P(669, "Deshacer la exponencial", "inversion", 1,
 "Sea f(x) = 2ˣ. ¿Cuánto vale f⁻¹(8) (la imagen inversa de 8)?",
 ["f⁻¹(8) es el valor de x tal que 2ˣ = 8.",
  "8 = 2³.",
  "Entonces 2ˣ = 2³.",
  "x = 3.",
  "f⁻¹(8) = 3 (que es log₂ 8)."],
 "f⁻¹(8) resuelve 2ˣ = 8 = 2³ ⇒ x = 3 (= log₂ 8). Verificado con Python.",
 "La inversa de la exponencial 2ˣ es el logaritmo en base 2. Hallar f⁻¹(8) es resolver hacia atrás la ecuación 2ˣ = 8.",
 8, ["función inversa", "logaritmo", "exponencial"],
 ["escalas logarítmicas", "complejidad", "finanzas"],
 "", ["funciones", "logaritmos", "inversion", "nivel-basico"], "cap. 7 (The Inverse of a Function)"))

A(P(670, "Sumas de Newton hacia atrás", "inversion", 3,
 "Dos números a y b cumplen a + b = 6 y a² + b² = 14. ¿Cuánto vale su producto a·b?",
 ["Relaciona la suma de cuadrados con la suma y el producto mediante una identidad, y despeja el producto.",
  "(a + b)² = a² + 2ab + b², así que a² + b² = (a + b)² − 2ab.",
  "Sustituye: 14 = 6² − 2ab = 36 − 2ab.",
  "2ab = 36 − 14 = 22.",
  "ab = 11."],
 "De a² + b² = (a+b)² − 2ab: 14 = 36 − 2ab ⇒ ab = 11. Verificado con Python.",
 "Conocidas la suma y la suma de cuadrados, se recupera el producto invirtiendo la identidad (a+b)² = a²+b²+2ab. Es la sumas de Newton al revés.",
 12, ["identidad (a+b)²", "sumas de Newton", "despejar producto"],
 ["reconstruir parámetros", "Vieta inversa", "álgebra"],
 "", ["newton", "inversion", "nivel-intermedio"], "cap. 6 (Newton's Sums)"))

A(P(671, "Cuando seno iguala coseno", "inversion", 2,
 "Halla el ángulo θ entre 0° y 90° tal que sen θ = cos θ.",
 ["Divide ambos lados entre cos θ para convertir la ecuación en una de tangente.",
  "sen θ = cos θ ⇒ sen θ/cos θ = 1 ⇒ tan θ = 1.",
  "Busca el ángulo agudo con tangente 1.",
  "θ = 45°.",
  "Comprueba: sen 45° = cos 45° = √2/2. ✓"],
 "sen θ = cos θ ⇒ tan θ = 1 ⇒ θ = 45°. Verificado con Python.",
 "Convertir una ecuación de seno y coseno en una de tangente (dividiendo) facilita despejar el ángulo. sen = cos solo en 45° dentro de [0°, 90°].",
 8, ["ecuación trigonométrica", "tan θ=1", "despejar ángulo"],
 ["equilibrio de componentes", "diseño a 45°", "física"],
 "", ["trigonometria", "inversion", "nivel-basico"], "cap. 2 (Going Backwards)"))

A(P(672, "Una raíz cuadrada de i", "inversion", 4,
 "Halla un número complejo z tal que z² = i (la unidad imaginaria). Da la raíz con parte real positiva.",
 ["Escribe i en forma polar: tiene módulo 1 y ángulo 90°. Una raíz cuadrada tiene la mitad del ángulo.",
  "z debe tener módulo √1 = 1 y ángulo 90°/2 = 45°.",
  "z = cos 45° + i·sen 45° = (√2/2) + (√2/2)i.",
  "También se escribe z = (1 + i)/√2.",
  "Comprueba: ((1 + i)/√2)² = (1 + i)²/2 = 2i/2 = i. ✓"],
 "En polar, i = 1∠90°; su raíz cuadrada es 1∠45° = (1 + i)/√2, y en efecto ((1+i)/√2)² = i. Verificado con Python.",
 "Sacar raíces complejas es invertir DeMoivre: se toma la raíz del módulo y se DIVIDE el ángulo entre n. La raíz de i con parte real positiva es (1+i)/√2.",
 16, ["raíz cuadrada compleja", "forma polar", "inversa de DeMoivre"],
 ["procesamiento de señales", "ecuaciones diferenciales", "rotaciones"],
 "", ["complejos", "demoivre", "inversion", "nivel-avanzado"], "cap. 9 (DeMoivre's Theorem)"))

# =====================================================================
# Validación de balance y append idempotente
# =====================================================================
assert len(PROBLEMS) == 44, len(PROBLEMS)
bal = collections.Counter(p["estrategia"] for p in PROBLEMS)
assert bal["inversion"] == bal["optimizacion"] == bal["invariantes"] == bal["patrones"] == 11, bal
ids = [p["id"] for p in PROBLEMS]
assert ids == list(range(629, 673)), ids
assert len(set(ids)) == 44

PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
clash = existing & set(ids)
assert not clash, ("choque de ids", clash)

data["problemas"].extend(PROBLEMS)
gbal = collections.Counter(p["estrategia"] for p in data["problemas"])
print("balance global tras append:", dict(gbal))
assert all(v == 168 for v in gbal.values()), gbal

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: añadidos {len(PROBLEMS)} problemas (ids {ids[0]}-{ids[-1]}). Total = {len(data['problemas'])}.")
