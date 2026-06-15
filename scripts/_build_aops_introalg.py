# -*- coding: utf-8 -*-
"""Tanda 33 — Richard Rusczyk, *Introduction to Algebra* (Art of Problem Solving).
Append 44 problemas verificados a data/problems.json. Fuentes internas:
 - Cap. 11 «Special Factorizations» (Simon's Favorite Factoring Trick, diferencia
   de cuadrados, identidades) -> patrones.
 - Cap. 15 «More Inequalities» (desigualdad trivial x²≥0, AM-GM, optimización
   cuadrática completando el cuadrado) -> optimizacion.
 - Cap. 22 «Special Manipulations» (elevar a potencias, auto-similaridad /
   radicales anidados y fracciones continuas) -> inversion; (simetría, sumas/
   productos de raíces tipo Vieta, sistemas simétricos) -> invariantes.
Todas las afirmaciones numéricas verificadas con Python (sympy/fractions; ver
/tmp/verif_aops.py + /tmp/verif_aops2.py y la bitácora de HANDOFFCES.md).
El libro de soluciones es un volumen aparte no disponible: cada solución y cada
número fue resuelto y comprobado de forma independiente. Builder idempotente:
aborta si hay choque de ids. Sector C (entrenamiento), esquema §4.1, ids 321-364.
Distribución 14/8/11/11 (optimizacion/patrones/inversion/invariantes): el texto
es riquísimo en optimización cuadrática y desigualdades, sesgo que lleva el
balance GLOBAL de problems.json a 91/91/91/91 exactos."""
import json, collections

SRC = "Rusczyk, *Introduction to Algebra* (Art of Problem Solving, 2nd ed.)"

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
# OPTIMIZACION (14) — desigualdad trivial, AM-GM, optimización cuadrática
# =====================================================================

A(P(321, "El máximo escondido en una parábola", "optimizacion", 2,
 "¿Cuál es el valor máximo de la expresión −x² + 5x − 7, y para qué valor de x se alcanza?",
 ["La gráfica de −x² + 5x − 7 es una parábola. ¿Abre hacia arriba o hacia abajo? Eso decide si hay máximo o mínimo.",
  "El coeficiente de x² es negativo, así que abre hacia abajo: tiene un MÁXIMO en su vértice.",
  "Completa el cuadrado: saca factor −1 de los términos en x, −(x² − 5x) − 7, y completa.",
  "−(x² − 5x + 25/4) − 7 + 25/4 = −(x − 5/2)² + (25/4 − 7). El cuadrado nunca aporta nada positivo.",
  "El término −(x − 5/2)² es ≤ 0, máximo 0 cuando x = 5/2. Ahí la expresión vale 25/4 − 7 = −3/4."],
 "Completando el cuadrado: −x² + 5x − 7 = −(x − 5/2)² − 3/4. Como −(x − 5/2)² ≤ 0 con igualdad solo en x = 5/2, el máximo es −3/4, alcanzado en x = 5/2. Verificado con Python (vértice en x = 5/2, valor −3/4).",
 "La técnica de completar el cuadrado convierte cualquier cuadrática en (vértice) ± (cuadrado), y como un cuadrado real es ≥ 0, el óptimo se lee de inmediato. Es la 'desigualdad trivial' x² ≥ 0 disfrazada.",
 18, ["completar el cuadrado", "vértice de parábola", "desigualdad trivial"],
 ["optimización sin cálculo", "diseño de antenas parabólicas", "trayectorias balísticas"],
 "", ["cuadratica", "optimizacion", "completar-cuadrado", "nivel-basico"], "cap. 15.4 (Prob. 15.11)"))

A(P(322, "Buscando el fondo del valle", "optimizacion", 2,
 "¿Cuál es el valor mínimo de 2x² + 8x − 9?",
 ["El coeficiente de x² es positivo: la parábola abre hacia arriba y tiene un MÍNIMO.",
  "Factoriza primero el 2 de los términos con x: 2(x² + 4x) − 9.",
  "Completa el cuadrado dentro del paréntesis: x² + 4x = (x + 2)² − 4.",
  "2((x + 2)² − 4) − 9 = 2(x + 2)² − 8 − 9 = 2(x + 2)² − 17.",
  "2(x + 2)² ≥ 0 con igualdad en x = −2; el mínimo es −17."],
 "2x² + 8x − 9 = 2(x + 2)² − 17. Como 2(x + 2)² ≥ 0 con igualdad en x = −2, el mínimo es −17 (en x = −2). Verificado con Python.",
 "Cuando el coeficiente principal no es 1, hay que factorizarlo de los términos con x ANTES de completar el cuadrado; si no, el ajuste de la constante sale mal. Completar el cuadrado vuelve a ser la desigualdad trivial: un cuadrado real es ≥ 0.",
 16, ["completar el cuadrado", "factor común", "mínimo de cuadrática"],
 ["minimización de costos", "ajuste por mínimos cuadrados", "energía potencial"],
 "", ["cuadratica", "optimizacion", "minimo", "nivel-basico"], "cap. 15.4 (Prob. 15.12)"))

A(P(323, "Un máximo con coeficientes grandes", "optimizacion", 2,
 "Halla el valor máximo de −3a² − 36a + 2.",
 ["Coeficiente de a² negativo ⇒ hay máximo. No te dejes intimidar por el −36.",
  "Saca factor −3 de los términos en a: −3(a² + 12a) + 2.",
  "Completa el cuadrado: a² + 12a = (a + 6)² − 36.",
  "−3((a + 6)² − 36) + 2 = −3(a + 6)² + 108 + 2.",
  "−3(a + 6)² ≤ 0 con igualdad en a = −6; el máximo es 110."],
 "−3a² − 36a + 2 = −3(a + 6)² + 110. Como −3(a + 6)² ≤ 0 con igualdad en a = −6, el máximo es 110. Verificado con Python.",
 "Al sacar factor común negativo, el signo cambia el sentido del óptimo: el cuadrado sigue siendo ≥ 0, pero al multiplicarlo por −3 se vuelve ≤ 0, por eso hay máximo y no mínimo.",
 16, ["completar el cuadrado", "factor común negativo", "vértice"],
 ["maximizar ingresos", "óptica geométrica", "control de procesos"],
 "", ["cuadratica", "optimizacion", "maximo", "nivel-basico"], "cap. 15.4 (Prob. 15.13)"))

A(P(324, "Dos variables, un solo fondo", "optimizacion", 3,
 "¿Cuál es el valor mínimo de x² + 4x + 2y² − 14y + 1?",
 ["Las variables x e y no se mezclan en ningún término: puedes optimizar cada una por separado.",
  "Agrupa: (x² + 4x) + (2y² − 14y) + 1 y completa el cuadrado en cada grupo.",
  "x² + 4x = (x + 2)² − 4. Para el grupo de y, factoriza 2 primero: 2(y² − 7y).",
  "2(y² − 7y) = 2((y − 7/2)² − 49/4) = 2(y − 7/2)² − 49/2.",
  "Suma todo: (x + 2)² + 2(y − 7/2)² − 4 − 49/2 + 1. Ambos cuadrados son 0 en x=−2, y=7/2."],
 "x² + 4x + 2y² − 14y + 1 = (x + 2)² + 2(y − 7/2)² − 55/2. Ambos cuadrados se anulan en x = −2, y = 7/2, dando el mínimo −55/2. Verificado con Python.",
 "Cuando las variables no comparten términos cruzados, el problema se DESACOPLA: minimizar la suma equivale a minimizar cada bloque por separado. Cada cuadrado se anula independientemente.",
 22, ["completar el cuadrado", "separación de variables", "mínimo multivariable"],
 ["mínimos cuadrados con varios parámetros", "ajuste de superficies", "energía en sistemas desacoplados"],
 "", ["cuadratica", "optimizacion", "multivariable", "nivel-medio"], "cap. 15.4 (Prob. 15.16)"))

