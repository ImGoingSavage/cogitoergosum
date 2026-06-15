# -*- coding: utf-8 -*-
"""Tanda 34 — Richard Rusczyk, *Introduction to Geometry* (Art of Problem Solving).
Append 44 problemas verificados a data/problems.json. Fuentes internas:
 - Cap. 4 «Perimeter and Area» (razón de áreas con base/altura común, máximos de
   área, trabajar hacia atrás desde área/perímetro).
 - Cap. 6 «Right Triangles» (Teorema de Pitágoras, ternas pitagóricas, triángulos
   45-45-90 y 30-60-90, fórmula del triángulo equilátero, escalera deslizante).
 - Cap. 9 «Polygons» (suma de ángulos interiores/exteriores, diagonales, áreas).
 - Power of a Point / ángulo inscrito (cap. 12-13) como invariantes.
Mapeo a las 4 estrategias canónicas (11 c/u, balance GLOBAL -> 102/102/102/102):
 - invariantes: lo que permanece constante (sumas de ángulos, razón de áreas con
   base/altura compartida, producto potencia de un punto, ángulo inscrito).
 - patrones: ternas pitagóricas y triángulos especiales (regularidades ocultas).
 - optimizacion: máximos/mínimos de área y perímetro, camino más corto (reflexión).
 - inversion: trabajar hacia atrás desde el área/perímetro hacia las dimensiones.
TODA afirmación numérica verificada con Python (ver bitácora HANDOFFCES.md). El
libro de soluciones es un volumen aparte no disponible: cada número fue resuelto
y comprobado de forma independiente. Nota: la cuenta de triángulos rectángulos
enteros con un cateto = 24 (Prob. 6.54) Python la fija en 7. Builder idempotente:
aborta si hay choque de ids. Sector C (entrenamiento), esquema §4.1, ids 365-408."""
import json, collections

SRC = "Rusczyk, *Introduction to Geometry* (Art of Problem Solving, 2nd ed.)"

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
# INVARIANTES (11) — sumas de ángulos, razón de áreas, potencia de un punto
# =====================================================================

A(P(365, "El polígono delatado por su ángulo", "invariantes", 2,
 "Cada ángulo interior de un polígono regular mide 140°. ¿Cuántos lados tiene?",
 ["¿Qué cantidad NO cambia sin importar la forma exacta del polígono? La suma total de sus ángulos interiores.",
  "Para un polígono de n lados, la suma de los ángulos interiores es siempre (n − 2)·180°. Esa fórmula es el invariante.",
  "Si es regular, cada ángulo es esa suma dividida entre n: (n − 2)·180°/n = 140°.",
  "Otra vía: el ángulo exterior es 180° − 140° = 40°, y los exteriores SIEMPRE suman 360°.",
  "360° ÷ 40° = 9. Comprueba con la fórmula interior: (9 − 2)·180/9 = 140. ✓"],
 "El ángulo exterior es 180° − 140° = 40°. Como los ángulos exteriores de cualquier polígono convexo suman exactamente 360° (invariante), el número de lados es 360/40 = 9. Verificado: (9 − 2)·180/9 = 140°.",
 "La suma de ángulos exteriores = 360° es uno de los invariantes más útiles de la geometría: no depende del número de lados. Convierte un problema de interiores en una simple división.",
 12, ["suma de ángulos exteriores", "polígono regular", "ángulo interior"],
 ["diseño de engranajes", "teselados", "navegación por rumbos"],
 "", ["poligono", "angulos", "invariante", "nivel-basico"], "cap. 9.6 (Prob. 9.18)"))

A(P(366, "Treinta y seis lados", "invariantes", 2,
 "¿Cuánto mide cada ángulo interior de un polígono regular de 36 lados?",
 ["No midas: usa el invariante de la suma. ¿Cuánto suman TODOS los ángulos interiores de un 36-ágono?",
  "Suma de interiores = (n − 2)·180° = (36 − 2)·180°.",
  "Como es regular, los 36 ángulos son iguales: divide la suma entre 36.",
  "Atajo: el ángulo exterior es 360/36 = 10°, así que el interior es 180 − 10.",
  "34·180/36 = 6120/36 = 170°."],
 "Suma de ángulos interiores = (36 − 2)·180° = 6120°. Cada uno mide 6120/36 = 170°. (Atajo: exterior = 360/36 = 10°, interior = 180 − 10 = 170°.) Verificado con Python.",
 "Cuando muchos lados hacen el dibujo imposible, el invariante de la suma resuelve sin necesidad de visualizar la figura. El ángulo exterior 360/n es la ruta más corta.",
 10, ["suma de ángulos interiores", "ángulo exterior", "polígono regular"],
 ["arquitectura de cúpulas", "modelado 3D", "ruedas dentadas"],
 "", ["poligono", "angulos", "invariante", "nivel-basico"], "cap. 9.6 (Prob. 9.19)"))

A(P(367, "Un ángulo exterior diminuto", "invariantes", 2,
 "Los ángulos exteriores de un polígono regular miden 6° cada uno. ¿Cuántos lados tiene?",
 ["El dato clave es un invariante puro: ¿cuánto suman todos los ángulos exteriores de cualquier polígono convexo?",
  "Suman 360°, sin importar cuántos lados haya.",
  "Si todos los exteriores son iguales (regular) y cada uno mide 6°, ¿cuántos caben en 360°?",
  "n = 360° / (ángulo exterior).",
  "360 / 6 = 60 lados."],
 "Los ángulos exteriores suman 360° (invariante). Si cada uno mide 6°, entonces n = 360/6 = 60 lados. Verificado con Python.",
 "Un ángulo exterior muy pequeño significa muchos lados: el polígono se parece cada vez más a un círculo. El invariante 360° captura esa idea con una división.",
 8, ["ángulo exterior", "suma 360", "polígono regular"],
 ["aproximación de círculos", "discretización", "diseño de tuercas"],
 "", ["poligono", "angulos", "invariante", "nivel-basico"], "cap. 9.6 (Prob. 9.21)"))

A(P(368, "Contar lados por las diagonales", "invariantes", 3,
 "Un polígono tiene exactamente 27 diagonales. ¿Cuántos lados tiene?",
 ["Cada diagonal une dos vértices que NO son adyacentes. ¿Cuántas parejas de vértices hay en total?",
  "De n vértices salen C(n,2) = n(n−1)/2 segmentos entre pares; n de ellos son lados, el resto diagonales.",
  "Número de diagonales = n(n−1)/2 − n = n(n−3)/2. Esa fórmula es fija para cada n.",
  "Plantea n(n−3)/2 = 27, es decir n(n−3) = 54.",
  "Busca dos factores que difieran en 3 y multipliquen 54: 9·6 = 54, así que n = 9."],
 "El número de diagonales de un polígono de n lados es n(n−3)/2. Igualando a 27: n(n−3) = 54. Como 9·6 = 54, resulta n = 9 (un nonágono). Verificado con Python: 9·6/2 = 27.",
 "La fórmula n(n−3)/2 es invariante: solo depende de cuántos vértices hay, no de la forma. Reconocer 54 = 9·6 (factores que difieren en 3) cierra el problema sin resolver la cuadrática.",
 14, ["diagonales de un polígono", "combinatoria de vértices", "factorización"],
 ["redes de comunicación", "grafos completos", "apretones de manos"],
 "", ["poligono", "diagonales", "invariante", "nivel-intermedio"], "cap. 9.6 (Prob. 9.27)"))

