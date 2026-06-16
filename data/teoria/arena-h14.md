# OHDSI IV: calidad de la evidencia, validez de método y estudios en red

## De qué trata esta lección (y qué sabrás hacer al final)

Un resultado "estadísticamente significativo" sobre datos observacionales puede ser puro sesgo sistemático, y el intervalo de confianza clásico no lo delata —solo cuenta el azar—. Esta lección construye, desde cero, las salvaguardas que vuelven creíble la evidencia del mundo real: las **cuatro validez**, los **controles negativos** que *miden* el sesgo del propio método, la **calibración empírica** que lo descuenta de los p-valores, y los **estudios en red** que dan escala y privacidad corriendo el mismo código en muchas bases sin mover datos de pacientes.

Al terminar podrás: (1) enumerar las cuatro validez (datos, clínica, software, método); (2) entender qué revela un control negativo (si los RR de nulos conocidos no se centran en 1, hay sesgo residual); (3) explicar por qué la calibración empírica ensancha los IC; y (4) ver por qué un estudio en red es a la vez reproducible y privado. El control negativo entra por un ejemplo. Cierra el cluster causal-health. *(Ejemplos clínicos ilustran el método, no son consejo médico.)*

## Las cuatro validez

La evidencia es creíble solo si se sostienen:
1. **Calidad de datos** (¿aptos para el propósito? → DQD/ACHILLES, Kahn).
2. **Validez clínica** (¿los fenotipos capturan el concepto? ¿generaliza?).
3. **Validez de software** (¿el código hace lo que debe? tests, revisión, versionado).
4. **Validez de método** (¿el diseño produce estimaciones sin sesgo sistemático en esta base?).

## Validez clínica (fenotipos)

¿La cohorte = la idea clínica? Mide **sensibilidad / especificidad / PPV** con **source record verification** (chart review, gold standard caro) o **PheValuator** (gold standard **probabilístico**, escalable). Un fenotipo mal validado mete **misclasificación** en todo el estudio. Ver [[validez-clinica-fenotipo]].

## Validez de método

- **Controles negativos:** pares exposición-outcome sin efecto causal (verdadero **RR≈1**). El mismo análisis sobre muchos: si las estimaciones **no** se centran en 1, hay **error sistemático residual** (confundimiento/selección/medición). Ver [[validez-de-metodo-controles-negativos]].
- **Controles positivos** (a menudo **sintéticos**): efecto conocido → miden **potencia**.
- **Calibración empírica:** usa la distribución de los negativos para **ajustar p-valores e IC** por el sesgo sistemático → **IC más anchos**, menos falsos positivos. Los IC clásicos solo capturan el azar. Ver [[calibracion-empirica-pvalores]].
- **Diagnósticos de diseño:** balance de covariables tras PS, **equipoise**/solapamiento (positividad), MDRR (potencia). Deben **pasar** antes de creer un efecto. La **OHDSI Methods Benchmark** compara métodos por su sesgo/cobertura.

## Estudios en red

El **mismo paquete** estandarizado se corre en **muchas bases** (cada una en su CDM) **sin compartir datos de paciente**: solo viajan **resultados agregados** que se meta-analizan. Da **privacidad + escala + reproducibilidad**. Con protocolo pre-registrado, diagnósticos compartidos y código abierto, supera a los estudios "a medida" (propensos a p-hacking). La generación **a gran escala** (p. ej. **LEGEND**) reporta TODOS los resultados → combate cherry-picking y sesgo de publicación. Ver [[estudios-en-red-ohdsi]].

---

## Mini-ejemplo trabajado: qué revela un control negativo

Eliges **50 pares exposición–outcome** que *sabes* no tienen relación causal (verdadero RR=1): fármacos y desenlaces sin conexión plausible. Corres exactamente tu mismo análisis sobre los 50. Si el método fuera perfecto, los RR estimados se repartirían **alrededor de 1** y ~5% saldrían "significativos" por azar.

Pero observas que la **mediana** de los 50 RR es **1.4** y que el 30% son "significativos". Eso no es azar: es **error sistemático residual** (confundimiento/selección/medición) que tu diseño no quitó. La **calibración empírica** usa esa distribución de negativos para **reajustar** tus p-valores e IC del efecto real: como hay un sesgo de fondo, los IC **se ensanchan** y muchos falsos positivos desaparecen. Los IC clásicos solo cuentan el azar; la calibración añade el sesgo sistemático que sí existe en datos observacionales.

**Predicción antes de seguir:** tras calibrar, tu efecto de interés (antes p=0.03) pasa a p=0.20. ¿Lo "perdiste"? No: descubriste que era del tamaño del ruido sistemático que el propio método genera sobre nulos conocidos — un hallazgo honesto, no una pérdida.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** controles negativos centrados en 1 + diagnósticos de balance que pasan → confías en el efecto.
- **Contraejemplo (IC clásico observacional):** reportar un IC 95% "normal" en datos de claims como si solo importara el azar — ignora el sesgo sistemático que los negativos revelan.
- **Caso borde (controles positivos sintéticos):** como rara vez hay pares con efecto *conocido*, se inyectan outcomes sintéticos con RR conocido para medir **potencia**.

## Errores típicos

- **Conceptual:** creer que "estadísticamente significativo" en observacional = real; sin controles negativos no sabes cuánto sesgo systemático queda.
- **De método:** saltarse los diagnósticos de diseño (balance, equipoise/positividad, MDRR) antes de interpretar.
- **De reporte:** publicar solo el resultado bonito (cherry-picking) en vez de toda la generación (estilo LEGEND).

## Transferencia isomorfa

Estas salvaguardas son control de calidad estadístico de propósito general:

- **Controles negativos ↔ A/A tests / placebo tests:** correr el pipeline sobre casos donde *sabes* que no hay efecto, para medir el sesgo del propio sistema, es el A/A test del experimentador (conecta con [[arena-ads4]]).
- **Calibración empírica ↔ corrección por comparaciones múltiples / ajuste de p-valores:** ajustar la inferencia por un error sistemático conocido es pariente de controlar el FDR cuando corres miles de tests.
- **Estudio en red ↔ aprendizaje federado:** el código va a los datos y solo salen agregados — exactamente el patrón de federated learning y privacidad por diseño (conecta con [[arena-h11]]).

Moraleja de la arista: *en datos observacionales el IC clásico miente por optimista; los controles negativos miden el sesgo del método y la calibración lo descuenta — y compartir código, no pacientes, da escala con privacidad.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| ¿Confío en esta cohorte? | Valida el fenotipo (sens/espec/PPV; PheValuator) |
| RR "significativo" observacional | Controles negativos + calibración empírica |
| ¿El método sesga en esta base? | Controles negativos (¿se centran en RR=1?) |
| p/IC clásicos | Solo capturan el azar → calibra (IC se ensanchan) |
| Datos no centralizables | Estudio en red (solo agregados salen) |

---

> **Síntesis:** la evidencia confiable necesita **cuatro validez** (datos, clínica, software, método). Valida fenotipos por **sens/espec/PPV** (PheValuator). La **validez de método** usa **controles negativos** (RR≈1) para medir el sesgo sistemático y **calibración empírica** para ajustar p/IC (que se ensanchan), más diagnósticos de diseño. Los **estudios en red** corren el mismo código en muchas bases compartiendo solo agregados → privacidad, escala y reproducibilidad.

---

*Retrieval: (1) las 4 validez; (2) ¿qué es un control negativo y qué revela?; (3) ¿qué hace la calibración empírica al IC?; (4) ¿por qué un estudio en red es reproducible y privado?*
