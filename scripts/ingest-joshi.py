#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ingesta tanda 4: Quant Job Interview (Mark Joshi) → study.json.
Idempotente: aborta si arena-q8 ya existe. Re-ejecutable tras un rollback."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'data', 'study.json')
LIBRO = "Quant Job Interview Questions and Answers (Joshi, Denson & Downes)"

with open(SP, encoding='utf-8') as f:
    s = json.load(f)

if any(u['id'] == 'arena-q8' for u in s['unidades']):
    print("arena-q8 ya existe — nada que hacer (idempotente).")
    sys.exit(0)

# ---- Heurísticas nuevas ----
nuevas_heur = [
    {"id": "parada-optima", "nombre": "Parada óptima",
     "descripcion": "Resuelve hacia atrás y quédate con el valor inmediato solo si supera la esperanza de continuar."},
    {"id": "martingala-parada", "nombre": "Martingala y muestreo opcional",
     "descripcion": "Si una cantidad es martingala, su esperanza en un tiempo de parada de esperanza finita iguala su valor inicial."},
    {"id": "conservacion", "nombre": "Conservación",
     "descripcion": "Sigue una cantidad que no cambia (masa, volumen, conteo de piezas) para resolver sin álgebra."},
    {"id": "desdoblar", "nombre": "Desdoblar la geometría",
     "descripcion": "Aplana o reconfigura una figura 3D en 2D para convertir un problema espacial en uno plano."},
]
ids_heur = {h['id'] for h in s['catalogoHeuristicas']}
for h in nuevas_heur:
    if h['id'] not in ids_heur:
        s['catalogoHeuristicas'].append(h)

META = {"nivel": "intermedio", "fuente": LIBRO, "session": "2026-06-13"}

def unidad(uid, orden, titulo, objetivo, heur, skills, ideas, banco):
    return {
        "id": uid, "bloque": "fase-7", "orden": orden, "titulo": titulo,
        "libro": LIBRO, "lectura": f"data/teoria/{uid}.md",
        "dosis": f"{len(banco)} preguntas · destiladas de Joshi (entrevistas reales)",
        "objetivo": objetivo, "heuristicas": heur,
        "metadata": {"ruta": "quant", "nivel": "intermedio", "skills": skills,
                     "fuente": LIBRO, "session": "2026-06-13"},
        "ideas_clave": ideas, "banco": banco,
    }

def q(uid, n, tipo, enun, sol, exp):
    return {"id": f"{uid}-q{n}", "tipo": tipo, "enunciado": enun,
            "solucion": sol, "explicacion": exp}

unidades = []

# ===================== arena-q8 =====================
uid = "arena-q8"
banco = [
 q(uid,1,"quiz",
   "Tiras un dado justo hasta 3 veces; en cada tiro puedes quedarte con el número (en dólares) o volver a tirar. ¿Cuál es tu ganancia esperada bajo la estrategia óptima?",
   "14/3 ≈ 4.67. Resuelve hacia atrás: con 1 tiro E=3.5. Con 2 tiros te quedas con el primero si sale 4,5 o 6: E(2)=(6+5+4)/6+(3/6)·3.5=4.25. Con 3 tiros te quedas si sale 5 o 6: E(3)=(6+5)/6+(4/6)·4.25=14/3.",
   "Es valorar una opción americana sobre un árbol multinomial. La regla: en cada nodo te quedas con el valor inmediato solo si supera la esperanza de continuar."),
 q(uid,2,"quiz",
   "Cuatro cajas selladas; una contiene $100 y el resto están vacías. Pagas X por abrir una caja y tomar su contenido; puedes seguir jugando. ¿Qué X hace el juego justo?",
   "X=40. Bajo la estrategia óptima sigues abriendo hasta encontrar los $100, así que siempre ganas $100. E(coste)=X·(1·¼+2·¼+3·¼+4·¼) con las probabilidades condicionales = 2.5X. Igualando 100=2.5X → X=40.",
   "El número esperado de cajas abiertas hasta acertar (sin reposición sobre 4) es 2.5. Juego justo: E(coste)=E(premio)."),
 q(uid,3,"acertijo",
   "Yo elijo un número n de 1 a 100. Si lo adivinas te pago $n; si no, nada. ¿Cuánto pagarías por jugar?",
   "≈ $0.193 = (Σ_{j=1}^{100} 1/j)^{-1}. Es teoría de juegos: la estrategia óptima elige k con probabilidad ∝ 1/k, lo que hace la ganancia esperada independiente de la jugada del rival e igual a 1/H₁₀₀, con H₁₀₀≈5.187.",
   "El valor decrece al crecer el rango. Elegir proporcional a 1/k equilibra 'pago pequeño' contra 'más probable de coincidir'."),
 q(uid,4,"quiz",
   "Empiezas con $1. Lanzas una moneda justa infinitas veces: en cara tu posición se duplica, en cruz se reduce a la mitad. ¿Cuál es el valor esperado del dinero?",
   "Diverge a infinito. Por tiro, E(factor)=½·2+½·½=5/4>1, y por independencia E(producto)=(5/4)ⁿ → ∞.",
   "Paradoja: casi toda trayectoria tiende a 0 (la mediana baja), pero la media la dominan trayectorias raras con muchísimas caras. Media ≠ comportamiento típico."),
 q(uid,5,"quiz",
   "Lanzas una moneda justa hasta que sale cara; N es el número de tiros (incluyendo la cara final). Calcula E(N) y Var(N).",
   "E(N)=2 y Var(N)=2. N es geométrica con P(N=k)=0.5ᵏ. E(N)=Σk·0.5ᵏ=2 (suma por diferencias); E(N²)=6 → Var=E(N²)−E(N)²=6−4=2.",
   "El truco 'multiplica la serie por 0.5 y resta' evita memorizar fórmulas. Geométrica: E=1/p, Var=(1−p)/p²; con p=½ ambas valen 2."),
 q(uid,6,"quiz",
   "Con una moneda justa, el juego para cuando aparecen dos caras (CC) o dos cruces (XX) consecutivas. ¿Tiempo esperado hasta que para?",
   "3 tiros. Tras el primer tiro, faltan k−1 tiros 'determinados' para parar: P(N=k)=0.5^{k−1} para k≥2, y E(N)=Σ k·0.5^{k−1}=3.",
   "Equivale a: tira la primera, y luego cada tiro tiene prob ½ de repetir el anterior y parar → 1 + (tiros extra geométricos con p=½) = 1 + 2 = 3."),
 q(uid,7,"quiz",
   "¿Número esperado de lanzamientos de una moneda justa para obtener tres caras seguidas?",
   "14. Construye una apuesta-martingala que tras una cruz en el tiro n deje tu posición en −n; tras tres caras vale 14−n. Como es martingala y el tiempo de tres caras es un tiempo de parada finito, E(14−n)=0 → E=14.",
   "Fórmula general (moneda justa, n caras seguidas): 2^{n+1}−2. Para n=1:2, n=2:6, n=3:14. La técnica de la martingala generaliza al instante."),
 q(uid,8,"quiz",
   "Una moneda sesgada tiene probabilidad p de cara. ¿Tiempo esperado hasta la primera cara?",
   "1/p. La cara aparece por primera vez en el tiro j con probabilidad p(1−p)^{j−1}; E=p·Σ j(1−p)^{j−1}=p·1/p²=1/p.",
   "Derivando 1/(1−x)=Σxʲ se obtiene Σj·x^{j−1}=1/(1−x)². Con x=1−p sale 1/p²; multiplica por p."),
 q(uid,9,"quiz",
   "Lanzas un dardo a una diana circular de radio R acertando el área uniformemente. ¿Distancia esperada al centro?",
   "2R/3. P(radio ≤ s)=(s/R)², así que la densidad del radio es 2s/R² (no uniforme). E(dist)=∫₀ᴿ s·(2s/R²)ds=2R/3.",
   "Error típico: suponer densidad uniforme en el radio (daría R/2). Hay más área cuanto más lejos del centro, por eso la densidad crece linealmente con s."),
 q(uid,10,"quiz",
   "Un dado de n caras justo. ¿Cuál es la esperanza de un tiro y la del 4.º día hábil del mes siendo jueves (semana de lunes a viernes)?",
   "Esperanza del dado de n caras: (n+1)/2. El 4.º día hábil es jueves si el día 1 cae sábado, domingo o lunes → 3/7.",
   "Dos clásicos de calentamiento. El segundo enseña a contar 'hacia atrás' qué día 1 produce el día hábil objetivo; ignora festivos para el modelo base."),
]
unidades.append(unidad(uid,17,"Arena Quant · Esperanza, juegos y parada óptima",
 "Valorar juegos bajo estrategia óptima resolviendo hacia atrás, y dominar las esperanzas de tiradas de moneda con la técnica de la martingala.",
 ["parada-optima","linealidad-esperanza"],
 ["parada óptima","esperanza condicional","distribución geométrica","martingalas"],
 ["Parada óptima: resuelve hacia atrás; quédate si el inmediato > E(continuar).",
  "Geométrica: E(tiros a 1.ª cara)=1/p; con moneda justa E(N)=Var(N)=2.",
  "n caras seguidas (moneda justa): 2^{n+1}−2 tiros esperados (martingala).",
  "Juego justo: iguala E(coste)=E(premio) bajo la estrategia óptima.",
  "Diana uniforme en área: densidad radial 2s/R², E(distancia)=2R/3."],
 banco))

