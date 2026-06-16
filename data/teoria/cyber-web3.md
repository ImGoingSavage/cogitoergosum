# Seguridad de APIs: BOLA, mass assignment, rate limiting y el OWASP Top 10 como mapa

> Recurso troncal: **PortSwigger Web Security Academy** + OWASP API Security Top 10. Las apps de datos exponen su valor por **APIs**; esta lección las audita. Sigue a [[cyber-web2]] (auth/acceso) y prepara [[cyber-web4]] (cabeceras).

## De qué trata (y qué sabrás hacer al final)

Tu modelo, tu dashboard y tu pipeline hablan con el mundo por una **API**. Las APIs concentran hoy la mayoría de las brechas porque exponen lógica y datos directamente, sin la "interfaz" que esconde detalles. La buena noticia: el OWASP Top 10 (web y API) no es una lista que memorizar, sino un **mapa** de categorías de riesgo con el que puedes leer cualquier endpoint.

La intuición: una API es como una ventanilla de banco sin vidrio ni guardia visible: cada operación que ofrece es una puerta directa. Si una puerta no verifica quién eres y qué te corresponde, alguien la cruza. La seguridad de APIs es, sobre todo, **control de acceso por objeto** hecho bien, a escala.

Al terminar podrás: (1) usar el OWASP Top 10 como **mapa de categorías**; (2) reconocer **BOLA/IDOR** como el riesgo #1 de APIs; (3) detectar **mass assignment**; y (4) aplicar **rate limiting** y límites de recursos.

## El OWASP Top 10 como mapa, no como lista

OWASP publica un Top 10 de riesgos (web y, aparte, API). No los memorices uno a uno: úsalos como **ejes para interrogar** un sistema. Las grandes familias:

- **Control de acceso roto** (la #1): ¿cada operación verifica permiso por objeto?
- **Inyección** ([[cyber-web1]]): ¿alguna entrada cruza a instrucción?
- **Fallos de autenticación/sesión** ([[cyber-web2]], [[cyber-sys3]]).
- **Mala configuración de seguridad**: defaults inseguros, cabeceras faltantes ([[cyber-web4]]).
- **Exposición de datos sensibles**: devolver de más, sin minimizar ([[cyber-data-privacy]]).

El mapa convierte "¿es segura mi API?" en preguntas concretas por categoría.

## BOLA / IDOR: el rey de los bugs de API

**BOLA** (Broken Object Level Authorization) es el IDOR de [[cyber-web2]] a escala de API: el endpoint sirve un objeto identificado por un id sin verificar que pertenece al solicitante. `GET /api/orders/1001` devuelve la orden 1001; cambias a `1002` y ves la de otro. Es el riesgo #1 de APIs porque cada endpoint con un id es un candidato, y la verificación debe repetirse **en cada uno**, en el servidor, derivando la identidad de la sesión/token, no del parámetro.

## Mass assignment: campos que no debías poder tocar

Muchos frameworks "enlazan" automáticamente el JSON entrante a los campos de un objeto. Si el cliente envía `{"nombre":"Ana","rol":"admin"}` y el servidor asigna **todo** a ciegas, el usuario se autopromovió a admin. Eso es **mass assignment**: aceptar campos que el cliente no debería poder establecer. Defensa: **allow-list** explícita de campos editables (nunca enlazar el objeto entero), separando lo que el cliente puede cambiar de lo que decide el servidor.

## Rate limiting y límites de recursos

Una API sin límites permite fuerza bruta de credenciales ([[cyber-sys3]]), scraping masivo de datos, extracción de modelos ([[cyber-ml-security]]) y denegación de servicio por agotamiento. **Rate limiting** (cuántas peticiones por tiempo y por cliente), **paginación obligatoria** y **límites de tamaño** son controles baratos de alto impacto. Conecta con el **consumo no acotado** (LLM10) de [[cyber-llm-rag-agents]].

## Mini-ejemplo trabajado

Una API de una plataforma educativa: `GET /api/students/{id}/grades` y `PATCH /api/students/{id}`. Auditoría con el mapa:

- **BOLA:** ¿`/students/1001/grades` verifica que el solicitante es ese alumno (o su docente)? Si confía en el `id`, cualquiera lee notas ajenas → derivar permiso de la sesión.
- **Mass assignment:** el `PATCH` enlaza el JSON al objeto alumno; un alumno envía `{"role":"teacher"}` y escala. → allow-list: solo `nombre`, `email` editables por el alumno.
- **Sin rate limit:** se pueden enumerar todos los `id` y descargar la base. → rate limiting + paginación.
- **Exposición:** ¿el endpoint devuelve más campos de los necesarios (p. ej. datos de contacto del tutor)? → minimizar la respuesta ([[cyber-data-privacy]]).

## Señales de reconocimiento

| Señal | Riesgo de API |
|---|---|
| Endpoint con `{id}` que no checa dueño | BOLA / control de acceso roto |
| El JSON entrante se enlaza al objeto completo | Mass assignment |
| Sin límite de peticiones ni paginación | Fuerza bruta, scraping, DoS |
| La respuesta trae campos de más | Exposición de datos sensibles |
| Endpoints internos/admin accesibles | Mala configuración / acceso roto |

## Errores típicos

- **Verificar acceso solo en la UI:** la API se llama directo; el control vive en el servidor por endpoint.
- **Enlazar el objeto entero al input:** abre mass assignment; usa allow-list de campos.
- **Asumir que "nadie conoce el endpoint":** la oscuridad no es control; los endpoints se descubren.

## Contraejemplo y caso borde

- **Contraejemplo:** una API donde cada endpoint deriva el usuario del token, autoriza por objeto, usa allow-list de campos y aplica rate limiting: BOLA y mass assignment quedan cerrados por diseño.
- **Caso borde:** **GraphQL** y endpoints de búsqueda complejos amplían la superficie: una sola consulta puede pedir muchos objetos anidados, multiplicando los puntos donde falta autorización y facilitando consultas costosas (DoS). Requieren control de acceso por campo y límites de complejidad.

## Transferencia a ciencia de datos e IA

Tus APIs de inferencia y de datos son exactamente este terreno: BOLA = servir predicciones/registros de otro usuario; rate limiting = frenar **model extraction** ([[cyber-ml-security]]) y consumo no acotado de LLMs ([[cyber-llm-rag-agents]]); minimizar la respuesta = no filtrar datos sensibles ([[cyber-data-privacy]]). El mapa OWASP es tu checklist al exponer cualquier endpoint.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** audita el mini-ejemplo y escribe la verificación de acceso y la allow-list de campos correctas.
- **Misión externa (lab vivo):** haz un laboratorio de **access control** o **API** en PortSwigger (https://portswigger.net/web-security/all-labs). **Criterio de cierre:** resolver un lab de BOLA/access control y explicar la verificación faltante. Practica **solo** en laboratorios autorizados.
- **Mini-entregable:** tabla "endpoint → quién puede → cómo se verifica → límites" para 5 endpoints de una API que diseñes.

---

> **Síntesis:** las APIs concentran el riesgo porque exponen datos y lógica directamente. El OWASP Top 10 es un **mapa** de categorías para interrogar cada endpoint; la #1 es **control de acceso roto / BOLA** (verifica permiso por objeto en el servidor, derivando la identidad del token). Cierra **mass assignment** con allow-list de campos y aplica **rate limiting/paginación/límites** contra fuerza bruta, scraping, extracción y DoS.

---

**Referencias**

- PortSwigger. (n.d.). *Web Security Academy*. https://portswigger.net/web-security
- OWASP Foundation. (2023). *OWASP API Security Top 10*. https://owasp.org/API-Security/
- OWASP Foundation. (2021). *OWASP Top 10:2021*. https://owasp.org/Top10/

*Retrieval: (1) ¿cómo se usa el OWASP Top 10 como mapa?; (2) ¿qué es BOLA y por qué es el riesgo #1 de APIs?; (3) ¿qué es mass assignment y su defensa?; (4) ¿qué ataques frena el rate limiting?*
