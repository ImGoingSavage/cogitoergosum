# Bloques distribuidos fundamentales

## Rate limiter — controlar el caudal de peticiones

Limita cuántas peticiones puede hacer un cliente en una ventana de tiempo. Beneficios: frena ataques DoS, reduce costo, evita sobrecarga. Devuelve **HTTP 429 (Too Many Requests)**; cabeceras útiles: `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, `Retry-After`.

| Algoritmo | Idea | Pro | Contra |
|-----------|------|-----|--------|
| **Token bucket** | Bucket se rellena a tasa fija; cada petición consume un token | Permite ráfagas controladas; simple | Dos parámetros que afinar |
| **Leaking bucket** | Cola FIFO procesada a tasa fija | Caudal de salida estable | Ráfagas llenan la cola; datos viejos |
| **Fixed window counter** | Contador por ventana fija (p.ej. por minuto) | Memoria mínima | Pico en el borde de la ventana (hasta 2×) |
| **Sliding window log** | Guarda timestamps de cada petición | Preciso | Mucha memoria |
| **Sliding window counter** | Híbrido: pondera la ventana previa | Suaviza el borde; poca memoria | Aproximado |

**Token bucket es el más usado** (Amazon, Stripe). Implementación típica: **Redis** con `INCR` + `EXPIRE` (atómico, baja latencia). En sistemas distribuidos surgen **condiciones de carrera** (usar scripts Lua / locks) y **sincronización** entre nodos (almacén centralizado de contadores).

---

## Consistent hashing — repartir datos minimizando el remapeo

**Problema con hash módulo n:** `servidor = hash(key) % n`. Al añadir o quitar un servidor, **casi todas** las claves se remapean → tormenta de cache miss.

**Consistent hashing:** coloca servidores y claves en un **anillo hash**. Una clave se asigna al **primer servidor en sentido horario**. Al añadir/quitar un nodo, **solo k/n claves** se mueven (las del segmento afectado), no todas.

**Nodos virtuales (vnodes):** cada servidor físico se representa con muchos puntos en el anillo. Esto:
- Reduce la **varianza** del reparto (distribución más uniforme).
- Permite **heterogeneidad**: un servidor más potente recibe más vnodes.

Más vnodes → mejor balance, pero más metadatos. Es la base de Dynamo, Cassandra y muchas CDNs.

---

## CAP — el trade-off ineludible

En un sistema distribuido no puedes tener las tres a la vez; ante una **partición de red** debes elegir dos:

- **C**onsistency: todos los clientes ven el mismo dato a la vez.
- **A**vailability: toda petición recibe respuesta aunque haya nodos caídos.
- **P**artition tolerance: el sistema sigue operando pese a cortes de red.

Como la partición de red **es inevitable**, en la práctica eliges entre **CP** y **AP**:
- **CP** (sacrifica disponibilidad): bloquea escrituras durante la partición para no servir datos inconsistentes. *Ej.: sistema bancario — el saldo debe ser exacto.*
- **AP** (sacrifica consistencia): sigue aceptando lecturas/escrituras y reconcilia después. *Ej.: feed social — tolera datos un poco rancios.*
- **CA** no existe en el mundo real (no puedes renunciar a tolerar particiones).

---

## Quórum N/W/R — consistencia ajustable

En un KV store replicado N veces:
- **N** = número de réplicas.
- **W** = réplicas que deben confirmar una **escritura** para considerarla exitosa.
- **R** = réplicas que deben responder una **lectura**.

Regla clave: **si W + R > N, hay consistencia fuerte** (siempre hay al menos un nodo solapado con el dato más reciente).

| Config | Optimiza |
|--------|----------|
| R=1, W=N | Lectura rápida |
| W=1, R=N | Escritura rápida |
| W=R=2, N=3 | Balance con consistencia fuerte (W+R>N) |
| W+R ≤ N | Sin garantía de consistencia fuerte |

W/R grandes → más consistencia pero más latencia (esperas al nodo más lento). Es un dial que ajustas según el caso de uso.

---

## Modelos de consistencia y resolución de conflictos

- **Fuerte:** toda lectura ve la última escritura. Bloquea operaciones → mala para alta disponibilidad.
- **Débil:** lecturas posteriores pueden no ver el último valor.
- **Eventual:** forma de débil; con tiempo suficiente, todas las réplicas convergen. *Dynamo y Cassandra la adoptan.*

**Vector clocks** para conflictos por escrituras concurrentes: par `[servidor, versión]` por dato. Versión X es **ancestro** de Y (sin conflicto) si cada contador de X ≤ el de Y; son **hermanas** (conflicto) si ninguna domina a la otra → el cliente reconcilia. Desventaja: crecen con el número de escritores; se truncan los pares más viejos.

---

## Manejo de fallos en KV stores

- **Detección — gossip protocol:** cada nodo lleva una lista de miembros con *heartbeat counters*; los incrementa y los propaga a nodos aleatorios. Si un heartbeat no sube en cierto tiempo, el nodo se marca caído. Descentralizado y escalable (mejor que all-to-all multicast).
- **Fallo temporal — hinted handoff:** otro nodo acepta las escrituras del caído y se las entrega cuando vuelve.
- **Fallo permanente — anti-entropy con Merkle trees:** árbol de hashes de los rangos de datos; comparas raíces y bajas solo por las ramas que difieren → sincronizas transfiriendo el mínimo.
- **Fallo de datacenter:** replica entre regiones conectadas por red de alta velocidad.

**Write path** (estilo Cassandra): escribe en *commit log* → *memtable* en memoria → al llenarse, *flush* a *SSTable* en disco.
**Read path:** consulta memtable; si falla, usa un **bloom filter** para saber en qué SSTable podría estar antes de tocar el disco.

---

## Generador de IDs únicos distribuido

Requisitos: únicos, numéricos, **ordenables por tiempo** (sortable), ~64 bits, miles por segundo.

Opciones y su problema:
- **Auto-increment de BD:** no escala horizontalmente.
- **UUID (128 bits):** únicos sin coordinación, pero no numéricos ni ordenables por tiempo.
- **Ticket server:** punto único de fallo.

**Snowflake (Twitter) — 64 bits**, la respuesta canónica:

| Campo | Bits | Para qué |
|-------|------|----------|
| Signo | 1 | Siempre 0 (positivo) |
| Timestamp | 41 | ms desde una época propia → ~69 años, da el orden temporal |
| Datacenter ID | 5 | 32 datacenters |
| Máquina ID | 5 | 32 máquinas por datacenter |
| Secuencia | 12 | 4096 IDs por ms por máquina |

El timestamp en los bits altos garantiza orden creciente; la secuencia evita colisiones dentro del mismo milisegundo en la misma máquina. Sin coordinación entre nodos.

---

## Mini-ejemplo trabajado: por qué `hash % n` es un desastre al reescalar

Tienes 4 servidores de caché y asignas `servidor = hash(key) % 4`. Añades un quinto → ahora es `% 5`. ¿Cuántas claves cambian de servidor?

Una clave con `hash=100`: antes `100 % 4 = 0`, ahora `100 % 5 = 0` (coincide). Pero `hash=101`: antes 1, ahora 1; `hash=102`: antes 2, ahora 2; `hash=103`: antes 3, ahora 3; `hash=104`: antes 0, ahora **4** (cambia). En general, cambiar el módulo remapea **casi todas** las claves → **tormenta de cache miss** justo al escalar.

El **consistent hashing** lo arregla: servidores y claves en un **anillo**; una clave va al primer servidor en sentido horario. Al añadir un nodo, solo se mueven las **k/n claves** de su segmento, no todas. Los **vnodes** (cada servidor = muchos puntos en el anillo) reducen la varianza del reparto.

**Predicción antes de seguir:** KV store con N=3 réplicas. ¿Qué W y R dan **consistencia fuerte**? Necesitas **W + R > N**: p. ej. W=2, R=2 (2+2=4 > 3) garantiza que el conjunto de lectura y el de escritura **se solapan** en al menos un nodo con el dato más reciente.

## Prototipo, contraejemplo y caso borde

- **Prototipo (token bucket):** rate limiter que permite ráfagas controladas, implementado en Redis con INCR+EXPIRE atómico.
- **Contraejemplo (CA no existe):** prometer consistencia *y* disponibilidad ignorando particiones → en el mundo real la partición es inevitable, eliges CP o AP.
- **Caso borde (fixed window counter):** un contador por minuto deja pasar hasta **2×** el límite en el borde de la ventana (ráfaga al final de un minuto + inicio del siguiente) → sliding window lo suaviza.

## Errores típicos

- **Conceptual:** creer en "CA" de CAP; ante partición (inevitable) eliges **CP** (banca, bloquea) o **AP** (feed, reconcilia luego).
- **Técnico:** rate limiter distribuido sin atomicidad → race conditions; usa scripts Lua/locks o un contador centralizado.
- **De consistencia:** asumir consistencia fuerte con **W + R ≤ N** (no hay solapamiento garantizado).

## Transferencia isomorfa

- **Consistent hashing ↔ hashing como reparto / load balancing:** repartir claves minimizando el remapeo es la misma función hash que reparte elementos en buckets (conecta con [[arena-cc1]], hashing).
- **Token/leaking bucket ↔ load shedding / control de sobrecarga:** limitar el caudal para no colapsar es el rate-limiting del SRE (conecta con [[arena-sre4]], rechazar pronto).
- **Quórum W+R>N ↔ dial consistencia-latencia:** ajustar W/R es el mismo trade-off explícito que el error budget o el CAP — más garantía cuesta más latencia.

Moraleja de la arista: *`hash % n` remapea todo al reescalar; el anillo mueve solo k/n. Y la consistencia es un dial (W+R>N), no un absoluto — ante partición eliges CP o AP.*

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Limitar peticiones por usuario" | Rate limiter: token bucket en Redis (INCR+EXPIRE) |
| "Repartir datos y añadir/quitar nodos sin remapear todo" | Consistent hashing con vnodes |
| "¿Consistencia o disponibilidad ante partición?" | CAP: CP (banca) vs AP (feed) |
| "Quiero ajustar consistencia vs latencia" | Quórum N/W/R, busca W+R>N |
| "Escrituras concurrentes en réplicas" | Vector clocks → reconciliar hermanas |
| "Detectar nodos caídos a escala" | Gossip protocol + hinted handoff |
| "Sincronizar réplicas con poco tráfico" | Merkle trees (anti-entropy) |
| "IDs únicos ordenables sin coordinación" | Snowflake de 64 bits |

---

> **Síntesis:** Estos son los ladrillos que se repiten en casi todo diseño. El rate limiter protege el sistema (token bucket + Redis). El consistent hashing reparte estado minimizando el costo de reescalar. CAP fuerza la decisión CP/AP, y el quórum N/W/R la vuelve un dial continuo (W+R>N = consistencia fuerte). Los conflictos se resuelven con vector clocks, los fallos con gossip + hinted handoff + Merkle trees, y los IDs con el reparto de bits de Snowflake.

---

*Retrieval: cierra y responde: (1) ¿por qué hash%n es malo al reescalar y cómo lo arregla el anillo?; (2) con N=3, ¿qué W y R dan consistencia fuerte y por qué?; (3) ¿qué resuelve un vector clock que un timestamp simple no?; (4) reparte los 64 bits de un ID Snowflake.*
