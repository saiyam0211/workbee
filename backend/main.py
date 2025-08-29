from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Request
from pydantic import BaseModel
from app.config.logger import setup_logger
import os, time
import json
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from datetime import datetime
from app.config.setup_chrome_driver import setup_chrome
import uuid
import asyncio
from typing import Dict, Optional
import threading
from starlette.middleware.base import BaseHTTPMiddleware
from urllib.parse import urlencode


class URLEncodingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Access query params
        query_params = dict(request.query_params)
        
        # Encode them
        encoded_query = urlencode(query_params)
        print("URL-encoded query string:", encoded_query)

        # Proceed with the request
        response = await call_next(request)
        return response

# set up logger
logger = setup_logger("main", "logs/main.log")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(URLEncodingMiddleware)

# Global variables for background task management
scraping_jobs: Dict[str, Dict] = {}
scraping_lock = threading.Lock()
current_scraping_job: Optional[str] = None

# Load initial job data
try:
    with open("data/output.json", "r") as f:
        job_data = json.load(f)
except Exception as e:
    job_data = {}
    logger.warning("No initial job data found")

class ScrapeJobStatus(BaseModel):
    job_id: str
    status: str  # "starting", "running", "completed", "failed"
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_step: Optional[str] = None
    progress: Optional[float] = None  # 0-100
    total_jobs: Optional[int] = None
    companies_processed: Optional[int] = None
    error_message: Optional[str] = None

