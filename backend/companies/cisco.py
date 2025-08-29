
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
url ="https://jobs.cisco.com/jobs/SearchJobs/?21181=%5B186%2C194%2C187%2C191%2C202%2C185%2C55816092%5D&21181_format=6023&listFilterMode=1"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i< elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""
driver.find_element(By.XPATH,"//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']").click()
time.sleep(2)
L = []
def function1():
    L1 = driver.execute_script(script)
    hrefs= []
    for i in L1:
        if "/ProjectDetail/" in i:
            hrefs.append(i)
    count = 0
    element = driver.find_element(By.TAG_NAME,"tbody")
    soup = BeautifulSoup(str(element.get_attribute("outerHTML")), "html.parser")
    job_elements = soup.find_all("tr")
    for i in job_elements:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("td",attrs={"data-th":"Job Title"}).text
        job_link =  hrefs[count]
        job_location = soup2.find("td",attrs={"data-th":"Location"}).text
        if {"job_title":job_title,"job_location":job_location,"job_link": job_link, "job_description": job_description} not in L:
        job_description = extract_job_description(job_link, firefox_options)
L.append({"job_title":job_title,"job_location":job_location,"job_link": job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
count+=1
while True:
    driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
    try:
        element1 = driver.find_elements(By.XPATH, "//a[@class='pagination_item']")
        time.sleep(2)
        function1()
        next =[]
        for i in element1:
            var1 = i.text
            if ">>" in var1:
                next.append(i)
        if len(next) == 0:
            break
        else:
            driver.execute_script("arguments[0].click()", next[0])
            time.sleep(3)
    except:
        pass

json_data = json.dumps({"company":"cisco","data":L})
print(json_data)

driver.quit()