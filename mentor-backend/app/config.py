"""config.py — Configuración única, tipada y validada (pydantic-settings).

Toda variable viene de entorno/.env. Un secreto JAMÁS se hardcodea
(OWASP A05/A07). Importar `settings` desde cualquier módulo.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Supabase / auth
    supabase_project_ref: str = ""
    supabase_jwks_url: str = ""
    supabase_jwt_secret: str = ""

    # CORS / red
    allowed_origin: str = "https://imgoingsavage.github.io"
    service_token: str = ""

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "cogito_biblioteca"

    # Ollama
    ollama_url: str = "http://localhost:11434"
    ollama_gen_model: str = "deepseek-r1:1.5b"
    ollama_embed_model: str = "nomic-embed-text"

    # nomic-embed-text emite vectores de 768 dims; distancia coseno.
    embed_dim: int = 768

    # Cola / límites
    max_inflight: int = 1
    max_queue: int = 12
    job_timeout_s: int = 180
    user_rate_per_min: int = 6
    job_ttl_s: int = 900

    # Pedagogía
    evaluacion_fallback: str = "curated"  # "curated" | "local"

    # Presupuesto de contexto (tokens aprox.) que se inyecta del RAG
    rag_context_token_budget: int = 1200
    rag_top_k: int = 6


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
