import { readFileSync, writeFileSync } from 'node:fs';

const path = 'data/genai/_unidades.json';
const doc = JSON.parse(readFileSync(path, 'utf8'));

const additions = {
  'gen-ma1': [
    mc('gma1-q5', 'easy', '¿Qué problema de un agente único ataca directamente la división en agentes especializados?',
      'La saturación de contexto y mezcla de responsabilidades en una tarea grande.',
      ['La saturación de contexto y mezcla de responsabilidades en una tarea grande.', 'La imposibilidad de usar herramientas en sistemas LLM.', 'La necesidad de eliminar toda coordinación entre pasos.', 'La falta de tokens especiales para marcar observaciones.'],
      'Distingue especialización real de multiplicar agentes sin motivo.', 'Creer que varios agentes mejoran cualquier tarea automáticamente.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si un rol no necesita todo el contexto, separarlo puede limpiar el razonamiento.'),
    mc('gma1-q6', 'medium', '¿Qué patrón encaja con “investigadores paralelos, sintetizador y revisor”?',
      'Orquestador-trabajadores con integración posterior de resultados.',
      ['Orquestador-trabajadores con integración posterior de resultados.', 'Q-learning tabular con política greedy.', 'RAG fijo de una sola búsqueda sin routing.', 'Fine-tuning supervisado sobre una respuesta dorada.'],
      'Reconoce el patrón dominante de colaboración.', 'Llamar debate a cualquier reparto de sub-tareas.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si alguien reparte trabajo y luego junta salidas, piensa orquestador-trabajadores.'),
    mc('gma1-q7', 'medium', '¿Qué condición hace valioso el patrón de debate entre agentes?',
      'Perspectivas suficientemente independientes que detectan errores distintos.',
      ['Perspectivas suficientemente independientes que detectan errores distintos.', 'Agentes idénticos con el mismo prompt y el mismo contexto.', 'Una única métrica ROUGE para escoger ganador.', 'Ausencia total de criterio de selección final.'],
      'Evalúa diversidad útil, no solo cantidad de voces.', 'Usar copias del mismo agente y esperar revisión independiente.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si todos comparten el mismo punto ciego, el debate no corrige mucho.'),
    mc('gma1-q8', 'hard', '¿Cuál es el costo oculto de pasar de un agente a muchos?',
      'Coordinación, latencia, cómputo y nuevas fronteras de confianza.',
      ['Coordinación, latencia, cómputo y nuevas fronteras de confianza.', 'Eliminación completa de prompt injection y errores compartidos.', 'Reducción garantizada de llamadas al modelo.', 'Imposibilidad de evaluar cada componente por separado.'],
      'Recupera el tradeoff central de multi-agente.', 'Contar solo ventajas de paralelismo y olvidar coordinación.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si agregas nodos, agregas mensajes, costos y superficies de fallo.'),
    mc('gma1-q9', 'hard', '¿Qué significa que la descomposición debe ser MECE en multi-agente?',
      'Sub-tareas sin solapes importantes y sin huecos de cobertura.',
      ['Sub-tareas sin solapes importantes y sin huecos de cobertura.', 'Todos los agentes reciben exactamente el mismo objetivo y contexto.', 'El orquestador evita revisar resultados para no sesgar.', 'Cada agente puede delegar sin límite a cualquier otro.'],
      'Evalúa calidad de descomposición, no solo número de agentes.', 'Dividir mal y producir redundancias o faltantes.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si dos agentes hacen lo mismo o nadie cubre algo, la división falló.'),
    mc('gma1-q10', 'medium', '¿Qué analogía técnica explica mejor orquestador-trabajadores?',
      'Map-reduce: repartir trabajo, procesar en paralelo e integrar resultados.',
      ['Map-reduce: repartir trabajo, procesar en paralelo e integrar resultados.', 'Softmax: convertir logits en probabilidades token a token.', 'BLEU: contar n-gramas compartidos con una referencia.', 'Backpropagation: propagar gradientes por una red neuronal.'],
      'Conecta el patrón de colaboración con sistemas conocidos.', 'Pensar en multi-agente como charla libre sin integración.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si puedes mapear subproblemas y reducir resultados, el patrón es natural.'),
    mc('gma1-q11', 'hard', '¿Qué riesgo de seguridad aumenta cuando agentes se pasan mensajes entre sí?',
      'Una inyección o error puede propagarse como contenido confiado entre fronteras.',
      ['Una inyección o error puede propagarse como contenido confiado entre fronteras.', 'Cada agente queda automáticamente aislado de datos no confiables.', 'Los mensajes internos dejan de necesitar validación.', 'El sistema ya no requiere permisos mínimos por herramienta.'],
      'Reconoce propagación de inyecciones como riesgo nuevo.', 'Tratar mensajes internos como seguros por estar dentro del sistema.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Cada salto agente-agente es una frontera de confianza que debe validarse.'),
    mc('gma1-q12', 'medium', '¿Cuándo NO se justifica un sistema multi-agente?',
      'Cuando la tarea es simple, de un paso o resuelta por workflow fijo más barato.',
      ['Cuando la tarea es simple, de un paso o resuelta por workflow fijo más barato.', 'Cuando hay sub-tareas paralelas con fuentes independientes.', 'Cuando el contexto de un agente único se satura claramente.', 'Cuando se requiere revisión independiente de resultados complejos.'],
      'Aplica el contraejemplo de sobreingeniería.', 'Usar multi-agente como señal de sofisticación sin necesidad real.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si el baseline simple gana en calidad/costo, multi-agente no se sostiene.'),
    open('gma1-s3', 'scenario', 'hard', 'Escenario: tu sistema de informe de mercado produce secciones redundantes y omite competidores clave. ¿Dónde mirarías primero?',
      'Miraría la descomposición del orquestador: sub-preguntas solapadas, huecos MECE y criterios de integración. Después mediría calidad por investigador y síntesis, pero el síntoma apunta a routing/planificación del coordinador.',
      'Diagnostica redundancia y huecos como fallo de orquestación.', 'Culpar solo al sintetizador sin revisar cómo se dividió la tarea.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si el trabajo llega duplicado o incompleto, audita primero la división.'),
    open('gma1-s4', 'scenario', 'medium', 'Escenario: quieres mejorar factualidad mediante debate, pero todos los agentes usan el mismo prompt, modelo y evidencia. ¿Qué cambiarías?',
      'Aumentaría independencia: roles distintos, evidencia separada, criterios explícitos, quizá modelos o temperaturas diferentes y un juez que compare argumentos con fuentes. Sin diversidad, el debate replica el mismo punto ciego.',
      'Diseña debate como revisión independiente, no repetición.', 'Multiplicar copias idénticas y llamar eso revisión por pares.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si quieres detectar errores, crea diferencias reales entre revisores.'),
    open('gma1-r3', 'reflexion', 'medium', 'Elige un proyecto grande. ¿Qué roles separarías y qué información NO debería ver cada rol?',
      'Una buena respuesta define roles por responsabilidad, limita contexto por necesidad y explica qué datos excluir para reducir ruido o riesgo. También debe nombrar dónde se integra y quién valida el resultado final.',
      'Reflexión sobre especialización y contexto mínimo.', 'Separar roles pero dar a todos todo el contexto y permisos.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si un rol no necesita un dato para decidir, excluirlo puede mejorar calidad y seguridad.'),
    open('gma1-r4', 'reflexion', 'hard', '¿Qué métrica usarías para decidir si dividir en agentes valió el costo?',
      'Debe comparar contra un agente único: task success, calidad por rúbrica, costo, latencia, tasa de errores y robustez. La respuesta fuerte define un umbral: multi-agente solo queda si mejora lo importante sin daño inaceptable.',
      'Reflexión sobre complejidad justificada por evidencia.', 'Aceptar más complejidad porque la arquitectura parece avanzada.', 'sistemas multi-agente, roles, patrones y fronteras de confianza', 'data/teoria/gen-ma1.md; Sistemas multi-agente: por qué y cuándo varios agentes', 'Si no supera al baseline simple en métricas relevantes, no está justificado.'),
  ],

  'gen-ma2': [
    mc('gma2-q5', 'easy', '¿Qué pregunta responde un router en un sistema multi-agente?',
      'Qué agente o herramienta debe atender una entrada o sub-tarea.',
      ['Qué agente o herramienta debe atender una entrada o sub-tarea.', 'Qué token será el próximo en la distribución del LLM.', 'Qué documento debe convertirse en embedding permanente.', 'Qué recompensa humana se usará para PPO.'],
      'Recupera la función central del routing.', 'Confundir routing con generación final.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si hay varios especialistas, alguien debe decidir a cuál enviar cada caso.'),
    mc('gma2-q6', 'medium', '¿Cuándo un router por reglas puede ser mejor que un clasificador LLM?',
      'Cuando las categorías son pocas, claras y estables.',
      ['Cuando las categorías son pocas, claras y estables.', 'Cuando la intención es ambigua y cambia a diario.', 'Cuando no existe forma de observar el resultado.', 'Cuando se busca maximizar costo y latencia.'],
      'Aplica el principio de solución simple para routing.', 'Usar un LLM para una decisión trivial y estable.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si una regla clara cubre el caso, no necesitas clasificador flexible.'),
    mc('gma2-q7', 'medium', '¿Qué debe pasar si una API falla de forma transitoria?',
      'Reintento con backoff, y si persiste, fallback o escalada.',
      ['Reintento con backoff, y si persiste, fallback o escalada.', 'Inventar un resultado plausible para no detener el flujo.', 'Pasar el fallo como verdad al siguiente agente.', 'Aumentar permisos hasta que alguna llamada funcione.'],
      'Evalúa manejo de errores sin alucinar éxito.', 'Silenciar fallos para preservar apariencia de fluidez.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si el fallo es temporal, reintenta controlado; si no, degrada o escala.'),
    mc('gma2-q8', 'hard', '¿Qué control ataca la deriva del objetivo en cadenas largas?',
      'Re-anclar periódicamente en la meta original y validar progreso.',
      ['Re-anclar periódicamente en la meta original y validar progreso.', 'Permitir que cada agente redefina libremente la tarea.', 'Eliminar el presupuesto global para no cortar ideas.', 'Evitar registrar trazas intermedias para reducir ruido.'],
      'Distingue deriva de fallos puntuales de herramienta.', 'Confiar en que cada sub-agente recuerda siempre la intención inicial.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si muchos pasos separan la acción de la meta, necesitas re-anclaje.'),
    mc('gma2-q9', 'hard', '¿Por qué validar entre etapas es una frontera de confianza?',
      'Porque la salida de un agente puede contener errores o instrucciones maliciosas para el siguiente.',
      ['Porque la salida de un agente puede contener errores o instrucciones maliciosas para el siguiente.', 'Porque los mensajes internos siempre son más confiables que datos externos.', 'Porque validar elimina la necesidad de logs y presupuestos.', 'Porque la frontera solo existe en llamadas HTTP públicas.'],
      'Conecta validación intermedia con seguridad de sistemas.', 'Tratar salida de otro agente como autoridad absoluta.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si un mensaje cruza de un rol a otro, puede transportar fallo o ataque.'),
    mc('gma2-q10', 'medium', '¿Qué evita un presupuesto global además de límites por agente?',
      'Que muchos agentes y reintentos sumen una explosión total de costo.',
      ['Que muchos agentes y reintentos sumen una explosión total de costo.', 'Que el sistema mida routing accuracy por componente.', 'Que el router elija reglas cuando son suficientes.', 'Que el agente admita incertidumbre ante una fuente ausente.'],
      'Evalúa costo agregado en sistemas distribuidos de LLMs.', 'Limitar cada agente pero olvidar el gasto total del sistema.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si varias rutas pueden dispararse, controla presupuesto global y local.'),
    mc('gma2-q11', 'hard', '¿Qué distingue fallback de reintento?',
      'Fallback cambia a una alternativa; reintento prueba de nuevo la misma ruta fallida.',
      ['Fallback cambia a una alternativa; reintento prueba de nuevo la misma ruta fallida.', 'Fallback siempre ignora el fallo y responde con confianza.', 'Reintento exige intervención humana antes de cada llamada.', 'Ambos significan aumentar temperatura del modelo.'],
      'Precisa dos mecanismos de recuperación distintos.', 'Repetir indefinidamente la misma llamada sin estrategia alternativa.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si el camino principal no funciona, pregunta si conviene repetir o cambiar de camino.'),
    mc('gma2-q12', 'medium', '¿Qué síntoma muestra routing equivocado?',
      'Una sub-tarea llega a un especialista sin herramientas ni conocimiento adecuados.',
      ['Una sub-tarea llega a un especialista sin herramientas ni conocimiento adecuados.', 'El sistema reporta explícitamente que una API falló.', 'El orquestador aplica timeout antes de entrar en bucle.', 'El agente técnico cita la fuente correcta antes de responder.'],
      'Reconoce fallo de asignación, no de ejecución local.', 'Arreglar prompts del especialista cuando nunca debió recibir la tarea.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si el agente correcto habría tenido herramientas correctas, mide routing.'),
    open('gma2-s3', 'scenario', 'hard', 'Escenario: una consulta ambigua pasa por facturación, técnico y cuenta; cada agente añade supuestos y la respuesta final contradice el objetivo inicial. ¿Cómo lo rediseñas?',
      'Añadiría un router con clasificación explícita y confianza, re-anclaje al objetivo original, límite de saltos, validación de salida por etapa y escalada cuando la intención sea ambigua. También registraría trazas para medir dónde se desvió.',
      'Aplica routing, incertidumbre y límites contra deriva.', 'Dejar que agentes se pasen la tarea hasta que alguno responda.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si la ambigüedad causa cadena larga, decide, valida o escala antes de propagar.'),
    open('gma2-s4', 'scenario', 'medium', 'Escenario: un agente devuelve “no estoy seguro” sobre una fuente crítica. El sintetizador quiere ocultarlo para sonar más firme. ¿Qué debe hacer el orquestador?',
      'Debe preservar la incertidumbre, pedir evidencia adicional o escalar, y evitar que una duda crítica se convierta en afirmación final. La salida puede ser parcial o explícitamente limitada, no falsamente segura.',
      'Manejo de incertidumbre como señal que debe propagarse.', 'Enterrar dudas intermedias para mejorar tono de la respuesta final.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si una etapa no sabe, el sistema debe saber que no sabe.'),
    open('gma2-r3', 'reflexion', 'medium', 'Diseña un router para tres dominios de soporte. ¿Qué casos resolverías con reglas y cuáles con clasificador?',
      'Una respuesta fuerte usa reglas para categorías claras y de bajo cambio, clasificador para ambigüedad o lenguaje variable, y un umbral de confianza con fallback/escalada. Debe incluir cómo medir routing accuracy.',
      'Reflexión sobre routing simple vs flexible.', 'Usar un solo método de routing sin mirar estabilidad y riesgo.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si puedes escribir reglas confiables, empieza ahí; si no, clasifica con evaluación.'),
    open('gma2-r4', 'reflexion', 'hard', 'Traslada patrones de sistemas distribuidos a agentes. ¿Qué equivalentes tienen timeout, circuit breaker y observabilidad?',
      'Debe mapear timeout a límite de espera por agente/herramienta, circuit breaker a bloquear rutas fallidas o costosas, y observabilidad a trazas de routing, acciones, costos, errores e incertidumbre. La transferencia muestra que producción es control de fallos.',
      'Transferencia de resiliencia distribuida a LLMs coordinados.', 'Pensar que un mejor prompt reemplaza timeouts, logs y circuit breakers.', 'orquestación, routing, errores y límites en sistemas multi-agente', 'data/teoria/gen-ma2.md; Orquestación: routing dinámico y manejo de errores entre agentes', 'Si tus nodos son LLMs, aún necesitas ingeniería de sistemas distribuidos.'),
  ],

  'gen-ma3': [
    mc('gma3-q5', 'easy', '¿Qué decisión puede tomar un RAG adaptativo que el RAG fijo no toma?',
      'Decidir no recuperar cuando la pregunta no necesita evidencia externa.',
      ['Decidir no recuperar cuando la pregunta no necesita evidencia externa.', 'Eliminar toda necesidad de evaluar faithfulness.', 'Entrenar de nuevo los pesos del LLM en cada consulta.', 'Garantizar que toda fuente recuperada sea confiable.'],
      'Distingue recuperación condicional de recuperación refleja.', 'Recuperar siempre aunque añada ruido.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si buscar no aporta, la mejor acción puede ser no buscar.'),
    mc('gma3-q6', 'medium', '¿Qué problema resuelve reformular una consulta antes de recuperar?',
      'Una pregunta cruda vaga o mal enfocada que trae fragmentos irrelevantes.',
      ['Una pregunta cruda vaga o mal enfocada que trae fragmentos irrelevantes.', 'La falta de aprobación humana para transferencias irreversibles.', 'La alta varianza de policy gradient en RLHF.', 'El sesgo de posición en comparaciones de jueces.'],
      'Evalúa query rewriting como acción adaptativa.', 'Culpar siempre al generador cuando la consulta recuperó mal.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si la búsqueda falla por formulación, reescribe antes de insistir.'),
    mc('gma3-q7', 'medium', '¿Qué significa routing de fuentes en RAG adaptativo?',
      'Elegir el índice o corpus correcto según la necesidad de información.',
      ['Elegir el índice o corpus correcto según la necesidad de información.', 'Enviar siempre toda pregunta a todos los documentos disponibles.', 'Ordenar tokens por probabilidad antes de generar.', 'Reemplazar embeddings por una tabla Q.'],
      'Conecta routing multi-agente con recuperación multi-fuente.', 'Usar una sola fuente para dominios distintos.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si legal y técnico viven en corpus distintos, la ruta de fuente importa.'),
    mc('gma3-q8', 'hard', '¿Qué debe hacer un RAG adaptativo cuando no encuentra evidencia suficiente?',
      'Admitir el límite, pedir más datos o escalar; no inventar por insistencia.',
      ['Admitir el límite, pedir más datos o escalar; no inventar por insistencia.', 'Seguir recuperando sin límite hasta producir una respuesta segura.', 'Aumentar k indefinidamente y tratar el ruido como evidencia.', 'Usar la memoria interna del LLM como cita documental.'],
      'Recupera el caso borde central: adaptativo no significa alucinatorio.', 'Insistir hasta fabricar evidencia inexistente.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si el corpus no sostiene la respuesta, la respuesta debe decirlo.'),
    mc('gma3-q9', 'hard', '¿Por qué más búsquedas pueden empeorar un RAG adaptativo?',
      'Aumentan costo, latencia, ruido contextual y exposición a contenido no confiable.',
      ['Aumentan costo, latencia, ruido contextual y exposición a contenido no confiable.', 'Reducen automáticamente la superficie de prompt injection.', 'Garantizan mayor precisión de contexto en todos los dominios.', 'Eliminan la necesidad de decidir cuándo parar.'],
      'Evalúa el tradeoff de iterar recuperación.', 'Equivaler más recuperación con mejor recuperación.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si cada búsqueda agrega ruido y riesgo, necesitas criterio de parada.'),
    mc('gma3-q10', 'medium', '¿Qué patrón de agente implementa un RAG adaptativo?',
      'ReAct con buscar como acción, observar evidencia y decidir el siguiente paso.',
      ['ReAct con buscar como acción, observar evidencia y decidir el siguiente paso.', 'Fine-tuning supervisado con una sola respuesta dorada.', 'Q-learning tabular sin herramientas ni observaciones.', 'ROUGE fijo contra una referencia de resumen.'],
      'Conecta recuperación adaptativa con bucle agente-entorno.', 'Ver RAG adaptativo como solo subir k.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si el sistema decide buscar, observa y vuelve a decidir, es ReAct aplicado a RAG.'),
    mc('gma3-q11', 'hard', '¿Qué falla en un RAG fijo ante una pregunta multi-fuente como política 2024 vs actual y regulación?',
      'Una búsqueda única mezcla necesidades distintas y deja huecos de evidencia.',
      ['Una búsqueda única mezcla necesidades distintas y deja huecos de evidencia.', 'El modelo no puede generar texto si recupera documentos.', 'El sistema siempre sabe qué fuente consultar sin routing.', 'La respuesta correcta solo depende de temperatura baja.'],
      'Aplica multi-paso y multi-fuente al ejemplo trabajado.', 'Esperar que una query cruda cubra subtareas heterogéneas.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si la pregunta contiene partes con fuentes distintas, descompón y enruta.'),
    mc('gma3-q12', 'medium', '¿Cuándo un RAG fijo puede ser preferible al adaptativo?',
      'En FAQ simple sobre un corpus único, donde una búsqueda estable basta.',
      ['En FAQ simple sobre un corpus único, donde una búsqueda estable basta.', 'En preguntas legales multi-fuente con evidencia ausente.', 'Cuando hay que decidir dinámicamente si buscar o no.', 'Cuando el sistema debe reformular y comparar varias fuentes.'],
      'Recupera el contraejemplo de simplicidad suficiente.', 'Agregar adaptatividad donde solo suma costo y variabilidad.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si el problema es estable y acotado, la solución fija puede ganar.'),
    open('gma3-s3', 'scenario', 'hard', 'Escenario: un agente recuperador trae un documento irrelevante pero el sintetizador lo usa porque “hay cita”. ¿Qué controles añadirías?',
      'Añadiría evaluación de relevancia y faithfulness por paso, umbral de evidencia, reranking, trazas de qué cita sostiene qué afirmación y una regla para descartar contexto no pertinente. Una cita irrelevante no debe convertirse en autoridad.',
      'Diagnostica ruido recuperado convertido en argumento final.', 'Tratar cualquier documento recuperado como evidencia suficiente.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si la evidencia no sostiene la frase, medir retrieval no basta.'),
    open('gma3-s4', 'scenario', 'medium', 'Escenario: tu RAG adaptativo responde saludos buscando en tres bases documentales. ¿Qué cambiarías?',
      'Implementaría una decisión previa de recuperación: intents triviales o autocontenidos no buscan. Mediría retrieval decision accuracy, costo y ruido contextual contra un baseline always-retrieve.',
      'Aplica decisión de no recuperar para evitar ruido/costo.', 'Recuperar por reflejo porque el sistema tiene una base vectorial.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si la pregunta no requiere evidencia externa, buscar es una acción innecesaria.'),
    open('gma3-r3', 'reflexion', 'medium', 'Diseña una política de recuperación para tres tipos de preguntas: trivial, dominio único y multi-fuente.',
      'Debe definir señales para no recuperar, recuperar una vez o descomponer/rutear. También debe incluir criterio de parada, qué hacer ante evidencia ausente y cómo medir precisión de la decisión de retrieval.',
      'Reflexión sobre política adaptativa de recuperación.', 'Aplicar el mismo k y la misma fuente a todas las preguntas.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Si las preguntas tienen complejidad distinta, la política de retrieval debe variar.'),
    open('gma3-r4', 'reflexion', 'hard', '¿Cómo balancearías potencia y seguridad en un RAG adaptativo que consulta fuentes externas?',
      'Una respuesta fuerte propone control de acceso por fuente, aislamiento de contenido recuperado, validación de citas, límites de iteración/costo, red team de inyecciones, y fallback honesto cuando no hay evidencia.',
      'Transferencia entre adaptatividad, seguridad y costo.', 'Abrir más fuentes sin modelar permisos, inyección ni latencia.', 'RAG adaptativo, routing de fuentes e iteración agéntica', 'data/teoria/gen-ma3.md; RAG adaptativo en sistemas agénticos', 'Cada fuente nueva aporta información y también una frontera de confianza.'),
  ],

  'gen-ma4': [
    mc('gma4-q5', 'easy', '¿Qué mide task success en un sistema de agentes?',
      'Si el sistema completó el objetivo del usuario de extremo a extremo.',
      ['Si el sistema completó el objetivo del usuario de extremo a extremo.', 'Si cada token tuvo baja perplexity durante generación.', 'Si el embedding de la pregunta tiene norma alta.', 'Si el router usó siempre el agente más caro.'],
      'Recupera la métrica reina de resultado final.', 'Confundir métricas internas con objetivo del usuario.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si quieres saber si el usuario logró su objetivo, mide task success.'),
    mc('gma4-q6', 'medium', '¿Por qué task success no basta sola?',
      'No localiza qué componente falló ni captura costo, latencia o seguridad.',
      ['No localiza qué componente falló ni captura costo, latencia o seguridad.', 'Porque nunca puede medirse con un conjunto held-out.', 'Porque solo sirve para modelos sin herramientas.', 'Porque reemplaza automáticamente el red teaming.'],
      'Evalúa la necesidad de métricas por componente y dimensiones extra.', 'Arreglar a ciegas cuando solo sabes que el sistema falló.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si el resultado final falla, necesitas saber qué eslabón lo causó.'),
    mc('gma4-q7', 'medium', '¿Qué mide routing accuracy?',
      'Si el router asignó cada tarea o sub-tarea al agente correcto.',
      ['Si el router asignó cada tarea o sub-tarea al agente correcto.', 'Si el sintetizador escribió con estilo atractivo.', 'Si el modelo de recompensa prefirió una respuesta.', 'Si la base vectorial almacenó chunks grandes.'],
      'Distingue routing accuracy de tool accuracy y calidad final.', 'Culpar a especialistas cuando el router les dio casos incorrectos.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si la pregunta llegó al rol equivocado, mide el router.'),
    mc('gma4-q8', 'hard', '¿Qué evalúa unsafe pass rate en red teaming de agentes?',
      'La proporción de casos adversarios que atraviesan controles y producen acción insegura.',
      ['La proporción de casos adversarios que atraviesan controles y producen acción insegura.', 'La cantidad de documentos recuperados por cada consulta.', 'La frecuencia con que ROUGE supera a BLEU en resúmenes.', 'El número de agentes disponibles en el catálogo.'],
      'Conecta robustez con medición cuantitativa de fallos de seguridad.', 'Declarar seguro un sistema sin medir ataques que pasan.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si pruebas ataques, cuenta cuántos logran cruzar la barrera.'),
    mc('gma4-q9', 'hard', '¿Qué problema indica subir de 70% a 95% tras iterar sobre los mismos casos?',
      'Posible overfitting al set de evaluación; falta held-out nuevo.',
      ['Posible overfitting al set de evaluación; falta held-out nuevo.', 'Prueba definitiva de generalización a producción.', 'Evidencia de que ya no hace falta evaluar componentes.', 'Señal de que el sistema debe agregar más agentes.'],
      'Reconoce sobreajuste de evaluación en sistemas agénticos.', 'Confundir mejora en casos vistos con robustez real.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si optimizaste repetidamente el mismo set, reserva casos nuevos.'),
    mc('gma4-q10', 'medium', '¿Qué dimensión captura que un sistema correcto sea inviable por caro o lento?',
      'Eficiencia: pasos, llamadas, costo y latencia.',
      ['Eficiencia: pasos, llamadas, costo y latencia.', 'Solo calidad estilística de la respuesta final.', 'Cantidad de agentes definidos en el diagrama.', 'Longitud promedio de las instrucciones del sistema.'],
      'Incluye costo/latencia como parte de evaluación.', 'Medir calidad e ignorar viabilidad operativa.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si acierta pero cuesta demasiado, la métrica debe mostrarlo.'),
    mc('gma4-q11', 'hard', '¿Qué conclusión sale si un agente único logra 90% y el multi-agente 88% al triple de costo?',
      'No usar multi-agente; la evaluación no justifica la complejidad.',
      ['No usar multi-agente; la evaluación no justifica la complejidad.', 'Agregar más agentes hasta superar el costo del baseline.', 'Ignorar costo porque la arquitectura es más avanzada.', 'Medir solo debate interno y descartar task success.'],
      'Aplica métrica como guardarraíl contra sobreingeniería.', 'Preferir complejidad aunque pierda contra el baseline.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si el baseline simple gana, la arquitectura compleja debe retirarse o cambiar.'),
    mc('gma4-q12', 'medium', '¿Qué hace accionable una evaluación por componente?',
      'Convierte “falló el sistema” en un fallo localizado de routing, tool use, síntesis o seguridad.',
      ['Convierte “falló el sistema” en un fallo localizado de routing, tool use, síntesis o seguridad.', 'Oculta trazas intermedias para juzgar solo la salida final.', 'Reemplaza todos los casos adversarios con ejemplos felices.', 'Garantiza que nunca habrá regresiones entre versiones.'],
      'Recupera el valor diagnóstico de separar culpas.', 'Medir un promedio global que no dice qué arreglar.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si puedes nombrar el eslabón fallido, puedes intervenir con precisión.'),
    open('gma4-s3', 'scenario', 'hard', 'Escenario: un sistema multi-agente tiene task success alto, pero una inyección en una fuente hace que envíe datos sensibles. ¿Está listo?',
      'No. Task success y seguridad son dimensiones distintas. Hay que medir red teaming, unsafe pass rate, control de permisos, validación entre agentes y casos adversarios antes de producción.',
      'Distingue éxito funcional de seguridad operacional.', 'Aceptar alto task success como sustituto de robustez adversaria.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si el sistema cumple tareas pero cae ante ataques, no está evaluado para producción.'),
    open('gma4-s4', 'scenario', 'medium', 'Escenario: el informe final está mal. Routing fue correcto, tool accuracy fue alta, pero las citas no sostienen las conclusiones. ¿Qué componente arreglas?',
      'El problema apunta a síntesis/faithfulness: el sintetizador no mantuvo fidelidad a la evidencia. Debes evaluar afirmación-cita, añadir verificación de groundedness y quizá un revisor especializado en fuentes.',
      'Localiza fallo de síntesis tras descartar routing y tool use.', 'Cambiar el router aunque la evidencia muestra otro eslabón fallido.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si las herramientas trajeron bien la evidencia pero la conclusión no se sostiene, mira síntesis.'),
    open('gma4-r3', 'reflexion', 'medium', 'Diseña una matriz mínima de evaluación para un sistema multi-agente que incluya resultado, componentes y eficiencia.',
      'Debe incluir task success, routing accuracy, tool accuracy, calidad por agente, faithfulness, costo, latencia y pasos. También debe explicar cómo cada columna decide una acción de mejora concreta.',
      'Reflexión sobre evaluación accionable y multidimensional.', 'Medir solo un score final sin trazas ni costo.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si una métrica no cambia una decisión de ingeniería, revisa por qué está ahí.'),
    open('gma4-r4', 'reflexion', 'hard', '¿Cómo evitarías que tu suite de evaluación se vuelva una lista memorizada por el equipo?',
      'Una respuesta fuerte propone held-out, rotación de casos, generación de adversarios nuevos, revisión externa, ablations, congelar un set de regresión y reportar intervalos o segmentos, no solo un promedio optimizado.',
      'Reflexión sobre overfitting de evaluación en operación continua.', 'Iterar eternamente sobre los mismos ejemplos y declarar generalización.', 'evaluación de sistemas multi-agente por resultado y componente', 'data/teoria/gen-ma4.md; Evaluar y medir sistemas de agentes', 'Si el equipo conoce todos los casos, necesitas una reserva real y casos renovados.'),
  ],
};

