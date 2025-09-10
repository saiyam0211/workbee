"""
Tesla job scraper (Selenium)
"""
import os
import sys
import time
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseJobScraper, JobData  # noqa: E402

logger = logging.getLogger(__name__)


class TeslaScraper(BaseJobScraper):
    """Tesla job scraper"""

    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Tesla",
            base_url="https://hire-r1.mokahr.com/social-recruitment/tesla/100004142#/jobs?page=1&anchorName=jobsList",
            headless=headless,
        )

    def scrape_jobs(self, max_pages: int = 1) -> List[JobData]:
        logger.info(f"🚀 Starting to scrape {self.company_name} jobs (max {max_pages} pages)...")

        try:
            self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=8)

            seen_jobs = set()
            current_page = 1

            while current_page <= max_pages:
                logger.info(f"📄 Scraping page {current_page} of {max_pages}")

                cards = self._find_job_cards()
                logger.info(f"🔍 Found {len(cards)} job cards")

                for index in range(len(cards)):
                    try:
                        cards = self._find_job_cards()
                        if index >= len(cards):
                            break
                        card = cards[index]

                        title, link = self._extract_title_and_link(card)
                        if not title or not link:
                            continue

                        key = f"{title}_{link}"
                        if key in seen_jobs:
                            continue

                        location = self._extract_location(card)
                        jd_text, posted_date = self._extract_details_from_job_page(link)

                        job = JobData(
                            title=title,
                            location=location or "Not specified",
                            experience_required=None,
                            job_description=jd_text or "Not specified",
                            job_link=link,
                            posted_date=posted_date or "Not specified",
                            company=self.company_name,
                        )

                        self.jobs_data.append(job)
                        seen_jobs.add(key)
                        logger.info(f"✅ {title}")

                    except StaleElementReferenceException:
                        continue
                    except Exception as e:
                        logger.warning(f"Error on card {index}: {e}")
                        continue

                if current_page >= max_pages:
                    break

                moved = self._go_to_next_page()
                if not moved:
                    logger.info("🔚 No next page detected; stopping")
                    break
                current_page += 1
                self.wait_for_page_load(3)

            logger.info(
                f"🎉 Scraped {len(self.jobs_data)} unique jobs from {self.company_name} across {min(current_page, max_pages)} pages"
            )
            return self.jobs_data

        except Exception as e:
            logger.error(f"❌ Error during scraping {self.company_name}: {e}")
            return []
        finally:
            self.close_driver()

    def _find_job_cards(self):
        selectors = [
            "a.link-txmgVOCVz9[href]",
            "a[href][class*='link-']",
        ]
        for sel in selectors:
            els = self.driver.find_elements(By.CSS_SELECTOR, sel)
            if els:
                return els
        return []

    def _extract_title_and_link(self, card):
        try:
            href = card.get_attribute("href") or ""
            title = ""
            try:
                title = card.find_element(By.CSS_SELECTOR, "span.title-u2qk9xX9Ie.target-color-container").text.strip()
            except NoSuchElementException:
                pass
            if not title:
                title = card.text.strip()
            return (title if title else None), (href if href else None)
        except Exception:
            return None, None

    def _extract_location(self, card):
        try:
            el = card.find_element(By.CSS_SELECTOR, "div.sd-foundation-body-primary-b0MG4.mgt8-sGRgM9Em3e.ellipsis-s4h2VX0z8O")
            txt = el.text.strip()
            if txt:
                return txt
        except Exception:
            pass
        return "Not specified"

    def _extract_details_from_job_page(self, link):
        original = self.driver.current_url
        jd_text = posted = None
        try:
            self.driver.execute_script("window.open(arguments[0], '_blank');", link)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-Yu939rjoGi"))
            )
            time.sleep(0.5)

            try:
                jd = self.driver.find_element(By.CSS_SELECTOR, "div.list-Yu939rjoGi")
                jd_text = jd.text.strip()
            except Exception:
                jd_text = None

            for sel in ["time", "[data-testid='posting-date']", "span[class*='date']"]:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, sel)
                    txt = el.text.strip()
                    if txt:
                        posted = txt
                        break
                except Exception:
                    continue

        except Exception as e:
            logger.warning(f"Failed to extract job details: {e}")
        finally:
            try:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                if self.driver.current_url != original:
                    self.driver.get(original)
            except Exception:
                pass
        return jd_text, posted

    def _go_to_next_page(self) -> bool:
        # Click the forward pagination button
        selectors = [
            "button.sd-Pagination-item-1cqBB.sd-Pagination-forward-3z80f",
            ".sd-Pagination-forward-3z80f",
        ]
        for sel in selectors:
            try:
                btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )
                self.driver.execute_script("arguments[0].click();", btn)
                return True
            except Exception:
                continue
        return False


if __name__ == "__main__":
    scraper = TeslaScraper(headless=True)
    data = scraper.scrape_jobs(max_pages=1)
    scraper.save_to_json()
    print(f"Scraped {len(data)} jobs from Tesla")