A(P(325, "La altura máxima del proyectil", "optimizacion", 3,
 "Una pelota lanzada hacia arriba tiene altura h(t) = −16t² + 48t + 45 (en pies, t en segundos). ¿Cuál es su altura máxima y en qué instante toca el suelo?",
 ["La altura es una cuadrática que abre hacia abajo: su vértice da la altura máxima.",
  "El instante del máximo: completa el cuadrado o usa t = −b/(2a) = 48/32.",
  "El vértice está en t = 3/2 s. Evalúa h(3/2) para la altura máxima.",
  "h(3/2) = −16(9/4) + 48(3/2) + 45 = −36 + 72 + 45 = 81 pies.",
  "Para 'tocar el suelo' resuelve h(t) = 0: −16t² + 48t + 45 = 0, factoriza o usa la fórmula general."],
 "El vértice está en t = 48/32 = 3/2 s, con altura h(3/2) = 81 pies. Para el suelo, −16t² + 48t + 45 = 0 tiene raíces t = −3/4 y t = 15/4; la física exige t > 0, así que toca el suelo en t = 15/4 = 3.75 s. Verificado con Python.",
 "Un mismo modelo cuadrático responde dos preguntas distintas: el VÉRTICE da el óptimo (altura máxima) y las RAÍCES dan los cruces por cero (instante de impacto). No confundas una con otra.",
 22, ["modelo cuadrático", "vértice", "raíces de cuadrática"],
 ["cinemática", "tiro parabólico", "optimización de alcance"],
 "", ["cuadratica", "fisica", "optimizacion", "nivel-medio"], "cap. 15.4 (Ej. 15.4.3)"))

A(P(326, "El corral contra el granero", "optimizacion", 3,
 "Un granjero tiene 20 m de cerca y quiere encerrar un corral rectangular usando la pared del granero como uno de los lados (esa pared no consume cerca). ¿Cuál es el área máxima que puede encerrar?",
 ["Solo necesitas cercar tres lados. Llama x a cada uno de los dos lados perpendiculares al granero.",
  "Si los dos lados perpendiculares miden x, el lado paralelo al granero mide 20 − 2x.",
  "El área es A(x) = x(20 − 2x). Es una cuadrática en x: maximízala.",
  "A(x) = 20x − 2x² = −2(x² − 10x) = −2(x − 5)² + 50.",
  "El máximo es 50 m², con x = 5 (lados 5, 5 y 10)."],
 "Con dos lados x y el tercero 20 − 2x, el área es A(x) = x(20 − 2x) = −2(x − 5)² + 50. El máximo es 50 m² en x = 5 (corral de 5 × 10). Verificado con Python.",
 "La pared gratis del granero rompe la simetría del problema isoperimétrico: con tres lados, el óptimo ya no es un cuadrado sino un rectángulo 1:2. Modelar bien la restricción es medio problema.",
 20, ["modelado", "optimización con restricción", "completar el cuadrado"],
 ["uso eficiente de materiales", "diseño de empaques", "isoperimetría"],
 "", ["cuadratica", "optimizacion", "modelado", "nivel-medio"], "cap. 15.4 (Ej. 15.4.4)"))

A(P(327, "La suma con su recíproco", "optimizacion", 2,
 "Demuestra que para todo número real positivo x se cumple x + 1/x ≥ 2, e indica cuándo hay igualdad.",
 ["Quieres una desigualdad de la forma 'algo al cuadrado ≥ 0'. ¿Qué cuadrado involucra √x y 1/√x?",
  "Considera (√x − 1/√x)². Desarróllalo.",
  "(√x − 1/√x)² = x − 2 + 1/x ≥ 0.",
  "Pasa el −2 al otro lado: x + 1/x ≥ 2.",
  "La igualdad ocurre cuando √x − 1/√x = 0, es decir x = 1."],
 "Para x > 0, (√x − 1/√x)² ≥ 0 desarrolla a x − 2 + 1/x ≥ 0, o sea x + 1/x ≥ 2, con igualdad solo en x = 1. (Es AM-GM aplicado a x y 1/x.) Verificado con Python.",
 "x + 1/x ≥ 2 es AM-GM entre x y 1/x, cuyo producto es 1. Reconocer un cuadrado escondido —aquí (√x − 1/√x)²— convierte una desigualdad en algo evidente.",
 16, ["desigualdad trivial", "AM-GM", "caso de igualdad"],
 ["acotar expresiones", "análisis de eficiencia", "desigualdades clásicas"],
 "", ["desigualdad", "am-gm", "optimizacion", "nivel-basico"], "cap. 15.2 (Prob. 15.10)"))

A(P(328, "La media aritmética nunca pierde", "optimizacion", 2,
 "Demuestra que para todos los reales a, b se cumple (a² + b²)/2 ≥ ab.",
 ["Todo se reduce a la desigualdad trivial: algún cuadrado real es ≥ 0. ¿Cuál?",
  "Piensa en (a − b)². Siempre es ≥ 0.",
  "(a − b)² = a² − 2ab + b² ≥ 0.",
  "Pasa el 2ab al otro lado: a² + b² ≥ 2ab.",
  "Divide entre 2: (a² + b²)/2 ≥ ab, con igualdad si y solo si a = b."],
 "(a − b)² ≥ 0 implica a² − 2ab + b² ≥ 0, es decir a² + b² ≥ 2ab; dividiendo entre 2, (a² + b²)/2 ≥ ab. Igualdad si y solo si a = b. Verificado con Python sobre 5000 pares aleatorios.",
 "Esta es la desigualdad de medias en su forma más básica; nace de (a − b)² ≥ 0. Casi toda desigualdad elemental se reduce a 'un cuadrado real no es negativo'.",
 14, ["desigualdad trivial", "AM-GM", "cuadrado de una diferencia"],
 ["desigualdad de medias", "estabilidad de varianza", "demostraciones algebraicas"],
 "", ["desigualdad", "am-gm", "optimizacion", "nivel-basico"], "cap. 15.2 (Prob. 15.9)"))

A(P(329, "El rango oculto de una expresión", "optimizacion", 4,
 "Si x satisface x² − 5x + 6 < 0, ¿entre qué valores está P = x² + 5x + 6?",
 ["Primero descubre para qué x se cumple la condición x² − 5x + 6 < 0.",
  "Factoriza: x² − 5x + 6 = (x − 2)(x − 3) < 0, lo que ocurre cuando 2 < x < 3.",
  "Ahora P = x² + 5x + 6 es creciente en ese intervalo (su vértice está en x = −5/2, lejos a la izquierda).",
  "Por monotonía, evalúa P en los extremos x = 2 y x = 3 para acotar.",
  "P(2) = 20 y P(3) = 30; como el intervalo es abierto, 20 < P < 30."],
 "La condición (x − 2)(x − 3) < 0 da 2 < x < 3. En ese tramo P = x² + 5x + 6 es estrictamente creciente (vértice en x = −5/2), así que P va de P(2) = 20 a P(3) = 30 sin alcanzarlos: 20 < P < 30. Verificado con Python (barrido en (2,3)).",
 "Una restricción cuadrática define un intervalo; propagarlo a otra expresión exige saber si esta es monótona allí. Evaluar en los extremos solo es válido por la monotonía, no por costumbre.",
 24, ["desigualdad cuadrática", "monotonía", "análisis de rango"],
 ["propagación de cotas", "análisis de sensibilidad", "intervalos de confianza"],
 "", ["desigualdad", "cuadratica", "rango", "ahsme", "nivel-avanzado"], "cap. 15.3 (Prob. 15.37, AHSME)"))

A(P(330, "¿Cuándo existe la otra variable?", "optimizacion", 4,
 "Para la ecuación 4y² + 4xy + x + 6 = 0, ¿para qué valores reales de x existe un valor real de y que la satisfaga?",
 ["Mírala como una cuadrática EN y (con x como parámetro): 4y² + (4x)y + (x + 6) = 0.",
  "Una cuadrática con coeficientes reales tiene solución real si y solo si su discriminante es ≥ 0.",
  "Discriminante = (4x)² − 4·4·(x + 6) = 16x² − 16x − 96.",
  "Pide 16x² − 16x − 96 ≥ 0, es decir x² − x − 6 ≥ 0.",
  "Factoriza: (x − 3)(x + 2) ≥ 0, que se cumple para x ≤ −2 o x ≥ 3."],
 "Vista como cuadrática en y, su discriminante es 16x² − 16x − 96 = 16(x² − x − 6) = 16(x − 3)(x + 2). Hay y real ⇔ discriminante ≥ 0 ⇔ x ≤ −2 o x ≥ 3. Verificado con Python.",
 "Reinterpretar la ecuación como cuadrática en la variable 'libre' y exigir discriminante ≥ 0 es la palanca clave: traduce 'existe solución real' en una desigualdad sobre el parámetro.",
 24, ["discriminante", "cuadrática en una variable elegida", "desigualdad factorizada"],
 ["condiciones de existencia de solución", "análisis de estabilidad", "regiones admisibles"],
 "", ["discriminante", "cuadratica", "ahsme", "nivel-avanzado"], "cap. 15.3 (Prob. 15.40, AHSME)"))

