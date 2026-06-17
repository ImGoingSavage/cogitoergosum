#!/usr/bin/env node
// Enriquece la Fase 9 con asignaciones transferibles, laboratorios externos,
// banco ampliado y metadatos de auditoria. Idempotente: conserva preguntas
// hechas a mano y regenera solo las marcadas con MARKER.

import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const unidadesPath = join(ROOT, 'data', 'genai', '_unidades.json');
const taxonomiaPath = join(ROOT, 'data', 'genai', '_taxonomia.json');
const teoriaDir = join(ROOT, 'data', 'teoria');

const MARKER = 'enriquecer-genai-transferencia-v1';
const REVIEW_DATE = '2026-06-17';
const BLOCK_START = '<!-- GENAI_TRANSFER_ASSIGNMENT_START -->';
const BLOCK_END = '<!-- GENAI_TRANSFER_ASSIGNMENT_END -->';

const links = {
  cs224n: {
    nombre: 'Stanford CS224N: NLP with Deep Learning',
    url: 'https://web.stanford.edu/class/cs224n/',
  },
  cs25: {
    nombre: 'Stanford CS25: Transformers United',
    url: 'https://web.stanford.edu/class/cs25/',
  },
  karpathy: {
    nombre: 'Karpathy Neural Networks: Zero to Hero',
    url: 'https://karpathy.ai/zero-to-hero.html',
  },
  nanogpt: {
    nombre: 'nanoGPT',
    url: 'https://github.com/karpathy/nanoGPT',
  },
  annotated: {
    nombre: 'The Annotated Transformer',
    url: 'https://nlp.seas.harvard.edu/annotated-transformer/',
  },
  pytorchTransformer: {
    nombre: 'PyTorch Transformer tutorial',
    url: 'https://docs.pytorch.org/tutorials/beginner/transformer_tutorial.html',
  },
  deeplearning: {
    nombre: 'DeepLearning.AI Generative AI for Everyone',
    url: 'https://www.deeplearning.ai/courses/generative-ai-for-everyone/',
  },
  ragLangchain: {
    nombre: 'LangChain RAG tutorial',
    url: 'https://python.langchain.com/docs/tutorials/rag/',
  },
  llamaIndex: {
    nombre: 'LlamaIndex documentation',
    url: 'https://docs.llamaindex.ai/',
  },
  ragas: {
    nombre: 'RAGAS',
    url: 'https://docs.ragas.io/',
  },
  pgvector: {
    nombre: 'pgvector',
    url: 'https://github.com/pgvector/pgvector',
  },
  openaiEvals: {
    nombre: 'OpenAI Evals',
    url: 'https://github.com/openai/evals',
  },
  lmarena: {
    nombre: 'LMArena',
    url: 'https://lmarena.ai/',
  },
  promptfoo: {
    nombre: 'promptfoo',
    url: 'https://www.promptfoo.dev/docs/intro/',
  },
  promptingGuide: {
    nombre: 'Prompt Engineering Guide',
    url: 'https://www.promptingguide.ai/',
  },
  sutton: {
    nombre: 'Sutton & Barto: Reinforcement Learning',
    url: 'http://incompleteideas.net/book/the-book-2nd.html',
  },
  anthropicAgents: {
    nombre: 'Anthropic: Building Effective Agents',
    url: 'https://www.anthropic.com/research/building-effective-agents',
  },
  anthropicMulti: {
    nombre: 'Anthropic multi-agent research system',
    url: 'https://www.anthropic.com/engineering/multi-agent-research-system',
  },
  autogen: {
    nombre: 'Microsoft AutoGen',
    url: 'https://microsoft.github.io/autogen/',
  },
  langgraph: {
    nombre: 'LangGraph tutorials',
    url: 'https://langchain-ai.github.io/langgraph/tutorials/',
  },
  nist: {
    nombre: 'NIST AI Risk Management Framework',
    url: 'https://www.nist.gov/itl/ai-risk-management-framework',
  },
  mitRisk: {
    nombre: 'MIT AI Risk Repository',
    url: 'https://airisk.mit.edu/',
  },
};

const clusterProfiles = {
  'genai-transformers': {
    shorthand: 'Transformers',
    priority: 'implementacion PyTorch desde tensores hasta un mini GPT',
    capstone: 'proyecto final tipo GPT-2: tokenizador simple, decoder causal, entrenamiento, generacion y evaluacion',
    labs: [links.cs224n, links.karpathy, links.annotated, links.nanogpt, links.pytorchTransformer],
    gradedStyle: 'asignaciones estilo CS224N/Karpathy: shapes, pruebas unitarias, ablations y reporte de errores',
  },
  'genai-rag': {
    shorthand: 'RAG',
    priority: 'construccion de un sistema RAG evaluable, con corpus propio y diagnostico por componente',
    capstone: 'asistente RAG con recuperacion, atribucion, pruebas de faithfulness y casos adversarios',
    labs: [links.ragLangchain, links.llamaIndex, links.ragas, links.pgvector],
    gradedStyle: 'asignaciones de ingenieria: corpus, chunking, retriever, generador, metricas y error analysis',
  },
  'genai-eval': {
    shorthand: 'Evaluacion',
    priority: 'benchmarking de LLMs, rubricas, jueces, held-out y control de alucinacion',
    capstone: 'harness de evaluacion con linea base, prompts candidatos, LLM-as-judge calibrado y reporte de regresiones',
    labs: [links.cs224n, links.openaiEvals, links.promptfoo, links.lmarena, links.promptingGuide],
    gradedStyle: 'asignaciones tipo Andrew Ng/Stanford: set, metrica, baseline, iteracion controlada y decision por evidencia',
  },
  'genai-agentes': {
    shorthand: 'Agentes',
    priority: 'del bucle RL a workflows con herramientas, agencia minima y humano en el lazo',
    capstone: 'agente con herramientas estrechas, limites duros, evaluacion por task success y fallos controlados',
    labs: [links.sutton, links.anthropicAgents, links.langgraph],
    gradedStyle: 'asignaciones de diseno operativo: politica, herramientas, observaciones, limites y metricas',
  },
  'genai-multiagente': {
    shorthand: 'Multi-agente',
    priority: 'orquestacion, routing, RAG adaptativo y evaluacion por componente',
    capstone: 'sistema multi-agente con roles, grafo de estado, presupuesto, red team y comparacion contra agente unico',
    labs: [links.anthropicMulti, links.autogen, links.langgraph, links.ragas],
    gradedStyle: 'asignaciones de arquitectura: descomposicion, routing, limites, telemetria y ablation contra baseline',
  },
  'genai-responsable': {
    shorthand: 'IA responsable',
    priority: 'llevar GenAI a produccion con riesgos, costos, observabilidad y responsabilidad medible',
    capstone: 'diseno extremo a extremo para un vertical con evaluacion, seguridad, gobierno y operacion',
    labs: [links.nist, links.mitRisk, links.deeplearning, links.openaiEvals],
    gradedStyle: 'asignaciones ejecutivas y tecnicas: caso, matriz de riesgo, metrica, arquitectura y plan de despliegue',
  },
};

