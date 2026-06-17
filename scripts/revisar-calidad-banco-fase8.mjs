#!/usr/bin/env node
// Revisa el banco generado de la Fase 8 sin tocar preguntas hechas a mano.
// Fuente canonica: data/ciberseguridad/_unidades.json.

import { readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const unidadesPath = join(ROOT, 'data', 'ciberseguridad', '_unidades.json');
const taxonomiaPath = join(ROOT, 'data', 'ciberseguridad', '_taxonomia.json');
const progresoPath = join(ROOT, 'PROGRESO-CALIDAD-BANCO.md');

const OLD_MARKER = 'enriquecer-ciberseguridad-contrato-v1';
const NEW_MARKER = 'revision-calidad-humana-v1';
const QUALITY_PROMPT = 'PROMPT-EJECUTOR-CALIDAD-BANCO.md';

const unidadesDoc = JSON.parse(readFileSync(unidadesPath, 'utf8'));
const taxDoc = JSON.parse(readFileSync(taxonomiaPath, 'utf8'));
const baselineQuestions = loadBaselineQuestions();

const clusterByUnit = new Map();
for (const cluster of taxDoc.clusters ?? []) {
  for (const unitId of cluster.unidades ?? []) clusterByUnit.set(unitId, cluster);
}

const clusterDefaults = {
  'cyber-mindset': {
    setting: 'un producto de datos con notebooks, API keys, dashboards y usuarios internos',
    asset: 'datos, credenciales y confianza del equipo',
    property: 'riesgo proporcional sobre confidencialidad, integridad o disponibilidad',
    related: '[[cyber-ms2]]',
  },
  'cyber-systems-crypto': {
    setting: 'un entorno de notebooks, procesos Linux, tokens, TLS y servicios internos',
    asset: 'credenciales, procesos, trafico y estado de sesion',
    property: 'limite de confianza tecnico',
    related: '[[cyber-web1]]',
  },
  'cyber-web-api': {
    setting: 'una API con login, roles, dashboards, endpoints privados y datos de usuario',
    asset: 'sesion, autorizacion por recurso y datos renderizados',
    property: 'frontera servidor-cliente',
    related: '[[cyber-dev1]]',
  },
  'cyber-data-privacy': {
    setting: 'un dataset sensible que alimenta analisis, dashboards y modelos',
    asset: 'personas representadas por los datos',
    property: 'privacidad, finalidad y minimizacion',
    related: '[[cyber-mls4]]',
  },
  'cyber-secure-dev': {
    setting: 'un pipeline ML con CI/CD, dependencias, contenedores, secretos y revisiones',
    asset: 'codigo, secretos, artefactos y cadena de suministro',
    property: 'integridad del software entregado',
    related: '[[cyber-blue4]]',
  },
  'cyber-blue-team': {
    setting: 'un mini SOC que investiga accesos a notebooks, buckets, repositorios y dashboards',
    asset: 'evidencia, logs, cobertura y tiempo de respuesta',
    property: 'deteccion y respuesta verificables',
    related: '[[cyber-blue5]]',
  },
  'cyber-ml-security': {
    setting: 'un pipeline ML que entrena, versiona y expone modelos en una API',
    asset: 'datos de entrenamiento, pesos, salidas y privacidad del modelo',
    property: 'robustez e integridad del sistema ML',
    related: '[[cyber-llm1]]',
  },
  'cyber-llm-rag-agents': {
    setting: 'un asistente RAG con documentos privados, herramientas y acciones externas',
    asset: 'documentos, contexto, herramientas, memoria y acciones del agente',
    property: 'control de agencia y salida no confiable',
    related: '[[cyber-blue2]]',
  },
};

const unitProfiles = {
  'cyber-ms1': {
    failure: 'se confunde una debilidad con riesgo real',
    control: 'inventario de activos, amenazas, impacto y control proporcional',
    evidence: 'tabla activo-amenaza-vulnerabilidad-impacto-control revisada',
    tradeoff: 'invertir primero donde el impacto es mayor',
    assumption: 'el equipo sabe que vale la pena proteger',
    safeTest: 'clasificar tres activos y romper CIA en cada uno',
    edge: 'un dato publico puede no tener C sensible, pero si I y A criticas',
    symptoms: ['una API key aparece en un notebook compartido', 'se protege un servidor pero no el dataset exportado', 'alguien dice "nadie va a entrar"', 'hay 200 hallazgos sin priorizar por impacto'],
    wrongs: ['Contar vulnerabilidades sin activo ni impacto.', 'Poner el mismo control a todos los activos.', 'Hablar de "hackers" sin amenaza concreta.', 'Medir seguridad por cantidad de herramientas instaladas.'],
  },
  'cyber-ms2': {
    failure: 'un supuesto de confianza queda implicito y rompe el diseno',
    control: 'threat model con privilegio minimo, capas y fallo seguro',
    evidence: 'diagrama de flujo con fronteras de confianza y pruebas del control',
    tradeoff: 'menos permisos y mas pasos de aprobacion',
    assumption: 'el componente vecino siempre se comporta bien',
    safeTest: 'simular en staging una entrada no confiable y comprobar contencion',
    edge: 'una capa fuerte puede fallar si comparte el mismo secreto o permiso que la anterior',
    symptoms: ['un job de batch usa una clave de administrador', 'el fallback abre acceso cuando falla la autorizacion', 'un dashboard confia en datos generados por otro servicio', 'nadie puede decir que pasa si una capa falla'],
    wrongs: ['Anadir una sola barrera y declarar riesgo cero.', 'Dar permisos amplios para evitar friccion.', 'Fallar abierto porque "mejora UX".', 'Revisar amenazas solo al final del proyecto.'],
  },
  'cyber-ms3': {
    failure: 'los incentivos hacen racional descuidar el control',
    control: 'asignar dueno, costo, beneficio y senal verificable de seguridad',
    evidence: 'metricas que muestran quien paga el control y quien sufre el dano',
    tradeoff: 'mover costo operativo al equipo que puede reducir el riesgo',
    assumption: 'quien decide tambien absorbe el impacto',
    safeTest: 'mapear tres decisiones a externalidades y duenos reales',
    edge: 'un seguro o SLA puede relajar defensas si no exige evidencia',
    symptoms: ['producto gana velocidad dejando secretos en variables compartidas', 'proveedor promete seguridad sin artefactos verificables', 'el dano cae en usuarios que no aprobaron el riesgo', 'se premia despliegue rapido y no mantenimiento'],
    wrongs: ['Tratar un problema de incentivos como si fuera solo tecnico.', 'Aceptar certificados sin evidencia operativa.', 'Externalizar el dano a usuarios o soporte.', 'Medir seguridad por promesas del proveedor.'],
  },
  'cyber-ms4': {
    failure: 'se excluye a personas, procesos y abuso del modelo de amenaza',
    control: 'casos de abuso, base de confianza minima y verificaciones fuera de la buena fe',
    evidence: 'lista de roles, decisiones confiadas y rutas de abuso probadas',
    tradeoff: 'menos automatismo ciego y mas confirmaciones en pasos sensibles',
    assumption: 'el usuario interno siempre actua con buen contexto',
    safeTest: 'ensayar una solicitud falsa de autoridad en un canal autorizado',
    edge: 'un insider con permiso legitimo puede causar dano sin explotar codigo',
    symptoms: ['soporte puede cambiar correo sin segunda verificacion', 'un manager pide exportar datos por chat', 'un bot obedece instrucciones en un documento externo', 'el flujo feliz no describe abusos'],
    wrongs: ['Culpar al usuario sin arreglar el proceso.', 'Confiar en titulos, tono o urgencia.', 'Modelar solo ataques tecnicos remotos.', 'Dar permisos permanentes por comodidad.'],
  },
  'cyber-ms5': {
    failure: 'se comunica riesgo como alarma o certeza falsa',
    control: 'priorizar por impacto, resiliencia, riesgo residual y proxima accion',
    evidence: 'runbook, RTO/RPO, dueno y senal de recuperacion probada',
    tradeoff: 'aceptar friccion o costo para reducir impacto medible',
    assumption: 'prevenir todo es posible',
    safeTest: 'ejecutar un tabletop de caida y medir recuperacion',
    edge: 'un control caro puede ser desproporcionado si el activo tiene bajo impacto',
    symptoms: ['un reporte dice "critico" sin impacto ni dueno', 'no existe plan de recuperacion', 'nadie nombra el riesgo residual aceptado', 'se oculta incertidumbre para sonar seguro'],
    wrongs: ['Prometer riesgo cero.', 'Usar miedo en vez de impacto.', 'Priorizar por ruido de alertas.', 'Comunicar sin accion, dueno ni fecha.'],
  },
  'cyber-sys1': {
    failure: 'una entrada hostil cruza una frontera tecnica sin validacion',
    control: 'permisos minimos, aislamiento y validacion del lado correcto',
    evidence: 'prueba de permisos, limites de proceso y rechazo de entradas no validas',
    tradeoff: 'menos comodidad al ejecutar codigo y compartir archivos',
    assumption: 'un proceso o entrada local es confiable por estar dentro',
    safeTest: 'crear un usuario sin privilegios y verificar que no alcance secretos',
    edge: 'un bug de memoria puede saltar abstracciones si el proceso tiene demasiado privilegio',
    symptoms: ['un notebook ejecuta archivos subidos por usuarios', 'un proceso lee mas carpetas de las necesarias', 'se acepta JSON de otro servicio sin validar', 'un servicio interno no autentica porque "esta en la red"'],
    wrongs: ['Confiar en la red interna.', 'Correr notebooks con permisos de administrador.', 'Validar solo en la UI.', 'Asumir que una excepcion no es superficie de ataque.'],
  },
  'cyber-sys2': {
    failure: 'se elige una primitiva criptografica por nombre y no por garantia',
    control: 'usar hash, cifrado, MAC, firma o TLS segun la propiedad requerida',
    evidence: 'diseno que separa confidencialidad, integridad, origen y autenticacion',
    tradeoff: 'mas gestion de llaves y rotacion disciplinada',
    assumption: 'un hash simple prueba origen o protege secretos',
    safeTest: 'clasificar cinco necesidades en hash/cifrado/MAC/firma/TLS',
    edge: 'TLS protege transito, no endpoints comprometidos ni logs con secretos',
    symptoms: ['contraseñas guardadas cifradas en vez de hash lento', 'se publica un checksum como prueba de autor', 'se cifra un payload pero no se autentica', 'se inventa un esquema casero de tokens'],
    wrongs: ['Cifrar contraseñas para poder recuperarlas.', 'Usar SHA-256 como firma.', 'Confiar en cripto casera.', 'Creer que TLS arregla autorizacion.'],
  },
  'cyber-sys3': {
    failure: 'se protege la contrasena pero no la identidad completa',
    control: 'hash lento, MFA, sesiones seguras, rotacion y recuperacion robusta',
    evidence: 'politica de sesiones, rate limit, eventos de login y pruebas de recuperacion',
    tradeoff: 'friccion moderada en MFA y recuperacion',
    assumption: 'quien posee el token sigue siendo el usuario legitimo',
    safeTest: 'invalidar una sesion y verificar que no siga autorizando',
    edge: 'la recuperacion de cuenta puede saltarse MFA si no tiene el mismo rigor',
    symptoms: ['tokens largos viven meses sin rotacion', 'reset por email cambia credenciales sin alertar', 'no hay rate limit de login', 'cookies de sesion accesibles a scripts'],
    wrongs: ['Guardar contrasenas cifradas.', 'Tratar MFA como decoracion opcional.', 'No revocar sesiones tras cambio critico.', 'Hacer recuperacion mas debil que login.'],
  },
  'cyber-sys4': {
    failure: 'se confunde contenedor con aislamiento absoluto',
    control: 'aislamiento por nivel de desconfianza, sin privilegios ni secretos embebidos',
    evidence: 'perfil de permisos, usuario no-root, limites y prueba de escape contenida',
    tradeoff: 'mayor costo operativo al subir de proceso a sandbox, contenedor o VM',
    assumption: 'compartir kernel no importa',
    safeTest: 'ejecutar codigo no confiable sin red ni secretos y comprobar limites',
    edge: 'un contenedor privileged con root y socket Docker equivale casi a host',
    symptoms: ['un contenedor trae secretos en la imagen', 'se usa --privileged para que "funcione"', 'jobs de usuarios comparten volumen sensible', 'se ejecuta codigo descargado en el proceso principal'],
    wrongs: ['Montar todo el filesystem por conveniencia.', 'Usar root dentro del contenedor.', 'Meter credenciales en la imagen.', 'Bajar aislamiento porque el lab es interno.'],
  },
  'cyber-sys5': {
    failure: 'se protege el dominio nominal pero no el transito autenticado',
    control: 'TLS correcto, certificados validados, HSTS y defensa de endpoints',
    evidence: 'certificado valido, HSTS, errores duros y monitoreo de cambios DNS',
    tradeoff: 'gestion de certificados y fallos visibles ante mala configuracion',
    assumption: 'DNS correcto implica servidor autentico',
    safeTest: 'probar que el cliente rechaza certificados invalidos en staging',
    edge: 'TLS no protege si el servidor o el navegador ya estan comprometidos',
    symptoms: ['un cliente acepta cualquier certificado', 'se mandan tokens por HTTP interno', 'DNS redirige a un host inesperado', 'la app desactiva validacion TLS para pruebas'],
    wrongs: ['Confiar en DNS sin autenticar el servidor.', 'Desactivar verificacion TLS.', 'Creer que VPN reemplaza TLS.', 'Ignorar endpoints porque el canal va cifrado.'],
  },
  'cyber-web1': {
    failure: 'un dato se convierte en instruccion SQL o HTML',
    control: 'parametrizar consultas y codificar salida en el servidor/contexto correcto',
    evidence: 'queries preparadas, uso de textContent o escaping contextual y prueba con payload benigno',
    tradeoff: 'menos libertad para armar HTML/SQL dinamico',
    assumption: 'validar en cliente basta',
    safeTest: 'usar payloads de laboratorio para confirmar que se tratan como texto',
    edge: 'un ORM vuelve a ser vulnerable si se usa raw concatenado',
    symptoms: ['se concatena q en un SELECT', 'un nombre de usuario entra por innerHTML', 'se filtran comillas como defensa principal', 'un dataset de texto libre se renderiza en dashboards'],
    wrongs: ['Filtrar comillas o la palabra script.', 'Depender de validacion del navegador.', 'Creer que HTTPS evita SQLi/XSS.', 'Usar ORM raw concatenando strings.'],
  },
  'cyber-web2': {
    failure: 'autenticacion se confunde con autorizacion o confianza de origen',
    control: 'verificar permisos por recurso en servidor, CSRF tokens y allow-list SSRF',
    evidence: 'tests IDOR/BOLA, tokens CSRF y bloqueos de destinos internos',
    tradeoff: 'mas chequeos por request y excepciones explicitas',
    assumption: 'si el usuario esta logueado puede ver cualquier ID',
    safeTest: 'probar acceso cruzado a un recurso propio y ajeno en staging',
    edge: 'un JWT firmado no autoriza si los permisos cambiaron o el recurso es ajeno',
    symptoms: ['GET /reportes/124 devuelve datos de otro usuario', 'un webhook acepta cualquier URL', 'acciones POST no tienen CSRF token', 'OAuth se usa sin validar audience/scope'],
    wrongs: ['Confiar en IDs ocultos.', 'Usar JWT como permiso permanente.', 'Bloquear SSRF con lista negra de strings.', 'Creer que SameSite arregla toda autorizacion.'],
  },
  'cyber-web3': {
    failure: 'la API expone objetos, campos o recursos sin control fino',
    control: 'autorizacion por objeto, allow-list de campos y limites de tasa/recursos',
    evidence: 'pruebas BOLA, esquema de entrada estricto y metricas de rate limit',
    tradeoff: 'mas codigo de autorizacion y manejo de errores 403/429',
    assumption: 'el cliente solo enviara campos permitidos',
    safeTest: 'intentar modificar owner_id o role en staging y exigir rechazo',
    edge: 'paginacion sin limite puede ser extraccion aunque la auth sea correcta',
    symptoms: ['PATCH /users/me acepta isAdmin', 'se cambia el ID en la URL y responde', 'un endpoint exporta miles de filas sin cuota', 'el backend mapea JSON completo al modelo'],
    wrongs: ['Ocultar campos en el front.', 'Validar solo el formato del ID.', 'Confiar en mass assignment del framework.', 'Subir rate limit hasta que no moleste.'],
  },
  'cyber-web4': {
    failure: 'se delega seguridad de navegador a cabeceras mal entendidas',
    control: 'HTTPS/HSTS, cookies Secure/HttpOnly/SameSite, CORS estrecho y CSP como capa',
    evidence: 'cabeceras verificadas, cookies no accesibles por JS y pruebas de origen',
    tradeoff: 'mas configuracion por entorno y debugging de integraciones',
    assumption: 'CORS es control de acceso de la API',
    safeTest: 'revisar desde un origen no permitido que el navegador bloquee lectura',
    edge: 'CSP reduce impacto de XSS pero no reemplaza codificar salida',
    symptoms: ['Access-Control-Allow-Origin: * con credenciales', 'cookies sin HttpOnly', 'CSP permite unsafe-inline', 'HSTS ausente en produccion'],
    wrongs: ['Usar CORS como autorizacion.', 'Guardar tokens en localStorage por comodidad.', 'Creer que CSP cura XSS.', 'Permitir HTTP porque hay login.'],
  },
  'cyber-web5': {
    failure: 'archivo, objeto serializado o configuracion se trata como confiable',
    control: 'validar tipo real, renombrar, aislar almacenamiento y endurecer defaults',
    evidence: 'pruebas de tipo MIME/magic bytes, permisos de bucket y deserializacion segura',
    tradeoff: 'restricciones de formatos y mas pasos de procesamiento',
    assumption: 'la extension o el Content-Type declaran la verdad',
    safeTest: 'subir archivo benigno con extension falsa y confirmar rechazo',
    edge: 'pickle/yaml.load sobre datos no confiables puede ejecutar codigo, incluso en ML',
    symptoms: ['se guardan uploads bajo /public', 'un bucket queda publico por default', 'se deserializa pickle de un usuario', 'se acepta ZIP sin limite de tamano'],
    wrongs: ['Confiar en la extension.', 'Servir uploads desde el mismo dominio ejecutable.', 'Usar defaults de nube sin revisar.', 'Deserializar para "validar" el archivo.'],
  },
  'cyber-dp1': {
    failure: 'se protege la tabla pero no a las personas representadas',
    control: 'minimizacion, finalidad explicita, base legal y evaluacion de dano',
    evidence: 'registro de finalidad, campos justificados y revision de retencion',
    tradeoff: 'menos datos disponibles para analisis exploratorio',
    assumption: 'si el acceso esta protegido, el uso siempre es apropiado',
    safeTest: 'eliminar un campo y medir si el objetivo aun se cumple',
    edge: 'un dato no sensible aislado puede volverse personal al combinarse',
    symptoms: ['se recolecta fecha exacta de nacimiento sin necesidad', 'un dashboard mezcla datos de salud y rendimiento', 'la retencion no tiene fecha de borrado', 'nadie puede explicar la finalidad de una columna'],
    wrongs: ['Confundir privacidad con cifrado.', 'Recolectar "por si acaso".', 'Tratar sensible y personal como sinonimos.', 'Conservar datos porque almacenarlos es barato.'],
  },
  'cyber-dp2': {
    failure: 'se promete anonimato ignorando cuasi-identificadores y contexto externo',
    control: 'evaluar reidentificacion, agregacion, DP cuando aplique y gobernanza de acceso',
    evidence: 'analisis de cuasi-identificadores, linaje, acceso y retencion',
    tradeoff: 'menor granularidad o utilidad estadistica',
    assumption: 'quitar nombre y correo anonimiza',
    safeTest: 'intentar reidentificacion interna con columnas auxiliares autorizadas',
    edge: 'seudonimizacion reversible sigue siendo dato personal',
    symptoms: ['dataset sin nombres conserva ZIP, edad y fechas', 'se comparte una muestra fila a fila', 'hash de ID se trata como anonimo', 'no hay procedencia ni finalidad documentada'],
    wrongs: ['Confundir seudonimizacion con anonimato.', 'Publicar microdatos por comodidad.', 'Ignorar datos auxiliares externos.', 'Usar k-anonimato sin discutir utilidad.'],
  },
  'cyber-dp3': {
    failure: 'consentimiento y transparencia se reducen a un banner incomprensible',
    control: 'base clara, proposito especifico, revocacion y derechos implementables',
    evidence: 'flujo de derechos probado y textos comprensibles por usuarios',
    tradeoff: 'menos conversion y mas trabajo operativo de derechos',
    assumption: 'aceptar terminos legitima cualquier uso futuro',
    safeTest: 'simular acceso/borrado/rectificacion de un titular y medir cumplimiento',
    edge: 'consentimiento no es libre si el servicio esencial exige aceptar todo',
    symptoms: ['casilla premarcada', 'propositos vagos como "mejorar servicios"', 'no hay ruta de borrado', 'se reutilizan datos para ML sin aviso claro'],
    wrongs: ['Usar dark patterns.', 'Esconder finalidades en texto legal largo.', 'Pedir consentimiento para todo.', 'No disenar derechos en la arquitectura.'],
  },
  'cyber-dp4': {
    failure: 'la politica dice quien puede acceder pero el sistema no lo verifica ni audita',
    control: 'least privilege por dato, auditoria inalterable y borrado real por ciclo de vida',
    evidence: 'logs de acceso a filas/columnas, revisiones de permisos y pruebas de borrado',
    tradeoff: 'mas complejidad en permisos y manejo de backups',
    assumption: 'tener politica equivale a tener control',
    safeTest: 'pedir acceso con rol equivocado y comprobar denegacion/log',
    edge: 'borrar la tabla principal no borra backups, features ni embeddings derivados',
    symptoms: ['todos los analistas ven columnas sensibles', 'logs registran login pero no consulta', 'permisos no caducan', 'features derivadas sobreviven al borrado'],
    wrongs: ['Auditar solo autenticacion.', 'Permisos permanentes por rol amplio.', 'Olvidar derivados y backups.', 'Confiar en controles manuales sin logs.'],
  },
  'cyber-dp5': {
    failure: 'el modelo filtra privacidad aunque el dataset bruto este cerrado',
    control: 'privacy by design, evaluacion de fuga, DP si aplica y limitacion de salida',
    evidence: 'pruebas de membership/inversion, presupuesto epsilon y card de privacidad',
    tradeoff: 'menor exactitud o utilidad por ruido y minimizacion',
    assumption: 'si no se publica el dataset, no hay fuga',
    safeTest: 'medir memorization y sensibilidad antes de publicar el modelo',
    edge: 'DP protege estadisticamente pero no arregla finalidad ni acceso indebido',
    symptoms: ['modelo completa datos raros de entrenamiento', 'API devuelve scores demasiado precisos', 'se publican embeddings de texto sensible', 'no hay evaluacion de fuga por modelo'],
    wrongs: ['Llamar anonimo al modelo entrenado.', 'Publicar probabilidades sin limite.', 'Usar DP sin explicar epsilon.', 'Anadir privacidad al final del pipeline.'],
  },
  'cyber-dev1': {
    failure: 'seguridad aparece despues del codigo y no como requisito verificable',
    control: 'requisitos de seguridad, validacion servidor, secretos fuera del repo y logs minimizados',
    evidence: 'tests de validacion, escaneo de secretos y revision de logs',
    tradeoff: 'mas trabajo antes de desplegar cambios rapidos',
    assumption: 'si pasa tests funcionales, es seguro',
    safeTest: 'inyectar entrada invalida y secreto falso en CI para confirmar bloqueo',
    edge: 'un log de debug puede filtrar mas que la respuesta de la API',
    symptoms: ['.env se sube por accidente', 'se loguea payload completo', 'validacion solo en frontend', 'requisito dice "seguro" sin criterio medible'],
    wrongs: ['Poner secretos en variables compartidas sin rotacion.', 'Validar solo en UI.', 'Loguear datos sensibles para depurar.', 'Convertir seguridad en ticket final.'],
  },
  'cyber-dev2': {
    failure: 'la cadena de dependencias se trata como caja negra confiable',
    control: 'SBOM, SCA, pinning, integridad y permisos minimos en CI/CD',
    evidence: 'SBOM actualizado, alertas priorizadas y firmas/hashes verificados',
    tradeoff: 'menos actualizaciones impulsivas y mas mantenimiento',
    assumption: 'paquete popular equivale a paquete seguro',
    safeTest: 'simular typosquatting en entorno local y confirmar que el lockfile lo bloquea',
    edge: 'una CVE critica puede ser irrelevante si no es alcanzable, y una media puede ser urgente si esta expuesta',
    symptoms: ['pip install sin lockfile', 'CI usa token admin', 'dependencia transitiva vulnerable sin dueno', 'se actualiza por version y no por explotabilidad'],
    wrongs: ['Actualizar todo a ciegas.', 'Ignorar transitivas.', 'Dar secretos amplios al CI.', 'Confiar en descargas sin integridad.'],
  },
  'cyber-dev3': {
    failure: 'el codigo viola principios de diseno sin que nadie lo nombre',
    control: 'threat modeling por componente y principios como mediacion completa y fail-safe',
    evidence: 'checklist por componente con supuesto roto, principio y prueba',
    tradeoff: 'mas diseno antes de implementar',
    assumption: 'un control en el borde cubre todos los caminos internos',
    safeTest: 'trazar una accion sensible por todos sus endpoints y jobs',
    edge: 'un cache o cola puede saltarse mediacion completa si no replica autorizacion',
    symptoms: ['endpoint alterno omite autorizacion', 'default permite acceso', 'modulo complejo concentra privilegios', 'secreto global resuelve todo'],
    wrongs: ['Parchear sintomas sin principio.', 'Fallar abierto.', 'Hacer excepciones "temporales" permanentes.', 'Confiar en revision manual sin prueba.'],
  },
  'cyber-dev4': {
    failure: 'una sola tecnica de verificacion deja puntos ciegos',
    control: 'combinar SAST, SCA, fuzzing, DAST y code review de logica',
    evidence: 'hallazgos reproducibles, cobertura de pruebas y decisiones de riesgo',
    tradeoff: 'mas tiempo de CI y triage de falsos positivos',
    assumption: 'el scanner encontrara errores de autorizacion',
    safeTest: 'fuzzear parser en entorno controlado y revisar autorizacion manualmente',
    edge: 'SAST no entiende reglas de negocio; review humano sin tests no escala',
    symptoms: ['scanner limpio pero IDOR en flujo', 'parser cae con input raro', 'PR cambia permisos sin reviewer de seguridad', 'falsos positivos se silencian globalmente'],
    wrongs: ['Confiar solo en SAST.', 'Fuzzear produccion.', 'Cerrar hallazgos sin reproducir.', 'Revisar estilo y no amenazas.'],
  },
  'cyber-dev5': {
    failure: 'el despliegue se vuelve el activo mas privilegiado y menos revisado',
    control: 'CI/CD con permisos minimos, contenedores endurecidos y proceso de parcheo',
    evidence: 'tokens acotados, imagen no-root, SBOM y SLA de vulnerabilidades',
    tradeoff: 'menos velocidad de hotfix improvisado',
    assumption: 'si el build pasa, el artefacto es integro',
    safeTest: 'revocar un token de CI y comprobar que el pipeline falla cerrado',
    edge: 'parchear rapido sin verificar puede romper disponibilidad o dejar el bug vivo',
    symptoms: ['runner de CI puede desplegar a todo', 'imagen corre como root', 'base vieja con CVEs', 'no hay canal de divulgacion'],
    wrongs: ['Usar credenciales largas en CI.', 'Meter secretos en imagen.', 'Parchear sin prueba de regresion.', 'Ignorar vulnerabilidades tras release.'],
  },
  'cyber-blue1': {
    failure: 'se mira una alerta sin traducirla a conducta adversaria y evidencia',
    control: 'mapear ATT&CK a logs, hipotesis, triage e incidente',
    evidence: 'evento, fuente, tecnica, severidad y decision documentada',
    tradeoff: 'mas instrumentacion y almacenamiento de logs',
    assumption: 'si no hay alerta, no hubo actividad',
    safeTest: 'generar un evento benigno y verificar que aparece en el log correcto',
    edge: 'un IoC aislado caduca; la conducta persiste mejor como deteccion',
    symptoms: ['hay logs pero nadie sabe que tecnica cubren', 'alerta sin severidad', 'evento aislado se llama incidente', 'no se registra acceso a buckets'],
    wrongs: ['Detectar solo por IP/hash.', 'Tratar todo evento como incidente.', 'Comprar SIEM sin fuentes utiles.', 'No registrar lo que se quiere detectar.'],
  },
  'cyber-blue2': {
    failure: 'una regla no nace de hipotesis ni mide falsos positivos/negativos',
    control: 'detection engineering con conducta, fuente, logica, baseline y validacion',
    evidence: 'regla probada, tasa FP/FN, datos faltantes y plan de ajuste',
    tradeoff: 'menos alertas pero mas trabajo de calibracion',
    assumption: 'mas alertas significa mas seguridad',
    safeTest: 'emular una conducta autorizada y confirmar alerta esperada',
    edge: 'una regla perfecta en staging falla si produccion no tiene la fuente de datos',
    symptoms: ['alerta por cualquier login fuera de horario', 'no hay baseline por entidad', 'regla sin dueno', 'emulacion no dispara nada'],
    wrongs: ['Optimizar solo para cero falsos positivos.', 'Ignorar falsos negativos.', 'Escribir reglas sin hipotesis.', 'No versionar detecciones.'],
  },
  'cyber-blue3': {
    failure: 'inteligencia se reduce a listas de IoC sin prioridad ni contexto',
    control: 'usar TTPs, contexto propio y piramide del dolor para priorizar deteccion',
    evidence: 'mapeo adversario-activo-tecnica-log-control',
    tradeoff: 'menos bloqueo automatico y mas analisis contextual',
    assumption: 'un feed externo sabe que amenaza mi organizacion',
    safeTest: 'tomar un TTP y buscar si existe fuente de log que lo observe',
    edge: 'un hash malicioso cambia facil; una tecnica operativa cuesta mas al adversario',
    symptoms: ['se bloquean IPs sin saber activo afectado', 'feed enorme genera ruido', 'no se conecta ATT&CK con logs propios', 'IoC viejo se trata como critico'],
    wrongs: ['Coleccionar IoC como fin.', 'No priorizar por activos propios.', 'Confundir atribucion con defensa.', 'Ignorar TTPs por ser mas dificiles.'],
  },
  'cyber-blue4': {
    failure: 'la respuesta destruye evidencia o improvisa decisiones criticas',
    control: 'preparacion, triaje, contencion preservando evidencia, erradicacion y lecciones',
    evidence: 'runbook, cadena de custodia, timeline y post-mortem sin culpa',
    tradeoff: 'contener puede mantener sistemas degradados mientras se preserva evidencia',
    assumption: 'apagar todo siempre es lo mas seguro',
    safeTest: 'tabletop de incidente con roles, tiempos y criterios de escalamiento',
    edge: 'aislar un host puede ser mejor que apagarlo si se necesita memoria/evidencia',
    symptoms: ['analista borra VM antes de capturar logs', 'no hay dueno de comunicacion', 'alerta critica espera horas', 'post-mortem busca culpables'],
    wrongs: ['Apagar sin preservar evidencia.', 'Saltar triaje.', 'Improvisar roles durante el incidente.', 'Cerrar sin lecciones accionables.'],
  },
  'cyber-blue5': {
    failure: 'la cobertura defensiva se declara sin haber sido emulada ni medida',
    control: 'purple teaming, matriz de cobertura, brechas y metricas MTTD/MTTR',
    evidence: 'emulaciones autorizadas, detecciones disparadas y backlog de brechas',
    tradeoff: 'tiempo de ejercicios y exposicion de fallas incomodas',
    assumption: 'tener una regla equivale a detectar la tecnica',
    safeTest: 'ejecutar emulacion segura y verificar alerta, triage y respuesta',
    edge: 'teatro de cobertura: marcar ATT&CK sin fuente de log ni prueba',
    symptoms: ['matriz ATT&CK llena en una hoja pero sin evidencia', 'metricas cuentan reglas creadas', 'purple team no genera backlog', 'MTTD desconocido'],
    wrongs: ['Medir actividad y no resultado.', 'Evitar ejercicios para no fallar.', 'No cerrar brechas.', 'Aceptar cobertura declarada por proveedor.'],
  },
  'cyber-mls1': {
    failure: 'el modelo introduce superficies que no existen en software clasico',
    control: 'separar amenazas de entrenamiento, inferencia, privacidad y supply chain',
    evidence: 'threat model ML con datos, pesos, API, metricas y monitoreo',
    tradeoff: 'menor velocidad experimental y mas gobierno de artefactos',
    assumption: 'accuracy en test resume seguridad',
    safeTest: 'revisar si un backdoor simple pasaria validacion normal en laboratorio',
    edge: 'un modelo puede memorizar datos aunque el endpoint nunca exponga la tabla',
    symptoms: ['dataset externo entra sin procedencia', 'validacion promedio ignora subgrupos raros', 'modelo responde sobre datos de entrenamiento', 'se publica API sin limite de consultas'],
    wrongs: ['Tratar ML como API tradicional solamente.', 'Confiar en accuracy promedio.', 'Ignorar datos de entrenamiento como activo.', 'No versionar datasets.'],
  },
  'cyber-mls2': {
    failure: 'se expone inferencia sin limitar extraccion, inversion o abuso',
    control: 'auth, rate limit, salida acotada, provenance y monitoreo de consultas',
    evidence: 'limites por usuario, auditoria de consultas y verificacion de origen de modelos',
    tradeoff: 'menos detalle de salida y mas friccion para usuarios intensivos',
    assumption: 'si el modelo no se descarga, no se puede robar informacion',
    safeTest: 'consultas controladas para medir si salidas permiten clonar o inferir miembros',
    edge: 'embeddings compartidos pueden filtrar similitud y contenido sensible',
    symptoms: ['API devuelve probabilidades completas', 'modelo preentrenado sin origen verificable', 'no hay cuota por usuario', 'se comparten embeddings de documentos privados'],
    wrongs: ['Publicar logits completos por comodidad.', 'No auditar consultas repetitivas.', 'Descargar modelos sin provenance.', 'Creer que pesos cerrados eliminan extraccion.'],
  },
  'cyber-mls3': {
    failure: 'robustez se confunde con exactitud limpia',
    control: 'evaluacion adversarial, adversarial training cuando aplique y monitoreo de deriva',
    evidence: 'metricas de robustez por amenaza, no solo test accuracy',
    tradeoff: 'posible baja de exactitud limpia y mayor costo de evaluacion',
    assumption: 'si no se ve la perturbacion, no importa',
    safeTest: 'generar perturbaciones benignas en un dataset de laboratorio',
    edge: 'ataques black-box pueden transferir aunque el modelo sea cerrado',
    symptoms: ['clasificador falla con cambios pequenos', 'solo se reporta accuracy global', 'no hay pruebas por subgrupo', 'defensa oculta gradientes sin medir transferencia'],
    wrongs: ['Llamar robusto a un modelo con test limpio.', 'Confiar en security through obscurity.', 'Ignorar black-box.', 'No definir amenaza antes de evaluar.'],
  },
  'cyber-mls4': {
    failure: 'las salidas del modelo revelan el modelo o sus datos',
    control: 'limitar consultas/salidas, reducir memorizacion, DP y monitoreo de abuso',
    evidence: 'pruebas extraction, inversion y membership con riesgo residual documentado',
    tradeoff: 'menos transparencia de scores y posible perdida de utilidad',
    assumption: 'un endpoint de prediccion no filtra datos de entrenamiento',
    safeTest: 'evaluar membership inference en datos sintenticos o autorizados',
    edge: 'proteger pesos no evita inversion si la API responde demasiado',
    symptoms: ['API permite consultas ilimitadas', 'respuestas muestran confianza exacta', 'modelo recuerda ejemplos raros', 'embeddings se entregan sin control'],
    wrongs: ['Ocultar pesos y no limitar API.', 'Publicar scores de alta precision.', 'Ignorar memorizacion.', 'Confundir inversion con extraction.'],
  },
  'cyber-mls5': {
    failure: 'gobernanza de IA no cubre origen, integridad y reevaluacion de modelos',
    control: 'provenance, model cards de seguridad, AI RMF y MITRE ATLAS',
    evidence: 'linaje de datos/modelos, firma o hash, riesgos y reevaluaciones programadas',
    tradeoff: 'mas disciplina documental y gates de despliegue',
    assumption: 'un modelo de un repositorio popular es automaticamente confiable',
    safeTest: 'verificar hash/origen y mapear una tecnica ATLAS a un control',
    edge: 'integridad del archivo no prueba que el origen o los datos sean apropiados',
    symptoms: ['modelo base sin licencia ni dataset conocidos', 'no hay model card', 'cambio de version sin reevaluacion', 'riesgo residual no tiene dueno'],
    wrongs: ['Confundir integridad con confianza.', 'Usar AI RMF como checklist decorativo.', 'No documentar riesgo residual.', 'Desplegar modelos sin linaje.'],
  },
  'cyber-llm1': {
    failure: 'contenido no confiable se vuelve instruccion para el modelo',
    control: 'arquitectura con contenido no confiable, capacidades reducidas y verificacion externa',
    evidence: 'pruebas de prompt injection directa/indirecta y limites de herramienta',
    tradeoff: 'menos autonomia del asistente y mas validaciones',
    assumption: 'el system prompt separa perfectamente instrucciones de datos',
    safeTest: 'inyectar una instruccion benigna en documento RAG de laboratorio',
    edge: 'no existe separacion perfecta texto-instruccion en un LLM general',
    symptoms: ['documento externo dice "ignora instrucciones"', 'asistente resume paginas web y ejecuta acciones', 'defensa se basa en pedirle al modelo que no obedezca', 'prompt contiene secretos'],
    wrongs: ['Confiar solo en el system prompt.', 'Pedir al modelo que filtre su propia inyeccion.', 'Poner secretos en contexto.', 'Dar herramientas potentes sin verificacion.'],
  },
  'cyber-llm2': {
    failure: 'RAG o agentes convierten texto malicioso en accion real',
    control: 'control por documento, agencia minima, herramientas estrechas y humano en el lazo',
    evidence: 'ACL por documento, permisos de herramienta, logs y aprobaciones',
    tradeoff: 'menos automatizacion y mas confirmaciones',
    assumption: 'todo documento recuperado puede instruir al asistente',
    safeTest: 'documento de prueba intenta ordenar una accion y debe quedar como cita no confiable',
    edge: 'una salida LLM es entrada no confiable para el siguiente componente',
    symptoms: ['RAG trae documentos de RRHH a usuarios sin permiso', 'agente puede enviar correos externos', 'herramienta acepta comandos amplios', 'memoria guarda datos sensibles sin TTL'],
    wrongs: ['Usar permisos del bot para todo.', 'Confiar en ranking del retriever como autorizacion.', 'Permitir herramientas genericas.', 'Omitir confirmacion humana en acciones irreversibles.'],
  },
  'cyber-llm3': {
    failure: 'se pone informacion sensible donde el modelo puede repetirla o alcanzarla',
    control: 'no secretos en prompt, control de acceso RAG y salida minimizada',
    evidence: 'pruebas de fuga de contexto, ACL en retrieval y revision de logs',
    tradeoff: 'menos contexto disponible y respuestas menos completas',
    assumption: 'el system prompt es secreto',
    safeTest: 'probar extraccion de prompt y datos ficticios en entorno autorizado',
    edge: 'la fuga RAG es BOLA/IDOR aplicado a recuperacion de documentos',
    symptoms: ['system prompt contiene API keys', 'retriever no filtra por usuario', 'logs guardan prompts con datos sensibles', 'modelo puede citar documentos privados'],
    wrongs: ['Tratar prompt como caja fuerte.', 'Confiar en que el modelo no revelara contexto.', 'Filtrar salida sin arreglar retrieval.', 'Guardar prompts completos indefinidamente.'],
  },
  'cyber-llm4': {
    failure: 'modelo, datos o consumo se aceptan sin limites ni provenance',
    control: 'verificar supply chain, proteger fuentes RAG, limitar cuotas y monitorear costos',
    evidence: 'linaje de modelo/dataset, cambios aprobados y alertas de consumo',
    tradeoff: 'mas gates para actualizar modelos y fuentes',
    assumption: 'fine-tuning, plugins y fuentes RAG son confiables por default',
    safeTest: 'editar fuente RAG de laboratorio y comprobar revision antes de indexar',
    edge: 'LLM10 combina DoS tecnico con denial of wallet por costo variable',
    symptoms: ['fuente RAG editable entra al indice sin revision', 'plugin nuevo sin permisos acotados', 'sin cuota por usuario', 'adapter descargado sin verificar'],
    wrongs: ['Actualizar modelo sin reevaluar.', 'Indexar cualquier fuente editable.', 'No poner presupuesto ni rate limit.', 'Confiar en plugins por reputacion.'],
  },
  'cyber-llm5': {
    failure: 'se gobierna cada riesgo LLM aislado y no el sistema completo',
    control: 'defensa en profundidad, red teaming continuo, monitoreo y humano en el lazo',
    evidence: 'plan de pruebas adversarias, gates de cambio y runbook de incidente',
    tradeoff: 'menor velocidad de habilitar herramientas nuevas',
    assumption: 'una mitigacion contra prompt injection sera definitiva',
    safeTest: 'red team autorizado antes de lanzar y tras cada cambio de modelo/herramienta',
    edge: 'un multiagente invalida evaluaciones previas al agregar capacidades',
    symptoms: ['se lanza sin red teaming', 'agente con correo externo sin aprobacion', 'no se reevalua al cambiar modelo', 'monitoreo no registra abuso o deriva'],
    wrongs: ['Buscar defensa definitiva.', 'Evaluar una sola vez.', 'Habilitar agencia amplia sin aprobacion.', 'No gatear cambios de capacidades.'],
  },
};

function clean(text) {
  return polishSpanish(String(text ?? '')
    .replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, '$2')
    .replace(/\*\*/g, '')
    .replace(/`/g, '')
    .replace(/\s+/g, ' ')
    .trim());
}

function clip(text, max = 170) {
  const t = clean(text);
  if (t.length <= max) return t;
  const cut = t.slice(0, max - 1);
  return `${cut.slice(0, Math.max(0, cut.lastIndexOf(' '))).trim()}.`;
}

function polishSpanish(text) {
  return text
    .replace(/¿Que\b/g, '¿Qué')
    .replace(/¿Cual\b/g, '¿Cuál')
    .replace(/¿Como\b/g, '¿Cómo')
    .replace(/¿Donde\b/g, '¿Dónde')
    .replace(/¿Quien\b/g, '¿Quién')
    .replace(/\bdano\b/g, 'daño')
    .replace(/\bdanos\b/g, 'daños')
    .replace(/\bdueno\b/g, 'dueño')
    .replace(/\bduenos\b/g, 'dueños')
    .replace(/\bsenal\b/g, 'señal')
    .replace(/\bsenales\b/g, 'señales')
    .replace(/\bredisenar\b/g, 'rediseñar')
    .replace(/\bredisenia\b/g, 'rediseña')
    .replace(/\bredisenaria\b/g, 'rediseñaría')
    .replace(/\baccion\b/g, 'acción')
    .replace(/\bautorizacion\b/g, 'autorización')
    .replace(/\bconfiguracion\b/g, 'configuración')
    .replace(/\bproduccion\b/g, 'producción')
    .replace(/\bverificacion\b/g, 'verificación')
    .replace(/\brevision\b/g, 'revisión')
    .replace(/\bdecision\b/g, 'decisión')
    .replace(/\bdecisiones\b/g, 'decisiones')
    .replace(/\bafirmacion\b/g, 'afirmación')
    .replace(/\bcorreccion\b/g, 'corrección')
    .replace(/\bcondicion\b/g, 'condición')
    .replace(/\bgarantia\b/g, 'garantía')
    .replace(/\bopcion\b/g, 'opción')
    .replace(/\btecnologia\b/g, 'tecnología')
    .replace(/\bconversacion\b/g, 'conversación')
    .replace(/\baceptacion\b/g, 'aceptación')
    .replace(/\btension\b/g, 'tensión')
    .replace(/\bevaluacion\b/g, 'evaluación')
    .replace(/\bintencion\b/g, 'intención')
    .replace(/\bextraccion\b/g, 'extracción')
    .replace(/\brecuperacion\b/g, 'recuperación')
    .replace(/\bmitigacion\b/g, 'mitigación')
    .replace(/\bconfirmacion\b/g, 'confirmación')
    .replace(/\bindice\b/g, 'índice')
    .replace(/\bdiseno\b/g, 'diseño')
    .replace(/\btecnico\b/g, 'técnico')
    .replace(/\btecnica\b/g, 'técnica')
    .replace(/\bgenerico\b/g, 'genérico')
    .replace(/\bgenerica\b/g, 'genérica')
    .replace(/\bminimo\b/g, 'mínimo')
    .replace(/\bminima\b/g, 'mínima')
    .replace(/\btrafico\b/g, 'tráfico')
    .replace(/\bpolitica\b/g, 'política')
    .replace(/\bpractica\b/g, 'práctica')
    .replace(/\bcritico\b/g, 'crítico')
    .replace(/\bcritica\b/g, 'crítica')
    .replace(/\bseparacion\b/g, 'separación')
    .replace(/\bmedicion\b/g, 'medición')
    .replace(/\boperacion\b/g, 'operación')
    .replace(/\butil\b/g, 'útil')
    .replace(/\butiles\b/g, 'útiles')
    .replace(/\blimite\b/g, 'límite')
    .replace(/\blimites\b/g, 'límites')
    .replace(/\bhipotesis\b/g, 'hipótesis')
    .replace(/\bimplicita\b/g, 'implícita')
    .replace(/\bexplicito\b/g, 'explícito')
    .replace(/\bexplicita\b/g, 'explícita')
    .replace(/\bvalido\b/g, 'válido')
    .replace(/\bvalida\b/g, 'válida')
    .replace(/\breevaluacion\b/g, 'reevaluación')
    .replace(/\bversion\b/g, 'versión')
    .replace(/\bautonomía\b/g, 'autonomía')
    .replace(/\bautomatizacion\b/g, 'automatización')
    .replace(/\bfriccion\b/g, 'fricción')
    .replace(/\bauditoria\b/g, 'auditoría')
    .replace(/\bautomatico\b/g, 'automático')
    .replace(/\bfragiles\b/g, 'frágiles')
    .replace(/\bsesion\b/g, 'sesión')
    .replace(/\bcontencion\b/g, 'contención')
    .replace(/\bReflexion\b/g, 'Reflexión')
    .replace(/\breflexion\b/g, 'reflexión')
    .replace(/\bhabrias\b/g, 'habrías')
    .replace(/\bharia\b/g, 'haría')
    .replace(/\btentacion\b/g, 'tentación')
    .replace(/\bdeberia\b/g, 'debería')
    .replace(/\bpediria\b/g, 'pediría')
    .replace(/\bcambiaria\b/g, 'cambiaría')
    .replace(/\bConten\b/g, 'Contén')
    .replace(/\bMantendria\b/g, 'Mantendría')
    .replace(/\bPediria\b/g, 'Pediría')
    .replace(/\bCambiaria\b/g, 'Cambiaría')
    .replace(/\bmas\b/g, 'más');
}

function pick(items, index) {
  if (!items?.length) return '';
  return items[((index % items.length) + items.length) % items.length];
}

function unique(items) {
  const seen = new Set();
  const out = [];
  for (const item of items) {
    const v = clip(item, 170);
    if (!v || seen.has(v)) continue;
    seen.add(v);
    out.push(v);
  }
  return out;
}

function ideas(unit) {
  return unique([
    ...(unit.ideas_clave ?? []),
    unit.lesson_contract?.central_idea,
    unit.learning_objective,
    unit.objetivo,
  ]);
}

function profileFor(unit) {
  const cluster = clusterByUnit.get(unit.id);
  const base = clusterDefaults[cluster?.id] ?? clusterDefaults['cyber-mindset'];
  const specific = unitProfiles[unit.id] ?? {};
  return {
    cluster,
    ...base,
    ...specific,
    title: unit.titulo,
    concepts: ideas(unit),
    wrongs: unique([...(specific.wrongs ?? []), ...genericWrongs(base, specific)]),
    symptoms: specific.symptoms ?? ['aparece una frontera de confianza sin dueno', 'un control se acepta sin evidencia'],
  };
}

function genericWrongs(base, profile) {
  return [
    `Aceptar el riesgo sin dueño, evidencia ni fecha de revisión.`,
    `Mover el control al cliente o a documentación sin verificación técnica.`,
    `Aplicar un control genérico sin revisar el activo afectado.`,
    `Confiar en que, por ser interno, el fallo no tiene impacto real.`,
    `Bloquear todo sin medir impacto, utilidad ni riesgo residual.`,
  ];
}

function questionOrdinal(q, fallback) {
  const m = String(q.id ?? '').match(/-(?:quiz-[emh]|scenario|reflexion)-?0*(\d+)$/);
  return m ? Number(m[1]) : fallback + 1;
}

function typeFor(q) {
  if (q.tipo === 'concepto') return 'quiz';
  return q.tipo ?? q.type ?? 'scenario';
}

function wrongOptions(profile, answer, n) {
  const all = unique([
    ...profile.wrongs.slice(n),
    ...profile.wrongs.slice(0, n),
    `Pedir más datos antes de nombrar activo, amenaza e impacto.`,
    `Esperar al incidente para decidir controles.`,
  ]).filter((x) => x !== answer);
  return all.slice(0, 3);
}

function makeQuiz(unit, q, profile, index) {
  const difficulty = q.difficulty ?? 'medium';
  const n = questionOrdinal(q, index);
  const concept = clean(q.concept) || pick(profile.concepts, n) || profile.failure;
  const symptom = pick(profile.symptoms, n - 1);
  const wrong = pick(profile.wrongs, n + 1);
  const templates = {
    easy: [
      () => ({
        enunciado: `En ${profile.setting}, ${symptom}. ¿Cuál es la lectura defensiva correcta de "${concept}"?`,
        answer: `${profile.failure}; protege ${profile.asset} con ${profile.control}.`,
        feedback: `La pista no es la herramienta, sino el activo y la frontera de confianza. Conecta ${concept} con ${profile.related}.`,
        mistake: wrong,
        signal: `Aparece cuando ${symptom}.`,
      }),
      () => ({
        enunciado: `Un revisor acepta "${concept}" como cubierto. ¿Qué evidencia mínima debería pedir?`,
        answer: `${profile.evidence}.`,
        feedback: `Una afirmacion de seguridad sin evidencia observable no discrimina riesgo real de deseo.`,
        mistake: `Aceptar "${concept}" como etiqueta sin prueba verificable.`,
        signal: `Busca logs, configuracion, prueba, politica o artefacto revisable.`,
      }),
      () => ({
        enunciado: `El equipo propone: "${wrong}". ¿Qué corrección aplica mejor a ${unit.titulo}?`,
        answer: `Nombrar el activo, explicar por qué ${profile.failure} y elegir un control proporcional con evidencia.`,
        feedback: `La defensa proporcional une activo, impacto, control y costo; no basta una accion aislada.`,
        mistake: wrong,
        signal: `La decision nombra un control pero no el dano que reduce.`,
      }),
      () => ({
        enunciado: `Si ${symptom}, ¿qué propiedad se debe proteger primero antes de elegir herramienta?`,
        answer: `${profile.property}, con evidencia de ${profile.evidence}.`,
        feedback: `La pregunta obliga a decidir que garantia importa antes de comprar o configurar algo.`,
        mistake: `Elegir tecnologia antes de nombrar la propiedad amenazada.`,
        signal: `La conversacion salta directo a una herramienta.`,
      }),
    ],
    medium: [
      () => ({
        enunciado: `En ${profile.setting}, el control existe pero nadie puede mostrar ${profile.evidence}. ¿Qué conclusión es más rigurosa?`,
        answer: `El riesgo no esta cerrado; falta evidencia de que ${profile.control} funciona.`,
        feedback: `Un control documentado no equivale a un control efectivo. La evidencia es parte del diseno.`,
        mistake: `Tratar documentacion o intencion como control operativo.`,
        signal: `La defensa se describe, pero no deja huella verificable.`,
      }),
      () => ({
        enunciado: `Compara dos respuestas: aplicar "${wrong}" o aplicar "${profile.control}". ¿Por qué la segunda discrimina mejor el riesgo?`,
        answer: `Porque ataca ${profile.failure} sobre ${profile.asset} y deja ${profile.evidence}.`,
        feedback: `La opcion correcta reduce un mecanismo de fallo concreto y permite auditarlo.`,
        mistake: wrong,
        signal: `Dos controles parecen razonables, pero uno no toca el supuesto roto.`,
      }),
      () => ({
        enunciado: `El supuesto oculto es: "${profile.assumption}". ¿Qué pregunta de revisión lo pondría a prueba?`,
        answer: `¿Qué pasa si ese supuesto falla, quién ve el impacto y dónde queda registrado?`,
        feedback: `Buen threat modeling convierte confianza implicita en pregunta falsable.`,
        mistake: `No formular el supuesto como algo que pueda fallar.`,
        signal: `La arquitectura depende de buena fe, default o memoria humana.`,
      }),
      () => ({
        enunciado: `Tras observar ${symptom}, producto quiere aceptar el riesgo por velocidad. ¿Qué condición mínima vuelve defendible esa decisión?`,
        answer: `Documentar riesgo residual, dueno, monitoreo y condicion de revision.`,
        feedback: `Aceptar riesgo puede ser valido, pero solo si queda explicito, acotado y revisable.`,
        mistake: `Confundir aceptacion de riesgo con ignorarlo.`,
        signal: `Se decide seguir sin dueno ni fecha de reevaluacion.`,
      }),
    ],
    hard: [
      () => ({
        enunciado: `Caso borde: ${profile.edge}. ¿Qué respuesta evita una falsa sensación de seguridad?`,
        answer: `Usar capas: ${profile.control}, verificacion con ${profile.evidence} y riesgo residual explicito.`,
        feedback: `Los casos borde prueban si el estudiante entiende limites, no solo la regla general.`,
        mistake: `Aplicar la regla de forma absoluta sin revisar condiciones.`,
        signal: `Una defensa parece correcta, pero el contexto cambia su garantia.`,
      }),
      () => ({
        enunciado: `Diseña una prueba adversarial segura para "${concept}" sin tocar sistemas ajenos. ¿Cuál es la mejor forma?`,
        answer: `${profile.safeTest}; medir resultado esperado y accion correctiva.`,
        feedback: `La prueba debe ser autorizada, reproducible y conectada a un criterio de cierre.`,
        mistake: `Probar en produccion o contra terceros para "ver si pasa".`,
        signal: `Quieres evidencia de resistencia, no instrucciones ofensivas accionables.`,
      }),
      () => ({
        enunciado: `El control de ${unit.titulo} reduce riesgo pero introduce ${profile.tradeoff}. ¿Qué decisión técnica es más madura?`,
        answer: `Comparar impacto, utilidad y evidencia; aceptar o rediseñar con riesgo residual documentado.`,
        feedback: `La seguridad profesional decide tradeoffs; no maximiza controles a ciegas.`,
        mistake: `Bloquear todo o ignorar el control sin cuantificar impacto.`,
        signal: `Hay tension real entre utilidad, costo y dano posible.`,
      }),
      () => ({
        enunciado: `Un cambio nuevo invalida parte de la evidencia anterior sobre "${concept}". ¿Qué debe ocurrir antes de desplegar?`,
        answer: `Reevaluar ${profile.control}, actualizar evidencia y revisar monitoreo asociado.`,
        feedback: `La garantia de seguridad envejece cuando cambian datos, permisos, modelos o dependencias.`,
        mistake: `Confiar en una evaluacion vieja tras cambiar la superficie.`,
        signal: `Aparece una version nueva, fuente nueva, permiso nuevo o herramienta nueva.`,
      }),
    ],
  };
  const spec = pick(templates[difficulty] ?? templates.medium, n - 1)();
  const answer = clip(spec.answer, 170);
  const options = unique([answer, ...wrongOptions(profile, answer, n)]);
  while (options.length < 4) options.push(`Revisar solo documentacion y posponer evidencia operativa ${options.length}.`);

  return {
    ...q,
    tipo: 'concepto',
    type: 'quiz',
    difficulty,
    enunciado: clip(spec.enunciado, 260),
    prompt: clip(spec.enunciado, 260),
    solucion: answer,
    answer,
    explicacion: clip(spec.feedback, 320),
    feedback: clip(spec.feedback, 320),
    options: options.slice(0, 4),
    concept,
    source_reference: `${unit.libro}; ${unit.lectura}`,
    common_mistake: clip(spec.mistake, 220),
    recognition_signal: clip(spec.signal, 220),
    metadata: revisedMetadata(q),
  };
}

function makeScenario(unit, q, profile, index) {
  const n = questionOrdinal(q, index);
  const concept = clean(q.concept) || pick(profile.concepts, n) || profile.failure;
  const symptom = pick(profile.symptoms, n);
  const frames = [
    () => ({
      prompt: `Escenario: vas a aprobar el despliegue de ${profile.setting}. Antes de firmar, aparece esta senal: ${symptom}. Decide control prioritario, evidencia y riesgo residual.`,
      answer: `Prioriza ${profile.control} porque ${profile.failure} afecta ${profile.asset}. La evidencia minima es ${profile.evidence}. La respuesta excelente explicita ${profile.tradeoff} y el riesgo residual que queda.`,
      feedback: `Busca decision, no lista: activo afectado, amenaza plausible, control, evidencia y riesgo residual.`,
    }),
    () => ({
      prompt: `Escenario de revision: un equipo defiende "${concept}" diciendo que "${profile.assumption}". Redacta el contraargumento tecnico y una prueba segura.`,
      answer: `El supuesto debe probarse: si falla, ${profile.failure}. Usa una prueba autorizada como ${profile.safeTest}; si no produce ${profile.evidence}, el control no esta demostrado.`,
      feedback: `Una buena respuesta convierte confianza implicita en hipotesis falsable.`,
    }),
    () => ({
      prompt: `Escenario operativo: un incidente menor muestra que ${symptom}. ¿Como separas contencion inmediata, correccion de fondo y aprendizaje del equipo?`,
      answer: `Conten: limita el dano sobre ${profile.asset}. Corrige: aplica ${profile.control}. Aprende: documenta causa, dueno, monitoreo y ${profile.evidence} para verificar que no se repite.`,
      feedback: `Contener, corregir y aprender son capas distintas; mezclarlas produce parches fragiles.`,
    }),
    () => ({
      prompt: `Escenario de producto: una mejora de UX reduce friccion pero debilita ${concept}. Propone una alternativa que conserve utilidad sin ocultar el riesgo.`,
      answer: `Mantendria la utilidad solo si se conserva ${profile.control}, se observa ${profile.evidence} y se acepta explicitamente ${profile.tradeoff}. Si el riesgo residual supera el umbral, se redisenia.`,
      feedback: `La respuesta fuerte no dice "no" automatico: formula condiciones tecnicas para decidir.`,
    }),
    () => ({
      prompt: `Escenario de auditoria: el equipo afirma que ${unit.titulo} esta cubierto. Disena tres evidencias que pedirias y que hallazgo cambiaria tu decision.`,
      answer: `Pediria artefacto de diseno, prueba controlada y senal operativa: ${profile.evidence}. Cambiaria mi decision si el hallazgo muestra ${profile.failure} sin dueno ni monitoreo.`,
      feedback: `Auditar es buscar evidencia proporcional, no acumular capturas de pantalla.`,
    }),
  ];
  const spec = pick(frames, n - 1)();
  return {
    ...q,
    tipo: 'scenario',
    type: 'scenario',
    enunciado: clip(spec.prompt, 360),
    prompt: clip(spec.prompt, 360),
    solucion: clip(spec.answer, 520),
    answer: clip(spec.answer, 520),
    explicacion: clip(spec.feedback, 260),
    feedback: clip(spec.feedback, 260),
    concept,
    source_reference: `${unit.libro}; ${unit.lectura}`,
    common_mistake: clip(`Saltar directo a ${pick(profile.wrongs, n)} sin justificar activo, impacto, evidencia y tradeoff.`, 260),
    recognition_signal: clip(`Se reconoce cuando ${symptom} y la decision afecta ${profile.asset}.`, 220),
    metadata: revisedMetadata(q),
  };
}

function makeReflection(unit, q, profile, index) {
  const n = questionOrdinal(q, index);
  const concept = clean(q.concept) || pick(profile.concepts, n + 2) || profile.failure;
  const frames = [
    () => ({
      prompt: `Reflexion: elige un artefacto real de tu proyecto (diagrama, endpoint, notebook, dataset o runbook). ¿Donde aparece "${concept}" y que evidencia dejarias esta semana?`,
      answer: `Una respuesta fuerte elige un artefacto concreto, nombra ${profile.failure}, propone ${profile.control} y deja evidencia como ${profile.evidence}. Evita promesas generales.`,
    }),
    () => ({
      prompt: `Reflexion de transferencia: conecta "${concept}" con ${profile.related}. ¿Que patron profundo es el mismo y que cambia en el nuevo dominio?`,
      answer: `Debe reconocer el mismo limite de confianza o riesgo, pero ajustar activo, amenaza y control al dominio. La transferencia madura no copia herramientas: copia estructura de razonamiento.`,
    }),
    () => ({
      prompt: `Reflexion de criterio: describe una vez en que habrias aceptado "${pick(profile.wrongs, n)}". ¿Que senal te haria corregir esa decision hoy?`,
      answer: `La respuesta modelo identifica la tentacion real, la senal observable y el cambio de proceso. Debe incluir dueno, evidencia y condicion de revision.`,
    }),
    () => ({
      prompt: `Reflexion de diseno: si tuvieras que quitar un control por costo, ¿como decidirias si "${concept}" aun queda defendible?`,
      answer: `Compararia impacto, probabilidad, utilidad y evidencia. Si queda riesgo residual, lo documentaria con dueno y monitoreo; si no es aceptable, redisenaria en capas.`,
    }),
    () => ({
      prompt: `Reflexion de aprendizaje: formula una pregunta que harias a otro estudiante para detectar si entiende "${concept}" o solo memoriza palabras.`,
      answer: `La pregunta debe forzar un caso: activo, supuesto roto, control y evidencia. Una pregunta de definicion sola no basta para mostrar dominio.`,
    }),
  ];
  const spec = pick(frames, n - 1)();
  return {
    ...q,
    tipo: 'reflexion',
    type: 'reflexion',
    enunciado: clip(spec.prompt, 360),
    prompt: clip(spec.prompt, 360),
    solucion: clip(spec.answer, 520),
    answer: clip(spec.answer, 520),
    explicacion: 'Se evalúa por transferencia, especificidad del artefacto y evidencia verificable.',
    feedback: 'Aterriza la respuesta en una decisión concreta, no en una declaración de intenciones.',
    concept,
    source_reference: `${unit.libro}; ${unit.lectura}`,
    common_mistake: 'Responder con una intención vaga sin artefacto, dueño ni criterio de cierre.',
    recognition_signal: clip(`Puedes convertir ${concept} en una mejora semanal observable sobre ${profile.asset}.`, 220),
    metadata: revisedMetadata(q),
  };
}

function revisedMetadata(q) {
  return {
    ...(q.metadata ?? {}),
    generated_by: NEW_MARKER,
    quality_prompt: QUALITY_PROMPT,
    revised_on: '2026-06-17',
  };
}

function reviseQuestion(unit, q, profile, index) {
  if (!isReviewable(q)) return q;
  if (q.tipo === 'concepto') return makeQuiz(unit, q, profile, index);
  if (q.tipo === 'scenario') {
    const out = makeScenario(unit, q, profile, index);
    delete out.options;
    return out;
  }
  if (q.tipo === 'reflexion') {
    const out = makeReflection(unit, q, profile, index);
    delete out.options;
    return out;
  }
  return {
    ...q,
    metadata: revisedMetadata(q),
  };
}

function isReviewable(q) {
  return q.metadata?.generated_by === OLD_MARKER || q.metadata?.generated_by === NEW_MARKER;
}

function loadBaselineQuestions() {
  try {
    const raw = execFileSync('git', ['show', 'HEAD:data/ciberseguridad/_unidades.json'], {
      cwd: ROOT,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    });
    const doc = JSON.parse(raw);
    const map = new Map();
    for (const unit of doc.unidades ?? []) {
      for (const q of unit.banco ?? []) map.set(`${unit.id}:${q.id}`, q);
    }
    return map;
  } catch {
    return new Map();
  }
}

function clusterIdFor(unit) {
  return clusterByUnit.get(unit.id)?.id ?? 'sin-cluster';
}

function countReviewed(unit, q) {
  stats.byType[q.tipo] = (stats.byType[q.tipo] ?? 0) + 1;
  const clusterId = clusterIdFor(unit);
  stats.byCluster[clusterId] = (stats.byCluster[clusterId] ?? 0) + 1;
}

const samples = [];
const stats = {
  rewritten: 0,
  alreadyRevised: 0,
  preserved: 0,
  optionNormalized: 0,
  byType: {},
  byCluster: {},
};

for (const unit of unidadesDoc.unidades ?? []) {
  if (unit.bloque !== 'fase-8') continue;
  const profile = profileFor(unit);
  unit.banco = (unit.banco ?? []).map((q, index) => {
    if (!isReviewable(q)) {
      stats.preserved += 1;
      return normalizeMultipleChoice(unit, q, profile, index);
    }
    if (q.metadata?.generated_by === NEW_MARKER) {
      stats.alreadyRevised += 1;
      countReviewed(unit, q);
      const before = baselineQuestions.get(`${unit.id}:${q.id}`) ?? q;
      const after = normalizeMultipleChoice(unit, reviseQuestion(unit, q, profile, index), profile, index);
      maybeSample(unit, before, after);
      return after;
    }
    const before = q;
    const after = normalizeMultipleChoice(unit, reviseQuestion(unit, q, profile, index), profile, index);
    stats.rewritten += 1;
    countReviewed(unit, q);
    maybeSample(unit, baselineQuestions.get(`${unit.id}:${q.id}`) ?? before, after);
    return after;
  });
}

writeFileSync(unidadesPath, `${JSON.stringify(unidadesDoc, null, 2)}\n`, 'utf8');
writeFileSync(progresoPath, progresoMarkdown(stats, samples), 'utf8');

console.log(
  `OK: banco fase-8 revisado. Reescritas=${stats.rewritten}. Ya revisadas=${stats.alreadyRevised}. Conservadas=${stats.preserved}. Marcador=${NEW_MARKER}.`
);

function progresoMarkdown(result, sampleRows) {
  const clusterLines = Object.entries(result.byCluster)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([clusterId, count]) => `| ${clusterId} | ${count} |`)
    .join('\n');
  const typeLines = Object.entries(result.byType)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([type, count]) => `| ${type} | ${count} |`)
    .join('\n');
  const sampleText = sampleRows
    .map(({ unit, before, after }, i) => {
      const oldOptions = (before.options ?? []).slice(0, 4).map((o) => `  - ${clip(o, 150)}`).join('\n');
      const newOptions = (after.options ?? []).slice(0, 4).map((o) => `  - ${clip(o, 150)}`).join('\n');
      return [
        `### Muestra ${i + 1}: ${unit}`,
        '',
        '**Antes**',
        '',
        `Enunciado: ${before.enunciado}`,
        oldOptions ? `Opciones:\n${oldOptions}` : '',
        '',
        '**Despues**',
        '',
        `Enunciado: ${after.enunciado}`,
        newOptions ? `Opciones:\n${newOptions}` : '',
      ].filter(Boolean).join('\n');
    })
    .join('\n\n');

  return `# Progreso calidad banco Fase 8

Fecha: 2026-06-17  
Prompt ejecutado: \`${QUALITY_PROMPT}\`  
Marcador aplicado: \`${NEW_MARKER}\`

## Resumen

| Estado | Preguntas |
|---|---:|
| Reescritas en esta corrida desde marcador generado | ${result.rewritten} |
| Protegidas con marcador de revision | ${result.rewritten + result.alreadyRevised} |
| Conservadas sin tocar | ${result.preserved} |
| Normalizadas en capa interactiva MC | ${result.optionNormalized} |

## Protegidas por tipo

| Tipo | Preguntas |
|---|---:|
${typeLines}

## Protegidas por cluster

| Cluster | Preguntas |
|---|---:|
${clusterLines}

## Muestras antes -> despues

${sampleText}

## Criterios aplicados

- Opcion multiple: 4 opciones, una correcta exacta, distractores plausibles y concisos.
- Escenarios/reflexiones: sin \`options\`, con decision defensiva, evidencia y riesgo residual.
- Alcance: solo preguntas con \`metadata.generated_by === "${OLD_MARKER}"\`.
- Proteccion futura: el marcador viejo queda reemplazado para que el generador no destruya esta revision.
`;
}