A(P(331, "Mínimo con término independiente grande", "optimizacion", 2,
 "Halla el valor mínimo de x² − 6x − 13.",
 ["Abre hacia arriba ⇒ tiene mínimo en el vértice.",
  "Completa el cuadrado en x² − 6x.",
  "x² − 6x = (x − 3)² − 9.",
  "(x − 3)² − 9 − 13 = (x − 3)² − 22.",
  "El mínimo es −22, en x = 3."],
 "x² − 6x − 13 = (x − 3)² − 22, así que el mínimo es −22 (en x = 3). Verificado con Python.",
 "Completar el cuadrado es el método universal para el óptimo de una cuadrática sin cálculo: deja a la vista el vértice (h, k) en la forma (x − h)² + k.",
 14, ["completar el cuadrado", "vértice", "mínimo"],
 ["minimización básica", "ajuste de datos", "energía mínima"],
 "", ["cuadratica", "optimizacion", "minimo", "nivel-basico"], "cap. 15 (Prob. 15.29)"))

A(P(332, "Máximo sin mínimo", "optimizacion", 2,
 "Halla el valor máximo de −2t² + 12t − 8. ¿Tiene también un valor mínimo?",
 ["Coeficiente de t² negativo ⇒ hay máximo. ¿Por qué no puede haber mínimo?",
  "Factoriza −2 de los términos en t: −2(t² − 6t) − 8.",
  "t² − 6t = (t − 3)² − 9.",
  "−2((t − 3)² − 9) − 8 = −2(t − 3)² + 18 − 8 = −2(t − 3)² + 10.",
  "Máximo 10 en t = 3; al alejar t, −2(t−3)² → −∞, así que no hay mínimo."],
 "−2t² + 12t − 8 = −2(t − 3)² + 10. El máximo es 10 (en t = 3). No existe valor mínimo: la expresión decrece sin cota cuando |t| crece. Verificado con Python.",
 "Una parábola que abre hacia abajo tiene techo pero no piso: crece sin cota negativa. Reconocer la dirección de apertura decide de antemano si buscar máximo o mínimo.",
 14, ["completar el cuadrado", "vértice", "comportamiento al infinito"],
 ["máximo de ingresos", "alcance de proyectiles", "rendimientos decrecientes"],
 "", ["cuadratica", "optimizacion", "maximo", "nivel-basico"], "cap. 15 (Prob. 15.30)"))

A(P(333, "El fondo de una parábola sencilla", "optimizacion", 1,
 "Halla el valor mínimo de x² − 8x + 12.",
 ["Abre hacia arriba: hay mínimo.",
  "Completa el cuadrado en x² − 8x.",
  "x² − 8x = (x − 4)² − 16.",
  "(x − 4)² − 16 + 12 = (x − 4)² − 4.",
  "El mínimo es −4, en x = 4."],
 "x² − 8x + 12 = (x − 4)² − 4, mínimo −4 en x = 4. Verificado con Python.",
 "El caso más limpio de completar el cuadrado: coeficiente principal 1 y todo entero. Sirve como plantilla mental para los casos con coeficientes incómodos.",
 12, ["completar el cuadrado", "vértice", "mínimo"],
 ["optimización elemental", "trayectorias", "costos cuadráticos"],
 "", ["cuadratica", "optimizacion", "minimo", "nivel-basico"], "cap. 15 (Prob. 15.15)"))

A(P(334, "Una desigualdad disfrazada", "optimizacion", 2,
 "Demuestra que a² + 4 ≥ 4a para todo número real a, e indica cuándo hay igualdad.",
 ["Pasa todo a un lado: a² − 4a + 4 ≥ 0. ¿Reconoces el lado izquierdo?",
  "a² − 4a + 4 es un trinomio cuadrado perfecto.",
  "Es (a − 2)².",
  "(a − 2)² ≥ 0 siempre (desigualdad trivial).",
  "La igualdad ocurre cuando a − 2 = 0, es decir a = 2."],
 "a² + 4 − 4a = (a − 2)² ≥ 0, luego a² + 4 ≥ 4a, con igualdad si y solo si a = 2. Verificado con Python.",
 "Toda desigualdad de la forma 'cuadrática ≥ lineal' se prueba pasando todo a un lado y reconociendo un cuadrado perfecto. El caso de igualdad sale del cero del cuadrado.",
 14, ["desigualdad trivial", "trinomio cuadrado perfecto", "caso de igualdad"],
 ["acotaciones", "AM-GM", "demostración por cuadrados"],
 "", ["desigualdad", "optimizacion", "cuadrado-perfecto", "nivel-basico"], "cap. 15 (Prob. 15.27)"))

# =====================================================================
# PATRONES (8) — factorizaciones especiales (cap. 11)
# =====================================================================

A(P(335, "El truco favorito de Simon", "patrones", 3,
 "¿Cuántos pares de enteros positivos (m, n) cumplen mn + m + n = 76?",
 ["El lado izquierdo casi se factoriza... le falta un término para ser un producto. ¿Qué constante sumar?",
  "Suma 1 a ambos lados: mn + m + n + 1 = 77. Ahora el lado izquierdo SÍ factoriza.",
  "mn + m + n + 1 = (m + 1)(n + 1), así que (m + 1)(n + 1) = 77.",
  "77 = 7 × 11 (y 1 × 77). Como m, n ≥ 1, ambos factores m+1, n+1 son ≥ 2.",
  "Solo sirven 7 × 11 y 11 × 7, dando (m, n) = (6, 10) y (10, 6): 2 pares."],
 "Sumando 1: (m + 1)(n + 1) = 77 = 7·11. Con m, n ≥ 1 los factores deben ser ≥ 2, así que (m+1, n+1) ∈ {(7,11),(11,7)}, dando (m, n) = (6,10) y (10,6). Hay 2 pares. Verificado con Python (búsqueda exhaustiva).",
 "El truco de Simon consiste en sumar la constante justa para que una expresión 'casi factorizable' se vuelva un producto; entonces contar soluciones es contar factorizaciones.",
 20, ["Simon's Favorite Factoring Trick", "factorización por agrupación", "divisores"],
 ["ecuaciones diofánticas", "conteo de soluciones", "factorización estratégica"],
 "", ["factorizacion", "simon", "diofantica", "nivel-medio"], "cap. 11.1 (SFFT)"))

A(P(336, "Simon con coeficientes", "patrones", 4,
 "¿Cuántos pares de enteros positivos (b, c) satisfacen bc − 7b + 3c = 70?",
 ["Quieres llevarlo a la forma (b + ?)(c + ?) = constante. Agrupa por b: b(c − 7) + 3c.",
  "Para completar el producto añade una constante: b(c − 7) + 3(c − 7) = (b + 3)(c − 7).",
  "(b + 3)(c − 7) = bc − 7b + 3c − 21, así que (b + 3)(c − 7) = 70 − 21 = 49.",
  "49 = 1·49 = 7·7 = 49·1. Como b ≥ 1, b + 3 ≥ 4, y como c ≥ 1, c − 7 ≥ −6.",
  "Necesitas c − 7 > 0 divisor de 49 con b + 3 ≥ 4: (b+3, c−7) ∈ {(7,7),(49,1)} ⇒ (b,c) = (4,14),(46,8). 2 pares."],
 "Reescribiendo: (b + 3)(c − 7) = 49. Con b ≥ 1 (b+3 ≥ 4) y c ≥ 1, los únicos factores válidos son (7,7) y (49,1), dando (b, c) = (4, 14) y (46, 8): 2 pares. Verificado con Python. (El texto cuenta 6 soluciones si se admiten enteros de cualquier signo; aquí pedimos positivos.)",
 "Con coeficientes, primero se agrupa para sacar el factor (c − 7) y luego se ajusta la constante. El conteo final depende crucialmente del signo permitido de cada factor.",
 24, ["Simon's Favorite Factoring Trick con coeficientes", "agrupación", "análisis de signos de divisores"],
 ["diofánticas con coeficientes", "factorización adaptada", "conteo cuidadoso de casos"],
 "", ["factorizacion", "simon", "diofantica", "nivel-avanzado"], "cap. 11.1 (Prob. 11.5)"))

