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

class AMDCareersScraper:
    def __init__(self, headless=True, timeout=20):
        self.timeout = timeout
        self.data = []
        self.processed_links = set()  # To avoid duplicates
        self.BASE_URL = "https://careers.amd.com"
        
        # Multiple selectors for job containers (fallback options)
        self.JOB_CONTAINER_SELECTORS = [
            "job-results-container",
            "mat-expansion-panel-header",
            "job-card",
            "search-results",
            ".job-results"
        ]
        
        # Job element selectors
        self.JOB_ITEM_SELECTORS = [
            "mat-expansion-panel",
            ".job-item",
            ".job-card",
            "[data-job-id]"
        ]
        
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
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        # Keep JavaScript enabled for dynamic content
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
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to load completely"""
        try:
            # Wait for document ready state
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait for Angular/dynamic content
            time.sleep(3)
            
            # Try to wait for job content to be visible
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "mat-expansion-panel"))
                )
            except TimeoutException:
                logger.warning("mat-expansion-panel not found, trying alternative selectors")
            
        except TimeoutException:
            logger.warning("Page load timeout reached")
    
    def scroll_to_load_content(self):
        """Scroll down to trigger lazy loading"""
        try:
            # Get initial page height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            scroll_attempts = 0
            max_scrolls = 5
            
            while scroll_attempts < max_scrolls:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for new content to load
                time.sleep(2)
                
                # Calculate new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                    
                last_height = new_height
                scroll_attempts += 1
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            logger.info(f"Completed {scroll_attempts} scroll attempts to load content")
            
        except Exception as e:
            logger.warning(f"Error during scrolling: {str(e)}")
    
    def find_job_container(self):
        """Find the job container using multiple strategies"""
        job_container = None
        
        # Try different selectors
        for selector in self.JOB_CONTAINER_SELECTORS:
            try:
                if selector.startswith('.'):
                    job_container = self.driver.find_element(By.CSS_SELECTOR, selector)
                else:
                    job_container = self.driver.find_element(By.CLASS_NAME, selector)
                
                if job_container:
                    logger.info(f"Found job container using selector: {selector}")
                    break
                    
            except NoSuchElementException:
                continue
        
        # If no specific container found, try to get the entire page body
        if not job_container:
            try:
                job_container = self.driver.find_element(By.TAG_NAME, "body")
                logger.info("Using body tag as job container")
            except Exception as e:
                logger.error(f"Could not find any job container: {str(e)}")
        
        return job_container
    
    def extract_jobs_from_current_page(self):
        """Extract job data from the current page"""
        jobs_data = []
        
        try:
            # Wait for page to load completely
            self.wait_for_page_load()
            
            # Scroll to load any lazy-loaded content
            self.scroll_to_load_content()
            
            # Find job container
            job_container = self.find_job_container()
            if not job_container:
                logger.error("No job container found")
                return jobs_data
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(job_container.get_attribute("outerHTML"), "html.parser")
            
            # Try different selectors to find job items
            job_items = []
            for selector in self.JOB_ITEM_SELECTORS:
                if selector.startswith('.'):
                    job_items = soup.select(selector)
                else:
                    job_items = soup.find_all(selector)
                
                if job_items:
                    logger.info(f"Found {len(job_items)} job items using selector: {selector}")
                    break
            
            if not job_items:
                logger.warning("No job items found with any selector")
                # Debug: print available elements
                logger.debug("Available elements in container:")
                for tag in soup.find_all(['div', 'mat-expansion-panel', 'article'])[:5]:
                    logger.debug(f"Tag: {tag.name}, Classes: {tag.get('class', [])}")
                return jobs_data
            
            logger.info(f"Processing {len(job_items)} job items")
            
            for i, job in enumerate(job_items):
                try:
                    # Multiple strategies for finding job title and link
                    title = None
                    link = None
                    location = None
                    
                    # Strategy 1: Look for .job-title-link
                    link_tag = job.select_one(".job-title-link")
                    if link_tag:
                        title = link_tag.get_text(strip=True)
                        href = link_tag.get("href")
                        if href:
                            link = urljoin(self.BASE_URL, href)
                    
                    # Strategy 2: Look for any link with job-related text
                    if not link_tag:
                        link_candidates = job.find_all("a", href=True)
                        for candidate in link_candidates:
                            href = candidate.get("href")
                            if href and ("job" in href.lower() or "career" in href.lower()):
                                title = candidate.get_text(strip=True)
                                link = urljoin(self.BASE_URL, href)
                                break
                    
                    # Strategy 3: Look for h1, h2, h3 tags
                    if not title:
                        for header_tag in job.find_all(['h1', 'h2', 'h3', 'h4']):
                            text = header_tag.get_text(strip=True)
                            if text and len(text) > 5:  # Reasonable title length
                                title = text
                                break
                    
                    # Extract location with multiple strategies
                    location_selectors = [".location", ".job-location", "[data-location]", ".city"]
                    for loc_selector in location_selectors:
                        loc_elem = job.select_one(loc_selector)
                        if loc_elem:
                            location = loc_elem.get_text(strip=True).replace('\n', ' ').replace('\t', ' ')
                            # Clean up extra whitespace
                            location = ' '.join(location.split())
                            break
                    
                    # Skip if essential data is missing
                    if not title or len(title.strip()) < 3:
                        logger.debug(f"Skipping job {i+1}: No valid title found")
                        continue
                    
                    # Use a placeholder link if none found
                    if not link:
                        link = f"{self.BASE_URL}/jobs/{i+1}"
                        logger.debug(f"Using placeholder link for job: {title}")
                    
                    # Check for duplicates
                    if link in self.processed_links:
                        logger.debug(f"Skipping duplicate job: {title}")
                        continue
                    
                    self.processed_links.add(link)
                    
                    job_data = {
                        "job_title": title,
                        "job_location": location or "Location not specified",
                        "job_link": link
                    }
                    
                    jobs_data.append(job_data)
                    logger.debug(f"Extracted job {len(jobs_data)}: {title[:50]}...")
                    
                except Exception as e:
                    logger.warning(f"Error parsing job {i+1}: {str(e)}")
                    continue
            
            logger.info(f"Successfully extracted {len(jobs_data)} jobs from current page")
            
        except Exception as e:
            logger.error(f"Error extracting jobs from page: {str(e)}")
        
        return jobs_data
    
    def navigate_to_next_page(self):
        """Navigate to the next page"""
        try:
            # Multiple strategies to find the next button
            next_button_selectors = [
                '//button[@aria-label="Next Page of Job Search Results"]',
                '//button[contains(@class, "next")]',
                '//a[contains(@class, "next")]',
                '//button[contains(text(), "Next")]',
                '//a[contains(text(), "Next")]',
                '//button[@data-direction="next"]'
            ]
            
            next_button = None
            for selector in next_button_selectors:
                try:
                    next_button = self.driver.find_element(By.XPATH, selector)
                    if next_button.is_displayed() and next_button.is_enabled():
                        logger.info(f"Found next button with selector: {selector}")
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
            self.wait_for_page_load()
            logger.info("Successfully navigated to next page")
            
            return True
            
        except ElementClickInterceptedException:
            logger.warning("Next button click was intercepted")
            return False
        except Exception as e:
            logger.warning(f"Error navigating to next page: {str(e)}")
            return False
    
    def scrape_all_jobs(self, url):
        """Scrape all job listings from AMD Careers"""
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
                if page_count > 50:  # Reasonable limit
                    logger.warning("Reached maximum page limit (50)")
                    break
            
            logger.info(f"Scraping completed! Total jobs: {len(self.data)} across {page_count} pages")
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
        
        finally:
            self.close_driver()
    
    def get_results(self):
        """Get the scraped results"""
        return {
            "company": "amd",
            "total_jobs": len(self.data),
            "unique_jobs": len(self.processed_links),
            "scraping_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": self.data
        }
    
    def save_results(self, filename="amd.json"):
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
    url = "https://careers.amd.com/careers-home/jobs?categories=Engineering&page=1&location=India&woe=12&regionCode=IN&stretchUnit=MILES&stretch=10&country=India&limit=100"
    
    scraper = AMDCareersScraper(headless=True, timeout=20)  # Set headless=False for debugging
    
    try:
        start_time = time.time()
        logger.info("Starting AMD careers scraping...")
        
        scraper.scrape_all_jobs(url)
        
        end_time = time.time()
        scraping_time = end_time - start_time
        
        results = scraper.get_results()
        results["scraping_time_seconds"] = round(scraping_time, 2)
        
        # Print results
        print(f"Data Length: {len(results['data'])}")
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