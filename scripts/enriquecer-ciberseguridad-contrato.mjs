#!/usr/bin/env node
// Enriquece la Fase 8 para cumplir el contrato de ciberseguridad.md:
// - metadata de lección: level/difficulty, external_lab, portfolio_task
// - campos auditables por pregunta: type/prompt/answer/feedback/concept/source_reference/common_mistake/recognition_signal
// - mínimo por lección: 10 quiz easy, 10 quiz medium, 10 quiz hard, 5 scenarios, 5 reflexiones
// - diagnóstico inicial, laboratorios vivos y estándar curricular "MIT+" por cluster
//
// Idempotente: elimina sólo las preguntas generadas por este script antes de regenerar.

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const uniPath = join(ROOT, 'data', 'ciberseguridad', '_unidades.json');
const taxPath = join(ROOT, 'data', 'ciberseguridad', '_taxonomia.json');
const GENERATED_BY = 'enriquecer-ciberseguridad-contrato-v1';

const unidadesDoc = JSON.parse(readFileSync(uniPath, 'utf8'));
const taxDoc = JSON.parse(readFileSync(taxPath, 'utf8'));

const LEVEL_BY_NUM = { 1: 'intro', 2: 'core', 3: 'advanced' };
const DIFF_BY_LEVEL = { intro: 'easy', core: 'medium', advanced: 'hard', arena: 'hard' };

const LABS_BY_CLUSTER = {
  'cyber-mindset': [
    ['NIST Cybersecurity Framework', 'https://www.nist.gov/cyberframework', 'mapear Identify/Protect/Detect/Respond/Recover a un sistema de datos propio', 'explicar el mapa de funciones con un activo y un control por función'],
  ],
  'cyber-systems-crypto': [
    ['OverTheWire Bandit', 'https://overthewire.org/wargames/bandit/', 'practicar permisos, archivos y credenciales en un entorno autorizado', 'llegar al nivel 5 explicando el supuesto de seguridad de cada paso'],
    ['picoCTF Practice', 'https://play.picoctf.org/practice', 'resolver retos introductorios de criptografía/redes/forensics', 'explicar qué propiedad de seguridad se rompía y qué control la habría protegido'],
  ],
  'cyber-web-api': [
    ['PortSwigger Web Security Academy', 'https://portswigger.net/web-security', 'estudiar el patrón defensivo de vulnerabilidades web y APIs', 'resolver o revisar un laboratorio apprentice y escribir la mitigación robusta'],
    ['PortSwigger All Labs', 'https://portswigger.net/web-security/all-labs', 'seleccionar labs de SQLi, XSS, access control, CORS, SSRF o file upload', 'documentar frontera de confianza, impacto y control por lab'],
    ['OWASP Juice Shop', 'https://owasp.org/www-project-juice-shop/', 'practicar auditoría defensiva en una app deliberadamente vulnerable', 'producir un reporte de hallazgo, impacto y mitigación'],
  ],
  'cyber-data-privacy': [
    ['NIST Privacy Framework', 'https://www.nist.gov/privacy-framework', 'mapear Identify-P, Govern-P, Control-P y Communicate-P a un dataset', 'justificar minimización, finalidad, acceso, retención y comunicación'],
  ],
  'cyber-secure-dev': [
    ['OpenSSF Training', 'https://openssf.org/training/courses/', 'revisar desarrollo seguro, supply chain, secrets, SAST/SCA y respuesta a vulnerabilidades', 'definir una política de secretos, dependencias y parcheo verificable'],
  ],
  'cyber-blue-team': [
    ['MITRE ATT&CK', 'https://attack.mitre.org', 'mapear tácticas/técnicas a logs y detecciones', 'explicar qué evidencia confirmaría o descartaría una técnica'],
    ['CyberDefenders', 'https://cyberdefenders.org/blueteam-ctf-challenges/', 'investigar escenarios blue team con logs y artefactos', 'producir línea de tiempo, hipótesis y acción de contención'],
    ['Blue Team Labs Online', 'https://blueteamlabs.online/', 'practicar investigaciones de incident response, forensics y threat hunting', 'documentar hallazgos y brechas de cobertura'],
    ['KC7 Cyber', 'https://kc7cyber.com/', 'resolver investigaciones guiadas con consultas y evidencia', 'transformar consultas en hipótesis defensivas y detecciones candidatas'],
  ],
  'cyber-ml-security': [
    ['MITRE ATLAS', 'https://atlas.mitre.org', 'mapear técnicas contra sistemas de IA a entrenamiento, inferencia y supply chain', 'proponer control, señal de monitoreo y riesgo residual por técnica'],
  ],
  'cyber-llm-rag-agents': [
    ['OWASP GenAI Security Project', 'https://genai.owasp.org/', 'revisar guías de seguridad GenAI, agentic apps y red teaming', 'convertir riesgos en controles para un asistente realista'],
    ['OWASP LLM Top 10', 'https://genai.owasp.org/llm-top-10/', 'recorrer LLM01-LLM10 con foco en mitigaciones', 'definir una prueba adversarial segura por riesgo relevante'],
  ],
};

