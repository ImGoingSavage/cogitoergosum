import { readFileSync, writeFileSync } from 'node:fs';

const path = 'data/genai/_unidades.json';
const doc = JSON.parse(readFileSync(path, 'utf8'));

const additions = {
  'gen-eval1': [
    mc('gev1-q5', 'easy', '¿Qué propiedad de la generación rompe la idea de “clave única” de una clasificación?',
      'La multiplicidad: muchas respuestas distintas pueden ser igualmente válidas.',
      ['La multiplicidad: muchas respuestas distintas pueden ser igualmente válidas.', 'La generación siempre produce una sola etiqueta discreta.', 'El texto generado no puede compararse con humanos.', 'Las métricas de generación no pueden usar datasets.'],
      'Evalúa por qué generación se parece más a ensayo que a opción múltiple.', 'Buscar una respuesta dorada única para tareas abiertas.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si varias salidas buenas no comparten palabras, una clave única no basta.'),
    mc('gev1-q6', 'medium', '¿Qué dimensión de “buena respuesta” no mide ROUGE aunque el texto suene fluido?',
      'Fidelidad factual: si las afirmaciones son verdaderas y seguras.',
      ['Fidelidad factual: si las afirmaciones son verdaderas y seguras.', 'Cantidad de n-gramas compartidos con la referencia.', 'Recall léxico frente a una respuesta humana.', 'Longitud de subsecuencia común en ROUGE-L.'],
      'Distingue superposición léxica de verdad factual.', 'Usar ROUGE como métrica general de calidad.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si una palabra cambia un hecho crítico, contar n-gramas no alcanza.'),
    mc('gev1-q7', 'medium', '¿Por qué BLEU penaliza respuestas demasiado cortas en traducción?',
      'Para evitar que una salida breve gane precisión omitiendo contenido necesario.',
      ['Para evitar que una salida breve gane precisión omitiendo contenido necesario.', 'Para convertir precisión de n-gramas en similitud semántica.', 'Para evaluar alucinaciones sin referencia humana.', 'Para medir si la respuesta cita fuentes externas.'],
      'Evalúa la penalización por brevedad de BLEU.', 'Pensar que precisión de n-gramas basta sin controlar omisiones.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si un sistema puede ganar escribiendo poco, la métrica necesita penalizar brevedad.'),
    mc('gev1-q8', 'hard', '¿Qué falla si la única referencia humana es pobre o demasiado estrecha?',
      'La métrica penaliza salidas buenas que difieren de una referencia limitada.',
      ['La métrica penaliza salidas buenas que difieren de una referencia limitada.', 'ROUGE se vuelve una métrica sin referencia automáticamente.', 'BLEU deja de contar n-gramas y mide factualidad.', 'El sistema ya no necesita evaluación humana.'],
      'Recupera el caso borde: la métrica no supera la calidad de su referencia.', 'Tratar una referencia única como universo de respuestas válidas.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si la referencia es estrecha, mide contra su sesgo, no contra calidad total.'),
    mc('gev1-q9', 'medium', '¿Cuál es una lectura correcta de ROUGE alto en un resumen?',
      'La salida comparte mucha superficie léxica con la referencia; no prueba calidad total.',
      ['La salida comparte mucha superficie léxica con la referencia; no prueba calidad total.', 'La salida es factualmente correcta en todos sus detalles.', 'La salida es necesariamente mejor para el usuario final.', 'La salida no requiere revisión semántica ni humana.'],
      'Evita sobreinterpretar un proxy reproducible.', 'Convertir un número alto en garantía de utilidad.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si la métrica cuenta palabras, interpreta el resultado como solapamiento, no verdad.'),
    mc('gev1-q10', 'hard', '¿Qué decisión de evaluación tomarías para un asistente legal abierto sin respuestas doradas por consulta?',
      'Usar rúbrica sin referencia, LLM-juez calibrado y muestreo humano/factualidad.',
      ['Usar rúbrica sin referencia, LLM-juez calibrado y muestreo humano/factualidad.', 'Usar BLEU con una sola respuesta inventada por el evaluador.', 'Optimizar ROUGE porque siempre correlaciona con utilidad legal.', 'Evitar evaluación porque no hay referencia exacta.'],
      'Aplica con/sin referencia a un sistema real.', 'Forzar métricas con referencia donde la tarea es abierta.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si no existe referencia natural, diseña rúbrica y verificación sin referencia.'),
    mc('gev1-q11', 'medium', '¿Qué ejemplo muestra mejor la ley de Goodhart aplicada a ROUGE?',
      'Copiar frases de la referencia sube el score pero produce peores resúmenes.',
      ['Copiar frases de la referencia sube el score pero produce peores resúmenes.', 'Usar varias referencias reduce sesgo de una referencia única.', 'Medir BLEU en traducción profesional comparable.', 'Complementar ROUGE con juicio humano calibrado.'],
      'Evalúa optimizar proxy en vez de tarea.', 'Creer que subir una métrica siempre mejora el producto.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si el sistema aprende a satisfacer la métrica y empeora la tarea, hay Goodhart.'),
    mc('gev1-q12', 'hard', '¿Cuándo ROUGE/BLEU siguen siendo útiles según la lección?',
      'En benchmarks comparables con buenas referencias y tareas acotadas.',
      ['En benchmarks comparables con buenas referencias y tareas acotadas.', 'En cualquier chatbot abierto sin referencia por consulta.', 'Para demostrar factualidad en dominios médicos.', 'Para reemplazar por completo evaluación semántica.'],
      'Recupera el contraejemplo: insuficientes no significa inútiles.', 'Desechar métricas clásicas incluso donde sí son comparables y baratas.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si hay referencias buenas y tarea estable, una métrica léxica puede servir como señal parcial.'),
    open('gev1-s3', 'scenario', 'hard', 'Escenario: un resumen médico cambia “diario” por “semanal” y mantiene casi todas las palabras. ROUGE sube frente a otra paráfrasis correcta. ¿Cómo rediseñas la evaluación?',
      'Mantendría ROUGE solo como señal secundaria y añadiría evaluación semántica/factual: checks de unidades críticas, LLM-juez con rúbrica clínica, revisión humana de muestra y penalización fuerte por cambios de dosis/frecuencia. La métrica debe medir daño factual, no solo solapamiento.',
      'Caso de falso positivo léxico con consecuencia médica.', 'Aceptar un score alto aunque cambie una variable clínica crítica.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si una palabra cambia el riesgo, la métrica debe mirar factualidad.'),
    open('gev1-s4', 'scenario', 'medium', 'Escenario: tu equipo quiere comparar dos traductores internos con un corpus fijo y referencias profesionales. ¿Defenderías BLEU como parte de la evaluación?',
      'Sí, como parte de la evaluación: en traducción con referencias profesionales y corpus comparable, BLEU es barato y reproducible. Pero lo acompañaría con revisión humana o métricas semánticas para errores críticos, porque BLEU sigue siendo un proxy de n-gramas.',
      'Usa el contraejemplo donde la métrica clásica sí aporta.', 'Pensar que una métrica imperfecta no sirve nunca.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si el benchmark es acotado y con referencias buenas, BLEU puede ser señal útil.'),
    open('gev1-r3', 'reflexion', 'medium', 'Diseña una rúbrica mínima para una respuesta de soporte que no tenga referencia única. ¿Qué dimensiones pondrías y qué peso tendría cada una?',
      'Una buena respuesta incluye dimensiones como resolución del problema, fidelidad a políticas, claridad, concisión, tono y seguridad. Debe justificar pesos según consecuencias: en soporte regulado, fidelidad y seguridad pesan más que estilo.',
      'Reflexión sobre calidad multidimensional sin referencia única.', 'Diseñar una rúbrica solo con “suena bien”.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si no hay respuesta única, define dimensiones de calidad explícitas.'),
    open('gev1-r4', 'reflexion', 'hard', 'Elige un KPI de tu entorno que sea proxy de algo importante. ¿Cómo podría ser hackeado y qué métrica complementaria añadirías?',
      'Una respuesta fuerte identifica el objetivo real, el proxy y el modo de gaming: tickets cerrados vs calidad, clicks vs satisfacción, alertas vs seguridad. Debe añadir una señal complementaria que capture el daño oculto o revisión cualitativa.',
      'Transferencia de Goodhart desde ROUGE/BLEU a sistemas reales.', 'Optimizar lo fácil de medir sin vigilar efectos secundarios.', 'evaluación de generación, métricas proxy y límites de ROUGE/BLEU', 'data/teoria/gen-eval1.md; Por qué evaluar texto generado es difícil', 'Si una métrica se vuelve objetivo, busca cómo se puede explotar.'),
  ],

  'gen-eval2': [
    mc('gev2-q5', 'easy', '¿Qué necesita BERTScore que LLM-as-a-judge puede evitar?',
      'Una referencia dorada contra la cual comparar la salida.',
      ['Una referencia dorada contra la cual comparar la salida.', 'Un conjunto de documentos recuperados por BM25.', 'Una máscara causal en cada respuesta.', 'Un índice HNSW de millones de vectores.'],
      'Distingue métrica semántica con referencia de juez sin referencia.', 'Creer que BERTScore resuelve evaluación abierta sin referencia.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si tienes referencia y quieres significado, BERTScore ayuda; si no, mira jueces/rúbricas.'),
    mc('gev2-q6', 'medium', '¿Qué sesgo se mitiga evaluando A vs B y luego B vs A?',
      'Sesgo de posición.',
      ['Sesgo de posición.', 'Falta de embeddings multilingües.', 'Alucinación intrínseca.', 'Penalización por brevedad.'],
      'Evalúa control de orden en pairwise judging.', 'Confiar en un único orden de presentación.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si el ganador cambia al invertir orden, el juez está contaminado por posición.'),
    mc('gev2-q7', 'medium', '¿Qué hace que una escala pointwise 1–5 sea ruidosa sin rúbrica?',
      'El juez no tiene criterios ancla para asignar números consistentemente.',
      ['El juez no tiene criterios ancla para asignar números consistentemente.', 'El modo pointwise siempre compara dos respuestas.', 'La escala elimina sesgos de verbosidad automáticamente.', 'Las respuestas dejan de necesitar pregunta original.'],
      'Evalúa por qué las rúbricas importan para puntuaciones absolutas.', 'Pedir notas numéricas sin definir qué significa cada nota.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si el juez puntúa en abstracto, dale criterios y ejemplos ancla.'),
    mc('gev2-q8', 'hard', '¿Por qué BERTScore puede fallar ante una afirmación falsa bien parafraseada?',
      'Mide adecuación semántica con una referencia, no verifica verdad externa.',
      ['Mide adecuación semántica con una referencia, no verifica verdad externa.', 'Solo cuenta n-gramas exactos como ROUGE-1.', 'No puede comparar palabras con embeddings.', 'Siempre detecta negaciones mejor que un humano.'],
      'Evalúa el límite factual de una métrica semántica.', 'Confundir similitud de significado con verificación de hechos.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si la pregunta es factual, necesitas anclaje además de similitud.'),
    mc('gev2-q9', 'medium', '¿Qué riesgo hay al usar el mismo modelo/familia como generador y juez?',
      'Self-enhancement: el juez puede favorecer su propio estilo o errores.',
      ['Self-enhancement: el juez puede favorecer su propio estilo o errores.', 'El juez deja de poder leer respuestas largas.', 'La comparación pairwise se vuelve imposible.', 'BERTScore reemplaza automáticamente al juez.'],
      'Evalúa sesgo de autoafinidad.', 'Creer que un juez de la misma familia es neutral por ser potente.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si juez y modelo comparten familia, calibra contra humano o juez alternativo.'),
    mc('gev2-q10', 'hard', '¿Qué práctica reduce el sesgo de verbosidad en un LLM-juez?',
      'Una rúbrica que premie concisión suficiente y penalice relleno irrelevante.',
      ['Una rúbrica que premie concisión suficiente y penalice relleno irrelevante.', 'Pedir siempre respuestas evaluadas en primer lugar.', 'Eliminar la pregunta original del prompt de evaluación.', 'Usar solo ROUGE-L como juez final.'],
      'Evalúa mitigación concreta del sesgo de respuestas largas.', 'Confundir detalle con calidad sin criterios.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si el juez prefiere largo, define concisión como criterio explícito.'),
    mc('gev2-q11', 'medium', '¿Por qué pairwise puede alimentar rankings tipo Arena mejor que notas absolutas?',
      'Porque preferencias comparativas son más estables para humanos y modelos.',
      ['Porque preferencias comparativas son más estables para humanos y modelos.', 'Porque pairwise elimina toda necesidad de más de un caso.', 'Porque siempre produce una explicación factual verificada.', 'Porque no sufre ningún sesgo de orden.'],
      'Evalúa por qué comparar suele ser más fiable que puntuar en abstracto.', 'Asumir que pairwise elimina todos los sesgos sin controles.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si la escala absoluta fluctúa, compara pares y controla orden.'),
    mc('gev2-q12', 'hard', '¿Qué combinación es más robusta para evaluar factualidad en RAG?',
      'LLM-juez con rúbrica más verificación contra fuentes/citas recuperadas.',
      ['LLM-juez con rúbrica más verificación contra fuentes/citas recuperadas.', 'BERTScore solo, porque mide significado de cada token.', 'Pointwise 1–5 sin contexto para ahorrar tokens.', 'Preferir siempre la respuesta más larga y detallada.'],
      'Integra juez con anclaje externo.', 'Dejar factualidad a la opinión no anclada de otro LLM.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si evalúas verdad, el juez debe mirar evidencia externa.'),
    open('gev2-s3', 'scenario', 'hard', 'Escenario: haces un benchmark pairwise y el modelo A gana 62% de las veces. Al invertir el orden de presentación, gana solo 48%. ¿Qué concluyes?',
      'El resultado está contaminado por sesgo de posición. No reportaría el 62% como ventaja real. Repetiría A/B y B/A, promediaría órdenes, revisaría la rúbrica y quizá usaría varios jueces o calibración humana antes de declarar ganador.',
      'Caso cuantitativo de sesgo de posición.', 'Reportar un ranking sin test de orden.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si invertir orden cambia el ganador, tu benchmark mide posición.'),
    open('gev2-s4', 'scenario', 'medium', 'Escenario: tu juez 1–5 da notas muy distintas para la misma respuesta en corridas diferentes. ¿Qué rediseñas?',
      'Cambiaría a pairwise cuando sea posible, agregaría rúbrica explícita con niveles ancla, ejemplos oro, temperatura baja/estable, y mediría agreement con humanos en una muestra. Si se mantiene ruidoso, usaría panel o agregación de múltiples evaluaciones.',
      'Diseño de juez más estable.', 'Tratar varianza del juez como ruido inevitable que no se mide.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si la nota absoluta fluctúa, ancla criterios o compara pares.'),
    open('gev2-r3', 'reflexion', 'medium', '¿Qué ejemplos ancla incluirías en una rúbrica para evaluar respuestas de tu dominio?',
      'Una buena respuesta incluye al menos un ejemplo excelente, uno aceptable y uno peligroso, con explicación de la nota. Debe cubrir errores reales del dominio: omisión crítica, tono excesivo, falta de fuente, verbosidad o afirmación no soportada.',
      'Reflexión sobre calibración de rúbricas.', 'Diseñar rúbricas abstractas sin ejemplos que fijen criterio.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si dos evaluadores no comparten ejemplos ancla, sus notas divergen.'),
    open('gev2-r4', 'reflexion', 'hard', 'Un juez automático escala barato pero sesgado; humanos son caros pero confiables. ¿Qué mezcla usarías para un producto crítico?',
      'Una respuesta fuerte propone juez automático para cobertura amplia, muestreo humano estratificado para calibrar, revisión especial de casos de alto riesgo, métricas de agreement y reentrenamiento/ajuste de la rúbrica cuando aparezcan sesgos.',
      'Reflexión sobre escala vs confiabilidad.', 'Elegir 100% automatizado o 100% humano sin pensar en riesgo.', 'BERTScore, LLM-as-a-judge y sesgos de evaluación', 'data/teoria/gen-eval2.md; Métricas semánticas y LLM-as-a-judge', 'Si el riesgo es alto, usa automatización calibrada, no fe ciega.'),
  ],

  'gen-eval3': [
    mc('gev3-q5', 'easy', '¿Qué tipo de alucinación contradice directamente el documento recuperado?',
      'Intrínseca.',
      ['Intrínseca.', 'Extrínseca.', 'Verbosa.', 'Pairwise.'],
      'Evalúa la taxonomía básica de alucinaciones.', 'Confundir contradicción de fuente con invención no verificable.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si contradice la fuente dada, es intrínseca.'),
    mc('gev3-q6', 'medium', '¿Qué señal produce SelfCheckGPT cuando una afirmación es inventada?',
      'Varias muestras dan afirmaciones divergentes o incompatibles.',
      ['Varias muestras dan afirmaciones divergentes o incompatibles.', 'Todas las muestras citan la misma fuente verificada.', 'El modelo reduce automáticamente su temperatura a cero.', 'ROUGE sube aunque la afirmación sea falsa.'],
      'Evalúa inconsistencia entre muestras como señal.', 'Pedir una sola muestra y perder variación informativa.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si al repetir cambian números/citas, sospecha invención.'),
    mc('gev3-q7', 'medium', '¿Qué control operativo vuelve verificable una respuesta factual de alto riesgo?',
      'Exigir citas y comprobar que cada cita sostiene la afirmación.',
      ['Exigir citas y comprobar que cada cita sostiene la afirmación.', 'Pedir al modelo que responda con más seguridad.', 'Aumentar la longitud de la respuesta final.', 'Usar solo chain-of-thought privado.'],
      'Evalúa anclaje/groundedness como auditoría.', 'Aceptar citas decorativas sin revisar si dicen lo afirmado.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si la afirmación importa, debe apuntar a evidencia que realmente la respalde.'),
    mc('gev3-q8', 'hard', '¿Cuál es el límite de la consistencia como detector de alucinaciones?',
      'Un modelo puede repetir consistentemente el mismo error horneado en sus pesos.',
      ['Un modelo puede repetir consistentemente el mismo error horneado en sus pesos.', 'La consistencia siempre requiere una base vectorial.', 'Si hay consistencia, ya no hace falta anclaje.', 'La consistencia solo aplica a tareas creativas.'],
      'Recupera el contraejemplo: consistencia sugiere, no garantiza verdad.', 'Tratar acuerdo entre muestras como prueba definitiva.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si todas las muestras coinciden, aún verifica contra fuente cuando importa.'),
    mc('gev3-q9', 'hard', '¿Cuándo “inventar” no debe contarse como alucinación problemática?',
      'En tareas creativas donde la ficción o el brainstorming son el objetivo.',
      ['En tareas creativas donde la ficción o el brainstorming son el objetivo.', 'En asesoría legal con citas requeridas.', 'En respuestas médicas con dosis específicas.', 'En RAG corporativo que exige fidelidad al documento.'],
      'Evalúa que alucinación depende de la tarea y factualidad requerida.', 'Castigar creatividad como si fuera fallo factual.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si la tarea no exige verdad factual, “inventar” puede ser comportamiento deseado.'),
    mc('gev3-q10', 'medium', '¿Por qué pedir “¿qué tan seguro estás?” al modelo no basta?',
      'Porque su autoconfianza está mal calibrada y puede sonar seguro estando equivocado.',
      ['Porque su autoconfianza está mal calibrada y puede sonar seguro estando equivocado.', 'Porque los LLMs no pueden producir lenguaje en primera persona.', 'Porque la confianza siempre baja cuando hay una cita.', 'Porque SelfCheckGPT reemplaza todo anclaje externo.'],
      'Evalúa la trampa de confiar en tono o autoevaluación.', 'Usar confianza declarada como detector principal.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si el modelo suena seguro, eso no aumenta la evidencia.'),
    mc('gev3-q11', 'medium', '¿Qué métrica operacional resume afirmaciones sin soporte en una respuesta?',
      'Unsupported claim rate.',
      ['Unsupported claim rate.', 'BLEU brevity penalty.', 'Número de heads de atención.', 'Tamaño del chunk promedio.'],
      'Conecta verificación por claims con una métrica práctica.', 'Medir solo fluidez cuando el fallo es falta de soporte.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si verificas claims, cuenta cuántos no tienen evidencia.'),
    mc('gev3-q12', 'hard', '¿Qué combinación es más fuerte para un asistente médico factual?',
      'Consistencia multi-muestra, verificación por fuente y abstención si falta evidencia.',
      ['Consistencia multi-muestra, verificación por fuente y abstención si falta evidencia.', 'Una sola respuesta larga con tono clínico seguro.', 'ROUGE contra una referencia genérica sin revisar fuentes.', 'Temperatura alta para cubrir más posibilidades.'],
      'Integra consistencia, anclaje y política de no sé.', 'Confiar en estilo profesional como seguridad.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'En alto riesgo, combina señales y abstén si no hay soporte.'),
    open('gev3-s3', 'scenario', 'hard', 'Escenario: un asistente cita tres papers que no existen. Al repetir la pregunta, inventa títulos distintos. ¿Qué protocolo aplicarías?',
      'Primero marcaría posible alucinación extrínseca por citas inexistentes. Aplicaría consistencia multi-muestra para confirmar variabilidad, luego verificación externa de cada cita en el corpus/base bibliográfica. En producción exigiría que solo cite documentos recuperados y que se abstenga si no hay fuente.',
      'Caso de citas inventadas con inconsistencia observable.', 'Aceptar referencias bibliográficas por formato convincente.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si las citas cambian entre muestras, verifica existencia antes de confiar.'),
    open('gev3-s4', 'scenario', 'medium', 'Escenario: un RAG recupera correctamente una garantía de 12 meses, pero la respuesta dice “24 meses”. ¿Cómo clasificas y depuras el fallo?',
      'Es alucinación intrínseca: contradice el contexto dado. Depuraría generación/fidelidad, no retrieval: revisar instrucción “responde solo con contexto”, verificador de claims, citas obligatorias y ejemplos negativos donde no puede cambiar números.',
      'Separa recuperación correcta de generación infiel.', 'Rehacer chunking cuando el contexto ya era correcto.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si el contexto correcto llegó y la respuesta lo contradice, falla faithfulness.'),
    open('gev3-r3', 'reflexion', 'medium', '¿Qué tipos de afirmaciones de tu dominio deberían convertirse en claims verificables antes de publicarse?',
      'Una buena respuesta enumera afirmaciones de alto impacto: números, fechas, citas legales, dosis, cobertura, precios, permisos. Debe explicar qué fuente las respalda y qué pasaría si se publican sin soporte.',
      'Reflexión sobre descomponer respuestas en claims auditables.', 'Verificar solo el tono general y no afirmaciones críticas.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si una afirmación puede causar daño, trátala como claim verificable.'),
    open('gev3-r4', 'reflexion', 'hard', 'Diseña una regla para decidir cuántas muestras usar en un chequeo de consistencia. ¿Qué tradeoff aparece?',
      'Una respuesta fuerte balancea costo/latencia contra sensibilidad: más muestras detectan más divergencia pero encarecen y ralentizan. Propone aumentar muestras en dominios de alto riesgo o cuando la primera respuesta no tiene fuente sólida, y combinar con anclaje.',
      'Reflexión sobre costo de self-consistency/SelfCheckGPT.', 'Pedir muchas muestras siempre sin medir costo ni beneficio.', 'alucinaciones, consistencia, anclaje y confianza mal calibrada', 'data/teoria/gen-eval3.md; Detección de alucinaciones', 'Si subes muestras, mide detección ganada contra latencia/costo.'),
  ],

  'gen-eval4': [
    mc('gev4-q5', 'easy', '¿Qué paso falta si cambias un prompt y solo dices “se ve mejor”?',
      'Medirlo contra una línea base y un set de evaluación.',
      ['Medirlo contra una línea base y un set de evaluación.', 'Agregar más ejemplos al prompt sin registrar cambios.', 'Subir temperatura para obtener salidas variadas.', 'Elegir el cambio que produce respuestas más largas.'],
      'Evalúa el núcleo del lazo de optimización.', 'Aceptar intuición o demo como evidencia.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si no hay baseline y métrica, no sabes si mejoró.'),
    mc('gev4-q6', 'medium', '¿Por qué cambiar rol, formato y ejemplos al mismo tiempo es mala práctica experimental?',
      'No sabes cuál cambio causó la mejora o la regresión.',
      ['No sabes cuál cambio causó la mejora o la regresión.', 'Los LLMs no entienden roles ni formatos.', 'Few-shot solo funciona sin métrica.', 'El held-out deja de ser necesario.'],
      'Evalúa control de variables en prompt optimization.', 'Cambiar muchas cosas y atribuir causalidad a una sola.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si cambias varias cosas, pierdes diagnóstico.'),
    mc('gev4-q7', 'medium', '¿Qué técnica conviene probar si el problema principal es salida JSON inconsistente?',
      'Formato explícito más few-shot con ejemplos válidos de JSON.',
      ['Formato explícito más few-shot con ejemplos válidos de JSON.', 'Chain-of-thought largo para todos los campos.', 'Eliminar ejemplos para dejar libertad al modelo.', 'Subir k de retrieval aunque no haya documentos.'],
      'Aplica técnica de prompting al síntoma correcto.', 'Usar CoT por moda en una tarea de formato.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si falla formato, muestra el patrón exacto y exige estructura.'),
    mc('gev4-q8', 'hard', '¿Qué señal indica overfitting al set de evaluación de prompts?',
      'Mejora fuerte en el set iterado y mejora nula o caída en held-out.',
      ['Mejora fuerte en el set iterado y mejora nula o caída en held-out.', 'Sube la métrica en train y held-out por igual.', 'El prompt conserva una sola instrucción clara.', 'La rúbrica penaliza respuestas no soportadas.'],
      'Evalúa sobreajuste por iterar demasiadas veces sobre los mismos casos.', 'Creer que el set de evaluación sigue siendo test después de usarlo para optimizar.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si miraste un set muchas veces, ya no es prueba independiente.'),
    mc('gev4-q9', 'medium', '¿Qué comparten APE y DSPy con el lazo manual de la lección?',
      'La evaluación decide qué prompt conservar; no el gusto del diseñador.',
      ['La evaluación decide qué prompt conservar; no el gusto del diseñador.', 'Ambos evitan construir datasets de evaluación.', 'Ambos prohíben cambiar instrucciones de formato.', 'Ambos convierten prompts en pesos permanentes del LLM.'],
      'Evalúa optimización automática como búsqueda guiada por métricas.', 'Creer que automatizar prompts elimina la necesidad de datos.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si el sistema busca prompts, aún necesita métrica que seleccione.'),
    mc('gev4-q10', 'hard', '¿Por qué CoT puede empeorar una tarea simple de extracción?',
      'Añade pasos, ruido y latencia donde bastaba copiar campos con formato claro.',
      ['Añade pasos, ruido y latencia donde bastaba copiar campos con formato claro.', 'Porque CoT solo funciona en modelos sin embeddings.', 'Porque impide usar held-out para evaluar.', 'Porque elimina la posibilidad de few-shot.'],
      'Recupera el contraejemplo: técnica famosa no siempre ayuda.', 'Aplicar CoT universalmente por reputación.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si la tarea no requiere razonamiento, CoT puede ser carga innecesaria.'),
    mc('gev4-q11', 'medium', '¿Qué instrucción de grounding reduce alucinación en un prompt RAG?',
      'Responde solo con el contexto; si no está, dilo.',
      ['Responde solo con el contexto; si no está, dilo.', 'Usa cualquier conocimiento general para completar huecos.', 'Nunca cites documentos porque distraen.', 'Ignora el contexto si tu respuesta suena mejor.'],
      'Conecta prompting con anclaje a fuentes.', 'Permitir que el modelo rellene huecos con memoria no verificada.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si el sistema tiene fuentes, limita la respuesta a ellas.'),
    mc('gev4-q12', 'hard', '¿Qué riesgo de seguridad aparece al incluir contenido no confiable dentro del prompt?',
      'Prompt injection: el contenido puede intentar cambiar instrucciones o exfiltrar datos.',
      ['Prompt injection: el contenido puede intentar cambiar instrucciones o exfiltrar datos.', 'El modelo deja de poder generar texto natural.', 'ROUGE se vuelve imposible de calcular.', 'El held-out mide automáticamente permisos.'],
      'Evalúa el prompt como superficie de ataque.', 'Tratar todo texto incluido en el prompt como instrucciones legítimas.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si el prompt contiene datos externos, sepáralos de instrucciones confiables.'),
    open('gev4-s3', 'scenario', 'hard', 'Escenario: un prompt con CoT sube accuracy de razonamiento de 68% a 74%, pero duplica latencia y empeora extracción JSON. ¿Cómo decides si conservarlo?',
      'Segmentaría por tarea: quizá conservar CoT solo para razonamiento multi-paso y desactivarlo para extracción. Evaluaría delta, latencia, costo y regresiones por segmento en held-out. No lo dejaría globalmente por una mejora promedio que esconde daño en otra clase de casos.',
      'Caso de tradeoff por segmento en prompt optimization.', 'Conservar una técnica global por mejora promedio sin mirar regresiones.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si una técnica ayuda a un segmento y daña otro, enruta o condiciona.'),
    open('gev4-s4', 'scenario', 'medium', 'Escenario: tras 80 iteraciones, el prompt contiene reglas específicas para cada ejemplo fallido del set. En held-out cae. ¿Qué hiciste mal?',
      'Convertiste el prompt en una memorización del set de validación: overfitting. Debes congelar un held-out, limitar iteraciones, agrupar errores por patrón general y conservar reglas que mejoren distribución nueva, no casos vistos uno por uno.',
      'Diagnóstico de overfitting de prompt.', 'Parchear ejemplos individuales y llamar a eso generalización.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si el prompt enumera casos vistos, probablemente memorizó el benchmark.'),
    open('gev4-r3', 'reflexion', 'medium', '¿Qué haría que tu set de evaluación de prompts fuera representativo de producción?',
      'Una buena respuesta incluye distribución real de tareas, idiomas, longitudes, casos raros, adversarios, ejemplos de abstención y segmentos de alto impacto. Debe explicar cómo se actualizaría cuando cambie el uso.',
      'Reflexión sobre calidad del set como calidad de optimización.', 'Usar solo casos fáciles o demos exitosas.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si el set no se parece a producción, optimizas el prompt equivocado.'),
    open('gev4-r4', 'reflexion', 'hard', 'Si el prompt es “código”, ¿qué prácticas de ingeniería de software aplicarías a prompts críticos?',
      'Una respuesta fuerte menciona versionado, review, tests, changelog, rollback, evaluación CI, separación de secretos, threat modeling de prompt injection y monitoreo de regresiones. Debe tratar prompts como artefactos productivos, no texto casual.',
      'Transferencia de ingeniería de software a prompts.', 'Editar prompts críticos sin pruebas ni control de cambios.', 'optimización de prompts guiada por evaluación y held-out', 'data/teoria/gen-eval4.md; Optimización de prompts dirigida por evaluación', 'Si un prompt controla producción, necesita pruebas y revisión como código.'),
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
console.log(`OK: eval ampliado manualmente (${summary})`);

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
