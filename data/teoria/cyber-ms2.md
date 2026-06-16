# Diseño defensivo: threat modeling y principios que reducen daño

> Recurso troncal: **Anderson, *Security Engineering* (3.ª ed.)**. Construye sobre el vocabulario de [[cyber-ms1]]: ahora que sabes nombrar el riesgo, aprende a **reducirlo por diseño**.

## De qué trata (y qué sabrás hacer al final)

Tener vocabulario no basta; hay que *decidir*. El diseño defensivo es el arte de gastar el esfuerzo de seguridad donde más rinde, aceptando que **nunca habrá riesgo cero**. La intuición: un banco no intenta volverse infalible —intenta que robarlo cueste más de lo que vale, que un solo error no lo hunda, y que cuando algo falle, falle hacia el lado seguro.

Al terminar podrás: (1) construir un **threat model** simple con cuatro preguntas; (2) aplicar **least privilege, defense in depth y fail-safe defaults**; (3) reconocer el **factor humano** como parte del sistema; y (4) razonar **tradeoffs** y **riesgo residual** sin caer en el "asegurémoslo todo".

## Threat modeling en cuatro preguntas

No necesitas una metodología pesada para empezar. Cuatro preguntas (estilo Shostack) bastan:

1. **¿Qué estamos construyendo?** Un diagrama simple: qué datos fluyen por dónde.
2. **¿Qué puede salir mal?** Por cada flujo y almacén, ¿qué amenaza a su C/I/A?
3. **¿Qué vamos a hacer al respecto?** Un control proporcional por amenaza creíble.
4. **¿Lo hicimos bien?** ¿Quedó riesgo residual aceptable? ¿cómo lo verificamos?

La clave está en la pregunta 2: casi siempre hay **un supuesto de confianza que se rompe**. "Confío en que el archivo que subo es una imagen" se rompe cuando subo un script. Cazar ese supuesto roto es el corazón del threat modeling.

## Principios de diseño que rinden

| Principio | Idea | Ejemplo en datos |
|---|---|---|
| **Least privilege** | Cada parte recibe el mínimo permiso necesario | La key de lectura del dashboard no puede escribir |
| **Defense in depth** | Varias capas: si una falla, otra contiene | Red privada + auth + cifrado del dato |
| **Fail-safe defaults** | Ante la duda, **negar** | Endpoint nuevo cerrado por defecto, no abierto |
| **Separation of duties** | Nadie tiene todo el poder solo | Quien entrena no despliega a producción sin revisión |
| **Economía de mecanismo** | Lo simple se audita; lo complejo esconde fallos | Una regla clara > diez excepciones |

## El factor humano y la economía de la seguridad

Anderson insiste en algo que los técnicos olvidan: **los sistemas fallan donde los incentivos y las personas se cruzan**. Un control que es tan molesto que la gente lo evade (post-its con contraseñas, claves compartidas por chat) reduce la seguridad real aunque se vea robusto en el papel. La pregunta no es "¿es seguro?" sino "¿es seguro *y* alguien lo va a usar así en la práctica?".

Y todo control tiene **costo**: dinero, fricción, latencia, mantenimiento. Seguridad es **economía**: inviertes donde el riesgo (probabilidad × impacto) lo justifica. Por eso no existe "asegurarlo todo": existe asignar bien un presupuesto finito.

## Mini-ejemplo trabajado

Diseñas el acceso a un dataset sensible para un equipo de 10 analistas.

- **Opción A (cómoda):** una sola cuenta compartida con permiso total. Falla least privilege, separation of duties y trazabilidad: si algo se filtra, no sabes quién fue.
- **Opción B (defensiva):** cada analista con su cuenta; permiso de **solo lectura** sobre las columnas que necesita; el acceso caduca al terminar el proyecto; cada consulta queda en un log.
- **Tradeoff explícito:** B cuesta más de montar y administrar. ¿Lo vale? Si el activo son datos de personas, el impacto de una fuga justifica el costo. Ese juicio —no la paranoia— es el diseño.
- **Riesgo residual:** aun con B, un analista autorizado podría copiar lo que ve. Lo *aceptas* conscientemente y lo monitoreas; no finges que desapareció.

## Señales de reconocimiento

| Señal | Jugada defensiva |
|---|---|
| "Demos acceso total, ya lo afinamos" | Empieza cerrado (fail-safe) y abre lo justo |
| "Con el firewall basta" | Una sola capa = punto único de fallo → defense in depth |
| "La gente igual se salta la regla" | Rediseña el control para que el camino fácil sea el seguro |
| "Asegurémoslo todo" | No hay presupuesto infinito: prioriza por riesgo |

## Errores típicos

- **Seguridad por capas decorativas:** muchas medidas que protegen lo mismo y ninguna lo que importa.
- **Ignorar el riesgo residual:** creer que un control lo elimina en vez de reducirlo; deja de monitorear y se sorprende.
- **Diseñar contra el usuario:** controles tan rígidos que la gente los burla, empeorando la postura real.

## Contraejemplo y caso borde

- **Contraejemplo:** abrir un puerto "temporalmente" para una demo y dejarlo abierto. El default dejó de ser fail-safe sin que nadie lo decidiera.
- **Caso borde:** least privilege llevado al absurdo puede paralizar el trabajo (permisos tan finos que nadie puede hacer nada). El principio se balancea con usabilidad: mínimo **necesario**, no mínimo absoluto.

## Transferencia a ciencia de datos e IA

Estos principios son el esqueleto de los clusters siguientes: least privilege reaparece en credenciales de [[cyber-secure-dev]] y en la **agencia mínima** de agentes LLM en [[cyber-llm-rag-agents]]; defense in depth estructura la detección de [[cyber-blue-team]]; el threat model de cuatro preguntas es el mismo que aplicarás a un pipeline ML en [[cyber-ml-security]].

## Práctica, misión externa y mini-entregable

- **Práctica interna:** toma el sistema de [[cyber-ms1]] y responde las 4 preguntas del threat model; marca cuál supuesto de confianza es el más frágil.
- **Misión externa (lab vivo):** en el **NIST CSF** (https://www.nist.gov/cyberframework), ubica las funciones *Detect, Respond, Recover*. **Criterio de cierre:** explicar por qué proteger no basta sin detectar y responder.
- **Mini-entregable:** un threat model de una carilla (diagrama simple + 3 amenazas + su control + riesgo residual aceptado).

---

> **Síntesis:** el diseño defensivo asigna esfuerzo finito donde el riesgo lo justifica. Se modela con cuatro preguntas (qué construyes, qué falla, qué haces, lo hiciste bien) cazando el **supuesto de confianza roto**, y se apoya en **least privilege, defense in depth y fail-safe defaults**, sin olvidar el **factor humano** ni negar el **riesgo residual**.

---

**Referencias**

- Anderson, R. (2020). *Security engineering: A guide to building dependable distributed systems* (3rd ed.). Wiley.
- Shostack, A. (2014). *Threat modeling: Designing for security*. Wiley.
- National Institute of Standards and Technology. (2018). *Framework for improving critical infrastructure cybersecurity* (v1.1). https://www.nist.gov/cyberframework

*Retrieval: (1) las 4 preguntas del threat model; (2) define least privilege, defense in depth y fail-safe defaults; (3) ¿por qué un control que la gente evade reduce la seguridad?; (4) ¿qué es riesgo residual?*
