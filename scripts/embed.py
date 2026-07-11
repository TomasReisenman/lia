import json
import os
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

FAISS_DIR = Path(__file__).resolve().parent.parent / "faiss_store"
INDEX_PATH = FAISS_DIR / "faiss_index"
METADATA_PATH = FAISS_DIR / "metadata.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def build_template_description(data: dict) -> str:
    nombre_template = data.get("id", "template")

    def describe_value(v, indent=0):
        prefix = "  " * indent
        if isinstance(v, dict):
            return "\n".join(
                f"{prefix}  - {k}: {describe_value(v, indent + 1)}"
                for k, v in v.items()
            )
        if isinstance(v, list):
            parts = [f"{prefix}  - [{describe_value(item, indent + 1)}]" for item in v[:3]]
            return "\n".join(parts)
        return str(v)[:80]

    lines = [
        f"Template: {nombre_template}",
        "",
        "Campos del template:",
    ]
    for k, v in data.items():
        if k == "temas":
            continue
        lines.append(f"  - {k}: {describe_value(v)}")

    return "\n".join(lines)


def tema_chunk(tema: dict, fuente: str) -> dict:
    text = (
        f"Tema: {tema.get('nombre', '')}\n"
        f"Área: {tema.get('area', '')}\n"
        f"Nivel: {tema.get('nivel_dificultad', '')}\n"
        f"Descripción: {tema.get('descripcion_breve', '')}\n"
        f"Palabras clave: {', '.join(tema.get('palabras_clave', []))}\n"
        f"Subtemas relacionados: {', '.join(tema.get('subtemas_relacionados', []))}"
    )
    return {
        "text": text,
        "metadata": {
            "id": tema.get("id", ""),
            "tipo": "study_topic",
            "archivo": "study_themes",
            "nombre": tema.get("nombre", ""),
            "area": tema.get("area", ""),
            "nivel": tema.get("nivel_dificultad", ""),
            "tema": fuente,
        },
    }


def load_chunks(path: Path) -> list[dict]:
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    chunks = []
    for file_path in files:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        nombre = file_path.stem
        temas_list = data.get("temas")
        if isinstance(temas_list, list) and len(temas_list) > 0:
            for t in temas_list:
                chunks.append(tema_chunk(t, data.get("tema", "")))
        else:
            text = build_template_description(data)
            chunks.append({
                "text": text,
                "metadata": {
                    "id": data.get("id", nombre),
                    "tipo": "template",
                    "archivo": nombre,
                    "tema": data.get("tema", ""),
                },
            })
    return chunks


def embed(chunks: list[dict]) -> tuple[np.ndarray, list[dict]]:
    model = SentenceTransformer(MODEL_NAME)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    metadata = [c["metadata"] for c in chunks]
    return embeddings, metadata


def save(embeddings: np.ndarray, metadata: list[dict]) -> None:
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_PATH))
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Index saved: {INDEX_PATH} ({index.ntotal} vectors, dim={dim})")
    print(f"Metadata saved: {METADATA_PATH}")


def main():
    import sys as _sys
    if len(_sys.argv) < 2:
        print("Usage: python embed.py <path_to_json>")
        return
    path = Path(_sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        return
    chunks = load_chunks(path)
    if not chunks:
        print("No chunks found")
        return
    print(f"Loaded {len(chunks)} chunks")
    embeddings, metadata = embed(chunks)
    save(embeddings, metadata)


if __name__ == "__main__":
    main()
