import re
from src.utils.logging import logger

class SectionExtractor:
    def __init__(self):
        self.patterns = {
            "business": re.compile(r'(?i)\n\s*item\s+1\.\s*Business\b'),
            "risk_factors": re.compile(r'(?i)\n\s*item\s+1A\.\s*Risk\s+Factors\b'),
            "item_1b": re.compile(r'(?i)\n\s*item\s+1B\.\s*Unresolved\b'),
            "mda": re.compile(r'(?i)\n\s*item\s+7\.\s*Management[^\n]*Discussion\b'),
            "item_7a": re.compile(r'(?i)\n\s*item\s+7A\.\s*Quantitative\b'),
            "financial_statements": re.compile(r'(?i)\n\s*item\s+8\.\s*Financial\s+Statements\b'),
            "item_9": re.compile(r'(?i)\n\s*item\s+9\.\s*Changes\b')
        }
        
    def extract_sections(self, text: str) -> dict:
        positions = {}
        for key, pattern in self.patterns.items():
            matches = list(pattern.finditer(text))
            if matches:
                # Usually the actual section is the last occurrence (after the TOC)
                positions[key] = matches[-1].end()
            else:
                positions[key] = -1
                logger.warning(f"Could not find marker for {key}")
                
        sections = {}
        
        def slice_text(start_key, end_key):
            if positions.get(start_key, -1) != -1 and positions.get(end_key, -1) != -1:
                return text[positions[start_key]:positions[end_key]].strip()
            return ""

        sections["business"] = slice_text("business", "risk_factors")
        sections["risk_factors"] = slice_text("risk_factors", "item_1b")
        sections["mda"] = slice_text("mda", "item_7a")
        sections["financial_statements"] = slice_text("financial_statements", "item_9")
        
        for k, v in sections.items():
            logger.info(f"Extracted section '{k}' with length {len(v)} chars")
            
        return sections
