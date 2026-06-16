Actúa como un software engineer senior especializado en frontend vanilla JavaScript, arquitectura local-first, Supabase, diseño de producto educativo y refactor seguro en aplicaciones ya existentes.

Vas a trabajar sobre el repositorio actual de CogitoErgoSum.

## Contexto del proyecto

CogitoErgoSum es una app educativa desplegada en GitHub Pages, con frontend HTML/CSS/JavaScript vanilla, persistencia local y sincronización con Supabase.

Actualmente existe una fase de estudio llamada:

**Fase 7 · Arena de Entrevistas de Élite**

En esta fase hay 8 clusters principales. Cada cluster contiene varias lecciones/unidades. Cada lección tiene asociado un banco de preguntas, normalmente entre 30 y 60 preguntas.

Ejemplos visibles de clusters:

* Probabilidad, esperanza y conteo (Quant)
* Estadística aplicada e inferencia
* Estructuras de datos y algoritmos (MAANG)
* Diseño de sistemas (MAANG)
* Ciencia de datos aplicada
* ML Systems y feature pipelines
* Causalidad y Health AI / RWE
* Conductual y comunicación bajo presión

Ejemplo de lección dentro de un cluster:

* Cluster: Probabilidad, esperanza y conteo
* Lección: Fundamentos de probabilidad y conteo
* Banco de preguntas asociado a esa lección

Actualmente las preguntas aparecen de forma arbitraria o sin control explícito de dificultad por parte del usuario.

## Objetivo principal

Implementar un sistema de dificultad para las preguntas de la Fase 7 Arena.

Cada pregunta debe poder clasificarse como:

* `easy`
* `medium`
* `hard`

En la interfaz del usuario debe existir una forma clara de elegir el nivel de dificultad antes de practicar una lección o antes de iniciar el examen final de un cluster.

## Funcionalidad requerida

### 1. Clasificación de preguntas por dificultad

Inspecciona el repositorio y localiza dónde viven los bancos de preguntas de la Fase 7 Arena.

Para cada pregunta asociada a una lección, agrega o normaliza metadata de dificultad usando un campo compatible con el esquema actual.

Preferencia de campo:

```json
"difficulty": "easy" | "medium" | "hard"
```

Si ya existe un campo equivalente, reutilízalo en vez de crear otro.

Si el esquema actual no permite agregar metadata directamente sin romper consumidores existentes, diseña una adaptación mínima y compatible.

No borres preguntas existentes.

No cambies IDs salvo que sea estrictamente necesario.

No alteres el contenido pedagógico de las preguntas salvo que sea necesario para clasificarlas o corregir errores evidentes.

### 2. Criterios para clasificar dificultad

Usa estos criterios como guía inicial:

#### Easy

Pregunta directa de reconocimiento, definición, intuición básica o aplicación inmediata.

Ejemplos:

* Identificar cuándo usar una regla.
* Aplicar una fórmula directa.
* Reconocer un concepto.
* Resolver un caso pequeño sin combinaciones de ideas.

#### Medium

Pregunta que exige combinar 2 o más ideas, hacer un razonamiento intermedio o evitar un error común.

Ejemplos:

* Conteo con restricción.
* Esperanza con variable indicadora.
* Caso SQL con agrupación y filtro temporal.
* Algoritmo con análisis de complejidad básico.
* Inferencia donde hay que identificar supuesto.

#### Hard

Pregunta que exige transferencia, varios pasos, caso borde, razonamiento bajo presión o mezcla de dominios.

Ejemplos:

* Problema tipo entrevista Quant/MAANG.
* Caso con trampa conceptual.
* Combinación de probabilidad + conteo + esperanza.
* Problema de causalidad con confounders/colliders.
* Diseño de sistema con tradeoffs reales.
* ML system con leakage, drift, features y validación temporal.

Si una pregunta no puede clasificarse con seguridad, usa:

```json
"difficulty": "medium",
"needs_review": true
```

o el patrón equivalente compatible con el esquema real.

### 3. Selector de dificultad por lección

Cuando el usuario seleccione una lección, por ejemplo:

**Fundamentos de probabilidad y conteo**

la pantalla de práctica debe permitir elegir dificultad antes o durante la generación de preguntas.

Debe haber al menos estas opciones:

* Fácil
* Medio
* Difícil
* Mixto

Comportamiento esperado:

