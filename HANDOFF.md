# HANDOFF — Estado del proyecto y plan de continuación

Documento de contexto para el siguiente agente que trabaje en este proyecto.
Fecha de corte: 2026-06-10. **Actualizado 2026-06-12.**

> **⚠️ ACTUALIZACIÓN 2026-06-11 — léela antes que nada:**
> 1. El proyecto pasa a llamarse **CogitoErgoSum**. La extensión del plan vive
>    en `HANDOFFCES.md` (identidad §1, motivación §2, escalabilidad §3, Claude
>    por usuario §4) y su **Constitución §0 es LEY** para toda decisión nueva.
> 2. Estado de fases (bitácoras en HANDOFFCES §5.1-§5.3): **✅ Fase A**
>    (identidad "la biblioteca", lenguaje, timer pausable 20-120 min, PWA),
>    **✅ Fase B** (insignias, fresh start, rating por heurística, avatar),
>    **✅ Fase C** (cuentas + sincronización offline-first con Supabase
>    `rcaljqmibtkorcmdyqvg` + cron keep-alive en GitHub Actions; E2E 8/8),
>    **✅ Fase D** (el claustro: amistades por código, vitrina,
>    reconocimiento ❧; 4.ª pestaña).
> 3. **Si vienes a continuar el proyecto: empieza por HANDOFFCES §5.4**
>    ("Mapa para el siguiente agente"): infraestructura viva, ritual de
>    verificación y la lista de QUÉ FALTA en orden de valor (E2E social,
>    "Pensar juntos" aprobado con sorteo del pool común, chat socrático,
>    ingestión Fase 4+, publicación del frontend).

---

## 0. NORTE DEL PROYECTO: `Definitivo.pdf` (léelo antes de curar problemas)

