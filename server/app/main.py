from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(title="HireSight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.get("/version")
def version():
    return {"impl":"skills-synonyms+aliases+reweight","ts":"2025-09-07"}

@app.post("/diagnostics")
def diagnostics(payload: dict):
    from app.services.analyzer import _extract_required_skills,_present_skills_in_resume
    from app.core.nlp import chunk_resume
    jd = payload.get("jobText","")
    rs = payload.get("resumeText","")
    req = _extract_required_skills(jd)
    have = _present_skills_in_resume(req, rs)
    miss = [k for k in req if k not in have]
    secs = chunk_resume(rs)
    return {"required":req,"present":have,"missing":miss,"sections":{k:len(v) for k,v in secs.items()}}
