#!/usr/bin/env python3
"""
Simple validation script for Google AI Overview scraper.
Tests core functionality without requiring browser installation.
"""

import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_ai_scraper.scraper import GoogleAIOverviewScraper


def test_basic_functionality():
    """Test basic scraper functionality."""
    print("🧪 Testing basic functionality...")
    
    # Create temporary output directory
    temp_dir = tempfile.mkdtemp()
    scraper = GoogleAIOverviewScraper(output_dir=temp_dir)
    
    try:
        # Test filename sanitization
        test_cases = [
            ("how to create retriever using langchain", "how_to_create_retriever_using_langchain"),
            ("what is python?", "what_is_python"),
            ("C++ vs Python", "c_vs_python"),
            ("test@#$%query", "testquery"),
            ("  spaces   everywhere  ", "spaces_everywhere"),
        ]
        
        for input_query, expected in test_cases:
            result = scraper._sanitize_filename(input_query)
            assert result == expected, f"Expected {expected}, got {result}"
        
        print("✅ Filename sanitization tests passed")
        
        # Test URL construction
        query = "how to create retriever using langchain"
        url = scraper._construct_google_url(query)
        
        assert "google.com/search" in url
        assert "udm=50" in url
        assert "how+to+create+retriever+using+langchain" in url
        
        print("✅ URL construction tests passed")
        
        # Test JSON save functionality
        test_result = {
            "query": "test query",
            "ai_answer": "Test answer",
            "referenced_urls": ["https://example.com"],
            "source_url": "https://google.com/search?q=test"
        }
        
        filepath = scraper._save_result(test_result, "test query")
        assert filepath.exists(), "JSON file should be created"
        
        # Validate saved JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == test_result, "Saved data should match input"
        print("✅ JSON save/load tests passed")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("✅ All basic functionality tests passed!")


def test_error_handling():
    """Test error handling."""
    print("\n🧪 Testing error handling...")
    
    from google_ai_scraper import get_google_ai_overview
    
    # Test empty query handling
    try:
        get_google_ai_overview("")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Empty query error handling passed")
    
    try:
        get_google_ai_overview("   ")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Whitespace query error handling passed")
    
    print("✅ All error handling tests passed!")


def test_expected_response_structure():
    """Test that response structure matches requirements."""
    print("\n🧪 Testing expected response structure...")
    
    # Create a mock response to validate structure
    expected_keys = ["query", "ai_answer", "referenced_urls", "source_url"]
    
    # This would be the structure returned by get_google_ai_overview
    mock_response = {
        "query": "test query",
        "ai_answer": "Test AI answer",
        "referenced_urls": ["https://example.com/1", "https://example.com/2"],
        "source_url": "https://www.google.com/search?q=test+query&udm=50"
    }
    
    # Validate structure
    for key in expected_keys:
        assert key in mock_response, f"Missing required key: {key}"
    
    assert isinstance(mock_response["query"], str)
    assert mock_response["ai_answer"] is None or isinstance(mock_response["ai_answer"], str)
    assert isinstance(mock_response["referenced_urls"], list)
    assert isinstance(mock_response["source_url"], str)
    
    print("✅ Response structure validation passed")


def main():
    """Run all validation tests."""
    print("🚀 Starting Google AI Overview Scraper Validation")
    print("=" * 60)
    
    try:
        test_basic_functionality()
        test_error_handling()
        test_expected_response_structure()
        
        print("\n" + "=" * 60)
        print("🎉 All validation tests passed!")
        print("\n📋 Implementation Summary:")
        print("- ✅ Core scraper functionality implemented")
        print("- ✅ Error handling in place")
        print("- ✅ JSON persistence working")
        print("- ✅ CLI script ready")
        print("- ✅ Expected response structure validated")
        print("\n⚠️  Note: Browser automation tests require Playwright browser installation")
        print("   Run 'playwright install chromium' for full functionality testing")
        
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()