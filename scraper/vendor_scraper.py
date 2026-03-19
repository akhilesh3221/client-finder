from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import logging
import time

# THIS IS THE FUNCTION NAME THE ROUTE WILL LOOK FOR
def scrape_b2b_vendors(product: str) -> list:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new") # Keep disabled so you can see if the browser crashes
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(options=options)
    vendors = []
    
    try:
        encoded_product = urllib.parse.quote_plus(product)
        # Using a generic search URL as a placeholder
        url = f"https://mkp.gem.gov.in/search?q={encoded_product}"
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "seller-name")))

        for item in items[:5]: # Just pulling 5 for a quick test
            vendors.append({
                "company": item.text.strip(),
                "product": product,
                "city": "Raipur", # Default fallback
                "phone": "Requires Google API", 
                "email": "Hidden"
            })
                
    except Exception as e:
        logging.error(f"Scrape Error: {e}")
    finally:
        driver.quit()

    return vendors