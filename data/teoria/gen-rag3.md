# Recuperación y construcción del pipeline RAG

> Recurso troncal: **MIT-AI.md (Semana 9)**. Ensambla embeddings y chunking ([[gen-rag2]]) en un pipeline que recupera bien. Prepara [[gen-rag4]] (RAG avanzado y evaluación).

## De qué trata (y qué sabrás hacer al final)

Ya tienes los documentos troceados y embebidos. Esta lección es el **acto de recuperar**: cómo se busca entre millones de vectores rápido, por qué la búsqueda **solo semántica** falla en casos importantes, cómo combinarla con búsqueda por palabras clave (**híbrida**), y cómo **reordenar** (re-ranking) para poner lo mejor arriba. Es donde un RAG mediocre se vuelve uno bueno.

La intuición: recuperar es una **biblioteca con dos bibliotecarios**. Uno entiende de *significado* (el semántico: te trae libros sobre tu tema aunque no usen tus palabras exactas). Otro es literal (el de palabras clave: si buscas el código de error "ERR-4021", te trae exactamente lo que contiene ese código, que el semántico podría pasar por alto). Los mejores sistemas usan **a los dos** y luego un editor (**re-ranker**) que lee los candidatos con cuidado y los ordena por relevancia real antes de dárselos al modelo.

Al terminar podrás: (1) explicar la **búsqueda de vecinos cercanos (ANN)** y por qué es aproximada; (2) razonar cuándo falla la búsqueda **semántica** y por qué conviene la **híbrida**; (3) entender el **re-ranking** (cross-encoder); y (4) elegir $k$ y construir el flujo recuperar→aumentar→generar.

## Búsqueda de vecinos cercanos (y por qué es aproximada)

