from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (Ensure you have ChromeDriver installed)
driver = webdriver.Chrome()

try:
    # Step 1: Open Google
    driver.get("https://www.google.com")
    print("Opened Google...")

    # Step 2: Find the search bar
    search_bar = driver.find_element("name", "q")

    # Step 3: Enter a search query
    search_query = "Selenium Python tutorial"
    search_bar.send_keys(search_query)
    search_bar.send_keys(Keys.RETURN)

    # Step 4: Wait for the results to load
    time.sleep(3)

    # Step 5: Scrape the top 10 search result titles
    results = driver.find_elements("xpath", "//h3")[:10]  # Top 10 results
    print(f"\nTop 10 Google Search Results for '{search_query}':\n")
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result.text}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
