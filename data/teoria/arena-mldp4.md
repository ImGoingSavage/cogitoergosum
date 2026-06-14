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
