# PROMPT PARA EL EJECUTOR (Claude Sonnet 4.6) · Sistema de dificultad en Fase 7 Arena

> **Eres un software engineer junior y ejecutor.** El arquitecto ya tomó TODAS
> las decisiones de diseño y, sobre todo, **ya clasificó manualmente las 1619
> preguntas** por dificultad. Tu trabajo es **implementar el código**, no
> re-clasificar nada ni rediseñar. Sigue estas instrucciones al pie de la letra.
> Si algo de la realidad del repo no coincide con lo descrito aquí, **DETENTE y
> reporta** en vez de improvisar.

---

## 0. Contexto obligatorio (léelo antes de tocar código)

Lee, en este orden:

1. **`reformulacion-examenes.md`** — la especificación funcional completa del
   feature (selector de dificultad por lección, examen final de cluster, edge
   cases, reglas de compatibilidad). Es la fuente de verdad del COMPORTAMIENTO.
2. **`data/arena-dificultades.json`** — el **resultado de la clasificación
   manual del arquitecto**. Es tu fuente de verdad de los DATOS. NO la
   modifiques. NO reclasifiques. NO inventes dificultades.
3. **`CLASIFICACION-DIFICULTAD-ARENA.md`** — el reporte legible de esa misma
   clasificación (criterios + desglose por cluster/unidad). Solo lectura.
4. **`HANDOFFCES.md` §0 (Constitución, es LEY)** y la sección de convenciones —
   para no violar reglas del proyecto.

### Reglas duras del proyecto (NO negociables)

- HTML/CSS/JavaScript **vanilla**, ES Modules. **Cero dependencias** nuevas,
  cero frameworks, cero CDNs.
- Todo el texto visible al usuario, en **español**.
- **`js/storage.js` es la única puerta a LocalStorage.** Usa sus helpers
  (`load`, `save`, `update`); no llames a `localStorage` directamente.
- Funciona en **GitHub Pages**, offline-first. No rompas el service worker ni
  el manifest. **No rompas Supabase ni la sincronización.**
- **No borres preguntas, no cambies IDs, no alteres el contenido pedagógico**
  (enunciado/solución/explicación) de ninguna pregunta.
- `node --check` debe pasar en cada `.js` que toques; todo JSON debe quedar
  parseable.
- Al cambiar cualquier archivo del **shell** (incluido `data/study.json`),
  **sube `VERSION` en `sw.js`** (hoy va en `cogitoergosum-v138` → súbela a
  `cogitoergosum-v139`).

---

## 1. Mapa del terreno (ya investigado por el arquitecto — verifícalo, no lo redescubras)

### Dónde viven las preguntas

Las preguntas de la **Fase 7 Arena** viven en **`data/study.json`** →
arreglo `unidades[]`. Cada unidad de Arena tiene `bloque: "fase-7"` y un campo
**`banco[]`** con las preguntas. Hay **118 unidades** `fase-7` y **1619
preguntas** en total.

Esquema actual de una pregunta del banco (ejemplo real):

```json
{
  "id": "arq1-q1",
  "tipo": "quiz",
  "enunciado": "Enuncia el teorema de linealidad de la esperanza...",
  "solucion": "$E[X+Y] = ...$",
  "explicacion": "Si lo demostraste con integrales..."
}
```

> Ninguna pregunta tiene hoy campo de dificultad. Tú se lo vas a agregar
> (Tarea A) usando EXACTAMENTE los valores de `data/arena-dificultades.json`.

### Cómo se agrupan en clusters

`data/entrevista/_taxonomia.json` define los **8 clusters** y, en cada uno, el
arreglo `unidades[]` (ids de unidad `fase-7`) en orden didáctico. La UI del Modo
Estudio ya agrupa las lecciones bajo estos clusters.

### Flujo actual del quiz por lección (en `js/study.js`)

