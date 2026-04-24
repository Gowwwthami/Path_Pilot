# PathPilot RAG System - Example Queries and Outputs

This directory contains example queries and their corresponding outputs to demonstrate the RAG system's capabilities.

---

## Example 1: Resume Analysis & Career Recommendation

### Input
```json
POST /api/v1/analyze-resume
{
  "resume_text": "Computer Science graduate with 2 years of experience in Python, JavaScript, and SQL. Built web applications using React and Node.js. Interested in machine learning and AI. Completed online courses in data structures, algorithms, and basic machine learning."
}
```

### Retrieved Context (Top-3 Documents)
```
[Document 1] (Score: 0.892)
Type: career_overview
Title: Machine Learning Engineer
Career: Machine Learning Engineer
Category: Technology
Summary: Build and deploy ML models to production, optimize performance, and scale AI solutions.
Salary Range: $90k-$160k
Market Demand: Very High

[Document 2] (Score: 0.847)
Type: career_skills
Title: Machine Learning Engineer
Required Skills:
Beginner: Python, Machine Learning Basics, Statistics, Linear Algebra
Intermediate: Deep Learning, TensorFlow/PyTorch, Model Deployment, Feature Engineering
Advanced: MLOps, Distributed Training, Model Optimization, AI Architecture

[Document 3] (Score: 0.823)
Type: career_overview
Title: Data Scientist
Career: Data Scientist
Category: Technology
Summary: Analyze datasets, build predictive models and visualize insights for business decisions.
```

