# Project Improvement & Refactoring Plan

This document outlines a comprehensive plan to quickly refactor, optimize, and modernize the QAGenerator pipeline.

## 1. Remove Dead Code & Scaffolding
The project still contains a lot of initial scaffolding that was replaced by the unified generator. These files clutter the codebase and should be deleted:
- `src/generation/fact_generator.py`
- `src/generation/calculation_generator.py`
- `src/generation/comparison_generator.py`
- `src/generation/synthesis_generator.py`
- `src/generation/generator.py`
- `src/generation/mistral_client.py`

## 2. Asynchronous API Execution
**Current State:** The pipeline uses a synchronous `for` loop with `time.sleep(2)` to iterate through chunks, making sequential calls to the generation and verification models. This is extremely slow.
**Improvement:** 
- Implement Python's `asyncio` alongside `aiohttp` (for OpenRouter) and the async interface of `google-generativeai`.
- Use `asyncio.gather` with a semaphore (e.g., `asyncio.Semaphore(5)`) to process chunks concurrently while respecting rate limits.
- This will reduce the execution time from ~10 minutes down to <1 minute for a 100-pair dataset.

## 3. Advanced Document Parsing (Tables & Context)
**Current State:** `HTMLParser` strips tags using BeautifulSoup, which destroys the semantic structure of financial tables. This severely limits the model's ability to generate "numeric calculation" or "multi-step reasoning" questions.
**Improvement:**
- Integrate `Unstructured.io` or a specialized table-parsing library to retain tabular structures as Markdown.
- Feed the Markdown tables directly into the LLM, dramatically improving the quality of financial QA pairs.

## 4. Enhanced Heuristic Section Extraction
**Current State:** `SectionExtractor` relies on brittle regular expressions (e.g., searching for "Item 1."). 10-K formats vary drastically between companies and years, meaning chunks are often missed or incorrectly boundaries.
**Improvement:**
- Use the `sec-api` Python package (or a dedicated EDGAR parser) which natively understands XBRL and the exact structural tree of SEC filings. This guarantees 100% accurate extraction of the MD&A, Risk Factors, and Financial Statements without regex guessing.

## 5. Few-Shot Prompting for Question Diversity
**Current State:** The `UnifiedGenerator` asks the LLM to randomly "Categorize the question type". This often results in a heavy skew toward simple "fact extraction" questions and very few "multi-step reasoning" questions.
**Improvement:**
- Inject 3-4 highly specific few-shot examples into the `prompt_template` demonstrating exactly what a "multi-step reasoning" question looks like.
- Alternatively, force the LLM to output exactly one question of *each* type for high-density chunks.

## 6. Vector-Based Deduplication
**Current State:** `Deduplicator` does exact or near-exact text matching. It cannot detect if two questions ask the exact same concept using different words.
**Improvement:**
- Compute embeddings for each generated question using a fast local model (e.g., `sentence-transformers/all-MiniLM-L6-v2`).
- Use cosine similarity to deduplicate semantically identical questions, ensuring a highly diverse final benchmark dataset.

---
**Do you approve of these architectural changes?** If so, I can begin executing them immediately!
