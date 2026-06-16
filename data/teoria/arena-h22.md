# The Mixtape IV: panel/efectos fijos, DiD y control sintético

## De qué trata esta lección (y qué sabrás hacer al final)

Cuando observas las mismas unidades a lo largo del tiempo, el tiempo mismo se vuelve tu aliado contra el confundimiento. Esta lección construye, desde cero, los diseños que lo explotan: los **efectos fijos** (que barren todo lo estable no observado de cada unidad), las **diferencias en diferencias** (que restan la tendencia común) y el **control sintético** (que fabrica un "gemelo" cuando solo hay una unidad tratada). El hilo: cada uno cambia el CIA por un supuesto sobre *trayectorias* más fácil de defender.

Al terminar podrás: (1) saber qué controlan los efectos fijos y qué no (lo que varía en el tiempo se les escapa); (2) calcular un DiD 2×2 y entender que su supuesto es **tendencias paralelas**, no niveles iguales; (3) apoyar ese supuesto con event studies y placebos, y evitar el TWFE ingenuo con adopción escalonada; y (4) construir un control sintético con inferencia por permutación. El DiD entra por un ejemplo numérico. Cierra el toolkit cuasi-experimental ([[arena-h21]]).

## Datos de panel y efectos fijos

Con **panel** (mismas unidades en varios periodos), los **efectos fijos de unidad** controlan TODO lo **invariante en el tiempo**, observado o **no** (cultura, habilidad, geografía): el estimador **within** usa solo la variación dentro de cada unidad. Se añaden **FE de tiempo** para shocks comunes.

**Límites:** NO resuelven confundidores que **varían en el tiempo** ni la causalidad inversa; **absorben** (no estiman) covariables constantes; exigen **exogeneidad estricta** (error no correlacionado con el tratamiento en ningún periodo). Ver [[efectos-fijos-panel]].

## Diferencias en diferencias (DiD)

$$\text{ATT} = (\bar Y_{trat,post}-\bar Y_{trat,pre}) - (\bar Y_{ctrl,post}-\bar Y_{ctrl,pre})$$

La 1ª diferencia (post−pre) quita lo **fijo** de cada grupo; la 2ª (tratado−control) quita la **tendencia común**. Es un FE de dos vías (grupo + tiempo) con interacción tratado×post. Identifica el ATT bajo **TENDENCIAS PARALELAS** (sin tratamiento, ambos grupos habrían evolucionado igual — trayectorias, no niveles). Ver [[diferencias-en-diferencias]].

