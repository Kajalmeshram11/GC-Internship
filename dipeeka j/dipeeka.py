import os
import sys
import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

def scrape_google_results(query, num_results=10):
    # Suppress unnecessary logs to keep console clean
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # Suppress warning to keep console clean
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

    # Initialize the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Apply stealth to avoid detection
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    # Open Google and perform a search
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for CAPTCHA if prompted
    print("Solve the CAPTCHA if prompted. Waiting for search results to load...")
    while True:
        if len(driver.find_elements(By.CSS_SELECTOR, '.tF2Cxc')) > 0:
            print("CAPTCHA solved, proceeding...")
            break
        time.sleep(5)

    # Random wait time before scraping results
    time.sleep(random.uniform(3, 6))

    results = []
    search_results = driver.find_elements(By.CSS_SELECTOR, '.tF2Cxc')

    for result in search_results[:num_results]:
        try:
            # Extract Title, Link, and Description
            title_element = result.find_element(By.TAG_NAME, "h3")
            link_element = result.find_element(By.CSS_SELECTOR, "a")
            snippet_element = result.find_element(By.CSS_SELECTOR, ".VwiC3b")

            title = title_element.text if title_element else "No Title"
            link = link_element.get_attribute("href") if link_element else "No Link"
            snippet = snippet_element.text if snippet_element else "No Description"

            results.append({
                "Title": title,
                "Link": link,
                "Description": snippet
            })
        except Exception as e:
            print(f"Error extracting result: {e}")
            continue  # Continue even if there is an error with one result

    # Close the browser window
    driver.quit()

    # Restore standard output and error streams
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    return results

# Function to save results to a CSV file
def save_to_csv(data, filename='google_results.csv'):
    # Open CSV file and write the scraped data
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Link", "Description"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    scraped_data = scrape_google_results(search_query)

    if scraped_data:
        save_to_csv(scraped_data)
    else:
        print("No results found.")