A(P(369, "Exterior, una octava parte del interior", "invariantes", 3,
 "En un polígono regular, cada ángulo exterior mide 1/8 de su ángulo interior. ¿Cuántos lados tiene?",
 ["Hay un invariante local: en cada vértice, el ángulo interior y el exterior son suplementarios (suman 180°).",
  "Llama e al exterior e i al interior. Sabes que e + i = 180° y que e = i/8.",
  "Sustituye: i/8 + i = 180° ⇒ (9/8)i = 180°.",
  "Despeja i = 160°, de modo que e = 20°.",
  "Usa el invariante global: n = 360°/e = 360/20 = 18."],
 "Interior + exterior = 180° y exterior = interior/8. Entonces interior/8 + interior = 180° ⇒ interior = 160°, exterior = 20°. Como los exteriores suman 360°, n = 360/20 = 18 lados. Verificado con Python.",
 "Se combinan dos invariantes: el local (suplementarios en cada vértice) y el global (exteriores suman 360°). Es típico que un problema 'difícil' sea solo dos hechos constantes encadenados.",
 14, ["ángulos suplementarios", "suma de exteriores", "polígono regular"],
 ["relojería", "diseño paramétrico", "tolerancias angulares"],
 "", ["poligono", "angulos", "invariante", "nivel-intermedio"], "cap. 9.6 (Prob. 9.23)"))

A(P(370, "Tantas diagonales como lados", "invariantes", 3,
 "Un polígono tiene exactamente el mismo número de diagonales que de lados. ¿Cuánto suman sus ángulos interiores?",
 ["Usa la fórmula invariante del número de diagonales: n(n−3)/2.",
  "Iguala diagonales y lados: n(n−3)/2 = n. Divide entre n (n ≠ 0).",
  "(n−3)/2 = 1 ⇒ n − 3 = 2 ⇒ n = 5: es un pentágono.",
  "La suma de ángulos interiores también es invariante: (n − 2)·180°.",
  "(5 − 2)·180° = 540°."],
 "n(n−3)/2 = n ⇒ n − 3 = 2 ⇒ n = 5. La suma de los ángulos interiores de un pentágono es (5 − 2)·180° = 540°. Verificado con Python.",
 "Dos invariantes (número de diagonales y suma de interiores) se usan en cascada: el primero identifica la figura, el segundo responde la pregunta. Cada uno depende solo de n.",
 14, ["diagonales", "suma de interiores", "pentágono"],
 ["clasificación de figuras", "grafos", "diseño estructural"],
 "", ["poligono", "diagonales", "invariante", "nivel-intermedio"], "cap. 9.6 (Prob. 9.30)"))

A(P(371, "Dos cortes sobre el mismo ángulo", "invariantes", 3,
 "En el triángulo ABC, el punto X está sobre el lado CB con CX = 2·BX, y el punto Y está sobre el lado AB con AY = 3·BY. Si el área de ABC es 144, ¿cuál es el área del triángulo BXY?",
 ["El triángulo BXY comparte el ángulo en B con el triángulo BCA. ¿Qué fórmula de área usa dos lados y el ángulo entre ellos?",
  "Área = (1/2)·(lado1)·(lado2)·sen(ángulo). El sen(B) es el mismo para ambos triángulos: se cancela.",
  "Como CX = 2·BX, todo el lado CB mide BX + CX = 3·BX, así que BX = CB/3.",
  "Como AY = 3·BY, todo el lado AB mide BY + AY = 4·BY, así que BY = AB/4.",
  "[BXY]/[BCA] = (BX/BC)·(BY/BA) = (1/3)·(1/4) = 1/12, luego [BXY] = 144/12 = 12."],
 "Ambos triángulos comparten el ángulo B, así que la razón de áreas es el producto de las razones de los lados que lo forman: (BX/BC)·(BY/BA). Con BX = BC/3 y BY = BA/4, la razón es 1/12 y [BXY] = 144·(1/12) = 12. Verificado con Python.",
 "El invariante es sen(B): al compartir el ángulo, la razón de áreas no depende de su valor. Reducir áreas a productos de razones de lados es una de las herramientas más potentes de la geometría de competencia.",
 18, ["razón de áreas", "ángulo compartido", "área = ½ab·senC"],
 ["escalado de mapas", "proporciones en diseño", "semejanza"],
 "", ["area", "razon", "invariante", "nivel-intermedio"], "cap. 4 (Prob. 4.32, MATHCOUNTS)"))

A(P(372, "El área fija la altura", "invariantes", 1,
 "Un triángulo tiene área 42 y uno de sus lados mide 7. ¿Cuánto mide la altura trazada hacia ese lado?",
 ["Recuerda la relación que SIEMPRE liga área, base y altura de un triángulo.",
  "Área = (base · altura) / 2. Aquí la base es el lado de longitud 7.",
  "Sustituye lo que sabes: 42 = (7 · altura) / 2.",
  "Despeja: 7 · altura = 84.",
  "altura = 84 / 7 = 12."],
 "Área = base·altura/2 ⇒ 42 = 7·h/2 ⇒ h = 84/7 = 12. Verificado con Python.",
 "Para un lado fijo como base, el área determina la altura de forma única: es una relación invariante. (Ojo: el área NO determina el perímetro; muchos triángulos distintos comparten base, altura y área.)",
 8, ["área de triángulo", "base y altura", "despeje"],
 ["cálculo de alturas inaccesibles", "agrimensura", "diseño de rampas"],
 "", ["area", "triangulo", "invariante", "nivel-basico"], "cap. 4 (Prob. 4.14)"))

A(P(373, "La ceviana reparte el área", "invariantes", 2,
 "En el triángulo ABC, el punto D está sobre el lado BC de modo que BD:DC = 3:5. Si el área de ABC es 64, ¿cuál es el área del triángulo ABD?",
 ["Los triángulos ABD y ABC (o ABD y ADC) comparten algo que no cambia: la altura desde A hacia la recta BC.",
  "Cuando dos triángulos tienen la misma altura, la razón de sus áreas es la razón de sus bases.",
  "ABD y ADC tienen la misma altura desde A; sus bases son BD y DC, en razón 3:5.",
  "Por tanto [ABD] : [ABC] = BD : BC = 3 : (3+5) = 3 : 8.",
  "[ABD] = 64 · 3/8 = 24."],
 "ABD y ADC comparten la altura desde A, así que sus áreas están en la razón de las bases BD:DC = 3:5. Entonces [ABD] = [ABC]·BD/BC = 64·3/8 = 24. Verificado con Python.",
 "La altura compartida es el invariante: el área se vuelve proporcional a la base. Una ceviana reparte el área de un triángulo en la misma razón en que divide al lado opuesto.",
 12, ["altura compartida", "razón de bases", "ceviana"],
 ["reparto proporcional", "presupuestos por superficie", "catastro"],
 "", ["area", "razon", "invariante", "nivel-basico"], "cap. 4.3 (Same Base/Same Altitude)"))

A(P(374, "El producto que no cambia", "invariantes", 3,
 "Dos cuerdas de un círculo se cruzan en un punto interior P. La primera cuerda queda dividida por P en segmentos de longitud 4 y 6. La segunda cuerda queda dividida en un segmento de longitud 3 y otro desconocido. ¿Cuánto mide el segmento desconocido?",
 ["Cuando dos cuerdas se cruzan, hay una cantidad que es la misma sin importar qué cuerda elijas: se llama 'potencia del punto'.",
  "El teorema dice: PA · PB = PC · PD, el producto de los dos trozos de una cuerda iguala al de la otra.",
  "Para la primera cuerda ese producto es 4 · 6 = 24.",
  "Para la segunda debe valer lo mismo: 3 · x = 24.",
  "x = 24 / 3 = 8."],
 "Por la potencia de un punto, el producto de los segmentos de cualquier cuerda que pasa por P es constante: 4·6 = 3·x ⇒ x = 24/3 = 8. Verificado con Python.",
 "La 'potencia de un punto' es un invariante notable: dado P y el círculo, el producto de las distancias a los dos cortes de cualquier recta que pase por P no cambia. De ahí su nombre.",
 16, ["potencia de un punto", "cuerdas que se cruzan", "producto invariante"],
 ["óptica geométrica", "triangulación", "intersección de trayectorias"],
 "", ["circulo", "potencia-punto", "invariante", "nivel-intermedio"], "cap. 13 (Power of a Point)"))

