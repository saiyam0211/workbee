from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import threading
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AmazonJobsScraper:
    def __init__(self, headless=True, timeout=10):
        self.timeout = timeout
        self.data = []
        self.PAGINATION_LIST_CLASS_NAME = "ehuj7it0"
        self.UNORDERED_LIST_CLASS_NAME = "jobs-module_root__gY8Hp"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Optimized Chrome options for faster performance
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-images")
        self.chrome_options.add_argument("--disable-plugins")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = None
        self.wait = None
        self.lock = threading.Lock()
    
    def init_driver(self):
        """Initialize driver and wait object"""
        if not self.driver:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
    
    def close_driver(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def safe_find_element(self, by, value, timeout=None):
        """Safely find element with timeout"""
        try:
            if timeout:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            return self.driver.find_element(by, value)
        except (TimeoutException, NoSuchElementException) as e:
            logger.warning(f"Element not found: {by}={value}, Error: {str(e)}")
            return None
    
    def extract_job_data_from_page(self):
        """Extract job data from current page"""
        jobs_data = []
        
        try:
            # Wait for job listings to load with reduced timeout
            ul = self.safe_find_element(By.CLASS_NAME, self.UNORDERED_LIST_CLASS_NAME, timeout=8)
            if not ul:
                logger.warning("Job listings container not found")
                return jobs_data
            
            # Use BeautifulSoup for faster parsing
            soup = BeautifulSoup(ul.get_attribute("outerHTML"), "html.parser")
            job_list = soup.find_all("li")
            
            for job in job_list:
                try:
                    h3 = job.find("h3")
                    if not h3:
                        continue
                        
                    title = h3.get_text(strip=True)
                    link_elem = h3.find("a")
                    if not link_elem:
                        continue
                        
                    link = "https://amazon.jobs" + link_elem.get("href")
                    
                    # More robust location extraction
                    location_elem = job.find("div", class_="metadatum-module_text__ncKFr")
                    location = location_elem.get_text(strip=True) if location_elem else "Location not specified"
                    
                    jobs_data.append({
                        "job_title": title,
                        "job_location": location,
                        "job_link": link
                    })
                    
                except Exception as e:
                    logger.warning(f"Error parsing job: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
        
        return jobs_data
    
    def get_total_pages(self):
        """Get total number of pages"""
        try:
            pagination_list = self.safe_find_element(By.CLASS_NAME, self.PAGINATION_LIST_CLASS_NAME, timeout=5)
            if not pagination_list:
                logger.warning("Pagination not found, assuming single page")
                return 1
            
            soup = BeautifulSoup(pagination_list.get_attribute("outerHTML"), "html.parser")
            pagination_items = soup.find_all("li")
            
            if pagination_items:
                last_page_button = pagination_items[-1].find("button")
                if last_page_button and last_page_button.get("data-test-id"):
                    return int(last_page_button.get("data-test-id"))
            
            return 1
            
        except Exception as e:
            logger.error(f"Error getting total pages: {str(e)}")
            return 1
    
    def navigate_to_next_page(self):
        """Navigate to next page"""
        try:
            next_button = self.safe_find_element(By.CSS_SELECTOR, 'button[data-test-id="next-page"]', timeout=3)
            if next_button and next_button.is_enabled():
                self.driver.execute_script("arguments[0].click();", next_button)
                # Reduced wait time
                time.sleep(1)
                return True
            return False
        except Exception as e:
            logger.warning(f"Error navigating to next page: {str(e)}")
            return False
    
    def scrape_category_fast(self, url):
        """Fast scraping using requests where possible"""
        category_data = []
        
        try:
            # Try to get initial page with requests first
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Check if we can extract jobs directly from HTML
                job_list = soup.find_all("li")
                if job_list:
                    for job in job_list:
                        try:
                            h3 = job.find("h3")
                            if not h3:
                                continue
                                
                            title = h3.get_text(strip=True)
                            link_elem = h3.find("a")
                            if not link_elem:
                                continue
                                
                            link = "https://amazon.jobs" + link_elem.get("href")
                            
                            location_elem = job.find("div", class_="metadatum-module_text__ncKFr")
                            location = location_elem.get_text(strip=True) if location_elem else "Location not specified"
                            
                            category_data.append({
                                "job_title": title,
                                "job_location": location,
                                "job_link": link
                            })
                            
                        except Exception as e:
                            continue
                    
                    if category_data:
                        logger.info(f"Fast scraping successful for {url}: {len(category_data)} jobs")
                        return category_data
            
            # Fallback to Selenium if requests method fails
            logger.info(f"Falling back to Selenium for {url}")
            return self.scrape_category_selenium(url)
            
        except Exception as e:
            logger.error(f"Error in fast scraping {url}: {str(e)}")
            return self.scrape_category_selenium(url)
    
    def scrape_category_selenium(self, url):
        """Original Selenium-based scraping as fallback"""
        category_data = []
        
        try:
            self.init_driver()
            logger.info(f"Scraping category with Selenium: {url}")
            
            self.driver.get(url)
            time.sleep(2)  # Reduced initial page load time
            
            total_pages = self.get_total_pages()
            logger.info(f"Found {total_pages} pages to scrape")
            
            # Limit pages for faster scraping
            max_pages = min(total_pages, 5)  # Limit to 5 pages per category for speed
            
            current_page = 1
            while current_page <= max_pages:
                logger.info(f"Scraping page {current_page}/{max_pages}")
                
                # Extract jobs from current page
                page_jobs = self.extract_job_data_from_page()
                category_data.extend(page_jobs)
                logger.info(f"Extracted {len(page_jobs)} jobs from page {current_page}")
                
                # Navigate to next page if not the last page
                if current_page < max_pages:
                    if not self.navigate_to_next_page():
                        logger.warning(f"Failed to navigate to page {current_page + 1}")
                        break
                
                current_page += 1
            
            logger.info(f"Category completed. Total jobs extracted: {len(category_data)}")
            
        except Exception as e:
            logger.error(f"Error scraping category {url}: {str(e)}")
        
        finally:
            self.close_driver()
        
        return category_data
    
    def scrape_category(self, url):
        """Main category scraping method"""
        return self.scrape_category_fast(url)
    
    def scrape_all_categories_parallel(self, urls, max_workers=5):
        """Scrape multiple categories with parallel processing"""
        all_data = []
        start_time = time.time()
        
        # Prepare URLs with country filter
        category_urls = [url + "?country%5B%5D=IN" for url in urls]
        
        logger.info(f"Starting parallel scraping of {len(category_urls)} categories with {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all category scraping tasks
            future_to_url = {
                executor.submit(self.scrape_category, url): url 
                for url in category_urls
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    category_data = future.result()
                    with self.lock:
                        all_data.extend(category_data)
                        logger.info(f"Completed {url}: {len(category_data)} jobs (Total: {len(all_data)})")
                        
                except Exception as e:
                    logger.error(f"Error processing {url}: {str(e)}")
        
        end_time = time.time()
        logger.info(f"Parallel scraping completed in {end_time - start_time:.2f} seconds")
        
        return all_data
    
    def scrape_all_categories(self, urls, max_workers=5):
        """Main method for scraping all categories"""
        return self.scrape_all_categories_parallel(urls, max_workers)

def main():
    """Main execution function"""
    engineering_tech_categories = [
        "https://amazon.jobs/content/en/job-categories/business-intelligence-data-engineering",
        "https://amazon.jobs/content/en/job-categories/data-science",
        "https://amazon.jobs/content/en/job-categories/database-administration",
        "https://amazon.jobs/content/en/job-categories/hardware-development",
        "https://amazon.jobs/content/en/job-categories/machine-learning-science",
        "https://amazon.jobs/content/en/job-categories/operations-it-support-engineering",
        "https://amazon.jobs/content/en/job-categories/project-program-product-management-technical",
        "https://amazon.jobs/content/en/job-categories/research-science",
        "https://amazon.jobs/content/en/job-categories/software-development",
        "https://amazon.jobs/content/en/job-categories/solutions-architecture",
        "https://amazon.jobs/content/en/job-categories/systems-quality-security-engineering"
    ]
    
    scraper = AmazonJobsScraper(headless=True, timeout=10)
    
    try:
        logger.info("Starting optimized Amazon jobs scraping...")
        start_time = time.time()
        
        all_jobs = scraper.scrape_all_categories(engineering_tech_categories, max_workers=5)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        logger.info(f"Scraping completed in {elapsed_time:.2f} seconds")
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        logger.info(f"Jobs per second: {len(all_jobs)/elapsed_time:.2f}")
        
        # Generate output
        result = {
            "company": "amazon",
            "total_jobs": len(all_jobs),
            "scraping_time": f"{elapsed_time:.2f} seconds",
            "jobs_per_second": f"{len(all_jobs)/elapsed_time:.2f}",
            "data": all_jobs
        }
        
        json_output = json.dumps(result, indent=2, ensure_ascii=False)
        print(json_output)
        
        # Save to file
        with open('amazon_jobs.json', 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        logger.info("Results saved to amazon_jobs.json")
        
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")
    
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main()