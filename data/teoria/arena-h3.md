# Inferencia causal I: contrafactuales, experimentos e identificación

## El efecto causal como contraste contrafactual

Cada individuo tiene **resultados potenciales**: Y^{a=1} (bajo tratamiento) y Y^{a=0} (sin él). Hay **efecto causal individual** si Y^{a=1}≠Y^{a=0}, pero solo observamos UNO (el del tratamiento recibido): **problema fundamental** de la inferencia causal → es un problema de **datos faltantes**.

Lo identificable es el **efecto causal promedio**: E[Y^{a=1}] ≠ E[Y^{a=0}] (el outcome medio si TODA la población se tratara vs si NADIE lo hiciera).

**Asociación ≠ causación:**
- Asociación: E[Y|A=1] vs E[Y|A=0] — dos **subpoblaciones** distintas observadas.
- Causación: E[Y^{a=1}] vs E[Y^{a=0}] — la **misma** población bajo dos intervenciones.

Coinciden solo si los grupos son **intercambiables**.

## Aleatorización e intercambiabilidad

La aleatorización asigna A por azar, independiente de los resultados potenciales → **intercambiabilidad** (Y^a ⊥ A): los grupos son comparables y E[Y|A=a]=E[Y^a]. Por eso el ECA es el patrón oro. En observacional solo se aspira a intercambiabilidad **condicional** (Y^a ⊥ A | L), con el riesgo de **confundimiento no medido**.

## Las 3 condiciones de identificación

1. **Intercambiabilidad** (condicional): Y^a ⊥ A | L — no hay confundimiento no medido. *(supuesto)*
2. **Positividad:** 0 < P(A=a|L=l) < 1 en todo estrato presente. *(parcialmente verificable)*
3. **Consistencia:** intervención bien definida y, si A=a, Y^a=Y. *(supuesto)*

Con las tres, el efecto se identifica y se estima por **estandarización** (E[Y^a]=Σ_l E[Y|a,l]P(l), modela el outcome) o **IP weighting** (pondera 1/P(A|L), modela el tratamiento). Ver [[condiciones-identificacion-causal]].

## Medidas de efecto, modificación e interacción

- **Diferencia de riesgos** P(Y^{a=1}=1)−P(Y^{a=0}=1) (aditiva), **razón de riesgos** (multiplicativa), **odds ratio**. Todas **marginales**.
- **Modificación de efecto:** el efecto de A varía por estratos de un marcador V; depende de la **escala** (puede haber aditiva sin multiplicativa).
- **Interacción:** efecto **conjunto** de DOS tratamientos A y E (se interviene a ambos; causas suficientes). Ver [[modificacion-efecto-vs-interaccion]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Pregunta causal vaga | Define el contraste contrafactual Y^{a=1} vs Y^{a=0} |
| ¿Asociación = efecto? | Solo si hay intercambiabilidad (aleatorización o ajuste por L) |
| Datos observacionales | Chequea intercambiabilidad|L + positividad + consistencia |
| Reportar por subgrupos | Modificación de efecto: especifica la escala |
| Estrato sin tratados/controles | Violación de positividad |

---

> **Síntesis:** el efecto causal es un contraste **contrafactual** poblacional (E[Y^{a=1}]−E[Y^{a=0}]), distinto de la **asociación**. La **aleatorización** da intercambiabilidad; en observacional se necesitan **intercambiabilidad|L + positividad + consistencia** para identificar, y luego **estandarización** o **IP weighting** para estimar. Distingue **modificación de efecto** (un tratamiento, varía por V) de **interacción** (dos tratamientos).

---

*Retrieval: (1) ¿efecto promedio vs asociación?; (2) las 3 condiciones de identificación; (3) ¿qué da la aleatorización?; (4) ¿modificación vs interacción?*
