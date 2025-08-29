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
req = requests.get("https://jobs.lever.co/Polygon/")
soup = BeautifulSoup(req.content, "html.parser")
res1 = soup.find_all("div", class_='posting')
# print(res1)
# print(len(res1))
final_divs=[]
for i in res1:
    soup1 = BeautifulSoup(str(i), "html.parser")
    res2 = soup1.find('span',class_='sort-by-team posting-category small-category-label department').text
    # print(res2)
    if "Tech" in str(res2):
        # print(res2)
        final_divs.append(i)


        
       
data = []
for i in final_divs:
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_link= soup2.find('a')["href"]
    job_title= soup2.find(attrs={"data-qa":"posting-name"}).text
    job_location= soup2.find(attrs={"class":"sort-by-location posting-category small-category-label location"}).text
    job_commitment = soup2.find(class_="sort-by-commitment posting-category small-category-label commitment").text
    work_place_type = soup2.find(attrs={"class":"display-inline-block small-category-label workplaceTypes"}).text
    job_department = soup2.find(attrs={"class":"sort-by-team posting-category small-category-label department"}).text.replace("\u2013","-")
    job_description = extract_job_description(str(job_link), firefox_options)
data.append({"job_title":str(job_title),"job_location":str(job_location),"job_link":str(job_link), "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

json_data = json.dumps({"company":"polygon","data":data})
print(json_data)







