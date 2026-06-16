# Interpretabilidad III: métodos agnósticos (efectos e importancia)

> Tratan al modelo como **caja negra** (solo input→output). Perturban features y miran cómo cambia la predicción. Ventaja: comparan cualquier modelo.

## De qué trata esta lección (y qué sabrás hacer al final)

¿Y si tu modelo es una caja negra (un random forest, una red profunda)? Entonces lo interpretas **perturbando inputs y mirando outputs**, sin abrir la caja. Esta lección construye, desde cero, esos métodos agnósticos: el PDP (efecto marginal global) y su trampa de independencia, el ICE (que revela la heterogeneidad que el PDP esconde), el ALE (la corrección para features correlacionadas), la H-statistic (interacción) y la importancia por permutación.

Al terminar podrás: (1) entender qué supuesto rompe el PDP bajo correlación y por qué el ALE lo arregla (no inventa combinaciones imposibles); (2) usar el ICE para detectar efectos heterogéneos; (3) medir importancia por permutación correctamente (en test, no train); y (4) cuantificar interacción con la H-statistic. La trampa de independencia del PDP conecta con la positividad causal ([[arena-h3]]). Continúa [[arena-iml2]].

## PDP — Partial Dependence Plot (efecto marginal global)

Muestra el **efecto marginal promedio** de una (o dos) features sobre la predicción. Para cada valor de xⱼ, **fija** ese valor en todas las instancias, deja el resto como está, **promedia** las predicciones. La curva resultante es el efecto medio. **Intuitivo y global.** **Supuesto fuerte y peligroso: independencia** — al fijar xⱼ creas combinaciones **imposibles** si xⱼ se correlaciona con otras features (p. ej. altura=2 m con peso=50 kg). Además **oculta heterogeneidad**: efectos positivos y negativos que se cancelan dan una curva plana engañosa. Máx. 2 features (visualización).

## ICE — Individual Conditional Expectation

Una **línea por instancia**: cómo cambia **su** predicción al variar xⱼ (PDP es el promedio de todas las líneas ICE). **Revela la heterogeneidad** que el PDP esconde: si las líneas no son paralelas, hay **interacción**. **c-ICE** (centradas) fijan todas en un punto de anclaje para comparar pendientes. Mismo problema de independencia que el PDP.

## ALE — Accumulated Local Effects (la corrección para features correlacionadas)

Resuelve el sesgo del PDP bajo correlación. En vez de fijar xⱼ a un valor global, divide xⱼ en **ventanas (cuantiles)** y dentro de cada ventana calcula la **diferencia** de predicción al mover xⱼ de un extremo a otro de la ventana (usando solo instancias **reales** de esa ventana → no inventa combinaciones imposibles), y luego **acumula** esas diferencias locales. Resultado **centrado en 0**: "comparado con la predicción media, en x=v el efecto es ±k". Más rápido que el PDP y **no sesgado por correlación**. (Los **M-plots** condicionan en lugar de intervenir y mezclan el efecto de features correlacionadas; ALE lo evita.)

## Interacción de features — H-statistic (Friedman)

Mide cuánto de la varianza de la predicción se debe a la **interacción** entre features (lo que NO se explica por sus efectos individuales). Compara la partial dependence conjunta con la **suma** de las parciales individuales. **H² ∈ [0,1]**: 0 = sin interacción; 1 = el efecto es **puro** de interacción. Se calcula por par (H entre xⱼ y xₖ) o de una feature con todas las demás. Caro (cuadrático en n) y con varianza por el muestreo.

## Importancia por permutación

Importancia global y agnóstica: **baraja** (permuta) los valores de una feature, rompiendo su relación con el target, y mide **cuánto sube el error** del modelo. Mucho aumento ⇒ feature importante; nada ⇒ irrelevante. Basada en el **model reliance** de Fisher/Rudin. **Decisiones clave:** ¿usar datos de **train o test**? → **test** mide cuánto importa para *generalizar* (train puede inflar por overfitting). Repetir varias veces (es aleatorio) y promediar. **Trampa con features correlacionadas:** se reparten la importancia (cada una parece menos importante) y la permutación crea instancias **irreales**.

## Modelo sustituto global (global surrogate)

Entrena un **modelo interpretable** (árbol, lineal) para **imitar las predicciones** de la caja negra (target = ŷ del modelo negro, no la y real). Luego interpretas el sustituto. Mide la calidad con **R²** entre sustituto y modelo negro (fidelity). Barato y agnóstico, pero solo es válido donde el sustituto **aproxima bien**; no sustituye al original.

