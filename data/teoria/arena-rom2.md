# Reglas de ML (Google) II: tu primer objetivo y feature engineering

## De qué trata esta lección (y qué sabrás hacer al final)

Con el pipeline ya en pie, las dos decisiones que más determinan tu primer modelo son **qué objetivo optimiza** y **con qué features**. Esta lección destila, desde cero, las Reglas 12-22 de Google en criterios concretos: por qué el primer objetivo debe ser simple y observable (y por qué no debes pedirle al ML que adivine si el usuario "es feliz"), y por qué empezar con features observadas, escaladas al tamaño de tus datos, vence a los embeddings profundos prematuros.

Al terminar podrás: (1) elegir un objetivo simple, observable y atribuible que sea proxy del verdadero, y un modelo interpretable/calibrado para depurar; (2) entender por qué las features observadas van antes que las aprendidas; (3) combinar features por discretización y cruces; y (4) escalar el número de features al tamaño de los datos (R21). Cada regla entra por un caso. Continúa la disciplina de [[arena-rom1]].

## Tu primer objetivo (Reglas 12-15)

Un **objetivo** es el número que tu algoritmo intenta optimizar; una **métrica** es cualquier número que el sistema reporta (importe o no).

- **R12 — No sobrepienses qué objetivo optimizar directamente.** Quieres dinero, usuarios felices y un mundo mejor; hay montones de métricas que te importan. Al inicio, muchas suben juntas aunque no las optimices directamente (optimiza clicks y sube el tiempo en sitio). Mantenlo simple. (Si subes la métrica optimizada pero decides NO lanzar, toca **revisar el objetivo**.)
- **R13 — Elige una métrica simple, observable y atribuible para el primer objetivo.** El objetivo de ML debe ser **fácil de medir y un proxy del objetivo "verdadero"**. Modela comportamiento **directamente observado y atribuible** a una acción (¿se clicó/descargó/reenvió/calificó/marcó como spam el objeto rankeado?). Evita modelar al inicio efectos **indirectos** (¿volvió al día siguiente?, DAU): son grandes métricas para A/B y decisiones de lanzamiento, pero malos objetivos directos. Y **no** intentes que el ML adivine si el usuario es feliz o si mejora su bienestar.
- **R14 — Empezar con un modelo interpretable facilita el debugging.** Regresión lineal/logística/Poisson están motivadas por un modelo probabilístico: cada predicción es interpretable como probabilidad o valor esperado, y son **calibradas** (en subconjuntos, la expectativa media predicha = label media). Más fáciles de depurar que objetivos zero-one/hinge.
- **R15 — Separa filtrado de spam y ranking de calidad en una policy layer.** El ranking de calidad es un arte; el spam es una **guerra** (adversarios que ajustan sus posts). Sepáralos: el ranking de calidad asume contenido de buena fe; el spam se filtra aparte (a menudo más agresivo) y suele actualizarse a diario.

## Feature engineering (Reglas 16-22)

- **R16 — Planea lanzar e iterar.** No será el último modelo; muchos equipos lanzan un modelo por trimestre durante años. Lanzas por: nuevas features, retunear regularización/combinar features, o tunear el objetivo. Considera cuánto frena cada lanzamiento los siguientes.
- **R17 — Empieza con features directamente observadas/reportadas, no aprendidas.** Una feature **aprendida** (por un sistema externo de clustering o por el propio learner, p.ej. modelo factorizado/deep) tiene su propio objetivo (débilmente correlacionado), puede quedar obsoleta, y los modelos no convexos dan mínimos locales distintos por iteración (difícil juzgar si un cambio importa). Consigue un baseline sin deep features primero.
- **R18 — Explora con features de contenido que generalizan entre contextos.** P.ej. usar stats globales de un post (plus-ones, reshares) para promover contenido nuevo sin datos en el contexto objetivo. No es personalización: primero averigua si gusta en este contexto.
- **R19 — Usa features muy específicas cuando puedas.** Con muchos datos, es más simple aprender millones de features simples que pocas complejas. No temas grupos de features que aplican a una fracción ínfima de datos si la cobertura total supera 90%; usa regularización para eliminar las de muy pocos ejemplos.
- **R20 — Combina y modifica features de forma humano-entendible (discretizaciones y cruces).** **Discretización**: de una feature continua (edad) crea features discretas por cuantiles (no sobrepienses los cortes). **Cruces**: combina feature columns (p.ej. {male,female} × {US,Canada,Mexico} → la feature (male, Canada)); cruces de 3+ columnas exigen muchísimos datos y pueden sobreajustar.
- **R21 — El nº de pesos que puedes aprender en un modelo lineal es ~proporcional a la cantidad de datos.** 1.000 ejemplos → una docena de features (dot product/TF-IDF + features humanas); 1M → intersección + regularización (cientos de miles); miles de millones → cruces (10M features). Escala el aprendizaje al tamaño de los datos.
- **R22 — Limpia features que ya no usas.** Las features sin uso son **deuda técnica**; si una no aporta ni combinada, quítala de la infra para probar features prometedoras más rápido (siempre se puede readir). Piensa en **cobertura**: una feature que cubre 1% de los datos pero el 90% de esos son positivos puede ser excelente.

