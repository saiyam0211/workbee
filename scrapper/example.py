#!/usr/bin/env python3
"""
Example script demonstrating how to use the Career Page Scraper programmatically.
This shows various ways to use the scraper in your own Python code.
"""

import json
import logging
from career_scraper import CareerScraper, load_config
from company_scrapers import get_scraper

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_basic_usage():
    """Example 1: Basic scraping with the generic CareerScraper."""
    print("\n=== Example 1: Basic Usage ===")
    
    # Define a simple configuration
    config = {
        "job_container": ".job-posting, .career-item, .opening",
        "fields": {
            "title": ".title, .job-title, h3",
            "location": ".location, .job-location",
            "company": ".company, .employer",
            "job_url": {
                "selector": "a[href*='job'], a[href*='career']",
                "attribute": "href",
                "make_absolute": True
            }
        }
    }
    
    # Create scraper instance
    with CareerScraper(headless=True) as scraper:
        # Scrape a sample career page
        jobs = scraper.scrape_career_page("https://jobs.example.com/careers", config)
        print(f"Found {len(jobs)} jobs")
        
        if jobs:
            print("Sample job:", json.dumps(jobs[0], indent=2, default=str))


def example_2_using_configuration_file():
    """Example 2: Using pre-configured companies from JSON file."""
    print("\n=== Example 2: Using Configuration File ===")
    
    # Load configuration
    config = load_config("companies_config.json")
    
    if not config:
        print("Configuration file not found!")
        return
    
    # Scrape specific companies
    companies_to_scrape = ["netflix", "apple"]  # Choose companies from config
    
    for company_name in companies_to_scrape:
        if company_name not in config:
            print(f"Company {company_name} not found in config")
            continue
        
        print(f"\nScraping {company_name}...")
        
        # Get specialized scraper for the company
        with get_scraper(company_name, headless=True) as scraper:
            company_config = config[company_name]
            all_jobs = []
            
            urls = company_config.get('urls', [])
            if isinstance(urls, str):
                urls = [urls]
            
            for url in urls:
                jobs = scraper.scrape_career_page(url, company_config)
                all_jobs.extend(jobs)
            
            print(f"Found {len(all_jobs)} jobs from {company_name}")
            
            # Save results for this company
            if all_jobs:
                filename = f"{company_name}_jobs.json"
                scraper.save_results({company_name: all_jobs}, filename)


def example_3_custom_company_scraping():
    """Example 3: Scraping a custom company with dynamic configuration."""
    print("\n=== Example 3: Custom Company Scraping ===")
    
    # Define custom company configuration
    custom_company_config = {
        "urls": ["https://jobs.mycompany.com/openings"],
        "job_container": ".job-item",
        "wait_for_element": ".job-item",
        "load_more_button": ".load-more-jobs",
        "max_load_more_clicks": 2,
        "fields": {
            "title": {
                "selector": ".job-title",
                "attribute": "text"
            },
            "location": {
                "selector": ".job-location", 
                "attribute": "text",
                "transform": {
                    "type": "clean_whitespace"
                }
            },
            "salary": {
                "selector": ".salary-range",
                "attribute": "text",
                "transform": {
                    "type": "regex_extract",
                    "pattern": r"(\$[\d,]+ - \$[\d,]+)"
                }
            },
            "job_url": {
                "selector": "a.apply-button",
                "attribute": "href",
                "make_absolute": True
            },
            "posted_date": {
                "selector": ".posted-date",
                "attribute": "data-timestamp"
            }
        }
    }
    
    # Use generic scraper with custom config
    with CareerScraper(headless=True, timeout=20) as scraper:
        jobs = scraper.scrape_career_page(
            custom_company_config["urls"][0], 
            custom_company_config
        )
        
        print(f"Found {len(jobs)} jobs from custom company")
        
        if jobs:
            # Process jobs data
            for job in jobs[:3]:  # Show first 3 jobs
                print(f"Job: {job.get('title', 'N/A')}")
                print(f"Location: {job.get('location', 'N/A')}")
                print(f"URL: {job.get('job_url', 'N/A')}")
                print("-" * 40)


