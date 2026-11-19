"""
Embedding module for PathPilot RAG System.
Handles text embedding generation using Google Gemini.
"""
import logging
import time
from typing import List, Dict, Any
from google import genai
from config import config

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Manages text embedding generation with Google Gemini."""
    
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model = config.EMBEDDING_MODEL
        self.max_retries = 3
        self.retry_delay = 1.5
    
    def _extract_values(self, embeddings) -> List[List[float]]:
        """Extract float vectors from google-genai embedding objects."""
        vectors = []
        for item in embeddings or []:
            values = getattr(item, "values", None)
            if values is None and isinstance(item, dict):
                values = item.get("values")
            if values is None:
                raise ValueError("Embedding response did not include .values")
            vectors.append(list(values))
        return vectors
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.embed_content(
                    model=self.model,
                    contents=text
                )
                vectors = self._extract_values(response.embeddings)
                if not vectors:
                    raise ValueError("Empty embedding response")
                return vectors[0]
            except Exception as e:
                logger.warning(f"Embedding attempt {attempt}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay ** attempt)
                else:
                    raise
    
    def get_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of input texts
            batch_size: Number of texts per batch
            
        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} texts)")
            
            for attempt in range(1, self.max_retries + 1):
                try:
                    response = self.client.models.embed_content(
                        model=self.model,
                        contents=batch
                    )
                    batch_embeddings = self._extract_values(response.embeddings)
                    if len(batch_embeddings) != len(batch):
                        raise ValueError(
                            f"Expected {len(batch)} embeddings, got {len(batch_embeddings)}"
                        )
                    all_embeddings.extend(batch_embeddings)
                    break
                    
                except Exception as e:
                    logger.warning(f"Batch embedding attempt {attempt}/{self.max_retries} failed: {e}")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay ** attempt)
                    else:
                        raise
        
        logger.info(f"Generated {len(all_embeddings)} embeddings successfully")
        return all_embeddings
    
    def embed_documents(self, documents: List[Any]) -> List[Dict[str, Any]]:
        """
        Embed a list of Document objects.
        
        Args:
            documents: List of Document objects from ingestion
            
        Returns:
            List of dicts with text, embedding, and metadata
        """
        texts = [doc.text for doc in documents]
        embeddings = self.get_embeddings_batch(texts)
        
        embedded_docs = []
        for doc, embedding in zip(documents, embeddings):
            embedded_docs.append({
                "id": f"{doc.metadata.get('type', 'unknown')}_{doc.metadata.get('career_id', doc.metadata.get('startup_id', doc.metadata.get('symbol', 'unknown')))}_{doc.metadata.get('chunk_type', 'unknown')}",
                "text": doc.text,
                "embedding": embedding,
                "metadata": doc.metadata
            })
        
        logger.info(f"Embedded {len(embedded_docs)} documents")
        return embedded_docs
