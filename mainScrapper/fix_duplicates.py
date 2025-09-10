"""
Script to fix duplicate job issues in all scrapers
"""
import os
import re

def fix_duplicates_in_scraper(file_path):
    """Add duplicate prevention logic to a scraper file"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if already fixed
    if "seen_jobs = set()" in content:
        print(f"✅ {os.path.basename(file_path)} already has duplicate prevention")
        return
    
    # Extract company name from filename
    company_name = os.path.basename(file_path).replace('.py', '').title()
    
    # Add duplicate tracking after setup_driver
    old_setup = 'self.setup_driver()\n            self.navigate_to_page(self.base_url, wait_time=10)'
    new_setup = '''self.setup_driver()
            self.navigate_to_page(self.base_url, wait_time=10)
            
            # Track unique jobs to avoid duplicates
            seen_jobs = set()'''
    
    content = content.replace(old_setup, new_setup)
    
    # Add duplicate check in job processing
    old_job_processing = '''if job_data and job_data.title not in ["Job", "Learn more", "share", "..."] and len(job_data.title) > 5:
                                self.jobs_data.append(job_data)
                                real_jobs_found_on_page += 1
                                logger.info(f"✅ Scraped: {job_data.title}")'''
    
    new_job_processing = '''if job_data and job_data.title not in ["Job", "Learn more", "share", "..."] and len(job_data.title) > 5:
                                # Check for duplicates using job title and link
                                job_key = f"{job_data.title}_{job_data.job_link}"
                                if job_key not in seen_jobs:
                                    self.jobs_data.append(job_data)
                                    seen_jobs.add(job_key)
                                    real_jobs_found_on_page += 1
                                    logger.info(f"✅ Scraped: {job_data.title}")'''
    
    content = content.replace(old_job_processing, new_job_processing)
    
    # Update logging to show unique jobs
    content = content.replace(
        'logger.info(f"📊 Page {page_num + 1}: Found {real_jobs_found_on_page} jobs")',
        'logger.info(f"📊 Page {page_num + 1}: Found {real_jobs_found_on_page} new jobs (Total unique: {len(self.jobs_data)})")'
    )
    
    content = content.replace(
        'logger.info(f"🎉 Successfully scraped {len(self.jobs_data)} REAL jobs from {self.company_name} across {max_pages} pages")',
        'logger.info(f"🎉 Successfully scraped {len(self.jobs_data)} UNIQUE jobs from {self.company_name} across {max_pages} pages")'
    )
    
    # Write the updated content
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed duplicates in {os.path.basename(file_path)}")

def main():
    """Fix all scraper files"""
    companies_dir = "companies"
    
    # Files to fix (excluding already fixed ones)
    files_to_fix = [
        "apple.py", "microsoft.py", "meta.py", "amd.py", "nvidia.py", 
        "yahoo.py", "stripe.py", "tesla.py", "airbnb.py", "spotify.py"
    ]
    
    for filename in files_to_fix:
        file_path = os.path.join(companies_dir, filename)
        if os.path.exists(file_path):
            fix_duplicates_in_scraper(file_path)
        else:
            print(f"❌ File not found: {file_path}")

if __name__ == "__main__":
    main()
