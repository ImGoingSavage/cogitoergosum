# Puesta en marcha del Mentor local — guía paso a paso

> **Esta es la guía operativa.** El `README.md` explica el *porqué* (arquitectura
> y decisiones); este documento es el *qué hago, en qué orden, y cómo sé que
> funcionó*. Síguelo de arriba a abajo. Marca cada `[ ]` al completarlo.

## Dónde estamos (13 jun 2026)

- ✅ **Todo el código está escrito y subido al repo** (commit `225c624`).
- ✅ El frontend ya trae la tarjeta "Mentor local (opcional)" en el Dashboard,
  pero está **inerte**: no apunta a ningún backend todavía.
- ❌ **El backend NUNCA se ha ejecutado.** Qdrant, Ollama y la API no existen
  en ninguna máquina aún.

**Lo que falta = encender el backend en tu laptop Linux i5.** Son 5 etapas.
Casi todas solo las puedes hacer tú (el agente no tiene acceso a esa laptop).

```
ETAPA 0  Prerequisitos        (instalar una vez)
ETAPA 1  Construir el cerebro  (Qdrant + ingesta de la biblioteca)
ETAPA 2  Encender el servidor  (probar en local, sin internet)
ETAPA 3  Abrir al mundo        (Cloudflare Tunnel)
ETAPA 4  Conectar la app       (en el navegador, 1 minuto)
ETAPA 5  Validar y ajustar     (medir latencia, decidir EVALUACIÓN)
```

---

## ETAPA 0 — Prerequisitos (una sola vez, en la laptop Linux)

- [ ] **Docker** instalado y corriendo (`docker --version`).
- [ ] **Python 3.11+** (`python3 --version`).
- [ ] **Ollama** instalado (`curl -fsSL https://ollama.com/install.sh | sh`).
- [ ] **Descargar los modelos** (tarda; son ~1.5 GB + ~280 MB):
  ```sh
  ollama pull deepseek-r1:1.5b
  ollama pull nomic-embed-text
  ```
- [ ] **Copiar el código y la biblioteca a la laptop.** El repo NO incluye
  `Biblioteca/` (está en `.gitignore` por copyright), así que:
  ```sh
  git clone https://github.com/ImGoingSavage/cogitoergosum.git
  # y aparte, copia tu carpeta Biblioteca/ (con los .txt) a la raíz del repo:
  #   cogitoergosum/Biblioteca/*.txt
  ```

**Cómo sé que terminé la etapa 0:** `ollama list` muestra los dos modelos y
existe `cogitoergosum/Biblioteca/` con archivos `.txt` dentro.

---

## ETAPA 1 — Construir el cerebro (Qdrant + ingesta)

```sh
cd cogitoergosum/mentor-backend

# 1. Base vectorial (queda escuchando solo en 127.0.0.1)
docker compose up -d

# 2. Entorno Python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Configuración. Copia la plantilla y EDÍTALA (ver abajo qué rellenar)
cp .env.example .env
nano .env

# 4. Ingestar la biblioteca a Qdrant (idempotente: puedes re-correrlo)
python ingest.py
```

**Qué rellenar en `.env` (mínimo para arrancar):**
- `SERVICE_TOKEN` → inventa un secreto largo (ej. `openssl rand -hex 32`).
- `SUPABASE_JWKS_URL` → ya viene con tu proyecto; déjalo.
- `ALLOWED_ORIGIN` → `https://imgoingsavage.github.io` (ya viene).
- El resto puede quedarse en su valor por defecto para la primera prueba.

**Cómo sé que terminé la etapa 1:** `ingest.py` imprime al final algo como
`LISTO. nuevos=NNNN saltados=0 archivos_con_error=0 total_en_coleccion=NNNN`.
Si algún archivo falla, lo dice por nombre y sigue con los demás.

> ⏱️ La ingesta embebe cada chunk con Ollama en CPU: con ~50 libros puede
> tardar **bastante** (decenas de minutos). Es de una sola vez. Déjalo correr.

---

## ETAPA 2 — Encender el servidor y probar en LOCAL (sin internet)

```sh
# Con el venv activo y dentro de mentor-backend/
python -m pytest tests/ -q          # 7 pruebas de lógica pura deben pasar
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

En otra terminal:
```sh
curl http://127.0.0.1:8000/health
# Esperado: {"status":"ok","gen_model":"deepseek-r1:1.5b"}
```

**Cómo sé que terminé la etapa 2:** `/health` responde `ok`. (Todavía NO
pruebes `/mentor/evaluar` por curl: exige un JWT real de Supabase; eso se
prueba mejor desde la app en la etapa 4.)

---

## ETAPA 3 — Abrir al mundo (Cloudflare Tunnel)

El túnel hace que `https://...` público llegue a tu `127.0.0.1:8000` **sin
abrir puertos del router**. Dos caminos:

### Camino rápido (para PROBAR hoy, sin dominio)
```sh
cloudflared tunnel --url http://127.0.0.1:8000
```
Te imprime una URL tipo `https://algo-aleatorio.trycloudflare.com`. Sirve para
probar, pero **cambia cada vez** que reinicias. Úsala solo para la primera
prueba de extremo a extremo.

### Camino estable (para los 30 usuarios; necesita un dominio en Cloudflare)
1. `cloudflared tunnel login`
2. `cloudflared tunnel create cogito-mentor`
3. Copia `cloudflared/config.yml` a `~/.cloudflared/config.yml` y edita
   `USUARIO`, el `credentials-file` y `hostname: mentor.TU-DOMINIO.com`.
4. `cloudflared tunnel route dns cogito-mentor mentor.TU-DOMINIO.com`
5. Servicio que arranca solo: copia `cloudflared/cogito-mentor.service` a
   `/etc/systemd/system/`, edita `USUARIO`, y:
   ```sh
   sudo systemctl daemon-reload
   sudo systemctl enable --now cogito-mentor
   ```

**Cómo sé que terminé la etapa 3:** desde tu teléfono (con datos, no wifi)
abres `https://TU-URL/health` y ves el `{"status":"ok"...}`.

---

## ETAPA 4 — Conectar la app (en el navegador, 1 minuto)

1. Abre https://imgoingsavage.github.io/cogitoergosum/ e **inicia sesión**
   (el mentor local exige tu cuenta).
2. Ve al **Dashboard** → tarjeta **"Mentor local (opcional)"**.
3. Marca **"Activar mentor local"**, pega:
   - **URL** → la del túnel (etapa 3).
   - **Service token** → el mismo `SERVICE_TOKEN` de tu `.env`.
4. **Guardar** → **Probar conexión**. Debe decir "Mentor local conectado".
5. Ve al **Modo Estudio**, abre el chat del mentor (la pluma 🪶) y haz una
   pregunta de teoría. La respuesta vendrá del modelo local, citando las
   fuentes de tu biblioteca ("— Apoyado en: …").

**Cómo sé que terminé la etapa 4:** recibes una explicación en Estudio y, abajo,
la línea "Apoyado en: <libros>".

---

## ETAPA 5 — Validar y ajustar

- [ ] **Mide la latencia real** del 1.5B en tu i5 (la respuesta tarda X seg).
      Si es demasiado, baja `num_predict` en `app/llm_providers.py` (p. ej. de
      700 a 400) y reinicia uvicorn.
- [ ] **Decide el modo EVALUACIÓN.** Por defecto (`EVALUACION_FALLBACK=curated`
      en `.env`) el forcejeo NO usa el 1.5B (riesgo de filtrar la solución):
      da pistas curadas. Si quieres experimentar con el modelo local ahí,
      ponlo en `local` — pero revisa que no revele finales.
- [ ] **Apaga y enciende la laptop** y confirma que la app sigue funcionando
      con el mentor local apagado (debe caer a Claude o a pistas curadas, sin
      romperse). Es la prueba de que la Constitución §0.7 se respeta.

---

## Qué le puedes pedir al AGENTE (no necesita la laptop)

- Un `run.sh` que levante Qdrant + uvicorn + túnel con un solo comando.
- Ajustar prompts, `num_predict`, o la política anti-fuga según lo que veas.
- Un endpoint o panel para leer `/metrics` desde la app.
- Cualquier corrección de bug que descubras al probar.

## Problemas comunes

| Síntoma | Causa probable | Arreglo |
|---|---|---|
| `Probar conexión` falla | laptop apagada / URL mal / túnel caído | revisa etapa 3 (`/health` desde el móvil) |
| 401 al preguntar | sesión sin iniciar o JWT vencido | re-inicia sesión en la app |
| 429 | demasiadas preguntas seguidas | espera; sube `USER_RATE_PER_MIN` en `.env` |
| Respuesta vacía o rara | el 1.5B se quedó corto | sube `num_predict`; revisa `ollama list` |
| Ingesta lentísima | embeddings en CPU | normal; es de una vez, déjalo correr |
