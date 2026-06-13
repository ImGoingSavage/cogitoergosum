"""rag.py — Recuperación sobre Qdrant + política anti-fuga de soluciones.

Diseño deliberado para hardware modesto y corpus mediano:
- Búsqueda vectorial con filtros de payload (materia/tema/dificultad/tipo).
- Reranking ligero por solapamiento de keywords (sin modelo cross-encoder:
  no cabe en el presupuesto de CPU). Barato y mejora bastante el orden.
- Fallback semántico: si el filtro estricto no devuelve nada, se relaja.
- POLÍTICA ANTI-FUGA: en EVALUACION los chunks tipo "solucion" se EXCLUYEN
  del recuperador (filtro a nivel de Qdrant) y, por si acaso, se vuelven a
  filtrar en memoria. Defensa en profundidad.
"""

import re
import httpx
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from .config import settings

COLLECTION = settings.qdrant_collection

# Tipos de contenido que NUNCA deben alimentar al generador en EVALUACION:
# revelarían el final. Coherente con el gating del frontend.
TIPOS_PROHIBIDOS_EVALUACION = {"solucion", "moraleja"}

_client = QdrantClient(url=settings.qdrant_url, timeout=10)


def _embed(texto: str) -> list[float]:
    """Embedding vía Ollama (nomic-embed-text). Síncrono a propósito: corre
    dentro del worker de la cola, no en el event loop de FastAPI."""
    r = httpx.post(
        f"{settings.ollama_url}/api/embeddings",
        json={"model": settings.ollama_embed_model, "prompt": texto},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["embedding"]


def _filtro(flujo: str, materia: str | None, dificultad: int | None) -> qm.Filter | None:
    must: list[qm.FieldCondition] = []
    if materia:
        must.append(qm.FieldCondition(key="materia", match=qm.MatchValue(value=materia)))
    if dificultad:
        # Recupera material de igual o menor dificultad (no spoilear con algo
        # más avanzado de lo que el usuario está trabajando).
        must.append(qm.FieldCondition(key="dificultad", range=qm.Range(lte=dificultad + 1)))
    must_not: list[qm.FieldCondition] = []
    if flujo == "EVALUACION":
        for tipo in TIPOS_PROHIBIDOS_EVALUACION:
            must_not.append(qm.FieldCondition(key="tipo_contenido", match=qm.MatchValue(value=tipo)))
    if not must and not must_not:
        return None
    return qm.Filter(must=must or None, must_not=must_not or None)


def _keywords(texto: str) -> set[str]:
    return {w for w in re.findall(r"[a-záéíóúñ0-9]{4,}", texto.lower())}


def _rerank(query: str, hits: list) -> list:
    """Reordena por (score vectorial) + bonus de solape de keywords."""
    qk = _keywords(query)
    rescored = []
    for h in hits:
        texto = h.payload.get("texto", "")
        solape = len(qk & _keywords(texto))
        bonus = min(solape * 0.02, 0.15)  # techo: el vector manda
        rescored.append((h.score + bonus, h))
    rescored.sort(key=lambda x: x[0], reverse=True)
    return [h for _, h in rescored]


def recuperar(query: str, flujo: str, materia: str | None = None,
              dificultad: int | None = None, top_k: int | None = None) -> list[dict]:
    """Devuelve una lista de chunks ya rerankeados y filtrados por política.
    Cada item: {texto, fuente, tema, tipo_contenido, score}."""
    if not query.strip():
        return []
    top_k = top_k or settings.rag_top_k
    vec = _embed(query)

    def _buscar(filtro):
        return _client.search(
            collection_name=COLLECTION, query_vector=vec,
            query_filter=filtro, limit=top_k * 3, with_payload=True,
        )

    hits = _buscar(_filtro(flujo, materia, dificultad))
    # Fallback semántico: si el filtro estricto no dio nada, relaja materia
    # y dificultad (pero NUNCA la exclusión de soluciones en EVALUACION).
    if not hits:
        hits = _buscar(_filtro(flujo, None, None))

    hits = _rerank(query, hits)[:top_k]

    salida = []
    for h in hits:
        p = h.payload
        # Segundo cinturón anti-fuga (en memoria), por si un chunk quedó mal
        # etiquetado en Qdrant.
        if flujo == "EVALUACION" and p.get("tipo_contenido") in TIPOS_PROHIBIDOS_EVALUACION:
            continue
        salida.append({
            "texto": p.get("texto", ""),
            "fuente": p.get("fuente", ""),
            "tema": p.get("tema", ""),
            "tipo_contenido": p.get("tipo_contenido", ""),
            "score": float(h.score),
        })
    return salida


def empaquetar_contexto(chunks: list[dict], token_budget: int | None = None) -> tuple[str, list[dict]]:
    """Concatena chunks hasta el presupuesto (~4 chars/token). Devuelve el
    texto y la lista de metadatos usados (para retrieved_context)."""
    budget = token_budget or settings.rag_context_token_budget
    char_budget = budget * 4
    usados, piezas, total = [], [], 0
    for c in chunks:
        t = c["texto"]
        if total + len(t) > char_budget:
            t = t[: max(0, char_budget - total)]
        if not t:
            break
        piezas.append(f"[{c['fuente']} · {c['tema'] or c['tipo_contenido']}]\n{t}")
        usados.append(c)
        total += len(t)
        if total >= char_budget:
            break
    return "\n\n---\n\n".join(piezas), usados
