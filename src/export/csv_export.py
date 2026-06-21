import csv
from pathlib import Path
from typing import Dict, Any, List
from src.utils.logging import logger

class CSVExporter:
    """
    Exports a list of QA pairs to CSV format.
    """
    def export(self, qa_pairs: List[Dict[str, Any]], output_path: Path) -> None:
        if not qa_pairs:
            logger.warning("CSV Exporter: No QA pairs provided to export.")
            return
            
        # Determine headers dynamically or enforce a set
        fieldnames = ["question", "answer", "difficulty", "evidence"]
        
        with open(output_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for qa in qa_pairs:
                row = qa.copy()
                # Ensure the list of evidence IDs is properly stringified for CSV
                if "evidence" in row and isinstance(row["evidence"], list):
                    row["evidence"] = ",".join(str(e) for e in row["evidence"])
                writer.writerow(row)
                
        logger.info(f"Successfully exported {len(qa_pairs)} QA pairs to {output_path}")
