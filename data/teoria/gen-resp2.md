# Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS

> Recurso troncal: **MIT-AI.md ("Frameworks and Tools": MITRE ATLAS, AI Secure-by-Design Executive Framework, MIT AI Risk Taxonomy, NIST AI RMF)**. Cómo se operacionaliza la IA responsable ([[gen-resp1]]) en procesos. Conecta con la gobernanza de seguridad ([[cyber-mit3]], [[cyber-mls5]]). Prepara [[gen-resp3]] (producción).

## De qué trata (y qué sabrás hacer al final)

Saber qué es la IA responsable ([[gen-resp1]]) no basta; hay que **operacionalizarla** —convertir principios en procesos, roles y controles repetibles—. Para eso existen **frameworks**: mapas que la industria y los gobiernos crearon para que las organizaciones gestionen el riesgo de IA sin reinventar la rueda. Esta lección te da los cuatro que MIT-AI.md cita, qué hace cada uno, y cuándo usarlos — para que no sean siglas vacías.

La intuición: los frameworks son como los **códigos de construcción** de un edificio. No te dicen qué edificio hacer, pero te dan los estándares probados (estructura, incendios, accesibilidad) para que no se caiga ni mate a nadie, y un lenguaje común para que arquitecto, ingeniero e inspector se entiendan. Sin código cada quien improvisa; con código, hay un piso mínimo y rendición de cuentas.

Al terminar podrás: (1) ubicar el **NIST AI RMF** (Govern/Map/Measure/Manage); (2) explicar **AI Secure-by-Design**; (3) saber qué cataloga **MITRE ATLAS** y la **MIT AI Risk Taxonomy**; y (4) elegir el framework según la pregunta.

## NIST AI RMF: gestionar el riesgo de IA

El **[NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)** (AI 100-1) es el marco de referencia para gestionar riesgo de IA, organizado en cuatro funciones:
- **Govern:** cultura, roles, políticas, rendición de cuentas (la base que envuelve todo).
- **Map:** entender el contexto y **identificar** los riesgos del sistema en su uso.
- **Measure:** **evaluar** y cuantificar esos riesgos (sesgo, robustez, privacidad, desempeño).
- **Manage:** **priorizar y tratar** los riesgos, asignar recursos, monitorear.

Es el equivalente, para IA, del Cybersecurity Framework de [[cyber-ms1]]. Su valor: da un **lenguaje y proceso comunes** para que un sistema de IA tenga riesgos mapeados, medidos, gestionados y con un dueño — lo que [[cyber-mit3]] llamaba gobernanza. Es voluntario pero se está volviendo estándar de facto y base de regulación.

## AI Secure-by-Design (Executive Framework)

Lleva el principio de [[cyber-dev3]] (la seguridad se diseña, no se parchea) al nivel **ejecutivo y a todo el ciclo de vida de la IA**: integrar seguridad, gobernanza y ética desde el encuadre hasta el retiro, con **alineación interfuncional** (seguridad, legal, datos, negocio decidiendo juntos) y responsabilidad de los líderes técnicos. No es un control puntual sino una postura: que cada decisión de diseño de un sistema de IA pase por seguridad/ética **antes**, no como auditoría final. Es la operacionalización ejecutiva de [[cyber-mit3]].

## MITRE ATLAS: el "ATT&CK de la IA"

