#!/usr/bin/env python3
"""
Demo script showing the MCP Tool capabilities
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_tool import DocumentLoaderTool

def demo_basic_usage():
    """Demonstrate basic usage of the MCP Tool"""
    print("=" * 60)
    print("MCP Tool Demo: Basic Usage")
    print("=" * 60)
    
    # Create the tool
    tool = DocumentLoaderTool(max_depth=1, timeout=10)
    
    # Example URLs to test (using smaller sites for demo)
    demo_urls = [
        "https://docs.python.org/3/library/os.html",  # Single page for faster demo
        "https://docs.python.org/3/library/json.html",
    ]
    
    for url in demo_urls:
        print(f"\n📚 Loading documentation from: {url}")
        try:
            # Load documentation
            documents = tool.load_documentation(url)
            
            # Show statistics
            stats = tool.get_document_stats()
            print(f"✅ Loaded {stats['total_documents']} documents")
            print(f"📊 Total characters: {stats['total_characters']:,}")
            
            # Create retriever
            print("🔍 Creating retriever...")
            retriever = tool.create_retriever(chunk_size=500, chunk_overlap=100)
            
            # Perform searches
            demo_queries = ["file operations", "JSON parsing", "error handling"]
            
            for query in demo_queries:
                print(f"\n🔎 Searching for: '{query}'")
                results = tool.hybrid_search(query, k=2, search_type="similarity")
                
                if results:
                    print(f"Found {len(results)} relevant documents:")
                    for i, result in enumerate(results[:1], 1):  # Show only first result
                        print(f"\n{i}. Source: {result['source']}")
                        preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                        print(f"   Content: {preview}")
                else:
                    print("No results found")
                    
        except Exception as e:
            print(f"❌ Error processing {url}: {str(e)}")
            continue
        
        print("-" * 60)

def demo_advanced_features():
    """Demonstrate advanced features of the MCP Tool"""
    print("\n" + "=" * 60)
    print("MCP Tool Demo: Advanced Features")
    print("=" * 60)
    
    # Create the tool with custom parameters
    tool = DocumentLoaderTool(max_depth=1, timeout=15)
    
    # Use a documentation site that's likely to be accessible
    url = "https://docs.python.org/3/library/json.html"
    
    print(f"\n📚 Loading documentation from: {url}")
    
    try:
        # Load documentation
        documents = tool.load_documentation(url)
        
        # Create retriever with custom parameters
        print("🔍 Creating retriever with custom parameters...")
        retriever = tool.create_retriever(chunk_size=800, chunk_overlap=150)
        
        # Demonstrate different search types
        query = "JSON encoding"
        search_types = ["similarity", "mmr"]
        
        for search_type in search_types:
            print(f"\n🔎 Performing {search_type} search for: '{query}'")
            results = tool.hybrid_search(query, k=3, search_type=search_type)
            
            if results:
                print(f"Found {len(results)} results using {search_type} search:")
                for i, result in enumerate(results[:2], 1):
                    print(f"\n{i}. Rank: {result['rank']}")
                    preview = result['content'][:150] + "..." if len(result['content']) > 150 else result['content']
                    print(f"   Content: {preview}")
            else:
                print(f"No results found using {search_type} search")
        
        # Show comprehensive statistics
        print("\n📊 Document Statistics:")
        stats = tool.get_document_stats()
        for key, value in stats.items():
            if key != 'sources':
                print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error in advanced demo: {str(e)}")

def main():
    """Main demo function"""
    print("🚀 MCP Tool Demonstration")
    print("This demo showcases the document loading and hybrid search capabilities.")
    print("Note: This demo uses smaller documentation pages for faster execution.")
    
    try:
        # Run basic usage demo
        demo_basic_usage()
        
        # Run advanced features demo
        demo_advanced_features()
        
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        print("=" * 60)
        print("\n💡 Try the tool with your own documentation URLs:")
        print("   python mcp_tool.py --url 'https://docs.python.org/3.9/' --query 'your query here'")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()