- `renderClustersFase7(container, b)` (≈línea 400) y `crearClusterAcordeon(c, unidades, b)`
  (≈línea 426) pintan los acordeones de cluster con sus lecciones.
- `abrirUnidad(unidadId)` (≈línea 670) abre el panel de una lección. El botón
  **`#btn-quiz-iniciar`** (≈línea 719) arranca el quiz y crea el estado:

  ```js
  st.quizEnCurso = {
    unidadId: u.id,
    preguntasIds: u.banco.map((q) => q.id),  // <-- HOY: TODAS, en orden, sin filtro ni azar
    indice: 0,
    resultados: [],
    esRepaso: false,
  };
  ```

- `renderPreguntaQuiz()` (≈línea 738) pinta la pregunta en el índice actual,
  resolviendo `q = u.banco.find(b => b.id === ids[qc.indice])`.
- `finalizarQuiz()` (≈línea 853) cierra la unidad y guarda resultados.
- La simulación de cluster (`abrirSimCluster`, ≈línea 514) usa los archivos
  `data/entrevista/cluster-*.json` (Nivel E, 4 preguntas guionizadas). **Eso NO
  es el banco** y **NO es** el examen final que pide `reformulacion-examenes.md`.
  No lo confundas ni lo rompas.
- Persistencia del estado de estudio: clave `estudio` vía `storage.js`
  (`load('estudio')`, `update('estudio', fn)`).

### Render de contenido

`renderInline(texto)` (de `js/markdown.js`, ya importado en `study.js`) renderiza
markdown + KaTeX. Úsalo para cualquier texto que pintes.

---

## 2. El contrato de datos que te dejó el arquitecto

`data/arena-dificultades.json` tiene esta forma:

```json
{
  "_meta": { "criterios": {...}, "total": 1619, "distribucion": {...} },
  "dificultades": {
    "arq1-q1": "easy",
    "arq1-q2": "medium",
    "...": "..."
  }
}
```

- La llave de `dificultades` es el **`id` exacto** de cada pregunta en
  `banco[]`.
- El valor es siempre uno de: `"easy"`, `"medium"`, `"hard"`.
- Cubre las **1619** preguntas, sin faltantes ni sobrantes (ya validado).

---

## 3. TAREA A — Inyectar `difficulty` en cada pregunta del banco

**Objetivo:** que cada objeto de `unidad.banco[]` (solo unidades `fase-7`) tenga
un campo `"difficulty"` con el valor que indica `arena-dificultades.json`.

Reutiliza el campo preferido por la spec (`reformulacion-examenes.md` §1):

```json
"difficulty": "easy" | "medium" | "hard"
```

**Implementación: un script de migración idempotente, único y verificable.**
Crea `scripts/aplicar-dificultad-arena.mjs` (o el patrón de scripts que ya use el
repo — revisa la carpeta `scripts/` antes) que:

1. Lea `data/study.json` y `data/arena-dificultades.json`.
2. Para cada `unidad` con `bloque === "fase-7"`, para cada `q` en `unidad.banco`:
   - Asigna `q.difficulty = dificultades[q.id]`.
   - Si `q.id` **no** está en el mapa → **aborta con error** listando los ids
     faltantes (no inventes un default silencioso).
3. NO toques unidades de otros bloques. NO reordenes claves de forma destructiva.
   NO cambies ningún otro campo.
4. Escribe `data/study.json` de vuelta **preservando el formato** (mismo
   `indent`, UTF-8 sin escapar acentos: `ensure_ascii` apagado / `JSON.stringify`
   con indent de 2 si ese es el estilo actual — **verifica el estilo actual del
   archivo antes de sobreescribir** para no generar un diff gigante por
   reformateo).
5. Es **idempotente**: correrlo dos veces deja el archivo igual.

Tras correrlo, valida:

```bash
python3 -c "import json; d=json.load(open('data/study.json')); \
b=[q for u in d['unidades'] if u.get('bloque')=='fase-7' for q in u['banco']]; \
print('banco:', len(b), '| con difficulty:', sum('difficulty' in q for q in b), \
'| valores:', set(q.get('difficulty') for q in b))"
# Debe imprimir: banco: 1619 | con difficulty: 1619 | valores: {'easy','medium','hard'}
```

> **Compatibilidad:** agregar un campo nuevo NO rompe consumidores existentes
> (todos los `find`/`map` actuales ignoran campos extra). Datos viejos en
> LocalStorage no se ven afectados: el banco vive en `study.json`, no en el
> progreso del usuario.

---

## 4. TAREA B — Selector de dificultad por lección

Implementa en `js/study.js`, dentro del flujo de `abrirUnidad` /
`#btn-quiz-iniciar`, un selector de dificultad **antes de iniciar el quiz** de la
lección.

### 4.1 UI

- Cuatro opciones, en este orden y con estas etiquetas en español:
  **Fácil**, **Medio**, **Difícil**, **Mixto**.
- Estilo sobrio, oscuro, consistente con la Arena actual (reusa clases CSS
  existentes de botones/segmented control; **no** hagas rediseño visual masivo).
- Colócalo en el panel de la lección, junto a `#btn-quiz-iniciar`, visible solo
  cuando la unidad **no** está completada ni con quiz en curso (mismo `else` de
  `abrirUnidad` donde hoy se muestra `#btn-quiz-iniciar`).
- **Default: `Mixto`** (conserva el comportamiento actual).

### 4.2 Mapeo etiqueta → valor

`Fácil→easy`, `Medio→medium`, `Difícil→hard`, `Mixto→todas`.

### 4.3 Comportamiento al iniciar el quiz

Al pulsar iniciar, construye `preguntasIds` así (modifica el handler de
`#btn-quiz-iniciar`, ≈línea 719):

```js
const dif = /* valor elegido: 'easy' | 'medium' | 'hard' | 'mixto' */;
let pool = u.banco;
if (dif !== 'mixto') pool = u.banco.filter((q) => q.difficulty === dif);
const ids = barajar(pool.map((q) => q.id));   // selección ALEATORIA, sin repetición
st.quizEnCurso = {
  unidadId: u.id,
  preguntasIds: ids,
  dificultad: dif,           // persistir la dificultad elegida en la sesión
  indice: 0,
  resultados: [],
  esRepaso: false,
};
```

- **`barajar`**: implementa un Fisher–Yates puro (sin libs). Si ya existe un
  helper de shuffle en el repo, reúsalo (búscalo: `grep -rn "sort(() => Math.random"`).
- **Mixto** debe seguir incluyendo TODAS las preguntas de la lección (no pierdas
  contenido curado). Hoy van en orden; con esta tarea pasan a ir barajadas — eso
  es aceptable y deseable (`reformulacion-examenes.md` §4 pide selección
  aleatoria). Si quieres ser ultra-conservador y NO barajar en Mixto, documenta
  la decisión en el reporte; pero para Fácil/Medio/Difícil **sí** se baraja.
- **Dosis:** el campo `unidad.dosis` es texto libre (p. ej. "30-40 min…"), **no
  un número** — no lo uses como conteo. Por defecto, usa **todas** las preguntas
  del subconjunto filtrado (no truncar). Si decides introducir un tope
  configurable de preguntas por sesión, **centralízalo** en una sola constante al
  inicio del módulo (p. ej. `const MAX_QUIZ_LECCION = null; // null = sin tope`)
  y deja `null` por defecto para no cambiar el comportamiento.

### 4.4 Edge cases (obligatorios, de `reformulacion-examenes.md` §4 y §10)

