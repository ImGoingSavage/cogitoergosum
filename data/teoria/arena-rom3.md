# Reglas de ML (Google) III: análisis humano del sistema y training-serving skew

## Análisis humano del sistema (Reglas 23-28)

Mirar un modelo existente y mejorarlo es más arte que ciencia; hay anti-patrones que evitar.

- **R23 — No eres un usuario típico.** El fishfooding/dogfooding ayuda, pero estás demasiado cerca del código (sesgo de confirmación) y tu tiempo es muy valioso (9 ingenieros 1 h = muchas etiquetas en crowdsourcing). Para feedback real, usa **metodologías de UX**: user personas y usability testing con gente real (paga laypeople o experimento en vivo).
- **R24 — Mide el delta entre modelos.** Antes de que un usuario vea el nuevo modelo, calcula cuán **diferentes** son sus resultados de producción (p.ej. diferencia simétrica ponderada por posición en ranking). Delta muy pequeño → poco cambio sin experimentar; muy grande → asegúrate de que el cambio es bueno. Verifica que un modelo comparado consigo mismo dé diferencia ~0 (sistema estable).
- **R25 — Al elegir modelos, el rendimiento utilitario gana a la potencia predictiva.** El modelo puede predecir CTR, pero lo que importa es **qué haces con la predicción**: si rankeas, la calidad del ranking final importa más que la predicción; si filtras spam, importa la precisión de lo permitido. Si un cambio mejora el log loss pero degrada el sistema, busca otra feature; si pasa seguido, revisa el objetivo.
- **R26 — Busca patrones en los errores medidos y crea features.** Un ejemplo que el modelo *sabe* que erró (falso positivo/negativo) y que arreglaría si pudiera: dale una feature que le permita corregirlo y la usará. Pero una feature basada en algo que el sistema NO ve como error será ignorada. No seas muy específico: si demota posts largos, añade «longitud del post» (una docena de features, deja que el modelo decida).
- **R27 — Intenta cuantificar el comportamiento indeseable observado.** Si algo molesta y no lo captura la loss, conviértelo en números (p.ej. raters humanos identifican «gag apps»). Si es medible, úsalo como feature/objetivo/métrica. Regla: **«mide primero, optimiza después»**.
- **R28 — Comportamiento idéntico a corto plazo NO implica idéntico a largo plazo.** Un sistema que mira (doc_id, query) y predice clic puede verse idéntico al actual en A/B y side-by-sides, pero no mostrar apps nuevas (solo sabe del historial de esa query). La única forma de entender el largo plazo es **entrenar solo con datos del modelo en vivo** (muy difícil).

## Training-serving skew (Reglas 29-37)

El **training-serving skew** es la diferencia de rendimiento entre entrenamiento y serving, causada por: (a) discrepancia de manejo de datos entre pipelines, (b) cambio de datos entre entrenar y servir, o (c) un feedback loop entre modelo y algoritmo. **Monitoréalo explícitamente.**

- **R29 — La mejor forma de entrenar como sirves: guarda las features usadas en serving y pípalas a un log para entrenar con ellas.** (YouTube home cambió a logear features en serving → mejoras de calidad y menos complejidad de código.)
- **R30 — Pondera por importancia los datos muestreados, no los descartes arbitrariamente.** Descartar datos en entrenamiento causa problemas; si muestreas X con prob. 30%, dale peso 10/3. Así se preservan las propiedades de calibración (R14).
- **R31 — Si joineas una tabla en entrenamiento y serving, los datos de la tabla pueden cambiar.** Features en una tabla (nº de comentarios) cambian entre entrenar y servir → predicciones distintas. Evítalo logeando features en serving (R32); o snapshotea la tabla por hora/día.
- **R32 — Reusa código entre pipelines de entrenamiento y serving siempre que puedas.** Serving es online, entrenamiento es batch, pero puedes compartir el código que crea el objeto legible y lo formatea para el ML. Esto **elimina una fuente de skew**. Corolario: no uses dos lenguajes distintos entre entrenar y servir.
- **R33 — Si entrenas con datos hasta el 5 de enero, testea con datos del 6 en adelante.** El rendimiento sobre datos POSTERIORES refleja mejor producción; se espera algo peor pero no radicalmente, y el AUC debería quedar razonablemente cerca.
- **R34 — En clasificación binaria para filtrado (spam, emails interesantes), sacrifica un poco de rendimiento a corto plazo por datos muy limpios.** Si el filtro bloquea el 75% de los negativos en serving, etiqueta el **1% del tráfico como "held out"** y muéstralo al usuario para datos sin sesgo de muestreo (ahora bloqueas ≥74%). 10.000 ejemplos bastan para estimar bien.
- **R35 — Cuidado con el skew inherente en problemas de ranking.** Al cambiar el ranking radicalmente, cambias los datos que verás en el futuro. Mitiga: más regularización en features que cubren muchas queries, solo pesos positivos, y no tengas features document-only.
- **R36 — Evita feedback loops con features posicionales.** La posición afecta dramáticamente el clic: añade **features posicionales** (el modelo aprende a pesar «1st-position»), y en serving NO des la feature posicional (o dásela constante), porque rankeas ANTES de decidir el orden. Mantén las features posicionales separadas (no las cruces con features de documento).
- **R37 — Mide el training-serving skew.** Divídelo en: (1) rendimiento train vs holdout (siempre existe, no siempre malo), (2) holdout vs «next-day» (tunea la regularización para maximizar el next-day; caídas grandes = features time-sensitive), (3) next-day vs live (una discrepancia aquí, con R5, indica un error de ingeniería).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «A mí me funciona bien el modelo» | R23: no eres usuario típico; usa raters/UX |
| Lanzar un modelo nuevo sin experimento | R24: mide el delta vs producción primero |
| El log loss mejoró pero el ranking empeoró | R25: rendimiento utilitario > potencia predictiva |
| Algo molesta pero «no se puede medir» | R27: mide primero, optimiza después |
| El modelo se ve igual en A/B pero algo raro | R28: corto plazo ≠ largo plazo (feedback de historial) |
| Predicciones distintas en train vs serving | R29/R31/R32: logea features en serving; reusa código |
| Quiero descartar datos por exceso | R30: pondera por importancia, no descartes |
| Items en 1ª posición siempre ganan | R36: features posicionales separadas; quítalas en serving |

---

> **Síntesis:** al **analizar el sistema como humano**, recuerda que no eres usuario típico (R23), mide el **delta entre modelos** (R24), prioriza el **rendimiento utilitario** sobre la potencia predictiva (R25), crea features desde los **errores** (R26), **cuantifica antes de optimizar** (R27) y no confundas corto con largo plazo (R28). El **training-serving skew** (discrepancia de pipelines, datos cambiantes o feedback loop) se combate **logeando features en serving y reusando código** (R29-32), testeando en datos posteriores (R33), recogiendo datos limpios (R34) y **midiéndolo** en sus tres componentes (R37).

---

*Retrieval: (1) ¿por qué «no eres un usuario típico» y qué usar en su lugar?; (2) ¿qué significa que el rendimiento utilitario gana a la potencia predictiva?; (3) ¿qué causa el training-serving skew y cuál es la mejor forma de evitarlo?; (4) ¿por qué y cómo se usan features posicionales (R36)?*
