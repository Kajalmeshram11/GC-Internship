from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_google_results(query, num_results=5):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--headless")  # Optional: Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")  # Prevent sandbox issues in some environments

    # Initialize ChromeDriver with options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open Google
        driver.get("https://www.google.com")

        # Find the search bar and input the query
        search_box = driver.find_element("name", "q")  # Search bar is identified by name "q"
        search_box.send_keys(query)  # Enter the query
        search_box.send_keys(Keys.RETURN)  # Press Enter to search

        # Wait for results to load
        time.sleep(2)

        # Scrape search results
        results = driver.find_elements("xpath", "//div[@class='tF2Cxc']")  # Google's search result block

        # Extract titles and links
        scraped_data = []
        for result in results[:num_results]:  # Limit to the desired number of results
            title = result.find_element("xpath", ".//h3").text  # Extract title
            link = result.find_element("xpath", ".//a").get_attribute("href")  # Extract link
            scraped_data.append({"title": title, "link": link})

        # Print the results
        print("\nScraped Google Search Results:")
        for idx, data in enumerate(scraped_data, start=1):
            print(f"{idx}. {data['title']} ({data['link']})")

        return scraped_data

    finally:
        # Close the browser
        driver.quit()

# Usage
if __name__ == "__main__":
    search_query = "Python web scraping"
    scrape_google_results(search_query)
