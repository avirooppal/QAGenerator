from src.utils.logging import logger

class MistralClient:
    """
    Mock client for local Mistral to avoid downloading heavy weights during scaffolding.
    """
    def __init__(self, model_path: str = "mistral-7b-v0.1.Q4_K_M.gguf"):
        self.model_path = model_path
        logger.info(f"Loaded local Mistral model from {model_path} (Mocked)")

    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        logger.info(f"Generating completion for prompt (length {len(prompt)})")
        return "This is a mocked completion from local Mistral."
