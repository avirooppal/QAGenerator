# pyrefly: ignore [missing-import]
import google.generativeai as genai
import json
from src.config import GEMINI_API_KEY
from src.utils.logging import logger

class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        if not GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Gemini API calls will fail.")
        else:
            genai.configure(api_key=GEMINI_API_KEY)
            logger.info("Gemini API configured successfully.")
            
        # Using a model that supports generation
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        """Generates a response from the Gemini model based on the given prompt."""
        if not GEMINI_API_KEY:
            # Fallback mock for testing if no key is provided
            logger.warning("No API key, returning mock response.")
            return '{"question": "Mock?", "answer": "Mock Answer", "source_passage": "Mock passage", "question_type": "fact_extraction", "difficulty": "easy"}'
            
        logger.info(f"Sending prompt to Gemini (length: {len(prompt)})...")
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
