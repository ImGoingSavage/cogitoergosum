# Fundamentos SRE: riesgo, error budgets y SLOs

SRE (Site Reliability Engineering) es lo que sale cuando un ingeniero de software diseña operaciones. Su idea central: **gestionar la fiabilidad como riesgo**, no maximizar el uptime.

## 100% es el objetivo equivocado

Pasado cierto punto, **más fiabilidad es peor**: el usuario no distingue 99.99% de 99.999% (su experiencia la domina la red/dispositivo), cada **nueve** extra cuesta ~10x más y frena features. El coste tiene dos caras: recursos redundantes y **coste de oportunidad** (ingenieros que no hacen features). Se trata el objetivo de disponibilidad como **mínimo Y máximo**: excederlo desperdicia oportunidades y crea **dependencias ocultas** (caso Chubby: tan fiable que nadie manejaba su caída → se provocan caídas controladas).

**Medición:** en vez de uptime/(uptime+downtime), Google usa **tasa de éxito de peticiones** (peticiones con éxito / totales) sobre ventana móvil, porque los servicios están distribuidos globalmente y esto aplica también a batch/pipeline. Ej.: 2.5M req/día a 99.99% permite 250 errores.

## Error budget

**error budget = 1 − SLO.** Producto define el SLO, el monitoreo (tercero neutral) mide el uptime real, y la diferencia es el presupuesto de "no-fiabilidad" restante. Mientras quede budget, **se pueden empujar releases**; si se agota, se **frenan** y se invierte en fiabilidad. Convierte la tensión Dev (velocidad) ↔ SRE (estabilidad) en una **métrica objetiva**: el equipo de producto se autorregula. *"Hope is not a strategy."*

## SLI, SLO, SLA

- **SLI** (indicator): medida cuantitativa de un aspecto del servicio — latencia, tasa de error, **disponibilidad** (fracción de peticiones bien formadas con éxito = *yield*), throughput, durabilidad.
- **SLO** (objective): objetivo/umbral sobre un SLI (`SLI ≤ objetivo`), p.ej. "latencia media < 100 ms".
- **SLA** (agreement): **contrato con consecuencias** (multa/reembolso) por (in)cumplir los SLOs.

**Test rápido:** "¿qué pasa si no se cumple?" — sin consecuencia explícita, es un **SLO**, no un SLA. (La gente dice "SLA" cuando quiere decir "SLO".) Elige **pocos** SLIs (un puñado) y mídelos como **distribución/percentiles** (p99), no como media — la media oculta la cola.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Hagámoslo 100% fiable" | No: el usuario no lo nota y cuesta ~10x por nueve |
| "Dev quiere velocidad, SRE estabilidad" | Error budget = 1−SLO arbitra los lanzamientos |
| "Tenemos un SLA de 99.9%" (¿seguro?) | ¿Hay consecuencia? Si no, es un SLO |
| "Nuestra latencia media es buena" | Mira el p99: la media oculta la cola |
| Servicio tan fiable que crea dependencias | Caída controlada para flushear dependencias (Chubby) |

---

> **Síntesis:** SRE gestiona la fiabilidad como **riesgo**: **100% nunca es el objetivo** (el usuario no lo nota y cada nueve cuesta ~10x). El **error budget = 1 − SLO** arbitra de forma objetiva la velocidad de lanzamiento entre Dev y SRE. Distingue **SLI** (mides), **SLO** (objetivo) y **SLA** (contrato con consecuencias), con pocos indicadores medidos por **percentiles**.

---

*Retrieval: (1) ¿por qué 100% es el objetivo equivocado?; (2) ¿cómo se calcula y para qué sirve el error budget?; (3) distingue SLI/SLO/SLA y el test del SLA; (4) ¿por qué medir percentiles y no la media?*
