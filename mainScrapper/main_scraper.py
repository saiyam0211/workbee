"""
Main job scraper orchestrator - runs all company scrapers
"""
import asyncio
import json
import logging
import argparse
from typing import Dict, List
from dataclasses import asdict, is_dataclass
import sys
import os

# Add companies directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'companies'))

# Import all company scrapers
from companies.google import GoogleScraper
from companies.amazon import AmazonScraper
from companies.apple import AppleScraper
from companies.microsoft import MicrosoftScraper
from companies.meta import MetaScraper
from companies.amd import AMDScraper
from companies.nvidia import NvidiaScraper
from companies.yahoo import YahooScraper
from companies.stripe import StripeScraper
from companies.tesla import TeslaScraper
from companies.airbnb import AirbnbScraper
from companies.spotify import SpotifyScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobScraperOrchestrator:
    """Orchestrator for running all company job scrapers"""
    
    def __init__(self):
        self.scrapers = {
            'google': GoogleScraper,
            'amazon': AmazonScraper,
            'apple': AppleScraper,
            'microsoft': MicrosoftScraper,
            'meta': MetaScraper,
            'amd': AMDScraper,
            'nvidia': NvidiaScraper,
            'yahoo': YahooScraper,
            'stripe': StripeScraper,
            'tesla': TeslaScraper,
            'airbnb': AirbnbScraper,
            'spotify': SpotifyScraper
        }
        self.results = {}
    
    def scrape_company(self, company_name: str, max_pages: int = 1, headless: bool = True) -> Dict:
        """Scrape jobs from a specific company"""
        if company_name not in self.scrapers:
            return {
                'status': 'failed',
                'error': f'Unknown company: {company_name}',
                'total_jobs': 0
            }
        
        try:
            logger.info(f"🚀 Starting to scrape {company_name} jobs...")
            scraper_class = self.scrapers[company_name]
            scraper = scraper_class(headless=headless)
            jobs = scraper.scrape_jobs(max_pages=max_pages)
            scraper.save_to_json()
            
            return {
                'status': 'success',
                'total_jobs': len(jobs),
                'jobs': jobs
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to scrape {company_name}: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'total_jobs': 0
            }
    
    def scrape_all_companies(self, max_pages: int = 1, headless: bool = True, concurrent: bool = True) -> Dict:
        """Scrape jobs from all companies"""
        logger.info(f"🚀 Starting to scrape jobs from all {len(self.scrapers)} companies...")
        
        results = {}
        total_jobs = 0
        
        for company_name in self.scrapers.keys():
            result = self.scrape_company(company_name, max_pages, headless)
            results[company_name] = result
            if result['status'] == 'success':
                total_jobs += result['total_jobs']
        
        logger.info(f"🎉 Completed scraping all companies. Total jobs: {total_jobs}")
        return results

    def save_combined_json(self, results: Dict, filename: str = "all_jobs.json") -> None:
        """Save a single combined JSON for all companies"""
        combined = []
        for company, result in results.items():
            if result.get('status') != 'success':
                continue
            for job in result.get('jobs', []):
                if is_dataclass(job):
                    combined.append(asdict(job))
                elif isinstance(job, dict):
                    combined.append(job)
                else:
                    # Fallback best-effort serialization
                    try:
                        combined.append(asdict(job))
                    except Exception:
                        continue
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved combined {len(combined)} jobs to {filename}")
    
    def print_summary(self, results: Dict):
        """Print summary of scraping results"""
        print("\n" + "="*60)
        print("📊 JOB SCRAPING SUMMARY")
        print("="*60)
        
        total_jobs = 0
        successful_companies = 0
        
        for company, result in results.items():
            status = result['status']
            job_count = result['total_jobs']
            
            if status == 'success':
                print(f"✅ {company.upper():<12} - {job_count:>3} jobs")
                total_jobs += job_count
                successful_companies += 1
            else:
                print(f"❌ {company.upper():<12} - FAILED ({result.get('error', 'Unknown error')})")
        
        print("="*60)
        print(f"📈 Total Jobs Scraped: {total_jobs}")
        print(f"🏢 Successful Companies: {successful_companies}/{len(self.scrapers)}")
        print("="*60)

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Job Scraper for Multiple Companies')
    parser.add_argument('--company', type=str, help='Specific company to scrape (e.g., google, amazon)')
    parser.add_argument('--pages', type=int, help='Maximum pages to scrape per company. If omitted, scrapes ALL pages')
    parser.add_argument('--page', type=int, help='Alias for --pages (for backward compatibility)')
    parser.add_argument('--headless', action='store_true', default=True, help='Run browser in headless mode (default: True)')
    parser.add_argument('--no-headless', action='store_true', help='Run browser with GUI')
    parser.add_argument('--list-companies', action='store_true', help='List available companies')
    
    args = parser.parse_args()
    
    if args.list_companies:
        print("Available companies:")
        for company in ['google', 'amazon', 'apple', 'microsoft', 'meta', 'amd', 'nvidia', 'yahoo', 'stripe', 'tesla', 'airbnb', 'spotify']:
            print(f"  - {company}")
        return
    
    headless = args.headless and not args.no_headless
    
    # Handle both --pages and --page arguments
    # If neither provided, scrape ALL pages (use high cap; scrapers stop when no next page)
    max_pages = args.pages if args.pages is not None else args.page
    if max_pages is None:
        max_pages = 1000
    
    orchestrator = JobScraperOrchestrator()
    
    try:
        if args.company:
            # Scrape specific company
            if args.company not in orchestrator.scrapers:
                print(f"Error: Unknown company '{args.company}'")
                print("Available companies:", list(orchestrator.scrapers.keys()))
                return
                
            result = orchestrator.scrape_company(args.company, max_pages, headless)
            orchestrator.results[args.company] = result
            
            # Print summary for single company
            print(f"\n🎉 Scraped {result['total_jobs']} jobs from {args.company.upper()}")
            if result['status'] == 'failed':
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
        else:
            # Scrape all companies
            results = orchestrator.scrape_all_companies(max_pages, headless, concurrent=True)
            orchestrator.print_summary(results)
            # Save combined output
            orchestrator.save_combined_json(results, filename="all_jobs.json")
            
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()