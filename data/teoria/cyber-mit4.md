# Shadow AI y confianza humano-IA

> Recurso troncal: **MIT — *AI and Cybersecurity*** (Módulo 4). El riesgo que crece más rápido (IA no sancionada) y el factor que decide todo (la confianza). Conecta con el factor humano de [[cyber-ms4]] y la gobernanza de [[cyber-mit3]].

## De qué trata (y qué sabrás hacer al final)

Tus empleados ya están usando IA —ChatGPT, copilotos, traductores— con o sin permiso, y a menudo pegando datos sensibles en herramientas que no controlas. Eso es **Shadow AI**: uso de IA no sancionada, sin visibilidad ni gobierno. Y del otro lado está la pregunta que sostiene toda la relación: ¿cuánto, y en qué, deben **confiar** los humanos en la IA? Esta lección cierra el cluster con los dos extremos del factor humano: el uso descontrolado y la confianza calibrada.

La intuición: la Shadow AI es como empleados llevándose documentos confidenciales a fotocopiar a una tienda de la esquina "para ir más rápido": resuelven su tarea, pero el dato salió de tu control y no hay registro. Prohibirlo del todo los empuja a esconderse más; ignorarlo es una fuga constante. La confianza humano-IA, por su parte, es como confiar en un GPS: ni desobedecerlo siempre (pierdes su valor) ni seguirlo a un lago (exceso de confianza); es **confianza calibrada**.

Al terminar podrás: (1) distinguir **Shadow AI de Shadow IT**; (2) nombrar sus riesgos propios; (3) usar el **OODA loop** para descubrirla y gestionarla; y (4) razonar la **confianza humano-IA calibrada**.

## Shadow AI vs Shadow IT

| | Shadow IT | Shadow AI |
|---|---|---|
| Qué es | Uso de servicios/software de IT no autorizados | Uso de **herramientas de IA** no sancionadas |
| Riesgo clásico | Datos en apps no aprobadas, sin parches | Lo anterior **+** riesgos propios de IA |
| Riesgo PROPIO | — | Salidas no verificadas, **sesgo del modelo**, datos de entrenamiento ajenos, decisiones opacas |

La diferencia clave: la Shadow IT mete tus datos en un lugar no aprobado; la Shadow AI, además, **introduce decisiones y contenido generados por un modelo que no controlas** —que puede alucinar, sesgar, o haber memorizado lo que le pegaste ([[cyber-mls4]])—.

## Los riesgos propios de la Shadow AI

- **Fuga de datos:** pegar código, datos de clientes o secretos en una IA pública → salen de tu control y pueden quedar en sus datos ([[cyber-data-privacy]]).
- **Cumplimiento e IP:** violar privacidad o regulación sin saberlo; perder propiedad intelectual.
- **Sin trazabilidad:** decisiones tomadas con IA sin registro ni auditoría ([[cyber-dp4]]) → no puedes investigar ni rendir cuentas.
- **Superficie de ataque:** herramientas no vetadas pueden traer prompt injection, malware o robo de datos ([[cyber-llm1]]).

## Descubrir y gestionar con el OODA loop

No puedes gobernar ([[cyber-mit3]]) lo que no ves. El **OODA loop** (Observar, Orientar, Decidir, Actuar) estructura la respuesta:
- **Observar:** ¿qué herramientas de IA se usan, dónde y cómo? (telemetría de red, encuestas, descubrimiento).
- **Orientar:** ¿qué riesgo introduce cada una (datos, cumplimiento)?
- **Decidir:** ¿prohibir, permitir con condiciones, o proveer una alternativa sancionada?
- **Actuar:** implementar y **repetir** (el uso cambia rápido).

Moraleja de gestión: la mejor defensa contra la Shadow AI no suele ser prohibir (empuja a esconderse), sino **dar una vía sancionada buena** + visibilidad + reglas claras de qué datos nunca se pegan.

## Confianza humano-IA calibrada

El otro extremo: que los humanos confíen **lo justo** en la IA. Dos fallos simétricos:
- **Exceso de confianza (automation bias):** aceptar la salida de la IA sin verificar —el operador del SOC que cierra un sistema porque "la IA dijo"—.
- **Desconfianza/abandono:** ignorar a la IA y perder su valor, o desactivarla.

La meta es **confianza calibrada**: confiar en la IA donde es fiable (patrón a escala) y verificar donde es falible (juicio de alta consecuencia) — el cuadrante de [[cyber-mit1]] hecho cultura. Se construye con transparencia (saber qué hace y sus límites), explicabilidad y experiencia compartida.

