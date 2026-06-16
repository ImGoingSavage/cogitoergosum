# SLOs, alertas basadas en SLO y burn alerts

## De qué trata esta lección (y qué sabrás hacer al final)

Las alertas que avisan de *causas potenciales* (CPU alta, hilos anómalos) producen un mar de falsos positivos que desensibiliza al equipo —la **fatiga de alertas**, la misma normalización de la desviación del desastre del Challenger—. Esta lección construye, desde cero, la alternativa: alertar por el **síntoma de dolor del usuario** vía **SLOs**, gobernar releases con el **error budget**, y avisar *antes* de agotarlo con **burn alerts predictivas**.

Al terminar podrás: (1) entender por qué el umbral estático solo cubre known-unknowns y por qué una buena alerta debe ser indicador fiable de impacto al usuario y accionable; (2) definir SLI/SLO y por qué preferir SLI basados en eventos; (3) usar el error budget ($1-\text{SLO}$) para arbitrar releases; y (4) construir una burn alert predictiva (ventana deslizante de 30 días, lookahead + baseline del mismo orden). El caso del brownout por fuga de memoria hace de hilo. Comparte el error budget con [[arena-sre1]].

## El problema: fatiga de alertas

Las alertas tradicionales de **causa potencial** (CPU alta, nº anómalo de hilos) producen muchos **falsos positivos**: la condición puede deberse a mil factores, no al que importa. El equipo se desensibiliza → **fatiga de alertas** (*normalización de la desviación*, término del desastre del Challenger). Una buena alerta (según el libro SRE de Google) debe ser **fiable indicador de impacto al usuario** y **accionable**; si no cumple ambas, debe **borrarse**.

**El umbral estático es solo para *known-unknowns*.** En sistemas distribuidos el fallo es inevitable y el rendimiento varía durante el día; los umbrales fijos no captan la degradación emergente y **desacoplar el «qué» del «por qué»** es la clave de una alerta con señal máxima. Las fallas auto-remediadas (autoscaling, failover) **no deberían despertar a nadie** de madrugada.

## SLI, SLO y el North Star del usuario

- La **experiencia del usuario es el North Star**: alertar por **síntoma de dolor del usuario**, no por causa potencial.
- **SLO** (objetivo de nivel de servicio): meta interna acordada de salud, basada en **journeys críticos del usuario**, normalmente más estricta que el SLA externo.
- **SLI** (indicador): mide el estado como bueno/malo. Dos tipos: **basado en tiempo** (p.ej. «p99 < 300 ms cada ventana de 5 min») y **basado en eventos** (p.ej. «proporción de eventos < 300 ms en la ventana móvil»). **Preferir SLI basado en eventos**: más granular y fiable (las métricas por tiempo crean falsos positivos y negativos).
- Ejemplo de SLI por evento: «evento con path `/home`, duration < 100 ms y éxito = OK; > 100 ms = error aunque devuelva 200».

## Error budget y burn alerts

**error budget = 1 − SLO** = máxima indisponibilidad que el negocio tolera. Cada evento «malo» (*burned*) lo consume; agotarlo = fuera de SLO → se frenan releases y se invierte en estabilidad. Hay que actuar **antes** de agotarlo: las **burn alerts** avisan de violaciones futuras si el ritmo de quema continúa. (Caso real Honeycomb 2019: una SLO burn alert detectó un brownout/OOM por fuga de memoria que el monitoreo tradicional **nunca** habría visto.)

### Ventana deslizante, no fija
Calcula el SLO sobre una **ventana deslizante** (p.ej. trailing 30 días), no fija de calendario: las emociones del cliente no se «resetean» el día 1 del mes. 30 días es lo más pragmático (7-14 días no alinea con la memoria del cliente; 90 es demasiado).

### Dos modelos de burn alert preventiva
1. **Umbral no-cero** (p.ej. alertar cuando queda < 30% del budget): simple pero «mueve el poste» y deja al equipo en feature-freeze hasta recuperar.
2. **Predictiva (forecast)**: extrapola si el ritmo actual agotará el budget. Requiere:
   - **Lookahead window**: cuán lejos al futuro proyectas (días → no urge; horas → paginar).
   - **Baseline/lookback window**: cuántos datos recientes usas para predecir; debe ser del **mismo orden de magnitud** que el lookahead (un baseline puede predecir hasta ~4× hacia adelante sin compensar estacionalidad).
   - **Short-term (ahistórico)**: solo usa el baseline reciente; barato. **Context-aware**: usa todos los eventos buenos/malos de la ventana completa del SLO; más caro pero más sensato cuando importa cuánto budget queda (un error con 10% restante urge más que con 90%).

