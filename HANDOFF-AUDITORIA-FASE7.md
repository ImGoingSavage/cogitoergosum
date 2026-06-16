# HANDOFF — Auditoría pedagógica Fase 7 (Arena de Entrevistas)

> **Para el siguiente agente (cambio de cuenta).** Este archivo es el registro
> durable del trabajo de la auditoría `auditoria.md`. La memoria de Claude NO
> cruza de cuenta, así que **todo lo que necesitas está aquí y en el repo**.
> Última actualización: 2026-06-15. Último commit de esta tanda: ver `git log`.

---

## 0. Qué es este trabajo (en una frase)

Convertir las 118 lecciones de teoría de la Fase 7 (`data/teoria/arena-*.md`) de
"fichas densas de repaso" en **material estudiable** que fabrique **aristas
conceptuales** entre dominios (Quant / MAANG / Health AI-RWE / ML Systems / DS),
siguiendo el contrato pedagógico de `auditoria.md`. NO se borra contenido: solo
se **inserta**.

El reporte completo de la auditoría inicial (modelo mental, matriz, taxonomía,
hallazgos) está en el historial de la conversación original; lo esencial para
**continuar** está abajo.

---

## 1. Modelo mental del sistema (lo que NO hay que redescubrir)

- **Dónde vive la lección:** `data/teoria/<unidad-id>.md`, una por unidad. Se
  carga en runtime con `fetch('data/teoria/${u.id}.md')` en `js/study.js`
  (función `alternarLeccion`) y se renderiza con `renderMarkdown` de
  `js/markdown.js`. Es lo que el usuario lee como "📖 Leer la lección aquí".
- **Metadata + quizzes:** `data/study.json` → `unidades[]` (campos: `id, bloque,
  orden, titulo, libro, lectura, dosis, objetivo, heuristicas[], metadata.ruta,
  ideas_clave[], banco[]`). El `banco[]` (quiz) NO se toca en esta auditoría.
  **No edites `study.json`** salvo necesidad real (todo el trabajo es markdown).
- **Rutas/dominios** (`metadata.ruta`): `quant`, `maang`, `ml-systems`,
  `health-ai-rwe`, `ciencia-datos`, `estadistica`, `conductual`.
- **PWA / caché:** `sw.js` precachea todas las `data/teoria/*.md` en `SHELL`.
  **Al editar cualquier `.md` o `js/markdown.js`/`css/styles.css` hay que subir
  `const VERSION` en `sw.js`** (va por `cogitoergosum-vNN`) para invalidar caché.
- **Sitio público:** https://imgoingsavage.github.io/cogitoergosum/ (repo
  `ImGoingSavage/cogitoergosum`, GitHub Pages desde `main`). **Se commitea y
  pushea directo a `main`** (es la convención del repo y dispara el deploy).

---

## 2. El fix de render (YA HECHO — no rehacer)

`js/markdown.js` no soportaba matemáticas ni enlaces. Se añadió (vanilla, sin
librerías):
- **`texAUnicode(tex)`**: traductor ligero LaTeX→Unicode (`\frac`, `\sqrt`,
  `\sum`, `^{}`/`_{}`→`<sup>`/`<sub>`, `\begin{cases}`, ~150 símbolos/griegas).
- En `inline()`: `$…$` inline → `<span class="matematica">`; `$$…$$` → bloque
  centrado `<div class="ecuacion">`. **Lookahead `(?![0-9\s])`** evita romper
  cantidades en dólares (`$4M`, `$100`).
- Enlaces de concepto `[[slug]]` / `[[slug|etiqueta]]` → chip
  `<span class="enlace-concepto">` (de-slugged; SIN navegación todavía — el
  resolver es trabajo futuro). Los **literales de matriz** `[[1,3],[2,6]]` se
  dejan crudos a propósito.
- CSS en `css/styles.css`: `.matematica`, `.ecuacion`, `.enlace-concepto`.

**Limitación conocida:** `$$…$$` **multi-línea no está soportado** (todos los
actuales son de una sola línea). Si escribes una ecuación de varias líneas,
ponla en una sola línea `$$...$$`.

---

## 3. Estado EXACTO del plan (al 2026-06-15)

**118 / 118 lecciones enriquecidas — OLEADA 2 COMPLETA.** Clusters COMPLETOS:

| Cluster | Lecciones (todas hechas) |
|---|---|
| **Health AI / causal** | arena-h1 … h22 (22 — cluster completo) |
| **ML Systems** | rom1-4, rml1-4, dmls1-4, htd1-4, sre1-4, mldp1-4, obs1-4, iml1-4 (32) |
| **MAANG** | cc1-4, sd1-4, m1, m2 (10) |
| **Quant núcleo (lotes 11-12,20)** | q1 … q13 (12 — cluster completo) |
| **Blitzstein (lote 13)** | b1, b2, b3, b4 (4) |
| **Inferencia clásica (lotes 14-15)** | dg1-4 (DeGroot) + cb1-4 (Casella & Berger) (8) |
| **Estadística aplicada (lotes 16-17)** | pst1-4 (Practical Statistics) + isl1-4 (ISLP) (8) |
| **Ciencia de datos (lotes 18-19)** | ads1-4 + cds1-4 + s1 (9) |
| **Health originales (lote 20)** | h1, h2 (2) |
| **Conductual (lote 21)** | c1, c2, c3, c4 (STAR) (4) |
| **Fifty Challenging (lote 22)** | fc1, fc2, fc3, fc4 (4) |
| **A Practical Guide (lote 23)** | p1, p2, p3, p4 (4) |

