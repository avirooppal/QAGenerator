import re
from typing import Dict, Any, List
from src.utils.logging import logger

class NumericValidator:
    """
    Validates that numerical answers mathematically align with the evidence.
    """
    def validate(self, qa_pair: Dict[str, Any], evidence_units: List[Dict[str, Any]]) -> bool:
        question = qa_pair.get("question", "").lower()
        answer = qa_pair.get("answer", "")
        evidence_ids = qa_pair.get("evidence", [])
        
        # Get target evidence
        target_evidence = [ev for ev in evidence_units if ev.get("evidence_id") in evidence_ids]
        if not target_evidence:
            logger.warning("Numeric validator failed: No valid evidence found.")
            return False
            
        # Try to find a numeric value in the evidence
        evidence_values = []
        for ev in target_evidence:
            val = ev.get("value")
            if val is not None:
                try:
                    evidence_values.append(float(val))
                except (ValueError, TypeError):
                    pass
                    
        if not evidence_values:
            # If evidence has no specific value, we skip math checks.
            return True
            
        base_value = evidence_values[0]
        
        # Find numeric values in the answer
        answer_numbers = [float(n) for n in re.findall(r'\b\d+(?:\.\d+)?\b', answer)]
        if not answer_numbers:
            logger.warning("Numeric validator failed: No numbers found in the answer.")
            return False
            
        # Specific rule for our mock CalculationGenerator logic
        if "10%" in question or "grew by 10" in question:
            expected_val = round(base_value * 1.1, 2)
            for ans_num in answer_numbers:
                if abs(ans_num - expected_val) < 0.1:
                    logger.info(f"Numeric validator successfully recomputed: base {base_value} * 1.1 = {expected_val}.")
                    return True
            logger.warning(f"Numeric validator failed: Expected ~{expected_val}, found {answer_numbers}.")
            return False
            
        # Fallback: Check if the base value is present exactly
        for ans_num in answer_numbers:
            if abs(ans_num - base_value) < 0.01:
                logger.info(f"Numeric validator verified exact match of base value {base_value}.")
                return True
                
        logger.warning(f"Numeric validator failed: Could not recompute or match base {base_value} in {answer_numbers}.")
        return False