A(P(375, "Medio del centro", "invariantes", 2,
 "En un círculo, un ángulo central abarca un arco de 100°. Otro ángulo, con su vértice SOBRE el círculo, abarca exactamente ese mismo arco. ¿Cuánto mide este ángulo inscrito?",
 ["Compara dos ángulos que 'ven' el mismo arco: uno desde el centro y otro desde el borde.",
  "Un ángulo central mide lo mismo que su arco: 100°.",
  "El teorema del ángulo inscrito relaciona el ángulo en el borde con el arco que abarca.",
  "Un ángulo inscrito mide siempre la MITAD del arco que subtiende.",
  "100° / 2 = 50°."],
 "Por el teorema del ángulo inscrito, un ángulo con vértice en el círculo mide la mitad del arco que abarca: 100°/2 = 50°. Verificado con Python.",
 "El invariante es contundente: TODOS los ángulos inscritos que subtienden el mismo arco son iguales (la mitad del central). Por eso un ángulo inscrito en un semicírculo siempre mide 90°.",
 10, ["ángulo inscrito", "ángulo central", "arco"],
 ["diseño de lentes", "fotografía (ángulo de visión)", "arcos arquitectónicos"],
 "", ["circulo", "angulo-inscrito", "invariante", "nivel-basico"], "cap. 12 (Inscribed Angles)"))

# =====================================================================
# PATRONES (11) — ternas pitagóricas y triángulos especiales
# =====================================================================

A(P(376, "La terna disfrazada con decimales", "patrones", 2,
 "En un triángulo rectángulo, la hipotenusa mide 6 y uno de los catetos mide 3.6. ¿Cuánto mide el otro cateto?",
 ["Antes de calcular raíces, sospecha de una terna pitagórica conocida escondida tras los decimales.",
  "Divide los datos por un factor común: 6 y 3.6 son 5 y 3 multiplicados por 1.2.",
  "La terna 3-4-5 es la más famosa. Si la hipotenusa 6 = 5·1.2 y un cateto 3.6 = 3·1.2…",
  "…el cateto que falta debería ser 4·1.2.",
  "4 · 1.2 = 4.8. Comprueba: 3.6² + 4.8² = 12.96 + 23.04 = 36 = 6². ✓"],
 "Los datos son la terna 3-4-5 escalada por 1.2: hipotenusa 5·1.2 = 6, cateto 3·1.2 = 3.6, así que el otro cateto es 4·1.2 = 4.8. Verificado: 3.6² + 4.8² = 36 = 6².",
 "Las ternas pitagóricas se conservan al multiplicar por cualquier factor: si (a,b,c) funciona, (ka,kb,kc) también. Reconocer el patrón evita raíces cuadradas feas.",
 12, ["terna pitagórica 3-4-5", "escalado de ternas", "teorema de Pitágoras"],
 ["medición rápida en obra", "verificar escuadras", "gráficos a escala"],
 "", ["pitagoras", "terna", "patron", "nivel-basico"], "cap. 6.3 (Prob. 6.27a)"))

A(P(377, "Catetos grandes, terna conocida", "patrones", 2,
 "Un triángulo rectángulo tiene catetos de longitud 45 y 24. ¿Cuánto mide la hipotenusa? (Busca el patrón, no fuerces la calculadora.)",
 ["Saca factor común a 45 y 24 para descubrir una terna pequeña.",
  "45 = 3·15 y 24 = 3·8, así que ambos son múltiplos de 3: piensa en la terna (8, 15, 17).",
  "Catetos 24 = 8·3 y 45 = 15·3 corresponden a (8,15,17) escalada por 3.",
  "Entonces la hipotenusa es 17·3.",
  "17 · 3 = 51. Comprueba: 24² + 45² = 576 + 2025 = 2601 = 51². ✓"],
 "24 = 8·3 y 45 = 15·3 son la terna (8,15,17) multiplicada por 3, así que la hipotenusa es 17·3 = 51. Verificado: 24² + 45² = 2601 = 51².",
 "Memorizar unas pocas ternas primitivas —(3,4,5),(5,12,13),(8,15,17),(7,24,25)— y reconocer sus múltiplos convierte cálculos pesados en multiplicaciones mentales.",
 12, ["terna pitagórica 8-15-17", "múltiplos de ternas", "Pitágoras"],
 ["ingeniería estructural", "topografía", "control de calidad"],
 "", ["pitagoras", "terna", "patron", "nivel-basico"], "cap. 6.3 (Prob. 6.27b)"))

A(P(378, "Una terna multiplicada por raíz de dos", "patrones", 3,
 "Un triángulo rectángulo tiene un cateto de longitud 5√2 y una hipotenusa de longitud 13√2. ¿Cuánto mide el otro cateto?",
 ["El factor común √2 aparece en ambos datos: factorízalo y mira la terna que queda.",
  "Quitando √2: cateto 5, hipotenusa 13. ¿Qué terna empieza con 5 y termina en 13?",
  "La terna (5, 12, 13). El cateto faltante sin el factor es 12.",
  "Como todo está multiplicado por √2, el cateto buscado es 12√2.",
  "Comprueba: (5√2)² + (12√2)² = 50 + 288 = 338 = (13√2)². ✓"],
 "Factorizando √2, los datos son la terna (5,12,13): cateto 5√2, hipotenusa 13√2, así que el otro cateto es 12√2. Verificado: (5√2)² + (12√2)² = 50 + 288 = 338 = (13√2)².",
 "El patrón pitagórico se conserva incluso con factores irracionales: (5,12,13) escalada por √2 sigue siendo rectángulo. Buscar el factor común simplifica antes de operar.",
 14, ["terna 5-12-13", "factor común irracional", "Pitágoras"],
 ["geometría con radicales", "diagonales de rectángulos", "vectores"],
 "", ["pitagoras", "terna", "patron", "nivel-intermedio"], "cap. 6.3 (Prob. 6.27c)"))

A(P(379, "El triángulo de la media tuerca", "patrones", 2,
 "En un triángulo rectángulo, un ángulo agudo mide 30° y la hipotenusa mide 10. ¿Cuánto miden los dos catetos?",
 ["Un triángulo rectángulo con un ángulo de 30° es uno de los dos 'triángulos especiales'. Sus lados siguen una proporción fija.",
  "En un 30-60-90 los lados están en razón 1 : √3 : 2 (frente a 30°, frente a 60°, hipotenusa).",
  "La hipotenusa corresponde al '2' de la razón; aquí vale 10, así que la unidad es 5.",
  "El cateto opuesto a 30° es el '1' = 5; el opuesto a 60° es '√3' = 5√3.",
  "Catetos: 5 y 5√3. Comprueba: 5² + (5√3)² = 25 + 75 = 100 = 10². ✓"],
 "En un triángulo 30-60-90 los lados están en razón 1 : √3 : 2. Con hipotenusa 10 (el '2'), la unidad es 5: el cateto opuesto a 30° mide 5 y el opuesto a 60° mide 5√3. Verificado: 5² + (5√3)² = 100.",
 "Los triángulos 30-60-90 y 45-45-90 aparecen una y otra vez; conocer sus razones (1:√3:2 y 1:1:√2) ahorra usar Pitágoras cada vez. Es reconocer un patrón, no calcular.",
 12, ["triángulo 30-60-90", "razón 1:√3:2", "triángulo especial"],
 ["trigonometría sin tablas", "diseño de rampas", "cristalografía"],
 "", ["triangulo-especial", "30-60-90", "patron", "nivel-basico"], "cap. 6.2 (Two Special Right Triangles)"))

A(P(380, "La diagonal del cuadrado", "patrones", 1,
 "Un triángulo rectángulo isósceles tiene catetos de longitud 7. ¿Cuánto mide su hipotenusa?",
 ["Un triángulo rectángulo isósceles tiene dos ángulos de 45°: es el otro 'triángulo especial'.",
  "En un 45-45-90 los lados están en razón 1 : 1 : √2 (cateto : cateto : hipotenusa).",
  "La hipotenusa es siempre el cateto multiplicado por √2.",
  "Aquí el cateto es 7.",
  "Hipotenusa = 7√2. Comprueba: 7² + 7² = 98 = (7√2)². ✓"],
 "En un triángulo 45-45-90 la hipotenusa es el cateto por √2: 7√2. Verificado: 7² + 7² = 98 = (7√2)².",
 "El 45-45-90 es la mitad de un cuadrado partido por su diagonal; por eso la diagonal de un cuadrado de lado s mide s√2. Patrón fijo, sin cálculos.",
 8, ["triángulo 45-45-90", "razón 1:1:√2", "diagonal de cuadrado"],
 ["diagonales de pantallas", "carpintería", "diseño de baldosas"],
 "", ["triangulo-especial", "45-45-90", "patron", "nivel-basico"], "cap. 6.2 (Two Special Right Triangles)"))

