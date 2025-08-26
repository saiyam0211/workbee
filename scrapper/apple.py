from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
from selenium.webdriver.chrome.options import Options
import json
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import threading
from urllib.parse import urljoin

# Set up Chrome options for faster performance
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment to run headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")  # We'll use requests for faster scraping
chrome_options.add_argument("--headless")  # Run headless for speed
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Global variables for thread safety
jobs_lock = threading.Lock()
all_jobs = []
total_jobs_found = 0

def scrape_page(page_num, base_url):
    """Scrape a single page and return job data"""
    global total_jobs_found
    
    try:
        # Use requests for faster scraping instead of Selenium
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page_num}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all job listing items
        job_items = soup.find_all("li", class_="rc-accordion-item")
        
        if not job_items:
            return []
        
        page_jobs = []
        for job_item in job_items:
            try:
                # Extract job title and link
                title_element = job_item.find("a", class_="link-inline")
                if not title_element:
                    continue
                    
                job_title = title_element.text.strip()
                job_link = urljoin("https://jobs.apple.com", title_element.get("href", ""))
                
                # Extract location
                location_element = job_item.find("span", class_="table--advanced-search__location-sub")
                job_location = location_element.text.strip() if location_element else "Location not specified"
                
                # Extract team name
                team_element = job_item.find("span", class_="team-name")
                team_name = team_element.text.strip() if team_element else "Team not specified"
                
                # Extract posted date
                date_element = job_item.find("span", class_="job-posted-date")
                posted_date = date_element.text.strip() if date_element else "Date not specified"
                
                # Create job data dictionary
                job_data = {
                    "job_title": job_title,
                    "job_location": job_location,
                    "job_link": job_link,
                    "team": team_name,
                    "posted_date": posted_date
                }
                
                page_jobs.append(job_data)
                
            except Exception as e:
                print(f"Error processing job item on page {page_num}: {e}")
                continue
        
        return page_jobs
        
    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")
        return []

def get_total_job_count():
    """Get the total number of jobs from the first page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get("https://jobs.apple.com/en-in/search", headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Look for the result count element
        result_count_element = soup.find("p", {"id": "search-result-count"})
        if result_count_element:
            num_str = result_count_element.text
            ns = ""
            for i in num_str:
                if i.isdigit():
                    ns += i
                elif ns:
                    break
            if ns:
                return int(ns)
    except Exception as e:
        print(f"Error getting total job count: {e}")
    
    return 0

def main():
    base_url = "https://jobs.apple.com/en-in/search"
    
    print("Getting total job count...")
    total_jobs = get_total_job_count()
    print(f"Found {total_jobs} total jobs")
    
    if total_jobs == 0:
        print("Could not determine total job count, using default limit")
        total_jobs = 229  # Default fallback
    
    # Calculate how many pages we need to scrape
    jobs_per_page = 25  # Apple shows ~25 jobs per page
    estimated_pages = min((total_jobs // jobs_per_page) + 2, 20)  # Limit to 20 pages max for speed
    
    print(f"Will scrape approximately {estimated_pages} pages to get all jobs")
    
    # Use ThreadPoolExecutor for parallel scraping
    all_jobs = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all page scraping tasks
        future_to_page = {
            executor.submit(scrape_page, page_num, base_url): page_num 
            for page_num in range(1, estimated_pages + 1)
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_page):
            page_num = future_to_page[future]
            try:
                page_jobs = future.result()
                if page_jobs:
                    all_jobs.extend(page_jobs)
                    print(f"Page {page_num}: Found {len(page_jobs)} jobs (Total: {len(all_jobs)})")
                else:
                    print(f"Page {page_num}: No jobs found")
                
                # Early termination if we have enough jobs
                if len(all_jobs) >= total_jobs:
                    print(f"Reached target job count ({total_jobs}), stopping...")
                    break
                    
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        job_key = (job["job_title"], job["job_location"], job["job_link"])
        if job_key not in seen:
            seen.add(job_key)
            unique_jobs.append(job)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Save the results
    json_data = json.dumps({
        "company": "apple",
        "data": unique_jobs
    }, indent=2)
    
    print(f"\n=== SCRAPING COMPLETE ===")
    print(f"Total jobs scraped: {len(unique_jobs)}")
    print(f"Expected jobs: {total_jobs}")
    print(f"Time taken: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print(f"Pages processed: {estimated_pages}")
    print(f"Jobs per second: {len(unique_jobs)/elapsed_time:.2f}")
    
    print("\nSample of scraped data:")
    if unique_jobs:
        print(json.dumps(unique_jobs[:3], indent=2))
    
    # Save to file
    with open("apple_jobs.json", "w", encoding="utf-8") as f:
        f.write(json_data)
    
    print(f"\nData saved to apple_jobs.json")
    
    return unique_jobs

if __name__ == "__main__":
    main()