**Apoyo del supuesto:** **event study** / pre-tendencias ≈0 y **pruebas placebo**. **Riesgo moderno:** con adopción **escalonada** (staggered) + efectos heterogéneos, el **TWFE** ingenuo usa ya-tratados como controles → sesgo (**Goodman-Bacon**); usar estimadores robustos (Callaway-Sant'Anna, etc.). Ver [[tendencias-paralelas-placebo]]. Ejemplo: **Card-Krueger** (salario mínimo NJ vs PA).

## Control sintético

Para **una** unidad tratada agregada: el contrafactual es una **combinación ponderada** de un *donor pool* de controles, con pesos (≥0, suman 1) que **reproducen la trayectoria pre-tratamiento**. El efecto es la **brecha** post-tratamiento entre la unidad y su **gemelo sintético**. No extrapola, pesos explícitos; **inferencia por placebo/permutación** (aplicar a cada control). Ejemplo: **California sintética** (Prop. 99, tabaco, Abadie et al.). Ver [[control-sintetico]].

---

## Mini-ejemplo trabajado: DiD 2×2 con números

Empleo medio (en miles) antes y después de subir el salario mínimo, tratado (NJ) vs control (PA):

| | Pre | Post | Δ (post−pre) |
|---|---|---|---|
| **Tratado (NJ)** | 20 | 21 | +1 |
| **Control (PA)** | 22 | 25 | +3 |

La 1ª diferencia quita el nivel fijo de cada estado; la 2ª quita la tendencia común. **ATT = (+1) − (+3) = −2**: sin la política, NJ "debería" haber subido +3 como PA; subió solo +1 → el salario mínimo costó 2 mil empleos *relativos a la tendencia*. Nota que el empleo de NJ **subió** en términos absolutos (+1): mirar solo "antes/después del tratado" (+1) daría el signo equivocado. La tendencia paralela (PA) es la que revela el efecto.

**Predicción antes de seguir:** si PA hubiera estado plano (Δ=0), ¿cuál sería el ATT? +1 − 0 = +1. El control *es* el contrafactual; cambia el control y cambia la conclusión — por eso el supuesto de tendencias paralelas es todo.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** dos grupos, un shock que cae sobre uno, tendencias pre paralelas → DiD limpio.
- **Contraejemplo (TWFE escalonado):** con adopción en distintos momentos y efectos heterogéneos, el TWFE ingenuo usa a los *ya tratados* como controles → sesgo de Goodman-Bacon. Parece DiD, pero el "control" ya está contaminado.
- **Caso borde (una sola unidad tratada):** un estado, un país → no hay grupo control natural; el control sintético construye uno ponderando el donor pool.

## Errores típicos

- **Conceptual:** confundir tendencias **paralelas** (trayectorias) con niveles iguales — DiD no exige que los grupos arranquen igual, solo que evolucionen igual sin tratamiento.
- **De supuestos:** no testear pre-tendencias (event study) ni correr placebos.
- **Técnico:** aplicar TWFE a adopción escalonada sin estimadores robustos (Callaway-Sant'Anna).

## Transferencia isomorfa

La doble diferencia y los efectos fijos no son solo de econometría:

- **DiD ↔ experimentación con control:** un A/B donde mides el *cambio* en tratamiento menos el *cambio* en control (en vez de niveles) es DiD; absorbe estacionalidad común igual que PA absorbe la tendencia (conecta con [[arena-ads4]]).
- **Efectos fijos ↔ demeaning por usuario:** restar la media de cada usuario antes de modelar elimina su sesgo estable no observado — es el estimador within aplicado a features de recomendación.
- **Control sintético ↔ causal impact / forecasting contrafactual:** predecir "qué habría pasado sin el cambio" con un modelo ajustado al periodo pre es la misma idea que el gemelo sintético, ahora con series de tiempo.

Moraleja de la arista: *casi todo diseño cuasi-experimental cambia el supuesto incómodo (CIA, "medí los confundidores") por otro más defendible (tendencias paralelas, efectos estables) — elegir bien el contrafactual es el oficio.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Panel + confundidores estables no observados | Efectos fijos (within) |
| Política sobre unos, control disponible, antes/después | DiD (tendencias paralelas) |
| ¿Tendencias paralelas? | Event study (pre-tendencias≈0) + placebos |
| Adopción escalonada + heterogeneidad | No TWFE ingenuo (Goodman-Bacon); estimadores robustos |
| Una sola unidad tratada (estado/país) | Control sintético + inferencia por permutación |

---

> **Síntesis:** los **efectos fijos** barren confundidores **invariantes en el tiempo** no observados (within, exogeneidad estricta). **DiD** resta la tendencia común y los niveles fijos para dar el **ATT** bajo **tendencias paralelas** (apóyalo con event study/placebos; cuidado con TWFE escalonado). El **control sintético** construye un gemelo ponderado del donor pool para una unidad tratada, con inferencia por **permutación**. Cada diseño cambia el CIA por otro supuesto más defendible.

---

*Retrieval: (1) ¿qué controlan los efectos fijos y qué no?; (2) la doble diferencia de DiD y su supuesto; (3) ¿cómo apoyas las tendencias paralelas?; (4) ¿qué es el control sintético y cómo se hace inferencia?*
