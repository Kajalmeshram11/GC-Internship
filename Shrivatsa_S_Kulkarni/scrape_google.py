from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

# Ask the user for a search query
search_query = input("What would you like to search for? ")

# Set up Chrome options with a custom user-agent to avoid reCAPTCHA detection
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the WebDriver with the configured options
driver = webdriver.Chrome(options=options)  # Ensure chromedriver is installed and in PATH

# Prepare the new data to prepend
new_data = []

# Open the CSV file to read its existing contents
if os.path.exists('search_results.csv'):
    with open('search_results.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        existing_data = list(reader)
else:
    existing_data = []

# Prepare header row and new data
header = ['Rank', 'Title', 'Link']
new_data.append(header)

try:
    # Open Google
    driver.get("https://www.google.com")
    time.sleep(3)  # Adding delay to simulate human behavior

    # Maximize the browser window (full screen)
    driver.maximize_window()

    # Find the search box and enter the user's query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(40)  # Wait for results to load

    # Scrape the results
    results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
    for idx, result in enumerate(results[:10], 1):  # Limit to top 10 results
        title = result.find_element(By.CSS_SELECTOR, "h3").text
        link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        print(f"{idx}. {title} - {link}")
        
        # Add the new data to the list
        new_data.append([idx, title, link])

finally:
    # Close the browser
    driver.quit()

# Write the combined data (new data above the old data) into the CSV file
with open('search_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(new_data)

print("Results have been added above the previous ones in 'search_results.csv'.")
