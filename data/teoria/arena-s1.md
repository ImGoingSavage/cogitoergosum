# Del modelo al sistema: skew, drift y rollback

*Lección redactada para CogitoErgoSum. Referencia: Huyen C — Designing Machine Learning Systems (O'Reilly 2022), caps. 8-9; Sculley et al. — "Hidden Technical Debt in Machine Learning Systems" (NeurIPS 2015).*

## De qué trata esta lección (y qué sabrás hacer al final)

Hay un salto enorme entre "mi modelo da buen AUC en el notebook" y "mi modelo crea valor en producción seis meses después". Casi todo lo que sale mal en ese salto **no es el modelo**: es el contorno —cómo se calculan las features, qué llega de verdad en inferencia, si alguien vigila, si hay forma de volver atrás—. Esta lección construye, desde cero, los tres fallos que más hunden modelos buenos: el **training-serving skew** (entrenas con una feature y sirves con otra), el **drift** (el mundo o sus datos cambian) y la falta de **rollback**.

Al terminar podrás: (1) explicar por qué en producción el modelo es la pieza más pequeña; (2) detectar y prevenir el training-serving skew loggeando las features tal como se sirven; (3) distinguir data drift de concept drift y monitorear cada uno por su lado; y (4) entender por qué un mejor número offline puede empeorar el negocio, y diseñar el rollback **antes** de desplegar. No se asume experiencia en producción: cada falla entra por un ejemplo concreto.

## El principio central

Empieza por aquí porque reordena toda tu intuición: en producción el **modelo es la pieza más pequeña del sistema**. Lo que falla casi siempre es el contorno —el pipeline de datos, el cálculo de features, el monitoreo ausente, la ausencia de un plan de rollback—. La moraleja con la que conviene quedarse: un modelo con AUC 0.92 en un pipeline roto es **peor** que un modelo con AUC 0.85 en un pipeline sano. Optimizar el modelo cuando el cuello de botella es el sistema es pulir la pieza equivocada.

---

## Training-serving skew

Analogía para fijarlo: es como entrenar para una carrera midiendo tu tiempo en una pista de tartán y luego competir en arena — las piernas no cambiaron, pero el terreno sí, y el rendimiento se desploma. El **training-serving skew** ocurre cuando las features o los datos que el modelo recibe en producción **difieren** de los que vio durante el entrenamiento. El modelo no ha cambiado; lo que cambió es lo que le llega.

**Tres causas típicas:**

1. **Código de features duplicado offline/online.** El equipo de entrenamiento calcula la feature "promedio de compras en los últimos 7 días" con una ventana de datos históricos completos; el serving la calcula con una ventana deslizante en tiempo real que maneja NULLs y defaults de forma distinta. El modelo fue entrenado en una feature; se sirve con otra.

2. **Datos de entrenamiento no representativos del tráfico real.** Se entrena con datos históricos de usuarios activos pero el modelo se despliega para nuevos usuarios: distribuciones distintas, proporciones distintas, features faltantes distintas.

3. **Feedback loops.** El modelo en producción determina qué ítems se muestran, por tanto qué ítems se clican, por tanto qué datos de entrenamiento se generan. El nuevo modelo se entrena sobre la distribución sesgada por el modelo viejo: el error se amplifica con cada ciclo.

**Defensa:** definición única de features — idealmente un feature store o código compartido ejecutable tanto offline como online — y **loggear las features TAL COMO se sirvieron** para reentrenar exactamente sobre lo que el modelo vio en producción.

---

## Data drift vs concept drift

| Tipo | Qué cambia | Señal | Cómo monitorear |
|------|-----------|-------|-----------------|
| **Data drift** | P(X): la distribución de las entradas | Cambio de segmento de usuarios, temporalidad, fallo upstream | Tests de distribución sobre features: PSI, Kolmogorov-Smirnov contra la distribución de entrenamiento. **No necesita labels.** |
| **Concept drift** | P(Y\|X): la relación aprendida | El mundo cambió (economía, comportamiento, regulación) | Performance real con labels (a menudo retrasadas) o proxies tempranos: distribución de scores, tasa de aceptación, tasa de fraude reportado. |

Un modelo puede sufrir data drift sin concept drift (llega tráfico de otro país, pero el patrón fraude/no-fraude es el mismo) o concept drift sin data drift aparente (los mismos usuarios empiezan a comportarse diferente tras un evento externo). El monitoreo cubre ambos planos por separado.

---

## Offline ≠ online

Un AUC mejor en el conjunto de evaluación puede empeorar el CTR o el outcome en producción. Las causas más frecuentes:

- **Leakage temporal.** El split de evaluación no respetó el tiempo: el modelo "vio" el futuro durante el entrenamiento o la evaluación. El AUC offline es inflado; en producción el modelo enfrenta el futuro real.
- **Training-serving skew.** Las features evaluadas offline no son las que se calculan al servir: la métrica mide el modelo sobre datos que nunca llegan en producción.
- **Feedback loop en los datos de evaluación.** El conjunto de evaluación fue generado por el modelo anterior: un AUC mejor en esa distribución no implica mejor ranking en la distribución futura.
- **Métrica que no captura el objetivo.** AUC global mide discriminación promedio; el producto depende de la calidad del top-k visible. Optimizar AUC global puede perjudicar el top-k.

**El A/B con guardrails es el árbitro.** La evaluación online mide el objetivo real; el rollback se diseña antes del despliegue.

---

## Plantilla de diseño

Copia esta tabla en la pizarra **antes** de proponer arquitectura o modelo:

| Campo | Tu respuesta |
|---|---|
| Supuestos | |
| Métrica principal | |
| Métrica secundaria / guardrails | |
| Riesgos | |
| Tradeoffs | |
| Datos disponibles | |
| Datos NO disponibles | |
| Componentes del sistema | |
| Puntos de leakage | |
| Privacidad / PHI | |
| Monitoreo | |
| Rollback | |
| Casos borde | |

---

## Mini-ejemplo trabajado: el skew que nadie ve hasta producción

La feature "promedio de compras en los últimos 7 días" se calcula así:
- **Offline (entrenamiento):** sobre el histórico completo, una media limpia sobre 7 días de datos siempre presentes.
- **Online (serving):** una ventana deslizante en tiempo real donde, si faltan días, se rellena con 0 (default).

Un usuario nuevo con 2 días de historia recibe offline un promedio sobre 2 días, pero online un promedio "sobre 7" con 5 ceros → **valores sistemáticamente más bajos en serving**. El modelo fue entrenado con una feature y se sirve con otra; el AUC offline no lo detecta porque offline ambos coinciden.

**Predicción antes de seguir:** ¿cómo entrenarías para que el modelo aprenda la feature *real* que verá en producción? Respuesta: **loggea las features tal como se sirvieron** y reentrena sobre esos logs, no sobre el cálculo histórico idealizado. La regla profunda: la única feature que importa es la que el modelo recibe en inferencia; entrénalo sobre exactamente eso. Un feature store con código compartido offline/online elimina la duplicación de raíz.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** "funciona en pruebas, falla en prod" → audita training-serving skew (¿misma feature offline y online?) y leakage temporal en el split.
- **Contraejemplo (AUC mejor, negocio peor):** un AUC global más alto puede empeorar el top-k visible; optimizar la métrica equivocada engaña. La métrica debe capturar el objetivo real.
- **Caso borde (feedback loop):** el modelo decide qué se muestra → qué se clica → los datos del próximo entrenamiento; el sesgo se amplifica solo. El borde muestra que el modelo contamina sus propios datos futuros.

## Errores típicos

- **Conceptual:** tratar el modelo como el sistema; en producción es la pieza más pequeña, el contorno (datos, features, monitoreo, rollback) es lo que falla.
- **Técnico:** split de evaluación que no respeta el tiempo (leakage temporal) → AUC offline inflado.
- **De supuestos:** desplegar sin plan de rollback ni guardrails definidos antes del lanzamiento.

## Transferencia isomorfa

- **Training-serving skew ↔ data/covariate shift:** train y serving ven distribuciones distintas; es el mismo desajuste P_train(X) ≠ P_serving(X) del drift (conecta con [[arena-htd4]] y [[arena-cds3]]).
- **Leakage temporal ↔ data leakage de preprocesamiento:** "ver el futuro" en el split es el mismo pecado que escalar antes de separar train/test (conecta con [[arena-cds1]]).
- **Feedback loop ↔ regresión a la media / sesgo de selección:** el modelo que genera sus propios datos de entrenamiento sesga la distribución, como condicionar en lo que un proceso decide mostrar (conecta con [[arena-h17]]).
- **AUC global vs top-k ↔ métrica alineada al costo real:** discriminación promedio no es calidad del top visible; elegir la métrica correcta es la misma disciplina que precisión vs recall según el costo (conecta con [[arena-ads3]]).

Moraleja de la arista: *en producción el modelo es lo de menos; entrénalo sobre las features que de verdad verá (loggeadas), respeta el tiempo en el split, y define rollback y guardrails antes de desplegar.*

---

## Señales de reconocimiento y jugadas

| Señal | Jugada |
|-------|--------|
| "El modelo funciona en pruebas pero falla en producción" | Audita el skew: ¿se calculan las features igual offline y online? ¿Se entrena sobre features loggeadas? |
| "El AUC mejoró pero el negocio empeoró" | Revisa leakage temporal en el split, skew y si el conjunto de evaluación fue generado por el modelo anterior |
| "La distribución de scores cambió sin cambio de código" | Data drift: tests PSI/KS sobre features contra distribución de entrenamiento; no esperes labels |
| "El modelo rinde peor en los últimos 30 días" | Concept drift: compara performance con labels retrasadas; considera reentrenamiento o recalibración |
| "¿Cómo desplegarías este modelo?" | Plantilla primero: métricas, guardrails, leakage, privacidad, monitoreo, rollback — el modelo es lo último |

---

## Ejercicio de consolidación

Un banco despliega un modelo de scoring crediticio. Seis meses después, la tasa de incumplimiento del grupo aprobado sube un 15% aunque el AUC en el conjunto de prueba histórico no cambió.

1. ¿Puede ser skew? ¿Qué verificarías primero?
2. ¿Puede ser concept drift? ¿Qué evidencia lo confirmaría?
3. ¿Qué proxies de monitoreo hubieras necesitado, dado que los labels (incumplimiento) llegan con 90 días de retraso?
4. ¿Cómo diseñarías el rollback para este modelo?

*Respuesta: (1) Sí: verifica si las features de producción (ingresos, historial, ratio deuda/ingreso) se calculan con el mismo código y ventanas que en entrenamiento; loggea features servidas y compara su distribución con la de entrenamiento. (2) Sí: puede haber cambiado la relación riesgo/features por condiciones macroeconómicas; lo confirmaría comparando la tasa real de incumplimiento por score-bucket contra la esperada por el modelo — si el calibrado se rompió, es concept drift. (3) Proxies: distribución de scores aprobados, tasa de aprobación por segmento, distribución de ingresos declarados, ratio de solicitudes por canal. Un proxy que se desvía sin labels es la alarma temprana. (4) Rollback: definir umbrales de guardrail (p. ej. tasa de aprobación cae >10% o distribución de scores se desplaza >X PSI) que disparan el regreso automático al modelo anterior; versionar el modelo y el pipeline de features juntos para que el rollback sea reproducible.*
