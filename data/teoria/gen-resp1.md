# IA responsable: sesgo, equidad, transparencia y rendición de cuentas

> Recurso troncal: **MIT-AI.md (Responsible AI + frameworks)**. La capa que decide si un sistema de IA debe existir y bajo qué condiciones. Conecta con la gobernanza de seguridad ([[cyber-mit3]]) y la privacidad ([[cyber-dp5]]). Prepara [[gen-resp2]] (los frameworks).

## De qué trata (y qué sabrás hacer al final)

Que un modelo sea **preciso** no lo hace **aceptable**. Un sistema de IA puede tener 95% de accuracy y aun así discriminar, ser inexplicable, violar la privacidad o no rendir cuentas a nadie. La **IA responsable** es el conjunto de propiedades —equidad, transparencia, rendición de cuentas, privacidad, robustez— que decide si un sistema **debe** desplegarse y cómo. Para un científico de datos, esto no es "ética blanda": es ingeniería con consecuencias humanas y legales.

La intuición: la precisión es como la **potencia de un coche**; la IA responsable son los **frenos, el cinturón, las luces y las reglas de tránsito**. Un coche potentísimo sin frenos no es "mejor", es peligroso. Optimizar solo la métrica de desempeño y olvidar la responsabilidad es construir un coche de carreras para circular entre peatones.

Al terminar podrás: (1) explicar por qué **precisión ≠ aceptabilidad**; (2) distinguir **sesgo** y **equidad** (y que la equidad tiene definiciones en conflicto); (3) razonar **transparencia e interpretabilidad**; y (4) ubicar la **rendición de cuentas** y el daño a personas.

## Precisión no es aceptabilidad: las dimensiones que faltan

Más allá del desempeño, un sistema responsable debe considerar:
- **Equidad (fairness):** ¿trata de forma justa a distintos grupos, o hereda/amplifica sesgos?
- **Transparencia/interpretabilidad:** ¿se puede entender y explicar por qué decidió algo?
- **Privacidad:** ¿protege a las personas de los datos? ([[cyber-dp5]]).
- **Robustez y seguridad:** ¿resiste fallos y ataques? ([[cyber-ml-security]]).
- **Rendición de cuentas:** ¿hay un responsable y un recurso si daña?

Un modelo puede ser excelente en accuracy y fallar en cualquiera de estas — y entonces no debe desplegarse tal cual.

## Sesgo y equidad: de dónde viene y por qué es difícil

El **sesgo** entra por los **datos** (reflejan desigualdades históricas), por las **etiquetas** (decisiones humanas sesgadas), por las **features** (proxies de atributos protegidos: el código postal puede ser proxy de raza) y por el **objetivo** (optimizar lo equivocado). Casos reales: sistemas de scoring crediticio o de reincidencia ([análisis de COMPAS, ProPublica, 2016](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing)) que discriminaban por raza; un modelo de contratación que penalizaba CVs de mujeres.

