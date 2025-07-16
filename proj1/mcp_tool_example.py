#!/usr/bin/env python3
"""
Example usage of the MCP Website Generator
==========================================

This script demonstrates how to use the MCP tool to create semantic retrievers
from websites and query them for relevant content.
"""

import os
import sys
import time

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_tool.generate_mcp import generate_mcp_from_website
from mcp_tool.mcps.registry import MCP_REGISTRY

def demo_with_mock_data():
    """
    Demonstrate MCP functionality with mock data (works offline).
    """
    print("=" * 60)
    print("MCP Website Generator - Demo with Mock Data")
    print("=" * 60)
    
    # Create mock documents for demonstration
    mock_documents = [
        {
            'url': 'https://example.com/machine-learning',
            'text': 'Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns, and make decisions with minimal human intervention. Popular algorithms include linear regression, decision trees, neural networks, and support vector machines.',
            'title': 'Introduction to Machine Learning',
            'length': 350
        },
        {
            'url': 'https://example.com/python-programming',
            'text': 'Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, as well as for use as a scripting or glue language to connect existing components together.',
            'title': 'Python Programming Language',
            'length': 320
        },
        {
            'url': 'https://example.com/data-science',
            'text': 'Data science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data. It combines aspects of statistics, computer science, and domain expertise to analyze complex data sets and solve real-world problems.',
            'title': 'Data Science Overview',
            'length': 290
        },
        {
            'url': 'https://example.com/web-scraping',
            'text': 'Web scraping is the process of extracting data from websites. It involves making HTTP requests to web servers and parsing the returned HTML content to extract specific information. Common tools include BeautifulSoup, Scrapy, and Selenium. Important considerations include respecting robots.txt and rate limiting.',
            'title': 'Web Scraping Techniques',
            'length': 280
        },
        {
            'url': 'https://example.com/neural-networks',
            'text': 'Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information using a connectionist approach. Deep learning, which uses multi-layered neural networks, has achieved remarkable success in image recognition, natural language processing, and game playing.',
            'title': 'Neural Networks and Deep Learning',
            'length': 340
        }
    ]
    
    # Simulate the MCP creation process
    print("📚 Creating MCP from mock website data...")
    
    try:
        # Import required modules
        from mcp_tool.indexers.faiss_indexer import build_index
        from mcp_tool.mcps.registry import get_registry
        
        # Build index with mock data
        print("🔧 Building FAISS index...")
        build_index(mock_documents, "demo_mcp", save_dir="/tmp/demo_indices")
        
        # Register the MCP
        print("📝 Registering MCP...")
        registry = get_registry()
        registry.register_mcp("demo_mcp", "https://example.com", {
            "max_depth": 2,
            "max_pages": 100,
            "model_name": "all-MiniLM-L6-v2"
        })
        
        print("✅ MCP 'demo_mcp' created successfully!")
        
        # Test queries
        print("\n🔍 Testing MCP queries...")
        mcp_func = registry.get_mcp("demo_mcp")
        
        if mcp_func:
            test_queries = [
                "machine learning algorithms",
                "python programming language",
                "data analysis and statistics",
                "web scraping techniques",
                "neural networks deep learning"
            ]
            
            for query in test_queries:
                print(f"\n📝 Query: '{query}'")
                results = mcp_func(query, k=2)
                
                if results:
                    for i, result in enumerate(results, 1):
                        print(f"  {i}. {result['title']} (score: {result['score']:.3f})")
                        print(f"     URL: {result['url']}")
                        print(f"     Text: {result['text'][:100]}...")
                else:
                    print("  No results found")
        else:
            print("❌ Failed to load MCP function")
            
    except ImportError as e:
        print(f"⚠️  Skipping demo due to missing dependencies: {e}")
        print("Please install: pip install sentence-transformers faiss-cpu")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        
    print("\n" + "=" * 60)

def demo_cli_usage():
    """
    Demonstrate CLI usage examples.
    """
    print("=" * 60)
    print("MCP Website Generator - CLI Usage Examples")
    print("=" * 60)
    
    cli_examples = [
        {
            "description": "Generate MCP from a website",
            "command": 'python -m mcp_tool.generate_mcp --url "https://docs.python.org" --name "python_docs"'
        },
        {
            "description": "Generate with custom settings",
            "command": 'python -m mcp_tool.generate_mcp --url "https://langchain.readthedocs.io" --name "langchain" --max-depth 3 --max-pages 50'
        },
        {
            "description": "List all registered MCPs",
            "command": 'python -m mcp_tool.generate_mcp --list'
        },
        {
            "description": "Query an existing MCP",
            "command": 'python -m mcp_tool.generate_mcp --query "langchain" --search "how to use retrievers"'
        },
        {
            "description": "Delete an MCP",
            "command": 'python -m mcp_tool.generate_mcp --delete "langchain"'
        }
    ]
    
    for example in cli_examples:
        print(f"\n📝 {example['description']}:")
        print(f"   {example['command']}")
    
    print("\n" + "=" * 60)

def demo_python_api():
    """
    Demonstrate Python API usage.
    """
    print("=" * 60)
    print("MCP Website Generator - Python API Examples")
    print("=" * 60)
    
    python_examples = [
        {
            "description": "Generate MCP from website",
            "code": '''
from mcp_tool.generate_mcp import generate_mcp_from_website

# Generate an MCP
success = generate_mcp_from_website(
    base_url="https://www.langchain.com",
    mcp_name="langchain",
    max_depth=2,
    max_pages=100
)

if success:
    print("MCP generated successfully!")
'''
        },
        {
            "description": "Use the MCP registry",
            "code": '''
from mcp_tool.mcps.registry import MCP_REGISTRY

# Query the MCP
results = MCP_REGISTRY["langchain"]("how to use retrievers in langgraph?")

for result in results:
    print(f"URL: {result['url']}")
    print(f"Title: {result['title']}")
    print(f"Text: {result['text']}")
    print(f"Score: {result['score']:.3f}")
    print("-" * 40)
'''
        },
        {
            "description": "Direct scraping and indexing",
            "code": '''
from mcp_tool.scrapers.website_scraper import scrape_website
from mcp_tool.indexers.faiss_indexer import build_index

# Scrape website
documents = scrape_website("https://example.com", max_depth=2)

# Build index
build_index(documents, "my_mcp", model_name="all-MiniLM-L6-v2")
'''
        }
    ]
    
    for example in python_examples:
        print(f"\n📝 {example['description']}:")
        print(example['code'])
    
    print("=" * 60)

def main():
    """
    Main demo function.
    """
    print("🚀 MCP Website Generator - Complete Demo")
    print("This demo shows how to use the MCP tool for semantic website search")
    print()
    
    # Show CLI examples
    demo_cli_usage()
    print()
    
    # Show Python API examples
    demo_python_api()
    print()
    
    # Run mock data demo
    demo_with_mock_data()
    
    print("\n🎉 Demo completed!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install sentence-transformers faiss-cpu")
    print("2. Try generating an MCP from a real website")
    print("3. Use the MCP in your applications")
    print("4. Check the README for more detailed documentation")

if __name__ == "__main__":
    main()