# PROMPT EJECUTOR (ChatGPT 5.5) · Reparar render de código + Fase 8 Oleada 3

> **Eres un software engineer senior y ejecutor.** Un arquitecto ya auditó el
> repo CogitoErgoSum, localizó la causa raíz del bug y diseñó el plan. Tu trabajo
> es **implementar** siguiendo esto al pie de la letra. Si la realidad del repo no
> coincide con lo aquí descrito, **DETENTE y reporta** en vez de inventar.
>
> Hay **2 tareas**. Ejecútalas **en orden** (Tarea 1 es ALTA y bloquea a la 2).
> **Un commit por sub-tarea.** Tras cada una, corre su checklist antes de seguir.

---

## 0. Reglas duras del proyecto (NO negociables)

- HTML / CSS / **JavaScript vanilla**, ES Modules. **Cero dependencias** nuevas,
  cero frameworks, cero CDNs, cero librerías de markdown ni de resaltado.
- Todo el texto visible al usuario, en **español**.
- **`js/storage.js` es la única puerta a LocalStorage.** Nunca llames a
  `localStorage` directamente.
- Funciona en **GitHub Pages**, **offline-first**. No rompas el service worker,
  el manifest, Supabase ni la sincronización.
- `node --check` debe pasar en cada `.js` que toques. Todo JSON debe quedar
  parseable.
- **Service worker:** al tocar cualquier archivo del `SHELL` de `sw.js`
  (incluye `index.html`, `css/styles.css`, **todos** los `js/*.js`,
  `data/study.json`, `data/ciberseguridad/_taxonomia.json` y los
  `data/teoria/*.md`), **sube `VERSION` +1**. Hoy va en **`cogitoergosum-v148`**
  (ajusta al número real cuando llegues; Tarea 1 → v149, etc.).
- No reformatees archivos enteros (cuida el diff). No cambies contenido
  pedagógico salvo que la tarea lo pida.
- Código limpio, comentado al estilo del módulo que edites.
- **`data/ciberseguridad/_unidades.json` es la FUENTE de las unidades de la
  Fase 8** (formato 2 espacios). Las unidades NO se editan a mano en
  `data/study.json`: se editan en `_unidades.json` y se **inyectan** con
  `node scripts/aplicar-ciberseguridad.mjs` (idempotente; reordena y renumera
  `orden` 801+ por el orden de la taxonomía; escribe study.json con indent de
  **1 espacio y sin newline final**). `data/study.json` NO lleva newline final:
  no se lo agregues.

---

# TAREA 1 — [ALTA] Reparar el render de bloques de código (fenced code blocks)

## 1.1 Diagnóstico (ya confirmado por el arquitecto — NO lo re-investigues)

