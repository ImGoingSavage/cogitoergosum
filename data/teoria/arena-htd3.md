# Deuda técnica oculta en ML III: anti-patrones de sistema y configuración

Solo una **fracción diminuta** del código de un sistema ML real se dedica a aprender/predecir (la famosa Figura 1: una cajita negra en medio de una infraestructura vasta); el resto es **"plumbing"** (fontanería). Es común que los sistemas con ML acaben con anti-patrones de alta deuda.

## Glue code

Los investigadores ML desarrollan soluciones de propósito general como **paquetes auto-contenidos** (mloss.org, in-house, cloud). Usarlos genera **glue code**: una masa enorme de código de soporte para meter y sacar datos de paquetes genéricos. Es costoso porque **congela el sistema a las peculiaridades de un paquete** (testear alternativas se vuelve prohibitivo) e **inhibe mejoras** (dificulta explotar propiedades del dominio). Un sistema maduro puede ser **≤5% código ML y ≥95% glue code**; a veces sale más barato una **solución nativa limpia** que reusar un paquete genérico. **Mitigación:** envolver los paquetes black-box en **APIs comunes** → infraestructura reusable y menor coste de cambiar de paquete.

## Pipeline jungles

Caso especial de glue code en la **preparación de datos**: crecen orgánicamente al añadir señales incrementalmente, hasta volverse una **jungla de scrapes, joins y pasos de sampling** con archivos intermedios. Gestionarlas, detectar errores y recuperarse de fallos es difícil; testearlas exige **tests de integración end-to-end caros**. **Solo se evitan pensando holísticamente** sobre recolección de datos y extracción de features; el rediseño **clean-slate** (tirar la jungla y rehacer) es una gran inversión que reduce drásticamente costes y acelera la innovación. **Raíz** de glue code y pipeline jungles: roles **research vs engineering demasiado separados**; un enfoque **híbrido** (ingenieros e investigadores en el mismo equipo, a menudo las mismas personas) reduce mucho la fricción.

## Dead experimental codepaths

Consecuencia del glue code/pipeline jungles: se vuelve tentador experimentar con métodos alternativos como **ramas condicionales dentro del código principal**. Para un cambio individual el coste es bajo, pero con el tiempo acumulan deuda: dificultan la **compatibilidad hacia atrás**, aumentan exponencialmente la **complejidad ciclomática** y vuelven imposible testear todas las interacciones. Ejemplo célebre del peligro: **Knight Capital perdió 465 millones de dólares en 45 minutos** por comportamiento inesperado de codepaths experimentales obsoletos. **Mitigación** (como los *dead flags* del software tradicional): reexaminar periódicamente cada rama y **arrancar** lo que no se use (a menudo solo se usa un subconjunto pequeño).

## Abstraction debt y smells

- **Abstraction debt:** falta de abstracciones fuertes para ML. Nada en ML iguala el éxito de la **base de datos relacional** como abstracción; ¿cuál es la interfaz correcta para un stream de datos, un modelo, una predicción? En aprendizaje distribuido, el uso masivo de **Map-Reduce** vino del vacío de abstracciones, pese a ser **mala abstracción para algoritmos ML iterativos**; el **parameter-server** es más robusto pero hay especificaciones que compiten.
- **Common smells** (indicadores subjetivos, no reglas duras): **Plain-Old-Data-Type smell** (info rica codificada en floats/ints crudos; un parámetro debería saber si es un log-odds multiplier o un decision threshold); **Multiple-Language smell** (mezclar lenguajes encarece testing y transferir ownership); **Prototype smell** (depender regularmente de un entorno de prototipo indica fragilidad; los resultados a pequeña escala rara vez reflejan el full scale).

## Configuration debt

Otra área sorprendente de deuda. En un sistema maduro, las **líneas de configuración pueden superar a las de código tradicional**, y cada una puede contener un error; config suele tratarse como algo secundario (sin verificación ni testing). Ejemplos reales de "desorden": la feature A se logueó mal del 9/14 al 9/17; B no está disponible antes del 10/7; C cambia de cómputo por el formato de logging; D no está en producción y exige sustitutas D'/D''; usar Z exige memoria extra; Q impide usar R por latencia. **Principios de buena configuración:** (1) fácil especificar una config como pequeño **cambio** sobre una previa; (2) **difícil** cometer errores/omisiones manuales; (3) fácil **ver visualmente** la diferencia entre dos modelos; (4) fácil **aseverar/verificar** automáticamente hechos básicos (nº de features, clausura transitiva de dependencias); (5) posible **detectar settings** no usados o redundantes; (6) las configs deben pasar **code review** y vivir en un repositorio.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| 95% del código es para meter datos en un paquete genérico | Glue code: envuelve el black-box en una API común |
| Preparación de datos = jungla de scrapes/joins/sampling | Pipeline jungle: rediseño clean-slate; piensa holísticamente |
| Experimentos como if/else en el código principal | Dead codepaths (Knight Capital $465M): arráncalos periódicamente |
| Map-Reduce para ML iterativo | Mala abstracción; considera parameter-server |
| Parámetros como floats crudos sin significado | Plain-Old-Data-Type smell |
| Más líneas de config que de código, sin review | Configuration debt: aplica los 6 principios y code-review |

---

> **Síntesis:** el código ML es mayormente **plumbing**. Evita el **glue code** envolviendo paquetes en APIs comunes; las **pipeline jungles** con rediseño holístico; los **dead experimental codepaths** arrancándolos (Knight Capital perdió $465M por ellos). Hay **abstraction debt** (Map-Reduce es mala abstracción para ML iterativo) y **smells** (plain-old-data-type, multiple-language, prototype). La **configuration debt** puede superar al código: trátala con principios de diff fácil, verificación automática y **code review**.

---

*Retrieval: (1) ¿qué es el glue code y cómo se mitiga?; (2) ¿qué es una pipeline jungle y cuál es su raíz organizacional?; (3) ¿por qué son peligrosos los dead experimental codepaths (caso Knight Capital)?; (4) cita 3 principios de buena configuración.*
