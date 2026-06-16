# Respuesta a incidentes en sistemas de ML

## De qué trata esta lección (y qué sabrás hacer al final)

Cuando un sistema de ML falla en producción, la respuesta hereda el playbook del SRE pero con un giro propio: el fallo suele ser **Public** (lo ven antes los usuarios), **Fuzzy** (sin inicio ni fin nítidos) y **Unbounded** (toca producto, negocio, legal). Esta lección construye, desde cero, cómo gestionar un incidente de ML —los tres pilares (estado, roles, registro), las fases y los cuatro roles— y qué cambia respecto a un incidente de infraestructura.

Al terminar podrás: (1) reconocer un incidente no gestionado (el peor tipo) y montar la respuesta con estado+roles+registro; (2) nombrar las fases y los cuatro roles (commander, comms, ops, planning); (3) entender por qué en ML un problema de sistemas se disfraza de caída de calidad (la Historia 1, modelo congelado 3 semanas por un OOM crash loop); y (4) prepararte versionando modelos/datos y sin posponer nunca la privacidad. Conecta con el ICS del SRE ([[arena-sre3]]).

## Los tres pilares de un incidente gestionado

**Estado** (en qué fase está) + **roles** (quién hace qué) + **registro** (para el postmortem). Sin ellos aparece el **incidente no gestionado** —el peor tipo—: un ingeniero lo depura en solitario, no mide el impacto en usuarios, no comunica, y otras partes de la organización toman pasos descoordinados. La clave es un **proceso ensayado** que se aplica solo cuando algo merece llamarse incidente (formalizar tiene coste).

## Las fases de un incidente

Pre-incidente → **trigger** → inicio de la caída → **detección** → troubleshooting → **mitigación** (frenar lo peor, rápido y de bajo riesgo) → **resolución** (arreglar la causa) → **follow-up** (retrospectiva y mejoras). A veces no hay mitigación obvia y mitigación = resolución.

## Los cuatro roles (marco tipo FEMA/ICS)

- **Incident commander:** coordina, ve el incidente a alto nivel, asigna y supervisa.
- **Communications lead:** comunicación entrante y saliente (usuarios, otros equipos, soporte).
- **Operations lead:** aprueba, agenda y **registra** todos los cambios de producción (y detiene cambios programados no relacionados).
- **Planning lead:** rastrea lo de largo plazo (work items, logs a analizar, agendar la revisión).

No hace falta una persona por rol, pero **todos deben cubrirse**.

## Qué cambia en un incidente de ML

Los roles son invariantes; cambian **detección** (menos determinista → más difícil atrapar antes que un humano), **stakeholders** (involucra producto, negocio, finanzas, legal) y **timeline** (métricas de calidad que ya varían → inicio/fin difusos). Tres principios rectores:

- **Public:** lo detectan primero los usuarios (monitorear calidad es difícil; algo que afecta a un slice pequeño el 100% del tiempo se diluye en el agregado).
- **Fuzzy:** difuso en impacto y tiempo; no hay transición nítida entre "malo" y "bueno", solo "mejor" y "no tan bueno".
- **Unbounded:** abarca un rango amplio de sistemas y de la organización.

## Historia 1 (búsqueda que no encuentra)

**Causa próxima:** el modelo de ranking llevaba **3 semanas congelado** (CTR de los top-5 cayendo, golden set "sospechosamente estable"). **Causa raíz:** los `log-feeders` se quedaban sin memoria y **crasheaban en bucle**, así el training nunca terminaba. Mitigación: subir de 10 a 20 log-feeders. **Lección:** en ML mal instrumentado, los problemas de sistemas se manifiestan **solo como caída de calidad** — a menudo la única señal end-to-end. **Follow-up:** alertar por **edad del modelo**, golden set (cambia demasiado *o* nada), **tasa de entrenamiento** y **CTR top-5** (horario).

## Preparación por rol

- **Data scientist:** lo más importante, **versionar todos los modelos y datos** (feature store versionado, procedencia, código de transformación, snapshots, versiones históricas listas-para-servir). Además: **fallback** aceptable y métricas independientes de la implementación.
- **Software engineer:** datos limpios con procedencia y mínimas copias; rollouts de **modelo y binario separables**; consistencia de features (anti-skew); herramientas de rollout/rollback.

## Ética durante el incidente

El **manifiesto del ingeniero ético de guardia**: es un error "arreglar primero y la privacidad después". Aunque haya que hacer análisis a medida o variantes del modelo, hay que **rechazar** peticiones que violen privacidad u otros principios. Y a veces la mejor mitigación está **fuera del sistema de ML** (Historia 3: mostrar "agotado" e invitar a avisar, en vez de seguir depurando el modelo).

