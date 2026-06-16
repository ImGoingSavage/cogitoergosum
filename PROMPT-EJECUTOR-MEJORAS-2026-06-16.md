# PROMPTS PARA EL EJECUTOR (Claude Sonnet 4.6) · Lote de mejoras 2026-06-16

> **Eres un software engineer junior y ejecutor.** El arquitecto ya auditó el
> repo, localizó las causas raíz y diseñó cada solución. Tu trabajo es
> **implementar el código** siguiendo estas instrucciones al pie de la letra,
> sin rediseñar ni improvisar. Si la realidad del repo no coincide con lo que
> aquí se describe, **DETENTE y reporta** en vez de inventar.
>
> Hay **4 tareas**. Ejecútalas **en orden de prioridad** (la Tarea 1 es ALTA;
> 2–4 son BAJAS). **Una rama/commit por tarea.** No mezcles tareas en un mismo
> commit. Tras cada tarea, corre su checklist de validación antes de pasar a la
> siguiente.

---

## 0. Reglas duras del proyecto (NO negociables, aplican a TODAS las tareas)

- HTML / CSS / **JavaScript vanilla**, ES Modules. **Cero dependencias** nuevas,
  cero frameworks, cero CDNs, cero librerías de PDF.
- Todo el texto visible al usuario, en **español**.
- **`js/storage.js` es la única puerta a LocalStorage.** Usa sus helpers
  (`load`, `save`, `update`, `hoy`, `uidNuevo`, `encolarEvento`) o los módulos
  que ya los envuelven (`Analytics`, etc.). **Nunca** llames a `localStorage`
  directamente.
- Funciona en **GitHub Pages**, **offline-first**. No rompas el service worker,
  el manifest, Supabase ni la sincronización.
- `node --check` debe pasar en cada `.js` que toques. Todo JSON debe quedar
  parseable.
- **Service worker:** el `SHELL` de `sw.js` incluye `index.html`,
  `css/styles.css`, **todos** los `js/*.js`, `data/study.json`,
  `data/entrevista/_taxonomia.json` y los `data/teoria/*.md`. **Si tocas
  cualquiera de esos, sube `VERSION` en `sw.js`.** Hoy va en
  **`cogitoergosum-v139`**. Súbela **+1 por cada commit que toque el shell**
  (Tarea 1 → `v140`, Tarea 2 → `v141`, etc.; ajusta al número real que tenga el
  archivo cuando llegues).
- No reformatees archivos enteros (cuida el diff). No cambies contenido
  pedagógico (enunciados/soluciones) salvo que la tarea lo pida explícitamente.
- Código limpio, comentado al estilo del módulo que edites. **Nada de spaghetti.**

---

# TAREA 1 — [ALTA] Corregir el bug «undefined» en el render de teoría/quiz

## 1.1 Diagnóstico (ya confirmado por el arquitecto — NO lo re-investigues)

En **`js/markdown.js`**, la función **`inline(texto)`** protege fragmentos de
código y matemáticas con un mecanismo de *tokens*:

```js
const proteger = (html) => {
  tokens.push(html);
  return ` ${tokens.length - 1} `;   // ← placeholder: ESPACIO + número + ESPACIO
};
```

y al final los restaura (≈línea 173):

```js
s = s.replace(/ (\d+) /g, (_, i) => tokens[Number(i)]);
```

