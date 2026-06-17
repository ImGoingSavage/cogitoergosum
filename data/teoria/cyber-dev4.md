# Verificación: SAST, fuzzing, code review y pruebas de seguridad

> Recurso troncal: **OpenSSF / Wheeler, *Secure Software Development Fundamentals***. Diseñar seguro ([[cyber-dev3]]) no basta: hay que **comprobar** que el código lo es. Sigue de [[cyber-dev2]] (SCA) y prepara [[cyber-dev5]] (CI/CD y respuesta).

## De qué trata (y qué sabrás hacer al final)

Creer que tu código es seguro porque "lo escribiste con cuidado" es como creer que un texto no tiene erratas porque lo escribiste tú. La seguridad necesita **verificación**: herramientas y prácticas que busquen los fallos que se te escaparon. Esta lección reúne las técnicas de verificación que un científico de datos puede aplicar a sus repos sin ser pentester.

La intuición: verificar es tener varios revisores con superpoderes distintos. Uno lee el código buscando patrones peligrosos (SAST), otro lo bombardea con entradas raras a ver si se rompe (fuzzing), y otro —humano— entiende la intención y caza lo que las máquinas no ven (code review). Ninguno solo basta; juntos cubren mucho.

Al terminar podrás: (1) distinguir **SAST, DAST y SCA**; (2) entender **fuzzing** y por qué halla lo que las pruebas normales no; (3) hacer un **code review** con foco en seguridad; y (4) combinar técnicas según su punto ciego.

## Las familias de verificación

| Técnica | Qué examina | Punto fuerte | Punto ciego |
|---|---|---|---|
| **SAST** (estático) | Tu código fuente sin ejecutarlo | Patrones inseguros temprano y barato | Falsos positivos; no ve lógica de negocio |
| **DAST** (dinámico) | La app corriendo, desde fuera | Fallos en ejecución real (config, auth) | Solo lo que alcanza por la interfaz |
| **SCA** (composición) | Tus dependencias ([[cyber-dev2]]) | CVEs heredados | No tu propio código |
| **Fuzzing** | Comportamiento ante entradas raras | Crashes y casos no previstos | Necesita objetivos y tiempo |

La lección clave: **cada técnica tiene un punto ciego distinto**, por eso se combinan (defense in depth aplicado a la verificación). SAST sin SCA deja pasar la dependencia vulnerable; SCA sin SAST deja pasar tu propio bug.

## Fuzzing: romper a propósito

El **fuzzing** alimenta a un programa con entradas masivas, aleatorias o malformadas para provocar fallos (crashes, cuelgues, comportamiento inesperado). Halla lo que las pruebas normales no, porque tus pruebas usan entradas "razonables" y los ataques usan entradas **patológicas**: el archivo de 0 bytes, el string de 10 MB, el carácter raro, el número negativo donde esperabas positivo. Para un DS: fuzzear un parser de datos o una función que recibe entrada externa revela los casos borde que un dataset malicioso explotaría.

## Code review con foco en seguridad

La revisión humana caza lo que las herramientas no: errores de **lógica de autorización** ([[cyber-web2]]), supuestos de confianza rotos, secretos olvidados ([[cyber-dev1]]). Un checklist mental al revisar:

- ¿Hay alguna **entrada externa** que no se valida? ([[cyber-dev1]])
- ¿Se construye SQL/HTML/comandos concatenando? ([[cyber-web1]])
- ¿Algún **secreto** en el código o en logs? ([[cyber-dev1]])
- ¿La **autorización** se verifica por recurso? ([[cyber-web3]])
- ¿Los **errores** fallan hacia el lado seguro sin filtrar?
- ¿Alguna dependencia nueva sospechosa? ([[cyber-dev2]])

Revisar con estas preguntas convierte un code review normal en uno de seguridad sin volverte experto.

## Mini-ejemplo trabajado

Tu repo de un servicio de datos pasa los tests funcionales. ¿Está seguro? Plan de verificación por capas:

