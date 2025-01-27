# Google Search Scraper

A Python tool to scrape Google search results using Selenium.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Basic usage
google-scraper --query="your search query" --num-results=10

# Run in headless mode
google-scraper --query="your search query" --headless
```

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements_test.txt
```

3. Run tests:
```bash
pytest tests/
```

4. Run linter:
```bash
flake8
```