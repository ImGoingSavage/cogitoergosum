#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ingesta tanda 5: Statistical Inference (Casella & Berger, 2nd ed.) → study.json.
Idempotente: aborta si arena-cb1 ya existe. Re-ejecutable tras un rollback.
RANGOS RESERVADOS (cuenta B, 2026-06-13): órdenes 35-54, exam f7-ex-27..36, sw.js v34."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'data', 'study.json')
LIBRO = "Statistical Inference (Casella & Berger, 2nd ed.)"

with open(SP, encoding='utf-8') as f:
    s = json.load(f)

if any(u['id'] == 'arena-cb1' for u in s['unidades']):
    print("arena-cb1 ya existe — nada que hacer (idempotente).")
    sys.exit(0)

# ---- Heurísticas nuevas ----
nuevas_heur = [
    {"id": "factorizacion-suficiente",
     "nombre": "Factorización de Fisher-Neyman",
     "descripcion": "Escribe la densidad conjunta como g(T(x),θ)·h(x). Si puedes separar así, T es suficiente."},
    {"id": "rao-blackwell",
     "nombre": "Rao-Blackwell",
     "descripcion": "Para mejorar un estimador, condiciona en el estadístico suficiente: E[δ|T] no empeora nunca la varianza."},
    {"id": "neyman-pearson",
     "nombre": "Lema de Neyman-Pearson",
     "descripcion": "El test más potente de nivel α rechaza cuando el cociente de verosimilitudes L(θ₁|x)/L(θ₀|x) supera un umbral k."},
    {"id": "delta-method",
     "nombre": "Método delta",
     "descripcion": "Si √n(θ̂−θ)→N(0,σ²) y g es derivable, entonces √n(g(θ̂)−g(θ))→N(0,σ²[g'(θ)]²)."},
]
ids_heur = {h['id'] for h in s['catalogoHeuristicas']}
for h in nuevas_heur:
    if h['id'] not in ids_heur:
        s['catalogoHeuristicas'].append(h)

META = {"nivel": "avanzado", "fuente": LIBRO, "session": "2026-06-13"}

def unidad(uid, orden, titulo, objetivo, heur, skills, ideas, banco):
    return {
        "id": uid, "bloque": "fase-7", "orden": orden, "titulo": titulo,
        "libro": LIBRO, "lectura": f"data/teoria/{uid}.md",
        "dosis": f"{len(banco)} preguntas · Statistical Inference (Casella & Berger)",
        "objetivo": objetivo, "heuristicas": heur,
        "metadata": {"ruta": "estadistica", "nivel": "avanzado", "skills": skills,
                     "fuente": LIBRO, "session": "2026-06-13"},
        "ideas_clave": ideas, "banco": banco,
    }

def q(uid, n, tipo, enun, sol, exp):
    return {"id": f"{uid}-q{n}", "tipo": tipo, "enunciado": enun,
            "solucion": sol, "explicacion": exp}

unidades = []