# ===================== arena-q9 =====================
uid = "arena-q9"
banco = [
 q(uid,1,"quiz",
   "Una bolsa tiene 9 monedas normales y 1 de dos caras. Sacas una y sale cara 3 veces seguidas. ¿Probabilidad de que sea la de dos caras?",
   "8/17 ≈ 0.47. Bayes: P=(1·1/10)/(1·1/10 + (1/8)·9/10)=(1/10)/(1/10+9/80)=8/17.",
   "La verosimilitud (1 vs 1/8) empuja hacia la trucada, pero la tasa base (1/10 vs 9/10) la frena; el resultado vive entre ambas. Mismo motor que el VPP de un test médico."),
 q(uid,2,"quiz",
   "Sacas una moneda 'de aspecto normal' del bolsillo y salen 3 caras seguidas. ¿Probabilidad de que la siguiente sea cara? ¿Y si hubieran salido 100 caras?",
   "Con 3 caras: 1/2 (si la crees justa, los tiros son independientes). Con 100 caras: necesitas un prior. Si crees que es de dos caras con prob p, entonces P(2caras | N caras)=p/(p+(1−p)2^{−N}) → ≈1 para N grande.",
   "Sin información extra, una moneda normal es justa y el pasado no afecta. Un dato extremo (P=2^{−100} bajo 'justa') activa el razonamiento bayesiano."),
 q(uid,3,"quiz",
   "Mazo ordenado A>K>Q>…>2 (con palos, 52 cartas). Tú sacas una carta y luego yo otra. ¿Probabilidad de que mi carta sea mayor que la tuya?",
   "24/51. Casos: igual rango con prob 3/51; distinto rango con prob 48/51 y por simetría ½. P(mía mayor)=½·48/51=24/51≈0.471.",
   "La simetría colapsa el conteo: condicionado a rangos distintos, 'mía mayor' y 'tuya mayor' son igualmente probables."),
 q(uid,4,"quiz",
   "Cajón con 2 calcetines rojos y 2 negros. Sacas 2 al azar. ¿Probabilidad de que emparejen (mismo color)?",
   "1/3. Tras sacar el primero quedan 3 calcetines y solo 1 empareja con él → 1/3.",
   "No depende del color del primero. Generaliza: con n colores y un par de cada uno, P(par)=1/(2n−1)."),
 q(uid,5,"quiz",
   "Sacas 2 cartas de un mazo. ¿Probabilidad de que ambas sean ases (a) con reposición y (b) sin reposición?",
   "(a) con reposición: (1/13)²=1/169. (b) sin reposición: (1/13)·(3/51)=1/221.",
   "Con reposición los eventos son independientes e idénticos; sin reposición, la segunda probabilidad se condiciona en que ya salió un as (quedan 3 de 51)."),
 q(uid,6,"quiz",
   "Lanzas una moneda justa 1 000 000 de veces. ¿Número esperado de cadenas '6 caras seguidas de 6 cruces' (CCCCCCXXXXXX)?",
   "(10⁶−11)/2¹² ≈ 244.14. Hay 10⁶−11 posiciones de inicio posibles; cada una contiene el patrón de 12 símbolos con probabilidad 2^{−12}. Por linealidad de la esperanza, suma los indicadores.",
   "La linealidad de la esperanza NO requiere independencia (las ventanas se solapan): por eso basta multiplicar nº de posiciones por la probabilidad puntual."),
 q(uid,7,"quiz",
   "Torneo eliminatorio con 2ⁿ equipos; el de mayor ranking siempre gana. Emparejamientos iniciales al azar. ¿Probabilidad de que el 2.º mejor equipo juegue la final?",
   "2^{n−1}/(2ⁿ−1). El 2.º mejor llega a la final solo si NO cae en la misma mitad del cuadro que el mejor; de los 2ⁿ−1 lugares restantes, 2^{n−1} están en la otra mitad.",
   "El mejor siempre llega a la final; el 2.º solo si está en la otra rama. Para n=2: 2/3; n=3: 4/7; n→∞ tiende a 1/2."),
 q(uid,8,"quiz",
   "¿Es posible que tres activos A,B,C tengan ρ(A,B)=0.9, ρ(B,C)=0.8 y ρ(A,C)=0.1?",
   "No. La matriz de correlaciones [[1,.9,.1],[.9,1,.8],[.1,.8,1]] tiene determinante −0.316<0, luego no es semidefinida positiva, así que no puede ser una matriz de covarianzas válida.",
   "Las correlaciones están encadenadas: deben formar una matriz PSD. Es una desigualdad tipo triangular sobre los ángulos entre vectores."),
 q(uid,9,"quiz",
   "Da un ejemplo de distribución con varianza infinita y explica por qué importa.",
   "La distribución de Cauchy, densidad 1/(π(1+x²)). ∫x²·f(x)dx diverge (el integrando → 1), así que la varianza es infinita; ni siquiera tiene media propia (solo en valor principal).",
   "Es el contraejemplo estándar al TLC y a 'promediar reduce el ruido': la media muestral de Cauchy no converge. Surge como cociente de dos normales centradas."),
 q(uid,10,"acertijo",
   "Ruleta rusa: dos balas en recámaras CONTIGUAS de un revólver de 6 tiros. Se gira el tambor, aprietas el gatillo y no dispara. Eres el siguiente: ¿giras de nuevo o disparas directo?",
   "Disparas directo. Si giras: 2/6=1/3 de morir. Si no giras: el primer disparo vacío te dejó en una de las 4 recámaras vacías; solo 1 de esas 4 precede a una bala, así que P(morir)=1/4 < 1/3.",
   "La contigüidad de las balas es la clave: condicionado a un disparo vacío, la posición no es uniforme entre las cargadas. No girar aprovecha esa información."),
]
unidades.append(unidad(uid,18,"Arena Quant · Probabilidad condicional, Bayes y conteo",
 "Actualizar creencias con Bayes y tasa base, y usar simetría y linealidad de la esperanza para colapsar conteos difíciles.",
 ["bayes-tasa-base","casework"],
 ["teorema de Bayes","probabilidad condicional","simetría","linealidad de la esperanza","matriz PSD"],
 ["Bayes mezcla prior (tasa base) y verosimilitud; el resultado vive entre ambos.",
  "Simetría: condicionado a 'rangos distintos', 'mía mayor' = ½.",
  "Linealidad de la esperanza suma indicadores sin exigir independencia.",
  "Una matriz de correlaciones válida debe ser semidefinida positiva.",
  "La Cauchy tiene varianza infinita: rompe el TLC y la ley de promedios."],
 banco))