const blueprints = {
  'gen-tf1': {
    concept: 'cuello de botella seq2seq y atencion como recuperacion diferenciable',
    system: 'traductor secuencia-a-secuencia de juguete',
    build: 'comparar un encoder fijo con una capa de atencion sobre frases sinteticas',
    evidenceShort: 'medir desempeno por longitud y visualizar pesos sobre tokens lejanos',
    artifact: 'notebook con curva por longitud, heatmap de atencion y explicacion Q/A',
    baseline: 'LSTM encoder-decoder sin atencion',
    advanced: 'decoder con atencion Bahdanau o Transformer pequeno',
    failure: 'la calidad cae justo al aumentar la longitud de la frase',
    mistake: 'confundir el cuello de botella con vocabulario o hardware',
    transfer: 'RAG: conservar fuentes y recuperar fragmentos en vez de resumir todo',
    metric: 'accuracy/BLEU por longitud y error analysis de dependencias largas',
    labName: links.karpathy.nombre,
    labUrl: links.karpathy.url,
    secondLabName: links.cs224n.nombre,
    secondLabUrl: links.cs224n.url,
    capstoneStep: 'definir la intuicion que luego se implementara como self-attention causal',
    recognition: 'si el sistema olvida el principio al crecer la secuencia, sospecha compresion en vector fijo',
  },
  'gen-tf2': {
    concept: 'self-attention Q/K/V y atencion escalada',
    system: 'capa PyTorch de scaled dot-product attention',
    build: 'implementar Q, K, V, mascara y softmax(QK^T/sqrt(d_k))V desde tensores',
    evidenceShort: 'pasar tests de shapes, mascara causal y suma de pesos por fila',
    artifact: 'modulo PyTorch minimo con pruebas de shapes, mascara y gradientes',
    baseline: 'producto punto sin escalado ni mascara',
    advanced: 'scaled dot-product attention vectorizada',
    failure: 'el softmax se satura y casi todo el peso cae en un token',
    mistake: 'confundir Query con Value o creer que sqrt(d_k) ahorra computo',
    transfer: 'cross-attention para que un decoder consulte documentos recuperados',
    metric: 'tests unitarios de tensores, ablation sin escalado y estabilidad de gradientes',
    labName: links.annotated.nombre,
    labUrl: links.annotated.url,
    secondLabName: links.pytorchTransformer.nombre,
    secondLabUrl: links.pytorchTransformer.url,
    capstoneStep: 'convertir la atencion en el bloque central del mini GPT',
    recognition: 'si QK^T produce logits enormes, divide por sqrt(d_k) antes del softmax',
  },
  'gen-tf3': {
    concept: 'multi-head attention, masking causal y bloques decoder',
    system: 'bloque decoder estilo GPT',
    build: 'construir multi-head attention con mascara causal, residual, LayerNorm y MLP',
    evidenceShort: 'probar que ningun token atiende al futuro y que cada head aprende patrones distintos',
    artifact: 'bloque decoder entrenable con tests de causalidad y ablation de heads',
    baseline: 'una sola cabeza sin mascara causal',
    advanced: 'multi-head causal attention con residual y LayerNorm',
    failure: 'el modelo hace leakage mirando tokens futuros durante entrenamiento',
    mistake: 'creer que mas cabezas siempre mejora sin medir redundancia',
    transfer: 'agentes: separar subproblemas como heads especializadas, pero medir redundancia',
    metric: 'perplexity de validacion, prueba de fuga causal y diversidad entre heads',
    labName: links.nanogpt.nombre,
    labUrl: links.nanogpt.url,
    secondLabName: links.karpathy.nombre,
    secondLabUrl: links.karpathy.url,
    capstoneStep: 'ensamblar el bloque repetible del proyecto GPT-2 pequeno',
    recognition: 'si una prediccion usa informacion del futuro, la mascara causal esta rota',
  },
  'gen-tf4': {
    concept: 'positional encoding, embeddings y extension Transformer a vision',
    system: 'mini Transformer con posiciones y una variante de patches tipo ViT',
    build: 'anadir embeddings posicionales y comparar texto causal contra patches de imagen',
    evidenceShort: 'mostrar que sin posicion se pierde orden aunque el contenido sea el mismo',
    artifact: 'experimento con permutaciones, positional embeddings y reporte de errores',
    baseline: 'tokens sin codificacion de posicion',
    advanced: 'positional embeddings aprendidos o sinusoidales',
    failure: 'el modelo no distingue secuencias con los mismos tokens en otro orden',
    mistake: 'pensar que la atencion por si sola conoce el orden',
    transfer: 'vision: tratar imagenes como secuencias de patches con posicion',
    metric: 'accuracy en pares permutados y comparacion con/sin positional encoding',
    labName: links.cs25.nombre,
    labUrl: links.cs25.url,
    secondLabName: links.cs224n.nombre,
    secondLabUrl: links.cs224n.url,
    capstoneStep: 'cerrar el bloque Transformer reusable antes del entrenamiento GPT',
    recognition: 'si el orden importa y el modelo procesa en paralelo, necesitas posicion explicita',
  },
  'gen-rag1': {
    concept: 'RAG como recuperacion externa en vez de memorizar conocimiento',
    system: 'asistente sobre una carpeta de documentos propios',
    build: 'implementar el flujo pregunta -> embeddings -> top-k -> prompt aumentado -> respuesta',
    evidenceShort: 'medir si el fragmento correcto aparece en top-k y si la respuesta cita fuente',
    artifact: 'RAG minimo con corpus pequeno, citas y casos donde el modelo debe decir no se',
    baseline: 'LLM sin contexto recuperado',
    advanced: 'RAG con recuperacion semantica y atribucion',
    failure: 'el modelo inventa cuando el dato no estaba en su entrenamiento',
    mistake: 'usar fine-tuning para conocimiento cambiante que debe citarse',
    transfer: 'busqueda de soporte: responder solo con documentos verificables',
    metric: 'context recall, abstencion correcta y faithfulness contra fuentes',
    labName: links.ragLangchain.nombre,
    labUrl: links.ragLangchain.url,
    secondLabName: links.llamaIndex.nombre,
    secondLabUrl: links.llamaIndex.url,
    capstoneStep: 'conectar el mini GPT conceptual con conocimiento externo auditable',
    recognition: 'si el problema es conocimiento propio cambiante, piensa RAG antes de fine-tuning',
  },
  'gen-rag2': {
    concept: 'embeddings, similitud y chunking como diseno de recuperacion',
    system: 'indice vectorial de documentos con chunks controlados',
    build: 'comparar chunking fijo, semantico y con solape usando el mismo set de preguntas',
    evidenceShort: 'reportar recall@k por estrategia de chunking y ejemplos de fallos',
    artifact: 'tabla de retrieval con chunks, queries, top-k y diagnostico',
    baseline: 'chunks grandes sin solape',
    advanced: 'chunking calibrado por estructura y embeddings adecuados',
    failure: 'el answer span queda partido o enterrado en chunks demasiado grandes',
    mistake: 'tratar el chunk size como detalle cosmetico',
    transfer: 'bases de conocimiento legales o medicas donde la cita exacta importa',
    metric: 'recall@k, precision@k y cobertura del answer span',
    labName: links.pgvector.nombre,
    labUrl: links.pgvector.url,
    secondLabName: links.ragas.nombre,
    secondLabUrl: links.ragas.url,
    capstoneStep: 'preparar corpus recuperable para evaluacion y agentes',
    recognition: 'si el contexto correcto no llega al prompt, el generador no puede salvarlo',
  },
  'gen-rag3': {
    concept: 'recuperacion robusta: ANN, hibrida y re-ranking',
    system: 'pipeline de retrieval con busqueda vectorial e indice lexical',
    build: 'comparar vector-only, BM25/hibrida y re-ranking sobre consultas dificiles',
    evidenceShort: 'mostrar que el re-ranking sube precision sin destruir recall',
    artifact: 'benchmark de retrieval con tabla por consulta y decision de k',
    baseline: 'top-k vectorial directo',
    advanced: 'recuperacion hibrida con re-ranking y k calibrado',
    failure: 'top-k trae textos parecidos pero no el fragmento que responde',
    mistake: 'subir k sin medir ruido ni latencia',
    transfer: 'soporte tecnico: sinonimos, IDs exactos y documentos similares',
    metric: 'MRR, recall@k, precision@k, latencia y costo por consulta',
    labName: links.llamaIndex.nombre,
    labUrl: links.llamaIndex.url,
    secondLabName: links.ragas.nombre,
    secondLabUrl: links.ragas.url,
    capstoneStep: 'hacer que el contexto externo sea seleccionable y medible',
    recognition: 'si semantic search confunde documentos vecinos, agrega lexical/re-ranking',
  },
  'gen-rag4': {
    concept: 'evaluacion RAG separando recuperacion, generacion y fidelidad',
    system: 'RAG evaluado con triangulo retrieval-generacion-faithfulness',
    build: 'crear un set con preguntas, fuentes esperadas, respuestas y casos adversarios',
    evidenceShort: 'separar errores de retriever y errores de generador en una matriz',
    artifact: 'dashboard pequeno con context recall, faithfulness y ejemplos fallidos',
    baseline: 'evaluar solo la respuesta final',
    advanced: 'evaluacion por componente con RAGAS o rubrica propia',
    failure: 'mejoras de prompt esconden que el contexto correcto nunca se recupero',
    mistake: 'arreglar generacion cuando el fallo era retrieval',
    transfer: 'auditoria de asistentes corporativos con documentos privados',
    metric: 'context recall, faithfulness, answer relevancy y tasa de abstencion',
    labName: links.ragas.nombre,
    labUrl: links.ragas.url,
    secondLabName: links.openaiEvals.nombre,
    secondLabUrl: links.openaiEvals.url,
    capstoneStep: 'crear la misma disciplina de evaluacion que usaran agentes y LLMs',
    recognition: 'si solo miras la respuesta final, no sabes que componente fallo',
  },
  'gen-eval1': {
    concept: 'limites de BLEU/ROUGE y necesidad de metricas semanticas',
    system: 'benchmark de resumen con referencias y parafrasis',
    build: 'comparar ROUGE/BLEU contra BERTScore o juez rubricado en ejemplos controlados',
    evidenceShort: 'mostrar falsos positivos lexicos y falsos negativos por parafrasis',
    artifact: 'reporte con pares de salidas, metricas y juicio humano razonado',
    baseline: 'ROUGE/BLEU como unica metrica',
    advanced: 'metrica semantica mas revision de factualidad',
    failure: 'sube la superposicion de palabras pero baja la calidad real',
    mistake: 'creer que n-gramas equivalen a significado o factualidad',
    transfer: 'evaluar respuestas de un asistente sin una unica respuesta dorada',
    metric: 'correlacion con juicio humano, errores por parafrasis y factualidad',
    labName: links.cs224n.nombre,
    labUrl: links.cs224n.url,
    secondLabName: links.openaiEvals.nombre,
    secondLabUrl: links.openaiEvals.url,
    capstoneStep: 'definir el primer benchmark del proyecto final',
    recognition: 'si una parafrasis correcta puntua bajo, la metrica es demasiado lexical',
  },
  'gen-eval2': {
    concept: 'BERTScore, LLM-as-a-judge y calibracion de rubricas',
    system: 'juez de respuestas para QA/resumen con rubrica explicita',
    build: 'disenar una rubrica, calibrarla con ejemplos ancla y medir sesgos del juez',
    evidenceShort: 'probar sensibilidad a orden, verbosidad y respuestas ancla',
    artifact: 'harness de juez con rubrica, ejemplos oro y pruebas de sesgo',
    baseline: 'juez sin rubrica ni ejemplos ancla',
    advanced: 'LLM-as-judge calibrado y comparado con metrica semantica',
    failure: 'el juez premia respuestas largas o primeras por sesgo de posicion',
    mistake: 'tratar el juicio del LLM como verdad objetiva',
    transfer: 'evaluacion de prompts y modelos candidatos con criterios repetibles',
    metric: 'agreement con humano, bias tests y estabilidad entre seeds/modelos',
    labName: links.promptfoo.nombre,
    labUrl: links.promptfoo.url,
    secondLabName: links.lmarena.nombre,
    secondLabUrl: links.lmarena.url,
    capstoneStep: 'crear el juez que comparara checkpoints y prompts',
    recognition: 'si el juez cambia por orden o longitud, necesitas calibracion',
  },
  'gen-eval3': {
    concept: 'alucinacion, faithfulness y consistencia contra fuentes',
    system: 'detector de alucinacion para respuestas con contexto recuperado',
    build: 'implementar checks de afirmaciones contra contexto y consistencia multi-muestra',
    evidenceShort: 'marcar afirmaciones sin soporte y distinguir ausencia de evidencia de falsedad',
    artifact: 'set de hallucination eval con claims, fuentes y verdictos',
    baseline: 'aceptar respuestas plausibles sin verificar soporte',
    advanced: 'verificacion por claims y abstencion cuando falta evidencia',
    failure: 'una respuesta segura agrega datos no presentes en la fuente',
    mistake: 'confundir fluidez con verdad',
    transfer: 'dominios sensibles donde cada afirmacion necesita trazabilidad',
    metric: 'unsupported claim rate, faithfulness y tasa de abstencion correcta',
    labName: links.ragas.nombre,
    labUrl: links.ragas.url,
    secondLabName: links.openaiEvals.nombre,
    secondLabUrl: links.openaiEvals.url,
    capstoneStep: 'anadir guardrail evaluable al RAG o agente',
    recognition: 'si una afirmacion no se puede apuntar a una fuente, no esta verificada',
  },
  'gen-eval4': {
    concept: 'optimizacion de prompts dirigida por evaluacion y held-out',
    system: 'loop de prompt optimization con baseline y set oculto',
    build: 'probar candidatos de prompt cambiando una variable a la vez y midiendo held-out',
    evidenceShort: 'mostrar curva train/held-out y descartar cambios que sobreajustan',
    artifact: 'reporte de experimentos con baseline, candidatos, metricas y decision',
    baseline: 'prompt elegido por gusto o demo',
    advanced: 'prompt seleccionado por metrica en validacion y confirmado en held-out',
    failure: '99% en el set iterado pero caida en casos nuevos',
    mistake: 'optimizar sobre los mismos ejemplos hasta memorizar el benchmark',
    transfer: 'A/B interno de asistentes, clasificadores o extractores con prompts',
    metric: 'delta contra baseline, intervalo de confianza y regresiones por segmento',
    labName: links.deeplearning.nombre,
    labUrl: links.deeplearning.url,
    secondLabName: links.promptingGuide.nombre,
    secondLabUrl: links.promptingGuide.url,
    capstoneStep: 'cerrar el ciclo de mejora del proyecto final sin overfitting',
    recognition: 'si iteraste sobre el mismo set, exige held-out antes de creer la mejora',
  },
  'gen-ag1': {
    concept: 'bucle agente-entorno: estado, accion, recompensa y politica',
    system: 'entorno gridworld o tarea de decision secuencial',
    build: 'modelar estados, acciones, recompensas y politica antes de usar un LLM',
    evidenceShort: 'mostrar episodios, retorno descontado y decisiones de politica',
    artifact: 'simulador pequeno con trazas y funcion de recompensa explicada',
    baseline: 'script reactivo sin estado ni recompensa definida',
    advanced: 'agente con politica evaluada por retorno',
    failure: 'la recompensa proxy incentiva conductas no deseadas',
    mistake: 'llamar agente a cualquier prompt largo',
    transfer: 'workflows LLM: observar, decidir, actuar y volver a observar',
    metric: 'retorno promedio, tasa de exito y casos donde la recompensa falla',
    labName: links.sutton.nombre,
    labUrl: links.sutton.url,
    secondLabName: links.anthropicAgents.nombre,
    secondLabUrl: links.anthropicAgents.url,
    capstoneStep: 'definir si el problema necesita decision secuencial o solo pipeline',
    recognition: 'si hay estado, accion y feedback, razona como bucle agente-entorno',
  },
  'gen-ag2': {
    concept: 'Q-learning, policy gradient y RLHF como optimizacion de comportamiento',
    system: 'agente tabular y preferencia humana simulada',
    build: 'comparar actualizacion Q con una politica optimizada por recompensa',
    evidenceShort: 'mostrar curva de retorno y efecto de una recompensa mal especificada',
    artifact: 'notebook con Q-table, policy rollout y analisis de reward hacking',
    baseline: 'politica aleatoria o heuristica fija',
    advanced: 'Q-learning o policy gradient con evaluacion held-out',
    failure: 'el agente maximiza el proxy pero viola la intencion',
    mistake: 'creer que RLHF hace correcto todo lo que el usuario prefiere',
    transfer: 'alinear respuestas de LLM sin olvidar que la recompensa es proxy',
    metric: 'retorno, win rate por preferencia y ejemplos de reward hacking',
    labName: links.sutton.nombre,
    labUrl: links.sutton.url,
    secondLabName: links.deeplearning.nombre,
    secondLabUrl: links.deeplearning.url,
    capstoneStep: 'entender el limite de optimizar comportamiento por feedback',
    recognition: 'si una recompensa proxy puede explotarse, no confundas score con objetivo',
  },
  'gen-ag3': {
    concept: 'agentes LLM con ReAct, herramientas, memoria y autocrítica',
    system: 'agente que responde una tarea usando busqueda y calculadora',
    build: 'implementar ciclo pensar-actuar-observar con herramientas limitadas',
    evidenceShort: 'medir tool accuracy, pasos, costo y casos donde debe detenerse',
    artifact: 'trazas de agente con llamadas a herramientas, errores y correcciones',
    baseline: 'LLM de una sola respuesta sin herramientas',
    advanced: 'workflow ReAct con herramientas tipadas y limites duros',
    failure: 'el agente llama herramientas irrelevantes o actua con argumentos inseguros',
    mistake: 'dar herramientas amplias porque el modelo parece inteligente',
    transfer: 'asistentes operativos que consultan APIs pero requieren permisos estrechos',
    metric: 'task success, tool accuracy, pasos promedio y costo',
    labName: links.anthropicAgents.nombre,
    labUrl: links.anthropicAgents.url,
    secondLabName: links.langgraph.nombre,
    secondLabUrl: links.langgraph.url,
    capstoneStep: 'decidir donde el mini sistema necesita herramientas y donde no',
    recognition: 'si el modelo debe actuar fuera del texto, evalua permisos y herramienta',
  },
  'gen-ag4': {
    concept: 'seguridad de agentes: agencia minima, HITL y limites de ejecucion',
    system: 'agente con una herramienta de lectura y otra de escritura',
    build: 'disenar permisos, aprobaciones humanas y limites antes de conectar acciones reales',
    evidenceShort: 'probar que acciones irreversibles requieren aprobacion y quedan auditadas',
    artifact: 'matriz herramienta-permiso-riesgo y pruebas adversarias',
    baseline: 'agente autonomo con acceso amplio',
    advanced: 'workflow con agencia minima, validacion y humano en el lazo',
    failure: 'prompt injection o razonamiento erroneo dispara una accion irreversible',
    mistake: 'reducir seguridad a un system prompt mas estricto',
    transfer: 'compras, correos, finanzas o soporte con acciones de consecuencia',
    metric: 'blocked unsafe actions, task success seguro y auditabilidad',
    labName: links.anthropicAgents.nombre,
    labUrl: links.anthropicAgents.url,
    secondLabName: links.nist.nombre,
    secondLabUrl: links.nist.url,
    capstoneStep: 'convertir capacidad en sistema gobernable',
    recognition: 'si una accion no se puede deshacer, pon humano/regla antes de ejecutar',
  },
  'gen-ma1': {
    concept: 'descomposicion multi-agente y patrones de colaboracion',
    system: 'asistente de investigacion con coordinador, investigador y sintetizador',
    build: 'comparar agente unico contra roles separados con el mismo presupuesto',
    evidenceShort: 'demostrar que multi-agente mejora calidad neta despues de costo y latencia',
    artifact: 'experimento con roles, trazas y comparacion contra baseline simple',
    baseline: 'un solo agente con prompt amplio',
    advanced: 'orquestador con especialistas y contrato de salida',
    failure: 'mas agentes aumentan costo sin mejorar task success',
    mistake: 'suponer que dividir en roles siempre mejora',
    transfer: 'equipos humanos: especializar solo cuando la coordinacion se paga',
    metric: 'task success, costo, latencia y errores por rol',
    labName: links.anthropicMulti.nombre,
    labUrl: links.anthropicMulti.url,
    secondLabName: links.autogen.nombre,
    secondLabUrl: links.autogen.url,
    capstoneStep: 'decidir si el proyecto final requiere un solo agente o varios',
    recognition: 'si la metrica no supera al baseline simple, no justifiques multi-agente',
  },
  'gen-ma2': {
    concept: 'orquestacion, routing dinamico y manejo de errores',
    system: 'grafo de agentes con router y recuperacion de fallos',
    build: 'implementar un router que elija especialista, limite pasos y maneje tool errors',
    evidenceShort: 'medir routing accuracy y degradacion ante herramienta caida',
    artifact: 'grafo de estado con casos de exito, fallo y recuperacion',
    baseline: 'conversacion libre entre agentes sin limites',
    advanced: 'orquestacion por grafo con contratos, timeouts y fallback',
    failure: 'los agentes entran en bucle o pasan errores sin verificar',
    mistake: 'confundir conversacion entre agentes con arquitectura controlada',
    transfer: 'sistemas de soporte con dominios, escalamiento y SLAs',
    metric: 'routing accuracy, loops evitados, latencia y fallback success',
    labName: links.langgraph.nombre,
    labUrl: links.langgraph.url,
    secondLabName: links.autogen.nombre,
    secondLabUrl: links.autogen.url,
    capstoneStep: 'hacer observable la coordinacion entre componentes',
    recognition: 'si no sabes quien decide el siguiente paso, falta orquestacion',
  },
  'gen-ma3': {
    concept: 'RAG adaptativo y agentes que deciden que recuperar',
    system: 'agente que decide si buscar, que buscar y cuando abstenerse',
    build: 'comparar always-retrieve contra retrieval condicional y reintentos guiados',
    evidenceShort: 'mostrar cuando recuperar ayuda, cuando mete ruido y cuando abstenerse',
    artifact: 'policy de retrieval con trazas, fuentes y evaluacion por consulta',
    baseline: 'siempre recuperar k documentos',
    advanced: 'RAG adaptativo con decision de query, k y re-ranking',
    failure: 'el agente recupera ruido y lo convierte en argumento final',
    mistake: 'creer que mas contexto siempre reduce alucinacion',
    transfer: 'asistentes expertos que alternan memoria interna, busqueda y herramientas',
    metric: 'decision accuracy de retrieval, faithfulness, costo y context precision',
    labName: links.ragas.nombre,
    labUrl: links.ragas.url,
    secondLabName: links.langgraph.nombre,
    secondLabUrl: links.langgraph.url,
    capstoneStep: 'unir recuperacion, agente y evaluacion en una politica medible',
    recognition: 'si el contexto recuperado contamina la respuesta, mide precision y decision de buscar',
  },
  'gen-ma4': {
    concept: 'evaluacion de sistemas de agentes por resultado y por componente',
    system: 'benchmark de sistema multi-agente con casos normales y adversarios',
    build: 'crear task suite, metricas por componente y red team de inyecciones',
    evidenceShort: 'localizar fallos por routing, tool accuracy, synthesis o seguridad',
    artifact: 'matriz de evaluacion end-to-end y por componente con red team',
    baseline: 'solo medir task success final',
    advanced: 'evaluacion jerarquica con trazas, ablations y held-out',
    failure: 'un 70% de exito no dice que pieza arreglar',
    mistake: 'tomar una demo exitosa como evaluacion del sistema',
    transfer: 'operacion de agentes en produccion con observabilidad real',
    metric: 'task success, tool accuracy, routing, costo, latencia y unsafe pass rate',
    labName: links.anthropicMulti.nombre,
    labUrl: links.anthropicMulti.url,
    secondLabName: links.openaiEvals.nombre,
    secondLabUrl: links.openaiEvals.url,
    capstoneStep: 'cerrar el proyecto con comparacion contra alternativas mas simples',
    recognition: 'si no localizas el eslabon fallido, tu evaluacion no es accionable',
  },
  'gen-resp1': {
    concept: 'IA responsable: precision no equivale a aceptabilidad',
    system: 'clasificador o asistente en dominio sensible',
    build: 'mapear stakeholders, danos, sesgos y decisiones humanas antes del despliegue',
    evidenceShort: 'separar metricas tecnicas de impactos, equidad y rendicion de cuentas',
    artifact: 'matriz de impacto con mitigaciones y decision de uso/no uso',
    baseline: 'lanzar por alta accuracy promedio',
    advanced: 'decision con grupos, danos, transparencia y humano responsable',
    failure: 'un modelo preciso causa dano por sesgo o uso inapropiado',
    mistake: 'tratar responsabilidad como seccion legal posterior',
    transfer: 'admisiones, credito, salud o RRHH donde el error tiene asimetria',
    metric: 'performance por segmento, harm review y trazabilidad de decisiones',
    labName: links.nist.nombre,
    labUrl: links.nist.url,
    secondLabName: links.mitRisk.nombre,
    secondLabUrl: links.mitRisk.url,
    capstoneStep: 'definir limites eticos y operativos del sistema final',
    recognition: 'si una salida afecta oportunidades o derechos, accuracy promedio no basta',
  },
  'gen-resp2': {
    concept: 'frameworks de riesgo: Govern, Map, Measure y Manage',
    system: 'registro de riesgos para una solucion GenAI',
    build: 'usar AI RMF y MIT AI Risk Repository para crear controles verificables',
    evidenceShort: 'vincular cada riesgo con dueno, metrica, control y umbral de escalacion',
    artifact: 'risk register con controles, evidencias y cadencia de revision',
    baseline: 'checklist informal sin duenos ni evidencias',
    advanced: 'gobierno operativo con medicion continua y responsables',
    failure: 'riesgos conocidos quedan sin dueno hasta que aparecen en produccion',
    mistake: 'confundir nombrar un riesgo con gestionarlo',
    transfer: 'comites de producto, seguridad y cumplimiento con lenguaje compartido',
    metric: 'riesgos con dueno, controles probados y incidentes detectados',
    labName: links.nist.nombre,
    labUrl: links.nist.url,
    secondLabName: links.mitRisk.nombre,
    secondLabUrl: links.mitRisk.url,
    capstoneStep: 'crear la capa de gobierno del proyecto final',
    recognition: 'si no hay dueno ni evidencia, el riesgo solo esta escrito',
  },
  'gen-resp3': {
    concept: 'GenAI en produccion: costo, latencia, observabilidad y deriva',
    system: 'servicio GenAI desplegado con usuarios reales',
    build: 'disenar monitoreo de costo, latencia, errores, drift y evaluacion continua',
    evidenceShort: 'detectar regresiones ante cambio de modelo, prompt, corpus o patron de uso',
    artifact: 'runbook de produccion con SLOs, metricas y rollback',
    baseline: 'demo notebook sin telemetria ni versionado',
    advanced: 'servicio con SLOs, logs, evaluacion continua y version pinning',
    failure: 'un cambio de proveedor degrada respuestas sin que el equipo lo note',
    mistake: 'pensar que pasar el benchmark una vez basta',
    transfer: 'operar cualquier producto ML/LLM que cambia con datos y proveedores',
    metric: 'costo por tarea, p95 latencia, error rate, drift y eval score continuo',
    labName: links.openaiEvals.nombre,
    labUrl: links.openaiEvals.url,
    secondLabName: links.promptfoo.nombre,
    secondLabUrl: links.promptfoo.url,
    capstoneStep: 'hacer desplegable y mantenible el proyecto final',
    recognition: 'si modelo, prompt o corpus cambian, re-evalua antes de confiar',
  },
  'gen-resp4': {
    concept: 'seleccion de arquitectura GenAI por vertical y metrica',
    system: 'caso de negocio con clasificacion, RAG, agente o multi-agente',
    build: 'elegir la pieza mas simple que resuelva y justificarla con evaluacion',
    evidenceShort: 'comparar alternativas y explicar por que la complejidad se paga o se descarta',
    artifact: 'proyecto final: arquitectura, evaluacion, riesgo, costos y plan de produccion',
    baseline: 'usar la arquitectura mas sofisticada por moda',
    advanced: 'solucion minima viable, evaluable y responsable',
    failure: 'multi-agente impresiona en demo pero pierde en costo, riesgo o fiabilidad',
    mistake: 'confundir capacidad del modelo con valor de negocio medido',
    transfer: 'seguros, finanzas, legal, supply chain o educacion',
    metric: 'metrica de negocio, calidad, seguridad, costo y riesgo residual',
    labName: links.deeplearning.nombre,
    labUrl: links.deeplearning.url,
    secondLabName: links.nist.nombre,
    secondLabUrl: links.nist.url,
    capstoneStep: 'presentar el diseno final como si fuera revisado por producto, ML y riesgo',
    recognition: 'si una solucion simple logra la metrica, la complejidad extra debe justificarse',
  },
};

