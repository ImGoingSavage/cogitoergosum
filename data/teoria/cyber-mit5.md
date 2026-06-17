# Casos de estudio: anatomía del fraude con IA

> Recurso troncal: **MIT — *AI and Cybersecurity*** (Case Studies & Practical Applications). Capstone del cluster: cuatro incidentes **reales** de fraude potenciado por IA, analizados con método de caso. Aplica todo: [[cyber-mit2]] (arsenal ofensivo), [[cyber-ms4]] (ingeniería social), [[cyber-ms2]] (controles), [[cyber-blue4]] (respuesta).

## De qué trata (y qué sabrás hacer al final)

La teoría se vuelve criterio cuando la cruzas con lo que **de verdad pasó**. Esta lección estudia cuatro fraudes reales con IA y, para cada uno, responde las mismas preguntas: **¿qué ocurrió? ¿cómo se hizo? ¿qué tipo de ataque fue? ¿cómo se habría evitado?** Y cierra evaluándote con un **caso espejo** —un incidente nuevo que tú debes diagnosticar—, que es como el MIT enseña con casos: no memorizar el incidente, sino **transferir** el patrón a uno que no has visto.

La intuición: estudiar estos casos es como un médico revisando autopsias —no para asustarse, sino para reconocer los síntomas a tiempo la próxima vez—. Verás que los cuatro, pese a sus diferencias, comparten **el mismo esqueleto**: IA que falsifica una identidad de autoridad + urgencia + un canal que parecía confiable, para que una persona autorizada actúe antes de verificar.

Al terminar podrás: (1) analizar un incidente con un **marco de caso** repetible; (2) clasificar el **tipo de ataque** (deepfake, voice cloning, vishing, secuestro de canal); (3) nombrar el **control de proceso** que lo habría detenido; y (4) **transferir** el patrón a un caso espejo.

## El marco de análisis (úsalo en cualquier incidente)

Por cada caso preguntamos seis cosas. Memoriza el marco; es reutilizable:

1. **Qué pasó** (impacto, en una frase).
2. **Cómo se hizo** (la mecánica del ataque).
3. **Qué tipo de ataque fue** (la categoría, para reconocerlo).
4. **Cómo se habría evitado** (el control —casi siempre de proceso, no técnico—).
5. **Aristas** (con qué de lo aprendido conecta).
6. **Evaluación** (un caso espejo para transferir).

---

## Caso 1 — La videoconferencia deepfake de $25 millones (enero 2024)

- **Qué pasó:** un empleado de finanzas de la sede en Hong Kong de una multinacional hizo varias transferencias por ~HK$200M (≈ **$25.6M USD**) a cuentas de estafadores. Sospechó de un primer correo de "phishing" del CFO… pero **bajó la guardia tras una videollamada**.
- **Cómo se hizo:** los atacantes tomaron video y audio **públicos** de los ejecutivos y, con IA generativa, crearon **deepfakes en tiempo real** del CFO y varios directivos. Montaron una videollamada grupal donde los deepfakes hablaban entre sí y con la víctima, ordenando transferencias urgentes y "confidenciales" por una supuesta adquisición secreta.
- **Tipo de ataque:** **deepfake de video en tiempo real** + ingeniería social (BEC, *Business Email Compromise*, elevado con IA). El video sirvió como **falsa verificación**.
- **Cómo se habría evitado:** el correo inicial ya era sospechoso; la regla de [[cyber-mit2]] es que **el realismo no es verificación**. Control: **verificación fuera de banda** (llamar al CFO a un número conocido), **doble aprobación** para transferencias grandes ([[cyber-ms2]], separación de funciones), y política de "ninguna orden urgente+confidencial salta el proceso". Nada de esto requiere "detectar el deepfake".
- **Aristas:** [[cyber-mit2]] (deepfake como arma), [[cyber-ms4]] (autoridad+urgencia), [[cyber-mit1]] (transferencia = alta consecuencia → humano + verificación, jamás automatizado).

## Caso 2 — Clonación de voz del CEO (primer semestre 2024)

