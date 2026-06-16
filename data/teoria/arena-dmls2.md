# Datos de entrenamiento: muestreo, etiquetas y desbalance

## De qué trata esta lección (y qué sabrás hacer al final)

Un modelo no es mejor que los datos con que se entrena, y construir esos datos esconde tres decisiones difíciles: **cómo muestrear**, **cómo etiquetar** y **qué hacer con el desbalance**. Esta lección las construye desde cero: las familias de muestreo (incluido el reservoir sampling para streams de tamaño desconocido y el importance sampling para distribuciones inaccesibles), las fuentes de etiquetas (de las caras hand labels a las natural labels gratis del comportamiento), y por qué el accuracy miente cuando una clase es rara.

Al terminar podrás: (1) describir el reservoir sampling y por qué garantiza uniformidad sin conocer $n$; (2) usar importance sampling (reponderar por $P/Q$) y reconocerlo como la misma maquinaria del IP weighting causal; (3) aprovechar natural labels y entender el feedback-loop length; y (4) abandonar el accuracy por F1/AUC con resampling o weighted loss ante el desbalance. Cada técnica entra por un ejemplo.

## Muestreo: dos familias

- **No probabilístico (nonprobability):** la selección no se basa en ninguna probabilidad — por conveniencia, por bola de nieve, por juicio, por cuotas. Es rápido y barato para arrancar, pero las muestras **no son representativas** y arrastran sesgos al modelo. (Muchos datasets famosos se armaron así.)
- **Aleatorio (random):** muestreo aleatorio simple, **estratificado** (divide la población en grupos/estratos y muestrea dentro de cada uno para no dejar fuera grupos raros) y **ponderado** (cada muestra recibe un peso según su importancia).

### Reservoir sampling (para streams)
Cuando los datos **llegan en streaming** y no sabes cuántos habrá ni caben en memoria, ¿cómo tomar k muestras con igual probabilidad? El **reservoir sampling**: (1) mete los primeros k elementos en el reservorio; (2) para el n-ésimo elemento entrante genera un aleatorio i en [1, n]; (3) si i ≤ k, reemplaza el i-ésimo del reservorio por el nuevo, si no, no hagas nada. Garantiza que en cualquier momento que pares, las k muestras tienen la probabilidad correcta (k/n cada elemento).

### Importance sampling
Permite muestrear de una distribución P(x) **cara o imposible** de muestrear, usando otra Q(x) fácil (la "proposal distribution") y **reponderando** cada muestra por P(x)/Q(x). Solo requiere que Q(x) > 0 siempre que P(x) ≠ 0. En RL basado en políticas se usa para estimar la política nueva reponderando recompensas de la vieja.

## Etiquetas (labeling)

La mayoría de los modelos en producción son **supervisados** → dependen de etiquetas de calidad, que suelen ser el cuello de botella.

- **Hand labels:** caras, lentas, amenazan la privacidad y sufren **label multiplicity** (distintos anotadores discrepan → define instrucciones claras).
- **Natural labels:** tareas donde el sistema **infiere la etiqueta solo**, de la realidad o del comportamiento del usuario. Canónico: recomendadores (un clic o su ausencia es la etiqueta — *implicit labels*). El **feedback loop length** (cuánto tarda en llegar la etiqueta natural) define cuán rápido detectas fallos: clics llegan en minutos; una compra puede tardar semanas.
- **Weak supervision:** en vez de etiquetar a mano, escribe **labeling functions** (heurísticas: "si el email contiene 'oferta', spam") y combina sus votos, ruidosos pero baratos y escalables (Snorkel).
- **Semi-supervisión:** parte de pocas etiquetas y propaga a más con supuestos estructurales.
- **Transfer learning** y **active learning:** en active learning el modelo **elige qué ejemplos** quiere que le etiqueten (los más informativos: mayor incertidumbre), en lugar de etiquetar al azar — más eficiente en etiquetas.

## Desbalance de clases (class imbalance)

Cuando una clase domina (fraude: 99.9% legítimo), un modelo que diga "siempre la mayoritaria" acierta 99.9% y es inútil. Remedios:
- **Métricas correctas:** nada de accuracy; usa F1, precision/recall, AUC.
- **Resampling:** **oversample** la minoría (p.ej. SMOTE) o **undersample** la mayoría.
- **Cost-sensitive / weighted loss:** penaliza más los errores en la clase rara.

---

## Mini-ejemplo trabajado: reservoir sampling, por qué funciona

