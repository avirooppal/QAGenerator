from typing import Any
from src.utils.logging import logger

class EntailmentModel:
    """
    Uses an LLM (Gemini or OpenRouter) as a judge to verify if a given hypothesis (answer)
    is entailed by the premise (source passage).
    """
    def __init__(self, client: Any):
        self.client = client
        self.prompt_template = """
You are an expert fact-checker. Given a premise (a text passage) and a hypothesis (an answer to a question), determine if the hypothesis is fully supported and entailed by the premise.

Premise: {premise}
Hypothesis: {hypothesis}

Respond with exactly "YES" if the hypothesis is fully supported by the premise. 
Respond with exactly "NO" if the hypothesis contains outside information, is contradictory, or is not fully supported by the premise.
"""

    def get_entailment_score(self, premise: str, hypothesis: str) -> float:
        """
        Returns 1.0 if entailed, 0.0 otherwise.
        """
        logger.info(f"Checking entailment using LLM-as-a-judge...")
        if not premise.strip() or not hypothesis.strip():
            return 0.0
            
        prompt = self.prompt_template.format(premise=premise, hypothesis=hypothesis)
        try:
            response = self.client.generate(prompt)
            if "YES" in response.upper():
                return 1.0
            return 0.0
        except Exception as e:
            logger.error(f"Entailment check failed: {e}")
            return 0.0
