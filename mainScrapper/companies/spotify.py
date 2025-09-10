"""
Spotify job scraper
"""
import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseJobScraper, JobData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

class SpotifyScraper(BaseJobScraper):
    """Spotify job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Spotify",
            base_url="https://www.lifeatspotify.com/jobs?location=India",
            headless=headless
        )
    
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Spotify jobs with load-more pagination as instructed"""
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (chunks {max_pages})...")
        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=10)
            seen: set[str] = set()
            processed = 0
            for chunk in range(max_pages):
                # keep loading more until no changes or we reached chunk target
                prev_count = -1
                cards = self.driver.find_elements("css selector", "div.entry_container__eT9IU")
                while True:
                    if len(cards) == prev_count:
                        break
                    prev_count = len(cards)
                    try:
                        load_more = self.driver.find_element("css selector", "button[aria-label='Load more jobs']")
                        if load_more.is_enabled():
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more)
                            time.sleep(0.2)
                            self.driver.execute_script("arguments[0].click();", load_more)
                            WebDriverWait(self.driver, 8).until(
                                lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.entry_container__eT9IU")) > prev_count
                            )
                            cards = self.driver.find_elements("css selector", "div.entry_container__eT9IU")
                        else:
                            break
                    except Exception:
                        break

                logger.info(f"🔍 Found {len(cards)} job cards (processed {processed})")
                for idx in range(processed, len(cards)):
                    try:
                        cards = self.driver.find_elements("css selector", "div.entry_container__eT9IU")
                        if idx >= len(cards):
                            break
                        card = cards[idx]
                        # title
                        title_el = card.find_element("css selector", "h2.entry_title__Q0z3u")
                        title = title_el.text.strip()
                        # location (prefer desktop-visible, fallback to mobile container)
                        location = ""
                        try:
                            # desktop version
                            loc_span = card.find_element("css selector", "p.detail-3.color-black.is-hidden-mobile span")
                            location = loc_span.text.strip()
                        except Exception:
                            try:
                                # mobile version path
                                loc_span = card.find_element("css selector", "div.entry_locationCommitment__6yJo8 p span")
                                location = loc_span.text.strip()
                            except Exception:
                                location = ""
                        # build job link from card slug and open in new tab
                        slug = card.get_attribute("data-info") or ""
                        job_link = f"https://www.lifeatspotify.com/jobs/{slug}" if slug else ""
                        if job_link:
                            self.driver.execute_script("window.open(arguments[0], '_blank');", job_link)
                            self.driver.switch_to.window(self.driver.window_handles[-1])
                        else:
                            # fallback: click card and use current URL
                            self.driver.execute_script("arguments[0].click();", card)
                            time.sleep(1.5)
                            job_link = self.driver.current_url
                        # JD
                        jd = ""
                        try:
                            jd_el = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div.singlejob_right__z4gG5"))
                            )
                            jd = jd_el.text.strip()
                        except Exception:
                            jd = ""
                        job_key = f"{title}_{job_link}"
                        if title and job_link and job_key not in seen:
                            self.jobs_data.append(JobData(
                                title=title,
                                location=location,
                                experience_required="",
                                job_description=jd,
                                job_link=job_link,
                                posted_date="",
                                company=self.company_name,
                            ))
                            seen.add(job_key)
                            logger.info(f"✅ Scraped: {title}")
                    except Exception as e:
                        logger.debug(f"skip card {idx}: {e}")
                    finally:
                        # go back to list
                        try:
                            if len(self.driver.window_handles) > 1 and self.driver.current_url == job_link:
                                self.driver.close()
                                self.driver.switch_to.window(self.driver.window_handles[0])
                            else:
                                self.driver.back()
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.entry_container__eT9IU"))
                            )
                        except Exception:
                            try:
                                self.navigate_to_page(self.base_url, wait_time=5)
                            except Exception:
                                pass
                processed = len(self.driver.find_elements("css selector", "div.entry_container__eT9IU"))
            logger.info(f"🎉 Successfully scraped {len(self.jobs_data)} UNIQUE jobs from {self.company_name}")
            return self.jobs_data
        except Exception as e:
            logger.error(f"❌ Error during scraping: {str(e)}")
            return []
        finally:
            self.close_driver()
    
    def find_next_page_button(self) -> bool:
        """Unused for Spotify; load-more handled in scrape_jobs"""
        return False
if __name__ == "__main__":
    scraper = SpotifyScraper(headless=True)
    jobs = scraper.scrape_jobs()
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from Spotify")
