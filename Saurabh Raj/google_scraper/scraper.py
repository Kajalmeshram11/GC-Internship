"""Google search scraper implementation."""

from typing import List, Dict, Any
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class GoogleScraper:
    """A class to scrape Google search results using Selenium."""

    def __init__(self, headless: bool = False) -> None:
        """Initialize the GoogleScraper.

        Args:
            headless: Whether to run the browser in headless mode
        """
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        
        # Add additional options to avoid detection
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)  # Increased timeout to 20 seconds

    def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """Perform a Google search and extract results.

        Args:
            query: The search query string
            num_results: Number of results to return

        Returns:
            A list of dictionaries containing search results

        Raises:
            TimeoutException: If the page takes too long to load
            WebDriverException: If there's an issue with the browser
        """
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.driver.get("https://www.google.com")
                time.sleep(2)  # Small delay to let the page load
                
                # Find and fill the search box
                search_box = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )
                search_box.clear()
                search_box.send_keys(query)
                time.sleep(1)  # Small delay before hitting enter
                search_box.send_keys(Keys.RETURN)
                
                # Wait for results to load
                self.wait.until(
                    EC.presence_of_element_located((By.ID, "search"))
                )
                time.sleep(2)  # Give time for results to fully load
                
                results = []
                while len(results) < num_results:
                    # Extract results from current page
                    elements = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
                    
                    for element in elements:
                        if len(results) >= num_results:
                            break
                            
                        try:
                            title_elem = element.find_element(By.CSS_SELECTOR, "h3")
                            url_elem = element.find_element(By.CSS_SELECTOR, "a")
                            desc_elem = element.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                            
                            results.append({
                                "title": title_elem.text,
                                "url": url_elem.get_attribute("href"),
                                "description": desc_elem.text
                            })
                        except Exception:
                            continue
                            
                    if len(results) < num_results:
                        try:
                            next_button = self.driver.find_element(
                                By.ID, "pnnext"
                            )
                            next_button.click()
                            time.sleep(2)  # Wait for next page to load
                            self.wait.until(
                                EC.presence_of_element_located((By.ID, "search"))
                            )
                        except Exception:
                            break
                
                return results[:num_results]
                
            except (TimeoutException, WebDriverException) as e:
                retry_count += 1
                print(f"Attempt {retry_count} failed. Retrying...")
                time.sleep(5)  # Wait before retrying
                
                if retry_count == max_retries:
                    print("Error: Maximum retries reached. Please try again later.")
                    raise e
                
                # Restart the browser for the next attempt
                self.driver.quit()
                self.driver = webdriver.Chrome(service=self.service, options=self.options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def __del__(self) -> None:
        """Clean up by closing the browser."""
        if hasattr(self, "driver"):
            self.driver.quit()