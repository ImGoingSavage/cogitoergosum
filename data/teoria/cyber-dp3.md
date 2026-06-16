# Consentimiento, transparencia y derechos del titular

> Recurso troncal: **NIST Privacy Framework 1.1 (IPD)**. Tras separar privacidad de seguridad ([[cyber-dp1]]) y atacar la reidentificación ([[cyber-dp2]]), aquí entra la **relación con la persona**: por qué tiene datos, qué se le dijo y qué puede exigir. Prepara [[cyber-dp4]] (acceso/gobernanza).

## De qué trata (y qué sabrás hacer al final)

La privacidad no es solo técnica ni solo de seguridad: es una **relación de confianza** con la persona cuyos datos usas. Esa relación se gobierna con **transparencia** (¿sabe la persona qué haces con sus datos?), **base/legitimidad** del tratamiento (¿por qué puedes tenerlos?) y **derechos** que puede ejercer (acceder, corregir, borrar, oponerse). Un sistema seguro que trata a las personas como meros "registros" sigue fallando en privacidad.

La intuición: imagina que prestas tu diario a alguien "para una cosa". Si lo fotocopia, lo comparte y lo usa para otra cosa sin avisarte, y encima no te deja recuperarlo, te sentirías traicionado aunque nunca lo "robaran". La privacidad es respetar la expectativa con la que la persona te confió sus datos.

Al terminar podrás: (1) explicar **transparencia** y **consentimiento** y sus límites; (2) ligar el tratamiento a una **finalidad legítima**; (3) nombrar los **derechos del titular** y su impacto en el diseño; y (4) reconocer **dark patterns** de consentimiento.

## Transparencia: la persona debe poder entender

Transparencia es que la persona pueda saber, en términos comprensibles, **qué datos** tomas, **para qué**, con **quién** los compartes y **cuánto** los conservas. No es enterrar todo en 40 páginas de "términos". El NIST Privacy Framework trata la comunicación clara como un control: si la gente no entiende qué pasa con sus datos, no hay confianza informada. Para un equipo de datos, esto se traduce en documentar el propósito real de cada recolección.

## Consentimiento y sus límites

El **consentimiento** es una de las bases para tratar datos, pero no la única ni una varita mágica:

- Debe ser **informado, específico y libre**: "acepto todo o no uso el servicio" no es libre.
- El consentimiento para una finalidad **no** habilita otras (limitación de finalidad, [[cyber-dp1]]).
- Es **revocable**: la persona puede retirarlo, y tu sistema debe poder respetarlo.
- A veces el tratamiento se justifica por otra base (un contrato, una obligación legal) y forzar "consentimiento" donde no aplica es teatro.

Diseñar para consentimiento real cambia la arquitectura: necesitas registrar **a qué** consintió cada persona y poder **revertirlo**.

## Derechos del titular y su impacto en el diseño

Las personas suelen poder ejercer derechos sobre sus datos: **acceder** (qué tienes de mí), **rectificar** (corregir), **suprimir/borrar** ("derecho al olvido"), **oponerse** o limitar un uso, y **portabilidad**. Esto **no** es solo legal: impone requisitos técnicos.

- Borrar de verdad exige saber **dónde** vive cada dato de una persona (incluidos backups, logs, datasets derivados, y modelos que lo memorizaron — [[cyber-ml-security]]).
- Acceder exige poder **localizar y exportar** los datos de un individuo.

Si no diseñaste para esto, cumplir un derecho se vuelve imposible o carísimo. La privacidad por diseño anticipa estos derechos.

## Mini-ejemplo trabajado

Una app educativa pide al registrarse aceptar una casilla pre-marcada que autoriza "usar tus datos para mejorar el servicio y compartirlos con socios". Más tarde, un usuario pide borrar su cuenta. Análisis:

- **Consentimiento defectuoso:** casilla pre-marcada y propósito vago/agrupado ("mejorar + compartir con socios") → no es libre ni específico (es un **dark pattern**).
- **Finalidad:** "compartir con socios" excede lo que el usuario espera al registrarse → viola limitación de finalidad.
- **Derecho de borrado:** ¿pueden borrar de verdad? Si los datos ya viajaron a "socios", a backups y a un modelo entrenado, el borrado es incompleto salvo que se haya diseñado para rastrearlo.
- **Rediseño:** consentimientos separados y opt-in real por finalidad, registro de a qué consintió cada quien, y un proceso de borrado que alcance derivados y backups.

## Señales de reconocimiento

| Señal | Problema |
|---|---|
| Casillas pre-marcadas / "acepta todo o vete" | Consentimiento no libre (dark pattern) |
| Un solo consentimiento global para muchos fines | No específico; viola finalidad |
| "Mejorar el servicio" como cajón de sastre | Propósito vago, no transparente |
| No se puede localizar/borrar los datos de una persona | Diseño que ignora los derechos |
| Términos de 40 páginas ilegibles | Falsa transparencia |

## Errores típicos

- **Tratar el consentimiento como casilla única:** debe ser específico, informado y revocable.
- **Confundir transparencia con un documento legal largo:** transparencia es que se **entienda**.
- **No diseñar para el borrado/acceso:** descubrir al recibir la solicitud que no sabes dónde están los datos.

## Contraejemplo y caso borde

- **Contraejemplo:** registro con opt-in separado por finalidad, lenguaje claro, y un sistema que sabe dónde vive cada dato y puede exportarlo/borrarlo: cumplir un derecho es una operación, no una crisis.
- **Caso borde:** el **derecho al olvido vs un modelo entrenado**: borrar la fila no borra lo que el modelo memorizó ([[cyber-ml-security]], membership inference). Cumplir el borrado puede exigir reentrenar o aplicar técnicas de *machine unlearning*; es un problema abierto que debes anticipar, no ignorar.

## Transferencia a ciencia de datos e IA

Limitación de finalidad y consentimiento gobiernan qué datos puedes meter a un modelo y para qué ([[cyber-ml-security]]); el derecho al borrado choca con la memorización de modelos y embeddings ([[cyber-dp2]], [[cyber-llm-rag-agents]]); y la transparencia es parte de la **IA responsable**. Diseñar el pipeline para rastrear procedencia y consentimiento por dato es lo que hace estos derechos cumplibles.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** rediseña el flujo de consentimiento del mini-ejemplo (opt-in por finalidad, lenguaje claro, registro y revocación).
- **Misión externa (lab vivo):** en el **NIST Privacy Framework** (https://www.nist.gov/privacy-framework), ubica las funciones *Communicate-P* y *Control-P*. **Criterio de cierre:** explicar por qué la transparencia es un control de privacidad.
- **Mini-entregable:** un mapa de "ciclo de derechos" para una persona: dónde viven sus datos y cómo cumplirías acceso, rectificación y borrado.

---

> **Síntesis:** la privacidad es una **relación de confianza** con la persona: **transparencia** (que entienda qué haces), **consentimiento** informado/específico/libre/revocable (cuando es la base aplicable, no un cajón de sastre) y **derechos** (acceder, rectificar, borrar, oponerse). Esos derechos imponen requisitos técnicos —saber **dónde** vive cada dato para localizarlo o borrarlo, incluidos backups, derivados y modelos—, así que la privacidad por diseño los anticipa. Evita los **dark patterns** de consentimiento.

---

**Referencias**

- National Institute of Standards and Technology. (2025). *NIST Privacy Framework 1.1: Initial public draft* (NIST CSWP 40 ipd). https://doi.org/10.6028/NIST.CSWP.40.ipd
- National Institute of Standards and Technology. (n.d.). *Privacy Framework*. https://www.nist.gov/privacy-framework

*Retrieval: (1) ¿qué hace válido a un consentimiento?; (2) ¿qué es transparencia real vs un documento legal?; (3) nombra 3 derechos del titular y su requisito técnico; (4) ¿por qué el derecho al olvido choca con un modelo entrenado?*
