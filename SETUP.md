# PathPilot RAG System - Quick Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- OpenAI API key (get from https://platform.openai.com/api-keys)
- Pinecone API key (get from https://app.pinecone.io/)

---

## Step 1: Get API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

### Pinecone API Key
1. Go to https://app.pinecone.io/
2. Sign up for free account
3. Navigate to API Keys
4. Copy the API key
5. Note your environment (e.g., `us-east1-aws`)

---

## Step 2: Backend Setup

### Windows
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your API keys
notepad .env
```

### Mac/Linux
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### .env File Content
```env
OPENAI_API_KEY=sk-your-openai-key-here
PINECONE_API_KEY=your-pinecone-key-here
PINECONE_ENVIRONMENT=us-east1-aws
PINECONE_INDEX_NAME=pathpilot-careers
EMBEDDING_MODEL=text-embedding-3-small
GENERATION_MODEL=gpt-3.5-turbo
TOP_K=5
LOG_LEVEL=INFO
PORT=8000
```

---

## Step 3: Run Backend

```bash
# Make sure you're in the backend directory and venv is activated
python app.py
```

You should see:
```
INFO: Initializing PathPilot RAG System...
INFO: Configuration validated
INFO: Services initialized
INFO: Pinecone initialized
INFO: Starting data ingestion...
INFO: Loaded careers.json with 5 entries
...
INFO: PathPilot RAG System initialized successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Backend is now running at:** http://localhost:8000

**API Documentation:** http://localhost:8000/docs

---

## Step 4: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# (Optional) Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Run development server
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Frontend is now running at:** http://localhost:5173

---

## Step 5: Test the System

### Option 1: Use Swagger UI (Recommended for testing)
1. Open http://localhost:8000/docs
2. Click on `/api/v1/health` to verify system is running
3. Try `/api/v1/analyze-resume` endpoint
4. Fill in request body and click "Execute"

### Option 2: Use Frontend
1. Open http://localhost:5173/pilot
2. Upload a resume (PDF)
3. View career recommendations

### Option 3: Use curl
```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test resume analysis
curl -X POST http://localhost:8000/api/v1/analyze-resume \
  -H "Content-Type: application/json" \
  -d "{\"resume_text\": \"I am a software engineer with Python and JavaScript experience\"}"
```

---

## Troubleshooting

### Issue: "OPENAI_API_KEY is required"
**Solution:** Make sure your `.env` file has the correct API key and you restarted the server.

### Issue: "Pinecone initialization failed"
**Solution:** 
1. Verify Pinecone API key is correct
2. Check environment matches your Pinecone account
3. Ensure you have internet connection

### Issue: "Module not found" errors
**Solution:** Make sure you're running from the correct directory and virtual environment is activated.

### Issue: Frontend can't connect to backend
**Solution:** 
1. Verify backend is running on port 8000
2. Check `frontend/src/config.js` has correct API_URL
3. Check for CORS errors in browser console

### Issue: Slow response times
**Solution:** This is normal for first request (data ingestion). Subsequent requests will be faster.

---

## What to Expect

### First Run (Takes 2-3 minutes)
- System loads all datasets
- Generates embeddings for ~500 documents
- Uploads to Pinecone
- This is a one-time process

### Subsequent Runs
- System connects to existing Pinecone index
- Much faster startup (~10 seconds)
- Ready to serve requests immediately

---

## Next Steps

1. **Explore the API:** http://localhost:8000/docs
2. **Try example queries:** See `backend/examples/sample_queries_and_outputs.md`
3. **Run tests:** `pytest backend/tests/`
4. **Customize data:** Edit JSON files in `backend/data/`
5. **Deploy to production:** See deployment guides for FastAPI + React

---

## Need Help?

- Check the main README.md for detailed documentation
- Review example queries in `backend/examples/`
- Check FastAPI logs for error details
- Verify API keys are valid and have credits

---

**Enjoy exploring PathPilot! 🚀**