### FALTAN: 0 lecciones — ✅ las 118 contienen "Transferencia isomorfa"

Verificación (debe imprimir vacío):
```bash
comm -23 \
  <(ls data/teoria/arena-*.md | sed 's#data/teoria/##;s#.md##' | sort) \
  <(grep -l "Transferencia isomorfa" data/teoria/arena-*.md | sed 's#data/teoria/##;s#.md##' | sort)
```

**La Oleada 2 (enriquecimiento por lotes) está terminada.** Lo que sigue es
**Oleada 3** (§7): resolver `[[wiki-links]]` para hacerlos navegables, render de
`$$` multi-línea si aparece la necesidad, metadata de heurísticas en `banco[]`
(requiere migración de esquema → consultar a Edgar antes), y rúbricas/simulación
de entrevista (Nivel E). NO empieces Oleada 3 sin que lo pidan.

Agrupadas por sub-libro (mira `data/study.json` campo `libro` de cada unidad
para la fuente; los libros están en `Arena/` y `Biblioteca/` y **se pueden citar
sin problema de copyright**, ver `<permisos>` de `auditoria.md`):

**Quant / probabilidad (route: quant):**
- ~~`arena-q1` (toque ligero: Transferencia + Errores típicos)~~ **HECHA (lote 20)**.
- ~~`arena-q2 … q11, q13` (Quant núcleo, lotes 11-12)~~ **HECHAS — cluster
  completo**.
- ~~`arena-p1, p2, p3, p4` (A Practical Guide to Quantitative Finance)~~ **HECHAS
  (lote 23)** — cierre de la Oleada 2.
- ~~`arena-fc1, fc2, fc3, fc4` (Fifty Challenging Problems)~~ **HECHAS (lote 22)**.
- ~~`arena-b1, b2, b3, b4` (Blitzstein & Hwang)~~ **HECHAS (lote 13)**.

**Estadística / inferencia (route: estadistica/quant):**
- ~~`arena-dg1, dg2, dg3, dg4` (DeGroot & Schervish)~~ **HECHAS (lote 14)**.
- ~~`arena-cb1, cb2, cb3, cb4` (Casella & Berger)~~ **HECHAS (lote 15)**.
- ~~`arena-pst1, pst2, pst3, pst4` (Practical Statistics)~~ **HECHAS (lote 16)**.
- ~~`arena-isl1, isl2, isl3, isl4` (ISLP)~~ **HECHAS (lote 17)**.

**Ciencia de datos (route: ciencia-datos / ml-systems):**
- ~~`arena-ads1, ads2, ads3, ads4` (Ace the DS Interview)~~ **HECHAS (lote 18)**.
- ~~`arena-cds1, cds2, cds3, cds4` (Cracking the DS Interview)~~ **HECHAS (lote 19)**.
- ~~`arena-s1` (Huyen — skew, drift, rollout)~~ **HECHA (lote 19)**.

**Conductual (route: conductual):**
- ~~`arena-c1, c2, c3, c4` (Build a Career in Data Science — STAR)~~ **HECHAS
  (lote 21)**: toque ligero (errores típicos + transferencia hacia clusters técnicos).

**Originales sueltos (route: health-ai-rwe):**
- ~~`arena-h1` (DAGs/adjustment sets), `arena-h2` (target trial/immortal time)~~
  **HECHAS (lote 20)** — el cluster Health (h1-h22) queda completo.

> Cómo recomputar esta lista en cualquier momento (la marca de "hecha" es que el
> archivo contiene la cadena `Transferencia isomorfa`):
> ```bash
> cd <repo>
> comm -23 \
>   <(ls data/teoria/arena-*.md | sed 's#data/teoria/##;s#.md##' | sort) \
>   <(grep -l "Transferencia isomorfa" data/teoria/arena-*.md | sed 's#data/teoria/##;s#.md##' | sort)
> ```

---

## 4. LA PLANTILLA (cómo enriquecer — exacta y validada)

Para cada lección: **lee el archivo entero**, localiza el closer `## Disparadores`
(o, en las pocas que usan otro nombre, `## Señales de reconocimiento y jugadas`)
e **inserta JUSTO ANTES** estos bloques (en este orden). Conserva intactos los
closers existentes (Disparadores / Síntesis / Retrieval).

