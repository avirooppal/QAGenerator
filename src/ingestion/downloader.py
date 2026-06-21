import requests
from pathlib import Path
from src.config import DATA_DIR
from src.utils.logging import logger

class EDGARDownloader:
    def __init__(self, user_agent="QAGenerator user@example.com"):
        self.headers = {"User-Agent": user_agent}
        self.tickers_url = "https://www.sec.gov/files/company_tickers.json"
        
        # Ensure raw directory exists
        self.raw_dir = DATA_DIR / "raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        
    def get_cik(self, ticker: str) -> str:
        resp = requests.get(self.tickers_url, headers=self.headers)
        resp.raise_for_status()
        tickers_data = resp.json()
        
        for entry in tickers_data.values():
            if entry['ticker'].upper() == ticker.upper():
                return str(entry['cik_str']).zfill(10)
        raise ValueError(f"Ticker {ticker} not found in SEC database.")
        
    def download_10k(self, ticker: str, year: int) -> Path:
        ticker = ticker.upper()
        logger.info(f"Downloading 10-K for {ticker} (Year: {year})")
        
        cik_str = self.get_cik(ticker)
        logger.info(f"Found CIK for {ticker}: {cik_str}")
        
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik_str}.json"
        sub_resp = requests.get(submissions_url, headers=self.headers)
        sub_resp.raise_for_status()
        
        recent = sub_resp.json()['filings']['recent']
        target_year = str(year)
        
        for i in range(len(recent['form'])):
            if recent['form'][i] == '10-K':
                if recent['reportDate'][i].startswith(target_year):
                    accession = recent['accessionNumber'][i]
                    primary_doc = recent['primaryDocument'][i]
                    
                    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik_str)}/{accession.replace('-', '')}/{primary_doc}"
                    logger.info(f"Downloading document from {url}")
                    
                    doc_resp = requests.get(url, headers=self.headers)
                    doc_resp.raise_for_status()
                    
                    output_path = self.raw_dir / f"{ticker}_{year}.html"
                    output_path.write_text(doc_resp.text, encoding='utf-8')
                    logger.info(f"Saved filing to {output_path}")
                    
                    return output_path
                    
        raise ValueError(f"No 10-K found for {ticker} for year {year}")
