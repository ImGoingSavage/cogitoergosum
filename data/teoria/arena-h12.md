# OHDSI II: vocabularios, ETL y calidad de datos

## Vocabularios estandarizados

Cada evento clínico se representa con un **CONCEPT_ID**. Distinción clave:
- **Concepto ESTÁNDAR:** representación canónica única de una idea clínica (condiciones→**SNOMED**, fármacos→**RxNorm**, labs→**LOINC**); va en los campos `*_concept_id` para analizar.
- **Concepto FUENTE/no estándar** (ICD-10, NDC, CPT): como venía el dato; se guarda en `*_source_concept_id` y se **mapea** al estándar vía la relación **'Maps to'**.

Así, códigos fuente distintos que significan lo mismo **convergen** al mismo estándar (estandarización **semántica**). El **DOMINIO** (Condition/Drug/…) enruta cada concepto a su tabla. **CONCEPT_ANCESTOR** codifica jerarquías → seleccionar un concepto + **todos sus descendientes** (p. ej. "todos los antihipertensivos"). Un **concept set** empaqueta una idea clínica reutilizable. Ver [[vocabularios-estandarizados-omop]].

## ETL hacia el CDM

**Extract-Transform-Load:** extraer la fuente, transformar su estructura a las tablas del CDM y **mapear** los códigos fuente a conceptos estándar. Es trabajo **clínico + técnico** con decisiones documentadas. Herramientas:
- **WhiteRabbit:** escanea/perfila la fuente.
- **Rabbit-in-a-Hat:** diseña la especificación del ETL.
- **Usagi:** mapea códigos fuente → conceptos estándar.

El ETL **nunca es perfecto** (mapeos imperfectos, juicios clínicos) → documentar y someter a calidad de datos. Ver [[proceso-etl-cdm]].

## Calidad de datos (marco de Kahn)

Tres **categorías** × dos **contextos**:
- **Conformance** (¿cumple estructura/formato/relaciones?), **Completeness** (¿falta lo que debería estar?), **Plausibility** (¿valores creíbles: rangos, temporalidad?).
- **Verification** (vs reglas internas/el modelo) vs **Validation** (vs referencia externa/mundo real).

Tools: **ACHILLES** (caracterización descriptiva + alertas) y **DataQualityDashboard (DQD)** (miles de chequeos sistemáticos). **Datos malos sesgan todo aguas abajo**: la calidad de datos es el primer eslabón de la evidencia. Ver [[calidad-datos-kahn]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Capturar un concepto clínico completo | Concepto estándar + descendientes (CONCEPT_ANCESTOR) |
| Código original en los datos (ICD/NDC) | Es fuente → mapea a estándar con 'Maps to'/Usagi |
| Incorporar una base nueva | ETL: WhiteRabbit → Rabbit-in-a-Hat → Usagi |
| ¿Es apta la base? | Kahn: conformance/completeness/plausibility; corre DQD |
| "No hay registro" | ¿Ausencia de evento o de observación? |

---

> **Síntesis:** los **vocabularios** dan la semántica: conceptos **estándar** (SNOMED/RxNorm/LOINC) vs **fuente** (ICD/NDC) unidos por 'Maps to', con **jerarquías** para descendientes. El **ETL** transforma la fuente al CDM y mapea códigos (WhiteRabbit/Rabbit-in-a-Hat/Usagi) y nunca es perfecto. La **calidad de datos** (marco de **Kahn**, ACHILLES, **DQD**) es el primer eslabón de la calidad de la evidencia.

---

*Retrieval: (1) estándar vs fuente y 'Maps to'; (2) ¿qué hacen WhiteRabbit/Usagi?; (3) las 3 categorías × 2 contextos de Kahn; (4) ¿qué hace el DQD?*