# ===================== arena-cb1: Suficiencia y completitud =====================
uid = "arena-cb1"
banco = [
 q(uid,1,"quiz",
   "X₁,…,Xₙ i.i.d. con f(xᵢ|θ) = e^{iθ−xᵢ} · I(xᵢ≥iθ), i=1,…,n. Muestra que T = min(Xᵢ/i) es suficiente para θ usando el criterio de factorización.",
   "T = min(Xᵢ/i). La densidad conjunta es ∏e^{iθ−xᵢ}·I(xᵢ≥iθ) = exp(nθ·(n+1)/2−Σxᵢ)·I(min(xᵢ/i)≥θ). Esto es g(T,θ)·h(x) con g=exp(θΣi·I(T≥θ)) y h=exp(−Σxᵢ).",
   "El indicador I(xᵢ≥iθ) para todo i equivale a I(min(xᵢ/i)≥θ), así que T colapsa todos los indicadores en uno solo que involucra a θ. Por factorización, T es suficiente."),
 q(uid,2,"quiz",
   "X₁,…,Xₙ i.i.d. Geométrica: P(X=x|θ)=θ(1−θ)^{x−1}, x=1,2,… Muestra que ΣXᵢ es suficiente. ¿Es la familia completa?",
   "Suficiencia: la función de masa conjunta es θⁿ(1−θ)^{Σxᵢ−n} = g(ΣXᵢ,θ)·1 (h=1). Por factorización, T=ΣXᵢ es suficiente. Completitud: E_θ[g(T)]=Σ_{t=n}^∞ g(t)θⁿ(1−θ)^{t−n}·C(t,n)=0 para todo θ∈(0,1) implica g(t)=0 para todo t≥n (es una familia exponencial de rango completo).",
   "Toda familia de un parámetro en la forma exponencial con rango de parámetro natural abierto tiene estadístico suficiente completo. La geométrica cumple esto."),
 q(uid,3,"quiz",
   "Demuestra que para X₁,…,Xₙ i.i.d. N(θ, aθ²) con a>0 conocido, T=(ΣXᵢ, ΣXᵢ²) es suficiente pero NO completo.",
   "Suficiente: la familia exponencial bivariada tiene T=(ΣXᵢ, ΣXᵢ²). No completo: el parámetro natural (θ/σ², 1/(2σ²)) = (1/(aθ), 1/(2aθ²)) está en una curva (no un abierto de ℝ²). La función g(T)=ΣXᵢ²−a(ΣXᵢ)²/n − aθ² satisface E[g(T)]=0 para todo θ pero g≢0.",
   "La completitud falla cuando el espacio paramétrico natural no contiene un abierto: las restricciones entre parámetros crean funciones g≠0 con esperanza cero. Es el contraejemplo estándar de Casella & Berger §6.2."),
 q(uid,4,"quiz",
   "Sea f(x|θ) = (1/2θ)·I(−θ<x<θ), θ>0. Encuentra el estadístico minimal suficiente para θ.",
   "T = max(|X₁|,…,|Xₙ|) = X₍ₙ₎^{|·|}. El cociente L(θ|x)/L(θ|y)=(1/2θ)ⁿ/(1/2θ)ⁿ=1 (constante) si y solo si max|xᵢ|=max|yᵢ|, luego T=max|Xᵢ| es minimal suficiente.",
   "Para familias uniformes sobre intervalos que dependen de θ, el estadístico de orden extremo (o una función de él) es el candidato natural. El criterio de cociente de verosimilitudes confirma la minimalidad."),
 q(uid,5,"quiz",
   "Enuncia el teorema de Basu y aplícalo: X₁,…,Xₙ i.i.d. N(μ,σ²) con ambos parámetros desconocidos. Muestra que X̄ y S² son independientes.",
   "Basu: si T es completo suficiente y V es ancilario, entonces T⊥V. Con σ² conocida: T=ΣXᵢ es completo suficiente para μ; V=S²=(1/(n−1))Σ(Xᵢ−X̄)² es ancilario para μ (distribución σ²χ²_{n−1}/(n−1), no depende de μ). Por Basu, X̄⊥S² — y esto se mantiene cuando σ² es desconocida.",
   "El argumento requiere T completo (no solo suficiente). La distribución de S² depende de σ² pero no de μ, lo que lo hace ancilario para μ. Basu entonces da la independencia sin cálculo directo."),
 q(uid,6,"quiz",
   "X₁,…,Xₙ i.i.d. Uniform(θ, 2θ), θ>0. Encuentra el estadístico minimal suficiente y discute su completitud.",
   "Minimal suficiente: T=(X₍₁₎, X₍ₙ₎) = (min, max). El cociente de verosimilitudes es 1 ↔ min(x)/min(y)=max(x)/max(y), que equivale a T(x)=T(y) (comprueba la condición de Lehmann-Scheffé). Para completitud: el espacio paramétrico es {θ>0}, que forma una curva en el espacio de (X₍₁₎,X₍ₙ₎) pues ambos deben tener la razón max/min. La familia NO es de rango completo en ℝ².",
   "La uniforme U(θ,2θ) es un caso clásico donde el estadístico minimal suficiente es bidimensional pero la familia no es completa porque los parámetros naturales están restringidos a una curva."),
 q(uid,7,"quiz",
   "X₁,…,Xₙ i.i.d. con f(x|θ) = θx^{θ−1}, 0<x<1, θ>0. (a) Encuentra el estadístico suficiente completo. (b) ¿Qué función de T es el UMVUE de 1/θ?",
   "(a) T=ΣlogXᵢ es suficiente y completo (familia exponencial, un parámetro). (b) Para encontrar el UMVUE de 1/θ: T~Gamma(n,1/θ) (suma de exponenciales con parámetro θ). Necesitamos φ(T) insesgada: E[φ(T)]=1/θ. Prueba φ(T)=−T/n: E[−T/n]=−(1/θ)·n/n=−1/θ... no. Correcto: E[T]=n/θ, así que E[T/n]=1/θ pero T/n=ΣlogXᵢ/n... Espera: −Σlog Xᵢ ~ Gamma(n,1/θ), con E[−ΣlogXᵢ]=n/θ. Así φ(T)=−T/n = −ΣlogXᵢ/n es insesgado para 1/θ y función de T completo suficiente → es el UMVUE.",
   "Usamos que si T~Gamma(n,β), E[T]=nβ, y aquí T=−ΣlogXᵢ~Gamma(n,1/θ), así que E[T/n]=1/θ. El UMVUE de 1/θ es −ΣlogXᵢ/n."),
]
unidades.append(unidad(uid, 35, "Arena Inferencia · Suficiencia, completitud y Basu",
 "Identificar estadísticos suficientes por factorización, distinguir suficiencia de completitud, y usar el teorema de Basu para establecer independencias.",
 ["factorizacion-suficiente", "rao-blackwell"],
 ["suficiencia", "completitud", "estadísticos ancilarios", "teorema de Basu", "familias exponenciales"],
 ["Factorización: f(x|θ)=g(T(x),θ)·h(x) ↔ T suficiente.",
  "Familias exponenciales de rango completo tienen T suficiente completo.",
  "Basu: T completo suficiente ⊥ V ancilario → X̄ ⊥ S² en la normal.",
  "No completo: parámetro natural restringido a curva (no abierto de ℝᵏ).",
  "Minimal suficiente: cociente de verosimilitudes constante ↔ T(x)=T(y)."],
 banco))

