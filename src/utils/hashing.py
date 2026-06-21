import hashlib

def generate_chunk_id(text: str) -> str:
    """Generate a SHA-256 hash of the chunk text to be used as its ID."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
