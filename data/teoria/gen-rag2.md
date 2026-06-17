# Embeddings y chunking: cómo se representa y trocea el conocimiento

> Recurso troncal: **MIT-AI.md (Semana 9)**. Las dos decisiones que más determinan la calidad de un RAG. Sigue a [[gen-rag1]] (por qué RAG) y prepara [[gen-rag3]] (recuperación y construcción del pipeline).

## De qué trata (y qué sabrás hacer al final)

Para que un RAG "encuentre lo relevante", primero hay que (1) **representar** el significado del texto como números que se puedan comparar —**embeddings**— y (2) **partir** los documentos en pedazos del tamaño correcto —**chunking**—. Suenan a detalles de plomería, pero son donde **la mayoría de los RAG fallan o triunfan**: un buen modelo de embeddings con mal chunking recupera basura, y viceversa.

La intuición de los embeddings: imagina un **mapa gigante** donde cada texto es un punto, y los textos de **significado parecido están cerca**. "perro", "cachorro" y "can" caen en el mismo barrio; "perro" y "ecuación diferencial" en continentes distintos. Un embedding es las **coordenadas** de un texto en ese mapa. Buscar lo relevante = encontrar los puntos más cercanos a la pregunta.

La intuición del chunking: no puedes meter un libro entero como un solo punto en el mapa (perderías el detalle) ni cada palabra suelta (perderías el contexto). Hay que cortarlo en **párrafos coherentes**: ni tan grandes que mezclen muchos temas, ni tan chicos que pierdan sentido. Cortar bien es un arte con reglas.

Al terminar podrás: (1) explicar qué es un **embedding** y la **similitud coseno**; (2) razonar el **tradeoff del tamaño de chunk**; (3) nombrar estrategias de chunking (fijo, por estructura, con solapamiento); y (4) elegir un **modelo de embeddings** con criterio.

## Embeddings: significado como coordenadas

Un **embedding** es un vector (cientos a miles de números) que representa el significado de un texto, producido por un modelo entrenado para que **textos similares tengan vectores cercanos**. La cercanía se mide casi siempre con **similitud coseno**: el coseno del ángulo entre dos vectores.

$$\text{sim}(a, b) = \frac{a \cdot b}{\lVert a\rVert\,\lVert b\rVert}$$

Vale 1 si apuntan en la misma dirección (muy similares), 0 si son ortogonales (no relacionados), −1 si opuestos. Se usa el **ángulo** (no la distancia) porque importa la *dirección* del significado, no la magnitud. Fíjate en el eco de [[gen-tf2]]: ahí la relevancia era un producto punto Query·Key; aquí es producto punto pregunta·documento. **RAG es atención sobre el corpus**, y la similitud coseno es su puntaje.