**[MITRE ATLAS](https://atlas.mitre.org)** cataloga **tácticas y técnicas reales de ataque contra sistemas de IA/ML** (data poisoning, evasión, model extraction, inversión, ataques a la cadena de suministro de modelos…) con casos de estudio. Es a la IA lo que ATT&CK ([[cyber-blue1]]) a la seguridad clásica: un mapa de amenazas con el que mapear tu cobertura, emular ataques ([[cyber-blue5]]) y cerrar brechas. Donde el AI RMF te dice **cómo gobernar** el riesgo, ATLAS te dice **qué ataques** existen — se complementan (visto en [[cyber-mls5]]).

## MIT AI Risk Taxonomy

La **[MIT AI Risk Repository / Taxonomy](https://airisk.mit.edu/)** es una recopilación estructurada de **cientos de riesgos de IA** documentados (de cientos de marcos y papers), clasificados por causa (¿humano o IA?, ¿intencional?, ¿cuándo?) y por dominio (discriminación, desinformación, malos usos, seguridad, impacto socioeconómico…). Su utilidad: un **catálogo exhaustivo** para no olvidar categorías de riesgo al hacer el *Map* del AI RMF — una checklist para que tu análisis no tenga puntos ciegos.

## Cómo encajan (no compiten, se complementan)

| Pregunta | Framework |
|---|---|
| ¿Cómo **gobierno** el riesgo de IA de extremo a extremo? | NIST AI RMF (Govern/Map/Measure/Manage) |
| ¿Cómo integro seguridad/ética en **todo el ciclo**, a nivel ejecutivo? | AI Secure-by-Design |
| ¿Qué **ataques** existen contra sistemas de IA? | MITRE ATLAS |
| ¿Qué **categorías de riesgo** podría estar olvidando? | MIT AI Risk Taxonomy |

Usados juntos: el AI RMF da el proceso, Secure-by-Design la postura, ATLAS las amenazas técnicas y la MIT Taxonomy la exhaustividad del mapeo.

## Mini-ejemplo trabajado

Vas a desplegar un asistente clínico con LLM + RAG. Operacionalizar con frameworks:
- **Govern (AI RMF):** define un dueño, un comité que aprueba el caso de uso, políticas de uso.
- **Map:** identifica riesgos usando la **MIT Risk Taxonomy** como checklist (sesgo clínico, privacidad de pacientes, alucinación, mal uso) y **ATLAS** para amenazas técnicas (poisoning del corpus, inyección por RAG).
- **Measure:** evalúa sesgo por subgrupo, faithfulness ([[gen-eval3]]), robustez a inyección (red teaming).
- **Manage:** controles proporcionales (anclaje, humano en el lazo, monitoreo), riesgo residual documentado.
- **Secure-by-Design:** todo esto decidido **desde el diseño**, con legal y clínicos en la mesa.

Predicción antes de seguir: el equipo dice "ya leímos los frameworks, estamos cubiertos". ¿Basta leerlos? → No: un framework **no aplicado** es un PDF. La gobernanza es roles, métricas y evidencia ([[cyber-mit3]]: tener política ≠ tener control); los frameworks son el mapa, no el viaje.

## Señales de reconocimiento

| Señal | Framework / jugada |
|---|---|
| "Necesito un proceso de gestión de riesgo de IA" | NIST AI RMF |
| "La seguridad de IA se revisa al final" | Falta AI Secure-by-Design |
| "¿De qué ataques de IA me defiendo?" | MITRE ATLAS |
| "¿Qué riesgos podría estar olvidando?" | MIT AI Risk Taxonomy |
| "Leímos los frameworks, ya está" | Framework sin aplicar = PDF |

## Errores típicos

- **Tratar los frameworks como burocracia o como casilla:** son mapas para no olvidar nada y hablar un lenguaje común; aplicarlos es lo que cuenta.
- **Confundir cuál usar:** AI RMF (proceso) ≠ ATLAS (amenazas) ≠ Risk Taxonomy (catálogo); se complementan.
- **Adoptar un framework sin dueño ni métricas:** sin rendición de cuentas, es teatro de gobernanza ([[cyber-mit3]]).
- **Creer que un framework garantiza seguridad/equidad:** reduce puntos ciegos, no elimina el trabajo.

## Contraejemplo y caso borde

- **Contraejemplo (framework que da valor):** una organización que usa el AI RMF para mapear, medir y gestionar el riesgo de cada sistema de IA, con dueños y model cards: cuando algo falla, sabe quién responde y con qué evidencia. El framework convirtió principios en práctica.
- **Caso borde (framework como escudo):** una empresa "cumple" un framework en el papel pero sigue desplegando un modelo sesgado — usa el framework como **escudo de responsabilidad**, no como mejora real. El cumplimiento formal sin sustancia es un riesgo en sí (eco de "principios éticos sin auditoría", [[cyber-mit3]]).

## Transferencia isomorfa

- **AI RMF ↔ Cybersecurity Framework:** mismo patrón Identify/Protect…→Govern/Map/Measure/Manage; un marco de funciones para gestionar riesgo, aplicado a IA ([[cyber-ms1]]).
- **ATLAS ↔ ATT&CK:** catálogo de tácticas/técnicas adversarias para mapear cobertura y emular ([[cyber-blue1]], [[cyber-blue5]]).
- **Risk Taxonomy ↔ checklist anti-puntos-ciegos:** una lista exhaustiva para que el análisis no olvide categorías, como el OWASP Top 10 es un mapa para interrogar ([[cyber-web3]]).

Moraleja de la arista: *los frameworks operacionalizan la IA responsable —AI RMF (gobernar), Secure-by-Design (postura), ATLAS (amenazas), MIT Taxonomy (catálogo)— pero un framework no aplicado es un PDF; el valor está en roles, métricas y evidencia.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para un sistema de IA que conozcas, asigna a cada framework una pregunta concreta que te ayudaría a responder.
- **Misión externa (lab vivo):** explora el [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [MITRE ATLAS](https://atlas.mitre.org) y el [MIT AI Risk Repository](https://airisk.mit.edu/). **Criterio de cierre:** mapear un riesgo concreto de un sistema a una función del AI RMF y a una técnica de ATLAS.
- **Mini-entregable:** un plan de gobernanza de un sistema de IA usando el AI RMF (Govern/Map/Measure/Manage), citando dónde usarías ATLAS y la MIT Taxonomy.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (frameworks de riesgo: Govern, Map, Measure y Manage) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** usar AI RMF y MIT AI Risk Repository para crear controles verificables.
2. **Baseline obligatorio:** checklist informal sin duenos ni evidencias.
3. **Versión mejorada:** gobierno operativo con medicion continua y responsables.
4. **Evaluación:** riesgos con dueno, controles probados y incidentes detectados.
5. **Fallo que debes explicar:** riesgos conocidos quedan sin dueno hasta que aparecen en producción.
6. **Transferencia:** comités de producto, seguridad y cumplimiento con lenguaje compartido.

**Laboratorio externo principal:** [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).
**Laboratorio alternativo:** [MIT AI Risk Repository](https://airisk.mit.edu/).
**Ruta de cluster:** diseño extremo a extremo para un vertical con evaluación, seguridad, gobierno y operación.

**Entregable:** risk register con controles, evidencias y cadencia de revisión. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y que harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** los **frameworks** operacionalizan la IA responsable en procesos repetibles. El **NIST AI RMF** (Govern/Map/Measure/Manage) gobierna el riesgo de extremo a extremo (el CSF para IA); **AI Secure-by-Design** integra seguridad/ética en todo el ciclo a nivel ejecutivo; **MITRE ATLAS** cataloga los **ataques** contra IA (el ATT&CK de la IA); y la **MIT AI Risk Taxonomy** es un **catálogo exhaustivo** de riesgos para no tener puntos ciegos. No compiten: AI RMF da el proceso, Secure-by-Design la postura, ATLAS las amenazas, la Taxonomy la exhaustividad. Pero **un framework no aplicado es un PDF**: el valor está en roles, métricas, evidencia y un dueño.

---

**Referencias**

- National Institute of Standards and Technology. (2023). *AI risk management framework (AI RMF 1.0)* (NIST AI 100-1). [nist.gov](https://www.nist.gov/itl/ai-risk-management-framework) · [DOI](https://doi.org/10.6028/NIST.AI.100-1)
- MITRE. (n.d.). *MITRE ATLAS*. [atlas.mitre.org](https://atlas.mitre.org)
- Slattery, P., et al. (2024). The AI Risk Repository. *MIT*. [airisk.mit.edu](https://airisk.mit.edu/) · [arXiv:2408.12622](https://arxiv.org/abs/2408.12622)
- Kressel, J., et al. (2025). SAFE-AI: A framework for securing AI-enabled systems. *MITRE*.

*Retrieval: (1) ¿qué cuatro funciones tiene el NIST AI RMF?; (2) ¿qué es AI Secure-by-Design?; (3) ¿qué cataloga ATLAS vs la MIT Risk Taxonomy?; (4) ¿por qué "un framework no aplicado es un PDF"?*
