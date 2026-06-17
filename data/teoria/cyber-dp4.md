# Control de acceso, auditoría y ciclo de vida del dato

> Recurso troncal: **NIST Privacy Framework 1.1 (IPD)**. La gobernanza ([[cyber-dp2]]) se vuelve operación: quién toca el dato, cómo se registra y cuándo muere. Sigue a [[cyber-dp3]] (derechos) y prepara [[cyber-dp5]] (privacidad en ML).

## De qué trata (y qué sabrás hacer al final)

Tener buenas políticas de privacidad no sirve si en la práctica cualquiera accede a los datos, nadie sabe quién los tocó, y se conservan para siempre. Esta lección aterriza la gobernanza en tres mecanismos operativos: **control de acceso** (least privilege sobre datos), **auditoría** (registro de accesos) y **ciclo de vida** (retención y borrado). Son los mismos principios de [[cyber-ms2]] aplicados al activo "datos de personas".

La intuición: un archivo de historias clínicas no se protege solo con una cerradura; se protege decidiendo **quién** tiene llave (acceso), llevando un **libro de visitas** (auditoría) y **destruyendo** los expedientes que ya no se necesitan (ciclo de vida). Sin el libro de visitas, una fuga es invisible; sin destrucción, el riesgo se acumula.

Al terminar podrás: (1) aplicar **least privilege** y modelos de acceso a datos; (2) diseñar **auditoría** de accesos útil; (3) gestionar el **ciclo de vida** (retención, minimización en el tiempo, borrado); y (4) ligar todo a la detección ([[cyber-blue1]]).

## Control de acceso a los datos

Least privilege ([[cyber-ms2]]) sobre datos significa: cada persona/servicio accede **solo** a los datos que necesita, con el permiso mínimo (leer vs escribir), por el tiempo necesario. Patrones útiles:

- **Acceso por rol/atributo:** define quién puede ver qué por su función, no caso por caso.
- **Granularidad:** a nivel de columna/fila cuando importa (un analista ve métricas agregadas, no la columna de diagnóstico).
- **Acceso temporal:** que caduca al terminar el proyecto, en vez de permanente.
- **Separación de funciones:** quien administra los datos no necesariamente los analiza.

El error opuesto —"todos al dataset completo por comodidad"— convierte cualquier cuenta comprometida o insider ([[cyber-ms4]]) en una fuga total.

## Auditoría: el libro de visitas

Auditoría es registrar **quién accedió a qué, cuándo y para qué**. Sin ella, una fuga por insider o por credencial robada es **invisible** y no se puede investigar. Una auditoría útil:

- Registra accesos a datos sensibles (no solo logins).
- Es **inalterable** por quien podría querer borrar su rastro (integridad del log).
- Alimenta la **detección** ([[cyber-blue1]]): "esta cuenta descargó 10× lo habitual" es una alerta sobre el log de acceso.

La auditoría es a la vez control de privacidad (rendición de cuentas), pieza de seguridad (detección) y requisito para cumplir derechos ([[cyber-dp3]]).

## Ciclo de vida: el dato también muere

Recuerda que la retención es un **pasivo** ([[cyber-dp1]]): cada día que conservas un dato sensible es exposición. Gestionar el ciclo de vida:

- **Calendario de retención:** cuánto se conserva cada tipo de dato y por qué.
- **Borrado real y verificable:** al vencer, se elimina —incluidos backups, logs y datasets derivados— y se puede **demostrar**.
- **Minimización en el tiempo:** datos que dejan de ser necesarios se agregan o anonimizan ([[cyber-dp2]]) en vez de guardarse en crudo.

"Guardar todo para siempre" no es prudencia; es deuda de privacidad que crece sola.

## Mini-ejemplo trabajado

Un equipo guarda un dataset de pacientes en un bucket con acceso para todo el equipo, sin logs de acceso y sin política de borrado. Aterrizaje operativo:

