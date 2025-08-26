from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Make sure you have the ChromeDriver executable in your system PATH
driver.maximize_window()

# Navigate to the website
driver.get("https://jobs.exxonmobil.com/search/?q=&department=engineering&sortColumn=referencedate&sortDirection=desc")

# Wait for the job list to load
page_number = 3
last_page = int(int(driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[3]/div/div/div/span[1]/b[2]")[0].text.strip()) / 25 + 2)
job_data = []

while True:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".searchResultsShell")))

    # Get all the job elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".data-row")

    # Iterate over the job elements and extract the job information
    for job_element in job_elements:
        # Extract job title
        title_element = job_element.find_element(By.CSS_SELECTOR, '.colTitle')
        job_title = title_element.text.strip()

        # # Extract job location
        location_element = job_element.find_element(By.CSS_SELECTOR, ".colLocation")
        job_location = location_element.text.strip()

        # Extract job description
        description_element = job_element.find_element(By.CSS_SELECTOR, ".jobDepartment")
        job_description = description_element.text.strip()

        job_details = {
            'Title': job_title,
            'Location': job_location,
            'Category': job_description
        }


        # Append the job details to the job data list
        job_data.append(job_details)

    
    # next_button = driver.find_element(By.CSS_SELECTOR, ".paginationItemLast")
    # if not next_button:
    #     break  # Exit the loop if there's no next button or if it's disabled

    # # Click the next button to load the next page of job listings
    # next_button.click()

    # # Wait for the new page to load
    # wait.until(EC.staleness_of(job_elements[0]))

    # # Get the job elements of the new page
    # job_elements = driver.find_elements(By.CSS_SELECTOR, ".data-row")
    
    try:
        # Find the page number element and click on the next page number
        page_number_element = driver.find_element(By.CSS_SELECTOR, f".pagination > li:nth-of-type({page_number}) a")
        page_number_element.click()
        page_number += 1

        # Wait for the new page to load
        wait.until(EC.staleness_of(job_elements[0]))

        # Get the job elements of the new page
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-result-list .job-result")
        if(page_number>=last_page):
            break

    except NoSuchElementException:
        break  # Exit the loop if the page number element is not found

with open('Exxonmobil.json', 'w') as file:
    json.dump(job_data, file, indent=4)

# Close the browser
driver.quit()
