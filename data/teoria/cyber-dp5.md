# Privacidad en ML: differential privacy, fuga por modelos y privacy by design

> Recurso troncal: **NIST Privacy Framework 1.1 (IPD)**. Capstone del cluster: la privacidad cuando el dato deja de ser una tabla y se vuelve un **modelo**. Integra [[cyber-dp1]]–[[cyber-dp4]], conecta con [[cyber-ml-security]] y prepara el mini-proyecto del cluster.

## De qué trata (y qué sabrás hacer al final)

Para un científico de datos, la privacidad no termina en el CSV: continúa en el **modelo** que entrenas con él. Un modelo puede **memorizar y filtrar** a las personas de su entrenamiento, y un *embedding* puede reconstruir el texto original. Esta lección reúne las herramientas para entrenar respetando a las personas: **differential privacy** como garantía formal y **privacy by design** como método.

La intuición: entrenar un modelo es como dejar que un estudiante estudie con los expedientes reales de personas. Si el estudiante **memoriza** casos concretos, podrá "recitar" datos privados aunque le quites los expedientes. Differential privacy es enseñarle de forma que aprenda los **patrones** sin poder recitar a ningún individuo.

Al terminar podrás: (1) explicar la **fuga por modelos** (memorización, membership inference, inversión); (2) entender **differential privacy** y su tradeoff; (3) aplicar **privacy by design** a un pipeline; y (4) ejecutar el mini-proyecto del cluster.

## La fuga ya no está en la tabla, está en el modelo

Recuerda de [[cyber-dp2]] y [[cyber-ml-security]]: un modelo entrenado con datos sensibles es **un activo de privacidad**. Tres formas de fuga:

- **Memorización:** el modelo "recuerda" ejemplos raros y puede emitirlos (un LLM que reproduce datos personales de su entrenamiento).
- **Membership inference:** un atacante determina si **una persona específica** estuvo en el entrenamiento — revelador si el dataset es, p. ej., "pacientes con cierta condición".
- **Model inversion / embeddings:** reconstruir rasgos o el texto/imagen originales a partir del modelo o de sus vectores.

Conclusión: "el dataset es privado" **no** basta; hay que evaluar qué filtra el modelo y sus salidas.

## Differential privacy: una garantía formal

**Differential privacy (DP)** añade ruido calibrado durante el entrenamiento (o al consultar) de modo que la salida **casi no cambia** esté o no una persona concreta en los datos. Su poder: ofrece una **garantía cuantificable** (un parámetro de privacidad, ε) en vez de una promesa vaga; cuanto menor ε, más privacidad y más ruido. Es el estándar moderno cuando el riesgo de fuga es serio.

El costo es el **tradeoff utilidad↔privacidad** ([[cyber-dp2]]): más privacidad reduce algo de exactitud. No necesitas implementar DP-SGD a mano, pero sí saber que existe, qué garantiza y que se **decide** ese tradeoff conscientemente.

## Privacy by design: anticipar, no remendar

**Privacy by design** es construir la privacidad desde el inicio del pipeline, no parchearla al final:

- **Minimiza antes de entrenar:** no metas variables sensibles que no aportan ([[cyber-dp1]]).
- **De-identifica/agrega** donde sea posible ([[cyber-dp2]]).
- **Limita lo que el modelo expone:** salidas de baja resolución, rate limiting ([[cyber-ml-security]]).
- **Rastrea procedencia y consentimiento** por dato, para poder cumplir borrado/derechos ([[cyber-dp3]], [[cyber-dp4]]).
- **Considera DP** cuando el riesgo lo amerite.

Es la aplicación de *fail-safe defaults* ([[cyber-ms2]]) a la privacidad: el camino por defecto debe ser el que menos expone.

## Mini-ejemplo trabajado

Vas a entrenar y exponer un modelo que predice riesgo de deserción escolar con datos de estudiantes. Privacy by design:

- **Minimización:** excluir variables sensibles sin justificación (salud, etnia); usar región amplia en vez de dirección exacta ([[cyber-dp1]], [[cyber-dp2]]).
- **Fuga por modelo:** como el dataset identifica a alumnos, evaluar **membership inference**; limitar memorización (regularización; DP si el riesgo es alto).
- **Exposición:** la API devuelve una categoría de riesgo, no probabilidades finísimas; con auth y rate limiting ([[cyber-web3]], [[cyber-ml-security]]).
- **Derechos:** rastrear qué alumno entró al entrenamiento para poder responder borrado (sabiendo que puede exigir reentrenar — [[cyber-dp3]]).
- **Resultado:** un modelo útil que no recita a ningún alumno ni revela quién estuvo en los datos.

## Señales de reconocimiento

| Señal | Riesgo de privacidad en ML |
|---|---|
| "El dataset es privado, el modelo da igual" | Memorización / inferencia de pertenencia |
| Modelo con datos sensibles y API abierta | Membership inference / inversión |
| Embeddings publicados "porque son números" | Reconstrucción del original |
| Privacidad "se ve al final" | Falta privacy by design |
| Métrica priorizada sobre todo, sin tradeoff | Se ignora utilidad↔privacidad (DP) |

## Errores típicos

- **Creer que entrenar "anonimiza":** el modelo puede memorizar y filtrar individuos.
- **Tratar embeddings como anónimos:** son invertibles ([[cyber-dp2]], [[cyber-mls2]]).
- **Dejar la privacidad para el final:** remendar es caro e incompleto; se diseña desde el inicio.

## Contraejemplo y caso borde

- **Contraejemplo:** un pipeline con minimización, entrenamiento con DP, salidas de baja resolución y procedencia rastreada: útil para predecir y resistente a membership inference e inversión. Privacidad **con** utilidad.
- **Caso borde:** DP protege contra **inferencia sobre individuos**, pero un ε mal elegido (demasiado grande) da garantía nominal sin protección real; y DP no resuelve el sesgo ni el uso indebido del modelo. La técnica es necesaria pero no suficiente: sigue haciendo falta gobernanza ([[cyber-dp4]]).

## Transferencia a ciencia de datos e IA

Este cluster cierra el puente con [[cyber-ml-security]] (la fuga por modelos es ataque de inferencia) y con [[cyber-llm-rag-agents]] (embeddings y memorización de LLMs, LLM02/LLM08). La privacidad por diseño es parte central de la **IA responsable** y de tu oficio: decide qué datos merecen entrar a un modelo y qué expone su despliegue.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el modelo de deserción, lista 4 medidas de privacy by design ordenadas por impacto.
- **Misión externa (lab vivo):** en el **NIST Privacy Framework** (https://www.nist.gov/privacy-framework) busca material sobre *privacy risk* en sistemas con IA/analítica. **Criterio de cierre:** explicar por qué un modelo puede filtrar a personas y qué lo mitiga.
- **Mini-entregable (mini-proyecto del cluster):** una **evaluación de privacidad de un dataset** (biomédico, educativo o financiero) **antes de entrenar**: clasificación de columnas, riesgo de reidentificación, minimización aplicada, decisiones de de-identificación, y medidas de privacidad para el modelo resultante. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** la privacidad continúa en el **modelo**: memorización, **membership inference** e **inversión/embeddings** pueden filtrar a las personas aunque el dataset nunca se publique. **Differential privacy** da una garantía formal (parámetro ε) a costa de un **tradeoff utilidad↔privacidad** consciente, y **privacy by design** construye la protección desde el inicio (minimizar, de-identificar, limitar la exposición del modelo, rastrear procedencia). La técnica es necesaria pero no sustituye la **gobernanza**.

---

**Referencias**

- National Institute of Standards and Technology. (2025). *NIST Privacy Framework 1.1: Initial public draft* (NIST CSWP 40 ipd). https://doi.org/10.6028/NIST.CSWP.40.ipd
- Dwork, C., & Roth, A. (2014). The algorithmic foundations of differential privacy. *Foundations and Trends in Theoretical Computer Science, 9*(3–4), 211–407.

*Retrieval: (1) ¿de qué tres formas filtra privacidad un modelo?; (2) ¿qué garantiza differential privacy y a costa de qué?; (3) ¿qué es privacy by design?; (4) ¿por qué "el dataset es privado" no basta?*
