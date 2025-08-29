from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import json
import time
import logging
from urllib.parse import urljoin
# from app.config.logger import setup_logger  # Removed due to import issues
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

# Configure logging
logger = setup_logger("ti_logger", "logs/companies/texas_instrument.log")
class TICareersScraper:
    def __init__(self, headless=False, timeout=20):
        self.timeout = timeout
        self.data = []
        self.processed_links = set()  # To avoid duplicates
        self.BASE_URL = "https://careers.ti.com"
        
        # Optimized Chrome options
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        
        # Performance optimizations
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Keep JavaScript enabled for dynamic loading
        self.driver = None
        self.wait = None
    
    def init_driver(self):
        """Initialize driver and wait object"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(60)
            self.wait = WebDriverWait(self.driver, self.timeout)
            logger.info("Driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize driver: {str(e)}")
            raise
    
    def close_driver(self):
        """Close the driver safely"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.warning(f"Error closing driver: {str(e)}")
            finally:
                self.driver = None
    
    def wait_for_initial_load(self):
        """Wait for initial page load and job listings"""
        try:
            # Wait for the job list container to be present
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-list__list"))
            )
            
            # Wait for at least one job to be loaded
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-list__list li"))
            )
            
            logger.info("Initial job listings loaded")
            time.sleep(2)  # Additional buffer
            
        except TimeoutException:
            logger.warning("Timeout waiting for initial job listings")
    
    def scroll_and_load_jobs(self):
        """Perform infinite scroll to load all jobs"""
        logger.info("Starting infinite scroll to load all jobs...")
        
        last_job_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 100  # Prevent infinite loops
        no_new_jobs_count = 0
        max_no_new_jobs = 5  # Stop after 5 consecutive scrolls with no new jobs
        
        while scroll_attempts < max_scroll_attempts and no_new_jobs_count < max_no_new_jobs:
            try:
                # Get current job count
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-list__list li")
                current_job_count = len(job_elements)
                
                logger.info(f"Scroll attempt {scroll_attempts + 1}: {current_job_count} jobs loaded")
                
                # Check if new jobs were loaded
                if current_job_count > last_job_count:
                    no_new_jobs_count = 0  # Reset counter
                    last_job_count = current_job_count
                else:
                    no_new_jobs_count += 1
                    logger.info(f"No new jobs loaded ({no_new_jobs_count}/{max_no_new_jobs})")
                
                # Scroll down to the last job element
                if job_elements:
                    last_job = job_elements[-1]
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", last_job)
                else:
                    # Fallback: scroll to bottom of page
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for new content to load
                time.sleep(3)
                
                # Try to detect loading indicators
                try:
                    loading_indicators = self.driver.find_elements(By.CSS_SELECTOR, 
                        ".loading, .spinner, [data-loading='true'], .jobs-loading")
                    if loading_indicators:
                        logger.info("Loading indicator detected, waiting longer...")
                        time.sleep(5)
                except:
                    pass
                
                scroll_attempts += 1
                
            except Exception as e:
                logger.warning(f"Error during scroll attempt {scroll_attempts + 1}: {str(e)}")
                scroll_attempts += 1
                time.sleep(2)
        
        # Final job count
        final_job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-list__list li")
        logger.info(f"Infinite scroll completed. Total jobs loaded: {len(final_job_elements)}")
        
        return len(final_job_elements)
    
    def extract_job_data(self):
        """Extract job data from all loaded job listings"""
        jobs_data = []
        
        try:
            # Get the job list container
            job_list_element = self.driver.find_element(By.CLASS_NAME, "jobs-list__list")
            
            # Parse with BeautifulSoup for better performance
            soup = BeautifulSoup(job_list_element.get_attribute("outerHTML"), "html.parser")
            job_items = soup.find_all("li")
            
            logger.info(f"Processing {len(job_items)} job listings...")
            
            for i, job in enumerate(job_items, 1):
                try:
                    # Extract job link
                    link_element = job.find("a")
                    if not link_element or not link_element.get("href"):
                        logger.debug(f"Job {i}: No link found, skipping")
                        continue
                    
                    link = link_element["href"]
                    # Make absolute URL if needed
                    if link.startswith("/"):
                        link = urljoin(self.BASE_URL, link)
                    elif not link.startswith("http"):
                        link = urljoin(self.BASE_URL, "/" + link)
                    
                    # Check for duplicates
                    if link in self.processed_links:
                        logger.debug(f"Job {i}: Duplicate link found, skipping")
                        continue
                    
                    # Extract job title
                    title_element = job.find(class_="job-tile__title")
                    if not title_element:
                        # Try alternative selectors
                        title_element = job.find(["h2", "h3", "h4"]) or job.find("a")
                    
                    title = title_element.get_text(strip=True) if title_element else f"Job {i}"
                    
                    # Extract location with multiple strategies
                    location = "Location not specified"
                    
                    # Strategy 1: posting-locations span
                    location_container = job.find("posting-locations")
                    if location_container:
                        location_span = location_container.find("span")
                        if location_span:
                            location = location_span.get_text(strip=True)
                    
                    # Strategy 2: Alternative location selectors
                    if location == "Location not specified":
                        location_selectors = [
                            ".job-tile__location",
                            ".location",
                            ".job-location",
                            "[data-location]"
                        ]
                        
                        for selector in location_selectors:
                            loc_elem = job.select_one(selector)
                            if loc_elem:
                                location = loc_elem.get_text(strip=True)
                                break
                    
                    # Clean up location text
                    if location:
                        location = ' '.join(location.split())  # Remove extra whitespace
                    
                    # Validate extracted data
                    if not title or len(title.strip()) < 2:
                        logger.debug(f"Job {i}: Invalid title, skipping")
                        continue
                    
                    self.processed_links.add(link)
                    
                    job_data = {
                        "job_title": title,
                        "job_location": location,
                        "job_link": link,
                        "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    jobs_data.append(job_data)
                    
                    if i % 10 == 0:  # Log progress every 10 jobs
                        logger.info(f"Processed {i}/{len(job_items)} jobs...")
                    
                except Exception as e:
                    logger.warning(f"Error processing job {i}: {str(e)}")
                    continue
            
            logger.info(f"Successfully extracted {len(jobs_data)} valid jobs")
            
        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
        
        return jobs_data
    
    def scrape_all_jobs(self, url):
        """Main scraping function"""
        try:
            logger.info(f"Starting TI careers scraping: {url}")
            self.init_driver()
            
            # Navigate to URL
            self.driver.get(url)
            
            # Wait for initial load
            self.wait_for_initial_load()
            
            # Perform infinite scroll to load all jobs
            total_loaded = self.scroll_and_load_jobs()
            
            # Extract job data
            self.data = self.extract_job_data()
            
            logger.info(f"Scraping completed! Total jobs extracted: {len(self.data)}")
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
        
        finally:
            self.close_driver()
    
    def get_results(self):
        """Get the scraped results"""
        return {
            "company": "texas_instruments",
            "data": self.data
        }
    
    def save_results(self, filename="texas_instrument.json"):
        """Save results to JSON file"""
        try:
            results = self.get_results()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

def main():
    """Main execution function"""
    url = "https://careers.ti.com/en/sites/CX/jobs?lastSelectedFacet=CATEGORIES&location=India&locationId=300000000361484&locationLevel=country&mode=location&selectedCategoriesFacet=300000068853972%3B300000068853892"
    
    scraper = TICareersScraper(headless=True, timeout=20)
    start_time = time.time()
    logger.info("Starting Texas Instruments careers scraping...")
        
    scraper.scrape_all_jobs(url)
        
    end_time = time.time()
    scraping_time = end_time - start_time
        
    results = scraper.get_results()
        
    json_output = json.dumps(results)
    print(json_output)
        
    logger.info(f"Scraping completed in {scraping_time:.2f} seconds")
    logger.info(f"Total jobs scraped: {len(results['data'])}")
    scraper.close_driver()    


if __name__ == "__main__":
    main()