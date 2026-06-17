# Gobernanza de IA: GRC, roles ejecutivos y Secure-by-Design

> Recurso troncal: **MIT — *AI and Cybersecurity*** (Módulo 2B). Lleva la seguridad de IA del control técnico ([[cyber-mls5]]) al **gobierno organizacional**. Conecta con la comunicación de riesgo de [[cyber-ms5]].

## De qué trata (y qué sabrás hacer al final)

Los controles técnicos no bastan si nadie es **responsable** de la IA, si no hay reglas claras de uso, ni rendición de cuentas. La **gobernanza de IA** es el conjunto de estructuras, roles y procesos que hacen que una organización use IA de forma segura, ética y conforme a la ley —más allá del gobierno tradicional de IT, porque la IA trae riesgos propios (sesgo, alucinación, opacidad, datos de entrenamiento)—.

La intuición: tener modelos potentes sin gobernanza es como tener autos veloces sin reglas de tránsito, licencias ni responsables: el accidente es cuestión de tiempo y nadie sabe quién responde. La gobernanza es ese sistema de reglas, licencias y responsabilidades que permite ir rápido **sin** estrellarse —y saber a quién rendir cuentas cuando algo sale mal—.

Al terminar podrás: (1) explicar por qué la IA necesita gobierno **propio**, no solo el de IT; (2) ubicar **GRC** (gobernanza, riesgo, cumplimiento) aplicado a IA; (3) entender **Secure-by-Design** para IA; y (4) identificar **roles ejecutivos** y rendición de cuentas.

## Por qué la IA necesita gobierno propio

El gobierno de IT clásico asume software **determinista** (mismo input → mismo output, auditable línea por línea). La IA rompe esos supuestos:

- Es **probabilística** (puede alucinar, equivocarse de formas nuevas).
- Depende de **datos** cuya calidad y sesgo determinan su conducta ([[cyber-mls1]]).
- Es **opaca** (cuesta explicar por qué decidió algo — interpretabilidad).
- Aprende y **deriva** con el tiempo ([[cyber-blue5]]).

Por eso necesita controles específicos: validación de datos y modelos, monitoreo de deriva, evaluación de sesgo, y reglas sobre qué decisiones puede tomar (el cuadrante de [[cyber-mit1]]).

## GRC aplicado a IA

**[CAJA NEGRA OK — entiende los tres roles, no la teoría regulatoria completa]**
- **Gobernanza (G):** ¿quién decide y responde? Estructuras, roles, políticas de uso de IA.
- **Riesgo (R):** ¿qué puede salir mal y cuánto importa? Identificar, medir y tratar los riesgos de IA (el AI RMF de [[cyber-mls5]]: Map/Measure/Manage).
- **Cumplimiento (C):** ¿cumplimos leyes y normas? Privacidad ([[cyber-data-privacy]]), regulación de IA, auditoría.

GRC convierte "deberíamos usar IA con cuidado" en responsabilidades, métricas y evidencias concretas.

## Secure-by-Design para IA

El principio de [[cyber-dev3]] (la seguridad se diseña, no se parchea) aplicado a IA: integrar seguridad, gobernanza y ética **a lo largo de todo el ciclo de vida** del sistema de IA —encuadre, datos, entrenamiento, despliegue, monitoreo, retiro—, no como una revisión final. Significa, p. ej.: decidir desde el diseño qué datos entran (privacidad, [[cyber-dp5]]), qué decisiones delega el modelo (autonomía mínima), cómo se monitorea y quién aprueba su puesta en producción. Promueve **alineación interfuncional**: seguridad, legal, datos y negocio decidiendo juntos, no en silos.

## Roles ejecutivos y rendición de cuentas

La gobernanza falla sin un **dueño**. Roles típicos: un responsable de IA/seguridad (a veces un Chief AI Officer o el CISO ampliado) que rinde cuentas por el riesgo de IA; comités interfuncionales que aprueban casos de uso de alto riesgo; y dueños por sistema que mantienen su model card y su riesgo residual ([[cyber-mls5]]). La pregunta de gobernanza por excelencia: *"si este sistema de IA causa daño mañana, ¿quién responde y con qué evidencia demuestra que actuó con diligencia?"*

## Mini-ejemplo trabajado

Un banco quiere desplegar un modelo de scoring crediticio. Sin gobernanza vs con gobernanza:

