#!/usr/bin/env python3
"""
Test script for MCP website generator functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_tool.scrapers.website_scraper import scrape_website
from mcp_tool.indexers.faiss_indexer import build_index, load_index
from mcp_tool.mcps.registry import get_registry
from mcp_tool.generate_mcp import generate_mcp_from_website

def test_basic_functionality():
    """Test basic functionality with mock data"""
    print("Testing MCP website generator...")
    
    # Create mock documents for testing
    mock_documents = [
        {
            'url': 'https://example.com/page1',
            'text': 'This is about machine learning and artificial intelligence. We discuss various algorithms and techniques used in modern AI systems.',
            'title': 'Machine Learning Basics',
            'length': 120
        },
        {
            'url': 'https://example.com/page2', 
            'text': 'Python programming language is versatile and powerful. It is widely used for data science, web development, and automation.',
            'title': 'Python Programming',
            'length': 115
        },
        {
            'url': 'https://example.com/page3',
            'text': 'Deep learning neural networks are a subset of machine learning. They can learn complex patterns from large amounts of data.',
            'title': 'Deep Learning',
            'length': 118
        }
    ]
    
    print("✅ Mock documents created")
    
    # Test FAISS indexing
    try:
        print("Testing FAISS indexing...")
        build_index(mock_documents, "test_mcp", save_dir="/tmp/test_indices")
        print("✅ FAISS index created successfully")
        
        # Test loading index
        indexer = load_index("test_mcp", save_dir="/tmp/test_indices")
        print("✅ FAISS index loaded successfully")
        
        # Test search
        results = indexer.search("machine learning algorithms", k=2)
        print(f"✅ Search completed, found {len(results)} results")
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']} (score: {result['score']:.3f})")
        
    except ImportError as e:
        print(f"⚠️  Skipping FAISS test due to missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ FAISS test failed: {e}")
        return False
    
    # Test registry
    try:
        print("Testing MCP registry...")
        registry = get_registry()
        registry.register_mcp("test_mcp", "https://example.com", {})
        
        mcp_func = registry.get_mcp("test_mcp")
        if mcp_func:
            test_results = mcp_func("python programming", k=1)
            print(f"✅ MCP query successful, found {len(test_results)} results")
            
            if test_results:
                result = test_results[0]
                print(f"  Title: {result['title']}")
                print(f"  URL: {result['url']}")
                print(f"  Score: {result['score']:.3f}")
        else:
            print("❌ Failed to load MCP function")
            return False
            
    except Exception as e:
        print(f"❌ Registry test failed: {e}")
        return False
    
    print("✅ All tests passed!")
    return True

def test_website_scraper():
    """Test website scraper with a mock approach"""
    print("Testing website scraper...")
    
    # Note: In a real environment, this would test actual scraping
    # For now, we'll just verify the scraper can be imported and initialized
    try:
        from mcp_tool.scrapers.website_scraper import WebsiteScraper
        scraper = WebsiteScraper(max_depth=1, max_pages=5)
        print("✅ Website scraper initialized successfully")
        
        # Test URL validation
        is_valid = scraper._is_valid_url("https://example.com/page1", "example.com")
        print(f"✅ URL validation works: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ Website scraper test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running MCP Tool Tests")
    print("=" * 50)
    
    success = True
    
    # Run tests
    success &= test_website_scraper()
    print()
    success &= test_basic_functionality()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! MCP tool is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)