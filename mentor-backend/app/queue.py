"""queue.py — Cola ligera de inferencia (la laptop no debe congelarse).

POR QUÉ NO BackgroundTasks (auditoría):
- No tiene límite de cola: 10 requests = 10 inferencias compitiendo por la
  CPU → todo se cuelga, no hay backpressure ni 429.
- No tiene estado consultable, ni timeout, ni cancelación, ni TTL.
- Muere con el proceso sin dejar rastro.

DISEÑO: una asyncio.Queue + un pool de N workers (N=MAX_INFLIGHT, =1 en el
i5). El trabajo de inferencia es bloqueante (httpx síncrono a Ollama), así
que cada worker lo corre en un thread (run_in_executor) para no tapar el
event loop. El estado vive en memoria (dict) con TTL; las métricas, en SQLite.
Suficiente y honesto para 30 usuarios con baja simultaneidad. Si algún día
hay varias laptops o reinicios frecuentes, ESTE es el módulo que se cambia
por Redis+RQ — nada más.
"""

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from .config import settings


@dataclass
class Job:
    id: str
    user_id: str
    fn: Callable[[], dict]  # trabajo bloqueante; devuelve dict de resultado
    status: str = "queued"  # queued|running|completed|failed|timeout
    result: Optional[dict] = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    finished_at: Optional[float] = None


class InferenceQueue:
    def __init__(self):
        self._q: asyncio.Queue[str] = asyncio.Queue(maxsize=settings.max_queue)
        self._jobs: dict[str, Job] = {}
        self._workers: list[asyncio.Task] = []
        self._jobs_por_usuario: dict[str, int] = {}

    # --- ciclo de vida (lo llama main.py en startup/shutdown) ---
    async def start(self):
        for _ in range(settings.max_inflight):
            self._workers.append(asyncio.create_task(self._worker()))
        asyncio.create_task(self._purgador())

    async def stop(self):
        for w in self._workers:
            w.cancel()

    # --- API pública ---
    def pendientes_de(self, user_id: str) -> int:
        return self._jobs_por_usuario.get(user_id, 0)

    def nuevo_id(self) -> str:
        return uuid.uuid4().hex

    def encolar(self, user_id: str, fn: Callable[[], dict], job_id: str | None = None) -> Job:
        """Lanza ValueError si la cola está llena o el usuario tiene demasiados
        jobs vivos (el endpoint lo traduce a 429). job_id puede venir dado para
        que el closure de trabajo conozca su propio id antes de encolarse."""
        if self._q.full():
            raise ValueError("cola llena")
        if self.pendientes_de(user_id) >= 2:
            raise ValueError("demasiados jobs en vuelo para este usuario")
        job = Job(id=job_id or self.nuevo_id(), user_id=user_id, fn=fn)
        self._jobs[job.id] = job
        self._jobs_por_usuario[user_id] = self.pendientes_de(user_id) + 1
        self._q.put_nowait(job.id)
        return job

    def obtener(self, job_id: str) -> Optional[Job]:
        return self._jobs.get(job_id)

    def cancelar(self, job_id: str, user_id: str) -> bool:
        job = self._jobs.get(job_id)
        if not job or job.user_id != user_id:
            return False
        if job.status == "queued":
            job.status = "failed"
            job.error = "cancelado por el usuario"
            self._cerrar(job)
            return True
        return False  # ya corriendo: no se interrumpe a mitad

    # --- internos ---
    async def _worker(self):
        loop = asyncio.get_running_loop()
        while True:
            job_id = await self._q.get()
            job = self._jobs.get(job_id)
            if not job or job.status != "queued":
                self._q.task_done()
                continue
            job.status = "running"
            try:
                # Timeout duro: una generación colgada no bloquea al worker.
                job.result = await asyncio.wait_for(
                    loop.run_in_executor(None, job.fn),
                    timeout=settings.job_timeout_s,
                )
                job.status = "completed"
            except asyncio.TimeoutError:
                job.status = "timeout"
                job.error = "la generación superó el tiempo límite"
            except Exception as e:  # noqa: BLE001 — se reporta, no se filtra traza
                job.status = "failed"
                job.error = str(e)[:200]
            finally:
                self._cerrar(job)
                self._q.task_done()

    def _cerrar(self, job: Job):
        job.finished_at = time.time()
        n = self.pendientes_de(job.user_id)
        if n > 0:
            self._jobs_por_usuario[job.user_id] = n - 1

    async def _purgador(self):
        """Borra jobs terminados pasado el TTL (no crece la memoria)."""
        while True:
            await asyncio.sleep(60)
            ahora = time.time()
            muertos = [
                jid for jid, j in self._jobs.items()
                if j.finished_at and ahora - j.finished_at > settings.job_ttl_s
            ]
            for jid in muertos:
                self._jobs.pop(jid, None)


queue = InferenceQueue()
