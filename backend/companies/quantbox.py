from bs4 import BeautifulSoup
import requests
import time
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


html_text = requests.get('https://www.quantboxresearch.com/jobs').text
final_data = list()
soup = BeautifulSoup(html_text, 'html.parser')
jobs = soup.find_all('div', class_='job-item')

for index, job in enumerate(jobs):
    job_name = job.find('h3', class_='job-title').text.strip()
    location = job.find('div', class_='job-sub-title').find('small').text.strip()
    job_link = job.h3.a['href']
    job_description = extract_job_description("https://www.quantboxresearch.com"+job_link.strip(), firefox_options)
final_    job_description = extract_job_description("https://www.quantboxresearch.com"+job_link.strip(), firefox_options)
data.append({
        "job_title": job_name.strip(),
        "job_location": location.strip(),
        "job_link": "https://www.quantboxresearch.com"+job_link.strip(),
        "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    , "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

json_data = json.dumps({"company": "quantbox", "data": final_data})
print(json_data)
