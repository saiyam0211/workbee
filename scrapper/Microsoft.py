from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import json
import requests
from bs4 import BeautifulSoup
import time

firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

url = "https://jobs.careers.microsoft.com/global/en/search?p=Software%20Engineering&p=Data%20Center&p=Research%2C%20Applied%2C%20%26%20Data%20Sciences&p=Hardware%20Engineering&p=Engineering&p=Design%20%26%20Creative&p=Analytics&p=Technical%20Support&d=Art&d=Software%20Engineering&rt=People%20Manager&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true"
driver.get(url)
L = []

driver.implicitly_wait(20)
time.sleep(3)

# Get total job count if available
ns = ""
try:
    count_element = driver.find_element(By.XPATH, "//span[contains(text(), 'jobs') or contains(text(), 'positions')]")
    num_str = count_element.text
    for i in num_str:
        if i in "0123456789":
            ns += i
    int_num = int(ns) if ns else 100  # Default to 100 if can't find count
except:
    int_num = 100  # Default to 100 if can't find count

print(f"Expected job count: {int_num}")

while True:
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ms-List-page")))

        # Get all the job elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".ms-List-cell")
        
        print(f"Found {len(job_elements)} jobs on current page")

        # Iterate over the job elements and extract the job information
        for job_element in job_elements:
            try:
                # Extract job title
                title_element = job_element.find_element(By.CSS_SELECTOR, '.MZGzlrn8gfgSs8TZHhv2')
                job_title = title_element.text.strip()

                # Extract job location - try multiple selectors
                job_location = "N/A"
                location_selectors = [
                    "span[class*='location']",
                    "div[class*='location']",
                    "span[class*='Location']",
                    "div[class*='Location']"
                ]
                
                for selector in location_selectors:
                    try:
                        location_element = job_element.find_element(By.CSS_SELECTOR, selector)
                        job_location = location_element.text.strip()
                        break
                    except:
                        continue

                # Extract job link if available
                job_link = "N/A"
                try:
                    link_element = job_element.find_element(By.CSS_SELECTOR, "a")
                    job_link = link_element.get_attribute("href")
                except:
                    pass

                if job_title and job_title != "N/A":
                    L.append({
                        "job_title": job_title,
                        "job_location": job_location,
                        "job_link": job_link
                    })

            except Exception as e:
                print(f"Error processing job element: {e}")
                continue

        # Check if there's a next button
        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
            if 'disabled' in next_button.get_attribute('class'):
                print("Next button is disabled")
                break
            next_button.click()
            time.sleep(3)
        except:
            try:
                # Try alternative next button selector
                next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Next']")
                if 'disabled' in next_button.get_attribute('class'):
                    print("Next button is disabled")
                    break
                next_button.click()
                time.sleep(3)
            except:
                print("No more pages or next button not found")
                break

        if len(L) >= int_num:
            print(f"Reached target count: {len(L)}")
            break

    except Exception as e:
        print(f"Error processing page: {e}")
        break

json_data = json.dumps({
    "company": "microsoft",
    "data": L
})
print(f"Total jobs scraped: {len(L)}")
print(json_data)
driver.quit()