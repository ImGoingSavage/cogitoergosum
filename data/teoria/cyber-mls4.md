# Robo y fuga del modelo: extraction, inversion y membership inference

> Recurso troncal: **MITRE SAFE-AI / MITRE ATLAS**. Profundiza los ataques que **sacan** algo del modelo (no que lo engañan), esbozados en [[cyber-mls2]]. Sigue a [[cyber-mls3]] (evasión) y prepara [[cyber-mls5]] (supply chain y gobernanza).

## De qué trata (y qué sabrás hacer al final)

Un modelo desplegado no solo puede ser engañado (evasión, [[cyber-mls3]]); también puede ser **robado** o hecho **filtrar** lo que aprendió, solo consultándolo. Para un científico de datos esto es directo: cada API de modelo que expones, cada conjunto de embeddings que compartes, es una posible fuga de propiedad intelectual y de privacidad. Entenderlo decide qué expones y cómo.

La intuición: tu modelo es un experto tras una ventanilla. Un competidor puede hacerle miles de preguntas y, con las respuestas, **entrenar a su propio experto** que imita al tuyo (extraction). Un curioso puede formular preguntas astutas para que el experto **revele casos** que estudió (inversion/membership). No fuerzan la ventanilla; abusan del servicio que ofreces.

Al terminar podrás: (1) explicar **model extraction** y su impacto; (2) distinguir **model inversion** de **membership inference**; (3) razonar el riesgo de compartir **modelos y embeddings**; y (4) elegir controles proporcionales.

## Model extraction: clonar consultando

Con suficientes pares entrada→salida, un atacante puede entrenar un modelo sustituto que **imita** al tuyo, robando el resultado de tu inversión en datos y cómputo. Peor: ese sustituto sirve para montar ataques de evasión white-box ([[cyber-mls3]]) que luego **transfieren** a tu modelo. Cuanta más información dé tu salida (probabilidades exactas vs solo la etiqueta), más fácil la extracción. Por eso devolver salidas de **baja resolución** y aplicar **rate limiting** ([[cyber-web3]]) son las defensas base.

## Inversion vs membership inference

Dos fugas distintas de los **datos de entrenamiento**:

- **Model inversion:** reconstruir rasgos representativos de una clase o de los datos (p. ej., aproximar el rostro "promedio" asociado a una etiqueta). Filtra **cómo eran** los datos.
- **Membership inference:** determinar si **un individuo concreto** estuvo en el entrenamiento, explotando que el modelo suele estar "más seguro" con lo que vio. Filtra **quién** estuvo — devastador si el dataset es, p. ej., "pacientes con cierta condición".

Ambas nacen de la **memorización** ([[cyber-mls1]]): el modelo recuerda más de lo necesario. La defensa de fondo es reducir esa memorización (regularización, **differential privacy**, [[cyber-dp5]]).

## Compartir modelos y embeddings: el riesgo oculto

- **Compartir pesos** habilita extraction/inversion **offline** (sin rate limit que valga) y, si el modelo traía un backdoor ([[cyber-mls1]]), lo propaga.
- **Compartir embeddings** parece inocuo —"son vectores"— pero a menudo permiten **reconstruir** el original o inferir atributos sensibles ([[cyber-dp2]]). Un embedding no es anónimo por ser un número.

Regla de [[cyber-mls2]]: antes de exponer un modelo, una API o un store de embeddings, pregunta **qué podría reconstruir o inferir** un consumidor malicioso, no solo qué quieres que haga.

## Mini-ejemplo trabajado

Expones una API que da, por imagen médica, la probabilidad detallada de cada diagnóstico, sin límites. Análisis:

