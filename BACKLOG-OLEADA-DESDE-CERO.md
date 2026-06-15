# Backlog — Oleada "lecciones desde cero" (auditoría Fase 7)

> **Qué es esta oleada.** Reescribir cada lección de teoría de la Fase 7
> (`data/teoria/arena-*.md`) para que **asuma conocimiento nulo y construya desde
> ahí**, siguiendo el contrato de `auditoria.md`, con la matemática en **LaTeX**
> (la renderiza KaTeX, ya vendorizado). Es una capa más profunda que la Oleada 2
> (que solo insertaba secciones): aquí cada lección se reescribe entera —pero
> **conservando todo el contenido curado**—.
>
> Última actualización: 2026-06-15 (cluster 1 completo, sw.js v87).
> Lee también: `PROMPT-OLEADA-DESDE-CERO.md` (instrucciones para el agente),
> `HANDOFF-AUDITORIA-FASE7.md` §7 (registro), `auditoria.md` (contrato de calidad),
> `CLAUDE.md` → `HANDOFFCES.md` §0 (Constitución, es LEY).

## Progreso global

| Cluster | Unidades | Estado |
|---|---|---|
| **1. quant-prob** (Probabilidad, esperanza y conteo) | 25 | ✅ **COMPLETO** (v82–v87) |
| 2. stats-inf (Estadística aplicada e inferencia) | 16 | ⬜ pendiente |
| 3. dsa (Estructuras de datos y algoritmos) | 6 | ⬜ pendiente |
| 4. system-design (Diseño de sistemas) | 4 | ⬜ pendiente |
| 5. ds-applied (Ciencia de datos aplicada) | 9 | ⬜ pendiente |
| 6. ml-systems (ML Systems y feature pipelines) | 32 | ⬜ pendiente |
| 7. causal-health (Causalidad y Health AI / RWE) | 22 | ⬜ pendiente |
| 8. conductual (Conductual y comunicación) | 4 | ⬜ pendiente |
| | **118** | **25 / 118 hechas** |

> El orden de las unidades dentro de cada cluster es el **orden didáctico** de
> `data/entrevista/_taxonomia.json` (cimientos → avanzado). Trabaja en ese orden;
> es también el orden en que el usuario las ve en la app.

---

## Cómo marcar progreso

Marca `[x]` cuando una lección queda reescrita **y validada** (renderiza en KaTeX
sin throw, secciones del contrato presentes). Commitea por lotes de 4-5 lecciones
subiendo `VERSION` en `sw.js`, y actualiza este backlog + `HANDOFF` §7.

---

### 1. quant-prob — Probabilidad, esperanza y conteo (25) — ✅ COMPLETO

- [x] `arena-b1` — Fundamentos de probabilidad y conteo
- [x] `arena-p1` — Acertijos matemáticos y razonamiento rápido
- [x] `arena-q1` — Linealidad de la esperanza
- [x] `arena-q2` — Bayes, tasas base y señales ruidosas
- [x] `arena-p2` — Combinatoria y probabilidad discreta
- [x] `arena-fc1` — Coincidencias, urnas y emparejamiento
- [x] `arena-b2` — Variables aleatorias conjuntas y correlación
- [x] `arena-b3` — Distribuciones importantes y sus relaciones
- [x] `arena-q10` — Distribuciones, geometría y estadísticos de orden
- [x] `arena-fc2` — Probabilidad geométrica
- [x] `arena-q4` — Probabilidad y Bayes (Monty Hall, etc.)
- [x] `arena-q9` — Probabilidad condicional, Bayes y conteo
- [x] `arena-fc3` — Paradojas probabilísticas
- [x] `arena-q3` — Brainteasers: patrones y lógica
- [x] `arena-q12` — Brainteasers: trucos, invariantes y conteo
- [x] `arena-q13` — Brainteasers: lógica, inducción y juegos
- [x] `arena-q8` — Esperanza, juegos y parada óptima
- [x] `arena-fc4` — Apuestas, colas y azar en el tiempo
- [x] `arena-b4` — Cadenas de Markov e inferencia bayesiana
- [x] `arena-p3` — Procesos estocásticos y movimiento browniano
- [x] `arena-q11` — Movimiento browniano, Itô y martingalas
- [x] `arena-p4` — Cálculo y álgebra lineal para finanzas cuantitativas
- [x] `arena-q5` — Derivadas y mercados (no-arbitraje, Black-Scholes)
- [x] `arena-q7` — Finanzas avanzadas: bonos, Greeks y procesos
- [x] `arena-q6` — Estadística inferencial: distribuciones y estimación