# ===================== arena-q10 =====================
uid = "arena-q10"
banco = [
 q(uid,1,"quiz",
   "Romeo y Julieta llegan independientemente a una hora uniforme entre las 9 y las 10; cada uno espera 15 minutos. ¿Probabilidad de que se encuentren?",
   "7/16. Toma x,y ~ U[0,1]; se encuentran si |x−y|≤¼. El complemento son dos triángulos rectángulos de cateto ¾ que juntan un cuadrado de lado ¾ (área 9/16). P(encuentro)=1−9/16=7/16.",
   "Dos tiempos al azar → un punto en el cuadrado unitario; la pregunta es la fracción del área que cumple la condición. Geometría > integrales."),
 q(uid,2,"quiz",
   "Rompes un palo en dos puntos elegidos uniformemente al azar. ¿Probabilidad de que los tres trozos formen un triángulo?",
   "1/4. Forman triángulo si ningún trozo supera ½, es decir si exactamente uno de x,y es <½ y |x−y|<½. En el cuadrado unitario la región válida tiene área 1/4.",
   "Condición triangular = ningún lado ≥ semiperímetro. Dibuja la región en el cuadrado y mide: dos medios cuadraditos = ¼."),
 q(uid,3,"acertijo",
   "100 personas abordan un avión de 100 asientos en orden. La primera (la abuela) se sienta al azar; cada siguiente toma su asiento si está libre, si no uno al azar. ¿Probabilidad de que el pasajero 100 acabe en SU asiento?",
   "1/2. Condiciona en el primer pasajero 'desplazado' con elección: acabará en el asiento 1 o en el 100, y ambos son igualmente probables por simetría. Da igual el número de asientos.",
   "El truco es condicionar en el evento que colapsa el problema (asiento 1 vs asiento 100), evitando la recursión algebraica."),
 q(uid,4,"quiz",
   "X₁,…,Xₙ son uniformes i.i.d. en [0,1]. ¿E(máx), E(mín) y E(máx−mín)?",
   "E(máx)=n/(n+1), E(mín)=1/(n+1), E(máx−mín)=(n−1)/(n+1). De P(máx≤x)=xⁿ sale densidad n·x^{n−1}; integrando x·n·x^{n−1} da n/(n+1). El mín es simétrico.",
   "El máximo de uniformes tiene CDF xⁿ (producto de CDFs por independencia). La diferencia esperada (rango) tiende a 1 cuando n crece."),
 q(uid,5,"quiz",
   "Da la función de densidad del k-ésimo estadístico de orden de n variables i.i.d. con densidad f y CDF F.",
   "f_{(k)}(x) = n!/[(k−1)!(n−k)!] · f(x)·F(x)^{k−1}·(1−F(x))^{n−k}. Sale de derivar P(X_{(k)}≤x)=Σ_{j≥k} C(n,j)F(x)ʲ(1−F)^{n−j}; casi todos los términos se cancelan.",
   "Interpretación: k−1 valores por debajo, uno en x, n−k por encima, con el coeficiente multinomial. Para uniformes es una distribución Beta(k, n−k+1)."),
 q(uid,6,"quiz",
   "X e Y son uniformes independientes en [0,1]. ¿Cuál es la densidad de X+Y?",
   "Triangular: h(z)=z para 0≤z≤1, h(z)=2−z para 1≤z≤2, y 0 fuera. Es la convolución h(z)=∫f(z−y)g(y)dy partida según los límites de integración.",
   "La densidad de una suma de independientes es la convolución de sus densidades. El pico en z=1 refleja que hay más formas de sumar 1 que 0 o 2."),
 q(uid,7,"quiz",
   "Si X ~ N(μ,σ), calcula E(X²) y E(exp(λX)) para λ>0.",
   "E(X²)=σ²+μ² (de Var(X)=E(X²)−(EX)²). E(exp(λX))=exp(μλ+σ²λ²/2): se completa el cuadrado y el integrando se vuelve la densidad de una N(μ+σ²λ, σ).",
   "E(exp(λX)) es la función generatriz de momentos de la normal y la base de la valoración lognormal (E[Sₜ] con Sₜ lognormal)."),
 q(uid,8,"quiz",
   "M es la Gaussiana acumulada (CDF de N(0,1)) y X ~ N(0,1). ¿Cuánto vale E[M(X)]?",
   "1/2. Por la transformada integral de probabilidad, M(X) ~ U(0,1), cuya media es 1/2. (Alternativa: M(x)−½ es impar y la densidad de X es par, así que su producto integra 0.)",
   "Aplicar la propia CDF de una variable continua a esa variable la uniformiza. Vale para cualquier X continua, no solo la normal."),
 q(uid,9,"quiz",
   "Enuncia con precisión el Teorema del Límite Central. ¿Qué condición es imprescindible?",
   "Para X₁,…,Xₙ i.i.d. con media μ y varianza σ² FINITA, (Sₙ−μn)/(σ√n) converge en distribución a N(0,1), independientemente de la distribución de partida. La condición clave es el segundo momento finito.",
   "Por eso la Cauchy (varianza infinita) no obedece el TLC clásico. Existen variantes (Lindeberg) para variables no idénticas con condiciones extra."),
 q(uid,10,"quiz",
   "Demuestra que toda matriz de covarianzas es semidefinida positiva.",
   "Para cualquier combinación lineal Y=aᵀX, Var(Y)=aᵀΣa. Como la varianza de una variable real es siempre ≥0, se tiene aᵀΣa≥0 para todo a, que es la definición de semidefinida positiva.",
   "Es 'semidefinida' (no definida): puede haber un vector a≠0 con aᵀΣa=0 si una combinación lineal de las X es constante (degenerada)."),
]
unidades.append(unidad(uid,19,"Arena Quant · Distribuciones, geometría y estadísticos de orden",
 "Resolver probabilidades de uniformes como áreas, manejar estadísticos de orden y dominar las identidades clave de la Gaussiana.",
 ["parametrizar-dibujar","linealidad-esperanza"],
 ["probabilidad geométrica","estadísticos de orden","convolución","función generatriz de momentos","TLC"],
 ["Dos uniformes → un punto en el cuadrado; la probabilidad es un área.",
  "E(máx de n uniformes)=n/(n+1); E(mín)=1/(n+1).",
  "La densidad de una suma es la convolución de las densidades.",
  "E(exp(λX))=exp(μλ+σ²λ²/2): la MGF gaussiana, base de lo lognormal.",
  "El TLC exige segundo momento finito; toda covarianza es PSD."],
 banco))

