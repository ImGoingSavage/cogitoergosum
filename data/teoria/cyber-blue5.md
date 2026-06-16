# Mejora continua: emulación adversaria, brechas de cobertura y métricas

> Recurso troncal: **Getting Started with MITRE ATT&CK**. Capstone del cluster blue team: la defensa no es un estado sino un **ciclo**. Integra [[cyber-blue1]]–[[cyber-blue4]] y prepara el mini-proyecto (mini-SOC).

## De qué trata (y qué sabrás hacer al final)

Una defensa que no se prueba se degrada en silencio: el sistema cambia, los atacantes evolucionan, y las reglas de ayer dejan huecos hoy. Esta lección cierra el cluster con el motor que mantiene la defensa viva: **emular** al adversario para validar, medir la **cobertura** para ver los huecos, y mejorar en ciclo. Es la versión defensiva del *deliberate practice*: practicar contra resistencia para crecer.

La intuición: un equipo deportivo no asume que su defensa funciona; la prueba en entrenamientos contra un sparring (emulación), revisa la grabación para ver por dónde le anotaron (brechas), y ajusta. La seguridad madura hace lo mismo: ataca sus propias defensas, a propósito y de forma controlada, para encontrar los huecos antes que el adversario real.

Al terminar podrás: (1) usar **emulación adversaria** (purple team) para validar detección; (2) medir **cobertura** contra ATT&CK y hallar brechas; (3) elegir **métricas** útiles (y evitar las engañosas); y (4) ejecutar el mini-proyecto de mini-SOC.

## Emulación adversaria y purple teaming

De [[cyber-blue2]]: emular es ejecutar, **de forma controlada y autorizada**, las técnicas ATT&CK que te preocupan para ver si tus detecciones las cazan. El **purple team** une al equipo ofensivo (red, que emula) y defensivo (blue, que detecta) trabajando juntos: el red ejecuta una técnica, el blue verifica si saltó la alerta, y ajustan en el momento. Lo que pasa **sin** disparar nada es una **brecha de cobertura**. Límite no negociable: solo sobre sistemas propios o autorizados.

## Cobertura: hacer visibles los huecos

No puedes mejorar lo que no mides. Una **matriz de cobertura** mapea las técnicas ATT&CK relevantes (priorizadas por inteligencia, [[cyber-blue3]]) contra tu capacidad de detectarlas: detectada / parcial / brecha. Hace el progreso visible y evita el autoengaño de "estamos cubiertos". Las brechas priorizadas se vuelven el backlog de detección ([[cyber-blue2]]).

Cuidado con el **teatro de cobertura**: marcar una técnica como "detectada" porque existe una regla, sin haber verificado que realmente dispara (eso lo confirma la emulación).

## Métricas útiles vs engañosas

| Métrica engañosa | Por qué engaña | Mejor métrica |
|---|---|---|
| "N.º de alertas" | Más alertas ≠ más seguridad (puede ser ruido) | % de incidentes reales detectados |
| "N.º de reglas" | Tener reglas ≠ que funcionen | Cobertura verificada por emulación |
| "Vulnerabilidades cerradas" | Sin contexto de riesgo | Tiempo de detección y de respuesta (MTTD/MTTR) |

Buenas métricas miden **resultado** (¿detectamos rápido lo que importa?), no **actividad** (¿cuántas cosas hicimos?). Conecta con la comunicación de riesgo de [[cyber-ms5]].

## Mini-ejemplo trabajado

Tu equipo cree estar "bien cubierto" porque tiene 200 reglas de detección. Aplica el ciclo:

- **Emulación:** ejecutas (autorizado) una exfiltración de datos simulada del bucket. Resultado: **no saltó nada** — la regla existía pero filtraba por otra cosa. Brecha confirmada.
- **Cobertura:** mapeas las técnicas relevantes a tu sector ([[cyber-blue3]]); descubres que cubres bien "acceso inicial" pero mal "exfiltración" y "movimiento lateral".
- **Mejora:** construyes/ajustas detección de exfiltración por volumen vs línea base ([[cyber-blue2]]) y la **revalidas** emulando de nuevo hasta que dispara sin marcar respaldos legítimos.
- **Métricas:** dejas de reportar "200 reglas" y empiezas a reportar cobertura verificada y MTTD. El "estábamos cubiertos" era teatro; ahora hay evidencia.

