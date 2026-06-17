import { readFileSync, writeFileSync } from 'node:fs';

const path = 'data/genai/_unidades.json';
const doc = JSON.parse(readFileSync(path, 'utf8'));

const additions = {
  'gen-resp1': [
    mc('grs1-q5', 'easy', '¿Qué dimensión falta si solo reportas accuracy global en un sistema de alto impacto?',
      'El desempeño y daño por grupo, además de equidad, privacidad y rendición de cuentas.',
      ['El desempeño y daño por grupo, además de equidad, privacidad y rendición de cuentas.', 'La cantidad de tokens del prompt usado para inferencia.', 'La temperatura exacta del muestreo durante la demo.', 'El nombre comercial del proveedor del modelo.'],
      'Evalúa por qué el promedio global oculta daños.', 'Tomar accuracy global como autorización de despliegue.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si una decisión afecta oportunidades, mira segmentos y daños, no solo promedio.'),
    mc('grs1-q6', 'medium', '¿Por qué el código postal puede mantener sesgo aunque quites raza o etnia?',
      'Porque funciona como proxy correlacionado con el atributo protegido.',
      ['Porque funciona como proxy correlacionado con el atributo protegido.', 'Porque todo código postal es una etiqueta humana incorrecta.', 'Porque SHAP elimina automáticamente variables sensibles.', 'Porque la paridad demográfica siempre se cumple al quitar columnas.'],
      'Reconoce proxies y fracaso de fairness through unawareness.', 'Creer que esconder la variable sensible borra la señal.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si otra variable reconstruye el atributo protegido, el sesgo sigue disponible.'),
    mc('grs1-q7', 'hard', '¿Qué implica que paridad demográfica y calibración puedan ser incompatibles?',
      'Que elegir una noción de equidad exige justificar tradeoffs del contexto.',
      ['Que elegir una noción de equidad exige justificar tradeoffs del contexto.', 'Que ningún sistema debe medir equidad por grupos.', 'Que la accuracy global resuelve automáticamente el conflicto.', 'Que basta usar SHAP para cumplir todas las definiciones.'],
      'Evalúa equidad como decisión sociotécnica con tradeoffs.', 'Buscar una definición universal de justicia sin contexto.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si dos métricas de justicia chocan, la decisión debe explicarse y gobernarse.'),
    mc('grs1-q8', 'medium', '¿Qué limita una explicación post-hoc como LIME o SHAP?',
      'Aproxima el comportamiento local del modelo, pero no prueba la causa real de la decisión.',
      ['Aproxima el comportamiento local del modelo, pero no prueba la causa real de la decisión.', 'Garantiza interpretabilidad completa en cualquier modelo de alto riesgo.', 'Elimina la necesidad de modelos interpretables en salud o crédito.', 'Corrige sesgos de entrenamiento sin cambiar datos ni objetivo.'],
      'Distingue explicación útil de razón causal garantizada.', 'Confundir explicación post-hoc con verdad interna del modelo.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si la decisión es crítica, una aproximación explicativa puede no bastar.'),
    mc('grs1-q9', 'hard', '¿Qué origen de sesgo captura una etiqueta histórica “aprobado/rechazado” producida por humanos sesgados?',
      'Sesgo en etiquetas: el modelo aprende decisiones humanas injustas como verdad.',
      ['Sesgo en etiquetas: el modelo aprende decisiones humanas injustas como verdad.', 'Sesgo solo en infraestructura, sin relación con datos.', 'Sesgo por temperatura de inferencia demasiado baja.', 'Sesgo por usar una métrica semántica con referencia.'],
      'Identifica etiquetas como fuente de sesgo, no solo features.', 'Auditar solo columnas sensibles y olvidar cómo se generaron las etiquetas.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si el pasado etiquetó injustamente, el modelo puede automatizar esa injusticia.'),
    mc('grs1-q10', 'medium', '¿Qué pregunta expresa rendición de cuentas en IA responsable?',
      'Quién responde, corrige y ofrece recurso si el sistema causa daño.',
      ['Quién responde, corrige y ofrece recurso si el sistema causa daño.', 'Cuántos parámetros tiene el modelo base.', 'Qué embedding tiene mayor similitud coseno.', 'Qué prompt produce la respuesta más larga.'],
      'Ubica accountability como dueño y recurso ante daño.', 'Desplegar sin responsable claro porque la métrica técnica es alta.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si alguien afectado no sabe a quién apelar, falta accountability.'),
    mc('grs1-q11', 'hard', '¿Por qué una métrica de equidad puede dañar al grupo que busca proteger?',
      'Porque forzar una definición puede empeorar resultados relevantes en ese contexto.',
      ['Porque forzar una definición puede empeorar resultados relevantes en ese contexto.', 'Porque medir por grupo siempre está prohibido legalmente.', 'Porque los modelos interpretables no pueden ser justos.', 'Porque toda explicación post-hoc introduce privacidad diferencial.'],
      'Reconoce consecuencias de tradeoffs de equidad.', 'Aplicar una noción de justicia sin analizar efectos reales.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si una restricción cambia decisiones, mide también daños y beneficios por grupo.'),
    mc('grs1-q12', 'medium', '¿Qué práctica convierte “precisión no basta” en ingeniería verificable?',
      'Auditar segmentos, daños, privacidad, interpretabilidad y responsables antes del despliegue.',
      ['Auditar segmentos, daños, privacidad, interpretabilidad y responsables antes del despliegue.', 'Elegir el modelo más grande disponible para subir accuracy.', 'Eliminar del reporte toda métrica que no sea desempeño global.', 'Pedir al LLM que declare que su respuesta es ética.'],
      'Convierte principios responsables en checklist técnico-operativo.', 'Tratar ética como declaración textual sin evidencia.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si el riesgo puede afectar personas, tradúcelo a auditorías y dueños.'),
    open('grs1-s3', 'scenario', 'hard', 'Escenario: un modelo de contratación no usa género, pero penaliza carreras, huecos laborales y clubes correlacionados con mujeres. ¿Cómo lo auditas?',
      'Mediría resultados por grupo, buscaría proxies correlacionados, auditaría etiquetas históricas, compararía definiciones de equidad relevantes y revisaría explicaciones con cautela. Quitar género no basta; hay que demostrar que el sistema no reproduce daño.',
      'Aplica proxies y sesgo histórico a contratación.', 'Declarar justo un modelo porque eliminó la columna sensible.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si features sustituyen al atributo protegido, audita correlaciones y resultados.'),
    open('grs1-s4', 'scenario', 'medium', 'Escenario: un hospital quiere usar un modelo opaco para priorizar pacientes porque supera en accuracy a uno interpretable. ¿Qué preguntas harías antes de aprobarlo?',
      'Preguntaría el impacto por subgrupo, el costo de errores, necesidad legal/clinica de explicación, mecanismos de apelación, privacidad, robustez y si el aumento de accuracy justifica perder interpretabilidad en una decisión de alto riesgo.',
      'Evalúa accuracy versus interpretabilidad en alto impacto.', 'Aceptar caja negra crítica solo porque mejora un promedio.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'A más consecuencia humana, más exigencia de explicación y accountability.'),
    open('grs1-r3', 'reflexion', 'medium', 'Elige una decisión automatizada que te afectaría personalmente. ¿Qué explicación y recurso exigirías?',
      'Debe nombrar qué información necesitaría la persona afectada, cómo impugnar la decisión, qué humano responde y qué datos o criterios no deberían usarse. La respuesta conecta transparencia con poder real de corrección.',
      'Reflexión desde la posición de la persona afectada.', 'Pensar en explicabilidad solo como herramienta para ingenieros.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si tú sufrirías la decisión, define qué necesitarías para entenderla y apelarla.'),
    open('grs1-r4', 'reflexion', 'hard', 'Diseña una reunión para elegir una definición de equidad. ¿Quién debe estar y qué evidencia debe llevar?',
      'Una respuesta fuerte incluye técnicos, negocio, legal, dominio, usuarios afectados o representantes, y evidencia: métricas por grupo, costos de falsos positivos/negativos, restricciones legales, alternativas y riesgo residual documentado.',
      'Equidad como decisión sociotécnica gobernada.', 'Dejar que un solo equipo elija la métrica de justicia sin stakeholders.', 'IA responsable: equidad, transparencia, privacidad y rendición de cuentas', 'data/teoria/gen-resp1.md; IA responsable: sesgo, equidad, transparencia y rendición de cuentas', 'Si hay tradeoff normativo, la decisión requiere datos y legitimidad, no solo cálculo.'),
  ],

  'gen-resp2': [
    mc('grs2-q5', 'easy', '¿Qué función del NIST AI RMF identifica contexto y riesgos del sistema?',
      'Map.',
      ['Map.', 'Softmax.', 'BLEU.', 'PPO.'],
      'Recupera las funciones del AI RMF.', 'Confundir funciones de gobierno con métricas de NLP.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Cuando el trabajo es entender uso, contexto y riesgos, estás en Map.'),
    mc('grs2-q6', 'medium', '¿Qué función del AI RMF asegura roles, políticas y rendición de cuentas?',
      'Govern.',
      ['Govern.', 'Retrieve.', 'Decode.', 'Tokenize.'],
      'Ubica gobernanza como capa que envuelve el proceso.', 'Tratar gobierno como documentación posterior al despliegue.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si no hay dueño ni política, el riesgo no está gobernado.'),
    mc('grs2-q7', 'medium', '¿Qué aporta MITRE ATLAS que no aporta por sí solo el AI RMF?',
      'Un catálogo de tácticas y técnicas de ataque contra sistemas de IA.',
      ['Un catálogo de tácticas y técnicas de ataque contra sistemas de IA.', 'Una función de pérdida para entrenar transformers.', 'Una métrica universal de equidad sin tradeoffs.', 'Un reemplazo automático de auditorías humanas.'],
      'Distingue proceso de gestión de riesgo frente a mapa de amenazas.', 'Usar un marco de proceso como si listara ataques concretos.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si preguntas “qué ataques existen”, ATLAS complementa al RMF.'),
    mc('grs2-q8', 'hard', '¿Qué convierte un risk register en operativo y no decorativo?',
      'Dueño, control, métrica, umbral, evidencia y cadencia de revisión.',
      ['Dueño, control, métrica, umbral, evidencia y cadencia de revisión.', 'Una lista larga de riesgos sin responsables ni pruebas.', 'Un PDF aprobado por el comité y nunca revisado.', 'Un prompt que prometa cumplir todos los frameworks.'],
      'Evalúa aplicación real de frameworks.', 'Confundir documentación con control ejecutado.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si no puedes mostrar evidencia y dueño, el riesgo sigue escrito, no gestionado.'),
    mc('grs2-q9', 'hard', '¿Qué significa AI Secure-by-Design en el ciclo de vida?',
      'Seguridad, ética y gobernanza se integran desde diseño hasta retiro, no al final.',
      ['Seguridad, ética y gobernanza se integran desde diseño hasta retiro, no al final.', 'La seguridad se añade con un prompt de sistema antes de lanzar.', 'El modelo se vuelve seguro solo por usar RAG.', 'La auditoría se omite si el proveedor es reconocido.'],
      'Recupera secure-by-design como postura de ciclo completo.', 'Parchear seguridad al final como trámite.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si seguridad aparece tarde, no es secure-by-design.'),
    mc('grs2-q10', 'medium', '¿Para qué usarías la MIT AI Risk Taxonomy al hacer Map?',
      'Como checklist amplio para no olvidar categorías de riesgo de IA.',
      ['Como checklist amplio para no olvidar categorías de riesgo de IA.', 'Como herramienta para ejecutar ataques de evasión automáticamente.', 'Como algoritmo para elegir el siguiente token.', 'Como sustituto de medir sesgo o privacidad.'],
      'Ubica la taxonomía como catálogo anti-puntos-ciegos.', 'Creer que una taxonomía reemplaza mediciones reales.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si estás mapeando riesgos, una taxonomía evita olvidar clases completas.'),
    mc('grs2-q11', 'hard', '¿Cuál es el riesgo de usar un framework como escudo de responsabilidad?',
      'Cumplir formalmente mientras el sistema conserva daños no medidos ni gestionados.',
      ['Cumplir formalmente mientras el sistema conserva daños no medidos ni gestionados.', 'Medir demasiadas métricas por componente antes de desplegar.', 'Asignar dueños claros a riesgos de alto impacto.', 'Documentar riesgo residual y monitoreo continuo.'],
      'Reconoce teatro de gobernanza.', 'Pensar que nombrar el framework equivale a reducir el riesgo.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si el papel dice cumplir pero los daños persisten, el framework se volvió teatro.'),
    mc('grs2-q12', 'medium', '¿Cómo encajan AI RMF, ATLAS y Risk Taxonomy en un asistente clínico RAG?',
      'AI RMF da proceso; ATLAS amenazas técnicas; Taxonomy categorías de riesgo a mapear.',
      ['AI RMF da proceso; ATLAS amenazas técnicas; Taxonomy categorías de riesgo a mapear.', 'ATLAS decide equidad, AI RMF genera embeddings y Taxonomy ejecuta prompts.', 'Los tres reemplazan evaluación clínica y revisión humana.', 'Solo sirven si el sistema no usa documentos privados.'],
      'Integra frameworks complementarios en un caso real.', 'Confundir frameworks o tratarlos como competidores.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si ves proceso, amenazas y catálogo, cada framework tiene un rol distinto.'),
    open('grs2-s3', 'scenario', 'hard', 'Escenario: tu risk register lista “alucinación médica” pero no tiene dueño, control ni umbral. ¿Cómo lo conviertes en Govern/Measure/Manage?',
      'Asignaría dueño clínico/técnico, control de abstención y revisión humana, métrica de unsupported claims, umbral de bloqueo, set de evaluación, cadencia de monitoreo y plan de respuesta. Así pasa de riesgo escrito a riesgo gestionado.',
      'Operacionaliza un riesgo concreto con evidencia.', 'Dejar un riesgo crítico en una lista sin acción verificable.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si un riesgo no tiene dueño y métrica, no está bajo gestión.'),
    open('grs2-s4', 'scenario', 'medium', 'Escenario: seguridad solo revisa el agente una semana antes del lanzamiento y exige bloquear herramientas peligrosas. ¿Qué falla de Secure-by-Design ves?',
      'Seguridad llegó tarde. Secure-by-Design exige diseñar herramientas, permisos, datos, evaluaciones y aprobaciones desde el encuadre, con legal/seguridad/negocio participando antes de construir la arquitectura.',
      'Aplica secure-by-design a timing y ciclo de vida.', 'Tratar seguridad como gate final en vez de restricción de diseño.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si rediseñar al final cuesta demasiado, debió discutirse al inicio.'),
    open('grs2-r3', 'reflexion', 'medium', 'Elige un sistema de IA. Escribe un riesgo para cada función AI RMF: Govern, Map, Measure y Manage.',
      'Debe separar gobierno, identificación, medición y tratamiento. Una buena respuesta asigna dueño, contexto de uso, métrica verificable y acción de mitigación, mostrando que el framework estructura trabajo real.',
      'Reflexión sobre AI RMF como proceso completo.', 'Reducir el framework a una lista de deseos sin acciones.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si puedes mapear cada riesgo a función y evidencia, el marco está vivo.'),
    open('grs2-r4', 'reflexion', 'hard', '¿Qué señales te dirían que una organización usa frameworks como teatro de gobernanza?',
      'Debe mencionar ausencia de dueños, métricas no revisadas, controles sin pruebas, riesgo residual no aceptado explícitamente, comités sin poder y reportes que no cambian decisiones. También debe proponer auditorías de evidencia.',
      'Reflexión sobre diferencia entre cumplimiento formal y control real.', 'Equivaler madurez con cantidad de documentos aprobados.', 'frameworks de gobernanza de IA, AI RMF, Secure-by-Design y ATLAS', 'data/teoria/gen-resp2.md; Frameworks para gobernar la IA: NIST AI RMF, Secure-by-Design, ATLAS', 'Si un framework no cambia decisiones ni muestra evidencia, probablemente es teatro.'),
  ],

  'gen-resp3': [
    mc('grs3-q5', 'easy', '¿Qué reto de producción aparece cuando cada llamada al LLM cuesta dinero?',
      'Costo a escala, que se controla con caché, límites, routing y modelos más pequeños.',
      ['Costo a escala, que se controla con caché, límites, routing y modelos más pequeños.', 'Equidad demográfica, que se resuelve con temperatura alta.', 'Tokenización BPE, que elimina latencia automáticamente.', 'BLEU bajo, que siempre prueba alucinación factual.'],
      'Recupera costo como restricción operativa.', 'Ignorar costo porque la demo tiene poco tráfico.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si multiplicas llamadas por usuarios, el costo define viabilidad.'),
    mc('grs3-q6', 'medium', '¿Qué métrica de latencia suele importar más que el promedio?',
      'p95 o p99 de latencia, porque captura colas lentas que sufren usuarios reales.',
      ['p95 o p99 de latencia, porque captura colas lentas que sufren usuarios reales.', 'Número de parámetros del modelo proveedor.', 'Cantidad de documentos en el índice aunque no se consulten.', 'Longitud del nombre del prompt en el repositorio.'],
      'Evalúa latencia operacional con colas, no solo media.', 'Reportar promedio y ocultar respuestas extremadamente lentas.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si unos usuarios esperan 20s, el promedio puede esconderlo.'),
    mc('grs3-q7', 'medium', '¿Qué habilita el tracing en un agente de producción?',
      'Reconstruir herramientas llamadas, observaciones, costos y pasos que llevaron a una salida.',
      ['Reconstruir herramientas llamadas, observaciones, costos y pasos que llevaron a una salida.', 'Eliminar toda necesidad de evaluación continua.', 'Cambiar pesos del modelo sin despliegue.', 'Garantizar que no existan datos personales en logs.'],
      'Conecta observabilidad con depuración de cadenas LLM.', 'No registrar trazas y depender de quejas de usuarios.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si no puedes reconstruir una respuesta mala, no puedes arreglarla bien.'),
    mc('grs3-q8', 'hard', '¿Por qué un cambio del proveedor puede romper tu sistema aunque no cambies código?',
      'Porque el modelo servido puede cambiar comportamiento, formato, seguridad o calidad.',
      ['Porque el modelo servido puede cambiar comportamiento, formato, seguridad o calidad.', 'Porque los prompts dejan de ser texto y se vuelven embeddings privados.', 'Porque RAG elimina la dependencia del modelo base.', 'Porque la latencia ya no se puede medir después del cambio.'],
      'Recupera dependencia externa y necesidad de versionado.', 'Asumir que un endpoint de modelo es estable para siempre.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si el proveedor cambia el modelo, re-evalúa como si fuera una dependencia nueva.'),
    mc('grs3-q9', 'hard', '¿Qué dispara re-evaluación según la regla de producción?',
      'Cualquier cambio de prompt, modelo, corpus, herramienta o política de recuperación.',
      ['Cualquier cambio de prompt, modelo, corpus, herramienta o política de recuperación.', 'Solo cambios visibles en el CSS de la aplicación.', 'Únicamente aumentos de accuracy reportados por el proveedor.', 'Nada después del lanzamiento inicial si la demo funcionó.'],
      'Evalúa evaluación continua como CI de calidad.', 'Cambiar piezas del sistema sin medir regresiones.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si una dependencia cambia, corre el set antes de confiar.'),
    mc('grs3-q10', 'medium', '¿Qué control ayuda tanto a costo como a latencia para consultas repetidas?',
      'Caché de respuestas o de pasos recuperados cuando sea seguro hacerlo.',
      ['Caché de respuestas o de pasos recuperados cuando sea seguro hacerlo.', 'Aumentar siempre el número de agentes y reintentos.', 'Eliminar límites por usuario para evitar fricción.', 'Usar el modelo más grande para toda consulta trivial.'],
      'Reconoce caché como control operacional.', 'Resolver costo con más capacidad sin reducir trabajo repetido.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si muchas consultas repiten trabajo, cachear reduce llamadas y espera.'),
    mc('grs3-q11', 'hard', '¿Qué relación tiene GenAI en producción con Fase 8 de seguridad?',
      'Debe aplicar entradas no confiables, mínimos permisos, secretos fuera de prompts, cuotas y red team.',
      ['Debe aplicar entradas no confiables, mínimos permisos, secretos fuera de prompts, cuotas y red team.', 'La seguridad ya no aplica porque las salidas son lenguaje natural.', 'Basta con filtrar palabras ofensivas en la respuesta final.', 'RAG garantiza control de acceso y ausencia de inyección por defecto.'],
      'Integra controles de seguridad al despliegue GenAI.', 'Tratar seguridad como capa separada del sistema LLM.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si hay usuarios, datos y herramientas reales, aplica amenazas de Fase 8.'),
    mc('grs3-q12', 'medium', '¿Qué diferencia un demo de un sistema confiable?',
      'SLOs, monitoreo, límites, fallback, versionado, evaluación continua y respuesta a incidentes.',
      ['SLOs, monitoreo, límites, fallback, versionado, evaluación continua y respuesta a incidentes.', 'Una presentación con tres casos felices y capturas bonitas.', 'Un prompt largo que diga “sé confiable” al inicio.', 'Una sola ejecución manual revisada por el equipo fundador.'],
      'Resume producción como operación verificable.', 'Confundir funcionamiento puntual con confiabilidad sostenida.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si no hay SLO, logs y eval continua, aún estás cerca de demo.'),
    open('grs3-s3', 'scenario', 'hard', 'Escenario: el proveedor depreca tu modelo en 30 días. Tu asistente regula respuestas legales. ¿Cuál es el plan responsable?',
      'Congelaría el estado actual, elegiría candidatos de reemplazo, correría suite held-out y adversaria, compararía faithfulness/latencia/costo, revisaría prompts y formatos, prepararía rollback, comunicaría riesgo residual y no migraría sin aprobación.',
      'Aplica migración de dependencia crítica con evaluación.', 'Cambiar de modelo el último día y confiar en la compatibilidad.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si cambia una dependencia crítica, trata la migración como release de alto riesgo.'),
    open('grs3-s4', 'scenario', 'medium', 'Escenario: soporte reporta quejas de alucinación, pero no hay trazas de prompts, documentos recuperados ni versión de modelo. ¿Qué deuda operacional aparece?',
      'Falta observabilidad y versionado. Sin trazas no puedes separar recuperación, prompt, modelo o datos; debes instrumentar logging seguro, IDs de versión, contexto recuperado, métricas de calidad y alertas de regresión.',
      'Diagnostica producción sin visibilidad.', 'Intentar arreglar a mano casos aislados sin datos operativos.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si no puedes ver el camino de la respuesta, el fallo no es depurable.'),
    open('grs3-r3', 'reflexion', 'medium', 'Define tres SLOs para un producto GenAI que usarías cada día. ¿Qué alertas pondrías?',
      'Debe incluir calidad, latencia/costo y fiabilidad o seguridad: por ejemplo eval score, p95 latency, error rate, costo por tarea, unsupported claims o unsafe pass rate. Cada alerta debe tener umbral y acción.',
      'Reflexión sobre SLOs y alertas accionables.', 'Monitorear métricas vanidosas sin umbrales ni respuesta.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si una alerta no dispara acción, probablemente no es un SLO útil.'),
    open('grs3-r4', 'reflexion', 'hard', 'Diseña un runbook para una regresión silenciosa de calidad tras cambiar corpus RAG.',
      'Una respuesta fuerte incluye detección por eval continua, congelar despliegue, comparar antes/después, revisar documentos modificados, reproducir trazas fallidas, rollback o hotfix, comunicación a dueños y nueva prueba antes de liberar.',
      'Transferencia de incident response a calidad GenAI.', 'Corregir documentos al azar sin reproducir ni contener el impacto.', 'GenAI en producción: observabilidad, versiones, costo y evaluación continua', 'data/teoria/gen-resp3.md; GenAI en producción: del prototipo al sistema confiable', 'Si la calidad cae sin error visible, trata la evaluación como detector de incidente.'),
  ],

  'gen-resp4': [
    mc('grs4-q5', 'easy', '¿Qué pieza conviene para clasificar sentimiento en reseñas de smartwatch?',
      'Clasificación/análisis con LLM y evaluación rigurosa, no un agente.',
      ['Clasificación/análisis con LLM y evaluación rigurosa, no un agente.', 'Sistema multi-agente con debate y herramientas financieras.', 'RAG agéntico sobre regulación europea.', 'Agente autónomo que compra inventario.'],
      'Mapea problema simple de texto a pieza simple.', 'Usar arquitectura agéntica para clasificación acotada.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si la tarea es clasificar/extraer, empieza simple y mide.'),
    mc('grs4-q6', 'medium', '¿Qué pieza encaja con un asistente de pólizas de seguros?',
      'RAG con atribución y evaluación de fidelidad a documentos.',
      ['RAG con atribución y evaluación de fidelidad a documentos.', 'Policy gradient para aprender preferencias de inversión.', 'Debate multi-agente sin fuentes ni citas.', 'Clasificador simple sin acceso a pólizas.'],
      'Reconoce conocimiento propio documental como señal de RAG.', 'Responder sobre documentos privados sin recuperación ni citas.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si la respuesta depende de pólizas, necesitas recuperar y citar pólizas.'),
    mc('grs4-q7', 'medium', '¿Qué señal justifica pasar de RAG a agente?',
      'La solución debe decidir pasos y ejecutar acciones según observaciones.',
      ['La solución debe decidir pasos y ejecutar acciones según observaciones.', 'La respuesta necesita citar un documento único.', 'La tarea es etiquetar sentimiento de textos cortos.', 'La métrica ROUGE bajó en un resumen offline.'],
      'Distingue conocimiento externo de acción multi-paso.', 'Usar agente cuando solo faltaba recuperar información.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si el sistema actúa y reacciona, evalúa agente; si solo responde con documentos, RAG.'),
    mc('grs4-q8', 'hard', '¿Qué condición justifica multi-agente en legal o inteligencia regulatoria?',
      'Tarea grande, divisible por fuentes/roles, y mejora medida frente a agente simple.',
      ['Tarea grande, divisible por fuentes/roles, y mejora medida frente a agente simple.', 'Deseo de mostrar una arquitectura compleja en la demo.', 'Una pregunta de una sola póliza con respuesta directa.', 'Necesidad de evitar toda evaluación por componente.'],
      'Aplica complejidad justificada por métrica.', 'Elegir multi-agente por moda o prestigio técnico.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si roles y fuentes se separan naturalmente, prueba multi-agente contra baseline.'),
    mc('grs4-q9', 'hard', '¿Qué hace que “fidelidad, atribución y responsabilidad” sean el producto en finanzas?',
      'Una respuesta falsa puede causar pérdidas, incumplimiento y responsabilidad legal.',
      ['Una respuesta falsa puede causar pérdidas, incumplimiento y responsabilidad legal.', 'El usuario siempre prefiere respuestas largas aunque no citen fuentes.', 'Las finanzas no requieren control de acceso documental.', 'La demo sustituye consistency checks si el tono es seguro.'],
      'Conecta consecuencia del dominio con controles estrictos.', 'Tratar anti-alucinación como extra cosmético.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'A más daño potencial, más evidencia, citas y aprobación.'),
    mc('grs4-q10', 'medium', '¿Qué salvaguarda corresponde a supply chain si el agente genera órdenes de compra?',
      'Agencia mínima y humano en el lazo para órdenes sensibles o irreversibles.',
      ['Agencia mínima y humano en el lazo para órdenes sensibles o irreversibles.', 'Permiso autónomo ilimitado para acelerar compras.', 'Eliminar logs para no exponer proveedores.', 'Usar solo sentimiento de reseñas como métrica.'],
      'Aplica controles de agentes a acciones de negocio.', 'Automatizar compras sin umbrales ni aprobación.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si el sistema emite órdenes reales, separa propuesta de ejecución.'),
    mc('grs4-q11', 'hard', '¿Cuándo la arquitectura correcta puede ser “no usar IA generativa”?',
      'Cuando la decisión es de alto impacto y no puede hacerse auditable, explicable o segura.',
      ['Cuando la decisión es de alto impacto y no puede hacerse auditable, explicable o segura.', 'Cuando el equipo quiere evitar escribir prompts largos.', 'Cuando hay documentos propios que podrían usarse con RAG.', 'Cuando una clasificación simple tiene un dataset evaluable.'],
      'Recupera el caso borde responsable: no desplegar.', 'Forzar GenAI aunque el riesgo no sea gobernable.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si no puedes auditar ni controlar el daño, apoyo humano o no usar IA puede ser correcto.'),
    mc('grs4-q12', 'medium', '¿Qué significa “la pieza más simple que resuelva” en un caso vertical?',
      'Elegir clasificación, RAG, agente o multi-agente por necesidad medible, no por moda.',
      ['Elegir clasificación, RAG, agente o multi-agente por necesidad medible, no por moda.', 'Usar siempre la arquitectura más reciente aunque el baseline gane.', 'Evitar evaluación para no limitar creatividad del sistema.', 'Empezar por multi-agente y retirar piezas solo si falla.'],
      'Resume el criterio transversal de arquitectura GenAI.', 'Confundir sofisticación con ajuste al problema.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si una pieza simple cumple métricas, la complejidad extra debe justificarse.'),
    open('grs4-s3', 'scenario', 'hard', 'Escenario: en legal, un equipo propone un único RAG fijo para comparar regulaciones de varios países y producir un informe auditado. ¿Qué arquitectura evaluarías?',
      'Evaluaría RAG agéntico o multi-agente con routing por jurisdicción/fuente, revisor de fidelidad, atribución por afirmación y comparación contra un baseline RAG fijo. La decisión depende de task success, costo, latencia y auditoría.',
      'Aplica arquitectura por complejidad divisible y fuentes múltiples.', 'Usar una búsqueda cruda única para un problema legal multi-fuente.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si el caso tiene jurisdicciones y fuentes distintas, descompón y mide.'),
    open('grs4-s4', 'scenario', 'medium', 'Escenario: e-commerce quiere recomendaciones personalizadas con historial, carrito y clics. ¿Qué riesgos responsables añadirías al plan?',
      'Añadiría privacidad y minimización de datos, sesgo de exposición, métricas de conversión junto a satisfacción/retención, explicación básica de personalización y límites para no manipular ni discriminar segmentos.',
      'Integra caso de negocio con privacidad y sesgo.', 'Optimizar conversión sin mirar privacidad, equidad ni daño al usuario.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si personalizas con datos conductuales, privacidad y sesgo son parte del diseño.'),
    open('grs4-r3', 'reflexion', 'medium', 'Elige un vertical y escribe un baseline simple antes de tu arquitectura GenAI ideal. ¿Qué tendría que superar?',
      'Debe definir un baseline concreto, métrica de negocio, calidad, costo y riesgo. La respuesta fuerte explica qué mejora mínima justificaría RAG, agente o multi-agente frente a una solución más simple.',
      'Reflexión sobre baseline como disciplina arquitectónica.', 'Diseñar la solución ideal sin comparación contra alternativa simple.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si no sabes qué debe superar, no sabes si la complejidad vale.'),
    open('grs4-r4', 'reflexion', 'hard', 'Diseña el proyecto final para un caso sensible: arquitectura, evaluación, gobierno, seguridad y operación.',
      'Una respuesta excelente incluye problema, stakeholders, pieza elegida, arquitectura, baseline, métricas de calidad/negocio/seguridad, risk register, controles de acceso, atribución, humano en el lazo, SLOs, monitoreo y rollback.',
      'Síntesis final de toda Fase 9 aplicada a negocio real.', 'Presentar una demo funcional sin evaluación, gobierno ni operación.', 'selección de arquitectura GenAI por vertical y métrica', 'data/teoria/gen-resp4.md; Casos por vertical: aplicar GenAI a problemas reales de negocio', 'Si es proyecto final, debe probar valor, riesgo y operación, no solo una respuesta bonita.'),
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
console.log(`OK: responsable ampliado manualmente (${summary})`);

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
