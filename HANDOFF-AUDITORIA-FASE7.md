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

**78 / 118 lecciones enriquecidas.** Clusters COMPLETOS:

| Cluster | Lecciones (todas hechas) |
|---|---|
| **Health AI / causal** | arena-h3 … h22 (20) |
| **ML Systems** | rom1-4, rml1-4, dmls1-4, htd1-4, sre1-4, mldp1-4, obs1-4, iml1-4 (32) |
| **MAANG** | cc1-4, sd1-4, m1, m2 (10) |
| **Quant núcleo (lotes 11-12)** | q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q13 (11) |
| **Blitzstein (lote 13)** | b1, b2, b3, b4 (4) |
| Muestra Oleada 1 | q12 (+cc1, h17 ya contados arriba) |

### FALTAN (40 lecciones) — esto es lo que debes hacer

Agrupadas por sub-libro (mira `data/study.json` campo `libro` de cada unidad
para la fuente; los libros están en `Arena/` y `Biblioteca/` y **se pueden citar
sin problema de copyright**, ver `<permisos>` de `auditoria.md`):

**Quant / probabilidad (route: quant):**
- `arena-q1` *(ojo: ya nació estudiable, solo añádele la sección **Transferencia
  isomorfa** + Errores típicos; no la reescribas)*
- ~~`arena-q2 … q11, q13` (Quant núcleo, lotes 11-12)~~ **HECHAS — cluster
  completo**.
- `arena-p1, p2, p3, p4` (A Practical Guide to Quantitative Finance — acertijos,
  combinatoria, brownian, álgebra lineal). **Son MUY largas (200+ líneas)**.
- `arena-fc1, fc2, fc3, fc4` (Fifty Challenging Problems in Probability)
- ~~`arena-b1, b2, b3, b4` (Blitzstein & Hwang)~~ **HECHAS (lote 13)**.

**Estadística / inferencia (route: estadistica/quant):**
- `arena-dg1, dg2, dg3, dg4` (DeGroot & Schervish)
- `arena-cb1, cb2, cb3, cb4` (Casella & Berger — Statistical Inference)
- `arena-pst1, pst2, pst3, pst4` (Practical Statistics for Data Scientists)
- `arena-isl1, isl2, isl3, isl4` (ISLP — Introduction to Statistical Learning)

**Ciencia de datos (route: ciencia-datos / ml-systems):**
- `arena-ads1, ads2, ads3, ads4` (Ace the Data Science Interview)
- `arena-cds1, cds2, cds3, cds4` (Cracking the Data Science Interview)
- `arena-s1` (Huyen — "del modelo al sistema": skew, drift, rollout)

**Conductual (route: conductual):**
- `arena-c1, c2, c3, c4` (Build a Career in Data Science — STAR). *Formato STAR
  ya es bastante adecuado; prioridad BAJA. Probablemente solo necesiten
  Transferencia isomorfa ligera o pueden quedarse como needs_review.*

**Originales sueltos (route: health-ai-rwe):**
- `arena-h1` (DAGs y adjustment sets), `arena-h2` (target trial / immortal time).
  *Son los originales cortos del bloque; mismo tratamiento que h3-h22.*

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

## 7. Oleada 3 (futuro, NO ahora — solo si lo piden)

- Resolver `[[wiki-links]]`: hacerlos navegables (hoy son chips no clicables).
- Render de `$$` multi-línea si aparece la necesidad.
- Metadata de heurísticas por problema en `banco[]` (requiere migración de
  esquema → consultar a Edgar antes).
- Rúbricas / simulación de entrevista (Nivel E) si el esquema lo soporta.

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
