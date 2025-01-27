from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def stealthy_google_search(query):
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Bypass automation detection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })

        driver.get("https://www.google.com")
        
        # Handle cookie consent
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='L2AGLb']"))
            )
            cookie_button.click()
        except:
            pass

        # Perform search
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Type query slowly
        for char in query:
            search_box.send_keys(char)
            time.sleep(0.1)
            
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        # Extract results
        results = []
        for g in driver.find_elements(By.CSS_SELECTOR, "div.g"):
            try:
                title = g.find_element(By.TAG_NAME, "h3").text
                link = g.find_element(By.TAG_NAME, "a").get_attribute("href")
                if title and link:
                    results.append({"title": title, "url": link})
            except:
                continue
        
        return results
        
    finally:
        driver.quit()

if __name__ == "__main__":
    search_query = "Agney Nalapat"
    results = stealthy_google_search(search_query)
    
    for idx, result in enumerate(results, 1):
        print(f"{idx}. {result['title']}")
        print(f"   {result['url']}\n")