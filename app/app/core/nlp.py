from typing import List
import io
from PyPDF2 import PdfReader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
    _sbert = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
except Exception:
    _sbert = None

_tf = TfidfVectorizer(stop_words='english')

SECTION_HEADINGS = ["summary", "experience", "projects", "skills", "education"]

def extract_text_from_pdf(raw: bytes) -> str:
    reader = PdfReader(io.BytesIO(raw))
    return "\n".join((page.extract_text() or "") for page in reader.pages)

def _embed_sbert(texts: List[str]) -> np.ndarray:
    assert _sbert is not None
    return _sbert.encode(texts, normalize_embeddings=True)

def _embed_tfidf(texts: List[str]) -> np.ndarray:
    X = _tf.fit_transform(texts).toarray()
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    return X / norms

def embed(texts: List[str]) -> np.ndarray:
    if _sbert is not None:
        try:
            return _embed_sbert(texts)
        except Exception:
            pass
    return _embed_tfidf(texts)

def chunk_resume(resume_text: str) -> dict:
    text = resume_text.lower()
    sections = {k: "" for k in SECTION_HEADINGS}
    current = "summary"
    for line in text.splitlines():
        line_stripped = line.strip()
        if not line_stripped:
            continue
        for h in SECTION_HEADINGS:
            if line_stripped.startswith(h + ":") or line_stripped == h:
                current = h
                line_stripped = ""
                break
        if line_stripped:
            sections[current] += line + "\n"
    return sections

def similarity(a: str, b: str) -> float:
    emb = embed([a, b])
    return float(cosine_similarity([emb[0]], [emb[1]])[0][0])
