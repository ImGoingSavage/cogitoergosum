# ROL

Actúa como un equipo multidisciplinario compuesto por:

* Arquitecto Senior de Software
* Investigador en Ciencias Cognitivas
* Especialista en Neurociencia del Aprendizaje
* Diseñador de Experiencias Educativas
* Experto en Psicología Cognitiva
* Diseñador UX/UI para herramientas de aprendizaje profundo
* Especialista en Aprendizaje Adaptativo

Tu objetivo es construir una aplicación local de entrenamiento mental deliberado, no una plataforma de ejercicios tradicional.

---

# MISIÓN

Crear una Web App local utilizando exclusivamente:

* HTML
* CSS
* JavaScript Vanilla

Sin frameworks.
Sin backend.
Sin dependencias externas.

La aplicación se llamará:

# Curaduría de Problem Solving General

Su objetivo es desarrollar capacidades transferibles de resolución de problemas mediante práctica deliberada y metacognición.

NO quiero una copia de:

* LeetCode
* HackerRank
* Brilliant
* Khan Academy

Tampoco quiero una plataforma centrada exclusivamente en programación.

La aplicación debe entrenar:

* Pensamiento matemático
* Pensamiento algorítmico
* Pensamiento estratégico
* Modelado mental
* Toma de decisiones
* Creatividad estructurada
* Capacidad de abstracción
* Transferencia de conocimiento entre dominios

---

# PRINCIPIOS PEDAGÓGICOS OBLIGATORIOS

Toda decisión de diseño debe estar fundamentada en evidencia proveniente de:

## Psicología Cognitiva

Aplicar:

* Retrieval Practice
* Productive Struggle
* Desirable Difficulties
* Generation Effect
* Metacognición

## Neurociencias

Favorecer:

* Consolidación de memoria
* Reconsolidación
* Esfuerzo cognitivo profundo
* Atención sostenida
* Formación de esquemas

## Ciencia del Aprendizaje

Aplicar:

* Interleaving
* Spaced Repetition
* Active Recall
* Transfer Learning
* Deliberate Practice

---

# PRINCIPIO FUNDAMENTAL

NO mostrar etiquetas de clasificación al usuario antes de resolver.

NO indicar:

* Estrategia Mental
* Tipo de problema
* Categoría

La clasificación existe únicamente para el motor adaptativo.

El usuario debe descubrir por sí mismo qué herramientas mentales utilizar.

Inspirarse en:

* Olimpiadas matemáticas
* Problemas de Fermi
* Acertijos de razonamiento
* Pensamiento lateral
* Competencias de resolución de problemas

La experiencia debe obligar al usuario a pensar sin andamiaje.

---

# BASE DE DATOS

Crear un archivo:

data/problems.json

Los problemas estarán clasificados internamente por:

## Estrategias Mentales

### Inversión

Pensar hacia atrás.

### Optimización

Maximizar o minimizar recursos.

### Invariantes

Detectar lo que permanece constante.

### Patrones

Encontrar regularidades ocultas.

---

# ESTRUCTURA JSON

Cada problema debe contener:

```json
{
  "id": 1,
  "titulo": "",
  "estrategia": "",
  "dificultad": 1,
  "enunciado": "",
  "hints": [],
  "solucion": "",
  "explicacion": "",
  "tiempo_estimado": 20,
  "conceptos": [],
  "transferencias": []
}
```

Generar mínimo:

* 40 problemas

Distribuidos entre:

* Matemáticos
* Algorítmicos
* Cotidianos
* Estratégicos
* Pensamiento lateral
* Estimación
* Optimización de decisiones

---

# UN PROBLEMA AL DÍA

Al abrir la aplicación:

Mostrar únicamente:

* Enunciado
* Dificultad visual mínima

No mostrar:

* Categoría
* Etiquetas
* Estrategia

La experiencia debe sentirse como una sesión diaria de entrenamiento mental.

El sistema debe:

* Elegir automáticamente el problema
* Evitar repeticiones
* Guardar progreso
* Persistir en LocalStorage

---

# TEMPORIZADOR DE REFLEXIÓN

Implementar un temporizador obligatorio de:

20 minutos

Durante ese tiempo:

* La solución permanece bloqueada
* No se puede revelar la respuesta

Mostrar:

* Temporizador
* Barra de progreso

Persistir incluso al recargar la página.

---

# DESCONSTRUCCIÓN OBLIGATORIA

Antes de revelar cualquier solución:

El usuario debe completar una sección llamada:

# Mi Desconstrucción

Debe responder implícitamente:

* ¿Qué información tengo?
* ¿Qué información falta?
* ¿Qué restricciones existen?
* ¿Qué hipótesis considero?
* ¿Qué estrategias podría probar?
* ¿Qué analogías encuentro?

Requisitos:

* Mínimo 200 caracteres
* Auto guardado
* Contador de caracteres
* Persistencia local

Hasta completar esto:

NO se puede acceder a la solución.

---

# SISTEMA DE HINTS INTELIGENTES

Implementar un sistema progresivo de pistas.

Objetivo:

Ayudar sin destruir el aprendizaje.

Los hints deben liberarse gradualmente.

Nivel 1:

Redirigir atención.

Nivel 2:

Señalar una estructura relevante.

Nivel 3:

Reducir el espacio de búsqueda.

Nivel 4:

Sugerir una posible estrategia.

Nivel 5:

Prácticamente revelar el camino.

Reglas:

* Cada hint solicitado reduce la puntuación.
* Registrar cuántos hints fueron utilizados.
* Guardar historial.

Los hints deben sentirse socráticos.

Evitar dar respuestas directas.

---

# SISTEMA DE REFLEXIÓN POSTERIOR

Después de revelar la solución:

Mostrar:

## Comparación

Mi enfoque vs solución propuesta.

## Reflexión

¿Qué aprendí?

## Transferencia

¿Dónde más podría aplicar esta idea?

---

# MOTOR ADAPTATIVO

Implementar un sistema de dificultad dinámica.

Factores:

* Calidad de autoevaluación
* Tiempo invertido
* Cantidad de hints usados
* Frecuencia de éxito
* Historial reciente

Ejemplo:

```javascript
if (
 score > 85 &&
 hintsUsed <= 1 &&
 completionTime < expectedTime
)
 difficulty++;
```

y

```javascript
if (
 score < 50 ||
 hintsUsed >= 3
)
 difficulty--;
```

---

# INTERLEAVING

El sistema debe favorecer aprendizaje intercalado.

NO presentar problemas consecutivos de la misma estrategia.

El usuario nunca debe notar explícitamente el patrón.

La mezcla debe ser automática.

Objetivo:

Forzar recuperación de estrategias desde memoria.

---

# REPETICIÓN ESPACIADA

Los problemas difíciles o fallados deben reaparecer.

No inmediatamente.

Usar intervalos crecientes:

* 3 días
* 7 días
* 14 días
* 30 días

Mantener historial de revisiones.

---

# DASHBOARD COGNITIVO

Agregar una sección avanzada.

Mostrar:

* Problemas resueltos
* Tasa de éxito
* Tiempo promedio
* Hints utilizados
* Estrategias dominadas
* Estrategias débiles
* Racha diaria
* Curva de dificultad

Crear visualizaciones usando:

* CSS
* SVG
* JavaScript

Sin librerías externas.

---

# DISEÑO VISUAL

Inspiración:

* Obsidian
* Readwise Reader
* Linear
* Raycast
* Superhuman

Características:

* Dark Mode
* Diseño minimalista
* Alto contraste
* Tipografía moderna
* Responsive
* Sin distracciones

La interfaz debe transmitir:

"Entrenamiento intelectual serio"

y no

"Sitio de ejercicios escolares".

---

# ARQUITECTURA

Separar el código en módulos.

```text
index.html

css/
  styles.css

js/
  app.js
  storage.js
  timer.js
  adaptiveEngine.js
  hintSystem.js
  spacedRepetition.js
  analytics.js

data/
  problems.json
```

Utilizar:

* ES6 Modules
* Código limpio
* Comentarios claros
* Principios SOLID cuando sea posible

---

# ENTREGABLES

Genera la aplicación completa.

Incluye:

1. Arquitectura de carpetas.
2. Todos los archivos.
3. HTML completo.
4. CSS completo.
5. JavaScript completo.
6. JSON con 40 problemas.
7. Sistema de hints.
8. Temporizador persistente.
9. Adaptación de dificultad.
10. Interleaving.
11. Repetición espaciada.
12. Dashboard cognitivo.
13. Persistencia LocalStorage.
14. Diseño responsive.

Presenta todo el resultado dentro de un único artefacto interactivo bien organizado mostrando claramente cada archivo y su contenido.

No resumas código.
No uses pseudocódigo.
Entrega una implementación funcional completa.

# FILOSOFÍA CENTRAL DE ENTRENAMIENTO

La aplicación debe inspirarse explícitamente en:

* George Pólya
* Entrenamiento de Olimpiadas Matemáticas
* Art of Problem Solving (AoPS)
* Investigación sobre Deliberate Practice
* Teoría del Flujo (Flow)
* Aprendizaje Adaptativo
* Desirable Difficulties
* Productive Struggle

El objetivo NO es resolver la mayor cantidad de problemas.

El objetivo es desarrollar capacidad general de resolución de problemas.

---

# MARCO DE PÓLYA

Toda la experiencia debe estar estructurada alrededor de las cuatro fases clásicas de Pólya:

## 1. Comprender el problema