Esta app NO es un proyecto aislado: existe para ejecutar la **Parte I ("El motor
cognitivo — la biblioteca de problemas")** del documento maestro del usuario,
`Definitivo.pdf` (85 pp., copia en la raíz del proyecto). El usuario (Edgar) es
aprendiz → arquitecto de datos en salud (RWE); la app es su práctica deliberada
diaria estilo Pólya/Schoenfeld. **Toda selección y generación de problemas debe
servir a ese syllabus.** Claves extraídas (Parte I, pp. 6-23):

- **Bucle por problema**: entender → forcejear con plan (20-30 min, timer
  visible, checkpoint metacognitivo cada ~8 min) → pista una a la vez →
  solución → "mira atrás y destila". La app ya implementa esto; respétalo.
- **Cuaderno de moralejas**: por problema se destila MORALEJA (qué desbloqueó)
  y ★DISPARADOR ("qué señal del problema debía hacerme pensar en esa idea").
  La reflexión post-solución de la app debería evolucionar hacia esta ficha
  (campos moraleja + disparador) — es "el artefacto más importante del plan".
- **Catálogo de heurísticas del PDF** (alinear estrategias internas y futuras
  variantes): caso pequeño → patrón; simetría/WLOG; invariante-monovariante;
  trabajar hacia atrás; caso extremo; palomar; inducción; contradicción;
  casework organizado; pensamiento ilusorio; parametrizar/dibujar.
- **Fuentes graduadas del syllabus** (de dónde curar, en este orden de nivel):
  AoPS Alcumus (entrada) · Zeitz "Art and Craft" (columna vertebral) ·
  AMC 10/12 · Canguro/OMM inicial México · AIME · Engel (por heurística) ·
  Project Euler (puente con ciencia de datos) · OMM/Putnam (destino).
- **Prioridad temática por su carrera**: combinatoria, teoría de números,
  probabilidad, optimización y detección de casos borde — conectan con RWE,
  estadística y matemáticas discretas (clave 0502).
- **Régimen**: punto dulce = fallar ~40-60% (coincide con la zona 30-55% del
  motor adaptativo); dosis 1 problem-block de 30-45 min, 4-5 días/semana;
  piso mínimo en días malos; **nunca dos días seguidos en cero** (la racha de
  la app es la materialización de esa regla).
- Los 3 problemas semilla del PDF (cifra de unidades de 7^2026, tablero
  mutilado, 100 casilleros) ya existen en `problems.json` (ids 35, 21, 34) —
  buena señal de alineación; mantenla al ampliar.

---

## 1. Qué es este proyecto

**Curaduría de Problem Solving General**: web app 100% local de entrenamiento mental
deliberado (HTML + CSS + JavaScript vanilla, sin frameworks, sin backend, sin
dependencias externas). La especificación completa y obligatoria está en
`claude.md` — **léelo antes de tocar código**: define los principios pedagógicos
(Pólya, deliberate practice, desirable difficulties), la regla olímpica de
dificultad (mantener tasa de éxito sin ayuda entre 30% y 50%) y el principio
fundamental: **nunca mostrar al usuario la estrategia/categoría del problema
antes de resolverlo** (la clasificación es solo para el motor adaptativo).

**Decisión de arquitectura (2026-06-10): la app tiene DOS CAMINOS permanentes
e independientes** (acordado explícitamente con el usuario):

1. **Entrenamiento diario** — lo ya construido (§2): un problema al día con el
   bucle completo. Es la práctica de por vida del usuario; NO es una versión
   transitoria que el Modo Estudio vaya a reemplazar. No tocar al construir
   el camino 2.
2. **Modo Estudio / Roadmap** — NUEVO, aún sin código: recorre las fases del
   `Definitivo.pdf` con su bibliografía, evalúa con retrieval y exámenes de
   bloque con interleaving. Diseño completo y protocolo de ingestión en §3.11.

Cada camino tiene **su propia racha** (una no cuenta en la otra) y **ambas
deben ser visibles en todo momento** en el header (refuerzo del hábito; ver
§3.11.3).

## 2. Estado actual: aplicación completa y funcional

Todo lo descrito a continuación ya está implementado y verificado
(JSON validado, `node --check` en todos los módulos).

### Estructura

```text
index.html              UI completa: Sesión, Estudio y Dashboard (+ fresh start,
                        controles de timer, vitrina, avatar, pie de citas)
manifest.webmanifest    PWA: nombre CogitoErgoSum, iconos, theme color
sw.js                   Service worker: precache del shell, offline-first
                        (⚠️ al cambiar cualquier archivo del shell, sube VERSION)
css/styles.css          "La biblioteca" (HANDOFFCES §1): piedra volcánica +
                        luz de lámpara, EB Garamond local, tokens documentados
assets/fonts/           EB Garamond woff2 (OFL, subset latin, servida local)
assets/icons/           Icono SVG + PNG 512/192/180 (generados localmente)
js/app.js               Orquestador: flujo diario, selección, vistas, fresh start,
                        timer UI, citas, registro del SW
js/storage.js           Única capa de acceso a LocalStorage (prefijo cps_)
js/timer.js             Timer §2.6: pausable, 20-120 min, tiempo EFECTIVO,
                        extensión en caliente; persiste al recargar
js/hintSystem.js        5 niveles secuenciales de pistas, −8 pts por pista
js/adaptiveEngine.js    Dificultad dinámica 1-5, ventana de 8 sesiones, zona 30-55%
js/spacedRepetition.js  Intervalos 3/7/14/30 días para problemas débiles
js/analytics.js         Dashboard cognitivo SVG + ratingPorEstrategia() (§2.5)
js/aiMentor.js          Mentor socrático con API de Claude (opcional) + multi-cuenta
js/problemFactory.js    Variantes isomórficas con IA (structured outputs, opcional)
js/study.js             Camino 2: Modo Estudio (roadmap, quiz, examen del motor, racha 📘)
js/badges.js            Sellos de la biblioteca (§2.1): evaluadores + vitrina + revelado
js/avatar.js            "El pensador" (§2.3): avatar SVG por capas ganadas
js/api.js               Puerta única al backend Supabase (auth+REST sin SDK;
                        URL y anon key como constantes; cambiar de backend =
                        reemplazar solo este archivo)
js/sync.js              Sincronización offline-first: outbox, snapshot,
                        adoptar/unir multi-dispositivo, recomputo de rachas
js/claustro.js          Fase D: amistades, vitrina, reconocimiento ❧
supabase/schema.sql     DDL Fase C (events/snapshots/keepalive + RLS) — APLICADO
supabase/schema-fase-d.sql  DDL claustro (perfiles/amistades/invitaciones/
                        reconocimientos + RLS por amistad) — APLICADO
.github/workflows/keepalive.yml  Cron keep-alive de Supabase (cada 2 días)
data/problems.json      100 problemas curados (25 por estrategia)
data/study.json         Syllabus + bancos del Modo Estudio (Fases 0-3 sembradas)
data/quotes.json        Citas curadas (16, con autor) para el pie de la app
data/badges.json        Metadatos de los 21 sellos + mapa heurística→tags
data/avatar.json        Mapa requisito→capa del avatar
Biblioteca/             PDFs del usuario + .txt convertidos (materia prima de ingestión)
claude.md               Especificación del proyecto (fuente de verdad)
HANDOFFCES.md           Extensión 2026-06-11: Constitución, motivación, multi-usuario
```

### Mecánicas clave implementadas

- **Un problema al día**: `app.js → asegurarAsignacionDelDia()` crea una
  `asignacion` en LocalStorage por fecha. Una asignación incompleta de días
  anteriores se conserva (continuidad). **Esto es lo que el siguiente paso debe
  flexibilizar** (ver §3.1).
- **Gating de la solución**: bloqueada hasta cumplir TRES condiciones —
  agotar el temporizador (timestamp persistido, no contador; desde 2026-06-11
  la duración es configurable 20-120 min con pausa/reanudar y extensión +10,
  ver HANDOFFCES §2.6 — el tiempo que cuenta es el EFECTIVO, las pausas lo
  congelan y un desbloqueo ganado no se revoca) + desconstrucción de mínimo
  200 caracteres (autoguardado con debounce) + **predicción de jugada**
  (el usuario marca qué cree que pedía el problema; ver §3.6).
- **Checkpoints metacognitivos (Schoenfeld)**: al ~40% y ~80% del forcejeo
  (con 20 min: a los 8 y 16, la pauta del PDF) aparece un aviso de 2 min en
  la tarjeta del temporizador ("¿este camino está funcionando? ¿cuál es mi
  plan ahora mismo?"). Derivado del tiempo EFECTIVO transcurrido — sobrevive
  recargas y las pausas no lo saltan. Al cumplirse el timer sin revelar, la
  etiqueta invita a la pausa de incubación (PDF §2 paso 3).
- **Campos nuevos del historial (2026-06-11)**: cada sesión cerrada guarda
  además `desconstruccionLen`, `duracionMin`, `pausas`, `msPausado`,
  `incubada` (cerrada en día posterior al inicio) y `revisionDe` — alimentan
  los sellos (badges.js) y el Dashboard, jamás penalizan. Las sesiones
  antiguas no los tienen: todo el código los lee con `?? defaults`.
- **Ficha de moralejas obligatoria**: cerrar sesión exige ★MORALEJA y
  ★DISPARADOR (mín. 15 chars c/u, en `completarSesion`). Van al `historial`
  junto a `prediccion` y `esRevision`; comparación y transferencia siguen
  siendo opcionales (el campo "¿qué aprendí?" se fusionó con la moraleja).
  El Dashboard tiene la vista "Cuaderno de moralejas" + contador de fichas
  completas (el termómetro del PDF §11).
- **Piso mínimo de racha** (PDF §10 "nunca dos días seguidos en cero"):
  si hoy no hay sesión cerrada y existe historial, aparece una invitación
  discreta al final de la vista Sesión. Es un recall de ≥80 chars de una ficha
  pasada (prioriza sesiones débiles); al cerrarlo conserva la racha
  (`perfil.ultimaSesion`/`racha`), enseña la ficha original como
  autocomparación y se registra en `cps_pisosMinimos`. NO toca historial ni
  motor adaptativo.
- **Selección de problema** (`seleccionarProblema()` en app.js): prioridad a
  revisiones espaciadas vencidas → filtro por rango de dificultad adaptativa
  (centro ±1) → interleaving (nunca la misma estrategia que la sesión anterior)
  → relajación progresiva de filtros si el conjunto queda vacío.
- **Score**: base por autoevaluación (resuelto 100 / parcial 60 / fallado 25)
  − 8 × hints + bono 5 si la desconstrucción ≥ 400 chars (`adaptiveEngine.calcularScore`).
- **Repetición espaciada**: un problema entra al ciclo si score < 50, autoevaluación
  fallida o 3+ hints. Revisión exitosa avanza etapa; débil reinicia.
- **Mentor IA**: `aiMentor.js` usa `fetch` directo a `https://api.anthropic.com/v1/messages`
  con modelo **`claude-opus-4-8`**, `thinking: {type: "adaptive"}`, header
  `anthropic-dangerous-direct-browser-access: true`. Prompt de sistema socrático
  estricto (jamás revela la solución; calibra la pista al nivel 1-5). Si no hay
  API key configurada o la llamada falla, el sistema cae silenciosamente a los
  hints estáticos curados del JSON. La key se guarda en LocalStorage
  (`cps_mentorIA`) y se configura desde el Dashboard.

### Cómo ejecutar y validar

```sh
cd /Users/EdgarDevice/Desktop/ProyectoX
python3 -m http.server 8000        # módulos ES6 exigen HTTP, no file://
# abrir http://localhost:8000

# Validaciones rápidas tras cualquier cambio:
python3 -c "import json; d=json.load(open('data/problems.json')); print(len(d['problemas']))"
for f in js/*.js; do node --check "$f"; done
```

### Esquema de un problema en `problems.json`

```json
{
  "id": 1,
  "titulo": "", "estrategia": "inversion|optimizacion|invariantes|patrones",
  "dificultad": 1, "enunciado": "",
  "hints": ["nivel1","nivel2","nivel3","nivel4","nivel5"],
  "solucion": "", "explicacion": "", "tiempo_estimado": 20,
  "conceptos": [], "transferencias": [],
  "source": "", "source_url": "", "year": "", "tags": []
}
```

Los 5 hints son obligatorios y siguen la escala: 1 redirigir atención,
2 señalar estructura, 3 reducir espacio de búsqueda, 4 sugerir estrategia,
5 casi revelar el camino. Todo en español, tono socrático.

---

## 3. Plan de continuación

> **⭐ El siguiente gran paso es el Modo Estudio — lee §3.11 antes que nada.**
> Los §3.1–3.8 documentan lo ya hecho; §3.9 son mejoras menores del camino 1.

### ✅ 3.1 Más de un problema al día (HECHO, 2026-06-10)

Implementado: botón "Entrenar otro problema" en la pantalla de resultado
(`app.js → entrenarOtroProblema()` + `resetearVistaSesion()`). Cada sesión
completada se archiva en `cps_sesionesArchivadas` (con su score) para no
perder trazabilidad al sobrescribir `asignacion`. La racha sigue contando
por día y el interleaving/motor adaptativo funcionan entre sesiones del
mismo día (leen de `historial`). De paso se corrigió un bug: recargar la
página tras completar la sesión creaba una asignación nueva en silencio;
ahora la asignación completada de hoy se conserva hasta que el usuario pida
otro problema (o llegue el día siguiente).

### ✅ 3.2 Base ampliada a 100 problemas (HECHO, 2026-06-10)

`data/problems.json` tiene ahora 100 problemas (ids 1-100), 25 por estrategia.
Distribución de dificultad: 7/22/34/24/13 (antes los niveles 4-5 escaseaban).
Los 60 nuevos cubren el catálogo de heurísticas del PDF vía `tags`
(caso-pequeno, simetria, invariante, monovariante, hacia-atras, caso-extremo,
palomar, induccion, contradiccion, casework, pensamiento-ilusorio,
parametrizar, dibujar), los temas prioritarios de carrera (combinatoria,
teoría de números, probabilidad, optimización, Fermi aplicado a datos de
salud) y la graduación del syllabus vía tags `nivel-entrada` /
`nivel-medio` / `nivel-alto`. Enunciados propios; `source` registra la
inspiración (Engel, Zeitz, AMC/AIME, Project Euler, clásicos).

### ✅ 3.3 Generador de variantes isomórficas (HECHO, 2026-06-10)

`js/problemFactory.js` implementado según el diseño previsto: extrae la
estructura cognitiva de una semilla curada y genera una variante con contexto
distinto vía `claude-opus-4-8` + structured outputs
(`output_config.format json_schema`, compatible con `thinking: adaptive`).
Valida 5 hints exactos, hereda `estrategia`/`dificultad`/`tiempo_estimado`
de la semilla, marca `origen: "generado"` y `semilla_id`, guarda en
`cps_problemasGenerados` y maneja `refusal`/`max_tokens`/errores de red con
fallback silencioso. Lee la cuenta activa SOLO vía `cuentaActiva()` de
`aiMentor.js`. `app.js` fusiona generados + estáticos en el pool al arrancar
y expone en el Dashboard la tarjeta "Generador de variantes" (botón +
contador); la semilla se elige priorizando problemas débiles del historial
(solo semillas curadas, nunca variantes de variantes) y jamás se revela.

### ✅ 3.4 Ficha de moralejas (HECHO, 2026-06-10)

La reflexión post-solución ahora ES la ficha del PDF §3: ★MORALEJA ("¿qué
aprendiste? en una frase, qué desbloqueó el problema") y ★DISPARADOR ("¿qué
señal del enunciado debía hacerte pensar en esa idea?") son obligatorias para
cerrar; "comparación" absorbió "qué intenté / dónde me atasqué" y
"transferencia" sigue igual. Dashboard: tarjeta "Cuaderno de moralejas"
(fichas de la más reciente a la más antigua, con título del problema, chip de
estrategia y fecha) + stat "Fichas con disparador".

### ✅ 3.5 Repaso por variantes, estilo Chessable (HECHO, 2026-06-10)

`app.js → resolverProblemaDeRevision()`: cuando una revisión vence y hay
cuenta IA, se presenta una variante isomórfica NO trabajada de esa semilla si
ya existe; si no existe, se usa el original hoy y se dispara
`Factory.generarVariante(semilla)` en segundo plano (fire-and-forget, jamás
bloquea el arranque) para que la PRÓXIMA revisión sí tenga variante. Si lo
vencido es una variante, la familia es la de su semilla curada (nunca
variantes de variantes). La asignación guarda `revisionDe` y
`completarSesion` registra el resultado de la repetición espaciada contra el
problema ORIGINAL (la variante es solo el vehículo). En revisiones, la guía
de desconstrucción añade: "¿qué señal reconoces y qué moraleja de tu cuaderno
aplica?".

### ✅ 3.6 Predicción de jugada + estrategia revelada al cerrar (HECHO, 2026-06-10)

Implementa el "examen del motor" del PDF §8b (test de reconocimiento de
disparadores) + el momento Lichess del benchmark §4: antes de revelar la
solución el usuario debe marcar qué cree que pedía el problema (radios con
descripciones neutras: "pensar hacia atrás", "algo que se conserva"…, o "aún
no lo veo"; nunca se nombra la etiqueta del problema actual). Al cerrar la
sesión, la pantalla de resultado revela "Esto era **Invariantes** — detectar
lo que permanece constante…" y el veredicto de la predicción. Dashboard:
stat "Disparadores reconocidos" (% de predicciones correctas — la métrica de
oro del PDF: "cuántos disparadores reconoces en frío"). La predicción vive en
`asignacion.prediccion` y se copia al historial.

### ✅ 3.7 Checkpoints metacognitivos + incubación (HECHO, 2026-06-10)

Ver §2 "Mecánicas clave". Constantes en `app.js → CHECKPOINTS` (8-10 min y
16-18 min, texto de Schoenfeld del PDF §2).

### ✅ 3.8 Piso mínimo de racha (HECHO, 2026-06-10)

Ver §2 "Mecánicas clave". Funciones `abrirPisoMinimo()` /
`completarPisoMinimo()` en app.js; registro en `cps_pisosMinimos`.

### 3.9 Mejoras menores del camino 1 (no iniciadas, MENOR prioridad que §3.11)

1. **FSRS simplificado** cuando haya historial suficiente (sustituir los
   intervalos fijos de `spacedRepetition.js` por estabilidad/dificultad por
   ítem, estilo Anki).
2. **Rating por heurística (estilo Alcumus)**: evolucionar la dificultad
   global 1-5 hacia un nivel por estrategia; el historial ya guarda
   estrategia + score + prediccion por sesión.
3. **Modo "reintenta tus fallos"** (Lichess): lista de problemas fallados
   reintentables en frío, separada del ciclo espaciado.
4. ~~Profundizar `evaluarDesconstruccion()`~~ — SUPERADO (2026-06-11): el
   chat socrático (§4.4 de HANDOFFCES, ya implementado) cubre este caso y
   más: el mentor lee la desconstrucción como contexto en cada turno.
   `evaluarDesconstruccion()` queda en aiMentor.js como utilidad disponible.

### ⚠️ 3.10 Requisito transversal: cambio de cuenta de Claude (YA IMPLEMENTADO)

El usuario tiene varias cuentas de Anthropic y alternará entre ellas (la actual
será cancelada en algún momento). `aiMentor.js` ya incluye un **gestor
multi-cuenta**: el usuario registra cuentas (nombre + API key) en el Dashboard,
elige cuál está activa con un radio button y puede eliminarlas. Formato en
LocalStorage (`cps_mentorIA`): `{ cuentas: [{id, nombre, apiKey}], activa: id }`
(con migración automática desde el formato antiguo de una sola key).

Reglas para módulos nuevos (problemFactory incluido):

- Nada de keys hardcodeadas. Leer SIEMPRE la cuenta activa vía
  `cuentaActiva()` / `mentorDisponible()` exportadas por `aiMentor.js`
  (única fuente de verdad; idealmente reutilizar su helper de fetch).
- El progreso y los problemas generados viven en LocalStorage y NO dependen
  de la cuenta: cambiar/eliminar cuentas no debe borrar nada.

### 🧭 3.11 MODO ESTUDIO — la nueva dirección (decidida 2026-06-10, cero código)

El usuario quiere recorrer la bibliografía del roadmap de `Definitivo.pdf`
DENTRO de la app, como segundo camino independiente del entrenamiento diario.
El diseño ya está acordado con él; lo que sigue es construirlo.

#### 3.11.1 Principio rector: lectura dirigida, NO lecciones en-app

La app NO contiene lecciones legibles. El PDF lo advierte ("la gente lee
soluciones y siente que aprende — no aprende, reconoce"; "Zeitz es una
cantera, no una carrera") y `claude.md` excluye el modelo Brilliant/Khan.
En su lugar:

1. **La app dice qué leer y cuánto** según la fase del usuario: puntero a
   libro + capítulo + páginas, con la dosis del PDF ("~6-8 pp de concepto O
   1-2 problemas, no las dos cosas a tope"). La lectura ocurre en el libro.
2. **Al volver, evaluación por retrieval de generación**: preguntas
   retadoras y acertijos del capítulo — "¿qué heurística aplica y por qué?",
   encuentra-el-error-en-esta-solución, quizzes de disparador, Fermi. El
   destilado/feedback aparece SOLO después de responder (struggle first).
3. **Problemas del libro entran al bucle completo del camino 1** (timer,
   desconstrucción, predicción, ficha): reutilizar la maquinaria existente,
   no construir una segunda máquina de práctica.
4. **Acceso libre (desde 2026-06-12)**: todas las unidades y lecciones están
   accesibles sin candado (`unidadDisponible()` devuelve siempre `true`).
   El progreso oficial (racha, resumen, `bloqueActual()`) sigue anclado al
   primer bloque sin examen aprobado. El selector `estudio-bloque-selector`
   permite saltar a cualquier bloque desde la UI sin alterar ese ancla.

#### 3.11.2 Examen de bloque = "examen del motor" del PDF §8b

Al cerrar cada bloque, examen acumulativo CON INTERLEAVING: mezcla aleatoria
de TODO lo avanzado hasta ese punto (no solo lo recién visto), con peso extra
en heurísticas débiles (el historial ya tiene esos datos). Formato del PDF:
set de problemas no vistos + predicción de jugada antes de atacar +
disparador correcto después. Criterio de aprobado del PDF: predicción
coincide en ≥3 de 5, y por cada problema fallado el disparador queda
correctamente identificado. La mecánica de predicción ya existe en el camino
1 (§3.6) — reutilizarla.

#### 3.11.3 Rachas: separadas y siempre visibles (pedido explícito del usuario)

- **Racha de entrenamiento** (existente, `perfil.racha`) y **racha de
  estudio** (nueva) son INDEPENDIENTES: completar una NO cuenta para la otra.
- **Ambas visibles en todo momento** en el header de la app (no solo en el
  Dashboard): el usuario quiere ver sus días consecutivos mientras navega
  (refuerzo del hábito). Mantener la sobriedad visual — contador discreto,
  no confeti.
- El piso mínimo existente (§3.8) pertenece SOLO a la racha de entrenamiento.
  Si el estudio necesita su propio piso, decidirlo después con el usuario.

#### 3.11.4 Arquitectura acordada

- **Infraestructura compartida, progreso separado**: el Modo Estudio reutiliza
  `storage.js`, el cuaderno de moralejas y la repetición espaciada, pero su
  avance vive aparte (p. ej. `cps_estudio`) y NO afecta la dificultad
  adaptativa del camino 1, ni al revés.
- **Navegación de tres pestañas**: Entrenamiento · Estudio · Dashboard
  (el Dashboard muestra ambos progresos).
- **Bancos estáticos primero**: el Modo Estudio funciona completo sin IA.
  Con cuenta activa, el mentor puede generar preguntas/variantes frescas
  encima (vía `cuentaActiva()`, regla §3.10).
- Esbozo de datos (ajustable por quien lo implemente):

```json
// data/estudio.json — mapa del syllabus + bancos por unidad
{
  "unidades": [{
    "id": "zeitz-1", "fase": 0, "orden": 2,
    "libro": "Zeitz — The Art and Craft of Problem Solving",
    "capitulo": "1", "paginas": "1-12",
    "dosis": "1 sección (~6-10 pp) + 2-3 problemas con bucle completo",
    "heuristicas": ["caso-pequeno", "patron"],
    "ideas_clave": ["3-5 líneas; solo se muestran DESPUÉS del quiz"],
    "banco": [ { "tipo": "quiz|acertijo|encuentra-error|disparador",
                 "...": "mismo esquema que problems.json (5 hints, solucion, explicacion)" } ]
  }],
  "bloques": [{ "id": "fase-0", "unidades": ["polya-1", "zeitz-1", "zeitz-2"] }]
}
```

#### 3.11.5 Pipeline de contenido (protocolo de ingestión incremental)

La carga de bibliografía es INCREMENTAL por diseño — nunca ingerir libros
completos en una sesión, y NUNCA copiar texto íntegro de los libros a la app
(copyright + pedagogía: la app debe obligar a volver al libro; solo
destilados de 3-5 líneas, punteros de lectura y preguntas propias).

- **Paso 0 (usuario, pendiente)**: convertir sus PDFs a texto plano:
  `brew install poppler && pdftotext -layout libro.pdf libro.txt`.
  Orden: Pólya (How to Solve It) y Zeitz caps. 1-4 primero (= Fase 0-1);
  después AMC/Engel según fase. **Sin estos textos no se puede sembrar
  contenido real; el esqueleto sí puede construirse antes.**
- **Paso 1 (una sesión de agente)**: construir el esqueleto completo —
  vista Estudio, `data/estudio.json`, motor de quiz con gating, examen de
  bloque, desbloqueo por progreso, racha de estudio + header con ambas
  rachas. Sembrar con Fase 0 si ya hay textos.
- **Pasos 2…N (una sesión por tanda)**: destilar capítulo a capítulo en el
  orden del syllabus, generando SOLO archivos de datos (cero cambios de
  código). Al final de cada sesión, registrar aquí qué unidades quedaron
  ingeridas y cuál sigue.

#### 3.11.6 Estado actual y qué falta (actualizado 2026-06-10, noche)

**EL ESQUELETO DEL MODO ESTUDIO YA ESTÁ CONSTRUIDO Y SEMBRADO CON LA FASE 0.**
Lo implementado en esta sesión (todo verificado: `node --check` en los 10
módulos, JSON validado, cruce de IDs HTML↔JS en ambas direcciones):

| Pieza | Estado |
|---|---|
| Camino 1 (entrenamiento diario completo, §2-§3.8) | ✅ Hecho y verificado |
| Biblioteca convertida a texto plano | ✅ 51 PDFs → 51 .txt en `Biblioteca/` (incluye libros de Partes II-III del PDF para futuro) |
| Header con ambas rachas siempre visibles | ✅ `#header-rachas`, chips 🔥 (práctica) y 📘 (estudio); se actualiza al cerrar sesión, piso, unidad o examen |
| Racha de estudio separada | ✅ En `cps_estudio.rachaEstudio`; rompe-racha al arrancar (`actualizarRachaEstudio`), nunca se cruza con `perfil.racha` |
| Esqueleto del Modo Estudio | ✅ `js/study.js` + pestaña Estudio + `data/study.json`; ver detalle abajo |
| Contenido Fase 0 | ✅ 5 unidades (Pólya×2, Zeitz×3), 22 preguntas de retrieval, examen de 6 ítems |
| Contenido Fase 1 | ✅ 6 unidades (Zeitz §2.3, §2.4, §3.1, §3.2, §3.3, §3.4), 24 preguntas, examen de 6 ítems |
| Contenido Fase 2 (2026-06-10, madrugada) | ✅ 7 unidades (Zeitz §4.1 grafos, §6.1-§6.3 conteo, §7.1-§7.2 números + Engel cap. 5 como cantera), 30 preguntas, examen de 7 ítems (5 AMC 10A 2019 adaptados con source/url/year + Engel E6 + Königsberg) |
| Contenido Fase 3 (2026-06-10, madrugada) | ✅ 6 unidades (Zeitz §6.4 recurrencias, §4.3 generatrices, §7.3 funciones aritméticas, §7.4 diofánticas, §7.5 ejemplos instructivos + Engel cap. 6 como cantera), 28 preguntas, examen de 6 ítems (AMC 10A 2018 P4/P19, AMC 10B 2019 P6/P14/P25 + Sophie Germain; todas las respuestas verificadas por fuerza bruta en Python). Pool acumulado de examen: 25 ítems |
| Contenido Fase 4 (2026-06-11, tarde) | ✅ 5 unidades (Zeitz §5.2 factor tactic, §5.3 telescopio, §5.4 polinomios/Vieta, §5.5 desigualdades AM-GM/massage/Cauchy + Engel cap. 7 como cantera), 25 preguntas, examen de 7 ítems TODOS de probabilidad AMC (10B 2017 P9; 10A 2017 P15, P18; 10B 2018 P6, P9; 10B 2019 P17; 10A 2019 P20 — espejos ZIML 2017/2018/2019 10A+10B descargados y convertidos; respuestas verificadas por fuerza bruta/derivación en Python). Pool acumulado de examen: 32 ítems |
| Contenido Fase 5 (2026-06-11, noche) | ✅ 9 unidades — "métele todo" pedido por el usuario: Zeitz §4.2 complejos, §8.2-§8.4 geometría de supervivencia completa, cap. 9 (convergencia + matemática euleriana) y Engel por heurística (cap. 1 invariancia, cap. 2 coloraciones, cap. 3 extremal, cap. 13 juegos) — 45 preguntas, examen de 8 ítems nivel AMC 12 (12A 2017 P17/P19, 12A 2018 P17, 12A 2019 P14, 12B 2019 P17/P20 + Bachet y tetrominós 1×4 de Engel; espejos ZIML AMC12 2017-2019 A/B descargados; TODAS las respuestas verificadas por cómputo en Python, incl. coloración (i+j) mod 4 con censo 25/26/25/24 y W/L de Bachet hasta 100). Pool acumulado: 40 ítems |
| Tarjeta "Modo Estudio" en Dashboard | ✅ Bloque actual, unidades x/y, examen, racha |
| Ingestión Fase 6+ | ❌ SIGUIENTE PASO — ver protocolo abajo |
| Refinamientos del Modo Estudio | ❌ Ver lista al final |

**Cómo funciona lo construido** (`js/study.js`, contenido en `data/study.json`,
progreso en `cps_estudio` — esquema documentado en `storage.js`):

- **Camino**: la pestaña Estudio muestra el bloque actual con sus unidades en
  orden (✓ hecha / ▸ abierta). Todas las unidades son accesibles; el examen
  se muestra al completar las unidades del bloque visible.
- **Unidad**: tarjeta de lectura dirigida (libro/lectura/dosis/"al leer,
  busca") → botón "Ya leí — evalúame" → quiz de retrieval pregunta por
  pregunta: el usuario responde por escrito (mín. 40 chars) ANTES de ver la
  respuesta esperada, y se autoevalúa (lo tenía / a medias / no lo tenía).
  Las `ideas_clave` (destilado del capítulo) se muestran SOLO al terminar.
  El quiz en curso persiste (`quizEnCurso`) y se retoma tras recargar.
- **Examen del bloque** (`muestrearExamen`): pool acumulativo de ítems de
  examen de todos los bloques hasta el actual, barajado evitando dos
  heurísticas iguales consecutivas (interleaving); muestrea 5. Por ítem:
  predicción de jugada (radios del `catalogoHeuristicas`, 12 entradas del
  catálogo del PDF §4 + penúltimo paso) → forcejeo con UNA pista opcional →
  autoreporte (resuelto solo / con pista / no resuelto) → revelado con
  solución + ★disparador → "¿identificaste la señal?". Aprobado (PDF §8b):
  predicciones correctas ≥3/5 Y todo fallado con disparador identificado.
  Reintentos permitidos (remuestrea); `intentos` queda registrado.
- **Aprobar el examen abre el siguiente bloque** (`bloqueAprobado` →
  `indiceBloqueActual`). Existen `fase-0` a `fase-3`; añadir un bloque
  nuevo a `study.json` basta para que el desbloqueo funcione solo.

**Protocolo de ingestión para el siguiente agente (Pasos 2…N):**

1. Los textos están en `Biblioteca/*.txt` (¡no leas libros enteros! usa
   grep/offsets para ubicar capítulos). Anclas ya verificadas: Zeitz cap. 1
   pp. 1-11, §2.1 pp. 12-23, §2.2 pp. 23-37, §2.3 pp. 37-49, §2.4 pp. 49-58,
   cap. 3 (tácticas: simetría 59, extremo 70, palomar 80) — TOC en líneas
   430-470 del .txt. Pólya: cuatro fases pp. 28-36, diccionario pp. 58+.
2. Para cada tanda: añadir unidades a `data/study.json` (mismo esquema que
   las existentes: lectura/dosis/objetivo/ideas_clave/banco de 4-5 preguntas
   tipo quiz|acertijo|encuentra-error|disparador) y, si abre bloque nuevo,
   su entrada en `bloques` con `examen.items` (≥6, con heuristica del
   catálogo, pista única, solucion, disparador). CERO cambios de código.
3. Orden del syllabus (PDF §7) y estado: ✅ Fase 0 (Pólya + Zeitz 1-2.2),
   ✅ Fase 1 (Zeitz §2.3-§3.4), ✅ Fase 2 (Zeitz §4.1 + §6.1-§6.3 +
   §7.1-§7.2, Engel cap. 5, 5 AMC), ✅ Fase 3 (Zeitz §6.4 + §4.3 +
   §7.3-§7.5, Engel cap. 6, 5 AMC), ✅ Fase 4 (2026-06-11: Zeitz
   §5.2-§5.5 álgebra completa + Engel cap. 7 desigualdades, examen 100%
   probabilidad AMC — 7 ítems verificados) y ✅ Fase 5 (2026-06-11, noche:
   Zeitz §4.2 + cap. 8 completo + cap. 9, Engel caps. 1/2/3/13, examen
   AMC 12 + Engel — 8 ítems verificados). **Con esto, de Zeitz solo queda
   §8.5 (transformaciones) como sección sustantiva; la fase 6 natural es
   subir a AIME y/o Engel caps. restantes (8 inducción, 9 sucesiones,
   10 polinomios, 11 funcionales, 12 geometría, 14 estrategias) — decidir
   con el usuario.** Anclas Zeitz verificadas en el .txt: §4.2 línea 7190
   (De Moivre 7373), §8.2 línea 15797 (fantasma 16043, inscrito 16157),
   §8.3 línea 16487 (semejantes 16675, altura-hipotenusa 16736), §8.4
   línea 17171 (checklist 17179, concíclicos 17215, cevianas 17386), §9.2
   línea 19154 (seis vías 19190), §9.4 línea 20690 (euleriana 20958);
   §5.2 línea 9076 (factor tactic 9147), §5.3 línea 9650 (telescopio
   9731), §5.4 línea 10142 (ceros 10213, Vieta 10364), §5.5 línea 10708
   (AM-GM 10878, massage/Cauchy 11138); §4.3 línea 7980, §6.4 línea
   13221, §7.1 línea 13733, §7.2 línea 14170, §7.3 línea 14445, §7.4
   línea 14807; TOC completo en líneas 430-620. Anclas Engel: cap. 1
   línea 237 (E2 paridad 290, monovariante E4 304), cap. 2 línea 1374
   (mutilado 1382, problemas 1400+), cap. 3 línea 1956 (receta 1971,
   E1 1996), cap. 13 línea 18838 (W/L 18854, Bachet 18876), cap. 5 línea
   4117, cap. 6 línea 5833, cap. 7 línea 7935 (cadena de medias 7965,
   Nesbitt 8058).
4. **Exámenes AMC/AIME: obtenerlos de la web** (decisión del usuario,
   2026-06-10). ⚠️ El wiki de AoPS y isinj.com BLOQUEAN el fetch directo
   (Cloudflare 403); web.archive.org tampoco está disponible. Lo que SÍ
   funciona (verificado 2026-06-10): PDFs de espejo vía `curl -A "Mozilla/5.0..."`
   — `ziml.areteem.org/zimlresources/AMC10/ZIML_Download_<año>_AMC_10A.pdf`
   (≈la mitad de los problemas de cada examen) y
   `ivyleaguecenter.org/wp-content/uploads/...` (examen completo); convertir
   con `pdftotext -layout` y verificar la respuesta DERIVÁNDOLA (los espejos
   no traen soluciones fiables). Protocolo: ADAPTAR al español con enunciado
   propio (no volcar bancos completos: curar 3-6 problemas por tanda, los
   que sirvan a la unidad o al examen del bloque), y registrar siempre
   `source` ("AMC 10A 2019 P4"), `source_url` (la URL canónica del wiki de
   AoPS aunque no sea fetchable) y `year`. Los problemas AMC también pueden
   ir al pool del camino 1 (problems.json) con su estrategia/dificultad
   interna, no solo al Modo Estudio. Curados hasta ahora (todos al examen
   de su bloque, respuestas derivadas y verificadas): fase-2 → AMC 10A 2019
   P2, P4, P18, P19, P20; fase-3 → AMC 10A 2018 P4, P19 y AMC 10B 2019 P6,
   P14, P25; fase-4 (probabilidad) → AMC 10B 2017 P9, 10A 2017 P15 y P18,
   10B 2018 P6 y P9, 10B 2019 P17, 10A 2019 P20; fase-5 (AMC 12) →
   12A 2017 P17 y P19, 12A 2018 P17, 12A 2019 P14, 12B 2019 P17 y P20.
   Espejos ZIML ya descargados en /tmp (se pierden al reiniciar;
   re-descargar con el mismo patrón de URL, también existe
   `/zimlresources/AMC12/ZIML_Download_<año>_AMC_12<A|B>.pdf`):
   2017/2018/2019, 10A/10B y 12A/12B.
   Nota: los PDF de ZIML traen solo ~la mitad de los problemas de cada
   examen; verificar SIEMPRE la respuesta derivándola o por fuerza bruta
   en Python antes de publicarla en study.json.
5. NUNCA copiar texto íntegro de los libros: solo punteros, destilados de
   3-5 líneas y preguntas propias. Validar siempre:
   `python3 -c "import json; json.load(open('data/study.json'))"` y
   `for f in js/*.js; do node --check $f; done`.
6. **Campos del esquema actualizados (2026-06-12)**: `metadata.ruta` acepta
   `'quant'|'maang'|'health-ai-rwe'|'ml-systems'`; la heurística `skew-drift`
   existe en `catalogoHeuristicas`. Los ítems de examen de `fase-7` usan
   `pistas[]` (array de 5 strings), no el campo `pista` (string) de fases
   anteriores. `examenEnCurso.registros[]` guarda `confianza: 1-5` (1=adivinando,
   5=lo veo claro). `examenEnCurso` almacena `bloqueId` para que `contextoEntrevista()`
   pueda detectar si el examen activo es de `fase-7`.

**Refinamientos pendientes del Modo Estudio (menores, en orden de valor):**

1. Las preguntas falladas ("no lo tenía") no entran aún a repetición
   espaciada — integrarlas a `spacedRepetition.js` o a un repaso propio.
2. El examen no tiene timer (el PDF sugiere 90 min para Fase 0); valorar
   timer visible reutilizando `timer.js`.
3. ✅ (HECHO 2026-06-10) Respuesta parcial del quiz se autoguarda con
   debounce en `quizEnCurso.respuestaParcial` y se restaura al recargar.
   El textarea de forcejeo del EXAMEN sigue siendo efímero — pendiente.
4. Piso mínimo de estudio (¿una pregunta de repaso conserva la racha 📘?)
   — decidirlo con el usuario.
5. Los problemas sugeridos en `dosis` ("+ 2-3 problemas del libro") aún no
   se materializan como sesiones del camino 1; idea: botón "entrenar un
   problema de esta unidad" que cree una asignación etiquetada.

---

## 4. Benchmarks de inspiración — qué tomar de cada plataforma

Ninguna app existente hace el sistema completo (esa es nuestra ventaja:
desconstrucción obligatoria, moraleja + disparador, variantes isomórficas).
Pero estas resuelven muy bien piezas individuales; al implementar §3, tomar:

| Plataforma | Qué hace bien | Cómo incorporarlo aquí |
|---|---|---|
| **AoPS Alcumus** | Rating fino por problema calibrado con datos + mastery por tema | Evolucionar la dificultad 1-5 hacia un rating continuo por problema y un nivel por heurística (no solo global). El historial del usuario ya da los datos. |
| **Lichess Puzzles** | Temas ocultos hasta resolver; rating Glicko adaptativo; reintentar fallos | Valida nuestro principio de no-etiquetas. Tras revelar la solución, mostrar la estrategia/heurística como momento de aprendizaje explícito ("esto era un invariante"). Añadir modo "reintenta tus fallos". |
| **Chessable (MoveTrainer)** | Repite *ideas*, no partidas enteras | **La mejora prioritaria para 3.3**: en repasos espaciados, en vez de repetir el problema completo, mostrar una variante isomórfica nueva (de problemFactory) y preguntar "¿qué señal ves?" — entrena directamente el DISPARADOR del cuaderno de moralejas (Definitivo.pdf §3). |
| **Math Academy** | SRS integrada al currículo, no como módulo aparte; interleaving automático | Que el repaso espaciado cuente como la sesión del día (no tarea extra) y que un solo problema bien elegido repase varias moralejas a la vez. |
| **Project Euler** | Acceso a la discusión solo al resolver; progresión por desbloqueo | Ya tenemos el gating; reforzar la sensación de "ganarte" la explicación y las transferencias. |
| **Anki (FSRS)** | Algoritmo de repetición espaciada ajustado al desempeño real | Cuando haya historial suficiente, sustituir los intervalos fijos 3/7/14/30 de `spacedRepetition.js` por un FSRS simplificado (estabilidad/dificultad por ítem). |
| **Exercism** | Mentoría socrática sobre la solución del alumno | Tono y formato para el mentor IA: comentar el razonamiento escrito del usuario (su desconstrucción), nunca dar la respuesta. Ya está en el system prompt; profundizar en `evaluarDesconstruccion()`. |
| **Duolingo** | Racha con piso mínimo (streak freeze) | Materializa "nunca dos días seguidos en cero": ofrecer un "piso mínimo" en días malos (una variante corta o un quiz de disparador) que conserve la racha. Evitar su estética gamificada — la UI debe seguir siendo sobria. |

Anti-modelos (qué NO copiar): Brilliant y Khan Academy — exceso de andamiaje,
respuesta demasiado accesible, cero forcejeo productivo (claude.md los excluye
explícitamente).

---

## 5. Convenciones del proyecto

- Todo el código, comentarios y UI en **español**; nombres de archivo en inglés
  según la arquitectura de claude.md.
- ES6 modules; `storage.js` es la única puerta a LocalStorage.
- Sin librerías externas, sin build step, sin npm. Las gráficas son SVG manual.
  (La fuente EB Garamond se sirve LOCAL desde `assets/fonts/` — jamás CDNs.)
- La app debe funcionar completa sin API key (la IA siempre es opcional).
- Modelo de IA: `claude-opus-4-8` (no degradar a modelos menores sin que el
  usuario lo pida).
- **Constitución de HANDOFFCES §0 es LEY**: nada aleatorio ni comprable, el
  fallo nunca castiga (validación-del-proceso + dato + reencuadre), insignias
  reveladas SOLO en pantallas de cierre, todo comparativo es contra el propio
  pasado del usuario. Releer §0.1 antes de cerrar cualquier fase.
- **PWA**: al cambiar cualquier archivo del shell (HTML/CSS/JS/data), subir
  `VERSION` en `sw.js` o el navegador seguirá sirviendo la versión cacheada.
- Verificación mínima tras cualquier cambio: `node --check` en js/*.js y sw.js,
  JSON validados, cruce de IDs HTML↔JS, y probar con red desconectada
  (offline-first es requisito) y con `prefers-reduced-motion`.
- Las API keys de Claude (`cps_mentorIA`) viven SOLO en el dispositivo:
  cuando exista sincronización (Fase C), ese namespace queda EXCLUIDO del
  outbox y del snapshot.