def scrape_all_companies_background(job_id: str):
    """Background task for scraping all companies"""
    global job_data, current_scraping_job
    
    try:
        logger.info(f"Starting background scraping job {job_id}")
        
        # Update job status
        with scraping_lock:
            scraping_jobs[job_id].update({
                "status": "running",
                "current_step": "Initializing scraping process",
                "progress": 0
            })
        
        # Step 1: Handle yesterday.json file
        with scraping_lock:
            scraping_jobs[job_id]["current_step"] = "Processing yesterday's data"
        
        try:
            # delete yesterday.json
            file_path = "data/yesterday.json"
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info("yesterday.json deleted successfully")
            else:
                logger.info("yesterday.json does not exist.")
                
            # Read the data from output.json
            with open('data/output.json', 'r') as f:
                yesterday_data = json.load(f)
            
            # change the file name: output -> yesterday
            os.rename('data/output.json', 'data/yesterday.json')
            logger.info("File renamed from output.json to yesterday.json")

        except Exception as e:
            yesterday_data = {
                'company_name_list': [],
                'company_posting_array': [],
                "error-companies": []
            }
            logger.error(f"couldn't find yesterday data, error {e}")
        
        # Step 2: Setup scraping configuration
        with scraping_lock:
            scraping_jobs[job_id]["current_step"] = "Setting up scraping configuration"
            scraping_jobs[job_id]["progress"] = 5
        
        folder_path = './companies'
        file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".py")]
        total_files = len(file_list)
        
        project_root = os.path.abspath(".")
        env = os.environ.copy()
        env["PYTHONPATH"] = project_root
        
        new_data = {
            'company_name_list': [],
            'company_posting_array': [],
            "error-companies": []
        }
        
        logger.info(f"Started scrapping {total_files} companies")
        start_time = time.time()
        
        # Step 3: Scrape each company
        for i, file in enumerate(file_list):
            company_name = os.path.basename(file).replace(".py", "")
            
            # Update progress
            progress = 10 + (i / total_files) * 70  # 10-80% for scraping
            with scraping_lock:
                scraping_jobs[job_id].update({
                    "current_step": f"Scraping {company_name} ({i+1}/{total_files})",
                    "progress": progress,
                    "companies_processed": i
                })
      
            start = time.time()
            logger.info(f"Scraping company : {company_name}")
            
            result = subprocess.run(['python3', file], capture_output=True, text=True, env=env)
            
            end = time.time()
            logger.info(f"Scrapped completed for company {file}, total time taken : {round(end - start, 2)} second")
            
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            # Initialize default structure for this company
            new_data["company_name_list"].append(company_name)

            if not stdout:
                logger.warning(f"No output from company: {company_name}")
                new_data["company_posting_array"].append([])
                new_data["error-companies"].append({"name": file, "error": stderr, "output": "No output"})
                continue
            
            try:
                output_json = json.loads(stdout)

                jobs_data = output_json.get('data', [])
                new_data['company_posting_array'].append(jobs_data)
                new_data["error-companies"].append({"name": file, "error": stderr, "output": stdout})
                
                # Optional: in case company name returned is inconsistent
                parsed_company = output_json.get('company', company_name)
                
                if parsed_company != company_name:
                    logger.debug(f"Company mismatch: Expected {company_name}, got {parsed_company}")

            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from {company_name}: {e}")
                new_data["company_posting_array"].append([])

                new_data["error-companies"].append({
                    "name": file,
                    "error": stderr,
                    "stdout": stdout[:500]  # Trimmed to avoid huge logs
                })
                continue
        
        end_time = time.time()
        logger.info(f"Scrapped all the companies, total time taken {round((end_time - start_time), 2)} seconds")
        
        # Step 4: Process data with yesterday's data
        with scraping_lock:
            scraping_jobs[job_id].update({
                "current_step": "Processing job data with yesterday's data",
                "progress": 85
            })
        
        def job_present(job_link, i):
            if i >= len(yesterday_data["company_posting_array"]):
                return None
            for job in yesterday_data["company_posting_array"][i]:
                if job.get('job_link') == job_link:
                    return job
            return None

        # Traverse on each company
        total_jobs = 0
        logger.info("Starting to update the data with yesterday's job listing's data")
        
        n = len(new_data["company_name_list"])
        for i in range(n):
            # Traverse on each job listing
            total_jobs += len(new_data["company_posting_array"][i])
            for j, job in enumerate(new_data["company_posting_array"][i]):
                # If job is in yesterday's job listing
                matched_job = job_present(job.get("job_link"), i)
                if matched_job:
                    # Update the date with yesterday data's date
                    new_data["company_posting_array"][i][j]['job_posted_at'] = matched_job.get('job_posted_at')
        
        # Step 5: Save results
        with scraping_lock:
            scraping_jobs[job_id].update({
                "current_step": "Saving results",
                "progress": 95
            })
        
        with open('data/output.json', 'w') as file:
            json.dump(new_data, file, indent=4)
        
        # update the global job data
        job_data = new_data.copy()
        
        # Final status update
        with scraping_lock:
            scraping_jobs[job_id].update({
                "status": "completed",
                "completed_at": datetime.now(),
                "current_step": "Scraping completed successfully",
                "progress": 100,
                "total_jobs": total_jobs,
                "companies_processed": len(new_data["company_name_list"])
            })
        
        logger.info(f"Background scraping job {job_id} completed successfully. Total jobs: {total_jobs}")
        
    except Exception as e:
        logger.error(f"Error occurred in background scraping job {job_id}: {str(e)}")
        with scraping_lock:
            scraping_jobs[job_id].update({
                "status": "failed",
                "completed_at": datetime.now(),
                "error_message": str(e),
                "current_step": f"Failed: {str(e)}"
            })
    finally:
        current_scraping_job = None

@app.post("/scrape_all")
async def start_scraping(background_tasks: BackgroundTasks):
    """Start scraping in background - replaces the old /scrape_all_ endpoint"""
    global current_scraping_job
    
    try:
        # Check if scraping is already running
        if current_scraping_job and current_scraping_job in scraping_jobs:
            with scraping_lock:
                current_status = scraping_jobs[current_scraping_job]["status"]
            
            if current_status in ["starting", "running"]:
                return {
                    "message": "Scraping already in progress",
                    "job_id": current_scraping_job,
                    "status": current_status
                }
        
        # Create new job
        job_id = str(uuid.uuid4())
        current_scraping_job = job_id
        
        # Initialize job status
        scraping_jobs[job_id] = {
            "job_id": job_id,
            "status": "starting",
            "started_at": datetime.now(),
            "current_step": "Initializing",
            "progress": 0,
            "companies_processed": 0
        }
        
        # Add background task
        background_tasks.add_task(scrape_all_companies_background, job_id)
        
        logger.info(f"Started new scraping job: {job_id}")
        
        return {
            "message": "Scraping started successfully",
            "job_id": job_id,
            "status": "started"
        }
        
    except Exception as e:
        logger.error(f"Error starting scraping job: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error starting scraping job: {str(e)}"
        )

