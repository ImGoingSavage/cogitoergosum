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
  > **✅ APROBADO por el usuario (2026-06-11) con regla de sorteo**: el
  > problema se SORTEA del pool común — problemas curados (jamás variantes
  > generadas, que son personales) que NINGUNO de los dos haya trabajado.
  > El sorteo ocurre en el cliente de quien ACEPTA: el proponente publica
  > sus candidatos (ids curados no trabajados, barajados), el aceptante
  > intersecta con los suyos y sortea; si la intersección queda vacía,
  > sortea de los candidatos del proponente. Cada quien lo resuelve con el
  > bucle COMPLETO del camino 1 (timer, desconstrucción, ficha — sin
  > atajos); las entregas del otro solo se pueden leer cuando TÚ ya
  > entregaste (struggle first, garantizado por RLS). Se comparte:
  > desconstrucción, moraleja y disparador. Sin score, sin ganador.
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
- **Fase C** (§3.3-§3.5): **CÓDIGO TERMINADO (2026-06-11, tarde)** — ver
  estado exacto al final de §5.2. Proyecto Supabase creado
  (rcaljqmibtkorcmdyqvg, GoTrue verificado, signup con sesión directa),
  repo GitHub privado `ImGoingSavage/cogitoergosum` creado con secrets
  cargados. Solo falta: (1) ejecutar `supabase/schema.sql` en el SQL
  Editor (acción del usuario), (2) push del workflow (el token de gh
  necesita scope `workflow`: `gh auth refresh -h github.com -s workflow`),
  (3) verificación E2E del checklist C.6 y borrar el usuario de prueba
  `prueba-borrar-luego@cogitoergosum.test`.
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

### C.7 Estado de ejecución — **FASE C CERRADA (2026-06-11)**

| Pieza | Estado |
|---|---|
| Proyecto Supabase (rcaljqmibtkorcmdyqvg) | ✅ Creado; GoTrue v2 responde; signup con sesión directa (Confirm email desactivado) |
| `supabase/schema.sql` | ✅ Ejecutado por el usuario en el SQL Editor (verificado: keepalive responde `[{"id":1}]`) |
| `js/api.js` (C.3) | ✅ Implementado con URL/anon key del proyecto como constantes |
| `js/sync.js` (C.4) | ✅ Outbox + snapshot + adoptarOUnir + recomputo de rachas + migración |
| `storage.js` | ✅ outbox/deviceId/sesionSupabase/ultimaSync + CLAVES_SYNC + encolarEvento (evento DOM `cps:evento-encolado`, sin ciclos) |
| Eventos en cierres | ✅ sesion (con uid), piso, unidad, examen, insignia |
| UI "Mi cuenta" (C.5) | ✅ Tarjeta en Dashboard: login/registro, sincronizar, importar progreso, exportar JSON, borrar cuenta (2 clics); verificada en headless |
| `sw.js` | ✅ v2 con api.js y sync.js en el precache |
| Repo GitHub | ✅ Privado `ImGoingSavage/cogitoergosum`, main pusheado (gh como credential helper vía `gh auth setup-git`; el scope `workflow` se añadió con `gh auth refresh`); secrets cargados |
| Workflow keep-alive (C.2) | ✅ En el repo; corrida manual `workflow_dispatch` → **success** (run 27352416985); cron activo cada 2 días |
| Verificación E2E por REST | ✅ 8/8: login → insert evento (201) → leer eventos propios → upsert snapshot (201) → leer snapshot → **RLS: anónimo ve 0 filas** → RPC borrar_mi_cuenta (204) → usuario de prueba eliminado |
| Pendiente de la C.6 con USUARIO real | ❌ Prueba humana de 2 dispositivos: Edgar crea su cuenta en la app, "Importar mi progreso local", abrir en segundo navegador/celular y verificar adopción + rachas. (La maquinaria está probada por REST; falta el recorrido de UI real.) |
| Web Push diaria opcional (C.5) | ❌ Pospuesta a propósito (no bloqueante; requiere emisor push) |

**Siguiente trabajo disponible**: chat socrático (§4.4) · ingestión Fase 4+
del Modo Estudio (HANDOFF §3.11.6) · publicar el frontend (GitHub Pages/
Cloudflare Pages apuntando al mismo Supabase) cuando Edgar quiera usarlo
desde el celular sin servidor local.

---

## §5.3 FASE D — EL CLAUSTRO: ESTADO (2026-06-11, tarde)

**Código completo y verificado en local; falta aplicar el SQL y la prueba
social E2E.** Implementa §2.4 puntos 13-14 del plan; el punto 15 ("Pensar
juntos") queda SIN construir hasta validarlo con el usuario.

| Pieza | Estado |
|---|---|
| `supabase/schema-fase-d.sql` | ✅ Escrito y versionado: perfiles (vitrina jsonb), amistades, invitaciones, reconocimientos; RLS "leer perfil solo dueño o amigo" vía `son_amigos()` (security definer); vínculo SOLO nace por RPC `canjear_invitacion` (sin insert directo); reconocimiento UNIQUE (de,para,sello) — jamás contador. ❌ PENDIENTE de ejecutar en el SQL Editor |
| `js/api.js` | ✅ 11 operaciones sociales nuevas (perfil, invitaciones, amistades, reconocimientos) |
| `js/claustro.js` | ✅ Vitrina propia (`construirVitrina()`: SOLO avatar/sellos/rachas/moraleja opt-in — sin puntajes ni actividad), republicación tras cada sync (`cps:sync-completada`), amigos, canje, vitrina ajena con ❧ único, notificaciones in-app de reconocimientos (se marcan vistas al verlas), deshacer vínculo en 2 clics |
| UI | ✅ 4.ª pestaña "Claustro" (estados: sin cuenta / sin nombre / activo), tarjeta "Mi moraleja de la semana" (compartir/dejar de compartir una ficha del cuaderno) |
| `avatar.js` | ✅ Refactor: `capasGanadas()` (lo que viaja a la vitrina) + `renderDesdeCapas()` (pintar el pensador de un amigo) |
| `storage.js` | ✅ `cps_claustro` {username, fichaCompartidaUid} añadido a CLAVES_SYNC |
| `sw.js` | ✅ v4 con claustro.js |
| Verificación local | ✅ node --check (14 módulos), IDs HTML↔JS sin huecos, vista Claustro sin sesión verificada en headless |
| Prueba social E2E | ✅ 10/10 (2026-06-11, tarde): RLS pre-vínculo, invitación+canje, código quemado, vitrina mutua, ❧ 201 + duplicado 409, marcar visto, extraños ven 0 perfiles, vínculo deshecho, ambas cuentas de prueba borradas |
| "Pensar juntos" (§2.4, punto 15) | ✅ CONSTRUIDO (2026-06-11, tarde): `supabase/schema-pensar-juntos.sql` (pensar_juntos + pj_entregas con RLS "struggle first": la entrega del otro solo es legible cuando la tuya existe), 7 operaciones en api.js, UI completa en claustro.js (proponer desde vitrina, aceptar con sorteo del pool común en el cliente del aceptante, lista de sesiones conjuntas, lado a lado), integración camino 1 en app.js (`abrirProblemaCompartido` — jamás pisa un forcejeo vivo; entrega al cerrar con reintento offline). sw.js v5. SQL aplicado por el usuario y **E2E 9/9** (2026-06-11, tarde): propuesta 201 → aceptar/fijar problema 204 → **struggle first probado** (sin entrega propia se ven 0 entregas aunque exista la del otro) → ambas entregas legibles lado a lado → duplicado 409 → retirada y cuentas de prueba borradas. **FASE D COMPLETA, incluido el punto 15.** |

---

## §5.4 MAPA PARA EL SIGUIENTE AGENTE (actualizado 2026-06-12)

Todo lo que hace falta saber para continuar el proyecto desde este punto,
sin releer la conversación. Léelo junto con: `claude.md` (pedagogía),
`HANDOFF.md` (camino 1 y 2, protocolo de ingestión) y este archivo
(§0 Constitución — ES LEY —, §5.1-§5.3 bitácoras).

### Infraestructura viva (no es plan: ya existe)

- **Supabase**: proyecto `rcaljqmibtkorcmdyqvg` (cuenta del usuario).
  - URL y anon key viven como CONSTANTES en `js/api.js` (la anon es pública
    por diseño; la seguridad la dan las políticas RLS). La `service_role`
    no existe en ningún archivo y así debe seguir.
  - SQL aplicado por el usuario en el SQL Editor: `supabase/schema.sql`
    (Fase C) y `supabase/schema-fase-d.sql` (claustro). Cualquier DDL nuevo
    = archivo nuevo en `supabase/` + pedirle al usuario que lo pegue
    (la anon key no puede correr DDL, por diseño).
  - "Confirm email" está DESACTIVADO (signup devuelve sesión directa).
- **GitHub**: repo privado `ImGoingSavage/cogitoergosum`. `gh` autenticado
  (token con scope `workflow`) y configurado como credential helper de git
  (`gh auth setup-git`). Secrets del repo: `SUPABASE_URL`,
  `SUPABASE_ANON_KEY`. Workflow `keepalive.yml` en verde, cron cada 2 días
  (si el repo pasa ~60 días sin commits, GitHub pausa el schedule: un
  commit lo reactiva).
- **`.gitignore`**: `Biblioteca/` y `Definitivo.pdf` NUNCA se suben
  (material personal/copyright); la app no los necesita.

### Cómo verificar cualquier cambio (ritual mínimo)

```sh
cd /Users/EdgarDevice/Desktop/ProyectoX
for f in js/*.js sw.js; do node --check "$f"; done
python3 -c "import json,glob; [json.load(open(p)) for p in glob.glob('data/*.json')]"
python3 -m http.server 8000   # y probar en navegador (módulos ES6 exigen HTTP)
# Si cambiaste CUALQUIER archivo del shell: subir VERSION en sw.js
# (la app del usuario se recarga sola una vez al detectar la versión nueva).
# Cruce de IDs HTML↔JS: grep de $('...') vs id="..." en ambas direcciones.
# Probar con red desconectada y prefers-reduced-motion. Releer §0.1.
```

### QUÉ FALTA, en orden de valor

> ## 📍 PUNTO ACTUAL (2026-06-13) — léelo primero
>
> **Frontend (camino 1 + 2 + claustro + Fases A-D):** COMPLETO, verificado y
> en producción (https://imgoingsavage.github.io/cogitoergosum/). Oleadas de
> auditoría 1-6 + extracción de módulos: HECHAS (bitácoras 6, 7, 8).
>
> **Frontera actual = MENTOR LOCAL HÍBRIDO** (bitácora 9). Todo el código
> está escrito y subido (commit `225c624`): backend en `mentor-backend/`
> (FastAPI+Qdrant+Ollama) y cliente frontend `js/mentorLocal.js` + UI. PERO
> **el backend NUNCA se ha ejecutado** — vive solo como código. El frontend
> ya trae la tarjeta "Mentor local (opcional)" pero está inerte hasta que
> apunte a un backend vivo.
>
> **La acción pendiente es de DESPLIEGUE, no de código, y es HUMANA** (en la
> laptop Linux i5 de Edgar; el agente no tiene acceso a esa máquina). El
> runbook paso a paso es **`mentor-backend/PUESTA-EN-MARCHA.md`** — 5 etapas:
> 0) prerequisitos (Docker/Python/Ollama + pull de modelos + copiar Biblioteca),
> 1) Qdrant + `python ingest.py`, 2) uvicorn + probar `/health` local,
> 3) Cloudflare Tunnel, 4) conectar la app (URL + service token en el
> Dashboard), 5) medir latencia del 1.5B y decidir `EVALUACION_FALLBACK`.
>
> **Lo que el agente SÍ puede hacer si se le pide** (sin la laptop): un
> `run.sh` de arranque, ajustar prompts/`num_predict`/política anti-fuga,
> exponer `/metrics` en la app, o corregir bugs que aparezcan al probar.
>
> **Menores aún abiertos, independientes del mentor local:** comprimir
> `login.mp4` 4.8 MB→~2 MB (ffmpeg, cosmético, punto 9 de abajo); lista de
> "menores acumulados" (punto 8).

0. ~~Fondo de video + liquid glass~~ ✅ HECHO (2026-06-11, noche). Detalle:
   - El video llegó como `fondo .mp4` en la raíz → movido a
     `assets/video/fondo.mp4`. Ya venía óptimo (H.264, 720×1280 vertical,
     19.8 s, sin audio, 1.5 MB ≈ 638 kbps): NO se recomprimió.
   - **Decisión de diseño documentada**: el video original es CLARO
     (astrolabio sobre blanco), incompatible tal cual con la paleta §1 y el
     contraste AA. Se invierte por filtro CSS a nocturno (tinta luminosa
     sobre piedra, entonada a cálido): token `--fondo-filtro` en
     `styles.css`. Para usarlo sin invertir: `--fondo-filtro: none` y subir
     `--fondo-velo` a ~0.82 (está comentado en el propio CSS). Validar con
     el usuario cuál de las dos lecturas prefiere.
   - Implementación: capa `.fondo-app` fixed con `<video muted loop
     playsinline preload="none" poster=assets/video/fondo-poster.jpg>`
     (póster JPEG 67 KB generado del primer fotograma, precacheado);
     `object-fit: cover` encuadra bien el video vertical en móvil y
     escritorio. SIN atributo autoplay: `configurarFondoVideo()` (app.js)
     reproduce a 0.5× solo si `prefers-reduced-motion` lo permite, pausa
     con pestaña oculta. Con motion reducido el video NI SE DESCARGA
     (verificado por log del servidor: solo pide el póster).
   - Liquid glass: `.tarjeta` y header con `backdrop-filter: blur+saturate`
     (+ prefijo -webkit-), tokens `--vidrio`/`--vidrio-borde`, velo
     `--fondo-velo` para AA; fallback `@supports` a superficies opacas;
     blur reducido (10px) en móvil por GPU; las superficies interiores
     (--bg-sutil) siguen opacas — solo 2 niveles con backdrop-filter.
   - `sw.js` v7: póster en el precache; el video NO (cache-first bajo
     demanda en `cogitoergosum-media-v1`, que sobrevive cambios de VERSION,
     con manejo de Range: se guarda la copia completa y se recorta al
     responder 206, porque cache.put rechaza parciales).
   - Verificado: node --check (15 módulos+sw), JSON, capturas headless
     escritorio/móvil/reduced-motion (contraste y vidrio correctos).
   - PENDIENTE humano: sensación de fluidez/batería en el celular real
     (si el FPS sufre, bajar blur o quitar `saturate`) y validar la
     decisión de inversión del video.

1. ~~Prueba social E2E de la Fase D~~ ✅ HECHA (10/10, ver tabla §5.3).
2. ~~"Pensar juntos"~~ ✅ HECHO Y VERIFICADO (E2E 9/9 con struggle first
   probado por RLS; SQL aplicado; ver tabla §5.3). Las 4 fases del plan
   §5 están COMPLETAS.
3. ~~Chat socrático (§4.4)~~ ✅ HECHO Y AMPLIADO (2026-06-11, noche; pedido
   del usuario): **mentor flotante en TODAS las vistas + visión (fotos)**.
   Sustituye a la tarjeta de chat embebida de la vista Sesión (eliminada
   de index.html). Detalle:
   - **Mentor flotante** (`#mentor-flotante`, burbuja 🪶 + panel de vidrio):
     existe SOLO con cuenta de Claude activa; cambia de modo según el
     contexto (`aiMentor.js → chatMentor(modo, contexto, mensajes)`):
     `forcejeo` (socrático puro, jamás revela/confirma — gating intacto),
     `revision` (tras revelar: puede comparar con la solución oficial),
     `estudio` (explica lo leído con ejemplos nuevos; en quiz/examen solo
     guía) y `general` (coach sobre `Analytics.resumen()`, siempre contra
     el propio pasado, §0.3). Chat de forcejeo/revisión persiste en
     `asignacion.chat` (se archiva con la sesión); estudio/general son
     efímeros en memoria (sin historial infinito). Se puede adjuntar 📷
     foto a cualquier mensaje (las fotos JAMÁS se persisten: viajan solo
     en la llamada; el historial guarda un marcador de texto).
   - **Foto de la desconstrucción en papel** (tarjeta Mi Desconstrucción,
     solo durante forcejeo): `analizarFotoDesconstruccion()` transcribe
     fielmente la hoja (incluidas expresiones matemáticas, vía structured
     outputs/json_schema) y devuelve una observación socrática SOLO sobre
     redacción/completitud — el prompt prohíbe juzgar corrección o
     insinuar la solución. Botón "Añadir a mi desconstrucción" inyecta la
     transcripción al textarea y dispara el autosave normal (cuenta para
     el mínimo de 200 caracteres y viaja con la sesión = "cargar a la BD").
   - **Revisión del intento** (sección Reflexión, SOLO tras revelar — guard
     en JS): `revisarIntento()` compara desconstrucción + texto de
     comparación + foto opcional contra la solución oficial y señala el
     punto EXACTO de divergencia (lenguaje §2.2: valida proceso, jamás
     veredicto seco). El resultado se guarda en `asignacion.revisionIA`
     (se archiva con la sesión).
   - `prepararImagen()` comprime en el cliente (canvas, lado ≤1568 px,
     JPEG) antes de enviar. Modelo sigue siendo `claude-opus-4-8`.
   - **Login con Claude vía Gmail: NO existe para terceros** (re-verificado
     contra la referencia oficial de la API, 2026-06-11). La tarjeta
     "Potenciar con Claude" ahora trae la guía honesta de 3 pasos con
     enlace a platform.claude.com → API Keys (ahí sí se entra con Gmail).
   - Verificado: node --check (15 módulos+sw), JSON, cruce de IDs, headless
     con cuenta sembrada (burbuja+panel en forcejeo, botón de foto en
     Desconstrucción), sw.js **v8**. PENDIENTE humano: una pasada real con
     key (chat con foto, transcripción de hoja y revisión post-revelado).
4. ~~Ingestión Fase 4 del Modo Estudio~~ ✅ HECHA (2026-06-11, tarde):
   bloque `fase-4` "Álgebra de competencia y probabilidad" en
   `data/study.json` — 5 unidades (Zeitz §5.2 factor tactic, §5.3
   telescopio, §5.4 polinomios/Vieta, §5.5 desigualdades + Engel cap. 7),
   25 preguntas de retrieval, examen de 7 ítems TODOS de probabilidad AMC
   (respuestas verificadas por fuerza bruta/derivación en Python; fuentes
   y anclas actualizadas en HANDOFF §3.11.6). Cero código; sw.js v10.
4bis. ~~Ingestión Fase 5~~ ✅ HECHA (2026-06-11, noche; "métele todo"
   pedido por el usuario): bloque `fase-5` "El cruce" — 9 unidades (Zeitz
   §4.2 complejos, §8.2-§8.4 geometría completa, cap. 9 convergencia +
   euleriana; Engel caps. 1 invariancia, 2 coloraciones, 3 extremal,
   13 juegos), 45 preguntas, examen de 8 ítems nivel AMC 12 (6 AMC 12
   2017-2019 + Bachet + tetrominós de Engel; todas las respuestas
   verificadas por cómputo). Pool de examen acumulado: 40. sw.js v11.
   **Fase 6**: solo queda Zeitz §8.5 (transformaciones); lo natural es
   AIME y/o Engel caps. 8-12/14 — decidir con el usuario.
4ter. ~~Fase 7 — Arena de Entrevistas de Élite~~ ✅ HECHA Y AUDITADA
   (2026-06-12, commits ea21c60 + 7700fc3): bloque `fase-7`, 7 unidades
   (2 Quant, 2 MAANG, 1 ML Systems, 2 Health AI/RWE), 7 ítems de examen con `pistas[]`
   de 5 niveles graduados (retrocompatible con `pista` string de fases
   anteriores), 7 lecciones markdown, ruta-chips en la UI, sw.js v17.
   La auditoría de Oleada 1 (14 criterios) encontró y corrigió 6
   problemas — ninguno estructural; veredicto: publicado. Su lista de
   "Oleada 2" quedó en el punto 8 de pendientes. Nota: la Fase 7 se
   construyó ANTES que la Fase 6 (decisión del usuario); la Fase 6 ya
   está EN CURSO (punto 7) e insertada en `bloques[]` antes de `fase-7`,
   así que el orden de desbloqueo quedará correcto. Ver bitácora al final.
   (arena-s1 + f7-ex-7 añadidos 2026-06-12, bitácora (4)).
5. ~~Publicar el frontend~~ ✅ HECHO (2026-06-11, noche; decisión del
   usuario: GitHub Pages): el repo `ImGoingSavage/cogitoergosum` se hizo
   **PÚBLICO** (auditado antes: cero secretos — la anon key es pública por
   diseño, `Biblioteca/` y `Definitivo.pdf` siguen fuera por .gitignore;
   se retiró `test-dash.html`) y Pages sirve `main`/raíz con `.nojekyll`.
   **URL: https://imgoingsavage.github.io/cogitoergosum/** (HTTPS
   forzado → la PWA instala). Verificado en vivo: 10 recursos críticos en
   200 (shell, JSONs, video y póster del login, fuentes) y captura del
   sitio con la portada funcionando. Todo es rutas RELATIVAS y el manifest
   ya tenía `start_url:"./"`, así que el subpath `/cogitoergosum/` no
   rompió nada; el handler de video del SW usa `includes('/assets/video/')`
   (compatible con subpath). Cada `git push` a main redespliega solo; el
   usuario recibe la versión nueva en la recarga siguiente
   (`controllerchange`). Nota: el deploy es el build "legacy" de Pages
   (branch main, raíz) — no hay workflow de deploy que mantener.
6. **Pruebas humanas** (solo Edgar puede hacerlas; nada de esto bloquea
   al agente):
   - Instalar la PWA desde https://imgoingsavage.github.io/cogitoergosum/
     en el celular ("Añadir a pantalla de inicio") y sentir fluidez y
     batería con los dos videos (portada a 0.5× y fondo a 0.5×). Si el
     FPS sufre: bajar el blur del vidrio o quitar `saturate` (tokens en
     styles.css). Validar también la decisión de INVERSIÓN del video de
     fondo (alternativa documentada en el propio CSS).
   - **Fase C de punta a punta** (único pendiente real de C.6): crear su
     cuenta real en la app → "Importar mi progreso local" → abrir en un
     segundo navegador/dispositivo → verificar adopción del progreso y
     rachas intactas. La maquinaria está probada por REST (8/8); falta el
     recorrido de UI con humano.
   - Una pasada real del mentor con API key: mensaje al chat socrático,
     foto de una hoja (transcripción) y revisión post-revelado.
   - **Pizarra con Apple Pencil real en el iPad** (presión, rechazo de
     palma, lazo, resaltador) y lectura de 2-3 lecciones integradas en la
     tablet (bitácora "noche, 3").
   - **Fase 7 en dispositivo real**: ya NO requiere aprobar nada — usa el
     selector de bloques (2026-06-12) para navegar directo a la Arena.
     Verificar: ruta-chips visibles en la lista de unidades, lectura de
     las 7 lecciones arena-*, panel de pistas graduadas en el examen
     (pedir 2-3, recargar la página y confirmar que se reponen), y que
     las fases 1-5 siguen mostrando su pista única.