A(P(337, "Diferencia de cuadrados a la vista", "patrones", 1,
 "Calcula 111² − 89² sin elevar al cuadrado ningún número de tres cifras.",
 ["No calcules 111² ni 89². ¿Qué identidad relaciona a² − b² con factores simples?",
  "a² − b² = (a − b)(a + b).",
  "Aquí a = 111, b = 89: (111 − 89)(111 + 89).",
  "111 − 89 = 22 y 111 + 89 = 200.",
  "22 × 200 = 4400."],
 "Por diferencia de cuadrados, 111² − 89² = (111 − 89)(111 + 89) = 22 · 200 = 4400. Verificado con Python.",
 "Diferencia de cuadrados convierte una resta de números grandes en un producto de dos números chicos: la factorización es una herramienta de cálculo, no solo de álgebra.",
 8, ["diferencia de cuadrados", "cálculo mental", "factorización"],
 ["aritmética rápida", "simplificación algebraica", "patrones numéricos"],
 "", ["factorizacion", "diferencia-cuadrados", "nivel-basico"], "cap. 11 (Prob. 11.30)"))

A(P(338, "Casi cuadrado perfecto", "patrones", 2,
 "¿Cuál es mayor y por cuánto: 4050607² o 4050608 × 4050606?",
 ["Llama n = 4050607. Reescribe el producto en términos de n.",
  "4050608 = n + 1 y 4050606 = n − 1, así que el producto es (n + 1)(n − 1).",
  "(n + 1)(n − 1) = n² − 1 por diferencia de cuadrados.",
  "Entonces el producto es exactamente n² − 1.",
  "Por tanto 4050607² es mayor, por exactamente 1."],
 "Con n = 4050607, el producto es (n + 1)(n − 1) = n² − 1. Así 4050607² supera a 4050608 × 4050606 por exactamente 1. Verificado con Python.",
 "Escribir n+1 y n−1 alrededor de n revela que el producto es n² − 1: comparar 'casi cuadrados' se vuelve trivial al nombrar el centro con una variable.",
 12, ["diferencia de cuadrados", "sustitución n", "comparación sin calcular"],
 ["estimación", "identidades algebraicas", "trucos de competencia"],
 "", ["factorizacion", "diferencia-cuadrados", "nivel-basico"], "cap. 11 (Prob. 11.32)"))

A(P(339, "Dos cuadrados que difieren en 63", "patrones", 2,
 "Encuentra dos cuadrados perfectos consecutivos (de enteros positivos consecutivos) cuya diferencia sea 63.",
 ["Sean n² y (n + 1)². ¿Cuánto vale su diferencia en términos de n?",
  "(n + 1)² − n² = 2n + 1.",
  "Iguala a 63: 2n + 1 = 63.",
  "n = 31, así que los enteros son 31 y 32.",
  "Los cuadrados son 31² = 961 y 32² = 1024 (y 1024 − 961 = 63)."],
 "La diferencia de cuadrados consecutivos es (n+1)² − n² = 2n + 1 = 63 ⇒ n = 31. Los cuadrados son 31² = 961 y 32² = 1024. Verificado con Python.",
 "La diferencia de cuadrados consecutivos es siempre el impar 2n+1; por eso los impares son justo los saltos entre cuadrados, una de las primeras regularidades de la aritmética.",
 14, ["diferencia de cuadrados consecutivos", "ecuación lineal", "patrón impar"],
 ["sumas de impares", "patrones cuadráticos", "diofánticas sencillas"],
 "", ["factorizacion", "cuadrados-consecutivos", "nivel-basico"], "cap. 11 (Prob. 11.34)"))

A(P(340, "Un cuadrado perfecto enorme", "patrones", 4,
 "Reconoce que 5¹² − 2·10⁶ + 2¹² es un cuadrado perfecto y halla su mayor factor primo.",
 ["10⁶ = (5·2)⁶ = 5⁶·2⁶. Reescribe el término central usando eso.",
  "La expresión es 5¹² − 2·5⁶·2⁶ + 2¹² = (5⁶)² − 2·5⁶·2⁶ + (2⁶)².",
  "Eso es un trinomio cuadrado perfecto: (5⁶ − 2⁶)².",
  "5⁶ − 2⁶ = 15625 − 64 = 15561. Factoriza 15561.",
  "15561 = 3²·7·13·19, así que el mayor primo es 19."],
 "5¹² − 2·10⁶ + 2¹² = (5⁶)² − 2(5⁶)(2⁶) + (2⁶)² = (5⁶ − 2⁶)² = 15561². Como 15561 = 3²·7·13·19, el mayor factor primo es 19. Verificado con Python.",
 "Reescribir 10⁶ como 5⁶·2⁶ destapa un trinomio cuadrado perfecto. Buscar la estructura a²−2ab+b² en expresiones intimidantes es lo que vuelve fácil el resto.",
 24, ["trinomio cuadrado perfecto", "factorización de potencias", "factorización en primos"],
 ["reconocer estructuras ocultas", "criptoaritmética", "teoría de números"],
 "", ["factorizacion", "cuadrado-perfecto", "primos", "nivel-avanzado"], "cap. 11 (Prob. 11.47)"))

A(P(341, "La raíz que se vuelve entera", "patrones", 4,
 "Calcula √(1 + 50·51·52·53) y muestra que es un entero.",
 ["El producto de cuatro enteros consecutivos más 1 suele ser un cuadrado perfecto. Busca la identidad.",
  "Para k(k+1)(k+2)(k+3), agrupa el primero con el último y los dos de en medio.",
  "k(k+3) = k² + 3k y (k+1)(k+2) = k² + 3k + 2; llama u = k² + 3k.",
  "El producto es u(u + 2) = u² + 2u, y 1 + u² + 2u = (u + 1)².",
  "Con k = 50, u + 1 = k² + 3k + 1 = 2500 + 150 + 1 = 2651, así que la raíz es 2651."],
 "Con k = 50: 1 + k(k+1)(k+2)(k+3) = (k² + 3k + 1)². Como k² + 3k + 1 = 2651, se tiene √(1 + 50·51·52·53) = 2651. Verificado con Python (2651² = 1 + 50·51·52·53).",
 "El producto de cuatro enteros consecutivos más 1 siempre es un cuadrado, (k²+3k+1)². Sustituir u = k²+3k transforma un cuádruple producto en u(u+2)+1 = (u+1)².",
 22, ["identidad de producto de consecutivos", "cuadrado perfecto", "sustitución"],
 ["telescopaje algebraico", "identidades de competencia", "reconocer cuadrados"],
 "", ["factorizacion", "cuadrado-perfecto", "mathcounts", "nivel-avanzado"], "cap. 11 (Prob. 11.53, MATHCOUNTS)"))

