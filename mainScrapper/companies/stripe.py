"""
Stripe job scraper (Selenium)
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


class StripeScraper(BaseJobScraper):
    """Stripe job scraper"""

    def __init__(self, headless: bool = True):
        super().__init__(
            company_name="Stripe",
            base_url="https://stripe.com/jobs/search?l=india",
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

                # Wait for listing container
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "main, div[data-testid='jobs-results'], ul, section[role='main']",
                            )
                        )
                    )
                except TimeoutException:
                    logger.warning("Timeout waiting for listings container; continuing")

                job_cards = self._find_job_cards()
                logger.info(f"🔍 Found {len(job_cards)} job cards")

                for index in range(len(job_cards)):
                    try:
                        # Re-find to avoid stale element
                        job_cards = self._find_job_cards()
                        if index >= len(job_cards):
                            break
                        card = job_cards[index]

                        title, link = self._extract_title_and_link(card)
                        if not title or not link:
                            continue

                        job_key = f"{title}_{link}"
                        if job_key in seen_jobs:
                            continue

                        location = self._extract_location(card)

                        jd_text, posted_date, experience = self._extract_details_from_job_page(link)

                        job = JobData(
                            title=title,
                            location=location or "Not specified",
                            experience_required=experience,
                            job_description=jd_text or "Not specified",
                            job_link=link,
                            posted_date=posted_date or "Not specified",
                            company=self.company_name,
                        )

                        self.jobs_data.append(job)
                        seen_jobs.add(job_key)
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
            "[data-component='JobsListings'] a.JobsListings__link",
            "section[id*='jobs'] a.JobsListings__link",
            "a.JobsListings__link",
            "[data-component='JobsListings'] a[href*='/jobs/positions/']",
        ]
        for sel in selectors:
            cards = self.driver.find_elements(By.CSS_SELECTOR, sel)
            if cards:
                return cards
        return []

    def _extract_title_and_link(self, card):
        try:
            link_el = card
            if card.tag_name.lower() != "a":
                try:
                    link_el = card.find_element(By.CSS_SELECTOR, "a[href]")
                except NoSuchElementException:
                    return None, None
            href = link_el.get_attribute("href") or ""
            title = link_el.text.strip()
            if not title:
                # Try nested heading
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h3, h2").text.strip()
                except NoSuchElementException:
                    title = None
            # Normalize relative urls
            if href.startswith("/"):
                href = f"https://stripe.com{href}"
            if "/jobs/positions/" not in href and "/jobs/listing/" not in href:
                return None, None
            banned = {"Life at Stripe", "Benefits", "University", "Teams", "Open roles"}
            if title in banned or (title and title.lower() in {"benefits", "university"}):
                return None, None
            return title, href
        except Exception:
            return None, None

    def _extract_location(self, card):
        # Stripe renders listings in table rows; location is in a sibling <td> with span.JobsListings__locationDisplayName
        try:
            el = card.find_element(
                By.XPATH,
                "ancestor::tr[1]//span[contains(@class,'JobsListings__locationDisplayName')]",
            )
            txt = el.text.strip()
            if txt:
                return txt
        except Exception:
            pass
        # Fallbacks within the same row
        try:
            el = card.find_element(
                By.XPATH,
                "ancestor::tr[1]//td[contains(@class,'JobsListings__tableCell--country')]//span",
            )
            txt = el.text.strip()
            if txt:
                return txt
        except Exception:
            pass
        # Last resort: search near the card up the DOM
        try:
            el = card.find_element(By.XPATH, "ancestor::*[self::tr or self::li][1]//span[contains(@class,'location')]")
            txt = el.text.strip()
            if txt:
                return txt
        except Exception:
            pass
        return "Not specified"

    def _extract_details_from_job_page(self, link):
        original = self.driver.current_url
        jd_text = posted = exp = None
        try:
            # Open details in new tab
            self.driver.execute_script("window.open(arguments[0], '_blank');", link)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div.ArticleMarkdown, article, div[data-testid='job-description'], section[aria-labelledby*='description']",
                    )
                )
            )
            time.sleep(0.5)

            # Description
            for sel in [
                "div.ArticleMarkdown",
                "div[data-testid='job-description']",
                "article",
                "section[aria-labelledby*='description']",
            ]:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, sel)
                    text = el.text.strip()
                    if text and len(text) > 50:
                        jd_text = text
                        break
                except Exception:
                    continue

            # Posted date
            for sel in ["time", "[data-testid='posting-date']", "span[class*='date']"]:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, sel)
                    txt = el.text.strip()
                    if txt:
                        posted = txt
                        break
                except Exception:
                    continue

            # Do not infer experience; return null (None) instead as requested

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
        return jd_text, posted, exp

    def _go_to_next_page(self) -> bool:
        # Try explicit next controls
        next_selectors = [
            "a[rel='next']",
            "a[aria-label='Next']",
            "button[aria-label='Next']",
            "a.JobsPagination__link[aria-label*='Next']",
        ]
        for sel in next_selectors:
            try:
                btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )
                self.driver.execute_script("arguments[0].click();", btn)
                return True
            except Exception:
                continue

        # Fallback: attempt infinite scroll and detect growth
        before = len(self._find_job_cards())
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        after = len(self._find_job_cards())
        return after > before


if __name__ == "__main__":
    scraper = StripeScraper(headless=True)
    data = scraper.scrape_jobs(max_pages=2)
    scraper.save_to_json()
    print(f"Scraped {len(data)} jobs from Stripe")
