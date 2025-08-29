
def extract_job_description(job_link, driver_options=None):
    """Extract job description from individual job page"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        
        # Create a new driver instance for description extraction
        if driver_options is None:
            from selenium.webdriver.chrome.options import Options
            driver_options = Options()
            driver_options.add_argument("--headless")
            driver_options.add_argument("--no-sandbox")
            driver_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        desc_driver = webdriver.Chrome(options=driver_options, service=service)
        desc_driver.get(job_link)
        time.sleep(2)
        
        # Look for job description content
        description_selectors = [
            "div[data-testid='job-description']",
            ".job-description",
            ".description",
            "[class*='description']",
            "[class*='content']",
            "section",
            "article",
            ".job-details",
            "[data-testid='job-details']",
            ".job-content",
            ".job-summary",
            ".job-requirements",
            ".job-responsibilities"
        ]
        
        job_description = "Description not available"
        
        for selector in description_selectors:
            try:
                desc_element = desc_driver.find_element(By.CSS_SELECTOR, selector)
                if desc_element:
                    job_description = desc_element.text.strip()
                    if job_description and len(job_description) > 50:  # Ensure we got meaningful content
                        break
            except:
                continue
        
        desc_driver.quit()
        return job_description
        
    except Exception as e:
        print(f"Error extracting job description from {job_link}: {str(e)}")
        return "Description not available"
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
            "[class*='content']",
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
url = "https://careers.mcafee.com/global/en/search-results"
driver.get(url)
L = []

driver.implicitly_wait(20)
time.sleep(2)

category = ['Engineering', 'Information Technology']


for i in category:

    team = driver.find_element(By.XPATH, "//input[@type='checkbox' and @data-ph-at-text='%s']"%i)
    driver.execute_script('arguments[0].scrollIntoView();', team)
    driver.execute_script('arguments[0].click();', team)
    time.sleep(2)
    
num_str = driver.find_element(By.XPATH, "//span[@class='result-count']").get_attribute('innerHTML')
int_num=int(num_str)
# print(int_num)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    # print(total)
    # print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("div", class_= 'job-title').text.strip()   
        job_link = soup2.find("a")["href"]
        job_location = soup2.find('span', class_= 'au-target externalLocation').text.strip()             
        # job_category = soup2.find('span', class_= 'job-category').text[9:].strip()                    
        # job_created = soup2.find('span', class_='job-postdate').text[12:].strip()
        
        job_description = get_job_description_with_driver(driver, job_link)
        L.append({"job_title":job_title, "job_link": job_link, "job_location": job_location, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        # print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        driver.quit()
        break

    if len(L)>=int_num:
        # print('done')
        driver.quit()
        break

# print(len(L))

json_data=json.dumps({'company':'mcafee','data':L})
print(json_data)
driver.quit()