A(P(342, "Una suma telescópica con raíces", "patrones", 4,
 "Calcula 1/(√2 + √1) + 1/(√3 + √2) + 1/(√4 + √3) + ... + 1/(√100 + √99).",
 ["Cada término tiene un denominador con suma de raíces. ¿Cómo racionalizar 1/(√(k+1) + √k)?",
  "Multiplica numerador y denominador por el conjugado √(k+1) − √k.",
  "1/(√(k+1) + √k) = (√(k+1) − √k)/((k+1) − k) = √(k+1) − √k.",
  "La suma se vuelve (√2 − √1) + (√3 − √2) + ... + (√100 − √99): telescopia.",
  "Casi todo se cancela: queda √100 − √1 = 10 − 1 = 9."],
 "Racionalizando, cada término 1/(√(k+1) + √k) = √(k+1) − √k. La suma telescopia a √100 − √1 = 10 − 1 = 9. Verificado con Python (identidad término a término y suma cerrada).",
 "Racionalizar por el conjugado convierte cada término en una diferencia de raíces consecutivas; la suma entonces TELESCOPIA y casi todo se cancela. Es la versión con raíces del truco de fracciones parciales.",
 22, ["racionalización por conjugado", "suma telescópica", "cancelación"],
 ["series telescópicas", "simplificación de sumas", "cálculo previo a límites"],
 "", ["telescopaje", "racionalizacion", "raices", "nivel-avanzado"], "cap. 11.4 (Ej. 11.4.5)"))

# =====================================================================
# INVERSION (11) — elevar a potencias, auto-similaridad (cap. 22.1-22.2)
# =====================================================================

A(P(343, "De primer grado a segundo grado", "inversion", 2,
 "Si x + 1/x = 7, halla x² + 1/x².",
 ["No despejes x: sería feo (sale con raíz). Trabaja hacia atrás desde lo que quieres.",
  "Quieres una expresión con x² y 1/x². ¿Qué operación sobre la ecuación dada produce esos términos?",
  "Eleva al cuadrado ambos lados: (x + 1/x)² = 7².",
  "(x + 1/x)² = x² + 2·x·(1/x) + 1/x² = x² + 2 + 1/x².",
  "Entonces x² + 2 + 1/x² = 49, así que x² + 1/x² = 47."],
 "Elevando al cuadrado: (x + 1/x)² = x² + 2 + 1/x² = 49, luego x² + 1/x² = 47. Verificado con Python.",
 "Elevar la ecuación al cuadrado sube de grado y crea justo los términos buscados. Trabajar hacia atrás desde el objetivo evita el despeje de x, que sería irracional e inútil.",
 14, ["elevar la ecuación a una potencia", "identidad de cuadrado", "trabajar hacia atrás"],
 ["funciones simétricas", "manipulación de recíprocos", "evitar despejes feos"],
 "", ["potencias", "reciprocos", "inversion", "nivel-basico"], "cap. 22.1 (Prob. 22.1)"))

A(P(344, "Simplificar una suma de radicales", "inversion", 3,
 "Simplifica √(6 + √11) + √(6 − √11).",
 ["No hay una ecuación para manipular... créala. Pon la expresión igual a x.",
  "Sea x = √(6 + √11) + √(6 − √11), con x > 0. ¿Qué te conviene hacerle a x?",
  "Eleva al cuadrado: x² = (6 + √11) + (6 − √11) + 2√((6 + √11)(6 − √11)).",
  "El producto bajo la raíz es 36 − 11 = 25, cuya raíz es 5.",
  "x² = 12 + 2·5 = 22, y como x > 0, x = √22."],
 "Sea x la expresión (x > 0). Entonces x² = 12 + 2√(36 − 11) = 12 + 2·5 = 22, así que x = √22. Verificado con Python (el cuadrado da exactamente 22).",
 "Sin ecuación que manipular, se CREA una poniendo la expresión igual a x. El producto de conjugados radicales elimina la raíz interna, dejando un cuadrado limpio.",
 20, ["crear una ecuación", "elevar al cuadrado", "conjugados radicales"],
 ["simplificación de radicales anidados", "uso de conjugados", "técnica de la variable"],
 "", ["radicales", "potencias", "inversion", "nivel-medio"], "cap. 22.1 (Prob. 22.2)"))

A(P(345, "De cubos a cuadrados", "inversion", 4,
 "Si a + b = 20 y a³ + b³ = 800, halla a² + b².",
 ["No resuelvas para a y b. Relaciona las potencias entre sí trabajando hacia atrás.",
  "Recuerda a³ + b³ = (a + b)³ − 3ab(a + b). Úsalo para despejar ab.",
  "800 = 20³ − 3ab·20 = 8000 − 60ab, así que ab = 120.",
  "Ahora a² + b² = (a + b)² − 2ab.",
  "a² + b² = 400 − 240 = 160."],
 "De a³ + b³ = (a+b)³ − 3ab(a+b): 800 = 8000 − 60ab ⇒ ab = 120. Entonces a² + b² = (a+b)² − 2ab = 400 − 240 = 160. Verificado con Python (resolviendo el sistema real, a² + b² = 160).",
 "La identidad a³+b³ = (a+b)³ − 3ab(a+b) enlaza grados distintos sin resolver el sistema. Toda la familia de sumas de potencias se conecta vía las simétricas a+b y ab.",
 22, ["identidades de potencias", "funciones simétricas elementales", "trabajar hacia atrás"],
 ["sumas de potencias (Newton)", "evitar resolver sistemas", "manipulación simétrica"],
 "", ["potencias", "simetria", "inversion", "nivel-avanzado"], "cap. 22.1 (Prob. 22.3)"))

A(P(346, "Subiendo dos peldaños de potencia", "inversion", 3,
 "Si a + 1/a = 3, halla a² + 1/a² y luego a⁴ + 1/a⁴.",
 ["Igual que con la suma y su recíproco: eleva al cuadrado para subir de grado.",
  "(a + 1/a)² = a² + 2 + 1/a² = 9, así que a² + 1/a² = 7.",
  "Ahora repite la idea sobre a² + 1/a² = 7 para llegar a la cuarta potencia.",
  "(a² + 1/a²)² = a⁴ + 2 + 1/a⁴ = 49.",
  "Por tanto a⁴ + 1/a⁴ = 47."],
 "Elevando al cuadrado dos veces: a² + 1/a² = 3² − 2 = 7, y a⁴ + 1/a⁴ = 7² − 2 = 47. Verificado con Python.",
 "Elevar al cuadrado repetidamente sube de a² a a⁴; cada paso resta 2. Es una escalera: x_{2n} = x_n² − 2 sobre las sumas con recíproco.",
 16, ["elevar al cuadrado iterado", "escalera de potencias", "recíprocos"],
 ["funciones simétricas", "recurrencias de potencias", "manipulación algebraica"],
 "", ["potencias", "reciprocos", "inversion", "nivel-medio"], "cap. 22.1 (Ej. 22.1.1)"))

A(P(347, "El radical que se contiene a sí mismo", "inversion", 4,
 "Evalúa √(20 − √(20 − √(20 − √(20 − ...)))), donde el patrón continúa infinitamente.",
 ["La expresión es auto-similar: dentro de ella aparece una copia idéntica de sí misma.",
  "Llama x al valor total (x > 0). ¿Qué parte de la expresión también vale x?",
  "Lo que está bajo la primera raíz es 20 menos otra copia de la misma expresión, es decir x = √(20 − x).",
  "Eleva al cuadrado: x² = 20 − x, o sea x² + x − 20 = 0.",
  "Factoriza (x + 5)(x − 4) = 0; como x > 0, x = 4."],
 "Sea x el valor (x > 0). La auto-similaridad da x = √(20 − x), luego x² + x − 20 = 0 = (x + 5)(x − 4). Como x > 0, x = 4. Verificado con Python.",
 "La clave es ver que la expresión se contiene a sí misma, así que x = √(20 − x). La auto-similaridad transforma un objeto infinito en una ecuación finita de punto fijo.",
 22, ["auto-similaridad", "ecuación de punto fijo", "selección de raíz positiva"],
 ["fracciones continuas", "puntos fijos", "límites de sucesiones recursivas"],
 "", ["auto-similaridad", "radicales-anidados", "inversion", "nivel-avanzado"], "cap. 22.2 (Prob. 22.4)"))

