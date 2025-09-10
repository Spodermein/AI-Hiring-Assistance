from app.core.nlp import chunk_resume, similarity
from app.services.utils import ats_checks

# --- Skills lexicon & helpers ---
_SYNONYMS: dict[str, set[str]] = {
    "html": {"html","html5"},
    "css": {"css","css3","tailwind","bootstrap"},
    "javascript": {"javascript","js","es6","ecmascript"},
    "typescript": {"typescript","ts"},
    "react": {"react","reactjs","react.js"},
    "angular": {"angular"},
    "vue": {"vue","vuejs","vue.js"},
    "node.js": {"node","nodejs","node.js"},
    "express": {"express","express.js"},
    "python": {"python"},
    "php": {"php"},
    "java": {"java"},
    "c#": {"c#","csharp","c-sharp"},
    "c++": {"c++"},
    "go": {"go","golang"},
    "rest": {"rest","restful"},
    "graphql": {"graphql"},
    "api": {"api","api development","api integration","web api"},
    "mysql": {"mysql"},
    "postgresql": {"postgresql","postgres","psql"},
    "mongodb": {"mongodb","mongo"},
    "sql": {"sql"},
    "nosql": {"nosql"},
    "git": {"git","github","gitlab"},
    "docker": {"docker"},
    "kubernetes": {"kubernetes","k8s"},
    "aws": {"aws","amazon web services"},
    "ci/cd": {"ci/cd","cicd","ci cd"}
}

_CANON_ORDER = list(_SYNONYMS.keys())

def _contains_any(text: str, variants: set[str]) -> bool:
    t = text.lower()
    return any(v in t for v in variants)

def _extract_required_skills(job_text: str) -> list[str]:
    required: list[str] = []
    for canon in _CANON_ORDER:
        if _contains_any(job_text, _SYNONYMS[canon]):
            required.append(canon)
    return required

def _present_skills_in_resume(required: list[str], resume_text: str) -> list[str]:
    present: list[str] = []
    for canon in required:
        if _contains_any(resume_text, _SYNONYMS[canon]):
            present.append(canon)
    return present

def analyze_texts(job_text: str, resume_text: str | None):
    if not resume_text:
        return {"error": "Missing resume text"}

    sections = chunk_resume(resume_text)
    sim_overall = similarity(resume_text, job_text)
    sim_skills  = similarity(sections.get("skills",""), job_text)
    sim_exp     = similarity(sections.get("experience",""), job_text)

    required = _extract_required_skills(job_text)
    present  = _present_skills_in_resume(required, resume_text)
    missing  = [k for k in required if k not in present]

    skills_cov    = (len(present) / max(1, len(required))) if required else 1.0
    section_align = (sim_skills + sim_exp) / 2

    W_OVERALL = 0.20
    W_SKILLS  = 0.55
    W_SECT    = 0.25

    base = (W_OVERALL*sim_overall) + (W_SKILLS*skills_cov) + (W_SECT*section_align)

    bonus = 0.0
    if required:
        if len(missing) == 0:
            bonus += 0.08
        elif skills_cov >= 0.85:
            bonus += 0.04

    overall = 100 * min(1.0, max(0.0, base + bonus))

    ats_score, ats_list = ats_checks(resume_text)

    return {
        "overallScore": round(overall),
        "similarity": {
            "overall": round(sim_overall,3),
            "experience": round(sim_exp,3),
            "skills": round(sim_skills,3)
        },
        "skills": {"required": required,"present": present,"missing": missing},
        "keywords": {"present": present,"suggested": missing},
        "atsHealth": {"score": ats_score,"checks": ats_list},
        "recommendations": _gen_recs(missing, sim_exp)
    }

def _gen_recs(missing: list[str], sim_exp: float) -> list[str]:
    recs = []
    if missing:
        recs.append(f"Consider learning or surfacing: {', '.join(missing)} (if you have experience).")
    if sim_exp < 0.7:
        recs.append("Map your bullets to the job responsibilities; mirror phrasing where accurate.")
    recs.append("Quantify bullets with impact metrics (%, ms, $, users).")
    return recs
