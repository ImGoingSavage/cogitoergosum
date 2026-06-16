# OHDSI I: comunidad, datos observacionales y OMOP CDM

> La **capa operacional/de estandarización** de la RWE. Complementa [[arena-h3]] (teoría causal) y [[arena-h7]] (métodos de supervivencia) con el "cómo" a escala.

## De qué trata esta lección (y qué sabrás hacer al final)

Toda la teoría causal y de supervivencia anterior necesita **datos** — y los datos de salud del mundo real (historias clínicas, claims) son enormes, sucios, incompatibles entre sistemas y recolectados para *facturar*, no para investigar. Esta lección construye, desde cero, la respuesta de la comunidad **OHDSI**: estandarizar la *estructura* de los datos con el **OMOP Common Data Model** para escribir un análisis una sola vez y correrlo en muchas bases. Es la capa de ingeniería que hace posible la evidencia del mundo real (RWE) a escala.

Al terminar podrás: (1) entender qué problema resuelve estandarizar datos y métodos; (2) leer el OMOP CDM (persona-céntrico) y por qué OBSERVATION_PERIOD distingue "no ocurrió" de "no observado"; (3) separar los tres casos de uso (caracterización, estimación, predicción); y (4) ubicar ATLAS/HADES. La distinción NULL-vs-cero entra por un ejemplo. *(Ejemplos clínicos ilustran el método, no son consejo médico.)*

## ¿Qué es OHDSI?

**OHDSI** (Observational Health Data Sciences and Informatics) es una colaboración internacional de **ciencia abierta** que genera evidencia a partir de **datos observacionales** (no de ensayos):
- **Claims** (reclamaciones): amplios en población, longitudinales, poco detalle clínico.
- **EHR** (historias clínicas): ricos en detalle, seguimiento fragmentado.

Ambos se recolectaron para **facturar/atender**, no para investigar → faltan variables, hay sesgos de codificación. La apuesta: estandarizar **datos** (OMOP CDM) y **métodos** (open-source: ATLAS, HADES) para escribir un análisis **una vez** y correrlo en muchas bases. Ver [[que-es-ohdsi-open-science]].

**Tres casos de uso:** **caracterización** (describir), **estimación a nivel de población** (causa) y **predicción a nivel de paciente** (pronóstico).

## El OMOP Common Data Model

Modelo relacional **centrado en la persona** que estandariza la **estructura** (sintaxis):
- **PERSON** + **OBSERVATION_PERIOD** (ventanas en que el paciente está observado → distingue "no ocurrió" de "no observado").
- Eventos: **VISIT/CONDITION/DRUG/PROCEDURE_OCCURRENCE**, **MEASUREMENT**, **OBSERVATION**, **DEATH**.
- Derivadas: **CONDITION_ERA / DRUG_ERA** (agrupan ocurrencias en episodios continuos por una ventana de persistencia). Ver [[omop-common-data-model]].

La estandarización **semántica** (significado) la dan los vocabularios. **Sintaxis (CDM) + semántica (vocabularios)** = análisis portables y **estudios en red**.

**Herramientas:** **ATLAS** (GUI web, sin código) y **HADES** (paquetes R: CohortMethod, PatientLevelPrediction, EmpiricalCalibration…). **EUNOMIA** = dataset OMOP de juguete para practicar.

---

## Mini-ejemplo trabajado: "no ocurrió" vs "no observado"

Paciente cuyo `OBSERVATION_PERIOD` va del 2019-01 al 2020-12 (estuvo asegurado esos dos años). Buscas si tuvo un infarto:

- Si **no hay** registro de infarto entre 2019-01 y 2020-12 → puedes afirmar "**no ocurrió** (mientras lo veíamos)".
- Si el infarto fue en **2018** (antes de su ventana) o en **2021** (después) → en tus datos figura como ausente, pero la verdad es "**no observado**". Tratar ese hueco como "sano" mete sesgo.

El `OBSERVATION_PERIOD` es justo lo que distingue ambos casos: sin él, todo NULL parece un "no". Con él, calculas denominadores correctos (persona-tiempo en riesgo) y evitas contar como sanos a quienes simplemente no mirabas.

**Predicción antes de seguir:** dos bases con el mismo SQL de "incidencia de infarto" dan números muy distintos. ¿Culpa del CDM? No necesariamente: si una base captura mejor el `OBSERVATION_PERIOD` o usa otros vocabularios fuente, el *significado* difiere. El CDM unifica la **estructura**; los vocabularios, el **significado**.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** un estudio en red que corre el mismo paquete sobre claims y EHR transformados a OMOP → resultados comparables sin compartir datos crudos.
- **Contraejemplo (caso de uso equivocado):** usar **caracterización** (descriptiva) para afirmar que un fármaco *causa* un evento — describir no es estimar; falta el diseño causal.
- **Caso borde (claims sin detalle clínico):** un valor de laboratorio que el EHR tiene pero el claim no → "no observado" por la naturaleza de la fuente, no por el paciente.

## Errores típicos

- **Conceptual:** olvidar que EHR/claims se recolectaron para **atender/facturar**, no para investigar → ausencias y sesgos de codificación sistemáticos.
- **Técnico:** leer NULL como "negativo" sin consultar el `OBSERVATION_PERIOD`.
- **De método:** mezclar los tres casos de uso (describir / causa / pronóstico) en una sola afirmación.

## Transferencia isomorfa

El CDM es un patrón de ingeniería de datos, no solo de salud:

- **OMOP CDM ↔ esquema canónico / data contract:** "transforma cada fuente a un modelo común y escribe el análisis una vez" es exactamente un *canonical data model* o un contrato de datos en una plataforma (conecta con [[arena-sd3]], sistemas de datos a escala).
- **OBSERVATION_PERIOD ↔ distinguir NULL de 0:** "ausente porque no pasó" vs "ausente porque no lo registramos" es el problema universal de datos faltantes (conecta con [[arena-h19]], el contrafactual no observado).
- **Estudio en red ↔ federación / privacidad por diseño:** correr código donde viven los datos y exportar solo agregados es el principio del aprendizaje federado.

Moraleja de la arista: *estandarizar estructura (CDM) y significado (vocabularios) convierte muchas bases sucias en una superficie analítica única; y todo NULL pregunta "¿no pasó o no miramos?".*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Proyecto de RWE con EHR/claims | Sitúalo en OMOP/OHDSI; elige caso de uso |
| ¿Describir, causa o pronóstico? | Caracterización / estimación / predicción |
| Datos de varios sistemas | Transforma al CDM (estructura) + vocabularios (significado) |
| "No hay registro" | ¿No ocurrió o no observado? → observation_period |
| Análisis reproducible en muchas bases | CDM + ATLAS/HADES → estudio en red |

---

> **Síntesis:** OHDSI es **ciencia abierta** sobre **datos observacionales** que estandariza datos (**OMOP CDM**, persona-céntrico: PERSON/OBSERVATION_PERIOD/tablas de eventos/era) y métodos (ATLAS/HADES). La estandarización **sintáctica (CDM) + semántica (vocabularios)** permite escribir el análisis una vez y correrlo en toda la red. Tres casos de uso: **caracterización, estimación, predicción**.

---

*Retrieval: (1) ¿qué estandariza el CDM y qué los vocabularios?; (2) ¿para qué sirve OBSERVATION_PERIOD?; (3) los 3 casos de uso; (4) ATLAS vs HADES.*