Llega un stream de tamaño **desconocido** y quieres **k=1** muestra uniformemente al azar (cada elemento con prob 1/n al final, sin saber n). El algoritmo:

1. Guarda el 1.º en el reservorio.
2. Para el n-ésimo elemento, genera `i` aleatorio en [1, n]; si `i ≤ k` (aquí i=1), **reemplaza**; si no, descarta.

¿Por qué es uniforme? El elemento n entra con prob **k/n = 1/n**. ✓ ¿Y los anteriores siguen con 1/n? El elemento 1 sobrevive si los siguientes no lo expulsan: P(sobrevive) = ∏... = 1/n también. La magia: en *cualquier* punto donde pares, cada elemento visto tiene exactamente probabilidad k/n — sin conocer n de antemano ni guardar el stream entero.

**Predicción antes de seguir:** quieres muestrear de una distribución P cara/imposible de samplear, pero tienes una Q fácil. ¿Cómo? **Importance sampling**: muestrea de Q y repondera cada muestra por **P(x)/Q(x)** (requiere Q>0 donde P≠0). Es *exactamente* la maquinaria de IP weighting / off-policy: estimar la política nueva reponderando la vieja (conecta con [[arena-h5]]).

## Prototipo, contraejemplo y caso borde

- **Prototipo (estratificado):** hay grupos raros que no quieres perder → muestrea dentro de cada estrato.
- **Contraejemplo (no probabilístico):** armar el dataset por conveniencia/bola de nieve → rápido pero no representativo, arrastra sesgo al modelo.
- **Caso borde (feedback-loop length largo):** la etiqueta natural de "compra" tarda semanas en llegar → detectas fallos lento; los clics (minutos) son más rápidos.

## Errores típicos

- **Conceptual:** confiar en el **accuracy** con clases desbalanceadas (99.9% legítimo → "siempre legítimo" acierta 99.9% e inútil); usa F1/AUC.
- **Técnico:** muestrear un stream materializándolo en memoria en vez de **reservoir sampling**.
- **De etiquetas:** ignorar la **label multiplicity** (anotadores que discrepan) sin instrucciones claras.

## Transferencia isomorfa

- **Importance sampling ↔ IP weighting / off-policy:** reponderar por P/Q es el mismo estimador que corrige confundimiento o evalúa una política nueva con datos de la vieja (conecta con [[arena-h5]] y [[arena-h20]]).
- **Reservoir sampling ↔ algoritmos de streaming con estado mínimo:** mantener k muestras correctas sin guardar el stream es el espíritu de los algoritmos online de un paso (conecta con [[arena-dmls3]], streaming features).
- **Desbalance / accuracy paradox ↔ tasa base:** una clase rara vuelve engañosa la métrica global, como el PPV de un fenotipo raro (conecta con [[arena-mldp2]] y [[arena-h13]]).

Moraleja de la arista: *muestrea bien (estratificado para grupos raros, reservoir para streams, importance para distribuciones inaccesibles), aprovecha natural labels y abandona el accuracy cuando hay desbalance.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Datos en stream, no caben en memoria, quiero k al azar" | Reservoir sampling |
| "Muestrear de una distribución cara/imposible" | Importance sampling (reponderar por P/Q) |
| "Hay grupos raros que no quiero perder" | Muestreo estratificado |
| "Etiquetar a mano es carísimo" | Natural labels / weak supervision (labeling functions) |
| "¿Qué ejemplos mando a etiquetar?" | Active learning: los más inciertos/informativos |
| "99.9% de una clase, accuracy engañosa" | F1/AUC + resampling o weighted loss |

---

> **Síntesis:** Los datos de entrenamiento se gobiernan por tres decisiones. **Muestreo:** el no probabilístico es rápido pero sesgado; el aleatorio (estratificado para no perder grupos raros) es representativo; en streams usa **reservoir sampling**, y para distribuciones inaccesibles, **importance sampling** (reponderar por P/Q). **Etiquetas:** las manuales son caras y discrepantes, así que aprovecha **natural labels** (con su feedback-loop length), **weak supervision** (labeling functions) y **active learning** (el modelo pide los ejemplos más informativos). **Desbalance de clases:** abandona accuracy por F1/AUC y aplica resampling o weighted loss.

---

*Retrieval: cierra y responde: (1) describe el algoritmo de reservoir sampling y qué garantiza; (2) ¿qué hace importance sampling y cuándo?; (3) ¿qué son natural labels y el feedback-loop length?; (4) tres remedios para el desbalance de clases.*