def example_4_batch_scraping_with_error_handling():
    """Example 4: Batch scraping multiple companies with proper error handling."""
    print("\n=== Example 4: Batch Scraping with Error Handling ===")
    
    companies_config = load_config("companies_config.json")
    if not companies_config:
        print("Could not load configuration file")
        return
    
    # Select companies to scrape
    target_companies = ["google", "amazon", "microsoft"]
    results = {}
    
    for company_name in target_companies:
        if company_name not in companies_config:
            logger.warning(f"Company {company_name} not in configuration")
            continue
        
        try:
            logger.info(f"Starting scrape for {company_name}")
            
            # Get specialized scraper
            scraper = get_scraper(company_name, headless=True, timeout=15)
            
            with scraper:
                company_config = companies_config[company_name]
                jobs = []
                
                urls = company_config.get('urls', [])
                if isinstance(urls, str):
                    urls = [urls]
                
                for url in urls:
                    try:
                        page_jobs = scraper.scrape_career_page(url, company_config)
                        jobs.extend(page_jobs)
                        logger.info(f"Scraped {len(page_jobs)} jobs from {url}")
                    except Exception as e:
                        logger.error(f"Error scraping {url}: {str(e)}")
                        continue
                
                results[company_name] = jobs
                logger.info(f"Total jobs from {company_name}: {len(jobs)}")
                
        except Exception as e:
            logger.error(f"Error with {company_name}: {str(e)}")
            results[company_name] = []
    
    # Save all results
    total_jobs = sum(len(jobs) for jobs in results.values())
    print(f"\nScraping completed! Total jobs found: {total_jobs}")
    
    output_data = {
        "total_companies": len(results),
        "total_jobs": total_jobs,
        "companies": results
    }
    
    with open("batch_scraping_results.json", 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
    
    print("Results saved to batch_scraping_results.json")


def example_5_filtering_and_processing():
    """Example 5: Scraping with post-processing and filtering."""
    print("\n=== Example 5: Filtering and Processing Results ===")
    
    config = load_config("companies_config.json")
    if not config.get("google"):
        print("Google configuration not found")
        return
    
    # Scrape Google jobs
    with get_scraper("google", headless=True) as scraper:
        google_config = config["google"]
        jobs = scraper.scrape_career_page(google_config["urls"][0], google_config)
    
    if not jobs:
        print("No jobs found")
        return
    
    # Filter and process results
    print(f"Total jobs scraped: {len(jobs)}")
    
    # Filter by location (example)
    us_jobs = [job for job in jobs if job.get('location') and 
               any(state in job['location'] for state in ['CA', 'NY', 'WA', 'TX'])]
    
    print(f"US jobs: {len(us_jobs)}")
    
    # Filter by department (example)
    engineering_jobs = [job for job in jobs if job.get('department') and 
                       'engineering' in job['department'].lower()]
    
    print(f"Engineering jobs: {len(engineering_jobs)}")
    
    # Create summary statistics
    locations = {}
    departments = {}
    
    for job in jobs:
        location = job.get('location', 'Unknown')
        department = job.get('department', 'Unknown')
        
        locations[location] = locations.get(location, 0) + 1
        departments[department] = departments.get(department, 0) + 1
    
    print("\nTop 5 locations:")
    for location, count in sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {location}: {count} jobs")
    
    print("\nTop 5 departments:")
    for dept, count in sorted(departments.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {dept}: {count} jobs")
    
    # Save filtered results
    filtered_results = {
        "summary": {
            "total_jobs": len(jobs),
            "us_jobs": len(us_jobs),
            "engineering_jobs": len(engineering_jobs)
        },
        "top_locations": dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:10]),
        "top_departments": dict(sorted(departments.items(), key=lambda x: x[1], reverse=True)[:10]),
        "sample_jobs": jobs[:5]  # First 5 jobs as sample
    }
    
    with open("filtered_results.json", 'w', encoding='utf-8') as f:
        json.dump(filtered_results, f, indent=2, ensure_ascii=False, default=str)
    
    print("Filtered results saved to filtered_results.json")


if __name__ == "__main__":
    print("Career Page Scraper - Examples")
    print("=" * 50)
    
    # Run examples (comment out any you don't want to run)
    try:
        # example_1_basic_usage()
        # example_2_using_configuration_file()
        # example_3_custom_company_scraping()
        # example_4_batch_scraping_with_error_handling()
        # example_5_filtering_and_processing()
        
        print("\nTo run examples, uncomment the desired functions in the main section.")
        print("Make sure you have the required dependencies installed:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        logger.error(f"Error running examples: {str(e)}")
        print("Make sure you have installed all dependencies and have proper configuration files.")