```markdown
## Mini-ejemplo trabajado: <título concreto>

<Un caso pequeño manipulable a mano, con NÚMEROS SIMPLES y desarrollo paso a paso.
Explica el razonamiento, no solo el resultado. Cierra con una **predicción/forcejeo
socrático**: "Predicción antes de seguir: ¿...?" + respuesta breve.>

## Prototipo, contraejemplo y caso borde

- **Prototipo:** <caso donde la idea aplica limpiamente>
- **Contraejemplo:** <parece aplicar pero NO; el patrón tentador equivocado>
- **Caso borde:** <situación extrema que revela la condición oculta>

## Errores típicos

- **Conceptual:** <...>
- **Técnico:** <...>
- **De interpretación / de supuestos:** <...>

## Transferencia isomorfa

<2-4 viñetas "X ↔ Y": la MISMA estructura profunda en OTRO dominio, con un enlace
[[arena-zzz]] real cuando exista. Esta sección es OBLIGATORIA — es el corazón de
la Fase 7 (originalmente 0/118 la tenían).>

Moraleja de la arista: *<una frase que comprime la lección como chunk reutilizable>.*
```

### Reglas de calidad NO negociables (de `auditoria.md`)
1. **Solo inserciones. Nunca borres contenido curado.** El `git diff` de cada
   `.md` debe ser `+N, -0`.
2. **Anti-relleno:** cada párrafo nuevo debe fabricar una arista (intuición,
   ejemplo, error, señal, transferencia, contraejemplo, moraleja). Si no, fuera.
3. **Intuición/ejemplo antes que fórmula.** Números simples siempre que se pueda.
4. **Forcejeo antes de la solución** (la "Predicción antes de seguir").
5. **Aristas explícitas y cruzadas entre clusters** (lo más valioso): p. ej.
   importance sampling ↔ IP weighting `[[arena-h5]]`; concept drift ↔ prediction
   bias `[[arena-htd4]]`; odds ratio ↔ HR de Cox `[[arena-h8]]`; tasa base ↔
   `[[arena-q2]]`; fanout write/read ↔ batch/online `[[arena-dmls3]]`.
6. **`[CAJA NEGRA OK]`** para matemática avanzada que bloquearía (Cox partial
   likelihood, martingalas, etc.): di qué asumir, por qué, qué sí razonar, la
   intuición mínima, y cuándo reabrir la caja. (Ejemplo ya hecho en `arena-h8`.)
7. **Math en Unicode plano** cuando sea simple (E[X+Y], σ², ≤); usa `$…$`/`$$…$$`
   solo si de verdad lo necesitas (el renderer ya los soporta, una sola línea).
8. Cada lección, tras enriquecer, debe permitir: entender la intuición, saber
   cuándo usar la herramienta, reconstruir un caso pequeño, detectar errores
   típicos, ver una transferencia isomorfa y recordar una moraleja.

### Ejemplares ya hechos para imitar el tono y la profundidad
- Causal/Health: `data/teoria/arena-h17.md`, `arena-h13.md` (PPV/tasa base).
- ML Systems: `data/teoria/arena-htd1.md` (CACE), `arena-sre4.md` (cascada).
- MAANG: `data/teoria/arena-cc3.md` (DP/coin change), `arena-sd2.md` (consistent
  hashing).
- Modelo de lección "nativa estudiable" (referencia de estilo): `arena-q1.md`.

---

## 5. WORKFLOW por lote (sigue esto al pie de la letra)

Trabaja en **lotes de 5-8 lecciones** (típicamente un sub-libro completo, p. ej.
`arena-b1..b4` o `arena-dg1..dg4`). Por lote:

1. **Lee** los archivos del lote enteros (tool Read; un `cat` por Bash NO cuenta
   para poder editar — el editor exige Read previo del archivo).
2. **Enriquece** cada uno con la plantilla (Edit, insertando antes del closer).
3. **Valida render** (debe dar `threw=0 rawDisplayMath=0`; `rawLinks` puede ser
   >0 por literales de matriz):
   ```bash
   node scripts/smoke-teoria.mjs
   # opcional, comprueba secciones por lección:
   node scripts/smoke-teoria.mjs arena-b1 arena-b2 arena-b3 arena-b4
   ```
4. **Verifica que son solo inserciones:**
   ```bash
   git diff --stat data/teoria/arena-b1.md ... | tail -1   # debe ser "+N, -0"
   ```
5. **Sube la versión del service worker** (una vez por lote):
   ```bash
   # editar sw.js: const VERSION = 'cogitoergosum-vNN'  (incrementa NN)
   node --check sw.js
   ```
   (Versión actual al cerrar esta tanda: ver `grep VERSION sw.js`. Iba en v63.)
6. **Commit + push a `main`** (mensaje en español, estilo del repo):
   ```bash
   git add sw.js data/teoria/arena-b1.md data/teoria/arena-b2.md ...
   git commit -F - <<'EOF'
   Auditoría Fase 7 · Oleada 2 lote N: <cluster/libro> (sw.js vNN)

   Enriquecidas K lecciones (solo inserciones, closers intactos): ...
   Mini-ejemplos: ...  Transferencia isomorfa con aristas: [[...]] ...
   Validado: 118/118 renderizan sin excepción, 0 con $$ crudo.

   Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
   EOF
   git push origin main
   ```
