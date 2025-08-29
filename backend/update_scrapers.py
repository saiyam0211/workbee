#!/usr/bin/env python3
"""
Script to update all job scrapers to include job description extraction
"""

import os
import re
import glob
from pathlib import Path

def add_job_description_extraction(file_path):
    """Add job description extraction to a scraper file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if job_description is already present
    if 'job_description' in content:
        print(f"Skipping {file_path} - already has job_description")
        return False
    
    # Add the extract_job_description function
    description_function = '''
def extract_job_description(job_link, driver_options=None):
    """Extract job description from individual job page"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        
        # Create a new driver instance for description extraction
        if driver_options is None:
            from selenium.webdriver.chrome.options import Options
            driver_options = Options()
            driver_options.add_argument("--headless")
            driver_options.add_argument("--no-sandbox")
            driver_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        desc_driver = webdriver.Chrome(options=driver_options, service=service)
        desc_driver.get(job_link)
        time.sleep(2)
        
        # Look for job description content
        description_selectors = [
            "div[data-testid='job-description']",
            ".job-description",
            ".description",
            "[class*='description']",
            "[class*='content']",
            "section",
            "article",
            ".job-details",
            "[data-testid='job-details']",
            ".job-content",
            ".job-summary",
            ".job-requirements",
            ".job-responsibilities"
        ]
        
        job_description = "Description not available"
        
        for selector in description_selectors:
            try:
                desc_element = desc_driver.find_element(By.CSS_SELECTOR, selector)
                if desc_element:
                    job_description = desc_element.text.strip()
                    if job_description and len(job_description) > 50:  # Ensure we got meaningful content
                        break
            except:
                continue
        
        desc_driver.quit()
        return job_description
        
    except Exception as e:
        print(f"Error extracting job description from {job_link}: {str(e)}")
        return "Description not available"
'''
    
    # Find where to insert the function (after imports)
    import_pattern = r'(from.*\n|import.*\n)*'
    imports_match = re.search(import_pattern, content)
    
    if imports_match:
        # Insert after imports
        insert_pos = imports_match.end()
        new_content = content[:insert_pos] + description_function + content[insert_pos:]
    else:
        # Insert at the beginning
        new_content = description_function + '\n' + content
    
    # Update job data dictionaries to include job_description
    # Pattern to match job data dictionaries
    job_data_pattern = r'(\{[^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*\})'
    
    def update_job_data(match):
        job_data = match.group(1)
        # Check if job_description is already present
        if 'job_description' not in job_data:
            # Add job_description before job_posted_at or at the end
            if 'job_posted_at' in job_data:
                job_data = job_data.replace('"job_posted_at"', '"job_description": job_description, "job_posted_at"')
            else:
                # Add at the end before closing brace
                job_data = job_data.replace('}', ', "job_description": job_description}')
        return job_data
    
    new_content = re.sub(job_data_pattern, update_job_data, new_content)
    
    # Add job description extraction calls
    # Look for patterns where job data is being created
    patterns_to_update = [
        # Pattern for class-based scrapers
        r'(jobs_data\.append\(\{[^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*\}\)\s*)',
        # Pattern for function-based scrapers
        r'(final_data\.append\(\{[^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*\}\)\s*)',
        # Pattern for L.append
        r'(L\.append\(\{[^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*\}\)\s*)',
        # Pattern for data.append
        r'(data\.append\(\{[^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*\}\)\s*)'
    ]
    
    for pattern in patterns_to_update:
        def add_description_extraction(match):
            job_data_line = match.group(1)
            
            # Extract job_link from the line
            link_match = re.search(r'"job_link":\s*([^,}]+)', job_data_line)
            if link_match:
                job_link = link_match.group(1).strip()
                
                # Add description extraction before the append
                if 'self.extract_job_description' in new_content:
                    # Class-based scraper
                    description_line = f'                    job_description = self.extract_job_description({job_link})\n'
                else:
                    # Function-based scraper
                    description_line = f'    job_description = extract_job_description({job_link}, firefox_options)\n'
                
                return description_line + job_data_line
            return job_data_line
        
        new_content = re.sub(pattern, add_description_extraction, new_content)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {file_path}")
    return True

def main():
    """Main function to update all scrapers"""
    
    # Get all Python files in the companies directory
    companies_dir = Path("companies")
    if not companies_dir.exists():
        print("Companies directory not found!")
        return
    
    python_files = list(companies_dir.glob("*.py"))
    
    print(f"Found {len(python_files)} scraper files")
    
    updated_count = 0
    for file_path in python_files:
        try:
            if add_job_description_extraction(file_path):
                updated_count += 1
        except Exception as e:
            print(f"Error updating {file_path}: {str(e)}")
    
    print(f"\nUpdated {updated_count} out of {len(python_files)} scrapers")

if __name__ == "__main__":
    main()
