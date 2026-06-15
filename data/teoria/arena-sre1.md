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

## Mini-ejemplo trabajado: gastar el error budget

Servicio con **SLO = 99.9%** de éxito y **2.5 M peticiones/día**. El error budget es `1 − 0.999 = 0.001`:

`presupuesto = 0.001 × 2.5M = 2 500 errores/día` permitidos antes de incumplir.

Un martes, un despliegue defectuoso quema **2 000** errores en una hora. Te quedan 500 para el resto del día y del periodo. La regla SRE: **mientras quede budget, Dev empuja releases; si se agota, se congelan** y el equipo invierte en fiabilidad. No es una discusión de opiniones (Dev quiere velocidad, SRE estabilidad): es una **métrica objetiva** que autorregula al equipo de producto.

**Predicción antes de seguir:** tu jefe pide subir de 99.9% a 99.999% "para estar seguros". ¿Buena idea? Casi nunca: el usuario no distingue ese salto (su experiencia la domina su red/dispositivo), cada nueve cuesta ~10× y frena features. Peor: un servicio *demasiado* fiable crea **dependencias ocultas** (caso Chubby: nadie manejaba su caída).

## Prototipo, contraejemplo y caso borde

- **Prototipo:** SLO sobre tasa de éxito de peticiones + error budget que arbitra releases + p99 monitoreado → fiabilidad gestionada como riesgo.
- **Contraejemplo ("SLA" que no lo es):** "tenemos un SLA de 99.9%" sin ninguna consecuencia por incumplir → es un **SLO**; el test es "¿qué pasa si no se cumple?".
- **Caso borde (latencia media engañosa):** la media de latencia se ve bien pero hay quejas → el **p99** revela la cola que la media esconde.

## Errores típicos

- **Conceptual:** perseguir 100% de uptime como objetivo (es a la vez mínimo *y* máximo; excederlo desperdicia oportunidad y crea dependencias ocultas).
- **De vocabulario:** llamar SLA a un SLO (un SLA conlleva multa/reembolso).
- **De medición:** reportar la **media** en vez de **percentiles** → la cola (la experiencia peor) queda invisible.

## Transferencia isomorfa

El error budget es gestión de riesgo cuantificada, un patrón portable:

- **Error budget ↔ presupuesto de experimentación / de cambios:** "te quedan N errores antes de congelar" es como un presupuesto de riesgo que regula cuántos cambios arriesgados puedes lanzar — el mismo espíritu que limitar el daño de un rollout (conecta con [[arena-rml1]], models as code).
- **p99 sobre la media ↔ pensar en la cola, no en el promedio:** ignorar la cola es el mismo error que confiar en la esperanza sin mirar la varianza/los extremos (conecta con [[arena-q1]]).
- **SLO como contrato objetivo ↔ métrica que zanja una tensión:** convertir "Dev vs SRE" en un número es lo que hace una métrica alineada al costo real en cualquier organización.

Moraleja de la arista: *la fiabilidad es riesgo, no maximización; el error budget = 1−SLO convierte una pelea en una métrica, y la cola (p99) cuenta la verdad que la media oculta.*

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
