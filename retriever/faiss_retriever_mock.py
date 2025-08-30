"""
Mock FAISS retriever for testing integration without sentence-transformers.
"""
import json
import logging
import numpy as np
import faiss
from pathlib import Path
from typing import List, Dict, Any, Tuple

from retriever.models import SearchResult

logger = logging.getLogger(__name__)


class MockFaissRetriever:
    """Mock FAISS retriever for testing integration."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize mock FAISS retriever with configuration."""
        self.config = config
        self.embedding_config = config.get('embedding', {})
        self.vectorstore_config = config.get('rag', {}).get('vectorstore', {})
        
        # Load FAISS index
        self.index_path = self.vectorstore_config.get('index_path', 'index/faiss/index.faiss')
        self.id_map_path = self.vectorstore_config.get('id_map_path', 'index/faiss/id_map.jsonl')
        self.metric = self.vectorstore_config.get('metric', 'ip')
        self.normalize = self.vectorstore_config.get('normalize', True)
        self.dimension = self.embedding_config.get('dimension', 384)
        
        # Load components
        self.index = None
        self.id_map = []
        
        self._load_index()
    
    def _load_index(self):
        """Load FAISS index and ID mapping."""
        try:
            if not Path(self.index_path).exists():
                raise FileNotFoundError(f"FAISS index not found: {self.index_path}")
            
            # Load FAISS index
            self.index = faiss.read_index(self.index_path)
            logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            
            # Load ID mapping
            if Path(self.id_map_path).exists():
                with open(self.id_map_path, 'r', encoding='utf-8') as f:
                    self.id_map = [json.loads(line.strip()) for line in f]
                logger.info(f"Loaded ID mapping with {len(self.id_map)} entries")
            else:
                logger.warning(f"ID mapping not found: {self.id_map_path}")
                
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {e}")
            raise
    
    def retrieve(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Retrieve relevant regulatory context for a query using mock embeddings.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of SearchResult objects
        """
        if self.index is None:
            raise RuntimeError("FAISS retriever not properly initialized")
        
        # Generate mock query embedding (random but deterministic)
        np.random.seed(hash(query) % 2**32)  # Deterministic based on query
        query_embedding = np.random.randn(1, self.dimension).astype('float32')
        
        # Normalize if configured
        if self.normalize or self.metric == 'ip':
            faiss.normalize_L2(query_embedding)
        
        # Search index
        scores, indices = self.index.search(
            query_embedding.astype('float32'), 
            top_k
        )
        
        # Convert to SearchResult objects
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx < len(self.id_map):  # Valid index
                meta = self.id_map[idx]
                
                # Create SearchResult
                result = SearchResult(
                    snippet=meta.get('text', ''),
                    law_name=meta.get('law_name', 'Unknown'),
                    law_id=meta.get('law_id', 'Unknown'),
                    section_label=meta.get('section_label', ''),
                    jurisdiction=meta.get('jurisdiction', 'Unknown'),
                    source_path=meta.get('source_path', ''),
                    score=float(score),
                    latency_ms=0,  # Will be set by caller
                    start_line=meta.get('meta', {}).get('start_line', 0),
                    end_line=meta.get('meta', {}).get('end_line', 0)
                )
                results.append(result)
        
        logger.info(f"Retrieved {len(results)} results for query: {query}")
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get retriever statistics."""
        return {
            'index_vectors': self.index.ntotal if self.index else 0,
            'dimension': self.dimension,
            'metric': self.metric,
            'normalize': self.normalize,
            'id_map_entries': len(self.id_map),
            'index_path': self.index_path,
            'id_map_path': self.id_map_path
        }
