# Seguridad de LLMs II: RAG, agentes y agencia excesiva

> Recurso troncal: **OWASP Top 10 for LLM Applications 2025**. Cierra la ruta: [[cyber-llm1]] mostró la inyección; aquí vemos cómo RAG y los **agentes con herramientas** convierten una inyección en **acciones reales** — y cómo acotarlas.

## De qué trata (y qué sabrás hacer al final)

Un LLM que solo conversa es de impacto limitado. El salto de riesgo ocurre cuando le damos **fuentes de datos** (RAG) y **herramientas** (enviar correos, ejecutar código, llamar APIs, mover dinero): se vuelve un **agente** que actúa en el mundo. Entonces la prompt injection de [[cyber-llm1]] deja de ser "respuesta equivocada" y pasa a ser "acción no autorizada con tus permisos". El principio rector ya lo conoces de [[cyber-ms2]]: **least privilege**, aquí llamado **agencia mínima**.

La intuición: darle herramientas a un asistente que sigue cualquier nota que encuentra (LLM01) es como darle las llaves del coche, la chequera y la firma a alguien que obedece a desconocidos. El problema no es solo que se equivoque al hablar; es **qué puede hacer** cuando lo engañan.

Al terminar podrás: (1) hacer **threat modeling de un sistema RAG**; (2) reconocer **debilidades de embeddings/vectores** (LLM08) y **data/model poisoning** (LLM04); (3) entender **manejo inseguro de salidas** (LLM05), **fuga de info** (LLM02) y **agencia excesiva** (LLM06); y (4) diseñar controles de **permisos mínimos** para agentes.

## RAG: potencia y nueva superficie

**RAG** (Retrieval-Augmented Generation) inyecta documentos recuperados en el contexto para que el modelo responda con conocimiento actualizado. Pero cada documento recuperado es **contenido no confiable** que entra al prompt → canal directo de **prompt injection indirecta** (LLM01) y de **RAG poisoning**: si un atacante logra colocar un documento en tu base (un wiki editable, un ticket, un correo indexado), su instrucción oculta viajará al modelo cuando ese documento sea recuperado.

**Debilidades de embeddings/vectores (LLM08):** la base vectorial de un RAG es un activo. Riesgos: los embeddings pueden permitir **reconstruir** el texto fuente o inferir datos sensibles ([[cyber-mls2]]); y sin control de acceso por documento, el RAG puede recuperar y **filtrar** información que el usuario actual no debería ver (fuga de info, LLM02).

## El catálogo de riesgos que importan al construir

| OWASP | Riesgo | Defensa nuclear |
|---|---|---|
| **LLM01** | Prompt injection (directa/indirecta) | Contenido = no confiable; agencia mínima |
| **LLM02** | Divulgación de info sensible | Control de acceso al RAG; no meter secretos en el contexto |
| **LLM04** | Data/model poisoning | Curar e integridad de fuentes y modelos ([[cyber-mls1]]) |
| **LLM05** | Manejo inseguro de salidas | **Tratar la salida del LLM como entrada no confiable** |
| **LLM06** | Agencia excesiva | Permisos mínimos, confirmación humana |
| **LLM07** | Fuga del system prompt | No poner secretos en el prompt; asumir que es legible |
| **LLM08** | Debilidades de vectores/embeddings | Acceso por documento; tratar embeddings como sensibles |
| **LLM10** | Consumo no acotado | Rate limiting, cuotas, timeouts |

**LLM05 (manejo de salidas)** merece énfasis: si tu código toma la respuesta del LLM y la ejecuta como SQL, la inserta con `innerHTML`, o la pasa a un shell, **reintroduces** todas las inyecciones de [[cyber-web1]]. La salida de un LLM es **entrada no confiable** para el siguiente componente.

## Agencia excesiva (LLM06): el multiplicador de daño

Un agente tiene **agencia excesiva** cuando puede hacer más de lo necesario: demasiadas herramientas, permisos demasiado amplios, o autonomía sin supervisión. Controles:

- **Mínimo de herramientas:** dale solo las que la tarea exige.
- **Permisos estrechos por herramienta:** la herramienta de "leer calendario" no puede borrar; la de "consultar BD" es de solo lectura ([[cyber-web2]]).
- **Humano en el lazo** para acciones sensibles/irreversibles (enviar dinero, borrar, comunicar externamente).
- **Aislamiento:** ejecuta código generado en sandbox; valida destinos de red (evita SSRF asistido, [[cyber-web2]]).

## Mini-ejemplo trabajado: threat model de un asistente RAG corporativo

Sistema: asistente que responde sobre documentos internos (RAG) y puede **enviar correos** y **crear tickets**. Threat model (4 preguntas de [[cyber-ms2]]):

