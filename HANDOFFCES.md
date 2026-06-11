# HANDOFF — CogitoErgoSum: de app local a plataforma multi-usuario

Extensión del `HANDOFF.md` existente (2026-06-10). Este documento NO lo
sustituye: los caminos 1 (Entrenamiento) y 2 (Modo Estudio) descritos ahí
siguen siendo intocables en su pedagogía y mecánicas. Aquí se añaden las
secciones §3.12 a §3.15: identidad, motivación, escalabilidad e integración
de Claude por usuario. Léelo junto con `claude.md` (espec. pedagógica) y
`HANDOFF.md` (estado del código).

Fecha: 2026-06-11. El proyecto pasa a llamarse **CogitoErgoSum**.

---

## §0. CONSTITUCIÓN DE COGITOERGOSUM (dictada por el usuario; es LEY)

Toda decisión de producto, diseño, código o contenido se valida contra estos
principios. Si una tarea de este documento entra en conflicto con ellos, los
principios ganan y la tarea se rediseña.

1. **El amor es al proceso de pensar, no al resultado.** La app celebra el
   forcejeo, la lucha y el esfuerzo sostenido. Resolver o no resolver es
   secundario; pensar bien es lo primario.
2. **El error es parte del proceso de mejora.** Fallar nunca produce castigo,
   culpa, pérdida visible ni lenguaje negativo. Tras un fallo, la app valida
   el intento ("forcejeaste 20 minutos con un nivel 4 — eso es entrenamiento
   real") y reencuadra hacia la siguiente oportunidad de aprendizaje.
3. **La competencia más importante es contigo mismo.** Toda métrica
   comparativa por defecto compara al usuario con su propio pasado. Si
   mejoraste, la app te lo hace saber con datos concretos.
4. **La red de amigos existe para compartir una pasión, no para establecer
   dominancia intelectual.** Los logros de un amigo se presentan como fuente
   de inspiración, admiración y reconocimiento al trabajo de un par — nunca
   como ranking, derrota o presión.
5. **Hábitos saludables y sostenibles en el tiempo.** Nada de mecánicas que
   erosionen la concentración o el pensamiento autónomo (anti-TikTok). De las
   apps masivas se toma SOLO lo bueno: interfaz atractiva, identidad,
   sensación de pertenecer a un lugar bonito pensado para gente que ama
   razonar.
6. **Cero dinero.** No hay cobros, suscripciones, monedas, tienda ni ningún
   feature/insignia/avatar/derivado que requiera pago. Todo se gana con
   esfuerzo sostenido, disciplina, paciencia y amor.
7. **La IA es siempre opcional.** Ninguna funcionalidad esencial puede
   degradarse si el usuario decide no conectar su cuenta de Claude.

### §0.1 Reglas anti-patrón-oscuro (prohibiciones explícitas para el agente)

NUNCA implementar, ni siquiera como "mejora de retención":

- Recompensas variables/aleatorias (loot boxes, cofres, ruletas, drops
  sorpresa de cosméticos). Toda recompensa es determinista y anunciable:
  "esto se gana así".
- Feeds infinitos, autoplay, o cualquier superficie de scroll sin fondo.
- Leaderboards globales o entre amigos, ligas, divisiones, posiciones.
- Notificaciones de comparación ("X te superó", "vas perdiendo contra Y").
- Notificaciones de urgencia falsa, culpa o pérdida ("¡tu racha está a punto
  de morir!", "Cogito está triste"). Máximo 1 notificación/día, en horario
  elegido por el usuario, con contenido útil y neutro ("tu revisión de hoy
  está lista", "tu sesión de las 7:00 te espera").
- Contadores de "amigos activos ahora", indicadores de presencia en línea,
  doble palomita, "visto".
- Temporizadores de oferta, eventos FOMO de tiempo limitado.
- Penalizaciones visibles por fallo (perder puntos, vidas, corazones).
- Cualquier dark pattern de retención en el flujo de borrar cuenta o
  desactivar notificaciones (debe ser de 2 clics, sin súplicas).

---

## §1. IDENTIDAD VISUAL — "La biblioteca" (nueva dirección de diseño)

Brief del usuario: la app debe sentirse **elegante, minimalista y racional, como
estar en la Biblioteca de Alejandría o la Biblioteca Vasconcelos** — un lugar
donde la relajación, el pensamiento y el esfuerzo mental sostenido son lo más
importante, y donde quien entra siente que el sitio fue pensado para alguien
que disfruta razonar.

La base actual (dark mode Obsidian/Linear) es compatible; se refina, no se
reescribe. Direcciones concretas:

- **Metáfora rectora**: sala de lectura nocturna. Fondo oscuro profundo y
  cálido (no negro puro: pensar en piedra volcánica de Vasconcelos o madera
  oscura), una sola fuente de "luz de lámpara de escritorio" como acento
  (ámbar/dorado tenue) reservada para los momentos de logro y las rachas.
  El acento índigo/violeta actual puede conservarse para lo interactivo.
- **Tipografía con alma de imprenta**: display serif clásica para títulos de
  problemas y momentos ceremoniales (revelado de solución, ficha de moraleja,
  insignias) — p. ej. una serif tipo old-style vía `@font-face` con archivo
  local (sin CDNs, convención del proyecto: cero dependencias externas;
  descargar una fuente libre tipo EB Garamond / Cormorant y servirla desde
  `/assets/fonts/`). Sans actual para UI funcional; monoespaciada para
  números y timer (ya existe).
- **Ornamento tipográfico, no decorativo**: separadores con florones simples
  (❧, ⁂), numeración de problemas en versalitas, citas breves de
  matemáticos/filósofos en pantallas vacías y de carga (rotación curada en un
  JSON local, en español, con autor; jamás motivacionales corporativas).
- **Ritmo lento deliberado**: las transiciones son serenas (200-300 ms,
  ease-out), jamás rebotes ni confeti. El único "momento de teatro" permitido:
  el revelado de una insignia nueva y el cierre de un examen de bloque —
  una animación sobria de tinta/sello.
- **`prefers-reduced-motion` respetado** en todo; foco de teclado visible;
  contraste AA mínimo.
- El nombre **CogitoErgoSum** aparece en el header con su propia marca
  tipográfica (wordmark serif). El subtítulo permanente de la app:
  "*Entrenamiento del pensamiento*" (o el que el usuario decida después).

Entregable de esta sección: actualizar `css/styles.css` + `index.html`
(wordmark, fuentes locales, tokens de color documentados como variables CSS
al inicio del archivo) sin tocar la estructura de vistas existente.

---

## §2. SISTEMA DE MOTIVACIÓN (§3.13 del plan) — "dopamina del proceso"

Marco teórico obligatorio: **Self-Determination Theory** (competencia,
autonomía, relación) + hábitos sostenibles (señal→rutina→recompensa con
recompensa intrínseca). Se premia el PROCESO; el acierto es consecuencia.

### §2.1 Insignias ("Sellos de la biblioteca")

Determinísticas, gratuitas, ganadas por esfuerzo. Tres familias:

**Familia Forcejeo (proceso puro — la más importante):**
- *Forcejeo limpio*: cerrar un problema nivel ≥4 sin pistas (resuelto o no:
  cuenta el proceso completo con desconstrucción ≥400 chars).
- *Tinta abundante*: 10 desconstrucciones de ≥400 caracteres.
- *El que mira atrás*: 25 fichas de moraleja completas (moraleja+disparador).
- *Incubadora*: 5 sesiones donde se usó la pausa de incubación y se cerró
  el problema en una sesión posterior.
- *Paciencia de piedra*: 10 sesiones que agotaron el timer completo de 20 min
  antes de revelar.

**Familia Mejora contra ti mismo:**
- *Fénix*: resolver en revisión espaciada un problema que antes fallaste.
  (Insignia repetible: lleva contador ×N.)
- *Ojo de halcón*: 10 predicciones de jugada correctas acumuladas; nivel II a
  las 50; nivel III a las 100 (la "métrica de oro" del PDF).
- *Marea que sube*: superar tu propia tasa de disparadores reconocidos del
  mes anterior.
- *Cartógrafo*: primera ficha de moraleja en cada una de las 4 estrategias;
  *Cartógrafo mayor* al cubrir las 12 heurísticas del catálogo.

**Familia Constancia:**
- Sellos de racha 🔥 a 7/30/100/365 días (entrenamiento) y 📘 ídem (estudio).
- *Piso firme*: 5 pisos mínimos completados (premia salvar el hábito en días
  malos — exactamente lo contrario a castigar el fallo).
- *Lector disciplinado*: aprobar cada examen de bloque del Modo Estudio.

Reglas de presentación: las insignias NO se muestran como checklist por
ganar (eso convierte el estudio en grinding). Existe una vitrina ("Mi
estante") donde aparecen las ganadas con fecha y la historia de cómo se ganó;
las no ganadas son siluetas sin nombre ("aún por descubrir"). El revelado de
una insignia ocurre en la pantalla de cierre de sesión, nunca interrumpe el
forcejeo.

### §2.2 Racha y fallo (refinar lo existente, no reemplazar)

- Mantener el piso mínimo actual tal cual (mejor diseñado que el streak
  freeze de Duolingo: exige recall real).
- **Fresh start tras romper racha**: pantalla serena ("Las rachas se rompen;
  los hábitos se reconstruyen. Tu mejor racha fue de N días — está guardada
  en tu estante.") + invitación a una meta corta de 3 días. Guardar
  `mejorRachaHistorica` para que romper la racha nunca borre el logro.
- **Lenguaje de fallo en TODA la app**: auditar strings existentes. Prohibido
  "incorrecto/fallaste/error" como veredicto seco; usar el patrón
  validación-del-proceso + dato + reencuadre: "No salió esta vez — invertiste
  22 min y tu desconstrucción identificó la restricción clave. Este problema
  volverá en 3 días con otra cara." (las variantes isomórficas ya existen).

### §2.3 Avatar evolutivo ("El pensador")

- Avatar SVG generado por capas, estilo grabado/línea sobrio coherente con §1
  (NADA cartoon). Base elegible al crear cuenta (rasgos neutros, inclusivos).
- **Los aditamentos se ganan, jamás se compran ni se sortean**: cada
  heurística dominada (ver rating §2.5) añade un elemento simbólico —
  ejemplos: compás (geometría/dibujar), balanza (invariantes), espejo
  (simetría/inversión), llave (hacia atrás), constelación (patrones), pluma
  (25 fichas), laurel discreto por exámenes de bloque. Mapa completo
  insignia→capa en `data/avatar.json`.
- El avatar es la representación del usuario ante sus amigos: cuenta la
  historia de SU trabajo. Tooltip al pasar el cursor por cada elemento:
  "Balanza — dominó Invariantes el 12/08/2026".

### §2.4 Capa social ("El claustro") — inspiración, no dominancia

- **Amistades simétricas por invitación** (código/enlace). Sin sugerencias
  algorítmicas de contactos, sin importar agenda.
- Lo único visible de un amigo es su **perfil-vitrina**: avatar, estante de
  insignias, rachas actuales y mejor racha, y (opt-in) su "moraleja de la
  semana" — una ficha que él decida compartir. NADA de actividad en tiempo
  real, ni qué problema hace, ni cuántos resolvió, ni puntajes.
- Interacción única permitida: **"Reconocimiento"** (un gesto, p. ej. ❧):
  "Edgar reconoció tu insignia *Fénix*". Sin comentarios, sin likes
  acumulables públicos, sin números de popularidad.
- Modo **"Pensar juntos"** (fase posterior, opcional): dos amigos acuerdan
  atacar el MISMO problema cada quien por su lado; al cerrar ambos, la app
  les muestra las desconstrucciones y moralejas del otro lado a lado. No hay
  ganador: el premio es ver otra mente trabajar. (Esto materializa "compartir
  la pasión".)
- Todo lo social es opt-in y la app es 100% funcional sin un solo amigo.

### §2.5 Rating por heurística (ya previsto en §3.9.2 del HANDOFF)

Sube de prioridad porque alimenta avatar e insignias: evolucionar la
dificultad global 1-5 a un nivel por estrategia/heurística (estilo Alcumus,
datos ya disponibles en `historial`). "Dominada" = definir umbral simple y
documentarlo (p. ej. ≥5 sesiones con score ≥70 en esa heurística dentro de
la zona de dificultad del usuario). El nivel por heurística es PRIVADO por
defecto (regla §0.4: no es instrumento de comparación).

### §2.6 Control del temporizador de reflexión (pedido del usuario, 2026-06-11)

Dos cambios sobre `js/timer.js` y la tarjeta del temporizador, cuidando que
el gating pedagógico no se debilite:

1. **Botón de pausa/reanudar.** Una vez iniciado un problema, el usuario
   puede pausar el cronómetro (interrupciones de la vida real). Detalles de
   implementación:
   - El timer actual se basa en timestamp persistido, no en contador: la
     pausa se implementa guardando `pausadoEn` y acumulando
     `tiempoPausadoTotal` en la asignación; el tiempo transcurrido efectivo
     = ahora − inicio − tiempoPausadoTotal. Sobrevive recargas igual que hoy.
   - La pausa NUNCA adelanta el desbloqueo de la solución: solo lo pospone
     (el gating exige minutos efectivos de forcejeo, así que pausar es
     pedagógicamente neutro).
   - Los checkpoints metacognitivos (~8 y ~16 min) se calculan sobre tiempo
     efectivo, de modo que una pausa no los salte.
   - UI sobria: icono ⏸/▶ junto al cronómetro; en pausa, la tarjeta muestra
     "En pausa — tu forcejeo te espera" (sin culpa, regla §0.1).
   - Registrar en el historial de la sesión cuántas pausas hubo y su
     duración total (dato para el Dashboard, no para penalizar).

2. **Duración configurable del temporizador, de 20 a 120 minutos.**
   - El valor por defecto sigue siendo 20 min (la dosis del PDF); el usuario
     puede ajustarlo ANTES de iniciar el problema (selector en la tarjeta
     del temporizador o en Ajustes como preferencia persistente
     `cps_preferencias.duracionTimer`).
   - Rango permitido: mínimo 20, máximo 120 minutos (pasos de 5). El mínimo
     NO baja de 20: el piso de forcejeo es la regla pedagógica central de
     `claude.md` y no se negocia desde la UI.
   - Una vez iniciado el problema, la duración elegida queda fija para esa
     asignación (se persiste en la asignación, como hoy); no se puede
     recortar a mitad de sesión para desbloquear antes. Sí se puede
     EXTENDER en caliente (botón "+10 min") si el usuario quiere seguir
     forcejeando — extender nunca rompe el gating.
   - Los checkpoints metacognitivos escalan proporcionalmente a la duración
     elegida (≈40% y ≈80% del total) en lugar de quedarse fijos en 8/16 min.
   - `tiempo_estimado` de cada problema puede sugerir una duración inicial
     ("este problema sugiere 30 min") sin imponerla.

---

## §3. ESCALABILIDAD MULTI-USUARIO (§3.12 del plan)

### §3.1 Requisitos del usuario

- Corre en computadora, tablet y celular; accesible para cualquiera.
- Login propio de CogitoErgoSum; métricas y progreso resguardados.
- Sin pagos de ningún tipo.
- Supabase preocupa por la pausa de proyectos inactivos → resolver.

### §3.2 Decisión de plataforma cliente: PWA

La app actual (HTML/CSS/JS vanilla, responsive) se convierte en **Progressive
Web App**: `manifest.json` (nombre CogitoErgoSum, iconos, theme color de §1)
+ service worker con precache de la app shell y los JSON de datos. Resultado:
instalable en iOS/Android/escritorio desde el navegador, funciona offline
(coherente con la arquitectura offline-first de §3.4) y no exige tiendas de
apps ni build step. CSS: auditar breakpoints táctiles (objetivos ≥44 px,
textarea de desconstrucción cómoda en móvil, timer visible sin scroll).

### §3.3 Backend: PocketBase (primario) / Supabase con keep-alive (alterno)

> **✅ DECISIÓN TOMADA (usuario, 2026-06-11): Opción B — Supabase con cron
> keep-alive.** El playbook de ejecución paso a paso está en §5.2. La Opción A
> se conserva solo como referencia si Supabase mostrara límites reales.

**Opción A — PocketBase autohospedado (descartada 2026-06-11).**
Un solo binario (Go + SQLite) que trae auth (email+password, verificación,
reset), API REST/realtime, panel admin y reglas de acceso por colección.
Encaja con la filosofía del proyecto: cero frameworks, cero dependencias de
plataforma, nunca se pausa, exportable (la BD es un archivo SQLite).
Hospedaje: VPS pequeño (Hetzner/DigitalOcean ~4-6 USD/mes) o PikaPods
(~1-2 USD/mes, PocketBase con un clic). El frontend estático puede vivir en
el mismo VPS detrás de Caddy (HTTPS automático) o gratis en Cloudflare
Pages/GitHub Pages apuntando al backend.

**Opción B — ✅ ELEGIDA: Supabase, mitigando la pausa.** Si se prefiere Postgres
gestionado: el plan gratuito pausa proyectos tras ~1 semana sin tráfico. La
mitigación estándar y suficiente: un **GitHub Action con cron** (cada 2-3
días) que hace un `select` trivial a una tabla `keepalive` con la anon key
— mantiene el proyecto activo indefinidamente; documentar el workflow YAML
en el repo. (Con usuarios reales activos el problema desaparece solo; el
cron cubre los valles.)

El módulo de sincronización (§3.4) debe escribirse contra una interfaz
propia (`js/api.js`) con las ~8 operaciones que la app necesita, de modo que
cambiar PocketBase↔Supabase sea reemplazar un solo archivo.

### §3.4 Sincronización offline-first (NO romper lo local)

Principio: **LocalStorage sigue siendo la verdad inmediata**; el servidor es
respaldo y puente entre dispositivos. La app jamás bloquea por falta de red.

- `storage.js` es ya la única puerta a LocalStorage (decisión previa
  excelente): interceptar ahí. Cada `guardar()` relevante encola un evento en
  `cps_outbox`; un nuevo `js/sync.js` drena la cola cuando hay conexión y
  sesión iniciada.
- Modelo de datos en servidor: **event log append-only** + snapshot.
  - `events`: {user_id, device_id, ts, tipo, payload} — sesiones cerradas,
    pisos mínimos, unidades de estudio, exámenes, insignias ganadas.
  - `snapshots`: último estado computado del perfil por usuario (para
    arranque rápido en un dispositivo nuevo).
  - Resolución de conflictos pragmática: el historial se UNE (append-only no
    colisiona); para contadores derivados (racha, niveles) se RECOMPUTAN del
    event log en el cliente — una sola función `derivarPerfil(eventos)`
    compartida. Nada de CRDTs: el caso real es 1 persona, 2-3 dispositivos.
- Primer login en dispositivo nuevo: descargar snapshot+eventos → poblar
  LocalStorage → la app funciona igual que hoy.
- Migración del usuario actual (Edgar): pantalla única "importar mi progreso
  local a mi cuenta" que sube el LocalStorage existente como eventos
  retroactivos. NO perder ni un día de racha en la migración.

### §3.5 Cuentas y privacidad

- Registro con email + contraseña (PocketBase lo trae); username público
  elegible. Sin login social de terceros (menos dependencias).
- Privacidad por defecto: perfil invisible salvo para amigos aceptados.
- Exportar mis datos (JSON) y borrar cuenta: visibles, de 2 clics, sin
  fricción (regla §0.1).
- Las API keys de Claude del usuario NUNCA se suben al servidor (ver §4).

---

## §4. INTEGRACIÓN DE CLAUDE POR USUARIO (§3.14 del plan)

**Restricción de política verificada (2026):** Anthropic prohíbe que apps de
terceros usen el login/OAuth de suscripciones de Claude (Free/Pro/Max); la
vía oficial para terceros es la autenticación con API key emitida en la
Claude Console. Por tanto, "conectar tu cuenta de Claude" en CogitoErgoSum
significa: **el usuario pega su propia API key**, no un botón "Sign in with
Claude". Documentarlo así en la UI para no prometer lo imposible.

Diseño (evoluciona el gestor multi-cuenta ya implementado en `aiMentor.js`):

1. Tras iniciar sesión en CogitoErgoSum, en Ajustes existe la sección
   "Potenciar con Claude (opcional)": explica qué habilita (hints
   inteligentes dinámicos, chat socrático, variantes isomórficas frescas),
   deja pegar la API key y enlaza a la guía de cómo obtenerla en la Console.
2. **La key vive SOLO en el dispositivo** (LocalStorage, como hoy) y las
   llamadas van directo del navegador a `api.anthropic.com` (mecanismo
   actual con `anthropic-dangerous-direct-browser-access`, aceptable porque
   es la key del propio usuario en su propio navegador). La key NO se
   sincroniza al backend de CogitoErgoSum: si el usuario usa 2 dispositivos,
   la pega en cada uno (decisión consciente de seguridad; explicárselo).
3. **Cero degradación sin Claude** (ley §0.7): ya es así por diseño (fallback
   silencioso a hints estáticos curados). Mantenerlo como invariante en todo
   código nuevo: cada feature IA debe tener su camino estático o simplemente
   no aparecer (el chat socrático no se muestra si no hay key — no se
   muestra "bloqueado", no existe).
4. El **chat socrático** (nuevo): panel lateral durante el forcejeo, system
   prompt heredado de `aiMentor.js` (jamás revela soluciones, pregunta y
   reenfoca; conoce el problema actual y la desconstrucción escrita). Sin
   historial infinito: el chat se archiva con la sesión.
5. Mantener el modelo definido en convenciones (`claude-opus-4-8`) y la regla
   §3.10 del HANDOFF: toda llamada pasa por `cuentaActiva()`.

---

## §5. PLAN DE EJECUCIÓN POR FASES (para el agente)

Orden pensado para que la práctica diaria de Edgar nunca se interrumpa.
Cada fase termina con la app 100% funcional.

**✅ Fase A — Identidad y lenguaje (HECHA 2026-06-11, ver §5.1):**
1. Renombrar a CogitoErgoSum (wordmark, manifest, títulos).
2. Rediseño visual §1 sobre el CSS existente (tokens documentados).
3. Auditoría de lenguaje de fallo (§2.2) en todos los strings.
4. Control del temporizador (§2.6): pausa/reanudar + duración configurable
   20-120 min con extensión en caliente (toca `timer.js`, `app.js` y la
   tarjeta del temporizador; verificar que el gating y los checkpoints
   siguen funcionando tras recarga, en pausa y con duraciones largas).
5. PWA: manifest + service worker + auditoría móvil/tablet.

**✅ Fase B — Motivación local (HECHA 2026-06-11, ver §5.1):**
5. Motor de insignias (`js/badges.js` + `data/badges.json`): evaluación
   declarativa sobre `historial`/`cps_estudio` al cierre de sesión; vitrina
   "Mi estante" en Dashboard; revelado sobrio.
6. `mejorRachaHistorica` + flujo fresh-start (§2.2).
7. Rating por heurística (§2.5) alimentando el avatar.
8. Avatar por capas (`js/avatar.js` + `data/avatar.json`, SVG).

**▸ Fase C — Backend y cuentas (SIGUIENTE; Supabase elegido — playbook en §5.2):**
9. Levantar PocketBase (colecciones: users, events, snapshots, friendships,
   reconocimientos; reglas de acceso por dueño). Alternativa Supabase + cron
   keep-alive documentada.
10. `js/api.js` + `js/sync.js` + outbox en `storage.js` (§3.4).
11. Login/registro UI + migración del progreso local existente.
12. Ajustes: exportar datos, borrar cuenta, notificación diaria opcional
    (Web Push, 1/día máx, hora elegida).

**Fase D — El claustro (social; después de C):**
13. Amistades por código de invitación; perfil-vitrina (avatar, estante,
    rachas, moraleja compartida opt-in).
14. "Reconocimiento" (❧) con notificación dentro de la app (no push).
15. (Posterior, validar con el usuario) "Pensar juntos" (§2.4).

**Verificación continua** (convenciones del HANDOFF se mantienen): español
en todo, `node --check` en cada módulo, JSON validados, cero librerías de
frontend, `storage.js` única puerta a LocalStorage, la IA siempre opcional.
Añadir: probar cada fase con red desconectada (offline-first es requisito,
no accidente) y con `prefers-reduced-motion`.

**Checklist anti-§0.1 antes de cerrar cada fase**: releer las prohibiciones
y confirmar que nada implementado las viola. En caso de duda, preguntar al
usuario antes de implementar.

---

## §5.1 BITÁCORA DE EJECUCIÓN (2026-06-11)

**FASES A Y B COMPLETADAS Y VERIFICADAS.** Detalle de lo implementado:

**Fase A — Identidad y lenguaje:**
1. ✅ Renombre a CogitoErgoSum: wordmark serif + subtítulo "Entrenamiento del
   pensamiento" en el header; `<title>`; manifest.
2. ✅ Rediseño §1: `css/styles.css` reescrito con tokens documentados al
   inicio (piedra volcánica `--bg`, luz de lámpara `--lampara` SOLO para
   logros/rachas/ceremonias, índigo `--acento` para lo interactivo).
   EB Garamond (OFL) servida localmente desde `assets/fonts/*.woff2`
   (subset latin, ~67 KB total) con `@font-face`; serif en títulos de
   problema, solución revelada, insignias y citas. Florón ❧ como separador.
   Citas curadas (16, con autor real, en español) en `data/quotes.json`,
   rotación determinista por día en el pie. Transiciones 200-300 ms
   ease-out; `prefers-reduced-motion` global; `:focus-visible` visible;
   única animación "de teatro": `@keyframes sello` (300 ms) al revelar
   insignia. Puntos de fallo en gráficas ya no son rojos (neutro).
3. ✅ Auditoría de lenguaje de fallo (§2.2): "No lo logré"→"Aún no salió";
   mensaje de validación-del-proceso con datos (min de forcejeo, nivel,
   caracteres escritos) + reencuadre en la pantalla de resultado para
   fallado/parcial (`textoValidacionProceso` en app.js); examen del Modo
   Estudio reencuadrado ("Todavía no — y este intento ya fue entrenamiento
   real…"); cero veredictos secos (verificado por grep).
4. ✅ Timer §2.6: `timer.js` reescrito — pausa/reanudar con `pausadoEn` +
   `msPausadoTotal` (tiempo EFECTIVO; sobrevive recargas), duración
   configurable 20-120 min en pasos de 5 (preferencia persistente
   `cps_preferencias.duracionTimer`, aplica al PRÓXIMO problema; la actual
   queda fija), extensión en caliente +10 min (nunca recorta ni revoca un
   desbloqueo ganado), checkpoints metacognitivos proporcionales (~40% y
   ~80% del total, sobre tiempo efectivo: la pausa no los salta),
   `tiempo_estimado` sugiere sin imponer. Pausas registradas en historial
   (`pausas`, `msPausado`) como dato, jamás penalización.
5. ✅ PWA §3.2: `manifest.webmanifest`, `sw.js` (precache de 27 recursos,
   cache-first + refresco en segundo plano, NUNCA intercepta
   api.anthropic.com), iconos generados localmente (`assets/icons/`,
   SVG + PNG 512/192/180 vía qlmanage), registro en app.js, objetivos
   táctiles ≥44 px y textarea ≥16 px (sin zoom forzado iOS).

**Fase B — Motivación local:**
6. ✅ Motor de insignias: `js/badges.js` + `data/badges.json` (21 sellos en
   3 familias; Fénix y Marea repetibles con contador; mapa
   heurística→tags para Cartógrafo mayor). Evaluación SOLO al cierre
   (sesión, piso, unidad, examen); revelado sobrio en pantallas de cierre;
   vitrina "Mi estante" en Dashboard con siluetas sin nombre (◌ "Aún por
   descubrir"). Para alimentar los sellos, el historial ahora guarda
   `desconstruccionLen`, `incubada`, `duracionMin`, `revisionDe`.
7. ✅ `mejorRachaHistorica` (perfil) y `mejorRachaEstudio` (estudio):
   romper racha nunca borra el logro. Fresh start §2.2: tarjeta serena al
   abrir la app tras romper una racha >0, con meta corta opcional de
   3 días (`perfil.metaCorta`, progreso visible en el cierre de sesión).
   Stat "Mejor racha" en Dashboard.
8. ✅ Rating por heurística §2.5 (`Analytics.ratingPorEstrategia`):
   dominada = ≥5 sesiones con score ≥70 (documentado en el código y en la
   UI); nivel 1-5 = promedio de las últimas 5 sesiones por tramos de 20.
   PRIVADO: solo en Dashboard, con nota explícita.
9. ✅ Avatar "El pensador": `js/avatar.js` + `data/avatar.json` (mapa
   requisito→capa). SVG por capas estilo grabado/línea: base de busto +
   halo de lámpara; capas ganadas — balanza (Invariantes), espejo
   (Inversión), constelación (Patrones), compás (Optimización), llave
   (insignia Fénix), pluma (25 fichas), laurel (exámenes de bloque) — con
   tooltip de historia y fecha.

**Verificación realizada:** `node --check` en los 12 módulos; 6 JSON
validados; cruce bidireccional de IDs HTML↔JS sin huecos; app arrancada en
Chrome headless (problema cargado, timer corriendo, cita del día); Dashboard
con datos sembrados (rating dominada, avatar con capas correctas según
requisitos, estante con ganadas + siluetas, mejor racha); fresh start y
pausa del timer verificados por captura; precache PWA: 27/27 recursos en 200;
checklist §0.1 releída (sin leaderboards, sin aleatoriedad, sin culpa, fallo
nunca castiga, revelado solo en cierres, IA opcional intacta).

**Pendiente (en orden recomendado):**
- **Fase C** (§3.3-§3.5): hosting **DECIDIDO** por el usuario (2026-06-11):
  **Supabase + cron keep-alive**. Aún sin código — playbook completo en §5.2.
- **Fase D** (§2.4): el claustro (amistades por código, perfil-vitrina,
  reconocimiento ❧, "Pensar juntos") — depende de la Fase C.
- **Chat socrático** (§4.4): panel lateral durante el forcejeo con la key
  del usuario; el resto de §4 (texto honesto de "pegar API key", key solo
  en dispositivo, cero degradación sin IA) ya está reflejado en la UI.
  No depende del backend: puede hacerse antes o después de la Fase C.
- **Ingestión de contenido Fase 4+** del Modo Estudio (HANDOFF §3.11.6,
  protocolo ahí): independiente de todo lo anterior, solo datos.
- Al cambiar cualquier archivo del shell, subir `VERSION` en `sw.js`.

---

## §5.2 PLAYBOOK FASE C — SUPABASE + CRON KEEP-ALIVE

Decisión del usuario (2026-06-11). Guía autocontenida para el agente que
ejecute la fase. Mantener las convenciones: fetch directo SIN SDK de Supabase
(cero dependencias), `storage.js` única puerta a LocalStorage, español en
todo, la app 100% funcional sin cuenta y sin red.

### C.0 Pre-requisitos (acciones del USUARIO; pedírselas antes de codificar)

1. Crear proyecto en supabase.com (plan gratuito, región cercana). Anotar
   **Project URL** y **anon public key** (Settings → API). La `service_role`
   key NUNCA va al cliente ni a ningún archivo del repo.
2. En Authentication → Providers → Email: decidir si exigir confirmación de
   correo (para arrancar simple: desactivarla; reevaluar al abrir a amigos).
3. Para el cron con GitHub Actions hace falta repo en GitHub (el proyecto aún
   NO es repo git): `git init` + push (visibilidad a elección del usuario) y
   cargar los secrets `SUPABASE_URL` y `SUPABASE_ANON_KEY`. Alternativa sin
   GitHub: un cron HTTP gratuito (p. ej. cron-job.org) apuntando al endpoint
   de C.2 con el header `apikey`.

### C.1 Esquema SQL (ejecutar en el SQL Editor de Supabase)

```sql
-- Event log append-only (§3.4): los historiales se UNEN, nunca colisionan
create table public.events (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users (id) on delete cascade,
  device_id text not null,
  ts timestamptz not null default now(),
  tipo text not null,        -- 'sesion' | 'piso' | 'unidad' | 'examen' | 'insignia' | 'perfil' | 'migracion'
  payload jsonb not null
);
create index events_user_ts on public.events (user_id, ts);

-- Snapshot del estado derivado (arranque rápido en dispositivo nuevo)
create table public.snapshots (
  user_id uuid primary key references auth.users (id) on delete cascade,
  actualizado timestamptz not null default now(),
  estado jsonb not null
);

-- Keep-alive: una fila que el cron toca con un select trivial
create table public.keepalive ( id int primary key, nota text );
insert into public.keepalive (id, nota) values (1, 'cron keep-alive');

alter table public.events enable row level security;
alter table public.snapshots enable row level security;
alter table public.keepalive enable row level security;

create policy "events: leer propios" on public.events
  for select using (auth.uid() = user_id);
create policy "events: insertar propios" on public.events
  for insert with check (auth.uid() = user_id);
-- append-only deliberado: SIN políticas de update/delete para el cliente

create policy "snapshot: leer propio" on public.snapshots
  for select using (auth.uid() = user_id);
create policy "snapshot: crear propio" on public.snapshots
  for insert with check (auth.uid() = user_id);
create policy "snapshot: actualizar propio" on public.snapshots
  for update using (auth.uid() = user_id);

create policy "keepalive: lectura anonima" on public.keepalive
  for select using (true);

-- Borrar cuenta en 2 clics (§0.1): el cliente no puede tocar auth.users,
-- así que se expone una RPC security definer que borra al propio usuario
-- (events y snapshots caen en cascada).
create or replace function public.borrar_mi_cuenta()
returns void language plpgsql security definer set search_path = public as $$
begin
  delete from auth.users where id = auth.uid();
end $$;
revoke all on function public.borrar_mi_cuenta() from public;
grant execute on function public.borrar_mi_cuenta() to authenticated;
```

### C.2 Cron keep-alive (GitHub Action, cada 2 días)

`.github/workflows/keepalive.yml`:

```yaml
name: Supabase keep-alive
on:
  schedule:
    - cron: '17 6 */2 * *'   # cada 2 días, 06:17 UTC
  workflow_dispatch:
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: select trivial a keepalive
        run: |
          curl -sf "${{ secrets.SUPABASE_URL }}/rest/v1/keepalive?select=id&limit=1" \
            -H "apikey: ${{ secrets.SUPABASE_ANON_KEY }}" \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_ANON_KEY }}"
```

⚠️ GitHub desactiva los schedules de repos sin actividad tras ~60 días: un
commit ocasional los reactiva; documentar al usuario el respaldo cron-job.org
(mismo URL + header `apikey`). Con uso real de la app, la pausa no ocurre.

### C.3 Cliente `js/api.js` (fetch directo, sin SDK)

Interfaz estable de ~10 operaciones — cambiar de backend = reemplazar SOLO
este archivo (regla §3.3). Endpoints REST de Supabase (GoTrue + PostgREST):

```text
configurar()/configurado()      constantes URL + ANON_KEY al inicio del archivo
                                (la anon key es pública por diseño; la
                                seguridad la dan las políticas RLS)
registrar(email, pass)          POST {url}/auth/v1/signup
iniciarSesion(email, pass)      POST {url}/auth/v1/token?grant_type=password
renovarSesion()                 POST {url}/auth/v1/token?grant_type=refresh_token
cerrarSesion()                  POST {url}/auth/v1/logout + limpiar tokens locales
sesionActual()                  {userId, email} | null (con auto-refresh si expiró)
subirEventos(eventos[])         POST {url}/rest/v1/events            (en lote)
descargarEventos(desdeTs)       GET  {url}/rest/v1/events?ts=gt.{ts}&order=ts
subirSnapshot(estado)           POST {url}/rest/v1/snapshots
                                Prefer: resolution=merge-duplicates  (upsert)
descargarSnapshot()             GET  {url}/rest/v1/snapshots?select=*
borrarCuenta()                  POST {url}/rest/v1/rpc/borrar_mi_cuenta
```

Headers comunes: `apikey: ANON_KEY` y `Authorization: Bearer {access_token}`.
Tokens en `cps_sesionSupabase` ({access_token, refresh_token, expira}) vía
storage.js. `device_id`: uuid generado una vez, en `cps_deviceId`.

### C.4 Sincronización `js/sync.js` + outbox (§3.4)

- **LocalStorage sigue siendo la verdad inmediata**; la app JAMÁS bloquea
  por red ni por falta de cuenta.
- `storage.js`: helper `encolarEvento(tipo, payload)` → push a `cps_outbox`.
  Llamarlo en los puntos de cierre ya existentes: sesión completada
  (app.js → completarSesion), piso mínimo, unidad de estudio, examen,
  insignia nueva, cambios de perfil/preferencias relevantes.
- **EXCLUIDOS de outbox y snapshot**: `cps_mentorIA` (API keys de Claude,
  regla §4.2) y `cps_asignacion` en curso (estado efímero del día).
- `sync.js`: drena el outbox en lotes cuando hay sesión y conexión — al
  arrancar, en `window 'online'` y tras cada encolado; luego sube snapshot.
  Silencioso: los fallos dejan la cola intacta y se reintenta después.
- `derivarPerfil(eventos)`: función PURA compartida que recomputa los
  derivados (historial, racha, mejorRacha, insignias, estudio) desde el log.
  Conflictos: el log se une (append-only no colisiona); los contadores se
  recomputan; nada de CRDTs (caso real: 1 persona, 2-3 dispositivos).
- Primer login en dispositivo nuevo: descargar snapshot + eventos → poblar
  LocalStorage → la app funciona exactamente igual que hoy.

### C.5 UI (tarjetas nuevas en el Dashboard)

- **"Mi cuenta CogitoErgoSum"**: registro / login / logout; estado de sync
  ("N eventos pendientes · última sincronización HH:MM"); botón **"Importar
  mi progreso local a mi cuenta"** (migración: convierte el LocalStorage
  actual en eventos retroactivos tipo 'migracion' + snapshot; verificar tras
  migrar que racha y mejorRachaHistorica quedaron intactas — NO perder ni un
  día). Todo opt-in: sin cuenta, la app sigue 100% funcional local.
- **"Exportar mis datos"** (descarga JSON de todos los cps_*, 2 clics) y
  **"Borrar cuenta"** (2 clics, sin súplicas — §0.1). Exportar funciona
  incluso sin cuenta (es local).
- Notificación diaria opcional (Web Push, 1/día máx, hora elegida): dejarla
  para el final de la fase o posponerla — requiere HTTPS y un emisor push;
  NO es bloqueante para nada más.

### C.6 Verificación de la fase (antes de darla por cerrada)

1. Offline completo (red desconectada): la app funciona y el outbox acumula;
   al volver la red, drena solo.
2. Dos navegadores como dos dispositivos: cerrar una sesión de entrenamiento
   en uno, login en el otro → progreso unificado y rachas correctas.
3. Migración del progreso real de Edgar sin pérdida (comparar perfil antes
   y después).
4. `node --check` en todo, JSON validados, cruce de IDs HTML↔JS, y subir
   `VERSION` en sw.js (api.js y sync.js entran a la lista SHELL del precache).
5. Releer el checklist anti-§0.1 (borrar cuenta sin fricción, nada de culpa).

Fase D (claustro) se construye DESPUÉS, sobre estas mismas tablas + nuevas
`friendships`/`reconocimientos` con sus políticas RLS (diseño en §2.4).

---

## §6. LO QUE EXPLÍCITAMENTE QUEDA FUERA (decisiones, no olvidos)

- Leaderboards, ligas, rankings, puntos comparables entre usuarios.
- Feed de actividad de contactos y presencia en tiempo real.
- Compras, monedas, gemas, anuncios, niveles "premium".
- Cosméticos aleatorios o de evento limitado.
- Login "Sign in with Claude" vía suscripción (prohibido por política de
  Anthropic para terceros; usar API key por usuario, §4).
- Notificaciones de comparación, culpa o urgencia.
- Apps nativas de tienda (la PWA cubre los tres dispositivos sin costo ni
  proceso de revisión; reevaluar solo si la PWA muestra límites reales).
