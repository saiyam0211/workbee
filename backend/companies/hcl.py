
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
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service 
from datetime import datetime

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
#take the url of website
url = "https://www.hcltech.com/careers/Careers-in-india#job-openings"
#this code gets the info from the url given
driver.get(url)
#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)
time.sleep(3)
while True:
    try:
        elem = driver.find_element(By.XPATH,"//a[@title='Load more items']")
        driver.execute_script("arguments[0].click()",elem)
        time.sleep(3)
    except:
        break
soup = BeautifulSoup(driver.page_source,"html.parser")
jobs = soup.find_all("tr")
L=[]
count = 0
for i in jobs:
    if count!=0:
    count+=1
        soup2 = BeautifulSoup(str(i),"html.parser")
        # print(soup2)
        try:
            title = soup2.find("td",class_='views-field views-field-field-designation').text.replace("  "," ")
            link = "https://www.hcltech.com"+soup2.find("a")["href"]
            # link=''
            location = soup2.find("td",class_='views-field views-field-field-kenexa-jobs-location').text.replace(" ","")
            job_description = extract_job_description(link, firefox_options)
L.append({"job_title":title,"job_location":location,"job_link":link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        except:
            pass
    else:
    count+=1
# print(len(L))
# print(L)
print(json.dumps({"company":"hcl","data":L}))
driver.quit()
