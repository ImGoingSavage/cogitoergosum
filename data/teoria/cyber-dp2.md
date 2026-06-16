# Reidentificación, anonimización y gobernanza de datos

> Recurso troncal: **NIST Privacy Framework 1.1 (IPD)**. Profundiza [[cyber-dp1]]: aquí atacamos el mito de la "anonimización fácil" y construimos gobernanza real de datasets.

## De qué trata (y qué sabrás hacer al final)

El reflejo más común al "anonimizar" es **borrar la columna de nombre**. Es también el más peligroso, porque produce una falsa sensación de seguridad: el dataset *parece* anónimo y se comparte con confianza, pero un atacante con datos auxiliares puede **reidentificar** a las personas. Esta lección te enseña por qué, y qué se hace de verdad.

La intuición: imagina que tachas el nombre de una ficha pero dejas "mujer, nacida el 3/7/1989, código postal 06700, diagnóstico X". Cualquiera con un padrón público puede cruzar esos cuasi-identificadores y ponerte el nombre de vuelta. El anonimato no es quitar *el* identificador; es asegurar que **ninguna combinación** señale a un individuo.

Al terminar podrás: (1) explicar la **reidentificación por cuasi-identificadores**; (2) distinguir **seudonimización de anonimización**; (3) nombrar técnicas reales (k-anonimato, agregación, *differential privacy* como idea); y (4) diseñar **gobernanza** de un dataset (acceso, auditoría, retención).

## Por qué la reidentificación funciona

Los **identificadores directos** (nombre, DNI, email) se quitan fácil. El problema son los **cuasi-identificadores**: atributos que por separado no identifican, pero combinados sí. Estudios clásicos mostraron que **código postal + fecha de nacimiento + sexo** identifican de forma única a una gran fracción de la población. Sumar datos auxiliares públicos (padrones, redes sociales, otra filtración) hace el resto. Por eso datasets "anonimizados" famosos fueron reidentificados.

Regla mental: **anonimización no es una operación sobre una columna, es una propiedad del dataset frente a un atacante con información externa.**

## Seudonimización vs anonimización

| | Seudonimización | Anonimización |
|---|---|---|
| Qué hace | Reemplaza identificadores por un seudónimo/clave | Elimina la posibilidad de reidentificar |
| ¿Reversible? | Sí, con la tabla/llave de mapeo | No (si se hizo bien) |
| Estatus legal típico | Sigue siendo dato personal | Deja de serlo (si es real) |
| Ejemplo | `user_842` con tabla aparte | Datos agregados o con DP |

Confundirlas es caro: tratar datos **seudonimizados** como si fueran anónimos (y compartirlos libremente) es una fuga, porque la reidentificación está a una tabla de distancia.

## Técnicas reales (panorama)

- **Supresión y generalización:** quitar columnas o reducir resolución (edad → rango, código postal → región). Base del **k-anonimato**: que cada combinación de cuasi-identificadores se comparta con al menos *k−1* personas más.
- **Agregación:** publicar conteos/promedios en vez de filas, cuidando los grupos pequeños (ver caso borde de [[cyber-dp1]]).
- **Differential privacy (idea):** añadir ruido calibrado de modo que la salida casi no cambie esté o no una persona en los datos; ofrece una **garantía cuantificable** de privacidad, a costa de algo de exactitud. No necesitas implementarla hoy, pero sí saber que existe y que es el estándar moderno.

Ninguna es mágica: todas implican un **tradeoff utilidad↔privacidad** que se decide explícitamente.

## Gobernanza de datasets

La técnica sin proceso no basta. Gobernar un dataset es responder, por escrito:

- **Acceso:** ¿quién puede verlo, con qué permiso mínimo, y cómo se concede/revoca? (least privilege, [[cyber-ms2]]).
- **Auditoría:** ¿queda registro de quién accedió y para qué? (lo necesitará [[cyber-blue-team]]).
- **Retención:** ¿cuándo se borra? Un calendario de borrado, no "para siempre".
- **Procedencia y finalidad:** ¿de dónde vino, con qué consentimiento, para qué se permite usarlo?

