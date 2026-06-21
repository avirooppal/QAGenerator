from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
from pathlib import Path
from src.utils.logging import logger

class HTMLParser:
    def __init__(self, parser_type: str = "lxml"):
        self.parser_type = parser_type
        # SEC filings often start with an XML declaration despite being HTML
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

    def load_html(self, file_path: Path | str) -> BeautifulSoup:
        file_path = Path(file_path)
        logger.info(f"Loading HTML from {file_path}")
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        soup = BeautifulSoup(content, self.parser_type)
        logger.info(f"Successfully parsed HTML to BeautifulSoup object (length: {len(content)} chars)")
        return soup

    def extract_text(self, soup: BeautifulSoup) -> str:
        """
        Extracts plain text from a BeautifulSoup object.
        """
        text = soup.get_text(separator='\n', strip=True)
        logger.info(f"Extracted plain text (length: {len(text)} chars)")
        return text
