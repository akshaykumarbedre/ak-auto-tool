"""
MCP Server for LangChain Retriever
================================

FastMCP server instance for exposing LangChain documentation search as an MCP tool.
"""

from mcp.server.fastmcp import FastMCP

# Create the shared MCP server instance
mcp = FastMCP("retriever_mcp_server")