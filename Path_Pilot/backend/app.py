# backend/app.py
import os
import json
import numpy as np
import logging
import re
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

import google.generativeai as genai

# ---------- Setup logging ----------
logging.basicConfig(level=logging.INFO)

# ---------- Load environment ----------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------- Config ----------
GEN_MODEL = os.getenv("GEN_MODEL", "gemini-1.5-flash")     # generation model
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-004")  # embeddings model
TOP_K = int(os.getenv("TOP_K", 3))
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "careers.json")

# ---------- Init Gemini ----------
genai.configure(api_key=GEMINI_API_KEY)

# Normalize model id if users passed a display name
def _normalize_model(m: str) -> str:
    m = (m or "").strip()
    # Accept either "gemini-1.5-flash" or "models/gemini-1.5-flash"
    if m and not m.startswith("models/"):
        return f"models/{m}"
    return m or "models/gemini-1.5-flash"

GEN_MODEL = _normalize_model(GEN_MODEL)
gen_model = genai.GenerativeModel(GEN_MODEL)

# Simple retry helper for transient errors
MAX_RETRIES = int(os.getenv("GEN_RETRIES", 3))
RETRY_BACKOFF = float(os.getenv("GEN_RETRY_BACKOFF", 1.5))

def _retry(fn, *args, **kwargs):
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_err = e
            # Log and backoff on transient network/service issues
            logging.warning(f"GenAI call failed (attempt {attempt}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF ** attempt)
    raise last_err

# ---------- Load dataset ----------
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        careers = json.load(f)
    
    career_texts = [
        f"{c.get('title','')}. {c.get('summary','')} Skills: {', '.join(c.get('skills',[]))}"
        for c in careers
    ]
    career_meta = careers
    
    # ---------- Pre-compute dataset embeddings ----------
    print("⚡ Generating embeddings for career dataset...")
    
    def get_embeddings(texts):
        is_single = False
        if isinstance(texts, str):
            texts = [texts]
            is_single = True

        resp = _retry(
            genai.embed_content,
            model=EMBED_MODEL,
            content=texts
        )

        embeddings = []
        if isinstance(resp, dict):
            if "embedding" in resp:
                embeddings.append(np.array(resp["embedding"], dtype=np.float32))
            elif "embeddings" in resp:
                for e in resp["embeddings"]:
                    embeddings.append(np.array(e, dtype=np.float32))
            else:
                raise RuntimeError("Unexpected embeddings response: " + str(resp))
        else:
            emb = getattr(resp, "embedding", None)
            if emb is None:
                raise RuntimeError("Unexpected response type: " + str(resp))
            embeddings.append(np.array(emb, dtype=np.float32))

        arr = np.vstack(embeddings)
        return arr[0] if is_single else arr
    
    try:
        career_embeddings = get_embeddings(career_texts)
        print("✅ Career embeddings shape:", career_embeddings.shape)
    except Exception as e:
        logging.error(f"Failed to precompute embeddings (continuing without DB): {e}")
        career_embeddings = None
    
except FileNotFoundError:
    print("⚠️ Career dataset not found. Some features may not work.")
    careers = []
    career_texts = []
    career_meta = []
    career_embeddings = None

# ---------- Helper functions ----------
def try_parse_json(text):
    """Helper function to parse potentially messy JSON"""
    text = text.strip()
    # Try to find the first '{' or '[' and last '}' or ']'
    match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
    if match:
        json_string = match.group(0)
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            pass
    return None

def top_k_similar(query_emb, k=3):
    """Similarity search function"""
    if career_embeddings is None:
        return [], []
        
    def normalize(x):
        norms = np.linalg.norm(x, axis=1, keepdims=True) + 1e-10
        return x / norms

    A = normalize(career_embeddings)
    qn = query_emb / (np.linalg.norm(query_emb) + 1e-10)
    sims = (A @ qn.reshape(-1, 1)).squeeze()
    idx = np.argsort(-sims)[:k]
    return idx, sims[idx].tolist()

def generate_with_gemini(prompt, max_output_tokens=700, temperature=0.2):
    """Text generation with Gemini with retries"""
    resp = _retry(
        gen_model.generate_content,
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        },
    )
    return resp.text.strip()

# ---------- Flask app ----------
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health():
    return {"status": "ok", "model": GEN_MODEL}

