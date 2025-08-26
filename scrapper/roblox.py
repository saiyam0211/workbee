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
url = "https://careers.roblox.com/jobs"
driver.get(url)
L=[]
driver.implicitly_wait(20)
driver.execute_script("window.scrollTo(0,0.85*document.body.scrollHeight);")
time.sleep(3)
all_filters = driver.find_elements(By.XPATH,"//a[@class='toggle ng-tns-c32-0']")
# print(all_filters)
wanted_filters = ["Engineering","Data Science & Analytics","Information Technology"]
for i in all_filters:
    # print(i)
    if i.get_attribute("innerHTML") in wanted_filters or "Data Science" in i.get_attribute("innerHTML"):
        # print(i)
        driver.execute_script("arguments[0].click();", i)
time.sleep(3)


while True:
    current_html = driver.page_source
    soup = BeautifulSoup(current_html,"html.parser")
    all_jobs = soup.find_all("div",class_='job ng-tns-c32-0 ng-star-inserted')


    for i in all_jobs:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("a",class_='ng-tns-c32-0').text
        job_location = soup2.find("small",class_='ng-tns-c32-0').text
        job_link = "https://careers.roblox.com"+soup2.find("a",class_='ng-tns-c32-0')["href"]
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    # try:
    #     driver.find_element(By.XPATH,"//li[@class='pagination-next ng-star-inserted disabled']")
    #     break
    try:
        el = driver.find_element(By.XPATH,"//li[@class='pagination-next ng-star-inserted']")
        driver.find_element(By.XPATH,"//li[@class='pagination-next ng-star-inserted']").click()
        # print(el)
        driver.execute_script("arguments[0].click();", el)
        time.sleep(3)
    except:
        driver.quit()
        break
    
# print(len(L))
json_data = json.dumps(L)
print(json_data)
driver.quit()