### 2. stats-inf — Estadística aplicada e inferencia (16) — ⬜

- [ ] `arena-dg1` — Estimación puntual y propiedades de estimadores
- [ ] `arena-dg2` — Máxima verosimilitud y familias exponenciales
- [ ] `arena-cb1` — Suficiencia, completitud y Basu
- [ ] `arena-cb2` — MLE, Cramér-Rao y UMVUE
- [ ] `arena-dg3` — Intervalos de confianza y tests de hipótesis
- [ ] `arena-cb3` — NP Lemma, LRT y tests UMP
- [ ] `arena-cb4` — Intervalos de confianza y métodos asintóticos
- [ ] `arena-dg4` — Teoría de la decisión, regresión y modelos lineales
- [ ] `arena-pst1` — Análisis exploratorio: estimadores robustos
- [ ] `arena-pst2` — Distribuciones muestrales y bootstrap
- [ ] `arena-pst3` — Experimentos estadísticos y tests de permutación
- [ ] `arena-pst4` — Regresión y predicción: interpretación y diagnóstico
- [ ] `arena-isl1` — El marco (estimar f, sesgo-varianza, KNN)
- [ ] `arena-isl2` — Regresión lineal y clasificación
- [ ] `arena-isl3` — Remuestreo, selección y regularización
- [ ] `arena-isl4` — No linealidad, árboles, SVM y no supervisado

### 3. dsa — Estructuras de datos y algoritmos (MAANG) (6) — ⬜

- [ ] `arena-cc1` — Arrays, cadenas y tablas hash
- [ ] `arena-m1` — Hashing, frecuencia y memoria comprada
- [ ] `arena-cc4` — Ordenamiento, búsqueda binaria y bits
- [ ] `arena-cc2` — Árboles, grafos y búsqueda
- [ ] `arena-cc3` — Recursión y programación dinámica
- [ ] `arena-m2` — SQL Window Functions

### 4. system-design — Diseño de sistemas (MAANG) (4) — ⬜

- [ ] `arena-sd1` — Fundamentos de escalabilidad y estimación
- [ ] `arena-sd2` — Bloques distribuidos fundamentales
- [ ] `arena-sd3` — Sistemas de datos a escala
- [ ] `arena-sd4` — Sistemas en tiempo real y de medios

### 5. ds-applied — Ciencia de datos aplicada (9) — ⬜

- [ ] `arena-ads1` — Probabilidad para ciencia de datos
- [ ] `arena-ads2` — Estadística e inferencia
- [ ] `arena-ads4` — SQL y product sense / A·B testing
- [ ] `arena-cds1` — Feature engineering y preparación de datos
- [ ] `arena-ads3` — Machine Learning aplicado
- [ ] `arena-cds2` — Deep learning: redes neuronales por dentro
- [ ] `arena-cds3` — MLOps: despliegue y monitoreo en producción
- [ ] `arena-s1` — Del modelo al sistema: skew, drift y rollback
- [ ] `arena-cds4` — Toolkit práctico: visualización, storytelling y Git

### 6. ml-systems — ML Systems y feature pipelines (32) — ⬜

- [ ] `arena-rom1` — Antes del ML y tu primer pipeline
- [ ] `arena-dmls1` — Encuadre de problemas de ML: objetivos y tipos de tarea
- [ ] `arena-rom2` — Tu primer objetivo y feature engineering
- [ ] `arena-dmls2` — Datos de entrenamiento: muestreo, etiquetas y desbalance
- [ ] `arena-mldp1` — Patrones de representación de datos y de problemas
- [ ] `arena-rml2` — Datos como pasivo y sistemas de entrenamiento confiables
- [ ] `arena-mldp2` — Ensembles, cascada, clase neutra y rebalanceo
- [ ] `arena-mldp3` — Patrones de entrenamiento y de serving resiliente
- [ ] `arena-rom4` — Fase III: modelos complejos y trade-offs
- [ ] `arena-dmls3` — Despliegue y predicción: batch vs online, compresión y edge
- [ ] `arena-rml3` — Serving, monitoreo y observabilidad de modelos
- [ ] `arena-rom3` — Análisis humano y training-serving skew
- [ ] `arena-dmls4` — Cambios de distribución, monitoreo y test en producción
- [ ] `arena-rml1` — Confiabilidad e2e: ciclo de vida del ML y los SLOs
- [ ] `arena-sre1` — Fundamentos SRE: riesgo, error budgets y SLOs
- [ ] `arena-sre2` — Eliminar toil, monitoreo y las cuatro señales doradas
- [ ] `arena-sre3` — Troubleshooting, incidentes y postmortems sin culpa
- [ ] `arena-sre4` — Robustez en producción: releases, simplicidad, sobrecarga y cascada
- [ ] `arena-rml4` — Respuesta a incidentes en sistemas de ML
- [ ] `arena-obs1` — ¿Qué es observabilidad? Monitoreo vs. observabilidad
- [ ] `arena-obs2` — Eventos, trazas y Core Analysis Loop
- [ ] `arena-obs3` — SLOs, alertas por síntoma y burn alerts
- [ ] `arena-obs4` — Escala: almacenamiento, muestreo y madurez
- [ ] `arena-htd1` — Deuda técnica ML: fundamentos y erosión de fronteras
- [ ] `arena-htd2` — Dependencias de datos y feedback loops
- [ ] `arena-htd3` — Anti-patrones de sistema y configuración
- [ ] `arena-htd4` — Mundo externo, otras deudas y medición
- [ ] `arena-mldp4` — Patrones de reproducibilidad e IA responsable
- [ ] `arena-iml1` — Interpretabilidad: conceptos, taxonomía y buenas explicaciones
- [ ] `arena-iml2` — Modelos interpretables (intrínsecos)
- [ ] `arena-iml3` — Métodos agnósticos: efectos e importancia
- [ ] `arena-iml4` — LIME, Shapley/SHAP y ejemplos