const CLUSTER_COMPETENCIAS = {
  'cyber-mindset': [
    'Nombrar activos, amenazas, vulnerabilidades, impacto y controles sin caer en lenguaje teatral.',
    'Construir threat models que localicen supuestos de confianza rotos.',
    'Razonar seguridad como economía, incentivos, factor humano y riesgo residual.',
    'Comunicar decisiones defensivas con tradeoffs entendibles para producto, datos e ingeniería.',
  ],
  'cyber-systems-crypto': [
    'Leer sistemas como composición de procesos, permisos, red, identidad y límites de confianza.',
    'Distinguir hash, cifrado, MAC, firma, TLS y sesión por la propiedad que garantizan.',
    'Detectar cuándo un control de red no protege endpoints, secretos o autorización.',
    'Elegir aislamiento proporcional para notebooks, jobs, contenedores y servicios de inferencia.',
  ],
  'cyber-web-api': [
    'Reconocer dato tratado como instrucción en SQLi, XSS, SSRF, deserialización y LLM output handling.',
    'Auditar autenticación, autorización por recurso, sesión, JWT/OAuth y APIs desde el servidor.',
    'Elegir mitigaciones robustas: parametrizar, codificar, allow-list, rate limit y control de acceso.',
    'Traducir vulnerabilidades web a riesgos de dashboards, APIs de modelos y sistemas RAG.',
  ],
  'cyber-data-privacy': [
    'Separar seguridad, privacidad, cumplimiento y daño a individuos.',
    'Evaluar minimización, finalidad, reidentificación, retención, acceso y auditoría antes de entrenar.',
    'Diseñar gobernanza de datasets y modelos con tradeoff utilidad-privacidad explícito.',
    'Comunicar riesgos de privacidad sin prometer anonimización falsa.',
  ],
  'cyber-secure-dev': [
    'Convertir seguridad en requisitos, diseño, revisión, pruebas y respuesta, no en parche final.',
    'Controlar secretos, dependencias, SBOM/SCA, SAST, fuzzing, CI/CD y contenedores.',
    'Priorizar vulnerabilidades por explotabilidad, exposición, impacto y capacidad de parcheo.',
    'Asegurar pipelines ML y notebooks como software productivo, no como experimentos aislados.',
  ],
  'cyber-blue-team': [
    'Mapear comportamiento adversario a tácticas, técnicas, logs, hipótesis y reglas de detección.',
    'Distinguir evento, alerta, incidente, indicador y evidencia faltante.',
    'Diseñar detecciones calibradas con línea base, falsos positivos, cobertura y respuesta.',
    'Cerrar el ciclo emular, medir, mejorar con práctica autorizada y post-mortems sin culpa.',
  ],
  'cyber-ml-security': [
    'Distinguir ataques a entrenamiento, inferencia, privacidad, modelos y supply chain.',
    'Evaluar poisoning, backdoors, evasión, extraction, inversion, membership inference y provenance.',
    'Diseñar controles para pipelines ML con monitoreo, limitación de salida y riesgo residual.',
    'Usar MITRE ATLAS, SAFE-AI y AI RMF como mapas de amenaza, control y gobernanza.',
  ],
  'cyber-llm-rag-agents': [
    'Tratar contenido externo, documentos RAG y salidas LLM como no confiables.',
    'Aplicar LLM01-LLM10 a RAG, agentes, herramientas, memoria, embeddings y consumo.',
    'Diseñar agencia mínima, control por documento, validación de salida y humano en el lazo.',
    'Red-teamear de forma segura y continua antes de habilitar nuevas capacidades.',
  ],
};

