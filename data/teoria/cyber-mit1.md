# Panorama estratégico: IA en ataque y defensa, y cuándo IA vs humanos

> Recurso troncal: **MIT — *AI and Cybersecurity: Strategies for Resilience and Defense*** (Módulos 1A y 2A). Apertura del cluster ejecutivo: complementa la mirada técnico-defensiva de [[cyber-ms1]] con la pregunta estratégica de *quién decide qué* entre humanos e IA. Prepara [[cyber-mit2]] (IA ofensiva).

## De qué trata (y qué sabrás hacer al final)

La IA no es "una herramienta más" de ciberseguridad: cambia **a la vez** el ataque y la defensa, y obliga a una decisión nueva —¿qué tareas delego a la IA y cuáles exigen juicio humano?—. Esta lección da el marco estratégico (nivel CTO/líder) para pensar esa doble cara sin caer ni en el tecno-optimismo ("la IA nos defenderá sola") ni en el pánico.

La intuición: la IA en ciberseguridad es como la electricidad cuando llegó a la industria: amplifica lo que ya hacías —para bien (más detección, más rápido) y para mal (ataques más baratos y a escala)—. La pregunta de un líder no es "¿uso IA?", sino "¿dónde amplifica mi defensa y dónde amplifica al atacante, y qué pongo en manos de una máquina vs de una persona?".

Al terminar podrás: (1) distinguir los **usos ofensivos y defensivos** de la IA; (2) ubicar dónde la IA **agrega valor** y dónde **introduce riesgo**; (3) diferenciar modelos **generativos / supervisados / no supervisados** por su rol; y (4) aplicar un **cuadrante de decisión humano-vs-IA**.

## La doble cara: la IA amplifica ataque y defensa

| | La IA potencia la DEFENSA | La IA potencia el ATAQUE |
|---|---|---|
| Detección | Anomalías a escala, correlación de señales ([[cyber-blue2]]) | Evasión adaptativa, malware polimórfico |
| Velocidad | Respuesta y triaje más rápidos ([[cyber-blue4]]) | Ataques automatizados, phishing masivo |
| Escala | Cubrir más telemetría con menos analistas | Deepfakes y vishing personalizados a miles ([[cyber-mit2]]) |

Moraleja estratégica: **toda capacidad de IA defensiva tiene un espejo ofensivo.** Asumir solo el lado bueno es el error de liderazgo más común.

## Dónde la IA agrega valor y dónde introduce riesgo

- **Valor:** tareas de **patrón a escala** —clasificar, correlacionar, priorizar alertas, resumir—. Donde el volumen supera a los humanos y el costo de un error individual es bajo y reversible.
- **Riesgo:** tareas de **juicio, contexto y consecuencia alta** —decidir bloquear producción, atribuir un incidente, aprobar una transacción—. Aquí la IA introduce riesgo si decide sola: alucina, es engañable ([[cyber-mls3]]) y no rinde cuentas.

La regla: usa IA para **ampliar la percepción** (ver más, más rápido) y reserva el **juicio con consecuencias** para humanos con la IA como copiloto.

## Tres familias de modelos y su rol

[CAJA NEGRA OK — no necesitas entrenar estos modelos, solo saber qué rol cumplen]
- **Supervisado:** aprende de ejemplos etiquetados → clasificar (spam/no spam, malicioso/benigno). Útil cuando tienes etiquetas históricas.
- **No supervisado:** halla estructura sin etiquetas → **detección de anomalías** (lo que no se parece a lo normal), base del blue team ([[cyber-blue2]]).
- **Generativo (LLMs, deepfakes):** produce contenido nuevo → asistentes defensivos… y también la materia prima del ataque ofensivo ([[cyber-mit2]]).

Saber la familia te dice qué esperar: un supervisado no detecta lo que nunca vio; un generativo puede inventar (alucinar).

## Mini-ejemplo trabajado: el cuadrante de decisión

Un SOC recibe 10,000 alertas/día. ¿Qué delega a la IA y qué al humano? Cruza **volumen** × **consecuencia del error**:

| | Consecuencia baja | Consecuencia alta |
|---|---|---|
| **Volumen alto** | **IA decide** (filtrar/triar alertas) | **IA propone, humano aprueba** (cerrar un sistema) |
| **Volumen bajo** | IA asiste (resumir un caso) | **Humano decide** (atribuir, comunicar a la junta) |

Predicción antes de seguir: ¿"aprobar una transferencia urgente que pide el CEO por video" cae en qué cuadrante? → consecuencia altísima → **humano + verificación**, jamás automatizado. (Eso es exactamente lo que falló en los casos de [[cyber-mit5]].)

## Prototipo, contraejemplo y caso borde

- **Prototipo:** triaje de alertas con IA (alto volumen, bajo costo de error) + escalamiento humano de las graves. La IA amplía, el humano juzga.
- **Contraejemplo (parece buen uso, no lo es):** dejar que la IA **apruebe pagos** o **bloquee producción** sola "porque es más rápida": consecuencia alta + engañable = riesgo inaceptable.
- **Caso borde:** un ataque diseñado para **explotar la automatización** (envenenar las señales para que la IA misma cierre tu sistema, un DoS asistido) — la automatización sin supervisión se vuelve superficie de ataque.

## Señales de reconocimiento

| Señal en una decisión | Jugada |
|---|---|
| "La IA lo hará sola, es más rápida" | ¿Consecuencia alta? → humano en el lazo |
| "Solo pensamos el lado defensivo" | Toda capacidad tiene espejo ofensivo |
| "Usamos IA para todo" | Reserva el juicio con consecuencias |
| Automatizar una acción irreversible | Riesgo: la automatización es superficie de ataque |

## Errores típicos

- **Tecno-optimismo:** creer que la IA defiende sola; olvida su espejo ofensivo y su falibilidad.
- **Delegar juicio de alta consecuencia:** automatizar decisiones que exigen contexto y rendición de cuentas.
- **Confundir velocidad con acierto:** la IA rápida y equivocada hace daño rápido.

## Transferencia isomorfa

El cuadrante humano-vs-IA es el mismo **least privilege / agencia mínima** de [[cyber-ms2]] y [[cyber-llm2]] aplicado a la autonomía: das a la IA el mínimo poder de decisión necesario, y exiges humano en el lazo para lo irreversible. Y "toda capacidad defensiva tiene espejo ofensivo" es la simetría que estructura todo el cluster: lo veremos hecho ataque en [[cyber-mit2]] y gobernado en [[cyber-mit3]].

## Práctica, misión externa y mini-entregable

- **Práctica interna:** ubica 4 tareas de tu trabajo en el cuadrante volumen × consecuencia y di cuáles delegarías a IA.
- **Misión externa (lab vivo):** explora el **NIST AI Risk Management Framework** (https://www.nist.gov/itl/ai-risk-management-framework) y ubica sus funciones Govern/Map/Measure/Manage. **Criterio de cierre:** explicar por qué la IA necesita gobierno propio, no solo el de IT.
- **Mini-entregable:** un cuadrante de decisión humano-vs-IA de un proceso real, con qué reservas siempre al humano.

---

> **Síntesis:** la IA **amplifica ataque y defensa a la vez** —toda capacidad defensiva tiene espejo ofensivo—. Agrega valor en tareas de **patrón a escala** (alto volumen, bajo costo de error) y **introduce riesgo** en el **juicio de alta consecuencia**, donde es engañable y no rinde cuentas. Decide con el **cuadrante volumen × consecuencia**: IA para ampliar la percepción, **humano en el lazo** para lo irreversible —la automatización sin supervisión es, ella misma, superficie de ataque—.

---

**Referencias**

- Massachusetts Institute of Technology. (n.d.). *AI and cybersecurity: Strategies for resilience and defense* (Module 1A, 2A). MIT Professional Education.
- National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1

*Retrieval: (1) ¿por qué "toda capacidad defensiva tiene espejo ofensivo"?; (2) ¿dónde agrega valor la IA y dónde introduce riesgo?; (3) rol de modelos supervisado/no supervisado/generativo; (4) ¿qué decide el cuadrante humano-vs-IA?*
