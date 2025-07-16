"""
Website Scraper Module
======================

Recursive website crawler with depth limits using requests and BeautifulSoup.
Extracts meaningful text content while filtering out scripts, styles, and noise.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging
from typing import List, Dict, Set, Optional
import re
from requests.exceptions import RequestException, Timeout, ConnectionError

logger = logging.getLogger(__name__)


class WebsiteScraper:
    """
    A recursive website scraper that extracts meaningful text content.
    """
    
    def __init__(self, max_depth: int = 2, max_pages: int = 100, delay: float = 1.0, timeout: int = 10):
        """
        Initialize the website scraper.
        
        Args:
            max_depth: Maximum depth for recursive crawling
            max_pages: Maximum number of pages to scrape
            delay: Delay between requests to be respectful
            timeout: Request timeout in seconds
        """
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; MCP-Tool/1.0)'
        })
        
    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        """
        Check if URL is valid and belongs to the base domain.
        
        Args:
            url: URL to check
            base_domain: Base domain to restrict crawling to
            
        Returns:
            True if URL is valid and internal
        """
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc == base_domain and
                parsed.scheme in ['http', 'https'] and
                not any(ext in url.lower() for ext in ['.pdf', '.doc', '.zip', '.jpg', '.png', '.gif', '.css', '.js'])
            )
        except Exception:
            return False
    
    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """
        Extract meaningful text content from HTML.
        
        Args:
            soup: BeautifulSoup object of the HTML
            
        Returns:
            Cleaned text content
        """
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Extract text from main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', {'id': 'content'}) or soup
        
        text = main_content.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str, base_domain: str) -> Set[str]:
        """
        Extract internal links from the page.
        
        Args:
            soup: BeautifulSoup object of the HTML
            base_url: Base URL for resolving relative links
            base_domain: Base domain to restrict links to
            
        Returns:
            Set of valid internal links
        """
        links = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Remove fragment identifiers
            full_url = full_url.split('#')[0]
            
            if self._is_valid_url(full_url, base_domain):
                links.add(full_url)
        
        return links
    
    def _scrape_page(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape a single page and extract text content.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with URL and text content, or None if failed
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = self._extract_text_content(soup)
            
            # Only include pages with substantial content
            if len(text_content) > 100:
                return {
                    'url': url,
                    'text': text_content,
                    'title': soup.title.string if soup.title else '',
                    'length': len(text_content)
                }
            
        except (RequestException, Timeout, ConnectionError) as e:
            logger.warning(f"Failed to scrape {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {str(e)}")
        
        return None
    
    def scrape_website(self, base_url: str) -> List[Dict[str, str]]:
        """
        Recursively scrape a website starting from the base URL.
        
        Args:
            base_url: Starting URL for scraping
            
        Returns:
            List of dictionaries with 'url' and 'text' keys
        """
        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc
        
        visited = set()
        to_visit = [(base_url, 0)]  # (url, depth)
        results = []
        
        logger.info(f"Starting website scrape from {base_url}")
        logger.info(f"Max depth: {self.max_depth}, Max pages: {self.max_pages}")
        
        while to_visit and len(results) < self.max_pages:
            current_url, current_depth = to_visit.pop(0)
            
            if current_url in visited or current_depth > self.max_depth:
                continue
            
            visited.add(current_url)
            
            logger.info(f"Scraping page {len(results)+1}/{self.max_pages}: {current_url} (depth: {current_depth})")
            
            # Scrape current page
            page_data = self._scrape_page(current_url)
            if page_data:
                results.append(page_data)
                
                # Extract links for further crawling if not at max depth
                if current_depth < self.max_depth:
                    try:
                        response = self.session.get(current_url, timeout=self.timeout)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        links = self._extract_links(soup, current_url, base_domain)
                        
                        for link in links:
                            if link not in visited:
                                to_visit.append((link, current_depth + 1))
                    
                    except Exception as e:
                        logger.warning(f"Failed to extract links from {current_url}: {str(e)}")
            
            # Be respectful with delays
            time.sleep(self.delay)
        
        logger.info(f"Scraping completed. Collected {len(results)} pages.")
        return results


def scrape_website(base_url: str, max_depth: int = 2, max_pages: int = 100, 
                  delay: float = 1.0, timeout: int = 10) -> List[Dict[str, str]]:
    """
    Convenience function to scrape a website.
    
    Args:
        base_url: Starting URL for scraping
        max_depth: Maximum depth for recursive crawling
        max_pages: Maximum number of pages to scrape
        delay: Delay between requests
        timeout: Request timeout
        
    Returns:
        List of dictionaries with 'url' and 'text' keys
    """
    scraper = WebsiteScraper(max_depth, max_pages, delay, timeout)
    return scraper.scrape_website(base_url)