"""schemas.py — Contratos de E/S validados con Pydantic (OWASP A03/A04).

Los límites de longitud NO son cosméticos: truncan superficie de prompt
injection y protegen la latencia del 1.5B (entradas largas = generación
larga = laptop al límite).
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ContextoFlujo(str, Enum):
    TEORIA = "TEORIA"
    EVALUACION = "EVALUACION"


# Límites duros por campo (caracteres). Se truncan en sanitize, pero el
# schema rechaza lo absurdo de entrada.
_MAX = 4000


class MentorRequest(BaseModel):
    contexto_flujo: ContextoFlujo
    topic: str = Field(default="", max_length=300)
    difficulty: int = Field(default=1, ge=1, le=5)
    problem_statement: str = Field(default="", max_length=_MAX)
    user_desconstruccion: str = Field(default="", max_length=_MAX)
    user_code_or_answer: str = Field(default="", max_length=_MAX)
    error_message: str = Field(default="", max_length=2000)
    user_question: str = Field(default="", max_length=2000)

    @field_validator("topic", "problem_statement", "user_desconstruccion",
                     "user_code_or_answer", "error_message", "user_question")
    @classmethod
    def _strip(cls, v: str) -> str:
        return (v or "").strip()


class RetrievedChunk(BaseModel):
    fuente: str
    tema: str = ""
    tipo_contenido: str = ""
    score: float = 0.0


class JobAccepted(BaseModel):
    """Respuesta 202 al encolar."""
    job_id: str
    status: str = "queued"
    poll: str  # URL relativa para consultar estado


class MentorResult(BaseModel):
    job_id: str
    status: str  # queued | running | completed | failed | timeout | rejected
    provider: Optional[str] = None  # "ollama" | "curated" | "claude_byok_clientside"
    answer: Optional[str] = None
    retrieved_context: list[RetrievedChunk] = []
    safety_flags: list[str] = []
    latency_ms: Optional[int] = None
    error: Optional[str] = None
