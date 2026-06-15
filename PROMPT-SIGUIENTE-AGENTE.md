# PROMPT para el siguiente agente (pégalo tal cual al iniciar la nueva cuenta)

---

Vas a continuar la **auditoría pedagógica de la Fase 7** (Arena de Entrevistas de
Élite) del proyecto **CogitoErgoSum** (web app local-first, HTML/CSS/JS vanilla,
sin frameworks, PWA en GitHub Pages). La memoria de Claude NO cruza de cuenta, así
que **todo lo que necesitas vive en el repo**. **Antes de tocar nada, lee, en este
orden:**

1. `HANDOFF-AUDITORIA-FASE7.md` — estado exacto, qué falta, plantilla, workflow,
   reglas. Es tu mapa principal. Lee especialmente §3 (estado), §4 (la plantilla de
   enriquecimiento), §5 (workflow por lote), §7 (Oleada 3) y §8 (lo que NO hacer).
2. `auditoria.md` — la especificación pedagógica original / contrato de calidad.
3. `CLAUDE.md` (la cabecera apunta a `HANDOFFCES.md` §0 "Constitución" — es LEY:
   el error nunca castiga, cero dinero, IA siempre opcional, anti-dark-patterns).
4. Como ejemplares del tono y profundidad, lee 2-3 lecciones ya enriquecidas:
   `data/teoria/arena-h17.md`, `data/teoria/arena-cc3.md`, `data/teoria/arena-q6.md`.

**Contexto en una frase:** la Fase 7 son 118 unidades; la lección estudiable de cada
una vive en `data/teoria/<unidad-id>.md`, se carga en runtime (`fetch` +
`renderMarkdown` de `js/markdown.js`) y se lee como "📖 Leer la lección aquí". El
metadata y los quizzes viven en `data/study.json` (campo `unidades[]`); **NO edites
`study.json` ni `banco[]`** salvo que Edgar lo pida.

---

## Estado EXACTO (al 2026-06-15, sw.js v87, último commit en `main`)

**Oleada 2 (enriquecimiento por lotes): COMPLETA — 118/118.** Las 118 lecciones
`data/teoria/arena-*.md` contienen ya la sección **Transferencia isomorfa** y el
resto del contrato (mini-ejemplo socrático, prototipo/contraejemplo/caso-borde,
errores típicos, moraleja con aristas `[[arena-xxx]]`). Verifícalo (debe imprimir
vacío):
```bash
comm -23 \
  <(ls data/teoria/arena-*.md | sed 's#data/teoria/##;s#.md##' | sort) \
  <(grep -l "Transferencia isomorfa" data/teoria/arena-*.md | sed 's#data/teoria/##;s#.md##' | sort)
```

**Oleada 3 (en curso) — ver §7 del HANDOFF.** Hecho:
- ✅ **Wiki-links navegables** (sw.js v77): los `[[arena-xxx]]` de las lecciones son
  clicables y abren esa unidad. `js/markdown.js` los emite como
  `<a class="enlace-unidad">`; `js/study.js` (`cablearEnlacesLeccion`/`navegarAUnidad`)
  pone el título real y navega. Los `[[concepto-sin-unidad]]` siguen como chip; los
  literales de matriz `[[1,3],…]` intactos. NO lo rehagas.
- ✅ **Taxonomía aplicada + simulación de entrevista por área (Nivel E sin IA).**
  Sin tocar `study.json`, todo en `data/entrevista/`:
  - `_taxonomia.json`: 8 clusters (= 8 rondas de entrevista) que **particionan las
    118 unidades sin solape**: quant-prob (25), stats-inf (16), dsa (6),
    system-design (4), ds-applied (9), ml-systems (32), causal-health (22),
    conductual (4). Cada cluster tiene `track`, `descripcion`, `secuencia`, `sim` y
    `unidades[]`. **El `unidades[]` está en orden DIDÁCTICO** (no por sub-libro).
  - `cluster-<id>.json` ×8: el guion de cada ronda
    (`{ rol, duracion, preguntas:[{q, rubrica[], errores[], seguimiento?}], cierre }`),
    con 3-4 preguntas cada uno (cobertura representativa, **no exhaustiva todavía**).
- ✅ **Vista Estudio de fase-7 agrupada por las 8 categorías (UI/UX) (sw.js v80).**
  En el bloque Arena, `renderizar()` pinta **acordeones** (una categoría por cluster,
  colapsable; al desplegar: unidades en orden didáctico + botón de simulación de su
  ronda) en `#estudio-unidades` vía `renderClustersFase7()`/`crearClusterAcordeon()`/
  `crearUnidadItem()` (`js/study.js`); las demás fases siguen con lista plana. La
  simulación vive ahora dentro de cada acordeón (`abrirSimCluster(id, btn, panel)`);
  se retiró la tarjeta `#estudio-entrevista`. CSS `.cluster-*` en `css/styles.css`.
