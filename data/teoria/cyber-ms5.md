# Resiliencia y comunicación del riesgo: defensa proporcional y hablar con el equipo

> Recurso troncal: **Anderson, *Security Engineering* (3.ª ed.)**. Capstone del cluster de mentalidad: integra [[cyber-ms1]]–[[cyber-ms4]] en la capacidad de **decidir y comunicar** la seguridad. Prepara el mini-proyecto del cluster.

## De qué trata (y qué sabrás hacer al final)

Saber de amenazas no sirve si no puedes **priorizar** la defensa y **convencer** a un equipo de adoptarla. Dos habilidades cierran el cluster: diseñar para la **resiliencia** (que el sistema sobreviva y se recupere de fallos, no que sea infalible) y **comunicar el riesgo** de forma que un equipo no experto actúe. La excelencia en seguridad se siente como oficio: criterio claro, comunicado con sobriedad.

La intuición: un sistema resiliente es como un cuerpo sano —no inmune a todo, sino capaz de detectar la infección, contenerla y recuperarse—. Y comunicar riesgo es como un buen diagnóstico médico: ni minimizar ("no es nada") ni aterrar ("te vas a morir"), sino explicar con claridad qué está en juego y qué conviene hacer.

Al terminar podrás: (1) diseñar para **resiliencia** (detectar, contener, recuperar) más allá de la prevención; (2) elegir **defensa proporcional** al riesgo; (3) **comunicar riesgo** a un equipo técnico sin alarmismo; y (4) ejecutar el **mini-proyecto** del cluster.

## Resiliencia: más allá de prevenir

Como ningún sistema es impenetrable ([[cyber-ms2]], riesgo residual), el objetivo no es "que nunca pase" sino "que cuando pase, duela poco y se arregle rápido". Tres capacidades:

- **Detectar:** ver el fallo a tiempo (telemetría, monitoreo — base de [[cyber-blue1]]).
- **Contener:** que un fallo no se propague (aislamiento, least privilege, segmentación — [[cyber-ms2]], [[cyber-sys1]]).
- **Recuperar:** respaldos verificados, planes de respuesta, capacidad de revertir.

La prevención reduce la probabilidad; la resiliencia reduce el **impacto**. Una buena postura invierte en ambas, porque la prevención perfecta no existe.

## Defensa proporcional

No todo activo merece la misma inversión ([[cyber-ms3]]). Defensa proporcional = el costo y la fricción del control guardan relación con el riesgo (probabilidad × impacto) del activo que protege. Sobre-proteger un no-activo desperdicia recursos y genera fricción evitable; sub-proteger un activo crítico es negligencia. El arte es **asignar un presupuesto finito** donde más rinde.

## Comunicar el riesgo

Un análisis brillante que nadie entiende no cambia nada. Para comunicar a un equipo técnico (o a una gerencia):

- **Habla de activos e impacto, no de jerga:** "si esto se filtra, exponemos datos de 50 000 personas y arriesgamos una multa", no "hay un CVE 9.8".
- **Prioriza:** presenta los pocos riesgos que concentran el daño, no una lista de 200.
- **Propón acción proporcional:** por cada riesgo, una mitigación con su costo y su tradeoff.
- **Sé sobrio:** sin alarmismo ni minimización; el tono es de oficio, no de espectáculo (Constitución del proyecto).
- **Nombra el riesgo residual:** qué queda aún tras mitigar y por qué es aceptable.

## Mini-ejemplo trabajado

Detectas que el dataset de pacientes está en un bucket con acceso amplio y sin logs. ¿Cómo lo comunicas y resuelves?

