
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
#from webdriver_manager.firefox import GeckoDriverManager
#geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from datetime import datetime

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
url = "https://workday.wd5.myworkdayjobs.com/Workday?jobFamilyGroup=8c5ce7a1cffb43e0a819c249a49fcb00&jobFamilyGroup=a88cba90a00841e0b750341c541b9d56&jobFamilyGroup=4b2f970c50930155b9985193020a0c72"
driver.get(url)
L=[]
driver.implicitly_wait(100)
time.sleep(4)
num_str = driver.find_element(By.XPATH,"//p[@class='css-12psxof']").get_attribute("innerHTML")
ns = ""
for i in num_str:
    if i not in "0123456789":
        break
    else:
        ns+=i
int_num = int(ns)
count = 0
while True:
    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    total = soup.find_all("li",class_='css-1q2dra3')
    # print(len(total))
    # print(total)
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://workday.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        job_description = extract_job_description(job_link, firefox_options)
L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        # print({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description})
    total = soup.find_all("li",class_='css-3hlofn')
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://workday.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        job_description = extract_job_description(job_link, firefox_options)
L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    time.sleep(3)
    try:
        elem = driver.find_element(By.XPATH,"//button[@class='css-ly8o31' and @aria-label='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
    except:
        break

    
json_data = json.dumps({"company":"workday","data":L})
print(json_data)
driver.quit()





