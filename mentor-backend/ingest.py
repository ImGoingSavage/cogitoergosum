#!/usr/bin/env python3
"""ingest.py — Ingesta idempotente de Biblioteca/*.txt a Qdrant.

Uso:
    python ingest.py                 # ingesta incremental (idempotente)
    python ingest.py --recreate      # borra la colección y la reconstruye
    python ingest.py --file X.txt    # solo un archivo

CHUNKING: semántico-estructural, no por caracteres a ciegas. Se parte por
límites naturales (encabezados, líneas en blanco dobles, marcadores tipo
"Solución:", "Ejemplo:", "Teorema") y se clasifica cada chunk por su forma
(tipo_contenido). Idempotencia por hash SHA-256 del texto del chunk: el id en
Qdrant ES el hash, así que reingestar no duplica.

NOTA DE LICENCIA (leer README §0): los .txt son copias que cada usuario
adquirió y aportó. El corpus vive SOLO en la laptop local (Biblioteca/ y
qdrant_storage/ están en .gitignore: nunca al repo público). El sistema no
devuelve texto íntegro al usuario, solo síntesis del modelo: los chunks
alimentan el contexto, no la respuesta (garantía en app/main.py).
"""

import argparse
import hashlib
import logging
import re
import sys
import time
from pathlib import Path

import httpx
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ingest")

BIBLIOTECA = Path(__file__).parent.parent / "Biblioteca"
COLLECTION = settings.qdrant_collection

# --- Clasificación de materia por nombre de archivo (corpus real del repo) ---
MATEMATICAS = ("engel", "art and craft", "polya", "problem-solving", "problem solving")
def materia_de(nombre: str) -> str:
    n = nombre.lower()
    if any(k in n for k in MATEMATICAS):
        return "matematicas"
    return "ingenieria_ml"  # papers/libros de ML, sistemas, datos → Arena Fase 7


# --- Marcadores que delatan el tipo de contenido de un chunk ---
_MARCADORES = [
    (re.compile(r"^\s*(soluci[oó]n|solution)\b", re.I), "solucion"),
    (re.compile(r"^\s*(pista|hint)\b", re.I), "pista"),
    (re.compile(r"^\s*(ejemplo|example)\b", re.I), "ejemplo"),
    (re.compile(r"^\s*(contraejemplo|counterexample)\b", re.I), "contraejemplo"),
    (re.compile(r"^\s*(teorema|theorem|definici[oó]n|definition|lema|lemma)\b", re.I), "teoria"),
    (re.compile(r"^\s*(problema|problem|ejercicio|exercise)\b", re.I), "enunciado"),
    (re.compile(r"```|def |class |import |#include", re.I), "codigo"),
]
def tipo_de(texto: str) -> str:
    cabeza = texto[:120]
    for rx, tipo in _MARCADORES:
        if rx.search(cabeza) or rx.search(texto[:400]):
            return tipo
    return "teoria"


def trocear(texto: str, max_chars: int = 1400, min_chars: int = 250) -> list[str]:
    """Parte por dobles saltos de línea (párrafos/secciones) y reagrupa hasta
    max_chars sin partir un párrafo. Acumula los muy cortos."""
    bloques = re.split(r"\n\s*\n", texto)
    chunks, buf = [], ""
    for b in bloques:
        b = b.strip()
        if not b:
            continue
        if len(buf) + len(b) + 2 <= max_chars:
            buf = f"{buf}\n\n{b}" if buf else b
        else:
            if buf:
                chunks.append(buf)
            # un bloque gigante (página sin saltos) se corta por oraciones
            if len(b) > max_chars:
                chunks.extend(_cortar_largo(b, max_chars))
                buf = ""
            else:
                buf = b
    if buf:
        chunks.append(buf)
    return [c for c in chunks if len(c) >= min_chars]


