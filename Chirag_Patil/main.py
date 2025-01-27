import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random

 
def scrape_google_results(query, max_results=100):
    # Configure Chrome WebDriver options
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--start-maximized")
    
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    
   
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    time.sleep(random.uniform(1, 2))  # Add delay to mimic human behavior
    search_box.send_keys(Keys.RETURN)
    time.sleep(random.uniform(2, 4))  # Wait for results to load
    
    results = []
    # Locate search result elements
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
    
     
    for result in search_results[:max_results]:
        try:
            title_elem = result.find_element(By.CSS_SELECTOR, "h3")
            link_elem = result.find_element(By.CSS_SELECTOR, "a")
            
            title = title_elem.text
            link = link_elem.get_attribute("href")
            
            if title and link:
                results.append({"title": title, "link": link})
        except Exception:
            pass  # Skip any errors in extracting data
    
    driver.quit()   
    return results

 
def save_to_csv(results, filename="google_results.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "link"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to '{filename}'")


 

if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    scraped_results = scrape_google_results(search_query)

    if scraped_results:
        save_to_csv(scraped_results)
    else:
        print("No results found.")