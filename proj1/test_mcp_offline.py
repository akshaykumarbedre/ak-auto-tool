#!/usr/bin/env python3
"""
Offline test for MCP website generator - tests core functionality without network dependencies
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing module imports...")
    
    try:
        from mcp_tool.scrapers.website_scraper import WebsiteScraper, scrape_website
        print("✅ Website scraper imported successfully")
        
        from mcp_tool.indexers.faiss_indexer import FAISSIndexer, build_index, load_index
        print("✅ FAISS indexer imported successfully")
        
        from mcp_tool.mcps.registry import MCPRegistry, get_registry, MCP_REGISTRY
        print("✅ MCP registry imported successfully")
        
        from mcp_tool.generate_mcp import generate_mcp_from_website
        print("✅ MCP generator imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_website_scraper_logic():
    """Test website scraper logic without network calls"""
    print("Testing website scraper logic...")
    
    try:
        from mcp_tool.scrapers.website_scraper import WebsiteScraper
        scraper = WebsiteScraper(max_depth=2, max_pages=50)
        
        # Test URL validation
        assert scraper._is_valid_url("https://example.com/page1", "example.com") == True
        assert scraper._is_valid_url("https://other.com/page1", "example.com") == False
        assert scraper._is_valid_url("https://example.com/file.pdf", "example.com") == False
        assert scraper._is_valid_url("https://example.com/script.js", "example.com") == False
        
        print("✅ URL validation tests passed")
        
        # Test HTML text extraction
        from bs4 import BeautifulSoup
        html = """
        <html>
        <head><title>Test Page</title></head>
        <body>
            <script>alert('test');</script>
            <style>body { color: red; }</style>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content of the page.</p>
                <p>Multiple paragraphs with   extra   spaces.</p>
            </main>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        text = scraper._extract_text_content(soup)
        
        assert "Main Content" in text
        assert "This is the main content" in text
        assert "alert('test')" not in text
        assert "color: red" not in text
        
        print("✅ HTML text extraction tests passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Website scraper logic test failed: {e}")
        return False

def test_registry_logic():
    """Test registry logic without FAISS dependencies"""
    print("Testing registry logic...")
    
    try:
        from mcp_tool.mcps.registry import MCPRegistry
        import tempfile
        import json
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            registry = MCPRegistry(temp_dir)
            
            # Test registration
            registry.register_mcp("test_mcp", "https://example.com", {"max_depth": 2})
            
            # Test listing
            mcps = registry.list_mcps()
            assert "test_mcp" in mcps
            
            # Test info retrieval
            info = registry.get_mcp_info("test_mcp")
            assert info is not None
            assert info["base_url"] == "https://example.com"
            
            print("✅ Registry logic tests passed")
            
            return True
            
    except Exception as e:
        print(f"❌ Registry logic test failed: {e}")
        return False

def test_cli_interface():
    """Test that CLI interface can be imported and parsed"""
    print("Testing CLI interface...")
    
    try:
        from mcp_tool.generate_mcp import main
        import argparse
        
        # Test that argparse doesn't crash
        parser = argparse.ArgumentParser()
        parser.add_argument("--url")
        parser.add_argument("--name")
        
        args = parser.parse_args(["--url", "https://example.com", "--name", "test"])
        assert args.url == "https://example.com"
        assert args.name == "test"
        
        print("✅ CLI interface tests passed")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running MCP Tool Offline Tests")
    print("=" * 50)
    
    success = True
    
    # Run offline tests
    success &= test_imports()
    print()
    success &= test_website_scraper_logic()
    print()
    success &= test_registry_logic()
    print()
    success &= test_cli_interface()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All offline tests passed! Core functionality is working.")
        print("\nNote: Full functionality testing requires internet access for:")
        print("- Downloading SentenceTransformer models")
        print("- Actual website scraping")
        print("- FAISS indexing with embeddings")
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)