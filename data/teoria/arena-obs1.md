# ¿Qué es observabilidad? Monitoreo vs. observabilidad

El término **observabilidad** lo acuñó Rudolf Kálmán (1960) en teoría de control: una medida de qué tan bien se pueden inferir los **estados internos** de un sistema a partir de sus **salidas externas**. Aplicado al software, un sistema es observable en la medida en que puedes **entender y explicar cualquier estado en que pueda caer —por nuevo o extraño que sea— sin tener que desplegar código nuevo** para explicarlo.

## La prueba de fuego

¿Puedes responder preguntas abiertas e iterativas sobre tu sistema sin haber **predicho de antemano** que necesitarías esa métrica? Ej.: «de los usuarios que se quejaron de timeouts, ¿qué tienen en común si mis percentiles p99/p99.9 se ven rápidos?». Si para responder tienes que enviar código o configurar un monitor primero, **no tienes observabilidad**.

## Monitoreo es para *known-unknowns*; observabilidad para *unknown-unknowns*

- **Monitoreo** (métricas + dashboards + umbrales): comprueba condiciones contra umbrales conocidos. Es **fundamentalmente reactivo** — solo detecta modos de fallo que **ya anticipaste**. Funciona cuando el sistema es lo bastante simple para predecir cómo fallará.
- **Observabilidad**: investigación exploratoria iterativa para hallar el porqué de **cualquier** fallo, conocido o no. En sistemas distribuidos modernos (microservicios, 20-30 saltos de red por petición, autoescalado, polyglot persistence) los modos de fallo nuevos superan la capacidad de cualquiera para predecir dashboards.

## Por qué fallan las métricas: cardinalidad y dimensionalidad

- **Métrica** = un solo número preagregado con etiquetas; barato y de huella predecible, pero la **preagregación es el nivel mínimo de granularidad** y oculta al usuario individual.
- **Cardinalidad** = nº de valores únicos de un campo. Los IDs únicos (UUID, user_id, request_id) son de **alta cardinalidad** — y *la alta cardinalidad es casi siempre lo más útil para depurar* (encontrar la aguja en el pajar). Las métricas solo manejan baja cardinalidad a escala razonable.
- **Dimensionalidad** = nº de claves por evento. Los eventos observables son **arbitrariamente anchos** (cientos o miles de pares clave-valor): a más dimensiones, más correlaciones ocultas puedes descubrir.

## Sistema vs. software

Regla práctica: el **monitoreo** sirve para la salud del **sistema/infraestructura** (cambia poco, predecible: CPU, memoria, disco → autoescalado, capacity planning); la **observabilidad** sirve para el **software** que escribes (cambia a diario, impredecible, lo que viven tus clientes). Coexisten; excepción: métricas de infra de alto orden (CPU/mem/disco) que avisan de impacto en el código sí valen junto a tu observabilidad.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| «Crearé un dashboard para esto» | ¿Y para el fallo que aún no imaginaste? Los known-unknowns no bastan |
| Quieres filtrar por user_id / request_id | Alta cardinalidad → métricas no llegan; necesitas eventos anchos |
| «El promedio se ve bien» pero hay quejas | La métrica preagregada oculta al usuario individual; baja a eventos |
| Fallo nuevo y nunca visto | unknown-unknown → observabilidad, no monitoreo |
| ¿Monitoreo o observabilidad? | Sistema/infra → monitoreo; tu código/cliente → observabilidad |

---

> **Síntesis:** observabilidad = entender **cualquier** estado nuevo o extraño **sin desplegar código nuevo**, troceando datos de **alta cardinalidad y alta dimensionalidad** de forma iterativa. El monitoreo (métricas/umbrales) es reactivo y solo cubre **known-unknowns**; la observabilidad persigue los **unknown-unknowns** de los sistemas distribuidos modernos.

---

*Retrieval: (1) define observabilidad en una frase y da su prueba de fuego; (2) ¿por qué monitoreo = known-unknowns y observabilidad = unknown-unknowns?; (3) ¿qué son cardinalidad y dimensionalidad y por qué hunden a las métricas?; (4) ¿cuándo monitoreo y cuándo observabilidad (sistema vs. software)?*
