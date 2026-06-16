# Encuadre de problemas de ML: objetivos y tipos de tarea

## De qué trata esta lección (y qué sabrás hacer al final)

Antes de elegir un modelo, hay una decisión que decide el destino del proyecto: **cómo encuadras el problema**. Un modelo con accuracy espectacular muere joven si no mueve ninguna métrica de negocio; un sistema con objetivos en conflicto se vuelve inmantenible si los metes en una sola loss. Esta lección construye, desde cero, el arte del encuadre: atar el ML al negocio, desacoplar objetivos que tiran en direcciones opuestas, y elegir el tipo de tarea pensando en cuánto costará *mantener* el sistema.

Al terminar podrás: (1) explicar por qué la métrica de ML debe mapear a una de negocio; (2) desacoplar objetivos en conflicto (un modelo por objetivo, combinados al rankear) para reajustar sin reentrenar; (3) distinguir multiclase de multietiqueta; y (4) reconocer cuándo reformular clasificación como regresión/ranking ahorra reentrenamientos. Cada idea entra por un ejemplo de producto. Conecta con la disciplina de las Reglas de ML ([[arena-rom1]]).

## Objetivo de negocio vs objetivo de ML

El error más común de los proyectos de ML que mueren jóvenes: optimizar **métricas de ML** (accuracy, F1) sin atarlas a **métricas de negocio** (ingresos, retención). A la dirección solo le importan las de negocio. Antes de modelar hay que responder: *¿cómo mueve este modelo una métrica de negocio?* Cuando el mapeo es directo —click-through de anuncios, detección de fraude— el ML prospera; cuando es difuso, el proyecto se cancela.

## Desacoplar objetivos (decoupling objectives)

Cuando un sistema persigue **varios objetivos en conflicto** (p.ej. maximizar engagement **y** calidad del contenido), no los metas en una sola loss ponderada `α·calidad + β·engagement`: si reajustas los pesos hay que **reentrenar**. Mejor entrena **un modelo por objetivo** y combina sus scores en el ranking; así reajustar la prioridad es solo cambiar la combinación, sin reentrenar. Desacoplar también permite razonar sobre cada objetivo por separado.

## ¿Usar ML o no?

ML tiene sentido cuando hay **patrones** que aprender, los **datos** existen, el problema es **repetitivo**, el coste de un error es tolerable y la respuesta no necesita ser perfecta. Si una **heurística simple** basta, empieza por ahí. ML es mala elección cuando es poco ético, cuando una regla más barata resuelve, o cuando cada decisión es única y sin patrón.

## Tipos de tarea de ML

- **Clasificación binaria vs multiclase:** con muchas clases (alta cardinalidad) el problema se vuelve difícil; conviene tener suficientes ejemplos por clase.
- **Multiclase vs multietiqueta (multilabel):** en multiclase cada ejemplo pertenece a **una** clase; en **multietiqueta** puede pertenecer a varias a la vez (un artículo es "tech" y "finanzas"). Es, según Huyen, el tipo de tarea que más problemas suele dar (representación y métricas más enredadas).
- **Reformular el encuadre:** un mismo problema admite varios encuadres. Predecir "qué app abrirá el usuario" como **clasificación** (una salida por app, hay que reentrenar al añadir apps) o como **regresión/ranking** (puntuar cada par usuario-app, añadir apps no exige reentrenar) cambia radicalmente la mantenibilidad.

## El proceso es iterativo

Diseñar un sistema de ML no es lineal: encuadrar el problema, reunir datos, entrenar, evaluar, desplegar, monitorear y **volver** a encuadrar a la luz de lo aprendido. Esperar iteración desde el principio evita sorpresas.

---

## Mini-ejemplo trabajado: desacoplar objetivos en un feed

Un feed quiere **maximizar engagement** *y* **calidad del contenido**, que tiran en direcciones opuestas (el clickbait engancha pero baja la calidad). La tentación es una sola loss:

`loss = α·engagement + β·calidad`

Problema: si producto decide que ahora la calidad pesa más, hay que cambiar β y **reentrenar todo** — caro y lento. La jugada de desacople: entrena **dos modelos**, uno que predice engagement y otro que predice calidad, y combínalos *en el ranking*:

`score = α·ŝ_engagement + β·ŝ_calidad`

Ahora reajustar la prioridad es cambiar α, β en la combinación, **sin reentrenar**, y puedes razonar sobre cada objetivo por separado.

**Predicción antes de seguir:** el equipo quiere recomendar por "vídeo realmente visto" en vez de por click (para matar el clickbait). ¿Es un cambio de features o de **encuadre**? De encuadre: pasas de clasificación (click sí/no) a regresión sobre fracción vista — y ojo con el **label bias** al cambiar el objetivo.

## Prototipo, contraejemplo y caso borde

- **Prototipo (ML justificado):** patrón aprendible + datos + repetición + error tolerable + mapeo claro a métrica de negocio → adelante.
- **Contraejemplo (accuracy huérfana):** un modelo con F1 altísimo que no mueve ninguna métrica de negocio → muere joven; la métrica de ML era un fin en sí misma.
- **Caso borde (multietiqueta):** un artículo que es "tech" *y* "finanzas" a la vez no es multiclase (una de N) sino **multilabel** → sigmoid + multi-hot + umbral por clase, no softmax.

## Errores típicos

- **Conceptual:** optimizar la métrica de ML (accuracy/F1) sin atarla a una de **negocio** — el fallo nº1 de proyectos que mueren.
- **De diseño:** meter objetivos en conflicto en una sola loss ponderada → cada reajuste exige reentrenar.
- **De encuadre:** elegir clasificación cuando añadir una categoría obliga a reentrenar; un encuadre de regresión/ranking por par lo evita.

## Transferencia isomorfa

El encuadre de objetivos es un patrón que cruza dominios:

- **Métrica de ML vs de negocio ↔ proxy vs meta real:** el riesgo de optimizar un proxy desalineado es el mismo que en las Reglas de ML (lanzamiento multi-métrica) y en quant (optimizar la señal equivocada) (conecta con [[arena-rml1]]).
- **Desacoplar objetivos ↔ separar modelos componibles:** un modelo por objetivo combinado al servir es pariente de los ensembles aislados que evitan el entanglement de la deuda técnica (conecta con [[arena-htd1]]).
- **Multilabel sigmoid ↔ Bernoullis independientes:** tratar cada etiqueta como un 0/1 independiente es exactamente modelar variables indicadoras por separado (conecta con la linealidad/indicadores de [[arena-q1]]).

Moraleja de la arista: *el encuadre decide el destino del proyecto: ata el ML al negocio, desacopla objetivos en conflicto y elige el tipo de tarea pensando en cuánto costará mantenerlo.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Mi modelo tiene gran accuracy pero nadie lo usa" | Átalo a una métrica de NEGOCIO, no solo de ML |
| "Tengo objetivos en conflicto (engagement vs calidad)" | Desacopla: un modelo por objetivo, combina scores |
| "¿Debería usar ML aquí?" | ¿Hay patrón, datos, repetición y error tolerable? Si no, heurística |
| "Un ejemplo puede tener varias clases" | Multietiqueta (multilabel), no multiclase |
| "Añadir una categoría me obliga a reentrenar todo" | Reencuadra como regresión/ranking por par |

---

> **Síntesis:** El encuadre manda. Un sistema de ML solo sobrevive si su métrica de ML se mapea a una **métrica de negocio**. Con objetivos en conflicto, **desacóplalos** (un modelo por objetivo, combinados al rankear) para reajustar prioridades sin reentrenar. Usa ML solo si hay patrón, datos, repetición y coste de error tolerable. Y elige bien el **tipo de tarea** —binaria/multiclase/**multietiqueta**, o reformular como clasificación vs regresión/ranking—, porque el encuadre decide cuánto cuesta mantener el sistema.

---

*Retrieval: cierra y responde: (1) ¿por qué un modelo con buena accuracy puede ser un fracaso?; (2) ¿qué es desacoplar objetivos y qué problema resuelve?; (3) distingue multiclase de multietiqueta; (4) ¿cuándo NO conviene usar ML?*
