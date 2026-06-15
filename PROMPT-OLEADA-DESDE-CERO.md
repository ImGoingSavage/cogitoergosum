# PROMPT para el siguiente agente — Oleada "lecciones desde cero" (pégalo tal cual)

---

Vas a continuar la **auditoría pedagógica de la Fase 7** (Arena de Entrevistas de
Élite) de **CogitoErgoSum** (web app local-first, HTML/CSS/JS vanilla, sin
frameworks, PWA en GitHub Pages; repo `ImGoingSavage/cogitoergosum`, se pushea
directo a `main`). La memoria de Claude NO cruza de cuenta: **todo lo que necesitas
está en el repo**.

## Tu tarea

Reescribir las lecciones de teoría de la Fase 7 (`data/teoria/arena-*.md`) para que
**asuman conocimiento nulo del estudiante y construyan desde ahí**, siguiendo el
contrato de `auditoria.md`, con la matemática en **LaTeX** (la renderiza KaTeX, ya
vendorizado). El **cluster 1 (quant-prob, 25 lecciones) ya está hecho** y sirve de
referencia de tono y profundidad. Te toca **replicar exactamente el mismo
tratamiento en los otros 7 clusters** (93 lecciones), un cluster a la vez.

**El estado, el orden didáctico y el checklist por unidad viven en
`BACKLOG-OLEADA-DESDE-CERO.md`.** Empieza por ahí.

## Antes de tocar nada, lee en este orden

1. `BACKLOG-OLEADA-DESDE-CERO.md` — qué falta, en qué orden, checklist por unidad.
2. `auditoria.md` — el contrato de calidad de las lecciones (es la especificación).
3. `HANDOFF-AUDITORIA-FASE7.md` §7 — registro de lo hecho (incl. KaTeX y convenio).
4. `CLAUDE.md` → `HANDOFFCES.md` §0 (Constitución, es LEY: el error nunca castiga,
   cero dinero, IA siempre opcional, anti-dark-patterns).
5. Como **ejemplares del tono y profundidad ya logrados**, lee 3-4 lecciones del
   cluster 1 ya reescritas: `data/teoria/arena-b1.md` (fundamentos, from-zero puro),
   `arena-q11.md` (mate densa con LaTeX), `arena-fc3.md` (paradojas, mate ligera),
   `arena-b3.md` (red de distribuciones).

## El estándar de cada lección (de `auditoria.md`)

Cada lección, **desde conocimiento nulo**, debe llevar (adaptado a su tema):

- **Espina conceptual:** "De qué trata (y qué sabrás hacer)" — la idea central en
  una frase + qué podrá hacer el usuario después.
- **Intuición / analogía / motivación** ANTES de cualquier fórmula.
- **Fórmula** (si aplica) solo tras la intuición, con **cada símbolo explicado**,
  cuándo usarla y cuándo no, y el supuesto que la habilita.
- **Mini-ejemplo trabajado** con números simples, paso a paso, y un **forcejeo
  socrático** ("Predicción antes de seguir: …" + respuesta breve).
- **Prototipo, contraejemplo y caso borde.**
- **Errores típicos** (conceptual / técnico / de interpretación o supuestos).
- **Transferencia isomorfa** con aristas `[[arena-xxx]]` reales a otras unidades.
- **Moraleja** que comprima la lección como chunk reutilizable.
- Conserva los **closers** existentes (Disparadores / Síntesis / Retrieval).

**Anti-relleno (regla dura):** cada párrafo nuevo debe fabricar una arista
(intuición, ejemplo, error, señal, transferencia, contraejemplo, moraleja). Si no,
fuera. No confundas longitud con profundidad.

`[CAJA NEGRA OK]` para matemática avanzada que bloquearía (Cox partial likelihood,
martingalas, backprop completa, teoría de medida): di qué asumir, por qué, qué sí
razonar, la intuición mínima, y cuándo reabrir la caja.

## Reglas innegociables

- **COPYRIGHT:** **redacta explicaciones ORIGINALES** que enseñen el mismo material.
  **No reproduzcas texto de los libros** de `Arena/`/`Biblioteca/` de forma literal
  ni casi-literal (que estén comprados no habilita reproducir su texto). Puedes citar
  ideas, teoremas y datos; el fraseo y los ejemplos son tuyos.
- **No borres contenido curado.** Reescribe envolviendo/expandiendo: al final la
  lección debe conservar todas las fórmulas, tablas, ejemplos, señales, aristas y
  closers que ya tenía. (En el cluster 1, varias lecciones se reescribieron enteras
  con `Write`, pero preservando todo lo valioso.)
- **MATEMÁTICA EN LaTeX, y el convenio de dólar:** `$…$` (inline) y `$$…$$` (bloque)
  son **siempre matemática**; KaTeX las renderiza con calidad de libro. **La moneda
  se escribe `\$`** (`\$4M`, `\$100`) — si pones un `$` crudo antes de un número se
  interpretará como matemática. Usa Unicode plano solo para cosas triviales (≤, σ²);
  para fracciones, integrales, sub/superíndices, matrices, usa LaTeX.
  - KaTeX está vendorizado en `assets/katex/` y cableado en `js/markdown.js`
    (`window.katex`, `strict:false`, fallback a Unicode en Node). **No lo toques.**
  - Evita comandos que KaTeX no soporta (p. ej. `\begin{psmallmatrix}`; usa
    `\big(\begin{smallmatrix}…\end{smallmatrix}\big)`). No metas prosa española
    larga dentro de `$…$` (úsala fuera, o dentro de `\text{…}` para etiquetas cortas).