Los embeddings modernos vienen de modelos tipo Transformer ([Sentence-BERT, Reimers & Gurevych, 2019](https://arxiv.org/abs/1908.10084); familias E5, BGE, OpenAI `text-embedding-3`, etc.). Para elegir uno, mira el [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) (benchmark estándar de embeddings) y considera: idioma (¿multilingüe?), dimensión (más no siempre mejor), longitud máxima, y costo.

## El tradeoff del tamaño de chunk

Cada fragmento se embebe como **un** vector. El tamaño del fragmento crea una tensión central:

| Chunks **grandes** | Chunks **pequeños** |
|---|---|
| Más contexto por fragmento | Más precisión: el vector representa una idea, no diez |
| Riesgo: un vector "promedia" muchos temas → se diluye y recupera mal | Riesgo: se pierde el contexto que da sentido (referencias rotas) |
| Menos fragmentos, índice más barato | Más fragmentos, más recuperación granular |

La regla: el chunk debe ser **una unidad semántica coherente** —idealmente un párrafo o sección que responda "una cosa"—. Demasiado grande y el embedding se vuelve un puré sin foco; demasiado chico y "el reembolso es de 60 días" pierde a qué producto se refería. No hay número mágico universal (cientos de tokens es un punto de partida común), pero la **estructura del documento** manda más que el conteo de tokens.

## Estrategias de chunking

- **Tamaño fijo (por tokens/caracteres):** simple, rápido; riesgo de cortar a media frase/idea.
- **Con solapamiento (overlap):** los chunks comparten un margen (p. ej. 10-20%) para no perder contexto en los bordes; estándar pragmático.
- **Por estructura (recursivo):** respeta los límites naturales —encabezados, párrafos, secciones— (el [RecursiveCharacterTextSplitter de LangChain](https://python.langchain.com/docs/concepts/text_splitters/) es el caballo de batalla). Casi siempre mejor que el fijo ciego.
- **Semántico:** corta donde cambia el tema (detectando saltos de similitud entre frases). Más caro, a veces mejor.
- **Enriquecido:** añadir al chunk su título/sección o un pequeño resumen ("contextual retrieval", [Anthropic, 2024](https://www.anthropic.com/news/contextual-retrieval)) para que el fragmento no pierda su contexto global.

## Mini-ejemplo trabajado

Documento: un manual con secciones "Reembolsos", "Envíos", "Garantías", cada una de 3 párrafos. 

- **Chunk malo (todo el manual = 1 vector):** la pregunta "¿cuántos días de reembolso?" se compara con un vector que mezcla reembolsos+envíos+garantías → similitud tibia, recuperación pobre.
- **Chunk malo (cada frase = 1 vector):** recuperas "60 días" pero sin "para clientes enterprise" (estaba en otra frase) → respuesta incompleta o errónea.
- **Chunk bueno (por sección/párrafo, con solapamiento y título):** el fragmento "Reembolsos — Enterprise: 60 días, requiere aprobación…" es una unidad coherente con su contexto → alta similitud con la pregunta, recuperación precisa.

Predicción antes de seguir: si embebes los **documentos** con un modelo y las **preguntas** con **otro** modelo distinto, ¿funcionará la búsqueda? → No: estarían en **mapas distintos**, las coordenadas no son comparables. **Pregunta y documentos deben embeberse con el MISMO modelo** (mismo espacio vectorial). Error clásico.

## Señales de reconocimiento

| Señal | Qué pensar |
|---|---|
| "El RAG recupera fragmentos irrelevantes" | Chunks demasiado grandes (diluidos) o mal modelo |
| "Recupera el dato pero le falta contexto" | Chunks demasiado pequeños; añade overlap/título |
| "Funciona en inglés pero no en español" | Modelo de embeddings no multilingüe |
| "Documentos y queries se embeben con modelos distintos" | Espacios incompatibles → búsqueda rota |

## Errores típicos

- **Chunk único gigante o frases sueltas:** los dos extremos degradan la recuperación; busca la unidad semántica.
- **Modelos de embedding distintos para query y documentos:** rompe la comparación; usa el mismo.
- **Ignorar la estructura del documento:** cortar por tokens a ciegas parte ideas; respeta encabezados/párrafos.
- **Asumir que "más dimensiones = mejor":** la calidad la decide el benchmark (MTEB) y el ajuste a tu dominio, no el tamaño del vector.

## Contraejemplo y caso borde

- **Contraejemplo (similitud coseno no es comprensión):** dos textos pueden tener alta similitud coseno y significar lo contrario ("el contrato **sí** se renueva" vs "**no** se renueva") si el modelo de embeddings no captura bien la negación. La recuperación es un proxy de relevancia, no una garantía de verdad — por eso luego se evalúa la respuesta ([[gen-rag4]]).
- **Caso borde (tablas y código):** los modelos de embeddings de texto representan mal **tablas, fórmulas y código**; un chunk que es una tabla puede recuperarse pésimo. Requiere preprocesamiento especial (convertir tabla a texto descriptivo, o embeddings especializados).

## Transferencia isomorfa

- **Embedding ↔ coordenadas / hashing semántico:** convertir algo no estructurado en un punto en un espacio donde "cerca = parecido" es la misma idea de los embeddings de [[gen-tf4]] (y de los que filtran privacidad en [[cyber-mls2]]: un embedding puede reconstruir su origen — son representaciones ricas).
- **Chunking ↔ normalización/granularidad en bases de datos:** elegir la unidad correcta (¿fila por transacción o por sesión?) decide qué consultas son fáciles, igual que el chunk decide qué se recupera bien.
- **Similitud coseno ↔ el QK de la atención:** mismo producto punto normalizado; RAG es atención sobre el corpus.

Moraleja de la arista: *embeber es poner el significado en un mapa; chunkear es decidir el tamaño de los puntos. Pregunta y documentos, en el mismo mapa.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para un manual con secciones, propón una estrategia de chunking (tamaño, overlap, qué metadato añadir) y justifícala con el tradeoff grande/pequeño.
- **Misión externa (lab vivo):** explora el [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) y la guía de [text splitters de LangChain](https://python.langchain.com/docs/concepts/text_splitters/). **Criterio de cierre:** elegir un modelo de embeddings para un caso (idioma, costo) y justificar el chunking.
- **Mini-entregable:** una "ficha de indexación" para un corpus tuyo: modelo de embeddings elegido (y por qué), estrategia de chunking, overlap y metadatos por chunk.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (embeddings, similitud y chunking como diseño de recuperación) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** comparar chunking fijo, semantico y con solape usando el mismo set de preguntas.
2. **Baseline obligatorio:** chunks grandes sin solape.
3. **Versión mejorada:** chunking calibrado por estructura y embeddings adecuados.
4. **Evaluación:** recall@k, precisión@k y cobertura del answer span.
5. **Fallo que debes explicar:** el answer span queda partido o enterrado en chunks demasiado grandes.
6. **Transferencia:** bases de conocimiento legales o médicas donde la cita exacta importa.

**Laboratorio externo principal:** [pgvector](https://github.com/pgvector/pgvector).
**Laboratorio alternativo:** [RAGAS](https://docs.ragas.io/).
**Ruta de cluster:** asistente RAG con recuperación, atribucion, pruebas de faithfulness y casos adversarios.

**Entregable:** tabla de retrieval con chunks, queries, top-k y diagnóstico. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y qué harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** un **embedding** pone el significado de un texto como **coordenadas** en un mapa donde *cerca = parecido*; la relevancia se mide con **similitud coseno** (el QK de la atención, a escala de corpus). El **chunking** parte los documentos en **unidades semánticas coherentes**: ni tan grandes que el vector se diluya, ni tan chicas que pierdan contexto —prefiere cortar por **estructura**, con **solapamiento** y metadatos (título/resumen)—. Regla inviolable: **pregunta y documentos se embeben con el mismo modelo** (mismo espacio). La recuperación es un **proxy** de relevancia (cuidado con negación, tablas y código), no garantía de verdad.

---

**Referencias**

- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. *EMNLP*. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)
- Muennighoff, N., et al. (2023). MTEB: Massive text embedding benchmark. *EACL*. [arXiv:2210.07316](https://arxiv.org/abs/2210.07316) · [Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- Anthropic. (2024). Introducing contextual retrieval. [anthropic.com](https://www.anthropic.com/news/contextual-retrieval)
- LangChain. (n.d.). Text splitters (concepts). [python.langchain.com](https://python.langchain.com/docs/concepts/text_splitters/)

*Retrieval: (1) ¿qué es un embedding y qué mide la similitud coseno?; (2) ¿cuál es el tradeoff del tamaño de chunk?; (3) nombra 3 estrategias de chunking; (4) ¿por qué pregunta y documentos deben usar el mismo modelo de embeddings?*