Las burn alerts predictivas funcionan mejor para SLOs ≤ 99.95%.

---

## Mini-ejemplo trabajado: burn alert antes de quedarte sin budget

SLO = **99.9%** sobre ventana deslizante de 30 días. El error budget es 0.1% del tráfico. A las 02:00 un brownout por fuga de memoria empieza a quemar budget **10× más rápido** de lo normal.

- Una alerta de **umbral no-cero** ("avisa con < 30% de budget") saltaría… cuando ya quemaste el 70%: tarde, y te deja en feature-freeze.
- Una **burn alert predictiva** extrapola el ritmo actual: "a esta velocidad, el budget de 30 días se agota en **6 horas**". Con un *lookahead* de 6 h y un *baseline* del mismo orden, te pagina **ahora**, mientras hay margen para revertir.

Esto es exactamente lo que el monitoreo tradicional de umbral de CPU **nunca** habría visto (caso real Honeycomb 2019): la CPU se veía normal, pero la *experiencia del usuario* (el síntoma) se degradaba.

**Predicción antes de seguir:** ¿por qué medir el SLO sobre ventana **deslizante** de 30 días y no por mes calendario? Porque las emociones del cliente no se "resetean" el día 1; un incidente el 31 importa igual que el 1.

## Prototipo, contraejemplo y caso borde

- **Prototipo (alerta sana):** SLI por eventos sobre un journey crítico → alerta por **síntoma de dolor del usuario**, accionable.
- **Contraejemplo (alerta de causa):** "CPU > 80%" → mil causas posibles, casi siempre falso positivo → fatiga de alertas (normalización de la desviación, Challenger).
- **Caso borde (auto-remediado):** un failover/autoscaling que se resolvió solo **no** debe despertar a nadie de madrugada.

## Errores típicos

- **Conceptual:** alertar por **causa potencial** en vez de por **síntoma**; el "qué" (dolor del usuario) debe desacoplarse del "por qué".
- **De medición:** SLI **por tiempo** ("p99 < 300 ms cada 5 min") en vez de **por eventos** (proporción de eventos buenos) → falsos positivos/negativos.
- **De ventana:** baseline de la burn alert demasiado corto vs el lookahead → predicción inestable (deben ser del mismo orden).

## Transferencia isomorfa

- **Error budget = 1 − SLO ↔ presupuesto de riesgo:** es el mismo arbitraje velocidad/estabilidad del SRE clásico (conecta con [[arena-sre1]]).
- **Burn alert predictiva ↔ forecasting / detección temprana:** extrapolar el ritmo para actuar antes del agotamiento es un pronóstico con lookahead, como prever drift antes de que pegue (conecta con [[arena-dmls4]]).
- **Normalización de la desviación ↔ fatiga de alertas tóxica:** desensibilizarse ante señales repetidas es un fallo socio-técnico, no técnico (conecta con [[arena-sre3]], postmortems sin culpa).

Moraleja de la arista: *alerta por el síntoma del usuario vía SLO, gobierna releases con el error budget, y avisa antes de agotarlo con una burn alert predictiva sobre ventana deslizante.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Alertas que nadie atiende ya | Fatiga/normalización de desviación: borra lo no-accionable; alerta por síntoma |
| Umbral estático de CPU para «salud» | Solo cubre known-unknowns; usa SLO por síntoma de dolor del usuario |
| ¿SLI por tiempo o por eventos? | Por eventos: más granular, menos falsos positivos/negativos |
| «¿Cuándo freno releases?» | Cuando se agota el error budget (= 1 − SLO) |
| Quiero avisar antes de agotar el budget | Burn alert predictiva: lookahead + baseline (~mismo orden), short-term vs context-aware |
| SLO calculado por mes calendario | Usa ventana **deslizante** de 30 días: el cliente no se resetea el día 1 |

---

> **Síntesis:** las alertas de causa potencial generan **fatiga**; el umbral estático solo cubre **known-unknowns**. Alerta por **síntoma de dolor del usuario** vía **SLOs** medidos con **SLI basados en eventos**. El **error budget = 1 − SLO** gobierna los releases; las **burn alerts predictivas** (ventana deslizante de 30 días, lookahead + baseline del mismo orden, short-term vs context-aware) avisan antes de agotarlo.

---

*Retrieval: (1) ¿qué es la fatiga de alertas y por qué el umbral estático solo da known-unknowns?; (2) define SLI/SLO y por qué preferir SLI por eventos; (3) ¿qué es el error budget y cómo se relaciona con los releases?; (4) explica ventana deslizante vs fija y lookahead/baseline en una burn alert predictiva.*