6bis. **Decidir el alcance del texto en las lecciones** (bitácora
   "noche, 3"): lecciones redactadas (estado actual) vs. texto íntegro del
   libro vía canal privado en Supabase — el texto íntegro NO puede ir al
   repo público (copyright). Decisión del usuario.
7. ~~Fase 6 del Modo Estudio~~ ✅ **HECHA (2026-06-12, commit pendiente).**
   Bloque **"Fase 6 · Transformaciones, Engel avanzado y AIME"**, 10 unidades
   en orden de dificultad creciente, pusheado a main. Detalle:
   - ✅ 3 heurísticas nuevas en `catalogoHeuristicas` (total 21):
     `transformacion`, `recurrencia`, `ecuacion-funcional`.
   - ✅ Bloque `fase-6` en `bloques[]` ANTES de `fase-7` con examen de 7
     ítems (`f6-ex-1..7`; pista string, estilo competencia).
   - ✅ 10 unidades en `unidades[]` con banco[4], ideas_clave[5],
     heurísticas en catálogo, IDs sin duplicados:
     `zeitz-85a`, `zeitz-85b` (Zeitz §8.5), `engel-ind`, `engel-suc`,
     `engel-pol`, `engel-fun`, `engel-geo2` (Engel avanzado),
     `aime-alg`, `aime-geo`, `aime-cnt` (nivel AIME).
   - ✅ 10 lecciones `data/teoria/{id}.md` (formato estándar: secciones
     temáticas + Disparadores + Síntesis en blockquote + pie de retrieval).
   - ✅ `sw.js` → **v19**: 10 rutas nuevas en SHELL (total 88 archivos,
     54 lecciones; cruce filesystem 88/88 sin faltantes).
   - ✅ Validación: `node --check` (18 módulos + sw), JSON válido,
     heurísticas en catálogo, sin IDs duplicados.
   **Estado del pool de examen acumulado: 47 ítems (40 fases 0-5 + 7
   fase-6 + 7 fase-7 Arena = 54; nota: conteo exacto en study.json).**
8. **Menores acumulados** (en orden de valor):
   - Web Push diaria opcional (1/día máx, hora elegida, contenido neutro
     — §0.1): requiere un emisor push; con el sitio ya en HTTPS público
     dejó de estar bloqueada por infraestructura.
   - Refinamientos del Modo Estudio (lista al final de HANDOFF §3.11.6):
     ~~timer visible en el examen~~ ✅ (mm:ss en la cabecera, sobrevive
     recargas, limpia su intervalo al salir del panel — commit 3f8e3e6);
     ~~persistir el textarea de forcejeo del examen~~ ✅ (autosave en
     `textareasPorItem[item.id]`, restaurado en cada render — mismo
     commit); ~~preguntas falladas ("no lo tenía") hacia repetición
     espaciada~~ ✅ (commit 09061e1: las preguntas marcadas "mal"/"parcial"
     en un quiz se guardan en `pendientesRepaso[unidadId]`; botón "Repasar
     N pregunta(s) pendiente(s)" en el cierre de unidad re-corre el quiz
     solo con esas IDs vía `iniciarRepaso(u)`, preservando el registro
     original de la unidad completada); piso mínimo de estudio para la
     racha 📘 (decidir con el usuario); materializar los problemas
     sugeridos en `dosis` como sesiones del camino 1.
   - FSRS simplificado y "reintenta tus fallos" (HANDOFF §3.9 y tabla de
     benchmarks: Anki/Lichess).
   - Exponer `evaluarDesconstruccion()` en la UI durante el forcejeo
     (cuidando el gating: feedback de redacción, jamás de corrección).
   - **Oleada 2 de Fase 7** (hallazgos no urgentes de la auditoría):
     - ~~Filtrar opciones de predicción al bloque en curso~~ ✅ (union
       de heurísticas de unidades + ítems del bloque: de 18 a 7-10
       opciones según el bloque; respuesta correcta siempre presente —
       verificado por script; commit 3f8e3e6).
     - ~~Etiqueta "Resuelto con la pista" singular con `pistas[]`~~ ✅
       (ahora "Resuelto con las pistas" si `pistas.length > 1` — mismo
       commit).
     - ~~Unidad ML Systems (skew, drift, rollback)~~ ✅ arena-s1 +
       lección + banco[4] + heurística `skew-drift` + chip
       `ml-systems` + f7-ex-7 (bitácora (4)).
     - ~~Modo entrevistador del Mentor~~ ✅ `SYSTEM_CHAT_ENTREVISTADOR`
       + `contextoEntrevista()` + contexto por ruta (bitácora (4)).
     - ~~Plantilla de diseño y cajas negras en lecciones de sistemas~~ ✅
       plantilla 13 campos en arena-s1/arena-h2; `[CAJA NEGRA OK]` IPW
       en arena-h2 y Eve's law en arena-q1 (bitácora (4)).
     - ~~Confianza 1-5 en la predicción del examen~~ ✅ fieldset +
       frases de calibración (bitácora (4)).
     - ~~Selector de bloques / acceso libre a lecciones~~ ✅ candado
       eliminado + `estudio-bloque-selector` (bitácora (4)).
     - Suavizar "diseñado para eliminar a quienes…" en arena-m1 (tono
       mejorable aunque no juzga al usuario).
     - Colores de los ruta-chips en hex directo en vez de tokens
       (contraste AA verificado; solo disciplina de estilo).
     - Decidir si `pistasUsadas` pesa en algo o se muestra en el
       Dashboard (hoy es solo dato, coherente con "registrar, no
       penalizar").
     - Ampliar la Arena: más unidades por ruta — mismo protocolo: unidad
       + lección + banco + ítem de examen con `pistas[]` y
       `source: "original"`.
9. **Plan de la auditoría de arquitectura 2026-06-12** (hallazgos, plan de
   6 oleadas y tabla de estado en la **bitácora (5)**, al final de este
   archivo). Es ahora el trabajo de MAYOR VALOR del proyecto — por delante
   de cualquier contenido nuevo, porque el multi-dispositivo real depende
   de él:
   - [x] **Oleadas 1-3** ✅ EJECUTADAS (2026-06-12, bitácora (6)).
   - [x] **Oleadas 4-6** ✅ EJECUTADAS (2026-06-12, bitácora (7)).
   - [x] **Extracción de módulos** ✅ EJECUTADA (2026-06-12, bitácora (8)):
     `js/cuentaUI.js` y `js/mentorChat.js` extraídos de app.js.
     app.js: 2017 → 1454 l; sw.js → v25.
   - ~~Reset de usuarios de prueba~~ **CANCELADO** por decisión del usuario.
   - [ ] **Comprimir login.mp4** de 4.8 MB a ~2 MB (ffmpeg; cosmético):
     instalar con `brew install ffmpeg` y ejecutar:
     `ffmpeg -i assets/video/login.mp4 -c:v libx264 -crf 28 -preset slow assets/video/login-small.mp4`
     luego reemplazar el archivo y subir VERSION.

### Bitácora 2026-06-11 (tarde, 2): portada de login + cerrar sesión

Pedido del usuario. Implementado y verificado en headless (escritorio,
móvil, camino "sin cuenta" y sesión sembrada):

- **Portada de inicio de sesión** (`#pantalla-login`, overlay z-40): video
  `assets/video/login.mp4` (llegó como `login.mp4` en la raíz; H.264,
  544×680, 42 s, sin audio, 5 MB — mármol clásico sobre negro, NO se
  invierte: ya es nocturno; viñeteado radial para legibilidad) + tarjeta
  de **vidrio líquido profundo** (blur 30 + saturate 1.7, brillo interior
  `inset 0 1px 0`, radios 28/14, fallback `@supports` opaco). Póster
  `login-poster.jpg` generado con qlmanage (precacheado).
- **Comportamiento**: aparece al abrir SOLO si no hay sesión Supabase y el
  usuario no eligió "Continuar sin cuenta" (clave local `cps_loginOmitido`,
  por dispositivo, EXCLUIDA de CLAVES_SYNC). Entrar/Crear cuenta reutilizan
  `Api` + `despuesDeEntrar()` (adopta/une progreso igual que la tarjeta del
  Dashboard). La cuenta sigue siendo opcional (§0.7): la portada invita,
  jamás bloquea. El video solo se reproduce con la portada visible, pestaña
  activa y sin `prefers-reduced-motion` (oculta: ni se descarga).
- **Botón cerrar sesión** (`#btn-header-salir`, ⏻ en el header): existe
  solo con sesión activa (toggle en `renderizarCuentaUI`); al pulsarlo
  cierra sesión, conserva intactos los datos locales (§3.4) y reabre la
  portada. El logout de la tarjeta "Mi cuenta" del Dashboard sigue igual.
- `sw.js` **v9**: `login-poster.jpg` al precache; el handler de media ahora
  cubre cualquier `assets/video/*.mp4` (cache-first con Range, misma
  `cogitoergosum-media-v1`).

### Bitácora 2026-06-11 (noche, 3) — Estudio autocontenido + pizarra (VIGENTE)

Pedido del usuario: (1) cada sección del Modo Estudio debe traer las páginas
del libro en markdown para estudiar sin cargar el libro; (2) al final de cada
sección, un resumen-chunk mínimo de lo revisado; (3) una pizarra tipo
GoodNotes en Estudio y Entrenamiento (lazo, lápiz, goma, tamaños, etc.).
Un agente anterior empezó este trabajo y fue INTERRUMPIDO sin documentarlo;
este apartado documenta lo suyo y lo que faltó, ya terminado y verificado.

**Lo que dejó el agente interrumpido (sin commit, sin bitácora):**
- `data/teoria/*.md` — 36 lecciones REDACTADAS para la app (una por unidad,
  ~5 KB), `js/markdown.js` (render Markdown→HTML mínimo y seguro: escapa
  todo antes de transformar) y botón "📖 Leer la lección aquí" en la vista
  de unidad (`study.js → alternarLeccion`, caché en memoria + precache SW).
- `js/pizarra.js` (~650 líneas, completa y de buena factura): pluma con
  presión del pencil, goma de trazo, lazo (seleccionar/mover/borrar),
  grosor 1-14, 4 tintas de la biblioteca, deshacer/rehacer (100 niveles),
  varias páginas, rechazo de palma, atajos ⌘Z/⌘⇧Z/Esc, limpiar con doble
  toque. Una pizarra POR CONTEXTO (problema del día / unidad / examen /
  libre), persistida en `cps_pizarras` (storage.js) con poda a 30 tableros
  y manejo de LocalStorage lleno. EXCLUIDA de CLAVES_SYNC a propósito
  (borrador local, pesa). Burbuja ✎ visible solo en Sesión y Estudio
  (`actualizarVisibilidad`), contexto inyectado desde app.js
  (`configurarPizarra`). CSS de overlay/barra/botones en styles.css.
- `sw.js` subido a v13 con markdown.js, pizarra.js y las lecciones en el
  precache… **incluyendo 2 lecciones que NUNCA escribió** (`engel-extremo`,
  `engel-juegos`): como el install usa `cache.addAll`, el 404 de esas dos
  ROMPÍA la instalación del SW v13 completo. Ahí lo interrumpieron.
- También bajó el video de login a 0.3× (antes 0.5×).

**Lo terminado hoy (este agente):**
- ✅ Escritas las 2 lecciones faltantes con el estilo y estructura de las
  demás: `engel-extremo.md` (receta variacional, 3 hechos base, E1, E2,
  Sylvester-Gallai) y `engel-juegos.md` (W/L, hacia atrás, Bachet y sus
  3 variantes modulares, pareo/espejo, doble verificación) — alineadas con
  los bancos de quiz de sus unidades. El precache v13 queda íntegro (38/38).
- ✅ **Síntesis al final de las 38 lecciones** (pedido 2 del usuario):
  sección `## Síntesis` con UN chunk mínimo en blockquote que concatena con
  precisión lo revisado, colocada antes del pie "Antes del quiz" (orden
  pedagógico: chunk → instrucción de retrieval).
- ✅ **Resaltador en la pizarra** (la herramienta GoodNotes que faltaba):
  botón ▰, tinta translúcida (alfa 0.38) de ancho constante (3× el grosor),
  pintada como UN solo path para que las uniones no doblen el alfa; la goma
  y el lazo lo tratan como cualquier trazo (radio de borrado ajustado al
  ancho real). Persistencia: flag `m` en el trazo.
- ✅ Verificación: node --check en 17 módulos + sw; JSON válidos; cruce
  unidades↔lecciones↔precache 38/38/38 sin huecos; cruce IDs HTML↔JS;
  render markdown probado (Síntesis → blockquote, sin HTML inyectable);
  arranque en Chrome headless sin errores de consola. `sw.js` se queda en
  **v13**: la v13 rota nunca llegó a instalarse en ningún navegador (addAll
  fallaba), así que no hace falta otro bump.
- ⚠️ NADA de esto está commiteado aún (tampoco lo del agente interrumpido).

**⚠️ DECISIÓN PENDIENTE DEL USUARIO — "contenido completo, tal cual":**
el pedido original era poner TODO el texto del libro de cada sección, no un
resumen. Lo que existe son lecciones redactadas que cubren el temario
completo de cada unidad (definiciones, teoremas, demostraciones y ejemplos
del syllabus), pero NO son las páginas íntegras de Zeitz/Engel/Pólya. El
agente anterior tomó esa decisión sin documentarla, y hay una razón dura
para no copiar el texto íntegro: **el repo es PÚBLICO y GitHub Pages lo
sirve a internet** — subir capítulos completos de libros con copyright es
distribuirlos públicamente (la misma razón por la que `Biblioteca/` está en
.gitignore). Opciones para decidir CON el usuario antes de mover nada:
  a) Quedarse con las lecciones redactadas (estado actual, publicable).
  b) **Canal privado**: tabla `teoria_privada` en Supabase con RLS
     solo-dueño + script LOCAL que cargue las secciones desde
     `Biblioteca/*.txt`; study.js intentaría primero el .md local/precache
     y, con sesión, el texto íntegro privado. El texto jamás tocaría el
     repo. (Esfuerzo medio; es la única vía que da texto íntegro EN la
     tablet vía el sitio público sin publicar el libro.)
  c) Carpeta local gitignoreada con el texto íntegro: solo serviría
     sirviendo la app desde la Mac, no en la PWA instalada desde Pages.

**PENDIENTE humano (pizarra):** probarla con Apple Pencil real en el iPad —
presión, rechazo de palma, lazo con el dedo, resaltador sobre tinta — y
ajustar `ancho()`/alfa si la sensación no convence.

### Bitácora 2026-06-11 (noche, 4) — credenciales recordadas + visibilidad

Pedido del usuario a otro agente que se quedó SIN TOKENS a medio camino
(las capturas de dónde se quedó estaban en la carpeta local `Estado actual`,
ahora gitignoreada por ser material personal). Lo que pidió: (1) que cada
dispositivo recuerde las credenciales de inicio de sesión para no
reteclearlas; (2) video del login más grande para ver el mármol tras la
tarjeta; (3) iconos del mentor y la pizarra más visibles; (4) explicarle
qué hace la burbuja del mentor.

**Lo que el agente interrumpido dejó hecho (working tree, sin commit):**
- `storage.js`: clave `credenciales` ({email, password} del último login
  exitoso) en DEFAULTS, FUERA de CLAVES_SYNC (solo este dispositivo, igual
  que mentorIA). Guardado en texto plano en LocalStorage: decisión
  consciente del usuario para su propia app (la nota de la portada lo
  declara: "tus credenciales se recuerdan solo en este dispositivo").
- `app.js`: `precargarCredenciales()` en la portada (al abrirla y en el
  arranque sin portada) + precarga en la tarjeta "Mi cuenta" del Dashboard;
  `Storage.save('credenciales', …)` en los 4 puntos de éxito (portada
  entrar/registrar, Dashboard entrar/registrar).
- `index.html`: nota de transparencia en la portada.
- `styles.css`: video del login a cover 2× (1088×1360 máx) — la edición
  que en su sesión aparecía fallida sí quedó aplicada.

**Lo terminado por este agente:**
- ✅ Burbujas del mentor (🪶) y la pizarra (✎) más visibles: 58 px, icono
  índigo (token de lo interactivo §1 — NO lámpara), fondo casi opaco
  rgba(27,24,21,0.88), borde índigo 0.45 y sombra; sobre el video el
  vidrio al 60% se perdía. Verificado por captura sobre el póster.
- ✅ Borrar cuenta ahora limpia `credenciales` (precargar credenciales de
  una cuenta que ya no existe sería confundir). Cerrar sesión NO las
  limpia: ese es exactamente el caso de uso de la precarga.
- ✅ `Estado actual*` en .gitignore (capturas personales, repo público).
- ✅ sw.js **v14** (cambió el shell). Verificación: node --check (17
  módulos+sw), captura del login (mármol grande y visible a través de la
  tarjeta) y de las burbujas.
- ℹ️ Respuesta a la pregunta (4): la burbuja 🪶 inferior derecha es el
  MENTOR SOCRÁTICO (§4.4): solo existe con cuenta de Claude activa y al
  pulsarla abre el panel de chat, cuyo modo depende de la vista (forcejeo:
  socrático puro, jamás revela; tras revelar: compara con la solución;
  estudio: explica lo leído; general: coach sobre tus métricas). La ✎
  inferior izquierda abre la pizarra (goma de trazo, lazo, resaltador,
  doble toque en ⌫ para limpiar la página).

### Bitácora 2026-06-11 (noche, 5) — pizarra GoodNotes + evaluar con el mentor

Pedido del usuario: (1) que la pizarra sea prácticamente idéntica a
GoodNotes (utilidades, posiciones, shortcuts como el doble toque del
pencil) copiando funcionalidad con cuidado de derechos (funcionalidad sí,
trade dress no); (2) botón DENTRO de la pizarra que cargue lo escrito al
mentor socrático para evaluarlo, visible SOLO con API key de Claude bien
configurada.

**Pizarra (js/pizarra.js reescrita; index.html + styles.css):**
- Memoria por herramienta (como GoodNotes): pluma y resaltador recuerdan
  su color y grosor; goma su tamaño. **3 presets de grosor** por
  herramienta (la fila de puntos de GoodNotes) en vez del slider;
  persistidos en `cps_pizarras._ajustes` (clave meta: la poda de tableros
  ignora claves `_*`).
- **Figura perfecta (dibuja y sostén ~0.6 s)**: el trazo se ajusta a
  línea, polilínea, triángulo, cuadrilátero/rectángulo o elipse.
  Reconocedor propio: RDP anclado en los 2 puntos más alejados (RDP
  ingenuo degenera en contornos cerrados), limpieza de vértices
  colineales, umbral de elipse 0.18 (un rectángulo da error medio ≈1/3
  contra su elipse inscrita — verificado con test sintético de 7 casos).
  Las figuras se pintan como polilíneas RECTAS (flag `f`): el suavizado
  de puntos medios redondeaba las esquinas ajustadas.
- **Gestos GoodNotes**: el dedo NO dibuja cuando hay pencil — desplaza el
  lienzo; pellizco de 2 dedos = zoom 0.5×–4× (chip de % visible); toque
  corto de 2 dedos = deshacer, de 3 = rehacer (clasificado por el MÁXIMO
  de dedos del gesto, robusto al orden de levantado); **doble toque del
  DEDO = alternar pluma↔goma**. ⚠️ HONESTO: el doble toque del PROPIO
  pencil es UIPencilInteraction (nativo iPadOS) y Safari NO lo expone a
  web apps — el doble toque del dedo es el sustituto, documentado en el
  hint (toast al detectar el primer pencil). Mouse: rueda desplaza,
  ⌘/Ctrl+rueda zoom al cursor. Rechazo de palma: contactos ≥36 px de
  ancho se ignoran; si el pen está dibujando, el tacto no gesticula.
- **Lazo**: ahora también **Duplicar** (offset 24 px, la selección pasa a
  las copias). Sin dibujar: un dedo dibuja como antes (modo tacto puro);
  un 2.º dedo aborta el trazo a medias y pasa a gesto (como GoodNotes).
- Robustez: `setPointerCapture` con try/catch (punteros sintéticos);
  `getCoalescedEvents()` vacío (eventos sintéticos) cae a `[e]`.
- Arnés local `test-seed.html` (gitignoreado) prueba la pizarra real por
  eventos sintéticos en headless; capturas verificadas (trazo con
  presión, resaltador translúcido, rectángulo ajustado perfecto).

**Evaluar con el mentor (§4.4):**
- Botón `🪶 Evaluar` en la barra de la pizarra, SOLO visible con cuenta
  de Claude activa (`mentorDisponible()`, regla §0.7: sin key no existe).
- Exporta la página actual como JPEG (recorte al bbox de lo dibujado,
  fondo del papel, ≤1500 px) → cierra la pizarra (el panel del mentor
  vive debajo de su overlay) → abre el chat del mentor y envía la imagen
  como foto adjunta con un mensaje fijo. El MODO del chat protege el
  gating como siempre: en forcejeo el mentor pregunta y orienta SIN
  confirmar ni revelar (§0/§4 — "evaluar" durante el forcejeo es
  socrático por diseño); tras revelar sí compara con la solución oficial.
  La imagen jamás se persiste (regla existente del chat).
- sw.js **v15**. Verificación: node --check (17 módulos+sw), test
  unitario del reconocedor (7/7), cruce IDs HTML↔JS, arranque headless
  limpio y capturas del arnés.

**PENDIENTE humano:** probar en el iPad con Apple Pencil real: presión,
palma, dedo-desplaza, doble toque del dedo, pellizco, figura perfecta
(sostener al final del trazo) y el flujo Evaluar→mentor con su API key.

### Cierre de jornada 2026-06-11, noche (estado al apagar)

- **App v15** (sw.js al cierre de esa jornada; hoy va en **v21**:
  v16 = Fase 7, v17 = hotfix de su auditoría, ambos 2026-06-12,
  v18 = lecciones integradas + pizarra, v19 = Fase 6 completa,
  v20 = parches de sincronización, v21 = arena-s1 + selector de bloques
  (todos 2026-06-12)), todo
  commiteado y pusheado en `main`. Los 3 SQL de `supabase/` aplicados y
  verificados por E2E (Fase C 8/8, claustro 10/10, pensar-juntos 9/9 con
  struggle-first probado).
- **El sitio está PÚBLICO y en vivo**:
  https://imgoingsavage.github.io/cogitoergosum/ (GitHub Pages, branch
  main/raíz, `.nojekyll`, HTTPS). El repo es público desde hoy (auditado:
  sin secretos). Cada `git push` a main redespliega solo; la app
  instalada recibe la versión nueva en la recarga siguiente. Recordar:
  si el repo pasa ~60 días sin commits, GitHub pausa el cron keep-alive
  de Supabase — un commit lo reactiva.
- **Hecho en la jornada**: Fases A-D + chat socrático/mentor flotante +
  portada de login con video a 0.5× y vidrio líquido + botón ⏻ de cerrar
  sesión + ingestión de estudio Fases 4 y 5 (pool de examen: 40 ítems;
  38 unidades) + publicación del frontend.