@app.get("/scrape_status/{job_id}")
async def get_scraping_status(job_id: str):
    """Get specific scraping job status"""
    if job_id not in scraping_jobs:
        raise HTTPException(status_code=404, detail="Scraping job not found")
    
    with scraping_lock:
        job_status = scraping_jobs[job_id].copy()
    
    return job_status

@app.get("/scrape_status")
async def get_current_scraping_status():
    """Get current scraping job status"""
    if not current_scraping_job:
        return {
            "message": "No scraping job currently running",
            "current_job": None
        }
    
    if current_scraping_job not in scraping_jobs:
        return {
            "message": "Current job not found in records",
            "current_job": current_scraping_job
        }
    
    with scraping_lock:
        job_status = scraping_jobs[current_scraping_job].copy()
    
    return {
        "message": "Current scraping job status",
        "current_job": job_status
    }

@app.get("/scrape_jobs")
async def get_all_scraping_jobs(limit: int = Query(10, description="Number of recent jobs to return")):
    """Get all scraping jobs (recent first)"""
    with scraping_lock:
        all_jobs = list(scraping_jobs.values())
    
    # Sort by started_at descending
    sorted_jobs = sorted(all_jobs, key=lambda x: x["started_at"], reverse=True)
    
    return {
        "jobs": sorted_jobs[:limit],
        "total_jobs": len(sorted_jobs)
    }

# Keep the old endpoint for backward compatibility (but mark as deprecated)
@app.get("/scrape_all_", deprecated=True)
async def scrape_all_deprecated():
    """Deprecated: Use POST /scrape_all instead"""
    return {
        "message": "This endpoint is deprecated. Use POST /scrape_all instead.",
        "new_endpoint": "/scrape_all"
    }

def check_and_update() -> None:
    try:
        logger.info("Checking and updating output.json")
        global job_data
        if job_data:
            return
        
        # update the job data
        with open("data/output.json", "r") as f:
            job_data = json.load(f)
    except FileNotFoundError as fnf:
        logger.error(f"Could not find output.json file, error : {str(fnf)}")
    except Exception as e:
        logger.error(f"Error occurred while checking and updating the global job_data, error {str(e)}")

def find_index(company_name: str) -> int:
    try:
        logger.info(f"Finding the index for company: {company_name}")
        global job_data
        companies = job_data.get("company_name_list", [])
        
        for i in range(len(companies)):
            if companies[i].lower() == company_name.lower():
                return i
        return -1
    except Exception as e:
        logger.error(f"Error occurred while finding index, error {str(e)}")
        return -1

@app.get("/api/jobs")
async def get_jobs(company_name: str = Query(..., description="Name of the company")):
    try:
        logger.info(f"Get jobs called with company name: {company_name}")   
        check_and_update()
        
        company_name = company_name.lower()
        
        index = find_index(company_name)
        
        if index == -1:
            logger.warning("company name not found")
            return {
                "ok": False,
                "message": f"No company found with name {company_name}"
            }
            
        return {
            "ok": True,
            "message": "Company name found",
            "data": job_data["company_posting_array"][index],
            "number_of_jobs": len(job_data["company_posting_array"][index])
        }
        
    except Exception as e:
        logger.error(f"Some error occurred while sending job for company: {company_name}, error: {e}")
        raise HTTPException(
            status_code=500,
            ok=False,
            detail=f"Error occurred while getting jobs, error: {str(e)}"
        )