## Mini-ejemplo trabajado

Un investigador quiere compartir un dataset hospitalario "anonimizado": quitó nombre y DNI, dejó fecha exacta de nacimiento, código postal y diagnóstico. ¿Es anónimo? **No**: los tres cuasi-identificadores reidentifican a muchos pacientes cruzando con un padrón. Plan de remediación: generalizar fecha → año o rango, código postal → región (buscando k-anonimato con k razonable), revisar diagnósticos raros (un diagnóstico único en una región identifica solo), y compartir bajo **acuerdo de uso** con acceso y auditoría. Si el objetivo es publicar estadísticas, mejor **agregar** o aplicar **DP** en vez de liberar microdatos.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| "Quitamos el nombre, ya es anónimo" | Reidentificación por cuasi-identificadores |
| Fecha de nacimiento exacta + ubicación fina | Combinación altamente identificante |
| Estadística sobre un grupo de 1-2 personas | Revela al individuo |
| Dataset "anónimo" compartido sin acuerdo | Seudonimización tratada como anonimización |
| Sin calendario de retención | Exposición indefinida |

## Errores típicos

- **Anonimización por borrado de columna:** ignora cuasi-identificadores y datos auxiliares.
- **Olvidar al atacante externo:** evaluar privacidad solo "dentro" del dataset, sin pensar en lo que existe afuera.
- **Gobernanza implícita:** "todos sabemos quién puede usarlo" — sin acceso, auditoría ni retención escritos, no hay gobernanza.

## Contraejemplo y caso borde

- **Contraejemplo:** un dataset con DP bien aplicada que sigue siendo útil para estadística agregada y resiste reidentificación: privacidad fuerte **con** utilidad, el ideal.
- **Caso borde:** **outliers** —el paciente con una enfermedad rarísima, el cliente con un patrón único de compra— son casi siempre reidentificables aunque el resto del dataset cumpla k-anonimato. Requieren tratamiento especial (supresión o agregación más agresiva).

## Transferencia a ciencia de datos e IA

Un **modelo** puede memorizar y filtrar datos de entrenamiento (membership inference, [[cyber-ml-security]]); los **embeddings** de un RAG pueden permitir reconstruir el texto fuente ([[cyber-llm-rag-agents]]). Por eso la pregunta "¿quién podría reidentificar a alguien con esto?" no termina en el CSV: sigue en el modelo y en sus salidas.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el dataset hospitalario del ejemplo, propón las generalizaciones concretas que aplicarías para acercarte a k-anonimato.
- **Misión externa (lab vivo):** en el **NIST Privacy Framework** (https://www.nist.gov/privacy-framework) localiza guías de *de-identification*. **Criterio de cierre:** explicar por qué la de-identificación es un espectro, no un sí/no.
- **Mini-entregable:** una ficha de gobernanza de un dataset (acceso · auditoría · retención · finalidad/procedencia · técnica de de-identificación).

---

> **Síntesis:** "quitar el nombre" no anonimiza: los **cuasi-identificadores** + datos auxiliares **reidentifican**. Distingue **seudonimización** (reversible, sigue siendo dato personal) de **anonimización** (irreversible). Las técnicas reales —generalización/k-anonimato, agregación, **differential privacy**— implican un **tradeoff utilidad↔privacidad** explícito, y nada sustituye la **gobernanza** (acceso, auditoría, retención, procedencia).

---

**Referencias**

- National Institute of Standards and Technology. (2025). *NIST Privacy Framework 1.1: Initial public draft* (NIST CSWP 40 ipd). https://doi.org/10.6028/NIST.CSWP.40.ipd
- Sweeney, L. (2002). k-anonymity: A model for protecting privacy. *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, 10*(5), 557–570.
- National Institute of Standards and Technology. (n.d.). *Privacy Framework*. https://www.nist.gov/privacy-framework

*Retrieval: (1) ¿qué son cuasi-identificadores y por qué importan?; (2) seudonimización vs anonimización; (3) ¿qué garantiza differential privacy?; (4) ¿qué 4 cosas definen la gobernanza de un dataset?*
