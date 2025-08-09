"""
Google AI Overview Scraper Module

Provides real-time scraping of Google's AI Overview feature using Playwright.
"""

import asyncio
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote_plus, urljoin

from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeoutError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleAIOverviewScraper:
    """Scraper class for Google AI Overview feature."""
    
    def __init__(self, output_dir: str = "outputs", headless: bool = True):
        """
        Initialize the scraper.
        
        Args:
            output_dir: Directory to save JSON outputs
            headless: Whether to run browser in headless mode
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.headless = headless
        
    def _sanitize_filename(self, query: str) -> str:
        """Convert query to safe filename."""
        # Replace spaces with underscores and remove special characters
        filename = re.sub(r'[^\w\s-]', '', query.lower())
        filename = re.sub(r'[-\s]+', '_', filename).strip('_')
        return filename[:100]  # Limit filename length
    
    def _construct_google_url(self, query: str) -> str:
        """Construct Google search URL with AI Overview mode."""
        encoded_query = quote_plus(query)
        return f"https://www.google.com/search?q={encoded_query}&udm=50"
    
    async def _extract_ai_overview(self, page: Page) -> Dict[str, Optional[str]]:
        """
        Extract AI overview content and referenced URLs from the page.
        
        Returns:
            Dict with ai_answer and referenced_urls
        """
        try:
            # Wait for page to load
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            # Multiple possible selectors for AI overview content
            ai_overview_selectors = [
                '[data-snhf="1"]',  # Common AI overview container
                '[role="region"][aria-label*="AI"]',
                '.xpdopen',  # Alternative selector
                '.g-blk',    # Another alternative
                '.kno-rdesc',  # Knowledge graph description
            ]
            
            ai_answer = None
            referenced_urls = []
            
            # Try different selectors to find AI overview
            for selector in ai_overview_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        # Get the first matching element
                        element = elements[0]
                        
                        # Extract text content
                        text_content = await element.inner_text()
                        if text_content and len(text_content.strip()) > 50:  # Ensure meaningful content
                            ai_answer = text_content.strip()
                            
                            # Extract URLs from this section
                            links = await element.query_selector_all('a[href]')
                            for link in links:
                                href = await link.get_attribute('href')
                                if href and href.startswith('http'):
                                    # Clean up Google redirect URLs
                                    if '/url?q=' in href:
                                        # Extract actual URL from Google redirect
                                        actual_url = href.split('/url?q=')[1].split('&')[0]
                                        from urllib.parse import unquote
                                        actual_url = unquote(actual_url)
                                        referenced_urls.append(actual_url)
                                    elif not href.startswith('https://www.google.com'):
                                        referenced_urls.append(href)
                            
                            break
                except Exception as e:
                    logger.debug(f"Failed to extract with selector {selector}: {e}")
                    continue
            
            # If no AI overview found, try to get any prominent answer box
            if not ai_answer:
                fallback_selectors = [
                    '.Z0LcW',  # Featured snippet
                    '.kno-rdesc',  # Knowledge panel description
                    '.hgKElc',  # Answer box
                ]
                
                for selector in fallback_selectors:
                    try:
                        element = await page.query_selector(selector)
                        if element:
                            text_content = await element.inner_text()
                            if text_content and len(text_content.strip()) > 20:
                                ai_answer = text_content.strip()
                                break
                    except Exception as e:
                        logger.debug(f"Failed to extract with fallback selector {selector}: {e}")
                        continue
            
            return {
                "ai_answer": ai_answer,
                "referenced_urls": list(dict.fromkeys(referenced_urls))  # Remove duplicates
            }
            
        except Exception as e:
            logger.error(f"Error extracting AI overview: {e}")
            return {"ai_answer": None, "referenced_urls": []}
    
    async def _scrape_google_ai(self, query: str) -> Dict:
        """
        Perform the actual scraping using Playwright.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with scraped data
        """
        google_url = self._construct_google_url(query)
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=self.headless)
            
            try:
                # Create new page with user agent
                page = await browser.new_page()
                await page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                
                logger.info(f"Navigating to: {google_url}")
                
                # Navigate to Google search
                await page.goto(google_url, wait_until='networkidle', timeout=30000)
                
                # Extract AI overview content
                extraction_result = await self._extract_ai_overview(page)
                
                return {
                    "query": query,
                    "ai_answer": extraction_result["ai_answer"],
                    "referenced_urls": extraction_result["referenced_urls"],
                    "source_url": google_url
                }
                
            except PlaywrightTimeoutError:
                logger.error(f"Timeout while loading page for query: {query}")
                return {
                    "query": query,
                    "ai_answer": None,
                    "referenced_urls": [],
                    "source_url": google_url,
                    "error": "Timeout"
                }
            except Exception as e:
                logger.error(f"Error during scraping: {e}")
                return {
                    "query": query,
                    "ai_answer": None,
                    "referenced_urls": [],
                    "source_url": google_url,
                    "error": str(e)
                }
            finally:
                await browser.close()
    
    def _save_result(self, result: Dict, query: str) -> Path:
        """Save result to JSON file."""
        filename = f"{self._sanitize_filename(query)}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Result saved to: {filepath}")
        return filepath
    
    async def get_google_ai_overview_async(self, query: str) -> Dict:
        """
        Async version of get_google_ai_overview.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with AI overview data
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        logger.info(f"Starting AI overview scraping for query: {query}")
        
        # Perform scraping
        result = await self._scrape_google_ai(query.strip())
        
        # Save result
        self._save_result(result, query)
        
        return result


def get_google_ai_overview(query: str, output_dir: str = "outputs", headless: bool = True) -> Dict:
    """
    Synchronous wrapper for getting Google AI Overview.
    
    Args:
        query: Search query string
        output_dir: Directory to save JSON outputs
        headless: Whether to run browser in headless mode
        
    Returns:
        Dictionary containing:
        - query: Original search query
        - ai_answer: AI-generated summary text (None if not found)
        - referenced_urls: List of source URLs cited in the overview
        - source_url: Full Google Search URL used
        
    Example:
        >>> result = get_google_ai_overview("how to create retriever using langchain")
        >>> print(result["ai_answer"])
        >>> print(result["referenced_urls"])
    """
    scraper = GoogleAIOverviewScraper(output_dir=output_dir, headless=headless)
    return asyncio.run(scraper.get_google_ai_overview_async(query))


if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result = get_google_ai_overview(query)
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python google_ai_scraper.py 'your query here'")