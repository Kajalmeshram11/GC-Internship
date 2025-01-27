"""Google Search Scraper.

Usage:
    google-scraper [--query=<query> --num-results=<num>] [--headless]
    google-scraper (-h | --help)

Options:
    -h --help               Show this help message
    --query=<query>         Search query [default: python programming]
    --num-results=<num>     Number of results to fetch [default: 10]
    --headless             Run browser in headless mode
"""

from typing import Dict, Any
from docopt import docopt
from google_scraper.scraper import GoogleScraper


def main() -> None:
    """Execute the main program."""
    arguments = docopt(__doc__)
    
    query: str = arguments.get("--query", "python programming")
    num_results: int = int(arguments.get("--num-results", 10))
    headless: bool = arguments.get("--headless", False)
    
    scraper = GoogleScraper(headless=headless)
    results = scraper.search(query, num_results)
    
    for idx, result in enumerate(results, 1):
        print(f"\n{idx}. {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Description: {result['description']}")