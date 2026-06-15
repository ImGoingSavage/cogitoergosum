# OHDSI IV: calidad de la evidencia, validez de método y estudios en red

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
