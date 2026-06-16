# Seguridad de ML I: por qué la IA cambia la superficie de ataque

> Recurso troncal: **MITRE SAFE-AI** (marco para asegurar sistemas habilitados por IA), complementado con **MITRE ATLAS**. Aplica todo lo anterior a tu propio terreno: el modelo. Sigue en [[cyber-mls2]] (ataques a inferencia y controles).

## De qué trata (y qué sabrás hacer al final)

Un sistema de ML hereda **todas** las vulnerabilidades de software (las de los clusters previos) y **añade** otras nuevas, porque su comportamiento no está solo en el código: está en los **datos** y en el **modelo aprendido**. Eso abre superficies de ataque que un pentester clásico no contempla: puedes atacar un modelo **sin tocar una sola línea de código**, solo manipulando lo que aprende o lo que ve.

La intuición: un programa tradicional es una receta fija; si quieres cambiar su conducta, editas la receta. Un modelo de ML es un aprendiz que imita lo que le mostraste. Para corromperlo no necesitas reescribir su mente: basta con **mentirle durante el aprendizaje** (envenenar los datos) o **mostrarle ilusiones en el examen** (entradas adversarias). La superficie de ataque se mudó de la lógica a los datos.

Al terminar podrás: (1) explicar por qué la IA **amplía** la superficie de ataque; (2) distinguir ataques al **entrenamiento** vs a la **inferencia**; (3) entender **data poisoning, backdoors y data leakage**; y (4) ubicar SAFE-AI/ATLAS/NIST AI RMF como marcos de referencia.

## Dos momentos, dos superficies

El ciclo de vida de un modelo tiene dos grandes ventanas de ataque:

| Momento | Qué controla el atacante | Ataques representativos |
|---|---|---|
| **Entrenamiento** | Los datos de los que el modelo aprende | Data poisoning, backdoors |
| **Inferencia** | Las entradas que el modelo ve en producción | Evasion (adversarial), extraction, inversion, membership inference |

Más una superficie transversal: la **supply chain del modelo** (datasets y modelos preentrenados de terceros) y la **provenance** (¿de dónde vino, qué garantías tiene?). Esta lección cubre el entrenamiento y el leakage; [[cyber-mls2]] cubre la inferencia y los controles.

## Data poisoning: mentir durante el aprendizaje

Si el atacante puede inyectar o alterar datos de entrenamiento, moldea lo que el modelo aprende. Dos formas:

- **Envenenamiento de disponibilidad/integridad:** corromper etiquetas o muestras para degradar el modelo (baja exactitud general). Recuerda: rompe la **I** de la tríada CIA aplicada a los datos ([[cyber-ms1]]).
- **Backdoor (puerta trasera):** insertar un **patrón disparador** de modo que el modelo se comporte normal **salvo** cuando ve el disparador, momento en que hace lo que el atacante quiere (p. ej., clasifica como "benigno" todo lo que lleve cierta marca). Es sigiloso: en validación normal, el modelo parece perfecto.

El riesgo crece cuando entrenas con **datos no curados** (scraping web, contribuciones abiertas, feedback de usuarios): cada fuente no confiable es un canal de envenenamiento.

## Data leakage: el modelo recuerda demasiado

Dos sentidos, ambos importantes:

- **Leakage metodológico:** información del futuro o del target se cuela en las features (el clásico error de DS que infla métricas). Es un problema de validez **y** de seguridad cuando expone datos que no debían influir.
- **Memorización:** un modelo puede memorizar ejemplos de entrenamiento y filtrarlos después (base de la *membership inference* y la *model inversion* de [[cyber-mls2]]). Un modelo entrenado con datos sensibles **es** un activo de privacidad ([[cyber-data-privacy]]).

## Mini-ejemplo trabajado