- **Lo que queda, en una línea**: pruebas humanas (punto 6 de la lista de
  arriba) → fase 6 de estudio a decidir con el usuario (punto 7) →
  menores (punto 8). No hay código roto ni verificación pendiente del
  lado del agente.

### Bitácora 2026-06-12 — Fase 7 Arena de Entrevistas de Élite

**Pedido del usuario:** extender el Modo Estudio con una nueva fase para
preparación de entrevistas de élite en tres rutas: Quant/Hedge Fund,
MAANG/Big Tech, y Health AI/RWE. Especificación de 26 secciones entregada
en la sesión anterior (resumida en el handoff de compresión de contexto).

**Commit ea21c60 — pusheado a main. Estado final del JSON:**
`44 unidades · 7 bloques · 18 heurísticas · 75 archivos en SHELL`.

#### data/study.json

- **6 heurísticas nuevas** añadidas a `catalogoHeuristicas` después de
  `penultimo-paso`:
  `linealidad-esperanza`, `bayes-tasa-base`, `hashing-memoria`,
  `ventana-sql`, `dag-ajuste`, `tiempo-cero`.

- **Bloque `fase-7`** en `bloques[]` con 6 ítems de examen:

  | id | heurística | ruta |
  |----|-----------|------|
  | f7-ex-1 | linealidad-esperanza | quant |
  | f7-ex-2 | bayes-tasa-base | quant |
  | f7-ex-3 | hashing-memoria | maang |
  | f7-ex-4 | ventana-sql | maang |
  | f7-ex-5 | dag-ajuste | health-ai-rwe |
  | f7-ex-6 | tiempo-cero | health-ai-rwe |

  Cada ítem tiene `pistas[]` (array de 5 strings, nivel creciente) y
  `metadata` con `ruta`, `skills[]`, `errores_comunes[]`, `casos_borde[]`
  y `source: "original"` (problemas originales, sin copyright).

- **6 unidades** añadidas a `unidades[]` (al final, tras las de fase-5),
  cada una con `banco[]` de 4 ejercicios de tipos variados (quiz,
  acertijo, disparador) e `ideas_clave[]`. Tienen `metadata.ruta` para
  los ruta-chips en la UI.

#### data/teoria/ — 6 lecciones nuevas

| archivo | título | ruta |
|---------|--------|------|
| `arena-q1.md` | Linealidad de la esperanza bajo presión | quant |
| `arena-q2.md` | Bayes, tasas base y señales ruidosas | quant |
| `arena-m1.md` | Hashing, frecuencia y memoria comprada | maang |
| `arena-m2.md` | SQL Window Functions | maang |
| `arena-h1.md` | DAGs y adjustment sets | health-ai-rwe |
| `arena-h2.md` | Target trial emulation e immortal time bias | health-ai-rwe |

Todas con sección `## Señales de reconocimiento y jugadas` (tabla) y
`## Ejercicio de consolidación` (pregunta con respuesta oculta), en línea
con las lecciones de fases anteriores.

#### js/study.js — 3 cambios retrocompatibles

1. **`renderPasoForcejeo`**: detecta `item.pistas?.length` primero →
   panel `.pistas-container` con botón `"Pedir pista N/5"` que revela
   pistas una a una y actualiza `r.pistaUsada` + `r.pistasUsadas` en el
   registro. El camino `else if (item.pista)` sigue intacto para todas
   las fases anteriores (fases 1-5).
2. **`renderPasoPrediccion`**: añade `pistasUsadas: 0` al objeto de
   registro empujado al stack (además del `pistaUsada: false` existente).
3. **`renderizar` (lista de unidades)**: si `u.metadata?.ruta` existe,
   inserta `<span class="ruta-chip ruta-{ruta}">` entre el nombre y el
   libro.

#### css/styles.css — reglas nuevas (tras `.unidad-libro`)

```css
.ruta-chip          /* base: font 10px, uppercase, padding 2px 7px */
.ruta-quant         /* fondo violeta 18% opaco, texto #a78bfa */
.ruta-maang         /* fondo cyan 18% opaco, texto #67e8f9 */
.ruta-health-ai-rwe /* fondo verde 18% opaco, texto #86efac */
.pistas-container   /* flex column, gap 8px */
.pista-nivel        /* etiqueta "Pista N/5:", color --ambar */
```

#### sw.js — v16

Añadidas al SHELL las 6 rutas:
`data/teoria/arena-q1.md`, `arena-q2.md`, `arena-m1.md`, `arena-m2.md`,
`arena-h1.md`, `arena-h2.md`. Verificación: todos los 75 archivos del
SHELL existen en el filesystem (python3 cruzado).

#### Verificación pre-commit

- `node --check` en todos los módulos JS + sw.js: OK
- `python3` validó study.json: 44 unidades, 7 bloques, 18 heurísticas
- SHELL vs filesystem: 75/75 sin faltantes

#### Qué NO se hizo (y por qué)

- **Fase 6** (`fase-6` en `bloques[]`): no existe. El usuario saltó de
  fase-5 a fase-7 directamente. Queda pendiente (ver item 7 en "QUÉ
  FALTA").
- **pistas[] en fases 1-5**: no se migraron los ítems existentes de
  `pista` (string) a `pistas` (array). No hacía falta: el código nuevo es
  retrocompatible. Si se quiere enriquecer algún ítem anterior, basta con
  reemplazar `"pista": "..."` por `"pistas": ["...", "...", ...]` en ese
  ítem — sin cambios de código.

#### Auditoría de Oleada 1 (mismo día, commit 7700fc3 — sw.js v17)

Pedida por el usuario contra 14 criterios (rupturas de Estudio y
Entrenamiento, Pages/subpath, SW/SHELL, JSON, dependencias, secretos,
IA opcional, Constitución, copyright, lenguaje, pedagogía). Veredicto:
**publicar** — 6 hallazgos, ninguno estructural, todos parchados:

1. `arq1-q2`: la explicación contenía razonamiento a medio pensar
   ("multiplicado por... no, simplemente") que el usuario habría leído
   tal cual. Reescrita.
2. `arq2-q3`: referenciaba un "ejemplo del manual" con VPP=28% que no
   existe (el de la lección da ≈49%). Corregido a los datos reales.
3. `.pista-nivel` usaba `var(--ambar)` — token INEXISTENTE (el ámbar
   real es `--lampara`/`--alerta`); el color fallaba en silencio.
   Ahora `--alerta` (sancionado para atención por su propio comentario).
4. **Pistas graduadas no sobrevivían recargas**: el panel arrancaba de
   cero y volver a pedir podía REGRESAR `pistasUsadas` (3→1). Ahora se
   reponen desde el registro al renderizar y el contador nunca decrece
   (`Math.max`). Además las pistas se insertan ANTES del botón.
5. Anglicismos: "modelo excellent" (arena-q2.md), "patrón common"
   (arm2-q3).
6. Limpieza de los `.replace()` no-op del ruta-chip.

Verificado limpio en la misma auditoría: esquema fase-7 = fase-5
(`metadata` aditivo), `disparador` presente en los 6 ítems de examen,
heurísticas de unidades e ítems existen en el catálogo, cero IDs de
banco duplicados, lecciones resueltas por `data/teoria/${u.id}.md` con
nombres coincidentes, Cartógrafo mayor usa su propio mapa de
`badges.json` (las 6 heurísticas nuevas no lo afectan), rutas relativas
(subpath OK), SHELL 75/75, cero dependencias/secretos nuevos, pistas
estáticas (IA sigue opcional), ítems `source: "original"` y lecciones de
redacción propia con fuentes citadas. Hallazgos NO urgentes → punto 8
de "QUÉ FALTA" ("Oleada 2 de Fase 7").

### Bitácora 2026-06-12 (2) — repetición espaciada de estudio + Fase 6 a medias

Pedido del usuario en una sola instrucción: "comienza con la repetición
espaciada, para la fase 6 mete Zeitz, sube a AIME y mete más Engel, es
decir haz las 3" y, después, "ordénalos por dificultad".

**✅ Repetición espaciada del Modo Estudio (commit 09061e1, pusheado).**
Las preguntas de un quiz marcadas "mal" o "parcial" se acumulan en
`pendientesRepaso[unidadId]` (clave nueva en `storage.estudio`, dentro de
CLAVES_SYNC porque viaja con el progreso). El cierre de unidad ofrece
"Repasar N pregunta(s) pendiente(s)" → `iniciarRepaso(u)` re-corre el quiz
con `esRepaso: true` y SOLO esas IDs; al terminar, las acertadas salen de
la lista y el registro de la unidad completada (fecha/aciertos originales)
se preserva con spread. El quiz ahora opera sobre `preguntasIds[]` (IDs, no
índices) para que el subconjunto de repaso funcione sin tocar `u.banco`.
Verificado: node --check, JSON, arranque headless.

**⚠️ Fase 6 — INICIADA Y A MEDIAS (working tree, SIN commit).** Ver el
detalle completo y la lista de lo que falta en el punto **7 de "QUÉ FALTA"**
(reescrito hoy). Resumen del estado: en `data/study.json` ya están las **3
heurísticas nuevas** (`transformacion`, `recurrencia`, `ecuacion-funcional`,
total 21) y el **bloque `fase-6`** con su examen de **7 ítems**, insertado
correctamente ANTES de `fase-7`. **Faltan las 10 unidades, sus 10 lecciones
markdown, el bump de `sw.js` a v19 y la validación.** Mientras tanto el JSON
está en estado roto intermedio (fase-6 apunta a 10 unidades inexistentes; la
app no crashea pero renderiza el bloque vacío): **NO commitear ni publicar
hasta completar las unidades.** La interrupción fue deliberada (el usuario
pidió actualizar este handoff antes de seguir).

---

### Bitácora 2026-06-12 (3) — parches de la auditoría de sincronización

Auditoría de arquitectura (Fable 5) sobre bbe1fa3: 1 mayor, 3 menores,
1 sugerencia, 0 críticos. Parches aplicados (sw.js → v20):
- **sync.js `cadenas()`**: `new Date(fecha + 'T00:00:00')` — el parseo UTC
  de 'YYYY-MM-DD' hacía que días consecutivos no encadenaran en husos al
  oeste y `adoptarOUnir()` habría recomputado una racha de N días como 1
  (verificado por test en 3 husos; el flujo diario local nunca estuvo
  afectado). ERA EL ÚNICO BLOQUEANTE para la prueba humana de 2
  dispositivos (C.6).
- **sync.js `unirEstudio()`**: ahora une `pendientesRepaso` (antes se
  descartaban los del otro dispositivo).
- **sync.js `sincronizar()`**: outbox en lotes de 200, removiendo cada lote
  confirmado de inmediato (sin duplicados si falla un lote intermedio).
- **api.js `descargarEventos()`**: documentada como reserva sin llamadores.
- **sw.js**: refresco en segundo plano registrado con `event.waitUntil`
  (patrón stale-while-revalidate canónico).
Verificado: node --check (18 módulos + sw), JSON, test de cadenas() en
Mexico_City/UTC/Tokio, arranque headless limpio.

---

### Bitácora 2026-06-12 (4) — auditoría de contenido + Fase 7 completa contra spec

**Correcciones de contenido (auditoría):**
- **1 mayor**: biyección Fibonacci en `aime-cnt.md` — cadenas de longitud n (no n−1); la recurrencia y f(n)=Fibonacci(n+2) son correctas.
- **8 menores**: f4-ex-7 reemplazado (problema de producto de signos 5/9, heurística `casework`); f6-ex-5 Cauchy completado con f(0)=0 y f(−x)=−f(x); f7-ex-2 segunda pregunta reformulada a prevalencia mínima; f7-ex-4 solución RANK/DENSE_RANK corregida; f7-ex-5 C como antecedente/Z-bias; f7-ex-6 typo "redesiguarías"; zeitz-85a punto de Fermat con cláusula ángulo ≥ 120°; zeitz-85b tangencia exterior/interior y lema PAC/PBD; z85b-q4 reescrito (depende del sentido del movimiento).

**Unidad ML Systems (arena-s1):**
- Lección integrada `data/teoria/arena-s1.md` (7 secciones: principio central, skew, drift, offline≠online, plantilla 13 campos, señales/jugadas, ejercicio).
- Banco de 4 preguntas (`ars1-q1..4`): quiz×2, acertijo, disparador.
- Heurística `skew-drift` añadida al catálogo.
- Chip `ml-systems` (naranja) en la UI.
- `arena-s1` insertada en `fase-7.unidades` con orden 5; arena-h1→6, arena-h2→7.

**Examen de fase-7 ampliado a 7 ítems:**
- `f7-ex-7` (heurística `skew-drift`, ruta `ml-systems`): concept drift vs data drift, training-serving skew en pipeline duplicado, plan canary + guardrails + rollback; 5 pistas progresivas.
- Verificado: la aprobación del examen se calcula sobre `items.length` y `ex.registros.length` — no hay tamaño fijo hardcodeado.

**Modo entrevistador del Mentor:**
- `SYSTEM_CHAT_ENTREVISTADOR` en aiMentor.js con repertorio de preguntas por ruta.
- `contextoEntrevista()` exportada de study.js: detecta examen fase-7 en curso (devuelve enunciado) o unidad fase-7 abierta (devuelve ruta y título).
- `modoMentor()` en app.js delega a `contextoEntrevista()` para elegir entre `'entrevistador'` y `'estudio'`.
- Sin API key: nada cambia, mentorDisponible() oculta todo.

**Plantilla de diseño y cajas negras:**
- Plantilla de 13 campos en arena-s1.md y arena-h2.md.
- `[CAJA NEGRA OK]` IPW en arena-h2.md; Eve's law en arena-q1.md.

**Confianza 1-5 en la predicción del examen:**
- Fieldset de 5 radios `examen-confianza` antes del botón "Registrar predicción".
- Campo `confianza` guardado en `registros[]`.
- Frases de calibración al revelar: sobre-confianza (≥4 + errada) y sub-confianza (≤2 + correcta).

**Candado de unidades eliminado + selector de bloques:**
- `unidadDisponible()` devuelve siempre `true`.
- `let bloqueVisible` + `bloqueVisibleObj()` en study.js.
- `<select id="estudio-bloque-selector">` en index.html; CSS coherente.
- `iniciarExamen()` y `renderizar()` usan `bloqueVisibleObj()`; `progresoResumen()` sigue con `bloqueActual()`.
- El progreso oficial (rachas, resumen) sigue anclado al primer bloque sin examen aprobado.

**sw.js → v21.** Verificaciones 1-5 en verde: node --check (18 módulos + sw), JSON válido, cruce SHELL sin faltantes, correcciones de auditoría confirmadas, no hay 6 hardcodeado en el flujo del examen.

---

### Bitácora 2026-06-12 (5) — auditoría senior de arquitectura + plan por oleadas (SOLO documentación)

Auditoría completa (Fable 5) sobre el commit 8a13241, contrastando
documentación contra código real: 18 módulos JS, los 3 SQL, index.html,
sw.js y los puntos de llamada verificados por grep. Diez áreas: persistencia
multi-dispositivo, sync Supabase, mentor IA, login Google, borrado de
usuarios, escalabilidad, excepciones, responsividad, seguridad y SW/PWA.
**En esta sesión NO se tocó código ni datos**: solo esta documentación y
`PROMPT-MAESTRO-OLEADAS-1-3.md`.

**Hallazgos de severidad Alta (los 5 riesgos del proyecto):**

1. **La sincronización solo BAJA datos al login.** `adoptarOUnir()` tiene un
   único llamador (app.js, tras login) y `descargarEventos()` ninguno. Dos
   dispositivos con sesión persistente NO convergen hasta un re-login, y el
   snapshot (last-writer-wins) puede RETROCEDER en el servidor: el último en
   subir pisa el progreso del otro hasta el siguiente login. El event log
   preserva los datos, pero nada lo lee. → Parche: bajada continua
   (unirRemoto() dentro de sincronizar(), Oleada 3).
2. **`invitaciones.usado_por` referencia auth.users SIN `on delete`**
   (schema-fase-d.sql): `borrar_mi_cuenta()` falla con error de FK para
   cualquier usuario que canjeó un código (viola §0.1 "2 clics") y bloquea
   el reset de usuarios de prueba. Los E2E pasaron por orden afortunado de
   borrado. → Parche SQL: `on delete set null` (Oleada 2).
3. **El mentor es indiagnosticable**: los errores de la API de Claude
   descartan status y cuerpo ("API ${status}" → catch genérico). Hipótesis
   del bug "no responde aunque pegué la key", en orden de probabilidad:
   (a) Console sin saldo (400 credit balance), (b) key pegada en OTRO origen
   o dispositivo (LocalStorage es por origen: localhost ≠ github.io ≠
   celular), (c) credencial de claude.ai en vez de API key sk-ant- (401).
   → Parche: status+cuerpo en los Error + botón «Probar la cuenta» (Oleada 1).
4. **`cps_credenciales` guarda la contraseña en texto plano.** Fue decisión
   explícita del usuario (bitácora noche, 4); innecesaria técnicamente
   porque la sesión ya persiste por refresh token. PENDIENTE de decisión
   del usuario — NO tocar sin preguntarle.
5. **`storage.save()` no maneja cuota llena**: una excepción a mitad de
   `completarSesion()` puede dejar estado parcial. → Parche: poda de
   `sesionesArchivadas` + reintento + registro (Oleada 1).

**Hallazgos Media/Baja**: sin idempotencia server-side de events (reintentos
del outbox pueden duplicar filas); un solo breakpoint CSS (540px — tablet
usa layout desktop); `cache.addAll` con 88 archivos frágil a un 404 (ya
ocurrió una vez); disciplina de VERSION puramente manual; el modo
entrevistador se activa también para ítems viajeros de fases 0-6 dentro del
examen de fase-7 (pool acumulativo); etiqueta del último botón en quiz de
repaso compara contra `banco.length` en vez del subconjunto; `tokenVigente()`
invalida la sesión en silencio; `login.mp4` pesa 4.8 MB.

**Lo que la auditoría declaró BIEN DISEÑADO (no tocar):** el modelo
event-log + recomputo de rachas (está sub-disparado, no mal diseñado),
storage/api/sync como fachadas (cambiar de backend sigue siendo un archivo),
las políticas RLS (struggle-first garantizado por servidor), el patrón
"sin key no existe", el timer por timestamps y el manejo de Range del video.

**Plan aprobado — 6 oleadas** (cada una deja la app funcional; backlog
completo P0-P3 en la conversación de auditoría):

| Oleada | Contenido | Estado |
|---|---|---|
| 1 | Mentor diagnosticable (status+cuerpo, «Probar la cuenta», aviso sk-ant-), puerta única `llamarMessagesAPI` (problemFactory unificado), `save()` con poda ante cuota, registro `cps_diagnostico` + tarjeta Dashboard | ❌ Lista para ejecutar con el prompt maestro |
| 2 | SQL: FK `usado_por → set null` + `events.uid unique`; `on_conflict=uid` en api.js | ❌ Ídem (el SQL lo pega el usuario ANTES del código) |
| 3 | Convergencia multi-dispositivo: `unirRemoto()` + bajada continua en `sincronizar()` + disparo por visibilitychange (≥5 min) + aviso de sesión inválida | ❌ Ídem |
| 4 | Login con Google (Supabase Auth, flujo implícito sin SDK: `/auth/v1/authorize?provider=google`, tokens en el hash; checklist completo en la auditoría). ⚠️ Con "Confirm email" desactivado, mismo correo por Google puede crear un usuario DUPLICADO — decidir política antes | ❌ Requiere acciones del usuario (Google Cloud Console + Supabase) |
| 5 | Limpieza: `cps_schemaVersion` + migraciones en storage.js, extraer mentorChat.js/cuentaUI.js de app.js, script versionado de verificación del shell, coherencia del entrevistador (solo ítems con `metadata.ruta`) | ❌ |
| 6 | Responsividad/hardening: breakpoint ~900px (tablet), barra de pizarra con wrap en móvil, comprimir login.mp4 (4.8→~2 MB), decisión sobre `cps_credenciales`, pasada Lighthouse | ❌ |

**Fuera de las oleadas, pendiente CON el usuario:** reset de usuarios de
prueba (censo SQL → backup → `delete from auth.users where email <> '…'`;
desbloqueado por la FK de la Oleada 2) y las pruebas humanas del punto 6
de «QUÉ FALTA».

**PROMPT MAESTRO GENERADO**: `PROMPT-MAESTRO-OLEADAS-1-3.md` (raíz del
repo). Instrucciones exactas, paso a paso y con código literal, para que un
agente (Sonnet 4.6+) ejecute las oleadas 1-3 en una sesión. Orden crítico
codificado dentro: el SQL va PRIMERO y el agente debe esperar la
confirmación del usuario (el `on_conflict=uid` del código rompería la
sincronización si llegara antes que la columna; el SQL sí es retrocompatible
con la app v21 en vivo). Su Paso 12 escribe la **bitácora (6)** de este
archivo al terminar y marca las casillas de la tabla de arriba.

---

### Bitácora 2026-06-12 (6) — Oleadas 1-3: sincronización convergente + mentor diagnosticable

**SQL aplicado** (`supabase/schema-parches-2026-06-12.sql`):
- FK `invitaciones.usado_por → on delete set null`: `borrar_mi_cuenta()` ya no falla con error de FK para usuarios que canjearon un código (§0.1).
- `events.uid text unique`: idempotencia del outbox — reintentos duplicados se ignoran con `on_conflict=uid`.

**Bajada continua (convergencia multi-dispositivo):**
- `unirRemoto(remoto)` extraída en `sync.js`: función pura que une historial, pisos, sesiones archivadas, problemas generados, estudio, insignias y revisiones, y recomputa las rachas. La llaman tanto `adoptarOUnir()` (rama "unido") como la bajada continua.
- En `sincronizar()`, antes de subir el snapshot propio, se descarga el remoto y se une con `unirRemoto()`. Dos dispositivos con sesión viva convergen sin re-login; el snapshot del servidor nunca retrocede.
- Disparador por `visibilitychange` (≥5 min de inactividad) en `iniciar()`: volver a la pestaña tras un rato trae el progreso del otro dispositivo sin re-login.
- `cps:sesion-invalida` disparado por `tokenVigente()` cuando el refresh falla: la UI puede reaccionar (syncUI llama `avisar()`).
- Al adoptar un snapshot en dispositivo nuevo, se limpia `quizEnCurso` y `examenEnCurso` (estado efímero de otro aparato).

**Eventos idempotentes:** `subirEventos` incluye el campo `uid` en cada fila y usa `events?on_conflict=uid` con `resolution=ignore-duplicates`. Los reintentos del outbox no crean duplicados en el servidor.

**Mentor diagnosticable:**
- `llamarMessagesAPI(body)` exportada de `aiMentor.js`: única puerta de red a `api.anthropic.com` para todos los módulos. Los errores HTTP incluyen status y cuerpo completo (max 200 chars) — ya no se descarta el motivo del fallo.
- `llamarClaude` y `llamarApi` reescritas para usar `llamarMessagesAPI` (el código de fetch vive en un solo lugar).
- `problemFactory.js` unificado: eliminados `API_URL` y `MODEL` propios; usa `llamarMessagesAPI` importada.
- `probarCuenta()` exportada: llama con `max_tokens: 1` y devuelve `{ ok, mensaje }` siempre sin lanzar; distingue 401, 400/credit, 404, 429 con frases accionables.
- Botón «Probar la cuenta» en la tarjeta "Potenciar con Claude" del Dashboard; aviso de prefijo `sk-ant-` al agregar una cuenta.

**Cuota segura y diagnóstico local:**
- `storage.save()` atrapa `QuotaExceededError`: poda `sesionesArchivadas` a 100 y reintenta; si falla de nuevo, registra en diagnóstico sin lanzar (evita estado parcial en `completarSesion()`).
- `registrarDiagnostico(origen, mensaje)` en `storage.js`: ring buffer de 50 entradas en `cps_diagnostico` (fuera de `CLAVES_SYNC` — solo este dispositivo).
- Catches instrumentados: `sincronizar()` (sync), `solicitarHint` (mentor-hint), y los 3 catches del mentor en `app.js` (mentor).
- Tarjeta «Diagnóstico» en el Dashboard: muestra los últimos 15 avisos, útil para depurar fallas silenciosas.

**Micro-arreglo study.js:** botón "Siguiente pregunta"/"Cerrar evaluación" en `renderPreguntaQuiz()` ahora compara contra `ids.length` (subconjunto del repaso) en lugar de `u.banco.length` — la etiqueta ya no miente en la última pregunta de un repaso.

**sw.js → v22.** Verificado: `node --check` 18 módulos + sw, JSON OK, SHELL OK, cruce de IDs HTML↔JS, todos los cables confirmados por grep.

---

### Bitácora 2026-06-12 (7) — Oleadas 4-6: OAuth Google + hardening + limpieza

**Oleada 4 — Login con Google (OAuth 2.0 vía Supabase):**
- `js/api.js`: `loginConGoogle()` redirige a `/auth/v1/authorize?provider=google`; `manejarHashOAuth()` consume el fragment `#access_token=…` al volver, guarda sesión y limpia el hash con `history.replaceState`. No-op si no hay hash ni token — cero ruido en arranques normales.
- `index.html`: botón `#btn-login-google` ("Entrar con Google") en `.login-acciones` con clase `login-google` para el separador visual.
- `css/styles.css`: `.login-google` con `border-top` sutil para separar visualmente de email/contraseña.
- `js/app.js → init()`: `Api.manejarHashOAuth()` se ejecuta ANTES de `configurarPantallaLogin()`; si devuelve sesión, la portada no se abre y se llama `despuesDeEntrar()` tras cargar los problemas (merge + sync como si el usuario hubiese entrado con email).
- Listener `#btn-login-google`: muestra "Redirigiendo a Google…" y llama `Api.loginConGoogle()`.
- **Configura en Supabase** → Authentication → Providers → Google: pega el `Client ID` y `Client Secret` de Google Cloud Console. Ruta de retorno: la misma URL de la app (GitHub Pages o `localhost`).

**Oleada 5 — Limpieza arquitectónica (sin extracción de módulos):**
- `js/study.js → contextoEntrevista()`: el modo entrevistador solo se activa cuando el ítem actual tiene `item.metadata.ruta`; los ítems acumulados de fases 0-6 (sin `metadata.ruta`) devuelven `null` — el Mentor vuelve a modo `estudio` para ellos.
- `js/storage.js`: `schemaVersion: 1` en DEFAULTS (fuera de CLAVES_SYNC); `migrarSiNecesario()` exportada — stub idempotente listo para futuras migraciones. Se llama en `init()` como primera instrucción.
- `scripts/verificar-shell.py` NUEVO: comprueba que todos los archivos de SHELL existen, que los JSON son válidos y que no hay IDs duplicados en index.html. Salida "OK — N archivos" o lista de errores + exit 1. Ejecutar con `python3 scripts/verificar-shell.py` (89/89 OK).
- Extracción de `js/cuentaUI.js` y `js/mentorChat.js` **diferida**: alta complejidad por estado compartido (`vistaActual`, `problemaActual`, `chatsEfimeros`); sin urgencia mientras app.js < 2100 líneas.

**Oleada 6 — Responsividad y hardening:**
- `css/styles.css`: breakpoint `@media (max-width: 900px)` (tablet): reduce `gap`, `padding` y `font-size` de los botones de la barra de la pizarra para evitar overflow horizontal en iPad.
- `cps_credenciales` ELIMINADA (decisión del usuario): clave `credenciales` borrada de DEFAULTS en `storage.js`; toda la lógica de `precargarCredenciales()` y 6 llamadas a `Storage.save('credenciales', …)` eliminadas de `app.js` (tanto en `configurarPantallaLogin` como en `configurarCuentaUI`); texto "Al entrar, tus credenciales se recuerdan solo en este dispositivo." eliminado de `index.html → login-nota`.

**sw.js → v23.** Verificado: `node --check` 18 módulos + sw, `python3 scripts/verificar-shell.py` 89/89 OK, sin IDs duplicados en HTML, todos los cables confirmados por grep.

---

### Bitácora 2026-06-12 (8) — Extracción de módulos + login.mp4 pendiente

**Extracción de `js/cuentaUI.js` y `js/mentorChat.js` de app.js:**
- app.js: 2017 → 1454 líneas (-563). Refactor sin cambio funcional.
- `js/cuentaUI.js` (267 l): portada de login + tarjeta "Mi cuenta". Recibe `onEntrado` callback via `iniciar()` para que app.js ejecute `renderizarSesion()` + `actualizarFreshStartUI()` después del login sin ciclo de importación. Exporta: `configurarLogin`, `configurarCuenta`, `despuesDeEntrar`, `abrirPortada`, `renderizar`.
- `js/mentorChat.js` (358 l): todo el chat socrático, superficies de IA y fotos. Recibe `getVistaActual` / `getProblemaActual` via `iniciar()` (mismo patrón). Exporta: `actualizarSuperficiesIA`, `actualizarMentorUI`, `enviarMensajeMentor`, `iniciarConFoto`, `configurarFlotante`, `configurarFoto`, `configurarRevision`.
- `configurarPizarra()` en app.js usa `MentorChat.iniciarConFoto()` en lugar del bloque inline.
- Imports de aiMentor.js en app.js reducidos (chatMentor/prepararImagen/etc. ahora solo en mentorChat.js).
- sw.js → **v25**: `js/cuentaUI.js` y `js/mentorChat.js` añadidos al SHELL (91 archivos; verificado con `scripts/verificar-shell.py`).

**Reset de usuarios de prueba cancelado** por decisión del usuario.

**login.mp4 pendiente de comprimir** (ffmpeg no instalado en el momento; cosmético): `brew install ffmpeg` y luego `ffmpeg -i assets/video/login.mp4 -c:v libx264 -crf 28 -preset slow assets/video/login.mp4`. Subir VERSION en sw.js al hacerlo.

**Opacidad del recuadro de login** subida (2026-06-12): gradiente 0.05→0.20 → 0.10→0.72; blur 6px → 20px; sw.js → v24 (commit anterior a esta bitácora).

---

### Bitácora 2026-06-13 (9) — Mentor local híbrido: backend RAG + cliente frontend

Nuevo subsistema **opcional** (no toca el mentor Claude actual). Diseñado tras
una auditoría de arquitectura senior (ver el mensaje del agente / README §0).

**Backend** (`mentor-backend/`, NO se sirve en Pages como app; es un
deployable aparte para una laptop Linux i5/16GB):
- Stack: FastAPI + Qdrant (Docker, loopback) + Ollama (`deepseek-r1:1.5b` +
  `nomic-embed-text`). Cliente Claude BYOK se queda 100% en el navegador: la
  key JAMÁS llega a este backend (enrutarla aumentaría su exposición).
- `ingest.py`: ingesta idempotente (hash SHA-256) de `Biblioteca/*.txt` con
  chunking estructural y metadata (materia/tema/dificultad/tipo_contenido).
- Dual prompt: TEORÍA (expositor) vs EVALUACIÓN (socrático estricto). Política
  anti-fuga en 3 capas: filtro Qdrant excluye `solucion`/`moraleja` en
  EVALUACIÓN + segundo filtro en memoria + auditoría de la salida.
- Cola `asyncio` + 1 worker + timeout + TTL (NO BackgroundTasks). 202 + polling.
- Auth: JWT de Supabase verificado por firma (JWKS/RS256) + service token +
  rate limit. OWASP comentado in-situ. Métricas en SQLite (sin texto de usuario).
- **GARANTÍA "nunca texto íntegro"**: `retrieved_context` expone solo
  metadatos; el `texto` del chunk se queda en el servidor y alimenta el
  contexto del modelo; al usuario solo llega la SÍNTESIS. Decisión de corpus:
  textos íntegros (cada usuario aportó su copia comprada); `Biblioteca/` y
  `qdrant_storage/` siguen fuera del repo (.gitignore).
- 14 archivos, sintaxis verificada. NO probado end-to-end aquí (esta Mac no es
  el target: Ollama/Qdrant/i5 viven en la laptop Linux). Correr `README §2`.

**Frontend** (`js/mentorLocal.js` + cableado):
- `mentorLocal.js`: cliente del backend (health probe con cache 60s, POST
  202 + polling, fallback graceful a null). Config local en `cps_mentorLocal`
  (url, serviceToken, on/off) — FUERA de CLAVES_SYNC, como `mentorIA`.
- `mentorChat.js`: en modo **estudio** (TEORÍA) y sin foto, intenta el mentor
  local primero; si la laptop está apagada o falla, cae a Claude; si tampoco
  hay Claude, queda el aviso de "no respondió". Forcejeo/Arena/revisión siguen
  en Claude (gating intacto — el 1.5B no hace de tutor socrático).
- `actualizarMentorUI()`: la burbuja aparece para usuarios sin Claude pero con
  backend local SOLO en modo estudio.
- UI: tarjeta "Mentor local (opcional)" en el Dashboard (`local-*` IDs) +
  `configurarMentorLocalUI()` en app.js. Estilo `.check-fila` en styles.css.
- `sw.js` → **v26**: `js/mentorLocal.js` en SHELL (92 archivos verificados).

**Pendiente humano (en la laptop Linux):** `ollama pull`, `docker compose up`,
`pip install`, `python ingest.py`, `uvicorn`, túnel cloudflared; luego en la
app: activar el mentor local con la URL del túnel y el service token, y probar
una explicación en Modo Estudio. Decidir `EVALUACION_FALLBACK` (curated por
defecto; "local" arriesga el 1.5B).

---

### Convenciones que NO se negocian (resumen operativo)

- Español en todo; vanilla JS, ES6 modules, CERO librerías/CDNs/build.
- `storage.js` es la única puerta a LocalStorage. `cuentaActiva()` de
  aiMentor.js es la única fuente de la key de Claude. `cps_mentorIA` y
  `cps_asignacion` JAMÁS viajan al servidor (exclusión en CLAVES_SYNC).
- La IA y la cuenta son SIEMPRE opcionales: cada feature debe funcionar
  (o desaparecer limpiamente) sin ellas. La app jamás bloquea por red.
- Clasificaciones/estrategias nunca visibles antes de resolver.
- Modelo IA: `claude-opus-4-8`. Validar todo contra la Constitución §0;
  ante la duda, preguntar al usuario ANTES de implementar.

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
  proceso de revisión; eevaluar solo si la PWA muestra límites reales).