## Mini-ejemplo trabajado

Descubres que medio equipo de datos pega fragmentos de la base de clientes en un chatbot público para "acelerar el análisis". ¿Prohibir y ya?

- **Riesgos:** fuga de datos personales ([[cyber-data-privacy]]), posible incumplimiento, sin trazabilidad de qué se compartió.
- **OODA:** Observar (¿quién, qué datos, con qué frecuencia?) → Orientar (riesgo alto: datos personales) → Decidir (proveer una IA empresarial sancionada que no entrene con tus datos + política de "nunca pegar PII") → Actuar y monitorear.
- **Por qué no solo prohibir:** prohibir sin alternativa empuja el uso a la clandestinidad (más Shadow AI, menos visible). Dar una vía buena + reglas claras reduce el riesgo real.
- **Confianza:** además, capacitar para **no** aceptar a ciegas las salidas (verificar antes de decidir) — confianza calibrada.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** alternativa de IA sancionada + política de datos + descubrimiento continuo (OODA) + cultura de verificar salidas. Reduce Shadow AI **y** calibra confianza.
- **Contraejemplo (parece solución, no lo es):** prohibir toda IA por política. La gente la usa igual, a escondidas, sin reglas ni visibilidad → más riesgo, no menos.
- **Caso borde:** una IA sancionada y fiable genera **exceso de confianza** —el equipo deja de verificar—, hasta que un caso límite (una alucinación, un dato envenenado) pasa sin filtro. Confianza alta sin verificación residual también falla.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| "Prohibido usar IA" (sin alternativa) | Empuja a Shadow AI invisible |
| Datos sensibles pegados en IA pública | Fuga + incumplimiento |
| "La IA lo dijo, lo hicimos" | Exceso de confianza (automation bias) |
| Nadie sabe qué IA se usa en la empresa | Sin visibilidad → sin gobernanza |

## Errores típicos

- **Prohibir sin proveer alternativa:** convierte el problema en invisible.
- **Confundir Shadow AI con Shadow IT:** olvidar sus riesgos propios (sesgo, salidas no verificadas, datos de entrenamiento).
- **Confianza no calibrada:** aceptar a ciegas o descartar del todo, en vez de confiar-y-verificar según la consecuencia.

## Transferencia isomorfa

La Shadow AI es la **gobernanza de [[cyber-mit3]] vista desde su punto ciego**: lo que escapa al radar; por eso gobernar incluye **descubrir** (OODA), no solo regular. El "no pegar datos en IA pública" es minimización y control de acceso ([[cyber-data-privacy]], [[cyber-dp4]]) aplicado a un canal nuevo. Y la confianza calibrada es el cuadrante humano-vs-IA de [[cyber-mit1]] convertido en hábito y cultura ([[cyber-ms4]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** aplica el OODA loop a la Shadow AI de una organización imaginaria: ¿qué observas, qué decides, qué alternativa ofreces?
- **Misión externa (lab vivo):** revisa guías de gobernanza/uso aceptable de IA (p. ej. **NIST AI RMF** *Govern*, https://www.nist.gov/itl/ai-risk-management-framework). **Criterio de cierre:** explicar por qué prohibir no es la mejor defensa contra la Shadow AI.
- **Mini-entregable:** una política de uso de IA de una carilla (qué está sancionado, qué datos nunca se pegan, cómo se descubre el uso, cómo se calibra la confianza en las salidas).

---

> **Síntesis:** la **Shadow AI** (IA no sancionada) añade, sobre la Shadow IT, riesgos **propios**: salidas no verificadas, sesgo, datos de entrenamiento ajenos y decisiones opacas, todo sin trazabilidad. Se gestiona **descubriéndola** (OODA loop) y dando una **alternativa sancionada** + reglas de datos, no prohibiendo a ciegas. El reverso es la **confianza humano-IA calibrada**: confiar donde la IA es fiable y verificar donde es falible (el cuadrante de [[cyber-mit1]] hecho cultura), evitando tanto el exceso de confianza como el abandono.

---

**Referencias**

- Massachusetts Institute of Technology. (n.d.). *AI and cybersecurity: Strategies for resilience and defense* (Module 4). MIT Professional Education.
- National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1

*Retrieval: (1) ¿en qué se diferencia Shadow AI de Shadow IT?; (2) nombra 2 riesgos propios de la Shadow AI; (3) ¿qué pasos tiene el OODA loop y por qué prohibir no basta?; (4) ¿qué es confianza humano-IA calibrada y sus dos fallos?*