- **Sin gobernanza:** un equipo lo entrena con datos históricos y lo lanza. Meses después se descubre que discrimina por código postal (sesgo heredado, [[cyber-mls1]]); nadie sabe quién aprobó el uso, no hay registro de las decisiones, y enfrentan una sanción. Cero rendición de cuentas.
- **Con gobernanza (Secure-by-Design + GRC):** desde el diseño se define el caso de uso, se evalúa sesgo y privacidad (Map/Measure), un comité interfuncional lo aprueba, se documenta una model card con riesgo residual, se monitorea la deriva, y un responsable rinde cuentas. Si algo falla, hay evidencia de diligencia y un dueño claro.

Predicción: ¿qué habría evitado la sanción —un mejor modelo o mejor gobernanza? → la **gobernanza**: el problema no fue técnico, fue de proceso y responsabilidad.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** un caso de uso de IA de alto riesgo aprobado por un comité interfuncional, con dueño, model card, monitoreo y riesgo residual documentado.
- **Contraejemplo (parece gobernanza, no lo es):** un documento de "principios éticos de IA" colgado en la intranet que nadie aplica ni audita. Política sin roles, métricas ni evidencia **no** es gobernanza (eco de [[cyber-dp4]]: tener política ≠ tener control).
- **Caso borde:** la **Shadow AI** ([[cyber-mit4]]) —empleados usando IA no sancionada— evade toda la gobernanza por definición: por eso gobernar incluye **descubrir** el uso no autorizado, no solo regular el autorizado.

## Señales de reconocimiento

| Señal | Diagnóstico de gobernanza |
|---|---|
| "Gobernamos la IA con las reglas de IT" | Faltan controles propios (sesgo, deriva, datos) |
| Nadie responde si el modelo daña | Sin dueño ni rendición de cuentas |
| Principios éticos sin auditoría | Política sin control (gobernanza de fachada) |
| Seguridad de IA "se revisa al final" | Falta Secure-by-Design |

## Errores típicos

- **Tratar la IA como software determinista:** ignorar sesgo, alucinación, deriva y dependencia de datos.
- **Confundir tener principios con gobernar:** sin roles, métricas y evidencia no hay gobernanza.
- **Gobernar solo lo sancionado:** olvidar la Shadow AI, que vive fuera del radar.

## Transferencia isomorfa

GRC + Secure-by-Design es el **NIST AI RMF** de [[cyber-mls5]] elevado a la organización: lo que allí era "model card + riesgo residual" por sistema, aquí es "roles + comités + cumplimiento" por empresa. Y "tener política ≠ tener control" es exactamente la lección de gobernanza de datos de [[cyber-dp4]]. La comunicación de riesgo a la junta ([[cyber-ms5]]) es el acto ejecutivo que cierra el lazo.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para un sistema de IA que conozcas, define dueño, qué comité aprueba su uso, y 3 controles GRC.
- **Misión externa (lab vivo):** recorre el **NIST AI RMF** (https://www.nist.gov/itl/ai-risk-management-framework), función *Govern*. **Criterio de cierre:** explicar qué controles de IA no existen en el gobierno de IT tradicional.
- **Mini-entregable:** un esquema de gobernanza de IA de una carilla (roles, proceso de aprobación de casos de uso, controles GRC, cómo se descubre la Shadow AI).

---

> **Síntesis:** la IA necesita **gobierno propio** porque es probabilística, opaca, dependiente de datos y deriva —rompe los supuestos del gobierno de IT—. La **GRC** (gobernanza/riesgo/cumplimiento) le pone roles, métricas y evidencia; **Secure-by-Design** integra seguridad y ética en **todo el ciclo de vida** con alineación interfuncional; y la **rendición de cuentas** exige un dueño que pueda demostrar diligencia. Tener principios escritos **no** es gobernar: sin roles, auditoría y descubrimiento de la Shadow AI, es fachada.

---

**Referencias**

- Massachusetts Institute of Technology. (n.d.). *AI and cybersecurity: Strategies for resilience and defense* (Module 2B). MIT Professional Education.
- National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1

*Retrieval: (1) ¿por qué la IA necesita gobierno propio, no el de IT?; (2) ¿qué son las tres letras de GRC en IA?; (3) ¿qué es Secure-by-Design para IA?; (4) ¿por qué "principios éticos" sin roles/auditoría no es gobernanza?*
