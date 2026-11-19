# PathPilot

[![Live Demo](https://img.shields.io/badge/Live-path--pilot--ashy.vercel.app-brightgreen.svg)](https://path-pilot-ashy.vercel.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4.svg)](https://ai.google.dev/)
[![React](https://img.shields.io/badge/React-Vite-61DAFB.svg)](https://vitejs.dev/)

**Live app:** [https://path-pilot-ashy.vercel.app](https://path-pilot-ashy.vercel.app)

**PathPilot** is a Retrieval-Augmented Generation (RAG) system for career guidance, startup validation, and financial insights. The React frontend is deployed on Vercel. The FastAPI backend uses the Google Gemini API (`google-genai`) and an in-memory NumPy cosine-similarity index — no OpenAI or Pinecone account required.

---

## Project Overview

PathPilot turns a standard LLM assistant into a grounded RAG pipeline:

- Semantic retrieval over career, startup, and financial datasets
- Structured prompt engineering with JSON outputs
- Evaluation of RAG vs. no-retrieval baseline
- Modular backend (ingestion → embeddings → store → retrieve → generate)
- Gemini embeddings (`gemini-embedding-001`) and chat (`gemini-3.5-flash-lite` by default)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              FRONTEND (React + Vite)                 │
│  Live: https://path-pilot-ashy.vercel.app            │
│  Career advisor · Roadmaps · Startup · Finance       │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/REST  (VITE_API_URL)
┌──────────────────────▼──────────────────────────────┐
│              BACKEND (FastAPI)                       │
│                                                      │
│  ┌────────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Ingestion  │→ │Embedding │→ │ Vector Store │   │
│  │  Module    │  │ (Gemini) │  │ (NumPy RAM)  │   │
│  └────────────┘  └──────────┘  └──────┬───────┘   │
│                                        │            │
│  ┌────────────┐  ┌──────────┐  ┌──────▼───────┐   │
│  │Evaluation  │← │Generation│← │  Retrieval   │   │
│  │            │  │ (Gemini) │  │              │   │
│  └────────────┘  └──────────┘  └──────────────┘   │
│                                                      │
│           Google Gemini API (AI Studio key)          │
└─────────────────────────────────────────────────────┘
```

---

## RAG Pipeline

1. **Ingestion** — JSON datasets are chunked by semantic units (overview, skills, roadmap phases) and tagged with metadata.
2. **Embeddings** — Chunks are embedded with `gemini-embedding-001` (3072-dim by default) via `google-genai`.
3. **Vector store** — IDs, embeddings, and metadata live in memory. Search uses NumPy cosine similarity and `$in` metadata filters.
4. **Retrieval** — The user query is embedded, top-k neighbors are fetched (optionally filtered by domain), and context is assembled.
5. **Generation** — Gemini `generate_content` produces structured JSON (`response_mime_type=application/json`).
6. **Evaluation** — RAG answers are scored against a no-retrieval baseline (relevance, completeness, context usage, specificity, accuracy).

---

## Project Structure

```
Path_Pilot/
├── backend/
│   ├── app.py                      # FastAPI app (binds 0.0.0.0, PORT)
│   ├── config.py                   # Env-based configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # GEMINI_API_KEY and related vars
│   ├── data/                       # careers, startups, financial, resources
│   ├── modules/
│   │   ├── ingestion.py            # Loading & chunking
│   │   ├── embeddings.py           # Gemini embeddings
│   │   ├── vector_store.py         # In-memory NumPy cosine index
│   │   ├── retriever.py            # Search & context assembly
│   │   └── generator.py            # Gemini generation
│   ├── utils/
│   │   ├── prompt_templates.py
│   │   └── json_parser.py
│   └── tests/
│       └── test_modules.py
├── frontend/
│   └── src/
│       ├── config.js               # VITE_API_URL (fallback localhost:5000)
│       ├── App.jsx
│       └── ...
└── README.md
```

---

## Live Demo

| Surface | URL |
|---------|-----|
| **Frontend (Vercel)** | [https://path-pilot-ashy.vercel.app](https://path-pilot-ashy.vercel.app) |

Point the frontend at a running backend with `VITE_API_URL` (no trailing slash), for example your Render service URL.

---

## Quick Start (local)

### Prerequisites

- Python 3.9+
- Node.js 16+
- A free [Google AI Studio](https://aistudio.google.com/apikey) API key (`GEMINI_API_KEY`)

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Set GEMINI_API_KEY in .env

python app.py
# listens on http://0.0.0.0:5000  (or $PORT)
```

Swagger UI: `http://localhost:5000/docs`

Alternatively:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 5000
```

### Frontend

```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:5000" > .env
npm run dev
```

App: `http://localhost:5173`

---

## API Endpoints

Base path: `/api/v1`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Status, models, index stats |
| POST | `/analyze-resume` | Career recommendations from resume text |
| POST | `/career-roadmap` | Phase-by-phase learning plan |
| POST | `/startup-guidance` | Startup advice from project details |
| POST | `/financial-insights` | Market / stock analysis |
| POST | `/evaluate` | Assessment-based roadmap |
| POST | `/evaluate-rag` | RAG vs baseline comparison |
| GET | `/index-stats` | In-memory index statistics |

### Resume analysis

```http
POST /api/v1/analyze-resume
Content-Type: application/json

{
  "resume_text": "I have 2 years experience in Python and data analysis..."
}
```

### Career roadmap

```http
POST /api/v1/career-roadmap
Content-Type: application/json

{
  "role": "Machine Learning Engineer",
  "current_skills": ["Python", "Statistics"],
  "experience_level": "beginner"
}
```

### Startup guidance

```http
POST /api/v1/startup-guidance
Content-Type: application/json

{
  "project_details": {
    "name": "AI Tutor",
    "description": "AI-powered personalized tutoring platform",
    "goals": "Reach 1000 users in 6 months"
  },
  "current_stage": "Idea Validation",
  "challenges": ["Market research", "Technical feasibility"]
}
```

### Financial insights

```http
POST /api/v1/financial-insights
Content-Type: application/json

{
  "query": "What are the best tech stocks for long-term investment?",
  "stock_symbol": "AAPL"
}
```

CORS is enabled for all origins so the Vercel frontend can call a hosted backend.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google AI Studio API key | Yes | — |
| `GEMINI_CHAT_MODEL` | Chat model | No | `gemini-3.5-flash-lite` |
| `GEMINI_EMBEDDING_MODEL` | Embedding model | No | `gemini-embedding-001` |
| `TOP_K` | Retrieved neighbors | No | `5` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `PORT` | Listen port (Render sets this) | No | `5000` when using `python app.py` |

### Frontend (`frontend/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend origin, no trailing slash | Yes in production (Vercel). Local fallback: `http://localhost:5000` |

---

## Deployment

### Frontend (Vercel) — live

- **URL:** [https://path-pilot-ashy.vercel.app](https://path-pilot-ashy.vercel.app)
- Set `VITE_API_URL` in Vercel project settings to your backend URL.
- Rebuild after changing `VITE_API_URL` (Vite inlines it at build time).

### Backend (Render, free tier)

- **Root directory:** `backend`
- **Build command:** `pip install -r requirements.txt`
- **Start command:**
  ```text
  gunicorn app:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 180 --workers 1
  ```
- **Env vars:** `GEMINI_API_KEY` (required). Use **one worker** so the in-memory index built at startup stays in that process.

---

## Testing

```bash
cd backend
pytest tests/ -v
```

```bash
curl -X POST http://localhost:5000/api/v1/analyze-resume \
  -H "Content-Type: application/json" \
  -d "{\"resume_text\": \"I am a software engineer with 3 years experience...\"}"
```

---

## Knowledge Base

- **Careers** — 50+ roles with skills, roadmaps, resources, salary ranges
- **Startups** — SaaS / e-commerce / fintech frameworks, stages, case studies
- **Finance** — sample stocks, strategies, analysis frameworks
- **Learning resources** — courses, docs, and videos used in generated plans

---

## License

MIT License.

## Author

M Gowthami  
IIITDM Jabalpur

---

**Try it live:** [https://path-pilot-ashy.vercel.app](https://path-pilot-ashy.vercel.app)
