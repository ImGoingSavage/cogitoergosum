# Diseño seguro: requisitos, principios y modelado de amenazas en el código

> Recurso troncal: **OpenSSF / Wheeler, *Secure Software Development Fundamentals***. Antes de validar entradas ([[cyber-dev1]]) o cazar dependencias ([[cyber-dev2]]), hay que **decidir** la seguridad. Sigue en [[cyber-dev4]] (SAST, fuzzing, code review).

## De qué trata (y qué sabrás hacer al final)

La mayoría de las vulnerabilidades no se "introducen" al final: se **diseñan** sin querer al principio, cuando nadie escribió la seguridad como un requisito. Esta lección te da el método para que la seguridad sea una decisión explícita del diseño, no un parche tardío. Es [[cyber-ms2]] (principios defensivos) aplicado al momento de escribir software.

La intuición: construir software sin requisitos de seguridad es como construir una casa sin decidir dónde van las puertas con llave. Puedes ponerlas después rompiendo paredes (caro, incompleto) o decidirlas en el plano (barato, coherente). El diseño seguro es ponerlas en el plano.

Al terminar podrás: (1) escribir **requisitos de seguridad** junto a los funcionales; (2) aplicar principios de diseño seguro (Saltzer & Schroeder) al código; (3) hacer **threat modeling** a nivel de componente; y (4) reconocer cuándo una decisión de diseño crea deuda de seguridad.

## La seguridad como requisito

Un requisito funcional dice "el usuario puede subir su CV". Un requisito de seguridad acompaña: "solo el dueño y RRHH pueden leerlo; el archivo se valida y se guarda aislado; un fallo niega el acceso". Sin ese segundo enunciado, el equipo improvisa y casi siempre falla abierto. Escribir requisitos de seguridad —qué entradas son no confiables, qué datos no deben salir, qué permisos mínimos, qué debe pasar ante un error— convierte la seguridad en algo **comprobable**, no en buena voluntad.

## Principios de diseño seguro (Saltzer & Schroeder, vigentes desde 1975)

| Principio | Idea | En tu código |
|---|---|---|
| **Economía de mecanismo** | Lo simple se audita; lo complejo esconde fallos | Una ruta de autorización clara, no diez excepciones |
| **Fail-safe defaults** | Ante la duda, negar | Permiso denegado por defecto, se concede explícito |
| **Mediación completa** | Verificar el acceso en **cada** petición | Autorizar por recurso siempre, no solo al entrar |
| **Diseño abierto** | No depender del secreto del diseño | La seguridad no descansa en "que nadie sepa cómo funciona" |
| **Privilegio mínimo** | El mínimo permiso necesario | Cada componente con su credencial acotada |
| **Mecanismo menos común** | Menos recursos compartidos = menos vías de ataque | Aislar lo que no necesita compartirse |

Estos principios no envejecen: casi toda vulnerabilidad viola uno. Reconocer **cuál** viola un diseño te dice cómo arreglarlo.

## Threat modeling a nivel de componente

Lleva las 4 preguntas de [[cyber-ms2]] a cada componente que diseñas: ¿qué datos entran y de quién (confiable o no)? ¿qué frontera de confianza cruza? ¿qué pasa si esta parte es comprometida —qué alcanza? Un diagrama simple de flujo de datos (de dónde viene cada entrada, dónde se valida, qué permisos usa) revela los puntos donde falta validación o sobra privilegio antes de escribir una línea.

## Mini-ejemplo trabajado

Diseñas un servicio que recibe un CSV de un usuario, lo procesa y guarda resultados en la BD. Diseño seguro vs improvisado:

