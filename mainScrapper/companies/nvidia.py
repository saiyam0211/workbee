"""
NVIDIA job scraper
"""
import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseJobScraper, JobData
import logging

logger = logging.getLogger(__name__)

class NvidiaScraper(BaseJobScraper):
    """NVIDIA job scraper"""
    
    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="NVIDIA",
            base_url="https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
            headless=headless
        )
    
    def scrape_jobs(self, max_pages: int = 1) -> list[JobData]:
        """Scrape Nvidia jobs with pagination using provided selectors"""
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (max {max_pages} pages)...")
        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=10)
            seen_jobs: set[str] = set()
            for page_num in range(max_pages):
                logger.info(f"📄 Scraping page {page_num + 1} of {max_pages}")
                # Wait for job list
                time.sleep(2)
                job_items = self.driver.find_elements("css selector", "li.css-1q2dra3")
                logger.info(f"🔍 Found {len(job_items)} job cards")
                for idx in range(len(job_items)):
                    try:
                        cards = self.driver.find_elements("css selector", "li.css-1q2dra3")
                        if idx >= len(cards):
                            break
                        card = cards[idx]
                        # title and link
                        link_el = card.find_element("css selector", "h3 a.css-19uc56f")
                        title = link_el.text.strip()
                        href = link_el.get_attribute("href")
                        if not title or not href:
                            continue
                        if href.startswith("/"):
                            href = self.base_url.rstrip("/") + href
                        job_key = f"{title}_{href}"
                        if job_key in seen_jobs:
                            continue
                        # open in new tab
                        self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(2)
                        # location: dd values under div[data-automation-id='locations']
                        location = ""
                        try:
                            dd_nodes = self.driver.find_elements("css selector", "div[data-automation-id='locations'] dd.css-129m7dg")
                            if dd_nodes:
                                location = ", ".join([d.text.strip() for d in dd_nodes if d.text.strip()])
                        except Exception:
                            location = ""
                        # job description
                        job_description = ""
                        try:
                            jd_el = self.driver.find_element("css selector", "div[data-automation-id='jobPostingDescription']")
                            job_description = jd_el.text.strip()
                        except Exception:
                            job_description = ""
                        posted_date = ""
                        # build data
                        job = JobData(
                            title=title,
                            location=location,
                            experience_required="",
                            job_description=job_description,
                            job_link=href,
                            posted_date=posted_date,
                            company=self.company_name,
                        )
                        self.jobs_data.append(job)
                        seen_jobs.add(job_key)
                        logger.info(f"✅ Scraped: {title}")
                    except Exception as e:
                        logger.debug(f"skip card {idx}: {e}")
                    finally:
                        # close tab if opened
                        if len(self.driver.window_handles) > 1:
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                            time.sleep(1)
                # pagination
                if page_num < max_pages - 1:
                    if not self.find_next_page_button():
                        logger.info("🔚 No more pages available, stopping pagination")
                        break
                    self.wait_for_page_load(2)
            logger.info(f"🎉 Successfully scraped {len(self.jobs_data)} UNIQUE jobs from {self.company_name} across {max_pages} pages")
            return self.jobs_data
        except Exception as e:
            logger.error(f"❌ Error during scraping: {str(e)}")
            return []
        finally:
            self.close_driver()
    
    def find_next_page_button(self) -> bool:
        """Find and click next page button for Nvidia"""
        try:
            # Primary selector provided by you
            try:
                btn = self.driver.find_element("css selector", "button[data-uxi-widget-type='stepToNextButton']")
                if btn.is_enabled():
                    self.driver.execute_script("arguments[0].click();", btn)
                    logger.info("✅ Clicked next page button")
                    return True
            except Exception:
                pass
            # fallbacks
            for sel in ["button[aria-label='Next']", "a[aria-label='Next']"]:
                try:
                    b = self.driver.find_element("css selector", sel)
                    if b.is_enabled():
                        self.driver.execute_script("arguments[0].click();", b)
                        return True
                except Exception:
                    continue
            return False
        except Exception as e:
            logger.warning(f"⚠️ Could not find next page button: {str(e)}")
            return False
if __name__ == "__main__":
    scraper = NvidiaScraper(headless=True)
    jobs = scraper.scrape_jobs()
    scraper.save_to_json()
    print(f"Scraped {len(jobs)} jobs from NVIDIA")
