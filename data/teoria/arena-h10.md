# Análisis de supervivencia IV: eventos recurrentes y riesgos competitivos

## De qué trata esta lección (y qué sabrás hacer al final)

El análisis de supervivencia básico asume un evento único y "censura" todo lo demás. Pero el mundo real tiene dos complicaciones frecuentes: eventos que se **repiten** en el mismo sujeto (recaídas, hospitalizaciones) y eventos que **compiten** —uno impide al otro (morir de una causa impide morir de otra)—. Esta lección construye, desde cero, cómo manejar ambos sin sesgar, y revela el error más común: tratar un evento competidor como censura, lo que hace que **1−KM sobrestime** la incidencia.

Al terminar podrás: (1) saber por qué los eventos recurrentes exigen varianza robusta y elegir entre AG/PWP/WLW; (2) explicar por qué 1−KM miente con riesgos competitivos y usar la **CIF** en su lugar; (3) distinguir el hazard específico de causa (etiología) del de subdistribución/Fine-Gray (riesgo absoluto); y (4) comparar grupos con la prueba de Gray. El gemelo en producto —churn vs conversión— hace todo concreto. Cierra la mecánica de supervivencia ([[arena-h7]]). *(Ejemplos clínicos ilustran el método, no son consejo médico.)*

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

## Mini-ejemplo trabajado: por qué 1−KM sobrestima

100 pacientes, dos causas de muerte mutuamente excluyentes: **cáncer** (interés) y **cardiaca** (competidora). A 5 años, supón que el riesgo *real* (CIF) de morir de cáncer es **30%** y de causa cardiaca **40%** (y 30% sigue vivo). Suma de CIFs = 0.70 ≤ 1 ✓.

Ahora calcula la incidencia de cáncer con **1−KM tratando la muerte cardiaca como censura**: KM asume que los 40 muertos por causa cardiaca *podrían* aún morir de cáncer → los "resucita" en el risk set. El resultado infla la incidencia de cáncer **por encima del 30%**, y si sumas el 1−KM de cáncer + el 1−KM de causa cardiaca puedes **pasar de 100%** — un imposible que delata el error. La **CIF** acumula riesgo solo entre los **libres de todo evento**, así que respeta la suma ≤ 1.

**Predicción antes de seguir:** un fármaco que reduce drásticamente la muerte cardiaca, ¿qué le hace a la CIF de cáncer? La **sube**: al morir menos gente del corazón, más pacientes "viven para" desarrollar cáncer. Por eso se reportan **ambos** hazards (etiología vs riesgo absoluto).

## Prototipo, contraejemplo y caso borde

- **Prototipo (riesgos competitivos):** muerte por otra causa impide el evento de interés → usa CIF y Fine-Gray para riesgo absoluto.
- **Contraejemplo (censura disfrazada):** tratar la muerte competidora como censura ordinaria (1−KM) — parece censura, pero el competidor *no puede* tener el evento luego.
- **Caso borde (eventos recurrentes correlacionados):** varias hospitalizaciones por sujeto → SE subestimados si asumes independencia; exige varianza robusta (AG/PWP/WLW).

## Errores típicos

- **Conceptual:** usar 1−KM o log-rank en presencia de riesgos competitivos (sobrestima; usa CIF y prueba de Gray).
- **De interpretación:** elegir hazard específico de causa cuando la pregunta es de **riesgo absoluto** (ahí va Fine-Gray) o viceversa.
- **Técnico:** ignorar la correlación intra-sujeto en eventos recurrentes → intervalos de confianza demasiado estrechos.

## Transferencia isomorfa

Riesgos competitivos y eventos recurrentes aparecen fuera de la clínica:

- **Riesgos competitivos ↔ destinos absorbentes mutuamente excluyentes:** un usuario que "se da de baja" no puede luego "convertir"; modelar conversión censurando las bajas como si pudieran convertir comete el mismo error de 1−KM (conecta con [[arena-h7]]).
- **Hazard específico vs subdistribución ↔ etiología vs predicción:** "¿qué causa el churn?" (específico) vs "¿qué fracción habrá churneado a 90 días?" (riesgo absoluto, Fine-Gray) — la misma dualidad causa/pronóstico de [[arena-h13]].
- **Eventos recurrentes ↔ datos agrupados:** tickets repetidos por cliente son observaciones correlacionadas; ignorarlo infla la significancia, como en cualquier modelo con clustering.

Moraleja de la arista: *cuando un evento impide a otro, censurarlo miente; usa la CIF — y "specific" responde por qué, "subdistribution" responde cuánto.*

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