Entrenas un detector de fraude que se reentrena cada noche con transacciones **etiquetadas por reportes de usuarios**. Un atacante crea muchas cuentas y reporta sistemáticamente sus propias transacciones fraudulentas como "legítimas". Con el tiempo, el modelo aprende que el patrón del atacante es benigno: un **data poisoning** a través del canal de etiquetado, sin tocar tu código. Peor, podría inducir un **backdoor**: cierto monto+hora exactos siempre pasan. Defensa (anticipo de [[cyber-mls2]]): validar y limitar la influencia de fuentes no confiables, detectar deriva en las etiquetas, y monitorear el comportamiento del modelo, no solo su exactitud agregada.

## Señales de reconocimiento

| Señal | Riesgo de ML |
|---|---|
| Entrenamiento con datos scrapeados/no curados | Data poisoning |
| Reentrenamiento con feedback de usuarios sin control | Envenenamiento por el canal de etiquetas |
| Métrica de validación "demasiado buena" | Leakage metodológico (o backdoor invisible) |
| Modelo entrenado con datos sensibles y expuesto | Memorización → fuga de privacidad |
| Modelo preentrenado de origen desconocido | Supply chain / backdoor heredado |

## Errores típicos

- **Tratar el modelo solo como código:** ignorar que datos y pesos son superficies de ataque propias.
- **Confiar en la exactitud agregada:** un backdoor no baja la exactitud general; pasa todas las pruebas normales.
- **Asumir que los datos de entrenamiento son confiables:** sobre todo cuando vienen de la web o de usuarios.

## Contraejemplo y caso borde

- **Contraejemplo:** un pipeline que **valida y rastrea la procedencia** de cada fuente de datos, limita el peso de contribuciones no confiables y testea con datos *hold-out* curados: reduce drásticamente el poisoning sin sacrificar utilidad.
- **Caso borde:** un modelo entrenado solo con datos **propios y limpios** sigue teniendo superficie de **inferencia** (evasion, extraction): cerrar el entrenamiento no cierra el modelo desplegado.

## Transferencia a ciencia de datos e IA

El poisoning es la versión-ML del envenenamiento de supply chain de [[cyber-dev2]]; la memorización es el puente con la reidentificación de [[cyber-data-privacy]]; y la detección de etiquetas anómalas es detection engineering ([[cyber-blue2]]) aplicado a tu propio pipeline. En LLMs, el poisoning de datos reaparece como LLM04 ([[cyber-llm-rag-agents]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el detector de fraude, lista 3 controles que reducirían el poisoning por el canal de reportes.
- **Misión externa (lab vivo):** explora **MITRE ATLAS** (https://atlas.mitre.org), el "ATT&CK de la IA"; elige una táctica y lee una técnica de ataque a ML. **Criterio de cierre:** explicar si ataca al entrenamiento o a la inferencia.
- **Mini-entregable:** un diagrama del ciclo de vida de un modelo que conozcas, marcando dónde podría ocurrir poisoning y dónde leakage.

---

> **Síntesis:** un sistema de ML hereda las vulnerabilidades de software y **añade** las suyas, porque su conducta vive en **datos** y **pesos**, no solo en el código. Distingue ataques al **entrenamiento** (data poisoning, **backdoors** sigilosos) de los de **inferencia**, más la **supply chain** del modelo. La **memorización** convierte a un modelo entrenado con datos sensibles en un activo de privacidad. Marcos guía: **SAFE-AI, ATLAS, NIST AI RMF**.

---

**Referencias**

- Kressel, J., Perrella, R., Reed, E., Naik, N., Sidhu, J., Hu, Q., Booker, L., Cintron, J., & Huffner, L. (2025). *SAFE-AI: A framework for securing AI-enabled systems*. The MITRE Corporation.
- MITRE. (n.d.). *MITRE ATLAS*. https://atlas.mitre.org

*Retrieval: (1) ¿por qué la IA amplía la superficie de ataque?; (2) entrenamiento vs inferencia; (3) ¿qué hace un backdoor y por qué es sigiloso?; (4) ¿por qué un modelo entrenado con datos sensibles es un activo de privacidad?*