---

## Mini-ejemplo trabajado: la trampa de independencia del PDP

Quieres el efecto marginal del `peso corporal` sobre un riesgo predicho. El PDP **fija** peso = 50 kg en *todas* las personas, promedia las predicciones, y repite para cada valor. Problema: al fijar peso=50 kg en una persona de **2 m de altura**, creas una combinación **imposible** (altura y peso correlacionan) y le pides al modelo que prediga en una región donde nunca vio datos → la curva PDP se contamina con extrapolaciones absurdas.

La cura es **ALE**: divide el peso en ventanas (cuantiles) y, *dentro de cada ventana*, mide cuánto cambia la predicción al mover el peso de un extremo al otro **usando solo personas reales de esa ventana**; luego acumula. Nunca inventa combinaciones imposibles → no sesgado por correlación.

Además el PDP **oculta heterogeneidad**: si en la mitad de la gente el efecto es +k y en la otra −k, la curva promedio sale **plana** (engañosa). **ICE** (una línea por persona) lo revela: líneas no paralelas = interacción.

**Predicción antes de seguir:** calculas importancia por permutación barajando una feature. ¿Sobre train o test? **Test**: en train, una feature memorizada por overfitting parece importante aunque no generalice; el test mide cuánto importa para *generalizar*.

## Prototipo, contraejemplo y caso borde

- **Prototipo (ALE):** features correlacionadas → efectos locales acumulados sobre instancias reales, centrado en 0.
- **Contraejemplo (PDP bajo correlación):** usar PDP con features muy correlacionadas → combinaciones imposibles y curva sesgada.
- **Caso borde (permutación con correlated features):** dos features correlacionadas se **reparten** la importancia (cada una parece menos importante) — no concluyas "ninguna importa".

## Errores típicos

- **Conceptual:** confiar en el PDP cuando hay correlación (supone independencia) o cuando hay heterogeneidad (la curva plana engaña).
- **De evaluación:** medir importancia por permutación en **train** en vez de **test**.
- **De interpretación:** leer una curva PDP plana como "sin efecto" cuando ICE mostraría efectos que se cancelan.

## Transferencia isomorfa

- **Independencia del PDP ↔ positividad/overlap causal:** fijar una feature a valores sin soporte real es el mismo pecado que evaluar un efecto causal donde no hay overlap (conecta con [[arena-h3]], positividad).
- **Permutación en test, no train ↔ generalización:** medir importancia donde el modelo *no* memorizó es la misma lógica de evaluar fuera de muestra (conecta con [[arena-isl3]], remuestreo).
- **Correlated features reparten importancia ↔ confundimiento/colinealidad:** atribuir mal entre features correlacionadas es el problema causal de distinguir el predictor real (conecta con [[arena-h4]]).

Moraleja de la arista: *al perturbar una feature no inventes combinaciones imposibles (ALE > PDP bajo correlación), mide importancia en test, y desconfía de la curva promedio que esconde heterogeneidad.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Efecto promedio de una feature, global | **PDP** (ojo: supone independencia, oculta heterogeneidad) |
| Sospecho efectos heterogéneos/interacción | **ICE** (una línea por instancia; no paralelas = interacción) |
| Features **correlacionadas** | **ALE** (efectos locales acumulados, no sesgado) |
| ¿Hay interacción y cuánta? | **H-statistic** de Friedman (H²∈[0,1]) |
| ¿Qué features importan globalmente? | **Importancia por permutación** (en **test**, repetida) |
| Quiero una visión global simple del modelo negro | **Surrogate global** (mide fidelity con R²) |

---

> **Síntesis:** los métodos agnósticos perturban inputs y observan outputs. **PDP/ICE** muestran efectos (PDP el promedio, ICE la heterogeneidad) pero **suponen independencia**; **ALE** corrige el sesgo por **correlación** acumulando efectos locales sobre instancias reales. La **H-statistic** cuantifica interacción. La **importancia por permutación** baraja una feature y mide cuánto sube el error (hazla en **test**). El **surrogate global** imita la caja negra con un modelo interpretable (valida con R²).

---

*Retrieval: (1) ¿qué supuesto rompe el PDP bajo correlación y qué método lo arregla?; (2) ¿qué revela ICE que el PDP esconde?; (3) explica la importancia por permutación y por qué usar test; (4) ¿qué mide la H-statistic y su rango?*
