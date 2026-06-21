import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Core directories
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "outputs"

# API Keys
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
