from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_google_search_results(query, max_results=10):
    """
    Scrapes Google search results for a given query using Selenium.

    Parameters:
        query (str): Search query to scrape results for.
        max_results (int): Maximum number of results to fetch.

    Returns:
        list: A list of dictionaries containing titles and URLs of search results.
    """
    # Configure Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service('path/to/chromedriver')  # Update with your chromedriver path

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open Google Search
    driver.get("https://www.google.com")

    # Locate the search bar, enter the query, and submit
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(2)

    # Scrape search results
    search_results = []
    results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf")

    for result in results[:max_results]:
        try:
            title_element = result.find_element(By.TAG_NAME, "h3")
            link_element = result.find_element(By.TAG_NAME, "a")
            title = title_element.text
            link = link_element.get_attribute("href")
            search_results.append({"title": title, "link": link})
        except Exception as e:
            print(f"Error extracting a result: {e}")

    # Close the browser
    driver.quit()

    return search_results

if __name__ == "__main__":
    query = input("Enter your search query: ")
    max_results = int(input("Enter the number of results to fetch: "))
    results = scrape_google_search_results(query, max_results)

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result['title']}\n   {result['link']}\n")
