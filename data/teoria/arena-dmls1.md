# Encuadre de problemas de ML: objetivos y tipos de tarea

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