Lo contraintuitivo: **"equidad" tiene varias definiciones matemáticas que no pueden cumplirse a la vez.** Paridad demográfica (mismas tasas de aprobación por grupo), igualdad de oportunidades (misma tasa de verdaderos positivos), calibración… son **mutuamente incompatibles** salvo en casos triviales ([Kleinberg et al., 2016](https://arxiv.org/abs/1609.05807)). No existe "el modelo justo" universal; hay que **elegir** qué noción de equidad importa para el contexto, y justificarlo. Eso es una decisión sociotécnica, no solo técnica.

## Transparencia e interpretabilidad

- **Transparencia:** que las personas afectadas sepan que hay un sistema de IA, qué decide y con qué datos (eco de [[cyber-dp3]]).
- **Interpretabilidad:** poder explicar **por qué** el modelo decidió algo. Importa para depurar, para confiar, y a veces es **legal** (derecho a explicación). Herramientas: modelos intrínsecamente interpretables, o explicaciones post-hoc como [SHAP](https://arxiv.org/abs/1705.07874) y [LIME](https://arxiv.org/abs/1602.04938) — con la advertencia de que una explicación post-hoc es una **aproximación**, no necesariamente la razón real del modelo ([Rudin, 2019](https://arxiv.org/abs/1811.10154) argumenta por usar modelos interpretables en decisiones de alto riesgo). En LLMs, la interpretabilidad es aún más difícil (cajas negras enormes).

## Mini-ejemplo trabajado: el modelo "preciso" que discrimina

Un banco entrena un scoring crediticio con 92% de accuracy. Al auditarlo: aprueba al 70% de un grupo y al 45% de otro, replicando un sesgo histórico de los datos, y usa el código postal (proxy de zona y, de facto, de etnia). ¿Es aceptable? **No**, pese al 92%:
- **Sesgo:** hereda y amplifica desigualdad histórica vía un proxy.
- **Equidad:** ¿qué definición eliges? Igualar tasas de aprobación (paridad) puede chocar con igualar la precisión por grupo — hay que decidir y justificar.
- **Transparencia/rendición de cuentas:** ¿se le explica al rechazado por qué? ¿quién responde?

Predicción antes de seguir: para "arreglar" el sesgo, el equipo **quita la variable de etnia** del modelo. ¿Basta? → No: el modelo la reconstruye vía **proxies** (código postal, nombre, etc.). Quitar el atributo protegido **no** elimina el sesgo (es el "fairness through unawareness", que falla). Hay que medir y mitigar el sesgo activamente, no esconder la variable — eco de la reidentificación de [[cyber-dp2]] (los proxies delatan).

## Señales de reconocimiento

| Señal | Bandera de IA responsable |
|---|---|
| "Tiene 95% accuracy, está listo" | Precisión ≠ aceptabilidad; falta auditar equidad/privacidad |
| "Quitamos la variable sensible, ya es justo" | Proxies reconstruyen el sesgo (unawareness falla) |
| "No sabemos por qué rechazó a esta persona" | Falta interpretabilidad (y quizá es ilegal) |
| "Si el modelo daña, ¿quién responde?" | Falta rendición de cuentas |
| "Es justo" (sin decir según qué definición) | La equidad tiene definiciones en conflicto |

## Errores típicos

- **Optimizar solo el desempeño:** ignorar equidad, transparencia y daño a personas.
- **Fairness through unawareness:** creer que quitar el atributo protegido elimina el sesgo (los proxies no).
- **Asumir que existe 'el modelo justo':** las definiciones de equidad son incompatibles; hay que elegir.
- **Confiar ciegamente en explicaciones post-hoc:** SHAP/LIME aproximan, no son la verdad del modelo.

## Contraejemplo y caso borde

- **Contraejemplo (responsable y útil):** un sistema con auditoría de sesgo por grupo, una definición de equidad elegida y justificada, explicaciones para los afectados y un responsable claro: útil **y** defendible. La responsabilidad no impide el valor; lo hace sostenible.
- **Caso borde (equidad que daña a quien busca proteger):** imponer paridad demográfica a la fuerza puede, en algún contexto, empeorar la precisión para el grupo protegido (aprobar casos que fallarán, perjudicando a esas personas). No hay almuerzo gratis: cada elección de equidad tiene consecuencias que deben evaluarse, no asumirse.

## Transferencia isomorfa

- **Precisión ≠ aceptabilidad ↔ riesgo residual y tradeoffs:** una métrica alta no captura todas las dimensiones, como ROUGE no capturaba calidad ([[gen-eval1]]) ni accuracy captura seguridad. Optimizar una sola dimensión es el error transversal del bloque.
- **Proxies del sesgo ↔ reidentificación:** los atributos correlacionados reconstruyen lo que escondes, igual que los cuasi-identificadores reidentifican ([[cyber-dp2]]).
- **Equidad como decisión ↔ comunicar tradeoffs:** elegir y justificar una noción de equidad es comunicación de riesgo sociotécnica ([[cyber-ms5]]).

Moraleja de la arista: *un modelo preciso no es aceptable por sí solo; la IA responsable exige elegir y justificar equidad, dar transparencia y rendición de cuentas, y recordar que esconder la variable sensible no borra el sesgo.*

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el scoring crediticio del ejemplo, propón cómo auditarías el sesgo (qué medirías por grupo) y qué definición de equidad elegirías y por qué.
- **Misión externa (lab vivo):** lee el caso [Machine Bias (ProPublica/COMPAS)](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing) y hojea [SHAP](https://github.com/shap/shap). **Criterio de cierre:** explicar por qué quitar la variable protegida no elimina el sesgo.
- **Mini-entregable:** una "ficha de IA responsable" para un modelo: dimensiones (equidad, transparencia, privacidad, rendición de cuentas), qué auditarías en cada una, y la definición de equidad elegida con su justificación.

---

> **Síntesis:** **precisión ≠ aceptabilidad**: un modelo de 95% puede discriminar, ser inexplicable o no rendir cuentas. La **IA responsable** exige equidad, transparencia/interpretabilidad, privacidad, robustez y rendición de cuentas. El **sesgo** entra por datos, etiquetas, features (proxies) y objetivo; **quitar el atributo protegido no lo elimina** (los proxies lo reconstruyen). Y "**equidad**" tiene definiciones matemáticas **incompatibles** entre sí: hay que **elegir y justificar** cuál importa — una decisión sociotécnica, no solo técnica. Las explicaciones post-hoc (SHAP/LIME) **aproximan**, no son la verdad del modelo.

---

**Referencias**

- Angwin, J., et al. (2016). Machine bias (COMPAS). *ProPublica*. [propublica.org](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing)
- Kleinberg, J., Mullainathan, S., & Raghavan, M. (2016). Inherent trade-offs in the fair determination of risk scores. [arXiv:1609.05807](https://arxiv.org/abs/1609.05807)
- Lundberg, S., & Lee, S.-I. (2017). A unified approach to interpreting model predictions (SHAP). *NeurIPS*. [arXiv:1705.07874](https://arxiv.org/abs/1705.07874)
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?" (LIME). *KDD*. [arXiv:1602.04938](https://arxiv.org/abs/1602.04938)
- Rudin, C. (2019). Stop explaining black box models for high-stakes decisions. *Nature Machine Intelligence*. [arXiv:1811.10154](https://arxiv.org/abs/1811.10154)

*Retrieval: (1) ¿por qué precisión ≠ aceptabilidad?; (2) ¿por qué quitar la variable protegida no elimina el sesgo?; (3) ¿por qué no existe "el modelo justo"?; (4) ¿qué límite tienen SHAP/LIME?*
