"""
Vector store module for PathPilot RAG System.
Handles Pinecone integration for semantic search.
"""
import logging
from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from config import config

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages vector database operations with Pinecone."""
    
    def __init__(self):
        self.pc = None
        self.index = None
        self.index_name = config.PINECONE_INDEX_NAME
        self.dimension = config.EMBEDDING_DIMENSION
    
    def initialize(self) -> None:
        """Initialize Pinecone connection and index."""
        try:
            self.pc = Pinecone(api_key=config.PINECONE_API_KEY)
            
            # Check if index exists
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine"
                )
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            raise
    
    def upsert_documents(self, documents: List[Dict[str, Any]], batch_size: int = 100) -> None:
        """
        Upsert documents into Pinecone index.
        
        Args:
            documents: List of dicts with id, embedding, text, and metadata
            batch_size: Number of vectors per upsert batch
        """
        if not self.index:
            raise RuntimeError("Pinecone index not initialized. Call initialize() first.")
        
        total = len(documents)
        logger.info(f"Upserting {total} documents to Pinecone")
        
        for i in range(0, total, batch_size):
            batch = documents[i:i + batch_size]
            
            # Prepare vectors for upsert
            vectors = []
            for doc in batch:
                vectors.append({
                    "id": doc["id"],
                    "values": doc["embedding"],
                    "metadata": {
                        "text": doc["text"],
                        "type": doc["metadata"].get("type", ""),
                        "title": doc["metadata"].get("title", ""),
                        "category": doc["metadata"].get("category", ""),
                        "chunk_type": doc["metadata"].get("chunk_type", "")
                    }
                })
            
            # Upsert batch
            self.index.upsert(vectors=vectors)
            logger.info(f"Upserted batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size}")
        
        logger.info(f"Successfully upserted {total} documents")
    
    def query_similar(
        self, 
        query_embedding: List[float], 
        top_k: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Query Pinecone for similar vectors.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filter_dict: Optional metadata filter
            
        Returns:
            List of matching documents with scores
        """
        if not self.index:
            raise RuntimeError("Pinecone index not initialized. Call initialize() first.")
        
        query_params = {
            "vector": query_embedding,
            "top_k": top_k,
            "include_metadata": True
        }
        
        if filter_dict:
            query_params["filter"] = filter_dict
        
        response = self.index.query(**query_params)
        
        results = []
        for match in response.matches:
            results.append({
                "id": match.id,
                "score": match.score,
                "text": match.metadata.get("text", ""),
                "type": match.metadata.get("type", ""),
                "title": match.metadata.get("title", ""),
                "category": match.metadata.get("category", ""),
                "chunk_type": match.metadata.get("chunk_type", "")
            })
        
        logger.info(f"Retrieved {len(results)} similar documents")
        return results
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the Pinecone index."""
        if not self.index:
            raise RuntimeError("Pinecone index not initialized. Call initialize() first.")
        
        stats = self.index.describe_index_stats()
        return {
            "index_name": self.index_name,
            "total_vectors": stats.total_vector_count,
            "dimension": self.dimension,
            "metric": "cosine"
        }
    
    def delete_index(self) -> None:
        """Delete the Pinecone index (for testing/resetting)."""
        try:
            self.pc.delete_index(self.index_name)
            logger.info(f"Deleted Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Failed to delete index: {e}")
            raise
    
    def clear_index(self) -> None:
        """Clear all vectors from the index without deleting it."""
        if not self.index:
            raise RuntimeError("Pinecone index not initialized. Call initialize() first.")
        
        self.index.delete(delete_all=True)
        logger.info("Cleared all vectors from index")