# ===================== arena-q11 =====================
uid = "arena-q11"
banco = [
 q(uid,1,"quiz",
   "Define el movimiento browniano estándar Wₜ y da el valor de E(Wₛ·Wₜ).",
   "Wₜ es browniano si W₀=0, tiene incrementos independientes y Wₜ−Wₛ ~ N(0,t−s). Entonces, para s≤t, E(Wₛ·Wₜ)=mín(s,t)=s, usando Wₜ=Wₛ+(Wₜ−Wₛ) y la independencia de incrementos.",
   "El truco x=x+y−y con incrementos independientes: E(Wₛ(Wₛ+(Wₜ−Wₛ)))=E(Wₛ²)+E(Wₛ)E(Wₜ−Wₛ)=s+0."),
 q(uid,2,"quiz",
   "Un paseo aleatorio simétrico en {0,…,1000} arranca en 80; ±1 con prob ½; para al tocar 0 o 1000. ¿Probabilidad de tocar 0 antes que 1000?",
   "0.92. La posición es una martingala; el tiempo de salida es un tiempo de parada de esperanza finita, así que E(posición al parar)=80. Si p=P(tocar 1000): 1000p=80 → p=0.08, luego P(tocar 0)=0.92.",
   "El muestreo opcional convierte la probabilidad de absorción en una ecuación lineal. Con paso justo, P(tocar la barrera superior)=inicio/altura."),
 q(uid,3,"quiz",
   "Si Sₜ sigue un browniano geométrico dSₜ=μSₜdt+σSₜdWₜ, ¿qué proceso sigue (Sₜ)²?",
   "Otro browniano geométrico, con deriva (2μ+σ²) y difusión 2σ. Por Itô con f(x)=x²: d(S²)=2S dS+(dS)²=(2μ+σ²)S²dt+2σS²dWₜ.",
   "También se ve desde la solución Sₜ=S₀exp((μ−σ²/2)t+σWₜ): al elevar al cuadrado, (Sₜ)²=S₀²exp((2μ−σ²)t+2σWₜ), de nuevo lognormal."),
 q(uid,4,"quiz",
   "Dado dSₜ=μSₜdt+σSₜdWₜ, deriva la SDE de log(Sₜ).",
   "d log Sₜ=(μ−σ²/2)dt+σdWₜ. Por Itô con f(x)=log x: df=(1/S)dS−(1/2S²)(dS)²=(μ−σ²/2)dt+σdWₜ.",
   "El término −σ²/2 es la corrección de Itô: la diferencia entre la media aritmética y la geométrica de los retornos. Origen de innumerables errores en valoración."),
 q(uid,5,"quiz",
   "Demuestra que Xₜ=cosh(λWₜ)·exp(−λ²t/2) es una martingala.",
   "Aplica Itô: ∂g/∂t=−(λ²/2)g, ∂g/∂x=λ·senh(λx)e^{−λ²t/2}, ∂²g/∂x²=λ²g. dXₜ=[−(λ²/2)X + ½λ²X]dt + λ·senh(λWₜ)e^{−λ²t/2}dWₜ = λ·senh(λWₜ)e^{−λ²t/2}dWₜ. Sin deriva → martingala.",
   "El factor exp(−λ²t/2) está calibrado justo para cancelar el término dt de Itô. Misma familia que exp(σWₜ−σ²t/2)."),
 q(uid,6,"quiz",
   "Si Wₜ es browniano estándar, ¿es Wₜ³ una martingala?",
   "No. Por Itô: d(Wₜ³)=3Wₜ²dWₜ+3Wₜ(dWₜ)²=3Wₜ dt+3Wₜ²dWₜ. El término de deriva 3Wₜ dt no es nulo, así que Wₜ³ no es martingala.",
   "Test de martingala: aplica Itô y exige deriva cero. En cambio, Wₜ³−3tWₜ SÍ es martingala (la resta cancela la deriva)."),
 q(uid,7,"quiz",
   "Aplica Itô a 2^{Wₜ}. ¿Es martingala?",
   "No. Con f(x)=2ˣ=e^{x ln2}: f'=ln2·2ˣ, f''=(ln2)²2ˣ. d(2^{Wₜ})=ln2·2^{Wₜ}dWₜ+½(ln2)²2^{Wₜ}dt. La deriva ½(ln2)²2^{Wₜ}dt≠0 → no es martingala.",
   "Cualquier f(Wₜ) estrictamente convexa adquiere deriva positiva por el término ½f''(dW)². Solo las funciones afines (o con corrección temporal) son martingala."),
 q(uid,8,"quiz",
   "Wₜ y Zₜ son dos movimientos brownianos independientes. ¿Cuál es la distribución del cociente Wₜ/Zₜ?",
   "Cauchy estándar, densidad 1/(π(1+u²)). Es el cociente de dos normales centradas con la misma varianza; el resultado no depende de t.",
   "Por eso Wₜ/Zₜ no tiene media ni varianza: el cociente de normales genera colas pesadas. Es la fuente clásica de la Cauchy."),
 q(uid,9,"quiz",
   "Para un browniano con X₀=0 y X₁>0, ¿cuál es la probabilidad de que X₂<0?",
   "1/4. Necesitas que el incremento X₂−X₁ sea negativo (prob ½) y de magnitud mayor que X₁ (prob ½, pues X₂−X₁ y X₁ tienen la misma distribución). Producto: ¼.",
   "La clave es la simetría e idéntica distribución de los incrementos independientes en intervalos de igual longitud."),
 q(uid,10,"quiz",
   "Resuelve la SDE del proceso de Ornstein-Uhlenbeck dXₜ=θ(μ−Xₜ)dt+σdWₜ.",
   "Xₜ=X₀e^{−θt}+μ(1−e^{−θt})+∫₀ᵗ σe^{θ(s−t)}dWₛ. Se usa el factor integrante e^{θt}: d(e^{θt}Xₜ)=θμe^{θt}dt+σe^{θt}dWₜ; integra y multiplica por e^{−θt}.",
   "θ es la velocidad de reversión hacia μ. E(Xₜ)=X₀e^{−θt}+μ(1−e^{−θt}); Var(Xₜ)=σ²/(2θ)·(1−e^{−2θt}). Es el modelo Vasicek de tasas."),
 q(uid,11,"quiz",
   "¿Qué significa la regla dt=(dWₜ)² y por qué importa en el lema de Itô?",
   "Expresa que la variación cuadrática del browniano crece a razón 1 por unidad de tiempo: el cuadrado de los incrementos NO es despreciable en el límite. Por eso, al hacer Taylor de f(Wₜ), el término ½f''(dW)² sobrevive como ½f''dt.",
   "En cálculo ordinario (dx)² se descarta; en el estocástico no, porque el browniano no es diferenciable y su variación cuadrática es finita y positiva."),
]
unidades.append(unidad(uid,20,"Arena Quant · Movimiento browniano, Itô y martingalas",
 "Usar el muestreo opcional para barreras y la fórmula de Itô para transformar procesos, distinguiendo qué procesos son martingala.",
 ["martingala-parada","caminata-aleatoria"],
 ["movimiento browniano","lema de Itô","martingalas","muestreo opcional","Ornstein-Uhlenbeck"],
 ["Browniano: incrementos independientes Wₜ−Wₛ~N(0,t−s); E(WₛWₜ)=mín(s,t).",
  "Muestreo opcional: P(absorción) lineal en el punto de partida (paso justo).",
  "Itô: d log S=(μ−σ²/2)dt+σdW; la corrección −σ²/2 es central.",
  "Un proceso f(Wₜ) es martingala solo si Itô deja deriva cero.",
  "Cociente de dos normales = Cauchy; OU revierte a μ con velocidad θ."],
 banco))