7. **Actualiza la sección §3 de ESTE archivo** (marca el lote como hecho) y
   commitéalo, para que el registro siga vivo.

---

## 6. Orden sugerido de los lotes restantes

1. **Quant núcleo:** `arena-q2..q11, q13` (probabilidad/Bayes/derivadas/estocásticos).
   Empieza por `q2` (Bayes/tasa base) — es referencia de muchas aristas.
2. **Blitzstein:** `arena-b1..b4` (fundamentos, conjuntas, distribuciones, Markov).
3. **Inferencia clásica:** `arena-dg1..dg4` y `arena-cb1..cb4`.
4. **Estadística aplicada / ML estadístico:** `arena-pst1..pst4`, `arena-isl1..isl4`.
5. **Ciencia de datos:** `arena-ads1..ads4`, `arena-cds1..cds4`, `arena-s1`.
6. **Quant largas:** `arena-p1..p4`, `arena-fc1..fc4` (200+ líneas; cuida no
   inflar — solo inserta las secciones del contrato).
7. **Originales Health:** `arena-h1`, `arena-h2`.
8. **Conductual (prioridad baja):** `arena-c1..c4`.
9. **`arena-q1`:** solo añadir Transferencia isomorfa + Errores típicos (ya es
   estudiable; no reescribir).

---

## 7. Oleada 3 (en curso desde 2026-06-15 — solo si lo piden)

- ✅ **Resolver `[[wiki-links]]` (HECHO, sw.js v77, commit `fa4d02b`):** los
  `[[arena-xxx]]` ahora son navegables. `js/markdown.js` los emite como
  `<a class="enlace-unidad" data-unidad="…">` (con `data-auto` cuando no traen
  etiqueta); `js/study.js` (`cablearEnlacesLeccion` / `navegarAUnidad`) pone el
  título real de la unidad, marca rotos (`.enlace-roto`) y al click/Enter abre la
  unidad destino (haciendo visible su bloque si hace falta) y su lección. CSS
  `.enlace-unidad` en `css/styles.css`. Los `[[concepto-sin-unidad]]` siguen como
  chip `.enlace-concepto`; los literales de matriz `[[1,3],…]` intactos. Verificado:
  93 targets únicos resuelven a unidades de `study.json`, 0 rotos.
- 🟢 **Taxonomía aplicada + simulación de entrevista POR ÁREA (Nivel E) — HECHO
  (sw.js v79, commit `39f606f`).** Edgar pidió aplicar la taxonomía propuesta
  (auditoria.md Fase 3) y montar la simulación SOBRE ella (rondas por cluster, no
  por unidad). **No toca `study.json`**; todo vive en `data/entrevista/`:
  - `_taxonomia.json`: **8 clusters = 8 rondas**, cada uno con `track`,
    `descripcion` (por qué existe) y la lista de `unidades`. Particiona las 118 sin
    solape: quant-prob (25), stats-inf (16), dsa (6), system-design (4), ds-applied
    (9), ml-systems (32), causal-health (22), conductual (4). *(El mapeo se computa
    de `study.json` por ruta + prefijo de id; ver el script en el commit.)*
  - `cluster-<id>.json` ×8: guion de cada ronda. Esquema
    `{ rol, duracion, preguntas:[{q, rubrica[], errores[], seguimiento?}], cierre }`.
  - UI: tarjeta `#estudio-entrevista` "Simulación de entrevista por área", visible
    solo en el bloque `fase-7`; lista las rondas y abre su guion. `js/study.js`
    (`renderEntrevistaTaxonomia` desde `renderizar()`, `abrirSimCluster`,
    `construirEntrevista`), `index.html` (`#estudio-entrevista`/`#entrevista-clusters`/
    `#entrevista-sim`), CSS `.entrevista*`. La versión previa por-unidad (botón en el
    panel de unidad + `_index.json` + 3 JSON `arena-*`) se retiró (`git rm`).
  - **Pendiente de iterar tras review:** los 8 guiones tienen 3-4 preguntas cada uno
    (cobertura representativa, no exhaustiva); se pueden profundizar/ampliar. Para
    añadir un cluster nuevo: archivo `cluster-<id>.json` + entrada en `_taxonomia.json`
    + línea en el SHELL de `sw.js`.
