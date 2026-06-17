# Supply chain de modelos, gobernanza y AI RMF

> Recurso troncal: **MITRE SAFE-AI / MITRE ATLAS** + **NIST AI RMF**. Capstone del cluster de ML security: de los ataques puntuales a **gobernar** la seguridad de un sistema de IA de extremo a extremo. Integra [[cyber-mls1]]–[[cyber-mls4]] y prepara el mini-proyecto.

## De qué trata (y qué sabrás hacer al final)

Has visto ataques al entrenamiento ([[cyber-mls1]]), a la inferencia ([[cyber-mls3]], [[cyber-mls4]]) y a la privacidad. Ahora falta lo que une todo: la **supply chain** del modelo (de dónde vienen datos, modelos y librerías) y la **gobernanza** que decide, documenta y mantiene los controles. Un sistema de IA seguro no es una colección de defensas sueltas: es un proceso gestionado, como propone el **NIST AI Risk Management Framework**.

La intuición: construir un sistema de IA es como montar un platillo con ingredientes de muchos proveedores (datos, modelos preentrenados, librerías). La seguridad depende de la **procedencia** de cada ingrediente y de un **proceso de cocina** documentado (quién verifica qué, qué se permite, qué riesgo se acepta). Sin proceso, cada defensa individual se erosiona y nadie sabe el estado real.

Al terminar podrás: (1) evaluar la **supply chain y provenance** de modelos y datos; (2) ubicar **NIST AI RMF** y **MITRE ATLAS** como marcos; (3) razonar **riesgo residual** y documentación (model cards); y (4) ejecutar el mini-proyecto del cluster.

## Supply chain de IA: datos, modelos y librerías

Casi nadie entrena desde cero: usas **datasets públicos**, **modelos preentrenados** y **librerías** (que arrastran su propia supply chain, [[cyber-dev2]]). Cada uno es una dependencia con riesgo:

- **Datos de terceros:** pueden estar **envenenados** ([[cyber-mls1]]) o tener problemas de privacidad/licencia.
- **Modelos preentrenados:** pueden traer **backdoors** ([[cyber-mls1]]) y, según el formato, **ejecutar código al cargarse** ([[cyber-web5]], ¡pickle!).
- **Provenance:** ¿de dónde vino este checkpoint? ¿quién lo publicó? ¿puedo **verificar su integridad** (hash/firma, [[cyber-sys2]])?

Un modelo de origen desconocido es un binario no confiable que ejecutarás con tus datos. La verificación de procedencia es a la IA lo que el SBOM/SCA al software.

## Marcos: NIST AI RMF y MITRE ATLAS

- **NIST AI RMF:** un marco para **gestionar** el riesgo de sistemas de IA en cuatro funciones —*Govern* (cultura y proceso), *Map* (contexto y riesgos), *Measure* (evaluar) y *Manage* (priorizar y tratar)—. Da el lenguaje para hacer la seguridad de IA un proceso, no una ocurrencia (paralelo al CSF de [[cyber-ms1]]).
- **MITRE ATLAS:** el "ATT&CK de la IA": un catálogo de tácticas y técnicas reales contra sistemas de ML, para mapear amenazas, emular ([[cyber-blue5]]) y cerrar brechas.

Juntos: ATLAS te dice **qué ataques existen**; AI RMF te dice **cómo gobernar** el riesgo de extremo a extremo.

## Gobernanza, model cards y riesgo residual

La seguridad de IA se documenta y mantiene, no se "logra una vez":

- **Model card de seguridad:** activos (datos, pesos, embeddings), amenazas relevantes (entrenamiento/inferencia/supply chain), controles aplicados, procedencia y **riesgo residual aceptado**.
- **Monitoreo:** consultas anómalas, drift, intentos de evasión ([[cyber-blue2]]).
- **Ciclo de vida:** reevaluar al reentrenar o cambiar el contexto; un control de hace seis meses puede tener una brecha hoy ([[cyber-blue5]]).

El objetivo, como siempre, es **riesgo residual aceptable** ([[cyber-ms5]]), explícito y vigilado, no invulnerabilidad.

## Mini-ejemplo trabajado

Vas a desplegar un sistema de scoring de fraude que usa un modelo preentrenado descargado de un repo público y se reentrena con datos de un proveedor externo. Gobernanza tipo AI RMF:

- **Map (contexto/riesgos):** activos = modelo, datos del proveedor, API; amenazas = poisoning del proveedor ([[cyber-mls1]]), backdoor/ejecución del checkpoint ([[cyber-web5]]), extraction/evasion en inferencia ([[cyber-mls3]], [[cyber-mls4]]).
- **Measure:** verificar integridad/origen del checkpoint; evaluación adversaria de robustez; auditoría de las etiquetas del proveedor.
- **Manage:** usar formato sin ejecución (safetensors) o cargar aislado ([[cyber-sys4]]); limitar la influencia de fuentes no confiables; salida de baja resolución + rate limiting; monitoreo.
- **Govern:** una model card con controles y riesgo residual; reevaluación periódica.
- **Resultado:** no una defensa suelta, sino un sistema cuyo riesgo está mapeado, medido, gestionado y documentado.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| Checkpoint preentrenado sin verificar origen | Backdoor / ejecución / poisoning heredado |
| Reentrenar con datos de terceros sin auditar | Data poisoning por el proveedor |
| Cargar modelos con pickle de fuentes no confiables | Ejecución de código ([[cyber-web5]]) |
| Sin model card ni riesgo residual documentado | Gobernanza ausente; estado real desconocido |
| Controles "una vez" sin reevaluar | Brechas que aparecen al cambiar el sistema |

## Errores típicos

- **Confiar en un modelo por ser popular:** la popularidad no es procedencia verificada (igual que las dependencias, [[cyber-dev2]]).
- **Tratar la seguridad de IA como defensas sueltas:** sin gobernanza, se erosionan y nadie sabe el estado.
- **Documentar capacidades pero no riesgos:** una model card sin riesgo residual es marketing, no gobernanza.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** verificas la provenance e integridad de un modelo preentrenado, mapeas sus ataques con MITRE ATLAS y gobiernas el riesgo con NIST AI RMF y una model card de seguridad.
- **Contraejemplo:** un sistema con procedencia verificada de datos y modelos, evaluación adversaria, controles proporcionales, model card y reevaluación periódica: el riesgo está gestionado de extremo a extremo y es comunicable.
- **Caso borde:** verificar la integridad de un checkpoint (hash correcto) prueba que **no fue alterado tras publicarse**, pero **no** que el publicador no le puso un backdoor de origen; provenance incluye **confiar en la fuente**, no solo en el hash. Integridad ≠ confiabilidad del origen.

## Transferencia a ciencia de datos e IA

Este capstone integra toda la ruta aplicada a IA: supply chain ([[cyber-dev2]]), ejecución de código al cargar ([[cyber-web5]]), aislamiento ([[cyber-sys4]]), privacidad ([[cyber-dp5]]), detección/emulación ([[cyber-blue2]], [[cyber-blue5]]) y comunicación de riesgo ([[cyber-ms5]]). Gobernar la seguridad de un sistema de IA **es** aplicar toda la ciberseguridad al objeto "modelo". Continúa en [[cyber-llm-rag-agents]] para LLMs.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el sistema de fraude, escribe su model card de seguridad (activos, amenazas, controles, procedencia, riesgo residual).
- **Misión externa (lab vivo):** revisa **MITRE ATLAS** (https://atlas.mitre.org) y, si puedes, el **NIST AI RMF**. **Criterio de cierre:** mapear una amenaza de ATLAS a una función del AI RMF (Map/Measure/Manage).
- **Mini-entregable (mini-proyecto del cluster):** un **threat model y evaluación de controles de un pipeline ML** (clasificación médica, scoring financiero, fraude, recomendación o priorización): ataques de entrenamiento/inferencia/supply chain, controles proporcionales, procedencia y riesgo residual. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** la seguridad de un sistema de IA no son defensas sueltas sino un **proceso gobernado**. La **supply chain** (datos, modelos preentrenados, librerías) exige verificar **provenance** porque trae poisoning, backdoors y hasta ejecución de código al cargar. **MITRE ATLAS** cataloga los ataques; el **NIST AI RMF** (Govern/Map/Measure/Manage) gobierna el riesgo de extremo a extremo, documentado en una **model card** con **riesgo residual** explícito y reevaluado en el tiempo. Integridad de un checkpoint ≠ confianza en su origen.

---

**Referencias**

- Kressel, J., Perrella, R., Reed, E., Naik, N., Sidhu, J., Hu, Q., Booker, L., Cintron, J., & Huffner, L. (2025). *SAFE-AI: A framework for securing AI-enabled systems*. The MITRE Corporation.
- National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1
- MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org

*Retrieval: (1) ¿qué riesgos trae la supply chain de IA (datos/modelos/librerías)?; (2) ¿qué aportan ATLAS y NIST AI RMF respectivamente?; (3) ¿qué lleva una model card de seguridad?; (4) ¿por qué integridad de un checkpoint no es confianza en el origen?*