# ===================== arena-q12 =====================
uid = "arena-q12"
banco = [
 q(uid,1,"acertijo",
   "Copa de vino blanco y copa de tinto, 100 ml cada una. Pasas 5 ml de tinto al blanco, mezclas, y devuelves 5 ml de la mezcla al tinto. ¿Hay más blanco en el tinto o más tinto en el blanco?",
   "Exactamente igual. Al final cada copa vuelve a tener 100 ml; por conservación, el volumen de blanco que falta en su copa es igual al de tinto que falta en la suya, así que el blanco en el tinto = tinto en el blanco.",
   "Conservación: no hace falta seguir las concentraciones. Como los volúmenes finales son iguales a los iniciales, el intercambio neto es simétrico."),
 q(uid,2,"acertijo",
   "Estás en un bote en una piscina y tiras el ancla por la borda hasta el fondo. ¿Sube, baja o queda igual el nivel del agua de la piscina?",
   "Baja. En el bote, el ancla desplaza agua igual a su PESO; en el fondo, igual a su VOLUMEN. Como el ancla es más densa que el agua, desplaza más estando en el bote, así que al hundirla el nivel baja.",
   "Principio de Arquímedes: flotando desplazas tu peso; sumergido (y apoyado) desplazas tu volumen. Para algo más denso que el agua, peso>volumen en agua → el nivel cae."),
 q(uid,3,"acertijo",
   "Una tableta de chocolate de n cuadritos. ¿Cuántas roturas (siempre por una línea recta de una sola pieza) necesitas para separar los n cuadritos? ¿Depende de la forma?",
   "n−1 roturas, independientemente de la forma. Cada rotura convierte una pieza en dos, aumentando el número de piezas en exactamente 1; de 1 pieza a n piezas hacen falta n−1.",
   "Invariante puro: el conteo de piezas sube en 1 por rotura. La forma de la tableta es irrelevante."),
 q(uid,4,"acertijo",
   "Una hormiga va de un vértice a su opuesto sobre la SUPERFICIE de un cubo de volumen 1 m³. ¿Cuál es la distancia mínima?",
   "√5 m. Desdobla el cubo en el plano: el camino más corto entre vértices opuestos se convierte en la diagonal de un rectángulo 1×2, de longitud √(1²+2²)=√5≈2.236 m.",
   "Desdoblar la geometría convierte un problema 3D en uno 2D resoluble con Pitágoras. La diagonal recta interna (√3) no vale: la hormiga va por la superficie."),
 q(uid,5,"quiz",
   "¿Cuál es el número mínimo de pesas enteras para equilibrar exactamente cualquier peso entero de 1 a 40 usando UN solo platillo? ¿Y si puedes ponerlas en AMBOS platillos?",
   "Un platillo: 6 pesas {1,2,4,8,16,32} (sistema binario; cada pesa entra o no). Dos platillos: 4 pesas {1,3,9,27} (sistema ternario; cada pesa suma, resta o no participa, y 3⁴=81≥2·40+1).",
   "Un platillo = base 2 (presente/ausente). Dos platillos = base 3 balanceada (+1/0/−1). Con 5 pesas binarias solo cubres 2⁵=32<40."),
 q(uid,6,"acertijo",
   "Tú y yo bebemos una pinta: yo tomo la mitad, tú la mitad de lo que queda, yo la mitad del nuevo resto, y así indefinidamente. ¿Cuánto bebe cada uno?",
   "Yo bebo 2/3 de la pinta y tú 1/3. Yo bebo Σ_{k≥0} 1/2^{2k+1} y tú la mitad de esa suma, así que bebo el doble que tú; como entre los dos consumimos la pinta entera (Σ1/2^k=1), me toca 2/3 y a ti 1/3.",
   "No hace falta sumar las series: basta ver que en cada ronda yo bebo el doble que tú, y que el total es 1."),
 q(uid,7,"quiz",
   "Un conejo sube una escalera de n peldaños dando saltos de 1 o 2 peldaños. ¿De cuántas formas distintas puede llegar arriba?",
   "F_{n+1} (Fibonacci). Si p(n) es el número de formas: p(n)=p(n−1)+p(n−2) (el último salto fue de 1 o de 2), con p(1)=1, p(2)=2. Da 1,2,3,5,8,13,… para n=1,2,3,4,5,6.",
   "La recurrencia 'el último paso es de un tipo u otro' genera Fibonacci. Aparece siempre que una construcción se arma pegando un bloque de tamaño 1 o 2."),
 q(uid,8,"quiz",
   "¿De cuántas formas se puede embaldosar un tablero 2×n con fichas de dominó 2×1?",
   "F_{n+1} (Fibonacci), con F(0)=1, F(1)=1… aquí p(n)=p(n−1)+p(n−2): la primera columna es un dominó vertical (deja 2×(n−1)) o dos horizontales (deja 2×(n−2)). p(1)=1, p(2)=2.",
   "Misma recurrencia que el conejo: Fibonacci. La clave es que dos dominós horizontales ocupan un bloque 2×2 completo."),
 q(uid,9,"acertijo",
   "Una vuelta a una pista de 1 milla la recorres a 30 mph de media. ¿A qué velocidad debes hacer la segunda vuelta para promediar 60 mph en las dos vueltas?",
   "Imposible. Dos millas a 60 mph requieren 2 minutos en total; pero 1 milla a 30 mph ya consume 2 minutos, sin dejar tiempo para la segunda vuelta. Necesitarías velocidad infinita.",
   "La velocidad media sobre distancia fija es la media ARMÓNICA, no la aritmética. El error es promediar 30 y 90 para 'dar' 60."),
 q(uid,10,"acertijo",
   "Empieza a nevar a ritmo constante en algún momento antes del mediodía. Un quitanieves arranca a las 12:00 con velocidad inversamente proporcional al tiempo transcurrido desde que empezó a nevar. Recorre el doble de distancia entre 12 y 1 que entre 1 y 2. ¿Cuándo empezó a nevar?",
   "½(√5−1) horas antes del mediodía (≈0.618 h ≈ 37 min). Con velocidad α/t, la distancia entre t₁ y t₂ es α·ln(t₂/t₁). La condición d(x,x+1)=2·d(x+1,x+2) da ln((x+1)/x)=2ln((x+2)/(x+1)), o (x+1)/x=((x+2)/(x+1))², cuya raíz positiva es x=½(−1+√5).",
   "Aparece la razón áurea. El truco: la distancia es la integral de la velocidad α/t, que da un logaritmo; la condición se vuelve una ecuación cuadrática."),
]
unidades.append(unidad(uid,21,"Arena Quant · Brainteasers: trucos, invariantes y conteo",
 "Resolver acertijos encontrando la cantidad conservada o el invariante de conteo, y reconocer recurrencias de Fibonacci y trampas de promedio.",
 ["invariante","desdoblar"],
 ["conservación","invariantes","recurrencias","Fibonacci","media armónica","series geométricas"],
 ["Conservación: si las cantidades finales son fijas, el resultado se sigue sin álgebra.",
  "Cada rotura/corte cambia el conteo de piezas en exactamente 1 → n−1 roturas.",
  "Pesas: un platillo = binario {1,2,4,…}; dos platillos = ternario {1,3,9,…}.",
  "Desdobla una superficie 3D a un plano y usa Pitágoras (hormiga en cubo = √5).",
  "Velocidad media sobre distancia fija = media armónica, no aritmética."],
 banco))