const unidadesDoc = JSON.parse(readFileSync(unidadesPath, 'utf8'));
const taxDoc = JSON.parse(readFileSync(taxonomiaPath, 'utf8'));

const clusterByUnit = new Map();
for (const cluster of taxDoc.clusters ?? []) {
  for (const unitId of cluster.unidades ?? []) clusterByUnit.set(unitId, cluster);
}

for (const cluster of taxDoc.clusters ?? []) enrichCluster(cluster);
for (const unit of unidadesDoc.unidades ?? []) enrichUnit(unit);

writeFileSync(unidadesPath, `${JSON.stringify(unidadesDoc, null, 2)}\n`, 'utf8');
writeFileSync(taxonomiaPath, `${JSON.stringify(taxDoc, null, 2)}\n`, 'utf8');

let theoryBlocks = 0;
for (const unit of unidadesDoc.unidades ?? []) {
  const bp = getBlueprint(unit);
  const filePath = join(ROOT, unit.lectura);
  if (!existsSync(filePath)) continue;
  const before = readFileSync(filePath, 'utf8');
  const after = upsertAssignmentBlock(before, unit, bp, clusterByUnit.get(unit.id));
  if (after !== before) {
    writeFileSync(filePath, after, 'utf8');
    theoryBlocks += 1;
  }
}

