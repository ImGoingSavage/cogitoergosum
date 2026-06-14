# Confiabilidad de extremo a extremo: el ciclo de vida del ML y los SLOs

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
