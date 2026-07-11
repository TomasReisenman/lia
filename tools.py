import json
import re
import urllib.request
from html.parser import HTMLParser
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


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._text.append(data)

    def get_text(self) -> str:
        return re.sub(r'\s+', ' ', ' '.join(self._text)).strip()


def fetch_url(url: str) -> str:
    """Fetch the content of a URL and return it as plain text.

    Args:
        url: The URL to fetch (must start with http:// or https://)

    Returns:
        The text content of the URL with HTML tags stripped
    """
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    stripper = _HTMLStripper()
    stripper.feed(raw)
    text = stripper.get_text()
    max_chars = 8000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[Contenido truncado...]"
    return text


def save_summary(url: str, title: str, summary: str, tool_context: ToolContext) -> dict:
    """Save a URL summary to session state for later use by other agents.

    Args:
        url: The original URL
        title: Title of the page
        summary: The summary text
    """
    tool_context.state["last_url"] = url
    tool_context.state["last_url_title"] = title
    tool_context.state["last_url_summary"] = summary
    return {"status": "saved"}


def get_summary(tool_context: ToolContext) -> dict:
    """Get the last saved URL summary from session state.

    Returns:
        dict with url, title, summary
    """
    return {
        "url": tool_context.state.get("last_url", ""),
        "title": tool_context.state.get("last_url_title", ""),
        "summary": tool_context.state.get("last_url_summary", ""),
    }
