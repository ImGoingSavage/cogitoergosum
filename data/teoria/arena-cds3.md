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
