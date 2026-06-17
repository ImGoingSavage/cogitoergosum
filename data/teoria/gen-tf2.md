# Self-attention: Query, Key, Value y atención escalada

> Recurso troncal: [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) §3.2. El corazón mecánico del Transformer. Sigue a [[gen-tf1]] (la idea de atención) y prepara [[gen-tf3]] (multi-head y arquitectura).

## De qué trata (y qué sabrás hacer al final)

En [[gen-tf1]] vimos *qué* es la atención (mezcla ponderada de la entrada). Aquí vemos *cómo* se calcula en un Transformer: el mecanismo **Query–Key–Value (QKV)** y la fórmula de **scaled dot-product attention**. Esta es la ecuación más importante de la IA del siglo XXI; al terminar, no será un conjuro sino una idea clara.

La intuición: piensa en una **búsqueda en una biblioteca**. Tú llegas con una pregunta (**Query**). Cada libro tiene una etiqueta en el lomo que dice de qué trata (**Key**). Comparas tu pregunta con cada etiqueta para ver cuáles libros encajan (**puntaje de similitud**). Los que más encajan, los lees con más cuidado; tomas de cada libro su contenido (**Value**) en proporción a cuánto encajó su etiqueta con tu pregunta. La self-attention es exactamente eso, hecho con vectores y de forma diferenciable: cada palabra **pregunta** qué otras palabras le importan, las **puntúa**, y se queda con una **mezcla** de su contenido.

Al terminar podrás: (1) explicar qué son **Query, Key y Value** y de dónde salen; (2) leer y justificar la fórmula $\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$ símbolo a símbolo; (3) explicar **por qué se divide por $\sqrt{d_k}$**; y (4) distinguir **self-attention** de **cross-attention**.

## De cada palabra salen tres vectores: Q, K, V

Cada palabra (token) entra como un vector (su *embedding*). De ese vector, mediante tres matrices aprendidas $W^Q, W^K, W^V$, se derivan **tres** proyecciones distintas:

- **Query ($q$):** "lo que esta palabra está buscando" en las demás.
- **Key ($k$):** "lo que esta palabra ofrece" para ser encontrada.
- **Value ($v$):** "el contenido que esta palabra aporta" si resulta relevante.

$$q_i = x_i W^Q,\quad k_i = x_i W^K,\quad v_i = x_i W^V$$

La misma palabra tiene, a la vez, una pregunta (Q), una etiqueta (K) y un contenido (V). La separación es la clave: lo que buscas (Q) no es lo mismo que lo que ofreces (K). Las matrices $W$ se **aprenden** durante el entrenamiento; ahí vive el "conocimiento" de cómo relacionar palabras.

## La fórmula, paso a paso

La **scaled dot-product attention** se calcula así:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$$

Desarmémosla por partes:

1. **$Q K^\top$ — los puntajes de relevancia.** El producto punto entre la query $q_i$ y cada key $k_j$ mide **cuánto encajan**. Producto punto alto = vectores alineados = "esta palabra me importa". Es una matriz $n\times n$: para cada palabra, su afinidad con todas.
2. **$/\sqrt{d_k}$ — el escalado.** Se divide por la raíz de la dimensión de las keys, $d_k$. (Por qué, en la sección siguiente.)
3. **$\text{softmax}(\cdot)$ — convertir puntajes en pesos.** El softmax por filas transforma los puntajes en una distribución que **suma 1**: los $\alpha_{ij}$ de [[gen-tf1]]. Ahora cada palabra tiene un reparto de "cuánta atención" da a las demás.
4. **$\cdots\, V$ — la mezcla.** Se multiplican esos pesos por los Values: cada palabra se queda con una **suma ponderada del contenido** de las que le importaron. Eso es su nueva representación, ahora **contextualizada**.

En una frase: *cada palabra pregunta (Q) a todas (K), normaliza cuánto le importa cada una (softmax), y se lleva una mezcla de su contenido (V).*

## Por qué se divide por $\sqrt{d_k}$ (el detalle que casi todos omiten)