const totalQuestions = unidadesDoc.unidades.reduce((acc, u) => acc + (u.banco?.length ?? 0), 0);
console.log(
  `OK: fase-9 enriquecida. unidades=${unidadesDoc.unidades.length} preguntas=${totalQuestions} bloques_teoria_actualizados=${theoryBlocks}`
);

function enrichCluster(cluster) {
  const profile = clusterProfiles[cluster.id];
  if (!profile) return;
  cluster.laboratoriosVivos = mergeLabs(cluster.laboratoriosVivos ?? [], profile.labs.map((lab) => polishDeep({
    nombre: lab.nombre,
    url: lab.url,
    objetivo: labObjective(cluster.id, lab.nombre),
    criterio_cierre: labClosure(cluster.id),
    safety_note: 'Material educativo; ejecuta codigo solo en tu entorno y evita subir datos o secretos reales.',
  })));
  cluster.estandar_transferencia = polishDeep({
    revision: MARKER,
    fecha: REVIEW_DATE,
    prioridad: profile.priority,
    estilo_asignacion: profile.gradedStyle,
    proyecto_cluster: profile.capstone,
    contrato_calidad: [
      'Cada unidad debe cerrar con evidencia ejecutable o verificable, no solo lectura.',
      'Toda mejora debe compararse contra una linea base y un set held-out cuando aplique.',
      'Los errores se diagnostican por componente para que el alumno sepa que corregir.',
      'Los entregables deben ser portafolio: notebook, harness, reporte, rubrica o diseno auditable.',
    ],
  });
  cluster.asignacionesTransferencia = polishDeep(buildClusterAssignments(cluster, profile));
  cluster.miniProyecto = polishDeep(enrichMiniProject(cluster.miniProyecto, profile));
}

function enrichUnit(unit) {
  const cluster = clusterByUnit.get(unit.id);
  const profile = clusterProfiles[cluster?.id];
  const bp = getBlueprint(unit);
  unit.metadata = {
    ...(unit.metadata ?? {}),
    revision_pedagogica: MARKER,
    revision_fecha: REVIEW_DATE,
    nivel: unit.metadata?.nivel ?? 3,
    evaluacion_minima: {
      easy: 10,
      medium: 10,
      hard: 10,
      scenario: 5,
      reflexion: 5,
    },
  };
  unit.asignacion_practica = polishDeep({
    tipo: 'graded_assignment',
    estilo: profile?.gradedStyle ?? 'asignacion graduada con baseline, metrica y rubrica',
    implementacion: bp.build,
    laboratorio_externo: {
      nombre: bp.labName,
      url: bp.labUrl,
      alternativa: {
        nombre: bp.secondLabName,
        url: bp.secondLabUrl,
      },
    },
    evaluacion: bp.metric,
    evidencia_cierre: bp.evidenceShort,
    entregable: bp.artifact,
    transferencia: bp.transfer,
    capstone: bp.capstoneStep,
    rubrica: [
      'Correctitud tecnica: implementacion o diseno coherente con la leccion.',
      'Pruebas: baseline, ablation o casos adversarios con evidencia.',
      'Transferencia: explicita donde reaparece la misma estructura en otro dominio.',
      'Error analysis: nombra el fallo dominante y la siguiente accion.',
      'Comunicacion: reporte breve, reproducible y auditable.',
    ],
  });
  unit.mini_entregable = polishText(`Entrega ${bp.artifact}. Debe incluir linea base (${bp.baseline}), version mejorada (${bp.advanced}), metrica (${bp.metric}) y analisis del fallo: ${bp.failure}.`);
  unit.referencias_transferencia = [
    { nombre: bp.labName, url: bp.labUrl },
    { nombre: bp.secondLabName, url: bp.secondLabUrl },
  ];
  unit.banco = expandBank(unit, bp, cluster).map((q) => polishDeep(q));
}

function expandBank(unit, bp, cluster) {
  const preserved = (unit.banco ?? []).filter((q) => q?.metadata?.generated_by !== MARKER);
  const normalized = preserved.map((q, index) => normalizeQuestion(q, unit, bp, cluster, index));

  const generated = [];
  const counts = countByKind(normalized);
  for (const difficulty of ['easy', 'medium', 'hard']) {
    let count = counts.concept[difficulty] ?? 0;
    let idx = 1;
    while (count < 10) {
      generated.push(makeConceptQuestion(unit, bp, cluster, difficulty, idx));
      count += 1;
      idx += 1;
    }
  }
  let scenarioCount = counts.scenario;
  let scenarioIdx = 1;
  while (scenarioCount < 5) {
    generated.push(makeScenarioQuestion(unit, bp, cluster, scenarioIdx));
    scenarioCount += 1;
    scenarioIdx += 1;
  }
  let reflectionCount = counts.reflexion;
  let reflectionIdx = 1;
  while (reflectionCount < 5) {
    generated.push(makeReflectionQuestion(unit, bp, cluster, reflectionIdx));
    reflectionCount += 1;
    reflectionIdx += 1;
  }
  return [...normalized, ...generated];
}

