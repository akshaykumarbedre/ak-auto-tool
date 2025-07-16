# LangChain Retriever MCP Server

A Model Context Protocol (MCP) server that exposes LangChain documentation search as a tool that can be used by Claude Desktop or other MCP-compatible clients.

## Features

- **langchain_search_tool**: Query LangChain documentation and return relevant results
- **Semantic Search**: Uses FAISS indexing and embeddings for intelligent document retrieval
- **Fallback Support**: Automatically falls back to mock data when offline
- **Easy Integration**: Works with Claude Desktop and other MCP clients

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
pip install mcp
```

2. The server is ready to run!

## Usage

### Running the Server

```bash
# From the project root
python main.py
```

The server will start and register the `langchain_search_tool` for use by MCP clients.

### Claude Desktop Integration

1. **Configure Claude Desktop**: Add the following to your Claude Desktop configuration file:

**macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "retriever_mcp_server": {
      "command": "python",
      "args": [
        "/ABSOLUTE/PATH/TO/ak-auto-tool/proj1/main.py"
      ],
      "cwd": "/ABSOLUTE/PATH/TO/ak-auto-tool/proj1"
    }
  }
}
```

2. **Restart Claude Desktop** to load the new server configuration.

3. **Use the tool** by asking Claude questions like:
   - "Search LangChain docs for retriever interface"
   - "How do I use vector stores with LangChain?"
   - "Find information about RAG systems in LangChain"

## API Reference

### langchain_search_tool

Query LangChain documentation and return the most relevant result.

**Parameters:**
- `query` (str): Search query to find relevant LangChain documentation

**Returns:**
- Formatted string containing the top search result with:
  - Query used
  - Document title
  - URL
  - Relevance score
  - Content excerpt

**Example:**
```python
result = langchain_search_tool("retriever interface")
# Returns formatted documentation result
```

## Architecture

```
mcp_tool/
├── retriever_mcp_server/
│   ├── tools/
│   │   └── langchain_tool.py         # MCP tool implementation
│   ├── server.py                     # FastMCP server instance
│   ├── main.py                       # Server entry point
│   └── mock_langchain.py             # Fallback mock data
├── mcps/
│   └── registry.py                   # MCP registry system
├── indexers/
│   └── faiss_indexer.py              # FAISS indexing system
└── scrapers/
    └── website_scraper.py            # Web scraping utilities
```

## Testing

Run the test suite to verify functionality:

```bash
python test_mcp_server.py
```

## Troubleshooting

### Internet Connection Issues

The server automatically falls back to mock data when it cannot connect to download embedding models. This ensures the server works even in offline environments.

### Configuration Issues

1. **Server not starting**: Check that all dependencies are installed
2. **Tool not appearing in Claude**: Verify the configuration file paths and restart Claude Desktop
3. **No results returned**: The server will use mock data as fallback

### Logs

The server provides detailed logging to help with troubleshooting:

```
INFO     Using mock langchain MCP
INFO     Registering langchain MCP
INFO     Tools registered: langchain_search_tool
```

## Development

### Adding New Tools

1. Create a new tool file in `mcp_tool/retriever_mcp_server/tools/`
2. Use the `@mcp.tool()` decorator
3. Import the tool in `main.py`

### Extending Search Capabilities

The server can be extended to support:
- Multiple documentation sources
- Different search algorithms
- Custom result formatting
- Additional metadata extraction

## License

This project is part of the ak-auto-tool repository.