---

## §6b. PROTOCOLO DE TRABAJO PARALELO CON MÚLTIPLES CUENTAS

Cuando dos sesiones de Claude trabajan en paralelo sobre este repo:

### Regla de oro
**Una sesión activa por archivo a la vez.** Nunca dos sesiones editando
`data/study.json` o `sw.js` simultáneamente.

### Antes de empezar (siempre)
1. `git pull` para partir del estado más reciente.
2. Revisar `data/arena-ingesta-ledger.json`: tomar el **siguiente libro
   en estado `"pendiente"`** según el orden de prioridad §10 de
   `PROMPT-MAESTRO-ARENA.md`.
3. Marcar ese libro como `"en_progreso"` y hacer commit del ledger
   **antes** de empezar el trabajo de contenido.
4. Nunca tomar un libro que otra sesión tenga en `"en_progreso"`.

### Al terminar (siempre)
1. Marcar el libro como `"completado"` con `preguntas_agregadas` y
   `unidades_creadas` actualizados.
2. Commit de todos los archivos tocados (study.json, sw.js, teoría .md,
   ledger, HANDOFFCES.md con la bitácora del turno).
3. Push antes de cerrar la sesión.

### División recomendada por sector
| Cuenta | Sectores preferentes |
|--------|---------------------|
| A | `quant` (Practical Guide, Joshi, probabilidad) |
| B | `maang`, `ciencia-datos`, `conductual` |
| Cualquiera | `ml-systems`, `health-ai-rwe`, Sector C |

### Prompt de arranque para una sesión nueva
```
lee HANDOFFCES.md primero (§0 es ley, §5.4 es el mapa),
luego ejecuta las indicaciones de PROMPT-MAESTRO-ARENA.md.
Antes de empezar: haz git pull y revisa el ledger
(data/arena-ingesta-ledger.json) para saber qué libro tomar —
elige el siguiente en estado "pendiente" según el orden §10,
pero NUNCA el que otra sesión tenga en "en_progreso".
```

---

## Bitácora 2026-06-12 (10) — Arena tanda 1: Heard on the Street, 31 preguntas

**Qué se hizo**

- Creado `data/arena-ingesta-ledger.json` con las 43 entradas del plan maestro
  (estado `pendiente` por defecto; `en_progreso` para Heard on the Street).
- Cableadas rutas nuevas `ciencia-datos` y `conductual` en CSS (`styles.css`)
  y en el mapa de etiquetas de `study.js` (línea 243).
- Añadidas 3 heurísticas a `catalogoHeuristicas` (total: 25):
  `paridad-cuadrados`, `no-arbitraje`, `cadena-markov-ee`.
- Creadas 3 unidades en `fase-7` (arena-q3/q4/q5, órdenes 8-10) con 31
  preguntas de banco combinadas (arq3-q1..q11, arq4-q1..q10, arq5-q1..q10).
- Añadidos 3 ítems al examen de `fase-7` (f7-ex-8/9/10; total: 10 ítems).
- Creados `data/teoria/arena-q{3,4,5}.md`; toda la matemática verificada
  con Python antes de incluirla.
- `sw.js` → `v27`; nuevos archivos de teoría en SHELL.

**Estado** — Heard on the Street: 31/60 preguntas (en_progreso; faltan 29).
**Siguiente** — Completar cuota (arena-q6/q7 con ~29 preguntas más) y luego
iniciar A Practical Guide to Quantitative Finance Interviews.

## Bitácora 2026-06-13 (Arena tanda 4) — Quant Job Interview (Joshi), 67 preguntas

**Qué se hizo** (ruta `quant`, libro completado en el ledger)

- Destilado **Quant Job Interview Questions and Answers** (Joshi, Denson &
  Downes) del cap. 3 (probabilidad y procesos estocásticos) y cap. 8
  (logic/brainteasers), apuntando a las secciones de ejercicios por el índice.
- **6 unidades nuevas** en `fase-7` (arena-q8..q13, órdenes 17-22) con **61
  preguntas de banco** (10-11 por unidad):
  - arena-q8 · Esperanza, juegos y parada óptima.
  - arena-q9 · Probabilidad condicional, Bayes y conteo.
  - arena-q10 · Distribuciones, geometría y estadísticos de orden.
  - arena-q11 · Movimiento browniano, Itô y martingalas.
  - arena-q12 · Brainteasers: trucos, invariantes y conteo.
  - arena-q13 · Brainteasers: lógica, inducción y juegos.
- **6 ítems de examen** `f7-ex-15..20` (total fase-7: 20 ítems), con `pistas[]`
  de 5 niveles **como strings** (lo que renderiza `study.js`; ver nota abajo).
- **4 heurísticas nuevas** en `catalogoHeuristicas` (total 33):
  `parada-optima`, `martingala-parada`, `conservacion`, `desdoblar`.
- **6 lecciones** `data/teoria/arena-q{8..13}.md` (destilados con tablas de
  disparadores y síntesis en blockquote, formato estándar).
- `sw.js` → **v30**; las 6 lecciones añadidas al SHELL (107 archivos).
- Script de ingesta re-ejecutable e idempotente: `scripts/ingest-joshi.py`
  (aborta si arena-q8 ya existe).

**Verificación** — `node --check sw.js` OK; `study.json`/`problems.json` JSON
válido; `scripts/verificar-shell.py` → OK 107 archivos; unicidad global de ids
sin duplicados; integridad referencial (heurísticas, lecturas .md, registro en
bloque) OK; **todas las respuestas numéricas verificadas con Python** (parada
óptima 14/3, 3 caras→14 tiros, Bayes 8/17, hormiga en cubo 8 min, ruina 0.92,
P(X₂<0)=1/4, Romeo&Julieta 7/16, dardo 2R/3, matriz de correlaciones no PSD,
det=−0.316, etc.); recursos sirven 200 por HTTP.

**Notas para el siguiente agente**
- ⚠️ Bug latente preexistente (NO mío): los ítems `f7-ex-13` y `f7-ex-14`
  (tanda 3) usan `pistas` como objetos `{nivel,texto}`, pero `study.js:818`
  hace `createTextNode(item.pistas[n])` → renderiza "[object Object]". El
  esquema correcto y el que la UI muestra bien es **array de strings** (§4.3
  del PROMPT). Conviene migrar f7-ex-13/14 a strings en una pasada futura.
- `node --check` sobre `js/*.js` falla en ESTE entorno (Linux) porque son
  módulos ES y node los trata como CommonJS; es ambiental, no del código (falla
  en archivos no tocados). La verificación real es `verificar-shell.py` + el
  navegador.

**Siguiente** — Según orden §10: **Fifty Challenging Problems in Probability**
(ruta `quant`, cuota 60), luego Blitzstein/DeGroot/Casella, y después ruta
`maang` (Cracking the Coding → System Design).

## Bitácora 2026-06-14 (Arena tanda 13) — Reliable Machine Learning, 62 preguntas