@app.get("/api/latest_jobs/")
async def get_latest_jobs(company_name: str = Query(..., description="Name of the company")):
    try:
        logger.info(f"Get latest jobs called with company name: {company_name}")    
        check_and_update()
        company_name = company_name.lower()

        index = find_index(company_name)
  
        if index == -1:
            return {
                'message': f"No company found with name {company_name}"
            }
                
        jobs = job_data["company_posting_array"][index]
        # sort the job with date
        sorted_jobs = sorted(
            jobs,
            key=lambda x: datetime.strptime(x['job_posted_at'], '%Y-%m-%d %H:%M:%S'),
            reverse=False
        )

        return {
            "message": "Company name found successfully",
            "data": sorted_jobs
        }
    except Exception as e:
        logger.error(f"Failed to get latest jobs for the company: {company_name}, error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while getting latest jobs, error: {str(e)}"
        )

@app.get("/api/get_companies", description="Get all the available company name, send this name in lowercase for getting the jobs for particular company")
async def get_companies():
    try:
        check_and_update()
        company_names = [f.split(".")[0] for f in os.listdir("./companies") if f.endswith(".py")]
        
        number_of_open_jobs = []
        
        
        for company in company_names:
            index = find_index(company)
            number_of_open_jobs.append(len(job_data["company_posting_array"][index]))
        
        return {
            "company_names": company_names,
            "number_of_available_companies": len(company_names),
            "open_positions": number_of_open_jobs
        }
    except Exception as e:
        logger.error(f"Error occurred while sending company names, error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while getting company names, error: {str(e)}"
        )
        
@app.get("/api/number_of_jobs")
async def get_number_of_jobs(company_name: str = Query(..., description="Name of the company")):
    try:
        logger.info(f"Get number of jobs called with company name: {company_name}")    
        check_and_update()
        company_name = company_name.lower()
        
        index = find_index(company_name)
        
        if index == -1:
            return {
                'message': f"No company found with name {company_name}"
            }

        return {
            "message": "Company name found successfully",
            "number_of_jobs": len(job_data["company_posting_array"][index]) 
        }
    except Exception as e:
        logger.error(f"Failed to send number of jobs for {company_name}")
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while getting number of jobs for company {company_name}, error: {str(e)}"
        )

@app.get("/test/check_chrome_driver")
async def check():
    try:
        file = "./companies/texas_instrument.py"
        project_root = os.path.abspath(".")
        env = os.environ.copy()
        env["PYTHONPATH"] = project_root
        logger.info("starting to run texas_instrument.py for testing")
      
        result = subprocess.run(['python3', file], capture_output=True, text=True, env=env)
        logger.info("Test run successfully")
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        if not stdout:
            return {
                "success": "warning",
                "message": "No output received",
                "error": stderr
            }
        
        try:
            output_json = json.loads(stdout)
            jobs_data = output_json.get('data', [])
            
            return {
                "success": "ok",
                "data": jobs_data,
                "error": stderr,
                "jobs_count": len(jobs_data)
            }
        except json.JSONDecodeError as e:
            return {
                "success": "error",
                "message": "Invalid JSON output",
                "stdout": stdout,
                "error": stderr,
                "json_error": str(e)
            }
            
    except Exception as e:
        logger.error(f"Error checking the chrome driver: {str(e)}")
        return {
            "success": "error",
            "message": "Got some error",
            "error": str(e)
        }

@app.get("/health")
async def health():
    try:
        return {
            "message": "App is running",
            "timestamp": datetime.now().isoformat(),
            "scraping_status": "running" if current_scraping_job else "idle"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error while checking health"
        )

def main():
    """Main application startup"""
    print("Starting application...")
    
    # Setup Chrome (much simpler now)
    if setup_chrome():
        print("Chrome is ready!")
    else:
        print("Chrome setup failed - continuing without browser automation")
    
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    
if __name__ == "__main__":
    main()