---

## Mini-ejemplo trabajado: el modelo congelado 3 semanas (Historia 1)

Síntoma: la búsqueda "no encuentra"; el CTR de los top-5 lleva semanas cayendo y el *golden set* está "sospechosamente estable". Nadie ve un error en logs.

- **Causa próxima:** el modelo de ranking llevaba **3 semanas congelado** — no se reentrenaba.
- **Causa raíz:** los `log-feeders` se quedaban sin memoria y **crasheaban en bucle (OOM crash loop)**, así que el training nunca terminaba y el modelo nunca se actualizaba.
- **Mitigación:** subir de 10 a 20 log-feeders.

La lección clave: en un sistema de ML mal instrumentado, **un problema de sistemas se manifiesta solo como caída de calidad** — a menudo la única señal end-to-end. Por eso el *follow-up* añadió alertas por **edad del modelo**, golden set (que cambie *demasiado* o *nada* es malo), **tasa de entrenamiento** y **CTR top-5 por hora**.

**Predicción antes de seguir:** un bug afecta al 100% de un slice pequeño (digamos, búsquedas en coreano), pero la métrica **agregada** apenas se mueve. ¿Lo detecta el monitoreo agregado? No — por eso un incidente de ML es **Public** (lo ven antes los usuarios) y hay que mirar **slices**.

## Prototipo, contraejemplo y caso borde

- **Prototipo (incidente gestionado):** estado + roles (commander/comms/ops/planning) + registro → respuesta coordinada y postmortem.
- **Contraejemplo (incidente no gestionado):** un ingeniero depura en solitario, no mide impacto, no comunica, otros toman pasos descoordinados → el peor tipo.
- **Caso borde (mitigación fuera del ML):** la mejor respuesta puede ser de producto ("mostrar agotado e invitar a avisar"), no seguir tocando el modelo.

## Errores típicos

- **Conceptual:** creer que un problema de "calidad" es siempre del modelo; suele ser un fallo de sistemas que solo *se ve* como caída de calidad.
- **De ética:** "primero que funcione, la privacidad después" — la privacidad no se pospone, ni bajo presión.
- **De monitoreo:** no alertar por **frescura del modelo**/golden set → degradación silenciosa de semanas.

## Transferencia isomorfa

- **Roles de incidente ↔ Incident Command System (SRE):** commander/comms/ops/planning son invariantes entre incidentes de infra y de ML; solo Ops modifica el sistema (conecta con [[arena-sre3]]).
- **Caída de calidad como única señal ↔ fallo silencioso de ML:** un sistema que "se ajusta" a un dato roto sin lanzar error es el fallo silencioso de las Reglas de ML (conecta con [[arena-rom1]]).
- **Public/Fuzzy/Unbounded ↔ monitorear por slices y proxies:** que el daño se diluya en el agregado obliga a vigilar subgrupos, como en distribution shift (conecta con [[arena-dmls4]]).

Moraleja de la arista: *gestiona con estado+roles+registro; en ML el problema de sistemas se disfraza de caída de calidad, así que alerta por frescura del modelo y por slices — y nunca pospongas la privacidad.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Lo arreglo yo solo y luego aviso" | Es un incidente no gestionado: estado+roles+registro |
| "¿Quién manda en la caída?" | Incident commander; + comms, ops, planning |
| "La métrica agregada está bien" | Public: revisa slices, un subgrupo puede recibir 100% mal |
| "¿Cuándo empezó/terminó?" | Fuzzy: el timeline de ML es difuso, define criterios |
| "El modelo se degradó en silencio" | Alerta por edad del modelo, golden set, tasa de training, CTR |
| "Primero que funcione, la privacidad después" | No: ética y privacidad no se posponen |

---

> **Síntesis:** Gestiona el incidente con **estado + roles + registro**. Los cuatro roles (commander, comms, ops, planning) son invariantes; lo que cambia en ML es que es **Public, Fuzzy y Unbounded**. La caída **silenciosa de calidad** suele ser la única señal end-to-end, así que monitorea **frescura del modelo, golden set, tasa de training y métrica de usuario**. Prepárate **versionando modelos y datos** y con un **fallback**, y nunca pospongas la **privacidad** —ni siquiera bajo la presión del incidente.

---

*Retrieval: cierra y responde: (1) ¿qué es un incidente no gestionado?; (2) nombra las fases y los cuatro roles; (3) explica Public/Fuzzy/Unbounded; (4) ¿cuál fue la causa raíz de la Historia 1 y qué se monitoreó después?*
