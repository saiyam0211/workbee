import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from base_scraper import BaseJobScraper, JobData

class MicrosoftScraper(BaseJobScraper):
    def __init__(self, headless=True):
        super().__init__(
            company_name="MICROSOFT",
            base_url="https://jobs.careers.microsoft.com/global/en/search?l=en_us&pg=1&pgSz=20&o=Relevance&flt=true&ref=cms",
            headless=headless
        )
        self.seen_jobs = set()

    def scrape_jobs(self, max_pages=1):
        """Scrape jobs from Microsoft career page"""
        try:
            print(f"Starting to scrape {self.company_name} jobs...")
            self.setup_driver()
            self.driver.get(self.base_url)
            print("Page loaded, waiting for page load...")
            self.wait_for_page_load()
            print("Page load complete")
            
            # Wait a bit more for dynamic content to load
            time.sleep(5)
            
            # Scroll to trigger any lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # ensure internal storage is used for saving later
            self.jobs_data = []
            
            for page in range(1, max_pages + 1):
                print(f"Scraping page {page}...")
                
                # Wait for job list to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.ms-List-page"))
                    )
                except TimeoutException:
                    print(f"Timeout waiting for job list on page {page}")
                    # Let's see what elements are actually on the page
                    print("Page title:", self.driver.title)
                    print("Current URL:", self.driver.current_url)
                    # Try to find any div elements that might contain jobs
                    all_divs = self.driver.find_elements(By.TAG_NAME, "div")
                    print(f"Found {len(all_divs)} div elements on page")
                    # Look for divs with classes that might contain "ms-List"
                    ms_divs = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='ms-List']")
                    print(f"Found {len(ms_divs)} divs with 'ms-List' in class")
                    for i, div in enumerate(ms_divs[:5]):  # Show first 5
                        print(f"  Div {i}: class='{div.get_attribute('class')}'")
                    
                    # Try to find other common job-related selectors
                    job_selectors = [
                        "div[class*='job']",
                        "div[class*='result']",
                        "div[class*='listing']",
                        "div[class*='card']",
                        "li[class*='job']",
                        "article[class*='job']",
                        "[data-testid*='job']",
                        "[data-automation*='job']"
                    ]
                    
                    for selector in job_selectors:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            print(f"Found {len(elements)} elements with selector: {selector}")
                            for i, elem in enumerate(elements[:3]):  # Show first 3
                                print(f"  Element {i}: class='{elem.get_attribute('class')}', text='{elem.text[:100]}...'")
                    
                    # Check for search forms or input fields
                    search_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='search'], input[placeholder*='search'], input[placeholder*='job']")
                    print(f"Found {len(search_inputs)} search input fields")
                    
                    # Check for buttons
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, "button, input[type='submit'], input[type='button']")
                    print(f"Found {len(buttons)} buttons")
                    for i, btn in enumerate(buttons[:5]):  # Show first 5
                        print(f"  Button {i}: text='{btn.text}', class='{btn.get_attribute('class')}'")
                    
                    # Check if we need to perform a search first
                    if search_inputs:
                        print("Found search inputs, trying to perform a search...")
                        try:
                            search_input = search_inputs[0]
                            search_input.clear()
                            search_input.send_keys("software engineer")  # Try a common job search term
                            
                            # Look for search button
                            search_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], button:contains('Search'), button:contains('Find')")
                            if search_buttons:
                                search_buttons[0].click()
                                time.sleep(5)  # Wait for search results
                                print("Performed search, checking for results...")
                            else:
                                # Try pressing Enter
                                from selenium.webdriver.common.keys import Keys
                                search_input.send_keys(Keys.RETURN)
                                time.sleep(5)
                                print("Pressed Enter, checking for results...")
                        except Exception as e:
                            print(f"Error performing search: {e}")
                    
                    continue
                
                # Find job cards (first pass)
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.ms-List-page div.ms-List-cell")
                print(f"Found {len(job_cards)} job cards on page {page}")
                
                if not job_cards:
                    print(f"No job cards found on page {page}")
                    continue
                
                print(f"Processing {len(job_cards)} job cards...")
                total_cards = len(job_cards)
                for idx in range(total_cards):
                    try:
                        # re-query list each iteration to avoid stale references
                        current_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.ms-List-page div.ms-List-cell")
                        if idx >= len(current_cards):
                            break
                        card = current_cards[idx]
                        job_data = self.extract_job_data(card)
                        if job_data and isinstance(job_data, JobData) and getattr(job_data, 'title', None):
                            # dedupe on title+location
                            job_key = f"{job_data.title}__{getattr(job_data,'location','')}"
                            if job_key not in self.seen_jobs:
                                self.seen_jobs.add(job_key)
                                self.jobs_data.append(job_data)
                                print(f"Scraped: {job_data.title}")
                        # after returning from details, wait for the job list to be visible again
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ms-List-page"))
                        )
                    except Exception as e:
                        print(f"Error extracting job data: {e}")
                        continue
                
                # Go to next page if not the last page
                if page < max_pages:
                    if not self.find_next_page_button():
                        print(f"No next page button found on page {page}")
                        break
                    
                    time.sleep(2)  # Wait for page to load
            
            print(f"Scraped {len(self.jobs_data)} jobs from {self.company_name}")
            return self.jobs_data
            
        except Exception as e:
            print(f"Error scraping {self.company_name}: {e}")
            return []

    def extract_job_data(self, job_card):
        """Extract job data from a job card"""
        try:
            print("Extracting job data from card...")
            # Job title
            title_element = job_card.find_element(By.CSS_SELECTOR, "h2.MZGzlrn8gfgSs8TZHhv2")
            title = title_element.text.strip() if title_element else ""
            print(f"Found title: {title}")
            
            if not title:
                print("No title found, returning None")
                return None
            
            # Location - robust: pick span next to POI icon
            location = ""
            try:
                location_span = job_card.find_element(By.XPATH, ".//i[@data-icon-name='POI' or @aria-label='job location icon']/following-sibling::span[1]")
                location = location_span.text.strip()
            except NoSuchElementException:
                try:
                    # fallback: any span within a container having POI icon
                    location_div = job_card.find_element(By.XPATH, ".//div[.//i[@data-icon-name='POI' or @aria-label='job location icon']]")
                    location_span = location_div.find_element(By.TAG_NAME, "span")
                    location = location_span.text.strip() if location_span else ""
                except Exception:
                    location = ""
            
            # Job link - click "See details" button to open job details
            job_link = ""
            try:
                # Dynamic class suffix, use prefix match and fallbacks
                see_more_button = None
                see_more_selectors = [
                    "button.ms-Link[class^='seeDetailsLink-']",
                    "button.ms-Link.seeDetailsLink",
                    "button[aria-label^='click to see details']",
                ]
                for sel in see_more_selectors:
                    try:
                        see_more_button = job_card.find_element(By.CSS_SELECTOR, sel)
                        if see_more_button:
                            break
                    except Exception:
                        continue
                if not see_more_button:
                    raise NoSuchElementException("See details button not found")
                # Click the button to open job details
                self.driver.execute_script("arguments[0].click();", see_more_button)
                # wait for details region to render
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'ms-Stack') and .//span[@aria-label='job description'] or .//div[contains(@class,'fcUffX')]]"))
                    )
                except Exception:
                    time.sleep(2)
                
                # Capture current URL as job link
                job_link = self.driver.current_url
                
                # Get job posted date from the job details page
                posted_date = self.get_job_posted_date()
                
                # Get job description
                job_description = self.get_job_description()
                
                # Go back to main page
                self.go_back_to_main_page()
                
            except NoSuchElementException:
                print("Could not find 'see more' button")
                return None
            
            return JobData(
                title=title,
                location=location,
                experience_required="",
                job_description=job_description,
                job_link=job_link,
                posted_date=posted_date,
                company=self.company_name
            )
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None

    def get_job_posted_date(self):
        """Get job posted date from job details page"""
        try:
            # Prefer explicit label search then sibling value
            try:
                label = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='Date posted']"))
                )
                value = label.find_element(By.XPATH, "following-sibling::div[1]")
                return value.text.strip()
            except Exception:
                pass

            # Fallback: style-based container as provided
            date_elements = self.driver.find_elements(By.XPATH, "//div[contains(@style, 'width: 64%;') and contains(@style, 'font-weight: 600')]")
            for element in date_elements:
                try:
                    parent = element.find_element(By.XPATH, "./..")
                    if "Date posted" in parent.text:
                        return element.text.strip()
                except Exception:
                    continue
            return ""
        except Exception as e:
            print(f"Error getting job posted date: {e}")
            return ""

    def get_job_description(self):
        """Get job description from job details page"""
        try:
            # Look for job description in div with class "fcUffXZZoGt8CJQd8GUl" (dynamic but stable here)
            try:
                description_element = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.fcUffXZZoGt8CJQd8GUl"))
                )
                return description_element.text.strip()
            except TimeoutException:
                # Fallback: try aria-label or generic container
                try:
                    description_element = self.driver.find_element(By.XPATH, "//div[@aria-label='job description' or contains(translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'description')]")
                    return description_element.text.strip()
                except Exception:
                    return ""
        except NoSuchElementException:
            print("Could not find job description element")
            return ""
        except Exception as e:
            print(f"Error getting job description: {e}")
            return ""

    def go_back_to_main_page(self):
        """Go back to main page from job details"""
        try:
            # Click the back button: dynamic class suffix, prefer aria-label
            back_button = None
            back_selectors = [
                "span.ms-Button-flexContainer[class^='flexContainer-']",
                "button[aria-label='Back']",
                "span[aria-label='Back']",
            ]
            for sel in back_selectors:
                try:
                    back_button = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if back_button:
                        break
                except Exception:
                    continue
            if back_button:
                self.driver.execute_script("arguments[0].click();", back_button)
            else:
                # As last resort, browser back
                self.driver.execute_script("window.history.back();")
            # wait for list view again
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.ms-List-page"))
                )
            except Exception:
                time.sleep(2)
        except NoSuchElementException:
            print("Could not find back button")
        except Exception as e:
            print(f"Error going back to main page: {e}")

    def find_next_page_button(self):
        """Find and click next page button"""
        try:
            # Scroll down to load more content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Look for button with aria-label="Go to next page"
            next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Go to next page']")
            
            if next_button.is_enabled():
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)  # Wait for page to load
                return True
            else:
                print("Next page button is disabled")
                return False
                
        except NoSuchElementException:
            print("Could not find next page button")
            return False
        except Exception as e:
            print(f"Error clicking next page button: {e}")
            return False