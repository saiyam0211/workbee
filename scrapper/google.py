from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import json
import time
import logging
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoogleCareersScraper:
    def __init__(self, headless=True, timeout=15):
        self.timeout = timeout
        self.data = []
        self.UNORDERED_LIST_CLASS_NAME = "spHGqe"
        self.BASE_URL = "https://www.google.com/about/careers/"
        self.processed_links = set()  # To avoid duplicates
        
        # Optimized Chrome options
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        
        # Performance optimizations
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-plugins")
        self.chrome_options.add_argument("--disable-images")
        self.chrome_options.add_argument("--disable-javascript")
        self.chrome_options.add_argument("--disable-css")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Additional performance settings
        self.chrome_options.add_argument("--memory-pressure-off")
        self.chrome_options.add_argument("--max_old_space_size=4096")
        
        self.driver = None
        self.wait = None
    
    def init_driver(self):
        """Initialize driver and wait object"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(30)
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
    
    def safe_find_element(self, by, value, timeout=None):
        """Safely find element with timeout"""
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Element not found within {wait_time}s: {by}={value}")
            return None
        except Exception as e:
            logger.error(f"Error finding element {by}={value}: {str(e)}")
            return None
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(1)  # Additional buffer
        except TimeoutException:
            logger.warning("Page load timeout reached")
    
    def extract_jobs_from_current_page(self):
        """Extract job data from the current page"""
        jobs_data = []
        
        try:
            # Wait for job listings to load
            ul = self.safe_find_element(By.CLASS_NAME, self.UNORDERED_LIST_CLASS_NAME, timeout=20)
            if not ul:
                logger.warning("Job listings container not found")
                return jobs_data
            
            # Parse with BeautifulSoup for better performance
            soup = BeautifulSoup(ul.get_attribute("outerHTML"), "html.parser")
            job_items = soup.find_all("li")
            
            logger.info(f"Found {len(job_items)} job items on current page")
            
            for job in job_items:
                try:
                    # Extract job title
                    title_elem = job.find("h3")
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    
                    # Extract location
                    location_elem = job.select_one(".r0wTof")
                    location = location_elem.get_text(strip=True) if location_elem else "Location not specified"
                    
                    # Extract job link
                    link_elem = job.select_one('a[href*="jobs/results/"]')
                    if not link_elem:
                        continue
                    
                    relative_link = link_elem.get("href")
                    full_link = urljoin(self.BASE_URL, relative_link)
                    
                    # Check for duplicates
                    if full_link in self.processed_links:
                        continue
                    
                    self.processed_links.add(full_link)
                    
                    job_data = {
                        "job_title": title,
                        "job_location": location,
                        "job_link": full_link
                    }
                    
                    jobs_data.append(job_data)
                    
                except Exception as e:
                    logger.warning(f"Error parsing individual job: {str(e)}")
                    continue
            
            logger.info(f"Successfully extracted {len(jobs_data)} new jobs from current page")
            
        except Exception as e:
            logger.error(f"Error extracting jobs from page: {str(e)}")
        
        return jobs_data
    
    def navigate_to_next_page(self):
        """Navigate to the next page"""
        try:
            # Multiple strategies to find the next button
            next_button_selectors = [
                '//a[@aria-label="Go to next page"]',
                '//a[contains(@class, "next")]',
                '//button[@aria-label="Go to next page"]',
                '//a[contains(text(), "Next")]'
            ]
            
            next_button = None
            for selector in next_button_selectors:
                try:
                    next_button = self.driver.find_element(By.XPATH, selector)
                    if next_button.is_displayed() and next_button.is_enabled():
                        break
                except NoSuchElementException:
                    continue
            
            if not next_button:
                logger.info("Next button not found - reached last page")
                return False
            
            # Check if button is actually clickable
            if not next_button.is_displayed() or not next_button.is_enabled():
                logger.info("Next button is not clickable - reached last page")
                return False
            
            # Scroll to button and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            
            try:
                # Try JavaScript click first (more reliable)
                self.driver.execute_script("arguments[0].click();", next_button)
            except Exception:
                # Fallback to regular click
                next_button.click()
            
            # Wait for page to load
            self.wait_for_page_load(timeout=15)
            logger.info("Successfully navigated to next page")
            
            return True
            
        except ElementClickInterceptedException:
            logger.warning("Next button click was intercepted")
            return False
        except Exception as e:
            logger.warning(f"Error navigating to next page: {str(e)}")
            return False
    
    def scrape_all_jobs(self, url):
        """Scrape all job listings from Google Careers"""
        try:
            logger.info(f"Starting to scrape: {url}")
            self.init_driver()
            
            # Navigate to the URL
            self.driver.get(url)
            self.wait_for_page_load()
            
            page_count = 1
            total_jobs = 0
            
            while True:
                logger.info(f"Scraping page {page_count}")
                
                # Extract jobs from current page
                page_jobs = self.extract_jobs_from_current_page()
                self.data.extend(page_jobs)
                total_jobs += len(page_jobs)
                
                logger.info(f"Page {page_count}: {len(page_jobs)} jobs extracted (Total: {total_jobs})")
                
                # Try to navigate to next page
                if not self.navigate_to_next_page():
                    logger.info("No more pages to scrape")
                    break
                
                page_count += 1
                
                # Safety check to avoid infinite loops
                if page_count > 100:  # Reasonable limit
                    logger.warning("Reached maximum page limit (100)")
                    break
            
            logger.info(f"Scraping completed! Total jobs: {len(self.data)} across {page_count} pages")
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
        
        finally:
            self.close_driver()
    
    def get_results(self):
        """Get the scraped results"""
        return {
            "company": "google",
            "total_jobs": len(self.data),
            "unique_jobs": len(self.processed_links),
            "scraping_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": self.data
        }
    
    def save_results(self, filename="google.json"):
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
    url = "https://www.google.com/about/careers/applications/jobs/results?location=India&sort_by=date"
    
    scraper = GoogleCareersScraper(headless=True, timeout=15)
    
    try:
        start_time = time.time()
        logger.info("Starting Google careers scraping...")
        
        scraper.scrape_all_jobs(url)
        
        end_time = time.time()
        scraping_time = end_time - start_time
        
        results = scraper.get_results()
        results["scraping_time_seconds"] = round(scraping_time, 2)
        
        # Print results
        json_output = json.dumps(results, indent=2, ensure_ascii=False)
        print(json_output)
        
        # Save to file
        scraper.save_results()
        
        logger.info(f"Scraping completed in {scraping_time:.2f} seconds")
        logger.info(f"Total jobs scraped: {len(results['data'])}")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()