- ✅ **Vista Estudio de fase-7 agrupada por taxonomía (UI/UX) — HECHO (sw.js v80).**
  Edgar pidió que la vista Estudio del bloque Arena no muestre las 118 lecciones en
  lista plana desordenada, sino **solo las 8 categorías** de la taxonomía, cada una
  colapsable; al desplegar muestra sus unidades **en orden didáctico** + el botón de
  simulación de su ronda. **No toca `study.json`.** Cambios:
  - `data/entrevista/_taxonomia.json`: el `unidades[]` de cada cluster se reordenó a
    **secuencia didáctica** (articulación vertical: los temas iniciales sostienen a
    los del final) y se añadió el campo `secuencia` (frase que describe ese arco).
    La partición de las 118 sin solape se mantiene (validado).
  - `js/study.js`: `renderizar()` ahora, si el bloque es `fase-7` y hay taxonomía,
    llama `renderClustersFase7()` (acordeones) en vez de la lista plana; las demás
    fases siguen con lista plana. Helper `crearUnidadItem(u,b)` (extraído, reutilizado
    en ambos modos). `crearClusterAcordeon()` pinta cabecera (chevron + título + chip
    de track + progreso `k/N`) y cuerpo colapsable (descripción, `secuencia`, unidades,
    y el botón+panel de simulación). Estado de despliegue en memoria
    (`clustersExpandidos`, todas colapsadas al cargar; `navegarAUnidad` despliega la
    categoría destino). `abrirSimCluster(clusterId, btn, panel)` ahora recibe su panel
    (cada categoría tiene el suyo). Se retiró `renderEntrevistaTaxonomia` y el uso de
    los IDs `#estudio-entrevista`/`#entrevista-clusters`/`#entrevista-sim`.
  - `index.html`: se eliminó la tarjeta suelta `#estudio-entrevista` (la simulación
    vive ahora dentro de cada acordeón).
  - `css/styles.css`: estilos `.estudio-clusters`/`.cluster-acordeon`/`.cluster-cabecera`/
    `.cluster-chevron`/`.cluster-cuerpo`/`.cluster-secuencia`/`.cluster-sim-wrap`/
    `.entrevista-launch` (se reemplazaron los antiguos `.entrevista-cluster-*` y
    `#entrevista-sim`). Se conserva `.entrevista*` del guion de simulación.
  - **Pendiente de iterar:** el orden didáctico es un juicio pedagógico revisable;
    densificar los 8 guiones sigue disponible (ver punto anterior).
- ✅ **KaTeX vendorizado local (render de matemáticas calidad de libro) — HECHO
  (sw.js v81).** Edgar pidió que las expresiones se vean "como en el libro". Se
  vendoriza KaTeX 0.16.11 self-hosted (sin CDN, offline/PWA) en `assets/katex/`
  (`katex.min.js` UMD → `window.katex`, `katex.min.css` recortado a woff2-only,
  20 fuentes). `js/markdown.js` renderiza `$…$`/`$$…$$` con KaTeX (`strict:false`,
  `throwOnError:false`) y cae a `texAUnicode` si KaTeX no cargó (p. ej. el smoke en
  Node). `index.html` carga css+js en `<head>`; `sw.js` precachea todo en SHELL.
  - **CAMBIO DE CONVENIO (clave para el siguiente agente):** `$…$` es **siempre
    matemática**; la **moneda se escribe `\$`** (`\$4M`, `\$100`). Se quitó el viejo
    guard anti-`$100` (rompía toda math que empezara con dígito: `$3/6$`, `$2^n$`).
    Al escribir lecciones nuevas usa `\$` para dólares. Migrada la moneda cruda a
    `\$` en las lecciones que la usaban (q5, h21, pst4, rom4, htd3, sre4).
  - **Verificación:** las 118 lecciones renderizan en KaTeX sin throw. Script ad-hoc:
    extrae `$…$`/`$$…$$` (protegiendo `\$`) y corre `katex.renderToString(...,
    {throwOnError:true, strict:false})`; debe dar 0 throws.
- ✅ **Cluster 1 (quant-prob) reescrito DESDE CERO — HECHO (sw.js v82-v87).** Edgar
  pidió que cada lección asuma conocimiento nulo y construya desde ahí (auditoria.md:
  espina conceptual → intuición/analogía → fórmula con símbolos explicados → mini-caso
  → prototipo/contraejemplo/borde → errores → forcejeo → transferencia → moraleja),
  con math en LaTeX. **Las 25 lecciones del cluster quant-prob** quedaron reescritas
  (contenido original, sin reproducir texto de los libros; se conservó todo lo curado):
  b1, p1, q1, q2 (lote 1, v82); p2, fc1, b2, b3 (lote 2, v83); q10, fc2, q4, q9 (lote
  3, v84); fc3, q3, q12, q13 (lote 4, v85); q8, fc4, b4, p3 (lote 5, v86); q11, p4,
  q5, q7, q6 (lote 6, v87). q1/q2 ya eran fuertes: solo se les insertó la espina de
  arranque desde cero. **Pendiente:** replicar el mismo trabajo en los otros 7 clusters
  (stats-inf, dsa, system-design, ds-applied, ml-systems, causal-health, conductual)
  cuando Edgar lo pida — son otra oleada.
