import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

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

url = "https://jobs.lever.co/kpmgnz?department=Corporate%20Services&team=IT"

req = requests.get(url)

soup = BeautifulSoup(req.content,"html.parser")
j = str(soup.find_all("h5"))
a = str(soup.find_all("a"))
s = str(soup.find_all("span"))
# # p = str(soup.find_all("p"))
# # l = str(soup.find_all("li"))
job_obj = BeautifulSoup(j,"html.parser")
link_obj = BeautifulSoup(a,"html.parser")
loc_obj = BeautifulSoup(s,"html.parser")
# # loc = BeautifulSoup(p,"html.parser")
# # lst = BeautifulSoup(l,"html.parser")
jobs = job_obj.find_all(attrs={"data-qa":"posting-name"})
links = link_obj.find_all(class_="posting-title")
locations = loc_obj.find_all(class_="sort-by-location posting-category small-category-label location")


data=[]
for i in range(len(jobs)):
    job_data = {
        "job_title":jobs[i].text,
        "job_link":links[i]["href"],
        "job_location":links[i].text,
        "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    }
    data.append(job_data)
json_data = json.dumps({"company":"kpmg","data":data})
print(json_data)
# driver.quit()