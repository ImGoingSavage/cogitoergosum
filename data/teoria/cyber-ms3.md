# Economía de la seguridad: incentivos, externalidades y por qué se descuida la defensa

> Recurso troncal: **Anderson, *Security Engineering* (3.ª ed.)**. Una de las tesis centrales de Anderson: muchos fallos de seguridad no son técnicos sino **económicos**. Construye sobre [[cyber-ms1]] y [[cyber-ms2]]; prepara [[cyber-ms4]] (sociotécnico).

## De qué trata (y qué sabrás hacer al final)

Pregunta incómoda: si sabemos cómo hacer software seguro desde hace décadas, ¿por qué el mundo sigue lleno de sistemas inseguros? La respuesta de Anderson no es "la gente es tonta", sino que **los incentivos están desalineados**: quien puede prevenir el fallo no es quien sufre el daño. La seguridad falla donde la economía la abandona.

La intuición: imagina un edificio donde el constructor ahorra en cerraduras porque las pérdidas por robo las pagan los inquilinos, no él. El constructor actúa "racionalmente" (maximiza su beneficio) y aun así el edificio queda inseguro. No hay maldad ni incompetencia: hay un **incentivo torcido**. Gran parte de la inseguridad del mundo digital es exactamente eso.

Al terminar podrás: (1) explicar por qué la seguridad es un problema de **incentivos**, no solo técnico; (2) reconocer **externalidades** de seguridad; (3) entender el **riesgo moral** y el problema del "limón"; y (4) ubicar quién debería pagar por una defensa.

## La idea central: incentivos desalineados

Un control de seguridad lo implementa **alguien**, cuesta **algo**, y el daño de no tenerlo lo sufre **alguien más**. Cuando esos "alguien" no coinciden, la defensa se descuida aunque sea técnicamente trivial:

- Una plataforma guarda mal las contraseñas: si las filtran, el daño lo sufren los **usuarios**, no la empresa (que quizá ni se entera o no paga consecuencias).
- Un fabricante de dispositivos IoT no invierte en seguridad: los dispositivos comprometidos atacan a **terceros**, no a sus clientes.

La pregunta económica —*¿quién paga el costo y quién sufre el daño?*— predice la inseguridad mejor que cualquier análisis puramente técnico.

## Externalidades, riesgo moral y el "limón"

- **Externalidad:** el costo de una decisión recae en alguien que no la tomó. La contaminación es la analogía clásica; un dispositivo inseguro que se usa para atacar a otros es una **externalidad de seguridad**.
- **Riesgo moral (moral hazard):** quien está protegido del daño toma más riesgos. Si "la nube" o "el seguro" absorben las pérdidas, el equipo se relaja.
- **Mercado de limones:** si el comprador no puede distinguir software seguro de inseguro, no pagará más por el seguro, y el seguro desaparece del mercado. Por eso la seguridad necesita **señales verificables** (certificaciones, SBOM, auditorías — ver [[cyber-dev2]]).

## Mini-ejemplo trabajado

Un equipo de datos debate si invertir una semana en cifrar y controlar el acceso a un dataset de clientes. El gerente dice: "nunca nos han hackeado, esa semana es cara". Análisis económico:

- **¿Quién paga el control?** El equipo (una semana de trabajo, costo visible e inmediato).
- **¿Quién sufre el daño de una fuga?** Los **clientes** (cuyo dato se expone) y la empresa solo si hay multa o escándalo (costo incierto y diferido).
- **El sesgo:** el costo del control es seguro y ahora; el del daño es incierto y después → el incentivo empuja a no invertir, aunque socialmente la inversión valga la pena.
- **Corrección:** hacer visible el costo del daño (responsabilidad legal, reputación, las personas afectadas) cambia el cálculo. La seguridad se decide alineando el incentivo, no solo "concientizando".

## Señales de reconocimiento

| Señal | Diagnóstico económico |
|---|---|
| "Nunca nos ha pasado, no invertimos" | Costo del control visible; daño diferido e incierto |
| El daño de un fallo lo sufre un tercero | Externalidad → nadie interno lo prioriza |
| "El proveedor/la nube responde por eso" | Riesgo moral: protegido del daño, baja la guardia |
| No se puede distinguir lo seguro de lo inseguro | Mercado de limones → señales verificables |

## Errores típicos

- **"Es un problema de concientización":** capacitar no arregla un incentivo torcido; alinear responsabilidades sí.
- **Ignorar las externalidades:** evaluar solo el daño propio y no el que tu sistema puede causar a otros.
- **Confundir "no nos ha pasado" con "es seguro":** ausencia de incidente ≠ ausencia de riesgo.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** un fabricante no asegura un dispositivo porque el daño recae en el usuario (externalidad); la pregunta '¿quién paga el control y quién sufre el daño?' explica el descuido.
- **Contraejemplo:** una regulación que hace **responsable** a quien guarda los datos por las fugas alinea el incentivo: de pronto cifrar "esa semana cara" se vuelve obviamente rentable. El cambio fue económico, no técnico.
- **Caso borde:** a veces el incentivo está alineado y aun así hay inseguridad por **descuido genuino** o falta de capacidad; la economía explica mucho, no todo. No todo fallo es un incentivo torcido.

## Transferencia a ciencia de datos e IA

El análisis de incentivos explica por qué los datasets sensibles se descuidan ([[cyber-data-privacy]]), por qué las dependencias inseguras persisten ([[cyber-dev2]]) y por qué la seguridad de modelos compartidos se ignora ([[cyber-ml-security]]): en todos, quien asume el costo del control no siempre sufre el daño. Como DS, identificar "¿quién paga y quién sufre?" te dice dónde **realmente** caerá la defensa.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para un sistema que conozcas, responde "¿quién paga el control?" y "¿quién sufre el daño?" en 3 controles distintos; marca dónde el incentivo está torcido.
- **Misión externa (lab vivo):** en el **NIST Cybersecurity Framework** (https://www.nist.gov/cyberframework), observa cómo *Govern/Identify* tratan el riesgo a nivel organización. **Criterio de cierre:** explicar por qué la gobernanza precede a la técnica.
- **Mini-entregable:** un párrafo aplicando "¿quién paga, quién sufre?" a una decisión de seguridad real que hayas visto.

---

> **Síntesis:** mucha inseguridad no es técnica sino **económica**: el control lo paga alguien y el daño lo sufre **otro** (externalidades), quien está cubierto se relaja (**riesgo moral**), y sin señales verificables el mercado no premia lo seguro (**limones**). La pregunta rectora —*¿quién paga el costo y quién sufre el daño?*— predice dónde se descuidará la defensa, y alinear ese incentivo logra más que "concientizar".

---

**Referencias**

- Anderson, R. (2020). *Security engineering: A guide to building dependable distributed systems* (3rd ed.). Wiley.
- Anderson, R., & Moore, T. (2006). The economics of information security. *Science, 314*(5799), 610–613.

*Retrieval: (1) ¿por qué la seguridad es un problema de incentivos?; (2) define externalidad y riesgo moral en seguridad; (3) ¿qué es el mercado de limones aplicado a software?; (4) ¿qué pregunta económica predice el descuido de la defensa?*