- **Improvisado:** acepta el archivo, lo parsea con una librería que ejecuta fórmulas, usa una credencial de BD con permisos totales, y ante un error muestra el stack trace. Viola fail-safe (error verboso), privilegio mínimo (credencial total) y mediación (¿quién puede subir?).
- **Diseño seguro (requisitos primero):** "solo usuarios autenticados suben; el CSV se valida (tipo, tamaño, columnas) y se parsea sin ejecutar nada ([[cyber-web5]]); la credencial de BD es de **escritura solo en su tabla**; un error devuelve mensaje genérico y registra detalle interno sin datos sensibles". Cada requisito mapea a un principio.
- **Resultado:** la seguridad está en el plano; implementar es seguir los requisitos, no recordarlos.

## Señales de reconocimiento

| Señal | Principio violado |
|---|---|
| "Le ponemos permisos finos después" | Privilegio mínimo / fail-safe |
| Autorización solo al iniciar sesión, no por recurso | Mediación completa |
| "Es seguro porque nadie conoce el endpoint" | Diseño abierto (seguridad por oscuridad) |
| Lógica de acceso con muchas excepciones | Economía de mecanismo |
| Sin requisitos de seguridad escritos | Seguridad como ocurrencia, no diseño |

## Errores típicos

- **Seguridad por oscuridad:** confiar en que el atacante no conozca el diseño; los diseños se filtran y se deducen.
- **Diseñar solo el camino feliz:** sin pensar qué pasa cuando una entrada es hostil o un componente cae.
- **Permisos amplios "temporales":** que se vuelven permanentes y violan privilegio mínimo.

## Contraejemplo y caso borde

- **Contraejemplo:** un servicio con requisitos de seguridad escritos, autorización por recurso en cada llamada, credenciales mínimas y fail-safe: las vulnerabilidades comunes simplemente no caben en el diseño.
- **Caso borde:** la **economía de mecanismo** puede chocar con features legítimas que requieren complejidad (reglas de negocio reales). El principio no dice "no tengas lógica", dice "haz la lógica de **seguridad** tan simple y auditable como puedas", aislándola de la complejidad del negocio.

## Transferencia a ciencia de datos e IA

Diseñar requisitos de seguridad es lo que hace que un pipeline ML nazca seguro ([[cyber-ml-security]]): qué fuentes de datos son confiables, qué credenciales mínimas usa cada etapa, qué pasa si una falla. La mediación completa es el control de acceso por recurso de tus APIs ([[cyber-web3]]) y por documento de un RAG ([[cyber-llm-rag-agents]]). El diseño seguro es el plano de toda la ruta.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el servicio del mini-ejemplo, escribe 5 requisitos de seguridad y di qué principio cumple cada uno.
- **Misión externa (lab vivo):** revisa el módulo de **diseño seguro/requisitos** en **OpenSSF Training** (https://openssf.org/training/courses/). **Criterio de cierre:** nombrar dos principios de Saltzer & Schroeder y un ejemplo propio de cada uno.
- **Mini-entregable:** los requisitos de seguridad (no funcionales) de un componente que vayas a construir, mapeados a principios.

---

> **Síntesis:** la seguridad se **diseña**, no se parchea: escribe **requisitos de seguridad** junto a los funcionales y aplica los principios de **Saltzer & Schroeder** —economía de mecanismo, **fail-safe defaults**, **mediación completa**, diseño abierto (nada de seguridad por oscuridad), **privilegio mínimo**—. Modela amenazas por componente (qué entra, qué frontera cruza, qué alcanza si cae) antes de escribir código. Casi toda vulnerabilidad viola un principio; reconocer cuál te dice cómo arreglarla.

---

**Referencias**

- Wheeler, D. A. (n.d.). *Developing secure software (LFD121): Secure software development fundamentals*. Open Source Security Foundation. https://openssf.org/training/courses/
- Saltzer, J. H., & Schroeder, M. D. (1975). The protection of information in computer systems. *Proceedings of the IEEE, 63*(9), 1278–1308.

*Retrieval: (1) ¿qué es un requisito de seguridad y por qué escribirlo?; (2) define fail-safe defaults y mediación completa; (3) ¿qué es seguridad por oscuridad y por qué falla?; (4) ¿cómo se hace threat modeling por componente?*
