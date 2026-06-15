# MLOps: llevar el modelo a producción y mantenerlo vivo

## Qué es MLOps y por qué importa

**MLOps** mezcla DevOps con ciencia de datos: el puente entre el modelo que crea el DS y las operaciones de IT. Cubre todo el ciclo de vida — ingesta de datos, desarrollo, prueba, **despliegue**, monitoreo y mejora continua. Un modelo brillante en un notebook no vale nada si no se **operacionaliza** y mantiene en producción. Beneficios: velocidad de iteración, colaboración, **gobernanza** (versionado, cumplimiento), escalabilidad y reducción de costos por automatización.

## El pipeline de modelo

El gran activo de MLOps es un **pipeline reproducible y automatizado** que va de prototipo a solución productiva: construir → entrenar → desplegar, siempre con los **mismos pasos**. Tres virtudes:
- **Automatización** — del prototipo a producción rápido.
- **Consistencia** — los mismos pasos cada vez, menos errores.
- **Reproducibilidad** — cada paso queda registrado (clave en farma/salud/finanzas reguladas).

## Ingesta de datos: ETL/ELT, batch y streaming

La ingesta automatiza recolectar datos confiables, consistentes y sin sesgo. Ocurre vía **ETL** (extract-transform-load) o **ELT**, en procesos **batch** (lotes) o **streaming** (continuo). Tecnologías de big data: Spark/PySpark (in-memory, distribuido), Hadoop/Hive, Apache Beam, Apache Storm (streaming), Dask (batch+stream en Python, datasets mayores que la RAM).

## Contenedores: Docker y Kubernetes

Un **contenedor** empaqueta el modelo **junto con sus dependencias y entorno** → se comporta igual en testing, staging y producción ("funciona en mi máquina" desaparece).

- **Docker:** un `Dockerfile` describe el entorno (imagen base, `pip install -r requirements.txt`, `EXPOSE`, `CMD`). `docker build -t mi-modelo .` construye la imagen; `docker run -p 4000:80 mi-modelo` la corre y mapea puertos. Detrás, un `app.py` (a menudo con **Flask**) recibe entradas y devuelve predicciones.
- **Kubernetes:** orquesta **muchos** contenedores en un clúster — para escalabilidad y alta disponibilidad.

## Validar y monitorear el modelo desplegado

**Validar** (tras desplegar): envía datos **no vistos** al endpoint, recoge predicciones, puntúalas. Confirma que (a) el despliegue funciona y (b) el rendimiento es el esperado — sin sorpresas.

**Monitorear** (continuo): el trabajo no termina al desplegar.
- **Logging:** bitácora de cada interacción/decisión del modelo — tu herramienta de depuración.
- **Métricas en tiempo real:** accuracy, tiempos de respuesta, uso de recursos; alertas ante caídas súbitas.
- **Data drift:** las propiedades estadísticas de la entrada **cambian con el tiempo** (cambia el comportamiento del usuario, el mundo). Se detecta fijando un **baseline** con los datos de entrenamiento y comparando la entrada nueva contra él, con tests como **Population Stability Index** o **divergencia de Jensen-Shannon**. Drift detectado → **reentrenar** (fácil porque el pipeline ya está automatizado).

## Gobernanza

Una vez en producción: rastrear versiones de modelo y datos, documentar diseño y rendimiento, asegurar cumplimiento regulatorio. Parte del monitoreo de largo plazo, especialmente en salud y finanzas.

---

## Mini-ejemplo trabajado: detectar data drift con un baseline

Tu modelo de fraude se entrenó cuando la edad media de los usuarios era 35 (σ=10). Tres meses después, el tráfico viene de una campaña que atrajo jóvenes: edad media 24. El modelo no cambió, pero la **entrada sí**. Fijas un *baseline* (la distribución de entrenamiento) y comparas la entrada nueva con un índice como el **PSI** (Population Stability Index): PSI < 0.1 estable, 0.1–0.25 cambio moderado, > 0.25 drift severo. Aquí saltaría la alarma.

Lo clave: el data drift se detecta **sin labels** (solo comparas distribuciones de features), así que avisa *antes* de que lleguen las etiquetas reales de fraude (que tardan semanas).

