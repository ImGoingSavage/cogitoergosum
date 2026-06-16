# PROMPT MAESTRO — CogitoErgoSum: Oleadas 1-3 de la auditoría 2026-06-12

> **Origen:** generado por la sesión de auditoría senior del 2026-06-12
> (bitácora (5) de HANDOFFCES.md, sobre el commit 8a13241). Pegar este
> documento COMPLETO como prompt a un agente (Sonnet 4.6 o superior).
> Cubre las oleadas 1-3 del plan; las oleadas 4-6 quedan para sesiones
> posteriores porque requieren decisiones/acciones del usuario.

Eres un ingeniero senior ejecutando parches EXACTOS sobre el proyecto
`/Users/EdgarDevice/Desktop/ProyectoX` (repo público `ImGoingSavage/cogitoergosum`,
servido en https://imgoingsavage.github.io/cogitoergosum/). NO audites de nuevo.
NO refactorices nada fuera de lo listado. Ejecuta los pasos EN ESTE ORDEN.

## REGLAS ABSOLUTAS (violarlas invalida el trabajo)

1. HANDOFFCES.md §0 (Constitución) es LEY. La IA y la cuenta son SIEMPRE
   opcionales: sin API key nada de IA aparece; sin cuenta la app funciona 100%.
2. Vanilla JS + ES6 modules. CERO librerías, CDNs, npm o build steps.
3. `storage.js` es la ÚNICA puerta a LocalStorage. `cuentaActiva()` de
   aiMentor.js es la única fuente de la key de Claude.
4. Modelo IA: `claude-opus-4-8`. No lo cambies.
5. Todo en español (código, comentarios, UI).
6. `cps_mentorIA`, `cps_asignacion`, `cps_credenciales`, `cps_pizarras` y la
   nueva `cps_diagnostico` JAMÁS entran a `CLAVES_SYNC`.
7. NO toques: pizarra.js, claustro.js, badges.js, avatar.js, timer.js,
   adaptiveEngine.js, spacedRepetition.js, analytics.js, markdown.js,
   problems.json, study.json, data/teoria/, el comportamiento de
   `cps_credenciales`, ni `.claude/settings.local.json`.
8. NO ejecutes SQL tú mismo: la anon key no puede correr DDL. Escribes el
   archivo, se lo muestras al usuario y ESPERAS su confirmación.
9. Conserva todos los fallbacks silenciosos existentes (hints estáticos,
   sync con reintento). Los parches AÑADEN registro, nunca quitan el silencio.

---

## PASO 1 — SQL de servidor (requiere al usuario; hazlo PRIMERO)

1.1. Crea el archivo `supabase/schema-parches-2026-06-12.sql` con EXACTAMENTE:

```sql
-- =============================================================
-- CogitoErgoSum — Parches 2026-06-12 (auditoría):
--   (1) FK de invitaciones.usado_por: borrar_mi_cuenta() fallaba con
--       error de FK para cualquier usuario que canjeó un código (§0.1).
--   (2) uid único en events: idempotencia del outbox (los reintentos
--       duplicados se ignorarán con on_conflict=uid).
-- Ejecutar UNA VEZ en el SQL Editor. Idempotente: re-ejecutar no daña.
-- =============================================================

alter table public.invitaciones
  drop constraint if exists invitaciones_usado_por_fkey;
alter table public.invitaciones
  add constraint invitaciones_usado_por_fkey
    foreign key (usado_por) references auth.users (id) on delete set null;

alter table public.events add column if not exists uid text unique;
```

1.2. Muestra el contenido al usuario y pídele: «Pega este SQL en
supabase.com → proyecto rcaljqmibtkorcmdyqvg → SQL Editor → Run, y confírmame
cuando esté». DETENTE hasta su confirmación.

1.3. Tras la confirmación, verifica tú mismo que la columna existe (la ANON_KEY
está como constante en `js/api.js`):

```sh
curl -s "https://rcaljqmibtkorcmdyqvg.supabase.co/rest/v1/events?select=uid&limit=1" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
```

Respuesta esperada: `[]` (RLS oculta filas a anónimos; un error de "column
events.uid does not exist" significa que el SQL NO se aplicó — vuelve a 1.2).
Pídele además al usuario que corra en el SQL Editor:
`select confdeltype from pg_constraint where conname = 'invitaciones_usado_por_fkey';`
y confirme que devuelve `n` (set null).

## PASO 2 — aiMentor.js: errores con status + cuerpo, y puerta única de red

2.1. Añade esta función exportada después de `mentorDisponible()`:

```js
/**
 * Llamada cruda a la Messages API con la cuenta activa: añade headers y key,
 * y convierte todo error HTTP en Error con status + cuerpo (diagnosticable).
 * Única puerta de red a api.anthropic.com para TODOS los módulos (§3.10);
 * la excepción documentada es probarCuenta(), que ES la herramienta de
 * diagnóstico y necesita el status crudo.
 */
export async function llamarMessagesAPI(body) {
  const cuenta = cuentaActiva();
  if (!cuenta?.apiKey) return null;
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': cuenta.apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({ model: MODEL, ...body }),
  });
  if (!res.ok) {
    const cuerpo = await res.text().catch(() => '');
    throw new Error(`API ${res.status}: ${cuerpo.slice(0, 200)}`);
  }
  return res.json();
}
```

2.2. Reescribe `llamarClaude` para usarla (mismo comportamiento, sin fetch
propio):

```js
async function llamarClaude(userPrompt) {
  const data = await llamarMessagesAPI({
    max_tokens: 1024,
    system: SYSTEM_MENTOR,
    messages: [{ role: 'user', content: userPrompt }],
  });
  if (!data || data.stop_reason === 'refusal') return null;
  const bloque = (data.content ?? []).find((b) => b.type === 'text');
  return bloque?.text?.trim() ?? null;
}
```

2.3. Reescribe `llamarApi` igual: elimina su fetch y su manejo de `!res.ok`;
obtén `data` con `await llamarMessagesAPI({ max_tokens: maxTokens, system:
systemFinal, messages: mensajes })`; si `!data` devuelve null; conserva
INTACTO todo lo demás (systemFinal con schema, refusal, extracción de JSON).

2.4. Añade al final de la sección de cuentas:

```js
/**
 * Prueba la cuenta activa con una llamada mínima (1 token). Devuelve
 * { ok, mensaje } SIEMPRE — jamás lanza. Vive en la tarjeta de Ajustes:
 * no toca ninguna otra superficie (cero degradación sin IA, §0.7).
 */
export async function probarCuenta() {
  const cuenta = cuentaActiva();
  if (!cuenta?.apiKey) return { ok: false, mensaje: 'No hay cuenta activa: agrega una API key primero.' };
  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': cuenta.apiKey,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({ model: MODEL, max_tokens: 1, messages: [{ role: 'user', content: 'ping' }] }),
    });
    if (res.ok) return { ok: true, mensaje: `✓ Cuenta funcionando (${MODEL}).` };
    const cuerpo = await res.text().catch(() => '');
    if (res.status === 401) return { ok: false, mensaje: 'API 401: la key no es válida. Debe ser una API key de platform.claude.com (empieza con sk-ant-).' };
    if (res.status === 400 && /credit/i.test(cuerpo)) return { ok: false, mensaje: 'API 400: tu Console no tiene saldo. Recarga crédito en platform.claude.com → Billing.' };
    if (res.status === 404) return { ok: false, mensaje: `API 404: tu cuenta no tiene acceso al modelo ${MODEL}.` };
    if (res.status === 429) return { ok: false, mensaje: 'API 429: límite de velocidad; espera un minuto y reintenta.' };
    return { ok: false, mensaje: `API ${res.status}: ${cuerpo.slice(0, 160)}` };
  } catch {
    return { ok: false, mensaje: 'Sin respuesta de api.anthropic.com (¿red, VPN o bloqueador de contenido?).' };
  }
}
```

## PASO 3 — Botón «Probar la cuenta» (index.html + app.js)

3.1. `index.html`: dentro de la tarjeta "Potenciar con Claude", en el
`<div class="mentor-config">` que contiene `btn-cuenta-agregar`, añade DESPUÉS
de ese botón:

```html
<button id="btn-cuenta-probar" class="secundario">Probar la cuenta</button>
```

3.2. `js/app.js`: añade `probarCuenta` al import de `./aiMentor.js`. En
`configurarMentorUI()`, después del listener de `btn-cuenta-agregar`, añade:

```js
$('btn-cuenta-probar').addEventListener('click', async () => {
  $('mentor-estado').textContent = 'Probando la cuenta…';
  const r = await probarCuenta();
  $('mentor-estado').textContent = r.mensaje;
});
```

3.3. En el listener existente de `btn-cuenta-agregar`, después de la línea
`renderizarCuentas();`, añade:

```js
if (!creada.apiKey.startsWith('sk-ant-')) {
  $('mentor-estado').textContent =
    'Aviso: la key no empieza con sk-ant- — verifica que sea una API key de la Console (no una contraseña de claude.ai). Usa «Probar la cuenta».';
}
```

## PASO 4 — problemFactory.js usa la puerta única

4.1. Cambia el import a:
`import { cuentaActiva, mentorDisponible, llamarMessagesAPI } from './aiMentor.js';`

4.2. Elimina las constantes `API_URL` y `MODEL` del archivo.

4.3. Dentro del `try` de `generarVariante`, sustituye el bloque
`const res = await fetch(...)` … `if (!res.ok) return null;` …
`const data = await res.json();` por:

```js
    const data = await llamarMessagesAPI({
      max_tokens: 16000,
      thinking: { type: 'adaptive' },
      system: SYSTEM_FACTORY,
      output_config: { format: { type: 'json_schema', schema: SCHEMA_VARIANTE } },
      messages: [{ role: 'user', content: userPrompt }],
    });
    if (!data) return null;
```

Conserva intactas las líneas de `refusal`/`max_tokens` y todo lo posterior.
El `catch` externo sigue devolviendo null (fallback silencioso intacto).

## PASO 5 — storage.js: diagnóstico + cuota segura

5.1. En `DEFAULTS`, añade (NO lo añadas a CLAVES_SYNC):

```js
  // Registro local de avisos técnicos (ring buffer 50). Para depurar fallos
  // que por diseño son silenciosos (sync, IA). Solo este dispositivo.
  diagnostico: [],
```

5.2. Añade después de `resetTotal()`:

```js
/**
 * Anota un aviso técnico. Usa setItem crudo con try/catch propio: jamás
 * recursa en save() ni tumba al llamador (el diagnóstico nunca rompe nada).
 */
export function registrarDiagnostico(origen, mensaje) {
  try {
    const lista = JSON.parse(localStorage.getItem(key('diagnostico')) ?? '[]');
    lista.push({ ts: new Date().toISOString(), origen, mensaje: String(mensaje).slice(0, 300) });
    localStorage.setItem(key('diagnostico'), JSON.stringify(lista.slice(-50)));
  } catch {
    // Nada: el diagnóstico es lo único que puede perderse en silencio.
  }
}
```

5.3. Sustituye `save()` ENTERA por:

```js
export function save(name, value) {
  const json = JSON.stringify(value);
  try {
    localStorage.setItem(key(name), json);
  } catch {
    // LocalStorage lleno: podar lo más pesado (archivo de sesiones) y
    // reintentar UNA vez. Si aun así falla, registrar sin lanzar: una
    // excepción a mitad de completarSesion() dejaría estado parcial.
    try {
      const archivadas = JSON.parse(localStorage.getItem(key('sesionesArchivadas')) ?? '[]');
      if (Array.isArray(archivadas) && archivadas.length > 100) {
        localStorage.setItem(key('sesionesArchivadas'), JSON.stringify(archivadas.slice(-100)));
      }
      localStorage.setItem(key(name), json);
    } catch {
      registrarDiagnostico('storage', `No se pudo guardar «${name}»: LocalStorage lleno.`);
    }
  }
}
```

5.4. Instrumenta EXACTAMENTE estos catch vacíos (añade la línea de registro,
sin cambiar nada más; importa lo necesario):
- `js/sync.js` → catch de `sincronizar()`: cámbialo a `catch (e)` y dentro
  `Storage.registrarDiagnostico('sync', e.message);`
- `js/hintSystem.js` → catch de `solicitarHint`: `catch (e)` +
  `registrarDiagnostico('mentor-hint', e.message);` (añade
  `registrarDiagnostico` al import de storage.js).
- `js/app.js` → en los TRES catch de mentor (el de `enviarMensajeMentor`, el
  del change de `input-descon-foto` y el del click de `btn-revision-pedir`):
  `catch (e)` + `Storage.registrarDiagnostico('mentor', e.message);` como
  primera línea del catch, conservando el mensaje de UI existente.

## PASO 6 — Tarjeta «Diagnóstico» en el Dashboard

6.1. `index.html`: después de la tarjeta "Potenciar con Claude" (antes de
cerrar `vista-dashboard`), añade:

```html
      <article class="tarjeta">
        <h2>Diagnóstico</h2>
        <p class="nota-privacidad">
          Últimos avisos técnicos de este dispositivo (jamás se suben).
          Útil si el mentor o la sincronización no responden.
        </p>
        <div id="diagnostico-lista" class="lista-estrategias"></div>
      </article>
```

6.2. `js/app.js`: al FINAL de `renderizarDashboard()`, añade:

```js
  const diag = $('diagnostico-lista');
  diag.innerHTML = '';
  const avisos = Storage.load('diagnostico').slice(-15).reverse();
  if (!avisos.length) {
    const p = document.createElement('p');
    p.className = 'fila';
    p.textContent = 'Sin avisos registrados.';
    diag.appendChild(p);
  } else {
    avisos.forEach((d) => {
      const p = document.createElement('p');
      p.className = 'fila';
      p.textContent = `${d.ts.slice(0, 16).replace('T', ' ')} · ${d.origen} · ${d.mensaje}`;
      diag.appendChild(p);
    });
  }
```

## PASO 7 — api.js: eventos idempotentes + aviso de sesión inválida

7.1. En `subirEventos`, añade `uid: e.uid,` a las filas (entre `device_id` y
`tipo`) y cambia la última línea por:

```js
  await rest('POST', 'events?on_conflict=uid', filas, 'resolution=ignore-duplicates');
```

7.2. En `tokenVigente()`, dentro del catch del refresh, entre
`remove('sesionSupabase');` y `return null;`, añade:

```js
      try {
        window.dispatchEvent(new CustomEvent('cps:sesion-invalida'));
      } catch {
        // Entornos sin window.
      }
```

## PASO 8 — sync.js: bajada continua (convergencia multi-dispositivo)

8.1. Extrae de `adoptarOUnir()` el bloque de unión a una función nueva,
colocada justo encima de `claveSesion`:

```js
/**
 * Une el estado remoto al local. Los escalares de perfil/preferencias se
 * conservan locales (este dispositivo es la verdad inmediata); las rachas
 * se recomputan del historial unido.
 */
function unirRemoto(remoto) {
  unirLista('historial', remoto.historial, claveSesion);
  unirLista('pisosMinimos', remoto.pisosMinimos, (p) => p.uid ?? `${p.fecha}|${p.problemId}`);
  unirLista('sesionesArchivadas', remoto.sesionesArchivadas, claveSesion);
  unirLista('problemasGenerados', remoto.problemasGenerados, (p) => `gen-${p.id}`);
  unirEstudio(remoto.estudio);
  unirInsignias(remoto.insignias);
  unirRevisiones(remoto.revisiones);
  recomputarRachaEntrenamiento();
  recomputarRachaEstudio();
}
```

`adoptarOUnir()` queda igual pero su rama final llama `unirRemoto(remoto);
return 'unido';`. En la rama de adopción (`!localConDatos`), DESPUÉS del
forEach de CLAVES_SYNC y ANTES del `return 'adoptado';`, añade:

```js
    // Lo en-curso es de ESTE dispositivo: jamás se adopta un quiz o examen
    // a medias de otro aparato.
    Storage.update('estudio', (e) => {
      e.quizEnCurso = null;
      e.examenEnCurso = null;
      return e;
    });
```

8.2. En `sincronizar()`, entre el bucle de lotes del outbox y
`await Api.subirSnapshot(...)`, inserta:

```js
    // Bajada continua: el snapshot remoto se UNE antes de subir el propio.
    // Dos dispositivos con sesión viva convergen sin re-login y el snapshot
    // del servidor nunca retrocede (sin esto, el último en subir borraba el
    // progreso del otro hasta el siguiente login).
    try {
      const snap = await Api.descargarSnapshot();
      if (snap?.estado) unirRemoto(snap.estado);
    } catch (e) {
      Storage.registrarDiagnostico('sync', `bajada: ${e.message}`);
      // La subida continúa; la unión se reintenta en el próximo disparo.
    }
```

8.3. En `iniciar()`, después del listener de `'online'`, añade:

```js
  // Al volver a la pestaña tras ≥5 min, traer lo que otros dispositivos
  // hayan subido (la bajada continua de sincronizar() hace la unión).
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState !== 'visible') return;
    const ultima = Storage.load('ultimaSync');
    if (!ultima || Date.now() - new Date(ultima).getTime() > 5 * 60_000) sincronizar();
  });
  window.addEventListener('cps:sesion-invalida', () => avisar());
```

8.4. `js/app.js`, en `init()`, inmediatamente después de `Sync.iniciar();`:

```js
  // Una sincronización pudo unir progreso de otro dispositivo: refrescar
  // SOLO el header (repintar la sesión a mitad de un forcejeo molestaría).
  window.addEventListener('cps:sync-completada', () => Study.actualizarHeaderRachas());
```

## PASO 9 — Micro-arreglo exacto en study.js

En `renderPreguntaQuiz()`, la línea
`btnSig.textContent = qc.indice + 1 < u.banco.length ? 'Siguiente pregunta' : 'Cerrar evaluación';`
debe comparar contra `ids.length` (en un repaso el subconjunto es menor que el
banco y la etiqueta mentía en la última pregunta):

```js
    btnSig.textContent = qc.indice + 1 < ids.length ? 'Siguiente pregunta' : 'Cerrar evaluación';
```

## PASO 10 — sw.js

Sube `VERSION` de `'cogitoergosum-v21'` a `'cogitoergosum-v22'`. NO toques el
SHELL (no hay archivos nuevos del shell: el SQL no se precachea).

## PASO 11 — VERIFICACIÓN (toda en verde antes de documentar)

```sh
cd /Users/EdgarDevice/Desktop/ProyectoX
for f in js/*.js sw.js; do node --check "$f"; done
python3 -c "import json,glob; [json.load(open(p)) for p in glob.glob('data/*.json')]; print('JSON OK')"
python3 - <<'EOF'
import re, os
shell = re.findall(r"'([^']+)'", open('sw.js').read().split('const SHELL')[1].split('];')[0])
faltan = [s for s in shell if s != './' and not os.path.exists(s)]
print('SHELL OK' if not faltan else f'FALTAN: {faltan}')
EOF
# Cruce de IDs nuevos:
grep -c "btn-cuenta-probar\|diagnostico-lista" index.html   # debe dar 2
grep -c "btn-cuenta-probar\|diagnostico-lista" js/app.js    # debe dar ≥2
# Confirmaciones de cableado:
grep -n "llamarMessagesAPI" js/aiMentor.js js/problemFactory.js
grep -n "on_conflict=uid" js/api.js
grep -n "unirRemoto" js/sync.js          # ≥3 apariciones (def + 2 llamadas)
grep -n "registrarDiagnostico" js/storage.js js/sync.js js/hintSystem.js js/app.js
```

Además: arranca `python3 -m http.server 8000` y verifica en headless o
navegador que la app carga sin errores de consola y que el Dashboard muestra
la tarjeta «Diagnóstico» con "Sin avisos registrados".

## PASO 12 — Documentación

En `HANDOFFCES.md`, antes de «### Convenciones que NO se negocian», añade
`### Bitácora 2026-06-12 (6) — oleadas 1-3 ejecutadas (sincronización convergente + mentor diagnosticable)`
resumiendo: SQL de parches (FK usado_por → set null; events.uid unique),
bajada continua en sincronizar() con unirRemoto(), disparador por
visibilitychange (≥5 min), eventos idempotentes on_conflict=uid,
llamarMessagesAPI como puerta única (problemFactory unificado), errores de la
API con status+cuerpo, botón «Probar la cuenta» + aviso sk-ant-, save() con
poda ante cuota, registro cps_diagnostico (fuera de CLAVES_SYNC) + tarjeta en
Dashboard, etiqueta del repaso corregida, sw.js v22. Marca además las
casillas de las oleadas 1-3 en el punto 9 de «QUÉ FALTA» (§5.4).

## PASO 13 — Commit y push

```sh
git add js/ index.html sw.js supabase/schema-parches-2026-06-12.sql HANDOFFCES.md
```

NO incluyas `.claude/settings.local.json`. Mensaje EXACTO:

```
Sincronización convergente + mentor diagnosticable + cuota segura

Bajada continua: cada sincronización une el snapshot remoto antes de subir
(dos dispositivos convergen sin re-login y el snapshot jamás retrocede).
Eventos idempotentes por uid (on_conflict=ignore-duplicates; SQL en
supabase/schema-parches-2026-06-12.sql, que también arregla la FK de
invitaciones.usado_por que rompía borrar_mi_cuenta). Mentor: errores de la
API con status y cuerpo, botón «Probar la cuenta», aviso de prefijo sk-ant-,
y problemFactory unificado en la puerta única llamarMessagesAPI.
storage.save tolera cuota llena con poda; registro de diagnóstico local
visible en el Dashboard. sw.js v22.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Push a `main`.

## PASO 14 — Instrucciones finales al usuario (imprímelas tal cual)

1. Recarga la app (el SW v22 recarga solo una vez) y en Dashboard →
   «Potenciar con Claude» pulsa **Probar la cuenta**: el mensaje te dirá la
   causa exacta de por qué el mentor no respondía (401 = key equivocada,
   400 = sin saldo en la Console, ✓ = ya funciona).
2. Recuerda: la key vive por dispositivo y por origen — la que pegaste en
   localhost NO existe en imgoingsavage.github.io ni en el celular.
3. Prueba de convergencia: dos navegadores con tu cuenta, cierra una sesión
   de entrenamiento en uno, en el otro pulsa «Sincronizar ahora» (o vuelve a
   la pestaña tras 5 min) → racha e historial deben aparecer SIN re-login.
4. El reset de usuarios de prueba y el login con Google quedan para la
   siguiente sesión (requieren decisiones tuyas); la FK ya quedó arreglada
   para que «Borrar cuenta» funcione siempre.