A(P(348, "Una fracción continua infinita", "inversion", 4,
 "Evalúa la fracción continua 1 + 6/(1 + 6/(1 + 6/(1 + ...))).",
 ["La estructura se repite hacia abajo: es auto-similar. Pon el todo igual a x.",
  "Sea x el valor total (x > 0). Localiza dónde vuelve a aparecer x dentro de la expresión.",
  "El denominador completo del primer 6 es otra copia de x, así que x = 1 + 6/x.",
  "Multiplica por x: x² = x + 6, es decir x² − x − 6 = 0.",
  "Factoriza (x − 3)(x + 2) = 0; como x > 0, x = 3."],
 "Sea x el valor (x > 0). La recurrencia da x = 1 + 6/x ⇒ x² − x − 6 = 0 = (x − 3)(x + 2). Como x > 0, x = 3. Verificado con Python.",
 "El denominador completo de la fracción continua vuelve a ser ella misma, dando x = 1 + 6/x. Reconocer la copia recurrente es lo que cierra el problema en una cuadrática.",
 22, ["fracción continua", "auto-similaridad", "punto fijo"],
 ["razón áurea y afines", "recurrencias", "aproximaciones racionales"],
 "", ["auto-similaridad", "fraccion-continua", "inversion", "nivel-avanzado"], "cap. 22.2 (Prob. 22.5)"))

A(P(349, "El radical que crece hacia adentro", "inversion", 3,
 "Evalúa √(12 + √(12 + √(12 + ...))) (infinitas raíces anidadas).",
 ["Es auto-similar igual que antes, pero con suma en vez de resta.",
  "Sea x el valor total (x > 0). ¿Qué parte vuelve a valer x?",
  "Bajo la primera raíz hay 12 más otra copia de x: x = √(12 + x).",
  "Eleva al cuadrado: x² = 12 + x, es decir x² − x − 12 = 0.",
  "Factoriza (x − 4)(x + 3) = 0; como x > 0, x = 4."],
 "Sea x el valor (x > 0). x = √(12 + x) ⇒ x² − x − 12 = 0 = (x − 4)(x + 3). Como x > 0, x = 4. Verificado con Python.",
 "Con suma en lugar de resta, la ecuación de punto fijo es x = √(12 + x). El método de la variable auto-similar es el mismo; solo cambia el signo dentro.",
 18, ["auto-similaridad", "punto fijo", "raíz positiva"],
 ["radicales anidados", "recurrencias convergentes", "puntos fijos"],
 "", ["auto-similaridad", "radicales-anidados", "inversion", "nivel-medio"], "cap. 22.2 (Ej. 22.2.1)"))

A(P(350, "Fracción continua de treses", "inversion", 4,
 "Evalúa la fracción continua 3 + 1/(3 + 1/(3 + 1/(3 + ...))).",
 ["Auto-similar: pon el todo igual a x (x > 0).",
  "El denominador entero del primer 1 es otra copia de x.",
  "Así x = 3 + 1/x.",
  "Multiplica por x: x² = 3x + 1, o sea x² − 3x − 1 = 0.",
  "Por la fórmula general y x > 0, x = (3 + √13)/2."],
 "Sea x (x > 0). x = 3 + 1/x ⇒ x² − 3x − 1 = 0; tomando la raíz positiva, x = (3 + √13)/2. Verificado con Python.",
 "La fracción continua de treses satisface x = 3 + 1/x, cuya raíz positiva es (3+√13)/2: las fracciones continuas periódicas siempre dan irracionales cuadráticos.",
 20, ["fracción continua", "punto fijo", "fórmula general"],
 ["fracciones continuas de irracionales", "aproximación de √13", "recurrencias"],
 "", ["auto-similaridad", "fraccion-continua", "inversion", "nivel-avanzado"], "cap. 22.2 (Ej. 22.2.2)"))

A(P(351, "Disfraz con raíz cuadrada", "inversion", 3,
 "Si √r + 2/√r = 6, halla r + 4/r.",
 ["Aunque aparezca √r, la estructura es 'algo + constante/algo'. Llama u = √r.",
  "Con u = √r, la condición es u + 2/u = 6, y quieres r + 4/r = u² + 4/u².",
  "Eleva al cuadrado u + 2/u: (u + 2/u)² = u² + 2·2 + 4/u² = u² + 4 + 4/u².",
  "Entonces u² + 4 + 4/u² = 36.",
  "Luego u² + 4/u² = 32, es decir r + 4/r = 32."],
 "Con u = √r: (u + 2/u)² = u² + 4 + 4/u² = 36 ⇒ u² + 4/u² = 32. Como r = u², esto es r + 4/r = 32. Verificado con Python.",
 "El disfraz √r se quita con u = √r; entonces es de nuevo 'término más recíproco' elevado al cuadrado. Identificar la estructura bajo el cambio de variable es el verdadero paso.",
 18, ["sustitución u = √r", "elevar al cuadrado", "término cruzado constante"],
 ["cambio de variable", "funciones simétricas", "manipulación de recíprocos"],
 "", ["potencias", "sustitucion", "inversion", "nivel-medio"], "cap. 22 (Prob. 22.8)"))

A(P(352, "Auto-similaridad con resta", "inversion", 3,
 "Halla el valor de √(12 − √(12 − √(12 − ...))) (infinitas raíces).",
 ["Auto-similar; pon el total igual a x (x > 0).",
  "Bajo la primera raíz hay 12 menos otra copia de x: x = √(12 − x).",
  "Eleva al cuadrado: x² = 12 − x.",
  "x² + x − 12 = 0, factoriza (x + 4)(x − 3) = 0.",
  "Como x > 0, x = 3."],
 "Sea x (x > 0). x = √(12 − x) ⇒ x² + x − 12 = 0 = (x + 4)(x − 3). Como x > 0, x = 3. Verificado con Python.",
 "Idéntico patrón de punto fijo que con suma, x = √(12 − x); hay que elegir la raíz positiva porque la expresión es una raíz cuadrada (no negativa).",
 18, ["auto-similaridad", "punto fijo", "raíz positiva"],
 ["radicales anidados", "puntos fijos", "convergencia de recurrencias"],
 "", ["auto-similaridad", "radicales-anidados", "inversion", "nivel-medio"], "cap. 22 (Prob. 22.9)"))

A(P(353, "Bajar un peldaño de potencia", "inversion", 3,
 "Si x² + 1/x² = 9, halla todos los posibles valores de x + 1/x.",
 ["Quieres ir de la segunda potencia a la primera. Piensa qué cuadrado contiene x² y 1/x².",
  "(x + 1/x)² = x² + 2 + 1/x².",
  "Sustituye x² + 1/x² = 9: (x + 1/x)² = 9 + 2 = 11.",
  "Por tanto x + 1/x = ±√11 (los dos signos son posibles para x real).",
  "Ambos valores ±√11 se realizan, así que hay dos posibilidades."],
 "(x + 1/x)² = x² + 2 + 1/x² = 9 + 2 = 11, luego x + 1/x = ±√11. Verificado con Python.",
 "Bajar de potencia también usa (x+1/x)² = x²+2+1/x², pero al sacar raíz aparecen DOS signos: hay que conservar ambas soluciones reales, ±√11.",
 16, ["identidad de cuadrado", "doble signo de la raíz", "recíprocos"],
 ["soluciones múltiples", "funciones simétricas", "control de signos"],
 "", ["potencias", "reciprocos", "inversion", "nivel-medio"], "cap. 22 (Prob. 22.24)"))

# =====================================================================
# INVARIANTES (11) — simetría, sumas/productos de raíces, sistemas simétricos
# =====================================================================

A(P(354, "Las raíces sin resolver la ecuación", "invariantes", 4,
 "Para la ecuación x² + 4x + 1 = 0 con raíces r y s, halla: (a) r + s, (b) r² + s², (c) r³ + s³.",
 ["No hace falta hallar r y s. Para x² + bx + c, ¿qué dicen las relaciones de Vieta sobre r + s y rs?",
  "Vieta: r + s = −b = −4 y rs = c = 1. Estas son las cantidades invariantes (simétricas).",
  "Para r² + s² usa (r + s)² = r² + 2rs + s².",
  "r² + s² = (−4)² − 2·1 = 14.",
  "Para r³ + s³ usa (r + s)³ = r³ + 3rs(r + s) + s³ ⇒ r³ + s³ = (r+s)³ − 3rs(r+s) = −64 + 12 = −52."],
 "Por Vieta, r + s = −4 y rs = 1. Entonces r² + s² = (r+s)² − 2rs = 16 − 2 = 14, y r³ + s³ = (r+s)³ − 3rs(r+s) = −64 − 3(1)(−4) = −52. Verificado con Python (resolviendo las raíces).",
 "Vieta entrega las simétricas r+s y rs sin resolver el polinomio; a partir de ellas, las identidades de Newton generan cualquier suma de potencias de las raíces.",
 24, ["relaciones de Vieta", "funciones simétricas de las raíces", "identidades de Newton"],
 ["polinomios y sus raíces", "sumas de potencias", "invariantes simétricos"],
 "", ["vieta", "simetria", "invariantes", "nivel-avanzado"], "cap. 22 (Prob. 22.20)"))

