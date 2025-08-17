"""
MCP Server Entry Point
=====================

Main entry point for the LangChain retriever MCP server.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Change to the project root directory to ensure proper file paths
os.chdir(project_root)

from mcp_tool.retriever_mcp_server.server import mcp

# Import tools so they get registered via decorators
import mcp_tool.retriever_mcp_server.tools.langchain_tool

def main():
    """Main function to run the MCP server."""
    print("Starting LangChain Retriever MCP Server...")
    print("Working directory:", os.getcwd())
    print("Tools registered:")
    print("- langchain_search_tool: Query LangChain documentation")
    mcp.run()

if __name__ == "__main__":
    main()