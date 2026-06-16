# Pensar en seguridad: activos, amenazas y el vocabulario del riesgo

> Recurso troncal: **Anderson, *Security Engineering* (3.ª ed.)**. Esta es la lección cero de toda la ruta: sin este vocabulario, las demás se vuelven anécdotas sueltas. Conecta con [[cyber-ms2]] (diseño defensivo).

## De qué trata (y qué sabrás hacer al final)

La mayoría cree que "seguridad" es poner un antivirus o una contraseña larga. Eso es como creer que la salud es tomar una pastilla. La seguridad real es una **propiedad de un sistema completo** —personas, código, datos, incentivos— y empieza por una pregunta incómoda: *¿qué puede salir mal aquí, y a quién le importa que salga mal?*

Antes del formalismo, la intuición: imagina que cuidas una casa. No proteges "la casa" en abstracto; proteges **cosas concretas** (las joyas, los niños, tu privacidad) contra **alguien** (un ladrón oportunista, un vecino chismoso) que aprovecha **una debilidad** (la ventana sin seguro) para causar **un daño** (robo, miedo), y lo enfrentas con **medidas** proporcionales (una reja, no un foso con cocodrilos).

Al terminar podrás: (1) nombrar con precisión **activo, amenaza, vulnerabilidad, impacto y control**; (2) aplicar la **tríada CIA**; y (3) traducir un sistema de ciencia de datos a ese vocabulario en vez de hablar de "hackeos" en general.

## El vocabulario mínimo

| Término | Pregunta que responde | Ejemplo en una app de datos |
|---|---|---|
| **Activo** | ¿Qué vale la pena proteger? | Dataset de pacientes, API key, modelo entrenado |
| **Amenaza** | ¿Qué evento malo puede pasar? | Robo del dataset, abuso de la API |
| **Vulnerabilidad** | ¿Qué debilidad lo permite? | La key está en un notebook público |
| **Impacto** | ¿Cuánto duele si pasa? | Multa, daño a personas, pérdida del modelo |
| **Control** | ¿Qué reduce el riesgo? | Secret manager, rotación de keys, acceso mínimo |

**Riesgo** no es ninguno de ellos por separado: es, informalmente, *probabilidad × impacto*. Una vulnerabilidad sin amenaza creíble ni impacto serio es ruido; una amenaza grave sobre un activo crítico con una vulnerabilidad abierta es una emergencia.

## La tríada CIA

Toda propiedad de seguridad se reduce casi siempre a tres garantías sobre un activo:

- **Confidencialidad (C):** solo quien debe, puede *ver* el dato. (Roto: una fuga del dataset.)
- **Integridad (I):** el dato no se altera sin autorización. (Roto: alguien envenena tus etiquetas de entrenamiento.)
- **Disponibilidad (A):** el dato/servicio está accesible cuando se necesita. (Roto: un proceso satura tu API y nadie más la usa.)

La tríada es un *checklist de imaginación*: ante cualquier activo, pregúntate qué pasaría si se rompiera su C, su I o su A. Casi siempre uno de los tres es el que de verdad importa, y descubrir cuál es ya media defensa.

## Mini-ejemplo trabajado

Un científico de datos guarda `clientes.csv` (datos personales) en un repo de GitHub y, para que "funcione el notebook", pega la API key de la base de datos en una celda. Traduzcamos:

- **Activo:** `clientes.csv` (personas reales) y la API key (acceso a la BD).
- **Amenaza:** alguien encuentra el repo y descarga ambos.
- **Vulnerabilidad:** repo público + secreto en texto plano en el notebook.
- **Impacto:** fuga de datos personales (rompe **C**), y con la key, alteración o borrado de la BD (rompe **I** y **A**).
- **Control proporcional:** repo privado, secreto fuera del código (variable de entorno / secret manager), y permisos mínimos para esa key.

Fíjate que no dijimos "lo hackearon". Nombramos *qué* se pierde y *por qué*. Esa precisión es el oficio.

## Señales de reconocimiento

| Señal en una conversación | Qué pensar |
|---|---|
| "Pero nadie va a entrar a esto" | Estás asumiendo la amenaza en cero sin evidencia |
| "Está protegido con contraseña" | ¿Protege C, I o A? ¿contra quién? |
| "Es un dato interno, no pasa nada" | ¿Es activo? ¿qué impacto si se filtra? |
| "Le ponemos seguridad después" | La seguridad retro-encajada casi nunca cubre el diseño |

## Errores típicos

- **Confundir vulnerabilidad con riesgo:** "tenemos 200 vulnerabilidades" no dice nada sin activos, amenazas e impacto. Tres de esas 200 pueden ser todo el riesgo real.
- **Proteger la tecnología, no el activo:** blindar el servidor mientras el dataset sensible viaja por correo.
- **Pensar en "el hacker" genérico:** sin un adversario concreto (oportunista, interno, competidor) no puedes dimensionar nada.

## Contraejemplo y caso borde

- **Contraejemplo:** una contraseña de 40 caracteres en una cuenta cuyo dato no le importa a nadie y que no da acceso a nada: esfuerzo de seguridad mal asignado. Mucho control sobre un no-activo.
- **Caso borde:** un dato **público** (un dataset abierto) parece sin riesgo de **C**, pero su **I** sí importa: si alguien lo altera y entrenas con la versión corrupta, el daño es real aunque la confidencialidad no aplique.

## Transferencia a ciencia de datos e IA

El pipeline de un DS está lleno de activos invisibles: *features* derivadas de datos sensibles, *embeddings* que pueden filtrar el texto original, *modelos* que costaron miles de horas de cómputo, *credenciales* de cloud. Cada uno tiene su C/I/A. La disciplina de nombrarlos es exactamente la misma que usarás en los clusters de [[cyber-data-privacy]], [[cyber-ml-security]] y [[cyber-llm-rag-agents]].

## Práctica, misión externa y mini-entregable

- **Práctica interna:** toma tu proyecto actual y lista 5 activos; para cada uno marca cuál de C/I/A es el que más duele perder.
- **Misión externa (lab vivo):** explora el **NIST Cybersecurity Framework** (https://www.nist.gov/cyberframework) y ubica las funciones *Identify* y *Protect*. **Criterio de cierre:** poder explicar con tus palabras qué cubre "Identify".
- **Mini-entregable:** una tabla de 5 filas (activo · amenaza · vulnerabilidad · impacto · control) de un sistema que conozcas.

---

> **Síntesis:** la seguridad es una propiedad del sistema, no un producto. Se piensa con un vocabulario preciso —**activo, amenaza, vulnerabilidad, impacto, control**— y se mide como **riesgo ≈ probabilidad × impacto**. La **tríada CIA** (confidencialidad, integridad, disponibilidad) es el checklist de imaginación que aplicas a cada activo.

---

**Referencias**

- Anderson, R. (2020). *Security engineering: A guide to building dependable distributed systems* (3rd ed.). Wiley.
- National Institute of Standards and Technology. (2018). *Framework for improving critical infrastructure cybersecurity* (v1.1). https://www.nist.gov/cyberframework

*Retrieval: (1) define activo vs vulnerabilidad vs riesgo; (2) ¿qué rompe cada letra de CIA?; (3) ¿por qué "nadie va a entrar" es un error de razonamiento?*