function normalizeQuestion(q, unit, bp, cluster, index) {
  const tipo = q.tipo ?? inferTipo(q);
  const type = q.type ?? typeFromTipo(tipo);
  const prompt = q.prompt ?? q.enunciado ?? '';
  const solucion = q.solucion ?? q.answer ?? q.feedback ?? '';
  const answer = q.answer ?? solucion;
  const difficulty = q.difficulty ?? 'medium';
  const feedback = q.feedback ?? q.explicacion ?? buildFeedback(bp, difficulty);
  const normalized = {
    ...q,
    id: q.id ?? `${unit.id}-manual-${index + 1}`,
    tipo,
    type,
    enunciado: q.enunciado ?? prompt,
    prompt,
    solucion,
    answer,
    explicacion: q.explicacion ?? feedback,
    feedback,
    difficulty,
    concept: q.concept ?? bp.concept,
    source_reference: q.source_reference ?? sourceReference(unit, bp, cluster),
    common_mistake: q.common_mistake ?? bp.mistake,
    recognition_signal: q.recognition_signal ?? bp.recognition,
  };
  if (tipo === 'concepto') {
    normalized.options = normalizeOptions(q.options, normalized.answer, bp);
    if (!normalized.options.includes(normalized.answer)) normalized.answer = normalized.options[0];
  } else {
    delete normalized.options;
  }
  return normalized;
}

function inferTipo(q) {
  if (Array.isArray(q.options)) return 'concepto';
  if ((q.id ?? '').includes('-s')) return 'scenario';
  if ((q.id ?? '').includes('-r')) return 'reflexion';
  return 'reflexion';
}

function typeFromTipo(tipo) {
  if (tipo === 'concepto') return 'quiz';
  if (tipo === 'scenario') return 'scenario';
  return 'reflection';
}

function normalizeOptions(options, answer, bp) {
  if (Array.isArray(options) && options.length === 4 && options.includes(answer)) return options;
  const correct = answer || bp.evidenceShort;
  return [
    correct,
    `Usar ${bp.baseline} sin comparar contra evidencia nueva.`,
    'Cambiar varias piezas a la vez y quedarse con la demo mas convincente.',
    `Ignorar ${bp.failure} porque el resultado promedio parece aceptable.`,
  ];
}

function countByKind(questions) {
  const concept = { easy: 0, medium: 0, hard: 0 };
  let scenario = 0;
  let reflexion = 0;
  for (const q of questions) {
    if (q.tipo === 'concepto') concept[q.difficulty] = (concept[q.difficulty] ?? 0) + 1;
    else if (q.tipo === 'scenario') scenario += 1;
    else if (q.tipo === 'reflexion') reflexion += 1;
  }
  return { concept, scenario, reflexion };
}

function makeConceptQuestion(unit, bp, cluster, difficulty, idx) {
  const templates = {
    easy: [
      {
        q: `En la practica de ${unit.titulo}, ¿que evidencia minima evita que ${bp.build} sea solo una demo?`,
        a: bp.evidenceShort,
        d: [`Leer ${bp.labName} y escribir un resumen.`, `Elegir ${bp.advanced} sin linea base.`, 'Aceptar una salida plausible sin medirla.'],
        f: `La evidencia debe observar el mecanismo central: ${bp.concept}.`,
      },
      {
        q: `Tu baseline es "${bp.baseline}" y la version nueva es "${bp.advanced}". ¿Que comparacion es la correcta?`,
        a: 'Misma tarea, mismos datos, una variable cambiada y metrica antes/despues.',
        d: ['Cambiar datos, prompt y modelo a la vez para acelerar.', 'Comparar contra una demo antigua sin set fijo.', 'Usar solo intuicion si la salida suena mejor.'],
        f: 'La transferencia exige aislar la causa del cambio, no impresiones.',
      },
      {
        q: `¿Que senal temprana te haria sospechar el fallo "${bp.failure}"?`,
        a: bp.recognition,
        d: ['El reporte tiene mas secciones que el anterior.', `El alumno uso ${bp.labName} como referencia.`, 'El sistema tarda menos en un caso feliz.'],
        f: `La senal apunta al mecanismo que la leccion intenta volver reconocible: ${bp.concept}.`,
      },
      {
        q: `¿Por que la transferencia "${bp.transfer}" pertenece a esta unidad?`,
        a: `Porque reutiliza la misma estructura profunda: ${bp.concept}.`,
        d: ['Porque usa exactamente la misma libreria.', 'Porque evita cualquier necesidad de evaluar.', 'Porque reemplaza el aprendizaje por una analogia superficial.'],
        f: 'Transferir no es copiar herramientas; es reconocer la misma estructura bajo otro contexto.',
      },
      {
        q: `Si solo puedes entregar una pieza de portafolio de esta unidad, ¿cual demuestra mejor dominio?`,
        a: bp.artifact,
        d: ['Una lista de definiciones copiadas de la leccion.', 'Una captura de una respuesta correcta del modelo.', 'Un prompt largo sin baseline ni metrica.'],
        f: 'Un entregable fuerte combina construccion, evidencia y explicacion del fallo.',
      },
      {
        q: `¿Que rol cumple el laboratorio externo ${bp.labName} en esta unidad?`,
        a: 'Dar una practica ejecutable cuando el laboratorio completo excede el espacio interno.',
        d: ['Sustituir la evaluacion local por lectura pasiva.', 'Permitir omitir el banco de preguntas.', 'Reemplazar las referencias de la leccion por autoridad externa.'],
        f: 'El enlace externo amplifica la practica, pero la evidencia de aprendizaje sigue siendo local.',
      },
      {
        q: `Antes de optimizar ${bp.system}, ¿que debes fijar?`,
        a: `Una linea base (${bp.baseline}) y una metrica: ${bp.metric}.`,
        d: ['El modelo mas grande disponible.', 'El prompt mas detallado posible.', 'Un ejemplo facil donde la demo ya funciona.'],
        f: 'Sin baseline y metrica, no hay aprendizaje medible.',
      },
      {
        q: `¿Cual es el error comun que esta unidad busca eliminar?`,
        a: bp.mistake,
        d: ['Documentar demasiado el resultado final.', 'Usar nombres tecnicos en el reporte.', 'Probar con un conjunto de validacion.'],
        f: `El distractor importante es una confusion real sobre ${bp.concept}.`,
      },
      {
        q: `¿Que hace que el mini-entregable sea "graduado" y no solo practica libre?`,
        a: 'Tiene criterio de cierre, rubrica, baseline y evidencia verificable.',
        d: ['Tiene muchas paginas de explicacion.', 'Permite cualquier respuesta si el alumno reflexiona.', 'Evita comparar contra una alternativa simple.'],
        f: 'La calificacion debe poder distinguir comprension transferible de actividad superficial.',
      },
      {
        q: `En una revision rapida, ¿que frase indicaria que el alumno entendio ${bp.concept}?`,
        a: `Puedo explicar cuando falla ${bp.baseline} y por que ${bp.advanced} lo corrige.`,
        d: [`${bp.advanced} es mejor porque es mas moderno.`, 'El resultado es correcto porque el modelo suena seguro.', 'La teoria importa menos si el notebook corre.'],
        f: 'El dominio aparece cuando se nombra el mecanismo, el fallo y la evidencia.',
      },
    ],
    medium: [
      {
        q: `Implementaste ${bp.advanced}, pero la metrica promedio sube poco. ¿Que decision es mas rigurosa?`,
        a: `Segmentar errores donde aparece "${bp.failure}" antes de cambiar otra pieza.`,
        d: ['Subir complejidad de inmediato para superar la media.', 'Eliminar casos dificiles para estabilizar el benchmark.', 'Conservar la version nueva porque es tecnicamente mas avanzada.'],
        f: 'La media puede ocultar el mecanismo que la unidad intenta entrenar.',
      },
      {
        q: `Un companero propone saltarse ${bp.baseline}. ¿Cual es la objecion tecnica mas fuerte?`,
        a: 'Sin baseline no sabes si la complejidad nueva produjo mejora real.',
        d: ['El baseline siempre sera mas caro.', 'Los baselines solo aplican a investigacion academica.', 'Una arquitectura moderna no necesita comparacion.'],
        f: 'El baseline es el control experimental de la ingenieria aplicada.',
      },
      {
        q: `¿Que evaluacion distingue mejor "${bp.mistake}" de dominio real?`,
        a: `Un caso donde ${bp.failure} fuerza a explicar el mecanismo y la correccion.`,
        d: ['Una pregunta de definicion sin contexto.', 'Un resumen de la lectura en cinco bullets.', 'Un ejemplo feliz elegido por el alumno.'],
        f: 'Una buena pregunta pone presion sobre el supuesto equivocado.',
      },
      {
        q: `Quieres transferir la idea a "${bp.transfer}". ¿Que debes conservar y que puedes cambiar?`,
        a: `Conservar ${bp.concept}; cambiar herramientas, datos y escala del dominio.`,
        d: ['Conservar la libreria exacta y cambiar la metrica.', 'Conservar solo el vocabulario y omitir el mecanismo.', 'Cambiar todo y confiar en que la analogia sea intuitiva.'],
        f: 'La transferencia conserva estructura causal, no superficie.',
      },
      {
        q: `El entregable ${bp.artifact} pasa casos faciles pero falla en held-out. ¿Que conclusion es correcta?`,
        a: 'El aprendizaje no generalizo; hay que analizar segmentos y revisar supuestos.',
        d: ['La metrica held-out debe ignorarse si la demo funciona.', 'El fallo prueba que la unidad no aplica.', 'Basta con aumentar la longitud del reporte.'],
        f: 'Held-out protege contra memorizar ejemplos o sobreajustar decisiones.',
      },
      {
        q: `¿Que ablation haria mas visible el valor de ${bp.advanced}?`,
        a: `Compararlo contra ${bp.baseline} manteniendo datos, tarea y metrica constantes.`,
        d: ['Cambiar corpus y arquitectura al mismo tiempo.', 'Eliminar los casos donde falla el baseline.', 'Medir solo latencia aunque la unidad trate calidad.'],
        f: 'Una ablation util aísla el componente que afirma aportar valor.',
      },
      {
        q: `Si ${bp.system} funciona bien en casos felices, ¿por que aun necesitas ${bp.metric}?`,
        a: 'Porque la metrica revela regresiones, segmentos debiles y tradeoffs invisibles.',
        d: ['Porque toda metrica reemplaza revision humana.', 'Porque una metrica evita disenar casos adversarios.', 'Porque el promedio siempre captura los riesgos importantes.'],
        f: 'Medir no sustituye juicio, pero evita decidir por demos.',
      },
      {
        q: `¿Que distractor seria plausible para alguien que no domino esta unidad?`,
        a: bp.mistake,
        d: ['Pedir un baseline antes de optimizar.', 'Usar un set held-out para confirmar.', 'Reportar errores por componente.'],
        f: 'Los errores plausibles suenan razonables hasta que entiendes el mecanismo.',
      },
      {
        q: `El laboratorio externo es mas amplio que Cogito. ¿Como lo integras sin perder foco?`,
        a: 'Ejecutas solo el tramo ligado a esta lección y lo cierras con evidencia local.',
        d: ['Lo completas entero aunque no conecte con la unidad.', 'Lo sustituyes por lectura pasiva.', 'Copias resultados ajenos si el entorno no corre.'],
        f: 'El enlace externo debe aterrizar en un entregable verificable de esta leccion.',
      },
      {
        q: `¿Cual seria una decision de producto basada en evidencia para ${bp.system}?`,
        a: `Adoptar ${bp.advanced} solo si supera ${bp.baseline} en ${bp.metric}.`,
        d: [`Adoptar ${bp.advanced} porque suena mas actual.`, 'Lanzar sin medicion si un experto lo aprueba.', 'Evitar comparar porque los casos reales son variables.'],
        f: 'La metrica justifica la complejidad en contexto de producto.',
      },
    ],
    hard: [
      {
        q: `Tu mejora supera la metrica principal, pero aumenta el riesgo asociado a "${bp.failure}". ¿Que haria una revision de alto nivel?`,
        a: 'Exigir analisis por segmento, ablation y criterio de lanzamiento con tradeoff explicito.',
        d: ['Lanzar porque la metrica promedio subio.', 'Descartar toda metrica automatica.', 'Cambiar a la arquitectura mas grande sin diagnostico.'],
        f: 'La excelencia exige decidir con tradeoffs, no maximizar un proxy.',
      },
      {
        q: `¿Cual es el caso borde que mas probablemente romperia una solucion superficial de ${unit.titulo}?`,
        a: `Un caso donde ${bp.failure} aparece fuera de la distribucion facil.`,
        d: ['Un caso identico al ejemplo de la leccion.', 'Un input corto y limpio sin ambiguedad.', 'Una demo con respuesta esperada visible en el prompt.'],
        f: 'Los casos borde fuerzan a probar si la estructura realmente se aprendio.',
      },
      {
        q: `Si un alumno maximiza ${bp.metric} iterando sobre los mismos ejemplos, ¿que riesgo metodologico aparece?`,
        a: 'Overfitting al benchmark; hace falta held-out y error analysis independiente.',
        d: ['Underfitting por falta de complejidad.', 'Mejora causal garantizada por repeticion.', 'Eliminacion automatica de sesgos del juez.'],
        f: 'La evaluacion tambien puede sobreajustarse cuando se usa como objetivo repetido.',
      },
      {
        q: `¿Que pregunta de auditoria revelaria si ${bp.artifact} es transferible?`,
        a: '¿La misma estructura funciona en otro dominio sin copiar la herramienta exacta?',
        d: ['¿El reporte menciona suficientes nombres de papers?', '¿El notebook produce una salida visual atractiva?', '¿El alumno uso la libreria mas popular?'],
        f: 'Transferibilidad significa mover la estructura a un problema nuevo.',
      },
      {
        q: `Un equipo presenta ${bp.advanced} sin explicar donde falla ${bp.baseline}. ¿Que falta en su argumento?`,
        a: 'La necesidad causal de la complejidad: que problema especifico resuelve.',
        d: ['Mas referencias bibliograficas en formato APA.', 'Un logo o diagrama de arquitectura.', 'Un prompt mas largo para explicar la solucion.'],
        f: 'Sin problema causal, la arquitectura es decoracion.',
      },
      {
        q: `¿Que diseno de benchmark seria mas dificil de manipular para esta unidad?`,
        a: 'Casos normales, casos borde, held-out y metrica alineada con el fallo dominante.',
        d: ['Solo ejemplos donde la nueva tecnica brilla.', 'Un unico caso curado para demo ejecutiva.', 'Preguntas definicionales con respuesta literal.'],
        f: 'Un benchmark serio evita que la solucion gane por seleccionar ejemplos faciles.',
      },
      {
        q: `¿Como conectarias esta unidad con el proyecto final tipo GPT-2 o sistema GenAI completo?`,
        a: `Usaria ${bp.capstoneStep} y lo validaria con ${bp.metric}.`,
        d: ['La dejaria como teoria separada sin impacto en el proyecto.', 'La usaria solo para decorar el reporte final.', 'La reemplazaria por un modelo cerrado sin evaluacion.'],
        f: 'Cada unidad debe aportar una pieza verificable al sistema final.',
      },
      {
        q: `Si el costo o la latencia impiden usar ${bp.advanced}, ¿que alternativa mantiene rigor?`,
        a: `Volver a ${bp.baseline}, documentar el tradeoff y dejar evidencia de cuando escalar.`,
        d: ['Ocultar el costo porque la calidad subio.', 'Eliminar la evaluacion para acelerar.', 'Usar una demo pequena como prueba de produccion.'],
        f: 'Rigor no siempre significa mas complejidad; significa decision justificada.',
      },
      {
        q: `¿Que explicacion seria inaceptable en una defensa tecnica de esta unidad?`,
        a: `${bp.advanced} funciona porque es el enfoque moderno y el output parece correcto.`,
        d: [`${bp.advanced} corrige ${bp.failure} bajo ${bp.metric}.`, `La comparacion contra ${bp.baseline} muestra el tradeoff.`, `El error restante se concentra en casos fuera de ${bp.transfer}.`],
        f: 'Autoridad y apariencia no sustituyen mecanismo ni evaluacion.',
      },
      {
        q: `¿Que convierte ${bp.failure} en una oportunidad pedagogica de alto nivel?`,
        a: 'Obliga a nombrar el supuesto roto, medirlo y transferir la correccion a otro dominio.',
        d: ['Permite eliminar casos dificiles del curso.', 'Hace innecesaria la teoria porque el fallo es visible.', 'Demuestra que solo importa usar modelos mas grandes.'],
        f: 'Los fallos bien analizados fabrican aristas entre concepto, evidencia y transferencia.',
      },
    ],
  };

  const t = templates[difficulty][(idx - 1) % templates[difficulty].length];
  return makeMc({
    id: `${unit.id}-transfer-${difficulty}-${String(idx).padStart(2, '0')}`,
    unit,
    bp,
    cluster,
    difficulty,
    prompt: t.q,
    answer: t.a,
    distractors: t.d,
    feedback: t.f,
    commonMistake: bp.mistake,
  });
}