---

## Mini-ejemplo trabajado: escala las features al tamaño de los datos (R21)

El nº de pesos que un modelo lineal aprende sin sobreajustar es ~proporcional a los datos. Concretamente:

- **1 000 ejemplos** → ~una docena de features (un dot product simple, TF-IDF + un puñado de features humanas). Si metes 10 000 features con 1 000 ejemplos, **memorizas ruido**.
- **1 millón** → cientos de miles de features con regularización.
- **Miles de millones** → cruces masivos (~10M features).

Y la discretización+cruce (R20) crea features humano-entendibles: de `edad` (continua) sacas cubetas por cuantiles, y cruzas `{male,female} × {US,Canada,Mexico}` → la feature `(male, Canada)`. Pero cruzar 3+ columnas multiplica la dimensionalidad y exige *muchísimos* datos.

**Predicción antes de seguir:** tienes 800 ejemplos y quieres usar un embedding profundo de 256 dimensiones. ¿Buena idea de arranque? No (R17+R21): empieza con features **observadas** y un baseline lineal; con 800 ejemplos el embedding aprendido sobreajusta y, además, tiene su propio objetivo débilmente correlacionado.

## Prototipo, contraejemplo y caso borde

- **Prototipo (buen primer objetivo):** "¿el usuario clicó/descargó este ítem?" — simple, observable y atribuible a la acción rankeada.
- **Contraejemplo (objetivo inobservable):** pedirle al ML que prediga "¿es feliz el usuario?" o "¿volverá mañana?" como objetivo *directo* → inobservable/indirecto; sirve para A/B y decisiones de lanzamiento, no como target.
- **Caso borde (feature de baja cobertura):** una feature presente en el 1% de los datos pero positiva el 90% de las veces puede ser oro — la cobertura baja no la descalifica.

## Errores típicos

- **Conceptual:** confundir **objetivo** (lo que el modelo optimiza) con **métrica** (lo que reportas); no todo lo que importa debe ser el objetivo.
- **Técnico:** usar features **aprendidas** (deep/factorizadas) antes de un baseline con features observadas → mínimos locales que cambian por iteración y vuelven indecidible si un cambio ayuda.
- **De mantenimiento:** dejar features muertas en la infra → deuda que frena probar features nuevas.

## Transferencia isomorfa

- **Modelo calibrado (R14) ↔ probabilidades bien escaladas:** que "la media predicha = label media en cada subconjunto" es exactamente la calibración que evalúas en un clasificador clínico/PLP (conecta con [[arena-h13]]).
- **Discretizar + cruzar ↔ feature cross / no linealidad para modelos lineales:** es el mismo patrón Feature Cross de los design patterns (conecta con [[arena-mldp1]]).
- **Pesos ∝ datos (R21) ↔ capacidad vs muestra (sesgo-varianza):** más parámetros que datos = sobreajuste, la ley fundamental del aprendizaje estadístico (conecta con [[arena-isl1]]).

Moraleja de la arista: *objetivo simple y observable + features observadas + capacidad escalada a los datos; lo aprendido y lo profundo llegan después, no antes del baseline.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «¿Qué objetivo exacto optimizo?» | R12-13: simple, observable, atribuible; proxy del verdadero |
| Quieres que el ML prediga «¿es feliz el usuario?» | R13: no; usa proxies observables (clic/descarga) |
| Primer modelo con embeddings/deep features | R17: features observadas primero; baseline sin deep |
| Tengo 1.000 ejemplos y quiero 1M de features | R21: escala las features al tamaño de los datos |
| Feature continua (edad, precio) | R20: discretiza por cuantiles; cruza columnas con cuidado |
| Features viejas que ya nadie usa | R22: deuda técnica, límpialas (cobertura en mente) |
| Mezclar ranking de calidad con anti-spam | R15: sepáralos en una policy layer (spam = guerra) |

---

> **Síntesis:** elige un **objetivo simple, observable y atribuible** (proxy del verdadero) y un **modelo interpretable/calibrado** para depurar (R12-14); separa spam de calidad en una **policy layer** (R15). En feature engineering: **planea iterar** (R16), empieza con features **observadas, no aprendidas** (R17), usa features **específicas** y generalizadoras (R18-19), combina por **discretización y cruces** (R20), **escala features al tamaño de los datos** (R21) y **limpia** las que no usas (R22).

---

*Retrieval: (1) ¿qué hace bueno a un primer objetivo (simple/observable/atribuible) y por qué evitar efectos indirectos?; (2) ¿por qué un modelo interpretable y qué es estar calibrado?; (3) ¿por qué features observadas antes que aprendidas?; (4) explica discretización y cruces, y la relación pesos↔datos (R21).*
