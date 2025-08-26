from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import requests
from bs4 import BeautifulSoup
import time
firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)
url ="https://careers.bloomberg.com/job/search?sd=Software+Engineering&sd=Engineering&sd=Systems%2F+Network+Engineering&sd=Technical+Operations&fd=Engineering&fd=UX"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
L = []
while True:
    soup = BeautifulSoup(driver.page_source,"html.parser")
    try:
        elem = driver.find_element(By.XPATH,"//button[@class='btn btn-primary smallcaps load-more-button js-load-more-jobs']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
    except:
        break
soup2 = BeautifulSoup(driver.page_source,"html.parser")
total = soup2.find_all("div",class_='job-results-section')
print(len(total))
for i in total:
    soup3 = BeautifulSoup(str(i),"html.parser")
    job_title = soup3.find("div", class_ = 'job-results-name').text
    job_link = "https://careers.bloomberg.com" + soup3.find("a", class_ ='js-display-job')["href"]
    job_location = soup3.find("span",class_="job-results-city").text
    L.append({"job_title":job_title,"job_location":job_location,"job_link": job_link})
json_data = json.dumps({"company":"bloomberg","data":L})
print(json_data)
driver.quit()