- **SCA:** escanea dependencias → detecta una librería con CVE crítico ([[cyber-dev2]]).
- **SAST:** marca una consulta SQL construida por concatenación → potencial inyección ([[cyber-web1]]).
- **Fuzzing:** lanza entradas raras al endpoint de carga → un CSV malformado tumba el servicio (manejo de errores deficiente).
- **Code review:** un humano nota que un endpoint no verifica el dueño del recurso (BOLA, [[cyber-web3]]) — invisible para las herramientas porque es lógica, no patrón.
- **Resultado:** cuatro técnicas, cuatro clases de fallo distintas; ninguna sola las habría hallado todas.

## Señales de reconocimiento

| Señal | Qué falta |
|---|---|
| "Pasan los tests, está seguro" | Tests funcionales ≠ verificación de seguridad |
| Solo SAST, sin SCA | Dependencias vulnerables sin ver |
| Sin fuzzing en parsers de entrada externa | Casos borde patológicos sin probar |
| Code review solo de estilo/funcionalidad | Bugs de lógica de seguridad sin cazar |
| Confiar en una sola herramienta | Su punto ciego queda descubierto |

## Errores típicos

- **Confundir tests funcionales con seguridad:** prueban el camino feliz, no el adversario.
- **Tratar el SAST como verdad absoluta:** tiene falsos positivos (triarlos) y falsos negativos (no lo ve todo).
- **Saltarse el code review humano:** la lógica de autorización casi siempre necesita ojos humanos.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** SAST revisa tu código, SCA tus dependencias, DAST la app corriendo y el code review humano caza la falla de autorización que ninguna herramienta ve.
- **Contraejemplo:** un pipeline que corre SAST + SCA en cada PR, fuzzing periódico de los parsers y code review con checklist de seguridad: las cuatro clases de fallo tienen una red que las atrapa.
- **Caso borde:** demasiados **falsos positivos** de SAST generan fatiga (como las alertas, [[cyber-blue2]]) y el equipo empieza a ignorar todo, incluidos los verdaderos. La verificación se calibra: priorizar hallazgos de alto impacto y afinar las reglas, no inundar.

## Transferencia a ciencia de datos e IA

Fuzzear un parser de datos es exactamente probar la robustez de tu ingesta contra datos malformados o **envenenados** ([[cyber-ml-security]]). El code review con foco en seguridad caza secretos en notebooks y lógica de acceso en APIs de modelo. Y la combinación de técnicas con puntos ciegos distintos es la misma filosofía que el monitoreo multi-señal del blue team ([[cyber-blue2]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** haz un code review del mini-ejemplo con el checklist de seguridad y lista los hallazgos por categoría.
- **Misión externa (lab vivo):** explora un módulo de **OpenSSF Training** (https://openssf.org/training/courses/) sobre verificación/testing de seguridad. **Criterio de cierre:** explicar el punto ciego de SAST y cómo lo cubre otra técnica.
- **Mini-entregable:** un plan de verificación para un repo: qué herramienta/práctica usas para cada clase de fallo (dependencias, inyección, casos borde, lógica de acceso).

---

> **Síntesis:** diseñar seguro no basta; hay que **verificar**. **SAST** (tu código), **SCA** (tus dependencias), **DAST** (la app corriendo) y **fuzzing** (entradas patológicas) tienen **puntos ciegos distintos**, por eso se combinan; y el **code review humano** caza la lógica de autorización que las máquinas no ven. Los tests funcionales no son verificación de seguridad, y la verificación se calibra para no morir de falsos positivos.

---

**Referencias**

- Wheeler, D. A. (n.d.). *Developing secure software (LFD121): Secure software development fundamentals*. Open Source Security Foundation. https://openssf.org/training/courses/

*Retrieval: (1) distingue SAST, DAST, SCA y fuzzing por lo que examinan; (2) ¿por qué el fuzzing halla lo que los tests normales no?; (3) ¿qué caza el code review humano que las herramientas no?; (4) ¿por qué se combinan técnicas con puntos ciegos distintos?*
