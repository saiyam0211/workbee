"""
Apple job scraper
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

class AppleScraper(BaseJobScraper):
    """Apple job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Apple",
            base_url="https://jobs.apple.com/en-in/search?location=india-INDC",
            headless=headless
        )
        
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Apple jobs with proper pagination"""
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
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list li.listitem'))
                    )
                except TimeoutException:
                    logger.warning("Job list not found, trying alternative selectors")
                
                # Debug: Check what elements are actually present
                logger.info("🔍 Debugging page elements...")
                
                # Try different selectors to find job containers
                selectors_to_try = [
                    'ul.list li.listitem',
                    'ul.list',
                    'li.listitem',
                    'ul[class*="list"]',
                    'li[class*="listitem"]',
                    'ul[class*="job"]',
                    'li[class*="job"]',
                    'div[class*="job"]',
                    'div[class*="result"]',
                    'tr',
                    'tbody tr'
                ]
                
                for selector in selectors_to_try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    logger.info(f"Selector '{selector}': Found {len(elements)} elements")
                    if elements:
                        logger.info(f"First element text: {elements[0].text[:100]}...")
                
                # Find job containers using the working selectors
                job_containers = self.driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"]')
                logger.info(f"🔍 Found {len(job_containers)} job containers on page {page_num + 1}")
                
                # Debug: Check what's inside the job containers
                for i, container in enumerate(job_containers[:3]):  # Check first 3 containers
                    logger.info(f"Job container {i+1} HTML: {container.get_attribute('outerHTML')[:500]}...")
                
                real_jobs_found_on_page = 0
                
                for i, job_container in enumerate(job_containers):
                    try:
                        # Extract job title and link from a.link-inline.t-intro.word-wrap-break-word.more
                        try:
                            title_element = job_container.find_element(By.CSS_SELECTOR, 'a.link-inline.t-intro.word-wrap-break-word.more')
                            job_title = title_element.text.strip()
                            job_link = title_element.get_attribute('href')
                            # Make sure it's a full URL
                            if job_link and not job_link.startswith('http'):
                                job_link = 'https://jobs.apple.com' + job_link
                        except NoSuchElementException:
                            continue
                        
                        # Extract location from span.table--advanced-search__location-sub
                        try:
                            location_element = job_container.find_element(By.CSS_SELECTOR, 'span.table--advanced-search__location-sub')
                            location = location_element.text.strip()
                        except NoSuchElementException:
                            location = "India"
                        
                        # Extract posted date from span.job-posted-date
                        try:
                            date_element = job_container.find_element(By.CSS_SELECTOR, 'span.job-posted-date')
                            posted_date = date_element.text.strip()
                        except NoSuchElementException:
                            posted_date = "Not specified"
                        
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
                            if real_jobs_found_on_page >= 100:
                                break
                            
                    except Exception as e:
                        logger.warning(f"Error processing job {i+1}: {str(e)}")
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
    
    def get_job_description(self, job_url: str) -> str:
        """Get formatted job description from individual job page"""
        try:
            # Open job page in new tab
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(job_url)
            
            # Wait for job content to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div#jobdetails-jobdetails-jobdescription-content-row'))
                )
                
                job_description_parts = []
                
                # Extract Description
                try:
                    description_div = self.driver.find_element(By.CSS_SELECTOR, 'div#jobdetails-jobdetails-jobdescription-content-row')
                    description_span = description_div.find_element(By.CSS_SELECTOR, 'span')
                    description_text = description_span.text.strip()
                    if description_text:
                        job_description_parts.append("Description")
                        job_description_parts.append(description_text)
                except NoSuchElementException:
                    pass
                
                # Extract Minimum Qualifications
                try:
                    min_qual_div = self.driver.find_element(By.CSS_SELECTOR, 'div#jobdetails-jobdetails-minimumqualifications-content-row')
                    min_qual_ul = min_qual_div.find_element(By.CSS_SELECTOR, 'ul')
                    min_qual_items = min_qual_ul.find_elements(By.CSS_SELECTOR, 'li')
                    min_qual_text = '\n'.join([item.text.strip() for item in min_qual_items if item.text.strip()])
                    if min_qual_text:
                        job_description_parts.append("\n\nMinimum Qualifications")
                        job_description_parts.append(min_qual_text)
                except NoSuchElementException:
                    pass
                
                # Extract Preferred Qualifications
                try:
                    pref_qual_div = self.driver.find_element(By.CSS_SELECTOR, 'div#jobdetails-jobdetails-preferredqualifications-content-row')
                    pref_qual_ul = pref_qual_div.find_element(By.CSS_SELECTOR, 'ul')
                    pref_qual_items = pref_qual_ul.find_elements(By.CSS_SELECTOR, 'li')
                    pref_qual_text = '\n'.join([item.text.strip() for item in pref_qual_items if item.text.strip()])
                    if pref_qual_text:
                        job_description_parts.append("\n\nPreferred Qualifications")
                        job_description_parts.append(pref_qual_text)
                except NoSuchElementException:
                    pass
                
                # Close the tab and switch back
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                
                job_description = '\n'.join(job_description_parts)
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
    
    def find_next_page_button(self) -> bool:
        """Find and click next page button for Apple using multiple selectors"""
        try:
            # Wait for page to fully load
            time.sleep(2)
            
            # Try multiple selectors for pagination
            next_selectors = [
                'div.rc-pagination-arrow button[data-analytics-pagination="next"]',
                'button[data-analytics-pagination="next"]',
                'div.rc-pagination-arrow button',
                'nav.rc-pagination div.rc-pagination-arrow button',
                'button[aria-label*="next"]',
                'button[aria-label*="Next"]',
                'a[aria-label*="next"]',
                'a[aria-label*="Next"]'
            ]
            
            next_page_button = None
            for selector in next_selectors:
                try:
                    next_page_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    logger.info(f"Found next page button with selector: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if next_page_button:
                # Check if button is visible and enabled
                if next_page_button.is_displayed() and next_page_button.is_enabled():
                    # Scroll to the button to make sure it's in view
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                    time.sleep(1)
                    
                    # Try clicking with JavaScript first
                    try:
                        self.driver.execute_script("arguments[0].click();", next_page_button)
                        logger.info("✅ Clicked next page button with JavaScript")
                    except:
                        # Fallback to regular click
                        next_page_button.click()
                        logger.info("✅ Clicked next page button with regular click")
                    
                    # Wait for page to load
                    time.sleep(3)
                    return True
                else:
                    logger.info("Next page button is not visible or enabled")
                    return False
            else:
                logger.warning("Could not find next page button with any selector")
                return False
                
        except Exception as e:
            logger.warning(f"Error clicking next page button: {str(e)}")
            return False

if __name__ == "__main__":
    scraper = AppleScraper(headless=False)
    jobs = scraper.scrape_jobs()
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from Apple")