"""
LangChain Search Tool
==================

MCP tool that wraps langchain_mcp() function for querying LangChain documentation.
"""

import sys
import os
import logging

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Change to the project root directory to ensure proper file paths
os.chdir(project_root)

from mcp_tool.retriever_mcp_server.server import mcp
from mcp_tool.mcps.registry import get_registry
from mcp_tool.retriever_mcp_server.mock_langchain import setup_mock_langchain_mcp

logger = logging.getLogger(__name__)

def get_langchain_mcp():
    """Get the langchain MCP function from the registry or use mock."""
    try:
        # Try to get the real langchain MCP first
        registry = get_registry()
        
        # Ensure langchain is registered
        if 'langchain' not in registry.list_mcps():
            logger.info("Registering langchain MCP")
            registry.register_mcp('langchain', 'https://python.langchain.com/docs/', {
                'max_depth': 2,
                'max_pages': 100,
                'model_name': 'all-MiniLM-L6-v2',
                'delay': 1.0,
                'timeout': 10
            })
        
        real_mcp = registry.get_mcp('langchain')
        
        if real_mcp:
            # Test if the real MCP works with a simple query
            try:
                test_results = real_mcp('test', k=1)
                if test_results:  # If we get results, use real MCP
                    logger.info("Using real langchain MCP")
                    return real_mcp
                else:
                    logger.warning("Real langchain MCP returned no results, using mock")
                    return setup_mock_langchain_mcp()
            except Exception as e:
                logger.warning(f"Real langchain MCP failed test: {e}, using mock")
                return setup_mock_langchain_mcp()
        else:
            logger.warning("Real langchain MCP not available, using mock")
            return setup_mock_langchain_mcp()
            
    except Exception as e:
        logger.warning(f"Error accessing real langchain MCP: {e}, using mock")
        return setup_mock_langchain_mcp()

@mcp.tool()
def langchain_search_tool(query: str) -> str:
    """
    Query LangChain documentation and return top match.
    
    Args:
        query: Search query to find relevant LangChain documentation
        
    Returns:
        Top search result from LangChain documentation
    """
    try:
        # Get the langchain MCP function
        langchain_mcp = get_langchain_mcp()
        
        if langchain_mcp is None:
            return "Error: LangChain MCP not available. Please ensure the langchain index is properly set up."
        
        # Query the langchain MCP (get top 3 results)
        results = langchain_mcp(query, k=3)
        
        if not results:
            return f"No results found for query: '{query}'"
        
        # Format the top result
        top_result = results[0]
        
        # Create a formatted response with the top result
        response = f"**LangChain Documentation Search Result**\n\n"
        response += f"**Query:** {query}\n\n"
        response += f"**Title:** {top_result.get('title', 'Untitled')}\n"
        response += f"**URL:** {top_result.get('url', 'N/A')}\n"
        response += f"**Relevance Score:** {top_result.get('score', 0):.3f}\n\n"
        response += f"**Content:**\n{top_result.get('text', 'No content available')[:1000]}"
        
        if len(top_result.get('text', '')) > 1000:
            response += "...\n\n*Content truncated for readability.*"
        
        return response
        
    except Exception as e:
        logger.error(f"Error in langchain_search_tool: {e}")
        return f"Error processing query '{query}': {str(e)}"