* Si el usuario elige Fácil, sólo se cargan preguntas `easy`.
* Si el usuario elige Medio, sólo se cargan preguntas `medium`.
* Si el usuario elige Difícil, sólo se cargan preguntas `hard`.
* Si el usuario elige Mixto, se cargan preguntas de todas las dificultades.

La opción por defecto debe ser `Mixto` si eso conserva mejor el comportamiento actual.

La UI debe integrarse con el estilo visual actual de Arena: sobria, oscura, con botones o controles consistentes con el diseño existente.

No hagas un rediseño visual masivo.

### 4. Selección aleatoria de preguntas por lección

La selección de preguntas debe ser aleatoria dentro del banco filtrado por dificultad.

Ejemplo:

Si la lección tiene 50 preguntas y el usuario elige `hard`, la app debe filtrar las preguntas `hard` y seleccionar aleatoriamente la dosis configurada para esa lección.

Reglas:

* No debe repetir preguntas dentro de una misma sesión si hay suficientes preguntas disponibles.
* Si hay menos preguntas disponibles que la dosis requerida, usa todas las preguntas disponibles y muestra una nota discreta o maneja el caso sin romper la UI.
* No debe crashear si una dificultad no tiene preguntas.
* Si no hay preguntas para la dificultad elegida, muestra un estado vacío claro y permite cambiar la dificultad.

### 5. Examen final por cluster

Al final de cada cluster debe existir una opción de:

**Examen final del cluster**

Ejemplo:

Cluster: Probabilidad, esperanza y conteo

El examen final debe construirse usando todas las preguntas asociadas a todas las lecciones de ese cluster.

El usuario debe poder seleccionar dificultad antes de iniciar el examen:

* Fácil
* Medio
* Difícil
* Mixto

Comportamiento esperado:

* Fácil: genera examen aleatorio sólo con preguntas `easy` de todo el cluster.
* Medio: genera examen aleatorio sólo con preguntas `medium` de todo el cluster.
* Difícil: genera examen aleatorio sólo con preguntas `hard` de todo el cluster.
* Mixto: genera examen aleatorio mezclando dificultades.

El examen final debe tomar preguntas de varias lecciones del cluster, no sólo de la última lección.

Si el esquema actual ya tiene una lógica de “examen se abre al completar todas las unidades del bloque”, respétala salvo que encuentres una razón clara para modificarla. Si debe seguir bloqueado hasta completar el cluster, conserva esa regla. Si ya hay un patrón de desbloqueo, úsalo.

### 6. Cantidad de preguntas del examen final

Inspecciona el sistema actual para ver si ya existe una cantidad/dosis para exámenes.

Si existe, reutilízala.

Si no existe, propón una constante configurable, por ejemplo:

```js
const DEFAULT_CLUSTER_EXAM_SIZE = 25;
```

Reglas:

* No hardcodees cantidades dispersas en muchos lugares.
* Centraliza la configuración.
* Si no hay suficientes preguntas filtradas por dificultad, usa las disponibles.
* La selección debe ser aleatoria sin repetición dentro del examen.

### 7. Persistencia y progreso

No rompas la persistencia actual del progreso del usuario.

Revisa cómo se guarda actualmente:

* progreso de lecciones,
* respuestas,
* sesión actual,
* avance por cluster,
* sincronización local/Supabase si aplica.

La nueva selección de dificultad debe integrarse sin borrar progreso existente.

Si decides persistir la última dificultad elegida por el usuario, hazlo de forma compatible y no invasiva.

Preferencia:

* Persistir última dificultad por lección.
* Persistir última dificultad por cluster exam.
* Si esto complica demasiado la primera implementación, dejarlo como mejora posterior documentada.

### 8. Arquitectura esperada

Antes de editar, inspecciona:

* archivos principales de Arena,
* estructura de datos de Fase 7,
* funciones de renderizado de clusters,
* funciones de renderizado de lecciones,
* lógica de preguntas,
* lógica de progreso,
* storage local,
* integración Supabase si existe en este flujo.

No inventes rutas.

No inventes nombres de archivos.

No hagas cambios globales innecesarios.

Prioriza una implementación pequeña, robusta y compatible.

Idealmente separa la lógica en funciones claras como:

```js
getQuestionsByLesson(...)
filterQuestionsByDifficulty(...)
shuffleQuestions(...)
selectRandomQuestions(...)
getClusterQuestionPool(...)
buildClusterExam(...)
```

Usa los nombres reales y patrones reales del repositorio.

### 9. Reglas de compatibilidad

Debes respetar:

* GitHub Pages.
* JavaScript vanilla.
* Sin dependencias innecesarias.
* Sin backend obligatorio nuevo.
* Sin romper LocalStorage.
* Sin romper Supabase.
* Sin romper el service worker o manifest.
* Sin cambiar masivamente la estructura visual.
* Sin eliminar contenido curado.

### 10. Manejo de edge cases

Implementa o deja correctamente manejados estos casos:

* Una pregunta no tiene difficulty.
* Una lección tiene preguntas sólo de una dificultad.
* Una dificultad seleccionada no tiene preguntas.
* El cluster tiene lecciones sin banco de preguntas.
* El examen final no tiene suficientes preguntas.
* El usuario cambia dificultad a mitad de flujo.
* Preguntas duplicadas entre lecciones.
* Datos antiguos sin metadata nueva.
* Progreso viejo guardado en LocalStorage.
* Supabase contiene registros anteriores al cambio.

### 11. Plan de trabajo obligatorio

Antes de modificar código, entrega un plan breve con:

1. Archivos detectados como relevantes.
2. Modelo mental del flujo actual de Arena.
3. Dónde viven las preguntas.
4. Cómo se seleccionan actualmente.
5. Dónde conviene introducir `difficulty`.
6. Qué UI se va a tocar.
7. Cómo se construirá el examen final de cluster.
8. Riesgos de compatibilidad.
9. Cómo validar.

Después implementa.

### 12. Implementación

Haz los cambios necesarios para:

1. Añadir o normalizar difficulty en preguntas de Arena.
2. Implementar filtro por dificultad en práctica de lección.
3. Implementar selector visual de dificultad.
4. Implementar pool de preguntas por cluster.
5. Implementar examen final por cluster con dificultad.
6. Manejar estados vacíos.
7. Mantener comportamiento actual cuando se elige `Mixto`.
8. Validar que no se rompe el flujo existente.

### 13. Validación obligatoria

Después de implementar, ejecuta las validaciones disponibles.

Si hay tests, ejecútalos.

Si no hay tests, valida manualmente al menos:

* La app carga.
* La Fase 7 Arena renderiza.
* Los 8 clusters siguen apareciendo.
* Las lecciones siguen apareciendo dentro de cada cluster.
* Una lección puede iniciar preguntas en modo Fácil.
* Una lección puede iniciar preguntas en modo Medio.
* Una lección puede iniciar preguntas en modo Difícil.
* Una lección puede iniciar preguntas en modo Mixto.
* El examen final aparece donde corresponde.
* El examen final filtra por dificultad.
* No hay errores en consola.
* Los JSON siguen siendo parseables.
* No hay IDs duplicados accidentales.
* No se perdió contenido curado.
* El flujo viejo funciona usando Mixto.

### 14. Resultado esperado en la UI

En una lección, el usuario debería poder hacer algo como:

1. Entrar a “Fundamentos de probabilidad y conteo”.
2. Ver selector de dificultad:

   * Fácil
   * Medio
   * Difícil
   * Mixto
3. Elegir dificultad.
4. Recibir preguntas aleatorias sólo de ese nivel.
5. Cambiar dificultad si no hay preguntas suficientes o si quiere practicar otro nivel.

En un cluster, el usuario debería poder hacer algo como:

1. Entrar a “Probabilidad, esperanza y conteo”.
2. Completar o acceder según las reglas actuales al examen final.
3. Elegir:

   * Examen fácil
   * Examen medio
   * Examen difícil
   * Examen mixto
4. Recibir una selección aleatoria de preguntas tomadas de todas las lecciones de ese cluster, filtradas por dificultad.

### 15. Reporte final

Al terminar, entrega un reporte con:

1. Resumen ejecutivo.
2. Archivos modificados.
3. Campos nuevos o reutilizados.
4. Cómo se clasificaron las preguntas.
5. Cómo funciona el selector por lección.
6. Cómo funciona el examen final por cluster.
7. Cómo se manejan preguntas sin dificultad.
8. Validaciones realizadas.
9. Riesgos pendientes.
10. Siguiente mejora recomendada.

## Instrucción final

Empieza inspeccionando el repositorio.

No propongas una arquitectura abstracta sin mirar el código real.

Implementa la solución de forma incremental, conservadora y compatible con el estado actual de CogitoErgoSum.

El objetivo es que Arena deje de lanzar preguntas arbitrarias y permita práctica deliberada por dificultad, tanto por lección como por examen final de cluster.
