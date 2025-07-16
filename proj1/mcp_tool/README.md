# MCP Website Generator

A powerful tool for generating MCP (Model Context Protocol) retrievers from websites. This tool scrapes websites, creates semantic embeddings using SentenceTransformers, stores them in a FAISS index, and provides a callable retriever function for querying the content.

## Features

- **Recursive Website Scraping**: Crawls websites with configurable depth limits
- **Semantic Search**: Uses SentenceTransformer embeddings for meaningful content matching
- **FAISS Integration**: Efficient vector storage and retrieval
- **MCP Registry**: Centralized management of multiple website retrievers
- **CLI Interface**: Easy-to-use command-line interface
- **Persistent Storage**: Saves indices and metadata for reuse

## Installation

```bash
cd proj1
./setup.sh
source venv/bin/activate
pip install sentence-transformers faiss-cpu
```

## Quick Start

### Generate an MCP from a website

```bash
python -m mcp_tool.generate_mcp --url "https://www.langchain.com" --name "langchain"
```

### Use the MCP in Python

```python
from mcp_tool.mcps.registry import MCP_REGISTRY

# Query the MCP
results = MCP_REGISTRY["langchain"]("how to use retrievers in langgraph?")

for result in results:
    print(f"URL: {result['url']}")
    print(f"Title: {result['title']}")
    print(f"Text: {result['text']}")
    print(f"Score: {result['score']:.3f}")
    print("-" * 40)
```

### Alternative Python API

```python
from mcp_tool.generate_mcp import generate_mcp_from_website

# Generate an MCP
success = generate_mcp_from_website(
    base_url="https://www.langchain.com",
    mcp_name="langchain",
    max_depth=2,
    max_pages=100
)

if success:
    print("MCP generated successfully!")
```

## Command Line Interface

### Generate MCP from Website

```bash
# Basic usage
python -m mcp_tool.generate_mcp --url "https://docs.python.org" --name "python_docs"

# With custom settings
python -m mcp_tool.generate_mcp --url "https://docs.python.org" --name "python_docs" \
    --max-depth 3 --max-pages 50 --model "all-MiniLM-L6-v2"
```

### List All MCPs

```bash
python -m mcp_tool.generate_mcp --list
```

### Query an MCP

```bash
python -m mcp_tool.generate_mcp --query "langchain" --search "how to use retrievers"
```

### Delete an MCP

```bash
python -m mcp_tool.generate_mcp --delete "langchain"
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-depth` | Maximum crawling depth | 2 |
| `--max-pages` | Maximum pages to scrape | 100 |
| `--delay` | Delay between requests (seconds) | 1.0 |
| `--timeout` | Request timeout (seconds) | 10 |
| `--model` | SentenceTransformer model | all-MiniLM-L6-v2 |
| `--force` | Force regeneration of existing MCP | False |
| `--results` | Number of search results | 3 |

## Architecture

```
mcp_tool/
├── scrapers/
│   └── website_scraper.py     # Recursive website crawler
├── indexers/
│   └── faiss_indexer.py       # FAISS indexing with embeddings
├── mcps/
│   └── registry.py            # MCP registry and management
└── generate_mcp.py            # Main entry point
```

### Website Scraper

- Uses `requests` and `BeautifulSoup` for web scraping
- Respects robots.txt and includes delays between requests
- Filters out non-content files (PDFs, images, etc.)
- Extracts meaningful text while removing scripts and styles
- Configurable depth limits and page limits

### FAISS Indexer

- Uses SentenceTransformer models for embeddings
- Stores vectors in FAISS index for efficient similarity search
- Normalizes embeddings for cosine similarity
- Saves indices and metadata to disk for persistence

### MCP Registry

- Centralized registry for all generated MCPs
- Lazy loading of indices for memory efficiency
- JSON-based configuration storage
- Automatic MCP function creation

## File Structure

When you generate an MCP, the following files are created:

```
mcp_indices/
├── registry.json              # Registry metadata
├── {mcp_name}_index.faiss     # FAISS vector index
└── {mcp_name}_metadata.pkl    # Document metadata
```

## Advanced Usage

### Custom Models

You can use different SentenceTransformer models:

```python
generate_mcp_from_website(
    base_url="https://example.com",
    mcp_name="example",
    model_name="sentence-transformers/all-mpnet-base-v2"  # More accurate but slower
)
```

### Programmatic Access

```python
from mcp_tool.scrapers.website_scraper import scrape_website
from mcp_tool.indexers.faiss_indexer import build_index

# Scrape website
documents = scrape_website("https://example.com", max_depth=2)

# Build index
build_index(documents, "my_mcp", model_name="all-MiniLM-L6-v2")
```

## Error Handling

The tool includes comprehensive error handling:

- **Network errors**: Skips failed URLs and continues crawling
- **Parsing errors**: Logs warnings and continues processing
- **Missing dependencies**: Clear error messages with installation instructions
- **File I/O errors**: Graceful handling of permission and disk space issues

## Performance Considerations

- **Memory usage**: Indices are loaded on-demand
- **Disk space**: Each MCP requires ~10-50MB depending on content
- **Speed**: Initial generation is slow, but queries are fast
- **Caching**: Reuses downloaded models and parsed content

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies
   ```bash
   pip install sentence-transformers faiss-cpu
   ```

2. **Network timeouts**: Increase timeout or reduce max_pages
   ```bash
   python -m mcp_tool.generate_mcp --timeout 30 --max-pages 50
   ```

3. **Out of memory**: Use smaller model or reduce batch size
   ```bash
   python -m mcp_tool.generate_mcp --model "all-MiniLM-L6-v2"
   ```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Testing

Run the test suite:

```bash
# Offline tests (no network required)
python test_mcp_offline.py

# Full tests (requires internet)
python test_mcp_tool.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details