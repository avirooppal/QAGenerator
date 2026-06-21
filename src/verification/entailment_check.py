from typing import Dict, Any, List
from src.verification.entailment_model import EntailmentModel
from src.utils.logging import logger

class EntailmentChecker:
    """
    Validates that the source evidence logically entails the generated answer.
    """
    def __init__(self, nli_model: EntailmentModel, threshold: float = 0.70):
        self.nli_model = nli_model
        self.threshold = threshold

    def validate(self, qa_pair: Dict[str, Any], evidence_units: List[Dict[str, Any]] = None) -> bool:
        answer_text = qa_pair.get("answer", "")
        premise = qa_pair.get("source_passage", "")
        
        if not premise:
            logger.warning("Entailment check failed: Premise (source_passage) is empty.")
            return False
            
        score = self.nli_model.get_entailment_score(premise=premise, hypothesis=answer_text)
        logger.info(f"Entailment score: {score:.2f} (Threshold: {self.threshold})")
        
        if score >= self.threshold:
            return True
        else:
            logger.warning("Entailment check failed: Score below threshold.")
            return False