for (const unit of doc.unidades) {
  const items = additions[unit.id];
  if (!items) continue;
  const byId = new Map((unit.banco || []).map((q) => [q.id, q]));
  for (const item of items) byId.set(item.id, item);
  unit.banco = [...byId.values()].sort(compareIds);
}

writeFileSync(path, `${JSON.stringify(doc, null, 2)}\n`, 'utf8');
const summary = Object.entries(additions).map(([id, items]) => `${id}:${items.length}`).join(' ');
console.log(`OK: multiagente ampliado manualmente (${summary})`);

function mc(id, difficulty, enunciado, answer, options, explicacion, common_mistake, concept, source_reference, recognition_signal) {
  return { id, tipo: 'concepto', enunciado, solucion: answer, explicacion, difficulty, answer, options, common_mistake, type: 'quiz', prompt: enunciado, feedback: explicacion, concept, source_reference, recognition_signal };
}

function open(id, tipo, difficulty, enunciado, solucion, explicacion, common_mistake, concept, source_reference, recognition_signal) {
  return { id, tipo, enunciado, solucion, explicacion, difficulty, answer: solucion, common_mistake, type: tipo === 'scenario' ? 'scenario' : 'reflection', prompt: enunciado, feedback: explicacion, concept, source_reference, recognition_signal };
}

function compareIds(a, b) {
  const pa = parts(a.id);
  const pb = parts(b.id);
  if (pa.kind !== pb.kind) return order(pa.kind) - order(pb.kind);
  return pa.num - pb.num;
}

function parts(id) {
  const match = id.match(/-(q|s|r)(\d+)$/);
  return { kind: match?.[1] ?? 'z', num: Number(match?.[2] ?? 9999) };
}

function order(kind) {
  return { q: 1, s: 2, r: 3, z: 4 }[kind] ?? 4;
}
