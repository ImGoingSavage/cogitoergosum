# Mentor local híbrido — CogitoErgoSum

Backend **opcional** de IA: RAG sobre la biblioteca + generación local
(Ollama/DeepSeek) con dos personalidades pedagógicas (TEORÍA / EVALUACIÓN).
Claude se queda 100 % en el cliente (BYOK), como hoy.

> **Esto NO reemplaza al mentor actual.** Es una mejora progresiva. Si la
> laptop está apagada, la app sigue funcionando exactamente como ahora
> (Constitución §0.7: la IA y la cuenta son SIEMPRE opcionales).

---

## 0. Decisiones de arquitectura (por qué NO se siguió la propuesta al pie)

La auditoría cambió cuatro cosas de la propuesta original. Resumen:

1. **El backend es opcional, no obligatorio.** La laptop personal es un punto
   único de fallo (se duerme, pierde wifi, se reinicia). Para 30 usuarios eso
   sería un mentor caído la mayor parte del tiempo. El frontend prueba
   `GET /health`; si no responde, cae a Claude BYOK (cliente) o a las pistas
   curadas que ya existen. Nunca bloquea.
2. **Claude BYOK NO pasa por este servidor.** Hoy la key va
   `navegador → api.anthropic.com` directo y no toca ningún servidor.
   Enrutarla por la laptop AUMENTARÍA su exposición (tránsito + memoria +
   riesgo de log). Por eso aquí solo hay generación local. Ver
   `app/llm_providers.py`.
3. **DeepSeek-R1 1.5B NO hace de tutor socrático en EVALUACIÓN por defecto.**
   Un modelo de 1.5B alucina matemáticas y filtra la solución pese a las
   reglas. En EVALUACIÓN, sin Claude BYOK, se sirven **pistas curadas**
   (`EVALUACION_FALLBACK=curated`). El 1.5B brilla en TEORÍA (exposición
   apoyada en RAG, donde filtrar la solución no es un riesgo).
4. **Cloudflare Tunnel ≠ autenticación.** El túnel solo evita abrir puertos.
   La auth real es el **JWT de Supabase** verificado por firma en FastAPI
   (`app/security.py`) + un service token compartido + rate limiting.
   Cloudflare Access rompería el `fetch` del SPA público (redirige a login):
   no se usa para la ruta XHR.

**Licencia / copyright (resuelto).** El corpus de RAG son `Biblioteca/*.txt`,
copias que **cada usuario adquirió y aportó** (material que ya licenció).
Además, el sistema **nunca devuelve el texto íntegro**: los chunks alimentan
el *contexto* del modelo y la respuesta al usuario es una **explicación
sintetizada**, no una transcripción. Garantía en código: `retrieved_context`
expone solo metadatos (fuente/tema/tipo/score); el campo `texto` del chunk se
queda en el servidor (ver comentario en `app/main.py`). Coherente con el
espíritu de HANDOFF §3.11.5: el repo público sigue sin texto íntegro (la
`Biblioteca/` y `qdrant_storage/` están en `.gitignore`); el corpus vive solo
en la laptop local y solo la síntesis cruza la red.

---

## 1. Arquitectura final

```
GitHub Pages (frontend, público)
  │  fetch con: Authorization: Bearer <JWT Supabase> + X-Service-Token
  ▼
Cloudflare Tunnel  (solo publica FastAPI; sin abrir puertos del router)
  ▼
FastAPI 127.0.0.1:8000   ── auth JWT, rate-limit, sanitiza, ENCOLA (202)
  │           └─ cola asyncio + 1 worker (i5) + timeout + TTL  (app/queue.py)
  ▼ (worker, en thread)
  ├─ Qdrant 127.0.0.1:6333   (vectorial; loopback, nunca público)
  └─ Ollama 127.0.0.1:11434  (DeepSeek 1.5B + nomic-embed-text; loopback)

Claude (opcional)  ──  navegador → api.anthropic.com   (NUNCA por la laptop)
```

