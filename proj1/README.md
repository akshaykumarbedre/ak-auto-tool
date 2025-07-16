# MCP Tool for Document Loading and Retrieval

## Overview

The MCP (Model Context Protocol) Tool is a powerful Python application that enables loading documentation from any Python library's URL and provides hybrid search capabilities. This tool uses `langchain_community.document_loaders.RecursiveUrlLoader` to extract documentation and creates a retriever system for efficient document search.

## Features

- 🔗 **URL-based Documentation Loading**: Load documentation from any Python library's documentation URL
- 🔍 **Hybrid Search**: Advanced search capabilities using vector similarity and keyword matching
- 📊 **Document Statistics**: Get insights about loaded documents
- 🎯 **Flexible Search Types**: Support for similarity, MMR, and threshold-based searches
- 📚 **Recursive Loading**: Configurable depth for recursive URL traversal
- ⚡ **Fast Retrieval**: FAISS-based vector store for efficient similarity search

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

2. **Or manually install**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Load documentation and perform search
python mcp_tool.py --url "https://docs.python.org/3.9/" --query "file operations"

# Load LangChain documentation
python mcp_tool.py --url "https://langchain.readthedocs.io/" --query "document loaders"

# Load FastAPI documentation
python mcp_tool.py --url "https://fastapi.tiangolo.com/" --query "authentication"
```

### Advanced Usage

```bash
# Get document statistics
python mcp_tool.py --url "https://docs.python.org/3.9/" --stats

# Customize search parameters
python mcp_tool.py --url "https://docs.python.org/3.9/" --query "async" \
  --results 10 --search-type mmr --max-depth 3

# Adjust text chunking
python mcp_tool.py --url "https://docs.python.org/3.9/" --query "classes" \
  --chunk-size 1500 --chunk-overlap 300
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | Base URL to load documentation from | Required |
| `--query` | Search query for hybrid search | Optional |
| `--max-depth` | Maximum depth for recursive loading | 2 |
| `--timeout` | Timeout for URL requests (seconds) | 10 |
| `--chunk-size` | Chunk size for text splitting | 1000 |
| `--chunk-overlap` | Chunk overlap for text splitting | 200 |
| `--results` | Number of search results to return | 5 |
| `--search-type` | Search type: similarity, mmr, similarity_score_threshold | similarity |
| `--stats` | Show document statistics | False |

## Python API Usage

You can also use the tool programmatically:

```python
from mcp_tool import DocumentLoaderTool

# Create the tool
tool = DocumentLoaderTool(max_depth=2, timeout=10)

# Load documentation
documents = tool.load_documentation("https://docs.python.org/3.9/")

# Create retriever
retriever = tool.create_retriever(chunk_size=1000, chunk_overlap=200)

# Perform hybrid search
results = tool.hybrid_search("file operations", k=5, search_type="similarity")

# Get document statistics
stats = tool.get_document_stats()
print(f"Loaded {stats['total_documents']} documents")
```

## Examples

### Example 1: Python Documentation

```bash
python mcp_tool.py --url "https://docs.python.org/3.9/" --query "file operations" --results 3
```

This will load Python 3.9 documentation and search for content related to file operations.

### Example 2: LangChain Documentation

```bash
python mcp_tool.py --url "https://langchain.readthedocs.io/" --query "document loaders" --search-type mmr
```

This will load LangChain documentation and use MMR (Maximal Marginal Relevance) search for diverse results.

### Example 3: Documentation Statistics

```bash
python mcp_tool.py --url "https://fastapi.tiangolo.com/" --stats
```

This will show statistics about the loaded FastAPI documentation.

## How It Works

1. **Document Loading**: Uses `RecursiveUrlLoader` to crawl the provided URL and extract documentation content
2. **Text Splitting**: Splits documents into manageable chunks using `RecursiveCharacterTextSplitter`
3. **Vector Store**: Creates a FAISS vector store with HuggingFace embeddings for semantic search
4. **Hybrid Search**: Combines semantic similarity with keyword matching for comprehensive search results

## Configuration

### RecursiveUrlLoader Parameters

The tool supports all parameters from `RecursiveUrlLoader`:

- `max_depth`: Maximum depth for recursive URL traversal
- `timeout`: Request timeout in seconds
- `check_response_status`: Whether to check HTTP response status
- `continue_on_failure`: Whether to continue on failed requests
- `prevent_outside`: Whether to prevent loading URLs outside the base domain

### Search Types

- **similarity**: Standard cosine similarity search
- **mmr**: Maximal Marginal Relevance for diverse results
- **similarity_score_threshold**: Threshold-based similarity search

## Troubleshooting

### Common Issues

1. **ImportError**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **Network Errors**: Check internet connection and URL accessibility
3. **Memory Issues**: Reduce `max_depth` or `chunk_size` for large documentation sites
4. **Slow Performance**: Adjust `timeout` and `max_depth` parameters

### Performance Tips

- Use `max_depth=1` for faster loading of large sites
- Increase `chunk_size` for better context but slower processing
- Use `search_type="mmr"` for more diverse search results

## Dependencies

- `langchain-community`: Document loading and vector stores
- `langchain-core`: Core LangChain functionality
- `langchain-text-splitters`: Text splitting utilities
- `faiss-cpu`: Efficient similarity search
- `sentence-transformers`: Embeddings for semantic search
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP requests

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.