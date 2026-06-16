# Deuda técnica oculta en ML II: dependencias de datos y feedback loops

## De qué trata esta lección (y qué sabrás hacer al final)

En código, un compilador te avisa de las dependencias rotas; en ML, las **dependencias de datos** son igual de peligrosas pero **invisibles** —no hay análisis estático equivalente—. Esta lección construye, desde cero, esa deuda silenciosa: las dependencias de datos **inestables** (un input que cambia bajo tus pies, donde hasta una "mejora" upstream puede romperte), las **infrautilizadas** (legacy, bundled, ε, correlated), y los **feedback loops** donde un modelo influye en su propio futuro.

Al terminar podrás: (1) entender por qué las dependencias de datos cuestan más que las de código; (2) mitigar una dependencia inestable con una copia versionada (frozen); (3) detectar features infrautilizadas con leave-one-feature-out periódico y reconocer el riesgo de las correlated no causales; y (4) distinguir feedback loops directos de ocultos. El caso de la señal mis-calibrada "corregida" hace de hilo. Continúa el paper de [[arena-htd1]].

## Las dependencias de DATOS cuestan más que las de código

En código, la *dependency debt* contribuye a la complejidad, pero las dependencias de código se identifican con **análisis estático** (compiladores, linkers). Las **dependencias de DATOS** tienen la misma capacidad de generar deuda pero son **más difíciles de detectar**: sin tooling equivalente, es demasiado fácil construir grandes cadenas de dependencias de datos difíciles de desenredar.

### Dependencias de datos inestables
Señales de entrada que **cambian de comportamiento con el tiempo** (cualitativa o cuantitativamente). Pasa **implícitamente** (el input viene de otro modelo ML que se actualiza, o de una tabla de TF/IDF o mapeo semántico) o **explícitamente** (el ownership del input está separado del modelo que lo consume). Es peligroso porque **incluso las "mejoras" al input pueden tener efectos detrimentales** y costosos en el consumidor: ej., si una señal estaba **mis-calibrada** y el modelo se ajustó a ello, una actualización que la "corrige" tiene ramificaciones súbitas. **Mitigación:** crear una **copia versionada** (frozen) de la señal y usarla hasta validar una versión nueva; coste: **staleness** y mantener múltiples versiones.

### Dependencias de datos infrautilizadas
Señales de entrada que aportan **poco beneficio** al modelo pero lo hacen vulnerable al cambio innecesariamente (a veces catastróficamente), aunque podrían quitarse sin perjuicio. Ej.: al migrar de un esquema viejo de numeración de productos a uno nuevo, se dejan **ambos**; un año después borran el código que poblaba los números viejos → mal día para los mantenedores. Cuatro formas en que se cuelan:
- **Legacy features:** una feature F incluida temprano, hecha redundante por features nuevas, sin que nadie lo note.
- **Bundled features:** un grupo evaluado como beneficioso se añade en bloque por presión de plazos, incluyendo features que aportan poco.
- **ε-features:** añadir una feature por una mejora **diminuta** de accuracy aunque el overhead de complejidad sea alto.
- **Correlated features:** dos features muy correlacionadas, una más **causal**; muchos métodos no lo detectan y las acreditan por igual (o eligen la no-causal) → **brittleness** si el mundo cambia las correlaciones.

**Detección:** evaluaciones exhaustivas **leave-one-feature-out**, corridas **regularmente** para identificar y quitar features innecesarias.

### Análisis estático de dependencias de datos
El tooling de análisis estático de datos es escaso pero **esencial** (error-checking, rastrear consumidores, forzar migración/borrado). Un **sistema de gestión de features** permite **anotar** fuentes y features; checks automáticos verifican que toda dependencia tenga anotaciones y que los árboles de dependencia se resuelvan, haciendo la migración y el borrado mucho más seguros.

## Feedback loops (deuda de análisis)

Los sistemas ML en vivo a menudo **influyen en su propio comportamiento** al actualizarse → *analysis debt*: es difícil predecir el comportamiento de un modelo antes de lanzarlo. Más difíciles de detectar si ocurren **gradualmente**.

- **Direct feedback loops:** un modelo influye directamente en la selección de sus **propios datos de entrenamiento futuros**. La solución teóricamente correcta serían **bandits**, pero no escalan al tamaño de los espacios de acción reales; se mitiga con algo de **randomización** o aislando partes de los datos de la influencia del modelo.
- **Hidden feedback loops:** dos sistemas se influyen **indirectamente a través del mundo**. Ej.: dos sistemas que eligen independientemente facetas de una página web (uno productos, otro reseñas relacionadas): mejorar uno cambia el comportamiento del usuario y afecta al otro. Pueden existir entre sistemas **completamente disjuntos** (ej.: dos modelos de predicción bursátil de empresas distintas, donde una mejora —o un bug— en uno influye en el bidding del otro).

