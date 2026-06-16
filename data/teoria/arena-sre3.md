# Troubleshooting, gestión de incidentes y postmortems sin culpa

## De qué trata esta lección (y qué sabrás hacer al final)

Cuando algo se rompe en producción, la diferencia entre resolverlo en minutos o en horas no es talento, es **método**. Esta lección construye, desde cero, tres disciplinas del SRE: depurar como científico (método hipotético-deductivo), coordinar un incidente sin que se descontrole (el Incident Command System) y aprender de él sin buscar culpables (postmortems blameless).

Al terminar podrás: (1) convertir "el sistema está lento" en un reporte accionable y probar hipótesis con cambios controlados (caballos, no cebras; correlación ≠ causa); (2) reconocer los tres fallos de un incidente mal gestionado y los roles del ICS (solo Ops modifica el sistema); y (3) entender por qué un postmortem **sin culpa** ataca causas sistémicas —porque la cultura de culpa hace que los problemas se oculten—. Conecta con la filosofía de que el error enseña, no castiga.

## Troubleshooting hipotético-deductivo

Depurar es aplicar el **método hipotético-deductivo**: ante un **reporte** (esperado vs real + cómo reproducir), mira telemetría/logs, plantea **hipótesis** de causa y pruébalas —comparando el estado observado contra la teoría, o **cambiando el sistema de forma controlada** y observando—, iterando hasta la **causa raíz**, luego corrige y escribe un postmortem. Abre un **bug** por cada incidencia (registro buscable).

**Trampas:** síntomas irrelevantes, teorías improbables, aferrarse a causas pasadas, correlaciones espurias. *"Cuando oigas cascos, piensa en caballos, no en cebras"*, prefiere lo simple (Occam) — pero recuerda que **correlación no es causa** (eventos correlacionados pueden compartir una causa común) y que a veces varios fallos comunes explican mejor que uno raro (Hickam).

## Gestión de incidentes (Incident Command System)

La **historia de Mary** (incidente no gestionado) muestra tres fallos: **foco excesivo en lo técnico**, **mala comunicación** y **freelancing** (cambios sin coordinar que empeoran). Todos hacían "su trabajo" y aun así se descontroló.

Google usa el **Incident Command System (ICS)**. La **separación clara de responsabilidades** da, contraintuitivamente, **más autonomía** (nadie cuestiona el trabajo del otro). Roles:

- **Incident Command:** mantiene el estado de alto nivel, estructura el equipo y asigna; ocupa de facto los roles no delegados.
- **Operational Work (Ops):** aplica las herramientas; **único grupo que modifica el sistema** durante el incidente.
- **Communication:** cara pública, emite actualizaciones periódicas y mantiene el documento.
- **Planning lead:** rastrea lo de más largo plazo y la dotación.

## Postmortems sin culpa (blameless)

Un **postmortem** registra impacto, acciones, **causa(s) raíz** y acciones de seguimiento para evitar la recurrencia. **Disparadores definidos de antemano:** downtime visible, pérdida de datos, intervención de on-call, resolución sobre umbral, fallo de monitoreo (cualquier stakeholder puede pedir uno).

**Sin culpa:** se enfoca en las causas **sistémicas** asumiendo que todos actuaron con buena intención e información incompleta, **sin señalar personas**. La cultura de culpa hace que la gente **oculte** problemas → más riesgo. No puedes "arreglar" personas, pero sí **sistemas y procesos** (origen en sanidad/aviación). Escribirlo **no es castigo**, es aprendizaje; no estigmatices a quien produce muchos. Proceso colaborativo (tiempo real, comentarios, revisión senior) y se comparte ampliamente.

---

## Mini-ejemplo trabajado: depurar como científico

"El servicio está lento." Eso no es un reporte accionable. Conviértelo en el método hipotético-deductivo:

1. **Reporte:** esperado = p99 < 200 ms; real = p99 = 3 s; repro = cualquier request a `/buscar` desde las 14:00.
2. **Hipótesis 1:** "la BD está saturada". **Test:** mira la latencia de la BD → normal. **Descartada.**
3. **Hipótesis 2:** "un deploy a las 14:00 cambió algo". **Test:** revisa el changelog → sí hubo deploy. **Cambio controlado:** rollback en un canario → la latencia vuelve a 200 ms. **Confirmada.**

Cada paso *compara el estado observado contra una teoría* o *cambia el sistema de forma controlada y observa*. La trampa a evitar: aferrarse a la causa del último incidente o perseguir una correlación espuria. "Cuando oigas cascos, piensa en **caballos, no cebras**" (Occam), pero recuerda que correlación ≠ causa.

**Predicción antes de seguir:** durante el incidente, tres ingenieros aplican fixes a la vez sin avisarse y la cosa empeora. ¿Qué falló y cómo lo evita el ICS? Es **freelancing**; el ICS lo previene haciendo que **solo Ops** modifique el sistema, coordinado por el Incident Command.

## Prototipo, contraejemplo y caso borde

- **Prototipo (incidente bien gestionado):** roles ICS separados (command/ops/comms/planning), un canal de comunicación, postmortem sin culpa al cierre.
- **Contraejemplo (la historia de Mary):** todos "haciendo su trabajo" pero con foco solo técnico, mala comunicación y freelancing → el incidente se descontrola.
- **Caso borde (síntoma raro real):** a veces *varios* fallos comunes explican mejor que uno raro (Hickam) — Occam guía, no dogmatiza.

## Errores típicos

- **Conceptual:** preguntar "¿de quién fue la culpa?" — pregunta equivocada; arreglas sistemas, no personas.
- **De diagnóstico:** confundir correlación con causa, o aferrarse a la causa del incidente anterior.
- **De coordinación:** modificar el sistema sin rol claro (freelancing) durante un incidente.

## Transferencia isomorfa

- **Método hipotético-deductivo ↔ inferencia causal y debugging de modelos:** plantear hipótesis y testearlas con cambios controlados es el RCT del ingeniero (conecta con [[arena-h15]], hacer vs observar).
- **Postmortem sin culpa ↔ normalizar el error como parte del proceso:** atacar el sistema y no a la persona es la misma filosofía de que el error enseña, no castiga — alineado con la Constitución de la app.
- **"Caballos, no cebras" ↔ tasa base / Occam:** preferir la explicación común es razonar con la prior correcta (conecta con [[arena-q2]], Bayes y tasa base).

Moraleja de la arista: *depura con hipótesis y cambios controlados, coordina con roles claros (solo Ops toca el sistema), y cierra atacando el sistema, no a la persona.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "El sistema está lento" | Reporte (esperado/real/repro) → hipótesis → testear → causa raíz |
| Síntoma raro | Caballos, no cebras; correlación ≠ causa |
| Incidente que se descontrola | Aplica ICS: roles claros, solo Ops modifica |
| Cambios descoordinados (freelancing) | El comandante coordina; comunica el estado |
| Tras un incidente significativo | Postmortem **sin culpa**: causas sistémicas |
| "¿De quién fue la culpa?" | Pregunta equivocada: arregla sistemas, no personas |

---

> **Síntesis:** Depura con el **método hipotético-deductivo** (hipótesis → testear → causa raíz; caballos, no cebras). Gestiona incidentes con el **ICS**: roles separados (command, ops, comms, planning), con **solo Ops** modificando el sistema, para evitar el freelancing que descontrola. Y cierra con un **postmortem sin culpa** que ataca causas sistémicas —no personas— porque la culpa hace que los problemas se oculten.

---

*Retrieval: (1) ¿cómo se prueban hipótesis en troubleshooting?; (2) los tres fallos del incidente no gestionado; (3) nombra los roles del ICS; (4) ¿qué es y por qué importa un postmortem sin culpa?*