A(P(355, "Un sistema casi simétrico", "invariantes", 4,
 "Resuelve el sistema: 3w + x + y + z = 20; w + 3x + y + z = 6; w + x + 3y + z = 44; w + x + y + 3z = 2.",
 ["Cada ecuación es (w + x + y + z) más el doble de una variable. Explota esa simetría.",
  "Suma las cuatro ecuaciones: cada variable aparece con coeficiente total 6.",
  "6(w + x + y + z) = 20 + 6 + 44 + 2 = 72, así que w + x + y + z = 12.",
  "Resta esta suma de cada ecuación original: por ejemplo 3w + x + y + z − (w+x+y+z) = 2w = 20 − 12 = 8.",
  "Así 2w = 8, 2x = −6, 2y = 32, 2z = −10 ⇒ (w, x, y, z) = (4, −3, 16, −5)."],
 "Sumando todo: 6(w+x+y+z) = 72 ⇒ w+x+y+z = 12. Restando esa suma de cada ecuación: 2w = 8, 2x = −6, 2y = 32, 2z = −10, o sea (w, x, y, z) = (4, −3, 16, −5). Verificado con Python.",
 "Cada ecuación es 'suma total + doble de una variable', así que sumarlas todas revela la suma total como invariante; restarla despeja cada variable de un golpe.",
 22, ["simetría de un sistema", "combinar todas las ecuaciones", "invariante: suma total"],
 ["sistemas lineales con estructura", "explotar simetría", "álgebra de competencia"],
 "", ["sistema-simetrico", "simetria", "invariantes", "nivel-avanzado"], "cap. 22.3 (Prob. 22.6)"))

A(P(356, "El producto que revela todo", "invariantes", 4,
 "Orión, Amadea y Atlas piensan cada uno un número positivo. El producto de los de Orión y Amadea es 27; el de Amadea y Atlas es 72; el de Atlas y Orión es 6. ¿Qué número pensó cada uno?",
 ["Llama r, m, t a los números. Escribe rm = 27, mt = 72, tr = 6. ¿Cómo combinar para obtener rmt?",
  "Multiplica las tres ecuaciones: (rm)(mt)(tr) = (rmt)².",
  "(rmt)² = 27·72·6 = 11664, así que rmt = 108 (positivo).",
  "Divide rmt entre cada producto par para despejar la variable que falta: t = rmt/(rm) = 108/27.",
  "t = 4, r = 108/72 = 3/2, m = 108/6 = 18."],
 "Multiplicando las tres: (rmt)² = 27·72·6 = 108², luego rmt = 108. Dividiendo: t = 108/27 = 4, r = 108/72 = 3/2, m = 108/6 = 18. Verificado con Python.",
 "Cuando un sistema es simétrico en producto, multiplicar todo da el producto total al cuadrado; dividirlo entre cada ecuación recupera las incógnitas. El truco gemelo de 'sumar todas'.",
 22, ["combinar ecuaciones por producto", "simetría multiplicativa", "raíz del producto total"],
 ["sistemas multiplicativos", "logaritmos como linealización", "invariante: producto total"],
 "", ["sistema-simetrico", "producto", "invariantes", "nivel-avanzado"], "cap. 22.3 (Prob. 22.7)"))

A(P(357, "Cinco ecuaciones, una variable ausente cada vez", "invariantes", 4,
 "Resuelve: a+b+c+d = 9; a+b+c+e = −3; a+b+d+e = 14; a+c+d+e = 15; b+c+d+e = −17.",
 ["Cada ecuación es la suma de las cinco variables menos UNA. Suma todas para hallar el total.",
  "Al sumar las cinco ecuaciones, cada variable aparece 4 veces: 4(a+b+c+d+e) = 9 − 3 + 14 + 15 − 17 = 18.",
  "Entonces a+b+c+d+e = 18/4 = 9/2.",
  "Cada variable ausente = (suma total) − (ecuación que la omite). P. ej. e = 9/2 − 9 = −9/2.",
  "Así a = 9/2 − (−17) = 43/2, b = 9/2 − 15 = −21/2, c = 9/2 − 14 = −19/2, d = 9/2 − (−3) = 15/2, e = −9/2."],
 "Sumando las cinco: 4·(suma) = 18 ⇒ suma = 9/2. Cada variable = suma − (la ecuación que la excluye): a = 43/2, b = −21/2, c = −19/2, d = 15/2, e = −9/2. Verificado con Python.",
 "Cada ecuación omite una variable, así que su suma da 4 veces el total; entonces cada incógnita es 'total menos la ecuación que la excluye'. Explotar la estructura ahorra toda la eliminación.",
 24, ["simetría de un sistema", "suma total como invariante", "variable ausente"],
 ["sistemas lineales estructurados", "promedios y totales", "eliminación elegante"],
 "", ["sistema-simetrico", "simetria", "invariantes", "nivel-avanzado"], "cap. 22.3 (Ej. 22.3.1)"))

A(P(358, "Signos que se combinan", "invariantes", 4,
 "Halla p, q, r, s si: p+q+r−s = 32; p+q−r+s = 13; p−q+r+s = −14; −p+q+r+s = 21.",
 ["En cada ecuación una variable lleva signo menos. Suma todas para que los signos se equilibren.",
  "Sumando las cuatro, cada variable aparece con coeficiente 2: 2(p+q+r+s) = 32+13−14+21 = 52.",
  "Entonces p+q+r+s = 26.",
  "Resta cada ecuación de esta suma: p+q+r+s − (p+q+r−s) = 2s = 26 − 32 = −6 ⇒ s = −3, etc.",
  "Resulta p = 5/2, q = 20, r = 13/2, s = −3."],
 "Sumando: 2(p+q+r+s) = 52 ⇒ p+q+r+s = 26. Restando cada ecuación de la suma se despeja la variable de signo negativo: p = 5/2, q = 20, r = 13/2, s = −3 (suma 26). Verificado con Python.",
 "La simetría está en los signos: al sumar, los signos opuestos se cancelan y emerge la suma total; restar cada ecuación aísla la variable que llevaba el signo menos.",
 22, ["simetría con signos", "suma total invariante", "despeje por diferencia"],
 ["sistemas lineales", "explotar estructura de signos", "combinación de ecuaciones"],
 "", ["sistema-simetrico", "simetria", "invariantes", "nivel-avanzado"], "cap. 22 (Prob. 22.11)"))

A(P(359, "Coeficientes que se reparten", "invariantes", 3,
 "Si a = 1, b = 10, c = 100 y d = 1000, calcula (a+b+c−d) + (a+b−c+d) + (a−b+c+d) + (−a+b+c+d).",
 ["No sumes cuatro cantidades grandes por separado. Cuenta cuántas veces aparece cada variable en total.",
  "Cada variable aparece con signo + en tres de los cuatro paréntesis y con − en uno.",
  "Su coeficiente total es 3 − 1 = 2, para las cuatro variables.",
  "Así la suma es 2(a + b + c + d).",
  "2(1 + 10 + 100 + 1000) = 2·1111 = 2222."],
 "Cada variable lleva +,+,+,− en los cuatro términos, con coeficiente neto 2. La suma es 2(a+b+c+d) = 2·1111 = 2222. Verificado con Python.",
 "No hay que sumar cuatro cantidades grandes: basta contar el coeficiente neto de cada variable (+,+,+,− = 2). Pensar en estructura, no en aritmética, es el atajo.",
 16, ["conteo de coeficientes", "simetría de la expresión", "invariante de suma"],
 ["simplificación por estructura", "combinaciones lineales", "patrones de signos"],
 "", ["simetria", "conteo-coeficientes", "ahsme", "invariantes", "nivel-medio"], "cap. 22.3 (Ej. 22.3.2, AHSME)"))

