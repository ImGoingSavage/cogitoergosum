"""observability.py — Métricas y logging mínimos en SQLite.

Filosofía artesanal: nada de Prometheus/Grafana para 30 usuarios. Una tabla
SQLite con una fila por job basta para responder "¿qué tan lento va?",
"¿cuántas fugas detectó la red de seguridad?", "¿qué proveedor se usa?".

PRIVACIDAD (OWASP A09 + Constitución §0): NO se guarda el texto del usuario
ni la respuesta. Solo metadatos: hashes, tiempos, banderas, conteos.
"""

import sqlite3
import time
import hashlib
from contextlib import contextmanager
from pathlib import Path

_DB = Path(__file__).parent.parent / "metrics.db"


def init_db() -> None:
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                user_hash TEXT,
                flujo TEXT,
                provider TEXT,
                status TEXT,
                retrieval_ms INTEGER,
                gen_ms INTEGER,
                total_ms INTEGER,
                n_chunks INTEGER,
                safety_flags TEXT,
                prompt_version TEXT,
                created_at REAL
            )
        """)


@contextmanager
def _conn():
    con = sqlite3.connect(_DB, timeout=10)
    try:
        yield con
        con.commit()
    finally:
        con.close()


def _hash_user(user_id: str) -> str:
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]


def registrar(job_id: str, user_id: str, flujo: str, provider: str, status: str,
              retrieval_ms: int, gen_ms: int, total_ms: int, n_chunks: int,
              safety_flags: list[str], prompt_version: str) -> None:
    with _conn() as c:
        c.execute(
            "INSERT OR REPLACE INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (job_id, _hash_user(user_id), flujo, provider, status,
             retrieval_ms, gen_ms, total_ms, n_chunks,
             ",".join(safety_flags), prompt_version, time.time()),
        )


def resumen() -> dict:
    """Para GET /metrics. Agregados de las últimas 24 h."""
    desde = time.time() - 86400
    with _conn() as c:
        cur = c.execute(
            "SELECT status, provider, total_ms, safety_flags FROM jobs WHERE created_at > ?",
            (desde,),
        )
        filas = cur.fetchall()
    if not filas:
        return {"jobs_24h": 0}
    tiempos = sorted(f[2] for f in filas if f[2])
    fugas = sum(1 for f in filas if "posible_fuga_solucion" in (f[3] or ""))
    errores = sum(1 for f in filas if f[0] in ("failed", "timeout"))

    def pct(p):
        return tiempos[min(len(tiempos) - 1, int(len(tiempos) * p))] if tiempos else 0

    return {
        "jobs_24h": len(filas),
        "errores_24h": errores,
        "fugas_detectadas_24h": fugas,
        "latencia_p50_ms": pct(0.50),
        "latencia_p95_ms": pct(0.95),
        "por_proveedor": _conteo(filas, idx=1),
        "por_estado": _conteo(filas, idx=0),
    }


def _conteo(filas, idx):
    d: dict[str, int] = {}
    for f in filas:
        d[f[idx]] = d.get(f[idx], 0) + 1
    return d
