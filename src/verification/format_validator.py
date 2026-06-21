from typing import Dict, Any
from src.utils.logging import logger

class FormatValidator:
    """
    Validates the structure of a generated QA pair.
    """
    def validate(self, qa_pair: Dict[str, Any]) -> bool:
        if not isinstance(qa_pair, dict):
            logger.warning("Format validation failed: QA pair is not a dictionary.")
            return False
            
        required_keys = ['question', 'answer', 'evidence']
        for key in required_keys:
            if key not in qa_pair:
                logger.warning(f"Format validation failed: Missing key '{key}'.")
                return False
                
        if not isinstance(qa_pair['question'], str) or not qa_pair['question'].strip():
            logger.warning("Format validation failed: 'question' must be a non-empty string.")
            return False
            
        if not isinstance(qa_pair['answer'], str) or not qa_pair['answer'].strip():
            logger.warning("Format validation failed: 'answer' must be a non-empty string.")
            return False
            
        if not isinstance(qa_pair['evidence'], list) or not qa_pair['evidence']:
            logger.warning("Format validation failed: 'evidence' must be a non-empty list.")
            return False
            
        return True
