#!/usr/bin/env python3
"""
Example usage of Google AI Overview scraper.

This script demonstrates various ways to use the scraper.
"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_ai_scraper import get_google_ai_overview, GoogleAIOverviewScraper


def example_basic_usage():
    """Demonstrate basic usage."""
    print("🤖 Example 1: Basic Usage")
    print("-" * 40)
    
    query = "what is machine learning"
    print(f"Query: {query}")
    
    try:
        result = get_google_ai_overview(query)
        print(f"✅ Result structure: {list(result.keys())}")
        print(f"📍 Search URL: {result['source_url']}")
        
        if result['ai_answer']:
            print(f"🤖 AI Answer (first 100 chars): {result['ai_answer'][:100]}...")
            print(f"📚 Referenced URLs count: {len(result['referenced_urls'])}")
        else:
            print("❌ No AI overview found")
            
    except Exception as e:
        print(f"❌ Error (expected without browser): {e}")


def example_async_usage():
    """Demonstrate async usage."""
    print("\n🚀 Example 2: Async Usage")
    print("-" * 40)
    
    import asyncio
    
    async def scrape_multiple_queries():
        scraper = GoogleAIOverviewScraper(output_dir="example_outputs")
        
        queries = [
            "python programming basics",
            "artificial intelligence overview"
        ]
        
        results = []
        for query in queries:
            print(f"Processing: {query}")
            try:
                result = await scraper.get_google_ai_overview_async(query)
                results.append(result)
                print(f"✅ Processed: {query}")
            except Exception as e:
                print(f"❌ Error for '{query}': {e}")
        
        return results
    
    try:
        # This would work with proper browser installation
        print("Note: This requires 'playwright install chromium' to actually run")
        print("Structure demonstration only...")
        
    except Exception as e:
        print(f"❌ Error (expected without browser): {e}")


def example_cli_integration():
    """Demonstrate CLI integration patterns."""
    print("\n⚡ Example 3: CLI Integration")
    print("-" * 40)
    
    # Example of how this would be used in a larger application
    def search_and_format(query: str) -> str:
        """Format search results for display."""
        try:
            result = get_google_ai_overview(query, headless=True)
            
            if result['ai_answer']:
                formatted = f"""
🔍 Query: {result['query']}
🤖 AI Overview: {result['ai_answer']}
📚 Sources: {', '.join(result['referenced_urls'][:3])}
🔗 Google URL: {result['source_url']}
"""
                return formatted.strip()
            else:
                return f"No AI overview found for: {query}"
                
        except Exception as e:
            return f"Error searching for '{query}': {e}"
    
    # Demonstrate the interface
    example_query = "how to create retriever using langchain"
    print(f"Example query: {example_query}")
    print("Output format:")
    print(search_and_format.__doc__)


def example_langchain_integration():
    """Demonstrate LangChain tool integration."""
    print("\n🔗 Example 4: LangChain Integration")
    print("-" * 40)
    
    # Example tool definition for LangChain
    tool_code = '''
from langchain.tools import Tool
from google_ai_scraper import get_google_ai_overview

def google_ai_tool(query: str) -> str:
    """Get real-time AI overview from Google."""
    result = get_google_ai_overview(query)
    
    if result['ai_answer']:
        sources = '\\n'.join(f"- {url}" for url in result['referenced_urls'])
        return f"{result['ai_answer']}\\n\\nSources:\\n{sources}"
    return "No AI overview available for this query."

# Create LangChain tool
google_tool = Tool(
    name="Google_AI_Overview",
    description="Get real-time AI answers from Google with citations",
    func=google_ai_tool
)
'''
    
    print("LangChain Tool Integration Example:")
    print(tool_code)


def main():
    """Run all examples."""
    print("🎯 Google AI Overview Scraper - Usage Examples")
    print("=" * 60)
    
    example_basic_usage()
    example_async_usage()
    example_cli_integration()
    example_langchain_integration()
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    print("- ✅ Basic synchronous interface demonstrated")
    print("- ✅ Async interface pattern shown")
    print("- ✅ CLI integration example provided")
    print("- ✅ LangChain tool integration template ready")
    print("\n🚀 Ready for production use with 'playwright install chromium'!")


if __name__ == "__main__":
    main()