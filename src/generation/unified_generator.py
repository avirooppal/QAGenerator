import json
from typing import Any
from src.utils.logging import logger

class UnifiedGenerator:
    def __init__(self, client: Any):
        self.client = client
        self.prompt_template = """
You are an expert financial analyst. Your task is to generate up to 2 high-quality question-answer pairs from the following text chunk extracted from a 10-K filing.

Instructions:
1. Formulate clear, unambiguous questions that can be definitively answered using ONLY the provided text.
2. Provide the correct answers.
3. Extract the exact 'source_passage' from the text that supports each answer. This must be a verbatim substring of the provided text.
4. Categorize the question type as one of: "fact extraction", "numeric calculation", "comparison", or "multi-step reasoning".
5. Estimate the difficulty as "easy", "medium", or "hard".
6. FORCE DIVERSITY: Try to generate at least one "multi-step reasoning", "comparison", or "numeric calculation" question if the text supports it. Avoid generating only simple "fact extraction" questions.

Example of a "multi-step reasoning" question:
Q: If the revenue from services grew by 10% and products dropped by 5%, what is the primary driver of overall margin increase based on the text?
A: The margin increase was driven by the higher gross margin profile of services, which outpaced the product decline.

Output strictly as a valid JSON array of objects in the following format. Do not use markdown blocks like ```json ... ```, just output the raw JSON array starting with [ and ending with ]:
[
  {{
    "question": "...",
    "answer": "...",
    "source_passage": "...",
    "question_type": "...",
    "difficulty": "..."
  }}
]

Text Chunk:
{text_chunk}
"""

    def generate(self, chunk: dict) -> str:
        prompt = self.prompt_template.format(text_chunk=chunk.get("text", ""))
        logger.info(f"Generating QA pair for chunk ID: {chunk.get('id')}")
        
        try:
            response_text = self.client.generate(prompt)
            # Basic cleanup in case the LLM returned markdown code blocks
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            return response_text.strip()
        except Exception as e:
            logger.error(f"Failed to generate QA for chunk {chunk.get('id')}: {e}")
            raise
