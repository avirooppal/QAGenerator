import requests
import json
from src.config import OPENROUTER_API_KEY
from src.utils.logging import logger

class OpenRouterClient:
    def __init__(self, model_name: str = "google/gemini-2.5-flash"):
        self.model_name = model_name
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        if not OPENROUTER_API_KEY:
            logger.warning("OPENROUTER_API_KEY is not set. OpenRouter API calls will fail.")
        else:
            logger.info(f"OpenRouter API configured for model: {model_name}.")

    def generate(self, prompt: str) -> str:
        """Generates a response from the OpenRouter model based on the given prompt."""
        if not OPENROUTER_API_KEY:
            # Fallback mock for testing if no key is provided
            logger.warning("No API key, returning mock response.")
            return '{"question": "Mock?", "answer": "Mock Answer", "source_passage": "Mock passage", "question_type": "fact_extraction", "difficulty": "easy"}'
            
        logger.info(f"Sending prompt to OpenRouter (length: {len(prompt)})...")
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://qagenerator.local", # Optional
            "X-Title": "QAGenerator", # Optional
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"OpenRouter API error: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                logger.error(f"Response body: {response.text}")
            raise
