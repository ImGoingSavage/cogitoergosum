# Privacidad ≠ seguridad: proteger personas, no solo tablas

> Recurso troncal: **NIST Privacy Framework 1.1 (IPD)**. Donde [[cyber-ms1]] te dio el riesgo de seguridad, esta lección abre el **riesgo de privacidad**, que es distinto. Sigue en [[cyber-dp2]] (reidentificación y gobernanza).

## De qué trata (y qué sabrás hacer al final)

Un científico de datos puede tener un sistema **perfectamente seguro** —cifrado, sin brechas— y aun así **dañar a personas**: recolectando datos que no necesita, usándolos para fines que el usuario no esperaba, o reteniéndolos para siempre. Eso es **riesgo de privacidad**, y es independiente del riesgo de seguridad. Confundirlos es el error fundacional del manejo de datos.

La intuición: la **seguridad** pregunta *"¿puede un atacante acceder a este dato?"*. La **privacidad** pregunta *"¿deberíamos siquiera tener este dato, y lo estamos usando como la persona esperaría?"*. Un hospital puede guardar tus análisis con cifrado militar (seguro) y aun así venderlos a una aseguradora (violación de privacidad). El candado estaba bien; la decisión de qué hacer con la llave, no.

Al terminar podrás: (1) separar **privacidad de seguridad**; (2) definir **riesgo de privacidad** y distinguir **datos personales de sensibles**; (3) aplicar **minimización y limitación de finalidad**; y (4) razonar **retención** como un riesgo, no como un activo.

## Dos riesgos que no son el mismo

| | Seguridad | Privacidad |
|---|---|---|
| Pregunta central | ¿Puede acceder un no autorizado? | ¿Es apropiado tener/usar este dato? |
| Daño típico | Brecha, robo, alteración | Vigilancia, discriminación, vergüenza, pérdida de control |
| Puede fallar aunque... | la privacidad esté bien | la seguridad sea perfecta |
| Marco base | CIA, threat modeling | Minimización, finalidad, transparencia |

El NIST Privacy Framework reconoce dos fuentes de problema: las **brechas de seguridad** (se solapan) **y** el **procesamiento mismo de datos** —recolectar, analizar, compartir— que, aun siendo "seguro" y autorizado, puede dañar. Esa segunda fuente es la que los técnicos suelen ignorar.

## Datos personales y datos sensibles

- **Dato personal:** cualquiera que identifique o pueda identificar a una persona (nombre, email, IP, ID de dispositivo, una combinación de columnas).
- **Dato sensible:** subconjunto cuyo abuso causa daño grave —salud, origen étnico, orientación, religión, geolocalización, biometría, finanzas—. Exige protección y justificación mayores.

Clave para DS: la identificabilidad es **combinatoria**. Código postal + fecha de nacimiento + sexo identifican a una fracción enorme de la población aunque ninguna columna sea "un identificador". (Esto se profundiza en [[cyber-dp2]].)

## Minimización y limitación de finalidad

Dos principios que cambian cómo diseñas un dataset:

- **Minimización:** recolecta y conserva **solo** lo necesario para la finalidad declarada. Cada columna extra es responsabilidad e impacto potencial, no "por si acaso".
- **Limitación de finalidad:** usa el dato **solo** para lo que se recolectó. Reutilizar datos de salud recolectados para "agendar citas" en un modelo de scoring de seguros rompe la expectativa del titular.

Corolario incómodo: a veces la decisión más profesional es **no recolectar** una variable, aunque mejore el modelo. El "más datos es mejor" del ML choca de frente con la privacidad.

## Mini-ejemplo trabajado

Un equipo entrena un modelo para predecir abandono de un curso. Quieren incluir, "porque están disponibles": género, código postal, historial médico declarado y la dirección IP de cada login. Análisis de privacidad:

- **¿Necesario para la finalidad?** El historial médico y el género no tienen justificación clara para predecir abandono → **viólan minimización**; además son **sensibles** y pueden introducir discriminación.
- **¿Finalidad respetada?** El historial médico se dio para otra cosa → **viola limitación de finalidad**.
- **Decisión:** excluir médico y género; el código postal, agregarlo a región amplia si aporta señal; IP solo si hay una razón de seguridad y con retención corta.

Resultado: un dataset más pequeño, más defendible y muchas veces igual de útil. Menos riesgo de privacidad **por diseño**.

## Señales de reconocimiento

| Señal | Bandera de privacidad |
|---|---|
| "Guardemos todo por si acaso" | Viola minimización |
| "Ya que lo tenemos, úsemoslo para X" | Viola limitación de finalidad |
| "Lo anonimizamos quitando el nombre" | Reidentificación probable (ver [[cyber-dp2]]) |
| "Es sensible pero está cifrado" | Cifrado ≠ que sea apropiado tenerlo |
| "Lo guardamos indefinidamente" | Retención = riesgo creciente |

## Errores típicos

- **Equiparar anonimato a "sin nombre":** quitar el identificador directo no anonimiza (ver [[cyber-dp2]]).
- **Tratar la retención como gratis:** cada día que conservas un dato sensible es un día de exposición; la retención es pasivo, no activo.
- **"Privacidad = cumplimiento legal":** la ley es el piso; el riesgo de privacidad existe aunque cumplas la letra.

## Contraejemplo y caso borde

- **Contraejemplo:** una empresa con seguridad impecable que, legalmente y "de forma segura", combina datos de fuentes para perfilar a usuarios sin que lo esperen: cero brechas, gran daño de privacidad.
- **Caso borde:** datos **agregados** parecen sin riesgo, pero una estadística sobre un grupo muy pequeño (p. ej. "el único empleado de 60 años en el área X") puede revelar a un individuo. La privacidad no termina en la fila individual.

## Transferencia a ciencia de datos e IA

Minimización y finalidad rigen el **feature engineering** responsable y los datasets de entrenamiento de [[cyber-ml-security]]; los **embeddings** pueden filtrar datos personales del texto original ([[cyber-llm-rag-agents]]); y la comunicación de riesgo de privacidad a un equipo es parte del oficio del DS de producto.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** toma un dataset que conozcas y clasifica cada columna en *no personal / personal / sensible*; marca cuáles eliminarías por minimización.
- **Misión externa (lab vivo):** recorre el **NIST Privacy Framework** (https://www.nist.gov/privacy-framework) y ubica las funciones *Identify-P* y *Control-P*. **Criterio de cierre:** explicar con tus palabras qué es "riesgo de privacidad" según el marco.
- **Mini-entregable:** una política de minimización de media carilla para un dataset: qué se recolecta, para qué, y qué se decidió **no** recolectar.

---

> **Síntesis:** privacidad y seguridad son **riesgos distintos**: la seguridad protege el acceso; la privacidad pregunta si es **apropiado tener y usar** el dato. Se gobierna con **minimización** (solo lo necesario) y **limitación de finalidad** (solo para lo declarado), tratando la **retención** como pasivo. Distingue **personal** de **sensible**, y recuerda que la identificabilidad es **combinatoria**.

---

**Referencias**

- National Institute of Standards and Technology. (2025). *NIST Privacy Framework 1.1: Initial public draft* (NIST CSWP 40 ipd). https://doi.org/10.6028/NIST.CSWP.40.ipd
- National Institute of Standards and Technology. (n.d.). *Privacy Framework*. https://www.nist.gov/privacy-framework

*Retrieval: (1) ¿en qué se diferencian riesgo de seguridad y de privacidad?; (2) define minimización y limitación de finalidad; (3) ¿por qué la retención es un riesgo?; (4) ¿por qué "quitar el nombre" no anonimiza?*