A(P(381, "¿Es rectángulo o no?", "patrones", 2,
 "¿Pueden 11, 16 y 19 ser las longitudes de los lados de un triángulo rectángulo?",
 ["El recíproco del teorema de Pitágoras decide: un triángulo es rectángulo si y solo si el cuadrado del lado mayor iguala la suma de los cuadrados de los otros dos.",
  "Identifica el lado mayor: 19. Será la hipotenusa candidata.",
  "Calcula 11² + 16² y compáralo con 19².",
  "11² + 16² = 121 + 256 = 377; en cambio 19² = 361.",
  "Como 377 ≠ 361, NO es rectángulo (de hecho 377 > 361, así que el ángulo mayor es obtuso)."],
 "Por el recíproco de Pitágoras, sería rectángulo solo si 11² + 16² = 19². Pero 121 + 256 = 377 ≠ 361 = 19². No es rectángulo. Verificado con Python.",
 "El recíproco de Pitágoras también clasifica: si a² + b² > c² el ángulo mayor es agudo; si es <, es obtuso. Aquí 377 > 361 indica un triángulo obtusángulo.",
 10, ["recíproco de Pitágoras", "clasificación de triángulos", "lado mayor"],
 ["verificar perpendicularidad", "control de estructuras", "GPS y trilateración"],
 "", ["pitagoras", "clasificacion", "patron", "nivel-basico"], "cap. 6 (Prob. 6.29)"))

A(P(382, "Construir una terna desde un cateto", "patrones", 4,
 "Un cateto de un triángulo rectángulo mide 22 y los otros dos lados también tienen longitudes enteras. ¿Cuál es el perímetro del triángulo?",
 ["Si los lados son enteros, busca una terna pitagórica con 22 como uno de los catetos. Usa la diferencia de cuadrados.",
  "Si los catetos son 22 y b y la hipotenusa c, entonces c² − b² = 22², es decir (c − b)(c + b) = 484.",
  "c − b y c + b tienen la misma paridad y su producto 484 es par, así que ambos deben ser pares. Escribe c − b = 2 y c + b = 242.",
  "Resolviendo: c = 122 y b = 120.",
  "Perímetro = 22 + 120 + 122 = 264. Comprueba: 22² + 120² = 484 + 14400 = 14884 = 122². ✓"],
 "Con catetos 22 y b e hipotenusa c: (c−b)(c+b) = 484. Tomando c−b = 2, c+b = 242 ⇒ c = 122, b = 120. Perímetro = 22 + 120 + 122 = 264. Verificado: 22² + 120² = 14884 = 122².",
 "La factorización c² − b² = (c−b)(c+b) es el motor para generar ternas pitagóricas a partir de un cateto dado. La restricción de paridad (ambos factores pares) descarta combinaciones imposibles.",
 22, ["diferencia de cuadrados", "generar ternas", "paridad"],
 ["criptografía (factorización)", "teoría de números", "diseño de retículas"],
 "", ["pitagoras", "terna", "patron", "nivel-avanzado"], "cap. 6.3 (Prob. 6.41)"))

A(P(383, "¿Cuántos triángulos con un cateto de 24?", "patrones", 5,
 "Las longitudes de los tres lados de un triángulo rectángulo son números enteros, y uno de los catetos mide 24. ¿Cuántos triángulos rectángulos distintos (no congruentes) existen con esta propiedad?",
 ["Plantea 24² + b² = c² con b y c enteros, b el otro cateto. Reescríbelo como diferencia de cuadrados.",
  "c² − b² = 576, es decir (c − b)(c + b) = 576. Cuenta de cuántas formas válidas se factoriza 576.",
  "Necesitas c − b y c + b con la MISMA paridad (para que b y c sean enteros) y c − b < c + b.",
  "Como 576 es par, ambos factores deben ser pares. Lista los pares (d, 576/d) con ambos pares y d < 576/d.",
  "Hay exactamente 7 de esas factorizaciones, y cada una da un triángulo distinto. La respuesta es 7."],
 "Con (c−b)(c+b) = 576 y ambos factores pares (misma paridad) y c−b < c+b, hay 7 factorizaciones válidas. Dan los triángulos con catetos 24 y {7, 10, 18, 32, 45, 70, 143}. La respuesta es 7. Verificado por enumeración en Python.",
 "Contar ternas es contar factorizaciones con la paridad correcta. Python confirmó 7 (no 6): es la trampa de este problema, fácil de subcontar si se olvida algún factor par de 576.",
 28, ["conteo de ternas", "factorización de 576", "paridad"],
 ["combinatoria de divisores", "teoría de números computacional", "criptoanálisis"],
 "", ["pitagoras", "terna", "conteo", "patron", "nivel-avanzado"], "cap. 6 (Prob. 6.54, ★)"))

A(P(384, "El 6-8-10 que se delata", "patrones", 1,
 "Un triángulo tiene lados de longitud 6, 8 y 10. ¿Cuál es su área?",
 ["Mira si los tres lados forman una terna pitagórica conocida antes de buscar fórmulas de área complicadas.",
  "6, 8, 10 es la terna 3-4-5 multiplicada por 2: comprueba 6² + 8² = 10².",
  "Entonces el triángulo es RECTÁNGULO, con catetos 6 y 8 e hipotenusa 10.",
  "El área de un triángulo rectángulo es (cateto · cateto)/2.",
  "Área = 6·8/2 = 24."],
 "6² + 8² = 36 + 64 = 100 = 10², así que es rectángulo con catetos 6 y 8. Área = 6·8/2 = 24. Verificado con Python.",
 "Detectar una terna pitagórica entre los lados revela un ángulo recto 'gratis', y con él los catetos sirven de base y altura. Patrón → atajo de área.",
 8, ["terna 6-8-10", "triángulo rectángulo", "área con catetos"],
 ["agrimensura", "cálculo rápido de superficies", "diseño de terrenos"],
 "", ["pitagoras", "terna", "area", "patron", "nivel-basico"], "cap. 6 (Prob. 6.34a)"))

A(P(385, "El área del triángulo equilátero", "patrones", 2,
 "¿Cuál es el área de un triángulo equilátero de lado 6?",
 ["Un equilátero se parte en dos triángulos 30-60-90 al trazar una altura; usa ese patrón para hallar la altura.",
  "La altura cae sobre la mitad de la base: forma un 30-60-90 con hipotenusa 6 y base 3.",
  "En razón 1:√3:2, la altura (opuesta a 60°) es 3√3.",
  "Área = base·altura/2 = 6·(3√3)/2.",
  "= 9√3. (En general, el área de un equilátero de lado s es s²√3/4.)"],
 "La altura de un equilátero de lado 6 es 6·√3/2 = 3√3. Área = 6·3√3/2 = 9√3. (Fórmula general: s²√3/4 = 36√3/4 = 9√3.) Verificado con Python.",
 "Del patrón 30-60-90 sale la fórmula que conviene memorizar: área de un equilátero = s²√3/4. Reconocer el triángulo especial dentro de la figura es la clave.",
 12, ["triángulo equilátero", "altura 30-60-90", "área s²√3/4"],
 ["mallas triangulares", "estructuras tipo cercha", "nanomateriales hexagonales"],
 "", ["equilatero", "area", "patron", "nivel-basico"], "cap. 6 (área del equilátero)"))

