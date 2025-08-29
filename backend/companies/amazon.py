from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
# from app.config.logger import setup_logger  # Removed due to import issues
from datetime import datetime

# Minimal logger replacement
class _SimpleLogger:
    def info(self, msg):
        print(f"[INFO] {msg}")
    def warning(self, msg):
        print(f"[WARN] {msg}")
    def error(self, msg):
        print(f"[ERROR] {msg}")

logger = _SimpleLogger()

class AmazonJobsScraper:
    def __init__(self, headless=True, timeout=10):
        self.timeout = timeout
        self.data = []
        self.PAGINATION_LIST_CLASS_NAME = "ehuj7it0"
        self.UNORDERED_LIST_CLASS_NAME = "jobs-module_root__gY8Hp"
        
        # Optimized Chrome options
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-images")  # Don't load images
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = None
        self.wait = None
    
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
    
    def _get_job_description_in_new_tab(self, job_link: str) -> str:
        try:
            original = self.driver.current_window_handle
            self.driver.execute_script("window.open('about:blank','_blank');")
            time.sleep(0.3)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(job_link)
            time.sleep(2)
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, "html.parser")
            selectors = [
                "div[data-testid='job-description']",
                ".job-description",
                "#job-description",
                "[class*='description']",
                "[class*='content']",
                "section",
                "article",
            ]
            text = "Description not available"
            for sel in selectors:
                node = soup.select_one(sel)
                if node:
                    t = node.get_text(" ", strip=True)
                    if t and len(t) > 50:
                        text = t
                        break
            self.driver.close()
            self.driver.switch_to.window(original)
            return text
        except Exception as e:
            try:
                # attempt to return to original window
                self.driver.switch_to.window(self.driver.window_handles[0])
            except Exception:
                pass
            logger.warning(f"Error extracting job description from {job_link}: {str(e)}")
            return "Description not available"
    
    def extract_job_data_from_page(self):
        """Extract job data from current page"""
        jobs_data = []
        
        try:
            # Wait for job listings to load
            ul = self.safe_find_element(By.CLASS_NAME, self.UNORDERED_LIST_CLASS_NAME, timeout=15)
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
                    
                    # Extract job description
                    job_description = self._get_job_description_in_new_tab(link)
                    
                    jobs_data.append({
                        "job_title": title,
                        "job_location": location,
                        "job_link": link,
                        "job_description": job_description,
                        "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            pagination_list = self.safe_find_element(By.CLASS_NAME, self.PAGINATION_LIST_CLASS_NAME, timeout=10)
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
            next_button = self.safe_find_element(By.CSS_SELECTOR, 'button[data-test-id="next-page"]', timeout=5)
            if next_button and next_button.is_enabled():
                self.driver.execute_script("arguments[0].click();", next_button)
                # Wait for page to load
                time.sleep(2)
                return True
            return False
        except Exception as e:
            logger.warning(f"Error navigating to next page: {str(e)}")
            return False
    
    def scrape_category(self, url):
        """Scrape all jobs from a category"""
        category_data = []
        
        try:
            self.init_driver()
            logger.info(f"Scraping category: {url}")
            
            self.driver.get(url)
            time.sleep(3)  # Initial page load
            
            total_pages = self.get_total_pages()
            logger.info(f"Found {total_pages} pages to scrape")
            
            current_page = 1
            while current_page <= total_pages:
                logger.info(f"Scraping page {current_page}/{total_pages}")
                
                # Extract jobs from current page
                page_jobs = self.extract_job_data_from_page()
                category_data.extend(page_jobs)
                logger.info(f"Extracted {len(page_jobs)} jobs from page {current_page}")
                
                # Navigate to next page if not the last page
                if current_page < total_pages:
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
    
    def scrape_all_categories(self, urls, max_workers=3):
        """Scrape multiple categories with threading"""
        all_data = []
        
        # Sequential processing (more stable for Selenium)
        for url in urls:
            category_url = url + "?country%5B%5D=IN"
            category_data = self.scrape_category(category_url)
            all_data.extend(category_data)
            
            # Brief pause between categories to avoid rate limiting
            time.sleep(2)
        
        return all_data

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
    
    scraper = AmazonJobsScraper(headless=True, timeout=15)
    logger.info("Starting Amazon jobs scraping...")
    start_time = time.time()
    
    all_jobs = scraper.scrape_all_categories(engineering_tech_categories)
    
    end_time = time.time()
    logger.info(f"Scraping completed in {end_time - start_time:.2f} seconds")
    logger.info(f"Total jobs scraped: {len(all_jobs)}")
    
    # Generate output
    result = {
        "company": "amazon",
        "data": all_jobs,
    }
    
    # Also persist to data/amazon.json alongside printing to stdout
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        out_path = os.path.join(data_dir, "amazon.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(all_jobs)} jobs to {out_path}")
    except Exception as e:
        logger.warning(f"Failed to write amazon.json: {e}")

    json_output = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_output)
    scraper.close_driver()

if __name__ == "__main__":
    main()