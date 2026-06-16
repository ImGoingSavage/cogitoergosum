# Defensa en el navegador: HTTPS/HSTS, cookies, CORS y CSP

> Recurso troncal: **PortSwigger Web Security Academy**. El navegador ofrece capas de defensa que casi nadie configura bien. Sigue a [[cyber-web3]] (APIs) y prepara [[cyber-web5]] (archivos, deserialización, config).

## De qué trata (y qué sabrás hacer al final)

Muchos ataques web (robo de sesión, XSS, CSRF) se **mitigan en capas** que viven en el navegador y se activan con unas pocas cabeceras HTTP. Son *defense in depth* ([[cyber-ms2]]) casi gratis: no arreglan el bug de raíz, pero reducen su impacto. El problema es que sus **defaults son inseguros** y hay que configurarlas a conciencia.

La intuición: el navegador es un portero que puede aplicar reglas estrictas —"solo acepto conexiones cifradas", "no dejo que scripts de fuera lean estos datos", "solo cargo código de estos orígenes"— pero solo si **el servidor se las dicta** mediante cabeceras. Sin esas instrucciones, el portero deja pasar casi todo.

Al terminar podrás: (1) configurar **HTTPS/HSTS** y cookies seguras; (2) entender **CORS** (qué permite y qué no); (3) usar **CSP** para mitigar XSS; y (4) reconocer una mala configuración de seguridad del lado navegador.

## HTTPS y HSTS

Ya sabes que TLS protege el tránsito ([[cyber-sys5]]). **HSTS** (`Strict-Transport-Security`) va más allá: indica al navegador "para este dominio, **siempre** usa HTTPS, nunca HTTP", evitando el degradado a `http://` que un atacante de red podría forzar. Junto con redirigir todo a HTTPS, cierra la ventana del primer request inseguro.

## Cookies seguras (repaso aplicado)

Las cookies de sesión ([[cyber-sys3]]) deben llevar:
- `Secure`: solo se envían por HTTPS.
- `HttpOnly`: invisibles a JavaScript → un XSS ([[cyber-web1]]) no puede robarlas.
- `SameSite` (`Lax`/`Strict`): no se envían en peticiones de otros sitios → mitiga **CSRF** ([[cyber-web2]]).

Tres atributos que convierten el robo de sesión de trivial a difícil. Son configuración, no código.

## CORS: lo que permite (y el malentendido común)

**CORS** (Cross-Origin Resource Sharing) decide si un sitio en el origen A puede leer respuestas de tu API en el origen B desde el navegador. Malentendidos peligrosos:

- CORS **no** es un control de acceso a tu API: protege al **usuario** del navegador, no a tus datos del servidor. Un atacante con `curl` ignora CORS por completo; tu autorización del servidor sigue siendo la verdadera defensa.
- Configurar `Access-Control-Allow-Origin: *` **junto con** credenciales, o reflejar cualquier origen, abre tus respuestas autenticadas a sitios maliciosos. Usa una **allow-list** de orígenes confiables.

Regla: CORS es para relajar la política de mismo-origen de forma controlada, no para sustituir la autorización.

## CSP: red de seguridad contra XSS

**CSP** (Content-Security-Policy) le dice al navegador de qué orígenes puede cargar y ejecutar recursos. Una CSP estricta (sin `unsafe-inline`, con orígenes acotados) hace que, **aunque** se cuele un XSS ([[cyber-web1]]), el script inyectado no se ejecute o no pueda exfiltrar a un dominio del atacante. No reemplaza codificar la salida; es la **segunda capa** que limita el daño cuando la primera falla.

## Mini-ejemplo trabajado

Un dashboard de analítica: sirve por HTTP y HTTPS, cookies sin atributos, `Access-Control-Allow-Origin: *` con credenciales, y sin CSP. Endurecimiento:

- **HTTPS/HSTS:** forzar HTTPS y enviar HSTS → no más degradado a HTTP.
- **Cookies:** `Secure`+`HttpOnly`+`SameSite=Lax` → robo por XSS y CSRF mitigados.
- **CORS:** quitar `*` con credenciales; allow-list solo de los orígenes propios del front.
- **CSP:** política que solo permita scripts del propio origen → un XSS inyectado no ejecuta ni exfiltra.
- **Resultado:** sin tocar la lógica, el impacto de varios ataques cae drásticamente. Defense in depth por configuración.

## Señales de reconocimiento

| Señal | Mala configuración |
|---|---|
| Sirve por `http://` o sin HSTS | Degradado a HTTP forzable |
| Cookies sin `Secure`/`HttpOnly`/`SameSite` | Robo de sesión / CSRF |
| `Access-Control-Allow-Origin: *` con credenciales | Respuestas autenticadas expuestas |
| "CORS nos protege la API" | Malentendido: protege al navegador, no al servidor |
| Sin CSP | Sin red de seguridad ante XSS |

## Errores típicos

- **Creer que CORS protege la API:** no; tu autorización del servidor sí. Un cliente no-navegador ignora CORS.
- **Reflejar cualquier origen para "que funcione":** equivale a desactivar la política de mismo-origen.
- **Confiar solo en CSP contra XSS:** es segunda capa; primero codifica la salida ([[cyber-web1]]).

## Contraejemplo y caso borde

- **Contraejemplo:** una app con HTTPS+HSTS, cookies endurecidas, CORS con allow-list y CSP estricta: aunque aparezca un XSS, el navegador limita su ejecución y su exfiltración. Las capas contienen el fallo.
- **Caso borde:** una CSP demasiado laxa (con `unsafe-inline` o comodines) da **falsa** sensación de protección: figura una CSP, pero permite justo lo que debía bloquear. Configurar mal una defensa es casi peor que no tenerla, porque relaja la vigilancia.

## Transferencia a ciencia de datos e IA

Tus dashboards y apps de visualización de datos viven en el navegador y heredan estos controles; un dashboard que renderiza datos de usuarios ([[cyber-web1]], XSS almacenado) se beneficia enormemente de cookies endurecidas + CSP. Y entender que CORS no es autorización evita el error de "abrir" una API de modelo creyendo que CORS la protege ([[cyber-web3]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** escribe las cabeceras (HSTS, set-cookie con atributos, CORS allow-list, CSP) que aplicarías al dashboard del ejemplo.
- **Misión externa (lab vivo):** revisa los labs de **CORS** y **CSP**/XSS en PortSwigger (https://portswigger.net/web-security/all-labs). **Criterio de cierre:** explicar por qué una CORS mal configurada filtra datos y cómo CSP frena un XSS. Practica **solo** en laboratorios autorizados.
- **Mini-entregable:** un set de cabeceras de seguridad recomendado para una app, con una línea de justificación por cabecera.

---

> **Síntesis:** el navegador ofrece **defensa en capas** activable por cabeceras: **HTTPS/HSTS** (no degradar a HTTP), **cookies** `Secure`/`HttpOnly`/`SameSite` (robo de sesión y CSRF), **CORS** con allow-list (relajar el mismo-origen sin abrir tus respuestas) y **CSP** (red de seguridad contra XSS). Sus defaults son inseguros y CORS **no** es autorización: la defensa real del servidor sigue siendo el control de acceso. Una defensa mal configurada da falsa seguridad.

---

**Referencias**

- PortSwigger. (n.d.). *Web Security Academy*. https://portswigger.net/web-security
- OWASP Foundation. (2021). *OWASP Top 10:2021* (A05: Security Misconfiguration). https://owasp.org/Top10/

*Retrieval: (1) ¿qué añade HSTS sobre HTTPS?; (2) ¿qué tres atributos endurecen una cookie y contra qué?; (3) ¿por qué CORS no es control de acceso de la API?; (4) ¿cómo mitiga CSP un XSS y por qué es segunda capa?*
