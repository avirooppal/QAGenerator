from typing import Dict, Any

class DifficultyScorer:
    """
    Scores the expected difficulty of answering a generated QA pair.
    Returns 'Easy', 'Medium', or 'Hard'.
    """
    def score(self, qa_pair: Dict[str, Any]) -> str:
        question = qa_pair.get("question", "").lower()
        
        # Scaffold heuristic based on question vocabulary
        if "synthesis" in question or "combined impact" in question:
            return "Hard"
        elif "10%" in question or "grew by" in question or "calculate" in question:
            return "Hard"
        elif "compare" in question or "difference" in question or "increase" in question:
            return "Medium"
        else:
            return "Easy"
