# Cibercrimen potenciado por IA: deepfakes, clonación de voz y mercado clandestino

> Recurso troncal: **MIT — *AI and Cybersecurity*** (Módulos 1B y 3A, uso ofensivo). El espejo ofensivo que anticipó [[cyber-mit1]]. Es el sustrato de los casos reales de [[cyber-mit5]]. Conecta con la ingeniería social de [[cyber-ms4]].

## De qué trata (y qué sabrás hacer al final)

La IA generativa abarató y escaló el fraude: hoy un atacante clona una voz con segundos de audio público y fabrica un video falso de tu director en una videollamada. El ataque no rompe tu cifrado ni tu firewall —rompe tu **confianza perceptual** ("vi y oí a mi jefe, debe ser real")—. Esta lección mapea el arsenal ofensivo de IA para que reconozcas el patrón antes de ser la víctima.

La intuición: durante milenios, "reconocer la cara y la voz" fue prueba suficiente de identidad. La IA generativa **rompió ese supuesto** de golpe. Es como si de pronto cualquiera pudiera falsificar perfectamente tu firma, tu sello y tu letra: el canal en el que confiabas dejó de ser confiable. La defensa no es "mirar más fuerte" (los deepfakes engañan a expertos); es **cambiar de canal de verificación**.

Al terminar podrás: (1) nombrar el arsenal ofensivo de IA (**deepfakes, voice cloning, vishing, dark-web AI, malware con IA**); (2) explicar por qué ataca a la **percepción/confianza**, no a la técnica; (3) reconocer las señales del fraude potenciado por IA; y (4) entender por qué la verificación **fuera de banda** es la defensa central.

## El arsenal ofensivo de IA

| Arma | Qué hace | Materia prima |
|---|---|---|
| **Deepfake de video** | Cara/gestos falsos en tiempo real (videollamada) | Video público del ejecutivo |
| **Voice cloning** | Clona una voz con segundos de audio | Audio de YouTube/presentaciones |
| **Vishing hiperpersonalizado** | Llamadas/notas de voz a medida, a escala | Voz clonada + datos OSINT |
| **Dark-web AI / "WormGPT"** | LLMs sin restricciones para fraude/malware | Servicios criminales de pago |
| **Malware asistido por IA** | Genera/ofusca variantes, evade detección | Modelos generativos |

El hilo común: la IA **abarata y escala** lo que antes exigía talento y tiempo. El phishing de "príncipe nigeriano" con errores ahora es un video fotorrealista de tu CFO.

## Por qué ataca a la confianza, no a la técnica

Tus controles técnicos (TLS, MFA, cifrado) protegen **canales**, no **percepciones**. El fraude con IA evita todos: convence a una **persona autorizada** de usar sus accesos legítimos. Es **ingeniería social** ([[cyber-ms4]]) sobrealimentada: la autoridad aparente (el "CEO") + urgencia + un canal que parecía irrefutable (ver y oír). Por eso la víctima suele ser alguien con poder de actuar (finanzas, IT), no un sistema.

**[CAJA NEGRA OK]** No necesitas saber cómo se entrena un deepfake; sí debes asumir: **cualquier voz o cara pública puede falsificarse de forma convincente**, y por tanto "lo vi/oí" ya no prueba identidad.

## Mini-ejemplo trabajado

Recibes un correo del "CFO" pidiendo una transferencia urgente y confidencial. Sospechas (bien). Luego te suma a una **videollamada** donde aparecen el CFO y dos directivos más, hablando entre sí, que confirman la orden. ¿Confías ahora?

Razonamiento defensivo: la videollamada **subió** tu confianza justo porque asumes que un video en vivo no se falsifica. Pero eso es exactamente lo falsificable hoy ([[cyber-mit5]], caso 1). La jugada correcta: la **alta consecuencia** (transferencia) exige verificación **fuera de banda** —llamar al CFO por un número conocido de antemano, usar un código acordado, exigir doble aprobación ([[cyber-ms2]] separación de funciones)—. La señal de "más realismo" debe **aumentar** la sospecha en transacciones sensibles, no bajarla.

