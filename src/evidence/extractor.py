from typing import List, Dict, Any
import uuid
from src.evidence.schemas import MetricEvidence, EvidenceUnit
from src.utils.logging import logger

class MockEvidenceExtractor:
    def extract(self, chunks: List[Dict[str, Any]]) -> List[EvidenceUnit]:
        evidence_list = []
        for chunk in chunks:
            # Generate 1 dummy evidence per chunk as a placeholder for LLM extraction
            evidence = MetricEvidence(
                evidence_id=str(uuid.uuid4()),
                chunk_id=chunk["id"],
                section=chunk["section"],
                source_text=chunk["text"],
                metric_name="Mock Revenue",
                value=42.0,
                unit="USD"
            )
            evidence_list.append(evidence)
            
        logger.info(f"Mock extracted {len(evidence_list)} evidence units.")
        return evidence_list
