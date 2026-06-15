# Paradojas probabilísticas

## Las cajas de Bertrand (tres cajas)

Tres cajas: (oro, oro), (plata, plata), (oro, plata). Sacas una moneda al azar: es oro. P(la otra cara es oro):

**P = 2/3** (no 1/2)

Razonamiento correcto: hay 3 monedas de oro (cara 1, cara 2 de caja GG, y cara de caja GS). De estas 3, dos son de una caja GG (la otra cara es oro). Luego P = 2/3.

Error habitual: razonar "hay 2 cajas compatibles (GG y GS), por simetría 1/2". Error: las cajas no son equiprobables dado que extrajiste oro — la caja GG tiene el doble de probabilidad.

---

## Dos hijos (el problema clásico)

Un padre tiene 2 hijos. Versión A: "al menos uno es niño" → P(ambos niños) = **1/3**.

| Pares (orden) | P dado A |
|---------------|---------|
| (N, N) | 1/3 |
| (N, G) | 1/3 |
| (G, N) | 1/3 |

Versión B: "el hijo mayor es niño" → P(ambos niños) = **1/2** (el orden fija una coordenada).

Versión C: "uno de mis hijos, nacido martes, es niño" → P(ambos niños) = **13/27**.

Dem. de C: P = (nacido martes, al menos uno) con niño nacido martes en 27/196 del espacio → numerador: niño-niño con al menos uno nacido martes = 13/196 → P = 13/27.

La información adicional (día de nacimiento) cambia la respuesta porque rompe la simetría.

---

## Los tres prisioneros

A, B, C. Uno será liberado al azar. El guardia (que lo sabe) revela que B será ejecutado.

**P(A es el libre) sigue siendo 1/3; P(C se libra) sube a 2/3.**

Razonamiento via tabla:

| Libre | Guardia dice "B" | P posterior |
|-------|-----------------|-------------|
| A | B (prob 1/2) | 1/6 |
| B | no puede decir B | 0 |
| C | B (siempre) | 1/3 |

P(A | guardia dice B) = (1/6)/(1/6+1/3) = **1/3**; P(C | ...) = **2/3**.

Equivalente al Problema de Monty Hall.

---

## La paradoja de los dos sobres

Dos sobres: uno tiene el doble del otro. Abres uno: tiene $x. ¿Cambias?

Argumento incorrecto: E[otro] = (1/2)(x/2) + (1/2)(2x) = 5x/4 > x → siempre cambiar.

La falacia: la distribución "uniforme" que asigna probabilidad igual a x/2 y 2x implica una distribución previa impropia (P(par = 2^k) = constante para k ∈ ℤ, que no normaliza).

Con cualquier prior **propio** (integrable), el valor esperado de la diferencia es 0 — no hay ventaja en cambiar.

El paradox enseña: la expectativa condicional requiere un modelo probabilístico coherente; sin un prior válido, el cálculo es inválido.

---

## La paradoja de Simpson

Un tratamiento puede ser mejor en cada subgrupo y peor en el total:

| | Hombres | Mujeres | Total |
|---|---------|---------|-------|
| Trat. A | 18/20=90% | 2/10=20% | 20/30≈67% |
| Trat. B | 7/10=70% | 1/20=5% | 8/30≈27% |

A es mejor en hombres (90%>70%) y en mujeres (20%>5%), pero aquí B parece mejor en el total por el sesgo de asignación.

Dato real: A fue peor en el total porque los hombres (grupo con más éxito) se asignaron desproporcionadamente a A.

Lección: la asociación agregada puede revertirse al estratificar por una variable de confusión.

---

## La paradoja de la inspección

Un autobús llega cada E[τ] minutos (distribución no determinista). Llegas en un tiempo aleatorio.

**E[tiempo de espera] ≠ E[τ]/2; E[intervalo que interceptas] = E[τ²]/E[τ] ≥ E[τ]**

Para llegadas de Poisson (Exp(λ)): E[intervalo interceptado] = 2/λ = 2·E[τ] (¡el doble!).

Razón: llegas con más probabilidad durante intervalos largos (sesgo de longitud). El intervalo promedio que interceptas es mayor que el intervalo promedio.