- ✅ **Cluster 5 (ds-applied) reescrito DESDE CERO — HECHO (sw.js v88-v90).** Edgar
  eligió este cluster como siguiente (2026-06-15). Patrón observado: estas lecciones
  ya traían el tratamiento de Oleada 2 (mini-ejemplo, prototipo/contraejemplo, errores,
  transferencia, disparadores, síntesis, retrieval) — todo eso se **conserva verbatim**;
  lo que se reescribe es la **mitad superior** (el núcleo teórico) al estándar from-zero:
  espina "De qué trata… y qué sabrás hacer", intuición/analogía ANTES de cada fórmula,
  cada símbolo explicado, y forcejeo socrático intercalado en el cuerpo. **Lote 1 (v88):**
  `ads1` (probabilidad DS), `ads2` (estadística e inferencia), `ads4` (SQL + product
  sense), `cds1` (feature engineering). **Lote 2 (v89):** `ads3` (ML clásico:
  sesgo-varianza, regularización, métricas), `cds2` (deep learning: neurona, activación
  no-lineal, backprop, vanishing gradient), `cds3` (MLOps: pipeline, Docker/K8s, data vs
  concept drift). **Lote 3 (v90):** `s1` (del modelo al sistema: skew, drift, rollback —
  ya muy narrativa; se le añadió espina + intuición, conserva su cierre propio "Señales
  de reconocimiento" + "Ejercicio de consolidación", por eso da `closers:false` en el
  smoke, que es su estado original, no regresión), `cds4` (toolkit: visualización,
  storytelling, pandas, Git/Bash — espina + intuición). Validado: smoke threw=0
  rawDisplayMath=0, KaTeX 0 throws. **Cluster 5 COMPLETO (9/9).** Siguiente cluster
  sugerido por el backlog: `stats-inf` (16), `dsa` (6), `system-design`/`conductual` (4
  c/u), `causal-health` (22), `ml-systems` (32). El patrón de trabajo de este cluster
  (reescribir solo la mitad superior, conservar la inferior curada) aplica a los demás.
- ✅ **Cluster 2 (stats-inf) reescrito DESDE CERO — HECHO (sw.js v91-v94).** Edgar pidió
  seguir con este cluster (2026-06-15). Estas lecciones eran las **más secas**: la mitad
  superior eran fichas de fórmulas en **texto plano/Unicode** (sin LaTeX). El trabajo es
  doble: reescribir el núcleo from-zero **y** pasar la matemática nueva a **LaTeX**
  (`$…$`/`$$…$$`). La mitad inferior curada (mini-ejemplo→retrieval) se conserva verbatim
  (sigue con su Unicode original, que ya pasaba el smoke). Por la densidad matemática se
  usa `[CAJA NEGRA OK]` en los teoremas pesados (Cramér-Rao, Lehmann-Scheffé, Basu,
  equivalencia Wald/LRT/Score): intuición obligatoria, prueba opcional. Hay solape natural
  entre dg1/dg2/cb1/cb2 (suficiencia, MLE, CR, UMVUE) → cada lección se sostiene sola pero
  cruza con [[ ]] para no duplicar. **Lote 1 (v91):** `dg1` (estimación puntual: sesgo,
  MSE, Fisher, CR, suficiencia, MLE, UMVUE — la fundacional), `dg2` (MLE + familias
  exponenciales + OLS=MLE + 3 tests), `cb1` (suficiencia/completitud/Basu), `cb2` (recetas
  MLE/CR/UMVUE + conjugación). Validado: smoke threw=0 rawDisplayMath=0, KaTeX 0 throws.
  **Lote 2 (v92):** `dg3` (IC + tests + p-valor + tamaño muestra + tests múltiples),
  `cb3` (Neyman-Pearson, MLR, UMP, LRT/Wilks, Lindley), `cb4` (pivotes, inversión de
  tests, **delta method**, transformaciones estabilizadoras), `dg4` (teoría de decisión,
  James-Stein, regresión/Gauss-Markov, ridge/lasso, logística, ANOVA, AIC/BIC). Validado:
  smoke threw=0 rawDisplayMath=0, KaTeX 0 throws. **Pendiente:** lote 3 (`pst1-4`,
  Practical Statistics — EDA/bootstrap/permutación/regresión), lote 4 (`isl1-4`, ISL —
  marco/sesgo-varianza/regresión/regularización/árboles). Orden en el backlog.
