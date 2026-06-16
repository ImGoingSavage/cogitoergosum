# Blue team I: MITRE ATT&CK, tácticas, técnicas y logs

> Recurso troncal: **Getting Started with MITRE ATT&CK**. Hasta aquí prevenimos; ahora aprendemos a **detectar**, porque ningún sistema es impenetrable. Sigue en [[cyber-blue2]] (detection engineering).

## De qué trata (y qué sabrás hacer al final)

La prevención falla; eso no es pesimismo, es diseño (recuerda el **riesgo residual** de [[cyber-ms2]]). El **blue team** asume que algo eventualmente entrará y se prepara para **verlo a tiempo**. La herramienta mental que organiza esa defensa es **MITRE ATT&CK**: un catálogo de lo que los adversarios realmente hacen, basado en observaciones del mundo real. Convierte "defiéndete de los hackers" en "detecta *estas* conductas concretas".

La intuición: un detective no memoriza a todos los criminales; conoce el **modus operandi** —cómo entran, cómo se mueven, cómo se llevan el botín—. ATT&CK es ese catálogo de modus operandi: **tácticas** (el *qué* persigue el adversario: acceso inicial, persistencia, exfiltración) y **técnicas** (el *cómo* lo logra). Si sabes qué huellas deja cada técnica, sabes qué **logs** mirar.

Al terminar podrás: (1) usar ATT&CK como **mapa**; (2) distinguir **táctica de técnica**; (3) leer **logs** y mapearlos a conductas adversarias; y (4) distinguir **evento, alerta, indicador e incidente**.

## ATT&CK: el mapa de conductas adversarias

ATT&CK organiza el comportamiento del atacante en una matriz:

- **Tácticas** = objetivos del adversario, en columnas: *Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Exfiltration, Impact*…
- **Técnicas** = formas concretas de lograr cada táctica (p. ej., táctica *Credential Access* → técnica "volcado de credenciales").

El valor para un DS: en vez de pánico difuso, obtienes una **lista priorizable** de conductas que podrías detectar en *tus* sistemas (notebooks, buckets, repos, dashboards). "¿Cubro la exfiltración de datos? ¿el acceso inicial por credenciales robadas?" se vuelven preguntas concretas.

## De la conducta al log

Cada técnica deja **huellas** en algún registro. Defender es saber qué fuente de log evidencia qué conducta:

| Conducta (técnica) | Log donde se ve |
|---|---|
| Login desde lugar/hora inusual | Logs de autenticación |
| Descarga masiva de un bucket | Logs de acceso al almacenamiento |
| Ejecución de comando inesperado | Logs de proceso/host |
| Llamadas anómalas a la API | Logs de la aplicación / gateway |
| Salida de datos a un destino raro | Logs de red / egress |

Sin la fuente de log adecuada, una técnica es **invisible**: no puedes detectar lo que no registras. Por eso "¿qué dato me falta para confirmarlo?" es la pregunta blue team por excelencia.

## El vocabulario: evento, indicador, alerta, incidente

- **Evento:** cualquier cosa registrada (un login, una consulta). La mayoría son benignos.
- **Indicador (IoC):** una señal asociada a actividad maliciosa (una IP conocida, un hash de malware).
- **Alerta:** un evento (o patrón) que una regla marcó como sospechoso y merece revisión.
- **Incidente:** una alerta **confirmada** como actividad maliciosa real, que dispara respuesta.

La cadena **evento → (regla) → alerta → (triaje) → incidente** evita dos errores opuestos: ahogarse en eventos (todo es ruido) o gritar "incidente" ante cada anomalía (todo es pánico). El triaje —decidir si una alerta es real— es el trabajo central.

## Mini-ejemplo trabajado: leer un log

```
2026-06-16 03:14  user=analista_4  action=login        ip=203.0.113.9  geo=RU   result=ok
2026-06-16 03:15  user=analista_4  action=bucket.list  bucket=pacientes        result=ok
2026-06-16 03:16  user=analista_4  action=bucket.get   objects=12,431          bytes=4.2GB
```

Lectura blue team: login OK pero desde una geo inusual a las 3 a.m. (posible **Credential Access** con credenciales robadas), seguido de **Discovery** (listar el bucket) y **Collection/Exfiltration** (descargar 4.2 GB de datos de pacientes). Es un patrón ATT&CK clásico. ¿Es incidente? Aún es **alerta**: para confirmarlo necesitas saber si `analista_4` viajó, si usa VPN, si esa descarga es parte de su trabajo. El dato que falta define el triaje.

## Señales de reconocimiento

| Señal en logs | Conducta probable (ATT&CK) |
|---|---|
| Login geo/hora atípica tras varios fallos | Credential access / fuerza bruta |
| Enumeración de recursos poco habitual | Discovery |
| Acceso a sistemas que ese usuario nunca toca | Lateral movement |
| Volumen de egress anómalo | Exfiltration |
| Borrado de logs | Defense evasion |

## Errores típicos

- **Detectar sin fuente de log:** querer ver una conducta que no se registra en ningún lado.
- **Confundir alerta con incidente:** disparar respuesta (o ignorar) sin triaje.
- **Coleccionar logs y no mirarlos:** logs sin hipótesis de detección son solo costo de almacenamiento.

## Contraejemplo y caso borde

- **Contraejemplo:** un SIEM carísimo que ingiere todo… pero sin reglas mapeadas a ATT&CK: mucha telemetría, cero detección. Recolectar ≠ detectar.
- **Caso borde:** un *insider* autorizado que abusa de su acceso legítimo no dispara las alertas de "acceso no autorizado"; se detecta por **comportamiento anómalo** (volumen, horario), no por permisos. La detección de insiders es intrínsecamente más sutil.

## Transferencia a ciencia de datos e IA

Mapear conductas a logs es, literalmente, un problema de **detección de anomalías** —tu especialidad—. Las hipótesis de detección de [[cyber-blue2]] son features e hipótesis estadísticas. Y los activos a vigilar son los de toda la ruta: notebooks ([[cyber-sys1]]), datasets ([[cyber-data-privacy]]), modelos ([[cyber-ml-security]]) y endpoints de LLM ([[cyber-llm-rag-agents]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** sobre el log del mini-ejemplo, etiqueta cada línea con su táctica ATT&CK y di qué dato confirmaría el incidente.
- **Misión externa (lab vivo):** navega **MITRE ATT&CK** (https://attack.mitre.org), elige una táctica (p. ej. *Exfiltration*) y lee 2 técnicas. **Criterio de cierre:** nombrar, por técnica, qué log la evidenciaría.
- **Mini-entregable:** una tabla "técnica ATT&CK → fuente de log → señal" para 5 conductas relevantes a un entorno de datos.

---

> **Síntesis:** como la prevención falla, el blue team **detecta**. **MITRE ATT&CK** cataloga conductas adversarias en **tácticas** (qué buscan) y **técnicas** (cómo). Cada técnica deja huellas en un **log**: no detectas lo que no registras. Ordena el ruido con la cadena **evento → alerta → incidente**, donde el **triaje** —y preguntar "¿qué dato falta?"— es el trabajo central.

---

**Referencias**

- Pennington, A. (Ed.), Applebaum, A., Nickels, K., Schulz, T., Strom, B., & Wunder, J. (2019). *Getting started with ATT&CK*. The MITRE Corporation.
- MITRE. (n.d.). *MITRE ATT&CK*. https://attack.mitre.org

*Retrieval: (1) táctica vs técnica; (2) ¿por qué "no detectas lo que no registras"?; (3) define evento, alerta e incidente; (4) ¿por qué un insider es difícil de detectar por permisos?*