Aplicaciones: por qué siempre parece que tu amigo tiene más amigos que tú (sesgo de red).

---

## La falacia del fiscal (prosecutor's fallacy)

DNA match: P(match | inocente) = 1/1,000,000. ¡No implica P(inocente | match) = 1/1,000,000!

Por Bayes: P(inocente | match) = P(match | inocente)·P(inocente) / P(match)

Si la ciudad tiene 1,000,000 personas y solo 1 es culpable:
- P(match) = P(match|inocente)·P(inocente) + P(match|culpable)·P(culpable)
             = (1/10^6)(999,999/10^6) + 1·(1/10^6) ≈ **2/10^6**

P(inocente | match) ≈ 1/2. ¡La evidencia por sí sola no es concluyente sin la tasa base!

---

## El hash de cumpleaños

¿Cuántos elementos se necesitan para que P(colisión) > 1/2 en una tabla de N slots?

**k ≈ 1.177·√N**

P(no colisión en k) = ∏_{i=0}^{k-1}(1−i/N) ≈ e^{-k(k-1)/(2N)} > 1/2 → k(k-1) < 2N·ln2.

Para N=365: k≈23 (el problema clásico de cumpleaños).

Para tablas hash de 2^64 slots: colisión esperada después de ~2^32 ≈ 4 mil millones de entradas.

---

## La paradoja del examen sorpresa

Un profesor anuncia: "habrá un examen sorpresa la semana que viene; no sabrán qué día hasta esa mañana".

Argumento del estudiante: "No puede ser el viernes (último día) porque lo sabríamos. Sin viernes, tampoco el jueves por la misma lógica. Por inducción: ningún día funciona. Pero el profesor puede dar el examen cualquier día." El error es el razonamiento hacia atrás que supone que el futuro es conocido dado el presente.

Formalmente: el problema enseña que "sorpresa" es un predicado que depende del conocimiento epistémico del agente, no solo de la distribución objetiva.

---

## Adivinanza de cartas (con retroalimentación)

Baraja estándar de 52 cartas. Volteas de una en una y tratas de predecir el color antes de voltear. Conoces las cartas ya voltadas. ¿Cuál es la estrategia óptima?

Intuitivamente parece que el conocimiento ayuda. Pero:

**E[aciertos con estrategia óptima] = E[aciertos con ninguna estrategia] = 26**

Dem.: en cualquier momento, P(roja | ninguna vista) = 1/2; la información solo te permite saber si queda más de un tipo, pero en promedio la predicción correcta es exactamente 26.

La estrategia no aporta nada: siempre adivinas "el color más frecuente entre los que quedan", y en esperanza esto da exactamente 26.

---

## El tanque alemán (estimación)

Seriales de tanques capturados: 1, 4, 7, 9, 12 (muestra de k=5, máximo m=12). Estimar N (producción total).

Estimador sin sesgo: **N̂ = m + m/k − 1 = m(k+1)/k − 1**

Para el ejemplo: N̂ = 12·6/5 − 1 = **13.4**. El verídico era 14.

Interpretación: m/k = densidad de muestra; asumimos distribución uniforme en {1,...,N}.

---

## La tasa de error acumulada

Si haces 1, 2, 3, … pruebas simultáneas con significancia α=5% cada una:

| Número de pruebas | P(al menos 1 error tipo I) |
|-----------------|---------------------------|
| 1 | 5% |
| 16 | ~55% |
| 100 | ~99.4% |

Corrección de Bonferroni: usa α/k por prueba para controlar la tasa familiar.

---

## Mini-ejemplo trabajado: la falacia del fiscal, con la tasa base

Un perfil de ADN coincide con el acusado; el laboratorio dice "P(coincidencia | inocente) = 1 en un millón". El fiscal concluye "luego hay 1 en un millón de que sea inocente". **Falso.** Aplica Bayes en una ciudad de 1 000 000:

- Esperados por azar entre inocentes: 1 000 000 × (1/1 000 000) ≈ 1 coincidencia inocente.
- Más la coincidencia del verdadero culpable: 1.
- P(inocente | coincidencia) ≈ 1/(1+1) = **1/2**, no 1 en un millón.

