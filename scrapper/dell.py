from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import csv
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
from selenium.webdriver.common.keys import Keys

firefox_options = Options()
firefox_options.add_argument("--headless")
# Set up Selenium webdriver
driver = webdriver.Firefox(options=firefox_options)

# Navigate to the Dell careers website
driver.get("https://jobs.dell.com/search-jobs")

driver.implicitly_wait(10)
#we can execute javascript code using driver.execute_script here i used javascript to scroll down to bottom
driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
time.sleep(3)

# Scrape all job listings from each page
final_data = []
ns = ''
while ns == "":
    num_str = driver.find_element(By.XPATH, "//h1[@class='search-results-heading']").get_attribute("innerHTML")
    for i in num_str:
        if i not in "0123456789":
            break
        else:
            ns += i
    try:
        int_num = int(ns)
    except:
        pass
count = 0

while True:
    # Get the page source using Selenium
    page_source = driver.page_source
    
    # Create BeautifulSoup object
    soup = BeautifulSoup(page_source, "html.parser")
    container = soup.find("section", id="search-results-list")
    total = container.find_all("li")
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        time.sleep(2)
        job_title = soup2.find("h2").text
        job_link = "https://jobs.dell.com"+soup2.find("a") ["href"]
        job_location = soup2.find("span",class_='job-location-search').text
        final_data.append({"job_title":job_title, "job_location": job_location,"job_link":job_link})
        # print({"job_title":job_title, "job_location": job_location, "job_link":job_link})
        print('a')
    time.sleep(3)  
    try:
        elem = driver.find_element(By.XPATH,"//a[@class='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep (3)
    except:
        break  

# print(len(final_data))
# # Print the job listings
# for job in final_data:
#     print("Title:", job["title"])
#     print("Location:", job["location"])
#     print("Link:", job["link"])
#     print("--------------------")

json_data = json.dumps({"company":"dell","data":final_data})
print(json_data)

# # Close the Selenium webdriver
driver.quit()
