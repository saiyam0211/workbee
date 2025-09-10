"""
Airbnb job scraper
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

class AirbnbScraper(BaseJobScraper):
    """Airbnb job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Airbnb",
            base_url="https://careers.airbnb.com/positions/?location=India",
            headless=headless
        )
    
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Airbnb jobs with proper pagination"""
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (max {max_pages} pages)...")
        
        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=10)
            
            # Track unique jobs to avoid duplicates
            seen_jobs = set()
            
            for page_num in range(max_pages):
                logger.info(f"📄 Scraping page {page_num + 1} of {max_pages}")
                
                # Wait for job list to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[role="list"]'))
                    )
                except TimeoutException:
                    logger.warning("Job list not found, trying alternative selectors")
                
                # Find job elements using the specific Airbnb structure
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, 'ul[role="list"] li[role="listitem"]')
                logger.info(f"🔍 Found {len(job_elements)} job elements on page {page_num + 1}")
                
                real_jobs_found_on_page = 0
                
                for i, element in enumerate(job_elements):
                    try:
                        # Extract job title and link from first div > h3 > a
                        title_element = element.find_element(By.CSS_SELECTOR, 'div:first-child h3 a')
                        job_title = title_element.text.strip()
                        job_link = title_element.get_attribute('href')
                        
                        # Extract location from span with specific classes
                        try:
                            location_element = element.find_element(By.CSS_SELECTOR, 'span.text-size-4.font-normal.text-gray-48.flex.items-center')
                            location = location_element.text.strip()
                        except NoSuchElementException:
                            location = "India"
                        
                        # Skip if no title
                        if not job_title or len(job_title) < 3:
                            continue
                        
                        # Check for duplicates
                        job_key = f"{job_title}_{job_link}"
                        if job_key not in seen_jobs:
                            # Get job description by visiting the job page
                            job_description = self.get_job_description(job_link)
                            
                            job_data = JobData(
                                title=job_title,
                                location=location,
                                experience_required="Not specified",
                                job_description=job_description,
                                job_link=job_link,
                                posted_date="Not specified",
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
            
            # Wait for job detail to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.job-detail.active'))
                )
                
                # Extract job description from .job-detail.active
                job_detail = self.driver.find_element(By.CSS_SELECTOR, '.job-detail.active')
                job_description = job_detail.text.strip()
                
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
        """Find and click next page button for Airbnb using facetwp-pager"""
        try:
            # Look for pagination in .facetwp-pager
            pagination_div = self.driver.find_element(By.CSS_SELECTOR, '.facetwp-pager')
            
            # Find the next page link with data-page attribute
            next_page_link = pagination_div.find_element(By.CSS_SELECTOR, f'a[data-page="{next_page_num}"]')
            
            if next_page_link.is_enabled():
                self.driver.execute_script("arguments[0].click();", next_page_link)
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
    scraper = AirbnbScraper(headless=True)
    jobs = scraper.scrape_jobs()
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from Airbnb")
