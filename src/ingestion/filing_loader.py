from dataclasses import dataclass
import requests

@dataclass
class FilingMetadata:
    ticker: str
    accession_number: str
    company_name: str
    filing_year: int

class FilingMetadataExtractor:
    def __init__(self, user_agent="QAGenerator user@example.com"):
        self.headers = {"User-Agent": user_agent}
        self.tickers_url = "https://www.sec.gov/files/company_tickers.json"

    def extract(self, ticker: str, year: int) -> FilingMetadata:
        resp = requests.get(self.tickers_url, headers=self.headers)
        resp.raise_for_status()
        tickers_data = resp.json()
        
        cik_str = None
        company_name = None
        for entry in tickers_data.values():
            if entry['ticker'].upper() == ticker.upper():
                cik_str = str(entry['cik_str']).zfill(10)
                company_name = entry['title']
                break
                
        if not cik_str:
            raise ValueError(f"Ticker {ticker} not found in SEC database.")
            
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik_str}.json"
        sub_resp = requests.get(submissions_url, headers=self.headers)
        sub_resp.raise_for_status()
        
        recent = sub_resp.json()['filings']['recent']
        target_year = str(year)
        
        for i in range(len(recent['form'])):
            if recent['form'][i] == '10-K':
                if recent['reportDate'][i].startswith(target_year):
                    accession = recent['accessionNumber'][i]
                    return FilingMetadata(
                        ticker=ticker.upper(),
                        accession_number=accession,
                        company_name=company_name,
                        filing_year=year
                    )
                    
        raise ValueError(f"No 10-K found for {ticker} for year {year}")
