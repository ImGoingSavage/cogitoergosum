# The Mixtape IV: panel/efectos fijos, DiD y control sintético

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
