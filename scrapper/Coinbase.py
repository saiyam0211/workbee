from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Make sure you have the ChromeDriver executable in your system PATH
driver.maximize_window()

# Navigate to the website
driver.get("https://www.coinbase.com/careers/positions")

# Wait for the job list to load

job_data = []

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Positions__PositionsColumn-jve35q-7")))
# Get all the job elements
jobs = driver.find_elements(By.CSS_SELECTOR, ".Department__DepartmentHeader-sc-1n8uxi6-1")
for job in jobs:
    job.click()

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".Department__Job-sc-1n8uxi6-4")
    print(len(job_elements))
    # Iterate over the job elements and extract the job information
    for job_element in job_elements:
        # Extract job title
        title_element = job_element.find_element(By.CSS_SELECTOR, '.Link__ARouterLink-eh4rrz-1')
        job_title = title_element.text.strip()

            # job_title = "Not available"
        # # Extract job location
        location_element = job_element.find_element(By.CSS_SELECTOR, ".cds-typographyResets-t1xhpuq2")
        job_location = location_element.text.strip()
            # job_location = "location not available"
            
        # Extract job description
        # try:
        #     description_element = job_element.find_element(By.CSS_SELECTOR, ".job-category")
        #     job_description = description_element.text.strip().replace("Category\n", "")
        # except:
        #     job_description = "Not Available"
        job_details = {
            'Title': job_title,
            'Location': job_location,
            'Category': job.text.strip()
        }
        # Append the job details to the job data list
        job_data.append(job_details)
        print(job_data)
    job.click()

    time.sleep(2)

    # try:
    #     next_button = driver.find_element(By.CSS_SELECTOR, ".next-btn")
    #     if "aurelia-hide" in next_button.get_attribute('class'):
    #         break  # Exit the loop if there's no next button or if it's disabled

    #     # Click the next button to load the next page of job listings
    #     driver.execute_script("arguments[0].click();", next_button)
    # except:
    #     break

    # next_button.click()

    # # Wait for the new page to load
    # wait.until(EC.staleness_of(job_elements[0]))

    # # Get the job elements of the new page
    # job_elements = driver.find_elements(By.CSS_SELECTOR, ".jobs-list-item")

with open('Coinbase.json', 'w') as file:
    json.dump(job_data, file, indent=4)

# Close the browser
driver.quit()