@app.route("/recommend", methods=["POST"])
def recommend():
    """Enhanced recommendation endpoint supporting both profile-based and resume-based recommendations"""
    req = request.get_json(force=True)
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "GEMINI_API_KEY is not configured on the server",
            "hint": "Set GEMINI_API_KEY in your Vercel project Environment Variables and redeploy"
        }), 500
    
    # Check if it's resume-based or profile-based
    resume_text = req.get("resume", "")
    if resume_text:
        # Resume-based recommendation (from career-advisor-ai-base)
        # Use centralized model
        model = gen_model
        
        prompt = f"""
        Analyze this resume and suggest exactly 5 career paths.
        Return STRICTLY valid JSON in this format:
        [
          {{
            "title": "Career Title",
            "rank": 1,
            "why_fit": [
              "Reason 1",
              "Reason 2",
              "Reason 3"
            ]
          }},
          ...
        ]
        Resume: {resume_text}
        """
        
        try:
            response = _retry(model.generate_content, prompt)
            recommendations = try_parse_json(response.text)
            if recommendations is None:
                raise ValueError("Failed to parse AI response into JSON.")
            return jsonify({"recommendations": recommendations})
        except Exception as e:
            logging.error(f"Error generating recommendations: {e}")
            return jsonify({"error": "Failed to generate recommendations. Please try again.", "details": str(e)}), 500
    
    else:
        # Profile-based recommendation (from career-advisor-ai)
        profile_text = (
            f"Name: {req.get('name','')}\n"
            f"Education: {req.get('education','')}\n"
            f"Interests: {', '.join(req.get('interests',[]))}\n"
            f"Skills: {', '.join(req.get('skills',[]))}\n"
            f"Constraints: {req.get('constraints','')}\n"
        )

        # Step 1: Embed user profile
        try:
            if career_embeddings is not None:
                q_emb = get_embeddings(profile_text)
                # Step 2: Retrieve similar careers
                idxs, sims = top_k_similar(q_emb, k=TOP_K)
                retrieved = []
                for i, s in zip(idxs, sims):
                    item = career_meta[i].copy()
                    item["_score"] = float(s)
                    retrieved.append(item)

                retrieved_text = "".join(
                    f"- {r['title']}: {r['summary']}\n  Skills: {', '.join(r.get('skills',[]))}\n"
                    for r in retrieved
                )
            else:
                retrieved_text = "No career database available."
        except Exception as e:
            return jsonify({"ok": False, "error": f"Embedding error: {str(e)}"}), 500

        # Step 3: Build structured prompt
        prompt = f"""You are an empathetic career advisor for students in India.
Given the USER PROFILE and RETRIEVED CAREER CONTEXT, return a JSON object with key 'recommendations' (up to 3 careers). 

Each career must include:
 - title
 - rank (1 = best)
 - why_fit (2 short bullets)
 - required_skills (beginner→intermediate, each with 1 practical task)
 - resources (3 items: title + url)
 - 90_day_plan (weekly milestones for 12 weeks)

USER PROFILE:
{profile_text}

RETRIEVED CAREER CONTEXT:
{retrieved_text}

Return ONLY valid JSON.
"""

        try:
            gen_text = generate_with_gemini(prompt)
        except Exception as e:
            return jsonify({"ok": False, "error": f"Generation error: {str(e)}"}), 500

        # Try parsing JSON
        parsed_json = None
        try:
            parsed_json = json.loads(gen_text)
        except Exception:
            m = re.search(r"(\{.*\})", gen_text, flags=re.DOTALL)
            if m:
                try:
                    parsed_json = json.loads(m.group(1))
                except Exception:
                    parsed_json = None

        if not parsed_json:
            return jsonify({"ok": False, "error": "Failed to parse model output", "raw": gen_text}), 500

        return jsonify(parsed_json)

