# PathPilot RAG System - Architecture Deep Dive

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │   Web App    │  │  API Clients │  │   Swagger UI (/docs)     │  │
│  │   (React)    │  │  (Postman)   │  │   (Interactive Testing)  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────────┘  │
│         │                 │                      │                   │
└─────────┼─────────────────┼──────────────────────┼───────────────────┘
          │                 │                      │
          └─────────────────┴──────────────────────┘
                             │
                    HTTP/REST API
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                        FASTAPI BACKEND                               │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    API Layer (app.py)                         │  │
│  │  - Request Validation (Pydantic)                              │  │
│  │  - CORS Middleware                                            │  │
│  │  - Error Handling                                             │  │
│  │  - Response Formatting                                        │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│  ┌────────────────────────▼─────────────────────────────────────┐  │
│  │                 Service Orchestration                         │  │
│  │  - Coordinate module interactions                             │  │
│  │  - Manage request lifecycle                                   │  │
│  │  - Track metrics (latency, context length)                    │  │
│  └────┬──────────┬──────────┬──────────┬────────────────────────┘  │
│       │          │          │          │                             │
└───────┼──────────┼──────────┼──────────┼─────────────────────────────┘
        │          │          │          │
        ▼          ▼          ▼          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         MODULES LAYER                                │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  INGESTION   │  │  EMBEDDING   │  │  RETRIEVAL   │              │
│  │              │  │              │  │              │              │
│  │ • Load JSON  │  │ • OpenAI     │  │ • Top-K      │              │
│  │ • Chunk data │  │   API        │  │   Search     │              │
│  │ • Tag meta   │  │ • Batch      │  │ • Filter by  │              │
│  │ • Validate   │  │   Process    │  │   Domain     │              │
│  └──────────────┘  └──────────────┘  │ • Assemble   │              │
│                                       │   Context    │              │
│  ┌──────────────┐  ┌──────────────┐  └──────┬───────┘              │
│  │  GENERATION  │  │   VECTOR     │         │                       │
│  │              │  │    STORE     │         │                       │
│  │ • OpenAI     │  │              │         │                       │
│  │   GPT-3.5    │  │ • Pinecone   │◄────────┘                       │
│  │ • JSON Mode  │  │ • Index Mgmt │                                 │
│  │ • Prompts    │  │ • Upsert     │                                 │
│  │ • Retry      │  │ • Query      │                                 │
│  └──────┬───────┘  └──────────────┘                                 │
│         │                                                            │
│  ┌──────▼───────┐                                                    │
│  │  EVALUATION  │                                                    │
│  │              │                                                    │
│  │ • LLM-Judge  │                                                    │
│  │ • A/B Test   │                                                    │
│  │ • Metrics    │                                                    │
│  │ • Logging    │                                                    │
│  └──────────────┘                                                    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                                 │
│                                                                       │
│  ┌─────────────────────┐              ┌─────────────────────────┐  │
│  │   OpenAI API        │              │   Pinecone Vector DB    │  │
│  │                     │              │                         │  │
│  │ • text-embedding-   │              │ • Cloud-hosted          │  │
│  │   3-small           │              │ • Auto-scaling          │  │
│  │ • gpt-3.5-turbo     │              │ • Low latency           │  │
│  │ • JSON mode         │              │ • Metadata filtering    │  │
│  └─────────────────────┘              └─────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
        ▲
        │
┌─────────────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE BASE                                  │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  careers.json│  │ startups.json│  │ financial_   │              │
│  │              │  │              │  │ data.json    │              │
│  │ • 50+ roles  │  │ • 3 types    │  │ • 10+ stocks │              │
│  │ • Skills     │  │ • Stages     │  │ • Strategies │              │
│  │ • Roadmaps   │  │ • Frameworks │  │ • Metrics    │              │
│  │ • Resources  │  │ • Case Study │  │ • Frameworks │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              learning_resources.json                          │  │
│  │  • Courses (Coursera, Udemy, edX)                             │  │
│  │  • YouTube Channels                                           │  │
│  │  • Documentation & Books                                      │  │
│  │  • GitHub Repositories                                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Request Lifecycle

### Example: Resume Analysis Request