function maybeSample(unit, before, after) {
  if (samples.length >= 3) return;
  if (!['cyber-ms1', 'cyber-web1', 'cyber-llm2'].includes(unit.id)) return;
  if (before.id === after.id) samples.push({ unit: unit.id, before, after });
}

function normalizeMultipleChoice(unit, q, profile, index) {
  if (q.tipo !== 'concepto' || !Array.isArray(q.options)) return q;
  const shouldRefreshManual = !isReviewable(q);
  const hasBadShape = q.options.length !== 4 || !q.options.includes(q.answer);
  const hasLongOption = q.options.some((option) => String(option ?? '').length > 180);
  if (!shouldRefreshManual && !hasBadShape && !hasLongOption) return q;

  const answer = conciseAnswer(q);
  const options = unique([answer, ...wrongOptions(profile, answer, index + 3)]).slice(0, 4);
  while (options.length < 4) options.push(`Aceptar el riesgo sin evidencia verificable ${options.length}.`);
  stats.optionNormalized += 1;
  return {
    ...q,
    type: q.type ?? typeFor(q),
    prompt: q.prompt ?? q.enunciado,
    answer,
    options,
    source_reference: q.source_reference ?? `${unit.libro}; ${unit.lectura}`,
  };
}

function conciseAnswer(q) {
  const raw = capitalize(clean(q.solucion ?? q.answer ?? q.options?.[0] ?? '').replace(/^Que\s+/i, ''));
  if (raw.length <= 170) return raw;
  const semicolon = raw.split(';').slice(0, 2).join(';').trim();
  if (semicolon.length >= 60 && semicolon.length <= 170) return semicolon;
  const firstSentence = raw.match(/^(.+?[.!?])\s/)?.[1];
  if (firstSentence && firstSentence.length <= 170 && !/\b(?:p|ej)\.$/i.test(firstSentence)) return firstSentence;
  return clip(raw, 170);
}

function capitalize(text) {
  return text ? `${text[0].toLocaleUpperCase('es-MX')}${text.slice(1)}` : text;
}
