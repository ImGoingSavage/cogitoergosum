# Supply chain, poisoning y consumo no acotado: LLM03, LLM04 y LLM10

> Recurso troncal: **OWASP Top 10 for LLM Applications 2025**. Lleva la supply chain ([[cyber-dev2]], [[cyber-mls5]]) al mundo de los LLMs. Sigue a [[cyber-llm3]] (fuga) y prepara [[cyber-llm5]] (gobernanza y evaluación).

## De qué trata (y qué sabrás hacer al final)

Construir con LLMs es ensamblar componentes de terceros: modelos base, *fine-tunes*, adapters, datasets de entrenamiento/RAG, plugins y librerías. Cada uno es una **dependencia** con su riesgo, y el modelo puede ser **envenenado** por los datos que ingiere. Además, a diferencia del software clásico, cada petición cuesta **cómputo y dinero**, así que el abuso de recursos es un riesgo de primera clase. Esta lección cubre tres riesgos OWASP que un DS subestima.

La intuición: un LLM en producción es como un chef que usa ingredientes de muchos proveedores (LLM03 supply chain), que puede ser saboteado si alguien adultera la despensa de la que aprende (LLM04 poisoning), y cuya cocina puede colapsar —o vaciarte la cuenta— si llegan diez mil pedidos gigantes a la vez (LLM10 consumo no acotado).

Al terminar podrás: (1) evaluar la **supply chain de un LLM (LLM03)**; (2) explicar **data y model poisoning (LLM04)** incluido el del RAG; (3) razonar el **consumo no acotado (LLM10)**; y (4) elegir controles proporcionales.

## LLM03: supply chain de un LLM

La cadena de un sistema LLM incluye: el **modelo base** (¿de quién? ¿verificable?), **fine-tunes/adapters** de terceros, **datasets** de entrenamiento y de RAG, **plugins/herramientas** y las **librerías** ([[cyber-dev2]]). Riesgos:

- Un modelo o adapter de origen desconocido puede traer un **backdoor** ([[cyber-mls1]]) o **ejecutar código al cargarse** según el formato ([[cyber-web5]], pickle).
- Un plugin/herramienta malicioso o vulnerable amplía lo que un atacante puede hacer ([[cyber-llm2]], agencia).
- Defensa: **provenance** (origen verificable, integridad por hash/firma — [[cyber-sys2]]), preferir formatos sin ejecución (safetensors), y aplicar SBOM/SCA a las librerías ([[cyber-dev2]]). Igual que [[cyber-mls5]]: integridad ≠ confianza en el origen.

## LLM04: data y model poisoning

Si un atacante influye en los datos de los que el modelo aprende —en pre-entrenamiento, **fine-tuning**, o en la **base del RAG**— moldea su comportamiento ([[cyber-mls1]]):

- **Fine-tune poisoning:** datos de ajuste manipulados introducen sesgos o backdoors.
- **RAG poisoning:** un atacante coloca un documento en tu base (un wiki editable, un ticket, un correo indexado) con contenido que sesga las respuestas o lleva una **inyección indirecta** ([[cyber-llm1]]) que se dispara al ser recuperado.
- **Feedback poisoning:** si reentrenas con feedback de usuarios sin control, lo envenenan (como el detector de fraude de [[cyber-mls1]]).

Defensa: **curar y verificar** las fuentes, controlar quién puede escribir en la base del RAG, limitar la influencia de fuentes no confiables, y tratar **todo** documento recuperado como no confiable ([[cyber-llm2]]).

## LLM10: consumo no acotado

Cada inferencia consume cómputo, memoria y, en APIs de pago, **dinero**. Sin límites, un atacante (o un bug) puede: agotar recursos y tumbar el servicio (DoS), provocar costos enormes ("denial of wallet"), o abusar de la ventana de contexto con entradas gigantes. Defensa: **rate limiting** por usuario, **límites de longitud** de entrada y salida, **cuotas y presupuestos**, timeouts, y monitoreo de uso anómalo ([[cyber-blue2]]). Es el mismo principio que el rate limiting de APIs ([[cyber-web3]]), pero el costo por petición lo hace más urgente.

## Mini-ejemplo trabajado

Montas un asistente que: usa un modelo base bajado de un repo público, se afina con datos de un proveedor, responde por RAG sobre un wiki interno **editable por cualquier empleado**, y expone una API sin límites. Riesgos:

