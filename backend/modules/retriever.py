"""
Retriever module for PathPilot RAG System.
Handles semantic search and context assembly.
"""
import logging
from typing import List, Dict, Any, Optional
from modules.embeddings import EmbeddingService
from modules.vector_store import VectorStore
from config import config

logger = logging.getLogger(__name__)


class Retriever:
    """Manages document retrieval for RAG pipeline."""
    
    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStore):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.top_k = config.TOP_K
    
    def retrieve_careers(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve career-related documents.
        
        Args:
            query: User query or profile text
            top_k: Number of results (defaults to config.TOP_K)
            
        Returns:
            List of relevant career documents
        """
        k = top_k or self.top_k
        
        # Generate query embedding
        query_embedding = self.embedding_service.get_embedding(query)
        
        # Query with career type filter
        filter_dict = {"type": {"$in": ["career_overview", "career_skills", "career_roadmap"]}}
        results = self.vector_store.query_similar(query_embedding, top_k=k, filter_dict=filter_dict)
        
        logger.info(f"Retrieved {len(results)} career documents for query")
        return results
    
    def retrieve_startup_guidance(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve startup-related documents.
        
        Args:
            query: User query about startup
            top_k: Number of results
            
        Returns:
            List of relevant startup documents
        """
        k = top_k or self.top_k
        
        # Generate query embedding
        query_embedding = self.embedding_service.get_embedding(query)
        
        # Query with startup type filter
        filter_dict = {"type": {"$in": ["startup_overview", "startup_stage", "startup_case_study"]}}
        results = self.vector_store.query_similar(query_embedding, top_k=k, filter_dict=filter_dict)
        
        logger.info(f"Retrieved {len(results)} startup documents for query")
        return results
    
    def retrieve_financial_insights(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve financial-related documents.
        
        Args:
            query: User query about finance/stocks
            top_k: Number of results
            
        Returns:
            List of relevant financial documents
        """
        k = top_k or self.top_k
        
        # Generate query embedding
        query_embedding = self.embedding_service.get_embedding(query)
        
        # Query with financial type filter
        filter_dict = {"type": {"$in": ["financial_stock", "financial_strategy", "financial_framework"]}}
        results = self.vector_store.query_similar(query_embedding, top_k=k, filter_dict=filter_dict)
        
        logger.info(f"Retrieved {len(results)} financial documents for query")
        return results
    
    def retrieve_all(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve documents from all domains without filtering.
        
        Args:
            query: User query
            top_k: Number of results
            
        Returns:
            List of relevant documents from all categories
        """
        k = top_k or self.top_k
        
        # Generate query embedding
        query_embedding = self.embedding_service.get_embedding(query)
        
        # Query without filter
        results = self.vector_store.query_similar(query_embedding, top_k=k)
        
        logger.info(f"Retrieved {len(results)} documents from all domains")
        return results
    
    def assemble_context(self, retrieved_docs: List[Dict[str, Any]], max_length: int = 3000) -> str:
        """
        Assemble retrieved documents into a coherent context string.
        
        Args:
            retrieved_docs: List of retrieved documents
            max_length: Maximum character length for context
            
        Returns:
            Formatted context string for LLM prompt
        """
        context_parts = []
        current_length = 0
        
        for i, doc in enumerate(retrieved_docs):
            doc_text = (
                f"[Document {i+1}] (Score: {doc['score']:.3f})\n"
                f"Type: {doc['type']}\n"
                f"Title: {doc.get('title', 'N/A')}\n"
                f"{doc['text']}\n"
            )
            
            # Check if adding this doc exceeds max length
            if current_length + len(doc_text) > max_length:
                break
            
            context_parts.append(doc_text)
            current_length += len(doc_text)
        
        context = "\n".join(context_parts)
        logger.info(f"Assembled context: {len(context)} characters from {len(context_parts)} documents")
        return context
    
    def retrieve_and_assemble(
        self, 
        query: str, 
        domain: str = "all",
        top_k: Optional[int] = None
    ) -> str:
        """
        Retrieve documents and assemble context in one step.
        
        Args:
            query: User query
            domain: Domain filter (career, startup, financial, all)
            top_k: Number of results
            
        Returns:
            Formatted context string
        """
        # Retrieve based on domain
        if domain == "career":
            docs = self.retrieve_careers(query, top_k)
        elif domain == "startup":
            docs = self.retrieve_startup_guidance(query, top_k)
        elif domain == "financial":
            docs = self.retrieve_financial_insights(query, top_k)
        else:
            docs = self.retrieve_all(query, top_k)
        
        # Assemble context
        context = self.assemble_context(docs)
        return context
