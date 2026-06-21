import json
from typing import List, Dict, Any
from src.generation.mistral_client import MistralClient
from src.utils.logging import logger

class SynthesisGenerator:
    def __init__(self, client: MistralClient):
        self.client = client
        self.prompt_template = """
You are a financial analyst. Given the following TWO pieces of evidence, generate a single synthesis-based question that requires combining both facts to answer, along with its answer.
Output strictly as JSON in the following format:
{{
  "question": "...",
  "answer": "...",
  "evidence": ["evidence_id_1", "evidence_id_2"]
}}

--- EVIDENCE 1 ---
Evidence ID: {evidence_id_1}
Metric: {metric_name_1}
Value: {value_1} {unit_1}
Source Text: {source_text_1}

--- EVIDENCE 2 ---
Evidence ID: {evidence_id_2}
Metric: {metric_name_2}
Value: {value_2} {unit_2}
Source Text: {source_text_2}
"""

    def generate(self, evidence_list: List[Dict[str, Any]]) -> str:
        if len(evidence_list) < 2:
            raise ValueError("SynthesisGenerator requires exactly 2 evidence units.")
            
        ev1 = evidence_list[0]
        ev2 = evidence_list[1]
        
        prompt = self.prompt_template.format(
            evidence_id_1=ev1.get("evidence_id", ""),
            metric_name_1=ev1.get("metric_name", "N/A"),
            value_1=ev1.get("value", "N/A"),
            unit_1=ev1.get("unit", ""),
            source_text_1=ev1.get("source_text", ""),
            evidence_id_2=ev2.get("evidence_id", ""),
            metric_name_2=ev2.get("metric_name", "N/A"),
            value_2=ev2.get("value", "N/A"),
            unit_2=ev2.get("unit", ""),
            source_text_2=ev2.get("source_text", "")
        )
        
        logger.info(f"Generated synthesis prompt for evidence_ids: {ev1.get('evidence_id')} and {ev2.get('evidence_id')}")
        
        # Simulate LLM call with MistralClient
        # In a real app: response = self.client.generate(prompt)
        
        mock_response = {
            "question": f"Considering both {ev1.get('metric_name', 'Metric 1')} and {ev2.get('metric_name', 'Metric 2')}, what is the overall synthesis?",
            "answer": f"The combined context of {ev1.get('value')} {ev1.get('unit')} and {ev2.get('value')} {ev2.get('unit')} reveals a broader trend.",
            "evidence": [ev1.get("evidence_id"), ev2.get("evidence_id")]
        }
        
        return json.dumps(mock_response, indent=2)
