# Blue team II: detection engineering, hipótesis y mejora continua

> Recurso troncal: **Getting Started with MITRE ATT&CK**. Profundiza [[cyber-blue1]]: del mapa de conductas a **construir detecciones** y mejorarlas con el tiempo.

## De qué trata (y qué sabrás hacer al final)

Saber qué conductas existen (ATT&CK) no detecta nada por sí solo. La **detection engineering** es el oficio de convertir una conducta adversaria en una **regla** que produzca alertas útiles, medir si funciona, y cerrar las **brechas de cobertura** que descubras. Para un científico de datos es terreno natural: es diseño de un clasificador con un tradeoff de falsos positivos/negativos.

La intuición: una alarma de casa demasiado sensible suena con cada gato y la acabas ignorando (fatiga de alertas → falsos positivos); demasiado laxa y no suena con el ladrón (falsos negativos). La ingeniería de detección es **calibrar** esa alarma: definir qué conducta detectar, con qué datos, y a qué umbral, sabiendo que cada elección tiene un costo.

Al terminar podrás: (1) formular una **hipótesis de detección**; (2) razonar el tradeoff **falsos positivos ↔ negativos**; (3) usar **emulación adversaria controlada** para probar tus defensas; y (4) cerrar **brechas de cobertura** en un ciclo de mejora continua.

## De la conducta a la hipótesis de detección

Una **hipótesis de detección** es una afirmación comprobable: *"si un adversario exfiltra el bucket de pacientes, veré una descarga de volumen anómalo desde una cuenta que normalmente no lo hace, fuera de horario"*. De ahí sale la regla:

1. **Conducta** (técnica ATT&CK): exfiltración de datos.
2. **Fuente de datos:** logs de acceso al almacenamiento.
3. **Lógica:** volumen descargado > umbral **y** cuenta sin historial de esa acción **y** horario atípico.
4. **Salida:** alerta para triaje, no bloqueo automático ciego.

Nótese que es indistinguible de plantear un modelo: defines la señal, los datos, el umbral y la acción.

## El tradeoff que define todo: FP vs FN

| | Demasiado sensible | Demasiado laxa |
|---|---|---|
| Consecuencia | Muchos **falsos positivos** | Muchos **falsos negativos** |
| Daño | Fatiga de alertas; el equipo ignora todo | Te perforan sin que suene nada |
| Ajuste | Subir umbral, añadir contexto | Bajar umbral, añadir señales |

No existe la regla perfecta; existe la regla **bien calibrada para tu contexto y capacidad de respuesta**. Una buena detección incluye **contexto** (¿la cuenta suele hacer esto? ¿el usuario está de viaje?) para reducir FP sin perder al atacante real. Esto conecta directo con curvas precision-recall que ya conoces.

## Emulación adversaria controlada

¿Cómo sabes si tus detecciones funcionan **antes** del ataque real? Emulando al adversario de forma **controlada y autorizada**: ejecutar, en un entorno seguro y con permiso, las técnicas ATT&CK que te preocupan, y verificar si tus reglas las cazan. Si la técnica pasa sin disparar nada, encontraste una **brecha de cobertura**. (Importante y no negociable: la emulación se hace **solo** en sistemas propios o autorizados, jamás contra terceros.)

## Brechas de cobertura y mejora continua

La defensa no es un estado, es un **ciclo**: mapeas qué técnicas te importan (ATT&CK) → revisas cuáles puedes detectar hoy → las no cubiertas son **brechas** → priorizas y construyes detección para ellas → emulas para validar → y repites, porque los adversarios y tu sistema cambian. Una "matriz de cobertura" (qué técnicas detectas vs cuáles no) hace visible el progreso, igual que un tablero de métricas de modelo.

## Mini-ejemplo trabajado

Tras el incidente de [[cyber-blue1]] (descarga de 4.2 GB del bucket de pacientes), tu detección actual no disparó: solo alertaba por "login fallido", no por exfiltración. Ciclo de mejora:

1. **Brecha identificada:** sin detección de exfiltración por volumen.
2. **Hipótesis:** descarga anómala en bytes/objetos + cuenta sin ese patrón + horario.
3. **Regla calibrada:** umbral basado en el percentil histórico por cuenta (no un número fijo), con contexto de horario; salida = alerta a triaje.
4. **Validación por emulación:** en un entorno de prueba, simulas una descarga grande autorizada y confirmas que la regla dispara, ajustando el umbral para no marcar los respaldos legítimos nocturnos (reducir FP).
5. **Cierre:** documentas la cobertura nueva y el riesgo residual restante.

## Señales de reconocimiento

| Señal | Acción de detection engineering |
|---|---|
| El equipo ignora las alertas | Demasiados FP → recalibrar con contexto |
| "Nunca nos ha sonado nada" | Posible exceso de FN → emular para verificar |
| Regla con umbral fijo global | Sustituir por línea base por entidad |
| Técnica ATT&CK sin ninguna regla | Brecha de cobertura → priorizar |

## Errores típicos

- **Optimizar solo por menos alertas:** bajar FP subiendo el umbral hasta volverte ciego (FN).
- **Detección "de una vez":** no revisar ni emular; las reglas se degradan al cambiar el sistema.
- **Umbral global ignorando la línea base:** lo normal para una cuenta es anómalo para otra; sin baseline, todo es ruido o nada lo es.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** escribes una hipótesis de detección (conducta: muchos logins fallidos y luego uno exitoso; fuente: logs de auth; lógica: umbral por cuenta; salida: alerta) y la validas con emulación autorizada.
- **Contraejemplo:** una regla con contexto (línea base por cuenta + horario + tipo de recurso) que caza la exfiltración real con pocos FP: detección **buena** es la que tu equipo *puede* atender.
- **Caso borde:** un atacante que exfiltra **lento y bajo** (poco volumen, muchos días) evade los umbrales de volumen; requiere detección de patrones acumulados en el tiempo, no por evento. Toda detección tiene un punto ciego que el adversario buscará.

## Transferencia a ciencia de datos e IA

Detection engineering **es** ciencia de datos aplicada a seguridad: ingeniería de features sobre logs, líneas base por entidad, tradeoff precision-recall, validación. Estas mismas detecciones vigilarán los activos de IA —entradas adversarias a un modelo ([[cyber-ml-security]]), abuso de un endpoint de LLM ([[cyber-llm-rag-agents]])— y el **monitoreo** de un sistema ML es la versión de disponibilidad/integridad de este ciclo.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** escribe una hipótesis de detección para "acceso a un repo desde una cuenta recién creada" y di cómo reducirías sus FP.
- **Misión externa (lab vivo):** intenta un reto de **CyberDefenders** (https://cyberdefenders.org/blueteam-ctf-challenges/) o **Blue Team Labs Online** (https://blueteamlabs.online/) de nivel introductorio, analizando logs. **Criterio de cierre:** describir una detección que construirías a partir de lo observado. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable:** una mini "matriz de cobertura" de 5 técnicas ATT&CK con estado *detectada / brecha* y la regla propuesta para cada brecha.

---

> **Síntesis:** la **detection engineering** convierte conductas (ATT&CK) en reglas comprobables a partir de una **hipótesis de detección**, navegando el tradeoff **falsos positivos ↔ negativos** con **contexto y líneas base por entidad**. Se valida con **emulación adversaria controlada y autorizada**, y se gestiona como **ciclo de mejora continua** que cierra **brechas de cobertura**. Es, en el fondo, ciencia de datos aplicada a la defensa.

---

**Referencias**

- Pennington, A. (Ed.), Applebaum, A., Nickels, K., Schulz, T., Strom, B., & Wunder, J. (2019). *Getting started with ATT&CK*. The MITRE Corporation.
- MITRE. (n.d.). *MITRE ATT&CK*. https://attack.mitre.org
- CyberDefenders. (n.d.). *Blue team CTF challenges*. https://cyberdefenders.org/blueteam-ctf-challenges/

*Retrieval: (1) ¿qué es una hipótesis de detección?; (2) explica el tradeoff FP/FN y la fatiga de alertas; (3) ¿qué es emulación adversaria y su límite ético?; (4) ¿por qué un umbral por entidad supera a uno global?*
