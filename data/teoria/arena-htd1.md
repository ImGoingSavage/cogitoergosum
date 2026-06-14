# Deuda técnica oculta en ML I: fundamentos y erosión de fronteras

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
