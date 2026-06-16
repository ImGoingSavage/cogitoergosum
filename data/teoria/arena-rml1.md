# Confiabilidad de extremo a extremo: el ciclo de vida del ML y los SLOs

## De qué trata esta lección (y qué sabrás hacer al final)

Un sistema de ML no es un proyecto que se termina, sino un **loop** que nunca para —y su confiabilidad hereda la del software, con un giro propio: puede fallar **en silencio**—. Esta lección construye, desde cero, el ciclo de vida end-to-end y cómo definirle SLOs por capa, por qué un pipeline de ML es más frágil que un ETL, y cómo lanzar un modelo con el rigor de código (despacio, aislando la capa de datos, con rollback).

Al terminar podrás: (1) entender por qué el ML es un loop que empieza y termina en los datos; (2) definir SLOs en tres capas (señales doradas → salud del modelo → métrica de negocio por slices) y por qué la infraestructura nunca mide la calidad del ML; (3) aplicar "models as code", "release not refactor" y aislar el rollout en la capa de datos; y (4) sospechar del sistema antes que del modelo (la mayoría de fallos no son de ML). El ejemplo del recomendador con tres capas de SLO hace de hilo. Conecta con los SLOs de SRE ([[arena-sre1]]).

## El ML es un loop, no una línea recta

Un sistema de ML **nunca está terminado**. Si el modelo va mal, el equipo itera (cambia features, datos, estructura); si va bien, la organización se entusiasma y hace *el mismo trabajo* para mejorarlo más. El primer modelo es solo un punto de partida. El ciclo: recolección/análisis de datos → pipelines de entrenamiento → integrar y validar la aplicación → evaluación de calidad → definir y medir SLOs → lanzamiento → monitoreo y realimentación, y vuelta a empezar. Empieza y termina en los **datos**, y a menudo hay que revisitar etapas.

## Por qué un pipeline de ML es más frágil que un ETL

Tiene todos los modos de fallo de un pipeline de datos normal (falta de datos, formato incorrecto, bugs, mala configuración, escasez de recursos, fallos de hardware y de sistema distribuido) **más** los específicos de ML: puede **fallar en silencio** por cambios de distribución o datos faltantes. Omitir una fracción pequeña pero **no aleatoria** de datos lo lleva de "casi bien" a "muy mal" sin error visible.

## SLOs para ML

Un **SLI** es una medición; un **SLO** es un umbral sobre ese SLI (p.ej. "99.99% de requests con código 20x en <150 ms"). Para ML, sepáralos por **subsistema** (serving, training, aplicación) y por **capa**:

- **Señales doradas** (genéricas): latencia, tráfico, errores, saturación.
- **Salud básica del modelo**: ¿tamaño esperado?, ¿carga sin error? (sin entender su contenido).
- **Calidad del modelo** (dominio): lo más difícil — no hay "suficientemente bueno" objetivo, es multidimensional y depende del contexto. Aquí mandan las **métricas de negocio** (CTR, ingreso atribuible), medidas por slices.

> Ningún SLO de infraestructura mide la calidad ML; para eso hace falta un SLO de negocio.

## Lanzar bien: el modelo es código

- **Models as code:** un modelo nuevo puede tumbar el serving igual que un binario → mismo rigor, mismo rollback.
- **Launch slowly:** ramp-up progresivo limitando daño en dos ejes, **usuarios** y **servidores**.
- **Release, not refactor:** cambia lo mínimo; el ruido de fondo del ML vuelve indeducible un fallo si mezclas cambios.
- **Aísla el rollout en la capa de datos:** un formato nuevo escrito y leído por código viejo causa caídas (la historia del rollback de pagos que saltó al 100% de error al revertir).
- **Mide SLOs durante el lanzamiento** y revisa el rollout (humano o automático).

## La mayoría de fallos NO son fallos de ML

Cuando un sistema de ML cae, la causa suele ser un fallo clásico de sistemas/datos (permisos perdidos, versión equivocada copiada a serving, pipeline mal monitoreado), no el modelo. **Primero** haz fiable el sistema distribuido genérico; **después** ataca lo ML-específico.

---

## Mini-ejemplo trabajado: tres capas de SLO para un recomendador

Tu modelo de recomendación tiene **AUC 0.82** offline. ¿Está "sano" en producción? Define SLOs por capa:

1. **Señales doradas (infra):** "99.9% de las peticiones de scoring responden en <100 ms". Mide latencia/errores; **no dice nada** de si las recomendaciones son buenas.
2. **Salud básica del modelo:** "el artefacto cargó, pesa lo esperado, devuelve scores en [0,1] para una petición canaria". Detecta un modelo corrupto, **sin** entender su contenido.
3. **Calidad (negocio), por slices:** "el CTR de la sección recomendada ≥ 4% en usuarios nuevos y recurrentes". *Esta* es la única que mide si el ML sirve — y ningún SLO de infra la sustituye.

Las tres pueden estar verdes en 1 y 2 mientras el CTR (capa 3) se desploma porque un join quedó vacío: el modelo "funciona" (responde rápido, carga bien) pero recomienda basura.

**Predicción antes de seguir:** despliegas un modelo nuevo y el CTR cae. ¿Reentrenas el modelo? Probablemente **no**: la mayoría de los fallos no son de ML. Revisa primero permisos, la versión copiada a serving y la frescura de los datos.

## Prototipo, contraejemplo y caso borde

- **Prototipo (deploy como código):** ramp-up por usuarios×servidores, SLOs medidos durante el rollout, rollback listo → un modelo malo daña a pocos.
- **Contraejemplo ("refactor" en vez de "release"):** mezclar 5 cambios en un despliegue; el ruido de fondo del ML vuelve **indeducible** cuál rompió la métrica.
- **Caso borde (rollback que empeora):** revertir el binario pero no el **formato de datos** que ya escribió → código viejo leyendo datos nuevos = 100% de error (la historia del rollback de pagos).

## Errores típicos

- **Conceptual:** creer que un sistema de ML "se termina"; es un **loop** que la organización siempre quiere mejorar.
- **De medición:** usar solo SLOs de infraestructura y declarar el modelo sano sin un SLO de **negocio por slices**.
- **De diagnóstico:** asumir que la caída es del modelo y no del sistema distribuido genérico.

## Transferencia isomorfa

La fiabilidad de ML hereda la del software, con un giro:

- **Models as code ↔ CI/CD + rollback:** un modelo tumba el serving igual que un binario; merece el mismo rigor de release y reversión (conecta con [[arena-sre1]], releases y error budget).
- **SLO de negocio por slices ↔ guardrail metrics en A/B:** medir CTR/ingreso por segmento durante el rollout es el mismo papel que las métricas guardrail de un experimento (conecta con [[arena-ads4]]).
- **Fracción no aleatoria de datos faltantes ↔ sesgo de selección:** omitir un trozo *sesgado* de datos lleva de "casi bien" a "muy mal" — el mismo peligro que el sesgo de selección causal (conecta con [[arena-h19]]).

Moraleja de la arista: *la infraestructura nunca mide la calidad del ML; necesitas un SLO de negocio por slices, despliega el modelo como código y sospecha del sistema antes que del modelo.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Mi modelo tiene buena accuracy pero el SLO no lo refleja" | Añade un SLO de métrica de NEGOCIO, por slices |
| "Voy a desplegar un modelo nuevo" | Trátalo como código: ramp-up usuarios×servidores + rollback |
| "Al hacer rollback los errores empeoraron" | Aísla el rollout también en la capa de datos |
| "El sistema de ML cayó, debe ser el modelo" | Probablemente NO: revisa sistemas/datos primero |
| "Quiero validar la integración sin arriesgar usuarios" | Dark launch (consulta y registra, no sirve) |

---

> **Síntesis:** Un sistema de ML es un **loop** de producción que nunca termina. Defínele SLOs **por subsistema y por capa** (señales doradas → salud del modelo → métrica de negocio), porque la infraestructura no mide la calidad ML. Despliega el modelo **como código**: despacio, aislando la capa de datos y con rollback obligatorio. Y recuerda que **la mayoría de los fallos no son fallos de ML** — haz fiable el sistema genérico antes que lo específico.

---

*Retrieval: cierra y responde: (1) ¿por qué el ML es un loop?; (2) ¿qué tres capas de SLO hay y por qué la infraestructura no mide calidad?; (3) ¿qué significa "release, not refactor" y "aislar en la capa de datos"?; (4) ¿por qué priorizar fallos no-ML?*
