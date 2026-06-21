# 10-K Benchmark QA Generator

This project is an automated pipeline that ingests SEC EDGAR 10-K filings, parses the text by section, and generates a structured dataset of high-quality Question-Answer pairs to benchmark Large Language Models.

## Approach & Architecture

The pipeline consists of the following automated stages:
1. **Ingestion (`downloader.py`)**: Fetches the raw HTML 10-K filing directly from the SEC EDGAR database using the company's CIK and the specified fiscal year.
2. **Parsing & Chunking (`html_parser.py`, `section_extractor.py`, `chunker.py`)**: Cleans the HTML into plain text, extracts relevant financial sections (e.g., Business, Risk Factors, MD&A, Financial Statements), and splits the text into ~400-token chunks with an 80-token overlap to maintain context.
3. **Generation (`unified_generator.py`)**: An LLM (via OpenRouter or Gemini) reads each chunk and is prompted to extract up to 2 Question-Answer pairs. It strictly formats the output as JSON, including the question, answer, verbatim source passage, question type, and difficulty.
4. **Verification (`orchestrator.py`, `entailment_model.py`)**: An "LLM-as-a-judge" acts as a strict verifier. It takes the generated answer (hypothesis) and the verbatim source passage (premise) and checks for entailment. If the answer contains any hallucinated information not explicitly stated in the source passage, the QA pair is rejected.
5. **Export (`deduplicator.py`, `jsonl_export.py`, `csv_export.py`)**: Exact duplicate questions are removed, and the final dataset is exported to the `outputs/` directory in both JSONL and CSV formats.

## Design Choices
- **Dual LLM Support**: The pipeline supports both OpenRouter and Google Gemini APIs via a flexible `--llm` CLI flag, allowing you to seamlessly swap out the generation and verification models.
- **Strict Entailment Verification**: To ensure a pristine benchmark dataset, local verification rules were replaced with an LLM-based entailment check. The LLM acts as an impartial judge, aggressively filtering out any ungrounded answers.
- **Array-based Generation**: To comfortably reach the target of 100+ QA pairs, the generation prompt was optimized to extract multiple QA pairs per text chunk.

## Known Limitations
- **API Rate Limits & Costs**: Generating and verifying 100+ QA pairs requires making over 200 API calls. Depending on the LLM provider (like Gemini Free Tier), strict rate limits or payment quotas can interrupt the pipeline before the target is reached.
- **Extraction Brittleness**: 10-K HTML structures vary wildly between companies. The `SectionExtractor` relies on regex heuristics to find sections like "Item 1A. Risk Factors", which may fail or extract incomplete data for certain historically formatted filings.
- **Complex Table Parsing**: The current `HTMLParser` extracts plain text but loses the semantic structure of complex financial tables, meaning "multi-step reasoning" questions involving deeply nested tabular data might be underrepresented.

## Scaling to Multiple Documents or 1000+ Pairs
To scale this pipeline to handle thousands of documents or generate 1000+ pairs:
1. **Asynchronous API Calls**: Move from synchronous linear requests to asynchronous requests (`asyncio` and `aiohttp`) for both LLM generation and verification. This maximizes throughput.
2. **Distributed Queue Processing**: Use a message queue (like Celery, RabbitMQ, or AWS SQS) to decouple ingestion/chunking from generation/verification. Worker nodes can pull chunks and process them in parallel.
3. **Batch APIs**: Both OpenRouter and Gemini offer Batch APIs or higher-tier rate limits. Sending prompts in batch files rather than one-by-one HTTP requests drastically reduces overhead and cost.
4. **Vector Database**: Instead of keeping all chunks in memory, index parsed chunks into a scalable vector database (e.g., Pinecone, Weaviate, or Postgres pgvector) to enable massive-scale retrieval and deduplication.
5. **Caching & Checkpointing**: Save state after every successful chunk to prevent data loss on API timeouts. Implement robust retry mechanisms with exponential backoff for API rate-limit errors (HTTP 429).

## Usage

Set your API key in the terminal and run the pipeline:

```bash
# Using OpenRouter (default)
$env:OPENROUTER_API_KEY="your_key"
python -m src.pipeline --ticker AAPL --year 2023 --llm openrouter

# Using Gemini
$env:GEMINI_API_KEY="your_key"
python -m src.pipeline --ticker AAPL --year 2023 --llm gemini
```
