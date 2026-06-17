# Desarrollo seguro: requisitos, validación y manejo de secretos

> Recurso troncal: **OpenSSF / Wheeler, *Secure Software Development Fundamentals***. Lleva los principios de [[cyber-ms2]] al código que tú escribes. Sigue en [[cyber-dev2]] (dependencias y supply chain).

## De qué trata (y qué sabrás hacer al final)

La seguridad no se "añade al final"; se decide en cada línea. Para un científico de datos esto es urgente: notebooks, scripts de ETL y APIs de modelo manejan **secretos** y **entradas no confiables** todo el tiempo, y el accidente más común de toda la industria —filtrar una credencial— ocurre en *tu* terreno.

La intuición: programar de forma segura es como cocinar en una cocina profesional. No "desinfectas al final"; tienes higiene **en el proceso**: ingredientes verificados (validación de entradas), cuchillos guardados con cuidado (secretos fuera del código), y no anuncias por el micrófono la combinación de la caja fuerte (no loguear datos sensibles).

Al terminar podrás: (1) tratar la seguridad como **requisito**, no como extra; (2) aplicar **validación de entradas y manejo de errores** sin filtrar información; (3) **gestionar secretos** correctamente; y (4) reconocer **leakage por logs**.

## Seguridad como requisito y diseño

Antes de codificar, pregunta qué propiedades debe cumplir el software: ¿qué entradas son no confiables? ¿qué datos no deben salir nunca en un error o log? ¿qué permisos mínimos necesita cada componente? Definir esto **es** un requisito, igual que la funcionalidad. Reaparecen los principios de [[cyber-ms2]]: least privilege en cada credencial, fail-safe defaults en cada configuración nueva.

## Validación de entradas (en el servidor, siempre)

Toda entrada externa es hostil hasta validarse (ver [[cyber-sys1]]). Validar = aceptar **solo** lo que cumple una forma esperada (allow-list), no intentar bloquear lo malo (deny-list, frágil):

```python
# Débil (deny-list): intenta adivinar todo lo peligroso
if "DROP" in q or "<script>" in q: rechazar()
# Robusto (allow-list): define lo válido y rechaza el resto
if not re.fullmatch(r"[A-Za-z0-9 _-]{1,50}", nombre): rechazar()
```

La validación complementa —no sustituye— a parametrizar consultas y codificar salidas ([[cyber-web1]]).

## Manejo de errores sin filtrar

Un error mal manejado es una fuga de información: un *stack trace* en producción revela rutas, versiones, consultas y a veces secretos, regalando el mapa al atacante. Regla: **mensajes genéricos al usuario, detalle solo en logs internos** —y esos logs sin datos sensibles—. Falla **hacia el lado seguro**: ante un error de autorización, niega; no "continúes por si acaso".

## Gestión de secretos

El accidente clásico: la API key pegada en el notebook o en el código que termina en GitHub. Una vez en el historial de git, **asume que está comprometida** aunque la borres después. Prácticas correctas:

- **Fuera del código:** secretos en variables de entorno o en un *secret manager*, nunca en el fuente ni en el notebook.
- **`.gitignore` + escaneo:** ignora `.env`; usa un escáner de secretos en el repo/CI.
- **Rotación y permiso mínimo:** si una key se filtra, rótala; dale a cada key el alcance más estrecho posible.
- **Nunca en logs ni en mensajes de error.**

## Mini-ejemplo trabajado: code review de un script de ETL

```python
import requests
API_KEY = "sk-live-9f8a7..."          # (1)
def fetch(user_input):
    url = "https://api.x.com/q?d=" + user_input   # (2)
    r = requests.get(url, headers={"Authorization": API_KEY})
    print("DEBUG payload:", r.text)     # (3)
    return r.json()
```

Hallazgos: **(1)** secreto hardcodeado → muévelo a variable de entorno y rótalo (ya está comprometido si esto se subió). **(2)** entrada del usuario concatenada en una URL → valida/encódala; potencial SSRF/inyección ([[cyber-web2]]). **(3)** `print` del payload completo → **leakage por logs** de posibles datos sensibles; loguea metadatos, no contenido. Tres bugs, los tres del día a día de un DS.

## Señales de reconocimiento

| Señal en el código | Problema |
|---|---|
| `API_KEY = "..."` en el fuente/notebook | Secreto hardcodeado |
| `print`/`logger.info` de payloads o PII | Leakage por logs |
| `except: pass` o stack trace al usuario | Manejo de errores inseguro |
| Validación con deny-list de "palabras malas" | Frágil; usa allow-list |
| Una sola key con permisos totales | Viola least privilege |

## Errores típicos

- **"Lo borro del repo y listo":** el secreto vive en el historial de git; hay que **rotarlo**.
- **Loguear para depurar y olvidarlo:** los `print` de depuración filtran datos en producción.
- **Validar en el cliente nada más:** la validación de seguridad es del servidor.

## Prototipo, contraejemplo y caso borde

- **Prototipo:** validas un campo de entrada con allow-list en el servidor y mueves la API key del código a un secret store con permiso mínimo, ignorada en git y rotada si se filtra.
- **Contraejemplo:** un `.env` correctamente ignorado… que alguien sube una vez "por error" y luego borra: sigue en la historia. El control (gitignore) existía, pero el secreto ya se filtró → rotación obligatoria.
- **Caso borde:** un mensaje de error **útil** para el usuario que sin querer revela si un email existe ("usuario no encontrado" vs "contraseña incorrecta") filtra cuentas válidas: incluso errores "amables" pueden ser fugas (enumeración).

## Transferencia a ciencia de datos e IA

El manejo de secretos y la validación de entradas son la base del **pipeline ML seguro** de [[cyber-ml-security]] y del *mini-proyecto* del cluster; el leakage por logs es un vector directo de fuga de **datos personales** ([[cyber-data-privacy]]); y la validación de entradas no confiables es justo lo que falta cuando un agente LLM procesa contenido externo ([[cyber-llm-rag-agents]]).

## Práctica, misión externa y mini-entregable

- **Práctica interna:** reescribe el script del mini-ejemplo a su versión segura (secreto en env, entrada validada, log sin contenido sensible).
- **Misión externa (lab vivo):** explora un curso de **OpenSSF Training** (https://openssf.org/training/courses/), p. ej. *Secure Software Development Fundamentals*, módulo de input validation o secrets. **Criterio de cierre:** resumir una práctica nueva que adoptarás.
- **Mini-entregable:** un checklist personal de manejo de secretos para tus repos (5–7 ítems accionables).

---

> **Síntesis:** la seguridad es un **requisito de diseño**, no un parche final. Valida entradas con **allow-list en el servidor**, maneja errores **sin filtrar** (genérico al usuario, detalle interno, fail-safe), y trata los **secretos** con cuidado quirúrgico: fuera del código, ignorados en git, con permiso mínimo y **rotados si se filtran**. El **leakage por logs** es una fuga silenciosa y cotidiana.

---

**Referencias**

- Wheeler, D. A. (n.d.). *Developing secure software (LFD121): Secure software development fundamentals*. Open Source Security Foundation. https://openssf.org/training/courses/

*Retrieval: (1) allow-list vs deny-list en validación; (2) ¿por qué borrar un secreto del repo no basta?; (3) ¿qué es leakage por logs?; (4) ¿cómo se debe fallar ante un error de autorización?*