Cuando $d_k$ (la dimensión de los vectores) es grande, los productos punto $q\cdot k$ tienden a tener **magnitudes grandes** (sumas de muchos términos). Si entran al softmax valores muy grandes, el softmax se **satura**: pone casi todo el peso en un solo elemento y deja gradientes minúsculos para el resto, lo que **frena el aprendizaje**. Dividir por $\sqrt{d_k}$ mantiene la varianza de los puntajes en torno a 1, evitando esa saturación. El propio [paper (§3.2.1)](https://arxiv.org/abs/1706.03762) lo justifica así. 

**[CAJA NEGRA OK]** No necesitas la derivación de la varianza para usar Transformers; sí debes conservar la intuición: *sin el escalado, el softmax se vuelve casi un máximo duro y el modelo no aprende bien*. Es la respuesta a una pregunta de entrevista frecuente.

## Self-attention vs cross-attention

- **Self-attention:** Q, K y V salen de la **misma** secuencia. Cada palabra atiende a las otras palabras de su propia frase. Es lo que contextualiza ("banco" mira a "senté", como en [[gen-tf1]]).
- **Cross-attention:** las Q salen de una secuencia (p. ej., lo que el decoder lleva generado) y las K, V de **otra** (p. ej., la frase de entrada del encoder). Es el puente encoder→decoder en traducción, y la base de cómo un modelo "consulta" un contexto externo.

Esta distinción reaparece en RAG: el modelo hace, en efecto, *cross-attention* sobre los documentos recuperados.

## Mini-ejemplo trabajado (con números pequeños)

Frase de 3 palabras, vectores de dimensión $d_k = 2$ (simplificado). Supón que para la palabra "gato" su query es $q=[1, 0]$, y las keys son: "el" $k_1=[0,1]$, "gato" $k_2=[1,0]$, "duerme" $k_3=[0.7, 0.7]$.

- Puntajes (producto punto con $q=[1,0]$): "el" → $0$; "gato" → $1$; "duerme" → $0.7$.
- Escala por $\sqrt{2}\approx1.41$: $0,\ 0.71,\ 0.49$.
- Softmax → pesos aprox.: $0.22,\ 0.45,\ 0.36$ (suman 1).
- La nueva representación de "gato" = $0.22\,v_{el} + 0.45\,v_{gato} + 0.36\,v_{duerme}$.

"Gato" se queda sobre todo con su propio contenido (0.45) y con el del verbo "duerme" (0.36) — capturó con qué se relaciona. Predicción antes de seguir: si "gato" solo pudiera atenderse a sí misma (peso 1 en $v_{gato}$), ¿qué perdería? → toda la información de **contexto**; sería como leer cada palabra aislada. La atención es justamente lo que mezcla el contexto.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "Necesito que cada elemento se relacione con todos" | self-attention (Q, K, V de la misma fuente) |
| "Una secuencia consulta a otra" | cross-attention (Q de una, K/V de otra) |
| "El softmax pone todo el peso en uno y no aprende" | falta el escalado $/\sqrt{d_k}$ |
| "¿Por qué tres matrices y no una?" | separar buscar (Q), ofrecer (K) y aportar (V) |

## Errores típicos

- **Confundir Q, K y V como si fueran iguales:** son tres proyecciones distintas del mismo vector, con roles distintos.
- **Olvidar el escalado:** sin $/\sqrt{d_k}$, el entrenamiento se degrada por saturación del softmax.
- **Creer que la atención "elige una" palabra:** elige una **distribución** (suma ponderada), no un único ganador (salvo que el softmax se sature, que es justo lo que se evita).

## Contraejemplo y caso borde

- **Contraejemplo:** producto punto alto **no** siempre significa "semánticamente similar" en el sentido humano; significa "alineado en el espacio aprendido". El modelo aprende un espacio donde la relevancia para la tarea, no la sinonimia, gobierna los puntajes.
- **Caso borde:** si todos los puntajes son iguales, el softmax da pesos **uniformes** → la atención colapsa a un promedio simple de todos los Values, perdiendo selectividad. El modelo aprende a evitarlo, pero es el degenerado a tener en mente.

## Transferencia isomorfa

QKV es un **diccionario diferenciable**: una Query busca entre Keys y recupera Values ponderados — como un `dict`/hash lookup, pero suave (en vez de "la clave existe o no", "cada clave encaja un poco"). 
- En **bases de datos vectoriales** (RAG, [[cyber-llm2]]): tu consulta (Query) se compara con embeddings (Keys) y recuperas documentos (Values) por similitud. Es atención sin softmax, sobre millones de vectores.
- En **sistemas de recomendación**: el perfil del usuario (Q) puntúa ítems (K) y recupera contenido (V). 

Moraleja de la arista: *la atención es un lookup blando: buscar con una query, puntuar contra keys, mezclar values.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** con $q=[2,0]$ y keys $k_1=[1,1], k_2=[2,0], k_3=[0,2]$, calcula a mano los puntajes, escálalos por $\sqrt{2}$ y di cualitativamente quién recibe más peso.
- **Misión externa (lab vivo):** lee [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) en la sección *Attention*. **Criterio de cierre:** mapear cada parte del código (`scores`, `p_attn`, `torch.matmul`) a la fórmula de esta lección.
- **Mini-entregable:** explica la fórmula $\text{softmax}(QK^\top/\sqrt{d_k})V$ a alguien que no sabe ML, usando la analogía de la biblioteca, nombrando Q, K, V y el porqué del escalado.

---

> **Síntesis:** la **self-attention** deriva de cada token tres vectores —**Query** (lo que busca), **Key** (lo que ofrece) y **Value** (lo que aporta)— mediante matrices aprendidas. La fórmula $\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$ se lee así: $QK^\top$ puntúa la relevancia de todos contra todos, $/\sqrt{d_k}$ evita que el softmax se sature, el **softmax** convierte puntajes en pesos que suman 1, y multiplicar por $V$ produce una **mezcla ponderada del contenido**. Es un **lookup blando** (diccionario diferenciable). **Self-attention** mezcla dentro de una secuencia; **cross-attention** consulta otra (la base de traducción y de RAG).

---

**Referencias**

- Vaswani, A., et al. (2017). Attention is all you need (§3.2 Scaled Dot-Product Attention). *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Rush, A., et al. (2018/2022). The Annotated Transformer. *Harvard NLP*. [nlp.seas.harvard.edu](https://nlp.seas.harvard.edu/annotated-transformer/)
- Alammar, J. (2018). The Illustrated Transformer. [jalammar.github.io](https://jalammar.github.io/illustrated-transformer/)

*Retrieval: (1) ¿qué representan Q, K y V y de dónde salen?; (2) lee la fórmula $\text{softmax}(QK^\top/\sqrt{d_k})V$ parte por parte; (3) ¿por qué se divide por $\sqrt{d_k}$?; (4) self-attention vs cross-attention.*
