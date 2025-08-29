
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
url = "https://careers.arcesium.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=&optionsFacetsDD_dept=Technology"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
L = []
count = 0
try:
    element = driver.find_element(By.XPATH, "//ul[@class='pagination']")
    elements = driver.find_elements(By.TAG_NAME, "a")
    L1=[]
    titles=[]
    for i in elements:
        try:
            title = i.get_attribute("title")
            # soup4 = BeautifulSoup(str(title), "html.parser")
            # title = soup4.find("a")["title"]
            
            if "Page" in title:
                if title not in titles:
                    titles.append(title)
                    if title!="First Page" and title!="Last Page":
                        L1.append(i)
                        # print(title)
        except:
            pass
    elements = L1[1:]
    soup2 = BeautifulSoup(driver.page_source,"html.parser")
    elements1 = soup2.find_all("tr", class_ = "data-row")
    for j in elements1:
        soup3 = BeautifulSoup(str(j),"html.parser")
        job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
        job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
        job_link = "https://careers.arcesium.com/"+ soup3.find("a", class_="jobTitle-link")["href"]
        job_description = extract_job_description(job_link, firefox_options)
        if {"job_title":job_title,"job_location":job_location,"job_link":job_link} not in L:
            L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        
    for i in range(len(elements)):
        if True:
            k = elements[i]
            driver.execute_script("arguments[0].click();", k)
            time.sleep(3)
            soup2 = BeautifulSoup(driver.page_source,"html.parser")
            elements1 = soup2.find_all("tr", class_ = "data-row")
            for j in elements1:
                soup3 = BeautifulSoup(str(j),"html.parser")
                job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
                job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
                job_link = "https://careers.arcesium.com/"+ soup3.find("a", class_="jobTitle-link")["href"]
                job_description = extract_job_description(job_link, firefox_options)
                if {"job_title":job_title,"job_location":job_location,"job_link":job_link} not in L:
                    L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            

except: 
    soup2 = BeautifulSoup(driver.page_source,"html.parser")
    elements = soup2.find_all("tr", class_ = "data-row")
    for i in elements:
        soup3 = BeautifulSoup(str(i),"html.parser")
        job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
        job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
        job_link = "https://careers.arcesium.com/"+ soup3.find("a", class_="jobTitle-link")["href"]
        job_description = extract_job_description(job_link, firefox_options)

        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        
# Remove this section as job_posted_at is now added in the append statements
json_data = json.dumps({"company":"arcesium","data":L})
print(json_data)
driver.quit()
