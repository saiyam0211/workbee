from selenium import webdriver
import traceback
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
url = "https://careers.airbnb.com/positions/"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
soup = BeautifulSoup(driver.page_source,"html.parser")
var0 = driver.find_element(By.XPATH,"//button[@data-item-id='85549']")
driver.execute_script("arguments[0].click()", var0)
time.sleep(3)
soup2 = BeautifulSoup(driver.page_source,"html.parser")
var1 = soup2.find_all("li",class_='jobs-board__positions__list__item')
L = []
for i in var1:
    soup3 = BeautifulSoup(str(i),"html.parser")
    job_title = soup3.find("h3", class_ = 'jobs-board__positions__list__item__title').text
    job_link =  soup3.find("a", class_ ='jobs-board__positions__list__item__link')["href"]
    job_location = soup3.find("span",class_="jobs-board__positions__list__item__location").text
    L.append({"job_title":job_title,"job_location":job_location,"job_location":job_location})



var0 = driver.find_element(By.XPATH,"//button[@data-item-id='Engineering']")
driver.execute_script("arguments[0].click()", var0)
time.sleep(3)
soup2 = BeautifulSoup(driver.page_source,"html.parser")
var1 = soup2.find_all("li",class_='jobs-board__positions__list__item')
for i in var1:
    soup3 = BeautifulSoup(str(i),"html.parser")
    job_title = soup3.find("h3", class_ = 'jobs-board__positions__list__item__title').text
    job_link =  soup3.find("a", class_ ='jobs-board__positions__list__item__link')["href"]
    job_location = soup3.find("span",class_="jobs-board__positions__list__item__location").text
    L.append({"job_title":job_title,"job_location":job_location,"job_location":job_location})



var0 = driver.find_element(By.XPATH,"//button[@data-item-id='252']")
driver.execute_script("arguments[0].click()", var0)
time.sleep(3)
soup2 = BeautifulSoup(driver.page_source,"html.parser")
var1 = soup2.find_all("li",class_='jobs-board__positions__list__item')
for i in var1:
    soup3 = BeautifulSoup(str(i),"html.parser")
    job_title = soup3.find("h3", class_ = 'jobs-board__positions__list__item__title').text
    job_link =  soup3.find("a", class_ ='jobs-board__positions__list__item__link')["href"]
    job_location = soup3.find("span",class_="jobs-board__positions__list__item__location").text
    L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})

json_data = json.dumps({"company":"airbnb","data":L})
print(json_data)



driver.quit()
