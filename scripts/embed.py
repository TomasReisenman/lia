import json
import os
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INFO_DIR = Path(__file__).resolve().parent.parent / "info"
FAISS_DIR = Path(__file__).resolve().parent.parent / "faiss_store"
INDEX_PATH = FAISS_DIR / "faiss_index"
METADATA_PATH = FAISS_DIR / "metadata.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


TEMPLATE_SCHEMA = {
    "multiple_choise_template": {
        "id": "Identificador único de la pregunta (ej: mc_0001)",
        "tema": "Tema principal del que trata la pregunta",
        "subtema": "Subtema específico dentro del tema",
        "nivel_dificultad": "Nivel: basico, intermedio o avanzado",
        "tags": ["Lista de etiquetas o palabras clave"],
        "enunciado": "Texto del enunciado de la pregunta",
        "opciones": [
            {"id": "Letra identificadora (A, B, C, D)", "texto": "Texto de la opción"}
        ],
        "respuesta_correcta": "Letra de la opción correcta (ej: A)",
        "explicacion": "Explicación detallada de por qué esa es la respuesta correcta",
        "distractores_justificacion": {
            "B": "Justificación de por qué la opción B es incorrecta",
            "C": "Justificación de por qué la opción C es incorrecta",
            "D": "Justificación de por qué la opción D es incorrecta"
        },
        "fuente": "Fuente de información del contenido",
        "metadata": {
            "idioma": "es",
            "formato_pregunta": "seleccion_unica",
            "num_opciones": 4,
            "fecha_creacion": "Fecha de creación",
            "autor": "Nombre del autor"
        }
    }
}


def build_template_description(data: dict) -> str:
    nombre_template = data.get("id", "template")
    formato = data.get("metadata", {}).get("formato_pregunta", "multiple_choice")
    num_opciones = data.get("metadata", {}).get("num_opciones", 4)

    lines = [
        f"Template: {nombre_template}",
        f"Tipo: {formato}",
        f"Número de opciones: {num_opciones}",
        "",
        "Campos del template:",
    ]
    for campo, descripcion in TEMPLATE_SCHEMA.get("multiple_choise_template", {}).items():
        lines.append(f"  - {campo}: {descripcion}")

    return "\n".join(lines)


def load_chunks(info_dir: Path) -> list[dict]:
    chunks = []
    for file_path in sorted(info_dir.glob("*.json")):
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        text = build_template_description(data)
        nombre = file_path.stem
        chunks.append({
            "text": text,
            "metadata": {
                "id": data.get("id", nombre),
                "tipo": "template",
                "archivo": nombre,
                "formato": data.get("metadata", {}).get("formato_pregunta", "multiple_choice"),
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
    chunks = load_chunks(INFO_DIR)
    if not chunks:
        print("No chunks found in info/")
        return
    print(f"Loaded {len(chunks)} chunks")
    embeddings, metadata = embed(chunks)
    save(embeddings, metadata)


if __name__ == "__main__":
    main()
