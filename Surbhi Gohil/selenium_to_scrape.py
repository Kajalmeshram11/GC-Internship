from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the Selenium WebDriver 
driver = webdriver.Chrome()  # or webdriver.Firefox() for Firefox

# Function to scrape Google search results
def google_search(query):
    driver.get("https://www.google.com")
    search_box = driver.find_element("name", "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for results to load

    # Get search results
    results = driver.find_elements("css selector", "h3")
    for result in results:
        print(result.text)

if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    google_search(search_query)
    driver.quit()