Con la pregunta embebida, hay que hallar los chunks cuyos vectores estén más cerca (mayor similitud coseno, [[gen-rag2]]). Comparar contra **todos** (búsqueda exacta) es $O(n)$ por consulta: inviable con millones de vectores. Por eso las **bases vectoriales** (FAISS, Pinecone, Weaviate, pgvector) usan **ANN** (*Approximate Nearest Neighbors*): índices como **HNSW** ([Malkov & Yashunin, 2018](https://arxiv.org/abs/1603.09320)) que encuentran los vecinos *casi* siempre correctos en tiempo casi logarítmico. El tradeoff: un poquito de exactitud a cambio de velocidad enorme. Para RAG, perder ocasionalmente el vecino #7 real importa poco; la latencia, mucho.

## Por qué la búsqueda semántica sola no basta — búsqueda híbrida

La búsqueda por embeddings entiende significado, pero **falla** en:
- **Términos exactos raros:** códigos (`ERR-4021`), nombres propios, SKUs, siglas internas — el embedding los "promedia" y pierde la coincidencia literal.
- **Palabras clave que importan:** una negación, un número, un nombre técnico que define la respuesta.

La solución estándar es **búsqueda híbrida**: combinar la semántica (densa, por embeddings) con la **léxica** (dispersa, tipo **BM25** — [Robertson & Zaragoza, 2009](https://www.nowpublishers.com/article/Details/INR-019), el clásico de recuperación por palabras). Se fusionan los rankings (p. ej. con **Reciprocal Rank Fusion**, [Cormack et al., 2009](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)). La híbrida captura lo mejor de ambos: significado **y** coincidencia exacta. Es de las mejoras de mayor retorno en RAG real.

## Re-ranking: leer con lupa los candidatos

La recuperación inicial (semántica/híbrida) es rápida pero "gruesa": prioriza recall (traer suficientes candidatos), no precisión fina. El **re-ranking** toma los, digamos, 50 candidatos y los reordena con un modelo más caro y preciso: un **cross-encoder** que lee la **pregunta y cada candidato juntos** (no por separado) y puntúa su relevancia real. Diferencia clave con los embeddings (bi-encoder), que codifican pregunta y documento **por separado**: el cross-encoder ve la interacción y es mucho más preciso, pero demasiado caro para correr sobre millones — por eso se usa **solo** sobre los top candidatos. Pipeline típico: **recuperar 50 (rápido) → re-rankear a los 5 mejores (preciso) → dárselos al LLM**.

## Elegir $k$ y armar el prompt aumentado

- **$k$ (cuántos fragmentos pasar al LLM):** muy pocos → puede faltar la respuesta; demasiados → ruido, costo y el modelo "se pierde en el medio" (efecto *lost in the middle*, [Liu et al., 2023](https://arxiv.org/abs/2307.03172): los LLMs atienden peor a lo que está a la mitad de un contexto largo). Suele bastar un puñado (3-8) de fragmentos **buenos** tras re-ranking, mejor que 50 mediocres.
- **Construcción del prompt:** instrucción ("responde **solo** con el contexto; si no está, dilo") + los fragmentos (idealmente con su fuente para citar) + la pregunta. La instrucción de "no inventes fuera del contexto" reduce alucinaciones y habilita la atribución de [[gen-rag1]].

## Mini-ejemplo trabajado

Usuario: *"¿Qué significa el error ERR-4021 en el módulo de pagos?"*

- **Solo semántica:** recupera párrafos sobre "errores de pago en general" pero **no** el que menciona literalmente `ERR-4021` (el embedding diluyó el código) → respuesta vaga.
- **Híbrida:** BM25 encuentra el chunk con `ERR-4021` exacto **y** la semántica trae contexto de pagos → ambos entran.
- **Re-ranking:** entre los candidatos, el cross-encoder pone arriba el que de verdad explica ese código.
- **$k$ y prompt:** se pasan los 4 mejores con la instrucción "responde solo con esto y cita". El LLM responde correcto y citando.

Predicción antes de seguir: subes $k$ de 4 a 40 "para no perder nada". ¿Mejora? → probablemente **empeora**: más ruido, más costo, y el efecto *lost in the middle* hace que el modelo ignore el fragmento clave si quedó enterrado. Más contexto **no** es mejor contexto; mejor recuperación sí.

## Señales de reconocimiento

| Señal | Jugada |
|---|---|
| "No encuentra códigos/SKUs/siglas exactos" | Búsqueda híbrida (añade BM25) |
| "Trae candidatos relevantes pero mal ordenados" | Re-ranking con cross-encoder |
| "Con muchos millones de vectores va lento" | ANN (HNSW), no búsqueda exacta |
| "Subí k y empeoró" | Lost in the middle; recupera mejor, no más |
| "El modelo responde fuera del contexto" | Instrucción 'solo con el contexto' + evaluar fidelidad |

## Errores típicos

- **Solo semántica para todo:** falla en términos exactos; la híbrida es casi siempre mejor.
- **Pasar 50 chunks al LLM:** ruido, costo y *lost in the middle*; re-rankea y pasa pocos buenos.
- **Confundir bi-encoder (embeddings) con cross-encoder (re-ranker):** el segundo lee pregunta+doc juntos y es más preciso pero más caro.
- **No instruir "responde solo con el contexto":** invita a alucinar y rompe la atribución.

## Contraejemplo y caso borde

- **Contraejemplo (ANN no siempre conviene):** con pocos miles de vectores, la búsqueda **exacta** es suficientemente rápida y evita la pérdida de exactitud del ANN; este último brilla a gran escala. No compliques de más.
- **Caso borde (la respuesta no está en el corpus):** si ningún chunk contiene la respuesta, un buen RAG debe **decir "no lo sé / no está en los documentos"**, no forzar una respuesta con el contexto irrelevante recuperado. Detectar "no hay evidencia suficiente" es parte del diseño (y se mide en [[gen-rag4]]).

## Transferencia isomorfa

- **Recuperar→re-rankear ↔ filtrar→verificar:** primero un filtro barato y amplio (recall), luego una verificación cara y precisa (precisión) sobre los pocos finalistas — el mismo patrón que "buscar candidatos y luego revisarlos a fondo" que usamos en revisión adversaria.
- **Híbrida (denso + léxico) ↔ defensa en profundidad:** dos métodos con puntos ciegos distintos se cubren mutuamente (como combinar SAST+SCA en [[cyber-dev4]]).
- **Lost in the middle ↔ memoria de trabajo:** tanto un LLM como un humano rinden peor cuando se les satura el centro de la atención; menos y mejor > más y disperso.

Moraleja de la arista: *recupera amplio y barato, re-rankea estrecho y caro, pasa pocos y buenos; combina significado con literalidad.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** diseña el pipeline de recuperación para una base de soporte técnico con muchos códigos de error: ¿semántica, léxica o híbrida? ¿re-ranking? ¿qué $k$?
- **Misión externa (lab vivo):** revisa la doc de [pgvector](https://github.com/pgvector/pgvector) o [FAISS](https://github.com/facebookresearch/faiss) y la idea de [HNSW](https://arxiv.org/abs/1603.09320). **Criterio de cierre:** explicar por qué la búsqueda es "aproximada" y qué se gana.
- **Mini-entregable:** un diagrama del pipeline recuperar→re-rankear→aumentar→generar, marcando dónde entra la híbrida y el efecto de $k$.

## Reconstrucción mínima en código

Recuperacion robusta: combina busqueda semantica con coincidencia lexica y re-ranking.

```python
docs = {"d1": "como reseteo mi contrasena",
        "d2": "error E500 al pagar en el checkout",
        "d3": "fallo generico del servidor"}

def lexico(q, t):                       # coincidencia exacta (ancla IDs como 'E500')
    return len(set(q.split()) & set(t.split()))

def hibrida(q, alpha=0.5):              # combina semantico (stub) + lexico
    semantico = {d: 0.5 for d in docs}  # <- aqui iria tu busqueda vectorial/ANN
    score = {d: alpha*semantico[d] + (1-alpha)*lexico(q, docs[d]) for d in docs}
    return sorted(score, key=score.get, reverse=True)

print(hibrida("error E500 al pagar"))   # el lexico rescata el ID exacto 'E500'
```

**Qué observar:** La busqueda vectorial confunde documentos vecinos; lo lexico ancla IDs/codigos exactos. El re-ranking sube precision@k sin destruir recall.

<!-- GENAI_TRANSFER_ASSIGNMENT_START -->
## Asignación práctica de transferencia

**Objetivo graduado:** convertir la idea central (recuperación robusta: ANN, hibrida y re-ranking) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementación o diseño, baseline, métrica, error analysis y transferencia.

1. **Implementación o diseño:** comparar vector-only, BM25/hibrida y re-ranking sobre consultas difíciles.
2. **Baseline obligatorio:** top-k vectorial directo.
3. **Versión mejorada:** recuperación hibrida con re-ranking y k calibrado.
4. **Evaluación:** MRR, recall@k, precisión@k, latencia y costo por consulta.
5. **Fallo que debes explicar:** top-k trae textos parecidos pero no el fragmento que responde.
6. **Transferencia:** soporte técnico: sinonimos, IDs exactos y documentos similares.

**Laboratorio externo principal:** [LlamaIndex documentation](https://docs.llamaindex.ai/).
**Laboratorio alternativo:** [RAGAS](https://docs.ragas.io/).
**Ruta de cluster:** asistente RAG con recuperación, atribucion, pruebas de faithfulness y casos adversarios.

**Entregable:** benchmark de retrieval con tabla por consulta y decisión de k. Debe incluir una conclusión breve: qué aprendiste, qué falló, qué mediste y qué harías distinto si lo llevaras a producción.

**Rúbrica de excelencia:**

- Corrección técnica: la implementación o el diseño corresponde a la lección, no a una demo genérica.
- Evidencia: incluye baseline, métrica, casos borde y al menos una comparación o ablation.
- Transferencia: explica qué estructura profunda se conserva al moverlo a otro dominio.
- Error analysis: nombra el supuesto roto, el síntoma observable y la siguiente acción.
- Comunicación: cualquier revisor puede reproducir la decisión sin confiar en autoridad externa.
<!-- GENAI_TRANSFER_ASSIGNMENT_END -->

---

> **Síntesis:** recuperar bien es más que coseno: a escala se usa **ANN** (HNSW) —aproximado pero rapidísimo—; la **búsqueda híbrida** combina semántica (embeddings) con léxica (**BM25**) para capturar significado **y** términos exactos; el **re-ranking** (cross-encoder, que lee pregunta+doc juntos) reordena los candidatos por relevancia real. Pasa **pocos fragmentos buenos** tras re-ranking (cuidado con *lost in the middle*: más contexto ≠ mejor) con la instrucción "responde **solo** con el contexto y cita". Patrón: **recuperar amplio y barato → re-rankear estrecho y caro → generar con evidencia**.

---

**Referencias**

- Malkov, Y. A., & Yashunin, D. A. (2018). Efficient and robust approximate nearest neighbor search using HNSW graphs. *IEEE TPAMI*. [arXiv:1603.09320](https://arxiv.org/abs/1603.09320)
- Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. *Foundations and Trends in IR*. [nowpublishers](https://www.nowpublishers.com/article/Details/INR-019)
- Cormack, G. V., Clarke, C. L. A., & Büttcher, S. (2009). Reciprocal rank fusion. *SIGIR*. [PDF](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- Liu, N. F., et al. (2023). Lost in the middle: How language models use long contexts. *TACL*. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- pgvector. (n.d.). Open-source vector similarity search for Postgres. [GitHub](https://github.com/pgvector/pgvector)

*Retrieval: (1) ¿qué es ANN y qué tradeoff hace?; (2) ¿por qué la búsqueda híbrida supera a la solo-semántica?; (3) ¿qué hace un re-ranker (cross-encoder) y por qué solo sobre los top candidatos?; (4) ¿por qué subir $k$ puede empeorar la respuesta?*