La evidencia sola, sin la tasa base de cuántos inocentes hay, no condena.

**Predicción antes de seguir:** ¿qué error cometió el fiscal? Respuesta: confundir P(coincidencia | inocente) con P(inocente | coincidencia) — invertir el condicional. Es **idéntico** a leer la sensibilidad de un test como su valor predictivo positivo: con una base enorme de "negativos reales", los falsos positivos dominan. Bayes y la tasa base son el antídoto a las tres grandes paradojas (fiscal, dos sobres, Simpson).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "evidencia rara, ¿culpable/enfermo?" → Bayes con tasa base; no inviertas el condicional.
- **Contraejemplo (Simpson):** un tratamiento mejor en cada subgrupo puede salir peor en el total si la asignación está confundida; la asociación agregada se revierte al estratificar.
- **Caso borde (adivinar cartas con feedback):** aunque conozcas las cartas vistas, E[aciertos] = 26, igual que sin estrategia; la información no ayuda en esperanza. El borde muestra que "saber más" no siempre cambia el resultado esperado.

## Errores típicos

- **Conceptual:** confundir P(A|B) con P(B|A) (fiscal); ignorar la tasa base.
- **Técnico:** usar un prior impropio (dos sobres: P(2x) y P(x/2) "iguales") que no normaliza, produciendo el falso "siempre cambiar".
- **De supuestos:** leer una asociación agregada como causal sin estratificar por la confundidora (Simpson).

## Transferencia isomorfa

- **Falacia del fiscal ↔ tasa base y VPP:** P(inocente|match) ≠ P(match|inocente) es exactamente sensibilidad ≠ VPP (conecta con [[arena-q2]]).
- **Paradoja de Simpson ↔ confounding y back-door:** la reversión al estratificar es la firma de un confundidor no ajustado (conecta con [[arena-h17]] y [[arena-h1]]).
- **Hash de cumpleaños (k≈1.177√N) ↔ colisiones y ocupación:** el mismo conteo que ~37% de cajas vacías y las colisiones de un sharding (conecta con [[arena-fc1]] y [[arena-sd2]]).
- **Tasa de error acumulada ↔ tests múltiples:** 1−(1−α)ᵏ creciendo a ~1 es la multiplicidad que corrige Bonferroni (conecta con [[arena-dg3]]).
- **Paradoja de la inspección ↔ sesgo de longitud / supervivencia:** interceptar intervalos largos con más probabilidad es el mismo sesgo que el immortal time (conecta con [[arena-h2]]).

Moraleja de la arista: *casi toda paradoja probabilística es un condicional invertido o una tasa base olvidada; Bayes es el antídoto universal.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Sacas una moneda de oro, ¿la otra cara?" | Bertrand: 2/3 (no 1/2) |
| "Un hijo es niño, ¿ambos?" | "Al menos uno": 1/3; "el mayor": 1/2 |
| "Guardia revela que B ejecutado" | Monty Hall: A se queda en 1/3 |
| "Siempre cambiar el sobre" | Falacia: prior impropio |
| "Tratamiento mejor por subgrupo" | Paradoja de Simpson: verificar confundidora |
| "E[intervalo del autobús]" | Inspección: E[τ²]/E[τ] ≥ E[τ] |
| "Match de DNA, ¿culpable?" | Tasa base: P(inocente|match) ≠ 1−p |
| "Colisión en tabla de N slots" | k ≈ 1.177·√N |

---

> **Síntesis:** Las paradojas probabilísticas exponen malentendidos del razonamiento condicional. Los tres grandes errores: (1) ignorar la tasa base (falacia del fiscal); (2) confundir P(A|B) con P(B|A); (3) mezclar priors impropios (dos sobres). El teorema de Bayes es el antídoto a todos.

---

*Retrieval: cierra y responde: (1) P(otra cara es oro en cajas de Bertrand); (2) P(ambos niños | al menos uno es niño); (3) E[intervalo interceptado para Poisson con E[τ]=10]; (4) k para P(colisión)>50% en tabla de 10,000 slots.*
