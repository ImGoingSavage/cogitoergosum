# Threat intelligence e indicadores: del adversario a la señal

> Recurso troncal: **Getting Started with MITRE ATT&CK**. Tras el mapa ([[cyber-blue1]]) y la ingeniería de detección ([[cyber-blue2]]), aquí entra el **conocimiento del adversario** que prioriza qué detectar. Prepara [[cyber-blue4]] (respuesta a incidentes).

## De qué trata (y qué sabrás hacer al final)

No puedes detectarlo todo; el presupuesto de detección es finito ([[cyber-ms3]]). La **threat intelligence** (inteligencia de amenazas) responde "¿de qué me defiendo **primero**?" estudiando qué adversarios son relevantes para ti y cómo operan. Convierte la defensa de "intentar cubrir las 200 técnicas de ATT&CK" a "cubrir las que mi tipo de organización realmente enfrenta".

La intuición: una clínica y un banco no temen a los mismos ladrones. La inteligencia de amenazas es el estudio de "¿quién querría atacarme, qué busca y cómo suele entrar?", para reforzar las puertas que de verdad usarán, no todas por igual. Es defensa **informada por el adversario**, no genérica.

Al terminar podrás: (1) explicar qué es **threat intelligence** y para qué sirve; (2) distinguir niveles de indicadores por su **valor y durabilidad** (la "pirámide del dolor"); (3) relacionar inteligencia con ATT&CK; y (4) priorizar detección según amenazas relevantes.

## Threat intelligence: defensa informada por el adversario

La inteligencia de amenazas recopila y analiza información sobre **quién** ataca a organizaciones como la tuya, **qué** buscan y **cómo** operan (sus tácticas y técnicas, [[cyber-blue1]]). No es coleccionar listas de "IPs malas"; es entender patrones de comportamiento para anticipar y priorizar. Su producto útil para un defensor: "los actores que atacan a empresas de salud suelen entrar por phishing y buscan exfiltrar datos de pacientes" → refuerza detección de phishing y de exfiltración primero.

## Indicadores y la pirámide del dolor

No todos los indicadores valen igual. La **pirámide del dolor** (Bianco) los ordena por cuánto le **cuesta al atacante** si se los bloqueas:

| Indicador | Ejemplo | Dolor para el atacante |
|---|---|---|
| Hash de archivo | hash de un malware | Trivial: recompila y cambia |
| IP / dominio | servidor del atacante | Fácil: cambia de IP |
| Artefactos de red/host | un patrón de tráfico, una ruta | Molesto |
| Herramientas | el software que usa | Difícil: debe cambiar de herramienta |
| **TTPs** (tácticas, técnicas, procedimientos) | **cómo** opera | **Doloroso**: cambiar su modo de operar |

Moraleja: detectar por **comportamiento (TTPs)** —lo que ATT&CK cataloga— es mucho más valioso que perseguir hashes e IPs, porque obliga al atacante a reinventar su método, no solo a renombrar un archivo. Los IoC de bajo nivel caducan rápido; los de comportamiento perduran.

## Mini-ejemplo trabajado

Tu equipo de datos recibe un "feed" con 5 000 IPs maliciosas y quiere bloquearlas todas. ¿Es la mejor inversión?

- **Análisis con la pirámide:** bloquear IPs es la base de la pirámide: el atacante cambia de IP y vuelve; el feed caduca en días. Esfuerzo alto, dolor bajo.
- **Mejor inversión:** usar inteligencia para saber **qué TTPs** usan los actores que atacan a tu sector (p. ej. phishing → ejecución → exfiltración de buckets de datos) y construir detección de **esas conductas** ([[cyber-blue2]]). Eso obliga al atacante a cambiar su método, no su IP.
- **Rol del feed:** los IoC de bajo nivel sirven como señal complementaria de bajo costo, no como la estrategia central.

## Señales de reconocimiento

| Señal | Diagnóstico |
|---|---|
| "Bloqueemos estas 5 000 IPs y listo" | Defensa en la base de la pirámide (caduca) |
| Detección genérica sin saber qué adversario importa | Falta threat intelligence |
| Foco en hashes de malware | Trivial de evadir; bajo dolor |
| Detección por comportamiento (TTPs) | Alto valor; difícil de evadir |

## Errores típicos

- **Confundir inteligencia con listas de IoC:** los feeds de IPs/hashes son insumo, no estrategia.
- **Intentar cubrir todo ATT&CK por igual:** sin priorizar por amenazas relevantes, diluyes el esfuerzo.
- **Invertir donde el atacante adapta gratis:** bloquear hashes/IPs da sensación de acción con poco efecto.

## Contraejemplo y caso borde

- **Contraejemplo:** un equipo que, sabiendo que su sector sufre exfiltración de datos tras phishing, prioriza detección de phishing y de descargas anómalas (TTPs): pocos controles, alto dolor para el atacante.
- **Caso borde:** la inteligencia puede **sesgarse** hacia las amenazas conocidas/famosas y dejar puntos ciegos en las no reportadas; complementa siempre con detección de anomalías de comportamiento ([[cyber-blue2]]) para lo que la inteligencia no anticipó.

## Transferencia a ciencia de datos e IA

Priorizar por amenazas relevantes es asignación de recursos bajo incertidumbre —tu terreno—. La pirámide del dolor enseña a elegir **features de detección durables** (comportamiento) sobre frágiles (identificadores que cambian), igual que prefieres features estables en un modelo. Y la inteligencia sobre ataques a sistemas de IA vive en **MITRE ATLAS** ([[cyber-ml-security]]), el ATT&CK de la IA.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para una organización ficticia (clínica, fintech), lista 3 amenazas relevantes y la conducta (TTP) que priorizarías detectar.
- **Misión externa (lab vivo):** en **MITRE ATT&CK** (https://attack.mitre.org) explora un "Group" (actor) y mira sus técnicas asociadas. **Criterio de cierre:** explicar por qué detectar sus TTPs es más durable que bloquear sus IPs.
- **Mini-entregable:** una mini "ficha de amenaza" de tu organización: quién podría atacarte, qué busca, por qué TTPs, y qué detectarías primero.

---

> **Síntesis:** como no puedes detectarlo todo, la **threat intelligence** prioriza: estudia qué adversarios y conductas son relevantes para ti, no listas genéricas de IoC. La **pirámide del dolor** ordena los indicadores por lo que le cuesta al atacante evadirlos: hashes e IPs son triviales (caducan), mientras detectar **TTPs** (comportamiento, lo que cataloga ATT&CK) es lo más doloroso y durable. Invierte la detección donde el atacante no pueda adaptarse gratis.

---

**Referencias**

- Pennington, A. (Ed.), Applebaum, A., Nickels, K., Schulz, T., Strom, B., & Wunder, J. (2019). *Getting started with ATT&CK*. The MITRE Corporation.
- Bianco, D. (2013). *The pyramid of pain*. https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html
- MITRE. (n.d.). *MITRE ATT&CK*. https://attack.mitre.org

*Retrieval: (1) ¿qué es threat intelligence y para qué sirve?; (2) ¿qué ordena la pirámide del dolor?; (3) ¿por qué detectar TTPs supera a bloquear hashes/IPs?; (4) ¿qué riesgo tiene basarse solo en inteligencia de amenazas conocidas?*
