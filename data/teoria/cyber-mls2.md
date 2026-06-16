# Seguridad de ML II: ataques en inferencia, supply chain y controles

> Recurso troncal: **MITRE SAFE-AI** + **MITRE ATLAS**. Cierra [[cyber-mls1]]: el modelo ya está entrenado y desplegado; ahora lo atacan **a través de sus entradas y salidas**, y montamos controles.

## De qué trata (y qué sabrás hacer al final)

Un modelo en producción es una **superficie de ataque viva**: cualquiera que pueda enviarle entradas y ver sus salidas puede intentar engañarlo, copiarlo o extraerle secretos. Y como el modelo a menudo viene de terceros (preentrenados, *fine-tunes*, datasets públicos), también hereda riesgos de **procedencia**. Esta lección te da el catálogo de ataques de inferencia y, sobre todo, los **controles** y el **riesgo residual** con que se gobiernan.

La intuición: el modelo desplegado es como un experto que atiende consultas tras una ventanilla. Un adversario puede: mostrarle una **ilusión** cuidadosamente diseñada para que se equivoque (evasion); hacerle **miles de preguntas** para reconstruir su conocimiento y clonarlo (extraction); o formular preguntas astutas para que **revele** lo que vio en su formación (inversion / membership inference). No rompe la ventanilla; abusa del servicio legítimo.

Al terminar podrás: (1) nombrar **evasion, model extraction, model inversion y membership inference**; (2) razonar el riesgo de **compartir un modelo o sus embeddings**; (3) evaluar la **supply chain y provenance** de modelos; y (4) elegir **controles proporcionales** asumiendo riesgo residual.

## Los ataques de inferencia

| Ataque | El adversario… | Daño |
|---|---|---|
| **Evasion** (adversarial) | Diseña una entrada con perturbación mínima que el modelo clasifica mal | Burla un filtro/detector |
| **Model extraction** | Consulta masivamente para clonar el modelo | Robo de propiedad intelectual |
| **Model inversion** | Reconstruye rasgos de los datos de entrenamiento | Fuga de datos sensibles |
| **Membership inference** | Determina si un individuo estuvo en el entrenamiento | Fuga de privacidad (¿estuvo este paciente?) |

Los dos últimos conectan directo con [[cyber-data-privacy]]: un modelo puede **filtrar a las personas** con las que se entrenó, aunque el dataset nunca se publique. Por eso "el dataset es privado" no implica "el modelo es privado".

## Compartir modelos y embeddings: el riesgo oculto

- **Compartir un modelo** (pesos) habilita extraction/inversion offline y, si traía un backdoor ([[cyber-mls1]]), lo propaga.
- **Compartir embeddings** parece inocuo —"son solo números"— pero a menudo permiten **reconstruir** el texto/imagen original o inferir atributos sensibles. Un vector no es anónimo por ser un vector. (Reaparecerá como LLM08 en [[cyber-llm-rag-agents]].)

Regla: antes de exponer un modelo, una API de scoring o un store de embeddings, pregúntate qué podría **reconstruir o inferir** un consumidor malicioso, no solo qué quieres que haga.

## Supply chain y provenance del modelo

Casi nadie entrena desde cero: se usan modelos preentrenados y datasets públicos. Eso es **dependencia** ([[cyber-dev2]]) con esteroides. Preguntas de provenance: ¿de dónde viene este *checkpoint*? ¿quién lo publicó? ¿puedo **verificar su integridad** (hash/firma, [[cyber-sys2]])? ¿el dataset de origen pudo estar envenenado? Un modelo de origen desconocido es un binario no confiable que ejecutarás con tus datos.

## Controles proporcionales y riesgo residual

No hay modelo invulnerable; hay riesgo gestionado. Controles típicos (elegidos por riesgo, no todos a la vez):

- **Limitar la exposición:** rate limiting y autenticación de la API (frena extraction/inversion masivos), salidas con menos detalle (top-1 en vez de probabilidades finas).
- **Validar entradas y monitorear:** detección de patrones adversarios / consultas anómalas (detection engineering, [[cyber-blue2]]).
- **Privacidad en entrenamiento:** *differential privacy* / regularización para reducir memorización ([[cyber-dp2]]).
- **Procedencia:** verificar integridad de modelos y datos; preferir fuentes confiables.
- **Gobernanza:** documentar el modelo (model cards), su uso permitido y su **riesgo residual** aceptado.

