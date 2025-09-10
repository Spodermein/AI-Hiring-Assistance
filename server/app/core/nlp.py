import re
import io
from PyPDF2 import PdfReader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

SECTION_HEADINGS = ["summary","experience","projects","skills","education"]

_HEADING_ALIASES = {
    "summary": [r"summary", r"profile", r"professional summary"],
    "experience": [r"experience", r"work experience", r"employment history", r"professional experience"],
    "projects": [r"projects", r"selected projects"],
    "skills": [r"skills", r"technical skills", r"tech skills", r"technologies"],
    "education": [r"education", r"qualifications"],
}
_ALIAS_PATTERNS = {k: re.compile(rf"^\s*(?:{'|'.join(v)})\s*:?\s*$", re.I) for k,v in _HEADING_ALIASES.items()}

def extract_text_from_pdf(raw: bytes) -> str:
    reader = PdfReader(io.BytesIO(raw))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def embed(texts: list[str]) -> np.ndarray:
    return _model.encode(texts, normalize_embeddings=True)

def chunk_resume(resume_text: str) -> dict:
    sections = {k: "" for k in SECTION_HEADINGS}
    current = "summary"
    for raw in resume_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        matched = False
        for key, pat in _ALIAS_PATTERNS.items():
            if pat.match(line):
                current = key
                matched = True
                break
        if not matched:
            sections[current] += raw + "\n"
    return sections

def similarity(a: str, b: str) -> float:
    if not a.strip() or not b.strip():
        return 0.0
    emb = embed([a,b])
    return float(cosine_similarity([emb[0]], [emb[1]])[0][0])
