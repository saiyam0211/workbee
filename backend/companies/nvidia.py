from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import requests
from bs4 import BeautifulSoup
import time

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


firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)
url = "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?jobFamilyGroup=0c40f6bd1d8f10ae43ffbd1459047e84&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78"

driver.get(url)
L=[]
driver.implicitly_wait(20)
time.sleep(3)
ns = ""
while ns=="":
    num_str = driver.find_element(By.XPATH,"//p[@class='css-12psxof']").get_attribute("innerHTML")

    for i in num_str:
        if i not in "0123456789":
            break
        else:
            ns+=i
    try:
        int_num = int(ns)
    except:
        pass
count = 0
while True:
    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    total = soup.find_all("li",class_='css-1q2dra3')
    # print(len(total))
    # print(total)
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        time.sleep(2)
        job_title = soup2.find("h3").text
        job_link = "https://nvidia.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        job_description = extract_job_description(job_link, firefox_options)

        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    total = soup.find_all("li",class_='css-3hlofn')
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://nvidia.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        job_description = extract_job_description(job_link, firefox_options)

        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    time.sleep(3)
    try:
        elem = driver.find_element(By.XPATH,"//button[@class='css-ly8o31' and @aria-label='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
    except:
        driver.quit()
        break
    
    if len(L)>=int_num:
        driver.quit()
        break



json_data = json.dumps({
    "company": "nvidia",
    "data": L
})

print(json_data)
driver.close()




