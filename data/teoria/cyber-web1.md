# Vulnerabilidades web I: inyección, XSS y la frontera del servidor

> Recurso troncal: **PortSwigger Web Security Academy**. Aplica las fronteras de confianza de [[cyber-sys1]] al mundo web. Sigue en [[cyber-web2]] (auth, acceso, CSRF/SSRF).

## De qué trata (y qué sabrás hacer al final)

Casi toda app de datos tiene una cara web: un dashboard, una API, un formulario. Y casi toda vulnerabilidad web nace del **mismo pecado**: el servidor trató una entrada del usuario como si fuera confiable —como **código** o como **consulta**— en lugar de como **dato sospechoso**. Si entiendes ese patrón único, el OWASP Top 10 deja de ser una lista que memorizar y se vuelve variaciones de un tema.

La intuición: imagina un cajero que ejecuta *al pie de la letra* todo lo que el cliente escribe en el formulario de "concepto". Si el cliente escribe "págale $0 a la cuenta X y bórrate el registro", y el cajero lo *ejecuta* en vez de *tratarlo como texto*, ese es el bug. Inyección y XSS son exactamente eso: entrada que cruza de "dato" a "instrucción".

Al terminar podrás: (1) explicar **SQL injection** y **XSS** como el mismo patrón; (2) distinguir **validar vs sanear vs parametrizar**; (3) ubicar la **frontera de confianza del servidor**; y (4) elegir la mitigación correcta en vez de un parche frágil.

## Inyección (SQLi): cuando el dato se vuelve consulta

Si construyes una consulta pegando texto del usuario:

```python
# VULNERABLE
q = "SELECT * FROM users WHERE name = '" + nombre + "'"
```

y el usuario escribe `' OR '1'='1`, la consulta cambia de *significado* y devuelve toda la tabla. El dato se convirtió en lógica. La defensa **no** es "filtrar comillas" (frágil, se evade); es **consultas parametrizadas** (prepared statements), que mandan el dato y la estructura por canales separados:

```python
# SEGURO
cur.execute("SELECT * FROM users WHERE name = %s", (nombre,))
```

El driver garantiza que `nombre` jamás se interprete como SQL. El mismo principio gobierna inyección de comandos del SO, de NoSQL y de LDAP: **separa instrucción de dato**.

## XSS: cuando el dato se vuelve código en el navegador

Si tu dashboard inserta texto del usuario directamente en el HTML:

```js
// VULNERABLE
el.innerHTML = "Hola, " + nombreUsuario;
```

y el "nombre" es `<script>roba(document.cookie)</script>`, el navegador lo **ejecuta** en la sesión de quien lo vea. Eso es **XSS**: el dato cruzó a código en el cliente, y puede robar cookies de sesión (ver [[cyber-sys1]]), suplantar al usuario o alterar la página. La defensa: **codificar la salida** según el contexto (HTML, atributo, JS) y, en frameworks, usar `textContent`/binding seguro en vez de `innerHTML`. (Esta misma app sigue esa regla: todo texto de lección se **escapa antes de transformar**.)

## Validar, sanear, parametrizar, codificar

| Acción | Qué hace | Dónde |
|---|---|---|
| **Validar** | Rechazar lo que no cumple forma esperada (un email es un email) | En la entrada |
| **Parametrizar** | Separar dato de instrucción (SQL) | Al consultar |
| **Codificar/escapar** | Neutralizar el significado especial en el contexto de salida | En la salida |
| **Sanear** | Quitar/transformar partes peligrosas (último recurso, frágil) | Cuando no hay alternativa |

La jerarquía importa: **parametrizar y codificar** vencen; **sanear con listas negras** casi siempre se evade.

## Mini-ejemplo trabajado

Un endpoint de búsqueda de pacientes: el front manda `?q=texto`, el back arma `... WHERE nombre LIKE '%{q}%'` y pinta los resultados con `innerHTML`. Dos bugs del **mismo patrón**: `q = '; DROP TABLE pacientes;--` es SQLi (dato→consulta); un nombre guardado como `<img onerror=...>` es XSS almacenado (dato→código al renderizar). Arreglo: **parametrizar** la consulta y **codificar** la salida. No hace falta "detectar hackers": basta dejar de confundir dato con instrucción.

## Señales de reconocimiento

| Señal en el código | Vulnerabilidad probable |
|---|---|
| Concatenar strings para armar SQL | SQL injection |
| `innerHTML` / `dangerouslySetInnerHTML` con datos de usuario | XSS |
| `os.system(f"... {entrada}")` | Inyección de comandos |
| "Filtramos las comillas/`<script>`" | Defensa por lista negra → evadible |

## Errores típicos

- **Confiar en la validación del cliente:** el JavaScript del navegador se salta con una petición directa; la frontera real es el **servidor**.
- **Lista negra en vez de parametrizar/codificar:** bloquear `<script>` deja pasar `<img onerror>`, `onmouseover`, etc.
- **"Es un campo interno":** entradas internas también pueden ser maliciosas (un usuario autenticado abusando).

## Contraejemplo y caso borde

- **Contraejemplo:** un ORM no te salva si usas `raw()` concatenando strings: la herramienta segura, usada inseguramente, vuelve a ser vulnerable.
- **Caso borde:** **XSS almacenado** es peor que el reflejado: el payload vive en tu base de datos y se dispara para *cada* visitante; un dataset "de texto libre" que luego renderizas es un vector silencioso.

## Transferencia a ciencia de datos e IA

El patrón "dato tratado como instrucción" es **exactamente** el de **prompt injection** en LLMs ([[cyber-llm-rag-agents]]): el texto recuperado por un RAG cruza de dato a instrucción igual que `' OR '1'='1` cruza a SQL. Quien entiende SQLi entiende prompt injection. Además, todo dashboard de DS que renderiza datos de usuarios es un candidato a XSS almacenado.

## Práctica, misión externa y mini-entregable

- **Práctica interna:** reescribe los dos snippets vulnerables de arriba a su versión segura y explica qué frontera protege cada cambio.
- **Misión externa (lab vivo):** haz el laboratorio introductorio de **SQL injection** en PortSwigger (https://portswigger.net/web-security/all-labs). **Criterio de cierre:** resolver un lab "apprentice" y poder explicar por qué la parametrización lo habría prevenido. Practica **solo** en estos laboratorios autorizados.
- **Mini-entregable:** media carilla "el mismo patrón en SQLi y XSS", con un ejemplo de cada uno y su defensa correcta.

---

> **Síntesis:** inyección y XSS son la **misma falla**: una entrada del usuario cruzó de **dato** a **instrucción** (consulta SQL o código en el navegador). La defensa robusta es **parametrizar** (SQL) y **codificar la salida** (XSS), no sanear con listas negras. La frontera de confianza real está en el **servidor**, nunca en el cliente.

---

**Referencias**

- PortSwigger. (n.d.). *Web Security Academy*. https://portswigger.net/web-security
- OWASP Foundation. (2021). *OWASP Top 10:2021*. https://owasp.org/Top10/

*Retrieval: (1) ¿qué patrón comparten SQLi y XSS?; (2) ¿por qué parametrizar vence a filtrar comillas?; (3) ¿dónde está la frontera de confianza real?; (4) ¿por qué el XSS almacenado es peor que el reflejado?*
