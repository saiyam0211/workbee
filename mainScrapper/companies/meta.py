"""
Meta job scraper
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

class MetaScraper(BaseJobScraper):
    """Meta job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Meta",
            base_url="https://www.metacareers.com/jobs/?q=&location=India",
            headless=headless
        )
    
    def extract_job_data(self, element, index: int) -> JobData:
        """Extract job data from a job element"""
        try:
            # Extract job title from div._6g3g.x10lme4x.x26uert.xngnso2.x117nqv4.x1mnlqng.x1e096f4
            title = ""
            try:
                title_element = element.find_element(By.CSS_SELECTOR, 'div._6g3g.x10lme4x.x26uert.xngnso2.x117nqv4.x1mnlqng.x1e096f4')
                title = title_element.text.strip()
            except NoSuchElementException:
                # Try alternative selectors
                try:
                    title_element = element.find_element(By.CSS_SELECTOR, 'div[class*="_6g3g"]')
                    title = title_element.text.strip()
                except NoSuchElementException:
                    # Try to get title from any div with substantial text content
                    try:
                        all_divs = element.find_elements(By.CSS_SELECTOR, 'div')
                        for div in all_divs:
                            div_text = div.text.strip()
                            if div_text and len(div_text) > 5 and len(div_text) < 100:
                                # Check if this looks like a job title
                                if not any(keyword in div_text.lower() for keyword in ["share", "apply", "filter", "sort", "search", "menu", "next", "previous", "chevron", "button"]):
                                    title = div_text
                                    break
                    except:
                        pass
            
            # Extract job link from the anchor tag
            job_link = ""
            try:
                job_link = element.get_attribute('href')
                if job_link and not job_link.startswith('http'):
                    job_link = 'https://www.metacareers.com' + job_link
                
                # Skip if this is not a job link (e.g., pagination links)
                if job_link and ('/jobs/' not in job_link or 'page=' in job_link):
                    return None
                    
            except:
                pass
            
            # Get job description and location from the job page
            job_description = "Job description available on company website"
            location = "India"
            
            if job_link:
                job_description = self.get_job_description(job_link)
                location = self.get_job_location(job_link)
            
            return JobData(
                title=title,
                location=location,
                experience_required="Not specified",
                job_description=job_description,
                job_link=job_link,
                posted_date="Not specified",
                company=self.company_name
            )
            
        except Exception as e:
            logger.warning(f"Error extracting job data: {str(e)}")
            return None
    
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
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div._8muv._ar_h'))
                )
                
                # Extract job description from div._8muv._ar_h
                try:
                    description_div = self.driver.find_element(By.CSS_SELECTOR, 'div._8muv._ar_h')
                    job_description = description_div.text.strip()
                    
                    # Close the current tab and switch back to main window
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(main_window)
                    else:
                        self.driver.back()
                    
                    return job_description if job_description else "Job description available on company website"
                    
                except NoSuchElementException:
                    # Close the current tab and switch back to main window
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(main_window)
                    else:
                        self.driver.back()
                    return "Job description available on company website"
                
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
    
    def get_job_location(self, job_url: str) -> str:
        """Get job location from individual job page"""
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
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div._91s1._armu'))
                )
                
                # Extract location from span._8lfp._9a80._careersV2RefreshJobDetailPage__location2024
                try:
                    location_div = self.driver.find_element(By.CSS_SELECTOR, 'div._91s1._armu')
                    location_span = location_div.find_element(By.CSS_SELECTOR, 'span._8lfp._9a80._careersV2RefreshJobDetailPage__location2024')
                    # Get the text content but exclude nested spans
                    location_text = location_span.text.strip()
                    
                    # Close the current tab and switch back to main window
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(main_window)
                    else:
                        self.driver.back()
                    
                    return location_text if location_text else "India"
                    
                except NoSuchElementException:
                    # Close the current tab and switch back to main window
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(main_window)
                    else:
                        self.driver.back()
                    return "India"
                
            except TimeoutException:
                logger.warning(f"Could not load job details for {job_url}")
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    self.driver.back()
                return "India"
                
        except Exception as e:
            logger.warning(f"Error getting job location: {str(e)}")
            try:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                else:
                    self.driver.back()
            except:
                pass
            return "India"
    
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Meta jobs with proper pagination"""
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (max {max_pages} pages)...")
        
        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=10)
            
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
                
                # Find job elements using the correct selector
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.x1ypdohk.x1lku1pv')
                logger.info(f"🔍 Found {len(job_elements)} potential job elements on page {page_num + 1}")
                
                if not job_elements:
                    logger.warning(f"No job elements found on page {page_num + 1}")
                    continue
                
                real_jobs_found_on_page = 0
                
                for i, element in enumerate(job_elements):
                    try:
                        text_content = element.text.strip()
                        
                        # Skip empty elements
                        if not text_content or len(text_content) < 5:
                            continue
                        
                        # Skip elements that are clearly not job listings
                        skip_keywords = ["share", "learn more", "apply", "filter", "sort", "search", "menu", "navigation", "next", "previous", "chevron", "button"]
                        if any(keyword in text_content.lower() for keyword in skip_keywords):
                            continue
                        
                        # Extract job data for all elements that have substantial content
                        job_data = self.extract_job_data(element, i)
                        if job_data and job_data.title and len(job_data.title) > 3:
                            # Check for duplicates using job title and link
                            job_key = f"{job_data.title}_{job_data.job_link}"
                            if job_key not in seen_jobs:
                                self.jobs_data.append(job_data)
                                seen_jobs.add(job_key)
                                real_jobs_found_on_page += 1
                                logger.info(f"✅ Scraped: {job_data.title}")
                                
                                # Limit per page to avoid too many results
                                if real_jobs_found_on_page >= 20:
                                    break
                                
                    except Exception as e:
                        logger.debug(f"Error processing element {i}: {str(e)}")
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
        """Find and click next page button for Meta using the specific selector"""
        try:
            # Wait for the page to fully load
            time.sleep(2)
            
            # Look for the next page button using the specific class selector
            next_selectors = [
                'a.x5y1uuc.x1lku1pv.x6s0dn4.x11g6tue.x972fbf.x10w94by.x1qhh985.x14e42zd.xbsr9hj.x1ypdohk.x78zum5.xtqikln.x1hl2dhg',
                'a[class*="x5y1uuc"][class*="x1lku1pv"]',
                'a[class*="x5y1uuc"]',
                'a[class*="x1lku1pv"]'
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
    scraper = MetaScraper(headless=True)
    jobs = scraper.scrape_jobs()
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from Meta")