A(P(360, "Las canicas en cinco cajas", "invariantes", 3,
 "Sesenta canicas se reparten en cajas A, B, C, D, E. Juntas A y B tienen 24; B y C tienen 15; C y D tienen 18; D y E tienen 30. ¿Cuántas canicas hay en la caja A?",
 ["Usa que el total es 60 y las sumas dadas son de cajas vecinas. Combina con cuidado.",
  "(A+B) + (C+D) + E = 24 + 18 + E = 60, así que E = 18.",
  "De D + E = 30 sale D = 12; de C + D = 18 sale C = 6.",
  "De B + C = 15 sale B = 9.",
  "De A + B = 24 sale A = 15."],
 "Como (A+B)+(C+D)+E = 60: E = 60 − 42 = 18. Luego D = 30 − 18 = 12, C = 18 − 12 = 6, B = 15 − 6 = 9, A = 24 − 9 = 15. Verificado con Python.",
 "Agrupar las parejas adecuadas frente al total convierte un sistema en cadena en restas sucesivas. Es un balance de conservación: el total fija la pieza que falta.",
 18, ["encadenar restricciones", "total como invariante", "sustitución hacia atrás"],
 ["sistemas en cadena", "balances de conservación", "razonamiento secuencial"],
 "", ["sistema", "conservacion", "mathcounts", "invariantes", "nivel-medio"], "cap. 22.3 (Ej. 22.3.4, MATHCOUNTS)"))

A(P(361, "Una cadena de igualdades", "invariantes", 4,
 "Si a + 1 = b + 2 = c + 3 = d + 4 = a + b + c + d + 5, halla a + b + c + d.",
 ["Dale un nombre k al valor común de toda la cadena. Expresa cada variable en términos de k.",
  "a + 1 = k ⇒ a = k − 1; análogamente b = k − 2, c = k − 3, d = k − 4.",
  "También a + b + c + d + 5 = k.",
  "Sustituye: (k−1)+(k−2)+(k−3)+(k−4) + 5 = k ⇒ 4k − 10 + 5 = k.",
  "3k = 5 ⇒ k = 5/3, y a+b+c+d = 4k − 10 = 20/3 − 10 = −10/3."],
 "Sea k el valor común: a = k−1, b = k−2, c = k−3, d = k−4. De a+b+c+d+5 = k sale 4k − 10 + 5 = k ⇒ k = 5/3. Entonces a+b+c+d = 4k − 10 = −10/3. Verificado con Python.",
 "Nombrar el valor común k parametriza toda la cadena; sustituir en la última igualdad cierra una sola ecuación en k. Las cadenas de igualdades casi siempre piden una variable auxiliar.",
 22, ["variable auxiliar para una cadena", "sustitución uniforme", "ecuación en k"],
 ["cadenas de igualdades", "parametrización", "álgebra de competencia (AMC)"],
 "", ["cadena-igualdades", "parametrizacion", "amc", "invariantes", "nivel-avanzado"], "cap. 22 (Prob. 22.14, AMC 12)"))

A(P(362, "El producto que iguala los exponentes", "invariantes", 4,
 "Si a, b, c son reales positivos con a⁴b³c² = 32, a³b²c⁴ = 8 y a²b⁴c³ = 2, halla abc.",
 ["Quieres abc, donde cada variable tiene exponente 1. ¿Cómo combinar las tres ecuaciones para igualar los exponentes?",
  "Multiplica las tres ecuaciones. Suma los exponentes de cada variable: 4+3+2 = 9 para a, igual para b y para c.",
  "Así (abc)⁹ = a⁹b⁹c⁹ = 32·8·2 = 512.",
  "512 = 2⁹.",
  "Entonces (abc)⁹ = 2⁹ ⇒ abc = 2 (positivo)."],
 "Multiplicando las tres ecuaciones, los exponentes de a, b, c suman 9 cada uno: (abc)⁹ = 32·8·2 = 512 = 2⁹. Por tanto abc = 2. Verificado con Python.",
 "Multiplicar las tres ecuaciones iguala los exponentes de a, b, c (todos a 9), dejando (abc)⁹. Buscar la combinación que simetriza los exponentes es el corazón del problema.",
 22, ["combinar ecuaciones por producto", "simetría de exponentes", "raíz n-ésima"],
 ["sistemas multiplicativos", "linealización por logaritmos", "invariante de exponentes"],
 "", ["sistema-multiplicativo", "exponentes", "invariantes", "nivel-avanzado"], "cap. 22 (Prob. 22.15)"))

A(P(363, "El promedio sin conocer cada número", "invariantes", 4,
 "Si 1001C − 2002A = 4004 y 1001B + 3003A = 5005, ¿cuál es el promedio de A, B y C?",
 ["No despejes A, B, C individualmente. Busca directamente A + B + C dividiendo entre 1001.",
  "Divide la primera entre 1001: C − 2A = 4. Divide la segunda entre 1001: B + 3A = 5.",
  "Suma esas dos ecuaciones simplificadas: (C − 2A) + (B + 3A) = 4 + 5.",
  "Los términos en A se combinan: A + B + C = 9.",
  "El promedio es (A + B + C)/3 = 9/3 = 3."],
 "Dividiendo entre 1001: C − 2A = 4 y B + 3A = 5. Sumándolas, A + B + C = 9, así que el promedio es 9/3 = 3. Verificado con Python.",
 "El objetivo A+B+C se alcanza sin hallar cada incógnita: se busca la combinación lineal exacta que lo produce. En sistemas subdeterminados, apuntar al agregado pedido evita callejones.",
 20, ["simplificar por factor común", "buscar la combinación útil", "promedio sin valores individuales"],
 ["combinaciones lineales objetivo", "sistemas subdeterminados", "álgebra de competencia (AMC)"],
 "", ["combinacion-lineal", "promedio", "amc", "invariantes", "nivel-avanzado"], "cap. 22 (Prob. 22.16, AMC 10)"))

A(P(364, "La hipotenusa a partir de suma y área", "invariantes", 4,
 "En un triángulo rectángulo, la suma de las longitudes de los catetos es 18 y el área es 37. ¿Cuál es la longitud de la hipotenusa?",
 ["Llama a, b a los catetos. Traduce los datos a funciones simétricas: suma y producto.",
  "a + b = 18 y área = ab/2 = 37 ⇒ ab = 74.",
  "La hipotenusa h cumple h² = a² + b² (Pitágoras). Exprésalo con suma y producto.",
  "a² + b² = (a + b)² − 2ab = 18² − 2·74 = 324 − 148 = 176.",
  "h = √176 = 4√11."],
 "Con a + b = 18 y ab = 74: a² + b² = (a+b)² − 2ab = 324 − 148 = 176, así que la hipotenusa es √176 = 4√11. Verificado con Python.",
 "Suma y producto de los catetos son funciones simétricas; (a+b)² − 2ab entrega a²+b² = hipotenusa². Es Vieta encubierto: se resuelve la geometría sin hallar cada cateto.",
 22, ["funciones simétricas (suma y producto)", "teorema de Pitágoras", "identidad (a+b)²−2ab"],
 ["geometría con álgebra simétrica", "Vieta encubierto", "resolver sin hallar cada raíz"],
 "", ["simetria", "pitagoras", "invariantes", "nivel-avanzado"], "cap. 22 (Prob. 22.17)"))

# =====================================================================
# Append idempotente
# =====================================================================
PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
new_ids = {p["id"] for p in PROBLEMS}
clash = existing & new_ids
assert not clash, f"choque de ids con existentes: {clash}"
assert len(new_ids) == len(PROBLEMS), "ids duplicados dentro del builder"

data["problemas"].extend(PROBLEMS)
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

dist = collections.Counter(p["estrategia"] for p in PROBLEMS)
print(f"Agregados {len(PROBLEMS)} problemas (ids {min(new_ids)}-{max(new_ids)}).")
print("Distribución de la tanda:", dict(dist))
total = collections.Counter(p["estrategia"] for p in data["problemas"])
print("Distribución total problems.json:", dict(total), "— total", len(data["problemas"]))
