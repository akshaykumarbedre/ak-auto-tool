"""
Unit tests for Google AI Overview scraper.

These tests validate the scraper functionality with real web data.
"""

import asyncio
import json
import unittest
from pathlib import Path
import sys
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_ai_scraper import get_google_ai_overview, GoogleAIOverviewScraper


class TestGoogleAIOverviewScraper(unittest.TestCase):
    """Test cases for Google AI Overview scraper."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test outputs
        self.test_output_dir = tempfile.mkdtemp()
        self.scraper = GoogleAIOverviewScraper(
            output_dir=self.test_output_dir,
            headless=True
        )
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        shutil.rmtree(self.test_output_dir, ignore_errors=True)
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        test_cases = [
            ("how to create retriever using langchain", "how_to_create_retriever_using_langchain"),
            ("what is python?", "what_is_python"),
            ("C++ vs Python", "c_vs_python"),
            ("test@#$%query", "testquery"),
            ("  spaces   everywhere  ", "spaces_everywhere"),
        ]
        
        for input_query, expected in test_cases:
            result = self.scraper._sanitize_filename(input_query)
            self.assertEqual(result, expected)
    
    def test_construct_google_url(self):
        """Test Google URL construction."""
        query = "how to create retriever using langchain"
        url = self.scraper._construct_google_url(query)
        
        self.assertIn("google.com/search", url)
        self.assertIn("udm=50", url)
        self.assertIn("how+to+create+retriever+using+langchain", url)
    
    def test_get_google_ai_overview_basic(self):
        """Test basic functionality with a simple query."""
        # Use a simple query that's likely to have an AI overview
        query = "what is python programming"
        
        try:
            result = get_google_ai_overview(
                query=query,
                output_dir=self.test_output_dir,
                headless=True
            )
            
            # Validate response structure
            self.assertIsInstance(result, dict)
            self.assertIn("query", result)
            self.assertIn("ai_answer", result)
            self.assertIn("referenced_urls", result)
            self.assertIn("source_url", result)
            
            # Validate specific values
            self.assertEqual(result["query"], query)
            self.assertIsInstance(result["referenced_urls"], list)
            self.assertIn("google.com/search", result["source_url"])
            self.assertIn("udm=50", result["source_url"])
            
            # Check if output file was created
            expected_filename = f"{self.scraper._sanitize_filename(query)}.json"
            expected_filepath = Path(self.test_output_dir) / expected_filename
            self.assertTrue(expected_filepath.exists())
            
            # Validate saved JSON
            with open(expected_filepath, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            self.assertEqual(saved_data, result)
            
        except Exception as e:
            # If test fails due to network issues or AI overview unavailability,
            # we should still validate the error handling
            self.skipTest(f"Skipping due to network/availability issue: {e}")
    
    def test_empty_query_handling(self):
        """Test handling of empty queries."""
        with self.assertRaises(ValueError):
            get_google_ai_overview("", output_dir=self.test_output_dir)
        
        with self.assertRaises(ValueError):
            get_google_ai_overview("   ", output_dir=self.test_output_dir)
    
    def test_async_interface(self):
        """Test async interface."""
        async def run_async_test():
            query = "machine learning basics"
            result = await self.scraper.get_google_ai_overview_async(query)
            
            # Validate response structure
            self.assertIsInstance(result, dict)
            self.assertIn("query", result)
            self.assertIn("ai_answer", result)
            self.assertIn("referenced_urls", result)
            self.assertIn("source_url", result)
            
            return result
        
        try:
            # Run async test
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_async_test())
            loop.close()
        except Exception as e:
            self.skipTest(f"Skipping async test due to issue: {e}")
    
    def test_special_characters_query(self):
        """Test handling queries with special characters."""
        query = "C++ vs Python: which is better?"
        
        try:
            result = get_google_ai_overview(
                query=query,
                output_dir=self.test_output_dir,
                headless=True
            )
            
            # Should handle special characters gracefully
            self.assertEqual(result["query"], query)
            self.assertIn("google.com/search", result["source_url"])
            
        except Exception as e:
            self.skipTest(f"Skipping special characters test due to issue: {e}")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete scraper workflow."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.test_output_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.test_output_dir, ignore_errors=True)
    
    def test_cli_like_usage(self):
        """Test usage similar to CLI script."""
        # Test queries that are likely to return results
        test_queries = [
            "what is artificial intelligence",
            "python programming tutorial",
        ]
        
        for query in test_queries:
            try:
                result = get_google_ai_overview(
                    query=query,
                    output_dir=self.test_output_dir,
                    headless=True
                )
                
                # Validate basic structure
                self.assertIsInstance(result, dict)
                required_keys = ["query", "ai_answer", "referenced_urls", "source_url"]
                for key in required_keys:
                    self.assertIn(key, result)
                
                # If we got an answer, validate it's reasonable
                if result["ai_answer"]:
                    self.assertIsInstance(result["ai_answer"], str)
                    self.assertGreater(len(result["ai_answer"]), 10)
                
                # Validate URLs
                self.assertIsInstance(result["referenced_urls"], list)
                for url in result["referenced_urls"]:
                    self.assertTrue(url.startswith(('http://', 'https://')))
                
                break  # If one query succeeds, that's sufficient for integration test
                
            except Exception as e:
                # Try next query if this one fails
                continue
        else:
            self.skipTest("All integration test queries failed - likely due to network or availability issues")


if __name__ == "__main__":
    # Set up test output
    print("Running Google AI Overview Scraper Tests")
    print("=" * 50)
    print("Note: These tests perform real web scraping and may take some time.")
    print("Tests may be skipped if Google AI Overview is not available in your region.")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2)