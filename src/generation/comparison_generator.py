import json
from src.generation.mistral_client import MistralClient
from src.utils.logging import logger

class ComparisonGenerator:
    def __init__(self, client: MistralClient):
        self.client = client
        self.prompt_template = """
You are a financial analyst. Given the following evidence, generate a comparison-based question and its answer.
Output strictly as JSON in the following format:
{{
  "question": "...",
  "answer": "...",
  "evidence": ["evidence_id"]
}}

Evidence ID: {evidence_id}
Metric: {metric_name}
Value: {value} {unit}
Source Text: {source_text}
"""

    def generate(self, evidence: dict) -> str:
        prompt = self.prompt_template.format(
            evidence_id=evidence.get("evidence_id", ""),
            metric_name=evidence.get("metric_name", "N/A"),
            value=evidence.get("value", "N/A"),
            unit=evidence.get("unit", ""),
            source_text=evidence.get("source_text", "")
        )
        
        logger.info(f"Generated comparison prompt for evidence_id: {evidence.get('evidence_id')}")
        
        # Simulate LLM call with MistralClient
        # In a real app: response = self.client.generate(prompt)
        
        mock_response = {
            "question": f"How does the reported {evidence.get('metric_name', 'metric')} compare to the previous reporting period?",
            "answer": f"The reported value of {evidence.get('value')} {evidence.get('unit')} represents an increase compared to the previous period.",
            "evidence": [evidence.get("evidence_id")]
        }
        
        return json.dumps(mock_response, indent=2)
