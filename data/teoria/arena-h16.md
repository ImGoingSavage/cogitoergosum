# La causalidad según Pearl II: diagramas, junciones y paradojas

## De qué trata esta lección (y qué sabrás hacer al final)

Si la causalidad necesita un modelo, ¿cómo se dibuja ese modelo? Con un **DAG** (grafo dirigido acíclico). Esta lección construye, desde cero, la gramática de los DAGs: las **tres junciones** (cadena, bifurcación, collider) que componen cualquier grafo, y la regla de oro que de ellas se deriva —cuándo ajustar una variable *cierra* el sesgo y cuándo lo *abre*—. Con eso, las paradojas famosas (Simpson, Berkson, Monty Hall) dejan de ser misterios: son la misma estructura disfrazada.

Al terminar podrás: (1) clasificar una variable como mediador, confundidor o collider; (2) aplicar la regla "ajusta confundidores, nunca colliders ni mediadores"; (3) explicar por qué un collider fabrica correlación de la nada; y (4) reconocer Simpson/Berkson/Monty Hall como casos de condicionar un efecto común. Cada junción entra por un ejemplo concreto.

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

## Mini-ejemplo trabajado: un collider fabrica correlación de la nada

Dos rasgos **independientes** entre sí: *talento* y *suerte*, cada uno 0 o 1 con probabilidad ½, sin ninguna relación. A un actor lo **admiten** si talento + suerte ≥ 1 (tiene al menos uno).

**Predicción antes de seguir:** en la población, talento y suerte no tienen ninguna relación (conocer uno no dice nada del otro). Si ahora miras *solo a los actores admitidos*, ¿seguirán sin relación, o aparecerá una correlación entre ellos? Apuesta sí/no antes de contar los casos.

Mira solo a los admitidos:

- (talento=1, suerte=1), (1,0), (0,1) entran; (0,0) queda fuera.
- Entre los admitidos, si ves talento=0, entonces forzosamente suerte=1. Si ves talento=1, la suerte puede ser 0 o 1.

Acabas de crear una **correlación negativa** talento–suerte *dentro de la muestra admitida*, aunque en la población eran independientes. No tocaste los datos; **condicionaste un collider** (la admisión, efecto común de ambos). Esa es la maquinaria de Berkson y de "los actores guapos actúan peor" — la selección, no el mundo, generó la asociación.

## Prototipo, contraejemplo y caso borde

- **Prototipo (ajustar es correcto):** fork A←B→C. B (edad) confunde fármaco y recuperación → ajustar por B cierra el camino trasero. Aquí *más control = menos sesgo*.
- **Contraejemplo (ajustar **mete** sesgo):** collider A→B←C. "Controlar por todo lo que mejora el R²" te lleva a meter un collider y *abrir* una asociación espuria. El R² sube y la estimación empeora — el ajuste que parecía prudente fue el error.
- **Caso borde (mediador):** cadena A→B→C. Ajustar por el mediador B *borra* justo el efecto que querías medir (el efecto indirecto desaparece). Revela que "controlar variables" no es neutro: depende del rol causal.

## Errores típicos

- **Conceptual:** tratar el DAG como una red de correlaciones (red bayesiana) en vez de causas — las flechas afirman causa directa.
- **De supuestos:** justificar un ajuste porque "cambia el coeficiente". El criterio es la **estructura** (¿fork, mediador o collider?), no el número.
- **Técnico:** condicionar sin querer un collider al **filtrar la muestra** (p. ej. "solo casos hospitalizados") — el filtro *es* un ajuste.

## Transferencia isomorfa

El collider no es una curiosidad epidemiológica; es el mismo sesgo en otros dominios:

- **Sesgo de selección en ML ↔ collider:** entrenar solo con "usuarios que convirtieron" condiciona en un efecto común (la conversión) y rompe la relación feature→outcome (conecta con [[arena-dmls2]], muestreo y etiquetas).
- **Survivorship bias en Quant ↔ Berkson:** evaluar una estrategia solo sobre fondos que sobrevivieron es muestrear por un efecto común (sobrevivir) → rendimiento espurio.
- **Monty Hall ↔ test diagnóstico:** "abrir una puerta" = recibir un dato que *depende* del estado oculto; actualizar como Bayes es el mismo gesto que reponderar la probabilidad de enfermedad ante un síntoma (conecta con la tasa base, [[arena-q2]]).

Moraleja de la arista: *casi todo "sesgo raro" famoso —Berkson, Simpson, survivorship, Monty Hall— es la misma estructura: condicionar (o seleccionar) sobre un efecto común.*

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
