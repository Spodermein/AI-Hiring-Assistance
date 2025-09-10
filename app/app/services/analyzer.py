from app.core.nlp import chunk_resume, similarity
from app.services.utils import ats_checks

def _extract_required_skills(job_text: str) -> list[str]:
    lines = [l.strip("-• ") for l in job_text.splitlines() if l.strip()]
    keywords: list[str] = []
    for l in lines:
        for token in ["python","fastapi","react","docker","postgresql","aws","kubernetes","ci/cd","go","java","ml"]:
            if token in l.lower() and token not in keywords:
                keywords.append(token)
    return keywords

def analyze_texts(job_text: str, resume_text: str | None):
    if not resume_text:
        return {"error": "Missing resume text"}
    resume_sections = chunk_resume(resume_text)
    sim_overall = similarity(resume_text, job_text)
    sim_skills = similarity(resume_sections.get("skills",""), job_text)
    sim_exp = similarity(resume_sections.get("experience",""), job_text)

    required = _extract_required_skills(job_text)
    present = [k for k in required if k in resume_text.lower()]
    missing = [k for k in required if k not in present]

    skills_cov = (len(present) / max(1, len(required)))
    section_align = (sim_skills + sim_exp) / 2

    overall = 100 * (0.5*sim_overall + 0.3*skills_cov + 0.2*section_align)

    health_score, health_checks = ats_checks(resume_text)

    return {
        "overallScore": round(overall),
        "similarity": {"overall": round(sim_overall,3), "experience": round(sim_exp,3), "skills": round(sim_skills,3)},
        "skills": {"required": required, "present": present, "missing": missing},
        "keywords": {"present": present, "suggested": missing},
        "atsHealth": {"score": health_score, "checks": health_checks},
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
