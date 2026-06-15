# Deuda técnica oculta en ML IV: mundo externo, otras deudas y cómo medirla

## Lidiar con cambios en el mundo externo

Los sistemas ML interactúan directamente con el mundo externo, que **rara vez es estable**: ese **background rate of change** crea coste de mantenimiento continuo.

- **Fixed thresholds in dynamic systems:** suele fijarse un **umbral de decisión** (predecir true/false, marcar spam o no, mostrar un ad o no) para buenos trade-offs en métricas como precisión/recall. Pero esos umbrales se ponen **a mano**, así que al actualizar el modelo con datos nuevos el umbral viejo queda **inválido**; actualizar muchos umbrales a mano es lento y frágil. **Mitigación:** **aprender los umbrales** mediante evaluación simple en datos de validación held-out.
- **Monitoring and testing:** los unit tests y los tests end-to-end son valiosos, pero **no bastan** ante un mundo cambiante para evidenciar que el sistema funciona como se pretende. Es crítico un **monitoreo en vivo, en tiempo real, con respuesta automatizada**. La pregunta clave: **¿qué monitorear?** (los invariantes testables no son obvios si el sistema adapta con el tiempo). Puntos de partida:
  - **Prediction Bias:** en un sistema sano, la **distribución de labels predichos ≈ distribución de labels observados**. No es un test exhaustivo (un modelo nulo que predice la media lo cumple), pero es un diagnóstico **sorprendentemente útil**: cambios aquí detectan que el mundo cambió y las distribuciones de entrenamiento ya no reflejan la realidad. **Slicing** el bias por dimensiones aísla problemas y permite alertas.
  - **Action Limits:** en sistemas que toman acciones reales (pujar, marcar spam), fija **límites de acción** como sanity check (lo bastante amplios para no dispararse espuriamente); si se alcanza un límite, alerta automática e intervención/investigación.
  - **Up-Stream Producers:** monitorea y testea a fondo a los productores up-stream que alimentan el sistema; deben cumplir un **SLA**, y las alertas deben **propagarse** al control plane del ML (y los fallos del ML, down-stream a todos los consumidores).
  - La respuesta debe ser **en tiempo real/automatizada** (los cambios externos ocurren en tiempo real); depender de intervención humana ante pages es frágil para issues sensibles al tiempo.

## Otras áreas de deuda ML

- **Data testing debt:** si los **datos reemplazan al código** en ML y el código se testea, entonces **hay que testear los datos de entrada**: sanity checks básicos y tests más sofisticados que monitoreen cambios en las distribuciones de entrada.
- **Reproducibility debt:** poder re-correr experimentos y obtener resultados similares es difícil por **algoritmos randomizados, no-determinismo del aprendizaje paralelo, dependencia de condiciones iniciales** e interacciones con el mundo externo.
- **Process management debt:** los sistemas maduros tienen **decenas o cientos** de modelos a la vez: actualizar muchas configs de forma segura, asignar recursos entre modelos con prioridades distintas, visualizar y detectar **bloqueos** en el flujo de datos, y tooling de recuperación de incidentes. Smell a evitar: **procesos comunes con muchos pasos manuales**.
- **Cultural debt:** a veces hay una **línea dura entre research y engineering** contraproducente para la salud del sistema. Es clave una cultura de equipo que **premie borrar features, reducir complejidad, mejorar reproducibilidad/estabilidad y monitorear** tanto como premia mejorar la accuracy; suele lograrse en **equipos heterogéneos** fuertes en ambas disciplinas.

## Cómo medir y pagar la deuda

La deuda técnica es una metáfora útil pero **no da una métrica estricta** rastreable. **Moverse rápido NO es evidencia de baja deuda ni de buenas prácticas** — el coste total solo aparece con el tiempo, y de hecho moverse rápido suele **introducir** deuda. Cinco preguntas útiles para evaluarla:
1. ¿Cuán fácil es probar un enfoque algorítmico **enteramente nuevo a escala completa**?
2. ¿Cuál es la **clausura transitiva** de todas las dependencias de datos?
3. ¿Cuán **precisamente** se puede medir el impacto de un cambio nuevo en el sistema?
4. ¿Mejorar un modelo o señal **degrada** otros?
5. ¿Cuán rápido puede **ponerse al día** un nuevo miembro del equipo?

Una investigación que da un beneficio de accuracy **diminuto** a costa de aumentos **masivos** de complejidad rara vez es sabia; incluso añadir una o dos dependencias de datos inocuas puede frenar el progreso. **Pagar la deuda requiere un compromiso específico, alcanzable solo con un cambio en la cultura del equipo.**