La aplicación debe obligar al usuario a responder preguntas como:

* ¿Qué se pide?
* ¿Qué información tengo?
* ¿Qué información parece irrelevante?
* ¿Puedo reformular el problema?

---

## 2. Diseñar un plan

La aplicación debe promover:

* Analogías
* Casos simples
* Trabajar hacia atrás
* Dibujos
* Tablas
* Búsqueda de patrones
* Descomposición

---

## 3. Ejecutar el plan

Permitir al usuario registrar:

* Intentos
* Hipótesis
* Errores
* Caminos descartados

---

## 4. Reflexionar

Después de resolver:

* ¿Qué aprendí?
* ¿Qué señal me hizo avanzar?
* ¿Dónde puedo reutilizar esta idea?
* ¿Qué estrategia fue decisiva?

---

# REGLA OLÍMPICA DE DIFICULTAD ÓPTIMA

El motor adaptativo debe inspirarse en prácticas reales de entrenamiento olímpico.

Principio:

El usuario debe permanecer en una zona donde pueda resolver aproximadamente entre el 30% y el 50% de los problemas sin ayuda.

Razón:

Resolver menos del 30% produce frustración.

Resolver más del 50%-60% genera estancamiento.

La aplicación debe intentar mantener dinámicamente esta zona de aprendizaje.

---

# ALGORITMO DE AJUSTE

Monitorear:

* Problemas resueltos
* Tiempo requerido
* Cantidad de hints
* Calidad de la desconstrucción
* Frecuencia de éxito

Ejemplo:

```javascript id="0y4w4o"
if (successRate > 0.55)
{
   difficulty++;
}

if (successRate < 0.30)
{
   difficulty--;
}
```

El objetivo no es maximizar aciertos.

El objetivo es maximizar crecimiento.

---

# CURACIÓN DE PROBLEMAS

La aplicación debe ser capaz de construir una biblioteca de problemas proveniente de fuentes públicas y educativas.

Fuentes deseables:

* Problemas de Olimpiadas Matemáticas nacionales e internacionales
* IMO Shortlist
* USAMO
* AMC
* AIME
* EGMO
* OMM
* Olimpiada Mexicana de Matemáticas
* Cuadernillos olímpicos mexicanos
* AoPS
* Project Euler
* Brilliant
* LeetCode
* Khan Academy
* Problemas de lógica clásicos
* Problemas de Fermi
* Acertijos matemáticos históricos
* Competencias universitarias

La aplicación debe almacenar además:

```json id="mfh1qi"
{
  "source": "",
  "source_url": "",
  "year": "",
  "difficulty": "",
  "tags": []
}
```

---

# SISTEMA DE CURACIÓN AUTOMÁTICA

No quiero únicamente consumir problemas existentes.

Quiero que la IA pueda:

1. Analizar problemas originales.
2. Detectar la estrategia mental subyacente.
3. Generar variantes isomórficas.
4. Crear problemas equivalentes con distinto contexto.
5. Generar nuevas versiones manteniendo la misma estructura cognitiva.

Objetivo:

Entrenar esquemas mentales y no memorización.

---

# INTEGRACIÓN CON IA

Diseñar la arquitectura para utilizar la API de Claude.

La IA debe actuar como mentor socrático.

NO debe dar respuestas inmediatamente.

Debe ser capaz de:

* Analizar la desconstrucción del usuario.
* Detectar bloqueos cognitivos.
* Generar hints progresivos.
* Formular preguntas orientadoras.
* Evaluar razonamiento.
* Identificar estrategias utilizadas.
* Recomendar problemas futuros.

---

# MODO MENTOR SOCRÁTICO

La IA nunca debe responder:

"la solución es..."

Antes debe intentar:

* Preguntar
* Guiar
* Reenfocar
* Reducir el espacio de búsqueda
* Recordar herramientas mentales relevantes

Inspirarse en:

* Tutoría olímpica
* Método socrático
* Coaching cognitivo

---

# MOTOR DE GENERACIÓN DE HINTS

Los hints deben generarse dinámicamente mediante IA.

Cada hint debe pertenecer a uno de cinco niveles:

Nivel 1:
Observación general.

Nivel 2:
Detectar una restricción importante.

Nivel 3:
Sugerir una representación útil.

Nivel 4:
Sugerir una estrategia.

Nivel 5:
Prácticamente revelar el método.

La calidad del entrenamiento debe disminuir conforme aumente el nivel solicitado.

---

# VISIÓN A LARGO PLAZO

La aplicación debe evolucionar hacia un entrenador cognitivo personal impulsado por IA.

No debe comportarse como una biblioteca de ejercicios.

Debe comportarse como un entrenador olímpico digital que aprende continuamente del usuario y adapta:

* dificultad,
* secuencia,
* estrategias,
* hints,
* revisiones,
* problemas futuros.