function makeMc({ id, unit, bp, cluster, difficulty, prompt, answer, distractors, feedback, commonMistake }) {
  const cleanAnswer = cleanOption(answer);
  const cleanOptions = [cleanAnswer, ...distractors.map(cleanOption)];
  return {
    id,
    tipo: 'concepto',
    type: 'quiz',
    enunciado: prompt,
    prompt,
    solucion: answer,
    answer: cleanAnswer,
    options: cleanOptions,
    explicacion: feedback,
    feedback,
    difficulty,
    concept: bp.concept,
    source_reference: sourceReference(unit, bp, cluster),
    common_mistake: commonMistake,
    recognition_signal: bp.recognition,
    metadata: {
      generated_by: MARKER,
      quality_contract: 'auditoria.md + PROMPT-EJECUTOR-CALIDAD-BANCO.md',
      revised_on: REVIEW_DATE,
    },
  };
}

function makeScenarioQuestion(unit, bp, cluster, idx) {
  const scenarios = [
    {
      prompt: `Escenario: eres responsable de ${bp.system}. En staging observas "${bp.failure}" justo antes del lanzamiento. El equipo propone pasar directo a ${bp.advanced}. ¿Que diagnostico, experimento minimo y decision tomas?`,
      solution: `Diagnostico: el sintoma apunta a ${bp.concept}, no a una mejora cosmetica. Experimento: comparar ${bp.baseline} contra ${bp.advanced} con los mismos datos, medir ${bp.metric} y revisar ejemplos fallidos. Decision: adoptar la version nueva solo si corrige el fallo dominante sin empeorar costo, seguridad o held-out; si no, documentar el tradeoff y mantener la solucion simple.`,
      feedback: 'El escenario evalua decision bajo presion: baseline, metrica, error analysis y criterio de lanzamiento.',
      difficulty: 'medium',
    },
    {
      prompt: `Escenario: un alumno entrega ${bp.artifact}, pero no incluye casos negativos ni explica por que ${bp.baseline} falla. ¿Como lo retroalimentas para que alcance nivel portafolio?`,
      solution: `Le pediria reconstruir el argumento: problema -> baseline -> fallo observable (${bp.failure}) -> version mejorada (${bp.advanced}) -> metrica (${bp.metric}) -> errores restantes. Sin ese hilo, el entregable muestra actividad, pero no dominio transferible.`,
      feedback: 'La respuesta fuerte convierte un artefacto en evidencia de aprendizaje.',
      difficulty: 'medium',
    },
    {
      prompt: `Escenario: quieres aplicar la idea de esta leccion a ${bp.transfer}. El dominio, datos y herramienta cambian. ¿Que conservas, que cambias y como sabes si la transferencia fue valida?`,
      solution: `Conservo la estructura ${bp.concept}; cambio herramienta, datos y escala. Valido con una linea base local, una metrica adecuada y casos donde el fallo ${bp.failure} podria reaparecer. La transferencia es valida si el mismo razonamiento predice donde falla la solucion simple y que evidencia lo corrige.`,
      feedback: 'No basta decir "tambien aplica"; hay que conservar estructura y reconstruir evidencia.',
      difficulty: 'hard',
    },
  ];
  const item = scenarios[(idx - 1) % scenarios.length];
  return makeOpenQuestion(unit, bp, cluster, {
    id: `${unit.id}-transfer-scenario-${String(idx).padStart(2, '0')}`,
    tipo: 'scenario',
    type: 'scenario',
    prompt: item.prompt,
    solution: item.solution,
    feedback: item.feedback,
    difficulty: item.difficulty,
  });
}