A(P(386, "Equilátero de altura conocida", "patrones", 3,
 "Un triángulo equilátero tiene una altura de longitud 8. ¿Cuál es su área?",
 ["Usa el patrón 30-60-90 que aparece al trazar la altura de un equilátero: relaciona altura y lado.",
  "La altura es el lado por √3/2, así que altura = s·√3/2 = 8 ⇒ s = 16/√3.",
  "El área es s²√3/4. Calcula s² = 256/3.",
  "Área = (256/3)·√3/4 = 64√3/3.",
  "Atajo: para un equilátero, área = altura²/√3 = 64/√3 = 64√3/3 ≈ 36.95."],
 "altura = s√3/2 = 8 ⇒ s = 16/√3, s² = 256/3. Área = (256/3)(√3/4) = 64√3/3 ≈ 36.95. (Atajo: área = h²/√3.) Verificado con Python.",
 "Cuando se conoce la altura en vez del lado, el mismo patrón 30-60-90 se usa al revés. El atajo área = h²/√3 evita pasar por el lado.",
 14, ["equilátero", "altura y lado", "racionalizar"],
 ["diseño con restricciones de altura", "óptica de prismas", "arquitectura"],
 "", ["equilatero", "area", "patron", "nivel-intermedio"], "cap. 6 (Prob. 6.36)"))

# =====================================================================
# OPTIMIZACION (11) — máximos/mínimos de área, perímetro, camino más corto
# =====================================================================

A(P(387, "El rectángulo de área máxima", "optimizacion", 2,
 "Entre todos los rectángulos cuyo perímetro es 40, ¿cuál es el área máxima posible y qué forma tiene ese rectángulo?",
 ["Con perímetro fijo, la suma de largo y ancho está fija. ¿Cuánto vale largo + ancho?",
  "Perímetro 40 ⇒ 2(l + w) = 40 ⇒ l + w = 20. Quieres maximizar el producto l·w con esa suma fija.",
  "Para suma fija, el producto es máximo cuando los dos números son iguales (desigualdad AM-GM o vértice de la parábola).",
  "l = w = 10: el rectángulo óptimo es un cuadrado.",
  "Área máxima = 10·10 = 100."],
 "Con l + w = 20 fijo, el producto l·w es máximo cuando l = w (AM-GM). El cuadrado de lado 10 da área 10·10 = 100. Verificado con Python.",
 "Principio isoperimétrico en versión rectangular: a perímetro fijo, el cuadrado maximiza el área. Es la desigualdad AM-GM aplicada a largo y ancho.",
 12, ["perímetro fijo", "AM-GM", "rectángulo óptimo"],
 ["diseño de corrales", "empaques eficientes", "asignación de recursos"],
 "", ["optimizacion", "area", "rectangulo", "nivel-basico"], "cap. 4 (isoperimétrico)"))

A(P(388, "El cerco más corto", "optimizacion", 2,
 "Entre todos los rectángulos de área 36, ¿cuál tiene el perímetro mínimo y cuánto vale ese perímetro?",
 ["Ahora el área (el producto l·w) está fija y quieres minimizar el perímetro 2(l + w).",
  "l·w = 36 fijo; minimizar l + w. Por AM-GM, l + w ≥ 2√(l·w).",
  "2√36 = 12, con igualdad cuando l = w.",
  "l = w = 6: de nuevo un cuadrado.",
  "Perímetro mínimo = 2(6 + 6) = 24."],
 "Con l·w = 36 fijo, AM-GM da l + w ≥ 2√36 = 12, con igualdad si l = w = 6. El perímetro mínimo es 2·12 = 24 (un cuadrado). Verificado con Python.",
 "Es el recíproco del problema isoperimétrico: a área fija, el cuadrado minimiza el perímetro. AM-GM funciona en ambos sentidos según qué se fije.",
 12, ["área fija", "AM-GM", "perímetro mínimo"],
 ["minimizar material", "diseño de envases", "burbujas y tensión superficial"],
 "", ["optimizacion", "perimetro", "rectangulo", "nivel-basico"], "cap. 4 (isoperimétrico)"))

A(P(389, "El ángulo recto maximiza", "optimizacion", 3,
 "Dos lados de un triángulo miden 5 y 8. Variando el ángulo entre ellos, ¿cuál es la mayor área que puede alcanzar el triángulo?",
 ["Escribe el área usando los dos lados dados y el ángulo entre ellos.",
  "Área = (1/2)·5·8·sen(θ), donde θ es el ángulo entre los lados de longitud 5 y 8.",
  "Lo único variable es sen(θ). ¿Cuándo es máximo el seno?",
  "sen(θ) ≤ 1, con máximo en θ = 90°.",
  "Área máxima = (1/2)·5·8·1 = 20 (cuando los lados son perpendiculares)."],
 "Área = (1/2)·5·8·sen θ. Como sen θ ≤ 1 con máximo en θ = 90°, el área máxima es (1/2)·5·8 = 20, lograda cuando los dos lados forman un ángulo recto. Verificado con Python.",
 "Con dos lados fijos, el área es máxima cuando son perpendiculares: ahí cada lado es la altura del otro. La fórmula ½ab·senC convierte la optimización en 'maximizar el seno'.",
 14, ["área = ½ab·senC", "maximizar seno", "ángulo recto"],
 ["diseño de brazos mecánicos", "máxima cobertura", "vela y empuje del viento"],
 "", ["optimizacion", "area", "triangulo", "nivel-intermedio"], "cap. 6/18 (½ab·senC)"))

A(P(390, "La altura más corta", "optimizacion", 3,
 "Un triángulo tiene lados de longitud 15, 20 y 25. ¿Cuál es la longitud de su altura más corta?",
 ["Para cada lado tomado como base, hay una altura. ¿Qué relación liga base y altura con el área (que es la misma siempre)?",
  "Primero, 15² + 20² = 225 + 400 = 625 = 25²: el triángulo es rectángulo, con área 15·20/2 = 150.",
  "Para cada lado, altura = 2·área/lado = 300/lado.",
  "La altura es más corta cuando el lado (la base) es más largo. El lado mayor es 25.",
  "Altura mínima = 300/25 = 12."],
 "El triángulo es rectángulo (15-20-25) con área 150. Cada altura vale 2·150/lado = 300/lado, mínima para el lado mayor: 300/25 = 12. Verificado con Python.",
 "Como el área es invariante, base y altura son inversamente proporcionales: la altura más corta cae sobre el lado más largo. Optimizar = elegir la base correcta.",
 14, ["área fija", "altura = 2A/base", "proporción inversa"],
 ["estabilidad estructural", "distribución de cargas", "diseño de soportes"],
 "", ["optimizacion", "altura", "triangulo", "nivel-intermedio"], "cap. 6 (Prob. 6.43, AMC 10)"))

A(P(391, "El vértice que sube en el círculo", "optimizacion", 4,
 "En el plano, A = (0,0) y B = (2,0). El vértice C de un triángulo ABC se mueve sobre la circunferencia de centro (3,2) y radio 1. ¿Cuál es el área máxima posible del triángulo ABC?",
 ["Toma AB como base fija; su longitud es 2 y está sobre el eje x. ¿De qué depende el área?",
  "Área = (1/2)·base·altura = (1/2)·2·(altura de C sobre el eje x) = (coordenada y de C).",
  "Así que maximizar el área es maximizar la coordenada y del punto C sobre el círculo.",
  "El centro está en y = 2 y el radio es 1, así que la mayor coordenada y posible es 2 + 1 = 3.",
  "Área máxima = (1/2)·2·3 = 3."],
 "Con base AB = 2 sobre el eje x, el área es (1/2)·2·y_C = y_C. La mayor altura es la mayor coordenada y de C en el círculo: 2 + 1 = 3. Área máxima = 3. Verificado con Python.",
 "El truco es elegir una base fija y reconocer que el área solo depende de la 'altura' del tercer vértice. Maximizar el área se reduce a empujar C lo más alto posible dentro de su restricción.",
 18, ["base fija", "altura = coordenada y", "punto óptimo en círculo"],
 ["optimización con restricciones", "programación geométrica", "robótica"],
 "", ["optimizacion", "area", "geometria-analitica", "nivel-avanzado"], "cap. 4 (Prob. 4.36, Mandelbrot)"))

