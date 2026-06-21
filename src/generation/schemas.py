from pydantic import BaseModel
from typing import List, Literal

class QAPair(BaseModel):
    question: str
    answer: str
    source_passage: str
    question_type: Literal["fact extraction", "numeric calculation", "comparison", "multi-step reasoning"]
    difficulty: Literal["easy", "medium", "hard"]
