# Deuda técnica oculta en ML I: fundamentos y erosión de fronteras

## De qué trata esta lección (y qué sabrás hacer al final)

Los sistemas de ML tienen una capacidad **especial** de acumular deuda técnica: además de todos los problemas del código normal, sufren una clase propia que vive a nivel de **sistema, no de código** —porque los datos corrompen sutilmente las abstracciones—. Esta lección construye, desde cero, los tres mecanismos que erosionan las fronteras de un sistema de ML: el **entanglement** (principio CACE), las **correction cascades** y los **undeclared consumers**.

Al terminar podrás: (1) entender por qué la deuda de ML no se paga como la de código (refactor+tests no bastan); (2) enunciar el principio CACE (*Changing Anything Changes Everything*) y a qué aplica; (3) reconocer una correction cascade y por qué crea deadlock de mejora; y (4) prevenir los undeclared consumers con SLAs y control de acceso. El ejemplo de CACE con tres features hace de hilo. Es el primero de cuatro sobre el clásico paper de Google "Hidden Technical Debt in ML".

## ¿Qué es la deuda técnica y por qué el ML tiene una capacidad especial?

**Deuda técnica** (metáfora de Ward Cunningham, 1992): los costes de largo plazo de moverse rápido. No toda deuda es mala, pero **toda deuda debe servirse**. Se paga refactorizando código, mejorando tests, borrando código muerto, reduciendo dependencias, ajustando APIs y mejorando documentación. La meta **no es añadir funcionalidad** sino permitir mejoras futuras, reducir errores y mejorar mantenibilidad. La **deuda oculta es peligrosa porque se compone silenciosamente**.

Los sistemas de ML tienen una **capacidad especial** de incurrir deuda: tienen todos los problemas del código tradicional **más** un conjunto de issues ML-específicos. Esta deuda es difícil de detectar porque existe a **nivel de SISTEMA, no a nivel de código**: las abstracciones tradicionales se corrompen sutilmente porque **los datos influyen en el comportamiento**. Los métodos típicos para pagar deuda de código **no bastan** a nivel de sistema.

## Modelos complejos erosionan las fronteras

Las **fronteras de abstracción fuertes** (encapsulación, diseño modular) hacen el código mantenible, pero son difíciles de imponer en ML porque **el comportamiento deseado no puede expresarse en lógica de software sin dependencia de datos externos** — el ML se usa justo cuando no se puede.

### Entanglement y el principio CACE
El ML **entrelaza** las señales: aislar mejoras es imposible. Si un modelo usa features x₁…xₙ y cambias la distribución de x₁, la importancia/pesos/uso de las **demás** features pueden cambiar; añadir o quitar una feature también. Esto es el **principio CACE: Changing Anything Changes Everything** ("cambiar cualquier cosa lo cambia todo"). CACE aplica no solo a inputs, sino a **hiperparámetros, learning settings, sampling, thresholds de convergencia, selección de datos** y casi cualquier otro ajuste.

**Mitigaciones:** (1) **aislar modelos y servir ensembles** — útil cuando los subproblemas se descomponen (multi-clase disjunta) o los errores de los componentes están **no correlacionados**; cuidado: si los errores se correlacionan, **mejorar un componente puede empeorar el sistema**. (2) **Detectar cambios** en la predicción (herramientas de visualización de alta dimensión, métricas slice-by-slice).