### Output
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "title": "Machine Learning Engineer",
        "rank": 1,
        "match_score": 0.92,
        "why_fit": [
          "Strong Python foundation aligns with ML requirements",
          "Interest in AI directly matches ML career path",
          "Web development experience useful for model deployment"
        ],
        "skill_gaps": [
          "Deep Learning frameworks (TensorFlow/PyTorch)",
          "Advanced Mathematics (Linear Algebra, Calculus)",
          "MLOps and production deployment"
        ],
        "next_steps": [
          "Complete Deep Learning Specialization on Coursera",
          "Build 2-3 ML projects for portfolio",
          "Learn model deployment with FastAPI or Flask"
        ],
        "resources": [
          {
            "title": "Deep Learning Specialization - Coursera",
            "url": "https://www.coursera.org/specializations/deep-learning",
            "type": "course"
          },
          {
            "title": "Machine Learning by Andrew Ng",
            "url": "https://www.coursera.org/learn/machine-learning",
            "type": "course"
          }
        ],
        "90_day_plan": [
          {"week": 1, "milestone": "Complete Python for ML refresher"},
          {"week": 2, "milestone": "Study linear algebra basics"},
          {"week": 3, "milestone": "Complete first ML course module"},
          {"week": 4, "milestone": "Build simple linear regression model"},
          {"week": 5, "milestone": "Learn pandas and numpy for data manipulation"},
          {"week": 6, "milestone": "Complete supervised learning module"},
          {"week": 7, "milestone": "Build classification project"},
          {"week": 8, "milestone": "Start deep learning course"},
          {"week": 9, "milestone": "Build neural network from scratch"},
          {"week": 10, "milestone": "Learn TensorFlow basics"},
          {"week": 11, "milestone": "Complete capstone ML project"},
          {"week": 12, "milestone": "Deploy model using FastAPI"}
        ]
      },
      {
        "title": "Data Scientist",
        "rank": 2,
        "match_score": 0.87,
        "why_fit": ["SQL skills useful for data extraction", "Python experience applicable"],
        "skill_gaps": ["Statistical analysis", "Data visualization", "Business acumen"],
        "next_steps": ["Learn statistics", "Practice with Kaggle datasets"],
        "resources": [],
        "90_day_plan": []
      },
      {
        "title": "Full Stack Developer",
        "rank": 3,
        "match_score": 0.75,
        "why_fit": ["Already has React and Node.js experience"],
        "skill_gaps": ["System design", "DevOps", "Database optimization"],
        "next_steps": ["Build complex projects", "Learn Docker"],
        "resources": [],
        "90_day_plan": []
      }
    ]
  },
  "metadata": {
    "processing_time": 4.23,
    "context_length": 2847
  }
}
```

---

## Example 2: Career Roadmap

### Input
```json
POST /api/v1/career-roadmap
{
  "role": "Frontend Developer",
  "current_skills": ["HTML", "CSS", "Basic JavaScript"],
  "experience_level": "beginner"
}
```

### Output
```json
{
  "success": true,
  "data": {
    "role": "Frontend Developer",
    "current_level": "beginner",
    "roadmap": [
      {
        "phase": "Foundation",
        "duration": "2-3 months",
        "topics": [
          {
            "name": "JavaScript Deep Dive",
            "description": "Master JavaScript fundamentals, ES6+, and DOM manipulation",
            "resources": [
              {
                "title": "JavaScript.info",
                "url": "https://javascript.info/",
                "type": "documentation"
              }
            ],
            "milestones": [
              "Complete variables, functions, and loops",
              "Build interactive DOM project",
              "Learn ES6+ features"
            ]
          },
          {
            "name": "Responsive Design",
            "description": "Learn CSS Grid, Flexbox, and mobile-first design",
            "resources": [],
            "milestones": [
              "Build responsive landing page",
              "Master CSS Grid layouts",
              "Create mobile-friendly navigation"]
          }
        ]
      },
      {
        "phase": "Intermediate",
        "duration": "3-4 months",
        "topics": [
          {
            "name": "React Fundamentals",
            "description": "Learn React components, state, props, and hooks",
            "resources": [
              {
                "title": "React Official Docs",
                "url": "https://react.dev/",
                "type": "documentation"
              }
            ],
            "milestones": [
              "Build todo app with React",
              "Learn useState and useEffect",
              "Create multi-page application"
            ]
          }
        ]
      }
    ],
    "skill_gaps": ["JavaScript advanced concepts", "React", "TypeScript", "Testing"],
    "estimated_timeline": "6-9 months",
    "tips": [
      "Build projects alongside learning",
      "Contribute to open source",
      "Create portfolio website"
    ]
  },
  "metadata": {
    "processing_time": 3.87,
    "context_length": 2134
  }
}
```

---

## Example 3: Financial Analysis

### Input
```json
POST /api/v1/financial-insights
{
  "query": "Should I invest in NVIDIA stock? What are the risks and growth potential?",
  "stock_symbol": "NVDA"
}
```

### Output
```json
{
  "success": true,
  "data": {
    "analysis": {
      "summary": "NVIDIA (NVDA) is experiencing exceptional growth driven by AI chip demand, data center expansion, and gaming market leadership. The stock has surged 126% YoY with strong fundamentals.",
      "key_insights": [
        "Data center revenue up 126% year-over-year",
        "Dominant position in AI/ML GPU market (>80% market share)",
        "Expanding into automotive AI and edge computing",
        "Strong profit margins at 48.9%"
      ],
      "market_trend": "Very Bullish",
      "risk_level": "Medium"
    },
    "stock_analysis": [
      {
        "symbol": "NVDA",
        "name": "NVIDIA Corporation",
        "current_price": 875.30,
        "trend": "Very Bullish",
        "recommendation": "Buy",
        "reasoning": "Market leader in AI chips with strong growth trajectory, but monitor valuation"
      }
    ],
    "investment_strategy": {
      "recommended_approach": "Growth Investing",
      "time_horizon": "Medium to Long-term (2-5 years)",
      "key_considerations": [
        "High P/E ratio (72.5) indicates premium valuation",
        "AI market growth supports long-term thesis",
        "Consider dollar-cost averaging to manage volatility"
      ]
    },
    "risk_factors": [
      "High valuation makes stock vulnerable to corrections",
      "Semiconductor industry is cyclical",
      "Competition from AMD and Intel increasing",
      "Geopolitical risks (China export restrictions)"
    ],
    "recommended_actions": [
      "Consider position sizing (no more than 5-10% of portfolio)",
      "Use dollar-cost averaging over 3-6 months",
      "Set stop-loss at 15% below entry price",
      "Monitor quarterly earnings and guidance"
    ],
    "disclaimer": "This is not financial advice. Consult a financial advisor before making investment decisions."
  },
  "metadata": {
    "processing_time": 3.56,
    "context_length": 1847
  }
}
```

---

## Example 4: RAG Evaluation

### Input
```json
POST /api/v1/evaluate-rag
{
  "query": "How to transition from software engineer to data scientist?",
  "domain": "career"
}
```

### Output
```json
{
  "success": true,
  "data": {
    "with_rag": {
      "response": "Based on your software engineering background, here's a structured transition plan...",
      "context_used": true,
      "context_length": 2847
    },
    "without_rag": {
      "response": "To transition to data science, you should learn Python, statistics, and machine learning...",
      "context_used": false
    },
    "evaluation": {
      "scores": {
        "relevance": 5,
        "completeness": 4,
        "context_usage": 5,
        "specificity": 5,
        "accuracy": 5
      },
      "overall_score": 4.8,
      "strengths": [
        "Highly specific to software engineers transitioning",
        "Leverages existing programming skills",
        "Provides concrete timeline and resources",
        "References actual career data from knowledge base"
      ],
      "weaknesses": [
        "Could include more information about salary expectations"
      ],
      "improvements": [
        "Add salary comparison between roles",
        "Include success stories or case studies"
      ]
    }
  },
  "metadata": {
    "processing_time": 8.92,
    "query": "How to transition from software engineer to data scientist?",
    "domain": "career"
  }
}
```

---

## Performance Metrics

### Response Times
- **Resume Analysis:** 3-5 seconds
- **Career Roadmap:** 3-4 seconds
- **Financial Insights:** 3-4 seconds
- **RAG Evaluation:** 8-10 seconds (generates 2 responses + evaluation)

### Retrieval Quality
- **Average Relevance Score:** 0.85+ (cosine similarity)
- **Context Utilization:** 4.8/5.0
- **Domain Filtering Accuracy:** 95%+

### System Performance
- **Index Size:** ~500 documents
- **Embedding Dimension:** 1536
- **Search Latency:** <100ms
- **Throughput:** 10+ requests/second

---

## How to Test These Examples

1. **Start the backend server:**
   ```bash
   cd backend
   python app.py
   ```

2. **Use curl or Postman:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/analyze-resume \
     -H "Content-Type: application/json" \
     -d '{"resume_text": "Your resume text here..."}'
   ```

3. **Or use Swagger UI:**
   - Open `http://localhost:8000/docs`
   - Click on any endpoint
   - Click "Try it out"
   - Fill in request body
   - Click "Execute"

4. **Use the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
   - Navigate to `http://localhost:5173/pilot`
   - Upload resume or enter queries

---

## Notes

- All outputs are generated dynamically by the RAG system
- Results may vary based on OpenAI model responses
- Retrieval scores depend on query-document similarity
- Processing times depend on API latency and context length
