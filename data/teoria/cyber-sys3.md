# Autenticación y gestión de identidad: contraseñas, MFA, tokens y sesiones

> Recurso troncal: **UC Berkeley CS 161 — *Computer Security***. Fundamentos de "¿eres quien dices?", base de la web ([[cyber-web2]]). Sigue a [[cyber-sys2]] (cripto) y prepara [[cyber-sys4]] (aislamiento).

## De qué trata (y qué sabrás hacer al final)

La autenticación es la puerta de entrada de casi todo sistema, y por eso el blanco favorito. Sus fallos rara vez son matemáticos: son de **diseño** (cómo se guardan las credenciales, cómo se prueban, cuánto dura una sesión, qué pasa si se roba un token). Entender los fundamentos te deja construir o auditar logins sin reinventar errores conocidos.

La intuición: autenticarse es demostrar una de tres cosas — **algo que sabes** (contraseña), **algo que tienes** (un teléfono, una llave) o **algo que eres** (huella, rostro). Cada factor falla distinto; combinarlos (MFA) es como pedir dos pruebas independientes en vez de una, de modo que robar una sola no basta.

Al terminar podrás: (1) razonar los **tres factores** y por qué **MFA** ayuda; (2) explicar cómo se guardan y prueban contraseñas; (3) entender **tokens y sesiones** y su robo; y (4) reconocer fallos comunes de autenticación.

## Los tres factores y por qué MFA

| Factor | Ejemplo | Cómo falla solo |
|---|---|---|
| Algo que **sabes** | contraseña, PIN | se adivina, se reutiliza, se filtra, se phishea |
| Algo que **tienes** | teléfono (TOTP), llave de seguridad | se pierde/roba; SMS es interceptable |
| Algo que **eres** | huella, rostro | no se puede "cambiar" si se compromete |

**MFA** combina dos factores **independientes**: aunque te roben la contraseña, sin el segundo factor no entran. Es de los controles de mayor impacto por su costo. No todos los segundos factores son iguales: una llave de seguridad/“passkey” resiste phishing mejor que un código por SMS.

## Cómo se guardan y prueban las contraseñas

Recordatorio de [[cyber-sys2]]: las contraseñas **no se cifran**, se guardan como **hash lento y salado** (bcrypt, Argon2). El *salt* (valor único por usuario) evita que dos personas con la misma contraseña tengan el mismo hash y frustra tablas precomputadas; la *lentitud* del hash encarece la fuerza bruta. Al iniciar sesión, el servidor hashea lo ingresado y compara con el almacenado: nunca guarda ni recupera la contraseña en claro.

Defensas complementarias: límite de intentos (rate limiting) contra fuerza bruta, y rechazar contraseñas conocidas por filtraciones.

## Tokens y sesiones: quien los roba, es tú

Tras autenticarte, el servidor emite un **identificador de sesión** (cookie) o un **token** (p. ej. JWT, [[cyber-web2]]) que acompaña tus siguientes peticiones. Ese token **es** tu identidad ante el servidor: quien lo roba te suplanta sin saber tu contraseña. Por eso:

- Cookies con `HttpOnly` (no accesibles a JS → mitiga robo por XSS), `Secure` (solo HTTPS) y `SameSite` (mitiga CSRF).
- **Expiración** y posibilidad de **revocar** sesiones (cerrar sesión de verdad invalida el token).
- No incrustar secretos ni datos sensibles en el token (un JWT es legible).

## Mini-ejemplo trabajado

Un servicio guarda contraseñas con SHA-256 simple, sin salt, sin límite de intentos, y sus cookies de sesión no caducan ni tienen `HttpOnly`. Auditoría:

- **Almacenamiento:** SHA-256 es rápido y sin salt → fuerza bruta y tablas precomputadas triviales. Corrección: bcrypt/Argon2 con salt.
- **Sin rate limit:** permite probar millones de contraseñas. Corrección: límite de intentos + bloqueo temporal.
- **Cookie sin `HttpOnly`:** un XSS ([[cyber-web1]]) roba la sesión. Corrección: `HttpOnly`+`Secure`+`SameSite`.
- **Sin expiración:** un token robado vale para siempre. Corrección: expiración + revocación.
- **Recomendación transversal:** ofrecer **MFA**, el mayor salto de seguridad por el costo.

## Señales de reconocimiento

| Señal | Fallo de autenticación |
|---|---|
| Contraseñas con hash rápido o sin salt | Fuerza bruta / tablas precomputadas |
| Sin límite de intentos | Fuerza bruta en línea |
| Cookie de sesión sin HttpOnly/Secure/SameSite | Robo por XSS/CSRF |
| Sesiones que nunca caducan ni se revocan | Token robado = acceso permanente |
| Solo contraseña en datos sensibles | Falta MFA |

## Errores típicos

- **Cifrar contraseñas en vez de hashearlas:** reversible = robable ([[cyber-sys2]]).
- **Confiar en SMS como segundo factor fuerte:** mejor que nada, pero interceptable; preferir TOTP/llaves.
- **Olvidar la revocación:** "cerrar sesión" que no invalida el token deja la puerta abierta.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** proteges el login con MFA (dos factores independientes) + hash lento y salado + rate limiting, y tratas el token de sesión como una identidad que, robada, te suplanta.
- **Contraejemplo:** un login con Argon2 + salt, rate limiting, MFA por llave de seguridad y sesiones con expiración y revocación: robar la contraseña ya no basta y un token tiene vida corta. Defensa en profundidad sobre la identidad.
- **Caso borde:** la **recuperación de cuenta** ("olvidé mi contraseña") suele ser el eslabón débil: si el reset se hace por un correo comprometido o preguntas adivinables, evita todo lo anterior. La autenticación es tan fuerte como su camino de recuperación.

## Transferencia a ciencia de datos e IA

Tus dashboards, notebooks compartidos y APIs de modelo necesitan autenticación robusta y sesiones bien gestionadas ([[cyber-web2]]); las API keys de servicios y de modelos son "tokens" cuyo robo suplanta tu identidad ([[cyber-secure-dev]]); y el rate limiting que frena la fuerza bruta es el mismo que limita el abuso de un endpoint de inferencia ([[cyber-ml-security]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** audita el mini-ejemplo y escribe la versión corregida de cada fallo.
- **Misión externa (lab vivo):** en **OverTheWire: Bandit** (https://overthewire.org/wargames/bandit/) practica el manejo de credenciales/llaves entre niveles. **Criterio de cierre:** explicar por qué una credencial filtrada en un archivo compromete el siguiente paso. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable:** un checklist de autenticación para una app (almacenamiento de contraseñas, rate limit, MFA, cookies, expiración/revocación, recuperación).

---

> **Síntesis:** la autenticación combina **factores** (algo que sabes/tienes/eres); **MFA** exige dos independientes y es de altísimo valor. Las contraseñas se guardan con **hash lento y salado**, con **rate limiting**; tras el login, **tokens/sesiones** son tu identidad —protégelos (`HttpOnly`/`Secure`/`SameSite`, expiración, revocación)— porque quien los roba te suplanta. Cuida también el camino de **recuperación de cuenta**, el eslabón débil habitual.

---

**Referencias**

- Wagner, D., Weaver, N., Kao, P., Shakir, F., Law, A., & Ngai, N. (2024). *Computer security* (CS 161). University of California, Berkeley.
- OverTheWire. (n.d.). *Bandit wargame*. https://overthewire.org/wargames/bandit/

*Retrieval: (1) ¿cuáles son los tres factores y por qué MFA ayuda?; (2) ¿cómo se guardan contraseñas y por qué con salt y lentas?; (3) ¿por qué un token robado suplanta sin la contraseña?; (4) ¿por qué la recuperación de cuenta es un eslabón débil?*