---

## Mini-ejemplo trabajado: prediction bias como detector de "el mundo cambió"

Un clasificador de spam predice, en promedio histórico, "spam" el **8%** de las veces, y observas que efectivamente ~8% del correo era spam. **Invariante sano:** distribución de labels predichos ≈ distribución de labels observados.

Un lunes, el modelo empieza a predecir "spam" el **20%** mientras el spam real sigue en ~8%. No hace falta saber *qué* falló: el **prediction bias** se disparó → el mundo (o un input) cambió y la distribución de entrenamiento ya no refleja la realidad. **Slicing** el bias por dimensión (idioma, dominio, región) aísla el subgrupo culpable y dispara una alerta.

No es un test exhaustivo (un modelo que siempre predice la media base también lo cumpliría), pero es **sorprendentemente útil** y barato como centinela de drift.

**Predicción antes de seguir:** reentrenas el modelo con datos frescos y tu umbral de decisión fijado a mano (0.5) deja de dar el trade-off precisión/recall de antes. ¿Por qué? Porque el umbral se calibró para el *modelo viejo*; al reentrenar se **invalida**. La cura: **aprender el umbral** en datos held-out, no clavarlo a mano.

## Prototipo, contraejemplo y caso borde

- **Prototipo (monitoreo vivo):** prediction bias + action limits + SLAs upstream con respuesta automática → detectas cambios del mundo en tiempo real.
- **Contraejemplo ("tenemos unit tests, basta"):** los tests pasan pero el mundo cambió; sin monitoreo en vivo el sistema "funciona" y decae.
- **Caso borde (umbral fijo en sistema dinámico):** un threshold a mano que era óptimo hace 6 meses ahora marca de más o de menos tras varios reentrenamientos.

## Errores típicos

- **Conceptual:** creer que "moverse rápido" prueba poca deuda — suele *introducirla*; el costo aparece con el tiempo.
- **De monitoreo:** no testear los **datos de entrada** (data testing debt) cuando los datos reemplazan al código.
- **De diseño:** depender de intervención humana ante pages para issues sensibles al tiempo, en vez de respuesta automatizada.

## Transferencia isomorfa

- **Prediction bias ↔ monitoreo de data/label drift:** comparar la distribución predicha vs observada es exactamente el chequeo de shift en producción (conecta con [[arena-dmls4]]).
- **Umbral fijo invalidado ↔ recalibración:** un threshold que caduca al reentrenar es el mismo problema que recalibrar probabilidades cuando cambia la prevalencia (conecta con [[arena-h13]]).
- **"Moverse rápido ≠ poca deuda" ↔ interés compuesto:** la deuda se acumula en silencio como un préstamo, principio universal de ingeniería sostenible (conecta con [[arena-htd1]]).

Moraleja de la arista: *el mundo cambia bajo tus pies; aprende umbrales en held-out, vigila el prediction bias como centinela de drift, y recuerda que ir rápido no es señal de poca deuda sino a menudo su causa.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Umbral de decisión fijado a mano | Se invalida al reentrenar; apréndelo en heldout |
| «Tenemos unit tests, basta» | No ante un mundo cambiante; monitoreo en vivo + respuesta automática |
| ¿Qué monitoreo si el sistema adapta? | Prediction bias, action limits, up-stream producers |
| Distribución de predicciones se desvía de la observada | Prediction bias: el mundo cambió; slice para aislar |
| Decenas de modelos con pasos manuales | Process management debt: automatiza, detecta bloqueos |
| «Vamos rápido, hay poca deuda» | Falso: moverse rápido suele INTRODUCIR deuda |

---

> **Síntesis:** el **mundo externo cambia**, invalidando **umbrales fijos** (apréndelos en heldout) y exigiendo **monitoreo en vivo** con respuesta automática (**prediction bias**, action limits, up-stream SLAs). Hay además **data testing debt** (testea los datos), **reproducibility debt**, **process management debt** (decenas de modelos, evita pasos manuales) y **cultural debt** (premiar borrar/simplificar/monitorear como la accuracy). La deuda no tiene métrica estricta: **moverse rápido no es evidencia de baja deuda**; mídela con las 5 preguntas y págala con un **cambio cultural**.

---

*Retrieval: (1) ¿por qué los umbrales fijos son deuda y cómo se mitigan?; (2) ¿qué es el prediction bias y por qué es útil monitorearlo?; (3) nombra dos «otras» deudas (reproducibility, process management, cultural, data testing); (4) cita 3 de las 5 preguntas para medir la deuda y por qué moverse rápido no implica baja deuda.*
