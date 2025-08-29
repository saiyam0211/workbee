#!/usr/bin/env python3
"""
Script to fix common issues in updated scrapers
"""

import os
import re
from pathlib import Path

def fix_scraper_issues(file_path):
    """Fix common issues in scraper files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix indentation issues with job_description extraction
    content = re.sub(
        r'(\s+)job_description = extract_job_description\(job_link, firefox_options\)\n(\s+)L\.append',
        r'\1job_description = extract_job_description(job_link, firefox_options)\n\1L.append',
        content
    )
    
    # Fix missing job_posted_at in append statements
    content = re.sub(
        r'L\.append\(\{([^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*"job_description"[^}]*)\}\)',
        r'L.append({\1, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})',
        content
    )
    
    content = re.sub(
        r'final_data\.append\(\{([^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*"job_description"[^}]*)\}\)',
        r'final_data.append({\1, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})',
        content
    )
    
    content = re.sub(
        r'data\.append\(\{([^}]*"job_title"[^}]*"job_location"[^}]*"job_link"[^}]*"job_description"[^}]*)\}\)',
        r'data.append({\1, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})',
        content
    )
    
    # Fix duplicate job_posted_at assignments
    content = re.sub(
        r'for i in range\(len\(L\)\):\s*L\["job_posted_at"\] = datetime\.now\(\)\.strftime\("%Y-%m-%d %H:%M:%S"\)',
        r'# job_posted_at already added in append statements',
        content
    )
    
    # Fix incorrect dictionary access
    content = re.sub(
        r'L\["job_posted_at"\]',
        r'# Fixed: job_posted_at should be added in append statements',
        content
    )
    
    # Write back only if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed issues in {file_path}")
        return True
    
    return False

def main():
    """Main function to fix all scrapers"""
    
    companies_dir = Path("companies")
    if not companies_dir.exists():
        print("Companies directory not found!")
        return
    
    python_files = list(companies_dir.glob("*.py"))
    
    print(f"Checking {len(python_files)} scraper files for issues...")
    
    fixed_count = 0
    for file_path in python_files:
        try:
            if fix_scraper_issues(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {file_path}: {str(e)}")
    
    print(f"\nFixed issues in {fixed_count} out of {len(python_files)} scrapers")

if __name__ == "__main__":
    main()
