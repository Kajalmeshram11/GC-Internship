from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv

chrome_driver_path = r"C:\Users\T.YAMINI\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.google.com")
time.sleep(3)

input("Please solve the CAPTCHA manually if prompted, and then press Enter here to continue...")

search_queries = [
    "Cloud Computing",
    "Cloud Security",
    "Cloud Engineering",
    "AWS Cloud Services",
    "Azure Cloud Architecture",
    "Google Cloud Platform",
    "Cloud Migration Strategies",
    "Cloud Infrastructure Management",
    "Cloud DevOps",
    "Engineering Cloud Solutions",
    "Software Engineering in Cloud",
    "Engineering Cloud Security"
]

data = []

for query in search_queries:
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)

    results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']")
    for result in results:
        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
        data.append([query, link])

with open('google_search_results_cloud_engineering.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Search Query", "Link"])
    writer.writerows(data)

driver.quit()

print("Google search queries and links saved to google_search_results_cloud_engineering.csv")