# ===================== arena-cb2: MLE, CR y UMVUE =====================
uid = "arena-cb2"
banco = [
 q(uid,1,"quiz",
   "X₁,…,Xₙ i.i.d. Uniform[0,θ]. (a) Halla el MLE θ̂. (b) Calcula su sesgo. (c) Da un estimador insesgado basado en θ̂. (d) Compara los MSE del MLE y del estimador insesgado.",
   "(a) θ̂=X₍ₙ₎=max(Xᵢ). (b) E[X₍ₙ₎]=nθ/(n+1), Sesgo=−θ/(n+1). (c) θ*=[(n+1)/n]X₍ₙ₎. (d) MSE(θ̂)=2θ²/((n+1)(n+2)), MSE(θ*)=θ²/(n(n+2)). Comparando: 2/(n+1) vs 1/n para el factor en θ². Para n≥1: θ* tiene menor MSE que θ̂.",
   "El MLE de la uniforme no es insesgado pero tiene menor varianza que el estimador insesgado por método de momentos. El estimador insesgado θ* tampoco domina a θ̂ en MSE para n pequeño — ahí el sesgo del MLE es relativamente grande."),
 q(uid,2,"quiz",
   "X₁,…,Xₙ i.i.d. con f(x|θ) = θx^{θ−1}, 0<x<1, θ>0. Halla el MLE de θ y muestra que su varianza → 0 conforme n→∞.",
   "MLE: ℓ(θ)=n log θ+(θ−1)Σlog xᵢ. Derivando: n/θ+Σlog xᵢ=0 → θ̂=−n/Σlog Xᵢ. Varianza: I(θ)=1/θ², así que Var(θ̂) ≈ θ²/n → 0 por la eficiencia asintótica del MLE.",
   "Como T=−ΣlogXᵢ~Gamma(n,1/θ), el MLE es θ̂=n/T. Por el método delta con g(t)=n/t: Var(θ̂)≈(n/T)²·Var(T)/n → θ²/n conforme n→∞."),
 q(uid,3,"quiz",
   "X₁,…,Xₙ i.i.d. con densidad doble exponencial f(x|θ)=(1/2)e^{−|x−θ|}. Muestra que el MLE de θ es la mediana muestral.",
   "ℓ(θ)=−n log 2−Σ|xᵢ−θ|. Maximizar ℓ equivale a minimizar Σ|xᵢ−θ|. Esta función (suma de distancias absolutas) alcanza su mínimo en la mediana muestral. Para n par, en el intervalo [x₍n/2₎, x₍n/2+1₎]; para n impar, en x₍(n+1)/2₎.",
   "La log-verosimilitud de la doble exponencial no es diferenciable en los puntos de dato. El argumento de minimización de suma de distancias absolutas es el estándar: la derivada vale Σ sign(xᵢ−θ), que cambia de signo en la mediana."),
 q(uid,4,"quiz",
   "X₁,…,Xₙ i.i.d. Bernoulli(p). Demuestra que X̄ alcanza la cota de Cramér-Rao para p. ¿Cuál es la cota CR para Var(θ̂) de cualquier estimador insesgado de p?",
   "I(p)=1/(p(1−p)), cota CR para n obs: 1/(n·I(p))=p(1−p)/n. Var(X̄)=p(1−p)/n = cota CR → X̄ es eficiente. La cota se alcanza porque la Bernoulli pertenece a la familia exponencial y ∂ log f/∂p = (x−p)/(p(1−p)) = [1/(p(1−p))](x−p) es lineal en x−p, condición exacta de la cota CR.",
   "Para cualquier estimador insesgado de p con n Bernoulli, Var(estimador) ≥ p(1−p)/n. X̄ es el único estimador eficiente (alcanza la cota) y es el UMVUE."),
 q(uid,5,"quiz",
   "X₁,…,Xₙ i.i.d. N(θ,1). Halla el UMVUE de θ² y calcula su varianza. ¿Supera la cota CR para θ²?",
   "T=ΣXᵢ es completo suficiente. Como E[X̄²]=θ²+1/n, el UMVUE de θ² es φ(T)=X̄²−1/n. Varianza: Var(X̄²−1/n)=Var(X̄²)=E[X̄⁴]−(θ²+1/n)². Con X̄~N(θ,1/n), se obtiene Var=4θ²/n+2/n². Cota CR para τ(θ)=θ²: [τ'(θ)]²/(n·I(θ))=(2θ)²/(n·1)=4θ²/n. La varianza del UMVUE es 4θ²/n+2/n² > 4θ²/n — NO alcanza la cota CR.",
   "Este es el ejemplo clave de C&B: el UMVUE puede no alcanzar la cota CR. La cota CR es una cota inferior para TODOS los estimadores insesgados, pero solo la alcanza cuando la familia exponencial lo permite (i.e., cuando la ecuación de puntuación es lineal en τ̂)."),
 q(uid,6,"quiz",
   "X₁,…,Xₙ i.i.d. Bernoulli(p). Usa Rao-Blackwell para mejorar el estimador δ(X₁)=X₁ de p y obtener el UMVUE. ¿Qué estimador resulta?",
   "T=ΣXᵢ es completo suficiente. E[X₁|T=t] = P(X₁=1|ΣXᵢ=t) = t/n (por la simetría de la distribución multinomial condicional: dado que hay t éxitos entre n ensayos, la probabilidad de que el primero sea éxito es t/n). Luego φ(T)=T/n=X̄ es el UMVUE.",
   "Rao-Blackwell en acción: el estimador mejorado E[δ(X₁)|T] resulta ser X̄, que ya sabíamos era el UMVUE. Este cálculo confirma que X̄ es el mejor insesgado no por inspección sino por el teorema."),
 q(uid,7,"quiz",
   "Para la distribución Gamma(α,β) con α conocido, halla el MLE de β y verifica que alcanza la cota de Cramér-Rao.",
   "f(x|β)=(1/Γ(α)βᵅ)xᵅ⁻¹e^{−x/β}. Log-verosimilitud: ℓ(β)=−nα log β−(1/β)Σxᵢ+cte. Ecuación de puntuación: −nα/β+Σxᵢ/β²=0 → β̂=X̄/α. Info de Fisher: I(β)=α/β². Var(β̂)=Var(X̄/α)=β²/(nα). Cota CR: 1/(n·I(β))=β²/(nα). Coinciden → β̂ alcanza la cota CR.",
   "La Gamma pertenece a la familia exponencial y el estadístico suficiente T=ΣXᵢ permite que la ecuación de puntuación sea lineal en T: ∂ℓ/∂β = −nα/β + T/β² = (α/β²)(T/α−β). La linealidad en T es la condición exacta de la cota CR."),
]
unidades.append(unidad(uid, 36, "Arena Inferencia · MLE, Cramér-Rao y UMVUE",
 "Calcular MLEs de distribuciones clave, verificar si alcanzan la cota de Cramér-Rao, y construir el UMVUE via Rao-Blackwell y Lehmann-Scheffé.",
 ["rao-blackwell", "factorizacion-suficiente"],
 ["MLE", "información de Fisher", "cota Cramér-Rao", "UMVUE", "Rao-Blackwell", "Lehmann-Scheffé"],
 ["MLE de doble exponencial = mediana muestral (minimiza distancias absolutas).",
  "Cota CR: Var(τ̂)≥[τ'(θ)]²/(n·I(θ)); se alcanza ↔ puntuación lineal en τ̂.",
  "UMVUE: cualquier función insesgada de T completo suficiente es el UMVUE.",
  "Rao-Blackwell: E[δ|T] siempre es ≥ tan bueno como δ.",
  "El UMVUE puede NO alcanzar la cota CR (ej: θ² en N(θ,1))."],
 banco))

