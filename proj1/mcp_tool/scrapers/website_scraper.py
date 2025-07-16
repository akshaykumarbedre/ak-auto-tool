"""
Website Scraper Module
======================

Simplified website scraper using RecursiveUrlLoader for efficient content extraction.
"""

import logging
import re
from typing import List, Dict, Optional
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def bs4_extractor(html: str) -> str:
    """
    Extract clean text from HTML using BeautifulSoup.
    
    Args:
        html: Raw HTML content
        
    Returns:
        Clean text content with normalized whitespace
    """
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


class WebsiteScraper:
    """
    A simplified website scraper using RecursiveUrlLoader for efficient content extraction.
    """
    
    def __init__(self, max_depth: int = 2, max_pages: int = 100, delay: float = 1.0, timeout: int = 10):
        """
        Initialize the website scraper.
        
        Args:
            max_depth: Maximum depth for recursive crawling
            max_pages: Maximum number of pages to scrape (used as max_pages in loader)
            delay: Delay between requests (not used in RecursiveUrlLoader)
            timeout: Request timeout in seconds
        """
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        self.timeout = timeout
        self.documents = []
        
    def scrape_website(self, base_url: str, **kwargs) -> List[Dict[str, str]]:
        """
        Scrape a website using RecursiveUrlLoader.
        
        Args:
            base_url: Starting URL for scraping
            **kwargs: Additional parameters for RecursiveUrlLoader
            
        Returns:
            List of dictionaries with 'url' and 'text' keys
        """
        logger.info(f"Loading documentation from: {base_url}")
        
        # Set up default parameters
        loader_params = {
            "max_depth": self.max_depth,
            "timeout": self.timeout,
            "check_response_status": True,
            "continue_on_failure": True,
            "prevent_outside": True,
            "extractor": bs4_extractor,  # Use BS4 extractor for better content parsing
            **kwargs
        }
        
        try:
            # Create the loader
            loader = RecursiveUrlLoader(base_url, **loader_params)
            
            # Load documents
            self.documents = loader.load()
            logger.info(f"Successfully loaded {len(self.documents)} documents")
            
            # Convert documents to the expected format
            results = []
            for doc in self.documents:
                results.append({
                    'url': doc.metadata.get('source', base_url),
                    'text': doc.page_content,
                    'title': doc.metadata.get('title', ''),
                    'length': len(doc.page_content)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error loading documentation: {str(e)}")
            raise


def scrape_website(base_url: str, max_depth: int = 2, max_pages: int = 100, 
                  delay: float = 1.0, timeout: int = 10) -> List[Dict[str, str]]:
    """
    Convenience function to scrape a website using RecursiveUrlLoader.
    
    Args:
        base_url: Starting URL for scraping
        max_depth: Maximum depth for recursive crawling
        max_pages: Maximum number of pages to scrape
        delay: Delay between requests (not used in RecursiveUrlLoader)
        timeout: Request timeout
        
    Returns:
        List of dictionaries with 'url' and 'text' keys
    """
    scraper = WebsiteScraper(max_depth, max_pages, delay, timeout)
    return scraper.scrape_website(base_url)