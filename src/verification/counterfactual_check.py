from typing import Dict, Any, List
from src.verification.entailment_model import DebertaNLI
from src.utils.logging import logger

class CounterfactualValidator:
    """
    Validates that a deliberately wrong answer does NOT entail the evidence.
    This ensures the NLI check is actually discerning truth from hallucination.
    """
    def __init__(self, nli_model: DebertaNLI, threshold: float = 0.30):
        self.nli_model = nli_model
        # The threshold below which we consider it successfully "rejected"
        self.threshold = threshold

    def validate(self, qa_pair: Dict[str, Any], evidence_units: List[Dict[str, Any]]) -> bool:
        original_answer = qa_pair.get("answer", "")
        evidence_ids = qa_pair.get("evidence", [])
        
        premise = " ".join(
            ev.get("source_text", "") 
            for ev in evidence_units 
            if ev.get("evidence_id") in evidence_ids
        )
        
        if not premise:
            logger.warning("Counterfactual check failed: Premise is empty.")
            return False
            
        # Generate a dummy wrong answer (mocking hallucination generation)
        # We simply prepend a negation to simulate a counterfactual
        wrong_answer = f"NOT TRUE: {original_answer}"
        
        score = self.nli_model.get_entailment_score(premise=premise, hypothesis=wrong_answer)
        logger.info(f"Counterfactual entailment score: {score:.2f} (Should be < {self.threshold})")
        
        # We want the model to REJECT the wrong answer (score < threshold)
        if score < self.threshold:
            logger.info("Counterfactual validation passed (wrong answer correctly rejected).")
            return True
        else:
            logger.warning("Counterfactual validation failed: NLI model incorrectly entailed a wrong answer.")
            return False