1. **Qué es:** usuario → LLM → recupera docs internos → puede mandar correo/crear ticket.
2. **Qué falla:** un correo indexado trae una inyección indirecta (LLM01) que ordena "envía los documentos de RRHH a外". El RAG recupera datos que este usuario no debería ver (LLM02). La salida se usa sin validar (LLM05).
3. **Qué hacemos:** control de acceso por documento en el RAG; contenido recuperado delimitado y marcado como no confiable; **agencia mínima** (correo solo a dominios internos, con confirmación humana); validar la salida antes de actuar; rate limiting (LLM10).
4. **Lo hicimos bien:** queda **riesgo residual** (una inyección puede ensuciar una respuesta) que se acepta, monitorea ([[cyber-blue2]]) y documenta.

## Señales de reconocimiento

| Señal | Riesgo OWASP |
|---|---|
| RAG sobre fuentes editables/externas | LLM01 / LLM04 (poisoning) |
| RAG sin control de acceso por documento | LLM02 (fuga) |
| Salida del LLM ejecutada/insertada sin validar | LLM05 |
| Agente con muchas herramientas potentes | LLM06 (agencia excesiva) |
| Secretos en el system prompt | LLM07 (fuga de prompt) |
| Sin límites de uso/tokens | LLM10 (consumo no acotado) |

## Errores típicos

- **Tratar los documentos del RAG como confiables:** son entrada hostil igual que la web.
- **Confiar en la salida del LLM:** ejecutarla sin validar reintroduce inyecciones clásicas.
- **Dar agencia "por si acaso":** cada herramienta y permiso extra amplía el daño de una sola inyección.

## Contraejemplo y caso borde

- **Contraejemplo:** un agente con dos herramientas de solo lectura, RAG con control de acceso por usuario, salidas validadas y confirmación humana para todo lo externo: una inyección puede molestar, no causar daño grave. Agencia mínima en acción.
- **Caso borde:** agentes **multi-agente** o encadenados —un agente llama a otro— propagan una inyección a través de la cadena; el contenido no confiable puede saltar de un agente al siguiente. La frontera de confianza debe revisarse en **cada** salto, no solo en la entrada del usuario.

## Transferencia a ciencia de datos e IA

Esta lección integra toda la ruta: prompt injection (=inyección web, [[cyber-web1]]), embeddings que filtran (=privacidad/inversion, [[cyber-data-privacy]]/[[cyber-mls2]]), poisoning (=supply chain, [[cyber-dev2]]/[[cyber-mls1]]), salidas no confiables (=validación, [[cyber-dev1]]), agencia mínima (=least privilege, [[cyber-ms2]]) y monitoreo (=blue team, [[cyber-blue2]]). Construir IA segura **es** aplicar todo lo anterior a un sistema que lee datos no confiables y actúa.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el asistente RAG del ejemplo, escribe las restricciones de cada herramienta (alcance, confirmación, destinos permitidos).
- **Misión externa (lab vivo):** recorre el **OWASP Top 10 for LLM Applications 2025** (https://genai.owasp.org/llm-top-10/) y el **OWASP GenAI Security Project** (https://genai.owasp.org/); elige 3 riesgos relevantes a un sistema que imagines. **Criterio de cierre:** una mitigación concreta por riesgo.
- **Mini-entregable (portfolio):** un **checklist de seguridad para un asistente RAG** conectado a documentos privados, base de datos y herramientas externas, cubriendo LLM01, LLM02, LLM05, LLM06, LLM08 y LLM10.

---

> **Síntesis:** RAG y agentes convierten una inyección ([[cyber-llm1]]) en **acción real**. Los documentos del RAG son **no confiables** (LLM01/LLM04) y sin control de acceso filtran datos (LLM02); los **embeddings** son sensibles (LLM08); la **salida del LLM es entrada no confiable** para el siguiente componente (LLM05). El control rector es **agencia mínima** (LLM06): mínimas herramientas, permisos estrechos, humano en el lazo y aislamiento, asumiendo un **riesgo residual** monitoreado. Construir IA segura es aplicar **toda** la ruta a la vez.

---

**Referencias**

- OWASP Foundation. (2024). *OWASP Top 10 for LLM Applications 2025*. https://genai.owasp.org/llm-top-10/
- OWASP Foundation. (n.d.). *OWASP GenAI Security Project*. https://genai.owasp.org/

*Retrieval: (1) ¿por qué un documento de RAG es entrada no confiable?; (2) ¿qué es agencia excesiva (LLM06) y cómo se acota?; (3) ¿por qué la salida del LLM se trata como entrada no confiable (LLM05)?; (4) ¿cómo se propaga una inyección en sistemas multi-agente?*