A(P(392, "El reflejo acorta el camino", "optimizacion", 4,
 "Un punto A = (0,3) y un punto B = (8,5) están del mismo lado del eje x. Debes ir de A a un punto cualquiera del eje x y de ahí a B. ¿Cuál es la longitud del camino total más corto?",
 ["Truco del espejo: refleja uno de los puntos respecto del eje x para 'enderezar' el camino quebrado.",
  "Refleja A = (0,3) al otro lado del eje: A' = (0,−3). Cualquier camino A→(punto del eje)→B mide lo mismo que A'→(punto del eje)→B.",
  "El camino más corto de A' a B es la línea recta, que cruza el eje en el punto óptimo.",
  "Distancia A'B = √((8−0)² + (5−(−3))²) = √(64 + 64).",
  "= √128 = 8√2 ≈ 11.31."],
 "Reflejando A en el eje x a A' = (0,−3), el camino A→eje→B iguala A'→eje→B, cuyo mínimo es la recta A'B = √(8² + 8²) = √128 = 8√2. Verificado con Python.",
 "El principio de reflexión convierte un camino quebrado con restricción en una línea recta: es la base de la ley de reflexión de la luz y de los problemas de 'mínima distancia con rebote'.",
 18, ["principio de reflexión", "distancia mínima", "ley de reflexión"],
 ["óptica (espejos)", "diseño de tuberías", "trayectorias de billar"],
 "", ["optimizacion", "camino-minimo", "reflexion", "nivel-avanzado"], "cap. 16 (Reflections)"))

A(P(393, "El rectángulo dentro del triángulo", "optimizacion", 4,
 "Un triángulo rectángulo tiene catetos de longitud 6 y 8. Se inscribe un rectángulo con un vértice en el ángulo recto y dos lados sobre los catetos, y el vértice opuesto sobre la hipotenusa. ¿Cuál es el área máxima de ese rectángulo?",
 ["Coloca el ángulo recto en el origen y los catetos sobre los ejes. Si el rectángulo mide x por y, su vértice (x,y) está sobre la hipotenusa.",
  "La hipotenusa une (6,0) y (0,8); su ecuación cumple x/6 + y/8 = 1. Esa es la restricción.",
  "Área = x·y, sujeta a x/6 + y/8 = 1. Despeja y = 8(1 − x/6) y maximiza x·y.",
  "El producto de dos términos cuya suma (x/6 + y/8 = 1) es fija se maximiza cuando son iguales: x/6 = y/8 = 1/2.",
  "Entonces x = 3, y = 4 y área = 12 (la mitad del área del triángulo)."],
 "Con el ángulo recto en el origen y vértice (x,y) sobre la hipotenusa x/6 + y/8 = 1, el área x·y se maximiza cuando x/6 = y/8 = 1/2, o sea x = 3, y = 4: área = 12. (En general, ab/4 = 6·8/4.) Verificado con Python.",
 "El máximo rectángulo inscrito en un triángulo rectángulo ocupa exactamente la mitad de su área y tiene como vértices los puntos medios de los catetos. AM-GM cierra la optimización.",
 20, ["rectángulo inscrito", "AM-GM", "ecuación de la hipotenusa"],
 ["aprovechamiento de material", "diseño de paneles", "corte óptimo"],
 "", ["optimizacion", "area", "rectangulo-inscrito", "nivel-avanzado"], "cap. 4/16 (optimización de área)"))

A(P(394, "El triángulo más amplio con un perímetro dado", "optimizacion", 3,
 "Entre todos los triángulos cuyo perímetro es 30, ¿cuál tiene la mayor área y cuánto vale esa área?",
 ["Intuye la forma 'más redonda': de todos los triángulos con perímetro fijo, ¿cuál crees que abarca más área?",
  "El más simétrico, el equilátero, maximiza el área a perímetro fijo (consecuencia de AM-GM sobre la fórmula de Herón).",
  "Perímetro 30 ⇒ lado = 10 para el equilátero.",
  "Área de un equilátero de lado s es s²√3/4.",
  "= 10²√3/4 = 25√3 ≈ 43.3."],
 "El triángulo de área máxima con perímetro fijo es el equilátero. Con perímetro 30, el lado es 10 y el área es 10²√3/4 = 25√3 ≈ 43.3. Verificado con Python.",
 "Versión triangular del problema isoperimétrico: a perímetro fijo, la máxima simetría (equilátero) da máxima área. Se prueba aplicando AM-GM a la fórmula de Herón.",
 14, ["isoperimétrico", "equilátero óptimo", "fórmula de Herón"],
 ["diseño eficiente de estructuras", "biología (formas óptimas)", "empaquetamiento"],
 "", ["optimizacion", "area", "equilatero", "nivel-intermedio"], "cap. 4/6 (isoperimétrico)"))

A(P(395, "El rectángulo de diagonal fija", "optimizacion", 3,
 "Entre todos los rectángulos cuya diagonal mide 10, ¿cuál tiene el área máxima y cuánto vale?",
 ["La diagonal fija liga los lados por Pitágoras: l² + w² = 10² = 100. Eso es una suma fija… de cuadrados.",
  "Quieres maximizar el área l·w sujeta a l² + w² = 100.",
  "Por AM-GM, l·w ≤ (l² + w²)/2 = 100/2 = 50, con igualdad cuando l = w.",
  "l = w significa un cuadrado; su lado cumple 2l² = 100 ⇒ l = √50.",
  "Área máxima = 50 (el cuadrado de diagonal 10)."],
 "Con l² + w² = 100, por AM-GM l·w ≤ (l² + w²)/2 = 50, con igualdad si l = w (cuadrado de lado √50). Área máxima = 50. Verificado con Python.",
 "Aquí AM-GM se aplica a los cuadrados de los lados: a diagonal fija, el cuadrado maximiza el área. Variantes del mismo principio según qué cantidad esté fija.",
 14, ["AM-GM con cuadrados", "diagonal fija", "cuadrado óptimo"],
 ["diseño de pantallas", "optimización con restricción cuadrática", "señales"],
 "", ["optimizacion", "area", "rectangulo", "nivel-intermedio"], "cap. 6 (Pitágoras + AM-GM)"))

A(P(396, "El triángulo del semicírculo", "optimizacion", 3,
 "Sobre el diámetro de un semicírculo de radio 5 se apoya la base de un triángulo, y su tercer vértice está sobre el arco. ¿Cuál es el área máxima posible de ese triángulo?",
 ["La base es el diámetro, fijo. ¿De qué depende entonces el área?",
  "Base = diámetro = 2·5 = 10. Área = (1/2)·10·altura, así que solo hay que maximizar la altura.",
  "La altura es la distancia del tercer vértice (sobre el arco) al diámetro.",
  "Esa distancia es máxima en el punto más alto del arco: una altura igual al radio, 5.",
  "Área máxima = (1/2)·10·5 = 25."],
 "La base (diámetro) mide 10 y es fija; el área = (1/2)·10·altura crece con la altura, máxima en la cima del arco donde vale el radio 5. Área máxima = (1/2)·10·5 = 25 = r². Verificado con Python.",
 "Con la base fijada como diámetro, optimizar el área es elevar el vértice lo más posible: el punto más alto del arco. El triángulo óptimo resulta ser rectángulo isósceles (ángulo recto inscrito en el semicírculo).",
 14, ["base fija", "altura máxima = radio", "ángulo inscrito en semicírculo"],
 ["diseño de arcos", "puentes", "antenas parabólicas"],
 "", ["optimizacion", "area", "circulo", "nivel-intermedio"], "cap. 11/12 (semicírculo)"))

A(P(397, "La distancia más corta a la recta", "optimizacion", 2,
 "¿Cuál es la distancia más corta entre el origen (0,0) y la recta de ecuación 3x + 4y = 25?",
 ["Entre todos los segmentos del origen a la recta, ¿cuál es el más corto? Piensa en perpendicularidad.",
  "La distancia mínima de un punto a una recta se mide por el segmento PERPENDICULAR a la recta.",
  "Hay una fórmula: distancia = |3·x₀ + 4·y₀ − 25| / √(3² + 4²) para el punto (x₀,y₀).",
  "Sustituye el origen: |3·0 + 4·0 − 25| / √(9 + 16) = 25/√25.",
  "= 25/5 = 5."],
 "La distancia mínima es la perpendicular: |3·0 + 4·0 − 25|/√(3²+4²) = 25/5 = 5. Verificado con Python.",
 "De todos los caminos de un punto a una recta, el perpendicular es el más corto. La fórmula de distancia punto-recta empaqueta esa optimización en una sola expresión.",
 10, ["distancia punto-recta", "perpendicular = mínima", "geometría analítica"],
 ["control de colisiones", "ajuste de mínimos cuadrados", "navegación"],
 "", ["optimizacion", "distancia", "geometria-analitica", "nivel-basico"], "cap. 17.5 (Distance Point-Line)"))

