# Respuesta a incidentes: del triaje a la recuperación

> Recurso troncal: **Getting Started with MITRE ATT&CK**. Detectar ([[cyber-blue1]], [[cyber-blue2]]) solo sirve si **sabes qué hacer** cuando suena la alarma. Sigue de la inteligencia ([[cyber-blue3]]) y prepara [[cyber-blue5]] (mejora continua).

## De qué trata (y qué sabrás hacer al final)

Una alerta sin un plan de respuesta es pánico. La **respuesta a incidentes** es el proceso ordenado que convierte "algo raro pasó" en "lo entendimos, lo contuvimos, nos recuperamos y aprendimos". Para un científico de datos, saber el flujo importa: a menudo eres quien primero nota la anomalía en los datos o quien aporta el análisis durante un incidente.

La intuición: es el protocolo de emergencia de un hospital. No improvisas cuando llega el paciente grave; sigues fases —evaluar, estabilizar, tratar, recuperar, revisar el caso—. La respuesta a incidentes es ese protocolo para una brecha: practicado **antes**, ejecutado con cabeza fría **durante**.

Al terminar podrás: (1) recorrer las **fases** de respuesta (preparar, detectar/analizar, contener, erradicar, recuperar, lecciones); (2) hacer **triaje** de una alerta; (3) razonar **contención** sin destruir evidencia; y (4) entender por qué la preparación decide el resultado.

## Las fases de la respuesta (modelo NIST/SANS)

| Fase | Qué se hace |
|---|---|
| **Preparación** | Antes del incidente: planes, accesos, contactos, respaldos, práctica |
| **Detección y análisis** | Confirmar que es real, alcance e impacto (triaje, [[cyber-blue1]]) |
| **Contención** | Frenar la propagación sin alertar al atacante de más ni destruir evidencia |
| **Erradicación** | Eliminar la causa (cuenta comprometida, malware, acceso indebido) |
| **Recuperación** | Restaurar servicios desde un estado limpio y verificado |
| **Lecciones aprendidas** | Post-mortem sin culpas: qué falló, qué mejorar ([[cyber-blue5]]) |

No son rígidas ni lineales (a veces iteras), pero dan un orden que evita el caos.

## Triaje: ¿es real y cuán grave?

Ante una alerta ([[cyber-blue2]]), el triaje responde rápido: ¿es un falso positivo o un incidente real? ¿qué activos toca? ¿cuál es el impacto potencial? Aquí vuelve la pregunta clave de [[cyber-blue1]]: **"¿qué dato falta para confirmarlo?"**. El triaje correcto evita dos errores: escalar todo (fatiga) o ignorar lo grave. Define la **severidad**, que decide la urgencia y a quién se involucra.

## Contención sin destruir evidencia

El instinto es "apágalo todo". Pero la contención tiene matices:

- **Frenar sin avisar de más:** si el atacante nota que lo descubriste, puede acelerar el daño o borrar rastros. A veces se aísla el sistema en silencio.
- **Preservar evidencia:** apagar una máquina borra memoria volátil útil para entender el ataque; a menudo se aísla de la red en vez de apagar, y se toman copias forenses antes de limpiar.
- **Contención corta vs larga:** primero detener el sangrado (aislar la cuenta/host), luego una solución estable.

Equilibrio: detener el daño **y** conservar lo necesario para erradicar bien y aprender.

## Mini-ejemplo trabajado

Salta la alerta de [[cyber-blue2]]: una cuenta de analista descargó 4.2 GB del bucket de pacientes a las 3 a.m. desde una geo inusual. Respuesta:

- **Triaje:** ¿el analista viajó/usó VPN? ¿esa descarga es parte de su trabajo? Si nada lo justifica → incidente real, severidad alta (datos sensibles).
- **Contención:** deshabilitar/forzar reautenticación de la cuenta y revocar sus tokens ([[cyber-sys3]]); restringir el acceso del bucket; **sin** borrar logs ni la máquina (evidencia).
- **Erradicación:** determinar cómo se comprometió la cuenta (phishing, credencial filtrada — [[cyber-ms4]]), cerrar esa vía, rotar credenciales.
- **Recuperación:** restaurar acceso legítimo con MFA, confirmar que no quedó persistencia.
- **Lecciones:** ¿por qué no había límite ni alerta antes? → mejora la detección y el control de acceso ([[cyber-dp4]]).

