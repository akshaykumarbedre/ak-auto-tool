# Google AI Overview Scraper

Real-time scraping of Google's AI Overview feature for LLM tooling and retrieval augmented generation (RAG).

## Overview

This project provides a production-ready Python function that extracts AI-generated summaries and cited sources from Google's AI Overview feature, making it ideal for integration with LLM agents and retrieval tools.

## Features

- 🤖 **Real-time AI Overview extraction** from Google Search
- 🔗 **Automatic citation URL collection** from AI responses  
- 💾 **Persistent JSON storage** for caching and inspection
- 🎯 **Graceful error handling** for missing AI Overview
- 🌐 **Playwright-based** browser automation for dynamic content
- ⚡ **Async/sync interfaces** for flexible integration
- 🧪 **Comprehensive testing** with real web data

## Installation

1. Install dependencies:
```bash
cd proj2
pip install -r requirements.txt
playwright install chromium
```

2. Verify installation:
```bash
python -c "from google_ai_scraper import get_google_ai_overview; print('✅ Installation successful')"
```

## Quick Start

### Basic Usage

```python
from google_ai_scraper import get_google_ai_overview

# Get AI overview for a query
result = get_google_ai_overview("how to create retriever using langchain")

print(f"AI Answer: {result['ai_answer']}")
print(f"Sources: {result['referenced_urls']}")
print(f"Search URL: {result['source_url']}")
```

### CLI Usage

```bash
# Basic scraping
python scrape_ai.py "what is machine learning"

# Run with visible browser (debugging)
python scrape_ai.py --no-headless "python async programming"

# Output only JSON
python scrape_ai.py --json "artificial intelligence trends"

# Custom output directory
python scrape_ai.py --output-dir ./my_results "langchain tutorials"
```

## API Reference

### `get_google_ai_overview(query: str, output_dir: str = "outputs", headless: bool = True) -> dict`

Extracts Google AI Overview for the given query.

**Parameters:**
- `query` (str): Search query string
- `output_dir` (str): Directory to save JSON results (default: "outputs")
- `headless` (bool): Run browser in headless mode (default: True)

**Returns:**
```python
{
  "query": "how to create retriever using langchain",
  "ai_answer": "To create a retriever using LangChain, use the VectorstoreRetriever...",
  "referenced_urls": [
    "https://docs.langchain.com/docs/modules/data_connection/retrievers",
    "https://python.langchain.com/docs/integrations/retrievers/faiss"
  ],
  "source_url": "https://www.google.com/search?q=how+to+create+retriever+using+langchain&udm=50"
}
```

### `GoogleAIOverviewScraper` Class

For advanced usage with custom configuration:

```python
from google_ai_scraper import GoogleAIOverviewScraper
import asyncio

# Create scraper instance
scraper = GoogleAIOverviewScraper(output_dir="./data", headless=False)

# Use async interface
async def scrape_multiple():
    queries = ["AI in healthcare", "quantum computing basics"]
    results = []
    for query in queries:
        result = await scraper.get_google_ai_overview_async(query)
        results.append(result)
    return results

results = asyncio.run(scrape_multiple())
```

## Output Format

Results are automatically saved as JSON files in the `outputs/` directory:

**File naming:** `{sanitized_query}.json`

**Example:** `how_to_create_retriever_using_langchain.json`

```json
{
  "query": "how to create retriever using langchain",
  "ai_answer": "To create a retriever using LangChain, you can use the VectorstoreRetriever class...",
  "referenced_urls": [
    "https://docs.langchain.com/docs/modules/data_connection/retrievers",
    "https://python.langchain.com/docs/integrations/retrievers/faiss"
  ],
  "source_url": "https://www.google.com/search?q=how+to+create+retriever+using+langchain&udm=50"
}
```

## Testing

Run the test suite:

```bash
cd proj2
python -m pytest tests/ -v
```

Or run individual test files:

```bash
python tests/test_scraper.py
```

**Note:** Tests perform real web scraping and may take time. Some tests may be skipped if Google AI Overview is not available in your region.

## Known Limitations

- **Regional availability**: Google AI Overview is not available in all regions
- **Rate limiting**: Google may throttle requests; implement delays for production use
- **DOM changes**: Google's page structure may change; selectors are designed to be flexible
- **JavaScript dependency**: Requires full browser rendering via Playwright
- **Network dependency**: Requires internet connection for real-time scraping

## Error Handling

The scraper gracefully handles common issues:

- **Missing AI Overview**: Returns `None` for `ai_answer` when feature is unavailable
- **Network timeouts**: Returns error information in the response
- **Rate limiting**: Logs errors and returns partial data when possible
- **Invalid queries**: Validates input and raises `ValueError` for empty queries

## Integration Examples

### LangChain Integration

```python
from langchain.tools import Tool
from google_ai_scraper import get_google_ai_overview

def google_ai_tool(query: str) -> str:
    """Tool for LangChain agents to get real-time Google AI overviews."""
    result = get_google_ai_overview(query)
    if result['ai_answer']:
        sources = '\n'.join(f"- {url}" for url in result['referenced_urls'])
        return f"{result['ai_answer']}\n\nSources:\n{sources}"
    return "No AI overview available for this query."

# Create LangChain tool
google_tool = Tool(
    name="Google_AI_Overview",
    description="Get real-time AI-generated answers from Google with sources",
    func=google_ai_tool
)
```

### Custom Retriever

```python
from typing import List, Dict
from google_ai_scraper import get_google_ai_overview

class GoogleAIRetriever:
    """Custom retriever using Google AI Overview."""
    
    def retrieve(self, query: str) -> List[Dict]:
        """Retrieve documents from Google AI Overview."""
        result = get_google_ai_overview(query)
        
        documents = []
        if result['ai_answer']:
            documents.append({
                'content': result['ai_answer'],
                'source': 'Google AI Overview',
                'url': result['source_url'],
                'metadata': {
                    'query': query,
                    'referenced_urls': result['referenced_urls']
                }
            })
        
        return documents
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of the ak-auto-tool repository. Please refer to the main repository license.

---

⚠️ **Disclaimer**: This tool is for educational and research purposes. Please respect Google's terms of service and implement appropriate rate limiting for production use.