# ===================== arena-cb3: NP, LRT y UMP =====================
uid = "arena-cb3"
banco = [
 q(uid,1,"quiz",
   "En 1000 lanzamientos de una moneda salen 560 caras. ¿Es razonable que la moneda sea justa? Plantea un test de hipótesis formal y calcula el p-valor.",
   "H₀: p=0.5 vs H₁: p≠0.5. Estadístico: z=(560−500)/√(1000·0.5·0.5)=(60/√250)≈3.79. p-valor=2P(Z>3.79)≈0.00015. Rechazamos H₀ a cualquier nivel razonable; hay evidencia fuerte de que la moneda no es justa.",
   "Con n=1000 por el TLC: p̂~N(0.5, 0.25/1000). El z-score de 3.79 supera z_{0.025}=1.96 con creces. Un p-valor de 0.015% indica que si la moneda fuera justa, 560+ caras sería extremadamente improbable."),
 q(uid,2,"quiz",
   "Enuncia el Lema de Neyman-Pearson y aplícalo: X₁,…,Xₙ i.i.d. N(μ,1). Test H₀: μ=0 vs H₁: μ=1. ¿Cuál es el test más potente de nivel α=0.05?",
   "NP: rechaza H₀ cuando L(1|x)/L(0|x)>k. El cociente es exp(−n/2+Σxᵢ), creciente en Σxᵢ=nX̄. Rechaza si X̄>k'. Con H₀, nX̄~N(0,n), así que X̄~N(0,1/n). P(X̄>k')=0.05 → k'=z_{0.05}/√n. Test: rechaza si X̄ > 1.645/√n. Potencia: β(1)=P_{μ=1}(X̄>1.645/√n)=P(Z>1.645−√n).",
   "El cociente de verosimilitudes para la normal con varianza conocida siempre resulta en un test basado en X̄. El Lema NP garantiza que no hay test de nivel α con mayor potencia contra μ=1."),
 q(uid,3,"quiz",
   "X₁,…,Xₙ i.i.d. Poisson(λ). Encuentra el test UMP de nivel α para H₀: λ≤λ₀ vs H₁: λ>λ₀.",
   "La familia Poisson tiene MLR en ΣXᵢ (la densidad conjunta es proporional a λ^{Σxᵢ}e^{−nλ}, creciente en ΣXᵢ para λ₂>λ₁). Por el corolario del MLR, el test UMP rechaza si ΣXᵢ>c, donde P_{λ₀}(ΣXᵢ>c)=α. Como ΣXᵢ~Poisson(nλ₀), c se encuentra con tablas Poisson.",
   "Para la Poisson con MLR en ΣXᵢ, el test UMP para hipótesis unilateral es simplemente 'rechaza si ΣXᵢ demasiado grande'. Para niveles exactos en distribuciones discretas, se usa a veces un test aleatorizado: rechaza con probabilidad γ cuando ΣXᵢ=c."),
 q(uid,4,"quiz",
   "X~Beta(θ,1), f(x|θ)=θx^{θ−1}, 0<x<1, θ>0. Encuentra el test UMP de nivel α para H₀: θ≤1 vs H₁: θ>1 basado en UNA observación.",
   "La densidad tiene MLR en logX: f(x|θ₂)/f(x|θ₁)=(θ₂/θ₁)x^{θ₂−θ₁} es creciente en log x cuando θ₂>θ₁. Test UMP: rechaza si log X > c, i.e., si X > e^c. Tamaño: P_{θ=1}(X > c) = 1−c (bajo θ=1, f(x|1)=1, uniforme[0,1]). Así c=1−α. Test: rechaza si X > 1−α.",
   "El truco es reconocer que logX juega el papel del estadístico suficiente ordenador. Bajo H₀: θ=1, X~Uniform[0,1], así que calibrar el nivel es trivial."),
 q(uid,5,"quiz",
   "X₁,…,Xₙ i.i.d. N(μ,σ²) con σ² desconocida. Deriva el LRT para H₀: μ=μ₀ vs H₁: μ≠μ₀ y muestra que equivale al test t.",
   "LRT: λ(x)=sup_{μ=μ₀}L/(sup_μ L). Numerador: MLE bajo H₀ son μ=μ₀, σ̂₀²=(1/n)Σ(xᵢ−μ₀)². Denominador: μ̂=X̄, σ̂²=(1/n)Σ(xᵢ−X̄)². El cociente λ=(σ̂²/σ̂₀²)^{n/2}=(1+t²/(n−1))^{−n/2} donde t=(X̄−μ₀)/(S/√n). Rechaza si λ<k ↔ |t|>c. Bajo H₀, T~t_{n−1}.",
   "El álgebra muestra que Σ(xᵢ−μ₀)²=Σ(xᵢ−X̄)²+n(X̄−μ₀)²=(n−1)S²+nT̄², y el cociente simplifica en función de T. Este es el test t de Student derivado formalmente desde primeros principios."),
 q(uid,6,"quiz",
   "Dos muestras independientes: X₁,…,Xₙ~N(μ_X,σ²) y Y₁,…,Yₘ~N(μ_Y,σ²) con σ² desconocida y común. Indica el LRT para H₀: μ_X=μ_Y y da su distribución bajo H₀.",
   "El LRT conduce al estadístico t de dos muestras: T=(X̄−Ȳ)/[Sₚ√(1/n+1/m)], donde Sₚ²=[(n−1)S_X²+(m−1)S_Y²]/(n+m−2) es la varianza pooled. Bajo H₀, T~t_{n+m−2}. Rechaza H₀ si |T|>t_{n+m−2,α/2}.",
   "La derivación del LRT para dos medias con varianza común pooled conduce exactamente al test t de Welch/Student de dos muestras. La varianza pooled Sₚ² combina las dos estimaciones de σ² ponderando por sus grados de libertad."),
 q(uid,7,"quiz",
   "Se desea un test de nivel α=0.05 para H₀: μ=μ₀ vs H₁: μ=μ₁>μ₀ en N(μ,σ²) con σ² conocida, con potencia β*=0.90 en μ=μ₁=μ₀+δ. ¿Cuántas observaciones se necesitan?",
   "El test es: rechaza si Z=(X̄−μ₀)/(σ/√n)>z_α=1.645. La potencia en μ₁: β(μ₁)=P_{μ₁}(Z>z_α)=P(Z>z_α−δ√n/σ)=1−Φ(z_α−δ√n/σ)=0.90. Entonces z_α−δ√n/σ=−z_{0.10}=−1.282. Despejando: n=σ²(z_α+z_{0.10})²/δ²=σ²(1.645+1.282)²/δ²≈σ²·8.56/δ².",
   "La fórmula n=(z_α+z_{β*})²σ²/δ² es la estándar para el diseño del tamaño de muestra. Aquí δ=μ₁−μ₀ es el efecto a detectar. Con α=0.05 y potencia=0.90: n≈(2.927)²σ²/δ²≈8.57σ²/δ²."),
]
unidades.append(unidad(uid, 37, "Arena Inferencia · NP Lemma, LRT y tests UMP",
 "Construir tests más potentes via NP Lemma, identificar cuándo existe test UMP usando MLR, derivar el LRT y calcular su distribución asintótica.",
 ["neyman-pearson", "factorizacion-suficiente"],
 ["Lema NP", "tests UMP", "MLR", "LRT", "potencia", "p-valor", "tamaño de muestra"],
 ["NP Lemma: rechaza si L(θ₁|x)/L(θ₀|x)>k; la región es función de T suficiente.",
  "MLR → UMP unilateral: rechaza si T>c (o T<c según el sentido).",
  "No existe UMP bilateral en general; sí UMP entre tests no sesgados.",
  "LRT: −2 log λ →_d χ²_r (r = diferencia de dimensiones).",
  "Diseño: n=(z_α+z_{β*})²σ²/δ² para detectar diferencia δ con potencia β*."],
 banco))