function makeReflectionQuestion(unit, bp, cluster, idx) {
  const reflections = [
    {
      prompt: `Reflexion: ¿que evidencia aceptarias como prueba honesta de que entiendes ${bp.concept}, y que evidencia rechazarias aunque se vea impresionante?`,
      solution: `Una buena respuesta acepta evidencia como ${bp.evidenceShort}, comparada contra ${bp.baseline}, y rechaza demos sin metrica, autoridad externa o outputs plausibles sin error analysis. Debe nombrar por que ${bp.failure} es el fallo que vuelve necesaria la idea.`,
      difficulty: 'medium',
    },
    {
      prompt: `Reflexion: imagina que debes explicar esta unidad a un equipo de producto que solo quiere resultados. ¿Como defenderias ${bp.advanced} sin vender complejidad innecesaria?`,
      solution: `La defensa debe partir del problema observable (${bp.failure}), no de la moda tecnica. Explicaria el baseline, la metrica (${bp.metric}), el costo y la condicion bajo la cual NO usaria ${bp.advanced}. Eso muestra criterio profesional.`,
      difficulty: 'hard',
    },
    {
      prompt: `Reflexion: ¿que habito de estudio te obliga a practicar esta unidad: construir desde cero, evaluar con held-out, analizar fallos, o transferir a otro dominio? Justifica con un ejemplo propio.`,
      solution: `Respuesta modelo: elegir un habito y conectarlo con la unidad. Por ejemplo, construir desde cero revela donde se rompe ${bp.concept}; evaluar con held-out evita autoengano; analizar fallos muestra ${bp.failure}; transferir a ${bp.transfer} prueba que la idea no quedo pegada al ejemplo.`,
      difficulty: 'medium',
    },
  ];
  const item = reflections[(idx - 1) % reflections.length];
  return makeOpenQuestion(unit, bp, cluster, {
    id: `${unit.id}-transfer-reflexion-${String(idx).padStart(2, '0')}`,
    tipo: 'reflexion',
    type: 'reflection',
    prompt: item.prompt,
    solution: item.solution,
    feedback: 'Reflexion evaluable: pide criterio, evidencia y transferencia, no opinion suelta.',
    difficulty: item.difficulty,
  });
}

function makeOpenQuestion(unit, bp, cluster, { id, tipo, type, prompt, solution, feedback, difficulty }) {
  return {
    id,
    tipo,
    type,
    enunciado: prompt,
    prompt,
    solucion: solution,
    answer: solution,
    explicacion: feedback,
    feedback,
    difficulty,
    concept: bp.concept,
    source_reference: sourceReference(unit, bp, cluster),
    common_mistake: bp.mistake,
    recognition_signal: bp.recognition,
    metadata: {
      generated_by: MARKER,
      quality_contract: 'auditoria.md + PROMPT-EJECUTOR-CALIDAD-BANCO.md',
      revised_on: REVIEW_DATE,
    },
  };
}

function sourceReference(unit, bp, cluster) {
  const clusterTitle = cluster?.titulo ?? 'Fase 9';
  return `${unit.lectura}; ${clusterTitle}; ${bp.labName}; ${bp.secondLabName}`;
}

function buildFeedback(bp, difficulty) {
  if (difficulty === 'hard') return `La clave es reconocer el supuesto roto: ${bp.failure}.`;
  return `La respuesta debe conectar ${bp.concept} con evidencia observable.`;
}

function getBlueprint(unit) {
  const bp = blueprints[unit.id];
  if (bp) return bp;
  return {
    concept: unit.ideas_clave?.[0] ?? unit.titulo,
    system: 'sistema GenAI de practica',
    build: `construir una practica aplicada de ${unit.titulo}`,
    evidenceShort: 'comparar baseline y mejora con metrica y casos de error',
    artifact: 'notebook o reporte con baseline, metrica y error analysis',
    baseline: 'solucion simple',
    advanced: 'solucion mejorada',
    failure: 'la solucion simple falla en casos no triviales',
    mistake: 'confundir demo con evaluacion',
    transfer: 'otro dominio con la misma estructura',
    metric: 'metrica de calidad, costo y robustez',
    labName: links.cs224n.nombre,
    labUrl: links.cs224n.url,
    secondLabName: links.deeplearning.nombre,
    secondLabUrl: links.deeplearning.url,
    capstoneStep: 'aportar una pieza verificable al proyecto final',
    recognition: 'si la demo no tiene baseline, todavia no sabes que aprendiste',
  };
}

function cleanOption(option) {
  const s = String(option).replace(/\s+/g, ' ').trim();
  if (s.length <= 170) return s;
  return `${s.slice(0, 167).trim()}...`;
}

function mergeLabs(existing, additions) {
  const byUrl = new Map();
  for (const lab of [...existing, ...additions]) {
    if (!lab?.url) continue;
    if (!byUrl.has(lab.url)) byUrl.set(lab.url, lab);
  }
  return [...byUrl.values()];
}

function labObjective(clusterId, labName) {
  const profile = clusterProfiles[clusterId];
  return `desarrollar ${profile?.priority ?? 'una practica aplicada'} usando ${labName} como laboratorio externo`;
}

function labClosure(clusterId) {
  const profile = clusterProfiles[clusterId];
  return `entregar evidencia local: baseline, metrica, error analysis y conexion con ${profile?.capstone ?? 'el proyecto de cluster'}`;
}

function buildClusterAssignments(cluster, profile) {
  return [
    {
      titulo: `Assignment 1 · ${profile.shorthand}: baseline y mecanismo`,
      objetivo: `Construir la version mas simple que haga visible ${profile.priority}.`,
      entregable: 'notebook o reporte reproducible con baseline, prueba minima y analisis de fallo.',
      criterio: 'La entrega debe explicar que supuesto rompe el baseline y que evidencia lo demuestra.',
    },
    {
      titulo: `Assignment 2 · ${profile.shorthand}: implementacion o evaluacion fuerte`,
      objetivo: `Elevar la solucion con ${profile.gradedStyle}.`,
      entregable: 'artefacto de portafolio con metricas, ablation y casos borde.',
      criterio: 'La mejora debe superar al baseline en una metrica alineada y no solo en una demo.',
    },
    {
      titulo: `Proyecto de cluster · ${profile.shorthand}`,
      objetivo: profile.capstone,
      entregable: 'informe tecnico breve con decisiones, tradeoffs, riesgos y proxima iteracion.',
      criterio: 'Debe ser transferible: otro equipo podria repetirlo y adaptar la estructura a un dominio nuevo.',
    },
  ];
}

function enrichMiniProject(project, profile) {
  const base = project ?? {};
  return {
    ...base,
    titulo: base.titulo ?? `Proyecto ${profile.shorthand}`,
    descripcion: `${base.descripcion ?? profile.capstone} Ademas, incorpora una linea base, un criterio de cierre, una comparacion contra alternativa simple y una seccion de error analysis que explique donde NO conviene usar la tecnica.`,
    entregable: `${base.entregable ?? 'Artefacto tecnico'} + evidencia de evaluacion, ablation y transferencia.`,
    rubrica: [
      ...(base.rubrica ?? []),
      'Incluye baseline y compara contra una alternativa mas simple.',
      'Usa metrica alineada con el fallo dominante, con held-out o casos adversarios.',
      'Explica transferencia: que estructura se conserva al cambiar de dominio.',
    ],
  };
}

function upsertAssignmentBlock(content, unit, bp, cluster) {
  const clusterProfile = clusterProfiles[cluster?.id];
  const block = buildAssignmentBlock(unit, bp, clusterProfile);
  const pattern = new RegExp(`${escapeRegExp(BLOCK_START)}[\\s\\S]*?${escapeRegExp(BLOCK_END)}`);
  if (pattern.test(content)) return content.replace(pattern, block);

  const synthesisIndex = content.indexOf('\n---\n\n> **Síntesis');
  if (synthesisIndex !== -1) {
    return `${content.slice(0, synthesisIndex).trimEnd()}\n\n${block}\n${content.slice(synthesisIndex)}`;
  }
  const referencesIndex = content.indexOf('\n**Referencias**');
  if (referencesIndex !== -1) {
    return `${content.slice(0, referencesIndex).trimEnd()}\n\n${block}\n${content.slice(referencesIndex)}`;
  }
  return `${content.trimEnd()}\n\n${block}\n`;
}

function buildAssignmentBlock(unit, bp, clusterProfile) {
  const routeLine = clusterProfile ? `**Ruta de cluster:** ${clusterProfile.capstone}.` : null;
  const block = [
    BLOCK_START,
    '## Asignación práctica de transferencia',
    '',
    `**Objetivo graduado:** convertir la idea central (${bp.concept}) en una evidencia que pueda revisarse como assignment de Stanford/DeepLearning.AI/Karpathy: implementacion o diseno, baseline, metrica, error analysis y transferencia.`,
    '',
    `1. **Implementacion o diseno:** ${bp.build}.`,
    `2. **Baseline obligatorio:** ${bp.baseline}.`,
    `3. **Version mejorada:** ${bp.advanced}.`,
    `4. **Evaluacion:** ${bp.metric}.`,
    `5. **Fallo que debes explicar:** ${bp.failure}.`,
    `6. **Transferencia:** ${bp.transfer}.`,
    '',
    `**Laboratorio externo principal:** [${bp.labName}](${bp.labUrl}).`,
    `**Laboratorio alternativo:** [${bp.secondLabName}](${bp.secondLabUrl}).`,
    routeLine,
    '',
    `**Entregable:** ${bp.artifact}. Debe incluir una conclusion breve: que aprendiste, que fallo, que mediste y que harias distinto si lo llevaras a produccion.`,
    '',
    '**Rubrica de excelencia:**',
    '',
    '- Correccion tecnica: la implementacion o el diseno corresponde a la leccion, no a una demo generica.',
    '- Evidencia: incluye baseline, metrica, casos borde y al menos una comparacion o ablation.',
    '- Transferencia: explica que estructura profunda se conserva al moverlo a otro dominio.',
    '- Error analysis: nombra el supuesto roto, el sintoma observable y la siguiente accion.',
    '- Comunicacion: cualquier revisor puede reproducir la decision sin confiar en autoridad externa.',
    BLOCK_END,
  ].filter((line) => line !== null).join('\n');
  return polishText(block);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function polishDeep(value, key = '') {
  const skip = new Set(['id', 'url', 'lectura', 'bloque', 'ruta', 'type', 'tipo', 'difficulty', 'generated_by', 'quality_contract', 'revised_on']);
  if (typeof value === 'string') return skip.has(key) ? value : polishText(value);
  if (Array.isArray(value)) return value.map((item) => polishDeep(item, key));
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([childKey, childValue]) => [childKey, polishDeep(childValue, childKey)]));
  }
  return value;
}

