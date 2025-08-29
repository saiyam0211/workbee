#import webdriver
import os
from selenium import webdriver
# import chromedriver_binary  # Removed due to installation issues
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service 
#from webdriver_manager.firefox import GeckoDriverManager
#geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
service = Service(ChromeDriverManager().install())
firefox_options = Options()
#firefox_options.binary_location = os.environ["PATHCHROME"]
#firefox_options.binary_location = './firefox/firefox'
import os
#os.chmod('./firefox/firefox', 0o755)
# firefox_options.binary_location = geckodriver_path
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=firefox_options,service=service)
driver.maximize_window()
from datetime import datetime

# helper to fetch job description using the same driver (opens a new tab)
def get_job_description_with_driver(driver, job_link: str) -> str:
    try:
        original_window = driver.current_window_handle
        driver.execute_script("window.open('about:blank','_blank');")
        time.sleep(0.5)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        driver.get(job_link)
        time.sleep(2)
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, "html.parser")
        selectors = [
            "div[data-testid='job-description']",
            ".job-description",
            "#job-description",
            "[class*='description']",
            "section",
            "article",
        ]
        description_text = "Description not available"
        for sel in selectors:
            tag = soup.select_one(sel)
            if tag:
                text = tag.get_text(" ", strip=True)
                if text and len(text) > 50:
                    description_text = text
                    break
        driver.close()
        driver.switch_to.window(original_window)
        return description_text
    except Exception:
        try:
            driver.switch_to.window(original_window)
        except Exception:
            pass
        return "Description not available"
# Navigate to the website
driver.get("https://careers.viasat.com/jobs?limit=100&page=1")

# Wait for the job list to load

job_data = []

while True:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-results-container")))

    # Get all the job elements
    job_elements = driver.find_elements(By.TAG_NAME, "mat-expansion-panel")

    # Iterate over the job elements and extract the job information
    for job_element in job_elements:
        # Extract job title
        title_element = job_element.find_element(By.CSS_SELECTOR, '.job-title')
        job_title = title_element.text.strip()

        # # Extract job location
        location_element = job_element.find_element(By.CSS_SELECTOR, ".label-container > span:nth-of-type(2)")
        job_location = location_element.text.strip()

        # Extract job link if available (fallback to careers page)
        link_elem = None
        try:
            link_elem = job_element.find_element(By.CSS_SELECTOR, 'a[href]')
        except Exception:
            link_elem = None
        job_link = link_elem.get_attribute('href') if link_elem else 'https://careers.viasat.com/'
        # Fetch description by visiting job page when link exists
        job_description = get_job_description_with_driver(driver, job_link) if job_link else "Description not available"

        job_details = {
            'job_title': job_title,
            'job_location': job_location,
            "job_link": job_link,
            "job_description": job_description,
            "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


        # Append the job details to the job data list
        job_data.append(job_details)

    next_button = driver.find_element(By.CSS_SELECTOR, ".mat-paginator-range-actions > button:nth-of-type(2)")
    if "mat-button-disabled" in next_button.get_attribute('class'):
        break  # Exit the loop if there's no next button or if it's disabled

    # Click the next button to load the next page of job listings
    # next_button.click()
    driver.execute_script("arguments[0].click();", next_button)

    # Wait for the new page to load
    # wait.until(EC.staleness_of(job_elements[0]))

    # # Get the job elements of the new page
    # job_elements = driver.find_elements(By.CSS_SELECTOR, ".search-result job-listing   ")

# with open('Walmart.json', 'w') as file:
#     json.dump(job_data, file, indent=4)
print(json.dumps({"company":"viasat","data":job_data}))

# Close the browser
driver.quit()
