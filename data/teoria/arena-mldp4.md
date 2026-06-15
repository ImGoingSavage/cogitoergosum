# Patrones de reproducibilidad e IA responsable

## Reproducibilidad

- **Transform:** los **inputs ≠ features** (las features se derivan de los inputs). Captura explícitamente la transformación input→feature y guárdala en el **grafo del modelo** (cláusula `TRANSFORM` de BigQuery ML, o un feature store) para aplicarla **idéntica** en train y serving → mata el **training-serving skew**. En inferencia mandas solo inputs crudos.
- **Repeatable Splitting:** no uses `random` sin semilla (no repetible + **fuga** si las filas están correlacionadas). Divide por el **módulo de un hash determinista** (FarmHash) de una columna que: (1) capture la correlación, (2) **no sea input**, (3) tenga suficientes valores únicos (3-5× el denominador), (4) tenga la etiqueta bien distribuida. Verifica con **Kolmogorov-Smirnov**.
- **Bridged Schema:** cuando el esquema mejora (card → gift/debit/credit), adapta los datos **viejos** al esquema nuevo para usar todo lo nuevo aumentado con lo viejo. **Método estático** (preferido): codifica los viejos con las **probabilidades a priori** de las clases nuevas (p.ej. `[0, 0.1, 0.3, 0.6]`); los nuevos usan one-hot real.
- **Windowed Inference:** modelos que necesitan una **secuencia** o **agregados temporales**. Externaliza el estado a un **pipeline de stream** con ventana deslizante (estado actualizado por cada llegada; parámetros calculados al cerrar la ventana) → evita skew en features de agregado temporal.
- **Workflow Pipeline:** **conteneriza** cada paso (preproceso, train, deploy) como servicio aislado y **orquéstalos** (TFX, Kubeflow, Airflow). Monolito→microservicios: reproducible, colaborable, ejecutable de extremo a extremo con una llamada.
- **Model Versioning:** despliega cada versión como un **endpoint REST distinto** → compatibilidad hacia atrás, monitoreo por versión, **A/B testing**, desacople del frontend.
- **Continued Model Evaluation:** monitorea el desempeño en producción contra la verdad de campo para detectar **concept drift** (cambia la relación inputs↔target) y **data drift** (cambian los datos de entrada).

## IA responsable

- **Heuristic Benchmark:** compara el modelo contra una **heurística simple** (constante, media/mediana, regla de oro, lookup de 1-2 features) para explicar su desempeño al negocio ("¿un MAE de 1.200 s es bueno?"). Si ya hay práctica operativa, compárate con **ella**.
- **Explainable Predictions:** accuracy no dice **por qué**; usa **atribuciones de features** para revelar qué influyó (un modelo de retinopatía podría fijarse en las anotaciones del médico, no en la enfermedad). Árboles son interpretables por diseño; las redes profundas no.
- **Fairness Lens:** los datos los crean humanos → sesgo. Distingue sesgo **natural** (estadístico) del **problemático** (afecta distinto a grupos): distribución, representación/reporting, etiquetado. **Quitar la feature sensible NO basta** (queda en proxies como código postal/ingreso). Evalúa por **slices**, no solo accuracy global.

---

## Mini-ejemplo trabajado: por qué quitar la feature sensible no arregla el sesgo

Quieres un modelo de crédito justo respecto a la **raza**, así que la eliminas de las features. ¿Resuelto? No: el **código postal**, el **ingreso** y el **historial** correlacionan con la raza y actúan como **proxies**. El modelo reconstruye la información sensible por la puerta de atrás y sigue discriminando — ahora de forma *oculta*.

Estructuralmente es **confundimiento por proxy**: borrar la variable no cierra el camino que va de ella a la decisión a través de sus sustitutos (la misma lógica de [[arena-h4]]). La cura no es ceguera, es **medición**: evalúa el modelo por **slices** (tasa de aprobación, error por grupo) y corrige si un grupo recibe trato sistemáticamente distinto.

**Predicción antes de seguir:** divides train/test con `random` sin semilla y tus filas son transacciones del mismo usuario. ¿Qué pasa? **Fuga**: el mismo usuario cae en train y test → métricas infladas. La cura es **Repeatable Splitting**: módulo de un **hash determinista** de una columna que capture la correlación (p. ej. `user_id`), que **no sea input** del modelo y tenga suficientes valores únicos.

## Prototipo, contraejemplo y caso borde

- **Prototipo (Transform):** guardas la transformación input→feature en el grafo del modelo → train y serving aplican lo mismo, mata el skew.
- **Contraejemplo (split ingenuo):** `random.shuffle` con filas correlacionadas → fuga y resultados no reproducibles.
- **Caso borde (Bridged Schema):** el esquema mejora (card → débito/crédito) y tienes poca data nueva → codifica la vieja con las **probabilidades a priori** de las clases nuevas en vez de tirarla.

## Errores típicos

- **Conceptual:** creer que la equidad se logra **quitando** la feature sensible (sobrevive en proxies).
- **Técnico:** splits no deterministas o por una columna que *es* input → fuga y no reproducibilidad.
- **De evaluación:** juzgar por **accuracy global** en vez de por **slices** (equidad, drift, subgrupos).

## Transferencia isomorfa

- **Transform ↔ paridad train/serving:** fijar la transformación input→feature en el grafo es la cura del training-serving skew de las Reglas de ML (conecta con [[arena-rom3]]).
- **Repeatable Splitting ↔ hashing determinista:** dividir por `hash(columna) % n` es el mismo FarmHash de los Hashed Features y de las tablas hash (conecta con [[arena-mldp1]] y [[arena-cc1]]).
- **Fairness por proxy ↔ confundimiento:** que una variable omitida sobreviva en sus sustitutos es exactamente el confundimiento por proxy del DAG causal (conecta con [[arena-h4]]).

Moraleja de la arista: *la reproducibilidad se compra con transformaciones fijas y splits por hash determinista; la equidad no se logra cegando el modelo (los proxies delatan), sino midiendo por slices.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Features derivadas de inputs, voy a producción | Transform (guarda la transformación en el grafo) |
| Filas correlacionadas, comparar modelos | Repeatable Splitting (hash de columna no-input) |
| El esquema de datos mejoró, poca data nueva | Bridged Schema (método estático) |
| Necesito agregados sobre ventana temporal | Windowed Inference (stream con estado) |
| Varias personas, pasos complejos | Workflow Pipeline (contenerizar + orquestar) |
| Actualizar modelo sin romper usuarios | Model Versioning (endpoints REST) |
| "¿Un MAE de X es bueno?" | Heuristic Benchmark |
| El usuario/regulador desconfía | Explainable Predictions (atribuciones) |
| Decisiones que afectan a personas | Fairness Lens (slices, ojo a proxies) |

---

> **Síntesis:** Para **reproducibilidad**: guarda la transformación input→feature (**Transform**), divide por **hash de una columna correlacionada no-input** (**Repeatable Splitting**), **puentea esquemas** viejos al nuevo, externaliza ventanas temporales (**Windowed Inference**), **conteneriza** el pipeline y **versiona** modelos como endpoints, y **evalúa continuamente** el drift. Para **IA responsable**: contextualiza con un **benchmark heurístico**, **explica** las predicciones (atribuciones) y mira con **lente de equidad** —quitar la feature sensible no basta, evalúa por slices.

---

*Retrieval: (1) ¿cómo evita Transform el skew?; (2) ¿qué dos problemas resuelve Repeatable Splitting y qué columna usar?; (3) ¿qué es el método estático de Bridged Schema?; (4) ¿por qué quitar la feature sensible no arregla el sesgo?*
