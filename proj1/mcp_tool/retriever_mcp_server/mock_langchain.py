"""
Mock LangChain MCP Function for Testing
=====================================

This creates a mock langchain_mcp function for testing when the actual embeddings model
is not available due to internet connectivity issues.
"""

import logging
import sys
import os

# Add the project root to the Python path  
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Change to the project root directory to ensure proper file paths
os.chdir(project_root)

from mcp_tool.mcps.registry import get_registry

logger = logging.getLogger(__name__)

def create_mock_langchain_mcp():
    """Create a mock langchain_mcp function that returns sample results."""
    def mock_langchain_mcp(query: str, k: int = 3):
        """Mock function that returns sample LangChain documentation results."""
        # Sample results that would come from a real LangChain documentation search
        sample_results = [
            {
                'url': 'https://python.langchain.com/docs/concepts/retrievers/',
                'title': 'Retrievers | LangChain',
                'text': 'Retrievers are responsible for taking in a query and returning a list of relevant documents. They are the core component of retrieval-augmented generation (RAG) systems. The Retriever interface has two main methods: get_relevant_documents() and aget_relevant_documents().',
                'score': 0.892,
                'full_text': 'Retrievers are responsible for taking in a query and returning a list of relevant documents. They are the core component of retrieval-augmented generation (RAG) systems. The Retriever interface has two main methods: get_relevant_documents() and aget_relevant_documents() for async operations. Retrievers can be created from vector stores, search APIs, or custom implementations.'
            },
            {
                'url': 'https://python.langchain.com/docs/how_to/vectorstore_retriever/',
                'title': 'How to use a vector store as a retriever | LangChain',
                'text': 'Vector stores can be used as retrievers. A vector store retriever uses similarity search to find and return the most relevant documents for a given query. This is useful for applications that need to find semantically similar content.',
                'score': 0.845,
                'full_text': 'Vector stores can be used as retrievers. A vector store retriever uses similarity search to find and return the most relevant documents for a given query. This is useful for applications that need to find semantically similar content. You can create a retriever from a vector store using the as_retriever() method.'
            },
            {
                'url': 'https://python.langchain.com/docs/integrations/retrievers/',
                'title': 'Retrievers | LangChain',
                'text': 'LangChain provides many different types of retrievers including vector store retrievers, web search retrievers, and multi-query retrievers. Each retriever has different strengths and is suitable for different use cases.',
                'score': 0.798,
                'full_text': 'LangChain provides many different types of retrievers including vector store retrievers, web search retrievers, and multi-query retrievers. Each retriever has different strengths and is suitable for different use cases. You can combine multiple retrievers using ensemble retrievers for better results.'
            }
        ]
        
        # Filter results based on query keywords for more realistic responses
        query_lower = query.lower()
        relevant_results = []
        
        for result in sample_results:
            if (any(keyword in result['text'].lower() for keyword in query_lower.split()) or 
                any(keyword in result['title'].lower() for keyword in query_lower.split())):
                relevant_results.append(result)
        
        # If no relevant results, return all results
        if not relevant_results:
            relevant_results = sample_results
        
        return relevant_results[:k]
    
    return mock_langchain_mcp

def setup_mock_langchain_mcp():
    """Setup a mock langchain MCP function in the registry."""
    try:
        registry = get_registry()
        
        # Check if we can get the real langchain MCP
        real_mcp = registry.get_mcp('langchain')
        
        if real_mcp:
            # Try to test the real MCP with a simple query
            try:
                test_results = real_mcp('test', k=1)
                if test_results:
                    logger.info("Real langchain MCP is working")
                    return real_mcp
                else:
                    logger.warning("Real langchain MCP returned no results, using mock")
            except Exception as e:
                logger.warning(f"Real langchain MCP failed: {e}, using mock")
        else:
            logger.warning("Real langchain MCP not available, using mock")
            
    except Exception as e:
        logger.warning(f"Error accessing real langchain MCP: {e}, using mock")
    
    # If we get here, use the mock
    logger.info("Using mock langchain MCP")
    return create_mock_langchain_mcp()

# For testing
if __name__ == "__main__":
    mock_mcp = setup_mock_langchain_mcp()
    results = mock_mcp("retriever interface", k=2)
    print("Mock MCP Results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Score: {result['score']:.3f}")
        print(f"   Text: {result['text'][:200]}...")
        print()