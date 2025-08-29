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
    url = "https://boards.greenhouse.io/embed/job_board?for=brave&amp;b=https%3A%2F%2Fbrave.com%2Fcareers%2F"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    job_positions = []
    job_elements = soup.find_all("section", class_="level-0")
    
    for element in job_elements:
        for x in element.find_all("div", class_="opening"):
            job_category = element.find("h3").text.strip()
            job_location = x.find("span", class_="location").text.strip()
            job_title = x.find("a").text.strip()
            
            job_positions.append({
                "job_title": job_title,
                "job_location": job_location,
                "job_link":'https://brave.com/careers/',
                "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return job_positions

def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Scrape job positions
job_positions = scrape_job_positions()

# Save job positions to JSON file
# save_to_json(job_positions, "BraveData.json")
fin = json.dumps({"company":"brave","data":job_positions})
print(fin)
