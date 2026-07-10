import json
from pathlib import Path

import faiss
import numpy as np
from google.adk.tools import ToolContext
from sentence_transformers import SentenceTransformer

FAISS_DIR = Path(__file__).resolve().parent / "faiss_store"
INDEX_PATH = FAISS_DIR / "faiss_index"
METADATA_PATH = FAISS_DIR / "metadata.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

_model = None
_index = None
_metadata = None


def _load():
    global _model, _index, _metadata
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    if _index is None:
        _index = faiss.read_index(str(INDEX_PATH))
    if _metadata is None:
        with open(METADATA_PATH, encoding="utf-8") as f:
            _metadata = json.load(f)


def search_templates(query: str, k: int = 3) -> list[dict]:
    """Search for templates similar to the query.

    Args:
        query: What kind of exercise template to look for (e.g. "multiple choice question")
        k: Number of results to return

    Returns:
        list of dicts with 'score' and 'metadata' keys
    """
    _load()
    query_vec = _model.encode([query], normalize_embeddings=True)
    scores, indices = _index.search(query_vec, k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "score": float(score),
            "metadata": _metadata[idx],
        })
    return results


def save_exercise_data(
    title: str,
    question: str,
    options: str,
    correct_answer: str,
    explanation: str,
    tool_context: ToolContext,
) -> dict:
    """Save exercise data to session state for later correction.

    Args:
        title: Title or topic of the exercise
        question: The exercise question text
        options: The available options (formatted as text)
        correct_answer: The correct answer identifier (e.g. "A")
        explanation: Explanation of why it's correct
    """
    tool_context.state["exercise_title"] = title
    tool_context.state["exercise_question"] = question
    tool_context.state["exercise_options"] = options
    tool_context.state["exercise_correct_answer"] = correct_answer
    tool_context.state["exercise_explanation"] = explanation
    return {"status": "saved"}


def get_exercise_data(tool_context: ToolContext) -> dict:
    """Get exercise data from session state for correction.

    Returns:
        dict with title, question, options, correct_answer, explanation
    """
    return {
        "title": tool_context.state.get("exercise_title", ""),
        "question": tool_context.state.get("exercise_question", ""),
        "options": tool_context.state.get("exercise_options", ""),
        "correct_answer": tool_context.state.get("exercise_correct_answer", ""),
        "explanation": tool_context.state.get("exercise_explanation", ""),
    }