function clusterDeUnidad(id) {
  return taxDoc.clusters.find((c) => (c.unidades ?? []).includes(id));
}

function slugCorto(id) {
  return id.replace(/^cyber-/, '').replace(/[^a-z0-9]+/g, '-');
}

function limpiarMd(s) {
  return (s ?? '')
    .replace(/^[-*]\s+/, '')
    .replace(/\*\*/g, '')
    .replace(/`/g, '')
    .replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_, id, label) => label ?? id)
    .trim();
}

function acortar(s, n = 190) {
  const t = limpiarMd(s).replace(/\s+/g, ' ');
  return t.length <= n ? t : `${t.slice(0, n - 1).trim()}…`;
}

function referenciasDe(md) {
  const i = md.indexOf('**Referencias**');
  if (i < 0) return [];
  return md.slice(i).split('\n')
    .filter((line) => line.trim().startsWith('- '))
    .map((line) => limpiarMd(line))
    .filter(Boolean);
}

function extraerLinea(md, etiqueta) {
  return md.split('\n').find((line) => line.includes(etiqueta)) ?? '';
}

function externalLabDe(unit, md) {
  const line = extraerLinea(md, 'Misión externa');
  const url = line.match(/https?:\/\/[^\s)]+/)?.[0]?.replace(/[.,;:]+$/g, '') ?? null;
  const criterio = line.match(/Criterio de cierre:\*\*\s*(.+)$/)?.[1] ?? line.match(/Criterio de cierre:\s*(.+)$/)?.[1] ?? '';
  return {
    type: 'external_lab',
    name: line.match(/\*\*([^*]+)\*\*\s*\(https?:\/\//)?.[1] ?? 'Laboratorio vivo',
    url,
    task: acortar(line.replace(/^.*Misión externa \(lab vivo\):\*\*\s*/, ''), 260),
    completion_criterion: acortar(criterio, 220),
    safety_note: 'Practica sólo en laboratorios, retos o sistemas propios/autorizados. Nunca pruebes técnicas contra sistemas ajenos.',
    source_reference: unit.libro,
  };
}

function portfolioTaskDe(unit, md) {
  const line = extraerLinea(md, 'Mini-entregable');
  return {
    type: 'portfolio_task',
    prompt: acortar(line.replace(/^.*Mini-entregable:\*\*\s*/, ''), 260),
    artifact: 'checklist, threat model, análisis, política, diagrama o reporte breve verificable',
    rubric: [
      'Modelo de amenaza claro',
      'Activos y riesgos correctamente identificados',
      'Mitigaciones proporcionales',
      'Señales de detección o verificación',
      'Comunicación sobria para un equipo técnico',
    ],
  };
}

function focosDe(unit, md) {
  const headings = [...md.matchAll(/^##\s+(.+)$/gm)]
    .map((m) => limpiarMd(m[1]))
    .filter((h) => !/De qué|Señales|Errores|Contraejemplo|Transferencia|Práctica|Referencias|Mini-ejemplo|Síntesis/i.test(h));
  return [...new Set([...(unit.ideas_clave ?? []), ...headings].map((x) => acortar(x, 120)).filter(Boolean))];
}

function contextoDe(clusterId) {
  const base = {
    'cyber-mindset': 'una app de ciencia de datos con notebooks, Supabase, API keys, datasets sensibles, modelos y dashboards',
    'cyber-systems-crypto': 'un entorno de notebooks que usa procesos Linux, tokens, TLS, archivos temporales y servicios internos',
    'cyber-web-api': 'una API educativa con login, roles, endpoints privados, carga de archivos y dashboards',
    'cyber-data-privacy': 'un dataset biomédico, educativo o financiero que se usará para entrenar un modelo',
    'cyber-secure-dev': 'un pipeline ML con CI/CD, dependencias Python/NPM, contenedores, secretos y datos de entrenamiento',
    'cyber-blue-team': 'un mini SOC que investiga accesos anómalos a notebooks, buckets, repositorios y dashboards',
    'cyber-ml-security': 'un pipeline ML que entrena, versiona y expone modelos para inferencia',
    'cyber-llm-rag-agents': 'un asistente RAG con documentos privados, herramientas externas y acciones con impacto',
  };
  return base[clusterId] ?? 'un sistema STEM con datos, software, usuarios y decisiones automatizadas';
}

function typeDe(tipo) {
  return tipo === 'concepto' ? 'quiz' : tipo;
}

function opcionIncorrecta(unit, foco, n) {
  const malos = [
    `Instalar una herramienta genérica sin nombrar el activo ni el impacto de ${foco}.`,
    `Confiar en que ${unit.titulo} no aplica porque el sistema es interno o pequeño.`,
    `Resolverlo sólo con documentación, sin control técnico ni evidencia verificable.`,
    `Aceptar el riesgo sin explicitar supuesto roto, señal de detección ni tradeoff.`,
  ];
  return malos[n % malos.length];
}

function opcionesPara(unit, q, foco) {
  const correcta = acortar(q.solucion ?? q.answer, 240);
  return [
    correcta,
    opcionIncorrecta(unit, foco, 0),
    opcionIncorrecta(unit, foco, 1),
    opcionIncorrecta(unit, foco, 2),
  ];
}

function normalizarPregunta(q, unit, index, focos) {
  const foco = q.concept ?? focos[index % focos.length] ?? unit.titulo;
  const normalized = {
    ...q,
    type: q.type ?? typeDe(q.tipo),
    prompt: q.prompt ?? q.enunciado,
    answer: q.answer ?? q.solucion,
    feedback: q.feedback ?? q.explicacion ?? 'La respuesta debe nombrar activo, supuesto roto, defensa, evidencia y tradeoff cuando aplique.',
    concept: foco,
    source_reference: q.source_reference ?? `${unit.libro}; ${unit.lectura}`,
    common_mistake: q.common_mistake ?? `Responder con una herramienta o definición aislada sin conectar ${foco} con riesgo, impacto y evidencia.`,
    recognition_signal: q.recognition_signal ?? `Señal: aparece ${foco} en una decisión con datos, permisos, confianza, automatización o exposición externa.`,
  };
  if (normalized.type === 'quiz' && !normalized.options) {
    normalized.options = opcionesPara(unit, normalized, foco);
  }
  return normalized;
}

function preguntaQuiz(unit, cluster, focos, difficulty, n) {
  const foco = focos[(n - 1) % focos.length] ?? unit.titulo;
  const ctx = contextoDe(cluster.id);
  const templates = {
    easy: [
      [
        `En ${unit.titulo}, ¿qué significa "${foco}" y qué activo o propiedad protege?`,
        `La respuesta debe traducir "${foco}" a un activo concreto y a una propiedad protegida: confidencialidad, integridad, disponibilidad, privacidad, autorización, trazabilidad o control de agencia.`,
      ],
      [
        `Distingue "${foco}" de una herramienta de seguridad genérica. ¿Qué pregunta defensiva obliga a hacer?`,
        `No basta nombrar una herramienta. "${foco}" obliga a preguntar qué puede salir mal, qué activo está expuesto, qué supuesto se rompe y qué evidencia mostraría que el control funciona.`,
      ],
      [
        `¿Qué señal temprana te haría pensar que "${foco}" importa en ${ctx}?`,
        `La señal suele ser un cruce de frontera: datos no confiables, permisos amplios, secreto expuesto, dependencia externa, salida automatizada, log insuficiente o decisión irreversible.`,
      ],
      [
        `Nombra un error típico al razonar sobre "${foco}" y corrígelo en una frase.`,
        `El error típico es convertir el concepto en checklist superficial. La corrección es enlazarlo con activo, adversario, impacto, defensa proporcional y verificación.`,
      ],
    ],
    medium: [
      [
        `En ${ctx}, aparece una decisión relacionada con "${foco}". ¿Qué supuesto de seguridad podría romperse y qué evidencia pedirías antes de aceptar el riesgo?`,
        `Primero se formula el supuesto: qué se confía, en quién, y bajo qué condición. Luego se pide evidencia observable: logs, permisos, configuración, linaje de datos, pruebas de control o monitoreo.`,
      ],
      [
        `Convierte "${foco}" en una regla operativa para un equipo de datos. Incluye dueño, control y señal de verificación.`,
        `Una regla operativa asigna responsabilidad, define un control verificable y deja señal: revisión, alerta, prueba, política, log o ticket. Sin dueño ni evidencia, el concepto no gobierna nada.`,
      ],
      [
        `Compara dos defensas posibles para "${foco}" en ${ctx}. ¿Cuál reduce más riesgo y qué costo introduce?`,
        `La defensa superior reduce impacto o probabilidad sobre el activo crítico con menor fricción razonable. Debe explicitar costo: latencia, trabajo manual, falsos positivos, menor utilidad o mantenimiento.`,
      ],
      [
        `Diseña una pregunta de revisión que detecte si el equipo está aplicando mal "${foco}".`,
        `La pregunta debe exponer un supuesto oculto: quién puede acceder, qué dato se recolecta, qué se ejecuta, qué salida se confía, qué se monitorea o qué pasa cuando falla.`,
      ],
    ],
    hard: [
      [
        `Caso borde de ${unit.titulo}: ¿cuándo una defensa basada en "${foco}" puede ser insuficiente o contraproducente? Propón mitigación por capas y riesgo residual.`,
        `Una defensa puede fallar por mala frontera de confianza, exceso de privilegios, datos auxiliares, fatiga operativa, cambios de contexto o falsas garantías. La respuesta excelente combina prevención, detección, recuperación y riesgo residual explícito.`,
      ],
      [
        `Critica esta postura: "ya cubrimos ${foco}, no hace falta monitorear". ¿Qué contraargumento técnico darías?`,
        `El control preventivo no demuestra ausencia de fallo. Se necesita monitoreo porque cambian datos, dependencias, usuarios, modelos, adversarios e incentivos; además hay riesgo residual y errores de configuración.`,
      ],
      [
        `Plantea un test adversarial seguro para validar "${foco}" sin atacar sistemas ajenos.`,
        `El test debe ejecutarse en laboratorio, staging o datos sintéticos; debe tener hipótesis, señal esperada, criterio de éxito, límite ético y acción correctiva si falla.`,
      ],
      [
        `¿Qué decisión tomarías si "${foco}" mejora seguridad pero reduce utilidad del sistema? Formula la decisión como riesgo residual aceptado o no aceptado.`,
        `La decisión compara impacto, probabilidad, utilidad, costo y verificabilidad. Si el riesgo residual supera el umbral, se rediseña; si se acepta, se documenta dueño, fecha, monitoreo y condición de revisión.`,
      ],
    ],
  };
  const [enunciado, solucion] = templates[difficulty][(n - 1) % templates[difficulty].length];
  const explicacion = {
    easy: 'Nivel easy: vocabulario exacto y conexión con un activo.',
    medium: 'Nivel medium: transferencia a operación, evidencia y tradeoff.',
    hard: 'Nivel hard: caso borde, validación adversarial segura y riesgo residual.',
  }[difficulty];
  return {
    id: `${unit.id}-quiz-${difficulty[0]}${String(n).padStart(2, '0')}`,
    tipo: 'concepto',
    type: 'quiz',
    difficulty,
    enunciado,
    prompt: enunciado,
    solucion,
    answer: solucion,
    explicacion,
    feedback: explicacion,
    options: [solucion, opcionIncorrecta(unit, foco, 0), opcionIncorrecta(unit, foco, 1), opcionIncorrecta(unit, foco, 2)],
    concept: foco,
    source_reference: `${unit.libro}; ${unit.lectura}`,
    common_mistake: `Contestar "${foco}" como palabra de glosario sin activo, adversario, evidencia ni tradeoff.`,
    recognition_signal: `Cuando ${ctx} cruza datos, permisos o decisiones automáticas, revisa "${foco}".`,
    metadata: { generated_by: GENERATED_BY, contract: '10 quiz por dificultad' },
  };
}

function preguntaScenario(unit, cluster, focos, n) {
  const foco = focos[(n + 1) % focos.length] ?? unit.titulo;
  const ctx = contextoDe(cluster.id);
  const enunciado = `Escenario ${n}: en ${ctx}, el equipo debe decidir sobre "${foco}" antes de desplegar. Identifica activo, amenaza, control, evidencia de verificación y tradeoff.`;
  const solucion = `Activos: datos, credenciales, modelo, usuarios o disponibilidad según el caso. Amenaza: abuso, fuga, manipulación, indisponibilidad o decisión no autorizada. Control: el mínimo proporcional (permisos, validación, aislamiento, monitoreo, gobernanza o humano en el lazo). Evidencia: configuración, prueba, log, métrica o revisión. Tradeoff: fricción, costo, latencia, menor utilidad o mantenimiento.`;
  return {
    id: `${unit.id}-scenario-${String(n).padStart(2, '0')}`,
    tipo: 'scenario',
    type: 'scenario',
    difficulty: n <= 2 ? 'medium' : 'hard',
    enunciado,
    prompt: enunciado,
    solucion,
    answer: solucion,
    explicacion: 'Un buen escenario defensivo fuerza decisión, evidencia y tradeoff; no basta nombrar una vulnerabilidad.',
    feedback: 'Busca activo, amenaza, control, evidencia y tradeoff en ese orden.',
    concept: foco,
    source_reference: `${unit.libro}; ${unit.lectura}`,
    common_mistake: 'Saltar directo a una herramienta o bloquear todo sin justificar proporcionalidad.',
    recognition_signal: `Señal: ${foco} aparece en una decisión de despliegue, datos, permisos o monitoreo.`,
    metadata: { generated_by: GENERATED_BY, contract: '5 escenarios prácticos' },
  };
}

function preguntaReflexion(unit, cluster, focos, n) {
  const foco = focos[(n + 2) % focos.length] ?? unit.titulo;
  const enunciado = `Reflexión ${n}: aplica "${foco}" a un proyecto real o ficticio de datos/IA. ¿Qué cambiarías esta semana y qué evidencia dejarías de que el riesgo bajó?`;
  const solucion = `La reflexión sólida elige un cambio pequeño y verificable: ajustar permisos, reducir datos, añadir una prueba, rotar un secreto, documentar un threat model, crear una alerta o limitar una herramienta. Debe producir evidencia concreta: diff, checklist, log, política, diagrama, ticket o resultado de laboratorio.`;
  return {
    id: `${unit.id}-reflexion-${String(n).padStart(2, '0')}`,
    tipo: 'reflexion',
    type: 'reflexion',
    difficulty: n <= 2 ? 'medium' : 'hard',
    enunciado,
    prompt: enunciado,
    solucion,
    answer: solucion,
    explicacion: 'La reflexión se evalúa por transferencia y evidencia, no por opinión general.',
    feedback: 'Aterriza la respuesta en una acción, un artefacto y una señal de verificación.',
    concept: foco,
    source_reference: `${unit.libro}; ${unit.lectura}`,
    common_mistake: 'Escribir una intención vaga sin artefacto observable ni criterio de cierre.',
    recognition_signal: `Señal: puedes convertir ${foco} en una práctica semanal verificable.`,
    metadata: { generated_by: GENERATED_BY, contract: '5 reflexiones' },
  };
}

function enriquecerUnidad(unit) {
  const md = readFileSync(join(ROOT, unit.lectura), 'utf8');
  const cluster = clusterDeUnidad(unit.id);
  const focos = focosDe(unit, md);
  const nivel = Number(unit.metadata?.nivel ?? 2);
  const level = LEVEL_BY_NUM[nivel] ?? 'core';
  const external_lab = externalLabDe(unit, md);
  const portfolio_task = portfolioTaskDe(unit, md);

  unit.level = unit.level ?? level;
  unit.difficulty = unit.difficulty ?? DIFF_BY_LEVEL[level];
  unit.primary_resource = unit.primary_resource ?? {
    title: unit.libro,
    type: unit.libro?.includes('http') ? 'web' : 'bibliography',
  };
  unit.learning_objective = unit.learning_objective ?? unit.objetivo;
  unit.lesson_contract = unit.lesson_contract ?? {
    central_idea: focos[0] ?? unit.objetivo,
    intuition_before_formalism: true,
    worked_example: true,
    recognition_signals: true,
    common_mistakes: true,
    counterexample_and_edge_case: true,
    transfer_to_data_ai_stem: true,
    retrieval_practice: true,
  };
  unit.external_lab = external_lab;
  unit.portfolio_task = portfolio_task;
  unit.references_apa = referenciasDe(md);
  unit.practice = [
    external_lab,
    portfolio_task,
    {
      type: 'retrieval_drill',
      prompt: `Antes de ver la solución, escribe desde memoria qué puede salir mal en ${unit.titulo}, qué evidencia lo mostraría y qué defensa reduce el riesgo.`,
      completion_criterion: 'Respuesta escrita con activo, supuesto roto, defensa, evidencia y tradeoff.',
    },
  ];

  let banco = (unit.banco ?? [])
    .filter((q) => q.metadata?.generated_by !== GENERATED_BY)
    .map((q, i) => normalizarPregunta(q, unit, i, focos));

  for (const difficulty of ['easy', 'medium', 'hard']) {
    let count = banco.filter((q) => q.tipo === 'concepto' && q.difficulty === difficulty).length;
    while (count < 10) {
      count += 1;
      banco.push(preguntaQuiz(unit, cluster, focos, difficulty, count));
    }
  }

  let scen = banco.filter((q) => q.tipo === 'scenario').length;
  while (scen < 5) {
    scen += 1;
    banco.push(preguntaScenario(unit, cluster, focos, scen));
  }

  let refl = banco.filter((q) => q.tipo === 'reflexion').length;
  while (refl < 5) {
    refl += 1;
    banco.push(preguntaReflexion(unit, cluster, focos, refl));
  }

  unit.banco = banco;
  return unit;
}

function diagnosticoPara(c) {
  const ctx = contextoDe(c.id);
  return {
    titulo: `Antes de ${c.titulo}`,
    instrucciones: 'Responde sin consultar la lección. No cuenta para calificación: sirve para calibrar criterio, vocabulario y transferencia.',
    preguntas: [
      {
        id: `${c.id}-diag-activo`,
        prompt: `En ${ctx}, nombra el activo más importante, quién podría abusarlo y qué impacto tendría.`,
        criterio: 'Activo concreto, adversario creíble e impacto sobre C/I/A, privacidad o disponibilidad.',
      },
      {
        id: `${c.id}-diag-supuesto`,
        prompt: 'Escribe un supuesto de confianza que, si fuera falso, rompería el sistema.',
        criterio: 'Supuesto verificable, no una amenaza genérica.',
      },
      {
        id: `${c.id}-diag-control`,
        prompt: 'Propón un control proporcional y explica qué tradeoff introduce.',
        criterio: 'Control con coste/fricción explícitos y relación con el riesgo.',
      },
      {
        id: `${c.id}-diag-evidencia`,
        prompt: '¿Qué evidencia técnica o documental demostraría que el control funciona?',
        criterio: 'Logs, pruebas, configuración, revisión, métrica, política o artefacto observable.',
      },
      {
        id: `${c.id}-diag-comunicacion`,
        prompt: 'Resume el riesgo en tres frases para un equipo técnico que debe decidir esta semana.',
        criterio: 'Comunicación sobria: riesgo, acción recomendada, riesgo residual.',
      },
    ],
  };
}

function enriquecerCluster(c) {
  const labs = LABS_BY_CLUSTER[c.id] ?? [];
  c.competencias = c.competencias ?? CLUSTER_COMPETENCIAS[c.id] ?? [];
  c.diagnosticoInicial = c.diagnosticoInicial ?? diagnosticoPara(c);
  c.laboratoriosVivos = labs.map(([nombre, url, objetivo, criterio_cierre]) => ({
    nombre,
    url,
    objetivo,
    criterio_cierre,
    safety_note: 'Sólo laboratorios autorizados; no probar contra sistemas ajenos.',
  }));
  c.estandar_mit_plus = c.estandar_mit_plus ?? {
    diferenciador: 'No se limita a exposición teórica: exige diagnóstico, retrieval, laboratorio vivo, escenario defensivo y artefacto de portafolio.',
    evidencia_de_dominio: [
      'Puede razonar qué puede salir mal antes de elegir herramienta.',
      'Produce controles proporcionales con señales de verificación.',
      'Conecta sistemas, datos, ML, LLMs, personas e incentivos.',
      'Comunica riesgo residual y tradeoffs sin espectáculo ni alarmismo.',
    ],
  };
  return c;
}

unidadesDoc._comment =
  'Unidades de la Fase 8 — Ciberseguridad. Fuente canónica inyectada a data/study.json con scripts/aplicar-ciberseguridad.mjs. Cumple contrato ciberseguridad.md: 40 unidades, metadata pedagógica, external_lab/portfolio_task y banco mínimo por lección (10 easy, 10 medium, 10 hard, 5 scenario, 5 reflexion), más prácticas avanzadas defensivas.';
unidadesDoc.unidades = unidadesDoc.unidades.map(enriquecerUnidad);

taxDoc._quality_standard = {
  nombre: 'MIT+ defensivo para científicos de datos e IA',
  descripcion:
    'Syllabus de criterio profesional: no enseña hacking como espectáculo; entrena threat modeling, defensa proporcional, laboratorios vivos, trazabilidad, evaluación auténtica y transferencia a datos, ML, LLMs, RAG y agentes.',
  principios: [
    'Intuición antes de formalismo.',
    'Escenarios y artefactos antes que memorización.',
    'Evidencia verificable de aprendizaje.',
    'Ética: sólo entornos propios o autorizados.',
    'Conexión explícita entre seguridad, privacidad, IA, producto y operación.',
  ],
};
taxDoc.clusters = taxDoc.clusters.map(enriquecerCluster);

writeFileSync(uniPath, `${JSON.stringify(unidadesDoc, null, 2)}\n`, 'utf8');
writeFileSync(taxPath, `${JSON.stringify(taxDoc, null, 2)}\n`, 'utf8');

const totalPreguntas = unidadesDoc.unidades.reduce((n, u) => n + (u.banco?.length ?? 0), 0);
console.log(`OK: contrato ciberseguridad enriquecido. Unidades=${unidadesDoc.unidades.length}. Preguntas=${totalPreguntas}.`);
