
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
#import webdriver
import os
from selenium import webdriver
# import chromedriver_binary  # Removed due to installation issues
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service 
#from webdriver_manager.firefox import GeckoDriverManager
#geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
service = Service(ChromeDriverManager().install())
firefox_options = Options()
#firefox_options.binary_location = os.environ["PATHCHROME"]
#firefox_options.binary_location = './firefox/firefox'
import os
from datetime import datetime

# helper to fetch job description using the same driver (opens a new tab)
def get_job_description_with_driver(driver, job_link: str) -> str:
    try:
        original_window = driver.current_window_handle
        driver.execute_script("window.open('about:blank','_blank');")
        time.sleep(0.5)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        driver.get(job_link)
        time.sleep(2)
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, "html.parser")
        # Try multiple common selectors
        selectors = [
            "div[data-testid='job-description']",
            ".job-description",
            "#job-description",
            "[class*='description']",
            "[class*='job__description']",
            "section",
            "article",
        ]
        description_text = "Description not available"
        for sel in selectors:
            tag = soup.select_one(sel)
            if tag:
                text = tag.get_text(" ", strip=True)
                if text and len(text) > 50:
                    description_text = text
                    break
        driver.close()
        driver.switch_to.window(original_window)
        return description_text
    except Exception:
        try:
            driver.switch_to.window(original_window)
        except Exception:
            pass
        return "Description not available"

#os.chmod('./firefox/firefox', 0o755)
# firefox_options.binary_location = geckodriver_path
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=firefox_options,service=service)
url = "https://careers.walmart.com/results?q=&page=1&sort=rank&jobCategory=00000161-7bad-da32-a37b-fbef5e390000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000015a-a577-de75-a9ff-bdff284e0000&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,00000161-8be6-da32-a37b-cbe70c150000,brand,type,rate&type=jobs"
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)
num_str = driver.find_element(By.XPATH, "//span[@id='count_totalResults']").get_attribute('innerHTML')
int_num=int(num_str)


while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="search-result job-listing")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("a", class_='job-listing__link').text   
        job_link = soup2.find("a", class_="job-listing__link")["href"]
        job_department = soup2.find("span", class_="job-listing__department eyebrow").text
        job_location = soup2.find("span", class_="job-listing__location").text
        job_created_on = soup2.find("span", class_="job-listing__created").text
        job_description = get_job_description_with_driver(driver, job_link)
        L.append({"job_title":job_title, "job_link":job_link, "job_location":job_location, "job_description": job_description, "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        # print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location, "job_created_on":job_created_on})
        # print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//button[@class='search__results__pagination__arrow' and @data-page='next']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        #print("no button?")
        driver.quit()
        break

    if len(L)>=int_num:
        #print('done')
        driver.quit()
        break

#print(len(L))

json_data=json.dumps({'company':'walmart','data':L})
print(json_data)
driver.quit()