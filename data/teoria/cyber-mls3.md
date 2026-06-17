# Ataques adversarios en inferencia: evasión y robustez

> Recurso troncal: **MITRE SAFE-AI / MITRE ATLAS**. Profundiza los ataques de inferencia de [[cyber-mls2]] centrándose en la **evasión** (adversarial examples) y en cómo medir y mejorar la robustez. Sigue en [[cyber-mls4]] (extracción/inversión a fondo).

## De qué trata (y qué sabrás hacer al final)

Un modelo desplegado puede ser engañado por una entrada diseñada para que se equivoque, aunque a un humano le parezca normal. Eso es un **ataque de evasión** (adversarial example), y es la prueba más clara de que un modelo no "entiende": optimiza una frontera de decisión que se puede empujar. Para un científico de datos, entender esto cambia cómo evalúas un modelo que actuará en un entorno con adversarios.

La intuición: un detector de spam es como un portero que aprendió a reconocer "cartas sospechosas" por ciertas señales. El spammer prueba variaciones mínimas —cambiar una palabra, añadir ruido— hasta encontrar la carta que el portero deja pasar pero sigue siendo spam. No rompió al portero; encontró el punto ciego de su criterio. La evasión es buscar sistemáticamente ese punto ciego.

Al terminar podrás: (1) explicar un **adversarial example** y por qué existe; (2) distinguir ataques **white-box vs black-box**; (3) razonar la **robustez** como propiedad medible; y (4) elegir defensas y su tradeoff.

## Por qué existen los adversarial examples

Un modelo aprende una **frontera de decisión** ajustada a los datos de entrenamiento, no el concepto "verdadero". En espacios de muchas dimensiones, esa frontera tiene zonas frágiles: una perturbación **pequeña y dirigida** en la entrada (a veces imperceptible) cruza la frontera y cambia la predicción. No es un bug puntual; es una consecuencia de cómo generalizan los modelos. Por eso "alta exactitud en test" no implica "robusto ante un adversario": el test mide entradas naturales, no entradas **diseñadas para fallar**.

## White-box vs black-box

- **White-box:** el atacante conoce el modelo (arquitectura, pesos) y calcula la perturbación óptima usando los gradientes. Es el escenario más fuerte (p. ej. un modelo on-device, [[cyber-mls2]]).
- **Black-box:** el atacante solo consulta el modelo (entrada→salida) y aproxima el ataque por prueba o entrenando un sustituto. Sorprendentemente, los adversarial examples a menudo **transfieren** entre modelos, así que un atacante puede crearlos en su propio modelo y usarlos contra el tuyo.

Esto conecta con el rate limiting de [[cyber-web3]]: limitar consultas encarece los ataques black-box.

## Robustez como propiedad medible

La **exactitud estándar** y la **robustez adversaria** son métricas distintas. Robustez = exactitud bajo perturbaciones acotadas diseñadas para engañar. Se mide evaluando el modelo contra ataques (evaluación adversaria), no solo contra el test natural. Hallazgo central: suele haber un **tradeoff** entre exactitud limpia y robustez —modelos más robustos a veces pierden algo de exactitud en datos normales—, y ese tradeoff se decide según el riesgo del despliegue.

## Defensas (panorama)

- **Adversarial training:** entrenar incluyendo ejemplos adversarios; la defensa más efectiva conocida, a costo de cómputo y algo de exactitud limpia.
- **Validación/saneamiento de entradas:** detectar o filtrar entradas anómalas antes del modelo (detección, [[cyber-blue2]]).
- **Limitar la exposición:** menos información en la salida (no probabilidades finísimas) y rate limiting frenan los black-box ([[cyber-mls2]]).
- **Defensa en profundidad:** no confiar el control crítico a un solo modelo (revisión humana para decisiones de alto impacto).

No hay defensa perfecta; el objetivo es **riesgo residual aceptable** ([[cyber-ms5]]), no invulnerabilidad.

## Mini-ejemplo trabajado

Despliegas un clasificador de imágenes para moderar contenido. Tiene 98% de exactitud en test. ¿Confías?