Predicción antes de seguir: ¿qué control habría detenido esto sin necesidad de "detectar el deepfake"? → un **proceso** (verificación fuera de banda + doble aprobación), no un ojo más entrenado.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** urgencia + autoridad + confidencialidad + presión para saltarse el proceso = bandera de fraude, **independientemente** de cuán real se vea/oiga.
- **Contraejemplo (parece defensa, no lo es):** "capacitaremos a la gente para detectar deepfakes". Los deepfakes ya engañan a expertos y mejoran cada mes; depender de la detección perceptual humana es perder. La defensa es de **proceso**, no de agudeza visual.
- **Caso borde:** un deepfake imperfecto (un glitch) que aun así funciona porque la **urgencia** impidió pensar. El factor decisivo no fue el realismo, fue la presión —ahí pega la defensa de proceso—.

## Señales de reconocimiento

| Señal | Lectura |
|---|---|
| Urgencia + confidencialidad + autoridad | Patrón clásico de fraude (con o sin IA) |
| "No lo comentes con nadie / no verifiques" | Busca anular la verificación cruzada |
| Petición de transferencia o credenciales por voz/video | Verifica fuera de banda, siempre |
| "Pero lo vi/oí en vivo" | Hoy eso NO prueba identidad |

## Errores típicos

- **Confiar en ver/oír:** tratar audio/video como prueba de identidad.
- **Apostar a la detección perceptual:** "lo notaríamos" — no, y empeora con el tiempo.
- **Saltarse el proceso por la urgencia:** la urgencia es la herramienta del atacante, no una excepción legítima.

## Transferencia isomorfa

Esto es la **prompt injection** de [[cyber-llm1]] aplicada a humanos: contenido fabricado que se hace pasar por una instrucción de autoridad para inducir una acción. La defensa también es la misma idea de [[cyber-ms4]]: no confiar en el canal, verificar por otro independiente, y limitar lo que un solo engañado puede ejecutar ([[cyber-ms2]], least privilege). En IA generativa, el deepfake es a la confianza lo que el adversarial example ([[cyber-mls3]]) es al clasificador: una entrada diseñada para cruzar tu frontera de "esto es legítimo".

## Práctica, misión externa y mini-entregable

- **Práctica interna:** diseña el "protocolo fuera de banda" para transferencias y para reseteo de credenciales (qué canal, qué código, quién aprueba).
- **Misión externa (lab vivo):** revisa recursos del **NIST** sobre *synthetic media / deepfakes* o el material de **MITRE ATLAS** (https://atlas.mitre.org) sobre manipulación. **Criterio de cierre:** explicar por qué la defensa es de proceso, no de detección perceptual. Solo material informativo; nunca generes deepfakes de personas reales.
- **Mini-entregable:** una política antifraude de IA de una carilla (señales, verificación fuera de banda, doble aprobación, qué hacer ante una "orden urgente").

---

> **Síntesis:** la IA generativa **abarata y escala** el fraude —**deepfakes, clonación de voz, vishing, dark-web AI, malware asistido**— y ataca tu **confianza perceptual**, no tu técnica: convence a una persona autorizada usando autoridad + urgencia + un canal que parecía irrefutable. Como los deepfakes engañan hasta a expertos, "lo vi/oí" ya **no** prueba identidad; la defensa es de **proceso**: **verificación fuera de banda**, doble aprobación y least privilege. El realismo creciente debe **subir** la sospecha en lo sensible, no bajarla.

---

**Referencias**

- Massachusetts Institute of Technology. (n.d.). *AI and cybersecurity: Strategies for resilience and defense* (Module 1B, 3A). MIT Professional Education.
- MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org

*Retrieval: (1) nombra 4 armas del arsenal ofensivo de IA; (2) ¿por qué el fraude con IA ataca la confianza y no la técnica?; (3) ¿por qué falla apostar a "detectar el deepfake"?; (4) ¿qué es verificación fuera de banda y por qué es la defensa central?*
