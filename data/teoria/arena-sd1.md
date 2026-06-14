# Fundamentos de escalabilidad y estimación

## De un servidor a millones de usuarios

El camino de crecimiento sigue un orden casi siempre igual:

1. **Un solo servidor** (web + app + DB juntos) → suficiente para empezar.
2. **Separa la base de datos** en su propia máquina: escala web y datos por separado.
3. **Load balancer** + varios servidores web sin estado (stateless): tolera caídas y reparte carga.
4. **Replicación de la BD** (primaria para escrituras, réplicas para lecturas).
5. **Caché** y **CDN** para descargar la BD y acercar los datos al usuario.
6. **Tier sin estado** + sesiones en un almacén compartido (Redis), no en memoria del servidor.
7. **Múltiples centros de datos** con geo-DNS.
8. **Cola de mensajes** y **sharding** de la base de datos para escalar la escritura.

**Principio rector:** mantén el tier web **stateless** — cualquier servidor atiende cualquier petición. El estado vive en un almacén compartido, nunca en el servidor de aplicación.

---

## Escalado vertical vs horizontal

| | Vertical (scale up) | Horizontal (scale out) |
|-|--------------------|------------------------|
| Qué haces | Máquina más potente | Más máquinas |
| Tope | Límite físico de hardware | Prácticamente ilimitado |
| Failover | Punto único de fallo | Redundante |
| Cuándo | Tráfico bajo, simplicidad | Escala real |

A escala grande, **horizontal es obligatorio**: no hay máquina lo bastante grande, y necesitas redundancia.

---

## Caché — descargar la base de datos

**Read-through / cache-aside:** la app consulta la caché; si falla (miss), lee la BD y rellena la caché.

Consideraciones:
- **Cuándo usar:** datos que se leen mucho y se modifican poco.
- **Expiración (TTL):** ni muy corta (muchos miss) ni muy larga (datos rancios).
- **Consistencia:** mantener caché y BD sincronizadas es difícil (invalidación).
- **Evicción:** LRU es la política más común.
- **Punto único de fallo:** usa varios nodos de caché; sobreaprovisiona memoria.

**CDN:** caché geográficamente distribuida para contenido estático (imágenes, JS, CSS, video). El usuario recibe los bytes del nodo más cercano. TTL, invalidación y costo por transferencia son las decisiones clave.

---

## Números de latencia que todo ingeniero debe conocer

El orden de magnitud importa más que el número exacto:

| Operación | Tiempo aproximado |
|-----------|------------------|
| Referencia a caché L1 | ~0.5 ns |
| Referencia a memoria principal | ~100 ns |
| Compresión rápida (1 KB) | ~10 µs |
| Enviar 1 KB por red 1 Gbps | ~10 µs |
| Lectura aleatoria de SSD | ~150 µs |
| Round trip dentro del mismo datacenter | ~500 µs |
| Seek de disco duro (HDD) | ~10 ms |
| Round trip intercontinental | ~150 ms |

**Conclusiones:** la memoria es rápida, el disco es lento (evita seeks), comprime antes de enviar por red, y los datacenters lejanos cuestan latencia.

---

## Disponibilidad medida en "nueves"

| Disponibilidad | Downtime al año |
|----------------|-----------------|
| 99% (dos nueves) | ~3.65 días |
| 99.9% (tres nueves) | ~8.76 horas |
| 99.99% (cuatro nueves) | ~52.6 minutos |
| 99.999% (cinco nueves) | ~5.26 minutos |

Los proveedores cloud fijan su **SLA** en 99.9% o más. Cada nueve adicional cuesta exponencialmente más.

---

## Estimación de capacidad (back-of-the-envelope)

El **proceso** importa más que el número. Reglas:

- **Redondea y aproxima:** "99987 / 9.1" ≈ "100000 / 10". La precisión no se evalúa.
- **Escribe tus supuestos** (usuarios activos, tamaño por registro, años de retención).
- **Etiqueta unidades** siempre (5 MB, no "5").
- **Potencias de 2:** KB=2¹⁰, MB=2²⁰, GB=2³⁰, TB=2⁴⁰, PB=2⁵⁰ bytes.

**Lo que casi siempre te piden:** QPS, QPS pico, almacenamiento, caché, número de servidores.

**Patrón de cálculo de QPS:**
```
DAU = usuarios_mensuales × fracción_diaria
QPS = DAU × acciones_por_día / 86400 s
QPS_pico ≈ 2 × QPS
```

**Ejemplo (estilo Twitter, cifras de práctica):** 300 M usuarios mensuales, 50% diarios, 2 tweets/día →
DAU = 150 M; QPS = 150M × 2 / 86400 ≈ **3500**; pico ≈ **7000**.
Almacenamiento media: 150M × 2 × 10% × 1 MB = 30 TB/día → 5 años ≈ **55 PB**.

---

## El marco de 4 pasos para la entrevista

El diseño final importa menos que **el proceso**. No seas como Jimmy (responder rápido sin entender es bandera roja).

**Paso 1 — Entender el problema y fijar el alcance.**
Haz preguntas; no asumas. ¿Qué features concretas? ¿Cuántos usuarios? ¿Escala esperada en un año? ¿Stack existente que reutilizar? Anota los supuestos.

**Paso 2 — Diseño de alto nivel.**
Diagrama de cajas: clientes, API gateway/LB, servidores, caché, BD, CDN, colas. Acuerda con el entrevistador los componentes y el flujo de datos. Haz una estimación de capacidad aquí.

**Paso 3 — Diseño en profundidad.**
Profundiza en los componentes críticos y sus cuellos de botella: el esquema de la BD, el algoritmo del rate limiter, cómo se hace el sharding. Discute trade-offs concretos.

**Paso 4 — Cerrar.**
Identifica cuellos de botella, puntos únicos de fallo, qué monitorear, cómo manejar errores, y cómo escalaría a 10×. Reconoce lo que dejaste fuera.

**Bandera roja capital: sobre-ingeniería.** Ignorar trade-offs por "pureza" de diseño cuesta caro. Lo simple que cumple los requisitos gana.

---

## Disparadores

| Señal | Jugada |
|-------|--------|
| "Diséñame el producto X" (vago) | Marco de 4 pasos: primero pregunta y fija alcance |
| "¿Cuántos servidores/almacenamiento?" | Estimación: DAU → QPS → storage, redondeando |
| "El servidor de app guarda la sesión" | Bandera roja: hazlo stateless, sesión en Redis |
| "Lecturas mucho mayores que escrituras" | Réplicas de lectura + caché read-through |
| "Contenido estático global" | CDN cercana al usuario |
| "Pico de tráfico hunde la BD" | Caché + cola para absorber y desacoplar |

---

> **Síntesis:** Escalar es una secuencia, no un salto: separa responsabilidades, vuelve stateless el tier web, replica y cachea las lecturas, y desacopla con colas. La estimación no busca precisión sino orden de magnitud para decidir el diseño. Y en la entrevista, el proceso (preguntar, acordar, discutir trade-offs, evitar sobre-ingeniería) vale más que el diagrama final.

---

*Retrieval: cierra y responde: (1) ¿por qué el tier web debe ser stateless y dónde vive la sesión?; (2) calcula el QPS de una app con 100 M usuarios diarios que hacen 5 acciones/día; (3) ¿cuánto downtime al año implica 99.99%?; (4) nombra los 4 pasos del marco de entrevista.*