- **Riesgo en términos de impacto:** "Cualquier cuenta del equipo puede descargar datos de pacientes y no quedaría registro: una fuga sería invisible y nos expone a daño a personas y a sanción."
- **Proporcionalidad:** es activo crítico (datos sensibles) → justifica inversión: acceso mínimo por persona, logs de acceso, alerta por descarga anómala.
- **Resiliencia:** aunque cerremos el acceso (prevención), añadimos detección (logs + alerta de volumen, [[cyber-blue2]]) y un plan de respuesta si se dispara.
- **Comunicación:** una página: el riesgo en una frase, 3 acciones priorizadas con su costo, y el riesgo residual aceptado. Sin culpar a nadie; enfocado en mejorar el sistema.

## Señales de reconocimiento

| Señal | Jugada |
|---|---|
| Todo el presupuesto en prevención, nada en detección/recuperación | Falta resiliencia |
| Mismo nivel de control para todo | Falta proporcionalidad |
| El reporte de riesgo es jerga o una lista de 200 ítems | Comunica por impacto y prioriza |
| "Esto es catastrófico" / "esto no es nada" | Alarmismo o minimización; busca el tono sobrio |

## Errores típicos

- **Confundir prevención con seguridad:** sin detección ni recuperación, el primer fallo es invisible y permanente.
- **Comunicar en jerga técnica:** el equipo no actúa sobre un CVSS; actúa sobre "qué se pierde".
- **Listar todo sin priorizar:** ahoga la señal; tres riesgos accionables valen más que doscientos.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** ante un activo de bajo valor aplicas un control ligero y ante uno crítico defensa en profundidad, comunicando el riesgo por impacto y nombrando el residual aceptado.
- **Contraejemplo:** un equipo que tras un casi-incidente documenta detección + plan de recuperación y comunica el riesgo en una página accionable: la próxima vez el daño se contiene. Resiliencia + comunicación en acción.
- **Caso borde:** comunicar de más (cada riesgo menor escalado a gerencia) genera fatiga y se ignora todo, igual que la fatiga de alertas ([[cyber-blue2]]). La proporcionalidad también aplica a la comunicación.

## Transferencia a ciencia de datos e IA

Comunicar riesgo es parte del oficio del DS de producto; la resiliencia es el **monitoreo y respuesta** de un sistema ML ([[cyber-blue2]], [[cyber-ml-security]]); y la defensa proporcional es cómo eliges controles para un modelo o un asistente RAG sin paralizar el producto ([[cyber-llm-rag-agents]]). Este cluster te dio el criterio que gobierna todos los demás.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** toma un riesgo real y redáctalo en una frase de impacto + 3 acciones priorizadas con tradeoff.
- **Misión externa (lab vivo):** en el **NIST CSF** (https://www.nist.gov/cyberframework), recorre *Detect / Respond / Recover* y relaciónalas con detectar/contener/recuperar. **Criterio de cierre:** explicar por qué prevención sin recuperación es frágil.
- **Mini-entregable (mini-proyecto del cluster):** un **threat model de una app de ciencia de datos** (notebooks, Supabase, API keys, datasets sensibles, modelos entrenados, dashboards): activos, amenazas, mitigaciones proporcionales, señales de detección y un párrafo de comunicación a tu equipo. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** como la prevención perfecta no existe, diseña para **resiliencia** (detectar, contener, recuperar) y aplica **defensa proporcional** (controla según el riesgo del activo). Y como el mejor análisis no sirve si nadie actúa, **comunica el riesgo** en términos de activos e impacto, priorizado, con acciones proporcionales, tono sobrio y riesgo residual explícito. Ese criterio integrador gobierna toda la ruta de ciberseguridad.

---

**Referencias**

- Anderson, R. (2020). *Security engineering: A guide to building dependable distributed systems* (3rd ed.). Wiley.
- National Institute of Standards and Technology. (2018). *Framework for improving critical infrastructure cybersecurity* (v1.1). https://www.nist.gov/cyberframework

*Retrieval: (1) ¿qué tres capacidades define la resiliencia?; (2) ¿qué es defensa proporcional?; (3) ¿cómo se comunica un riesgo a un equipo no experto?; (4) ¿por qué prevención sin detección/recuperación es frágil?*
