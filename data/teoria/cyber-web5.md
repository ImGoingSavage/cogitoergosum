# Subida de archivos, deserialización insegura y mala configuración

> Recurso troncal: **PortSwigger Web Security Academy**. Capstone del cluster web: tres vectores que un científico de datos toca a diario (subir archivos, cargar objetos serializados, configurar servicios). Integra [[cyber-web1]]–[[cyber-web4]] y prepara el mini-proyecto del cluster.

## De qué trata (y qué sabrás hacer al final)

Las apps de datos **reciben archivos** (CSVs, imágenes, modelos), **deserializan objetos** (pickle, JSON, YAML) y **configuran servicios** (buckets, bases, paneles admin). Cada uno es una frontera de confianza ([[cyber-sys1]]) donde lo recibido puede volverse ejecución o exposición. Esta lección cierra el cluster con los vectores menos glamurosos pero más frecuentes.

La intuición: aceptar un archivo o un objeto serializado es como aceptar un paquete cerrado de un desconocido y **abrirlo dentro de tu casa**. Si no verificas qué contiene ni dónde lo dejas, el "paquete" puede ser un script que se ejecuta, un archivo que sobrescribe otro, o algo que llena tu disco. La configuración es la cerradura de la casa: dejarla en el default suele ser dejarla abierta.

Al terminar podrás: (1) asegurar **subida de archivos**; (2) explicar por qué la **deserialización insegura** (¡pickle!) ejecuta código; (3) reconocer **mala configuración de seguridad**; y (4) ejecutar el mini-proyecto de auditoría del cluster.

## Subida de archivos: cuándo un archivo se vuelve ataque

Recibir archivos abre varios riesgos:
- **Ejecución:** si el archivo subido se guarda en una ruta servible y el servidor lo ejecuta (un `.php`, `.jsp`), el atacante corre código.
- **XSS almacenado:** un SVG/HTML subido y servido en tu origen ejecuta script ([[cyber-web1]]).
- **Path traversal:** un nombre como `../../config` escribe fuera de la carpeta prevista.
- **Agotamiento:** archivos enormes o "zip bombs" llenan disco/CPU (disponibilidad).

Defensas: validar **tipo real** (no solo la extensión), renombrar con un identificador propio, guardar **fuera de la raíz servible** o en almacenamiento de objetos, limitar tamaño, y servir descargas con cabeceras que eviten ejecución en el navegador.

## Deserialización insegura: el caso `pickle`

Deserializar es reconstruir un objeto desde bytes. El peligro: algunos formatos pueden **ejecutar código** durante la reconstrucción. En el mundo DS esto es crítico: **`pickle` de Python ejecuta código arbitrario al cargar**, así que abrir un `.pkl` (¡o un modelo!) de origen no confiable es ejecutar lo que el atacante puso. Lo mismo aplica a YAML inseguro (`yaml.load` sin `SafeLoader`) y a formatos de modelos que permiten código.

Reglas:
- **Nunca** deserialices datos no confiables con `pickle`; usa formatos de datos puros (JSON, Parquet) o cargadores seguros.
- Para modelos, prefiere formatos sin ejecución (p. ej. safetensors) y **verifica la procedencia/integridad** ([[cyber-sys2]], [[cyber-ml-security]]).

## Mala configuración de seguridad

Es la categoría más común y aburrida, y por eso tan explotada: defaults inseguros, paneles admin expuestos, buckets de almacenamiento públicos, mensajes de error verbosos ([[cyber-secure-dev]]), cabeceras faltantes ([[cyber-web4]]), credenciales por defecto sin cambiar. No requiere un exploit sofisticado: requiere que alguien encuentre la puerta que dejaste abierta. **Fail-safe defaults** ([[cyber-ms2]]) y revisar la configuración como parte del diseño la previenen.

## Mini-ejemplo trabajado

Un portal recibe "datasets" de usuarios: acepta cualquier archivo por su extensión, lo guarda en `/uploads` (servible) con su nombre original, y un job los carga con `pickle.load`. Riesgos del mismo cuento:

- **Subida:** un `.html`/SVG servido desde tu origen → XSS almacenado; un nombre `../` → path traversal.
- **Deserialización:** un `.pkl` malicioso ejecuta código al cargarlo → RCE.
- **Config:** `/uploads` servible y sin límites → ejecución y agotamiento.
- **Arreglo:** validar tipo real + renombrar + guardar fuera de la raíz / en object storage con límites; **no** usar `pickle` sobre archivos de usuarios (CSV/Parquet validados); revisar la config (nada servible que no deba serlo). Mismo patrón de [[cyber-web1]]: lo recibido no es confiable hasta validarse y aislarse.

