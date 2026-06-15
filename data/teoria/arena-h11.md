# OHDSI I: comunidad, datos observacionales y OMOP CDM

> La **capa operacional/de estandarización** de la RWE. Complementa [[arena-h3]] (teoría causal) y [[arena-h7]] (métodos de supervivencia) con el "cómo" a escala.

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