**El bug:** el placeholder ` N ` (espacio-dígito-espacio) es **indistinguible de
un número normal escrito en prosa rodeado de espacios** (p. ej. "subir al peldaño
**2** y predecir", "entre **10** y 20", "el paso **3** del método"). La
restauración `/ (\d+) /g` captura esos números de prosa y los reemplaza por
`tokens[N]`, que casi siempre es **`undefined`** (no hay tantos tokens). Además
**consume los espacios** que rodeaban al número, por eso en pantalla se ve
`peldañoundefinedy` (sin espacios).

**Caso reproducible real:** `data/teoria/arena-h15.md` línea 43 contiene
`…te deja subir al peldaño 2 y predecir…` → renderiza `peldañoundefinedy`
(es el screenshot reportado).

**Alcance:** afecta a **146 de 166** lecciones de `data/teoria/*.md`, y también
a cualquier pregunta/respuesta del quiz que pase por `renderInline()` (que usa
el mismo `inline()`). Es **una sola causa raíz**: arreglar `inline()` lo corrige
todo.

## 1.2 La solución (probada por el arquitecto)

Cambia el **delimitador del placeholder** por una **sentinela imposible de
aparecer en prosa**: el carácter de control NUL (`\u0000`). Así un número de
prosa jamás colisiona.

1. Declara la sentinela una vez (dentro de `inline`, o como const de módulo):

   ```js
   const SENT = '\u0000'; // sentinela de token: jamás aparece en texto de lección
   ```

2. En `proteger`, emite `SENT + idx + SENT` en lugar de ` idx `:

   ```js
   const proteger = (html) => {
     tokens.push(html);
     return SENT + (tokens.length - 1) + SENT;
   };
   ```

3. En la restauración (la línea `s = s.replace(/ (\d+) /g, …)`), usa la sentinela:

   ```js
   s = s.replace(new RegExp(SENT + '(\\d+)' + SENT, 'g'), (_, i) => tokens[Number(i)]);
   ```

**Verificación previa del arquitecto** (6 casos, incluido el de los espacios y
`\$` literal): con este cambio, `undefined` desaparece (0/6), las matemáticas
siguen renderizando y los números de prosa se conservan. Como beneficio extra,
desaparecen los espacios espurios que el placeholder viejo dejaba alrededor de
las matemáticas a inicio de línea.

> **No cambies** la lógica de tokens, ni el orden de las transformaciones, ni
> nada más de `markdown.js`. Solo el delimitador del placeholder y su regex de
> restauración.

## 1.3 Endurecer el smoke test

Edita **`scripts/smoke-teoria.mjs`** para que **falle (exit code ≠ 0)** si
alguna lección renderiza la cadena literal `undefined`:

- Hoy el script solo recorre los archivos `arena-*.md`. Para esta comprobación,
  **escanea TODOS los `*.md` de `data/teoria/`** (también `zeitz-*`, `engel-*`,
  `aime-*`, `polya-*`), renderiza con `renderMarkdown` y cuenta ocurrencias de
  `undefined` en el HTML. Imprime los archivos afectados y, al final, si el total
  es > 0, `process.exitCode = 1`.
- Conserva las comprobaciones existentes (`threw`, `rawDisplayMath`, `rawLinks`).

## 1.4 Validación obligatoria

1. `node --check js/markdown.js`.
2. `node scripts/smoke-teoria.mjs` → debe imprimir `threw=0 rawDisplayMath=0` y
   **0 lecciones con `undefined`** (antes del fix eran 146).
3. Comprobación puntual del caso real: el HTML de `arena-h15.md` debe contener
   `peldaño 2 y` (con espacios, sin `undefined`).
4. Sirve la app (`python3 -m http.server`), abre Estudio → una lección de la
   Arena → "📖 Leer la lección aquí": el texto se ve íntegro, sin `undefined`,
   con las matemáticas bien. **Cero errores en consola.**
5. Sube `VERSION` en `sw.js` (tocaste `js/markdown.js`, que está en el shell).
6. Commit solo de esta tarea.

---

# TAREA 2 — [BAJA] Descargar / imprimir el cuaderno de fichas (moralejas) en PDF

## 2.1 Qué se pide

Permitir al usuario **ver y descargar como PDF** el historial de fichas que ha
completado en el **entrenamiento** (camino 1), con: enunciado del ejercicio (en
LaTeX renderizado), la solución, la **estrategia** (invariantes / inversión /
optimización / patrones), su **predicción**, su autoevaluación, y lo que escribió
en cada recuadro (moraleja, disparador, comparación, transferencia y
desconstrucción).

## 2.2 Mapa del terreno (ya investigado — verifícalo)

- Las fichas viven en `historial` (LocalStorage). El helper
  **`Analytics.cuadernoMoralejas()`** (`js/analytics.js` ≈línea 63) ya devuelve
  el historial filtrado (las que tienen moraleja o disparador), de la más
  reciente a la más antigua.
- Cada entrada del historial (ver `completarSesion` en `js/app.js` ≈líneas
  795–820) tiene **realmente** estos campos:
  `problemId, fecha, score, hintsUsados, tiempoMin, autoevaluacion,
  estrategia, dificultad, esRevision, prediccion, moraleja, disparador,
  desconstruccionLen, duracionMin, reflexion:{comparacion, transferencia}`.
- El **enunciado y la solución** NO están en el historial: se obtienen de
  `data/problems.json` cruzando por `problemId`. En `app.js` el arreglo en
  memoria se llama `problemas` (`problemas.find(x => x.id === f.problemId)`).
  Cada problema tiene `titulo, estrategia, enunciado, solucion, explicacion`
  (con LaTeX en `$…$`).
- Los nombres legibles de estrategia están en `Analytics.NOMBRES_ESTRATEGIA`.
- El cuaderno ya se pinta en el Dashboard: función **`renderizarCuaderno()`**
  (`js/app.js` ≈línea 1142) dentro de `#cuaderno-lista` (`index.html` ≈línea 532).
- Para LaTeX usa **`renderInline(texto)`** de `js/markdown.js` (KaTeX, offline).

## 2.3 ⚠️ Hallazgo crítico del arquitecto: falta persistir la desconstrucción

Hoy el historial **NO guarda el texto** de "Mi Desconstrucción", solo su longitud
(`desconstruccionLen`). Para poder mostrar "lo que llenaste" debes **empezar a
persistirlo**:

- En `completarSesion` (`js/app.js`, dentro del objeto `entrada`, junto a
  `desconstruccionLen` ≈línea 811) **añade**: `desconstruccion: a.desconstruccion,`.
- Esto **solo afecta a sesiones futuras**: las fichas viejas no tendrán el campo.
  En el PDF, cuando falte, muestra `(no registrada)` — **no rompas** por ausencia.
- `historial` está en `CLAVES_SYNC` (storage.js): el campo viajará a Supabase.
  Es dato propio del usuario; es aceptable. No añadas claves nuevas al esquema
  fuera de la entrada del historial.

## 2.4 Enfoque técnico OBLIGATORIO (sin librerías)

**No** generes un PDF a mano ni añadas librerías. Usa el camino vanilla estándar:
**una vista imprimible + `window.print()`**, y el usuario elige "Guardar como
PDF" en el diálogo del navegador.

Recomendado: al pulsar el botón, **abre una ventana nueva** (`window.open()`) y
escribe en ella un documento HTML **autocontenido** que:

1. Enlace el **mismo CSS de KaTeX** ya vendorizado (`assets/katex/katex.min.css`)
   para que las matemáticas se vean en el PDF.
2. Incluya un `<style>` de impresión sobrio (tipografía legible, saltos de página
   por ficha con `break-inside: avoid`, márgenes, sin colores de fondo pesados).
3. Liste cada ficha de `Analytics.cuadernoMoralejas()` con, en este orden:
   título del problema, estrategia (de `NOMBRES_ESTRATEGIA`), fecha; luego
   **Enunciado** (`renderInline(p.enunciado)`), **Tu predicción**, **Tu
   autoevaluación**, **Desconstrucción** (texto si existe, si no `(no
   registrada)`), **★ Moraleja**, **★ Disparador**, **Comparación**,
   **Transferencia**, y opcionalmente **Solución** (`renderInline(p.solucion)`).
4. Tras inyectar el HTML, llame a `window.print()` de esa ventana.

> Como KaTeX se renderiza a HTML/CSS (no necesita el JS en la ventana hija si
> usas `renderInline` en la ventana **padre** y pasas el HTML ya generado), la
> ruta más simple y robusta es: **generar todo el HTML en la página actual**
> (donde KaTeX ya está cargado) y volcarlo en la ventana de impresión junto al
> `<link>` del CSS de KaTeX. Si prefieres un contenedor oculto + `@media print`
> en `styles.css` en vez de ventana nueva, es aceptable, pero entonces oculta
> TODO lo demás en impresión y restáuralo después.

## 2.5 UI

- Añade un botón **"⬇ Descargar / imprimir cuaderno"** en el Dashboard, junto a
  `#cuaderno-lista` (`index.html` ≈línea 532). Reusa `class="secundario"`.
- Cablea su `click` en `js/app.js` (donde se configura el Dashboard / cerca de
  `renderizarCuaderno`). Si no hay fichas, muestra un aviso suave y no abras nada.
- Texto del documento, en español. Encabezado: "Cuaderno de moralejas" + fecha
  de generación (usa `Storage.hoy()`).

## 2.6 Validación

1. `node --check` en los `.js` tocados.
2. Completa (o simula en LocalStorage) ≥1 ficha; pulsa el botón: se abre la vista
   imprimible, las **matemáticas se ven**, aparecen todos los recuadros, y el
   diálogo de impresión permite "Guardar como PDF".
3. Una ficha vieja sin `desconstruccion` muestra `(no registrada)` sin romper.
4. Funciona **offline** (KaTeX es local). Cero errores en consola.
5. Sube `VERSION` en `sw.js`. Commit solo de esta tarea.

---

# TAREA 3 — [BAJA] Vista "Cómo usar la app" (instructivo)

## 3.1 Qué se pide

Una vista nueva que explique al usuario: la **filosofía y el objetivo** de la app,
**cómo funciona el entrenamiento**, **qué hace cada botón**, **por qué se usan
cuestionarios** en el Modo Estudio, y **cómo sacarle provecho**.
**NO menciones el mentor/entrenador socrático** (aún no está activo para el
usuario): habla solo de lo que existe hoy.

## 3.2 Mapa del terreno (patrón de navegación — síguelo EXACTO)

- La barra de navegación tiene 4 botones (`index.html` ≈líneas 81–84):
  `nav-sesion`, `nav-estudio`, `nav-claustro`, `nav-dashboard`.
- Cada vista es una `<section id="vista-XXX">` (`vista-sesion`, `vista-estudio`,
  `vista-claustro`, `vista-dashboard`).
- El cambio de vista es **`cambiarVista(vista)`** (`js/app.js` ≈línea 1317):

  ```js
  function cambiarVista(vista) {
    vistaActual = vista;
    ['sesion', 'estudio', 'claustro', 'dashboard'].forEach((v) => {
      $(`vista-${v}`).hidden = vista !== v;
      $(`nav-${v}`).classList.toggle('activo', vista === v);
    });
    MentorChat.actualizarMentorUI();
    Pizarra.actualizarVisibilidad(vista);
  }
  ```

- Los handlers de nav se registran ≈líneas 1292–1303
  (`$('nav-sesion').addEventListener('click', () => cambiarVista('sesion'))`, …).

## 3.3 Implementación

1. **HTML:** añade un botón `nav-guia` en la barra (p. ej. "Guía" o "Cómo usar"),
   y una `<section id="vista-guia" hidden>` con el contenido del instructivo,
   maquetado con las mismas `class="tarjeta"` y estilos existentes (sin CSS nuevo
   salvo lo mínimo). Decide tú la posición del botón (sugerido: antes de
   "Dashboard").
2. **JS:** en `cambiarVista`, **añade `'guia'` al array** de vistas para que se
   muestre/oculte y marque el botón activo correctamente. Registra el handler
   `$('nav-guia').addEventListener('click', () => cambiarVista('guia'))` junto a
   los demás.
3. Verifica que `MentorChat.actualizarMentorUI()` y
   `Pizarra.actualizarVisibilidad('guia')` se comporten bien con la vista nueva
   (deben **ocultar** mentor/pizarra en una vista informativa). Si alguno asume
   solo las 4 vistas viejas y rompiera, ajústalo de forma conservadora (que en
   `'guia'` no muestren nada). **Repórtalo si tocaste esos módulos.**

## 3.4 Contenido (redáctalo en español, claro y breve; sin mentor socrático)

Cubre, en secciones (tarjetas):
- **Filosofía y objetivo:** entrenar capacidad transferible de resolución de
  problemas mediante práctica deliberada y metacognición (no "resolver muchos").
  Inspiración Pólya, dificultad deseable, productive struggle. (Base: `CLAUDE.md`
  y la sección de Pólya; resúmelo, no lo copies entero.)
- **El entrenamiento diario (camino 1):** un problema, temporizador de reflexión,
  "Mi Desconstrucción" (pensar por escrito antes de ver nada), predicción de
  jugada, pistas graduadas 1→5 (cada una cuesta), revelar solución, y la **ficha**
  (moraleja + disparador) como el artefacto más valioso. Qué hace cada botón
  principal de esa vista.
- **El Modo Estudio (camino 2):** el roadmap por bloques/clusters, leer la
  lección, y **por qué hay cuestionarios**: son *retrieval practice* (recordar
  desde la memoria consolida más que releer). Menciona el selector de dificultad
  y el examen final de cluster.
- **Dashboard:** rachas, estadísticas y el cuaderno de moralejas.
- **Pizarra:** donde está el botón y como usarla
- **Descargar fichas:** Hablar de la función para imprimir los ejercicios que has resuelto, con sus soluciones y las fichas que has generado como herramienta para tener una lista de moralejas que siempre puedas consultar
- **Cómo sacarle provecho:** forcejear antes de mirar, usar pocas pistas, escribir
  la ficha siempre, volver a los repasos.

## 3.5 Validación

1. `node --check` en los `.js` tocados.
2. La barra muestra el botón nuevo; al pulsarlo aparece la guía y se ocultan las
   otras vistas; al volver a otra vista, todo funciona como antes.
3. Mentor flotante y pizarra **no** aparecen en la guía. Cero errores en consola.
4. Sube `VERSION` en `sw.js`. Commit solo de esta tarea.

---

# TAREA 4 — [BAJA] Referencias (bibliografía APA) por cluster en la Fase 7

## 4.1 Qué se pide

En cada **cluster** de la Fase 7 (Arena), mostrar al final un apartado de
**Referencias** con la bibliografía **en formato APA** que sirvió de base, para
que el usuario pueda consultarla si quiere profundizar.

## 4.2 Mapa del terreno (ya investigado)

- Los 8 clusters están en **`data/entrevista/_taxonomia.json`** → `clusters[]`.
  Cada cluster tiene `id, titulo, track, descripcion, secuencia, sim, unidades[]`.
- Cada unidad de la Arena tiene un campo **`libro`** en `data/study.json` con
  **autor(es) y título reales**, p. ej.:
  - `arena-b1`: `"Introduction to Probability (Blitzstein & Hwang)"`
  - `arena-dg1`: `"Probability and Statistics (DeGroot & Schervish)"`
  - `arena-cc1`: `"Cracking the Coding Interview (6th ed.)"`
  - `arena-sd1`: `"System Design Interview – An Insider's Guide (Alex Xu)"`
  - `arena-h15`: `"The Book of Why… (Judea Pearl & Dana Mackenzie)"`
- El acordeón de cada cluster lo construye **`crearClusterAcordeon(c, unidades, b)`**
  (`js/study.js` ≈línea 426). Al final del `cuerpo` ya se añaden la simulación de
  entrevista (`if (c.sim)`) y el examen final del cluster (`if (c.id !== '__otras')`).
  El bloque de referencias va **después** de esos, también dentro de `cuerpo`.

## 4.3 Datos: añade `referencias` a cada cluster

En `data/entrevista/_taxonomia.json`, **añade a cada cluster** un array
`"referencias": [ "<entrada APA>", … ]`.

- **Compón cada entrada a partir de los `libro` reales** de las unidades de ese
  cluster (dedup por libro). Autor y título son datos verificables del repo: úsalos.
- Da formato **APA** (autor, año, *título en cursiva textual no — es JSON, texto
  plano*, editorial cuando la conozcas con certeza). Para estos textos clásicos y
  conocidos puedes incluir año/edición/editorial **solo si estás seguro**.
  **Nunca inventes** un año, editorial o edición: si no lo sabes con certeza,
  **omítelo** (una entrada APA sin editorial es preferible a una fabricada).
- No uses LaTeX en las referencias (son texto plano).
- El cluster `__otras` (grupo de respaldo, generado en runtime) **no** lleva
  referencias.

> Esta es la **única** parte del lote que es contenido bibliográfico. Marca en tu
> reporte final cualquier entrada cuyo año/editorial no pudiste confirmar, para
> revisión humana.

## 4.4 Render

En `crearClusterAcordeon`, tras el bloque del examen final, añade:

```js
if (c.id !== '__otras' && Array.isArray(c.referencias) && c.referencias.length) {
  // título "Referencias" + lista <ul> con cada entrada por textContent
}
```

- Usa **`textContent`** para cada entrada (no `innerHTML`): son texto plano.
- Estilo discreto, consistente con `cluster-desc` / `cluster-secuencia`. Puedes
  reutilizar clases existentes o añadir una mínima (`cluster-referencias`).
  Opcional: hazlo colapsable, pero no es obligatorio.

## 4.5 Validación

1. `data/entrevista/_taxonomia.json` parseable (JSON válido) tras la edición.
2. `node --check js/study.js`.
3. Sirve la app → Estudio → Fase 7 (Arena): cada uno de los 8 clusters muestra su
   apartado **Referencias** al final, con la bibliografía en APA. Cero errores.
4. `_taxonomia.json` está en el shell → sube `VERSION` en `sw.js`.
5. Commit solo de esta tarea.

---

## Reporte final (al terminar las 4 tareas)

1. Resumen ejecutivo por tarea.
2. Archivos modificados/creados (rutas reales) y el `VERSION` final de `sw.js`.
3. Tarea 1: salida del smoke test (lecciones con `undefined` antes/después).
4. Tarea 2: confirmación de que el PDF/impresión muestra LaTeX y todos los
   recuadros; nota sobre fichas viejas sin desconstrucción.
5. Tarea 3: que la nav nueva funciona y no rompe las otras vistas.
6. Tarea 4: lista de entradas APA con año/editorial **no confirmados** (para
   revisión humana).
7. Validaciones ejecutadas y su resultado. Riesgos o mejoras pendientes.

## Lo que NO debes hacer

- ❌ Añadir librerías, frameworks, CDNs o un generador de PDF.
- ❌ Llamar a `localStorage` directamente (usa `storage.js`/`Analytics`).
- ❌ Cambiar la lógica de tokens de `markdown.js` más allá del delimitador.
- ❌ Inventar años/editoriales en las referencias APA.
- ❌ Mencionar el mentor/entrenador socrático en la guía.
- ❌ Mezclar varias tareas en un mismo commit.
- ❌ Olvidar subir `VERSION` en `sw.js` cuando toques el shell.
```