- **Extraction:** un competidor consulta masivamente y clona tu modelo (las probabilidades detalladas lo facilitan).
- **Membership inference:** como entrenaste con pacientes reales, un atacante infiere si una persona específica estuvo en los datos (fuga de privacidad grave).
- **Inversion:** podría aproximar rasgos de los casos de entrenamiento.
- **Controles proporcionales:** devolver categoría/top-1 en vez de probabilidades finas; autenticación + rate limiting; entrenamiento con differential privacy; monitoreo de patrones de consulta anómalos ([[cyber-blue2]]); no publicar pesos ni embeddings crudos.
- **Riesgo residual:** un adversario muy decidido aún logra algo → se acepta, monitorea y documenta.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| API de modelo sin auth ni rate limit | Extraction / inversion masivos |
| Devuelve probabilidades de alta precisión | Facilita extraction e inversion |
| "Publicamos los embeddings, son anónimos" | Reconstrucción / inferencia de atributos |
| Modelo con datos sensibles y acceso abierto | Membership inference |
| Pesos compartidos públicamente | Ataques offline + backdoors heredados |

## Errores típicos

- **"El dataset es privado, el modelo da igual":** el modelo filtra a las personas que vio.
- **Tratar embeddings como anónimos:** son invertibles.
- **Exponer probabilidades finísimas por "transparencia":** entregan justo lo que facilita extraction/inversion.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** con muchos pares entrada→salida un atacante entrena un sustituto que imita tu modelo; como nace de la memorización, la defensa de fondo es reducirla (DP).
- **Contraejemplo:** API con auth, rate limiting, salida de baja resolución, entrenamiento con DP y monitoreo: extraer o invertir cuesta tanto que deja de ser rentable. Riesgo gestionado.
- **Caso borde:** un modelo **on-device** ([[cyber-mls2]]) entrega los pesos al usuario → extraction/inversion son inevitables offline; debes asumirlo y minimizar lo que el modelo memoriza, no confiar en límites de consulta que no existen.

## Transferencia a ciencia de datos e IA

Estos ataques deciden tu estrategia de despliegue: qué exponer, con qué granularidad, qué nunca publicar. Membership inference e inversion son el puente con la privacidad ([[cyber-dp5]]); extraction es robo de IP y habilitador de evasión ([[cyber-mls3]]); y los embeddings reaparecen como LLM08 en [[cyber-llm-rag-agents]]. La pregunta "¿qué puede reconstruir el consumidor?" gobierna todo.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para la API médica del ejemplo, ordena 4 controles por impacto/costo y justifica el riesgo residual.
- **Misión externa (lab vivo):** en **MITRE ATLAS** (https://atlas.mitre.org) localiza una técnica de exfiltración/robo de modelo o de inferencia de pertenencia. **Criterio de cierre:** explicar qué control la mitiga.
- **Mini-entregable:** una tabla "qué expongo (pesos / probabilidades / etiqueta / embeddings) → qué se puede sacar → control" para un modelo.

---

> **Síntesis:** un modelo puede ser **robado o hecho filtrar** solo consultándolo: **extraction** (clonarlo, y habilitar evasión transferible), **inversion** (reconstruir cómo eran los datos) y **membership inference** (saber **quién** estuvo en el entrenamiento). Nacen de la **memorización**, así que la defensa de fondo es reducirla (DP). Controles proporcionales: salida de baja resolución, auth + rate limiting, no publicar pesos ni embeddings crudos. La pregunta clave al exponer algo: **¿qué puede reconstruir o inferir un consumidor malicioso?**

---

**Referencias**

- Kressel, J., Perrella, R., Reed, E., Naik, N., Sidhu, J., Hu, Q., Booker, L., Cintron, J., & Huffner, L. (2025). *SAFE-AI: A framework for securing AI-enabled systems*. The MITRE Corporation.
- MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org
- Shokri, R., Stronati, M., Song, C., & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *IEEE S&P*.

*Retrieval: (1) ¿cómo se roba (extrae) un modelo y qué lo facilita?; (2) inversion vs membership inference; (3) ¿por qué compartir embeddings filtra?; (4) ¿cuál es la defensa de fondo contra la fuga y por qué?*
