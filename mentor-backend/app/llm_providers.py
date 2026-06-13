"""llm_providers.py — Generación local (Ollama) + limpieza de salida.

DECISIÓN DE ARQUITECTURA (auditoría):
- Este backend SOLO genera con el modelo LOCAL (Ollama/DeepSeek).
- Claude BYOK se queda 100% en el cliente (browser → api.anthropic.com,
  como hoy en aiMentor.js). La API key del usuario JAMÁS llega a este
  servidor: enviarla aquí AUMENTARÍA su exposición. Por eso no hay ningún
  proveedor "claude" en este módulo, a propósito.
- El frontend decide: si tiene Claude BYOK y el flujo lo amerita, llama a
  Anthropic directo; si no, llama a /mentor/evaluar (local). Ver README.
"""

import re
import httpx
from .config import settings

# DeepSeek-R1 emite trazas de razonamiento entre <think>…</think>. NUNCA
# deben llegar al usuario (ruido + a veces filtran el resultado en EVALUACION).
_THINK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_THINK_ABIERTO = re.compile(r"<think>.*", re.DOTALL | re.IGNORECASE)


def limpiar_salida(texto: str) -> str:
    texto = _THINK.sub("", texto)
    texto = _THINK_ABIERTO.sub("", texto)  # think sin cerrar (truncado)
    return texto.strip()


def generar_local(system: str, mensaje_usuario: str, *, max_tokens: int = 600,
                  temperature: float = 0.3) -> str:
    """Llamada bloqueante a Ollama. Corre dentro del worker de la cola, no en
    el event loop. num_predict acota la generación (latencia en CPU)."""
    r = httpx.post(
        f"{settings.ollama_url}/api/chat",
        json={
            "model": settings.ollama_gen_model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": mensaje_usuario},
            ],
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": 4096,
            },
        },
        timeout=settings.job_timeout_s,
    )
    r.raise_for_status()
    return limpiar_salida(r.json()["message"]["content"])
