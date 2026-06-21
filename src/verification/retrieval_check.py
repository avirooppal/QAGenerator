from typing import Dict, Any, List
from src.retrieval.indexer import BM25Indexer
from src.utils.logging import logger

class RetrievalChecker:
    """
    Validates that a generated QA pair is "retrievable", meaning the generated
    question can successfully retrieve the original evidence chunk in the top-k results.
    """
    def __init__(self, indexer: BM25Indexer):
        self.indexer = indexer

    def validate(self, qa_pair: Dict[str, Any], evidence_units: List[Dict[str, Any]]) -> bool:
        question = qa_pair.get("question", "")
        evidence_ids = qa_pair.get("evidence", [])
        
        # Identify the chunk IDs that correspond to the QA pair's evidence
        target_chunks = set()
        for ev in evidence_units:
            if ev.get("evidence_id") in evidence_ids:
                chunk_id = ev.get("chunk_id")
                if chunk_id:
                    target_chunks.add(chunk_id)
                    
        if not target_chunks:
            logger.warning("Retrieval check failed: No valid target chunks found for evidence.")
            return False
            
        # Search the index for the top 3 chunks
        try:
            results = self.indexer.search(question, top_k=3)
            retrieved_chunk_ids = {res.get("id") for res in results}
        except ValueError:
            # If the indexer is empty or not indexed
            logger.warning("Retrieval check failed: Indexer is empty.")
            return False
        
        # Check if at least one target chunk is retrieved in the top 3
        is_retrievable = bool(target_chunks.intersection(retrieved_chunk_ids))
        
        if not is_retrievable:
            logger.warning("Retrieval check failed: Target chunks not found in top 3 retrieval results.")
            
        return is_retrievable
