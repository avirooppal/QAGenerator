import json
from src.generation.mistral_client import MistralClient
from src.utils.logging import logger

class CalculationGenerator:
    def __init__(self, client: MistralClient):
        self.client = client
        self.prompt_template = """
You are a financial analyst. Given the following evidence, generate a calculation-based question and its mathematical answer.
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
        
        logger.info(f"Generated calculation prompt for evidence_id: {evidence.get('evidence_id')}")
        
        # Simulate LLM call with MistralClient
        # In a real app: response = self.client.generate(prompt)
        
        try:
            val = float(evidence.get('value', 0))
            new_val = round(val * 1.1, 2)
        except ValueError:
            val = evidence.get('value', 'N/A')
            new_val = 'N/A'
            
        mock_response = {
            "question": f"Based on the reported {evidence.get('metric_name', 'metric')}, if it grew by 10% next year, what would the new value be?",
            "answer": f"The new value would be {new_val} {evidence.get('unit')}.",
            "evidence": [evidence.get("evidence_id")]
        }
        
        return json.dumps(mock_response, indent=2)
