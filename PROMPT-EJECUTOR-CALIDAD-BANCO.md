# PROMPT EJECUTOR (ChatGPT 5.5) · Reescritura de calidad del banco de la Fase 8

> **Eres un diseñador pedagógico senior + ingeniero de datos.** Tu trabajo es
> convertir **1,325 preguntas generadas por plantilla** (áridas, formularias, de
> bajo valor) en preguntas **genuinamente pedagógicas, transferibles y de alto
> valor**, **una por una**. No es un trabajo de buscar-y-reemplazar: es reescribir
> con criterio, como lo haría un autor del MIT / Art of Problem Solving.
>
> **Estándar de exigencia: máximo. Sin piedad contigo mismo.** Si una pregunta no
> haría pensar a un estudiante listo, está mal y la rehaces. Si un distractor es
> obviamente absurdo, está mal. Si el enunciado solo pide recordar una definición,
> está mal. Revisa **cada** pregunta contra la rúbrica del §4 y recházate a ti
> mismo antes de dar una por buena.

---

## 0. Reglas duras del proyecto (NO negociables)

- HTML/CSS/**JavaScript vanilla**, ES Modules; cero dependencias nuevas.
- Todo el contenido visible, en **español**. Tono sobrio (Constitución del
  proyecto): nunca regañes, normaliza el error, nada de espectáculo ni alarmismo.
- **Enfoque defensivo.** Nunca incluyas instrucciones ofensivas accionables. Los
  laboratorios externos: "solo en laboratorios autorizados".
- La **fuente de las unidades** es `data/ciberseguridad/_unidades.json` (formato 2
  espacios). Tras editarlo, **reinyecta** con
  `node scripts/aplicar-ciberseguridad.mjs` (idempotente; reordena y renumera
  `orden` por taxonomía; escribe `data/study.json` con indent de **1 espacio y sin
  newline final** — no se lo agregues).
- `node --check` debe pasar; todo JSON debe quedar parseable.
- Al tocar el shell (`data/study.json`, `data/ciberseguridad/_taxonomia.json`),
  sube `VERSION` en `sw.js` (+1 por commit que toque el shell; hoy va en
  **`cogitoergosum-v156`**).
- No reformatees archivos enteros (cuida el diff donde sea posible; aquí el diff
  será grande **por contenido**, no por reformateo).

---

## 1. Alcance EXACTO (qué tocar y qué NO)

Trabaja **solo** sobre las unidades del bloque `fase-8` en `_unidades.json`.

- **A REESCRIBIR (1,325 preguntas):** las que tienen
  **`metadata.generated_by === "enriquecer-ciberseguridad-contrato-v1"`**.
  Distribución: **960 `concepto`** (opción múltiple), **182 `scenario`**, **183
  `reflexion`**, repartidas en 45 unidades.
- **NO TOCAR (344 preguntas):** las hechas a mano (sin esa marca; ids tipo
  `cms1-q1`, `cwe1-q1`, `cmit1-cs1`, etc.). Son de calidad; déjalas intactas.
- **NO TOCAR** las lecciones `.md`, la taxonomía (salvo `VERSION` de sw), ni los
  344 a mano.

**Verifica el alcance antes de empezar:**
```bash
node -e "const u=require('./data/ciberseguridad/_unidades.json').unidades.filter(x=>x.bloque==='fase-8');let g=0,m=0;for(const x of u)for(const b of(x.banco||[]))b.metadata&&b.metadata.generated_by==='enriquecer-ciberseguridad-contrato-v1'?g++:m++;console.log('a reescribir',g,'| conservar',m)"
```
Debe imprimir `a reescribir 1325 | conservar 344`.

---

## 2. Contexto imprescindible: cómo funciona cada tipo en la app

- **`concepto` = opción múltiple INTERACTIVA.** El motor (`js/study.js`,
  `pintarOpcionMultiple`) baraja `options` y marca como correcta la opción cuyo
  texto **es exactamente igual** a `q.answer`. Por tanto, **OBLIGATORIO**:
  - `options`: arreglo de **exactamente 4** cadenas.
  - `q.answer` **idéntica** (carácter por carácter) a **una** de las 4 opciones.
  - Exactamente **una** correcta; las otras 3 son distractores.
  - Opciones **concisas** (idealmente ≤ 140 caracteres cada una). HOY son párrafos
    larguísimos: acórtalas.
- **`scenario`** y **`reflexion`** = respuesta abierta (el usuario escribe y luego
  ve `solucion`). **No** llevan `options` (si las traen, elimínalas).
- Campos que la app renderiza: `enunciado`, `solucion`, `explicacion`. Mantén el
  contrato §11 llenando además `concept`, `common_mistake`, `recognition_signal`,
  `source_reference`, `feedback`, `prompt`, `answer`, `type` con contenido REAL
  (no eco del enunciado).
- **Ancla cada pregunta a SU lección.** La unidad tiene `lectura`
  (`data/teoria/cyber-*.md`): lee esa lección y asegúrate de que la pregunta
  evalúa SU contenido y enlaza sus **aristas** (`[[...]]`).

---

## 3. El problema actual (lo que debes erradicar)

Las generadas son moldes rellenados con `ideas_clave`/títulos. Patrones a matar:
- Conceptos: *"¿Qué señal temprana te haría pensar que «‹idea›» importa…"*,
  *"Nombra un error típico al razonar sobre «‹idea›»…"*, *"Distingue «‹idea›» de
  una herramienta genérica…"*.
- Distractores de relleno: *"Instalar una herramienta genérica sin nombrar el
  activo…"*, *"Confiar en que ‹título› no aplica porque es interno o pequeño"*,
  *"Resolverlo solo con documentación, sin control técnico"*. Son **obviamente
  falsos** → no discriminan → no enseñan.
- Scenarios: *"…el equipo debe decidir sobre «‹idea›»"* (genérico, sin situación
  real).
- Reflexiones: *"aplica «‹idea›» a un proyecto real… ¿qué cambiarías esta
  semana?"* (misma plantilla 183 veces).

Si tu reescritura todavía huele a plantilla, **no terminaste**.

---

## 4. Rúbrica de calidad (aplícala a CADA pregunta; si falla una, rehaz)

Basada en `auditoria.md` (contrato de estudiabilidad) y `ciberseguridad.md` §9/§11.

**Toda pregunta:**
1. **Evalúa pensar, no recordar.** Prioriza: ¿cuándo usar esto? ¿qué supuesto se
   rompe? ¿cuál es la estructura profunda? ¿qué problema isomorfo aparece en otro
   dominio? Evita "¿qué es X?" / "¿qué significa X?".
2. **Es transferible.** Plantea un caso, código, log o decisión concretos; pega la
   idea a un escenario realista de datos/IA, no a la abstracción.
3. **Conecta aristas.** Relaciona con otra idea de la ruta ("esto es un caso de…",
   "esto se diferencia de…", "esto falla cuando…"), citando aristas reales del
   cluster (puedes referirlas en `solucion`/`concept`).
4. **Fiel a la lección.** Lo que afirma como correcto debe sostenerse en la
   `.md` de esa unidad.
5. **Dificultad calibrada.** `easy` = reconocer/aplicar directo; `medium` =
   distinguir/elegir entre opciones cercanas; `hard` = transferir, caso borde,
   o detectar el supuesto roto. Las tres deben sentirse distintas.

**Solo opción múltiple (`concepto`):**
6. **Distractores plausibles y diagnósticos.** Cada uno de los 3 debe ser un
   **error real y común** (una confusión que un estudiante de verdad tendría), no
   un absurdo. Idealmente cada distractor mapea a una `common_mistake` nombrable.
7. **Una sola correcta, inequívoca.** Sin "todas las anteriores", sin dos
   defendibles. La correcta es claramente la mejor para quien entendió.
8. **Opciones paralelas y concisas.** Misma longitud/registro aproximado (que la
   correcta no destaque por ser la más larga o la única detallada — error clásico).
9. **`feedback` enseña.** Breve: por qué la correcta lo es y, si aporta, por qué
   el distractor tentador falla.

**Scenario:** situación específica (roles, sistema, datos), una decisión
defensiva concreta a tomar; `solucion` razona la elección (amenaza/impacto/
control/siguiente paso) y nombra el control de proceso o técnico correcto.

**Reflexion:** pregunta metacognitiva **abierta y variada** (no la misma plantilla);
`solucion` ofrece una reflexión modelo y qué haría buena a una respuesta.

> **Auto-rechazo:** antes de aceptar una pregunta, pregúntate: ¿un experto la
> miraría y diría "buena pregunta"? ¿el distractor me haría dudar si no supiera?
> ¿se podría responder sin haber estudiado, solo por sentido común o por
> eliminación de absurdos? Si lo último es sí, **rehazla**.

## 4.1 Ejemplo (antes → después) — calíbrate con esto

**ANTES (plantilla, malo):**
```
enunciado: "¿Qué señal temprana te haría pensar que 'La frontera de confianza real
            está en el servidor, no en el cliente' importa en una API educativa?"
options: ["<párrafo correcto largo>",
          "Instalar una herramienta genérica sin nombrar el activo...",
          "Confiar en que Web I no aplica porque el sistema es interno...",
          "Resolverlo solo con documentación, sin control técnico..."]
```

**DESPUÉS (pensar + distractores reales, bueno):**
```
enunciado: "Un endpoint valida el precio en el formulario con JavaScript antes de
            enviarlo. Un atacante hace la petición POST directamente con curl,
            saltándose esa validación. ¿Por qué pasó y qué lo corrige?"
options:
  - "La validación corría en el cliente; hay que validar también en el servidor."   ← answer
  - "Faltaba HTTPS; con TLS el precio no se puede modificar."
  - "El JavaScript tenía un bug; basta corregir la validación del front."
  - "Faltaba ofuscar el JavaScript para que no se pueda leer."
feedback: "El cliente es manipulable: la frontera de confianza real es el servidor.
           TLS protege el tránsito, no la lógica; ofuscar es seguridad por oscuridad."
common_mistake: "Creer que validar en el cliente es un control de seguridad."
```
Los tres distractores son creencias reales y tentadoras (TLS lo arregla, era un
bug del front, ofuscar basta), no absurdos. Eso **discrimina** y **enseña**.

---

## 5. Proceso de trabajo (lotes, una por una, con bitácora)

1325 preguntas no caben en una pasada con calidad. Trabaja por **unidad** (45) y
**commitea por lote** (p. ej. por cluster o cada 3-5 unidades).

Por cada unidad:
1. **Lee su lección** (`data/teoria/<id>.md`) y sus aristas.
2. Lista sus preguntas generadas (las del marcador).
3. **Reescribe una por una** según la rúbrica §4 — concepto (MC), scenario,
   reflexion. **Conserva el `id`** de cada pregunta (no rompas el progreso del
   usuario) y su `difficulty` (salvo que esté mal calibrada; si la cambias,
   mantén el balance 10/10/10 por unidad).
4. **Marca lo revisado:** cambia `metadata.generated_by` a
   **`"revision-calidad-humana-v1"`** en cada pregunta reescrita. ⚠️ CRÍTICO:
   `scripts/enriquecer-ciberseguridad-contrato.mjs` **borra y regenera** todo lo
   que tenga el marcador viejo (`enriquecer-…-v1`). Si dejas el marcador viejo, una
   futura corrida del generador **destruiría tu trabajo**. Al cambiarlo, quedan
   protegidas. **No vuelvas a correr ese generador** sobre estas unidades; el banco
   reescrito es ahora la fuente de verdad.
5. Reinyecta (`node scripts/aplicar-ciberseguridad.mjs`) y valida (§6).
6. Commitea el lote con un mensaje claro y una **bitácora** de cuántas unidades/
   preguntas llevas (p. ej. "calidad banco: clusters 1-2 (10 unidades, 420
   preguntas) ✓ — faltan 35 unidades").

Mantén una **bitácora de progreso** en el cuerpo de tus commits o en un archivo
`PROGRESO-CALIDAD-BANCO.md` para poder retomar si te interrumpen.

---

## 6. Validación obligatoria (tras cada lote y al final)

```bash
node --check js/study.js   # si tocaste algo de JS (normalmente no)
node -e "JSON.parse(require('fs').readFileSync('data/ciberseguridad/_unidades.json','utf8'));console.log('unidades OK')"
node scripts/aplicar-ciberseguridad.mjs
node scripts/smoke-teoria.mjs   # threw=0 undefined=0 rawFence=0
```
Y este chequeo de integridad del banco (créalo si no existe):
```bash
node -e "
const fs=require('fs');
const f8=JSON.parse(fs.readFileSync('data/study.json','utf8')).unidades.filter(u=>u.bloque==='fase-8');
const all=f8.flatMap(u=>u.banco||[]);
// 1) ids únicos
const ids=new Set();let dup=0;for(const b of all){if(ids.has(b.id))dup++;ids.add(b.id);}
// 2) MC bien formadas: 4 opciones y answer ∈ options
let mcMal=0;for(const b of all){if(Array.isArray(b.options)&&b.options.length){if(b.options.length!==4||!b.options.includes(b.answer))mcMal++;}}
// 3) opciones no-paragraph (alerta si alguna > 180 chars)
let largas=0;for(const b of all)for(const o of (b.options||[]))if((o||'').length>180)largas++;
console.log('preguntas',all.length,'| ids dup',dup,'| MC mal formadas',mcMal,'| opciones>180c',largas);
"
```
**Debe quedar:** `ids dup 0`, `MC mal formadas 0`. `opciones>180c` debe tender a 0
(acórtalas). Si `answer ∉ options`, la MC se rompe en la app: corrígelo siempre.

Comprobación de "ya no quedan plantillas":
```bash
node -e "
const fs=require('fs');
const f8=JSON.parse(fs.readFileSync('data/ciberseguridad/_unidades.json','utf8')).unidades.filter(u=>u.bloque==='fase-8');
let viejas=0;for(const u of f8)for(const b of(u.banco||[]))if(b.metadata&&b.metadata.generated_by==='enriquecer-ciberseguridad-contrato-v1')viejas++;
console.log('generadas sin revisar restantes:',viejas);
"
```
Al terminar debe ser **0**.

Prueba humana (muestreo): sirve la app (`python3 -m http.server 8000`), entra a un
par de unidades de Fase 8, haz un quiz de opción múltiple y un examen de cluster:
las opciones deben verse concisas, la correcta no obvia por eliminación, el
veredicto y la explicación correctos. Cero errores en consola.

---

## 7. Reporte final

1. Cuántas preguntas reescritas por tipo (debe sumar 1,325) y por cluster.
2. `VERSION` final de `sw.js`.
3. Salidas de los chequeos del §6 (ids dup 0, MC mal 0, generadas restantes 0).
4. Una muestra de 3 pares antes→después que ejemplifiquen el salto de calidad.
5. Decisiones difíciles (preguntas que reformulaste de raíz porque no tenían
   arreglo) y cualquier pregunta que recomiendes para revisión humana.

## 8. Lo que NO debes hacer

- ❌ Buscar-y-reemplazar mecánico, o reescribir con un nuevo molde (cambiar una
  plantilla por otra). Cada pregunta es individual.
- ❌ Tocar las 344 hechas a mano ni las lecciones `.md`.
- ❌ Dejar `answer` que no sea **exactamente** una de las `options` (rompe la MC).
- ❌ Distractores absurdos o reconocibles por eliminación.
- ❌ Opciones tipo párrafo; deben ser concisas y paralelas.
- ❌ Dejar el marcador `generated_by` viejo (lo borraría el generador).
- ❌ Re-correr `enriquecer-ciberseguridad-contrato.mjs` sobre estas unidades.
- ❌ Cambiar los `id` de las preguntas (rompe el progreso del usuario).
- ❌ Inventar hechos que la lección no sostenga; mantén el rigor técnico defensivo.
- ❌ Olvidar subir `VERSION` en `sw.js` y reinyectar a `study.json`.

> Meta: que un estudiante que termine el banco de la Fase 8 **piense mejor sobre
> seguridad**, no que haya reconocido 1,325 plantillas. Trabaja al máximo.
```