## Señales de reconocimiento

| Señal | Problema de respuesta |
|---|---|
| Alerta y nadie sabe a quién avisar | Falta preparación |
| "Apaga todo ya" como reflejo | Destruye evidencia; puede no contener bien |
| Se borra el log para "limpiar" | Se pierde la evidencia del incidente |
| No se hace post-mortem | El mismo incidente se repetirá |
| Triaje ausente: todo es incidente o nada | Fatiga o ceguera |

## Errores típicos

- **Improvisar durante el incidente:** sin plan previo, se cometen errores costosos bajo presión.
- **Destruir evidencia al contener:** apagar/borrar antes de preservar imposibilita entender y erradicar.
- **Saltarse las lecciones aprendidas:** sin post-mortem, la organización no mejora.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** ante una alerta de exfiltración, triajeas si es real, contienes aislando la máquina sin apagarla (preservas evidencia), erradicas la vía de entrada y recuperas con MFA.
- **Contraejemplo:** un equipo con plan ensayado, contactos claros, respaldos verificados y un runbook por tipo de incidente: cuando salta la alerta, ejecutan con calma, contienen preservando evidencia y se recuperan rápido.
- **Caso borde:** un **falso positivo** tratado como incidente grave consume recursos y erosiona la confianza en las alertas; por eso el triaje (severidad) es la primera fase activa. La respuesta debe ser proporcional ([[cyber-ms5]]) a la severidad real.

## Transferencia a ciencia de datos e IA

Como DS, sueles ser quien detecta la anomalía (en datos, en métricas de un modelo) y quien aporta análisis durante el incidente. La respuesta a incidentes aplica también a sistemas de IA: un modelo envenenado o un asistente RAG abusado ([[cyber-ml-security]], [[cyber-llm-rag-agents]]) requieren contener (deshabilitar el modelo/herramienta), erradicar (limpiar datos/reentrenar) y recuperar. El post-mortem alimenta el monitoreo.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el mini-ejemplo, escribe los pasos de contención que preservan evidencia y los que no, y por qué.
- **Misión externa (lab vivo):** intenta un reto de análisis en **CyberDefenders** (https://cyberdefenders.org/blueteam-ctf-challenges/) o **Blue Team Labs Online** (https://blueteamlabs.online/) que incluya investigar un incidente. **Criterio de cierre:** reconstruir qué pasó y qué contendrías. Practica **solo** en laboratorios autorizados.
- **Mini-entregable:** un runbook breve para un tipo de incidente (p. ej. cuenta comprometida): fases, quién hace qué, y qué preservar.

---

> **Síntesis:** detectar sin un **plan de respuesta** es pánico. La respuesta a incidentes sigue fases —**preparación, detección/análisis, contención, erradicación, recuperación, lecciones aprendidas**—; el **triaje** define si es real y su severidad (preguntando "¿qué dato falta?"); y la **contención** frena el daño **preservando evidencia** (a menudo aislar, no apagar). La **preparación previa** decide el resultado, y el **post-mortem sin culpas** evita repetir el incidente.

---

**Referencias**

- Pennington, A. (Ed.), Applebaum, A., Nickels, K., Schulz, T., Strom, B., & Wunder, J. (2019). *Getting started with ATT&CK*. The MITRE Corporation.
- Cichonski, P., Millar, T., Grance, T., & Scarfone, K. (2012). *Computer security incident handling guide* (NIST SP 800-61 Rev. 2). NIST.

*Retrieval: (1) nombra las fases de respuesta a incidentes; (2) ¿qué decide el triaje?; (3) ¿por qué "apagar todo" puede ser mal y qué se prefiere?; (4) ¿por qué la preparación previa decide el resultado?*
