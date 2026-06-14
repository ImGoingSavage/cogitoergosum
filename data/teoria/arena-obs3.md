# SLOs, alertas basadas en SLO y burn alerts

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
