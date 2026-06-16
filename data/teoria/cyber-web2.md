# Vulnerabilidades web II: autenticación, control de acceso, CSRF y SSRF

> Recurso troncal: **PortSwigger Web Security Academy**. Continúa [[cyber-web1]]: si la inyección es "el dato se vuelve instrucción", aquí el tema es **¿quién eres y qué puedes hacer?** — y cómo los atacantes lo subvierten.

## De qué trata (y qué sabrás hacer al final)

Dos preguntas gobiernan toda app con usuarios: **autenticación** (¿eres quien dices?) y **autorización / control de acceso** (¿puedes hacer *esto*?). La mayoría de las brechas graves no rompen el cifrado: explotan que el servidor **confía** en algo que no debía —un `id` que manda el cliente, una sesión mal protegida, una petición que el navegador hace "por ti"—.

La intuición: la autenticación es la **recepción** que verifica tu identificación; el control de acceso son las **puertas internas** que deciden a qué oficinas entras. Romper la primera es colarte; romper la segunda es entrar con gafete válido a oficinas ajenas. **Broken access control** —la segunda— es la categoría #1 del OWASP Top 10 y la más fácil de introducir sin darte cuenta.

Al terminar podrás: (1) distinguir **autenticación de autorización**; (2) reconocer **broken access control** (incl. IDOR); (3) entender **sesiones, JWT y OAuth** lo suficiente para no romperlos; y (4) explicar **CSRF y SSRF** y su mitigación.

## Autenticación vs autorización

- **Autenticación** establece *identidad* (login: contraseña + idealmente segundo factor). Sus fallos: contraseñas débiles guardadas mal (ver [[cyber-sys2]]), sin límite de intentos, sin MFA.
- **Autorización** decide *permisos* tras autenticarte. Su fallo estrella es **IDOR** (*Insecure Direct Object Reference*): el servidor sirve `GET /factura/42` sin verificar que la factura 42 es **tuya**. Cambias a `43` y ves la de otro.

Regla: **toda** petición a un recurso debe verificar permiso **en el servidor**, en cada llamada. Ocultar el botón en el front no es control de acceso.

## Sesiones, JWT y OAuth, sin romperlos

- **Sesión:** tras el login, el servidor te da un identificador (cookie). Protégelo: cookies `HttpOnly` (no accesibles a JS → mitiga XSS robando sesión), `Secure` (solo HTTPS), `SameSite` (mitiga CSRF), y expiración.
- **JWT:** un token firmado que el servidor verifica sin guardar estado. Fallos típicos: aceptar `alg: none`, no verificar la firma, o meter datos sensibles en el payload (es **legible**, solo va firmado, no cifrado).
- **OAuth:** delega acceso ("entra con Google") sin compartir tu contraseña. Es **autorización delegada**, no mágia de identidad; mal configurado (redirect URIs laxas, scopes excesivos) filtra cuentas.

## CSRF y SSRF: dos confusiones de confianza

- **CSRF** (Cross-Site Request Forgery): un sitio malicioso hace que **tu navegador** envíe una petición a una app donde ya tienes sesión, abusando de que las cookies viajan solas. Defensa: **tokens anti-CSRF** y cookies `SameSite`.
- **SSRF** (Server-Side Request Forgery): engañas al **servidor** para que haga una petición a un destino que tú no alcanzas —típicamente servicios internos o el *endpoint de metadatos* del cloud que entrega credenciales—. Defensa: validar/allow-list los destinos, no reenviar URLs del usuario a ciegas.

La simetría ayuda: en **CSRF** el atacante abusa de la confianza del *servidor en tu navegador*; en **SSRF**, de la confianza de la *red interna en su propio servidor*.

## Mini-ejemplo trabajado

Una API de reportes: `GET /report?user_id=1001` devuelve los datos de ese usuario, y un endpoint `POST /fetch?url=...` que "previsualiza" una URL. Dos fallos: cambiar `user_id` a `1002` devuelve datos ajenos (**IDOR / broken access control**, porque nadie verifica que 1001 es el solicitante); y `url=http://169.254.169.254/...` hace que el servidor consulte el **metadata del cloud** y filtre credenciales (**SSRF**). Arreglo: derivar el usuario **de la sesión**, no del parámetro; y allow-list de destinos para `fetch`.

## Señales de reconocimiento

| Señal | Vulnerabilidad |
|---|---|
| `id`/`user_id`/`account` viene del cliente y se usa sin checar dueño | IDOR / broken access control |
| El control de acceso "es" ocultar el botón en el front | Autorización ausente en el servidor |
| Cookie de sesión sin `HttpOnly`/`SameSite` | Robo por XSS / CSRF |
| El servidor pide una URL que manda el usuario | SSRF |
| JWT con datos sensibles o sin verificar firma | Fuga / suplantación |

## Errores típicos

- **Confundir autenticación con autorización:** "ya inició sesión" no implica "puede ver *este* registro".
- **Control de acceso en el cliente:** todo lo del navegador es manipulable; la decisión vive en el servidor.
- **Reenviar URLs del usuario sin allow-list:** la puerta de entrada clásica a SSRF.

## Contraejemplo y caso borde

- **Contraejemplo:** un JWT "seguro porque está firmado" cuyo payload lleva el rol `admin` en claro y el servidor confía en él sin re-verificar permisos por recurso: firmado ≠ autorizado.
- **Caso borde:** un endpoint **interno** sin autenticación ("solo lo llamamos nosotros") se vuelve crítico si un SSRF lo alcanza desde fuera: la red interna deja de ser una frontera.

## Transferencia a ciencia de datos e IA

Tus APIs de inferencia y tus dashboards de DS necesitan control de acceso por recurso (¿este usuario puede ver *esta* predicción/registro?). El SSRF es central en agentes LLM con herramientas que hacen *fetch* de URLs ([[cyber-llm-rag-agents]]): un agente que sigue una URL no confiable es SSRF asistido por IA. Y la **agencia mínima** de [[cyber-ms2]] es el control de acceso aplicado a lo que un agente puede invocar.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** para el mini-ejemplo, escribe la verificación de acceso correcta (derivar usuario de la sesión) y la allow-list de `fetch`.
- **Misión externa (lab vivo):** monta **OWASP Juice Shop** (https://owasp.org/www-project-juice-shop/) o usa los labs de *access control* de PortSwigger; resuelve un reto de **broken access control**. **Criterio de cierre:** explicar qué verificación faltaba en el servidor. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable:** una tabla "endpoint → quién debe poder → cómo se verifica" para 5 endpoints de una API que imagines.

---

> **Síntesis:** distingue **autenticación** (quién eres) de **autorización** (qué puedes); el fallo #1 es **broken access control / IDOR**, y se previene verificando permiso **por recurso en el servidor** derivando la identidad de la **sesión**, no del cliente. Protege sesiones (`HttpOnly`/`Secure`/`SameSite`), no confíes ciegamente en JWT, y recuerda: **CSRF** abusa de tu navegador, **SSRF** abusa de tu servidor.

---

**Referencias**

- PortSwigger. (n.d.). *Web Security Academy*. https://portswigger.net/web-security
- OWASP Foundation. (2021). *OWASP Top 10:2021*. https://owasp.org/Top10/
- OWASP Foundation. (n.d.). *OWASP Juice Shop*. https://owasp.org/www-project-juice-shop/

*Retrieval: (1) autenticación vs autorización; (2) ¿qué es IDOR y cómo se previene?; (3) diferencia CSRF de SSRF por "de quién se abusa la confianza"; (4) ¿por qué firmar un JWT no basta para autorizar?*
