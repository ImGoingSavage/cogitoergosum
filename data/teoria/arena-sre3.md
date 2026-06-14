# Troubleshooting, gestión de incidentes y postmortems sin culpa

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
