import requests
import json
from bs4 import BeautifulSoup
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

def scrape_job_positions():
    url = "https://jobs.dropbox.com/all-jobs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    job_positions = []
    job_elements = soup.find_all("div", class_="open-positions__listing-group open-positions__listing-group--left")
    # print(job_elements)
    
    for element in job_elements:
        for x in element.find_all("li", class_="open-positions__listing"):
            job_category = element.find("a", class_="open-positions__dept-title-link").text.strip()
            job_location = x.find("p", class_="open-positions__listing-location").text.strip()
            job_title = x.find("h5", class_="open-positions__listing-title").text.strip()
            
            job_positions.append({
                "job_title": job_title,
                "job_location": job_location,
                "job_link":'https://jobs.dropbox.com/all-jobs',
                "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return job_positions

# def save_to_json(data, filename):
#     with open(filename, "w") as file:
#         json.dump(data, file, indent=4)

# Scrape job positions
job_positions = scrape_job_positions()

# Save job positions to JSON file
# save_to_json(job_positions, "DropBoxData.json")
print(json.dumps({"company":"dropbox","data":job_positions}))
