from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def google_search(query):
   
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")  

    try:
        search_box = driver.find_element("name", "q")  
        search_box.send_keys(query)  
        search_box.send_keys(Keys.RETURN)  

        
        input("Browser is open. Press Enter to close...")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()  

if __name__ == "__main__":
    query = input("Enter search : ")
    google_search(query)