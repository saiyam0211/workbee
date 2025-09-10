"""
Amazon job scraper
"""
import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseJobScraper, JobData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging

logger = logging.getLogger(__name__)

class AmazonScraper(BaseJobScraper):
    """Amazon job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Amazon",
            base_url="https://www.amazon.jobs/en/search?base_query=&loc_query=India&latitude=&longitude=&loc_group_id=&invalid_location=false&country=&city=&region=&county=&query_options=&",
            headless=headless
        )
    
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Amazon jobs with proper pagination"""
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (max {max_pages} pages)...")
        
        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=10)
            
            # Track unique jobs to avoid duplicates
            seen_jobs = set()
            
            for page_num in range(max_pages):
                logger.info(f"📄 Scraping page {page_num + 1} of {max_pages}")
                
                # Wait for job list to load - try multiple selectors
                job_loaded = False
                selectors_to_wait_for = [
                    'div[data-testid="job-result"]',
                    'div[class*="job-result"]',
                    'div[class*="result-item"]',
                    'div[class*="job-item"]',
                    'h1.job-title',
                    'div[class*="search-results"]',
                    'div[class*="job-list"]'
                ]
                
                for selector in selectors_to_wait_for:
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        logger.info(f"✅ Found elements with selector: {selector}")
                        job_loaded = True
                        break
                    except TimeoutException:
                        continue
                
                if not job_loaded:
                    logger.warning("Job list not found with any selector, waiting longer...")
                    time.sleep(5)  # Wait a bit more for dynamic content
                    
                    # Try scrolling to trigger lazy loading
                    logger.info("🔄 Scrolling to trigger lazy loading...")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(2)
                
                # Find job containers using the correct selector - use job-list
                job_list_container = self.driver.find_element(By.CSS_SELECTOR, 'div[class*="job-list"]')
                logger.info(f"🔍 Found job-list container")
                
                # Look for individual job elements inside the job-list - use job-tile
                job_containers = job_list_container.find_elements(By.CSS_SELECTOR, 'div.job-tile')
                logger.info(f"🔍 Found {len(job_containers)} job containers inside job-list")
                
                real_jobs_found_on_page = 0
                
                for i, job_container in enumerate(job_containers):
                    try:
                        # Extract job title from h3.job-title > a.job-link
                        try:
                            title_element = job_container.find_element(By.CSS_SELECTOR, 'h3.job-title a.job-link')
                            job_title = title_element.text.strip()
                            job_link = title_element.get_attribute('href')
                            # Make sure it's a full URL
                            if job_link and not job_link.startswith('http'):
                                job_link = 'https://www.amazon.jobs' + job_link
                        except NoSuchElementException:
                            continue
                        
                        # Extract location from .location-and-id
                        try:
                            location_element = job_container.find_element(By.CSS_SELECTOR, '.location-and-id')
                            location = location_element.text.strip()
                        except NoSuchElementException:
                            location = "India"
                        
                        # Extract posted date - look for date elements
                        posted_date = "Not specified"
                        try:
                            # Try different date selectors
                            date_selectors = [
                                'h2.posting-date',
                                '.posting-date',
                                '.date',
                                '.job-date',
                                'time'
                            ]
                            for selector in date_selectors:
                                try:
                                    date_element = job_container.find_element(By.CSS_SELECTOR, selector)
                                    posted_date = date_element.text.strip()
                                    if posted_date:
                                        break
                                except NoSuchElementException:
                                    continue
                        except NoSuchElementException:
                            pass
                        
                        # Skip if no title
                        if not job_title or len(job_title) < 3:
                            continue
                        
                        # Check for duplicates
                        job_key = f"{job_title}_{job_link}"
                        if job_key not in seen_jobs:
                            # Get job description by visiting the job page
                            job_description = self.get_job_description(job_link) if job_link else "Job description available on company website"
                            
                            job_data = JobData(
                                title=job_title,
                                location=location,
                                experience_required="Not specified",
                                job_description=job_description,
                                job_link=job_link,
                                posted_date=posted_date,
                                company=self.company_name
                            )
                            
                            self.jobs_data.append(job_data)
                            seen_jobs.add(job_key)
                            real_jobs_found_on_page += 1
                            logger.info(f"✅ Scraped: {job_title} - {location}")
                            
                            # Limit per page to avoid too many results
                            if real_jobs_found_on_page >= 15:
                                break
                                    
                    except Exception as e:
                        logger.warning(f"Error processing job {i+1}: {str(e)}")
                        continue
                
                logger.info(f"📊 Page {page_num + 1}: Found {real_jobs_found_on_page} new jobs (Total unique: {len(self.jobs_data)})")
                
                # Try to go to next page if not on last page
                if page_num < max_pages - 1:
                    if not self.find_next_page_button(page_num + 2):
                        logger.info("🔚 No more pages available, stopping pagination")
                        break
                    self.wait_for_page_load(3)
            
            logger.info(f"🎉 Successfully scraped {len(self.jobs_data)} UNIQUE jobs from {self.company_name} across {max_pages} pages")
            return self.jobs_data
            
        except Exception as e:
            logger.error(f"❌ Error during scraping: {str(e)}")
            return []
            
        finally:
            self.close_driver()
    
    def get_job_description(self, job_url: str) -> str:
        """Get job description from individual job page"""
        try:
            # Open job page in new tab
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(job_url)
            
            # Wait for job content to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-12.col-md-7.col-lg-8.col-xl-9'))
                )
                
                # Look for read-more button and click it if present
                try:
                    read_more_button = self.driver.find_element(By.CSS_SELECTOR, 'a.read-more, button.read-more, .read-more')
                    if read_more_button.is_displayed() and read_more_button.is_enabled():
                        self.driver.execute_script("arguments[0].click();", read_more_button)
                        time.sleep(2)  # Wait for content to expand
                        logger.info("✅ Clicked read-more button")
                except NoSuchElementException:
                    logger.info("No read-more button found, trying to extract directly")
                
                # Extract job description from the specified div
                job_description_div = self.driver.find_element(By.CSS_SELECTOR, 'div.col-12.col-md-7.col-lg-8.col-xl-9')
                job_description = job_description_div.text.strip()
                
                # Close the tab and switch back
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                
                return job_description if job_description else "Job description available on company website"
                
            except TimeoutException:
                logger.warning(f"Could not load job details for {job_url}")
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return "Job description available on company website"
                
        except Exception as e:
            logger.warning(f"Error getting job description: {str(e)}")
            try:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return "Job description available on company website"
    
    def find_next_page_button(self, next_page_num: int) -> bool:
        """Find and click next page button for Amazon using pagination-control"""
        try:
            # Look for pagination in .pagination-control
            pagination_div = self.driver.find_element(By.CSS_SELECTOR, '.pagination-control')
            
            # Find the next page button with data-label attribute
            next_page_button = pagination_div.find_element(By.CSS_SELECTOR, f'button[data-label="{next_page_num}"]')
            
            if next_page_button.is_enabled():
                self.driver.execute_script("arguments[0].click();", next_page_button)
                logger.info(f"✅ Clicked page {next_page_num} button")
                return True
            else:
                logger.info(f"Page {next_page_num} button is disabled")
                return False
                
        except NoSuchElementException:
            logger.warning(f"Could not find page {next_page_num} button")
            return False
        except Exception as e:
            logger.warning(f"Error clicking next page button: {str(e)}")
            return False

if __name__ == "__main__":
    scraper = AmazonScraper(headless=True)
    jobs = scraper.scrape_jobs()
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from Amazon")