## Señales de reconocimiento

| Señal | Diagnóstico |
|---|---|
| "Tenemos N reglas, estamos cubiertos" | Teatro de cobertura sin verificar |
| Nunca se emulan ataques | Defensa no probada (se degrada) |
| Se reporta actividad, no resultados | Métricas engañosas |
| Brechas conocidas sin priorizar | Falta ciclo de mejora |
| Reglas que nadie revisa al cambiar el sistema | Detección que envejece |

## Errores típicos

- **Confundir actividad con seguridad:** muchas reglas/alertas no implican estar protegido.
- **Marcar cobertura sin verificar:** "hay una regla" ≠ "la regla detecta"; solo la emulación lo confirma.
- **No cerrar el ciclo:** emular y no actuar sobre las brechas halladas.

## Contraejemplo y caso borde

- **Contraejemplo:** un equipo que emula trimestralmente las técnicas relevantes, mantiene una matriz de cobertura verificada y mide MTTD/MTTR: su "estamos cubiertos" está respaldado por evidencia y mejora cada ciclo.
- **Caso borde:** la emulación cubre lo que **anticipas**; un adversario con una técnica nueva no emulada puede pasar. Por eso el ciclo se complementa con detección de anomalías de comportamiento ([[cyber-blue2]]) y con inteligencia actualizada ([[cyber-blue3]]) para lo desconocido.

## Transferencia a ciencia de datos e IA

El ciclo emular→medir→mejorar es *deliberate practice* aplicado a la defensa, y es idéntico al ciclo de validación de un modelo (probar contra casos difíciles, medir, reentrenar). Las técnicas adversarias contra IA se emulan con marcos como **MITRE ATLAS** ([[cyber-ml-security]]); el "red teaming" de un LLM ([[cyber-llm-rag-agents]]) es esta misma idea aplicada a prompts y agentes.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** propón una emulación segura para validar tu detección de exfiltración y di qué brecha buscarías.
- **Misión externa (lab vivo):** en un reto de **CyberDefenders** (https://cyberdefenders.org/blueteam-ctf-challenges/) identifica una conducta y define la detección que la cubriría; relaciónala con ATT&CK. Practica **solo** en laboratorios autorizados.
- **Mini-entregable (mini-proyecto del cluster):** un **mini-SOC**: analiza logs ficticios de acceso indebido a notebooks/buckets/repos/dashboards, mapea a ATT&CK, propón reglas de detección, una matriz de cobertura de 5 técnicas (detectada/brecha) y qué emularías para validarlas. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** la defensa es un **ciclo**, no un estado: **emula** al adversario (purple team, solo autorizado) para validar que tus detecciones realmente disparan, mide la **cobertura** contra ATT&CK para hacer visibles las **brechas**, y prioriza cerrarlas. Usa **métricas de resultado** (incidentes reales detectados, MTTD/MTTR) y no de actividad (n.º de reglas/alertas), evitando el **teatro de cobertura** de marcar "detectado" sin verificar.

---

**Referencias**

- Pennington, A. (Ed.), Applebaum, A., Nickels, K., Schulz, T., Strom, B., & Wunder, J. (2019). *Getting started with ATT&CK*. The MITRE Corporation.
- MITRE. (n.d.). *MITRE ATT&CK*. https://attack.mitre.org
- CyberDefenders. (n.d.). *Blue team CTF challenges*. https://cyberdefenders.org/blueteam-ctf-challenges/

*Retrieval: (1) ¿qué es emulación adversaria / purple team?; (2) ¿qué hace visible una matriz de cobertura y qué es el teatro de cobertura?; (3) da una métrica engañosa y su alternativa de resultado; (4) ¿por qué el ciclo no basta contra técnicas nuevas?*