- **Riesgo:** un adversario añade ruido imperceptible a una imagen prohibida hasta que el modelo la clasifica como "segura" (evasión). La exactitud del 98% no lo cubre: midió imágenes naturales, no diseñadas para fallar.
- **Evaluación:** mide robustez con una evaluación adversaria; probablemente caiga muchísimo bajo ataque.
- **Defensa proporcional:** adversarial training; salida sin probabilidades finas; rate limiting; y revisión humana para casos límite de alto impacto.
- **Riesgo residual:** un adversario decidido aún puede lograr alguna evasión → se acepta, monitorea ([[cyber-blue2]]) y documenta. No se promete invulnerabilidad.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| "98% en test, está listo" | Exactitud limpia ≠ robustez adversaria |
| Modelo crítico decidiendo solo, sin humano | Una evasión = daño directo |
| Salida con probabilidades muy detalladas | Facilita ataques black-box |
| Sin evaluación adversaria | Robustez desconocida |
| Modelo on-device sensible | White-box: el atacante tiene los gradientes |

## Errores típicos

- **Equiparar exactitud con robustez:** el test natural no mide al adversario.
- **Confiar un control crítico a un solo modelo:** sin defensa en profundidad, la evasión es daño directo.
- **Creer que black-box es seguro:** los adversarial examples transfieren entre modelos.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** una perturbación pequeña y dirigida en una imagen hace fallar al clasificador pese a su alta exactitud en test; adversarial training es la mejor defensa conocida, con tradeoff.
- **Contraejemplo:** un modelo de moderación con adversarial training, salida de baja resolución, rate limiting y humano en el lazo para casos límite: la evasión se vuelve cara y su impacto, contenido.
- **Caso borde:** la robustez a un **tipo** de perturbación (p. ej. ruido pequeño en píxeles) no garantiza robustez a otro (rotaciones, parches, cambios semánticos); defender contra una familia de ataques puede dejar otra abierta. La evaluación adversaria debe cubrir las amenazas realistas, no una sola.

## Transferencia a ciencia de datos e IA

La evasión es el ataque de inferencia central de cualquier modelo que actúe en un entorno hostil (moderación, fraude, seguridad). La idea "el test natural no mide al adversario" es la versión-ML de "los tests funcionales no son verificación de seguridad" ([[cyber-dev4]]). Y la evaluación adversaria es el *red teaming* de modelos, hermano del de LLMs en [[cyber-llm-rag-agents]].

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el clasificador de moderación, lista 3 defensas ordenadas por impacto/costo y el riesgo residual que aceptarías.
- **Misión externa (lab vivo):** en **MITRE ATLAS** (https://atlas.mitre.org) busca una técnica de evasión (evasion) y un caso real. **Criterio de cierre:** explicar por qué la exactitud en test no la habría predicho.
- **Mini-entregable:** un párrafo "exactitud limpia vs robustez" para un modelo que conozcas, con cómo evaluarías su robustez.

---

> **Síntesis:** un **adversarial example** es una entrada con perturbación pequeña y dirigida que hace fallar al modelo, consecuencia de cómo generaliza (frontera de decisión frágil), no un bug puntual. Por eso **exactitud en test ≠ robustez adversaria**, que se mide con evaluación adversaria. Los ataques pueden ser **white-box** (con gradientes) o **black-box** (por consulta, y a menudo **transfieren**). Se defiende con **adversarial training**, limitar la exposición y defensa en profundidad, aceptando **riesgo residual**.

---

**Referencias**

- Kressel, J., Perrella, R., Reed, E., Naik, N., Sidhu, J., Hu, Q., Booker, L., Cintron, J., & Huffner, L. (2025). *SAFE-AI: A framework for securing AI-enabled systems*. The MITRE Corporation.
- MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org
- Goodfellow, I., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. *ICLR*.

*Retrieval: (1) ¿por qué existen los adversarial examples?; (2) white-box vs black-box (y qué es la transferencia); (3) ¿por qué exactitud en test no es robustez?; (4) ¿cuál es la defensa más efectiva conocida y su costo?*