---

## Mini-ejemplo trabajado: cuando "corregir" la entrada rompe tu modelo

Tu modelo de ranking consume una señal `score_calidad` que viene de **otro equipo**. Resulta que esa señal está **mis-calibrada**: sistemáticamente devuelve valores ~0.2 más altos de lo que debería. Tu modelo, al entrenarse, **aprendió a compensarlo** (le restó importancia justo en ese rango).

Un día el otro equipo "mejora" su señal y **corrige** el sesgo de +0.2. Para ellos es un avance; para ti es un **desastre silencioso**: tu modelo seguía descontando un sesgo que ya no existe, y sus predicciones se descalibran de golpe. Ni siquiera fue un bug: fue una *mejora* del upstream.

La mitigación: usa una **copia versionada (frozen)** de la señal y valida cada versión nueva antes de adoptarla. Coste: **staleness** y mantener varias versiones — deuda que eliges conscientemente.

**Predicción antes de seguir:** corres un **leave-one-feature-out** y descubres dos features casi idénticas; quitar la "feature A" no cambia nada pero quitar "B" sí. ¿Cuál conservar? La más **causal/estable**: si el mundo cambia la correlación entre ambas, la no-causal te vuelve frágil (el mismo problema de elegir el predictor causal frente al espurio, [[arena-h4]]).

## Prototipo, contraejemplo y caso borde

- **Prototipo (dependencia gestionada):** input externo congelado y versionado + leave-one-feature-out periódico → cambias sin sorpresas.
- **Contraejemplo (ε-feature):** añadir una feature por una mejora *diminuta* de accuracy con overhead de complejidad alto → deuda que no compensa.
- **Caso borde (feedback loop directo):** el modelo elige qué ítems mostrar → solo recoge datos de lo que mostró → se refuerza; la cura teórica (bandits) no escala, así que randomizas o aíslas una fracción de datos.

## Errores típicos

- **Conceptual:** asumir que "mejorar el input siempre ayuda al consumidor" — una corrección puede romper a un modelo ajustado al sesgo viejo.
- **De detección:** confiar en que las dependencias de datos se ven con análisis estático como las de código (no hay tooling equivalente sin un sistema de gestión de features).
- **De diseño:** dejar features legacy/bundled/correlated acumulándose sin leave-one-feature-out → brittleness.

## Transferencia isomorfa

- **Dependencia de datos inestable ↔ dependencia de API sin contrato:** consumir una señal cuyo dueño la cambia sin avisar es el mismo riesgo que depender de un endpoint sin versionar; la cura (frozen + SLA) es versionado de contrato (conecta con [[arena-htd1]], undeclared consumers).
- **Direct feedback loop ↔ off-policy / bandits:** el modelo que elige sus propios datos futuros es el problema de exploración-explotación; randomizar es la mini-versión de un bandit (conecta con [[arena-h19]]).
- **Correlated features no causales ↔ confundimiento:** acreditar a la feature equivocada porque correlaciona es el riesgo de tomar el predictor espurio por el causal (conecta con [[arena-h4]]).

Moraleja de la arista: *los datos son una dependencia tan real como el código, pero invisible; congélalos, versiona y corre leave-one-feature-out, porque hasta una "mejora" del input puede romperte.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Mi input viene de otro modelo/tabla que se actualiza | Dependencia inestable: usa una copia versionada (frozen) |
| «Corregimos esa señal de entrada» y mi modelo se rompió | El modelo se ajustó a la mis-calibración; versiona |
| Features que «no molestan» pero nadie usa | Infrautilizadas (legacy/bundled/ε/correlated): leave-one-feature-out |
| Dos features muy correlacionadas | Riesgo: ML elige la no-causal → brittleness si cambia la correlación |
| El modelo elige sus propios datos futuros | Direct feedback loop: randomiza o aísla datos |
| Dos sistemas se afectan vía el comportamiento del usuario | Hidden feedback loop (puede ser entre sistemas disjuntos) |

---

> **Síntesis:** las **dependencias de datos** cuestan más que las de código por falta de análisis estático. Las **inestables** (input que cambia) se mitigan con **copias versionadas**; las **infrautilizadas** (legacy, bundled, ε, correlated) se detectan con **leave-one-feature-out** regular. Un **sistema de gestión de features** con anotaciones hace seguro migrar/borrar. Los **feedback loops** —directos (el modelo elige sus datos) y ocultos (dos sistemas vía el mundo)— vuelven impredecible el comportamiento; mitiga con randomización/aislamiento.

---

*Retrieval: (1) ¿por qué las dependencias de datos cuestan más que las de código?; (2) ¿qué es una dependencia inestable y cómo la mitigas?; (3) nombra las 4 formas de dependencia infrautilizada y cómo se detectan; (4) distingue feedback loop directo de oculto.*