### Correction cascades
Existe un modelo mₐ para el problema A y se necesita resolver A' (ligeramente distinto). Es tentador aprender mₐ' que **toma mₐ como input** y aprende una pequeña corrección. Pero esto crea una **dependencia nueva**: analizar mejoras a mₐ se vuelve mucho más caro, y si se **encadenan** correcciones (mₐ'' sobre mₐ'…) se crea un **deadlock de mejora** — mejorar un componente individual empeora el sistema. **Mitigación:** aprender las correcciones **dentro del mismo modelo** (añadir features que distingan los casos) o aceptar el coste de un **modelo separado** para A'.

### Undeclared consumers (deuda de visibilidad)
La predicción de mₐ suele ser **ampliamente accesible** (runtime, archivos, logs) y otros sistemas la consumen **sin declararlo** (visibility debt). Son **caros y peligrosos**: crean un **acoplamiento fuerte oculto** de mₐ al resto del stack; cambios en mₐ (¡aun mejoras!) impactan a esos consumidores de forma no intencionada, encareciendo radicalmente cualquier cambio. Además crean **hidden feedback loops**. **Prevención:** controles de acceso o **SLAs estrictos**; sin barreras, los ingenieros usan la señal más conveniente bajo presión de plazos.

---

## Mini-ejemplo trabajado: CACE en acción

Tu modelo de ranking usa 3 features: `precio`, `rating`, `popularidad`. Mides la importancia y `popularidad` aporta el 30%. Un equipo de datos "mejora" la feature `precio` (antes en dólares, ahora normalizada 0-1). No tocaste `popularidad`… pero al reentrenar, su importancia cae al 18% y el modelo se descalibra.

¿Por qué? Porque el modelo aprende **pesos conjuntos**: cambiar la escala de una feature redistribuye cómo el modelo reparte el crédito entre **todas** las demás. Eso es **CACE — Changing Anything Changes Everything**. Y no aplica solo a features: cambiar el learning rate, el umbral de convergencia, el muestreo o el threshold de decisión tiene el mismo efecto de onda.

**Predicción antes de seguir:** para "arreglar" un caso especial, decides entrenar un segundo modelo m_a' que toma la salida de m_a y le suma una corrección. ¿Qué deuda creas? Una **correction cascade**: ahora mejorar m_a puede *empeorar* el sistema (m_a' aprendió a compensar sus errores) → deadlock de mejora. Mejor mete el caso especial *dentro* de m_a con una feature que lo distinga.

## Prototipo, contraejemplo y caso borde

- **Prototipo (entanglement gestionado):** ensemble de submodelos con errores **no correlacionados** y detección de cambios slice-by-slice → aíslas mejoras.
- **Contraejemplo (ensemble que engaña):** componentes con errores **correlacionados**; mejorar uno empeora el sistema, justo lo contrario de lo que esperabas.
- **Caso borde (undeclared consumer):** otro equipo empezó a leer tu predicción desde un log; tu "mejora" rompe su sistema sin que lo sepas → acoplamiento oculto.

## Errores típicos

- **Conceptual:** tratar la deuda de ML como deuda de código (refactor + tests) cuando vive a **nivel de sistema** (los datos corrompen las abstracciones).
- **De diseño:** parchear modelo sobre modelo (cascada) en vez de añadir features que distingan los casos.
- **De gobernanza:** exponer la predicción sin SLA ni control de acceso → consumidores no declarados bajo presión de plazos.

## Transferencia isomorfa

La deuda técnica del ML reescribe principios clásicos de ingeniería:

- **Undeclared consumers ↔ acoplamiento por contrato de API roto:** consumir una salida sin declararlo es el mismo antipatrón que depender de un detalle interno no documentado; la cura (SLA/access control) es la **encapsulación** de siempre (conecta con [[arena-sd2]], bloques distribuidos).
- **CACE ↔ acoplamiento global / variables compartidas:** "cambiar algo lo cambia todo" es la versión-ML del estado global mutable que hace frágil cualquier sistema.
- **Correction cascade ↔ herencia/parches apilados:** modelo-sobre-modelo es como una jerarquía de overrides que nadie puede tocar sin romper la siguiente capa.

Moraleja de la arista: *en ML los datos disuelven las fronteras; CACE, cascadas y consumidores ocultos son acoplamiento clásico amplificado — y se combaten con aislamiento, features que distingan casos y contratos explícitos.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «Moverse rápido salió gratis» | La deuda oculta se compone en silencio; toda deuda debe servirse |
| Cambié una feature y todo se descalibró | CACE: Changing Anything Changes Everything |
| Quiero parchear mₐ para un problema casi-igual | Cuidado con la correction cascade: deadlock de mejora |
| Otros equipos leen mi output sin avisar | Undeclared consumers (visibility debt): pon SLAs/access controls |
| Mejoré un componente y el sistema empeoró | Errores correlacionados en el ensemble / entanglement |

---

> **Síntesis:** el ML tiene capacidad **especial** de deuda porque vive a nivel de **sistema** (los datos corrompen las abstracciones). Las fronteras se erosionan por **entanglement** (principio **CACE**: cambiar algo lo cambia todo), **correction cascades** (parchear un modelo sobre otro crea deadlock de mejora) y **undeclared consumers** (acoplamiento oculto por consumir una predicción sin declararlo). Mitiga con ensembles aislados, detección de cambios, features que distingan casos y SLAs/control de acceso.

---

*Retrieval: (1) ¿por qué el ML tiene capacidad especial de deuda (nivel sistema vs código)?; (2) enuncia el principio CACE y a qué aplica; (3) ¿qué es una correction cascade y por qué crea deadlock?; (4) ¿qué son los undeclared consumers y cómo se previenen?*
