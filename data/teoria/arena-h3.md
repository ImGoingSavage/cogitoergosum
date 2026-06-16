# Inferencia causal I: contrafactuales, experimentos e identificación

## De qué trata esta lección (y qué sabrás hacer al final)

Esta lección construye, desde cero, el otro gran lenguaje de la causalidad (el de Neyman-Rubin, complementario al grafo de Pearl): los **resultados potenciales**. La idea raíz es a la vez simple y demoledora: cada individuo tiene dos destinos —con tratamiento y sin él— pero solo observamos uno, así que la inferencia causal es, en el fondo, un problema de **datos faltantes**. De ahí salen las tres condiciones que cualquier estimación causal debe cumplir antes de tocar los datos.

Al terminar podrás: (1) distinguir asociación ($E[Y\mid A]$) de causación ($E[Y^a]$) y saber cuándo coinciden; (2) explicar por qué la aleatorización da intercambiabilidad; (3) verificar las tres condiciones de identificación (intercambiabilidad, positividad, consistencia); y (4) estimar un efecto por estandarización. Cada idea entra por un ejemplo numérico. Conecta con el lenguaje gráfico de [[arena-h15]].

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

## Mini-ejemplo trabajado: estandarizar a mano (y cuándo se rompe)

Un confundidor binario L (estado de salud base). Riesgo de muerte observado, por estrato:

| L | P(L) | P(Y=1\|A=1,L) | P(Y=1\|A=0,L) |
|---|---|---|---|
| sano (L=0) | 0.5 | 0.10 | 0.08 |
| frágil (L=1) | 0.5 | 0.40 | 0.30 |

**Estandarización:** E[Y^{a=1}] = Σ_l P(Y=1|a=1,l)P(l) = 0.10·0.5 + 0.40·0.5 = **0.25**; E[Y^{a=0}] = 0.08·0.5 + 0.30·0.5 = **0.19**. Diferencia de riesgos causal = **+0.06**. Fíjate que *promediamos los estratos con el peso de la población* P(l), no con el de los tratados — eso es lo que vuelve causal al número (la misma idea que IP weighting, visto desde el outcome).

**Predicción antes de seguir:** ¿qué pasa si en el estrato "frágil" *nadie* recibió A=0 (todos los frágiles se trataron)? Entonces P(Y=1|A=0,L=1) no existe en los datos → **violación de positividad**: la fórmula pide una casilla vacía y el efecto es inidentificable ahí, no cero.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** ECA. La aleatorización da intercambiabilidad marginal → E[Y|A=a]=E[Y^a] sin ajustar.
- **Contraejemplo (consistencia mal definida):** "¿efecto de la obesidad sobre la mortalidad?" El "tratamiento" no es una intervención bien definida (¿dieta? ¿cirugía? ¿genética?) → distintos Y^a, contraste ambiguo. Falla la consistencia antes que ninguna otra cosa.
- **Caso borde (positividad determinista):** un estrato donde el protocolo *obliga* a tratar (P(A=1|L)=1) rompe positividad; ningún método lo arregla, solo cambiar la pregunta o el diseño.

## Errores típicos

- **Conceptual:** confundir E[Y|A=1] (subpoblación observada) con E[Y^{a=1}] (toda la población intervenida) — son iguales **solo** bajo intercambiabilidad.
- **De supuestos:** verificar solo intercambiabilidad y olvidar positividad y consistencia (las tres son necesarias).
- **De interpretación:** reportar una razón de riesgos como si la "modificación de efecto" fuera la misma en escala aditiva y multiplicativa.

## Transferencia isomorfa

Las tres condiciones tienen gemelos exactos en ML/experimentación:

- **Consistencia ↔ "tratamiento bien definido" en producto:** medir "el efecto de mostrar el banner" exige que *mostrar el banner* signifique una sola cosa; si hay 5 variantes mezcladas, el estimando es ambiguo igual que "el efecto de la obesidad".
- **Positividad ↔ overlap / soporte común:** un segmento al que la política *siempre* asigna A no permite estimar su contrafactual — el mismo requisito que en covariate shift y en evaluación off-policy (conecta con [[arena-h20]]).
- **Estandarización ↔ métrica ponderada por segmento:** promediar una métrica de A/B por la *composición poblacional* (no por la del brazo) es exactamente la g-fórmula aplicada a un experimento.

Moraleja de la arista: *identificar es preguntar "¿tengo intercambiabilidad, positividad y consistencia?"; estimar viene después — sin las tres, más datos no compran causalidad.*

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
