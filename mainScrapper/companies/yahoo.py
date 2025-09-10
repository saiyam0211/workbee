"""
Yahoo job scraper
"""
import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseJobScraper, JobData
import logging

logger = logging.getLogger(__name__)

class YahooScraper(BaseJobScraper):
    """Yahoo job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Yahoo",
            base_url="https://ouryahoo.wd5.myworkdayjobs.com/en-US/YahooCareers/jobs?locationCountry=bc33aa3152ec42d4995f4791a106ed09",
            headless=headless
        )
    
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Yahoo jobs with pagination"""
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (max {max_pages} pages)...")
        
        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=10)
            
            # Track unique jobs to avoid duplicates
            seen_jobs = set()
            
            for page_num in range(max_pages):
                logger.info(f"📄 Scraping page {page_num + 1} of {max_pages}")
                
                # Find job elements
                job_elements = self.driver.find_elements("css selector", ".job-item")
                if not job_elements:
                    job_elements = self.driver.find_elements("css selector", "[data-testid='job-item']")
                if not job_elements:
                    job_elements = self.driver.find_elements("css selector", ".job")
                
                logger.info(f"🔍 Found {len(job_elements)} potential job elements on page {page_num + 1}")
                
                real_jobs_found_on_page = 0
                
                for i, element in enumerate(job_elements):
                    try:
                        text_content = element.text.strip()
                        
                        # Skip empty elements
                        if not text_content or len(text_content) < 10:
                            continue
                        
                        # Look for real job content
                        if "Yahoo" in text_content or "India" in text_content or "Bangalore" in text_content:
                            job_data = self.extract_job_data(element, i)
                            if job_data and job_data.title not in ["Job", "Learn more", "share", "..."] and len(job_data.title) > 5:
                                # Check for duplicates using job title and link
                                job_key = f"{job_data.title}_{job_data.job_link}"
                                if job_key not in seen_jobs:
                                    self.jobs_data.append(job_data)
                                    seen_jobs.add(job_key)
                                    real_jobs_found_on_page += 1
                                    logger.info(f"✅ Scraped: {job_data.title}")
                                
                                # Limit per page to avoid too many results
                                if real_jobs_found_on_page >= 15:
                                    break
                                    
                    except Exception as e:
                        continue
                
                logger.info(f"📊 Page {page_num + 1}: Found {real_jobs_found_on_page} new jobs (Total unique: {len(self.jobs_data)})")
                
                # Try to go to next page if not on last page
                if page_num < max_pages - 1:
                    if not self.find_next_page_button():
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
    
    def find_next_page_button(self) -> bool:
        """Find and click next page button for Yahoo"""
        try:
            # Yahoo uses different pagination methods
            next_selectors = [
                "button[aria-label='Next page']",
                "button[aria-label='Next']",
                ".next-page",
                "[data-testid='next-page']",
                "button:contains('Next')",
                "a:contains('Next')",
                ".pagination-next"
            ]
            
            for selector in next_selectors:
                try:
                    next_button = self.driver.find_element("css selector", selector)
                    if next_button.is_enabled():
                        self.driver.execute_script("arguments[0].click();", next_button)
                        logger.info("✅ Clicked next page button")
                        return True
                except:
                    continue
            
            # Try scrolling to load more
            logger.info("🔄 Trying infinite scroll to load more jobs...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Could not find next page button: {str(e)}")
            return False
if __name__ == "__main__":
    scraper = YahooScraper(headless=True)
    jobs = scraper.scrape_jobs()
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from Yahoo")
