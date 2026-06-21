from typing import Dict, Any, List
import numpy as np
from src.utils.logging import logger

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    TfidfVectorizer = None

class Deduplicator:
    """
    Removes duplicate QA pairs based on semantic similarity of the question text.
    """
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold

    def deduplicate(self, qa_pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not qa_pairs:
            return []
            
        if TfidfVectorizer is None:
            logger.warning("scikit-learn not installed. Falling back to exact string matching for deduplication.")
            return self._exact_deduplicate(qa_pairs)
            
        questions = [qa.get("question", "").strip().lower() for qa in qa_pairs]
        if not any(questions):
            return qa_pairs
            
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(questions)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        keep_indices = []
        for i in range(len(qa_pairs)):
            # Check if this question is highly similar to any question we've already decided to keep
            is_duplicate = False
            for j in keep_indices:
                if similarity_matrix[i][j] > self.threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                keep_indices.append(i)
                
        unique_pairs = [qa_pairs[i] for i in keep_indices]
        
        duplicates_removed = len(qa_pairs) - len(unique_pairs)
        if duplicates_removed > 0:
            logger.info(f"Deduplicator removed {duplicates_removed} semantically similar questions.")
        else:
            logger.info("Deduplicator found no duplicates.")
            
        return unique_pairs

    def _exact_deduplicate(self, qa_pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_questions = set()
        unique_pairs = []
        for qa in qa_pairs:
            question = qa.get("question", "").strip().lower()
            if question and question not in seen_questions:
                seen_questions.add(question)
                unique_pairs.append(qa)
        return unique_pairs
