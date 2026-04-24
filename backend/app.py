"""
PathPilot RAG System - FastAPI Application
Production-grade RAG-based AI system for career guidance, startup advice, and financial insights.
"""
import logging
import time
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import modules
from modules.ingestion import DataIngestion
from modules.embeddings import EmbeddingService
from modules.vector_store import VectorStore
from modules.retriever import Retriever
from modules.generator import Generator

# Initialize FastAPI app
app = FastAPI(
    title="PathPilot RAG API",
    description="Production-grade RAG-based AI system for career guidance, startup advice, and financial insights",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (initialized on startup)
ingestion_service: Optional[DataIngestion] = None
embedding_service: Optional[EmbeddingService] = None
vector_store: Optional[VectorStore] = None
retriever: Optional[Retriever] = None
generator: Optional[Generator] = None


# Request/Response Models
class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    preferences: Optional[Dict[str, Any]] = None

class CareerRoadmapRequest(BaseModel):
    role: str
    current_skills: List[str]
    experience_level: str

class StartupGuidanceRequest(BaseModel):
    project_details: Dict[str, Any]
    current_stage: str
    challenges: List[str]

class FinancialInsightsRequest(BaseModel):
    query: str
    stock_symbol: Optional[str] = None

class EvaluationRequest(BaseModel):
    query: str
    domain: str = "career"

class AssessmentRoadmapRequest(BaseModel):
    score: int
    career: str
    language: str = "Python"


@app.on_event("startup")
async def startup_event():
    """Initialize all services on startup."""
    global ingestion_service, embedding_service, vector_store, retriever, generator
    
    logger.info("Initializing PathPilot RAG System...")
    
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated")
        
        # Initialize services
        ingestion_service = DataIngestion()
        embedding_service = EmbeddingService()
        vector_store = VectorStore()
        retriever = Retriever(embedding_service, vector_store)
        generator = Generator()
        
        logger.info("Services initialized")
        
        # Initialize Pinecone
        vector_store.initialize()
        logger.info("Pinecone initialized")
        
        # Ingest data
        logger.info("Starting data ingestion...")
        documents = ingestion_service.ingest_all()
        logger.info(f"Ingested {len(documents)} documents")
        
        # Embed and store documents
        embedded_docs = embedding_service.embed_documents(documents)
        logger.info(f"Embedded {len(embedded_docs)} documents")
        
        vector_store.upsert_documents(embedded_docs)
        logger.info("Documents upserted to Pinecone")
        
        # Get stats
        stats = vector_store.get_index_stats()
        logger.info(f"Index stats: {stats}")
        
        logger.info("PathPilot RAG System initialized successfully!")
        
    except Exception as e:
        logger.error(f"Failed to initialize PathPilot: {e}")
        raise


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    try:
        stats = vector_store.get_index_stats()
        return {
            "status": "healthy",
            "model": config.GENERATION_MODEL,
            "embedding_model": config.EMBEDDING_MODEL,
            "index_stats": stats
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }


@app.post("/api/v1/analyze-resume")
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze resume and provide career recommendations using RAG.
    
    - Extract skills from resume
    - Retrieve relevant careers from vector store
    - Generate structured recommendations
    """
    try:
        start_time = time.time()
        
        # Use resume text as query
        profile_text = request.resume_text
        
        # Retrieve relevant careers
        context = retriever.retrieve_and_assemble(profile_text, domain="career", top_k=5)
        
        # Generate recommendations
        recommendations = generator.generate_career_recommendation(profile_text, context)
        
        elapsed = time.time() - start_time
        
        return {
            "success": True,
            "data": recommendations,
            "metadata": {
                "processing_time": round(elapsed, 2),
                "context_length": len(context)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in analyze_resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/career-roadmap")
async def career_roadmap(request: CareerRoadmapRequest):
    """
    Generate personalized career roadmap.
    
    - Retrieve role-specific data
    - Generate phase-by-phase learning plan
    - Include resources and milestones
    """
    try:
        start_time = time.time()
        
        # Build query from role and skills
        query = f"{request.role} career path with skills: {', '.join(request.current_skills)}"
        
        # Retrieve relevant data
        context = retriever.retrieve_and_assemble(query, domain="career", top_k=5)
        
        # Generate roadmap
        roadmap = generator.generate_career_roadmap(
            role=request.role,
            current_skills=", ".join(request.current_skills),
            experience_level=request.experience_level,
            context=context
        )
        
        elapsed = time.time() - start_time
        
        return {
            "success": True,
            "data": roadmap,
            "metadata": {
                "processing_time": round(elapsed, 2),
                "context_length": len(context)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in career_roadmap: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/startup-guidance")
async def startup_guidance(request: StartupGuidanceRequest):
    """
    Provide startup guidance based on project details.
    
    - Retrieve relevant startup frameworks
    - Generate actionable advice
    - Include timelines and resources
    """
    try:
        start_time = time.time()
        
        # Build project summary
        project_summary = f"""
Project: {request.project_details.get('name', 'N/A')}
Description: {request.project_details.get('description', 'N/A')}
Current Stage: {request.current_stage}
Challenges: {', '.join(request.challenges)}
Goals: {request.project_details.get('goals', 'N/A')}
"""
        
        # Retrieve relevant startup data
        context = retriever.retrieve_and_assemble(project_summary, domain="startup", top_k=5)
        
        # Generate guidance
        guidance = generator.generate_startup_guidance(project_summary, context)
        
        elapsed = time.time() - start_time
        
        return {
            "success": True,
            "data": guidance,
            "metadata": {
                "processing_time": round(elapsed, 2),
                "context_length": len(context)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in startup_guidance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/financial-insights")
async def financial_insights(request: FinancialInsightsRequest):
    """
    Provide financial market insights and analysis.
    
    - Retrieve relevant financial data
    - Generate market analysis
    - Include stock recommendations
    """
    try:
        start_time = time.time()
        
        # Build query
        query = request.query
        if request.stock_symbol:
            query += f" Specifically analyze {request.stock_symbol}"
        
        # Retrieve financial data
        context = retriever.retrieve_and_assemble(query, domain="financial", top_k=5)
        
        # Generate analysis
        analysis = generator.generate_financial_analysis(query, context)
        
        elapsed = time.time() - start_time
        
        return {
            "success": True,
            "data": analysis,
            "metadata": {
                "processing_time": round(elapsed, 2),
                "context_length": len(context)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in financial_insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/evaluate")
async def evaluate_assessment(request: AssessmentRoadmapRequest):
    """
    Generate learning roadmap based on assessment score.
    
    - Retrieve learning resources
    - Generate personalized roadmap
    - Include quizzes and resources
    """
    try:
        start_time = time.time()
        
        # Build query
        query = f"Learning roadmap for {request.career} with score {request.score}/10 using {request.language}"
        
        # Retrieve relevant data
        context = retriever.retrieve_and_assemble(query, domain="career", top_k=5)
        
        # Generate roadmap (reuse career roadmap generator)
        roadmap = generator.generate_career_roadmap(
            role=request.career,
            current_skills=request.language,
            experience_level="beginner" if request.score < 5 else "intermediate",
            context=context
        )
        
        elapsed = time.time() - start_time
        
        return {
            "success": True,
            "data": roadmap,
            "metadata": {
                "processing_time": round(elapsed, 2),
                "context_length": len(context)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in evaluate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/evaluate-rag")
async def evaluate_rag(request: EvaluationRequest):
    """
    Evaluate RAG system performance.
    
    - Generate response WITH retrieval (RAG)
    - Generate response WITHOUT retrieval (baseline)
    - Compare and score both responses
    """
    try:
        start_time = time.time()
        
        # Generate WITH retrieval (RAG)
        context = retriever.retrieve_and_assemble(request.query, domain=request.domain, top_k=5)
        response_with_rag = generator.generate(
            f"Query: {request.query}\nContext: {context}\nProvide a comprehensive answer."
        )
        
        # Generate WITHOUT retrieval (baseline)
        response_without_rag = generator.generate(
            f"Query: {request.query}\nProvide a comprehensive answer."
        )
        
        # Evaluate RAG response
        evaluation = generator.generate_evaluation(
            query=request.query,
            context=context,
            response=response_with_rag
        )
        
        elapsed = time.time() - start_time
        
        return {
            "success": True,
            "data": {
                "with_rag": {
                    "response": response_with_rag,
                    "context_used": True,
                    "context_length": len(context)
                },
                "without_rag": {
                    "response": response_without_rag,
                    "context_used": False
                },
                "evaluation": evaluation
            },
            "metadata": {
                "processing_time": round(elapsed, 2),
                "query": request.query,
                "domain": request.domain
            }
        }
        
    except Exception as e:
        logger.error(f"Error in evaluate_rag: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/index-stats")
async def index_stats():
    """Get Pinecone index statistics."""
    try:
        stats = vector_store.get_index_stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT, reload=True)
