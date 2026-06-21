from typing import List, Dict, Any
from src.generation.schemas import QAPair
from src.utils.logging import logger

class MockQAGenerator:
    def generate(self, evidence_units: List[Dict[str, Any]]) -> List[QAPair]:
        qa_pairs = []
        for evidence in evidence_units:
            # We create 1 dummy QAPair per evidence using the mock data
            evidence_id = evidence.get("evidence_id", "unknown_id")
            metric_name = evidence.get("metric_name", "Metric")
            value = evidence.get("value", "N/A")
            unit = evidence.get("unit", "")
            
            qa_pair = QAPair(
                question=f"What was the reported value for {metric_name}?",
                answer=f"The reported value was {value} {unit}.",
                evidence_ids=[evidence_id]
            )
            qa_pairs.append(qa_pair)
            
        logger.info(f"Mock generated {len(qa_pairs)} QA pairs.")
        return qa_pairs
