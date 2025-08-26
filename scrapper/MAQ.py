from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
import json
import requests
from bs4 import BeautifulSoup
import time

firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Chrome(options=firefox_options)
url = "https://careers.jobscore.com/careers/maqsoftware"
driver.get(url)
L=[]
driver.implicitly_wait(20)
time.sleep(3)
# num_str = driver.find_element(By.XPATH,"//p[@class='css-12psxof']").get_attribute("innerHTML")
# ns = ""
# for i in num_str:
#     if i not in "0123456789":
#         break
#     else:
#         ns+=i
# int_num = int(ns)
# count = 0
while True:
    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    total = soup.find_all("div",class_='js-job-departament-container')
    #print(total)
    # print(len(total))
    # print(total)
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("div",class_='js-job-department').text
        job_link = "https://careers.jobscore.com"+soup2.find("a")["href"]
        job_location = soup2.find("span",class_='js-job-location').text
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    # total = soup.find_all("li",class_='css-3hlofn')
    # for i in total:
    #     soup2 = BeautifulSoup(str(i),"html.parser")
    #     job_title = soup2.find("h3").text
    #     job_link = "https://careers.jobscore.com"+soup2.find("a",class_='css-19uc56f')["href"]
    #     job_location = soup2.find("span",class_='js-job-location').text
    #     L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    # time.sleep(3)
    try:
        elem = driver.find_element(By.XPATH,"//button[@class='css-ly8o31' and @aria-label='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
    except:
        break


cleaned_data = []

for item in L:
    cleaned_item = {
        "job_title": item["job_title"].strip(),
        "job_location": item["job_location"].strip(),
        "job_link": item["job_link"]
    }
    cleaned_data.append(cleaned_item)

print(cleaned_data)

    
json_data = json.dumps(cleaned_data)
# json_data = json.dumps({"company":"nvidia","data":L})
print(len(cleaned_data))

# print(int_num)
print(json_data)
driver.quit()