`js/markdown.js` (`renderMarkdown`) **no implementa bloques de código con triple
backtick** (```` ``` ````). Por eso, una lección con:

````
```python
# VULNERABLE
q = "SELECT * FROM users WHERE name = '" + nombre + "'"
```
````

renderiza MAL: la línea ```` ```python ```` sale como **texto literal**, y la
línea ```` # VULNERABLE ```` de dentro del bloque se interpreta como **encabezado
`<h1>`** (porque el `#` cae en la rama de encabezados del loop). El cierre
```` ``` ```` también sale literal. (Visto en `cyber-web1` y otras.)

**Alcance:** 14 lecciones usan fences hoy:
`grep -lF '```' data/teoria/*.md` → arena-cc1/cc2/cc3/cc4, arena-h1, arena-h2,
arena-m1, arena-m2, arena-sd1, **cyber-blue1, cyber-dev1, cyber-sys1, cyber-llm1,
cyber-web1**. El fix las arregla todas a la vez (una sola causa raíz).

El smoke test no lo detectó porque no busca fences sin renderizar (lo arreglas en
el paso 1.4).

## 1.2 El fix en `js/markdown.js`

Contexto del código: `renderMarkdown(md)` hace
`const lineas = escapar(md ?? '').split('\n');` (las líneas YA están escapadas
como HTML) y recorre `for (let i = 0; i < lineas.length; i++) { const linea =
lineas[i]; const t = linea.trim(); if (!t) { … continue; } … }` con ramas para
tabla, encabezado `/^(#{1,4})\s+(.*)$/`, `---`, `$$`, citas `&gt;`, listas y
párrafo. Usa los helpers ya existentes `cerrarLista()` y `cerrarCita()`.

**Añade una rama NUEVA como PRIMERA comprobación dentro del `for`, justo DESPUÉS
del bloque `if (!t) { … continue; }` y ANTES de la rama de tabla.** Debe:

1. Detectar el abre-fence: `t` empieza con ```` ``` ```` (regex `/^```(.*)$/`).
2. Cerrar lista y cita abiertas (`cerrarLista(); cerrarCita();`).
3. Recoger las líneas siguientes **crudas** (usa `lineas[j]`, NO `.trim()`, para
   conservar la indentación del código) hasta encontrar una línea cuyo `trim()`
   empiece con ```` ``` ```` (cierre) o hasta EOF.
4. Emitir `<pre><code> … </code></pre>` con el contenido unido por `'\n'`. **NO
   pases ese contenido por `inline()`** (es código literal). El contenido ya está
   escapado (viene de `escapar()` arriba), así que va seguro tal cual.
5. Avanzar `i` hasta la línea de cierre.

Código de referencia (ajústalo al estilo del archivo):

```js
// Bloque de código cercado: ```lang … ``` → <pre><code> verbatim (sin inline).
// Debe ir ANTES de la rama de encabezados: si no, las líneas '# ...' internas
// se renderizarían como <h1>. Las líneas ya vienen escapadas por escapar().
if (/^```/.test(t)) {
  cerrarLista();
  cerrarCita();
  const cuerpo = [];
  let j = i + 1;
  while (j < lineas.length && !lineas[j].trim().startsWith('```')) {
    cuerpo.push(lineas[j]); // crudas: conservan indentación
    j++;
  }
  html.push(`<pre><code>${cuerpo.join('\n')}</code></pre>`);
  i = j; // saltar hasta (e incluyendo) la línea de cierre ```
  continue;
}
```

> No toques nada más de `markdown.js`: ni `inline()`, ni la sentinela NUL, ni el
> resto de ramas. Solo añades esta rama.

## 1.3 CSS del bloque de código (`css/styles.css`)

Tras la regla `.leccion code { … }` (≈línea 1553-1560), añade el estilo del
bloque (y resetea el `code` interno para que no herede el chip inline):

```css
.leccion pre {
  background: var(--bg-elevado);
  border: 1px solid var(--borde);
  border-radius: 8px;
  padding: 12px 14px;
  overflow-x: auto;
  margin: 12px 0;
}
.leccion pre code {
  display: block;
  background: none;
  border: none;
  padding: 0;
  border-radius: 0;
  font-family: var(--mono);
  font-size: 0.82rem;
  line-height: 1.5;
  white-space: pre;
  color: var(--texto);
}
```

Si los quizzes/exámenes muestran código (Tarea 2), el contenedor de la pregunta
no es `.leccion`; añade también selectores equivalentes para esos contenedores
(p. ej. `#quiz-enunciado pre`, `#examen-cluster-contenido pre`) **o** una clase
genérica. Decide la forma menos invasiva y documenta cuál usaste.

## 1.4 Endurecer el smoke test (`scripts/smoke-teoria.mjs`)

Hoy ya escanea los 206 `.md` y falla si hay `undefined` en el HTML. **Añade una
comprobación de fences sin renderizar**: si el HTML renderizado contiene un triple
backtick literal (```` ``` ````), cuéntalo y, si el total > 0, imprime los
archivos y pon `process.exitCode = 1`. Reusa el patrón del contador `undefined`
existente (variable `rawFence`, mensaje claro, exit ≠ 0).

## 1.5 Validación obligatoria (Tarea 1)

1. `node --check js/markdown.js`.
2. `node scripts/smoke-teoria.mjs` → debe imprimir `threw=0 rawDisplayMath=0
   undefined=0` y **`rawFence=0`** (antes del fix habría ≥14).
3. Comprobación puntual: renderiza `data/teoria/cyber-web1.md` y verifica que el
   bloque sale como `<pre><code>…</code></pre>` y que `# VULNERABLE` aparece como
   **texto literal dentro del bloque** (NO como `<h1>`):
   ```bash
   node --input-type=module -e "import {renderMarkdown} from './js/markdown.js'; import fs from 'node:fs'; const h=renderMarkdown(fs.readFileSync('data/teoria/cyber-web1.md','utf8')); console.log('pre:', h.includes('<pre><code>'), '| h1 VULNERABLE:', /<h1>VULNERABLE/.test(h));"
   ```
   Debe dar `pre: true | h1 VULNERABLE: false`.
4. Sirve la app (`python3 -m http.server 8000`), abre Estudio → Fase 8 →
   cluster Web/APIs → lección "Web I" → "Leer la lección": el bloque de código se
   ve como bloque monoespaciado, sin `# VULNERABLE` gigante. Cero errores en
   consola.
5. Sube `VERSION` en `sw.js` (tocaste markdown.js + styles.css). Commit solo de
   esta tarea.

---

# TAREA 2 — [Oleada 3] Práctica avanzada + render multilínea + examen integrador

> Referencia: `ciberseguridad.md` §10 (tipos de práctica), §11 (evaluaciones),
> §17 Fase 3 **Oleada 3** (escenarios avanzados, log analysis, code review, ML
> pipeline review, LLM security review, **examen integrador de toda la ruta**).
> Estado actual: Fase 8 = 8 clusters × 5 lecciones = **40 unidades**, **240
> preguntas** de banco (todas `tipo: "concepto"`), 8 mini-proyectos, examen final
> por dificultad por cluster. Falta lo de Oleada 3.

Ejecuta las sub-tareas **en orden**: 2a habilita a 2b; 2c es independiente.

## 2a — Render multilínea/código en quizzes y exámenes (DEPENDE de Tarea 1)

**Problema:** las preguntas del banco se pintan con `renderInline(...)`, que es de
**una sola línea** y NO soporta saltos de línea ni fences. Por eso una pregunta de
`code_review` o `log_analysis` con un snippet multilínea no se vería bien.

**Fix:** introduce un helper en `js/study.js` y úsalo donde hoy se renderiza
`enunciado`/`solucion`/`explicacion` de banco:

```js
import { renderMarkdown, renderInline } from './markdown.js'; // (ya importado)

// Bloque si el texto trae saltos de línea o código cercado; si no, inline.
function renderCampoPregunta(txt) {
  const s = txt ?? '';
  return /\n|```/.test(s) ? renderMarkdown(s) : renderInline(s);
}
```

Sustituye `renderInline(q.enunciado)`, `renderInline(q.solucion)`,
`renderInline(q.explicacion)` por `renderCampoPregunta(...)` en:
- `renderPreguntaQuiz()` (≈líneas 954, 1000, 1005).
- `renderExamenCluster()` (≈líneas 1704, 1738, 1743).

**No** cambies el examen-motor de bloque (`renderExamen`, fase 0-7) salvo que
quieras; su esquema es distinto (`item.*`). Mantén el cambio acotado a las
preguntas de banco (quiz de unidad + examen de cluster), que es lo que usa la
Fase 8.

Verifica que el CSS de `pre` del paso 1.3 cubra los contenedores del quiz/examen
(`#quiz-enunciado`, `#examen-cluster-contenido` u homólogos reales — confírmalos
en `index.html`).

**Validación 2a:** crea una pregunta de prueba con `\n` y un fence en su
`enunciado` (en una unidad de _unidades.json), reinyecta, sirve y comprueba que se
ve el bloque de código en el quiz. (Quita la de prueba al terminar o conviértela
en una real de 2b.)

## 2b — Tipos de práctica avanzada como banco enriquecido (§10)

**Decisión de arquitectura (respétala):** NO crees un esquema nuevo de práctica.
Reutiliza el esquema de banco existente
`{ id, tipo, enunciado, solucion, explicacion, difficulty }` y usa el campo
**`tipo`** para marcar la modalidad. El `enunciado` lleva el escenario / snippet /
log (multilínea y con fences, que ya renderizan tras Tarea 1 + 2a) y la `solucion`
el análisis esperado. Así no hay más cambios de render.

Valores de `tipo` a usar (además del actual `"concepto"`):
`"scenario"`, `"code_review"`, `"log_analysis"`, `"ml_pipeline_review"`,
`"llm_security_review"`, `"threat_model"`, `"data_privacy_review"`, `"reflexion"`.

**Dónde:** añade estas preguntas al `banco[]` de las unidades correspondientes en
`data/ciberseguridad/_unidades.json`; luego corre
`node scripts/aplicar-ciberseguridad.mjs` para inyectarlas a `study.json`. Fluirán
solas al quiz de la unidad y al examen final del cluster (que toma de todas las
unidades del cluster).

**Mapeo por cluster (mínimo a añadir; cada pregunta con `id` único, p. ej.
sufijos `-s1` scenario, `-cr1` code_review, `-la1` log_analysis, `-mp1`
ml_pipeline_review, `-ls1` llm_security_review, `-tm1` threat_model, `-dpr1`
data_privacy_review, `-r1` reflexion):**

| Cluster (unidades) | Práctica avanzada a añadir (mínimo) |
|---|---|
| cyber-mindset (ms1-5) | 3 `scenario` (elegir amenaza/impacto/control), 2 `threat_model`, 2 `reflexion` |
| cyber-systems-crypto (sys1-5) | 3 `scenario`, 2 `code_review` (TLS/secretos/permisos), 2 `reflexion` |
| cyber-web-api (web1-5) | 2 `scenario`, 3 `code_review` (SQLi/XSS/BOLA con snippet en fence), 2 `reflexion` |
| cyber-data-privacy (dp1-5) | 3 `data_privacy_review` (clasificar datos/reidentificación), 2 `scenario`, 2 `reflexion` |
| cyber-secure-dev (dev1-5) | 3 `code_review` (secreto hardcodeado, validación, deserialización), 2 `scenario`, 2 `reflexion` |
| cyber-blue-team (blue1-5) | 3 `log_analysis` (logs ficticios → táctica/impacto/acción), 2 `scenario`, 2 `reflexion` |
| cyber-ml-security (mls1-5) | 3 `ml_pipeline_review` (leakage/poisoning/exposición), 2 `scenario`, 2 `reflexion` |
| cyber-llm-rag-agents (llm1-5) | 3 `llm_security_review` (prompt injection/RAG/agencia), 2 `scenario`, 2 `reflexion` |

Reglas de contenido (sigue el tono de las lecciones existentes, defensivo, no
"hacking"; ver `ciberseguridad.md` §12 para feedback sobrio):
- `code_review`: el `enunciado` incluye un snippet **vulnerable** en un fence
  (```` ```python ````, ```` ```js ````, etc.); la `solucion` señala el fallo y
  la corrección. Inserta la modalidad en la 1.ª línea del enunciado en prosa
  ("Revisa este código y di qué falla:") seguida del fence.
- `log_analysis`: el `enunciado` trae un log ficticio en un fence; la `solucion`
  mapea a táctica ATT&CK, impacto y acción defensiva, y qué dato faltaría.
- `scenario`: situación corta de decisión defensiva; la `solucion` razona la
  elección (amenaza/impacto/control/siguiente paso).
- `reflexion`: pregunta abierta de metacognición; la `solucion` ofrece una
  reflexión modelo (no hay "respuesta única").
- **No incluyas instrucciones ofensivas accionables.** Marca cada lab externo con
  la nota de seguridad ("solo en laboratorios autorizados") cuando aplique.
- `difficulty`: asigna `easy`/`medium`/`hard` de forma razonable (las prácticas
  suelen ser `medium`/`hard`).

**Idempotencia/IDs:** todos los `id` de pregunta deben ser únicos a nivel global.
Verifica con el chequeo del paso de validación. Reinyecta tras editar.

> **Nota de alcance honesta:** `ciberseguridad.md` §11 pide, por LECCIÓN, 10 easy
> + 10 medium + 10 hard + 5 escenario + 5 reflexión. Eso son ~1400 preguntas y NO
> es el objetivo de esta oleada: Oleada 3 (§17) es **añadir los tipos de práctica
> avanzada + el examen integrador**, que es lo de arriba. Si tras completar esto
> tienes presupuesto, densifica hacia §11 por cluster, pero **no** sacrifiques
> calidad por volumen (regla anti-contenido árido, §9). Si paras, **reporta** qué
> quedó para una Oleada 4.

## 2c — Examen integrador de toda la ruta (Fase 8)

Hoy existe el **examen final por cluster** (`prepararExamenCluster` /
`renderExamenCluster`, con selector de dificultad; pool vía
`getClusterQuestionPool(clusterId)` que filtra por el `bloque` del cluster).
Añade un **examen integrador** que tome preguntas de **TODAS** las unidades de la
Fase 8 (interleaving de los 8 clusters), con el mismo selector de dificultad.

Implementación recomendada (mínima y compatible):
1. Helper en `study.js`:
   ```js
   // Todas las preguntas de banco de un bloque (para el examen integrador).
   function getBloqueQuestionPool(bloqueId) {
     return (datos?.unidades ?? [])
       .filter((u) => u.bloque === bloqueId)
       .flatMap((u) => u.banco ?? []);
   }
   ```
2. Generaliza el examen de cluster para aceptar un **pool y un título explícitos**
   sin romper su uso actual. Opción A: refactiliza `prepararExamenCluster` para
   que acepte `(idLogico, titulo, pool)` y, si no se pasa `pool`, use
   `getClusterQuestionPool(idLogico)`. Opción B (más segura): crea
   `prepararExamenIntegrador()` y `renderExamenIntegrador()` clonando el patrón de
   cluster pero con `getBloqueQuestionPool('fase-8')` y un `id` lógico reservado
   (p. ej. `"__integrador-fase-8"`). Guarda el estado en el mismo
   `examenClusterEnCurso` de `storage.js` (DEFAULTS `estudio`) para persistir al
   recargar; reutiliza el panel `#estudio-examen-cluster`. **Elige la opción que
   menos riesgo introduzca y documenta cuál.**
3. **UI:** en `renderizar()`, cuando el bloque visible tenga taxonomía (hoy: el
   guard `taxonomiaDe(b.id).length > 0`), muestra un botón
   **"📚 Examen integrador de la ruta"** (además de la nota de "evaluación por
   cluster"). Cablea su `click` a la preparación del examen integrador. Tamaño por
   defecto: reutiliza `DEFAULT_CLUSTER_EXAM_SIZE` (25) o sube a ~30 para el
   integrador (decide y documenta). Barajado Fisher-Yates (`barajar`) ya existe.
4. Asegura que al recargar a mitad de examen integrador se restaure (igual que el
   de cluster en `renderizar`).

**Estilo/HTML:** reutiliza el panel y clases existentes del examen de cluster; si
añades un botón nuevo, dale una clase coherente (`.examen-integrador-launch` o
reusa `.cluster-exam-launch`).

## 2d — Validación y cierre (Tarea 2)

1. `node --check js/study.js` y de cualquier `.js` tocado.
2. `data/ciberseguridad/_unidades.json` y `data/study.json` parseables;
   reinyectado con `scripts/aplicar-ciberseguridad.mjs` (sin error).
3. Chequeo de consistencia (adáptalo del que ya se usa): 8 clusters, 40 unidades
   fase-8, **0 ids de pregunta duplicados** globales, toda unidad con su `.md`
   existente, conteo de preguntas por `tipo` (verifica que aparecen los nuevos
   tipos).
4. `node scripts/smoke-teoria.mjs` → `threw=0 undefined=0 rawFence=0`.
5. Verifica que **cada archivo del SHELL de `sw.js` existe** (script de conteo).
6. Sirve la app: en Fase 8, un quiz con `code_review`/`log_analysis` muestra el
   código/log como bloque; el **examen integrador** abre, baraja de varios
   clusters, respeta el selector de dificultad y persiste al recargar. Cero
   errores en consola. Las fases 0-7 siguen intactas.
7. Sube `VERSION` en `sw.js` por cada commit que toque el shell. **Un commit por
   sub-tarea** (2a, 2b, 2c) o agrupa 2a+2c (código) y 2b (datos) en dos commits
   claros — decide y deja el criterio en el mensaje.

---

## Reporte final (al terminar)

1. Resumen por tarea.
2. Archivos modificados/creados (rutas reales) y el `VERSION` final de `sw.js`.
3. Tarea 1: salida del smoke (`rawFence` antes/después) y la comprobación puntual
   de `cyber-web1` (`pre:true h1:false`).
4. Tarea 2: nuevos `tipo` añadidos y cuántas preguntas por cluster; cómo quedó el
   examen integrador (opción A/B elegida); conteo final de preguntas fase-8.
5. Qué quedó pendiente (densificación §11 → posible Oleada 4) y riesgos.

## Lo que NO debes hacer

- ❌ Añadir librerías, frameworks, CDNs, resaltadores de sintaxis o un motor de
  markdown externo.
- ❌ Tocar `inline()` / la sentinela NUL de `markdown.js` (solo añades la rama de
  fences).
- ❌ Editar las unidades de la Fase 8 directamente en `study.json` (edita
  `_unidades.json` y reinyecta).
- ❌ Añadir newline final a `study.json`.
- ❌ Romper el examen-motor de bloque (fases 0-7) ni la simulación de entrevista
  (fase-7).
- ❌ Incluir instrucciones ofensivas accionables en las prácticas; mantén el
  enfoque defensivo y la nota de "solo laboratorios autorizados".
- ❌ Sacrificar calidad pedagógica por volumen (regla anti-contenido árido §9).
- ❌ Olvidar subir `VERSION` en `sw.js` al tocar el shell.
```