# ===================== arena-q13 =====================
uid = "arena-q13"
banco = [
 q(uid,1,"acertijo",
   "Hay n leones hambrientos y un trozo de carne. Un león puede comerlo, pero al hacerlo se duerme y se vuelve presa de los demás. Todos son perfectamente lógicos y prefieren vivir a comer. ¿Qué ocurre?",
   "Si n es par, ningún león come; si n es impar, uno come. Por inducción: 1 león come (nadie lo amenaza); 2 leones, nadie come (comer te vuelve presa del único rival, que entonces no comería); 3, el más cercano come (sabe que con 2 nadie comería), etc.",
   "Inducción desde el caso base. La paridad emerge: cada león razona '¿qué haría el grupo si yo desaparezco como amenaza?'."),
 q(uid,2,"acertijo",
   "50 isleños perfectamente lógicos tienen ojos azules o marrones; nadie conoce su propio color y no hay espejos. La regla: si deduces que tienes ojos azules, te vas esa medianoche. Un forastero anuncia 'al menos uno tiene ojos azules'. Si hay exactamente n personas de ojos azules, ¿qué pasa?",
   "Todas las personas de ojos azules se van la n-ésima noche. Por inducción: con n=1, esa persona ve 0 azules y deduce de inmediato; con n, cada azul espera a la noche n−1 y, al ver que nadie se fue, deduce su color y se va la noche n.",
   "El forastero aporta CONOCIMIENTO COMÚN (todos saben que todos saben…), no información factual nueva. Eso desbloquea la cadena inductiva."),
 q(uid,3,"acertijo",
   "Tienes 9 canicas idénticas salvo una más pesada, y una báscula de dos platillos. ¿En cuántas pesadas garantizas hallar la pesada, y cómo?",
   "2 pesadas. Pesa 3 contra 3 (deja 3 fuera): si equilibran, la pesada está entre las 3 de fuera; si no, en el grupo más pesado. En cualquier caso te quedan 3 candidatas; pesa 1 contra 1 (deja 1 fuera) para hallarla.",
   "Cada pesada tiene TRES resultados (izquierda/derecha/equilibrio), no dos: por eso cubres 3²=9 con dos pesadas. El error es razonar en binario y dividir en mitades."),
 q(uid,4,"acertijo",
   "Cuatro cartas muestran 7, 6, A, C. La afirmación es: 'si una carta tiene una vocal en una cara, tiene un número par en la otra'. ¿Qué cartas debes girar para comprobarla?",
   "La A y el 7. La A (vocal) debe tener par detrás; el 7 (impar) no debe tener vocal detrás. No giras el 6 (la regla no exige nada sobre cartas con par) ni la C (no es vocal).",
   "Tarea de selección de Wason. Para comprobar 'P→Q' giras los casos que pueden falsarla: P (vocal) y ¬Q (impar). El error común es girar el 6 (afirmar el consecuente)."),
 q(uid,5,"acertijo",
   "Juego de Nim: hay n cerillas; por turnos cada jugador toma 1, 2 o 3; el que toma la ÚLTIMA cerilla pierde. ¿Cuál es la estrategia óptima?",
   "Deja siempre al rival un número de la forma 4j+1 cerillas. Si puedes hacerlo en tu primer turno, ve primero; si no, ve segundo. Cuando el rival toma x, tú tomas 4−x para mantener el patrón. Así él se queda con 1 al final y pierde.",
   "Las posiciones perdedoras (para quien va a mover) son ≡1 (mód 4). Si 'el que toma la última GANA', deja múltiplos de 4 (4j) en su lugar."),
 q(uid,6,"acertijo",
   "Por turnos colocáis monedas idénticas sobre una mesa redonda, sin solapar ni salirse; pierde quien no pueda colocar. ¿Puedes garantizar la victoria eligiendo orden?",
   "Sí: ve PRIMERO. Coloca tu primera moneda en el centro exacto y luego responde cada jugada del rival con la moneda diametralmente opuesta (reflejada respecto al centro). Por simetría, si el rival tuvo sitio, tú también lo tienes.",
   "Estrategia de simetría: rompes la simetría tú primero (centro) y luego la mantienes. El rival siempre se queda sin movimiento antes que tú."),
 q(uid,7,"acertijo",
   "Un rectángulo pequeño está completamente dentro de uno grande, en posición y orientación arbitrarias. Con una sola línea recta, divide en dos áreas iguales la parte del rectángulo grande que NO queda cubierta por el pequeño.",
   "Traza la recta que pasa por los CENTROS de ambos rectángulos. Toda recta por el centro de un rectángulo biseca su área; al bisecar el grande y el pequeño a la vez, también biseca la diferencia (el área no cubierta).",
   "Clave: el centro (intersección de las diagonales) es el punto por el que cualquier recta divide el rectángulo en dos mitades iguales."),
 q(uid,8,"acertijo",
   "22 presos en 22 celdas. Uno a uno, al azar, entran a una sala con dos interruptores (inicialmente abajo); el preso puede mover uno. Cuando alguno asegure que TODOS han entrado, quedan libres si acierta y mueren si no. Tienen una hora para planear. ¿Cómo lo garantizan?",
   "Eligen un 'capitán contador'. Los otros 21 suben un interruptor designado solo la PRIMERA vez que lo encuentran abajo (después lo dejan). El capitán, cada vez que lo encuentra arriba, suma 1 a su cuenta y lo baja. Al llegar a 21, sabe que los 21 estuvieron y lo declara.",
   "El segundo interruptor es señuelo para absorber movimientos obligatorios. El patrón canónico: un contador único acumula señales de un canal mínimo de un solo bit."),
 q(uid,9,"quiz",
   "¿Cuántos cuadritos 1×1×1 de un cubo 4×4×4 tienen pintura, si se pinta toda la superficie exterior del cubo grande?",
   "56. El truco es contar los SIN pintura: forman un cubo interior 2×2×2 = 8 cuadritos. Los pintados son 4³−8 = 64−8 = 56.",
   "Contar el complemento (los del núcleo (n−2)³) es mucho más limpio que sumar caras y restar solapamientos. Para n×n×n: n³−(n−2)³ pintados."),
 q(uid,10,"acertijo",
   "Calcula mentalmente 15³ y estima su magnitud antes de dar el número exacto.",
   "15³=3375. Estimación: 15 está entre 10 (cubo 1000) y 20 (cubo 8000); como elevar al cubo es convexo, el resultado está por debajo del promedio (4500) → algo menor que 4000 es buen ancla. Exacto: 15²·15=225·15=3375.",
   "Cálculo mental: descompón 225·15=225·10+225·5=2250+1125=3375. Entrenar cubos pequeños y cuadrados acelera la aritmética de entrevista."),
]
unidades.append(unidad(uid,22,"Arena Quant · Brainteasers: lógica, inducción y juegos",
 "Desarmar acertijos lógicos con inducción desde el caso base y ganar juegos identificando posiciones perdedoras y estrategias de simetría.",
 ["induccion","desdoblar"],
 ["inducción","lógica deductiva","teoría de juegos","estrategia de simetría","conocimiento común"],
 ["Inducción: empieza en 0/1/2 y sube; muchas respuestas dependen de la paridad.",
  "Báscula de platillos: tres resultados por pesada → cubres 3^k candidatos.",
  "Juegos por turnos: identifica posiciones perdedoras (Nim: deja 4j+1).",
  "Simetría: en mesas/tableros, juega el reflejo del rival respecto al centro.",
  "Cuenta el complemento: cuadritos pintados = n³−(n−2)³."],
 banco))

