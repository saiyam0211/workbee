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
url = "https://www.uber.com/in/en/careers/list/?"
filter_options = ["Data Science","Engineering"]
for i in filter_options:
    url = url+"department="+i+"&"
url = url[:len(url)-1]
# print(url)
driver.get(url)
L=[]
number_container = driver.find_element(By.XPATH,"//div[@class='css-kqHVrb']").text
str_num = ""
for i in number_container:
    if i not in "0123456789":
        break
    else:
        str_num+=i
initial_html = driver.page_source
soup = BeautifulSoup(initial_html,"html.parser")
start_element = soup.find_all("div",class_='css-wQMHt')
next_elements = soup.find_all("div",class_='css-fzNECT')
total = len(next_elements)+len(start_element)
# count=0
while (total<int(str_num)):
    elem = driver.find_element(By.XPATH,"//button[@class='css-kTiVgx']")
    driver.execute_script("arguments[0].click();", elem)
    time.sleep(3)
    initial_html = driver.page_source
    soup = BeautifulSoup(initial_html,"html.parser")
    start_element = soup.find_all("div",class_='css-wQMHt')
    next_elements = soup.find_all("div",class_='css-fzNECT')
    total = len(next_elements)+len(start_element)
for i in next_elements:
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_title = soup2.find("a",class_='css-bNzNOn').text
    job_link = soup2.find("a",class_='css-bNzNOn')["href"]
    if "https://www.uber.com" not in job_link:
        job_link="https://www.uber.com/global/en"+job_link
    job_locationlist = soup2.find_all("div",class_='css-bAjVIk')
    for i in job_locationlist:
        if "Location" in i.text.replace("\n",""):
            job_location = i.text.replace("\n","").replace("Location","")
    # job_location = soup2.find("div",class_='css-bAjVIk').text
    L.append({"job_title":job_title,"job_link":job_link,"job_location":job_location})
for i in start_element:
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_title = soup2.find("a",class_='css-bNzNOn').text
    job_link = soup2.find("a",class_='css-bNzNOn')["href"]
    if "https://www.uber.com" not in job_link:
        job_link="https://www.uber.com/global/en"+job_link
    job_locationlist = soup2.find_all("div",class_='css-bAjVIk')
    for i in job_locationlist:
        if "Location" in i.text.replace("\n",""):
            job_location = i.text.replace("\n","").replace("Location","")

    # job_location = soup2.find("div",class_='css-bAjVIk').text
    L.append({"job_title":job_title,"job_link":job_link,"job_location":job_location})
json_data = json.dumps(L)
driver.quit()
# json_data = json.dumps({"company":"uber","data":L})
print(json_data)

    

