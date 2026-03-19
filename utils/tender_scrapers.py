import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.tender_model import Tender
from sqlalchemy.orm import Session

is_scraping = False

def scrape_gem_all(db: Session):
    global is_scraping
    if is_scraping: return
    
    is_scraping = True
    options = Options()
    # options.add_argument("--headless") # Keep off to watch the fix
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    page_number = 1
    try:
        print("🚀 [FORCE SCAN] Navigating to GeM...")
        driver.get("https://bidplus.gem.gov.in/all-bids")
        
        while True:
            # 1. Wait for the page to stop spinning
            time.sleep(1) 
            
            # 2. BRUTE FORCE: Find all links that contain 'GEM/'
            # This is the most reliable way because GeM bid numbers are always links
            bid_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'GEM/')]")
            
            print(f"🔎 Page {page_number}: Detected {len(bid_links)} potential bids.")

            if len(bid_links) == 0:
                print("⚠️ No links found. Checking for 'bid_info' fallback...")
                bid_links = driver.find_elements(By.CLASS_NAME, "bid_info")

            for link in bid_links:
                try:
                    bid_no = link.text.strip()
                    if not bid_no: continue
                    
                    # Prevent duplicates
                    exists = db.query(Tender).filter(Tender.tender_number == bid_no).first()
                    if not exists:
                        # Try to find the parent container to get the description
                        # Usually, the description is in a parent div of the link
                        try:
                            parent_text = link.find_element(By.XPATH, "./../../..").text.split('\n')
                            dept = parent_text[1][:250] if len(parent_text) > 1 else "GeM Dept"
                            title = parent_text[0][:250] if len(parent_text) > 0 else "Goods/Services"
                        except:
                            dept, title = "GeM Department", "Product/Service"

                        new_t = Tender(
                            source="GeM",
                            tender_number=bid_no,
                            department=dept,
                            tender_name=title,
                            link=link.get_attribute("href"),
                            category="General",
                            estimate_cost="Refer Doc",
                            emd_amount="Check Portal",
                            publish_date="16-03-2026",
                            last_date="Open"
                        )
                        db.add(new_t)
                        print(f"✔️ SAVED TO MYSQL: {bid_no}")
                except Exception as e:
                    continue
            
            db.commit()

            # 3. PAGINATION: Click the 'Next' arrow specifically
            try:
                # Find the 'Next' link using XPATH for the literal arrow '»' or 'Next'
                next_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')] | //a[contains(text(), '»')]")
                
                # Check if it's the last page
                parent_li = next_btn.find_element(By.XPATH, "..")
                if "disabled" in parent_li.get_attribute("class"):
                    print("🏁 Reached the last page.")
                    break
                
                driver.execute_script("arguments[0].click();", next_btn)
                page_number += 1
                time.sleep(1) 
            except:
                print("🏁 End of list or button blocked.")
                break

    except Exception as e:
        print(f"🔴 Scraper Error: {e}")
    finally:
        driver.quit()
        is_scraping = False