# ---- insertar unidades y registrar en el bloque ----
s['unidades'].extend(unidades)
f7 = next(b for b in s['bloques'] if b['id'] == 'fase-7')
for u in unidades:
    f7['unidades'].append(u['id'])

# ---- ítems de examen ----
def pista(*ts):
    return list(ts)

exam = [
 {"id":"f7-ex-15","heuristica":"parada-optima",
  "enunciado":"Tiras un dado justo hasta 3 veces; en cada tiro te quedas con el número (en dólares) o vuelves a tirar. ¿Cuál es tu ganancia esperada óptima, y con qué regla decides parar en cada tiro?",
  "pistas":pista(
    "Resuelve hacia atrás: ¿cuánto vale el juego si solo te queda 1 tiro?",
    "Con 1 tiro, E=3.5. Con 2 tiros te quedas con el primero solo si supera tu esperanza de continuar (3.5). ¿Qué caras cumplen eso?",
    "Te quedas si sale 4,5 o 6. E(2)=(6+5+4)/6 + (3/6)·3.5. Calcula ese valor.",
    "E(2)=4.25. Para el 3.er tiro, te quedas con el primero si supera 4.25, es decir si sale 5 o 6. Escribe E(3).",
    "E(3)=(6+5)/6 + (4/6)·4.25 = 14/3 ≈ 4.67. La regla: en cada nodo, quédate si el valor inmediato supera la esperanza de seguir jugando."),
  "solucion":"E=14/3≈4.67. Hacia atrás: E(1)=3.5; E(2)=(6+5+4)/6+(3/6)·3.5=4.25; E(3)=(6+5)/6+(4/6)·4.25=14/3. Regla de parada: te quedas si el tiro supera la esperanza de continuar (4 o más en el primer tiro, 5 o más en el segundo).",
  "disparador":"Señal: 'puedes quedarte o seguir'. Jugada: parada óptima = valorar una opción americana resolviendo hacia atrás; en cada nodo compara el premio inmediato con E(continuar).",
  "metadata":{"ruta":"quant","nivel":"intermedio",
    "skills":["parada óptima","esperanza condicional","valoración por inducción"],
    "errores_comunes":["Promediar las caras sin la regla de parada","Olvidar recalcular el umbral en cada tiro"],
    "casos_borde":["Con 1 solo tiro E=3.5; con infinitos tiros el umbral tiende a 6"],
    "source":LIBRO}},
 {"id":"f7-ex-16","heuristica":"martingala-parada",
  "enunciado":"Un paseo aleatorio simétrico en {0,1,…,1000} arranca en 80 (±1 con prob ½) y para al tocar 0 o 1000. Calcula la probabilidad de tocar 0 antes que 1000, justificando el método.",
  "pistas":pista(
    "¿Qué propiedad tiene la posición del paseo en cada paso respecto a su esperanza futura?",
    "La posición es una martingala: E(posición mañana | hoy)=hoy. ¿Qué teorema relaciona su valor inicial con su esperanza en el momento de parar?",
    "Muestreo opcional: como el tiempo de salida tiene esperanza finita, E(posición al parar)=80.",
    "Al parar, la posición es 0 (prob 1−p) o 1000 (prob p). Plantea 1000p+0·(1−p)=80.",
    "p=P(tocar 1000)=80/1000=0.08, luego P(tocar 0)=1−0.08=0.92."),
  "solucion":"P(tocar 0)=0.92. La posición es martingala; por muestreo opcional E(posición al parar)=80. Si p=P(tocar 1000): 1000p=80 → p=0.08, así que P(tocar 0)=0.92.",
  "disparador":"Señal: 'probabilidad de tocar una barrera antes que otra, paso justo'. Jugada: la posición es martingala; el muestreo opcional vuelve la probabilidad de absorción lineal en el inicio (inicio/altura).",
  "metadata":{"ruta":"quant","nivel":"avanzado",
    "skills":["martingala","muestreo opcional","probabilidad de absorción"],
    "errores_comunes":["Dar la probabilidad de la barrera equivocada","Olvidar verificar que el tiempo de parada tiene esperanza finita"],
    "casos_borde":["Si arranca en 0 o 1000 el juego ya terminó","Con paso sesgado (p≠½) la fórmula deja de ser lineal"],
    "source":LIBRO}},
 {"id":"f7-ex-17","heuristica":"recurrencia",
  "enunciado":"Una hormiga camina por las aristas de un cubo, tardando 1 minuto por arista; en cada vértice elige al azar una de las 3 aristas. Colocas la hormiga en un vértice. ¿Cuántos minutos esperas hasta que vuelva a ese mismo vértice?",
  "pistas":pista(
    "Por simetría, lo único que importa es la distancia (0,1,2,3 aristas) al vértice de origen. Define f(n)=tiempo esperado de retorno desde distancia n.",
    "Desde distancia 1: con prob 1/3 vas al origen (1 min), con prob 2/3 vas a distancia 2. Escribe f(1) en función de f(2).",
    "Plantea el sistema: f(0)=1+f(1); f(1)=1/3+2/3(f(2)+1); f(2)=2/3(f(1)+1)+1/3(f(3)+1); f(3)=1+f(2).",
    "Sustituye f(3)=1+f(2) en f(2): obtienes f(2)=f(1)+2. Luego mete eso en f(1).",
    "f(1)=1+2/3(f(1)+2) → (1/3)f(1)=7/3 → f(1)=7; f(2)=9; f(3)=10; f(0)=1+7=8 minutos."),
  "solucion":"8 minutos. Por simetría f depende solo de la distancia: f(0)=1+f(1), f(1)=1/3+2/3(f(2)+1), f(2)=2/3(f(1)+1)+1/3(f(3)+1), f(3)=1+f(2). Resolviendo: f(1)=7, f(2)=9, f(3)=10, f(0)=8.",
  "disparador":"Señal: 'tiempo esperado de retorno en un grafo simétrico'. Jugada: colapsa los estados por simetría y plantea una recurrencia (primer paso) entre las clases de distancia.",
  "metadata":{"ruta":"quant","nivel":"avanzado",
    "skills":["cadenas de Markov","recurrencia por primer paso","explotar simetría"],
    "errores_comunes":["Tratar los 8 vértices como estados distintos en vez de agrupar por distancia","Olvidar el +1 por el minuto que toma cada arista"],
    "casos_borde":["El tiempo medio de retorno = 1/π(estado) = 8, con distribución estacionaria uniforme"],
    "source":LIBRO}},
 {"id":"f7-ex-18","heuristica":"invariante",
  "enunciado":"Tienes una tableta de chocolate de n cuadritos. En cada rotura partes UNA pieza en dos por una línea recta. ¿Cuántas roturas necesitas para separar los n cuadritos, y depende de la forma de la tableta?",
  "pistas":pista(
    "Piensa en una cantidad que cambie de forma predecible con cada rotura.",
    "¿Cuánto aumenta el número de piezas con una sola rotura?",
    "Cada rotura convierte 1 pieza en 2, así que el número de piezas sube exactamente en 1.",
    "Empiezas con 1 pieza y quieres llegar a n piezas. ¿Cuántos incrementos de 1 hacen falta?",
    "n−1 roturas, sin importar la forma ni el orden: es un invariante de conteo."),
  "solucion":"n−1 roturas, independientemente de la forma. Cada rotura aumenta el número de piezas en exactamente 1; para pasar de 1 a n piezas se necesitan n−1 roturas.",
  "disparador":"Señal: '¿cuántas operaciones para descomponer algo?'. Jugada: busca un invariante de conteo (aquí, +1 pieza por rotura) y la respuesta es inmediata e independiente de la estrategia.",
  "metadata":{"ruta":"quant","nivel":"basico",
    "skills":["invariantes","conteo","argumentos de monovariante"],
    "errores_comunes":["Intentar contar roturas por filas/columnas según la forma","Creer que un orden astuto reduce el número"],
    "casos_borde":["n=1: 0 roturas","Tablero 2D o pila 3D: el argumento +1 por corte se mantiene"],
    "source":LIBRO}},
 {"id":"f7-ex-19","heuristica":"induccion",
  "enunciado":"En una isla, k personas perfectamente lógicas tienen ojos azules (el resto marrones); nadie sabe su propio color ni hay espejos. Regla: quien deduzca que tiene ojos azules se va esa medianoche. Un visitante anuncia en voz alta 'al menos uno de ustedes tiene ojos azules'. ¿Qué ocurre y por qué, si el anuncio parece no decir nada nuevo cuando k≥2?",
  "pistas":pista(
    "Empieza por el caso más pequeño: si k=1, ¿qué ve y deduce esa única persona azul tras el anuncio?",
    "k=1: la persona azul ve 0 ojos azules; el anuncio le revela que es ella → se va la 1.ª noche.",
    "k=2: cada azul ve 1 azul y razona '¿se irá esa persona la 1.ª noche?'. Si no se va, ¿qué deduce?",
    "Generaliza: cada azul espera a la noche k−1; si nadie se fue, deduce su propio color.",
    "Las k personas de ojos azules se van todas la k-ésima noche. El anuncio aporta CONOCIMIENTO COMÚN (todos saben que todos saben…), no un hecho nuevo."),
  "solucion":"Las k personas de ojos azules se van todas la noche número k. Por inducción: con k=1 la deducción es inmediata; cada azul, al ver k−1 azules, espera a la noche k−1 y, al constatar que nadie se fue, concluye que él también es azul y se marcha la noche k.",
  "disparador":"Señal: 'agentes lógicos, información pública, deducción en cadena'. Jugada: inducción desde el caso base; el anuncio crea conocimiento común que desbloquea la cadena, aunque el hecho ya fuera 'sabido' por cada uno.",
  "metadata":{"ruta":"quant","nivel":"avanzado",
    "skills":["inducción","conocimiento común","lógica epistémica"],
    "errores_comunes":["Creer que el anuncio no cambia nada cuando k≥2","Confundir 'todos lo saben' con 'es conocimiento común'"],
    "casos_borde":["k=1: se va la 1.ª noche","Si el visitante mintiera pero le creyeran, la dinámica seguiría igual"],
    "source":LIBRO}},
 {"id":"f7-ex-20","heuristica":"bayes-tasa-base",
  "enunciado":"Una bolsa contiene 9 monedas normales y 1 moneda de dos caras. Sacas una al azar y la lanzas 3 veces: sale cara las 3 veces. ¿Cuál es la probabilidad de que hayas sacado la moneda de dos caras?",
  "pistas":pista(
    "Define los dos sucesos prior: P(dos caras)=1/10, P(normal)=9/10. ¿Cuál es la verosimilitud de '3 caras' bajo cada uno?",
    "Bajo la de dos caras, P(CCC)=1. Bajo una normal, P(CCC)=(1/2)³=1/8. Aplica Bayes.",
    "P = (1·1/10) / (1·1/10 + (1/8)·9/10).",
    "Numerador 1/10=0.1; denominador 0.1+9/80=0.1+0.1125=0.2125.",
    "P = 0.1/0.2125 = 8/17 ≈ 0.47."),
  "solucion":"8/17 ≈ 0.47. Por Bayes: P(2caras|CCC)=(1·1/10)/(1·1/10+(1/8)·9/10)=(1/10)/(17/80)=8/17.",
  "disparador":"Señal: 'dato a favor de una hipótesis rara'. Jugada: Bayes combinando tasa base (prior) y verosimilitud; el resultado se queda entre ambos, sin saltar al 'casi seguro'.",
  "metadata":{"ruta":"quant","nivel":"intermedio",
    "skills":["teorema de Bayes","tasa base","verosimilitud"],
    "errores_comunes":["Ignorar la tasa base y responder cerca de 1","Confundir P(CCC|2caras) con P(2caras|CCC)"],
    "casos_borde":["Con muchísimas caras seguidas la probabilidad → 1","Con 0 caras la posterior de 'dos caras' sería 0"],
    "source":LIBRO}},
]
f7['examen']['items'].extend(exam)

with open(SP, 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=2)
    f.write('\n')

total_banco = sum(len(u['banco']) for u in unidades)
print(f"OK: {len(unidades)} unidades, {total_banco} preguntas de banco, "
      f"{len(exam)} ítems de examen, {len(nuevas_heur)} heurísticas nuevas.")