@app.route("/assessment", methods=["POST"])
def assessment():
    """Generate assessment questions for a specific career"""
    data = request.json
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "GEMINI_API_KEY is not configured on the server",
            "hint": "Set GEMINI_API_KEY in your Vercel project Environment Variables and redeploy"
        }), 500
    career = data.get("career", "Software Engineer")
    if not career:
        return jsonify({"error": "No career path provided"}), 400

    model = gen_model

    assessment_prompt = f"""
    Create a short AI-generated assessment to evaluate a user's proficiency and interest in {career}.
    Return STRICTLY valid JSON in this format with 5-10 questions:
    {{
      "questions": [
        {{
          "type": "mcq",
          "question": "Question text here",
          "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
          "answer": 0,  # index of correct option
          "points": 1
        }},
        {{
          "type": "fill",
          "question": "Fill in the blank question text",
          "answer": "Correct answer",
          "points": 2
        }}
      ],
      "roadmap": "A brief, one-paragraph overview of the career progression."
    }}
    The output must be only the JSON object. Do not include any other text.
    """

    try:
        response = _retry(model.generate_content, assessment_prompt)
        result = try_parse_json(response.text)
        if result is None or "questions" not in result:
            raise ValueError("Failed to parse AI response for assessment.")
    except Exception as e:
        logging.error(f"Error generating assessment: {e}")
        return jsonify({"error": "Failed to generate assessment. Please try again."}), 500
    
    return jsonify(result)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    """Generate learning roadmap based on assessment score"""
    payload = request.get_json(silent=True) or {}
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "GEMINI_API_KEY is not configured on the server",
            "hint": "Set GEMINI_API_KEY in your Vercel project Environment Variables and redeploy"
        }), 500
    score = int(payload.get('score', 0))
    career = payload.get('career', "Software Engineer")
    language = payload.get('language', "Python")

    model = genai.GenerativeModel("models/gemini-1.5-flash")

    roadmap_prompt = f"""
    You are an expert technical mentor. Produce STRICTLY valid JSON (no commentary) describing a learning roadmap for someone aiming to become a pro {career}, who scored {score}/10 on a baseline test. The roadmap should have at least 2 phases. Each topic within a phase must include three sections: video resources, book resources, and a quiz.

    The JSON MUST have this exact structure:
    {{
      "score": {score},
      "career": "{career}",
      "language": "{language}",
      "roadmap": [
        {{
          "phase": "Phase name",
          "topics": [
            {{
              "title": "Topic name",
              "video_resources": [
                {{ "name": "Video title", "link": "YouTube URL" }},
                {{ "name": "Video title 2", "link": "YouTube URL 2" }},
                {{ "name": "Video title 3", "link": "YouTube URL 3" }},
                {{ "name": "Video title 4", "link": "YouTube URL 4" }},
                {{ "name": "Video title 5", "link": "YouTube URL 5" }}
              ],
              "book_resources": [
                {{ "name": "Book/Article title", "link": "URL" }},
                {{ "name": "Book/Article title 2", "link": "URL 2" }}
              ],
              "quiz": [
                {{ "type": "mcq", "question": "...", "options": ["a","b","c"], "answer": "correct", "points": 1 }},
                {{ "type": "fill", "question": "...", "answer": "correct", "points": 1 }},
                {{ "type": "code", "question": "Write code for ...", "answer": "expected output", "points": 3 }}
              ]
            }}
          ]
        }}
      ]
    }}

    Constraints:
    - Include exactly 5 video resources per topic.
    - Include exactly 2 book/article resources per topic.
    - Each topic must have 10-15 quiz questions.
    - Quiz questions should be a mix of "mcq", "fill", and "code" types.
    - All YouTube links should be genuine and active.
    - All book/article links should be genuine.
    - The output must be only the JSON object. No explanations or extra text.
    """

    try:
        response = _retry(model.generate_content, roadmap_prompt)
        response_text = response.text
        parsed = try_parse_json(response_text)
        
        if parsed is None:
            raise ValueError(f"Failed to parse AI response into JSON. Raw text: {response_text}")

        # Ensure the final structure is correct even if the AI adds a wrapper
        if "roadmap" not in parsed:
            return jsonify({"error": "AI response is missing the 'roadmap' key.", "raw_text": response_text}), 500

    except Exception as e:
        logging.error(f"Gemini API call or parsing failed: {e}")
        return jsonify({"error": "Gemini API call failed", "details": str(e)}), 500

    return jsonify(parsed), 200

@app.route("/get-startup-guidance", methods=["POST"])
def get_startup_guidance():
    """Get AI-powered startup guidance"""
    req = request.get_json(force=True)
    
    project_details = req.get('projectDetails', {})
    completed_steps = req.get('completedSteps', [])
    current_stage = req.get('currentStage', '')
    
    # Build context for AI
    context = f"""
Project Information:
- Name: {project_details.get('projectName', 'Not specified')}
- Description: {project_details.get('description', 'Not specified')}
- Current Stage: {current_stage}
- Challenges: {project_details.get('challenges', 'Not specified')}
- Goals: {project_details.get('goals', 'Not specified')}

Completed Steps: {completed_steps}
Total Steps Completed: {len(completed_steps)}/8

Startup Journey Steps:
1. Idea Validation & Market Research
2. Business Plan & Strategy  
3. Legal & Regulatory Setup
4. Funding & Investment
5. Product Development
6. Marketing & Branding
7. Team Building & Operations
8. Launch & Growth
"""

    prompt = f"""You are an expert startup advisor and mentor. Based on the following project information and progress, provide comprehensive, actionable guidance.

{context}

Please provide guidance in the following format:

1. **Current Status Assessment**: Analyze where they are in their startup journey
2. **Immediate Next Steps**: 3-5 specific, actionable next steps they should take
3. **Priority Focus Areas**: What they should focus on most right now
4. **Common Pitfalls to Avoid**: Based on their current stage
5. **Resource Recommendations**: Specific tools, platforms, or resources they should use
6. **Timeline Suggestions**: Realistic timeline for their next milestones

Make the guidance practical, specific, and tailored to their current situation. Use bullet points and be encouraging but realistic. Format the response in HTML for better presentation."""

    try:
        guidance_text = generate_with_gemini(prompt, max_output_tokens=1000, temperature=0.3)
        return jsonify({"guidance": guidance_text})
    except Exception as e:
        return jsonify({"error": f"Failed to generate guidance: {str(e)}"}), 500

@app.route("/get-role-roadmap", methods=["POST"])
def get_role_roadmap():
    """Get role-specific roadmap"""
    data = request.get_json()
    role = data.get("role")

    if not role:
        return jsonify({"error": "Role is required"}), 400

    try:
        prompt = f"""
        Given the role "{role}", return a JSON object with:
        1. Key technical and soft skills required.
        2. A step-by-step roadmap of skills to learn (Beginner → Intermediate → Advanced).
        Keep response structured in JSON only.
        """

        response = gen_model.generate_content(prompt)
        return jsonify({"result": response.text})

    except Exception as e:
        logging.error(f"Error in get_role_roadmap: {e}")
        return jsonify({"error": "Gemini API call failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