- Si el subconjunto filtrado queda **vacío** (la lección no tiene preguntas de
  esa dificultad): **no inicies el quiz**; muestra un estado vacío claro en
  español (p. ej. "Esta lección no tiene preguntas de nivel Difícil. Prueba otro
  nivel.") y permite **cambiar la dificultad** sin recargar.
- Nunca debe lanzar excepción si una dificultad no tiene preguntas.
- Una pregunta sin `difficulty` (no debería ocurrir tras la Tarea A) NO debe
  romper Mixto: trátala como incluida en Mixto y excluida de los filtros
  específicos.

---

## 5. TAREA C — Examen final por cluster

Implementa un **examen final del cluster** construido con **el banco de TODAS
las lecciones del cluster** (no de la última lección, no la simulación
`cluster-*.json`).

### 5.1 Dónde

En el acordeón de cluster (`crearClusterAcordeon`, ≈línea 426): añade una opción
**"Examen final del cluster"**. Respeta la regla de desbloqueo existente: si el
patrón actual abre algo "al completar todas las unidades del bloque/cluster"
(mira `bloqueUnidadesCompletas`, ≈línea 169, y `unidades.filter(unidadCompletada)`,
≈línea 430), **consérvala**. Si ya hay un patrón de desbloqueo, úsalo; no
inventes uno nuevo.

### 5.2 Pool de preguntas del cluster

```js
function getClusterQuestionPool(clusterId) {
  const c = taxonomia.find((x) => x.id === clusterId);
  return (c?.unidades ?? [])
    .map(unidad)
    .filter((u) => u && u.bloque === 'fase-7')
    .flatMap((u) => u.banco ?? []);
}
```

### 5.3 Selector de dificultad del examen

Mismas 4 opciones (Fácil/Medio/Difícil/Mixto, default Mixto) **antes** de iniciar
el examen. Filtra el pool por `difficulty` igual que en la Tarea B.

### 5.4 Tamaño del examen

- Revisa primero si ya existe una dosis/cantidad para exámenes (mira
  `muestrearExamen(bloque, n = 5)`, ≈línea 971, que es el examen de bloque del
  Modo Estudio — **no lo reutilices tal cual**, es otra cosa, pero te sirve de
  referencia de estilo).
- Define **una sola constante centralizada**:

  ```js
  const DEFAULT_CLUSTER_EXAM_SIZE = 25;
  ```

- Selección **aleatoria sin repetición** (`barajar` + `slice(0, N)`). Si tras
  filtrar por dificultad hay **menos** preguntas que `N`, usa **todas** las
  disponibles y muestra una nota discreta ("Solo hay X preguntas de este nivel
  en el cluster"). No truncar de forma que crashee.
- El examen debe tomar preguntas de **varias lecciones** del cluster (lo
  garantiza usar el pool completo + barajar).

### 5.5 Render y cierre

Reutiliza el render de pregunta del quiz tanto como puedas (mismo patrón de
`renderPreguntaQuiz`: enunciado con `renderInline`, textarea, revelar
solución+explicación, autoevaluación). Mantén el estado del examen en `storage.js`
(clave `estudio`, p. ej. `examenClusterEnCurso`), análogo a `quizEnCurso`, para
que sobreviva recargas. No mezcles ese estado con `quizEnCurso` de lección.

---

## 6. Persistencia (de `reformulacion-examenes.md` §7)

- **No rompas** el progreso existente (`unidadesCompletadas`, racha, repaso
  espaciado, sync Supabase). El banco y la dificultad viven en `study.json`; el
  progreso del usuario no cambia de forma.
- Persiste la **última dificultad elegida**:
  - por lección: p. ej. `estudio.ultimaDificultadLeccion[unidadId]`.
  - por examen de cluster: p. ej. `estudio.ultimaDificultadCluster[clusterId]`.
  - Todo vía `update('estudio', fn)`. Si complica la primera versión, déjalo
    documentado como mejora posterior, pero el **default Mixto** es obligatorio.
- Si agregas claves nuevas al objeto `estudio`, confirma que se sincronizan/
  excluyen correctamente (revisa `CLAVES_SYNC` y `encolarEvento` en `storage.js`);
  no subas estado efímero innecesario.

---

## 7. Service worker

- Sube `VERSION` en `sw.js` (`cogitoergosum-v138` → `cogitoergosum-v139`).
- `data/study.json` **ya** está en `SHELL` (línea ≈73). `data/arena-dificultades.json`
  **NO** necesita ir al precache si tu script de la Tarea A inyecta la dificultad
  directamente en `study.json` (recomendado). Si en cambio decidieras cargarlo en
  runtime con `fetch`, **debes** añadirlo a `SHELL`. La opción recomendada es
  inyectar en `study.json` y NO depender de un fetch extra.

---

## 8. Validación obligatoria antes de cerrar

Ejecuta y reporta:

1. `node --check` en `js/study.js`, `js/storage.js`, `sw.js` y cualquier `.js`
   que toques.
2. JSON parseables: `study.json`, `arena-dificultades.json`.
3. El one-liner de §3 (1619 / 1619 con difficulty).
4. Sin IDs duplicados nuevos en `banco`.
5. Manual (abre la app servida en local, p. ej. `python3 -m http.server`):
   - La app carga; la Fase 7 Arena renderiza; los **8 clusters** siguen
     apareciendo; las lecciones siguen dentro de cada cluster.
   - Una lección inicia quiz en **Fácil**, **Medio**, **Difícil** y **Mixto**.
   - Una dificultad sin preguntas muestra estado vacío y deja cambiar de nivel
     (sin crashear, sin errores en consola).
   - El examen final aparece donde corresponde y filtra por dificultad, tomando
     de varias lecciones.
   - **Cero errores en consola.** No se perdió contenido curado. El flujo viejo
     funciona con Mixto.
6. Prueba con **red desconectada** (offline-first): la app sigue cargando.
7. Relee el checklist anti-§0.1 de `HANDOFFCES.md`: nada de leaderboards,
   aleatoriedad de recompensas, culpa por fallo, etc. (Este feature no las
   introduce; confírmalo.)

---

## 9. Lo que NO debes hacer

- ❌ Reclasificar preguntas o cuestionar las dificultades de
  `arena-dificultades.json`. Esa es la decisión del arquitecto; tú la aplicas.
- ❌ Borrar o renombrar preguntas, cambiar IDs, editar enunciados/soluciones.
- ❌ Tocar la simulación `abrirSimCluster` / `cluster-*.json` (es otra feature).
- ❌ Añadir librerías, frameworks o CDNs.
- ❌ Llamar a `localStorage` directamente (usa `storage.js`).
- ❌ Reformatear `study.json` entero (cuida el diff: solo deben aparecer los
  nuevos campos `difficulty`).
- ❌ Olvidar subir `VERSION` en `sw.js`.

---

## 10. Reporte final (entrégalo al terminar)

1. Resumen ejecutivo.
2. Archivos modificados/creados (con rutas reales).
3. Confirmación de que `difficulty` quedó en las 1619 preguntas (salida del
   one-liner).
4. Cómo funciona el selector por lección (incl. default Mixto y edge cases).
5. Cómo funciona el examen final por cluster (pool, tamaño, desbloqueo).
6. Decisiones tomadas en puntos abiertos (barajar Mixto sí/no, persistencia de
   última dificultad sí/no, tope por lección).
7. Validaciones ejecutadas y su resultado.
8. Riesgos pendientes / mejoras recomendadas.

---

### Instrucción final

Empieza **leyendo el código real** (`js/study.js` completo, `js/storage.js`,
`sw.js`, el esquema de `data/study.json`) y confirma que los anclajes de este
documento (nombres de función, líneas aproximadas, estado `quizEnCurso`) siguen
vigentes. Si algo cambió, **ajústate a la realidad del repo y repórtalo**.
Implementa de forma incremental, conservadora y compatible. El objetivo: que
Arena permita práctica deliberada por dificultad —por lección y por examen final
de cluster— sin romper nada de lo existente.
