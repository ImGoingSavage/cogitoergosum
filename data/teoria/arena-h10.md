# Análisis de supervivencia IV: eventos recurrentes y riesgos competitivos

## Eventos recurrentes

El **mismo** evento ocurre **varias veces** por sujeto (recaídas, hospitalizaciones, infecciones). Los eventos intra-sujeto están **correlacionados** → los métodos que asumen independencia subestiman los SE. Enfoques (todos con **varianza robusta** por sujeto):
- **Andersen-Gill (proceso de conteo):** intervalos (start, stop] por sujeto, todos los eventos como un proceso; el sujeto vuelve al riesgo tras cada evento. Para eventos intercambiables.
- **PWP (condicional):** **estratifica por orden** del evento; no se está en riesgo del k-ésimo hasta tener el (k−1). Riesgo dependiente del historial.
- **WLW (marginal):** cada orden de evento como proceso paralelo separado. Ver [[eventos-recurrentes-supervivencia]].

Elección: AG (proceso único) · PWP (depende del orden) · WLW (marginal por evento).

## Riesgos competitivos

Varios eventos **mutuamente excluyentes**; uno **impide** los otros (muerte por cáncer vs por otra causa). El sujeto que sufre el competidor **ya no está en riesgo** del evento de interés.

### El error de 1 − KM
Tratar el competidor como **censura** asume que el sujeto **podría** tener el evento luego → **falso** (ya murió). Por eso **1−KM SOBRESTIMA** la incidencia acumulada (la suma de causas puede pasar de 1). La medida correcta es la **CIF (función de incidencia acumulada)**: probabilidad de sufrir el evento antes de t **y** antes de cualquier competidor; acumula riesgo solo entre los **libres de todo evento**.

### Dos hazards
- **Específico de causa:** tasa entre los aún libres de evento (Cox **censurando** competidores) → **etiología**.
- **Subdistribución / Fine-Gray:** mantiene a los que tuvieron el competidor en el risk set (peso decreciente) y permite **regresar sobre la CIF** → **predicción / riesgo absoluto**. Ver [[riesgos-competitivos-cif]].

Regla: reporta **ambos** (una covariable puede subir la CIF de una causa bajando la mortalidad competidora). Comparar grupos: **prueba de Gray** (no log-rank sobre 1−KM); efecto ajustado: subdistribution HR de Fine-Gray. La **CPC** = CIF_c / (1 − CIF de otras causas).

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| El evento se repite en el sujeto | Eventos recurrentes + varianza robusta (AG/PWP/WLW) |
| El riesgo depende del nº de eventos previos | PWP (condicional por orden) |
| Muerte (u otro) impide el evento de interés | Riesgos competitivos: usa la CIF, no 1−KM |
| Pregunta etiológica/biológica | Hazard específico de causa (censura competidores) |
| Predicción de riesgo absoluto | Fine-Gray (subdistribution) / CIF |
| Comparar incidencia entre grupos | Prueba de Gray (no log-rank sobre 1−KM) |

---

> **Síntesis:** en **eventos recurrentes** la correlación intra-sujeto exige **varianza robusta** (Andersen-Gill / PWP / WLW según la pregunta). En **riesgos competitivos**, **1−KM sobrestima** porque trata el competidor como censura: usa la **CIF**. El hazard **específico de causa** (censura competidores) sirve para **etiología** y el de **subdistribución (Fine-Gray)** para **riesgo absoluto**; compara con la **prueba de Gray**.

---

*Retrieval: (1) ¿por qué hace falta varianza robusta en eventos recurrentes?; (2) ¿por qué 1−KM sobrestima con competidores?; (3) ¿qué es la CIF?; (4) hazard específico de causa vs Fine-Gray: ¿cuándo cada uno?*
