"""
MCP Generator - Main Entry Point
===============================

Main function to generate MCP (Model Context Protocol) retrievers from websites.
Coordinates website scraping, embedding generation, and MCP registration.
"""

import argparse
import logging
import os
import sys
from typing import Dict, Any, Optional

from .scrapers.website_scraper import scrape_website
from .indexers.faiss_indexer import build_index
from .mcps.registry import get_registry

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_mcp_from_website(
    base_url: str,
    mcp_name: str,
    max_depth: int = 2,
    max_pages: int = 100,
    model_name: str = "all-MiniLM-L6-v2",
    delay: float = 1.0,
    timeout: int = 10,
    force_regenerate: bool = False,
    save_dir: str = "mcp_indices"
) -> bool:
    """
    Generate an MCP retriever from a website.
    
    Args:
        base_url: Base URL to scrape (e.g., "https://www.langchain.com")
        mcp_name: Name for the MCP (e.g., "langchain")
        max_depth: Maximum depth for recursive crawling
        max_pages: Maximum number of pages to scrape
        model_name: SentenceTransformer model name
        delay: Delay between requests (seconds)
        timeout: Request timeout (seconds)
        force_regenerate: Force regeneration even if MCP exists
        save_dir: Directory to save index files
        
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"Generating MCP '{mcp_name}' from website: {base_url}")
    
    try:
        # Check if MCP already exists
        registry = get_registry()
        if mcp_name in registry.list_mcps() and not force_regenerate:
            logger.info(f"MCP '{mcp_name}' already exists. Use force_regenerate=True to recreate.")
            return False
        
        # Step 1: Scrape the website
        logger.info("Step 1: Scraping website...")
        documents = scrape_website(
            base_url=base_url,
            max_depth=max_depth,
            max_pages=max_pages,
            delay=delay,
            timeout=timeout
        )
        
        if not documents:
            logger.error("No documents scraped. Cannot create MCP.")
            return False
        
        logger.info(f"Successfully scraped {len(documents)} documents")
        
        # Step 2: Build FAISS index
        logger.info("Step 2: Building FAISS index with embeddings...")
        build_index(
            documents=documents,
            mcp_name=mcp_name,
            model_name=model_name,
            save_dir=save_dir
        )
        
        # Step 3: Register the MCP
        logger.info("Step 3: Registering MCP...")
        scrape_config = {
            'max_depth': max_depth,
            'max_pages': max_pages,
            'model_name': model_name,
            'delay': delay,
            'timeout': timeout
        }
        
        registry.register_mcp(mcp_name, base_url, scrape_config)
        
        logger.info(f"✅ Successfully generated MCP '{mcp_name}'!")
        logger.info(f"   Base URL: {base_url}")
        logger.info(f"   Documents: {len(documents)}")
        logger.info(f"   Model: {model_name}")
        
        # Test the MCP
        logger.info("Testing MCP functionality...")
        mcp_func = registry.get_mcp(mcp_name)
        if mcp_func:
            test_results = mcp_func("test query", k=1)
            logger.info(f"✅ MCP test successful. Found {len(test_results)} results.")
        else:
            logger.warning("⚠️  MCP test failed - could not load function")
        
        return True
        
    except Exception as e:
        logger.error(f"Error generating MCP: {str(e)}")
        return False


def list_mcps() -> None:
    """List all registered MCPs."""
    registry = get_registry()
    mcps = registry.list_mcps()
    
    if not mcps:
        print("No MCPs registered.")
        return
    
    print(f"Registered MCPs ({len(mcps)}):")
    print("=" * 50)
    
    for mcp_name in mcps:
        info = registry.get_mcp_info(mcp_name)
        if info:
            print(f"📌 {mcp_name}")
            print(f"   URL: {info['base_url']}")
            print(f"   Created: {info['created_at']}")
            
            if 'stats' in info and info['stats'].get('status') == 'loaded':
                stats = info['stats']
                print(f"   Documents: {stats['total_documents']}")
                print(f"   Model: {stats['model_name']}")
            print()


def query_mcp(mcp_name: str, query: str, k: int = 3) -> None:
    """Query an MCP and display results."""
    registry = get_registry()
    mcp_func = registry.get_mcp(mcp_name)
    
    if not mcp_func:
        print(f"MCP '{mcp_name}' not found.")
        return
    
    print(f"Querying MCP '{mcp_name}' with: '{query}'")
    print("=" * 60)
    
    results = mcp_func(query, k)
    
    if not results:
        print("No results found.")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title'] or 'Untitled'}")
        print(f"   URL: {result['url']}")
        print(f"   Score: {result['score']:.3f}")
        print(f"   Text: {result['text']}")
        print("-" * 40)


def delete_mcp(mcp_name: str) -> None:
    """Delete an MCP."""
    registry = get_registry()
    
    if registry.delete_mcp(mcp_name):
        print(f"✅ Deleted MCP '{mcp_name}'")
    else:
        print(f"❌ Failed to delete MCP '{mcp_name}' (may not exist)")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Generate MCP retrievers from websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate MCP from website
  python generate_mcp.py --url "https://www.langchain.com" --name "langchain"
  
  # Generate with custom settings
  python generate_mcp.py --url "https://docs.python.org" --name "python_docs" --max-depth 3 --max-pages 50
  
  # List all MCPs
  python generate_mcp.py --list
  
  # Query an MCP
  python generate_mcp.py --query "langchain" --search "how to use retrievers"
  
  # Delete an MCP
  python generate_mcp.py --delete "langchain"
        """
    )
    
    # Main actions
    parser.add_argument("--url", help="Base URL to scrape")
    parser.add_argument("--name", help="Name for the MCP")
    parser.add_argument("--list", action="store_true", help="List all registered MCPs")
    parser.add_argument("--query", help="MCP name to query")
    parser.add_argument("--search", help="Search query for MCP")
    parser.add_argument("--delete", help="Delete an MCP")
    
    # Scraping options
    parser.add_argument("--max-depth", type=int, default=2, help="Maximum crawling depth")
    parser.add_argument("--max-pages", type=int, default=100, help="Maximum pages to scrape")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout")
    
    # Model options
    parser.add_argument("--model", default="all-MiniLM-L6-v2", help="SentenceTransformer model")
    
    # Other options
    parser.add_argument("--force", action="store_true", help="Force regeneration of existing MCP")
    parser.add_argument("--results", type=int, default=3, help="Number of search results")
    parser.add_argument("--save-dir", default="mcp_indices", help="Directory to save indices")
    
    args = parser.parse_args()
    
    # Handle different actions
    if args.list:
        list_mcps()
    
    elif args.query and args.search:
        query_mcp(args.query, args.search, args.results)
    
    elif args.delete:
        delete_mcp(args.delete)
    
    elif args.url and args.name:
        success = generate_mcp_from_website(
            base_url=args.url,
            mcp_name=args.name,
            max_depth=args.max_depth,
            max_pages=args.max_pages,
            model_name=args.model,
            delay=args.delay,
            timeout=args.timeout,
            force_regenerate=args.force,
            save_dir=args.save_dir
        )
        
        if success:
            print(f"\n🎉 MCP '{args.name}' ready for use!")
            print(f"Usage example:")
            print(f"  from mcp_tool.mcps.registry import MCP_REGISTRY")
            print(f"  results = MCP_REGISTRY['{args.name}']('your query here')")
        else:
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()