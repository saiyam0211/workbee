"""
Base scraper class for all company job scrapers
"""
import json
import logging
import time
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JobData:
    title: str
    location: str
    experience_required: str
    job_description: str
    job_link: str
    posted_date: str
    company: str
    scraped_at: str = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now().isoformat()

class BaseJobScraper:
    """Base class for all job scrapers"""
    
    def __init__(self, company_name: str, base_url: str, headless: bool = True):
        self.company_name = company_name
        self.base_url = base_url
        self.headless = headless
        self.jobs_data: List[JobData] = []
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        try:
            # Try to get the correct chromedriver path
            driver_path = ChromeDriverManager().install()
            logger.info(f"ChromeDriver path: {driver_path}")
            
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info(f"✅ Browser setup successful for {self.company_name}")
        except Exception as e:
            logger.error(f"❌ Failed to setup ChromeDriver: {str(e)}")
            # Fallback: try without service
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info(f"✅ Browser setup successful (fallback) for {self.company_name}")
            except Exception as e2:
                logger.error(f"❌ Fallback also failed: {str(e2)}")
                raise
    
    def close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def navigate_to_page(self, url: str, wait_time: int = 8):
        """Navigate to a page and wait for it to load"""
        logger.info(f"📍 Navigating to: {url}")
        self.driver.get(url)
        time.sleep(wait_time)
        logger.info("✅ Page loaded successfully")
    
    def extract_job_data(self, element, index: int) -> JobData:
        """Extract job data from an element"""
        try:
            text_content = element.text.strip()
            
            # Extract job title (usually the first line)
            lines = text_content.split('\n')
            title = lines[0].strip() if lines else f"Job {index+1}"
            
            # Extract location
            location = "India"
            for line in lines:
                if any(city in line for city in ["Bangalore", "Gurugram", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai", "Kolkata"]):
                    location = line.strip()
                    break
            
            # Try to get job link
            job_link = ""
            try:
                link_element = element.find_element(By.TAG_NAME, "a")
                job_link = link_element.get_attribute("href")
            except NoSuchElementException:
                pass
            
            return JobData(
                title=title,
                location=location,
                experience_required="Not specified",
                job_description="Job description available on company website",
                job_link=job_link,
                posted_date="Not specified",
                company=self.company_name
            )
            
        except Exception as e:
            logger.warning(f"Error extracting job data: {str(e)}")
            return None
    
    def save_to_json(self, filename: str = None):
        """Save scraped data to JSON file"""
        if not filename:
            filename = f"{self.company_name.lower()}_jobs.json"
            
        data = [asdict(job) for job in self.jobs_data]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved {len(self.jobs_data)} jobs to {filename}")
    
    def scrape_jobs(self, max_pages: int = 1) -> List[JobData]:
        """Main scraping method - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement scrape_jobs method")
    
    def find_next_page_button(self) -> bool:
        """Find and click next page button - to be implemented by subclasses"""
        return False
    
    def wait_for_page_load(self, timeout: int = 5):
        """Wait for page to load after navigation"""
        time.sleep(timeout)