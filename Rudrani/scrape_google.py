import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class GoogleSearchExtractor:
    
    def __init__(self, search_query: str, result_limit: int = 10, scroll_count: int = 3):
        self.driver = webdriver.Chrome()  # Ensure chromedriver is in PATH or specify the full path
        self.query = search_query
        self.result_limit = result_limit
        self.scroll_count = scroll_count
        self.links = []
        self.headings = []
        self.snippets = []
        
        # Open Google Search with the query
        self.driver.get(f'https://www.google.com/search?q={self.query}')
        print('[INFO]: Successfully connected to Google.')
        
        # Scroll to load more results
        for _ in range(self.scroll_count):
            self._load_more_results()
        
        # Collect the search results
        self._collect_results()
    
    def _load_more_results(self):
        """Simulate pressing the END key to scroll down and load more results."""
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)
        time.sleep(10)  # Wait for more results to load
    
    def _collect_results(self):
        """Gather the titles, descriptions, and URLs from the search results."""
        try:
            result_section = self.driver.find_element(By.ID, 'search')
            search_items = result_section.find_elements(By.CLASS_NAME, 'g')

            for item in search_items:
                if len(self.headings) >= self.result_limit:
                    break  # Stop if the required number of results are collected

                try:
                    title_element = item.find_element(By.CSS_SELECTOR, "h3")
                    description_element = item.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                    link_element = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')

                    # Append the extracted data
                    self.headings.append(title_element.text)
                    self.snippets.append(description_element.text)
                    self.links.append(link_element)

                except Exception as e:
                    pass  # Ignore any errors in extracting specific elements

            print('[INFO]: Search result extraction complete.')
        
        except Exception as e:
            print(f'[ERROR]: Failed to gather results. {e}')
    
    def save_to_csv(self, file_name: str):
        """Store the gathered data into a CSV file."""
        result_data = {
            'Title': self.headings,
            'Snippet': self.snippets,
            'URL': self.links
        }
        data_frame = pd.DataFrame(result_data)
        data_frame.to_csv(file_name, index=False)
        print('[INFO]: CSV file has been saved.')
    
    def terminate(self):
        """Close the WebDriver session."""
        self.driver.quit()
        print('[INFO]: WebDriver session closed.')
        

if __name__ == "__main__":
    # Take query as input from the user
    query = input("Enter the search query: ").strip()
    
    if not query:
        print("[ERROR]: Query cannot be empty.")
    else:
        scraper = GoogleSearchExtractor(search_query=query, result_limit=10, scroll_count=3)
        
        # Save the extracted data to a CSV file
        scraper.save_to_csv('search_results.csv')
        
        # End the session
        scraper.terminate()