### 7. causal-health — Causalidad y Health AI / RWE (22) — ⬜

- [ ] `arena-h15` — La escalera de la causalidad (Pearl)
- [ ] `arena-h16` — Diagramas, junciones y paradojas (Pearl)
- [ ] `arena-h1` — DAGs y adjustment sets
- [ ] `arena-h17` — do-operator, back-door, front-door y do-calculus
- [ ] `arena-h3` — Contrafactuales, experimentos e identificación
- [ ] `arena-h19` — Resultados potenciales y sesgo de selección (Mixtape)
- [ ] `arena-h4` — Confundimiento, selección y sesgo de medición
- [ ] `arena-h18` — Contrafactuales y mediación (Pearl)
- [ ] `arena-h5` — Modelos: IP weighting, g-fórmula, PS, IV
- [ ] `arena-h20` — Matching, subclasificación y propensity score
- [ ] `arena-h21` — Variables instrumentales y RDD
- [ ] `arena-h22` — Panel/efectos fijos, DiD y control sintético
- [ ] `arena-h2` — Target trial emulation e immortal time bias
- [ ] `arena-h6` — Longitudinal, supervivencia y target trial
- [ ] `arena-h7` — Supervivencia: fundamentos, Kaplan-Meier y log-rank
- [ ] `arena-h8` — Modelo de Cox y supuesto PH
- [ ] `arena-h9` — Cox extendido y modelos paramétricos/AFT
- [ ] `arena-h10` — Eventos recurrentes y riesgos competitivos
- [ ] `arena-h11` — OHDSI: comunidad, datos observacionales y OMOP CDM
- [ ] `arena-h12` — OHDSI: vocabularios, ETL y calidad de datos
- [ ] `arena-h13` — OHDSI: analítica estandarizada
- [ ] `arena-h14` — OHDSI: calidad de la evidencia, validez y estudios en red

### 8. conductual — Conductual y comunicación bajo presión (4) — ⬜

- [ ] `arena-c1` — Conflicto, colaboración y comunicación (STAR)
- [ ] `arena-c2` — Fracaso, errores, ambigüedad y feedback (STAR)
- [ ] `arena-c3` — Liderazgo, iniciativa, impacto y priorización (STAR)
- [ ] `arena-c4` — Data science aplicada, stakeholders y carrera (STAR)

---

## Orden sugerido de clusters

1. **conductual (4)** o **system-design (4)** — cortos, buenos para calibrar el tono
   en un dominio nuevo (poca/ninguna matemática → buena prueba del estilo "desde cero").
2. **dsa (6)** — algoritmos; matemática ligera, mucho pseudocódigo/complejidad.
3. **ds-applied (9)** y **stats-inf (16)** — estadística aplicada; aprovecha aristas
   ya tendidas hacia quant-prob (p-valor, bootstrap, MLE↔OLS, sesgo-varianza).
4. **causal-health (22)** — causalidad/supervivencia/RWE; cuida `<restricciones_clinicas>`
   de `auditoria.md` (nada clínico/diagnóstico en el contenido).
5. **ml-systems (32)** — el más grande; déjalo para el final, ya con el estilo afinado.

*(Es una sugerencia; Edgar puede pedir otro orden.)*