# ===================== arena-cb4: CIs, pivot y delta method =====================
uid = "arena-cb4"
banco = [
 q(uid,1,"quiz",
   "X₁,…,Xₙ i.i.d. N(μ,σ²) con σ² desconocida. Construye un IC de nivel 95% para μ identificando el pivote y despejando μ.",
   "Pivote: T=(X̄−μ)/(S/√n)~t_{n−1} (no depende de μ ni σ²). P(−t_{n−1,0.025}≤T≤t_{n−1,0.025})=0.95. Despejando μ: X̄−t_{n−1,0.025}·S/√n ≤ μ ≤ X̄+t_{n−1,0.025}·S/√n. IC: [X̄ ± t_{n−1,0.025}·S/√n].",
   "La clave es que T no depende del parámetro desconocido σ². El t-estadístico es el pivote correcto para la media normal cuando σ² es desconocida; con σ² conocida, usaríamos Z~N(0,1)."),
 q(uid,2,"quiz",
   "X₁,…,Xₙ i.i.d. Uniform[0,θ]. (a) Muestra que Q=X₍ₙ₎/θ es un pivote. (b) Halla el IC de nivel 1−α más corto posible.",
   "(a) Q=X₍ₙ₎/θ~Beta(n,1), densidad nq^{n−1} en (0,1): no depende de θ. (b) Intervalo de nivel 1−α: P(a≤Q≤1)=1−α → a^n=α → a=α^{1/n}. El IC es [X₍ₙ₎, X₍ₙ₎/α^{1/n}]. Es el más corto porque la densidad de Beta(n,1) es monótona creciente: la región de máxima densidad está concentrada cerca de 1.",
   "El pivot Beta(n,1) tiene densidad creciente, así que el intervalo más corto de nivel 1−α es el del extremo derecho: [α^{1/n}, 1]. Inversamente, θ∈[X₍ₙ₎, X₍ₙ₎/α^{1/n}]. Para n=10, α=0.05: α^{1/n}≈0.741 → IC de longitud relativa ≈35%."),
 q(uid,3,"quiz",
   "X₁,…,Xₙ i.i.d. Exponencial(λ). Construye un IC de nivel 1−α para λ invirtiendo el test UMP de H₀: λ=λ₀.",
   "El test UMP para H₀: λ≤λ₀ rechaza si 2λ₀ΣXᵢ>χ²_{2n,α}. El IC se obtiene invirtiendo: el conjunto de λ₀ que NO rechazarían los datos es [χ²_{2n,1−α/2}/(2ΣXᵢ), χ²_{2n,α/2}/(2ΣXᵢ)]. Pivot: 2λΣXᵢ~χ²_{2n} (pues ΣXᵢ~Gamma(n,1/λ)).",
   "La inversión del test UMP da automáticamente el IC UMA (Uniformly Most Accurate), que tiene la menor longitud media entre todos los IC de nivel 1−α. El pivot chi-cuadrado con 2n grados de libertad aparece porque ΣXᵢ~Gamma(n,1/λ) y 2λΣXᵢ~Gamma(n,1)=χ²_{2n}."),
 q(uid,4,"quiz",
   "Enuncia el método delta y aplícalo: X₁,…,Xₙ i.i.d. Bernoulli(p) y queremos un IC de nivel 95% para el logit log(p/(1−p)).",
   "Delta method: si √n(p̂−p)→N(0,p(1−p)) y g(p)=log(p/(1−p)), entonces √n(g(p̂)−g(p))→N(0,p(1−p)·[g'(p)]²). Derivada: g'(p)=1/(p(1−p)). Varianza asintótica de g(p̂): p(1−p)·[1/(p(1−p))]²=1/(p(1−p)). IC: g(p̂) ± 1.96/√(n·p̂(1−p̂)) = log(p̂/(1−p̂)) ± 1.96/√(n·p̂(1−p̂)).",
   "La transformación logit estabiliza la varianza en los extremos (p cerca de 0 o 1), donde el IC normal para p puede salir de [0,1]. El IC en escala logit se retrotransforma con la función logística para obtener un IC para p acotado en (0,1)."),
 q(uid,5,"quiz",
   "X₁,…,Xₙ i.i.d. N(μ,σ²) con σ² conocida. ¿Cuál es el mínimo n para garantizar que un IC del 95% para μ tenga longitud no mayor que δ?",
   "IC 95%: longitud=2·z_{0.025}·σ/√n=2·1.96σ/√n. Para longitud ≤ δ: n ≥ (2·1.96σ/δ)² = (3.92σ/δ)². Fórmula: n ≥ ⌈(3.92σ)²/δ²⌉. Si σ desconocida: usa σ̂ del piloto o el bound peor caso con rango/4 (para muestras pequeñas de normal).",
   "En diseño de estudios, antes de recolectar datos se especifica la precisión deseada δ (semi-longitud) y se calcula n. Si σ es desconocida, se usa S de un piloto o la regla de Stein en dos etapas."),
 q(uid,6,"quiz",
   "El coeficiente de correlación muestral r̂ de una muestra de tamaño n tiene la propiedad de que su distribución es complicada cuando ρ≠0. Aplica el método delta a la transformación de Fisher z=arctanh(r̂) para dar un IC asintótico para ρ.",
   "Por el método delta con g(r)=arctanh(r) y g'(r)=1/(1−r²): √n(z−ρ*)→N(0,1) donde ρ*=arctanh(ρ). De hecho, la varianza exacta de arctanh(r̂) es ≈1/(n−3) (Fisher 1921). IC para arctanh(ρ): arctanh(r̂) ± z_{α/2}/√(n−3). Retrotransforma: ρ ∈ [tanh(L), tanh(U)].",
   "La transformación de Fisher estabiliza la varianza de r̂ de forma que arctanh(r̂) es aproximadamente N(arctanh(ρ), 1/(n−3)) para cualquier ρ. Sin esto, el IC de r̂ sería muy inexacto, especialmente para |ρ| grande."),
 q(uid,7,"quiz",
   "X₁,…,Xₙ i.i.d. N(μ,σ²) con ambos desconocidos. Usa la desigualdad de Bonferroni para construir un IC simultáneo de nivel 90% para (μ, σ²).",
   "Construye ICs individuales de nivel 95% (α/2=5%) para cada parámetro. IC para μ: X̄ ± t_{n−1,0.025}·S/√n. IC para σ²: [(n−1)S²/χ²_{n−1,0.025}, (n−1)S²/χ²_{n−1,0.975}]. Por Bonferroni: P(ambos contienen) ≥ 1−0.05−0.05=0.90.",
   "La desigualdad de Bonferroni: P(∩Aᵢ) ≥ 1−Σ P(Aᵢᶜ). Usar α/k=0.05 en cada uno de k=2 ICs garantiza nivel conjunto ≥ 1−k·(α/k)=1−α=0.90. Los ICs individuales son independientes en la normal (por el teorema de Fisher), así que el nivel conjunto exacto es 0.95²≈0.9025."),
]
unidades.append(unidad(uid, 38, "Arena Inferencia · Intervalos de confianza y métodos asintóticos",
 "Construir ICs exactos usando pivotes, CIs asintóticos via delta method, y CIs óptimos invirtiendo tests UMP.",
 ["delta-method", "neyman-pearson"],
 ["pivotes", "intervalos de confianza", "delta method", "inferencia asintótica", "Bonferroni"],
 ["Pivot: Q(X,θ) con distribución conocida → despeja θ de P(a≤Q≤b)=1−α.",
  "IC por inversión: C(x)={θ₀: test de H₀:θ=θ₀ no rechaza x} → UMA si inviertes UMP.",
  "Delta method: Var(g(θ̂))≈[g'(θ)]²·Var(θ̂) asintóticamente.",
  "Logit(p̂) ± 1.96/√(n·p̂(1−p̂)) acota el logit; arctanh(r̂) ± z/√(n−3) para correlación.",
  "Tamaño muestral: n=(z_{α/2}·σ/(δ/2))² para longitud de IC ≤ δ."],
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
 {"id":"f7-ex-27","heuristica":"factorizacion-suficiente",
  "enunciado":"X₁,…,Xₙ i.i.d. con f(x|θ)=θxᶿ⁻¹, 0<x<1, θ>0. (a) Usa el criterio de factorización para hallar T suficiente. (b) Muestra que T es completo. (c) Halla el UMVUE de 1/θ.",
  "pistas":pista(
    "Escribe la densidad conjunta y busca separar la parte que involucra θ de la que solo involucra x.",
    "f(x₁,…,xₙ|θ)=θⁿ·exp((θ−1)Σlog xᵢ). ¿Qué función de los xᵢ aparece junto a θ?",
    "Por factorización, T=Σlog Xᵢ es suficiente. La familia es exponencial con parámetro natural θ en un abierto → T es completo.",
    "T=Σlog Xᵢ~−Gamma(n,1/θ): −log Xᵢ~Exp(θ). Así E[T]=n/θ. ¿Qué función de T tiene esperanza 1/θ?",
    "−T/n=−ΣlogXᵢ/n es insesgado para 1/θ y función de T completo suficiente → es el UMVUE."),
  "solucion":"T=ΣlogXᵢ es suficiente y completo. −ΣlogXᵢ/n es el UMVUE de 1/θ, pues E[−ΣlogXᵢ/n]=1/θ y es función de T completo suficiente (Lehmann-Scheffé).",
  "disparador":"Señal: 'familia de potencias f(x|θ)=θxᶿ⁻¹'. Jugada: log-verosimilitud lineal en T=ΣlogXᵢ → factorización inmediata. Para UMVUE: E[T/n]=1/θ, invertir la relación.",
  "metadata":{"ruta":"estadistica","nivel":"avanzado",
    "skills":["suficiencia","completitud","UMVUE","Lehmann-Scheffé"],
    "errores_comunes":["Proponer T=ΣXᵢ en lugar de T=ΣlogXᵢ","Olvidar verificar completitud antes de aplicar Lehmann-Scheffé"],
    "casos_borde":["Con n=1, T=logX₁~−Exp(θ) y −logX₁ es UMVUE de 1/θ"],
    "source":LIBRO}},
 {"id":"f7-ex-28","heuristica":"rao-blackwell",
  "enunciado":"X₁,…,Xₙ i.i.d. N(θ,1). El UMVUE de θ² es φ(T)=X̄²−1/n donde T=ΣXᵢ. (a) Verifica que φ(T) es insesgado. (b) Calcula su varianza. (c) Compara con la cota de Cramér-Rao para θ². ¿La alcanza?",
  "pistas":pista(
    "E[X̄²] = Var(X̄) + (E[X̄])² = 1/n + θ². ¿Qué implica esto para φ(T)=X̄²−1/n?",
    "E[φ(T)] = E[X̄²]−1/n = (1/n+θ²)−1/n = θ². Insesgado: ✓.",
    "Para la varianza: X̄~N(θ,1/n), así X̄²~χ²₁ no central. Var(X̄²)=E[X̄⁴]−(θ²+1/n)². Usa E[X̄⁴]=3/n²+6θ²/n+θ⁴ (4to momento de N(θ,1/n)).",
    "Var(X̄²−1/n)=Var(X̄²)=(3/n²+6θ²/n+θ⁴)−(θ²+1/n)² = 2/n²+4θ²/n.",
    "Cota CR para τ(θ)=θ²: [τ'(θ)]²/(n·I(θ))=(2θ)²/(n·1)=4θ²/n. Comparar: Var(φ)=4θ²/n+2/n² > cota CR."),
  "solucion":"φ(T)=X̄²−1/n es insesgado (E=θ²). Var(φ)=4θ²/n+2/n². Cota CR=4θ²/n. El UMVUE NO alcanza la cota CR (excede en 2/n²). Esto muestra que el UMVUE puede ser sub-eficiente respecto a la cota CR.",
  "disparador":"Señal: 'UMVUE de función cuadrática del parámetro'. Jugada: verifica E[T²]=Var(T)+(E[T])² para descentrar. El UMVUE de θ² en N(θ,1) es el ejemplo estándar de UMVUE que no alcanza la cota CR.",
  "metadata":{"ruta":"estadistica","nivel":"avanzado",
    "skills":["UMVUE","cota Cramér-Rao","normalidad"],
    "errores_comunes":["Creer que el UMVUE siempre alcanza la cota CR","Confundir E[X̄²] con (E[X̄])²"],
    "casos_borde":["Si τ(θ)=θ (lineal), el UMVUE sí alcanza la cota CR para la normal"],
    "source":LIBRO}},
 {"id":"f7-ex-29","heuristica":"neyman-pearson",
  "enunciado":"X₁,…,Xₙ i.i.d. N(μ,σ²) con σ² conocida. Usa el Lema de Neyman-Pearson para derivar el test más potente de nivel α para H₀:μ=μ₀ vs H₁:μ=μ₁>μ₀, y calcula su función de potencia.",
  "pistas":pista(
    "Escribe el cociente de verosimilitudes L(μ₁|x)/L(μ₀|x) para la normal.",
    "L(μ₁)/L(μ₀) = exp([(μ₁−μ₀)/σ²]Σxᵢ − n(μ₁²−μ₀²)/(2σ²)). ¿En qué estadístico es esto creciente?",
    "El cociente es función creciente de Σxᵢ (o X̄), pues μ₁>μ₀. NP: rechaza si X̄>k'.",
    "Calcula k': bajo H₀, X̄~N(μ₀,σ²/n). P(X̄>k')=α → k'=μ₀+z_α·σ/√n.",
    "Potencia: β(μ₁)=P_{μ₁}(X̄>k')=P(Z>z_α−(μ₁−μ₀)√n/σ)=1−Φ(z_α−(μ₁−μ₀)√n/σ)."),
  "solucion":"Rechaza H₀ si X̄>μ₀+z_α·σ/√n. Potencia: β(μ₁)=1−Φ(z_α−δ√n/σ) con δ=μ₁−μ₀. Es además el test UMP para H₀:μ≤μ₀ (porque la normal tiene MLR en X̄).",
  "disparador":"Señal: 'normal, varianza conocida, test unilateral'. Jugada: el cociente de verosimilitudes es creciente en X̄ → NP da el test z. La MLR extiende el resultado a H₀:μ≤μ₀ (UMP).",
  "metadata":{"ruta":"estadistica","nivel":"avanzado",
    "skills":["NP Lemma","UMP","potencia","diseño de tests"],
    "errores_comunes":["Olvidar que NP solo da el test más potente para H₁ simple; UMP requiere MLR","Calcular la potencia bajo H₀ en lugar de bajo H₁"],
    "casos_borde":["Si μ₁<μ₀, el test más potente rechaza si X̄<k' (sentido contrario)"],
    "source":LIBRO}},
 {"id":"f7-ex-30","heuristica":"neyman-pearson",
  "enunciado":"X~Beta(θ,1) (una sola observación). Encuentra el test de nivel α para H₀:θ=1 vs H₁:θ=2, y calcula el tipo II error.",
  "pistas":pista(
    "Escribe f(x|θ)=θx^{θ−1}. Calcula el cociente de verosimilitudes f(x|2)/f(x|1).",
    "f(x|2)/f(x|1) = 2x/1 = 2x, creciente en x. Por NP: rechaza si x>k.",
    "Tamaño: P_{θ=1}(X>k)=1−k=α (bajo θ=1, X~Uniform[0,1]). Así k=1−α.",
    "Test: rechaza H₀ si X>1−α.",
    "Error tipo II: P_{θ=2}(X≤1−α)=∫₀^{1−α} 2x dx=(1−α)². Con α=0.05: TII=(0.95)²=0.9025."),
  "solucion":"Test: rechaza si X>1−α. Error tipo II = (1−α)². Con α=0.05: TII=0.9025. El test tiene baja potencia porque con solo una observación y parámetros cercanos (1 vs 2), es difícil discriminar.",
  "disparador":"Señal: 'hipótesis simples, una observación, Beta(θ,1)'. Jugada: el cociente NP es creciente en X, lo que da un test de umbral superior. Bajo H₀:θ=1, X~Uniform → calibración trivial.",
  "metadata":{"ruta":"estadistica","nivel":"intermedio",
    "skills":["NP Lemma","error tipo II","potencia","Beta distribution"],
    "errores_comunes":["Olvidar que Beta(1,1)=Uniform[0,1]","Confundir región de rechazo con región de aceptación"],
    "casos_borde":["Con n observaciones iid Beta(θ,1): el test UMP rechaza si ΣlogXᵢ<−c"],
    "source":LIBRO}},
 {"id":"f7-ex-31","heuristica":"delta-method",
  "enunciado":"X₁,…,Xₙ i.i.d. Bernoulli(p). Quieres un IC de nivel 95% para el odds ratio ω=p/(1−p). Aplica el delta method a ω̂=p̂/(1−p̂) y da la fórmula del intervalo.",
  "pistas":pista(
    "p̂=X̄~aproximadamente N(p, p(1−p)/n). ¿A qué función g(p)=p/(1−p) corresponde ω?",
    "Calcula g'(p)=d/dp[p/(1−p)]=1/(1−p)².",
    "Por el delta method: √n(ω̂−ω) →_d N(0, p(1−p)·[1/(1−p)²]²) = N(0, p/(1−p)³).",
    "Varianza asintótica de ω̂: σ²(ω̂) ≈ p̂/(n(1−p̂)³). IC: ω̂ ± 1.96·√(p̂/n/(1−p̂)³).",
    "Equivalentemente: IC para logit log(ω)=log(p/(1−p)) con varianza 1/(n·p(1−p)) → retrotransforma."),
  "solucion":"ω̂=p̂/(1−p̂). Por delta method con g'(p)=1/(1−p)²: IC 95% es [p̂/(1−p̂) ± 1.96/√(n·p̂·(1−p̂)³)]. En la práctica es mejor trabajar con log(ω̂)=logit(p̂), que tiene varianza≈1/(n·p̂(1−p̂)), y luego exponenciar los límites.",
  "disparador":"Señal: 'IC para transformación no lineal del parámetro'. Jugada: delta method — propaga la varianza de p̂ a través de g'(p)². Para el odds ratio, es más estable usar la escala log-odds y retrotransformar.",
  "metadata":{"ruta":"estadistica","nivel":"intermedio",
    "skills":["delta method","odds ratio","intervalos de confianza"],
    "errores_comunes":["Olvidar elevar g'(p) al cuadrado","No retrotransformar si se trabaja en escala log-odds"],
    "casos_borde":["Si p̂=0 o 1, el delta method falla: usar métodos exactos (Wilson, Clopper-Pearson)"],
    "source":LIBRO}},
 {"id":"f7-ex-32","heuristica":"factorizacion-suficiente",
  "enunciado":"X₁,…,Xₙ i.i.d. Uniform[0,θ]. Demuestra que Q=X₍ₙ₎/θ~Beta(n,1) es un pivote, y construye el IC de nivel 1−α más corto para θ.",
  "pistas":pista(
    "La distribución de X₍ₙ₎=max(X₁,…,Xₙ) es Beta(n,1)·θ. ¿Por qué Q=X₍ₙ₎/θ no depende de θ?",
    "F_{X₍ₙ₎}(t)=P(todos Xᵢ≤t)=(t/θ)ⁿ para 0≤t≤θ. Así F_{Q}(q)=qⁿ para 0≤q≤1: no depende de θ. Q~Beta(n,1).",
    "Densidad de Q: f_Q(q)=nq^{n−1}. Es creciente en [0,1]. El intervalo más corto de nivel 1−α concentra probabilidad donde f_Q es mayor (cerca de 1).",
    "Intervalo: P(a≤Q≤1)=1−aⁿ=1−α → a=α^{1/n}. IC: P(α^{1/n}≤X₍ₙ₎/θ≤1)=1−α.",
    "Despeja θ: θ∈[X₍ₙ₎, X₍ₙ₎/α^{1/n}]."),
  "solucion":"Q=X₍ₙ₎/θ~Beta(n,1) (pivote exacto). IC más corto de nivel 1−α: [X₍ₙ₎, X₍ₙ₎/α^{1/n}]. Es más corto porque la densidad Beta(n,1) es creciente, concentrando probabilidad cerca de 1.",
  "disparador":"Señal: 'Uniform[0,θ], IC para θ'. Jugada: el pivote natural es X₍ₙ₎/θ~Beta(n,1); el IC más corto usa el extremo superior porque la densidad crece hacia 1. Es el IC UMA al invertir el test UMP.",
  "metadata":{"ruta":"estadistica","nivel":"avanzado",
    "skills":["pivotes","IC más corto","estadísticos de orden","distribución Beta"],
    "errores_comunes":["Usar IC simétrico para densidades asimétricas","Olvidar que Beta(n,1) tiene densidad creciente (no decreciente)"],
    "casos_borde":["Para n→∞, el IC colapsa a X₍ₙ₎ (el MLE es consistente)","IC igual-colas no es el más corto aquí"],
    "source":LIBRO}},
 {"id":"f7-ex-33","heuristica":"delta-method",
  "enunciado":"El coeficiente de correlación de Pearson r̂ tiene distribución complicada para ρ≠0. Demuestra que la transformación de Fisher z=arctanh(r̂) tiene varianza asintótica ≈1/(n−3), y da un IC de 95% para ρ.",
  "pistas":pista(
    "Por el delta method: si √n(r̂−ρ)→N(0,σ²(ρ)) y g(r)=arctanh(r), ¿cuál es la varianza asintótica de √n(g(r̂)−g(ρ))?",
    "g'(r)=1/(1−r²). Var asintótica de g(r̂): σ²(ρ)·[g'(ρ)]²=(1−ρ²)²·1/(1−ρ²)²=1. Así √(n−3)(arctanh(r̂)−arctanh(ρ))→N(0,1).",
    "El resultado exacto de Fisher (1921): arctanh(r̂) es aproximadamente N(arctanh(ρ), 1/(n−3)) para todo ρ.",
    "IC para arctanh(ρ): arctanh(r̂) ± z_{α/2}/√(n−3).",
    "IC para ρ: retrotransforma con tanh: [tanh(arctanh(r̂)−z/√(n−3)), tanh(arctanh(r̂)+z/√(n−3))]."),
  "solucion":"arctanh(r̂)≈N(arctanh(ρ), 1/(n−3)). IC 95% para ρ: [tanh(arctanh(r̂)−1.96/√(n−3)), tanh(arctanh(r̂)+1.96/√(n−3))]. La transformación de Fisher es la estabilización de varianza canónica para la correlación.",
  "disparador":"Señal: 'IC para correlación'. Jugada: transformación de Fisher arctanh estabiliza la varianza a 1/(n−3) para todo ρ. Aplica delta method con g'(r)=1/(1−r²) y la varianza exacta Var(r̂)=(1−ρ²)²/n.",
  "metadata":{"ruta":"estadistica","nivel":"avanzado",
    "skills":["delta method","correlación","transformación de Fisher","IC asintótico"],
    "errores_comunes":["Hacer IC directamente para r̂ con distribución normal (inválido para ρ≠0)","Olvidar retrotransformar los extremos del IC"],
    "casos_borde":["Para ρ=0: distribución de r̂ es simétrica y el IC normal para r̂ es razonable","Para n<10 la aproximación es pobre"],
    "source":LIBRO}},
]
f7['examen']['items'].extend(exam)

with open(SP, 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=2)
    f.write('\n')

total_banco = sum(len(u['banco']) for u in unidades)
print(f"OK: {len(unidades)} unidades, {total_banco} preguntas de banco, "
      f"{len(exam)} ítems de examen, {len(nuevas_heur)} heurísticas nuevas.")
