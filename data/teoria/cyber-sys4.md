# Aislamiento en profundidad: procesos, sandboxing y contenedores

> Recurso troncal: **UC Berkeley CS 161 — *Computer Security***. El aislamiento es cómo contienes el daño cuando algo falla. Sigue a [[cyber-sys3]] (identidad) y prepara [[cyber-sys5]] (ataques de red).

## De qué trata (y qué sabrás hacer al final)

Ninguna defensa es perfecta, así que la pregunta no es solo "¿cómo evito que entren?" sino "¿qué pasa **cuando** algo se compromete?". El **aislamiento** es la respuesta estructural: separar componentes para que un fallo en uno no contamine a los demás. Es la encarnación técnica de *defense in depth* y *least privilege* ([[cyber-ms2]]).

La intuición: un submarino tiene **compartimentos estancos**. Una vía de agua hunde un compartimento, no el barco, porque las mamparas contienen la inundación. El aislamiento de procesos y contenedores son esas mamparas: cuando un componente "se inunda" (es comprometido), el daño queda confinado.

Al terminar podrás: (1) explicar por qué el aislamiento **contiene** el daño; (2) distinguir procesos, **sandboxes** y **contenedores**; (3) entender qué aísla (y qué no) un contenedor; y (4) aplicar aislamiento a notebooks y jobs de datos.

## Por qué aislar contiene el daño

Recuerda de [[cyber-sys1]]: el SO separa la memoria de los procesos. El aislamiento extiende esa idea: si cada componente corre con **mínimo privilegio** y separado, comprometer uno no entrega el resto. Sin aislamiento, un solo bug (en una librería, en un script subido) puede tocar todo: datos, secretos, otros servicios. Con aislamiento, el atacante queda en una "celda" que aún debe romper para avanzar (lo que llamamos *escape*).

## Procesos, sandboxes y contenedores

| Mecanismo | Qué aísla | Fuerza típica |
|---|---|---|
| **Proceso** (SO) | Memoria entre procesos; permisos de usuario | Base; depende de no correr como root |
| **Sandbox** | Restringe lo que un proceso puede hacer (llamadas al SO, archivos, red) | Confina código no confiable |
| **Contenedor** (Docker) | Empaqueta app + dependencias con su propia vista de archivos/red/procesos | Aísla y hace reproducible |
| **VM / microVM** | Aísla a nivel de kernel/hardware | Más fuerte, más pesado |

La regla: **a mayor desconfianza del código, más fuerte el aislamiento**. Ejecutar código arbitrario (p. ej. el que genera un agente LLM, [[cyber-llm-rag-agents]]) exige sandbox/VM, no solo un proceso.

## Qué aísla un contenedor (y qué no)

Un contenedor es excelente para **empaquetar y reproducir** (mismas dependencias en todos lados, conecta con [[cyber-dev2]]) y aísla razonablemente, pero **comparte el kernel del host**: no es una barrera tan fuerte como una VM. Errores comunes que **rompen** su aislamiento:

- Correr el contenedor como **root** o con `--privileged` → un escape llega al host.
- Montar el socket de Docker o directorios sensibles del host dentro del contenedor.
- Incrustar **secretos** en la imagen (quedan en sus capas, recuperables — [[cyber-secure-dev]]).
- Imágenes base sin actualizar (heredan CVEs — [[cyber-dev2]]).

Un contenedor mal configurado da **falsa sensación** de aislamiento.

## Mini-ejemplo trabajado

Un equipo ejecuta notebooks de analistas y código de terceros en un mismo servidor, todo como el mismo usuario con acceso al dataset y a las llaves del cloud. Riesgo y rediseño:

- **Riesgo:** un notebook con una dependencia maliciosa ([[cyber-dev2]]) o un script subido corre con acceso total → lee datos, roba llaves, toca otros trabajos. Sin mamparas, una fuga lo inunda todo.
- **Rediseño con aislamiento:** cada job/notebook en su **contenedor** con usuario **no-root**, montando solo los datos que necesita (least privilege), sin las llaves del cloud salvo las imprescindibles y de alcance estrecho, y con red restringida. Código no confiable, en un sandbox más fuerte.
- **Resultado:** comprometer un notebook ya no entrega el dataset completo ni las llaves; el daño queda confinado a su celda.

## Señales de reconocimiento

| Señal | Riesgo de aislamiento |
|---|---|
| Todo corre como el mismo usuario/root | Un fallo = compromiso total |
| Contenedor `--privileged` o con socket de Docker montado | Escape trivial al host |
| Secretos dentro de la imagen | Recuperables de las capas |
| Código no confiable en un proceso normal | Falta sandbox |
| "Está en un contenedor, es seguro" | Comparte kernel; config puede anular el aislamiento |

## Errores típicos

- **Tratar el contenedor como una VM:** comparte kernel; no asumas aislamiento de nivel hardware.
- **Correr como root por comodidad:** anula least privilege y facilita el escape.
- **Meter secretos en la imagen:** viven en las capas; usa inyección en tiempo de ejecución ([[cyber-secure-dev]]).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** ejecutas código poco confiable en un contenedor no-root, sin secretos en la imagen y con base actualizada, subiendo la fuerza del aislamiento según la desconfianza.
- **Contraejemplo:** jobs en contenedores no-root, con datos montados al mínimo, sin secretos en la imagen y con red restringida: una dependencia maliciosa queda contenida y no alcanza llaves ni otros datos. Mamparas que funcionan.
- **Caso borde:** dos contenedores "aislados" que comparten un **volumen** o una **red** sin restricción pueden comunicarse y propagar el compromiso; el aislamiento se evalúa también en lo que comparten, no solo en lo que separan.

## Transferencia a ciencia de datos e IA

El aislamiento es cómo ejecutas con seguridad **código no confiable** que genera un agente LLM ([[cyber-llm-rag-agents]]), cómo limitas qué puede tocar un pipeline de entrenamiento ([[cyber-ml-security]]) y cómo contienes una dependencia comprometida ([[cyber-dev2]]). Reproducibilidad (contenedores) y seguridad (aislamiento) van de la mano en MLOps.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** rediseña el mini-ejemplo enumerando qué montas, con qué usuario y qué red para cada contenedor.
- **Misión externa (lab vivo):** practica permisos y confinamiento en **OverTheWire: Bandit** (https://overthewire.org/wargames/bandit/). **Criterio de cierre:** explicar cómo los permisos limitan lo que un proceso comprometido puede hacer. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable:** un esquema de aislamiento para un entorno de ejecución de notebooks/jobs (usuario, datos montados, secretos, red) con su justificación.

---

> **Síntesis:** el aislamiento **contiene** el daño cuando algo falla: compartimentos estancos para tu sistema. Procesos < sandboxes < contenedores < VMs en fuerza; **a mayor desconfianza del código, más fuerte el aislamiento**. Un **contenedor** empaqueta y aísla razonablemente pero comparte el kernel y su config (root, `--privileged`, secretos en la imagen, volúmenes compartidos) puede anular esa protección. Aplícalo con **mínimo privilegio** a notebooks, jobs y código no confiable.

---

**Referencias**

- Wagner, D., Weaver, N., Kao, P., Shakir, F., Law, A., & Ngai, N. (2024). *Computer security* (CS 161). University of California, Berkeley.
- OverTheWire. (n.d.). *Bandit wargame*. https://overthewire.org/wargames/bandit/

*Retrieval: (1) ¿por qué el aislamiento contiene el daño?; (2) ordena proceso/sandbox/contenedor/VM por fuerza; (3) ¿qué NO aísla un contenedor y qué config lo rompe?; (4) ¿por qué código no confiable exige sandbox/VM?*
