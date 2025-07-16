# AK Auto Tool - Structured Project Repository

This repository contains multiple projects organized in a structured format for automated tool development.

## Project Structure

```
ak-auto-tool/
├── proj1/          # MCP Tool for Document Loading and Retrieval
├── proj2/          # Future Project (TBD)
├── proj3/          # Future Project (TBD)
└── README.md       # This file
```

## Projects

### 📚 Project 1: MCP Tool for Document Loading and Retrieval

**Status**: ✅ **Complete**

A comprehensive MCP (Model Context Protocol) suite that provides:

#### Original MCP Tool
- Loads documentation from any Python library's URL
- Uses `langchain_community.document_loaders.RecursiveUrlLoader` for content extraction
- Provides hybrid search capabilities with vector similarity and keyword matching
- Supports multiple search types (similarity, MMR, threshold-based)
- Includes comprehensive CLI and Python API

#### NEW: MCP Website Generator 🆕
- **Recursive Website Scraping**: Crawls websites with configurable depth limits
- **Semantic Search**: Uses SentenceTransformer embeddings for meaningful content matching
- **FAISS Integration**: Efficient vector storage and retrieval
- **MCP Registry**: Centralized management of multiple website retrievers
- **CLI Interface**: Easy-to-use command-line interface
- **Persistent Storage**: Saves indices and metadata for reuse

**Key Features**:
- 🔗 URL-based documentation loading
- 🕷️ Recursive website scraping with depth control
- 🔍 Advanced semantic search with SentenceTransformers
- 📊 Document statistics and insights
- ⚡ Fast FAISS-based vector retrieval
- 🎯 Configurable search parameters
- 🗂️ MCP registry for managing multiple retrievers

**Quick Start**:
```bash
cd proj1
./setup.sh
source venv/bin/activate
pip install sentence-transformers faiss-cpu

# Original MCP tool
python mcp_tool.py --url "https://docs.python.org/3.9/" --query "file operations"

# NEW: Generate MCP from website
python -m mcp_tool.generate_mcp --url "https://www.langchain.com" --name "langchain"

# Query the generated MCP
python -m mcp_tool.generate_mcp --query "langchain" --search "how to use retrievers"
```

**Python API**:
```python
from mcp_tool.mcps.registry import MCP_REGISTRY
results = MCP_REGISTRY["langchain"]("how to use retrievers in langgraph?")
```

See [proj1/README.md](proj1/README.md) and [proj1/mcp_tool/README.md](proj1/mcp_tool/README.md) for detailed documentation.

### 📋 Project 2: Future Project

**Status**: 🔮 **Planning**

Reserved for future development based on upcoming requirements.

### 📋 Project 3: Future Project

**Status**: 🔮 **Planning**

Reserved for future development based on upcoming requirements.

## Getting Started

Each project has its own setup instructions and requirements. Navigate to the specific project folder and follow the README instructions:

1. **For Project 1**: `cd proj1` and follow the setup instructions
2. **For Project 2**: Coming soon
3. **For Project 3**: Coming soon

## Development

This repository follows a structured approach with each project being self-contained:

- Each project has its own `requirements.txt`
- Each project has its own `setup.sh` script
- Each project has comprehensive documentation
- Each project includes examples and demos

## Contributing

Contributions are welcome! Please:
1. Navigate to the specific project folder
2. Follow the project-specific setup instructions
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.