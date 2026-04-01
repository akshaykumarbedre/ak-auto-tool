#!/usr/bin/env python3
"""
CLI script for testing Google AI Overview scraper.

Usage:
    python scrape_ai.py "your query here"
    python scrape_ai.py "how to create retriever using langchain"
"""

import argparse
import json
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from google_ai_scraper import get_google_ai_overview


def main():
    parser = argparse.ArgumentParser(
        description="Scrape Google AI Overview for a given query",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_ai.py "how to create retriever using langchain"
  python scrape_ai.py "what is machine learning"
  python scrape_ai.py --no-headless "python async programming"
        """
    )
    
    parser.add_argument(
        "query",
        help="Search query to get AI overview for"
    )
    
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory to save JSON results (default: outputs)"
    )
    
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser in non-headless mode (visible)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output only JSON result without formatting"
    )
    
    args = parser.parse_args()
    
    try:
        # Perform scraping
        result = get_google_ai_overview(
            query=args.query,
            output_dir=args.output_dir,
            headless=not args.no_headless
        )
        
        if args.json:
            # Output raw JSON
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Format output nicely
            print("=" * 60)
            print(f"Query: {result['query']}")
            print("=" * 60)
            
            if result.get('ai_answer'):
                print(f"\n🤖 AI Overview:")
                print("-" * 40)
                print(result['ai_answer'])
                
                if result.get('referenced_urls'):
                    print(f"\n📚 Referenced Sources ({len(result['referenced_urls'])}):")
                    print("-" * 40)
                    for i, url in enumerate(result['referenced_urls'], 1):
                        print(f"{i}. {url}")
                else:
                    print("\n📚 No referenced sources found.")
            else:
                if result.get('error'):
                    print(f"\n❌ Error: {result['error']}")
                else:
                    print("\n❌ No AI overview found for this query.")
                    print("This could be because:")
                    print("  - AI Overview feature is not available in your region")
                    print("  - The query didn't trigger an AI response")
                    print("  - Google's page structure has changed")
            
            print(f"\n🔗 Source URL: {result['source_url']}")
            
            # Show save location
            from google_ai_scraper.scraper import GoogleAIOverviewScraper
            scraper = GoogleAIOverviewScraper(output_dir=args.output_dir)
            filename = scraper._sanitize_filename(args.query) + ".json"
            filepath = Path(args.output_dir) / filename
            print(f"💾 Saved to: {filepath}")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraping interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()