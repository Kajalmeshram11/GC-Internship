"""Test suite for Google Scraper."""

import pytest
from google_scraper import GoogleScraper


def test_scraper_initialization():
    """Test that the scraper initializes correctly."""
    scraper = GoogleScraper(headless=True)
    assert isinstance(scraper, GoogleScraper)


def test_search_results_format():
    """Test that search results are in the correct format."""
    scraper = GoogleScraper(headless=True)
    results = scraper.search("test query", num_results=1)
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    result = results[0]
    assert isinstance(result, dict)
    assert "title" in result
    assert "url" in result
    assert "description" in result
    
    assert isinstance(result["title"], str)
    assert isinstance(result["url"], str)
    assert isinstance(result["description"], str)