---

## 2. Puesta en marcha (orden importa)

```sh
# 1. Modelos locales
ollama pull deepseek-r1:1.5b
ollama pull nomic-embed-text

# 2. Base vectorial
cd mentor-backend
docker compose up -d            # Qdrant en 127.0.0.1:6333

# 3. Entorno Python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # edita: SERVICE_TOKEN, SUPABASE_*, ALLOWED_ORIGIN

# 4. Ingesta del corpus (idempotente; reejecutable)
python ingest.py                # o --recreate para reconstruir

# 5. Pruebas de lógica pura (no necesitan Qdrant/Ollama)
python -m pytest tests/ -q

# 6. API
uvicorn app.main:app --host 127.0.0.1 --port 8000

# 7. Túnel (otra terminal; ver cloudflared/)
cloudflared tunnel run cogito-mentor
```

---

## 3. Endpoints

| Método | Ruta                     | Qué hace                                  |
|--------|--------------------------|-------------------------------------------|
| POST   | `/mentor/evaluar`        | Encola un trabajo → **202** `{job_id}`    |
| GET    | `/mentor/jobs/{id}`      | Estado/resultado del job (solo el dueño)  |
| DELETE | `/mentor/jobs/{id}`      | Cancela un job **en cola** (no en curso)  |
| GET    | `/health`                | Liveness (lo sondea el frontend)          |
| GET    | `/metrics`               | Agregados 24 h (requiere service token)   |

Respuestas: **202** al encolar, **429** si cola llena / rate limit / demasiados
jobs del mismo usuario, **401** sin JWT válido, **404** job ajeno o inexistente.

---

## 4. Integración con el frontend (sin romper nada)

`aiMentor.js` no se toca. Se añade un cliente nuevo (p. ej. `mentorLocal.js`)
que el `mentorChat.js` usa **solo si**:

1. `GET /health` responde (laptop encendida), y
2. el usuario optó por el mentor local (toggle en Ajustes), y
3. para EVALUACIÓN: solo si no hay Claude BYOK o el usuario lo prefiere.

Patrón de polling (202 → GET hasta `completed`), con el JWT que ya tienes en
`sesionSupabase.accessToken`. Si algo falla, se cae a lo de hoy. La key de
Claude **nunca** se manda a este backend.

---

## 5. Estructura

```
mentor-backend/
├── app/
│   ├── config.py          # settings tipadas (.env)
│   ├── schemas.py         # contratos Pydantic + límites de longitud
│   ├── prompts.py         # system prompts duales + empaquetado anti-injection
│   ├── rag.py             # Qdrant: filtros, rerank keyword, anti-fuga
│   ├── llm_providers.py   # Ollama + limpieza <think> (sin Claude, a propósito)
│   ├── queue.py           # cola asyncio + worker + timeout + TTL
│   ├── security.py        # JWT Supabase, sanitiza, audita salida, rate-limit
│   ├── observability.py   # métricas SQLite (sin texto de usuario)
│   └── main.py            # orquestador FastAPI
├── ingest.py              # ingesta idempotente Biblioteca/*.txt → Qdrant
├── docker-compose.yml     # Qdrant (loopback)
├── cloudflared/           # config.yml + servicio systemd
├── tests/test_smoke.py    # lógica pura (injection, fuga, troceo, <think>)
├── requirements.txt
└── .env.example
```

---

## 6. Deuda técnica aceptada

- Estado de jobs en memoria: un reinicio del proceso pierde jobs en curso (el
  frontend reintenta; es aceptable para 30 usuarios). Migrar a Redis+RQ solo
  si hay varias instancias o reinicios frecuentes.
- Rerank por keywords, no cross-encoder (no cabe en CPU). Suficiente con
  filtros de metadata buenos.
- Métricas en SQLite, no Prometheus. A propósito (artesanal, 30 usuarios).