- ✅ **KaTeX vendorizado local** (sw.js v81): render de matemáticas calidad de libro,
  self-hosted en `assets/katex/` (sin CDN, offline/PWA). `js/markdown.js` usa
  `window.katex` con fallback a Unicode. **CONVENIO NUEVO (impórtate):** `$…$` es
  **siempre matemática**; la moneda va con `\$` (`\$4M`, `\$100`). Se quitó el viejo
  guard anti-`$100`. Al escribir lecciones nuevas, dólares = `\$`.
- ✅ **Cluster 1 (quant-prob) reescrito DESDE CERO** (sw.js v82-v87): las 25 lecciones
  asumen conocimiento nulo y construyen desde ahí (auditoria.md), con math en LaTeX.
  Contenido original (sin reproducir texto de los libros), conservando lo curado.
  Pendiente (otra oleada, si Edgar lo pide): los otros 7 clusters.

---

## Tu tarea (elige según lo que pida Edgar; si no dice nada, pregúntale)

Lo más natural ahora es **profundizar/ampliar los 8 guiones de simulación** por
ronda (más preguntas, más profundidad, repreguntas de presión encadenadas) tras el
review de UX, y/o avanzar los demás puntos de Oleada 3 (§7 del HANDOFF). Reglas:

- **Para editar un guion de ronda:** edita `data/entrevista/cluster-<id>.json`
  (mismo esquema). Si añades un cluster: archivo `cluster-<id>.json` + entrada en
  `_taxonomia.json` + línea en el SHELL de `sw.js`.
- **`$$` multi-línea:** documentado como limitación, pero hoy **0 casos** en el
  corpus — no lo implementes salvo que aparezca la necesidad (YAGNI).
- **Metadata de heurísticas en `banco[]`:** requiere **migración del esquema de
  `study.json` → consulta a Edgar ANTES** (es regla dura del repo). No lo toques
  por tu cuenta.
- Si en algún momento vuelves a enriquecer lecciones, usa la plantilla del §4 del
  HANDOFF (solo inserciones, `git diff` de cada `.md` debe ser `+N, -0`).

---

## Reglas innegociables y convenciones

- **Vanilla puro:** HTML/CSS/JS, sin librerías, sin frameworks, sin backend nuevo.
  Compatible con GitHub Pages y PWA. No metas dependencias.
- **Solo inserciones en las lecciones** (`+N, -0`); conserva los closers
  (Disparadores/Síntesis/Retrieval).
- **PWA / caché:** al cambiar cualquier archivo del shell (`.md`, `js/*`,
  `css/styles.css`, `data/*`, `index.html`), **sube `const VERSION` en `sw.js`**
  (va por `cogitoergosum-vNN`; ahora en **v79**) y si añades archivos nuevos a
  `data/` precachéalos en el array `SHELL`.
- **Nada de información clínica/diagnóstica** en el contenido
  (`<restricciones_clinicas_y_eticas>` de `auditoria.md`).
- Puedes citar libremente los libros de `Arena/` y `Biblioteca/` (comprados, sin
  problema de copyright).
- **NO edites `data/study.json` ni `banco[]`** sin que Edgar lo pida.
- **NO commitees** los sueltos del working dir que no son parte de la tarea:
  `*.pdf`, `arena.md`, `prompt.md`, `.claude/settings.local.json`.

## Validación por cada cambio (al pie de la letra)

```bash
# 1. Render de lecciones intacto (si tocaste .md o markdown.js):
node scripts/smoke-teoria.mjs            # debe dar threw=0 rawDisplayMath=0 (rawLinks=4 = matrices, normal)
# 2. Sintaxis JS (si tocaste js/* o sw.js):
node --check js/study.js && node --check js/markdown.js && node --check sw.js
# 3. JSON de entrevista (si tocaste data/entrevista/*):
for f in data/entrevista/*.json; do node -e "JSON.parse(require('fs').readFileSync('$f','utf8'))" && echo "OK $f"; done
# 4. Inserciones puras (si enriqueciste .md):
git diff --stat data/teoria/arena-XX.md | tail -1   # debe ser "+N, -0"
```

## Sitio, repo y deploy

- Sitio público: https://imgoingsavage.github.io/cogitoergosum/
- Repo: `ImGoingSavage/cogitoergosum`, GitHub Pages desde `main`, raíz.
- **Se commitea y pushea directo a `main`** (es la convención del repo y dispara el
  deploy). Mensajes en español, estilo del repo, terminando con
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- Tras cada lote/cambio, **actualiza el registro del HANDOFF** (§3 para lecciones,
  §7 para Oleada 3) y commitéalo, para que el siguiente agente herede el estado.

Trabaja con criterio de arquitecto-integrador, prioriza calidad sobre cantidad,
valida y pushea cada cambio, y mantén vivo el registro del HANDOFF. Empieza leyendo
el HANDOFF y, si Edgar no especificó, pregúntale si quieres densificar las rondas de
simulación o avanzar otro punto de Oleada 3.
