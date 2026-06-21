import re
from typing import Dict, Any, List
from src.utils.logging import logger

class SpanChecker:
    """
    Validates that numeric values or key spans in the generated answer 
    actually exist in the original source evidence text.
    """
    def validate(self, qa_pair: Dict[str, Any], evidence_units: List[Dict[str, Any]]) -> bool:
        answer_text = qa_pair.get("answer", "").lower()
        evidence_ids = qa_pair.get("evidence", [])
        
        # Combine all source texts associated with the evidence IDs
        combined_source = " ".join(
            ev.get("source_text", "").lower() 
            for ev in evidence_units 
            if ev.get("evidence_id") in evidence_ids
        )
        
        if not combined_source:
            logger.warning("Span check failed: No matching source text found for evidence IDs.")
            return False
            
        # Strict scaffold check: Ensure all numbers generated in the answer 
        # are explicitly present in the source text.
        numbers_in_answer = set(re.findall(r'\b\d+(?:\.\d+)?\b', answer_text))
        
        for num in numbers_in_answer:
            if num not in combined_source:
                logger.warning(f"Span check failed: Number '{num}' in answer not found in source text.")
                return False
                
        return True
