#!/usr/bin/env python3
"""
Comprehensive script to fix all issues in scrapers and test them
"""

import os
import re
import json
import subprocess
import time
from pathlib import Path

def fix_missing_dependencies(file_path):
    """Fix missing dependencies in scraper files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove chromedriver_binary import if it fails
    content = re.sub(
        r'import chromedriver_binary\n',
        r'# import chromedriver_binary  # Removed due to installation issues\n',
        content
    )
    
    # Remove app.config.logger import if it fails
    content = re.sub(
        r'from app\.config\.logger import setup_logger\n',
        r'# from app.config.logger import setup_logger  # Removed due to import issues\n',
        content
    )
    
    # Add simple logging replacement
    if 'setup_logger' in content and 'from app.config.logger import setup_logger' not in content:
        content = re.sub(
            r'setup_logger\("([^"]+)", "([^"]+)"\)',
            r'print  # Simple logging replacement',
            content
        )
    
    # Write back only if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed dependencies in {file_path}")
        return True
    
    return False

def fix_indentation_issues(file_path):
    """Fix indentation issues in scraper files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix common indentation patterns
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Fix job_description extraction indentation
        if 'job_description = extract_job_description(' in line and line.strip().startswith('job_description'):
            # Check if previous line has proper indentation
            if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('#'):
                # Match indentation of previous line
                prev_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                line = ' ' * prev_indent + line.strip()
        
        # Fix count+=1 indentation
        if 'count+=1' in line and line.strip().startswith('count+=1'):
            if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('#'):
                prev_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                line = ' ' * prev_indent + line.strip()
        
        fixed_lines.append(line)
    
    new_content = '\n'.join(fixed_lines)
    
    # Write back only if changes were made
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed indentation in {file_path}")
        return True
    
    return False

def fix_missing_variables(file_path):
    """Fix missing variable definitions"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix missing job_description variable
    if 'job_description' in content and 'job_description = extract_job_description(' not in content:
        # Find where job_description is used but not defined
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # If line uses job_description but it's not defined in the loop
            if '"job_description": job_description' in line and i > 0:
                # Check if job_description was defined in previous lines
                prev_content = '\n'.join(lines[:i])
                if 'job_description = extract_job_description(' not in prev_content:
                    # Add job_description extraction before this line
                    if 'job_link' in prev_content:
                        # Find the job_link line and add job_description after it
                        for j in range(i-1, max(0, i-10), -1):
                            if 'job_link' in lines[j] and '=' in lines[j]:
                                indent = len(lines[j]) - len(lines[j].lstrip())
                                job_link_var = lines[j].split('=')[0].strip()
                                if job_link_var.endswith('job_link'):
                                    # Add job_description extraction
                                    desc_line = ' ' * indent + f'job_description = extract_job_description({job_link_var}, firefox_options)'
                                    fixed_lines.append(desc_line)
                                    break
            fixed_lines.append(line)
        
        new_content = '\n'.join(fixed_lines)
        
        # Write back only if changes were made
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed missing variables in {file_path}")
            return True
    
    return False

def fix_duplicate_job_posted_at(file_path):
    """Fix duplicate job_posted_at fields in scraper files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix duplicate job_posted_at fields
    content = re.sub(
        r'"job_posted_at": datetime\.now\(\)\.strftime\("%Y-%m-%d %H:%M:%S"\), "job_posted_at": datetime\.now\(\)\.strftime\("%Y-%m-%d %H:%M:%S"\)',
        r'"job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")',
        content
    )
    
    # Fix multiple duplicate job_posted_at fields
    content = re.sub(
        r'"job_posted_at": datetime\.now\(\)\.strftime\("%Y-%m-%d %H:%M:%S"\), "job_posted_at": datetime\.now\(\)\.strftime\("%Y-%m-%d %H:%M:%S"\), "job_posted_at": datetime\.now\(\)\.strftime\("%Y-%m-%d %H:%M:%S"\)',
        r'"job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")',
        content
    )
    
    # Fix trailing comma before job_posted_at
    content = re.sub(
        r', "job_posted_at": datetime\.now\(\)\.strftime\("%Y-%m-%d %H:%M:%S"\)',
        r', "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")',
        content
    )
    
    # Write back only if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed duplicate job_posted_at in {file_path}")
        return True
    
    return False

