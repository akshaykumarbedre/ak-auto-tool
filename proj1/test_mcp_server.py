"""
Comprehensive test for the LangChain MCP server
==============================================

Test that verifies all functionality of the MCP server.
"""

import asyncio
import json
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Change to the project root directory
os.chdir(project_root)

from mcp_tool.retriever_mcp_server.tools.langchain_tool import langchain_search_tool

def test_langchain_search_tool():
    """Test the langchain_search_tool function with various queries."""
    print("🧪 Testing LangChain Search Tool")
    print("=" * 50)
    
    # Test queries covering different aspects of LangChain
    test_queries = [
        "retriever interface",
        "vector store",
        "how to use retrievers",
        "search documentation",
        "RAG system",
        "embeddings"
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: Query '{query}'")
        print("-" * 30)
        
        try:
            result = langchain_search_tool(query)
            
            # Verify the result contains expected structure
            assert "LangChain Documentation Search Result" in result
            assert "Query:" in result
            assert "Title:" in result
            assert "URL:" in result
            assert "Relevance Score:" in result
            assert "Content:" in result
            
            # Extract key information
            lines = result.split('\n')
            title_line = next((line for line in lines if line.startswith("**Title:**")), "")
            url_line = next((line for line in lines if line.startswith("**URL:**")), "")
            score_line = next((line for line in lines if line.startswith("**Relevance Score:**")), "")
            
            print(f"✅ Title: {title_line.replace('**Title:** ', '')}")
            print(f"✅ URL: {url_line.replace('**URL:** ', '')}")
            print(f"✅ Score: {score_line.replace('**Relevance Score:** ', '')}")
            
            results.append({
                "query": query,
                "success": True,
                "title": title_line.replace('**Title:** ', ''),
                "url": url_line.replace('**URL:** ', ''),
                "score": score_line.replace('**Relevance Score:** ', '')
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "query": query,
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    successful_tests = sum(1 for r in results if r["success"])
    total_tests = len(results)
    
    print(f"✅ Successful tests: {successful_tests}/{total_tests}")
    print(f"❌ Failed tests: {total_tests - successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("\n🎉 All tests passed! The MCP server is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return False

def test_server_components():
    """Test that server components can be imported and initialized."""
    print("\n🔧 Testing Server Components")
    print("=" * 50)
    
    try:
        # Test server import
        from mcp_tool.retriever_mcp_server.server import mcp
        print("✅ Server imported successfully")
        
        # Test tool registration
        from mcp_tool.retriever_mcp_server.tools import langchain_tool
        print("✅ Tool module imported successfully")
        
        # Test registry
        from mcp_tool.mcps.registry import get_registry
        registry = get_registry()
        print(f"✅ Registry initialized: {len(registry.list_mcps())} MCPs registered")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 LangChain MCP Server Test Suite")
    print("=" * 60)
    
    # Run component tests
    component_test_passed = test_server_components()
    
    # Run functionality tests
    functionality_test_passed = test_langchain_search_tool()
    
    # Overall result
    print("\n📋 Overall Results")
    print("=" * 60)
    
    if component_test_passed and functionality_test_passed:
        print("🎉 All tests passed! The MCP server is ready to use.")
        print("\n📖 Usage Instructions:")
        print("1. Run the server: python main.py")
        print("2. Configure Claude Desktop to use this server")
        print("3. Query: 'Search LangChain docs for retriever interface'")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)