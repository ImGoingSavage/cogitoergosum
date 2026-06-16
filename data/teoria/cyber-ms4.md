# Sistemas sociotécnicos: confianza, abuso y el eslabón humano

> Recurso troncal: **Anderson, *Security Engineering* (3.ª ed.)**. La seguridad no vive solo en el código: vive en personas, procesos y la confianza entre ellos. Sigue a [[cyber-ms3]] (economía) y prepara [[cyber-ms5]] (resiliencia y comunicación).

## De qué trata (y qué sabrás hacer al final)

Los ataques más efectivos rara vez "rompen" la criptografía: rompen a las **personas** y a los **procesos** que rodean la tecnología. Un sistema es **sociotécnico** —técnico + humano + organizativo— y su seguridad es tan fuerte como su eslabón social más débil. Modelar solo lo técnico es como blindar la puerta y dejar la llave bajo el tapete.

La intuición: la estafa telefónica que convence a un empleado de "verificar su contraseña" no explota un bug del servidor; explota la **confianza** y la prisa. El sistema falló sin que ninguna línea de código fallara. Pensar en seguridad exige incluir al humano dentro del modelo de amenaza, no fuera.

Al terminar podrás: (1) razonar la **confianza** como decisión explícita (¿en quién/qué confío y por qué?); (2) construir **casos de abuso** (cómo se usa mal lo que diseñas); (3) entender la **ingeniería social** y el **insider** como propiedades del sistema; y (4) ubicar el **eslabón humano** dentro del threat model.

## La confianza como decisión, no como supuesto

Cada sistema confía en algo: en que el usuario es quien dice, en que la librería no es maliciosa ([[cyber-dev2]]), en que el documento que el RAG recupera es benigno ([[cyber-llm-rag-agents]]). El error es confiar **implícitamente**. La disciplina es hacer la confianza **explícita**: listar en quién/qué confías, qué pasa si esa confianza se traiciona, y reducir la **base de confianza** (cuántas partes deben portarse bien para que el sistema esté seguro). Cuanto más pequeña, mejor.

## Casos de abuso: el reverso de los casos de uso

Diseñamos pensando en **casos de uso** (qué debe hacer el sistema). La seguridad exige **casos de abuso**: cómo un actor malicioso —o uno legítimo descuidado— usaría lo mismo para dañar. Por cada "el usuario sube su foto de perfil", pregunta "¿y si sube un script? ¿un archivo de 10 GB? ¿la foto de otra persona?". El caso de abuso es el threat model ([[cyber-ms2]]) aplicado a cada funcionalidad.

## Ingeniería social y el insider

- **Ingeniería social:** manipular a una persona para que rompa la seguridad (phishing, pretexting, urgencia falsa). No se defiende solo con tecnología, sino con procesos (verificación por canal aparte, cultura de "está bien dudar") y con reducir lo que un solo engañado puede causar (least privilege, [[cyber-ms2]]).
- **Insider:** alguien con acceso legítimo que abusa de él (o cuya cuenta es secuestrada). Es difícil porque no "entra" (ya está dentro); se aborda con separación de funciones, mínimo privilegio, auditoría y detección por comportamiento anómalo ([[cyber-blue2]]).

Ambos comparten una lección: la seguridad debe asumir que **una parte confiable puede fallar** y limitar el daño cuando lo haga.

## Mini-ejemplo trabajado

Un asistente recibe un correo "del CEO" pidiendo con urgencia el export de la base de usuarios a una dirección externa. Análisis sociotécnico:

- **Confianza explotada:** la autoridad aparente del remitente y la urgencia (clásico de ingeniería social).
- **Caso de abuso no contemplado:** el proceso permitía exportar y enviar datos a un externo con una sola persona y sin verificación.
- **Defensa sociotécnica:** verificación por canal independiente para acciones sensibles, separación de funciones (exportar requiere una segunda aprobación), least privilege (la cuenta del asistente no puede exportar toda la base), y registro/auditoría. Ninguna es criptográfica; todas son del sistema humano-organizativo.
- **Conexión con IA:** el mismo patrón —autoridad falsa inyectada para inducir una acción— es la **prompt injection** de [[cyber-llm-rag-agents]]. El LLM es el "empleado crédulo" que obedece la nota del atacante.

## Señales de reconocimiento

| Señal | Riesgo sociotécnico |
|---|---|
| "Confiamos en que el usuario/archivo/proveedor es legítimo" | Confianza implícita sin plan B |
| Una sola persona puede hacer una acción crítica | Falta separación de funciones |
| Urgencia + autoridad en una petición inusual | Ingeniería social |
| El acceso legítimo no se audita | Insider invisible |
| Solo se diseñaron casos de uso, no de abuso | Funcionalidad sin threat model |

## Errores típicos

- **Sacar al humano del modelo de amenaza:** "eso es problema de las personas, no del sistema" — la persona es parte del sistema.
- **Confiar implícitamente:** no nombrar en quién/qué se confía hasta que la confianza se rompe.
- **Culpar a la víctima de phishing:** si un engaño individual hunde todo, el fallo es de diseño (faltó limitar el daño), no solo de la persona.

## Contraejemplo y caso borde

- **Contraejemplo:** una organización donde dudar y verificar es la norma cultural y las acciones sensibles exigen dos personas: una sola persona engañada no causa daño grave. La resiliencia social acotó el impacto.
- **Caso borde:** demasiados controles humanos (verificaciones, aprobaciones) generan fricción y se evaden ([[cyber-ms2]]); el diseño sociotécnico equilibra seguridad y usabilidad, no maximiza una a costa de la otra.

## Transferencia a ciencia de datos e IA

La confianza explícita es la base de la **provenance** de datos y modelos ([[cyber-ml-security]]) y de tratar el contenido del RAG como no confiable ([[cyber-llm-rag-agents]]). Los casos de abuso son los que descubren el data poisoning ([[cyber-ml-security]]) y la prompt injection. Y el insider/anomalía es el puente con la detección de [[cyber-blue2]]. Construir IA segura es, en buena parte, ingeniería sociotécnica.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** toma una funcionalidad de un sistema y escribe 3 casos de abuso con su mitigación.
- **Misión externa (lab vivo):** revisa material introductorio de ingeniería social/phishing (p. ej. recursos del **NIST CSF**, https://www.nist.gov/cyberframework, función *Protect: Awareness*). **Criterio de cierre:** describir una defensa de proceso (no técnica) contra phishing.
- **Mini-entregable:** un mapa de confianza de un sistema: en quién/qué confía, qué pasa si cada confianza se traiciona, y cómo se limita el daño.

---

> **Síntesis:** la seguridad es **sociotécnica**: personas y procesos están dentro del modelo de amenaza. Haz la **confianza explícita** y minimiza la base de confianza; diseña **casos de abuso** junto a los de uso; y asume que una parte confiable puede fallar (**ingeniería social, insider**), limitando el daño con separación de funciones, mínimo privilegio, verificación por canal aparte y auditoría. El mismo patrón "autoridad falsa que induce una acción" reaparece como prompt injection en IA.

---

**Referencias**

- Anderson, R. (2020). *Security engineering: A guide to building dependable distributed systems* (3rd ed.). Wiley.
- National Institute of Standards and Technology. (2018). *Framework for improving critical infrastructure cybersecurity* (v1.1). https://www.nist.gov/cyberframework

*Retrieval: (1) ¿por qué hacer la confianza explícita y reducir la base de confianza?; (2) qué es un caso de abuso; (3) ¿cómo se aborda el insider si "ya está dentro"?; (4) ¿qué paralelo hay entre ingeniería social y prompt injection?*
