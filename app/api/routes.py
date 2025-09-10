from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from app.services.analyzer import analyze_texts
from app.core.nlp import extract_text_from_pdf

router = APIRouter()

class AnalyzeReq(BaseModel):
    jobText: str
    resumeText: str | None = None

@router.post("/analyze")
async def analyze(req: AnalyzeReq):
    return analyze_texts(job_text=req.jobText, resume_text=req.resumeText)

@router.post("/analyze-file")
async def analyze_file(jobText: str = Form(...), resumeFile: UploadFile = File(...)):
    raw = await resumeFile.read()
    text = extract_text_from_pdf(raw)
    return analyze_texts(job_text=jobText, resume_text=text)