- **Qué pasó:** firmas de seguridad/credenciales (p. ej. **LastPass**, **Wiz**) sufrieron campañas donde empleados recibían llamadas y notas de voz que **imitaban idénticamente a su CEO**, pidiendo credenciales y accesos de administrador.
- **Cómo se hizo:** clonación de voz con redes neuronales alimentadas con **segundos de audio** sacados de presentaciones públicas del CEO en YouTube; un script automatizado generó **vishing hiperpersonalizado** a escala, con fidelidad e inflexiones que casi engañan a profesionales de seguridad.
- **Tipo de ataque:** **voice cloning + vishing** (phishing por voz). Suplantación de autoridad por un canal "de confianza" (la voz conocida).
- **Cómo se habría evitado:** la voz **ya no prueba identidad** ([[cyber-mit2]]). Control: nunca entregar credenciales/accesos por voz; **verificación fuera de banda**; **MFA resistente a phishing** (llaves de seguridad, no códigos dictables — [[cyber-sys3]]); cultura de "está bien dudar del CEO". Que en LastPass/Wiz **no** cayeran muestra el valor de una cultura de verificación.
- **Aristas:** [[cyber-sys3]] (MFA, credenciales), [[cyber-mit2]] (voice cloning), [[cyber-ms4]] (insider inducido por ingeniería social).

## Caso 3 — Fraude al CEO de la empresa energética (septiembre 2019)

- **Qué pasó:** el director de una energética británica transfirió de urgencia **€220,000** a un "proveedor" en Hungría, creyendo seguir órdenes telefónicas de su CEO de la matriz alemana. Uno de los **primeros** fraudes con IA comercial documentados.
- **Cómo se hizo:** software comercial de síntesis/clonación de voz imitó el tono, los **modismos**, la cadencia y el **acento** del CEO alemán; se reforzó con un correo de seguimiento para crear urgencia y mover los fondos **antes de cualquier verificación cruzada**.
- **Tipo de ataque:** **voice cloning + BEC** (la versión "temprana" del caso 2). Demuestra que el patrón no es nuevo: lo nuevo es lo barato y convincente que se volvió.
- **Cómo se habría evitado:** mismo control de proceso —**verificación fuera de banda** y **doble aprobación**—. La urgencia deliberada para "ganarle a la verificación" es la señal (eco de [[cyber-mit2]]).
- **Aristas:** [[cyber-mit2]] (clonación de voz), [[cyber-ms5]] (proceso proporcional a la consecuencia), [[cyber-blue4]] (un protocolo previo habría contenido el incidente).

## Caso 4 — La estafa cripto por livestream (junio 2024)

- **Qué pasó:** estafadores secuestraron canales verificados de YouTube de gran alcance, los renombraron como empresas reales (p. ej. Tesla) y emitieron **transmisiones en vivo** con deepfakes de Elon Musk y Jensen Huang prometiendo "duplicar" cripto vía códigos QR. Un solo stream recaudó **>$50,500 USD en menos de 2 horas**.
- **Cómo se hizo:** **secuestro de cuentas** (canales verificados) + **deepfake visual + voz sintética** en bucle a partir de discursos reales pasados, con falsa interacción "en vivo" y QR a monederos fraudulentos.
- **Tipo de ataque:** **deepfake masivo + secuestro de canal/cuenta + fraude de inversión**. Aquí la víctima es el **público**, no un empleado: ataque a la confianza a **escala**.
- **Cómo se habría evitado:** del lado de la plataforma/cuenta, **MFA fuerte** contra el secuestro del canal ([[cyber-sys3]]) y detección de cambios anómalos ([[cyber-blue2]]); del lado del usuario, el escepticismo base ("nadie duplica tu cripto"; promesa+urgencia+QR = fraude). El realismo del deepfake es irrelevante frente a la regla "si suena demasiado bueno…".
- **Aristas:** [[cyber-sys3]] (secuestro de cuenta/MFA), [[cyber-blue2]] (detección de anomalías de cuenta), [[cyber-mit2]] (deepfake a escala).

---

## El patrón común (la moraleja que transfiere)

Los cuatro casos, distintos en superficie, comparten el **mismo esqueleto**:

> **IA que falsifica una identidad de autoridad** (cara/voz) **+ urgencia + un canal que parecía irrefutable** → una persona (o un público) **actúa antes de verificar**.

Y comparten la **misma defensa**, que **no** depende de detectar la falsificación:
- **Verificación fuera de banda** por un canal independiente y acordado de antemano.
- **Doble aprobación / separación de funciones** para acciones de alta consecuencia ([[cyber-ms2]]).
- **El realismo creciente debe subir la sospecha**, no bajarla ([[cyber-mit2]]).
- **Cultura de "está bien verificar"**, incluso al CEO ([[cyber-ms4]], [[cyber-mit4]]).

Moraleja: **no entrenes el ojo, blinda el proceso.** La verificación perceptual es una carrera que el defensor pierde; el proceso de verificación cruzada es una carrera que gana.

## Errores típicos al estudiar casos

- **Quedarse en la anécdota:** memorizar "el caso de los $25M" sin extraer el patrón transferible.
- **Buscar la solución técnica:** "necesitamos un detector de deepfakes" — la defensa fue de **proceso**.
- **Creerse inmune:** "a mí no me engañarían"; los casos engañaron a profesionales y a un CEO.

## Evaluación: caso espejo (transfiere el patrón)

Así evalúa el método de caso: te doy un incidente **nuevo**; tú aplicas el marco. (Las preguntas del banco de esta unidad hacen justo esto.)

> **Caso espejo:** Eres analista en una fintech. Tu "Director de Operaciones" te escribe por chat interno y luego te envía una **nota de voz** —es su voz, sin duda— pidiendo que **deshabilites temporalmente el MFA** de una cuenta de servicio "para un despliegue urgente, no lo comentes con nadie todavía".
>
> Responde con el marco: (1) ¿qué **tipo de ataque** es probable? (2) ¿qué **señales** lo delatan? (3) ¿qué **control de proceso** aplicas antes de actuar? (4) ¿con qué **caso real** de esta lección rima?

*Pista de autoevaluación:* es voice cloning + vishing (casos 2 y 3); señales = voz de autoridad + urgencia + "no lo comentes" (anula verificación) + acción de alta consecuencia (bajar MFA); control = **verificación fuera de banda** + negarte a bajar MFA sin doble aprobación; rima con LastPass/Wiz, donde **dudar** salvó el día.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** resuelve el caso espejo por escrito con las 4 preguntas del marco.
- **Misión externa (lab vivo):** busca una nota pública reciente sobre fraude con deepfake/voice cloning (fuente confiable) y analízala con el marco de 6 puntos. **Criterio de cierre:** identificar el control de proceso que lo habría evitado. Solo análisis; nunca generes deepfakes de personas reales.
- **Mini-entregable (mini-proyecto del cluster):** un **playbook antifraude con IA** de una a dos carillas: señales de alerta, protocolo de verificación fuera de banda, reglas de doble aprobación por monto/acción, y guion de respuesta ante una "orden urgente del CEO". Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** cuatro fraudes reales con IA —deepfake de $25M, clonación de voz a LastPass/Wiz, fraude al CEO energético, estafa cripto por livestream— comparten un **mismo esqueleto**: IA que falsifica una **identidad de autoridad** + **urgencia** + un **canal que parecía irrefutable**, para que alguien **actúe antes de verificar**. La defensa común **no** es detectar la falsificación (carrera perdida) sino **blindar el proceso**: **verificación fuera de banda**, **doble aprobación** y una **cultura de verificar**, donde el realismo creciente **sube** la sospecha. El método de caso evalúa **transfiriendo** el patrón a un incidente nuevo, no memorizando el viejo.

---

**Referencias**

- Massachusetts Institute of Technology. (n.d.). *AI and cybersecurity: Strategies for resilience and defense* (Case Studies & Practical Applications). MIT Professional Education.
- MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org

*Retrieval: (1) ¿cuál es el esqueleto común de los cuatro casos?; (2) ¿por qué la defensa es de proceso y no de detección perceptual?; (3) nombra los tres controles que repiten en los casos; (4) en el caso espejo, ¿qué tipo de ataque es y qué control aplicas?*
