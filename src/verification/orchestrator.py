from typing import Dict, Any, List
from src.utils.logging import logger
from src.verification.entailment_model import EntailmentModel
from src.verification.entailment_check import EntailmentChecker

class VerifierOrchestrator:
    """
    Orchestrates the verification pipeline for a generated QA pair.
    """
    def __init__(self, client: Any, evidence_units: List[Dict[str, Any]] = None):
        self.evidence_units = evidence_units or []
        nli_model = EntailmentModel(client)
        self.entailment_check = EntailmentChecker(nli_model)

    def verify(self, qa_pair: Dict[str, Any]) -> bool:
        logger.info(f"Starting verification for question: '{qa_pair.get('question', 'UNKNOWN')}'")
        
        # Verify basic fields exist
        if not qa_pair.get("question") or not qa_pair.get("answer") or not qa_pair.get("source_passage"):
            logger.warning("Verification rejected: Missing required fields.")
            return False
            
        if not self.entailment_check.validate(qa_pair):
            logger.warning("Verification rejected: LLM Entailment Check failed.")
            return False
            
        logger.info("Verification passed all layers!")
        return True