## Mini-ejemplo trabajado: evaluar el despliegue de un clasificador médico

Vas a exponer una API que predice riesgo clínico, entrenada con datos de pacientes. Evaluación SAFE-AI-style:

- **Activos:** el modelo (IP + posible backdoor), los datos de entrenamiento (privacidad), la disponibilidad del servicio.
- **Ataques de inferencia:** *membership inference* (¿estuvo este paciente?) y *inversion* (reconstruir rasgos) → riesgo de privacidad alto.
- **Controles proporcionales:** autenticación + rate limiting, devolver categorías de riesgo (no probabilidades exactas), entrenamiento con DP, monitoreo de consultas anómalas, y verificación de procedencia de cualquier componente preentrenado.
- **Riesgo residual:** un adversario decidido con muchas consultas aún podría inferir algo; lo **aceptas explícitamente**, lo monitoreas, y lo documentas. No finges que llegó a cero.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| API de modelo sin auth ni rate limit | Extraction / inversion masivos |
| Devuelve probabilidades de altísima precisión | Facilita extraction e inversion |
| "Publicamos los embeddings, son anónimos" | Reconstrucción / inferencia de atributos |
| Checkpoint preentrenado sin verificar origen | Backdoor / poisoning heredado |
| Modelo con datos sensibles y acceso abierto | Membership inference |

## Errores típicos

- **"El dataset es privado, el modelo también":** el modelo puede filtrar a las personas del dataset.
- **Tratar embeddings como anónimos:** son reconstruibles/invertibles.
- **Perseguir invulnerabilidad:** el objetivo es **riesgo residual aceptable** con controles proporcionales, no cero ataques.

## Contraejemplo y caso borde

- **Contraejemplo:** una API de modelo con auth, rate limiting, salidas de baja resolución, entrenamiento con DP y monitoreo: sigue siendo atacable en teoría, pero el costo del ataque supera el beneficio → riesgo gestionado bien.
- **Caso borde:** un modelo **on-device** (en el dispositivo del usuario) da al adversario acceso total a los pesos: los controles de "limitar consultas" no aplican; debes asumir extraction y diseñar para ese supuesto.

## Transferencia a ciencia de datos e IA

Este es el corazón de la seguridad del trabajo de un DS: cada decisión de despliegue (qué exponer, con qué granularidad, de qué origen) es una decisión de seguridad. El threat model de cuatro preguntas ([[cyber-ms2]]), la verificación de integridad ([[cyber-sys2]]), la privacidad ([[cyber-data-privacy]]) y el monitoreo ([[cyber-blue2]]) convergen aquí. Y todo se extiende a sistemas con LLMs en [[cyber-llm-rag-agents]].

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el clasificador médico, ordena 4 controles por relación impacto/costo y justifica el riesgo residual que aceptarías.
- **Misión externa (lab vivo):** en **MITRE ATLAS** (https://atlas.mitre.org), localiza un estudio de caso de ataque a un sistema de IA real. **Criterio de cierre:** identificar qué control lo habría mitigado.
- **Mini-entregable:** una mini "model card de seguridad": activos, ataques de inferencia relevantes, controles, procedencia y riesgo residual aceptado.

---

> **Síntesis:** un modelo desplegado se ataca por sus **entradas y salidas**: **evasion** (engañarlo), **extraction** (clonarlo), **inversion** y **membership inference** (sacarle datos de entrenamiento). Compartir **modelos** o **embeddings** filtra más de lo que parece, y la **supply chain/provenance** importa porque casi nadie entrena desde cero. Se gobierna con **controles proporcionales** (auth, rate limiting, baja resolución de salida, DP, monitoreo, verificación de origen) aceptando un **riesgo residual** explícito.

---

**Referencias**

- Kressel, J., Perrella, R., Reed, E., Naik, N., Sidhu, J., Hu, Q., Booker, L., Cintron, J., & Huffner, L. (2025). *SAFE-AI: A framework for securing AI-enabled systems*. The MITRE Corporation.
- MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org

*Retrieval: (1) define evasion, extraction, inversion y membership inference; (2) ¿por qué los embeddings no son anónimos?; (3) ¿qué preguntas de provenance haces a un modelo preentrenado?; (4) ¿por qué el objetivo es riesgo residual y no invulnerabilidad?*