- **LLM03:** el modelo base/adapter podría traer backdoor o ejecutar código al cargar → verificar procedencia, formato sin ejecución, cargar aislado ([[cyber-sys4]]).
- **LLM04:** un empleado (o una cuenta comprometida) edita el wiki con contenido envenenado/inyección → control de quién escribe, tratar lo recuperado como no confiable.
- **LLM10:** alguien envía miles de prompts enormes → costos disparados y DoS → rate limiting, límites de tokens, cuotas.
- **Resultado:** los tres riesgos "aburridos" pero frecuentes, cerrados con controles baratos.

## Señales de reconocimiento

| Señal | Riesgo OWASP |
|---|---|
| Modelo/adapter de origen no verificado | LLM03 (backdoor / ejecución) |
| Base de RAG escribible sin control | LLM04 (RAG poisoning) |
| Reentrenar con feedback sin curar | LLM04 (feedback poisoning) |
| API de LLM sin rate limit ni cuotas | LLM10 (DoS / denial of wallet) |
| Sin límite de longitud de entrada | LLM10 (abuso de contexto) |

## Errores típicos

- **Confiar en un modelo por popular:** la popularidad no es procedencia verificada ([[cyber-dev2]], [[cyber-mls5]]).
- **RAG sobre fuentes editables sin control de escritura:** canal directo de poisoning e inyección indirecta.
- **Olvidar los límites de consumo:** el costo por petición convierte el abuso en daño financiero real.

## Contraejemplo y caso borde

- **Contraejemplo:** modelo con procedencia verificada y formato sin ejecución, base de RAG con control de escritura y contenido tratado como no confiable, y API con rate limiting y cuotas: la supply chain, el poisoning y el consumo quedan acotados.
- **Caso borde:** el **poisoning lento** —pocos documentos/feedback envenenados a lo largo del tiempo— evade los controles que miran cambios bruscos; requiere monitorear la deriva del comportamiento del modelo, no solo cambios puntuales (paralelo al "lento y bajo" de [[cyber-blue2]]).

## Transferencia a ciencia de datos e IA

LLM03/LLM04 son la supply chain de [[cyber-dev2]] y [[cyber-mls5]] aplicada a modelos y datos de LLM; el RAG poisoning une poisoning ([[cyber-mls1]]) con inyección indirecta ([[cyber-llm1]]); y LLM10 es el rate limiting de [[cyber-web3]] con la urgencia añadida del costo. Construir con LLMs no exime de la higiene de supply chain; la intensifica.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el asistente del ejemplo, define el control de procedencia del modelo, el control de escritura del RAG y los límites de consumo.
- **Misión externa (lab vivo):** lee **LLM03, LLM04 y LLM10** en el **OWASP Top 10 for LLM Applications 2025** (https://genai.owasp.org/llm-top-10/). **Criterio de cierre:** dar una mitigación concreta por riesgo.
- **Mini-entregable:** una mini "BOM de IA" de un sistema LLM (modelo base, adapters, datasets, plugins, librerías) con la verificación de procedencia y los límites de consumo de cada uno.

---

> **Síntesis:** construir con LLMs es ensamblar terceros: **LLM03** exige verificar la **provenance** del modelo base, adapters, datasets, plugins y librerías (riesgo de backdoor y ejecución al cargar); **LLM04** es **poisoning** de fine-tuning, de la **base del RAG** (fuentes editables) y del feedback, que se mitiga curando fuentes y controlando quién escribe; y **LLM10** es el **consumo no acotado** (DoS y "denial of wallet") que el costo por petición vuelve urgente, frenado con rate limiting, cuotas y límites de longitud. Cuidado con el poisoning **lento**.

---

**Referencias**

- OWASP Foundation. (2024). *OWASP Top 10 for LLM Applications 2025*. https://genai.owasp.org/llm-top-10/
- OWASP Foundation. (n.d.). *OWASP GenAI Security Project*. https://genai.owasp.org/

*Retrieval: (1) ¿qué componentes forman la supply chain de un LLM (LLM03)?; (2) ¿por qué vías ocurre el poisoning (LLM04), incluido el del RAG?; (3) ¿qué es "denial of wallet" (LLM10) y cómo se frena?; (4) ¿por qué el poisoning lento evade los controles?*
