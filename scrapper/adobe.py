from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import json
import requests
from bs4 import BeautifulSoup
import time

firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)
url = "https://careers.adobe.com/us/en/search-results"
driver.get(url)
L = []

driver.implicitly_wait(20)
time.sleep(3)

# Try to handle cookie consent if present
try:
    cookies = driver.find_element(By.XPATH,"//button[@class='btn primary-button au-target' and @click.delegate='acceptAndClose()']")
    driver.execute_script('arguments[0].click();', cookies)
    time.sleep(2)
except:
    pass

# Try to handle teams filter if present
try:
    elem = driver.find_element(By.XPATH,"//button[@data-ph-at-text='Teams']")
    driver.execute_script('arguments[0].scrollIntoView();', elem)
    driver.execute_script('arguments[0].click();', elem)
    time.sleep(2)

    category = ['Engineering and Product', 'Information Technology', 'Research']

    for i in category:
        try:
            team = driver.find_element(By.XPATH, "//input[@type='checkbox' and @data-ph-at-text='%s']"%i)
            driver.execute_script('arguments[0].scrollIntoView();', team)
            driver.execute_script('arguments[0].click();', team)
            time.sleep(2)
        except:
            pass
except:
    pass

# Get total job count with better error handling
ns = ""
try:
    num_str = driver.find_element(By.XPATH, "//span[@class='result-count']").get_attribute('innerHTML')
    for i in num_str:
        if i not in "0123456789":
            break
        else:
            ns+=i
    int_num = int(ns) if ns else 100  # Default to 100 if can't find count
except:
    int_num = 100  # Default to 100 if can't find count

print(f"Expected job count: {int_num}")

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    
    if not total:
        # Try alternative selector
        total = soup.find_all("div", class_="job-item")
    
    print(f"Found {len(total)} jobs on current page")
    
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        
        try:
            job_title = soup2.find("div", class_='job-title').text.strip()   
        except:
            try:
                job_title = soup2.find("h3").text.strip()
            except:
                job_title = "N/A"

        try:
            job_link = soup2.find("a")["href"]
            if not job_link.startswith("http"):
                job_link = "https://careers.adobe.com" + job_link
        except:
            job_link = "N/A"

        try:
            job_location = soup2.find('span', class_= 'job-location').text[9:].strip()             
        except:
            try:
                job_location = soup2.find('span', class_= 'location').text.strip()
            except:
                job_location = []
                try:
                    job_location_multi = soup2.find_all(attrs={'data-ph-at-id':"job-multi-location-item"})
                    for j in job_location_multi:
                        loc = j.get('data-ph-at-job-location-text').strip()
                        job_location.append(loc)
                except:
                    job_location = "N/A"

        try:
            job_category = soup2.find('span', class_= 'job-category').text[9:].strip()             
        except:
            try:
                job_category = soup2.find('span', class_= 'category').text.strip()
            except:
                job_category = []
                try:
                    job_category_multi = soup2.find_all(attrs={'data-ph-at-id':"job-multi-category-item"})
                    for j in job_category_multi:
                        cat = j.get('data-ph-at-job-location-text').strip()
                        job_category.append(cat)
                except:
                    job_category = "N/A"
        
        try:
            job_type = soup2.find("a")['data-ph-at-job-type-text'].strip()
        except:
            job_type = "N/A"
            
        try:
            job_created = soup2.find('span', class_='job-postdate').text[12:].strip()
        except:
            job_created = "N/A"
            
        L.append({
            "job_title": job_title, 
            'job_category': job_category, 
            "job_link": job_link, 
            "job_type": job_type, 
            "job_created": job_created, 
            "job_location": job_location
        })
        
    try:
        elem = driver.find_element(By.XPATH,"//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(3)
    except:
        try:
            # Try alternative next page selector
            elem = driver.find_element(By.XPATH,"//button[@aria-label='Next']")
            driver.execute_script('arguments[0].click();', elem)
            time.sleep(3)
        except:
            print("No more pages or next button not found")
            driver.quit()
            break

    if len(L) >= int_num:
        print(f"Reached target count: {len(L)}")
        driver.quit()
        break

json_data = json.dumps({
    "company": "adobe",
    "data": L
})
print(json_data)