- **Acceso:** pasar a roles —analistas con solo lectura sobre columnas no sensibles; acceso a columnas clínicas solo para quien lo justifique, temporal y aprobado—. Least privilege.
- **Auditoría:** activar logs de acceso al bucket (quién descargó qué y cuándo), inalterables, y una alerta por volumen anómalo ([[cyber-blue2]]).
- **Ciclo de vida:** definir retención (p. ej. borrar datos crudos a los N meses, conservar solo agregados), con borrado verificable que alcance backups.
- **Resultado:** una fuga deja de ser invisible y total; se vuelve detectable y acotada.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| Acceso total al dataset "por comodidad" | Una cuenta comprometida = fuga total |
| Sin logs de acceso a datos sensibles | Fuga invisible; sin investigación posible |
| Logs que el propio usuario puede borrar | Auditoría sin integridad |
| Sin calendario de retención | Pasivo de privacidad creciente |
| "Borramos" pero quedan en backups/derivados | Borrado incompleto (incumple derechos) |

## Errores típicos

- **Confundir tener política con tener control:** la política sin permisos, logs ni borrado reales no protege.
- **Auditar logins pero no accesos a datos:** el insider ya inició sesión; lo relevante es qué tocó.
- **"Borrado" que ignora backups y derivados:** el dato sobrevive donde no miraste.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** das acceso por rol granular (solo ciertas columnas), registras de forma inalterable quién accedió a qué, y borras de verdad al vencer la retención (incluidos backups).
- **Contraejemplo:** datos con acceso por rol temporal, logs de acceso inalterables con alerta de anomalías, y retención con borrado verificable: privacidad **operativa**, no solo declarada.
- **Caso borde:** los **logs de auditoría** son ellos mismos datos personales (revelan quién hizo qué) y tienen su propio riesgo de privacidad y retención: hay que protegerlos y no conservarlos eternamente tampoco. Auditar sin convertir el log en un nuevo problema de privacidad es el equilibrio.

## Transferencia a ciencia de datos e IA

El control de acceso por columna/fila es lo que evita que un RAG filtre documentos ajenos ([[cyber-llm-rag-agents]], LLM02); la auditoría de accesos es la materia prima de la detección ([[cyber-blue1]]); y el ciclo de vida choca con modelos que memorizan ([[cyber-ml-security]]) y con el derecho al olvido ([[cyber-dp3]]). Gobernar el dato operativamente es prerequisito de hacer ML responsable.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el dataset de pacientes, define el modelo de acceso por rol, qué se audita y el calendario de retención.
- **Misión externa (lab vivo):** en el **NIST Privacy Framework** (https://www.nist.gov/privacy-framework), recorre *Control-P* y *Govern-P*. **Criterio de cierre:** explicar por qué auditoría y retención son controles de privacidad, no solo de seguridad.
- **Mini-entregable:** una ficha operativa de un dataset: matriz de acceso por rol, qué eventos se auditan, y calendario de retención/borrado.

---

> **Síntesis:** la gobernanza se opera con tres mecanismos: **control de acceso** (least privilege sobre datos: por rol, granular, temporal, con separación de funciones), **auditoría** (registro inalterable de quién accedió a qué —no solo logins— que alimenta la detección y la rendición de cuentas) y **ciclo de vida** (retención con borrado real y verificable, incluidos backups y derivados). Tener política no es tener control; y los propios logs de auditoría son datos a proteger.

---

**Referencias**

- National Institute of Standards and Technology. (2025). *NIST Privacy Framework 1.1: Initial public draft* (NIST CSWP 40 ipd). https://doi.org/10.6028/NIST.CSWP.40.ipd
- National Institute of Standards and Technology. (n.d.). *Privacy Framework*. https://www.nist.gov/privacy-framework

*Retrieval: (1) ¿qué significa least privilege sobre datos?; (2) ¿por qué auditar accesos a datos y no solo logins?; (3) ¿qué hace verificable a un borrado?; (4) ¿por qué los logs de auditoría son a su vez un riesgo de privacidad?*
