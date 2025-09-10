HireSight — AI Resume & Job Match Analyzer

Upload a resume + job description → instantly get a match score, skill gap analysis, ATS health check, and bullet rewrites.
A project designed to impress recruiters by blending AI, full-stack engineering, and UX polish.

🚀 Features

Match Score (0–100) combining semantic similarity, skills coverage, and section alignment

Skill Extraction: detects required vs present vs missing skills with synonym/alias matching

ATS Health: checks for contact info, section headings, bullet length, action verbs, numbers, and formatting issues

Resume Rewrites: quantifies bullets with metrics and relevant keywords

Interactive UI: real-time score dial, coverage lists, ATS checklist, and actionable recommendations

🧱 Architecture
client/ (React + Vite + TypeScript)
  src/
    components/UploadPanel.tsx
    components/ResultsPane.tsx
    lib/api.ts
    App.tsx

server/ (FastAPI + ML models)
  app/
    api/routes.py
    core/nlp.py
    services/analyzer.py
    services/utils.py
    main.py
  requirements.txt

infra/
  docker-compose.yml
  Dockerfile.server
  Dockerfile.client


Data flow

Frontend sends { resumeText, jobText } → /analyze

Backend parses, embeds with sentence-transformers/all-MiniLM-L6-v2 (or OpenAI embeddings), compares skills & sections

Returns JSON with score, gaps, ATS checks, and recommendations

Frontend renders charts + lists

🧠 AI Layer

Embeddings: sentence-transformers/all-MiniLM-L6-v2 (local) or text-embedding-3-large (OpenAI)

Similarity: cosine similarity (scikit-learn)

ATS: regex & heuristics

Skill extraction: regex + curated synonym sets (HTML ↔ HTML5, CSS ↔ CSS3, Node ↔ Node.js, etc.)

⚙️ Quickstart
Backend
cd server
python -m venv .venv
.venv\Scripts\activate   # (Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir .


API available at: http://127.0.0.1:8000/docs

Frontend
cd client
npm install
npm run dev


Frontend runs at: http://localhost:5173

Create client/.env with:

VITE_API_URL=http://127.0.0.1:8000

📸 Screenshots

Resume ↔ JD Analysis → Score & Missing Skills

ATS Health Checklist

Resume Bullet Rewrites

(Add screenshots or GIF here)

🧪 Tests

Backend tests with Pytest:

pytest server/tests

📦 Tech Stack

Backend: FastAPI, scikit-learn, sentence-transformers, PyPDF2, NumPy

Frontend: React, Vite, TypeScript, Tailwind

Infra: Docker, AWS EC2 + Netlify deployment

📈 Resume Bullets (for your CV)

Built HireSight, an AI-powered resume ↔ job matcher (React + FastAPI + embeddings) delivering explainable match scores, ATS checks, and tailored bullet rewrites

Implemented local & cloud embedding backends; designed a weighted scoring model combining semantic similarity, skills coverage, and section alignment

Shipped Dockerized services, CI tests, and a polished UX with actionable suggestions; deployed on AWS EC2 + Netlify