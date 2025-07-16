#!/usr/bin/env python3

"""
Main entry point for the MCP server
===================================

This allows the server to be run with `python main.py` or `uv run main.py`
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Change to the project root directory
os.chdir(project_root)

# Import and run the MCP server
from mcp_tool.retriever_mcp_server.main import main

if __name__ == "__main__":
    main()