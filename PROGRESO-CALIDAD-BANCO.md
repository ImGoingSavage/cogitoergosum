# Progreso calidad banco Fase 8

Fecha: 2026-06-17  
Prompt ejecutado: `PROMPT-EJECUTOR-CALIDAD-BANCO.md`  
Marcador aplicado: `revision-calidad-humana-v1`

## Resumen

| Estado | Preguntas |
|---|---:|
| Reescritas en esta corrida desde marcador generado | 0 |
| Protegidas con marcador de revisión | 1325 |
| Conservadas sin tocar | 344 |
| Normalizadas en capa interactiva MC | 240 |

## Protegidas por tipo

| Tipo | Preguntas |
|---|---:|
| concepto | 960 |
| reflexion | 183 |
| scenario | 182 |

## Protegidas por cluster

| Cluster | Preguntas |
|---|---:|
| cyber-blue-team | 166 |
| cyber-data-privacy | 166 |
| cyber-llm-rag-agents | 166 |
| cyber-mindset | 164 |
| cyber-ml-security | 166 |
| cyber-secure-dev | 166 |
| cyber-systems-crypto | 165 |
| cyber-web-api | 166 |

## Muestras antes -> después

### Muestra 1: cyber-ms1
**Antes**
Enunciado: ¿Qué señal temprana te haría pensar que "Riesgo ≈ probabilidad × impacto (una vulnerabilidad sin impacto es ruido)" importa en una app de ciencia de datos con notebooks, Supabase, API keys, datasets sensibles, modelos y dashboards?
Opciones:
  - La señal suele ser un cruce de frontera: datos no confiables, permisos amplios, secreto expuesto, dependencia externa, salida automatizada, log insuficiente o decisión irreversible.
  - Instalar una herramienta genérica sin nombrar el activo ni el impacto de Riesgo ≈ probabilidad × impacto.
  - Confiar en que la unidad no aplica porque el sistema es interno o pequeño.
  - Resolverlo sólo con documentación, sin control técnico ni evidencia verificable.
**Después**
Enunciado: El equipo propone: "Aceptar el riesgo sin dueño, evidencia ni fecha de revisión.". ¿Qué corrección aplica mejor a Ciber · Mentalidad de seguridad: activos, amenazas y vocabulario del riesgo?
Opciones:
  - Nombrar el activo, explicar por qué se confunde una debilidad con riesgo real y elegir un control proporcional con evidencia.
  - Medir seguridad por cantidad de herramientas instaladas.
  - Aceptar el riesgo sin dueño, evidencia ni fecha de revisión.
  - Mover el control al cliente o a documentación sin verificación técnica.

### Muestra 2: cyber-web1
**Antes**
Enunciado: Compara dos defensas posibles para "La frontera de confianza real está en el servidor, no en el cliente" en una API educativa con login, roles, endpoints privados, carga de archivos y dashboards. ¿Cuál reduce más riesgo y qué costo introduce?
Opciones:
  - La defensa superior reduce impacto o probabilidad sobre el activo crítico con menor fricción razonable.
  - Instalar una herramienta genérica sin nombrar el activo ni el impacto.
  - Confiar en que Web I no aplica porque el sistema es interno o pequeño.
  - Resolverlo sólo con documentación, sin control técnico ni evidencia verificable.
**Después**
Enunciado: El supuesto oculto es: "validar en cliente basta". ¿Qué pregunta de revisión lo pondría a prueba?
Opciones:
  - ¿Qué pasa si ese supuesto falla, quién ve el impacto y dónde queda registrado?
  - Usar ORM raw concatenando strings.
  - Aceptar el riesgo sin dueño, evidencia ni fecha de revisión.
  - Mover el control al cliente o a documentación sin verificación técnica.

### Muestra 3: cyber-llm2
**Antes**
Enunciado: Plantea un test adversarial seguro para validar "Agencia excesiva (LLM06): el multiplicador de daño" sin atacar sistemas ajenos.
Opciones:
  - El test debe ejecutarse en laboratorio, staging o datos sintéticos; debe tener hipótesis, señal esperada, criterio de éxito, límite ético y acción correctiva si falla.
  - Instalar una herramienta genérica sin nombrar el activo ni el impacto de Agencia excesiva.
  - Confiar en que Seguridad de LLMs II no aplica porque el sistema es interno o pequeño.
  - Resolverlo sólo con documentación, sin control técnico ni evidencia verificable.
**Después**
Enunciado: El control de Ciber · Seguridad de LLMs II: RAG, agentes y agencia excesiva reduce riesgo pero introduce menos automatización y más confirmaciones. ¿Qué decisión técnica es más madura?
Opciones:
  - Comparar impacto, utilidad y evidencia; aceptar o rediseñar con riesgo residual documentado.
  - Confiar en que, por ser interno, el fallo no tiene impacto real.
  - Bloquear todo sin medir impacto, utilidad ni riesgo residual.
  - Usar permisos del bot para todo.

## Criterios aplicados

- Opción múltiple: 4 opciones, una correcta exacta, distractores plausibles y concisos.
- Escenarios/reflexiones: sin `options`, con decisión defensiva, evidencia y riesgo residual.
- Alcance: solo preguntas con `metadata.generated_by === "enriquecer-ciberseguridad-contrato-v1"`.
- Protección futura: el marcador viejo queda reemplazado para que el generador no destruya esta revisión.
