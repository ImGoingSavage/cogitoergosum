# Eliminar toil, monitoreo y las cuatro señales doradas

## Toil

**Toil** = trabajo ligado a operar el servicio que es **manual, repetitivo, automatizable, táctico** (interrupt-driven), **sin valor perdurable** y que escala **O(n)** con el servicio. *No* es "trabajo que no me gusta", ni **overhead** (reuniones, RR.HH., snippets), ni el grunt work que deja una mejora permanente (eso es ingeniería).

- SRE limita el toil a **<50%** del tiempo de cada ingeniero; el otro ≥50% es **ingeniería** (mejoras permanentes que reducen toil futuro) → la organización escala de forma **sublineal**.
- Sin control, el toil **crece hasta el 100%** y SRE degenera en Ops. En Google el promedio real ronda el 33%; la mayor fuente son las **interrupciones**.
- **Ingeniería** = trabajo novedoso, con juicio humano, mejora permanente, guiado por estrategia (software y sistemas).

## Monitoreo: las cuatro señales doradas

Si solo puedes medir cuatro métricas de un sistema de cara al usuario:

- **Latencia** — tiempo de respuesta. Separa éxito de error: un error 500 puede ser rápido (mezclarlo engaña), pero un **error lento es peor que uno rápido** → mide la latencia de error.
- **Tráfico** — demanda (web: req/s; streaming: sesiones; key-value: transacciones/s).
- **Errores** — tasa de fallos: explícitos (500), implícitos (200 con contenido erróneo) o por política (>1 s = error).
- **Saturación** — cuán "lleno" está el recurso más limitado. Muchos sistemas **se degradan antes del 100%** → ten un objetivo de utilización; el **p99** es un indicador temprano y predice saturación inminente ("el disco se llena en 4 h").

## Síntomas vs causas; black-box vs white-box

- **Alerta por SÍNTOMAS**, no por causas: solo preocúpate de causas muy definidas e inminentes.
- **Black-box** (orientado a síntomas, problema activo "no funciona ahora") fuerza molestar a un humano solo ante daño real; **white-box** (logs/endpoints internos) detecta problemas **inminentes** y enmascarados por reintentos.
- En sistemas multicapa, **el síntoma de uno es la causa de otro** (BD lenta = síntoma para el SRE de BD, causa para el de frontend). Distinguir **"qué" (síntoma) de "por qué" (causa)** es clave.

**Buena página:** urgente, **accionable**, requiere **inteligencia** (si basta respuesta robótica, no es página) y sobre un problema **novedoso**. Mide con **histogramas** de latencia (cubos exponenciales), no la media. Mantén el monitoreo **simple**: quita reglas y señales que casi nunca se usan.

---

## Mini-ejemplo trabajado: por qué el toil tiende al 100%

Un SRE dedica hoy el **60%** de su tiempo a toil (reinicios manuales, tickets repetitivos). Como queda solo el 40% para ingeniería, *no alcanza* a automatizar lo suficiente; mientras tanto el servicio crece y el toil escala **O(n)** con él. Resultado: el toil sube al 70%, luego 80%… hasta el **100%**, y SRE degenera en Ops puro. El cap del **<50%** no es burocracia: es lo que garantiza que siempre quede tiempo de ingeniería para reducir el toil *futuro*, de modo que la organización escale **sublinealmente** (más servicio sin más gente).

**Predicción antes de seguir:** un error 500 que tarda 50 ms y otro que tarda 5 s. Si mides "latencia" mezclando éxitos y errores, ¿qué pierdes? Pierdes que un **error lento es peor que uno rápido**; por eso se separa la latencia de éxito de la de error (una de las cuatro señales doradas).

## Prototipo, contraejemplo y caso borde

- **Prototipo (alerta por síntoma):** black-box que avisa "los usuarios ven errores ahora" → molesta a un humano solo ante daño real.
- **Contraejemplo (toil mal etiquetado):** llamar "toil" a las reuniones o al grunt work que deja una mejora permanente — eso es overhead o ingeniería, no toil.
- **Caso borde (saturación < 100%):** un sistema que se degrada al 80% de utilización; el p99 sube *antes* de saturar → indicador temprano ("el disco se llena en 4 h").

## Errores típicos

- **Conceptual:** confundir toil ("manual/repetitivo/O(n)/sin valor perdurable") con "trabajo que no me gusta".
- **De monitoreo:** alertar por **causas** internas en vez de **síntomas** visibles → páginas que no son accionables.
- **De medición:** reportar la **media** de latencia en vez de un **histograma**/p99, ocultando la cola.

## Transferencia isomorfa

- **Cuatro señales doradas ↔ SLOs de serving de ML:** latencia/tráfico/errores/saturación son exactamente las señales genéricas que también vigilas en un modelo en producción (conecta con [[arena-rml1]], las tres capas de SLO).
- **Cap de toil <50% ↔ presupuestar deuda/automatización:** reservar capacidad para ingeniería es el mismo principio que pagar deuda técnica antes de que se componga (conecta con [[arena-htd4]]).
- **p99 como early-warning ↔ pensar en la cola:** la saturación que asoma en el p99 antes que en la media es la misma lección de no fiarse del promedio (conecta con [[arena-sre1]]).

Moraleja de la arista: *limita el toil para que la ingeniería no muera, y vigila pocas señales (latencia/tráfico/errores/saturación) por síntoma y por percentil, no por causa ni por media.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Tarea manual, repetitiva, O(n), sin valor | Es toil → automatízala o redíseñala (cap <50%) |
| "¿Qué monitoreo si solo puedo medir 4 cosas?" | Latencia, tráfico, errores, saturación |
| Pager que suena por causas internas | Alerta por síntomas visibles (black-box) |
| Necesito diagnosticar la causa raíz | White-box (logs/métricas internas) |
| Mi media de latencia se ve bien | Histograma/p99: vigila la cola |

---

> **Síntesis:** Distingue **toil** (manual/repetitivo/automatizable/táctico/sin valor/O(n)) de la **ingeniería**, y limítalo a **<50%** para escalar sublinealmente. Monitorea con las **cuatro señales doradas** (latencia, tráfico, errores, saturación), **alerta por síntomas** (black-box) y usa **white-box** para diagnosticar. Cada página debe ser urgente, accionable, inteligente y novedosa.

---

*Retrieval: (1) ¿qué es toil y qué NO lo es?; (2) ¿por qué el cap del 50%?; (3) nombra las cuatro señales doradas y por qué separar latencia de éxito y error; (4) black-box vs white-box.*
