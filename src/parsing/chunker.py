import nltk
import tiktoken
from src.utils.logging import logger

class SentenceSplitter:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)

    def split(self, text: str) -> list[str]:
        if not text:
            return []
        sentences = nltk.sent_tokenize(text)
        logger.info(f"Split text into {len(sentences)} sentences")
        return sentences

class ChunkBuilder:
    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 80, model_name: str = "cl100k_base"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        try:
            self.encoding = tiktoken.get_encoding(model_name)
        except Exception:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def build_chunks(self, sentences: list[str]) -> list[str]:
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = self.count_tokens(sentence)
            
            # If adding this sentence exceeds chunk size and we already have sentences
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                
                # Create overlap for the next chunk
                while current_length > self.chunk_overlap and len(current_chunk) > 1:
                    removed = current_chunk.pop(0)
                    current_length -= self.count_tokens(removed)
            
            current_chunk.append(sentence)
            current_length += sentence_length
            
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        logger.info(f"Built {len(chunks)} chunks")
        return chunks
