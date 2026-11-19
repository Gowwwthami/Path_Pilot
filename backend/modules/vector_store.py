"""
Vector store module for PathPilot RAG System.
In-memory NumPy cosine-similarity index (no Pinecone).
"""
import logging
from typing import List, Dict, Any, Optional

import numpy as np
from config import config

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages in-memory vector search with cosine similarity."""
    
    def __init__(self):
        self.index_name = "pathpilot-inmemory"
        self.dimension = config.EMBEDDING_DIMENSION
        self._ready = False
        self._ids: List[str] = []
        self._metadatas: List[Dict[str, Any]] = []
        self._vectors: Optional[np.ndarray] = None
        self._id_to_pos: Dict[str, int] = {}
    
    def initialize(self) -> None:
        """Initialize the in-memory index."""
        self._ready = True
        if self._vectors is None:
            self._ids = []
            self._metadatas = []
            self._vectors = None
            self._id_to_pos = {}
        logger.info("Initialized in-memory vector store")
    
    def _ensure_ready(self) -> None:
        if not self._ready:
            raise RuntimeError("Vector store not initialized. Call initialize() first.")
    
    def _matches_filter(self, metadata: Dict[str, Any], filter_dict: Optional[Dict]) -> bool:
        if not filter_dict:
            return True
        for key, expected in filter_dict.items():
            actual = metadata.get(key)
            if isinstance(expected, dict) and "$in" in expected:
                if actual not in expected["$in"]:
                    return False
            elif actual != expected:
                return False
        return True
    
    def upsert_documents(self, documents: List[Dict[str, Any]], batch_size: int = 100) -> None:
        """
        Upsert documents into the in-memory index.
        
        Args:
            documents: List of dicts with id, embedding, text, and metadata
            batch_size: Unused (kept for API compatibility)
        """
        self._ensure_ready()
        del batch_size
        
        total = len(documents)
        for doc in documents:
            embedding = doc.get("embedding") or []
            if embedding:
                inferred = len(embedding)
                if inferred != self.dimension:
                    logger.warning(
                        f"Inferred embedding dimension {inferred} differs from "
                        f"configured {self.dimension}; using inferred value"
                    )
                    self.dimension = inferred
                break
        
        logger.info(f"Upserting {total} documents to in-memory index")
        
        for doc in documents:
            vector = np.asarray(doc["embedding"], dtype=np.float32)
            metadata = {
                "text": doc["text"],
                "type": doc["metadata"].get("type", ""),
                "title": doc["metadata"].get("title", ""),
                "category": doc["metadata"].get("category", ""),
                "chunk_type": doc["metadata"].get("chunk_type", ""),
            }
            doc_id = doc["id"]
            
            if doc_id in self._id_to_pos:
                pos = self._id_to_pos[doc_id]
                self._metadatas[pos] = metadata
                self._vectors[pos] = vector
            else:
                pos = len(self._ids)
                self._id_to_pos[doc_id] = pos
                self._ids.append(doc_id)
                self._metadatas.append(metadata)
                if self._vectors is None:
                    self._vectors = vector.reshape(1, -1)
                else:
                    self._vectors = np.vstack([self._vectors, vector.reshape(1, -1)])
        
        logger.info(f"Successfully upserted {total} documents")
    
    def query_similar(
        self, 
        query_embedding: List[float], 
        top_k: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Query the in-memory index for similar vectors.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filter_dict: Optional metadata filter (supports equality and $in)
            
        Returns:
            List of matching documents with scores
        """
        self._ensure_ready()
        
        if self._vectors is None or len(self._ids) == 0:
            return []
        
        mask = np.array(
            [self._matches_filter(meta, filter_dict) for meta in self._metadatas],
            dtype=bool,
        )
        if not np.any(mask):
            return []
        
        candidates = self._vectors[mask]
        candidate_indices = np.nonzero(mask)[0]
        
        query = np.asarray(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query)
        doc_norms = np.linalg.norm(candidates, axis=1)
        denom = doc_norms * query_norm
        denom = np.where(denom == 0, 1e-12, denom)
        scores = (candidates @ query) / denom
        
        k = min(top_k, len(scores))
        top_local = np.argpartition(-scores, kth=k - 1)[:k]
        top_local = top_local[np.argsort(-scores[top_local])]
        
        results = []
        for local_idx in top_local:
            pos = int(candidate_indices[local_idx])
            meta = self._metadatas[pos]
            results.append({
                "id": self._ids[pos],
                "score": float(scores[local_idx]),
                "text": meta.get("text", ""),
                "type": meta.get("type", ""),
                "title": meta.get("title", ""),
                "category": meta.get("category", ""),
                "chunk_type": meta.get("chunk_type", ""),
            })
        
        logger.info(f"Retrieved {len(results)} similar documents")
        return results
    
    def search(self, query_embedding: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None):
        """Alias for query_similar."""
        return self.query_similar(query_embedding, top_k=top_k, filter_dict=filter_dict)
    
    def query(self, query_embedding: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None):
        """Alias for query_similar."""
        return self.query_similar(query_embedding, top_k=top_k, filter_dict=filter_dict)
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the in-memory index."""
        self._ensure_ready()
        return {
            "index_name": self.index_name,
            "total_vectors": len(self._ids),
            "dimension": self.dimension,
            "metric": "cosine"
        }
    
    def delete_index(self) -> None:
        """Delete all vectors and reset the index."""
        self.clear_index()
        self._ready = False
        logger.info("Deleted in-memory vector index")
    
    def clear_index(self) -> None:
        """Clear all vectors from the index without deleting it."""
        self._ensure_ready()
        self._ids = []
        self._metadatas = []
        self._vectors = None
        self._id_to_pos = {}
        logger.info("Cleared all vectors from index")