def _cortar_largo(texto: str, max_chars: int) -> list[str]:
    oraciones = re.split(r"(?<=[.!?])\s+", texto)
    out, buf = [], ""
    for o in oraciones:
        if len(buf) + len(o) + 1 <= max_chars:
            buf = f"{buf} {o}".strip()
        else:
            if buf:
                out.append(buf)
            buf = o
    if buf:
        out.append(buf)
    return out


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _id_qdrant(h: str) -> str:
    # Qdrant acepta UUID o int como id; derivamos un UUID determinista del hash.
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def _embed(texto: str) -> list[float]:
    r = httpx.post(f"{settings.ollama_url}/api/embeddings",
                   json={"model": settings.ollama_embed_model, "prompt": texto},
                   timeout=60)
    r.raise_for_status()
    return r.json()["embedding"]


def asegurar_coleccion(client: QdrantClient, recreate: bool) -> None:
    existe = client.collection_exists(COLLECTION)
    if existe and recreate:
        client.delete_collection(COLLECTION)
        existe = False
    if not existe:
        client.create_collection(
            COLLECTION,
            vectors_config=qm.VectorParams(size=settings.embed_dim, distance=qm.Distance.COSINE),
        )
        # Índices de payload para que los filtros sean O(log n), no scan.
        for campo in ("materia", "tema", "tipo_contenido"):
            client.create_payload_index(COLLECTION, campo, qm.PayloadSchemaType.KEYWORD)
        client.create_payload_index(COLLECTION, "dificultad", qm.PayloadSchemaType.INTEGER)
        log.info("Colección %s creada con índices de payload", COLLECTION)


def ids_existentes(client: QdrantClient) -> set[str]:
    """Lee los ids ya presentes (idempotencia sin reembeber)."""
    vistos, offset = set(), None
    while True:
        puntos, offset = client.scroll(COLLECTION, limit=1000, offset=offset,
                                       with_payload=False, with_vectors=False)
        vistos.update(p.id for p in puntos)
        if offset is None:
            break
    return vistos


def ingestar_archivo(client: QdrantClient, path: Path, ya: set[str]) -> tuple[int, int]:
    texto = path.read_text(encoding="utf-8", errors="replace")
    materia = materia_de(path.name)
    nuevos, saltados = [], 0
    for idx, chunk in enumerate(trocear(texto)):
        h = _hash(chunk)
        pid = _id_qdrant(h)
        if pid in ya:
            saltados += 1
            continue
        payload = {
            "texto": chunk,
            "materia": materia,
            "tema": path.stem[:80],
            "subtema": "",
            "dificultad": 3,
            "tipo_contenido": tipo_de(chunk),
            "fuente": path.name,
            "capitulo": "",
            "chunk_index": idx,
            "hash": h,
            "version": "v1",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        nuevos.append(qm.PointStruct(id=pid, vector=_embed(chunk), payload=payload))
        ya.add(pid)
        if len(nuevos) >= 64:  # subidas por lotes (RAM y red)
            client.upsert(COLLECTION, points=nuevos)
            nuevos = []
    if nuevos:
        client.upsert(COLLECTION, points=nuevos)
    return len(ya), saltados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recreate", action="store_true")
    ap.add_argument("--file", default=None)
    args = ap.parse_args()

    if not BIBLIOTECA.exists():
        log.error("No existe %s — nada que ingestar.", BIBLIOTECA)
        sys.exit(1)

    client = QdrantClient(url=settings.qdrant_url, timeout=30)
    asegurar_coleccion(client, args.recreate)
    ya = set() if args.recreate else ids_existentes(client)

    archivos = ([BIBLIOTECA / args.file] if args.file
                else sorted(BIBLIOTECA.glob("*.txt")))
    total_nuevos = total_saltados = errores = 0
    for path in archivos:
        if not path.exists():
            log.warning("No existe %s, lo salto", path.name)
            continue
        try:
            antes = len(ya)
            _, saltados = ingestar_archivo(client, path, ya)
            nuevos = len(ya) - antes
            total_nuevos += nuevos
            total_saltados += saltados
            log.info("%-55s +%4d nuevos · %4d ya estaban", path.name[:55], nuevos, saltados)
        except Exception as e:  # noqa: BLE001 — un archivo roto no aborta todo
            errores += 1
            log.error("FALLÓ %s: %s", path.name, e)

    log.info("LISTO. nuevos=%d saltados=%d archivos_con_error=%d total_en_coleccion=%d",
             total_nuevos, total_saltados, errores, len(ya))


if __name__ == "__main__":
    main()
