#!/usr/bin/env python3
"""
Minimal MCP Tool for Document Loading and Retrieval
==================================================

This is a simplified version of the MCP tool that demonstrates the core functionality
without external dependencies for machine learning libraries.

Usage:
    python mcp_tool_minimal.py --url "https://docs.python.org/3/library/os.html" --query "file operations"
"""

import argparse
import logging
import re
import sys
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MinimalDocument:
    """Minimal document class to hold content and metadata."""
    
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.metadata = metadata or {}


class SimpleDocumentLoader:
    """Simple document loader that crawls documentation URLs."""
    
    def __init__(self, max_depth: int = 2, timeout: int = 10):
        self.max_depth = max_depth
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL is valid and within the base domain."""
        parsed = urlparse(url)
        return (
            parsed.scheme in ('http', 'https') and
            parsed.netloc == base_domain and
            not url.endswith(('.pdf', '.zip', '.tar.gz', '.jpg', '.png', '.gif'))
        )
    
    def _extract_text_from_html(self, html: str) -> str:
        """Extract text content from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _crawl_url(self, url: str, visited: set, depth: int, base_domain: str) -> List[MinimalDocument]:
        """Crawl a single URL and return documents."""
        if depth > self.max_depth or url in visited:
            return []
        
        visited.add(url)
        documents = []
        
        try:
            logger.info(f"Crawling: {url} (depth: {depth})")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Extract text content
            text_content = self._extract_text_from_html(response.text)
            
            if text_content.strip():
                doc = MinimalDocument(
                    content=text_content,
                    metadata={
                        'source': url,
                        'title': self._extract_title(response.text),
                        'depth': depth
                    }
                )
                documents.append(doc)
            
            # Find more URLs if not at max depth
            if depth < self.max_depth:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                
                for link in links:
                    href = link['href']
                    full_url = urljoin(url, href)
                    
                    if self._is_valid_url(full_url, base_domain):
                        time.sleep(0.5)  # Be respectful
                        documents.extend(self._crawl_url(full_url, visited, depth + 1, base_domain))
                        
                        # Limit number of URLs per page
                        if len(documents) > 50:
                            break
            
        except Exception as e:
            logger.warning(f"Error crawling {url}: {str(e)}")
        
        return documents
    
    def _extract_title(self, html: str) -> str:
        """Extract title from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        return title.text.strip() if title else 'Untitled'
    
    def load_documentation(self, base_url: str) -> List[MinimalDocument]:
        """Load documentation from a base URL."""
        logger.info(f"Loading documentation from: {base_url}")
        
        base_domain = urlparse(base_url).netloc
        visited = set()
        documents = self._crawl_url(base_url, visited, 0, base_domain)
        
        logger.info(f"Successfully loaded {len(documents)} documents")
        return documents


class SimpleSearchEngine:
    """Simple search engine using keyword matching."""
    
    def __init__(self, documents: List[MinimalDocument]):
        self.documents = documents
        self._build_index()
    
    def _build_index(self):
        """Build a simple keyword index."""
        self.word_index = {}
        
        for i, doc in enumerate(self.documents):
            words = re.findall(r'\b\w+\b', doc.content.lower())
            for word in set(words):
                if word not in self.word_index:
                    self.word_index[word] = []
                self.word_index[word].append(i)
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for documents matching the query."""
        query_words = re.findall(r'\b\w+\b', query.lower())
        
        # Calculate scores for each document
        doc_scores = {}
        
        for word in query_words:
            if word in self.word_index:
                for doc_idx in self.word_index[word]:
                    if doc_idx not in doc_scores:
                        doc_scores[doc_idx] = 0
                    doc_scores[doc_idx] += 1
        
        # Sort by score and return top k
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        
        for i, (doc_idx, score) in enumerate(sorted_docs[:k]):
            doc = self.documents[doc_idx]
            result = {
                'rank': i + 1,
                'content': doc.content,
                'metadata': doc.metadata,
                'source': doc.metadata.get('source', 'Unknown'),
                'relevance_score': score / len(query_words)
            }
            results.append(result)
        
        return results


class MinimalMCPTool:
    """Minimal MCP Tool implementation."""
    
    def __init__(self, max_depth: int = 2, timeout: int = 10):
        self.loader = SimpleDocumentLoader(max_depth, timeout)
        self.documents = []
        self.search_engine = None
    
    def load_documentation(self, base_url: str) -> List[MinimalDocument]:
        """Load documentation from URL."""
        self.documents = self.loader.load_documentation(base_url)
        self.search_engine = SimpleSearchEngine(self.documents)
        return self.documents
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search the loaded documents."""
        if not self.search_engine:
            raise ValueError("No documents loaded. Please load documentation first.")
        
        return self.search_engine.search(query, k)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get document statistics."""
        if not self.documents:
            return {"total_documents": 0}
        
        total_chars = sum(len(doc.content) for doc in self.documents)
        sources = set(doc.metadata.get('source', 'Unknown') for doc in self.documents)
        
        return {
            'total_documents': len(self.documents),
            'total_characters': total_chars,
            'average_document_length': total_chars / len(self.documents),
            'unique_sources': len(sources),
            'sources': list(sources)
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Minimal MCP Tool for Document Loading and Retrieval")
    parser.add_argument("--url", required=True, help="Base URL to load documentation from")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--max-depth", type=int, default=1, help="Maximum depth for crawling")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout")
    parser.add_argument("--results", type=int, default=5, help="Number of results to return")
    parser.add_argument("--stats", action="store_true", help="Show document statistics")
    
    args = parser.parse_args()
    
    try:
        # Create the tool
        tool = MinimalMCPTool(max_depth=args.max_depth, timeout=args.timeout)
        
        # Load documentation
        print(f"Loading documentation from: {args.url}")
        documents = tool.load_documentation(args.url)
        
        # Show statistics
        if args.stats:
            stats = tool.get_stats()
            print("\nDocument Statistics:")
            print(f"Total documents: {stats['total_documents']}")
            print(f"Total characters: {stats['total_characters']:,}")
            print(f"Average document length: {stats['average_document_length']:.0f} characters")
            print(f"Unique sources: {stats['unique_sources']}")
        
        # Perform search
        if args.query:
            print(f"\nSearching for: '{args.query}'")
            results = tool.search(args.query, k=args.results)
            
            if results:
                print(f"\nSearch Results ({len(results)} found):")
                print("=" * 80)
                
                for result in results:
                    print(f"\nRank {result['rank']}: {result['metadata'].get('title', 'Untitled')}")
                    print(f"Source: {result['source']}")
                    print(f"Relevance Score: {result['relevance_score']:.2f}")
                    print("-" * 40)
                    preview = result['content'][:300] + "..." if len(result['content']) > 300 else result['content']
                    print(preview)
                    print()
            else:
                print("No results found.")
        
        print("✅ MCP Tool execution completed successfully!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()