```
1. User submits resume text
   │
   ▼
2. FastAPI receives POST /api/v1/analyze-resume
   │
   ├─ Validate request with Pydantic model
   ├─ Extract resume_text
   │
   ▼
3. RETRIEVAL PHASE
   │
   ├─ Retriever.retrieve_careers(resume_text, top_k=5)
   │   │
   │   ├─ EmbeddingService.get_embedding(resume_text)
   │   │   └─→ OpenAI API: 1536-dim vector
   │   │
   │   ├─ VectorStore.query_similar(embedding, top_k=5)
   │   │   └─→ Pinecone: Cosine similarity search
   │   │       Filter: type IN [career_overview, career_skills, career_roadmap]
   │   │
   │   └─ Returns: 5 most relevant career documents
   │
   ├─ Retriever.assemble_context(documents)
   │   └─ Formats: "[Doc 1] (Score: 0.892)..."
   │
   ▼
4. GENERATION PHASE
   │
   ├─ Generator.generate_career_recommendation(profile, context)
   │   │
   │   ├─ Load CAREER_RECOMMENDATION_PROMPT template
   │   ├─ Format prompt with profile + context
   │   │
   │   └─ OpenAI GPT-3.5-turbo (JSON mode)
   │       └─→ Returns structured JSON
   │
   ▼
5. RESPONSE PHASE
   │
   ├─ Parse JSON response
   ├─ Add metadata (processing_time, context_length)
   ├─ Log request/response
   └─ Return to client
   │
   ▼
6. Client receives structured response
```

---

## Module Interactions

### Startup Sequence

```
app.py startup_event()
   │
   ├─ 1. config.validate()
   │      └─ Check API keys present
   │
   ├─ 2. Initialize services
   │      ├─ DataIngestion()
   │      ├─ EmbeddingService()
   │      ├─ VectorStore()
   │      ├─ Retriever(embeddings, vector_store)
   │      └─ Generator()
   │
   ├─ 3. vector_store.initialize()
   │      ├─ Connect to Pinecone
   │      ├─ Check if index exists
   │      └─ Create index if needed
   │
   ├─ 4. ingestion_service.ingest_all()
   │      ├─ Load careers.json → chunk → 15 documents
   │      ├─ Load startups.json → chunk → 20 documents
   │      ├─ Load financial_data.json → chunk → 25 documents
   │      └─ Returns: ~60 Document objects
   │
   ├─ 5. embedding_service.embed_documents(documents)
   │      ├─ Extract texts from documents
   │      ├─ Batch embedding (100 per batch)
   │      ├─ OpenAI API calls
   │      └─ Returns: documents with embeddings
   │
   └─ 6. vector_store.upsert_documents(embedded_docs)
          ├─ Batch upsert (100 per batch)
          ├─ Pinecone API calls
          └─ Documents stored and ready for retrieval
```

---

## RAG Pipeline Details

### 1. Ingestion Pipeline

```
Raw JSON → Parse → Chunk → Tag Metadata → Document Objects
   │
   ├─ Career Chunking Strategy:
   │   ├─ 1 overview chunk per career
   │   ├─ 1 skills chunk per career
   │   └─ N roadmap chunks (1 per phase)
   │
   ├─ Startup Chunking Strategy:
   │   ├─ 1 overview chunk per startup type
   │   ├─ N stage chunks (1 per stage)
   │   └─ M case study chunks
   │
   └─ Financial Chunking Strategy:
       ├─ 1 chunk per stock
       ├─ 1 chunk per investment strategy
       └─ 1 chunk per analysis framework
```

### 2. Embedding Pipeline

```
Document Text → OpenAI text-embedding-3-small → 1536-dim Vector
   │
   ├─ Input: "Career: Data Scientist\nCategory: Technology\n..."
   ├─ Model: text-embedding-3-small
   ├─ Output: [0.023, -0.045, 0.012, ...] (1536 floats)
   ├─ Batch Size: 100 documents per API call
   └─ Cost: ~$0.02 per 1000 documents
```

### 3. Retrieval Pipeline

