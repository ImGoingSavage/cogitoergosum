# Gobernar un sistema con LLMs: red teaming, evaluación y defensa en profundidad

> Recurso troncal: **OWASP Top 10 for LLM Applications 2025**. Capstone de la fase: integrar todos los riesgos LLM en un sistema **gobernado y evaluado**. Reúne [[cyber-llm1]]–[[cyber-llm4]] y prepara el mini-proyecto del cluster.

## De qué trata (y qué sabrás hacer al final)

Has visto los riesgos uno a uno: inyección ([[cyber-llm1]]), RAG y agencia ([[cyber-llm2]]), fuga ([[cyber-llm3]]), supply chain/poisoning/consumo ([[cyber-llm4]]). Un sistema LLM seguro no aplica una defensa contra cada uno por separado: monta **defensa en profundidad** y la **evalúa adversarialmente** de forma continua, porque —como con la prevención clásica— ninguna mitigación de LLM es perfecta. Esta lección te da el marco para gobernar el conjunto.

La intuición: asegurar un sistema con LLMs es como dirigir un equipo con un miembro talentoso pero **ingenuo y locuaz** (el modelo). No lo "arreglas" haciéndolo infalible; lo rodeas de **estructura**: límites a lo que puede hacer, verificación de lo que produce, y pruebas regulares de "a ver si te engaño" antes de que lo haga un atacante real. La gobernanza es esa estructura.

Al terminar podrás: (1) montar **defensa en profundidad** para un sistema LLM; (2) hacer **red teaming/evaluación adversaria** de un LLM; (3) ubicar al humano y al monitoreo en el lazo; y (4) ejecutar el mini-proyecto del cluster.

## Defensa en profundidad para LLMs

Como ninguna capa basta (no hay "parametrización" perfecta contra prompt injection, [[cyber-llm1]]), se apilan capas independientes:

- **Entrada:** tratar todo contenido externo/RAG como no confiable; control de acceso por documento ([[cyber-llm2]], [[cyber-llm3]]).
- **Modelo/contexto:** no poner secretos en el prompt ([[cyber-llm3]]); minimizar el contexto; procedencia del modelo ([[cyber-llm4]]).
- **Capacidades:** **agencia mínima** (LLM06) — pocas herramientas, permisos estrechos, aislamiento del código ([[cyber-llm2]], [[cyber-sys4]]).
- **Salida:** tratar la salida como no confiable (LLM05), validarla/sanearla antes de usarla o actuar.
- **Acción:** humano en el lazo para lo sensible/irreversible; confirmación explícita.
- **Operación:** rate limiting y cuotas (LLM10); monitoreo de abuso y deriva ([[cyber-blue2]]).

El objetivo: que **una** capa que falle (una inyección exitosa) no se traduzca en daño, porque las demás contienen.

## Red teaming y evaluación adversaria

No sabrás si tu sistema resiste hasta que intentes romperlo **tú** primero. El **red teaming de LLMs** es probar sistemáticamente —de forma autorizada— prompt injections directas e indirectas, intentos de extraer el system prompt, de hacer que use mal una herramienta, de filtrar datos del RAG, de evadir filtros. Es la **emulación adversaria** de [[cyber-blue5]] aplicada a IA: lo que logra pasar es una brecha que priorizas y cierras, y se re-evalúa tras cada cambio (modelo nuevo, prompt nuevo, herramienta nueva). Las evaluaciones automatizadas de seguridad ayudan a que esto sea continuo, no un examen único.

## Humano y monitoreo en el lazo

Dos controles transversales:
- **Humano en el lazo** para decisiones de alto impacto: el LLM propone, una persona aprueba lo irreversible (enviar dinero, borrar, comunicar al exterior).
- **Monitoreo:** registrar entradas/salidas (cuidando privacidad, [[cyber-dp4]]) para detectar abuso, fugas y deriva; alimenta la respuesta a incidentes ([[cyber-blue4]]).

## Mini-ejemplo trabajado

Vas a desplegar un asistente RAG corporativo con herramientas (correo, tickets). Gobernanza integrada:

