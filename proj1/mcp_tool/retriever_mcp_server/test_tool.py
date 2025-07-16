"""
Test script for the LangChain MCP server
=======================================

Simple test to verify the langchain_search_tool works correctly.
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from server import mcp
from tools.langchain_tool import langchain_search_tool

async def test_langchain_search_tool():
    """Test the langchain_search_tool function."""
    print("Testing langchain_search_tool...")
    
    # Test queries
    test_queries = [
        "retriever interface",
        "vector store",
        "how to use retrievers",
        "search documentation"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing query: '{query}'")
        print('='*60)
        
        try:
            result = langchain_search_tool(query)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    asyncio.run(test_langchain_search_tool())