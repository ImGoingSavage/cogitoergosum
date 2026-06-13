"""security.py — Autenticación de usuario, sanitización y anti-fuga de salida.

Capas (defensa en profundidad):
1. Cabecera de servicio compartida (lo que no la trae ni llega a la lógica).
2. JWT de Supabase verificado por firma (RS256 vía JWKS, o HS256 fallback).
3. Sanitización/neutralización de input antes de tocar el prompt.
4. Auditoría de la SALIDA en EVALUACION (red de seguridad anti-fuga).
"""

import re
import time
import httpx
import jwt
from jwt import PyJWKClient
from fastapi import Header, HTTPException, status

from .config import settings

# ---- 1. Cabecera de servicio ----------------------------------------------

def exigir_service_token(x_service_token: str = Header(default="")) -> None:
    if not settings.service_token:
        return  # sin token configurado: modo dev local
    if x_service_token != settings.service_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="service token inválido")


# ---- 2. JWT de Supabase ----------------------------------------------------

_jwks_client: PyJWKClient | None = None
if settings.supabase_jwks_url:
    _jwks_client = PyJWKClient(settings.supabase_jwks_url)


def usuario_actual(authorization: str = Header(default="")) -> str:
    """Devuelve el user_id (sub) si el Bearer JWT es válido. 401 si no.
    NO confía en ningún claim sin verificar la firma (OWASP A07/A01)."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="falta Bearer token")
    token = authorization[7:]
    try:
        if _jwks_client:  # RS256 moderno
            signing_key = _jwks_client.get_signing_key_from_jwt(token).key
            claims = jwt.decode(token, signing_key, algorithms=["RS256", "ES256"],
                                audience="authenticated")
        elif settings.supabase_jwt_secret:  # HS256 legado
            claims = jwt.decode(token, settings.supabase_jwt_secret,
                                algorithms=["HS256"], audience="authenticated")
        else:
            raise HTTPException(status_code=500, detail="auth no configurada")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="token inválido")
    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="token sin sub")
    return sub


# ---- 3. Sanitización de entrada -------------------------------------------

# Patrones de prompt injection más comunes: se NEUTRALIZAN (no se borran, para
# no romper texto legítimo) marcándolos como cita.
_INJECT = re.compile(
    r"(ignora\s+(todas?\s+)?(las?\s+)?instruccion|ignore\s+(all\s+)?previous|"
    r"system\s*prompt|olvida\s+lo\s+anterior|act\s+as\s+|reveal\s+the\s+solution|"
    r"dame\s+la\s+respuesta\s+final|dime\s+el\s+resultado)",
    re.IGNORECASE,
)
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def sanitizar(texto: str, limite: int = 4000) -> str:
    if not texto:
        return ""
    texto = _CTRL.sub("", texto)
    texto = _INJECT.sub(lambda m: f"«{m.group(0)}»", texto)  # desactiva como orden
    return texto[:limite].strip()


# ---- 4. Auditoría de salida en EVALUACION ---------------------------------

# Señales de que el modelo está REVELANDO la solución pese a las reglas.
_FUGA = re.compile(
    r"(la\s+respuesta\s+(es|final)|el\s+resultado\s+es|la\s+soluci[oó]n\s+es|"
    r"por\s+lo\s+tanto[, ]+\s*\w+\s*=\s*\d|en\s+conclusi[oó]n,\s+la\s+respuesta)",
    re.IGNORECASE,
)


def auditar_salida_evaluacion(texto: str) -> tuple[str, list[str]]:
    """En EVALUACION, si la salida parece revelar el final, se sustituye por
    una pista segura y se marca la bandera. Red de seguridad, no la única
    defensa (el system prompt es la primera)."""
    flags: list[str] = []
    if _FUGA.search(texto):
        flags.append("posible_fuga_solucion")
        texto = ("Estás muy cerca. En lugar de darte el final, piensa: ¿qué paso "
                 "te falta justificar para llegar tú mismo a la conclusión? "
                 "Prueba el siguiente caso pequeño y dime qué observas.")
    return texto, flags


# ---- Rate limiting por usuario (ventana deslizante en memoria) ------------

class RateLimiter:
    def __init__(self, por_minuto: int):
        self.por_minuto = por_minuto
        self._hits: dict[str, list[float]] = {}

    def permitir(self, user_id: str) -> bool:
        ahora = time.time()
        ventana = self._hits.setdefault(user_id, [])
        # purga > 60s
        self._hits[user_id] = [t for t in ventana if ahora - t < 60]
        if len(self._hits[user_id]) >= self.por_minuto:
            return False
        self._hits[user_id].append(ahora)
        return True


rate_limiter = RateLimiter(settings.user_rate_per_min)
