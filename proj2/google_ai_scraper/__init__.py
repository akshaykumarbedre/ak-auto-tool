"""
Google AI Overview Scraper Package

Real-time scraping of Google's AI Overview feature for LLM tooling.
"""

from .scraper import get_google_ai_overview, GoogleAIOverviewScraper

__version__ = "1.0.0"
__all__ = ["get_google_ai_overview", "GoogleAIOverviewScraper"]