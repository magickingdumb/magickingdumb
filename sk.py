from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

logging.basicConfig(filename="selenium_scraping.log", level=logging.INFO)

URL = "https://www.zillow.com/homes/new_homes"  # replace with the real URL

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)  # replace with the path to the chromedriver binary if necessary

wait = WebDriverWait(driver, 10)

try:
    driver.get(URL)

    # assuming new homes are listed in divs with class 'new-home'
    new_homes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.new-home')))
    for home in new_homes:
        print(home.text)

    # assuming neighborhoods are listed in divs with class 'neighborhood'
    neighborhoods = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.neighborhood')))
    for neighborhood in neighborhoods:
        print(neighborhood.text)

    logging.info(f"Successfully scraped URL: {URL}")
except Exception as e:
    logging.error(f"Failed to scrape URL: {URL}. Reason: {str(e)}")
finally:
    time.sleep(2)  # respect rate limits
    driver.quit()  # make sure to quit the driver