# =====================================================================
# INVERSION (11) — trabajar hacia atrás desde área/perímetro a dimensiones
# =====================================================================

A(P(398, "Del área al perímetro del cuadrado", "inversion", 2,
 "Un cuadrado tiene área 75. ¿Cuál es su perímetro?",
 ["No tienes el lado, pero el área te lleva a él hacia atrás. ¿Qué operación deshace 'elevar al cuadrado'?",
  "Área = lado² ⇒ lado = √75.",
  "Simplifica el radical: √75 = √(25·3) = 5√3.",
  "Perímetro = 4·lado.",
  "= 4·5√3 = 20√3 ≈ 34.64."],
 "lado = √75 = 5√3; perímetro = 4·5√3 = 20√3 ≈ 34.64. Verificado con Python.",
 "Trabajar hacia atrás: del área se recupera el lado con una raíz, y del lado el perímetro. Simplificar √75 = 5√3 deja la respuesta exacta y limpia.",
 10, ["raíz cuadrada", "simplificar radicales", "trabajar hacia atrás"],
 ["dimensionar a partir de superficie", "escalado de planos", "estimación"],
 "", ["cuadrado", "perimetro", "inversion", "nivel-basico"], "cap. 4 (Prob. 4.15)"))

A(P(399, "Reconstruir el rectángulo", "inversion", 3,
 "El largo de un rectángulo es 2 menos que 4 veces su ancho. Su perímetro es 51. ¿Cuál es su área?",
 ["Da nombre al ancho y traduce la frase hacia atrás: ¿cómo se escribe el largo en términos del ancho?",
  "Sea w el ancho; entonces el largo es l = 4w − 2.",
  "Perímetro: 2(l + w) = 51 ⇒ 2((4w − 2) + w) = 51.",
  "2(5w − 2) = 51 ⇒ 10w − 4 = 51 ⇒ w = 5.5; luego l = 4·5.5 − 2 = 20.",
  "Área = l·w = 20·5.5 = 110."],
 "Con l = 4w − 2 y 2(l + w) = 51: 10w − 4 = 51 ⇒ w = 5.5, l = 20. Área = 20·5.5 = 110. Verificado con Python.",
 "Del dato final (perímetro) se retrocede, vía una ecuación lineal, hasta las dimensiones, y con ellas el área. Nombrar la incógnita correcta (el ancho) hace que todo lo demás se exprese fácil.",
 14, ["traducir enunciados", "ecuación lineal", "trabajar hacia atrás"],
 ["dimensionar terrenos", "presupuesto de materiales", "planeación de espacios"],
 "", ["rectangulo", "area", "inversion", "nivel-intermedio"], "cap. 4 (Prob. 4.17)"))

A(P(400, "Perímetro y área conocidos", "inversion", 3,
 "Un rectángulo tiene perímetro 28 cm y área 48 cm². ¿Cuáles son sus dimensiones?",
 ["Tienes la suma (del perímetro) y el producto (del área) de los dos lados: busca dos números desde sus suma y producto.",
  "Perímetro 28 ⇒ l + w = 14. Área 48 ⇒ l·w = 48.",
  "Busca dos números que sumen 14 y multipliquen 48 (o resuelve x² − 14x + 48 = 0).",
  "x² − 14x + 48 = (x − 6)(x − 8) = 0.",
  "Las dimensiones son 6 cm y 8 cm."],
 "l + w = 14 y l·w = 48 ⇒ x² − 14x + 48 = 0 ⇒ (x−6)(x−8) = 0. Dimensiones 6 cm y 8 cm. Verificado con Python.",
 "Conocer suma y producto es conocer una ecuación cuadrática (Vieta al revés): las dimensiones son sus raíces. Es trabajar hacia atrás desde dos cantidades agregadas a los valores individuales.",
 14, ["suma y producto", "ecuación cuadrática", "fórmulas de Vieta"],
 ["reconstrucción de datos", "ingeniería inversa", "diseño con restricciones"],
 "", ["rectangulo", "dimensiones", "inversion", "nivel-intermedio"], "cap. 4 (Prob. 4.20)"))

A(P(401, "El perímetro del isósceles", "inversion", 3,
 "Un triángulo isósceles tiene base de longitud 10 y área 60. ¿Cuál es su perímetro?",
 ["Del área retrocede a la altura sobre la base; luego usa que la altura de un isósceles cae en el punto medio de la base.",
  "Área = base·altura/2 ⇒ 60 = 10·h/2 ⇒ h = 12.",
  "La altura llega al punto medio de la base, partiéndola en dos mitades de 5.",
  "Cada lado igual es la hipotenusa de un triángulo rectángulo con catetos 5 y 12.",
  "Lado = √(5² + 12²) = 13 (terna 5-12-13). Perímetro = 10 + 13 + 13 = 36."],
 "h = 2·60/10 = 12. Cada lado igual = √(5² + 12²) = 13. Perímetro = 10 + 2·13 = 36. Verificado con Python.",
 "Se trabaja hacia atrás (área → altura) y luego hacia adelante con la simetría del isósceles y Pitágoras (aquí, la terna 5-12-13). Combinar inversión con un patrón conocido acelera el cierre.",
 14, ["área → altura", "simetría del isósceles", "terna 5-12-13"],
 ["agrimensura", "diseño de techumbres", "cálculo de longitudes inaccesibles"],
 "", ["triangulo", "perimetro", "inversion", "nivel-intermedio"], "cap. 6 (Prob. 6.33)"))

A(P(402, "Del área e hipotenusa al perímetro", "inversion", 4,
 "Un triángulo rectángulo tiene área 210 e hipotenusa 29. ¿Cuál es su perímetro?",
 ["Llama a los catetos a y b. Traduce los dos datos a ecuaciones sobre a y b.",
  "Área 210 ⇒ ab/2 = 210 ⇒ ab = 420. Hipotenusa ⇒ a² + b² = 29² = 841.",
  "Quieres a + b. Recuerda que (a + b)² = a² + b² + 2ab.",
  "(a + b)² = 841 + 2·420 = 841 + 840 = 1681.",
  "a + b = √1681 = 41; perímetro = (a + b) + hipotenusa = 41 + 29 = 70."],
 "ab = 420 y a² + b² = 841. (a + b)² = 841 + 840 = 1681 ⇒ a + b = 41. Perímetro = 41 + 29 = 70. Verificado con Python.",
 "El truco algebraico (a + b)² = a² + b² + 2ab evita resolver para a y b por separado: con la suma de cuadrados y el producto basta. Es inversión apoyada en una identidad.",
 18, ["identidad (a+b)²", "área e hipotenusa", "no resolver por separado"],
 ["reconstrucción de parámetros", "álgebra simbólica", "ingeniería"],
 "", ["triangulo-rectangulo", "perimetro", "inversion", "nivel-avanzado"], "cap. 6 (Prob. 6.44)"))

A(P(403, "Hipotenusa 8, área 8", "inversion", 4,
 "Un triángulo rectángulo tiene hipotenusa de longitud 8 y área 8. ¿Cuál es su perímetro?",
 ["De nuevo nombra los catetos a, b y escribe las dos condiciones.",
  "Área 8 ⇒ ab = 16. Hipotenusa ⇒ a² + b² = 64.",
  "Usa (a + b)² = a² + b² + 2ab para obtener a + b sin hallar a y b.",
  "(a + b)² = 64 + 2·16 = 96 ⇒ a + b = √96 = 4√6.",
  "Perímetro = (a + b) + 8 = 4√6 + 8 ≈ 17.80."],
 "ab = 16 y a² + b² = 64 ⇒ (a + b)² = 64 + 32 = 96 ⇒ a + b = 4√6. Perímetro = 4√6 + 8 ≈ 17.80. Verificado con Python.",
 "Mismo método que el problema anterior, pero ahora la respuesta es irracional: el truco (a + b)² sigue funcionando y entrega la suma de catetos sin necesidad de los valores individuales.",
 18, ["identidad (a+b)²", "respuesta irracional", "inversión algebraica"],
 ["modelado con restricciones", "diseño paramétrico", "álgebra aplicada"],
 "", ["triangulo-rectangulo", "perimetro", "inversion", "nivel-avanzado"], "cap. 6 (Prob. 6.47)"))

