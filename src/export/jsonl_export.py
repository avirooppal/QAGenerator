import json
from pathlib import Path
from typing import Dict, Any, List
from src.utils.logging import logger

class JSONLExporter:
    """
    Exports a list of QA pairs to JSON Lines format.
    """
    def export(self, qa_pairs: List[Dict[str, Any]], output_path: Path) -> None:
        with open(output_path, "w", encoding="utf-8") as f:
            for qa in qa_pairs:
                f.write(json.dumps(qa) + "\n")
        logger.info(f"Successfully exported {len(qa_pairs)} QA pairs to {output_path}")
