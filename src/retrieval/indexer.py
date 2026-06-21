from rank_bm25 import BM25Okapi
from typing import List, Dict, Any
from src.utils.logging import logger

class BM25Indexer:
    def __init__(self):
        self.bm25 = None
        self.chunks = []
        
    def _tokenize(self, text: str) -> List[str]:
        # Simple whitespace tokenization for the "dumb" indexer
        return text.lower().split()

    def index(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        tokenized_corpus = [self._tokenize(chunk["text"]) for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        logger.info(f"Indexed {len(self.chunks)} chunks using BM25.")
        
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.bm25:
            raise ValueError("Corpus not indexed. Call index() first.")
            
        tokenized_query = self._tokenize(query)
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        # Sort indices by score descending
        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
        
        results = [self.chunks[i] for i in top_indices if doc_scores[i] > 0]
        logger.info(f"Query '{query}' returned {len(results)} chunks.")
        return results
