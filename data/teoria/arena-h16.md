# La causalidad según Pearl II: diagramas, junciones y paradojas

## Diagramas causales (DAGs)

Grafo dirigido acíclico: nodos = variables, flechas = causas directas. Codifica supuestos; las **flechas ausentes** son las afirmaciones más fuertes (niegan un efecto directo) y las que dan poder —y riesgo— a la identificación. Hace los supuestos **transparentes** y debatibles. Evolución de los path diagrams de Wright; misma forma que una **red bayesiana** (dependencia) pero con flechas interpretadas como **causa**.

## Las tres junciones

| Junción | Forma | Rol de B | Asociación A-C | Al condicionar B |
|---|---|---|---|---|
| **Cadena** | A→B→C | mediador | sí | se **bloquea** |
| **Bifurcación (fork)** | A←B→C | confundidor | sí (espuria) | se **bloquea** |
| **Collider** | A→B←C | efecto común | **no** | se **abre** (espuria) |

Regla: condicionar un **mediador o confundidor cierra** el flujo; condicionar un **collider lo abre**. Ver [[diagramas-causales-junciones]]. Por eso se ajusta el **confundidor** (cierra el camino trasero) pero **nunca** un collider ni un mediador (introducirían sesgo).

## Paradojas

- **Simpson:** la asociación se **invierte** al estratificar. La estadística no dice qué tabla creer: solo el **rol causal** de la variable decide — ajusta si es **confundidor** (mira subgrupos), no si es **mediador/collider** (mira el agregado). Es la prueba palpable de "mind over data". Ver [[paradoja-simpson-causal]].
- **Berkson:** muestras **seleccionadas** por un efecto común muestran correlaciones espurias (p. ej. enfermedades correlacionadas entre hospitalizados).
- **Monty Hall:** la puerta que abre el presentador es un **collider** (efecto de dónde está el premio y de tu elección); condicionarla actualiza las probabilidades → conviene **cambiar** (2/3). Ver [[sesgo-collider-berkson]].

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| ¿Ajusto esta variable? | Mira su junción: fork sí, mediador/collider no |
| La asociación se invierte al estratificar | Simpson: el DAG decide qué tabla |
| Muestra filtrada por un efecto común | Berkson: correlación espuria (sesgo de selección) |
| Correlación rara entre cosas "independientes" | ¿Condicionaste un collider? |
| Defender un ajuste con "cambia el coeficiente" | No: decide la estructura, no los números |

---

> **Síntesis:** un **DAG** descompone la realidad en tres **junciones** —cadena (mediador), fork (confundidor), collider (efecto común)—. Condicionar **cierra** cadenas/forks y **abre** colliders: por eso se ajusta el confundidor y nunca el collider/mediador. **Simpson, Berkson y Monty Hall** son colliders/selección disfrazados; el **modelo causal**, no la estadística, dice qué tabla creer.

---

*Retrieval: (1) las 3 junciones y su efecto al condicionar; (2) ¿cómo resuelve el DAG la paradoja de Simpson?; (3) ¿qué es el sesgo de Berkson?; (4) ¿por qué Monty Hall es un collider?*
