import argparse
import json
from pathlib import Path
from src.utils.logging import logger
from src.config import DATA_DIR
from src.ingestion.downloader import EDGARDownloader
from src.parsing.html_parser import HTMLParser
from src.parsing.section_extractor import SectionExtractor
from src.parsing.chunker import SentenceSplitter, ChunkBuilder
from src.utils.hashing import generate_chunk_id
from src.evidence.extractor import MockEvidenceExtractor
from src.retrieval.indexer import BM25Indexer
from src.generation.generator import MockQAGenerator

def main():
    parser = argparse.ArgumentParser(description="10-K Benchmark QA Generator Pipeline")
    parser.add_argument("--ticker", type=str, help="Stock ticker symbol (e.g. AAPL)")
    parser.add_argument("--year", type=int, help="Fiscal year to download (e.g. 2023)")
    parser.add_argument("--query", type=str, help="Search query to retrieve relevant chunks")
    parser.add_argument("--llm", type=str, choices=["gemini", "openrouter"], default="openrouter", help="LLM backend to use (gemini or openrouter)")
    
    args = parser.parse_args()
    
    logger.info("Pipeline started")
    
    if args.query:
        logger.info(f"Searching for: '{args.query}'")
        parsed_dir = DATA_DIR / "parsed"
        all_chunks = []
        
        if parsed_dir.exists():
            for filepath in parsed_dir.glob("*_chunks.json"):
                with open(filepath, "r", encoding="utf-8") as f:
                    file_chunks = json.load(f)
                    all_chunks.extend(file_chunks)
                    
        if not all_chunks:
            logger.warning("No chunks found in data/parsed/. Run the pipeline with --ticker and --year first.")
            return
            
        indexer = BM25Indexer()
        indexer.index(all_chunks)
        results = indexer.search(args.query, top_k=3)
        
        print(f"\n--- Top 3 Results for '{args.query}' ---")
        for i, res in enumerate(results):
            print(f"\n[Result {i+1}] (Section: {res.get('section', 'N/A')} | Ticker: {res.get('ticker', 'N/A')})")
            print(f"Text: {res.get('text', '')}")
            
    elif args.ticker and args.year:
        ticker = args.ticker.upper()
        year = args.year
        logger.info(f"Running pipeline for {ticker} year {year}")
        
        # Milestone 1: Ingestion
        downloader = EDGARDownloader()
        html_path = downloader.download_10k(ticker, year)
        
        # Milestone 2: Section Extraction
        html_parser = HTMLParser()
        soup = html_parser.load_html(html_path)
        text = html_parser.extract_text(soup)
        
        extractor = SectionExtractor()
        sections = extractor.extract_sections(text)
        
        # Save parsed sections
        parsed_dir = DATA_DIR / "parsed"
        parsed_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = parsed_dir / f"{ticker}_{year}_sections.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=2)
            
        logger.info(f"Successfully saved sections to {output_file}")
        
        # Milestone 3: Chunking
        splitter = SentenceSplitter()
        builder = ChunkBuilder()
        
        chunks_metadata = []
        for section_name, section_text in sections.items():
            if not section_text:
                continue
            sentences = splitter.split(section_text)
            chunks = builder.build_chunks(sentences)
            
            for chunk_text in chunks:
                chunk_id = generate_chunk_id(chunk_text)
                chunks_metadata.append({
                    "id": chunk_id,
                    "text": chunk_text,
                    "section": section_name,
                    "ticker": ticker,
                    "year": year
                })
        
        chunks_output_file = parsed_dir / f"{ticker}_{year}_chunks.json"
        with open(chunks_output_file, "w", encoding="utf-8") as f:
            json.dump(chunks_metadata, f, indent=2)
            
        logger.info(f"Successfully saved {len(chunks_metadata)} chunks to {chunks_output_file}")
        
        # Milestone 4: Evidence Extraction
        evidence_extractor = MockEvidenceExtractor()
        evidence_units = evidence_extractor.extract(chunks_metadata)
        
        evidence_output_file = parsed_dir / f"{ticker}_{year}_evidence.json"
        with open(evidence_output_file, "w", encoding="utf-8") as f:
            json.dump([e.model_dump() for e in evidence_units], f, indent=2)
            
        logger.info(f"Successfully saved {len(evidence_units)} evidence units to {evidence_output_file}")
        
        # Milestone 6 & 7: QA Generation & Verification
        import time
        from src.generation.openrouter_client import OpenRouterClient
        from src.generation.gemini_client import GeminiClient
        from src.generation.unified_generator import UnifiedGenerator
        from src.verification.orchestrator import VerifierOrchestrator
        from src.export.deduplicator import Deduplicator
        from src.export.jsonl_export import JSONLExporter
        from src.export.csv_export import CSVExporter
        from src.config import OUTPUT_DIR

        if args.llm == "gemini":
            client = GeminiClient()
        else:
            client = OpenRouterClient()
            
        generator = UnifiedGenerator(client)
        orchestrator = VerifierOrchestrator(client)
        
        verified_candidates = []
        target_qa_count = 100
        
        logger.info(f"Starting QA Generation. Target: {target_qa_count} pairs.")
        
        for i, chunk in enumerate(chunks_metadata):
            if len(verified_candidates) >= target_qa_count:
                logger.info(f"Successfully generated {target_qa_count} verified QA pairs. Stopping generation.")
                break
                
            try:
                res_str = generator.generate(chunk)
                qa_arr = json.loads(res_str)
                
                if not isinstance(qa_arr, list):
                    qa_arr = [qa_arr]
                    
                for qa_obj in qa_arr:
                    # Verify the generated QA pair
                    if orchestrator.verify(qa_obj):
                        verified_candidates.append(qa_obj)
                        logger.info(f"Accepted QA pair {len(verified_candidates)}/{target_qa_count}")
                    else:
                        logger.info("QA pair rejected by verifier.")
                    
                    if len(verified_candidates) >= target_qa_count:
                        break
                        
            except Exception as e:
                logger.error(f"Failed to generate/verify QA for chunk {i}: {e}")
                
            # Rate limiting delay
            time.sleep(2)
            
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Milestone 8: Dataset Assembly
        dedup = Deduplicator()
        final_dataset = dedup.deduplicate(verified_candidates)
        
        jsonl_exporter = JSONLExporter()
        csv_exporter = CSVExporter()
        
        final_jsonl_path = OUTPUT_DIR / f"{ticker}_{year}_final_dataset.jsonl"
        final_csv_path = OUTPUT_DIR / f"{ticker}_{year}_final_dataset.csv"
        
        jsonl_exporter.export(final_dataset, final_jsonl_path)
        csv_exporter.export(final_dataset, final_csv_path)
        
        logger.info(f"Pipeline complete! Final dataset size: {len(final_dataset)}")

    else:
        logger.info("No ticker, year, or query provided. Exiting.")

if __name__ == "__main__":
    main()