- **Nota de calibración (lote 3, v93):** las `pst*` (Practical Statistics) NO eran fichas
  secas como dg/cb — ya estaban en buen estilo narrativo, con intuición y poca fórmula.
  Para esas, el trabajo from-zero fue **solo añadir la espina** "De qué trata… y qué sabrás
  hacer" (toque ligero, sin relleno: anti-relleno manda), no reescribir el cuerpo. **Lote 3
  (v93):** `pst1` (EDA: robustez, punto de ruptura), `pst2` (distribución muestral,
  bootstrap, SE∝1/√n), `pst3` (A/B + test de permutación, multiplicidad), `pst4` (regresión:
  multicolinealidad/confounding/interacción + diagnóstico por residuales). Validado: smoke
  threw=0, KaTeX 0 throws. **Lote 4 (v94):** `isl1` (marco Y=f(X)+ε, sesgo-varianza, KNN),
  `isl2` (regresión lineal + clasificación logística/LDA/QDA), `isl3` (remuestreo,
  selección, ridge/lasso), `isl4` (no linealidad/splines, árboles/RF/boosting, SVM, no
  supervisado) — como las `pst`, ya estaban bien escritas con intuición y LaTeX, solo se
  les añadió la espina from-zero. Validado: smoke threw=0, KaTeX 0 throws. **Cluster 2
  COMPLETO (16/16).** Hechos hasta ahora: ds-applied (9) + stats-inf (16) = 50/118.
  **Siguiente cluster** sugerido: `dsa` (6) o `system-design`/`conductual` (4), luego
  `causal-health` (22) y `ml-systems` (32, el más grande). Patrón: clusters teóricos
  (dg/cb) = reescritura fuerte + math a LaTeX; clusters narrativos (pst/isl) = solo espina.
- ✅ **Cluster 7 (causal-health) reescrito DESDE CERO — HECHO (sw.js v95-v99).** Edgar pidió
  entrar a causal-health y luego ml-systems (2026-06-15). **Restricción dura:** nada
  clínico/diagnóstico en el contenido (ver `<restricciones_clinicas_y_eticas>` de
  `auditoria.md`); las lecciones usan ejemplos de fármaco/recuperación como ilustración
  causal, no como consejo médico — mantenerlo así. Calibración: estas lecciones (como
  pst/isl) ya están bien escritas, narrativas y con poca matemática → el trabajo from-zero
  es **solo añadir la espina** "De qué trata… y qué sabrás hacer", no reescribir el cuerpo.
  Varias usan cierre propio "Señales de reconocimiento" + "Ejercicio de consolidación"
  (como `s1`), por lo que dan `closers:false` en el smoke — es su estado original, NO
  regresión. **Lote 1 (v95):** `h15` (escalera de Pearl), `h16` (junciones/paradojas),
  `h1` (DAGs/adjustment sets), `h17` (do-operator/back-door/front-door/do-calculus).
  **Lote 2 (v96):** `h3` (resultados potenciales, 3 condiciones de identificación),
  `h19` (Mixtape: sesgo de selección, ATE/ATT/ATU, SUTVA), `h4` (sesgos estructurales:
  confundimiento/selección/medición, d-separación), `h18` (contrafactuales/SCM, mediación
  NDE/NIE, PN/PS). **Lote 3 (v97):** `h5` (IP weighting/g-fórmula/PS/IV/doble robustez),
  `h20` (Mixtape: matching/subclasificación/PS, CIA), `h21` (IV/2SLS y RDD), `h22`
  (panel/efectos fijos, DiD, control sintético). Validado: smoke threw=0, KaTeX 0 throws.
  **Lote 4 (v98):** `h2` (target trial + immortal time bias), `h6` (longitudinal/supervivencia
  causal/g-métodos/ITT-PP), `h7` (KM + log-rank), `h8` (Cox + supuesto PH). Validado: smoke
  threw=0, KaTeX 0 throws. **Lote 5 (v99):** `h9` (Cox extendido/paramétricos/AFT), `h10`
  (recurrentes/riesgos competitivos/CIF), `h11`-`h14` (OHDSI: OMOP CDM, vocabularios/ETL/DQ,
  analítica/cohortes/PLP, validez/controles negativos/estudios en red). Validado: smoke
  threw=0, KaTeX 0 throws. **Cluster 7 COMPLETO (22/22).** Hechos: ds-applied (9) +
  stats-inf (16) + quant-prob (25) + causal-health (22) = 72/118. **Siguiente y último gran
  cluster: `ml-systems` (32)** — el más grande; ya quedan dsa (6), system-design (4) y
  conductual (4) como cortos. Patrón confirmado: clusters narrativos (pst/isl/h*) = solo
  espina; clusters de fichas secas (dg/cb) = reescritura + math a LaTeX. Revisar el estilo
  de cada lección de ml-systems antes de decidir el nivel de trabajo.
