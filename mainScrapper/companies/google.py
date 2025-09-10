"""
Google job scraper
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseJobScraper, JobData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging

logger = logging.getLogger(__name__)

class GoogleScraper(BaseJobScraper):
    """Google job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Google",
            base_url="https://careers.google.com/jobs/results/?location=India",
            headless=headless
        )
    
    def extract_job_data(self, element, index: int) -> JobData:
        """Extract job data from a job element"""
        try:
            # Extract job title
            title = ""
            try:
                title_element = element.find_element(By.TAG_NAME, "h3")
                title = title_element.text.strip()
            except NoSuchElementException:
                # Try alternative selectors
                try:
                    title_element = element.find_element(By.TAG_NAME, "a")
                    title = title_element.text.strip()
                except NoSuchElementException:
                    pass
            
            # Extract location
            location = "India"
            try:
                lines = element.text.split('\n')
                for line in lines:
                    if any(city in line for city in ["Bangalore", "Gurugram", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai", "Kolkata"]):
                        location = line.strip()
                        break
            except:
                pass
            
            # Try to get job link
            job_link = ""
            try:
                link_element = element.find_element(By.TAG_NAME, "a")
                job_link = link_element.get_attribute("href")
            except NoSuchElementException:
                pass
            
            # Get job description and experience from the job page
            job_description = "Job description available on company website"
            experience_required = "Not specified"
            
            if job_link:
                job_description = self.get_job_description(job_link)
                experience_required = self.get_experience_required(job_link)
            
            return JobData(
                title=title,
                location=location,
                experience_required=experience_required,
                job_description=job_description,
                job_link=job_link,
                posted_date="Not specified",
                company=self.company_name
            )
            
        except Exception as e:
            logger.warning(f"Error extracting job data: {str(e)}")
            return None
    
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Google jobs with proper pagination"""
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (max {max_pages} pages)...")
        
        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=8)
            
            # Track unique jobs to avoid duplicates
            seen_jobs = set()
            
            for page_num in range(max_pages):
                logger.info(f"📄 Scraping page {page_num + 1} of {max_pages}")
                
                # Wait for page to load after pagination
                if page_num > 0:
                    time.sleep(3)
                    # Scroll to top to ensure we see all job elements
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(2)
                
                # Find job elements with multiple selectors
                job_selectors = [
                    "li",
                    "div[class*='job']",
                    "div[class*='result']",
                    "article",
                    "[data-testid*='job']"
                ]
                
                job_elements = []
                for selector in job_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        job_elements = elements
                        logger.info(f"🔍 Found {len(job_elements)} potential job elements on page {page_num + 1} using selector: {selector}")
                        break
                
                if not job_elements:
                    logger.warning(f"No job elements found on page {page_num + 1}")
                    continue
                
                real_jobs_found_on_page = 0
                
                for i, element in enumerate(job_elements):
                    try:
                        text_content = element.text.strip()
                        
                        # Skip empty elements
                        if not text_content or len(text_content) < 10:
                            continue
                        
                        # Debug: Log some elements on page 2
                        if page_num > 0 and i < 5:
                            logger.info(f"Page {page_num + 1} element {i}: {text_content[:100]}...")
                        
                        # Look for real job content (contains company name and location)
                        if "Google" in text_content and ("India" in text_content or "Bangalore" in text_content or "Gurugram" in text_content or "Hyderabad" in text_content):
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
                                else:
                                    logger.info(f"🔄 Duplicate job found: {job_data.title}")
                                    
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
    
    def get_job_description(self, job_url: str) -> str:
        """Get job description from individual job page"""
        try:
            # Store the main window handle
            main_window = self.driver.current_window_handle
            
            # Open job page in new tab
            self.driver.execute_script("window.open('');")
            
            # Wait a moment for the new tab to open
            time.sleep(1)
            
            # Get all window handles
            all_windows = self.driver.window_handles
            
            # Switch to the new tab (should be the last one)
            if len(all_windows) > 1:
                self.driver.switch_to.window(all_windows[-1])
                self.driver.get(job_url)
            else:
                # Fallback: navigate in the same tab
                self.driver.get(job_url)
            
            # Wait for job content to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.KwJkGe'))
                )
                
                job_description_parts = []
                
                # Extract content from div.KwJkGe
                try:
                    kwjge_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.KwJkGe')
                    for div in kwjge_divs:
                        text = div.text.strip()
                        if text:
                            job_description_parts.append(text)
                except NoSuchElementException:
                    pass
                
                # Extract content from div.aG5W3
                try:
                    ag5w3_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.aG5W3')
                    for div in ag5w3_divs:
                        text = div.text.strip()
                        if text:
                            job_description_parts.append(text)
                except NoSuchElementException:
                    pass
                
                # Extract content from div.BDNOWe
                try:
                    bdnowe_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.BDNOWe')
                    for div in bdnowe_divs:
                        text = div.text.strip()
                        if text:
                            job_description_parts.append(text)
                except NoSuchElementException:
                    pass
                
                # Close the current tab and switch back to main window
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    # If we're in the same tab, go back
                    self.driver.back()
                
                job_description = '\n\n'.join(job_description_parts)
                return job_description if job_description else "Job description available on company website"
                
            except TimeoutException:
                logger.warning(f"Could not load job details for {job_url}")
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    self.driver.back()
                return "Job description available on company website"
                
        except Exception as e:
            logger.warning(f"Error getting job description: {str(e)}")
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    self.driver.back()
            except:
                pass
            return "Job description available on company website"
    
    def get_experience_required(self, job_url: str) -> str:
        """Get experience required from individual job page"""
        try:
            # Store the main window handle
            main_window = self.driver.current_window_handle
            
            # Open job page in new tab
            self.driver.execute_script("window.open('');")
            
            # Wait a moment for the new tab to open
            time.sleep(1)
            
            # Get all window handles
            all_windows = self.driver.window_handles
            
            # Switch to the new tab (should be the last one)
            if len(all_windows) > 1:
                self.driver.switch_to.window(all_windows[-1])
                self.driver.get(job_url)
            else:
                # Fallback: navigate in the same tab
                self.driver.get(job_url)
            
            # Wait for job content to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.wVSTAb'))
                )
                
                # Extract experience from span.wVSTAb
                try:
                    experience_spans = self.driver.find_elements(By.CSS_SELECTOR, 'span.wVSTAb')
                    for span in experience_spans:
                        text = span.text.strip()
                        if text:
                            # Log what we found for debugging
                            logger.info(f"Found experience span: '{text}'")
                            # Close the current tab and switch back to main window
                            if len(self.driver.window_handles) > 1:
                                self.driver.close()
                                self.driver.switch_to.window(main_window)
                            else:
                                self.driver.back()
                            return text
                except NoSuchElementException:
                    pass
                
                # Close the current tab and switch back to main window
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    self.driver.back()
                
                return "Not specified"
                
            except TimeoutException:
                logger.warning(f"Could not load job details for {job_url}")
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    self.driver.back()
                return "Not specified"
                
        except Exception as e:
            logger.warning(f"Error getting experience required: {str(e)}")
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    self.driver.back()
            except:
                pass
            return "Not specified"
    
    def find_next_page_button(self) -> bool:
        """Find and click next page button for Google using aria-label"""
        try:
            # Wait for the page to fully load
            time.sleep(2)
            
            # Look for the next page button using aria-label
            next_selectors = [
                'a[aria-label="Go to next page"]',
                'button[aria-label="Go to next page"]',
                '[aria-label="Go to next page"]',
                'a[aria-label*="next page"]',
                'button[aria-label*="next page"]'
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
                logger.warning("Could not find next page button with aria-label selector")
                return False
                
        except Exception as e:
            logger.warning(f"Error clicking next page button: {str(e)}")
            return False

if __name__ == "__main__":
    scraper = GoogleScraper(headless=False)
    jobs = scraper.scrape_jobs(max_pages=2)
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from Google")
