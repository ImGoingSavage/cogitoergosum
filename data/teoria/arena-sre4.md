# Robustez en producción: releases, simplicidad, sobrecarga y cascada

## Ingeniería de releases

Cuatro principios: **autoservicio** (cada equipo controla su release, automatizado), **alta velocidad** (lanzar frecuente → menos cambios entre versiones → testing/troubleshooting más fáciles; *Push on Green* despliega todo build que pasa los tests), **builds herméticos** (insensibles a lo instalado en la máquina: mismas fuentes + revisión → resultado **idéntico y reproducible**; versiona también las herramientas) y **enforcement de políticas** (control de acceso, revisión de código). **Rama desde mainline + cherry-pick** de los fixes → se sabe el contenido exacto de cada release sin arrastrar cambios no relacionados.

## Simplicidad: "la virtud de lo aburrido"

En software, **aburrido es bueno**: las sorpresas en producción son la némesis de SRE. Distingue complejidad **esencial** (inherente al problema) de la **accidental** (resoluble con ingeniería) y empuja contra la accidental.

- **Cada línea de código es un pasivo:** borra el código muerto (no lo comentes ni lo dejes tras un flag desactivado — bomba de tiempo, cf. Knight Capital); celebra las **"líneas negativas"**.
- **APIs mínimas** ("perfección = no queda nada que quitar") y **modularidad** (bajo acoplamiento → arreglar/desplegar un componente aislado; versiona las APIs). Evita binarios "misc/util".
- **Releases simples** (lotes pequeños): es más fácil medir el impacto de un cambio que de 100 a la vez.

## Prevenir la sobrecarga

Estrategias en orden de prioridad: (1) **probar la capacidad límite y el modo de fallo** bajo sobrecarga; (2) servir **resultados degradados**; (3) instrumentar el servidor para **rechazar pronto y barato** (load shedding, p.ej. HTTP **503** si hay demasiadas peticiones en vuelo); (4) **rate-limiting** en proxies/balanceadores; (5) **planificación de capacidad** (p.ej. **N+2**).

- **Cola corta** (rechaza pronto); considera **LIFO/CoDel** para descartar peticiones viejas que el usuario ya abandonó; propaga **deadlines de RPC**.
- **Degradación elegante:** reducir cantidad/calidad del trabajo (buscar solo en la caché en memoria, ranking más barato). Ejercítala regularmente (*el camino de código que nunca usas no funciona*), monitorea cuántos servidores entran en modo degradado y mantenla simple.

## Evitar fallos en cascada

La causa #1 es la **sobrecarga**: si el clúster B cae, su tráfico va a A (1.000 → 1.200 QPS), A no aguanta, agota recursos y su éxito cae por debajo de 1.000; el balanceador propaga la carga a otros clústeres → fallo global en minutos. El **agotamiento de recursos** degrada/crashea (CPU: colas largas, deadlines perdidos; memoria: **GC death spiral**). Los **reintentos naïf amplifican**: cada fallo multiplica las RPC justo cuando ya hay sobrecarga → limita reintentos, **backoff exponencial con jitter**, presupuestos de reintento y deadlines propagados. **Degrada antes de colapsar.**

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| Builds que dan resultados distintos | Builds herméticos + versiona herramientas |
| Quiero lanzar seguro y rápido | Push on Green; lotes pequeños; cherry-pick |
| Complejidad que no es del problema | Es accidental → elimínala; borra código muerto |
| Servidor que se cae al saturarse | Load shedding (rechaza pronto, 503) + degradar |
| Un clúster cae y tumba a los demás | Sobrecarga→cascada: limita reintentos, capacidad N+2 |
| Reintentos que empeoran todo | Backoff+jitter+límite+deadlines de RPC |

---

> **Síntesis:** Lanza con **autoservicio, alta velocidad, builds herméticos y políticas** (rama + cherry-pick). Persigue la **simplicidad** ("aburrido es bueno"; ataca la complejidad accidental, cada línea es un pasivo, APIs mínimas, lotes pequeños). Y diseña contra la **sobrecarga**: **rechaza pronto** (load shedding), **degrada** la calidad antes de colapsar, y evita la **cascada** limitando reintentos (backoff+jitter+deadline) y planificando capacidad **N+2**.

---

*Retrieval: (1) ¿qué es un build hermético y para qué el cherry-pick?; (2) complejidad esencial vs accidental y "líneas negativas"; (3) load shedding vs degradación elegante; (4) ¿cómo la sobrecarga y los reintentos producen una cascada y cómo se mitiga?*