**Predicción antes de seguir:** si el PSI de las features está estable pero el modelo empeora, ¿qué pasó? Respuesta: probablemente **concept drift** — cambió P(Y|X), la *relación* features→fraude, no las features mismas (p. ej. nuevos esquemas de fraude). Eso NO lo ves comparando distribuciones de entrada; necesitas performance con labels o proxies. Data drift (cambia P(X)) y concept drift (cambia P(Y|X)) son alarmas distintas y se monitorean por separado.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** el modelo era preciso y empeora → compara entrada vs baseline (PSI/KS) para data drift; performance vs labels para concept drift.
- **Contraejemplo ("funciona en mi máquina"):** sin contenedor, el modelo depende del entorno local; en prod faltan versiones de librerías. Docker empaca dependencias para que el comportamiento sea idéntico.
- **Caso borde (data drift sin concept drift):** llega tráfico de otro país (P(X) cambia) pero el patrón fraude/no-fraude es el mismo (P(Y|X) intacto); reentrenar puede no hacer falta. El borde separa los dos tipos de drift.

## Errores típicos

- **Conceptual:** confundir data drift (distribución de entrada) con concept drift (relación aprendida); requieren monitoreos distintos.
- **Técnico:** esperar a tener labels para detectar problemas, cuando el data drift se ve sin ellos.
- **De supuestos:** desplegar sin baseline ni plan de rollback, de modo que un drift pasa inadvertido.

## Transferencia isomorfa

- **Data drift vs concept drift ↔ P(X) vs P(Y|X):** la misma descomposición distingue covariate shift de cambio de la función objetivo (conecta con [[arena-htd4]] y [[arena-s1]]).
- **PSI / Jensen-Shannon ↔ distancia entre distribuciones y test KS:** medir cuánto se alejó la entrada del baseline es comparar distribuciones, primo del test de Kolmogorov-Smirnov (conecta con [[arena-dg3]]).
- **Contenedor reproducible ↔ pipeline determinista:** empacar entorno+dependencias garantiza los mismos pasos siempre, la misma reproducibilidad que exige un pipeline de features (conecta con [[arena-dmls3]]).
- **Monitoreo + alertas ↔ observabilidad:** baseline, métricas en tiempo real y alarmas ante caídas son el mismo aparato que vigila un sistema en producción (conecta con [[arena-obs1]]).

Moraleja de la arista: *data drift (cambia la entrada) se ve sin labels comparando con un baseline; concept drift (cambia la relación) exige performance real — son alarmas distintas, monitoréalas por separado.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "El modelo funciona en mi notebook pero no en prod" | Contenerízalo (Docker): empaca dependencias + entorno |
| "Desplegar muchas instancias, alta disponibilidad" | Kubernetes orquesta el clúster |
| "Servir predicciones por HTTP" | Flask en `app.py` dentro del contenedor |
| "El modelo era preciso y ahora falla" | Data drift → comparar entrada vs baseline; reentrenar |
| "¿Cómo sé si el despliegue sirve?" | Validar con datos no vistos contra el endpoint |
| "Detectar cambio de distribución" | PSI / Jensen-Shannon vs baseline de training |
| "Recolectar datos batch y streaming" | ETL/ELT con Spark/Beam/Dask |
| "Industria regulada, auditoría del modelo" | Gobernanza: versionado + documentación + logging |

---

> **Síntesis:** MLOps operacionaliza el modelo: un pipeline automatizado, consistente y reproducible que va de prototipo a producción. La ingesta usa ETL/ELT (batch/streaming); el despliegue empaca el modelo con sus dependencias en un **contenedor Docker** (orquestado por **Kubernetes** a escala), sirviéndolo a menudo vía Flask. Tras desplegar se **valida** con datos no vistos y se **monitorea** en continuo: logging, métricas en tiempo real y detección de **data drift** (PSI / Jensen-Shannon vs baseline) que dispara el reentrenamiento — todo bajo gobernanza para entornos regulados.

---

*Retrieval: cierra y responde: (1) ¿qué problema resuelve contenerizar un modelo con Docker?; (2) Docker vs Kubernetes, ¿qué hace cada uno?; (3) ¿qué es data drift y cómo se detecta?; (4) ¿cómo validas un modelo recién desplegado?*
