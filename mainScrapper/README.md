# 🚀 Job Scraper - All 12 Companies

A clean, working job scraper that extracts **REAL job data** from 12 major tech companies.

## ✅ **What's Included**

### **12 Company Scrapers:**
- **Google** - Software Engineer, Data Scientist, etc.
- **Amazon** - SDE, Product Manager, etc.
- **Apple** - iOS Developer, Hardware Engineer, etc.
- **Microsoft** - Software Engineer, Cloud Engineer, etc.
- **Meta** - Frontend Engineer, Data Engineer, etc.
- **AMD** - Hardware Engineer, Software Engineer, etc.
- **NVIDIA** - AI Engineer, Graphics Engineer, etc.
- **Yahoo** - Full Stack Developer, etc.
- **Stripe** - Backend Engineer, etc.
- **Tesla** - Autopilot Engineer, etc.
- **Airbnb** - Frontend Engineer, etc.
- **Spotify** - Backend Engineer, etc.

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Individual Company Scraper**
```bash
# Scrape Google jobs
python3 companies/google.py

# Scrape Amazon jobs
python3 companies/amazon.py

# Scrape Apple jobs
python3 companies/apple.py
```

### **3. Run Main Orchestrator**
```bash
# Scrape specific company (1 page)
python3 main_scraper.py --company google --pages 1

# Scrape specific company (3 pages)
python3 main_scraper.py --company google --pages 3

# Scrape all companies (2 pages each)
python3 main_scraper.py --pages 2

# List available companies
python3 main_scraper.py --list-companies
```

## 📊 **What You Get**

### **Real Job Data:**
- ✅ **Job Title** - Actual job titles from company websites
- ✅ **Location** - Real locations (Bangalore, Gurugram, Mumbai, etc.)
- ✅ **Job Link** - Direct links to job postings
- ✅ **Company** - Company name
- ✅ **Scraped Date** - When the data was extracted

### **JSON Output:**
```json
{
  "title": "Software Engineer III, Google Cloud",
  "location": "Google | Gurugram, Haryana, India",
  "experience_required": "Not specified",
  "job_description": "Job description available on company website",
  "job_link": "https://www.google.com/about/careers/applications/jobs/results/74939955737961158-software-engineer-iii-google-cloud?location=India",
  "posted_date": "Not specified",
  "company": "Google",
  "scraped_at": "2025-09-09T22:39:54.042308"
}
```

## 🏗️ **Project Structure**

```
mainScrapper/
├── base_scraper.py          # Base scraper class
├── main_scraper.py          # Main orchestrator
├── requirements.txt         # Dependencies
├── README.md               # This file
└── companies/              # Individual company scrapers
    ├── google.py
    ├── amazon.py
    ├── apple.py
    ├── microsoft.py
    ├── meta.py
    ├── amd.py
    ├── nvidia.py
    ├── yahoo.py
    ├── stripe.py
    ├── tesla.py
    ├── airbnb.py
    └── spotify.py
```

## 🎯 **Features**

- ✅ **Real Data** - No mock data, extracts actual job postings
- ✅ **12 Companies** - All major tech companies covered
- ✅ **Pagination Support** - Scrape multiple pages per company
- ✅ **Clean Code** - Simple, maintainable Python code
- ✅ **JSON Output** - Structured data ready for frontend
- ✅ **CLI Interface** - Easy command-line usage
- ✅ **Error Handling** - Robust error handling and logging
- ✅ **Headless Mode** - Runs without opening browser windows

## 🔧 **CLI Options**

```bash
python3 main_scraper.py [OPTIONS]

Options:
  --company COMPANY    Specific company to scrape
  --pages PAGES        Maximum pages to scrape (default: 1)
  --headless           Run browser in headless mode (default)
  --no-headless        Run browser with GUI
  --list-companies     List available companies
```

## 📈 **Example Output**

```
🚀 Starting to scrape Google jobs (max 3 pages)...
✅ Browser setup successful for Google
📍 Navigating to: https://careers.google.com/jobs/results/?location=India
📄 Scraping page 1 of 3
🔍 Found 149 potential job elements on page 1
✅ Scraped: Software Engineer III, Google Cloud
✅ Scraped: Senior Service Strategy Activation Lead
✅ Scraped: Customer Engineer, Marketing Technology, Google Cloud
📊 Page 1: Found 15 jobs
🔄 Trying infinite scroll to load more jobs...
📄 Scraping page 2 of 3
📊 Page 2: Found 15 jobs
📄 Scraping page 3 of 3
📊 Page 3: Found 15 jobs
🎉 Successfully scraped 45 REAL jobs from Google across 3 pages
💾 Saved 45 jobs to google_jobs.json
```

## 🎉 **Success!**

This scraper successfully extracts **real job data** from all 12 companies. Each scraper is tested and working, providing you with actual job postings that you can use in your frontend application.

**No more mock data - just real, current job information!** 🚀