```
User Query → Embed → Pinecone Search → Top-K Results → Context
   │
   ├─ Query: "I want to become a data scientist"
   │
   ├─ Embedding: Same model as ingestion
   │   └─ Ensures vector space alignment
   │
   ├─ Pinecone Query:
   │   ├─ vector: query_embedding
   │   ├─ top_k: 5
   │   ├─ filter: {"type": {"$in": ["career_*"]}}
   │   └─ include_metadata: true
   │
   ├─ Results (sorted by cosine similarity):
   │   ├─ [0] Data Scientist overview (score: 0.892)
   │   ├─ [1] Data Scientist skills (score: 0.847)
   │   ├─ [2] ML Engineer overview (score: 0.823)
   │   ├─ [3] Data Scientist roadmap (score: 0.798)
   │   └─ [4] Data Analyst overview (score: 0.756)
   │
   └─ Context Assembly:
       ├─ Max length: 3000 characters
       ├─ Format: "[Doc N] (Score: X.XXX)\nType: ...\n..."
       └─ Truncates if exceeds max_length
```

### 4. Generation Pipeline

```
Prompt Template + Context → OpenAI GPT-3.5 → Structured JSON
   │
   ├─ Prompt Structure:
   │   ├─ System instructions
   │   ├─ User profile/query
   │   ├─ Retrieved context
   │   └─ Output schema (JSON structure)
   │
   ├─ Generation Config:
   │   ├─ model: gpt-3.5-turbo
   │   ├─ temperature: 0.2 (deterministic)
   │   ├─ max_tokens: 2000
   │   └─ response_format: {"type": "json_object"}
   │
   └─ Output:
       ├─ Parsed JSON
       ├─ Validated structure
       └─ Ready for frontend
```

---

## Evaluation Architecture

### A/B Testing Flow

```
User Query
   │
   ├─ Path A: WITH Retrieval (RAG)
   │   ├─ Retrieve context (top-k=5)
   │   ├─ Generate with context
   │   └─ Response A
   │
   ├─ Path B: WITHOUT Retrieval (Baseline)
   │   ├─ No context
   │   ├─ Generate without context
   │   └─ Response B
   │
   └─ Evaluation
       ├─ LLM-as-Judge evaluates Response A
       ├─ Scores: Relevance, Completeness, Context Usage, Specificity, Accuracy
       └─ Comparison: A vs B
```

### Metrics Calculation

```
Evaluation Prompt → LLM Judge → Scores (1-5 scale)
   │
   ├─ Input:
   │   ├─ Original query
   │   ├─ Retrieved context
   │   └─ Generated response
   │
   ├─ Metrics:
   │   ├─ Relevance: How well does it answer the query?
   │   ├─ Completeness: Does it cover all aspects?
   │   ├─ Context Usage: Does it use retrieved info?
   │   ├─ Specificity: Is it actionable and specific?
   │   └─ Accuracy: Is it factually correct?
   │
   └─ Output:
       ├─ Individual scores
       ├─ Overall score (average)
       ├─ Strengths
       ├─ Weaknesses
       └─ Improvement suggestions
```

---

## Scalability Design

### Current Capacity
- **Documents:** ~500 chunks
- **Index Size:** ~10 MB
- **Query Latency:** <100ms (retrieval)
- **Throughput:** 10+ req/sec

### Scaling Strategies

#### Horizontal Scaling
```
Multiple FastAPI Instances → Load Balancer → Clients
   │
   ├─ Share same Pinecone index
   ├─ Stateless architecture
   └─ Auto-scale based on traffic
```

#### Vertical Scaling
```
Larger Datasets → Better Chunking → Improved Retrieval
   │
   ├─ Add more domains (healthcare, education, etc.)
   ├─ Implement hierarchical chunking
   └─ Add metadata enrichment
```

#### Performance Optimization
```
Caching → Async Processing → Batch Operations
   │
   ├─ Redis cache for frequent queries
   ├─ Celery for background tasks
   └─ Batch embeddings for efficiency
```

---

## Security Considerations

- **API Keys:** Stored in .env, never committed
- **Input Validation:** Pydantic models for all requests
- **Rate Limiting:** Implement in production
- **CORS:** Configurable origins
- **Logging:** No sensitive data in logs
- **Error Handling:** No stack traces in responses

---

## Monitoring & Observability

### Metrics to Track
- Request latency (p50, p95, p99)
- Retrieval quality (average similarity scores)
- Evaluation scores over time
- API error rates
- Token usage and costs

### Logging Strategy
- Structured JSON logs
- Request/response correlation IDs
- Performance metrics
- Error tracking

---

This architecture demonstrates production-grade AI engineering with:
✅ Modular design
✅ Separation of concerns
✅ Scalability planning
✅ Evaluation framework
✅ Error handling
✅ Performance optimization
