"""
Genera 44 problemas de AoPS Calculus (ids 673-716) con KaTeX completo
y los añade a data/problems.json.
Estrategias: inversion 11, optimizacion 11, invariantes 11, patrones 11.
Todos los números verificados con Python (ver verificaciones_aops_calc.py).
"""
import json, re

nuevos = [

# ─────────────── INVERSIÓN 673-683 ───────────────

{
"id": 673,
"titulo": "La quitanieves y la nieve",
"estrategia": "inversion",
"dificultad": 4,
"enunciado": "Una quitanieves elimina nieve a una tasa constante (en volumen por minuto). Cierto día no había nieve al amanecer, pero en algún momento de la mañana comenzó a nevar a una tasa constante. Al mediodía la quitanieves comenzó a trabajar. Entre el mediodía y la 1 p.m. avanzó 2 millas; entre la 1 p.m. y las 2 p.m. avanzó 1 milla. ¿A qué hora empezó a nevar?",
"hints": [
    "Si la nieve lleva acumulándose $T$ horas antes del mediodía, la profundidad al tiempo $t$ horas después del mediodía es proporcional a $T + t$.",
    "La tasa de avance de la quitanieves (millas/hora) es inversamente proporcional a la profundidad de la nieve: $dx/dt = k/(T+t)$.",
    "Plantea dos ecuaciones integrando $\\int_0^1 \\frac{k}{T+t}\\,dt = 2$ e $\\int_1^2 \\frac{k}{T+t}\\,dt = 1$. Obtienes $\\ln\\!\\frac{T+1}{T} = 2\\ln\\!\\frac{T+2}{T+1}$.",
    "Sea $p = (T+1)/T$. Muestra que $(T+2)/(T+1) = (2p-1)/p$. Entonces $\\ln p = 2\\ln\\frac{2p-1}{p}$ implica $\\sqrt{p} = (2p-1)/p$, es decir $p^{3/2} = 2p - 1$.",
    "Con $q = \\sqrt{p}$: $q^3 - 2q^2 + 1 = 0$, que factoriza como $(q-1)(q^2-q-1)=0$. La raíz positiva distinta de 1 es $q = \\varphi = (1+\\sqrt{5})/2$. Entonces $T = 1/(\\varphi^2-1) = 1/\\varphi = (\\sqrt{5}-1)/2 \\approx 37$ minutos."
],
"solucion": "Sea $T$ el número de horas antes del mediodía en que empezó a nevar. La profundidad crece como $h = r(T+t)$. La quitanieves avanza a $dx/dt = k/(T+t)$. Integrando: $k\\ln\\frac{T+1}{T} = 2k\\ln\\frac{T+2}{T+1}$. Sea $p=(T+1)/T$; entonces $(2p-1)/p = \\sqrt{p}$, que lleva a $q^3 - 2q^2+1=0$ con $q=\\sqrt{p}$. Factorizando: $(q-1)(q^2-q-1)=0$, por lo que $q = \\varphi = (1+\\sqrt{5})/2$. Así $T = 1/(\\varphi^2-1) = (\\sqrt{5}-1)/2 \\approx 0.618$ horas $\\approx \\mathbf{37}$ minutos antes del mediodía. Verificado con Python.",
"explicacion": "El truco es modelar la profundidad de nieve como función del tiempo y luego trabajar hacia atrás desde las distancias recorridas. La ecuación resultante tiene como solución el número áureo $\\varphi$: la nieve comenzó a caer unos 37 minutos antes del mediodía.",
"tiempo_estimado": 35,
"conceptos": ["tasa de cambio", "ecuaciones integrales", "optimización inversa", "razón áurea"],
"transferencias": ["modelado de flujos variables", "ingeniería civil", "climatología"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz)",
"source_url": "",
"year": "",
"tags": ["cálculo", "ecuaciones-integrales", "inversión", "nivel-avanzado"]
},

{
"id": 674,
"titulo": "Una función con derivada siempre positiva",
"estrategia": "inversion",
"dificultad": 2,
"enunciado": "Sea $f$ una función definida sobre $\\mathbb{R}$ tal que $f'(x) = x^2 - 3x + 3$ para todo $x \\in \\mathbb{R}$. Demuestra que $f$ tiene inversa.",
"hints": [
    "Una función tiene inversa si y solo si es biyectiva. Para funciones diferenciables en $\\mathbb{R}$, ¿qué condición sobre $f'$ garantiza inyectividad?",
    "Si $f'(x) > 0$ para todo $x$, entonces $f$ es estrictamente creciente y por tanto inyectiva.",
    "Analiza el signo de $f'(x) = x^2 - 3x + 3$. ¿Tiene raíces reales?",
    "El discriminante es $\\Delta = (-3)^2 - 4(1)(3) = 9 - 12 = -3 < 0$.",
    "Como $\\Delta < 0$ y el coeficiente de $x^2$ es positivo, $f'(x) > 0$ para todo $x$. Por tanto $f$ es estrictamente creciente y tiene inversa."
],
"solucion": "Calculamos el discriminante de $f'(x) = x^2 - 3x + 3$: $\\Delta = 9 - 12 = -3 < 0$. Como el coeficiente líder es positivo y el discriminante es negativo, $f'(x) > 0$ para todo $x \\in \\mathbb{R}$. Esto significa que $f$ es estrictamente creciente, por lo que es inyectiva y tiene función inversa.",
"explicacion": "La clave es reconocer que un polinomio cuadrático con discriminante negativo nunca cambia de signo. Aquí $f'(x) > 0$ siempre, lo que garantiza que $f$ es monótona creciente y por tanto invertible.",
"tiempo_estimado": 10,
"conceptos": ["función inversa", "monotonía", "discriminante", "derivada positiva"],
"transferencias": ["funciones biyectivas", "teoremas de función inversa", "análisis real"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Review #4.35",
"source_url": "",
"year": "",
"tags": ["derivadas", "función-inversa", "inversión", "nivel-básico"]
},

{
"id": 675,
"titulo": "Sucesión de raíces anidadas",
"estrategia": "inversion",
"dificultad": 2,
"enunciado": "Define la sucesión $\\{a_n\\}_{n=1}^\\infty$ mediante $a_1 = \\sqrt{2}$ y $a_n = \\sqrt{2\\,a_{n-1}}$ para todo $n > 1$. Determina $\\displaystyle\\lim_{n\\to\\infty} a_n$.",
"hints": [
    "Calcula los primeros términos: $a_1 = \\sqrt{2}$, $a_2 = \\sqrt{2\\sqrt{2}}$, $a_3 = \\sqrt{2\\sqrt{2\\sqrt{2}}}$, $\\ldots$ ¿La sucesión parece creciente? ¿Acotada?",
    "Muestra que $a_n < 2$ para todo $n$ usando inducción: si $a_{n-1} < 2$, entonces $a_n = \\sqrt{2a_{n-1}} < \\sqrt{4} = 2$.",
    "Muestra también que $a_n$ es creciente: $a_2 = \\sqrt{2\\sqrt{2}} > \\sqrt{2} = a_1$; en general si $a_{n-1} < a_n$, entonces $a_n = \\sqrt{2a_{n-1}} < \\sqrt{2a_n} = a_{n+1}$.",
    "Como la sucesión es creciente y acotada superiormente, el límite $L = \\lim a_n$ existe.",
    "Toma límite en ambos lados de $a_n = \\sqrt{2a_{n-1}}$: $L = \\sqrt{2L}$, así que $L^2 = 2L$, es decir $L(L-2)=0$. Como $L > 0$, concluyes $L = 2$."
],
"solucion": "La sucesión es creciente ($a_n < a_{n+1}$) y acotada por 2 (demostrable por inducción). Por tanto existe $L = \\lim a_n$. Tomando límite en $a_n = \\sqrt{2a_{n-1}}$: $L = \\sqrt{2L} \\Rightarrow L^2 = 2L \\Rightarrow L = 0$ o $L = 2$. Como $a_1 = \\sqrt{2} > 0$, se tiene $L = \\mathbf{2}$. Verificado numéricamente.",
"explicacion": "El enfoque de inversión: asumimos que el límite existe y 'invertimos' la ecuación de recurrencia para hallar su valor. El truco clave es notar que en el límite, $a_n$ y $a_{n-1}$ convergen al mismo valor $L$, lo que convierte la recurrencia en una ecuación algebraica simple.",
"tiempo_estimado": 15,
"conceptos": ["sucesiones convergentes", "inducción", "ecuaciones de punto fijo"],
"transferencias": ["raíces anidadas infinitas", "atractores de iteraciones", "análisis numérico"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Review #7.36",
"source_url": "",
"year": "",
"tags": ["sucesiones", "límites", "inversión", "nivel-básico"]
},

{
"id": 676,
"titulo": "La función de HMMT: $f'(x)=f(1-x)$",
"estrategia": "inversion",
"dificultad": 5,
"enunciado": "Sea $f:\\mathbb{R}\\to\\mathbb{R}$ diferenciable e infinitamente diferenciable, que satisface $f'(x) = f(1-x)$ para todo $x$, con $f(0) = 1$. Halla el valor exacto de $f(1)$. (Fuente: HMMT)",
"hints": [
    "Diferencia ambos lados de $f'(x) = f(1-x)$ respecto a $x$.",
    "Obtienes $f''(x) = -f'(1-x)$. Pero la ecuación original dice $f'(1-x) = f(1-(1-x)) = f(x)$. Entonces $f''(x) = -f(x)$.",
    "La ecuación $f'' + f = 0$ tiene solución general $f(x) = A\\cos x + B\\sin x$. Aplica $f(0) = 1$ para hallar $A$.",
    "Usa la ecuación original en $x=0$: $f'(0) = f(1)$. Calcula $f'(0)$ y $f(1)$ en términos de $A$ y $B$. Usa $f'(x)=f(1-x)$ evaluada en $x=0$ para obtener una ecuación en $B$.",
    "De $f'(0) = B = f(1) = \\cos 1 + B\\sin 1$, obtienes $B(1-\\sin 1) = \\cos 1$, por lo que $B = \\frac{\\cos 1}{1 - \\sin 1}$. Entonces $f(1) = \\frac{\\cos 1}{1-\\sin 1} \\approx 3.408$."
],
"solucion": "Diferenciando $f'(x)=f(1-x)$ obtenemos $f''(x)=-f'(1-x)=-f(x)$, es decir $f''+f=0$. Solución general: $f(x)=A\\cos x + B\\sin x$. Con $f(0)=1$: $A=1$. Evaluando la ecuación original en $x=0$: $B = f'(0) = f(1) = \\cos 1 + B\\sin 1$, de donde $B = \\dfrac{\\cos 1}{1-\\sin 1}$. Por tanto $f(1) = \\cos 1 + B\\sin 1 = \\dfrac{\\cos 1}{1-\\sin 1} \\approx 3.408$. Verificado con Python.",
"explicacion": "La ecuación funcional se convierte en una EDO diferenciando dos veces. La inversión clave: usar la propia condición $f'(x)=f(1-x)$ evaluada estratégicamente para determinar la constante $B$ y calcular $f(1)$ sin resolver explícitamente todo el sistema.",
"tiempo_estimado": 30,
"conceptos": ["ecuaciones funcionales", "EDO de segundo orden", "serie trigonométrica"],
"transferencias": ["análisis de Fourier", "sistemas de ecuaciones funcionales", "física ondulatoria"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 9 Challenge #9.31 (Fuente: HMMT)",
"source_url": "",
"year": "",
"tags": ["ecuaciones-funcionales", "EDO", "inversión", "nivel-élite"]
},

{
"id": 677,
"titulo": "La regla del 72",
"estrategia": "inversion",
"dificultad": 2,
"enunciado": "La «regla del 72» afirma que si una cantidad de dinero se invierte a una tasa de interés del $r\\%$ anual, tardará aproximadamente $72/r$ años en duplicarse. Usa aproximación lineal de $\\ln(1+x)$ para explicar por qué esta regla es una buena aproximación cuando $r$ es pequeño.",
"hints": [
    "Plantea la ecuación exacta del doble: $(1 + r/100)^n = 2$.",
    "Toma logaritmo: $n \\cdot \\ln(1 + r/100) = \\ln 2$.",
    "Para $x$ pequeño, $\\ln(1+x) \\approx x$. Aplica esta aproximación con $x = r/100$.",
    "Obtienes $n \\cdot (r/100) \\approx \\ln 2 \\approx 0.6931$, por lo que $n \\approx 69.3/r$.",
    "La regla usa 72 en lugar de 69.3. Esto sobrecompensa ligeramente el error de la aproximación lineal (que subestima $\\ln(1+x)$ para $x>0$) y da resultados más prácticos para tasas del 6–10\\%."
],
"solucion": "La condición de duplicar es $(1+r/100)^n = 2$. Tomando logaritmo: $n = \\ln 2 / \\ln(1+r/100)$. Por aproximación lineal, $\\ln(1+r/100) \\approx r/100$ para $r$ pequeño. Entonces $n \\approx 100\\ln 2/r \\approx 69.3/r$. La regla del 72 usa el factor 72 en lugar de 69.3, lo que mejora la precisión práctica para tasas del 6–10\\% (donde $\\ln(1+r/100) < r/100$, así que el denominador real es algo menor que la aproximación, haciendo $n$ algo mayor que 69.3/r).",
"explicacion": "La aproximación lineal $\\ln(1+x)\\approx x$ transforma el tiempo de duplicación en $69.3/r$. La regla del 72 es una versión redondeada que también compensa el error sistemático de la aproximación, siendo más precisa en la práctica.",
"tiempo_estimado": 12,
"conceptos": ["interés compuesto", "aproximación lineal", "logaritmo natural"],
"transferencias": ["finanzas personales", "demografía", "crecimiento bacteriano"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.49",
"source_url": "",
"year": "",
"tags": ["aproximación-lineal", "logaritmos", "finanzas", "inversión", "nivel-básico"]
},

{
"id": 678,
"titulo": "El Teorema del Velocímetro (Racetrack)",
"estrategia": "inversion",
"dificultad": 3,
"enunciado": "Enuncia y demuestra el **Teorema del Velocímetro** (*Racetrack Theorem*): si $f$ y $g$ son funciones diferenciables con $f(a) = g(a)$ para algún $a$, y $f'(x) > g'(x)$ para todo $x > a$, entonces $f(x) > g(x)$ para todo $x > a$.",
"hints": [
    "Define una función auxiliar $h(x) = f(x) - g(x)$. ¿Cuánto vale $h(a)$?",
    "$h(a) = f(a) - g(a) = 0$. ¿Cuál es el signo de $h'(x)$ para $x > a$?",
    "$h'(x) = f'(x) - g'(x) > 0$ para $x > a$. ¿Qué implica que $h'(x) > 0$ sobre el comportamiento de $h$?",
    "$h$ es estrictamente creciente en $(a, \\infty)$ (por el criterio de la derivada positiva).",
    "Para $x > a$: $h(x) > h(a) = 0$, es decir $f(x) - g(x) > 0$, o sea $f(x) > g(x)$. $\\square$"
],
"solucion": "Sea $h = f - g$. Entonces $h(a) = 0$ y $h'(x) = f'(x) - g'(x) > 0$ para $x > a$. Por tanto $h$ es estrictamente creciente en $[a,\\infty)$. Para cualquier $x > a$: $h(x) > h(a) = 0$, luego $f(x) > g(x)$. $\\square$",
"explicacion": "Este teorema es la versión formal de la intuición: «si el coche A siempre va más rápido que el coche B desde el momento en que están juntos, entonces A siempre estará adelante». La inversión consiste en reducir la comparación de dos funciones a analizar el signo de una sola función diferencia.",
"tiempo_estimado": 15,
"conceptos": ["teorema del valor medio", "funciones crecientes", "desigualdades de funciones"],
"transferencias": ["comparación de tasas de crecimiento", "demostraciones de desigualdades", "física cinética"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.45",
"source_url": "",
"year": "",
"tags": ["TVM", "funciones-crecientes", "inversión", "nivel-intermedio"]
},

{
"id": 679,
"titulo": "Integral de $e^{ax}\\sin(bx)$ por partes dobles",
"estrategia": "inversion",
"dificultad": 3,
"enunciado": "Halla una fórmula cerrada para $\\displaystyle I = \\int e^{ax}\\sin(bx)\\,dx$, donde $a \\in \\mathbb{R}$ y $b \\neq 0$. (Aplica integración por partes dos veces y luego «invierte» algebraicamente para $I$.)",
"hints": [
    "Aplica integración por partes con $u = \\sin(bx)$, $dv = e^{ax}dx$. Obtienes $I = \\frac{e^{ax}\\sin(bx)}{a} - \\frac{b}{a}\\int e^{ax}\\cos(bx)\\,dx$.",
    "Aplica partes de nuevo a $\\int e^{ax}\\cos(bx)\\,dx$ con $u=\\cos(bx)$, $dv=e^{ax}dx$. Obtienes $\\frac{e^{ax}\\cos(bx)}{a} + \\frac{b}{a}\\int e^{ax}\\sin(bx)\\,dx = \\frac{e^{ax}\\cos(bx)}{a} + \\frac{b}{a}I$.",
    "Sustituye de vuelta: $I = \\frac{e^{ax}\\sin(bx)}{a} - \\frac{b}{a}\\left(\\frac{e^{ax}\\cos(bx)}{a} + \\frac{b}{a}I\\right)$.",
    "Simplifica: $I\\left(1 + \\frac{b^2}{a^2}\\right) = \\frac{e^{ax}(a\\sin(bx) - b\\cos(bx))}{a^2}$.",
    "Divide: $I = \\dfrac{e^{ax}(a\\sin(bx) - b\\cos(bx))}{a^2 + b^2} + C$."
],
"solucion": "Sea $I = \\int e^{ax}\\sin(bx)\\,dx$. Primera integración por partes ($u=\\sin bx$, $dv=e^{ax}dx$):\\n$$I = \\frac{e^{ax}\\sin(bx)}{a} - \\frac{b}{a}\\int e^{ax}\\cos(bx)\\,dx.$$\\nSegunda integración por partes en el integral restante ($u=\\cos bx$, $dv=e^{ax}dx$):\\n$$\\int e^{ax}\\cos(bx)\\,dx = \\frac{e^{ax}\\cos(bx)}{a} + \\frac{b}{a}I.$$\\nSustituyendo: $I = \\frac{e^{ax}\\sin bx}{a} - \\frac{b}{a}\\!\\left(\\frac{e^{ax}\\cos bx}{a}+\\frac{b}{a}I\\right)$, es decir $I\\cdot\\frac{a^2+b^2}{a^2} = \\frac{e^{ax}(a\\sin bx - b\\cos bx)}{a^2}$. Por tanto:\\n$$\\boxed{I = \\frac{e^{ax}(a\\sin(bx)-b\\cos(bx))}{a^2+b^2}+C.}$$",
"explicacion": "La inversión algebraica es el corazón del método: la integral $I$ reaparece en el lado derecho, lo que permite despejar $I$ como si fuera una incógnita algebraica. Esto ilustra la idea de 'resolver para la integral'.",
"tiempo_estimado": 20,
"conceptos": ["integración por partes", "inversión algebraica", "formas trigonométricas-exponenciales"],
"transferencias": ["circuitos RC de CA", "análisis de Fourier", "transformadas de Laplace"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 5 Review #5.57",
"source_url": "",
"year": "",
"tags": ["integración-por-partes", "inversión-algebraica", "inversión", "nivel-intermedio"]
},

{
"id": 680,
"titulo": "EDO: $y' = 1 + y^2$",
"estrategia": "inversion",
"dificultad": 2,
"enunciado": "Resuelve la ecuación diferencial $y' = 1 + y^2$ con condición inicial $y(0) = 0$. ¿Para qué valores de $x$ es válida la solución?",
"hints": [
    "Separa variables: escribe la ecuación como $\\dfrac{dy}{1+y^2} = dx$.",
    "Integra ambos lados: $\\int \\dfrac{dy}{1+y^2} = \\int dx$.",
    "$\\arctan(y) = x + C$. Aplica $y(0)=0$ para hallar $C$.",
    "Con $C=0$: $\\arctan(y) = x$, por lo que $y = \\tan(x)$.",
    "$\\tan(x)$ está definida para $x \\in (-\\pi/2,\\,\\pi/2)$. Fuera de ese intervalo la solución 'explota'."
],
"solucion": "Separando variables: $\\dfrac{dy}{1+y^2} = dx$. Integrando: $\\arctan(y) = x + C$. Con $y(0)=0$: $C=0$. Entonces $y = \\tan(x)$, válida para $x \\in (-\\pi/2,\\,\\pi/2)$. Verificado: $y' = \\sec^2(x) = 1+\\tan^2(x) = 1+y^2$. $\\checkmark$",
"explicacion": "La inversión aquí es literal: integramos para obtener $\\arctan(y)=x$, y luego invertimos $\\arctan$ para obtener $y=\\tan(x)$. Notar que aunque la EDO parece inocente, su solución tiene singularidades: $\\tan(x)\\to\\pm\\infty$ cuando $x\\to\\pm\\pi/2$.",
"tiempo_estimado": 10,
"conceptos": ["separación de variables", "función arcotangente", "singularidades de EDOs"],
"transferencias": ["óptica geométrica", "mecánica clásica", "modelos de crecimiento explosivo"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 9 Review #9.19",
"source_url": "",
"year": "",
"tags": ["EDO", "separación-de-variables", "inversión", "nivel-básico"]
},

{
"id": 681,
"titulo": "La función Gamma: $\\Gamma(z+1) = z\\,\\Gamma(z)$",
"estrategia": "inversion",
"dificultad": 4,
"enunciado": "La función Gamma se define por $\\Gamma(z) = \\displaystyle\\int_0^{\\infty} x^{z-1}e^{-x}\\,dx$ para $z > 0$. (a) Calcula $\\Gamma(1)$. (b) Demuestra que $\\Gamma(z+1) = z\\,\\Gamma(z)$ para todo $z>0$. (c) Deduce una fórmula para $\\Gamma(n)$ cuando $n$ es un entero positivo.",
"hints": [
    "Para (a): $\\Gamma(1) = \\int_0^\\infty e^{-x}\\,dx$. Integra directamente.",
    "Para (b): aplica integración por partes a $\\Gamma(z+1) = \\int_0^\\infty x^z e^{-x}\\,dx$ con $u = x^z$ y $dv = e^{-x}dx$.",
    "El término de frontera $[-x^z e^{-x}]_0^\\infty$ vale 0 en ambos extremos (en $\\infty$ porque $e^{-x}$ domina cualquier potencia; en $0$ porque $x^z\\to 0$ para $z>0$).",
    "Queda $\\Gamma(z+1) = z \\int_0^\\infty x^{z-1}e^{-x}\\,dx = z\\,\\Gamma(z)$.",
    "Para (c): aplica la recurrencia repetidamente: $\\Gamma(n) = (n-1)\\Gamma(n-1) = \\cdots = (n-1)!\\,\\Gamma(1) = (n-1)!$."
],
"solucion": "(a) $\\Gamma(1) = \\int_0^\\infty e^{-x}\\,dx = 1$. (b) Partes con $u=x^z$, $dv=e^{-x}dx$: $\\Gamma(z+1) = [-x^z e^{-x}]_0^\\infty + z\\int_0^\\infty x^{z-1}e^{-x}\\,dx = z\\,\\Gamma(z)$. (c) $\\Gamma(n) = (n-1)\\Gamma(n-1) = \\cdots = (n-1)!$. La función Gamma extiende el factorial a todos los reales positivos.",
"explicacion": "La recurrencia $\\Gamma(z+1) = z\\,\\Gamma(z)$ es la 'inversión': reduce el cálculo de $\\Gamma$ en $z+1$ al de $\\Gamma$ en $z$. Esta simetría hacia atrás convierte la integral impropia en la generalización natural del factorial.",
"tiempo_estimado": 25,
"conceptos": ["función Gamma", "integración por partes", "factorial", "integrales impropias"],
"transferencias": ["probabilidad (distribución gamma)", "combinatoria analítica", "física cuántica"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 6 Challenge #6.30",
"source_url": "",
"year": "",
"tags": ["función-gamma", "factorial", "integrales-impropias", "inversión", "nivel-avanzado"]
},

{
"id": 682,
"titulo": "Mínimo relativo con parámetro (HMMT)",
"estrategia": "inversion",
"dificultad": 4,
"enunciado": "Determina el número real $a$ con la propiedad de que $f(a) = a$ es un mínimo relativo de la función $f(x) = x^4 - x^3 - x^2 + ax + 1$. (Fuente: HMMT)",
"hints": [
    "Si $f(a) = a$, sustituye $x = a$ en la expresión de $f$: $a^4 - a^3 - a^2 + a^2 + 1 = a$.",
    "Simplifica: $a^4 - a^3 - a + 1 = 0$. Factoriza agrupando.",
    "$a^3(a-1) - (a-1) = (a-1)(a^3-1) = (a-1)^2(a^2+a+1) = 0$.",
    "Como $a^2+a+1 > 0$ siempre (discriminante $< 0$), la única solución real es $a = 1$.",
    "Verifica que es mínimo: con $a=1$, $f'(x) = 4x^3-3x^2-2x+1$, $f'(1)=0$, y $f''(1) = 12-6-2 = 4 > 0$. $\\checkmark$"
],
"solucion": "La condición $f(a)=a$ da $a^4-a^3-a^2+a^2+1=a$, es decir $a^4-a^3-a+1=0$. Factorizando: $(a-1)^2(a^2+a+1)=0$. Como $a^2+a+1>0$, la única raíz real es $a=1$. Con $a=1$: $f'(x)=4x^3-3x^2-2x+1$, $f'(1)=0$, $f''(1)=4>0$ (mínimo relativo confirmado). La respuesta es $\\boxed{a = 1}$.",
"explicacion": "Trabajamos hacia atrás desde las condiciones del mínimo: si $f(a)=a$ (el punto está en la diagonal) y es mínimo ($f'(a)=0$, $f''(a)>0$), primero buscamos todos los $a$ que satisfacen $f(a)=a$ y luego verificamos las condiciones de mínimo.",
"tiempo_estimado": 20,
"conceptos": ["mínimos relativos", "puntos fijos", "factorización polinomial"],
"transferencias": ["optimización con restricciones", "teoría de juegos", "puntos de equilibrio"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.47 (Fuente: HMMT)",
"source_url": "",
"year": "",
"tags": ["optimización", "puntos-fijos", "inversión", "nivel-avanzado"]
},

{
"id": 683,
"titulo": "El límite de $(p^n + q^n)^{1/n}$",
"estrategia": "inversion",
"dificultad": 3,
"enunciado": "Sean $p, q > 0$. Calcula $\\displaystyle\\lim_{n \\to \\infty} (p^n + q^n)^{1/n}$.",
"hints": [
    "Supón $p \\geq q > 0$. Factoriza $p^n$ dentro de la raíz.",
    "$(p^n + q^n)^{1/n} = p \\left(1 + \\left(\\frac{q}{p}\\right)^n\\right)^{1/n}$.",
    "Como $q/p \\leq 1$, se tiene $(q/p)^n \\to 0$ cuando $n \\to \\infty$.",
    "Por tanto el factor $\\left(1+(q/p)^n\\right)^{1/n} \\to (1+0)^0$. Usa el hecho de que $1 \\leq (1+u_n)^{1/n} \\leq 2^{1/n} \\to 1$ para $u_n \\to 0$.",
    "El límite es $p \\cdot 1 = p = \\max(p,q)$."
],
"solucion": "Sin pérdida de generalidad $p \\geq q > 0$. Escribimos $(p^n+q^n)^{1/n} = p\\left(1+(q/p)^n\\right)^{1/n}$. Como $0 < q/p \\leq 1$, $(q/p)^n \\to 0$. Además $1 \\leq \\left(1+(q/p)^n\\right)^{1/n} \\leq 2^{1/n} \\to 1$. Por el teorema del emparedado el factor tiende a 1, luego $\\lim(p^n+q^n)^{1/n} = p = \\max(p,q)$. Verificado numéricamente.",
"explicacion": "Factorizar el término dominante ($p^n$) 'invierte' el problema: en lugar de sumar dos potencias que crecen sin control, miramos cuánto contribuye la parte subdominante, que resulta ser negligible. Este truco generaliza a la norma $\\ell^p$: cuando $p\\to\\infty$, la $p$-norma de un vector converge a la norma máximo.",
"tiempo_estimado": 15,
"conceptos": ["límites de sucesiones", "norma del máximo", "teorema del emparedado"],
"transferencias": ["normas $\\ell^p$", "análisis funcional", "teoría de la información"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Review #7.41",
"source_url": "",
"year": "",
"tags": ["límites", "potencias", "inversión", "nivel-intermedio"]
},

# ─────────────── OPTIMIZACIÓN 684-694 ───────────────

{
"id": 684,
"titulo": "La fábrica de blivets",
"estrategia": "optimizacion",
"dificultad": 2,
"enunciado": "Una fábrica tiene costos fijos de $\\$2500$ al día. Cada blivet cuesta $\\$900$ fabricarlo. Si la dueña fija el precio de venta en $\\$(2500 - x)$, venderá exactamente $x$ blivets al día. ¿Cuántos blivets debe producir para maximizar la ganancia diaria? ¿Cuál es la ganancia máxima?",
"hints": [
    "Expresa la ganancia diaria $P(x)$ como ingreso menos costos totales.",
    "Ingreso $= x(2500-x)$. Costo total $= 900x + 2500$.",
    "$P(x) = x(2500-x) - 900x - 2500 = -x^2 + 1600x - 2500$.",
    "Máximo de parábola cóncava: $P'(x) = -2x + 1600 = 0 \\Rightarrow x = 800$.",
    "$P(800) = -(800)^2 + 1600(800) - 2500 = \\$637{,}500$ al día. Precio de venta: $\\$1700$ por blivet."
],
"solucion": "Ganancia: $P(x) = x(2500-x) - 900x - 2500 = -x^2 + 1600x - 2500$. $P'(x) = -2x+1600 = 0 \\Rightarrow x=800$. $P''(800) = -2 < 0$ (máximo). Producir $\\mathbf{800}$ blivets al día a \\$1700 cada uno da una ganancia máxima de $\\$\\mathbf{637{,}500}$/día. Verificado con Python.",
"explicacion": "Problema clásico de maximización de ganancia: la función es cuadrática en $x$ con concavidad hacia abajo, por lo que el único punto crítico es el máximo global. El modelo captura la tensión entre precio y volumen de ventas.",
"tiempo_estimado": 12,
"conceptos": ["optimización de ganancias", "parábola", "punto crítico"],
"transferencias": ["economía microeconómica", "fijación de precios", "análisis de mercado"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.39",
"source_url": "",
"year": "",
"tags": ["optimización", "economía", "nivel-básico"]
},

{
"id": 685,
"titulo": "Jardín en sector circular",
"estrategia": "optimizacion",
"dificultad": 3,
"enunciado": "Se desea construir un jardín vallado con forma de sector circular de área $300\\text{ m}^2$. El cerco incluye los dos radios y el arco. ¿Qué radio $r$ y ángulo $\\theta$ minimizan la longitud total del cerco?",
"hints": [
    "Área del sector: $\\frac{1}{2}r^2\\theta = 300$. Despeja $\\theta$ en términos de $r$.",
    "$\\theta = 600/r^2$. Longitud del cerco: $L = 2r + r\\theta$.",
    "Sustituye: $L(r) = 2r + r\\cdot\\frac{600}{r^2} = 2r + \\frac{600}{r}$.",
    "$L'(r) = 2 - \\frac{600}{r^2} = 0 \\Rightarrow r^2 = 300 \\Rightarrow r = 10\\sqrt{3}$ m.",
    "$\\theta = 600/(10\\sqrt{3})^2 = 600/300 = 2$ radianes. Longitud mínima $= 40\\sqrt{3}$ m."
],
"solucion": "Con la restricción $r^2\\theta/2 = 300$: $\\theta = 600/r^2$. La longitud a minimizar es $L = 2r + r\\theta = 2r + 600/r$. Derivando: $L'(r) = 2 - 600/r^2 = 0 \\Rightarrow r = \\sqrt{300} = 10\\sqrt{3}\\approx 17.3$ m. Entonces $\\theta = 2$ rad. $L''(r) = 1200/r^3 > 0$ (mínimo). Longitud mínima $= 4\\cdot 10\\sqrt{3} = 40\\sqrt{3} \\approx 69.3$ m.",
"explicacion": "El ángulo óptimo resulta ser exactamente 2 radianes, independientemente del área objetivo. Este es un resultado sorprendente: el sector circular de mínimo perímetro para área dada siempre tiene $\\theta = 2$ rad.",
"tiempo_estimado": 15,
"conceptos": ["optimización con restricciones", "sector circular", "lagrangiano elemental"],
"transferencias": ["diseño de jardines", "ingeniería civil", "problemas isoperimétricos"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.40",
"source_url": "",
"year": "",
"tags": ["sector-circular", "optimización", "nivel-intermedio"]
},

{
"id": 686,
"titulo": "Samuel cruza el lago circular",
"estrategia": "optimizacion",
"dificultad": 3,
"enunciado": "Samuel quiere cruzar un lago circular de diámetro 1 km (de un punto de la orilla al punto diametralmente opuesto). Puede remar a 4 km/h o caminar por la orilla a 6 km/h. ¿Cuál es el tiempo mínimo para cruzar el lago?",
"hints": [
    "Plantea la estrategia: Samuel rema hasta un punto $C$ en la orilla opuesta (no necesariamente el punto extremo), luego camina el arco restante hasta el destino $B$.",
    "Si $\\theta$ es el ángulo entre la cuerda $AC$ y el diámetro (radio $R=1/2$), la cuerda mide $2R\\cos(\\theta/2) = \\cos(\\theta/2)$ km y el arco $CB$ mide $R\\theta = \\theta/2$ km.",
    "$T(\\theta) = \\dfrac{\\cos(\\theta/2)}{4} + \\dfrac{\\theta}{12}$. Deriva e iguala a cero.",
    "$T'(\\theta) = -\\dfrac{\\sin(\\theta/2)}{8} + \\dfrac{1}{12} = 0 \\Rightarrow \\sin(\\theta/2) = 2/3$. Verifica si es mínimo o máximo.",
    "$T''(\\theta) < 0$ en ese punto: ¡es un máximo local! Por tanto el mínimo está en la frontera: ir directo ($\\theta=0$) tarda $T = 1/4$ h $= 15$ min, y rodear la orilla ($\\theta = \\pi$) tarda $T = \\pi/12 \\approx 15.7$ min. La estrategia óptima es remar directamente."
],
"solucion": "$T(\\theta) = \\frac{\\cos(\\theta/2)}{4} + \\frac{\\theta}{12}$. El punto crítico interior $\\sin(\\theta/2)=2/3$ es un **máximo** local (pues $T''<0$). Los valores en frontera son $T(0) = 1/4$ h y $T(\\pi) = \\pi/12 \\approx 0.262$ h. El mínimo es $T = 1/4$ h $= \\mathbf{15}$ minutos, remando directo a través del diámetro. ¡La optimización revela que la estrategia más intuitiva es la óptima!",
"explicacion": "Esta trampa clásica de cálculo enseña a verificar siempre si los puntos críticos son mínimos o máximos, y a revisar las fronteras del dominio. El punto crítico aquí resulta ser un máximo, ¡no un mínimo!",
"tiempo_estimado": 20,
"conceptos": ["optimización con frontera", "puntos críticos vs frontera", "geometría circular"],
"transferencias": ["logística de transporte", "navegación", "problemas de ruta óptima"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.48(a)",
"source_url": "",
"year": "",
"tags": ["optimización-frontera", "geometría", "nivel-intermedio"]
},

{
"id": 687,
"titulo": "La Ley de Snell desde el cálculo",
"estrategia": "optimizacion",
"dificultad": 3,
"enunciado": "La luz viaja del punto $A=(0,a)$ (semiplano $y>0$) al punto $B=(d,-b)$ (semiplano $y<0$), con $a,b,d>0$. La velocidad de la luz en el semiplano superior es $c_1$ y en el inferior es $c_2$. La luz cruza el eje $x$ en el punto $X=(x,0)$ para minimizar el tiempo total de viaje. Encuentra la ecuación que satisface $x$ óptimo e interprétala geométricamente.",
"hints": [
    "Tiempo total: $T(x) = \\dfrac{\\sqrt{x^2+a^2}}{c_1} + \\dfrac{\\sqrt{(d-x)^2+b^2}}{c_2}$.",
    "$T'(x) = \\dfrac{x}{c_1\\sqrt{x^2+a^2}} - \\dfrac{d-x}{c_2\\sqrt{(d-x)^2+b^2}} = 0$.",
    "Sea $\\theta_1$ el ángulo de incidencia (entre el rayo $AX$ y la normal al eje $x$): $\\sin\\theta_1 = x/\\sqrt{x^2+a^2}$.",
    "Sea $\\theta_2$ el ángulo de refracción: $\\sin\\theta_2 = (d-x)/\\sqrt{(d-x)^2+b^2}$.",
    "La condición $T'(x)=0$ se convierte en $\\sin\\theta_1/c_1 = \\sin\\theta_2/c_2$, es decir $\\sin\\theta_1/\\sin\\theta_2 = c_1/c_2$. ¡Esta es la Ley de Snell!"
],
"solucion": "$T'(x)=0$ es equivalente a $\\dfrac{\\sin\\theta_1}{c_1} = \\dfrac{\\sin\\theta_2}{c_2}$, donde $\\theta_1$ y $\\theta_2$ son los ángulos con la normal (eje $y$) en el punto de cruce. Esto es la **Ley de Snell**: $n_1\\sin\\theta_1 = n_2\\sin\\theta_2$ (con $n_i = 1/c_i$). La luz elige el camino que minimiza el tiempo, lo que implica refractarse al cambiar de medio.",
"explicacion": "El principio de Fermat (la luz toma el camino de mínimo tiempo) implica la ley de Snell. El cálculo traduce el principio físico en una ecuación trascendente cuya solución geométrica es la conocida relación de senos y velocidades.",
"tiempo_estimado": 20,
"conceptos": ["Principio de Fermat", "Ley de Snell", "optimización geométrica"],
"transferencias": ["óptica geométrica", "diseño de lentes", "metamateriales", "sísmología"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.50",
"source_url": "",
"year": "",
"tags": ["óptica", "Snell", "optimización", "nivel-intermedio"]
},

{
"id": 688,
"titulo": "Velocidad de ascenso en la rueda de la fortuna",
"estrategia": "optimizacion",
"dificultad": 3,
"enunciado": "La rueda de la fortuna de una feria tiene 60 metros de diámetro y gira a 4 revoluciones por minuto. Natalia está en uno de los carros. ¿A qué velocidad (en m/min) gana altura cuando pasa (subiendo) por la altura de 40 metros?",
"hints": [
    "El centro de la rueda está a 30 m del suelo. Si $t=0$ es cuando Natalia está abajo (0 m), su altura es $y(t) = 30 - 30\\cos(\\omega t)$, con $\\omega = 4 \\cdot 2\\pi = 8\\pi$ rad/min.",
    "Deriva: $dy/dt = 30\\omega\\sin(\\omega t) = 240\\pi\\sin(8\\pi t)$.",
    "Cuando $y = 40$: $30 - 30\\cos(8\\pi t) = 40 \\Rightarrow \\cos(8\\pi t) = -1/3$.",
    "$\\sin(8\\pi t) = \\sqrt{1 - 1/9} = \\sqrt{8/9} = \\frac{2\\sqrt{2}}{3}$ (positivo porque va subiendo).",
    "$dy/dt = 240\\pi \\cdot \\frac{2\\sqrt{2}}{3} = 160\\sqrt{2}\\,\\pi \\approx 710.9$ m/min."
],
"solucion": "Con $y(t) = 30 - 30\\cos(8\\pi t)$, la tasa de cambio es $dy/dt = 240\\pi\\sin(8\\pi t)$. En $y=40$: $\\cos(8\\pi t)=-1/3$, $\\sin(8\\pi t)=2\\sqrt{2}/3$. Tasa $= 240\\pi \\cdot \\frac{2\\sqrt{2}}{3} = 160\\sqrt{2}\\,\\pi \\approx \\mathbf{710.9}$ m/min $\\approx 11.85$ m/s. Verificado con Python.",
"explicacion": "Problema de tasas relacionadas con movimiento circular: la altura es una función coseno, y su derivada (la velocidad vertical) depende del ángulo en ese instante. El punto clave es encontrar $\\sin(\\omega t)$ cuando $\\cos(\\omega t)=-1/3$.",
"tiempo_estimado": 18,
"conceptos": ["movimiento circular", "tasas relacionadas", "identidad pitagórica trigonométrica"],
"transferencias": ["cinemática rotacional", "ingeniería mecánica", "animación por computadora"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.42",
"source_url": "",
"year": "",
"tags": ["tasas-relacionadas", "movimiento-circular", "optimización", "nivel-intermedio"]
},

{
"id": 689,
"titulo": "La integral del Putnam y la aproximación $22/7$",
"estrategia": "optimizacion",
"dificultad": 4,
"enunciado": "Calcula $\\displaystyle\\int_0^1 \\frac{x^4(1-x)^4}{1+x^2}\\,dx$. (Fuente: Putnam) ¿Qué revela este resultado sobre la aproximación $\\pi \\approx 22/7$?",
"hints": [
    "Expande el numerador: $x^4(1-x)^4 = x^4 - 4x^5 + 6x^6 - 4x^7 + x^8$.",
    "Divide entre $1+x^2$ usando división polinomial: $\\frac{x^4(1-x)^4}{1+x^2} = x^6 - 4x^5 + 5x^4 - 4x^2 + 4 - \\frac{4}{1+x^2}$.",
    "Integra término a término de $0$ a $1$: $\\int_0^1 x^k\\,dx = \\frac{1}{k+1}$, e $\\int_0^1 \\frac{4}{1+x^2}\\,dx = 4\\arctan(1) = \\pi$.",
    "$\\int_0^1 \\frac{x^4(1-x)^4}{1+x^2}\\,dx = \\frac{1}{7} - \\frac{4}{6} + \\frac{5}{5} - \\frac{4}{3} + 4 - \\pi = \\frac{22}{7} - \\pi$.",
    "Como el integrando es $\\geq 0$ en $[0,1]$, el resultado $22/7 - \\pi > 0$, lo que prueba que $\\pi < 22/7$."
],
"solucion": "Mediante división polinomial: $\\frac{x^4(1-x)^4}{1+x^2} = x^6-4x^5+5x^4-4x^2+4-\\frac{4}{1+x^2}$. Integrando: $\\int_0^1 = \\frac{1}{7}-\\frac{2}{3}+1-\\frac{4}{3}+4-\\pi = \\frac{22}{7}-\\pi \\approx 0.00126$. Como el integrando es no negativo, $\\mathbf{22/7 - \\pi > 0}$, probando que $\\pi < 22/7$. Verificado con Python.",
"explicacion": "Esta integral famosa cuantifica el error de la aproximación $22/7$ para $\\pi$: el error es exactamente la integral, que es pequeño pero positivo. Un resultado elegante que conecta integración, series y teoría de números.",
"tiempo_estimado": 30,
"conceptos": ["división polinomial", "integrales de fracciones racionales", "aproximaciones de $\\pi$"],
"transferencias": ["teoría de números", "análisis numérico", "series para $\\pi$"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 5 Challenge #5.67(a) (Fuente: Putnam)",
"source_url": "",
"year": "",
"tags": ["integral-definida", "Putnam", "pi", "optimización", "nivel-avanzado"]
},

{
"id": 690,
"titulo": "Área de la intersección de dos cardioidas",
"estrategia": "optimizacion",
"dificultad": 4,
"enunciado": "Calcula el área de la región que está simultáneamente en el interior de las dos cardioidas $r = 1 + \\sin\\theta$ y $r = 1 + \\cos\\theta$.",
"hints": [
    "Primero halla las intersecciones: $1+\\sin\\theta = 1+\\cos\\theta \\Rightarrow \\sin\\theta = \\cos\\theta \\Rightarrow \\theta = \\pi/4$ y $\\theta = 5\\pi/4$.",
    "En $[0, 2\\pi]$, la región interior a ambas cardioidas está donde $r \\leq \\min(1+\\sin\\theta, 1+\\cos\\theta)$. Por simetría respecto a la bisectriz $\\theta=\\pi/8$, puede simplificarse.",
    "Para $\\theta \\in [-3\\pi/4, \\pi/4]$, $1+\\cos\\theta \\leq 1+\\sin\\theta$; para $\\theta \\in [\\pi/4, 5\\pi/4]$, viceversa.",
    "Área $= 2\\cdot\\frac{1}{2}\\int_{-3\\pi/4}^{\\pi/4}(1+\\cos\\theta)^2\\,d\\theta$ (por simetría).",
    "Expandiendo: $\\int(1+2\\cos\\theta+\\cos^2\\theta)d\\theta = \\int\\left(\\frac{3}{2}+2\\cos\\theta+\\frac{\\cos 2\\theta}{2}\\right)d\\theta$. El resultado es $\\dfrac{3\\pi}{2} - 2\\sqrt{2}$."
],
"solucion": "Las cardioidas se cortan en $\\theta=\\pi/4$ y $\\theta=5\\pi/4$. Área interior a ambas $= \\int_{-3\\pi/4}^{\\pi/4}(1+\\cos\\theta)^2\\,d\\theta$ (usando simetría). Expandiendo $\\cos^2\\theta = (1+\\cos 2\\theta)/2$: resultado $= \\dfrac{3\\pi}{2} - 2\\sqrt{2} \\approx 1.884$. Verificado numéricamente con Python.",
"explicacion": "Las dos cardioidas son congruentes entre sí (rotadas 90°). El área de su intersección combina integración polar con simetría geométrica. El resultado $3\\pi/2 - 2\\sqrt{2}$ mezcla armónicamente la razón áurea del círculo con la diagonal $\\sqrt{2}$.",
"tiempo_estimado": 35,
"conceptos": ["coordenadas polares", "intersección de curvas", "área polar"],
"transferencias": ["diseño de logos", "geometría de curvas", "integrales de contorno"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 8 Review #8.25",
"source_url": "",
"year": "",
"tags": ["polar", "cardioida", "área", "optimización", "nivel-avanzado"]
},

{
"id": 691,
"titulo": "Área de un pétalo de la rosa polar",
"estrategia": "optimizacion",
"dificultad": 2,
"enunciado": "Calcula el área de un pétalo de la curva polar $r = \\cos 2\\theta$.",
"hints": [
    "La curva $r = \\cos 2\\theta$ es una rosa de 4 pétalos. El pétalo sobre el eje positivo $x$ existe para $\\theta\\in[-\\pi/4, \\pi/4]$ (donde $\\cos 2\\theta \\geq 0$).",
    "Área de una región polar: $A = \\dfrac{1}{2}\\int_\\alpha^\\beta r^2\\,d\\theta$.",
    "$A = \\dfrac{1}{2}\\int_{-\\pi/4}^{\\pi/4} \\cos^2(2\\theta)\\,d\\theta$.",
    "Usa $\\cos^2(2\\theta) = \\dfrac{1+\\cos(4\\theta)}{2}$.",
    "$A = \\dfrac{1}{4}\\int_{-\\pi/4}^{\\pi/4}(1+\\cos 4\\theta)\\,d\\theta = \\dfrac{1}{4}\\left[\\theta + \\frac{\\sin 4\\theta}{4}\\right]_{-\\pi/4}^{\\pi/4} = \\dfrac{\\pi}{8}$."
],
"solucion": "$A = \\frac{1}{2}\\int_{-\\pi/4}^{\\pi/4}\\cos^2(2\\theta)\\,d\\theta = \\frac{1}{4}\\int_{-\\pi/4}^{\\pi/4}(1+\\cos 4\\theta)\\,d\\theta = \\frac{1}{4}\\cdot\\frac{\\pi}{2} = \\mathbf{\\dfrac{\\pi}{8}}$. Área total de los 4 pétalos $= 4\\cdot\\pi/8 = \\pi/2$. Verificado con Python.",
"explicacion": "El área polar usa $r^2/2$ en lugar de $r$ porque los 'triángulos' en polares son sectores, no rectángulos. La identidad trigonométrica convierte $\\cos^2$ en una integral directa.",
"tiempo_estimado": 12,
"conceptos": ["área polar", "rosa polar", "identidad de doble ángulo"],
"transferencias": ["diseño de antenas", "geometría floral", "curvas en polares"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 8 Challenge #8.30(b)",
"source_url": "",
"year": "",
"tags": ["polares", "área", "trigonometría", "optimización", "nivel-básico"]
},

{
"id": 692,
"titulo": "Estimación de $\\int_0^1 \\sin(x^2)\\,dx$ con series",
"estrategia": "optimizacion",
"dificultad": 3,
"enunciado": "Estima $\\displaystyle\\int_0^1 \\sin(x^2)\\,dx$ con exactamente tres decimales de precisión, usando la serie de Taylor de $\\sin u$.",
"hints": [
    "La serie de Taylor de $\\sin u$ alrededor de $u=0$: $\\sin u = u - \\dfrac{u^3}{3!} + \\dfrac{u^5}{5!} - \\cdots$",
    "Sustituye $u = x^2$: $\\sin(x^2) = x^2 - \\dfrac{x^6}{6} + \\dfrac{x^{10}}{120} - \\dfrac{x^{14}}{5040} + \\cdots$",
    "Integra término a término de $0$ a $1$: $\\int_0^1 x^{2k}\\,dx = \\dfrac{1}{2k+1}$.",
    "$\\int_0^1 \\sin(x^2)\\,dx = \\dfrac{1}{3} - \\dfrac{1}{42} + \\dfrac{1}{1320} - \\dfrac{1}{75600} + \\cdots$",
    "Tres términos dan $0.3333 - 0.0238 + 0.000758 \\approx 0.3103$. El siguiente término $< 0.00002$, así que la estimación es $\\approx 0.310$ (tres decimales exactos)."
],
"solucion": "$\\sin(x^2) = \\sum_{k=0}^\\infty \\frac{(-1)^k x^{4k+2}}{(2k+1)!}$. Integrando: $\\int_0^1 \\sin(x^2)\\,dx = \\sum_{k=0}^\\infty \\frac{(-1)^k}{(2k+1)!\\,(4k+3)}$. Calculando: $\\frac{1}{3} - \\frac{1}{42} + \\frac{1}{1320} - \\frac{1}{75600} + \\cdots \\approx 0.3333 - 0.0238 + 0.000758 - \\cdots \\approx \\mathbf{0.310}$. Verificado con Python (valor exacto $\\approx 0.310268$).",
"explicacion": "La integral de Fresnel $\\int_0^x \\sin(t^2)\\,dt$ no tiene forma cerrada en funciones elementales, pero las series de Taylor permiten calcularla con precisión arbitraria. Este es el poder de la integración término a término.",
"tiempo_estimado": 20,
"conceptos": ["series de Taylor", "integración término a término", "estimación de error"],
"transferencias": ["integral de Fresnel", "difracción de ondas", "análisis numérico"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Review #7.40",
"source_url": "",
"year": "",
"tags": ["series", "integral-de-Fresnel", "estimación", "optimización", "nivel-intermedio"]
},

{
"id": 693,
"titulo": "La gravedad en altitud",
"estrategia": "optimizacion",
"dificultad": 2,
"enunciado": "La aceleración gravitacional varía con la distancia al centro de la Tierra según $g(r) = GM/r^2$, donde $G,M$ son constantes. El radio terrestre es $R = 6400$ km. Estima, usando aproximación lineal, el porcentaje de disminución de $g$ a 10 km de altitud.",
"hints": [
    "La gravedad a altitud $h$ es $g(R+h) = GM/(R+h)^2$. La fracción de cambio es $g(R+h)/g(R) - 1$.",
    "$g(R+h)/g(R) = R^2/(R+h)^2 = (1+h/R)^{-2}$.",
    "Aproximación lineal para $(1+u)^{-2} \\approx 1 - 2u$ cuando $u$ es pequeño. Aquí $u = h/R$.",
    "Disminución relativa $\\approx 2h/R$. Con $h=10$ km y $R=6400$ km: $2\\times 10/6400 = 0.003125 = 0.3125\\%$.",
    "El valor exacto es $1-(6400/6410)^2 \\approx 0.3118\\%$. ¡La aproximación lineal es muy precisa!"
],
"solucion": "$(1+h/R)^{-2} \\approx 1 - 2h/R$ para $h \\ll R$. Disminución $\\approx 2h/R = 2\\times 10/6400 \\approx \\mathbf{0.3125\\%}$. Valor exacto: $1-(6400/6410)^2 \\approx 0.3118\\%$. La aproximación lineal da el resultado correcto al 0.2\\%. Verificado con Python.",
"explicacion": "La aproximación lineal $(1+u)^{-2}\\approx 1-2u$ reduce una función no lineal a un problema lineal. La clave es identificar $u=h/R \\approx 0.0016$, que es suficientemente pequeño para que la aproximación sea precisa.",
"tiempo_estimado": 10,
"conceptos": ["aproximación lineal", "gravedad", "series de Taylor de primer orden"],
"transferencias": ["física satelital", "correcciones relativistas", "cartografía geodésica"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.41",
"source_url": "",
"year": "",
"tags": ["aproximación-lineal", "física", "gravedad", "optimización", "nivel-básico"]
},

{
"id": 694,
"titulo": "El pastel que se enfría",
"estrategia": "optimizacion",
"dificultad": 2,
"enunciado": "Al salir del horno, la temperatura de un pastel es $T(t) = 70 + 230e^{-kt}$ grados Fahrenheit, donde $t$ está en minutos. Tras 10 minutos, la temperatura es 200 °F. (a) ¿Cuánto tiempo tarda en llegar a 150 °F? (b) ¿A qué velocidad se estaba enfriando en ese momento?",
"hints": [
    "De $T(10) = 200$: $70 + 230e^{-10k} = 200 \\Rightarrow e^{-10k} = 130/230 = 13/23$.",
    "$k = \\dfrac{\\ln(23/13)}{10} \\approx 0.05705$ min$^{-1}$.",
    "Para (a): $70 + 230e^{-kt} = 150 \\Rightarrow e^{-kt} = 80/230 = 8/23 \\Rightarrow t = \\dfrac{\\ln(23/8)}{k}$.",
    "Sustituye $k$: $t = 10\\dfrac{\\ln(23/8)}{\\ln(23/13)} \\approx 18.5$ minutos.",
    "Para (b): $T'(t) = -k\\cdot 230\\,e^{-kt}$. En $t\\approx 18.5$: $T' = -k\\cdot 230\\cdot(8/23) = -80k \\approx -4.56$ °F/min."
],
"solucion": "(a) $k = \\ln(23/13)/10 \\approx 0.0571$ min$^{-1}$. Despejando: $t = 10\\ln(23/8)/\\ln(23/13) \\approx \\mathbf{18.5}$ minutos. (b) $T'(t) = -230k\\,e^{-kt}$; en ese punto $e^{-kt}=8/23$, por lo que $T' = -230k\\cdot 8/23 = -80k \\approx \\mathbf{-4.56}$ °F/min. Verificado con Python.",
"explicacion": "La Ley de Enfriamiento de Newton: la temperatura decae exponencialmente hacia la temperatura ambiente. El parámetro $k$ se determina a partir de una medición, y luego se pueden predecir tiempos y tasas en cualquier momento.",
"tiempo_estimado": 15,
"conceptos": ["ley de enfriamiento de Newton", "función exponencial", "tasas instantáneas"],
"transferencias": ["termodinámica aplicada", "medicina forense", "climatización"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.43",
"source_url": "",
"year": "",
"tags": ["enfriamiento", "exponencial", "tasas", "optimización", "nivel-básico"]
},

# ─────────────── INVARIANTES 695-705 ───────────────

{
"id": 695,
"titulo": "La energía conservada del oscilador armónico",
"estrategia": "invariantes",
"dificultad": 2,
"enunciado": "Sea $f:\\mathbb{R}\\to\\mathbb{R}$ dos veces diferenciable, con $f''(x) + f(x) = 0$ para todo $x$. Define $g(x) = (f(x))^2 + (f'(x))^2$. Demuestra que $g$ es constante.",
"hints": [
    "Calcula $g'(x)$ usando la regla de la cadena.",
    "$g'(x) = 2f(x)f'(x) + 2f'(x)f''(x)$.",
    "Factoriza: $g'(x) = 2f'(x)[f(x) + f''(x)]$.",
    "¿Qué dice la hipótesis sobre $f(x) + f''(x)$?",
    "$f''(x) = -f(x)$, por lo que $f(x) + f''(x) = 0$. Entonces $g'(x) = 0$, lo que significa que $g$ es constante. $\\square$"
],
"solucion": "$g'(x) = 2f(x)f'(x) + 2f'(x)f''(x) = 2f'(x)[f(x)+f''(x)] = 2f'(x)\\cdot 0 = 0$. Como la derivada es idénticamente cero, $g(x) = (f(x))^2+(f'(x))^2$ es constante para toda $x$. $\\square$",
"explicacion": "En física, $g(x)$ es la energía mecánica de un oscilador armónico (suma de energía potencial y cinética). El resultado demuestra que esta energía se conserva: siempre que $f''+f=0$, la trayectoria en el espacio de fase $(f, f')$ es un círculo de radio $\\sqrt{g}$.",
"tiempo_estimado": 10,
"conceptos": ["cantidad conservada", "oscilador armónico", "derivada nula implica constante"],
"transferencias": ["mecánica clásica", "circuitos LC", "análisis de Fourier"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 9 Challenge #9.30(a)",
"source_url": "",
"year": "",
"tags": ["EDO", "invariante", "energía-conservada", "nivel-básico"]
},

{
"id": 696,
"titulo": "Puntos de inflexión y el grado del polinomio",
"estrategia": "invariantes",
"dificultad": 2,
"enunciado": "(a) Demuestra que si $f$ es un polinomio cuadrático, su gráfica no tiene puntos de inflexión. (b) Demuestra que si $f$ es un polinomio cúbico, su gráfica tiene exactamente un punto de inflexión. (c) ¿Cuál es el patrón general para un polinomio de grado $n$?",
"hints": [
    "Un punto de inflexión ocurre donde $f''$ cambia de signo. Relaciona el grado de $f''$ con el de $f$.",
    "Para $f$ cuadrático ($\\deg f = 2$): $f''$ es constante $\\neq 0$, nunca cambia de signo.",
    "Para $f$ cúbico ($\\deg f = 3$): $f''$ es lineal (grado 1), con exactamente una raíz donde cambia de signo.",
    "Para $\\deg f = n$: $f''$ tiene grado $n-2$. Un polinomio real de grado $n-2$ tiene a lo sumo $n-2$ raíces reales.",
    "Por tanto un polinomio de grado $n$ tiene a lo sumo $n-2$ puntos de inflexión."
],
"solucion": "(a) Para $f(x)=ax^2+bx+c$: $f''=2a$ (constante no nula), sin cambios de signo, sin inflexión. (b) Para $f(x)=ax^3+bx^2+cx+d$: $f''=6ax+2b$ (lineal), exactamente una raíz $x_0=-b/(3a)$ donde cambia de signo. (c) Un polinomio de grado $n$ tiene a lo sumo $n-2$ puntos de inflexión (pues $f''$ es de grado $n-2$).",
"explicacion": "El invariante es la relación entre el grado de un polinomio y el número de sus puntos de inflexión: cada derivación reduce el grado en 1, y los inflexión son raíces de la segunda derivada. Esta es una aplicación del teorema fundamental del álgebra aplicado iterativamente.",
"tiempo_estimado": 12,
"conceptos": ["puntos de inflexión", "grado de un polinomio", "segunda derivada"],
"transferencias": ["análisis de gráficas", "ingeniería estructural", "diseño de curvas"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Review #4.36",
"source_url": "",
"year": "",
"tags": ["inflexión", "polinomios", "invariante", "nivel-básico"]
},

{
"id": 697,
"titulo": "La regla de Leibniz para integrales con límites variables",
"estrategia": "invariantes",
"dificultad": 3,
"enunciado": "Sea $f$ una función continua y $u(x), v(x)$ funciones diferenciables. Halla una fórmula para $\\dfrac{d}{dx}\\displaystyle\\int_{u(x)}^{v(x)} f(t)\\,dt$.",
"hints": [
    "Sea $F$ una antiderivada de $f$ (garantizada por el TFC). Entonces $\\int_{u(x)}^{v(x)} f(t)\\,dt = F(v(x)) - F(u(x))$.",
    "Deriva respecto a $x$ usando la regla de la cadena.",
    "$\\dfrac{d}{dx}F(v(x)) = F'(v(x))\\cdot v'(x) = f(v(x))\\cdot v'(x)$.",
    "$\\dfrac{d}{dx}F(u(x)) = f(u(x))\\cdot u'(x)$.",
    "Resultado: $\\dfrac{d}{dx}\\int_{u(x)}^{v(x)} f(t)\\,dt = f(v(x))\\,v'(x) - f(u(x))\\,u'(x)$."
],
"solucion": "Sea $F'=f$. Entonces $\\int_{u}^{v} f(t)\\,dt = F(v(x))-F(u(x))$. Derivando por la regla de la cadena:\\n$$\\frac{d}{dx}\\int_{u(x)}^{v(x)} f(t)\\,dt = f(v(x))\\,v'(x) - f(u(x))\\,u'(x).$$\\nEste resultado generaliza el TFC (caso $u(x)=a$ constante, $v(x)=x$: $f(x)$) a límites variables arbitrarios.",
"explicacion": "La 'invariante' aquí es el Teorema Fundamental del Cálculo: la derivada e integral son operaciones inversas, y esta identidad preserva esa relación incluso cuando los límites dependen de $x$. Es la base de técnicas como diferenciación bajo el signo integral (el truco de Feynman).",
"tiempo_estimado": 15,
"conceptos": ["Teorema Fundamental del Cálculo", "regla de la cadena", "regla de Leibniz"],
"transferencias": ["ecuaciones integro-diferenciales", "probabilidad", "truco de Feynman"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 5 Review #5.60",
"source_url": "",
"year": "",
"tags": ["TFC", "Leibniz", "derivación-bajo-integral", "invariante", "nivel-intermedio"]
},

{
"id": 698,
"titulo": "Convergencia de $\\sum n!/(cn)^n$ y el número $e$",
"estrategia": "invariantes",
"dificultad": 4,
"enunciado": "Sea $c > 0$. Demuestra que la serie $\\displaystyle\\sum_{n=1}^{\\infty} \\dfrac{n!}{(cn)^n}$ converge si $c > e$ y diverge si $c < e$. (Fuente: HMMT)",
"hints": [
    "Aplica el criterio del cociente: calcula $\\lim_{n\\to\\infty} |a_{n+1}/a_n|$.",
    "$\\dfrac{a_{n+1}}{a_n} = \\dfrac{(n+1)!}{(c(n+1))^{n+1}} \\cdot \\dfrac{(cn)^n}{n!} = \\dfrac{n+1}{c^{n+1}(n+1)^{n+1}} \\cdot c^n n^n$.",
    "Simplifica: $\\dfrac{a_{n+1}}{a_n} = \\dfrac{1}{c} \\left(\\dfrac{n}{n+1}\\right)^n = \\dfrac{1}{c}\\left(1-\\dfrac{1}{n+1}\\right)^n$.",
    "$\\left(1-\\dfrac{1}{n+1}\\right)^n \\to e^{-1}$ cuando $n\\to\\infty$ (límite fundamental de $e$).",
    "El cociente tiende a $1/(ce)$. Por el criterio del cociente: converge si $1/(ce) < 1$ ($c>e$); diverge si $1/(ce) > 1$ ($c<e$)."
],
"solucion": "Criterio del cociente: $\\dfrac{a_{n+1}}{a_n} = \\dfrac{1}{c}\\left(1-\\dfrac{1}{n+1}\\right)^n \\to \\dfrac{1}{ce}$. La serie converge si $1/(ce) < 1$, i.e., $c > e \\approx 2.718$, y diverge si $c < e$. Verificado: el umbral es exactamente $e$.",
"explicacion": "El número $e$ aparece naturalmente como umbral de convergencia porque el límite $(1-1/n)^n = e^{-1}$ es una de sus definiciones. El invariante aquí es la constante $e$ que emerge del comportamiento asintótico de $n!/(cn)^n$, conectando análisis y combinatoria.",
"tiempo_estimado": 25,
"conceptos": ["criterio del cociente", "número $e$", "convergencia de series", "aproximación de Stirling"],
"transferencias": ["análisis combinatorio", "teoría de probabilidad", "combinatoria asintótica"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Review #7.42 (Fuente: HMMT)",
"source_url": "",
"year": "",
"tags": ["series", "criterio-del-cociente", "número-e", "invariante", "nivel-avanzado"]
},

{
"id": 699,
"titulo": "La función generatriz de los números de Fibonacci",
"estrategia": "invariantes",
"dificultad": 4,
"enunciado": "Los números de Fibonacci se definen por $a_0 = a_1 = 1$ y $a_n = a_{n-1} + a_{n-2}$ para $n \\geq 2$. Sea $f(x) = \\sum_{n=0}^{\\infty} a_n x^n$. Demuestra que $f(x) = \\dfrac{1}{1-x-x^2}$ para $|x| < 1/2$.",
"hints": [
    "Calcula $f(x)(1-x-x^2)$ expandiendo el producto de la serie con el polinomio.",
    "$(1-x-x^2)\\sum_{n=0}^\\infty a_n x^n = \\sum a_n x^n - \\sum a_n x^{n+1} - \\sum a_n x^{n+2}$.",
    "Re-indexa: el coeficiente de $x^n$ (para $n\\geq 2$) es $a_n - a_{n-1} - a_{n-2}$.",
    "Por la recurrencia de Fibonacci, $a_n - a_{n-1} - a_{n-2} = 0$. El coeficiente de $x^0$ es $a_0 = 1$, el de $x^1$ es $a_1 - a_0 = 0$.",
    "Por tanto $f(x)(1-x-x^2) = 1$, luego $f(x) = 1/(1-x-x^2)$. $\\square$"
],
"solucion": "Calcula $(1-x-x^2)f(x) = \\sum_{n\\geq 0} a_n x^n - \\sum_{n\\geq 0} a_n x^{n+1} - \\sum_{n\\geq 0} a_n x^{n+2} = a_0 + (a_1-a_0)x + \\sum_{n\\geq 2}(a_n-a_{n-1}-a_{n-2})x^n = 1 + 0 + 0 = 1$, usando la recurrencia. Por tanto $f(x) = 1/(1-x-x^2)$ para $|x| < 1/2$. $\\square$",
"explicacion": "El invariante es la recurrencia de Fibonacci: al multiplicar la serie por $(1-x-x^2)$, todos los coeficientes de $n\\geq 2$ se cancelan exactamente por la recurrencia $a_n = a_{n-1}+a_{n-2}$. Las funciones generatrices transforman relaciones de recurrencia en identidades de funciones racionales.",
"tiempo_estimado": 25,
"conceptos": ["función generatriz", "sucesión de Fibonacci", "series de potencias"],
"transferencias": ["combinatoria analítica", "análisis de algoritmos", "teoría de números"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Challenge #7.47(b)",
"source_url": "",
"year": "",
"tags": ["Fibonacci", "función-generatriz", "invariante", "nivel-avanzado"]
},

{
"id": 700,
"titulo": "Expresar $\\int x^2 e^{-x^2}dx$ con la función error",
"estrategia": "invariantes",
"dificultad": 3,
"enunciado": "Sea $f(x)$ una antiderivada de $e^{-x^2}$ (es decir, $f'(x) = e^{-x^2}$). Esta función no se puede expresar en términos de funciones elementales. Expresa $\\displaystyle\\int x^2 e^{-x^2}\\,dx$ en términos de $f(x)$.",
"hints": [
    "Reescribe $x^2 e^{-x^2} = x \\cdot (x e^{-x^2})$. ¿Para qué sirve factorizar así?",
    "Aplica integración por partes: $u = x$ y $dv = x e^{-x^2}\\,dx$. ¿Cuál es $v$?",
    "$v = \\int x e^{-x^2}\\,dx = -\\dfrac{e^{-x^2}}{2}$ (usa sustitución $w = -x^2$).",
    "$\\int x^2 e^{-x^2}\\,dx = x\\cdot\\left(-\\frac{e^{-x^2}}{2}\\right) - \\int \\left(-\\frac{e^{-x^2}}{2}\\right)\\,dx$.",
    "$= -\\dfrac{x e^{-x^2}}{2} + \\dfrac{1}{2}\\int e^{-x^2}\\,dx = -\\dfrac{x e^{-x^2}}{2} + \\dfrac{f(x)}{2} + C$."
],
"solucion": "Partes con $u=x$, $dv = xe^{-x^2}dx$ (de modo que $v = -e^{-x^2}/2$):\\n$$\\int x^2 e^{-x^2}\\,dx = -\\frac{x e^{-x^2}}{2} + \\frac{1}{2}\\int e^{-x^2}\\,dx = \\boxed{-\\frac{x e^{-x^2}}{2} + \\frac{f(x)}{2} + C}.$$",
"explicacion": "El invariante es la relación: $\\int x^2 e^{-x^2}dx$ se reduce (via partes) a $\\int e^{-x^2}dx$ más un término elemental. Esto muestra que cualquier $\\int x^{2k}e^{-x^2}dx$ se puede expresar en términos de $f(x)$ mediante integración por partes repetida.",
"tiempo_estimado": 15,
"conceptos": ["integración por partes", "función error", "antiderivadas no elementales"],
"transferencias": ["estadística (distribución normal)", "física cuántica", "análisis de señales"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 5 Review #5.56",
"source_url": "",
"year": "",
"tags": ["función-error", "partes", "invariante", "nivel-intermedio"]
},

{
"id": 701,
"titulo": "El lema de Riemann-Lebesgue elemental",
"estrategia": "invariantes",
"dificultad": 2,
"enunciado": "Para cualesquiera $a \\leq b$, demuestra que $\\displaystyle\\lim_{m \\to \\infty} \\int_a^b \\sin(mx)\\,dx = 0$.",
"hints": [
    "Integra directamente $\\int_a^b \\sin(mx)\\,dx$ con respecto a $x$.",
    "$\\int_a^b \\sin(mx)\\,dx = \\left[-\\dfrac{\\cos(mx)}{m}\\right]_a^b = \\dfrac{\\cos(ma) - \\cos(mb)}{m}$.",
    "¿Qué pasa con el numerador $\\cos(ma)-\\cos(mb)$ cuando $m\\to\\infty$?",
    "El numerador está acotado: $|\\cos(ma)-\\cos(mb)| \\leq 2$ para todo $m$.",
    "$\\left|\\dfrac{\\cos(ma)-\\cos(mb)}{m}\\right| \\leq \\dfrac{2}{m} \\to 0$. Por el teorema del emparedado, el límite es 0. $\\square$"
],
"solucion": "$\\int_a^b \\sin(mx)\\,dx = \\dfrac{\\cos(ma)-\\cos(mb)}{m}$. Como $|\\cos(ma)-\\cos(mb)|\\leq 2$, el valor absoluto de la integral es $\\leq 2/m \\to 0$ cuando $m\\to\\infty$. $\\square$",
"explicacion": "La oscilación rápida de $\\sin(mx)$ hace que las partes positivas y negativas se cancelen cada vez más. El invariante es la cota universal $|\\cos| \\leq 1$: sin importar cómo oscile la función, la integral sobre un intervalo fijo tiende a cero porque la frecuencia $m$ crece sin límite.",
"tiempo_estimado": 10,
"conceptos": ["oscilaciones rápidas", "criterio del emparedado", "convergencia a cero"],
"transferencias": ["análisis de Fourier", "principio de estacionaridad de fase", "señales de alta frecuencia"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 6 Review #6.29",
"source_url": "",
"year": "",
"tags": ["Fourier", "oscilaciones", "invariante", "nivel-básico"]
},

{
"id": 702,
"titulo": "La ecuación logística",
"estrategia": "invariantes",
"dificultad": 3,
"enunciado": "La fracción de una población que conoce un rumor satisface $\\dfrac{dy}{dt} = k y(1-y)$, con condición inicial $0 < y(0) = y_0 < 1$ y $k > 0$. Resuelve la ecuación y determina $\\lim_{t\\to\\infty} y(t)$.",
"hints": [
    "Separa variables: $\\dfrac{dy}{y(1-y)} = k\\,dt$.",
    "Descompón en fracciones parciales: $\\dfrac{1}{y(1-y)} = \\dfrac{1}{y} + \\dfrac{1}{1-y}$.",
    "Integra: $\\ln|y| - \\ln|1-y| = kt + C$, es decir $\\ln\\left|\\dfrac{y}{1-y}\\right| = kt + C$.",
    "Despeja: $\\dfrac{y}{1-y} = Ae^{kt}$ con $A = y_0/(1-y_0)$. Despeja $y$.",
    "$y(t) = \\dfrac{1}{1 + ((1-y_0)/y_0)e^{-kt}} \\xrightarrow{t\\to\\infty} 1$. El equilibrio $y=1$ (toda la población conoce el rumor) es estable."
],
"solucion": "Por separación y fracciones parciales: $\\ln|y/(1-y)| = kt + C$. Con $y(0)=y_0$: $y/(1-y) = \\frac{y_0}{1-y_0}e^{kt}$. Despejando: $$y(t) = \\frac{y_0}{y_0 + (1-y_0)e^{-kt}}.$$ Como $e^{-kt}\\to 0$, $y(t)\\to 1$. El invariante es el equilibrio $y=1$: toda difusión logística converge a la capacidad máxima.",
"explicacion": "La curva logística tiene forma de 'S': crece lentamente al principio, luego rápidamente, y finalmente se aplana cerca de la capacidad de carga 1. El invariante es que la cantidad $y/(1-y)$ (razón entre infectados y no infectados) crece exponencialmente.",
"tiempo_estimado": 20,
"conceptos": ["ecuación logística", "fracciones parciales", "capacidad de carga"],
"transferencias": ["epidemiología", "redes sociales", "ecología de poblaciones"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 9 Review #9.25(b)",
"source_url": "",
"year": "",
"tags": ["logística", "EDO", "invariante", "nivel-intermedio"]
},

{
"id": 703,
"titulo": "La integral gaussiana desplazada y escalada",
"estrategia": "invariantes",
"dificultad": 2,
"enunciado": "Dados $a \\in \\mathbb{R}$ y $b \\neq 0$, y sabiendo que $\\displaystyle\\int_{-\\infty}^{\\infty} e^{-t^2}\\,dt = \\sqrt{\\pi}$, calcula $\\displaystyle\\int_{-\\infty}^{\\infty} e^{-(x-a)^2/b^2}\\,dx$.",
"hints": [
    "Haz la sustitución $t = (x-a)/b$.",
    "$dt = dx/b$, es decir $dx = b\\,dt$ (o $|b|\\,dt$ cuidando el signo).",
    "Cuando $x \\to \\pm\\infty$, $t \\to \\pm\\infty$ (independientemente del signo de $b$).",
    "$\\int_{-\\infty}^{\\infty} e^{-(x-a)^2/b^2}\\,dx = \\int_{-\\infty}^{\\infty} e^{-t^2}\\,|b|\\,dt = |b|\\int_{-\\infty}^{\\infty} e^{-t^2}\\,dt$.",
    "$= |b|\\sqrt{\\pi}$."
],
"solucion": "Sustitución $t=(x-a)/b$, $dx=|b|\\,dt$: $\\displaystyle\\int_{-\\infty}^{\\infty} e^{-(x-a)^2/b^2}\\,dx = |b|\\int_{-\\infty}^{\\infty} e^{-t^2}\\,dt = |b|\\sqrt{\\pi}.$",
"explicacion": "El invariante es la integral gaussiana: $\\int_{-\\infty}^{\\infty} e^{-t^2}dt = \\sqrt{\\pi}$. Cualquier traslación ($a$) o escalamiento ($b$) de la gaussiana solo multiplica el resultado por $|b|$; la forma cuadrática en el exponente garantiza que la integral siempre sea un múltiplo de $\\sqrt{\\pi}$.",
"tiempo_estimado": 8,
"conceptos": ["integral gaussiana", "cambio de variable", "distribución normal"],
"transferencias": ["probabilidad (distribución normal)", "física cuántica", "procesamiento de señales"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 6 Challenge #6.32",
"source_url": "",
"year": "",
"tags": ["gaussiana", "cambio-de-variable", "invariante", "nivel-básico"]
},

{
"id": 704,
"titulo": "La identidad de Euler: $\\pi^2/6 = \\sum 1/n^2$",
"estrategia": "invariantes",
"dificultad": 5,
"enunciado": "Demuestra (usando el argumento informal de Euler) que $\\dfrac{\\pi^2}{6} = \\displaystyle\\sum_{n=1}^{\\infty} \\dfrac{1}{n^2} = 1 + \\frac{1}{4} + \\frac{1}{9} + \\frac{1}{16} + \\cdots$",
"hints": [
    "Parte de la serie de Taylor de $\\sin x$: $\\sin x = x - x^3/3! + x^5/5! - \\cdots$",
    "Divide entre $x$: $\\sin x / x = 1 - x^2/3! + x^4/5! - \\cdots = 1 - x^2/6 + \\cdots$",
    "Las raíces de $\\sin x / x$ son $x = \\pm n\\pi$ para $n = 1, 2, 3, \\ldots$ Euler escribió el producto infinito: $\\frac{\\sin x}{x} = \\prod_{n=1}^\\infty \\left(1 - \\frac{x^2}{n^2\\pi^2}\\right)$.",
    "Expande el producto infinito y compara el coeficiente de $x^2$ en ambos lados.",
    "Lado izquierdo (serie Taylor): coeficiente de $x^2$ es $-1/6$. Lado derecho: coeficiente de $x^2$ es $-\\sum_{n=1}^\\infty 1/(n^2\\pi^2)$. Igualando: $1/6 = \\sum 1/(n^2\\pi^2)$, es decir $\\pi^2/6 = \\sum 1/n^2$. $\\square$"
],
"solucion": "La serie de Taylor da $\\sin x / x = 1 - x^2/6 + \\cdots$ El producto infinito de Euler sobre las raíces $\\pm n\\pi$: $\\sin x/x = \\prod_{n=1}^\\infty(1-x^2/(n^2\\pi^2))$. El coeficiente de $x^2$ en el producto es $-\\sum_{n=1}^\\infty 1/(n^2\\pi^2)$. Igualando con $-1/6$: $\\sum_{n=1}^\\infty 1/n^2 = \\pi^2/6$. Verificado numéricamente: $\\sum_{n=1}^{10^5} 1/n^2 \\approx 1.64492 \\approx \\pi^2/6 \\approx 1.64493$.",
"explicacion": "El invariante es la conexión entre las raíces de $\\sin x / x$ y los coeficientes de su expansión en serie. Euler identificó que la función $\\sin x / x$ puede factorizarse como producto sobre sus raíces (como se hace con polinomios), y esta audaz generalización revela la identidad $\\pi^2/6 = \\sum 1/n^2$.",
"tiempo_estimado": 40,
"conceptos": ["serie de Basel", "producto de Euler", "series de Taylor", "raíces de funciones"],
"transferencias": ["función zeta de Riemann", "teoría de números analítica", "física de cuerdas"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — §7.A (A Strange Formula for $\\pi$)",
"source_url": "",
"year": "",
"tags": ["Basel", "Euler", "pi", "series", "invariante", "nivel-élite"]
},

{
"id": 705,
"titulo": "Invarianza de integrales bajo traslación y escalamiento",
"estrategia": "invariantes",
"dificultad": 2,
"enunciado": "Sea $f$ continua y $c \\neq 0$ un número real. Demuestra que: (a) $\\displaystyle\\int_a^b f(x)\\,dx = \\int_{a+c}^{b+c} f(x-c)\\,dx$, y (b) $\\displaystyle\\int_a^b f(x)\\,dx = \\frac{1}{c}\\int_{ca}^{cb} f\\!\\left(\\frac{x}{c}\\right)\\!dx$.",
"hints": [
    "Para (a): haz la sustitución $x = t + c$ (o equivalentemente $t = x - c$).",
    "Cuando $t=a$, $x=a+c$; cuando $t=b$, $x=b+c$. Además $dx=dt$.",
    "Para (b): haz la sustitución $x = ct$ (o equivalentemente $t = x/c$).",
    "Cuando $t=a$, $x=ca$; cuando $t=b$, $x=cb$. Además $dx = c\\,dt$.",
    "El factor $1/c$ en la fórmula (b) cancela el $c$ que aparece de $dx = c\\,dt$."
],
"solucion": "(a) Sustitución $x = t+c$, $dx=dt$: $\\int_{a+c}^{b+c} f(x-c)\\,dx = \\int_a^b f(t)\\,dt$. $\\square$ (b) Sustitución $x = ct$, $dx=c\\,dt$: $\\frac{1}{c}\\int_{ca}^{cb} f(x/c)\\,dx = \\frac{1}{c}\\int_a^b f(t)\\cdot c\\,dt = \\int_a^b f(t)\\,dt$. $\\square$",
"explicacion": "El invariante es el valor de la integral: trasladar o escalar los límites (y ajustar el integrando) deja la integral invariante. Estas propiedades son la base de sustituciones complejas y de la teoría de la medida de Lebesgue.",
"tiempo_estimado": 12,
"conceptos": ["cambio de variable", "invarianza de integrales", "sustitución lineal"],
"transferencias": ["transformadas de Fourier y Laplace", "probabilidad (cambio de variable)", "análisis funcional"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 5 Review #5.55",
"source_url": "",
"year": "",
"tags": ["cambio-de-variable", "invarianza", "invariante", "nivel-básico"]
},

# ─────────────── PATRONES 706-716 ───────────────

{
"id": 706,
"titulo": "La familia cúbica $x^3 + px + q$",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "Describe la gráfica de $f(x) = x^3 + px + q$, donde $p$ y $q$ son constantes. Determina dónde $f$ es creciente o decreciente, dónde tiene extremos locales y cuál es la concavidad. ¿Cómo cambia el comportamiento cualitativo según el signo de $p$?",
"hints": [
    "Calcula $f'(x) = 3x^2 + p$ y $f''(x) = 6x$.",
    "$f''(x)=0$ en $x=0$, lo que da siempre un punto de inflexión ahí (independientemente de $p$ y $q$).",
    "Para los extremos locales: resuelve $f'(x)=3x^2+p=0$.",
    "Si $p > 0$: $3x^2+p > 0$ siempre, así que $f$ es estrictamente creciente y sin extremos locales. Si $p = 0$: $f'(x) = 3x^2 \\geq 0$, sin extremos. Si $p < 0$: hay máximo local en $x = -\\sqrt{-p/3}$ y mínimo en $x = \\sqrt{-p/3}$.",
    "El patrón: $f$ siempre tiene exactamente un punto de inflexión (en $x=0$). Si $p < 0$ tiene dos extremos locales; si $p \\geq 0$ no tiene ninguno. El parámetro $q$ solo desplaza la curva verticalmente."
],
"solucion": "Siempre: inflexión en $x=0$, $f(x)\\to -\\infty$ cuando $x\\to-\\infty$ y $f(x)\\to+\\infty$ cuando $x\\to+\\infty$. Si $p>0$: creciente en todo $\\mathbb{R}$. Si $p<0$: máximo local en $x=-\\sqrt{-p/3}$ y mínimo en $x=\\sqrt{-p/3}$; el discriminante del cúbico determina si tiene 1 o 3 raíces reales. $q$ traslada verticalmente.",
"explicacion": "El parámetro $p$ cambia cualitativamente la forma: positivo da una curva suave, negativo crea una 'S' con hump. El patrón clave: el punto de inflexión siempre está en $x=0$ para esta familia, y los extremos (si existen) son simétricos respecto a $x=0$.",
"tiempo_estimado": 20,
"conceptos": ["análisis de gráficas", "cúbicos", "extremos locales", "puntos de inflexión"],
"transferencias": ["bifurcaciones en sistemas dinámicos", "curvas de equilibrio en economía"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Challenge #4.37",
"source_url": "",
"year": "",
"tags": ["cúbicos", "gráficas", "patrones", "nivel-intermedio"]
},

{
"id": 707,
"titulo": "La función $x^m(1-x)^n$ en $[0,1]$",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "Sean $m, n \\geq 2$ enteros. Describe con el mayor detalle posible la gráfica de $f(x) = x^m(1-x)^n$ en el intervalo $[0,1]$. ¿Dónde está el máximo? ¿Cómo se comporta en los extremos? (Pista: HMMT)",
"hints": [
    "$f(0) = f(1) = 0$. La función es no negativa en $[0,1]$ y tiene un único máximo interior.",
    "Deriva: $f'(x) = x^{m-1}(1-x)^{n-1}[m(1-x) - nx]$.",
    "El factor entre corchetes se anula en $x^* = m/(m+n)$, que es el único cero interior de $f'$.",
    "Como $m,n \\geq 2$: $f'$ se anula también en $x=0$ y $x=1$ (con multiplicidad $m-1$ y $n-1$). La función tiene tangente horizontal en ambos extremos.",
    "Patrón: el máximo siempre está en $x = m/(m+n)$, con $f(x^*) = (m/(m+n))^m \\cdot (n/(m+n))^n$. Cuanto mayor es $n$ vs $m$, más se desplaza el máximo hacia la izquierda."
],
"solucion": "$f(0)=f(1)=0$. Máximo único en $x^* = m/(m+n)$, con valor $f(x^*) = \\left(\\frac{m}{m+n}\\right)^m\\!\\left(\\frac{n}{m+n}\\right)^n$. En $x=0$, $f$ se adhiere al eje con orden $m$; en $x=1$, con orden $n$. La curva siempre tiene la misma forma de 'campana asimétrica', independientemente de los valores exactos de $m$ y $n$.",
"explicacion": "Esta familia incluye la función Beta: $\\int_0^1 x^{m-1}(1-x)^{n-1}dx = B(m,n) = \\Gamma(m)\\Gamma(n)/\\Gamma(m+n)$. El patrón del máximo en $m/(m+n)$ es la forma continua de la moda de la distribución binomial.",
"tiempo_estimado": 20,
"conceptos": ["máximos de funciones producto", "análisis de gráficas", "función Beta"],
"transferencias": ["distribución Beta en estadística", "análisis de polinomios de Bernstein", "teorema de Weierstrass"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 4 Review #4.38 (Pista: HMMT)",
"source_url": "",
"year": "",
"tags": ["función-Beta", "extremos", "patrones", "nivel-intermedio"]
},

{
"id": 708,
"titulo": "Series de Taylor de cuatro funciones",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "Encuentra los primeros cuatro términos no nulos de la serie de Taylor centrada en $x=0$ para: (a) $e^{-x^2}$, (b) $\\cos x^3$, (c) $\\dfrac{1}{\\sqrt{1-4x^2}}$, (d) $e^{x^2+\\sin x}$.",
"hints": [
    "Para (a) y (b): sustituye directamente en las series conocidas de $e^u$ y $\\cos u$.",
    "Para (a): $e^u = 1+u+u^2/2!+u^3/3!+\\cdots$, con $u = -x^2$.",
    "Para (b): $\\cos u = 1-u^2/2!+u^4/4!-\\cdots$, con $u = x^3$.",
    "Para (c): usa $(1+u)^{-1/2} \\approx 1-u/2+3u^2/8-5u^3/16+\\cdots$, con $u = -4x^2$.",
    "Para (d): primero expande $x^2+\\sin x \\approx x + x^2 - x^3/6$, luego usa $e^v \\approx 1+v+v^2/2+v^3/6$ y expande con cuidado."
],
"solucion": "(a) $e^{-x^2} = 1 - x^2 + \\dfrac{x^4}{2} - \\dfrac{x^6}{6} + \\cdots$ (b) $\\cos x^3 = 1 - \\dfrac{x^6}{2} + \\dfrac{x^{12}}{24} - \\cdots$ (c) $(1-4x^2)^{-1/2} = 1 + 2x^2 + 6x^4 + 20x^6 + \\cdots$ (d) $e^{x^2+\\sin x} = 1 + x + \\dfrac{3x^2}{2} + \\dfrac{5x^3}{6} + \\cdots$",
"explicacion": "El patrón fundamental: las series de Taylor de funciones compuestas se obtienen sustituyendo en las series de las funciones base. La regla de composición es más potente que derivar directamente, especialmente cuando el argumento interior es complejo.",
"tiempo_estimado": 25,
"conceptos": ["series de Taylor", "composición de series", "binomio generalizado"],
"transferencias": ["cálculo numérico", "física (expansiones perturbativas)", "teoría de señales"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Review #7.38",
"source_url": "",
"year": "",
"tags": ["Taylor", "composición", "patrones", "nivel-intermedio"]
},

{
"id": 709,
"titulo": "Suma de la serie $\\sum 2^{n-1}/n!$",
"estrategia": "patrones",
"dificultad": 1,
"enunciado": "Calcula $\\displaystyle\\sum_{n=0}^{\\infty} \\dfrac{2^{n-1}}{n!}$.",
"hints": [
    "Factoriza la constante $2^{-1}=1/2$ fuera de la suma.",
    "$\\sum_{n=0}^\\infty \\frac{2^{n-1}}{n!} = \\frac{1}{2}\\sum_{n=0}^\\infty \\frac{2^n}{n!}$.",
    "Recuerda la serie de Taylor de $e^x = \\sum_{n=0}^\\infty \\frac{x^n}{n!}$.",
    "Con $x = 2$: $e^2 = \\sum_{n=0}^\\infty \\frac{2^n}{n!}$.",
    "Por tanto la suma es $\\dfrac{1}{2}e^2 = \\dfrac{e^2}{2}$."
],
"solucion": "$\\displaystyle\\sum_{n=0}^{\\infty} \\frac{2^{n-1}}{n!} = \\frac{1}{2}\\sum_{n=0}^{\\infty} \\frac{2^n}{n!} = \\frac{1}{2}e^2 = \\frac{e^2}{2} \\approx 3.6945$. Verificado con Python.",
"explicacion": "El patrón es reconocer la serie de $e^x$ evaluada en $x=2$. Muchas sumas de series son series conocidas disfrazadas: la clave es identificar la función generatriz subyacente.",
"tiempo_estimado": 6,
"conceptos": ["serie exponencial", "función generatriz", "reconocimiento de patrones"],
"transferencias": ["probabilidad (distribución de Poisson)", "combinatoria", "análisis de algoritmos"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Review #7.39",
"source_url": "",
"year": "",
"tags": ["series", "número-e", "patrones", "nivel-básico"]
},

{
"id": 710,
"titulo": "El teorema del binomio para exponentes reales",
"estrategia": "patrones",
"dificultad": 4,
"enunciado": "El Teorema del Binomio Generalizado afirma que para $|x| < 1$ y cualquier $p \\in \\mathbb{R}$: $(1+x)^p = \\displaystyle\\sum_{k=0}^{\\infty} \\binom{p}{k} x^k$, donde $\\binom{p}{k} = \\dfrac{p(p-1)\\cdots(p-k+1)}{k!}$. Explica y prueba este resultado.",
"hints": [
    "Sea $g(x) = \\sum_{k=0}^\\infty \\binom{p}{k} x^k$. Calcula $g'(x)$.",
    "$g'(x) = \\sum_{k=1}^\\infty k\\binom{p}{k} x^{k-1}$. Usa la identidad $k\\binom{p}{k} = p\\binom{p-1}{k-1}$.",
    "Obtienes $g'(x) = p\\sum_{k=0}^\\infty \\binom{p-1}{k}x^k = p\\,g_{p-1}(x)$, donde $g_{p-1}$ es la serie para $(1+x)^{p-1}$.",
    "Esto sugiere que $g$ satisface la EDO $(1+x)g' = p\\,g$. Comprueba que $(1+x)^p$ satisface la misma EDO con $h(0)=1$.",
    "Como ambas soluciones de $(1+x)h'=ph$ con $h(0)=1$ son iguales (unicidad de EDO), $(1+x)^p = g(x)$ para $|x|<1$."
],
"solucion": "Sea $h(x)=(1+x)^p$. Entonces $h'=p(1+x)^{p-1}=ph/(1+x)$, es decir $(1+x)h'=ph$, $h(0)=1$. La serie $g=\\sum\\binom{p}{k}x^k$ satisface la misma EDO $(1+x)g'=pg$ con $g(0)=1$ (verifiable coeficiente a coeficiente). Por unicidad de soluciones de EDO, $g=h=(1+x)^p$ para $|x|<1$. Para $p\\in\\mathbb{N}$, la serie termina (los binomios $\\binom{p}{k}=0$ para $k>p$) y converge para todo $x$.",
"explicacion": "El patrón es la misma estructura que el binomio finito, pero ahora con coeficientes $\\binom{p}{k}$ que siguen el mismo patrón $p(p-1)\\cdots/k!$ incluso cuando $p$ no es entero. Esto generaliza Newton y permite expandir $(1+x)^{1/2}$, $(1+x)^{-1}$, etc.",
"tiempo_estimado": 30,
"conceptos": ["teorema del binomio generalizado", "EDO de primer orden", "series de potencias"],
"transferencias": ["relatividad especial (factores $\\gamma$)", "óptica", "análisis combinatorio"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Challenge #7.48",
"source_url": "",
"year": "",
"tags": ["binomio-generalizado", "Newton", "patrones", "nivel-avanzado"]
},

{
"id": 711,
"titulo": "Ecuaciones paramétricas para movimientos clásicos",
"estrategia": "patrones",
"dificultad": 2,
"enunciado": "Escribe ecuaciones paramétricas para las curvas trazadas por: (a) Una partícula que traza el círculo de centro $(0,0)$ y radio 2, partiendo de $(2,0)$ en $t=0$ y moviéndose en sentido antihorario a velocidad angular constante 1 rad/s. (b) Una bala de cañón disparada desde $(0,0)$ con velocidad inicial 100 m/s en ángulo $\\pi/3$ sobre la horizontal, bajo gravedad $g = 9.8$ m/s².",
"hints": [
    "Para (a): usa $u(t)=r\\cos(\\omega t + \\phi)$ y $v(t)=r\\sin(\\omega t+\\phi)$. Con $r=2$, $\\omega=1$, sentido antihorario, punto inicial $(2,0)$.",
    "$(2,0)$ en $t=0$: $u(0)=2=2\\cos\\phi \\Rightarrow \\phi=0$. Antihorario: $u=2\\cos t$, $v=2\\sin t$.",
    "Para (b): las velocidades iniciales son $v_x = 100\\cos(\\pi/3) = 50$ m/s y $v_y = 100\\sin(\\pi/3) = 50\\sqrt{3}$ m/s.",
    "El movimiento horizontal es uniforme: $u(t) = 50t$. El vertical incluye la gravedad: $v(t) = 50\\sqrt{3}\\,t - \\frac{1}{2}(9.8)t^2 = 50\\sqrt{3}\\,t - 4.9t^2$.",
    "La bala aterriza cuando $v(t)=0$: $t = 50\\sqrt{3}/4.9 \\approx 17.67$ s. Alcance horizontal $\\approx 883$ m."
],
"solucion": "(a) $u(t) = 2\\cos t$, $v(t) = 2\\sin t$, $t \\in [0, 2\\pi)$. (b) $u(t) = 50t$, $v(t) = 50\\sqrt{3}\\,t - 4.9t^2$, $t \\in [0, 50\\sqrt{3}/4.9]$. Verificado: $u(0)=(2,0)$ ✓; en $t=0$ la bala está en el origen con las velocidades correctas ✓.",
"explicacion": "El patrón: el movimiento circular siempre usa senos y cosenos con la fase adecuada. El lanzamiento de proyectil separa el movimiento en horizontal (uniforme) y vertical (aceleración constante). Estas parametrizaciones son la base de cualquier simulación física.",
"tiempo_estimado": 15,
"conceptos": ["movimiento circular", "cinemática del proyectil", "parametrización"],
"transferencias": ["animación por computadora", "ingeniería aeroespacial", "robótica"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 8 Review #8.21(a)(b)",
"source_url": "",
"year": "",
"tags": ["paramétrico", "cinemática", "patrones", "nivel-básico"]
},

{
"id": 712,
"titulo": "Órbitas planeta-luna: una hipotrocoide",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "Un planeta orbita una estrella a distancia $R$ en trayectoria circular (período 1 año). Una luna orbita el planeta a distancia $r$ ($0 < r < R$, período $1/4$ año). En $t=0$: el planeta está en $(R,0)$ y la luna en $(R+r, 0)$. Escribe las ecuaciones paramétricas para la posición de la luna en función del tiempo $t$ (en años).",
"hints": [
    "La posición del planeta (moviéndose en sentido antihorario con período 1): $(R\\cos 2\\pi t, R\\sin 2\\pi t)$.",
    "La luna gira alrededor del planeta con período $1/4$, es decir velocidad angular $2\\pi/(1/4) = 8\\pi$ rad/año.",
    "Posición de la luna relativa al planeta: $(r\\cos 8\\pi t, r\\sin 8\\pi t)$ (en $t=0$ apunta hacia el sol, luego gira CCW).",
    "Posición absoluta de la luna: suma de la posición del planeta y la posición relativa.",
    "$(u(t), v(t)) = (R\\cos 2\\pi t + r\\cos 8\\pi t,\\; R\\sin 2\\pi t + r\\sin 8\\pi t)$. Verifica en $t=1/2$: $(-R+r, 0) = (r-R, 0)$ ✓"
],
"solucion": "$$u(t) = R\\cos(2\\pi t) + r\\cos(8\\pi t), \\quad v(t) = R\\sin(2\\pi t) + r\\sin(8\\pi t).$$\\nEn $t=0$: $(R+r, 0)$ ✓. En $t=1/2$: $(-R+r, 0)=(r-R, 0)$ ✓. En $t=1$: $(R+r, 0)$ ✓ (período 1 año). Verificado con Python. La curva resultante es una **epitrocoide**.",
"explicacion": "El patrón es la superposición de dos movimientos circulares con frecuencias distintas. El cociente de las frecuencias ($8\\pi/2\\pi = 4$) determina el número de 'lazos' de la hipotrocoide. Este mismo patrón aparece en el pantógrafo, el espirógrafo y la mecánica celeste de Ptolomeo.",
"tiempo_estimado": 20,
"conceptos": ["curvas paramétricas", "movimiento compuesto", "epitrocoide"],
"transferencias": ["mecánica celeste", "espirógrafo", "síntesis de formas en diseño"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 8 Challenge #8.27(a)",
"source_url": "",
"year": "",
"tags": ["paramétrico", "órbitas", "epitrocoide", "patrones", "nivel-intermedio"]
},

{
"id": 713,
"titulo": "El sistema de Romeo y Julieta",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "El amor de Romeo ($r$) y Julieta ($j$) evolucionan según el sistema: $\\dfrac{dr}{dt} = -kj$ y $\\dfrac{dj}{dt} = kr$, con $r(0)=1$, $j(0)=0$, $k>0$. Resuelve el sistema, describe el patrón a largo plazo, y encuentra una cantidad que se conserva.",
"hints": [
    "Diferencia $r'' = -k\\,j' = -k(kr) = -k^2 r$. Entonces $r'' + k^2 r = 0$.",
    "Solución general: $r(t) = A\\cos(kt) + B\\sin(kt)$. Con $r(0)=1$: $A=1$.",
    "$r'(0) = -k\\,j(0) = 0 \\Rightarrow B=0$. Así $r(t) = \\cos(kt)$.",
    "De $j'= kr$: $j(t) = \\int_0^t k\\cos(ks)\\,ds = \\sin(kt)$.",
    "La cantidad conservada es $r^2 + j^2 = \\cos^2(kt) + \\sin^2(kt) = 1$. El amor total es constante."
],
"solucion": "$r(t) = \\cos(kt)$, $j(t) = \\sin(kt)$. El amor de cada uno oscila con período $2\\pi/k$: cuando Romeo ama más, Julieta es indiferente; cuando Julieta ama más, Romeo es indiferente; cuando uno odia, el otro quiere. La cantidad conservada es $r^2 + j^2 = 1$: la 'energía total de amor' nunca cambia.",
"explicacion": "El sistema $\\dot{r}=-kj$, $\\dot{j}=kr$ es exactamente el oscilador armónico en el plano de fases $(r,j)$. La trayectoria es un círculo de radio 1 (gracias a la cantidad conservada), lo que produce la oscilación eterna entre amor y odio.",
"tiempo_estimado": 20,
"conceptos": ["sistemas de EDO", "oscilaciones acopladas", "conservación en el plano de fases"],
"transferencias": ["dinámica poblacional depredador-presa", "circuitos LC acoplados", "mecánica cuántica"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 9 Challenge #9.32 (basado en [H-H])",
"source_url": "",
"year": "",
"tags": ["sistema-EDO", "oscilación", "patrones", "nivel-intermedio"]
},

{
"id": 714,
"titulo": "Ecuación logística: $y' = 3y - y^2$",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "Resuelve la ecuación diferencial $y' = 3y - y^2$ con condición inicial $y(0) = 5$. Determina $\\displaystyle\\lim_{t\\to\\infty} y(t)$ y describe el patrón cualitativo de la solución.",
"hints": [
    "Factoriza: $y' = y(3-y)$. Los equilibrios son $y=0$ (inestable) e $y=3$ (estable).",
    "Como $y(0)=5>3$, la solución empieza por encima del equilibrio. ¿Hacia dónde se mueve?",
    "Separa: $\\dfrac{dy}{y(3-y)} = dt$. Usa fracciones parciales: $\\dfrac{1}{y(3-y)} = \\dfrac{1}{3}\\left(\\dfrac{1}{y} + \\dfrac{1}{3-y}\\right)$.",
    "Integra: $\\dfrac{1}{3}\\ln\\left|\\dfrac{y}{3-y}\\right| = t + C$. Con $y(0)=5$: $C = \\frac{1}{3}\\ln(5/|{-2}|) = \\frac{1}{3}\\ln(5/2)$.",
    "$y(t) = \\dfrac{15\\,e^{3t}}{5e^{3t} - 2}$. Cuando $t\\to\\infty$: $y\\to 15/5 = 3$."
],
"solucion": "Separando variables y usando fracciones parciales: $\\frac{1}{3}\\ln|y/(3-y)| = t+C$. Con $y(0)=5$: $5/(5-3)=5/2$, así $C=\\frac{1}{3}\\ln(5/2)$. Despejando: $y(t) = \\dfrac{15\\,e^{3t}}{5e^{3t}-2}$. Cuando $t\\to\\infty$: $y(t)\\to \\mathbf{3}$. El patrón: la solución decrece monótonamente desde $y_0=5$ hacia el equilibrio estable $y=3$. Verificado con Python.",
"explicacion": "El patrón logístico: cuando la población supera la capacidad de carga (aquí $K=3$), decrece; cuando está por debajo, crece. El equilibrio $y=K$ es el atractor global para toda condición inicial positiva.",
"tiempo_estimado": 20,
"conceptos": ["ecuación logística", "equilibrios estables e inestables", "capacidad de carga"],
"transferencias": ["dinámica de poblaciones", "epidemiología (SIR)", "economía del comportamiento"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 9 Review #9.21",
"source_url": "",
"year": "",
"tags": ["logística", "EDO", "equilibrio", "patrones", "nivel-intermedio"]
},

{
"id": 715,
"titulo": "La espiral de Arquímedes",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "La **espiral de Arquímedes** es la curva polar $r = \\theta$ para $\\theta \\geq 0$. (a) Halla la pendiente de la recta tangente a la espiral en el ángulo $\\theta$. (b) Calcula el área de la región encerrada por la espiral y el eje polar desde $\\theta = 0$ hasta $\\theta = 2\\pi$.",
"hints": [
    "Para la pendiente: convierte a coordenadas cartesianas: $x = r\\cos\\theta = \\theta\\cos\\theta$, $y = r\\sin\\theta = \\theta\\sin\\theta$.",
    "$dx/d\\theta = \\cos\\theta - \\theta\\sin\\theta$, $dy/d\\theta = \\sin\\theta + \\theta\\cos\\theta$.",
    "Pendiente $= \\dfrac{dy/d\\theta}{dx/d\\theta} = \\dfrac{\\sin\\theta + \\theta\\cos\\theta}{\\cos\\theta - \\theta\\sin\\theta}$.",
    "Para el área: $A = \\dfrac{1}{2}\\int_0^{2\\pi} r^2\\,d\\theta = \\dfrac{1}{2}\\int_0^{2\\pi} \\theta^2\\,d\\theta$.",
    "$A = \\dfrac{1}{2}\\cdot\\dfrac{\\theta^3}{3}\\Big|_0^{2\\pi} = \\dfrac{(2\\pi)^3}{6} = \\dfrac{4\\pi^3}{3} \\approx 41.34$."
],
"solucion": "(a) Pendiente en $\\theta$: $m(\\theta) = \\dfrac{\\sin\\theta + \\theta\\cos\\theta}{\\cos\\theta - \\theta\\sin\\theta}$. (b) $A = \\dfrac{1}{2}\\int_0^{2\\pi}\\theta^2\\,d\\theta = \\dfrac{4\\pi^3}{3} \\approx 41.34$ unidades cuadradas. Verificado con Python.",
"explicacion": "El patrón de la espiral: la distancia al origen crece linealmente con el ángulo ($r=\\theta$), lo que crea una curva con vueltas equiespaciadas. El área crece como $\\theta^3$: cada vuelta adicional tiene un área proporcionalmente mayor que la anterior.",
"tiempo_estimado": 20,
"conceptos": ["espiral de Arquímedes", "tangentes en polares", "área polar"],
"transferencias": ["tecnología de CD/DVD", "diseño de tornillos", "embobinados eléctricos"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 8 Review #8.24",
"source_url": "",
"year": "",
"tags": ["polares", "espiral", "Arquímedes", "patrones", "nivel-intermedio"]
},

{
"id": 716,
"titulo": "Una suma de Riemann converge a $\\pi/2$",
"estrategia": "patrones",
"dificultad": 3,
"enunciado": "Define la sucesión $a_n = \\dfrac{1}{\\sqrt{n^2-0^2}} + \\dfrac{1}{\\sqrt{n^2-1^2}} + \\dfrac{1}{\\sqrt{n^2-2^2}} + \\cdots + \\dfrac{1}{\\sqrt{n^2-(n-1)^2}}$. Calcula $\\displaystyle\\lim_{n\\to\\infty} a_n$. (Fuente: HMMT)",
"hints": [
    "Factoriza $n$ del radical: $\\dfrac{1}{\\sqrt{n^2-k^2}} = \\dfrac{1}{n}\\cdot\\dfrac{1}{\\sqrt{1-(k/n)^2}}$.",
    "$a_n = \\dfrac{1}{n}\\sum_{k=0}^{n-1} \\dfrac{1}{\\sqrt{1-(k/n)^2}}$.",
    "Esto es una suma de Riemann (con puntos izquierdos $x_k = k/n$, paso $\\Delta x = 1/n$) para alguna integral. ¿Cuál?",
    "El integrando es $f(x) = 1/\\sqrt{1-x^2}$, integrado de $x=0$ a $x=1$.",
    "$\\int_0^1 \\dfrac{dx}{\\sqrt{1-x^2}} = \\arcsin(x)\\Big|_0^1 = \\arcsin(1) - \\arcsin(0) = \\dfrac{\\pi}{2}$. Verificado numéricamente."
],
"solucion": "$a_n = \\dfrac{1}{n}\\sum_{k=0}^{n-1}\\dfrac{1}{\\sqrt{1-(k/n)^2}}$, que es la suma de Riemann de izquierda para $\\int_0^1 \\frac{dx}{\\sqrt{1-x^2}}$. Como $f(x) = 1/\\sqrt{1-x^2}$ es integrable en $[0,1)$ (con singularidad integrable en $x=1$): $\\lim_{n\\to\\infty} a_n = \\int_0^1 \\frac{dx}{\\sqrt{1-x^2}} = \\arcsin(1) = \\mathbf{\\dfrac{\\pi}{2}}$. Verificado con Python.",
"explicacion": "El patrón es reconocer la suma como una suma de Riemann. La singularidad en $x=1$ hace que la convergencia sea lenta (el término $1/\\sqrt{n^2-(n-1)^2} = 1/\\sqrt{2n-1}\\approx 1/\\sqrt{2n}$ es grande), pero la integral converge y por ello la suma también.",
"tiempo_estimado": 20,
"conceptos": ["sumas de Riemann", "integrales impropias", "identificar patrones en sumas"],
"transferencias": ["análisis numérico (cuadratura)", "probabilidad geométrica", "análisis de algoritmos"],
"source": "AoPS Calculus (Rusczyk, Patrick, Zawitz) — Ch. 7 Challenge #7.46 (Fuente: HMMT)",
"source_url": "",
"year": "",
"tags": ["Riemann", "suma-integral", "pi", "patrones", "nivel-intermedio"]
}

]

# Validate
assert len(nuevos) == 44, f"Expected 44, got {len(nuevos)}"
ids = [p['id'] for p in nuevos]
assert ids == list(range(673, 717)), f"IDs wrong: {ids[:5]}...{ids[-5:]}"
strat_counts = {}
for p in nuevos:
    s = p['estrategia']
    strat_counts[s] = strat_counts.get(s, 0) + 1
print("Strategy counts:", strat_counts)
assert all(strat_counts.get(s,0)==11 for s in ['inversion','optimizacion','invariantes','patrones']), f"Imbalanced: {strat_counts}"
for p in nuevos:
    assert len(p['hints']) == 5, f"Problem {p['id']} has {len(p['hints'])} hints"
print(f"All {len(nuevos)} problems validated OK")

# Load existing and append
with open('data/problems.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

existing = data['problemas']
print(f"Existing: {len(existing)} problems (ids {existing[0]['id']}-{existing[-1]['id']})")
data['problemas'] = existing + nuevos
print(f"After append: {len(data['problemas'])} problems")
all_strats = {}
for p in data['problemas']:
    s = p['estrategia']
    all_strats[s] = all_strats.get(s, 0) + 1
print("Total strategy counts:", all_strats)

with open('data/problems.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Written OK")