Procesado `Reliable Machine Learning` (Chen, Murphy, Parisa et al., O'Reilly)
— libros[13] del ledger, ruta `ml-systems`, cuota 25. Es el ledger.estado
13º libro en pasar a `completado`. **Valor NUEVO** de confiabilidad/SRE para
ML que complementa Huyen DMLS (tanda 12) y el MLOps básico de Cracking cds3 sin
duplicar. 4 unidades nuevas (`fase-7`, órdenes 63-66):
- **arena-rml1** — ciclo de vida del ML + SLOs (el loop; señales doradas, salud
  del modelo, métrica de negocio; models-as-code, launch slowly, isolate-at-
  data-layer, "most failures are not ML failures").
- **arena-rml2** — datos como pasivo + principios de entrenamiento confiable
  (data as liability, Sweeney 87%, borrado por cifrado, MCAR/MAR/MNAR, feature
  store, model management, models-will-be-retrained, multi-versión, good-models-
  become-bad/fallback, train-too-fast/race conditions, utilization vs efficiency,
  training-serving skew).
- **arena-rml3** — serving + observabilidad (QPS/latencia/tail/dónde-vive/GPU-vs-
  CPU-sparse; 4 arquitecturas offline/online/MaaS/edge; monitoreo vs
  observabilidad, mentalidad de detección, skew, retraining como roll-forward).
- **arena-rml4** — respuesta a incidentes (estado+roles+registro; fases;
  IC/comms/ops/planning; Public/Fuzzy/Unbounded; Historia 1 "búsqueda que no
  encuentra"; preparación por rol; ética del on-call).

60 preguntas de banco (15/unidad) + 2 ítems de examen (**f7-ex-46** incidente
ML, **f7-ex-47** SLOs de ML) = 62. 10 heurísticas nuevas (confiabilidad-ml-no-es-
ml, definir-slo-ml, desplegar-modelo-gradual, datos-como-pasivo, asumir-
reentrenamiento, vigilar-training-serving-skew, elegir-arquitectura-serving,
observabilidad-ml-produccion, responder-incidente-ml, monitorear-edad-modelo);
reúsa elegir-batch-vs-online. Catálogo total: 90 heurísticas. `sw.js` **v41**
(151 archivos en shell; +4 lecciones `data/teoria/arena-rml{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados (unidades/banco/examen/
heurísticas); integridad referencial OK (heurísticas existen, lecciones .md
existen, unidades registradas en bloque `fase-7` → 66); `verificar-shell.py` OK.
Contenido anclado en el libro (respuestas conceptuales de ML/sistemas, §1.2);
sin verificación Python por no haber problemas numéricos.

**Siguiente** — orden §10 (ml-systems): **Machine Learning Design Patterns**
(libros[14], ruta `ml-systems`, cuota 25), luego Site Reliability Engineering,
Observability Engineering, Rules of ML, Hidden Technical Debt, Interpretable ML,
ISL. Próxima unidad: órdenes desde 67, `f7-ex-48`+, VERSION v42+, ids de unidad
`arena-mldp1..` (o el prefijo que decidas; el banco usa `ar<unit>-q<n>`).

## Bitácora 2026-06-14 (Arena tanda 14) — Machine Learning Design Patterns, 62 preguntas

Procesado `Machine Learning Design Patterns` (Lakshmanan, Robinson & Munn,
O'Reilly) — libros[14] del ledger, ruta `ml-systems`, cuota 25. 14º libro en
`completado`. Organizado por los **30 design patterns** del libro
(problema→solución→trade-offs), valor NUEVO frente a Huyen DMLS, Reliable ML y
Cracking DS. 4 unidades (`fase-7`, órdenes 67-70):
- **arena-mldp1** — representación de datos y de problemas (Hashed Feature,
  Embeddings, Feature Cross, Multimodal Input, Reframing, Multilabel).
- **arena-mldp2** — ensembles, cascada, clase neutra y rebalanceo (Ensembles
  bagging/boosting/stacking, Cascade, Neutral Class, Rebalancing).
- **arena-mldp3** — entrenamiento + serving resiliente (Useful Overfitting,
  Checkpoints, Transfer Learning, Distribution Strategy, Hyperparameter Tuning,
  Stateless Serving, Batch Serving, Two-Phase Predictions, Keyed Predictions).
- **arena-mldp4** — reproducibilidad + IA responsable (Transform, Repeatable
  Splitting, Bridged Schema, Windowed Inference, Workflow Pipeline, Model
  Versioning, Continued Model Evaluation, Heuristic Benchmark, Explainable
  Predictions, Fairness Lens).

60 banco (15/unidad) + 2 examen (**f7-ex-48** ensembles/bias-varianza,
**f7-ex-49** repeatable splitting) = 62. 11 heurísticas nuevas
(usar-hashed-feature, usar-embeddings, reformular-regresion-clasificacion,
elegir-ensemble, usar-cascada-ml, transfer-learning-bottleneck,
tunear-hiperparametros, servir-modelo-resiliente,
separar-input-feature-transform, division-reproducible, lente-de-equidad);
reúsa manejar-desbalance-clases. Catálogo total **101** heurísticas. `sw.js`
**v42** (155 archivos; +4 lecciones `data/teoria/arena-mldp{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad
referencial OK (70 unidades en `fase-7`, 49 ítems de examen); `verificar-shell.py`
OK. Contenido anclado en el libro (patrones conceptuales de ML, §1.2).

**Siguiente** — orden §10 (ml-systems): **Site Reliability Engineering (Google)**
(libros[15]), luego Observability Engineering, Rules of ML, Hidden Technical
Debt, Interpretable ML, ISL. Próxima unidad: órdenes desde 71, `f7-ex-50`+,
VERSION v43+.

## Bitácora 2026-06-14 (Arena tanda 15) — Site Reliability Engineering (Google), 62 preguntas

Procesado `Site Reliability Engineering: How Google Runs Production Systems`
(Beyer, Jones, Petoff & Murphy, O'Reilly) — libros[15] del ledger, ruta
`ml-systems`, cuota 25. 15º libro en `completado`. Aporta el **canon SRE** que da
los fundamentos de fiabilidad bajo los SLOs/incidentes ya vistos en Reliable ML.
4 unidades (`fase-7`, órdenes 71-74):
- **arena-sre1** — riesgo, error budgets y SLOs (100% no es el objetivo,
  error budget = 1−SLO, caso Chubby, SLI/SLO/SLA, percentiles vs media).
- **arena-sre2** — toil (definición + cap <50%), cuatro señales doradas
  (latencia/tráfico/errores/saturación), black-box vs white-box, síntomas vs
  causas, propiedades de una buena página.
- **arena-sre3** — troubleshooting hipotético-deductivo (caballos no cebras,
  correlación≠causa), Incident Command System (roles command/ops/comms/planning,
  historia de Mary), postmortems sin culpa (blameless).
- **arena-sre4** — release engineering (autoservicio/alta velocidad/herméticos/
  cherry-pick), simplicidad (esencial vs accidental, líneas negativas, APIs
  mínimas), prevenir sobrecarga (load shedding, degradación elegante), fallos en
  cascada (GC death spiral, reintentos amplifican, capacidad N+2).

60 banco (15/unidad) + 2 examen (**f7-ex-50** error budget/SLO, **f7-ex-51**
fallos en cascada) = 62. 11 heurísticas nuevas (equilibrar-confiabilidad-
velocidad, definir-sli-slo-sla, eliminar-toil, cuatro-senales-doradas,
sintomas-vs-causas, troubleshooting-hipotetico-deductivo, postmortem-sin-culpa,
release-hermetico, preferir-simplicidad, prevenir-sobrecarga,
evitar-fallos-cascada); reúsa responder-incidente-ml. Catálogo total **112**
heurísticas. `sw.js` **v43** (159 archivos; +4 lecciones
`data/teoria/arena-sre{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (74 unidades en `fase-7`, 51 ítems de examen); `verificar-shell.py` OK.
Contenido anclado en el libro (conceptos SRE, §1.2).

**Siguiente** — orden §10 (ml-systems): **Observability Engineering**
(libros[16]), luego Rules of ML, Hidden Technical Debt, Interpretable ML, ISL.
Próxima unidad: órdenes desde 75, `f7-ex-52`+, VERSION v44+.

## Bitácora 2026-06-14 (Arena tanda 16) — Observability Engineering, 62 preguntas

Procesado `Observability Engineering: Achieving Production Excellence` (Majors,
Fong-Jones & Miranda, O'Reilly 2022) — libros[16] del ledger, ruta `ml-systems`,
cuota 25. 16º libro en `completado`. Aporta el enfoque **eventos-anchos + Core
Analysis Loop** de Honeycomb, valor NUEVO frente a SRE/Reliable ML. 4 unidades
organizadas por las 5 partes del libro (`fase-7`, órdenes 75-78):
- **arena-obs1** — ¿qué es observabilidad? (def. de Kálmán/teoría de control,
  prueba de fuego, monitoreo=known-unknowns vs observabilidad=unknown-unknowns,
  cardinalidad/dimensionalidad, eventos anchos, sistema vs software, crítica a
  los "3 pilares", explorabilidad).
- **arena-obs2** — pilares (evento estructurado ancho como bloque base, logs
  estructurados, trazas distribuidas + 5 campos del span + propagación W3C/B3,
  OpenTelemetry, depurar desde primeros principios, runbooks desperdiciados,
  Core Analysis Loop 4 pasos, BubbleUp/automatizar fuerza bruta, AIOps no es
  bala de plata).
- **arena-obs3** — SLOs (fatiga de alertas/normalización de la desviación, 2
  criterios de buena alerta, umbral estático=known-unknowns, desacoplar qué del
  por qué, user experience North Star, SLO/SLI tiempo vs eventos, error
  budget=1−SLO, ventana deslizante vs fija, 30 días, burn alert umbral vs
  predictiva, lookahead/baseline window, short-term vs context-aware).
- **arena-obs4** — escala (por qué TSDB explota cardinalidad, NoSQL ingress vs
  egress, row vs column vs híbrido, particionar por tiempo en segmentos,
  columnar+compresión, tiering/paralelismo+impaciencia/Kafka, rápido>perfecto,
  muestreo constante/dinámico/por clave/target rate, head vs tail, muestreo
  consistente, grabar sample rate, OMM 5 capacidades).

60 banco (15/unidad) + 2 examen (**f7-ex-52** error budget/burn alert con ejemplo
numérico 43.800u/SLO 99%, **f7-ex-53** estrategia de muestreo head/tail) = 62.
9 heurísticas nuevas (distinguir-observabilidad-monitoreo, usar-alta-cardinalidad,
instrumentar-eventos-anchos, trazas-distribuidas-spans, depurar-core-analysis-loop,
alertar-por-sintoma, error-budget-burn-alert, almacen-columnar-observabilidad,
muestreo-head-vs-tail); obs3 reúsa definir-sli-slo-sla. Catálogo total **121**
heurísticas. `sw.js` **v44** (+4 lecciones `data/teoria/arena-obs{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (78 unidades en `fase-7`, 53 ítems de examen); `verificar-shell.py` OK (163
archivos). Contenido anclado en el libro (§1.2).

**Siguiente** — orden §10 (ml-systems): **Rules of ML (Google)** (libros[17]),
luego Hidden Technical Debt, Interpretable ML, ISL. Después ruta `health-ai-rwe`
y Sectores D/C. Próxima unidad: órdenes desde 79, `f7-ex-54`+, VERSION v45+.

## Bitácora 2026-06-14 (Arena tanda 17) — Rules of ML (Zinkevich, Google), 62 preguntas

Procesado `Rules of Machine Learning: Best Practices for ML Engineering`
(Martin Zinkevich, Google) — libros[17] del ledger, ruta `ml-systems`, cuota 25.
17º libro en `completado`. Aporta las **43 reglas** de best practices de
ingeniería de ML ('haz ML como el ingeniero que eres, no como el experto en ML
que no eres'), valor NUEVO frente a Huyen/Reliable ML/SRE/Observability. 4
unidades por las fases del documento (`fase-7`, órdenes 79-82):
- **arena-rom1** — antes del ML + primer pipeline (R1-11): lanzar sin
  ML/heurística simple, métricas primero, ML>heurística compleja; modelo simple
  + infra correcta y testeada aparte, datos descartados al copiar pipelines,
  heurísticas→features; monitoreo (frescura, detectar antes de exportar, fallos
  silenciosos, dueños de feature columns).
- **arena-rom2** — objetivo + feature engineering (R12-22): objetivo simple,
  observable y atribuible (proxy del verdadero), modelo interpretable/calibrado,
  policy layer spam vs calidad; features observadas>aprendidas, específicas,
  discretización/cruces, pesos∝datos, limpiar features no usadas.
- **arena-rom3** — análisis humano + training-serving skew (R23-37): no eres
  usuario típico, medir delta, utilitario>predictivo, features desde errores,
  mide-primero-optimiza-después; skew (logear features en serving, reusar
  código, importance weight, testear en datos posteriores, feedback loops
  posicionales, medir skew en 3 componentes).
- **arena-rom4** — Fase III (R38-43): objetivos desalineados, decisiones de
  lanzamiento multi-métrica (proxy de metas largas, ejemplo DAU vs revenue),
  ensembles simples y monotónicos, fuentes nuevas ante plateau,
  popularidad vs diversidad/personalización, amigos transfieren e intereses no.

60 banco (15/unidad) + 2 examen (**f7-ex-54** training-serving skew, **f7-ex-55**
decisión de lanzamiento multi-métrica) = 62. 7 heurísticas nuevas
(lanzar-sin-ml-primero, pipeline-simple-infra-correcta, objetivo-simple-observable,
features-observadas-vs-aprendidas, analizar-modelo-como-humano,
decidir-lanzamiento-multimetrica, mantener-ensembles-simples); rom3 reúsa
vigilar-training-serving-skew. Catálogo total **128** heurísticas. `sw.js` **v45**
(+4 lecciones `data/teoria/arena-rom{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (82 unidades en `fase-7`, 55 ítems de examen); `verificar-shell.py` OK (167
archivos). Contenido anclado en el documento (§1.2).

**Siguiente** — orden §10 (ml-systems): **Hidden Technical Debt in ML Systems
(NIPS 2015)** (libros[18]), luego Interpretable ML (Molnar) e ISL. Después ruta
`health-ai-rwe` y Sectores D/C. Próxima unidad: órdenes desde 83, `f7-ex-56`+,
VERSION v46+.

## Bitácora 2026-06-14 (Arena tanda 18) — Hidden Technical Debt in ML (Sculley et al.), 62 preguntas

Procesado `Hidden Technical Debt in Machine Learning Systems` (Sculley, Holt,
Golovin et al., NIPS 2015, Google) — libros[18] del ledger, ruta `ml-systems`,
cuota 25. 18º libro en `completado`. Aporta el marco canónico de **deuda técnica
a nivel de sistema** del ML, valor NUEVO frente a best practices/SRE/observability.
4 unidades por las secciones del paper (`fase-7`, órdenes 83-86):
- **arena-htd1** — fundamentos + erosión de fronteras (§1-2): deuda técnica
  (Cunningham), capacidad especial del ML (nivel sistema, no código), principio
  **CACE**/entanglement, **correction cascades** (deadlock de mejora),
  **undeclared consumers** (visibility debt); mitigaciones (ensembles aislados,
  detección de cambios).
- **arena-htd2** — dependencias de datos + feedback loops (§3-4): data deps cost
  more than code deps, **inestables**→copia versionada, **infrautilizadas**
  (legacy/bundled/ε/correlated)→leave-one-feature-out, análisis estático/feature
  management, feedback loops **directos** vs **ocultos**.
- **arena-htd3** — anti-patrones de sistema + config (§5-6): plumbing/Figura 1,
  **glue code**→APIs comunes, **pipeline jungles**→clean-slate, **dead
  experimental codepaths** (Knight Capital $465M), abstraction debt (Map-Reduce
  malo para ML iterativo), smells (plain-data-type/multi-language/prototype),
  **configuration debt** + 6 principios.
- **arena-htd4** — mundo externo + otras deudas + medición (§7-9): **fixed
  thresholds**→aprender en heldout, monitoreo en vivo (**prediction bias**,
  action limits, up-stream SLAs), data testing/reproducibility/process
  management/**cultural debt**, las **5 preguntas**, rápido≠poca deuda,
  pagar=cultura.

60 banco (15/unidad) + 2 examen (**f7-ex-56** CACE/erosión de fronteras,
**f7-ex-57** medir deuda/pipeline jungle/dead codepaths) = 62. 8 heurísticas
nuevas (cace-entanglement, evitar-erosion-fronteras-ml,
gestionar-dependencias-datos, romper-feedback-loops,
evitar-glue-code-pipeline-jungles, deuda-configuracion-ml,
monitorear-cambios-mundo-externo, medir-deuda-tecnica-ml). Catálogo total **136**
heurísticas. `sw.js` **v46** (+4 lecciones `data/teoria/arena-htd{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (86 unidades en `fase-7`, 57 ítems de examen); `verificar-shell.py` OK (171
archivos). Contenido anclado en el paper (§1.2).

**Siguiente** — orden §10 (ml-systems): **Interpretable Machine Learning
(Molnar)** (libros[19]), luego ISL. Después ruta `health-ai-rwe` y Sectores D/C.
Próxima unidad: órdenes desde 87, `f7-ex-58`+, VERSION v47+.

## Bitácora 2026-06-14 (Arena tanda 19) — Interpretable Machine Learning (Molnar), 62 preguntas

Procesado `Interpretable Machine Learning` (Christoph Molnar) — libros[19] del
ledger, ruta `ml-systems`, cuota 25. 19º libro en `completado`. Aporta el **marco
completo de interpretabilidad** (taxonomía + modelos intrínsecos + métodos
agnósticos + Shapley/ejemplos), valor NUEVO frente al MLOps/observabilidad/deuda
técnica ya vistos. 4 unidades por las 4 partes del libro (`fase-7`, órdenes 87-90):
- **arena-iml1** — conceptos y taxonomía: def. de interpretabilidad, cuándo SÍ/NO
  se necesita, los **4 ejes** (intrínseca/post-hoc · específica/**agnóstica** ·
  **global/local** · tipo de resultado), alcance, explicaciones **contrastivas/
  selectivas/sociales** (ciencias sociales), propiedades de métodos y de
  explicaciones (**fidelity/stability**), niveles application/human/functionally-grounded.
- **arena-iml2** — modelos interpretables: lineal (peso ceteris paribus,
  **t-statistic**, R² ajustado, multicolinealidad, weight/effect plots); logística
  (**odds ratio** exp(β)); GLM (link+distribución); **GAM** (splines aditivos);
  árbol (camino+impureza+inestabilidad); reglas IF-THEN (soporte/accuracy/OneR);
  **RuleFit** (reglas de árboles + LASSO).
- **arena-iml3** — métodos agnósticos: **PDP** (efecto marginal + supuesto de
  independencia + oculta heterogeneidad), **ICE** (una línea/instancia = interacción,
  c-ICE), **ALE** (ventanas + diferencias locales sobre datos reales + acumular,
  insesgado bajo correlación vs M-plots), **H-statistic** de Friedman (H²∈[0,1]),
  **importancia por permutación** (ΔError en TEST, features correlacionadas),
  **surrogate global** (target=ŷ, fidelity R²).
- **arena-iml4** — LIME (4 pasos, texto/superpíxeles, inestable), **valores de
  Shapley** (contribución marginal media + 4 axiomas, **eficiencia** = suman ŷ−ŷ̄),
  **SHAP** (KernelSHAP/TreeSHAP, importancia global consistente), **contrafactuales**
  (mínimo cambio que voltea, Wachter, accionable), adversariales, **prototipos/
  críticas** (MMD-critic), **instancias influyentes** (DFBETA/influence functions),
  **anchors**.

60 banco (15/unidad) + 2 examen (**f7-ex-58** PDP vs ALE bajo correlación,
**f7-ex-59** Shapley/SHAP vs permutación/LIME + contrafactual) = 62. 14 heurísticas
nuevas (interpretabilidad-cuando-y-taxonomia, explicacion-contrastiva-selectiva,
preferir-modelo-interpretable, interpretar-odds-ratio, usar-gam-no-linealidad,
pdp-ice-efectos, ale-features-correlacionadas, interaccion-h-statistic,
importancia-por-permutacion, surrogate-global, lime-sustituto-local,
valores-shapley-shap, contrafactual-explicacion, explicaciones-por-ejemplos);
reúsa interpretar-coeficientes-regresion (lineal) y lente-de-equidad (iml4).
Catálogo total **150** heurísticas. `sw.js` **v47** (+4 lecciones
`data/teoria/arena-iml{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (90 unidades en `fase-7`, 59 ítems de examen); `verificar-shell.py` OK (175
archivos). Contenido anclado en el libro (§1.2).

**Siguiente** — orden §10 (ml-systems): **Introduction to Statistical Learning
(ISLR)** (libros[20]). Después ruta `health-ai-rwe` (What If, Survival Analysis,
OHDSI, Book of Why, Mixtape) y Sectores D (conductual) / C (problems.json).
Próxima unidad: órdenes desde 91, `f7-ex-60`+, VERSION v48+.

## Bitácora 2026-06-14 (Arena tanda 20) — Introduction to Statistical Learning (ISLR), 62 preguntas

Procesado `An Introduction to Statistical Learning` (James, Witten, Hastie &
Tibshirani, 1ª ed.) — libros[20] del ledger, ruta `ml-systems`, cuota 25. 20º
libro en `completado` y **último de la ruta ml-systems**. Aporta los
**fundamentos estadísticos** (sesgo-varianza canónico, CV, regularización,
métodos) que sostienen todo lo visto en ml-systems/ciencia-datos. 4 unidades por
bloques del libro (`fase-7`, órdenes 91-94):
- **arena-isl1** — el marco (Cap. 2): Y=f(X)+ε, **predicción vs inferencia**,
  error **reducible/irreducible**, **paramétrico vs no paramétrico** + trade-off
  flexibilidad-interpretabilidad, supervisado/no sup., regresión/clasif., MSE
  train vs test, **descomposición sesgo-varianza**, **clasificador de Bayes**/error
  de Bayes, **KNN** y el papel de K.
- **arena-isl2** — regresión y clasificación (Cap. 3-4): mínimos cuadrados, SE/IC,
  **t** y p-valor, RSE/R², efecto parcial vs marginal (confounding), **F-statistic**
  global vs t múltiples, dummies, **interacción**+principio jerárquico, problemas
  potenciales, **colinealidad/VIF**; logística/odds, **LDA** (cov común→lineal),
  **QDA** (cov por clase→cuadrática), naive Bayes, generativo vs discriminativo,
  matriz de confusión/sensibilidad/especificidad/**ROC-AUC**.
- **arena-isl3** — remuestreo + selección + regularización (Cap. 5-6): validation
  set, **LOOCV vs k-fold** y su propio sesgo-varianza, regla de un SE, **bootstrap**;
  best/forward/backward subset, **Cp/AIC/BIC/adjR²/CV**, **ridge (L2) vs lasso (L1)**
  geometría/selección, elegir λ, estandarizar, **PCR vs PLS**, **maldición de la
  dimensionalidad** (p≳n).
- **arena-isl4** — no linealidad + árboles + SVM + no sup. (Cap. 7-10): polinomios/
  escalón/funciones base, **splines** (nudos, natural, suavizante λ), **GAM**;
  árboles Gini/entropía, **bagging**, **random forest** (decorrelación m=√p, **OOB**,
  importancia), **boosting** (B/d/λ); **SVM** (margen máximo/support vectors, soft
  margin **C**, **kernel trick** RBF, one-vs-one/all); **PCA**/PVE, **K-means** (fija
  K) vs **jerárquico** (dendrograma/linkage).

60 banco (15/unidad) + 2 examen (**f7-ex-60** LOOCV vs k-fold / CV para selección,
**f7-ex-61** ridge vs lasso geometría/cuándo/λ) = 62. 15 heurísticas nuevas
(marco-aprendizaje-estadistico, parametrico-vs-no-parametrico, clasificador-bayes-knn,
f-statistic-significancia-global, detectar-colinealidad-vif, lda-qda-vs-logistica,
elegir-validacion-cruzada, seleccionar-modelo-subset, reduccion-dimension-pcr-pls,
maldicion-dimensionalidad, splines-y-gam, random-forest-decorrelacion,
boosting-secuencial, svm-margen-kernel, clustering-kmeans-jerarquico); reúsa
bias-varianza, interpretar-coeficientes-regresion, metrica-clasificacion,
bootstrap-resampling, regularizacion, elegir-ensemble. Catálogo total **165**
heurísticas. `sw.js` **v48** (+4 lecciones `data/teoria/arena-isl{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (94 unidades en `fase-7`, 61 ítems de examen); `verificar-shell.py` OK (179
archivos). Contenido anclado en el libro (§1.2).

**Siguiente** — la ruta `ml-systems` queda COMPLETA. Orden §10 pasa a la ruta
**`health-ai-rwe`**: **What If (Hernán & Robins)** (libros[21]), luego Survival
Analysis, The Book of OHDSI, The Book of Why (epub), Causal Inference: The Mixtape.
Después Sectores D (conductual) y C (problems.json). Próxima unidad: convención de
id de ruta `health-ai-rwe` continúa en `arena-h3,h4…` (ya existen arena-h1,h2);
órdenes desde 95, `f7-ex-62`+, VERSION v49+.

## Bitácora 2026-06-14 (Arena tanda 21) — Causal Inference: What If (Hernán & Robins), 62 preguntas

Procesado `Causal Inference: What If` (Miguel Hernán & James Robins, ed. 2025, 23
caps. en 3 partes) — libros[21] del ledger, ruta `health-ai-rwe`, cuota 25. Primer
libro de la ruta **health-ai-rwe** vía libro dedicado. **DIFERENCIADO** de las
unidades ligeras preexistentes `arena-h1` (DAGs básicos confundidor/mediador/
collider, 4q) y `arena-h2` (target trial/immortal time, 4q): estas 4 unidades dan
la BREADTH+DEPTH del libro sin duplicar. 4 unidades (`fase-7`, órdenes 95-98):
- **arena-h3** — fundamentos sin modelos (Cap. 1-5): resultados potenciales
  (efecto individual inobservable vs **promedio**), **asociación≠causación**,
  aleatorización→**intercambiabilidad**, las **3 condiciones de identificación**
  (intercambiabilidad|L + positividad + consistencia; solo positividad verificable),
  medidas de efecto marginales, **modificación de efecto** (depende de escala) vs
  **interacción**, causal=missing data.
- **arena-h4** — estructura de los sesgos (Cap. 6-10): confundimiento + **criterio
  backdoor**, **d-separación** (condicionar cierra cadenas/bifurcaciones, ABRE
  colliders), no ajustar mediador (sesga el total) ni collider, **sesgo de
  selección/censura** informativa→IPCW, **sesgo de medición** (no diferencial
  atenúa vs diferencial), confundidor mal medido=residual, identificación vs
  estimación, **M-bias/Z-bias**, SWIGs.
- **arena-h5** — modelos (Cap. 11-16,18): por qué modelar, **IP weighting + MSM +
  pesos estabilizados**, **estandarización/g-fórmula** (cara complementaria),
  **propensity score** (balancing score), **doble robustez** (consistente si UNO de
  los dos modelos; AIPW/TMLE + ML + cross-fitting), **variable instrumental** (3
  condiciones + monotonicidad→**LATE** en compliers; instrumentos débiles).
- **arena-h6** — longitudinal + supervivencia + target trial (Cap. 17,19-22):
  **hazard ratio** problemático (selección incorporada)→riesgo/supervivencia a
  tiempo fijo, censura=tratamiento tiempo-variable→**IPCW**, intercambiabilidad
  **secuencial**, **feedback tratamiento-confundidor** (L confundidor+mediador →
  métodos tradicionales fallan y no se arreglan → **g-métodos**), **ITT vs
  per-protocol** (naïve sesgado), **emular target trial** sostenido (alinear t=0 →
  immortal time; new-user → usuario prevalente; comparador activo; per-protocol con
  g-métodos), caballo de batalla de la **RWE**.

60 banco (15/unidad) + 2 examen (**f7-ex-62** confundimiento/backdoor/mediador/
collider/selección, **f7-ex-63** las 3 condiciones de identificación +
estandarización vs IP weighting) = 62. 16 heurísticas nuevas
(definir-efecto-causal-contrafactual, condiciones-identificacion-causal,
exchangeability-aleatorizacion, modificacion-efecto-vs-interaccion,
confundimiento-backdoor, sesgo-de-seleccion-censura,
sesgo-de-medicion-misclasificacion, ip-weighting-msm, estandarizacion-g-formula,
propensity-score, doble-robustez, variable-instrumental,
analisis-supervivencia-hazard-vs-riesgo, confounding-tiempo-variable-gmetodos,
itt-vs-per-protocol-estimando, emular-target-trial-sostenido). Catálogo total
**181** heurísticas. `sw.js` **v49** (+4 lecciones `data/teoria/arena-h{3..6}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (98 unidades en `fase-7`, 63 ítems de examen); `verificar-shell.py` OK (183
archivos). Contenido anclado en el libro (§1.2; TOC verificado: ed. 2025, 23 caps.).

**Siguiente** — orden §10 (health-ai-rwe): **Survival Analysis (3rd ed.)**
(libros[22]), luego The Book of OHDSI, The Book of Why (epub — saltar si Read no
abre), Causal Inference: The Mixtape (.txt en Biblioteca/). Después Sectores D
(conductual) y C (problems.json). Próxima unidad: `arena-h7,h8…`; órdenes desde 99,
`f7-ex-64`+, VERSION v50+.

## Bitácora 2026-06-14 (Arena tanda 22) — Survival Analysis (Kleinbaum & Klein, 3rd ed.), 62 preguntas

Procesado `Survival Analysis: A Self-Learning Text` (David Kleinbaum & Mitchel
Klein, 3ª ed., 2012, 9 caps.) — libros[22] del ledger, ruta `health-ai-rwe`, cuota
25. Es la **mecánica biostadística** de supervivencia, valor NUEVO **distinto** de
`arena-h6` (supervivencia CAUSAL / g-métodos de Hernán). 4 unidades por bloques del
libro (`fase-7`, órdenes 99-102):
- **arena-h7** — fundamentos + KM + log-rank (Cap. 1-2): **S(t)/h(t)/H(t)** y
  S=exp(−∫h), **censura** (derecha/izq/intervalo + no informativa), **Kaplan-Meier**
  product-limit (escalones en eventos, mediana), **log-rank** (H0 curvas iguales,
  observado−esperado, óptimo bajo PH; Wilcoxon/Tarone-Ware/Peto), risk set.
- **arena-h8** — Cox PH + supuesto PH (Cap. 3-5): **h(t,X)=h₀(t)exp(βX)**
  semiparamétrico, **HR=exp(β)**, **verosimilitud parcial**, supuesto **PH** (HR
  constante), evaluar con **log-log / Schoenfeld / variable tiempo-dependiente**,
  **Cox estratificado** (h₀ por estrato, β compartidos, no-interacción vs
  interacción por LR), curvas ajustadas.
- **arena-h9** — Cox extendido + paramétricos/AFT (Cap. 6-7): covariables
  **tiempo-dependientes** h₀(t)exp[βX+δX(t)] (HR depende de t; cuidado immortal
  time), paramétricos **exponencial/Weibull/log-logística** por forma del hazard,
  **AFT** (factor de aceleración estira/encoge el tiempo), **Weibull única PH+AFT**,
  HR<1↔factor>1, extrapolación.
- **arena-h10** — eventos recurrentes + riesgos competitivos (Cap. 8-9): recurrentes
  (correlación intra-sujeto → **varianza robusta**; Andersen-Gill/PWP/WLW);
  **riesgos competitivos** (hazard **específico de causa**=censura competidores=
  etiología; **1−KM SOBRESTIMA**; **CIF** correcta; **Fine-Gray** subdistribution
  hazard = regresión sobre la CIF = predicción/riesgo; prueba de **Gray**; censura
  vs riesgo competitivo).

60 banco (15/unidad) + 2 examen (**f7-ex-64** evaluar supuesto PH y qué hacer si se
viola, **f7-ex-65** riesgos competitivos 1−KM/CIF/cause-specific vs Fine-Gray) = 62.
11 heurísticas nuevas (funcion-supervivencia-hazard, manejar-censura-supervivencia,
estimador-kaplan-meier, prueba-log-rank, modelo-cox-ph, evaluar-supuesto-ph,
cox-estratificado, cox-extendido-tiempo-dependiente, modelo-parametrico-aft,
eventos-recurrentes-supervivencia, riesgos-competitivos-cif). Catálogo total **192**
heurísticas. `sw.js` **v50** (+4 lecciones `data/teoria/arena-h{7..10}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (102 unidades en `fase-7`, 65 ítems de examen); `verificar-shell.py` OK (187
archivos). Contenido anclado en el libro (§1.2; TOC verificado: 3ª ed., 9 caps.).

**Siguiente** — orden §10 (health-ai-rwe): **The Book of OHDSI** (libros[23]),
luego The Book of Why (epub — saltar si Read no abre), Causal Inference: The Mixtape
(.txt en Biblioteca/). Después Sectores D (conductual) y C (problems.json). Próxima
unidad: `arena-h11,h12…`; órdenes desde 103, `f7-ex-66`+, VERSION v51+.

## Bitácora 2026-06-14 (Arena tanda 23) — The Book of OHDSI, 62 preguntas

Procesado `The Book of OHDSI` (comunidad OHDSI, 5 partes, 20 caps., CC0) —
libros[23] del ledger, ruta `health-ai-rwe`, cuota 25. Es la **capa operacional /
de estandarización** de la RWE, valor NUEVO distinto de What If (teoría causal) y
Survival (métodos): el ecosistema **OMOP/OHDSI a escala**. 4 unidades por las
partes del libro (`fase-7`, órdenes 103-106):
- **arena-h11** — comunidad + datos observacionales + **OMOP CDM** (Part I + ch8):
  ciencia abierta, claims vs EHR, 3 casos de uso (caracterización/estimación/
  predicción), CDM persona-céntrico (PERSON/OBSERVATION_PERIOD/eventos/era),
  sintáctica vs semántica, ATLAS/HADES/EUNOMIA.
- **arena-h12** — **vocabularios + ETL + calidad de datos** (ch3-6,15): concept_id
  estándar (SNOMED/RxNorm/LOINC) vs fuente (ICD/NDC) con 'Maps to', dominios,
  **CONCEPT_ANCESTOR**/concept sets, ETL (WhiteRabbit/Rabbit-in-a-Hat/Usagi),
  **marco de Kahn** (conformance/completeness/plausibility × verification/validation),
  ACHILLES + **DataQualityDashboard**.
- **arena-h13** — **analítica estandarizada** (ch8-13): cohortes (entry/inclusión/
  exit + concept sets, rule-based vs probabilístico), validación de **fenotipos**
  (sens/espec/PPV), **caracterización** (pathways/incidencia), **estimación**
  (cohort method + PS a gran escala vs autocontrolados SCCS/case-crossover),
  **predicción PLP** (target+outcome+time-at-risk, AUC+calibración).
- **arena-h14** — **calidad de evidencia + validez de método + red** (ch14,16-20):
  4 validez (datos/clínica/software/método), **PheValuator**, **controles negativos**
  (RR≈1) + positivos sintéticos, **calibración empírica** de p/IC (ensancha),
  diagnósticos (balance/equipoise/MDRR), Methods Benchmark, **estudios en red**
  (solo agregados salen), LEGEND.

60 banco (15/unidad) + 2 examen (**f7-ex-66** validez de método: controles negativos
+ calibración empírica, **f7-ex-67** definir cohorte/fenotipo new-user + validación
+ portabilidad por conceptos estándar) = 62. 13 heurísticas nuevas
(que-es-ohdsi-open-science, omop-common-data-model, vocabularios-estandarizados-omop,
proceso-etl-cdm, calidad-datos-kahn, definir-cohorte-fenotipo, caracterizacion-ohdsi,
estimacion-nivel-poblacion-ohdsi, prediccion-nivel-paciente-plp,
validez-clinica-fenotipo, validez-de-metodo-controles-negativos,
calibracion-empirica-pvalores, estudios-en-red-ohdsi). Catálogo total **205**
heurísticas. `sw.js` **v51** (+4 lecciones `data/teoria/arena-h{11..14}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (106 unidades en `fase-7`, 67 ítems de examen); `verificar-shell.py` OK (191
archivos). Contenido anclado en el libro (§1.2; TOC verificado: 5 partes, 20 caps.).

**Siguiente** — orden §10 (health-ai-rwe): **The Book of Why** (Pearl & Mackenzie,
libros[24], **EPUB** — saltar y anotar si Read no lo abre), luego **Causal
Inference: The Mixtape** (Cunningham, libros[25], .txt en `Biblioteca/`). Después
Sectores D (conductual) y C (problems.json). Próxima unidad: `arena-h15,h16…`;
órdenes desde 107, `f7-ex-68`+, VERSION v52+.

## Bitácora 2026-06-14 (Arena tanda 24) — The Book of Why (Pearl & Mackenzie), 62 preguntas

Procesado `The Book of Why` (Judea Pearl & Dana Mackenzie, 10 caps.) — libros[24],
ruta `health-ai-rwe`, cuota 25. **El EPUB SÍ es legible**: se extrajo con
`unzip -p "<epub>" OEBPS/Text/chapterNNN.xhtml` + strip de HTML, y se verificó el
texto (escalera cap.1, front-door/do-calculus cap.7). Enfoque **gráfico/do-calculus**
de Pearl, **DIFERENCIADO** de `arena-h3/h4/h5` (What If, potential-outcomes-first):
la escalera, el do-operator, el front-door, la taxonomía de junciones, las paradojas
y la mediación. 4 unidades (`fase-7`, órdenes 107-110):
- **arena-h15** — **escalera de la causalidad** + génesis (cap.1-2): 3 peldaños
  (ver P(Y|X) / hacer P(Y|do(X)) / imaginar contrafactual), ML en peldaño 1,
  mini-Turing test, "mind over data", Galton/Pearson vs **Sewall Wright** (path
  diagrams), aleatorización = do.
- **arena-h16** — **diagramas, junciones y paradojas** (cap.3,4,6): DAG (flechas
  ausentes = supuestos fuertes), redes bayesianas vs causales, **3 junciones**
  (cadena/mediador, fork/confundidor, collider/efecto común; condicionar cierra
  cadena-fork y **abre** collider), **Simpson** resuelto por estructura, **Berkson**,
  **Monty Hall** como collider.
- **arena-h17** — **do-operator, back-door, front-door, do-calculus** (cap.4,7):
  P(Y|X)≠P(Y|do(X)), do() borra flechas hacia X, identificación, back-door/
  estandarización, **front-door** (mediador que capta todo el efecto → identifica
  con confundidor no medido; tabaco→alquitrán→cáncer), IV/Dr. Snow, **do-calculus**
  (3 reglas, completo).
- **arena-h18** — **contrafactuales y mediación** (cap.8-9): peldaño 3, **SCM** con
  errores U, **abducción→acción→predicción**, equivalencia con los **potential
  outcomes** Y_x, mediación (NDE/NIE; Baron-Kenny falla con interacción), **PN**
  (necesidad/'but-for'/legal) vs **PS** (suficiencia/prevención).

60 banco (15/unidad) + 2 examen (**f7-ex-68** escalera / ML en peldaño 1 /
predecir≠causar, **f7-ex-69** front-door con confundidor no medido) = 62. 11
heurísticas nuevas (escalera-de-la-causalidad, causalidad-requiere-modelo,
diagramas-causales-junciones, paradoja-simpson-causal, sesgo-collider-berkson,
do-operator-intervencion, criterio-puerta-delantera, do-calculus,
contrafactual-modelo-estructural, analisis-mediacion-efectos,
causa-necesaria-suficiente); h17 reúsa confundimiento-backdoor. Catálogo total
**216** heurísticas. `sw.js` **v52** (+4 lecciones `data/teoria/arena-h{15..18}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (110 unidades en `fase-7`, 69 ítems de examen); `verificar-shell.py` OK (195
archivos). Contenido anclado en el libro (§1.2; EPUB extraído y verificado).

**Siguiente** — orden §10 (health-ai-rwe, ÚLTIMO de la ruta): **Causal Inference:
The Mixtape** (Scott Cunningham, libros[25], **.txt en `Biblioteca/`**). Después la
ruta health-ai-rwe queda completa → Sectores **D** (conductual, STAR) y **C**
(problems.json + fase-0). Próxima unidad: `arena-h19,h20…`; órdenes desde 111,
`f7-ex-70`+, VERSION v53+.

## Bitácora 2026-06-14 (Arena tanda 25) — Causal Inference: The Mixtape (Cunningham), 62 preguntas

Procesado `Causal Inference: The Mixtape` (Scott Cunningham) — libros[25], ruta
`health-ai-rwe`, cuota 25. **ÚLTIMO libro de la ruta health-ai-rwe**, que queda
**COMPLETA (22 unidades, arena-h1..h22)**. NOTA: el `.txt` de `Biblioteca/` está
**cifrado** (César +1: "Bnoxqhfgs"→"Copyright"), ilegible; se usó el **PDF**
`Biblioteca/Causal Inference_ The Mixtape - Cunningham-Cuasal-Inference-the-Mixtape.pdf`
(TOC verificado). Toolkit **cuasi-experimental econométrico**, valor NUEVO frente a
What If/Book of Why/OHDSI/Survival. 4 unidades (`fase-7`, órdenes 111-114):
- **arena-h19** — **resultados potenciales y sesgo de selección**: Y¹/Y⁰ +
  switching equation, **ATE/ATT/ATU**, **SUTVA**, descomposición diferencia naïve =
  ATE + sesgo de selección + sesgo heterogéneo, aleatorización, endógeno vs exógeno.
- **arena-h20** — **matching, subclasificación, PS**: **CIA** (selección en
  observables (Y¹,Y⁰)⊥D|X, no testeable), maldición de dimensionalidad, propensity
  score/IPW, soporte común, balance, matching no extrapola vs regresión, Lalonde.
- **arena-h21** — **IV/2SLS + RDD**: 2SLS (relevancia/exclusión/independencia, LATE,
  instrumentos débiles F>10, forma reducida); **RDD** sharp vs fuzzy(IV), McCrary,
  bandwidth/polinomio local, Card Medicare@65, identifica **sin CIA** (efecto local).
- **arena-h22** — **panel/FE + DiD + control sintético**: efectos fijos (within,
  exogeneidad estricta), **DiD** (doble diferencia = ATT bajo **tendencias
  paralelas**, event study/placebos, **Goodman-Bacon** con staggered), **control
  sintético** (gemelo ponderado del donor pool, inferencia por permutación, Abadie).

60 banco (15/unidad) + 2 examen (**f7-ex-70** DiD/tendencias paralelas/Goodman-Bacon,
**f7-ex-71** RDD sharp vs fuzzy/McCrary/sin CIA) = 62. 10 heurísticas nuevas
(rubin-ate-att-atu-sutva, descomponer-comparacion-naive, matching-subclasificacion,
supuesto-seleccion-en-observables-cia, instrumentos-debiles-2sls,
regresion-discontinua-rdd, diferencias-en-diferencias, tendencias-paralelas-placebo,
efectos-fijos-panel, control-sintetico); reúsa propensity-score y
variable-instrumental. Catálogo total **226** heurísticas. `sw.js` **v53** (+4
lecciones `data/teoria/arena-h{19..22}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (114 unidades en `fase-7`, 71 ítems de examen); `verificar-shell.py` OK (199
archivos). Contenido anclado en el PDF (§1.2; TOC verificado).

**Siguiente** — la ruta `health-ai-rwe` queda **COMPLETA**. Orden §10 pasa al
**Sector D** (ruta `conductual`/STAR): **Build a Career in Data Science** (Robinson
& Nolis, libros[26]) + capítulos conductuales de Cracking the Coding/System Design.
**Cablear la ruta `conductual` (§6)** si no está (chip ya existe en `js/study.js`;
revisar CSS `.ruta-conductual`). Ver §SECTOR D del PROMPT-MAESTRO (esquema STAR:
`solucion`=andamiaje STAR + señales, NUNCA historia inventada). Después Sector C
(problems.json + fase-0). Próxima unidad: ids `arena-c1,c2…`; órdenes desde 115,
`f7-ex-72`+, VERSION v54+.

## Bitácora 2026-06-14 (Arena tanda 26) — SECTOR D conductual/STAR (Build a Career in DS), 62 preguntas

Procesado el **SECTOR D (conductual/STAR)** con `Build a Career in Data Science`
(Robinson & Nolis) — libros[26], ruta `conductual`, cuota 40 (superada con 60). La
ruta `conductual` **ya estaba cableada** (chip en `js/study.js` y CSS
`.ruta-conductual` de una sesión previa) → **sin cambios de código salvo sw.js**.
**REGLA §SECTOR D respetada:** `tipo:"conductual"`; `solucion` = andamiaje STAR para
ESA pregunta + señales de respuesta fuerte; `explicacion` = errores comunes +
esqueleto STAR genérico; **JAMÁS se inventó una historia personal del usuario**. 4
unidades (`fase-7`, órdenes 115-118):
- **arena-c1** — conflicto, colaboración y comunicación (conflicto sin culpar,
  desacuerdo con manager/'disagree and commit', explicar a no técnicos, influir sin
  autoridad, dar/recibir feedback, malas noticias, mentoría, remoto).
- **arena-c2** — fracaso, errores, ambigüedad y feedback (proyecto que fracasó,
  mayor error, crítica dura, ambigüedad, plazo incumplido, análisis equivocado,
  estrés, coste hundido, "no sé").
- **arena-c3** — liderazgo, iniciativa, impacto y priorización (liderar, iniciativa
  no pedida, priorizar con criterio, decisión con info incompleta, decisión
  impopular, mejora de proceso, mayor logro, calidad vs plazo, delegar).
- **arena-c4** — DS aplicada, stakeholders y carrera (proyecto end-to-end con
  impacto de **negocio**, resultado negativo, modelo que falló en producción, datos
  sucios, stakeholder escéptico, definir métrica, ética/privacidad, "por qué este
  puesto", "cuéntame de ti", Fermi, aprendizaje continuo, metas).

60 banco (15/unidad) + 2 examen (**f7-ex-72** conflicto, **f7-ex-73** fracaso; ambos
`heuristica: narrativa-star`, `pistas[5]` que guían S→T→A→R, `metadata.ruta:
conductual`) = 62. 5 heurísticas nuevas (**narrativa-star**, responder-conflicto-star,
responder-fracaso-star, responder-liderazgo-impacto-star, comunicar-resultado-ds-star).
Catálogo total **231** heurísticas. `sw.js` **v54** (+4 lecciones
`data/teoria/arena-c{1..4}.md`).

Verificación §9 en verde: JSON válido; sin ids duplicados; integridad referencial
OK (118 unidades en `fase-7`, 73 ítems de examen); `verificar-shell.py` OK (203
archivos). Contenido anclado en el libro (§1.2; las conductuales no se 'verifican':
su solución es el andamiaje STAR).

**Siguiente** — el **Sector A (todas las rutas de entrevista) y el Sector D quedan
COMPLETOS**. Orden §10 pasa al **Sector C**: `data/problems.json` (problemas nuevos,
ids numéricos **101+**, sin huecos; campo `estrategia` ∈ {inversion, optimizacion,
invariantes, patrones}, `dificultad` 1-5, `hints[5]` socráticos, solución
**verificada con Python** para mates) **y** bloque `fase-0`. Fuente: carpeta
`Arena/Problem solving y olimpiadas/` (Engel, Zeitz, Pólya, Putnam, Bóna, Kevin
Houston, serie AoPS). OJO: esquema distinto (§4.1, no fase-7). VERSION v55+.

## Bitácora 2026-06-14 (Arena tanda 27) — SECTOR C: Engel, *Problem-Solving Strategies*, 44 problemas

Arranca el **SECTOR C (entrenamiento)** con `Problem-Solving Strategies` (Arthur
Engel) — libros[27] del ledger, ruta `entrenamiento`, cuota 40 (superada con **44**).
Destino: **`data/problems.json`** (esquema §4.1), ids **101-144** sin huecos. **A Mind
for Numbers** (libros[27 previo, soporte-teórico, cuota 0) se deja como `pendiente`/no
genera problemas de Arena; se saltó por prioridad §10 hacia el Sector C.

Distribución por `estrategia` (las 4 ÚNICAS válidas), tomada de los capítulos de Engel
que mejor encarnan cada heurística:
- **invariantes** (10): borrar→|a−b| (E2), restas sobre 1..4n−1, seis sectores (E3),
  ±1 cíclico 4|n (E7), raíz digital mod 9, tres enteros por paridad (P21), cuádruple
  que diverge (E5, monovariante), pentágono IMO 1986 que se detiene (E9), romper
  chocolate (nm−1), pizarrón a+b+ab ((n+1)!−1).
- **optimizacion** (12, cap. 3 Extremal): parlamento ≤3 enemigos (E4/E14), enanos y
  leche 6/7..0 (E13), √2 irracional por mínimo elemento (E17), autos en pista circular
  (P15), seis puntos M/m≥√3 (P16), disparar al más cercano (P7), promedio de 4 vecinos
  (E8), rey del torneo (E11), pozos sin cruces (E3), torres y n²/2 (P8), pentágono y
  triángulo de diagonales (E6), circuncírculo que cubre (E16).
- **patrones** (11, cap. 2/4 coloreo+casillas): R(3,3)=6 (E12), R(3,3,3)=17 (E13), nueve
  tapetes 1/9 (E11), coprimos / divisibilidad entre n+1 de 1..2n, Erdős–Szekeres,
  bloque consecutivo divisible por n, dos con mismo nº de amigos, tablero mutilado,
  5 puntos en cuadrado (√2/2), 51 de 100.
- **inversion** (11, cap. 13/14 juegos+hacia-atrás): 21 cerillos (mult 4), juego del 100
  (≡1 mod 11), Nim 2 montones (espejo), monedas en mesa redonda (simetría), jarras 3&5
  →4, misère 1-2 (≡1 mod 3), doblar/+1 hasta N (binario), pesas de Bachet 1/3/9/27,
  Nim 3 montones (XOR), restar-cuadrado (DP retrógrada), juego del 15 = tres en raya.

**§1.2 cumplida — TODAS las afirmaciones numéricas verificadas con Python** antes de
escribir (invariantes de paridad/mod; R(3,3) y R(3,3,3) por fuerza bruta; Erdős–Szekeres
y bloque-divisible en miles de instancias; Nim/XOR, juego-100, misère, subtract-square
por minimax; Bachet 1..40; M/m≥√3 y enanos 6/7..0 por simulación). El builder de un solo
uso vive en `scripts/_build_engel.py` (idempotencia por chequeo de ids).

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`,
sin bump de `sw.js` (Engel → camino 1/entrenamiento, no fase-7/estudio). Verificación §9
en verde: ambos JSON válidos; 144 ids únicos (1-144); esquema §4.1 correcto para 101-144;
`verificar-shell.py` OK (203 archivos). Distribución total problems.json: invariantes 35,
optimizacion 37, patrones 36, inversion 36.

**Siguiente** — continuar Sector C con la carpeta `Arena/Problem solving y olimpiadas/`:
Zeitz (Art and Craft), Pólya (Cómo plantear y resolver), Putnam and Beyond, Bóna
(Walk Through Combinatorics), Kevin Houston, y la serie AoPS (Intro/Med/Vol/Calculus).
Mismo esquema §4.1 (ids 145+, sin huecos) y, donde aplique, `fase-0` (Pólya/Houston/Zeitz
cap.1-2/AoPS Intro como material introductorio del Modo Estudio). Verificar SIEMPRE con
Python. `A Mind for Numbers` (soporte-teórico) puede marcarse `hecho` con 0 al cerrar.

## Bitácora 2026-06-14 (Arena tanda 28) — SECTOR C: Zeitz, *The Art and Craft of Problem Solving*, 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `The Art and Craft of Problem Solving`
(3rd ed., Paul Zeitz) — libros[28] del ledger, ruta `entrenamiento`, cuota 40
(superada con **44**). Destino: **`data/problems.json`** (esquema §4.1), ids
**145-188** sin huecos. **Distribución balanceada 11/11/11/11** por `estrategia`,
tomada de los capítulos que mejor encarnan cada heurística:

- **inversion** (11, §3.1 simetría/reflexión + §4.4 juegos): censista→2,2,9 (hacia
  atrás), camino que toca dos ejes = √170 (reflexión), perímetro mínimo Putnam 1998
  = √(2(a²+b²)) (doble reflexión), integral Putnam 1980 = π/4 (sustitución x→π/2−x),
  monedas en mesa (estrategia de simetría), √2 irracional por descenso (papel doblado),
  takeaway 17 (P-posiciones = múltiplos de 5), divide&conquer 100 (gana par), Nim
  17⊕11⊕8=18 (Bouton), Putnam 1995 cuatro montones (Sprague-Grundy), chocolate mn−1.
- **invariantes** (11, §3.3-3.4 casillero/invariantes): tile 66×62 con 12×1 imposible
  (de Bruijn), fichas de Conway y=5 inalcanzable (monovariante razón áurea ζ²+ζ−1=0),
  tres ranas (paridad mod 2 de la rejilla), uv+u+v sobre 1..100 → 101!−1, rotación
  {3,4,12}→{4,6,12} imposible (sumSq 169≠196), sucesión último-dígito-de-6 (1,3,5,7,9
  imposible por paridad), divisibilidad cíclica imposible, 9 puntos enteros 3D (casillero
  2³), solitario búlgaro (punto fijo ⇔ total triangular), 5 puntos en cuadrado → √2/2,
  torneo de eliminación n−1 juegos.
- **optimizacion** (11, §3.2 extremo + §5.5 desigualdades): (Σa)(Σ1/a)≥n², ⌊Σ1/√n⌋=198
  (telescopaje), IMO 1976 producto máx = 2·3^658, (a²b+b²c+c²a)(ab²+bc²+ca²)≥9a²b²c²,
  √(3(a+b+c))≥√a+√b+√c, 1/a+1/b+4/c+16/d≥64/(a+b+c+d) (Cauchy-Engel), xyz=1⇒Σx≤Σx²,
  Nesbitt = 3/2, IMO 1984 ∈[0,7/27], n!<((n+1)/2)ⁿ, moneda tangente a ≤5 (extremo).
- **patrones** (11, §1.1+§3.1+§7.4-7.5 conteo/teoría de números): telescopaje = 99/100,
  producto de 4 en PA + d⁴ = cuadrado, producto de divisores = n^(d(n)/2), subconjuntos
  de {1..30} con suma >232 = 2²⁹, temperatura promedio esfera = 1600/3, Grecia 1995
  (−5⁴+5⁵+5ⁿ cuadrado → n=5), Reino Unido 1995 ((1+1/a)(1+1/b)(1+1/c)=2 → 5 ternas),
  2⁸+2¹¹+2ⁿ cuadrado → n=12, India 1995 (7ˣ−3ʸ=4 → (1,1)), Putnam 1983 (divisores de
  10⁴⁰ o 20³⁰ = 2301), x²+y²+z²=2xyz → solo (0,0,0) (descenso).

**§1.2 cumplida — TODAS las afirmaciones numéricas verificadas con Python** antes de
escribir (ver `/tmp/verify_zeitz.py` y `/tmp/verify_zeitz2.py`, 58 chequeos en verde):
juegos por solver retrógrado y Sprague-Grundy (takeaway, divide&conquer, Nim, Putnam'95);
diofantinas por fuerza bruta (n=5, n=12, (1,1), 5 ternas, origen); desigualdades por
muestreo masivo (AM-GM, Cauchy, Nesbitt min 3/2, IMO'84 max 7/27, ⌊Σ1/√n⌋=198);
identidades exactas (101!−1, prod divisores n^(d/2), 2²⁹, 1600/3, de Bruijn por backtracking,
2301 por inclusión-exclusión). El builder de un solo uso vive en `scripts/_build_zeitz.py`
(idempotencia por chequeo de ids).

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`,
sin bump de `sw.js` (Zeitz → camino 1/entrenamiento, no fase-7/estudio). Verificación §9
en verde: ambos JSON válidos; 188 ids únicos (1-188) sin huecos; esquema §4.1 correcto
para 145-188; `verificar-shell.py` OK (203 archivos). Distribución total problems.json:
inversion 47, optimizacion 48, invariantes 46, patrones 47 (188 total, global balanceado).

**Siguiente** — continuar Sector C con la carpeta `Arena/Problem solving y olimpiadas/`:
Pólya (`Cómo Plantear y Resolver Problemas`), Putnam and Beyond (Andreescu), Bóna
(`A Walk Through Combinatorics`), Kevin Houston, y la serie AoPS (Intro/Med/Vol/Calculus).
Mismo esquema §4.1 (ids 189+, sin huecos) y, donde aplique, `fase-0` como material
introductorio del Modo Estudio. Verificar SIEMPRE con Python.

## Bitácora 2026-06-14 (Arena tanda 29) — SECTOR C: Pólya SALTADO (decisión del usuario)

El usuario pidió **brincar Pólya** (`Cómo Plantear y Resolver Problemas`) y marcarlo
`completado` con 0 problemas en el ledger. Razón anotada: *How to Solve It* es ante todo
metodología/heurística (las 4 fases de Pólya YA son el esqueleto de la app y de los
`hints`), no una cantera de enunciados con respuesta numérica verificable; su material
introductorio encaja mejor en `fase-0`/Modo Estudio que en `problems.json`. Sin cambios
en datos salvo el `estado` del ledger. Se priorizó §10 hacia Putnam and Beyond (tanda 30).

## Bitácora 2026-06-14 (Arena tanda 30) — SECTOR C: Andreescu & Gelca, *Putnam and Beyond*, 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Putnam and Beyond` (Răzvan Gelca & Titu
Andreescu, Springer 2007) — libros[30] del ledger, ruta `entrenamiento`, cuota 40
(superada con **44**). Destino: **`data/problems.json`** (esquema §4.1), ids **189-232**
sin huecos. **Distribución balanceada 11/11/11/11.** Fuente: **cap. 1 «Methods of Proof»**
(que mapea perfecto a las 4 estrategias) + **§3.1.1 «Search for a Pattern»**. El libro
trae soluciones completas en su parte 2, lo que facilitó verificar.

- **inversion** (11, §1.1 contradicción + §1.2 construcción/hacia-atrás): √2+√3+√5 irracional,
  9 consecutivos sin partición de igual producto, Euler (no hay polinomio entero que dé solo
  primos), desplazamiento cíclico único con sumas parciales positivas (Raney), L-triominós en
  2ⁿ×2ⁿ menos esquina, cubo no disecable en cubos distintos (extremo), **IMO 2005** fichas
  (2 restantes ⇔ 3∤(n−1)), ±1²±2²±…±n²=N, Zeckendorf, n-dígitos div 2ⁿ con {2,3}, n-dígitos
  div 5ⁿ con {5–9}.
- **invariantes** (11, §1.3 casillero + §1.5 invariantes/semi-invariantes): **IMO 1972** (10
  números de dos dígitos → subconjuntos de igual suma), 9 puntos en cuadrado → triángulo ≤1/8,
  un Fibonacci divisible por 1000 (Pisano), ajedrecista → 20 juegos en días consecutivos, 2m+1
  enteros → tres suman 0, rotación √2 (sumSq 6.5≠6+2√2), Ducci 4-tuplas → (0,0,0,0), signos
  3×3 (invariante de producto 2×2), caballo generalizado (retorno en pasos pares), **IMO 1985**
  (1985 enteros → 4 con producto 4ª potencia), bolas de colores (≥1 verde).
- **optimizacion** (11, §1.4 extremo + §1.2 desigualdades): 50 enteros <100 → dos coprimos,
  3ⁿ≥n³, (n/3)ⁿ<n!<(n/2)ⁿ, Σ1/k³<3/2, Cauchy Σ1/(1+aᵢ)≥n/(1+G), Huygens ∏(1+aᵢ)≥(1+G)ⁿ,
  |sin nx|≤n|sin x|, Σaᵢ²≥(2n+1)/3·Σaᵢ (enteros distintos), Σ|sin xᵢ|+|cos Σxᵢ|≥1, n puntos →
  ángulo ≤π/n, cuadrados de área total 1 caben en cuadrado de área 2.
- **patrones** (11, §1.2 Fibonacci + §3.1.1 sucesiones): F(2n+1)=F(n+1)²+F(n)², F(3n)=
  F(n+1)³+F(n)³−F(n−1)³, identidad armónica alternante, recurrencia x_{n+3}=xₙ+xₙ₊₁xₙ₊₂ (alcanza
  múltiplo de m), divisores coprimos a+b−1|n ⇔ n potencia de primo impar, sucesión 1,2,2,3,3,3,…
  → ⌈(√(8k+1)−1)/2⌉, recurrencia de orden 4 → aₙ=n·Fₙ, ecuación funcional → aₙ=n², torres 3 vs
  100 → menor m=99, recurrencia con techo → xₙ−1 múltiplo de 3, teselados 2n×3 con dominós (2±√3).

**§1.2 cumplida — 39 afirmaciones numéricas verificadas con Python** (`/tmp/verify_putnam.py`):
juegos/IMO 2005 por búsqueda exhaustiva; identidades de Fibonacci y sucesiones recursivas
(297/299/300/303/311/Tomescu) por cómputo exacto; desigualdades por muestreo masivo; casillero
por conteo; Ducci/caballo/signos por simulación y BFS. Las pruebas de existencia/estructura
(cubo, ajedrecista, bolas, 50-coprimos, ángulo, cuadrados-área2) se tomaron **fielmente del
libro** (su «solución» es el argumento). **NOTA de honestidad:** se descartó el problema 1.1.6
(no existe f:ℤ→{1,2,3} con f(x)≠f(y) si |x−y|∈{2,3,5}) porque no se pudo verificar limpiamente
(no hay K₄ en el grafo de distancias {2,3,5}, así que el argumento de coloreo no es por clique).

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
232 ids únicos (1-232) sin huecos; esquema §4.1 correcto para 189-232; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: inversion 58, optimizacion 59, invariantes 57,
patrones 58 (232 total, global balanceado). Builder idempotente en `scripts/_build_putnam.py`.

**Siguiente** — continuar Sector C con la carpeta `Arena/Problem solving y olimpiadas/`:
Bóna (`A Walk Through Combinatorics`), Kevin Houston (`How to Think Like a Mathematician`),
y la serie AoPS (Intro/Med/Vol/Calculus). Mismo esquema §4.1 (ids 233+, sin huecos) y, donde
aplique, `fase-0` como material introductorio del Modo Estudio. Verificar SIEMPRE con Python.

## Bitácora 2026-06-14 (Arena tanda 31) — SECTOR C: Bóna, *A Walk Through Combinatorics*, 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `A Walk Through Combinatorics` (Miklós
Bóna, 2.ª ed., World Scientific) — libros[31] del ledger, ruta `entrenamiento`, cuota
40 (superada con **44**). Destino: **`data/problems.json`** (esquema §4.1), ids
**233-276** sin huecos. **Distribución balanceada 11/11/11/11.** Fuente: **cap. 1
«Pigeon-Hole Principle»**, **cap. 2 «Mathematical Induction»** y **cap. 9 «Graph
Theory»** — los tres con soluciones completas en el libro, lo que facilitó verificar.

- **invariantes** (11, cap. 1 casillero + cap. 9 paridad): fiesta de los Smith (la
  anfitriona da 4 apretones), 1500 despegues > 1440 minutos, 100 puntos en cubo →
  tetraedro ≤ 1/99, 9 enteros (factores ≤ 6) → producto cuadrado (2³ clases de paridad),
  502 enteros → suma o diferencia divisible por 1000, 17 puntos en triángulo → dos a ≤ 1/4,
  n+1 de {1..2n} → uno divide a otro (parte impar), apretón de manos (hermanos impares /
  apretones impares son par en número), dos vértices del mismo grado, 44ⁿ−1 divisible por 7.
- **inversion** (11, cap. 2 inducción/construcción): aₙ=2·3ⁿ−1, aₙ=(2·4ⁿ+1)/3, aₙ=2·3ⁿ⁻¹
  (suma acumulada), 6 | n³+11n, 7 | 8ⁿ−14n+27, cortar cuadrados → 3m+1, torneo donde un
  «rey» lista a todos, 2ⁿ jugadores → fila de n+1 que se vencen, triángulo → 3n+1 semejantes,
  cuadrado → n cuadrados (n>14), aₙ=(8·10ⁿ+1)/9.
- **optimizacion** (11, cap. 2 desigualdades + cap. 9 extremal): AM-GM por inducción de
  Cauchy, HM ≤ GM, 3ⁿ>n⁴ (n≥8), 100 reales suma 0 → ≥99 sumas no negativas (óptimo), 10
  vértices/28 aristas → C₄, 9 vértices grados ≥27 → grado ≥4, 10 vértices/38 aristas → K₄
  inducido, 7 vértices grado ≥3 → conexo, grado mínimo k → ciclo ≥ k+1, recurrencia aₙ ≤ 3ⁿ,
  secuencia [4,4,4,2,1,1] no gráfica (Havel–Hakimi).
- **patrones** (11, cap. 2 identidades + cap. 9 conteo): Σk³=(Σk)² (Nicómaco), Σi(i+1)=
  n(n+1)(n+2)/3, recurrencia con raíz doble aₙ=n·3ⁿ⁻¹, #grafos sobre [n]=2^C(n,2),
  automorfismos de Kₙ/Cₙ/Pₙ/Sₙ, ciclos hamiltonianos de Kₙ=(n−1)!/2, >6600 grafos no
  isomorfos en 8 vértices, automorfismos del cubo = 48, ciclos hamiltonianos del cubo = 6,
  1/a+1/b+1/c=1 → (2,3,6), 1/a+1/b+1/c+1/d=1 → 6 cuádruplas.

**§1.2 cumplida — las 44 afirmaciones numéricas verificadas con Python**
(`/tmp/verify_bona.py`): recurrencias e identidades por cómputo exacto; divisibilidad
directa; conteo de grafos, automorfismos y ciclos hamiltonianos por enumeración; diofantinas
(fracciones egipcias) por fuerza bruta; casillero por conteo; desigualdades por muestreo. El
C₄ forzado se confirmó empíricamente (20 000 grafos aleatorios 10v/28e siempre tienen C₄) y
con el valor extremal ex(10; C₄)=16 < 28. Las pruebas extremales/de existencia (torneo «rey»,
fila de jugadores, conexión por grado mínimo, ciclo largo, optimalidad de las 99 sumas) se
tomaron **fielmente del libro**. **CORRECCIÓN de honestidad:** el Ej. 25 del cap. 1 pregunta
si entre n+1 enteros de {1..2n} siempre hay dos donde uno es el DOBLE del otro — la respuesta
es NO (contraejemplo {1,3,4,5,7} para n=4); se usó la variante verdadera «uno DIVIDE al otro».

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
276 ids únicos (1-276) sin huecos; esquema §4.1 correcto para 233-276; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: inversion 69, optimizacion 70, invariantes 68,
patrones 69 (276 total, global balanceado). Builder idempotente en `scripts/_build_bona.py`.

**Siguiente** — continuar Sector C con la carpeta `Arena/Problem solving y olimpiadas/`:
Kevin Houston (`How to Think Like a Mathematician`) y la serie AoPS (Intro/Med/Vol/Calculus).
Mismo esquema §4.1 (ids 277+, sin huecos) y, donde aplique, `fase-0` como material
introductorio del Modo Estudio. Verificar SIEMPRE con Python.

## Bitácora 2026-06-15 (Arena tanda 32) — SECTOR C: Houston, *How to Think Like a Mathematician*, 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `How to Think Like a Mathematician`
(Kevin Houston, Cambridge University Press) — libros[32] del ledger, ruta
`entrenamiento`, cuota 40 (superada con **44**). Destino: **`data/problems.json`**
(esquema §4.1), ids **277-320** sin huecos. Fuente: **cap. 24-26 (técnicas de prueba:
inducción, contrapositiva)** + **cap. 27-29 (teoría de números: divisores, algoritmo
de Euclides, aritmética modular)**.

**Distribución 12/11/7/14** (invariantes/inversion/optimizacion/patrones) — Houston es
un libro número-teórico y flojo en desigualdades, así que el sesgo hacia invariantes y
patrones es honesto y además **mejora el balance GLOBAL** de problems.json (invariantes
y optimizacion eran de los más bajos antes de esta tanda).

- **invariantes** (12, modular/paridad/divisibilidad): x²+9x+20 par; x³−x÷3, x⁵−x÷5 y
  xⁿ−x NO siempre ÷n (Fermat solo primos); x³−6x²+11x÷3; cuadrado mód 4 ∈ {0,1}; 3^{2n}−1÷8;
  17 | 3^{4n}+4^{3n+2}; n²−1÷8 (n impar); 4·11ⁿ+2·5ⁿ÷6; ÷8 por los tres últimos dígitos;
  m²|n²⇒m|n; números de Fermat coprimos dos a dos; 6·9ⁿ−4ⁿ÷5.
- **inversion** (11, contradicción/contrapositiva/inducción): infinitud de primos (Euclides),
  √n irracional si n no es cuadrado, x irr⇒√x irr, x+y irr⇒x o y irr, xy impar⇒ambos impares,
  x² par⇒x par, todo n>1 es producto de primos (inducción fuerte), xₙ=2ⁿ+1, (x−1)|(xⁿ−1),
  ángulos de n-gono = 180(n−2), x²−3x+2<0 ⟺ 1<x<2.
- **optimizacion** (7, desigualdades/extremal): n²≤2^{n−1} (n≥7), 2ⁿ<n! (n≥4), xₙ<(7/4)ⁿ,
  |Σxᵢ|≤Σ|xᵢ| (triangular), gcd(a+b,a−b)≤2 (coprimos), sin nx ≤ n sin x en [0,π/2], lema de
  la división (menor resto vía buen orden).
- **patrones** (14, NT/identidades/recurrencias/Fibonacci): Σi²=n(n+1)(2n+1)/6, Euclides
  gcd(14441,3563)=7, Bézout 132·14441−535·3563=7, diofantina 51x+21y=18, fórmula de Binet,
  Σ Fibonacci impares = F_{2n}, Σ Fibonacci pares = F_{2n+1}−1, recurrencia promediadora
  xₙ=(2^{n−1}+(−1)ⁿ)/(3·2^{n−2}), factorización de 12870 y 17836, lcm·gcd=ab, 2ⁿ subconjuntos,
  (xⁿ−1)/(x−1)=Σxⁱ, diofantina soluble ⟺ gcd|c, ∏F_k=F_{n+1}−2.

**§1.2 cumplida — 49 afirmaciones numéricas verificadas con Python** (`/tmp/verify_houston.py`):
modular/divisibilidad por conteo masivo; Euclides, Bézout y diofantinas por cálculo exacto;
recurrencias e identidades de Fibonacci (incl. Binet, recurrencia promediadora con fracciones
exactas) por cómputo exacto; desigualdades por muestreo; factorizaciones por trial division.
**NOTA:** Houston es un libro de «cómo pensar/probar» (estilo Pólya), pero —a diferencia de
Pólya, que se saltó— SÍ contiene ejercicios concretos y verificables en sus Partes IV-V
(teoría de números, inducción), por lo que se procesó como tanda completa.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
320 ids únicos (1-320) sin huecos; esquema §4.1 correcto para 277-320; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: inversion 80, optimizacion 77, invariantes 80,
patrones 83 (320 total, global balanceado, spread 77-83). Builder idempotente en
`scripts/_build_houston.py`.

**Siguiente** — continuar Sector C con la **serie AoPS** de la carpeta `Arena/Problem solving
y olimpiadas/`: `IntroAlgeb.pdf`, `IntroGeom.pdf`, `IntroNumbTheo.pdf`, `introCountProb.pdf`,
`MedAlgebra.pdf`, `MedCountProb.pdf`, `Vol1.pdf`, `Vol2.pdf`, `Calculus.pdf` (Patrick et al.).
Mismo esquema §4.1 (ids 321+, sin huecos). Verificar SIEMPRE con Python.

## Bitácora 2026-06-15 (Arena tanda 33) — SECTOR C: AoPS *Introduction to Algebra* (Rusczyk), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Introduction to Algebra` (Richard
Rusczyk, Art of Problem Solving, 2.ª ed.) — libros[34] del ledger, ruta
`entrenamiento`, cuota 40 (superada con **44**). Destino: **`data/problems.json`**
(esquema §4.1), ids **321-364** sin huecos. Fuentes internas:
- **cap. 11 «Special Factorizations»** (Simon's Favorite Factoring Trick, diferencia de
  cuadrados, identidad del producto de 4 consecutivos +1, telescopaje con racionalización)
  → **patrones**.
- **cap. 15 «More Inequalities»** (desigualdad trivial x²≥0, AM-GM, optimización cuadrática
  completando el cuadrado, discriminante como condición de existencia) → **optimizacion**.
- **cap. 22 «Special Manipulations»** (elevar ecuaciones a potencias; auto-similaridad:
  radicales anidados y fracciones continuas) → **inversion**; (simetría, sumas/productos de
  raíces tipo Vieta, sistemas simétricos) → **invariantes**.

**Distribución 14/8/11/11** (optimizacion/patrones/inversion/invariantes) — el texto es
riquísimo en optimización cuadrática y desigualdades, sesgo elegido para llevar el balance
**GLOBAL a 91/91/91/91 exactos** (antes 77/83/80/80).

**NOTA de honestidad (verificación):** el volumen de SOLUCIONES de AoPS es un libro aparte
**no disponible** en la Arena, así que **cada solución y cada número se resolvió y verificó de
forma independiente con Python** (sympy/fractions; scripts `/tmp/verif_aops.py` y
`/tmp/verif_aops2.py`, 26 afirmaciones — todas OK tras corregir dos artefactos del propio
verificador, no de la matemática). Caso documentado: en `bc − 7b + 3c = 70` el texto cuenta
**6** soluciones admitiendo enteros de cualquier signo; el problema **336** pide enteros
**positivos** y se verifican **2** soluciones [(4,14),(46,8)] — el enunciado quedó acotado a
positivos para coincidir con lo verificado.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
364 ids únicos (1-364) sin huecos; esquema §4.1 correcto para 321-364; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: **inversion 91, optimizacion 91, invariantes
91, patrones 91** (364 total, balance perfecto). Builder idempotente en
`scripts/_build_aops_introalg.py`.

**Siguiente** — seguir con la serie AoPS: `IntroGeom.pdf`, `IntroNumbTheo.pdf`,
`introCountProb.pdf`, `MedAlgebra.pdf`, `MedCountProb.pdf`, `Vol1.pdf`, `Vol2.pdf`,
`Calculus.pdf`. Mismo esquema §4.1 (ids 365+, sin huecos). Verificar SIEMPRE con Python.

## Bitácora 2026-06-15 (Arena tanda 34) — SECTOR C: AoPS *Introduction to Geometry* (Rusczyk), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Introduction to Geometry` (Richard
Rusczyk, Art of Problem Solving, 2.ª ed.) — libros[35] del ledger, ruta
`entrenamiento`, cuota 40 (superada con **44**). Destino: **`data/problems.json`**
(esquema §4.1), ids **365-408** sin huecos. Fuentes internas (TOC verificado; se leyeron
las secciones de Review Problems / Challenge Problems de los caps. 4, 6 y 9):
- **cap. 4 «Perimeter and Area»** → razón de áreas con base/altura compartida y la ceviana
  que reparte el área (**invariantes**); máximos de área e isoperimétrico, rectángulo inscrito
  (**optimizacion**); trabajar hacia atrás desde área/perímetro a dimensiones (**inversion**).
- **cap. 6 «Right Triangles»** → ternas pitagóricas (3-4-5, 5-12-13, 8-15-17, 7-24-25 y sus
  múltiplos), triángulos especiales 30-60-90 y 45-45-90, área del equilátero, recíproco de
  Pitágoras y conteo de ternas (**patrones**); escalera deslizante y (área+hipotenusa)→perímetro
  vía (a+b)² (**inversion**); altura mínima sobre el lado mayor (**optimizacion**).
- **cap. 9 «Polygons»** → suma de ángulos interiores (n−2)·180°, exteriores = 360°, diagonales
  n(n−3)/2 (**invariantes**); más **potencia de un punto** (cap. 13) y **ángulo inscrito**
  (cap. 12) como invariantes.

**Distribución 11/11/11/11** (invariantes/patrones/optimizacion/inversion) — geometría es
balanceada por naturaleza; se eligió para llevar el balance **GLOBAL a 102/102/102/102 exactos**
(antes 91/91/91/91).

**NOTA de honestidad (verificación):** el volumen de SOLUCIONES de AoPS es un libro aparte
**no disponible** en la Arena, así que **cada número se resolvió y verificó de forma independiente
con Python** (44 afirmaciones — todas OK). Caso documentado: el **Prob. 6.54** (triángulos
rectángulos de lados enteros con un cateto = 24) lo fija Python en **7**, no 6 — la enumeración
da catetos 24 con {7, 10, 18, 32, 45, 70, 143} (siete factorizaciones pares de 576). Se usó 7;
Python corrigió la suposición inicial.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
408 ids únicos (1-408) sin huecos; esquema §4.1 correcto para 365-408; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: **inversion 102, optimizacion 102, invariantes
102, patrones 102** (408 total, balance perfecto). Builder idempotente en
`scripts/_build_aops_introgeom.py`.

**Siguiente** — seguir con la serie AoPS: `IntroNumbTheo.pdf`, `introCountProb.pdf`,
`MedAlgebra.pdf`, `MedCountProb.pdf`, `Vol1.pdf`, `Vol2.pdf`, `Calculus.pdf`. Mismo esquema §4.1
(ids 409+, sin huecos). Verificar SIEMPRE con Python.

## Bitácora 2026-06-15 (Arena tanda 35) — SECTOR C: AoPS *Introduction to Number Theory* (Crawford/Rusczyk), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Introduction to Number Theory` (Mathew
Crawford & Richard Rusczyk, Art of Problem Solving) — libros[36] del ledger, ruta
`entrenamiento`, cuota 40 (superada con **44**). Destino: **`data/problems.json`**
(esquema §4.1), ids **409-452** sin huecos. Fuentes internas (TOC verificado; se leyeron
las secciones Review/Challenge de los caps. 4, 5, 10 y 12):
- **cap. 4 «Prime Factorization»** → identidad ab = mcd·mcm, reconstruir n desde mcd/mcm,
  menor múltiplo/menor k, completar a cuadrado/cubo perfecto (**invariantes/optimizacion/inversion**).
- **cap. 5 «Divisor Problems»** → fórmula t(n) = ∏(eᵢ+1), divisores cuadrados perfectos,
  menor entero con d divisores, números con t(n) primo (**patrones/optimizacion/inversion**).
- **cap. 10 «Units Digits»** → dígito de unidades de productos (determinado por las unidades)
  y ciclos de las potencias (incl. dígito de unidades en base b) (**invariantes/patrones**).
- **cap. 12 «Modular Arithmetic»** → residuos, congruencias de producto y potencia, 21ⁿ−12ⁿ,
  ciclos de potencias mód p (Fermat) (**invariantes/patrones**).

**Distribución 11/11/11/11** (invariantes/patrones/optimizacion/inversion) — se eligió para
llevar el balance **GLOBAL a 113/113/113/113 exactos** (antes 102/102/102/102).

**NOTA de honestidad (verificación):** el volumen de SOLUCIONES de AoPS es un libro aparte
**no disponible** en la Arena, así que **cada número se resolvió y verificó de forma independiente
con Python** (sympy/math; 44 afirmaciones — todas OK). Casos comprobados por enumeración:
menor N con producto-de-dos-divisible-por-el-tercero para {30,72,N} = **60**; menor entero con
20 divisores = **240**; menor N con 7+30N no primo = **6** (187 = 11·17, tras cinco primos
seguidos).

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
452 ids únicos (1-452) sin huecos; esquema §4.1 correcto para 409-452; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: **inversion 113, optimizacion 113, invariantes
113, patrones 113** (452 total, balance perfecto). Builder idempotente en
`scripts/_build_aops_intront.py`.

**Siguiente** — seguir con la serie AoPS: `introCountProb.pdf`, `MedAlgebra.pdf`,
`MedCountProb.pdf`, `Vol1.pdf`, `Vol2.pdf`, `Calculus.pdf`. Mismo esquema §4.1 (ids 453+, sin
huecos). Verificar SIEMPRE con Python.

## Bitácora 2026-06-15 (Arena tanda 36) — SECTOR C: AoPS *Introduction to Counting & Probability* (Patrick), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Introduction to Counting & Probability`
(David Patrick, Art of Problem Solving) — libros[37] del ledger, ruta `entrenamiento`,
cuota 40 (superada con **44**). Destino: **`data/problems.json`** (esquema §4.1), ids
**453-496** sin huecos. Fuentes internas (TOC verificado; se leyeron las secciones
Review/Challenge de los caps. 2, 3, 4, 8 y 11):
- **cap. 2 «Basic Counting» + cap. 3 «Correcting for Overcounting»** → conteo complementario,
  constructivo, restricciones; permutaciones con repetidos y simetrías circulares.
- **cap. 4 «Committees and Combinations» + cap. 5** → C(n,r), identidad C(n,r)=C(n,n−r),
  caminos en cuadrícula.
- **cap. 8 «Basic Probability»** → suma/complemento/producto de probabilidades, P(A)+P(no A)=1.
- **cap. 11 «Expected Value» + cap. 12-13 «Pascal / Hockey Stick»** → valor esperado,
  identidades de Pascal y del palo de hockey.

**Distribución 11/11/11/11** (patrones/invariantes/optimizacion/inversion) — para llevar el
balance **GLOBAL a 124/124/124/124 exactos** (antes 113/113/113/113). Mapeo: fórmulas e
identidades combinatorias → **patrones**; conteo complementario, corrección de sobreconteo por
división y P(A)+P(no A)=1 / valor esperado como promedio ponderado → **invariantes**;
máximos/mínimos y garantías de tipo palomar (pigeonhole) y decisiones por valor esperado →
**optimizacion**; reconstruir n desde un conteo/probabilidad y «contar lo que no quieres»
(complementario) → **inversion**.

**NOTA de honestidad (verificación):** el volumen de SOLUCIONES de AoPS es un libro aparte
**no disponible** en la Arena, así que **cada número se resolvió y verificó de forma independiente
con Python** (math.comb/factorial, fractions; 44 afirmaciones — todas OK). Casos confirmados:
P(3 cartas no todas del mismo color) = 13/17; helicópteros óptimos = 2; menor n con C(n,2) ≥ 100
= 15; «palabras» de 5 letras con ≥2 consecutivas iguales = 1 725 126.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
496 ids únicos (1-496) sin huecos; esquema §4.1 correcto para 453-496; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: **inversion 124, optimizacion 124, invariantes
124, patrones 124** (496 total, balance perfecto). Builder idempotente en
`scripts/_build_aops_introcp.py`.

**Siguiente** — seguir con la serie AoPS: `MedAlgebra.pdf`, `MedCountProb.pdf`, `Vol1.pdf`,
`Vol2.pdf`, `Calculus.pdf`. Mismo esquema §4.1 (ids 497+, sin huecos). Verificar SIEMPRE con
Python.

## Bitácora 2026-06-15 (Arena tanda 37) — SECTOR C: AoPS *Intermediate Algebra* (Rusczyk), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Intermediate Algebra` (Richard Rusczyk,
Art of Problem Solving) — libros[38] del ledger, ruta `entrenamiento`, cuota 40 (superada
con **44**). Destino: **`data/problems.json`** (esquema §4.1), ids **497-540** sin huecos.

**NOTA TÉCNICA importante:** el PDF (193 MB, escaneado) **excede el límite de 100 MB de la tool
Read**. El TOC se extrajo con **PyMuPDF (`fitz`)**; la capa OCR distorsiona los símbolos
matemáticos, así que los problemas se **reformularon con palabras propias fieles a los temas de
cada capítulo** (§5 lo permite) y **cada número se verificó de forma independiente con
Python/sympy** (44 afirmaciones — todas OK). *Para los próximos AoPS grandes (Vol1/Vol2/Calculus
si superan 100 MB), usar la misma vía: `fitz` para el TOC y construcción verificada con Python.*

Fuentes internas (capítulos confirmados por TOC):
- **cap. 3 Complex Numbers, cap. 4 Quadratics, cap. 8 Vieta's Formulas** → fórmulas de Vieta
  (suma/producto de raíces), expresiones simétricas, conjugados (**invariantes**); construir
  ecuaciones desde sus raíces, despejar parámetros (**inversion**).
- **cap. 10/17 Sequences & Series** → aritméticas/geométricas, sumas de potencias y telescopaje
  (**patrones** e **invariantes**).
- **cap. 12/18 Inequalities** → AM-GM, Cauchy-Schwarz, vértice de la parábola (**optimizacion**).
- **cap. 13 Exponents & Logarithms, cap. 19 Functional Equations** → logs como inverso de la
  exponencial, ecuaciones funcionales por sustitución (**inversion**).

**Distribución 11/11/11/11** (invariantes/patrones/optimizacion/inversion) — para llevar el
balance **GLOBAL a 135/135/135/135 exactos** (antes 124/124/124/124).

**NOTA de honestidad (verificación):** el volumen de SOLUCIONES de AoPS es un libro aparte
**no disponible**; cada número se resolvió y verificó con Python/sympy. Casos: telescopaje
∑1/(n(n+1)) hasta 99 = 99/100; producto ∏(1−1/n²) de 2 a 10 = 11/20; ecuación funcional
f(x)+2f(1/x)=x ⇒ f(2) = −1/3; Cauchy-Schwarz: máx de 3x+4y con x²+y²=1 es 5.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
540 ids únicos (1-540) sin huecos; esquema §4.1 correcto para 497-540; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: **inversion 135, optimizacion 135, invariantes
135, patrones 135** (540 total, balance perfecto). Builder idempotente en
`scripts/_build_aops_medalg.py`.

**Siguiente** — seguir con la serie AoPS: `MedCountProb.pdf`, `Vol1.pdf`, `Vol2.pdf`,
`Calculus.pdf`. Mismo esquema §4.1 (ids 541+, sin huecos). Verificar SIEMPRE con Python; si el
PDF supera 100 MB, extraer el TOC con `fitz` (ver nota técnica arriba).

## Bitácora 2026-06-15 (Arena tanda 38) — SECTOR C: AoPS *Intermediate Counting & Probability* (Patrick), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Intermediate Counting & Probability` (David
Patrick, Art of Problem Solving) — libros[39] del ledger, ruta `entrenamiento`, cuota 40
(superada con **44**). Destino: **`data/problems.json`** (esquema §4.1), ids **541-584** sin
huecos.

**NOTA TÉCNICA:** el PDF (81 MB) cabe bajo el límite de 100 MB de Read, **pero NO tiene capa de
texto** (`fitz.get_text()` devolvió vacío: es imagen pura). El TOC y las secciones de ejercicio
(caps. 3 PIE, 7 Distributions) se leyeron como **imágenes con la tool Read**. Cada número se
verificó de forma independiente con Python. *Regla para el siguiente agente: un PDF puede estar
bajo 100 MB y aun así ser imagen pura; probar `fitz.get_text()` primero y, si está vacío, leer
páginas como imágenes con Read.*

Fuentes internas (capítulos por TOC):
- **cap. 3 PIE + cap. 12 Combinatorial Identities** → inclusión-exclusión y Vandermonde
  (**invariantes** y **patrones**).
- **cap. 5 Pigeonhole** → garantías de peor caso (**optimizacion**).
- **cap. 6 Constructive Expectation + cap. 11 Conditional Probability** → linealidad de la
  esperanza, probabilidad total (**invariantes**); Bayes y Monty Hall (**inversion**).
- **cap. 7 Distributions, cap. 9 Fibonacci, cap. 10 Recursion (Catalan), cap. 14 Generating
  Functions** → estrellas y barras, Fibonacci/Catalan (**patrones**); recurrencias y particiones
  (**inversion**).

**Distribución 11/11/11/11** (patrones/invariantes/optimizacion/inversion) — para llevar el
balance **GLOBAL a 146/146/146/146 exactos** (antes 135/135/135/135).

**NOTA de honestidad (verificación):** cada número se resolvió y verificó con Python (44 checks,
todos OK). Casos: estrellas-barras a+b+c+d=17 positivos = 560; PIE divisibles por 2,3,5 en 1-100
= 74; desarreglos D₄ = 9; Bayes (prevalencia 1%, sens/espec 90%) = 1/12; Monty Hall al cambiar =
2/3; particiones de 5 = 7; Catalan C₄ = 14.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump
de `sw.js` (entrenamiento, no fase-7/estudio). Verificación §9 en verde: ambos JSON válidos;
584 ids únicos (1-584) sin huecos; esquema §4.1 correcto para 541-584; `verificar-shell.py` OK
(203 archivos). Distribución total problems.json: **inversion 146, optimizacion 146, invariantes
146, patrones 146** (584 total, balance perfecto). Builder idempotente en
`scripts/_build_aops_medcp.py`.

**Siguiente** — seguir con la serie AoPS: `Vol1.pdf`, `Vol2.pdf`, `Calculus.pdf`. Mismo esquema
§4.1 (ids 585+, sin huecos). Verificar SIEMPRE con Python; revisar tamaño y capa de texto del PDF
(ver notas técnicas de tandas 37-38).

## Bitácora 2026-06-15 (Arena tanda 39) — SECTOR C: AoPS *the Art of Problem Solving, Vol. 1* (Lehoczky & Rusczyk), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Vol. 1 (the Basics)` (Lehoczky & Rusczyk) —
libros[40] del ledger, ruta `entrenamiento`, cuota 40 (superada con **44**). Destino:
**`data/problems.json`** (esquema §4.1), ids **585-628** sin huecos. PDF de 5 MB con capa de
texto; TOC extraído con `fitz` (29 capítulos, repaso transversal de TODO el temario básico).

**DECISIÓN CLAVE (anti-duplicación, §1.6):** Vol.1 es un REPASO que solapa con temas ya minados
en tandas previas (Intro/Intermediate Algebra, Geometry, Number Theory, C&P). Para no duplicar
preguntas se eligieron deliberadamente **ángulos y números FRESCOS** (p.ej. logaritmos por sus
LEYES de combinar en vez de evaluar; potencia de un punto tangente-secante con números nuevos;
desigualdad triangular; proporción inversa; Cauchy-Schwarz con 5-12-13). Cada número verificado
con Python/sympy.

**Distribución 11/11/11/11** (invariantes/patrones/optimizacion/inversion) — balance **GLOBAL a
157/157/157/157 exactos** (antes 146/146/146/146). Mapeo: leyes de log / módulo-conjugado complejo
/ potencia de un punto / proporciones encadenadas / media / ángulos → **invariantes**;
sucesiones-series / exponentes / binomios / sumas notables / último dígito → **patrones**;
AM-GM, Cauchy-Schwarz, vértice, desigualdad triangular, distancias → **optimizacion**; resolver
ecuaciones (exp/log/sistemas/cuadráticas), proporción inversa, porcentajes hacia atrás,
reconstruir sucesiones, funciones inversas → **inversion**.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump de
`sw.js`. Verificación §9 en verde: ambos JSON válidos; 628 ids únicos (1-628) sin huecos; esquema
§4.1 correcto para 585-628; `verificar-shell.py` OK (203 archivos). Distribución total
problems.json: **inversion 157, optimizacion 157, invariantes 157, patrones 157** (628 total,
balance perfecto). Builder idempotente en `scripts/_build_aops_vol1.py`.

**Siguiente** — seguir con la serie AoPS: `Vol2.pdf` (the ART of Problem Solving Vol. 2, temas
avanzados), `Calculus.pdf`. Mismo esquema §4.1 (ids 629+, sin huecos). Verificar SIEMPRE con
Python; cuidar la anti-duplicación con números frescos (Vol.2 también solapa temario).

## Bitácora 2026-06-15 (Arena tanda 40) — SECTOR C: AoPS *the Art of Problem Solving, Vol. 2* (Lehoczky & Rusczyk), 44 problemas

Continúa el **SECTOR C (entrenamiento)** con `Vol. 2 (and Beyond)` (Lehoczky & Rusczyk) —
libros[41] del ledger, ruta `entrenamiento`, cuota 40 (superada con **44**). Destino:
**`data/problems.json`** (esquema §4.1), ids **629-672** sin huecos. PDF de 81 MB, **imagen pura**
(get_text vacío); TOC leído como imágenes con Read.

**VALOR NUEVO (anti-duplicación, §1.6):** Vol.2 es el companion AVANZADO de bachillerato y
aporta temas FRESCOS no minados en tandas previas: **trigonometría** (identidades, leyes de
senos/cosenos), **cuadriláteros cíclicos / Ptolomeo**, **cónicas/polares**, **polinomios**
(raíces, **sumas de Newton**), **identidades funcionales**, **límites**, **complejos** (DeMoivre,
**raíces de la unidad**, forma polar), **vectores/producto punto**, **matrices/determinantes**.
Cada número verificado con Python/sympy (44 checks; las sumas/productos de raíces de la unidad
salen 0 numéricamente, ~1e-128).

**Distribución 11/11/11/11** (invariantes/patrones/optimizacion/inversion) — balance **GLOBAL a
168/168/168/168 exactos** (antes 157/157/157/157). Mapeo: identidades trig / ley cosenos-senos /
Ptolomeo / sumas de Newton / producto punto / determinante → **invariantes**; raíces de la unidad
/ DeMoivre / ciclos de i / valores trig / raíces de polinomios → **patrones**; amplitud
a·sen+b·cos / área con ángulo / AM-GM / distancia mínima / extremos en cónicas → **optimizacion**;
resolver trig / trig inversa / identidades funcionales / hallar raíces / Newton hacia atrás /
raíz cuadrada compleja → **inversion**.

**Solo se tocó `data/problems.json`.** Sin cambios de código, sin `data/teoria/*.md`, sin bump de
`sw.js`. Verificación §9 en verde: ambos JSON válidos; 672 ids únicos (1-672) sin huecos; esquema
§4.1 correcto para 629-672; `verificar-shell.py` OK (203 archivos). Distribución total
problems.json: **inversion 168, optimizacion 168, invariantes 168, patrones 168** (672 total,
balance perfecto). Builder idempotente en `scripts/_build_aops_vol2.py`.

**Siguiente** — ÚLTIMO de la serie AoPS: `Calculus.pdf` (AoPS Calculus, David Patrick). Mismo
esquema §4.1 (ids 673+, sin huecos). Verificar SIEMPRE con Python. Tras Calculus, solo queda en
el ledger *A Mind for Numbers* (Sector B, soporte teórico).

## Bitácora 2026-06-16 (Arena tanda 41) — SECTOR C: AoPS *Calculus* (Patrick, Rusczyk, Zawitz) + cierre de *A Mind for Numbers* — 44 problemas

**IDs creados:** 673–716 (44 problemas). **KaTeX calidad libro** en todos los campos: enunciado,
5 hints por problema, solución y explicación. Backslashes dobles en JSON para LaTeX correcta.

**Distribución por estrategia (tanda):** inversion 11 (673-683), optimizacion 11 (684-694),
invariantes 11 (695-705), patrones 11 (706-716).

**Distribución total problems.json:** inversion 179, optimizacion 179, invariantes 179,
patrones 179 — **716 problemas en total, balance perfecto**.

**Fuentes de problemas:** AoPS Calculus (David Patrick, Rusczyk, Zawitz) — capítulos 4-9.
Fuentes secundarias citadas: HMMT, Putnam. PDF image-only → reformulación propia §1.2.
Todos los valores numéricos verificados con Python.

**A Mind for Numbers** (libros[27]): marcado `completado` con `preguntas_agregadas = 0`.
Cuota mínima = 0. Es libro de soporte cognitivo sin problemas extraíbles directamente.

**Ledger:** libros[27] completado (0 probs), libros[42] completado (44 probs, ids 673-716).
**Sin libros pendientes en el ledger.** La serie AoPS está íntegramente ingresada.

**Verificación §9:** `verificar-shell.py` OK (234 archivos); 716 ids únicos (1-716) sin huecos;
schema §4.1 correcto para 673-716; sw.js sin bump (problems.json no está en SHELL precache).

**Solo se tocó `data/problems.json` y `data/arena-ingesta-ledger.json`.** Script idempotente en
`scripts/generar_aops_calculus.py`.