A(P(404, "La escalera que resbala", "inversion", 5,
 "Una escalera de 50 pies se apoya en una pared vertical. Resbala hasta que su punto de contacto con la pared baja 8 pies, mientras la base se aleja 16 pies de su posición original. Tras el deslizamiento, ¿a qué altura del suelo queda el extremo superior de la escalera?",
 ["Llama x a la distancia inicial de la base a la pared, y a la altura inicial. Plantea Pitágoras antes y después; la escalera mide 50 en ambos casos.",
  "Antes: x² + y² = 50² = 2500. Después: (x + 16)² + (y − 8)² = 2500 (misma escalera).",
  "Resta o desarrolla la segunda y usa x² + y² = 2500 para simplificar: 32x − 16y + 320 = 0, o sea y = 2x + 20.",
  "Sustituye en x² + y² = 2500: x² + (2x + 20)² = 2500 ⇒ 5x² + 80x − 2100 = 0 ⇒ x² + 16x − 420 = 0 ⇒ x = 14.",
  "Entonces y = 2·14 + 20 = 48 y la nueva altura es y − 8 = 40 pies."],
 "Sea x la base inicial, y la altura inicial: x² + y² = 2500 y (x+16)² + (y−8)² = 2500. Restando y simplificando: y = 2x + 20; sustituyendo, x = 14, y = 48. Nueva altura = 48 − 8 = 40 pies. Verificado: 14²+48² = 30²+40² = 2500.",
 "Modelar 'antes y después' con la misma longitud de escalera da dos ecuaciones; restarlas elimina los términos cuadráticos y deja una relación lineal. La terna 30-40-50 emerge al final.",
 26, ["Pitágoras antes/después", "restar ecuaciones", "terna 30-40-50"],
 ["cinemática", "modelado de movimiento", "problemas de tasas relacionadas"],
 "", ["escalera", "pitagoras", "inversion", "nivel-avanzado"], "cap. 6 (Prob. 6.52)"))

A(P(405, "Del área del equilátero a su lado", "inversion", 2,
 "Un triángulo equilátero tiene área 9√3. ¿Cuánto mide su lado?",
 ["Recuerda la fórmula del área de un equilátero en función del lado y úsala al revés.",
  "Área = s²√3/4. Iguala: s²√3/4 = 9√3.",
  "Divide ambos lados entre √3: s²/4 = 9.",
  "s² = 36.",
  "s = 6."],
 "s²√3/4 = 9√3 ⇒ s²/4 = 9 ⇒ s² = 36 ⇒ s = 6. Verificado con Python.",
 "Inversión directa de la fórmula s²√3/4: el factor √3 se cancela limpiamente, dejando una raíz sencilla. Conocer la fórmula de área del equilátero abre el camino de ida y de vuelta.",
 10, ["área del equilátero", "despejar el lado", "trabajar hacia atrás"],
 ["dimensionar piezas triangulares", "diseño modular", "estimación inversa"],
 "", ["equilatero", "lado", "inversion", "nivel-basico"], "cap. 6 (área del equilátero, inversa)"))

A(P(406, "Del área del círculo a su contorno", "inversion", 2,
 "Un círculo tiene área 49π. ¿Cuál es su circunferencia (perímetro)?",
 ["Del área retrocede al radio; luego pasa del radio a la circunferencia.",
  "Área = πr² = 49π ⇒ r² = 49.",
  "r = 7.",
  "Circunferencia = 2πr.",
  "= 2π·7 = 14π ≈ 43.98."],
 "πr² = 49π ⇒ r² = 49 ⇒ r = 7. Circunferencia = 2πr = 14π. Verificado con Python.",
 "El radio es el 'puente' entre área (πr²) y circunferencia (2πr): conocido uno, se recupera el radio y se llega al otro. Trabajar hacia atrás en dos pasos cortos.",
 8, ["área del círculo", "radio puente", "circunferencia"],
 ["diseño de tuberías", "ruedas y engranajes", "estimación de materiales"],
 "", ["circulo", "circunferencia", "inversion", "nivel-basico"], "cap. 11 (Arc Length & Circumference)"))

A(P(407, "El cateto que falta", "inversion", 1,
 "En un triángulo rectángulo, la hipotenusa mide 25 y uno de los catetos mide 7. ¿Cuánto mide el otro cateto?",
 ["Pitágoras también funciona al revés: si conoces la hipotenusa y un cateto, despeja el otro.",
  "a² + b² = c² con c = 25 (hipotenusa) y un cateto = 7.",
  "El cateto faltante cumple b² = 25² − 7².",
  "b² = 625 − 49 = 576.",
  "b = √576 = 24 (es la terna 7-24-25)."],
 "b² = 25² − 7² = 625 − 49 = 576 ⇒ b = 24. (Es la terna pitagórica 7-24-25.) Verificado con Python.",
 "El teorema de Pitágoras se usa hacia atrás restando, no sumando: hipotenusa² − cateto² = el otro cateto². Reconocer la terna 7-24-25 confirma el resultado al instante.",
 8, ["Pitágoras inverso", "terna 7-24-25", "despejar cateto"],
 ["medición indirecta", "verificación de escuadras", "topografía"],
 "", ["pitagoras", "cateto", "inversion", "nivel-basico"], "cap. 6 (Prob. 6.26, inversa)"))

A(P(408, "Las diagonales del rombo", "inversion", 2,
 "Un rombo tiene área 24 y una de sus diagonales mide 6. ¿Cuánto mide la otra diagonal?",
 ["Recuerda cómo se calcula el área de un rombo a partir de sus dos diagonales y úsalo al revés.",
  "Área de un rombo = (d₁·d₂)/2, el semiproducto de sus diagonales.",
  "Sustituye lo conocido: 24 = (6·d₂)/2.",
  "6·d₂ = 48.",
  "d₂ = 48/6 = 8."],
 "Área = d₁·d₂/2 ⇒ 24 = 6·d₂/2 ⇒ d₂ = 8. Verificado con Python.",
 "La fórmula del rombo (semiproducto de diagonales) se invierte como cualquier otra: conocida el área y una diagonal, se despeja la segunda. Vale igual para cualquier cuadrilátero de diagonales perpendiculares.",
 10, ["área del rombo", "diagonales perpendiculares", "despeje"],
 ["diseño de cometas", "patrones de mosaico", "cálculo de superficies"],
 "", ["rombo", "diagonales", "inversion", "nivel-basico"], "cap. 8.4 (Rhombi)"))

# =====================================================================
# Validación de balance y append idempotente
# =====================================================================
assert len(PROBLEMS) == 44, len(PROBLEMS)
bal = collections.Counter(p["estrategia"] for p in PROBLEMS)
assert bal["inversion"] == bal["optimizacion"] == bal["invariantes"] == bal["patrones"] == 11, bal
ids = [p["id"] for p in PROBLEMS]
assert ids == list(range(365, 409)), ids
assert len(set(ids)) == 44

PATH = "data/problems.json"
data = json.load(open(PATH, encoding="utf-8"))
existing = {p["id"] for p in data["problemas"]}
clash = existing & set(ids)
assert not clash, ("choque de ids", clash)

data["problemas"].extend(PROBLEMS)
gbal = collections.Counter(p["estrategia"] for p in data["problemas"])
print("balance global tras append:", dict(gbal))
assert all(v == 102 for v in gbal.values()), gbal

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: añadidos {len(PROBLEMS)} problemas (ids {ids[0]}-{ids[-1]}). Total = {len(data['problemas'])}.")