def test_scraper(file_path):
    """Test a single scraper to see if it works"""
    try:
        print(f"Testing {file_path.name}...")
        
        # Run the scraper with a timeout
        result = subprocess.run(
            ['python3', str(file_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            # Try to parse the output as JSON
            try:
                output = result.stdout.strip()
                if output:
                    # Find JSON in the output
                    json_start = output.find('{')
                    json_end = output.rfind('}') + 1
                    if json_start != -1 and json_end != 0:
                        json_str = output[json_start:json_end]
                        data = json.loads(json_str)
                        
                        if 'data' in data and isinstance(data['data'], list):
                            job_count = len(data['data'])
                            print(f"✅ {file_path.name}: {job_count} jobs found")
                            
                            # Check if job descriptions are present
                            if job_count > 0:
                                sample_job = data['data'][0]
                                has_description = 'job_description' in sample_job
                                print(f"   - Job descriptions: {'✅' if has_description else '❌'}")
                            
                            return job_count
                        else:
                            print(f"❌ {file_path.name}: Invalid data structure")
                            return 0
                    else:
                        print(f"❌ {file_path.name}: No JSON output found")
                        return 0
                else:
                    print(f"❌ {file_path.name}: No output")
                    return 0
            except json.JSONDecodeError as e:
                print(f"❌ {file_path.name}: JSON parsing error - {str(e)}")
                return 0
        else:
            print(f"❌ {file_path.name}: Execution failed - {result.stderr}")
            return 0
            
    except subprocess.TimeoutExpired:
        print(f"❌ {file_path.name}: Timeout (5 minutes)")
        return 0
    except Exception as e:
        print(f"❌ {file_path.name}: Error - {str(e)}")
        return 0

def main():
    """Main function to fix and test all scrapers"""
    
    companies_dir = Path("companies")
    if not companies_dir.exists():
        print("Companies directory not found!")
        return
    
    python_files = list(companies_dir.glob("*.py"))
    
    print(f"Found {len(python_files)} scraper files")
    print("=" * 50)
    
    # Step 1: Fix missing dependencies
    print("Step 1: Fixing missing dependencies...")
    fixed_count = 0
    for file_path in python_files:
        try:
            if fix_missing_dependencies(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing dependencies in {file_path}: {str(e)}")
    
    print(f"Fixed dependencies in {fixed_count} files")
    print("=" * 50)
    
    # Step 2: Fix indentation issues
    print("Step 2: Fixing indentation issues...")
    fixed_count = 0
    for file_path in python_files:
        try:
            if fix_indentation_issues(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing indentation in {file_path}: {str(e)}")
    
    print(f"Fixed indentation in {fixed_count} files")
    print("=" * 50)
    
    # Step 3: Fix missing variables
    print("Step 3: Fixing missing variables...")
    fixed_count = 0
    for file_path in python_files:
        try:
            if fix_missing_variables(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing variables in {file_path}: {str(e)}")
    
    print(f"Fixed variables in {fixed_count} files")
    print("=" * 50)
    
    # Step 4: Fix duplicate job_posted_at issues
    print("Step 4: Fixing duplicate job_posted_at fields...")
    fixed_count = 0
    for file_path in python_files:
        try:
            if fix_duplicate_job_posted_at(file_path):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {file_path}: {str(e)}")
    
    print(f"Fixed {fixed_count} files with duplicate job_posted_at fields")
    print("=" * 50)
    
    # Step 5: Test scrapers
    print("Step 5: Testing scrapers...")
    results = {}
    working_count = 0
    
    for file_path in python_files:
        job_count = test_scraper(file_path)
        results[file_path.name] = job_count
        if job_count > 0:
            working_count += 1
        time.sleep(1)  # Brief pause between tests
    
    print("=" * 50)
    print("SUMMARY:")
    print(f"Total scrapers: {len(python_files)}")
    print(f"Working scrapers: {working_count}")
    print(f"Non-working scrapers: {len(python_files) - working_count}")
    
    # Show results
    print("\nDetailed Results:")
    for filename, job_count in sorted(results.items()):
        status = "✅" if job_count > 0 else "❌"
        print(f"{status} {filename}: {job_count} jobs")
    
    # Save results to file
    with open("scraper_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to scraper_test_results.json")

if __name__ == "__main__":
    main()
