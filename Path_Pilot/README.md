# Path_Pilot (Merged)

A clean, merged project that combines the best parts of `career-advisor-ai-base` (as the foundation) and `career-advisor-ai` (unique features), with duplicates removed and no login page.

## Structure

```
Path_Pilot/
  backend/
    app.py
    requirements.txt
    .env               # put your real keys here
    data/
      careers.json
  frontend/
    package.json
    package-lock.json
    public/
    src/
      App.jsx
      CareerAdvisorFrontend.jsx
      CareerAdvisorFrontend.css
      AssessmentPage.jsx
      Question.jsx
      RoadmapPage.jsx
      SuccessPage.jsx
      EntrepreneurHome.jsx
      ProgressTracker.jsx
      TestTailwind.jsx
      ai.jsx
      index.css
      App.css
      main.jsx
      assets/
```

## Backend

### 1) Configure environment
Create and edit `backend/.env`:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEN_MODEL=gemini-1.5-flash
```

> Do not commit real API keys.

### 2) Install dependencies
From `Path_Pilot/backend/`:

```
pip install -r requirements.txt
```

### 3) Run the server
From `Path_Pilot/backend/`:

```
python app.py
```

The server runs by default on `http://localhost:5000`.

### 4) Available endpoints
- `GET /` — health check
- `POST /recommend` — two modes:
  - Resume-based: `{ "resume": "..." }`
  - Profile-based: `{ name, education, interests[], skills[], constraints }`
- `POST /assessment` — generates questions and a brief roadmap for a given career
- `POST /evaluate` — generates a detailed learning roadmap
- `POST /get-startup-guidance` — startup mentor guidance
- `POST /get-role-roadmap` — skills + roadmap for a given role

Note: Profile-based recommendations use an embeddings search over `backend/data/careers.json`. If the dataset is missing, it gracefully degrades and still works with resume-based recommendations and other endpoints.

## Frontend

From `Path_Pilot/frontend/`:

```
npm install
npm run dev
```

Open the dev server URL from the terminal output.

### Routes
- `/` → `CareerAdvisorFrontend`
- `/assessment` → `AssessmentPage`
- `/evaluate` → `RoadmapPage`
- `/success` → `SuccessPage`
- `/home` → `EntrepreneurHome`
- `/progress-tracker` → `ProgressTracker`
- `/test` → `TestTailwind`
- `/ai` → `ai`

There is no login screen (removed by request).

## Notes
- Secrets are read from `.env`; no hardcoded API keys in code.
- Frontend base is from `career-advisor-ai-base` with unique components brought from `career-advisor-ai`.
- If you need to adjust the default model, set `GEN_MODEL` in `.env`.

## Next Steps (optional)
- Add CORS origin restrictions for production.
- Add simple integration tests for backend endpoints.
- Wire frontend API base URL via an env (e.g., Vite env vars) for different environments.
