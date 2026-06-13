"""main.py — Orquestador FastAPI del Mentor local.

Flujo: auth → rate-limit → sanitiza → encola. El worker hace
retrieval → genera (local) → audita salida → loguea métricas.
La respuesta es 202 + job_id; el frontend hace polling a /mentor/jobs/{id}.
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .schemas import MentorRequest, JobAccepted, MentorResult, RetrievedChunk
from . import rag, security, observability
from .llm_providers import generar_local
from .prompts import system_para, construir_mensaje_usuario, PROMPT_VERSION
from .queue import queue


@asynccontextmanager
async def lifespan(app: FastAPI):
    observability.init_db()
    await queue.start()
    yield
    await queue.stop()


app = FastAPI(title="CogitoErgoSum Mentor", version="1.0", lifespan=lifespan)

# CORS estricto: SOLO el origen del frontend, solo POST/GET/DELETE, solo las
# cabeceras necesarias. Nada de "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origin],
    allow_methods=["POST", "GET", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Service-Token"],
    allow_credentials=False,
    max_age=600,
)


def _construir_trabajo(req: MentorRequest, user_id: str, job_id: str):
    """Devuelve una función SIN argumentos (closure) que el worker ejecuta en
    un thread. Hace todo el trabajo pesado: retrieval + generación + auditoría."""
    flujo = req.contexto_flujo.value

    def _trabajo() -> dict:
        t0 = time.time()
        # 1. Query de recuperación: prioriza la pregunta o el tema.
        query = security.sanitizar(
            req.user_question or req.topic or req.problem_statement, 1000
        )
        chunks = rag.recuperar(query, flujo, materia=req.topic or None,
                               dificultad=req.difficulty)
        contexto_txt, usados = rag.empaquetar_contexto(chunks)
        t_ret = int((time.time() - t0) * 1000)

        # 2. EVALUACION sin Claude BYOK: por defecto NO arriesgamos el 1.5B
        #    con tutoría socrática estricta (alto riesgo de fuga). Devolvemos
        #    una pista construida del contexto curado.
        if flujo == "EVALUACION" and settings.evaluacion_fallback == "curated":
            ans = _pista_curada(usados)
            provider, gen_ms, flags = "curated", 0, []
        else:
            # 3. Generación local (TEORIA siempre; EVALUACION solo si se
            #    configuró "local" explícitamente).
            t1 = time.time()
            req_san = _sanitizar_request(req)
            mensaje = construir_mensaje_usuario(req_san, contexto_txt)
            ans = generar_local(system_para(flujo), mensaje,
                                 max_tokens=500 if flujo == "EVALUACION" else 700)
            gen_ms = int((time.time() - t1) * 1000)
            provider, flags = "ollama", []
            if flujo == "EVALUACION":
                ans, flags = security.auditar_salida_evaluacion(ans)

        total_ms = int((time.time() - t0) * 1000)
        observability.registrar(
            job_id, user_id, flujo, provider, "completed",
            t_ret, gen_ms, total_ms, len(usados), flags, PROMPT_VERSION,
        )
        return {
            "provider": provider,
            "answer": ans,  # síntesis del modelo, NO el texto fuente
            # GARANTÍA "nunca texto íntegro": retrieved_context expone SOLO
            # metadatos de procedencia (fuente/tema/tipo/score). El campo
            # `texto` del chunk se queda en el servidor: alimenta el contexto
            # del modelo y jamás cruza la red hacia el navegador.
            "retrieved_context": [
                RetrievedChunk(fuente=c["fuente"], tema=c["tema"],
                               tipo_contenido=c["tipo_contenido"],
                               score=round(c["score"], 3)).model_dump()
                for c in usados
            ],
            "safety_flags": flags,
            "latency_ms": total_ms,
        }

    return _trabajo


def _sanitizar_request(req: MentorRequest) -> MentorRequest:
    return req.model_copy(update={
        "problem_statement": security.sanitizar(req.problem_statement),
        "user_desconstruccion": security.sanitizar(req.user_desconstruccion),
        "user_code_or_answer": security.sanitizar(req.user_code_or_answer),
        "error_message": security.sanitizar(req.error_message, 2000),
        "user_question": security.sanitizar(req.user_question, 2000),
        "topic": security.sanitizar(req.topic, 300),
    })


def _pista_curada(chunks: list[dict]) -> str:
    """Construye una pista en EVALUACION SIN modelo generativo: parafrasea el
    tipo de fragmento, nunca su contenido literal de solución (que además ya
    quedó excluido por rag.recuperar)."""
    if not chunks:
        return ("No tengo material recuperado para guiarte sin arriesgar el "
                "aprendizaje. Vuelve al enunciado: ¿qué cantidad se conserva, "
                "o qué pasa con el caso más pequeño?")
    temas = ", ".join(sorted({c["tema"] for c in chunks if c["tema"]})[:3])
    return ("Antes de seguir, revisa estas ideas del material: "
            f"{temas or 'los conceptos base del tema'}. "
            "Pregúntate cuál de ellas restringe el problema y prueba un caso "
            "pequeño con esa lente. Dime qué observas y seguimos.")


@app.post("/mentor/evaluar", response_model=JobAccepted, status_code=202)
async def evaluar(req: MentorRequest, request: Request,
                  user_id: str = Depends(security.usuario_actual),
                  _svc=Depends(security.exigir_service_token)):
    if not security.rate_limiter.permitir(user_id):
        raise HTTPException(status_code=429, detail="demasiadas solicitudes; espera un momento")
    job_id = queue.nuevo_id()  # se genera antes para que el closure lo conozca
    try:
        job = queue.encolar(user_id, _construir_trabajo(req, user_id, job_id), job_id=job_id)
    except ValueError as e:
        raise HTTPException(status_code=429, detail=str(e))
    return JobAccepted(job_id=job.id, poll=f"/mentor/jobs/{job.id}")


@app.get("/mentor/jobs/{job_id}", response_model=MentorResult)
async def estado_job(job_id: str, user_id: str = Depends(security.usuario_actual)):
    job = queue.obtener(job_id)
    if not job or job.user_id != user_id:  # A01: no se ven jobs ajenos
        raise HTTPException(status_code=404, detail="job no encontrado")
    base = MentorResult(job_id=job.id, status=job.status, error=job.error)
    if job.status == "completed" and job.result:
        return base.model_copy(update=job.result)
    return base


@app.delete("/mentor/jobs/{job_id}", status_code=200)
async def cancelar_job(job_id: str, user_id: str = Depends(security.usuario_actual)):
    if not queue.cancelar(job_id, user_id):
        raise HTTPException(status_code=409, detail="no se pudo cancelar (ya corriendo o ajeno)")
    return {"status": "cancelado"}


@app.get("/health")
async def health():
    return {"status": "ok", "gen_model": settings.ollama_gen_model}


@app.get("/metrics")
async def metrics(_svc=Depends(security.exigir_service_token)):
    return observability.resumen()