- **Vanilla puro:** sin librerías nuevas, sin frameworks, sin backend. Compatible con
  GitHub Pages y PWA.
- **NO edites `data/study.json` ni `banco[]`** (los quizzes) salvo que Edgar lo pida.
- **Nada clínico/diagnóstico** en el contenido (ver `<restricciones_clinicas_y_eticas>`
  de `auditoria.md`) — relevante sobre todo en el cluster `causal-health`.
- **PWA/caché:** al cambiar cualquier `.md` (o `js/*`, `css`, `index.html`, `data/*`),
  **sube `const VERSION` en `sw.js`** (va por `cogitoergosum-vNN`; ahora en **v87**).
  No hay archivos `data/` nuevos en esta oleada, así que con subir VERSION basta.
- **NO commitees** los sueltos del working dir: `*.pdf`, `arena.md`, `prompt.md`,
  `.claude/settings.local.json`.

## Workflow por lote (sigue esto)

Trabaja **un cluster a la vez**, en **lotes de 4-5 lecciones**, en el orden didáctico
del backlog. Por lote:

1. **Lee** los `.md` del lote enteros (tool Read; exige Read previo para editar) para
   preservar su contenido curado.
2. **Reescribe** cada uno desde cero según el estándar (con `Write` si es reescritura
   completa, o `Edit` si solo insertas la espina de arranque a una que ya esté fuerte).
   Math en LaTeX, dólares con `\$`.
3. **Valida render** (debe dar `threw=0 rawDisplayMath=0`):
   ```bash
   node scripts/smoke-teoria.mjs            # todas
   node scripts/smoke-teoria.mjs arena-XX arena-YY …   # por lección
   ```
4. **Valida que TODO LaTeX renderiza en KaTeX sin throw** (clave; el smoke usa
   fallback Unicode en Node y NO ejercita KaTeX). Script ad-hoc:
   ```bash
   node -e '
   const fs=require("fs"),katex=require("./assets/katex/katex.min.js");
   const files=fs.readdirSync("data/teoria").filter(f=>f.endsWith(".md"));let n=0;
   for(const f of files){fs.readFileSync("data/teoria/"+f,"utf8").split("\n").forEach((line,i)=>{
     let s=line.replace(/\\\$/g,"\x00");
     const b=[...s.matchAll(/\$\$([^$]+)\$\$/g)].map(m=>({t:m[1],d:true}));
     const inl=[...s.replace(/\$\$[^$]+\$\$/g,"").matchAll(/\$([^$\n]+?)\$/g)].map(m=>({t:m[1],d:false}));
     for(const {t,d} of [...b,...inl]){try{katex.renderToString(t,{displayMode:d,throwOnError:true,strict:false});}catch(e){n++;console.log(f+":"+(i+1)+" «"+t.slice(0,50)+"» "+String(e).split("\n")[0]);}}});}
   console.log("throws:",n);' 2>/dev/null
   ```
   Debe imprimir `throws: 0`. Si algo falla, arréglalo (suele ser un comando KaTeX no
   soportado o un `$` de moneda sin `\`).
5. **Sube `VERSION`** en `sw.js` (una vez por lote) y `node --check sw.js`.
6. **Commit + push a `main`** (mensaje en español, estilo del repo), terminando con:
   `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
7. **Marca el lote en `BACKLOG-OLEADA-DESDE-CERO.md`** (`[x]`) y actualiza `HANDOFF`
   §7; commitéalo. Mantén el registro vivo para el siguiente agente.

## Pregunta a Edgar antes de empezar

- ¿Qué cluster quieres primero? (sugerencia del backlog: empezar por uno corto —
  `conductual` o `system-design`— para calibrar el estilo "desde cero" en un dominio
  nuevo, luego `dsa`, `ds-applied`/`stats-inf`, `causal-health`, y `ml-systems` al
  final). El orden didáctico **dentro** de cada cluster ya está fijado en el backlog.
- Si no responde, empieza por **`conductual`** (4 lecciones) y enséñale el resultado
  antes de seguir.

## Sitio, repo y deploy

- Sitio: https://imgoingsavage.github.io/cogitoergosum/ — Pages desde `main`, raíz.
- Tras desplegar, los cambios se ven recargando **dos veces** (el SW sirve cache-first;
  la 1.ª recarga instala la versión nueva, la 2.ª ya la sirve). En iPad: cerrar la
  app por completo y reabrir, posiblemente dos veces.

Trabaja con criterio de arquitecto-integrador, prioriza **calidad pedagógica sobre
cantidad**, valida (render + KaTeX 0 throws) y pushea cada lote, y mantén vivo el
backlog y el HANDOFF.
