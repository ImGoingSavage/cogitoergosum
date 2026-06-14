# Despliegue y predicción: batch vs online, compresión y edge

## Batch prediction vs online prediction

- **Batch prediction (asíncrona):** se calculan predicciones **por adelantado** en lotes, en un horario, y se **guardan** (p.ej. en una key-value store) para servirlas al instante. Buena cuando no necesitas frescura inmediata (recomendaciones de Netflix precomputadas). Riesgo: predicciones **rancias** y desperdicio si el usuario nunca las pide.
- **Online prediction (síncrona, on-demand):** se predice **al momento** que llega la petición, con los datos más frescos. Imprescindible cuando el input no se conoce de antemano (búsqueda, pricing dinámico). Reto: **latencia** — hay que ser rápido.

Pasar de batch a online suele **mejorar** la calidad (datos frescos) pero exige infraestructura de baja latencia y, a menudo, **streaming features**.

## Batch features vs streaming features

- **Batch features:** se calculan de datos históricos en reposo (la edad media de los clientes), por **batch processing**.
- **Streaming features:** se extraen de datos en movimiento por **stream processing** (cuántos viajes en los últimos 5 min). La mayoría de los sistemas online serios necesitan **ambas**; la computación en streaming rara vez es trivial y requiere su propia infraestructura (p.ej. Kafka/Flink).

> Pista de entrevista: el paso **request-driven** (REST) es síncrono; el **event-driven** (pub/sub, message broker) permite paso de datos **asíncrono** y desacopla servicios.

## Compresión de modelos (model compression)

Para que un modelo grande corra rápido o en dispositivos limitados, se **comprime**. Cuatro técnicas frecuentes:

1. **Low-rank factorization:** reemplaza tensores densos por factores de menor rango (convoluciones compactas).
2. **Knowledge distillation:** un modelo pequeño (**student**) se entrena para imitar a uno grande (**teacher**); ej.: **DistilBERT**. El student conserva casi el rendimiento a una fracción del tamaño.
3. **Pruning:** elimina parámetros/conexiones poco útiles (o los pone a cero), reduciendo tamaño y a veces mejorando generalización.
4. **Quantization:** representa los números con **menos bits** (de 32 a 16 u 8). Reduce memoria y acelera cómputo; el riesgo es la pérdida de precisión numérica (rango/redondeo). Es la más general y usada.

## Edge vs cloud

- **Cloud:** el cómputo vive en servidores; fácil de escalar, pero suma **latencia de red**, **coste** continuo, dependencia de conectividad y preocupaciones de **privacidad** (los datos salen del dispositivo).
- **Edge:** el modelo corre **en el dispositivo** (móvil, IoT). Gana latencia, funciona **sin red**, abarata el servidor y protege la privacidad; a cambio exige hardware capaz y modelos comprimidos. La tendencia empuja cómputo hacia el edge, lo que hace la compresión aún más relevante.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "No necesito frescura inmediata, alto volumen" | Batch prediction precomputada |
| "El input no se conoce de antemano / necesito datos frescos" | Online prediction (cuida la latencia) |
| "Features de los últimos minutos" | Streaming features (stream processing) |
| "Modelo demasiado grande/lento para servir" | Compresión: distillation/quantization/pruning/low-rank |
| "Imitar un modelo grande con uno chico" | Knowledge distillation (teacher→student) |
| "Sin red, baja latencia, privacidad" | Desplegar en el edge (modelo comprimido) |

---

> **Síntesis:** Servir un modelo se decide en tres ejes. **Batch vs online:** batch precomputa y guarda (rápido de servir, datos rancios); online predice on-demand con datos frescos pero pelea contra la latencia y suele exigir **streaming features**. **Compresión:** low-rank, **knowledge distillation** (student imita al teacher, p.ej. DistilBERT), **pruning** y **quantization** (menos bits) achican el modelo para servir rápido. **Edge vs cloud:** la nube escala fácil pero suma latencia de red, coste y riesgos de privacidad; el edge gana latencia, offline y privacidad a cambio de modelos comprimidos y hardware capaz.

---

*Retrieval: cierra y responde: (1) ¿cuándo batch y cuándo online prediction?; (2) diferencia batch features de streaming features; (3) nombra las 4 técnicas de compresión y qué hace la quantization; (4) dos ventajas del edge sobre la nube.*
