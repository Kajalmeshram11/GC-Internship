from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the Chrome driver
driver = webdriver.Chrome(executable_path='C:/WebDrivers/chromedriver.exe')

# Open Google
driver.get("https://www.google.com")

# Find the search box
search_box = driver.find_element_by_name("q")

# Enter search term
search_box.send_keys("Selenium Python")

# Submit the search
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(2)

# Extract search results
results = driver.find_elements_by_css_selector('h3')

for result in results:
    print(result.text)

# Close the browser
driver.quit()