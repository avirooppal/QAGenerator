from typing import Dict, Any, List
from src.utils.logging import logger

class Deduplicator:
    """
    Removes duplicate QA pairs based on the question text.
    """
    def deduplicate(self, qa_pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_questions = set()
        unique_pairs = []
        
        for qa in qa_pairs:
            question = qa.get("question", "").strip().lower()
            if question and question not in seen_questions:
                seen_questions.add(question)
                unique_pairs.append(qa)
                
        duplicates_removed = len(qa_pairs) - len(unique_pairs)
        if duplicates_removed > 0:
            logger.info(f"Deduplicator removed {duplicates_removed} duplicate questions.")
        else:
            logger.info("Deduplicator found no duplicates.")
            
        return unique_pairs