- ✅ **Cluster 6 (ml-systems) reescrito DESDE CERO — HECHO (sw.js v100-v106).** Edgar pidió
  hacerlo tras causal-health (2026-06-15). Es el cluster **más grande (32)**. Estilo: como
  pst/isl/h*, ya están bien escritas y narrativas → trabajo from-zero = **solo añadir la
  espina** "De qué trata… y qué sabrás hacer" (sin reescribir cuerpo; anti-relleno). **Lote 1
  (v100):** `rom1` (Reglas de ML Google I: antes del ML/primer pipeline), `dmls1` (encuadre
  de problemas/objetivos), `rom2` (Reglas II: primer objetivo/feature eng), `dmls2` (datos de
  entrenamiento: muestreo/labels/desbalance). Validado: smoke threw=0, KaTeX 0 throws.
  **Lote 2 (v101):** `mldp1` (patrones de representación: hashed/embeddings/cross/reframing),
  `rml2` (datos como pasivo, anonimización, confiabilidad), `mldp2` (ensembles/cascada/clase
  neutra/rebalanceo), `mldp3` (patrones de entrenamiento y serving).
  **Lote 3 (v102):** `rom4` (Reglas IV Fase III), `dmls3` (despliegue batch/online,
  compresión, edge), `rml3` (serving/monitoreo/observabilidad), `rom3` (Reglas III: análisis
  humano, training-serving skew), `dmls4` (shifts covariate/label/concept, test en prod),
  `rml1` (confiabilidad e2e, SLOs por capa). **Lote 4 (v103):** `sre1` (riesgo/error budget/
  SLOs), `sre2` (toil/4 señales doradas), `sre3` (troubleshooting/ICS/postmortems sin culpa),
  `sre4` (releases/simplicidad/sobrecarga/cascada). **Lote 5 (v104):** `rml4` (respuesta a
  incidentes ML: Public/Fuzzy/Unbounded), `obs1` (monitoreo vs observabilidad, cardinalidad),
  `obs2` (eventos anchos/trazas/Core Analysis Loop), `obs3` (SLO alerts/burn alerts), `obs4`
  (escala: columnar/muestreo/OMM). **Lote 6 (v105):** `htd1` (deuda ML: CACE/cascadas/
  undeclared consumers), `htd2` (dependencias de datos/feedback loops), `htd3` (anti-patrones:
  glue code/pipeline jungles/dead codepaths/config), `htd4` (mundo externo/prediction bias).
  **Lote 7 FINAL (v106):** `mldp4` (reproducibilidad + IA responsable), `iml1` (interpretabilidad:
  conceptos/taxonomía/buenas explicaciones), `iml2` (modelos intrínsecos), `iml3` (métodos
  agnósticos PDP/ICE/ALE/permutación), `iml4` (LIME/SHAP/contrafactuales). **Cluster 6
  COMPLETO (32/32).** Hechos: quant-prob (25) + ds-applied (9) + stats-inf (16) + causal-health
  (22) + ml-systems (32) = **104/118**. **Pendiente: solo 3 clusters cortos:** `dsa` (6),
  `system-design` (4), `conductual` (4). Revisar su estilo: probablemente narrativos (solo
  espina) salvo `dsa` que puede tener algo de pseudocódigo/complejidad. Mismo workflow por lote.
- ✅ **Cluster 3 (dsa) reescrito DESDE CERO con EMPEÑO — HECHO (sw.js v107).** Edgar pidió
  esfuerzo extra aquí (2026-06-15): no solo espina, **reescritura profunda** del núcleo
  (como dg/cb de stats-inf), porque la mitad superior era fichas secas con pseudocódigo.
  Tratamiento: espina + intuición ANTES de cada estructura/algoritmo + ejemplos trabajados
  a mano + complejidad razonada + forcejeo socrático, **todo en prosa ORIGINAL** (el prompt
  prohíbe reproducir texto de los libros literal/casi-literal aunque estén comprados; se
  enseña el mismo material con fraseo propio). Math a LaTeX donde aplica. **Lote único (v107):**
  `cc1` (arrays/hash/sliding window/two pointers — además se reformateó el literal de matriz
  `[[1,3],…]` a bloque de código → **rawLinks ahora 0** en todo el corpus, y se arregló un
  enlace roto a `[[arena-h20]]`), `m1` (patrones de hash + ciclo de Floyd), `cc4` (ordenamiento/
  binaria sobre la respuesta/heaps/XOR), `cc2` (BFS/DFS/topo sort/Dijkstra/Union-Find/Trie),
  `cc3` (DP: estado/recurrencia/knapsack/LCS), `m2` (SQL window functions). m1/m2 conservan
  su cierre propio (Señales/Ejercicio) → `closers:false`/`Mini:false` en el smoke, su estado
  original. Validado: smoke threw=0 rawDisplayMath=0 rawLinks=0, KaTeX 0 throws.
- Render de `$$` multi-línea si aparece la necesidad. *(Pendiente — hoy 0 casos en el corpus.)*
- Metadata de heurísticas por problema en `banco[]` (requiere migración de
  esquema → consultar a Edgar antes). *(Pendiente — gated.)*

---

## 8. Lo que NO debes hacer

- No borres ni reescribas contenido existente (solo inserta).
- No edites `data/study.json` ni el `banco[]` (a menos que lo pidan).
- No metas dependencias ni frameworks (es vanilla HTML/CSS/JS, PWA, Pages).
- No olvides subir `VERSION` en `sw.js` por lote (si no, el iPad sirve caché vieja).
- No incluyas información clínica/diagnóstica en el contenido (ver
  `<restricciones_clinicas_y_eticas>` de `auditoria.md`).
- No commitees los PDFs/manuales sueltos del working dir (`*.pdf`, `arena.md`,
  `prompt.md`, `.claude/settings.local.json`): no son parte de esta tarea.