- **Capas:** RAG con control de acceso por usuario y contenido marcado no confiable; sin secretos en el prompt; agencia mínima (correo solo interno con confirmación humana); salida validada antes de actuar; rate limiting/cuotas; monitoreo.
- **Red teaming antes de lanzar:** intentar inyección indirecta vía un correo indexado, extraer el system prompt, hacer que mande datos de RRHH afuera, abusar del consumo. Cada éxito → brecha a cerrar.
- **Operación:** re-evaluar al cambiar el modelo o añadir una herramienta; monitorear y tener runbook de incidente ([[cyber-blue4]]).
- **Riesgo residual:** una inyección puede ensuciar una respuesta, pero no exfiltrar ni actuar sin aprobación → se acepta, documenta y vigila ([[cyber-ms5]]).

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| Una sola mitigación contra prompt injection | Falta defensa en profundidad |
| Nunca se hizo red teaming del asistente | Robustez desconocida |
| Agente con herramientas potentes sin humano en el lazo | Una inyección = acción real |
| Sin re-evaluar tras cambiar modelo/prompt/herramienta | Brechas nuevas sin detectar |
| Sin monitoreo de entradas/salidas | Abuso y fuga invisibles |

## Errores típicos

- **Buscar la "defensa definitiva" contra inyección:** no existe; se apilan capas y se limita el impacto.
- **Evaluar una vez:** cada cambio (modelo, prompt, herramienta) puede abrir una brecha; el red teaming es continuo.
- **Dar agencia sin humano en el lazo:** convierte un fallo del modelo en daño irreversible.

## Contraejemplo y caso borde

- **Contraejemplo:** un asistente con las seis capas, red-teameado antes de lanzar y re-evaluado en cada cambio, con humano en el lazo y monitoreo: las inyecciones que pasan no causan daño grave y se detectan. Gobernanza en acción.
- **Caso borde:** los sistemas **multi-agente** ([[cyber-llm2]]) y los modelos que se actualizan solos amplían la superficie entre evaluaciones: una capacidad nueva o un agente añadido puede invalidar pruebas previas. La gobernanza debe **gatear los cambios** (evaluar antes de habilitar), no solo evaluar al inicio.

## Transferencia a ciencia de datos e IA

Este capstone integra toda la ruta: defensa en profundidad ([[cyber-ms2]]), agencia mínima = least privilege ([[cyber-ms2]], [[cyber-web2]]), salida no confiable = validación ([[cyber-dev1]], [[cyber-web1]]), red teaming = emulación adversaria ([[cyber-blue5]]), monitoreo y respuesta ([[cyber-blue2]], [[cyber-blue4]]), y gobernanza/riesgo residual ([[cyber-mls5]], [[cyber-ms5]]). Construir IA segura **es** aplicar toda la ciberseguridad, a la vez, a un sistema que lee datos no confiables y actúa.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** diseña un plan de red teaming para el asistente del ejemplo (5 ataques a intentar y qué brecha revelaría cada uno).
- **Misión externa (lab vivo):** recorre el **OWASP Top 10 for LLM Applications 2025** (https://genai.owasp.org/llm-top-10/) y el **OWASP GenAI Security Project** (https://genai.owasp.org/) buscando guías de evaluación/red teaming. **Criterio de cierre:** listar 3 pruebas adversarias que aplicarías.
- **Mini-entregable (mini-proyecto del cluster):** un **checklist de seguridad para un asistente RAG** conectado a documentos privados, base de datos, herramientas y acciones externas, cubriendo LLM01–LLM10 con la mitigación de cada uno y un plan de red teaming. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** un sistema LLM seguro se **gobierna**, no se "arregla": **defensa en profundidad** en seis capas (entrada, contexto, capacidades con **agencia mínima**, salida no confiable, acción con humano en el lazo, operación con límites y monitoreo) para que una inyección exitosa no cause daño; **red teaming continuo** (emulación adversaria aplicada a IA) que se re-ejecuta tras cada cambio y **gatea** capacidades nuevas; y **monitoreo + respuesta** para lo que pase. Es aplicar toda la ciberseguridad, a la vez, a un sistema que lee lo no confiable y actúa.

---

**Referencias**

- OWASP Foundation. (2024). *OWASP Top 10 for LLM Applications 2025*. https://genai.owasp.org/llm-top-10/
- OWASP Foundation. (n.d.). *OWASP GenAI Security Project*. https://genai.owasp.org/
- National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1

*Retrieval: (1) ¿cuáles son las capas de defensa en profundidad de un sistema LLM?; (2) ¿qué es el red teaming de LLMs y por qué es continuo?; (3) ¿dónde entra el humano en el lazo?; (4) ¿por qué los cambios (modelo/herramienta) deben gatearse?*
