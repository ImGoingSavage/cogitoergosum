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

## §5.4 MAPA PARA EL SIGUIENTE AGENTE (actualizado 2026-06-11, tarde)

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
6bis. **Decidir el alcance del texto en las lecciones** (bitácora
   "noche, 3"): lecciones redactadas (estado actual) vs. texto íntegro del
   libro vía canal privado en Supabase — el texto íntegro NO puede ir al
   repo público (copyright). Decisión del usuario.
7. **Fase 6 del Modo Estudio** (decidir la dirección CON el usuario antes
   de ingerir): de Zeitz solo queda §8.5 (transformaciones: simetría,
   movimientos rígidos, homotecia) como sección sustantiva. Lo natural
   según el PDF: subir el nivel a **AIME** (los espejos ZIML también
   existen para AIME) y/o seguir con Engel por heurística — caps. 8
   (inducción), 9 (sucesiones), 10 (polinomios), 11 (funcionales),
   12 (geometría), 14 (estrategias adicionales). Protocolo de ingestión y
   anclas de TODO lo ya usado en HANDOFF §3.11.6 (pasos 2-5).
8. **Menores acumulados** (en orden de valor):
   - Web Push diaria opcional (1/día máx, hora elegida, contenido neutro
     — §0.1): requiere un emisor push; con el sitio ya en HTTPS público
     dejó de estar bloqueada por infraestructura.
   - Refinamientos del Modo Estudio (lista al final de HANDOFF §3.11.6):
     preguntas falladas ("no lo tenía") hacia repetición espaciada; timer
     visible en el examen; persistir el textarea de forcejeo del examen;
     piso mínimo de estudio para la racha 📘 (decidir con el usuario);
     materializar los problemas sugeridos en `dosis` como sesiones del
     camino 1.
   - FSRS simplificado y "reintenta tus fallos" (HANDOFF §3.9 y tabla de
     benchmarks: Anki/Lichess).
   - Exponer `evaluarDesconstruccion()` en la UI durante el forcejeo
     (cuidando el gating: feedback de redacción, jamás de corrección).

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

### Cierre de jornada 2026-06-11, noche (estado al apagar)

- **App v12** (sw.js), todo commiteado y pusheado en `main`. Los 3 SQL de
  `supabase/` aplicados y verificados por E2E (Fase C 8/8, claustro 10/10,
  pensar-juntos 9/9 con struggle-first probado).
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
  proceso de revisión; reevaluar solo si la PWA muestra límites reales).