## Señales de reconocimiento

| Señal | Riesgo |
|---|---|
| Acepta archivos por extensión y los sirve desde el origen | Ejecución / XSS almacenado |
| `pickle.load` / `yaml.load` sobre datos no confiables | Ejecución de código (RCE) |
| Nombre de archivo del usuario usado tal cual | Path traversal |
| Buckets/paneles/credenciales en su default | Mala configuración |
| Sin límite de tamaño de subida | Agotamiento (DoS) |

## Errores típicos

- **Validar la extensión, no el contenido:** `.jpg` puede ser cualquier cosa; valida el tipo real y no confíes en el nombre.
- **`pickle` para intercambiar datos/modelos:** equivale a ejecutar código ajeno; usa formatos sin ejecución.
- **Dejar defaults:** "ya lo configuramos seguro después" deja la puerta abierta hasta entonces.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** recibes un archivo (frontera de confianza): validas el tipo real, lo renombras, lo guardas fuera de la raíz servible y limitas el tamaño; nunca yaml.load inseguro.
- **Contraejemplo:** subidas validadas por tipo real, renombradas, en object storage privado con límites, y datos cargados como Parquet/CSV validados (nunca pickle de terceros): los tres vectores quedan cerrados.
- **Caso borde:** un **modelo** descargado de un repositorio público parece dato inerte, pero según el formato puede ejecutar código al cargarse: es a la vez deserialización insegura **y** supply chain ([[cyber-ml-security]]). "Es solo un modelo" es un supuesto peligroso.

## Transferencia a ciencia de datos e IA

`pickle` y los formatos de modelo con código son el puente directo con la **supply chain de modelos** y el **poisoning** de [[cyber-ml-security]]: cargar un checkpoint no confiable es ejecutar código. La subida de archivos es la puerta de muchos datasets de entrenamiento (vector de **data poisoning**). Y la mala configuración —buckets públicos— es la causa más común de fugas de datasets ([[cyber-data-privacy]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** reescribe el flujo del mini-ejemplo a su versión segura (subida + carga de datos), explicando qué frontera protege cada cambio.
- **Misión externa (lab vivo):** prueba un lab de **file upload** en PortSwigger o explora **OWASP Juice Shop** (https://owasp.org/www-project-juice-shop/). **Criterio de cierre:** describir cómo una subida mal validada lleva a ejecución. Practica **solo** en laboratorios autorizados.
- **Mini-entregable (mini-proyecto del cluster):** una **auditoría defensiva de una API educativa ficticia** (login, sesiones, roles, endpoints privados, dashboards): por endpoint, su vulnerabilidad probable (inyección, XSS, BOLA, sesión, SSRF, subida/deserialización, config), el impacto y la mitigación correcta. Evalúalo con la rúbrica de 5 criterios del cluster.

---

> **Síntesis:** recibir **archivos**, **deserializar objetos** y **configurar servicios** son fronteras de confianza cotidianas. Asegura subidas validando el **tipo real**, renombrando, guardando fuera de la raíz servible y con límites; **nunca** uses `pickle`/`yaml.load` inseguro sobre datos no confiables (ejecutan código —¡también los modelos!—); y trata la **mala configuración** (defaults, buckets públicos, paneles expuestos) como el riesgo frecuente que es, con **fail-safe defaults**. Lo recibido no es confiable hasta validarse y aislarse.

---

**Referencias**

- PortSwigger. (n.d.). *Web Security Academy*. https://portswigger.net/web-security
- OWASP Foundation. (2021). *OWASP Top 10:2021* (A05 Security Misconfiguration, A08 Software and Data Integrity Failures). https://owasp.org/Top10/
- OWASP Foundation. (n.d.). *OWASP Juice Shop*. https://owasp.org/www-project-juice-shop/

*Retrieval: (1) ¿cuándo un archivo subido se vuelve ataque y cómo se mitiga?; (2) ¿por qué `pickle` sobre datos no confiables es RCE?; (3) ¿por qué un modelo descargado puede ser deserialización insegura?; (4) ¿qué es mala configuración y cómo se previene?*