function polishText(value) {
  let out = String(value);
  const replacements = [
    [/\bimplementacion\b/g, 'implementación'],
    [/\bImplementacion\b/g, 'Implementación'],
    [/\bdisenar\b/g, 'diseñar'],
    [/\bDisenar\b/g, 'Diseñar'],
    [/\bdiseno\b/g, 'diseño'],
    [/\bDiseno\b/g, 'Diseño'],
    [/\bmetrica\b/g, 'métrica'],
    [/\bmetricas\b/g, 'métricas'],
    [/\bMetrica\b/g, 'Métrica'],
    [/\bMetricas\b/g, 'Métricas'],
    [/\bevaluacion\b/g, 'evaluación'],
    [/\bEvaluacion\b/g, 'Evaluación'],
    [/\banalisis\b/g, 'análisis'],
    [/\bAnalisis\b/g, 'Análisis'],
    [/\batencion\b/g, 'atención'],
    [/\bAtencion\b/g, 'Atención'],
    [/\bmascara\b/g, 'máscara'],
    [/\bMascara\b/g, 'Máscara'],
    [/\blinea\b/g, 'línea'],
    [/\bLinea\b/g, 'Línea'],
    [/\bversion\b/g, 'versión'],
    [/\bVersion\b/g, 'Versión'],
    [/\bcodigo\b/g, 'código'],
    [/\bCodigo\b/g, 'Código'],
    [/\btecnico\b/g, 'técnico'],
    [/\btecnica\b/g, 'técnica'],
    [/\bTecnico\b/g, 'Técnico'],
    [/\bTecnica\b/g, 'Técnica'],
    [/\bpractica\b/g, 'práctica'],
    [/\bPractica\b/g, 'Práctica'],
    [/\bpracticas\b/g, 'prácticas'],
    [/\bPracticas\b/g, 'Prácticas'],
    [/\bminima\b/g, 'mínima'],
    [/\bMinima\b/g, 'Mínima'],
    [/\bmaxima\b/g, 'máxima'],
    [/\bMaxima\b/g, 'Máxima'],
    [/\bsintoma\b/g, 'síntoma'],
    [/\bSintoma\b/g, 'Síntoma'],
    [/\baccion\b/g, 'acción'],
    [/\bAccion\b/g, 'Acción'],
    [/\bdecision\b/g, 'decisión'],
    [/\bDecision\b/g, 'Decisión'],
    [/\bconexion\b/g, 'conexión'],
    [/\bConexion\b/g, 'Conexión'],
    [/\bproduccion\b/g, 'producción'],
    [/\bProduccion\b/g, 'Producción'],
    [/\bgeneracion\b/g, 'generación'],
    [/\bGeneracion\b/g, 'Generación'],
    [/\brecuperacion\b/g, 'recuperación'],
    [/\bRecuperacion\b/g, 'Recuperación'],
    [/\bcomparacion\b/g, 'comparación'],
    [/\bComparacion\b/g, 'Comparación'],
    [/\bcalibracion\b/g, 'calibración'],
    [/\bCalibracion\b/g, 'Calibración'],
    [/\bsemantica\b/g, 'semántica'],
    [/\bsemanticas\b/g, 'semánticas'],
    [/\bSemantica\b/g, 'Semántica'],
    [/\bSemanticas\b/g, 'Semánticas'],
    [/\blexica\b/g, 'léxica'],
    [/\bLexica\b/g, 'Léxica'],
    [/\bunica\b/g, 'única'],
    [/\bUnica\b/g, 'Única'],
    [/\bautonoma\b/g, 'autónoma'],
    [/\bAutonoma\b/g, 'Autónoma'],
    [/\bpolitica\b/g, 'política'],
    [/\bPolitica\b/g, 'Política'],
    [/\bposicion\b/g, 'posición'],
    [/\bPosicion\b/g, 'Posición'],
    [/\bvision\b/g, 'visión'],
    [/\bVision\b/g, 'Visión'],
    [/\bextension\b/g, 'extensión'],
    [/\bExtension\b/g, 'Extensión'],
    [/\bimagenes\b/g, 'imágenes'],
    [/\bImagenes\b/g, 'Imágenes'],
    [/\bcritica\b/g, 'crítica'],
    [/\bCritica\b/g, 'Crítica'],
    [/\bcriticas\b/g, 'críticas'],
    [/\bCriticas\b/g, 'Críticas'],
    [/\brubrica\b/g, 'rúbrica'],
    [/\brubricas\b/g, 'rúbricas'],
    [/\bRubrica\b/g, 'Rúbrica'],
    [/\bRubricas\b/g, 'Rúbricas'],
    [/\bmodulo\b/g, 'módulo'],
    [/\bModulo\b/g, 'Módulo'],
    [/\bminimo\b/g, 'mínimo'],
    [/\bMinimo\b/g, 'Mínimo'],
    [/\bconclusion\b/g, 'conclusión'],
    [/\bConclusion\b/g, 'Conclusión'],
    [/\bcorreccion\b/g, 'corrección'],
    [/\bCorreccion\b/g, 'Corrección'],
    [/\bcomunicacion\b/g, 'comunicación'],
    [/\bComunicacion\b/g, 'Comunicación'],
    [/\bleccion\b/g, 'lección'],
    [/\bLeccion\b/g, 'Lección'],
    [/\bgenerica\b/g, 'genérica'],
    [/\bGenerica\b/g, 'Genérica'],
    [/\bgenerico\b/g, 'genérico'],
    [/\bGenerico\b/g, 'Genérico'],
    [/\bvalidacion\b/g, 'validación'],
    [/\bValidacion\b/g, 'Validación'],
    [/\boptimizacion\b/g, 'optimización'],
    [/\bOptimizacion\b/g, 'Optimización'],
    [/\biteracion\b/g, 'iteración'],
    [/\bIteracion\b/g, 'Iteración'],
    [/\bexplicita\b/g, 'explícita'],
    [/\bexplicito\b/g, 'explícito'],
    [/\bExplicita\b/g, 'Explícita'],
    [/\bExplicito\b/g, 'Explícito'],
    [/\bdecisiones\b/g, 'decisiones'],
    [/\bclasificacion\b/g, 'clasificación'],
    [/\bClasificacion\b/g, 'Clasificación'],
    [/\bextraccion\b/g, 'extracción'],
    [/\bExtraccion\b/g, 'Extracción'],
    [/\btraduccion\b/g, 'traducción'],
    [/\bTraduccion\b/g, 'Traducción'],
    [/\bdinamico\b/g, 'dinámico'],
    [/\bDinamico\b/g, 'Dinámico'],
    [/\blimites\b/g, 'límites'],
    [/\bLimites\b/g, 'Límites'],
    [/\bejecucion\b/g, 'ejecución'],
    [/\bEjecucion\b/g, 'Ejecución'],
    [/\bcolaboracion\b/g, 'colaboración'],
    [/\bColaboracion\b/g, 'Colaboración'],
    [/\bcoordinacion\b/g, 'coordinación'],
    [/\bCoordinacion\b/g, 'Coordinación'],
    [/\boperacion\b/g, 'operación'],
    [/\bOperacion\b/g, 'Operación'],
    [/\bprecision\b/g, 'precisión'],
    [/\bPrecision\b/g, 'Precisión'],
    [/\bcredito\b/g, 'crédito'],
    [/\bCredito\b/g, 'Crédito'],
    [/\basimetria\b/g, 'asimetría'],
    [/\bAsimetria\b/g, 'Asimetría'],
    [/\bcomites\b/g, 'comités'],
    [/\bComites\b/g, 'Comités'],
    [/\bbusqueda\b/g, 'búsqueda'],
    [/\bBusqueda\b/g, 'Búsqueda'],
    [/\bmedicas\b/g, 'médicas'],
    [/\bMedicas\b/g, 'Médicas'],
    [/\balucinacion\b/g, 'alucinación'],
    [/\bAlucinacion\b/g, 'Alucinación'],
    [/\bafirmacion\b/g, 'afirmación'],
    [/\bAfirmacion\b/g, 'Afirmación'],
    [/\bauditoria\b/g, 'auditoría'],
    [/\bAuditoria\b/g, 'Auditoría'],
    [/\brevision\b/g, 'revisión'],
    [/\bRevision\b/g, 'Revisión'],
    [/\bharia\b/g, 'haría'],
    [/\bHaria\b/g, 'Haría'],
    [/\bharias\b/g, 'harías'],
    [/\bHarias\b/g, 'Harías'],
    [/\bcaida\b/g, 'caída'],
    [/\bCaida\b/g, 'Caída'],
    [/\bautocritica\b/g, 'autocrítica'],
    [/\bAutocritica\b/g, 'Autocrítica'],
    [/\beconomica\b/g, 'económica'],
    [/\bEconomica\b/g, 'Económica'],
    [/\btipica\b/g, 'típica'],
    [/\bTipica\b/g, 'Típica'],
    [/\btambien\b/g, 'también'],
    [/\bTambien\b/g, 'También'],
    [/\bfuncion\b/g, 'función'],
    [/\bFuncion\b/g, 'Función'],
    [/\bambiguedad\b/g, 'ambigüedad'],
    [/\bAmbiguedad\b/g, 'Ambigüedad'],
    [/\bguia\b/g, 'guía'],
    [/\bGuia\b/g, 'Guía'],
    [/\butil\b/g, 'útil'],
    [/\bUtil\b/g, 'Útil'],
    [/\bmas\b/g, 'más'],
    [/¿Que/g, '¿Qué'],
    [/¿que/g, '¿qué'],
    [/¿Cual/g, '¿Cuál'],
    [/¿cual/g, '¿cuál'],
    [/¿Como/g, '¿Cómo'],
    [/¿como/g, '¿cómo'],
    [/¿Por que/g, '¿Por qué'],
    [/¿por que/g, '¿por qué'],
    [/explica que estructura/g, 'explica qué estructura'],
    [/sabes si la transferencia/g, 'sabes si la transferencia'],
    [/ que aprendiste/g, ' qué aprendiste'],
    [/ que fallo/g, ' qué falló'],
    [/ que mediste/g, ' qué mediste'],
    [/ que harías/g, ' qué harías'],
    [/ que harias/g, ' qué harías'],
    [/alumno uso/g, 'alumno usó'],
  ];
  for (const [from, to] of replacements) out = out.replace(from, to);
  return out;
}
